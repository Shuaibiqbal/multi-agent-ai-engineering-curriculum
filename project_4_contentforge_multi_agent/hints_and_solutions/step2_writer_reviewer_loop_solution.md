# Step 2 — That Specialist, Now a Real Agent That Can Improve Its Own Work — Solution

> [Back to this step](../READING_README.md#step-2-that-specialist-now-a-real-agent-that-can-improve-its-own-work) · [Hint 1](step2_writer_reviewer_loop_hints.md#hint-1) · [Hint 2](step2_writer_reviewer_loop_hints.md#hint-2) · [Solution](step2_writer_reviewer_loop_solution.md)

**Story — Step 2:** a first draft is rarely the best one. This step gives the Writer a way to improve: a Reviewer scores each draft, and a small loop sends the feedback back to the Writer — up to a hard limit. It's still just two agents in a plain Python loop, with no graph. **If not:** Step 5 would be the first place the revision loop ever ran, inside a much bigger system.

After this step the project runs: it writes an article, has it reviewed, and revises it until it passes or the limit is reached. Files not shown here don't change.

## Solution — a scored verdict, written criteria, and an honest report

**Changed from Step 1:** `writer.txt` gets a feedback section; `run_writer()` gets a `feedback` parameter.

**Story — `prompts/writer.txt` + `agents/writer_agent.py`:** the chain is the same; now it can be told what to fix. An empty feedback becomes the word "none", so the prompt always reads cleanly. **If not:** the Writer would redraft blindly, and could repeat the same mistake every round.

`src/contentforge/prompts/writer.txt`

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
# src/contentforge/agents/writer_agent.py
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from contentforge.models.llm import get_model
from contentforge.utils.prompts import load_prompt

def build_writer_chain():
    # why: the Writer's whole skill is one LCEL chain (Doc05) — proven
    # alone in Step 1, and never rewritten after that
    prompt = ChatPromptTemplate.from_template(load_prompt("writer"))
    return prompt | get_model() | StrOutputParser()

# changed in Step 2: + feedback
def run_writer(findings: str, feedback: str = "") -> str:
    # why: feedback is what turns a one-shot chain into an agent that
    # can improve its own work
    if feedback == "":
        feedback = "none"
    chain = build_writer_chain()
    return chain.invoke({"findings": findings, "feedback": feedback})
```

**Story — `schemas.py`:** the verdict as a checked object: a score from 1 to 10 and the feedback text (Doc05's `with_structured_output`). **If not:** you'd parse "GOOD"/"BAD" out of free text.

```python
# src/contentforge/schemas.py
from pydantic import BaseModel, Field

class ReviewVerdict(BaseModel):
    # why: a number the code can compare, not a word to search for
    score: int = Field(ge=1, le=10)
    # why: the Writer gets this text back on a revision
    feedback: str
```

**Story — `prompts/reviewer.txt`:** three written criteria — clarity, grounding, completeness — and "7 or more only if all three are met". **If not:** a vague Reviewer approves the first draft almost every time, and the loop never gets tested.

`src/contentforge/prompts/reviewer.txt`

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
# src/contentforge/agents/reviewer_agent.py
from langchain_core.prompts import ChatPromptTemplate

from contentforge.models.llm import get_model
from contentforge.schemas import ReviewVerdict
from contentforge.utils.prompts import load_prompt

# why: the pass mark is decided in code, not by the model's mood — so
# the bar is the same on every run and easy to change in one place
PASS_SCORE = 7

def run_reviewer(findings: str, draft: str) -> ReviewVerdict:
    prompt = ChatPromptTemplate.from_template(load_prompt("reviewer"))
    # how: with_structured_output returns a checked ReviewVerdict (Doc05)
    chain = prompt | get_model().with_structured_output(ReviewVerdict)
    return chain.invoke({"findings": findings, "draft": draft})
```

**Story — `main.py`:** `write_with_review()` is the Generator → Critic loop (Doc11): write, review, pass the feedback back, stop at `MAX_REVISIONS`. It returns a dict with the **same keys the Step 5 team will use** (`draft`, `accepted`, `feedback_history`, `revision_count`), and `print_report(result)` prints it — never showing a rejected draft as finished. `print_report()` keeps its name and its input for the rest of the project. **If not:** a Writer and Reviewer that never agree would loop forever, and Step 5 would have to rewrite how results are printed.

```python
# src/contentforge/main.py
import sys

from contentforge.agents.reviewer_agent import PASS_SCORE, run_reviewer
from contentforge.agents.writer_agent import run_writer
from contentforge.config import load_config
from contentforge.exceptions import MissingConfigError
from contentforge.utils.logger import get_logger

# why: the hard limit on Writer <-> Reviewer rounds — never loop forever
MAX_REVISIONS = 3

SAMPLE_FINDINGS = (
    "Range:\n- A battery gives 40 to 100 km per charge. [battery-review]\n"
    "Rules:\n- EU e-bike motors are limited to 25 km/h. [eu-rules]\n"
)

def write_with_review(findings: str) -> dict:
    # why: returns a dict with the SAME keys the Step 5 team state uses,
    # so print_report() never has to change its input
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
        logger.info("round %s: score %s", round_number, verdict.score)
        if verdict.score >= PASS_SCORE:
            result["accepted"] = True
            return result
        # how: the Reviewer's feedback goes into the Writer's next round
        feedback = verdict.feedback
        result["feedback_history"].append(feedback)
        result["revision_count"] = result["revision_count"] + 1
    return result

def print_report(result: dict) -> None:
    if result["accepted"]:
        print("\nFinal article:\n")
        print(result["draft"])
    else:
        # why: never pass a rejected draft off as finished
        attempts = result["revision_count"]
        print(f"\nCouldn't agree after {attempts} revisions. Feedback:")
        number = 1
        for feedback in result["feedback_history"]:
            print(f"  round {number}: {feedback}")
            number = number + 1
        print("\nLast draft (NOT approved):\n")
        print(result["draft"])

def main() -> None:
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

**Story — `tests/integration/test_live_agents.py`:** the one check that matters most here — a weak draft must **fail**. **If not:** a Reviewer that passes everything looks exactly like one that works.

```python
# tests/integration/test_live_agents.py
# Runs the agents against the real OpenAI API.
# Run from the repo root: python tests/integration/test_live_agents.py
# Makes real API calls — needs a valid OPENAI_API_KEY in .env.
from contentforge.agents.reviewer_agent import PASS_SCORE, run_reviewer
from contentforge.config import load_config

FINDINGS = (
    "Range:\n- A battery gives 40 to 100 km per charge. [battery-review]\n"
    "Rules:\n- EU e-bike motors are limited to 25 km/h. [eu-rules]\n"
)

def test_reviewer_rejects_weak_draft() -> None:
    # case 1: a weak draft must fail — a Reviewer that passes everything
    # would never make the revision loop run
    verdict = run_reviewer(FINDINGS, "E-bikes are good.")
    passed = verdict.score >= PASS_SCORE
    print(f"case 1 (weak draft)     -> score {verdict.score}, "
          f"passed={passed}")

if __name__ == "__main__":
    load_config()
    test_reviewer_rejects_weak_draft()
```

**Run it:**

```bash
python tests/integration/test_live_agents.py
python -m contentforge.main
```

```
case 1 (weak draft)     -> score 2, passed=False
```

To see the limit, set `PASS_SCORE = 11` for one run: you should get "Couldn't agree after 3 revisions" and the full feedback list — never an endless loop.
