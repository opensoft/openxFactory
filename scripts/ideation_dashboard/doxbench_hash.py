"""Authority-grade content identities for doxBench working buffers.

Hashes are computed over the exact UTF-8 bytes supplied by the caller. This
module intentionally performs no Unicode, newline, whitespace, or Markdown
normalization: a stale-authority check must describe the bytes that would be
reviewed or saved, not a normalized approximation.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

SHA256_ALGORITHM = "sha256"
SHA256_HEX_LENGTH = 64
MAX_BUFFER_BYTES = 400_000


class ContentSizeError(ValueError):
    """Raised when exact UTF-8 content exceeds its declared byte limit."""

    def __init__(self, actual_bytes: int, limit_bytes: int) -> None:
        self.actual_bytes = actual_bytes
        self.limit_bytes = limit_bytes
        super().__init__(
            f"content is {actual_bytes} UTF-8 bytes; maximum is {limit_bytes}"
        )


class ContentEncodingError(ValueError):
    """Raised when text cannot be represented identically across runtimes."""

    def __init__(self) -> None:
        super().__init__("content contains an unpaired UTF-16 surrogate")


@dataclass(frozen=True, slots=True)
class ContentIdentity:
    """Public content identity shape shared by turn, Apply, and Save contracts."""

    algorithm: str
    hex: str

    def as_dict(self) -> dict[str, str]:
        return {"algorithm": self.algorithm, "hex": self.hex}


def _validated_limit(max_bytes: int | None) -> int | None:
    if max_bytes is None:
        return None
    if isinstance(max_bytes, bool) or not isinstance(max_bytes, int):
        raise TypeError("max_bytes must be a non-negative integer or None")
    if max_bytes < 0:
        raise ValueError("max_bytes must be non-negative")
    return max_bytes


def _exact_utf8(content: str) -> bytes:
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    try:
        return content.encode("utf-8")
    except UnicodeEncodeError as error:
        raise ContentEncodingError() from error


def utf8_size(content: str) -> int:
    """Return the exact encoded byte size without normalizing ``content``."""

    return len(_exact_utf8(content))


def sha256_hex(
    content: str,
    *,
    max_bytes: int | None = MAX_BUFFER_BYTES,
) -> str:
    """Hash exact UTF-8 content after enforcing the optional byte limit."""

    limit = _validated_limit(max_bytes)
    encoded = _exact_utf8(content)
    if limit is not None and len(encoded) > limit:
        raise ContentSizeError(len(encoded), limit)
    return hashlib.sha256(encoded).hexdigest()


def content_identity(
    content: str,
    *,
    max_bytes: int | None = MAX_BUFFER_BYTES,
) -> ContentIdentity:
    """Return the contract-shaped authority identity for exact text content."""

    return ContentIdentity(
        algorithm=SHA256_ALGORITHM,
        hex=sha256_hex(content, max_bytes=max_bytes),
    )
