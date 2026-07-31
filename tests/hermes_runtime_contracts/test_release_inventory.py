"""Closed release digest inventory build and verification (T068 RED / T074 GREEN).

Covers deterministic candidate build, raw-Git-blob digest parity against a
hashlib oracle, exact-commit verification that ignores working-tree edits,
closed-membership negatives, symlink/submodule/traversal and host-path
rejection, pre-tag promotion-race negatives, annotated-tag verification, and CLI
subprocess exit codes.  Verification always reads exact Git objects and never
the working tree (research Decisions 10 and 11; requirement HGR-009).
"""

from __future__ import annotations

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


# --- promotion ----------------------------------------------------------------


def _repo_with_committed_inventory(
    tmp_path: Path, name: str, tag: str
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


# --- candidate / realization modes --------------------------------------------


def test_validate_candidate_passes_on_the_realized_repository() -> None:
    # Post-realization (contract-v1.9): the realized release digest inventory is
    # committed at contracts/releases/contract-v1.9.digests.yaml, which is the
    # thing this test actually needs to prove -- the pre-realization
    # missing-inventory state (HGR-RELEASE-INVENTORY-MISSING) is gone for both
    # candidate and realization validation.
    #
    # It does NOT assert `== []`: main keeps moving after a release is cut, and
    # release members (e.g. contracts/README.md) legitimately drift from the
    # frozen contract-v1.9 digest inventory in between releases -- that is
    # correct product behavior (you re-realize for the next version), not a
    # bug. So drift findings like HGR-RELEASE-DIGEST-MISMATCH are expected and
    # acceptable here; only the missing-inventory failure mode is disallowed.
    inventory_path = ROOT / "contracts/releases/contract-v1.9.digests.yaml"
    assert inventory_path.is_file(), inventory_path
    catalog = load_yaml_document(ROOT / "contracts/hermes-runtime/contract-index.yaml")
    candidate = release.validate_candidate(ROOT, catalog=catalog)
    assert "HGR-RELEASE-INVENTORY-MISSING" not in [
        finding["code"] for finding in candidate
    ]
    realization = release.validate_realization(ROOT, catalog=catalog)
    assert "HGR-RELEASE-INVENTORY-MISSING" not in [
        finding["code"] for finding in realization
    ]


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

def _append_index_entry(repo: Path, path_value: str) -> None:
    import yaml
    index_path = repo / "contracts" / "hermes-runtime" / "contract-index.yaml"
    index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    index["contracts"].append({
        "contract_id": "cross-family-entry",
        "path": path_value,
        "type": "schema",
        "contract_schema_version": 1,
        "consumers": ["openxfactory-validator"],
        "semantic_member": True,
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


def test_an_index_path_escaping_the_repo_fails_closed(tmp_path: Path) -> None:
    repo, _ = _synthetic_repo(tmp_path)
    _append_index_entry(repo, "../../../outside.yaml")
    with pytest.raises(release.ReleaseDependencyError) as excinfo:
        release.release_membership(repo)
    assert "escape" in str(excinfo.value)
