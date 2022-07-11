from passlib.context import CryptContext

# This tells passlib what the default hashing algorithm is to hash user passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)