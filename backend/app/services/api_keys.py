import hashlib
import hmac
import secrets


def generate_api_key() -> tuple[str, str, str]:
    """
    Generate an API key.

    Returns:
        raw_key: Shown to the user once.
        key_prefix: Safe identifier for displaying in the dashboard.
        key_hash: SHA-256 digest stored in the database.
    """
    raw_key = f"tw_live_{secrets.token_urlsafe(32)}"
    key_prefix = raw_key[:16]
    key_hash = hash_api_key(raw_key)

    return raw_key, key_prefix, key_hash


def hash_api_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def verify_api_key(raw_key: str, stored_hash: str) -> bool:
    candidate_hash = hash_api_key(raw_key)

    return hmac.compare_digest(candidate_hash, stored_hash)