"""ONE digest construction, cited rather than redefined.

The ratified scenario is blunt: "A second digest rule is proposed → it MUST use
the digest construction already in force for the estate AND a new construction
MUST NOT be defined by this capability." `add-cpc-clearing-boundary` adds the
other half — the manifest needs a SUBJECT in that construction's closed
enumeration, and until one exists the requirement is "UNREALIZABLE as written and
SHALL NOT be reported as satisfied".

So this module checks three things a reader would otherwise have to take on
trust: the subject exists in BOTH places that hold the enumeration, the family
declares no construction of its own, and the manifest's digest shape is the
chain's shape rather than a lookalike.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from conftest import FAMILY_DIR, REPO_ROOT

CHAIN_SCHEMA = REPO_ROOT / "contracts" / "signed-execution-chain" / \
    "digest-construction.schema.yaml"
MANIFEST_SCHEMA = FAMILY_DIR / "sealed-bundle-manifest.schema.yaml"
SUBJECT = "sealed_bundle_manifest"


@pytest.fixture(scope="module")
def chain_doc() -> dict:
    return yaml.safe_load(CHAIN_SCHEMA.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def manifest_doc() -> dict:
    return yaml.safe_load(MANIFEST_SCHEMA.read_text(encoding="utf-8"))


def test_the_subject_is_admitted_by_the_owning_contract(chain_doc) -> None:
    enum = chain_doc["$defs"]["digest_subject"]["enum"]
    assert SUBJECT in enum, (
        "the manifest subject is not admitted by signed-execution-chain's closed "
        "enumeration. add-cpc-clearing-boundary's field-(10) requirement is then "
        "UNREALIZABLE as written and must not be reported as satisfied"
    )


def test_the_reader_frozen_set_agrees_with_the_contract(chain_doc) -> None:
    """The contract and the reader hold the same enumeration, in two files.

    `scripts/signed_execution_chain/canonical.py` says why it keeps a copy: "the
    enumeration is the contract's; it is repeated here as a frozen set the
    validator checks against so a subject the contract does not declare cannot
    reach a comparison." A widening of one without the other leaves the reader
    refusing a subject the contract admits, or admitting one it does not.
    """
    import sys
    sys.path.insert(0, str(REPO_ROOT))
    from scripts.signed_execution_chain import canonical

    assert SUBJECT in canonical.SUBJECTS
    assert set(chain_doc["$defs"]["digest_subject"]["enum"]) == set(canonical.SUBJECTS)


def test_the_construction_name_did_not_move(chain_doc) -> None:
    """A tranche widens SUBJECTS. It never touches the construction."""
    assert chain_doc["$defs"]["construction_name"]["const"] == "xfc-jcs-sha256-1"


def test_the_manifest_digest_is_the_chain_digest_shape(chain_doc, manifest_doc) -> None:
    """Same three members, same value patterns — structurally, not by promise.

    The two families are separately registered contract files rather than one
    bundle resolved by relative `$ref`, so the constraint is restated in the
    manifest schema. This test is what keeps a restatement from drifting into a
    second rule wearing the first one's name.
    """
    chain = chain_doc["$defs"]["digest"]
    ours = manifest_doc["$defs"]["manifest_digest"]
    assert set(ours["required"]) == set(chain["required"]) == \
        {"construction", "subject", "value"}
    assert ours["additionalProperties"] is False
    assert ours["properties"]["value"]["pattern"] == \
        chain["properties"]["value"]["pattern"]
    assert ours["properties"]["construction"]["const"] == \
        chain_doc["$defs"]["construction_name"]["const"]
    assert ours["properties"]["subject"]["const"] == SUBJECT


def test_the_family_declares_no_construction_of_its_own() -> None:
    """No file under `contracts/clearing/` may mint a construction name.

    Scanned as TEXT rather than as parsed YAML, because the hazard is a
    construction arriving anywhere — a `$defs` member, a description, an example
    — and a structural check would only look where one is expected.

    `examples/negative/` is exempt BY DESIGN: one fixture there declares
    `clearing-sha256-1` on purpose, because that is the refusal it proves. A scan
    that could not tell a deliberate counterexample from a defect would force the
    corpus to stop demonstrating the very rule this test defends.
    """
    offenders = []
    negatives = FAMILY_DIR / "examples" / "negative"
    pattern = re.compile(r"construction_name|construction:\s*(?!xfc-jcs-sha256-1)\S")
    for path in sorted(FAMILY_DIR.rglob("*.yaml")):
        if negatives in path.parents:
            continue
        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), start=1):
            if line.lstrip().startswith("#"):
                continue
            if pattern.search(line):
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{number}: {line.strip()}")
    assert not offenders, (
        "a second digest construction is being declared beside the one in force. "
        "signed-execution-chain's own header names this the defect: 'a second "
        "construction declared beside this one is a defect whatever it is "
        "called'.\n" + "\n".join(offenders)
    )


def test_per_file_hashes_carry_no_construction(manifest_doc) -> None:
    """Per-file content hashes are BYTE hashes and must not be shaped like JSON
    digests — a canonical-JSON construction has nothing to canonicalize in a byte
    stream, and the ratified scenario refuses the confusion as a category error."""
    byte_hash = manifest_doc["$defs"]["byte_hash"]
    assert byte_hash["type"] == "string"
    assert byte_hash["pattern"] == r"^sha256:[0-9a-f]{64}$"
    assert "construction" not in str(byte_hash.get("properties", {}))


def test_the_packaged_signature_covers_the_ten_field_subject(reader) -> None:
    """The signable subject IS the ten declared fields, and its digest commits
    to them.

    Recomputed here rather than trusted: the packaged manifest's recorded digest
    must equal `canonical.digest` of the subject the validator derives, or the
    record's digest commits to bytes nobody shipped.
    """
    import sys
    sys.path.insert(0, str(REPO_ROOT))
    from scripts.signed_execution_chain import canonical

    path = FAMILY_DIR / "examples" / \
        "sealed-bundle-manifest-registered-producer.example.yaml"
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    subject = reader.signable_subject(doc)
    assert set(subject) == set(reader.DECLARED_FIELDS)
    assert "signature" not in subject["origin_attestation"], (
        "a signature cannot cover itself"
    )
    assert "value" not in subject["origin_attestation"]["manifest_digest"], (
        "a digest cannot commit to its own output"
    )
    assert doc["origin_attestation"]["manifest_digest"]["value"] == \
        canonical.digest(subject)
