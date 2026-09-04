"""The six family schemas, and the packaged positive corpus they admit.

Layer one of the family's proof: every schema is meta-valid and self-identifying,
and every positive example validates against the schema its own `kind` names. A
family whose examples were checked only by the validator's self-test would be
proving the validator, not the schemas.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

from conftest import EXAMPLES, FAMILY_DIR, adjudicate

SCHEMAS = sorted(FAMILY_DIR.glob("*.schema.yaml"))
POSITIVES = sorted(EXAMPLES.glob("*.example.yaml"))


def test_the_family_ships_six_schemas() -> None:
    """Pinned as a NUMBER, not as a glob's length.

    `add-clearing-dispatch-boundary`'s `code_surface` named five neutral record
    shapes and this line said so. Its own docstring said what a sixth would mean:
    "a sixth arriving without a change to this line is a shape nobody ratified".
    `admit-deliberation-clearing-operation` (ratified 2026-09-04 by Brett Heap,
    PR #645, merged `3cf917b7`) IS that ratification, and
    `deliberation-return.schema.yaml` is the sixth — the neutral return shape
    register entry number two declares, ruled a NEW NEUTRAL SCHEMA by OQ1 rather
    than borrowed from a producing repository.

    A SEVENTH arriving without a change to this line is still a shape nobody
    ratified, and a sixth disappearing is still a shape somebody deleted.
    """
    assert [p.name for p in SCHEMAS] == [
        "deliberation-return.schema.yaml",
        "dispatch-record.schema.yaml",
        "operation-report.schema.yaml",
        "permitted-operations.schema.yaml",
        "sealed-bundle-manifest.schema.yaml",
        "single-door-attestation.schema.yaml",
    ]


@pytest.mark.parametrize("path", SCHEMAS, ids=lambda p: p.name)
def test_every_schema_is_meta_valid_and_self_identifying(path: Path) -> None:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(doc)
    assert doc.get("$schema"), f"{path.name}: no dialect declared"
    assert doc.get("$id", "").startswith("https://xforge.us/schemas/openxfactory/clearing/v1/"), \
        f"{path.name}: the $id must be absolute and in the family's namespace, " \
        f"so a consumer's stock validator resolves the bundle the way ours does"
    assert doc.get("schema_version") == 1
    assert doc.get("kind") == "openxfactory-clearing-contract-schema"
    assert doc.get("contract_schema_version") == 1


@pytest.mark.parametrize("path", SCHEMAS, ids=lambda p: p.name)
def test_every_schema_closes_its_root_to_unknown_members(path: Path) -> None:
    """A record shape that admits unknown members cannot refuse a smuggled one.

    This is not stylistic. Three of this family's refusals — a verdict field on
    the operation report, an observed-group member on a lane, an eleventh field
    on the manifest — are only refusable because the root is closed.
    """
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert doc.get("additionalProperties") is False, \
        f"{path.name}: the root admits unknown members"


@pytest.mark.parametrize("path", POSITIVES, ids=lambda p: p.name)
def test_every_positive_example_validates(path: Path, reader, registry_and_docs,
                                          entries, fixture_origins) -> None:
    docs = reader.load_records(path)
    assert docs, f"{path.name}: carries no record"
    for index, doc in enumerate(docs):
        assert doc.get("kind") in reader.KIND_TO_SCHEMA, \
            f"{path.name}#{index}: kind {doc.get('kind')!r} is not this family's"
        findings = adjudicate(reader, registry_and_docs, entries, fixture_origins,
                              doc, f"{path.name}#{index}")
        assert findings.errors == [], f"{path.name}#{index}: {findings.errors}"


def test_the_corpus_covers_every_shipped_kind() -> None:
    """One positive per record kind, at least.

    A family may ship a schema nobody exercised; this test is what stops it. The
    register's own positive is the shipped instance itself, adjudicated by the
    validator on every run rather than duplicated into `examples/`.
    """
    kinds = set()
    for path in POSITIVES:
        for doc in yaml.safe_load_all(path.read_text(encoding="utf-8")):
            if isinstance(doc, dict) and doc.get("kind"):
                kinds.add(doc["kind"])
    assert kinds == {
        "xfactory_sealed_bundle_manifest",
        "xfactory_clearing_operation_report",
        "xfactory_clearing_deliberation_return",
        "xfactory_clearing_dispatch_record",
        "xfactory_clearing_single_door_attestation",
    }


def test_the_manifest_offers_both_field_ten_variants() -> None:
    """Field (10) is a disjunction where no identity is registered and a
    requirement where one is, so the corpus must show BOTH.

    A corpus holding only the signed form would let a later reader conclude the
    interim floor had been removed; one holding only hosted provenance would hide
    the tightening `add-cpc-clearing-boundary` ratified.
    """
    variants = set()
    for path in POSITIVES:
        for doc in yaml.safe_load_all(path.read_text(encoding="utf-8")):
            if isinstance(doc, dict) and \
                    doc.get("kind") == "xfactory_sealed_bundle_manifest":
                variants.add(doc["origin_attestation"]["attestation_type"])
    assert variants == {"origin_signature", "hosted_workflow_provenance"}
