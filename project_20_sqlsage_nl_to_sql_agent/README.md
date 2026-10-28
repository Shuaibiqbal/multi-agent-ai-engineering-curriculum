# SQLSage — Natural-Language-to-SQL Analytics Agent

> **Short description:** Ask a database a question in plain English and get an answer — safely. SQLSage reads the schema, has the model write a single read-only `SELECT` as **structured output**, checks it with a **deterministic guard** (no `INSERT`/`UPDATE`/`DELETE`/`DROP`/chained statements), runs it against SQLite, and phrases the result in one sentence.

**Tech:** Python · LangChain (structured output) · SQLite (`sqlite3`) · OpenAI SDK · Pydantic  ·  **Type:** NL-to-SQL analytics agent  ·  **Level:** Intermediate

## Demo

![SQLSage demo — answering a question about a database](assets/demo.png)

```
$ python main.py "How many orders are completed?"

SQL:
  SELECT count(*) FROM orders WHERE status = 'completed'

Answer:
  There are 3 completed orders.
```

## Overview

Business questions live in a database, but the people asking them don't write SQL. SQLSage turns a plain-English question into a query, **guards** it, runs it, and answers in one sentence.

- The database **schema** is read and handed to the model as context.
- The model returns a single read-only `SELECT` as **structured output**.
- A deterministic **guard** rejects anything that isn't a safe single `SELECT`.
- The **runner** executes the query; the **answer** step phrases the rows.

## Why

Letting a model write SQL is powerful and dangerous. The safety is a **deterministic guard**, not a hope — a plain-Python check that runs before any query touches the database. The guard and the runner need no model, so they test with hand-written SQL and a tiny in-memory database; the model only writes the query and phrases the result.

## Features

- Plain-English questions answered from a real SQLite database.
- SQL returned as structured output — a clean query string, not prose.
- A deterministic safety guard: single read-only `SELECT` only.
- Grounded answers phrased from the returned rows.
- The guard and runner are deterministic, testable with no model.

## Architecture

```
question
   |
   schema_text(db)                 -> the CREATE TABLE statements
   generate_sql(model, schema, q)  -> a single SELECT (structured output)
   |
   is_safe_select(sql)             -> True / False  (deterministic guard)
   run_select(db, sql)             -> rows
   |
   summarize_answer(model, q, rows)  ->  one-sentence answer
```

## Project Structure

```
<repo folder>/ (the SQLSage repo — full name in the heading above)
├── data/                        the SQLite database (built by seed)
├── src/
│   ├── models/llm.py
│   ├── db/                      seed.py, schema.py, runner.py
│   ├── utils/logger.py
│   ├── guard.py                 is_safe_select()
│   ├── schemas.py               SQLQuery
│   ├── sql_agent.py             generate_sql()
│   ├── answer.py                summarize_answer()
│   ├── config.py
│   ├── exceptions.py
│   └── pipeline.py              ask()
├── tests/
│   ├── integration/test_live_ask.py
│   └── unit/                    test_config, test_guard, test_db
├── .env.example
├── .gitignore
├── LICENSE
├── main.py
├── README.md
└── requirements.txt
```

## Getting Started

**Requirements:** Python 3.10+ and an OpenAI API key.

```bash
git clone <this-repo-url>
cd SQLSage-Natural-Language-To-SQL-Analytics-Agent
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # then put your key in .env
```

## Configuration

| Variable | Required | Default | Meaning |
|---|---|---|---|
| `OPENAI_API_KEY` | yes | — | Your OpenAI API key |
| `LOG_LEVEL` | no | `INFO` | Log verbosity |
| `DB_PATH` | no | `data/shop.db` | The SQLite database to query |

## Usage

```bash
python main.py "How many orders are completed?"
```

## Running the Tests

```bash
# unit — no model
python -m tests.unit.test_config
python -m tests.unit.test_guard
python -m tests.unit.test_db

# integration — real model
python -m tests.integration.test_live_ask
```

## Design Decisions

- **The guard is deterministic.** An LLM can write anything; a plain-Python check — `SELECT`-only, no write/schema keyword, single statement — decides what runs, and it tests with no model.
- **SQL comes back as structured output.** A Pydantic `SQLQuery` gives a clean query string, not prose to parse.
- **The answer is grounded in the rows.** The model phrases only what the query returned, and says "no matching data" when the rows are empty.

## License

MIT — see `LICENSE`.
