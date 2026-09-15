# Basic (your first graph) — Solution

> [Back to the exercise](../README.md#ex-first_graph) · [Hint 1](first_graph_hints.md#hint-1) · [Hint 2](first_graph_hints.md#hint-2) · [Solution](first_graph_solution.md)

Read all three depths — they're not "wrong, less wrong, right," they're 3 real, valid ways to solve the same problem, with real tradeoffs between them.

## Basic Version

### Approach 1 — `set_entry_point` / `set_finish_point`

```python
# first_graph_practice.py
from typing import TypedDict
from langgraph.graph import StateGraph


class GraphState(TypedDict):
    message: str


def node_one(state):
    return {"message": "Hello"}


def node_two(state):
    return {"message": state["message"] + ", World!"}


builder = StateGraph(GraphState)
builder.add_node("node_one", node_one)
builder.add_node("node_two", node_two)
builder.add_edge("node_one", "node_two")
builder.set_entry_point("node_one")
builder.set_finish_point("node_two")

graph = builder.compile()
result = graph.invoke({"message": "start"})
print(result)
```
**Expected output:**
```
{'message': 'Hello, World!'}
```
`set_entry_point("node_one")` and `set_finish_point("node_two")` are convenience methods — under the hood they're doing exactly `add_edge(START, "node_one")` and `add_edge("node_two", END)`, just without you importing `START`/`END` yourself. This version works correctly and traces exactly how you'd expect by hand: `node_one` sets `message` to `"Hello"`, then `node_two` reads that and appends `", World!"`.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-first_graph) · [Hint 1](first_graph_hints.md#hint-1) · [Hint 2](first_graph_hints.md#hint-2) · [Solution](first_graph_solution.md)

## Intermediate Version

### Approach 1 — explicit `START`/`END`, with type hints

```python
# first_graph_practice.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class GraphState(TypedDict):
    message: str


def node_one(state: GraphState) -> dict:
    return {"message": "Hello"}


def node_two(state: GraphState) -> dict:
    return {"message": state["message"] + ", World!"}


builder = StateGraph(GraphState)
builder.add_node("node_one", node_one)
builder.add_node("node_two", node_two)
builder.add_edge(START, "node_one")
builder.add_edge("node_one", "node_two")
builder.add_edge("node_two", END)

graph = builder.compile()
result = graph.invoke({"message": "start"})
print(result)
```
**Expected output:**
```
{'message': 'Hello, World!'}
```

**Difference from Basic:** same graph, same result — this version just spells out the entry and exit as real edges (`add_edge(START, "node_one")`, `add_edge("node_two", END)`) instead of using the `set_entry_point`/`set_finish_point` shortcuts, and adds type hints (`state: GraphState`, `-> dict`) to both node functions. Being explicit about `START`/`END` matters more once a graph has more than one possible entry or exit point — a shortcut method can only point at one node at a time, while `add_edge(START, ...)` can be called more than once if you ever need multiple entry nodes.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-first_graph) · [Hint 1](first_graph_hints.md#hint-1) · [Hint 2](first_graph_hints.md#hint-2) · [Solution](first_graph_solution.md)

## Advanced Version

### Approach 1 — a second field with a reducer

```python
# first_graph_practice.py
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END


class GraphState(TypedDict):
    message: str
    log: Annotated[list[str], operator.add]


def node_one(state: GraphState) -> dict:
    return {"message": "Hello", "log": ["node_one ran"]}


def node_two(state: GraphState) -> dict:
    return {"message": state["message"] + ", World!", "log": ["node_two ran"]}


builder = StateGraph(GraphState)
builder.add_node("node_one", node_one)
builder.add_node("node_two", node_two)
builder.add_edge(START, "node_one")
builder.add_edge("node_one", "node_two")
builder.add_edge("node_two", END)

graph = builder.compile()
result = graph.invoke({"message": "start", "log": []})
print(result)
```
**Expected output:**
```
{'message': 'Hello, World!', 'log': ['node_one ran', 'node_two ran']}
```
Notice `log` ends up with **both** entries, in order — `node_two`'s returned `{"log": ["node_two ran"]}` didn't overwrite `node_one`'s write, because `operator.add` (list concatenation) ran instead of the default plain overwrite. `message` still just overwrites, because it has no reducer annotation — proving both merge behaviors side by side in the same state shape.

**Difference from Intermediate:** Intermediate's single `message` field only ever needs (and only ever gets) the default overwrite behavior. This version adds a second field, `log`, annotated `Annotated[list[str], operator.add]`, so LangGraph calls `operator.add(old_log, new_log)` to merge instead of replacing — the one piece of machinery you need the moment a field should accumulate a history instead of holding a single current value.

**Which one should you actually write?** For a graph this small, Basic's `set_entry_point`/`set_finish_point` is perfectly fine and reads cleanly. Once a graph gets more than a couple of nodes, or you can imagine adding a second entry point later, switch to Intermediate's explicit `START`/`END` edges — it's the form you'll see in almost every real LangGraph example, so it's worth being fluent in it early. Reach for Advanced's reducer pattern the moment any field in your state needs to grow instead of being replaced — a running log, a list of tool calls, a list of sources found — which is most real graphs past this first exercise.
