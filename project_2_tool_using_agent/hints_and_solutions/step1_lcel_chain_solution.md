# Step 1 — A Single LCEL Chain That Answers One Question, No Tools — Solution

> [Back to this step](../README.md#step-1-a-single-lcel-chain-that-answers-one-question-no-tools) · [Hint 1](step1_lcel_chain_hints.md#hint-1) · [Hint 2](step1_lcel_chain_hints.md#hint-2) · [Hint 3](step1_lcel_chain_hints.md#hint-3) · [Hint 4](step1_lcel_chain_hints.md#hint-4) · [Solution](step1_lcel_chain_solution.md)

## Simple Version

```python
# chain.py
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

```python
# main.py
from chain import build_simple_chain

chain = build_simple_chain()
answer = chain.invoke({"question": "What is the capital of France?"})
print(answer)
```

This works. It's missing type hints and doesn't use Doc01's config/logger — both fine for proving the chain works, worth adding once you're happy with it.

<hr class="page-break">

> [Back to this step](../README.md#step-1-a-single-lcel-chain-that-answers-one-question-no-tools) · [Hint 1](step1_lcel_chain_hints.md#hint-1) · [Hint 2](step1_lcel_chain_hints.md#hint-2) · [Hint 3](step1_lcel_chain_hints.md#hint-3) · [Hint 4](step1_lcel_chain_hints.md#hint-4) · [Solution](step1_lcel_chain_solution.md)

## Intermediate Version

```python
# chain.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable


def build_simple_chain() -> Runnable:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a careful research assistant. Answer only from what you already know."),
        ("human", "{question}"),
    ])
    model = ChatOpenAI(model="gpt-4o-mini")
    parser = StrOutputParser()
    return prompt | model | parser
```

```python
# main.py
from config import load_config
from logging_setup import get_logger
from chain import build_simple_chain

config = load_config()
logger = get_logger(__name__)

chain = build_simple_chain()
question = "What is the capital of France?"

logger.info("Asking: %s", question)
answer = chain.invoke({"question": question})
logger.info("Got answer: %s", answer)
print(answer)
```

**What's different, and why it's better:** full type hints on `build_simple_chain()`, so anything importing it (Step 2's agent loop will) knows exactly what it gets back — a `Runnable`, which supports `.invoke()`, `.stream()`, and `.batch()` uniformly. It reuses Doc01's `config` and `logger`, which every later step in this project keeps building on, instead of introducing that habit later under more pressure.

**Which one should you use, and why?** The Simple version is a fine five-minute check that LCEL syntax is working. The Intermediate version is what should actually stay in the project — `build_simple_chain()`'s exact signature and return type is what Step 2 imports and wraps in a loop, so getting the interface right now saves you from changing it under Step 2's added complexity.
