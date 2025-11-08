
from typing import List
from .models import RuleResult

def score_report(results: List[RuleResult]) -> float:
    if not results:
        return 0.0
    passed = sum(1 for r in results if r.passed)
    return round(100.0 * passed / len(results), 2)
