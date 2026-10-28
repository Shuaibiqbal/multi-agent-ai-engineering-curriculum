# Step 3 — The Pipeline — Hints

> [Back to the step](../READING_README.md#step-3-the-pipeline-final) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](step3_pipeline_solution.md)

- [Hint 1 — ask, in order](#hint-1)
- [Hint 2 — main and the test](#hint-2)

## Hint 1 — ask, in order {: #hint-1 }

The pipeline is the pieces you built, with the guard in the middle:

```
ask(model, db_path, question):
    schema = schema_text(db_path)                  # Step 1
    sql    = generate_sql(model, schema, question) # Step 2
    if not is_safe_select(sql):                    # Step 1 guard
        raise UnsafeQueryError(sql)
    rows   = run_select(db_path, sql)              # Step 1
    answer = summarize_answer(model, question, rows) # Step 2
    return answer, sql, rows
```

The order is the point: the guard sits **between** generation and execution, so nothing unsafe ever reaches `run_select`. Return the SQL too, so the user can see the query that ran.

## Hint 2 — main and the test {: #hint-2 }

`main.py` takes the question from `sys.argv`, calls `build_sample_db` (so the database exists on first run), then `ask`, and prints the SQL and the answer. Wrap the call in `try/except UnsafeQueryError` so a refused query prints a clean message instead of a traceback. The integration test asks "How many orders are completed?" and checks the answer mentions `3`; a second case asks a lookup ("Which city is Ada in?") and checks the answer says London. Keep the model at `temperature=0` so it's repeatable. The whole file set is in the [Solution](step3_pipeline_solution.md).
