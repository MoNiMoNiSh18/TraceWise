from app.services.api_keys import (
    generate_api_key,
    hash_api_key,
    verify_api_key,
)


def test_api_key_generation():
    raw_key, prefix, key_hash = generate_api_key()

    assert raw_key.startswith("tw_live_")
    assert prefix == raw_key[:16]
    assert len(key_hash) == 64
    assert raw_key != key_hash


def test_api_key_verification():
    raw_key, _, stored_hash = generate_api_key()

    assert verify_api_key(raw_key, stored_hash)


def test_invalid_api_key_is_rejected():
    _, _, stored_hash = generate_api_key()

    assert not verify_api_key("invalid-api-key", stored_hash)


def test_api_key_hash_is_deterministic():
    key = "tw_live_test_key"

    assert hash_api_key(key) == hash_api_key(key)