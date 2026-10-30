# Intermediate (multi-agent content pipeline design) — Solution

> [Back to the exercise](../README.md#ex-multi_agent_pipeline_design) · [Hint 1](multi_agent_pipeline_design_hints.md#hint-1) · [Hint 2](multi_agent_pipeline_design_hints.md#hint-2) · [Solution](multi_agent_pipeline_design_solution.md)

**Story — `multi_agent_pipeline_design.md`:** this is Project 4's shape, but designed completely fresh from a one-sentence request instead of followed from a ready-made guide — you decide the phases, the pattern, the shared state, and what happens when a check fails, all yourself. **If not:** you'd only ever have built multi-agent systems someone else had already designed for you.

Write your own design first, in `practice/multi_agent_pipeline_design.md`.

The request: "research a topic, draft an article, fact-check it, only publish if fact-check passes."

## Solution

**Story:** a revision loop without a hard limit, and a single generic "try again" response for every kind of failure, are the two places this pipeline genuinely breaks in practice. A revision cap, a real escalation path to a human, and two *different* loop-back targets (one for the writer, one for research) fix both problems at once. **If not:** some articles would loop forever with no way out, and a missing-research problem would keep getting sent to the writer to "fix" by rewording something that was never the actual issue.

Same three agents, hardened where an unbounded loop and an underspecified state object would actually fail:

- **A hard revision cap with a named escalation path.** `MAX_REVISIONS = 3`. If fact-check still fails after 3 writer revisions, the article escalates to a human editor with the full history (every draft, every round of fact-check notes) — it does not loop again. This is a direct application of Doc14's failure vocabulary: an unbounded retry loop is a real failure mode, not just a hypothetical one, and this document's "Expected Behavior" explicitly expects you to ask "what stops this from looping forever" before being asked.
- **Two different loop-back destinations, not one.** If the fact-checker finds a claim with *no supporting source at all*, that's a research gap — it routes back to the researcher, not the writer, because no amount of rewriting fixes missing information. If the fact-checker finds a claim that's source-backed but overstated or misworded, that routes back to the writer with specific notes. Collapsing these into one generic "try again" loses the distinction that actually determines whether the retry can succeed.
- **A shared state object with a revision counter and structured notes**, not just a draft passed hand to hand — every agent downstream needs to see *why* the last attempt was rejected, or the writer is revising blind and likely repeating the same mistake.
- **Monitoring on revision_count and route taken**, so articles that consistently hit the cap become a visible signal that a specific topic or source set is the problem — not just individual bot failures nobody's tracking in aggregate.
- **The fact-checker flags, it doesn't rewrite** — named as a deliberate trade-off, not an unquestioned default: at the scale this exercise describes, the extra round-trip cost of sending it back to the writer is worth the cleaner separation of concerns and the auditability of "the fact-checker's only output is a pass/fail plus notes." At very high volume, this is exactly the kind of choice worth revisiting.

**Why each piece is here, not added for its own sake:** A plain "try again" loop has no answer for what happens when fact-check simply never passes — which is not an edge case, it's a certainty for some articles (a genuinely contradictory topic, a core claim the writer keeps reintroducing). Without a cap, that's an infinite loop burning tokens and never resolving; a reviewer will ask about this immediately, and "it just keeps retrying" is not an acceptable answer. Treating every fact-check failure the same way sends a missing-research problem to the writer to fix by rewording — something rewording can't actually fix. The cap, the escalation path, and the two loop-back destinations each trace directly to a specific way the simple loop breaks.

**Presenting this in an interview:** Present the shape first — phases and the loop-back concept are the correct instinct. Then, unprompted, raise "what happens if fact-check never passes" and walk through the cap and escalation path yourself — that's the exact behavior Doc16 expects, and it's usually the question that decides whether the interviewer sees you as someone who's actually thought about failure, not just the happy path.
