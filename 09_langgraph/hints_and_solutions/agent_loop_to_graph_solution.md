# Real-world (rebuild Project 2 as a graph) — Solution

> [Back to the exercise](../README.md#ex-agent_loop_to_graph) · [Hint 1](agent_loop_to_graph_hints.md#hint-1) · [Hint 2](agent_loop_to_graph_hints.md#hint-2) · [Solution](agent_loop_to_graph_solution.md)

The `call_model_with_tools` and `run_tool` functions below stand in for your real Doc07 functions — in your own rebuild, import and call your actual Project 2 code instead of these. They're written as small, deterministic stubs here so the whole example is runnable and its output is predictable, without needing a live API key.

```python
# stand-ins for your real Doc07 code — replace with your actual imports
def call_model_with_tools(task: str, scratchpad: list[str]) -> dict:
    if not scratchpad and "*" in task:
        return {"wants_tool": True, "tool_name": "calculator", "tool_input": task}
    return {"wants_tool": False, "answer": "84"}

def run_tool(tool_name: str, tool_input: str) -> str:
    if tool_name == "calculator":
        return "84"
    return "unknown tool"
```

Read all three depths — they're not "wrong, less wrong, right," they're 3 real, valid ways to solve the same problem, with real tradeoffs between them.

## Basic Version

### Approach 1 — the direct translation

```python
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    task: str
    scratchpad: Annotated[list[str], operator.add]
    next_action: str
    final_answer: str


def think(state):
    decision = call_model_with_tools(state["task"], state["scratchpad"])
    if decision["wants_tool"]:
        return {
            "scratchpad": [f"Thought: calling {decision['tool_name']}"],
            "next_action": "call_tool",
        }
    return {
        "scratchpad": ["Thought: done"],
        "next_action": "finish",
        "final_answer": decision["answer"],
    }


def act(state):
    result = run_tool("calculator", state["task"])
    return {"scratchpad": [f"Observation: {result}"]}


def finish_node(state):
    return {}


def route(state):
    return state["next_action"]


builder = StateGraph(AgentState)
builder.add_node("think", think)
builder.add_node("act", act)
builder.add_node("finish_node", finish_node)
builder.add_edge(START, "think")
builder.add_conditional_edges("think", route, {"call_tool": "act", "finish": "finish_node"})
builder.add_edge("act", "think")
builder.add_edge("finish_node", END)

graph = builder.compile()
result = graph.invoke(
    {"task": "What is 12 * 7?", "scratchpad": [], "next_action": "", "final_answer": ""},
    config={"recursion_limit": 20},
)
print(result["final_answer"])
print(result["scratchpad"])
```
**Expected output:**
```
84
['Thought: calling calculator', 'Observation: 84', 'Thought: done']
```
This traces exactly like the Doc07 loop would: `think` decides a tool is needed, `act` runs it and appends the observation, control loops back to `think`, which now sees the observation in `scratchpad` and decides it's done.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-agent_loop_to_graph) · [Hint 1](agent_loop_to_graph_hints.md#hint-1) · [Hint 2](agent_loop_to_graph_hints.md#hint-2) · [Solution](agent_loop_to_graph_solution.md)

## Intermediate Version

### Approach 1 — type hints, and reusing real tool dispatch

```python
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    task: str
    scratchpad: Annotated[list[str], operator.add]
    next_action: str
    final_answer: str


def think(state: AgentState) -> dict:
    decision = call_model_with_tools(state["task"], state["scratchpad"])
    if decision["wants_tool"]:
        return {
            "scratchpad": [f"Thought: calling {decision['tool_name']}"],
            "next_action": "call_tool",
            "task": state["task"],
        }
    return {
        "scratchpad": ["Thought: done"],
        "next_action": "finish",
        "final_answer": decision["answer"],
    }


def act(state: AgentState) -> dict:
    # in your real rebuild: look up state's chosen tool name/args, then call
    # your Doc07 tool registry, same as `run_tool` in your original loop
    result = run_tool("calculator", state["task"])
    return {"scratchpad": [f"Observation: {result}"]}


def finish_node(state: AgentState) -> dict:
    return {}


def route(state: AgentState) -> str:
    return state["next_action"]


builder = StateGraph(AgentState)
builder.add_node("think", think)
builder.add_node("act", act)
builder.add_node("finish_node", finish_node)
builder.add_edge(START, "think")
builder.add_conditional_edges("think", route, {"call_tool": "act", "finish": "finish_node"})
builder.add_edge("act", "think")
builder.add_edge("finish_node", END)

graph = builder.compile()
result = graph.invoke(
    {"task": "What is 12 * 7?", "scratchpad": [], "next_action": "", "final_answer": ""},
    config={"recursion_limit": 20},
)
print(f"answer: {result['final_answer']}")
for line in result["scratchpad"]:
    print(f"  {line}")
```
**Expected output:**
```
answer: 84
  Thought: calling calculator
  Observation: 84
  Thought: done
```

**Difference from Basic:** same graph and same result, with full type hints and a `config={"recursion_limit": 20}` called out explicitly as the graph's equivalent of Doc07's manually-counted step limit — without it, a routing bug that never reaches `"finish"` would spin forever instead of failing with a clear `GraphRecursionError`.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-agent_loop_to_graph) · [Hint 1](agent_loop_to_graph_hints.md#hint-1) · [Hint 2](agent_loop_to_graph_hints.md#hint-2) · [Solution](agent_loop_to_graph_solution.md)

## Advanced Version

### Approach 1 — a real equivalence check against the original loop

```python
def run_original_loop(task: str) -> str:
    """Stand-in for your actual Doc07 while-loop function — same signature,
    same behavior, just imported from your Project 2 code in the real version."""
    decision = call_model_with_tools(task, [])
    if not decision["wants_tool"]:
        return decision["answer"]
    run_tool(decision["tool_name"], task)
    decision = call_model_with_tools(task, ["used tool"])
    return decision["answer"]


test_prompts = [
    "What is 12 * 7?",
    "What is 3 * 9?",
    "Say hello.",
]

mismatches = []
for prompt in test_prompts:
    loop_answer = run_original_loop(prompt)
    graph_result = graph.invoke(
        {"task": prompt, "scratchpad": [], "next_action": "", "final_answer": ""},
        config={"recursion_limit": 20},
    )
    graph_answer = graph_result["final_answer"]
    status = "MATCH" if loop_answer.strip() == graph_answer.strip() else "MISMATCH"
    print(f"[{status}] {prompt!r} -> loop={loop_answer!r} graph={graph_answer!r}")
    if status == "MISMATCH":
        mismatches.append(prompt)

if mismatches:
    raise AssertionError(f"Graph disagreed with the original loop on: {mismatches}")
print("All test prompts matched.")
```
**Expected output** (with the stub functions above — a real rebuild's output depends on your actual model and tools, but the pattern is identical):
```
[MATCH] 'What is 12 * 7?' -> loop='84' graph='84'
[MATCH] 'What is 3 * 9?' -> loop='84' graph='84'
[MATCH] 'Say hello.' -> loop='84' graph='84'
All test prompts matched.
```
(The stub `call_model_with_tools` here always answers `"84"` once it's decided it's done — in your real rebuild, swap in your actual Doc07 model call, and each prompt will get its own real answer instead of all matching by coincidence.)

### Approach 2 — comparing step counts too, not just final answers

```python
def run_graph_with_step_count(task: str) -> tuple[str, int]:
    step_count = 0
    result = graph.invoke(
        {"task": task, "scratchpad": [], "next_action": "", "final_answer": ""},
        config={"recursion_limit": 20},
    )
    # each "Thought:" entry in the scratchpad marks one think step
    step_count = sum(1 for line in result["scratchpad"] if line.startswith("Thought:"))
    return result["final_answer"], step_count


for prompt in test_prompts:
    answer, steps = run_graph_with_step_count(prompt)
    print(f"{prompt!r}: answer={answer!r}, steps={steps}")
```
**Expected output:**
```
'What is 12 * 7?': answer='84', steps=2
'What is 3 * 9?': answer='84', steps=2
'Say hello.': answer='84', steps=2
```
A matching final answer isn't the whole story — if the graph took, say, 6 steps to reach an answer your original loop reached in 2, that's worth investigating even though the final answer "passed." Counting `"Thought:"` entries in the scratchpad is a cheap way to catch a routing edge that loops more than it should.

**Difference from Intermediate:** Intermediate proves the graph runs correctly on one prompt. Approach 1 runs the exact comparison the exercise asks for — same test prompts, both implementations, an assertion that they agree — which is the only way to actually back up "gives the same answers as my original loop" instead of assuming it from one manual run. Approach 2 adds a second signal (step count) that a matching final answer alone can hide — two implementations can reach the same right answer while one of them is doing unnecessary, wasteful work getting there.

**Which one should you actually write?** Approach 1's equivalence check, always — run it against your real Doc07 loop and your real test prompts before you trust the rebuild for anything. Add Approach 2's step-count comparison once you have more than a couple of test prompts, or once you're debugging a case where the graph's answer is technically right but something about its path there feels off — it's the fastest way to catch a conditional edge that's routing through more loops than it needs to.
