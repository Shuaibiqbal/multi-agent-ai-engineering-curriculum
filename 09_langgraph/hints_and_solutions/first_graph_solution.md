# Basic (your first graph) — Solution

> [Back to the exercise](../README.md#ex-first_graph) · [Hint 1](first_graph_hints.md#hint-1) · [Hint 2](first_graph_hints.md#hint-2) · [Solution](first_graph_solution.md)

**Story — `first_graph_practice.py`:** this is the smallest possible LangGraph graph — one field, two nodes, one edge — deliberately tiny so the 3 real ingredients (state, nodes, edges) are visible on their own, before Doc07's whole agent loop gets rebuilt as a graph in the next exercise. **If not:** `agent_loop_to_graph` would be the first place you ever saw `StateGraph`/`add_node`/`add_edge` at all, with a much bigger graph to learn them from.

## Solution

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
