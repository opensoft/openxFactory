"""openxFactory #918 / #919 — validate-domain-factory kind-aware fixes.

Both filed by lane opsXfactory-2 against OpsxFactory item 31 (2026-09-10).

#918: `ISOLATION_SCOPES` carried the legacy `per_customer_subject` machine key
but not `per_subject`, the ratified Subject/Tenant/Domain spelling
(contracts/policies/layer-vocabulary.yaml `legacy_mapping`: customer ->
subject). `per_customer_subject` is FROZEN (CLAUDE.md) and stays accepted
unrenamed; `per_subject` is purely additive.

#919: `profiles/*.yaml` required a nested `profile.id`. Domain-specific
profile kinds — OpsxFactory's `cloudpc_worker_profile` is the first one — key
their identifier on a flat top-level `profile_id` instead, and the canonical
profile glob had no kind filter, so those files were misreported as
"profile.id missing". The fix reads each profile's top-level `kind:` and
requires the flat `profile_id` only for kinds registered in
`PROFILE_ID_KEY_KINDS`; every other kind — including one that declares no
`kind:` at all — keeps requiring the nested `profile.id` exactly as before.
"""
from __future__ import annotations

import sys
from pathlib import Path

COMMIT = "0" * 40

CANONICAL_LAYERS = [
    {"role": "customer", "display_name": "Customer Hermes",
     "overlay": "overlays/customer"},
    {"role": "client", "display_name": "Client Hermes",
     "overlay": "overlays/client"},
    {"role": "domain", "display_name": "Domain Hermes",
     "overlay": "overlays/domain"},
]


def _stack(*, isolation_scope: str = "per_tenant") -> dict:
    return {
        "schema_version": 1,
        "kind": "xfactory_domain_stack",
        "domain": {"id": "fixture_domain"},
        "xfactory": {
            "contract_repo": "opensoft/openxFactory",
            "contract_name": "xfactory-domain-stack",
            "contract_ref_type": "commit",
            "contract_ref": COMMIT,
            "contract_schema_version": 1,
            "contract_declared_at": "contracts/manifest.yaml",
            "contract_source": "git",
        },
        "hermes": {"layers": CANONICAL_LAYERS},
        "tenancy": {
            "tenant_kinds": ["pilot"],
            "isolation": {"pilot": isolation_scope},
        },
        "omnigent": {"domain_overlay": "omnigent"},
    }


def _materialize(
    repo: Path, stack: dict, yaml_writer, *, profiles: dict[str, dict] | None = None,
) -> Path:
    yaml_writer(repo / "stack.yaml", stack)
    for relative in ("overlays/customer", "overlays/client", "overlays/domain"):
        yaml_writer(repo / relative / "agent.yaml", {"schema_version": 1})
    (repo / "omnigent").mkdir(parents=True, exist_ok=True)
    for name, content in (profiles or {}).items():
        yaml_writer(repo / "profiles" / name, content)
    return repo


def _run(command_runner, repo_root: Path, repo: Path):
    return command_runner(
        [sys.executable, repo_root / "scripts/validate-domain-factory.py",
         repo, "--no-secret-scan"],
        cwd=repo_root,
    )


# --------------------------------------------------------------------------
# #918 — `per_subject` added to ISOLATION_SCOPES; `per_customer_subject` stays
# --------------------------------------------------------------------------

def test_per_subject_is_a_recognized_isolation_scope(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    repo = _materialize(tmp_path / "per-subject",
                        _stack(isolation_scope="per_subject"), yaml_writer)

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 0, result.stdout
    assert "0 error(s)" in result.stdout
    assert "recognized isolation scope" not in result.stdout


def test_the_frozen_legacy_per_customer_subject_key_stays_accepted(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    """`per_customer_subject` is a FROZEN legacy machine key (CLAUDE.md);
    adding `per_subject` must not rename or drop it."""
    repo = _materialize(tmp_path / "per-customer-subject",
                        _stack(isolation_scope="per_customer_subject"), yaml_writer)

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 0, result.stdout
    assert "recognized isolation scope" not in result.stdout


def test_an_unrecognized_isolation_scope_still_fails(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    repo = _materialize(tmp_path / "unknown-scope",
                        _stack(isolation_scope="per_galaxy"), yaml_writer)

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 1, result.stdout
    assert ("tenancy.isolation.pilot='per_galaxy' is not a recognized "
            "isolation scope") in result.stdout


# --------------------------------------------------------------------------
# #919 — kind-aware `profile.id` / `profile_id` check
# --------------------------------------------------------------------------

def test_a_cloudpc_worker_profile_keyed_profile_id_passes(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    profiles = {
        "worker.yaml": {
            "kind": "cloudpc_worker_profile",
            "profile_id": "cloudpc-worker-1",
            "tenant_kind": "pilot",
        },
    }
    repo = _materialize(tmp_path / "cloudpc-profile-id", _stack(), yaml_writer,
                        profiles=profiles)

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 0, result.stdout
    assert "profile.id missing" not in result.stdout
    assert "profile_id missing" not in result.stdout


def test_a_generic_profile_missing_profile_id_still_fails(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    profiles = {
        "worker.yaml": {
            "tenant_kind": "pilot",
        },
    }
    repo = _materialize(tmp_path / "generic-missing-id", _stack(), yaml_writer,
                        profiles=profiles)

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 1, result.stdout
    assert "ERROR: worker.yaml: profile.id missing" in result.stdout


def test_a_cloudpc_worker_profile_missing_profile_id_still_fails(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    """The kind filter narrows which field is required; it does not make the
    kind's own identifier optional."""
    profiles = {
        "worker.yaml": {
            "kind": "cloudpc_worker_profile",
            "tenant_kind": "pilot",
        },
    }
    repo = _materialize(tmp_path / "cloudpc-missing-id", _stack(), yaml_writer,
                        profiles=profiles)

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 1, result.stdout
    assert "ERROR: worker.yaml: profile_id missing" in result.stdout


def test_a_generic_profile_with_nested_id_is_unaffected(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    """Control: a kind absent from PROFILE_ID_KEY_KINDS — including no `kind:`
    at all — keeps validating exactly as before the fix."""
    profiles = {
        "worker.yaml": {
            "profile": {"id": "generic-profile-1", "tenant_kind": "pilot"},
        },
    }
    repo = _materialize(tmp_path / "generic-nested-id", _stack(), yaml_writer,
                        profiles=profiles)

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 0, result.stdout
    assert "profile.id missing" not in result.stdout


def test_a_non_registered_kind_does_not_accept_a_flat_profile_id(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    """A profile declaring a `kind:` outside PROFILE_ID_KEY_KINDS (unlike the
    no-`kind:`-at-all case above) must still require nested `profile.id`: a
    flat `profile_id` is not a silently-accepted alternate spelling for every
    kind, only for the ones explicitly registered (Copilot, PR #989)."""
    profiles = {
        "worker.yaml": {
            "kind": "some_other_profile_kind",
            "profile_id": "should-not-count",
            "tenant_kind": "pilot",
        },
    }
    repo = _materialize(tmp_path / "unregistered-kind-flat-profile-id", _stack(),
                        yaml_writer, profiles=profiles)

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 1, result.stdout
    assert "ERROR: worker.yaml: profile.id missing" in result.stdout


def test_a_cloudpc_worker_profile_with_a_mixed_nested_profile_block_still_resolves(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    """`profile_id` may sit at the document top level even when a nested
    `profile:` block also exists for other fields; the top-level value must
    not be shadowed by the nested mapping's absence of its own `profile_id`
    (Copilot, PR #989)."""
    profiles = {
        "worker.yaml": {
            "kind": "cloudpc_worker_profile",
            "profile_id": "cloudpc-worker-mixed",
            "profile": {"tenant_kind": "pilot"},
        },
    }
    repo = _materialize(tmp_path / "cloudpc-mixed-shape", _stack(), yaml_writer,
                        profiles=profiles)

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 0, result.stdout
    assert "profile_id missing" not in result.stdout


def test_a_cloudpc_worker_profile_with_profile_id_fully_nested_passes(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    """The other half of the fallback: `profile_id` nested entirely under
    `profile:` (no top-level `profile_id` at all) must still resolve via
    `prof.get("profile_id")` (Copilot, PR #989)."""
    profiles = {
        "worker.yaml": {
            "kind": "cloudpc_worker_profile",
            "profile": {"profile_id": "cloudpc-worker-nested", "tenant_kind": "pilot"},
        },
    }
    repo = _materialize(tmp_path / "cloudpc-nested-profile-id", _stack(), yaml_writer,
                        profiles=profiles)

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 0, result.stdout
    assert "profile_id missing" not in result.stdout


def test_a_non_string_kind_is_reported_not_crashed_on(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    """A malformed profile with an unhashable top-level `kind` (a list or
    mapping) must fail the membership test safely rather than raise
    `TypeError` and abort the whole validation run (Copilot, PR #989)."""
    profiles = {
        "worker.yaml": {
            "kind": ["not", "a", "string"],
            "tenant_kind": "pilot",
        },
    }
    repo = _materialize(tmp_path / "non-string-kind", _stack(), yaml_writer,
                        profiles=profiles)

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 1, result.stdout + result.stderr
    assert "Traceback" not in result.stdout + result.stderr
    assert "ERROR: worker.yaml: profile.id missing" in result.stdout
