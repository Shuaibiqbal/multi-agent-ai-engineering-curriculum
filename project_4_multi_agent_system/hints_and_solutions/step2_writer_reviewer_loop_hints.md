# Step 2 — Writer↔Reviewer Loop — Hints

> [Back to this step](../README.md#step-2-that-specialist-now-a-real-agent-that-can-improve-its-own-work) · [Hint 1](step2_writer_reviewer_loop_hints.md#hint-1) · [Hint 2](step2_writer_reviewer_loop_hints.md#hint-2) · [Hint 3](step2_writer_reviewer_loop_hints.md#hint-3) · [Hint 4](step2_writer_reviewer_loop_hints.md#hint-4) · [Solution](step2_writer_reviewer_loop_solution.md)

Work through in order — don't jump ahead until you've genuinely tried.

- [Hint 1](#hint-1)
- [Hint 2](#hint-2)
- [Hint 3](#hint-3)
- [Hint 4](#hint-4)

<hr class="page-break">

> [Back to this step](../README.md#step-2-that-specialist-now-a-real-agent-that-can-improve-its-own-work) · [Hint 1](step2_writer_reviewer_loop_hints.md#hint-1) · [Hint 2](step2_writer_reviewer_loop_hints.md#hint-2) · [Hint 3](step2_writer_reviewer_loop_hints.md#hint-3) · [Hint 4](step2_writer_reviewer_loop_hints.md#hint-4) · [Solution](step2_writer_reviewer_loop_solution.md)

## Hint 1

### Simple Version

Two things get built here: a Reviewer (a new, small chain that reads a draft and scores it), and a loop that connects Writer and Reviewer together.

The loop's shape: Writer makes a draft. Reviewer reads it and gives a score plus feedback text. If the score isn't good enough, the Writer tries again — this time using the feedback. This repeats, but only up to a fixed number of times, so it can't go forever.

Think about what "feedback" needs to look like for the Writer to actually use it — not just a number, but text it can read and act on.

<hr class="page-break">

> [Back to this step](../README.md#step-2-that-specialist-now-a-real-agent-that-can-improve-its-own-work) · [Hint 1](step2_writer_reviewer_loop_hints.md#hint-1) · [Hint 2](step2_writer_reviewer_loop_hints.md#hint-2) · [Hint 3](step2_writer_reviewer_loop_hints.md#hint-3) · [Hint 4](step2_writer_reviewer_loop_hints.md#hint-4) · [Solution](step2_writer_reviewer_loop_solution.md)

### Intermediate Version

The README asks for two functions: `run_writer(notes, feedback=None) -> Draft` and `run_reviewer(draft) -> ReviewVerdict`. Notice `feedback` has a default of `None` — this one function has to handle *both* the first draft (no feedback yet) and every redraft (feedback from the previous round), which means your prompt needs a conditional section: "if feedback is given, revise using it; otherwise, write a fresh first draft."

`ReviewVerdict` should be a structured object (a dataclass or Pydantic model), not just a raw string — you need at least a score/pass-fail flag your loop can check with an `if`, plus feedback text the Writer can actually read.

The loop itself lives in `main.py` for this step (there's no Supervisor yet) — a plain Python `for` loop with a fixed `max_rounds`, breaking early if the Reviewer approves.

Sketch `ReviewVerdict`'s fields, and the loop's stopping conditions (both of them — "good enough" and "ran out of rounds"), before Hint 2.

<hr class="page-break">

> [Back to this step](../README.md#step-2-that-specialist-now-a-real-agent-that-can-improve-its-own-work) · [Hint 1](step2_writer_reviewer_loop_hints.md#hint-1) · [Hint 2](step2_writer_reviewer_loop_hints.md#hint-2) · [Hint 3](step2_writer_reviewer_loop_hints.md#hint-3) · [Hint 4](step2_writer_reviewer_loop_hints.md#hint-4) · [Solution](step2_writer_reviewer_loop_solution.md)

## Hint 2

### Simple Version

Pieces you need:

- `run_writer(notes, feedback=None)` — reuses Step 1's chain, but the prompt needs an extra `{feedback}` spot that's blank on the first call.
- A small class or dataclass for `ReviewVerdict` — something like `approved` (True/False) and `feedback` (text).
- `run_reviewer(draft)` — a second small chain, prompted to score/critique a draft and return that verdict shape (an LLM structured-output call, or just careful parsing of its text reply).
- A loop: `for round in range(max_rounds): draft = run_writer(notes, feedback); verdict = run_reviewer(draft); if verdict.approved: break; feedback = verdict.feedback`

<hr class="page-break">

> [Back to this step](../README.md#step-2-that-specialist-now-a-real-agent-that-can-improve-its-own-work) · [Hint 1](step2_writer_reviewer_loop_hints.md#hint-1) · [Hint 2](step2_writer_reviewer_loop_hints.md#hint-2) · [Hint 3](step2_writer_reviewer_loop_hints.md#hint-3) · [Hint 4](step2_writer_reviewer_loop_hints.md#hint-4) · [Solution](step2_writer_reviewer_loop_solution.md)

### Intermediate Version

Look specifically at:

- **Structured output for the Reviewer**, via a Pydantic model passed to `.with_structured_output(ReviewVerdict)` on the `ChatOpenAI` instance — this gets you a real typed object back (`verdict.approved`, `verdict.feedback`) instead of parsing free text yourself, which is fragile and exactly the kind of thing Doc06's tool-calling material warns about.
- **Reusing, not rewriting, Step 1's prompt** — add a `{feedback}` placeholder and a small conditional line ("If feedback is given below, revise the draft to address it.") rather than writing a second, separate Writer prompt from scratch.
- **The loop's two exit conditions**, both required: `verdict.approved` (good enough, stop early) and `round == max_rounds - 1` (ran out of tries, stop anyway and report the last draft plus the fact that it wasn't approved). Missing the second one is exactly the "loop forever" problem the README's own problems table warns about.
- **Keeping this loop in `main.py` for now, not in a graph** — Step 5 is where this exact logic gets moved inside the Supervisor's flow. Don't build graph/state machinery yet; a plain Python loop is the correct scope for this step.

<hr class="page-break">

> [Back to this step](../README.md#step-2-that-specialist-now-a-real-agent-that-can-improve-its-own-work) · [Hint 1](step2_writer_reviewer_loop_hints.md#hint-1) · [Hint 2](step2_writer_reviewer_loop_hints.md#hint-2) · [Hint 3](step2_writer_reviewer_loop_hints.md#hint-3) · [Hint 4](step2_writer_reviewer_loop_hints.md#hint-4) · [Solution](step2_writer_reviewer_loop_solution.md)

## Hint 3

### Simple Version

```
make a ReviewVerdict shape: approved (yes/no), feedback (text)

make run_writer(notes, feedback=None):
    same as Step 1's chain, but the prompt also includes feedback if it was given
    return the draft text

make run_reviewer(draft):
    ask the model to score the draft and explain what's wrong
    return a ReviewVerdict

loop up to N times:
    draft = run_writer(notes, feedback)
    verdict = run_reviewer(draft)
    if verdict says approved: stop, we're done
    otherwise: feedback = verdict's feedback text, try again

if we ran out of tries: report the last draft anyway, and say it wasn't approved
```

<hr class="page-break">

> [Back to this step](../README.md#step-2-that-specialist-now-a-real-agent-that-can-improve-its-own-work) · [Hint 1](step2_writer_reviewer_loop_hints.md#hint-1) · [Hint 2](step2_writer_reviewer_loop_hints.md#hint-2) · [Hint 3](step2_writer_reviewer_loop_hints.md#hint-3) · [Hint 4](step2_writer_reviewer_loop_hints.md#hint-4) · [Solution](step2_writer_reviewer_loop_solution.md)

### Intermediate Version

```
agents/writer_agent.py:
    def run_writer(notes: str, feedback: str | None = None) -> str:
        reuse Step 1's prompt, plus an optional feedback section
        invoke the chain, return the draft

agents/reviewer_agent.py:
    class ReviewVerdict(BaseModel):
        approved: bool
        feedback: str

    def run_reviewer(draft: str) -> ReviewVerdict:
        prompt the model to critique the draft against clear criteria
        use with_structured_output(ReviewVerdict)
        return the verdict

main.py:
    MAX_ROUNDS = 3
    feedback = None
    for round_num in range(MAX_ROUNDS):
        draft = run_writer(notes, feedback)
        verdict = run_reviewer(draft)
        if verdict.approved:
            break
        feedback = verdict.feedback
    report: final draft, verdict.approved, how many rounds it took
```

Test with one draft you make deliberately weak (vague, missing key facts) to confirm the loop actually improves it, and one case designed to never satisfy the Reviewer, to confirm the loop stops at `MAX_ROUNDS` instead of looping forever.

<hr class="page-break">

> [Back to this step](../README.md#step-2-that-specialist-now-a-real-agent-that-can-improve-its-own-work) · [Hint 1](step2_writer_reviewer_loop_hints.md#hint-1) · [Hint 2](step2_writer_reviewer_loop_hints.md#hint-2) · [Hint 3](step2_writer_reviewer_loop_hints.md#hint-3) · [Hint 4](step2_writer_reviewer_loop_hints.md#hint-4) · [Solution](step2_writer_reviewer_loop_solution.md)

## Hint 4

### Simple Version

The trickiest part — the Reviewer's structured verdict:

```python
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

class ReviewVerdict(BaseModel):
    approved: bool
    feedback: str

def run_reviewer(draft):
    model = ChatOpenAI(model="gpt-4o-mini").with_structured_output(ReviewVerdict)
    return model.invoke(f"Review this draft. Approve it only if it's clear and well-supported by facts:\n{draft}")
```

Try finishing `run_writer` (feedback support) and the loop yourself before looking at the Solution.

<hr class="page-break">

> [Back to this step](../README.md#step-2-that-specialist-now-a-real-agent-that-can-improve-its-own-work) · [Hint 1](step2_writer_reviewer_loop_hints.md#hint-1) · [Hint 2](step2_writer_reviewer_loop_hints.md#hint-2) · [Hint 3](step2_writer_reviewer_loop_hints.md#hint-3) · [Hint 4](step2_writer_reviewer_loop_hints.md#hint-4) · [Solution](step2_writer_reviewer_loop_solution.md)

### Intermediate Version

Same core piece, typed and with a clearer rubric in the prompt — the part most people under-invest in, and the reason a Reviewer chain often "approves everything":

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class ReviewVerdict(BaseModel):
    approved: bool = Field(description="True only if the draft is clear, accurate to the notes, and complete")
    feedback: str = Field(description="Specific, actionable feedback if not approved; empty string if approved")

def run_reviewer(draft: str) -> ReviewVerdict:
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(ReviewVerdict)
    return model.invoke(
        "Review this draft against these criteria: clarity, factual grounding, completeness.\n"
        f"Draft:\n{draft}"
    )
```

Note `temperature=0` here — a Reviewer should be consistent, not creative; that's a real, deliberate choice, not an accident. Finish `run_writer`'s feedback handling and the loop yourself, then compare against the [Solution](step2_writer_reviewer_loop_solution.md).

<hr class="page-break">

> [Back to this step](../README.md#step-2-that-specialist-now-a-real-agent-that-can-improve-its-own-work) · [Hint 1](step2_writer_reviewer_loop_hints.md#hint-1) · [Hint 2](step2_writer_reviewer_loop_hints.md#hint-2) · [Hint 3](step2_writer_reviewer_loop_hints.md#hint-3) · [Hint 4](step2_writer_reviewer_loop_hints.md#hint-4) · [Solution](step2_writer_reviewer_loop_solution.md)

Full solution: [Show me the solution](step2_writer_reviewer_loop_solution.md)
