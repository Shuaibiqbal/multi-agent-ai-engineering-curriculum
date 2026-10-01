

from dataclasses import dataclass
from dotenv import load_dotenv
from exception import MissingConfigError
import os 

load_dotenv()

@dataclass
class Config:
    openai_api_key: str
    openai_model: str

def require_env(key:str)-> str:

    value = os.getenv(key)
    
    if value is None or value == "":
        raise MissingConfigError(f"Required environment {key} variable is missing.")
    
    return value
    
def load_config(openai_api_key: str, openai_model: str) -> Config:
    openai_api_key = require_env(openai_api_key)
    openai_model = require_env(openai_model)

    return Config(openai_api_key=openai_api_key, openai_model=openai_model)