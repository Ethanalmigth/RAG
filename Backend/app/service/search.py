import uuid
from qdrant_client import models
from app.core.qdrant import client, COLLECTION
from app.worker.embed import embed_query


async def search(question: str, document_ids: list[uuid.UUID] | None = None, limit: int = 5):
    vector = await embed_query(question)
    flt = None
    if document_ids:
        flt = models.Filter(must=[
            models.FieldCondition(
                key="document_id",
                match=models.MatchAny(any=[str(d) for d in document_ids]),
            )
        ])
    res = await client.query_points(
        COLLECTION, query=vector, query_filter=flt, limit=limit, with_payload=True
    )
    return res.points