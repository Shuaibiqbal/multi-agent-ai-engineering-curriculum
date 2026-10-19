from openai import OpenAI
from schemas import ExtractedInfo
from pydantic import ValidationError


EXTRACT_PROMPT = (
 "Pull the person's name and what they want out of the message. "
 "If there is no name or no request, use null — never guess."
)

def send_message(client: OpenAI, messages_history:list[dict], user_message: str, OPENAI_MODEL: str) ->str:
        
    messages_history.append({"role":"user", "content":user_message})
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages_history
    )
    reply = response.choices[0].message.content
    messages_history.append({"role":"assistant","content":reply})
    return reply
def stream_message(client: OpenAI, messages_history:list[dict], user_message: str, OPENAI_MODEL: str):
    messages_history.append({"role":"user", "content":user_message})
    
    stream = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=messages_history, 
            stream=True
            )
    full_reply = ""
    for chunk in stream:
        piece = chunk.choices[0].delta.content
        if piece:
            full_reply += piece
    messages_history.append({"role": "assistant", "content": full_reply})
    return full_reply
def create_client() -> OpenAI:
    return OpenAI()

def get_structured_reply(client: OpenAI, user_message: str, OPENAI_MODEL: str = "gpt-4o-mini") -> ExtractedInfo:
    try:
        completion = client.beta.chat.completions.parse(
            model=OPENAI_MODEL,
            messages=[
                {"role":"system", "content": EXTRACT_PROMPT},
                {"role":"user", "content": user_message}
            ],
            response_format=ExtractedInfo,
        )
    except ValidationError:
        return None
    message = completion.choices[0].message

    if message.refusal:
        return None
    info = message.parsed
    if info.name is None and info.intent is None:
        return None 
    return info 