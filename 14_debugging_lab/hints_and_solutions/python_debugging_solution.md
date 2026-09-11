# Python Debugging — Worked Example: Solution

> [Back to the exercise](../README.md#dbg-python) · [Round 1: Basic](python_debugging_hints.md#round-basic) · [Round 2: Intermediate](python_debugging_hints.md#round-intermediate) · [Round 3: Real-world](python_debugging_hints.md#round-real-world) · [Round 4: Multi-agent](python_debugging_hints.md#round-multi-agent) · [Hints](python_debugging_hints.md)

- [Round 1: Basic](#round-basic)
- [Round 2: Intermediate](#round-intermediate)
- [Round 3: Real-world](#round-real-world)
- [Round 4: Multi-agent](#round-multi-agent)
- [Real cause vs. symptom fix](#real-cause-vs-symptom-fix)

<hr class="page-break">

> [Back to the exercise](../README.md#dbg-python) · [Round 1: Basic](python_debugging_hints.md#round-basic) · [Round 2: Intermediate](python_debugging_hints.md#round-intermediate) · [Round 3: Real-world](python_debugging_hints.md#round-real-world) · [Round 4: Multi-agent](python_debugging_hints.md#round-multi-agent) · [Hints](python_debugging_hints.md)

## Round: Basic {: #round-basic }

**Real cause:** `trim_history()` never has a `return` statement on the path where `len(trimmed) % 2 != 0` is false — it just falls off the end of the function, and a function with no `return` always gives back `None`.

**The fix:**
```python
def trim_history(history, max_turns):
    trimmed = history[-max_turns:]
    if len(trimmed) % 2 != 0:
        trimmed = trimmed[1:]
    return trimmed
```

**Test that would have caught it:**
```python
def test_trim_history_returns_a_list():
    history = ["a", "b", "c", "d"]
    result = trim_history(history, 4)
    assert result is not None
    assert isinstance(result, list)
```
Reading the trace from the bottom up: the error fires at the `for msg in ...` line, but the actual bug is one function call away — the fastest read is "something is returning `None`," then going straight to that function and checking every branch has a `return`.

<hr class="page-break">

> [Back to the exercise](../README.md#dbg-python) · [Round 1: Basic](python_debugging_hints.md#round-basic) · [Round 2: Intermediate](python_debugging_hints.md#round-intermediate) · [Round 3: Real-world](python_debugging_hints.md#round-real-world) · [Round 4: Multi-agent](python_debugging_hints.md#round-multi-agent) · [Hints](python_debugging_hints.md)

## Round: Intermediate {: #round-intermediate }

**Real cause:** `notes=[]` is a **mutable default argument**. Python creates that empty list exactly once, when the function is defined — not once per call. Every call to `log_turn()` that doesn't pass its own `notes` argument gets the *same* list object back, and keeps appending to it, for as long as the process stays alive. It looks like a session/state bug because the symptom is "data leaking between sessions" — but no session code is involved at all; it's one shared list living on the function object itself.

**The fix:**
```python
def log_turn(role, text, notes=None):
    if notes is None:
        notes = []
    notes.append(role + ": " + text[:40])
    return notes
```
Using `None` as the default, and creating a fresh list inside the function body, means every call that doesn't pass its own list gets a brand new one.

**Test that would have caught it:**
```python
def test_log_turn_does_not_leak_between_calls():
    first_session = log_turn("user", "what is the refund policy?")
    second_session = log_turn("user", "how do I reset my password?")
    assert len(second_session) == 1
    assert "refund" not in second_session[0]
```
This test calls the function twice in a row, on purpose, without passing `notes` — exactly the condition that never shows up if every test only ever calls a function once.

<hr class="page-break">

> [Back to the exercise](../README.md#dbg-python) · [Round 1: Basic](python_debugging_hints.md#round-basic) · [Round 2: Intermediate](python_debugging_hints.md#round-intermediate) · [Round 3: Real-world](python_debugging_hints.md#round-real-world) · [Round 4: Multi-agent](python_debugging_hints.md#round-multi-agent) · [Hints](python_debugging_hints.md)

## Round: Real-world {: #round-real-world }

**Real cause:** `for key in cache:` iterates directly over the dictionary while `del cache[key]` changes its size inside that same loop. Python detects this and raises `RuntimeError` — but only once a delete actually happens mid-loop. A cache with nothing expired yet just loops harmlessly to the end, which is exactly why quick manual testing (fresh cache, nothing expired) never triggers it.

**The fix:**
```python
def clear_expired(cache, now):
    expired_keys = []
    for key in cache:
        if cache[key]["expires_at"] < now:
            expired_keys.append(key)

    for key in expired_keys:
        del cache[key]
```
Collect the keys to remove in a first pass, then delete them in a second pass, after the first loop over `cache` has already finished.

**Test that would have caught it:**
```python
def test_clear_expired_removes_entries_without_crashing():
    cache = {
        "a": {"expires_at": 1},
        "b": {"expires_at": 100},
        "c": {"expires_at": 1},
    }
    clear_expired(cache, now=50)
    assert "a" not in cache
    assert "c" not in cache
    assert "b" in cache
```
The test that "passed" during development only ever ran against an empty or all-fresh cache — the real test has to include at least one entry that's actually supposed to be deleted, otherwise the buggy loop never gets exercised.

<hr class="page-break">

> [Back to the exercise](../README.md#dbg-python) · [Round 1: Basic](python_debugging_hints.md#round-basic) · [Round 2: Intermediate](python_debugging_hints.md#round-intermediate) · [Round 3: Real-world](python_debugging_hints.md#round-real-world) · [Round 4: Multi-agent](python_debugging_hints.md#round-multi-agent) · [Hints](python_debugging_hints.md)

## Round: Multi-agent {: #round-multi-agent }

**Real cause:** the exact same mutable-default-argument bug as Round 2, just in a place where the usual test (call the node once, check the `Command`) can't see it. `test_route()` only calls `route(state)` a single time before the test process exits, so the shared default list only ever has one entry in it when the assertion runs — it looks correct. The bug only appears once the *same process* handles several requests back to back, which a live multi-agent run does constantly and a narrow unit test never does.

**The fix:**
```python
def route(state, notes=None):
    if notes is None:
        notes = []
    notes.append(state["task"])
    next_agent = pick_agent(state)
    return Command(goto=next_agent, update={"routing_notes": notes})
```

**Test that would have caught it:**
```python
def test_route_does_not_leak_notes_across_requests():
    state_one = {"task": "summarize Q1 sales report"}
    state_two = {"task": "write a release blog post"}

    route(state_one)
    result_two = route(state_two)

    routing_notes = result_two.update["routing_notes"]
    assert len(routing_notes) == 1
    assert routing_notes[0] == "write a release blog post"
```
Same fix as Round 2, but the test that catches it has to call the node function more than once in the same process — a single-call unit test structurally cannot catch this bug, no matter how carefully it checks its one result.

<hr class="page-break">

> [Back to the exercise](../README.md#dbg-python) · [Round 1: Basic](python_debugging_hints.md#round-basic) · [Round 2: Intermediate](python_debugging_hints.md#round-intermediate) · [Round 3: Real-world](python_debugging_hints.md#round-real-world) · [Round 4: Multi-agent](python_debugging_hints.md#round-multi-agent) · [Hints](python_debugging_hints.md)

## Real cause vs. symptom fix {: #real-cause-vs-symptom-fix }

A symptom fix for Round 2 or 4 would be wrapping the caller in a `try/except` that clears `notes` whenever it looks "too long," or restarting the process between sessions so the shared list never has time to grow. Both would make the immediate failure go away without touching the actual bug — the shared default list would still be there, waiting to cause the same failure the next time the workaround doesn't quite cover the case. The real-cause fix is always the same one line, `if notes is None: notes = []`, because the real cause is always the same thing: a default argument evaluated once at definition time, silently shared by every call that doesn't override it. This is Core Concepts' "real cause vs. symptom fix" distinction directly — the fix that's actually correct is the one that would still work if you didn't know exactly when or how often the bug shows up.
