# Failure (search fails mid-run) — Hints

> [Back to the exercise](../README.md#ex-search_failure) · [Hint 1](search_failure_hints.md#hint-1) · [Hint 2](search_failure_hints.md#hint-2) · [Solution](search_failure_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried.

- [Hint 1 — The idea, and the exact pieces](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

## Hint 1 — The idea, and the exact pieces {: #hint-1 }

The exact pieces:

- `try: graph.invoke(...)` / `except RuntimeError` — and a `raise AssertionError(...)` right after `invoke()`, so the test fails if the crash ever stops happening.
- `snapshot = graph.get_state(config)` — `.values` is the saved state, `.next` the node that was about to run (Doc09).
- `build_graph(search_node)` taking the search node as a parameter, so later approaches plug in a real one.

Then the real question: should every failure fail the run? A `TimeoutError` or `ConnectionError` is often gone a second later — retry it, waiting a little longer each time (Doc02's backoff). A bad query or a bug fails the same way every time — raise it at once. To *test* that, you need a search that fails on demand: Doc07's fail-once counter idea, as a small `FlakySearch` class.

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

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

Full solution: [Show me the solution](search_failure_solution.md)
