
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from .models import AnalyzeResponse, RulesInfo
from .rules_engine import RuleEngine
from .ade_client import MockADEClient
from .scoring import score_report
import uuid

app = FastAPI(title="RegulaScan A API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RuleEngine(rules_dir="app/rules")
ade = MockADEClient()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/rules", response_model=RulesInfo)
def get_rules():
    info = engine.describe()
    return info

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(file: UploadFile = File(...), ruleset: str = Form("kyc_basic")):
    # Save upload (demo only; in prod store safely or stream)
    content = await file.read()
    doc_id = str(uuid.uuid4())
    tmp_path = f"/tmp/{doc_id}_{file.filename}"
    with open(tmp_path, "wb") as f:
        f.write(content)

    # Extract (mocked)
    fields = ade.extract(tmp_path)

    # Evaluate rules
    results = engine.evaluate(fields, ruleset=ruleset)

    # Score
    score = score_report(results)

    return AnalyzeResponse(
        document_id=doc_id,
        filename=file.filename,
        extracted_fields=fields,
        rule_results=results,
        score=score,
    )
