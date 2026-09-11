# Step 2 — One Tool, One Loop: the Smallest Possible Working Agent — Hints

> [Back to this step](../README.md#step-2-one-tool-one-loop-the-smallest-possible-working-agent) · [Hint 1](step2_single_tool_loop_hints.md#hint-1) · [Hint 2](step2_single_tool_loop_hints.md#hint-2) · [Hint 3](step2_single_tool_loop_hints.md#hint-3) · [Hint 4](step2_single_tool_loop_hints.md#hint-4) · [Solution](step2_single_tool_loop_solution.md)

Work through in order — don't jump ahead until you've genuinely tried.

- [Hint 1](#hint-1)
- [Hint 2](#hint-2)
- [Hint 3](#hint-3)
- [Hint 4](#hint-4)

<hr class="page-break">

> [Back to this step](../README.md#step-2-one-tool-one-loop-the-smallest-possible-working-agent) · [Hint 1](step2_single_tool_loop_hints.md#hint-1) · [Hint 2](step2_single_tool_loop_hints.md#hint-2) · [Hint 3](step2_single_tool_loop_hints.md#hint-3) · [Hint 4](step2_single_tool_loop_hints.md#hint-4) · [Solution](step2_single_tool_loop_solution.md)

## Hint 1

### Simple Version

An "agent," at its simplest, is a model that can decide to use a tool instead of just answering directly. This step gives it exactly one tool — a plain Python function, decorated so LangChain knows how to offer it to the model — and wraps a small loop around the model call: ask the model, check if it wants to use the tool, if so run the tool and tell the model what happened, then ask again.

Pick the simplest possible tool for this — something with no external dependency, like a calculator function. You want the *loop* to be the thing you're proving works, not the tool itself.

Deliberately don't reach for `AgentExecutor` here — building the loop by hand once is the whole point of this step, per Doc07.

<hr class="page-break">

> [Back to this step](../README.md#step-2-one-tool-one-loop-the-smallest-possible-working-agent) · [Hint 1](step2_single_tool_loop_hints.md#hint-1) · [Hint 2](step2_single_tool_loop_hints.md#hint-2) · [Hint 3](step2_single_tool_loop_hints.md#hint-3) · [Hint 4](step2_single_tool_loop_hints.md#hint-4) · [Solution](step2_single_tool_loop_solution.md)

### Intermediate Version

Two things to build:

```python
# tools.py
@tool(args_schema=CalculatorArgs)
def calculator(...) -> str:
```

```python
# agent.py
def run_agent(task: str) -> AgentResult:
```

The tool needs a Pydantic argument shape (`CalculatorArgs`, with typed fields like `expression: str`) so LangChain can validate what the model sends it — this is the same discipline Doc06 teaches: never trust the model's raw arguments without a schema checking them first.

`run_agent()`'s loop needs the model bound to the tool list (`model.bind_tools([calculator])`), so the model's response can include a `tool_calls` field. Check that field each time: if it's present, actually run the named tool with the given arguments, add the result back into the message history as a tool message, and call the model again. If it's empty, the model gave a final answer — stop the loop.

Sketch the loop's shape (ask → check for `tool_calls` → run tool or stop) before writing the tool or the full loop body.

<hr class="page-break">

> [Back to this step](../README.md#step-2-one-tool-one-loop-the-smallest-possible-working-agent) · [Hint 1](step2_single_tool_loop_hints.md#hint-1) · [Hint 2](step2_single_tool_loop_hints.md#hint-2) · [Hint 3](step2_single_tool_loop_hints.md#hint-3) · [Hint 4](step2_single_tool_loop_hints.md#hint-4) · [Solution](step2_single_tool_loop_solution.md)

## Hint 2

### Simple Version

Here are the exact pieces you need:

- `from langchain_core.tools import tool` — the decorator that turns a plain function into something the model can call.
- `from pydantic import BaseModel` — for the tool's argument shape.
- `model.bind_tools([calculator])` — gives the model the ability to ask for this tool.
- After calling the bound model, check `response.tool_calls` — a list, empty if the model didn't ask for a tool.
- Each entry in `tool_calls` has `name` and `args` — use `args` to actually call your Python function.
- Add the tool's result back as a message with `role="tool"` (LangChain's `ToolMessage`), so the model can see what happened on its next turn.

<hr class="page-break">

> [Back to this step](../README.md#step-2-one-tool-one-loop-the-smallest-possible-working-agent) · [Hint 1](step2_single_tool_loop_hints.md#hint-1) · [Hint 2](step2_single_tool_loop_hints.md#hint-2) · [Hint 3](step2_single_tool_loop_hints.md#hint-3) · [Hint 4](step2_single_tool_loop_hints.md#hint-4) · [Solution](step2_single_tool_loop_solution.md)

### Intermediate Version

Look specifically at:
- **`@tool(args_schema=CalculatorArgs)`** — the decorator reads the schema to build the tool's description for the model, and validates whatever arguments the model sends before your function body ever runs.
- **`response.tool_calls`** — on an `AIMessage`, this is a list of dicts with `name`, `args`, and `id`. An empty list means "no tool needed, this is the final answer" — that's your loop's stop condition.
- **`ToolMessage(content=result, tool_call_id=call["id"])`** — the `tool_call_id` must match the id from the original `tool_calls` entry, or the model can't tell which call this result belongs to (this matters more once you have several tools in Step 3).
- **The loop only calling the tool when asked:** don't hardcode "always call the calculator" — the whole point of Step 2's test (a prompt that needs it, one that doesn't) is proving the model decides correctly on its own.

Write `run_agent()`'s full loop body, including the `ToolMessage` construction, before moving to Hint 3.

<hr class="page-break">

> [Back to this step](../README.md#step-2-one-tool-one-loop-the-smallest-possible-working-agent) · [Hint 1](step2_single_tool_loop_hints.md#hint-1) · [Hint 2](step2_single_tool_loop_hints.md#hint-2) · [Hint 3](step2_single_tool_loop_hints.md#hint-3) · [Hint 4](step2_single_tool_loop_hints.md#hint-4) · [Solution](step2_single_tool_loop_solution.md)

## Hint 3

### Simple Version

The plan, in plain steps:

```
define a calculator tool: takes an expression, returns the computed result

function run_agent(task):
    messages = [system message, task as a human message]
    loop:
        ask the model, with the calculator tool available
        if the model asked to use the calculator:
            actually run it
            add the result to messages as a tool result
            ask again (loop continues)
        else:
            this is the final answer, stop and return it
```

<hr class="page-break">

> [Back to this step](../README.md#step-2-one-tool-one-loop-the-smallest-possible-working-agent) · [Hint 1](step2_single_tool_loop_hints.md#hint-1) · [Hint 2](step2_single_tool_loop_hints.md#hint-2) · [Hint 3](step2_single_tool_loop_hints.md#hint-3) · [Hint 4](step2_single_tool_loop_hints.md#hint-4) · [Solution](step2_single_tool_loop_solution.md)

### Intermediate Version

The same plan, closer to real structure:

```
tools.py:
    class CalculatorArgs(BaseModel):
        expression: str

    @tool(args_schema=CalculatorArgs)
    def calculator(expression: str) -> str:
        return str(eval(expression))   # fine for this exercise; a real project would use a safe parser

agent.py:
    class AgentResult(BaseModel):
        answer: str
        steps: list[str]

    def run_agent(task: str) -> AgentResult:
        model = ChatOpenAI(model="gpt-4o-mini").bind_tools([calculator])
        messages = [SystemMessage("Use the calculator tool for any math."), HumanMessage(task)]
        steps = []

        while True:
            response = model.invoke(messages)
            messages.append(response)

            if not response.tool_calls:
                return AgentResult(answer=response.content, steps=steps)

            for call in response.tool_calls:
                result = calculator.invoke(call["args"])
                steps.append(f"called {call['name']} with {call['args']} -> {result}")
                messages.append(ToolMessage(content=result, tool_call_id=call["id"]))
```

Notice the loop has no exit limit yet — that's deliberate, it's Step 3's job. For now, trust that a single-tool task naturally finishes in 1-2 rounds.

<hr class="page-break">

> [Back to this step](../README.md#step-2-one-tool-one-loop-the-smallest-possible-working-agent) · [Hint 1](step2_single_tool_loop_hints.md#hint-1) · [Hint 2](step2_single_tool_loop_hints.md#hint-2) · [Hint 3](step2_single_tool_loop_hints.md#hint-3) · [Hint 4](step2_single_tool_loop_hints.md#hint-4) · [Solution](step2_single_tool_loop_solution.md)

## Hint 4

### Simple Version

Here's almost the whole loop — try finishing the rest yourself:

```python
def run_agent(task):
    model = ChatOpenAI(model="gpt-4o-mini").bind_tools([calculator])
    messages = [SystemMessage("Use the calculator tool for any math."), HumanMessage(task)]

    while True:
        response = model.invoke(messages)
        messages.append(response)
        if not response.tool_calls:
            return response.content
        for call in response.tool_calls:
            result = calculator.invoke(call["args"])
            messages.append(ToolMessage(content=result, tool_call_id=call["id"]))
```

What's missing: type hints, the `AgentResult` return shape with a step log, and `main.py` printing each think/act/observe step as the README asks. Add those, then check the [Solution](step2_single_tool_loop_solution.md).

<hr class="page-break">

> [Back to this step](../README.md#step-2-one-tool-one-loop-the-smallest-possible-working-agent) · [Hint 1](step2_single_tool_loop_hints.md#hint-1) · [Hint 2](step2_single_tool_loop_hints.md#hint-2) · [Hint 3](step2_single_tool_loop_hints.md#hint-3) · [Hint 4](step2_single_tool_loop_hints.md#hint-4) · [Solution](step2_single_tool_loop_solution.md)

### Intermediate Version

The same idea, fully typed with a proper `AgentResult`:

```python
from pydantic import BaseModel
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from tools import calculator


class AgentResult(BaseModel):
    answer: str
    steps: list[str]


def run_agent(task: str) -> AgentResult:
    model = ChatOpenAI(model="gpt-4o-mini").bind_tools([calculator])
    messages = [SystemMessage("Use the calculator tool for any math."), HumanMessage(task)]
    steps: list[str] = []

    while True:
        response = model.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            return AgentResult(answer=response.content, steps=steps)

        for call in response.tool_calls:
            result = calculator.invoke(call["args"])
            steps.append(f"called {call['name']} with {call['args']} -> {result}")
            messages.append(ToolMessage(content=result, tool_call_id=call["id"]))
```

What's missing: `main.py`, and the two-prompt test from the README (one that clearly needs the calculator, one that clearly doesn't — confirm the loop only calls the tool for the first one). Write those yourself, then compare against the [Solution](step2_single_tool_loop_solution.md).

<hr class="page-break">

> [Back to this step](../README.md#step-2-one-tool-one-loop-the-smallest-possible-working-agent) · [Hint 1](step2_single_tool_loop_hints.md#hint-1) · [Hint 2](step2_single_tool_loop_hints.md#hint-2) · [Hint 3](step2_single_tool_loop_hints.md#hint-3) · [Hint 4](step2_single_tool_loop_hints.md#hint-4) · [Solution](step2_single_tool_loop_solution.md)

Full solution: [Show me the solution](step2_single_tool_loop_solution.md)
