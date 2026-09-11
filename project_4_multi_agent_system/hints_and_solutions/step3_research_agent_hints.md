# Step 3 — Research Agent — Hints

> [Back to this step](../README.md#step-3-a-research-agent-that-looks-things-up-before-anyone-else-works) · [Hint 1](step3_research_agent_hints.md#hint-1) · [Hint 2](step3_research_agent_hints.md#hint-2) · [Hint 3](step3_research_agent_hints.md#hint-3) · [Hint 4](step3_research_agent_hints.md#hint-4) · [Solution](step3_research_agent_solution.md)

Work through in order — don't jump ahead until you've genuinely tried.

- [Hint 1](#hint-1)
- [Hint 2](#hint-2)
- [Hint 3](#hint-3)
- [Hint 4](#hint-4)

<hr class="page-break">

> [Back to this step](../README.md#step-3-a-research-agent-that-looks-things-up-before-anyone-else-works) · [Hint 1](step3_research_agent_hints.md#hint-1) · [Hint 2](step3_research_agent_hints.md#hint-2) · [Hint 3](step3_research_agent_hints.md#hint-3) · [Hint 4](step3_research_agent_hints.md#hint-4) · [Solution](step3_research_agent_solution.md)

## Hint 1

### Simple Version

The Research agent is different from Writer and Reviewer: it actually needs to *look something up*, not just transform text it's already given. That means it needs a tool — something real (a search API) or something fake but tool-shaped (a function that returns made-up facts for a given topic, so you don't need a real API key yet to prove the agent's structure works).

Follow the same order you used for Writer: get the underlying lookup working first, then wrap it as an agent.

<hr class="page-break">

> [Back to this step](../README.md#step-3-a-research-agent-that-looks-things-up-before-anyone-else-works) · [Hint 1](step3_research_agent_hints.md#hint-1) · [Hint 2](step3_research_agent_hints.md#hint-2) · [Hint 3](step3_research_agent_hints.md#hint-3) · [Hint 4](step3_research_agent_hints.md#hint-4) · [Solution](step3_research_agent_solution.md)

### Intermediate Version

The README asks for `run_research(topic) -> ResearchNotes`. Two parts to design: the tool itself (Doc06's `@tool` decorator pattern), and the agent loop that decides to call it and then produces the final notes.

A fake lookup tool is genuinely fine here — the point of Step 3 isn't proving a real search API works, it's proving the Research agent's *shape* (tool-calling agent → structured notes output) is right, the same way Step 1 used made-up notes to prove the Writer's shape without needing Research to exist yet. Swapping a fake tool for a real search API later is a small, contained change specifically because the interface (`run_research(topic) -> ResearchNotes`) doesn't change.

`ResearchNotes` should be a structured object (Pydantic model), not a raw string — this is what lets Step 4's Analysis agent depend on a stable shape rather than parsing free text.

Sketch the tool's function signature and `ResearchNotes`'s fields before Hint 2.

<hr class="page-break">

> [Back to this step](../README.md#step-3-a-research-agent-that-looks-things-up-before-anyone-else-works) · [Hint 1](step3_research_agent_hints.md#hint-1) · [Hint 2](step3_research_agent_hints.md#hint-2) · [Hint 3](step3_research_agent_hints.md#hint-3) · [Hint 4](step3_research_agent_hints.md#hint-4) · [Solution](step3_research_agent_solution.md)

## Hint 2

### Simple Version

Pieces you need:

- `from langchain_core.tools import tool` — the `@tool` decorator from Doc06, to turn a plain function into something an agent can call.
- A fake tool function: takes a topic string, returns a few made-up fact strings about it (a small `if`/`dict` lookup, or just always returning generic placeholder facts, is fine).
- `create_react_agent` (or a similar prebuilt LangGraph agent constructor) bound to that one tool.
- A Pydantic model `ResearchNotes` with at least a `topic` field and a `facts: list[str]` field.

<hr class="page-break">

> [Back to this step](../README.md#step-3-a-research-agent-that-looks-things-up-before-anyone-else-works) · [Hint 1](step3_research_agent_hints.md#hint-1) · [Hint 2](step3_research_agent_hints.md#hint-2) · [Hint 3](step3_research_agent_hints.md#hint-3) · [Hint 4](step3_research_agent_hints.md#hint-4) · [Solution](step3_research_agent_solution.md)

### Intermediate Version

Look specifically at:

- **The `@tool` decorator with a docstring** — the docstring is not just documentation, it's what the model reads to decide *when* to call the tool, exactly as Doc06 covers. Write it like you're explaining the tool to the model, not to a human reader.
- **A fake tool is not a shortcut around learning the real pattern** — it's the same tool-calling mechanics as a real search API, just with a fake data source underneath. Everything about how the agent calls it, and how you'd swap it for `requests.get(...)` to a real search API later, stays identical.
- **`run_research(topic: str) -> ResearchNotes`** as a wrapper function, the same shape as `run_writer` and `run_reviewer` — it should call the underlying agent, then coerce/parse the final output into `ResearchNotes` (either by having the agent itself return structured output, or by having `run_research` build the object from the agent's final message).
- **Testing on made-up topics, not one you already know the "right" answer for** — the goal is confirming the *mechanism* (agent decides to call the tool, gets a result, produces notes), not fact-checking a fake tool's made-up facts.

<hr class="page-break">

> [Back to this step](../README.md#step-3-a-research-agent-that-looks-things-up-before-anyone-else-works) · [Hint 1](step3_research_agent_hints.md#hint-1) · [Hint 2](step3_research_agent_hints.md#hint-2) · [Hint 3](step3_research_agent_hints.md#hint-3) · [Hint 4](step3_research_agent_hints.md#hint-4) · [Solution](step3_research_agent_solution.md)

## Hint 3

### Simple Version

```
make a fake lookup tool:
    given a topic, return a short list of made-up facts about it

make a ResearchNotes shape: topic, facts (a list of text)

make run_research(topic):
    build an agent that has the fake tool available
    ask the agent to research the topic using the tool
    turn its answer into a ResearchNotes and return it

test:
    call run_research on 2-3 made-up topics
    check the facts list actually has something in it, and the tool really got called
```

<hr class="page-break">

> [Back to this step](../README.md#step-3-a-research-agent-that-looks-things-up-before-anyone-else-works) · [Hint 1](step3_research_agent_hints.md#hint-1) · [Hint 2](step3_research_agent_hints.md#hint-2) · [Hint 3](step3_research_agent_hints.md#hint-3) · [Hint 4](step3_research_agent_hints.md#hint-4) · [Solution](step3_research_agent_solution.md)

### Intermediate Version

```
agents/research_agent.py:
    @tool
    def lookup_facts(topic: str) -> list[str]:
        """Look up basic facts about a topic. Use this before writing any research notes."""
        return a fake but plausible list of fact strings for the topic

    class ResearchNotes(BaseModel):
        topic: str
        facts: list[str]

    def run_research(topic: str) -> ResearchNotes:
        agent = create_react_agent(ChatOpenAI(model="gpt-4o-mini"), tools=[lookup_facts])
        result = agent.invoke({"messages": [("user", f"Research this topic: {topic}")]})
        facts = extract the tool's returned facts, or parse them from the final message
        return ResearchNotes(topic=topic, facts=facts)
```

Test that `lookup_facts` genuinely gets *called* (not just that a plausible-looking answer comes back) — print the agent's intermediate messages/tool calls at least once while testing, so you know the tool-calling mechanism is really working and not just the model guessing plausible-sounding facts on its own.

<hr class="page-break">

> [Back to this step](../README.md#step-3-a-research-agent-that-looks-things-up-before-anyone-else-works) · [Hint 1](step3_research_agent_hints.md#hint-1) · [Hint 2](step3_research_agent_hints.md#hint-2) · [Hint 3](step3_research_agent_hints.md#hint-3) · [Hint 4](step3_research_agent_hints.md#hint-4) · [Solution](step3_research_agent_solution.md)

## Hint 4

### Simple Version

The fake tool, ready to use:

```python
from langchain_core.tools import tool

@tool
def lookup_facts(topic):
    """Look up basic facts about a topic."""
    return [f"{topic} is a growing area of interest.", f"{topic} has multiple viewpoints worth noting."]
```

Try building `run_research` and `ResearchNotes` around this yourself before checking the Solution.

<hr class="page-break">

> [Back to this step](../README.md#step-3-a-research-agent-that-looks-things-up-before-anyone-else-works) · [Hint 1](step3_research_agent_hints.md#hint-1) · [Hint 2](step3_research_agent_hints.md#hint-2) · [Hint 3](step3_research_agent_hints.md#hint-3) · [Hint 4](step3_research_agent_hints.md#hint-4) · [Solution](step3_research_agent_solution.md)

### Intermediate Version

The same tool, typed, with a docstring written specifically to guide the model on *when* to use it:

```python
from langchain_core.tools import tool

@tool
def lookup_facts(topic: str) -> list[str]:
    """Look up 3-5 basic, factual points about a given topic.
    Always call this before writing research notes — do not rely on your own
    general knowledge instead of this tool's results."""
    return [
        f"{topic} is a growing area of interest.",
        f"{topic} has multiple credible viewpoints worth noting.",
        f"{topic} has measurable trends worth citing with numbers.",
    ]
```

Note the explicit instruction in the docstring ("do not rely on your own general knowledge") — this matters for the same reason it mattered in Step 1's Writer prompt: without it, a capable model will sometimes skip the tool and just answer from what it already knows, which defeats the entire point of a Research agent. Build `ResearchNotes` and `run_research` yourself, then compare against the [Solution](step3_research_agent_solution.md).

<hr class="page-break">

> [Back to this step](../README.md#step-3-a-research-agent-that-looks-things-up-before-anyone-else-works) · [Hint 1](step3_research_agent_hints.md#hint-1) · [Hint 2](step3_research_agent_hints.md#hint-2) · [Hint 3](step3_research_agent_hints.md#hint-3) · [Hint 4](step3_research_agent_hints.md#hint-4) · [Solution](step3_research_agent_solution.md)

Full solution: [Show me the solution](step3_research_agent_solution.md)
