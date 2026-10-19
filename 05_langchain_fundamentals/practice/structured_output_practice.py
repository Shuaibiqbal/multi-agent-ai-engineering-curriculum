from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv

load_dotenv()
# Version 1
class Person(BaseModel):
    name: str
    age: int
structured_model = ChatOpenAI(temperature=0, model="gpt-4o-mini").with_structured_output(Person)

good_result = structured_model.invoke("Extract: SHuaib is 30 years old.")

print(good_result)

unclear_result = structured_model.invoke("Extract: the sky is blue today.")
print(unclear_result)

#Version 2

from langchain_core.runnables import Runnable

def get_structured_result() -> Runnable:

    structured_model = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    return structured_model.with_structured_output(Person)

def extract_person(text: str) -> Person | None:

    try:
        person = structured_model.invoke(text)
    except ValidationError as e:
        return None
    if person.name is None and person.age is None:

        return None
    return person
def main() -> None:
    texts = [
            "Extract: Maria is 34 years old.",
            "Extract: the sky is blue today.",
            ]
    for text in texts:
        person = extract_person(text=text)
        print(f"{text} -> {person}")
if __name__ == "__main__":
    main()

