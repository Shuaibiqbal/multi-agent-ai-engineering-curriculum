# Intermediate (defend one non-obvious trade-off under pushback) — Solution

> [Back to the exercise](../README.md#ex-defend_tradeoff) · [Hint 1](defend_tradeoff_hints.md#hint-1) · [Hint 2](defend_tradeoff_hints.md#hint-2) · [Solution](defend_tradeoff_solution.md)

**Story — `defend_tradeoff.md`:** a decision you've only ever defended against a weak objection isn't really defended at all. This exercise picks one real, genuinely debatable decision from your own capstone and holds it up against the strongest objection you can honestly build yourself. **If not:** the first truly strong objection you ever face would come from a real reviewer, live, in the moment, with no prepared reasoning ready.

Write your own version first, in `practice/defend_tradeoff.md`, then compare.

**Decision used for this model answer:** "I gave every agent access to most of the shared state, instead of giving each agent only its own private slice." (In this example, the capstone design added a fact-checker agent to Project 4's team, to check each draft's claims against the RAG sources.)

## Solution

**Story:** this names exactly what the alternative approach would really have cost, shows the actual mitigation you built for the risk you took on instead, and states plainly what would genuinely change your mind. **If not:** "it's simpler" would be your only defense, and that alone never actually answers "but it's riskier."

"I designed the shared LangGraph state object as mostly-shared, with each agent also holding a small private scratch field. The alternative — fully private state per agent, passed explicitly between them — is the more conservative, more encapsulated choice, and it's the one a strict software-engineering instinct favors: less surface area for one agent's bug to corrupt another agent's data.

The strongest objection: shared mutable state is a well-known source of hard-to-trace bugs, and it gets worse as agent count grows — this system already has five agents, and any of them could, in principle, write into a field another agent depends on, with no compiler or type system catching the mistake.

What fully private state would have cost me specifically: the fact-checker's entire job is evaluating the writer's draft against the researcher's sources — that's not incidental, it's the core requirement. Fully private state means explicitly passing those fields at every handoff, which is more code, and it doesn't remove the risk the objection raises — it just moves it from 'read the wrong shared field' to 'forget to pass the right field forward,' which is arguably worse because it fails silently (a missing field, not a wrong one) rather than loudly.

What I accepted on purpose: the corruption risk the objection names is real, so I mitigated it directly rather than dismissing it — each agent's write access is scoped by convention and enforced with a lightweight schema check at each node boundary (each agent's node function only writes to its own declared output keys), which gets most of fully-private-state's safety without the handoff overhead.

Verdict: I would not switch to fully private state, because the core requirement (cross-agent visibility for fact-checking) makes the objection's underlying concern unavoidable either way — the real fix is the schema-enforced write boundary, which I already have. I WOULD reconsider the schema-check approach itself if it turned out too permissive in practice — that's a concrete, checkable thing to watch for, not a hypothetical."

**Why this answer works:** it names the real, non-strawmanned cost of the alternative (encapsulation, less corruption risk) instead of dismissing it. It ties the decision to the specific functional requirement that makes the alternative genuinely worse, not just less convenient. It shows a real mitigation that was actually built, not promised. And the verdict names a concrete condition that would change the answer, which proves the position isn't just stubbornness.

**What a weaker answer misses:** a weaker answer says "I used shared state because it's simpler" — true, but "simpler for me to write" isn't a defense against "riskier to maintain," it just restates the choice without engaging the objection at all. A weaker answer also sometimes claims the objection doesn't apply ("that would never actually happen") instead of acknowledging the real risk and showing the mitigation — which reads as either not understanding the objection or being unwilling to admit any cost to your own decision, both of which read poorly under real pushback.
