# Failure (watch it loop, then measure the cost) — Hints

> [Back to the exercise](../README.md#ex-infinite_loop_cost) · [Hint 1](infinite_loop_cost_hints.md#hint-1) · [Hint 2](infinite_loop_cost_hints.md#hint-2) · [Solution](infinite_loop_cost_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried. Each hint builds toward the full solution.

- [Hint 1 — A loop that never ends, safely](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

## Hint 1 — A loop that never ends, safely {: #hint-1 }

Put both limits in one function, `run_with_limits(task, max_iterations, timeout_seconds)`, and raise `MaxIterationsExceeded` (from the Intermediate exercise) for either one — steps or deadline.

Then measure the cost: each response has `response.usage_metadata["total_tokens"]` (LangChain's name for Doc04's `usage`). Store it in each step, add the steps up after the run stops, and compare with one direct call on an easy question.

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

```
run_with_limits(task, max_iterations, timeout_seconds) -> str:
    for step ...:
        past the deadline? raise MaxIterationsExceeded("deadline passed", steps)
        think; done? return the answer
        act / observe; steps.append({..., "tokens": total_tokens})
    raise MaxIterationsExceeded(message, steps)

main: catch it, add up the tokens in e.steps; then one direct call's tokens
```

Write it, then compare against the [Solution](infinite_loop_cost_solution.md).

Full solution: [Show me the solution](infinite_loop_cost_solution.md)
