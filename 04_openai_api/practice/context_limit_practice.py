from dotenv import load_dotenv
from openai import OpenAI
import os 
import openai

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

client = OpenAI()

input_msg = "Shuaib" *100000

try:
    client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": input_msg}],
        max_completion_tokens=10
    )
except Exception as e:
    print(type(e).__name__, str(e)[:200])
### or you can direct use bad request error 
except openai.BadRequestError as e:
    print(f"Error Type: {type(e).__name__}")
    print(f"Message: {str(e)[:200]}")