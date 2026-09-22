import logging

def get_logger(name: str):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    screen_handler = logging.StreamHandler()
    screen_handler.setLevel(logging.DEBUG)
    logger.addHandler(screen_handler)

    file_handler = logging.FileHandler("logs/build_task.log")
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    return logger
