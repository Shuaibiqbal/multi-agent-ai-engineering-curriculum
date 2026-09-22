# Failure (make it confidently wrong, on purpose) — Hints

> [Back to the exercise](../README.md#ex-induced_hallucination) · [Hint 1](induced_hallucination_hints.md#hint-1) · [Hint 2](induced_hallucination_hints.md#hint-2) · [Solution](induced_hallucination_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried. Each hint has 2 depth levels: **Basic** (the plain idea) and **Intermediate** (the actual mechanism, and why the framing matters). Read Basic first even if you already understand the topic — it's the fastest way to spot exactly what Intermediate adds.

- [Hint 1 — Finding a good question, and phrasing it to invite confidence](#hint-1)
- [Hint 2 — Running it, and explaining why it happened](#hint-2)

<hr class="page-break">

> [Back to the exercise](../README.md#ex-induced_hallucination) · [Hint 1](induced_hallucination_hints.md#hint-1) · [Hint 2](induced_hallucination_hints.md#hint-2) · [Solution](induced_hallucination_solution.md)

## Hint 1 — Finding a good question, and phrasing it to invite confidence {: #hint-1 }

### Basic Version

You're looking for a question where the model doesn't actually know the answer, but the question is phrased in a way that makes the model want to give a confident, specific-sounding answer anyway — instead of saying "I don't know."

The best targets are things that sound like they should have one exact, findable answer (a specific number, date, or name) but are actually too obscure or too made-up for the model to have reliably learned.

Phrase the question as if the answer obviously exists — don't hint that you're unsure or testing it.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-induced_hallucination) · [Hint 1](induced_hallucination_hints.md#hint-1) · [Hint 2](induced_hallucination_hints.md#hint-2) · [Solution](induced_hallucination_solution.md)

### Intermediate Version

Three reliable categories to pick from:

1. **A real but obscure fact** — a statistic, a minor historical detail, a small company's founding date — something genuinely true but unlikely to appear often (or precisely) in training data.
2. **A plausible-sounding but fictional entity** — ask about a "paper," "law," or "person" you invent, phrased as if it definitely exists. The model often plays along rather than questioning the premise.
3. **A request for a specific citation** — "give me the exact page number where X said Y" — models are notoriously unreliable at exact citations because that's an extremely precise fact to have memorized correctly.

The framing matters as much as the category: "What was the exact attendance at [small, real but obscure event]?" works better than "do you happen to know roughly how many people attended...?" — the second version invites hedging, the first invites confidence, because a confidently-phrased question pulls the model toward a confidently-phrased continuation.

Pick one category and write the exact prompt you'll use before moving to Hint 2.

Notice all 3 categories share one property: the question has the *grammatical shape* of something with one exact, checkable answer. "What was the attendance at X" has the same shape whether X is a famous event with a well-documented number or a made-up local parade — the model responds to the shape of the question at least as much as to whether it actually knows the answer. Before running your prompt, predict: will the model hedge ("I'm not certain, but..."), refuse ("I don't have information about..."), or answer confidently and specifically? Write your prediction down — comparing it to what actually happens is the real test of whether you understand the mechanism, not just the trick.

**Difference between Basic and Intermediate:** Basic names the target (a question with no reliable answer, asked confidently). Intermediate gives 3 concrete categories and explains *why* the framing rule works — the model responds to the grammatical shape of a question, not a check of whether it actually knows the answer.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-induced_hallucination) · [Hint 1](induced_hallucination_hints.md#hint-1) · [Hint 2](induced_hallucination_hints.md#hint-2) · [Solution](induced_hallucination_solution.md)

## Hint 2 — Running it, and explaining why it happened {: #hint-2 }

### Basic Version

```
example prompt: "What was the exact founding date of [a small, obscure,
                 but real local business you know of]?"

expected result: the model gives a specific, confident-sounding date
                 that is probably wrong (or made up entirely) — instead
                 of saying "I don't actually know this."
```

Run your own version of this and record what it says. Then write one paragraph explaining *why* this happened — without using the word "mistake."

<hr class="page-break">

> [Back to the exercise](../README.md#ex-induced_hallucination) · [Hint 1](induced_hallucination_hints.md#hint-1) · [Hint 2](induced_hallucination_hints.md#hint-2) · [Solution](induced_hallucination_solution.md)

### Intermediate Version

```
prompt category chosen: fictional citation
example: "In which paragraph of [a real, well-known book] does the
          author first mention [a specific, invented detail]?"

expected result: the model names a specific paragraph or chapter,
                 stated confidently, that is very likely fabricated
                 — because it's answering "what would a citation for
                 this look like," not verifying the citation is real
```

Run your own prompt, record the exact answer you got, and note how confidently it was phrased — that confidence is the actual finding here, not just whether the fact was wrong.

Frame your explanation paragraph around the actual mechanism: the model generates the token sequence that's statistically most likely to follow your prompt, and a confident, specific-sounding, well-formed answer is a very natural-looking continuation of a confidently-phrased factual question — regardless of whether the underlying claim is grounded in anything real.

Write your explanation now. There is no separate step where the model checks its own answer against the world — fluency and correctness are produced by the identical process and look identical from the outside, which is why this "can't just be fixed like a bug" the way one faulty line of logic can. Grounding the answer in retrieved, real source text (RAG, covered properly in Doc08) is the main real mitigation — worth naming in your explanation if you want to go one step further than the plain mechanism.

Compare your explanation against the [Solution](induced_hallucination_solution.md).

**Difference between Basic and Intermediate:** Basic gets you a working example and asks for an explanation in your own words. Intermediate adds the mechanical vocabulary (token-sequence prediction, continuation likelihood) and names why this specific kind of failure resists being "just fixed" the way a normal bug would be.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-induced_hallucination) · [Hint 1](induced_hallucination_hints.md#hint-1) · [Hint 2](induced_hallucination_hints.md#hint-2) · [Solution](induced_hallucination_solution.md)

Full solution: [Show me the solution](induced_hallucination_solution.md)
