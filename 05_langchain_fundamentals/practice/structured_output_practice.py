from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Person(BaseModel):
    name: str
    age: int

