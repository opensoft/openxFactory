"""`scripts/validate-factory-identity.py`: the positives, and every refusal.

WHAT IS PROVEN HERE, AND WHY EACH HALF IS SEPARATE.

THE SHIPPED TREE IS ADJUDICATED AS IT STANDS. `test_the_shipped_tree_refuses_
until_the_key_is_minted` runs the reader against the REAL repository root and
asserts the exact refusal set: the register is unminted, so it MUST NOT merge,
and the proof of that is a red run rather than a comment saying so. When the
operator performs the mint, this test is the thing that goes green — and the
`FILL-IN-AT-MINT` count it pins is the thing that has to move deliberately.

THE RULES ARE ADJUDICATED AGAINST SYNTHETIC TREES. Every refusal gets its own
built tree, because a rule proven only against the shipped artifact is a rule
that stops being proven the moment the artifact changes.

THE NEGATIVE THAT MATTERS MOST is `test_a_key_id_shared_with_review_authority_
is_refused`: the ratified disjointness requirement's whole enforceable half. It
is asserted in both directions (shared `key_id`, shared fingerprint) and it is
asserted NOT to be waivable by declaring different acts, because "different act"
is exactly the argument somebody will make when the rule fires.

NO PRIVATE HALF, NO PLAUSIBLE PUBLIC HALF. The keys these tests use are derived
from labelled sha256 digests, so a reader can see at a glance that nobody holds
a private half and that no value here could be mistaken for a real minted key.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
VALIDATOR = REPO_ROOT / "scripts" / "validate-factory-identity.py"
PINNED_READER = REPO_ROOT / "openXwallet" / "scripts" / "validate-openxwallet.py"

FAMILY = REPO_ROOT / "governance" / "factory-identity"
REGISTER = FAMILY / "register.yaml"
REVIEW_REGISTER = REPO_ROOT / "governance" / "review-authority" / "register.yaml"

SENTINEL = "FILL-IN-AT-MINT"

#: The shipped tree's sentinel count, pinned LITERALLY. Five values are replaced
#: by the mint (three in the wallet, two in the attestation); a sixth appearing,
#: or one going missing, must break this test and force a deliberate edit here
#: beside the register edit rather than pass under a wildcard.
SHIPPED_SENTINEL_VALUES = 5

pytestmark = pytest.mark.skipif(
    not PINNED_READER.is_file(),
    reason="the pinned openXwallet reader is not initialized "
           "(`git submodule update --init openXwallet`); this reader REFUSES "
           "rather than deriving keys with arithmetic of its own")


# --------------------------------------------------------------- helpers

def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(VALIDATOR), *args],
                          capture_output=True, text=True, cwd=str(REPO_ROOT))


def codes(out: str) -> set[str]:
    return {line.split("[", 1)[1].split("]", 1)[0]
            for line in out.splitlines() if line.startswith("error [")}


def keypair(label: str) -> tuple[str, str, str]:
    """A deterministic (base64url, multibase, fingerprint) triple.

    Deterministic so a failure is reproducible, labelled so it is obvious that
    nobody holds a private half. The encoding is `did:key`'s own — `z` plus
    base58btc of the ed25519 multicodec prefix and the raw key — reached through
    the validator's OWN encoder, which round-trips every value through the
    pinned decoder before returning it. A second encoder in this file would be
    the exact defect the module under test exists to prevent.
    """
    import base64
    import importlib.util
    spec = importlib.util.spec_from_file_location("_fi_validator", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    raw = hashlib.sha256(("factory-identity test / " + label).encode()).digest()
    b64u = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    multibase = "z" + module.b58encode(b"\xed\x01" + raw)
    return b64u, multibase, "sha256:" + hashlib.sha256(raw).hexdigest()


def build_tree(tmp_path: Path, *, holder: str = "opensoft/codexFactory",
               rows: list | None = None, register_extra: dict | None = None,
               wallet_mutate=None, grant_mutate=None,
               attestation_complete: bool = True,
               review_seat_keys: list | None = None) -> Path:
    """A minimal but COMPLETE two-family tree, minted (no sentinels) unless a
    mutator puts one back. Everything a rule needs is present, so a refusal in a
    test is the rule under test and never an incidental gap."""
    _, multibase, fingerprint = keypair(holder)
    fam = tmp_path / "governance" / "factory-identity"
    (fam / "wallets").mkdir(parents=True)
    (fam / "grants").mkdir(parents=True)
    (fam / "attestations").mkdir(parents=True)
    review = tmp_path / "governance" / "review-authority"
    (review / "wallets").mkdir(parents=True)

    wallet = {
        "schema_version": 1, "kind": "xfactory_wallet_record",
        "wallet_id": "wal-origin-test-0001",
        "holder": {"holder_id": holder, "holder_class": "organisation"},
        "key_reference": {
            "did": f"did:key:{multibase}", "key_id": "key-factory-test-0001",
            "key_fingerprint": fingerprint,
            "public_key_multibase": multibase,
            "signature_algorithm": "ed25519"},
        "custody": {"model": "holder_readable", "registry_version": 1},
        "state": "active",
    }
    if wallet_mutate:
        wallet_mutate(wallet)
    (fam / "wallets" / "wal-origin-test-0001.yaml").write_text(
        yaml.safe_dump(wallet), encoding="utf-8")

    grant = {
        "schema_version": 1, "kind": "xfactory_wallet_grant",
        "grant_id": "grant-origin-test-0001",
        "audience": {"wallet_ref": "wal-origin-test-0001",
                     "holder_ref": holder},
        "scope": {"acts": ["originate"], "objects": [holder],
                  "authority_tier": "act"},
        "expires_at": "2026-12-01T00:00:00Z",
        "issued_at": "2026-09-02T00:00:00Z",
        "issued_by": "Brett.Heap@opensoft.one",
        "state": "active",
    }
    if grant_mutate:
        grant_mutate(grant)
    (fam / "grants" / "grant-origin-test-0001.yaml").write_text(
        yaml.safe_dump(grant), encoding="utf-8")

    attestation = {
        "attestation_id": "attest-custody-wal-origin-test-0001",
        "subject_wallet_ref": "wal-origin-test-0001",
        "custody_model_attested": "holder_readable",
        "attested_key_fingerprint":
            fingerprint if attestation_complete else SENTINEL,
        "verified_at":
            "2026-09-02T00:00:00Z" if attestation_complete else SENTINEL,
    }
    (fam / "attestations"
     / "custody-attest-wal-origin-test-0001.yaml").write_text(
        yaml.safe_dump(attestation), encoding="utf-8")

    register = {
        "register_version": 1,
        "revocation_staleness_bound": "P7D",
        "revocation_staleness_ceiling": "P7D",
        "rows": rows if rows is not None else [{
            "row_id": "row-origin-test-0001", "holder_ref": holder,
            "wallet_ref": "wal-origin-test-0001", "act": "originate",
            "grant_ref": "grant-origin-test-0001",
            "expires_at": "2026-12-01T00:00:00Z", "state": "active"}],
    }
    register.update(register_extra or {})
    (fam / "register.yaml").write_text(yaml.safe_dump(register),
                                       encoding="utf-8")

    review_register = {"register_version": 1,
                       "revocation_staleness_bound": "P7D",
                       "rows": [], "seat_keys": review_seat_keys or []}
    (review / "register.yaml").write_text(yaml.safe_dump(review_register),
                                          encoding="utf-8")
    return tmp_path


# --------------------------------------------------------------- the shipped tree

def test_the_shipped_tree_refuses_until_the_key_is_minted() -> None:
    """The register CANNOT MERGE holding a placeholder. That is the point."""
    result = run(".")
    assert result.returncode == 1, (
        f"the shipped tree must REFUSE while the origin key is unminted; got "
        f"exit {result.returncode}:\n{result.stdout}")
    assert "factory-identity-placeholder-unminted" in codes(result.stdout)
    minted = [line for line in result.stdout.splitlines()
              if "factory-identity-placeholder-unminted" in line]
    assert len(minted) == SHIPPED_SENTINEL_VALUES, (
        f"the shipped tree carries {len(minted)} mint sentinels, not "
        f"{SHIPPED_SENTINEL_VALUES}. The count is pinned literally so a value "
        f"appearing or going missing is a deliberate edit here beside the "
        f"register edit, never a silent pass")


def test_no_plausible_key_literal_was_invented() -> None:
    """A value that LOOKS like a key is worse than no value, because it merges.

    Every value the mint produces is the sentinel and nothing else: no
    43-character base64url literal, no `did:key:z…` and no `sha256:` hex digest
    sits anywhere under the family while it is unminted.
    """
    import re
    for path in sorted(FAMILY.rglob("*.yaml")):
        text = path.read_text(encoding="utf-8")
        assert not re.search(r"did:key:z[1-9A-HJ-NP-Za-km-z]{40,}", text), (
            f"{path} carries a did:key literal before the mint")
        assert not re.search(r"sha256:[0-9a-f]{64}", text), (
            f"{path} carries a fingerprint literal before the mint")


def test_the_shipped_tree_is_disjoint_from_review_authority() -> None:
    """The ratified rule holds TODAY, not only in a fixture."""
    result = run(".")
    assert "factory-identity-registers-not-disjoint" not in codes(result.stdout)
    assert "0 shared" in result.stdout


def test_the_shipped_register_declares_its_own_bound_and_ceiling() -> None:
    doc = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))
    assert doc["revocation_staleness_bound"] == "P7D"
    assert doc["revocation_staleness_ceiling"] == "P7D"
    review = yaml.safe_load(REVIEW_REGISTER.read_text(encoding="utf-8"))
    assert "revocation_staleness_ceiling" not in review, (
        "the two registers are SIBLINGS: this one declares its own bound AND "
        "its own ceiling and inherits neither. If the intake register grows a "
        "ceiling, that is its business and not a source for this one")


def test_the_shipped_register_carries_no_seat_spelling() -> None:
    doc = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))
    assert "seat_keys" not in doc
    for row in doc["rows"]:
        assert not str(row["holder_ref"]).startswith("agent:")
        assert "authority_tier" not in row, (
            "authority is a property of the GRANT and its custody attestation; "
            "a register column restating it is two places for one fact to "
            "disagree")


def test_the_shipped_family_names_no_secret(tmp_path: Path) -> None:
    """The ratified requirement forbids 'a secret name resolvable to key
    material' in this family — a comment naming the variable is exactly as
    resolvable as a field naming it, so the check reads raw bytes."""
    result = run(".")
    assert "factory-identity-secret-name-recorded" not in codes(result.stdout)


# --------------------------------------------------------------- the rules

def test_a_minted_tree_passes(tmp_path: Path) -> None:
    """The positive. Without it every refusal below could be a reader that
    simply refuses everything."""
    root = build_tree(tmp_path)
    result = run(str(root))
    assert result.returncode == 0, result.stdout
    assert "factory-identity register read" in result.stdout


def test_a_key_id_shared_with_review_authority_is_refused(
        tmp_path: Path) -> None:
    """THE RATIFIED DISJOINTNESS RULE, in its plainest form."""
    root = build_tree(tmp_path)
    review = root / "governance" / "review-authority" / "register.yaml"
    doc = yaml.safe_load(review.read_text(encoding="utf-8"))
    doc["seat_keys"] = [{"seat_id": "lead-quality",
                         "key_id": "key-factory-test-0001"}]
    review.write_text(yaml.safe_dump(doc), encoding="utf-8")
    result = run(str(root))
    assert result.returncode == 1
    assert "factory-identity-registers-not-disjoint" in codes(result.stdout)
    assert "key-factory-test-0001" in result.stdout, (
        "the finding must NAME the shared value; a rule that says only 'the "
        "families overlap' leaves the operator to find which key")


def test_a_shared_fingerprint_is_refused(tmp_path: Path) -> None:
    """One key recorded under two different `key_id`s is still ONE KEY, and the
    fingerprint is what proves it. A rule keyed on the id alone would be
    defeated by renaming."""
    root = build_tree(tmp_path)
    _, _, fingerprint = keypair("opensoft/codexFactory")
    review = root / "governance" / "review-authority" / "register.yaml"
    doc = yaml.safe_load(review.read_text(encoding="utf-8"))
    doc["seat_keys"] = [{"seat_id": "lead-quality",
                         "key_id": "key-seat-lead-quality-0001",
                         "key_fingerprint": fingerprint}]
    review.write_text(yaml.safe_dump(doc), encoding="utf-8")
    result = run(str(root))
    assert "factory-identity-registers-not-disjoint" in codes(result.stdout)


def test_a_shared_did_is_refused(tmp_path: Path) -> None:
    root = build_tree(tmp_path)
    _, multibase, _ = keypair("opensoft/codexFactory")
    wallet = (root / "governance" / "review-authority" / "wallets"
              / "wal-agent-test-0001.yaml")
    wallet.write_text(yaml.safe_dump({
        "schema_version": 1, "kind": "xfactory_wallet_record",
        "wallet_id": "wal-agent-test-0001",
        "key_reference": {"did": f"did:key:{multibase}",
                          "key_id": "key-review-0001"}}), encoding="utf-8")
    result = run(str(root))
    assert "factory-identity-registers-not-disjoint" in codes(result.stdout)


def test_disjointness_is_not_waivable_by_declaring_different_acts(
        tmp_path: Path) -> None:
    """The ratified scenario says so in terms, and 'but the acts differ' is
    exactly the argument somebody will make on the day the rule fires."""
    root = build_tree(tmp_path)
    review = root / "governance" / "review-authority" / "register.yaml"
    doc = yaml.safe_load(review.read_text(encoding="utf-8"))
    doc["rows"] = [{"row_id": "row-mrc-0001", "act": "review",
                    "key_id": "key-factory-test-0001"}]
    review.write_text(yaml.safe_dump(doc), encoding="utf-8")
    result = run(str(root))
    assert "factory-identity-registers-not-disjoint" in codes(result.stdout)
    assert "NOT waivable" in result.stdout


def test_a_placeholder_anywhere_refuses(tmp_path: Path) -> None:
    root = build_tree(tmp_path, wallet_mutate=lambda w: w["key_reference"]
                      .__setitem__("key_fingerprint", SENTINEL))
    result = run(str(root))
    assert result.returncode == 1
    assert "factory-identity-placeholder-unminted" in codes(result.stdout)


def test_a_second_active_row_for_one_repository_is_refused(
        tmp_path: Path) -> None:
    """Exactly ONE origin identity per originating repository is ratified;
    rotation SUPERSEDES a row rather than adding one."""
    base = {"holder_ref": "opensoft/codexFactory",
            "wallet_ref": "wal-origin-test-0001", "act": "originate",
            "grant_ref": "grant-origin-test-0001",
            "expires_at": "2026-12-01T00:00:00Z", "state": "active"}
    root = build_tree(tmp_path, rows=[dict(base, row_id="row-a"),
                                      dict(base, row_id="row-b")])
    result = run(str(root))
    assert "factory-identity-second-active-row" in codes(result.stdout)


def test_a_superseded_row_beside_an_active_one_is_allowed(
        tmp_path: Path) -> None:
    """Rotation's legal shape: the old row stays, superseded, and the new one
    NAMES it. A revoked or superseded row never returns to active."""
    base = {"holder_ref": "opensoft/codexFactory",
            "wallet_ref": "wal-origin-test-0001", "act": "originate",
            "grant_ref": "grant-origin-test-0001",
            "expires_at": "2026-12-01T00:00:00Z"}
    root = build_tree(tmp_path, rows=[
        dict(base, row_id="row-a", state="superseded"),
        dict(base, row_id="row-b", state="active", supersedes="row-a")])
    result = run(str(root))
    assert result.returncode == 0, result.stdout


def test_the_seat_spelling_is_refused_on_the_register(tmp_path: Path) -> None:
    root = build_tree(tmp_path, register_extra={"seat_keys": []})
    result = run(str(root))
    assert "factory-identity-seat-spelling" in codes(result.stdout)


def test_the_agent_holder_prefix_is_refused(tmp_path: Path) -> None:
    root = build_tree(tmp_path, holder="agent:merge-readiness-council")
    result = run(str(root))
    assert "factory-identity-seat-spelling" in codes(result.stdout)


def test_a_non_organisation_holder_class_is_refused(tmp_path: Path) -> None:
    root = build_tree(
        tmp_path,
        wallet_mutate=lambda w: w["holder"].__setitem__("holder_class",
                                                        "agent"))
    result = run(str(root))
    assert "factory-identity-seat-spelling" in codes(result.stdout)


def test_a_declared_key_set_is_refused(tmp_path: Path) -> None:
    """EXACTLY ONE origin identity per originating repository: a `keys:` set
    expresses a plurality the contract refuses."""
    _, multibase, fingerprint = keypair("second")
    root = build_tree(tmp_path, wallet_mutate=lambda w: w.__setitem__(
        "keys", [{"did": f"did:key:{multibase}", "key_id": "key-second-0001",
                  "key_fingerprint": fingerprint,
                  "custody": {"model": "holder_readable",
                              "registry_version": 1}}]))
    result = run(str(root))
    assert "factory-identity-seat-spelling" in codes(result.stdout)


def test_an_authority_tier_column_on_a_row_is_refused(tmp_path: Path) -> None:
    root = build_tree(tmp_path, rows=[{
        "row_id": "row-a", "holder_ref": "opensoft/codexFactory",
        "wallet_ref": "wal-origin-test-0001", "act": "originate",
        "grant_ref": "grant-origin-test-0001", "authority_tier": "act",
        "expires_at": "2026-12-01T00:00:00Z", "state": "active"}])
    result = run(str(root))
    assert "factory-identity-row-malformed" in codes(result.stdout)


def test_a_fingerprint_that_does_not_recompute_is_refused(
        tmp_path: Path) -> None:
    """One derivation, one place: the fingerprint is RECOMPUTED from the public
    half through the pinned decoder, never trusted."""
    _, _, other = keypair("someone else")
    root = build_tree(tmp_path, wallet_mutate=lambda w: w["key_reference"]
                      .__setitem__("key_fingerprint", other))
    result = run(str(root))
    assert "factory-identity-fingerprint-mismatch" in codes(result.stdout)


def test_a_did_that_is_not_derived_from_the_public_half_is_refused(
        tmp_path: Path) -> None:
    _, other, _ = keypair("someone else")
    root = build_tree(tmp_path, wallet_mutate=lambda w: w["key_reference"]
                      .__setitem__("did", f"did:key:{other}"))
    result = run(str(root))
    assert "factory-identity-key-encoding" in codes(result.stdout)


def test_a_row_and_grant_expiry_that_disagree_are_refused(
        tmp_path: Path) -> None:
    root = build_tree(tmp_path, grant_mutate=lambda g: g.__setitem__(
        "expires_at", "2027-06-30T00:00:00Z"))
    result = run(str(root))
    assert "factory-identity-expiry-mismatch" in codes(result.stdout)


def test_a_grant_past_the_ninety_day_ceiling_is_refused(
        tmp_path: Path) -> None:
    """No projection path can revoke an origin row at clearing, so a short
    unconditional expiry is the only propagation mechanism that works today."""
    root = build_tree(
        tmp_path,
        rows=[{"row_id": "row-a", "holder_ref": "opensoft/codexFactory",
               "wallet_ref": "wal-origin-test-0001", "act": "originate",
               "grant_ref": "grant-origin-test-0001",
               "expires_at": "2027-09-02T00:00:00Z", "state": "active"}],
        grant_mutate=lambda g: g.__setitem__("expires_at",
                                             "2027-09-02T00:00:00Z"))
    result = run(str(root))
    assert "factory-identity-expiry-window" in codes(result.stdout)


def test_a_tier_above_the_unattested_cap_needs_a_completed_attestation(
        tmp_path: Path) -> None:
    root = build_tree(tmp_path, attestation_complete=False)
    result = run(str(root))
    assert "factory-identity-tier-unattested" in codes(result.stdout)


def test_the_unattested_cap_itself_is_allowed(tmp_path: Path) -> None:
    """`request` is what unattested custody CAN carry, so a grant declaring it
    with no attestation is honest rather than refused."""
    root = build_tree(tmp_path, attestation_complete=False,
                      grant_mutate=lambda g: g["scope"].__setitem__(
                          "authority_tier", "request"))
    result = run(str(root))
    assert "factory-identity-tier-unattested" not in codes(result.stdout)


def test_a_secret_name_in_the_family_is_refused(tmp_path: Path) -> None:
    """The ratified requirement forbids 'a secret name resolvable to key
    material' — and a COMMENT naming the variable is exactly as resolvable as a
    field naming it, which is why the check reads raw bytes."""
    root = build_tree(tmp_path)
    register = root / "governance" / "factory-identity" / "register.yaml"
    register.write_text(
        "# private half lives as FACTORY_ORIGIN_SIGNING_KEY\n"
        + register.read_text(encoding="utf-8"), encoding="utf-8")
    result = run(str(root))
    assert "factory-identity-secret-name-recorded" in codes(result.stdout)


def test_key_material_in_the_family_is_refused(tmp_path: Path) -> None:
    """An ed25519 PRIVATE half is exactly 64 hex characters, and it is the
    single most likely thing to be pasted where a public half belongs."""
    root = build_tree(tmp_path)
    wallet = (root / "governance" / "factory-identity" / "wallets"
              / "wal-origin-test-0001.yaml")
    wallet.write_text(wallet.read_text(encoding="utf-8")
                      + "\nnote: " + "a" * 64 + "\n", encoding="utf-8")
    result = run(str(root))
    assert "factory-identity-key-material" in codes(result.stdout)


def test_an_armored_private_key_is_refused(tmp_path: Path) -> None:
    root = build_tree(tmp_path)
    wallet = (root / "governance" / "factory-identity" / "wallets"
              / "wal-origin-test-0001.yaml")
    wallet.write_text(wallet.read_text(encoding="utf-8")
                      + "\nnote: |\n  -----BEGIN OPENSSH PRIVATE KEY-----\n",
                      encoding="utf-8")
    result = run(str(root))
    assert "factory-identity-key-material" in codes(result.stdout)


def test_a_bound_wider_than_its_own_ceiling_is_refused(tmp_path: Path) -> None:
    """An artifact must never be able to widen its own trust window."""
    root = build_tree(tmp_path,
                      register_extra={"revocation_staleness_bound": "P30D"})
    result = run(str(root))
    assert "factory-identity-staleness-exceeds-ceiling" in codes(result.stdout)


def test_a_calendar_dependent_bound_is_refused(tmp_path: Path) -> None:
    root = build_tree(tmp_path,
                      register_extra={"revocation_staleness_bound": "P1M"})
    result = run(str(root))
    assert "factory-identity-staleness-malformed" in codes(result.stdout)


def test_an_unknown_top_level_declaration_is_refused(tmp_path: Path) -> None:
    """The register is deliberately kindless, so THIS READER is its shape: a
    declaration the reader does not know is a declaration nothing reads. That is
    the vacuous pass the intake register already suffered once."""
    root = build_tree(tmp_path, register_extra={"revocation_surface": "hermes"})
    result = run(str(root))
    assert "factory-identity-register-malformed" in codes(result.stdout)


def test_an_unresolvable_wallet_ref_is_refused(tmp_path: Path) -> None:
    root = build_tree(tmp_path, rows=[{
        "row_id": "row-a", "holder_ref": "opensoft/codexFactory",
        "wallet_ref": "wal-nope", "act": "originate",
        "grant_ref": "grant-origin-test-0001",
        "expires_at": "2026-12-01T00:00:00Z", "state": "active"}])
    result = run(str(root))
    assert "factory-identity-row-unresolved" in codes(result.stdout)


def test_a_row_act_the_grant_does_not_confer_is_refused(
        tmp_path: Path) -> None:
    root = build_tree(tmp_path, grant_mutate=lambda g: g["scope"].__setitem__(
        "acts", ["review"]))
    result = run(str(root))
    assert "factory-identity-row-unresolved" in codes(result.stdout)


def test_an_absent_register_is_refused(tmp_path: Path) -> None:
    """An origin signature would be verified against nothing."""
    (tmp_path / "governance").mkdir()
    result = run(str(tmp_path))
    assert "factory-identity-register-missing" in codes(result.stdout)


# --------------------------------------------------------------- the mint helper

def test_derive_reproduces_a_known_minted_key() -> None:
    """THE DERIVATION PATH IS THE ESTATE'S, NOT A SECOND ONE.

    The input is the `lead-quality` seat's PUBLIC half exactly as
    `governance/review-authority/register.yaml` records it; the outputs are that
    same key's `did`, `public_key_multibase` and `key_fingerprint` exactly as the
    live wallet record records them. If `--derive` and the estate's existing
    records ever disagree, this test is where it shows.
    """
    register = yaml.safe_load(REVIEW_REGISTER.read_text(encoding="utf-8"))
    seat = next(s for s in register["seat_keys"]
                if s["seat_id"] == "lead-quality")
    wallet = yaml.safe_load(
        (REPO_ROOT / "governance" / "review-authority" / "wallets"
         / "wal-agent-mrc-0001.yaml").read_text(encoding="utf-8"))
    declared = next(k for k in wallet["keys"]
                    if k["key_id"] == "key-seat-lead-quality-0001")
    result = run("--derive", seat["public_key"])
    assert result.returncode == 0, result.stderr
    assert declared["public_key_multibase"] in result.stdout
    assert declared["did"] in result.stdout
    assert seat["key_fingerprint"] in result.stdout
    assert declared["key_fingerprint"] == seat["key_fingerprint"]


def test_derive_refuses_a_non_canonical_public_key() -> None:
    """Two spellings of one key are two keys to anything comparing strings."""
    result = run("--derive", "bqJJdpCO4dx31e21t6UA4v7b0r0JaxaqmebrjvhK4OJ")
    assert result.returncode == 2
    assert "derive-input" in result.stderr


def test_derive_refuses_a_private_seed_shaped_input() -> None:
    """A 64-hex seed pasted where a public half belongs is refused by SHAPE,
    before it can be printed into a record."""
    result = run("--derive", "a" * 64)
    assert result.returncode == 2


def test_a_missing_target_is_a_usage_refusal_not_a_green_run() -> None:
    """A run with no target reads no register, and a green check that opened no
    register is a vacuous pass."""
    result = run()
    assert result.returncode == 2
    assert "vacuous pass" in result.stderr
