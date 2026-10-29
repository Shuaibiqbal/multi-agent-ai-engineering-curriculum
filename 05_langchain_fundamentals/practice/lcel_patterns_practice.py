from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel, RunnableLambda
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

lookups = RunnableParallel({"weather": get_weather, "news": get_news})

start = time.time()

result = lookups.invoke({"city": "Lahore"})

seconds = time.time() - start
print(result)
print(f"Case 1 (keys) -> {sorted(result)}")
print(f"Case 1 (under 1.5 s?) -> {seconds < 1.5}")

# FALL BACK

def backup_reply(inputs):
    return "Sorry, the assistant is busy. Please try again soon."

prompt = ChatPromptTemplate.from_template(
    "Write one sentence about {city}"
)

broken_model = ChatOpenAI(model="gpt-4o-mini", base_url="http://127.0.0.1:9", max_retries=0)

broken_chain = (prompt | broken_model | StrOutputParser()).with_fallbacks([RunnableLambda(backup_reply)],exceptions_to_handle=(openai.APIConnectionError, openai.RateLimitError))

reply = broken_chain.invoke({"city": "lahore"})

print(f"Case 2 (outage) -> backup used: {reply.startswith("Sorry")}")

#A code bug must still fail loudly 

def buggy_step(inputs):
    return inputs["missing_key"]

bug_chain = RunnableLambda(buggy_step).with_fallbacks(
    [RunnableLambda(backup_reply)],
    exceptions_to_handle=(openai.APIConnectionError, openai.RateLimitError)
)

try:
    bug_chain.invoke({"city": "Lahore"})
    print("case 3 (bug) -> hidden (wrong!)")
except KeyError:
    print("case 3 (bug) -> KeyErro still raised")

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

live_chain = prompt | model | StrOutputParser()

print("case 4 (stream) -> ", end="")

full_text = ""
for chunk in live_chain.stream({"city": "Lahore"}):
    print(chunk, end="", flush=True)

    full_text = full_text + chunk
print()

print(f"case 4 (full text) -> {len(full_text)} characters")