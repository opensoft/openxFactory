"""Supported-Domain regression denominator conformance (T067, T072, T073).

Reproduces the exact published DomainxFactory ``stack.yaml`` blobs pinned by
``contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml``. Every
check reads only exact ``commit:path`` Git objects through
``content.resolve_git_object`` -- the mutable working tree of a domain checkout
is never consulted, and the real domain repositories are never modified. For
each conformant entry a duplicate-Customer negative is derived purely in memory
to prove the static-conformance check has teeth.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Mapping
from copy import deepcopy
import os
from pathlib import Path
import re

import yaml

from scripts.hermes_runtime_validation.content import (
    ContentResolutionError,
    resolve_git_object,
)

Finding = dict[str, str]
RepositoryResolver = Callable[[str], Path]

_CANONICAL_REPOSITORY = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?/"
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?$"
)
_CANONICAL_ROLES = ("customer", "client", "domain")
_MINIMUM_ENTRIES = 5


class DomainRegressionDependencyError(RuntimeError):
    """An unavailable or ambiguous domain-regression dependency (CLI exit 2)."""

    exit_code = 2
    code = "HGR-REGRESSION-DEPENDENCY"

    def __init__(self, message: str) -> None:
        super().__init__(message)


def _finding(code: str, path: str, message: str) -> Finding:
    return {"code": code, "severity": "error", "path": path, "message": message}


def _sorted(findings: list[Finding]) -> list[Finding]:
    unique: dict[tuple[str, str], Finding] = {}
    for finding in findings:
        unique.setdefault((finding["path"], finding["code"]), finding)
    return sorted(
        unique.values(), key=lambda finding: (finding["path"], finding["code"])
    )


def build_repository_resolver(
    mappings: Mapping[str, Path] | None,
    root: Path | None,
) -> RepositoryResolver:
    """Return a deterministic canonical-repository resolver.

    Explicit ``mappings`` (``owner/repo`` -> checkout) win over ``root``. Under a
    mirror ``root`` a canonical ``owner/repo`` resolves ONLY to
    ``<root>/<owner>/<repo>`` or ``<root>/<owner>/<repo>.git``; if both or
    neither exist, or the repository name is not canonical, resolution fails
    closed with a dependency error (exit 2).
    """

    resolved_mappings: dict[str, Path] = {}
    for repository, checkout in (mappings or {}).items():
        if (
            not isinstance(repository, str)
            or _CANONICAL_REPOSITORY.fullmatch(repository) is None
        ):
            raise DomainRegressionDependencyError(
                f"domain repository mapping key is not canonical: {repository!r}"
            )
        resolved_mappings[repository] = Path(checkout)
    mirror_root = Path(root) if root is not None else None

    def resolve(repository: str) -> Path:
        if (
            not isinstance(repository, str)
            or _CANONICAL_REPOSITORY.fullmatch(repository) is None
        ):
            raise DomainRegressionDependencyError(
                f"domain repository is not canonical: {repository!r}"
            )
        if repository in resolved_mappings:
            return resolved_mappings[repository]
        if mirror_root is None:
            raise DomainRegressionDependencyError(
                f"no domain repository mapping or mirror root resolves {repository!r}"
            )
        owner, name = repository.split("/", 1)
        candidates = [
            mirror_root / owner / name,
            mirror_root / owner / f"{name}.git",
        ]
        present = [candidate for candidate in candidates if candidate.is_dir()]
        if len(present) != 1:
            detail = "is ambiguous" if len(present) > 1 else "is unavailable"
            raise DomainRegressionDependencyError(
                f"mirror resolution of {repository!r} {detail}"
            )
        return present[0]

    return resolve


def _parse_stack(data: bytes) -> object:
    return yaml.safe_load(data.decode("utf-8"))


def _stack_is_conformant(stack: object) -> bool:
    """Return whether one parsed stack satisfies canonical static conformance.

    Mirrors the canonical DomainxFactory rule enforced by
    ``scripts/validate-domain-factory.py``: the document declares the domain
    stack kind and exactly one Hermes layer for each canonical role
    (customer/client/domain); duplicate or missing canonical roles are
    non-conformant. Extension layers are unconstrained.
    """

    if not isinstance(stack, Mapping):
        return False
    if stack.get("kind") != "xfactory_domain_stack":
        return False
    hermes = stack.get("hermes")
    if not isinstance(hermes, Mapping):
        return False
    layers = hermes.get("layers")
    if not isinstance(layers, list):
        return False
    role_counts: Counter[str] = Counter()
    for layer in layers:
        if isinstance(layer, Mapping) and isinstance(layer.get("role"), str):
            role_counts[layer["role"]] += 1
    return all(role_counts.get(role, 0) == 1 for role in _CANONICAL_ROLES)


def _with_duplicate_customer(stack: object) -> object:
    """Return an in-memory copy of one stack with a second Customer role added.

    The real domain repository and its resolved bytes are never mutated: the
    derived negative operates on a deep copy of the parsed document so the
    static-conformance check can be proven to reject a duplicate Customer
    template (an alternate authority path).
    """

    derived = deepcopy(stack) if isinstance(stack, Mapping) else {}
    if not isinstance(derived, dict):
        derived = {}
    duplicate_layer = {
        "role": "customer",
        "display_name": "Injected Duplicate Customer",
        "overlay": "hermes/customer-duplicate",
    }
    hermes = derived.get("hermes")
    if not isinstance(hermes, dict):
        derived["hermes"] = {"layers": [duplicate_layer, dict(duplicate_layer)]}
        return derived
    layers = hermes.get("layers")
    if not isinstance(layers, list):
        hermes["layers"] = [duplicate_layer, dict(duplicate_layer)]
        return derived
    hermes["layers"] = [*layers, duplicate_layer]
    return derived


def validate_domain_regression(
    inventory: Mapping[str, object],
    *,
    resolver: RepositoryResolver,
) -> list[Finding]:
    """Return deterministic HGR-REGRESSION findings for one regression inventory.

    Structural and self-consistency checks (shape, denominator size, duplicate
    repositories, cited exclusions) run first and short-circuit before any Git
    object is read. Only a well-formed inventory proceeds to exact
    ``commit:path`` blob resolution, digest parity, expected openxFactory
    contract-pin parity, static conformance, and the duplicate-Customer derived
    negative. Missing or unavailable exact objects raise
    ``DomainRegressionDependencyError`` (exit 2).
    """

    findings: list[Finding] = []
    if not isinstance(inventory, Mapping):
        return [
            _finding(
                "HGR-REGRESSION-INVENTORY-SHAPE",
                "$",
                "domain regression inventory must be a mapping",
            )
        ]

    entries = inventory.get("entries")
    if not isinstance(entries, list):
        findings.append(
            _finding(
                "HGR-REGRESSION-INVENTORY-SHAPE",
                "entries",
                "entries must be a list",
            )
        )
        entries = []
    exclusions = inventory.get("exclusions")
    if not isinstance(exclusions, list):
        findings.append(
            _finding(
                "HGR-REGRESSION-INVENTORY-SHAPE",
                "exclusions",
                "exclusions must be a list",
            )
        )
        exclusions = []

    if len(entries) < _MINIMUM_ENTRIES:
        findings.append(
            _finding(
                "HGR-REGRESSION-DENOMINATOR-SIZE",
                "entries",
                f"the regression denominator requires at least {_MINIMUM_ENTRIES} entries",
            )
        )
    if not exclusions:
        findings.append(
            _finding(
                "HGR-REGRESSION-DENOMINATOR-SIZE",
                "exclusions",
                "at least one explicit exclusion is required",
            )
        )

    for position, exclusion in enumerate(exclusions):
        path = f"exclusions[{position}]"
        if not isinstance(exclusion, Mapping):
            findings.append(
                _finding(
                    "HGR-REGRESSION-INVENTORY-SHAPE",
                    path,
                    "exclusion must be a mapping",
                )
            )
            continue
        reason = exclusion.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            findings.append(
                _finding(
                    "HGR-REGRESSION-MISSING-EXCLUSION-REASON",
                    path,
                    "each exclusion requires a non-empty cited reason",
                )
            )
        evidence = exclusion.get("evidence")
        if not isinstance(evidence, str) or not evidence.strip():
            findings.append(
                _finding(
                    "HGR-REGRESSION-EXCLUSION-EVIDENCE",
                    path,
                    "each exclusion requires cited evidence",
                )
            )

    seen_repositories: set[str] = set()
    for position, entry in enumerate(entries):
        path = f"entries[{position}]"
        if not isinstance(entry, Mapping):
            findings.append(
                _finding(
                    "HGR-REGRESSION-INVENTORY-SHAPE",
                    path,
                    "entry must be a mapping",
                )
            )
            continue
        repository = entry.get("repository")
        if not isinstance(repository, str) or not repository:
            findings.append(
                _finding(
                    "HGR-REGRESSION-INVENTORY-SHAPE",
                    path,
                    "entry requires a canonical repository",
                )
            )
            continue
        if repository in seen_repositories:
            findings.append(
                _finding(
                    "HGR-REGRESSION-DUPLICATE-REPOSITORY",
                    path,
                    f"repository {repository} is declared more than once",
                )
            )
        seen_repositories.add(repository)

    # Exact-object resolution only makes sense on a well-formed inventory. Any
    # structural or self-consistency defect short-circuits before any Git read.
    if findings:
        return _sorted(findings)

    for position, entry in enumerate(entries):
        path = f"entries[{position}]"
        repository = str(entry["repository"])
        commit = entry.get("commit")
        stack_path = entry.get("stack_path")
        stack_digest = entry.get("stack_digest")
        expected_ref = entry.get("expected_contract_ref")
        expected_csv = entry.get("expected_contract_schema_version")
        expected_result = entry.get("expected_result")

        repository_path = resolver(repository)
        try:
            resolved = resolve_git_object(repository_path, str(commit), str(stack_path))
        except ContentResolutionError as error:
            raise DomainRegressionDependencyError(
                f"exact {repository}@{commit}:{stack_path} is unavailable"
            ) from error

        if resolved.digest != stack_digest:
            findings.append(
                _finding(
                    "HGR-REGRESSION-DIGEST-MISMATCH",
                    path,
                    "resolved stack blob digest does not match the pinned stack_digest",
                )
            )

        try:
            stack = _parse_stack(resolved.data)
        except (UnicodeDecodeError, yaml.YAMLError):
            findings.append(
                _finding(
                    "HGR-REGRESSION-STATIC-CONFORMANCE",
                    path,
                    "resolved stack.yaml is not parseable YAML",
                )
            )
            continue

        xfactory = stack.get("xfactory") if isinstance(stack, Mapping) else None
        actual_ref = (
            xfactory.get("contract_ref") if isinstance(xfactory, Mapping) else None
        )
        actual_csv = (
            xfactory.get("contract_schema_version")
            if isinstance(xfactory, Mapping)
            else None
        )
        if actual_ref != expected_ref or actual_csv != expected_csv:
            findings.append(
                _finding(
                    "HGR-REGRESSION-CONTRACT-REF",
                    path,
                    "resolved stack.yaml openxFactory contract pin does not match the "
                    "expected pin",
                )
            )

        conformant = _stack_is_conformant(stack)
        if expected_result != "pass":
            findings.append(
                _finding(
                    "HGR-REGRESSION-EXPECTED-RESULT",
                    path,
                    "expected_result must be pass",
                )
            )
        elif not conformant:
            findings.append(
                _finding(
                    "HGR-REGRESSION-STATIC-CONFORMANCE",
                    path,
                    "resolved stack.yaml fails canonical DomainxFactory static "
                    "conformance",
                )
            )

        if _stack_is_conformant(_with_duplicate_customer(stack)):
            findings.append(
                _finding(
                    "HGR-REGRESSION-DERIVED-NEGATIVE",
                    path,
                    "the duplicate-Customer derived negative was not rejected by static "
                    "conformance",
                )
            )

    return _sorted(findings)
