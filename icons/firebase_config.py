import requests
FIREBASE_URL = "https://safespot-c5e02-default-rtdb.europe-west1.firebasedatabase.app"

def get_data(path):
    url = f"{FIREBASE_URL}/{path}.json"
    response = requests.get(url)
    return response.json()

def post_data(path, data):
    url = f"{FIREBASE_URL}/{path}.json"
    response = requests.post(url, json=data)
    return response.json()