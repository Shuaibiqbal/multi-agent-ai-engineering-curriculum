# DocsGenie — Hints

> Read the [story](../READING_README.md) and try to build it first. These hints point you at the pieces and the easy-to-miss parts, without giving the whole answer. The full code is in the [complete solution](solution.md).

## Hint 1 — the pieces, and where to start

The same shape as RepoSage, for documentation:

- `src/context.py` — `build_context(passages)` (one block, each under a `# Page:` header) and `cited_pages(passages)` (de-duplicated page names). **Build this first** — it's plain Python, no model, so you can test the grounding block and the citation list with hand-made passages.
- `src/rag/docs_store.py` — `build_docs_store(docs_dir)`: load `**/*.md`, chunk, and **keep each chunk's page name in metadata** (that name is the citation). Keep just the filename (`source.split("/")[-1]`) so citations read `authentication.md`.
- `src/rag/retriever.py` — `retrieve_passages(collection, question)` → `[{text, page}, ...]`.
- `src/answer.py` — `answer_question(model, question, context)`: the model answers using **only** the context, says "I don't know" otherwise.
- `src/pipeline.py` — `run_query(model, docs_dir, question)`: retrieve → context → answer → attach cited pages.

Build order: context + cited_pages (test them) → docs store + retriever → answer → pipeline.

## Hint 2 — the two easy-to-miss parts

**The page name is the citation.** When you chunk, each document's `metadata["source"]` is the full path; keep just the filename so the citation is a page a user can open:

```
page = chunk.metadata.get("source", "unknown").split("/")[-1]
```

**"Answer only from this."** The prompt is the whole trick — without it the model answers from how products *usually* work, not *this* product:

```
You answer using ONLY the documentation below. If the answer is not in it,
say you don't know. Name the page(s) the answer comes from.
```

`cited_pages` de-duplicates in first-seen order, so two passages from the same page appear once:

```
pages = []
for passage in passages:
    if passage["page"] not in pages:
        pages.append(passage["page"])
```

Keep the model at `temperature=0` so answers are repeatable. The whole file set is in the [complete solution](solution.md).
