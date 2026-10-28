# Intermediate (.env by hand) — Hints

> [Back to the exercise](../README.md#ex-env_parsing) · [Hint 1](env_parsing_hints.md#hint-1) · [Hint 2](env_parsing_hints.md#hint-2) · [Solution](env_parsing_solution.md)

**Where this exercise is saved:** `practice/env_config_practice.py`, under its `# Intermediate` section — the same file also holds the [Edge cases exercise](../README.md#ex-env_edge_cases), under an `# Edge cases` section. Run it with `cd practice && python env_config_practice.py`.

**Used later by:** the [Build Task](../README.md#build-task-config-logging-foundation)'s `load_config()` in `practice/build_task/config.py` — it ships the short `load_dotenv()` + `os.getenv()` version you land on here, re-written (not imported) so it can return a typed `Config` object.

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried. Each hint builds toward the full solution.

- [Hint 1 — The idea, and the exact pieces](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

## Hint 1 — The idea, and the exact pieces {: #hint-1 }

Parsing this by hand touches a few real Python skills: reading a file line by line, string splitting with a limit, and building a dictionary as you go.

`for line in open(path):` iterates over a file one line at a time without loading the whole thing into memory first. `line.strip()` removes the trailing newline character each line comes with. `line.split("=", 1)` splits on the first `=` only (the second argument, `1`, is the max number of splits) — this matters because a value could itself contain an `=` character, and you don't want to split on that one too.

The exact pieces:

- `open(path)` used in a `for line in open(path):` loop — Python handles closing the file for you at the end of iteration in this pattern (though a `with open(path) as f:` block is the more correct, explicit way — worth knowing for later).
- `line.strip()` — removes leading/trailing whitespace, including the newline `\n` at the end of each line.
- Skip logic: `if not line or "=" not in line: continue` — handles blank lines and any malformed lines safely.
- `key, value = line.split("=", 1)` — unpacks the 2-item list `split()` returns directly into two variables.
- For the library comparison: `from dotenv import load_dotenv; load_dotenv(); os.getenv("KEY")`.

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

```
function parse_env_by_hand(path) -> dict:
    env_vars = {}
    for line in open(path):
        line = line.strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env_vars[key] = value
    return env_vars

compare against:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
```

```python
# practice/env_config_practice.py
def parse_env_by_hand(path: str) -> dict:
    env_vars = {}
    for line in open(path):
        line = line.strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env_vars[key] = value
    return env_vars
```

Now write the 2-line `python-dotenv` version yourself and compare both against the [Solution](env_parsing_solution.md).

Full solution: [Show me the solution](env_parsing_solution.md)
