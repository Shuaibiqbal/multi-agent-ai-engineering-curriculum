# Edge cases (a task that needs no tool at all) — Hints

> [Back to the exercise](../README.md#ex-no_tool_needed) · [Hint 1](no_tool_needed_hints.md#hint-1) · [Hint 2](no_tool_needed_hints.md#hint-2) · [Solution](no_tool_needed_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried. Each hint has 2 depth levels: **Basic** (the plain idea) and **Intermediate** (proper Python). Read Basic first even if you already know Python — it's the fastest way to spot exactly what Intermediate adds.

- [Hint 1 — What "no tool" looks like](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

<hr class="page-break">

> [Back to the exercise](../README.md#ex-no_tool_needed) · [Hint 1](no_tool_needed_hints.md#hint-1) · [Hint 2](no_tool_needed_hints.md#hint-2) · [Solution](no_tool_needed_solution.md)

## Hint 1 — What "no tool" looks like {: #hint-1 }

### Basic Version

Ask your `run_agent()` a question none of your tools can help with — "What's the capital of France?". If the model answers directly, the loop exits on the first turn and `result.steps` is empty.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-no_tool_needed) · [Hint 1](no_tool_needed_hints.md#hint-1) · [Hint 2](no_tool_needed_hints.md#hint-2) · [Solution](no_tool_needed_solution.md)

### Intermediate Version

One prompt is one data point. Use a short list of clearly-no-tool prompts, check each one with `len(result.steps) == 0`, and print a `case` line per prompt plus a total — the same plain test style as Doc04–06.

**Difference between Basic and Intermediate:** Basic looks at one run. Intermediate checks several prompts and counts how many passed.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-no_tool_needed) · [Hint 1](no_tool_needed_hints.md#hint-1) · [Hint 2](no_tool_needed_hints.md#hint-2) · [Solution](no_tool_needed_solution.md)

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

### Basic Version

```
result = run_agent("What's the capital of France?")
print the answer, and len(result.steps)
```

<hr class="page-break">

> [Back to the exercise](../README.md#ex-no_tool_needed) · [Hint 1](no_tool_needed_hints.md#hint-1) · [Hint 2](no_tool_needed_hints.md#hint-2) · [Solution](no_tool_needed_solution.md)

### Intermediate Version

```
NO_TOOL_PROMPTS = [3 questions no tool can help with]

check_no_tool(prompt) -> bool: len(run_agent(prompt).steps) == 0

main: for each prompt, print a case line; then "N/3 answered without a tool"
```

Write it, then compare against the [Solution](no_tool_needed_solution.md).

**Difference between Basic and Intermediate:** Basic is one check. Intermediate is a small, repeatable test.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-no_tool_needed) · [Hint 1](no_tool_needed_hints.md#hint-1) · [Hint 2](no_tool_needed_hints.md#hint-2) · [Solution](no_tool_needed_solution.md)

Full solution: [Show me the solution](no_tool_needed_solution.md)
