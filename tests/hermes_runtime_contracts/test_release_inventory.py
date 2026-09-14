"""Closed release digest inventory build and verification (T068 RED / T074 GREEN).

Covers deterministic candidate build, raw-Git-blob digest parity against a
hashlib oracle, exact-commit verification that ignores working-tree edits,
closed-membership negatives, symlink/submodule/traversal and host-path
rejection, pre-tag promotion-race negatives, annotated-tag verification, and CLI
subprocess exit codes.  Verification always reads exact Git objects and never
the working tree (research Decisions 10 and 11; requirement HGR-009).
"""

from __future__ import annotations

from collections.abc import Callable
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from scripts.hermes_runtime_validation import release
from scripts.hermes_runtime_validation.content import ContentResolutionError
from scripts.hermes_runtime_validation.fixtures import evaluate_expected_findings
from scripts.hermes_runtime_validation.loader import load_yaml_document
from tests.hermes_runtime_contracts import support

ROOT = Path(__file__).resolve().parents[2]
RELEASE_SCHEMA_PATH = ROOT / "contracts/releases/release-digest-inventory.schema.yaml"
FIXTURE_DIR = ROOT / "contracts/hermes-runtime/fixtures/release"
RELEASE_CLI = ROOT / "scripts/validate-contract-release.py"
NOW = "2026-07-13T12:00:00Z"
SYNTHETIC_TAG = "contract-v1.0"

CATALOG_YAML = """schema_version: 1
kind: openxfactory-hermes-runtime-contract-index
contracts:
- contract_id: contract-index
  path: contract-index.yaml
  type: contract-index
  release_member: true
- contract_id: example-record
  path: example-record.schema.yaml
  type: schema
  contract_schema_version: 2
  release_member: true
- contract_id: fixture-index
  path: fixtures/index.yaml
  type: fixture-index
  release_member: true
"""

FIXTURE_INDEX_YAML = """schema_version: 1
kind: openxfactory-hermes-runtime-fixture-index
fixture_root: contracts/hermes-runtime/fixtures
cases:
- case_id: example-case
  inputs:
  - example/one.yaml
"""

MANIFEST_YAML = "schema_version: 1\ncontract_bundle_version: contract-v1.0\n"
CHANGELOG_MD = "# changelog\n"
CONTRACTS_README_MD = "# contracts\n"
FAMILY_README_MD = "# hermes runtime family\n"
VERSIONING_DOC_MD = "# contract versioning policy\n"
REQUIREMENTS_IN = (
    "# hermes-runtime contract validation requirements\njsonschema\npyyaml\n"
)
REQUIREMENTS_LOCK = "# pinned by pip-compile\njsonschema==4.23.0\npyyaml==6.0.2\n"
IMAGES_LOCK_YAML = "schema_version: 1\nimages:\n- name: postgres\n  digest: sha256:0\n"
INVENTORY_SCHEMA_STUB = (
    "schema_version: 1\n"
    "kind: openxfactory-contract-release-digest-inventory-schema\n"
)

SYNTHETIC_TREE: dict[str, str] = {
    "contracts/hermes-runtime/contract-index.yaml": CATALOG_YAML,
    "contracts/hermes-runtime/example-record.schema.yaml": "schema_version: 1\nkind: example\n",
    "contracts/hermes-runtime/fixtures/index.yaml": FIXTURE_INDEX_YAML,
    "contracts/hermes-runtime/fixtures/example/one.yaml": "case_id: example-case\n",
    "contracts/hermes-runtime/README.md": FAMILY_README_MD,
    "contracts/manifest.yaml": MANIFEST_YAML,
    "contracts/CHANGELOG.md": CHANGELOG_MD,
    "contracts/README.md": CONTRACTS_README_MD,
    "docs/contract-versioning-policy.md": VERSIONING_DOC_MD,
    # Decision-10 mandatory auxiliaries: now unconditional release members, so
    # every synthetic tree must supply them or the closed-bundle build fails
    # closed with a read_member dependency error (see F-U3).
    "requirements/hermes-runtime-contracts.in": REQUIREMENTS_IN,
    "requirements/hermes-runtime-contracts.lock": REQUIREMENTS_LOCK,
    "tests/hermes_runtime_contracts/postgres/images.lock.yaml": IMAGES_LOCK_YAML,
    "contracts/releases/release-digest-inventory.schema.yaml": INVENTORY_SCHEMA_STUB,
}


def _git(repo: Path, *arguments: str) -> str:
    return support.run_command(["git", *arguments], cwd=repo, check=True).stdout.strip()


def _commit_all(repo: Path, message: str) -> str:
    _git(repo, "add", "-A")
    _git(repo, "commit", "--quiet", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


def _write_tree(repo: Path, tree: dict[str, str]) -> None:
    for relative, content in tree.items():
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def _synthetic_repo(tmp_path: Path, name: str = "repo") -> tuple[Path, str]:
    repo = support.init_git_repo(tmp_path / name)
    _git(repo, "symbolic-ref", "HEAD", "refs/heads/main")
    _write_tree(repo, SYNTHETIC_TREE)
    commit = _commit_all(repo, "synthetic release candidate")
    return repo, commit


def _canonical_inventory(repo: Path) -> dict:
    return release.build_release_inventory(repo, bundle_tag=SYNTHETIC_TAG)


def _bare_origin(tmp_path: Path, name: str = "origin.git") -> Path:
    origin = tmp_path / name
    origin.mkdir()
    _git(origin, "init", "--bare", "--quiet")
    return origin


def _write_url_redirect_config(path: Path, source: Path, target: Path) -> None:
    path.write_text(
        f'[url "{target.as_uri()}"]\n\tinsteadOf = {source}\n', encoding="utf-8"
    )


# --- deterministic inventory mutations shared with the fixture generator ------


def mutation_none(inventory: dict) -> dict:
    return copy.deepcopy(inventory)


def mutation_drop_member(inventory: dict) -> dict:
    mutated = copy.deepcopy(inventory)
    mutated["entries"].pop(0)
    return mutated


def mutation_duplicate_adjacent(inventory: dict) -> dict:
    mutated = copy.deepcopy(inventory)
    mutated["entries"].insert(1, copy.deepcopy(mutated["entries"][0]))
    return mutated


def mutation_out_of_order(inventory: dict) -> dict:
    mutated = copy.deepcopy(inventory)
    mutated["entries"] = list(reversed(mutated["entries"]))
    return mutated


def mutation_wrong_digest(inventory: dict) -> dict:
    mutated = copy.deepcopy(inventory)
    mutated["entries"][0]["digest"] = "sha256:" + "0" * 64
    return mutated


def mutation_host_absolute_path(inventory: dict) -> dict:
    mutated = copy.deepcopy(inventory)
    mutated["entries"][0]["path"] = "/etc/passwd"
    return mutated


FIXTURE_CASES = {
    "release-inventory-valid": {
        "mutation": mutation_none,
        "phase": "semantic",
        "class": "valid",
        "operation": "verify_inventory_against_commit",
        "scenario_ids": ["HGR-009-S01"],
        "expected": {"outcome": "pass", "allowed_secondary_codes": []},
    },
    "release-inventory-missing-member": {
        "mutation": mutation_drop_member,
        "phase": "semantic",
        "class": "invalid",
        "operation": "verify_inventory_against_commit",
        "scenario_ids": ["HGR-009-S04"],
        "expected": {
            "outcome": "fail",
            "primary_finding_code": "HGR-RELEASE-MEMBER-MISSING",
            "allowed_secondary_codes": [],
        },
    },
    "release-inventory-duplicate-path": {
        "mutation": mutation_duplicate_adjacent,
        "phase": "semantic",
        "class": "invalid",
        "operation": "verify_inventory_against_commit",
        "scenario_ids": ["HGR-009-S04"],
        "expected": {
            "outcome": "fail",
            "primary_finding_code": "HGR-RELEASE-PATH-DUPLICATE",
            "allowed_secondary_codes": [],
        },
    },
    "release-inventory-out-of-order": {
        "mutation": mutation_out_of_order,
        "phase": "semantic",
        "class": "invalid",
        "operation": "verify_inventory_against_commit",
        "scenario_ids": ["HGR-009-S04"],
        "expected": {
            "outcome": "fail",
            "primary_finding_code": "HGR-RELEASE-PATH-ORDER",
            "allowed_secondary_codes": [],
        },
    },
    "release-inventory-wrong-digest": {
        "mutation": mutation_wrong_digest,
        "phase": "semantic",
        "class": "invalid",
        "operation": "verify_inventory_against_commit",
        "scenario_ids": ["HGR-009-S04"],
        "expected": {
            "outcome": "fail",
            "primary_finding_code": "HGR-RELEASE-DIGEST-MISMATCH",
            "allowed_secondary_codes": [],
        },
    },
    "release-inventory-host-absolute-path": {
        "mutation": mutation_host_absolute_path,
        "phase": "structural",
        "class": "invalid",
        "operation": "validate_inventory_schema",
        "scenario_ids": ["HGR-009-S03"],
        "expected": {
            "outcome": "fail",
            "primary_finding_code": "HGR-RELEASE-INVENTORY-SHAPE",
            "allowed_secondary_codes": [],
        },
    },
}


def fixture_document(case_id: str, inventory: dict) -> dict:
    case = FIXTURE_CASES[case_id]
    document = {
        "schema_version": 1,
        "kind": "openxfactory-hermes-runtime-portable-evidence-fixture",
        "case_id": case_id,
        "phase": case["phase"],
        "class": case["class"],
        "requirement_ids": ["HGR-009"],
        "scenario_ids": list(case["scenario_ids"]),
        "evaluation_time": NOW,
        "operation": case["operation"],
        "inventory": case["mutation"](inventory),
        "expected": dict(case["expected"]),
    }
    return document


# --- schema -------------------------------------------------------------------


def _schema() -> dict:
    return load_yaml_document(RELEASE_SCHEMA_PATH)


def _validator() -> Draft202012Validator:
    schema = _schema()
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def test_release_schema_is_self_contained_and_valid() -> None:
    schema = _schema()
    Draft202012Validator.check_schema(schema)
    assert schema["kind"] == "openxfactory-contract-release-digest-inventory-schema"
    assert schema["$id"] == (
        "https://xforge.us/schemas/openxfactory/releases/"
        "release-digest-inventory.schema.yaml"
    )
    text = RELEASE_SCHEMA_PATH.read_text(encoding="utf-8")
    assert "shared-definitions" not in text
    for line in text.splitlines():
        if "$ref" in line:
            reference = line.split("$ref", 1)[1]
            assert reference.lstrip(": \"'").startswith("#/"), line


def test_schema_accepts_canonical_instance_and_rejects_malformations(
    tmp_path: Path,
) -> None:
    validator = _validator()
    repo, _ = _synthetic_repo(tmp_path)
    inventory = _canonical_inventory(repo)
    assert list(validator.iter_errors(inventory)) == []

    host_absolute = mutation_host_absolute_path(inventory)
    assert list(validator.iter_errors(host_absolute))

    traversal = copy.deepcopy(inventory)
    traversal["entries"][0]["path"] = "contracts/../secret.yaml"
    assert list(validator.iter_errors(traversal))

    backslash = copy.deepcopy(inventory)
    backslash["entries"][0]["path"] = "contracts\\windows.yaml"
    assert list(validator.iter_errors(backslash))

    self_member = copy.deepcopy(inventory)
    self_member["entries"][0]["path"] = "contracts/releases/contract-v1.0.digests.yaml"
    # A digests path is a structurally-valid repository path; the verifier, not
    # the schema, rejects it, so the schema still accepts this shape.
    assert list(validator.iter_errors(self_member)) == []

    with_commit = copy.deepcopy(inventory)
    with_commit["commit"] = "0" * 40
    assert list(validator.iter_errors(with_commit))

    bad_mode = copy.deepcopy(inventory)
    bad_mode["entries"][0]["git_mode"] = "120000"
    assert list(validator.iter_errors(bad_mode))

    lonely_schema_pin = copy.deepcopy(inventory)
    lonely_schema_pin["entries"][0]["schema_id"] = "example"
    lonely_schema_pin["entries"][0].pop("schema_version", None)
    assert list(validator.iter_errors(lonely_schema_pin))

    bad_digest = copy.deepcopy(inventory)
    bad_digest["entries"][0]["digest"] = "sha1:" + "a" * 40
    assert list(validator.iter_errors(bad_digest))

    bad_repository = copy.deepcopy(inventory)
    bad_repository["repository"] = "opensoft/impostor"
    assert list(validator.iter_errors(bad_repository))


# --- build --------------------------------------------------------------------


def test_build_is_deterministic_and_excludes_itself(tmp_path: Path) -> None:
    repo, _ = _synthetic_repo(tmp_path)
    first = _canonical_inventory(repo)
    second = _canonical_inventory(repo)
    assert first == second
    assert release.dump_inventory(first) == release.dump_inventory(second)
    assert first["kind"] == "openxfactory-contract-release-digest-inventory"
    assert first["repository"] == "opensoft/openxFactory"
    assert first["digest_source"] == "raw_git_blob"
    assert "commit" not in first
    paths = [entry["path"] for entry in first["entries"]]
    assert paths == sorted(paths, key=lambda value: value.encode("utf-8"))
    assert not any(
        path.startswith("contracts/releases/") and path.endswith(".digests.yaml")
        for path in paths
    )


def test_build_digests_match_the_raw_git_blob_oracle(tmp_path: Path) -> None:
    repo, commit = _synthetic_repo(tmp_path)
    inventory = _canonical_inventory(repo)
    for entry in inventory["entries"]:
        blob = subprocess.run(
            ["git", "-C", str(repo), "cat-file", "blob", f"{commit}:{entry['path']}"],
            capture_output=True,
            check=True,
        ).stdout
        assert entry["digest"] == "sha256:" + hashlib.sha256(blob).hexdigest()


def test_release_membership_is_the_closed_candidate_set(tmp_path: Path) -> None:
    repo, _ = _synthetic_repo(tmp_path)
    members = {path.as_posix() for path in release.release_membership(repo)}
    assert members == {
        "contracts/hermes-runtime/contract-index.yaml",
        "contracts/hermes-runtime/example-record.schema.yaml",
        "contracts/hermes-runtime/fixtures/example/one.yaml",
        "contracts/hermes-runtime/fixtures/index.yaml",
        "contracts/manifest.yaml",
        "contracts/CHANGELOG.md",
        "contracts/README.md",
        "docs/contract-versioning-policy.md",
        # Decision-10 mandatory auxiliaries are unconditional members (F-U3).
        "requirements/hermes-runtime-contracts.in",
        "requirements/hermes-runtime-contracts.lock",
        "tests/hermes_runtime_contracts/postgres/images.lock.yaml",
        "contracts/releases/release-digest-inventory.schema.yaml",
    }
    # The family README exists on disk but is not a catalog release member, so
    # membership excludes unregistered files.
    assert "contracts/hermes-runtime/README.md" not in members


def test_missing_mandatory_auxiliary_fails_closed_not_silently_shrunk(
    tmp_path: Path,
) -> None:
    # F-U3: Decision-10 mandatory auxiliaries are unconditional members. When one
    # is absent at the pinned commit the build/verify must fail closed rather than
    # silently omitting it and verifying a smaller inventory clean.
    repo, _ = _synthetic_repo(tmp_path)
    baseline = _canonical_inventory(repo)
    baseline_paths = {entry["path"] for entry in baseline["entries"]}
    assert "requirements/hermes-runtime-contracts.lock" in baseline_paths

    # Remove a mandatory auxiliary from the working tree and commit its deletion.
    (repo / "requirements/hermes-runtime-contracts.lock").unlink()
    dropped_commit = _commit_all(repo, "drop mandatory auxiliary")

    # Membership no longer shrinks: the lock is still a mandated member even
    # though it is absent (the old exists()-gated build would have dropped it).
    members_after = {path.as_posix() for path in release.release_membership(repo)}
    assert "requirements/hermes-runtime-contracts.lock" in members_after

    # The working-tree candidate build fails closed on the unreadable member.
    with pytest.raises(ContentResolutionError):
        release.build_release_inventory(repo, bundle_tag=SYNTHETIC_TAG)

    # The exact-commit canonical build behind verification also fails closed
    # instead of producing a smaller inventory that verifies clean.
    with pytest.raises(ContentResolutionError):
        release.verify_inventory_against_commit(repo, dropped_commit, baseline)


def test_semantic_member_must_be_a_release_member(tmp_path: Path) -> None:
    # F-U3 invariant: every catalog semantic_member must also be a release_member.
    repo, _ = _synthetic_repo(tmp_path)
    # The all-consistent synthetic catalog does not trip the invariant.
    assert release.release_membership(repo)

    orphan_catalog = CATALOG_YAML + (
        "- contract_id: orphan-semantic\n"
        "  path: orphan-semantic.schema.yaml\n"
        "  type: schema\n"
        "  contract_schema_version: 1\n"
        "  semantic_member: true\n"
        "  release_member: false\n"
    )
    (repo / "contracts/hermes-runtime/contract-index.yaml").write_text(
        orphan_catalog, encoding="utf-8"
    )
    with pytest.raises(release.ReleaseDependencyError) as excinfo:
        release.release_membership(repo)
    assert "orphan-semantic" in str(excinfo.value)
    assert excinfo.value.code == "HGR-RELEASE-SEMANTIC-NOT-RELEASED"


# --- exact-commit verification ------------------------------------------------


def test_verify_passes_and_ignores_working_tree_edits(tmp_path: Path) -> None:
    repo, commit = _synthetic_repo(tmp_path)
    inventory = _canonical_inventory(repo)
    assert release.verify_inventory_against_commit(repo, commit, inventory) == []

    (repo / "contracts/manifest.yaml").write_text("TAMPERED\n", encoding="utf-8")
    (repo / "contracts/hermes-runtime/example-record.schema.yaml").write_text(
        "kind: tampered\n", encoding="utf-8"
    )
    assert release.verify_inventory_against_commit(repo, commit, inventory) == []


def _codes(findings: list[dict]) -> list[str]:
    return sorted(finding["code"] for finding in findings)


def test_verify_detects_missing_extra_duplicate_and_unordered(tmp_path: Path) -> None:
    repo, commit = _synthetic_repo(tmp_path)
    inventory = _canonical_inventory(repo)

    assert _codes(
        release.verify_inventory_against_commit(
            repo, commit, mutation_drop_member(inventory)
        )
    ) == ["HGR-RELEASE-MEMBER-MISSING"]
    assert _codes(
        release.verify_inventory_against_commit(
            repo, commit, mutation_duplicate_adjacent(inventory)
        )
    ) == ["HGR-RELEASE-PATH-DUPLICATE"]
    assert _codes(
        release.verify_inventory_against_commit(
            repo, commit, mutation_out_of_order(inventory)
        )
    ) == ["HGR-RELEASE-PATH-ORDER"]
    assert _codes(
        release.verify_inventory_against_commit(
            repo, commit, mutation_wrong_digest(inventory)
        )
    ) == ["HGR-RELEASE-DIGEST-MISMATCH"]

    (repo / "contracts/hermes-runtime/extra.txt").write_text("x\n", encoding="utf-8")
    extra_commit = _commit_all(repo, "add non-member file")
    extra = _canonical_inventory(repo)
    _, mode, digest = release._CommitSource(repo, extra_commit).read_member(
        "contracts/hermes-runtime/extra.txt"
    )
    extra["entries"].append(
        {
            "artifact_id": "extra",
            "path": "contracts/hermes-runtime/extra.txt",
            "type": "documentation",
            "git_mode": mode,
            "digest": digest,
        }
    )
    extra["entries"].sort(key=lambda entry: entry["path"].encode("utf-8"))
    assert _codes(
        release.verify_inventory_against_commit(repo, extra_commit, extra)
    ) == ["HGR-RELEASE-MEMBER-EXTRA"]


def test_verify_rejects_type_and_schema_pin_drift(tmp_path: Path) -> None:
    repo, commit = _synthetic_repo(tmp_path)
    inventory = _canonical_inventory(repo)
    schema_entry = next(
        entry for entry in inventory["entries"] if entry["type"] == "schema"
    )
    wrong_version = copy.deepcopy(inventory)
    for entry in wrong_version["entries"]:
        if entry["path"] == schema_entry["path"]:
            entry["schema_version"] = 99
    assert "HGR-RELEASE-SCHEMA-PIN-MISMATCH" in _codes(
        release.verify_inventory_against_commit(repo, commit, wrong_version)
    )
    wrong_type = copy.deepcopy(inventory)
    wrong_type["entries"][0]["type"] = "sql"
    assert "HGR-RELEASE-TYPE-MISMATCH" in _codes(
        release.verify_inventory_against_commit(repo, commit, wrong_type)
    )


def test_catalog_pin_findings_cover_release_only_schemas() -> None:
    # Pins the working-tree gate directly: narrowing _catalog_pin_findings
    # back to `type == "schema"` (dropping release-schema members) must fail
    # here even though every other suite path goes through
    # verify_inventory_against_commit.
    catalog = {
        "contracts": [
            {
                "contract_id": "wire-only",
                "type": "release-schema",
                "release_member": True,
                "contract_schema_version": 1,
            }
        ]
    }
    matching = {
        "entries": [
            {"type": "release-schema", "schema_id": "wire-only", "schema_version": 1}
        ]
    }
    assert release._catalog_pin_findings(catalog, matching) == []
    for tampered_entries in (
        [{"type": "release-schema", "schema_id": "wire-only", "schema_version": 2}],
        [],
    ):
        findings = release._catalog_pin_findings(
            catalog, {"entries": tampered_entries}
        )
        assert [f["code"] for f in findings] == ["HGR-RELEASE-SCHEMA-PIN-MISMATCH"]


def test_missing_catalog_schema_pin_is_a_clean_dependency_error() -> None:
    entry = {
        "contract_id": "wire-only",
        "type": "release-schema",
        "release_member": True,
    }
    with pytest.raises(release.ReleaseDependencyError):
        release._require_schema_pin(entry)
    with pytest.raises(release.ReleaseDependencyError):
        release._catalog_pin_findings({"contracts": [entry]}, {"entries": []})


def test_verify_rejects_symlink_submodule_and_traversal(tmp_path: Path) -> None:
    repo, _ = _synthetic_repo(tmp_path)
    os.symlink(
        "contracts/manifest.yaml",
        repo / "contracts/hermes-runtime/link.schema.yaml",
    )
    symlink_commit = _commit_all(repo, "add symlink")
    inventory = _canonical_inventory(repo)
    inventory["entries"].append(
        {
            "artifact_id": "link",
            "path": "contracts/hermes-runtime/link.schema.yaml",
            "type": "schema",
            "schema_id": "link",
            "schema_version": 1,
            "digest": "sha256:" + "0" * 64,
        }
    )
    inventory["entries"].sort(key=lambda entry: entry["path"].encode("utf-8"))
    assert "HGR-RELEASE-PATH-UNRESOLVABLE" in _codes(
        release.verify_inventory_against_commit(repo, symlink_commit, inventory)
    )

    child = support.init_git_repo(tmp_path / "child")
    child_commit = support.commit_files(child, {"README.md": "child\n"})
    _git(
        repo,
        "update-index",
        "--add",
        "--cacheinfo",
        f"160000,{child_commit},contracts/hermes-runtime/vendor",
    )
    # Commit the staged gitlink directly; ``git add -A`` would restage it as a
    # deletion because the submodule path has no working-tree entry.
    _git(repo, "commit", "--quiet", "-m", "add gitlink")
    gitlink_commit = _git(repo, "rev-parse", "HEAD")
    gitlink = _canonical_inventory(repo)
    gitlink["entries"].append(
        {
            "artifact_id": "vendor",
            "path": "contracts/hermes-runtime/vendor",
            "type": "documentation",
            "digest": "sha256:" + "0" * 64,
        }
    )
    gitlink["entries"].sort(key=lambda entry: entry["path"].encode("utf-8"))
    assert "HGR-RELEASE-PATH-UNRESOLVABLE" in _codes(
        release.verify_inventory_against_commit(repo, gitlink_commit, gitlink)
    )


def test_verify_rejects_self_reference_and_recorded_commit(tmp_path: Path) -> None:
    repo, commit = _synthetic_repo(tmp_path)
    inventory = _canonical_inventory(repo)
    inventory["commit"] = commit
    inventory["entries"].append(
        {
            "artifact_id": "self",
            "path": "contracts/releases/contract-v1.0.digests.yaml",
            "type": "documentation",
            "digest": "sha256:" + "0" * 64,
        }
    )
    inventory["entries"].sort(key=lambda entry: entry["path"].encode("utf-8"))
    codes = _codes(release.verify_inventory_against_commit(repo, commit, inventory))
    assert codes.count("HGR-RELEASE-SELF-REFERENCE") == 2


def test_verify_reads_exact_commit_not_a_short_or_symbolic_revision(
    tmp_path: Path,
) -> None:
    repo, commit = _synthetic_repo(tmp_path)
    inventory = _canonical_inventory(repo)
    (repo / "contracts/manifest.yaml").write_text("drift\n", encoding="utf-8")
    _commit_all(repo, "advance HEAD past the reviewed candidate")
    # The reviewed candidate commit still verifies even though HEAD moved on.
    assert release.verify_inventory_against_commit(repo, commit, inventory) == []


def test_verify_uses_the_requested_repository_under_a_hostile_common_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    primary, commit = _synthetic_repo(tmp_path, "primary")
    repo = tmp_path / "requested"
    _git(primary, "worktree", "add", "--quiet", "-b", "requested", str(repo), commit)
    inventory = _canonical_inventory(repo)
    hostile = support.init_git_repo(tmp_path / "hostile")
    support.commit_files(hostile, {"hostile.txt": "unrelated repository\n"})
    monkeypatch.setenv("GIT_COMMON_DIR", str(hostile / ".git"))

    assert release.verify_inventory_against_commit(repo, commit, inventory) == []


# --- promotion ----------------------------------------------------------------


def _repo_with_committed_inventory(
    tmp_path: Path,
    name: str,
    tag: str,
    *,
    hazard: Callable[[Path], None] | None = None,
) -> tuple[Path, str]:
    repo = support.init_git_repo(tmp_path / name)
    _git(repo, "symbolic-ref", "HEAD", "refs/heads/main")
    tree = dict(SYNTHETIC_TREE)
    tree["contracts/manifest.yaml"] = (
        f"schema_version: 1\ncontract_bundle_version: {tag}\n"
    )
    _write_tree(repo, tree)
    inventory = release.build_release_inventory(repo, bundle_tag=tag)
    (repo / f"contracts/releases/{tag}.digests.yaml").parent.mkdir(
        parents=True, exist_ok=True
    )
    (repo / f"contracts/releases/{tag}.digests.yaml").write_text(
        release.dump_inventory(inventory), encoding="utf-8"
    )
    # A `hazard` runs AFTER the inventory is built, so the committed inventory
    # stays the one the ordinary fixture produces and only the release SURFACE
    # carries the condition under test (fix-content-resolution-conflation).
    if hazard is not None:
        hazard(repo)
    commit = _commit_all(repo, "release candidate with inventory")
    return repo, commit


def test_verify_promotion_accepts_a_reviewed_reachable_candidate(
    tmp_path: Path,
) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _bare_origin(tmp_path)
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    assert release.verify_promotion(repo, commit=commit, remote="origin", tag=tag) == []


def test_verify_promotion_uses_repo_origin_despite_indexed_config_override(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _bare_origin(tmp_path, "origin.git")
    hostile = _bare_origin(tmp_path, "hostile.git")
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
    monkeypatch.setenv("GIT_CONFIG_KEY_0", f"url.{hostile.as_uri()}.insteadOf")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", str(origin))

    assert release.verify_promotion(repo, commit=commit, remote="origin", tag=tag) == []


def test_verify_promotion_ignores_hostile_global_and_system_url_redirects(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _bare_origin(tmp_path, "origin.git")
    hostile = _bare_origin(tmp_path, "hostile.git")
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    global_config = tmp_path / "hostile-global.gitconfig"
    system_config = tmp_path / "hostile-system.gitconfig"
    _write_url_redirect_config(global_config, origin, hostile)
    _write_url_redirect_config(system_config, origin, hostile)
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(global_config))
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", str(system_config))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "0")

    assert release.verify_promotion(repo, commit=commit, remote="origin", tag=tag) == []


def test_verify_promotion_preserves_repository_local_url_rewrite(
    tmp_path: Path,
) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _bare_origin(tmp_path, "origin.git")
    local_alias = "local-release-origin:"
    _git(repo, "config", f"url.{origin.as_uri()}.insteadOf", local_alias)
    _git(repo, "remote", "add", "origin", local_alias)
    _git(repo, "push", "--quiet", "origin", "main")

    assert release.verify_promotion(repo, commit=commit, remote="origin", tag=tag) == []


def test_verify_promotion_rejects_an_already_published_tag(tmp_path: Path) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _bare_origin(tmp_path)
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    _git(repo, "tag", tag, commit)
    _git(repo, "push", "--quiet", "origin", tag)
    assert "HGR-RELEASE-TAG-EXISTS" in _codes(
        release.verify_promotion(repo, commit=commit, remote="origin", tag=tag)
    )


def test_verify_promotion_rejects_a_candidate_absent_from_remote_main(
    tmp_path: Path,
) -> None:
    tag = "contract-v2.0"
    repo, base = _repo_with_committed_inventory(tmp_path, "repo", tag)
    (repo / "contracts/hermes-runtime/fixtures/example/two.yaml").write_text(
        "case_id: extra\n", encoding="utf-8"
    )
    candidate = _commit_all(repo, "descendant candidate")
    origin = _bare_origin(tmp_path)
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", f"{base}:refs/heads/main")
    assert "HGR-RELEASE-CANDIDATE-UNREACHABLE" in _codes(
        release.verify_promotion(repo, commit=candidate, remote="origin", tag=tag)
    )


def test_verify_promotion_rejects_a_drifted_release_surface(tmp_path: Path) -> None:
    tag = "contract-v2.0"
    repo, candidate = _repo_with_committed_inventory(tmp_path, "repo", tag)
    (repo / "contracts/manifest.yaml").write_text(
        f"schema_version: 1\ncontract_bundle_version: {tag}\nextra: drift\n",
        encoding="utf-8",
    )
    _commit_all(repo, "post-review surface drift")
    origin = _bare_origin(tmp_path)
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    assert "HGR-RELEASE-SURFACE-DRIFT" in _codes(
        release.verify_promotion(repo, commit=candidate, remote="origin", tag=tag)
    )


# --- annotated tag verification -----------------------------------------------


def test_verify_tag_accepts_an_annotated_reachable_tag(tmp_path: Path) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _bare_origin(tmp_path)
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    _git(repo, "tag", "-a", tag, "-m", "release", commit)
    _git(repo, "push", "--quiet", "origin", tag)
    assert release.verify_tag(repo, remote="origin", tag=tag) == []


def test_verify_tag_uses_repo_origin_despite_config_parameters_override(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _bare_origin(tmp_path, "origin.git")
    hostile = _bare_origin(tmp_path, "hostile.git")
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    _git(repo, "tag", "-a", tag, "-m", "release", commit)
    _git(repo, "push", "--quiet", "origin", tag)
    monkeypatch.setenv(
        "GIT_CONFIG_PARAMETERS",
        f"'url.{hostile.as_uri()}.insteadOf={origin}'",
    )

    assert release.verify_tag(repo, remote="origin", tag=tag) == []


def test_verify_tag_ignores_hostile_global_and_system_url_redirects(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _bare_origin(tmp_path, "origin.git")
    hostile = _bare_origin(tmp_path, "hostile.git")
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    _git(repo, "tag", "-a", tag, "-m", "release", commit)
    _git(repo, "push", "--quiet", "origin", tag)
    global_config = tmp_path / "hostile-global.gitconfig"
    system_config = tmp_path / "hostile-system.gitconfig"
    _write_url_redirect_config(global_config, origin, hostile)
    _write_url_redirect_config(system_config, origin, hostile)
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(global_config))
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", str(system_config))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "0")

    assert release.verify_tag(repo, remote="origin", tag=tag) == []


def test_verify_tag_rejects_a_lightweight_tag(tmp_path: Path) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _bare_origin(tmp_path)
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    _git(repo, "tag", tag, commit)
    _git(repo, "push", "--quiet", "origin", tag)
    assert "HGR-RELEASE-TAG-NOT-ANNOTATED" in _codes(
        release.verify_tag(repo, remote="origin", tag=tag)
    )


def test_verify_tag_rejects_a_tag_off_published_main(tmp_path: Path) -> None:
    tag = "contract-v2.0"
    repo, main_commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    _git(repo, "checkout", "--quiet", "-b", "side")
    (repo / "sidefile.txt").write_text("side\n", encoding="utf-8")
    side_commit = _commit_all(repo, "off-main commit")
    _git(repo, "checkout", "--quiet", "main")
    origin = _bare_origin(tmp_path)
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    _git(repo, "tag", "-a", tag, "-m", "release", side_commit)
    _git(repo, "push", "--quiet", "origin", tag)
    assert "HGR-RELEASE-TAG-UNREACHABLE" in _codes(
        release.verify_tag(repo, remote="origin", tag=tag)
    )


def test_verify_tag_reports_a_missing_remote_tag(tmp_path: Path) -> None:
    tag = "contract-v2.0"
    repo, _ = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _bare_origin(tmp_path)
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    assert _codes(release.verify_tag(repo, remote="origin", tag=tag)) == [
        "HGR-RELEASE-TAG-MISSING"
    ]


# --- remote-derived operands: mid-run skew and unservable objects --------------
#
# Online release verification reads `refs/heads/main` and the tag advertisement
# from the canonical remote, then answers questions about those object ids
# inside the local clone. The clone is fixed at the moment it was taken; the
# remote's refs are not. These fixtures DRIVE that divergence rather than
# describing it: a second clone advances the bare origin's `main` so the
# verifying repository genuinely does not hold the object the remote
# advertises.


def _is_ancestor_on_the_real_history(repo: Path, ancestor: str, descendant: str) -> bool:
    """Ask a repository that holds the whole history, for use as a fixture oracle."""
    probe = support.run_command(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=repo
    )
    assert probe.returncode in (0, 1), probe.stderr
    return probe.returncode == 0


def _object_is_absent(repo: Path, object_id: str) -> bool:
    """True when the local object store cannot resolve the object id."""
    probe = support.run_command(
        ["git", "cat-file", "-e", f"{object_id}^{{object}}"], cwd=repo
    )
    return probe.returncode != 0


def test_remote_object_probe_rejects_an_alternate_only_object(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo, _ = _synthetic_repo(tmp_path, "repo")
    origin = _bare_origin(tmp_path, "origin.git")
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    alternate, _ = _synthetic_repo(tmp_path, "alternate")
    (alternate / "alternate-only.txt").write_text(
        "alternate object\n", encoding="utf-8"
    )
    alternate_commit = _commit_all(alternate, "alternate-only object")
    assert _object_is_absent(repo, alternate_commit)
    monkeypatch.setenv(
        "GIT_ALTERNATE_OBJECT_DIRECTORIES", str(alternate / ".git" / "objects")
    )

    with pytest.raises(release.ReleaseDependencyError) as excinfo:
        release._resolve_remote_object(repo, "origin", alternate_commit)

    assert "fetch" in str(excinfo.value)


def _advance_remote_main_from_a_peer_clone(
    tmp_path: Path,
    origin: Path,
    *,
    relative: str,
    content: str,
    message: str = "another change merged inside the window",
) -> str:
    """Advance the bare origin's `main` from a SECOND clone and return the oid.

    The verifying repository never sees this commit, which is exactly the
    condition continuous integration meets whenever another pull request
    merges inside a suite's eleven-minute window.
    """
    peer = tmp_path / "peer"
    _git(tmp_path, "clone", "--quiet", "--branch", "main", str(origin), str(peer))
    _git(peer, "config", "user.name", "Hermes Contract Tests")
    _git(peer, "config", "user.email", "hermes-tests@example.invalid")
    _git(peer, "config", "commit.gpgsign", "false")
    target = peer / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    advanced = _commit_all(peer, message)
    _git(peer, "push", "--quiet", "origin", "HEAD:refs/heads/main")
    return advanced


def _skewed_candidate(
    tmp_path: Path, tag: str, *, relative: str, content: str
) -> tuple[Path, str, str]:
    """Build a candidate repository whose remote `main` has moved beyond it."""
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _bare_origin(tmp_path)
    # Keep pushed objects loose so a single object file can be made unreadable.
    _git(origin, "config", "receive.unpackLimit", "10000")
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    advanced = _advance_remote_main_from_a_peer_clone(
        tmp_path, origin, relative=relative, content=content
    )
    # The condition is real, not asserted into being.
    assert release._ls_remote(repo, "origin", "refs/heads/main")[0][0] == advanced
    assert _object_is_absent(repo, advanced)
    return repo, commit, advanced


def test_verify_promotion_completes_when_remote_main_advanced_past_the_clone(
    tmp_path: Path,
) -> None:
    """THE SKEW REGRESSION. `_ls_remote` names the remote's CURRENT `main`;
    `git merge-base --is-ancestor` runs inside a clone taken earlier. Before
    the operand was resolved on entry, `merge-base` exited 128 on the absent
    object and the verifier raised "commit reachability could not be
    determined" -- a fail-closed refusal produced by somebody else's merge
    rather than by anything about this candidate (openxFactory PR #372, run
    32934803039: one tree, two failures, one pass, decided by what landed
    during the suite).
    """
    tag = "contract-v2.0"
    repo, commit, _ = _skewed_candidate(
        tmp_path, tag, relative="unrelated.txt", content="another change\n"
    )
    # The same verdict a current clone returns -- see
    # test_verify_promotion_accepts_a_reviewed_reachable_candidate.
    assert release.verify_promotion(repo, commit=commit, remote="origin", tag=tag) == []


def test_verify_tag_completes_when_the_tag_and_main_are_newer_than_the_clone(
    tmp_path: Path,
) -> None:
    """Both of `verify_tag`'s remote-derived operands absent at once: the
    commit the published tag peels to AND the remote's `main` tip. A tag
    published since the clone was taken is missing for the same reason main's
    new tip is, and `_verify_release_at` reads that commit's tree and blobs
    locally after the ancestor check.
    """
    tag = "contract-v2.0"
    repo, _ = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _bare_origin(tmp_path)
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")

    peer = tmp_path / "peer"
    _git(tmp_path, "clone", "--quiet", "--branch", "main", str(origin), str(peer))
    _git(peer, "config", "user.name", "Hermes Contract Tests")
    _git(peer, "config", "user.email", "hermes-tests@example.invalid")
    _git(peer, "config", "commit.gpgsign", "false")
    (peer / "unrelated.txt").write_text("another change\n", encoding="utf-8")
    advanced = _commit_all(peer, "another change merged inside the window")
    _git(peer, "tag", "-a", tag, "-m", "release", advanced)
    _git(peer, "push", "--quiet", "origin", "HEAD:refs/heads/main")
    _git(peer, "push", "--quiet", "origin", tag)

    assert _object_is_absent(repo, advanced)
    assert release.verify_tag(repo, remote="origin", tag=tag) == []


def test_surface_drift_is_computed_against_a_resolved_advanced_main(
    tmp_path: Path,
) -> None:
    """THE MASKED SECOND SITE. `_surface_drift` reads the same remote-derived
    `main_oid` twice -- `_CommitSource(...).list_release_inventories()` (a
    `git ls-tree` that raises "Git command failed" on an absent commit) and
    `_blob_object_id(...)` (which swallows `ContentResolutionError` and
    returns `None`, so an absent commit would compare every real blob against
    nothing and emit a FALSE drift finding on every release-surface path).
    Both are masked today by the ancestor check raising first, which is why
    this test asserts the drift verdict the surface actually warrants: ONE
    finding, on the one path that moved.
    """
    tag = "contract-v2.0"
    repo, commit, _ = _skewed_candidate(
        tmp_path,
        tag,
        relative="contracts/manifest.yaml",
        content=f"schema_version: 1\ncontract_bundle_version: {tag}\nextra: drift\n",
    )
    findings = release.verify_promotion(repo, commit=commit, remote="origin", tag=tag)
    assert [(finding["code"], finding["path"]) for finding in findings] == [
        ("HGR-RELEASE-SURFACE-DRIFT", "contracts/manifest.yaml")
    ]


def _revoke_read_on_the_remote_object(origin: Path, object_id: str) -> list[Path]:
    """Leave the bare origin's refs readable while its objects cannot be served.

    MEASURED 2026-08-26 (the measurement `tasks.md` § 3.3 asked for): `chmod
    000` on the whole `objects/` directory -- the mechanism that task proposed
    FIRST -- makes git refuse the path as a repository at all, so `ls-remote`
    itself exits 128 with "does not appear to be a git repository" and the
    fixture proves the pre-existing "remote main is unavailable" path instead
    of this one. Revoking read on the single object FILE keeps advertisement
    working (`ls-remote` exits 0, naming the advanced oid) while `upload-pack`
    answers "not our ref", which is the condition wanted: the remote declines
    to serve an object it advertises.
    """
    loose = origin / "objects" / object_id[:2] / object_id[2:]
    revoked = (
        [loose]
        if loose.is_file()
        else sorted((origin / "objects" / "pack").glob("*.pack"))
    )
    assert revoked, "the fixture found no object file to make unreadable"
    for path in revoked:
        path.chmod(0o000)
    return revoked


def test_verify_promotion_fails_closed_naming_the_fetch_it_could_not_perform(
    tmp_path: Path,
) -> None:
    """THE UNAVAILABLE-OBJECT PROOF. An object that cannot be made locally
    available is a fact about the ENVIRONMENT, so it stays a fail-closed
    dependency refusal rather than becoming a finding about the release -- and
    its reason names the retrieval that failed. "Reachability could not be
    determined" points at the verifier's own uncertainty and sends the reader
    to inspect the candidate, which is the one place the answer is not.
    """
    tag = "contract-v2.0"
    repo, commit, advanced = _skewed_candidate(
        tmp_path, tag, relative="unrelated.txt", content="another change\n"
    )
    origin = tmp_path / "origin.git"
    revoked = _revoke_read_on_the_remote_object(origin, advanced)
    try:
        # Fixture soundness: the refs still advertise, so this is the
        # fetch-impossible path and NOT "remote main is unavailable".
        assert release._ls_remote(repo, "origin", "refs/heads/main")[0][0] == advanced
        with pytest.raises(release.ReleaseDependencyError) as excinfo:
            release.verify_promotion(repo, commit=commit, remote="origin", tag=tag)
    finally:
        for path in revoked:
            path.chmod(0o644)
    message = str(excinfo.value)
    assert "fetch" in message
    assert advanced in message
    assert "could not be determined" not in message


@pytest.mark.parametrize(
    ("relative", "content"),
    [
        ("unrelated.txt", "another change\n"),
        (
            "contracts/manifest.yaml",
            "schema_version: 1\ncontract_bundle_version: contract-v2.0\nextra: drift\n",
        ),
    ],
    ids=["skew", "surface-drift"],
)
def test_mutation_removing_the_resolution_step_alone_reproduces_the_refusal(
    tmp_path: Path, relative: str, content: str
) -> None:
    """MUTATION CHECK: with the resolution step removed and NOTHING else
    changed, both skew proofs must fail by reproducing the original refusal on
    an absent object. A proof that still passed would be pinned to the shape of
    the fix rather than to the defect. This also pins `_is_ancestor`'s
    128-branch guard in place: widening it to treat 128 as "not reachable"
    would invent a verdict from an absence, and this assertion would notice.
    """
    tag = "contract-v2.0"
    repo, commit, _ = _skewed_candidate(
        tmp_path, tag, relative=relative, content=content
    )
    original = release._resolve_remote_object
    release._resolve_remote_object = lambda *args, **kwargs: None
    try:
        with pytest.raises(release.ReleaseDependencyError) as excinfo:
            release.verify_promotion(repo, commit=commit, remote="origin", tag=tag)
    finally:
        release._resolve_remote_object = original
    assert "commit reachability could not be determined" in str(excinfo.value), (
        "removing the resolution step did not reproduce the 128 refusal -- the "
        "skew proofs are unpinned and must be rewritten"
    )


# --- truncated history: a negative verdict a shallow clone cannot earn --------
#
# Resolving the operand makes the OBJECT present; it does not make the ANCESTRY
# present. A shallow clone's graft boundary tells git a commit has no parents,
# so `merge-base --is-ancestor` returns a definite 1 for a commit that is
# perfectly reachable on the real history. These fixtures build that exact
# store: a real `--depth 1` clone, which needs a `file://` URL because git
# ignores `--depth` on a plain local path.


def _shallow_clone(tmp_path: Path, origin: Path, name: str = "shallow") -> Path:
    """Clone the bare origin's `main` at depth 1 -- a genuinely truncated store."""
    target = tmp_path / name
    _git(
        tmp_path,
        "clone",
        "--quiet",
        "--depth",
        "1",
        "--branch",
        "main",
        f"file://{origin}",
        str(target),
    )
    _git(target, "config", "user.name", "Hermes Contract Tests")
    _git(target, "config", "user.email", "hermes-tests@example.invalid")
    _git(target, "config", "commit.gpgsign", "false")
    assert _git(target, "rev-parse", "--is-shallow-repository") == "true"
    return target


def test_verify_tag_refuses_a_negative_verdict_a_shallow_clone_cannot_earn(
    tmp_path: Path,
) -> None:
    """MEASURED against the canonical remote before it was fixed, and
    independently raised by Copilot on pull request #390: the tag here IS on
    published main -- the fixture pushes it at main's own parent -- but a depth-1
    clone cannot see the link, so `merge-base` answers a definite 1 and the
    verifier would have emitted a FALSE `HGR-RELEASE-TAG-UNREACHABLE`. Ruled by
    Brett 2026-08-26: refuse instead, naming the truncated history.
    """
    tag = "contract-v2.0"
    repo, tagged = _repo_with_committed_inventory(tmp_path, "repo", tag)
    (repo / "unrelated.txt").write_text("later\n", encoding="utf-8")
    _commit_all(repo, "main advances past the tagged commit")
    origin = _bare_origin(tmp_path)
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    _git(repo, "tag", "-a", tag, "-m", "release", tagged)
    _git(repo, "push", "--quiet", "origin", tag)

    shallow = _shallow_clone(tmp_path, origin)
    # The tag's commit is genuinely reachable from published main, and the
    # truncated store genuinely cannot tell.
    assert _object_is_absent(shallow, tagged)

    with pytest.raises(release.ReleaseDependencyError) as excinfo:
        release.verify_tag(shallow, remote="origin", tag=tag)
    message = str(excinfo.value)
    assert "shallow" in message
    assert tagged in message
    assert "UNREACHABLE" not in message
    # A full clone of the same origin reaches the honest verdict instead.
    full = tmp_path / "full"
    _git(tmp_path, "clone", "--quiet", "--branch", "main", str(origin), str(full))
    assert release.verify_tag(full, remote="origin", tag=tag) == []


def test_verify_promotion_refuses_a_negative_verdict_in_a_shallow_clone(
    tmp_path: Path,
) -> None:
    """The candidate path carries the identical hazard, so it carries the
    identical guard. Here the candidate really is off published main, and the
    refusal fires anyway -- deliberately: a truncated store cannot tell an
    earned negative from a grafted one, so a fail-closed refusal naming the
    truncation is the honest outcome for both, and the finding is left to a
    clone that can actually judge it.
    """
    tag = "contract-v2.0"
    repo, base = _repo_with_committed_inventory(tmp_path, "repo", tag)
    (repo / "unrelated.txt").write_text("later\n", encoding="utf-8")
    candidate = _commit_all(repo, "the candidate the shallow clone will hold")
    origin = _bare_origin(tmp_path)
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    shallow = _shallow_clone(tmp_path, origin)
    assert _git(shallow, "rev-parse", "HEAD") == candidate

    # Publish a main branched from BEFORE the candidate, so the candidate is
    # genuinely not an ancestor of it -- an earned negative, on the real history.
    _git(repo, "checkout", "--quiet", "-b", "side", base)
    (repo / "sidefile.txt").write_text("side\n", encoding="utf-8")
    side = _commit_all(repo, "off-main commit")
    _git(repo, "push", "--quiet", "--force", "origin", f"{side}:refs/heads/main")
    assert not _is_ancestor_on_the_real_history(repo, candidate, side)

    with pytest.raises(release.ReleaseDependencyError) as excinfo:
        release.verify_promotion(
            shallow, commit=candidate, remote="origin", tag=tag
        )
    message = str(excinfo.value)
    assert "shallow" in message
    assert "UNREACHABLE" not in message
    assert "could not be determined" not in message


def test_a_shallow_clone_still_answers_when_merge_base_can_say_yes(
    tmp_path: Path,
) -> None:
    """THE ASYMMETRY, PINNED. The guard re-examines only the NEGATIVE verdict,
    because a path git found is a path that exists in any store. So a shallow
    clone whose candidate IS reachable from the advanced remote main verifies
    normally and no refusal is raised -- which is also what keeps the extra
    `rev-parse` off the common path.
    """
    tag = "contract-v2.0"
    repo, candidate = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _bare_origin(tmp_path)
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    shallow = _shallow_clone(tmp_path, origin)
    assert _git(shallow, "rev-parse", "HEAD") == candidate

    # Remote main moves to a DESCENDANT of the shallow clone's tip.
    (repo / "unrelated.txt").write_text("another change\n", encoding="utf-8")
    advanced = _commit_all(repo, "another change merged inside the window")
    _git(repo, "push", "--quiet", "origin", "main")
    assert _object_is_absent(shallow, advanced)

    assert (
        release.verify_promotion(
            shallow, commit=candidate, remote="origin", tag=tag
        )
        == []
    )


# --- candidate / realization modes --------------------------------------------


def test_validate_candidate_and_realization_pass_for_a_local_annotated_release(
    tmp_path: Path,
) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _bare_origin(tmp_path)
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    _git(repo, "tag", "-a", tag, "-m", "release", commit)
    _git(repo, "push", "--quiet", "origin", tag)
    assert Path(_git(repo, "remote", "get-url", "origin")) == origin
    catalog = load_yaml_document(repo / "contracts/hermes-runtime/contract-index.yaml")

    assert release.validate_candidate(repo, catalog=catalog) == []
    assert release.validate_realization(repo, catalog=catalog) == []


def test_validate_candidate_passes_for_a_committed_synthetic_candidate(
    tmp_path: Path,
) -> None:
    tag = "contract-v2.0"
    repo, _ = _repo_with_committed_inventory(tmp_path, "repo", tag)
    catalog = load_yaml_document(repo / "contracts/hermes-runtime/contract-index.yaml")
    assert release.validate_candidate(repo, catalog=catalog) == []


# --- fixture matrix -----------------------------------------------------------


def test_release_fixture_matrix_is_self_describing_and_executable(
    tmp_path: Path,
) -> None:
    repo, commit = _synthetic_repo(tmp_path)
    inventory = _canonical_inventory(repo)
    validator = _validator()
    paths = sorted(FIXTURE_DIR.glob("*.yaml"))
    assert [path.name for path in paths] == [
        "release-inventory-duplicate-path.yaml",
        "release-inventory-host-absolute-path.yaml",
        "release-inventory-missing-member.yaml",
        "release-inventory-out-of-order.yaml",
        "release-inventory-valid.yaml",
        "release-inventory-wrong-digest.yaml",
    ]
    seen: set[str] = set()
    for path in paths:
        fixture = load_yaml_document(path)
        case_id = fixture["case_id"]
        seen.add(case_id)
        case = FIXTURE_CASES[case_id]
        assert fixture["kind"] == (
            "openxfactory-hermes-runtime-portable-evidence-fixture"
        ), path
        assert fixture["schema_version"] == 1, path
        assert case_id.startswith("release-"), path
        assert fixture["phase"] == case["phase"], path
        assert fixture["class"] == case["class"], path
        assert fixture["requirement_ids"] == ["HGR-009"], path
        assert fixture["scenario_ids"] == case["scenario_ids"], path
        assert fixture["evaluation_time"] == NOW, path
        assert fixture["inventory"] == case["mutation"](inventory), path

        if fixture["operation"] == "validate_inventory_schema":
            findings = release.inventory_schema_findings(
                fixture["inventory"], path=case_id
            )
        else:
            findings = release.verify_inventory_against_commit(
                repo, commit, fixture["inventory"]
            )
        result = evaluate_expected_findings(fixture, findings)
        assert result["passed"], (path, result)
        if fixture["expected"]["outcome"] == "pass":
            assert list(validator.iter_errors(fixture["inventory"])) == [], path
    assert seen == set(FIXTURE_CASES)


def test_inventory_never_encodes_a_host_local_source_path(tmp_path: Path) -> None:
    repo, _ = _synthetic_repo(tmp_path)
    inventory = _canonical_inventory(repo)
    for entry in inventory["entries"]:
        assert not entry["path"].startswith("/"), entry
        assert "\\" not in entry["path"], entry
        assert "/../" not in f"/{entry['path']}/", entry
    assert inventory["repository"] == "opensoft/openxFactory"


def test_inventory_schema_accepts_release_only_schema_members(tmp_path: Path) -> None:
    repo, _ = _synthetic_repo(tmp_path)
    inventory = _canonical_inventory(repo)
    schema_entry = next(
        entry for entry in inventory["entries"] if entry["type"] == "schema"
    )
    schema_entry["type"] = "release-schema"

    assert release.inventory_schema_findings(inventory, path="candidate") == []


# --- CLI ----------------------------------------------------------------------


def _run_cli(*arguments: str, repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(RELEASE_CLI), "--repo", str(repo), *arguments],
        capture_output=True,
        text=True,
        check=False,
        cwd=ROOT,
    )


def test_cli_build_writes_a_schema_valid_inventory(tmp_path: Path) -> None:
    repo, _ = _synthetic_repo(tmp_path)
    output = tmp_path / "contract-v1.0.digests.yaml"
    result = _run_cli(
        "build", "--tag", SYNTHETIC_TAG, "--output", str(output), "--json", repo=repo
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["status"] == "pass"
    written = load_yaml_document(output)
    assert list(_validator().iter_errors(written)) == []
    assert written == _canonical_inventory(repo)


def test_cli_verify_commit_pass_and_missing_inventory(tmp_path: Path) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    passing = _run_cli("verify-commit", "--commit", commit, repo=repo)
    assert passing.returncode == 0, passing.stderr

    bare_repo, bare_commit = _synthetic_repo(tmp_path, name="bare")
    # SYNTHETIC_TREE pins manifest to contract-v1.0 but writes no inventory file.
    missing = _run_cli(
        "verify-commit", "--commit", bare_commit, "--json", repo=bare_repo
    )
    assert missing.returncode == 1
    payload = json.loads(missing.stdout)
    assert payload["findings"][0]["code"] == "HGR-RELEASE-INVENTORY-MISSING"


def test_cli_verify_commit_uses_requested_repo_under_hostile_common_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tag = "contract-v2.0"
    primary, commit = _repo_with_committed_inventory(tmp_path, "primary", tag)
    repo = tmp_path / "requested"
    _git(primary, "worktree", "add", "--quiet", "-b", "requested", str(repo), commit)
    hostile_common_dir = tmp_path / "hostile-common"
    hostile_common_dir.mkdir()
    monkeypatch.setenv("GIT_COMMON_DIR", str(hostile_common_dir))

    result = _run_cli(
        "verify-commit",
        "--commit",
        commit,
        "--json",
        repo=repo,
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["findings"] == []


@pytest.mark.parametrize(
    "inherited_config",
    [
        {"GIT_CONFIG_PARAMETERS": "'core.bare=true'"},
        {
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "core.bare",
            "GIT_CONFIG_VALUE_0": "true",
        },
    ],
    ids=["parameters", "indexed"],
)
def test_cli_root_discovery_ignores_inherited_command_scope_config(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    inherited_config: dict[str, str],
) -> None:
    tag = "contract-v2.0"
    primary, commit = _repo_with_committed_inventory(tmp_path, "primary", tag)
    repo = tmp_path / "requested"
    _git(primary, "worktree", "add", "--quiet", "-b", "requested", str(repo), commit)
    for name, value in inherited_config.items():
        monkeypatch.setenv(name, value)

    result = _run_cli(
        "verify-commit",
        "--commit",
        commit,
        "--json",
        repo=repo,
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["findings"] == []


def test_cli_verify_commit_reports_findings_with_exit_one(tmp_path: Path) -> None:
    tag = "contract-v2.0"
    repo, candidate = _repo_with_committed_inventory(tmp_path, "repo", tag)
    # Advance HEAD and rewrite a member so the recorded inventory no longer
    # matches the tip, then verify the tip commit.
    (repo / "contracts/hermes-runtime/example-record.schema.yaml").write_text(
        "kind: changed\n", encoding="utf-8"
    )
    drifted = _commit_all(repo, "member drift after candidate")
    result = _run_cli("verify-commit", "--commit", drifted, repo=repo)
    assert result.returncode == 1
    assert "HGR-RELEASE-DIGEST-MISMATCH" in result.stdout


def test_cli_verify_promotion_and_verify_tag(tmp_path: Path) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _bare_origin(tmp_path)
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    promotion = _run_cli(
        "verify-promotion",
        "--commit",
        commit,
        "--remote",
        "origin",
        "--tag",
        tag,
        repo=repo,
    )
    assert promotion.returncode == 0, promotion.stderr

    _git(repo, "tag", "-a", tag, "-m", "release", commit)
    _git(repo, "push", "--quiet", "origin", tag)
    verified = _run_cli("verify-tag", "--remote", "origin", "--tag", tag, repo=repo)
    assert verified.returncode == 0, verified.stderr

    missing_tag = _run_cli(
        "verify-tag", "--remote", "origin", "--tag", "contract-v9.9", repo=repo
    )
    assert missing_tag.returncode == 1
    assert "HGR-RELEASE-TAG-MISSING" in missing_tag.stdout


def test_cli_ignores_hostile_global_and_system_url_redirects(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _bare_origin(tmp_path, "origin.git")
    hostile = _bare_origin(tmp_path, "hostile.git")
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    global_config = tmp_path / "hostile-global.gitconfig"
    system_config = tmp_path / "hostile-system.gitconfig"
    _write_url_redirect_config(global_config, origin, hostile)
    _write_url_redirect_config(system_config, origin, hostile)
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(global_config))
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", str(system_config))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "0")

    result = _run_cli(
        "verify-promotion",
        "--commit",
        commit,
        "--remote",
        "origin",
        "--tag",
        tag,
        repo=repo,
    )

    assert result.returncode == 0, result.stderr


def test_cli_dependency_error_is_exit_two(tmp_path: Path) -> None:
    repo, _ = _synthetic_repo(tmp_path)
    result = _run_cli("verify-commit", "--commit", "0" * 40, repo=repo)
    assert result.returncode == 2


# ---- cross-family membership paths (contract-v1.27 hardening) ---------------
#
# The doxBench wire schemas live in contracts/schemas/, named from the catalog
# via family-relative `../schemas/...` paths. Two pins: normalization RESOLVES
# a legitimate cross-family member into the repo, and a path that would escape
# the repository after normalization FAILS CLOSED as a dependency error rather
# than digesting content from outside the tree.

def _append_index_entry(
    repo: Path,
    path_value: str,
    *,
    member_type: str = "schema",
    semantic_member: bool = True,
) -> None:
    import yaml
    index_path = repo / "contracts" / "hermes-runtime" / "contract-index.yaml"
    index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    index["contracts"].append({
        "contract_id": "cross-family-entry",
        "path": path_value,
        "type": member_type,
        "contract_schema_version": 1,
        "consumers": ["openxfactory-validator"],
        "semantic_member": semantic_member,
        "release_member": True,
    })
    index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")


def test_cross_family_index_paths_normalize_into_the_repo(tmp_path: Path) -> None:
    repo, _ = _synthetic_repo(tmp_path)
    (repo / "contracts" / "schemas").mkdir(parents=True)
    (repo / "contracts" / "schemas" / "extra.schema.yaml").write_text(
        "kind: extra\n", encoding="utf-8")
    _append_index_entry(repo, "../schemas/extra.schema.yaml")
    members = {path.as_posix() for path in release.release_membership(repo)}
    assert "contracts/schemas/extra.schema.yaml" in members
    assert not any(m.startswith("contracts/hermes-runtime/..") for m in members)


def test_release_only_schema_carries_and_verifies_its_catalog_pin(
    tmp_path: Path,
) -> None:
    repo, _ = _synthetic_repo(tmp_path)
    (repo / "contracts" / "schemas").mkdir(parents=True)
    (repo / "contracts" / "schemas" / "extra.schema.yaml").write_text(
        "kind: extra\n", encoding="utf-8"
    )
    _append_index_entry(
        repo,
        "../schemas/extra.schema.yaml",
        member_type="release-schema",
        semantic_member=False,
    )
    commit = _commit_all(repo, "add release-only schema")

    inventory = _canonical_inventory(repo)
    entry = next(
        item for item in inventory["entries"]
        if item["artifact_id"] == "cross-family-entry"
    )
    assert entry["type"] == "release-schema"
    assert entry["schema_id"] == "cross-family-entry"
    assert entry["schema_version"] == 1

    entry["schema_version"] = 2
    assert "HGR-RELEASE-SCHEMA-PIN-MISMATCH" in _codes(
        release.verify_inventory_against_commit(repo, commit, inventory)
    )


def test_an_index_path_escaping_the_repo_fails_closed(tmp_path: Path) -> None:
    repo, _ = _synthetic_repo(tmp_path)
    _append_index_entry(repo, "../../../outside.yaml")
    with pytest.raises(release.ReleaseDependencyError) as excinfo:
        release.release_membership(repo)
    assert "escape" in str(excinfo.value)


def test_working_tree_source_fails_closed_outside_the_repo(tmp_path: Path) -> None:
    """PR #45 Copilot blocker 2: the working-tree source itself refuses a
    normalized path outside the repository root — defense in depth beneath the
    membership guard."""
    repo, _ = _synthetic_repo(tmp_path)
    (tmp_path / "outside.txt").write_text("x", encoding="utf-8")
    source = release._WorkingTreeSource(repo)
    with pytest.raises(release.ReleaseDependencyError):
        source.read_member("../outside.txt")


def test_two_entries_normalizing_to_one_member_fail_closed(tmp_path: Path) -> None:
    """PR #45 Copilot blocker 5: two DISTINCT catalog entries whose paths
    normalize to the same repository file must refuse loudly — a silent
    overwrite would let one entry's metadata masquerade as the other's in the
    closed membership."""
    repo, _ = _synthetic_repo(tmp_path)
    # `../hermes-runtime/contract-index.yaml` normalizes onto the raw
    # `contract-index.yaml` member already in the synthetic catalog.
    _append_index_entry(repo, "../hermes-runtime/contract-index.yaml")
    with pytest.raises(release.ReleaseDependencyError) as excinfo:
        release.release_membership(repo)
    assert "normalize" in str(excinfo.value) or "collision" in str(excinfo.value)


# ---- contracts/clearing/ family membership (issue #722) ---------------------
#
# The clearing family has its own closed-corpus mechanism — per-row sha256
# inside `contracts/manifest.yaml` itself, enforced by
# `scripts/validate-clearing-dispatch.py` and
# `tests/clearing/test_clearing_manifest_rows.py` — and none of that changes
# here. What these prove is the SEPARATE, general release-digest inventory:
# before this fix `FAMILY_PREFIX` never pointed at `contracts/clearing/` and no
# other block swept its paths in, so the family's contract bytes were silent in
# a cut's inventory even when a governed change registered a new clearing
# schema in the same cut. These pin the fix: the family joins when present,
# with the same digest rule as every other member, and stays silent — not an
# error — when it is absent (a pre-`contract-v3.3` repo).

CLEARING_SCHEMA_YAML = "kind: xfactory_clearing_dispatch_record\n"
CLEARING_REGISTRY_YAML = (
    "kind: xfactory_clearing_permitted_operations_registry\nentries: []\n"
)
CLEARING_README_MD = "# clearing\n"
CLEARING_TEST_PY = "def test_placeholder() -> None:\n    assert True\n"
CLEARING_VALIDATOR_PY = '#!/usr/bin/env python3\n"""stub clearing validator"""\n'

# The clearing family's own release-semantic floor (RULED, Brett Heap,
# 2026-09-12 ~14:55Z, openxFactory #745, PR #1000 thread
# PRRT_kwDOTAvnrs6hsjob): CLEARING_RELEASE_FLOOR = (4, 1), the first cut past
# the already-published contract-v4.0. AT_FLOOR is the lowest bundle the
# family is a member for; BELOW_FLOOR is the highest bundle it is not,
# deliberately the real contract-v4.0 boundary this repository actually
# published, not an arbitrary lower number.
CLEARING_AT_FLOOR_TAG = "contract-v4.1"
CLEARING_BELOW_FLOOR_TAG = "contract-v4.0"


def _set_bundle_tag(repo: Path, bundle_tag: str) -> None:
    """Overwrite only this synthetic repo's declared bundle version.

    A targeted rewrite of ``contracts/manifest.yaml`` rather than a change to
    module-level ``MANIFEST_YAML``/``SYNTHETIC_TREE``: those back every other
    test in this file at ``SYNTHETIC_TAG`` ("contract-v1.0"), and the clearing
    floor sits far above that, so the floor-boundary tests below need their
    own declared version without moving the shared default.

    Both floor-boundary tags this file uses (contract-v4.0 and contract-v4.1)
    sit past ``INTENT_RELEASE_FLOOR`` (2, 3) too, so crossing the clearing
    floor also arms intent-compliance's OWN registration-completeness
    invariant — a synthetic repo that declares one of these tags without also
    registering the six canonical intent tuples fails closed with
    ``HGR-RELEASE-INTENT-REGISTRATION-INCOMPLETE`` before the clearing gate is
    ever reached, exactly as it would for a real repo at this version. This
    writes that registration alongside the bundle tag and
    ``_satisfy_intent_registration`` below drops the six target files it
    names, so these tests exercise the clearing floor in an otherwise
    fully-compliant repo rather than tripping a second, unrelated gate.
    """
    registration_yaml = "".join(
        f"- id: {identifier}\n  path: {path}\n  type: {artifact_type}\n"
        "  schema_version: 1\n"
        for identifier, path, artifact_type in release.INTENT_REQUIRED_REGISTRATIONS
    )
    _write_tree(
        repo,
        {"contracts/manifest.yaml": (
            f"schema_version: 1\ncontract_bundle_version: {bundle_tag}\n"
            f"contracts:\n{registration_yaml}"
        )},
    )
    _satisfy_intent_registration(repo)


def _satisfy_intent_registration(repo: Path) -> None:
    """Drop the six files ``INTENT_REQUIRED_REGISTRATIONS`` names, so a
    repo whose manifest registers them (``_set_bundle_tag`` above) also
    carries them — the registration and the file are two separate
    invariants (`HGR-RELEASE-INTENT-REGISTRATION-INCOMPLETE` vs.
    `HGR-RELEASE-INTENT-MEMBER-MISSING`) and this satisfies both. Also drops
    `scripts/__init__.py`: once the intent floor is active `_collect_members`
    adds it unconditionally, and `SYNTHETIC_TREE` — built for tests well
    below that floor — never carries it, so a `build_release_inventory` call
    here would otherwise fail closed trying to read a member that does not
    exist on disk."""
    _write_tree(
        repo,
        {
            path: "schema_version: 1\n"
            for _, path, _ in release.INTENT_REQUIRED_REGISTRATIONS
        }
        | {"scripts/__init__.py": ""},
    )


def _add_clearing_family(repo: Path) -> None:
    _write_tree(
        repo,
        {
            "contracts/clearing/README.md": CLEARING_README_MD,
            "contracts/clearing/dispatch-record.schema.yaml": CLEARING_SCHEMA_YAML,
            "contracts/clearing/permitted-operations.registry.yaml": (
                CLEARING_REGISTRY_YAML
            ),
            "contracts/clearing/examples/dispatch-record-cleared.example.yaml": (
                CLEARING_SCHEMA_YAML
            ),
            "tests/clearing/test_schemas.py": CLEARING_TEST_PY,
            "scripts/validate-clearing-dispatch.py": CLEARING_VALIDATOR_PY,
        },
    )


def test_release_membership_excludes_clearing_family_when_absent(
    tmp_path: Path,
) -> None:
    repo, _ = _synthetic_repo(tmp_path)
    members = {path.as_posix() for path in release.release_membership(repo)}
    assert not any(m.startswith("contracts/clearing/") for m in members)
    assert not any(m.startswith("tests/clearing/") for m in members)
    assert "scripts/validate-clearing-dispatch.py" not in members


def test_release_membership_includes_clearing_family_when_present(
    tmp_path: Path,
) -> None:
    repo, _ = _synthetic_repo(tmp_path)
    _add_clearing_family(repo)
    # At or after CLEARING_RELEASE_FLOOR (RULED, #745): below it, the family
    # is excluded regardless of presence — see
    # test_release_membership_excludes_clearing_family_below_the_floor.
    _set_bundle_tag(repo, CLEARING_AT_FLOOR_TAG)
    commit = _commit_all(repo, "add clearing family at the release floor")

    members = {path.as_posix() for path in release.release_membership(repo)}
    expected = {
        "contracts/clearing/README.md",
        "contracts/clearing/dispatch-record.schema.yaml",
        "contracts/clearing/permitted-operations.registry.yaml",
        "contracts/clearing/examples/dispatch-record-cleared.example.yaml",
        "tests/clearing/test_schemas.py",
        "scripts/validate-clearing-dispatch.py",
    }
    assert expected <= members

    inventory = release.build_release_inventory(repo, bundle_tag=CLEARING_AT_FLOOR_TAG)
    entries = {
        e["path"]: e for e in inventory["entries"] if isinstance(e, dict)
    }

    schema_entry = entries["contracts/clearing/dispatch-record.schema.yaml"]
    assert schema_entry["type"] == "schema"
    assert schema_entry["digest"] == (
        "sha256:" + hashlib.sha256(CLEARING_SCHEMA_YAML.encode("utf-8")).hexdigest()
    )
    # Same digest rule as every other member (raw Git blob bytes) and no
    # schema_id/schema_version pin: the clearing family's own manifest rows
    # already carry that pin, so this inventory only has to record the bytes.
    # Both halves of the pin are checked (Copilot review,
    # PRRT_kwDOTAvnrs6hsjoh): an implementation that fabricated
    # `schema_version` alone while leaving `schema_id` absent would have
    # passed the single-field check.
    assert "schema_id" not in schema_entry
    assert "schema_version" not in schema_entry

    registry_entry = entries["contracts/clearing/permitted-operations.registry.yaml"]
    assert registry_entry["type"] == "documentation"

    validator_entry = entries["scripts/validate-clearing-dispatch.py"]
    assert validator_entry["type"] == "validator"

    readme_entry = entries["contracts/clearing/README.md"]
    assert readme_entry["type"] == "documentation"

    # No dependency error and no fail-closed path: unlike intent-compliance,
    # this family carries no registration-completeness invariant of its own,
    # so a plain round trip (build from the working tree, verify against the
    # exact commit) must be clean.
    assert release.verify_inventory_against_commit(repo, commit, inventory) == []


def test_release_membership_clearing_joins_are_independent_of_each_other(
    tmp_path: Path,
) -> None:
    """Each of the three clearing joins — the contracts tree, the test
    package, the named validator — is its own presence check. One present
    without the others does not pull the others in and does not error.

    Three separate repos, one per join (Copilot review,
    PRRT_kwDOTAvnrs6hxHX0): the original version of this test exercised only
    the contracts-tree case, so a regression that nested the test-package or
    validator join under the contracts-tree presence check would still have
    passed."""
    contracts_only, _ = _synthetic_repo(tmp_path, name="contracts-only")
    _write_tree(contracts_only, {"contracts/clearing/README.md": CLEARING_README_MD})
    _set_bundle_tag(contracts_only, CLEARING_AT_FLOOR_TAG)
    _commit_all(
        contracts_only, "add only the clearing contracts tree, at the release floor"
    )
    contracts_only_members = {
        path.as_posix() for path in release.release_membership(contracts_only)
    }
    assert "contracts/clearing/README.md" in contracts_only_members
    assert not any(m.startswith("tests/clearing/") for m in contracts_only_members)
    assert "scripts/validate-clearing-dispatch.py" not in contracts_only_members

    tests_only, _ = _synthetic_repo(tmp_path, name="tests-only")
    _write_tree(tests_only, {"tests/clearing/test_schemas.py": CLEARING_TEST_PY})
    _set_bundle_tag(tests_only, CLEARING_AT_FLOOR_TAG)
    _commit_all(
        tests_only, "add only the clearing test package, at the release floor"
    )
    tests_only_members = {
        path.as_posix() for path in release.release_membership(tests_only)
    }
    assert "tests/clearing/test_schemas.py" in tests_only_members
    assert not any(m.startswith("contracts/clearing/") for m in tests_only_members)
    assert "scripts/validate-clearing-dispatch.py" not in tests_only_members

    validator_only, _ = _synthetic_repo(tmp_path, name="validator-only")
    _write_tree(
        validator_only,
        {"scripts/validate-clearing-dispatch.py": CLEARING_VALIDATOR_PY},
    )
    _set_bundle_tag(validator_only, CLEARING_AT_FLOOR_TAG)
    _commit_all(
        validator_only, "add only the clearing validator, at the release floor"
    )
    validator_only_members = {
        path.as_posix() for path in release.release_membership(validator_only)
    }
    assert "scripts/validate-clearing-dispatch.py" in validator_only_members
    assert not any(
        m.startswith("contracts/clearing/") for m in validator_only_members
    )
    assert not any(m.startswith("tests/clearing/") for m in validator_only_members)


def test_release_membership_excludes_clearing_family_below_the_floor(
    tmp_path: Path,
) -> None:
    """RULED (#745, PR #1000 thread PRRT_kwDOTAvnrs6hsjob): presence alone is
    not enough. A declared bundle below CLEARING_RELEASE_FLOOR excludes the
    whole family even though every path is physically present at the source
    — contract-v4.0 is the real boundary this repository already published,
    so this is the exact case that made re-verifying it disagree with its own
    recorded inventory before the floor existed."""
    repo, _ = _synthetic_repo(tmp_path)
    _add_clearing_family(repo)
    _set_bundle_tag(repo, CLEARING_BELOW_FLOOR_TAG)
    commit = _commit_all(repo, "add clearing family below the release floor")

    members = {path.as_posix() for path in release.release_membership(repo)}
    assert not any(m.startswith("contracts/clearing/") for m in members)
    assert not any(m.startswith("tests/clearing/") for m in members)
    assert "scripts/validate-clearing-dispatch.py" not in members

    # The round trip must also stay clean: an inventory built (and thus
    # recorded) below the floor never claims the family, so verifying it
    # against the exact commit that already carries the family's bytes finds
    # no drift either.
    inventory = release.build_release_inventory(repo, bundle_tag=CLEARING_BELOW_FLOOR_TAG)
    assert release.verify_inventory_against_commit(repo, commit, inventory) == []


def test_verify_commit_against_contract_v4_0_stays_clean_under_the_clearing_floor() -> (
    None
):
    """RULED (Brett Heap, 2026-09-12 ~14:55Z, #745, PR #1000 thread
    PRRT_kwDOTAvnrs6hsjob): the one place this file departs from its own
    hermetic-fixture rule and pins a real historical commit on purpose. Unlike
    every other test above, what is under test here is not the mechanism in
    the abstract but a concrete, already-published fact: contract-v4.0 points
    at ce5c054e8522499c6f4ff2039496243a09cb4acf, whose tree already contains
    the whole contracts/clearing/ family, while contract-v4.0.digests.yaml
    (cut before this fix existed) lists none of it. Before
    CLEARING_RELEASE_FLOOR, verifying that exact commit against its own
    recorded inventory reported 59 HGR-RELEASE-MEMBER-MISSING findings —
    measured on PR #1000 before this fix. The floor is what makes it clean
    again, and only a real commit proves that; a synthetic fixture could not,
    because the whole defect was ABOUT a real tag someone already published."""
    commit = "ce5c054e8522499c6f4ff2039496243a09cb4acf"
    committed = release.resolve_committed_inventory(ROOT, commit)
    assert committed is not None, (
        f"{commit} (contract-v4.0) must still record a release digest "
        "inventory at that commit"
    )
    inventory_path, inventory = committed
    assert inventory_path == "contracts/releases/contract-v4.0.digests.yaml"
    assert release.verify_inventory_against_commit(ROOT, commit, inventory) == []


# --- content-resolution conflation (fix-content-resolution-conflation) --------
#
# `_blob_object_id` and `_CommitSource.exists` reduce a content resolution to a
# blob identity or to a presence answer.  Exactly one of the resolver's fifteen
# refusals establishes that answer; the other fourteen establish nothing about
# the release.  These proofs separate the two, and the quiet direction — BOTH
# sides of a `_surface_drift` comparison failing, two non-answers comparing
# equal, the surface reported undrifted having been read on neither side — is
# the one that matters, because it emits nothing a reader could notice.
#
# The hazards below are driven by COMMITTED DATA (a release-surface path that
# is a directory or a nested repository link at one commit) and by ARGUMENT (a
# repository that is not there, a revision that is not an object id, a path
# that is not canonical) rather than by a real store timeout, per Q4: the
# requirement is about the distinction, not about any one way of failing.

SURFACE_NON_MEMBER = "contracts/hermes-runtime/README.md"


def _hazard_directory(repo: Path) -> None:
    """Commit a DIRECTORY where a release-surface regular file belongs."""

    target = repo / SURFACE_NON_MEMBER
    if target.exists():
        target.unlink()
    target.mkdir(parents=True)
    (target / "keep.md").write_text("# not a regular file\n", encoding="utf-8")


def _hazard_gitlink(repo: Path, tmp_path: Path) -> None:
    """Commit a NESTED REPOSITORY LINK where a release-surface file belongs."""

    child = support.init_git_repo(tmp_path / "surface-child")
    child_commit = support.commit_files(child, {"README.md": "child\n"})
    target = repo / SURFACE_NON_MEMBER
    if target.exists():
        target.unlink()
    _git(
        repo,
        "update-index",
        "--add",
        "--cacheinfo",
        f"160000,{child_commit},{SURFACE_NON_MEMBER}",
    )


def _hazard_absent(repo: Path) -> None:
    """Commit a tree that simply does not carry the release-surface path."""

    (repo / SURFACE_NON_MEMBER).unlink()


def _published(repo: Path, tmp_path: Path, name: str = "origin.git") -> Path:
    origin = _bare_origin(tmp_path, name)
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "--quiet", "origin", "main")
    return origin


# 3.1 — the absent path is the ONE condition that is a release fact, and it
# still reaches exactly the answer it reaches today, in both directions.


def test_a_release_surface_path_absent_at_both_commits_still_reports_clean(
    tmp_path: Path,
) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(
        tmp_path, "repo", tag, hazard=_hazard_absent
    )
    _published(repo, tmp_path)
    assert release._blob_object_id(repo, commit, SURFACE_NON_MEMBER) is None
    assert release._surface_drift(repo, commit, commit) == []
    assert release.verify_promotion(repo, commit=commit, remote="origin", tag=tag) == []


def test_a_release_surface_path_absent_on_one_side_alone_still_drifts(
    tmp_path: Path,
) -> None:
    tag = "contract-v2.0"
    repo, candidate = _repo_with_committed_inventory(tmp_path, "repo", tag)
    _hazard_absent(repo)
    _commit_all(repo, "the release surface path leaves the tree")
    _published(repo, tmp_path)
    assert "HGR-RELEASE-SURFACE-DRIFT" in _codes(
        release.verify_promotion(repo, commit=candidate, remote="origin", tag=tag)
    )


# 3.2 / 3.6 — a resolution that failed for any other reason refuses, and the
# reason names the CONDITION OBSERVED rather than a conclusion about the
# release.  Driven by argument.


def test_an_unresolvable_content_question_refuses_instead_of_answering(
    tmp_path: Path,
) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    absent_repository = tmp_path / "there-is-no-repository-here"

    conditions = {
        "Git repository is unavailable": lambda: release._blob_object_id(
            absent_repository, commit, "contracts/manifest.yaml"
        ),
        "revision must be a full Git object ID": lambda: release._blob_object_id(
            repo, "HEAD", "contracts/manifest.yaml"
        ),
        "repository path contains a forbidden segment": (
            lambda: release._blob_object_id(
                repo, commit, "contracts/../contracts/manifest.yaml"
            )
        ),
    }
    for observed, operation in conditions.items():
        with pytest.raises(release.ReleaseDependencyError) as caught:
            operation()
        message = str(caught.value)
        assert observed in message, message
        assert caught.value.exit_code == 2
        # The reason names what failed, never what the release is.
        assert "drift" not in message.lower(), message
        assert "unreachable" not in message.lower(), message
        # The resolver's own refusal is preserved for the reader.
        assert isinstance(caught.value.__cause__, ContentResolutionError)


def test_commit_source_exists_reports_absence_and_refuses_everything_else(
    tmp_path: Path,
) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    source = release._CommitSource(repo, commit)

    assert source.exists("contracts/manifest.yaml") is True
    assert source.exists("contracts/there-is-no-such-file.yaml") is False

    with pytest.raises(release.ReleaseDependencyError):
        source.exists("contracts/../contracts/manifest.yaml")
    with pytest.raises(release.ReleaseDependencyError):
        release._CommitSource(tmp_path / "no-repository", commit).exists(
            "contracts/manifest.yaml"
        )
    with pytest.raises(release.ReleaseDependencyError):
        release._CommitSource(repo, "HEAD").exists("contracts/manifest.yaml")


def test_an_unreadable_manifest_is_not_reported_as_a_release_without_one(
    tmp_path: Path,
) -> None:
    """`exists` at :611 decides whether `contracts/manifest.yaml` is present.

    A safety refusal read as absence there makes `resolve_committed_inventory`
    answer `None` — "this commit records no release inventory" — which is a
    verdict about the release manufactured from a fact about the object it
    could not read.
    """

    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    manifest = repo / "contracts/manifest.yaml"
    manifest.unlink()
    manifest.mkdir()
    (manifest / "keep.yaml").write_text("schema_version: 1\n", encoding="utf-8")
    hazarded = _commit_all(repo, "the manifest path stops being a regular file")

    with pytest.raises(release.ReleaseDependencyError) as caught:
        release.resolve_committed_inventory(repo, hazarded)
    assert "Git path is not a supported regular file" in str(caught.value)
    # And the ordinary commit is untouched.
    assert release.resolve_committed_inventory(repo, commit) is not None


# 3.3 — THE QUIET DIRECTION.  Both sides fail; two identical non-answers
# compare equal; today the surface reports undrifted having been read on
# neither side.  The verification must refuse, and it must not trade the
# silence for a drift finding either.


def test_a_comparison_that_resolved_neither_side_refuses_rather_than_passing(
    tmp_path: Path,
) -> None:
    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(
        tmp_path, "repo", tag, hazard=_hazard_directory
    )
    _published(repo, tmp_path)

    # Both operands are the same commit, which is the ordinary shape of a
    # promotion check for a candidate already on `main` — so BOTH reads of the
    # surface path take the same safety refusal.
    with pytest.raises(release.ReleaseDependencyError) as caught:
        release._surface_drift(repo, commit, commit)
    message = str(caught.value)
    assert "Git path is not a supported regular file" in message, message
    assert SURFACE_NON_MEMBER in message, message
    # The failure has two wrong answers and only one of them is loud: the
    # refusal must not be a drift finding either.
    assert "HGR-RELEASE-SURFACE-DRIFT" not in message

    with pytest.raises(release.ReleaseDependencyError):
        release.verify_promotion(repo, commit=commit, remote="origin", tag=tag)


def test_the_quiet_direction_driven_by_argument_refuses_on_both_sides(
    tmp_path: Path,
) -> None:
    """The same failure at the expression `_surface_drift` evaluates.

    Driven by ARGUMENT rather than by a store timeout (Q4): an absent
    repository reaches the same branch instantly and deterministically.
    """

    tag = "contract-v2.0"
    repo, commit = _repo_with_committed_inventory(tmp_path, "repo", tag)
    origin = _published(repo, tmp_path)
    main_oid = _git(repo, "rev-parse", "HEAD")
    absent_repository = tmp_path / "neither-side-can-be-read"
    assert not absent_repository.exists()
    assert origin.is_dir()

    for operand in (commit, main_oid):
        with pytest.raises(release.ReleaseDependencyError):
            release._blob_object_id(
                absent_repository, operand, "contracts/manifest.yaml"
            )


# 3.4 — a safety refusal stays a refusal and is not demoted to absence, and it
# is not softened because the other commit reads cleanly.


@pytest.mark.parametrize("hazard_name", ["directory", "gitlink"])
def test_an_unsafe_release_surface_object_is_refused_not_read_as_absence(
    tmp_path: Path, hazard_name: str
) -> None:
    tag = "contract-v2.0"
    repo, candidate = _repo_with_committed_inventory(tmp_path, "repo", tag)
    # The candidate reads cleanly; the published side does not.
    assert release._blob_object_id(repo, candidate, SURFACE_NON_MEMBER) is not None
    if hazard_name == "directory":
        _hazard_directory(repo)
        _commit_all(repo, "the release surface path becomes a directory")
        observed = "Git path is not a supported regular file"
    else:
        _hazard_gitlink(repo, tmp_path)
        _git(repo, "commit", "--quiet", "-m", "the release surface path becomes a link")
        observed = "Git path is not a supported regular file"
    _published(repo, tmp_path)

    with pytest.raises(release.ReleaseDependencyError) as caught:
        release.verify_promotion(repo, commit=candidate, remote="origin", tag=tag)
    assert observed in str(caught.value)


# 3.7 — the distinction is read off the resolver's DECLARED code, at source
# level, never off its prose.  A structural assertion because no behavioural
# test can see the difference on the day the message is edited.


def test_the_distinction_is_carried_by_the_declared_code_not_by_the_message() -> None:
    source = (ROOT / "scripts/hermes_runtime_validation/release.py").read_text(
        encoding="utf-8"
    )
    assert "CONTENT_PATH_ABSENT" in source
    assert "exact Git path is unavailable" not in source
