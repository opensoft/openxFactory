from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from .model import Finding, InputLimitError, load_single_mapping_text

IDENTIFIER: Final = re.compile(r"[a-z][a-z0-9_.:-]{2,127}")
AUTHORITY_DOCUMENT_KEYS: Final = {"schema_version", "kind", "authorizations"}
AUTHORIZATION_KEYS: Final = {"principal_id", "authority_role", "approval_ids"}
MAX_AUTHORIZATIONS: Final = 64
MAX_APPROVAL_IDS: Final = 64


@dataclass(frozen=True, slots=True)
class AuthorityAuthorization:
    principal_id: str
    authority_role: str
    approval_ids: frozenset[str]


def parse_authority_authorizations(
    data: bytes, label: str
) -> tuple[tuple[AuthorityAuthorization, ...] | None, list[Finding]]:
    source = Path(label)
    try:
        document = load_single_mapping_text(data.decode("utf-8"), source)
    except (UnicodeDecodeError, InputLimitError):
        return None, [
            Finding(
                "authority-source-content",
                label,
                "authority source must be one bounded UTF-8 YAML mapping",
            )
        ]
    entries = document.get("authorizations")
    if (
        set(document) != AUTHORITY_DOCUMENT_KEYS
        or document.get("schema_version") != 1
        or document.get("kind") != "intent_compliance_authority"
        or not isinstance(entries, list)
        or not 1 <= len(entries) <= MAX_AUTHORIZATIONS
    ):
        return None, [_invalid_authority_document(label)]
    authorizations: list[AuthorityAuthorization] = []
    identities: set[tuple[str, str]] = set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != AUTHORIZATION_KEYS:
            return None, [_invalid_authority_document(label)]
        principal_id = entry.get("principal_id")
        authority_role = entry.get("authority_role")
        approval_ids = entry.get("approval_ids")
        if (
            not isinstance(principal_id, str)
            or IDENTIFIER.fullmatch(principal_id) is None
            or not isinstance(authority_role, str)
            or IDENTIFIER.fullmatch(authority_role) is None
            or not isinstance(approval_ids, list)
            or len(approval_ids) > MAX_APPROVAL_IDS
            or any(
                not isinstance(approval_id, str)
                or IDENTIFIER.fullmatch(approval_id) is None
                for approval_id in approval_ids
            )
            or len(set(approval_ids)) != len(approval_ids)
            or (principal_id, authority_role) in identities
        ):
            return None, [_invalid_authority_document(label)]
        identities.add((principal_id, authority_role))
        authorizations.append(
            AuthorityAuthorization(
                principal_id,
                authority_role,
                frozenset(approval_ids),
            )
        )
    return tuple(authorizations), []


def _invalid_authority_document(label: str) -> Finding:
    return Finding(
        "authority-source-content",
        label,
        "authority source does not match the closed authorization document shape",
    )
