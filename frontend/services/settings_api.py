import requests
from config.settings import BASE_URL


def update_name(student_id, name):
    try:
        res = requests.put(
            f"{BASE_URL}/settings/update-name/{student_id}",
            json={"name": name},
            timeout=5
        )
        return res.json()
    except:
        return {"error": "Server error"}


def change_password(student_id, old_password, new_password):
    try:
        res = requests.put(
            f"{BASE_URL}/settings/change-password/{student_id}",
            json={
                "old_password": old_password,
                "new_password": new_password
            },
            timeout=5
        )
        return res.json()
    except:
        return {"error": "Server error"}