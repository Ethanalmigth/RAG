from http import HTTPStatus
from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile

from app.dependencies.dependes import get_document_service
from app.schema.ResponseApi import ResponseApi
from app.schema.document import DocumentResponse
from app.service.document_service import DocumentService
from app.worker.worker import worker

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload", response_model=ResponseApi[DocumentResponse], status_code=HTTPStatus.CREATED)
async def upload_file(
    background: BackgroundTasks,
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
):
    reponse = await service.store_file(file)
    background.add_task(worker, reponse.document_id)
    return ResponseApi(success=True, message="Fichier enregistré", data=reponse)