# Document 05 — LangChain Basics

> This is for self-study and live mentoring. Full plan: [CURRICULUM.md](../CURRICULUM.md#document-05-langchain-basics)

## Prerequisites
[04_openai_api](../04_openai_api/) (Project 1 done) — you'll reuse two Doc01 scripts again here, copied unchanged into `practice/build_task/`:

- `config.py` — **What:** `load_config() -> Config`. **Why:** the model choice (name, temperature) comes from config, never hardcoded. **How:** copy `01_python_foundations/practice/build_task/config.py` in as-is; don't rewrite it.
- `logging_setup.py` — **What:** `get_logger(name)`. **Why:** same consistent logging as every other document. **How:** copy `01_python_foundations/practice/build_task/logging_setup.py` in as-is; don't rewrite it.

## How to Read & Practice This Document

- **What:** building LLM calls using LangChain's tools (LCEL, prompt templates, output parsers).
- **Why:** the code you write later for real agents — including LangGraph — is built on these exact same basic pieces.
- **When:** when you need to reuse and combine many prompts or chains, not for a single one-off call (where the raw SDK is often simpler — you'll need to be able to explain which one to pick and why).
- **How to practice:**
  1. Read the material once, just to get the shape of it.
  2. Do the **Basic** exercise closed-book.
  3. Do the **Intermediate/Real-world/Edge case** exercises with notes open.
  4. Build the chain without copying Doc04's raw-SDK version — rebuild it yourself, don't paste.
  5. Use **Hint 1 → Hint 4** only after really trying. Ask for the full solution only if you say **"Show me the solution."**
  6. Before moving on, explain out loud when you'd pick LangChain over the raw SDK for a new task, and why. If you can't, you're not done.

**Jump to:** [Core Concepts](#core-concepts-read-this-first-everything-you-need-is-here) · [Practice Exercises](#practice-exercises) · [Build Task](#build-task-reusable-chain-module)

## The Story — what this document is actually building

Picture this: in Doc04 you built a chatbot by hand — building a `messages` list yourself, calling the OpenAI API yourself, reading the reply yourself, every single time. That worked, but every new feature meant rewriting the same plumbing again from scratch.

This document is about a library, LangChain, that takes exactly that repeated plumbing and turns it into small, swappable pieces you connect instead of rewrite. **First**, `ChatOpenAI` replaces your raw API call — same model, same underlying request, just a standard shape that works the same way no matter which AI provider you're actually using underneath. **Second**, a prompt template separates the fixed wording of a prompt from the parts that change each time, so the prompt itself becomes something you can log, test, and swap out — not a string you build by hand with f-strings scattered through your code. **Third**, LCEL's `|` symbol lets you snap a prompt template, a model, and an output parser together into one pipeline — `prompt | model | parser` — so calling it once runs all three steps in order, and the whole thing behaves like one reusable object. **Fourth**, the output parser is what turns the model's raw text reply into a real Python object your code can actually use, and it checks that shape *after* the model answers — a different method from Doc04's structured output, which shapes the answer *while* it's being generated.

That's the whole story: each Core Concept below is one interchangeable piece, and LCEL is the glue that snaps them together. The Build Task at the end asks you to build exactly that — one small, reusable chain module — and prove, side by side, that it gives the same answer as Doc04's raw version, so you can actually explain, not just guess, when the extra layer is worth its cost.

## Core Concepts (read this first — everything you need is here)

**Topics on this page:** [What a library gives you, and what it costs](#what-a-library-gives-you-and-what-it-costs) · [`ChatOpenAI`](#chatopenai-a-wrapper-not-a-different-model) · [Prompt templates](#prompt-templates-keeping-the-fixed-part-separate-from-the-changing-part) · [LCEL](#lcel-chaining-pieces-together-with) · [Output parsers](#output-parsers-turning-raw-text-into-a-real-python-object) · [The three LangChain packages](#the-three-langchain-packages-langchain-core-langchain-openai-langchain)

### What a library gives you, and what it costs
A **library** is code someone else already wrote and tested, so you do not write it again. In Doc04 you built every request by hand: a `messages` list, `client.chat.completions.create(...)`, then reading `.choices[0].message.content` yourself, every single time. LangChain (`prompt | model | parser`) gives you that same shape as three interchangeable pieces you connect once. It is a toolbox, not a different way of thinking about the model — the model call underneath is unchanged.

**How it really works**

- LangChain adds one layer between your code and the real API call. A bug can now be in your code, in the library's code, or in the API — one more place to look.
- LangChain 1.0 (Oct 2025) reorganized the package: old classes (`LLMChain`, `AgentExecutor`) moved out. A 2023 tutorial's imports will not match what you install today — check the date before copying code.
- The saving only shows up at scale: one script gains nothing from the wrapper. Ten scripts sharing one `ChatOpenAI` object and one parser style gain a single place to fix a bug or swap a model.
- Every `ChatOpenAI().invoke()` call is still, underneath, the same HTTP POST Doc02 taught you to wrap in a timeout and retry logic — LangChain just builds that request for you.

| Situation | What to do | Why |
|---|---|---|
| One quick, one-off call in a small script | Raw OpenAI SDK (Doc04) | Fewer layers, easier to debug |
| Many similar prompts (extract, summarize, classify) | LangChain | One shared shape; less copied code |
| You may switch model provider later | LangChain | Every chat model shares `.invoke()` |
| Building agents, RAG, or LangGraph workflows | LangChain | Doc06-Doc11 are built on these pieces |
| A brand-new API feature, day one | Raw SDK for that call | The wrapper may not support it yet |

**Common mistakes:**

- *Mistake:* reaching for LangChain on a one-line nightly script. → *Symptom:* a five-line task now has more imports than logic. → *Fix:* if you are not reusing the prompt or chain elsewhere, use the raw SDK.
- *Mistake:* copying LangChain code from an old tutorial without checking the version. → *Symptom:* `ImportError: cannot import name 'LLMChain'`. → *Fix:* rebuild with LCEL (`prompt | model | parser`) — see the packages topic below.

**Where you'll meet it:** this choice returns in [Doc06](../06_tools_function_calling/) and [Doc07](../07_ai_agents/) (tools and agents are LangChain-native), and in [Doc08](../08_rag/) and [Doc09](../09_langgraph/), which are built on these same pieces. [Project 6](../project_6_langchainpro_lcel_patterns/) is entirely about knowing when LCEL is worth it and when it is not.

**Quick cheat sheet:**

- A library saves repeated work; it costs one more layer to debug.
- One-off call → raw SDK (Doc04). Many similar prompts, agents, RAG → LangChain.
- Check the date on any LangChain tutorial — 1.0 renamed and removed a lot.
- You must be able to explain your choice, not just make it.

### `ChatOpenAI`: a wrapper, not a different model
`ChatOpenAI` sends the exact same request to the exact same model Doc04 already taught you to call — only the Python shape changes. Instead of `client.chat.completions.create(...)` you call `.invoke(messages)`; instead of a raw `response` you get an `AIMessage` with `.content` for the text. The API key, `.env` loading, and rate limits are still Doc04's rules — nothing about talking to OpenAI itself is new here.

**How it really works**

- LangChain gives every provider's chat model (OpenAI, Anthropic, Google, local) the same interface — `.invoke()`, `.stream()`, `.batch()`, the same message types. Code written for `ChatOpenAI` mostly still works if you swap in `ChatAnthropic`.
- `max_retries` here is Doc02's backoff loop, built in — LangChain retries and waits between attempts for you. Keep it small (2 is plenty); `.with_retry()` on a whole chain (see LCEL, below) is the other place retries can live, so pick one layer, not both.
- `timeout` is Doc02's rule again: never call a model with none. LLM calls need a long read timeout (the model may think 30-60+ seconds) — the same connect/read split Doc02 drew.
- `reply.usage_metadata` gives token counts the same way Doc04's `response.usage` did — same numbers, a different attribute name. Log them with Doc01's `get_logger`, and Doc03's cost formula still applies unchanged.
- `.stream()` yields `AIMessageChunk` pieces you can add together with `+` — the same chunked-reply idea as Doc04's `delta.content`, except LangChain joins the pieces for you instead of you guarding every chunk with `or ""`.
- Errors raised through `ChatOpenAI` are the same named exceptions Doc04 taught — `RateLimitError`, `AuthenticationError`, `APITimeoutError` — LangChain does not invent new ones. Catch them the same way: permanent (401/400) don't retry, temporary (429/timeout/5xx) retry with backoff (Doc02's groups).
- Printing `reply` instead of `reply.content` dumps the whole `AIMessage` object (`content='...' response_metadata={...}`) — an easy, harmless-looking bug.

| Setting | What it does | When to set it |
|---|---|---|
| `model` | Which model to call | Always — from config (Doc01), never hardcoded |
| `temperature` | How random the answer is | `0` for extraction/classification, higher for creative writing |
| `timeout` | Max seconds to wait | Always — Doc02's rule, no exceptions |
| `max_retries` | Retries on failure | Small (`2`); one retry layer only |
| `api_key` | Which key to use | Usually leave out — reads `OPENAI_API_KEY`, same as Doc04 |

**Common mistakes:**

- *Mistake:* thinking `ChatOpenAI` is a smarter or different model. → *Symptom:* a wrong answer with the raw SDK is still wrong here — fixing the wrapper changes nothing. → *Fix:* fix the prompt or the model choice, not the wrapper.
- *Mistake:* `print(reply)` instead of `print(reply.content)`. → *Symptom:* your UI or log shows `content='...' response_metadata=...` instead of clean text. → *Fix:* always read `.content` for the text.

**Where you'll meet it:** every later document that calls a model. [Doc06](../06_tools_function_calling/) attaches tools with `.bind_tools(...)`; [Doc07](../07_ai_agents/) passes it to `create_agent(...)`; [Doc11](../11_multi_agent_systems/) often gives each agent its own `ChatOpenAI` — a cheap model for routing, a stronger one for writing.

**Quick cheat sheet:**

- Same OpenAI model as Doc04 — only the Python shape is new.
- `.invoke()` returns an `AIMessage` — use `.content` for the text.
- Always set `model` (from config), `timeout`, and a small `max_retries`.
- `.stream()` for live typing, `.batch()` for many inputs at once.
- One retry layer: either `max_retries` here, or `.with_retry()` on the chain — not both.

### Prompt templates: keeping the fixed part separate from the changing part
A **prompt template** is a prompt with empty slots — fixed wording written once, changing parts named in curly braces like `{text}`, filled in each call. Think of it like a form letter: the boilerplate is printed once, only the blanks change per recipient. `ChatPromptTemplate.from_template("Extract the {field} from: {text}")` replaces building the string by hand with f-strings scattered through your code, and turns the prompt into a real object you can log, version, and test without spending a token.

**How it really works**

- `.from_template(...)` builds one human message; `.from_messages([...])` builds a full list, keeping system rules separate from user input — the same separation Doc04 taught you to keep between the `system` message and the `user` turns.
- `MessagesPlaceholder("history")` drops a whole list of past messages into one slot — this is how a chat prompt carries Doc03's "no memory, resend everything" rule.
- `prompt.invoke({...})` only fills slots and returns messages — no API call, no cost — so you can test a prompt for free before it ever reaches the model.
- A missing slot raises `KeyError` at build time, before any call goes out — cheaper than sending a broken prompt and puzzling over a strange answer three functions later.
- Extra keys you pass but the template doesn't use are silently ignored, so a typo'd key (`"qestion"`) shows up as a *missing* variable, not an extra one.
- Real curly braces in the text (a JSON example) must be doubled — `{{` and `}}` — or LangChain reads them as slot names and raises a confusing "missing variable" error.
- `.partial(...)` pre-fills one slot (commonly a parser's format instructions) so the caller only supplies the rest.

| Situation | What to do | Why |
|---|---|---|
| One simple message with slots | `from_template(...)` | Shortest; becomes one human message |
| System rules + user input | `from_messages([...])` | Keeps rules apart from what changes |
| Chat history in the prompt | `MessagesPlaceholder("history")` | Carries Doc03's resend-everything memory |
| JSON example inside the text | Double the braces: `{{` `}}` | Single braces are read as a slot |
| Same template reused everywhere | Keep it in `prompts.py`, import it | One place to change and review |

**Common mistakes:**

- *Mistake:* writing a JSON example with single braces, like `Reply as {"name": "..."}`. → *Symptom:* a confusing error naming a "missing variable" that is actually part of your JSON. → *Fix:* double every real brace — `{{` and `}}`.
- *Mistake:* renaming a template variable but not the code that fills it. → *Symptom:* `KeyError` at `.invoke()`, or a typo'd key silently treated as missing. → *Fix:* keep the template and its caller close, or import the exact slot names from one place.

**Where you'll meet it:** this document's Build Task (`prompts.py`). [Doc08](../08_rag/) uses a template with `{context}` and `{question}` slots to answer from company documents. In [Doc11](../11_multi_agent_systems/) each agent has its own named system prompt, easy to see and change. [Project 9](../project_9_promptshield_injection_defense/) is built on why user text must go into a slot and never get mixed into the system rules.

**Quick cheat sheet:**

- Fixed words in the template; changing parts in `{slots}`.
- `from_template` for one message; `from_messages` for system + human.
- `MessagesPlaceholder("history")` for chat history.
- Real braces in the text → double them: `{{` `}}`.
- `prompt.invoke({...})` fills slots only — free, no API call.

### LCEL: chaining pieces together with `|`
**LCEL** (LangChain Expression Language) connects pieces with the `|` symbol: `chain = prompt | model | parser`. Calling `chain.invoke(inputs)` runs each step in order, feeding one step's output straight into the next. Every piece — and the whole chain — is a `Runnable`: anything with `.invoke()`, `.stream()`, `.batch()`, and async versions ([Doc08b](../08b_async_prereq/)). So a three-step chain behaves exactly like one single step: you can pass it around, nest it inside a bigger chain, and bolt on retries in one line, instead of writing the same glue code for every new chain.

**How it really works**

- `a | b` makes a new `Runnable` that runs `a`, then hands its result to `b` — no hidden magic beyond that; every piece takes one input and returns one output.
- A plain Python function becomes a Runnable step automatically; a `dict` becomes a step that runs each value in parallel and returns a dict of results (`RunnableParallel`).
- `RunnablePassthrough` keeps the original input alive for a later step — the standard way RAG ([Doc08](../08_rag/)) keeps the user's question next to the retrieved context.
- `.with_retry(stop_after_attempt=3)` is Doc02's backoff loop, built into the chain itself — LCEL does natively what Doc02 built by hand with a `for` loop and `time.sleep`. Pick exactly one retry layer: the chain's `.with_retry()`, the model's `max_retries`, or your own loop — never two, same rule Doc02 and Doc04 both taught.
- `.with_fallbacks([backup_chain])` swaps in a second chain — a cheaper model, a different prompt — when the first one raises. One layer above a single retry: retry the same thing again, fall back to something different.
- A broken `|` connection (`model | prompt` — the prompt expects a `dict`, the model returns an `AIMessage`) fails deep inside LangChain with a confusing type error. Debug by running each piece alone: `prompt.invoke(inputs)`, then `model.invoke(that_result)`.

| Situation | What to do | Why |
|---|---|---|
| Steps run one after another | `a \| b \| c` | Simple, readable pipeline |
| Your own code in the middle | A function, or `RunnableLambda` | Reshape data between steps |
| Two independent tasks, same input | `RunnableParallel` (or a `dict`) | Run at the same time — faster |
| Keep the original input for later | `RunnablePassthrough` | A later step still needs the first input |
| API fails for a moment | `.with_retry(...)` | Doc02's backoff, built in — one retry layer only |
| Main model down or too slow | `.with_fallbacks([...])` | Backup chain instead of a failed call |

**Common mistakes:**

- *Mistake:* connecting two pieces whose shapes don't match, like `model | prompt`. → *Symptom:* a confusing type error deep inside LangChain, mentioning `AIMessage` or `dict` at a step boundary. → *Fix:* for each `|`, check what the left side returns and what the right side accepts; run pieces alone to isolate it.
- *Mistake:* `.with_retry()` on the chain **and** `max_retries` on the model **and** your own loop. → *Symptom:* one real failure turns into far more calls than your logs show — Doc02's retry-stacking mistake, one layer higher. → *Fix:* pick exactly one retry layer.

**Where you'll meet it:** this document's Build Task (`build_extraction_chain() -> Runnable`). [Project 6](../project_6_langchainpro_lcel_patterns/) is entirely LCEL patterns — parallel steps, retry, and fallbacks in a support pipeline. [Doc08](../08_rag/)'s RAG chain is `{"context": retriever, "question": RunnablePassthrough()} | prompt | model | parser`. [Doc09](../09_langgraph/) and [Doc11](../11_multi_agent_systems/)'s graphs are Runnables too, called with the same `.invoke()` you learn here.

**Quick cheat sheet:**

- `a | b` = run `a`, hand its output to `b`. Nothing more.
- Every chain is a `Runnable`: `.invoke()`, `.stream()`, `.batch()`, `.ainvoke()`.
- `RunnableParallel`/`dict` for parallel steps; `RunnablePassthrough` to keep the input.
- `.with_retry()` = Doc02's backoff, built in. `.with_fallbacks()` = a backup chain.
- One retry layer only — chain, model, or your own loop, never two.

### Output parsers: turning raw text into a real Python object
An **output parser** is the last step of a chain — it turns the model's reply into a real Python value your code can use: a `str`, a `dict`, or a Pydantic object. `StrOutputParser` pulls out the text. `PydanticOutputParser` checks the reply against a Pydantic model and raises a named `OutputParserException` when it doesn't match. This is the same problem Doc02's JSON topic taught you about raw HTTP responses — text that parses fine but is still the wrong shape — just showing up in an LLM's reply instead of an API's.

**How it really works**

- Two different methods, and you must know which one a chain uses. **Check after**: the prompt asks for a shape in words, the model writes free text, the parser checks it afterward — works with any model, but the model can still get the shape wrong. **Shape during**: `model.with_structured_output(Model)` uses the provider's constrained decoding — the exact mechanism Doc04's structured-output topic explained — so the shape is enforced while the model writes, and LangChain hands you the parsed object directly.
- `PydanticOutputParser` needs `parser.get_format_instructions()` inserted into the prompt (usually via `.partial(...)`), or the model never learns what shape to write.
- A parser failure is `OutputParserException` (Pydantic's `ValidationError` underneath) — catch it near the call with a clear message, the same discipline Doc04 taught for a refusal or `LengthFinishReasonError`, never a bare `except`.
- Right shape is not the same as right values — a parser lets `{"price": 0}` through because `0` is a valid `int`. Add a Pydantic `field_validator` for business rules the schema can't express, same fix Doc04's structured-output topic gave.
- A mismatched prompt and parser (prompt asks for tags, chain ends in an `Order` parser) fails on every call, or — with a loose `JsonOutputParser` — quietly returns the wrong type instead of erroring.

| Situation | What to do | Why |
|---|---|---|
| Only need the text | `StrOutputParser()` | `AIMessage` → plain `str` |
| Typed object, model supports it | `model.with_structured_output(Model)` | Doc04's constrained decoding — fewest shape errors |
| No structured-output support | `PydanticOutputParser(pydantic_object=Model)` | Works with any text model; checks after |
| A loose, quick `dict` | `JsonOutputParser()` | Less strict, good for quick tools |
| Shape can fail, user is waiting | Catch `OutputParserException` / `ValidationError` | Show a clean message, don't crash |

**Common mistakes:**

- *Mistake:* prompt and parser describing different shapes — prompt says "list the tags," chain ends in an `Order` parser. → *Symptom:* every call fails, or a loose parser quietly returns the wrong type. → *Fix:* make the prompt's format instructions and the parser's model describe the same shape.
- *Mistake:* treating a parsed object as a correct one. → *Symptom:* `{"price": 0}` passes because `0` is a valid `int`, but it's still wrong. → *Fix:* add a Pydantic `field_validator` — shape is guaranteed, truth is not (Doc04).

**Where you'll meet it:** this document's Intermediate and Failure exercises, and the Build Task, compared against Project 1's structured output. [Doc06](../06_tools_function_calling/)'s tool arguments use the same Pydantic check. In [Doc11](../11_multi_agent_systems/) and [Project 4](../project_4_contentforge_multi_agent/), agents hand each other typed objects (a reviewer's `approved: bool`); a parser failure here is the handover point breaking — Doc02's "valid JSON, wrong shape" problem, one layer up.

**Quick cheat sheet:**

- Model gives text; parser gives a Python value.
- `StrOutputParser` → `str`. `PydanticOutputParser`/`with_structured_output` → typed object.
- "Check after" can fail — catch `OutputParserException`.
- `with_structured_output` = Doc04's constrained decoding, same guarantee.
- Shape is not truth — add validators for values the schema can't check.

### The three LangChain packages: `langchain-core`, `langchain-openai`, `langchain`
LangChain is not one package — it splits into `langchain-core`, `langchain-openai` (or another provider), and `langchain`, each installed separately with `pip` but sharing one naming quirk: install with a dash (`pip install langchain-core`), import with an underscore (`from langchain_core import ...`). Splitting it this way means a small extraction service installs only what it needs, and provider-specific code updates without touching the core — the same reason Doc01 taught pinned, minimal `requirements.txt` files.

**How it really works**

- `langchain-core`: the building blocks — `Runnable`, messages, prompt templates, output parsers, `@tool`. Very few dependencies.
- `langchain-openai` (and siblings `langchain-anthropic`, `langchain-google-genai`): provider-only pieces, `ChatOpenAI`/`OpenAIEmbeddings`. Swapping providers means changing this one import, not your prompts or parsers.
- `langchain`: high-level tools built on the other two — `create_agent` (built on LangGraph), `init_chat_model`. `langgraph` is its own separate package again.
- LangChain 1.0 (October 2025) shrank `langchain` down to agents and a few helpers. Old classes (`LLMChain`, `RetrievalQA`, `AgentExecutor`) moved to `langchain-classic`. A tutorial importing `from langchain.chains import LLMChain` predates this — rebuild with LCEL (`prompt | model | parser`) or `create_agent` instead.
- Mixed major versions across the `langchain-*` packages (core 1.x with openai 0.1.x) produce `ImportError`s that look like bugs in your own code. Check with `pip list | grep langchain` — all packages should share a major version — and pin them together in `requirements.txt`, the same Doc01 pinning discipline.

| Situation | What to do | Why |
|---|---|---|
| Chains with prompts, models, parsers | `langchain-core` + `langchain-openai` | All LCEL needs |
| Building agents ([Doc06](../06_tools_function_calling/)/[Doc07](../07_ai_agents/)) | Also install `langchain` | `create_agent` lives there |
| Building graphs ([Doc09](../09_langgraph/)) | Also install `langgraph` | Its own package |
| A vector store or loader ([Doc08](../08_rag/)) | Install that one integration package | Keeps other integrations out |
| Old code imports `LLMChain`/`AgentExecutor` | Rewrite with LCEL / `create_agent` | Removed from `langchain` 1.0 |

**Common mistakes:**

- *Mistake:* upgrading only one `langchain-*` package. → *Symptom:* strange `ImportError`s or missing attributes that look like your own bug. → *Fix:* `pip list | grep langchain` — upgrade and pin them together.
- *Mistake:* copying an old tutorial's `from langchain.chains import LLMChain`. → *Symptom:* `ImportError: cannot import name 'LLMChain'` on a fresh install. → *Fix:* rebuild with LCEL, or `create_agent` for agents — check the tutorial's date first.

**Where you'll meet it:** every `requirements.txt` from here on, and the top of every file in Doc06-Doc11 and the projects. [Project 11](../project_11_mcpcrew_multi_agent_mcp/) and [Project 13](../project_13_codeguard_pr_review/)'s real code mixes imports from all three packages plus `langgraph` in one file — each import line tells you which layer that piece comes from.

**Quick cheat sheet:**

- `langchain-core` = building blocks. `langchain-openai` = provider. `langchain` = agents/helpers. `langgraph` = graphs.
- Install with a dash, import with an underscore.
- `LLMChain`/`AgentExecutor` are gone from 1.0 — use LCEL and `create_agent`.
- Upgrade and pin all `langchain-*` packages together.

## Go Deeper (Optional)
_You don't need any of these to understand the Core Concepts above — use them if you want a second explanation or more detail._

- [LangChain — Introduction](https://python.langchain.com/docs/introduction/) — what LangChain is, and isn't.
- [LangChain — Concepts hub](https://python.langchain.com/docs/concepts/) — start with chat models, prompt templates, LCEL, output parsers.
- [LangChain Academy](https://academy.langchain.com/) — a free official course; do the intro alongside this document.

## Practice Exercises

**Setup:** same venv as before — if it's not active, `source ../01_python_foundations/.venv/bin/activate` (or your own venv for this folder). New package for this document: `pip install langchain langchain-openai langchain-core`.

**Where your code lives:** all of it under `05_langchain_fundamentals/practice/` (`mkdir -p practice`), never loose beside this README — same convention as Doc01, Doc02, and Doc04. Exercises are grouped **by topic, not by level**.

**The full file layout, all exercises:**

```
practice/
├── lcel_chain_basics_practice.py    Basic
├── structured_output_practice.py    Intermediate + Failure (two sections)
├── lcel_vs_raw_sdk_practice.py      Real-world
├── prompt_template_practice.py      Edge cases
└── build_task/                      Build Task — its own folder
    ├── chain.py                     build_extraction_chain() -> Runnable
    ├── prompts.py                   PromptTemplate/ChatPromptTemplate
    ├── compare_with_raw_sdk.py      runs both versions, prints the diff
    ├── config.py                    copied from 01_python_foundations, unchanged
    └── logging_setup.py             copied from 01_python_foundations, unchanged
```

**Why each script exists:**

- `lcel_chain_basics_practice.py` — the 3-piece chain every LangChain thing you'll build is made of.
- `structured_output_practice.py` — feels, directly, the difference between after-the-fact parser checking and during-generation structured output.
- `lcel_vs_raw_sdk_practice.py` — the only way to actually compare LangChain vs. raw SDK is having both versions side by side.
- `prompt_template_practice.py` — knowing whether a broken template fails while building the prompt or only once the call goes out changes how fast you can debug it.
- `build_task/chain.py` / `build_task/prompts.py` — the one chain module every later document imports instead of writing raw SDK calls again.
- `build_task/compare_with_raw_sdk.py` — proves the LCEL version and Doc04's raw version genuinely agree, not just look similar.
- `build_task/config.py` / `build_task/logging_setup.py` — copied unchanged from Doc01, same settings/logging behavior as every other document.

**For this document, save your practice code as:**

- **Basic** (your first LCEL chain) is its own topic — save it as `practice/lcel_chain_basics_practice.py`.
- **Intermediate** (swap in a structured parser) and **Failure** (force the parser to actually fail) are both about structured-output parsing and its errors — save them together as `practice/structured_output_practice.py`, one section per level.
- **Real-world** (rebuild a Project 1 feature, LCEL-style) is its own topic — save it as `practice/lcel_vs_raw_sdk_practice.py`.
- **Edge cases** (a template with the wrong variables) is its own topic — save it as `practice/prompt_template_practice.py`.

Why group by topic instead of by level: if you save each exercise by difficulty level instead, the different versions of the same idea end up scattered across separate files, and you can never see how one topic grows from simple to harder in one place. Grouping by topic keeps that growth visible — open one file, and you see the whole journey for that one thing, from basic to advanced, side by side.

**Jump to an exercise:** [Basic](#ex-lcel_chain_basics) · [Intermediate](#ex-structured_parser_swap) · [Real-world](#ex-lcel_vs_raw_sdk) · [Edge cases](#ex-template_variable_errors) · [Failure](#ex-parser_failure_handling) · [Build Task](#build-task-reusable-chain-module)

### Basic — your first LCEL chain {: #ex-lcel_chain_basics }

- **What:** connect a prompt template → `ChatOpenAI` → text output parser with `|`.
- **Why:** this 3-piece chain is the atom every LangChain thing you'll ever build is made of — get comfortable with it before adding anything else.
- **How to code it:** `prompt = ChatPromptTemplate.from_template("Answer: {question}")`, `chain = prompt | ChatOpenAI() | StrOutputParser()`, then `chain.invoke({"question": "..."})`.
- **Save as:** `practice/lcel_chain_basics_practice.py`.
- **Builds on:** Doc04's Basic exercise (`practice/chat_api_basics_practice.py`) — the same first call, now split into a prompt, a model, and a parser instead of one raw `client.chat.completions.create(...)`.
- **Used later by:** the [Real-world exercise](#ex-lcel_vs_raw_sdk) below and the [Build Task](#build-task-reusable-chain-module) — this exact three-piece shape, reused.
- **Stuck?** [Hint 1](hints_and_solutions/lcel_chain_basics_hints.md#hint-1) · [Hint 2](hints_and_solutions/lcel_chain_basics_hints.md#hint-2) · [Show me the solution](hints_and_solutions/lcel_chain_basics_solution.md)

### Intermediate — swap in a structured parser {: #ex-structured_parser_swap }

- **What:** replace the text parser with a Pydantic/structured one, and see what happens when the model's answer doesn't match the shape.
- **Why:** this is where you feel, directly, the difference between LCEL's after-the-fact parser checking and Doc04's during-generation structured output.
- **How to code it:** define a small Pydantic model, use `.with_structured_output(YourModel)` on the chat model, run it on a clearly-matching input, then a deliberately mismatched one — read the exact error.
- **Save as:** `practice/structured_output_practice.py`, under an `# Intermediate` section (this file also holds the [Failure exercise](#ex-parser_failure_handling) below, in its own `# Failure` section).
- **Builds on:** the [Basic exercise](#ex-lcel_chain_basics)'s chain, and Doc04's structured-output topic — `.with_structured_output(Model)` is the exact same constrained-decoding call, just reached through LangChain.
- **Used later by:** the [Failure exercise](#ex-parser_failure_handling) right below (same file), and the [Build Task](#build-task-reusable-chain-module)'s parser choice.
- **Stuck?** [Hint 1](hints_and_solutions/structured_parser_swap_hints.md#hint-1) · [Hint 2](hints_and_solutions/structured_parser_swap_hints.md#hint-2) · [Show me the solution](hints_and_solutions/structured_parser_swap_solution.md)

### Real-world — rebuild a Project 1 feature, LCEL-style {: #ex-lcel_vs_raw_sdk }

- **What:** take one feature from Project 1 (the raw-SDK version) and rebuild it with LCEL, keeping both versions.
- **Why:** this is the only way to actually compare LangChain vs. raw SDK — reading about the trade-off isn't the same as having both versions of the same feature side by side.
- **How to code it:** copy Project 1's structured-extraction feature into a new file, rewrite it as prompt → model → parser with `|`, then write a script that runs both on the same 3 inputs and diffs the outputs.
- **Save as:** `practice/lcel_vs_raw_sdk_practice.py`.
- **Builds on:** [Doc04](../04_openai_api/)'s Project 1 structured-extraction feature (the raw-SDK version), and the [Basic exercise](#ex-lcel_chain_basics)'s chain shape.
- **Used later by:** the [Build Task](#build-task-reusable-chain-module)'s `compare_with_raw_sdk.py`, which **copies** this same comparison almost unchanged.
- **Stuck?** [Hint 1](hints_and_solutions/lcel_vs_raw_sdk_hints.md#hint-1) · [Hint 2](hints_and_solutions/lcel_vs_raw_sdk_hints.md#hint-2) · [Show me the solution](hints_and_solutions/lcel_vs_raw_sdk_solution.md)

### Edge cases — a template with the wrong variables {: #ex-template_variable_errors }

- **What:** a prompt template missing a variable it needs, and one given an extra variable it doesn't use — see what fails, and exactly when.
- **Why:** knowing whether a broken template fails *while building the prompt* or *only once the API call goes out* changes how fast you can debug it.
- **How to code it:** call `.invoke({})` on a template expecting `{question}` — read the exact error. Then call it with `{"question": "...", "extra": "..."}` and confirm whether it's silently ignored or errors.
- **Save as:** `practice/prompt_template_practice.py`.
- **Builds on:** the [Basic exercise](#ex-lcel_chain_basics)'s prompt template — same template, now testing its failure modes instead of the happy path.
- **Used later by:** the [Build Task](#build-task-reusable-chain-module)'s `prompts.py`, which must fail the same clear way.
- **Stuck?** [Hint 1](hints_and_solutions/template_variable_errors_hints.md#hint-1) · [Hint 2](hints_and_solutions/template_variable_errors_hints.md#hint-2) · [Show me the solution](hints_and_solutions/template_variable_errors_solution.md)

### Failure — force the parser to actually fail {: #ex-parser_failure_handling }

- **What:** ask the model something that won't fit your Pydantic shape on purpose, and read the real error the parser raises.
- **Why:** you need to know, before it happens in production, exactly what kind of exception your code needs to catch here.
- **How to code it:** ask a structured-output chain expecting a number field for something that's clearly a description, not a number — catch the resulting error and print its type.
- **Save as:** `practice/structured_output_practice.py`, under a `# Failure` section (this file also holds the [Intermediate exercise](#ex-structured_parser_swap) above, in its own `# Intermediate` section).
- **Builds on:** the [Intermediate](#ex-structured_parser_swap) section of this same file, and Doc04's error-handling habit — catch the specific parser exception, never a bare `except`.
- **Used later by:** the [Build Task](#build-task-reusable-chain-module)'s requirement to handle a bad structured-output reply gracefully.
- **Stuck?** [Hint 1](hints_and_solutions/parser_failure_handling_hints.md#hint-1) · [Hint 2](hints_and_solutions/parser_failure_handling_hints.md#hint-2) · [Show me the solution](hints_and_solutions/parser_failure_handling_solution.md)

## Build Task — Reusable Chain Module
**Stuck on the Build Task?** [Hint 1](hints_and_solutions/build_task.md#hint-1) · [Hint 2](hints_and_solutions/build_task.md#hint-2) · [Show me the solution](hints_and_solutions/build_task.md#solution)

**Goal:** a small chain module that later documents will reuse instead of writing raw SDK calls each time — a comparison point next to Project 1, not a replacement for it.

**Requirements:**

- One LCEL chain that wraps a prompt template, a model, and a parser as one callable piece.
- The model choice (name, temperature) comes from your config — never hardcoded — using Doc01's `config.py`/`get_logger(name)`, copied in unchanged the way Doc04's Build Task did.
- A side-by-side test/script that proves your LCEL version and Doc04's raw-SDK version give the same answer for the same input.

**Inputs:** the same structured-extraction task as Project 1's structured-output feature.

**Outputs:** the same typed object as Project 1's, but built a different way.

**Constraints:** don't delete or replace the Doc04 raw version — you need both, to compare them and to answer the interview question "when would you use which."

```
05_langchain_fundamentals/practice/build_task/
├── chain.py              build_extraction_chain() -> Runnable
├── prompts.py            PromptTemplate/ChatPromptTemplate
├── compare_with_raw_sdk.py  runs both versions, prints the diff
├── config.py             copied from 01_python_foundations's Build Task
└── logging_setup.py      copied from 01_python_foundations's Build Task
```

- `chain.py` / `prompts.py` — **What/Why:** the one chain module every later document imports instead of writing raw SDK calls again.
- `compare_with_raw_sdk.py` — **What/Why:** proves the LCEL version and Doc04's raw version genuinely agree, not just look similar — also doubles as this Build Task's test file.
- `config.py` / `logging_setup.py` — **What/Why:** copied unchanged from Doc01, so this module uses the exact same settings/logging behavior as every other document.

**Run it:** `cd practice/build_task && python compare_with_raw_sdk.py` — from inside the folder, so `from config import load_config` finds the file next to it.

**Builds on:** Doc01's Build Task `config.py`/`get_logger(name)` — **copy** both in unchanged, same as Doc04 did. Doc04's Project 1 structured-extraction feature — the same task, rebuilt with LCEL. The [Basic](#ex-lcel_chain_basics), [Intermediate](#ex-structured_parser_swap), [Real-world](#ex-lcel_vs_raw_sdk), and [Edge cases](#ex-template_variable_errors) exercises above — fold their chain, parser, comparison script, and template checks into this one module.

**Used later by:** [Doc06](../06_tools_function_calling/) attaches tools to this same `ChatOpenAI` object with `.bind_tools(...)`; [Doc08](../08_rag/) reuses this LCEL chain shape for its RAG pipeline; [Project 6](../project_6_langchainpro_lcel_patterns/) builds directly on this chain, adding retries and fallbacks on top.

**Functions/Components to build:**

- `prompts.py` → the `PromptTemplate`/`ChatPromptTemplate`
- `chain.py` → `build_extraction_chain() -> Runnable`
- `compare_with_raw_sdk.py` → runs both versions on the same inputs, prints the difference

## Expected Behavior

- The chain gives the same structured object as Project 1's raw version, for the same input.
- Changing the prompt template's variables shouldn't require touching the chain-building code.

## Test Cases

| Scenario | Expected |
|---|---|
| A well-formed input | Chain and raw-SDK results match |
| A missing template variable | A clear error while building the prompt, not silently left blank |
| The model's answer doesn't fit the shape | The parser raises a clear, named, catchable error |

## Break-It / Debug Preview

- A chain that quietly returns the wrong Python type, because the parser doesn't actually match what the prompt asks for.
- Full debugging drill in [14_debugging_lab](../14_debugging_lab/).

## Interview Topics Preview

- When LangChain is worth its cost vs. when the raw SDK is simpler and easier to debug · what LCEL actually connects when it runs · `langchain-core` vs. `langchain-openai` vs. `langchain`.

## Move On When
You can decide, for a given task, LangChain vs. raw SDK — not just default to whichever you learned last. Full details: [CURRICULUM.md §4](../CURRICULUM.md#document-05-langchain-basics).

---
Stuck? Ask for **Hint 1** or **Hint 2** (each has Basic/Intermediate depth). Ask for the full solution only if you say **"Show me the solution."**
