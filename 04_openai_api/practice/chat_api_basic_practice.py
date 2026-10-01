from dotenv import load_dotenv
import os 
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")


client = OpenAI()

response = client.chat.completions.create(
            model = OPENAI_MODEL,
            messages = [{"role": "system", "content": "You are formal and professional"},
                       {"role": "user", "content": "Tell me about your day."}],
        )
print("*************** Direct Call  ***************")

print(response.choices[0].message.content)

response = client.chat.completions.create(
    model= OPENAI_MODEL,
    messages=[
        {"role": "system", "content": "You are a sarcastic pirate."},
        {"role": "user", "content": "Tell me about your day."},
    ]
)
print(response.choices[0].message.content)
## by using function

def ask(system_prompt, user_prompt) -> str:

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    return response.choices[0].message.content
print("*************** By Using function calling ***************")

print(ask("You are formal and professional.", "Tell me about your day."))
print(ask("You are a sarcastic pirate.", "Tell me about your day."))

### With Main function
def main():
    print("***************By using main function.***************")
    question = " Tell me about your day."

    formal_answer = ask("You are formal and professional.", question)

    print("Formal:", formal_answer)

    pirate_answer = ask("You are a sarcastic pirate.", question)

    print('Pirate:', pirate_answer)

if __name__ == "__main__":
    main()