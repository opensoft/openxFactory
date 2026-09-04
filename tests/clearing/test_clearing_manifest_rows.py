"""The family's manifest rows, closed in BOTH directions and digest-verified.

The estate-wide sweep in `tests/manifest_digests/` recomputes every row that
carries a digest, so a STALE row is already caught. What it cannot catch is a
MISSING one: a new schema that never got a row is invisible to a sweep over rows.
This module closes the other direction, the way
`tests/signed_execution_chain/test_manifest_row_digests.py` does for its family —
every expected row is registered, and every registered artifact on disk carries a
row.

THE FILENAME CARRIES THE FAMILY for the same reason its sibling gate test does:
that signed-execution-chain module has the obvious basename already, and two
rootless directories cannot both claim one bare module name in `sys.modules`.
"""

from __future__ import annotations

import hashlib

import pytest
import yaml

from conftest import FAMILY_DIR, REPO_ROOT

MANIFEST = REPO_ROOT / "contracts" / "manifest.yaml"

#: Every artifact of this family that is a MEMBER of the contract bundle, mapped
#: to its path. The validator, the README, the examples corpus and the tests are
#: deliberately NOT here: they are content-addressed by commit, the precedent
#: every family since openxWallet follows.
EXPECTED_ROWS = {
    "clearing-sealed-bundle-manifest":
        "contracts/clearing/sealed-bundle-manifest.schema.yaml",
    "clearing-permitted-operations-registry-schema":
        "contracts/clearing/permitted-operations.schema.yaml",
    "clearing-permitted-operations-registry":
        "contracts/clearing/permitted-operations.registry.yaml",
    "clearing-operation-report":
        "contracts/clearing/operation-report.schema.yaml",
    "clearing-deliberation-return":
        "contracts/clearing/deliberation-return.schema.yaml",
    "clearing-dispatch-record":
        "contracts/clearing/dispatch-record.schema.yaml",
    "clearing-single-door-attestation":
        "contracts/clearing/single-door-attestation.schema.yaml",
}


#: WHAT EACH ROW MUST RECORD ABOUT ITS OWN PROVENANCE, per row rather than per
#: family — which is what the assertion was always about: "each row records the
#: release that registered it, so a consumer reading one row knows which bundle
#: to pin". Six rows were registered AT the `contract-v3.3` cut and say so. The
#: seventh was registered AT REALIZATION, ahead of any cut, and says WHICH
#: GOVERNED CHANGE registered it instead — the form `add-chain-attestation` and
#: `add-chain-anchoring` already use in this manifest, and the form
#: `docs/contract-versioning-policy.md` requires of a change that must not
#: reserve a minor before merge order is known.
#:
#: A ROW CLAIMING A BUNDLE IT WAS NOT CUT IN IS THE DEFECT THIS GUARDS, in both
#: directions: a realization row that named a number would reserve one, and a cut
#: row that named none would leave a consumer nothing to pin.
REGISTRATION = {
    "clearing-sealed-bundle-manifest": "contract-v3.3",
    "clearing-permitted-operations-registry-schema": "contract-v3.3",
    "clearing-permitted-operations-registry": "contract-v3.3",
    "clearing-operation-report": "contract-v3.3",
    "clearing-dispatch-record": "contract-v3.3",
    "clearing-single-door-attestation": "contract-v3.3",
    "clearing-deliberation-return": "admit-deliberation-clearing-operation",
}


def test_every_expected_row_declares_its_provenance_form() -> None:
    """The two maps are one set, so a row added to one and not the other is red
    rather than silently unchecked."""
    assert set(REGISTRATION) == set(EXPECTED_ROWS)


def test_the_realization_row_reserves_no_bundle_number() -> None:
    """A change MUST NOT reserve a minor before merge order is known.

    `contract-v3.4` was claimed by another lane on the repository owner's word
    before this row existed, and Lane Collision Protocol Amendment 1 rule 7
    serializes contract-cut claims FIFO. So this row names its CHANGE and leaves
    the number to the cutting session — and this test is what stops a later
    session writing one in without cutting.
    """
    doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    row = next(r for r in doc["contracts"]
               if r["id"] == "clearing-deliberation-return")
    rule = row["consumption_rule"]
    assert "the bundle number is the cutting session's" in rule
    assert "contract-v3.4" not in rule
    assert "contract-v3.5" not in rule


@pytest.fixture(scope="module")
def rows() -> dict[str, dict]:
    doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    return {row["id"]: row for row in doc["contracts"]
            if row["path"].startswith("contracts/clearing/")}


def test_the_family_registers_exactly_the_seven_members(rows) -> None:
    """SIX until 2026-09-04, SEVEN since.

    `clearing-deliberation-return` is register entry number two's declared output
    shape, registered at realization by `admit-deliberation-clearing-operation`
    (ratified by Brett Heap, PR #645, merged `3cf917b7`). An eighth arriving
    without a change to this constant is still a bundle member nobody declared.
    """
    assert set(rows) == set(EXPECTED_ROWS), (
        "the manifest's clearing rows are not the expected set. A row added "
        "without a change to this constant is a bundle member nobody declared; a "
        "row removed is a member consumers may still be pinning"
    )


def test_every_registered_artifact_on_disk_carries_a_row(rows) -> None:
    """The direction the estate-wide digest sweep cannot see.

    A sweep over ROWS cannot notice a FILE that has none. `rglob` rather than
    `glob`, so a schema added in a future subdirectory is caught too.
    """
    on_disk = {
        str(p.relative_to(REPO_ROOT))
        for p in FAMILY_DIR.rglob("*.schema.yaml")
        if "examples" not in p.parts
    } | {
        str(p.relative_to(REPO_ROOT))
        for p in FAMILY_DIR.rglob("*.registry.yaml")
        if "examples" not in p.parts
    }
    registered = {row["path"] for row in rows.values()}
    assert on_disk == registered, (
        f"unregistered on disk: {sorted(on_disk - registered)}; "
        f"registered but absent: {sorted(registered - on_disk)}"
    )


@pytest.mark.parametrize("row_id,path", sorted(EXPECTED_ROWS.items()))
def test_the_row_digest_matches_the_artifact_on_disk(row_id, path, rows) -> None:
    """Recomputed from the bytes, and compared as `str()`.

    The `str()` is not decoration: a digest that happens to be all digits and is
    written unquoted parses as an INT, and an int never equals a hex string — the
    comparison would fail for a reason that has nothing to do with the bytes.
    """
    row = rows[row_id]
    assert row["path"] == path
    actual = hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest()
    assert str(row["sha256"]) == actual, (
        f"contracts/manifest.yaml records {str(row['sha256'])[:12]}… for {path} "
        f"but the bytes hash to {actual[:12]}…. Recompute it in the SAME commit: "
        f"a consumer verifies the digest before treating a copy as current, so a "
        f"stale row publishes a promise about bytes nobody shipped"
    )


@pytest.mark.parametrize("row_id", sorted(EXPECTED_ROWS))
def test_every_row_declares_the_neutral_ownership_fields(row_id, rows) -> None:
    row = rows[row_id]
    assert row["compatibility"] == "canonical_openxfactory_contract"
    assert row["adapter_owner"] == "openxFactory"
    assert row["schema_version"] == 1
    assert row["source_path"] == "openxFactory/" + row["path"]
    assert row["consumption_rule"].strip(), "a row with no consumption rule tells " \
        "a consumer what to copy and nothing about what it means"
    assert REGISTRATION[row_id] in row["consumption_rule"], (
        "each row records WHERE IT CAME FROM, so a consumer reading one row knows "
        "which bundle to pin — or, for a row registered at realization ahead of "
        "its cut, which governed change registered it and that the number is the "
        "cutting session's"
    )


def test_the_registry_instance_is_typed_as_a_registry(rows) -> None:
    """The instance's CONTENT is the contract, not merely its shape.

    A consumer that verified the schema and not the instance would have verified
    the shape of a decision without verifying the decision — which for a CLOSED
    register is the whole of it.
    """
    assert rows["clearing-permitted-operations-registry"]["type"] == "registry"
    for row_id in EXPECTED_ROWS:
        if row_id != "clearing-permitted-operations-registry":
            assert rows[row_id]["type"] == "schema"


def test_the_declared_bundle_version_is_the_one_the_rows_name() -> None:
    """The manifest's own version and the rows' registration note agree.

    Two places hold the number; a cut that moved one and not the other would
    publish rows claiming a release the bundle does not declare.
    """
    doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    assert doc["contract_bundle_version"] == "contract-v3.3"
    inventory = REPO_ROOT / "contracts" / "releases" / "contract-v3.3.digests.yaml"
    assert inventory.is_file(), (
        "the manifest declares a bundle with no release inventory beside it"
    )
