# Real-world — a support-reply router — Hints

> [Back to the exercise](../README.md#ex-runnable_routing) · [Hint 1](runnable_routing_hints.md#hint-1) · [Hint 2](runnable_routing_hints.md#hint-2) · [Solution](runnable_routing_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried.

- [Hint 1 — One reply chain per category, then branch](#hint-1)
- [Hint 2 — The plan, and how to prove routing](#hint-2)

## Hint 1 — One reply chain per category, then branch {: #hint-1 }

Keep each part in its own small function so the pipeline reads like a sentence:

- `build_reply_chain(model, system_text) -> Runnable` — one category's chain.
- `build_router(model) -> Runnable` — the `RunnableBranch` over all categories.
- `build_pipeline(model) -> Runnable` — `build_router(model) | RunnableLambda(tag_reply)`.
- The default (last) argument to `RunnableBranch` has **no condition** — it's what runs when nothing matched. Don't forget it, or an unknown category raises.

## Hint 2 — The plan, and how to prove routing {: #hint-2 }

To prove routing **without** spending a token, give each branch a tiny fake model that echoes the system line it was handed. Then the reply tells you which branch ran:

```
fake model: return AIMessage(content = the system message it received)
test 1: billing -> reply mentions "billing agent";
        technical -> "tech-support agent"; sales -> "general support agent"
test 2: an unknown category -> the default branch, and "(auto-routed)" is there
```

Because the branch condition is on `ticket["category"]`, not on the model's words, the fake model is enough to prove the routing is correct. Then run `main()` once with a real `ChatOpenAI` to see real replies.

Full solution: [Show me the solution](runnable_routing_solution.md)
