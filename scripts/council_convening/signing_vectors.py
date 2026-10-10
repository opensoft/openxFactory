"""The `signing` area's vectors, BUILT by the corpus generator (T044).

Feature 035 Phase 4. Every vector here is written by `generate` from the case
list below: the record under test, the frozen state and the oracles are
assembled, and every key, proof and signature is made with a LABELLED fixture
key (research R18). Ed25519 is deterministic, so `generate --check` reproduces
every signature byte for byte.

EXPECTED OUTCOMES ARE AUTHORED, NOT COMPUTED. Each case names its outcome and
its one refusal code, in the normative order of data-model E7 and E8, before
any implementation ran; the reference implementation (`signing`) is then held
to them by the self-test. The only values the builder derives are the known
answers of an accepted case (`signed_bytes` and `key_fingerprint`), and it
derives them with `canonical.serialize` and `hashlib`, never with `signing`.

TWO KNOWN ANSWERS ARE WRITTEN BY HAND (N9): one registration context and one
return context. Their canonical bytes are spelled out in this file as literals,
member by member, and carry `derived_origin: hand`, so the generator and the
reference implementation are never checked only against each other.

WHO RUNS WHICH VECTOR.

* `registration` vectors are `applies_to: [consumer]`. Every one of them carries
  the holder's binding and the seat job's verified claims, because E7 step 5
  runs before the challenge, key, context and proof steps. That is the rule
  analysis R4-M2 set for admission vectors that carry a binding: a shared one
  would force the producer to implement the consumer's OIDC checks. The four
  challenge-ceiling vectors are consumer-only on their own ground too (N23):
  the consumer issues challenges.
* `return` and `completion` vectors are `applies_to: [producer, consumer]`: both
  sides hold seat returns to the same order and the same names (data-model §
  Refusal vocabulary).

WHAT THE CORPUS CANNOT CARRY, AND WHERE IT IS PROVEN INSTEAD.

* Key transport BY MEMBER NAME: no corpus member at any depth may be named
  `seed`, `private_key`, `secret_key`, `sk` or `d` (U10), so a record carrying
  one cannot be a vector. The corpus probes key transport with a PEM
  private-key block, joined from `$parts`; the member-name cases are
  `tests/council_convening/test_signing.py`'s.
* A payload above 1 MiB: a vector would commit a megabyte to prove a length
  check. The bound is proven in `test_signing.py`.

THE PER-SEAT BINDINGS. Brett Heap's 025 ruling (A) of 2026-10-09, "Per-seat
environments (Recommended)": one binding per seat, told apart by the seat's
environment in the OIDC `sub`, with the holder's `principal_ref` equal to the
binding id. Every registration vector uses that shape.
"""

from __future__ import annotations

import base64
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from ..signed_execution_chain import canonical
from . import records

AREA = "signing"
KEY_LABEL_PREFIX = "council-convening/corpus/"

REPLACEMENT = "xfc-resolved-council-1"
LEGACY = "xfactory-council-seat-return/v1"
REGISTRATION_CONTEXT = "xfc-resolved-council-1/seat-key-registration"
RETURN_CONTEXT = "xfc-resolved-council-1/seat-return"
LEGACY_KEY_AUTHORIZATION_CONTEXT = "xfactory-council-seat-key-authorization/v1"

SHA_HEAD = "1" * 40
SHA_REVISION = "2" * 40
SHA_SEAT = "4" * 40
SHA_BEFORE = "5" * 40
SHA_OFF = "6" * 40
SHA_FILE = "sha256:" + "3" * 64

CANDIDATE_REPOSITORY = "example-owner/example-candidate"
GOVERNED_REPOSITORY = "example-owner/example-rules"
CALLER_REPOSITORY = "example-owner/example-caller"
CALLER_REPOSITORY_ID = 4242
ISSUER = "https://token.actions.githubusercontent.com"
AUDIENCE = "example-consumer"
SEAT_WORKFLOW = f"{GOVERNED_REPOSITORY}/.github/workflows/council-seat.yml@refs/heads/main"

CONVENING_ID = "convening-0001"
SEATS = ("seat-a", "seat-b")

EVALUATION_TIME = "2026-10-09T01:00:00Z"
EVALUATION_EPOCH = 1791507600
ISSUED_AT = "2026-10-09T00:55:00Z"
EXPIRES_AT = "2026-10-09T01:05:00Z"

REG_FRS = ["FR-007", "FR-008", "FR-010", "SC-003"]
RET_FRS = ["FR-008", "FR-010", "SC-003"]
CMP_FRS = ["FR-005", "FR-010", "SC-003"]
CONSUMER = ["consumer"]
BOTH = ["producer", "consumer"]


# --------------------------------------------------------------------------
# Keys, encodings and fingerprints, derived independently of `signing`.
# --------------------------------------------------------------------------

#: The fixture keys the signing area signs with: each seat's own key, and a
#: second key for seat A that plays the wrong key in the refusal cases.
KEY_NAMES = ("seat-a/1", "seat-b/1", "seat-a/2")


def _key(name: str):
    from . import generate

    if name not in KEY_NAMES:
        raise ValueError(f"{name!r} is not one of the signing area's fixture keys")
    return generate.test_key(KEY_LABEL_PREFIX + name)


def key_labels() -> list[str]:
    """Every fixture-key label the signing area signs with."""
    return [KEY_LABEL_PREFIX + name for name in KEY_NAMES]


def b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def fingerprint(public_key: bytes) -> str:
    """The estate spelling, Brett Heap's ruling of 2026-10-09, "Estate spelling
    (Recommended)": `sha256:` and the hex SHA-256 of the raw key."""
    return "sha256:" + hashlib.sha256(public_key).hexdigest()


def jcs(value: Any) -> bytes:
    return canonical.serialize(value).encode("utf-8")


def nonce(label: str) -> str:
    return b64url(hashlib.sha256(f"council-convening corpus nonce {label}".encode()).digest())


# --------------------------------------------------------------------------
# The frozen world.
# --------------------------------------------------------------------------

def binding_id(seat: str) -> str:
    return f"binding-{seat}"


def assignment_id(seat: str) -> str:
    return f"assignment-{seat}"


def environment_name(seat: str) -> str:
    return f"council-{seat}"


def convening_record() -> dict:
    return {
        "schema_version": 1, "kind": "xfactory_council_convening", "protocol": REPLACEMENT,
        "council_id": "council-alpha", "subject_pin": SHA_HEAD,
        "packet_refs": ["packet/alpha-1"], "required_seats": list(SEATS),
        "required_seats_provenance": {
            "candidate": {"repository": CANDIDATE_REPOSITORY, "pull_number": 7,
                          "head_sha": SHA_HEAD},
            "governed": {"repository": GOVERNED_REPOSITORY, "revision": SHA_REVISION,
                         "sources": [{"kind": "file", "path": "rules/council-alpha.yaml",
                                      "sha256": SHA_FILE}]},
            "standing_seats": list(SEATS), "conditions": [], "fact_sources": [],
            "consumed_facts": {},
        },
    }


def _digest(value: Any, subject: str) -> dict:
    return {"construction": "xfc-jcs-sha256-1", "subject": subject,
            "value": canonical.digest(value)}


def assignment(convening: dict, seat: str, convening_id: str = CONVENING_ID) -> dict:
    return {
        "schema_version": 1, "kind": "xfactory_council_seat_assignment", "protocol": REPLACEMENT,
        "convening_id": convening_id, "convening_digest": _digest(convening, "council_convening"),
        "council_id": convening["council_id"],
        "candidate": copy.deepcopy(convening["required_seats_provenance"]["candidate"]),
        "assignment_id": assignment_id(seat), "seat_id": seat,
        "holder": {"principal_kind": "github_oidc_job", "principal_ref": binding_id(seat),
                   "binding_ref": binding_id(seat)},
        "permitted_operations": ["seat_key_registration", "seat_return"],
        "not_before": "2026-10-09T00:00:00Z", "expires_at": "2026-10-09T06:00:00Z",
    }


def snapshot(convening_id: str = CONVENING_ID) -> dict:
    convening = convening_record()
    return {
        "schema_version": 1, "kind": "xfactory_council_convening_snapshot", "protocol": REPLACEMENT,
        "convening_id": convening_id, "convening_digest": _digest(convening, "council_convening"),
        "convening": convening,
        "assignments": [assignment(convening, seat, convening_id) for seat in SEATS],
        "admitted_at": "2026-10-09T00:00:00Z",
    }


def frozen(snap: dict, seat: str) -> dict:
    return next(a for a in snap["assignments"] if a["seat_id"] == seat)


def binding(seat: str) -> dict:
    return {
        "schema_version": 1, "kind": "xfactory_council_producer_binding", "protocol": REPLACEMENT,
        "binding_id": binding_id(seat), "principal_kind": "github_oidc_job", "issuer": ISSUER,
        "audience": AUDIENCE, "caller_repository": CALLER_REPOSITORY,
        "repository_id": CALLER_REPOSITORY_ID, "subject_claim_keys": ["repo", "context"],
        "subject_template": f"repo:{CALLER_REPOSITORY}:environment:{environment_name(seat)}",
        "permitted_workflows": [{"operation": "seat_execution", "job_workflow_ref": SEAT_WORKFLOW,
                                 "workflow_revision_rule": "on_governed_history_since_revision"}],
        "broker": {"broker_ref": "broker-example", "capability_verified": False,
                   "evidence_ref": None},
    }


def identity(seat: str) -> dict:
    return {
        "verified": True,
        "claims": {
            "iss": ISSUER, "aud": AUDIENCE,
            "sub": f"repo:{CALLER_REPOSITORY}:environment:{environment_name(seat)}",
            # The token outlives the challenge (01:10:00 against 01:05:00), so E7
            # step 5's window check never masks a step 6 challenge expiry.
            "nbf": EVALUATION_EPOCH - 60, "exp": EVALUATION_EPOCH + 600,
            "repository": CALLER_REPOSITORY, "repository_id": str(CALLER_REPOSITORY_ID),
            "environment": environment_name(seat),
            "job_workflow_ref": SEAT_WORKFLOW, "job_workflow_sha": SHA_SEAT,
        },
        "principal": {"principal_kind": "github_oidc_job", "principal_ref": binding_id(seat)},
    }


def governed_history() -> dict:
    return {
        f"{GOVERNED_REPOSITORY}@{SHA_SEAT}": {"on_first_parent": True,
                                              "at_or_after": [SHA_REVISION]},
        f"{GOVERNED_REPOSITORY}@{SHA_REVISION}": {"on_first_parent": True,
                                                  "at_or_after": [SHA_REVISION]},
        f"{GOVERNED_REPOSITORY}@{SHA_BEFORE}": {"on_first_parent": True, "at_or_after": []},
        f"{GOVERNED_REPOSITORY}@{SHA_OFF}": {"on_first_parent": False, "at_or_after": []},
    }


def repository_identity(root: Path) -> dict:
    """The frozen identity fixture's text, never the live map (R8; R7-M1)."""
    path = root / records.FAMILY_REL / "conformance" / "fixtures" / "repository-identity.json"
    fixture = json.loads(path.read_text(encoding="utf-8"))
    return {"state": "text", "text": fixture["text"]}


def challenge(seat: str, public_key: bytes) -> dict:
    return {
        "schema_version": 1, "kind": "xfactory_council_registration_challenge",
        "protocol": REPLACEMENT, "challenge_id": f"challenge-{seat}",
        "assignment_id": assignment_id(seat), "key_fingerprint": fingerprint(public_key),
        "nonce": nonce(seat), "issued_at": ISSUED_AT, "expires_at": EXPIRES_AT,
    }


def _common(signing_context: str, fixed: dict, key_fingerprint: str) -> dict:
    return {
        "signing_context": signing_context, "protocol": fixed["protocol"],
        "convening_id": fixed["convening_id"], "convening_digest": fixed["convening_digest"]["value"],
        "council_id": fixed["council_id"], "candidate": copy.deepcopy(fixed["candidate"]),
        "assignment_id": fixed["assignment_id"], "seat_id": fixed["seat_id"],
        "key_fingerprint": key_fingerprint,
    }


def payload(seat: str) -> dict:
    return {"seat": seat,
            "entry": {"summary": f"{seat} reviewed the candidate", "findings": [],
                      "model_usage": {"costUSD": "0.0125", "turns": 3}}}


# --------------------------------------------------------------------------
# The worlds each case mutates.
# --------------------------------------------------------------------------

class RegistrationWorld:
    """One seat's registration and everything the registration boundary reads."""

    def __init__(self, root: Path, seat: str = "seat-a"):
        self.seat = seat
        self.signer = _key(f"{seat}/1")
        self.snapshot = snapshot()
        self.bindings = [binding(s) for s in SEATS]
        self.challenge = challenge(seat, self.signer.public_key)
        fixed = frozen(self.snapshot, seat)
        context = _common(REGISTRATION_CONTEXT, fixed, fingerprint(self.signer.public_key))
        context["challenge_id"] = self.challenge["challenge_id"]
        context["challenge_nonce"] = self.challenge["nonce"]
        self.registration = {
            "schema_version": 1, "kind": "xfactory_council_seat_key_registration",
            "protocol": REPLACEMENT, "assignment_id": fixed["assignment_id"],
            "challenge_id": self.challenge["challenge_id"],
            "public_key": b64url(self.signer.public_key),
            "key_fingerprint": fingerprint(self.signer.public_key), "context": context,
        }
        self.resign()
        self.issued = {"challenges": [self.challenge], "consumed_challenges": [],
                       "registered_keys": []}
        self.identity = identity(seat)
        self.repository_identity = repository_identity(root)
        self.governed_history = governed_history()
        self.registry_status: dict | None = None
        self.selected_protocol: str | None = REPLACEMENT
        self.evaluation_time = EVALUATION_TIME

    def resign(self, signer=None) -> None:
        signer = signer or self.signer
        self.registration["proof"] = b64url(signer.sign(jcs(self.registration["context"])))

    def registered_key(self, seat: str, signer, assignment: str | None = None) -> dict:
        return {"assignment_id": assignment or assignment_id(seat),
                "key_fingerprint": fingerprint(signer.public_key),
                "public_key": b64url(signer.public_key)}

    def vector_parts(self) -> tuple[dict, dict]:
        inputs = {"registration": self.registration, "snapshot": self.snapshot,
                  "bindings": self.bindings, "selected_protocol": self.selected_protocol}
        environment = {"issued": self.issued, "identity": self.identity,
                       "repository_identity": self.repository_identity,
                       "governed_history": self.governed_history}
        if self.registry_status is not None:
            environment["registry_status"] = self.registry_status
        return inputs, environment

    def derived(self) -> dict:
        return {"key_fingerprint": self.registration["key_fingerprint"],
                "signed_bytes": b64url(jcs(self.registration["context"]))}


class ReturnWorld:
    """One seat's return and everything the return boundary reads."""

    def __init__(self, root: Path, seat: str = "seat-a"):
        del root
        self.seat = seat
        self.signers = {s: _key(f"{s}/1") for s in SEATS}
        self.signer = self.signers[seat]
        self.snapshot = snapshot()
        self.issued = {"registered_keys": [self.registered_key(s, self.signers[s]) for s in SEATS],
                       "accepted_returns": []}
        self.registry_status: dict | None = None
        self.selected_protocol: str | None = REPLACEMENT
        self.evaluation_time = EVALUATION_TIME
        self.seat_return = self.make_return(seat, self.signer, payload(seat))

    def registered_key(self, seat: str, signer) -> dict:
        return {"assignment_id": assignment_id(seat), "key_fingerprint": fingerprint(signer.public_key),
                "public_key": b64url(signer.public_key)}

    def make_return(self, seat: str, signer, content: dict, snap: dict | None = None) -> dict:
        fixed = frozen(snap or self.snapshot, seat)
        digest = _digest(content, "council_seat_return_payload")
        context = _common(RETURN_CONTEXT, fixed, fingerprint(signer.public_key))
        context["return_digest"] = digest["value"]
        value = {"schema_version": 1, "kind": "xfactory_council_seat_return",
                 "protocol": REPLACEMENT, "assignment_id": fixed["assignment_id"],
                 "key_fingerprint": fingerprint(signer.public_key), "payload": content,
                 "return_digest": digest, "context": context}
        value["signature"] = b64url(signer.sign(jcs(context)))
        return value

    def resign(self, signer=None) -> None:
        signer = signer or self.signer
        self.seat_return["signature"] = b64url(signer.sign(jcs(self.seat_return["context"])))

    def vector_parts(self) -> tuple[dict, dict]:
        inputs = {"return": self.seat_return, "snapshot": self.snapshot,
                  "selected_protocol": self.selected_protocol}
        environment = {"issued": self.issued}
        if self.registry_status is not None:
            environment["registry_status"] = self.registry_status
        return inputs, environment

    def derived(self) -> dict:
        return {"key_fingerprint": self.seat_return["key_fingerprint"],
                "signed_bytes": b64url(jcs(self.seat_return["context"]))}


class CompletionWorld:
    def __init__(self, root: Path):
        del root
        self.signers = {s: _key(f"{s}/1") for s in SEATS}
        self.snapshot = snapshot()
        maker = ReturnWorld.__new__(ReturnWorld)
        maker.snapshot = self.snapshot
        self.returns = [ReturnWorld.make_return(maker, s, self.signers[s], payload(s))
                        for s in SEATS]
        self.environment: dict | None = None
        self.evaluation_time = EVALUATION_TIME

    def vector_parts(self) -> tuple[dict, dict | None]:
        return {"snapshot": self.snapshot, "returns": self.returns}, self.environment


# --------------------------------------------------------------------------
# The two hand-authored known answers (N9).
#
# Each is the default seat-a context of its world, its canonical bytes spelled
# out BY HAND below, member by member in RFC 8785 order (UTF-16 code-unit order
# of the names, no whitespace). The 64-hex values inside them are the digests
# and fingerprint the world fixes, copied in once; the byte layout around them
# is hand-written, never produced by `canonical.serialize`.
# --------------------------------------------------------------------------

HAND_SEAT_A_FINGERPRINT = "sha256:024fe835c9ba38e0e9716d9d2a2a04db2dde00fbb3921a05bf4dfd9d093bb5e3"

HAND_REGISTRATION_BYTES = (
    b'{"assignment_id":"assignment-seat-a",'
    b'"candidate":{"head_sha":"1111111111111111111111111111111111111111",'
    b'"pull_number":7,"repository":"example-owner/example-candidate"},'
    b'"challenge_id":"challenge-seat-a",'
    b'"challenge_nonce":"dHhqtWI2bV8ZOxkX824rVU3YxFeLQ1CeriBAzPcPd0k",'
    b'"convening_digest":"sha256:d1f42938970ad468215fa0069ac1b578f2277d4e923beedeab112a00cc4289af",'
    b'"convening_id":"convening-0001",'
    b'"council_id":"council-alpha",'
    b'"key_fingerprint":"sha256:024fe835c9ba38e0e9716d9d2a2a04db2dde00fbb3921a05bf4dfd9d093bb5e3",'
    b'"protocol":"xfc-resolved-council-1",'
    b'"seat_id":"seat-a",'
    b'"signing_context":"xfc-resolved-council-1/seat-key-registration"}')

HAND_RETURN_BYTES = (
    b'{"assignment_id":"assignment-seat-a",'
    b'"candidate":{"head_sha":"1111111111111111111111111111111111111111",'
    b'"pull_number":7,"repository":"example-owner/example-candidate"},'
    b'"convening_digest":"sha256:d1f42938970ad468215fa0069ac1b578f2277d4e923beedeab112a00cc4289af",'
    b'"convening_id":"convening-0001",'
    b'"council_id":"council-alpha",'
    b'"key_fingerprint":"sha256:024fe835c9ba38e0e9716d9d2a2a04db2dde00fbb3921a05bf4dfd9d093bb5e3",'
    b'"protocol":"xfc-resolved-council-1",'
    b'"return_digest":"sha256:0e21b903ad3ee13dfd86ebcc55b91ce2d7c22fc85e0b3b44d6dfbd4438353fa7",'
    b'"seat_id":"seat-a",'
    b'"signing_context":"xfc-resolved-council-1/seat-return"}')


# --------------------------------------------------------------------------
# The cases. Each names its outcome first; the mutation makes the record.
# --------------------------------------------------------------------------

def _p(*parts: str) -> dict:
    return {"$parts": list(parts)}


def _pem() -> dict:
    return _p("-----BEGIN ", "PRIVATE", " KEY-----")


def _registration_cases() -> list[tuple]:
    """`(case_id, mutate, outcome, refusal, applies_to, derived_origin)`."""
    def legacy_root(w):
        del w.registration["protocol"]
        w.registration["root_signature"] = "A" * 85 + "Q"

    def legacy_selection(w):
        w.selected_protocol = LEGACY
        w.registry_status = {LEGACY: "in_use"}

    def legacy_routed(w):
        legacy_root(w)
        legacy_selection(w)

    def root_member(w):
        w.registration["root_key_fingerprint"] = "sha256:" + "ab" * 32

    def root_before_shape(w):
        w.registration["root_signature"] = "A" * 85 + "Q"
        del w.registration["proof"]

    def no_proof(w):
        del w.registration["proof"]

    def pem(w):
        w.registration["context"]["signing_context"] = _pem()

    def malformed_before_assignment(w):
        w.registration["assignment_id"] = "assignment-nobody"
        w.registration["public_key"] = "A" * 42 + "B"

    def unknown_assignment(w):
        w.registration["assignment_id"] = "assignment-nobody"

    def at(instant):
        def mutate(w):
            w.evaluation_time = instant
        return mutate

    def return_only(w):
        frozen(w.snapshot, "seat-a")["permitted_operations"] = ["seat_return"]

    def expired_and_wrong_principal(w):
        w.evaluation_time = "2026-10-09T06:00:00Z"
        w.identity["principal"]["principal_ref"] = binding_id("seat-b")

    def unresolved(w):
        frozen(w.snapshot, "seat-a")["holder"]["binding_ref"] = "binding-nobody"

    def broker(w):
        frozen(w.snapshot, "seat-a")["holder"]["principal_kind"] = "governed_broker_job"

    def wrong_principal(w):
        w.identity["principal"]["principal_ref"] = binding_id("seat-b")

    def no_challenge(w):
        w.issued["challenges"] = []

    def lifetime(expires_at):
        def mutate(w):
            w.challenge["expires_at"] = expires_at
        return mutate

    def wrong_assignment(w):
        w.challenge["assignment_id"] = assignment_id("seat-b")

    def consumed(w):
        w.issued["consumed_challenges"] = ["challenge-seat-a"]

    def consumed_and_shared(w):
        consumed(w)
        shared(w)

    def fingerprint_wrong(w):
        w.registration["key_fingerprint"] = "sha256:" + "ab" * 32

    def challenge_for_other_key(w):
        w.challenge["key_fingerprint"] = fingerprint(_key("seat-a/2").public_key)

    def already(w):
        w.issued["registered_keys"] = [w.registered_key("seat-a", _key("seat-a/2"))]

    def shared(w):
        w.issued["registered_keys"] = [
            w.registered_key("seat-a", w.signer, assignment=assignment_id("seat-b"))]

    def shared_and_cross_seat(w):
        shared(w)
        context(w, "seat_id", "seat-b")

    def context(w, member, value):
        w.registration["context"][member] = value
        w.resign()

    def ctx(member, value):
        return lambda w: context(w, member, value)

    def cross_convening_bad_proof(w):
        w.registration["context"]["convening_id"] = "convening-0002"
        w.resign(_key("seat-a/2"))

    def bad_proof(w):
        w.resign(_key("seat-a/2"))

    def claims_expired_and_no_challenge(w):
        w.identity["claims"]["exp"] = EVALUATION_EPOCH
        w.issued["challenges"] = []

    def nothing(w):
        pass

    def frozen_revision(w):
        w.identity["claims"]["job_workflow_sha"] = SHA_REVISION

    # E7 step 5's E10 half (Phase 5's binding module, operation seat_execution).
    def stub(w):
        w.bindings[0]["instantiation_stub"] = True

    def unverified(w):
        w.identity["verified"] = False

    def expired_token(w):
        w.identity["claims"]["exp"] = EVALUATION_EPOCH

    def other_audience(w):
        w.identity["claims"]["aud"] = "another-consumer"

    def other_seats_job(w):
        w.identity = identity("seat-b")

    def seat_commit(sha):
        def mutate(w):
            w.identity["claims"]["job_workflow_sha"] = sha
        return mutate

    return [
        # accepts
        ("reg-accept-hand-known-answer", nothing, "accept", None, CONSUMER, "hand"),
        ("reg-accept-seat-job-at-frozen-revision", frozen_revision, "accept", None, CONSUMER,
         "generated"),
        ("reg-challenge-ceiling-600-seconds-accept", lifetime("2026-10-09T01:05:00Z"), "accept",
         None, CONSUMER, "generated"),
        # step 1, classification
        ("reg-legacy-root-authorized-under-replacement-refuse", legacy_root, "refuse",
         "legacy_protocol_refused", CONSUMER, "generated"),
        ("reg-replacement-under-legacy-selection-refuse", legacy_selection, "refuse",
         "protocol_not_selected", CONSUMER, "generated"),
        ("reg-legacy-under-legacy-selection-route", legacy_routed, "route", None, CONSUMER,
         "generated"),
        # step 2, root authorization
        ("reg-root-authorization-refuse", root_member, "refuse", "root_authorization_refused",
         CONSUMER, "generated"),
        ("reg-root-authorization-before-shape-refuse", root_before_shape, "refuse",
         "root_authorization_refused", CONSUMER, "generated"),
        # step 3, shape and key transport
        ("reg-proof-missing-refuse", no_proof, "refuse", "registration_malformed", CONSUMER,
         "generated"),
        ("reg-key-transport-pem-block-refuse", pem, "refuse", "registration_malformed",
         CONSUMER, "generated"),
        ("reg-shape-before-assignment-refuse", malformed_before_assignment, "refuse",
         "registration_malformed", CONSUMER, "generated"),
        # step 4, the assignment
        ("reg-assignment-unknown-refuse", unknown_assignment, "refuse", "assignment_unknown",
         CONSUMER, "generated"),
        ("reg-assignment-not-yet-valid-refuse", at("2026-10-08T23:59:59Z"), "refuse",
         "assignment_not_yet_valid", CONSUMER, "generated"),
        ("reg-assignment-expired-at-the-instant-refuse", at("2026-10-09T06:00:00Z"), "refuse",
         "assignment_expired", CONSUMER, "generated"),
        ("reg-operation-not-permitted-refuse", return_only, "refuse", "operation_not_permitted",
         CONSUMER, "generated"),
        ("reg-assignment-before-principal-refuse", expired_and_wrong_principal, "refuse",
         "assignment_expired", CONSUMER, "generated"),
        # step 5, the principal against the holder's binding
        ("reg-binding-unresolved-refuse", unresolved, "refuse", "binding_unresolved", CONSUMER,
         "generated"),
        ("reg-broker-job-holder-refuse", broker, "refuse", "broker_capability_insufficient",
         CONSUMER, "generated"),
        ("reg-stub-binding-refuse", stub, "refuse", "binding_malformed", CONSUMER,
         "generated"),
        ("reg-claims-unverified-refuse", unverified, "refuse", "claims_unverified", CONSUMER,
         "generated"),
        ("reg-claims-expired-refuse", expired_token, "refuse", "claims_expired", CONSUMER,
         "generated"),
        ("reg-audience-mismatch-refuse", other_audience, "refuse", "audience_mismatch",
         CONSUMER, "generated"),
        ("reg-another-seats-job-refuse", other_seats_job, "refuse",
         "subject_template_mismatch", CONSUMER, "generated"),
        # follow-up 3, "At or after the frozen rev (Recommended)": the seat rule
        ("reg-seat-workflow-before-frozen-revision-refuse", seat_commit(SHA_BEFORE), "refuse",
         "workflow_revision_ungoverned", CONSUMER, "generated"),
        ("reg-seat-workflow-off-governed-history-refuse", seat_commit(SHA_OFF), "refuse",
         "workflow_revision_ungoverned", CONSUMER, "generated"),
        ("reg-principal-before-challenge-refuse", claims_expired_and_no_challenge, "refuse",
         "claims_expired", CONSUMER, "generated"),
        ("reg-wrong-principal-with-valid-proof-refuse", wrong_principal, "refuse",
         "wrong_principal", CONSUMER, "generated"),
        # step 6, the challenge
        ("reg-challenge-unknown-refuse", no_challenge, "refuse", "challenge_unknown", CONSUMER,
         "generated"),
        ("reg-challenge-ceiling-601-seconds-refuse", lifetime("2026-10-09T01:05:01Z"), "refuse",
         "challenge_malformed", CONSUMER, "generated"),
        ("reg-challenge-ceiling-zero-seconds-refuse", lifetime(ISSUED_AT), "refuse",
         "challenge_malformed", CONSUMER, "generated"),
        ("reg-challenge-ceiling-negative-refuse", lifetime("2026-10-09T00:54:59Z"), "refuse",
         "challenge_malformed", CONSUMER, "generated"),
        ("reg-challenge-wrong-assignment-refuse", wrong_assignment, "refuse",
         "challenge_wrong_assignment", CONSUMER, "generated"),
        ("reg-challenge-consumed-refuse", consumed, "refuse", "challenge_consumed", CONSUMER,
         "generated"),
        ("reg-challenge-expired-at-the-instant-refuse", at(EXPIRES_AT), "refuse",
         "challenge_expired", CONSUMER, "generated"),
        ("reg-challenge-before-key-refuse", consumed_and_shared, "refuse", "challenge_consumed",
         CONSUMER, "generated"),
        # step 7, the key
        ("reg-fingerprint-does-not-recompute-refuse", fingerprint_wrong, "refuse",
         "fingerprint_mismatch", CONSUMER, "generated"),
        ("reg-fingerprint-not-the-challenges-refuse", challenge_for_other_key, "refuse",
         "fingerprint_mismatch", CONSUMER, "generated"),
        ("reg-assignment-already-registered-refuse", already, "refuse",
         "assignment_already_registered", CONSUMER, "generated"),
        ("reg-shared-key-refuse", shared, "refuse", "shared_key", CONSUMER, "generated"),
        ("reg-key-before-context-refuse", shared_and_cross_seat, "refuse", "shared_key",
         CONSUMER, "generated"),
        # step 8, the context, re-signed so a valid proof over it still refuses
        ("reg-cross-protocol-return-context-string-refuse", ctx("signing_context", RETURN_CONTEXT),
         "refuse", "cross_protocol_context", CONSUMER, "generated"),
        ("reg-cross-protocol-legacy-context-string-refuse",
         ctx("signing_context", LEGACY_KEY_AUTHORIZATION_CONTEXT), "refuse",
         "cross_protocol_context", CONSUMER, "generated"),
        ("reg-cross-convening-convening-id-refuse", ctx("convening_id", "convening-0002"),
         "refuse", "cross_convening_context", CONSUMER, "generated"),
        ("reg-cross-convening-candidate-refuse",
         ctx("candidate", {"repository": CANDIDATE_REPOSITORY, "pull_number": 8,
                           "head_sha": SHA_HEAD}),
         "refuse", "cross_convening_context", CONSUMER, "generated"),
        ("reg-cross-seat-refuse", ctx("seat_id", "seat-b"), "refuse", "cross_seat_context",
         CONSUMER, "generated"),
        ("reg-context-challenge-nonce-refuse", ctx("challenge_nonce", nonce("seat-b")),
         "refuse", "challenge_wrong_assignment", CONSUMER, "generated"),
        ("reg-context-before-proof-refuse", cross_convening_bad_proof, "refuse",
         "cross_convening_context", CONSUMER, "generated"),
        # step 9, the proof
        ("reg-proof-invalid-refuse", bad_proof, "refuse", "proof_invalid", CONSUMER, "generated"),
    ]


def _return_cases() -> list[tuple]:
    def legacy(w):
        w.seat_return["protocol"] = LEGACY

    def no_signature(w):
        del w.seat_return["signature"]

    def pem(w):
        w.seat_return["payload"]["entry"]["summary"] = _pem()

    def floating(w):
        w.seat_return["payload"]["entry"]["model_usage"]["costUSD"] = 0.0125

    def floating_and_unknown(w):
        floating(w)
        w.seat_return["assignment_id"] = "assignment-nobody"

    def unknown(w):
        w.seat_return["assignment_id"] = "assignment-nobody"

    def at(instant):
        def mutate(w):
            w.evaluation_time = instant
        return mutate

    def registration_only(w):
        frozen(w.snapshot, "seat-a")["permitted_operations"] = ["seat_key_registration"]

    def unregistered(w):
        w.issued["registered_keys"] = [w.registered_key("seat-b", w.signers["seat-b"])]

    def unregistered_and_cross_seat(w):
        unregistered(w)
        w.seat_return["context"]["seat_id"] = "seat-b"

    def other_key(w):
        w.issued["registered_keys"][0] = w.registered_key("seat-a", _key("seat-a/2"))

    def context_key(w):
        w.seat_return["context"]["key_fingerprint"] = "sha256:" + "ab" * 32
        w.resign()

    def replay_other_assignment(w):
        w.seat_return["assignment_id"] = assignment_id("seat-b")

    def replay_relabelled(w):
        w.seat_return["assignment_id"] = assignment_id("seat-b")
        w.seat_return["key_fingerprint"] = fingerprint(w.signers["seat-b"].public_key)

    def replay_other_convening(w):
        w.snapshot = snapshot("convening-0002")

    def ctx(member, value):
        def mutate(w):
            w.seat_return["context"][member] = value
            w.resign()
        return mutate

    def payload_moved(w):
        w.seat_return["payload"]["entry"]["summary"] = "a different entry"

    def context_digest(w):
        w.seat_return["context"]["return_digest"] = "sha256:" + "e" * 64
        w.resign()

    def other_signer(w):
        w.resign(_key("seat-a/2"))

    def legacy_bytes(w):
        context = w.seat_return["context"]
        framed = (LEGACY.encode("utf-8") + b"\n"
                  + json.dumps(context, sort_keys=True, separators=(",", ":")).encode("utf-8"))
        w.seat_return["signature"] = b64url(w.signer.sign(framed))

    def replayed(w):
        w.issued["accepted_returns"] = [{"assignment_id": assignment_id("seat-a"),
                                         "return_digest": w.seat_return["return_digest"]["value"]}]

    def bad_signature_and_replayed(w):
        other_signer(w)
        replayed(w)

    def cross_convening_and_moved(w):
        w.seat_return["context"]["convening_id"] = "convening-0002"
        payload_moved(w)

    def moved_and_bad_signature(w):
        payload_moved(w)
        other_signer(w)

    def decimal(w):
        content = payload("seat-a")
        content["entry"]["model_usage"]["costUSD"] = "-1234.5678"
        w.seat_return = w.make_return("seat-a", w.signer, content)

    def seat_b(w):
        w.seat_return = w.make_return("seat-b", w.signers["seat-b"], payload("seat-b"))

    def nothing(w):
        pass

    return [
        ("ret-accept-hand-known-answer", nothing, "accept", None, BOTH, "hand"),
        ("ret-accept-decimal-string-quantity", decimal, "accept", None, BOTH, "generated"),
        ("ret-accept-second-seat", seat_b, "accept", None, BOTH, "generated"),
        ("ret-legacy-under-replacement-refuse", legacy, "refuse", "legacy_protocol_refused",
         BOTH, "generated"),
        ("ret-signature-missing-refuse", no_signature, "refuse", "return_malformed", BOTH,
         "generated"),
        ("ret-key-transport-pem-block-in-payload-refuse", pem, "refuse", "return_malformed",
         BOTH, "generated"),
        ("ret-float-in-payload-refuse", floating, "refuse", "value_not_canonicalizable", BOTH,
         "generated"),
        ("ret-shape-before-assignment-refuse", floating_and_unknown, "refuse",
         "value_not_canonicalizable", BOTH, "generated"),
        ("ret-assignment-unknown-refuse", unknown, "refuse", "assignment_unknown", BOTH,
         "generated"),
        ("ret-assignment-not-yet-valid-refuse", at("2026-10-08T23:59:59Z"), "refuse",
         "assignment_not_yet_valid", BOTH, "generated"),
        ("ret-assignment-expired-at-the-instant-refuse", at("2026-10-09T06:00:00Z"), "refuse",
         "assignment_expired", BOTH, "generated"),
        ("ret-operation-not-permitted-refuse", registration_only, "refuse",
         "operation_not_permitted", BOTH, "generated"),
        ("ret-unregistered-refuse", unregistered, "refuse", "return_unregistered", BOTH,
         "generated"),
        ("ret-key-before-context-refuse", unregistered_and_cross_seat, "refuse",
         "return_unregistered", BOTH, "generated"),
        ("ret-key-mismatch-refuse", other_key, "refuse", "return_key_mismatch", BOTH,
         "generated"),
        ("ret-context-key-mismatch-refuse", context_key, "refuse", "return_key_mismatch", BOTH,
         "generated"),
        ("ret-replay-into-another-assignment-refuse", replay_other_assignment, "refuse",
         "return_key_mismatch", BOTH, "generated"),
        ("ret-replay-into-another-assignment-relabelled-refuse", replay_relabelled, "refuse",
         "cross_seat_context", BOTH, "generated"),
        ("ret-replay-into-another-convening-refuse", replay_other_convening, "refuse",
         "cross_convening_context", BOTH, "generated"),
        ("ret-cross-protocol-legacy-protocol-refuse", ctx("protocol", LEGACY), "refuse",
         "cross_protocol_context", BOTH, "generated"),
        ("ret-cross-protocol-registration-context-string-refuse",
         ctx("signing_context", REGISTRATION_CONTEXT), "refuse", "cross_protocol_context", BOTH,
         "generated"),
        ("ret-context-before-digest-refuse", cross_convening_and_moved, "refuse",
         "cross_convening_context", BOTH, "generated"),
        ("ret-digest-mismatch-payload-moved-refuse", payload_moved, "refuse",
         "return_digest_mismatch", BOTH, "generated"),
        ("ret-digest-mismatch-context-refuse", context_digest, "refuse", "return_digest_mismatch",
         BOTH, "generated"),
        ("ret-digest-before-signature-refuse", moved_and_bad_signature, "refuse",
         "return_digest_mismatch", BOTH, "generated"),
        ("ret-signature-by-another-key-refuse", other_signer, "refuse",
         "return_signature_invalid", BOTH, "generated"),
        ("ret-legacy-v1-signed-bytes-refuse", legacy_bytes, "refuse", "return_signature_invalid",
         BOTH, "generated"),
        ("ret-replayed-refuse", replayed, "refuse", "return_replayed", BOTH, "generated"),
        ("ret-signature-before-replay-refuse", bad_signature_and_replayed, "refuse",
         "return_signature_invalid", BOTH, "generated"),
    ]


def _completion_cases() -> list[tuple]:
    def nothing(w):
        pass

    def reversed_order(w):
        w.returns.reverse()

    def unlisted(w):
        w.returns[1]["assignment_id"] = "assignment-nobody"

    def duplicate(w):
        w.returns[1] = copy.deepcopy(w.returns[0])

    def swapped(w):
        w.returns[0]["context"]["seat_id"], w.returns[1]["context"]["seat_id"] = "seat-b", "seat-a"

    def missing(w):
        w.returns.pop()

    def none(w):
        w.returns = []

    def unlisted_and_duplicate(w):
        third = copy.deepcopy(w.returns[1])
        third["assignment_id"] = "assignment-nobody"
        w.returns = [w.returns[0], copy.deepcopy(w.returns[0]), third]

    def duplicate_and_swapped(w):
        w.returns[0]["context"]["seat_id"] = "seat-b"
        w.returns = [w.returns[0], copy.deepcopy(w.returns[0])]

    def swapped_and_missing(w):
        w.returns[0]["context"]["seat_id"] = "seat-b"
        w.returns = [w.returns[0]]

    def rule_changed(w):
        # The frozen projection at the snapshot's revision, and a changed one
        # (another seat set) at a later revision on the governed first-parent
        # history, whose rule file's tip digest differs from the frozen one. An
        # adapter that re-resolved CURRENT rules would see the change;
        # completion follows the snapshot, and accepts.
        frozen = f"{GOVERNED_REPOSITORY}@{SHA_REVISION}"
        tip = f"{GOVERNED_REPOSITORY}@{SHA_SEAT}"
        changed = {"councils": {"council-alpha": {"standing_seats": ["seat-a", "seat-c"],
                                                  "conditions": []}},
                   "sources": ["rules/council-alpha.yaml"]}
        w.environment = {
            "rules": {
                frozen: {"councils": {"council-alpha": {"standing_seats": list(SEATS),
                                                        "conditions": []}},
                         "sources": ["rules/council-alpha.yaml"]},
                tip: changed,
            },
            "governed": {f"{frozen}:rules/council-alpha.yaml": {
                "available": True, "governed": True, "sha256": SHA_FILE,
                "tip_sha256": "sha256:" + hashlib.sha256(
                    canonical.serialize(changed).encode("utf-8")).hexdigest()}},
            "governed_history": {
                frozen: {"on_first_parent": True, "at_or_after": [SHA_REVISION]},
                tip: {"on_first_parent": True, "at_or_after": [SHA_REVISION, SHA_SEAT]},
            },
        }

    return [
        ("cmp-accept", nothing, "accept", None, BOTH, "generated"),
        ("cmp-accept-in-any-arrival-order", reversed_order, "accept", None, BOTH, "generated"),
        ("cmp-accept-after-the-rule-changed", rule_changed, "accept", None, BOTH, "generated"),
        ("cmp-return-unlisted-refuse", unlisted, "refuse", "return_unlisted", BOTH, "generated"),
        ("cmp-return-duplicate-same-count-refuse", duplicate, "refuse", "return_duplicate", BOTH,
         "generated"),
        ("cmp-wrong-identities-same-count-refuse", swapped, "refuse", "completion_set_mismatch",
         BOTH, "generated"),
        ("cmp-return-missing-refuse", missing, "refuse", "return_missing", BOTH, "generated"),
        ("cmp-no-returns-refuse", none, "refuse", "return_missing", BOTH, "generated"),
        ("cmp-unlisted-before-duplicate-refuse", unlisted_and_duplicate, "refuse",
         "return_unlisted", BOTH, "generated"),
        ("cmp-duplicate-before-identity-refuse", duplicate_and_swapped, "refuse",
         "return_duplicate", BOTH, "generated"),
        ("cmp-identity-before-missing-refuse", swapped_and_missing, "refuse",
         "completion_set_mismatch", BOTH, "generated"),
    ]


# --------------------------------------------------------------------------
# Building.
# --------------------------------------------------------------------------

def _vector(case_id: str, boundary: str, applies_to: list[str], requirement_ids: list[str],
            evaluation_time: str, inputs: dict, environment: dict | None, outcome: str,
            refusal: str | None, derived: dict, origin: str) -> dict:
    findings = ["legacy_protocol_routed"] if outcome == "route" else []
    if outcome == "route":
        derived = {"classification": "legacy"}
    vector = {
        "schema_version": 1, "kind": "openxfactory-council-convening-conformance-vector",
        "case_id": case_id, "area": AREA, "boundary": boundary, "applies_to": applies_to,
        "requirement_ids": requirement_ids, "evaluation_time": evaluation_time,
        "inputs": inputs,
        "expected": {"outcome": outcome, "refusal": refusal, "findings": findings,
                     "derived": derived, "derived_origin": origin},
    }
    if environment:
        vector["environment"] = environment
    return vector


def _hand(world, known_bytes: bytes, known_fingerprint: str) -> dict:
    """A hand-authored known answer, checked here against the world it names:
    a hand literal that no longer describes the world is a build failure."""
    derived = {"key_fingerprint": known_fingerprint, "signed_bytes": b64url(known_bytes)}
    if derived != world.derived():
        raise ValueError("a hand-authored signing known answer no longer matches its world")
    return derived


def build(root: Path) -> dict[str, dict]:
    """Every signing-area vector, keyed by its path relative to `conformance/`."""
    root = Path(root)
    out: dict[str, dict] = {}

    for case_id, mutate, outcome, refusal, applies_to, origin in _registration_cases():
        world = RegistrationWorld(root)
        mutate(world)
        derived = {}
        if outcome == "accept":
            derived = (_hand(world, HAND_REGISTRATION_BYTES, HAND_SEAT_A_FINGERPRINT)
                       if origin == "hand" else world.derived())
        inputs, environment = world.vector_parts()
        out[f"vectors/{AREA}/{case_id}.json"] = _vector(
            case_id, "registration", applies_to, REG_FRS, world.evaluation_time, inputs,
            environment, outcome, refusal, derived, origin)

    for case_id, mutate, outcome, refusal, applies_to, origin in _return_cases():
        world = ReturnWorld(root)
        mutate(world)
        derived = {}
        if outcome == "accept":
            derived = (_hand(world, HAND_RETURN_BYTES, HAND_SEAT_A_FINGERPRINT)
                       if origin == "hand" else world.derived())
        inputs, environment = world.vector_parts()
        out[f"vectors/{AREA}/{case_id}.json"] = _vector(
            case_id, "return", applies_to, RET_FRS, world.evaluation_time, inputs, environment,
            outcome, refusal, derived, origin)

    for case_id, mutate, outcome, refusal, applies_to, origin in _completion_cases():
        world = CompletionWorld(root)
        mutate(world)
        inputs, environment = world.vector_parts()
        out[f"vectors/{AREA}/{case_id}.json"] = _vector(
            case_id, "completion", applies_to, CMP_FRS, world.evaluation_time, inputs,
            environment, outcome, refusal, {}, origin)
    return out
