import requests

# ✅ Your correct Firebase Realtime Database URL
FIREBASE_URL = "https://safespot-c5e02-default-rtdb.europe-west1.firebasedatabase.app"

def get_data(path):
    """
    Fetch data from Firebase at /path
    Example: get_data("spots/Liverpool")
    """
    url = f"{FIREBASE_URL}/{path}.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("❌ Firebase GET error:", response.text)
            return None
    except Exception as e:
        print("🔥 GET request failed:", e)
        return None


def save_data(path, data):
    """
    Save or update data using PATCH
    Example: save_data("spots/Liverpool", { "spot1": {...} })
    """
    url = f"{FIREBASE_URL}/{path}.json"
    try:
        response = requests.patch(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print("❌ Firebase PATCH error:", response.text)
            return None
    except Exception as e:
        print("🔥 PATCH request failed:", e)
        return None


def delete_data(path):
    """
    Delete a node
    Example: delete_data("spots/Liverpool/spot1")
    """
    url = f"{FIREBASE_URL}/{path}.json"
    try:
        response = requests.delete(url)
        if response.status_code == 200:
            return True
        else:
            print("❌ Firebase DELETE error:", response.text)
            return False
    except Exception as e:
        print("🔥 DELETE request failed:", e)
        return False