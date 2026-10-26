from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Using shorthand tuple syntax ("placeholder", "{variable_name}")
template = ChatPromptTemplate([
    ("system", "You are a helpful AI bot."),
    ("placeholder", "{conversation}"),  # Equivalent to MessagesPlaceholder(variable_name="conversation", optional=True)
])

# Invoking the template with a list of historical messages
prompt_value = template.invoke({
    "conversation": [
        ("human", "Hi!"),
        ("ai", "How can I assist you today?"),
        ("human", "Can you make me an ice cream sundae?"),
        ("ai", "No."),
    ]
})
# print(prompt_value)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful {role}."),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
        ])
messages = prompt.invoke({
    "role": "tutor",
    "history": [HumanMessage(content="My name is Sara.")],
    "question": "What is my name?",
    })
print([m.type for m in messages.to_messages()]) # ['system','human','human']

from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# 1. Define your few-shot examples
examples = [
    {"input": "2+2", "output": "4"},
    {"input": "2+3", "output": "5"},
]

# 2. Define the template for formatting each individual example
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}"),
])

# 3. Create the FewShotChatMessagePromptTemplate
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

# 4. Combine into a final ChatPromptTemplate
final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a wondrous wizard of math."),
    few_shot_prompt,
    ("human", "{input}"),
])

# Format the prompt
formatted_messages = final_prompt.format_messages(input="4+4")
print(formatted_messages)
