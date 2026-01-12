import hashlib
import json
from fastapi.encoders import jsonable_encoder

def stable_request_hash(payload: dict) -> str:
    """
    Stable hash so {a:1, b:2} and {b:2,a:1} hash the same
    hanldes date/UUID/Enum by converting to JSON-sfe types first.
    """
    encoded = jsonable_encoder(payload) #concerts date/UUID/Enum -> JSON-friendly
    normalized = json.dumps(encoded, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()