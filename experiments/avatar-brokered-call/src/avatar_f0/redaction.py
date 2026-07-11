"""Redaction allowlist + fail-closed prohibited-content scan (FR-017 / SC-007).

Evidence is built from typed models whose fields are an allowlist (durations, enums,
hashes, bounded codes, short notes). Before writing, this scan re-checks the serialized
structure and rejects any prohibited class: credential material, SDP/ICE, raw provider
payloads, audio/transcript bytes, arbitrary/high-cardinality identifiers, and unbounded
strings. A single finding ⇒ status FAIL and the run does not commit evidence.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

from . import FAIL, PASS

MAX_STRING_LEN = 1024
_HEX64 = re.compile(r"^[a-f0-9]{64}$")
_HEX_ONLY = re.compile(r"^[a-f0-9]+$")
_SDP_MARKERS = (re.compile(r"(^|\n)v=0"), re.compile(r"(^|\n)m=(audio|video)"),
                re.compile(r"(^|\n)a=(rtpmap|candidate|fingerprint|ice-)"),
                re.compile(r"candidate:\d"))
_KEY_MARKERS = (re.compile(r"sk-[A-Za-z0-9_\-]{16,}"), re.compile(r"\bBearer\s+\S+"),
                re.compile(r"OPENAI_API_KEY\s*[:=]"))
_DATA_AUDIO = re.compile(r"data:audio/")


@dataclass
class RedactionFinding:
    path: str          # location key path (structural, not the offending content)
    reason: str        # bounded reason code


def _is_secretish(s: str) -> bool:
    if _HEX_ONLY.match(s):
        return False  # lowercase hex hashes/tokens are allowed
    if len(s) < 40:
        return False
    compact = s.replace("-", "").replace("_", "")
    return (compact.isalnum() and any(c.isupper() for c in compact)
            and any(c.islower() for c in compact) and any(c.isdigit() for c in compact))


def _scan_string(path: str, s: str, findings: List[RedactionFinding]) -> None:
    if len(s) > MAX_STRING_LEN:
        findings.append(RedactionFinding(path, "unbounded_string"))
    for rx in _KEY_MARKERS:
        if rx.search(s):
            findings.append(RedactionFinding(path, "credential_material"))
            break
    for rx in _SDP_MARKERS:
        if rx.search(s):
            findings.append(RedactionFinding(path, "sdp_or_ice"))
            break
    if _DATA_AUDIO.search(s):
        findings.append(RedactionFinding(path, "raw_media"))
    if _is_secretish(s):
        findings.append(RedactionFinding(path, "high_entropy_token"))


def scan(obj, path: str = "$") -> List[RedactionFinding]:
    findings: List[RedactionFinding] = []

    def walk(node, p):
        if isinstance(node, str):
            _scan_string(p, node, findings)
        elif isinstance(node, dict):
            for k, v in node.items():
                walk(v, f"{p}.{k}")
        elif isinstance(node, (list, tuple)):
            for i, v in enumerate(node):
                walk(v, f"{p}[{i}]")
        elif isinstance(node, (bytes, bytearray)):
            findings.append(RedactionFinding(p, "raw_bytes"))
        # numbers / bools / None are allowlisted primitives

    walk(obj, path)
    return findings


def scan_prose(text: str, path: str = "$report") -> List[RedactionFinding]:
    """Prose-safe scan for the human-readable report.

    The narrative report is legitimately long, so the field-length and high-entropy
    heuristics do not apply; only hard prohibited classes (credentials, SDP/ICE, raw
    media) are rejected.
    """
    findings: List[RedactionFinding] = []
    for rx in _KEY_MARKERS:
        if rx.search(text):
            findings.append(RedactionFinding(path, "credential_material"))
            break
    for rx in _SDP_MARKERS:
        if rx.search(text):
            findings.append(RedactionFinding(path, "sdp_or_ice"))
            break
    if _DATA_AUDIO.search(text):
        findings.append(RedactionFinding(path, "raw_media"))
    return findings


def redaction_scan(obj) -> dict:
    """Return the schema ``redaction_scan`` object; status FAIL if any finding."""
    findings = scan(obj)
    return {
        "status": FAIL if findings else PASS,
        "prohibited_findings": len(findings),
    }
