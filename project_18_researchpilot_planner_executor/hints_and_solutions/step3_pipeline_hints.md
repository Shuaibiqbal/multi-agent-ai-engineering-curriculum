# Step 3 — The Pipeline — Hints

> [Back to the step](../READING_README.md#step-3-the-pipeline-final) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](step3_pipeline_solution.md)

- [Hint 1 — run_research, in order](#hint-1)
- [Hint 2 — main and the test](#hint-2)

## Hint 1 — run_research, in order {: #hint-1 }

The pipeline is the three tested pieces, in order:

```
run_research(model, question):
    plan = make_plan(model, question).sub_questions   # Step 2 (planner)
    collection = build_source_store()                 # Step 2 (RAG)
    search = make_search(collection)                  # Step 2 (search closure)
    findings = execute_plan(plan, search)             # Step 1 (executor)
    return compile_report(question, findings)         # Step 1 (compiler)
```

Each line is a piece you already built and tested — the pipeline just wires them.

## Hint 2 — main and the test {: #hint-2 }

`main.py` takes a question from `sys.argv`, calls `run_research`, and prints `format_report(report)`. The integration test asks a broad question and checks the report has several findings, a `[1]` citation, and a "Sources:" list — and that each `finding.source` ends with `.md` (a real file). Keep the planner at `temperature=0` so the sub-questions are repeatable enough to test. The whole file set is in the [Solution](step3_pipeline_solution.md).
