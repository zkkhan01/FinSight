from landingai_ade import LandingAIADE
import os, re
from pathlib import Path
from typing import Dict, Any

class LandingAIADEClient:
    def __init__(self):
        self.api_key = os.getenv("VISION_AGENT_API_KEY") or os.getenv("LANDINGAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("VISION_AGENT_API_KEY or LANDINGAI_API_KEY not set")
        
        self.model = os.getenv("LANDINGAI_ADE_MODEL", "dpt-2")
        self.client = LandingAIADE(apikey=self.api_key)

    def extract(self, file_path: str) -> Dict[str, Any]:
        """Extract structured fields using LandingAI SDK."""
        resp = self.client.parse(
            document=Path(file_path),
            model=self.model,
        )

        # LandingAI SDK response is usually dict-like
        fields_block = resp.get("fields", {}) or {}

        # Helper to safely pull keys
        def get(*keys, default=None):
            for k in keys:
                if k in fields_block and fields_block[k]:
                    return fields_block[k]
            return default

        full_name = get("full_name", "name", "Name")
        dob = get("dob", "date_of_birth")
        country = get("country", "nationality")
        address = get("address", "residential_address")
        doc_type = get("document_type", "doc_type")
        id_number = get("document_number", "id_number")
        issue_date = get("issue_date", "issued")
        expiry_date = get("expiry_date", "expires")
        email = get("email", "Email")

        return {
            "full_name": full_name,
            "dob": dob,
            "country": country,
            "address": address,
            "document_type": doc_type,
            "document_number": id_number,
            "issue_date": issue_date,
            "expiry_date": expiry_date,
            "email": email,
            "proof_of_address": bool(address),
            "pep_flag": False,
            "sanctions_hit": False,
            "source_of_funds": None
        }
