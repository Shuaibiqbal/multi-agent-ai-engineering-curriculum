import os 
from exception import MissConfigError
from dotenv import load_dotenv

class Config:
    def __init__(self, openai_api_key, log_level):
        self.openai_api_key = openai_api_key
        self.log_level = log_level

def required_env(key):
    value = os.environ.get(key)
    if value is None or value == "":
        raise MissConfigError("Missing environment variable.")
    return value
def load_config() -> Config:
    load_dotenv()

    api_key = required_env("OPENAI_API_KEY")
    log_level = required_env("LOG_LEVEL")

    return Config(openai_api_key=api_key, log_level=log_level)
    