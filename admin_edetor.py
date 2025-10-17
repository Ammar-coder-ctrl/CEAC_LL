import json

ADMIN_FILE = "admins.json"

def load_admins():
    try:
        with open(ADMIN_FILE, "r") as f:
            return json.load(f)["admins"]
    except:
        return []

def save_admins(admins):
    with open(ADMIN_FILE, "w") as f:
        json.dump({"admins": admins}, f, indent=2)

def is_admin(user_id) -> bool:
    return int(user_id) in [int(a) for a in load_admins()]

def add_admin(user_id) -> bool:
    admins = load_admins()
    if int(user_id) not in [int(a) for a in admins]:
        admins.append(int(user_id))
        save_admins(admins)
        return True
    return False

def remove_admin(user_id) -> bool:
    admins = load_admins()
    if int(user_id) in [int(a) for a in admins]:
        admins.remove(int(user_id))
        save_admins(admins)
        return True
    return False