from dotenv import load_dotenv
import os 
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

client = OpenAI()

############ Stream Version 1 ############
print("############ Stream Version 1 ############")

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain a REST API in 10 sentences."}
]

stream = client.chat.completions.create(
    model=OPENAI_MODEL,
    messages=messages,
    stream=True
)

for chunk in stream:
    piece = chunk.choices[0].delta.content 
    if piece:
        print(piece, end="")


############ Stream Version 2 ############
print("############ Stream Version 2 ############")

def stream_reply(history: list) -> str:

    stream = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=history,
        stream=True
    )
    full_reply = ""
    for chunk in stream:
        piece = chunk.choices[0].delta.content 
        if piece:
            print(piece, end="")
            full_reply = full_reply + piece
    print()
    return full_reply

def main() -> None:

    history = [{"role": "system", "content": "You are a helpful assistant."},
               {"role": "user", "content": "EXplain a REST API in 10 sentences."}]

    reply = stream_reply(history)
    history.append({"role": "assistant", "content": reply})
    
if __name__ == "__main__":
    main()
