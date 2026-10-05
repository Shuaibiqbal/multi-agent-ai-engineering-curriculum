# Failure (search fails mid-run) — Hints

> [Back to the exercise](../README.md#ex-search_failure) · [Hint 1](search_failure_hints.md#hint-1) · [Hint 2](search_failure_hints.md#hint-2) · [Solution](search_failure_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried. Each hint has 2 depth levels: **Basic** (the plain idea) and **Intermediate** (proper Python, plus the cases a real project has to handle).

- [Hint 1 — The idea, and the exact pieces](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

<hr class="page-break">

> [Back to the exercise](../README.md#ex-search_failure) · [Hint 1](search_failure_hints.md#hint-1) · [Hint 2](search_failure_hints.md#hint-2) · [Solution](search_failure_solution.md)

## Hint 1 — The idea, and the exact pieces {: #hint-1 }

### Basic Version

Make a two-node graph — `plan_node`, then `search_node` — with a checkpointer, and make `search_node` raise on purpose. Catch the error, then call `graph.get_state(config)`: `plan_node`'s work should still be saved, and `.next` should say the run stopped before `search_node`.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-search_failure) · [Hint 1](search_failure_hints.md#hint-1) · [Hint 2](search_failure_hints.md#hint-2) · [Solution](search_failure_solution.md)

### Intermediate Version

The exact pieces:

- `try: graph.invoke(...)` / `except RuntimeError` — and a `raise AssertionError(...)` right after `invoke()`, so the test fails if the crash ever stops happening.
- `snapshot = graph.get_state(config)` — `.values` is the saved state, `.next` the node that was about to run (Doc09).
- `build_graph(search_node)` taking the search node as a parameter, so later approaches plug in a real one.

Then the real question: should every failure fail the run? A `TimeoutError` or `ConnectionError` is often gone a second later — retry it, waiting a little longer each time (Doc02's backoff). A bad query or a bug fails the same way every time — raise it at once. To *test* that, you need a search that fails on demand: Doc07's fail-once counter idea, as a small `FlakySearch` class.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-search_failure) · [Hint 1](search_failure_hints.md#hint-1) · [Hint 2](search_failure_hints.md#hint-2) · [Solution](search_failure_solution.md)

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

### Basic Version

```
plan_node:   {"plan": "search the documents for: " + task}
search_node: raise RuntimeError("simulated vector store outage")
graph: START -> plan -> search -> END, MemorySaver()

try invoke, catch the RuntimeError,
then print graph.get_state(config).values and .next
```

<hr class="page-break">

> [Back to the exercise](../README.md#ex-search_failure) · [Hint 1](search_failure_hints.md#hint-1) · [Hint 2](search_failure_hints.md#hint-2) · [Solution](search_failure_solution.md)

### Intermediate Version

```
TRANSIENT_ERRORS = (TimeoutError, ConnectionError); MAX_ATTEMPTS = 3

search_with_retry(search, query):
    for attempt in range(MAX_ATTEMPTS):
        try: return search(query)
        except TRANSIENT_ERRORS: last attempt -> raise; else sleep 2 ** attempt

FlakySearch(fail_times, error): .search(query) raises `error` for the
    first fail_times calls (count them in call_count), then really searches

tests: 2 timeouts then success (call_count == 3); a ValueError raised at
       once (call_count == 1); retries used up -> state still saved
```

**Difference between Basic and Intermediate:** Basic proves state survives one crash. Intermediate retries only the errors worth retrying, and proves every outcome with a search that fails on demand.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-search_failure) · [Hint 1](search_failure_hints.md#hint-1) · [Hint 2](search_failure_hints.md#hint-2) · [Solution](search_failure_solution.md)

Full solution: [Show me the solution](search_failure_solution.md)
