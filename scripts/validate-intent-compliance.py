#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import override

import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.intent_compliance.authority_repository import (
    TrustedSnapshotError,
)
from scripts.intent_compliance.authority_validation import (
    TrustedSnapshot,
    validate_authoritative_submission,
)
from scripts.intent_compliance.discovery import (
    bounded_record_paths,
    discover_record_documents,
)
from scripts.intent_compliance.fixture_metadata import read_fixture_metadata
from scripts.intent_compliance.model import InputLimitError
from scripts.intent_compliance.negative_corpus import (
    negative_case_documents,
)
from scripts.intent_compliance.validator import (
    FAMILY_DIR,
    load_record_documents,
    validate_documents,
)

REQUIREMENTS = {
    "authority-bound-vocabulary",
    "closed-bounded-redacted-decisions",
    "immutable-allowance-and-revocation",
    "current-append-only-registry",
    "neutral-scope-outcomes",
    "deterministic-allowance-precedence",
    "binding-approval-current-compliance",
    "dispatch-floor-and-composition",
    "bounded-classifier-escalation",
    "identical-enforcement-bindings",
}


@dataclass(frozen=True, slots=True)
class CliArguments:
    target: Path | None
    strict: bool
    trusted_repository: Path | None
    trusted_repository_id: str | None
    trusted_commit: str | None


@dataclass(slots=True)
class CliUsageError(Exception):
    detail: str

    @override
    def __str__(self) -> str:
        return self.detail


def _arguments() -> CliArguments:
    parser = argparse.ArgumentParser(description="Validate intent-compliance contracts.")
    _ = parser.add_argument(
        "target", nargs="?", type=Path, help="consumer repository or record directory"
    )
    _ = parser.add_argument(
        "--strict", action="store_true", help="fail when no governed records are found"
    )
    _ = parser.add_argument(
        "--trusted-repository",
        type=Path,
        help="caller-trusted Git checkout containing authoritative records",
    )
    _ = parser.add_argument(
        "--trusted-repository-id",
        help="caller-trusted canonical owner/name repository identity",
    )
    _ = parser.add_argument(
        "--trusted-commit",
        help="full 40-hex commit selecting the authoritative Git tree",
    )
    arguments = parser.parse_args()
    target = arguments.target
    strict = arguments.strict
    trusted_repository = arguments.trusted_repository
    trusted_repository_id = arguments.trusted_repository_id
    trusted_commit = arguments.trusted_commit
    if target is not None and not isinstance(target, Path):
        raise CliUsageError("target must resolve to a path")
    if not isinstance(strict, bool):
        raise CliUsageError("strict must resolve to a boolean")
    if trusted_repository is not None and not isinstance(trusted_repository, Path):
        raise CliUsageError("trusted repository must resolve to a path")
    if trusted_repository_id is not None and not isinstance(trusted_repository_id, str):
        raise CliUsageError("trusted repository ID must resolve to text")
    if trusted_commit is not None and not isinstance(trusted_commit, str):
        raise CliUsageError("trusted commit must resolve to text")
    if target is not None and (
        trusted_repository is None
        or trusted_repository_id is None
        or trusted_commit is None
    ):
        raise CliUsageError(
            "target validation requires trusted repository, repository ID, and commit"
        )
    if target is None and (
        trusted_repository is not None
        or trusted_repository_id is not None
        or trusted_commit is not None
    ):
        raise CliUsageError("trusted repository, repository ID, and commit require a target")
    return CliArguments(
        target, strict, trusted_repository, trusted_repository_id, trusted_commit
    )


def _record_paths(target: Path) -> list[Path]:
    return bounded_record_paths(target)


def _self_test() -> list[str]:
    failures: list[str] = []
    positive = load_record_documents(sorted((FAMILY_DIR / "examples" / "positive").glob("*.yaml")))
    for finding in validate_documents(positive):
        failures.append(f"positive corpus: {finding.code}: {finding.message}")
    negative_paths = sorted((FAMILY_DIR / "examples" / "negative").glob("*.yaml"))
    covered_requirements: set[str] = set()
    for path in negative_paths:
        metadata = read_fixture_metadata(path)
        expected = metadata.expected_failure
        requirement = metadata.requirement
        if requirement not in REQUIREMENTS:
            failures.append(f"{path.name}: unknown requirement {requirement}")
        covered_requirements.add(requirement)
        codes = {
            finding.code
            for finding in validate_documents(
                negative_case_documents(path, positive, fixture_text=metadata.text)
            )
        }
        if expected not in codes:
            failures.append(f"{path.name}: expected {expected}; observed {sorted(codes)}")
    if not negative_paths:
        failures.append("negative corpus is empty")
    missing_requirements = sorted(REQUIREMENTS - covered_requirements)
    if missing_requirements:
        failures.append(f"requirements lack negative probes: {missing_requirements}")
    return failures


def main() -> int:
    try:
        arguments = _arguments()
        failures = _self_test()
        if arguments.target is not None and not failures:
            target = arguments.target.absolute()
            documents = discover_record_documents(_record_paths(target))
            decisions = [
                document
                for document in documents
                if document.data.get("kind") == "compliance_decision"
            ]
            if arguments.strict and not decisions:
                failures = ["no governed intent-compliance records found"]
            elif decisions:
                if (
                    arguments.trusted_repository is None
                    or arguments.trusted_repository_id is None
                    or arguments.trusted_commit is None
                ):
                    raise CliUsageError(
                        "target validation requires trusted repository, repository ID, and commit"
                    )
                snapshot = TrustedSnapshot(
                    arguments.trusted_repository.resolve(),
                    arguments.trusted_repository_id,
                    arguments.trusted_commit,
                )
                findings = validate_authoritative_submission(decisions, snapshot)
                failures = [f"{finding.source}: {finding.code}: {finding.message}" for finding in findings]
    except (
        OSError,
        CliUsageError,
        ValueError,
        InputLimitError,
        TrustedSnapshotError,
        yaml.YAMLError,
    ) as error:
        print(f"intent-compliance validator harness error: {error}", file=sys.stderr)
        return 2
    if failures:
        print("intent-compliance validation failed", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print("intent-compliance validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
