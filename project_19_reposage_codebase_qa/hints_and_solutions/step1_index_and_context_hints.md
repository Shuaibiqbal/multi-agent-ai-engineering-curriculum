# Step 1 — The Code Index and the Context Builder — Hints

> [Back to the step](../READING_README.md#step-1-the-code-index-and-the-context-builder) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](step1_index_and_context_solution.md)

- [Hint 1 — index the code, keep the file path](#hint-1)
- [Hint 2 — the two deterministic builders](#hint-2)

## Hint 1 — index the code, keep the file path {: #hint-1 }

Doc08's RAG, over `.py` files:

- `build_code_store(repo_dir)`: `DirectoryLoader(repo_dir, glob="**/*.py", loader_cls=TextLoader)`, `RecursiveCharacterTextSplitter.split_documents(...)`, embed, `collection.add(...)`. The one thing that matters: keep each chunk's file path in `metadata["file"]` — that path is the citation.
- `retrieve_snippets(collection, question, k=4)`: `collection.query(...)` and build a list of `{"code": documents[i], "file": metadatas[i]["file"]}`.

## Hint 2 — the two deterministic builders {: #hint-2 }

Both take snippets and return something the rest of the pipeline uses — no model:

```
build_context(snippets):
    for each snippet: f"# File: {snippet['file']}\n{snippet['code']}"
    join the blocks with blank lines

cited_files(snippets):
    first-seen, de-duplicated list of snippet["file"]
```

The `# File:` header is what lets the model (Step 2) see which code came from which file, and `cited_files` is the "jump to source" list. Test both with hand-made snippets — two from `auth.py` → three `# File:` headers in the context but `auth.py` once in `cited_files`. The whole file set is in the [Solution](step1_index_and_context_solution.md).
