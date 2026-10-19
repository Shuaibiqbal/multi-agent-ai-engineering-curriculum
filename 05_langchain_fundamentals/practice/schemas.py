from pydantic import BaseModel


class ExtractedInfo(BaseModel):
    name: str | None
    intent: str | None

