
from pydantic import BaseModel
from typing import Dict, Any, List

class RuleResult(BaseModel):
    id: str
    description: str
    passed: bool
    details: Dict[str, Any] = {}

class AnalyzeResponse(BaseModel):
    document_id: str
    filename: str
    extracted_fields: Dict[str, Any]
    rule_results: List[RuleResult]
    score: float

class RulesInfo(BaseModel):
    rulesets: Dict[str, int]  # ruleset name -> count
