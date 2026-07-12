"""Adversarial exact-object and pinned-manifest regressions for HCS-004."""

from __future__ import annotations

from dataclasses import replace
import hashlib
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
import pytest
import yaml

from scripts.hermes_runtime_validation.content import (
    ContentResolutionError,
    ResolvedGitContent,
    normalize_repository_path,
    resolve_git_object,
)
from scripts.hermes_runtime_validation.loader import load_yaml_document
from scripts.hermes_runtime_validation.semantics import overlays
from tests.hermes_runtime_contracts.support import commit_files, init_git_repo, run_command


REPOSITORY = "opensoft/example-domain"


def _digest(body: bytes) -> str:
    return f"sha256:{hashlib.sha256(body).hexdigest()}"


def _codes(findings: list[dict[str, str]]) -> list[str]:
    return [finding["code"] for finding in findings]


def _manifest(overlay_files: dict[str, bytes], root: str = "overlay") -> dict[str, Any]:
    paths = sorted(
        (path for path in overlay_files if path.startswith(f"{root}/")),
        key=lambda path: path.encode("utf-8"),
    )
    return {
        "schema_version": 1,
        "kind": "HermesRuntimeOverlayManifest",
        "overlay_root": root,
        "files": [{"path": path, "digest": _digest(overlay_files[path])} for path in paths],
        "exclusions": [],
    }


def _manifest_bytes(manifest: dict[str, Any]) -> bytes:
    return yaml.safe_dump(manifest, sort_keys=False, allow_unicode=False).encode("utf-8")


def _overlay_pin(commit: str, manifest_body: bytes, *, root: str = "overlay") -> dict[str, Any]:
    return {
        "repository": REPOSITORY,
        "commit": commit,
        "overlay_root": root,
        "manifest_path": "manifests/customer.yaml",
        "manifest_digest": _digest(manifest_body),
        "schema_id": overlays.OVERLAY_SCHEMA_ID,
        "schema_version": 1,
    }


def _single_pin(commit: str, body: bytes) -> dict[str, Any]:
    return {
        "repository": REPOSITORY,
        "commit": commit,
        "path": "templates/customer.yaml",
        "digest": _digest(body),
        "schema_id": "https://xforge.us/schemas/example/customer-template",
        "schema_version": 1,
    }


@pytest.fixture
def pinned_overlay_repo(tmp_path: Path) -> tuple[Path, str, dict[str, bytes], bytes, dict[str, Any]]:
    repo = init_git_repo(tmp_path / "repo")
    overlay_files = {
        "overlay/a.yaml": b"name: a\n",
        "overlay/nested/b.yaml": b"name: b\n",
    }
    manifest_body = _manifest_bytes(_manifest(overlay_files))
    files = {
        **overlay_files,
        "manifests/customer.yaml": manifest_body,
        "templates/customer.yaml": b"role: customer\n",
    }
    commit = commit_files(repo, files)
    return repo, commit, files, manifest_body, _overlay_pin(commit, manifest_body)


def test_full_pinned_overlay_reads_exact_manifest_blob_not_worktree(
    pinned_overlay_repo: tuple[Path, str, dict[str, bytes], bytes, dict[str, Any]],
) -> None:
    repo, _, _, _, pin = pinned_overlay_repo
    (repo / "manifests/customer.yaml").write_text("dirty: worktree\n", encoding="utf-8")

    assert overlays.validate_pinned_overlay(
        pin, checkout=repo, expected_repository=REPOSITORY
    ) == []


def test_git_replace_cannot_substitute_bytes_under_pinned_commit(tmp_path: Path) -> None:
    repo = init_git_repo(tmp_path / "repo")
    original_overlay = {"overlay/a.yaml": b"version: original\n"}
    original_manifest = _manifest_bytes(_manifest(original_overlay))
    original_template = b"template: original\n"
    original = commit_files(
        repo,
        {
            **original_overlay,
            "manifests/customer.yaml": original_manifest,
            "templates/customer.yaml": original_template,
        },
        message="original",
    )
    replacement_overlay = {"overlay/a.yaml": b"version: replacement\n"}
    replacement_manifest = _manifest_bytes(_manifest(replacement_overlay))
    replacement_template = b"template: replacement\n"
    replacement = commit_files(
        repo,
        {
            **replacement_overlay,
            "manifests/customer.yaml": replacement_manifest,
            "templates/customer.yaml": replacement_template,
        },
        message="replacement",
    )
    run_command(["git", "replace", original, replacement], cwd=repo, check=True)

    overlay_pin = _overlay_pin(original, replacement_manifest)
    single_pin = _single_pin(original, replacement_template)
    assert "HCS-PIN-DIGEST" in _codes(
        overlays.validate_pinned_overlay(
            overlay_pin, checkout=repo, expected_repository=REPOSITORY
        )
    )
    assert "HCS-PIN-DIGEST" in _codes(
        overlays.validate_single_file_pin(
            single_pin, checkout=repo, expected_repository=REPOSITORY
        )
    )


def test_hostile_resolver_metadata_cannot_authorize_pin_or_overlay(
    pinned_overlay_repo: tuple[Path, str, dict[str, bytes], bytes, dict[str, Any]],
) -> None:
    repo, commit, files, _, _ = pinned_overlay_repo
    manifest = _manifest({path: body for path, body in files.items() if path.startswith("overlay/")})

    def hostile(checkout: str | Path, revision: str, path: str) -> ResolvedGitContent:
        honest = resolve_git_object(checkout, revision, path)
        return replace(
            honest,
            path="attacker/wrong-path",
            git_mode="120000",
            blob_oid="0" * 40,
        )

    assert _codes(
        overlays.validate_single_file_pin(
            _single_pin(commit, files["templates/customer.yaml"]),
            checkout=repo,
            expected_repository=REPOSITORY,
            resolver=hostile,
        )
    ) == ["HCS-PIN-CONTENT"]
    assert "HCS-PIN-CONTENT" in _codes(
        overlays.validate_overlay_manifest(
            manifest,
            checkout=repo,
            commit=commit,
            expected_repository=REPOSITORY,
            resolver=hostile,
        )
    )


def test_hostile_resolver_digest_claim_is_recomputed_from_raw_bytes(
    pinned_overlay_repo: tuple[Path, str, dict[str, bytes], bytes, dict[str, Any]],
) -> None:
    repo, commit, files, _, _ = pinned_overlay_repo

    def hostile(checkout: str | Path, revision: str, path: str) -> ResolvedGitContent:
        honest = resolve_git_object(checkout, revision, path)
        return replace(honest, data=b"attacker bytes", digest=honest.digest)

    assert _codes(
        overlays.validate_single_file_pin(
            _single_pin(commit, files["templates/customer.yaml"]),
            checkout=repo,
            expected_repository=REPOSITORY,
            resolver=hostile,
        )
    ) == ["HCS-PIN-DIGEST"]


def test_resolver_exception_is_a_closed_content_finding(
    pinned_overlay_repo: tuple[Path, str, dict[str, bytes], bytes, dict[str, Any]],
) -> None:
    repo, commit, files, _, _ = pinned_overlay_repo

    def crashing(*_args: object) -> ResolvedGitContent:
        raise ValueError("hostile resolver failure")

    assert _codes(
        overlays.validate_single_file_pin(
            _single_pin(commit, files["templates/customer.yaml"]),
            checkout=repo,
            expected_repository=REPOSITORY,
            resolver=crashing,
        )
    ) == ["HCS-PIN-CONTENT"]


def test_canonical_repository_binding_is_not_self_asserted(
    pinned_overlay_repo: tuple[Path, str, dict[str, bytes], bytes, dict[str, Any]],
) -> None:
    repo, commit, files, _, _ = pinned_overlay_repo
    pin = _single_pin(commit, files["templates/customer.yaml"])
    pin["repository"] = "opensoft/wrong-domain"

    assert _codes(
        overlays.validate_single_file_pin(
            pin, checkout=repo, expected_repository=REPOSITORY
        )
    ) == ["HCS-PIN-REPOSITORY"]
    assert _codes(overlays.validate_single_file_pin(pin, checkout=repo)) == [
        "HCS-PIN-REPOSITORY"
    ]


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        ("root", "HCS-OVERLAY-PIN-MISMATCH"),
        ("digest", "HCS-PIN-DIGEST"),
        ("schema_id", "HCS-PIN-SCHEMA"),
        ("schema_version", "HCS-PIN-SCHEMA"),
    ],
)
def test_overlay_pin_binds_root_digest_and_schema_identity(
    pinned_overlay_repo: tuple[Path, str, dict[str, bytes], bytes, dict[str, Any]],
    mutation: str,
    expected_code: str,
) -> None:
    repo, _, _, _, original_pin = pinned_overlay_repo
    pin = dict(original_pin)
    if mutation == "root":
        pin["overlay_root"] = "overlay-other"
    elif mutation == "digest":
        pin["manifest_digest"] = _digest(b"different manifest")
    elif mutation == "schema_id":
        pin["schema_id"] = "https://example.invalid/wrong.schema.yaml"
    else:
        pin["schema_version"] = 2

    assert expected_code in _codes(
        overlays.validate_pinned_overlay(
            pin, checkout=repo, expected_repository=REPOSITORY
        )
    )


def test_pinned_manifest_rejects_ambiguous_yaml(tmp_path: Path) -> None:
    repo = init_git_repo(tmp_path / "repo")
    overlay_body = b"name: a\n"
    manifest_body = b"""\
schema_version: 1
schema_version: 1
kind: HermesRuntimeOverlayManifest
overlay_root: overlay
files: []
exclusions: []
"""
    commit = commit_files(
        repo,
        {"overlay/a.yaml": overlay_body, "manifests/customer.yaml": manifest_body},
    )
    pin = _overlay_pin(commit, manifest_body)

    assert _codes(
        overlays.validate_pinned_overlay(
            pin, checkout=repo, expected_repository=REPOSITORY
        )
    ) == ["HCS-OVERLAY-SCHEMA"]


def test_manifest_path_must_be_outside_inventory_root(
    pinned_overlay_repo: tuple[Path, str, dict[str, bytes], bytes, dict[str, Any]],
) -> None:
    repo, _, _, _, original_pin = pinned_overlay_repo
    pin = dict(original_pin)
    pin["manifest_path"] = "overlay/overlay-manifest.yaml"

    assert _codes(
        overlays.validate_pinned_overlay(
            pin, checkout=repo, expected_repository=REPOSITORY
        )
    ) == ["HCS-OVERLAY-PIN-CIRCULAR"]


@pytest.mark.parametrize("path", ["templates/with space.yaml", "templates/café.yaml"])
def test_semantics_match_closed_ascii_repository_path_schema(
    pinned_overlay_repo: tuple[Path, str, dict[str, bytes], bytes, dict[str, Any]],
    path: str,
) -> None:
    repo, commit, files, _, _ = pinned_overlay_repo
    pin = _single_pin(commit, files["templates/customer.yaml"])
    pin["path"] = path

    assert _codes(
        overlays.validate_single_file_pin(
            pin, checkout=repo, expected_repository=REPOSITORY
        )
    ) == ["HCS-PIN-PATH"]
    with pytest.raises(ContentResolutionError):
        normalize_repository_path(path)


def test_shared_pin_and_content_only_manifest_schemas_match_public_vocabulary() -> None:
    root = Path("contracts/hermes-runtime")
    shared = load_yaml_document(root / "shared-definitions.schema.yaml")
    manifest_schema = load_yaml_document(root / "overlay-manifest.schema.yaml")
    for document in (shared, manifest_schema):
        Draft202012Validator.check_schema(document)
    registry = Registry().with_resources(
        [
            (shared["$id"], Resource.from_contents(shared, default_specification=DRAFT202012)),
            (
                manifest_schema["$id"],
                Resource.from_contents(manifest_schema, default_specification=DRAFT202012),
            ),
        ]
    )
    checker = FormatChecker()
    single_validator = Draft202012Validator(
        {"$ref": shared["$id"] + "#/$defs/git_file_pin"},
        registry=registry,
        format_checker=checker,
    )
    overlay_pin_validator = Draft202012Validator(
        {"$ref": shared["$id"] + "#/$defs/git_overlay_pin"},
        registry=registry,
        format_checker=checker,
    )
    single = _single_pin("a" * 40, b"template")
    overlay_pin = _overlay_pin("a" * 40, b"manifest")
    manifest = _manifest({"overlay/a.yaml": b"a"})

    assert list(single_validator.iter_errors(single)) == []
    assert list(overlay_pin_validator.iter_errors(overlay_pin)) == []
    assert list(
        Draft202012Validator(
            manifest_schema, registry=registry, format_checker=checker
        ).iter_errors(manifest)
    ) == []
    assert "repository" not in manifest and "commit" not in manifest
