# Basic (a simple version log) — Solution

> [Back to the exercise](../README.md#ex-version_log) · [Hint 1](version_log_hints.md#hint-1) · [Hint 2](version_log_hints.md#hint-2) · [Solution](version_log_solution.md)

**Story — `version_log_practice.py`:** a release gate needs something real to compare a new version against, and a question like "which prompt was actually live last Tuesday?" needs a genuine historical record to answer. This log is exactly that record — every version saved with its full text and timestamp, and never overwritten by a later save. **If not:** the Build Task's gate would have nothing real to check against, and a bad answer in production could never be traced back to the exact prompt that produced it.

All examples below use a stand-in for Doc13's real test suite, `run_eval_suite(prompt_text)`, so the script runs on its own. In your real Project 5 code, swap it for your actual Doc13 suite import.

## Solution

**Story:** a log file you simply rewrite from scratch on every run isn't actually a history at all — it's just the latest snapshot. The correct pattern is load the existing file first, then append the new entry to it, and stop loudly with a clear error if the file turns out damaged rather than silently treating it as empty. **If not:** a half-written or corrupted file would quietly become treated as an empty list, and the very next save would wipe out every previously saved version.

```python
# version_log_practice.py
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

class VersionLogCorruptError(Exception):
    pass

def run_eval_suite(prompt_text: str) -> dict:
    if "politely" in prompt_text:
        return {"score": 1.0}
    return {"score": 0.6}

def load_versions(path: str) -> list[dict]:
    if not Path(path).exists():
        return []
    with open(path) as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # why: a damaged file must stop the save — silently treating
            # it as [] would wipe the whole history on the next write
            raise VersionLogCorruptError(
                f"{path} is not valid JSON — restore it before saving, "
                "or its history will be lost"
            )

def save_version(name: str, prompt_text: str, path: str) -> None:
    # how: load what's already there first, then append — never
    # rebuild the file from scratch
    versions = load_versions(path)
    versions.append({
        "version_name": name,
        "prompt_text": prompt_text,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    with open(path, "w") as f:
        json.dump(versions, f, indent=2)
    logger.info(f"Saved version {name} ({len(versions)} in log)")

save_version("v1", "Answer the customer's question.", "versions.json")
save_version(
    "v2",
    "Answer the customer's question politely and cite the source.",
    "versions.json",
)

for version in load_versions("versions.json"):
    result = run_eval_suite(version["prompt_text"])
    print(version["version_name"], result["score"])
```
**Expected output:**
```
Saved version v1 (1 in log)
Saved version v2 (2 in log)
v1 0.6
v2 1.0
```
(the log lines show only the message, because this handler has no formatter)

And if `versions.json` is damaged — say, half-written when the script was stopped — `save_version` now stops instead of overwriting it. The last line of the traceback:
```
__main__.VersionLogCorruptError: versions.json is not valid JSON — restore it
before saving, or its history will be lost
```

**Revision from Doc01 (Intermediate):** two habits come back here. First, a named logger, `logging.getLogger(__name__)`, instead of the root logger — so these lines say which module they came from once this code is imported by the release gate. Second, catching one *specific* exception, `json.JSONDecodeError`, and raising a named error with a clear message. This matters a lot here: `save_version` loads, then rewrites the whole file. If a broken file quietly became `[]`, the next save would wipe the whole version history. The named error stops that before any damage is done.
