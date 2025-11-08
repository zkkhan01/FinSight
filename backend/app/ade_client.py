
# Mock ADE client. Replace with a real vendor (LandingAI, etc.) as needed.
# For the hack/demo, we synthesize fields from filename hints.
import re
from typing import Dict, Any

class MockADEClient:
    def extract(self, file_path: str) -> Dict[str, Any]:
        # In real life, you would run OCR+parsing here.
        # We'll create deterministic, safe demo fields based on filename regexes.
        fname = file_path.lower()

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
        }

        if "canada" in fname:
            fields["country"] = "CA"
            fields["address"] = "99 King St W, Toronto, ON M5H 1A1"

        if re.search(r"temp|expired", fname):
            fields["expiry_date"] = "2024-01-01"

        if re.search(r"poabox|p\.o\.", fname):
            fields["address"] = "P.O. Box 123, Anywhere"
            fields["proof_of_address"] = False

        return fields
