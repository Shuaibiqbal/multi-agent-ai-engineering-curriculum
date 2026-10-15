# Step 1 — The Two-Agent Pipeline, Running Standalone (No MCP Yet) — Hints

> [Back to the step](../READING_README.md#step-1-the-two-agent-pipeline-running-standalone-no-mcp-yet) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](step1_standalone_pipeline_solution.md)

- [Hint 1 — The idea, and the exact pieces](#hint-1)
- [Hint 2 — The plan, and the two things that make the loop real](#hint-2)

## Hint 1 — The idea, and the exact pieces {: #hint-1 }

A generator->critic->revise loop as plain Python, no MCP. The pieces (Project 4's Writer/Reviewer, reused):

- `src/agents/researcher.py` — `Draft` (topic, summary), `run_researcher(model, topic, feedback=None)`. With feedback, fix ONLY the named issues.
- `src/agents/fact_checker.py` — `FactCheckVerdict` (`approved`, `issues`), `run_fact_checker(model, draft)` = `prompt | model.with_structured_output(...)`, with real criteria (wrong dates/names/invented facts).
- `src/pipeline.py` — `run_pipeline(model, topic, max_rounds, progress=None) -> PipelineResult`, plus a `Progress` holder.
- `main.py` — run it on a convergent topic and a hard one.

## Hint 2 — The plan, and the two things that make the loop real {: #hint-2 }

```
run_pipeline(model, topic, max_rounds, progress):
    draft = run_researcher(model, topic)
    for r in 1..max_rounds:
        progress.latest_draft = draft.summary
        v = run_fact_checker(model, draft)
        progress.rounds.append({round:r, approved:v.approved, issues:v.issues})
        if v.approved: return PipelineResult(..., approved=True, rounds)
        draft = run_researcher(model, topic, feedback="\n".join(v.issues))
    return PipelineResult(..., approved=False, rounds)   # the CAP
```

Two things make the loop real, not a formality: (1) the Fact-Checker's prompt has **real criteria** (a vague critic approves round 1 and the loop never runs), and (2) the Researcher's prompt tells it to **fix only the named issues** (so round 2 differs from round 1, and it converges instead of rewriting forever). The `Progress` holder is seeded now because Step 4's partial fallback reads it. Test the loop with a fake model (no key): a wrong draft -> rejected -> fixed; a never-approved topic -> stops at the cap. The whole file set is in the [Solution](step1_standalone_pipeline_solution.md).
