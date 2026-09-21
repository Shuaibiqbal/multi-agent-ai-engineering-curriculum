# Intermediate (make search conditional) — Solution

> [Back to the exercise](../README.md#ex-conditional_search) · [Hint 1](conditional_search_hints.md#hint-1) · [Hint 2](conditional_search_hints.md#hint-2) · [Solution](conditional_search_solution.md)

Read all three depths — they're not "wrong, less wrong, right," they're 3 real, valid ways to solve the same problem, with real tradeoffs between them.

## Basic Version

### Approach 1 — a keyword check

```python
# search_tool_integration_practice.py — Intermediate section
def should_search(state):
    task = state["messages"][-1].content.lower()
    keywords = ["document", "policy", "according to", "the file says"]
    if any(keyword in task for keyword in keywords):
        return "search"
    return "skip"

graph.add_conditional_edges("router", should_search, {"search": "search_node", "skip": "reason_node"})
```

### Approach 2 — asking a small model to decide

```python
# search_tool_integration_practice.py — Intermediate section
def should_search(state):
    task = state["messages"][-1].content
    prompt = "Does answering this question require looking up information in a document set? Answer only yes or no.\n\nQuestion: " + task
    answer = model.invoke(prompt).content.strip().lower()
    if "yes" in answer:
        return "search"
    return "skip"
```

Both work. Approach 1 is free and instant but easy to fool with unexpected phrasing. Approach 2 catches more phrasings but costs one extra model call on every single task.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-conditional_search) · [Hint 1](conditional_search_hints.md#hint-1) · [Hint 2](conditional_search_hints.md#hint-2) · [Solution](conditional_search_solution.md)

## Intermediate Version

### Approach 1 — a keyword check, with type hints

```python
# search_tool_integration_practice.py — Intermediate section
def should_search(state: dict) -> str:
    task = state["messages"][-1].content.lower()
    keywords = ["document", "policy", "according to", "the file says"]
    if any(keyword in task for keyword in keywords):
        return "search"
    return "skip"


graph.add_conditional_edges(
    "router",
    should_search,
    {"search": "search_node", "skip": "reason_node"},
)
```

### Approach 2 — a small classification call

```python
# search_tool_integration_practice.py — Intermediate section
from langchain_core.messages import HumanMessage


def should_search(state: dict) -> str:
    task = state["messages"][-1].content
    classification_prompt = (
        "Does answering this question require looking up information "
        "in a document set? Answer with exactly one word: yes or no.\n\n"
        f"Question: {task}"
    )
    answer = model.invoke([HumanMessage(content=classification_prompt)])
    return "search" if "yes" in answer.content.strip().lower() else "skip"


graph.add_conditional_edges(
    "router",
    should_search,
    {"search": "search_node", "skip": "reason_node"},
)
```

**Difference from Basic:** both approaches add full type hints. Approach 2's prompt is more precise about the expected answer format ("exactly one word: yes or no"), which makes the `"yes" in answer` check more reliable. Neither version yet mixes the two strategies — each one commits to keywords-only or model-call-only for every single task, which is what Advanced changes.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-conditional_search) · [Hint 1](conditional_search_hints.md#hint-1) · [Hint 2](conditional_search_hints.md#hint-2) · [Solution](conditional_search_solution.md)

## Advanced Version

### Approach 1 — a hybrid: cheap check first, model call only when ambiguous

```python
# search_tool_integration_practice.py — Intermediate section
from langchain_core.messages import HumanMessage

KEYWORDS = ["document", "policy", "according to", "the file says"]


def should_search(state: dict) -> str:
    task = state["messages"][-1].content
    lowered = task.lower()
    has_keyword = any(keyword in lowered for keyword in KEYWORDS)

    # confident hit: a clear keyword match
    if has_keyword:
        return "search"

    # confident skip: short, no keyword, no question mark
    looks_conversational = len(task.split()) <= 6 and "?" not in task
    if looks_conversational:
        return "skip"

    # ambiguous: fall through to the more expensive, more accurate check
    classification_prompt = (
        "Does answering this question require looking up information "
        "in a document set? Answer with exactly one word: yes or no.\n\n"
        f"Question: {task}"
    )
    answer = model.invoke([HumanMessage(content=classification_prompt)])
    return "search" if "yes" in answer.content.strip().lower() else "skip"


graph.add_conditional_edges(
    "router",
    should_search,
    {"search": "search_node", "skip": "reason_node"},
)
```
Most real questions hit one of the two confident branches and never pay for a model call at all — the extra round trip is spent only on the genuinely ambiguous middle, like "what's our time-off rule?", which has no keyword and isn't obviously conversational either.

### Approach 2 — logging every routing decision, for later review

A hybrid router is still a guess, and guesses are worth checking. This approach keeps Approach 1's logic unchanged, but records which branch fired and why, so misroutes can be found and fixed later instead of going unnoticed.

```python
# search_tool_integration_practice.py — Intermediate section
import logging

logger = logging.getLogger("routing")


def should_search(state: dict) -> str:
    task = state["messages"][-1].content
    lowered = task.lower()
    has_keyword = any(keyword in lowered for keyword in KEYWORDS)

    if has_keyword:
        logger.info("routed=search reason=keyword task=%r", task)
        return "search"

    looks_conversational = len(task.split()) <= 6 and "?" not in task
    if looks_conversational:
        logger.info("routed=skip reason=conversational task=%r", task)
        return "skip"

    classification_prompt = (
        "Does answering this question require looking up information "
        "in a document set? Answer with exactly one word: yes or no.\n\n"
        f"Question: {task}"
    )
    answer = model.invoke([HumanMessage(content=classification_prompt)])
    decision = "search" if "yes" in answer.content.strip().lower() else "skip"
    logger.info("routed=%s reason=model_call task=%r", decision, task)
    return decision
```
Nothing about the routing behavior changes — this is purely observability. Reviewing these logs later is how you'd actually discover, with evidence instead of a guess, whether the keyword list is missing real phrasings or the model call is being triggered far more often than expected.

**Difference from Intermediate, and between these 2 Advanced approaches:** Intermediate commits to one strategy for every task — either always the cheap check (missing some real search-needing questions) or always the model call (correct more often, but paying the cost and latency on every task, including the 90% that were obvious either way). Approach 1 fixes that by only paying for the model call on the genuinely ambiguous cases. Approach 2 doesn't change the routing decision at all — it adds a record of *why* each decision was made, which is what actually lets you improve the keyword list or the conversational heuristic later, based on real misroutes instead of guessing at them.

**Which one should you actually write?** Start with Intermediate Approach 1 (keywords only) — it's free, instant, and good enough while you're building and testing the rest of the graph. Move to Advanced Approach 1's hybrid once you've actually seen the keyword version misroute a real question in testing — don't add the model-call fallback speculatively before you've confirmed you need it. Add Approach 2's logging once this router is handling real, varied traffic (not just your own test questions) — that's the point where "which cases are being misrouted" stops being something you can answer by inspection and becomes something you need evidence for.
