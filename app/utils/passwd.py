import os
from dotenv import load_dotenv

from passlib.context import CryptContext

load_dotenv()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"])


def hash_password(password: str) -> str:
    return pwd_context.hash(password, salt=bytes(os.getenv('SECRET_KEY'), 'UTF-8'))
