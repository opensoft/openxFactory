"""Gate G0 consumer handoff receipt validation (T069, T075).

The receipt is the openxFactory-side external record written after the Gate G0
contract bundle is consumed by the single canonical downstream install
repository ``opensoft/xFactory-Hermes-Install``.  Validation asserts the
consumer product identity before any object lookup, then independently
reproduces the closure packet and every recorded artifact from the exact landed
consumer commit -- committed Git object bytes only, never a mutable working
tree.  The finding shape and deterministic sort mirror the existing semantics
convention; missing or unfetchable objects raise a dependency error (exit 2).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Callable, Iterable, Mapping

from . import content

CONSUMER_REPOSITORY = "opensoft/xFactory-Hermes-Install"
PROVIDER_REPOSITORY = "opensoft/openxFactory"

_GIT_COMMIT = re.compile(r"^[0-9a-f]{40}$")
_CANONICAL_REPOSITORY = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?/[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?$"
)

ConsumerResolver = Callable[[str], Path]


class ConsumerHandoffDependencyError(RuntimeError):
    """An unavailable or unsafe consumer content dependency (CLI exit code 2)."""

    exit_code = 2
    code = "HGR-HANDOFF-DEPENDENCY"

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        if code is not None:
            self.code = code


def _finding(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "severity": "error", "path": path, "message": message}


def _sorted(findings: Iterable[Mapping[str, object]]) -> list[dict[str, str]]:
    return sorted(
        (dict(item) for item in findings),
        key=lambda item: (
            str(item.get("path", "")),
            str(item.get("code", "")),
            str(item.get("message", "")),
        ),
    )


def build_consumer_resolver(
    mappings: Mapping[str, Path | str] | None, root: Path | str | None
) -> ConsumerResolver:
    """Return a deterministic canonical-repository resolver.

    An explicit ``owner/repo`` mapping wins outright.  Otherwise a canonical
    ``owner/repo`` resolves ONLY to ``<root>/<owner>/<repo>`` or
    ``<root>/<owner>/<repo>.git`` under the mirror root; ambiguity (both
    present), absence, a non-canonical name, or a missing root all fail closed
    as a dependency error.  The rules match the domain-regression resolver in
    shape without sharing a mutable module.
    """

    normalized: dict[str, Path] = {}
    if mappings:
        for repository, target in mappings.items():
            if _CANONICAL_REPOSITORY.fullmatch(repository) is None:
                raise ConsumerHandoffDependencyError(
                    f"mapping key {repository!r} is not a canonical repository"
                )
            normalized[repository] = Path(target)
    root_path = Path(root) if root is not None else None

    def resolver(repository: str) -> Path:
        if repository in normalized:
            return normalized[repository]
        if _CANONICAL_REPOSITORY.fullmatch(repository) is None:
            raise ConsumerHandoffDependencyError(
                f"{repository!r} is not a canonical repository"
            )
        if root_path is None:
            raise ConsumerHandoffDependencyError(
                f"no checkout mapping or mirror root resolves {repository!r}"
            )
        owner, _, name = repository.partition("/")
        candidates = [
            candidate
            for candidate in (
                root_path / owner / name,
                root_path / owner / f"{name}.git",
            )
            if candidate.exists()
        ]
        if len(candidates) != 1:
            raise ConsumerHandoffDependencyError(
                f"mirror root does not resolve {repository!r} to exactly one checkout"
            )
        return candidates[0]

    return resolver


def _resolve_object(
    repository: Path, revision: str, path: str
) -> content.ResolvedGitContent:
    try:
        return content.resolve_git_object(repository, revision, path)
    except content.ContentResolutionError as exc:
        raise ConsumerHandoffDependencyError(str(exc)) from exc


def _internal_findings(receipt: Mapping[str, object]) -> list[dict[str, str]]:
    """Return field-agreement defects detectable without any Git object read."""

    findings: list[dict[str, str]] = []

    provider = receipt.get("provider")
    provider = provider if isinstance(provider, Mapping) else {}
    if provider.get("repository") != PROVIDER_REPOSITORY:
        findings.append(
            _finding(
                "HGR-HANDOFF-PROVIDER",
                "provider.repository",
                "provider repository must be the canonical provider "
                f"{PROVIDER_REPOSITORY!r}",
            )
        )
    if provider.get("tag") != receipt.get("bundle_tag"):
        findings.append(
            _finding(
                "HGR-HANDOFF-TAG",
                "provider.tag",
                "provider annotated tag must equal the recorded bundle_tag",
            )
        )

    consumer_commit = receipt.get("consumer_commit")
    if (
        not isinstance(consumer_commit, str)
        or _GIT_COMMIT.fullmatch(consumer_commit) is None
    ):
        findings.append(
            _finding(
                "HGR-HANDOFF-COMMIT",
                "consumer_commit",
                "consumer_commit must pin an exact 40-hex Git commit",
            )
        )

    packet = receipt.get("closure_packet")
    packet = packet if isinstance(packet, Mapping) else {}
    expected_packet_path = f"evidence/gates/g0/{receipt.get('bundle_tag')}.yaml"
    if packet.get("path") != expected_packet_path:
        findings.append(
            _finding(
                "HGR-HANDOFF-PACKET-PATH",
                "closure_packet.path",
                "closure packet path must be "
                f"{expected_packet_path!r} for the recorded bundle_tag",
            )
        )

    findings.extend(_structure_findings(receipt))
    findings.extend(_check_result_findings(receipt))
    return findings


def _structure_findings(receipt: Mapping[str, object]) -> list[dict[str, str]]:
    """Assert every block consumed during digest reproduction is present and typed.

    ``_digest_findings`` reads these blocks with raw subscripts against committed
    Git objects; without this guard a receipt that omits one (e.g.
    ``compatibility_manifest``) would raise an uncaught ``KeyError`` on the CLI
    runtime path, breaking the 0/1/2 exit-code contract (a contract defect must be
    a clean exit 1 with a finding).  Reported here so a malformed receipt is a
    field-agreement finding that short-circuits before any object read.
    """

    findings: list[dict[str, str]] = []

    def _require_ref(block: object, label: str) -> None:
        if (
            not isinstance(block, Mapping)
            or not isinstance(block.get("path"), str)
            or not block.get("path")
            or not isinstance(block.get("digest"), str)
            or not block.get("digest")
        ):
            findings.append(
                _finding(
                    "HGR-HANDOFF-STRUCTURE",
                    label,
                    f"{label} must be a mapping with a non-empty 'path' and 'digest'",
                )
            )

    _require_ref(receipt.get("closure_packet"), "closure_packet")
    for artifact in (
        "compatibility_manifest",
        "checker",
        "runtime_binding",
        "evidence",
    ):
        _require_ref(receipt.get(artifact), artifact)

    check_results = receipt.get("check_results")
    if not isinstance(check_results, Mapping):
        findings.append(
            _finding(
                "HGR-HANDOFF-STRUCTURE",
                "check_results",
                "check_results must be a mapping with 'positive' and 'negative' "
                "result lists",
            )
        )
        return findings
    for side in ("positive", "negative"):
        results = check_results.get(side)
        if not isinstance(results, list):
            findings.append(
                _finding(
                    "HGR-HANDOFF-STRUCTURE",
                    f"check_results.{side}",
                    f"check_results.{side} must be a list of recorded checks",
                )
            )
            continue
        for index, result in enumerate(results):
            if (
                not isinstance(result, Mapping)
                or not isinstance(result.get("evidence_path"), str)
                or not result.get("evidence_path")
                or not isinstance(result.get("evidence_digest"), str)
                or not result.get("evidence_digest")
            ):
                findings.append(
                    _finding(
                        "HGR-HANDOFF-STRUCTURE",
                        f"check_results.{side}[{index}]",
                        "each recorded check must carry a non-empty 'evidence_path' "
                        "and 'evidence_digest'",
                    )
                )
    return findings


def _check_result_findings(receipt: Mapping[str, object]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    check_results = receipt.get("check_results")
    check_results = check_results if isinstance(check_results, Mapping) else {}
    for side, required_outcome in (("positive", "pass"), ("negative", "fail")):
        results = check_results.get(side)
        results = results if isinstance(results, list) else []
        for index, result in enumerate(results):
            outcome = result.get("outcome") if isinstance(result, Mapping) else None
            if outcome != required_outcome:
                findings.append(
                    _finding(
                        "HGR-HANDOFF-CHECK-RESULTS",
                        f"check_results.{side}[{index}].outcome",
                        f"recorded {side} check outcome must be {required_outcome!r}",
                    )
                )
    return findings


def _digest_findings(
    receipt: Mapping[str, object], repository: Path, commit: str
) -> list[dict[str, str]]:
    """Reproduce every recorded artifact from committed bytes and compare digests."""

    findings: list[dict[str, str]] = []

    packet = receipt["closure_packet"]
    resolved = _resolve_object(repository, commit, packet["path"])
    if resolved.digest != packet["digest"]:
        findings.append(
            _finding(
                "HGR-HANDOFF-PACKET-DIGEST",
                "closure_packet.digest",
                "closure packet digest does not match the committed bytes",
            )
        )

    for artifact in (
        "compatibility_manifest",
        "checker",
        "runtime_binding",
        "evidence",
    ):
        block = receipt[artifact]
        resolved = _resolve_object(repository, commit, block["path"])
        if resolved.digest != block["digest"]:
            findings.append(
                _finding(
                    "HGR-HANDOFF-ARTIFACT-DIGEST",
                    f"{artifact}.digest",
                    f"{artifact} digest does not match the committed bytes",
                )
            )

    check_results = receipt["check_results"]
    for side in ("positive", "negative"):
        for index, result in enumerate(check_results[side]):
            resolved = _resolve_object(repository, commit, result["evidence_path"])
            if resolved.digest != result["evidence_digest"]:
                findings.append(
                    _finding(
                        "HGR-HANDOFF-ARTIFACT-DIGEST",
                        f"check_results.{side}[{index}].evidence_digest",
                        f"{side} check evidence digest does not match the "
                        "committed bytes",
                    )
                )
    return findings


def validate_handoff_receipt(
    receipt: Mapping[str, object], *, consumer_resolver: ConsumerResolver
) -> list[dict[str, str]]:
    """Validate one Gate G0 consumer handoff receipt.

    The consumer product identity is asserted FIRST and short-circuits before
    any repository resolution or object lookup, so a wrong-product receipt can
    never trigger downstream reads.  All remaining field-agreement defects are
    reported before object resolution; digest parity is proven only against the
    exact landed consumer commit.  Missing or unfetchable objects raise
    :class:`ConsumerHandoffDependencyError` (exit code 2).
    """

    if receipt.get("consumer_repository") != CONSUMER_REPOSITORY:
        return [
            _finding(
                "HGR-HANDOFF-CONSUMER-REPOSITORY",
                "consumer_repository",
                "consumer repository must be the canonical single downstream "
                f"install repository {CONSUMER_REPOSITORY!r}",
            )
        ]

    internal = _internal_findings(receipt)
    if internal:
        return _sorted(internal)

    repository = consumer_resolver(CONSUMER_REPOSITORY)
    commit = str(receipt["consumer_commit"])
    return _sorted(_digest_findings(receipt, repository, commit))
