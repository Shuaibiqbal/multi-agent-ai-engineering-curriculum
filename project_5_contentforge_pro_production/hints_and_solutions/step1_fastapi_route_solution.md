# Step 1 — ContentForge, Reachable Over HTTP for the First Time — Solution

> [Back to this step](../READING_README.md#step-1-contentforge-reachable-over-http-for-the-first-time) · [Hint 1](step1_fastapi_route_hints.md#hint-1) · [Hint 2](step1_fastapi_route_hints.md#hint-2) · [Solution](step1_fastapi_route_solution.md)

**Story — Step 1:** Project 4 works, but only for someone sitting at the terminal. This step gives it a front door: `POST /run-task` takes a topic as JSON and returns the team's article. The five agents don't change at all — the API calls them through **one** function, `run_pipeline()`. **If not:** every caller would need Python, your code and your key on their own machine.

After this step the project runs as a web API: `uvicorn src.api.main:app --reload`, then `/docs` in the browser. Project 4's files (copied in during Setup) don't change.

## Solution — one door into the team, typed shapes, 400/500, and tests with a faked team

**Story — `pipeline.py`:** the **one** function that runs Project 4's team and turns its final state into plain values: the article, whether it was accepted, why the run stopped, and one text line per routing step. **If not:** the route would reach into the graph's state itself — and a test couldn't swap the team for a fake in one place.

```python
# src/pipeline.py
# The one door into Project 4's team. run_pipeline(topic) builds and runs
# the graph and returns plain values (article, accepted, reason, steps);
# steps_from_log() turns the routing log into one text line per step.
from src.graph import build_graph
from src.state import start_state

def steps_from_log(routing_log: list[dict]) -> list[str]:
    steps = []
    for entry in routing_log:
        steps.append(entry["step"] + ": " + entry["reason"])
    return steps

def run_pipeline(topic: str) -> dict:
    graph = build_graph()
    result = graph.invoke(start_state(topic))
    last_entry = result["routing_log"][-1]
    return {
        "article": result["draft"],
        "accepted": result["accepted"],
        "reason": last_entry["reason"],
        "steps": steps_from_log(result["routing_log"]),
    }
```

**Story — `api/schemas.py`:** the API's contract, written once (Doc12's `chat_schemas.py`). `Field(min_length=1, max_length=200)` rejects an empty or huge topic with a 422 before any model is called. **If not:** a 5,000-word "topic" would be sent to five agents, and a typo in a reply field would only be found by the client.

```python
# src/api/schemas.py
# The API's request/reply shapes. TaskRequest rejects an empty or huge
# topic with a 422 before the route runs; TaskResponse is the checked reply.
from pydantic import BaseModel, Field

class TaskRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=200)

class TaskResponse(BaseModel):
    accepted: bool
    reason: str
    article: str
```

**Story — `api/routes.py`:** the routes on an `APIRouter` (Doc12's `health_routes.py`). `POST /run-task` is Doc12's `chat_route`: our own 400 for a blank topic, and any crash turned into a plain 500 while `logger.exception()` keeps the real traceback on the server. (Also create an empty `api/__init__.py`.) **If not:** a client could see file paths from a traceback, and nobody on the server would know why a run failed.

```python
# src/api/routes.py
# The API routes on an APIRouter: GET /health and POST /run-task. The POST
# route rejects a blank topic with 400 and turns any crash into a plain 500,
# keeping the real traceback on the server with logger.exception().
from fastapi import APIRouter, HTTPException

from src.api.schemas import TaskRequest, TaskResponse
from src.pipeline import run_pipeline
from src.utils.logger import get_logger

router = APIRouter()

INTERNAL_ERROR = "Internal error. Please try again later."

@router.get("/health")
def health() -> dict:
    return {"status": "ok"}

@router.post("/run-task", response_model=TaskResponse)
def run_task(request: TaskRequest) -> TaskResponse:
    logger = get_logger(__name__)
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="topic cannot be empty")

    try:
        outcome = run_pipeline(request.topic)
    except Exception:
        logger.exception("run-task failed")
        raise HTTPException(status_code=500, detail=INTERNAL_ERROR)

    logger.info(f"run-task done: {outcome['reason']}")
    return TaskResponse(
        accepted=outcome["accepted"],
        reason=outcome["reason"],
        article=outcome["article"],
    )
```

**Story — `api/main.py`:** the one file uvicorn starts. `load_config()` runs first — it reads `.env` (the agents need the key) and stops the app at once if `OPENAI_API_KEY` is missing. **If not:** the server would start "fine" and fail on every real request.

```python
# src/api/main.py
# The app uvicorn starts. load_config() runs first, so a missing
# OPENAI_API_KEY stops the server at startup, not on the first request.
from fastapi import FastAPI

from src.api.routes import router
from src.config import load_config

load_config()

app = FastAPI(title="ContentForge Pro")
app.include_router(router)
```

**Story — `tests/api/test_routes.py`:** API tests with pytest and `TestClient` (Doc12, Doc13), with the team **faked**: `monkeypatch` swaps `routes.run_pipeline` for a function that returns a fixed answer, or crashes on purpose (Doc13's integration-test pattern). No model calls, no cost, the same result every run. **If not:** every API test would run five real agents — slow, paid, and never the same twice.

```python
# tests/api/test_routes.py
# The API's own behavior — status codes and replies — with Project 4's
# team FAKED: no model calls, no cost, same every time.
# Run from the repo root: pytest tests/api -v
# The app still refuses to start without OPENAI_API_KEY — any value
# works here, because no real model is ever called.
from fastapi.testclient import TestClient

from src.api import routes
from src.api.main import app

client = TestClient(app)

def fake_run_pipeline(topic: str) -> dict:
    return {
        "article": "E-Bikes Explained\n\nUp to 100 km. [battery-review]",
        "accepted": True,
        "reason": "reviewer accepted the draft",
        "steps": [
            "research_agent: no research yet",
            "END: reviewer accepted the draft",
        ],
    }

def broken_run_pipeline(topic: str) -> dict:
    raise RuntimeError("simulated internal failure")

def use_fake_team(monkeypatch, fake) -> None:
    monkeypatch.setattr(routes, "run_pipeline", fake)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_valid_request_is_answered(monkeypatch):
    use_fake_team(monkeypatch, fake_run_pipeline)
    response = client.post("/run-task", json={"topic": "electric bikes"})
    assert response.status_code == 200
    body = response.json()
    assert body["accepted"] is True
    assert "[battery-review]" in body["article"]

def test_bad_body_is_422(monkeypatch):
    use_fake_team(monkeypatch, fake_run_pipeline)
    response = client.post("/run-task", json={})
    assert response.status_code == 422

def test_blank_topic_is_400(monkeypatch):
    use_fake_team(monkeypatch, fake_run_pipeline)
    response = client.post("/run-task", json={"topic": "   "})
    assert response.status_code == 400
    assert response.json() == {"detail": "topic cannot be empty"}

def test_internal_error_is_a_plain_500(monkeypatch):
    use_fake_team(monkeypatch, broken_run_pipeline)
    response = client.post("/run-task", json={"topic": "electric bikes"})
    assert response.status_code == 500
    expected = {"detail": "Internal error. Please try again later."}
    assert response.json() == expected
```

**Run it** (from the repo root):

```bash
pytest tests/api -v
uvicorn src.api.main:app --reload
```

```
tests/api/test_routes.py::test_health PASSED
tests/api/test_routes.py::test_valid_request_is_answered PASSED
tests/api/test_routes.py::test_bad_body_is_422 PASSED
tests/api/test_routes.py::test_blank_topic_is_400 PASSED
tests/api/test_routes.py::test_internal_error_is_a_plain_500 PASSED
```

Project 4's own tests stay exactly as Project 4 wrote them — plain OK/WRONG scripts you run with `python -m tests.unit.test_config` — so point pytest at `tests/api` only. New tests in this project use pytest (Doc13); Project 4's are never rewritten. Then send a request to the running server from `/docs`:

```
{"accepted":true,"reason":"reviewer accepted the draft",
 "article":"E-Bikes: How Far, How Fast ... [battery-review] ..."}
```

(Really one line — shown wrapped to fit the page. The article varies from run to run.) Try `{"topic": "deep sea mining"}` too: `"accepted":false`, `"reason":"research found no facts for this topic"` and an empty article — the team's honest stop, now visible to the client.
