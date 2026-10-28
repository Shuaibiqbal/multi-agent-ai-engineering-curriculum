# Real-world (how long can this conversation actually go?) — Hints

> [Back to the exercise](../README.md#ex-context_window_capacity) · [Hint 1](context_window_capacity_hints.md#hint-1) · [Hint 2](context_window_capacity_hints.md#hint-2) · [Solution](context_window_capacity_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried. Each hint builds toward the full solution.

- [Hint 1 — The idea, and the formula](#hint-1)
- [Hint 2 — A worked example, and the trimming decision](#hint-2)

## Hint 1 — The idea, and the formula {: #hint-1 }

The context window is a fixed token budget for the whole call, shared by the system prompt, every prior message in the resent history, and the room the model needs left over to write its reply. Nothing about the window itself distinguishes "old messages" from "new reply" — it's one number, consumed from all sides.

Build the estimate as a small budget, not one giant division:

- Reserve tokens for the system prompt (fixed, paid every single call).
- Reserve tokens for the model's own reply room (budget generously — replies often run longer than the user's message).
- Whatever's left over is what turns get to share.

`turns_that_fit = (window_size - system_prompt_tokens) / average_tokens_per_turn`

Pick a window size and an average turn size before moving to Hint 2.

Keep in mind the formula assumes every turn is the same size — real conversations never are. A support chat has short turns throughout. A document-Q&A feature has one huge turn (the pasted document) followed by short follow-ups. A safety margin (start trimming at 75% full, not 100%) is what actually protects you from that unevenness, not a more precise average.

## Hint 2 — A worked example, and the trimming decision {: #hint-2 }

```
window_size = 128_000
system_prompt_tokens = 100
avg_user_message_tokens = 50
# replies tend to run longer than a short user message
avg_reply_tokens = 300
avg_turn_tokens = avg_user_message_tokens + avg_reply_tokens   # 350

leftover = window_size - system_prompt_tokens                  # 127,900
turns_that_fit = leftover / avg_turn_tokens   # about 365 turns
```

Notice how much the estimate moved (1,279 turns down to about 365) just from being honest that replies usually run longer than the user's own message.

A common real-world rule is to start trimming or summarizing older messages once you've used somewhere around 70-80% of the window, not 100% — that leaves headroom for an unusually long reply and avoids a hard failure appearing suddenly mid-conversation.

Two design details worth writing down alongside your number, for when this becomes real code: never trim the system prompt (it's not part of history, it's a fixed instruction), and never trim the most recent turn or two (the model needs the immediate context to make sense of a follow-up question like "what about the second one?").

Write your final turn estimate, the percentage where you'd start trimming, and these two rules, then compare against the [Solution](context_window_capacity_solution.md).

Full solution: [Show me the solution](context_window_capacity_solution.md)
