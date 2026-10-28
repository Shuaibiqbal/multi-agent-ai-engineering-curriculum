# Failure (force the parser to actually fail) — Hints

> [Back to the exercise](../README.md#ex-parser_failure_handling) · [Hint 1](parser_failure_handling_hints.md#hint-1) · [Hint 2](parser_failure_handling_hints.md#hint-2) · [Solution](parser_failure_handling_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried. Each hint builds toward the full solution.

- [Hint 1 — Forcing a real failure: "check after"](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

## Hint 1 — Forcing a real failure: "check after" {: #hint-1 }

The error is `OutputParserException` (from `langchain_core.exceptions`) — catch it by name, never a bare `except`, so a network error or a bad key still fails loudly.

Then fix the cause, not just the symptom: tell the model the shape. `parser.get_format_instructions()` returns that text, and `.partial(format_instructions=...)` fills a `{format_instructions}` slot once, so callers still pass only `{thing}` (the Prompt templates topic).

`parser.parse("some text")` checks any text with no API call — a free way to test the failure again.

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

```
BROKEN_TEMPLATE = "Rate {thing} from 1 to 10."
FIXED_TEMPLATE  = "Rate {thing} from 1 to 10.\n{format_instructions}"

function build_rating_chain(template) -> Runnable:
    prompt from the template
    if the template has {format_instructions}: fill it with .partial()
    return prompt | model | parser

function get_rating(chain, thing) -> Rating | None:
    try: return chain.invoke(...)
    except OutputParserException: return None
```

Run the broken chain, the fixed chain, and `parser.parse("I'd say eight")`, then compare against the [Solution](parser_failure_handling_solution.md).

Full solution: [Show me the solution](parser_failure_handling_solution.md)
