# Step 3 — The Pipeline — Hints

> [Back to the step](../READING_README.md#step-3-the-pipeline-final) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](step3_pipeline_solution.md)

- [Hint 1 — run_query, in order](#hint-1)
- [Hint 2 — main and the test](#hint-2)

## Hint 1 — run_query, in order {: #hint-1 }

The pipeline is the pieces you built, in order:

```
run_query(model, repo_dir, question):
    collection = build_code_store(repo_dir)        # Step 1
    snippets   = retrieve_snippets(collection, q)  # Step 1
    context    = build_context(snippets)           # Step 1
    answer     = answer_question(model, q, context) # Step 2
    return answer, cited_files(snippets)           # Step 1
```

It returns both the answer and the list of files it came from — a written answer plus the places to look.

## Hint 2 — main and the test {: #hint-2 }

`main.py` takes a question from `sys.argv`, calls `run_query`, prints the answer and each cited file. The integration test asks "How is login handled?" and checks the answer mentions login and cites `auth.py`; a second case asks something the repo doesn't cover ("how do I train a neural network here?") and checks the answer admits it doesn't know. Keep the model at `temperature=0` so answers are repeatable. The whole file set is in the [Solution](step3_pipeline_solution.md).
