import os
from google import genai
from google.genai import types
from app.service.search import search

client = genai.Client()  # lit GEMINI_API_KEY dans l'environnement
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

SYSTEM = (
    "Tu réponds en français, uniquement à partir des extraits fournis. "
    "Si la réponse n'y figure pas, dis-le clairement. "
    "Cite les sources par leur numéro, par exemple [1]."
)


async def answer(question: str, document_ids: list[int] | None = None):
    points = await search(question, document_ids)
    if not points:
        return {"answer": "Aucun document pertinent trouvé.", "sources": []}

    context = "\n\n".join(
        f"[{i + 1}] (page {p.payload['page_start']})\n{p.payload['text']}"
        for i, p in enumerate(points)
    )

    res = await client.aio.models.generate_content(
        model=MODEL,
        contents=f"Extraits :\n{context}\n\nQuestion : {question}",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM,
            temperature=0.2,
        ),
    )

    return {
        "answer": res.text,
        "sources": [
            {
                "n": i + 1,
                "document_id": p.payload["document_id"],
                "page": p.payload["page_start"],
                "score": p.score,
                "text": p.payload["text"],
            }
            for i, p in enumerate(points)
        ],
    }