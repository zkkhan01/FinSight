
import os, json, requests, re
from typing import Dict, Any, List

# ------- Real ADE client (LandingAI) -------
class LandingAIADEClient:
    def __init__(self):
        self.api_key = os.getenv("LANDINGAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("LANDINGAI_API_KEY not set")
        self.model = os.getenv("LANDINGAI_ADE_MODEL", "DPT-2")
        self.url = f"https://api.landing.ai/ade/models/{self.model}/parse"

    def extract(self, file_path: str) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        # We post multipart file per ADE docs. Map response to FinSight schema
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            resp = requests.post(self.url, headers=headers, files=files, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        # Map ADE response to our normalized schema.
        # ADE often returns hierarchical/chunked structures; extract likely fields safely.
        def pick(*keys, src=None, default=None):
            src = src or {}
            for k in keys:
                if k in src and src[k]:
                    return src[k]
            return default

        # Try common top-level shapes
        fields_obj = data.get("fields") or data.get("data") or {}
        chunks = data.get("chunks") or data.get("pages") or []

        # Heuristic extraction from common keys
        full_name = pick("full_name","name","Name", src=fields_obj)
        dob       = pick("dob","date_of_birth","DoB","birth_date", src=fields_obj)
        country   = pick("country","Country","nationality", src=fields_obj)
        address   = pick("address","Address","residential_address", src=fields_obj)
        doc_type  = pick("document_type","doc_type","id_type", src=fields_obj)
        id_num    = pick("id_number","document_number","doc_number","number", src=fields_obj)
        issue     = pick("issue_date","issued","date_of_issue", src=fields_obj)
        expiry    = pick("expiry_date","expires","date_of_expiry", src=fields_obj)
        email     = pick("email","Email","e_mail", src=fields_obj)

        # Fallback: search chunks for simple patterns
        def from_chunks(pattern: str):
            rx = re.compile(pattern, re.I)
            for c in chunks:
                txt = c.get("text") or ""
                m = rx.search(txt)
                if m:
                    return m.group(1).strip() if m.groups() else txt.strip()
            return None

        if not full_name:
            full_name = from_chunks(r"Name\s*[:\-]\s*(.+)")
        if not dob:
            dob = from_chunks(r"(\d{4}-\d{2}-\d{2})")
        if not email:
            email = from_chunks(r"([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})")

        # Return normalized dictionary used by rules
        return {
            "full_name": full_name,
            "dob": dob,
            "country": country,
            "address": address,
            "document_type": doc_type,
            "document_number": id_num,
            "issue_date": issue,
            "expiry_date": expiry,
            "email": email,
            # Optional fields for AML demos (can be enriched by other services)
            "proof_of_address": bool(address),
            "pep_flag": False,
            "sanctions_hit": False,
            "source_of_funds": None
        }

# ------- Mock client (for credit‑saving & offline dev) -------
class MockADEClient:
    def extract(self, file_path: str) -> Dict[str, Any]:
        # Deterministic mock based on filename hints
        fname = os.path.basename(file_path).lower()
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
        if "canada" in fname:
            fields["country"] = "CA"
            fields["address"] = "99 King St W, Toronto, ON M5H 1A1"
        if "expired" in fname or "temp" in fname:
            fields["expiry_date"] = "2024-01-01"
        if "poabox" in fname or "p.o." in fname:
            fields["address"] = "P.O. Box 123, Anywhere"
            fields["proof_of_address"] = False
        if "pep" in fname:
            fields["pep_flag"] = True
        if "sanction" in fname:
            fields["sanctions_hit"] = True
        if "crypto" in fname:
            fields["source_of_funds"] = "crypto_trading"
        return fields
