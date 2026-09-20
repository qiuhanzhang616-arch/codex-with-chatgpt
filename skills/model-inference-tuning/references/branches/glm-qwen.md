# GLM/Qwen Tuning Branch

Load only for GLM, GLM-Flash, CodeGeeX, Qwen, Qwen-Coder, Qwen-VL, and related families. This file provides no cross-project default parameters.

## Confirm first

- Exact model revision, Dense or MoE architecture, active parameters, Reasoning, MTP or draft capability, and quantization.
- Hardware generation, runtime image, and explicitly supported kernel and communication optimizations.
- Alignment among chat template, Reasoning Parser, Tool Parser, and client fields.
- Effective context, batching, sequence, memory, parallel topology, cache, and graph-compilation settings from actual processes.

## GLM branch

- Streaming TTFT ends at the first Reasoning token; report first Content token separately when the business needs it.
- For coding or agents, emphasize Decode TPOT, MTP acceptance, Tool Calling, empty streams, and completion time; for long context, also measure Prefill and KV behavior.
- A/B MLAPO, FlashComm, Fused MC2, Shared Expert Multistream, Dynamic EPLB, sparse C8, MTP, and PD only for the current model/image/hardware combination.
- Request load balancing and Dynamic EPLB address request distribution across ranks and MoE expert load respectively; never treat them as one function.
- Inspect every DP rank and local port because averages can hide cold ranks, hot ranks, and MTP-acceptance skew.

### Historical A2 PD coding case

In one 64-device A2 deployment using GLM-5.2 W4A8C8, Prefill DP4×TP8, and Decode DP8×TP4, a retained candidate reduced Decode batch tokens from 8192 to 256, increased HCCL buffers, enabled MLAPO, resolved a Fused MC2 and Shared Expert Multistream conflict, and removed A3-only parameters. In a specific same-restart 8K test, TPOT improved about 10%–11% and output throughput about 11%–15%.

These numbers describe that project's experiment method only. A later Decode DP4×TP8 candidate was rejected for empty streams and performance; Fused MC2 plus Dynamic EPLB was rejected for sustained-load GMM/Tiling errors. Never reuse these values as defaults.

## Qwen branch

- Distinguish text, Coder, MoE, VL, and Audio variants because processors, workload, and metrics differ.
- Verify Thinking, Tool Calling, structured output, and streaming fields in the target client.
- For Qwen-VL, measure media preprocessing, visual tokens, processor cache, and text Decode separately.
- For MoE, emphasize expert/rank imbalance, communication, tails, and kernel support; never apply EPLB assumptions to Dense variants.

## Promotion gates

- Performance gains reproduce with the same cache, path, and output length.
- Required Tool, JSON, Reasoning, and multimodal capabilities do not regress.
- No new empty responses, OOM, communication, graph-compilation or kernel errors, restarts, or recovery failures.
