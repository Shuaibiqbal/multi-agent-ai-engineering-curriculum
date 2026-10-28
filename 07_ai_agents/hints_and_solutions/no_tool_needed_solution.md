# Edge cases (a task that needs no tool at all) — Solution

> [Back to the exercise](../README.md#ex-no_tool_needed) · [Hint 1](no_tool_needed_hints.md#hint-1) · [Hint 2](no_tool_needed_hints.md#hint-2) · [Solution](no_tool_needed_solution.md)

**Story — `no_tool_needed_practice.py`:** an agent that reaches for a tool on every question wastes a full round trip each time. This checks that your loop lets the model answer directly when no tool fits. **If not:** the Build Task's "task needs no tool" Test Case would be checked for the first time there.

Run from inside `practice/`, next to `react_loop_practice.py`.

## Solution

```python
# no_tool_needed_practice.py
from react_loop_practice import run_agent

# why: none of these needs add, get_weather or flaky_lookup — a model
# that calls a tool here is wasting a round trip on every question
NO_TOOL_PROMPTS = [
    "What's the capital of France?",
    "What's the boiling point of water in Celsius?",
    "Write a haiku about the sea.",
]

def check_no_tool(prompt: str) -> bool:
    result = run_agent(prompt)
    return len(result.steps) == 0

def main() -> None:
    passed = 0
    number = 0
    for prompt in NO_TOOL_PROMPTS:
        number = number + 1
        ok = check_no_tool(prompt)
        if ok:
            passed = passed + 1
        print(f"case {number} (no tool?) -> {ok}: {prompt}")
    print(f"{passed}/{len(NO_TOOL_PROMPTS)} answered without a tool")

if __name__ == "__main__":
    main()
```
**Expected output:**

```
case 1 (no tool?) -> True: What's the capital of France?
case 2 (no tool?) -> True: What's the boiling point of water in Celsius?
case 3 (no tool?) -> True: Write a haiku about the sea.
3/3 answered without a tool
```
