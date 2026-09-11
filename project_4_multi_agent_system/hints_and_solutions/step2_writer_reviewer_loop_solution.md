# Step 2 — Writer↔Reviewer Loop — Solution

> [Back to this step](../README.md#step-2-that-specialist-now-a-real-agent-that-can-improve-its-own-work) · [Hint 1](step2_writer_reviewer_loop_hints.md#hint-1) · [Hint 2](step2_writer_reviewer_loop_hints.md#hint-2) · [Hint 3](step2_writer_reviewer_loop_hints.md#hint-3) · [Hint 4](step2_writer_reviewer_loop_hints.md#hint-4) · [Solution](step2_writer_reviewer_loop_solution.md)

## Simple Version

**`agents/writer_agent.py`**
```python
from agents.writer_chain import build_writer_chain

_chain = build_writer_chain()

def run_writer(notes, feedback=None):
    if feedback:
        prompt_notes = notes + "\n\nPrevious feedback to address:\n" + feedback
    else:
        prompt_notes = notes
    return _chain.invoke({"notes": prompt_notes})
```

**`agents/reviewer_agent.py`**
```python
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

class ReviewVerdict(BaseModel):
    approved: bool
    feedback: str

def run_reviewer(draft):
    model = ChatOpenAI(model="gpt-4o-mini").with_structured_output(ReviewVerdict)
    return model.invoke("Review this draft for clarity and accuracy:\n" + draft)
```

**`main.py`**
```python
from agents.writer_agent import run_writer
from agents.reviewer_agent import run_reviewer

MAX_ROUNDS = 3
notes = "Electric bikes cost $800-3000. Battery range 20-60 miles."
feedback = None

for i in range(MAX_ROUNDS):
    draft = run_writer(notes, feedback)
    verdict = run_reviewer(draft)
    print(f"Round {i+1}, approved={verdict.approved}")
    if verdict.approved:
        break
    feedback = verdict.feedback

print(draft)
```

This works. It reuses Step 1's chain via a module-level `_chain`, which is fine, though building the chain fresh inside `run_writer` on every call (Intermediate version) is a little cleaner for testing.

<hr class="page-break">

> [Back to this step](../README.md#step-2-that-specialist-now-a-real-agent-that-can-improve-its-own-work) · [Hint 1](step2_writer_reviewer_loop_hints.md#hint-1) · [Hint 2](step2_writer_reviewer_loop_hints.md#hint-2) · [Hint 3](step2_writer_reviewer_loop_hints.md#hint-3) · [Hint 4](step2_writer_reviewer_loop_hints.md#hint-4) · [Solution](step2_writer_reviewer_loop_solution.md)

## Intermediate Version

**`agents/writer_agent.py`**
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

WRITER_PROMPT = (
    "You are a content writer. Write a short, clear draft (3-5 paragraphs) "
    "based only on these research notes. Do not invent facts not in the notes.\n\n"
    "Research notes:\n{notes}\n\n"
    "{feedback_section}"
)


def run_writer(notes: str, feedback: str | None = None) -> str:
    feedback_section = ""
    if feedback:
        feedback_section = f"Revise to address this reviewer feedback:\n{feedback}"

    prompt = ChatPromptTemplate.from_template(WRITER_PROMPT)
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    chain = prompt | model | StrOutputParser()
    return chain.invoke({"notes": notes, "feedback_section": feedback_section})
```

**`agents/reviewer_agent.py`**
```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI


class ReviewVerdict(BaseModel):
    approved: bool = Field(description="True only if clear, accurate to the notes, and complete")
    feedback: str = Field(description="Specific, actionable feedback if not approved; empty if approved")


def run_reviewer(draft: str) -> ReviewVerdict:
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(ReviewVerdict)
    return model.invoke(
        "Review this draft against: clarity, factual grounding in the notes, completeness.\n"
        f"Draft:\n{draft}"
    )
```

**`main.py`**
```python
from agents.writer_agent import run_writer
from agents.reviewer_agent import run_reviewer, ReviewVerdict

MAX_ROUNDS = 3


def run_writer_reviewer_loop(notes: str) -> tuple[str, ReviewVerdict]:
    feedback: str | None = None
    verdict: ReviewVerdict | None = None
    draft = ""

    for round_num in range(MAX_ROUNDS):
        draft = run_writer(notes, feedback)
        verdict = run_reviewer(draft)
        if verdict.approved:
            return draft, verdict
        feedback = verdict.feedback

    return draft, verdict  # ran out of rounds; return last attempt, unapproved


if __name__ == "__main__":
    notes = "Electric bikes cost $800-3000. Battery range 20-60 miles."
    final_draft, final_verdict = run_writer_reviewer_loop(notes)
    print(final_draft)
    print("Approved:", final_verdict.approved)
```

**What's different, and why it's better:** the loop logic is pulled into its own testable function, `run_writer_reviewer_loop`, instead of living directly in a script's top level — this is exactly what `test_writer_reviewer.py` needs to import and call. Full type hints, including the `tuple[str, ReviewVerdict]` return type, which tells any caller (including Step 5's Supervisor, later) exactly what it gets back. `temperature=0` on the Reviewer keeps its judgments consistent between runs — important once you're comparing "did this get better" across rounds.

**Which one should you use, and why?** The Simple version is correct and fine for a first pass at proving the loop works. Move to the Intermediate version specifically because Step 5's Supervisor needs to call this exact loop logic as a function with a clear return type — if the loop only exists as inline script code, you'll end up rewriting it anyway when the Supervisor arrives. Writing it as a real function now, even though nothing calls it but `main.py` yet, is the same "prove it works alone, in a reusable shape" principle the whole project is built on.
