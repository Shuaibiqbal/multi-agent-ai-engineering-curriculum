# Edge cases (a missing required argument) — Solution

> [Back to the exercise](../README.md#ex-missing_argument_handling) · [Hint 1](missing_argument_handling_hints.md#hint-1) · [Hint 2](missing_argument_handling_hints.md#hint-2) · [Solution](missing_argument_handling_solution.md)

**Story — `missing_argument_practice.py`:** when a required argument is missing from the user's message (they say "what's the weather?" with no city), the model has three choices — ask a clarifying question, guess a value, or send an empty string — and *which* it does decides how your tool must defend itself. This exercise makes you watch that behavior directly, so you know whether to design for a clarifying question or a graceful default, and so a bad value (an empty city) is caught rather than sent to the API. **If not:** the Build Task's Pydantic argument models would be guessing at a problem you'd never actually watched happen.

## Solution

```python
# missing_argument_practice.py
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a named city. Requires a city name."""
    return f"Sunny in {city}"


# Sort one response into one of three real outcomes.
def classify_response(response):
    if not response.tool_calls:
        return "asked_or_answered_directly"
    city_sent = response.tool_calls[0]["args"].get("city")
    if not city_sent:
        return "called_with_empty_value"
    return "called_with_guessed_value"


# Ask the same vague prompt (no city!) 5 times and see what the model does.
model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools([get_weather])
for run_number in range(1, 6):
    response = model.invoke("what's the weather like")
    outcome = classify_response(response)
    record = {"run": run_number, "outcome": outcome}
    if outcome == "called_with_guessed_value":
        record["city_sent"] = response.tool_calls[0]["args"].get("city")
    if outcome == "asked_or_answered_directly":
        record["reply"] = response.content
    print(record)
```
**Expected output (example):**
```
{'run': 1, 'outcome': 'asked_or_answered_directly', 'reply': 'Which city?'}
{'run': 2, 'outcome': 'called_with_guessed_value', 'city_sent': 'London'}
{'run': 3, 'outcome': 'asked_or_answered_directly', 'reply': 'Specify a city?'}
{'run': 4, 'outcome': 'called_with_guessed_value', 'city_sent': 'New York'}
{'run': 5, 'outcome': 'called_with_empty_value'}
```
