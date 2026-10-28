# Edge cases (fix a flaky test) — Solution

> [Back to the exercise](../README.md#ex-flaky_test_fix) · [Hint 1](flaky_test_fix_hints.md#hint-1) · [Hint 2](flaky_test_fix_hints.md#hint-2) · [Solution](flaky_test_fix_solution.md)

**Story — `llm_output_testing_practice.py` (Edge cases section):** everyone writes `assert response == "..."` against a real model once, and watches it fail on a perfectly good answer. Fixing one such test on purpose teaches the habit every later LLM test needs: check what makes the answer correct, not its exact words. **If not:** the Build Task's rule-based tasks would be written as exact matches, fail at random, and get ignored.

The solution calls the real OpenAI API, and runs from inside `practice/` with `pytest llm_output_testing_practice.py -v`.

## Solution

**Story:** a property check is only as good as the property. Writing the reason next to each `assert` forces you to say *why* it proves correctness, and the failure message shows the real reply. **If not:** a failing test would say only `AssertionError`, and you'd rerun the model by hand to see what it said.

```python
# practice/llm_output_testing_practice.py — Edge cases section
from openai import OpenAI

client = OpenAI()

SHIPPING_PROMPT = (
    "You are a support assistant. Order A123 shipped today.\n"
    "Customer: Has my order shipped?"
)

def call_model(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

def test_shipping_reply():
    response = call_model(SHIPPING_PROMPT)
    # why: the key fact must be present, whatever the wording
    assert "shipped" in response.lower(), response
    # why: a direct reply, not a ramble
    assert len(response.split()) < 60, response
```
**Expected output:**
```
llm_output_testing_practice.py::test_shipping_reply PASSED
```
