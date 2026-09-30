import uuid
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    document_ids: list[uuid.UUID] | None = None


class SourceResponse(BaseModel):
    n: int
    document_id: str
    page: int | None = None
    score: float
    text: str


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]