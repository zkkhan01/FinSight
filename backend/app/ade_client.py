
# Mock ADE client – deterministic extraction from filename hints.
import re
from typing import Dict, Any

class MockADEClient:
    def extract(self, file_path: str) -> Dict[str, Any]:
        f = file_path.lower()
        fields = {
            "full_name": "Alex Johnson",
            "dob": "1999-06-15",
            "country": "US",
            "document_type": "driver_license",
            "document_number": "D123-456-7890",
            "issue_date": "2022-07-01",
            "expiry_date": "2030-07-01",
            "address": "123 Market St, Chicago, IL 60616",
            "proof_of_address": True,
            "pep_flag": False,
            "sanctions_hit": False,
            "source_of_funds": "salary",
            "email": "alex.j@example.com"
        }
        if "canada" in f:
            fields["country"] = "CA"
            fields["address"] = "99 King St W, Toronto, ON M5H 1A1"
        if re.search(r"expired|temp", f):
            fields["expiry_date"] = "2024-01-01"
        if re.search(r"poabox|p\.o\.", f):
            fields["address"] = "P.O. Box 123, Anywhere"
            fields["proof_of_address"] = False
        if "pep" in f:
            fields["pep_flag"] = True
        if "sanction" in f:
            fields["sanctions_hit"] = True
        if "crypto" in f:
            fields["source_of_funds"] = "crypto_trading"
        return fields
