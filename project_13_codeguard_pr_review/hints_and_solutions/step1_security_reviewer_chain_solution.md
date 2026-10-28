# Step 1 — The Security Reviewer on a Diff — Solution

> [Back to the step](../READING_README.md#step-1-the-security-reviewer-on-a-diff) · [Hint 1](step1_security_reviewer_chain_hints.md#hint-1) · [Hint 2](step1_security_reviewer_chain_hints.md#hint-2)

**Story:** the smallest piece — a Security reviewer working on a diff, proven on a planted *and* a clean example before anything else exists. **If not:** a reviewer only ever tested on bad input will happily flag good code.

## Setup files

`requirements.txt`: `openai`, `langchain-openai`, `langgraph`, `chromadb`, `python-dotenv`, `pydantic`.
`.env.example`: `OPENAI_API_KEY=sk-your-key-here` / `LOG_LEVEL=INFO`. `.gitignore`: `.env`, `.venv/`, `__pycache__/`, `*.pyc`, `chroma_db/`. Every folder under `src/` gets an empty `__init__.py`. `LICENSE` is the MIT text.

## Settings, errors, logging

```python
# src/exceptions.py
class MissingConfigError(Exception):
    """A required setting is missing from the environment."""
    pass
```

```python
# src/config.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv
from src.exceptions import MissingConfigError

@dataclass
class Config:
    openai_api_key: str
    log_level: str

def require_env(key: str) -> str:
    value = os.getenv(key)
    if value is None or value == "":
        raise MissingConfigError(
            f"Required environment variable is missing: {key}"
        )
    return value

def load_config() -> Config:
    load_dotenv()
    return Config(
        openai_api_key=require_env("OPENAI_API_KEY"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
```

```python
# src/utils/logger.py
import logging
import os

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        level_name = os.getenv("LOG_LEVEL", "INFO")
        level = getattr(logging, level_name.upper(), logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(level)
        log_format = "%(asctime)s %(name)s %(levelname)s %(message)s"
        handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger
```

```python
# src/models/llm.py
from langchain_openai import ChatOpenAI

from src.config import Config

def get_model(config: Config) -> ChatOpenAI:
    return ChatOpenAI(
        model="gpt-4o-mini", temperature=0, api_key=config.openai_api_key
    )
```

## The finding shape and the diff parser

```python
# src/schemas.py
# One review finding. severity is high/medium/low; category is which reviewer
# raised it; message is the human-readable issue.
from pydantic import BaseModel

class Finding(BaseModel):
    severity: str
    category: str
    message: str
```

```python
# src/diff.py
# Parse a unified diff into the ADDED lines per file (like Doc08's chunking:
# only look at what actually changed), and categorize a file by extension.
def parse_diff(text: str) -> list:
    files = []
    current = None
    for line in text.splitlines():
        if line.startswith("+++ b/"):
            current = {"path": line[len("+++ b/"):], "added": []}
            files.append(current)
        elif line.startswith("+") and not line.startswith("+++"):
            if current is not None:
                current["added"].append(line[1:])
    return files

def categorize(path: str) -> str:
    if path.endswith((".md", ".rst", ".txt")):
        return "docs"
    if path.endswith((".yaml", ".yml", ".json", ".toml", ".ini", ".cfg")):
        return "config"
    return "code"
```

## The Security reviewer

**Story:** a deterministic scanner is the trustworthy core — it looks only at the added lines for secret and unsafe patterns, and returns `Finding`s. (You can add an LLM pass for judgment calls, but the scanner is what you can actually test.) **If not:** a purely prompted reviewer is non-deterministic and hard to pin down on a clean diff.

```python
# src/agents/security_reviewer.py
# Scan the diff's ADDED lines for hardcoded secrets and unsafe patterns.
# Deterministic, so it's testable; a reviewer tested only on bad input would
# flag good code, so test a clean diff too.
import re

from src.schemas import Finding

SECRET_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "hardcoded AWS access key"),
    (r"(?i)(password|passwd|secret|api[_-]?key)\s*=\s*['\"][^'\"]{6,}['\"]",
     "hardcoded secret/credential"),
]
UNSAFE_PATTERNS = [
    (r"\beval\(", "use of eval() on untrusted input"),
    (r"subprocess\.\w+\([^)]*shell\s*=\s*True", "subprocess with shell=True"),
    (r"pickle\.loads\(", "unsafe pickle.loads()"),
]

def run_security(files) -> list:
    findings = []
    for one_file in files:
        for line in one_file["added"]:
            for pattern, message in SECRET_PATTERNS:
                if re.search(pattern, line):
                    findings.append(Finding(
                        severity="high", category="security",
                        message=f"{one_file['path']}: {message}",
                    ))
            for pattern, message in UNSAFE_PATTERNS:
                if re.search(pattern, line):
                    findings.append(Finding(
                        severity="medium", category="security",
                        message=f"{one_file['path']}: {message}",
                    ))
    return findings
```

## main.py (standalone)

```python
# main.py  (Step 1 version)
from src.agents.security_reviewer import run_security
from src.diff import parse_diff

DIRTY = """--- a/app.py
+++ b/app.py
+api_key = "SUPERsecret12345"
+result = eval(user_input)
+x = 1
"""
CLEAN = """--- a/app.py
+++ b/app.py
+total = price * quantity
+return total
"""

def main():
    for label, diff in [("dirty", DIRTY), ("clean", CLEAN)]:
        findings = run_security(parse_diff(diff))
        print(f"\n=== {label} ===")
        if not findings:
            print("  no security findings")
        for finding in findings:
            print(f"  [{finding.severity}] {finding.message}")

if __name__ == "__main__":
    main()
```

## The tests

```python
# tests/unit/test_config.py
# Run from the repo root: python -m tests.unit.test_config
import os

from src.config import load_config, require_env
from src.exceptions import MissingConfigError

TEST_SETTING = "CODEGUARD_TEST_SETTING"

def test_missing_setting() -> None:
    os.environ.pop(TEST_SETTING, None)
    result = "WRONG"
    try:
        require_env(TEST_SETTING)
    except MissingConfigError:
        result = "OK"
    print(f"case 1 (missing setting) -> {result}")

def test_empty_setting() -> None:
    os.environ[TEST_SETTING] = ""
    result = "WRONG"
    try:
        require_env(TEST_SETTING)
    except MissingConfigError:
        result = "OK"
    print(f"case 2 (empty setting)   -> {result}")

def test_config_loads() -> None:
    os.environ["OPENAI_API_KEY"] = "sk-test-123"
    config = load_config()
    result = "OK"
    if config.openai_api_key != "sk-test-123":
        result = "WRONG"
    print(f"case 3 (config loads)    -> {result}")

if __name__ == "__main__":
    test_missing_setting()
    test_empty_setting()
    test_config_loads()
```

```python
# tests/unit/test_diff.py
# Run from the repo root: python -m tests.unit.test_diff
from src.diff import categorize, parse_diff

DIFF = """--- a/app.py
+++ b/app.py
 unchanged line
+added line one
+added line two
-removed line
"""

def test_parses_added_lines_only() -> None:
    files = parse_diff(DIFF)
    result = "OK"
    if len(files) != 1 or files[0]["path"] != "app.py":
        result = "WRONG"
    if files[0]["added"] != ["added line one", "added line two"]:
        result = "WRONG"
    print(f"case 1 (added lines only) -> {result}")

def test_categorize() -> None:
    result = "OK"
    if categorize("README.md") != "docs":
        result = "WRONG"
    if categorize("config.yaml") != "config":
        result = "WRONG"
    if categorize("app.py") != "code":
        result = "WRONG"
    print(f"case 2 (categorize paths) -> {result}")

if __name__ == "__main__":
    test_parses_added_lines_only()
    test_categorize()
```

```python
# tests/unit/test_security.py
# Run from the repo root: python -m tests.unit.test_security
from src.agents.security_reviewer import run_security
from src.diff import parse_diff

DIRTY = """--- a/app.py
+++ b/app.py
+api_key = "SUPERsecret12345"
+result = eval(user_input)
"""
CLEAN = """--- a/app.py
+++ b/app.py
+total = price * quantity
"""

def test_flags_secret_and_eval() -> None:
    findings = run_security(parse_diff(DIRTY))
    messages = " ".join(f.message for f in findings)
    result = "OK"
    if "secret" not in messages or "eval" not in messages:
        result = "WRONG"
    print(f"case 1 (secret + eval flagged) -> {result}")

def test_clean_diff_no_findings() -> None:
    findings = run_security(parse_diff(CLEAN))
    result = "OK"
    if findings != []:
        result = "WRONG"
    print(f"case 2 (clean diff -> none)    -> {result}")

if __name__ == "__main__":
    test_flags_secret_and_eval()
    test_clean_diff_no_findings()
```

**Expected output:**

```
case 1 (missing setting) -> OK
case 2 (empty setting)   -> OK
case 3 (config loads)    -> OK
```
```
case 1 (added lines only) -> OK
case 2 (categorize paths) -> OK
```
```
case 1 (secret + eval flagged) -> OK
case 2 (clean diff -> none)    -> OK
```

The clean-diff case is the one that matters most: it proves the reviewer stays quiet on good code, not just that it's loud on bad code.
