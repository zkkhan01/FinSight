
import React, { useState, useEffect } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function App(){
  const [file, setFile] = useState(null)
  const [rulesets, setRulesets] = useState(['kyc_advanced'])
  const [ruleset, setRuleset] = useState('kyc_advanced')
  const [res, setRes] = useState(null)
  const [err, setErr] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(()=>{
    fetch(`${API_BASE}/rules`).then(r=>r.json()).then(d=>{
      const names = Object.keys(d.rulesets || {})
      if(names.length) { setRulesets(names); setRuleset(names[0]) }
    }).catch(()=>{})
  },[])

  const submit = async (e)=>{
    e.preventDefault()
    setErr(''); setRes(null)
    if(!file) { setErr('Choose a file first.'); return }
    const form = new FormData()
    form.append('file', file)
    form.append('ruleset', ruleset)
    setLoading(true)
    try{
      const r = await fetch(`${API_BASE}/analyze`, { method:'POST', body: form })
      if(!r.ok) throw new Error(`HTTP ${r.status}`)
      const data = await r.json()
      setRes(data)
    }catch(e){ setErr(String(e)) } finally { setLoading(false) }
  }

  return (
    <div style={{maxWidth:900, margin:'40px auto', fontFamily:'system-ui'}}>
      <header style={{display:'flex', alignItems:'center', gap:12}}>
        <img src="/brand/finsight.png" width="36" height="36" alt="FinSight"/>
        <h1 style={{margin:0}}>FinSight</h1>
      </header>
      <p>Upload a (synthetic) document to run KYC/AML checks with transparent rule‑packs.</p>

      <form onSubmit={submit} style={{display:'grid', gap:12}}>
        <input type="file" onChange={e=>setFile(e.target.files?.[0]||null)} />
        <label>
          Ruleset:{" "}
          <select value={ruleset} onChange={e=>setRuleset(e.target.value)}>
            {rulesets.map(n=> <option key={n}>{n}</option>)}
          </select>
        </label>
        <button disabled={loading}>{loading?'Analyzing…':'Analyze'}</button>
      </form>

      {err && <p style={{color:'crimson'}}>{err}</p>}

      {res && (
        <section style={{marginTop:24}}>
          <h2>Report</h2>
          <p><b>Score:</b> {res.score}%</p>
          <details open><summary><b>Extracted Fields</b></summary>
            <pre style={{background:'#f6f6f6', padding:12, borderRadius:8}}>{JSON.stringify(res.extracted_fields,null,2)}</pre>
          </details>
          <details open><summary><b>Rule Results</b></summary>
            <pre style={{background:'#f6f6f6', padding:12, borderRadius:8}}>{JSON.stringify(res.rule_results,null,2)}</pre>
          </details>
        </section>
      )}
    </div>
  )
}
