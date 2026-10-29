# Basic (your first working tool) — Solution

> [Back to the exercise](../README.md#ex-first_tool_call) · [Hint 1](first_tool_call_hints.md#hint-1) · [Hint 2](first_tool_call_hints.md#hint-2) · [Solution](first_tool_call_solution.md)

**Story — `first_tool_call_practice.py`:** this is the exact primitive every agent in this entire curriculum is built from — a model deciding to call a function instead of answering directly. Seeing it work once, standalone, before combining it with anything else, is what makes the Build Task's `run_with_tools()` obvious instead of magic. **If not:** the first time you'd see a tool call requested and executed would be inside a bigger harness already juggling 2-3 tools, making it harder to tell which part is "the round trip" and which part is everything else.

## Solution

```python
# first_tool_call_practice.py
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def add(a: int, b: int) -> int:
    """Add two integers together and return the sum."""
    return a + b


# .bind_tools() gives back a model that can choose to call our tool.
model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools([add])
response = model.invoke("What's 5 + 7?")

# Even for obvious math, the model might just answer in text — always check.
if not response.tool_calls:
    print("The model answered directly, without calling a tool.")
    print(response.content)
else:
    for call in response.tool_calls:
        if call["name"] == "add":
            # .invoke() on the tool — @tool wraps add into a Runnable too
            result = add.invoke(call["args"])
            print(f"Called add({call['args']}) -> {result}")
        else:
            print(f"Unexpected tool requested: {call['name']}")
```
**Expected output:**
```
Called add({'a': 5, 'b': 7}) -> 12
```
