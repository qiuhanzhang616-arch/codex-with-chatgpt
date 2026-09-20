# Tuning Baseline and Experiment Template

## Project and scenario

- Project/environment:
- Workload branch:
- Real work item:
- Tuning objectives and priorities:
- Hard gates/non-regression requirements:

## Effective runtime baseline

- Model, revision, precision/quantization:
- Tokenizer/processor/template:
- Platform, hardware, devices, nodes:
- Framework, image digest, drivers/toolchain:
- Replicas and parallel topology:
- Effective process arguments and environment:
- Request path and measurement points:
- Health, errors, and resources:
- Evidence timestamp:

## Workload contract

- Input distribution:
- Output distribution:
- Concurrency/QPS/arrival:
- Streaming/Reasoning/Tools/sampling:
- Cache state:
- Test data and quality judgment:
- Requests, repeats, and timeout:

## Metric definitions

| Metric | Formula | Start | End | Aggregation | Gate |
|---|---|---|---|---|---|

## Candidate record

| Candidate | Parent | Unique change/Bundle | Hypothesis | Risk | Promotion criteria | Rollback criteria |
|---|---|---|---|---|---|---|

## Change authorization

- Mutable components:
- Downtime/restart/traffic switch:
- Resource, cost, and duration limits:
- Stop conditions:
- Approval status:

## Backup and rollback

- Known stable version:
- File/image/artifact hashes:
- Backup location:
- Rollback steps:
- Post-rollback verification:

## Per-round result

Record raw-file locations, start/end times, effective parameters, cold/warm state, success/failure/retry, performance, quality, resources, errors, recovery state, and conclusion.
