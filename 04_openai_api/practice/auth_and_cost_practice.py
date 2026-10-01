from openai import OpenAI
import os 
from dotenv import load_dotenv
import openai

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL")

client = OpenAI()

# Part1: Bad key
bad_client = OpenAI(api_key="fake-key-123")

try:
    response = bad_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role":"user", "content": "How are you?"}]
    )
except openai.AuthenticationError as e:
    print("Login failed - check your API key.")

# Part2: cost comparison

short_prompt = "Be helpful."
user_query = "What is the capital of France?"
short_client = client.chat.completions.create(
    model=OPENAI_MODEL,
    messages=[
        {"role": "system", "content": short_prompt},
        {"role": "user", "content": user_query}
    ],
)

long_prompt = "You are a friendly, detailed assistant. " * 20

long_client = client.chat.completions.create(
    model=OPENAI_MODEL,
    messages=[
        {"role":"system", "content": long_prompt},
        {"role": "user","content": user_query}
    ],
)

print("Short prompt tokens: ", short_client.usage.total_tokens)
print("Long prompt tokens: ", long_client.usage.total_tokens)

# Version 2
print("******* Version2 *******")

import openai
from openai import OpenAI
client = OpenAI()
def try_bad_key() -> None:
    bad_client = OpenAI(api_key="sk-fake-key-123")
    try:
        bad_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "hi"}],
        )
    except openai.AuthenticationError:
        print("Login failed — check your API key.")
def compare_prompt_cost(question: str) -> None:
    short_prompt = "Be helpful."
    long_prompt = (
                "You are a friendly, detailed, thorough assistant "
                "who explains everything carefully. "
                ) * 10
    short_messages = [
                {"role": "system", "content": short_prompt},
                {"role": "user", "content": question},
                ]
    long_messages = [
                {"role": "system", "content": long_prompt},
                {"role": "user", "content": question},
                ]
    short = client.chat.completions.create(
    model="gpt-4o-mini", messages=short_messages
                                )
    long = client.chat.completions.create(
    model="gpt-4o-mini", messages=long_messages
    )
    print(f"Short system prompt: {short.usage.total_tokens} tokens")
    print(f"Long system prompt: {long.usage.total_tokens} tokens")

try_bad_key()
compare_prompt_cost("What's the capital of France?")
