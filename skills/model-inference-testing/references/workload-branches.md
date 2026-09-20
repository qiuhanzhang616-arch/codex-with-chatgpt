# Workload Test Branches

## Online text or chat

- Measure TTFT, first content, TPOT or ITL, end-to-end P50/P95/P99, output throughput, success, and conversation continuity.
- Cover short, medium, and long history, Reasoning modes, streaming, and burst sessions.

## Coding or agents

- In addition to token metrics, measure task duration, step count, Tool Calls, code execution, test pass, error recovery, and cost.
- Use executable short, medium, and long tasks; never represent long-horizon agents with only trivial function-writing microbenchmarks.

## Long context or RAG

- Test actual required levels such as 8K, 32K, 64K, 128K, and longer.
- Measure cold and warm prefixes, TTFT, Prefill, KV/cache behavior, stable concurrency, distant-evidence recall, and answer correctness.

## Offline batch

- Measure makespan, work items/s, token or media throughput, utilization, failures/retries, and unit cost.
- Use a fixed backlog or open-loop rate and report whole-batch results.

## VLM, document, or video

- Stratify by image count, resolution, pages, frames, video duration, and media tokens.
- Separate preprocessing, transport, model, and output stages. Report requests/s and images/pages/frames/s plus task quality.

## Embedding or reranking

- Measure queries/s, documents/s, batch size, padding, latency, recall/nDCG/MRR, and cost.

## Speech

- Measure RTF, first partial or audio, streaming jitter, audio-seconds/s, end-to-end latency, and WER or task quality.

## Image or video generation

- Measure generation latency, samples/s, pixels or frames/s, memory, utilization, failure, and quality while freezing steps, resolution, sampler, and seed policy.

## Structured output or Tools

- Measure schema validity, tool selection, argument correctness, parallel Tool Calls, empty output, and post-stress regression.

Choose units and evaluators per branch; never force token metrics across incompatible workloads.
