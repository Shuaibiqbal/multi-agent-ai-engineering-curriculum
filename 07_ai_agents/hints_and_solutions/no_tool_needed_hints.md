# Edge cases (a task that needs no tool at all) — Hints

> [Back to the exercise](../README.md#ex-no_tool_needed) · [Hint 1](no_tool_needed_hints.md#hint-1) · [Hint 2](no_tool_needed_hints.md#hint-2) · [Solution](no_tool_needed_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried. Each hint builds toward the full solution.

- [Hint 1 — What "no tool" looks like](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

## Hint 1 — What "no tool" looks like {: #hint-1 }

One prompt is one data point. Use a short list of clearly-no-tool prompts, check each one with `len(result.steps) == 0`, and print a `case` line per prompt plus a total — the same plain test style as Doc04–06.

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

```
NO_TOOL_PROMPTS = [3 questions no tool can help with]

check_no_tool(prompt) -> bool: len(run_agent(prompt).steps) == 0

main: for each prompt, print a case line; then "N/3 answered without a tool"
```

Write it, then compare against the [Solution](no_tool_needed_solution.md).

Full solution: [Show me the solution](no_tool_needed_solution.md)
