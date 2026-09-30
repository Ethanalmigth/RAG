import asyncio
from uuid import UUID

from loguru import logger
from sqlalchemy import select, update

from app.core.engine import SESSION
from app.models.document import Documents
from app.worker.chunk import chunk_pages
from app.worker.embed import embed_texts
from app.worker.extract import extract_file
from app.worker.store import store_chunks
from app.enums.statusDocument import StatusDocument


class DocumentRejected(Exception):
    """Document vide ou illisible."""


async def set_status(id: int, status: StatusDocument, error: str | None = None):
    async with SESSION() as db:
        await db.execute(
            update(Documents)
            .where(Documents.id == id)
            .values(status=status, error=error)
        )
        await db.commit()


async def worker(id):
    await set_status(id, StatusDocument.Processing)
    try:
        async with SESSION() as db:
            result = await db.execute(
                select(Documents.url, Documents.type).where(Documents.id == id)
            )
            row = result.one_or_none()
        if row is None:
            raise ValueError(f"Document {id} introuvable")

        pages = await asyncio.to_thread(extract_file, row.type.value, row.url)

        chunks = chunk_pages(pages, size=500, overlap=80)
        if not chunks:
            raise DocumentRejected("Document vide ou illisible")

        embeddings = await embed_texts([c["text"] for c in chunks])
        await store_chunks(id, chunks, embeddings)

        await set_status(id, StatusDocument.SUCCESS)
        logger.info(f"Document {id} indexé : {len(chunks)} chunks")

    except DocumentRejected as e:
        logger.warning(f"Document {id} rejeté : {e}")
        await set_status(id, StatusDocument.REJECTED, str(e))

    except Exception:
        logger.exception(f"Échec de l'indexation du document {id}")
        await set_status(id, StatusDocument.REJECTED, "Échec de l'indexation")
        raise