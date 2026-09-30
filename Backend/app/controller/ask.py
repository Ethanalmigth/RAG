from http import HTTPStatus
from fastapi import APIRouter

from app.schema.ResponseApi import ResponseApi
from app.schema.ask import AskRequest, AskResponse
from app.service.answer import answer

router = APIRouter(prefix="/api", tags=["ask"])


@router.post("/ask", response_model=ResponseApi[AskResponse], status_code=HTTPStatus.OK)
async def ask(body: AskRequest):
    result = await answer(body.question, body.document_ids)
    return ResponseApi(success=True, message="Réponse générée", data=AskResponse(**result))