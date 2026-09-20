# Matrix Metrics Summary

Use for multidimensional performance, capacity, stability, or regression matrices when the user requests a matrix summary, or when results include at least two input/load levels and two concurrency/QPS levels.

## Freeze matrix semantics

- Rows and columns must remain original contract dimensions. Text tests often use input length by concurrency or target QPS; other workloads may use image count, resolution, batch size, sequence length, or media duration. Never redefine cells for visual convenience.
- Freeze output length, streaming, Thinking or Reasoning, sampling, arrival pattern, cache state, retries, fallbacks, and timeout. Split or clearly mark matrices when any changes.
- Show only completed cells that pass data-quality checks. Label not-run, paused, invalid, and missing cells with text, never zero.

## Summary views

Use a separate panel for each metric on shared row and column coordinates:

1. **Aggregate Output TPS**: successful output tokens divided by complete-cell wall time, including queueing, failures, and visible retries.
2. **TTFT P95**: first-token latency under the frozen definition; state whether Thinking models use first Reasoning or first Content.
3. **TPOT P95**: P95 of per-request TPOT in ms/token.
4. **Success Rate**: successful requests divided by Started. Empty HTTP 200 responses, truncated streams, missing terminal events, wrong models, and fallback substitutions are failures.
5. **Per-request Output TPS P50**: compute each successful request's output rate using the frozen formula, then take P50 in tokens/s/request. Add P95 when long-tail behavior matters.

Add QPS, E2E P95/P99, unit cost, media throughput, or quality when needed. Never replace tail latency with means or mix per-request and aggregate TPS in one panel.

### Per-request and concurrency-one TPS

- Preferred streaming decode rate is `(completion_tokens - 1) / (last_token_time - first_token_time)`, equivalent to `1 / TPOT`. If only stream-end time is available, use `completion_tokens / (E2E - TTFT)`, but freeze the choice and never compare it directly with the first formula.
- Per-request Output TPS describes successful requests under shared load. It is not system throughput and not aggregate TPS divided by concurrency.
- A single-request or concurrency-one baseline requires a measured `concurrency=1` cell. Show per-request TPS, TTFT, E2E, and success separately. Mark missing data as not run; never infer it from high-concurrency cells.
- Do not calculate per-request TPS for empty output, no first token, or incomplete streams. Those requests still affect Success Rate and failure categories.

## Failures and capacity boundaries

- Always show Success Rate. Successful-request latency alone cannot prove a healthy cell.
- With failures, throughput still uses whole-cell wall time. Report Started, Completed, Success, Failed, Timeout, Retried, and empty or invalid responses.
- Identify platform, gateway, or client boundaries precisely, for example "HTTP 200, zero output, about 120 seconds," instead of guessing OOM or insufficient throughput.
- After a stop condition, mark later cells not run or paused. On authorized resume, preserve the original failure and record the new time window.

## Decision conclusion

State only supported conclusions: peak throughput and cell, throughput knee, maximum stable load meeting success and latency constraints, recommended default and optional batch levels, and limitations such as platform timeouts, background traffic, resumed windows, or single-round evidence. Without business thresholds, never turn visual green into an SLA pass.

## Excel or durable report

Prefer four sheets or sections:

1. **Matrix Summary**: core panels, per-request TPS P50, units, color direction, and short conclusions; add a measured concurrency-one panel when requested.
2. **Cell Details**: Started, Success, failure categories, P50/P95/P99/Max, aggregate TPS, per-request TPS, QPS, E2E, and status.
3. **Request Details**: request ID, input/output units, TTFT, TPOT, E2E, Usage, Finish Reason, terminal event, errors, and fallback evidence.
4. **Test Notes**: model, path, version, request contract, formulas, cache, arrival pattern, timeout, stop conditions, windows, and limitations.

Use formulas or links from Summary to Cell Details while preserving types and units. Conditional formatting aids scanning, but failures and missing data also need text status. Never include API keys, cookies, tokens, private keys, or unredacted request bodies.
