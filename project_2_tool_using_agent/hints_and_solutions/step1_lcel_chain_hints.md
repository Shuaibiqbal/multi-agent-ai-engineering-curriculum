# Step 1 — A Single LCEL Chain That Answers One Question, No Tools — Hints

> [Back to this step](../README.md#step-1-a-single-lcel-chain-that-answers-one-question-no-tools) · [Hint 1](step1_lcel_chain_hints.md#hint-1) · [Hint 2](step1_lcel_chain_hints.md#hint-2) · [Hint 3](step1_lcel_chain_hints.md#hint-3) · [Hint 4](step1_lcel_chain_hints.md#hint-4) · [Solution](step1_lcel_chain_solution.md)

Work through in order — don't jump ahead until you've genuinely tried.

- [Hint 1](#hint-1)
- [Hint 2](#hint-2)
- [Hint 3](#hint-3)
- [Hint 4](#hint-4)

<hr class="page-break">

> [Back to this step](../README.md#step-1-a-single-lcel-chain-that-answers-one-question-no-tools) · [Hint 1](step1_lcel_chain_hints.md#hint-1) · [Hint 2](step1_lcel_chain_hints.md#hint-2) · [Hint 3](step1_lcel_chain_hints.md#hint-3) · [Hint 4](step1_lcel_chain_hints.md#hint-4) · [Solution](step1_lcel_chain_solution.md)

## Hint 1

### Simple Version

"LCEL" just means "connect pieces together with `|`," the same way you'd pipe commands in a terminal. Three pieces, chained: a prompt template, the model, and something that turns the model's raw response into plain text.

This step has no tools and no loop — it's just proving that "text goes in, model answers, text comes out" works, before anything more complicated gets layered on top in Step 2.

Don't reach for an agent here at all — a plain chain is the right tool for a question the model can already answer from what it knows.

<hr class="page-break">

> [Back to this step](../README.md#step-1-a-single-lcel-chain-that-answers-one-question-no-tools) · [Hint 1](step1_lcel_chain_hints.md#hint-1) · [Hint 2](step1_lcel_chain_hints.md#hint-2) · [Hint 3](step1_lcel_chain_hints.md#hint-3) · [Hint 4](step1_lcel_chain_hints.md#hint-4) · [Solution](step1_lcel_chain_solution.md)

### Intermediate Version

The function to build:

```python
def build_simple_chain() -> Runnable:
```

It should assemble three LangChain pieces with `|`:
- A `ChatPromptTemplate` — describes the shape of the input (a system message plus a `{question}` placeholder).
- A `ChatOpenAI` instance — the actual model call.
- A `StrOutputParser` — pulls the plain string answer out of the model's response object, so callers get back `str`, not a LangChain message object.

The result of `prompt | model | parser` is itself a single `Runnable` you can call with `.invoke({"question": "..."})`.

Sketch the three pieces and how `|` connects them before writing the function body.

<hr class="page-break">

> [Back to this step](../README.md#step-1-a-single-lcel-chain-that-answers-one-question-no-tools) · [Hint 1](step1_lcel_chain_hints.md#hint-1) · [Hint 2](step1_lcel_chain_hints.md#hint-2) · [Hint 3](step1_lcel_chain_hints.md#hint-3) · [Hint 4](step1_lcel_chain_hints.md#hint-4) · [Solution](step1_lcel_chain_solution.md)

## Hint 2

### Simple Version

Here are the exact pieces you need:

- `from langchain_core.prompts import ChatPromptTemplate`
- `from langchain_openai import ChatOpenAI`
- `from langchain_core.output_parsers import StrOutputParser`
- `ChatPromptTemplate.from_messages([("system", "..."), ("human", "{question}")])`
- `ChatOpenAI(model="gpt-4o-mini")`
- Connect them: `chain = prompt | model | StrOutputParser()`
- Run it: `chain.invoke({"question": "your question here"})`

<hr class="page-break">

> [Back to this step](../README.md#step-1-a-single-lcel-chain-that-answers-one-question-no-tools) · [Hint 1](step1_lcel_chain_hints.md#hint-1) · [Hint 2](step1_lcel_chain_hints.md#hint-2) · [Hint 3](step1_lcel_chain_hints.md#hint-3) · [Hint 4](step1_lcel_chain_hints.md#hint-4) · [Solution](step1_lcel_chain_solution.md)

### Intermediate Version

Look specifically at:
- **`ChatPromptTemplate.from_messages([...])`** — a list of `(role, template_string)` tuples. `{question}` inside the human message is a placeholder LangChain fills in from the dict you pass to `.invoke()`.
- **Why a `StrOutputParser` matters:** without it, `chain.invoke(...)` hands you back an `AIMessage` object, not a plain string — fine for chaining further, but annoying for a script that just wants to `print()` the answer. `StrOutputParser` is the piece that bridges "LangChain object" to "plain Python string."
- **`.invoke()` vs `.stream()` vs `.batch()`** — every LCEL chain gets all three for free, because it implements the same `Runnable` interface regardless of what's inside it. You only need `.invoke()` for this step; keep the others in mind for later.
- **Why no tools here matters:** if you're tempted to add a tool to make the chain "more agent-like," resist it — this step exists specifically to prove the chain works in isolation, before Step 2 adds the one thing that turns it into an agent.

Write `build_simple_chain()`'s full body and a one-line `main.py` that calls `.invoke()` before moving to Hint 3.

<hr class="page-break">

> [Back to this step](../README.md#step-1-a-single-lcel-chain-that-answers-one-question-no-tools) · [Hint 1](step1_lcel_chain_hints.md#hint-1) · [Hint 2](step1_lcel_chain_hints.md#hint-2) · [Hint 3](step1_lcel_chain_hints.md#hint-3) · [Hint 4](step1_lcel_chain_hints.md#hint-4) · [Solution](step1_lcel_chain_solution.md)

## Hint 3

### Simple Version

The plan, in plain steps:

```
build a prompt template with a system message and a place for the question

build the model connection

build a parser that turns the model's reply into plain text

connect all three with | into one chain

in main.py:
    call the chain with a research question
    print the answer
```

<hr class="page-break">

> [Back to this step](../README.md#step-1-a-single-lcel-chain-that-answers-one-question-no-tools) · [Hint 1](step1_lcel_chain_hints.md#hint-1) · [Hint 2](step1_lcel_chain_hints.md#hint-2) · [Hint 3](step1_lcel_chain_hints.md#hint-3) · [Hint 4](step1_lcel_chain_hints.md#hint-4) · [Solution](step1_lcel_chain_solution.md)

### Intermediate Version

The same plan, closer to real structure:

```
chain.py:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import Runnable

    def build_simple_chain() -> Runnable:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a careful research assistant. Answer from what you know."),
            ("human", "{question}"),
        ])
        model = ChatOpenAI(model="gpt-4o-mini")
        parser = StrOutputParser()
        return prompt | model | parser

main.py:
    from chain import build_simple_chain

    chain = build_simple_chain()
    answer = chain.invoke({"question": "What is the capital of France?"})
    print(answer)
```

Notice `build_simple_chain()` takes no arguments and returns the assembled chain — it's a factory function, not something that runs the chain itself. That separation (build vs. run) is what makes it easy to reuse the same chain from `main.py`, a test file, or Step 2's agent loop later.

<hr class="page-break">

> [Back to this step](../README.md#step-1-a-single-lcel-chain-that-answers-one-question-no-tools) · [Hint 1](step1_lcel_chain_hints.md#hint-1) · [Hint 2](step1_lcel_chain_hints.md#hint-2) · [Hint 3](step1_lcel_chain_hints.md#hint-3) · [Hint 4](step1_lcel_chain_hints.md#hint-4) · [Solution](step1_lcel_chain_solution.md)

## Hint 4

### Simple Version

Here's almost the whole thing:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

def build_simple_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a careful research assistant."),
        ("human", "{question}"),
    ])
    model = ChatOpenAI(model="gpt-4o-mini")
    return prompt | model | StrOutputParser()
```

What's missing: the `Runnable` type hint, and `main.py` that builds the chain, calls `.invoke()` with a real question, and prints the answer. Add those, then check the [Solution](step1_lcel_chain_solution.md).

<hr class="page-break">

> [Back to this step](../README.md#step-1-a-single-lcel-chain-that-answers-one-question-no-tools) · [Hint 1](step1_lcel_chain_hints.md#hint-1) · [Hint 2](step1_lcel_chain_hints.md#hint-2) · [Hint 3](step1_lcel_chain_hints.md#hint-3) · [Hint 4](step1_lcel_chain_hints.md#hint-4) · [Solution](step1_lcel_chain_solution.md)

### Intermediate Version

The same idea, fully typed:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable


def build_simple_chain() -> Runnable:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a careful research assistant. Answer from what you know."),
        ("human", "{question}"),
    ])
    model = ChatOpenAI(model="gpt-4o-mini")
    return prompt | model | StrOutputParser()
```

What's missing: `main.py`. Write it yourself — build the chain, call `.invoke({"question": ...})`, print the result — then compare against the [Solution](step1_lcel_chain_solution.md).

<hr class="page-break">

> [Back to this step](../README.md#step-1-a-single-lcel-chain-that-answers-one-question-no-tools) · [Hint 1](step1_lcel_chain_hints.md#hint-1) · [Hint 2](step1_lcel_chain_hints.md#hint-2) · [Hint 3](step1_lcel_chain_hints.md#hint-3) · [Hint 4](step1_lcel_chain_hints.md#hint-4) · [Solution](step1_lcel_chain_solution.md)

Full solution: [Show me the solution](step1_lcel_chain_solution.md)
