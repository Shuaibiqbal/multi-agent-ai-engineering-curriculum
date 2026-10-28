# Step 2 — The Grounded Answer — Hints

> [Back to the step](../READING_README.md#step-2-the-grounded-answer) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](step2_answer_solution.md)

- [Hint 1 — one grounded chain](#hint-1)
- [Hint 2 — the two rules in the prompt](#hint-2)

## Hint 1 — one grounded chain {: #hint-1 }

`answer_question` is a small chain over the context Step 1 built:

```
answer_question(model, question, context):
    prompt = ChatPromptTemplate.from_template(ANSWER_PROMPT)
    chain = prompt | model
    return chain.invoke({"context": context, "question": question}).content
```

The `context` is `build_context(snippets)` — one block with `# File:` headers — so the model sees both the code and which file each piece came from.

## Hint 2 — the two rules in the prompt {: #hint-2 }

The prompt needs exactly two rules to be useful:

1. **"Answer using ONLY the code below."** This ties the answer to the repo, not the model's memory of how `login` is usually written.
2. **"If it's not there, say you don't know."** A question about a feature the repo lacks must get an honest "I don't know", not a plausible invention — the same honesty rule as every RAG answer.

Add "name the functions or files involved" so the written answer points at specifics, pairing with the cited-files list. The whole file set is in the [Solution](step2_answer_solution.md).
