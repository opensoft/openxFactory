from __future__ import annotations

from pathlib import Path

from .authority_repository import (
    SourceCoordinates,
    TrustedSnapshot,
    TrustedSnapshotError,
    read_git_blob,
    read_trusted_family_blob,
    source_ancestry_findings,
    trusted_family_paths,
)
from .model import (
    Finding,
    Record,
    RecordDocument,
    as_record,
    load_record_document_texts,
)
from .pipeline import validate_governed_documents

ROOT = Path(__file__).resolve().parents[2]
FAMILY_DIR = ROOT / "contracts" / "intent-compliance"
AUTHORITY_KINDS = {
    "veto_class_vocabulary",
    "policy_allowance",
    "policy_allowance_revocation",
    "policy_allowance_registry",
}

__all__ = [
    "TrustedSnapshot",
    "load_authoritative_documents",
    "validate_authoritative_submission",
    "verify_authoritative_sources",
]


def load_authoritative_documents(
    snapshot: TrustedSnapshot,
) -> tuple[list[RecordDocument], list[Finding]]:
    paths = trusted_family_paths(snapshot)
    findings: list[Finding] = []
    inputs: list[tuple[str, Path]] = []
    for path in paths:
        data = read_trusted_family_blob(snapshot, path)
        source = Path(f"{snapshot.commit}:{path}")
        try:
            inputs.append((data.decode("utf-8"), source))
        except UnicodeDecodeError as error:
            raise TrustedSnapshotError(
                snapshot.repository, f"trusted family blob is not UTF-8: {source}"
            ) from error
    parsed = load_record_document_texts(inputs)
    documents = [
        document
        for document in parsed
        if document.data.get("kind") in AUTHORITY_KINDS
    ]
    if not documents:
        findings.append(
            Finding(
                "trusted-snapshot",
                snapshot.commit,
                "authoritative family contains no authority records",
            )
        )
    return documents, findings


def validate_authoritative_submission(
    submitted: list[RecordDocument], snapshot: TrustedSnapshot
) -> list[Finding]:
    authoritative, findings = load_authoritative_documents(snapshot)
    decisions = [
        document
        for document in submitted
        if document.data.get("kind") == "compliance_decision"
    ]
    governed = [*authoritative, *decisions]
    findings.extend(validate_governed_documents(governed, FAMILY_DIR))
    if any(finding.code == "schema" for finding in findings):
        return findings
    findings.extend(verify_authoritative_sources(governed, snapshot))
    return findings


def verify_authoritative_sources(
    documents: list[RecordDocument], snapshot: TrustedSnapshot
) -> list[Finding]:
    return _AuthorityVerifier(snapshot).verify(documents)


class _AuthorityVerifier:
    def __init__(self, snapshot: TrustedSnapshot) -> None:
        self.snapshot: TrustedSnapshot = snapshot
        self.cache: set[tuple[str, str, str]] = set()

    def verify(self, documents: list[RecordDocument]) -> list[Finding]:
        findings: list[Finding] = []
        for document in documents:
            label = str(document.path)
            match document.data.get("kind"):
                case "veto_class_vocabulary":
                    findings.extend(self._vocabulary(document.data, label))
                case "policy_allowance":
                    issuer = as_record(document.data.get("issuer")) or {}
                    approval = as_record(document.data.get("policy_approval")) or {}
                    findings.extend(self._attribution_source(issuer, label))
                    findings.extend(self._attribution_source(approval, label))
                case "policy_allowance_revocation":
                    revoker = as_record(document.data.get("revoker")) or {}
                    findings.extend(self._attribution_source(revoker, label))
                case "policy_allowance_registry" | "compliance_decision":
                    if document.data.get("kind") == "compliance_decision":
                        findings.extend(self._vocabulary(document.data, label))
                case _:
                    pass
        return findings

    def _vocabulary(self, vocabulary: Record, label: str) -> list[Finding]:
        source = as_record(vocabulary.get("policy_source"))
        if source is None:
            return []
        findings = self._trusted_source(source, label)
        ratification = as_record(source.get("ratification_record"))
        if ratification is not None:
            combined = {
                **ratification,
                "repository": source.get("repository"),
                "revision": source.get("revision"),
            }
            findings.extend(self._trusted_source(combined, label))
        return findings

    def _trusted_source(
        self, source: Record, label: str
    ) -> list[Finding]:
        repository = source.get("repository")
        revision = source.get("revision")
        path = source.get("path")
        expected = source.get("content_digest")
        match repository, revision, path, expected:
            case str(), str(), str(), str():
                coordinates = SourceCoordinates(revision, path, expected)
            case _:
                return [
                    Finding("authority-source", label, "source reference is incomplete")
                ]
        if repository.lower() != self.snapshot.repository_id.lower():
            return [
                Finding(
                    "authority-repository",
                    label,
                    "source repository differs from the trusted repository ID",
                )
            ]
        cache_key = (revision, path, expected)
        if cache_key in self.cache:
            return []
        findings = source_ancestry_findings(self.snapshot, revision, label)
        if findings:
            return findings
        data, findings = read_git_blob(self.snapshot.repository, coordinates, label)
        if data is None or findings:
            return findings
        self.cache.add(cache_key)
        return []

    def _attribution_source(self, proof: Record, label: str) -> list[Finding]:
        source = as_record(proof.get("authority_source"))
        if source is None:
            return [
                Finding(
                    "authority-source", label, "principal authority source is missing"
                )
            ]
        return self._trusted_source(source, label)
