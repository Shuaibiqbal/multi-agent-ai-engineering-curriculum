# Step 1 — Writer Drafting Chain — Hints

> [Back to this step](../README.md#step-1-one-specialists-drafting-logic-working-alone-no-agent-behavior) · [Hint 1](step1_writer_chain_hints.md#hint-1) · [Hint 2](step1_writer_chain_hints.md#hint-2) · [Hint 3](step1_writer_chain_hints.md#hint-3) · [Hint 4](step1_writer_chain_hints.md#hint-4) · [Solution](step1_writer_chain_solution.md)

Work through in order — don't jump ahead until you've genuinely tried.

- [Hint 1](#hint-1)
- [Hint 2](#hint-2)
- [Hint 3](#hint-3)
- [Hint 4](#hint-4)

<hr class="page-break">

> [Back to this step](../README.md#step-1-one-specialists-drafting-logic-working-alone-no-agent-behavior) · [Hint 1](step1_writer_chain_hints.md#hint-1) · [Hint 2](step1_writer_chain_hints.md#hint-2) · [Hint 3](step1_writer_chain_hints.md#hint-3) · [Hint 4](step1_writer_chain_hints.md#hint-4) · [Solution](step1_writer_chain_solution.md)

## Hint 1

### Simple Version

This step has no "agent" behavior at all yet — no loop, no tools, no deciding what to do next. It's just: text in (research notes), text out (a draft). That's exactly what an LCEL chain is for: a prompt, piped into a model, piped into something that turns the model's reply into plain text.

Three pieces, connected with `|`: a prompt template, `ChatOpenAI`, and an output parser.

<hr class="page-break">

> [Back to this step](../README.md#step-1-one-specialists-drafting-logic-working-alone-no-agent-behavior) · [Hint 1](step1_writer_chain_hints.md#hint-1) · [Hint 2](step1_writer_chain_hints.md#hint-2) · [Hint 3](step1_writer_chain_hints.md#hint-3) · [Hint 4](step1_writer_chain_hints.md#hint-4) · [Solution](step1_writer_chain_solution.md)

### Intermediate Version

The README asks for `build_writer_chain() -> Runnable`, so this is a factory function — it builds and returns the chain object, it doesn't run it. That's a deliberate design choice: the caller (Step 1's `main.py`, and later the real Writer agent) decides *when* to invoke it and with *what* input.

The chain itself is LCEL: `prompt | ChatOpenAI(...) | StrOutputParser()`. `ChatPromptTemplate.from_template(...)` takes a template string with a `{notes}` placeholder. The whole chain is invoked with `chain.invoke({"notes": some_notes_string})`.

Sketch the function signature and the prompt template's wording before moving to Hint 2.

<hr class="page-break">

> [Back to this step](../README.md#step-1-one-specialists-drafting-logic-working-alone-no-agent-behavior) · [Hint 1](step1_writer_chain_hints.md#hint-1) · [Hint 2](step1_writer_chain_hints.md#hint-2) · [Hint 3](step1_writer_chain_hints.md#hint-3) · [Hint 4](step1_writer_chain_hints.md#hint-4) · [Solution](step1_writer_chain_solution.md)

## Hint 2

### Simple Version

The exact pieces you need:

- `from langchain_core.prompts import ChatPromptTemplate`
- `from langchain_openai import ChatOpenAI`
- `from langchain_core.output_parsers import StrOutputParser`
- Build the prompt with a placeholder: `ChatPromptTemplate.from_template("Write a short draft based on these notes:\n{notes}")`
- Chain them: `prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()`

<hr class="page-break">

> [Back to this step](../README.md#step-1-one-specialists-drafting-logic-working-alone-no-agent-behavior) · [Hint 1](step1_writer_chain_hints.md#hint-1) · [Hint 2](step1_writer_chain_hints.md#hint-2) · [Hint 3](step1_writer_chain_hints.md#hint-3) · [Hint 4](step1_writer_chain_hints.md#hint-4) · [Solution](step1_writer_chain_solution.md)

### Intermediate Version

Look specifically at:

- **`Runnable` as the return type:** every LCEL chain (the piped-together object) implements the `Runnable` interface — that's what `-> Runnable` in the README's function signature means, and why `chain.invoke(...)` always works the same way regardless of what's inside the chain.
- **`ChatPromptTemplate.from_template`** vs. building messages by hand — the template form is enough here since the Writer only needs one variable input (`notes`); save `from_messages` (system + human roles) for when you actually need a system prompt with separate instructions.
- **Keeping the model config out of the caller's hands** — `build_writer_chain()` should own its own `ChatOpenAI(model=..., temperature=...)`, not accept one as an argument yet. Simpler is correct at this step.
- **`StrOutputParser()`** just extracts `.content` from the model's response as a plain string — without it, `chain.invoke(...)` would return a full `AIMessage` object instead of text.

<hr class="page-break">

> [Back to this step](../README.md#step-1-one-specialists-drafting-logic-working-alone-no-agent-behavior) · [Hint 1](step1_writer_chain_hints.md#hint-1) · [Hint 2](step1_writer_chain_hints.md#hint-2) · [Hint 3](step1_writer_chain_hints.md#hint-3) · [Hint 4](step1_writer_chain_hints.md#hint-4) · [Solution](step1_writer_chain_solution.md)

## Hint 3

### Simple Version

```
make a function build_writer_chain that returns a chain:
    make a prompt template with a {notes} spot in it
    make a chat model
    make a parser that turns the reply into plain text
    connect them with | and return the result

in main.py:
    make 2-3 fake research notes strings
    build the chain
    for each fake notes string:
        call chain.invoke with the notes
        print the draft, read it, check it's reasonable
```

<hr class="page-break">

> [Back to this step](../README.md#step-1-one-specialists-drafting-logic-working-alone-no-agent-behavior) · [Hint 1](step1_writer_chain_hints.md#hint-1) · [Hint 2](step1_writer_chain_hints.md#hint-2) · [Hint 3](step1_writer_chain_hints.md#hint-3) · [Hint 4](step1_writer_chain_hints.md#hint-4) · [Solution](step1_writer_chain_solution.md)

### Intermediate Version

```
agents/writer_chain.py:
    def build_writer_chain() -> Runnable:
        prompt = ChatPromptTemplate.from_template(...)
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        parser = StrOutputParser()
        return prompt | model | parser

main.py:
    chain = build_writer_chain()
    fake_notes = [note1, note2, note3]
    for notes in fake_notes:
        draft = chain.invoke({"notes": notes})
        print(draft)
```

Test against notes that are deliberately different in shape — short bullet points, a longer paragraph, a notes set with almost nothing in it — so you can see how the chain handles thin input before Research (Step 3) ever exists to feed it real notes.

<hr class="page-break">

> [Back to this step](../README.md#step-1-one-specialists-drafting-logic-working-alone-no-agent-behavior) · [Hint 1](step1_writer_chain_hints.md#hint-1) · [Hint 2](step1_writer_chain_hints.md#hint-2) · [Hint 3](step1_writer_chain_hints.md#hint-3) · [Hint 4](step1_writer_chain_hints.md#hint-4) · [Solution](step1_writer_chain_solution.md)

## Hint 4

### Simple Version

Here is almost the whole thing:

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

What's missing: the `-> Runnable` type hint, and `main.py`'s test calls. Add those yourself, then check the [Solution](step1_writer_chain_solution.md).

<hr class="page-break">

> [Back to this step](../README.md#step-1-one-specialists-drafting-logic-working-alone-no-agent-behavior) · [Hint 1](step1_writer_chain_hints.md#hint-1) · [Hint 2](step1_writer_chain_hints.md#hint-2) · [Hint 3](step1_writer_chain_hints.md#hint-3) · [Hint 4](step1_writer_chain_hints.md#hint-4) · [Solution](step1_writer_chain_solution.md)

### Intermediate Version

The same thing, with the type hint the README's suggested-files list actually asks for:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

def build_writer_chain() -> Runnable:
    prompt = ChatPromptTemplate.from_template(
        "Write a short draft based on these research notes:\n{notes}"
    )
    model = ChatOpenAI(model="gpt-4o-mini")
    parser = StrOutputParser()
    return prompt | model | parser
```

What's missing: `main.py`, with 2-3 made-up notes strings and a loop that invokes the chain and prints each draft. Write it yourself, then compare against the [Solution](step1_writer_chain_solution.md).

<hr class="page-break">

> [Back to this step](../README.md#step-1-one-specialists-drafting-logic-working-alone-no-agent-behavior) · [Hint 1](step1_writer_chain_hints.md#hint-1) · [Hint 2](step1_writer_chain_hints.md#hint-2) · [Hint 3](step1_writer_chain_hints.md#hint-3) · [Hint 4](step1_writer_chain_hints.md#hint-4) · [Solution](step1_writer_chain_solution.md)

Full solution: [Show me the solution](step1_writer_chain_solution.md)
