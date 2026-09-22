# Basic (your first LCEL chain) — Hints

> [Back to the exercise](../README.md#ex-lcel_chain_basics) · [Hint 1](lcel_chain_basics_hints.md#hint-1) · [Hint 2](lcel_chain_basics_hints.md#hint-2) · [Solution](lcel_chain_basics_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried. Each hint has 2 depth levels: **Basic** (the plain idea) and **Intermediate** (proper Python). Read Basic first even if you already know Python — it's the fastest way to spot exactly what Intermediate adds.

- [Hint 1 — The idea, and the `Runnable` pattern](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

<hr class="page-break">

> [Back to the exercise](../README.md#ex-lcel_chain_basics) · [Hint 1](lcel_chain_basics_hints.md#hint-1) · [Hint 2](lcel_chain_basics_hints.md#hint-2) · [Solution](lcel_chain_basics_solution.md)

## Hint 1 — The idea, and the `Runnable` pattern {: #hint-1 }

### Basic Version

You need three pieces, connected in a row: something that builds the prompt, something that calls the model, and something that reads the reply.

A prompt template is just a sentence with a blank in it, like "Answer: {question}". You fill in the blank later, when you actually call it.

The `|` symbol connects the three pieces into one chain. Think of it like a pipe: whatever comes out of the first piece goes straight into the next one.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-lcel_chain_basics) · [Hint 1](lcel_chain_basics_hints.md#hint-1) · [Hint 2](lcel_chain_basics_hints.md#hint-2) · [Solution](lcel_chain_basics_solution.md)

### Intermediate Version

This exercise is about the `Runnable` pattern that every LCEL piece shares. A prompt template, a chat model, and an output parser are all `Runnable` objects — each one takes an input and produces an output in a predictable, swappable way.

`ChatPromptTemplate.from_template("Answer: {question}")` builds a template object — it doesn't call anything yet, it just describes the shape of the prompt, with `{question}` as a placeholder. `prompt | ChatOpenAI() | StrOutputParser()` chains three `Runnable`s together using `|`, which LangChain overloads to mean "feed this one's output into the next one's input." The result is itself a single `Runnable`, so `chain.invoke({"question": "..."})` runs all three steps and returns the final parsed answer.

The imports: `ChatPromptTemplate` and `StrOutputParser` live in `langchain_core`, while `ChatOpenAI` lives in `langchain_openai` — this is the package split the Core Concepts section describes. `ChatOpenAI()` reads its API key and default model name from your environment the same way Doc04's raw client did — pass `model=` and `temperature=` explicitly if you want to be sure which model you're using.

Worth knowing beyond `.invoke()`: the exact same chain also supports `.batch(...)` (run it on a *list* of inputs, often concurrently) and `.stream(...)` (get pieces of the output as they're produced) — for free, no extra code. Not needed for this exercise's single-input chain, but useful the moment you're processing more than a handful of inputs.

**Difference between Basic and Intermediate:** Basic and Intermediate both build and call the chain once, with `.invoke(...)`. Intermediate names the exact package each piece comes from and explains what `Runnable` actually means for each one.

<hr class="page-break">

<hr class="page-break">

> [Back to the exercise](../README.md#ex-lcel_chain_basics) · [Hint 1](lcel_chain_basics_hints.md#hint-1) · [Hint 2](lcel_chain_basics_hints.md#hint-2) · [Solution](lcel_chain_basics_solution.md)

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

### Basic Version

```
build a prompt template with one blank called question

build a chain: prompt, then the model, then a plain-text parser, joined with |

run the chain with question set to "What's 5 + 7?"

print the answer that comes back
```

Here is almost the whole thing — just try running it and reading it line by line:
```python
# lcel_chain_basics_practice.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("Answer: {question}")
chain = prompt | ChatOpenAI() | StrOutputParser()
```
**Expected output if you run just this:** nothing yet — the chain is built but never called. Add `result = chain.invoke({"question": "What's 5 + 7?"})` and `print(result)` below it.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-lcel_chain_basics) · [Hint 1](lcel_chain_basics_hints.md#hint-1) · [Hint 2](lcel_chain_basics_hints.md#hint-2) · [Solution](lcel_chain_basics_solution.md)

### Intermediate Version

```
import ChatPromptTemplate, ChatOpenAI, StrOutputParser

prompt = ChatPromptTemplate.from_template("Answer: {question}")

chain = prompt | ChatOpenAI(model="...", temperature=0) | StrOutputParser()

result = chain.invoke({"question": "What's 5 + 7?"})

print(result)
```

```python
# lcel_chain_basics_practice.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("Answer: {question}")
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chain = prompt | model | StrOutputParser()
```
Notice the input to `.invoke(...)` is a dictionary whose key (`question`) matches the template's placeholder name exactly. If they don't match, the chain fails while building the prompt, before any API call happens — you'll practice that failure directly in this document's Edge cases exercise. Add the `.invoke(...)` call and print line yourself, then compare against the [Solution](lcel_chain_basics_solution.md).

**Difference between Basic and Intermediate:** Basic calls the chain once and prints the answer. Intermediate uses explicit `model=`/`temperature=` instead of hidden defaults, and wraps chain-building in a reusable function.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-lcel_chain_basics) · [Hint 1](lcel_chain_basics_hints.md#hint-1) · [Hint 2](lcel_chain_basics_hints.md#hint-2) · [Solution](lcel_chain_basics_solution.md)

Full solution: [Show me the solution](lcel_chain_basics_solution.md)
