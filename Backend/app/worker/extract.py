from pathlib import Path

from docx import Document
from pypdf import PdfReader


def extract_pdf(url):
    reader = PdfReader(str(Path(url)))
    result= []

    for i,page in enumerate(reader.pages, start=1):
       text = page.extract_text() or ""
       text= text.strip()
       if text:
           result.append((i,text))
    return result

def extract_text(url):
    path = Path(url)
    text = path.read_text(encoding="utf-8-sig", errors="replace").strip()
    return [(None,text)]

def extract_docx(url):
    texts= Document(url)
    result= []
    for i,page in enumerate(texts.paragraphs, start=1):
        text = page.text or ""
        text= text.strip()
        if text:
            result.append((i,text))
    return result

EXTRACTORS={
    "pdf": extract_pdf,
    "docx": extract_docx,
    "txt": extract_text,
    "md": extract_text
}

def extract_file(type,url):
    extractor= EXTRACTORS.get(type.lower().lstrip("."))
    if extractor is None:
        raise ValueError(f"Invalid extractor type: {type}")
    return extractor(url)

