from dotenv import load_dotenv
from dataclasses import dataclass
import os 

class MissingConfigErrror(Exception):
    pass

@dataclass
class Config:
    openai_api_key: str
    log_level: str

def required_env(key: str) -> Config:

    value = os.environ.get(key)

    if value is None or value == "":
        raise MissingConfigErrror(f"Missing config {key} is {value}")

    return value
def load_config():
    load_dotenv()

    openai_api_key = required_env("OPENAI_API_KEY")
    log_level = required_env("LOG_LEVEL")

    return Config(openai_api_key=openai_api_key, log_level=log_level)
