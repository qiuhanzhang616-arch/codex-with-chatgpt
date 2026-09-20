---
name: model-inference-tuning
description: Design and execute rollback-safe inference performance tuning across models, accelerators, inference frameworks, deployment platforms, and business workloads. Use to improve latency, throughput, concurrency, context capacity, resource utilization, cost, or stability. Clarify the business objective, real workload, current configuration, and quality constraints first, then establish a comparable baseline before changing parameters. Load GLM, Qwen, hardware-specific, and historical-result branches only when relevant.
---

# Model Inference Performance Tuning

The goal is to find the best stable configuration among candidates validated under the current project's constraints, not to produce a universal best parameter set. Any change to the model, weights, precision, hardware, runtime, request shape, traffic, or quality standard may define a new experiment domain.

## First step: clarify before acting

For a new tuning, performance regression, or capacity optimization request, first read the complete [pre-tuning checklist](references/pre-tuning-checklist.md).

1. Prefill known answers from the conversation, files, and read-only runtime evidence, then ask the user to confirm them.
2. Until objectives, workload, metric definitions, quality limits, and variable parameters are clear, do not give final parameter values or modify the service.
3. Use read-only inspection to establish process arguments, versions, topology, and monitoring data. Do not ask the user to provide information you can inspect; mark remaining unknowns explicitly.
4. Before changing parameters, restarting, scaling, or sending substantial load, present the experiment contract, change target, expected duration, stop conditions, and rollback point, then obtain authorization.

## Select workload branches

Read the relevant section of [workload and metric branches](references/workload-branches.md) for the real work item:

- online text or chat;
- coding or tool-using agents;
- long-context or RAG;
- offline batch;
- vision-language, document, or video understanding;
- embedding or reranking;
- speech;
- image or video generation;
- structured output or Function Calling.

A project may combine branches, but each branch retains its own input distribution, performance metrics, and quality gates. For GLM or Qwen, also read the [GLM/Qwen tuning branch](references/branches/glm-qwen.md).

## Freeze the tuning contract

Use the [baseline and experiment template](references/tuning-baseline.md) to record and confirm:

- model artifacts, precision, runtime, hardware, and actual topology;
- complete request path and measurement points;
- input and output distributions, concurrency or QPS, cache state, and full matrix;
- metric formulas and quality and stability limits;
- permitted parameter families, resources, downtime, and test budget;
- baseline version, backups, stop conditions, and rollback target.

Expand multiple input lengths, output lengths, concurrency levels, and modes into the full Cartesian product. State the cell count, repeat count, and expected duration. If cost is high, propose a screening stage followed by full validation, but obtain approval and never silently reduce coverage.

## Establish a trustworthy baseline

Create a four-column fact ledger:

1. configuration the user believes is active;
2. saved script or console configuration;
3. actual process, environment, loaded artifacts, and logs;
4. observed metrics under the frozen workload.

Resolve discrepancies before tuning. A directory name, configuration file, console label, or successful startup does not prove a parameter is active.

When possible, send identical requests through both the shortest model path and the real business path. Separate client, preprocessing, authentication, gateway, network, queueing, retries, inference, and postprocessing. For distributed runtimes, inspect every instance and rank rather than relying on global averages.

The baseline includes at least:

- passing functionality and quality;
- defined cold, warm, and mixed cache states;
- request-level P50/P95/P99 and system throughput;
- successful, failed, timed-out, retried, and empty responses;
- accelerator, VRAM or HBM, communication, CPU, network, storage, queue, and cache observations;
- post-stress recovery and health.

## Form candidates from bottleneck evidence

Select parameter families only from evidence:

1. Request construction, preprocessing, and output policy.
2. Admission, queueing, batching, and scheduling.
3. Replicas and TP/DP/PP/EP/CP/PD topology.
4. Context or input limits, cache, and memory allocation.
5. Kernels, Attention, graph compilation, speculative decoding, MoE, and communication optimizations.
6. Precision or quantization only when the user accepts the tradeoff and quality gates are explicit.
7. Client, gateway, transport, streaming, timeout, and retry behavior.

For each candidate, record the unique change, hypothesis, expected metric direction, possible side effects, test method, promotion criteria, and rollback criteria. Change one independent variable at a time. Declare parameters that must change together as a Bundle.

Confirm hardware-generation, architecture, and runtime-specific parameters through support evidence for the current image and version plus startup logs. Never copy values directly from another model, accelerator, or region.

## Metric discipline

- Never mix per-request TPS with aggregate TPS.
- For streaming reasoning models, TTFT ends at the first `reasoning_content` or equivalent model increment. If the business requires final content, report time to first content separately.
- Calculate TPOT only for requests with at least two output tokens and preserve the formula.
- Whole-round wall time includes failures, queueing, and retries; a successful subset cannot represent the SLA.
- For non-token models, use requests/s, images/s, pages/s, frames/s, audio-seconds/s, samples/s, or another appropriate unit.
- Validate correctness, Tool Calling, schema conformance, recall, or media quality together with performance.

Never manufacture a performance gain by shrinking real inputs, shortening outputs, disabling Reasoning, reducing context capability, changing cache reuse, hiding failures, or enabling fallbacks. If the user accepts one of these business tradeoffs, create a separate result series and label it clearly.

## Safe execution and rollback

Before a change:

- preserve the actual live files, image or artifact, complete process arguments, and hashes;
- prepare rollback steps that do not depend on the candidate directory;
- confirm the authorized components, downtime, resources, cost, duration, and load range.

Execution order:

1. Functional smoke test and quality gates.
2. Warm-up and lazy-compilation characterization.
3. Small candidate screening.
4. Same-condition baseline and Candidate A/B.
5. Full matrix and quality testing.
6. Boundary, sustained stress, and recovery.
7. Post-stress functional, health, and error regression.

On OOM, process death, communication or kernel error, empty response, quality violation, uncontrolled retries, or failed recovery, stop sending new load and roll back according to the contract. If the user asks to pause, stop new requests immediately and do not extend previous authorization to another candidate.

## Promotion and delivery

Promote a candidate only when it meets performance objectives, success-rate, quality, stability, and recovery requirements, and material gains reproduce at least once. Deliver:

- questionnaire answers, open items, and the tuning contract;
- baseline fact ledger;
- parameter diff, hypothesis, result, and conclusion for every candidate;
- full-matrix performance, quality, failure, and resource data;
- accepted and rejected candidates with reasons;
- current effective runtime state, backups, and rollback procedure;
- explicit separation of measured facts, reasonable inference, and untested recommendations.

Call the result only the best stable configuration among the candidates tested in this round. Never claim a global optimum. Reports must not contain passwords, API keys, cookies, OTPs, or private keys.
