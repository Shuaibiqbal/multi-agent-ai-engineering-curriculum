# Step 1 — A 2-Node Graph With No Branching, Just to Prove the Mechanics — Hints

> [Back to this step](../READING_README.md#step-1-a-2-node-graph-with-no-branching-just-to-prove-the-mechanics) · [Hint 1](step1_graph_basics_hints.md#hint-1) · [Hint 2](step1_graph_basics_hints.md#hint-2) · [Solution](step1_graph_basics_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've really tried. Each hint starts with the plain idea, then shows the shape of the real code.

- [Hint 1 — The three pieces of a graph](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

<hr class="page-break">

> [Back to this step](../READING_README.md#step-1-a-2-node-graph-with-no-branching-just-to-prove-the-mechanics) · [Hint 1](step1_graph_basics_hints.md#hint-1) · [Hint 2](step1_graph_basics_hints.md#hint-2) · [Solution](step1_graph_basics_solution.md)

## Hint 1 — The three pieces of a graph {: #hint-1 }

A LangGraph graph has three pieces (Doc09):

- **state** — one `TypedDict` listing every field the graph carries;
- **nodes** — plain functions: take the state, return a dict of *only* the fields they change;
- **edges** — which node runs after which, from `START` to `END`.

For this step: two nodes, `clean_task` (strip the question) and `answer_node` (ask the model), joined in a straight line. `graph.invoke(starting_state)` runs them and returns the final state.

Put each piece in its own file, the way Doc09's Build Task did:

- `state.py` — `DocState` with `task`, `answer`, and `path: Annotated[list[str], operator.add]`. The `operator.add` tells LangGraph to **append** what a node returns for `path`, instead of replacing it — so `return {"path": ["clean_task"]}` adds one entry. Add `start_state(task)`, which returns every field with a starting value.
- `nodes.py` — each node returns its own name in `path`. `answer_node` uses a Doc05 chain: `ChatPromptTemplate.from_template(load_prompt("general")) | get_model() | StrOutputParser()`.
- `models/llm.py` — `get_model()` takes no arguments: nodes only receive the state, so they build the model themselves. `ChatOpenAI` reads the key that `load_config()` loaded.

<hr class="page-break">

> [Back to this step](../READING_README.md#step-1-a-2-node-graph-with-no-branching-just-to-prove-the-mechanics) · [Hint 1](step1_graph_basics_hints.md#hint-1) · [Hint 2](step1_graph_basics_hints.md#hint-2) · [Solution](step1_graph_basics_solution.md)

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

```
build_graph():
    builder = StateGraph(DocState)
    builder.add_node("clean_task", clean_task)
    builder.add_node("answer_node", answer_node)
    builder.add_edge(START, "clean_task")
    builder.add_edge("clean_task", "answer_node")
    builder.add_edge("answer_node", END)
    return builder.compile()
```

`main.py`:

```
load_config()  (exit with one line on MissingConfigError)
graph = build_graph()
loop:
    task = input("You: ").strip()   — "/quit" stops, "" skips
    result = graph.invoke(start_state(task))
    print("path:", " -> ".join(result["path"]))
    print("Answer:", result["answer"])
```

Before running it, write down what the state looks like after each node. Then run it and compare with the printed `path`.

Full solution: [Show me the solution](step1_graph_basics_solution.md)
