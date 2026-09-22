import os 
from dotenv import load_dotenv
from exception import MissingConfigError


class Config:
    def __init__(self, openai_api_key, log_level):
        self.openai_api_key = openai_api_key
        self.log_level = log_level
def require_env(key):
    value = os.getenv(key)
    if value is None or value == "":
        raise MissingConfigError("Required environment variable is missing.")
    return value
def load_config():
    load_dotenv()
    api_key = require_env("OPENAI_API_KEY")
    log_level = require_env("LOG_LEVEL")

    return Config(openai_api_key=api_key, log_level=log_level)
