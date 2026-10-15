# Step 4 — Production Wrap (optional) — Hints

> [Back to the step](../READING_README.md#step-4-production-wrap-optional) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](step4_production_wrap_solution.md)

This step is honestly closer to "go redo Project 5" than to anything new.

- [Hint 1 — This is Project 5, not a new design](#hint-1)
- [Hint 2 — The one eval that actually matters here](#hint-2)

## Hint 1 — This is Project 5, not a new design {: #hint-1 }

You already built this layer in Project 5 (ContentForge). Reuse it almost unchanged:

- `src/pipeline.py` — `review_diff(model, collection, diff)`: build the graph once, run it, return the compiled review (plus which reviewers ran).
- `src/api/` — `schemas.py` (`ReviewRequest`/`ReviewResponse`), `routes.py` (`POST /review`, `GET /health`), `main.py` (`FastAPI` app).
- `Dockerfile` — the same slim-python image from Project 5.

The only real change from Project 5 is *what the pipeline does inside* — a 4-agent review instead of a writer/reviewer loop. The wrapper is identical.

## Hint 2 — The one eval that actually matters here {: #hint-2 }

A suite that only checks each reviewer's accuracy could pass even if routing were completely broken — every reviewer running on every diff would still produce correct findings. So the eval that matters checks **routing**:

```
docs-only diff   -> "security" NOT in reviewers_run
code-with-secret -> "security" IN reviewers_run AND review mentions the secret
```

That's the point of the whole project — the routing — so that's what the eval guards. Test the API with the pipeline faked (monkeypatch `review_diff`) so it runs with no model and no key. The whole file set is in the [Solution](step4_production_wrap_solution.md).
