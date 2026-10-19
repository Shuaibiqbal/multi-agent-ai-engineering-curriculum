# from langchain_core.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# from chat_client import EXTRACT_PROMPT, create_client, get_structured_reply
# from schemas import ExtractedInfo

# load_dotenv()

# prompt = ChatPromptTemplate.from_messages(
#     [("system", EXTRACT_PROMPT), ("human", "{text}")]
# )

# model = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# lcel_chain = prompt | model.with_structured_output(ExtractedInfo)

# client = create_client()

# test_inputs = [
#  "Maria wants to reset her password",
#  "Hi, I'm Tom and my invoice looks wrong",
#  "Ahmed here, please cancel my order",
# ]

# for text in test_inputs:
#     raw_result = get_structured_reply(client ,text)

#     lcel_result = lcel_chain.invoke({"text": text})

#     print("Input:", text)
#     print(" raw:", raw_result)
#     print(" lcel:", lcel_result)

#Version 2
# from openai import OpenAI
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import Runnable
# from dotenv import load_dotenv

# load_dotenv()

# from chat_client import get_structured_reply, create_client, EXTRACT_PROMPT
# from schemas import ExtractedInfo

# TEST_INPUTS = [
#     "Maria wants to reset her password",
#     "Hi, I am Rom and my invoice looks wrong",
#     "Ahmed here please cancel my order",
# ]
# def build_lcel(model: str = "gpt-4o-mini") -> Runnable:
#     prompt = ChatPromptTemplate(
#         [("system", EXTRACT_PROMPT), ("human", "{text}")]
#     )
#     model = ChatOpenAI(model=model, temperature=0)

#     return prompt | model.with_structured_output(ExtractedInfo)

# def compare(client: OpenAI, lcel_chain: Runnable, text: str) -> bool:
#     raw_result = get_structured_reply(client, text)
#     lcel_result = lcel_chain.invoke({"text": text})

#     matched = raw_result.name == lcel_result.name

#     print(f"{text} -> match: {matched}")

#     print(f" raw: {raw_result}")
#     print(f" lcel: {lcel_result}")
#     return matched

# def main() -> None:
#     client = create_client()

#     lcel_chain = build_lcel()

#     matched = 0

#     for text in TEST_INPUTS:
#         if compare(client, lcel_chain, text):
#             matched = matched + 1
#     print(f"{matched}/{len(TEST_INPUTS)} matched")
# if __name__ == "__main__":
#     main()
#Version 3

from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.runnables import Runnable
from dataclasses import dataclass

load_dotenv()

from chat_client import get_structured_reply, create_client, EXTRACT_PROMPT
from schemas import ExtractedInfo

TEST_INPUTS = [
    "Maria wants to reset her password",
    "Hi, I'm Tom and my invoice looks wrong",
    "Ahmed here, please cancel my order",
    ]

@dataclass
class ComparisonRow:
    input_text: str
    raw_result: ExtractedInfo
    lcel_result: ExtractedInfo
    matched: bool
def build_lcel_chain(model_name: str = "gpt-4o-mini") -> Runnable:
    prompt = ChatPromptTemplate.from_messages(
        [("system", EXTRACT_PROMPT), ("human", "{text}")]
        )
    model = ChatOpenAI(model=model_name, temperature=0)
    return prompt | model.with_structured_output(ExtractedInfo)
def run_comparison(test_inputs: list[str]) -> list[ComparisonRow]:
    client = create_client()
    lcel_chain = build_lcel_chain()
    rows = []

    for text in test_inputs:
        raw_result = get_structured_reply(client, text)
        lcel_result = lcel_chain.invoke({"text": text})

        matched = raw_result.name == lcel_result.name
        rows.append(ComparisonRow(text, raw_result, lcel_result, matched))
    return rows

def main() -> None:
    rows = run_comparison(TEST_INPUTS)
    matched = 0

    for row in rows:
        if row.matched:
            matched = matched + 1
    print(f"{matched}/{len(rows)} matched")

    for row in rows:
        if not row.matched:
            print(f"MISMATCH on: {row.input_text}")
            print(f" raw: {row.raw_result}")
            print(f" lcel: {row.lcel_result}")

if __name__ == "__main__":
    main()