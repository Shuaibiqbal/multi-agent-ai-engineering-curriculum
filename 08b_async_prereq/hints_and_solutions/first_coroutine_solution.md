# Basic (your first coroutine) — Solution

> [Back to the exercise](../README.md#ex-first_coroutine) · [Hint 1](first_coroutine_hints.md#hint-1) · [Hint 2](first_coroutine_hints.md#hint-2) · [Solution](first_coroutine_solution.md)

## Basic Version

### Approach 1 — the direct way

```python
import asyncio

async def wait_and_return():
    await asyncio.sleep(1)
    return "done"

# the mistake: calling it with no await and no asyncio.run
unstarted = wait_and_return()
print(unstarted)   # something like: <coroutine object wait_and_return at 0x...>

# the fix: asyncio.run actually starts the event loop and runs it to completion
result = asyncio.run(wait_and_return())
print(result)       # "done"
```
**Expected output:**
```
<coroutine object wait_and_return at 0x7f2a1c0b1a40>
done
```
The first `print` shows a coroutine object — `wait_and_return()` on its own never ran the function body, it just built a suspended coroutine and handed it back unstarted. The second `print` shows `"done"`, because `asyncio.run(...)` is what actually drives that coroutine to completion (waiting the 1 second along the way) and gives you its return value.

This version works correctly. It's missing type hints and the `if __name__ == "__main__":` guard — both fine for a first working version.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-first_coroutine) · [Hint 1](first_coroutine_hints.md#hint-1) · [Hint 2](first_coroutine_hints.md#hint-2) · [Solution](first_coroutine_solution.md)

## Intermediate Version

### Approach 1 — type hints and a `__main__` guard

```python
import asyncio


async def wait_and_return() -> str:
    await asyncio.sleep(1)
    return "done"


if __name__ == "__main__":
    unstarted = wait_and_return()
    print(unstarted)   # <coroutine object wait_and_return at 0x...>

    result: str = asyncio.run(wait_and_return())
    print(result)       # "done"
```
**Expected output:**
```
<coroutine object wait_and_return at 0x7f2a1c0b1a40>
done
```

**Difference from Basic:** the `-> str` type hint on `wait_and_return` documents, without reading the body, what the coroutine resolves to once it's awaited. The `if __name__ == "__main__":` guard means this file can be safely imported elsewhere (a test, another module) without the demonstration code running on import — only running when the file is executed directly. Same underlying behavior either way: calling an `async def` function builds a coroutine object, and only `await` or `asyncio.run(...)` actually runs it.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-first_coroutine) · [Hint 1](first_coroutine_hints.md#hint-1) · [Hint 2](first_coroutine_hints.md#hint-2) · [Solution](first_coroutine_solution.md)

## Advanced Version

### Approach 1 — a timeout, so a hang can't freeze the program forever

```python
import asyncio


async def wait_and_return() -> str:
    await asyncio.sleep(1)
    return "done"


async def main() -> None:
    try:
        result = await asyncio.wait_for(wait_and_return(), timeout=5)
        print(result)
    except asyncio.TimeoutError:
        print("wait_and_return took too long, giving up")


if __name__ == "__main__":
    asyncio.run(main())
```
**Expected output:**
```
done
```
And with `timeout=0.5` instead (shorter than the 1-second sleep inside `wait_and_return`):
```
wait_and_return took too long, giving up
```
`asyncio.wait_for(coro, timeout=...)` cancels the coroutine and raises `asyncio.TimeoutError` if it hasn't finished in time, instead of waiting on it forever. Notice `asyncio.run()` is called exactly once now, wrapping `main()` — every other coroutine in this file is reached with a plain `await`, never its own nested `asyncio.run()` call.

### Approach 2 — safe to call whether or not a loop is already running

```python
import asyncio


async def wait_and_return() -> str:
    await asyncio.sleep(1)
    return "done"


def run_wait_and_return() -> str:
    """Run wait_and_return() from plain, synchronous code.

    Only call this from a script's true entry point. If you're already
    inside async code (a FastAPI route, another coroutine), just
    `await wait_and_return()` directly instead of calling this at all.
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        # no loop running -- safe to start one
        return asyncio.run(wait_and_return())
    raise RuntimeError(
        "run_wait_and_return() was called from inside a running event loop; "
        "await wait_and_return() directly instead"
    )


if __name__ == "__main__":
    print(run_wait_and_return())
```
**Expected output:**
```
done
```
This version fails loudly and clearly, with a message that actually explains what to do instead, if someone reuses `run_wait_and_return()` from inside code that already has an event loop running — instead of surfacing asyncio's own less obvious `RuntimeError: asyncio.run() cannot be called from a running event loop`.

**Difference from Intermediate, and between these 2 Advanced approaches:** Intermediate's version trusts `wait_and_return()` to always finish, and trusts that `asyncio.run()` is always safe to call from wherever this code ends up. Approach 1 fixes the first assumption — a coroutine waiting on something outside your program (a network call, in every later document) needs a timeout, or a single hang can freeze everything indefinitely. Approach 2 fixes the second assumption — it turns a confusing `RuntimeError` from deep inside `asyncio` into a clear, specific message pointing at the actual fix, for the specific case of this function being reused from inside an already-async caller.

**Which one should you actually write?** For a throwaway script, Intermediate is genuinely enough. The moment this kind of function is going to be imported and reused elsewhere in the curriculum — which is exactly what happens from `async_client_conversion` onward — Approach 1's timeout is worth adding on almost anything that waits on the outside world, since "it just hangs forever" is a much worse failure than "it raised a clear timeout error after 5 seconds." Approach 2's running-loop check is worth adding specifically to small entry-point helpers you expect other files to import — not to every coroutine, just the ones meant to be a program's front door.
