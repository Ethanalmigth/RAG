import uuid
from http import HTTPStatus
from pathlib import Path

import aiofiles
from fastapi import UploadFile, Depends

from app.schema.document import DocumentResponse, DocumentCreate
from app.enums.type import TypeEnum
from app.repository.document_repository import DocumentRepository
from app.exception.CustomException import CustomException


class DocumentService:
    def __init__(self, repo: DocumentRepository ,upload_dir: str = "storage/uploads"):
        self.directory = Path(upload_dir)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.chunk_size = 1024 * 1024
        self.max_size = 50 * 1024 * 1024
        self.allowed_extensions = {".pdf", ".txt", ".md", ".docx"}
        self.repo = repo

    async def store_file(self, file: UploadFile) -> DocumentResponse:
        filename = Path(file.filename or "").name
        extension = Path(filename).suffix.lower()
        if extension not in self.allowed_extensions:
            raise CustomException(message="Ce type de fichier n'est pas valide",status_code=HTTPStatus.BAD_REQUEST)

        document_id = uuid.uuid4()
        filepath = self.directory / f"{document_id}{extension}"

        size = 0
        try:
            async with aiofiles.open(filepath, mode="xb") as out:
                while True:
                    chunk = await file.read(self.chunk_size)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > self.max_size:
                        raise CustomException(message="Fichier trop grand",status_code=HTTPStatus.BAD_REQUEST)
                    await out.write(chunk)
        except Exception:
            filepath.unlink(missing_ok=True)
            raise CustomException(message="Une erreur cote serveur",status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        document_create = DocumentCreate(filename=filename,type=TypeEnum(extension),url=str(filepath))
        documentcreate =  await self.repo.create_document(document_create)
        return DocumentResponse(document_id=documentcreate.id, filename=document_create.filename)
