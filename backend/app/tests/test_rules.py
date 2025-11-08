
from app.rules_engine import RuleEngine

def test_rulesets_load():
    eng = RuleEngine(rules_dir="app/rules")
    info = eng.describe()
    assert info["rulesets"]["kyc_basic"] >= 3
    assert info["rulesets"]["kyc_advanced"] >= 5
    assert info["rulesets"]["aml_advanced"] >= 3
