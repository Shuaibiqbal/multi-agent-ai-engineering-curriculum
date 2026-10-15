# Step 3 — Report Progress as a Trace — Hints

> [Back to the step](../READING_README.md#step-3-report-progress-as-a-trace) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](step3_progress_trace_solution.md)

- [Hint 1 — The idea](#hint-1)
- [Hint 2 — The plan](#hint-2)

## Hint 1 — The idea {: #hint-1 }

A slow multi-round call with zero feedback is a bad tool. Return a short revision **trace** alongside the summary, so the caller can see what happened each round. Add `src/formatting.py` with two **pure** functions: `format_result(result)` (the trace + status + summary block) and `format_partial(topic, progress)` (for Step 4). Have `deep_research` return `format_result(run_pipeline(..., progress))`. Pure formatters = unit-testable with no model.

## Hint 2 — The plan {: #hint-2 }

```
format_result(result):
    "Deep research on: {topic}"
    "Revision trace:" + per round "  Round N: approved/rejected" + issues
    "Status: approved after N round(s)."  OR  "...stopped at the N-round cap."
    "Summary:" + result.final_summary
deep_research:
    progress = Progress()
    return format_result(run_pipeline(MODEL, topic, cap, progress))
```

Pass a `Progress` holder into `run_pipeline` now (not just for the trace — Step 4's partial reads `progress.latest_draft` on timeout). Test `format_result` on a hand-made result: it should show "Round 1: rejected / - issue / Round 2: approved" and the summary. The whole file set is in the [Solution](step3_progress_trace_solution.md).
