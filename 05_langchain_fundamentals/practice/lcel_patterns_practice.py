from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable, RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
import time
from dotenv import load_dotenv

from langchain_core.output_parsers import StrOutputParser


def get_weather(inputs: dict) -> str:
    time.sleep(1)
    return "sunny in " + inputs["city"]
def get_news(inputs: dict) -> str:
    time.sleep(1)
    return "a new park opened in " + inputs["city"]
def backup_reply(inputs: dict) -> str:
    return "Sorry, the assistant is busy. Please try again soon"

lookups = RunnableParallel({"weather": get_weather, "news": get_news})

start = time.time()

result = lookups.invoke({"city": "Lahore"})

seconds = time.time() - start

print("keys:", sorted(result.keys()))
print(f"took {seconds:.1f} s")