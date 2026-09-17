# Edge cases (when the answer spans two chunks) — Solution

> [Back to the exercise](../README.md#ex-chunk_boundary_split) · [Hint 1](chunk_boundary_split_hints.md#hint-1) · [Hint 2](chunk_boundary_split_hints.md#hint-2) · [Solution](chunk_boundary_split_solution.md)

## Basic Version

### Approach 1 — see the split, and the k=1 vs k=2 gap

```python
# chunking_practice.py — Edge cases section
import math
from openai import OpenAI

client = OpenAI()

document = "The quarterly meeting will be held at 3 PM on Friday in Room 204, and everyone from the product and engineering teams is expected to attend without exception."
chunk_size = 80

chunks = []
for i in range(0, len(document), chunk_size):
    chunks.append(document[i:i + chunk_size])

print("chunks:")
for i, chunk in enumerate(chunks):
    print(i, ":", repr(chunk))

def get_embedding(text):
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b)

chunk_embeddings = [get_embedding(chunk) for chunk in chunks]

question = "What time and room is the quarterly meeting, and who is expected to attend?"
question_embedding = get_embedding(question)

scored = []
for i in range(len(chunks)):
    score = cosine_similarity(question_embedding, chunk_embeddings[i])
    scored.append((score, i))
scored.sort(reverse=True)

print()
print("search with k=1:")
for score, i in scored[:1]:
    print(chunks[i])

print()
print("search with k=2 (all chunks):")
for score, i in scored[:2]:
    print(chunks[i])
```
**Expected output:**
```
0 : 'The quarterly meeting will be held at 3 PM on Friday in Room 204, and everyone f'
1 : 'rom the product and engineering teams is expected to attend without exception.'
```
The boundary lands mid-word, mid-fact: chunk 0 has the time and room, chunk 1 has who is expected to attend. With `k=1`, the search returns only one of those two chunks — you get either the time/room or the attendee list, never both. With `k=2`, both chunks come back and together they contain the full answer.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-chunk_boundary_split) · [Hint 1](chunk_boundary_split_hints.md#hint-1) · [Hint 2](chunk_boundary_split_hints.md#hint-2) · [Solution](chunk_boundary_split_solution.md)

## Intermediate Version

### Approach 1 — a reusable `search(..., k)` function

```python
# chunking_practice.py — Edge cases section
import math
from openai import OpenAI

client = OpenAI()

DOCUMENT: str = (
    "The quarterly meeting will be held at 3 PM on Friday in Room 204, "
    "and everyone from the product and engineering teams is expected "
    "to attend without exception."
)
CHUNK_SIZE: int = 80
QUESTION: str = "What time and room is the quarterly meeting, and who is expected to attend?"


def chunk_text(text: str, chunk_size: int) -> list[str]:
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b)


def search(
    question: str, chunks: list[str], chunk_embeddings: list[list[float]], k: int
) -> list[str]:
    question_embedding = get_embedding(question)
    scored = [
        (cosine_similarity(question_embedding, embedding), chunk)
        for chunk, embedding in zip(chunks, chunk_embeddings)
    ]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [chunk for _, chunk in scored[:k]]


def main() -> None:
    chunks = chunk_text(DOCUMENT, CHUNK_SIZE)
    print(f"document was cut into {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f"  {i}: {chunk!r}")

    chunk_embeddings = [get_embedding(chunk) for chunk in chunks]

    top_1 = search(QUESTION, chunks, chunk_embeddings, k=1)
    top_all = search(QUESTION, chunks, chunk_embeddings, k=len(chunks))

    print("\nk=1 result:")
    for chunk in top_1:
        print(" ", chunk)
    print(f"\nk={len(chunks)} result (all chunks):")
    for chunk in top_all:
        print(" ", chunk)


if __name__ == "__main__":
    main()
```

**Difference from Basic:** `search` is a reusable function with an explicit `k`, instead of inline tuple-sorting written out by hand — the shape real retrieval code needs, since a real pipeline calls this with different questions and different `k` values repeatedly. `k=len(chunks)` instead of a hardcoded `2` means the same code keeps working if `CHUNK_SIZE` changes and the document ends up in 3 or 4 chunks instead of 2.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-chunk_boundary_split) · [Hint 1](chunk_boundary_split_hints.md#hint-1) · [Hint 2](chunk_boundary_split_hints.md#hint-2) · [Solution](chunk_boundary_split_solution.md)

## Advanced Version

### Approach 1 — overlap removes the need for a bigger `k` at all

```python
# chunking_practice.py — Edge cases section
def chunk_with_overlap(text: str, chunk_size: int, overlap: int) -> list[str]:
    chunks: list[str] = []
    step = chunk_size - overlap
    i = 0
    while i < len(text):
        chunks.append(text[i:i + chunk_size])
        i += step
    return chunks


def main() -> None:
    overlap_chunks = chunk_with_overlap(DOCUMENT, chunk_size=80, overlap=20)
    print(f"overlapping chunks ({len(overlap_chunks)}):")
    for i, chunk in enumerate(overlap_chunks):
        print(f"  {i}: {chunk!r}")

    overlap_embeddings = [get_embedding(chunk) for chunk in overlap_chunks]
    top_1_overlap = search(QUESTION, overlap_chunks, overlap_embeddings, k=1)

    print("\nk=1 result, WITH overlap:")
    for chunk in top_1_overlap:
        print(" ", chunk)


if __name__ == "__main__":
    main()
```
**Expected output:** with `overlap=20`, one of the overlapping chunks now spans past where the old, non-overlapping cut fell — the room number and the "expected to attend" clause end up inside the *same* chunk, because the new chunk starts 20 characters before the previous one ended. `search(..., k=1)` against the overlapping chunks returns that one chunk, and it now contains the complete fact — something `k=1` against the non-overlapping chunks could never do, no matter how the scores landed.

### Approach 2 — proving `k` alone never fully solves this, at any size

```python
# chunking_practice.py — Edge cases section
# same fact, but now buried inside a much longer document with lots of
# other, unrelated sentences before and after it
padding = "This is unrelated filler text about the cafeteria menu. " * 20
long_document = padding + DOCUMENT + padding

chunks = chunk_text(long_document, chunk_size=80)
print(f"long document produced {len(chunks)} non-overlapping chunks")

chunk_embeddings = [get_embedding(chunk) for chunk in chunks]
top_3 = search(QUESTION, chunks, chunk_embeddings, k=3)

print("k=3 result on the long document:")
for chunk in top_3:
    print(" ", chunk)
```
**Expected output (illustrative):** with dozens of chunks now competing for the top spots, `k=3` is no longer guaranteed to include *both* halves of the split fact — the "unrelated filler" chunks don't win, but the two fact-halves might not both make the top 3 either, depending on exactly how the cut fell relative to the surrounding filler text. This is the point: raising `k` was never a guarantee, just better odds in a small example. Chunking with overlap (Approach 1) removes the problem at its source, regardless of how many other chunks exist.

**Difference from Intermediate, and between these 2 Advanced approaches:** Intermediate shows that a bigger `k` recovers the full fact *in this specific 2-chunk document*. Approach 1 fixes the actual cause — with overlap, the fact is never split across chunks in the first place, so even `k=1` gets the whole thing. Approach 2 demonstrates why that matters: once the document is realistically sized, a bigger `k` stops being a reliable fix at all, because it's competing against many more chunks for a fixed number of "winning" slots.

**Which one should you actually write?** Overlap (Approach 1) — always, for any fixed-size chunker used on real documents. It costs a little redundant storage (each chunk shares text with its neighbors) in exchange for removing an entire class of "half the fact went missing" bugs. Treat a bigger `k` as a mitigation you might still use for other reasons (recall on genuinely separate but related chunks), never as the actual fix for a boundary-split fact — Approach 2 is the proof that raising `k` doesn't scale the way it might feel like it does in a 2-chunk toy example.
