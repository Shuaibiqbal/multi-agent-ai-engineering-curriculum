# Real-world (how long can this conversation actually go?) — Solution

> [Back to the exercise](../README.md#ex-context_window_capacity) · [Hint 1](context_window_capacity_hints.md#hint-1) · [Hint 2](context_window_capacity_hints.md#hint-2) · [Solution](context_window_capacity_solution.md)

**Story — `context_window_capacity_practice.md`:** "how long can this conversation go?" decides whether you need history trimming at all. Working it out once, with real numbers, turns a guess into a design input. **If not:** a chatbot would work in testing and fail on long real conversations.

## Basic Version

**Story:** the straight calculation — the window, minus the system prompt, divided by an average turn. **If not:** you'd find the limit when a user hits it.

Chosen numbers: a 128,000-token context window, a short-message chat feature where each user message is about 50 tokens and each reply is about 300 tokens.

```
one turn = 50 + 300 = 350 tokens
room after the system prompt (100 tokens) = 128,000 - 100 = 127,900
turns that fit = 127,900 / 350 = about 365 turns
```

About 365 back-and-forth turns before the window is technically full. In practice, you'd start trimming or summarizing older messages well before that — around 70-80% full (roughly turn 255-290) — so a single unusually long reply never suddenly overflows the window with no warning.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-context_window_capacity) · [Hint 1](context_window_capacity_hints.md#hint-1) · [Hint 2](context_window_capacity_hints.md#hint-2) · [Solution](context_window_capacity_solution.md)

## Intermediate Version

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

**Difference from Basic:** same formula, but with a safety margin built in (274 turns before trimming, vs. 365 turns before the window is technically full) — the Basic Version answers "when does this break," the Intermediate Version answers the more useful question, "when should I act before it breaks."

**Which one should you actually write?** For a quick feasibility check while designing a feature ("do I even need trimming logic, or is this conversation short-lived by nature?"), the Basic Version's back-of-envelope math is enough. For an actual production chat feature, the Intermediate Version's safety margin is the number to actually build around — track the real running total per conversation using `tiktoken` or the token count the API reports back, start trimming at that margin, and never trim the system prompt or the most recent turn or two (a follow-up question like "what about the second one?" is meaningless without the turn it's referring to). A single precomputed "turn limit," even with a safety margin, is a planning number — real code checks the running total fresh, since real conversations have wildly uneven turn sizes (one huge pasted document, then short follow-ups).
