import React, { useState, useEffect } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export default function Dashboard() {
  const [file, setFile] = useState(null);
  const [rulesets, setRulesets] = useState([]);
  const [ruleset, setRuleset] = useState("");
  const [res, setRes] = useState(null);
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);

  // Fetch ruleset names
  useEffect(() => {
    fetch(`${API_BASE}/rules`)
      .then(r => r.json())
      .then(d => {
        const names = Object.keys(d.rulesets || {});
        setRulesets(names);
        setRuleset(names[0] || "");
      });
  }, []);

  // Compute gauge angle
  const score = res?.score ?? 0;
  const gaugeAngle = Math.round((score / 100) * 360) + "deg";

  async function analyze(e) {
    e.preventDefault();
    setErr("");
    setRes(null);

    if (!file) {
      setErr("Please upload a file.");
      return;
    }

    setLoading(true);

    const fd = new FormData();
    fd.append("file", file);
    fd.append("ruleset", ruleset);

    try {
      const r = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        body: fd
      });
      if (!r.ok) throw new Error("Request failed");
      setRes(await r.json());
    } catch (e) {
      setErr(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <section className="toolbar">
        <h2>Compliance Dashboard</h2>

        <div className="row" style={{ gap: 10 }}>
          <select value={ruleset} onChange={e => setRuleset(e.target.value)}>
            {rulesets.map(r => <option key={r}>{r}</option>)}
          </select>

          <label className="btn" style={{ position: "relative" }}>
            <input 
              type="file" 
              style={{ opacity: 0, position: "absolute", inset: 0 }} 
              onChange={e => setFile(e.target.files?.[0] || null)} 
            />
            Upload
          </label>

          <button className="btn" disabled={loading} onClick={analyze}>
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>
      </section>

      {err && <p style={{ color: "var(--bad)", marginTop: 10 }}>{err}</p>}

      <div className="grid">
        
        {/* Score Gauge */}
        <div className="card" style={{ gridColumn: "span 4" }}>
          <h3>Compliance Score</h3>

          <div className="meter" style={{ "--angle": gaugeAngle }}>
            <div className="ring"></div>
            <div className="inner">
              <div style={{ textAlign: "center" }}>
                <div style={{ fontSize: 36, fontWeight: 800 }}>{Math.round(score)}%</div>
                <div style={{ fontSize: 12, color: "var(--muted)" }}>Compliance</div>
              </div>
            </div>
          </div>
        </div>

        {/* Extracted Fields */}
        <div className="card" style={{ gridColumn: "span 8" }}>
          <h3>Extracted Fields</h3>

          <pre className="extract-box">
{JSON.stringify(res?.extracted_fields || {}, null, 2)}
          </pre>
        </div>

        {/* Rule Results */}
        <div className="card full">
          <h3>Rule Results</h3>

          {!res?.rule_results?.length ? (
            <p style={{ color: "var(--muted)" }}>Run an analysis to see results.</p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>Rule</th>
                  <th>Description</th>
                  <th>Status</th>
                  <th>Details</th>
                </tr>
              </thead>
              <tbody>
                {res.rule_results.map((rule, i) => (
                  <tr key={i}>
                    <td>{rule.id}</td>
                    <td>{rule.description}</td>
                    <td>
                      <span className={`pill ${rule.passed ? "good" : "bad"}`}>
                        {rule.passed ? "PASS" : "FAIL"}
                      </span>
                    </td>
                    <td>
                      <code>{JSON.stringify(rule.details)}</code>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}
