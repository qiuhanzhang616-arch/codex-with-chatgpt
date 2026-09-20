---
name: model-inference-testing
description: >
  Design, execute, and review reproducible functional, performance, capacity,
  stability, quality, and regression tests across models, APIs, inference
  frameworks, hardware, and business scenarios. Clarify the test purpose,
  request semantics, metric formulas, matrix, baseline, and pass criteria first.
  By default, test and collect evidence only: do not tune, restart, scale, or
  hide failures with fallbacks. Treat GLM, Qwen, agent protocols, and
  multimodal protocols as separate branches.
---

# Model Inference Testing

Use frozen requests, environments, and metric definitions to answer whether a specific version passes in a specific scenario. This skill does not search for optimal parameters or treat results from different models, paths, cache states, or clients as directly comparable.

## First step: clarify before acting

For a new test, benchmark, load test, capacity validation, or performance comparison, first read the complete [pre-test checklist](references/pre-test-checklist.md).

1. Prefill answers from the conversation, files, and read-only evidence, then ask the user to confirm them.
2. Do not start formal testing while the system under test, real workload, metric formulas, matrix, quality criteria, or safety limits remain unclear.
3. Use read-only inspection to establish unknown runtime versions, effective parameters, and monitoring capability. Record remaining unknowns as risks.
4. Before sending formal load, consuming paid resources, reading sensitive data, or running destructive or fault tests, present the complete test contract and obtain authorization.
5. By default, do not change model, gateway, agent, or deployment configuration. If a test variant requires a change, treat it as a separate system-under-test version and obtain change and rollback authorization.

## Define the test types

- **Functional**: API behavior, streaming, Reasoning, Tools, JSON, Embedding, multimodal capabilities, and related semantics.
- **Quality**: task accuracy, recall or precision, schema conformance, judge scores, human review, or media quality.
- **Performance**: latency, throughput, and resource efficiency.
- **Capacity**: stable concurrency or QPS, maximum input or context, queues, and recovery.
- **Stability**: sustained load, error rate, memory or cache drift, restarts, and recovery.
- **Regression**: same-condition comparison with a clearly identified historical or candidate version.
- **Resilience**: instance, network, upstream, or dependency failures; inject faults only with explicit authorization.

A project may combine test types, but each needs its own pass criteria.

## Freeze the test contract

Use the [test plan and baseline template](references/test-plan.md) to record and confirm:

- tested model, service, version, actual artifacts, and runtime environment;
- complete client-to-model path and control path;
- request protocol, prompt, sampling, streaming, Reasoning, Tools, and termination semantics;
- input, output, concurrency or QPS, arrival pattern, cache state, and data-reuse distributions;
- full matrix, request counts, repeats, random seeds, timeouts, and maximum duration;
- metric formulas, collection points, aggregation methods, and thresholds;
- quality judgment, test-data permissions, and privacy handling;
- maximum load, cost, stop conditions, and recovery requirements.

Expand multidimensional requirements into the full Cartesian product and state the total number of cells. If screening comes first, define separate screening and formal matrices and obtain user approval. Never present screening results as complete acceptance.

## Establish a comparable baseline

Before testing, confirm:

- model revision, quantization or precision, tokenizer or processor, templates, and adapters;
- image, framework, drivers, toolchain, and effective process arguments;
- hardware, nodes, replicas, topology, and resource exclusivity;
- gateway, authentication, network, client, and load generator;
- service idleness or background traffic, cache state, warm-up, and compilation state;
- health, queues, restarts, errors, and clock synchronization.

For comparison tests, keep every factor except the compared variable constant. If that is impossible, label the result directional, list confounders, and do not report an exact improvement percentage.

Where possible, preserve both the shortest model path and the real business path. The former isolates the model, while the latter represents user experience. Never mix their results in one column.

## Select branches and metrics

Read the relevant [workload branches](references/workload-branches.md). For GLM or Qwen, also read the [GLM/Qwen testing branch](references/branches/glm-qwen.md).

General statistical rules:

- Report submitted, started, completed, successful, failed, timed-out, retried, and empty or invalid responses.
- Report at least P50, P95, P99, maximum latency, and either the complete distribution or raw details.
- Calculate system throughput over whole-round wall time, including failures, queueing, and retries.
- Keep per-request generation rate separate from aggregate throughput.
- For streaming reasoning models, TTFT ends at the first `reasoning_content` or equivalent model increment. Report time to first content token separately when required.
- For non-token models, use business units rather than forcing TTFT or TPOT.
- Treat HTTP 200 with no valid content, reasoning, tool call, embedding, or media output as failure.

## Execution order

1. **Connectivity and version snapshot**: excluded from scores.
2. **Functional smoke test**: validate protocol, fields, terminal events, and target capabilities.
3. **Cold start or first compilation**: record separately.
4. **Warm-up**: reach a predefined steady state; preserve anomalies but separate them from formal rounds.
5. **Formal matrix**: use a fixed or randomized order and record background traffic and resources.
6. **Repeated rounds**: validate material differences and tail latency.
7. **Capacity or sustained stress**: increase load stepwise and stop new requests immediately at a stop condition.
8. **Recovery and post-stress functional regression**: confirm queue, memory, instance, and feature recovery.

Do not poll long-running tests at high frequency. Preserve PIDs, logs, checkpoints, manifests, and completed cells so the run can resume. When the user requests a pause, stop new cells immediately and save current results.

## Data-quality checks

Before reporting results, verify:

- request counts match detail-row counts;
- token or media count provenance is explicit;
- timestamps use a monotonic clock and cross-machine analysis confirms synchronization;
- failures, cancellations, retries, and fallbacks are not hidden;
- cache hits and background traffic match their labels;
- there is no output truncation, empty stream, wrong model, wrong endpoint, or wrong dataset;
- averages do not replace tail latency, and peaks do not masquerade as sustained capacity;
- accuracy uses a fixed sample set and a reviewable judgment.

If definitions or data are invalid, mark the cell invalid and rerun it. Never massage numbers to make a test pass.

## Stop conditions

Stop adding load when any user-confirmed condition occurs:

- OOM, process or instance death, or repeated restart;
- communication, kernel, graph-compilation, or data-corruption errors;
- error rate, timeout, tail latency, queue, or resource use exceeds its safety limit;
- output quality or required functionality fails;
- time, cost, request, or load budget is exhausted;
- the service does not recover within the required time.

A failed test does not authorize tuning. Preserve evidence and report the failure without changing production configuration.

## Deliverables

When results include at least two input or load levels and at least two concurrency or QPS levels, or the user requests a matrix metrics summary or Excel summary, read the [matrix metrics summary](references/matrix-summary.md). The summary is a decision view that must drill down to cell summaries and request details; it never replaces raw evidence.

- Questionnaire answers, open items, and test contract.
- Environment, version, and effective-configuration baseline.
- Full matrix and every cell's status.
- Locations of raw request-level data, logs, and resource metrics.
- Performance, capacity, stability, quality, and functional results.
- Invalid data, failures, limits, and confounders.
- Pass or fail conclusion with evidence.
- Reproducible commands, resume procedure, and next recommendations.

Use consistent units, formulas, and language. Never include passwords, API keys, cookies, OTPs, private keys, or sensitive request bodies in the report.
