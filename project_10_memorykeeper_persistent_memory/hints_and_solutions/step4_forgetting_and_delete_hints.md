# Step 4 — Forgetting, and a Privacy-Respecting Delete — Hints

> [Back to the step](../READING_README.md#step-4-forgetting-and-a-privacy-respecting-delete) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](step4_forgetting_and_delete_solution.md)

- [Hint 1 — The idea, and why one key isn't enough](#hint-1)
- [Hint 2 — The plan, and proving it](#hint-2)

## Hint 1 — The idea, and why one key isn't enough {: #hint-1 }

A real "forget me" deletes **everything** about a user, not one key. By Step 3 the Store may hold several keys (`preferred_name`, a preference, …). So:

```python
def forget_user(store, user_id):
    ns = namespace_for(user_id)
    for item in store.search(ns):     # list every item first
        store.delete(ns, item.key)    # then delete each
```

`search` the namespace to discover the keys — don't assume there's only one. Wire a `forget_me` command into `main.py`'s loop.

## Hint 2 — The plan, and proving it {: #hint-2 }

```
store.py:  forget_user(store, user_id) -> deletes every item, returns count
main.py:   if text == "forget_me":
               forget_user(store, user_id); print(...); continue
test_store: save two facts -> forget_user
            -> assert recall_facts == [] and count == 2
integration: say name -> forget_user -> a new thread recalls nothing
```

The proof that matters is the **fresh run after the forget**: `recall_node` returns nothing, so the model genuinely has no idea who you are. A delete you can't prove emptied the store isn't a real forget. The whole file set is in the [Solution](step4_forgetting_and_delete_solution.md).
