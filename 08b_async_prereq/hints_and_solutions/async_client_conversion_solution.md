# Real-world (convert a real function to async) — Solution

> [Back to the exercise](../README.md#ex-async_client_conversion) · [Hint 1](async_client_conversion_hints.md#hint-1) · [Hint 2](async_client_conversion_hints.md#hint-2) · [Solution](async_client_conversion_solution.md)

**Story — `async_client_conversion_practice.py`:** this is the exercise where an async prerequisite becomes a real, reusable function — the exact `ask()` shape gets imported into a Doc12 FastAPI route later, unchanged. **If not:** Doc12 would be the first place you ever had to write an async OpenAI call that's actually safe to reuse, with no smaller version to trust.

## Solution

```python
# async_client_conversion_practice.py
from openai import AsyncOpenAI
import asyncio

client = AsyncOpenAI()

async def ask(question):
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}],
    )
    return response.choices[0].message.content


# ask is a coroutine (it uses await), so asyncio.run() is what runs it.
answer = asyncio.run(ask("What is 2 + 2?"))
print(answer)
```
**Expected output:**
```
2 + 2 equals 4.
```
