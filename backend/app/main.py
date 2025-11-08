
import os, uuid
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from .models import AnalyzeResponse, RulesInfo
from .rules_engine import RuleEngine
from .ade_client import LandingAIADEClient, MockADEClient
from .scoring import score_report

app = FastAPI(title="FinSight API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RuleEngine(rules_dir="app/rules")

from .ade_client import get_ade_client

ade = get_ade_client()


@app.get("/health")
def health():
    return {"status": "ok", "mode": "mock" if USE_MOCK else "ade"}

@app.get("/rules", response_model=RulesInfo)
def rules():
    return engine.describe()

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(file: UploadFile = File(...), ruleset: str = Form("kyc_advanced")):
    content = await file.read()
    doc_id = str(uuid.uuid4())
    tmp_path = f"/tmp/{doc_id}_{file.filename}"
    with open(tmp_path, "wb") as f:
        f.write(content)

    fields = ade.extract(tmp_path)
    results = engine.evaluate(fields, ruleset=ruleset)
    score = score_report(results)

    return AnalyzeResponse(
        document_id=doc_id,
        filename=file.filename,
        extracted_fields=fields,
        rule_results=results,
        score=score,
    )
