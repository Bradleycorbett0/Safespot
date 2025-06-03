import os
import json

CONSENT_FILE = "gdpr_consent.json"

def load_consent():
    if os.path.exists(CONSENT_FILE):
        with open(CONSENT_FILE, "r") as f:
            return json.load(f).get("consent", None)
    return None

def save_consent(value):
    with open(CONSENT_FILE, "w") as f:
        json.dump({"consent": value}, f)

def get_ad_consent():
    consent = load_consent()
    if consent == "personalized":
        return {"npa": "0"}  # Personalized ads allowed
    elif consent == "non_personalized":
        return {"npa": "1"}  # Non-personalized ads only
    return {}