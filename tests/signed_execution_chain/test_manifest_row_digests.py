"""THE REGISTRATION IS ENFORCEABLE, NOT MERELY WRITTEN (contract-v2.5 cut,
add-signed-execution-chain task 4.7).

`contracts/manifest.yaml` is what a cross-repository consumer reads to learn
which bytes it is entitled to pin, and this cut adds FIVE rows to it. A row whose
`sha256` no longer matches the schema on disk publishes a promise about bytes
nobody shipped — and that is not hypothetical here: `validate-manifest-digests.py`
exists at all because one stale row (`content-manifest.schema.yaml`) rode through
THREE bundle cuts undetected.

**AND THAT SWEEPER IS WIRED INTO NOTHING.** `grep -rn validate-manifest-digests`
finds it in prose — a README line, changelog history, task lists — and in no
workflow and no test. So it catches drift only when a human remembers to run it,
which is the same failure mode it was written to close, one level up. This test
is the standing check for the rows THIS family owns.

WHY NOT THE WHOLE MANIFEST. The estate-wide sweep is
`scripts/validate-manifest-digests.py`'s job and it is the right tool for it
(155 rows at this cut). Scoping here to the five rows this capability owns means a
red reds for THIS capability's reason, and cannot be greened — or reddened — by an
unrelated row's drift. The precedent is
`tests/credential_contracts/test_manifest_row_digest.py`, built one release
earlier for the same reason.

WHAT THIS DOES NOT ASSERT. Nothing here is evidence that the named reader is a
REQUIRED check. It IS one, since 2026-08-31 — opensoft org ruleset 21957695,
proved refusing on canary PR #549 (tasks 4.5 and 4.6) — but that fact lives in a
ruleset and not in this file. A verified digest says the bytes are the bytes, and
says nothing about whether anything walks them.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "contracts" / "manifest.yaml"

# The five schemas the family README's table names, keyed by manifest row id.
# A sixth file in contracts/signed-execution-chain/ that is a schema and is NOT
# here would be an unregistered contract, which is what the closure test below
# refuses.
EXPECTED_ROWS = {
    "signed-execution-chain-digest-construction": (
        "contracts/signed-execution-chain/digest-construction.schema.yaml"
    ),
    "signed-execution-chain-inception": (
        "contracts/signed-execution-chain/chain-inception.schema.yaml"
    ),
    "signed-execution-chain-traveling-contract": (
        "contracts/signed-execution-chain/traveling-contract.schema.yaml"
    ),
    "signed-execution-chain-transparency-log-leaf": (
        "contracts/signed-execution-chain/transparency-log-leaf.schema.yaml"
    ),
    "signed-execution-chain-conformance-declaration": (
        "contracts/signed-execution-chain/conformance-declaration.schema.yaml"
    ),
}


def _walk(node):
    if isinstance(node, dict):
        if isinstance(node.get("id"), str) and "sha256" in node:
            yield node
        for value in node.values():
            yield from _walk(value)
    elif isinstance(node, list):
        for item in node:
            yield from _walk(item)


def _family_rows() -> dict[str, dict]:
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    rows: dict[str, dict] = {}
    for row in _walk(manifest):
        identifier = row["id"]
        if not identifier.startswith("signed-execution-chain"):
            continue
        assert identifier not in rows, f"duplicate manifest row {identifier!r}"
        rows[identifier] = row
    return rows


def test_the_family_registers_exactly_the_five_schemas() -> None:
    """Closed in BOTH directions: a schema with no row is an unregistered
    contract, and a row with no schema is a digest over nothing."""
    assert _family_rows().keys() == EXPECTED_ROWS.keys()


def test_every_schema_file_on_disk_carries_a_row() -> None:
    """The set is derived from the DIRECTORY, not from the expectation above, so
    a sixth schema added without a manifest row reds here rather than shipping
    unregistered.

    ``rglob``, NOT ``glob`` — PR #533 round one, Copilot. A top-level ``glob``
    reads the family root only, so a schema in a SUBDIRECTORY would bypass the
    closure this test exists to enforce and ship unregistered while the test
    stayed green. That is not hypothetical: this repository already places a
    schema at ``contracts/hermes-runtime/migrations/v1-to-v2-mapping.schema.yaml``,
    the only nested one under ``contracts/`` today and proof the layout is
    reachable. The docstring said "derived from the DIRECTORY" while the code
    read one level of it — a check that looked like it was doing its job, which
    is this capability's own round-one defect class. Measured: ``glob`` and
    ``rglob`` return the identical five paths at this cut, so the fix changes
    nothing today and closes the hole for whoever adds the sixth file.
    """
    on_disk = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "contracts" / "signed-execution-chain").rglob(
            "*.schema.yaml"
        )
    }
    assert on_disk == set(EXPECTED_ROWS.values())


@pytest.mark.parametrize("row_id", sorted(EXPECTED_ROWS))
def test_the_row_digest_matches_the_schema_on_disk(row_id: str) -> None:
    row = _family_rows()[row_id]
    assert row["path"] == EXPECTED_ROWS[row_id]
    path = ROOT / row["path"]
    assert path.is_file(), row["path"]
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    # str() DELIBERATELY, on `validate-manifest-digests.py`'s precedent: an
    # unquoted all-digit digest is parsed by PyYAML as an INT, and comparing or
    # slicing it raw turns a MISMATCH — a finding this test exists to report —
    # into a TypeError, which is a harness failure in the wrong currency.
    # Measured, not assumed: the first red-proof of this test crashed exactly
    # that way, which is the round-three lesson of the realization this cut
    # registers, arriving in its own gate.
    recorded = str(row["sha256"])
    assert recorded == actual, (
        f"contracts/manifest.yaml records {recorded[:12]}… for {row['path']} "
        f"but the bytes hash to {actual[:12]}…. The schema moved and the row did "
        f"not. Recompute it in the SAME commit — a consumer verifies the digest "
        f"before treating a copy as current, so a stale row publishes a promise "
        f"about bytes nobody shipped."
    )
    # A quoted-or-not digest must still BE 64 lowercase hex; an int-parsed value
    # that happened to match would have lost its leading zeros.
    assert isinstance(row["sha256"], str), (
        f"{row['path']}: the manifest's sha256 must be a STRING — an unquoted "
        f"all-digit or leading-zero digest silently changes value when parsed"
    )


@pytest.mark.parametrize("row_id", sorted(EXPECTED_ROWS))
def test_every_row_names_the_bundle_that_registered_it(row_id: str) -> None:
    """A digest that verifies over bytes whose provenance the row does not state
    is half a registration: the rule is what tells a consumer which bundle it is
    pinning and that the digest must be checked before a copy is treated as
    current."""
    rule = _family_rows()[row_id]["consumption_rule"]
    assert "Registered at contract-v2.5" in rule, row_id
    assert "per-file sha256 verified" in rule, row_id
