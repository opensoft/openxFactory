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
import re

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
    "clearing-dispatch-record":
        "contracts/clearing/dispatch-record.schema.yaml",
    "clearing-single-door-attestation":
        "contracts/clearing/single-door-attestation.schema.yaml",
}


@pytest.fixture(scope="module")
def rows() -> dict[str, dict]:
    doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    return {row["id"]: row for row in doc["contracts"]
            if row["path"].startswith("contracts/clearing/")}


def test_the_family_registers_exactly_the_six_members(rows) -> None:
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
    assert "contract-v3.3" in row["consumption_rule"], (
        "each row records the release that registered it, so a consumer reading "
        "one row knows which bundle to pin"
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


#: ``Registered at contract-v<major>.<minor>`` as the rows spell it.
_REGISTERING_RELEASE = re.compile(r"Registered at (contract-v(\d+)\.(\d+))")


def _bundle_order(tag: str) -> tuple[int, int]:
    matched = re.fullmatch(r"contract-v(\d+)\.(\d+)", tag)
    assert matched, f"{tag!r} is not a contract-v<major>.<minor> bundle tag"
    return int(matched.group(1)), int(matched.group(2))


def test_the_declared_bundle_has_an_inventory_and_is_not_behind_the_rows(rows) -> None:
    """The rows' REGISTERING release and the manifest's DECLARED bundle agree.

    Two places hold a number and they are DIFFERENT numbers, which is why this
    no longer asserts they are equal. The rows say ``Registered at
    contract-v3.3`` and that is HISTORY — it names the bundle whose bytes first
    carried this family, and it never moves again. ``contract_bundle_version``
    names the bundle the repository declares TODAY, and it advances at EVERY
    cut. Written as an equality while `contract-v3.3` was both, this test could
    only red the required suite at the next cut, for no defect in the family it
    guards; `contract-v3.4` — the first cut past its own writing — is where that
    came due, and the equality is repaired here rather than re-pinned to a
    number that would fail again at `contract-v3.5`.

    What was actually owed survives and is checked instead: every row names ONE
    registering release, that release has an inventory beside it, the declared
    bundle has one too, and the declared bundle is NEVER BEHIND the release the
    rows advertise — a manifest declaring an earlier bundle than its own rows
    name would publish rows claiming a release the bundle does not contain,
    which is the failure the original docstring described.
    """
    registering = {
        matched.group(1)
        for row in rows.values()
        for matched in [_REGISTERING_RELEASE.search(row["consumption_rule"])]
        if matched
    }
    assert len(registering) == 1, (
        "the clearing rows name more than one registering release "
        f"({sorted(registering)}); a consumer reading one row would not know "
        "which bundle to pin"
    )
    registered_at = registering.pop()

    doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    declared = doc["contract_bundle_version"]

    for tag in (registered_at, declared):
        inventory = REPO_ROOT / "contracts" / "releases" / f"{tag}.digests.yaml"
        assert inventory.is_file(), (
            f"{tag} has no release inventory beside it at contracts/releases/"
        )

    assert _bundle_order(declared) >= _bundle_order(registered_at), (
        f"the manifest declares {declared}, which is BEHIND the {registered_at} "
        "these rows advertise as their registering release"
    )
