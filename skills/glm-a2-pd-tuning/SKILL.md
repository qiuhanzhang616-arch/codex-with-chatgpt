---
name: glm-a2-pd-tuning
description: Diagnose, benchmark, and safely tune GLM or GLM-Flash inference on Huawei Ascend A2 in ModelArts Standard, especially vLLM-Ascend deployments with prefill/decode disaggregation. Use for TTFT, TPOT, output TPS, long-context capacity, NPU/HBM/HCCL bottlenecks, PD topology, MTP, CUDAGraph, MLAPO, FlashComm1, Dynamic EPLB, load-balancing, or performance regressions in coding-agent workloads.
---

# GLM A2 PD Tuning

Use this workflow to produce evidence-backed tuning changes without confusing a saved script, a ModelArts UI label, and the process that is actually running.

## Operating rules

1. Treat read-only inspection as allowed. Before editing a deployment file, changing a ModelArts service, stopping traffic, restarting, scaling, or rolling back, obtain explicit approval from the user.
2. Before every approved change, back up the exact live files, record SHA-256 hashes, deployment ID, image digest, model/quantization, and the complete process command line. Make rollback executable before applying the candidate.
3. Never claim a candidate is active from its directory name. Verify the effective values from every running Prefill and Decode process and from startup logs.
4. Never call a configuration “best” until it passes performance, correctness, tool-calling, long-context, and stability gates. Preserve the previous configuration when any gate regresses.
5. Do not apply A3 examples to A2 merely because the model name matches. Verify that every environment variable and kernel path is supported by the deployed A2 image.
6. Do not expose API keys, SSH keys, passwords, cookies, or account identifiers in commands, logs, reports, or skill files.

## Phase 1: Freeze the test contract

Record these values before diagnosing or tuning:

- User workload: coding agent, chat, batch generation, or mixed.
- Model, weight format, quantization, image tag/digest, vLLM and vLLM-Ascend versions.
- A2 card count and physical node layout.
- Prefill and Decode topology separately: instances, cards per instance, DP, TP, EP, and local DP ranks.
- Model context limit and the operational admission limits.
- Input lengths, output length, concurrency, request count, arrival pattern, and timeout.
- Streaming mode, thinking policy, tool schema, sampling parameters, and stop conditions.
- Direct ModelArts path and gateway/LiteLLM path.
- Cold-prefix, warm-prefix, and mixed-prefix test groups.
- Required thresholds and quality dataset.

Use a full Cartesian matrix when the user gives multiple input lengths and concurrency levels. Do not silently reduce it. For coding, retain realistic decode lengths; a short output microbenchmark cannot establish coding-agent TPOT.

## Phase 2: Establish the actual baseline

Create a fact ledger with four columns: declared configuration, saved file, actual process, and observed metric. Resolve every mismatch before changing anything.

### Verify topology and runtime

- Count total cards as `instance count × cards per instance` for each inference unit.
- Inspect all Prefill and Decode pods, not only one representative pod.
- Inspect all local API/metrics ports. A physical Decode pod may host multiple DP ranks.
- Capture full process arguments, relevant environment variables, health status, image digest, model path, and startup timestamps.
- Confirm `max-model-len`, DP/TP/EP, `max-num-batched-tokens`, `max-num-seqs`, memory utilization, prefix caching, chunked prefill, speculative decoding, compilation mode, and additional Ascend options.
- Confirm that the load-balancing proxy advertises every Prefill and Decode endpoint.

### Measure both paths

Run the same payload directly against ModelArts and through LiteLLM or the application gateway. The difference isolates gateway, TLS, authentication, network, and client-side delay from model delay.

### Use consistent metric definitions

- TTFT: request start to the first streamed model token in either `reasoning_content` or `content`.
- TPOT: time between first and last generated token divided by `output_tokens - 1` when at least two tokens are present.
- Per-request output TPS: reciprocal of TPOT, based on decoded tokens.
- Aggregate output TPS: total decoded tokens divided by wall-clock duration of the whole concurrency cell.
- End-to-end latency: request start to final stream event.
- Success rate: valid completed responses divided by submitted requests. HTTP 200 with an empty stream is a failure.
- Correctness: deterministic execution or judge result on a fixed coding set; do not infer correctness from HTTP success.

Report P50 and P95 for TTFT, TPOT, and latency. Keep per-request TPS and aggregate TPS separate.

## Phase 3: Locate the bottleneck

Diagnose in this order so that one layer is not blamed for another:

1. **Routing and queueing**: request distribution per DP rank, active/waiting requests, queue time, admission control, retries, and empty streams.
2. **Prefill**: TTFT, prefix-cache hit rate, input throughput, chunked-prefill behavior, KV transfer delay, and long-context scaling.
3. **Decode**: TPOT, output TPS, CUDAGraph coverage, graph fallbacks, speculative acceptance, shared-expert overlap, and per-rank skew.
4. **Memory**: HBM allocation, KV-cache use, preemptions, recomputation, swap/offload, OOM, and fragmentation.
5. **Communication**: HCCL errors/retries, link utilization, collectives, FlashComm1/MC2 behavior, and PD transfer.
6. **MoE balance**: expert heat, token imbalance, stragglers, and whether Dynamic EPLB is supported and stable in this exact image.
7. **Client/gateway**: buffering, non-streaming calls, missing `reasoning_content`, TLS/auth delay, proxy timeout, and retry amplification.

Interpretation rules:

- Stable TTFT with worsening TPOT points to Decode, not Prefill.
- Zero preemptions, idle queues, and safe HBM during the sampled period weaken an HBM-capacity hypothesis; they do not prove capacity for a different concurrency/input cell.
- Low MTP acceptance can make speculative decoding slower. Compare MTP off, 1, 3, and 5 only when the image supports those modes.
- A request-level load balancer and Dynamic EPLB solve different problems. One balances requests across ranks; the other balances MoE expert placement/load.
- Strong request-count skew across Decode ranks can hide cold ranks during sparse traffic and expose them during bursts. Inspect all ranks before changing kernels.

Use `scripts/summarize_vllm_metrics.py` when Prometheus snapshots from multiple Decode ranks are available. It summarizes request distribution, average TPOT, queue time, preemptions, and MTP acceptance.

## Phase 4: Design candidates

Read [tuning-levers.md](references/tuning-levers.md) before choosing parameters. Change one independent variable at a time, or name an inseparable bundle and explain why it must be tested together.

Use this candidate order unless evidence points elsewhere:

1. Correct invalid or conflicting flags and remove hardware-generation mismatches.
2. Fix request routing and warm all ranks.
3. Tune Decode batching, sequence limit, and graph capture sizes around the observed concurrency distribution.
4. A/B speculative token count using acceptance and TPOT together.
5. Tune communication and supported MoE optimizations.
6. Revisit PD card allocation and DP/TP topology only after the lower-risk levers are understood.
7. Adjust memory utilization or maximum context only with long-context capacity evidence.

Do not lower the advertised context window to manufacture a performance win unless the user explicitly approves that product tradeoff. Do not disable thinking to claim kernel-level performance improvement; thinking policy is a separate workload mode and must be reported as such.

## Phase 5: Apply an approved candidate

Before the change:

- Save the original files in a timestamped, immutable backup directory.
- Record hashes and a machine-readable parameter diff.
- Confirm the rollback command does not depend on the candidate directory.
- Announce that this skill is pausing for approval if approval has not already been given.

After the change:

- Wait for every unit and rank to become ready.
- Verify actual process arguments on all ranks.
- Run non-streaming, streaming, reasoning-stream, tool-calling, and empty-stream checks.
- Confirm queues return to zero and no OOM, HCCL, graph/tiling, serialization, timeout, or process-restart errors appear.

## Phase 6: Validate and select

Run, in order:

1. Small smoke cell to catch startup and schema failures.
2. Same-restart A/B cells to reduce cache and runtime-age bias.
3. Cold-prefix and warm-prefix cells.
4. Full requested input × concurrency matrix.
5. Fixed coding correctness set, including tool calls.
6. Long-context boundary and recovery test.
7. Post-stress health and tool-call regression.

Accept a candidate only when:

- Required performance thresholds are met or the tradeoff is explicitly accepted.
- Success rate and correctness do not regress beyond the agreed tolerance.
- There are no empty HTTP 200 streams.
- No new OOM, preemption storm, HCCL, graph/tiling, or repeated restart appears.
- The service returns to a healthy idle state after stress.
- Results are reproducible in at least one same-condition repeat for material claims.

If any hard gate fails, restore the backup and verify the original runtime before continuing.

## Deliverables

Produce:

- Baseline fact ledger and topology/card accounting.
- Redacted original and candidate configurations with SHA-256 hashes.
- Candidate-by-candidate change log with accepted/rejected status.
- Matrix results for TTFT, TPOT, per-request TPS, aggregate TPS, latency, success, and correctness.
- Per-rank load, MTP acceptance, queue, KV/HBM, NPU, and communication findings.
- Errors and stability observations.
- Exact rollback procedure.
- A concise conclusion that separates measured facts, inference, and untested recommendations.

For the historical GLM-5.2 A2 tuning record that motivated these rules, read [prior-tuning-record.md](references/prior-tuning-record.md). Treat its values as evidence from one environment, not reusable defaults.
