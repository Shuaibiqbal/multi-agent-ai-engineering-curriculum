# Intermediate (feel the speed difference) — Solution

> [Back to the exercise](../README.md#ex-gather_speed) · [Hint 1](gather_speed_hints.md#hint-1) · [Hint 2](gather_speed_hints.md#hint-2) · [Solution](gather_speed_solution.md)

**Story — `gather_practice.py`:** reading "concurrent is faster than sequential" is not the same as timing 6 seconds against 2 seconds yourself, on the same 3 tasks — this is the exercise that turns that claim into something you measured. **If not:** every later use of `asyncio.gather` in this curriculum would rest on a speedup you took on faith instead of one you watched happen.

## Solution

```python
# gather_practice.py
import asyncio
import time

async def f1() -> str:
    await asyncio.sleep(2)
    return "f1 done"

async def f2() -> str:
    await asyncio.sleep(2)
    return "f2 done"

async def f3() -> str:
    await asyncio.sleep(2)
    return "f3 done"

async def run_sequential() -> None:
    start = time.perf_counter()
    await f1()
    await f2()
    await f3()
    print("sequential:", time.perf_counter() - start)

async def run_parallel() -> None:
    start = time.perf_counter()
    await asyncio.gather(f1(), f2(), f3())
    print("parallel:", time.perf_counter() - start)

if __name__ == "__main__":
    asyncio.run(run_sequential())
    asyncio.run(run_parallel())
```
**Expected output:**
```
sequential: 6.01
parallel: 2.01
```
