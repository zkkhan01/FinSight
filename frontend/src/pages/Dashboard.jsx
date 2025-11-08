import React, { useState, useEffect } from "react"

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000"
const blue = "#2d78f4"
const darkBg = "#0c1120"
const card = "#ffffff11"

export default function Dashboard({ goHome, setResultData }) {
  const [file, setFile] = useState(null)
  const [rulesets, setRulesets] = useState([])
  const [ruleset, setRuleset] = useState("")
  const [res, setRes] = useState(null)
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState("")

  useEffect(() => {
    fetch(`${API_BASE}/rules`).then(r => r.json()).then(d => {
      const names = Object.keys(d.rulesets || {})
      setRulesets(names)
      setRuleset(names[0])
    })
  }, [])

  const analyze = async () => {
    if (!file) return setErr("Please upload a document.")
    setErr("")
    setLoading(true)

    const form = new FormData()
    form.append("file", file)
    form.append("ruleset", ruleset)

    try {
      const r = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        body: form
      })
      const json = await r.json()
      setRes(json)
      setResultData(json)
    } catch (e) {
      setErr(String(e))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      minHeight: "100vh",
      background: darkBg,
      color: "white",
      fontFamily: "Inter, system-ui",
      padding: "40px 20px"
    }}>
      
      {/* Top bar */}
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        maxWidth: "1100px",
        margin: "0 auto",
        marginBottom: "20px"
      }}>
        <h2 style={{ fontSize: "32px", fontWeight: 700 }}>FinSight Dashboard</h2>
        <button
          onClick={goHome}
          style={{
            background: blue,
            padding: "10px 24px",
            borderRadius: "10px",
            border: "none",
            cursor: "pointer"
          }}
        >
          ← Back
        </button>
      </div>

      {/* Upload Card */}
      <div style={{
        maxWidth: "1100px",
        margin: "0 auto",
        padding: "25px",
        background: card,
        borderRadius: "20px",
        backdropFilter: "blur(12px)",
        marginBottom: "40px"
      }}>
        <h3>Upload Document</h3>
        <input type="file" onChange={e => setFile(e.target.files?.[0] || null)} />
        
        <div style={{ marginTop: "20px" }}>
          <label style={{ fontWeight: 600 }}>Ruleset:</label>
          <select
            value={ruleset}
            onChange={e => setRuleset(e.target.value)}
            style={{
              marginLeft: "14px",
              padding: "8px 12px",
              borderRadius: "10px"
            }}
          >
            {rulesets.map(r => <option key={r}>{r}</option>)}
          </select>
        </div>

        <button
          onClick={analyze}
          disabled={loading}
          style={{
            marginTop: "20px",
            padding: "12px 28px",
            fontSize: "16px",
            background: loading ? "#777" : blue,
            border: "none",
            color: "white",
            borderRadius: "10px",
            cursor: "pointer"
          }}
        >
          {loading ? "Analyzing…" : "Run Analysis"}
        </button>

        {err && <p style={{ color: "red", marginTop: "10px" }}>{err}</p>}
      </div>

      {/* RESULTS */}
      {res && (
        <div style={{ maxWidth: "1100px", margin: "0 auto" }}>

          {/* SCORE */}
          <div style={{ textAlign: "center", marginBottom: "40px" }}>
            <h3 style={{ fontSize: "28px", fontWeight: 700 }}>Risk Score</h3>

            <div style={{
              width: "180px",
              height: "180px",
              margin: "0 auto",
              borderRadius: "50%",
              background: `conic-gradient(${blue} ${res.score}%, #555 ${res.score}%)`,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontSize: "38px",
              fontWeight: 700,
              boxShadow: `0 0 35px ${blue}66`
            }}>
              {res.score}%
            </div>
          </div>

          {/* Rule Table */}
          <div style={{
            background: card,
            padding: "25px",
            borderRadius: "16px",
            backdropFilter: "blur(12px)"
          }}>
            <h3>Rule Results</h3>
            <table style={{ width: "100%", marginTop: "20px", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ background: blue }}>
                  <th style={{ padding: "12px" }}>Rule</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(res.rule_results).map(([rule, passed]) => (
                  <tr key={rule} style={{ background: passed ? "#1a3b1deb" : "#4a1313" }}>
                    <td style={{ padding: "10px" }}>{rule}</td>
                    <td style={{ textAlign: "center" }}>
                      {passed ? "✅" : "❌"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

        </div>
      )}
    </div>
  )
}
