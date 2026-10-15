from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from dotenv import load_dotenv
from config import Config, load_config

##Version1
load_dotenv()

# prompt = ChatPromptTemplate.from_template("Answer: {question}")

# model = ChatOpenAI()

# parser = StrOutputParser()

# chain = prompt | model | parser

# result = chain.invoke({"question": "What's 5+7?"})

# print(result)

##Version2 

# def build_chain(temperature: float = 0.0, model_name: str = "gpt-4o-mini"):
#     prompt = ChatPromptTemplate.from_template("Answer: {question}")

#     model = ChatOpenAI(temperature=temperature, model=model_name)

#     parser = StrOutputParser()

#     return prompt | model | parser

# if __name__ == "__main__":
#     print("Version2 Result \n")
#     chain = build_chain()
#     result = chain.invoke({"question": "What's 5+7?"})
#     print(result)

# Version 3

def build_chain(config: Config | None = None) -> Runnable:

    if config is None:
        config = load_config()

    prompt = ChatPromptTemplate.from_template("Answer: {question}")
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=config.openai_api_key)
    parser = StrOutputParser()

    return prompt | model | parser

if __name__ == "__main__":
    chain = build_chain()

    result = chain.invoke({"question": "What's 5+7"})

    print(f"Answer: {result}")

    test_config = Config(openai_api_key="sk-test-not-real")
    test_chain = build_chain(test_config)

    print(f"Built with a test Config: {type(test_chain).__name__}")
