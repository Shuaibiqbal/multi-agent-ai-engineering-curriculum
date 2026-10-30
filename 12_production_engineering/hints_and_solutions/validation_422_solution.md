# Edge cases (a request that fails validation) — Solution

> [Back to the exercise](../README.md#ex-validation_422) · [Hint 1](validation_422_hints.md#hint-1) · [Hint 2](validation_422_hints.md#hint-2) · [Solution](validation_422_solution.md)

**Story — `sqlite_persistence_practice.py` (Edge cases section):** "bad input never touches the database" is an easy claim to believe and a claim rarely actually checked. This section proves it by counting real rows before and after a rejected request, then looks at the one case Pydantic's automatic validation can't cover at all — a *valid* request that fails partway through, between two separate writes. **If not:** the Build Task's "bad request body → 422, no database write" test case, and its started → completed/failed status transitions, would rest entirely on an untested assumption.

The solution below assume your `sqlite_persistence` server is running on `localhost:8000` (or use `TestClient`, as noted).

## Solution

**Story:** two `curl` outputs checked by eye prove the behavior once, today, and only today. A script with real `assert` statements proves the same thing every single time you run it, and stops loudly with a clear failure the exact day it breaks. **If not:** a future change that accidentally starts writing to the database before checking input would go completely unnoticed.

```python
# practice/sqlite_persistence_practice.py — Edge cases section
import sqlite3
import requests

conn = sqlite3.connect("runs.db")

def row_count() -> int:
    return conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]

before = row_count()

url = "http://localhost:8000/chat"
response = requests.post(url, json={})
# why: assert stops the script with this message if the check fails
assert response.status_code == 422, f"expected 422, got {response.status_code}"

after = row_count()
assert before == after, f"row count changed: {before} -> {after}"

print("422 confirmed, no row written")
print(response.json())
```
**Expected output (the second line is shown wrapped onto 2 lines just to fit the page — really one line of output):**
```
422 confirmed, no row written
{'detail': [{'type': 'missing', 'loc': ['body', 'message'],
  'msg': 'Field required', 'input': {}}]}
```
