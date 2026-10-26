# ReceiptRadar — Hints

> Read the [story](../READING_README.md) and try to build it first. These hints point you at the pieces and the easy-to-miss parts, without giving the whole answer. The full code is in the [complete solution](solution.md).

## Hint 1 — the pieces, and the one that matters

Four small jobs, one file each (the same shape as InvoiceIQ):

- `src/schemas.py` — `Receipt(merchant, amount, category, has_note)`. Make `merchant`/`amount`/`category` optional (`None`), and `has_note: bool = False` — a receipt with no note defaults to "no note".
- `src/loader.py` — `load_receipt_text(path)`: `.txt`/`.md` with `open()`, `.pdf` with `PyPDFLoader` (Doc08).
- `src/policy.py` — `check_policy(receipt) -> list[str]`: the expense rules. **This is the whole point** — build and test it first, with hand-made `Receipt` objects, no model.
- `src/pipeline.py` — `extract_receipt(model, text)` with `with_structured_output(Receipt)`, then `process_receipt(model, path)` = load → extract → check.

Build order: schema → policy (test it) → extractor → loader → pipeline.

## Hint 2 — the policy, rule by rule

The policy is plain Python, so it's right every time:

```
NOTE_THRESHOLD = 75.0
BANNED_CATEGORIES = ("alcohol", "gift", "gifts")

check_policy(receipt):
    problems = []
    if not receipt.merchant: -> "missing merchant"
    if receipt.amount is None: -> "missing amount"
    else:
        if receipt.amount > NOTE_THRESHOLD and not receipt.has_note:
            -> "amount X is over the 75.0 note threshold and has no note"
    if receipt.category and receipt.category.lower() in BANNED_CATEGORIES:
        -> "category '...' is not reimbursable"
    return problems
```

Two details that matter: compare the category **lowercased** (so "Alcohol" is caught too), and the `has_note` escape — an over-limit receipt **with** a note is fine. The extractor's prompt must set `has_note` to true only when a note is actually present. Test the policy with hand-made receipts: a small one (approved), over-limit-no-note (flagged), over-limit-with-note (ok), a banned category (flagged). The whole file set is in the [complete solution](solution.md).
