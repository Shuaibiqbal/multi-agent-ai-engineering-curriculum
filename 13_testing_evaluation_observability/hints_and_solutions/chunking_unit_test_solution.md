# Basic (a normal, exact test) — Solution

> [Back to the exercise](../README.md#ex-chunking_unit_test) · [Hint 1](chunking_unit_test_hints.md#hint-1) · [Hint 2](chunking_unit_test_hints.md#hint-2) · [Solution](chunking_unit_test_solution.md)

**Story — `chunking_unit_test_practice.py`:** the chunker has no model call inside it at all, so it's the easiest possible place to learn pytest itself — `test_` prefixed functions that pytest auto-discovers, plain `assert` statements, and reading what a failure actually reports — before any LLM output makes the checking itself harder. **If not:** your first pytest test would be against a model's answer, and you couldn't tell whether a failure came from pytest, your own check, or the model's unpredictability.

Run it with `pytest chunking_unit_test_practice.py -v`.

## Solution

**Story:** a check that only counts the number of chunks still passes even if the chunker scrambles their order or silently cuts text off the end. Checking the first and last chunk's actual text catches both, and a second, clearly named test covers the "no blank lines at all" input that real documents often have. **If not:** a chunker that quietly drops the last sentence would pass every test, and your RAG answers would be missing facts with no failing test anywhere to say why.

```python
# practice/chunking_unit_test_practice.py
# chunk_by_paragraph from Doc08, inline so this test runs on its own.
def chunk_by_paragraph(text: str) -> list:
    chunks = []
    for piece in text.split("\n\n"):
        stripped = piece.strip()
        if stripped:
            chunks.append(stripped)
    return chunks


sample_text = "Paragraph one.\n\nParagraph two.\n\nParagraph three."

def test_chunk_by_paragraph():
    chunks = chunk_by_paragraph(sample_text)
    assert len(chunks) == 3
    # why: content checks catch a scrambled order or cut-off text,
    # which a count check alone would miss
    assert chunks[0] == "Paragraph one."
    assert chunks[-1] == "Paragraph three."

# how: one test per case, named after the case —
# the name alone tells you what broke
def test_chunk_by_paragraph_single_paragraph():
    chunks = chunk_by_paragraph("Just one paragraph, no blank lines.")
    assert len(chunks) == 1
    assert chunks[0] == "Just one paragraph, no blank lines."
```
**Expected output:**
```
chunking_unit_test_practice.py::test_chunk_by_paragraph PASSED
chunking_unit_test_practice.py::test_chunk_by_paragraph_single_paragraph PASSED
```
