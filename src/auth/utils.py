import secrets

import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    bytes_password = bcrypt.hashpw(password.encode(), salt)
    return bytes_password.decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def generate_session_id(nbytes: int) -> str:
    return secrets.token_urlsafe(nbytes)
