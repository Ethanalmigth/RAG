from qdrant_client import AsyncQdrantClient, models

from app.core.setting import settings

COLLECTION = "chunks"
VECTOR_SIZE = 384

client = AsyncQdrantClient(url=settings.QDRANT_URL)


async def init_collection():
    if await client.collection_exists(COLLECTION):
        return
    await client.create_collection(
        COLLECTION,
        vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
    )
    await client.create_payload_index(
        COLLECTION,
        field_name="document_id",
        field_schema=models.PayloadSchemaType.KEYWORD,
    )