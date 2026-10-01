# Step 4 — Stream the Reply Live and Build One Structured Record per Ticket — Hints

> [Back to this step](../READING_README.md#step-4-stream-the-reply-live-and-build-one-structured-record-per-ticket) · [Hint 1](step4_structured_output_streaming_hints.md#hint-1) · [Hint 2](step4_structured_output_streaming_hints.md#hint-2) · [Solution](step4_structured_output_streaming_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've really tried. Each hint starts with the plain idea, then shows the shape of the real code.

- [Hint 1 — One reply, two shapes](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

<hr class="page-break">

> [Back to this step](../READING_README.md#step-4-stream-the-reply-live-and-build-one-structured-record-per-ticket) · [Hint 1](step4_structured_output_streaming_hints.md#hint-1) · [Hint 2](step4_structured_output_streaming_hints.md#hint-2) · [Solution](step4_structured_output_streaming_solution.md)

## Hint 1 — One reply, two shapes {: #hint-1 }

Every chain is a `Runnable`, so it already has `.stream()` (Doc05's LCEL topic). Instead of one `.invoke()` result, you get small text pieces as the model writes them:

```
reply = ""
for chunk in chain.stream(inputs):
    print(chunk, end="", flush=True)
    reply = reply + chunk
```

`flush=True` makes each piece appear at once — the same trick as Project 1's streaming. The joined `reply` is the full text, for the record.

The record is built from that **same** `reply` — never from a second model call, which could say something different.

`TicketRecord` in `schemas.py` only **adds** two fields, both with defaults:

```
needs_human_review: bool = False
review_reasons:     list[str] = []
```

<hr class="page-break">

> [Back to this step](../READING_README.md#step-4-stream-the-reply-live-and-build-one-structured-record-per-ticket) · [Hint 1](step4_structured_output_streaming_hints.md#hint-1) · [Hint 2](step4_structured_output_streaming_hints.md#hint-2) · [Solution](step4_structured_output_streaming_solution.md)

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

```
handle_ticket(ticket, customer_id):
    category = classify_ticket(ticket)
    chain = build_reply_chain(category.category)
    reply = stream_reply(chain, inputs)
    used_fallback = reply == FALLBACK_REPLY
    reasons = review_reasons(category, used_fallback)
    return TicketRecord(..., needs_human_review=len(reasons) > 0,
                        review_reasons=reasons)
```

`review_reasons(category, used_fallback) -> list[str]` — plain rules, one `if` each:

- the fallback reply was sent;
- the ticket could fit more than one category (`sure` is `False`).

A list, not one `True`: the person reviewing sees **why**. Test each rule with hand-made inputs in `tests/unit/test_review.py` — no API key needed. Then check the unclear sample ticket really gets flagged in the integration test.

Full solution: [Show me the solution](step4_structured_output_streaming_solution.md)
