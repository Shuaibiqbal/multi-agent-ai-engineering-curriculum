from langchain_core.runnables import RunnableLambda, RunnableBranch
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.messages import AIMessage

load_dotenv()

def reply_chain(model, system_text):
    prompt = ChatPromptTemplate.from_messages(
        [("system", system_text), ("human", "{text}")]
    )
    return prompt | model | StrOutputParser()

def tag_reply(text):
    return f"{text.strip()} (auto-routed)"

def build_pipeline(model):
    billing = reply_chain(model, "You are a billing agent. Mention refunds.")
    technical = reply_chain(model, "you are tech support. Ask for repro steps.")
    general = reply_chain(model, "You are general support. Friendly, brief.")

    router = RunnableBranch(
        (lambda t: t["category"] == "billing", billing),
        (lambda t: t["category"] == "technical", technical),
        general
    )
    return router | RunnableLambda(tag_reply)

real_model = ChatOpenAI(model="gpt-4o-mini", temperature=0, timeout=30)

pipeline = build_pipeline(real_model)

for category in ["billing", "technical", "hello"]:
    reply = pipeline.invoke({"category": category, "text": "help me"})
    print(f"{category} -> {reply}")


def echo_system_line(prompt_value):
    return AIMessage(content=prompt_value.to_messages()[0].content)

test_pipeline = build_pipeline(RunnableLambda(echo_system_line))

billing = test_pipeline.invoke({"category": "billing", "text": "x"})
technical = test_pipeline.invoke({"category": "technical", "text": "x"})
unknown = test_pipeline.invoke({"category": "sales", "text": "x"})

print("case 1 (billing -> billing branch) ->", "billing agent" in billing)
print("case 1 (technical -> technical branch) ->", "tech support" in technical)
print("case 2 (unknown -> default + tag) ->", "general support" in unknown and "(auto-routed)" in unknown)