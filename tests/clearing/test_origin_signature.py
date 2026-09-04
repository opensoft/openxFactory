"""Field (10): the three ratified outcomes, and the key discipline behind them.

`add-cpc-clearing-boundary` closed field (10)'s disjunction ONLY where an origin
identity is registered. That makes three lawful states, and this module holds all
three apart:

  1. A REGISTERED producer with a VERIFYING signature — accepted.
  2. A REGISTERED producer presenting hosted provenance alone — refused, and the
     refusal NAMES THE MISSING ORIGIN SIGNATURE rather than reporting field (10)
     as present.
  3. An UNREGISTERED producer presenting hosted provenance — accepted exactly as
     the basis states, and the absence of a registered identity does not by
     itself refuse.

So registering an identity TIGHTENS a producer and never loosens one.

KEY DISCIPLINE. The keys here are of two kinds and neither is a secret. Where a
signature must genuinely verify, the packaged corpus carries an EPHEMERAL public
half whose private half was never written to this repository. Where only a public
value is needed, it is derived from a LABELLED sha256 digest — the practice
`tests/factory_identity/test_validator.py` states in its own words: "a reader can
see at a glance that nobody holds a private half and that no value here could be
mistaken for a real minted key."

NO TEST HERE SKIPS. `.github/workflows/pytest-suite.yml` initializes the
`openXwallet` gitlink before the suite and pins the skipped count EXACTLY, so a
directory that quietly turned into skips is the condition that pin exists to
catch.
"""

from __future__ import annotations

import copy
import hashlib

import yaml

from conftest import EXAMPLES, adjudicate

REGISTERED = EXAMPLES / "sealed-bundle-manifest-registered-producer.example.yaml"
UNREGISTERED = EXAMPLES / "sealed-bundle-manifest-unregistered-producer.example.yaml"


def _load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def unmintable_public_half(label: str, pinned, reader) -> str:
    """A multibase public value with NO private half, by construction.

    Derived from a labelled digest and round-tripped through the PINNED decoder,
    so the value is both obviously synthetic and genuinely well-formed. A
    hand-typed `did:key:z…` literal would be neither.
    """
    raw = hashlib.sha256(("clearing test / " + label).encode()).digest()
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    payload = b"\xed\x01" + raw
    number = int.from_bytes(payload, "big")
    out = ""
    while number:
        number, rest = divmod(number, 58)
        out = alphabet[rest] + out
    leading = 0
    for byte in payload:
        if byte:
            break
        leading += 1
    multibase = "z" + alphabet[0] * leading + out
    assert pinned.decode_public_key_multibase(multibase) == raw, (
        "the derived value does not round-trip through the pinned decoder"
    )
    return multibase


# ---------------------------------------------------------------- outcome 1

def test_a_registered_producer_with_a_verifying_signature_is_accepted(
        reader, registry_and_docs, entries, fixture_origins) -> None:
    doc = _load(REGISTERED)
    assert doc["origin_attestation"]["attestation_type"] == "origin_signature"
    findings = adjudicate(reader, registry_and_docs, entries, fixture_origins, doc)
    assert findings.errors == [], findings.errors
    assert findings.warnings == [], findings.warnings


def test_the_signature_really_is_checked_and_not_merely_shaped(
        reader, registry_and_docs, entries, fixture_origins) -> None:
    """One byte changes and the verification fails.

    Without this, "accepted" above would be consistent with a validator that
    looked at the signature's LENGTH. The manifest is otherwise untouched and
    remains internally consistent — which is exactly the condition the boundary
    refuses to accept as evidence.
    """
    doc = _load(REGISTERED)
    signature = doc["origin_attestation"]["signature"]
    flipped = ("B" if signature[0] != "B" else "C") + signature[1:]
    doc["origin_attestation"]["signature"] = flipped
    findings = adjudicate(reader, registry_and_docs, entries, fixture_origins, doc)
    assert "clearing-origin-signature-invalid" in reader.codes_of(findings.errors), \
        findings.errors


def test_altering_a_signed_field_breaks_the_signature(
        reader, registry_and_docs, entries, fixture_origins) -> None:
    """THE PER-FILE HASHES ARE INSIDE THE SIGNED SUBJECT.

    "The signature SHALL cover ALL TEN DECLARED FIELDS, the per-file hashes
    included, so that no field can be altered after signing without detection."
    This test alters ONE character of ONE file hash and nothing else; the
    signature must stop verifying, or that sentence is decoration.
    """
    import sys
    from conftest import REPO_ROOT
    sys.path.insert(0, str(REPO_ROOT))
    from scripts.signed_execution_chain import canonical

    doc = _load(REGISTERED)
    original = doc["selected_files"][0]["content_hash"]
    doc["selected_files"][0]["content_hash"] = original[:-1] + \
        ("0" if original[-1] != "0" else "1")

    # THE RECORDED DIGEST IS RE-COMPUTED FOR THE TAMPERED SUBJECT, so that this
    # test proves what it claims. Leaving the old digest in place would trip the
    # digest comparison first, and the signature would never be reached — a pass
    # that evidenced the digest check rather than the signature's coverage.
    doc["origin_attestation"]["manifest_digest"]["value"] = \
        canonical.digest(reader.signable_subject(doc))

    findings = adjudicate(reader, registry_and_docs, entries, fixture_origins, doc)
    assert "clearing-origin-signature-invalid" in reader.codes_of(findings.errors), \
        findings.errors


# ---------------------------------------------------------------- outcome 2

def test_a_registered_producer_offering_hosted_provenance_is_refused(
        reader, registry_and_docs, entries, fixture_origins) -> None:
    doc = _load(REGISTERED)
    doc["origin_attestation"] = {
        "attestation_type": "hosted_workflow_provenance",
        "provider": "github-actions",
        "run_id": "33999000999",
    }
    findings = adjudicate(reader, registry_and_docs, entries, fixture_origins, doc)
    codes = reader.codes_of(findings.errors)
    assert "clearing-origin-signature-missing" in codes, findings.errors
    named = reader.lines_for(findings.errors, "clearing-origin-signature-missing")
    assert any("missing origin signature" in line for line in named), (
        "the refusal must NAME the missing origin signature rather than report "
        "field (10) as present"
    )


def test_a_partial_signature_is_not_a_signed_manifest(
        reader, registry_and_docs, entries, fixture_origins) -> None:
    doc = _load(REGISTERED)
    doc["origin_attestation"]["covered_fields"] = [
        f for f in doc["origin_attestation"]["covered_fields"]
        if f != "selected_files"]
    findings = adjudicate(reader, registry_and_docs, entries, fixture_origins, doc)
    assert "clearing-origin-signature-partial" in reader.codes_of(findings.errors), \
        findings.errors


# ---------------------------------------------------------------- outcome 3

def test_an_unregistered_producer_may_present_hosted_provenance(
        reader, registry_and_docs, entries, fixture_origins) -> None:
    doc = _load(UNREGISTERED)
    assert doc["origin"]["repository"] not in fixture_origins
    findings = adjudicate(reader, registry_and_docs, entries, fixture_origins, doc)
    assert findings.errors == [], (
        "the absence of a registered identity must not by itself refuse: "
        f"{findings.errors}"
    )


def test_a_revoked_row_does_not_make_a_producer_registered(
        reader, fixture_origins) -> None:
    """Only an ACTIVE row registers a producer.

    The fixture register carries a revoked row on purpose. Registering an
    identity tightens a producer; a REVOKED identity must not silently keep the
    tighter rule in force against a key nothing can verify against, leaving that
    producer unable to present any lawful field (10) at all.
    """
    assert "opensoft/example-retired-producer" not in fixture_origins
    assert "opensoft/example-producer" in fixture_origins


# ------------------------------------------------------ the live register

def test_the_live_register_makes_codexfactory_a_registered_producer(
        live_origins) -> None:
    """The whole-tree sweep resolves REAL producers against the REAL register.

    The packaged corpus resolves against a fixture register — the live private
    halves do not exist in this repository and must not — so this is the test
    that keeps the live path from being untested. `opensoft/codexFactory` holds
    the first origin row, minted by `add-cpc-clearing-boundary`'s realization, and
    a bundle from it presenting hosted provenance alone is therefore refused.
    """
    assert "opensoft/codexFactory" in live_origins
    row = live_origins["opensoft/codexFactory"]
    assert row["act"] == "originate"
    assert row["_public_key"] is not None, (
        "the live row's public half does not decode; a key that cannot be "
        "resolved verifies nothing"
    )


def test_a_bundle_from_the_live_registered_producer_needs_a_signature(
        reader, registry_and_docs, entries, live_origins) -> None:
    doc = _load(UNREGISTERED)
    doc = copy.deepcopy(doc)
    doc["origin"]["repository"] = "opensoft/codexFactory"
    findings = adjudicate(reader, registry_and_docs, entries, live_origins, doc)
    assert "clearing-origin-signature-missing" in reader.codes_of(findings.errors), \
        findings.errors


# ------------------------------------------------------- key discipline

def test_a_synthetic_public_half_round_trips_but_signs_nothing(
        reader, registry_and_docs, entries, pinned) -> None:
    """A digest-derived key is well-formed AND unusable, which is the point.

    It decodes, it fingerprints, and no signature will ever verify against it
    because nobody holds the private half. That is what makes it safe to write
    into a fixture.
    """
    multibase = unmintable_public_half("no-private-half", pinned, reader)
    raw = pinned.decode_public_key_multibase(multibase)
    assert raw is not None and len(raw) == 32
    assert pinned.fingerprint_of_public_key(raw).startswith("sha256:")

    origins = {
        "opensoft/example-producer": {
            "row_id": "row-origin-example-producer-0001",
            "holder_ref": "opensoft/example-producer",
            "_public_key": raw,
            "_key_reference": {"key_id": "key-fixture-example-producer-0001"},
        }
    }
    # The MANIFEST is untouched — only the KEY the register resolves changes, so
    # the digest still commits to the same bytes and the only thing that can
    # fail is the verification itself.
    doc = _load(REGISTERED)
    findings = adjudicate(reader, registry_and_docs, entries, origins, doc)
    assert "clearing-origin-signature-invalid" in reader.codes_of(findings.errors), \
        findings.errors


def test_no_private_key_material_is_committed_under_the_family() -> None:
    """The family's tree holds public halves and signatures, and nothing else.

    Scanned rather than asserted, because the hazard is a convenience someone
    adds later to make a fixture reproducible — a seed beside the key, a PEM
    block, a JWK with a `d` member.
    """
    from conftest import FAMILY_DIR

    forbidden = ("PRIVATE KEY", "BEGIN OPENSSH", "private_key", "seed:",
                 "passphrase", '"d":', "'d':")
    offenders = []
    for path in sorted(FAMILY_DIR.rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for number, line in enumerate(text.splitlines(), start=1):
            # COMMENTS ARE EXEMPT. The fixture register's header says in prose
            # that it holds "no seed, no passphrase" — a scan that could not
            # tell a prohibition from a violation would force the tree to stop
            # documenting its own rule.
            if line.lstrip().startswith("#"):
                continue
            for token in forbidden:
                if token in line:
                    offenders.append(f"{path.name}:{number}: {token!r}")
    assert not offenders, offenders


# ------------------------------------------------- outcome 4: a LAPSED row

def test_a_lapsed_row_is_indexed_but_credits_nothing(reader, fixture_origins) -> None:
    """`state: active` and EXPIRED are both true at once, and both matter.

    Filtering on `state` alone was the bug: a row a human last wrote as active,
    whose declared expiry time has since passed, still credited signatures.
    Nothing revokes an origin row at clearing today — the factory-identity
    register says so in its own header, and OQ1 names four candidate projection
    shapes and chooses none — so the declared expiry is the ONLY revocation that
    propagates.
    """
    row = fixture_origins["opensoft/example-lapsed-producer"]
    assert row["state"] == "active"
    assert reader.row_has_lapsed(row, reader.NOW_SENTINEL)
    assert not reader.row_has_lapsed(
        fixture_origins["opensoft/example-producer"], reader.NOW_SENTINEL)


def test_a_lapsed_producer_is_refused_offering_hosted_provenance(
        reader, registry_and_docs, entries, fixture_origins) -> None:
    """THE DIRECTION THAT IS EASY TO GET WRONG.

    If the reader merely SKIPPED a lapsed row, this producer would look
    unregistered and hosted provenance would satisfy field (10) — an EXPIRY that
    WIDENED what a producer may present. Registering an identity tightens a
    producer and never loosens one; letting one lapse must not loosen one either.
    """
    doc = _load(UNREGISTERED)
    doc["origin"]["repository"] = "opensoft/example-lapsed-producer"
    findings = adjudicate(reader, registry_and_docs, entries, fixture_origins, doc)
    codes = reader.codes_of(findings.errors)
    assert "clearing-origin-row-expired" in codes, findings.errors
    assert "clearing-origin-signature-missing" not in codes, (
        "the lapsed-row refusal must be the one reported: a producer whose "
        "authority has run out is not merely missing a signature"
    )


def test_a_lapsed_producer_is_refused_offering_a_signature(
        reader, registry_and_docs, entries, fixture_origins) -> None:
    """The other direction: a signature is not credited against a lapsed row.

    The manifest here is the packaged registered-producer one, re-pointed at the
    lapsed holder, so the signature is well-formed and simply belongs to an
    authority that has expired.
    """
    doc = _load(REGISTERED)
    doc["origin"]["repository"] = "opensoft/example-lapsed-producer"
    findings = adjudicate(reader, registry_and_docs, entries, fixture_origins, doc)
    assert "clearing-origin-row-expired" in reader.codes_of(findings.errors), \
        findings.errors


def test_an_unexpired_row_is_not_reported_as_lapsed(
        reader, registry_and_docs, entries, fixture_origins) -> None:
    """The negative branch, so the predicate is not just always-true."""
    doc = _load(REGISTERED)
    findings = adjudicate(reader, registry_and_docs, entries, fixture_origins, doc)
    assert findings.errors == [], findings.errors


def test_the_live_codexfactory_row_has_not_lapsed(reader, live_origins) -> None:
    """A live-register canary with a real deadline.

    codexFactory's origin grant runs to 2026-12-02. When it lapses this assertion
    goes red — deliberately: at that moment the key stops evidencing that the
    repository acted, and the register needs a governed rotation rather than a
    quieter test.
    """
    from datetime import datetime, timezone

    row = live_origins["opensoft/codexFactory"]
    assert not reader.row_has_lapsed(row, datetime.now(timezone.utc)), (
        f"the live origin row expired at {row.get('expires_at')}. Supersede it "
        f"with a new row naming it, or mark it revoked — a revoked row never "
        f"returns to active"
    )
