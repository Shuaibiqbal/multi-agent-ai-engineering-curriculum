# Step 4 — A Router That Sends Each Message to the Right Agent Automatically — Hints

> [Back to this step](../READING_README.md#step-4-a-router-that-sends-each-message-to-the-right-agent-automatically-final-2-agents) · [Hint 1](step4_router_hints.md#hint-1) · [Hint 2](step4_router_hints.md#hint-2) · [Solution](step4_router_solution.md)

Only 2 hints — work through them in order. Each has 2 depth levels: **Basic** (the plain idea) and **Intermediate** (the shape of the real code).

- [Hint 1 — What the router decides, and how](#hint-1)
- [Hint 2 — The plan, and where every piece moves](#hint-2)

<hr class="page-break">

> [Back to this step](../READING_README.md#step-4-a-router-that-sends-each-message-to-the-right-agent-automatically-final-2-agents) · [Hint 1](step4_router_hints.md#hint-1) · [Hint 2](step4_router_hints.md#hint-2) · [Solution](step4_router_solution.md)

## Hint 1 — What the router decides, and how {: #hint-1 }

### Basic Version

The router answers one question per message: **Concierge or Triage?** Start with the simplest version — a keyword list:

```python
TRIGGER_WORDS = ["charged", "broken", "refund", "crash", "can't log"]
```

Lowercase the message, loop over the words, and return `"triage"` on the first match, `"concierge"` otherwise.

Then try messages that break it: "the app freezes on login" (no trigger word) and "what's your refund policy?" (a trigger word, but just a question). Seeing these fail is the reason for the Intermediate version.

<hr class="page-break">

> [Back to this step](../READING_README.md#step-4-a-router-that-sends-each-message-to-the-right-agent-automatically-final-2-agents) · [Hint 1](step4_router_hints.md#hint-1) · [Hint 2](step4_router_hints.md#hint-2) · [Solution](step4_router_solution.md)

### Intermediate Version

Make the router a small structured-output call — the same `.parse(...)` you used for Triage, with a new schema:

```python
class RouteDecision(BaseModel):
    agent: Literal["concierge", "triage"]
    reason: str
```

`decide(client, message) -> RouteDecision` in `agents/router.py`:

- Start with a safe default: `RouteDecision(agent="concierge", reason="router could not decide")`.
- Inside `try`, call `.parse(...)` with `prompts/router.txt` as the system prompt. If `reply.parsed is not None`, use it (it's `None` when the model refused).
- `except ValidationError` → log a warning and keep the default.
- Always end with one `logger.info(...)` line: agent, reason, message.

Why Concierge as the default: a wrong chat reply is harmless; a wrong ticket is not.

<hr class="page-break">

> [Back to this step](../READING_README.md#step-4-a-router-that-sends-each-message-to-the-right-agent-automatically-final-2-agents) · [Hint 1](step4_router_hints.md#hint-1) · [Hint 2](step4_router_hints.md#hint-2) · [Solution](step4_router_solution.md)

## Hint 2 — The plan, and where every piece moves {: #hint-2 }

### Basic Version

```
loop:
    message = input(...)
    if decide(message) == "triage":
        show triage_agent(client, message)
    else:
        concierge_agent(client, history, message)
```

For that, the chat code moves out of `main.py` into `agents/concierge.py`:

- `start_history()` returns `[system message from concierge.txt]`.
- `concierge_agent(client, history, message)` trims, then calls `stream_message()`.

`MAX_HISTORY_TOKENS` moves with it.

<hr class="page-break">

> [Back to this step](../READING_README.md#step-4-a-router-that-sends-each-message-to-the-right-agent-automatically-final-2-agents) · [Hint 1](step4_router_hints.md#hint-1) · [Hint 2](step4_router_hints.md#hint-2) · [Solution](step4_router_solution.md)

### Intermediate Version

Put the flow in `services/desk_service.py` (plus an empty `services/__init__.py`):

```
handle_message(client, history, message):
    decision = decide(client, message)
    if decision.agent == "triage":
        ticket = triage_agent(client, message)
        None → "couldn't turn that into a ticket"; else print_ticket(ticket)
    else:
        print("Concierge: ", end="", flush=True)
        concierge_agent(client, history, message)
```

`print_ticket()` moves here from `main.py`. `main.py` shrinks to: startup, `history = start_history()`, the input loop, and **Step 3's exact `except` blocks** around `handle_message(...)`. Remove `/extract`.

Last, add a `"routing"` list to `messages.json` — `{"message": ..., "expected": "concierge"}` items. Add a `test_routing()` that prints `OK` or `WRONG` for each one, and a unit case showing `RouteDecision(agent="billing", ...)` raises `ValidationError`.

Full solution: [Show me the solution](step4_router_solution.md)
