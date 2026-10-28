# Real-world (compare your loop to the library's) — Hints

> [Back to the exercise](../README.md#ex-agent_executor_comparison) · [Hint 1](agent_executor_comparison_hints.md#hint-1) · [Hint 2](agent_executor_comparison_hints.md#hint-2) · [Solution](agent_executor_comparison_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried. Each hint builds toward the full solution.

- [Hint 1 — `create_agent` is your loop, pre-built](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

## Hint 1 — `create_agent` is your loop, pre-built {: #hint-1 }

To compare fairly, run the **same prompts** through both loops and count tool calls:

- yours: `len(run_agent(prompt).steps)`;
- the library's: count the messages whose `.type` is `"tool"` — one per tool result.

And compare how each stops a run that never ends: your `MaxIterationsExceeded`, and the library's `recursion_limit` setting — `agent.invoke(inputs, {"recursion_limit": 6})` — which raises `GraphRecursionError` (from `langgraph.errors`). It counts graph steps, about 2 per turn.

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

```
for each of 3 prompts:
    mine = run_agent(prompt)            # from react_loop_practice.py
    library = agent.invoke(...)
    print both tool-call counts

looping_agent = create_agent(model, tools=[always_ask_again])
try: looping_agent.invoke(..., {"recursion_limit": 6})
except GraphRecursionError: print it
try: run_agent(two-step task, max_iterations=1)
except MaxIterationsExceeded as e: print len(e.steps)
```

Write it, then compare against the [Solution](agent_executor_comparison_solution.md).

Full solution: [Show me the solution](agent_executor_comparison_solution.md)
