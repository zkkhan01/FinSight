
import yaml, re
from typing import Dict, Any, List
from .models import RuleResult
from datetime import date, datetime

class RuleEngine:
    def __init__(self, rules_dir: str):
        self.rules_dir = rules_dir
        self._cache = {}
        self._load_all()

    def _load_yaml(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or []

    def _load_all(self):
        import glob, os
        for p in glob.glob(f"{self.rules_dir}/*.yaml"):
            name = os.path.splitext(os.path.basename(p))[0]
            self._cache[name] = self._load_yaml(p)

    def describe(self):
        return {"rulesets": {k: len(v) for k, v in self._cache.items()}}

    def evaluate(self, fields: Dict[str, Any], ruleset: str) -> List[RuleResult]:
        rules = self._cache.get(ruleset, [])
        out: List[RuleResult] = []
        for rule in rules:
            out.append(self._eval_rule(fields, rule))
        return out

    def _eval_rule(self, fields: Dict[str, Any], rule: Dict[str, Any]) -> RuleResult:
        rid = rule.get("id", "rule")
        desc = rule.get("description", "")
        field = rule.get("field")
        cond = rule.get("when", "exists")
        allowed = rule.get("allowed_values", [])
        pattern = rule.get("pattern")
        min_age = rule.get("min_age")
        max_age = rule.get("max_age")
        value = fields.get(field) if field else None

        passed = False
        details = {"field": field, "value": value}

        if cond == "exists":
            passed = value is not None
        elif cond == "not_empty":
            passed = value not in (None, "", [])
        elif cond == "equals":
            passed = value == rule.get("equals")
        elif cond == "in":
            passed = value in allowed
            details["allowed_values"] = allowed
        elif cond == "regex":
            passed = bool(value) and bool(re.search(pattern, str(value)))
            details["pattern"] = pattern
        elif cond in ("min_age", "max_age"):
            dob = fields.get(field) if field else None
            age = None
            try:
                if dob:
                    d = datetime.strptime(str(dob), "%Y-%m-%d").date()
                    today = date.today()
                    age = today.year - d.year - ((today.month, today.day) < (d.month, d.day))
            except Exception:
                age = None
            details["age"] = age
            if cond == "min_age":
                passed = age is not None and age >= int(min_age or 0)
                details["min_age"] = min_age
            else:
                passed = age is not None and age <= int(max_age or 200)
                details["max_age"] = max_age
        elif cond == "not_in":
            passed = value not in allowed
            details["blocked_values"] = allowed
        elif cond == "implies":
            # If precondition is True, dependent field must satisfy 'equals' or 'in'
            pre_field = rule.get("pre_field")
            pre_equals = rule.get("pre_equals")
            dep_equals = rule.get("equals")
            dep_in = rule.get("allowed_values", [])
            pre_ok = fields.get(pre_field) == pre_equals
            if not pre_ok:
                passed = True  # vacuous truth
            else:
                if dep_equals is not None:
                    passed = (fields.get(field) == dep_equals)
                elif dep_in:
                    passed = (fields.get(field) in dep_in)
                else:
                    passed = False
            details.update({"pre_field": pre_field, "pre_equals": pre_equals})
        else:
            details["error"] = f"Unknown condition: {cond}"
            passed = False

        return RuleResult(id=rid, description=desc, passed=bool(passed), details=details)
