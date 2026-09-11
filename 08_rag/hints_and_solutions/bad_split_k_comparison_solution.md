# Failure (a bad split, and a k comparison) — Solution

> [Back to the exercise](../README.md#ex-bad_split_k_comparison) · [Hint 1](bad_split_k_comparison_hints.md#hint-1) · [Hint 2](bad_split_k_comparison_hints.md#hint-2) · [Solution](bad_split_k_comparison_solution.md)

All examples below use:
```python
TEST_DOCUMENT = (
    "Our team ships a small internal newsletter every month. "
    "The Treaty of Lisbon was signed on 13 December 2007 in Lisbon, Portugal, "
    "marking a major change to how the European Union is governed. "
    "Most readers skip the history section and go straight to the recipe at the bottom."
)
QUESTION = "When and where was the Treaty of Lisbon signed?"
```

## Basic Version

### Approach 1 — the direct way

```python
import math
import time
from openai import OpenAI

client = OpenAI()

def chunk_by_chars(text, chunk_size):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size
    return chunks

def get_embedding(text):
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b)

def retrieve(question, chunks_with_embeddings, k):
    question_embedding = get_embedding(question)
    scored = []
    for chunk_text, embedding in chunks_with_embeddings:
        score = cosine_similarity(question_embedding, embedding)
        scored.append((score, chunk_text))
    scored.sort(reverse=True)
    return scored[:k]

chunks = chunk_by_chars(TEST_DOCUMENT, 40)
print("chunks:")
for i, chunk in enumerate(chunks):
    print(i, ":", repr(chunk))

chunks_with_embeddings = [(chunk, get_embedding(chunk)) for chunk in chunks]

print()
print("k=1 result:")
for score, chunk_text in retrieve(QUESTION, chunks_with_embeddings, k=1):
    print(score, repr(chunk_text))

print()
print("timing at k=1, k=3, k=10:")
for k in (1, 3, 10):
    start = time.perf_counter()
    results = retrieve(QUESTION, chunks_with_embeddings, k)
    elapsed = time.perf_counter() - start
    print("k =", k, "| time:", round(elapsed, 4), "seconds")
    for score, chunk_text in results:
        print("   ", round(score, 3), repr(chunk_text))
```
**Expected output (shape):** the fact's sentence gets sliced across 2-3 of the 40-character chunks, mid-word in at least one place. At `k=1`, the single chunk that comes back usually has only the date, or only the place, never both. As `k` grows to 3 and then 10, more surrounding chunks come back and the full fact becomes reconstructable — but the timing barely changes at this scale, because comparing a question against a handful of chunks one by one is already close to instant.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-bad_split_k_comparison) · [Hint 1](bad_split_k_comparison_hints.md#hint-1) · [Hint 2](bad_split_k_comparison_hints.md#hint-2) · [Solution](bad_split_k_comparison_solution.md)

## Intermediate Version

### Approach 1 — `build_index()` / `retrieve()`, factored apart

```python
import math
import time
from openai import OpenAI

client = OpenAI()


def chunk_by_chars(text: str, chunk_size: int) -> list[str]:
    chunks: list[str] = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size
    return chunks


def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b)


def retrieve(
    question: str, chunks_with_embeddings: list[tuple[str, list[float]]], k: int
) -> list[tuple[float, str]]:
    question_embedding = get_embedding(question)
    scored: list[tuple[float, str]] = []
    for chunk_text, embedding in chunks_with_embeddings:
        score = cosine_similarity(question_embedding, embedding)
        scored.append((score, chunk_text))
    scored.sort(reverse=True)
    return scored[:k]


def build_index(text: str, chunk_size: int) -> list[tuple[str, list[float]]]:
    chunks = chunk_by_chars(text, chunk_size)
    return [(chunk, get_embedding(chunk)) for chunk in chunks]


def main() -> None:
    chunks_with_embeddings = build_index(TEST_DOCUMENT, 40)

    print("k=1 result:")
    for score, chunk_text in retrieve(QUESTION, chunks_with_embeddings, k=1):
        print(f"  {score:.3f}  {chunk_text!r}")

    print("\ntiming at k=1, k=3, k=10:")
    for k in (1, 3, 10):
        start = time.perf_counter()
        results = retrieve(QUESTION, chunks_with_embeddings, k)
        elapsed = time.perf_counter() - start
        print(f"k = {k} | time: {elapsed:.4f} seconds")
        for score, chunk_text in results:
            print(f"    {score:.3f}  {chunk_text!r}")


if __name__ == "__main__":
    main()
```

**Difference from Basic:** full type hints, and `build_index()` separates "turn raw text into a searchable index" from `retrieve()`'s "search an existing index" — a real pipeline builds the index once and searches it many times, so keeping those responsibilities apart matters even in a small script.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-bad_split_k_comparison) · [Hint 1](bad_split_k_comparison_hints.md#hint-1) · [Hint 2](bad_split_k_comparison_hints.md#hint-2) · [Solution](bad_split_k_comparison_solution.md)

## Advanced Version

### Approach 1 — timing at real scale, not toy scale

```python
def build_large_corpus(document: str, repeats: int) -> str:
    return document * repeats


large_document = build_large_corpus(TEST_DOCUMENT, repeats=200)
large_index = build_index(large_document, chunk_size=40)
print(f"large corpus: {len(large_index)} chunks")

print("timing at k=1, k=3, k=10 (large corpus):")
for k in (1, 3, 10):
    start = time.perf_counter()
    retrieve(QUESTION, large_index, k)
    elapsed = time.perf_counter() - start
    print(f"k = {k} | time: {elapsed:.4f} seconds")
```
**Expected output (shape):** where the small corpus (a handful of chunks) showed almost no timing difference across `k` values, the large corpus's `retrieve()` calls all take noticeably longer than any of the small-corpus calls did — because `retrieve()` scores *every* stored chunk against the question no matter what `k` is; `k` only controls how many of those already-computed scores get returned. The cost that actually scales with corpus size was always there — the earlier, tiny example was just too small to show it. This is exactly why a real vector store (Chroma, FAISS, a hosted service) doesn't do this brute-force comparison at all once a knowledge base grows past a few thousand chunks — it builds an index ahead of time so a query only touches a small, likely-relevant fraction of the stored vectors, not every single one.

### Approach 2 — the real fix for the split fact: overlap, not a bigger k

```python
def chunk_by_chars_with_overlap(text: str, chunk_size: int, overlap: int) -> list[str]:
    chunks: list[str] = []
    step = chunk_size - overlap
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += step
    return chunks


def build_overlap_index(text: str, chunk_size: int, overlap: int) -> list[tuple[str, list[float]]]:
    chunks = chunk_by_chars_with_overlap(text, chunk_size, overlap)
    return [(chunk, get_embedding(chunk)) for chunk in chunks]


overlap_index = build_overlap_index(TEST_DOCUMENT, chunk_size=40, overlap=15)

print("k=1 result, WITH overlap:")
for score, chunk_text in retrieve(QUESTION, overlap_index, k=1):
    print(f"  {score:.3f}  {chunk_text!r}")
```
**Expected output:** with `overlap=15` on a `chunk_size=40` split, the fact's date-and-place sentence now lands whole inside at least one chunk, so `retrieve(..., k=1)` alone returns the complete fact — no need for `k=3` or `k=10` to reconstruct it from separate pieces.

**Difference from Intermediate, and between these 2 Advanced approaches:** Intermediate measures timing at a scale too small to reveal that brute-force cost actually grows with corpus size — Approach 1 makes that cost visible, and explains why real vector stores don't do this same brute-force comparison at scale. Approach 2 tackles a different question entirely: not "how do we search faster," but "how do we stop losing half the fact in the first place" — and shows that the answer isn't `k`, it's the chunker.

**Which one should you actually use?** Both matter, but they answer different questions. For "the search is too slow," reach for a real vector index (Approach 1's lesson) once your chunk count is large enough for brute force to actually hurt — not before, since brute force over a small corpus is simpler and genuinely fine. For "the answer is missing half a fact," reach for overlap (Approach 2) — not a bigger `k` — since `k` only ever improves the odds of the workaround, while overlap removes the actual cause. Mixing these two up (treating a `k` bump as if it fixes the boundary-split problem) is the exact trap this exercise exists to catch you doing once, on purpose, before it happens to you by accident in a real project.
