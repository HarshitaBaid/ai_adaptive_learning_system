import requests
from config.settings import BASE_URL

def login_user(data):
    return requests.post(f"{BASE_URL}/students/login", json=data)

def register_user(data):
    return requests.post(f"{BASE_URL}/students/register", json=data)