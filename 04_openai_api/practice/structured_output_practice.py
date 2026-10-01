from pydantic import BaseModel, ValidationError
from typing import Literal
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

class ExtractedInfo(BaseModel):
    name: str | None
    intent: str | None
    urgency: Literal["low", "normal", "urgent"]

good = {"name": "Maria", "intent": "reset_password", "urgency": "urgent"}

print(ExtractedInfo.model_validate(good))

bad = {"name": "Maria", "intent": "reset her password", "urgency": "very"}

try:
    ExtractedInfo.model_validate(bad)
except ValidationError as e:
    print("bad urgency -> ValidationError", e)
print("**************Part2 ****************")

response = client.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role":"user", "content": "I am Maria, reset my password!"},
    ],
    response_format=ExtractedInfo,
)

message = response.choices[0].message

if message.refusal:
    print(f"the model refused: {message.refusal}")
else:
    info = message.parsed
    print(info)
    print(f"name: {info.name}, urgency: {info.urgency}")
