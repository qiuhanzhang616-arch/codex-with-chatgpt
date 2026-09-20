# Test Plan and Baseline Template

## 1. Test question

- Test type:
- Decision purpose:
- Pass criteria:
- Non-regression requirements:

## 2. Tested version

- Model/revision/precision:
- Tokenizer/processor/template:
- Endpoint/alias:
- Framework/image/drivers:
- Hardware/devices/nodes/topology:
- Effective process arguments:
- Health and background traffic:

## 3. Request path

- Real business path:
- Shortest model path:
- Client/SDK/agent:
- Authentication/gateway/LB/proxy:
- Streaming/buffering/retry/fallback:

## 4. Request contract

- Real work item:
- Input/output distribution:
- Prompt/Reasoning/Tools/schema/sampling:
- Media and preprocessing:
- Cache/reuse state:
- Success and failure definitions:

## 5. Matrix

| Cell | Input | Output | Concurrency/QPS | Mode | Requests/duration | Repeats | Cache state |
|---|---|---|---|---|---|---|---|

- Total cells:
- Expected duration:
- Execution order:
- Checkpoint/resume method:
- Summary row and column dimensions, when required:
- Summary metrics and units:
- Cell-detail and request-detail locations:

## 6. Metrics

| Metric | Unit | Formula | Start | End | Aggregation | Pass value |
|---|---|---|---|---|---|---|

## 7. Quality

- Dataset/version/sample:
- Evaluator:
- Quality gate:
- Post-stress regression:

## 8. Observation

- Raw client data:
- Gateway/model logs:
- Accelerator/memory/communication:
- Queue/cache/rank:
- Request IDs/clock synchronization:

## 9. Safety boundary

- Maximum load/cost/duration:
- Stop conditions:
- Recovery requirements:
- Change authorization:

## 10. Result status

Mark every cell: not run / running / valid pass / valid fail / invalid data, rerun required / paused.
