from cryptography.fernet import Fernet, InvalidToken

from config import settings

_fernet: Fernet | None = None


def _get_fernet() -> Fernet:
    global _fernet
    if _fernet is None:
        key = settings.encryption_key.strip().encode()
        try:
            _fernet = Fernet(key)
        except (ValueError, TypeError) as e:
            raise ValueError(
                "ENCRYPTION_KEY must be a valid Fernet key "
                "(url-safe base64-encoded 32-byte key)."
            ) from e
    return _fernet


def encrypt(plaintext: str) -> str:
    return _get_fernet().encrypt(plaintext.encode("utf-8")).decode("utf-8")


def decrypt(ciphertext: str) -> str:
    try:
        return _get_fernet().decrypt(ciphertext.encode("utf-8")).decode("utf-8")
    except InvalidToken as e:
        raise ValueError("Failed to decrypt data") from e
