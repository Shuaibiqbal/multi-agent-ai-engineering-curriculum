from logging_setup import get_logger
from config import load_config

config = load_config()
logger = get_logger(__name__)

logger.info("Loaded config for " + config.openai_api_key)


logger.info("Version2 code")

import os 
from pathlib import Path
from exception import MissConfigError

ENV_PATH = Path(".env")
BACKUP_PATH = Path(".env.backup")

def set_env_file(contents: str | None) -> None:

    os.environ.pop("OPENAI_API_KEY", None)
    os.environ.pop("LOG_LEVEL", None)

    if contents is None:
        ENV_PATH.unlink(missing_ok=True)
    else:
        ENV_PATH.write_text(contents)

def main() -> None:
    if ENV_PATH.exists():
        ENV_PATH.rename(BACKUP_PATH)
    try:
        set_env_file(None)
        try:
            load_config()
        except MissConfigError as e:
            print(f"case 1 (.env missing) --> MissingConfigError: {e}")
        set_env_file("LOG_LEVEL = INFO")

        try:
            load_config()
        except MissConfigError as e:
            print(f"case 2 (key missing) -> MissingConfigError: {e}")
        set_env_file("OPENAI_API_KEY = sk-test-321")
        config = load_config()
        print(f"case 3 (valid .env) -> COnfig Loaded, "
              f"log level {config.log_level}")
        get_logger("x")
        logger = get_logger("x")
        logger.info("case 4 (get_logger twice) -> printed exactly once")
    finally:
        ENV_PATH.unlink(missing_ok=True)
        if BACKUP_PATH.exists():
            BACKUP_PATH.rename(ENV_PATH)
if __name__ == "__main__":
    main()