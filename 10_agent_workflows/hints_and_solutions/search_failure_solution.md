# Failure (search fails mid-run) — Solution

> [Back to the exercise](../README.md#ex-search_failure) · [Hint 1](search_failure_hints.md#hint-1) · [Hint 2](search_failure_hints.md#hint-2) · [Solution](search_failure_solution.md)

**Story — `search_failure_practice.py`:** a checkpointer's whole promise is that a crash doesn't erase earlier progress — this exercise proves it, by making search fail on purpose. **If not:** the Build Task's first real outage would also be your first time finding out what's left after a crash.

## Solution

```python
# search_failure_practice.py
from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

class FailureState(TypedDict):
    task: str
    plan: str
    sources: list[dict]

def plan_node(state: FailureState) -> dict:
    return {"plan": f"search the documents for: {state['task']}"}

def broken_search_node(state: FailureState) -> dict:
    # temporary, for this test
    raise RuntimeError("simulated vector store outage")

def build_graph(search_node):
    builder = StateGraph(FailureState)
    builder.add_node("plan_node", plan_node)
    builder.add_node("search_node", search_node)
    builder.add_edge(START, "plan_node")
    builder.add_edge("plan_node", "search_node")
    builder.add_edge("search_node", END)
    return builder.compile(checkpointer=MemorySaver())

def test_state_survives_search_failure() -> None:
    graph = build_graph(broken_search_node)
    config = {"configurable": {"thread_id": "failure-test-1"}}
    try:
        graph.invoke({"task": "How hot should the water be?"}, config)
        raise AssertionError("expected the graph to raise, but it didn't")
    except RuntimeError as e:
        print(f"Caught expected failure: {e}")

    snapshot = graph.get_state(config)
    assert snapshot.values["plan"].startswith("search the documents")
    assert snapshot.next == ("search_node",)
    print("Confirmed: plan_node's work survived, and the graph knows")
    print("it stopped before search_node.")

# Run the test: the graph should survive a search node that raises.
test_state_survives_search_failure()
```
**Expected output:**
```
Caught expected failure: simulated vector store outage
Confirmed: plan_node's work survived, and the graph knows
it stopped before search_node.
```
