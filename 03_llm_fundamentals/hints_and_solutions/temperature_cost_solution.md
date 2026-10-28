# Intermediate (temperature and cost, side by side) — Solution

> [Back to the exercise](../README.md#ex-temperature_cost) · [Hint 1](temperature_cost_hints.md#hint-1) · [Hint 2](temperature_cost_hints.md#hint-2) · [Solution](temperature_cost_solution.md)

**Story — `temperature_cost_practice.md`:** temperature changes how varied the answers are, and tokens decide what each call costs. Seeing both side by side, with real numbers, is the base for every later cost and quality decision. **If not:** you'd tune these by feel.

## Solution

**Story:** the same two parts, with the mechanism behind temperature and the units written out in the cost sum. **If not:** a units mistake would put your cost estimate off by a factor of a million.

**Part 1 — temperature, explained mechanically.** At each step, the model computes a probability distribution over its whole vocabulary for "what comes next." `temperature=0` collapses that into effectively always taking the single highest-probability token — this is called greedy decoding, and it's why repeated calls converge on nearly identical output. `temperature=1` samples from the distribution closer to its natural shape, so tokens with real but lower probability get picked sometimes, and one different token early in the sentence compounds into a different sentence by the end, since each next token is chosen conditioned on everything before it.

This is also why a fact-lookup or classification prompt barely moves with temperature — the model's distribution is already sharply peaked on one answer regardless of setting, so there's nothing for temperature to meaningfully redistribute. An open-ended creative prompt has a much flatter distribution across many reasonable continuations, so temperature has real material to work with.

**Part 2 — cost, with units made explicit.**

```
input_rate_per_million  = $0.15
output_rate_per_million = $0.60

input_tokens  = 2000
output_tokens = 500

cost = (2000 / 1_000_000) * 0.15 + (500 / 1_000_000) * 0.60
     = 0.0003 + 0.0003
     = $0.0006
```

Scaling this up matters more than the tiny absolute number suggests: at 10,000 calls a day with this shape, that's $6/day, or about $180/month, from one feature alone — and that's before a growing conversation history multiplies the input-token count on every later turn.
