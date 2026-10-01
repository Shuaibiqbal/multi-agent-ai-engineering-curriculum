from openai import OpenAI
from chat_client import create_client, get_structured_reply, send_message

def test_normal_conversation(OPENAI_MODEL: str) -> None:
    # case 1: a normal 3-turn conversation should remember earlier turns
    client = create_client()
    history = [{"role": "system", "content": "You are a helpful assistant."}]
    user_msg = "My favorite color is teal."
    reply = send_message(client, history, user_msg, OPENAI_MODEL=OPENAI_MODEL)
    print(f"case 1 (3-turn memory) -> {reply}")
def test_bad_key() -> None:
    # case 2: a wrong API key should raise AuthenticationError, caught cleanly
    import openai
    bad_client = OpenAI(api_key="sk-fake-key-123")
    try:
        send_message(bad_client, [], "hi", OPENAI_MODEL)
    except openai.AuthenticationError:
        print("case 2 (bad key-> AuthenticationError caught") 
def test_context_limit() -> None:
    # case 3: a huge input should raise BadRequestError, not crash unhandled
    import openai
    client = create_client()
    huge_input = "Shuaib" *100000
    try:
        send_message(client, [], huge_input, OPENAI_MODEL)
    except openai.BadRequestError:
        print("case 3 (context limit) -> BadRequestError caught")
def test_structured_clear() -> None:
    # case 4: a clear input should come back as a valid ExtractedInfo
    client = create_client()
    result = get_structured_reply(client, [],"Maria wants to reset her password", OPENAI_MODEL=OPENAI_MODEL)
    print(f"case 4 (clear structured) -> {result}")
def test_structured_unclear() -> None:
    # case 5: an unclear input should not silently produce a wrong answer
    client = create_client()
    result = get_structured_reply(client, [], user_message="the sky is blue", OPENAI_MODEL=OPENAI_MODEL)
    # client: OpenAI, messages_history:list[dict], user_message:OPENAI_MODEL
    print(f"case 5 (unclear structured) -> {result}")

if __name__ == "__main__":
    from config import load_config
    config = load_config("OPENAI_API_KEY", "OPENAI_MODEL")
    OPENAI_MODEL = config.openai_model

    test_normal_conversation(OPENAI_MODEL)
    test_bad_key()
    test_context_limit()
    test_structured_clear()
    test_structured_unclear()