
from app.rules_engine import RuleEngine

def test_rules_load():
    eng = RuleEngine(rules_dir="app/rules")
    info = eng.describe()
    assert "kyc_basic" in info["rulesets"]
    assert info["rulesets"]["kyc_basic"] >= 3

def test_eval_pass():
    eng = RuleEngine(rules_dir="app/rules")
    fields = {
        "full_name": "Alex J",
        "country": "US",
        "document_number": "D-1",
        "dob": "2000-01-01",
        "address": "123 Main St"
    }
    res = eng.evaluate(fields, "kyc_basic")
    assert all(r.passed or r.id == "kyc_address_required" for r in res)
