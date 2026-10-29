# Basic (your first real API call) — Solution

> [Back to the exercise](../README.md#ex-first_chat_call) · [Hint 1](first_chat_call_hints.md#hint-1) · [Hint 2](first_chat_call_hints.md#hint-2) · [Solution](first_chat_call_solution.md)

**Story — `chat_api_basics_practice.py`:** this is the single call every other exercise, the Build Task, and every later document's chat feature builds on top of. Written here, once, on its own, so you see the plain request/response shape before anything else (memory, streaming, error handling) gets added on top of it. **If not:** the first time you'd see a raw `client.chat.completions.create(...)` call would be buried inside a bigger file already juggling a loop or a try/except, making it harder to tell which part is "the API call" and which part is everything else.

## Solution

```python
# chat_api_basics_practice.py
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# One reusable function for "call the API with these prompts", so trying
# another prompt is just one more call, not a copy-pasted block.
def ask(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    # .choices[0].message.content is the reply text, not the whole object
    return response.choices[0].message.content


# Ask the same question with two different system prompts and compare.
question = "Tell me about your day."

formal_answer = ask("You are formal and professional.", question)
print("Formal:", formal_answer)

pirate_answer = ask("You are a sarcastic pirate.", question)
print("Pirate:", pirate_answer)
```
**Expected output:**
```
Formal: As a formal assistant, I do not experience days the way a person does...
Pirate: Arrr, another day chained to this here API, matey...
```
