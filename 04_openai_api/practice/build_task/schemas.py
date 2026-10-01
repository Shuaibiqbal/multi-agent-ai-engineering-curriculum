from pydantic import BaseModel, ValidationError


class ExtractedInfo(BaseModel):
    name: str | None
    intent: str | None

