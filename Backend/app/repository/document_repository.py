from http import HTTPStatus
from uuid import UUID

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Documents
from app.schema.document import DocumentCreate
from app.exception.CustomException import CustomException


class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_document(self, doc:DocumentCreate):
        document = Documents(filename=doc.filename, url=doc.url, type=doc.type)
        try:
            self.db.add(document)
            await self.db.commit()
            await self.db.refresh(document)
            return document
        except Exception:
            await self.db.rollback()
            raise CustomException(message="Probleme au niveau de la base de données",status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    async def get_document(self, document_id: UUID) :
        document = await self.db.execute(Select(Documents.url).where(Documents.id == document_id))
        return document.scalar_one_or_none()
