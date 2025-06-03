import os
import json

CONSENT_FILE = "gdpr_consent.json"

def load_consent():
    try:
        if os.path.exists(CONSENT_FILE):
            with open(CONSENT_FILE, "r") as f:
                return json.load(f).get("consent", None)
    except (json.JSONDecodeError, IOError):
        return None
    return None

def save_consent(value):
    try:
        with open(CONSENT_FILE, "w") as f:
            json.dump({"consent": value}, f)
    except IOError as e:
        print("Error saving consent:", e)

def get_ad_consent():
    consent = load_consent()
    if consent == "personalized":
        return {"npa": "0"}  # Personalized ads allowed
    elif consent == "non_personalized":
        return {"npa": "1"}  # Non-personalized ads only
    return {}