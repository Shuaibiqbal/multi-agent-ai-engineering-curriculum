# Basic (typed function + custom error) — Hints

> [Back to the exercise](../README.md#ex-basic1) · [Hint 1](basic1_hints.md#hint-1) · [Hint 2](basic1_hints.md#hint-2) · [Solution](basic1_solution.md)

**Where this exercise is saved:** `practice/custom_errors_practice.py`, under its `# Basic` section — the same file also holds the [Failure handling exercise](../README.md#ex-failure_handling), under a `# Failure handling` section. Run it with `cd practice && python custom_errors_practice.py`.

**Used later by:** the [Real-world wiring exercise](../README.md#ex-config_logging_wiring) and the [Build Task](../README.md#build-task-config-logging-foundation). Neither imports this file — they re-write the same one-line custom-error pattern as `MissingConfigError` in `practice/config_logging_wiring/exceptions.py` and `practice/build_task/exceptions.py`.

Only 2 hints — work through them in order, and don't jump ahead until you've genuinely tried. Each hint has 2 depth levels: **Basic** (the plain idea) and **Intermediate** (proper Python). Read Basic first even if you already know Python — it's the fastest way to spot exactly what Intermediate adds.

- [Hint 1 — The idea, and the exact pieces](#hint-1)
- [Hint 2 — The plan, and almost the whole thing](#hint-2)

<hr class="page-break">

> [Back to the exercise](../README.md#ex-basic1) · [Hint 1](basic1_hints.md#hint-1) · [Hint 2](basic1_hints.md#hint-2) · [Solution](basic1_solution.md)

## Hint 1 — The idea, and the exact pieces {: #hint-1 }

### Basic Version

You need two things: a custom error, and a function that uses it.

A custom error is just a name for a specific kind of problem. In Python, you make one by writing a small class that is a type of `Exception`.

The function should check its input. If the input is bad (like a negative age), it should raise your custom error instead of continuing. Think about it like this: "if the age is less than 0, something is wrong — stop and say so, using my own error name, not a generic one."

Here are the exact pieces you need:

- To make your own error: `class InvalidAgeError(Exception): pass`
- To trigger it: `raise InvalidAgeError("your message here")`
- To catch it and see the message: `try: ... except InvalidAgeError as e: print(e)`

<hr class="page-break">

> [Back to the exercise](../README.md#ex-basic1) · [Hint 1](basic1_hints.md#hint-1) · [Hint 2](basic1_hints.md#hint-2) · [Solution](basic1_solution.md)

### Intermediate Version

The exercise is really about two Python features working together: a custom exception class, and full type hints on a function.

A custom exception is a class that inherits from `Exception`:
```python
# practice/custom_errors_practice.py — Basic section
class InvalidAgeError(Exception):
    pass
```
`pass` means the class body is empty — you don't need any extra code inside it for a basic custom exception. The class *existing*, with this specific name, is what makes it useful: it lets calling code catch this *one* problem specifically, instead of catching every possible exception with a broad `except Exception`.

The function's type hints should describe its contract precisely:
```python
# practice/custom_errors_practice.py — Basic section
def set_age(age: int) -> None:
```
This tells any reader — without looking at the function body — that it takes an `int` and returns nothing (`None`).

Look specifically at:

- **Exception subclassing:** you're inheriting all of `Exception`'s behavior (the message, the traceback machinery) for free, and only adding a distinct *name* the code can catch.
- **The `raise` statement:** `raise InvalidAgeError(f"age cannot be negative: {age}")` — an f-string here lets you embed the actual bad value in the message.
- **Catching it specifically:** `except InvalidAgeError as e:` — binding the caught exception to `e` lets you access `str(e)` (its message).

**Difference between Basic and Intermediate:** Basic gives you the ingredients and exact syntax pieces in plain words. Intermediate explains what each piece of that syntax actually does — this is the depth the exercise's Solution is written at.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-basic1) · [Hint 1](basic1_hints.md#hint-1) · [Hint 2](basic1_hints.md#hint-2) · [Solution](basic1_solution.md)

## Hint 2 — The plan, and almost the whole thing {: #hint-2 }

### Basic Version

```
make a new error type called InvalidAgeError

make a function called set_age that takes one number (age):
    if age is less than 0:
        stop, and raise InvalidAgeError, with a message about the bad age
    if age is 0 or more, do nothing, it's fine

test it:
    call set_age(25) -> nothing happens, it's valid
    call set_age(-5) inside a try/except
        -> catch InvalidAgeError, print the message
```

Here's almost the whole thing — just try running it and reading it line by line:
```python
# practice/custom_errors_practice.py — Basic section
class InvalidAgeError(Exception):
    pass

def set_age(age):
    if age < 0:
        raise InvalidAgeError("age cannot be negative")
```
**Expected output if you run just this (nothing calls `set_age` yet):** nothing — defining a class and a function doesn't run either of them.

What's missing: the type hints (`age: int`, `-> None`), and the two test calls (one good, one bad, with `try/except`). Add those yourself, then check the [Solution](basic1_solution.md).

<hr class="page-break">

> [Back to the exercise](../README.md#ex-basic1) · [Hint 1](basic1_hints.md#hint-1) · [Hint 2](basic1_hints.md#hint-2) · [Solution](basic1_solution.md)

### Intermediate Version

```
define:
    class InvalidAgeError(Exception): pass

define:
    def set_age(age: int) -> None:
        if age < 0:
            raise InvalidAgeError(f"age cannot be negative: {age}")
        # implicitly returns None if age is valid — no else branch needed

test:
    set_age(25)                          # runs to completion, no output
    try:
        set_age(-5)
    except InvalidAgeError as e:
        print(f"Caught: {e}")
```
Notice there's no `else` branch needed — if the `if` condition is false, the function just falls through and returns `None` naturally.

```python
# practice/custom_errors_practice.py — Basic section
class InvalidAgeError(Exception):
    pass


def set_age(age: int) -> None:
    if age < 0:
        raise InvalidAgeError(f"age cannot be negative: {age}")
```
What's missing: the two test calls. Write them yourself:
```python
# practice/custom_errors_practice.py — Basic section
set_age(25)  # should run with no output

try:
    set_age(-5)
except InvalidAgeError as e:
    ...  # what goes here?
```

Finish it yourself, then compare against the [Solution](basic1_solution.md).

**Difference between Basic and Intermediate:** same underlying idea (check, raise, catch) at 2 completeness levels, shown here both as pseudocode and as near-complete code — Basic proves the concept works, Intermediate adds the type contract real Python expects.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-basic1) · [Hint 1](basic1_hints.md#hint-1) · [Hint 2](basic1_hints.md#hint-2) · [Solution](basic1_solution.md)

Full solution: [Show me the solution](basic1_solution.md)
