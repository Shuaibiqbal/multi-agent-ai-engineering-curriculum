from dotenv import load_dotenv
from openai import OpenAI
import os 

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

client = OpenAI()

print("********************* Version1 Assistant ****************************")

system_message = {"role": "system", "content": "You are a helpful assistant."}
history = [system_message]

while True:
    user_input = input("Use: ")

    if user_input == "quit":
        break
    history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model = OPENAI_MODEL,
        messages= history,
    )
    assistant_message = response.choices[0].message.content
    print("Assistant: ", assistant_message)
    history.append({"role": "assistant", "content": assistant_message})


## Version2

def get_reply(history: list) -> str:

    response = client.chat.completions.create(
        model= OPENAI_MODEL,
        messages=history,
    )   

    return response.choices[0].message.content

def run_chat() -> None:
    history = [{"role": "system", "content": "You are a helpful Assistant."}]

    while True:
        user_input = input("You: ")

        if user_input == "quit":
            break

        history.append({"role": "user", "content": user_input})

        reply = get_reply(history=history)
        history.append({"role": "assistant", "content": reply})

        print("Assistant: ", reply)
if __name__ == "__main__":
    print("********************* Version2 Assistant ****************************")
    run_chat()
        