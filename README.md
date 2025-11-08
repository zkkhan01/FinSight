
# RegulaScan A

AI-powered, rule-driven compliance analyzer for financial documents.  
**Goal:** Given a PDF/IMG of a KYC/AML doc (e.g., driver license + utility bill), extract structured fields using an ADE (Automated Document Extraction) pipeline, then apply transparent rules (YAML) and produce a pass/fail report with explanations.

## Why it's safe & within rules
- Uses publicly shareable, synthetic sample docs only (no PII).
- Deterministic, auditable rule engine; LLM is optional/assistive.
- No scraping, no bypassing auth, no restricted data sources.

## Architecture
```text
regulascanA_full/
├── backend/                # FastAPI + rules engine + mock ADE client
├── frontend/               # Minimal React app (upload & results)
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
