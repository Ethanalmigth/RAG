async function request(url, options) {
  let res;
  try {
    res = await fetch(url, options);
  } catch {
    throw new Error("Serveur injoignable. Vérifie que le backend tourne sur le port 8000.");
  }
  const body = await res.json().catch(() => null);
  if (!res.ok) {
    const detail = typeof body?.detail === "string" ? body.detail : null;
    throw new Error(body?.message || detail || `Erreur ${res.status}`);
  }
  return body.data;
}

export function uploadDocument(file) {
  const form = new FormData();
  form.append("file", file);
  return request("/api/documents/upload", { method: "POST", body: form });
}

export function ask(question, documentIds) {
  return request("/api/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question,
      document_ids: documentIds.length ? documentIds : null,
    }),
  });
}