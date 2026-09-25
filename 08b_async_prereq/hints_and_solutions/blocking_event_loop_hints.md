# Failure (accidentally blocking the event loop) — Hints

> [Back to the exercise](../README.md#ex-blocking_event_loop) · [Hint 1](blocking_event_loop_hints.md#hint-1) · [Hint 2](blocking_event_loop_hints.md#hint-2) · [Solution](blocking_event_loop_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried. Each hint has 2 depth levels: **Basic** (the plain idea) and **Intermediate** (proper Python, plus the actual fix, not just the diagnosis). Read Basic first even if you already know Python — it's the fastest way to spot exactly what Intermediate adds.

- [Hint 1 — The idea, and the exact pieces](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

<hr class="page-break">

> [Back to the exercise](../README.md#ex-blocking_event_loop) · [Hint 1](blocking_event_loop_hints.md#hint-1) · [Hint 2](blocking_event_loop_hints.md#hint-2) · [Solution](blocking_event_loop_solution.md)

## Hint 1 — The idea, and the exact pieces {: #hint-1 }

### Basic Version

You're going to break concurrency on purpose, so you recognize the *shape* of this bug when it happens by accident later.

The trick: `time.sleep(...)` and `asyncio.sleep(...)` look similar, but behave completely differently inside an `async def` function. `asyncio.sleep(...)` tells the event loop "I'm waiting, go do something else in the meantime." `time.sleep(...)` doesn't know the event loop exists at all — it just freezes the entire thread, event loop included, for that whole time.

Things to use:

- A "good" coroutine using `await asyncio.sleep(3)`.
- A "blocking" coroutine using `time.sleep(3)` instead — still `async def`, but nothing inside it ever awaits.
- `asyncio.gather(...)` to run both together, timed.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-blocking_event_loop) · [Hint 1](blocking_event_loop_hints.md#hint-1) · [Hint 2](blocking_event_loop_hints.md#hint-2) · [Solution](blocking_event_loop_solution.md)

### Intermediate Version

The exercise is really about one substitution — `time.sleep` in place of `await asyncio.sleep` — and what it does to a `gather` call that should otherwise run concurrently.

You'll write two coroutine functions, both sleeping the same duration so the comparison is clean, run together with `asyncio.gather(good_task(), blocking_task())`, timed with `time.perf_counter()` around the whole call. If concurrency were actually happening, the total time should be roughly the max of the two (about 3 seconds). Predict, before running it, what you think the actual total will be instead.

The exact pieces:

- **`time.sleep(3)` inside an `async def` function** — still syntactically legal Python; nothing raises an error. The function is still a coroutine because of `async def`, but since it never hits an `await`, the event loop has no opportunity to pause it and run something else.
- **`await asyncio.sleep(3)`** — genuinely returns control to the event loop, which is exactly what lets a *second* coroutine run during that wait.
- **The comparison that proves it:** two "good" coroutines run together finish in ~3 seconds (the max). One "good" and one "blocking" finish in ~6 seconds (the sum) — the blocking one froze everything else, including the good one, until it was done.
- **No error, no warning:** this is what makes the bug sneaky — the code runs, gives a correct final answer, and the only symptom is that it took twice as long as it should have.

Think about where this actually happens in real code — nobody writes `time.sleep(3)` inside an `async def` function on purpose in production. It happens by accident, almost always the same way: someone reaches for a library that only ships a synchronous version — a database driver, a file-parsing library, `requests` instead of `httpx`/`aiohttp` — and calls it from inside an `async def` function without realizing that call blocks the whole event loop exactly like `time.sleep` does here, just less obviously, since it doesn't have "sleep" in its name to give it away.

The real design question isn't just "did I accidentally block the loop" — it's "what do I do when the work I need genuinely has no async version, and I can't just rewrite the library myself?"

The extra piece that answers that question:

- **`asyncio.to_thread(...)`** (or the lower-level `loop.run_in_executor(...)`) runs a normal, blocking, synchronous function in a separate thread, and gives you back something you `await` — so the event loop stays free to run other coroutines while that blocking call happens somewhere else. `result = await asyncio.to_thread(some_blocking_function, arg1, arg2)` is the fix any time you're stuck calling code that was never written to be async.

**Difference between Basic and Intermediate:** Basic diagnoses the bug — spot it, measure it, understand why it's silent. Intermediate also answers the question that leaves open: once you find a real blocking call you can't avoid (a sync-only library, not a `time.sleep()` typo), `asyncio.to_thread(...)` is how you keep the event loop free anyway, without rewriting the blocking code itself.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-blocking_event_loop) · [Hint 1](blocking_event_loop_hints.md#hint-1) · [Hint 2](blocking_event_loop_hints.md#hint-2) · [Solution](blocking_event_loop_solution.md)

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

### Basic Version

```
make an async function called good_task that takes nothing:
    wait 3 seconds the correct way (asyncio.sleep),
        without freezing anything else
    give back "good"

make an async function called blocking_task that takes nothing:
    wait 3 seconds the wrong way (time.sleep) -- this freezes everything
    give back "blocking"

time this:
    run good_task and good_task together with gather
    -> expect around 3 seconds (they really overlap)

time this too:
    run good_task and blocking_task together with gather
    -> expect around 6 seconds
       (blocking_task froze everything, nothing overlapped)
```

Here's almost the whole thing — just try running it and reading it line by line:
```python
# blocking_event_loop_practice.py
import asyncio
import time

async def good_task():
    await asyncio.sleep(3)
    return "good"

async def blocking_task():
    time.sleep(3)
    return "blocking"

async def time_it(label, coro_a, coro_b):
    start = time.perf_counter()
    results = await asyncio.gather(coro_a, coro_b)
    elapsed = time.perf_counter() - start
    print(label, elapsed, results)
```
**Expected output if you run just this:** nothing — add a `main()` that calls `time_it` twice (once with two `good_task()`s, once with a `good_task()` and a `blocking_task()`) and an `asyncio.run(main())` call to see the two very different timings.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-blocking_event_loop) · [Hint 1](blocking_event_loop_hints.md#hint-1) · [Hint 2](blocking_event_loop_hints.md#hint-2) · [Solution](blocking_event_loop_solution.md)

### Intermediate Version

```
import asyncio
import time

define:
    async def good_task() -> str:
        await asyncio.sleep(3)
        return "good"

define:
    async def blocking_task() -> str:
        time.sleep(3)             # the bug: no await, freezes the whole loop
        return "blocking"

define:
    async def time_it(label: str, coro_a, coro_b) -> None:
        start = time.perf_counter()
        results = await asyncio.gather(coro_a, coro_b)
        elapsed = time.perf_counter() - start
        print(f"{label} took {elapsed:.2f}s -> {results}")

define:
    async def main() -> None:
        await time_it("two good tasks:", good_task(), good_task())
        await time_it("good + blocking:", good_task(), blocking_task())

if __name__ == "__main__":
    asyncio.run(main())
```
Fill in `main()` and the entry point yourself, then compare against the [Solution](blocking_event_loop_solution.md).

Once that's working, fix it without touching the blocking call itself:

```
make a fixed version of blocking_task that uses asyncio.to_thread
instead of calling time.sleep directly:

async def fixed_task():
    await asyncio.to_thread(time.sleep, 3)   # still calls the real
                                               # blocking function, but
                                               # off the loop's thread
    return "fixed"

time this:
    run good_task and fixed_task together with gather
    -> expect around 3 seconds again, even though fixed_task still
       calls time.sleep internally
```

```python
# blocking_event_loop_practice.py
async def fixed_task() -> str:
    await asyncio.to_thread(time.sleep, 3)
    return "fixed"


async def main_fixed() -> None:
    await time_it("good + fixed (to_thread):", good_task(), fixed_task())
```
Add this third comparison to your `main()` from the Basic version, run all 3, and confirm `"good + fixed"` comes back close to 3 seconds — not 6, like `"good + blocking"` did — then compare against the [Solution](blocking_event_loop_solution.md).

**Difference between Basic and Intermediate:** Basic stops at showing the bug and measuring it. Intermediate also fixes it without touching the blocking call itself — `asyncio.to_thread(time.sleep, 3)` still calls the exact same blocking `time.sleep`, just from a separate thread the event loop doesn't have to wait on directly, which is exactly the pattern you'd reach for with a real sync-only library you can't rewrite.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-blocking_event_loop) · [Hint 1](blocking_event_loop_hints.md#hint-1) · [Hint 2](blocking_event_loop_hints.md#hint-2) · [Solution](blocking_event_loop_solution.md)

Full solution: [Show me the solution](blocking_event_loop_solution.md)
