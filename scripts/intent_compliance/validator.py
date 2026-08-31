from __future__ import annotations

from pathlib import Path

from .authority_validation import verify_authoritative_sources
from .fixture_metadata import expected_failure_code
from .model import (
    Finding,
    RecordDocument,
    load_record_documents,
)
from .pipeline import validate_governed_documents

ROOT = Path(__file__).resolve().parents[2]
FAMILY_DIR = ROOT / "contracts" / "intent-compliance"

__all__ = [
    "Finding",
    "RecordDocument",
    "expected_failure_code",
    "load_record_documents",
    "validate_documents",
    "verify_authoritative_sources",
]


def validate_documents(documents: list[RecordDocument]) -> list[Finding]:
    return validate_governed_documents(documents, FAMILY_DIR)
