# Basic (design on paper before touching code) — Solution

> [Back to the exercise](../README.md#ex-paper_design) · [Hint 1](paper_design_hints.md#hint-1) · [Hint 2](paper_design_hints.md#hint-2) · [Solution](paper_design_solution.md)

**Story — `architecture_comparison_practice.py` (Basic section):** a prediction written *before* any code is the only way to find out later whether your design instinct was right. This section is plain text, kept as a comment block at the top of the file, so the measured numbers below it can be checked against it. **If not:** after building, you'd remember "I expected that" — whether you did or not.

Task chosen below: "research the top 3 causes of X, then write a 3-sentence summary."

## Solution

**Story:** a guess becomes useful once it has numbers and mechanisms a colleague could argue with. **If not:** "the supervisor is slower" can't be proven wrong — so it can't teach you anything either.

```
design 1 -- single agent
    flow: one agent gets "research X, write a summary," calls a research tool as
    needed inside its own turn, then writes the final summary itself
    cost: ~1-2 LLM calls total
    speed: fastest of the three -- no agent-to-agent handoff at all
    reliability risk: the single system prompt has to be good at both research
    judgment and writing style simultaneously; a prompt tuned for good writing
    style can quietly get worse at judging source quality, and vice versa

design 2 -- sequential
    flow: research_agent(topic) -> findings; write_agent(findings) -> summary,
    always in that fixed order
    cost: ~2 LLM calls, one per stage
    speed: about the same wall-clock time as design 1 -- there's no parallelism
    to gain here, since writing genuinely needs the research first
    reliability risk: very predictable in structure (the order is enforced by
    code, not judgment), but there is no check step -- a weak research_agent
    output is faithfully summarized as if it were solid

design 3 -- supervisor
    flow: supervisor reads the task, decides to call research_agent, gets the
    result, decides to call write_agent, gets the result, returns
    cost: ~3+ LLM calls -- 2 for the actual work, 1 or more for the routing
    decision itself, which is not free
    speed: slowest of the three -- the routing decision adds real delay on
    top of design 2's delay, for a task whose order was fixed anyway
    reliability risk: everything design 2 has, plus a new failure mode --
    the supervisor could route to the wrong specialist, or call one specialist
    twice thinking it needs another pass
```
