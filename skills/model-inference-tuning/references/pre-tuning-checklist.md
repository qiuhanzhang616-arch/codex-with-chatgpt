# Pre-tuning Checklist

Use for every new project. Prefill known information and mark unknown technical items as read-only inspection allowed or pending confirmation.

## A. Tuning objective

1. What should improve: TTFT or first usable output, TPOT, end-to-end latency, system throughput, concurrency, context/input capacity, resource utilization, cost, or stability?
2. Which items are hard gates, with exact targets, and which are directional goals?
3. What must not regress: accuracy, Reasoning, Tool Calling, structured output, context capability, availability, or cost? What tolerance is allowed?
4. Prioritize single-request experience, total capacity, per-user fairness, and unit cost.

## B. Model and artifacts

1. What are the model name, version, immutable revision, and weight source?
2. Is it Dense or MoE, how large is it, what are active parameters and tasks, and does it use Reasoning?
3. What precision or quantization, tokenizer or processor, chat template, adapters, and custom code apply?
4. What are current and target context/input and output limits?
5. Are streaming, Reasoning, Tools, JSON, image, audio, video, Embedding, reranking, or speculative decoding required?

## C. Real business workload

1. Provide a real input, expected output, and success definition.
2. Is the workload online interaction, agent, batch, or mixed?
3. What are P50, P95, and maximum input and output sizes with units?
4. What are average, peak, and burst concurrency or QPS and session duration? Is it open-loop or closed-loop?
5. What streaming, Thinking or Reasoning, temperature, stop, tool, and retry policies apply?
6. What repeated prefixes, media or documents, cache-hit rate, conversation history, and request intervals occur?
7. Are preprocessing, retrieval, tool execution, and postprocessing included in user experience?

## D. Current platform and runtime

1. What platform, region/AZ, service type, and request path apply?
2. What accelerator model and generation, per-device memory, device count, nodes, CPU/RAM, and exclusivity apply?
3. What framework, version, image tag or digest, drivers, toolchain, and firmware apply?
4. What replicas and TP/DP/PP/EP/CP/PD topology are active?
5. What launch arguments, environment variables, batching, sequence, memory, cache, graph compilation, kernel, speculative, and communication settings are actually running?
6. What recent version, parameter, traffic, client, gateway, network, or data changes occurred?

## E. Current issue and measurement

1. Where is performance slow, when did it start, and under which request shapes?
2. What values are measured, with what formulas and timestamps?
3. Does the baseline use the same model artifact, hardware, path, requests, concurrency, cache, and time window?
4. Are there OOMs, preemptions, empty responses, retries, timeouts, restarts, communication errors, or kernel errors?
5. Does the client correctly handle streaming, Reasoning, Tool or JSON fields, and terminal events?

## F. Testing and quality

1. Is data real, public benchmark, or synthetic? Who provides it, and may it be retained?
2. Is correctness judged by tests, labels, recall or precision, schema, an evaluator, or humans?
3. What fixed prompt, sampling, seed, output length, and protocol apply?
4. What is the complete input × output × concurrency × mode matrix, request count, repeats, and maximum duration?
5. Do results represent cold, warm, cached, mixed, or steady-state traffic?

## G. Monitoring and bottleneck evidence

1. Are per-instance/rank requests, queues, caches, VRAM/HBM, utilization, communication, CPU, network, and errors visible?
2. Are request IDs or timestamps aligned across client, gateway, and model?
3. Are historical logs and metrics available for the regression period?
4. Is profiling allowed, with what overhead and window?

## H. Change and rollback authorization

1. Which layers may change: requests, gateway, runtime, topology, hardware, model artifacts, or quantization?
2. Are restarts, downtime, traffic switching, and scaling allowed, and in what window?
3. What maximum load, cost, resources, and duration apply?
4. What is the current stable version, backup location, rollback method, and rollback-time limit?
5. Which errors or metrics require immediate stopping, and who approves the final candidate?

## Confirmation before formal action

Show the user the scenario branch and workload, hard goals and quality limits, formulas, comparable baseline, full matrix and duration, candidate parameter family and first variable, affected objects, authorized downtime/resources/cost/load, backups, rollback and stop conditions, and remaining risks. Execute changes or formal stress only after confirmation.
