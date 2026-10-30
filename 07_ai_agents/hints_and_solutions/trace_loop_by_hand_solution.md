# Basic (trace the loop on paper) — Solution

> [Back to the exercise](../README.md#ex-trace_loop_by_hand) · [Hint 1](trace_loop_by_hand_hints.md#hint-1) · [Hint 2](trace_loop_by_hand_hints.md#hint-2) · [Solution](trace_loop_by_hand_solution.md)

**Story — `react_loop_practice.py`:** if you can't trace a ReAct loop by hand, on paper — writing out each think → act → observe turn and what the model sees at each one — you can't debug it in code either. Doing it on paper first is the cheapest possible way to catch a wrong mental model, before a single line of Python is at stake. **If not:** the first time you'd trace a loop's real steps would be inside a debugger, under time pressure, with no smaller version of this skill to fall back on.

## Solution

Task: "Convert 100 US dollars to euros, then tell me if that's enough for a 90-euro hotel room."

```
round 1:
    thought: I need the USD→EUR conversion for $100 before I can compare
             it to anything.
    action: convert_currency(amount=100, from_currency="USD", to_currency="EUR")
    observation: 92.50

round 2:
    thought: 92.50 EUR vs. a 90 EUR room — I can compare these two numbers
             myself, I don't need a tool for basic arithmetic comparison.
    final answer: Yes — $100 converts to about €92.50, which covers the
                  €90 room, with about €2.50 left over.
```
