from __future__ import annotations

import hashlib
import unicodedata

from .import_execution import source_content_text


def content_digest(raw: str) -> str:
    return hashlib.sha256(source_content_text(str(raw)).encode()).hexdigest()[:16]


def normalized_digest(raw: str) -> str:
    body = source_content_text(str(raw))
    body = unicodedata.normalize("NFC", body)
    body = body.replace("\r\n", "\n").replace("\r", "\n")
    body = "\n".join(line.rstrip() for line in body.split("\n"))
    return hashlib.sha256(body.rstrip("\n").encode()).hexdigest()[:16]
