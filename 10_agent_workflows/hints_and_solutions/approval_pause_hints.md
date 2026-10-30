# Real-world (a real approval pause) — Hints

> [Back to the exercise](../README.md#ex-approval_pause) · [Hint 1](approval_pause_hints.md#hint-1) · [Hint 2](approval_pause_hints.md#hint-2) · [Solution](approval_pause_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried.

- [Hint 1 — The idea, and the exact pieces](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

## Hint 1 — The idea, and the exact pieces {: #hint-1 }

The exact pieces:

- `interrupt({"draft": ..., "sources": [...files...], "prompt": ...})` — whatever you put in the dict is what the reviewer sees.
- Test **both** outcomes, each in its own `thread_id` — a run that does the risky thing even on "rejected" is the bug that matters most.
- A dict as the resume value — `{"decision": ..., "by": ..., "at": ...}` — so the node can save who decided and when.

And one trap worth knowing before you add a "too old to approve" check: when a paused node resumes, LangGraph runs it again **from its first line**. A `datetime.now()` taken inside `approval_node` would be the resume time. Save the time in `draft_node`, in state, instead.

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

```
run_with_approval(graph, task, decision, thread_id):
    invoke the task, then invoke Command(resume=decision)

Resume with {"decision", "by", "at"}; save approved_by/at.
draft_node also saves drafted_at (datetime.now(...)
            .isoformat()); is_stale(drafted_at) compares its age with
            timedelta(hours=MAX_APPROVAL_AGE_HOURS)
```

Full solution: [Show me the solution](approval_pause_solution.md)
