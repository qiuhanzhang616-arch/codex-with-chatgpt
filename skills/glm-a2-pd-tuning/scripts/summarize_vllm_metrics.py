#!/usr/bin/env python3
"""Summarize selected vLLM Prometheus metrics across Decode-rank snapshots."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path


SAMPLE_RE = re.compile(
    r"^(?P<name>[a-zA-Z_:][a-zA-Z0-9_:]*)"
    r"(?:\{(?P<labels>.*)\})?\s+"
    r"(?P<value>[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?|NaN|Inf|-Inf)"
    r"(?:\s+\d+)?$"
)
LABEL_RE = re.compile(r'(\w+)="((?:\\.|[^"\\])*)"')


ALIASES = {
    "generation_tokens": ("generation_tokens_total",),
    "tpot_count": ("request_time_per_output_token_seconds_count",),
    "tpot_sum": ("request_time_per_output_token_seconds_sum",),
    "queue_count": ("request_queue_time_seconds_count",),
    "queue_sum": ("request_queue_time_seconds_sum",),
    "preemptions": ("num_preemptions_total",),
    "draft_tokens": ("spec_decode_num_draft_tokens_total",),
    "accepted_tokens": ("spec_decode_num_accepted_tokens_total",),
    "running": ("num_requests_running",),
    "waiting": ("num_requests_waiting",),
}


def metric_matches(name: str, suffixes: tuple[str, ...]) -> bool:
    return any(name == suffix or name.endswith(":" + suffix) or name.endswith("_" + suffix) for suffix in suffixes)


def parse_labels(raw: str | None) -> dict[str, str]:
    if not raw:
        return {}
    return {key: bytes(value, "utf-8").decode("unicode_escape") for key, value in LABEL_RE.findall(raw)}


def rank_name(path: Path, labels: dict[str, str]) -> str:
    for key in ("engine", "engine_id", "rank", "data_parallel_rank", "instance", "pod"):
        if labels.get(key):
            return labels[key]
    return path.stem


def collect(path: Path) -> dict[str, dict[str, float]]:
    ranks: dict[str, dict[str, float]] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = SAMPLE_RE.match(line)
        if not match:
            continue
        try:
            value = float(match.group("value"))
        except ValueError:
            continue
        if not math.isfinite(value):
            continue
        name = match.group("name")
        labels = parse_labels(match.group("labels"))
        logical = next((key for key, suffixes in ALIASES.items() if metric_matches(name, suffixes)), None)
        if logical is None:
            continue
        rank = rank_name(path, labels)
        ranks.setdefault(rank, {}).setdefault(logical, 0.0)
        ranks[rank][logical] += value
    return ranks


def merge(target: dict[str, dict[str, float]], source: dict[str, dict[str, float]], prefix: str) -> None:
    for rank, values in source.items():
        output_rank = rank if rank not in target else f"{prefix}:{rank}"
        target[output_rank] = values


def derived(values: dict[str, float]) -> dict[str, float | None]:
    tpot_count = values.get("tpot_count", 0.0)
    queue_count = values.get("queue_count", 0.0)
    draft = values.get("draft_tokens", 0.0)
    return {
        **values,
        "avg_tpot_ms": values.get("tpot_sum", 0.0) / tpot_count * 1000 if tpot_count else None,
        "avg_queue_ms": values.get("queue_sum", 0.0) / queue_count * 1000 if queue_count else None,
        "mtp_acceptance_pct": values.get("accepted_tokens", 0.0) / draft * 100 if draft else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path, help="Prometheus files or directories containing *.prom/*.txt")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of a text table")
    args = parser.parse_args()

    files: list[Path] = []
    for item in args.inputs:
        if item.is_dir():
            files.extend(sorted(item.glob("*.prom")))
            files.extend(sorted(item.glob("*.txt")))
        elif item.is_file():
            files.append(item)
    if not files:
        parser.error("no readable metric files found")

    ranks: dict[str, dict[str, float]] = {}
    for path in files:
        merge(ranks, collect(path), path.stem)

    enriched = {rank: derived(values) for rank, values in sorted(ranks.items())}
    total_requests = sum(values.get("tpot_count", 0.0) for values in ranks.values())
    for values in enriched.values():
        count = values.get("tpot_count", 0.0) or 0.0
        values["request_share_pct"] = count / total_requests * 100 if total_requests else None

    if args.json:
        print(json.dumps({"files": [str(path) for path in files], "ranks": enriched}, indent=2, ensure_ascii=False))
        return 0

    header = f"{'rank':<24} {'requests':>10} {'share%':>8} {'avg_tpot_ms':>12} {'avg_queue_ms':>13} {'mtp_accept%':>12} {'preempt':>9}"
    print(header)
    print("-" * len(header))
    for rank, values in enriched.items():
        def fmt(key: str, width: int, decimals: int = 2) -> str:
            value = values.get(key)
            return f"{'-':>{width}}" if value is None else f"{float(value):>{width}.{decimals}f}"

        print(
            f"{rank:<24}"
            f"{fmt('tpot_count', 10, 0)}"
            f"{fmt('request_share_pct', 8)}"
            f"{fmt('avg_tpot_ms', 12)}"
            f"{fmt('avg_queue_ms', 13)}"
            f"{fmt('mtp_acceptance_pct', 12)}"
            f"{fmt('preemptions', 9, 0)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
