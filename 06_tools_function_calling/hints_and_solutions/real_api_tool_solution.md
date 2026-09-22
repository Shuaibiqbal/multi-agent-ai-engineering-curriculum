# Real-world (a tool backed by a real API call) — Solution

> [Back to the exercise](../README.md#ex-real_api_tool) · [Hint 1](real_api_tool_hints.md#hint-1) · [Hint 2](real_api_tool_hints.md#hint-2) · [Solution](real_api_tool_solution.md)

## Basic Version

### Approach 1 — the direct way

```python
# real_api_tool_practice.py
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from http_client import request_with_retry  # your Doc02 client

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

CITY_COORDINATES = {
    "lahore": {"latitude": 31.55, "longitude": 74.34},
    "karachi": {"latitude": 24.86, "longitude": 67.01},
}

@tool
def get_weather(city: str) -> str:
    """Get the current temperature for a named city."""
    coords = CITY_COORDINATES.get(city.lower())
    if coords is None:
        return f"No coordinates on file for {city}."

    params = {
        "latitude": coords["latitude"],
        "longitude": coords["longitude"],
        "current_weather": True,
    }
    response = request_with_retry(WEATHER_URL, params=params)
    temperature = response["current_weather"]["temperature"]
    return f"Currently {temperature}°C in {city}"

model_with_tools = ChatOpenAI().bind_tools([get_weather])

response = model_with_tools.invoke("What's the weather in Lahore?")
print("Requested tool calls:", response.tool_calls)

for call in response.tool_calls:
    if call["name"] == "get_weather":
        result = get_weather.invoke(call["args"])
        print("Real result:", result)
```
**Expected output:**
```
Requested tool calls: [{'name': 'get_weather', 'args': {'city': 'Lahore'}, 'id': 'call_abc', 'type': 'tool_call'}]
Real result: Currently 34.2°C in Lahore
```

This version makes a real network call through your existing retry logic, and returns a plain text summary. It only knows 2 cities, and it doesn't catch a shape-mismatch or exhausted-retries failure — both worth fixing next.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-real_api_tool) · [Hint 1](real_api_tool_hints.md#hint-1) · [Hint 2](real_api_tool_hints.md#hint-2) · [Solution](real_api_tool_solution.md)

## Intermediate Version

### Approach 1 — params-building split out, and checked

```python
# real_api_tool_practice.py
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from http_client import request_with_retry


WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

CITY_COORDINATES = {
    "lahore": {"latitude": 31.55, "longitude": 74.34},
    "karachi": {"latitude": 24.86, "longitude": 67.01},
}


def build_weather_params(city: str) -> dict | None:
    coords = CITY_COORDINATES.get(city.lower())
    if coords is None:
        return None
    return {
        "latitude": coords["latitude"],
        "longitude": coords["longitude"],
        "current_weather": True,
    }


@tool
def get_weather(city: str) -> str:
    """Get the current temperature for a named city."""
    params = build_weather_params(city)
    if params is None:
        return f"No coordinates on file for {city}."

    response = request_with_retry(WEATHER_URL, params=params)
    temperature = response["current_weather"]["temperature"]
    return f"Currently {temperature}°C in {city}"


def get_model_with_tools() -> ChatOpenAI:
    return ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools([get_weather])


def main() -> None:
    model_with_tools = get_model_with_tools()
    response = model_with_tools.invoke("What's the weather in Lahore?")

    if not response.tool_calls:
        print("The model answered directly, without calling a tool.")
        print(response.content)
        return

    for call in response.tool_calls:
        if call["name"] == "get_weather":
            result = get_weather.invoke(call["args"])
            print(f"Called get_weather({call['args']}) -> {result}")
        else:
            print(f"Unexpected tool requested: {call['name']}")


if __name__ == "__main__":
    main()
```
**Expected output:**
```
Called get_weather({'city': 'Lahore'}) -> Currently 34.2°C in Lahore
```

**Difference from Basic:** pulling `build_weather_params()` out as its own function makes the "do we have coordinates for this city" check independently testable, without needing a real network call or a running model. Checking `response.tool_calls` before looping over it also matters here for the same reason it mattered in the Basic exercise: an obvious-looking question is still not a *guarantee* the model calls anything.

**Which one should you actually write?** Intermediate's version is enough for this exercise — the plumbing (model → tool → `request_with_retry()` → real API) working end to end is the point. Two gaps are worth naming honestly rather than fixing here: `response["current_weather"]["temperature"]` assumes the API's response shape never changes, and `CITY_COORDINATES` only actually covers the 2 cities someone typed into it even though the tool's description promises "a named city." Neither needs fixing in this exercise — a `KeyError` here is the same category of crash the next exercise (`missing_argument_handling`) deliberately teaches you to catch, and a hardcoded lookup table is a fine demo shortcut as long as you can say out loud that it's one.
