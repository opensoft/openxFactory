"""THE CONCURRENT-WRITER GATE (add-binding-consumer-identity §5.4).

`add-credential-escrow-checkout` owes an additive minor on the SAME schema file,
is RATIFIED and therefore frozen, makes no mention of this change, and carries no
concurrent-writer re-read in any of its nine schema tasks. And `main` is a THIRD
writer of `contracts/manifest.yaml` in its own right. So an instruction telling
"whichever cuts second" to re-read the file binds only the packet that wrote the
instruction — which is a hope, not coordination.

**THE INVARIANT IS BUILT INSTEAD, and it binds every writer without editing a
frozen packet**: the `credential-contracts` manifest row's digest is recomputed
from the file ON DISK and a mismatch reds. Whoever moves the schema bytes and
does not move the row — this change, escrow, main, or a hand edit — fails here,
at the commit, rather than at a consumer that pinned a digest for bytes it never
received.

WHY NOT THE WHOLE MANIFEST. `scripts/validate-manifest-digests.py` already checks
all 145 rows and is the right tool for the estate-wide sweep; this test is scoped
to the row this capability owns so it fails for THIS capability's reason and
cannot be reddened, or greened, by an unrelated row's drift.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "contracts" / "manifest.yaml"
ROW_ID = "credential-contracts"


def _row():
    manifest = yaml.safe_load(MANIFEST.read_text())

    def walk(node):
        if isinstance(node, dict):
            if node.get("id") == ROW_ID and "sha256" in node:
                yield node
            for value in node.values():
                yield from walk(value)
        elif isinstance(node, list):
            for item in node:
                yield from walk(item)

    rows = list(walk(manifest))
    assert len(rows) == 1, f"expected exactly one {ROW_ID!r} row, found {len(rows)}"
    return rows[0]


def test_the_row_digest_matches_the_schema_on_disk():
    row = _row()
    path = ROOT / row["path"]
    assert path.is_file(), row["path"]
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert row["sha256"] == actual, (
        f"contracts/manifest.yaml records {row['sha256'][:12]}… for {row['path']} but the bytes "
        f"hash to {actual[:12]}…. The schema moved and the row did not. Recompute it in the SAME "
        f"commit — a consumer verifies the digest before treating a copy as current, so a stale "
        f"row publishes a promise about bytes nobody shipped.")


def test_the_row_points_at_the_schema_this_capability_owns():
    assert _row()["path"] == "contracts/schemas/xfactory-credential-contracts.schema.yaml"


def test_the_consumption_rule_names_the_block_and_its_phasing():
    """A digest that verifies over bytes whose meaning the row does not describe
    is half a registration. The rule is what a cross-repository consumer reads to
    learn that the block is declared here and constrained later."""
    rule = _row()["consumption_rule"]
    for token in ("consumer:", "holder_ref", "fetch_identity", "instantiation_stub",
                  "contract-v3.0"):
        assert token in rule, token
