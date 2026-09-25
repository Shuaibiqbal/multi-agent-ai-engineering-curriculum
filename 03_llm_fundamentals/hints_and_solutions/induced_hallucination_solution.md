# Failure (make it confidently wrong, on purpose) — Solution

> [Back to the exercise](../README.md#ex-induced_hallucination) · [Hint 1](induced_hallucination_hints.md#hint-1) · [Hint 2](induced_hallucination_hints.md#hint-2) · [Solution](induced_hallucination_solution.md)

**Story — `induced_hallucination_practice.md`:** a model will state made-up facts with full confidence. Causing it on purpose, and explaining why it happens, is what makes you design around it instead of being surprised by it. **If not:** you'd trust fluent answers as if fluency meant truth.

## Basic Version

**Story:** make it happen once, and explain it in plain words. **If not:** "hallucination" would stay a word you've read, not something you've seen.

**Prompt used:** "What was the exact attendance figure at the third annual Millbrook Founders' Day parade?" (a plausible-sounding but invented local event).

**What happened:** the model gave a specific number, stated plainly, with no hedging — something like "approximately 4,200 people attended." There is no such event, so this number cannot be real; it's a plausible-sounding guess dressed up as a fact.

**Why, in one paragraph, without the word "mistake":** the model isn't looking anything up when it answers — it's predicting what a normal, confident answer to a question shaped like this usually looks like. A specific attendance question "wants" a specific numeric answer in the kind of text the model was trained on, so it produces one, the same way it would produce a grammatically correct sentence — by pattern, not by verification.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-induced_hallucination) · [Hint 1](induced_hallucination_hints.md#hint-1) · [Hint 2](induced_hallucination_hints.md#hint-2) · [Solution](induced_hallucination_solution.md)

## Intermediate Version

**Story:** a subtler case, and the actual mechanism — a next-token predictor completing a likely-sounding answer. **If not:** you'd try to "fix" it like a bug instead of designing around it (sources, checks, refusals).

**Prompt used:** "In which chapter does the narrator of [a real, well-known novel] first describe the color of the house on Elm Street?" (a specific, invented detail about a real book).

**What happened:** the model named a specific chapter number and even paraphrased a plausible-sounding description, stated with no hedging or uncertainty markers.

**The mechanism:** a language model is a next-token predictor trained to maximize the likelihood of natural-sounding continuations of text, not a fact-retrieval system with a verification step. When given a question with the *grammatical shape* of a fact-based query — "in which chapter does X happen" — the highest-probability continuation is a specific, confidently-stated answer, because that is what answers to this shape of question look like in the training data, independent of whether the specific detail was actually memorized correctly, or exists at all.

**Difference from Basic:** Basic shows the phenomenon and names the mechanism in plain terms ("predicting a normal answer, not checking a fact"). Intermediate makes the mechanism precise — it's specifically about the *grammatical shape* of the question triggering a matching-shaped answer, regardless of the underlying claim's truth. Confidence in the output is a property of how the text is phrased, not a signal correlated with the claim being true — which is exactly why a fluent wrong answer and a fluent right one are indistinguishable from the outside.

**Why this can't just be "fixed" like a bug:** a bug implies a specific faulty line of logic you can locate and correct. This isn't that — it's the normal, intended behavior of a system whose entire purpose is producing plausible continuations, applied to a case where "plausible" and "true" have quietly come apart. Real systems reduce this without eliminating it — grounding the model's answer in retrieved, real source text (RAG, covered properly in Doc08) gives it something to condition on besides its own training-data patterns, and instructing it explicitly to say "I don't know" when uncertain measurably increases how often it does so.

**Which framing should you actually carry forward?** The plain-language version ("it's finishing a sentence, not checking a fact") is the one to keep in your head day-to-day when deciding whether to trust a specific answer — if a question has the shape of something the model would confidently answer either way, treat any precise-sounding number, date, or citation as unverified until you check it yourself.
