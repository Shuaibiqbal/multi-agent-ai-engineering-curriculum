import logging

def get_logger(name) -> logging.getLogger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    screen_handler = logging.StreamHandler()
    screen_handler.setLevel(level=logging.DEBUG)
    logger.addHandler(screen_handler)

    file_handler = logging.FileHandler("logs/doc4_build_task.log")
    file_handler.setLevel(level=logging.DEBUG)
    logger.addHandler(file_handler)

    return logger