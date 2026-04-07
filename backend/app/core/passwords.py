from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(value: str) -> str:
    return pwd_context.hash(value)


def verify_password(plain_value: str, hashed_value: str) -> bool:
    return pwd_context.verify(plain_value, hashed_value)
