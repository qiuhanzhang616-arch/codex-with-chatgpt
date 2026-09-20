# Workload and Metric Branches

## Online text or chat

- Focus on first usable token, TPOT or ITL, end-to-end latency, conversation experience, output throughput, and success rate.
- Freeze conversation history, Reasoning, streaming, output length, and stop conditions.
- Test both steady and burst traffic.

## Coding or tool-using agents

- Focus on first Reasoning or Content token, TPOT, task duration, tool correctness, iteration count, task success, and executable correctness.
- Token microbenchmarks locate engine effects but never replace real repository or sandbox tasks.
- Separate model, tool, repository I/O, context construction, agent orchestration, and gateway time.

## Long context or RAG

- Focus on TTFT, Prefill throughput, retrieval latency, KV/cache capacity and hit rate, stable concurrency, distant-evidence correctness, and recovery.
- Stratify by real token distribution and prefix reuse, separating cold and warm results.
- Maximum context capability does not imply high concurrency at that context.

## Offline batch

- Focus on work items/s, token or media throughput, makespan, utilization, failures/retries, and unit cost.
- Use fixed backlog or open-loop arrival and include failures in whole-batch results.

## Vision-language, document, or video understanding

- Focus on requests/s, images/pages/frames/video-seconds/s, preprocessing, visual tokens, end-to-end latency, memory, and quality.
- Freeze image count, resolution, pages, frame sampling, codec, transport, OCR, and output schema.
- Repeated-media cache results cannot represent unique-document traffic.

## Embedding or reranking

- Focus on queries/s, documents/s, P50/P95/P99, padding waste, maximum sequence, memory, recall/nDCG/MRR, and cost.
- Do not use generative TTFT or TPOT definitions.

## Speech

- Focus on realtime factor, first partial or audio, audio-seconds/s, end-to-end latency, WER or task quality, and streaming stability.
- Freeze sample rate, channels, duration, chunks, VAD, language, and codec.

## Image or video generation

- Focus on first preview, generation latency, samples/s, pixels or frames/s, utilization, memory, failures, and quality.
- Freeze resolution, duration, steps, sampler, guidance, seed, and postprocessing.

## Structured output or Function Calling

- As a cross-cutting branch, measure schema validity, tool selection, argument accuracy, recovery behavior, and empty responses.
- Revalidate after stress rather than relying only on startup smoke tests.

Parameter names and ranges must come from the current model, runtime, and hardware. Branches define questions and metrics, not fixed best values.
