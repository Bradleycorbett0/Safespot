import requests

BASE_URL = "https://safespot-c5e02-default-rtdb.europe-west1.firebasedatabase.app"

def get_data(collection):
    url = f"{BASE_URL}/{collection}.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data if data else {}
        print("Firebase error:", response.status_code, response.text)
        return {}
    except Exception as e:
        print("Exception in get_data:", e)
        return {}

def post_data(collection, payload):
    url = f"{BASE_URL}/{collection}.json"
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except Exception as e:
        print("Exception in post_data:", e)
        return False