# Step 2 — That Specialist, Now a Real Agent That Can Improve Its Own Work — Solution

> [Back to this step](../READING_README.md#step-2-that-specialist-now-a-real-agent-that-can-improve-its-own-work) · [Hint 1](step2_writer_reviewer_loop_hints.md#hint-1) · [Hint 2](step2_writer_reviewer_loop_hints.md#hint-2) · [Solution](step2_writer_reviewer_loop_solution.md)

**Story — Step 2:** a first draft is rarely the best one. This step gives the Writer a way to improve: a Reviewer scores each draft, and a small loop sends the feedback back to the Writer — up to a hard limit. It's still just two agents in a plain Python loop, with no graph. **If not:** Step 5 would be the first place the revision loop ever ran, inside a much bigger system.

After this step the project runs: it writes an article, has it reviewed, and revises it until it passes or the limit is reached. Files not shown here don't change.

## Solution — a scored verdict, written criteria, and an honest report

**Changed from Step 1:** `writer.txt` gets a feedback section; `run_writer()` gets a `feedback` parameter.

**Story — `prompts/writer.txt` + `agents/writer_agent.py`:** the chain is the same; now it can be told what to fix. An empty feedback becomes the word "none", so the prompt always reads cleanly. **If not:** the Writer would redraft blindly, and could repeat the same mistake every round.

`src/prompts/writer.txt`

```text
You are the Writer on a content team. Write a short article (150-250
words) with a title, using ONLY the findings below. Do not add facts
that are not in the findings. Keep each fact's [source] tag.

Findings:
{findings}

Reviewer feedback on your last draft (fix every point, or "none"):
{feedback}
```

```python
# src/agents/writer_agent.py
# The Writer agent. build_writer_chain() is the LCEL chain; run_writer()
# turns findings (and optional feedback) into a draft.
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.models.llm import get_model
from src.utils.prompts import load_prompt

def build_writer_chain():
    prompt = ChatPromptTemplate.from_template(load_prompt("writer"))
    return prompt | get_model() | StrOutputParser()

# changed in Step 2: + feedback
def run_writer(findings, feedback=""):
    if feedback == "":
        feedback = "none"
    chain = build_writer_chain()
    return chain.invoke({"findings": findings, "feedback": feedback})
```

**Story — `schemas.py`:** the verdict as a checked object: a score from 1 to 10 and the feedback text (Doc05's `with_structured_output`). **If not:** you'd parse "GOOD"/"BAD" out of free text.

```python
# src/schemas.py
# ReviewVerdict: the Reviewer's reply as a checked object — a score (1-10)
# the code compares to the pass mark, and the feedback text.
from pydantic import BaseModel, Field

class ReviewVerdict(BaseModel):
    score: int = Field(ge=1, le=10)
    feedback: str
```

**Story — `prompts/reviewer.txt`:** three written criteria — clarity, grounding, completeness — and "7 or more only if all three are met". **If not:** a vague Reviewer approves the first draft almost every time, and the loop never gets tested.

`src/prompts/reviewer.txt`

```text
You are the Reviewer on a content team. Score this draft from 1 to 10
against three criteria:
1. Clarity - is it easy to read, with a clear title and structure?
2. Grounding - is every fact backed by a [source] tag from the findings?
3. Completeness - does it cover the main findings, in 150-250 words?
Give 7 or more only if all three criteria are met. In the feedback, list
exactly what to fix.

Findings the draft must be based on:
{findings}

Draft:
{draft}
```

**Story — `agents/reviewer_agent.py`:** the model scores; **the code** decides the pass mark (`PASS_SCORE = 7`). **If not:** "pass" would drift with the model's mood from run to run.

```python
# src/agents/reviewer_agent.py
# The Reviewer agent. PASS_SCORE is the pass mark, decided in code.
# run_reviewer(findings, draft) returns a checked ReviewVerdict.
from langchain_core.prompts import ChatPromptTemplate

from src.models.llm import get_model
from src.schemas import ReviewVerdict
from src.utils.prompts import load_prompt

PASS_SCORE = 7

def run_reviewer(findings, draft):
    prompt = ChatPromptTemplate.from_template(load_prompt("reviewer"))
    chain = prompt | get_model().with_structured_output(ReviewVerdict)
    return chain.invoke({"findings": findings, "draft": draft})
```

**Story — `main.py`:** `write_with_review()` is the Generator → Critic loop (Doc11): write, review, pass the feedback back, stop at `MAX_REVISIONS`. It returns a dict with the **same keys the Step 5 team will use** (`draft`, `accepted`, `feedback_history`, `revision_count`), and `print_report(result)` prints it — never showing a rejected draft as finished. `print_report()` keeps its name and its input for the rest of the project. **If not:** a Writer and Reviewer that never agree would loop forever, and Step 5 would have to rewrite how results are printed.

```python
# main.py
# The file you run: python main.py
# Step 2 version: write_with_review() loops the Writer and Reviewer up to
# MAX_REVISIONS; print_report() shows the result honestly.
import sys

from src.agents.reviewer_agent import PASS_SCORE, run_reviewer
from src.agents.writer_agent import run_writer
from src.config import load_config
from src.exceptions import MissingConfigError
from src.utils.logger import get_logger

MAX_REVISIONS = 3

SAMPLE_FINDINGS = (
    "Range:\n- A battery gives 40 to 100 km per charge. [battery-review]\n"
    "Rules:\n- EU e-bike motors are limited to 25 km/h. [eu-rules]\n"
)

def write_with_review(findings):
    logger = get_logger(__name__)
    result = {
        "draft": "",
        "accepted": False,
        "feedback_history": [],
        "revision_count": 0,
    }
    feedback = ""
    for round_number in range(1, MAX_REVISIONS + 1):
        result["draft"] = run_writer(findings, feedback)
        verdict = run_reviewer(findings, result["draft"])
        logger.info(f"round {round_number}: score {verdict.score}")
        if verdict.score >= PASS_SCORE:
            result["accepted"] = True
            return result
        feedback = verdict.feedback
        result["feedback_history"].append(feedback)
        result["revision_count"] = result["revision_count"] + 1
    return result

def print_report(result):
    if result["accepted"]:
        print("\nFinal article:\n")
        print(result["draft"])
    else:
        attempts = result["revision_count"]
        print(f"\nCouldn't agree after {attempts} revisions. Feedback:")
        number = 1
        for feedback in result["feedback_history"]:
            print(f"  round {number}: {feedback}")
            number = number + 1
        print("\nLast draft (NOT approved):\n")
        print(result["draft"])

def main():
    try:
        load_config()
    except MissingConfigError as e:
        print(f"Setup problem: {e}")
        sys.exit(1)

    result = write_with_review(SAMPLE_FINDINGS)
    print_report(result)

if __name__ == "__main__":
    main()
```

**Story — `tests/integration/test_live_agents.py`:** the one check that matters most here — a weak draft must **fail** (case 2). **If not:** a Reviewer that passes everything looks exactly like one that works.

```python
# tests/integration/test_live_agents.py
# Runs the agents against the real OpenAI API — each step adds cases.
# Each case prints OK or WRONG. Needs a valid OPENAI_API_KEY in .env.
# Run from the repo root: python -m tests.integration.test_live_agents
from src.agents.reviewer_agent import PASS_SCORE, run_reviewer
from src.agents.writer_agent import run_writer
from src.config import load_config

FINDINGS = (
    "Range:\n- A battery gives 40 to 100 km per charge. [battery-review]\n"
    "Rules:\n- EU e-bike motors are limited to 25 km/h. [eu-rules]\n"
)


def test_writer_keeps_sources():
    draft = run_writer(FINDINGS)
    result = "OK"
    if "[" not in draft:
        result = "WRONG"
    print(f"case 1 (writer keeps sources) -> {result}")


def test_reviewer_rejects_weak_draft():
    verdict = run_reviewer(FINDINGS, "E-bikes are good.")
    result = "OK"
    if verdict.score >= PASS_SCORE:
        result = "WRONG"
    print(f"case 2 (weak draft fails)     -> {result}")


if __name__ == "__main__":
    load_config()
    test_writer_keeps_sources()
    test_reviewer_rejects_weak_draft()
```

**Run it** (from the repo root):

```bash
python -m tests.integration.test_live_agents
python main.py
```

**Expected output:**

```
case 1 (writer keeps sources) -> OK
case 2 (weak draft fails)     -> OK
```

To see the limit, set `PASS_SCORE = 11` for one run: you should get "Couldn't agree after 3 revisions" and the full feedback list — never an endless loop.
