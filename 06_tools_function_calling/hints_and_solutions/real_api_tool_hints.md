# Real-world (a tool backed by a real API call) — Hints

> [Back to the exercise](../README.md#ex-real_api_tool) · [Hint 1](real_api_tool_hints.md#hint-1) · [Hint 2](real_api_tool_hints.md#hint-2) · [Solution](real_api_tool_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried. Each hint builds toward the full solution.

- [Hint 1 — The idea, and the exact pieces](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

## Hint 1 — The idea, and the exact pieces {: #hint-1 }

Doc02's `request_with_retry()` already handles the messy parts (timeouts, transient failures) — don't rewrite that logic inside the tool function. Instead, call it *from* the tool function, and let the `@tool` decorator wrap the whole thing.

Keep the argument shape small and typed (a single typed parameter like `city: str` is fine to start) — the model needs to know exactly what to send, and Doc02's client needs a real URL built from that argument.

The tool function should stay thin: build the request URL/params, call `request_with_retry("GET", url, params=params)` — Doc02's signature takes the HTTP method first — and return the one or two fields the model actually needs, not the whole raw JSON blob. In Basic, let a real failure raise, so you see what an unhandled tool error looks like once. In Intermediate, catch Doc02's `TransientHTTPError` and `PermanentHTTPError` by name and return `f"Error: ..."` instead.

Write out, in plain words, the full call chain: model decides to call the tool → your tool function runs → it calls `request_with_retry()` → that makes the actual HTTP call → the result flows back up through all three layers.

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

One piece to get you unstuck — the shape of the params dict and the return value:
```python
# real_api_tool_practice.py
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

CITY_COORDINATES = {
    "lahore": {"latitude": 31.55, "longitude": 74.34},
    "karachi": {"latitude": 24.86, "longitude": 67.01},
}

def get_weather(city: str) -> str:
    coords = CITY_COORDINATES.get(city.lower())
    if coords is None:
        return f"No coordinates on file for {city}."
    params = {
        "latitude": coords["latitude"],
        "longitude": coords["longitude"],
        "current_weather": True,
    }
    # TODO: call request_with_retry("GET", WEATHER_URL, params=params),
    # pull out
    # ["current_weather"]["temperature"], and return a text summary.
```
Finish the `TODO` yourself, wire it up to a model with `@tool` and `bind_tools`, then compare against the [Solution](real_api_tool_solution.md).

Full solution: [Show me the solution](real_api_tool_solution.md)
