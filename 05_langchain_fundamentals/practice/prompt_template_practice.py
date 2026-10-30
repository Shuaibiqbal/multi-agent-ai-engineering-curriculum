from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("Answer: {question}")

try:
    prompt.invoke({})
except KeyError:
    print("Missing variable -> Keyerror before any API call.")

result = prompt.invoke({"question": "What is LCEL?", "extra": "unused"})
print(f"Extra variable -> no error: {result.messages[0].content}")

result1 = prompt.invoke({"question":"hello", "extra_var": "i am extra variable"})
print(result1)
