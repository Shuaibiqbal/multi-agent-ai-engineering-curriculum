# Step 1 — The Help-Docs RAG and the Confidence Gate — Hints

> [Back to the step](../READING_README.md#step-1-the-help-docs-rag-and-the-confidence-gate) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](step1_rag_and_confidence_solution.md)

- [Hint 1 — the RAG layer](#hint-1)
- [Hint 2 — the gate is one line](#hint-2)

## Hint 1 — the RAG layer {: #hint-1 }

Doc08's RAG, over your help articles:

- `src/rag/help_store.py` → `build_help_store()`: load `data/help_docs/*.md` (`DirectoryLoader` + `TextLoader`), embed with `OpenAIEmbeddings`, `collection.add(...)` to a fresh Chroma collection.
- `src/rag/retriever.py` → `best_match(collection, question)`: `collection.query(..., n_results=1)` and return `(documents[0], distances[0])` — the closest article and how far it is. Return `("", 2.0)` if the collection is empty.

The distance is the whole signal — lower means the docs cover this question.

## Hint 2 — the gate is one line {: #hint-2 }

The entire answer-or-escalate decision is this:

```
# src/confidence.py
def is_confident(distance, cutoff=0.8):
    return distance <= cutoff
```

That's it — a small function the whole bot turns on. Test it with made-up distances, no model: `is_confident(0.2)` is True, `is_confident(1.5)` is False, and `is_confident(0.8)` (exactly the cutoff) is True. Keeping the gate separate and deterministic is what lets you prove the bot's behavior before any graph or model exists. The whole file set is in the [Solution](step1_rag_and_confidence_solution.md).
