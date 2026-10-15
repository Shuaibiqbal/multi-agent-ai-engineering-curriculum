from dataclasses import dataclass
import os 
from exceptions import MissingConfigError
@dataclass
class Config: 
    openai_api_key: str

def require_env(key: str)-> Config:
    value = os.getenv(key)
    if value is None or value == "":
        raise MissingConfigError(f"env value missing {value}. Please check your .env")
    

def load_config(): 

    openai_api_key = require_env("OPENAI_API_KEY")

    return Config(openai_api_key=openai_api_key)