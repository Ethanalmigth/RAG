import { useEffect, useRef, useState } from "react";
import { ask, uploadDocument } from "./api.js";

const ACCEPT = ".pdf,.docx,.txt,.md";

// **gras** et [1] (citations) dans le texte renvoyé par Gemini
function Inline({ text }) {
  return text.split(/(\*\*[^*]+\*\*|\[\d+\])/g).map((part, i) => {
    if (part.startsWith("**")) return <strong key={i}>{part.slice(2, -2)}</strong>;
    if (/^\[\d+\]$/.test(part)) return <sup key={i} className="cite">{part.slice(1, -1)}</sup>;
    return part;
  });
}

function Answer({ text }) {
  const blocks = [];
  let list = [];
  const flush = () => {
    if (list.length) blocks.push({ list });
    list = [];
  };
  text.split("\n").forEach((line) => {
    const item = line.match(/^\s*[*-]\s+(.*)/);
    if (item) list.push(item[1]);
    else {
      flush();
      if (line.trim()) blocks.push({ p: line });
    }
  });
  flush();
  return blocks.map((b, i) =>
    b.list ? (
      <ul key={i}>{b.list.map((l, j) => <li key={j}><Inline text={l} /></li>)}</ul>
    ) : (
      <p key={i}><Inline text={b.p} /></p>
    )
  );
}

function Sources({ sources, names }) {
  if (!sources?.length) return null;
  return (
    <details className="sources">
      <summary>{sources.length} extraits utilisés</summary>
      <ol>
        {sources.map((s) => (
          <li key={s.n} value={s.n}>
            <div className="src-meta">
              {names[s.document_id] || "Document"}
              {s.page ? `, page ${s.page}` : ""} · pertinence {Math.round(s.score * 100)} %
            </div>
            <div className="src-text">{s.text.length > 300 ? s.text.slice(0, 300) + "…" : s.text}</div>
          </li>
        ))}
      </ol>
    </details>
  );
}

export default function App() {
  const [docs, setDocs] = useState([]);
  const [selected, setSelected] = useState(new Set());
  const [notice, setNotice] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const fileRef = useRef(null);
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, loading]);

  const names = Object.fromEntries(docs.map((d) => [d.id, d.name]));

  async function onFiles(files) {
    for (const file of files) {
      setNotice({ kind: "info", text: `Envoi de ${file.name}…` });
      try {
        const data = await uploadDocument(file);
        setDocs((d) => [...d, { id: String(data.document_id), name: file.name }]);
        setNotice({
          kind: "info",
          text: `${file.name} est envoyé. L'indexation prend quelques secondes : attends avant de poser ta question.`,
        });
      } catch (e) {
        setNotice({ kind: "error", text: e.message });
      }
    }
    fileRef.current.value = "";
  }

  function toggle(id) {
    setSelected((prev) => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  }

  async function send() {
    const question = input.trim();
    if (question.length < 3 || loading) return;
    setMessages((m) => [...m, { role: "user", text: question }]);
    setInput("");
    setLoading(true);
    try {
      const data = await ask(question, [...selected]);
      setMessages((m) => [...m, { role: "assistant", text: data.answer, sources: data.sources }]);
    } catch (e) {
      setMessages((m) => [...m, { role: "error", text: e.message }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <aside className="side">
        <h1>Mon RAG</h1>
        <button className="btn" onClick={() => fileRef.current.click()}>Ajouter un document</button>
        <input ref={fileRef} type="file" accept={ACCEPT} multiple hidden onChange={(e) => onFiles(e.target.files)} />
        <p className="hint">PDF, Word, texte ou Markdown.</p>
        {notice && <p className={`notice ${notice.kind}`} role="status">{notice.text}</p>}

        <h2>Documents</h2>
        {docs.length === 0 ? (
          <p className="hint">Aucun document pour l'instant. Ajoute-en un pour commencer.</p>
        ) : (
          <ul className="docs">
            {docs.map((d) => (
              <li key={d.id}>
                <label>
                  <input type="checkbox" checked={selected.has(d.id)} onChange={() => toggle(d.id)} />
                  <span>{d.name}</span>
                </label>
              </li>
            ))}
          </ul>
        )}
        {docs.length > 0 && (
          <p className="hint">
            {selected.size ? `Recherche limitée à ${selected.size} document(s).` : "Recherche dans tous les documents."}
          </p>
        )}
      </aside>

      <main className="chat">
        <div className="thread">
          {messages.length === 0 && (
            <div className="empty">
              <p>Pose une question sur tes documents.</p>
              <p className="hint">Les réponses citent leurs sources : ouvre « extraits utilisés » pour vérifier.</p>
            </div>
          )}
          {messages.map((m, i) => (
            <div key={i} className={`msg ${m.role}`}>
              {m.role === "assistant" ? (
                <>
                  <div className="answer"><Answer text={m.text} /></div>
                  <Sources sources={m.sources} names={names} />
                </>
              ) : (
                <p>{m.text}</p>
              )}
            </div>
          ))}
          {loading && <div className="msg assistant"><p className="hint">Recherche en cours…</p></div>}
          <div ref={endRef} />
        </div>

        <div className="composer">
          <textarea
            rows={2}
            value={input}
            placeholder="Ta question…"
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                send();
              }
            }}
          />
          <button className="btn" onClick={send} disabled={loading || input.trim().length < 3}>
            Envoyer
          </button>
        </div>
      </main>
    </div>
  );
}