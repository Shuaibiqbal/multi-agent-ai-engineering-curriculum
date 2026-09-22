from config import load_config
from logging_setup import get_logger

logger = get_logger("main")
config = load_config()

logger.info(f"Loaded config with log_level: {config.log_level}")