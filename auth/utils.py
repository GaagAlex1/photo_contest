from datetime import timedelta, datetime, timezone
import jwt
import bcrypt
from settings import settings


def encode_jwt(payload: dict,
               private_key: str = settings.auth_jwt.private_key_path.read_text(),
               algorithm: str = settings.auth_jwt.algorithm,
               expire_timedelta: timedelta | None = None,
               expire_minutes: int = settings.auth_jwt.access_token_expire_minutes
               ) -> bytes | str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    expire = now + (expire_timedelta if expire_timedelta else timedelta(minutes=expire_minutes))
    to_encode.update(
        iat=now,
        exp=expire
    )

    encoded: bytes = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(token: str | bytes,
               public_key: str = settings.auth_jwt.public_key_path.read_text(),
               algorithm: str = settings.auth_jwt.algorithm) -> dict:
    decoded: dict = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_passwd(password: str) -> bytes:
    salt = bcrypt.gensalt()
    passwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(passwd_bytes, salt)


def validate_passwd(password: str,
                    hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password
    )