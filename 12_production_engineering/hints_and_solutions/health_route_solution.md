# Basic (your first FastAPI route) — Solution

> [Back to the exercise](../README.md#ex-health_route) · [Hint 1](health_route_hints.md#hint-1) · [Hint 2](health_route_hints.md#hint-2) · [Solution](health_route_solution.md)

**Story — `health_route_practice.py`:** every real service needs one tiny route that just answers "are you up?" — and because it's the smallest possible FastAPI app, it's the right place to learn `FastAPI()`, the `@app.get(...)` decorator, and `uvicorn` itself, before any real logic is in the picture at all. **If not:** your first FastAPI route would be the Build Task's `/run-task`, with a database and an agent sitting behind it, and any mistake in the basic setup would be buried under everything else.

The solution below runs from inside `practice/` with `uvicorn health_route_practice:app --reload`, and is checked with `curl localhost:8000/health`.

## Solution

**Story:** a bare dict returned from a route can silently change shape — a typo like `"stauts"` instead of `"status"` — and nobody notices until a client breaks in production. Declaring a `response_model` makes FastAPI validate every reply against it and document the exact shape automatically. **If not:** the Build Task's replies would have no written contract at all, and a wrong field name would only ever be discovered by the client failing.

```python
# practice/health_route_practice.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class HealthResponse(BaseModel):
    # why: the reply's shape is written down once, in one place
    status: str

# how: FastAPI checks the return value against HealthResponse
@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Liveness check: is the process up and able to answer at all."""
    return HealthResponse(status="ok")
```
**Expected output:**
```
{"status":"ok"}
```
The JSON reply looks identical to Basic's, but `http://localhost:8000/docs` now shows a documented `HealthResponse` schema for this route, and FastAPI would reject (loudly, with a server-side error) any code path that tried to return something that doesn't match `HealthResponse`.
