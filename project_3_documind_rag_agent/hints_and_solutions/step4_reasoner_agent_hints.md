# Step 4 — A Reasoner Agent That Only Answers From What the Retriever Found — Hints

> [Back to this step](../READING_README.md#step-4-a-reasoner-agent-that-only-answers-from-what-the-retriever-found) · [Hint 1](step4_reasoner_agent_hints.md#hint-1) · [Hint 2](step4_reasoner_agent_hints.md#hint-2) · [Solution](step4_reasoner_agent_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've really tried. Each hint starts with the plain idea, then shows the shape of the real code.

- [Hint 1 — What the Reasoner may and may not do](#hint-1)
- [Hint 2 — The plan, and how to check it](#hint-2)

<hr class="page-break">

> [Back to this step](../READING_README.md#step-4-a-reasoner-agent-that-only-answers-from-what-the-retriever-found) · [Hint 1](step4_reasoner_agent_hints.md#hint-1) · [Hint 2](step4_reasoner_agent_hints.md#hint-2) · [Solution](step4_reasoner_agent_solution.md)

## Hint 1 — What the Reasoner may and may not do {: #hint-1 }

The Reasoner writes the answer — and **only** from the excerpts the Retriever found. Left alone, a model quietly fills gaps from what it remembers.

So its prompt needs three rules:

- use only the excerpts below;
- after each fact, name its source file in square brackets;
- if the excerpts don't answer the question, reply with one **exact** sentence.

It doesn't search and doesn't approve — it only writes.

You don't add a node — you upgrade the inside of Step 3's `reason_node`. Keep its name, its input (the state) and its output (`answer` + `"reason_node"` in the path).

- `format_sources(sources) -> str` (new) — one line per excerpt: `"[refund_policy.md] Customers can return ..."`. Without the file name in front, the model has nothing to cite.
- inside `reason_node` — `ChatPromptTemplate.from_template(load_prompt("reasoner")) | get_model() | StrOutputParser()`, invoked with `{"sources": ..., "task": ...}`.

The prompt goes in `prompts/reasoner.txt`, with `{sources}` and `{task}` placeholders.

<hr class="page-break">

> [Back to this step](../READING_README.md#step-4-a-reasoner-agent-that-only-answers-from-what-the-retriever-found) · [Hint 1](step4_reasoner_agent_hints.md#hint-1) · [Hint 2](step4_reasoner_agent_hints.md#hint-2) · [Solution](step4_reasoner_agent_solution.md)

## Hint 2 — The plan, and how to check it {: #hint-2 }

```
agents/reasoner_agent.py:  + format_sources()
                           reason_node: same name and output,
                           the answer now comes from the chain
prompts/reasoner.txt:      new
```

Nothing else changes — the graph, the Retriever and `approval_node` stay the same.

Checking "it ran" isn't enough. For 3-4 questions, open the document and compare:

- Is every fact in the answer really in the excerpt it cites?
- Did it add anything the documents don't say?
- For a question the documents only half answer, does it say so instead of filling the gap?

If it adds facts, make the prompt stricter. If it never cites, check that `format_sources()` puts the file name in front of each excerpt.

Then turn the citation into a test: integration case 7 — the refund answer must contain `[refund_policy.md]`.

Full solution: [Show me the solution](step4_reasoner_agent_solution.md)
