# Step 3 — Scaling to 3 Tools With a Hard Step Limit and Failure Recovery — Hints

> [Back to this step](../READING_README.md#step-3-scaling-to-3-tools-with-a-hard-step-limit-and-failure-recovery) · [Hint 1](step3_multi_tool_limits_hints.md#hint-1) · [Hint 2](step3_multi_tool_limits_hints.md#hint-2) · [Solution](step3_multi_tool_limits_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've really tried. Each hint starts with the plain idea, then shows the shape of the real code.

- [Hint 1 — Two new tools, and what can go wrong](#hint-1)
- [Hint 2 — The plan, and what to change](#hint-2)

<hr class="page-break">

> [Back to this step](../READING_README.md#step-3-scaling-to-3-tools-with-a-hard-step-limit-and-failure-recovery) · [Hint 1](step3_multi_tool_limits_hints.md#hint-1) · [Hint 2](step3_multi_tool_limits_hints.md#hint-2) · [Solution](step3_multi_tool_limits_solution.md)

## Hint 1 — Two new tools, and what can go wrong {: #hint-1 }

Two new tools, each in its own file:

- `tools/weather.py` — Doc06's Open-Meteo tool. It needs coordinates, so keep Doc06's `CITY_COORDINATES` dict and `build_weather_params(city)`. Call Doc02's `request_with_retry("GET", WEATHER_URL, params=params)` — bring Doc02's client in as `utils/http_client.py`, and its two errors into `exceptions.py`.
- `tools/docs_search.py` — a small dict of policy texts (refund, shipping, warranty); return the one whose key appears in the query.

Make the search **fail on its first call** with Doc07's `FlakyToolState` (a class with `call_count`): add 1 on each call, and `raise ConnectionError(...)` when it's 1. Now every run proves recovery.

With 3 tools, the model chooses by description. Say in each docstring when *not* to use the tool.

The Worker needs almost nothing new — that's the point of building its full shape in Step 2:

- `run_tool()` already catches any exception, so the failing search becomes an `Error: ...` observation and the model can retry it;
- the step log already records the failure (`error` set) and the retry;
- the limit already stops a model that keeps retrying.

So in `agents/worker.py` you only import the two tools and add them to `ALL_TOOLS`.

<hr class="page-break">

> [Back to this step](../READING_README.md#step-3-scaling-to-3-tools-with-a-hard-step-limit-and-failure-recovery) · [Hint 1](step3_multi_tool_limits_hints.md#hint-1) · [Hint 2](step3_multi_tool_limits_hints.md#hint-2) · [Solution](step3_multi_tool_limits_solution.md)

## Hint 2 — The plan, and what to change {: #hint-2 }

```
exceptions.py      + TransientHTTPError, PermanentHTTPError  (Doc02)
utils/http_client  + request_with_retry()                    (Doc02)
tools/weather.py   + get_weather, build_weather_params
tools/docs_search  + search_docs, FlakyToolState, search_state
agents/worker.py   ALL_TOOLS = [get_weather,
                                celsius_to_fahrenheit, search_docs]
prompts/worker.txt rewritten for 3 tools
```

`main.py` doesn't change.

Rewrite `prompts/worker.txt`: which questions need which tool (weather, conversions, company policy), "you may retry a failed tool once", and "answer only from what the tools returned".

Tests:

- `test_tools.py` — add the weather params for a known and an unknown city, and the fail-then-work search (set `search_state.call_count = 0` first).
- `test_live_agents.py` — add a weather question that must use `get_weather`, and the refund question, where the step log must show one failed and one successful search.

Full solution: [Show me the solution](step3_multi_tool_limits_solution.md)
