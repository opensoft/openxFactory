from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from typing import override

from .model import JsonValue, Record

MAX_SAFE_INTEGER = 9_007_199_254_740_991


@dataclass(slots=True)
class CanonicalizationError(Exception):
    detail: str

    @override
    def __str__(self) -> str:
        return self.detail


def canonical_bytes(value: JsonValue) -> bytes:
    return _encode(value).encode("utf-8")


def canonical_digest(record: Record, digest_field: str) -> str:
    content = {key: value for key, value in record.items() if key != digest_field}
    return "sha256:" + hashlib.sha256(canonical_bytes(content)).hexdigest()


def _encode(value: JsonValue) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        if abs(value) > MAX_SAFE_INTEGER:
            raise CanonicalizationError("integer exceeds the interoperable JSON range")
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise CanonicalizationError("non-finite numbers are forbidden")
        raise CanonicalizationError("canonical records use integers only; floats are forbidden")
    if isinstance(value, str):
        if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
            raise CanonicalizationError("lone Unicode surrogates are forbidden")
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, list):
        return "[" + ",".join(_encode(item) for item in value) + "]"
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise CanonicalizationError("canonical object keys must be strings")
        ordered = sorted(value, key=lambda key: key.encode("utf-16-be"))
        return "{" + ",".join(
            f"{_encode(key)}:{_encode(value[key])}" for key in ordered
        ) + "}"
    raise CanonicalizationError(f"unsupported canonical JSON value: {type(value).__name__}")
