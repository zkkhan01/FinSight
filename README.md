
# FinSight

FinSight is an AI‑powered financial document analyzer that combines document extraction (ADE-style) with a transparent, rule‑based engine to perform KYC/AML checks and produce audit‑ready compliance reports.

## Highlights
- **Explainable**: YAML rule‑packs, not opaque heuristics.
- **Safe demo**: Works with synthetic/anonymized samples.
- **Modular**: Swap in any Document Extraction provider (e.g., LandingAI ADE, AWS Textract).
- **Full stack**: FastAPI backend + React/Vite frontend + Docker compose.

## Architecture
```text
FinSight/
├── backend/                # API, rules engine, scoring, mock ADE client
├── frontend/               # React app for upload + results
├── assets/                 # Branding assets (logo)
└── docker-compose.yml
```

## Quickstart (Dev)
### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Visit http://localhost:5173 (frontend) with backend at http://localhost:8000.

### Docker
```bash
docker compose up --build
```

## API
- `GET /health` → status
- `GET /rules` → ruleset names and counts
- `POST /analyze` (multipart): `file`, optional `ruleset` (default `kyc_advanced`)

## Rules
Rule‑packs live in `backend/app/rules/`:
- `kyc_basic.yaml` – minimal identity checks
- `kyc_advanced.yaml` – stronger KYC checks (address, document, age, country lists, regex integrity)
- `aml_advanced.yaml` – AML heuristics: risk flags for jurisdictions, addresses, document mismatch, etc.

Add or modify YAML files to update policy without changing code.

## Security Notes
- Use only anonymized or synthetic data in demos.
- Configure real ADE credentials via environment variables if you integrate a live provider.

## License
MIT
