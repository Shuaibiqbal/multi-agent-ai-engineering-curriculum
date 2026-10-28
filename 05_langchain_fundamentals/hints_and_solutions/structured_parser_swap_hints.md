# Intermediate (swap in a structured parser) — Hints

> [Back to the exercise](../README.md#ex-structured_parser_swap) · [Hint 1](structured_parser_swap_hints.md#hint-1) · [Hint 2](structured_parser_swap_hints.md#hint-2) · [Solution](structured_parser_swap_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried. Each hint builds toward the full solution.

- [Hint 1 — The idea, and the exact pieces](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

## Hint 1 — The idea, and the exact pieces {: #hint-1 }

`.with_structured_output(Person)` returns a new runnable whose output is already a `Person`, not text. With `gpt-4o-mini` it uses the same constrained decoding as Doc04's `.parse()` — the "shape during" method from the Output parsers topic.

That means a text with no person in it does **not** raise an error: the model **must** fill the form, so with `name: str` and `age: int` it invents something (`''` and `0`, for example). The fix is Doc04's rule again — `str | None` and `int | None` — so "nothing found" becomes a real answer.

A `ValidationError` is still possible (the reply fails the model in a rare case), so catch it by name.

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

```
class Person: name: str | None, age: int | None

function extract_person(text) -> Person | None:
    try: person = structured_model.invoke(text)
    except ValidationError: return None
    if name is None and age is None: return None
    return person
```

This is the same shape as Doc04's `extract_info()` — only the call changed from `client.beta.chat.completions.parse(...)` to `.invoke(...)`. Write it, run it on both texts, then compare against the [Solution](structured_parser_swap_solution.md).

Full solution: [Show me the solution](structured_parser_swap_solution.md)
