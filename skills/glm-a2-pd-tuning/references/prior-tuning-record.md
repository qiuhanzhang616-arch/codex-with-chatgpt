# Prior GLM-5.2 A2 tuning record

This is a historical record from one 64-card A2 ModelArts deployment. It explains the workflow and failure modes that shaped this skill. Do not copy these values into another service without a fresh baseline.

## Workload and topology

- Workload: streaming coding-agent requests with PD separation.
- Total hardware: 64 Ascend A2 cards.
- Retained topology at the end of the 2026-09-01 cycle:
  - Prefill: DP4 × TP8 = 32 cards.
  - Decode: DP8 × TP4 = 32 cards.
- Model context limit during that cycle: 256,000 tokens.
- Quantization, model weights, sampling behavior, and LiteLLM public interface were not changed by the retained candidate.

## Baseline issues found

- Decode used `max-num-batched-tokens=8192`, which was Prefill-like for the targeted Decode-heavy coding workload.
- Fused MC2 and shared-expert multistream were both configured. Runtime warnings showed the combination disabled shared-expert overlap.
- An A3-specific environment flag existed in an A2 deployment.
- The smaller HCCL buffer and runtime identity settings were candidates for communication/jitter improvement.
- Saved scripts, UI labels, and actual process arguments had to be checked separately; directory names were not sufficient evidence.

## Candidate history

The labels below are experiment identifiers, not reusable tiers.

- **B0**: original configuration used for baseline.
- **C1**: official-style A2 alignment candidate. It reduced Decode batching, introduced MLAPO/Fused MC2 choices, and tested lower memory utilization.
- **C2**: added Dynamic EPLB to the C1 direction.
- **C3**: explored Decode DP4 × TP8 with Dynamic EPLB and a lower sequence limit.
- **C4**: isolated MLAPO while preserving more of the original runtime.
- **C5**: combined MLAPO and Dynamic EPLB.
- **C6**: retained A2-aligned candidate.
- **C7**: later Decode DP4 × TP8 test; rejected.
- **C8**: later Fused MC2 + Dynamic EPLB test; rejected.

Intermediate C1–C5 candidates informed the final selection but were not retained as production recommendations.

## Retained C6 changes

Only the Decode script changed materially:

1. `HCCL_BUFFSIZE`: 256 → 2560.
2. `max-num-batched-tokens`: 8192 → 256.
3. Enabled MLAPO.
4. Removed `VLLM_ASCEND_ENABLE_FUSED_MC2=1` so configured `multistream_overlap_shared_expert=true` could remain active.
5. Removed the A3-only `ASCEND_A3_ENABLE=1` flag.
6. Set `VLLM_HOST_IP` to the local service IP.
7. Changed `PYTHONHASHSEED` from 1234 to 0.

The following remained unchanged in that cycle:

- Prefill script and PD topology.
- `gpu-memory-utilization=0.95`.
- `max-model-len=256000`.
- Decode DP8 × TP4.
- Model weights, quantization, and sampling policy.

## Measured C6 result

In same-restart 8K comparisons using the same path, prompts, and output length:

- Concurrency 1: TTFT P50 3.392s → 3.223s; TPOT P50 63.30ms → 56.79ms; output throughput 14.06 → 15.61 tokens/s.
- Concurrency 8: TTFT P50 4.123s → 3.912s; TPOT P50 95.76ms → 85.00ms; aggregate output throughput 66.47 → 76.26 tokens/s.
- Interpreted improvement: roughly 10–11% lower TPOT and 11–15% higher output throughput in those cells.

Quality and stability gates:

- Fixed 20-problem HumanEval single run: 19/20 for C6 versus 10/20 baseline. This only established no observed regression; it was not treated as proof that runtime parameters improved model accuracy.
- Tool calling after stress: 5/5.
- 32K/16, 64K/8, 128K/2, and 192K/1 boundary cells completed without request failures.

## Rejected candidates and why

- **C7 Decode DP4 × TP8**: worse 8K/8 performance. At 32K/8, only 8 of 16 requests produced valid output; the others ended HTTP 200 with empty streams. Rolled back.
- **C8 Fused MC2 + Dynamic EPLB**: initially passed tool calls, then sustained load produced `GMM_tiling`, `Tiling failed`, and `ADD_TO_LAUNCHER_LIST_AICORE failed`. Rolled back.

These failures demonstrate that startup success and a small smoke test are insufficient.

## Later long-context experiment track

A separate 1M-context track was created later and must not be confused with the earlier C1–C8 labels. It tested, among other items:

- `max-model-len=1048576`.
- Decode batch tokens near 192, sequence capacity near 32, and memory utilization near 0.92.
- Decode MTP 5 versus MTP 3.
- Narrower graph capture sets around 1–32 active sequences.
- C8 reshape optimization and Prefill layer-sharding variants.

Those values are experiment inputs, not a recorded universal winner. Revalidate them with the current image, weights, 128K/48 target, and correctness gates.

## Later regression diagnosis pattern

In another read-only sample of the running 256K service:

- All eight Decode ranks had zero preemptions and idle queues after the workload.
- Request distribution was highly skewed: about 89% of requests landed on the first two ranks.
- Later/cold ranks showed higher average TPOT and lower MTP acceptance.
- MTP acceptance ranged roughly from the mid-50% range on colder ranks to about 72% on the hottest rank.

This supported a Decode routing/warmth/speculation hypothesis for burst degradation, not a general service outage or an HBM-capacity conclusion. The reusable lesson is to inspect all local rank ports and correlate request distribution with TPOT and MTP acceptance.
