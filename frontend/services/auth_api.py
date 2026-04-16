import requests
from config.settings import BASE_URL

def login_user(data):
    try:
        res = requests.post(f"{BASE_URL}/students/login", json=data)
        return res
    except requests.exceptions.RequestException:
        return None

def register_user(data):
    try:
        res = requests.post(f"{BASE_URL}/students/register", json=data)
        return res
    except requests.exceptions.RequestException:
        return None