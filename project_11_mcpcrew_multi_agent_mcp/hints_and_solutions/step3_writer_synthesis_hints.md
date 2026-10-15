# Step 3 — The Writer Synthesizes a Final Report — Hints

> [Back to the step](../READING_README.md#step-3-the-writer-synthesizes-a-final-report) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](step3_writer_synthesis_solution.md)

- [Hint 1 — The idea, synthesize not concatenate](#hint-1)
- [Hint 2 — The plan](#hint-2)

## Hint 1 — The idea, synthesize not concatenate {: #hint-1 }

The Writer is a plain LLM call (no tools) that turns both specialists' findings into **one** report. The whole value is in the prompt: tell it to *weave the sources together*, not stack them — and to name any source marked unavailable (so a degraded run is honest, Step 4). Add `src/agents/writer_agent.py` (`run_writer(client, task, notes_findings, web_findings, web_unavailable)`) and a real `writer_node` replacing Step 2's placeholder.

## Hint 2 — The plan {: #hint-2 }

```
run_writer(client, task, notes, web, web_unavailable):
    web_section = "(web page could not be reached)" if web_unavailable else web
    user = task + notes + web_section + "write the combined report"
    system = "Synthesize into ONE report; weave sources; if a source is
              unavailable, say so; never pretend it was checked."
    return chat.completions.create([system, user]).content
writer_node(state): run_writer(...) -> Command(goto=END, update={report})
```

Prove it on task 3: the report should contain at least one point that *connects* a note and the status page (e.g. "docs pending in the notes, and listed as an open risk on the status page") — something a concatenation could never produce. The whole file set is in the [Solution](step3_writer_synthesis_solution.md).
