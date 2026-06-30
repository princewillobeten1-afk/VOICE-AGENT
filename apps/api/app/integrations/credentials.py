import json
from uuid import uuid4
from app.core.security import hash_token


def credential_fingerprint(payload: dict) -> str:
    return hash_token(json.dumps(payload, sort_keys=True, separators=(",", ":")))


def create_secret_ref(provider: str = "external_secret_manager") -> str:
    return f"{provider}:integration:{uuid4()}"


def redact_credential_metadata(payload: dict) -> dict:
    return {key: "***" for key in payload.keys()}