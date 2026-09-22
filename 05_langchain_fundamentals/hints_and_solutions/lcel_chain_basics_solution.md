# Basic (your first LCEL chain) — Solution

> [Back to the exercise](../README.md#ex-lcel_chain_basics) · [Hint 1](lcel_chain_basics_hints.md#hint-1) · [Hint 2](lcel_chain_basics_hints.md#hint-2) · [Solution](lcel_chain_basics_solution.md)

**Story — `lcel_chain_basics_practice.py`:** this 3-piece chain — prompt, model, parser, joined with `|` — is the atom every LangChain thing you'll ever build is made of. Written here, once, on its own, so the `|` syntax and what each piece does is obvious before Doc06's tools, Doc08's RAG pipeline, or this document's own Build Task pile more onto it. **If not:** the first time you'd see `prompt | model | parser` would be inside a bigger chain already doing three other things, making it hard to tell which part the `|` syntax actually changed.

## Basic Version

### Approach 1 — the direct way

```python
# lcel_chain_basics_practice.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("Answer: {question}")
model = ChatOpenAI()
parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({"question": "What's 5 + 7?"})
print(result)
```
**Expected output:**
```
5 + 7 = 12
```

This version works correctly. It's missing an explicit model name and temperature (it relies on `ChatOpenAI()`'s hidden defaults), and it builds the pieces as separate named variables before chaining — fine for a first working version, but not quite what you'd write once the pattern feels natural.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-lcel_chain_basics) · [Hint 1](lcel_chain_basics_hints.md#hint-1) · [Hint 2](lcel_chain_basics_hints.md#hint-2) · [Solution](lcel_chain_basics_solution.md)

## Intermediate Version

### Approach 1 — a small `build_chain()` function, with explicit settings

```python
# lcel_chain_basics_practice.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


def build_chain(model_name: str = "gpt-4o-mini", temperature: float = 0.0):
    # why: model name and temperature as real parameters, not hidden
    # defaults — a model swap should be a visible, one-line decision.
    prompt = ChatPromptTemplate.from_template("Answer: {question}")
    model = ChatOpenAI(model=model_name, temperature=temperature)
    parser = StrOutputParser()
    # how: | connects the three pieces into one Runnable — the prompt's
    # output feeds the model, the model's output feeds the parser.
    return prompt | model | parser


if __name__ == "__main__":
    chain = build_chain()
    result = chain.invoke({"question": "What's 5 + 7?"})
    print(f"Answer: {result}")
```
**Expected output:**
```
Answer: 5 + 7 = 12
```

**Difference from Basic:** the model name and temperature are explicit parameters instead of hidden defaults — this matters because a model swap or a temperature change should be a visible, one-line decision, not something buried in a library default that might change between versions. Wrapping the chain-building in a function (`build_chain()`) also means this exact chain can be imported and reused elsewhere, which is exactly what this document's Build Task asks you to do.

**Which one should you actually write?** Intermediate's single-input chain is all this document's exercises and Build Task need. `chain.batch(inputs, return_exceptions=True)` is worth knowing exists the moment you're processing more than a handful of inputs through the same chain — a CSV of rows, a list of user messages to classify — where losing every result to one bad row would be a real, avoidable cost, and where requests running concurrently instead of one-by-one genuinely saves time. Not needed for a single-input chain like this one.
