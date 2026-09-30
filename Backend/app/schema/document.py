import uuid

from pydantic import BaseModel

from app.enums.type import TypeEnum


class DocumentResponse(BaseModel):
    document_id: uuid.UUID
    filename: str

class DocumentCreate(BaseModel):
    filename: str
    type:TypeEnum
    url: str





class RetrievedChunk(BaseModel):
    text: str
    page: int
    score: float


class SearchResponse(BaseModel):
    document_id: str
    results: list[RetrievedChunk]