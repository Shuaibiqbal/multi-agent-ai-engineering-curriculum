# Failure/choice — pick the right tool — Hints

> [Back to the exercise](../README.md#ex-framework_choice) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](framework_choice_solution.md)

- [Hint 1 — ask one question](#hint-1)
- [Hint 2 — the mapping](#hint-2)

## Hint 1 — ask one question {: #hint-1 }

For each scenario, ask: **who is the user, and what do they need around the AI?**

- A person, and you need it *fast*? → the lightest UI.
- *Code* calling it? → an API.
- Users, logins, stored data, an admin? → the heavyweight that includes those.

The AI is the same every time — the answer is entirely about the app around it.

## Hint 2 — the mapping {: #hint-2 }

```
demo / "due tonight" / data app        -> Streamlit
JSON for another app or service        -> FastAPI
small custom web app you control       -> Flask
product with users + saved data + admin -> Django
a chatbot front for an agent           -> Streamlit (st.chat_input)
```

Write one sentence of *why* for each — the "why" is the actual exercise. If two feel close (Flask vs Streamlit for an internal tool), the tie-breaker is: do you need real routes and custom HTML (Flask), or is "a page with a box" enough (Streamlit)? The full reasoning is in the [Solution](framework_choice_solution.md).
