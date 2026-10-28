# Edge cases (fix a flaky test) — Hints

> [Back to the exercise](../README.md#ex-flaky_test_fix) · [Hint 1](flaky_test_fix_hints.md#hint-1) · [Hint 2](flaky_test_fix_hints.md#hint-2) · [Solution](flaky_test_fix_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried. Each hint builds toward the full solution.

- [Hint 1 — The idea, and the exact pieces](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

## Hint 1 — The idea, and the exact pieces {: #hint-1 }

A test that sometimes passes and sometimes fails on the *same behavior* is worse than a test that always fails — a failing test gets investigated; a flaky one gets a shrug and a re-run, and is eventually ignored, while still looking like part of your safety net.

The fix is always the same shape: replace an exact-match check with a **property** check — something true of every correct answer, whatever the wording. Common properties:

- **Keyword check:** `"shipped" in response.lower()` — `.lower()` matters, because capital letters don't make an answer more or less correct.
- **Length limit:** `len(response.split()) < 60` — when a rule really is "keep it short".
- **One of several phrasings:** a list like `["shipped", "on its way", "dispatched"]`, and a `for` loop that sets `found = True` when any of them appears — for facts with more than one correct wording.

Watch out: a single keyword can create *new* flakiness. If the model sometimes correctly says "your order is on its way", a check for only `"shipped"` fails on a right answer.

The model also needs the facts to answer at all: put them in the prompt (for example, "Order A123 shipped today"), the same way a real support bot gets them from a tool or a database.

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

```
ACCEPTABLE_PHRASES = ["shipped", "on its way", "sent out", "dispatched"]

test_shipping_reply():
    response = call the model, lower-cased
    found = False
    for each phrase: if it is in the response, found = True
    assert found (and show the response if not)
    assert the reply is under 60 words
```

Here's most of it — write the loop yourself:
```python
# practice/llm_output_testing_practice.py — Edge cases section
ACCEPTABLE_PHRASES = ["shipped", "on its way", "sent out", "dispatched"]

def test_shipping_reply():
    response = call_model(SHIPPING_PROMPT).lower()
    found = False
    # your turn: loop over ACCEPTABLE_PHRASES, set found = True
    # when a phrase is in response
    ...
    assert found, response
    assert len(response.split()) < 60
```

Full solution: [Show me the solution](flaky_test_fix_solution.md)
