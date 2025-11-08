import os, re, requests
from pathlib import Path
from typing import Dict, Any

from landingai_ade import LandingAIADE

# ---------------------------------------------
# HELPERS
# ---------------------------------------------
def pick(src: dict, *keys, default=None):
    """Return the first populated key from a dict."""
    for k in keys:
        if k in src and src[k]:
            return src[k]
    return default


# ---------------------------------------------
# 1. LandingAI ADE — SDK Client
# ---------------------------------------------
class SDKLandingAIADEClient:
    def __init__(self):
        self.api_key = os.getenv("VISION_AGENT_API_KEY") or os.getenv("LANDINGAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("VISION_AGENT_API_KEY or LANDINGAI_API_KEY is required.")

        self.model = os.getenv("LANDINGAI_ADE_MODEL", "dpt-2")
        self.client = LandingAIADE(apikey=self.api_key)

    def extract(self, file_path: str) -> Dict[str, Any]:
        try:
            response = self.client.parse(
                document=Path(file_path),
                model=self.model
            )
        except Exception as e:
            raise RuntimeError(f"ADE SDK extraction failed: {e}")

        fields_raw = response.get("fields", {}) or {}
        pages = response.get("pages", [])

        # Extract fields using known keys
        return {
            "full_name": pick(fields_raw, "full_name", "name", "Name"),
            "dob": pick(fields_raw, "dob", "date_of_birth"),
            "country": pick(fields_raw, "country", "nationality"),
            "address": pick(fields_raw, "address", "residential_address"),
            "document_type": pick(fields_raw, "document_type", "doc_type"),
            "document_number": pick(fields_raw, "document_number", "id_number"),
            "issue_date": pick(fields_raw, "issue_date", "issued"),
            "expiry_date": pick(fields_raw, "expiry_date", "expires"),
            "email": pick(fields_raw, "email", "Email"),

            # Optional metadata
            "confidence": fields_raw.get("confidence", None),
            "proof_of_address": bool(pick(fields_raw, "address")),
            "pep_flag": False,
            "sanctions_hit": False,
            "source_of_funds": None,
        }


# ---------------------------------------------
# 2. REST Client (fallback)
# ---------------------------------------------
class RESTLandingAIADEClient:
    def __init__(self):
        self.api_key = os.getenv("LANDINGAI_API_KEY")
        self.model = os.getenv("LANDINGAI_ADE_MODEL", "dpt-2")
        self.url = f"https://api.landing.ai/ade/models/{self.model}/parse"

    def extract(self, file_path: str) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            resp = requests.post(self.url, headers=headers, files=files)
        resp.raise_for_status()

        data = resp.json()
        fields = data.get("fields", {}) or {}

        return {
            "full_name": pick(fields, "full_name", "name"),
            "dob": pick(fields, "dob", "date_of_birth"),
            "country": pick(fields, "country"),
            "address": pick(fields, "address"),
            "document_type": pick(fields, "document_type"),
            "document_number": pick(fields, "document_number"),
            "issue_date": pick(fields, "issue_date"),
            "expiry_date": pick(fields, "expiry_date"),
            "email": pick(fields, "email"),
            "proof_of_address": bool(fields.get("address")),
            "pep_flag": False,
            "sanctions_hit": False,
            "source_of_funds": None
        }


# ---------------------------------------------
# 3. Mock Client (offline)
# ---------------------------------------------
class MockADEClient:
    def extract(self, file_path: str):
        return {
            "full_name": "John Synthetic",
            "dob": "1990-01-01",
            "country": "US",
            "address": "123 Market St",
            "document_type": "driver_license",
            "document_number": "SYNTH-001",
            "issue_date": "2022-01-01",
            "expiry_date": "2030-01-01",
            "email": "synthetic@example.com",
            "confidence": 0.99,
            "proof_of_address": True,
            "pep_flag": False,
            "sanctions_hit": False,
            "source_of_funds": "salary",
        }


# ---------------------------------------------
# 4. Client Selector
# ---------------------------------------------
def get_ade_client():
    mode = os.getenv("ADE_MODE", "sdk").lower()
    use_mock = os.getenv("USE_MOCK", "false").lower() == "true"

    if use_mock:
        return MockADEClient()

    if mode == "sdk":
        return SDKLandingAIADEClient()

    if mode == "rest":
        return RESTLandingAIADEClient()

    raise RuntimeError(f"Unknown ADE_MODE: {mode}")
