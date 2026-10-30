# Basic (cold recall) — Solution

> [Back to the exercise](../README.md#ex-cold_recall) · [Hint 1](cold_recall_hints.md#hint-1) · [Hint 2](cold_recall_hints.md#hint-2) · [Solution](cold_recall_solution.md)

**Story — `cold_recall.md`:** recognizing a fact while the reference page is open in front of you, and recalling it cold, out loud, weeks later with no notes, are genuinely different skills — and only the second one is ever actually tested in a real interview. This exercise practices recalling one real question cold, at every depth level. **If not:** the very first cold recall you ever attempted would be live, in front of an interviewer, with the job on the line.

Write your own answer first, in `practice/cold_recall.md`, then compare.

**Question used for this model answer (from Doc01's Interview Topics Preview):** "Why does logging beat `print()` in production?"

## Solution

**Story:** this is the same answer, but with its real underlying mechanism actually named (logging levels, handlers), still delivered inside the 30-45 second target — rung 1 of the Four-Depth Format done properly, not just recited. **If not:** your answer would sound memorized rather than genuinely understood, and a good interviewer can always tell the difference.

"Logging beats `print()` in production because it separates *what* gets recorded from *where* it goes and *how much* you see — `print()` conflates all three into one hard-coded statement. Logging gives you severity levels — `DEBUG` through `CRITICAL` — so you can leave detailed instrumentation in the code permanently and control verbosity through configuration, not code changes. And handlers decouple output destination from the log call itself, so the same line can go quietly to a file in production and loudly to the console while you're debugging locally — without touching a single log statement."

**Why this answer works:** it's rung 1 of this document's Four-Depth Format, done properly — it leads with the claim in one sentence, then backs it with the *specific mechanism* (levels + handlers) rather than a vague "it's more professional." It uses precise vocabulary (severity levels, handlers, decoupling) that signals real understanding, not memorized phrasing. It stays inside the 30-45 second window instead of turning into a full lecture on the `logging` module — climbing to rungs 2-4 of the Four-Depth Format is a different answer, for a different, deeper question.
