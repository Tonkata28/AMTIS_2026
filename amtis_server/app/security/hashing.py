from argon2 import PasswordHasher
from ..errors.exceptions import AppError
from ..errors.error_codes import Codes


ph = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Returns a hash password of the provided
    """

    return ph.hash(password)

def verify_password(password_hash: str, password_str: str):
    try:
        ph.verify(hash=password_hash, password=password_str)
        return True
    except Exception:
        return False