import os
import requests

class ADEClient:
    """
    Real LandingAI ADE client using the universal DPT-2 model.
    No pipeline ID is required for the hackathon.
    """

    def __init__(self):
        self.api_key = os.getenv("LANDINGAI_API_KEY")
        self.model = "DPT-2"
        self.url = f"https://api.landing.ai/ade/models/{self.model}/parse"

    def extract(self, file_path: str):
        if not self.api_key:
            raise ValueError("Missing LANDINGAI_API_KEY in environment!")

        headers = {"Authorization": f"Bearer {self.api_key}"}

        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            response = requests.post(self.url, headers=headers, files=files)
            response.raise_for_status()
            data = response.json()

        fields = data.get("fields", {})

        # Map ADE → FinSight expected fields
        return {
            "full_name": fields.get("name"),
            "dob": fields.get("dob"),
            "country": fields.get("country"),
            "address": fields.get("address"),
            "document_type": fields.get("document_type"),
            "document_number": fields.get("id_number"),
            "issue_date": fields.get("issue_date"),
            "expiry_date": fields.get("expiry_date"),
            "email": fields.get("email"),
            "proof_of_address": fields.get("proof_of_address", False),

            # Extra fields required for AML rules
            "pep_flag": False,
            "sanctions_hit": False,
            "source_of_funds": None
        }
