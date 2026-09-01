"""THE TWO contract-v3.0 RETIREMENTS, MEASURED IN BOTH DIRECTIONS.

Realization of `retire-hermes-flat-keys-and-openworkflow-tokens` §§ 2.1-2.5
(ratified 2026-09-01, PR #551 squash `59eb913e`; entries 1 and 2 of
openxFactory issue #522).

The fallback branch had NO coverage before this file: `LEGACY_HERMES_KEYS`
appeared nowhere outside the validator, which is part of why nobody noticed the
warning had been dead code for the entire supported population. So the coverage
lands WITH the removal rather than after it, and it is written in both
directions on purpose.

WHY A `layers`-LESS STACK IS TESTED FOR A FINDING RATHER THAN FOR SILENCE. The
`hermes.layers missing required role` errors sit INSIDE the branch taken when
`hermes.layers` IS declared. Delete the `else` arm and nothing else and a
`layers`-less stack falls straight through to an EMPTY layer map, producing no
finding at all — a silent WIDENING at a major, the exact opposite of the
retirement. The removal is therefore a REPLACEMENT: one explicit error naming
the missing or non-list `hermes.layers`, and
`test_a_layers_less_stack_is_REFUSED_and_not_silently_widened` is the assertion
that keeps it one.

WHY THE REFUSAL LIST IS BY PATH AND NOT BY NAME. `domain_overlay` is ALSO a
live, non-deprecated key under `omnigent:` — every supported consumer declares
it and the validator reads it. The deprecated key is `hermes.domain_overlay`
and nothing else, and
`test_omnigent_domain_overlay_is_a_live_key_and_is_still_required` is why a
later sweep by key name cannot quietly refuse it.

WHY THE `openworkflow` REMOVAL MOVES TWO CASES IN OPPOSITE DIRECTIONS. The
removed branch was an `if` that PRECEDED the general `elif token not in
allowed`, so it shadowed it: any token beginning `openworkflow` took it,
including one that resolved perfectly well to a declared layer. Removing it
narrows the unresolvable case and WIDENS the resolvable one, and both are
asserted here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
COMMIT = "0" * 40

DEPRECATED_HERMES_FLAT_KEYS = (
    # the nine `LEGACY_HERMES_KEYS` carried
    "subject_overlay",
    "subject_layer_name",
    "customer_overlay",
    "customer_layer_name",
    "client_overlay",
    "client_layer_name",
    "care_organization_overlay",
    "domain_overlay",
    "domain_layer_name",
    # the three the starter emitted that appeared in neither list
    "domain_agent_mixes",
    "client_agent_mixes_template",
    "customer_agent_mixes_template",
)

CANONICAL_LAYERS = [
    {"role": "customer", "display_name": "Customer Hermes",
     "overlay": "overlays/customer"},
    {"role": "client", "display_name": "Client Hermes",
     "overlay": "overlays/client"},
    {"role": "domain", "display_name": "Domain Hermes",
     "overlay": "overlays/domain"},
]

CO_RESIDENT_FLAT_KEYS = {
    "domain_layer_name": "Domain Hermes",
    "domain_overlay": "overlays/domain",
    "client_layer_name": "Client Hermes",
    "client_overlay": "overlays/client",
    "customer_layer_name": "Customer Hermes",
    "customer_overlay": "overlays/customer",
    "subject_layer_name": "Customer Hermes",
    "subject_overlay": "overlays/customer",
    "care_organization_overlay": "overlays/client",
}


def _stack(hermes: dict, omnigent: dict | None = None) -> dict:
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
        "hermes": hermes,
        "tenancy": {
            "tenant_kinds": ["pilot"],
            "isolation": {"pilot": "per_tenant"},
        },
        "omnigent": {"domain_overlay": "omnigent"} if omnigent is None else omnigent,
    }


def _materialize(repo: Path, stack: dict, yaml_writer, *, gates=None) -> Path:
    yaml_writer(repo / "stack.yaml", stack)
    for relative in ("overlays/customer", "overlays/client", "overlays/domain"):
        yaml_writer(repo / relative / "agent.yaml", {"schema_version": 1})
    (repo / "omnigent").mkdir(parents=True, exist_ok=True)
    if gates is not None:
        yaml_writer(
            repo / "workflows" / "probe.yaml",
            {"workflow": {"id": "probe_workflow", "gates": gates}},
        )
    return repo


def _run(command_runner, repo_root: Path, repo: Path):
    return command_runner(
        [sys.executable, repo_root / "scripts/validate-domain-factory.py",
         repo, "--no-secret-scan"],
        cwd=repo_root,
    )


def _gate(owner_layer: str) -> dict:
    return {"id": "probe_gate", "owner_layer": owner_layer,
            "requires": ["probe_requirement"]}


def _findings(result) -> list[str]:
    """Every ERROR/WARN line, so "no NEW finding" is measured against a
    baseline rather than asserted as "no finding at all" — the synthetic
    fixtures carry unrelated scaffold warnings and always did."""
    return [line for line in result.stdout.splitlines()
            if line.startswith(("ERROR:", "WARN:"))]


# --------------------------------------------------------------------------
# Entry 1 — the `hermes` flat-key FALLBACK READ
# --------------------------------------------------------------------------

def test_a_layers_declaring_stack_validates_exactly_as_before(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    """The removal refuses nobody: all five supported consumers declare
    `hermes.layers`, so none exercises the removed fallback."""
    repo = _materialize(tmp_path / "layers-declared",
                        _stack({"layers": CANONICAL_LAYERS}), yaml_writer)

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 0, result.stdout
    assert "0 error(s)" in result.stdout
    assert "hermes.layers" not in result.stdout
    assert "legacy flat keys" not in result.stdout


def test_a_layers_less_stack_is_REFUSED_and_not_silently_widened(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    """The replacement, not the deletion.

    At the prior bundle this stack produced a legacy-flat-keys WARNING and
    resolved through the fallback. At contract-v3.0 it is REFUSED — and the
    thing this test exists to forbid is the third outcome, silence.
    """
    repo = _materialize(tmp_path / "layers-less",
                        _stack(dict(CO_RESIDENT_FLAT_KEYS)), yaml_writer)

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 1, result.stdout
    assert ("ERROR: stack.yaml: hermes.layers is missing or is not a list"
            in result.stdout)
    # the finding is an ERROR, not the warning the fallback used to emit
    assert "legacy flat keys" not in result.stdout
    assert "no overlay resolvable for hermes role" not in result.stdout


@pytest.mark.parametrize("declared", [None, {}, "layers", 3])
def test_every_non_list_hermes_layers_shape_reaches_the_same_refusal(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner, declared,
) -> None:
    """`missing OR non-list` — the error names both, so no shape falls through
    to an empty layer map."""
    hermes: dict = {} if declared is None else {"layers": declared}
    repo = _materialize(tmp_path / f"non-list-{type(declared).__name__}",
                        _stack(hermes), yaml_writer)

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 1, result.stdout
    assert ("ERROR: stack.yaml: hermes.layers is missing or is not a list"
            in result.stdout)


def test_a_co_resident_stack_still_validates_with_no_new_warning(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    """Entry 1's REFUSING half is not taken.

    All five supported consumers carry flat keys ALONGSIDE `hermes.layers`.
    That shape has never produced a warning against any of them — the warning
    sat in the `else` arm taken only when `layers` was absent — so refusing it
    would be an unphased narrowing. It stays accepted, and silently.
    """
    plain = _materialize(tmp_path / "plain", _stack({"layers": CANONICAL_LAYERS}),
                         yaml_writer)
    hermes = {"layers": CANONICAL_LAYERS, **CO_RESIDENT_FLAT_KEYS}
    repo = _materialize(tmp_path / "co-resident", _stack(hermes), yaml_writer)

    baseline = _run(command_runner, repo_root, plain)
    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 0, result.stdout
    # the co-resident keys add NOTHING: not an error, not a warning
    assert _findings(result) == _findings(baseline)
    for key in DEPRECATED_HERMES_FLAT_KEYS:
        assert key not in result.stdout


def test_omnigent_domain_overlay_is_a_live_key_and_is_still_required(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    """The refusal list is by PATH. `hermes.domain_overlay` is the deprecated
    key; `omnigent.domain_overlay` is a live one every supported consumer
    declares, and dropping it is still an error."""
    hermes = {"layers": CANONICAL_LAYERS, "domain_overlay": "overlays/domain"}
    repo = _materialize(tmp_path / "omnigent-dropped",
                        _stack(hermes, omnigent={}), yaml_writer)

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 1, result.stdout
    assert "ERROR: omnigent domain_overlay dir missing" in result.stdout
    # ... and the co-resident `hermes.domain_overlay` drew no finding of its own
    assert "hermes.domain_overlay" not in result.stdout


# --------------------------------------------------------------------------
# Entry 2 — the `openworkflow`-prefixed token compatibility branch
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "token", ["openworkflow_legacy", "openworkflow", "openworkflowx",
              "openworkflow-legacy"])
def test_an_unresolvable_openworkflow_token_falls_to_the_general_rule(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner, token,
) -> None:
    """The NARROWING half, over the prefix the code actually matched.

    The policy entry and the validator docstring both declared the shape as
    `openworkflow_`, with a trailing underscore; the removed code wrote
    `token.startswith("openworkflow")`, with none. All four of these tokens
    took the compatibility branch, and all four are refused by the removal —
    which is why the entry is corrected to the prefix the code matched before
    the row moves.
    """
    repo = _materialize(tmp_path / f"unresolvable-{token}",
                        _stack({"layers": CANONICAL_LAYERS}), yaml_writer,
                        gates=[_gate(token)])

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 1, result.stdout
    assert "does not resolve to a declared layer" in result.stdout
    assert "deprecated openWorkflow naming" not in result.stdout


def test_a_RESOLVABLE_openworkflow_token_now_validates_silently(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    """The WIDENING half, stated rather than discovered.

    The removed branch was an `if` preceding the general `elif`, so it shadowed
    it: a token beginning `openworkflow` was warned even when it resolved to a
    declared layer. Measured on the pre-removal validator, this fixture emitted
    `WARN: ... uses deprecated openWorkflow naming`; it is silent now.
    """
    layers = [dict(layer) for layer in CANONICAL_LAYERS]
    layers[2]["display_name"] = "OpenWorkflow Domain Hermes"
    repo = _materialize(tmp_path / "resolvable-openworkflow",
                        _stack({"layers": layers}), yaml_writer,
                        gates=[_gate("OpenWorkflow Domain Hermes")])
    control = _materialize(tmp_path / "resolvable-control",
                           _stack({"layers": CANONICAL_LAYERS}), yaml_writer,
                           gates=[_gate("Domain Hermes")])

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 0, result.stdout
    # indistinguishable from a gate naming an ordinary declared layer
    assert _findings(result) == _findings(_run(command_runner, repo_root, control))
    assert "probe_gate" not in result.stdout
    assert "openWorkflow" not in result.stdout


def test_the_replacement_token_xfactory_is_unchanged_by_the_removal(
    tmp_path: Path, repo_root: Path, yaml_writer, command_runner,
) -> None:
    repo = _materialize(tmp_path / "xfactory-token",
                        _stack({"layers": CANONICAL_LAYERS}), yaml_writer,
                        gates=[_gate("xfactory")])

    result = _run(command_runner, repo_root, repo)

    assert result.returncode == 0, result.stdout
    assert "probe_gate" not in result.stdout


# --------------------------------------------------------------------------
# The surfaces themselves — neither retirement may quietly return
# --------------------------------------------------------------------------

def test_neither_retired_surface_survives_in_the_validator(
    repo_root: Path,
) -> None:
    """A removal that a later edit re-adds is not a removal.

    Both entries were removed at contract-v3.0 and both entries' Executed rows
    say so; the source is the thing those rows describe.
    """
    source = (repo_root / "scripts/validate-domain-factory.py").read_text(
        encoding="utf-8")

    assert "LEGACY_HERMES_KEYS" not in source
    assert "uses legacy flat keys" not in source
    assert "no overlay resolvable for hermes role" not in source
    assert 'startswith("openworkflow")' not in source
    assert "deprecated openWorkflow naming" not in source
    assert '"openworkflow_*" tokens' not in source
    # the live key keeps its reader
    assert "omnigent domain_overlay dir missing" in source


# --------------------------------------------------------------------------
# The generator stops EMITTING the deprecated shape
# --------------------------------------------------------------------------

@pytest.fixture(scope="module")
def scaffolded_stack(tmp_path_factory):
    """A repository generated by the REAL starter, read as bytes.

    An already-generated repository is NOT edited by this change — nothing
    refuses what it carries. What changes is what a NEW one is born with.
    """
    import subprocess

    target = tmp_path_factory.mktemp("retirement-scaffold") / "probex"
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/apply-domain-starter.py"),
         str(target), "--domain-id", "probex", "--product-name", "ProbexFactory"],
        capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    return target


def test_a_newly_scaffolded_stack_carries_no_deprecated_flat_key(
    scaffolded_stack: Path,
) -> None:
    text = (scaffolded_stack / "stack.yaml").read_text(encoding="utf-8")
    hermes = yaml.safe_load(text)["hermes"]

    assert list(hermes) == ["layers"]
    for key in DEPRECATED_HERMES_FLAT_KEYS:
        assert key not in hermes
    # the live key under `omnigent:` is untouched
    assert yaml.safe_load(text)["omnigent"]["domain_overlay"] == "omnigent"


def test_a_newly_scaffolded_stack_names_no_spent_removal_target(
    scaffolded_stack: Path,
) -> None:
    """The generator carried `# Deprecated flat keys (removal at
    contract-v2.0); kept for older tooling.` — openxFactory's own generator
    writing the deprecated shape into every new domain, under a target that was
    already one major and five minors in the past."""
    text = (scaffolded_stack / "stack.yaml").read_text(encoding="utf-8")

    assert "Deprecated flat keys" not in text
    assert "removal at contract-v2.0" not in text


def test_the_scaffolded_repo_does_not_REQUIRE_what_it_no_longer_writes(
    scaffolded_stack: Path,
) -> None:
    """The generator writes three artifacts that named the flat keys, not one.

    Its `schemas/stack.schema.yaml` listed six of them under `required_paths`
    and its generated local validator resolved overlay directories through
    them. A generated repository that requires paths its own generated
    `stack.yaml` does not carry is self-contradicting on day one, so both move
    with the template.
    """
    schema = yaml.safe_load(
        (scaffolded_stack / "schemas/stack.schema.yaml").read_text(encoding="utf-8"))
    required = schema["schema"]["required_paths"]

    assert "hermes.layers" in required
    assert "omnigent.domain_overlay" in required
    for key in DEPRECATED_HERMES_FLAT_KEYS:
        assert f"hermes.{key}" not in required

    stack = yaml.safe_load(
        (scaffolded_stack / "stack.yaml").read_text(encoding="utf-8"))
    for dotted in required:
        cursor = stack
        for part in dotted.split("."):
            assert isinstance(cursor, dict) and part in cursor, dotted
            cursor = cursor[part]
        assert cursor not in (None, "", [])


def test_the_scaffolded_repo_still_passes_its_own_generated_validator(
    scaffolded_stack: Path, command_runner,
) -> None:
    result = command_runner(
        [sys.executable, scaffolded_stack / "scripts/validate-domain-factory.py"],
        cwd=scaffolded_stack,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_the_scaffolded_repo_passes_the_CANONICAL_validator_at_the_major(
    scaffolded_stack: Path, repo_root: Path, command_runner,
) -> None:
    """The generated `stack.yaml` declares `hermes.layers`, so it meets the
    post-removal validator on the accepting side of the retirement."""
    result = _run(command_runner, repo_root, scaffolded_stack)

    assert result.returncode == 0, result.stdout
    assert "0 error(s)" in result.stdout
    assert "hermes.layers is missing" not in result.stdout
