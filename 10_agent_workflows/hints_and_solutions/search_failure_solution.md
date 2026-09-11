# Failure (search fails mid-run) — Solution

> [Back to the exercise](../README.md#ex-search_failure) · [Hint 1](search_failure_hints.md#hint-1) · [Hint 2](search_failure_hints.md#hint-2) · [Solution](search_failure_solution.md)

Read all three depths — they're not "wrong, less wrong, right," they're 3 real, valid ways to solve the same problem, with real tradeoffs between them.

## Basic Version

### Approach 1 — the direct way

```python
from langgraph.checkpoint.memory import MemorySaver

def search_node(state):
    raise RuntimeError("simulated vector store outage")   # temporary, for this test

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "failure-test-1"}}

try:
    graph.invoke({"task": "What does the policy say about refunds?"}, config)
except RuntimeError as e:
    print("Caught expected failure:", e)

snapshot = graph.get_state(config)
print("Surviving state:", snapshot.values)
print("Was about to run:", snapshot.next)
```

This confirms state survives the crash and prints it. It doesn't assert anything specific about that state's correctness — just prints it for a human to eyeball.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-search_failure) · [Hint 1](search_failure_hints.md#hint-1) · [Hint 2](search_failure_hints.md#hint-2) · [Solution](search_failure_solution.md)

## Intermediate Version

### Approach 1 — real assertions, and a test that fails loudly if the crash stops happening

```python
from langgraph.checkpoint.memory import MemorySaver


def search_node(state: dict) -> dict:
    raise RuntimeError("simulated vector store outage")   # temporary, for this test


def test_state_survives_search_failure() -> None:
    checkpointer = MemorySaver()
    graph = builder.compile(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": "failure-test-1"}}

    try:
        graph.invoke({"task": "What does the policy say about refunds?"}, config)
        raise AssertionError("expected the graph to raise, but it didn't")
    except RuntimeError as e:
        print(f"Caught expected failure: {e}")

    snapshot = graph.get_state(config)
    assert "task" in snapshot.values, "the original task should still be in state"
    assert snapshot.next == ("search_node",), "the graph should have stopped right before search_node"
    print("Confirmed: pre-failure state is intact, and the graph knows exactly where it stopped.")


test_state_survives_search_failure()
```

**Difference from Basic:** full type hints. Wrapping the test in a function with real assertions, not just prints — this is the difference between "I looked at it and it seemed fine" and a test you can rerun automatically after any future change. The extra `raise AssertionError` if the graph *doesn't* fail is a safety check — without it, a bug that accidentally makes `search_node` stop raising would make this whole test silently pass without testing anything. This version still gives up completely on the first failure — no retry — which is what Advanced changes.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-search_failure) · [Hint 1](search_failure_hints.md#hint-1) · [Hint 2](search_failure_hints.md#hint-2) · [Solution](search_failure_solution.md)

## Advanced Version

### Approach 1 — a retry with backoff, transient errors only

```python
import time

TRANSIENT_ERRORS = (TimeoutError, ConnectionError)
MAX_ATTEMPTS = 3


def search_node(state: dict) -> dict:
    for attempt in range(MAX_ATTEMPTS):
        try:
            results = retrieve(state["task"])
            return {"sources": results}
        except TRANSIENT_ERRORS as exc:
            if attempt == MAX_ATTEMPTS - 1:
                raise
            wait_seconds = 2 ** attempt
            print(f"Search attempt {attempt + 1} failed ({exc}); retrying in {wait_seconds}s")
            time.sleep(wait_seconds)
    # unreachable: the loop above always returns or raises
    raise RuntimeError("search_node exited its retry loop unexpectedly")
```
A `TimeoutError` or `ConnectionError` gets up to `MAX_ATTEMPTS` tries, with a growing delay between them (1s, then 2s), so a brief network blip is absorbed automatically. Anything else — a malformed query, a programming bug — is not in `TRANSIENT_ERRORS`, so it propagates immediately on the first attempt; retrying a bug five times just wastes five times as long finding out it still doesn't work.

### Approach 2 — retry plus proving both outcomes with a real test

Approach 1 is the retry logic itself; this approach tests it the way `search_failure`'s own lesson demands — proving both that a transient failure recovers, and that state still survives when retries are genuinely exhausted.

```python
import time
from langgraph.checkpoint.memory import MemorySaver

TRANSIENT_ERRORS = (TimeoutError, ConnectionError)
MAX_ATTEMPTS = 3


def make_search_node(fail_times: int, permanent: bool = False):
    """Test helper: builds a search_node that fails `fail_times` before succeeding."""
    calls = {"count": 0}

    def search_node(state: dict) -> dict:
        for attempt in range(MAX_ATTEMPTS):
            calls["count"] += 1
            if calls["count"] <= fail_times:
                if permanent:
                    raise ValueError("malformed query")  # not transient -- no retry
                raise TimeoutError("simulated timeout")
            return {"sources": ["a real result"]}
        raise RuntimeError("exhausted retries")

    return search_node


def test_recovers_from_transient_failure() -> None:
    node = make_search_node(fail_times=2)  # fails twice, then succeeds
    result = node({"task": "test"})
    assert result["sources"] == ["a real result"]
    print("Recovered after 2 transient failures, as expected.")


def test_permanent_failure_does_not_retry() -> None:
    node = make_search_node(fail_times=1, permanent=True)
    try:
        node({"task": "test"})
        raise AssertionError("expected a ValueError, but none was raised")
    except ValueError:
        print("Permanent failure raised immediately, with no retry delay, as expected.")


def test_state_survives_when_retries_are_exhausted() -> None:
    checkpointer = MemorySaver()
    graph = builder.compile(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": "exhausted-retries-test"}}

    try:
        graph.invoke({"task": "something needing search"}, config)
        raise AssertionError("expected the graph to eventually raise")
    except TimeoutError:
        pass

    snapshot = graph.get_state(config)
    assert "task" in snapshot.values
    print("Even after all retries were exhausted, pre-failure state is still intact.")


test_recovers_from_transient_failure()
test_permanent_failure_does_not_retry()
test_state_survives_when_retries_are_exhausted()
```

**Difference from Intermediate, and between these 2 Advanced approaches:** Intermediate proves the checkpointer's guarantee once, against a node that fails exactly once and stays failed — a correct but incomplete picture of a real deployment, where most external failures are brief. Approach 1 adds the retry logic itself: transient errors get a few chances with growing delays, permanent errors fail immediately. Approach 2 doesn't change the retry logic at all — it proves all three outcomes a reviewer would actually want confirmed: recovery after a transient blip, no wasted retries on a permanent failure, and Intermediate's original "state survives" guarantee still holding even when every retry is used up.

**Which one should you actually write?** Intermediate's plain crash-and-check test is worth keeping regardless — it's the simplest proof the checkpointing promise holds at all, and it's what `search_failure`'s Core Concepts point is really about. Add Advanced Approach 1's retry loop the moment your search backend is a real network service instead of a local file or in-memory store — a single dropped connection shouldn't fail an entire user-facing run. Approach 2's three-part test suite is worth writing once the retry logic itself is something other people (or future you) will change — a retry loop with no test can silently start retrying permanent failures, or stop retrying transient ones, without anyone noticing until it matters.
