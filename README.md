<p align="center">
<img width="120" height="120" alt="image" src="assets/finsight.png" /> 
</p>

# FinSight  
**AI-powered financial document intelligence for automated KYC/AML compliance.**  

<p align="center">
  <img src="https://img.shields.io/badge/FinSight-AI%20Financial%20Insight-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/React-Frontend-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Compliance-KYC%2FAML-orange?style=for-the-badge" />
</p>

FinSight transforms PDFs and images into structured, validated, and audit-ready compliance insight using ADE-style extraction and a declarative rule engine.

> ✅ Built for speed  
> ✅ Built for transparency  
> ✅ Built for real financial workflows

FinSight is a financial document intelligence system that performs automated extraction, validation, and compliance assessment on unstructured financial documents. It integrates an ADE-style document extraction pipeline with a deterministic, rule-driven validation engine to deliver transparent, auditable financial insight at scale.

FinSight ingests PDF and image-based documents—such as KYC packets, identity documents, bank forms, and regulatory disclosures—then converts them into structured, machine-readable fields. These fields are normalized into a canonical schema and evaluated against declarative YAML rulepacks representing KYC, AML, and document-integrity controls. Each rule produces deterministic pass/fail outcomes with field-level evidence, metadata traces, and configuration-driven thresholds.

The architecture emphasizes explainability, reproducibility, and system-level transparency, making FinSight suitable for automated onboarding pipelines, internal audit workflows, and pre-compliance screening system

<p align="center">
<img width="750" height="500" alt="image" src="https://github.com/user-attachments/assets/e46b6614-ed82-4063-91a8-d76e939718a8" />
</p>

**Goal:** Given a PDF/IMG of a KYC/AML doc (e.g., driver license + utility bill), extract structured fields using an ADE (Automated Document Extraction) pipeline, then apply transparent rules (YAML) and produce a pass/fail report with explanations.

## Why it's safe & within rules
- Uses publicly shareable, synthetic sample docs only (no PII).
- Deterministic, auditable rule engine; LLM is optional/assistive.
- No scraping, no bypassing auth, no restricted data sources.

## Architecture
```text
FinSight/
├── backend/                   # FastAPI service
│   ├── app/
│   │   ├── ade_client.py      # Real/Mock ADE client
│   │   ├── rules_engine.py    # Declarative YAML logic
│   │   ├── scoring.py         # Compliance scoring
│   │   ├── models.py
│   │   ├── main.py            # API routes
│   │   └── rules/
│   │       ├── kyc_basic.yaml
│       └── aml_advanced.yaml
│
├── frontend/                  # Premium React dashboard
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Dashboard.jsx
│   │   ├── styles/finsight.css
│   │   ├── App.jsx
│   │   └── main.jsx
│
├── docker-compose.yml
└── README.md
```

## Quickstart (Dev)
### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:5173 (frontend) talking to http://localhost:8000 (backend).

## Docker
```bash
docker compose up --build
```

## Rules
- Define rules in YAML at `backend/app/rules/*.yaml`.
- Each rule has an `id`, `description`, `when` (field condition), and optional `pattern` or `allowed_values`.
- Add/modify rules without code changes.

## Example Rule (KYC)
```yaml
- id: kyc_name_present
  field: full_name
  description: "Legal name must be present"
  when: "exists"   # supported: exists, equals, in, regex, not_empty, min_age, max_age
- id: kyc_country_allowed
  field: country
  description: "Customer country must be in whitelist"
  when: "in"
  allowed_values: ["US","CA","UK"]
```

## API
- `GET /health` -> `{"status":"ok"}`
- `GET /rules` -> list loaded rules & counts
- `POST /analyze` (multipart form): `file=<pdf/img>` + optional `ruleset` name  
  Returns JSON report: extracted fields, rule outcomes, and a compliance score.

## Tests
```bash
cd backend
pytest -q
```

## Notes
- ADE integration is mocked for offline demo. Swap in real vendor SDK in `app/ade_client.py`.
- LLM (optional) prompt helper included but disabled by default to avoid network calls.
