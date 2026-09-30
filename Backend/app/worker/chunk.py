SEPARATORS = ["\n\n", "\n", ". ", " "]


def _split(text: str, size: int, seps=SEPARATORS) -> list[str]:
    if len(text) <= size:
        return [text]
    if not seps:
        return [text[i:i + size] for i in range(0, len(text), size)]

    sep, *rest = seps
    parts = text.split(sep)
    out = []
    for j, part in enumerate(parts):
        if j < len(parts) - 1:
            part += sep
        if len(part) > size:
            out.extend(_split(part, size, rest))
        else:
            out.append(part)
    return out


def _build(items, index):
    pages = [p for p, _ in items if p is not None]
    return {
        "index": index,
        "text": "".join(t for _, t in items).strip(),
        "page_start": min(pages) if pages else None,
        "page_end": max(pages) if pages else None,
    }


def chunk_pages(pages, size=1000, overlap=150):
    if overlap >= size:
        raise ValueError("overlap doit être inférieur à size")

    pieces = []
    for page, text in pages:
        parts = _split(text, size)
        if parts:
            parts[-1] += "\n"
        pieces.extend((page, p) for p in parts)

    chunks = []
    current, current_len = [], 0

    for page, piece in pieces:
        if current and current_len + len(piece) > size:
            chunks.append(_build(current, len(chunks)))

            keep, kept_len = [], 0
            for item in reversed(current):
                if kept_len + len(item[1]) > overlap:
                    break
                keep.insert(0, item)
                kept_len += len(item[1])
            current, current_len = keep, kept_len

        current.append((page, piece))
        current_len += len(piece)

    if current:
        chunks.append(_build(current, len(chunks)))

    return [c for c in chunks if c["text"]]