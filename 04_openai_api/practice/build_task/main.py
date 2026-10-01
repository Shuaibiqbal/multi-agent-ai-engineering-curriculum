import sys
import openai
from config import load_config
from logging_setup import get_logger
from chat_client import create_client, send_message, stream_message, get_structured_reply

def main() -> None:
    config = load_config("OPENAI_API_KEY", "OPENAI_MODEL")
    OPENAI_MODEL = config.openai_model
    logger = get_logger(__name__)

    client = create_client()

    system_message = {
        "role": "system", "content": "You are a helpful assistant."
    }

    history: list[dict] = [system_message]

    while True:
        user_input = input("You: ")
        if user_input == "/quite":
            break
        try:
            if user_input.startswith("/extract "):
                text = user_input.removeprefix("/extract")
                result = get_structured_reply(client, history, text, OPENAI_MODEL)
                if result is None:
                    print("Could not understand that clearly enough to extract.")
                else:
                    print(result)
        except openai.AuthenticationError:
            logger.error("Authentaication failed - check OPENAI_API_KEY")
            print("login failed - check your api")
            sys.exit(1)
        except openai.BadRequestError:
            logger.warning("Conversation too long, trim history.")
            print("That got too long - forgetting the oldest messages.")
            history = [history[0]] + history[-4:]
if __name__ == "__main__":
    main()