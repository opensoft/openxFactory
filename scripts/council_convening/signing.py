"""Assignment-bound key registration, signed returns and completion.

T047, feature 035 Phase 4, written from data-model E6 (the challenge), E7 (the
registration), E8 (the return and the completion order) and E9 (the two
signing contexts), and nothing else.

ONE CONSTRUCTION, NO SECOND FRAMING (research R3). The signed bytes of a context
are the UTF-8 of `canonical.serialize(context)`, the `xfc-jcs-sha256-1`
serialization, with no prefix line and no other canonicalization. A replacement
message therefore always begins with `{`, and a legacy v1 message with its
protocol string and a newline, so neither protocol's signature verifies as the
other's. The return digest is the same construction, subject
`council_seat_return_payload`.

VERIFICATION IS THE STANDARD LIBRARY'S. Signatures are checked with
`scripts/signed_execution_chain/ed25519.verify`, the repository's one Ed25519
verifier; this module signs nothing, and imports no signing library.

THE ESTATE'S ONE FINGERPRINT SPELLING: `sha256:` and the hex SHA-256 of the raw
32-byte public key (openXwallet `fingerprint_of_public_key`; codexFactory
`key_fingerprint`). Brett Heap ruled it on 2026-10-09, "Estate spelling
(Recommended)". `fingerprint_of` is its one home here.

CONTEXTS ARE REBUILT, NEVER TRUSTED. A verifier rebuilds the expected context
from frozen state (the snapshot's assignment, the issued challenge, the key)
and compares it with the presented one member by member, before it verifies
the signature. That comparison is what tells the cross-protocol, cross-convening
and cross-seat refusals apart.

EVERY ORDER IS NORMATIVE: the first failing check names the refusal (R21). Each
boundary begins with classification (data-model E1), so a legacy record is
refused or routed and never judged by these rules.

E7 STEP 5 READS THE HOLDER'S BINDING (E10). The binding's offline checks and its
claim checks, with operation `seat_execution`, are the producer-binding module's
(Phase 5, T054); `_check_holder_binding` is the one place this module calls it.
Brett Heap's OPEN-3 follow-up 3 (2026-10-08), "At or after the frozen rev
(Recommended)", is applied there: a seat job's workflow commit must be on the
governed first-parent history at or after the snapshot's frozen revision.

Completion lives here, beside the return it reads, so the Phase 3 module that
freezes the assignments is not reopened.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import re
from datetime import datetime, timezone
from functools import lru_cache
from typing import Any, Mapping

from . import classification, records
from ..signed_execution_chain import canonical, ed25519

REPLACEMENT = next(pid for pid, entry in classification.LANDED_PROTOCOLS.items()
                   if entry["role"] == "replacement")

#: The two versioned signing contexts, as the protocol registry lands them.
REGISTRATION_CONTEXT, RETURN_CONTEXT = classification.LANDED_PROTOCOLS[REPLACEMENT][
    "signing_contexts"]

CHALLENGE_SCHEMA = "registration-challenge.schema.yaml"
REGISTRATION_SCHEMA = "seat-key-registration.schema.yaml"
RETURN_SCHEMA = "seat-return.schema.yaml"
CHALLENGE_SCHEMA_ID = records.ID_BASE + CHALLENGE_SCHEMA
REGISTRATION_SCHEMA_ID = records.ID_BASE + REGISTRATION_SCHEMA
RETURN_SCHEMA_ID = records.ID_BASE + RETURN_SCHEMA

CHALLENGE_KIND = "xfactory_council_registration_challenge"
REGISTRATION_KIND = "xfactory_council_seat_key_registration"
RETURN_KIND = "xfactory_council_seat_return"

#: E7 step 2: the root-authorization members, as the legacy recognition rule
#: names them.
ROOT_AUTHORIZATION_MEMBERS = tuple(next(
    rule["members"] for rule in classification.LANDED_PROTOCOLS[
        next(pid for pid, e in classification.LANDED_PROTOCOLS.items()
             if e["role"] == "legacy")]["recognition"]
    if rule["rule"] == "root_authorization_member"))

#: E7 step 3 and E8 step 2: key transport. A member by one of these names at any
#: depth, or a PEM private-key block in any string, is the record's malformed
#: code. The spec delta: "key transport MUST refuse".
KEY_TRANSPORT_MEMBERS = frozenset({"private_key", "secret_key", "seed", "sk", "d"})
PEM_PRIVATE_KEY = re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----")

PERMITTED_REGISTRATION = "seat_key_registration"
PERMITTED_RETURN = "seat_return"
SEAT_OPERATION = "seat_execution"

#: The rules `check` cannot run offline, as it reports them (T045).
REGISTRATION_STATE_RULES = (
    "assignment (assignment_unknown, assignment_not_yet_valid, assignment_expired, "
    "operation_not_permitted)",
    "principal (the holder's binding, the verified claims, wrong_principal)",
    "challenge (challenge_unknown, challenge_malformed, challenge_wrong_assignment, "
    "challenge_consumed, challenge_expired)",
    "registered keys (assignment_already_registered, shared_key)",
    "context against frozen state",
)
RETURN_STATE_RULES = (
    "assignment (assignment_unknown, assignment_not_yet_valid, assignment_expired, "
    "operation_not_permitted)",
    "registered key (return_unregistered, return_key_mismatch)",
    "context against frozen state",
    "signature (return_signature_invalid; the return carries no key)",
    "replay (return_replayed)",
)
CHALLENGE_STATE_RULES = (
    "issued state (challenge_unknown, challenge_wrong_assignment, challenge_consumed, "
    "challenge_expired)",
)

#: The context members, in the order their comparison names a refusal (E7 step
#: 8, E8 step 5).
PROTOCOL_MEMBERS = ("signing_context", "protocol")
CONVENING_MEMBERS = ("convening_id", "convening_digest", "council_id", "candidate")
SEAT_MEMBERS = ("assignment_id", "seat_id")
CHALLENGE_MEMBERS = ("challenge_id", "challenge_nonce")


class Routed(Exception):
    """A legacy record under a selection that routes it: this family gives no
    verdict. `outcome` is the classification's route, findings included."""

    def __init__(self, outcome: records.Outcome):
        self.outcome = outcome
        super().__init__("routed to the legacy verifier")


class InconsistentEnvironment(ValueError):
    """Oracle data that contradicts itself, such as a registered key whose
    fingerprint is not its public key's. A harness error, never a refusal."""


# --------------------------------------------------------------------------
# The contract values this module reads from the landed schemas.
# --------------------------------------------------------------------------

def _schema_const(name: str, definition: str) -> int:
    path = records.REPO_ROOT / records.FAMILY_REL / name
    document = records.strict_yaml(path.read_bytes(), name)
    value = document["$defs"][definition]["const"]
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise records.SchemaLoadError(f"{name}: $defs/{definition} is not a positive integer")
    return value


def contract_challenge_ceiling() -> int:
    """Brett Heap's OPEN-1 ruling of 2026-10-08, "600 s challenge, 6 h
    assignment (Recommended)", read from the challenge schema: the contract
    maximum of `expires_at - issued_at`, in seconds."""
    return _schema_const(CHALLENGE_SCHEMA, "lifetime_ceiling_seconds")


def contract_payload_limit() -> int:
    """The bound on a return payload's canonical bytes, from the return schema."""
    return _schema_const(RETURN_SCHEMA, "payload_limit_bytes")


CHALLENGE_LIFETIME_CEILING_SECONDS = contract_challenge_ceiling()
PAYLOAD_LIMIT_BYTES = contract_payload_limit()


@lru_cache(maxsize=1)
def _default_schemas() -> records.SchemaSet:
    return records.load_schemas()


@lru_cache(maxsize=1)
def _default_registry() -> classification.Registry:
    return classification.load_registry()


# --------------------------------------------------------------------------
# Fingerprints, bytes and digests.
# --------------------------------------------------------------------------

def fingerprint_of(public_key: bytes) -> str:
    """The estate's one spelling of a key fingerprint: `sha256:` and the hex
    SHA-256 of the raw 32-byte public key."""
    if not isinstance(public_key, (bytes, bytearray)) or len(public_key) != 32:
        raise ValueError("a key fingerprint is of a raw 32-byte Ed25519 public key")
    return "sha256:" + hashlib.sha256(bytes(public_key)).hexdigest()


def b64url(raw: bytes) -> str:
    """Unpadded base64url, the spelling of every key, nonce and signature."""
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def b64url_decode(text: str) -> bytes:
    """Decode unpadded base64url. The schemas have already checked the grammar
    and the length; this refuses anything else as a `ValueError`."""
    if not isinstance(text, str) or "=" in text:
        raise ValueError("not unpadded base64url")
    try:
        return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))
    except (binascii.Error, ValueError) as exc:
        raise ValueError("not unpadded base64url") from exc


def signed_bytes(context: Mapping[str, Any]) -> bytes:
    """The bytes a seat signs: the UTF-8 of the context's `xfc-jcs-sha256-1`
    serialization. A value the construction refuses raises its
    `ConstructionError`."""
    return canonical.serialize(context).encode("utf-8")


def return_digest(payload: Any) -> dict[str, str]:
    """`xfc-jcs-sha256-1`, subject `council_seat_return_payload`, over the
    return's payload."""
    return {"construction": canonical.CONSTRUCTION, "subject": "council_seat_return_payload",
            "value": canonical.digest(payload)}


# --------------------------------------------------------------------------
# The contexts (E9), rebuilt from frozen state.
# --------------------------------------------------------------------------

def _common_context(signing_context: str, assignment: Mapping[str, Any],
                    key_fingerprint: str) -> dict[str, Any]:
    return {
        "signing_context": signing_context,
        "protocol": assignment["protocol"],
        "convening_id": assignment["convening_id"],
        "convening_digest": assignment["convening_digest"]["value"],
        "council_id": assignment["council_id"],
        "candidate": dict(assignment["candidate"]),
        "assignment_id": assignment["assignment_id"],
        "seat_id": assignment["seat_id"],
        "key_fingerprint": key_fingerprint,
    }


def registration_context(assignment: Mapping[str, Any], challenge: Mapping[str, Any],
                         key_fingerprint: str) -> dict[str, Any]:
    """The registration context the frozen assignment, the issued challenge and
    the key determine."""
    context = _common_context(REGISTRATION_CONTEXT, assignment, key_fingerprint)
    context["challenge_id"] = challenge["challenge_id"]
    context["challenge_nonce"] = challenge["nonce"]
    return context


def return_context(assignment: Mapping[str, Any], key_fingerprint: str,
                   return_digest_value: str) -> dict[str, Any]:
    """The return context the frozen assignment, the registered key and the
    payload's digest determine."""
    context = _common_context(RETURN_CONTEXT, assignment, key_fingerprint)
    context["return_digest"] = return_digest_value
    return context


def _compare_context(presented: Mapping[str, Any], expected: Mapping[str, Any],
                     groups: tuple[tuple[tuple[str, ...], str], ...]) -> None:
    """Compare member by member in `groups` order; the first differing group
    names the refusal."""
    for members, code in groups:
        for member in members:
            if presented.get(member) != expected.get(member):
                raise records.Refused(code, member=f"context.{member}")


# --------------------------------------------------------------------------
# Shared steps.
# --------------------------------------------------------------------------

def refuse_key_transport(value: Any, code: str, where: str = "") -> None:
    """Refuse a member named like key material at any depth, or a PEM
    private-key block in any string, as `code`. Names the member, never the
    value."""
    if isinstance(value, Mapping):
        for name, item in value.items():
            path = f"{where}.{name}" if where else str(name)
            if name in KEY_TRANSPORT_MEMBERS:
                raise records.Refused(code, member=path)
            refuse_key_transport(item, code, path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            refuse_key_transport(item, code, f"{where}[{index}]")
    elif isinstance(value, str) and PEM_PRIVATE_KEY.search(value):
        raise records.Refused(code, member=where or "(root)")


def _shape(record: Any, schema_id: str, code: str, schemas: records.SchemaSet) -> None:
    errors = schemas.errors(schema_id, record)
    if errors:
        where = "/".join(map(str, errors[0].absolute_path)) or "(root)"
        raise records.Refused(code, member=where)
    refuse_key_transport(record, code)


def _classify(record: Any, selected_protocol: str | None, registry: classification.Registry,
              statuses: Mapping[str, str] | None) -> None:
    """E7 and E8 step 1: classification and the selection's effect."""
    outcome = classification.classify_and_select(record, selected_protocol, registry, statuses)
    if outcome.outcome == "refuse":
        raise records.Refused(outcome.refusal, member="protocol")
    if outcome.outcome == "route":
        raise Routed(outcome)


def _instant(text: str) -> datetime:
    return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def _frozen_assignment(snapshot: Mapping[str, Any], assignment_id: str) -> Mapping[str, Any]:
    for assignment in snapshot.get("assignments", []):
        if isinstance(assignment, Mapping) and assignment.get("assignment_id") == assignment_id:
            return assignment
    raise records.Refused("assignment_unknown", member="assignment_id")


def _use_assignment(snapshot: Mapping[str, Any], assignment_id: str, operation: str,
                    evaluation_time: str) -> Mapping[str, Any]:
    """E7 step 4 and E8 step 3: the assignment, when it is used."""
    assignment = _frozen_assignment(snapshot, assignment_id)
    now = _instant(evaluation_time)
    if now < _instant(assignment["not_before"]):
        raise records.Refused("assignment_not_yet_valid", member="assignment.not_before")
    if now >= _instant(assignment["expires_at"]):
        raise records.Refused("assignment_expired", member="assignment.expires_at")
    if operation not in assignment.get("permitted_operations", ()):
        raise records.Refused("operation_not_permitted", member="assignment.permitted_operations")
    return assignment


def _issued(environment: Mapping[str, Any]) -> Mapping[str, Any]:
    issued = environment.get("issued", {})
    return issued if isinstance(issued, Mapping) else {}


# --------------------------------------------------------------------------
# The challenge (E6).
# --------------------------------------------------------------------------

def check_challenge(challenge: Any, *, schemas: records.SchemaSet | None = None) -> None:
    """An issued challenge against E6 and the ruled ceiling: `challenge_malformed`
    unless its shape holds and `0 < expires_at - issued_at <= 600` seconds."""
    schemas = schemas if schemas is not None else _default_schemas()
    if schemas.errors(CHALLENGE_SCHEMA_ID, challenge):
        raise records.Refused("challenge_malformed", member="challenge")
    records.check_canonicalizable(challenge, code="challenge_malformed", member="challenge")
    lifetime = (_instant(challenge["expires_at"]) - _instant(challenge["issued_at"])).total_seconds()
    if not 0 < lifetime <= CHALLENGE_LIFETIME_CEILING_SECONDS:
        raise records.Refused("challenge_malformed", member="challenge.expires_at")


# --------------------------------------------------------------------------
# Registration (E7).
# --------------------------------------------------------------------------

def _check_holder_binding(binding: Mapping[str, Any], *, governed: Mapping[str, Any],
                          environment: Mapping[str, Any], evaluation_time: str,
                          schemas: records.SchemaSet) -> None:
    """E7 step 5's binding half: E10 steps 1 to 6 on the holder's binding, then
    E10 steps 7 to 14 on the seat job's verified claims with operation
    `seat_execution`, step 14 applying the seat rule against the snapshot's
    FROZEN `governed` member. The producer-binding module (Phase 5, T054) owns
    every one of those steps; this is the one place they are called from."""
    try:
        from . import binding as producer_binding
    except ImportError as exc:
        raise records.SchemaLoadError(
            "the producer-binding module (Phase 5, T054) has not landed at this commit, "
            "and registration reads the holder's binding (data-model E7 step 5)") from exc
    producer_binding.check_seat_job(
        binding, governed=governed, environment=environment,
        evaluation_time=evaluation_time, schemas=schemas)


def check_registration(registration: Any, *, snapshot: Mapping[str, Any],
                       bindings: list[Mapping[str, Any]], environment: Mapping[str, Any],
                       evaluation_time: str, selected_protocol: str | None,
                       schemas: records.SchemaSet | None = None,
                       registry: classification.Registry | None = None) -> dict[str, str]:
    """The registration boundary, in the E7 order. Returns the derived values
    `{key_fingerprint, signed_bytes}`; raises `records.Refused` on the first
    failing check, or `Routed` for a legacy record a legacy selection routes."""
    schemas = schemas if schemas is not None else _default_schemas()
    registry = registry if registry is not None else _default_registry()

    # 1. Classification and selection.
    _classify(registration, selected_protocol, registry, environment.get("registry_status"))
    # 2. Root authorization, before the shape: never reclassified as legacy (I3).
    for member in ROOT_AUTHORIZATION_MEMBERS:
        if member in registration:
            raise records.Refused("root_authorization_refused", member=member)
    # 3. Shape, key transport included; then admissibility.
    _shape(registration, REGISTRATION_SCHEMA_ID, "registration_malformed", schemas)
    records.check_canonicalizable(registration, member="registration")
    # 4. The assignment, when it is used.
    assignment = _use_assignment(snapshot, registration["assignment_id"],
                                 PERMITTED_REGISTRATION, evaluation_time)
    # 5. The principal, against the holder's own binding.
    holder = assignment["holder"]
    binding = next((b for b in bindings if isinstance(b, Mapping)
                    and b.get("binding_id") == holder["binding_ref"]), None)
    if binding is None:
        raise records.Refused("binding_unresolved", member="holder.binding_ref")
    if holder["principal_kind"] == "governed_broker_job":
        raise records.Refused("broker_capability_insufficient", member="holder.principal_kind")
    governed = snapshot["convening"]["required_seats_provenance"]["governed"]
    _check_holder_binding(binding, governed=governed, environment=environment,
                          evaluation_time=evaluation_time, schemas=schemas)
    principal = (environment.get("identity") or {}).get("principal") or {}
    if (principal.get("principal_kind") != holder["principal_kind"]
            or principal.get("principal_ref") != holder["principal_ref"]):
        raise records.Refused("wrong_principal", member="identity.principal")
    # 6. The issued challenge.
    issued = _issued(environment)
    challenge = next((c for c in issued.get("challenges", []) if isinstance(c, Mapping)
                      and c.get("challenge_id") == registration["challenge_id"]), None)
    if challenge is None:
        raise records.Refused("challenge_unknown", member="challenge_id")
    check_challenge(challenge, schemas=schemas)
    if challenge["assignment_id"] != registration["assignment_id"]:
        raise records.Refused("challenge_wrong_assignment", member="challenge.assignment_id")
    if registration["challenge_id"] in issued.get("consumed_challenges", []):
        raise records.Refused("challenge_consumed", member="challenge_id")
    if _instant(evaluation_time) >= _instant(challenge["expires_at"]):
        raise records.Refused("challenge_expired", member="challenge.expires_at")
    # 7. The key.
    public_key = b64url_decode(registration["public_key"])
    fingerprint = fingerprint_of(public_key)
    if registration["key_fingerprint"] != fingerprint:
        raise records.Refused("fingerprint_mismatch", member="key_fingerprint")
    if challenge["key_fingerprint"] != fingerprint:
        raise records.Refused("fingerprint_mismatch", member="challenge.key_fingerprint")
    registered = [k for k in issued.get("registered_keys", []) if isinstance(k, Mapping)]
    if any(k.get("assignment_id") == registration["assignment_id"] for k in registered):
        raise records.Refused("assignment_already_registered", member="assignment_id")
    convening = {a.get("assignment_id") for a in snapshot.get("assignments", [])
                 if isinstance(a, Mapping)}
    if any(k.get("key_fingerprint") == fingerprint and k.get("assignment_id") in convening
           for k in registered):
        raise records.Refused("shared_key", member="key_fingerprint")
    # 8. The context, rebuilt from frozen state and compared member by member.
    presented = registration["context"]
    expected = registration_context(assignment, challenge, fingerprint)
    _compare_context(presented, expected, (
        (PROTOCOL_MEMBERS, "cross_protocol_context"),
        (CONVENING_MEMBERS, "cross_convening_context"),
        (SEAT_MEMBERS, "cross_seat_context"),
        (("key_fingerprint",), "fingerprint_mismatch"),
        (CHALLENGE_MEMBERS, "challenge_wrong_assignment"),
    ))
    # 9. The proof, over the presented bytes, which by now equal the expected.
    message = signed_bytes(presented)
    if not ed25519.verify(public_key, message, b64url_decode(registration["proof"])):
        raise records.Refused("proof_invalid", member="proof")
    return {"key_fingerprint": fingerprint, "signed_bytes": b64url(message)}


# --------------------------------------------------------------------------
# The return (E8).
# --------------------------------------------------------------------------

def _return_shape(seat_return: Any, schemas: records.SchemaSet) -> None:
    """E8 step 2: the shape with key transport, then admissibility, then the
    payload's size in canonical bytes."""
    _shape(seat_return, RETURN_SCHEMA_ID, "return_malformed", schemas)
    records.check_canonicalizable(seat_return, member="return")
    if len(canonical.serialize(seat_return["payload"]).encode("utf-8")) > PAYLOAD_LIMIT_BYTES:
        raise records.Refused("return_malformed", member="payload")


def _return_digest_holds(seat_return: Mapping[str, Any]) -> None:
    """E8 step 6."""
    value = seat_return["return_digest"]["value"]
    if value != canonical.digest(seat_return["payload"]):
        raise records.Refused("return_digest_mismatch", member="return_digest")
    if seat_return["context"]["return_digest"] != value:
        raise records.Refused("return_digest_mismatch", member="context.return_digest")


def check_return(seat_return: Any, *, snapshot: Mapping[str, Any],
                 environment: Mapping[str, Any], evaluation_time: str,
                 selected_protocol: str | None,
                 schemas: records.SchemaSet | None = None,
                 registry: classification.Registry | None = None) -> dict[str, str]:
    """The return boundary, in the E8 order. Returns `{key_fingerprint,
    signed_bytes}`; raises `records.Refused` on the first failing check, or
    `Routed`."""
    schemas = schemas if schemas is not None else _default_schemas()
    registry = registry if registry is not None else _default_registry()

    # 1. Classification and selection.
    _classify(seat_return, selected_protocol, registry, environment.get("registry_status"))
    # 2. Shape, admissibility, size.
    _return_shape(seat_return, schemas)
    # 3. The assignment, when it is used.
    assignment = _use_assignment(snapshot, seat_return["assignment_id"], PERMITTED_RETURN,
                                 evaluation_time)
    # 4. The registered key.
    issued = _issued(environment)
    registered = next((k for k in issued.get("registered_keys", []) if isinstance(k, Mapping)
                       and k.get("assignment_id") == seat_return["assignment_id"]), None)
    if registered is None:
        raise records.Refused("return_unregistered", member="assignment_id")
    if registered.get("key_fingerprint") != seat_return["key_fingerprint"]:
        raise records.Refused("return_key_mismatch", member="key_fingerprint")
    # 5. The context, rebuilt from frozen state and compared member by member.
    presented = seat_return["context"]
    expected = return_context(assignment, registered["key_fingerprint"],
                              seat_return["return_digest"]["value"])
    _compare_context(presented, expected, (
        (PROTOCOL_MEMBERS, "cross_protocol_context"),
        (CONVENING_MEMBERS, "cross_convening_context"),
        (SEAT_MEMBERS, "cross_seat_context"),
        (("key_fingerprint",), "return_key_mismatch"),
    ))
    # 6. The digest.
    _return_digest_holds(seat_return)
    # 7. The signature, with the key registered for the assignment.
    try:
        public_key = b64url_decode(registered.get("public_key"))
        consistent = fingerprint_of(public_key) == registered["key_fingerprint"]
    except ValueError:
        consistent = False
    if not consistent:
        raise InconsistentEnvironment(
            "environment.issued.registered_keys: an entry's public_key is not the key "
            "its key_fingerprint names")
    message = signed_bytes(presented)
    if not ed25519.verify(public_key, message, b64url_decode(seat_return["signature"])):
        raise records.Refused("return_signature_invalid", member="signature")
    # 8. Replay.
    if any(isinstance(r, Mapping) and r.get("assignment_id") == seat_return["assignment_id"]
           for r in issued.get("accepted_returns", [])):
        raise records.Refused("return_replayed", member="assignment_id")
    return {"key_fingerprint": registered["key_fingerprint"], "signed_bytes": b64url(message)}


# --------------------------------------------------------------------------
# Completion (E8): over the frozen identities, never a count.
# --------------------------------------------------------------------------

def check_completion(snapshot: Mapping[str, Any], returns: list[Mapping[str, Any]], *,
                     environment: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """The completion order over the frozen snapshot and the accepted returns.

    `environment` is accepted and never read: completion follows the snapshot,
    so a rule changed after freezing changes nothing (US2 scenario 4)."""
    del environment
    frozen = {a["assignment_id"]: a for a in snapshot["assignments"]}
    for index, seat_return in enumerate(returns):
        if seat_return.get("assignment_id") not in frozen:
            raise records.Refused("return_unlisted", member=f"returns[{index}].assignment_id")
    seen: set[str] = set()
    for index, seat_return in enumerate(returns):
        if seat_return["assignment_id"] in seen:
            raise records.Refused("return_duplicate", member=f"returns[{index}].assignment_id")
        seen.add(seat_return["assignment_id"])
    for index, seat_return in enumerate(returns):
        context = seat_return.get("context") or {}
        if context.get("seat_id") != frozen[seat_return["assignment_id"]]["seat_id"]:
            raise records.Refused("completion_set_mismatch",
                                  member=f"returns[{index}].context.seat_id")
    for assignment_id in frozen:
        if assignment_id not in seen:
            raise records.Refused("return_missing", member="returns")
    return {}


# --------------------------------------------------------------------------
# The offline half, for the validator's `check` (T045, T048).
# --------------------------------------------------------------------------

def check_registration_offline(registration: Mapping[str, Any],
                               schemas: records.SchemaSet | None = None) -> list[str]:
    """Every E7 rule a lone registration can be held to, in the E7 order, after
    classification: root authorization; the shape; the fingerprint; the context
    members the record itself fixes; and the proof, which a registration can be
    checked for because it carries its own public key. Returns the notes of
    what was checked; raises `records.Refused`."""
    schemas = schemas if schemas is not None else _default_schemas()
    for member in ROOT_AUTHORIZATION_MEMBERS:
        if member in registration:
            raise records.Refused("root_authorization_refused", member=member)
    _shape(registration, REGISTRATION_SCHEMA_ID, "registration_malformed", schemas)
    records.check_canonicalizable(registration, member="registration")
    public_key = b64url_decode(registration["public_key"])
    fingerprint = fingerprint_of(public_key)
    if registration["key_fingerprint"] != fingerprint:
        raise records.Refused("fingerprint_mismatch", member="key_fingerprint")
    presented = registration["context"]
    _compare_context(presented, {
        "signing_context": REGISTRATION_CONTEXT, "protocol": REPLACEMENT,
        "assignment_id": registration["assignment_id"], "key_fingerprint": fingerprint,
        "challenge_id": registration["challenge_id"],
    }, (
        (PROTOCOL_MEMBERS, "cross_protocol_context"),
        (("assignment_id",), "cross_seat_context"),
        (("key_fingerprint",), "fingerprint_mismatch"),
        (("challenge_id",), "challenge_wrong_assignment"),
    ))
    if not ed25519.verify(public_key, signed_bytes(presented),
                          b64url_decode(registration["proof"])):
        raise records.Refused("proof_invalid", member="proof")
    return ["registration shape, fingerprint and context members valid; "
            "proof verified over the presented context"]


def check_return_offline(seat_return: Mapping[str, Any],
                         schemas: records.SchemaSet | None = None) -> list[str]:
    """Every E8 rule a lone return can be held to, after classification: the
    shape, admissibility and size; the context members the record itself fixes;
    and the digest, recomputed over the payload. Its signature needs the key
    registered for its assignment, which the return does not carry."""
    schemas = schemas if schemas is not None else _default_schemas()
    _return_shape(seat_return, schemas)
    presented = seat_return["context"]
    _compare_context(presented, {
        "signing_context": RETURN_CONTEXT, "protocol": REPLACEMENT,
        "assignment_id": seat_return["assignment_id"],
        "key_fingerprint": seat_return["key_fingerprint"],
    }, (
        (PROTOCOL_MEMBERS, "cross_protocol_context"),
        (("assignment_id",), "cross_seat_context"),
        (("key_fingerprint",), "return_key_mismatch"),
    ))
    _return_digest_holds(seat_return)
    return ["return shape and context members valid; return digest recomputed over the payload"]


def check_challenge_offline(challenge: Mapping[str, Any],
                            schemas: records.SchemaSet | None = None) -> list[str]:
    check_challenge(challenge, schemas=schemas)
    return [f"challenge valid against E6 and its {CHALLENGE_LIFETIME_CEILING_SECONDS}-second "
            f"ceiling"]
