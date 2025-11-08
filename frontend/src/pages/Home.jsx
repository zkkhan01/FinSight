import React from "react";

export default function Home() {
  return (
    <div className="hero">
      <h1>AI-Driven KYC/AML Compliance</h1>
      <p>
        FinSight uses LandingAI ADE to extract document data and a transparent rules engine 
        to deliver explainable, auditable KYC/AML decisions.
      </p>

      <div className="row">
        <a href="#dashboard" className="btn">Go to Dashboard</a>
        <a 
          href="https://docs.landing.ai/api-reference/tools/ade-parse" 
          target="_blank" 
          className="btn secondary"
        >
          ADE Docs
        </a>
      </div>

      <div className="grid">
        <div className="card">
          <h3>Explainable</h3>
          <p>Every decision is supported by a rule, visible and auditable.</p>
        </div>
        <div className="card">
          <h3>Enterprise-Ready</h3>
          <p>Containerized backend, modular rules, production-grade API.</p>
        </div>
        <div className="card">
          <h3>Fast & Accurate</h3>
          <p>Powered by LandingAI’s high-performance document extraction engine.</p>
        </div>
        <div className="card">
          <h3>Dark/Light Mode</h3>
          <p>Beautiful fintech UI with premium design language.</p>
        </div>
      </div>
    </div>
  );
}
