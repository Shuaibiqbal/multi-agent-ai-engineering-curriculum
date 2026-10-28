# Edge cases (empty vs. missing) — Solution

> [Back to the exercise](../README.md#ex-env_edge_cases) · [Hint 1](env_edge_cases_hints.md#hint-1) · [Hint 2](env_edge_cases_hints.md#hint-2) · [Solution](env_edge_cases_solution.md)

**Where this exercise is saved:** `practice/env_config_practice.py`, under its `# Edge cases` section — the same file also holds the [Intermediate exercise](../README.md#ex-env_parsing), under an `# Intermediate` section. Run it with `cd practice && python env_config_practice.py`.

**Builds on:** your practice file of that same file — you are testing *that* loader against the two tricky `.env` states, so keep both sections in the one file. The `MissingConfigError` used below is the same class the [Build Task](../README.md#build-task-config-logging-foundation) ends up with in `practice/build_task/exceptions.py`.

**Story — `env_config_practice.py` (Edge cases section):** "missing" isn't one thing — a key that was never set and a key set to an empty string are two different states that look the same to a careless check. This exercise decides, on purpose, which one a required secret should tolerate. **If not:** `require_env()` in the Build Task would ship with an untested assumption about empty strings, and a genuinely blank API key could sail through as if it were valid.

## Solution

```python
# practice/env_config_practice.py — Edge cases section
import os

class MissingConfigError(Exception):
    pass

def require_env(key: str) -> str:
    # why: strict on purpose — an API key that's set but empty is never
    # usable, so it's treated the same as not being set at all.
    value = os.getenv(key)
    if value is None or value == "":
        raise MissingConfigError(
            f"Required environment variable is missing: {key}"
        )
    return value

# case 1: key was never set at all
# how: pop(..., None) removes it if present, does nothing if not — never raises
os.environ.pop("OPENAI_API_KEY", None)
try:
    require_env("OPENAI_API_KEY")
except MissingConfigError as e:
    print(f"Case 1 - not set at all: {e}")

# case 2: key is set, but empty
# when: simulates a .env line like "OPENAI_API_KEY=" with nothing after the "="
os.environ["OPENAI_API_KEY"] = ""
try:
    require_env("OPENAI_API_KEY")
except MissingConfigError as e:
    print(f"Case 2 - set but empty: {e}")
```
**Expected output:**
```
Case 1 - not set at all: Required environment variable is missing:
OPENAI_API_KEY
Case 2 - set but empty: Required environment variable is missing: OPENAI_API_KEY
```
