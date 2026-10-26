# Step 3 — The Loader and the Full Pipeline (final) — Hints

> [Back to the step](../READING_README.md#step-3-the-loader-and-the-full-pipeline-final) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](step3_loader_and_pipeline_solution.md)

- [Hint 1 — the loader: one text shape for every format](#hint-1)
- [Hint 2 — the pipeline, in three lines](#hint-2)

## Hint 1 — the loader: one text shape for every format {: #hint-1 }

`load_invoice_text(path)` returns plain text whatever the file is:

- `.txt`/`.md` → `with open(path) as f: return f.read()`.
- `.pdf` → `PyPDFLoader(path).load()` (Doc08) gives one `Document` per page; join their `.page_content` with `"\n"`. (Needs `pip install pypdf`.)
- anything else → `raise UnsupportedFileError(...)`.

The point: the rest of the pipeline never cares what the file was — it always gets text.

## Hint 2 — the pipeline, in three lines {: #hint-2 }

`process_invoice(model, path)` is just the three pieces you already built, in order:

```
text    = load_invoice_text(path)        # Step 3
invoice = extract_invoice(model, text)   # Step 2
problems = validate_invoice(invoice)     # Step 1
return Result(invoice=invoice, problems=problems)
```

`Result` is a small `@dataclass(invoice, problems)`. `main.py` takes the path from `sys.argv`, calls `process_invoice`, and prints the fields plus any problems ("Cleared" when the list is empty). The integration test runs `samples/clean.txt` (clears) and `samples/bad_total.txt` (flagged). The whole file set is in the [Solution](step3_loader_and_pipeline_solution.md).
