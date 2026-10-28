# Edge cases (proving gather actually waits) — Solution

> [Back to the exercise](../README.md#ex-gather_waits_for_slowest) · [Hint 1](gather_waits_for_slowest_hints.md#hint-1) · [Hint 2](gather_waits_for_slowest_hints.md#hint-2) · [Solution](gather_waits_for_slowest_solution.md)

**Story — `gather_practice.py` (Edge cases section):** it's easy to assume `gather` hands back results as soon as the first task finishes — this exercise proves, with a real timestamp, that it doesn't. **If not:** the first time a slow straggler silently doubled an agent turn's latency, you'd have no smaller example to recognize the cause from.

## Solution

```python
# gather_practice.py — Edge cases section
import asyncio
import time

async def fast_task() -> str:
    await asyncio.sleep(0.1)
    print(f"fast_task finished at {time.perf_counter():.2f}")
    return "fast"

async def slow_task() -> str:
    await asyncio.sleep(5)
    print(f"slow_task finished at {time.perf_counter():.2f}")
    return "slow"

async def main() -> None:
    start = time.perf_counter()
    print(f"starting at {start:.2f}")

    results = await asyncio.gather(fast_task(), slow_task())

    print(f"gather returned at {time.perf_counter():.2f}")
    print(f"results: {results}")

if __name__ == "__main__":
    asyncio.run(main())
```
**Expected output:**
```
starting at 1000.00
fast_task finished at 1000.10
slow_task finished at 1005.00
gather returned at 1005.00
results: ['fast', 'slow']
```
