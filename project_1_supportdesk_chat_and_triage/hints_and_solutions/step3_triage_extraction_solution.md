# Step 3 — A Triage Agent That Extracts a Structured Ticket From Free Text — Solution

> [Back to this step](../READING_README.md#step-3-a-triage-agent-that-extracts-a-structured-ticket-from-free-text) · [Hint 1](step3_triage_extraction_hints.md#hint-1) · [Hint 2](step3_triage_extraction_hints.md#hint-2) · [Solution](step3_triage_extraction_solution.md)

**Story — Step 3:** the chat can't file tickets yet. This step adds the first real agent — Triage — which turns a complaint into a checked `SupportTicket`. For now you trigger it by hand with `/extract`, so you can test it on its own before Step 4 automates the choice. This is also where the app learns to survive every common failure. **If not:** a support desk that can't produce structured tickets is just a chatbot, and one rate limit or bad reply would crash the whole session.

After this step the project runs as a chat app that can also file tickets. Files from Steps 1-2 that aren't shown here don't change.

## Solution — a strict agent, every failure handled, sample data and tests

**Story — `schemas.py`:** the contract between the model and your code. `str | None` lets "no name given" be a real answer, and `Literal` limits category and urgency to exact values. **If not:** a required `customer_name` would force the model to invent one, and a free-text category could come back as "Billing issue" — valid text that breaks any `if category == "billing"`.

```python
# src/schemas.py
# The shapes the model must answer in. SupportTicket: one support ticket.
from typing import Literal

from pydantic import BaseModel

class SupportTicket(BaseModel):
    customer_name: str | None
    issue_category: Literal["billing", "technical", "account_access", "other"]
    urgency: Literal["low", "medium", "high"]
    summary: str
```

**Story — `prompts/triage.txt`:** a strict prompt for a strict job — it says outright never to guess a name, and when urgency is "high". **If not:** the schema allows `None`, but nothing *tells* the model to use it, so it may still fill in a name.

`src/prompts/triage.txt`

```text
You are a support triage agent. Turn the customer's message into a
support ticket. Fill customer_name only if the customer states their
name - otherwise leave it null, never guess one. Use urgency 'high'
only if the customer says it is urgent or needed today.
```

**Story — `agents/triage.py`:** the Triage agent — its own prompt, no chat history, one structured call. It checks `refusal` before reading `parsed`, and returns `None` on any unusable answer, so the caller has exactly two cases to handle. **If not:** a refusal would come back as `parsed=None` with no explanation, and invalid output could reach code that trusts it.

```python
# src/agents/triage.py
# The Triage agent: turns one complaint into a SupportTicket, or returns
# None when the model's answer can't be used.
from openai import OpenAI
from pydantic import ValidationError

from src.models.llm import MODEL
from src.schemas import SupportTicket
from src.utils.logger import get_logger
from src.utils.prompts import load_prompt

def triage_agent(client: OpenAI, message: str) -> SupportTicket | None:
    logger = get_logger(__name__)
    messages = [
        {"role": "system", "content": load_prompt("triage")},
        {"role": "user", "content": message},
    ]
    try:
        completion = client.beta.chat.completions.parse(
            model=MODEL, messages=messages, response_format=SupportTicket
        )
    except ValidationError as e:
        logger.warning("Triage output did not match SupportTicket: %s", e)
        return None

    reply = completion.choices[0].message
    if reply.refusal:
        logger.warning("Triage agent refused: %s", reply.refusal)
        return None
    return reply.parsed
```

Also create an empty `src/agents/__init__.py`.

**Story — `services/desk_service.py`:** the file for the app's "business flow" — what happens to a message, apart from reading the keyboard. In this step it holds one function, `print_ticket()`, which shows a ticket in a readable way. Step 4 adds the router → agent flow to **this same file**, so nothing has to move later. (Also create an empty `src/services/__init__.py`.) **If not:** `print_ticket()` would sit in `main.py` now and have to move in Step 4.

```python
# src/services/desk_service.py
# The app's flow, apart from the keyboard. print_ticket() shows a ticket.
from src.schemas import SupportTicket

def print_ticket(ticket: SupportTicket) -> None:
    name = ticket.customer_name
    if name is None:
        name = "(not given)"
    print("Ticket created:")
    print(f"  customer: {name}")
    print(f"  category: {ticket.issue_category}")
    print(f"  urgency:  {ticket.urgency}")
    print(f"  summary:  {ticket.summary}")
```

**Changed from Step 2:** the startup and the chat branch are the same. What's new: 3 imports, the `/extract` branch that calls `print_ticket()`, and the `try` / `except` blocks around the loop body.

**Story — `main.py`:** Step 2's loop plus `/extract` and one `except` per failure. Each failure gets the reaction Doc04's error table gives it: exit on a bad key, ask the user to wait on a rate limit, and drop a too-long message. (The 4th failure, bad structured output, is already handled inside `triage_agent()`.) **If not:** any one of these would end the session with a traceback, and the user would lose the whole conversation.

```python
# main.py
# The file you run: python main.py
# The chat loop, plus /extract <text> to file a ticket, and one clear
# message for each OpenAI error (bad key, rate limit, too long).
import sys

# new in Step 3: openai (for its error classes), triage_agent, print_ticket
import openai

from src.agents.triage import triage_agent
from src.config import load_config
from src.exceptions import MissingConfigError
from src.models.llm import (
    check_api_key_at_startup,
    create_client,
    stream_message,
)
from src.services.desk_service import print_ticket
from src.utils.history import trim_history
from src.utils.logger import get_logger
from src.utils.prompts import load_prompt

MAX_HISTORY_TOKENS = 3000

def main() -> None:
    try:
        config = load_config()
    except MissingConfigError as e:
        print(f"Setup problem: {e}")
        sys.exit(1)

    logger = get_logger(__name__)
    client = create_client(config)
    if not check_api_key_at_startup(client):
        logger.error("Authentication failed — check OPENAI_API_KEY.")
        print("Login failed — check OPENAI_API_KEY in your .env file.")
        sys.exit(1)

    history = [{"role": "system", "content": load_prompt("concierge")}]
    print("SupportDesk AI — type a message, or /quit to exit.")
    print("Type /extract <complaint> to file a ticket.")

    while True:
        message = input("You: ").strip()
        if message == "/quit":
            break
        if message == "":
            continue

        # new in Step 3: try / except around the loop body, and /extract
        try:
            if message.startswith("/extract "):
                text = message.removeprefix("/extract ")
                ticket = triage_agent(client, text)
                if ticket is None:
                    print("Sorry, I couldn't turn that into a ticket.")
                else:
                    print_ticket(ticket)
            else:
                trim_history(history, MAX_HISTORY_TOKENS)
                print("Assistant: ", end="", flush=True)
                stream_message(client, history, message)
        except openai.AuthenticationError:
            logger.error("API key stopped working mid-session.")
            print("Login failed — check OPENAI_API_KEY in your .env file.")
            sys.exit(1)
        except openai.RateLimitError:
            logger.warning("Rate limited after the client's retries.")
            print("We're busy right now — wait a moment and try again.")
        except openai.BadRequestError as e:
            logger.warning("Request rejected (likely too long): %s", e)
            if history[-1]["role"] == "user":
                history.pop()
            print("That message was too long to handle — please shorten it.")

if __name__ == "__main__":
    main()
```

Why these `except` blocks sit in `main.py`: this is the only place that knows how to talk to the *user* (print a message, or exit). The agents just raise or return `None`.

**Story — `data/sample/messages.json`:** the 3 test complaints from the README, stored once. **If not:** the script and the test would each keep their own copy, and the copies would drift apart.

`data/sample/messages.json`

```json
{
  "triage": [
    "Hi, I'm Sarah Khan. I was charged twice this month. Please fix it today.",
    "can't log into my account, tried resetting password twice, still nothing",
    "just wondering what your refund policy is, no rush"
  ]
}
```

(The first message is wrapped onto 2 lines here only to fit the page — in your file keep it on **one** line, because a JSON string can't contain a line break.)

**Story — `scripts/triage_samples.py`:** runs Triage on every sample and prints each ticket, for *you* to judge — for example after rewording `triage.txt`. **If not:** checking a prompt change would mean typing 3 complaints by hand each time.

```python
# scripts/triage_samples.py
# Runs the Triage agent on every sample complaint and prints each ticket.
# Run from the repo root: python -m scripts.triage_samples
# Makes real API calls — needs a valid OPENAI_API_KEY in .env.
import json

from src.agents.triage import triage_agent
from src.config import load_config
from src.models.llm import create_client

SAMPLES_PATH = "data/sample/messages.json"

def main() -> None:
    config = load_config()
    client = create_client(config)
    with open(SAMPLES_PATH) as samples_file:
        samples = json.loads(samples_file.read())

    for message in samples["triage"]:
        print(f"\nMessage: {message}")
        ticket = triage_agent(client, message)
        if ticket is None:
            print("No ticket — the Triage agent couldn't extract one.")
        else:
            print(f"Ticket:  {ticket}")

if __name__ == "__main__":
    main()
```

**Story — `tests/unit/test_schemas.py`:** checks the schema allows a missing name and rejects an unknown urgency — free and instant. **If not:** someone could change `customer_name` to a plain `str` and nothing would warn them until the model started inventing names.

```python
# tests/unit/test_schemas.py
# Checks the Pydantic schemas accept good data and reject bad data.
# No API calls, no API key needed.
# Run from the repo root: python -m tests.unit.test_schemas
from pydantic import ValidationError

from src.schemas import SupportTicket

def test_ticket_without_a_name() -> None:
    ticket = SupportTicket(
        customer_name=None,
        issue_category="account_access",
        urgency="medium",
        summary="Customer can't log in after two password resets.",
    )
    print(f"case 1 (no name allowed)     -> {ticket.customer_name}")

def test_ticket_rejects_unknown_urgency() -> None:
    try:
        SupportTicket(
            customer_name="Sarah Khan",
            issue_category="billing",
            urgency="urgent",
            summary="Charged twice.",
        )
    except ValidationError:
        print("case 2 (bad urgency)         -> ValidationError")

if __name__ == "__main__":
    test_ticket_without_a_name()
    test_ticket_rejects_unknown_urgency()
```

**Changed from Step 2:** `tests/integration/test_live_agents.py` gets cases 4 and 5 — `load_samples()`, `test_triage()`, their imports, and two new lines at the bottom.

**Story — `tests/integration/test_live_agents.py`:** the Triage agent is this step's feature, so the 3 sample complaints must each become a ticket — and the one with no name must not get an invented name. **If not:** a prompt change could start inventing customer names, and nothing would notice.

```python
# tests/integration/test_live_agents.py
# The project's checks against the real OpenAI API — each step adds
# cases. Needs a valid OPENAI_API_KEY in .env.
# Run from the repo root: python -m tests.integration.test_live_agents
#   case 1 — one message in, a real reply out
#   case 2 — a wrong key is caught at startup, not mid-chat
#   case 3 — turn 3 can use what was said in turn 1 (memory)
#   case 4 — each sample complaint becomes a ticket
#   case 5 — the complaint with no name gets no invented name
# new in Step 3
import json

from openai import OpenAI

# new in Step 3
from src.agents.triage import triage_agent
from src.config import load_config
from src.models.llm import (
    check_api_key_at_startup,
    create_client,
    send_message,
)

# new in Step 3
SAMPLES_PATH = "data/sample/messages.json"


def test_first_reply(client: OpenAI) -> None:
    reply = send_message(client, [], "What's 2+2?")
    print(f"case 1 (first reply)   -> {reply}")


def test_bad_key() -> None:
    bad_client = OpenAI(api_key="sk-fake-key-123")
    key_ok = check_api_key_at_startup(bad_client)
    print(f"case 2 (bad key ok?)   -> {key_ok}")


def test_memory(client: OpenAI) -> None:
    history = [{"role": "system", "content": "You are a helpful assistant."}]
    send_message(client, history, "My order number is 4471.")
    send_message(client, history, "Thanks, that's all for now.")
    reply = send_message(client, history, "What was my order number?")
    print(f"case 3 (memory)        -> {reply}")


# new in Step 3
def load_samples() -> dict:
    with open(SAMPLES_PATH) as samples_file:
        return json.loads(samples_file.read())


# new in Step 3
def test_triage(client: OpenAI, samples: dict) -> None:
    for message in samples["triage"]:
        ticket = triage_agent(client, message)
        print(f"case 4 (triage)        -> {ticket}")

    second = triage_agent(client, samples["triage"][1])
    if second is not None and second.customer_name is None:
        print("case 5 (no name)       -> OK, customer_name is None")
    else:
        print("case 5 (no name)       -> WRONG, a name was invented")


if __name__ == "__main__":
    config = load_config()
    client = create_client(config)
    # new in Step 3
    samples = load_samples()
    test_first_reply(client)
    test_bad_key()
    test_memory(client)
    # new in Step 3
    test_triage(client, samples)
```

**Run everything:**

```bash
python -m tests.unit.test_config
python -m tests.unit.test_history
python -m tests.unit.test_schemas
python -m tests.integration.test_live_agents
python -m scripts.triage_samples
python main.py
```

**Expected output** of the unit test:

```
case 1 (no name allowed)     -> None
case 2 (bad urgency)         -> ValidationError
```

**Expected output** of the integration test (tickets shown shortened — the model's wording varies):

```
case 1 (first reply)   -> 2 + 2 equals 4.
case 2 (bad key ok?)   -> False
case 3 (memory)        -> Your order number was 4471.
case 4 (triage)        -> customer_name='Sarah Khan' issue_category='billing'
                          urgency='high' summary='...'
case 4 (triage)        -> customer_name=None issue_category='account_access'
                          urgency='medium' summary='...'
case 4 (triage)        -> customer_name=None issue_category='other'
                          urgency='low' summary='...'
case 5 (no name)       -> OK, customer_name is None
```

(Each ticket is really one line; it's wrapped here to fit the page.)

In the app, `/extract can't log into my account, tried resetting password twice` prints a ticket with `customer: (not given)`.
