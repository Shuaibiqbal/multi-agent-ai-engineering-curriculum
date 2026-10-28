# Real-world (how long can this conversation actually go?) — Solution

> [Back to the exercise](../README.md#ex-context_window_capacity) · [Hint 1](context_window_capacity_hints.md#hint-1) · [Hint 2](context_window_capacity_hints.md#hint-2) · [Solution](context_window_capacity_solution.md)

**Story — `context_window_capacity_practice.md`:** "how long can this conversation go?" decides whether you need history trimming at all. Working it out once, with real numbers, turns a guess into a design input. **If not:** a chatbot would work in testing and fail on long real conversations.

## Solution

**Story:** the same formula with a safety margin, because real turns vary and the reply needs room too. **If not:** you'd trim exactly at the limit and still overflow on a long reply.

```
window_size            = 128_000
system_prompt_tokens   = 100
avg_user_message_tokens = 50
avg_reply_tokens        = 300
avg_turn_tokens         = avg_user_message_tokens + avg_reply_tokens   # 350

safety_margin           = 0.75      # start trimming at 75% full, not 100%
usable_budget           = (window_size - system_prompt_tokens) * safety_margin
                        = 127_900 * 0.75
                        = 95_925

turns_before_trimming   = usable_budget / avg_turn_tokens
                        = 95_925 / 350
                        = about 274 turns
```

The two numbers that matter most for how this estimate holds up in a real feature: **average message length** (a document-Q&A feature where users paste in paragraphs has a far smaller turn ceiling than a short-message support chatbot — redo the math with the real average, not a generic guess), and **the safety margin** (100% is not a safe target — a single long reply can push you over the edge with no warning if you're targeting the hard limit).
