# Edge cases (a template with the wrong variables) — Solution

> [Back to the exercise](../README.md#ex-template_variable_errors) · [Hint 1](template_variable_errors_hints.md#hint-1) · [Hint 2](template_variable_errors_hints.md#hint-2) · [Solution](template_variable_errors_solution.md)

## Basic Version

### Approach 1 — the direct way

```python
# prompt_template_practice.py
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("Answer: {question}")

# missing variable
try:
    prompt.invoke({})
except Exception as e:
    print("Missing variable error:", type(e).__name__, "-", e)

# extra variable
result = prompt.invoke({"question": "What is LCEL?", "extra": "unused"})
print("Extra variable result:", result)
```
**Expected output:**
```
Missing variable error: KeyError - 'question'
Extra variable result: messages=[HumanMessage(content='Answer: What is LCEL?')]
```

This version works and shows both cases clearly. It catches the broad `Exception` for the missing-variable case rather than the specific `KeyError`, which is fine for exploring but not what you'd write once you know exactly what error type to expect.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-template_variable_errors) · [Hint 1](template_variable_errors_hints.md#hint-1) · [Hint 2](template_variable_errors_hints.md#hint-2) · [Solution](template_variable_errors_solution.md)

## Intermediate Version

### Approach 1 — the specific `KeyError`, in named functions

```python
# prompt_template_practice.py
from langchain_core.prompts import ChatPromptTemplate


def demonstrate_missing_variable(prompt: ChatPromptTemplate) -> None:
    try:
        prompt.invoke({})
    except KeyError as e:
        print(f"Missing variable -> KeyError: {e}")


def demonstrate_extra_variable(prompt: ChatPromptTemplate) -> None:
    result = prompt.invoke({"question": "What is LCEL?", "extra": "unused"})
    print(f"Extra variable -> no error, result: {result}")


def main() -> None:
    prompt = ChatPromptTemplate.from_template("Answer: {question}")
    demonstrate_missing_variable(prompt)
    demonstrate_extra_variable(prompt)


if __name__ == "__main__":
    main()
```
**Expected output:**
```
Missing variable -> KeyError: 'question'
Extra variable -> no error, result: messages=[HumanMessage(content='Answer: What is LCEL?')]
```

**Difference from Basic:** catching `KeyError` specifically (not a broad `Exception`) documents, right in the code, exactly what failure you expect and are prepared to handle — if the library ever changed to raise a different error type here, this code would stop silently swallowing it and let you notice. Splitting the two demonstrations into named functions also makes each case something you could reuse as an actual test later, not just a script you run once and read.

**Which one should you write?** Intermediate's specific-`KeyError` catch is what this document's Build Task needs — a clear error while building the prompt, not silently left blank. A stricter check — reading `prompt.input_variables` directly and validating both missing *and* extra (typo'd) keys before ever calling `.invoke()` — is worth adding anywhere you're building prompts from user input or config, where a typo'd key is a real, easy mistake; not required for this exercise or the Build Task.
