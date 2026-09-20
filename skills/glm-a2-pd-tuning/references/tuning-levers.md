# GLM on Ascend A2 PD tuning levers

Use this catalog to form hypotheses. A parameter is not recommended merely because it exists or worked in another image.

## Prefill-side levers

- **PD topology and card allocation**: More Prefill capacity can reduce long-input queueing and TTFT, but removes cards from Decode. Account for physical nodes and communication boundaries.
- **`max-num-batched-tokens`**: Larger values can improve Prefill throughput but may worsen latency, HBM pressure, and fairness. Test against the real 64K–256K distribution.
- **`max-num-seqs`**: Set from concurrent sequence capacity, not team headcount. Long contexts consume disproportionate KV cache.
- **Chunked prefill**: Usually useful for long-context fairness; verify chunk size behavior and interaction with batching.
- **Prefix caching**: Preserve for repeated repository/system prefixes, but report cold and hot results separately.
- **FlashComm1 and DSA CP**: Candidate communication optimizations for supported A2 images. Verify the startup log confirms activation.
- **Layer sharding**: Image/model-specific. Test correctness, HBM balance, and communication before retaining it.
- **Prefill speculative settings**: Do not assume Decode-oriented MTP settings help Prefill.

## Decode-side levers

- **DP/TP shape**: More DP ranks can raise concurrency throughput; larger TP can reduce per-rank weight footprint but add collectives. Compare with the same total cards and workload.
- **`max-num-batched-tokens`**: Decode-heavy coding can benefit from a much smaller value than a Prefill-oriented default. Too small may underutilize the device; too large may increase TPOT and scheduling work.
- **`max-num-seqs`**: Size to the operational concurrency envelope and graph shapes. Large advertised capacity is not free capacity.
- **CUDAGraph `FULL_DECODE_ONLY`**: Useful for stable Decode shapes when supported. Capture sizes should cover observed active batch sizes; excessively broad capture lists increase warm-up and memory cost.
- **MLAPO**: Candidate for MoE Decode performance. Confirm it is supported and active in the exact runtime.
- **Shared-expert multistream overlap**: Can improve overlap, but may conflict with Fused MC2 in some vLLM-Ascend versions. Read startup warnings; a configured flag can be disabled at runtime.
- **Fused MC2**: Do not enable together with conflicting shared-expert overlap settings. Test for kernel/tiling failures under sustained load.
- **Dynamic EPLB**: Expert-level balancing, not request-level balancing. Run a sustained warm-up and inspect expert/rank distribution before measuring. Reject on instability or unsupported kernels.
- **MTP/speculative decoding**: Test disabled and supported token counts. Keep only when acceptance-adjusted TPOT and aggregate TPS improve without correctness or tool-call regression.
- **Sparse SFA/LI C8, C8 reshape, INT8 per-token head**: Quantized-kernel candidates that must match the weight format and image.
- **CPU binding and static host IP**: Reduce orchestration jitter and communication ambiguity; verify NUMA and container CPU allocation.
- **HCCL buffer**: A larger buffer may improve communication-heavy Decode but consumes memory. Test HBM headroom and HCCL behavior.
- **Recompute scheduler**: Can protect memory but may trade compute for capacity. Correlate with preemption and TPOT.

## Cross-cutting levers

- **`gpu-memory-utilization`**: Do not maximize blindly. Higher values increase KV capacity but reduce headroom for graphs, workspaces, fragmentation, and bursts.
- **`max-model-len`**: A capability boundary, not a throughput knob. Validate the maximum with low concurrency, then use admission pools for long requests.
- **Quantization**: Changing W4A8/W8A8/C8 is a model artifact and accuracy decision, not a minor runtime tuning step.
- **Load-balancer policy**: Track request counts and active tokens per Decode rank. Deterministic tie-breaking can create hot and cold ranks.
- **Retries/timeouts**: Retries can amplify overload. Keep gateway diagnosis separate from model execution, and do not hide model failures with fallback during benchmark cells.
- **Thinking policy**: Benchmark on/off or effort levels as distinct workload modes. Count the first `reasoning_content` token as first model output.

## Evidence required before retaining a lever

For each lever record:

1. Supported by which image/version and startup confirmation.
2. Exact Prefill or Decode scope.
3. Performance delta under same conditions.
4. Correctness/tool-call delta.
5. HBM, queue, NPU, HCCL, and error impact.
6. Whether a repeat reproduced the result.
