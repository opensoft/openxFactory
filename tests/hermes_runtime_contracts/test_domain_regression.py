"""Contracts for the supported-Domain regression denominator (T067, T072, T073).

Every check uses SYNTHETIC Git repositories only -- the real xFactories
checkouts are never read or modified. The realized inventory is asserted
value-for-value against the pinned research-Decision-12 table.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from scripts.hermes_runtime_validation.content import resolve_git_object
from scripts.hermes_runtime_validation.domain_regression import (
    DomainRegressionDependencyError,
    build_repository_resolver,
    validate_domain_regression,
)
from scripts.hermes_runtime_validation.fixtures import validate_index
from scripts.hermes_runtime_validation.loader import load_yaml_document
from tests.hermes_runtime_contracts.support import (
    commit_files,
    finding_codes,
    init_git_repo,
    run_command,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
FAMILY_ROOT = REPOSITORY_ROOT / "contracts/hermes-runtime"
FIXTURE_ROOT = FAMILY_ROOT / "fixtures"
REGRESSION_DIR = FIXTURE_ROOT / "regression"
REALIZED_INVENTORY_PATH = FIXTURE_ROOT / "domain-regression-inventory.yaml"
SCHEMA_PATH = FAMILY_ROOT / "domain-regression-inventory.schema.yaml"
SHARED_DEFINITIONS_PATH = FAMILY_ROOT / "shared-definitions.schema.yaml"

BASE = "https://xforge.us/schemas/openxfactory/hermes-runtime/v2/"
META = "https://json-schema.org/draft/2020-12/schema"
INVENTORY_KIND = "openxfactory-hermes-runtime-domain-regression-inventory"
PORTABLE_KIND = "openxfactory-hermes-runtime-portable-evidence-fixture"
CANONICAL_CONTRACT_REF = "3d51c3ed5854d112bcc049e1ef7f70863b993fa3"

# The exact ratified research-Decision-12 / SIC section 4 denominator table
# (repository, published commit, raw-blob stack_digest, domain id), bytewise
# sorted by repository. Every row pins openxFactory commit 3d51c3ed..., schema
# version 1, stack path stack.yaml, and an expected pass.
PINNED_TABLE: tuple[tuple[str, str, str, str], ...] = (
    (
        "codeXfactory/codexFactory",
        "7bfa492f700de29cdeab31dc899420745546d982",
        "sha256:06f88e192bfd17d42ea6519072e472b9f6d028d88ab0985065640e37c9719722",
        "codex",
    ),
    (
        "opensoft/AdxFactory",
        "d0e42622d1da51a3aa6475e2df076df4e55e7918",
        "sha256:b5ab723eac7395523a7988468076048e4d0426e03b556231dfb4c282bb8b3fc9",
        "adx",
    ),
    (
        "opensoft/LedgerxFactory",
        "1b2ca4c1e66b5e90c9e983a7d0aad11c1ab5ae1c",
        "sha256:85d67c54a07f3d4e31943257cf43cb19e0fc400f39a0c719591ed30eeb140ab9",
        "ledgerx",
    ),
    (
        "opensoft/MedxFactory",
        "280fdbb5aee8cd83f5c75defd652c1a60039cd0e",
        "sha256:02e4b34528217870e982462dde4ff8624c29a7b9e61f3ab405f4710307ff6622",
        "medx",
    ),
    (
        "opensoft/OpsxFactory",
        "beed3481fb7f500695bcc4394bb686fab125ad71",
        "sha256:3de89a6c7e8b9f112deb7074b8798dc17311425f819968f2f7e1c7e86c7e8fa0",
        "opsx",
    ),
)

NEGATIVE_FIXTURES: dict[str, str] = {
    "regression-duplicate-repository": "duplicate-repository.yaml",
    "regression-missing-exclusion-reason": "missing-exclusion-reason.yaml",
    "regression-digest-mismatch": "digest-mismatch.yaml",
}
NEGATIVE_PRIMARY_CODES: dict[str, str] = {
    "regression-duplicate-repository": "HGR-REGRESSION-DUPLICATE-REPOSITORY",
    "regression-missing-exclusion-reason": "HGR-REGRESSION-MISSING-EXCLUSION-REASON",
    "regression-digest-mismatch": "HGR-REGRESSION-DIGEST-MISMATCH",
}


def _validator() -> Draft202012Validator:
    schema = load_yaml_document(SCHEMA_PATH)
    shared = load_yaml_document(SHARED_DEFINITIONS_PATH)
    registry: Registry = Registry().with_resources(
        [
            (
                schema["$id"],
                Resource.from_contents(schema, default_specification=DRAFT202012),
            ),
            (
                shared["$id"],
                Resource.from_contents(shared, default_specification=DRAFT202012),
            ),
        ]
    )
    return Draft202012Validator(
        schema, registry=registry, format_checker=FormatChecker()
    )


def _synthetic_stack_text(
    *,
    contract_ref: str = CANONICAL_CONTRACT_REF,
    contract_schema_version: int = 1,
    extra_customer: bool = False,
) -> str:
    layers = [
        {"role": "customer", "display_name": "Customer", "overlay": "hermes/customer"},
        {"role": "client", "display_name": "Client", "overlay": "hermes/client"},
        {"role": "domain", "display_name": "Domain", "overlay": "hermes/domain"},
    ]
    if extra_customer:
        layers.append(
            {
                "role": "customer",
                "display_name": "Second Customer",
                "overlay": "hermes/customer-two",
            }
        )
    document = {
        "schema_version": 1,
        "kind": "xfactory_domain_stack",
        "domain": {
            "id": "synthetic",
            "product_name": "Synthetic",
            "display_name": "Synthetic Domain Factory",
            "category": "engineering",
        },
        "xfactory": {
            "contract_name": "openxFactory",
            "contract_ref_type": "commit",
            "contract_ref": contract_ref,
            "contract_schema_version": contract_schema_version,
        },
        "hermes": {"layers": layers},
    }
    return yaml.safe_dump(document, sort_keys=False, allow_unicode=False)


def _build_repo(root: Path, repository: str, stack_text: str) -> tuple[Path, str, str]:
    owner, name = repository.split("/", 1)
    repo = init_git_repo(root / owner / name)
    commit = commit_files(repo, {"stack.yaml": stack_text}, message="synthetic stack")
    resolved = resolve_git_object(repo, commit, "stack.yaml")
    return repo, commit, resolved.digest


def _build_denominator(
    tmp_path: Path, *, stack_text: str | None = None
) -> tuple[dict[str, Any], Path, dict[str, Path]]:
    checkouts = tmp_path / "checkouts"
    text = _synthetic_stack_text() if stack_text is None else stack_text
    repos: dict[str, Path] = {}
    entries: list[dict[str, Any]] = []
    for repository, _commit, _digest, domain_id in PINNED_TABLE:
        repo, commit, digest = _build_repo(checkouts, repository, text)
        repos[repository] = repo
        entries.append(
            {
                "repository": repository,
                "commit": commit,
                "stack_path": "stack.yaml",
                "stack_digest": digest,
                "domain_id": domain_id,
                "expected_contract_ref": CANONICAL_CONTRACT_REF,
                "expected_contract_schema_version": 1,
                "expected_result": "pass",
            }
        )
    inventory = {
        "schema_version": 1,
        "kind": INVENTORY_KIND,
        "inventory_version": 1,
        "entries": entries,
        "exclusions": [
            {
                "repository": "opensoft/LegalxFactory",
                "reason": "no canonical stack.yaml yet",
                "evidence": "research Decision 12",
            }
        ],
    }
    return inventory, checkouts, repos


def _materialize_scenario(
    tmp_path: Path, fixture: dict[str, Any]
) -> tuple[dict[str, Any], Any]:
    scenario = fixture["scenario"]
    stack_text = scenario["stack_content_utf8"]
    corrupt = set(scenario.get("corrupt_digest_repositories", []))
    inventory = deepcopy(fixture["inventory"])
    checkouts = tmp_path / "checkouts"
    mappings: dict[str, Path] = {}
    for entry in inventory["entries"]:
        repository = entry["repository"]
        repo, commit, digest = _build_repo(checkouts, repository, stack_text)
        entry["commit"] = commit
        if repository not in corrupt:
            entry["stack_digest"] = digest
        mappings[repository] = repo
    return inventory, build_repository_resolver(mappings, None)


class _RaisingResolver:
    """A resolver double that fails if any object resolution is attempted."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def __call__(self, repository: str) -> Path:
        self.calls.append(repository)
        raise DomainRegressionDependencyError("resolver must not be reached")


# --------------------------------------------------------------------------- #
# Realized inventory: value-for-value against the pinned table
# --------------------------------------------------------------------------- #


def test_realized_inventory_matches_the_pinned_table_value_for_value() -> None:
    inventory = load_yaml_document(REALIZED_INVENTORY_PATH)
    assert inventory["schema_version"] == 1
    assert inventory["kind"] == INVENTORY_KIND
    assert inventory["inventory_version"] == 1

    entries = inventory["entries"]
    assert len(entries) == len(PINNED_TABLE) == 5
    for entry, (repository, commit, digest, domain_id) in zip(entries, PINNED_TABLE):
        assert entry == {
            "repository": repository,
            "commit": commit,
            "stack_path": "stack.yaml",
            "stack_digest": digest,
            "domain_id": domain_id,
            "expected_contract_ref": CANONICAL_CONTRACT_REF,
            "expected_contract_schema_version": 1,
            "expected_result": "pass",
        }

    repositories = [entry["repository"] for entry in entries]
    assert repositories == sorted(repositories, key=lambda value: value.encode("utf-8"))
    assert len(set(repositories)) == len(repositories)

    assert inventory["exclusions"] == [
        {
            "repository": "opensoft/LegalxFactory",
            "reason": "no canonical stack.yaml yet",
            "evidence": "specs/005-customer-subject-runtime/research.md Decision 12",
        }
    ]


def test_realized_inventory_satisfies_the_closed_schema() -> None:
    assert _validator().is_valid(load_yaml_document(REALIZED_INVENTORY_PATH))


# --------------------------------------------------------------------------- #
# Schema annotations and structural negatives
# --------------------------------------------------------------------------- #


def test_schema_annotations_are_canonical() -> None:
    schema = load_yaml_document(SCHEMA_PATH)
    assert schema["schema_version"] == 1
    assert schema["kind"] == "openxfactory-hermes-runtime-contract-schema"
    assert schema["$schema"] == META
    assert schema["$id"] == BASE + "domain-regression-inventory.schema.yaml"
    assert schema["contract_id"] == "domain-regression-inventory"
    assert schema["contract_schema_version"] == 1
    Draft202012Validator.check_schema(schema)

    assert schema["properties"]["schema_version"] == {"const": 1}
    assert schema["properties"]["kind"] == {"const": INVENTORY_KIND}
    assert schema["properties"]["entries"]["minItems"] == 5
    assert schema["properties"]["exclusions"]["minItems"] == 1

    def assert_closed(node: object, location: str) -> None:
        if isinstance(node, dict):
            if node.get("type") == "object":
                assert node.get("additionalProperties") is False, f"{location} is open"
            for key, value in node.items():
                assert_closed(value, f"{location}/{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                assert_closed(value, f"{location}/{index}")

    assert_closed(schema, "$")


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(lambda inv: inv["entries"].pop(), id="fewer-than-five-entries"),
        pytest.param(lambda inv: inv.pop("exclusions"), id="missing-exclusions"),
        pytest.param(
            lambda inv: inv["exclusions"][0].pop("reason"), id="exclusion-no-reason"
        ),
        pytest.param(
            lambda inv: inv["exclusions"][0].pop("evidence"), id="exclusion-no-evidence"
        ),
        pytest.param(
            lambda inv: inv["entries"][0].pop("expected_result"),
            id="entry-missing-result",
        ),
        pytest.param(
            lambda inv: inv["entries"][0].__setitem__("expected_result", "fail"),
            id="entry-result-not-pass",
        ),
        pytest.param(
            lambda inv: inv["entries"][0].__setitem__("stack_digest", "not-a-digest"),
            id="entry-bad-digest",
        ),
        pytest.param(
            lambda inv: inv["entries"][0].__setitem__(
                "expected_contract_schema_version", 0
            ),
            id="entry-bad-schema-version",
        ),
        pytest.param(
            lambda inv: inv["entries"][0].__setitem__("commit", "XYZ"),
            id="entry-bad-commit",
        ),
        pytest.param(lambda inv: inv.__setitem__("kind", "wrong-kind"), id="bad-kind"),
        pytest.param(
            lambda inv: inv.__setitem__("unexpected", True), id="extra-top-level"
        ),
        pytest.param(
            lambda inv: inv["entries"][0].__setitem__("surprise", 1),
            id="extra-entry-field",
        ),
    ],
)
def test_schema_rejects_malformed_inventories(mutate: Any) -> None:
    inventory = load_yaml_document(REALIZED_INVENTORY_PATH)
    mutate(inventory)
    assert not _validator().is_valid(inventory)


def test_schema_accepts_wellformed_but_semantically_defective_fixtures() -> None:
    for case_id in ("regression-duplicate-repository", "regression-digest-mismatch"):
        inventory = load_yaml_document(REGRESSION_DIR / NEGATIVE_FIXTURES[case_id])[
            "inventory"
        ]
        assert _validator().is_valid(inventory), case_id


def test_schema_rejects_missing_exclusion_reason_fixture() -> None:
    inventory = load_yaml_document(
        REGRESSION_DIR / NEGATIVE_FIXTURES["regression-missing-exclusion-reason"]
    )["inventory"]
    assert not _validator().is_valid(inventory)


# --------------------------------------------------------------------------- #
# Resolver root-resolution rules
# --------------------------------------------------------------------------- #


def test_repository_resolver_deterministic_root_rules(tmp_path: Path) -> None:
    root = tmp_path / "mirrors"
    plain = root / "opensoft" / "AdxFactory"
    plain.mkdir(parents=True)

    resolver = build_repository_resolver(None, root)
    assert resolver("opensoft/AdxFactory") == plain

    bare = root / "opensoft" / "AdxFactory.git"
    bare.mkdir()
    with pytest.raises(DomainRegressionDependencyError):
        resolver("opensoft/AdxFactory")  # both plain and .git present -> ambiguous

    override = tmp_path / "explicit-checkout"
    override.mkdir()
    mapped = build_repository_resolver({"opensoft/AdxFactory": override}, root)
    assert mapped("opensoft/AdxFactory") == override  # explicit mapping wins

    with pytest.raises(DomainRegressionDependencyError):
        resolver("opensoft/absent-repository")  # missing
    with pytest.raises(DomainRegressionDependencyError):
        resolver("not-a-canonical-repository")  # not canonical
    with pytest.raises(DomainRegressionDependencyError):
        build_repository_resolver({"../escape": override}, None)  # bad mapping key
    with pytest.raises(DomainRegressionDependencyError):
        build_repository_resolver(None, None)("opensoft/AdxFactory")  # no source


def test_repository_resolver_resolves_a_bare_git_mirror(tmp_path: Path) -> None:
    root = tmp_path / "mirrors"
    bare = root / "codeXfactory" / "codexFactory.git"
    bare.mkdir(parents=True)
    resolver = build_repository_resolver(None, root)
    assert resolver("codeXfactory/codexFactory") == bare


# --------------------------------------------------------------------------- #
# Exact-object semantics: positive, dirty tree, missing object, determinism
# --------------------------------------------------------------------------- #


def test_wellformed_inventory_against_synthetic_repos_passes(tmp_path: Path) -> None:
    inventory, checkouts, _ = _build_denominator(tmp_path)
    resolver = build_repository_resolver(None, checkouts)
    assert validate_domain_regression(inventory, resolver=resolver) == []


def test_resolution_is_independent_of_a_dirty_working_tree(tmp_path: Path) -> None:
    inventory, checkouts, repos = _build_denominator(tmp_path)
    resolver = build_repository_resolver(None, checkouts)
    for repo in repos.values():
        (repo / "stack.yaml").write_text(
            "kind: dirtied-working-tree\n", encoding="utf-8"
        )
        (repo / "untracked.txt").write_text("junk\n", encoding="utf-8")
    # Exact commit:path objects are read; the dirtied worktree is ignored.
    assert validate_domain_regression(inventory, resolver=resolver) == []


@pytest.mark.parametrize("field", ["commit", "stack_path"])
def test_missing_exact_object_is_an_exit_two_dependency_error(
    tmp_path: Path, field: str
) -> None:
    inventory, checkouts, _ = _build_denominator(tmp_path)
    resolver = build_repository_resolver(None, checkouts)
    if field == "commit":
        inventory["entries"][0]["commit"] = "0" * 40
    else:
        inventory["entries"][0]["stack_path"] = "absent.yaml"

    with pytest.raises(DomainRegressionDependencyError) as caught:
        validate_domain_regression(inventory, resolver=resolver)

    assert caught.value.exit_code == 2
    assert caught.value.code == "HGR-REGRESSION-DEPENDENCY"


def test_deterministic_mirror_resolution_matches_the_checkout(tmp_path: Path) -> None:
    inventory, checkouts, repos = _build_denominator(tmp_path)
    checkout_resolver = build_repository_resolver(None, checkouts)

    mirror = tmp_path / "mirror"
    for repository, repo in repos.items():
        owner, name = repository.split("/", 1)
        destination = mirror / owner / f"{name}.git"
        destination.parent.mkdir(parents=True, exist_ok=True)
        run_command(
            ["git", "clone", "--quiet", "--bare", str(repo), str(destination)],
            cwd=tmp_path,
            check=True,
        )
    mirror_resolver = build_repository_resolver(None, mirror)

    checkout_findings = validate_domain_regression(
        inventory, resolver=checkout_resolver
    )
    mirror_findings = validate_domain_regression(inventory, resolver=mirror_resolver)
    assert checkout_findings == []
    assert checkout_findings == mirror_findings


# --------------------------------------------------------------------------- #
# Digest, contract-pin, and static-conformance parity
# --------------------------------------------------------------------------- #


def test_digest_mismatch_is_rejected(tmp_path: Path) -> None:
    inventory, checkouts, _ = _build_denominator(tmp_path)
    resolver = build_repository_resolver(None, checkouts)
    inventory["entries"][0]["stack_digest"] = "sha256:" + "0" * 64

    findings = validate_domain_regression(inventory, resolver=resolver)
    assert finding_codes(findings) == ["HGR-REGRESSION-DIGEST-MISMATCH"]


def test_contract_pin_mismatch_is_rejected(tmp_path: Path) -> None:
    inventory, checkouts, _ = _build_denominator(tmp_path)
    resolver = build_repository_resolver(None, checkouts)
    inventory["entries"][0]["expected_contract_ref"] = "0" * 40

    findings = validate_domain_regression(inventory, resolver=resolver)
    assert finding_codes(findings) == ["HGR-REGRESSION-CONTRACT-REF"]


def test_nonconformant_stack_fails_static_conformance(tmp_path: Path) -> None:
    # A stack that already declares two Customer roles must fail conformance --
    # the same defect the derived negative injects in memory.
    duplicate_stack = _synthetic_stack_text(extra_customer=True)
    inventory, checkouts, _ = _build_denominator(tmp_path, stack_text=duplicate_stack)
    resolver = build_repository_resolver(None, checkouts)

    findings = validate_domain_regression(inventory, resolver=resolver)
    assert set(finding_codes(findings)) == {"HGR-REGRESSION-STATIC-CONFORMANCE"}


def test_derived_negative_fires_when_conformance_wrongly_accepts_duplicate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # If static conformance were broken (always accepting), the in-memory
    # duplicate-Customer derived negative must catch it on every entry.
    import scripts.hermes_runtime_validation.domain_regression as module

    inventory, checkouts, _ = _build_denominator(tmp_path)
    resolver = build_repository_resolver(None, checkouts)
    monkeypatch.setattr(module, "_stack_is_conformant", lambda stack: True)

    findings = validate_domain_regression(inventory, resolver=resolver)
    assert set(finding_codes(findings)) == {"HGR-REGRESSION-DERIVED-NEGATIVE"}
    assert len(findings) == len(PINNED_TABLE)


# --------------------------------------------------------------------------- #
# Indexed negative fixtures
# --------------------------------------------------------------------------- #


def test_digest_mismatch_fixture_is_rejected(tmp_path: Path) -> None:
    fixture = load_yaml_document(
        REGRESSION_DIR / NEGATIVE_FIXTURES["regression-digest-mismatch"]
    )
    inventory, resolver = _materialize_scenario(tmp_path, fixture)

    findings = validate_domain_regression(inventory, resolver=resolver)
    assert finding_codes(findings) == ["HGR-REGRESSION-DIGEST-MISMATCH"]


@pytest.mark.parametrize(
    "case_id",
    ["regression-duplicate-repository", "regression-missing-exclusion-reason"],
)
def test_resolution_free_fixtures_fail_before_any_object_lookup(case_id: str) -> None:
    fixture = load_yaml_document(REGRESSION_DIR / NEGATIVE_FIXTURES[case_id])
    resolver = _RaisingResolver()

    findings = validate_domain_regression(fixture["inventory"], resolver=resolver)

    assert finding_codes(findings) == [NEGATIVE_PRIMARY_CODES[case_id]]
    assert resolver.calls == []


@pytest.mark.parametrize("case_id", sorted(NEGATIVE_FIXTURES))
def test_negative_fixture_self_description_is_consistent(case_id: str) -> None:
    fixture = load_yaml_document(REGRESSION_DIR / NEGATIVE_FIXTURES[case_id])
    assert fixture["schema_version"] == 1
    assert fixture["kind"] == PORTABLE_KIND
    assert fixture["case_id"] == case_id
    assert case_id.startswith("regression-")
    assert fixture["phase"] == "semantic"
    assert fixture["class"] == "invalid"
    assert fixture["evaluation_time"] == "2026-07-13T12:00:00Z"
    assert fixture["requirement_ids"] == ["HCS-006"]
    assert fixture["scenario_ids"] == ["HCS-006-S03"]

    expected = fixture["expected"]
    assert expected["outcome"] == "fail"
    assert expected["primary_finding_code"] == NEGATIVE_PRIMARY_CODES[case_id]
    assert expected["primary_finding_code"].startswith("HGR-REGRESSION-")
    assert expected["allowed_secondary_codes"] == []


def test_registered_regression_cases_pass_the_fixture_index_harness() -> None:
    # The exact cases returned to the coordinator (SIC section 7) must survive
    # the strict fixture-index structural gate, including self-description parity.
    cases = [
        {
            "case_id": "regression-inventory-realized",
            "phase": "semantic",
            "class": "valid",
            "requirement_ids": ["HCS-006"],
            "scenario_ids": ["HCS-006-S01"],
            "inputs": ["domain-regression-inventory.yaml"],
            "depends_on": [],
            "evaluation_time": "2026-07-13T12:00:00Z",
            "expected": {"outcome": "pass", "allowed_secondary_codes": []},
            "evidence_id": "EVIDENCE-FIXTURE-REGRESSION-INVENTORY-REALIZED",
        }
    ]
    for case_id, relative in sorted(NEGATIVE_FIXTURES.items()):
        cases.append(
            {
                "case_id": case_id,
                "phase": "semantic",
                "class": "invalid",
                "requirement_ids": ["HCS-006"],
                "scenario_ids": ["HCS-006-S03"],
                "inputs": [f"regression/{relative}"],
                "depends_on": [],
                "evaluation_time": "2026-07-13T12:00:00Z",
                "expected": {
                    "outcome": "fail",
                    "primary_finding_code": NEGATIVE_PRIMARY_CODES[case_id],
                    "allowed_secondary_codes": [],
                },
                "evidence_id": f"EVIDENCE-FIXTURE-{case_id.upper()}",
            }
        )
    index = {
        "schema_version": 1,
        "kind": "hermes-runtime-fixture-index",
        "cases": cases,
    }

    assert (
        validate_index(
            index, fixture_root=FIXTURE_ROOT, repository_root=REPOSITORY_ROOT
        )
        == []
    )
