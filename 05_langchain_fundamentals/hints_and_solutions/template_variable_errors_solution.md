# Edge cases (a template with the wrong variables) — Solution

> [Back to the exercise](../README.md#ex-template_variable_errors) · [Hint 1](template_variable_errors_hints.md#hint-1) · [Hint 2](template_variable_errors_hints.md#hint-2) · [Solution](template_variable_errors_solution.md)

**Story — `prompt_template_practice.py`:** a LangChain `ChatPromptTemplate` has named slots like `{topic}` that you fill in when you call it. When the variables you pass don't line up with the slots, it can break in two very different places, and this exercise makes you see both on purpose. A *missing* variable (you forgot to pass `topic`) fails immediately, while you're still building the prompt — a fast, local `KeyError` you can fix in seconds. An *extra* variable (you passed `topping` by mistake) is sneakier: the template builds fine and the stray key is silently ignored, so the mistake only surfaces later as a wrong or empty answer from the model. Knowing which of the two you're looking at is what lets you debug it quickly. **If not:** the Build Task's `prompts.py` requirement to "fail the same clear way" would ask you to guarantee behavior you'd never actually observed happening.

## Solution

```python
# prompt_template_practice.py
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("Answer: {question}")

# A missing variable fails right away, before any API call. Catch KeyError
# specifically, so a genuinely different bug would still surface.
try:
    prompt.invoke({})
except KeyError:
    print("Missing variable -> KeyError, before any API call")

# An extra, unused key is silently ignored — not an error. (Easy to assume
# the opposite, so it's worth seeing once.) The filled prompt is a list of
# messages; [0] is the only one here.
result = prompt.invoke({"question": "What is LCEL?", "extra": "unused"})
print(f"Extra variable -> no error: {result.messages[0].content}")
```
**Expected output:**
```
Missing variable -> KeyError, before any API call
Extra variable -> no error: Answer: What is LCEL?
```

**Going further:** a stricter check — reading `prompt.input_variables` directly and validating both missing *and* extra (typo'd) keys before ever calling `.invoke()` — is worth adding anywhere you're building prompts from user input or config, where a typo'd key is a real, easy mistake; not required for this exercise or the Build Task.
