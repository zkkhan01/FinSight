
import React, { useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function App() {
  const [file, setFile] = useState(null)
  const [ruleset, setRuleset] = useState('kyc_basic')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const onSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setResult(null)
    if (!file) { setError('Please choose a file.'); return; }
    const form = new FormData()
    form.append('file', file)
    form.append('ruleset', ruleset)
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/analyze`, { method: 'POST', body: form })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{maxWidth: 800, margin: '40px auto', fontFamily: 'system-ui'}}>
      <img width="120" height="120" alt="image" src="assets/finsight.png" /> 
      <h1>FinSight AI</h1>
      <p>AI-powered financial document insight.</p>
      <p>Upload a (synthetic) document to run KYC/AML checks with transparent rules.</p>

      <form onSubmit={onSubmit} style={{display:'grid', gap: 12}}>
        <label>
          <div>Choose file (PDF/IMG)</div>
          <input type="file" onChange={e => setFile(e.target.files?.[0] || null)} />
        </label>

        <label>
          <div>Ruleset</div>
          <select value={ruleset} onChange={e=>setRuleset(e.target.value)}>
            <option value="kyc_basic">kyc_basic</option>
          </select>
        </label>

        <button disabled={loading}>{loading ? 'Analyzing…' : 'Analyze'}</button>
      </form>

      {error && <p style={{color:'crimson'}}>{error}</p>}

      {result && (
        <div style={{marginTop: 24}}>
          <h2>Result</h2>
          <pre style={{background:'#f6f6f6', padding:12, borderRadius:8}}>
            {JSON.stringify(result, null, 2)}
          </pre>
          <h3>Score: {result.score}%</h3>
          <details>
            <summary>Extracted Fields</summary>
            <pre>{JSON.stringify(result.extracted_fields, null, 2)}</pre>
          </details>
        </div>
      )}
    </div>
  )
}
