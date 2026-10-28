# Basic (cold recall) — Solution

> [Back to the exercise](../README.md#ex-cold_recall) · [Hint 1](cold_recall_hints.md#hint-1) · [Hint 2](cold_recall_hints.md#hint-2) · [Solution](cold_recall_solution.md)

**Story — `cold_recall.md`:** knowing a fact while the page is open and saying it cold, weeks later, are different skills — only the second one is tested in an interview. This exercise practices it on one real question, at every depth. **If not:** the first cold recall you ever did would be in front of an interviewer.

Write your own answer first, in `practice/cold_recall.md`, then compare.

**Question used for this model answer (from Doc01's Interview Topics Preview):** "Why does logging beat `print()` in production?"

## Solution

**Story:** the same answer with its real mechanism named (levels, handlers), still inside 30-45 seconds — rung 1 of the Four-Depth Format done properly. **If not:** your answer would sound memorized instead of understood.

"Logging beats `print()` in production because it separates *what* gets recorded from *where* it goes and *how much* you see — `print()` conflates all three into one hard-coded statement. Logging gives you severity levels — `DEBUG` through `CRITICAL` — so you can leave detailed instrumentation in the code permanently and control verbosity through configuration, not code changes. And handlers decouple output destination from the log call itself, so the same line can go quietly to a file in production and loudly to the console while you're debugging locally — without touching a single log statement."

**Why this answer works:** it's rung 1 of this document's Four-Depth Format, done properly — it leads with the claim in one sentence, then backs it with the *specific mechanism* (levels + handlers) rather than a vague "it's more professional." It uses precise vocabulary (severity levels, handlers, decoupling) that signals real understanding, not memorized phrasing. It stays inside the 30-45 second window instead of turning into a full lecture on the `logging` module — climbing to rungs 2-4 of the Four-Depth Format is a different answer, for a different, deeper question.
