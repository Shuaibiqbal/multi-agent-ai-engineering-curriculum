import logging

def logging_setup(name: str) -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    screen_handler = logging.StreamHandler()
    screen_handler.setLevel(logging.DEBUG)
    logger.addHandler(screen_handler)

    file_handler = logging.FileHandler("logs/02_http.log")
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    return logger

