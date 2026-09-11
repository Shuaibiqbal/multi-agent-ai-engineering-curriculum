# Step 1 — Writer Drafting Chain — Solution

> [Back to this step](../README.md#step-1-one-specialists-drafting-logic-working-alone-no-agent-behavior) · [Hint 1](step1_writer_chain_hints.md#hint-1) · [Hint 2](step1_writer_chain_hints.md#hint-2) · [Hint 3](step1_writer_chain_hints.md#hint-3) · [Hint 4](step1_writer_chain_hints.md#hint-4) · [Solution](step1_writer_chain_solution.md)

## Simple Version

**`agents/writer_chain.py`**
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

def build_writer_chain():
    prompt = ChatPromptTemplate.from_template(
        "Write a short draft based on these research notes:\n{notes}"
    )
    model = ChatOpenAI(model="gpt-4o-mini")
    parser = StrOutputParser()
    return prompt | model | parser
```

**`main.py`**
```python
from agents.writer_chain import build_writer_chain

fake_notes = [
    "Electric bikes cost $800-3000. Battery range 20-60 miles. Growing 15%/year.",
    "Topic: remote work. Notes: productivity mixed, saves commute time, isolation a concern.",
    "Topic: coffee. Notes: arabica vs robusta, cold brew trend, price volatility.",
]

chain = build_writer_chain()
for notes in fake_notes:
    draft = chain.invoke({"notes": notes})
    print("---")
    print(draft)
```

This works and is a reasonable first version. It's missing type hints, and there's no `if __name__ == "__main__":` guard, but both are fine to skip on a genuinely first pass.

<hr class="page-break">

> [Back to this step](../README.md#step-1-one-specialists-drafting-logic-working-alone-no-agent-behavior) · [Hint 1](step1_writer_chain_hints.md#hint-1) · [Hint 2](step1_writer_chain_hints.md#hint-2) · [Hint 3](step1_writer_chain_hints.md#hint-3) · [Hint 4](step1_writer_chain_hints.md#hint-4) · [Solution](step1_writer_chain_solution.md)

## Intermediate Version

**`agents/writer_chain.py`**
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

WRITER_PROMPT = (
    "You are a content writer. Write a short, clear draft (3-5 paragraphs) "
    "based only on these research notes. Do not invent facts that aren't "
    "in the notes.\n\nResearch notes:\n{notes}"
)


def build_writer_chain() -> Runnable:
    prompt = ChatPromptTemplate.from_template(WRITER_PROMPT)
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    parser = StrOutputParser()
    return prompt | model | parser
```

**`main.py`**
```python
from agents.writer_chain import build_writer_chain

FAKE_NOTES: list[str] = [
    "Electric bikes cost $800-3000. Battery range 20-60 miles. Growing 15%/year.",
    "Topic: remote work. Notes: productivity mixed, saves commute time, isolation a concern.",
    "Topic: coffee. Notes: arabica vs robusta, cold brew trend, price volatility.",
]


def main() -> None:
    chain = build_writer_chain()
    for notes in FAKE_NOTES:
        draft = chain.invoke({"notes": notes})
        print("---")
        print(draft)


if __name__ == "__main__":
    main()
```

**What's different, and why it's better:** the prompt is pulled out into its own constant (`WRITER_PROMPT`) instead of being buried inline — makes it easy to find and tune later, which matters once Step 2 needs a second, similar prompt for redrafting with feedback. Full type hints throughout. The prompt itself is more specific — "don't invent facts not in the notes" matters a lot once Research (Step 3) starts feeding this chain real, limited information; a vague prompt tends to quietly hallucinate details to fill gaps. The `if __name__ == "__main__":` guard means `main.py` can later be imported without immediately running its test calls.

**Which one should you use, and why?** The Simple version proves the mechanism works and is fine to write first. The Intermediate version's prompt wording — telling the model explicitly not to invent facts — is not just style, it's a real correctness requirement for this specific project: Step 3's Research agent will only give the Writer limited, real information, and a Writer that happily fills gaps with invented "facts" would produce briefs the Reviewer (Step 2) should be rejecting. Fix the prompt now, while it's a one-line change, rather than after the whole team is assembled in Step 5.
