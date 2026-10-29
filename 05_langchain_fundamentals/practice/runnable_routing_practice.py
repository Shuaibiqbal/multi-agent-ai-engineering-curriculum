from langchain_core.runnables import RunnableLambda, RunnableBranch
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

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
    techincal = reply_chain(model, "you are tech support. Ask for repro steps.")
    general = reply_chain(model, "You are general support. Friendly, brief.")

    router = RunnableBranch(
        (lambda t: t["category"] == "billing", billing),
        (lambda t: t["category"] == "techincal", techincal),
        general
    )
    return router | RunnableLambda(tag_reply)

real_model = ChatOpenAI(model="gpt-4o-mini", temperature=0, timeout=30)

pipeline = build_pipeline(real_model)

for category in ["billing", "techincal", "hello"]:
    reply = pipeline.invoke({"category": category, "text": "help me"})
    print(f"{category} -> {reply}")

#Make all curriculum code first-timer friendly and refresh every PDF

#Rewrite the doc exercise solutions to read top to bottom instead of being split across small functions, and lighten the project solutions by dropping heavy type hints while keeping their professional structure, so the code uses only what the docs teach. Update CURRICULUM and the study plan, and rebuild every PDF so each one matches its markdown.