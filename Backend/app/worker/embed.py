import asyncio
from fastembed import TextEmbedding

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
VECTOR_SIZE = 384

model = TextEmbedding(model_name=MODEL_NAME, cache_dir="/models")


def _embed(texts: list[str]) -> list[list[float]]:
    return [v.tolist() for v in model.embed(texts)]


async def embed_texts(texts: list[str]) -> list[list[float]]:
    return await asyncio.to_thread(_embed, texts)


async def embed_query(text: str) -> list[float]:
    res = await asyncio.to_thread(_embed, [text])
    return res[0]