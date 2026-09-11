# Step 3 — Research Agent — Solution

> [Back to this step](../README.md#step-3-a-research-agent-that-looks-things-up-before-anyone-else-works) · [Hint 1](step3_research_agent_hints.md#hint-1) · [Hint 2](step3_research_agent_hints.md#hint-2) · [Hint 3](step3_research_agent_hints.md#hint-3) · [Hint 4](step3_research_agent_hints.md#hint-4) · [Solution](step3_research_agent_solution.md)

## Simple Version

```python
# agents/research_agent.py
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

@tool
def lookup_facts(topic):
    """Look up basic facts about a topic."""
    return [f"{topic} is a growing area of interest.", f"{topic} has multiple viewpoints worth noting."]

class ResearchNotes(BaseModel):
    topic: str
    facts: list

def run_research(topic):
    agent = create_react_agent(ChatOpenAI(model="gpt-4o-mini"), tools=[lookup_facts])
    result = agent.invoke({"messages": [("user", f"Research this topic using the tool: {topic}")]})
    last_message = result["messages"][-1]
    return ResearchNotes(topic=topic, facts=[last_message.content])
```

This works and proves the mechanism — an agent decides to call `lookup_facts`, gets results, and produces something you can wrap into `ResearchNotes`. It's a little sloppy about *how* the facts get extracted (dumping the whole final message into one list item), which the Intermediate version fixes.

<hr class="page-break">

> [Back to this step](../README.md#step-3-a-research-agent-that-looks-things-up-before-anyone-else-works) · [Hint 1](step3_research_agent_hints.md#hint-1) · [Hint 2](step3_research_agent_hints.md#hint-2) · [Hint 3](step3_research_agent_hints.md#hint-3) · [Hint 4](step3_research_agent_hints.md#hint-4) · [Solution](step3_research_agent_solution.md)

## Intermediate Version

```python
# agents/research_agent.py
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel


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


class ResearchNotes(BaseModel):
    topic: str
    facts: list[str]


def run_research(topic: str) -> ResearchNotes:
    agent = create_react_agent(ChatOpenAI(model="gpt-4o-mini"), tools=[lookup_facts])
    result = agent.invoke(
        {"messages": [("user", f"Research this topic using the lookup_facts tool: {topic}")]}
    )

    facts: list[str] = []
    for message in result["messages"]:
        if getattr(message, "name", None) == "lookup_facts":
            # this is the tool's own returned message — the real, structured facts
            facts.extend(message.content if isinstance(message.content, list) else [message.content])

    if not facts:
        # fall back to the agent's own summary if the tool result wasn't found this way
        facts = [result["messages"][-1].content]

    return ResearchNotes(topic=topic, facts=facts)


if __name__ == "__main__":
    for test_topic in ["electric bikes", "remote work", "specialty coffee"]:
        notes = run_research(test_topic)
        print(notes)
```

**What's different, and why it's better:** the facts are pulled directly from the tool's own returned message, not the model's final free-text summary — this means `ResearchNotes.facts` holds the real, structured tool output, which is exactly what Step 4's Analysis agent needs to depend on reliably. Full type hints. A fallback path if the tool message isn't found the expected way, instead of the whole function crashing. A real `if __name__ == "__main__":` test block against multiple made-up topics.

**Which one should you use, and why?** The Simple version is fine to confirm the agent-plus-tool wiring works at all. Switch to the Intermediate version's fact-extraction approach specifically because it's the difference between Step 4 receiving reliable, structured facts vs. one long unstructured paragraph it then has to re-parse — and Step 4's whole job is organizing raw research, which only works if what it receives is actually raw and structured, not already summarized and mixed with the agent's own commentary.
