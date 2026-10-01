# Step 4 — A Verifier Agent That Catches the Worker's Bad Answers — Solution

> [Back to this step](../READING_README.md#step-4-a-verifier-agent-that-catches-the-workers-bad-answers-final-2-agents) · [Hint 1](step4_verifier_agent_hints.md#hint-1) · [Hint 2](step4_verifier_agent_hints.md#hint-2) · [Solution](step4_verifier_agent_solution.md)

**Story — Step 4:** the Worker can still be confidently wrong — misread a tool result, or answer from memory when it shouldn't. A model re-reading its own answer shares the same blind spots. This step adds a second agent with a different job and a different prompt: check the answer against what the tools really returned, and flag it if it doesn't hold up. **If not:** a wrong answer would reach the user looking exactly as trustworthy as a right one.

After this step the project is complete. Files not shown here don't change.

## Solution — a structured verdict, tool evidence, and one retry

**Story — `schemas.py`:** the Verifier's answer as a Pydantic model, so it comes back checked (Doc05's `with_structured_output`). **If not:** you'd be searching free text for "APPROVED", and "NOT APPROVED" would pass.

```python
# src/schemas.py
# The shape the Verifier must answer in: VerifierVerdict (approved,
# reason).
from pydantic import BaseModel

class VerifierVerdict(BaseModel):
    approved: bool
    reason: str
```

**Story — `prompts/verifier.txt`:** a separate, strict prompt. It never sees the Worker's instructions, so it judges the answer instead of defending it. It fills in the question, the answer and the tool evidence. **If not:** a Verifier sharing the Worker's prompt would tend to agree with it.

`src/prompts/verifier.txt`

```text
You are a strict fact checker. You did not write the answer below.
Approve it only if it really answers the question AND every fact in it
matches the evidence from the tools. If no tools were used, approve it
only if the question is general knowledge that needs no live or exact data.

Question: {question}

Evidence from tools:
{evidence}

Answer to check: {answer}
```

**Story — `agents/verifier.py`:** the Verifier chain, plus `collect_evidence()`, which passes along only what the tools *successfully* returned — not the Worker's failed attempts or retries. The Verifier judges the answer, not the effort (like a grader who sees the exam paper, not how long the student worked). **If not:** without evidence it can only guess; with the whole step log it tends to reward effort.

```python
# src/agents/verifier.py
# The Verifier agent: verify() checks the Worker's answer against the
# evidence from its tool calls, and returns a VerifierVerdict.
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.agents.worker import AgentResult
from src.schemas import VerifierVerdict
from src.utils.logger import get_logger
from src.utils.prompts import load_prompt

def build_verifier_chain(model: ChatOpenAI):
    prompt = ChatPromptTemplate.from_template(load_prompt("verifier"))
    return prompt | model.with_structured_output(VerifierVerdict)

def collect_evidence(steps: list[dict]) -> str:
    evidence = ""
    for step in steps:
        if step["error"] is None:
            line = f"- {step['tool']} returned: {step['result']}\n"
            evidence = evidence + line
    if evidence == "":
        return "(no tools were used)"
    return evidence

def verify(
    verifier_chain, question: str, result: AgentResult
) -> VerifierVerdict:
    logger = get_logger(__name__)
    verdict = verifier_chain.invoke({
        "question": question,
        "answer": result.final_answer,
        "evidence": collect_evidence(result.steps),
    })
    logger.info("verifier: approved=%s (%s)", verdict.approved, verdict.reason)
    return verdict
```

**Story — `services/research_service.py`:** the whole handoff in one function: the Worker answers, the Verifier checks, and on a rejection the Worker gets **one** retry with the Verifier's reason added to its task. The retry's answer is judged against the *original* question. (Also create an empty `services/__init__.py`.) **If not:** `main.py` would mix input handling with the agent flow, and a rejected answer would get no chance to be fixed.

```python
# src/services/research_service.py
# The flow between the agents: answer_task() runs the Worker, then the
# Verifier, and on a rejection reruns the Worker once with the reason.
from langchain_openai import ChatOpenAI

from src.agents.verifier import verify
from src.agents.worker import AgentResult, run_worker
from src.schemas import VerifierVerdict
from src.utils.logger import get_logger

def answer_task(
    model: ChatOpenAI, verifier_chain, task: str, max_iterations: int
) -> tuple[AgentResult, VerifierVerdict]:
    logger = get_logger(__name__)
    result = run_worker(model, task, max_iterations)
    verdict = verify(verifier_chain, task, result)

    if not verdict.approved:
        logger.warning("Verifier rejected the answer — retrying once")
        retry_task = (
            task
            + "\n\nA reviewer rejected your last answer because: "
            + verdict.reason
            + "\nCheck the facts with your tools and answer again."
        )
        result = run_worker(model, retry_task, max_iterations)
        verdict = verify(verifier_chain, task, result)

    return result, verdict
```

**Changed from Step 3:** `main.py` builds the Verifier chain once at startup and calls `answer_task()` instead of `run_worker()`. Every answer is now labelled verified or NOT verified. The error handling is the same.

```python
# main.py
# The file you run: python main.py
# Runs each task through answer_task() — Worker, then Verifier — and
# labels every answer verified or NOT verified.
import sys

import openai

from src.agents.verifier import build_verifier_chain
from src.config import load_config
from src.exceptions import MaxIterationsExceeded, MissingConfigError
from src.models.llm import get_model
from src.services.research_service import answer_task
from src.utils.logger import get_logger

MAX_ITERATIONS = 5

def print_steps(steps: list[dict]) -> None:
    for step in steps:
        if step["error"] is None:
            outcome = step["result"]
        else:
            outcome = "Error: " + step["error"]
        print(f"  step {step['step']}: {step['tool']}({step['arguments']})")
        print(f"          -> {outcome}")

def main() -> None:
    try:
        config = load_config()
    except MissingConfigError as e:
        print(f"Setup problem: {e}")
        sys.exit(1)

    logger = get_logger(__name__)
    model = get_model(config)
    # new in Step 4: the Verifier chain is built once, at startup
    verifier_chain = build_verifier_chain(model)
    print("ResearchHand — ask a question, or /quit to exit.")

    while True:
        task = input("You: ").strip()
        if task == "/quit":
            break
        if task == "":
            continue

        try:
            # changed in Step 4: Worker + Verifier, instead of Worker alone
            result, verdict = answer_task(
                model, verifier_chain, task, MAX_ITERATIONS
            )
        except MaxIterationsExceeded as e:
            print(f"Gave up: {e}")
            print_steps(e.steps)
            continue
        except openai.AuthenticationError:
            logger.error("Authentication failed — check OPENAI_API_KEY.")
            print("Login failed — check OPENAI_API_KEY in your .env file.")
            sys.exit(1)
        except openai.RateLimitError:
            logger.warning("Rate limited after the client's retries.")
            print("We're busy right now — wait a moment and try again.")
            continue

        print_steps(result.steps)
        # new in Step 4: the label depends on the Verifier's verdict
        if verdict.approved:
            print(f"Answer (verified): {result.final_answer}")
        else:
            print(f"Answer (NOT verified — {verdict.reason}):")
            print(f"  {result.final_answer}")

if __name__ == "__main__":
    main()
```

**Changed from Step 3:** `test_agents.py` adds case 3 for `collect_evidence()`.

```python
# tests/unit/test_agents.py
# Checks the Worker's and Verifier's helper functions with hand-made
# tool calls and steps. No API calls, no API key needed.
# Run from the repo root: python -m tests.unit.test_agents
from src.agents.verifier import collect_evidence
from src.agents.worker import ALL_TOOLS, find_tool, run_tool

def test_find_tool() -> None:
    found = find_tool(ALL_TOOLS, "celsius_to_fahrenheit")
    missing = find_tool(ALL_TOOLS, "send_email")
    print(f"case 1 (known tool)          -> {found.name}")
    print(f"case 1 (unknown tool)        -> {missing}")

def test_run_tool() -> None:
    good = {"name": "celsius_to_fahrenheit", "args": {"celsius": 0}}
    unknown = {"name": "send_email", "args": {}}
    bad_args = {"name": "celsius_to_fahrenheit", "args": {"celsius": "x"}}
    print(f"case 2 (good call)           -> {run_tool(good, ALL_TOOLS)}")
    print(f"case 2 (unknown tool)        -> {run_tool(unknown, ALL_TOOLS)}")
    result, error = run_tool(bad_args, ALL_TOOLS)
    print(f"case 2 (bad arguments)       -> result={result}, error set: "
          f"{error is not None}")

def test_collect_evidence() -> None:
    steps = [
        {"tool": "search_docs", "result": None, "error": "index down"},
        {"tool": "search_docs", "result": "Refunds within 30 days.",
         "error": None},
    ]
    print("case 3 (failed step skipped) ->")
    print(collect_evidence(steps), end="")
    print(f"case 3 (no steps)            -> {collect_evidence([])}")

if __name__ == "__main__":
    test_find_tool()
    test_run_tool()
    test_collect_evidence()
```

**Changed from Step 3:** the integration test adds cases 7 and 8. Case 7 matters most: a Verifier that has never rejected anything hasn't been tested.

**Story — cases 7 and 8:** a hand-made `AgentResult` whose tools said 64.4°F but whose answer says 90°F must be **rejected**; the same evidence with the right answer must be **approved**. **If not:** a Verifier that approves everything would look exactly like one that works.

```python
# tests/integration/test_live_agents.py
# The project's checks against the real OpenAI API (and Open-Meteo) —
# each step adds cases. Needs a valid OPENAI_API_KEY in .env.
# Run from the repo root: python -m tests.integration.test_live_agents
#   case 1 — the no-tools chain answers a question from memory
#   case 2 — a conversion uses the converter tool
#   case 3 — general knowledge needs no tool at all
#   case 4 — 1 round can't finish a tool task: MaxIterationsExceeded
#   case 5 — a live-data question uses get_weather
#   case 6 — search_docs fails once, and the Worker recovers
#   case 7 — the Verifier rejects an answer the evidence contradicts
#   case 8 — the same evidence with the right answer is approved
from langchain_openai import ChatOpenAI

from src.agents.worker import AgentResult, run_worker
# new in Step 4
from src.agents.verifier import build_verifier_chain, verify
from src.chains.direct_answer import build_direct_chain
from src.config import load_config
from src.exceptions import MaxIterationsExceeded
from src.models.llm import get_model
from src.tools.docs_search import search_state


def test_direct_answer(model: ChatOpenAI) -> None:
    chain = build_direct_chain(model)
    answer = chain.invoke({"question": "What is the capital of France?"})
    print(f"case 1 (direct answer)  -> {answer}")


def tools_used(result: AgentResult) -> list[str]:
    names = []
    for step in result.steps:
        names.append(step["tool"])
    return names


def test_conversion_uses_tool(model: ChatOpenAI) -> None:
    task = "What is 25 degrees Celsius in Fahrenheit?"
    result = run_worker(model, task, 5)
    print(f"case 2 (conversion)     -> tools: {tools_used(result)}")


def test_no_tool_needed(model: ChatOpenAI) -> None:
    result = run_worker(model, "What is the capital of France?", 5)
    print(f"case 3 (no tool needed) -> {len(result.steps)} steps: "
          f"{result.final_answer}")


def test_step_limit(model: ChatOpenAI) -> None:
    task = "What is 25 degrees Celsius in Fahrenheit?"
    try:
        run_worker(model, task, 1)
        print("case 4 (step limit)     -> WRONG, no error was raised")
    except MaxIterationsExceeded as e:
        print(f"case 4 (step limit)     -> raised, {len(e.steps)} step(s) "
              f"in the partial log")


def test_weather_uses_tool(model: ChatOpenAI) -> None:
    result = run_worker(model, "What's the weather in Lahore right now?", 5)
    print(f"case 5 (weather task)   -> tools: {tools_used(result)}")


def test_tool_failure_recovery(model: ChatOpenAI) -> None:
    search_state.call_count = 0
    result = run_worker(model, "What is your refund policy?", 5)
    failed = 0
    succeeded = 0
    for step in result.steps:
        if step["error"] is None:
            succeeded = succeeded + 1
        else:
            failed = failed + 1
    print(f"case 6 (recovery)       -> failed={failed}, "
          f"succeeded={succeeded}")
    print(f"                           {result.final_answer}")


# new in Step 4
def test_verifier_rejects_wrong_answer(verifier_chain) -> None:
    steps = [
        {"tool": "get_weather", "result": "Currently 18°C in Lahore",
         "error": None},
        {"tool": "celsius_to_fahrenheit", "result": "64.4", "error": None},
    ]
    wrong = AgentResult(final_answer="It is 90°F in Lahore.", steps=steps)
    verdict = verify(verifier_chain, "Weather in Lahore in °F?", wrong)
    if verdict.approved:
        print("case 7 (wrong answer)   -> WRONG, it was approved")
    else:
        print(f"case 7 (wrong answer)   -> OK, rejected: {verdict.reason}")

    right = AgentResult(final_answer="It is 64.4°F in Lahore.", steps=steps)
    verdict = verify(verifier_chain, "Weather in Lahore in °F?", right)
    print(f"case 8 (right answer)   -> approved={verdict.approved}")


if __name__ == "__main__":
    config = load_config()
    model = get_model(config)
    # new in Step 4
    verifier_chain = build_verifier_chain(model)
    test_direct_answer(model)
    test_conversion_uses_tool(model)
    test_no_tool_needed(model)
    test_step_limit(model)
    test_weather_uses_tool(model)
    test_tool_failure_recovery(model)
    # new in Step 4
    test_verifier_rejects_wrong_answer(verifier_chain)
```

**Story — `data/sample/tasks.json` + `scripts/compare_with_tools.py`:** asks each sample task two ways — Step 1's from-memory chain, and the Worker + Verifier — and prints both side by side. It's for *you* to read, which is why it's a script, not a test. **If not:** the project's whole claim ("verified answers, not guesses") would never be shown in one place.

`data/sample/tasks.json`

```json
{
  "tasks": [
    "What's the weather in Lahore right now, in Fahrenheit?",
    "What is your refund policy?",
    "What is the capital of France?"
  ]
}
```

```python
# scripts/compare_with_tools.py
# Asks every sample task two ways: from memory (Step 1's chain) and with
# the Worker + Verifier. Prints both, side by side, for a person to judge.
# Run from the repo root: python -m scripts.compare_with_tools
# Makes real API calls — needs a valid OPENAI_API_KEY in .env.
import json

from src.agents.verifier import build_verifier_chain
from src.chains.direct_answer import build_direct_chain
from src.config import load_config
from src.models.llm import get_model
from src.services.research_service import answer_task

SAMPLES_PATH = "data/sample/tasks.json"

def main() -> None:
    config = load_config()
    model = get_model(config)
    direct_chain = build_direct_chain(model)
    verifier_chain = build_verifier_chain(model)
    with open(SAMPLES_PATH) as samples_file:
        samples = json.loads(samples_file.read())

    for task in samples["tasks"]:
        print(f"\nTask: {task}")
        guess = direct_chain.invoke({"question": task})
        print(f"  from memory: {guess}")
        result, verdict = answer_task(model, verifier_chain, task, 5)
        print(f"  with tools:  {result.final_answer}")
        print(f"  verified:    {verdict.approved} ({verdict.reason})")

if __name__ == "__main__":
    main()
```

**Run everything:**

```bash
python -m tests.unit.test_config
python -m tests.unit.test_tools
python -m tests.unit.test_agents
python -m tests.integration.test_live_agents
python -m scripts.compare_with_tools
python main.py
```

**Expected output** of the new integration lines:

```
case 7 (wrong answer)   -> OK, rejected: The answer says 90°F, but the
                           tools returned 64.4°F.
case 8 (right answer)   -> approved=True
```

**Expected app session** (the log lines are left out; wording varies):

```
You: What's the weather in Lahore in Fahrenheit?
  step 0: get_weather({'city': 'Lahore'})
          -> Currently 18.0°C in Lahore
  step 1: celsius_to_fahrenheit({'celsius': 18.0})
          -> 64.4
Answer (verified): It's currently 64.4°F in Lahore.
```
