# Step 2 — Extract an Invoice From Text (the model's job) — Hints

> [Back to the step](../READING_README.md#step-2-extract-an-invoice-from-text-the-models-job) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](step2_structured_extraction_solution.md)

- [Hint 1 — one chain, one method](#hint-1)
- [Hint 2 — the one line the prompt must contain](#hint-2)

## Hint 1 — one chain, one method {: #hint-1 }

This is the easy step — the model does the work. `extract_invoice(model, text)` is one small chain:

```
prompt = ChatPromptTemplate.from_template(EXTRACT_PROMPT)
chain  = prompt | model.with_structured_output(Invoice)
return chain.invoke({"text": text})
```

`with_structured_output(Invoice)` (Doc04/05) makes the model return an `Invoice` object directly — no JSON string, no parsing, no `try/except`. You get a real `Invoice` every time.

## Hint 2 — the one line the prompt must contain {: #hint-2 }

The prompt has exactly one important instruction: **"if a field is not present, leave it empty — never invent a value."**

Without it, a missing invoice number tempts the model to make one up, and an invented value that looks plausible is the worst kind of wrong — your validator can't catch what the model fabricated. With it (and optional fields from Step 1), a missing field comes back as `None`, and Step 1's validator reports it. Structured output guarantees the *shape*; this line is what keeps the *values* honest. The whole file set is in the [Solution](step2_structured_extraction_solution.md).
