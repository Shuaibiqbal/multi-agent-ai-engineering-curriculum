# Basic (your first real API call) — Solution

> [Back to the exercise](../README.md#ex-api_first_call) · [Hint 1](api_first_call_hints.md#hint-1) · [Hint 2](api_first_call_hints.md#hint-2) · [Solution](api_first_call_solution.md)

## Basic Version

### Approach 1 — the direct way

```python
# api_first_call_practice.py
import requests

response = requests.get("https://api.github.com")
print(response.status_code)
print(response.json())

try:
    requests.get("htp://broken")
except Exception as e:
    print("Caught it:", type(e).__name__)
```
**Expected output:**
```
200
{'current_user_url': 'https://api.github.com/user', ...}
Caught it: MissingSchema
```
This works. It catches `Exception` broadly rather than the specific `requests` exception class, which is fine for a first pass, but it would also swallow completely unrelated bugs in the same block if you added more code later.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-api_first_call) · [Hint 1](api_first_call_hints.md#hint-1) · [Hint 2](api_first_call_hints.md#hint-2) · [Solution](api_first_call_solution.md)

## Intermediate Version

### Approach 1 — the specific exception, wrapped in `main()`

```python
# api_first_call_practice.py
import requests


def main() -> None:
    response = requests.get("https://api.github.com")
    print(f"status: {response.status_code}")
    print(f"body: {response.json()}")

    try:
        requests.get("htp://broken")
    except requests.exceptions.RequestException as e:
        print(f"Caught a client-side request error: {type(e).__name__} - {e}")


if __name__ == "__main__":
    main()
```
**Expected output:**
```
status: 200
body: {'current_user_url': 'https://api.github.com/user', ...}
Caught a client-side request error: MissingSchema - Invalid URL 'htp://broken': No scheme supplied. Perhaps you meant https://htp://broken?
```

**Difference from Basic:** catching `requests.exceptions.RequestException` specifically (instead of bare `Exception`) means this block only swallows problems that are actually about making the request — a bug anywhere else in a bigger `try` block would still surface normally, instead of being silently caught here too. Wrapping the script in `main()` also matches the pattern from Doc01 — small habit, but it's the one you'll want once this script grows past a few lines.

**Which one should you actually write?** Intermediate's plain `try/except RequestException` is enough for exploring an API. This document's Build Task takes status-code classification (which failures to retry, which to fail on immediately) much further — that's the whole point of `http_client.py`, covered in its own exercises below, not something to over-build here.
