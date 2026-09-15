import logging

logging.getLogger(__name__)
logging.StreamHandler()
logging.FileHandler("app.log")

print("Hi")