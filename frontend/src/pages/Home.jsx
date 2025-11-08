import React from "react"

export default function Home({ goDashboard }) {
  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg, #0a1d3b, #10294f, #133a70)",
      color: "white",
      fontFamily: "Inter, system-ui",
      padding: "60px 30px",
      textAlign: "center"
    }}>
      
      {/* Logo */}
      <img src="/brand/finsight.png" alt="FinSight"
        style={{ width: 80, opacity: 0.9 }}
      />

      {/* Hero */}
      <h1 style={{
        marginTop: "40px",
        fontSize: "56px",
        fontWeight: 800,
        lineHeight: "1.1",
        textShadow: "0 4px 25px rgba(0,0,0,0.4)"
      }}>
        AI-Driven KYC & AML<br/>Verification for Modern Finance
      </h1>

      <p style={{
        fontSize: "20px",
        maxWidth: "700px",
        margin: "20px auto",
        opacity: 0.9,
      }}>
        FinSight uses LandingAI’s industry-leading Document Extraction (ADE)
        and our rule-driven compliance engine to evaluate identity, risk,
        and fraud indicators in seconds.
      </p>

      {/* CTA */}
      <button
        onClick={goDashboard}
        style={{
          marginTop: "40px",
          background: "#2d78f4",
          border: "none",
          padding: "16px 40px",
          fontSize: "20px",
          borderRadius: "50px",
          color: "white",
          cursor: "pointer",
          boxShadow: "0 8px 25px rgba(45,120,244,0.5)",
          transition: "0.2s",
        }}
      >
        Get Started →
      </button>

      {/* Value Props */}
      <div style={{
        marginTop: "90px",
        display: "flex",
        justifyContent: "center",
        flexWrap: "wrap",
        gap: "30px"
      }}>
        {[
          "Real-Time ADE Extraction",
          "Advanced KYC/AML Rule Engine",
          "Neon Score Risk Gauge",
          "Compliance-Ready Reports",
        ].map((txt, i) => (
          <div key={i} style={{
            padding: "25px 30px",
            background: "rgba(255,255,255,0.08)",
            borderRadius: "16px",
            backdropFilter: "blur(12px)",
            fontSize: "18px",
            minWidth: "260px",
          }}>
            {txt}
          </div>
        ))}
      </div>
    </div>
  )
}
