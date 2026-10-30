# Basic (your first real API call) — Solution

> [Back to the exercise](../README.md#ex-api_first_call) · [Hint 1](api_first_call_hints.md#hint-1) · [Hint 2](api_first_call_hints.md#hint-2) · [Solution](api_first_call_solution.md)

**Story — `api_first_call_practice.py`:** every later exercise in this document assumes you've already seen, once, that a bad URL and a bad response are two completely different kinds of failure: a bad URL raises a `requests` exception *before any server is reached*, while a 4xx/5xx is a real response that came back and you inspect with `.status_code`. This script is where you see that split for the first time, with nothing else going on. **If not:** the first time you'd meet that distinction would be buried inside a retry loop or an error-classification function, where it's much harder to isolate what's actually different about the two failure types.

## Solution

```python
# api_first_call_practice.py
import requests

# A real call/response round trip, before anything else builds on it.
response = requests.get("https://api.github.com")
print(f"status: {response.status_code}")   # the transport succeeded
print(f"body: {response.json()}")   # parsing the body is a separate step

# A malformed URL fails before any network call happens — a client-side
# mistake, not a server response.
try:
    requests.get("htp://broken")
except requests.exceptions.RequestException as e:
    # catch only requests' own errors, not every possible Exception
    print(f"Caught a client-side request error: {type(e).__name__} - {e}")
```
**Expected output:**
```
status: 200
body: {'current_user_url': 'https://api.github.com/user', ...}
Caught a client-side request error: MissingSchema - Invalid URL
'htp://broken': No scheme supplied. Perhaps you meant https://htp://broken?
```
(The last line is shown wrapped onto 2 lines just to fit the page — really one line of output.)
