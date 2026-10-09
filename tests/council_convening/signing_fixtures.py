"""Record builders for the Phase 4 tests: a frozen snapshot with PER-SEAT
holders, each seat's producer binding, its verified identity, the issued
challenge, and signed registrations and returns (feature 035, data-model E5 to
E10).

Shared by `test_signing.py` (T042) and the `check` cases of
`test_validator_cli.py` (T045), so the two describe one well-formed world.
Every builder returns a fresh value; a test mutates its own copy.

PER-SEAT BINDINGS. Brett Heap's 025 ruling (A) of 2026-10-09, "Per-seat
environments (Recommended)": one producer binding per seat, told apart by a
per-seat GitHub environment in the OIDC `sub`, with the holder's
`principal_ref` equal to the binding id. So each seat here has its own binding
`binding-<seat>`, whose `subject_template` names the environment
`council-<seat>`, and each assignment's holder carries that id as both its
`binding_ref` and its `principal_ref`. Data-model E5 and E7 step 5 carry that
shape unchanged: `binding_ref` resolves to the seat's own binding, and the seat
job's claims, its environment included through `sub`, are checked against that
binding alone.

THE WORKFLOW COMMIT OF A SEAT JOB. Brett Heap's OPEN-3 follow-up 3 of
2026-10-08, "At or after the frozen rev (Recommended)": a seat job's
`job_workflow_sha` must be on the governed first-parent history at or after the
snapshot's frozen `governed.revision`. `SHA_SEAT` is after it, `SHA_BEFORE`
before it, and `SHA_OFF` off that history.

It imports no implementation module of this family at import time, so a test
module that uses it still fails at its own import while `signing` is absent
(the tests-first rule). The one family module it reaches, the generator's
labelled test keys, is imported lazily inside `key()`.
"""

from __future__ import annotations

import base64
import copy
import hashlib
import json

from scripts.signed_execution_chain import canonical

from .conftest import CONFORMANCE

REPLACEMENT = "xfc-resolved-council-1"
LEGACY = "xfactory-council-seat-return/v1"
REGISTRATION_CONTEXT = "xfc-resolved-council-1/seat-key-registration"
RETURN_CONTEXT = "xfc-resolved-council-1/seat-return"
LEGACY_KEY_AUTHORIZATION_CONTEXT = "xfactory-council-seat-key-authorization/v1"

SHA_HEAD = "1" * 40
SHA_REVISION = "2" * 40      # the snapshot's frozen governed.revision
SHA_SEAT = "4" * 40          # a seat job's workflow commit, after the frozen revision
SHA_BEFORE = "5" * 40        # a governed commit before the frozen revision
SHA_OFF = "6" * 40           # a commit off the governed first-parent history
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

#: Brett Heap's OPEN-1 ruling of 2026-10-08, "600 s challenge, 6 h assignment
#: (Recommended)": the CONTRACT ceiling on a challenge's lifetime.
CHALLENGE_CEILING = 600
PAYLOAD_LIMIT = 1048576

EVALUATION_TIME = "2026-10-09T01:00:00Z"
EVALUATION_EPOCH = 1791507600            # the same instant, in seconds since the epoch
ISSUED_AT = "2026-10-09T00:55:00Z"
EXPIRES_AT = "2026-10-09T01:05:00Z"      # exactly the 600-second ceiling after ISSUED_AT


def b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def b64url_decode(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def fingerprint(public_key: bytes) -> str:
    """The estate's one spelling, computed here independently of the module
    under test: `sha256:` and the hex SHA-256 of the raw 32-byte key (openXwallet
    `fingerprint_of_public_key`; codexFactory `key_fingerprint`)."""
    return "sha256:" + hashlib.sha256(public_key).hexdigest()


def binding_id(seat: str) -> str:
    return f"binding-{seat}"


def environment_name(seat: str) -> str:
    return f"council-{seat}"


def assignment_id(seat: str) -> str:
    return f"assignment-{seat}"


def challenge_id(seat: str) -> str:
    return f"challenge-{seat}"


def key(seat: str, generation: int = 1):
    """A labelled test key for this module's own cases, from the generator's
    one derivation (research R18). The label names this test module, so no
    corpus key is reused here. Nothing private is written anywhere."""
    from scripts.council_convening import generate

    return generate.test_key(f"phase4-unit/{seat}/{generation}")


def nonce(label: str) -> str:
    """A public, deterministic 32-byte nonce: the SHA-256 of a label."""
    return b64url(hashlib.sha256(f"council-convening phase 4 nonce {label}".encode()).digest())


# --- frozen state: the commission record and the snapshot (E2, E4, E5) -------


def convening_record() -> dict:
    """A shape-valid E2 record of an unclassed council with two standing seats."""
    return {
        "schema_version": 1,
        "kind": "xfactory_council_convening",
        "protocol": REPLACEMENT,
        "council_id": "council-alpha",
        "subject_pin": SHA_HEAD,
        "packet_refs": ["packet/alpha-1"],
        "required_seats": list(SEATS),
        "required_seats_provenance": {
            "candidate": {
                "repository": CANDIDATE_REPOSITORY,
                "pull_number": 7,
                "head_sha": SHA_HEAD,
            },
            "governed": {
                "repository": GOVERNED_REPOSITORY,
                "revision": SHA_REVISION,
                "sources": [
                    {"kind": "file", "path": "rules/council-alpha.yaml", "sha256": SHA_FILE},
                ],
            },
            "standing_seats": list(SEATS),
            "conditions": [],
            "fact_sources": [],
            "consumed_facts": {},
        },
    }


def digest_of(value) -> dict:
    return {"construction": "xfc-jcs-sha256-1", "subject": "council_convening",
            "value": canonical.digest(value)}


def holder(seat: str) -> dict:
    """The per-seat holder: `binding_ref` and `principal_ref` are both the
    seat's own binding id (025 ruling A)."""
    return {"principal_kind": "github_oidc_job", "principal_ref": binding_id(seat),
            "binding_ref": binding_id(seat)}


def assignment(convening: dict, seat: str, **overrides) -> dict:
    value = {
        "schema_version": 1,
        "kind": "xfactory_council_seat_assignment",
        "protocol": REPLACEMENT,
        "convening_id": CONVENING_ID,
        "convening_digest": digest_of(convening),
        "council_id": convening["council_id"],
        "candidate": copy.deepcopy(convening["required_seats_provenance"]["candidate"]),
        "assignment_id": assignment_id(seat),
        "seat_id": seat,
        "holder": holder(seat),
        "permitted_operations": ["seat_key_registration", "seat_return"],
        "not_before": "2026-10-09T00:00:00Z",
        "expires_at": "2026-10-09T06:00:00Z",
    }
    value.update(overrides)
    return value


def snapshot(convening_id: str = CONVENING_ID) -> dict:
    convening = convening_record()
    assignments = [assignment(convening, seat, convening_id=convening_id) for seat in SEATS]
    return {
        "schema_version": 1,
        "kind": "xfactory_council_convening_snapshot",
        "protocol": REPLACEMENT,
        "convening_id": convening_id,
        "convening_digest": digest_of(convening),
        "convening": convening,
        "assignments": assignments,
        "admitted_at": "2026-10-09T00:00:00Z",
    }


def frozen_assignment(snap: dict, seat: str) -> dict:
    return next(a for a in snap["assignments"] if a["seat_id"] == seat)


# --- the seat's binding and its verified identity (E10) ----------------------


def binding(seat: str) -> dict:
    """The seat's own producer binding (E10), with the seat's environment in
    its subject template."""
    return {
        "schema_version": 1,
        "kind": "xfactory_council_producer_binding",
        "protocol": REPLACEMENT,
        "binding_id": binding_id(seat),
        "principal_kind": "github_oidc_job",
        "issuer": ISSUER,
        "audience": AUDIENCE,
        "caller_repository": CALLER_REPOSITORY,
        "repository_id": CALLER_REPOSITORY_ID,
        "subject_claim_keys": ["repo", "context"],
        "subject_template": f"repo:{CALLER_REPOSITORY}:environment:{environment_name(seat)}",
        "permitted_workflows": [
            {"operation": "seat_execution", "job_workflow_ref": SEAT_WORKFLOW,
             "workflow_revision_rule": "on_governed_history_since_revision"},
        ],
        "broker": {"broker_ref": "broker-example", "capability_verified": False,
                   "evidence_ref": None},
    }


def bindings() -> list[dict]:
    return [binding(seat) for seat in SEATS]


def identity(seat: str, **claims) -> dict:
    """The seat job's verified identity evidence: its claims, verified, and the
    principal the trusted dispatcher resolved, which is the seat's binding id."""
    value = {
        "verified": True,
        "claims": {
            "iss": ISSUER,
            "aud": AUDIENCE,
            "sub": f"repo:{CALLER_REPOSITORY}:environment:{environment_name(seat)}",
            "nbf": EVALUATION_EPOCH - 60,
            "exp": EVALUATION_EPOCH + 300,
            "repository": CALLER_REPOSITORY,
            "repository_id": str(CALLER_REPOSITORY_ID),
            "environment": environment_name(seat),
            "job_workflow_ref": SEAT_WORKFLOW,
            "job_workflow_sha": SHA_SEAT,
        },
        "principal": {"principal_kind": "github_oidc_job", "principal_ref": binding_id(seat)},
    }
    value["claims"].update(claims)
    return value


def governed_history() -> dict:
    """The `governed_history` oracle for the three seat commits."""
    return {
        f"{GOVERNED_REPOSITORY}@{SHA_SEAT}": {"on_first_parent": True,
                                              "at_or_after": [SHA_REVISION]},
        f"{GOVERNED_REPOSITORY}@{SHA_REVISION}": {"on_first_parent": True,
                                                  "at_or_after": [SHA_REVISION]},
        f"{GOVERNED_REPOSITORY}@{SHA_BEFORE}": {"on_first_parent": True, "at_or_after": []},
        f"{GOVERNED_REPOSITORY}@{SHA_OFF}": {"on_first_parent": False, "at_or_after": []},
    }


def repository_identity() -> dict:
    """The `repository_identity` oracle: the corpus's frozen identity fixture's
    text, never the live map (research R8; R7-M1)."""
    fixture = json.loads((CONFORMANCE / "fixtures" / "repository-identity.json")
                         .read_text(encoding="utf-8"))
    return {"state": "text", "text": fixture["text"]}


# --- the challenge and the registration (E6, E7, E9) -------------------------


def challenge(seat: str, public_key: bytes, **overrides) -> dict:
    value = {
        "schema_version": 1,
        "kind": "xfactory_council_registration_challenge",
        "protocol": REPLACEMENT,
        "challenge_id": challenge_id(seat),
        "assignment_id": assignment_id(seat),
        "key_fingerprint": fingerprint(public_key),
        "nonce": nonce(seat),
        "issued_at": ISSUED_AT,
        "expires_at": EXPIRES_AT,
    }
    value.update(overrides)
    return value


def registration_context(frozen: dict, issued: dict, key_fingerprint: str) -> dict:
    """The registration context, rebuilt here from the data-model E9 table, so
    the module under test is compared with an independent construction."""
    return {
        "signing_context": REGISTRATION_CONTEXT,
        "protocol": frozen["protocol"],
        "convening_id": frozen["convening_id"],
        "convening_digest": frozen["convening_digest"]["value"],
        "council_id": frozen["council_id"],
        "candidate": copy.deepcopy(frozen["candidate"]),
        "assignment_id": frozen["assignment_id"],
        "seat_id": frozen["seat_id"],
        "key_fingerprint": key_fingerprint,
        "challenge_id": issued["challenge_id"],
        "challenge_nonce": issued["nonce"],
    }


def jcs(value) -> bytes:
    return canonical.serialize(value).encode("utf-8")


def sign_registration(registration: dict, signer) -> dict:
    """Re-sign `registration["context"]` as presented, with `signer`."""
    registration["proof"] = b64url(signer.sign(jcs(registration["context"])))
    return registration


def registration(snap: dict, seat: str, signer, issued: dict) -> dict:
    frozen = frozen_assignment(snap, seat)
    value = {
        "schema_version": 1,
        "kind": "xfactory_council_seat_key_registration",
        "protocol": REPLACEMENT,
        "assignment_id": frozen["assignment_id"],
        "challenge_id": issued["challenge_id"],
        "public_key": b64url(signer.public_key),
        "key_fingerprint": fingerprint(signer.public_key),
        "context": registration_context(frozen, issued, fingerprint(signer.public_key)),
    }
    return sign_registration(value, signer)


def registration_record(seat: str = "seat-a") -> dict:
    """One seat's signed registration alone, with no environment: what `check`
    reads offline."""
    signer = key(seat)
    return registration(snapshot(), seat, signer, challenge(seat, signer.public_key))


def registration_case(seat: str = "seat-a") -> dict:
    """One seat's registration and everything its boundary reads. Each member
    is fresh; mutate it, then run it through the module under test."""
    snap = snapshot()
    signer = key(seat)
    issued = challenge(seat, signer.public_key)
    return {
        "seat": seat,
        "signer": signer,
        "snapshot": snap,
        "bindings": bindings(),
        "registration": registration(snap, seat, signer, issued),
        "environment": {
            "issued": {"challenges": [issued], "consumed_challenges": [],
                       "registered_keys": []},
            "identity": identity(seat),
            "repository_identity": repository_identity(),
            "governed_history": governed_history(),
        },
        "evaluation_time": EVALUATION_TIME,
        "selected_protocol": REPLACEMENT,
    }


# --- the return (E8, E9) -------------------------------------------------------


def payload(seat: str) -> dict:
    """A seat's whole checked entry, as the producer signs it: open members,
    with the one non-integer quantity written as a `decimal_string`."""
    return {
        "seat": seat,
        "entry": {"summary": f"{seat} reviewed the candidate", "findings": [],
                  "model_usage": {"costUSD": "0.0125", "turns": 3}},
    }


def return_digest(value) -> dict:
    return {"construction": "xfc-jcs-sha256-1", "subject": "council_seat_return_payload",
            "value": canonical.digest(value)}


def return_context(frozen: dict, key_fingerprint: str, digest_value: str) -> dict:
    return {
        "signing_context": RETURN_CONTEXT,
        "protocol": frozen["protocol"],
        "convening_id": frozen["convening_id"],
        "convening_digest": frozen["convening_digest"]["value"],
        "council_id": frozen["council_id"],
        "candidate": copy.deepcopy(frozen["candidate"]),
        "assignment_id": frozen["assignment_id"],
        "seat_id": frozen["seat_id"],
        "key_fingerprint": key_fingerprint,
        "return_digest": digest_value,
    }


def sign_return(value: dict, signer) -> dict:
    """Re-sign `value["context"]` as presented, with `signer`."""
    value["signature"] = b64url(signer.sign(jcs(value["context"])))
    return value


def seat_return(snap: dict, seat: str, signer, content: dict | None = None) -> dict:
    frozen = frozen_assignment(snap, seat)
    content = payload(seat) if content is None else content
    digest = return_digest(content)
    value = {
        "schema_version": 1,
        "kind": "xfactory_council_seat_return",
        "protocol": REPLACEMENT,
        "assignment_id": frozen["assignment_id"],
        "key_fingerprint": fingerprint(signer.public_key),
        "payload": content,
        "return_digest": digest,
        "context": return_context(frozen, fingerprint(signer.public_key), digest["value"]),
    }
    return sign_return(value, signer)


def registered_key(seat: str, signer) -> dict:
    """An `environment.issued.registered_keys` entry. It carries the public
    key as well as its fingerprint, because a return carries no key and is
    verified with the one registered for its assignment."""
    return {"assignment_id": assignment_id(seat), "key_fingerprint": fingerprint(signer.public_key),
            "public_key": b64url(signer.public_key)}


def return_case(seat: str = "seat-a") -> dict:
    snap = snapshot()
    signers = {name: key(name) for name in SEATS}
    return {
        "seat": seat,
        "signer": signers[seat],
        "signers": signers,
        "snapshot": snap,
        "return": seat_return(snap, seat, signers[seat]),
        "environment": {
            "issued": {"registered_keys": [registered_key(name, signers[name]) for name in SEATS],
                       "accepted_returns": []},
        },
        "evaluation_time": EVALUATION_TIME,
        "selected_protocol": REPLACEMENT,
    }


def completion_case() -> dict:
    snap = snapshot()
    signers = {name: key(name) for name in SEATS}
    return {
        "snapshot": snap,
        "signers": signers,
        "returns": [seat_return(snap, seat, signers[seat]) for seat in SEATS],
    }


# --- the legacy v1 bytes, for the cross-protocol cases --------------------------


def legacy_v1_signed_bytes(context: dict) -> bytes:
    """The legacy framing, rebuilt here from its published form for the
    cross-protocol cases only: the protocol string, a newline, and
    `json.dumps` with sorted keys. It is a second canonicalization, which is
    exactly why the replacement never uses it (research R3)."""
    return (LEGACY.encode("utf-8") + b"\n"
            + json.dumps(context, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def pem_private_key_block() -> str:
    """A PEM private-key header, built from parts so no committed file carries
    it contiguously (research R9)."""
    return "-----" + "BEGIN " + "PRIVATE" + " KEY-----\nAAAA\n-----END " + "PRIVATE KEY-----"
