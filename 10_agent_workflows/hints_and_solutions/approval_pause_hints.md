# Real-world (a real approval pause) — Hints

> [Back to the exercise](../README.md#ex-approval_pause) · [Hint 1](approval_pause_hints.md#hint-1) · [Hint 2](approval_pause_hints.md#hint-2) · [Solution](approval_pause_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried. Each hint has 2 depth levels: **Basic** (the plain idea) and **Intermediate** (proper Python, plus the cases a real project has to handle).

- [Hint 1 — The idea, and the exact pieces](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

<hr class="page-break">

> [Back to the exercise](../README.md#ex-approval_pause) · [Hint 1](approval_pause_hints.md#hint-1) · [Hint 2](approval_pause_hints.md#hint-2) · [Solution](approval_pause_solution.md)

## Hint 1 — The idea, and the exact pieces {: #hint-1 }

### Basic Version

Build a three-node graph: `draft_node` searches and writes a draft, `approval_node` pauses with `interrupt()` showing the draft and its source files, and `finish_node` sends the draft only if approved. Compile it with a checkpointer (Doc09), run it once (it pauses), then resume with `Command(resume="approved")` on the same `thread_id`.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-approval_pause) · [Hint 1](approval_pause_hints.md#hint-1) · [Hint 2](approval_pause_hints.md#hint-2) · [Solution](approval_pause_solution.md)

### Intermediate Version

The exact pieces:

- `interrupt({"draft": ..., "sources": [...files...], "prompt": ...})` — whatever you put in the dict is what the reviewer sees.
- Test **both** outcomes, each in its own `thread_id` — a run that does the risky thing even on "rejected" is the bug that matters most.
- A dict as the resume value — `{"decision": ..., "by": ..., "at": ...}` — so the node can save who decided and when.

And one trap worth knowing before you add a "too old to approve" check: when a paused node resumes, LangGraph runs it again **from its first line**. A `datetime.now()` taken inside `approval_node` would be the resume time. Save the time in `draft_node`, in state, instead.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-approval_pause) · [Hint 1](approval_pause_hints.md#hint-1) · [Hint 2](approval_pause_hints.md#hint-2) · [Solution](approval_pause_solution.md)

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

### Basic Version

```
draft_node:    sources = retrieve(...); draft = model answer from them
approval_node: decision = interrupt({"draft": ..., "sources": ...})
               return {"approved": decision == "approved"}
finish_node:   the draft if approved, else "Not approved -- nothing was sent."

graph: START -> draft -> approval -> finish -> END, MemorySaver()
run once (pauses), then graph.invoke(Command(resume="approved"), config)
```

<hr class="page-break">

> [Back to the exercise](../README.md#ex-approval_pause) · [Hint 1](approval_pause_hints.md#hint-1) · [Hint 2](approval_pause_hints.md#hint-2) · [Solution](approval_pause_solution.md)

### Intermediate Version

```
run_with_approval(graph, task, decision, thread_id):
    invoke the task, then invoke Command(resume=decision)

Approach 2: resume with {"decision", "by", "at"}; save approved_by/at
Approach 3: draft_node also saves drafted_at (datetime.now(...)
            .isoformat()); is_stale(drafted_at) compares its age with
            timedelta(hours=MAX_APPROVAL_AGE_HOURS)
```

**Difference between Basic and Intermediate:** Basic pauses and resumes on the happy path. Intermediate tests rejection too, records who and when, and refuses a draft that waited too long — measuring from the right moment.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-approval_pause) · [Hint 1](approval_pause_hints.md#hint-1) · [Hint 2](approval_pause_hints.md#hint-2) · [Solution](approval_pause_solution.md)

Full solution: [Show me the solution](approval_pause_solution.md)
