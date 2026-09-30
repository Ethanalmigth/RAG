import uuid
from qdrant_client import models
from app.core.qdrant import client, COLLECTION


async def store_chunks(document_id: uuid.UUID, chunks: list[dict], embeddings: list[list[float]]):
    doc_id = str(document_id)

    # idempotence : on supprime les anciens points du document
    await client.delete(
        COLLECTION,
        points_selector=models.FilterSelector(
            filter=models.Filter(must=[
                models.FieldCondition(key="document_id", match=models.MatchValue(value=doc_id))
            ])
        ),
    )

    points = [
        models.PointStruct(
            id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"{doc_id}:{c['index']}")),
            vector=emb,
            payload={
                "document_id": doc_id,
                "index": c["index"],
                "text": c["text"],
                "page_start": c["page_start"],
                "page_end": c["page_end"],
            },
        )
        for c, emb in zip(chunks, embeddings)
    ]

    for i in range(0, len(points), 100):
        await client.upsert(COLLECTION, points=points[i:i + 100])