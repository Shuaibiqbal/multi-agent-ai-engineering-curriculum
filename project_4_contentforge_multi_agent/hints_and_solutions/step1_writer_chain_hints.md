# Step 1 — One Specialist's Drafting Logic, Working Alone, No Agent Behavior — Hints

> [Back to this step](../READING_README.md#step-1-one-specialists-drafting-logic-working-alone-no-agent-behavior) · [Hint 1](step1_writer_chain_hints.md#hint-1) · [Hint 2](step1_writer_chain_hints.md#hint-2) · [Solution](step1_writer_chain_solution.md)

Only 2 hints — work through them in order, and don't jump ahead until you've really tried. Each hint starts with the plain idea, then shows the shape of the real code.

- [Hint 1 — One specialist, one chain](#hint-1)
- [Hint 2 — The plan, and how to test it](#hint-2)

<hr class="page-break">

> [Back to this step](../READING_README.md#step-1-one-specialists-drafting-logic-working-alone-no-agent-behavior) · [Hint 1](step1_writer_chain_hints.md#hint-1) · [Hint 2](step1_writer_chain_hints.md#hint-2) · [Solution](step1_writer_chain_solution.md)

## Hint 1 — One specialist, one chain {: #hint-1 }

Start with the Writer — it needs no tools. Its whole skill is: findings in, article out.

That's one Doc05 chain: a prompt, the model, and a parser, joined with `|`. No loop, no other agents, no graph.

The prompt is the Writer's job description. Say three things: the length and shape (a titled 150-250-word article), **only** the given findings, and keep each fact's `[source]` tag.

Two functions in `agents/writer_agent.py`:

- `build_writer_chain()` — `ChatPromptTemplate.from_template(load_prompt("writer")) | get_model() | StrOutputParser()`.
- `run_writer(findings: str) -> str` — builds the chain and invokes it with `{"findings": findings}`.

`run_writer()` is the one door the rest of the project will use; nothing else should touch the chain.

Bring in the shared files first: config, errors, logger, prompt loader (folder `src/contentforge/prompts`), and `get_model()` from Project 3.

<hr class="page-break">

> [Back to this step](../READING_README.md#step-1-one-specialists-drafting-logic-working-alone-no-agent-behavior) · [Hint 1](step1_writer_chain_hints.md#hint-1) · [Hint 2](step1_writer_chain_hints.md#hint-2) · [Solution](step1_writer_chain_solution.md)

## Hint 2 — The plan, and how to test it {: #hint-2 }

```
main():
    load_config()
    for findings in TEST_FINDINGS:
        print a separator line
        print(run_writer(findings))
```

`TEST_FINDINGS` is a list of 3 made-up findings strings — two normal ones, and one almost empty.

The almost-empty input is the important one. Read what the Writer does with it:

- Good: a very short piece, or a note that there's too little to go on.
- Bad: a full article about solar panels, with facts that weren't in the input.

If it invents, make the "ONLY the findings" rule stronger now — later, Research can hand it thin notes for real, and you don't want to find this out inside the full team.

Full solution: [Show me the solution](step1_writer_chain_solution.md)
