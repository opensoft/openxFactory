"""T042 — assignment-bound key registration, signed returns and completion
(feature 035, Phase 4, PR-4).

Data-model E6 (the challenge), E7 (the registration), E8 (the return and the
completion order) and E9 (the two signing contexts), with E7 step 5's claim
checks against the holder's binding (E10), under Brett Heap's rulings:

* OPEN-1 (2026-10-08), "600 s challenge, 6 h assignment (Recommended)": a
  challenge's lifetime is greater than 0 and at most 600 seconds. That is the
  CONTRACT ceiling; a consumer's tighter value applies when it issues a
  challenge and never changes an outcome here (research R12).
* OPEN-3 follow-up 3 (2026-10-08), "At or after the frozen rev
  (Recommended)": at E7 step 5, a seat job's workflow commit before the frozen
  revision, or off the governed history, is `workflow_revision_ungoverned`.
* 025 ruling (A) (2026-10-09), "Per-seat environments (Recommended)": the
  claims-against-binding cases use one binding per seat, told apart by the
  seat's environment in the OIDC `sub`, with `principal_ref` equal to the
  binding id (see `signing_fixtures`).

THE SIGNED BYTES ARE THE UTF-8 OF THE CONTEXT'S `xfc-jcs-sha256-1`
SERIALIZATION, with no framing (research R3). Two of the known answers below
are written out BY HAND, one registration context and one return context, so
the code is never checked only against itself (N9).

Every order is normative: the first failing check names the outcome, and the
multi-defect cases pin each adjacent pair of steps (research R21).

The module under test is imported as `scripts.council_convening.signing`,
never under a bare name (see this package's `__init__.py`).
"""

from __future__ import annotations

import copy
import hashlib
import inspect

import pytest
import yaml

from scripts.council_convening import assignments, signing
from scripts.council_convening.records import Refused
from scripts.signed_execution_chain import canonical, ed25519

from . import signing_fixtures as fx
from .conftest import FAMILY, PROTOCOL_REGISTRY, SHARED_DEFINITIONS


def refusal(callable_, *args, **kwargs) -> str:
    with pytest.raises(Refused) as caught:
        callable_(*args, **kwargs)
    return caught.value.code


def register(case: dict) -> dict:
    return signing.check_registration(
        case["registration"], snapshot=case["snapshot"], bindings=case["bindings"],
        environment=case["environment"], evaluation_time=case["evaluation_time"],
        selected_protocol=case["selected_protocol"])


def give_return(case: dict) -> dict:
    return signing.check_return(
        case["return"], snapshot=case["snapshot"], environment=case["environment"],
        evaluation_time=case["evaluation_time"], selected_protocol=case["selected_protocol"])


def complete(case: dict, **kwargs) -> dict:
    return signing.check_completion(case["snapshot"], case["returns"], **kwargs)


def resign(case: dict) -> dict:
    """Re-sign the presented registration context, so a case shows that a
    VALID signature over a wrong context still refuses."""
    fx.sign_registration(case["registration"], case["signer"])
    return case


def issued_challenge(case: dict) -> dict:
    return case["environment"]["issued"]["challenges"][0]


def holder_of(case: dict, seat: str = "seat-a") -> dict:
    return fx.frozen_assignment(case["snapshot"], seat)["holder"]


# =============================================================================
# The contract values the module reads, and the one fingerprint spelling.
# =============================================================================


def test_the_signing_contexts_are_the_registrys():
    registry = yaml.safe_load(PROTOCOL_REGISTRY.read_text(encoding="utf-8"))
    replacement = next(p for p in registry["protocols"] if p["role"] == "replacement")
    assert signing.REGISTRATION_CONTEXT == fx.REGISTRATION_CONTEXT
    assert signing.RETURN_CONTEXT == fx.RETURN_CONTEXT
    assert [signing.REGISTRATION_CONTEXT, signing.RETURN_CONTEXT] == replacement["signing_contexts"]


def test_the_ruled_challenge_ceiling_is_600_seconds_and_is_read_from_the_contract():
    # OPEN-1. The module takes the ceiling from the landed schema, so the contract
    # and the reference implementation cannot hold two values.
    schema = yaml.safe_load((FAMILY / "registration-challenge.schema.yaml").read_text(encoding="utf-8"))
    assert schema["$defs"]["lifetime_ceiling_seconds"] == {
        "description": schema["$defs"]["lifetime_ceiling_seconds"]["description"],
        "const": fx.CHALLENGE_CEILING}
    assert signing.CHALLENGE_LIFETIME_CEILING_SECONDS == fx.CHALLENGE_CEILING
    assert signing.contract_challenge_ceiling() == fx.CHALLENGE_CEILING


#: Phase 4's refusal codes (T046), in data-model § Refusal vocabulary order. The
#: E10 codes registration also reaches at E7 step 5 are Phase 5's (T053).
PHASE_4_CODES = [
    "assignment_unknown", "assignment_not_yet_valid", "assignment_expired",
    "operation_not_permitted", "challenge_malformed", "challenge_unknown",
    "challenge_wrong_assignment", "challenge_consumed", "challenge_expired",
    "registration_malformed", "root_authorization_refused", "wrong_principal",
    "fingerprint_mismatch", "assignment_already_registered", "shared_key",
    "cross_protocol_context", "cross_convening_context", "cross_seat_context",
    "proof_invalid", "return_malformed", "return_unregistered", "return_key_mismatch",
    "return_digest_mismatch", "return_signature_invalid", "return_replayed",
    "return_unlisted", "return_duplicate", "return_missing", "completion_set_mismatch",
    "binding_unresolved", "broker_capability_insufficient"]


def test_the_phase_4_codes_extend_the_closed_refusal_vocabulary_in_one_run():
    # The enumeration grows by phase in landing order (1, 2, 3, 5, 4, 6); Phase
    # 4's codes are one contiguous run in their own order, wherever it begins.
    enum = yaml.safe_load(SHARED_DEFINITIONS.read_text(encoding="utf-8"))[
        "$defs"]["refusal_code"]["enum"]
    start = enum.index(PHASE_4_CODES[0])
    assert enum[start:start + len(PHASE_4_CODES)] == PHASE_4_CODES
    assert len(set(enum)) == len(enum)


def test_the_payload_bound_is_one_mebibyte_and_is_read_from_the_contract():
    schema = yaml.safe_load((FAMILY / "seat-return.schema.yaml").read_text(encoding="utf-8"))
    assert schema["$defs"]["payload_limit_bytes"]["const"] == fx.PAYLOAD_LIMIT
    assert signing.PAYLOAD_LIMIT_BYTES == fx.PAYLOAD_LIMIT


def test_the_fingerprint_is_the_estate_spelling_with_a_known_answer():
    # RFC 8032 section 7.1 TEST 1's public key; the answer was computed with
    # hashlib outside this module and written here as a literal.
    public_key = bytes.fromhex(
        "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a")
    assert signing.fingerprint_of(public_key) == (
        "sha256:21fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9")
    assert signing.fingerprint_of(public_key) == "sha256:" + hashlib.sha256(public_key).hexdigest()
    assert signing.fingerprint_of(public_key) != "sha256:" + public_key.hex()


@pytest.mark.parametrize("length", [0, 31, 33, 64])
def test_a_fingerprint_is_only_of_a_32_byte_key(length):
    with pytest.raises(ValueError):
        signing.fingerprint_of(b"\x01" * length)


def test_the_generators_labelled_test_key_uses_the_same_spelling():
    signer = fx.key("seat-a")
    assert signer.fingerprint == signing.fingerprint_of(signer.public_key)


# =============================================================================
# Signed bytes: the JCS bytes of the context, with hand-authored answers (N9).
# =============================================================================

HAND_CANDIDATE = {"repository": "example-owner/example-candidate", "pull_number": 7,
                  "head_sha": "1" * 40}
HAND_NONCE = "A" * 42 + "E"

HAND_REGISTRATION_CONTEXT = {
    "signing_context": "xfc-resolved-council-1/seat-key-registration",
    "protocol": "xfc-resolved-council-1",
    "convening_id": "convening-0001",
    "convening_digest": "sha256:" + "a" * 64,
    "council_id": "council-alpha",
    "candidate": HAND_CANDIDATE,
    "assignment_id": "assignment-seat-a",
    "seat_id": "seat-a",
    "key_fingerprint": "sha256:" + "b" * 64,
    "challenge_id": "challenge-seat-a",
    "challenge_nonce": HAND_NONCE,
}

#: Written out BY HAND from RFC 8785's rules (members sorted by UTF-16 code
#: unit, no whitespace), never produced by `canonical.serialize`.
HAND_REGISTRATION_BYTES = (
    b'{"assignment_id":"assignment-seat-a",'
    b'"candidate":{"head_sha":"1111111111111111111111111111111111111111",'
    b'"pull_number":7,"repository":"example-owner/example-candidate"},'
    b'"challenge_id":"challenge-seat-a",'
    b'"challenge_nonce":"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE",'
    b'"convening_digest":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",'
    b'"convening_id":"convening-0001",'
    b'"council_id":"council-alpha",'
    b'"key_fingerprint":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",'
    b'"protocol":"xfc-resolved-council-1",'
    b'"seat_id":"seat-a",'
    b'"signing_context":"xfc-resolved-council-1/seat-key-registration"}')

HAND_RETURN_CONTEXT = {
    "signing_context": "xfc-resolved-council-1/seat-return",
    "protocol": "xfc-resolved-council-1",
    "convening_id": "convening-0001",
    "convening_digest": "sha256:" + "a" * 64,
    "council_id": "council-alpha",
    "candidate": HAND_CANDIDATE,
    "assignment_id": "assignment-seat-a",
    "seat_id": "seat-a",
    "key_fingerprint": "sha256:" + "b" * 64,
    "return_digest": "sha256:" + "c" * 64,
}

HAND_RETURN_BYTES = (
    b'{"assignment_id":"assignment-seat-a",'
    b'"candidate":{"head_sha":"1111111111111111111111111111111111111111",'
    b'"pull_number":7,"repository":"example-owner/example-candidate"},'
    b'"convening_digest":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",'
    b'"convening_id":"convening-0001",'
    b'"council_id":"council-alpha",'
    b'"key_fingerprint":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",'
    b'"protocol":"xfc-resolved-council-1",'
    b'"return_digest":"sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",'
    b'"seat_id":"seat-a",'
    b'"signing_context":"xfc-resolved-council-1/seat-return"}')

#: A payload and its canonical bytes, by hand: a decimal quantity is a string.
HAND_PAYLOAD = {"seat": "seat-a", "entry": {"cost": "12.5", "turns": 3}}
HAND_PAYLOAD_BYTES = b'{"entry":{"cost":"12.5","turns":3},"seat":"seat-a"}'


def test_the_registration_signed_bytes_match_the_hand_authored_answer():
    assert signing.signed_bytes(HAND_REGISTRATION_CONTEXT) == HAND_REGISTRATION_BYTES


def test_the_return_signed_bytes_match_the_hand_authored_answer():
    assert signing.signed_bytes(HAND_RETURN_CONTEXT) == HAND_RETURN_BYTES


def test_the_return_digest_matches_the_hand_authored_answer():
    assert signing.return_digest(HAND_PAYLOAD) == {
        "construction": "xfc-jcs-sha256-1",
        "subject": "council_seat_return_payload",
        "value": "sha256:" + hashlib.sha256(HAND_PAYLOAD_BYTES).hexdigest(),
    }


def test_signed_bytes_are_the_one_construction_and_no_second_framing():
    context = fx.registration_case()["registration"]["context"]
    assert signing.signed_bytes(context) == canonical.serialize(context).encode("utf-8")
    assert signing.signed_bytes(context).startswith(b"{")


def test_signed_bytes_refuse_a_value_the_construction_cannot_serialize():
    with pytest.raises(canonical.ConstructionError):
        signing.signed_bytes(dict(HAND_RETURN_CONTEXT, seat_id=1.5))


# =============================================================================
# Contexts are rebuilt from frozen state, never taken from the record.
# =============================================================================


def test_the_registration_context_is_rebuilt_from_the_assignment_the_challenge_and_the_key():
    case = fx.registration_case()
    frozen = fx.frozen_assignment(case["snapshot"], "seat-a")
    issued = issued_challenge(case)
    fpr = fx.fingerprint(case["signer"].public_key)
    assert signing.registration_context(frozen, issued, fpr) == fx.registration_context(
        frozen, issued, fpr)


def test_the_return_context_is_rebuilt_from_the_assignment_the_key_and_the_digest():
    case = fx.return_case()
    frozen = fx.frozen_assignment(case["snapshot"], "seat-a")
    fpr = fx.fingerprint(case["signer"].public_key)
    value = case["return"]["return_digest"]["value"]
    assert signing.return_context(frozen, fpr, value) == fx.return_context(frozen, fpr, value)


def test_the_contexts_carry_exactly_the_data_model_e9_members():
    case = fx.registration_case()
    frozen = fx.frozen_assignment(case["snapshot"], "seat-a")
    shared = {"signing_context", "protocol", "convening_id", "convening_digest", "council_id",
              "candidate", "assignment_id", "seat_id", "key_fingerprint"}
    assert set(signing.registration_context(frozen, issued_challenge(case), "sha256:" + "0" * 64)) == (
        shared | {"challenge_id", "challenge_nonce"})
    assert set(signing.return_context(frozen, "sha256:" + "0" * 64, "sha256:" + "1" * 64)) == (
        shared | {"return_digest"})


# =============================================================================
# Registration: the accepted case and its derived values.
# =============================================================================


def test_a_well_formed_registration_is_accepted_with_its_derived_values():
    case = fx.registration_case()
    derived = register(case)
    assert derived == {
        "key_fingerprint": fx.fingerprint(case["signer"].public_key),
        "signed_bytes": fx.b64url(fx.jcs(case["registration"]["context"])),
    }


def test_each_seat_registers_against_its_own_binding():
    for seat in fx.SEATS:
        assert register(fx.registration_case(seat))["key_fingerprint"] == fx.fingerprint(
            fx.key(seat).public_key)


def test_a_binding_shared_by_two_seats_with_distinct_principals_freezes_today():
    # PINS CURRENT BEHAVIOUR, which an owner ruling may tighten (pre-review of
    # 03cb77e29, M2). E4 step 7 refuses only a repeated `holder.principal_ref`,
    # so two seats whose holders share one `binding_ref` and name distinct
    # `principal_ref`s freeze, and E7 step 5 then resolves both to that one
    # binding. Per-seat isolation then rests on the dispatcher's principal.
    shared_binding = fx.snapshot()
    for item in shared_binding["assignments"]:
        item["holder"]["binding_ref"] = fx.binding_id("seat-a")
    assignments.check_snapshot(shared_binding)

    shared_principal = fx.snapshot()
    for item in shared_principal["assignments"]:
        item["holder"]["principal_ref"] = fx.binding_id("seat-a")
    with pytest.raises(Refused) as caught:
        assignments.check_snapshot(shared_principal)
    assert caught.value.code == "assignment_shared_holder"

    # So at registration, seat-a's job registers for seat-b once the dispatcher
    # names seat-b's principal: the shared binding admits seat-a's subject.
    case = fx.registration_case("seat-b")
    for item in case["snapshot"]["assignments"]:
        item["holder"]["binding_ref"] = fx.binding_id("seat-a")
    case["environment"]["identity"] = fx.identity("seat-a")
    case["environment"]["identity"]["principal"]["principal_ref"] = fx.binding_id("seat-b")
    assert register(case)["key_fingerprint"] == fx.fingerprint(fx.key("seat-b").public_key)


def test_registration_verifies_the_proof_with_the_stdlib_verifier(monkeypatch):
    calls = []
    real = ed25519.verify

    def spy(public_key, message, signature):
        calls.append((public_key, message, signature))
        return real(public_key, message, signature)

    monkeypatch.setattr(ed25519, "verify", spy)
    case = fx.registration_case()
    register(case)
    assert calls == [(case["signer"].public_key, fx.jcs(case["registration"]["context"]),
                      fx.b64url_decode(case["registration"]["proof"]))]


def test_the_module_imports_no_signing_library():
    # Verification is stdlib-only (research R18); `cryptography` signs fixtures
    # in the generator and nowhere else.
    source = inspect.getsource(signing)
    assert "cryptography" not in source.replace("# ", "")
    assert not hasattr(signing, "Ed25519PrivateKey")


# =============================================================================
# Registration, E7 steps 1 and 2: classification, then root authorization.
# =============================================================================


def test_a_legacy_root_authorized_registration_under_the_replacement_is_refused_first():
    # E7 step 1 before step 2: a record with no `protocol` that carries root
    # members classifies as LEGACY (recognition rule (c)), so it is refused as
    # legacy, never judged as a replacement record.
    case = fx.registration_case()
    del case["registration"]["protocol"]
    case["registration"]["root_signature"] = "A" * 85 + "Q"
    assert refusal(register, case) == "legacy_protocol_refused"


def test_an_unknown_protocol_is_protocol_unknown():
    case = fx.registration_case()
    case["registration"]["protocol"] = "xfc-resolved-council-2"
    assert refusal(register, case) == "protocol_unknown"


def test_a_replacement_registration_under_a_legacy_selection_is_not_selected():
    case = fx.registration_case()
    case["selected_protocol"] = fx.LEGACY
    case["environment"]["registry_status"] = {fx.LEGACY: "in_use"}
    assert refusal(register, case) == "protocol_not_selected"


@pytest.mark.parametrize("member", ["root_key_fingerprint", "root_signature", "authorization"])
def test_root_authorization_on_a_replacement_record_is_refused(member):
    # I3: a record carrying the replacement `protocol` is a replacement record
    # whatever else it carries, and its root members are refused, never routed.
    case = fx.registration_case()
    case["registration"][member] = "sha256:" + "ab" * 32
    assert refusal(register, case) == "root_authorization_refused"


def test_root_authorization_is_refused_before_the_shape():
    case = fx.registration_case()
    case["registration"]["root_signature"] = "A" * 85 + "Q"
    del case["registration"]["proof"]
    assert refusal(register, case) == "root_authorization_refused"


# =============================================================================
# Registration, E7 step 3: the shape, including key transport (N18).
# =============================================================================


@pytest.mark.parametrize("mutate", [
    pytest.param(lambda r: r.pop("proof"), id="proof-missing"),
    pytest.param(lambda r: r.update(principal="binding-seat-a"), id="a-principal-in-the-body"),
    pytest.param(lambda r: r.update(kind="xfactory_council_seat_return"), id="wrong-kind"),
    pytest.param(lambda r: r.update(public_key="A" * 42 + "B"), id="public_key-nonzero-pad-bits"),
    pytest.param(lambda r: r.update(proof="A" * 84), id="proof-not-64-bytes"),
    pytest.param(lambda r: r.update(assignment_id="assignment-seat-a\n"),
                 id="assignment_id-trailing-newline"),
    pytest.param(lambda r: r["context"].pop("challenge_nonce"), id="context-not-a-registration-context"),
    pytest.param(lambda r: r["context"].update(return_digest="sha256:" + "c" * 64),
                 id="context-carries-a-return-member"),
    pytest.param(lambda r: r["context"]["candidate"].update(pull_number=True),
                 id="candidate-pull_number-boolean"),
])
def test_a_registration_that_fails_its_schema_is_registration_malformed(mutate):
    case = fx.registration_case()
    mutate(case["registration"])
    assert refusal(register, case) == "registration_malformed"


@pytest.mark.parametrize("name", ["private_key", "secret_key", "seed", "sk", "d"])
@pytest.mark.parametrize("where", ["top", "context", "candidate"])
def test_key_transport_by_member_name_is_refused_at_any_depth(name, where):
    case = fx.registration_case()
    target = {"top": case["registration"], "context": case["registration"]["context"],
              "candidate": case["registration"]["context"]["candidate"]}[where]
    target[name] = "A" * 43
    assert refusal(register, case) == "registration_malformed"


def test_key_transport_as_a_pem_private_key_block_is_refused():
    case = fx.registration_case()
    case["registration"]["context"]["council_id"] = fx.pem_private_key_block()
    assert refusal(register, case) == "registration_malformed"


def test_the_key_transport_scan_names_the_member_and_never_echoes_the_value():
    value = {"outer": [{"inner": {"seed": "Z" * 43}}]}
    with pytest.raises(Refused) as caught:
        signing.refuse_key_transport(value, "registration_malformed")
    assert caught.value.code == "registration_malformed"
    assert "Z" * 43 not in str(caught.value)


def test_the_shape_is_checked_before_the_assignment():
    case = fx.registration_case()
    case["registration"]["assignment_id"] = "assignment-nobody"
    del case["registration"]["proof"]
    assert refusal(register, case) == "registration_malformed"


# =============================================================================
# Registration, E7 step 4: the assignment, when it is used.
# =============================================================================


def test_an_assignment_not_in_the_snapshot_is_assignment_unknown():
    case = fx.registration_case()
    case["registration"]["assignment_id"] = "assignment-nobody"
    assert refusal(register, case) == "assignment_unknown"


def test_an_assignment_before_its_not_before_is_not_yet_valid():
    case = fx.registration_case()
    case["evaluation_time"] = "2026-10-08T23:59:59Z"
    assert refusal(register, case) == "assignment_not_yet_valid"


@pytest.mark.parametrize("instant", ["2026-10-09T06:00:00Z", "2026-10-09T06:00:01Z"])
def test_an_assignment_is_expired_at_the_instant_and_after(instant):
    case = fx.registration_case()
    case["evaluation_time"] = instant
    assert refusal(register, case) == "assignment_expired"


def test_a_registration_against_a_return_only_assignment_is_not_permitted():
    case = fx.registration_case()
    fx.frozen_assignment(case["snapshot"], "seat-a")["permitted_operations"] = ["seat_return"]
    assert refusal(register, case) == "operation_not_permitted"


def test_the_assignment_checks_run_in_their_order():
    case = fx.registration_case()
    frozen = fx.frozen_assignment(case["snapshot"], "seat-a")
    frozen["permitted_operations"] = ["seat_return"]
    case["evaluation_time"] = "2026-10-09T06:00:00Z"
    assert refusal(register, case) == "assignment_expired"          # before not-permitted
    case["evaluation_time"] = "2026-10-08T23:00:00Z"
    assert refusal(register, case) == "assignment_not_yet_valid"     # before expiry


# =============================================================================
# Registration, E7 step 5: the principal, against the holder's own binding.
# Per-seat bindings, under 025 ruling (A).
# =============================================================================


def test_a_binding_ref_that_resolves_to_nothing_is_binding_unresolved():
    case = fx.registration_case()
    holder_of(case).update(binding_ref="binding-nobody")
    assert refusal(register, case) == "binding_unresolved"


def test_a_binding_ref_resolves_only_against_the_configured_bindings():
    case = fx.registration_case()
    case["bindings"] = [fx.binding("seat-b")]
    assert refusal(register, case) == "binding_unresolved"


def test_a_governed_broker_job_holder_is_broker_capability_insufficient():
    # No binding shape exists for a broker holder yet, so it refuses rather
    # than borrowing an OIDC job's checks.
    case = fx.registration_case()
    holder_of(case).update(principal_kind="governed_broker_job")
    assert refusal(register, case) == "broker_capability_insufficient"


def test_an_unresolved_binding_is_named_before_the_broker_holder():
    case = fx.registration_case()
    holder_of(case).update(principal_kind="governed_broker_job", binding_ref="binding-nobody")
    assert refusal(register, case) == "binding_unresolved"


def test_a_stub_binding_is_binding_malformed():
    case = fx.registration_case()
    case["bindings"][0]["instantiation_stub"] = True
    assert refusal(register, case) == "binding_malformed"


def test_decoded_but_unverified_claims_are_claims_unverified():
    case = fx.registration_case()
    case["environment"]["identity"]["verified"] = False
    assert refusal(register, case) == "claims_unverified"


@pytest.mark.parametrize("claims", [
    pytest.param({"exp": fx.EVALUATION_EPOCH}, id="exp-at-the-instant"),
    pytest.param({"exp": fx.EVALUATION_EPOCH - 1}, id="exp-before"),
    pytest.param({"nbf": fx.EVALUATION_EPOCH + 1}, id="nbf-after"),
])
def test_a_token_outside_its_window_is_claims_expired(claims):
    case = fx.registration_case()
    case["environment"]["identity"]["claims"].update(claims)
    assert refusal(register, case) == "claims_expired"


def test_another_audience_is_audience_mismatch():
    case = fx.registration_case()
    case["environment"]["identity"]["claims"]["aud"] = "another-consumer"
    assert refusal(register, case) == "audience_mismatch"


def test_another_seats_job_cannot_register_for_this_seat():
    # Per-seat isolation: seat B's job, whose `sub` names seat B's environment,
    # presents claims against seat A's assignment. Seat A's binding names seat
    # A's environment, so the claims fail against it.
    case = fx.registration_case("seat-a")
    case["environment"]["identity"] = fx.identity("seat-b")
    assert refusal(register, case) == "subject_template_mismatch"


def test_a_seat_job_at_the_frozen_revision_is_accepted():
    case = fx.registration_case()
    case["environment"]["identity"]["claims"]["job_workflow_sha"] = fx.SHA_REVISION
    register(case)


@pytest.mark.parametrize("sha", [
    pytest.param(fx.SHA_BEFORE, id="before-the-frozen-revision"),
    pytest.param(fx.SHA_OFF, id="off-the-governed-history"),
])
def test_a_seat_workflow_commit_outside_the_seat_rule_is_ungoverned(sha):
    # OPEN-3 follow-up 3, "At or after the frozen rev (Recommended)".
    case = fx.registration_case()
    case["environment"]["identity"]["claims"]["job_workflow_sha"] = sha
    assert refusal(register, case) == "workflow_revision_ungoverned"


def test_the_seat_rule_reads_the_snapshots_frozen_revision():
    # The seat commit is judged against the revision the snapshot froze, so a
    # snapshot frozen at a LATER revision refuses the same seat commit.
    case = fx.registration_case()
    case["snapshot"]["convening"]["required_seats_provenance"]["governed"]["revision"] = fx.SHA_SEAT
    case["environment"]["identity"]["claims"]["job_workflow_sha"] = fx.SHA_REVISION
    case["environment"]["governed_history"][f"{fx.GOVERNED_REPOSITORY}@{fx.SHA_REVISION}"] = {
        "on_first_parent": True, "at_or_after": []}
    assert refusal(register, case) == "workflow_revision_ungoverned"


def test_a_valid_proof_from_the_wrong_principal_is_wrong_principal():
    # The claims satisfy the holder's binding and the proof is valid, but the
    # principal the dispatcher resolved is not the assignment's holder.
    case = fx.registration_case()
    case["environment"]["identity"]["principal"]["principal_ref"] = fx.binding_id("seat-b")
    assert refusal(register, case) == "wrong_principal"


def test_a_principal_of_another_kind_is_wrong_principal():
    case = fx.registration_case()
    case["environment"]["identity"]["principal"]["principal_kind"] = "governed_broker_job"
    assert refusal(register, case) == "wrong_principal"


def test_the_principal_checks_run_in_their_order():
    case = fx.registration_case()
    case["environment"]["identity"]["principal"]["principal_ref"] = fx.binding_id("seat-b")
    case["environment"]["identity"]["claims"]["aud"] = "another-consumer"
    assert refusal(register, case) == "audience_mismatch"           # claims before principal
    case["environment"]["identity"]["verified"] = False
    assert refusal(register, case) == "claims_unverified"
    case["bindings"][0]["instantiation_stub"] = True
    assert refusal(register, case) == "binding_malformed"           # binding before claims
    holder_of(case).update(binding_ref="binding-nobody")
    assert refusal(register, case) == "binding_unresolved"


# =============================================================================
# Registration, E7 step 6: the issued challenge.
# =============================================================================


def test_a_challenge_nobody_issued_is_challenge_unknown():
    case = fx.registration_case()
    case["environment"]["issued"]["challenges"] = []
    assert refusal(register, case) == "challenge_unknown"


@pytest.mark.parametrize("expires_at, outcome", [
    pytest.param("2026-10-09T01:05:00Z", None, id="exactly-600-seconds-accepted"),
    pytest.param("2026-10-09T01:05:01Z", "challenge_malformed", id="601-seconds"),
    pytest.param("2026-10-09T00:55:00Z", "challenge_malformed", id="zero"),
    pytest.param("2026-10-09T00:54:59Z", "challenge_malformed", id="negative"),
])
def test_the_challenge_lifetime_is_bounded_by_the_contract_ceiling(expires_at, outcome):
    # OPEN-1, at the contract ceiling: a consumer's tighter configured value
    # applies when it issues, and never changes this outcome (R12).
    case = fx.registration_case()
    issued_challenge(case)["expires_at"] = expires_at
    if outcome is None:
        register(case)
    else:
        assert refusal(register, case) == outcome


@pytest.mark.parametrize("mutate", [
    pytest.param(lambda c: c.pop("nonce"), id="nonce-missing"),
    pytest.param(lambda c: c.update(extra=True), id="unknown-member"),
    pytest.param(lambda c: c.update(kind="xfactory_council_seat_key_registration"), id="wrong-kind"),
    pytest.param(lambda c: c.update(issued_at="2026-10-09T00:55:00+00:00"), id="not-a-utc_instant"),
])
def test_an_issued_challenge_that_fails_e6_is_challenge_malformed(mutate):
    case = fx.registration_case()
    mutate(issued_challenge(case))
    assert refusal(register, case) == "challenge_malformed"


def test_a_challenge_for_another_assignment_is_challenge_wrong_assignment():
    case = fx.registration_case()
    issued_challenge(case)["assignment_id"] = fx.assignment_id("seat-b")
    assert refusal(register, case) == "challenge_wrong_assignment"


def test_a_consumed_challenge_is_challenge_consumed():
    case = fx.registration_case()
    case["environment"]["issued"]["consumed_challenges"] = [fx.challenge_id("seat-a")]
    assert refusal(register, case) == "challenge_consumed"


@pytest.mark.parametrize("instant", ["2026-10-09T01:05:00Z", "2026-10-09T01:05:30Z"])
def test_a_challenge_is_expired_at_the_instant_and_after(instant):
    case = fx.registration_case()
    case["evaluation_time"] = instant
    assert refusal(register, case) == "challenge_expired"


def test_the_challenge_checks_run_in_their_order():
    case = fx.registration_case()
    issued = issued_challenge(case)
    case["evaluation_time"] = "2026-10-09T01:05:00Z"
    case["environment"]["issued"]["consumed_challenges"] = [fx.challenge_id("seat-a")]
    assert refusal(register, case) == "challenge_consumed"           # before expiry
    issued["assignment_id"] = fx.assignment_id("seat-b")
    assert refusal(register, case) == "challenge_wrong_assignment"   # before consumed
    issued["expires_at"] = "2026-10-09T01:05:01Z"
    assert refusal(register, case) == "challenge_malformed"          # before wrong assignment


def test_the_challenge_alone_is_checked_against_e6():
    issued = fx.challenge("seat-a", fx.key("seat-a").public_key)
    signing.check_challenge(issued)
    issued["expires_at"] = "2026-10-09T01:05:01Z"
    assert refusal(signing.check_challenge, issued) == "challenge_malformed"


# =============================================================================
# Registration, E7 step 7: the key.
# =============================================================================


def test_a_fingerprint_that_does_not_recompute_is_fingerprint_mismatch():
    case = fx.registration_case()
    case["registration"]["key_fingerprint"] = "sha256:" + "ab" * 32
    assert refusal(register, case) == "fingerprint_mismatch"


def test_a_key_other_than_the_one_the_challenge_was_issued_for_is_fingerprint_mismatch():
    case = fx.registration_case()
    issued_challenge(case)["key_fingerprint"] = fx.fingerprint(fx.key("seat-a", 2).public_key)
    assert refusal(register, case) == "fingerprint_mismatch"


def test_a_second_registration_for_the_assignment_is_already_registered():
    case = fx.registration_case()
    case["environment"]["issued"]["registered_keys"] = [
        fx.registered_key("seat-a", fx.key("seat-a", 2))]
    assert refusal(register, case) == "assignment_already_registered"


def test_a_key_registered_for_another_seat_is_shared_key():
    case = fx.registration_case()
    case["environment"]["issued"]["registered_keys"] = [
        dict(fx.registered_key("seat-a", case["signer"]), assignment_id=fx.assignment_id("seat-b"))]
    assert refusal(register, case) == "shared_key"


def test_the_key_checks_run_in_their_order():
    case = fx.registration_case()
    case["environment"]["issued"]["registered_keys"] = [
        fx.registered_key("seat-a", case["signer"]),
        dict(fx.registered_key("seat-a", case["signer"]), assignment_id=fx.assignment_id("seat-b"))]
    assert refusal(register, case) == "assignment_already_registered"   # before shared key
    case["registration"]["key_fingerprint"] = "sha256:" + "ab" * 32
    assert refusal(register, case) == "fingerprint_mismatch"            # before already registered


# =============================================================================
# Registration, E7 step 8: the context, rebuilt and compared member by member.
# Each case RE-SIGNS the presented context, so a valid signature over the wrong
# context is shown to refuse: the presented labels are never trusted.
# =============================================================================


@pytest.mark.parametrize("member, value, code", [
    pytest.param("signing_context", fx.RETURN_CONTEXT, "cross_protocol_context",
                 id="the-return-context-string"),
    pytest.param("signing_context", fx.LEGACY_KEY_AUTHORIZATION_CONTEXT, "cross_protocol_context",
                 id="a-legacy-context-string"),
    pytest.param("protocol", fx.LEGACY, "cross_protocol_context", id="the-legacy-protocol"),
    pytest.param("convening_id", "convening-0002", "cross_convening_context", id="convening_id"),
    pytest.param("convening_digest", "sha256:" + "d" * 64, "cross_convening_context",
                 id="convening_digest"),
    pytest.param("council_id", "council-beta", "cross_convening_context", id="council_id"),
    pytest.param("candidate", dict(repository=fx.CANDIDATE_REPOSITORY, pull_number=8,
                                   head_sha=fx.SHA_HEAD), "cross_convening_context",
                 id="candidate"),
    pytest.param("assignment_id", fx.assignment_id("seat-b"), "cross_seat_context",
                 id="assignment_id"),
    pytest.param("seat_id", "seat-b", "cross_seat_context", id="seat_id"),
    pytest.param("key_fingerprint", "sha256:" + "ab" * 32, "fingerprint_mismatch",
                 id="key_fingerprint"),
    pytest.param("challenge_id", "challenge-seat-b", "challenge_wrong_assignment",
                 id="challenge_id"),
    pytest.param("challenge_nonce", fx.nonce("seat-b"), "challenge_wrong_assignment",
                 id="challenge_nonce"),
])
def test_a_context_member_that_differs_from_frozen_state_names_its_code(member, value, code):
    case = fx.registration_case()
    case["registration"]["context"][member] = value
    resign(case)
    assert refusal(register, case) == code


def test_the_context_comparison_runs_in_its_order():
    case = fx.registration_case()
    context = case["registration"]["context"]
    context["challenge_nonce"] = fx.nonce("seat-b")
    context["seat_id"] = "seat-b"
    resign(case)
    assert refusal(register, case) == "cross_seat_context"
    context["council_id"] = "council-beta"
    resign(case)
    assert refusal(register, case) == "cross_convening_context"
    context["signing_context"] = fx.RETURN_CONTEXT
    resign(case)
    assert refusal(register, case) == "cross_protocol_context"


# =============================================================================
# Registration, E7 step 9: the proof.
# =============================================================================


def test_a_proof_by_another_key_is_proof_invalid():
    case = fx.registration_case()
    fx.sign_registration(case["registration"], fx.key("seat-a", 2))
    assert refusal(register, case) == "proof_invalid"


def test_a_proof_with_one_flipped_byte_is_proof_invalid():
    case = fx.registration_case()
    raw = bytearray(fx.b64url_decode(case["registration"]["proof"]))
    raw[0] ^= 0x01
    case["registration"]["proof"] = fx.b64url(bytes(raw))
    assert refusal(register, case) == "proof_invalid"


# =============================================================================
# Registration: the E7 order across its steps (multi-defect records).
# =============================================================================


def test_e7_step_3_before_step_4():
    case = fx.registration_case()
    case["registration"]["assignment_id"] = "assignment-nobody"
    case["registration"]["private_key"] = "A" * 43
    assert refusal(register, case) == "registration_malformed"


def test_e7_step_4_before_step_5():
    case = fx.registration_case()
    case["evaluation_time"] = "2026-10-09T06:00:00Z"
    case["environment"]["identity"]["principal"]["principal_ref"] = fx.binding_id("seat-b")
    assert refusal(register, case) == "assignment_expired"


def test_e7_step_5_before_step_6():
    case = fx.registration_case()
    case["environment"]["identity"]["claims"]["exp"] = fx.EVALUATION_EPOCH
    case["environment"]["issued"]["challenges"] = []
    assert refusal(register, case) == "claims_expired"


def test_e7_step_6_before_step_7():
    case = fx.registration_case()
    case["environment"]["issued"]["consumed_challenges"] = [fx.challenge_id("seat-a")]
    case["environment"]["issued"]["registered_keys"] = [
        dict(fx.registered_key("seat-a", case["signer"]), assignment_id=fx.assignment_id("seat-b"))]
    assert refusal(register, case) == "challenge_consumed"


def test_e7_step_7_before_step_8():
    case = fx.registration_case()
    case["environment"]["issued"]["registered_keys"] = [
        dict(fx.registered_key("seat-a", case["signer"]), assignment_id=fx.assignment_id("seat-b"))]
    case["registration"]["context"]["seat_id"] = "seat-b"
    resign(case)
    assert refusal(register, case) == "shared_key"


def test_e7_step_8_before_step_9():
    case = fx.registration_case()
    case["registration"]["context"]["convening_id"] = "convening-0002"
    fx.sign_registration(case["registration"], fx.key("seat-a", 2))
    assert refusal(register, case) == "cross_convening_context"


# =============================================================================
# Return: the accepted case, and E8 steps 1 and 2.
# =============================================================================


def test_a_well_formed_return_is_accepted_with_its_derived_values():
    case = fx.return_case()
    assert give_return(case) == {
        "key_fingerprint": fx.fingerprint(case["signer"].public_key),
        "signed_bytes": fx.b64url(fx.jcs(case["return"]["context"])),
    }


def test_return_verifies_the_signature_with_the_stdlib_verifier(monkeypatch):
    calls = []
    real = ed25519.verify
    monkeypatch.setattr(ed25519, "verify",
                        lambda *args: calls.append(args) or real(*args))
    case = fx.return_case()
    give_return(case)
    assert calls == [(case["signer"].public_key, fx.jcs(case["return"]["context"]),
                      fx.b64url_decode(case["return"]["signature"]))]


def test_a_legacy_return_under_the_replacement_is_refused():
    case = fx.return_case()
    case["return"]["protocol"] = fx.LEGACY
    assert refusal(give_return, case) == "legacy_protocol_refused"


@pytest.mark.parametrize("mutate", [
    pytest.param(lambda r: r.pop("signature"), id="signature-missing"),
    pytest.param(lambda r: r.update(public_key="A" * 42 + "E"), id="a-public-key-in-the-return"),
    pytest.param(lambda r: r["return_digest"].update(subject="council_convening"),
                 id="digest-subject-not-the-return-payload"),
    pytest.param(lambda r: r.update(payload=["not", "an", "object"]), id="payload-not-an-object"),
    pytest.param(lambda r: r["context"].update(challenge_id="challenge-seat-a"),
                 id="context-not-a-return-context"),
])
def test_a_return_that_fails_its_schema_is_return_malformed(mutate):
    case = fx.return_case()
    mutate(case["return"])
    assert refusal(give_return, case) == "return_malformed"


@pytest.mark.parametrize("name", ["private_key", "secret_key", "seed", "sk", "d"])
def test_key_transport_inside_the_open_payload_is_return_malformed(name):
    case = fx.return_case()
    case["return"]["payload"]["entry"]["findings"] = [{"note": "x", name: "A" * 43}]
    assert refusal(give_return, case) == "return_malformed"


def test_a_pem_private_key_block_inside_the_payload_is_return_malformed():
    case = fx.return_case()
    case["return"]["payload"]["entry"]["summary"] = "see " + fx.pem_private_key_block()
    assert refusal(give_return, case) == "return_malformed"


def test_a_pem_private_key_block_as_a_payload_member_name_is_return_malformed():
    # E8 step 2: "a PEM private-key block in any string", and a JSON member
    # name is a string. Unit-only, like the member-name cases (U10).
    case = fx.return_case()
    case["return"]["payload"]["entry"]["extra"] = {fx.pem_private_key_block(): "x"}
    assert refusal(give_return, case) == "return_malformed"


def test_a_pem_private_key_block_as_a_member_name_is_refused_without_echoing_it():
    block = fx.pem_private_key_block()
    with pytest.raises(Refused) as caught:
        signing.refuse_key_transport({"outer": [{"inner": {block: "x"}}]},
                                     "return_malformed")
    assert caught.value.code == "return_malformed"
    # The member named is the object that carries the name, never the name.
    assert caught.value.member == "outer[0].inner"
    assert block not in str(caught.value)
    assert "PRIVATE KEY" not in str(caught.value.member)


def test_a_float_in_the_payload_is_value_not_canonicalizable():
    case = fx.return_case()
    case["return"]["payload"]["entry"]["model_usage"]["costUSD"] = 0.0125
    assert refusal(give_return, case) == "value_not_canonicalizable"


@pytest.mark.parametrize("value", [2 ** 53, -(2 ** 53), "\ud800"])
def test_a_payload_value_outside_the_construction_is_value_not_canonicalizable(value):
    case = fx.return_case()
    case["return"]["payload"]["entry"]["probe"] = value
    assert refusal(give_return, case) == "value_not_canonicalizable"


def test_a_decimal_string_in_the_payload_is_accepted():
    case = fx.return_case()
    content = case["return"]["payload"]
    content["entry"]["model_usage"]["costUSD"] = "1234.5678"
    case["return"] = fx.seat_return(case["snapshot"], "seat-a", case["signer"], content)
    give_return(case)


def _sized_payload(size: int) -> dict:
    content = {"blob": ""}
    content["blob"] = "x" * (size - len(fx.jcs(content)))
    assert len(fx.jcs(content)) == size
    return content


def test_a_payload_of_exactly_one_mebibyte_of_canonical_bytes_is_accepted():
    case = fx.return_case()
    case["return"] = fx.seat_return(case["snapshot"], "seat-a", case["signer"],
                                    _sized_payload(fx.PAYLOAD_LIMIT))
    give_return(case)


def test_a_payload_above_one_mebibyte_of_canonical_bytes_is_return_malformed():
    case = fx.return_case()
    case["return"] = fx.seat_return(case["snapshot"], "seat-a", case["signer"],
                                    _sized_payload(fx.PAYLOAD_LIMIT + 1))
    assert refusal(give_return, case) == "return_malformed"


def test_the_shape_checks_run_in_their_order():
    case = fx.return_case()
    entry = case["return"]["payload"]["entry"]
    entry["blob"] = "x" * (fx.PAYLOAD_LIMIT + 1)
    entry["model_usage"]["costUSD"] = 0.5
    assert refusal(give_return, case) == "value_not_canonicalizable"   # before the size
    entry["model_usage"]["sk"] = "A" * 43
    assert refusal(give_return, case) == "return_malformed"            # key transport first


# =============================================================================
# Return, E8 steps 3 and 4: the assignment, then the registered key.
# =============================================================================


def test_a_return_for_an_assignment_not_in_the_snapshot_is_assignment_unknown():
    case = fx.return_case()
    case["return"]["assignment_id"] = "assignment-nobody"
    assert refusal(give_return, case) == "assignment_unknown"


def test_a_return_before_the_assignments_not_before_is_not_yet_valid():
    case = fx.return_case()
    case["evaluation_time"] = "2026-10-08T23:59:59Z"
    assert refusal(give_return, case) == "assignment_not_yet_valid"


@pytest.mark.parametrize("instant", ["2026-10-09T06:00:00Z", "2026-10-09T07:00:00Z"])
def test_a_return_at_or_after_the_assignments_expiry_is_assignment_expired(instant):
    case = fx.return_case()
    case["evaluation_time"] = instant
    assert refusal(give_return, case) == "assignment_expired"


def test_a_return_against_a_registration_only_assignment_is_not_permitted():
    case = fx.return_case()
    fx.frozen_assignment(case["snapshot"], "seat-a")["permitted_operations"] = [
        "seat_key_registration"]
    assert refusal(give_return, case) == "operation_not_permitted"


def test_a_return_with_no_registered_key_is_return_unregistered():
    case = fx.return_case()
    case["environment"]["issued"]["registered_keys"] = [
        fx.registered_key("seat-b", case["signers"]["seat-b"])]
    assert refusal(give_return, case) == "return_unregistered"


def test_a_return_under_another_key_is_return_key_mismatch():
    case = fx.return_case()
    other = fx.key("seat-a", 2)
    case["environment"]["issued"]["registered_keys"][0] = fx.registered_key("seat-a", other)
    assert refusal(give_return, case) == "return_key_mismatch"


def test_a_context_naming_another_key_is_return_key_mismatch():
    # N16: the context's `key_fingerprint` differs from the registered key.
    case = fx.return_case()
    case["return"]["context"]["key_fingerprint"] = "sha256:" + "ab" * 32
    fx.sign_return(case["return"], case["signer"])
    assert refusal(give_return, case) == "return_key_mismatch"


# =============================================================================
# Return, E8 step 5: the context, rebuilt and compared member by member.
# =============================================================================


@pytest.mark.parametrize("member, value, code", [
    pytest.param("signing_context", fx.REGISTRATION_CONTEXT, "cross_protocol_context",
                 id="the-registration-context-string"),
    pytest.param("signing_context", fx.LEGACY, "cross_protocol_context",
                 id="the-legacy-return-context-string"),
    pytest.param("protocol", fx.LEGACY, "cross_protocol_context", id="the-legacy-protocol"),
    pytest.param("convening_id", "convening-0002", "cross_convening_context", id="convening_id"),
    pytest.param("convening_digest", "sha256:" + "d" * 64, "cross_convening_context",
                 id="convening_digest"),
    pytest.param("council_id", "council-beta", "cross_convening_context", id="council_id"),
    pytest.param("candidate", dict(repository=fx.CANDIDATE_REPOSITORY, pull_number=7,
                                   head_sha="9" * 40), "cross_convening_context",
                 id="candidate"),
    pytest.param("assignment_id", fx.assignment_id("seat-b"), "cross_seat_context",
                 id="assignment_id"),
    pytest.param("seat_id", "seat-b", "cross_seat_context", id="seat_id"),
])
def test_a_return_context_member_that_differs_from_frozen_state_names_its_code(member, value, code):
    case = fx.return_case()
    case["return"]["context"][member] = value
    fx.sign_return(case["return"], case["signer"])
    assert refusal(give_return, case) == code


def test_a_return_replayed_into_another_assignment_is_refused_by_its_key():
    # Seat A's valid return presented for seat B: seat B's registered key is
    # not the key that signed it.
    case = fx.return_case()
    case["return"]["assignment_id"] = fx.assignment_id("seat-b")
    assert refusal(give_return, case) == "return_key_mismatch"


def test_a_replay_into_another_assignment_that_also_relabels_the_key_is_told_apart_by_the_context():
    case = fx.return_case()
    case["return"]["assignment_id"] = fx.assignment_id("seat-b")
    case["return"]["key_fingerprint"] = fx.fingerprint(case["signers"]["seat-b"].public_key)
    assert refusal(give_return, case) == "cross_seat_context"


def test_a_return_replayed_into_another_convening_is_cross_convening_context():
    case = fx.return_case()
    case["snapshot"] = fx.snapshot(convening_id="convening-0002")
    assert refusal(give_return, case) == "cross_convening_context"


def test_the_return_context_comparison_runs_in_its_order():
    case = fx.return_case()
    context = case["return"]["context"]
    context["key_fingerprint"] = "sha256:" + "ab" * 32
    context["seat_id"] = "seat-b"
    fx.sign_return(case["return"], case["signer"])
    assert refusal(give_return, case) == "cross_seat_context"        # before the key
    context["council_id"] = "council-beta"
    fx.sign_return(case["return"], case["signer"])
    assert refusal(give_return, case) == "cross_convening_context"
    context["protocol"] = fx.LEGACY
    fx.sign_return(case["return"], case["signer"])
    assert refusal(give_return, case) == "cross_protocol_context"


# =============================================================================
# Return, E8 steps 6 to 8: the digest, the signature, replay.
# =============================================================================


def test_a_payload_changed_after_signing_is_return_digest_mismatch():
    case = fx.return_case()
    case["return"]["payload"]["entry"]["summary"] = "a different entry"
    assert refusal(give_return, case) == "return_digest_mismatch"


def test_a_context_digest_that_differs_from_the_records_is_return_digest_mismatch():
    case = fx.return_case()
    case["return"]["context"]["return_digest"] = "sha256:" + "e" * 64
    fx.sign_return(case["return"], case["signer"])
    assert refusal(give_return, case) == "return_digest_mismatch"


def test_a_signature_by_another_key_is_return_signature_invalid():
    case = fx.return_case()
    fx.sign_return(case["return"], fx.key("seat-a", 2))
    assert refusal(give_return, case) == "return_signature_invalid"


def test_a_second_return_for_the_assignment_is_return_replayed():
    case = fx.return_case()
    case["environment"]["issued"]["accepted_returns"] = [
        {"assignment_id": fx.assignment_id("seat-a"),
         "return_digest": case["return"]["return_digest"]["value"]}]
    assert refusal(give_return, case) == "return_replayed"


def test_legacy_v1_signed_bytes_never_verify_as_replacement_bytes():
    case = fx.return_case()
    context = case["return"]["context"]
    legacy_signature = case["signer"].sign(fx.legacy_v1_signed_bytes(context))
    case["return"]["signature"] = fx.b64url(legacy_signature)
    assert refusal(give_return, case) == "return_signature_invalid"


def test_replacement_signed_bytes_never_verify_as_legacy_v1_bytes():
    case = fx.return_case()
    context = case["return"]["context"]
    replacement = signing.signed_bytes(context)
    legacy = fx.legacy_v1_signed_bytes(context)
    assert replacement[:1] == b"{" and legacy.startswith(fx.LEGACY.encode() + b"\n")
    assert replacement != legacy
    signature = fx.b64url_decode(case["return"]["signature"])
    assert ed25519.verify(case["signer"].public_key, replacement, signature)
    assert not ed25519.verify(case["signer"].public_key, legacy, signature)


# =============================================================================
# Return: the E8 order across its steps (multi-defect records).
# =============================================================================


def test_e8_step_2_before_step_3():
    case = fx.return_case()
    case["return"]["payload"]["entry"]["model_usage"]["costUSD"] = 0.5
    case["return"]["assignment_id"] = "assignment-nobody"
    assert refusal(give_return, case) == "value_not_canonicalizable"


def test_e8_step_3_before_step_4():
    case = fx.return_case()
    fx.frozen_assignment(case["snapshot"], "seat-a")["permitted_operations"] = [
        "seat_key_registration"]
    case["environment"]["issued"]["registered_keys"] = []
    assert refusal(give_return, case) == "operation_not_permitted"


def test_e8_step_4_before_step_5():
    case = fx.return_case()
    case["environment"]["issued"]["registered_keys"] = []
    case["return"]["context"]["seat_id"] = "seat-b"
    assert refusal(give_return, case) == "return_unregistered"


def test_e8_step_5_before_step_6():
    case = fx.return_case()
    case["return"]["context"]["convening_id"] = "convening-0002"
    case["return"]["payload"]["entry"]["summary"] = "changed"
    assert refusal(give_return, case) == "cross_convening_context"


def test_e8_step_6_before_step_7():
    case = fx.return_case()
    case["return"]["payload"]["entry"]["summary"] = "changed"
    fx.sign_return(case["return"], fx.key("seat-a", 2))
    assert refusal(give_return, case) == "return_digest_mismatch"


def test_e8_step_7_before_step_8():
    case = fx.return_case()
    fx.sign_return(case["return"], fx.key("seat-a", 2))
    case["environment"]["issued"]["accepted_returns"] = [
        {"assignment_id": fx.assignment_id("seat-a"),
         "return_digest": case["return"]["return_digest"]["value"]}]
    assert refusal(give_return, case) == "return_signature_invalid"


# =============================================================================
# Completion (E8): over the frozen identities, never a count.
# =============================================================================


def test_every_frozen_assignment_returned_completes():
    assert complete(fx.completion_case()) == {}


def test_completion_does_not_depend_on_the_order_returns_arrived_in():
    case = fx.completion_case()
    case["returns"].reverse()
    assert complete(case) == {}


def test_a_return_for_an_assignment_not_in_the_snapshot_is_return_unlisted():
    case = fx.completion_case()
    case["returns"][1]["assignment_id"] = "assignment-nobody"
    assert refusal(complete, case) == "return_unlisted"


def test_two_returns_for_one_assignment_are_return_duplicate_at_the_same_count():
    case = fx.completion_case()
    case["returns"][1] = copy.deepcopy(case["returns"][0])
    assert len(case["returns"]) == len(case["snapshot"]["assignments"])
    assert refusal(complete, case) == "return_duplicate"


def test_a_same_count_return_set_of_the_wrong_identities_is_completion_set_mismatch():
    case = fx.completion_case()
    first, second = case["returns"]
    first["context"]["seat_id"], second["context"]["seat_id"] = "seat-b", "seat-a"
    assert refusal(complete, case) == "completion_set_mismatch"


def test_a_frozen_assignment_with_no_return_is_return_missing():
    case = fx.completion_case()
    case["returns"].pop()
    assert refusal(complete, case) == "return_missing"


def test_no_returns_at_all_is_return_missing():
    case = fx.completion_case()
    case["returns"] = []
    assert refusal(complete, case) == "return_missing"


def test_the_completion_checks_run_in_their_order():
    case = fx.completion_case()
    first, second = case["returns"]
    first["context"]["seat_id"] = "seat-b"
    case["returns"] = [first]
    assert refusal(complete, case) == "completion_set_mismatch"   # before missing
    case["returns"] = [first, copy.deepcopy(first)]
    assert refusal(complete, case) == "return_duplicate"          # before the set mismatch
    third = copy.deepcopy(second)
    third["assignment_id"] = "assignment-nobody"
    case["returns"] = [first, copy.deepcopy(first), third]
    assert refusal(complete, case) == "return_unlisted"           # before the duplicate


def test_completion_follows_the_snapshot_after_the_rule_changed():
    # US2 scenario 4: a rule changed after freezing changes nothing for work
    # already convened. A projection that would now seat only one seat, or a
    # third, is not read by completion at all.
    case = fx.completion_case()
    changed = {f"{fx.GOVERNED_REPOSITORY}@{fx.SHA_SEAT}": {
        "councils": {"council-alpha": {"standing_seats": ["seat-a", "seat-c"], "conditions": []}},
        "sources": ["rules/council-alpha.yaml"]}}
    assert complete(case, environment={"rules": changed}) == {}


# =============================================================================
# The oracles the orders read (pre-review of 03cb77e29, L1, L3 and L4). An
# oracle a step reads and the environment does not carry, an entry of another
# shape, or an id the oracle repeats is a harness error, never a refusal: a
# vector author's omission must not pass for a plausible code. An oracle the
# order never reaches is not required.
# =============================================================================


@pytest.mark.parametrize("oracle", ["identity", "governed_history", "issued"])
def test_an_absent_oracle_the_registration_order_reads_is_a_harness_error(oracle):
    case = fx.registration_case()
    del case["environment"][oracle]
    with pytest.raises(signing.InconsistentEnvironment):
        register(case)


@pytest.mark.parametrize("member", ["challenges", "consumed_challenges", "registered_keys"])
def test_an_absent_issued_list_the_registration_order_reads_is_a_harness_error(member):
    case = fx.registration_case()
    del case["environment"]["issued"][member]
    with pytest.raises(signing.InconsistentEnvironment):
        register(case)


def test_an_identity_without_its_principal_is_a_harness_error():
    case = fx.registration_case()
    del case["environment"]["identity"]["principal"]
    with pytest.raises(signing.InconsistentEnvironment):
        register(case)


def test_an_oracle_the_order_never_reaches_is_not_required():
    case = fx.registration_case()
    del case["registration"]["protocol"]
    case["registration"]["root_signature"] = "A" * 85 + "Q"
    for oracle in ("identity", "governed_history", "issued"):
        del case["environment"][oracle]
    assert refusal(register, case) == "legacy_protocol_refused"


@pytest.mark.parametrize("member", ["issued", "registered_keys", "accepted_returns"])
def test_an_absent_oracle_the_return_order_reads_is_a_harness_error(member):
    case = fx.return_case()
    if member == "issued":
        del case["environment"]["issued"]
    else:
        del case["environment"]["issued"][member]
    with pytest.raises(signing.InconsistentEnvironment):
        give_return(case)


@pytest.mark.parametrize("member,entry", [
    pytest.param("consumed_challenges", {"challenge_id": "challenge-seat-a"},
                 id="consumed-challenge-as-an-object"),
    pytest.param("challenges", "challenge-seat-a", id="challenge-as-a-string"),
    pytest.param("registered_keys", {"assignment_id": "assignment-seat-b",
                                     "key_fingerprint": "sha256:" + "ab" * 32},
                 id="registered-key-without-its-public-key"),
])
def test_an_issued_entry_of_another_shape_is_a_harness_error_at_registration(member, entry):
    case = fx.registration_case()
    case["environment"]["issued"][member] = [
        *case["environment"]["issued"][member], entry]
    with pytest.raises(signing.InconsistentEnvironment):
        register(case)


@pytest.mark.parametrize("member,entry", [
    pytest.param("accepted_returns", "assignment-seat-b", id="accepted-return-as-a-string"),
    pytest.param("registered_keys", {"assignment_id": "assignment-seat-b",
                                     "key_fingerprint": "sha256:" + "ab" * 32,
                                     "public_key": "A" * 43, "seat_id": "seat-b"},
                 id="registered-key-with-another-member"),
])
def test_an_issued_entry_of_another_shape_is_a_harness_error_at_return(member, entry):
    case = fx.return_case()
    case["environment"]["issued"][member] = [*case["environment"]["issued"][member], entry]
    with pytest.raises(signing.InconsistentEnvironment):
        give_return(case)


def test_a_repeated_binding_id_is_a_harness_error():
    case = fx.registration_case()
    case["bindings"] = [*case["bindings"], copy.deepcopy(case["bindings"][0])]
    with pytest.raises(signing.InconsistentEnvironment):
        register(case)


def test_a_repeated_challenge_id_is_a_harness_error():
    # The probe: with two issued challenges sharing an id, the list's order
    # decided the outcome (`challenge_malformed` or accept).
    case = fx.registration_case()
    bad = dict(issued_challenge(case), expires_at="2026-10-09T01:05:01Z")
    case["environment"]["issued"]["challenges"] = [issued_challenge(case), bad]
    with pytest.raises(signing.InconsistentEnvironment):
        register(case)


def test_a_repeated_registered_assignment_is_a_harness_error():
    case = fx.return_case()
    keys = case["environment"]["issued"]["registered_keys"]
    case["environment"]["issued"]["registered_keys"] = [*keys, copy.deepcopy(keys[0])]
    with pytest.raises(signing.InconsistentEnvironment):
        give_return(case)


def test_a_malformed_frozen_instant_is_a_harness_error():
    case = fx.registration_case()
    fx.frozen_assignment(case["snapshot"], "seat-a")["not_before"] = "not-an-instant"
    with pytest.raises(signing.InconsistentEnvironment):
        register(case)
