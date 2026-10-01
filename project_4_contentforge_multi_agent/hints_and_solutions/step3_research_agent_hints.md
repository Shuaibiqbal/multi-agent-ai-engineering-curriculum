# Step 3 — A Research Agent That Looks Things Up Before Anyone Else Works — Hints

> [Back to this step](../READING_README.md#step-3-a-research-agent-that-looks-things-up-before-anyone-else-works) · [Hint 1](step3_research_agent_hints.md#hint-1) · [Hint 2](step3_research_agent_hints.md#hint-2) · [Solution](step3_research_agent_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've really tried. Each hint starts with the plain idea, then shows the shape of the real code.

- [Hint 1 — Look it up before you write it down](#hint-1)
- [Hint 2 — The plan, and the new main.py](#hint-2)

<hr class="page-break">

> [Back to this step](../READING_README.md#step-3-a-research-agent-that-looks-things-up-before-anyone-else-works) · [Hint 1](step3_research_agent_hints.md#hint-1) · [Hint 2](step3_research_agent_hints.md#hint-2) · [Solution](step3_research_agent_solution.md)

## Hint 1 — Look it up before you write it down {: #hint-1 }

Research is the one specialist that needs a tool: facts must be **looked up**, not remembered.

Build the tool first, alone:

- `data/sample/facts.json` — a few topics, each with 4-5 facts, each fact ending in a `[source]` tag;
- `tools/lookup.py` — a `@tool` called `lookup_facts(topic)`: read the file (Doc02: `json.loads(file.read())`), find a known topic whose name appears in the given topic, and return its facts one per line — or `""` if none matches.

Test it with no model at all (`tests/unit/test_lookup.py`).

`run_research(topic) -> str` in `agents/research_agent.py`:

1. `facts = lookup_facts.invoke({"topic": topic})`
2. if `facts == ""` → log a warning and return `""` — **no model call**, nothing invented;
3. otherwise, a Doc05 chain with `research.txt` ("one line per fact, keep the tag, add nothing") turns the facts into notes.

The order is the point: the model only rewrites what the tool found.

<hr class="page-break">

> [Back to this step](../READING_README.md#step-3-a-research-agent-that-looks-things-up-before-anyone-else-works) · [Hint 1](step3_research_agent_hints.md#hint-1) · [Hint 2](step3_research_agent_hints.md#hint-2) · [Solution](step3_research_agent_solution.md)

## Hint 2 — The plan, and the new main.py {: #hint-2 }

```
main():
    topic = input("Topic: ").strip()
    notes = run_research(topic)
    if notes == "":
        print("No article: nothing is known about this topic yet.")
        return
    print the notes
    result = write_with_review(notes)
    print_report(result)
```

The Writer and Reviewer don't change — the notes simply take the place of the made-up findings.

Add to the integration test:

- `run_research("electric bikes")` → count the `[` characters: every fact should keep its source;
- `run_research("deep sea mining")` → exactly `""`.

If a known topic comes back with fewer tags than facts, the research prompt is letting the model drop or merge facts — tighten it.

Full solution: [Show me the solution](step3_research_agent_solution.md)
