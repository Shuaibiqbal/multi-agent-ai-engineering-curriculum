import logging


## Version one simple Message
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

screen_handler = logging.StreamHandler()
screen_handler.setLevel(logging.INFO)
logger.addHandler(screen_handler)

file_handler = logging.FileHandler("logs/app.log")
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

logger.debug("This only goes to the file.")

logger.info("This goes to both file and screen.")

logger.warning("this also goes to both")

##Version2 Wrapped in types function

def get_logger(name: str) -> logging.Logger:
    loggerv2 = logging.getLogger(name)

    loggerv2.setLevel(logging.DEBUG)

    screen_handlerv2 = logging.StreamHandler()
    screen_handlerv2.setLevel(logging.INFO)
    loggerv2.addHandler(screen_handler)

    file_handlerv2 = logging.FileHandler("logs/app.log")
    file_handlerv2.setLevel(logging.DEBUG)
    loggerv2.addHandler(file_handler)

    return loggerv2

loggerv2 = get_logger(__name__)

loggerv2.debug("from typed function. this goes to file only.")
loggerv2.info('from typed funcntion. this goes to terminal and file also.')
loggerv2.warning("from typed function this goes to both file and terminal ")
