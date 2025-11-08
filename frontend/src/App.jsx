import React, { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export default function App() {
  const [file, setFile] = useState(null);
  const [res, setRes] = useState(null);
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setErr("");
    setRes(null);

    if (!file) {
      setErr("Please choose a file.");
      return;
    }

    const form = new FormData();
    form.append("file", file);

    setLoading(true);

    try {
      const r = await fetch(`${API_BASE}/api/parse`, {
        method: "POST",
        body: form,
      });

      if (!r.ok) throw new Error(`HTTP ${r.status}`);

      const data = await r.json();
      setRes(data);
    } catch (e) {
      setErr(String(e));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", fontFamily: "system-ui" }}>
      <header style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <img src="/brand/finsight.png" width="36" height="36" alt="FinSight" />
        <h1 style={{ margin: 0 }}>FinSight</h1>
      </header>

      <p>Upload a document and extract key KYC/AML fields using LandingAI ADE.</p>

      <form onSubmit={submit} style={{ display: "grid", gap: 12 }}>
        <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button disabled={loading}>{loading ? "Analyzing…" : "Analyze"}</button>
      </form>

      {err && <p style={{ color: "crimson" }}>{err}</p>}

      {res && (
        <section style={{ marginTop: 24 }}>
          <h2>Extracted Data</h2>

          <details open>
            <summary><b>Full ADE Response</b></summary>
            <pre
              style={{
                background: "#f6f6f6",
                padding: 12,
                borderRadius: 8,
                maxHeight: 400,
                overflow: "auto",
              }}
            >
              {JSON.stringify(res, null, 2)}
            </pre>
          </details>
        </section>
      )}
    </div>
  );
}
