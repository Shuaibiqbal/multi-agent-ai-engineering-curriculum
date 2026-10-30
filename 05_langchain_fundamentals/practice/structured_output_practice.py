from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


class Rating(BaseModel):
    score: str
parser = PydanticOutputParser(pydantic_object=Rating)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def get_rating(template, thing):
    prompt = ChatPromptTemplate.from_template(template)

    if "{format_instructions}" in template:
        prompt = prompt.partial(
            format_instructions = parser.get_config_jsonschema()
        )
    try:
        return (prompt | model | parser).invoke({"thing": thing})
    except OutputParserException:
        return None

no_hint = get_rating("Rate {thing} from 1 to 10.", "pizza")
print(f"case 1 (no instructions) -> {no_hint}")

fixed = "Rate {thing} from 1 to 10.\n{format_instructions}"
with_hint = get_rating(fixed, "pizza")
print(f"case 2 (with instructions) -> {with_hint}")

try:
    parser.parse("I'd say eight")
    print("case 3 (parse by hand)")
except OutputParserException:
    print("case 3 (parse by hand) -> OutputParserException")