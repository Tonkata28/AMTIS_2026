from ..models.user import User, UserLogin, StoredUser
from uuid import uuid4
from ..db.store import db
from ..errors.error_codes import Codes
from ..errors.exceptions import AppError
from ..security.hashing import hash_password, verify_password
from ..models.user import UpdateCredentials
from decimal import Decimal


def register_user(user: User) -> str:

    for r in db["users"].values():
        if r.email == user.email:
            raise AppError(Codes.CONFLICT)

    user_id = str(uuid4())
    db["users"][user_id] = StoredUser(
        id=user_id,
        email=user.email,
        balances=[
        
        ],
        stocks=[
        
        ],
        transactions=[
         
        ],
        country_code=user.countryCode,
        password_hash=hash_password(user.password)
    )

    return user_id


def authorize(credentials: UserLogin) -> str:
    """
    Returns the user id of the authenticated user, if the credentials are valid
    """
    res: tuple[str, StoredUser]|None = next(((uid, u) for uid, u in db["users"].items() if u.email == credentials.email), None)

    if res is None:
        raise AppError(Codes.MISSING_REQUIRED_FIELDS)

    if not verify_password(res[1].password_hash, credentials.password):
        raise AppError(Codes.AUTH_REQUIRED)

    return res[0]


def validate_new_password_rules(user: StoredUser, v: str):
    if not v.strip():
        raise AppError(Codes.MISSING_REQUIRED_FIELDS)
            
    if any([
        len(v) < 6,
        not any(e.isupper() for e in v),
        not any(e.islower() for e in v),
        not any(e.isdigit() for e in v),
        all(e.isalnum() for e in v),
        user.email.lower() in v.lower()
    ]):
        raise AppError(Codes.VALIDATION_FAILED)
    

def check_user_exists(user_id: str):
    user = db["users"].get(user_id)

    if user is None:
        raise AppError(Codes.AUTH_REQUIRED)
    
    return user

def change_password(user_id: str, credentials: UpdateCredentials):
    user = check_user_exists(user_id)
    
    assert credentials.currentPassword is not None
    if not verify_password(password_hash=user.password_hash, password_str=credentials.currentPassword):
        raise AppError(Codes.VALIDATION_FAILED)
    
    assert credentials.newPassword is not None
    validate_new_password_rules(user, credentials.newPassword)

    db["users"][user_id].password_hash = hash_password(credentials.newPassword)


def change_email(user_id: str, credentials: UpdateCredentials):
    """
    changes the countryCode attribute of the user with the provided id, assumes the email is already validated
    """
    user = check_user_exists(user_id)
    password = credentials.currentPassword if credentials.newPassword is None else credentials.newPassword # covers the case in which there is a posibility we changed the password with the new one before

    if password is None:
        raise AppError(Codes.INVALID_VALUE)

    if not verify_password(password_hash=user.password_hash, password_str=password):
        raise AppError(Codes.INVALID_VALUE)
    
    for u_id, r in db["users"].items():
        if r.email == credentials.email and user_id != u_id:
            raise AppError(Codes.CONFLICT)
    
    assert credentials.email is not None
    if credentials.email.lower() in password.lower():
        raise AppError(Codes.INVALID_VALUE)
    
    db["users"][user_id].email = credentials.email


def change_country_code(user_id: str, credentials: UpdateCredentials):
    """
    changes the countryCode attribute of the user with the provided id, assumes the countryCode is already validated
    """
    user = check_user_exists(user_id)

    user.country_code = credentials.countryCode

