# Edge cases (a task that needs no tool at all) — Solution

> [Back to the exercise](../README.md#ex-no_tool_needed) · [Hint 1](no_tool_needed_hints.md#hint-1) · [Hint 2](no_tool_needed_hints.md#hint-2) · [Solution](no_tool_needed_solution.md)

**Story — `no_tool_needed_practice.py`:** an agent that reaches for a tool on every question wastes a full round trip each time. This checks that your loop lets the model answer directly when no tool fits. **If not:** the Build Task's "task needs no tool" Test Case would be checked for the first time there.

Run from inside `practice/`, next to `react_loop_practice.py`.

## Solution

```python
# no_tool_needed_practice.py
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def add(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b


# None of these needs the add tool — a model that calls a tool here is
# wasting a round trip on every question.
prompts = [
    "What's the capital of France?",
    "What's the boiling point of water in Celsius?",
    "Write a haiku about the sea.",
]

model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools([add])
passed = 0
for prompt in prompts:
    response = model.invoke(prompt)
    no_tool = not response.tool_calls     # True = answered directly, good
    if no_tool:
        passed = passed + 1
    print(f"no tool? -> {no_tool}: {prompt}")
print(f"{passed}/{len(prompts)} answered without a tool")
```
**Expected output:**

```
case 1 (no tool?) -> True: What's the capital of France?
case 2 (no tool?) -> True: What's the boiling point of water in Celsius?
case 3 (no tool?) -> True: Write a haiku about the sea.
3/3 answered without a tool
```
