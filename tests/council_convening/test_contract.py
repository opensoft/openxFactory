from __future__ import annotations

import pytest
from jsonschema import Draft202012Validator

from scripts.council_convening_validation.models import RelativePath
from scripts.council_convening_validation.yaml_io import load_yaml
from tests.council_convening.support import (
    ACCEPTANCE_MAP_PATH,
    FAMILY_ROOT,
    FIXTURE_ROOT,
    INDEX_PATH,
    REPOSITORY_ROOT,
    indexed_paths,
    load_index,
    load_schema,
    mapping_at,
    valid_convening,
    validation_keywords,
)


def test_contract_family_foundation_exists() -> None:
    # Given the planned neutral contract-family surface
    # When the foundation is inspected
    # Then its orientation and fixture catalog exist at canonical paths.
    assert (FAMILY_ROOT / "README.md").is_file()
    assert INDEX_PATH.is_file()


def test_fixture_index_has_explicit_schema_metadata() -> None:
    # Given the canonical fixture index
    # When its envelope is loaded
    # Then its version, kind, and ordered case collection are explicit.
    document = load_index()

    assert document.schema_version == 1
    assert document.kind == "council-convening-fixture-index"
    assert document.contract_version == 1
    assert isinstance(document.cases, tuple)


def test_fixture_index_case_ids_and_paths_are_unique() -> None:
    # Given every indexed fixture case
    # When identifiers and paths are compared
    # Then neither address is ambiguous.
    cases = load_index().cases
    case_ids = [case.case_id for case in cases]
    case_paths = [case.path for case in cases]

    assert len(case_ids) == len(set(case_ids))
    assert len(case_paths) == len(set(case_paths))


def test_fixture_paths_are_repository_relative_and_contained() -> None:
    # Given every path named by the fixture index
    # When each path is resolved from the repository root
    # Then it remains beneath the council-convening fixture directory.
    for relative_path in indexed_paths(load_index()):
        assert not relative_path.is_absolute()
        resolved = (REPOSITORY_ROOT / relative_path).resolve()
        assert resolved.is_relative_to(FIXTURE_ROOT.resolve())
        assert resolved.is_file()


def test_fixture_index_has_exact_yaml_file_parity() -> None:
    # Given the index and the packaged fixture tree
    # When their repository-relative paths are compared
    # Then every fixture is indexed exactly once and no index path is missing.
    indexed = set(indexed_paths(load_index()))
    packaged = {
        path.relative_to(REPOSITORY_ROOT)
        for path in FIXTURE_ROOT.rglob("*.yaml")
        if path != INDEX_PATH
    }

    assert indexed == packaged


def test_all_indexed_yaml_records_have_required_metadata() -> None:
    records = (
        ACCEPTANCE_MAP_PATH,
        INDEX_PATH,
        *(REPOSITORY_ROOT / path for path in indexed_paths(load_index())),
    )

    assert len(records) == 16
    for path in records:
        relative_path = RelativePath(path.relative_to(REPOSITORY_ROOT).as_posix())
        document = load_yaml(path, relative_path)

        assert document["schema_version"] == 1
        assert isinstance(document["kind"], str) and document["kind"]


def test_indexed_cases_have_stable_expected_result_fields() -> None:
    # Given an indexed positive or negative case
    # When its expected result is inspected
    # Then accept cases name no finding and refusals name one stable code.
    for case in load_index().cases:
        assert case.case_class in {"positive", "negative"}
        assert case.expected_outcome in {"accept", "refuse"}
        if case.expected_outcome == "accept":
            assert case.expected_primary_finding is None
        else:
            finding = case.expected_primary_finding
            assert isinstance(finding, str) and finding


def test_resolved_convening_schema_is_valid_draft_2020_12() -> None:
    # Given the canonical resolved-convening schema
    schema = load_schema()

    # When its declared dialect and meta-schema are checked
    Draft202012Validator.check_schema(schema)

    # Then it is explicitly a Draft 2020-12 machine contract.
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"


def test_resolved_convening_schema_closes_every_object_boundary() -> None:
    # Given valid documents with one unexpected field at each object boundary
    object_paths = (
        (),
        ("required_seats_provenance",),
        ("required_seats_provenance", "candidate"),
        ("required_seats_provenance", "governed_rule"),
        ("required_seats_provenance", "resolution"),
    )

    # When each document is validated
    for path in object_paths:
        document = valid_convening()
        mapping_at(document, *path)["unexpected"] = True

        # Then the exact boundary rejects the unknown field.
        assert validation_keywords(document) & {
            "additionalProperties",
            "unevaluatedProperties",
        }
    document = valid_convening()
    resolution = mapping_at(document, "required_seats_provenance", "resolution")
    evaluations = resolution["conditional_seats"]
    assert isinstance(evaluations, list)
    evaluation = evaluations[0]
    assert isinstance(evaluation, dict)
    evaluation["unexpected"] = True
    assert validation_keywords(document) & {
        "additionalProperties",
        "unevaluatedProperties",
    }


def test_resolved_convening_schema_requires_every_contract_field() -> None:
    # Given one valid document for each required root or nested contract field
    required_fields = (
        ((), "schema_version"),
        ((), "kind"),
        ((), "convening_id"),
        ((), "required_seats"),
        ((), "required_seats_provenance"),
        (("required_seats_provenance",), "candidate"),
        (("required_seats_provenance",), "governed_rule"),
        (("required_seats_provenance",), "normalized_facts"),
        (("required_seats_provenance",), "resolution"),
        (("required_seats_provenance", "candidate"), "repository"),
        (("required_seats_provenance", "candidate"), "pull_request"),
        (("required_seats_provenance", "candidate"), "head_revision"),
        (("required_seats_provenance", "governed_rule"), "repository"),
        (("required_seats_provenance", "governed_rule"), "path"),
        (("required_seats_provenance", "governed_rule"), "revision"),
        (("required_seats_provenance", "governed_rule"), "matched_class"),
        (("required_seats_provenance", "resolution"), "standing_seats"),
        (("required_seats_provenance", "resolution"), "conditional_seats"),
    )

    # When each required field is removed
    for path, field in required_fields:
        document = valid_convening()
        _ = mapping_at(document, *path).pop(field)

        # Then schema validation identifies a required-field violation.
        assert "required" in validation_keywords(document)
    for field in ("seat", "condition_ref", "required"):
        document = valid_convening()
        resolution = mapping_at(document, "required_seats_provenance", "resolution")
        evaluations = resolution["conditional_seats"]
        assert isinstance(evaluations, list)
        evaluation = evaluations[0]
        assert isinstance(evaluation, dict)
        _ = evaluation.pop(field)
        assert "required" in validation_keywords(document)


@pytest.mark.parametrize(
    "seat", ["", "company policy", "Company-Policy", "company/policy"]
)
def test_required_seat_identifiers_use_the_portable_shape(seat: str) -> None:
    # Given a required seat outside the lowercase portable identifier shape
    document = valid_convening()
    document["required_seats"] = [seat]

    # When the convening is schema-validated
    keywords = validation_keywords(document)

    # Then the seat identifier is rejected by its string shape contract.
    assert keywords & {"minLength", "pattern"}


def test_required_seats_refuses_an_empty_roster() -> None:
    # Given a resolved convening with no required seats
    document = valid_convening()
    document["required_seats"] = []

    # When the convening is schema-validated
    keywords = validation_keywords(document)

    # Then the non-empty roster contract rejects it.
    assert "minItems" in keywords


def test_required_seats_refuses_duplicate_identifiers() -> None:
    # Given a resolved convening that repeats one required seat
    document = valid_convening()
    document["required_seats"] = ["domain-policy", "domain-policy"]

    # When the convening is schema-validated
    keywords = validation_keywords(document)

    # Then the unique-roster contract rejects it.
    assert "uniqueItems" in keywords


@pytest.mark.parametrize(
    ("path", "repository"),
    [
        (("required_seats_provenance", "candidate"), "owner"),
        (("required_seats_provenance", "candidate"), "owner/repository/extra"),
        (("required_seats_provenance", "governed_rule"), "owner"),
        (("required_seats_provenance", "governed_rule"), "/owner/repository"),
    ],
)
def test_provenance_repositories_require_canonical_owner_repository(
    path: tuple[str, ...], repository: str
) -> None:
    # Given provenance with a non-canonical repository identifier
    document = valid_convening()
    mapping_at(document, *path)["repository"] = repository

    # When the convening is schema-validated
    # Then the owner/repository shape rejects it.
    assert "pattern" in validation_keywords(document)


@pytest.mark.parametrize("pull_request", [0, -1])
def test_candidate_pull_request_requires_a_positive_number(pull_request: int) -> None:
    # Given candidate provenance with a non-positive pull-request number
    document = valid_convening()
    mapping_at(document, "required_seats_provenance", "candidate")["pull_request"] = (
        pull_request
    )

    # When the convening is schema-validated
    # Then the positive-number contract rejects it.
    assert "minimum" in validation_keywords(document)


@pytest.mark.parametrize(
    "rule_path",
    ["", "/rules/ordinary.yaml", "../ordinary.yaml", "rules/../ordinary.yaml"],
)
def test_governed_rule_path_is_normalized_and_repository_relative(
    rule_path: str,
) -> None:
    # Given governed-rule provenance with an empty, absolute, or traversing path
    document = valid_convening()
    mapping_at(document, "required_seats_provenance", "governed_rule")["path"] = (
        rule_path
    )

    # When the convening is schema-validated
    # Then its normalized repository-relative path contract rejects it.
    assert validation_keywords(document) & {"minLength", "pattern"}


@pytest.mark.parametrize(
    ("path", "field", "revision"),
    [
        (
            ("required_seats_provenance", "candidate"),
            "head_revision",
            "ABCDEF0123456789ABCDEF0123456789ABCDEF01",
        ),
        (("required_seats_provenance", "candidate"), "head_revision", "01234567"),
        (
            ("required_seats_provenance", "governed_rule"),
            "revision",
            "ABCDEF0123456789ABCDEF0123456789ABCDEF01",
        ),
        (("required_seats_provenance", "governed_rule"), "revision", "89abcdef"),
    ],
)
def test_provenance_revisions_require_lowercase_forty_hex(
    path: tuple[str, ...], field: str, revision: str
) -> None:
    # Given candidate or rule provenance with a non-canonical revision
    document = valid_convening()
    mapping_at(document, *path)[field] = revision

    # When the convening is schema-validated
    # Then the lowercase forty-hex contract rejects it.
    assert "pattern" in validation_keywords(document)


def test_governed_rule_matched_class_is_non_empty() -> None:
    # Given governed-rule provenance with no matched class identity
    document = valid_convening()
    mapping_at(document, "required_seats_provenance", "governed_rule")[
        "matched_class"
    ] = ""

    # When the convening is schema-validated
    # Then the non-empty identity contract rejects it.
    assert "minLength" in validation_keywords(document)


@pytest.mark.parametrize(
    "forbidden_field",
    ["client_secret", "private_key", "raw_provider_payload", "host_absolute_path"],
)
def test_provenance_schema_refuses_sensitive_or_host_specific_fields(
    forbidden_field: str,
) -> None:
    # Given provenance carrying a secret, private key, raw payload, or host path field
    document = valid_convening()
    mapping_at(document, "required_seats_provenance")[forbidden_field] = "forbidden"

    # When the convening is schema-validated
    # Then the closed provenance boundary rejects it.
    assert validation_keywords(document) & {
        "additionalProperties",
        "unevaluatedProperties",
    }
