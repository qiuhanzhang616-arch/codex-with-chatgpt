# Pre-test Checklist

Use this questionnaire for every new test. Prefill known information and mark unknown technical items as pending read-only verification.

## A. Test purpose

1. Is the test functional, quality, performance, capacity, stability, regression, or resilience?
2. What exact question must it answer, and who will use the result for what decision?
3. What are the pass values, fail values, and non-regression requirements for each test type?
4. Does the result represent a POC, production commitment, release acceptance, or directional research?

## B. System under test

1. What are the model or service name, revision, quantization or precision, endpoint, and model alias?
2. What tokenizer or processor, chat template, adapters, and custom code apply?
3. What platform, region, hardware, device count, nodes, replicas, and parallel topology apply?
4. What framework, image digest, drivers or toolchain, and effective process arguments are running?
5. What is the comparison target, and are all factors except the target variable held constant?

## C. Real request path

1. What is the complete sequence through client, SDK or agent, enterprise authentication, gateway, load balancer, proxy, and model endpoint?
2. Are we testing the shortest model path, the real business path, or both?
3. Is the request streaming, and does middleware buffer or transform Reasoning, Tools, JSON, or media?
4. What are timeout, retry, fallback, connection reuse, and queue policies? Are fallbacks disabled for benchmarking?
5. Can one request ID align client, gateway, and model logs?

## D. Requests and data

1. Provide a real request, expected output, and success definition.
2. What are P50, P95, and maximum input sizes and units? What are the output distribution and limit?
3. Are prompt, system message, history, Reasoning, Tools, schema, temperature, seed, and stop conditions fixed?
4. What media counts, resolution, pages, frames, duration, codec, and preprocessing apply?
5. Is data unique, repeated, or mixed, and what cache-hit rate is expected?
6. Is data sensitive, may requests or responses be stored, and what redaction applies?

## E. Load matrix

1. What input, output, concurrency or QPS, and mode values must be tested?
2. Is load open-loop arrival rate or closed-loop concurrent sessions? What burst model applies?
3. What request count, duration, repeats, timeout, and random seed apply to each cell?
4. How are cold, warm, cached, mixed, and steady states defined?
5. What are the total cell count, expected duration, priority order, and screening permission?

## F. Metric definitions

1. Where does latency start and end, and what counts as the first usable output?
2. Does TTFT include Reasoning, and is time to first content also required?
3. What formulas define TPOT, ITL, throughput, QPS, concurrency, and end-to-end latency?
4. Which business unit applies to non-text tasks?
5. How are success, empty response, truncation, timeout, retry, cancellation, and fallback counted?
6. Should the report include P50/P95/P99/maximum, mean, or the full distribution?

## G. Quality judgment

1. What dataset or benchmark, version, and sample scope apply?
2. Is correctness judged by unit tests, labels, recall or precision, schema, an evaluator, humans, or media metrics?
3. Are dedicated Tool Calling, code execution, citation, long-context retrieval, or structured-output tests required?
4. Must quality and functionality be rerun after performance testing?

## H. Resources and observation

1. Is the load generator's location, CPU/network capacity, and client concurrency sufficient?
2. Can we collect model, per-instance/rank, queue, cache, VRAM/HBM, utilization, communication, CPU, network, and storage metrics?
3. Is there background traffic, and can the test window be isolated?
4. Is profiling allowed, and what overhead is acceptable?

## I. Safety and authorization

1. What maximum concurrency/QPS, duration, requests, cost, and resource use apply?
2. Which errors require immediate stopping, and how long should recovery be observed?
3. Are log reads, result storage, sensitive sample transmission, and public networking allowed?
4. If configuration changes are required, are change, restart, and rollback authorized?
5. Who approves formal start and final acceptance?

## Pre-start confirmation

Show the user the test question, pass criteria, tested version, comparable baseline, request path, data permissions, full matrix and duration, metric formulas, failure accounting, quality judgment, observation sources, maximum load, stop conditions, recovery requirements, open risks, and authorization status. Start formal testing only after confirmation.
