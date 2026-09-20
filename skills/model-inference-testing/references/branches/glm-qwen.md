# GLM/Qwen Testing Branch

Use for GLM, GLM-Flash, CodeGeeX, Qwen, Qwen-Coder, Qwen-VL, Qwen-Audio, and related MoE or quantized variants.

## Protocol baseline

- Freeze model alias, chat template, Reasoning or Thinking, Tool schema, streaming, and sampling.
- Preserve raw SSE or responses, not only client-rendered text.
- Confirm that every layer preserves `reasoning_content`, `content`, Tool Calls, Finish Reason, Usage, and error codes.
- Treat HTTP 200 with an empty stream or control events only as failure.

## GLM

- Measure TTFT to first Reasoning or Content increment and optionally time to first Content separately.
- For coding, report TPOT, aggregate output TPS, agent duration, tool correctness, and execution correctness.
- For MoE, PD, or MTP, collect per-Prefill/Decode-rank requests, queues, KV/HBM, communication, and MTP acceptance.
- Increase long-context load stepwise; a single request at the maximum window does not prove high-concurrency safety.

## Qwen

- Distinguish text, Coder, MoE, VL, and Audio variants and use their correct processors and units.
- For Qwen-VL, freeze image or video shapes and report preprocessing separately from model latency.
- For Qwen-Coder or Tool scenarios, use executable tests and argument validation, not semantic judges alone.
- A Thinking-mode change creates a separate test series.

## Comparison requirements

For GLM versus Qwen, freeze task, prompt, target output, context, output limit, Reasoning mode, endpoint path, concurrency, arrival pattern, cache state, test window, failure definition, and quality judgment. If capabilities prevent exact control, report both same-business-goal and same-compute-budget views instead of one overall winner.
