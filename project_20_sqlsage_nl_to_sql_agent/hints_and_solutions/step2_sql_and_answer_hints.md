# Step 2 — The SQL Generator and the Answer — Hints

> [Back to the step](../READING_README.md#step-2-the-sql-generator-and-the-answer) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](step2_sql_and_answer_solution.md)

- [Hint 1 — structured SQL](#hint-1)
- [Hint 2 — the answer step](#hint-2)

## Hint 1 — structured SQL {: #hint-1 }

You want a clean SQL string, not a sentence you have to cut the query out of. That's exactly what structured output is for (Doc05):

```
class SQLQuery(BaseModel):
    sql: str

chain = prompt | model.with_structured_output(SQLQuery)
result = chain.invoke({"schema": schema, "question": question})
return result.sql
```

Put the schema (`schema_text` from Step 1) in the prompt so the model only uses tables and columns that exist, and tell it plainly: one read-only `SELECT`, no writes, no multiple statements. (The guard still checks — the prompt just makes a good query likelier.)

## Hint 2 — the answer step {: #hint-2 }

The runner returns rows like `[(3,)]` or `[('Ada', 120.0)]` — not something to hand a user. `summarize_answer` turns them into a sentence, grounded in the rows only:

```
"Answer in one sentence using ONLY the rows below. If empty, say no
 matching data was found.  Question: {question}  Rows: {rows}"
```

Pass the rows as a string (`str(rows)`). Keep the model at `temperature=0` so the SQL and the phrasing are repeatable. The whole file set is in the [Solution](step2_sql_and_answer_solution.md).
