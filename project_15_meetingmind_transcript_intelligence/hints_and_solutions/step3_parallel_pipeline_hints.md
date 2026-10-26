# Step 3 — Run Them in Parallel and Compile (final) — Hints

> [Back to the step](../READING_README.md#step-3-run-them-in-parallel-and-compile-final) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](step3_parallel_pipeline_solution.md)

- [Hint 1 — RunnableParallel, keyed by name](#hint-1)
- [Hint 2 — the pipeline, in two lines](#hint-2)

## Hint 1 — RunnableParallel, keyed by name {: #hint-1 }

The three chains are independent, so run them at the same time with `RunnableParallel`:

```
RunnableParallel(
    summary   = build_summary_chain(model),
    decisions = build_decisions_chain(model),
    actions   = build_actions_chain(model),
)
```

It gives every chain the same input, runs them concurrently, and returns a dict keyed by the names you chose — `{"summary": ..., "decisions": ..., "actions": ...}`. Those keys must match what `compile_report` (Step 1) reads.

## Hint 2 — the pipeline, in two lines {: #hint-2 }

`run_meeting(model, transcript)` is just: run the parallel pipeline, then compile.

```
parts = build_pipeline(model).invoke({"transcript": transcript})
return compile_report(parts)     # Step 1's compiler
```

`main.py` reads the transcript file, calls `run_meeting`, and prints `format_report(report)`. The integration test runs a tiny transcript with one clear decision ("ship v2") and one action ("book the venue") and checks the report names both. The whole file set is in the [Solution](step3_parallel_pipeline_solution.md).
