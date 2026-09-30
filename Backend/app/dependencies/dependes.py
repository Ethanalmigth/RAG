from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.document_service import DocumentService
from app.core.engine import get_db
from app.repository.document_repository import DocumentRepository


async def get_document_repository(db:AsyncSession=Depends(get_db)) -> DocumentRepository:
    return DocumentRepository(db=db)

async def get_document_service(repo:DocumentRepository=Depends(get_document_repository)) -> DocumentService:
    return DocumentService(repo=repo)