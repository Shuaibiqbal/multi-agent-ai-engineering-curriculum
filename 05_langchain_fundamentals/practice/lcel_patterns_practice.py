from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable, RunnableParallel, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
import time
from dotenv import load_dotenv
import openai

load_dotenv()

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

print("keys:", sorted(result.keys()), result)
print(f"took {seconds:.1f} s")

# part 2: a backup when the model can't be reached
prompt = ChatPromptTemplate.from_template("Write one sentence about {city}.")
broken_model = ChatOpenAI(
    model="gpt-4o-mini", base_url="http://127.0.0.1:9", max_retries=0
    )
chain = prompt | broken_model | StrOutputParser()
safe_chain = chain.with_fallbacks(
    [RunnableLambda(backup_reply)],
    exceptions_to_handle=(openai.APIConnectionError,),
)
print("fallback:", safe_chain.invoke({"city": "Lahore"}))

#part3 
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
live_chain = prompt | model | StrOutputParser()

for chunk in live_chain.stream({"city": "Lahore"}):
    print(chunk, end="", flush=True)
print()