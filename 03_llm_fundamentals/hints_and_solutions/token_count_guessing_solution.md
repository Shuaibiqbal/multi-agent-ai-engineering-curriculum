# Basic (guess token counts, then check) — Solution

> [Back to the exercise](../README.md#ex-token_count_guessing) · [Hint 1](token_count_guessing_hints.md#hint-1) · [Hint 2](token_count_guessing_hints.md#hint-2) · [Solution](token_count_guessing_solution.md)

**Story — `token_count_guessing_practice.md`:** every cost and every context limit is counted in tokens, not words. Guessing first and then checking shows where the quick rule works and where it breaks. **If not:** you'd plan prompts and budgets with a rule you've never tested.

## Basic Version

### Approach 1 — word count × 1.3

**Story:** the simplest estimate, checked against the real tokenizer on a few kinds of text. **If not:** you'd trust words × 1.3 everywhere, including where it's badly wrong.

There's no single "correct" set of 5 sentences — this is about the process, not a fixed answer. Here's a worked example table you can compare your own results against:

| Sentence | Words | Guess (words × 1.3) | Actual tokens (check yourself) |
|---|---|---|---|
| "Hi." | 1 | ~1-2 | usually 1-2 |
| "The cat sat on the mat." | 6 | ~8 | usually 6-8 |
| "Unbelievably, the antidisestablishmentarianism debate continued." | 4 | ~5 | usually 9-11 — the guess is way off |
| "print('hello world')" | 2 (code) | ~3 | usually 5-7 — code tokenizes differently than prose |
| "میں آج بازار جا رہا ہوں" (Urdu) | 5 | ~7 | usually much higher — non-English text uses more tokens per word |

**What this shows:** the word-count guess works fine for short, plain, common English. It breaks down fast on long/uncommon words, code, and non-English text — exactly the pattern Doc03's Core Concepts warned about.

<hr class="page-break">

> [Back to the exercise](../README.md#ex-token_count_guessing) · [Hint 1](token_count_guessing_hints.md#hint-1) · [Hint 2](token_count_guessing_hints.md#hint-2) · [Solution](token_count_guessing_solution.md)

## Intermediate Version

### Approach 1 — chars ÷ 4 and words × 1.3, side by side

**Story:** two quick estimates next to the real count, so you can see which one fails on which kind of text — and why. **If not:** you'd keep one rule of thumb and never notice its blind spots.

The same table, with both estimation methods shown side by side, and the actual mechanism explained for each surprising row:

| Sentence | Char ÷ 4 | Words × 1.3 | Actual | Why the gap (if any) |
|---|---|---|---|---|
| "Hi." | ~1 | ~1-2 | 1-2 | No gap — trivially short, matches the rule directly. |
| "The cat sat on the mat." | ~7 | ~8 | 6-8 | Both estimates land close — this is the "average English sentence" the rule of thumb is calibrated for. |
| "Unbelievably, the antidisestablishmentarianism debate continued." | ~13 | ~5 | 9-11 | The word-count method fails badly here — one very long, rare word ("antidisestablishmentarianism") splits into many small sub-word tokens, but only counted as "1 word" in the word-based guess. |
| `print('hello world')` | ~5 | ~3 | 5-7 | Code has meaningful punctuation (`(`, `'`, `)`) that each often becomes its own token — word-counting code badly undercounts. |
| "میں آج بازار جا رہا ہوں" (Urdu) | varies | ~7 | often 2-3× higher | Non-Latin scripts were far less represented in training data used to build the token vocabulary, so the same *meaning* takes noticeably more tokens to express. |

**The actual mechanism, briefly:** the tokenizer's vocabulary was built by finding the most common recurring chunks in a mostly-English, mostly-prose training set. Anything that looks like that training data (common English words) compresses efficiently into few tokens. Anything that doesn't (rare words, code syntax, other scripts) gets broken into smaller, less efficient pieces — because those exact chunks weren't common enough to earn their own single token.

**Difference from Basic:** Basic uses one estimate (words × 1.3) and observes where it breaks. Intermediate runs two independent estimates side by side (chars ÷ 4 and words × 1.3) across a deliberately wider range of sentence types, and explains the underlying mechanism (byte-pair-encoding-style vocabulary built mostly from English prose) that predicts *which kinds* of text will break the rule, not just that some of them do.

**Which estimate should you actually use, day to day?** For a one-off "will this fit / roughly what will this cost" check, chars ÷ 4 in your head is enough — precision below about 20% doesn't change any real decision. For a system prompt or any other text resent unchanged on every call of a running feature, don't estimate at all: verify with `tiktoken` that what you're sending is actually what you think it is.
