# Step 5 — An Approval Agent That Only Asks a Human When It Really Needs To — Hints

> [Back to this step](../READING_README.md#step-5-an-approval-agent-that-only-asks-a-human-when-it-really-needs-to-final-3-agents) · [Hint 1](step5_approval_agent_hints.md#hint-1) · [Hint 2](step5_approval_agent_hints.md#hint-2) · [Solution](step5_approval_agent_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've really tried. Each hint starts with the plain idea, then shows the shape of the real code.

- [Hint 1 — When should a human be asked?](#hint-1)
- [Hint 2 — The plan: grow Step 2's node](#hint-2)

<hr class="page-break">

> [Back to this step](../READING_README.md#step-5-an-approval-agent-that-only-asks-a-human-when-it-really-needs-to-final-3-agents) · [Hint 1](step5_approval_agent_hints.md#hint-1) · [Hint 2](step5_approval_agent_hints.md#hint-2) · [Solution](step5_approval_agent_solution.md)

## Hint 1 — When should a human be asked? {: #hint-1 }

Asking about **every** answer (Steps 2-4) is safe, but too slow to use. Ask only when something is actually uncertain or risky:

- the answer isn't grounded in the documents;
- the answer cites no source file;
- the task asks the system to **do** something (send, cancel, delete ...).

If none of these apply, approve by yourself. If any does, pause — and tell the person *which* one.

Add each check as its own small function to `agents/approval_agent.py`:

- `cites_a_source(answer, sources)` — is any `"[" + source_file + "]"` in the answer?
- `asks_for_an_action(task)` — is any word from `ACTION_WORDS` in the lowered task?
- `run_checks(state) -> list[str]` — a list of the checks that **failed**, like `["the task asks for an action"]`.

An explicit list beats one "is this okay?" model call: when an answer is wrongly approved or wrongly escalated, you can see exactly which rule did it — and unit-test each one.

<hr class="page-break">

> [Back to this step](../READING_README.md#step-5-an-approval-agent-that-only-asks-a-human-when-it-really-needs-to-final-3-agents) · [Hint 1](step5_approval_agent_hints.md#hint-1) · [Hint 2](step5_approval_agent_hints.md#hint-2) · [Solution](step5_approval_agent_solution.md)

## Hint 2 — The plan: grow Step 2's node {: #hint-2 }

`approval_node` already exists from Step 2. Change only two things:

```
approval_node(state):
    reasons = run_checks(state)        # was: a fixed one-line list
    if not reasons:                    # new block
        return approved, path += ["auto_approved"]
    ... Step 2's interrupt() and yes/no handling, unchanged ...
```

`graph.py` and `main.py` don't change — `ask_human()` already prints the reasons.

One LangGraph rule to know here: when a paused node is resumed, it runs **again from its first line** — `interrupt()` then returns the resume value instead of pausing. So anything above `interrupt()` runs twice (you'll see the log line twice). Never put a real action — sending an email — above `interrupt()`.

Tests:

- `test_approval_checks.py` — hand-made states: all pass → `[]`; no citation → `["cites no source file"]`; an action task → `["the task asks for an action"]`.
- The integration test: a document question is now **auto-approved**; an action request pauses — resume `"yes"` in one thread and `"no"` in another.

Then run `pause_demo.py` and `resume_demo.py` once more: the resume still comes from disk.

Full solution: [Show me the solution](step5_approval_agent_solution.md)
