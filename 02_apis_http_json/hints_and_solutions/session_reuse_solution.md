# Real-world (one reusable session) — Solution

> [Back to the exercise](../README.md#ex-session_reuse) · [Hint 1](session_reuse_hints.md#hint-1) · [Hint 2](session_reuse_hints.md#hint-2) · [Solution](session_reuse_solution.md)

**Story — `session_reuse_practice.py`:** headers passed by hand to every call are a typo waiting to happen — one call in five forgets the `Authorization` header, and nothing tells you until a request mysteriously gets rejected. One shared `Session`, configured once, makes that mistake structurally impossible. **If not:** `http_client.py` in the Build Task would open a new connection and re-specify headers on every single call, slower and more fragile than it needs to be.

## Basic Version

### Approach 1 — a module-level session

```python
# session_reuse_practice.py
import requests

session = requests.Session()
session.headers.update({"Authorization": "Bearer fake-token"})

urls = [
    "https://api.github.com",
    "https://api.github.com/zen",
    "https://api.github.com/octocat",
]

for url in urls:
    response = session.get(url)
    print(url, "->", response.status_code)

print("Authorization header set to:", session.headers["Authorization"])
```
**Expected output:**
```
https://api.github.com -> 200
https://api.github.com/zen -> 200
https://api.github.com/octocat -> 200
Authorization header set to: Bearer fake-token
```

This works and proves the header sticks across calls. It doesn't yet confirm the header was actually *sent* on the wire, just that it's set on the session object — the Intermediate version checks that distinction.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-session_reuse) · [Hint 1](session_reuse_hints.md#hint-1) · [Hint 2](session_reuse_hints.md#hint-2) · [Solution](session_reuse_solution.md)

## Intermediate Version

### Approach 1 — a typed factory function

```python
# session_reuse_practice.py
import requests


def make_authenticated_session(token: str) -> requests.Session:
    # why: one shared Session with the header set once, instead of passing
    # the same headers dict to every call by hand where it can drift or get
    # missed.
    # when: call this once, at the start of the program — treat the
    # returned session's headers as read-only after this point.
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session


def main() -> None:
    session = make_authenticated_session("fake-token")

    urls = [
        "https://api.github.com",
        "https://api.github.com/zen",
        "https://api.github.com/octocat",
    ]

    for url in urls:
        # how: session.get(...), not requests.get(...) — this is what makes
        # the Authorization header go out automatically on every call.
        response = session.get(url)
        print(f"{url} -> {response.status_code}")

    # how: response.request.headers reads back what was actually sent over
    # the wire, not just what's configured on the session object.
    sent_header = response.request.headers.get("Authorization")
    print(f"header actually sent on the last request: {sent_header}")


if __name__ == "__main__":
    main()
```
**Expected output:**
```
https://api.github.com -> 200
https://api.github.com/zen -> 200
https://api.github.com/octocat -> 200
header actually sent on the last request: Bearer fake-token
```
`response.request.headers` reads back the *actual* request object `requests` sent, not the session's own dict — confirming the header genuinely went out over the wire, not just that it's set somewhere in Python.

**Difference from Basic:** a named, typed factory function (`make_authenticated_session`) instead of module-level statements is reusable and importable, and checking `response.request.headers` instead of `session.headers` confirms the header was actually transmitted, not just configured.

**Which one should you actually write?** This factory function is enough for a script or a one-off tool with a single, short-lived call site — including this document's Build Task, which holds one module-level `Session` for the whole wrapper. Configure headers once, right after creating the session, and treat them as read-only after that — the moment more than one part of a program might mutate a shared session's headers from different places is the moment that discipline starts to matter.
