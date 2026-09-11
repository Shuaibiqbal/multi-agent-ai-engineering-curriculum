# Step 4 — Analysis Agent — Hints

> [Back to this step](../README.md#step-4-an-analysis-agent-that-turns-raw-research-into-organized-findings) · [Hint 1](step4_analysis_agent_hints.md#hint-1) · [Hint 2](step4_analysis_agent_hints.md#hint-2) · [Hint 3](step4_analysis_agent_hints.md#hint-3) · [Hint 4](step4_analysis_agent_hints.md#hint-4) · [Solution](step4_analysis_agent_solution.md)

Work through in order — don't jump ahead until you've genuinely tried.

- [Hint 1](#hint-1)
- [Hint 2](#hint-2)
- [Hint 3](#hint-3)
- [Hint 4](#hint-4)

<hr class="page-break">

> [Back to this step](../README.md#step-4-an-analysis-agent-that-turns-raw-research-into-organized-findings) · [Hint 1](step4_analysis_agent_hints.md#hint-1) · [Hint 2](step4_analysis_agent_hints.md#hint-2) · [Hint 3](step4_analysis_agent_hints.md#hint-3) · [Hint 4](step4_analysis_agent_hints.md#hint-4) · [Solution](step4_analysis_agent_solution.md)

## Hint 1

### Simple Version

This one is likely the simplest specialist to build — it doesn't need a tool (Research already looked things up; Analysis just organizes what it found), so it can probably be a plain LCEL chain, the same shape as Step 1's Writer chain, just with a different job: turn a loose list of facts into organized findings (grouped, prioritized, maybe with a short "why this matters" note per group).

The key test here isn't made-up input — it's Step 3's *real* `ResearchNotes` output, since the whole point of this step is proving two already-built specialists' interfaces actually fit together.

<hr class="page-break">

> [Back to this step](../README.md#step-4-an-analysis-agent-that-turns-raw-research-into-organized-findings) · [Hint 1](step4_analysis_agent_hints.md#hint-1) · [Hint 2](step4_analysis_agent_hints.md#hint-2) · [Hint 3](step4_analysis_agent_hints.md#hint-3) · [Hint 4](step4_analysis_agent_hints.md#hint-4) · [Solution](step4_analysis_agent_solution.md)

### Intermediate Version

The README asks for `run_analysis(notes) -> Findings`, taking Step 3's `ResearchNotes` object directly as input. This is a deliberate interface decision: `run_analysis` should accept the *typed object* Step 3 already produces, not a raw string — if it accepted a string, you'd be throwing away the structure Step 3 worked to build, and re-parsing text that was already data.

Design `Findings` the same way you designed `ResearchNotes` — a Pydantic model with a shape the Writer (Step 1/2) can draft from directly: maybe `topic`, and `themes: list[Theme]` where each `Theme` has a short label and the facts that support it.

Since this is likely a tool-free chain, focus your design effort on the prompt: what does "organize these facts into findings" actually mean well enough for the model to do it consistently?

<hr class="page-break">

> [Back to this step](../README.md#step-4-an-analysis-agent-that-turns-raw-research-into-organized-findings) · [Hint 1](step4_analysis_agent_hints.md#hint-1) · [Hint 2](step4_analysis_agent_hints.md#hint-2) · [Hint 3](step4_analysis_agent_hints.md#hint-3) · [Hint 4](step4_analysis_agent_hints.md#hint-4) · [Solution](step4_analysis_agent_solution.md)

## Hint 2

### Simple Version

Pieces you need:

- A `Findings` Pydantic model — something like `topic: str`, `themes: list[str]` (or a richer nested shape if you want to go further).
- A prompt that takes Step 3's facts (turned into a plain string, e.g. `"\n".join(notes.facts)`) and asks the model to group/prioritize them.
- `.with_structured_output(Findings)` on the model, same pattern as Step 2's Reviewer, so you get a typed object back directly.
- `run_analysis(notes: ResearchNotes) -> Findings`, importing `ResearchNotes` from `research_agent.py`.

<hr class="page-break">

> [Back to this step](../README.md#step-4-an-analysis-agent-that-turns-raw-research-into-organized-findings) · [Hint 1](step4_analysis_agent_hints.md#hint-1) · [Hint 2](step4_analysis_agent_hints.md#hint-2) · [Hint 3](step4_analysis_agent_hints.md#hint-3) · [Hint 4](step4_analysis_agent_hints.md#hint-4) · [Solution](step4_analysis_agent_solution.md)

### Intermediate Version

Look specifically at:

- **Importing `ResearchNotes` as the real input type**, not redefining a similar shape locally — `from agents.research_agent import ResearchNotes` and using it directly in `run_analysis`'s signature. This is what makes Step 4's test genuinely prove the two specialists' interfaces fit, instead of testing against a fresh guess at what Research's output looks like.
- **A nested `Findings` shape**, if you want the Writer's job in Step 1/2 easier later — e.g. a `Theme` model (`label: str`, `supporting_facts: list[str]`) nested inside `Findings.themes: list[Theme]`. This is optional, but organizing raw facts into *labeled groups*, not just a reordered flat list, is what actually makes this specialist worth having as its own agent.
- **`.with_structured_output(Findings)`** — same reliability reason as Step 2's Reviewer: you want a typed object your test code and the later Writer can depend on, not text you re-parse.
- **Testing against Step 3's actual saved output**, not new made-up facts — call `run_research(...)` first, then feed that real `ResearchNotes` object straight into `run_analysis(...)`.

<hr class="page-break">

> [Back to this step](../README.md#step-4-an-analysis-agent-that-turns-raw-research-into-organized-findings) · [Hint 1](step4_analysis_agent_hints.md#hint-1) · [Hint 2](step4_analysis_agent_hints.md#hint-2) · [Hint 3](step4_analysis_agent_hints.md#hint-3) · [Hint 4](step4_analysis_agent_hints.md#hint-4) · [Solution](step4_analysis_agent_solution.md)

## Hint 3

### Simple Version

```
make a Findings shape: topic, themes (a list of short labeled groups)

make run_analysis(notes):
    take notes.facts, join them into one block of text
    ask the model to group these facts into a few clear themes
    return a Findings object

test:
    call run_research(topic) from Step 3 to get real notes
    pass those real notes into run_analysis
    check the themes make sense given the facts that went in
```

<hr class="page-break">

> [Back to this step](../README.md#step-4-an-analysis-agent-that-turns-raw-research-into-organized-findings) · [Hint 1](step4_analysis_agent_hints.md#hint-1) · [Hint 2](step4_analysis_agent_hints.md#hint-2) · [Hint 3](step4_analysis_agent_hints.md#hint-3) · [Hint 4](step4_analysis_agent_hints.md#hint-4) · [Solution](step4_analysis_agent_solution.md)

### Intermediate Version

```
agents/analysis_agent.py:
    class Theme(BaseModel):
        label: str
        supporting_facts: list[str]

    class Findings(BaseModel):
        topic: str
        themes: list[Theme]

    def run_analysis(notes: ResearchNotes) -> Findings:
        facts_block = "\n".join(f"- {fact}" for fact in notes.facts)
        model = ChatOpenAI(...).with_structured_output(Findings)
        return model.invoke(f"Group these facts about {notes.topic} into 2-4 clear themes:\n{facts_block}")

test_analysis.py (or main.py):
    from agents.research_agent import run_research
    from agents.analysis_agent import run_analysis

    notes = run_research("electric bikes")
    findings = run_analysis(notes)
    print(findings)
```

Confirm every fact from `notes.facts` ends up under *some* theme — a common bug here is the model quietly dropping a fact it didn't know where to file.

<hr class="page-break">

> [Back to this step](../README.md#step-4-an-analysis-agent-that-turns-raw-research-into-organized-findings) · [Hint 1](step4_analysis_agent_hints.md#hint-1) · [Hint 2](step4_analysis_agent_hints.md#hint-2) · [Hint 3](step4_analysis_agent_hints.md#hint-3) · [Hint 4](step4_analysis_agent_hints.md#hint-4) · [Solution](step4_analysis_agent_solution.md)

## Hint 4

### Simple Version

The core piece:

```python
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

class Findings(BaseModel):
    topic: str
    themes: list[str]

def run_analysis(notes):
    facts_block = "\n".join(notes.facts)
    model = ChatOpenAI(model="gpt-4o-mini").with_structured_output(Findings)
    return model.invoke(f"Group these facts into clear themes for topic {notes.topic}:\n{facts_block}")
```

Try importing `ResearchNotes` and testing against Step 3's real output yourself before checking the Solution.

<hr class="page-break">

> [Back to this step](../README.md#step-4-an-analysis-agent-that-turns-raw-research-into-organized-findings) · [Hint 1](step4_analysis_agent_hints.md#hint-1) · [Hint 2](step4_analysis_agent_hints.md#hint-2) · [Hint 3](step4_analysis_agent_hints.md#hint-3) · [Hint 4](step4_analysis_agent_hints.md#hint-4) · [Solution](step4_analysis_agent_solution.md)

### Intermediate Version

The typed, nested version — closer to what the Writer will actually want to draft from:

```python
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from agents.research_agent import ResearchNotes

class Theme(BaseModel):
    label: str
    supporting_facts: list[str]

class Findings(BaseModel):
    topic: str
    themes: list[Theme]

def run_analysis(notes: ResearchNotes) -> Findings:
    facts_block = "\n".join(f"- {fact}" for fact in notes.facts)
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(Findings)
    return model.invoke(
        f"Group ALL of these facts about {notes.topic} into 2-4 clear themes. "
        f"Every fact must appear under exactly one theme:\n{facts_block}"
    )
```

Note the explicit "every fact must appear under exactly one theme" instruction — this is what prevents the dropped-fact bug mentioned in Hint 3. Write the test yourself, then compare against the [Solution](step4_analysis_agent_solution.md).

<hr class="page-break">

> [Back to this step](../README.md#step-4-an-analysis-agent-that-turns-raw-research-into-organized-findings) · [Hint 1](step4_analysis_agent_hints.md#hint-1) · [Hint 2](step4_analysis_agent_hints.md#hint-2) · [Hint 3](step4_analysis_agent_hints.md#hint-3) · [Hint 4](step4_analysis_agent_hints.md#hint-4) · [Solution](step4_analysis_agent_solution.md)

Full solution: [Show me the solution](step4_analysis_agent_solution.md)
