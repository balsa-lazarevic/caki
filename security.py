from user import User
from werkzeug.security import safe_str_cmp

users = [
    User(1, "Aki", "d7d05512c864a5f867eff324ee146a3ad4fb0e4fe8c7cb679dfb3ee95592a2ea", 1)
]


username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return userid_mapping.get(user_id, None)
