"""THE TRANCHE-TWO RULES: links 4, 5, 6 and 10, and the design obligations a gate
cannot see.

This module holds `add-chain-attestation`'s half of the canonical reader.
`scripts/validate-signed-execution-chain.py` owns the corpus, the schema
registry, the scope and links 1-3; it calls `check_tranche_two` once, at the end
of the rule sequence, so the tranche-one walk still reports first and a chain
that fails at link 2 is not also told about link 6.

WHY A MODULE AND NOT MORE OF THE SAME FILE. The tranche-one reader is one file
because it walks one chain of eight checks. Tranche two adds three legs, seven
record kinds, a composed issuance, a committed expectation and a closure horizon,
and folding them in would have doubled a file whose readability is the reason its
refusals are auditable at all. The seam is the SCOPE — a list of (label, record)
pairs — which is the same object both halves already read.

THE REFUSALS ARE NAMED, CLOSED AND PROBED. Every code this module can emit is in
`REFUSAL_CODES` below, the caller unions it into its own closed enumeration, and
the packaged self-test REFUSES a code no negative fixture provokes: a refusal
this reader can emit and nobody has seen work is a refusal on paper.

WHAT IS REFUSED BY SHAPE IS NOT REFUSED HERE, AND THAT IS THE STRONGER ANSWER.
An unclassed attested fact, a runner attestation with no recorded signing
request, a setup attestation committing to no expected set, a closure consuming
no review, an expectation carried outside the signed bytes, an authority record
under a tier-2 identity: every one of them is UNREPRESENTABLE in the shipped
schemas, so the corpus probes them as schema findings with the shape's own
message pinned. This module carries no code for them, because a rule enforced
twice is a rule that can disagree with itself.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from scripts.signed_execution_chain import canonical
from scripts.signed_execution_chain import ed25519

# --------------------------------------------------------------------------
# kinds
# --------------------------------------------------------------------------

SETUP = "xfactory_signed_execution_chain_setup_attestation"
EXTENSION = "xfactory_signed_execution_chain_commitment_extension"
BINDING = "xfactory_signed_execution_chain_chain_binding"
ATTESTATION = "xfactory_signed_execution_chain_runner_attestation"
DECISION = "xfactory_signed_execution_chain_pr_open_decision"
CLOSURE = "xfactory_signed_execution_chain_closure_record"
REMEDIATION = "xfactory_signed_execution_chain_remediation_declaration"

INCEPTION = "xfactory_signed_execution_chain_inception"
DECLARATION = "xfactory_signed_execution_chain_conformance_declaration"
LEAF = "xfactory_signed_execution_chain_log_leaf"

# The CONSUMED `add-trust-anchor` vocabulary. Consumed and never redefined: this
# capability declares no certificate, issuance or anchor shape of its own, and
# reads these three exactly as that change ships them.
CERTIFICATE = "xfactory_certificate_record"
ISSUANCE = "xfactory_certificate_issuance_evidence"
ANCHOR = "xfactory_trust_anchor"

# The signed block of each kind, and the digest SUBJECT that block is hashed
# under. A record's kind never determines its PLACE in the chain — its position
# in the log does — but it does determine WHAT its signature covers, and a reader
# that guessed either would produce chains no other reader could verify.
SIGNED_BLOCK = {
    SETUP: ("signed_setup", "setup_attestation"),
    EXTENSION: ("signed_extension", "commitment_extension"),
    BINDING: ("signed_binding", "signed_chain_binding"),
    ATTESTATION: ("signed_attestation", "runner_attestation"),
    DECISION: ("signed_decision", "pr_open_decision"),
    CLOSURE: ("signed_closure", "closure_record"),
}
SIGNATURE_MEMBER = {
    SETUP: "setup_signature",
    EXTENSION: "extension_signature",
    BINDING: "binding_signature",
    ATTESTATION: "attestation_signature",
    DECISION: "decision_signature",
    CLOSURE: "closure_signature",
}

# The two closed enumerations, one per subject scope. They are held HERE as the
# sets a binding's own `authorized_record_kinds` must EQUAL, so a binding cannot
# widen an identity by writing a longer list — and no authority record is a member
# of either, at either scope, ever.
SCOPE_ENUMERATION = {
    "per_task": {ATTESTATION},
    "chain_scoped": {DECISION, CLOSURE},
}

# Tranche two's nine obligations, in the delta's order, continuing tranche one's
# SEC-R1..SEC-R9.
OBLIGATIONS = ["SEC-R10", "SEC-R11", "SEC-R12", "SEC-R13", "SEC-R14", "SEC-R15",
               "SEC-R16", "SEC-R17", "SEC-R18"]

# SEC-R18 is the executing layer, and it is UNMET rather than partially met until
# a running layer REFUSES a step whose inbound chain does not verify. SEC-R16 is
# closure, whose residuals — per-seat signatures outside this tranche's gate scope,
# revocation-at-exercise a file-based register cannot serve, and the lineage block
# the shape must leave optional so the release stays additive — are declared rather
# than claimed. Neither may be recorded `satisfied` at this tranche.
STRUCTURAL_RESIDUALS = {"SEC-R16", "SEC-R18"}

REFUSAL_CODES = frozenset({
    # --- requirement 1: the setup attestation and the controller certificate ---
    "controller_anchor_not_held",
    "custody_ceiling_exceeded",
    "issuance_provenance_asserted_undeclared",
    "revocation_standing_unchecked",
    "certificate_revoked_at_signing",
    "certificate_revoked_after_signing",
    "commitment_extension_after_dispatch",
    "extension_minted_on_request_arrival",
    "attestation_for_uncommitted_task",
    "extension_signed_away_from_controller",
    # --- requirement 2: the runner attestation and the tier-2 identity ---
    "attestation_signed_away_from_controller",
    "signing_request_unattributable",
    "requester_identity_self_reported",
    "platform_attribution_shortfall_undeclared",
    "platform_attribution_shortfall_disqualifies",
    "attestation_identity_as_actor",
    "persona_proposed_for_workload",
    "per_task_identity_reused",
    "forged_attestation_identity",
    "chain_binding_names_another_chain",
    "record_kind_outside_closed_enumeration",
    "tier2_identity_expired_at_signing",
    "certificate_fingerprint_absent",
    "signing_key_fingerprint_mismatch",
    "record_signature_invalid",
    "subject_scope_mismatch",
    # --- requirement 3: corroboration and the per-fact evidence class ---
    "payload_disagrees_with_setup_attestation",
    "evidence_class_unsupported",
    "runner_claimed_fact_read_as_attested",
    "signing_subject_not_provisioned",
    # --- requirement 4: tier-2 custody, in every configuration ---
    "tier2_key_in_worker",
    "tier2_key_reachable_from_runner",
    "controller_colocated_with_runner",
    "ephemeral_lifetime_offered_as_non_secret",
    "reusable_signing_delegation",
    # --- requirement 5: the pull-request open as a signed decision ---
    "orphan_pull_request",
    "open_decision_names_another_chain",
    "open_decision_enumeration_incomplete",
    "open_decision_pull_request_mismatch",
    "open_decision_offered_as_permission",
    # --- requirement 6: the hash link and the extended walk ---
    "predecessor_digest_break",
    "digest_subject_unnamed",
    "attestation_leaf_deferred_past_successor",
    "enumerated_record_unproven",
    "attestation_outside_committed_expectation",
    "dispatched_leaf_never_written",
    "gate_scope_understated",
    "gate_walk_incomplete",
    "links_1_3_only_after_tranche_two",
    # --- requirement 7: closure ---
    "closure_outcome_unestablished",
    "closure_result_failed",
    "closure_result_unsigned",
    "tested_revision_mismatch",
    "governed_test_identity_mismatch",
    "closure_declared_shortfall_offered",
    "closure_proposal_binding_mismatch",
    "review_record_authority_unproven",
    "review_authority_revoked_at_exercise",
    "review_authority_standing_stale",
    "review_record_replayed",
    "amendment_lineage_absent",
    "amendment_lineage_unsupported",
    "merged_and_never_closed",
    "release_over_unclosed_chain",
    # --- requirement 8: the remediation exemption ---
    "remediation_subject_not_declared",
    "remediation_exemption_inherited",
    "remediation_skips_gate",
    "remediation_own_closure_failed",
    # --- requirement 9: the executing layer's precondition ---
    "step_executed_without_verified_chain",
    "seventh_permission_boolean_proposed",
    "worker_given_key_material_to_verify",
})

# The three legs the extended walk adds, at their own positions after tranche
# one's eight. A `links_1_6` verdict carries all eleven; a `links_1_3` verdict
# carries the first eight, and still does.
EXTENDED_CHECK_NAMES = (
    "setup_attestation_established_and_committed",
    "runner_attestations_equal_the_committed_expectation",
    "open_decision_binds_chain_and_pull_request",
)

# What a certificate's declared custody EVIDENCES, read off the ratified, CLOSED
# registry rather than restated: `contracts/trust-anchor/`
# `trust-anchor-chain-custody.registry.yaml`. This module holds only the AXIS
# NAMES it compares against; the members and their `evidences` come from the
# registry file at run time, so the two sets cannot drift into two custody models.
HOLDER_ATTRIBUTED = "named_holder"
HOST_ATTRIBUTED = "using_host"


# --------------------------------------------------------------------------
# small helpers, kept local so this module reads on its own
# --------------------------------------------------------------------------

def get(doc: Any, *path: str) -> Any:
    node = doc
    for key in path:
        if not isinstance(node, dict):
            return None
        node = node.get(key)
    return node


def digest_value(node: Any) -> Any:
    return node.get("value") if isinstance(node, dict) else None


def digest_subject(node: Any) -> Any:
    return node.get("subject") if isinstance(node, dict) else None


def fingerprint(public_key: Any) -> str | None:
    """The supplied key's fingerprint UNDER THE ONE CONSTRUCTION IN FORCE.

    Not a second construction and not a second encoding: the key is a value, and
    `xfc-jcs-sha256-1` is what this capability computes every digest with,
    including the ones a later tranche adds."""
    if not isinstance(public_key, str):
        return None
    try:
        return canonical.digest(public_key)
    except canonical.ConstructionError:
        return None


def _iso(value: Any) -> str | None:
    return value if isinstance(value, str) else None


# --------------------------------------------------------------------------
# the tranche-two view of a scope
# --------------------------------------------------------------------------

@dataclass
class ChainTwo:
    """Everything in scope that claims one chain identity, at tranche two."""
    chain_id: str
    setups: list[tuple[str, dict]] = field(default_factory=list)
    extensions: list[tuple[str, dict]] = field(default_factory=list)
    bindings: list[tuple[str, dict]] = field(default_factory=list)
    attestations: list[tuple[str, dict]] = field(default_factory=list)
    decisions: list[tuple[str, dict]] = field(default_factory=list)
    closures: list[tuple[str, dict]] = field(default_factory=list)
    remediations: list[tuple[str, dict]] = field(default_factory=list)

    def signed_records(self) -> list[tuple[str, dict]]:
        return (self.setups + self.extensions + self.bindings + self.attestations
                + self.decisions + self.closures)

    def carries_tranche_two(self) -> bool:
        return bool(self.signed_records())


@dataclass
class View:
    records: list[tuple[str, dict]]
    chains: dict[str, ChainTwo] = field(default_factory=dict)
    inceptions: dict[str, dict] = field(default_factory=dict)
    leaves: list[tuple[str, dict]] = field(default_factory=list)
    declarations: list[tuple[str, dict]] = field(default_factory=list)
    certificates: dict[str, dict] = field(default_factory=dict)
    issuances: dict[str, dict] = field(default_factory=dict)
    anchors: dict[str, dict] = field(default_factory=dict)
    bindings_by_id: dict[str, tuple[str, dict]] = field(default_factory=dict)
    custody_models: dict[str, dict] = field(default_factory=dict)

    def chain(self, chain_id: str) -> ChainTwo:
        return self.chains.setdefault(chain_id, ChainTwo(chain_id))


LIST_FOR_KIND = {
    SETUP: "setups",
    EXTENSION: "extensions",
    BINDING: "bindings",
    ATTESTATION: "attestations",
    DECISION: "decisions",
    CLOSURE: "closures",
    REMEDIATION: "remediations",
}


def build_view(records: Iterable[tuple[str, dict]],
               custody_models: dict[str, dict] | None = None) -> View:
    view = View(records=list(records), custody_models=custody_models or {})
    for label, doc in view.records:
        if not isinstance(doc, dict):
            continue
        kind = doc.get("kind")
        if kind in LIST_FOR_KIND:
            chain_id = doc.get("chain_ref")
            if isinstance(chain_id, str):
                getattr(view.chain(chain_id), LIST_FOR_KIND[kind]).append((label, doc))
            if kind == BINDING and isinstance(doc.get("binding_id"), str):
                view.bindings_by_id[doc["binding_id"]] = (label, doc)
        elif kind == INCEPTION:
            chain_id = digest_value(doc.get("chain_identity"))
            if isinstance(chain_id, str):
                view.inceptions[chain_id] = doc
        elif kind == LEAF:
            view.leaves.append((label, doc))
        elif kind == DECLARATION:
            view.declarations.append((label, doc))
        elif kind == CERTIFICATE and isinstance(doc.get("certificate_id"), str):
            view.certificates[doc["certificate_id"]] = doc
        elif kind == ISSUANCE and isinstance(doc.get("issuance_evidence_id"), str):
            view.issuances[doc["issuance_evidence_id"]] = doc
        elif kind == ANCHOR and isinstance(doc.get("anchor_id"), str):
            view.anchors[doc["anchor_id"]] = doc
    return view


# --------------------------------------------------------------------------
# rule: every signature resolves, compares, then verifies
# --------------------------------------------------------------------------

def check_signatures(f, view: View) -> None:
    """RESOLVE, COMPARE, THEN VERIFY — FOR EVERY CERTIFICATE IN THE CONSUMED SET.

    The canonical `certificate-record` carries an OPTIONAL
    `subject.public_key_fingerprint` and NO PUBLIC KEY AT ALL, so "the signature
    verifies under the certified key" is unrunnable from the consumed records as
    they stand. The signed record SUPPLIES the key; this reader computes its
    fingerprint under the one construction in force, REQUIRES EQUALITY with the
    certificate's, and only then verifies. A MISMATCH IS THE FORGED-IDENTITY
    REFUSAL — it is precisely a key that is not the certified one — and so is an
    ABSENT FINGERPRINT, the same condition reached by omission.

    THE RULE IS OVER THE SET AND NOT PER TIER. Link 4 and the commitment
    extensions are signed under the CONTROLLER certificate; a per-tier clause left
    both forgeable by exactly the supplied-key trick it had closed one tier over.
    """
    for chain in view.chains.values():
        for label, doc in chain.signed_records():
            kind = doc.get("kind")
            block_name, subject = SIGNED_BLOCK[kind]
            block = doc.get(block_name)
            signature = doc.get(SIGNATURE_MEMBER[kind])
            if not isinstance(block, dict) or not isinstance(signature, dict):
                continue

            supplied = signature.get("public_key")
            cert_ref = signature.get("certificate_ref")
            cert = view.certificates.get(cert_ref) if isinstance(cert_ref, str) else None
            if cert is None:
                f.error("forged_attestation_identity",
                        f"{label}: the signature names certificate {cert_ref!r} and "
                        f"no certificate record for it is in scope. A signature "
                        f"under an identity whose issuance cannot be resolved is a "
                        f"FORGED IDENTITY — refused with the fraud-signal force of a "
                        f"broken link, never as an unrecognised key")
                continue

            declared = get(cert, "subject", "public_key_fingerprint")
            if not isinstance(declared, str):
                f.error("certificate_fingerprint_absent",
                        f"{label}: certificate {cert_ref!r} carries no "
                        f"`subject.public_key_fingerprint`. The field is OPTIONAL in "
                        f"the canonical shape and REQUIRED here — a consumer may "
                        f"require what the canonical shape leaves open — because a "
                        f"certificate that cannot be tied to any key certifies "
                        f"nothing a signature can be verified against")
                continue

            computed = fingerprint(supplied)
            if computed is None or computed.lower() != declared.lower():
                f.error("signing_key_fingerprint_mismatch",
                        f"{label}: the supplied public key's fingerprint "
                        f"{computed} does not EQUAL certificate {cert_ref}'s "
                        f"{declared}. A key that is not the certified key is exactly "
                        f"what the FORGED-IDENTITY refusal names, and the signature's "
                        f"verifying under the supplied key is never accepted — it is "
                        f"the binding to the certificate that was in question, not "
                        f"the arithmetic")
                continue

            _verify_one(f, label, block, subject, signature, supplied)
            _check_validity(f, label, cert, cert_ref, doc, kind)


def _verify_one(f, label: str, block: dict, subject: str, signature: dict,
                supplied: str) -> None:
    if signature.get("algorithm") != "ed25519":
        f.warn("algorithm-unevaluable",
               f"{label}: {signature.get('algorithm')!r} is declared and not "
               f"verified by this reader; an unevaluable signature is reported "
               f"rather than accepted")
        return
    try:
        message = canonical.serialize(block).encode("utf-8")
    except canonical.ConstructionError as exc:
        f.error("digest_construction_mismatch",
                f"{label}: the {subject} block cannot be serialized under "
                f"{canonical.CONSTRUCTION}: {exc}")
        return
    try:
        key = ed25519.public_key_from_multibase(supplied)
    except (ed25519.KeyRecoveryError, ValueError) as exc:
        f.error("record_signature_invalid",
                f"{label}: the supplied public key could not be decoded: {exc}")
        return
    raw = signature.get("signature")
    try:
        import base64
        blob = base64.urlsafe_b64decode(raw + "==") if isinstance(raw, str) else b""
    except Exception:  # noqa: BLE001
        blob = b""
    if len(blob) != 64 or not ed25519.verify(key, message, blob):
        f.error("record_signature_invalid",
                f"{label}: the signature over `{subject}` does not verify under the "
                f"key the record supplies. A signature that does not verify is not "
                f"a record with a detail wrong; it is a record nobody signed")


def _check_validity(f, label: str, cert: dict, cert_ref: str, doc: dict,
                    kind: str) -> None:
    """BOUNDS THAT ARE MERELY PRESENT ARE NOT BOUNDS THAT ARE MET, and revocation
    is checked AT USE rather than trusted from issuance."""
    signed_at = _iso(doc.get("attested_at") or doc.get("written_at")
                     or doc.get("issued_at") or doc.get("decided_at")
                     or doc.get("closed_at"))
    not_before = _iso(get(cert, "validity", "not_before"))
    not_after = _iso(get(cert, "validity", "not_after"))
    if signed_at and not_after and signed_at > not_after:
        f.error("tier2_identity_expired_at_signing",
                f"{label}: the signing moment {signed_at} is outside certificate "
                f"{cert_ref}'s validity, which ended {not_after}. An ephemeral "
                f"identity is one whose bounds say so, and bounds that are merely "
                f"PRESENT are not bounds that are MET")
    if signed_at and not_before and signed_at < not_before:
        f.error("tier2_identity_expired_at_signing",
                f"{label}: the signing moment {signed_at} precedes certificate "
                f"{cert_ref}'s `not_before` {not_before}")
    if cert.get("state") == "revoked":
        revoked_at = _iso(get(cert, "trust_evaluation", "evaluated_at"))
        if signed_at and revoked_at and revoked_at > signed_at:
            f.error("certificate_revoked_after_signing",
                    f"{label}: certificate {cert_ref} was revoked at {revoked_at}, "
                    f"AFTER this record was signed at {signed_at}. The act the gate "
                    f"already permitted is not retroactively unmade; EVERYTHING THE "
                    f"CHAIN HAS NOT YET BEEN PERMITTED FOR is refused from that "
                    f"point, and the two cases are recorded as two outcomes")
        else:
            f.error("certificate_revoked_at_signing",
                    f"{label}: certificate {cert_ref} records a REVOKED standing at "
                    f"signing, so no admissible record was produced at all. The "
                    f"signature's cryptographic validity is never accepted in place "
                    f"of standing, because revocation does not invalidate a "
                    f"signature")


# --------------------------------------------------------------------------
# rule: the composed tier-2 issuance
# --------------------------------------------------------------------------

def check_issuance(f, view: View) -> None:
    """EVERY VERIFICATION OF A TIER-2 SIGNATURE VERIFIES THE COMPOSED ISSUANCE
    FIRST, AND THE FORGED-IDENTITY REFUSAL FIRES ON ANY ONE MISSING.

    A lane can generate its own keypair, label it with the scope a verifier
    expects, and forge BOTH the record and its request attribution under that same
    untrusted key — and every attribution rule in this capability is satisfied by
    the forgery, because they all check the record against the KEY and never the
    key against an ISSUER. Three records compose: the canonical certificate (the
    fingerprint and the bounds), the canonical issuance evidence (the issuance
    act), and this capability's own SIGNED CHAIN BINDING (the subject scope, the
    closed enumeration and the chain served).
    """
    for chain_id, chain in view.chains.items():
        seen_scoped: list[str] = []
        per_task_use: dict[str, set[str]] = {}
        for label, doc in chain.bindings:
            binding = doc.get("signed_binding") or {}
            if binding.get("chain_ref") != chain_id:
                f.error("chain_binding_names_another_chain",
                        f"{label}: the signed binding names chain "
                        f"{binding.get('chain_ref')} while the record is filed under "
                        f"{chain_id}. An identity issued for one chain is not an "
                        f"identity for the next one")
            scope = binding.get("subject_scope")
            kinds = set(binding.get("authorized_record_kinds") or [])
            expected = SCOPE_ENUMERATION.get(scope, set())
            if expected and kinds != expected:
                f.error("record_kind_outside_closed_enumeration",
                        f"{label}: a {scope!r} binding authorizes {sorted(kinds)} "
                        f"where its scope fixes {sorted(expected)}. The enumeration "
                        f"is CLOSED, so a binding cannot widen an identity by "
                        f"writing a longer list, and an authority record is not a "
                        f"member of either enumeration at either scope, ever")
            if scope == "per_task" and not binding.get("task_ref"):
                f.error("subject_scope_mismatch",
                        f"{label}: a per-task binding names no task, so it is valid "
                        f"for one task nobody can identify")
            if scope == "chain_scoped":
                if binding.get("task_ref"):
                    f.error("subject_scope_mismatch",
                            f"{label}: a chain-scoped binding names a task, giving "
                            f"it a subject narrower than the records it is "
                            f"authorized to sign")
                seen_scoped.append(label)
            for ref, code in (("certificate_ref", "certificate"),
                              ("issuance_evidence_ref", "issuance evidence")):
                value = binding.get(ref)
                pool = view.certificates if ref == "certificate_ref" else view.issuances
                if not isinstance(value, str) or value not in pool:
                    f.error("forged_attestation_identity",
                            f"{label}: the binding references {code} {value!r}, "
                            f"which is not in scope. A composition is not composed "
                            f"until every part is there, and an identity MISSING ANY "
                            f"ONE of the three records is refused at issuance")
        if len(seen_scoped) > 1:
            f.error("subject_scope_mismatch",
                    f"chain {chain_id}: {len(seen_scoped)} chain-scoped tier-2 "
                    f"identities are bound to one chain ({', '.join(seen_scoped)}); "
                    f"the controller issues EXACTLY ONE per chain identity")

        for label, doc in (chain.attestations + chain.decisions + chain.closures):
            kind = doc.get("kind")
            block_name, _ = SIGNED_BLOCK[kind]
            identity = get(doc, block_name, "identity") or {}
            binding_ref = identity.get("binding_ref")
            entry = view.bindings_by_id.get(binding_ref) if isinstance(binding_ref, str) else None
            if entry is None:
                f.error("forged_attestation_identity",
                        f"{label}: the record names tier-2 binding {binding_ref!r} "
                        f"and no SIGNED CHAIN BINDING for it is in scope. Its "
                        f"internally consistent attribution is not accepted, because "
                        f"an attribution verified against the forger's own key "
                        f"establishes nothing")
                continue
            binding = entry[1].get("signed_binding") or {}
            declared_scope = identity.get("subject_scope")
            if binding.get("subject_scope") != declared_scope:
                f.error("subject_scope_mismatch",
                        f"{label}: the record declares subject scope "
                        f"{declared_scope!r} while its binding was issued at "
                        f"{binding.get('subject_scope')!r}")
            if kind not in set(binding.get("authorized_record_kinds") or []):
                f.error("record_kind_outside_closed_enumeration",
                        f"{label}: {kind} is not in the closed enumeration this "
                        f"identity's OWN SIGNED CHAIN BINDING carries "
                        f"({sorted(binding.get('authorized_record_kinds') or [])}). "
                        f"Being genuinely controller-issued is not accepted, since "
                        f"issuance bounds what an identity may SIGN and not merely "
                        f"that it exists")
            if binding.get("chain_ref") != chain_id:
                f.error("chain_binding_names_another_chain",
                        f"{label}: the signing identity's binding serves chain "
                        f"{binding.get('chain_ref')}, not this one")
            if declared_scope == "per_task":
                task = get(doc, block_name, "task_ref")
                if isinstance(task, str) and isinstance(binding_ref, str):
                    per_task_use.setdefault(binding_ref, set()).add(task)
        for binding_ref, tasks in per_task_use.items():
            if len(tasks) > 1:
                f.error("per_task_identity_reused",
                        f"chain {chain_id}: per-task identity {binding_ref} signed "
                        f"attestations for {sorted(tasks)}. A per-task identity is "
                        f"valid for ONE task, and reuse is never accepted on the "
                        f"strength of the identity still being unexpired")


# --------------------------------------------------------------------------
# rule: the setup attestation, the anchor, and the custody ceiling
# --------------------------------------------------------------------------

def check_setup(f, view: View) -> None:
    for chain_id, chain in view.chains.items():
        if not chain.carries_tranche_two():
            continue
        if not chain.setups:
            f.error("missing_link",
                    f"chain {chain_id}: tranche-two records are presented for a "
                    f"chain carrying NO SETUP ATTESTATION. They have no issuer to "
                    f"chain to and nothing to be corroborated against, and the "
                    f"absence is reported as a BROKEN LINK rather than as a "
                    f"controller that had nothing to say")
            continue
        for label, doc in chain.setups:
            block = doc.get("signed_setup") or {}
            if block.get("chain_ref") != chain_id:
                f.error("continuity_broken",
                        f"{label}: the signed block names chain "
                        f"{block.get('chain_ref')} and the envelope names "
                        f"{chain_id}; the mismatch is never resolved in favour of "
                        f"either copy")
            cert_block = block.get("controller_certificate") or {}
            anchor_ref = cert_block.get("anchor_ref")
            if isinstance(anchor_ref, str) and anchor_ref not in view.anchors:
                f.error("controller_anchor_not_held",
                        f"{label}: the controller certificate's chain terminates in "
                        f"anchor {anchor_ref!r}, which the evaluating gate does not "
                        f"hold. The certificate's well-formedness is not accepted in "
                        f"place of an anchor")
            standing = cert_block.get("revocation_standing_at_signing")
            if standing == "revoked":
                f.error("certificate_revoked_at_signing",
                        f"{label}: the setup attestation records a REVOKED "
                        f"controller certificate AT SIGNING, so the attestation is "
                        f"refused outright and nothing downstream of it is permitted")
            elif standing == "unchecked":
                f.error("revocation_standing_unchecked",
                        f"{label}: the controller certificate's standing was not "
                        f"checked at signing. `add-trust-anchor` requires revocation "
                        f"to be CHECKED AT USE rather than trusted from issuance, and "
                        f"an unchecked standing is not a standing")
            if cert_block.get("issuance_evidence_ref") is None:
                f.error("issuance_provenance_asserted_undeclared",
                        f"{label}: the setup attestation records no issuance "
                        f"evidence for the controller certificate and declares no "
                        f"shortfall. Asserting unestablished provenance is a "
                        f"validation failure, while the DECLARED gap leaves the "
                        f"realization conformant")
            _check_custody_ceiling(f, label, view, cert_block, block)
            _check_facts(f, label, block.get("provisioned_environment") or {})


def _check_custody_ceiling(f, label: str, view: View, cert_block: dict,
                           block: dict) -> None:
    """THE SIGNING CERTIFICATE'S CUSTODY CEILING BOUNDS WHAT ANY FACT UNDER IT CAN
    BE READ AS EVIDENCING, and no evidence class raises a fact above it.

    The two axes are DIFFERENT and neither may be substituted for the other: the
    ratified registry classes WHOSE ACT a signature evidences; this capability's
    evidence classes class WHERE A FACT INSIDE THE SIGNED PAYLOAD CAME FROM. They
    are read TOGETHER AND IN THAT ORDER.
    """
    model = cert_block.get("declared_custody_model")
    entry = view.custody_models.get(model) if isinstance(model, str) else None
    if entry is None:
        return
    evidences = entry.get("evidences")
    if evidences != HOST_ATTRIBUTED:
        return
    for group in (block.get("provisioned_environment") or {}).values():
        for fact in group if isinstance(group, list) else []:
            if isinstance(fact, dict) and fact.get("evidence_class") == "independently_observed":
                f.error("custody_ceiling_exceeded",
                        f"{label}: a fact is classed `independently_observed` under "
                        f"a certificate whose declared custody {model!r} evidences "
                        f"only `{HOST_ATTRIBUTED}`. The custody ceiling BOUNDS what "
                        f"any fact under it evidences, and what the signature "
                        f"evidences is derived from the DECLARED CUSTODY and never "
                        f"from the certificate's contents")
                return


def _check_facts(f, label: str, environment: dict) -> None:
    for where, group in environment.items():
        for fact in group if isinstance(group, list) else []:
            if not isinstance(fact, dict):
                continue
            if fact.get("evidence_class") == "independently_observed" \
                    and not fact.get("observed_by"):
                f.error("evidence_class_unsupported",
                        f"{label}: {where}/{fact.get('fact')!r} is classed "
                        f"`independently_observed` and names no observer. The "
                        f"property that earns the class is INDEPENDENT OBSERVATION — "
                        f"by a party that is neither the runner making the claim nor "
                        f"the controller signing it — and a class asserted without "
                        f"the party that supplies it is a word")


# --------------------------------------------------------------------------
# rule: the committed expectation
# --------------------------------------------------------------------------

def expected_set(chain: ChainTwo) -> dict[str, str]:
    """LINK 4'S COMMITTED EXPECTATION, AS EXTENDED — THE AUTHORITY.

    An enumeration can only be judged incomplete against an AUTHORITATIVE SET, and
    a gate reading only the artifacts it was handed has none. A set derived from
    the log cannot see a leaf that was NEVER WRITTEN, so a lane that simply never
    writes an unwanted attestation produces an enumeration EQUAL to the derived
    set and the terminal act is permitted. The authority is therefore the
    controller's own commitment, and the log comparison is a SECOND check."""
    tasks: dict[str, str] = {}
    for _, doc in chain.setups:
        for entry in get(doc, "signed_setup", "expected_attestation_set") or []:
            if isinstance(entry, dict) and isinstance(entry.get("task_ref"), str):
                tasks[entry["task_ref"]] = entry.get("dispatched_at") or ""
    for _, doc in chain.extensions:
        for entry in get(doc, "signed_extension", "added_tasks") or []:
            if isinstance(entry, dict) and isinstance(entry.get("task_ref"), str):
                tasks[entry["task_ref"]] = entry.get("dispatched_at") or ""
    return tasks


def check_expectation(f, view: View) -> None:
    for chain_id, chain in view.chains.items():
        if not chain.carries_tranche_two():
            continue
        expected = expected_set(chain)
        setup_ids = {doc.get("attestation_id") for _, doc in chain.setups}

        for label, doc in chain.extensions:
            block = doc.get("signed_extension") or {}
            if block.get("signed_where") != "harness_controller":
                f.error("extension_signed_away_from_controller",
                        f"{label}: the extension records a signature produced at "
                        f"{block.get('signed_where')!r}. A runner is never permitted "
                        f"to enlarge or shrink the expectation its own completeness "
                        f"is measured against")
            if block.get("extends") not in setup_ids:
                f.error("missing_link",
                        f"{label}: the extension extends "
                        f"{block.get('extends')!r}, which is not this chain's setup "
                        f"attestation; an extension naming no link 4 extends nothing")
            written = _iso(doc.get("written_at"))
            for entry in block.get("added_tasks") or []:
                dispatched = _iso(entry.get("dispatched_at")) if isinstance(entry, dict) else None
                if written and dispatched and written > dispatched:
                    f.error("commitment_extension_after_dispatch",
                            f"{label}: the extension was written {written}, AFTER "
                            f"task {entry.get('task_ref')} was dispatched "
                            f"{dispatched}. An expectation recorded after the "
                            f"controller has acted is a DESCRIPTION and not an "
                            f"expectation, and the extension's correct content and "
                            f"valid signature are not accepted in place of its being "
                            f"written at or before dispatch")

        attested: dict[str, str] = {}
        for label, doc in chain.attestations:
            block = doc.get("signed_attestation") or {}
            task = block.get("task_ref")
            if isinstance(task, str):
                attested[task] = label
            if isinstance(task, str) and task not in expected:
                f.error("attestation_for_uncommitted_task",
                        f"{label}: task {task!r} is named neither in link 4 nor in "
                        f"any extension. The attestation's corroborating cleanly "
                        f"against link 4's environment is not accepted in place of "
                        f"the task having been COMMITTED, so extension cannot be "
                        f"skipped by attesting anyway")
            if block.get("signed_where") != "harness_controller":
                f.error("attestation_signed_away_from_controller",
                        f"{label}: the attestation carries a signature produced at "
                        f"{block.get('signed_where')!r}. The refusal names the "
                        f"CUSTODY BREACH rather than the signature's validity, "
                        f"because a valid signature made in the wrong place is not a "
                        f"conforming attestation")

        # THE LOG COMPARISON, IN BOTH DIRECTIONS AND AS A SECOND CHECK.
        for task in sorted(set(expected) - set(attested)):
            if chain.decisions or chain.closures:
                f.error("dispatched_leaf_never_written",
                        f"chain {chain_id}: task {task!r} is in link 4's committed "
                        f"expectation and produced NO link-5 attestation and no "
                        f"leaf. The leaf's never having existed is not accepted as "
                        f"the task's never having been dispatched, because the "
                        f"controller committed to it BEFORE ANY RUNNER EXECUTED")


# --------------------------------------------------------------------------
# rule: the signing requests
# --------------------------------------------------------------------------

REQUEST_SITES = {
    ATTESTATION: ("signed_attestation", "controller_provisioning"),
    DECISION: ("signed_decision", "chain_inception_binding"),
    CLOSURE: ("signed_closure", "chain_inception_binding"),
}


def check_requests(f, view: View) -> None:
    """RECORDING IS NECESSARY AND NOT SUFFICIENT.

    A recorded request establishes that SOMETHING asked; it does not establish
    WHAT. An opportunistic caller that can reach the signing service can submit a
    payload that corroborates against link 4 and satisfy every other refusal, so
    the controller ATTRIBUTES the request and REFUSES one it cannot attribute. The
    task-scoped attribution reaches no record ABOUT A CHAIN, which is why the
    chain-scoped records take their requester from THE CHAIN'S OWN INCEPTION
    RECORD — no authority is minted, the set is READ OFF what the chain carries.
    """
    for chain_id, chain in view.chains.items():
        inception = view.inceptions.get(chain_id)
        bound_actor = get(inception, "signed_ratification", "actor",
                          "subject_reference", "subject") if inception else None
        expected = expected_set(chain)
        for label, doc in (chain.attestations + chain.decisions + chain.closures):
            kind = doc.get("kind")
            block_name, mode = REQUEST_SITES[kind]
            block = doc.get(block_name) or {}
            request = block.get("signing_request") or {}
            attribution = request.get("attribution") or {}
            by = attribution.get("attributed_by")
            requester = attribution.get("requester_ref")
            if by == "runner_asserted":
                f.error("requester_identity_self_reported",
                        f"{label}: the signing request carries a requester identity "
                        f"the runner asserts about ITSELF. The attribution comes "
                        f"from the controller's OWN PROVISIONING, and a "
                        f"self-reported asker is refused on the same ground as a "
                        f"self-reported measurement")
            elif by != mode:
                f.error("signing_request_unattributable",
                        f"{label}: the request is attributed by {by!r} where a "
                        f"{kind.rsplit('_', 2)[-1]!r} record requires {mode!r}")
            elif mode == "controller_provisioning":
                if requester not in expected:
                    f.error("signing_subject_not_provisioned",
                            f"{label}: the request names subject {requester!r}, "
                            f"which appears nowhere in the controller's own setup "
                            f"attestation. BEING ASKED IS NEVER ACCEPTED AS "
                            f"AUTHORITY TO SIGN")
            elif bound_actor is not None and requester != bound_actor:
                f.error("signing_request_unattributable",
                        f"{label}: the chain-scoped request is attributed to "
                        f"{requester!r}, whom the chain's inception record does not "
                        f"bind (it binds {bound_actor!r}). The payload's satisfying "
                        f"every other refusal is never accepted in place of "
                        f"attributing the asker")
            _check_payload_digest(f, label, block, request, kind)


def _check_payload_digest(f, label: str, block: dict, request: dict,
                          kind: str) -> None:
    _, subject = SIGNED_BLOCK[kind]
    carried = {key: value for key, value in block.items() if key != "signing_request"}
    node = request.get("payload_digest")
    if digest_subject(node) != subject:
        f.error("digest_subject_unnamed",
                f"{label}: the request's payload digest names subject "
                f"{digest_subject(node)!r} where the block it covers is a "
                f"{subject}. Readers that agree on HOW to hash can still disagree "
                f"on WHAT was hashed")
        return
    try:
        derived = canonical.digest(carried)
    except canonical.ConstructionError as exc:
        f.error("digest_construction_mismatch", f"{label}: {exc}")
        return
    if derived != digest_value(node):
        f.error("digest_construction_mismatch",
                f"{label}: the request's payload digest is {digest_value(node)} and "
                f"the {subject} block it covers recomputes to {derived}")


# --------------------------------------------------------------------------
# rule: corroboration
# --------------------------------------------------------------------------

def check_corroboration(f, view: View) -> None:
    """BIND BEFORE SIGN. The controller is a SIGNER, never a notary of whatever it
    is handed, and the model, version and harness of link 5 are facts it
    PROVISIONED in link 4."""
    for chain in view.chains.values():
        provisioned: dict[str, dict] = {}
        for _, doc in chain.setups:
            for group in (get(doc, "signed_setup", "provisioned_environment") or {}).values():
                for fact in group if isinstance(group, list) else []:
                    if isinstance(fact, dict) and isinstance(fact.get("fact"), str):
                        provisioned[fact["fact"]] = fact
        for label, doc in chain.attestations:
            for fact in get(doc, "signed_attestation", "attested_facts") or []:
                if not isinstance(fact, dict):
                    continue
                source = provisioned.get(fact.get("fact"))
                if source is None:
                    continue
                if fact.get("value") != source.get("value"):
                    f.error("payload_disagrees_with_setup_attestation",
                            f"{label}: {fact.get('fact')!r} is attested as "
                            f"{fact.get('value')!r} where link 4 records it as "
                            f"{source.get('value')!r} PROVISIONED. The controller "
                            f"REFUSES TO SIGN rather than signing and flagging, "
                            f"because a signed record with a warning beside it still "
                            f"chains")
                if source.get("evidence_class") == "runner_claimed" \
                        and fact.get("evidence_class") != "runner_claimed":
                    f.error("runner_claimed_fact_read_as_attested",
                            f"{label}: {fact.get('fact')!r} is carried as "
                            f"{fact.get('evidence_class')!r} where link 4 classes it "
                            f"`runner_claimed`. The class TRAVELS WITH THE FACT, and "
                            f"the controller's signature over the record is not "
                            f"evidence for a claim the record itself labels "
                            f"unverified")
            _check_facts(f, label,
                         {"attested_facts": get(doc, "signed_attestation",
                                                "attested_facts") or []})


# --------------------------------------------------------------------------
# rule: the hash link, over records that exist
# --------------------------------------------------------------------------

def check_hash_links(f, view: View) -> None:
    """THE PREDECESSOR OF ANY SIGNED RECORD THIS CAPABILITY DEFINES IS THE ACTUAL
    NEAREST PRIOR IN-FORCE SIGNED RECORD OF ITS CHAIN, whatever kind that record
    happens to be.

    A RECORD'S KIND NEVER DETERMINES ITS PLACE; ITS POSITION IN THE LOG DOES. The
    walk is over THE RECORDS THE LOG HOLDS IN THE ORDER IT HOLDS THEM, so a
    commitment extension or a signed chain binding interleaved between the
    numbered links IS WALKED and its successor chains from it. A signed record
    omitted from the walk because its kind is unnumbered is an UNLINKED RECORD,
    and the gate refuses the chain rather than skipping it.
    """
    index_of: dict[str, int] = {}
    for _, leaf in view.leaves:
        payload = leaf.get("payload_ref")
        if isinstance(payload, str) and isinstance(leaf.get("leaf_index"), int):
            index_of[payload] = leaf["leaf_index"]

    for chain_id, chain in view.chains.items():
        ordered: list[tuple[int, str, dict]] = []
        for label, doc in chain.signed_records():
            record_id = _record_id(doc)
            if record_id not in index_of:
                f.error("enumerated_record_unproven",
                        f"{label}: the log holds NO LEAF for {record_id!r}. An act "
                        f"that writes no leaf is refused by every consumer requiring "
                        f"the chain, and the record's own well-formedness is not "
                        f"accepted in its place")
                continue
            ordered.append((index_of[record_id], label, doc))
        ordered.sort()

        for position, (_, label, doc) in enumerate(ordered):
            kind = doc.get("kind")
            block_name, _subject = SIGNED_BLOCK[kind]
            declared = get(doc, block_name, "predecessor")
            if kind == SETUP:
                continue
            if position == 0:
                f.error("predecessor_digest_break",
                        f"{label}: this is the FIRST signed record of chain "
                        f"{chain_id} in log order and it is not the setup "
                        f"attestation; link 4 is the first link with a signer of its "
                        f"own and nothing may precede it")
                continue
            _, prior_label, prior = ordered[position - 1][1], ordered[position - 1][1], ordered[position - 1][2]
            _compare_predecessor(f, label, declared, prior, prior_label)

        _check_leaf_order(f, chain_id, chain, index_of)


def _record_id(doc: dict) -> Any:
    for key in ("attestation_id", "extension_id", "binding_id", "decision_id",
                "closure_id"):
        if isinstance(doc.get(key), str):
            return doc[key]
    return None


def _compare_predecessor(f, label: str, declared: Any, prior: dict,
                         prior_label: str) -> None:
    prior_kind = prior.get("kind")
    prior_block_name, prior_subject = SIGNED_BLOCK[prior_kind]
    prior_block = prior.get(prior_block_name) or {}
    prior_id = _record_id(prior)
    if not isinstance(declared, dict):
        f.error("predecessor_digest_break",
                f"{label}: no predecessor is declared; every signed record from "
                f"link 4 onward commits to the digest of its predecessor")
        return
    if declared.get("record_ref") != prior_id:
        f.error("predecessor_digest_break",
                f"{label}: the declared predecessor is "
                f"{declared.get('record_ref')!r} where the log's actual nearest "
                f"prior in-force signed record is {prior_id!r} ({prior_label}). A "
                f"record chaining from anything other than its actual nearest prior "
                f"is REFUSED as a break, in the illustrative order and in any "
                f"interleaved one")
        return
    node = declared.get("digest")
    if digest_subject(node) != prior_subject:
        f.error("digest_subject_unnamed",
                f"{label}: the predecessor digest names subject "
                f"{digest_subject(node)!r} where {prior_id} is a {prior_subject}")
        return
    try:
        derived = canonical.digest(prior_block)
    except canonical.ConstructionError as exc:
        f.error("digest_construction_mismatch", f"{label}: {exc}")
        return
    if derived != digest_value(node):
        f.error("predecessor_digest_break",
                f"{label}: the predecessor digest is {digest_value(node)} and "
                f"{prior_id}'s {prior_subject} recomputes to {derived}")


def _check_leaf_order(f, chain_id: str, chain: ChainTwo,
                      index_of: dict[str, int]) -> None:
    """EVERY LINK-5 LEAF FOR A CHAIN IDENTITY IS WRITTEN BEFORE THAT CHAIN'S LINK-6
    LEAF, and a link-5 leaf sequenced AFTER its successor's is refused as a DROPPED
    LINK — never accepted as a late-arriving record on an otherwise complete chain.
    A rule that is satisfiable by waiting is not a rule."""
    successors = [index_of[_record_id(doc)] for _, doc in chain.decisions
                  if _record_id(doc) in index_of]
    if not successors:
        return
    first_successor = min(successors)
    for label, doc in chain.attestations:
        position = index_of.get(_record_id(doc))
        if position is not None and position > first_successor:
            f.error("attestation_leaf_deferred_past_successor",
                    f"{label}: this link-5 leaf sits at index {position}, AFTER the "
                    f"chain's link-6 leaf at {first_successor}. It is refused as a "
                    f"DROPPED LINK, and the deferral is caught at the GATE in any "
                    f"case by the committed expectation, which named the task before "
                    f"any runner executed and does not shrink when a leaf is "
                    f"withheld")


# --------------------------------------------------------------------------
# rule: the pull-request open decision
# --------------------------------------------------------------------------

def check_decisions(f, view: View) -> None:
    for chain_id, chain in view.chains.items():
        if not chain.carries_tranche_two():
            continue
        expected = expected_set(chain)
        if chain.attestations and not chain.decisions and not chain.remediations:
            f.error("orphan_pull_request",
                    f"chain {chain_id}: runner attestations are presented and NO "
                    f"link-6 record exists. A pull request EXISTS, so something "
                    f"opened it, so a signed decision is owed — the absence is never "
                    f"read as an unremarkable omission, because an unsigned open is "
                    f"an act with no signer")
        for label, doc in chain.decisions:
            block = doc.get("signed_decision") or {}
            if block.get("chain_ref") != chain_id:
                f.error("open_decision_names_another_chain",
                        f"{label}: the signed open decision names chain "
                        f"{block.get('chain_ref')} and the traveling contract carries "
                        f"{chain_id}; the mismatch is a FRAUD SIGNAL and is never "
                        f"resolved in favour of either copy")
            if block.get("offered_as_permission") is True:
                f.error("open_decision_offered_as_permission",
                        f"{label}: link 6 is offered as evidence that the terminal "
                        f"act is permitted. PROPOSING IS NOT PERMITTING, and the "
                        f"permission remains the gate's verdict and nothing else")
            if block.get("signed_where") != "harness_controller":
                f.error("attestation_signed_away_from_controller",
                        f"{label}: the open decision was signed at "
                        f"{block.get('signed_where')!r}; its correctness is not "
                        f"accepted as a defence of where it was signed")
            enumerated = {entry.get("task_ref") for entry
                          in block.get("committed_attestations") or []
                          if isinstance(entry, dict)}
            missing = sorted(set(expected) - enumerated)
            extra = sorted(enumerated - set(expected))
            if missing:
                f.error("open_decision_enumeration_incomplete",
                        f"{label}: the enumeration omits {missing} from link 4's "
                        f"committed expectation. The gate compares against the "
                        f"COMMITTED EXPECTATION and never against the submission, so "
                        f"an enumeration complete over what was handed in is never "
                        f"accepted as complete, and the omission is reported as a "
                        f"DROPPED LINK rather than as work that produced nothing")
            if extra:
                f.error("attestation_outside_committed_expectation",
                        f"{label}: the enumeration carries {extra}, which no "
                        f"commitment covers. The enumeration must EQUAL the "
                        f"committed expectation — not a subset and not a superset — "
                        f"because work the controller never committed to dispatching "
                        f"is work the chain cannot account for")
            _check_pull_request_binding(f, label, chain, block)


def _check_pull_request_binding(f, label: str, chain: ChainTwo,
                                block: dict) -> None:
    """THE GATE REFUSES UNLESS THE SIGNED PULL-REQUEST IDENTIFIER AND HEAD REVISION
    EQUAL THE ONES ACTUALLY BEING MERGED. Three reuses are refused by that one
    comparison and all three pass without it: a decision REUSED AFTER THE BRANCH
    MOVED, one RETARGETED, and one ATTACHED TO A DIFFERENT PULL REQUEST CARRYING
    THE SAME CHAIN IDENTITY."""
    signed = block.get("pull_request") or {}
    for _, closure in chain.closures:
        execution = get(closure, "signed_closure", "test_execution") or {}
        merged_pr = execution.get("merged_pull_request_ref")
        merge_commit = execution.get("merge_commit")
        if merged_pr is None or merge_commit is None:
            continue
        if signed.get("pull_request_ref") != merged_pr \
                or signed.get("head_revision") != merge_commit:
            f.error("open_decision_pull_request_mismatch",
                    f"{label}: the decision signs pull request "
                    f"{signed.get('pull_request_ref')!r} at head "
                    f"{signed.get('head_revision')!r} while the merge was of "
                    f"{merged_pr!r} at {merge_commit!r}. The decision's being "
                    f"genuine, well-formed and correctly chained is not accepted, "
                    f"since it decided a DIFFERENT ACT than the one the gate is "
                    f"permitting")


# --------------------------------------------------------------------------
# rule: closure
# --------------------------------------------------------------------------

def check_closure(f, view: View) -> None:
    for chain_id, chain in view.chains.items():
        inception = view.inceptions.get(chain_id)
        for label, doc in chain.closures:
            block = doc.get("signed_closure") or {}
            _check_outcome(f, label, block)
            _check_governed_test(f, label, block, inception)
            _check_review(f, label, block, inception)
            shortfall = block.get("declared_outcome_shortfall") or {}
            if shortfall.get("declared") is True:
                f.error("closure_declared_shortfall_offered",
                        f"{label}: a declared shortfall is offered as grounds for "
                        f"closure. A declaration NEVER converts an unmeetable "
                        f"control into a met one, and here it would disqualify the "
                        f"chain from CLOSURE — the only thing closure does — leaving "
                        f"nothing for the declaration to permit. The chain stays "
                        f"MERGED-BUT-UNCLOSED and its downstream refusing")
            if block.get("signed_where") != "harness_controller":
                f.error("attestation_signed_away_from_controller",
                        f"{label}: the closure record was signed at "
                        f"{block.get('signed_where')!r}")
        _check_closure_horizon(f, chain_id, chain, view)


def _check_outcome(f, label: str, block: dict) -> None:
    execution = block.get("test_execution") or {}
    dispatched_by = execution.get("dispatched_by")
    result = execution.get("result")
    if dispatched_by in ("lane_claimed", "runner_claimed"):
        f.error("closure_outcome_unestablished",
                f"{label}: the post-merge outcome is {dispatched_by!r} — an outcome "
                f"the controller neither DISPATCHED nor OBSERVED. The chain does not "
                f"close, the outcome is recorded as UNESTABLISHED rather than as a "
                f"pass, and the controller's willingness to sign the bytes is never "
                f"accepted in place of establishing that the test RAN: a signer is "
                f"not a notary of an outcome it was handed")
    elif result == "failed":
        f.error("closure_result_failed",
                f"{label}: the established, correctly signed result is a FAILURE. "
                f"Closure is REFUSED and the chain is in the LINK-10-FAILED refusing "
                f"state — merged-but-unclosed, refusing everything downstream, firing "
                f"link 9's fraud signal. A FAILURE HONESTLY ESTABLISHED IS THIS "
                f"CONTROL WORKING, and a REMEDIATION CHAIN declaring that failed "
                f"closure as its signed subject is the route out")
    elif result == "unsigned":
        f.error("closure_result_unsigned",
                f"{label}: the governed post-merge test completed and its outcome is "
                f"UNSIGNED. The chain does not close, and the pass is not evidence "
                f"that the act it reports was permitted")
    elif result == "unestablished":
        f.error("closure_outcome_unestablished",
                f"{label}: the outcome is recorded UNESTABLISHED — a DIFFERENT FACT "
                f"from a test that ran and FAILED, kept distinct because a responder "
                f"who conflates them goes looking for a defect in the work when what "
                f"is missing is evidence about the test")
    if execution.get("tested_revision") != execution.get("merge_commit"):
        f.error("tested_revision_mismatch",
                f"{label}: the tested revision {execution.get('tested_revision')!r} "
                f"is not the merge commit {execution.get('merge_commit')!r} the "
                f"chain closed over. A test that passed against OTHER BYTES is "
                f"evidence about other bytes")


def _check_governed_test(f, label: str, block: dict, inception: dict | None) -> None:
    named = get(inception, "signed_ratification", "ratified_subject",
                "governed_test") if inception else None
    if not isinstance(named, dict):
        return
    ran = get(block, "test_execution", "test_identity") or {}
    if ran.get("test_id") != named.get("test_id") or \
            digest_value(ran.get("definition_digest")) != digest_value(named.get("definition_digest")):
        f.error("governed_test_identity_mismatch",
                f"{label}: the dispatched test {ran.get('test_id')!r} is not the "
                f"governed test the RATIFIED SUBJECT names ({named.get('test_id')!r}). "
                f"The execution's being authentic, the revision exact and the result "
                f"a real pass are not accepted, since none of them establishes that "
                f"WHAT WAS PROMISED IS WHAT WAS TESTED")


def _check_review(f, label: str, block: dict, inception: dict | None) -> None:
    """CLOSURE VERIFIES THE LINEAGE, IN THREE LIMBS, AND NEVER AN EQUALITY."""
    review = block.get("consumed_review") or {}
    exercise = review.get("authority_exercise") or {}
    if exercise.get("proof_presented") is not True or exercise.get("proof_verified") is not True:
        f.error("review_record_authority_unproven",
                f"{label}: the consumed review record is not established by a "
                f"VERIFIED review-authority exercise. A digest over a review record "
                f"proves only that the bytes did not change; the test's own passing "
                f"is never accepted as evidence that A COUNCIL PRODUCED WHAT IT READ")
    if exercise.get("standing_at_exercise") == "revoked":
        f.error("review_authority_revoked_at_exercise",
                f"{label}: the review grant behind the consumed record records a "
                f"REVOKED standing at exercise. A valid signature is not current "
                f"authority, and the review record's integrity is not accepted in "
                f"its place")
    if exercise.get("projection_age_within_declared_bound") is False:
        f.error("review_authority_standing_stale",
                f"{label}: the review authority's standing was read from a "
                f"projection OLDER than the intake register's own declared "
                f"revocation staleness bound. The shortfall's being declared does "
                f"not admit the closure — a declaration BOUNDS WHAT MAY BE CLAIMED "
                f"and never supplies the evidence the control asked for")
    if isinstance(exercise.get("object_ref"), str) and \
            exercise["object_ref"] != review.get("review_ref"):
        f.error("review_record_authority_unproven",
                f"{label}: the authority exercise's `object_ref` "
                f"{exercise['object_ref']!r} is not bound to the consumed review "
                f"record {review.get('review_ref')!r}")

    lineage = get(inception, "signed_ratification", "amendment_lineage") if inception else None
    if inception is not None and not isinstance(lineage, dict):
        f.error("amendment_lineage_absent",
                f"{label}: the ratification this chain descends from commits to NO "
                f"amendment lineage, so closure's three limbs read fields that do "
                f"not exist. Carrying the lineage in a later record is not accepted, "
                f"because a lineage the RATIFYING SIGNATURE DOES NOT COVER is "
                f"attachable afterwards")
        return
    if not isinstance(lineage, dict):
        return

    # LIMB 1 — AN IDENTITY COMPARISON, TWICE, AND NEVER A SUBJECT ONE.
    record = lineage.get("amendment_record_ref") or {}
    if digest_value(review.get("review_digest")) != digest_value(lineage.get("review_record_digest")):
        f.error("review_record_replayed",
                f"{label}: the consumed review's own digest does not EQUAL the "
                f"committed REVIEW-RECORD DIGEST. An earlier rejected review of the "
                f"SAME reviewed bytes fails here, because limb 1 compares the "
                f"REVIEW'S IDENTITY and never only the bytes it happened to cover")
    elif record.get("names_review_record") not in (None, review.get("review_ref")):
        f.error("review_record_replayed",
                f"{label}: the amendment record names review "
                f"{record.get('names_review_record')!r} and the closure consumes "
                f"{review.get('review_ref')!r}")
    if digest_value(review.get("reviewed_subject_digest")) != digest_value(lineage.get("reviewed_digest")):
        f.error("review_record_replayed",
                f"{label}: the consumed review names reviewed subject "
                f"{digest_value(review.get('reviewed_subject_digest'))} where this "
                f"ratification's lineage begins at "
                f"{digest_value(lineage.get('reviewed_digest'))}. That foreign "
                f"reviewed digest appears in NO LINEAGE this ratification commits "
                f"to; its differing from the ratified subject is NOT the ground of "
                f"refusal, since under the lineage rule a reviewed digest that "
                f"differs from the ratified subject is the ORDINARY case for an "
                f"accepted-as-amended packet")

    # LIMB 3 — THE RATIFIED SUBJECT IS THE LINEAGE'S ENDPOINT, NOT MERELY ASSERTED.
    if digest_value(record.get("from_digest")) != digest_value(lineage.get("reviewed_digest")) or \
            digest_value(record.get("to_digest")) != digest_value(lineage.get("ratified_subject_digest")):
        f.error("amendment_lineage_unsupported",
                f"{label}: the committed amendment record's trail runs "
                f"{digest_value(record.get('from_digest'))} -> "
                f"{digest_value(record.get('to_digest'))}, which does not connect "
                f"the lineage's own endpoints. A ratification cannot merely ASSERT a "
                f"lineage: the record it commits to must actually connect the "
                f"reviewed digest to the ratified subject")
    ratified = digest_value(get(inception, "signed_ratification", "ratified_subject",
                                "subject_digest"))
    if ratified is not None and digest_value(lineage.get("ratified_subject_digest")) != ratified:
        f.error("amendment_lineage_unsupported",
                f"{label}: the lineage's ratified-subject digest disagrees with the "
                f"ratification's own content digest. Two spellings of one fact are a "
                f"channel for the two to disagree, and this one is checked rather "
                f"than trusted")
    proposal = digest_value(get(block, "consumed_proposal", "subject_digest"))
    if ratified is not None and proposal is not None and proposal != ratified:
        f.error("closure_proposal_binding_mismatch",
                f"{label}: the closure consumes proposal digest {proposal} where "
                f"the ratification's CONTENT DIGEST is {ratified}. The two digests "
                f"tranche one distinguishes are each used for the comparison they "
                f"were defined for rather than collapsed")


def _check_closure_horizon(f, chain_id: str, chain: ChainTwo, view: View) -> None:
    """THE TWO ENFORCEMENT HORIZONS ARE DIFFERENT AND THE DIFFERENCE IS THE POINT.

    Links 1-6 enforce AT THE GATE, before the merge. Links 9 and 10 enforce AT
    CLOSURE, after it. A MERGE THAT ALREADY HAPPENED IS NOT RETROACTIVELY REFUSED —
    what an unclosed chain forfeits is EVERYTHING DOWNSTREAM OF IT."""
    permitted = any(get(leaf, "verdict", "outcome") == "permitted"
                    and get(leaf, "verdict", "scope") == "links_1_6"
                    and leaf.get("chain_ref") == chain_id
                    for _, leaf in view.leaves)
    if permitted and not chain.closures:
        f.error("merged_and_never_closed",
                f"chain {chain_id}: the gate permitted the terminal act at links 1-6 "
                f"and NO post-merge test record exists. Every consumer of that merge "
                f"REFUSES and the fraud signal fires; the merge itself is not "
                f"un-made, because the horizon that could have refused it has passed. "
                f"An unclosed chain is a REFUSING state and never a pending one")
    for label, doc in chain.remediations:
        if doc.get("promotion_claimed") is True:
            f.error("release_over_unclosed_chain",
                    f"{label}: promotion or release is attempted because a "
                    f"remediation chain was admitted. ADMISSION OF THE REPAIR IS "
                    f"NEVER READ AS CLOSURE of the chain being repaired, and the "
                    f"merge having succeeded is never accepted as evidence that the "
                    f"chain closed")


# --------------------------------------------------------------------------
# rule: the remediation exemption
# --------------------------------------------------------------------------

def check_remediation(f, view: View) -> None:
    for chain_id, chain in view.chains.items():
        for label, doc in chain.remediations:
            if doc.get("covered_by_ratifying_signature") is not True:
                f.error("remediation_subject_not_declared",
                        f"{label}: the remediation subject is not covered by the "
                        f"bytes the ratifying signature covers. MENTIONING IS NEVER "
                        f"DECLARING — a declaration attachable afterwards is a "
                        f"declaration anyone can attach, and the exemption would "
                        f"then be claimable by relabelling")
            if doc.get("inherits_exemption") is True:
                f.error("remediation_exemption_inherited",
                        f"{label}: the exemption is claimed by inheritance. A chain "
                        f"that builds on a remediation chain is an ORDINARY consumer "
                        f"and stays refused while the original is unclosed — an "
                        f"exemption that descends is an exemption that LAUNDERS")
            if not chain.setups or not chain.decisions:
                f.error("remediation_skips_gate",
                        f"{label}: the remediation chain is offered with its own "
                        f"links 4-6 absent. It is exempt as a CONSUMER and never as "
                        f"a CHAIN, and its purpose is not accepted as a substitute "
                        f"for its own links")
            for closure_label, closure in chain.closures:
                if get(closure, "signed_closure", "test_execution", "result") != "passed":
                    f.error("remediation_own_closure_failed",
                            f"{closure_label}: the remediation chain's OWN closure "
                            f"did not pass, so it is itself unclosed and refuses its "
                            f"own downstream. Its remediation status does not exempt "
                            f"it from the invariant it was raised under")


# --------------------------------------------------------------------------
# rule: the gate's own verdicts, at tranche two's scope
# --------------------------------------------------------------------------

def check_verdicts(f, view: View) -> None:
    for label, leaf in view.leaves:
        verdict = leaf.get("verdict")
        if not isinstance(verdict, dict):
            continue
        chain_id = leaf.get("chain_ref")
        chain = view.chains.get(chain_id) if isinstance(chain_id, str) else None
        scope = verdict.get("scope")
        checks = verdict.get("checks") or []
        if scope == "links_1_6" and len(checks) != 8 + len(EXTENDED_CHECK_NAMES):
            f.error("gate_walk_incomplete",
                    f"{label}: a links_1_6 verdict records {len(checks)} checks "
                    f"where the extended walk has {8 + len(EXTENDED_CHECK_NAMES)}. "
                    f"The links 4-6 legs are PART OF THE SAME ONE WALK and not a "
                    f"second gate, so a verdict claiming the longer scope while "
                    f"recording only the shorter walk has not walked it")
        if scope == "links_1_3" and chain is not None and chain.carries_tranche_two():
            f.error("gate_scope_understated",
                    f"{label}: the verdict claims scope links_1_3 over a chain "
                    f"carrying tranche-two records. THE GATE'S SCOPE IS EXACTLY THE "
                    f"LINKS THE RATIFIED TRANCHES HAVE PUT IN FORCE and it GROWS "
                    f"WITH THEM; a scope note written before a tranche existed is "
                    f"never available as a permission after it")
        if scope == "links_1_6" and verdict.get("outcome") == "permitted" \
                and (chain is None or not chain.carries_tranche_two()):
            f.error("links_1_3_only_after_tranche_two",
                    f"{label}: the terminal act is permitted for a chain presenting "
                    f"the ratification, the inception and the traveling contract and "
                    f"NO ATTESTATION LINKS AT ALL. Links 4-6 are in scope from this "
                    f"tranche and are no longer 'a later tranche's link', so tranche "
                    f"one's scope note is not available as a permission — it was "
                    f"written for the period before this tranche existed")


# --------------------------------------------------------------------------
# rule: the design obligations a gate cannot see
# --------------------------------------------------------------------------

DESIGN_REFUSALS: list[tuple[str, str, set[str], str]] = [
    ("tier2_key_custody", "tier2_key_in_worker",
     {"key_issued_into_worker", "key_issued_into_worker_and_destroyed",
      "handle_dereferencing_to_key"},
     "`access_secrets: false` FORBIDS CUSTODY, NOT MERELY LONG-LIVED CUSTODY. A "
     "private key is a secret; a design that hands a worker a key for one task has "
     "already breached the constraint it claims to honour, and its own destruction "
     "step is not a defence because THE BREACH IS THE CROSSING AND NOT THE "
     "RETENTION. A handle that dereferences to key bytes is key bytes"),
    ("controller_placement", "controller_colocated_with_runner",
     {"same_host_as_runner", "same_process_as_runner",
      "same_credential_scope_as_runner"},
     "A BOUNDARY THE REQUESTER CAN READ ACROSS IS A BOUNDARY IN NAME. The design's "
     "handing nothing across is never accepted as evidence that the boundary "
     "exists"),
    ("controller_placement", "tier2_key_reachable_from_runner",
     {"hardware_backed_reachable_from_runner"},
     "Hardware custody REACHABLE FROM THE RUNNER'S SCOPE does not conform, because "
     "WHERE A KEY LIVES IS NOT THE DISCRIMINATOR: reachability and hand-over are "
     "the same breach reached two ways"),
    ("signing_delegation", "reusable_signing_delegation",
     {"reusable_delegation_issued"},
     "A credential that signs again without asking is CUSTODY BY ANOTHER NAME"),
    ("request_attribution", "platform_attribution_shortfall_undeclared",
     {"cannot_attribute_undeclared"},
     "An UNDECLARED shortfall is non-conformance, and the identical shortfall "
     "DECLARED is conformant as a realization"),
    ("request_attribution", "platform_attribution_shortfall_disqualifies",
     {"cannot_attribute_declared"},
     "THE PLATFORM BRANCH GOVERNS AND IT GOVERNS DOWNWARD, NEVER UPWARD. A chain "
     "whose realization has declared it cannot attribute a signing request to the "
     "task provisioned in link 4 SHALL NOT satisfy the links 1-6 gate for the "
     "terminal act, because the terminal act is itself a use requiring per-task "
     "attribution. The declaration keeps the REALIZATION conformant; it never buys "
     "the gate's permission, and a declaration that disqualifies nothing is an "
     "exemption"),
    ("verification_material", "worker_given_key_material_to_verify",
     {"key_material_supplied_to_worker"},
     "VERIFYING A CHAIN NEEDS NO SECRET: continuity, digests, certificates and "
     "anchor records are public material, and this proposal RE-CREATES THE BREACH "
     "THE TIER SPLIT EXISTS TO PREVENT"),
    ("execution_layer_ordering", "step_executed_without_verified_chain",
     {"execute_then_verify"},
     "THE WEAK VERSION yields an audit trail a compromised or careless lane can "
     "write falsely. A record written after the fact is never accepted as a "
     "PRECONDITION"),
    ("commitment_extension_trigger", "extension_minted_on_request_arrival",
     {"signing_request_arrival"},
     "A realization that mints extensions on the arrival of a signing request "
     "never commits a task whose attestation the runner SUPPRESSES ENTIRELY — no "
     "request, no extension, no expectation — so link 6's enumeration equals the "
     "reduced committed set and THE DROPPED-ATTESTATION ATTACK PASSES AGAIN. A "
     "deadline the runner can influence is no deadline"),
]


def check_design(f, view: View) -> None:
    for label, doc in view.declarations:
        design = doc.get("attestation_design")
        named = [entry.get("obligation") for entry in doc.get("obligations") or []
                 if isinstance(entry, dict)]
        claims_two = any(name in OBLIGATIONS for name in named)
        if not claims_two:
            continue
        if not isinstance(design, dict):
            f.error("residual_not_declared",
                    f"{label}: the declaration names tranche-two obligations and "
                    f"carries no `attestation_design`. Three of them are enforced "
                    f"somewhere other than the walk — tier-2 key custody at review "
                    f"and realization, the executing layer at execution time, and "
                    f"the platform's attribution ceiling as a property of the "
                    f"realization — and a capability that stated them while giving a "
                    f"reader nothing to read would hold three requirements it does "
                    f"not enforce")
            continue
        for member, code, refused, why in DESIGN_REFUSALS:
            if design.get(member) in refused:
                f.error(code, f"{label}: `attestation_design.{member}` is "
                              f"{design.get(member)!r}. {why}")
        if design.get("omnigent_matrix_unchanged") is False:
            f.error("seventh_permission_boolean_proposed",
                    f"{label}: the realization declares it widened the omnigent "
                    f"permission matrix. The matrix is CLOSED over exactly six "
                    f"booleans with `execute_final_action` and `access_secrets` "
                    f"fixed `const: false`, and A REFUSAL IS NOT A PERMISSION: "
                    f"withholding execution requires no capability a worker does not "
                    f"already have")
        if design.get("persona_issued_to_workload") is True:
            f.error("persona_proposed_for_workload",
                    f"{label}: a broker persona is proposed for a runner. A tier-2 "
                    f"attestation identity is a WORKLOAD, and the runner's authority "
                    f"stays a `credential-contracts` / `openxwallet` grant")
        if design.get("ephemeral_lifetime_claimed_non_secret") is True:
            f.error("ephemeral_lifetime_offered_as_non_secret",
                    f"{label}: a key valid for one task is offered as not a secret. "
                    f"`access_secrets: false` binds CUSTODY rather than DURATION, and "
                    f"the key's short life is not accepted as a substitute for the "
                    f"boundary")


# --------------------------------------------------------------------------
# rule: the attestation identity is never an actor
# --------------------------------------------------------------------------

def check_actor(f, view: View) -> None:
    """A WORKLOAD IS NOT A PERSONA AND NEVER APPEARS AS THE ACTOR OF A GOVERNED
    ACT. Widening a SUBJECT does not make a workload a persona, so the refusal
    reaches the chain-scoped identity exactly as it reaches a per-task one."""
    identity_keys = {get(doc, "signed_binding", "identity_key_ref")
                     for chain in view.chains.values()
                     for _, doc in chain.bindings}
    identity_keys.discard(None)
    for chain_id, inception in view.inceptions.items():
        subject = get(inception, "signed_ratification", "actor",
                      "subject_reference", "subject")
        if subject in identity_keys:
            f.error("attestation_identity_as_actor",
                    f"chain {chain_id}: the recorded actor is the tier-2 attestation "
                    f"identity {subject!r}. Validation FAILS because a workload is "
                    f"not a persona, and the act's actor remains link 1's stable "
                    f"opaque subject bound to the wallet that signed")


# --------------------------------------------------------------------------
# the one entry point
# --------------------------------------------------------------------------

def check_tranche_two(f, records: Iterable[tuple[str, dict]],
                      custody_models: dict[str, dict] | None = None) -> None:
    view = build_view(records, custody_models)
    check_signatures(f, view)
    check_issuance(f, view)
    check_setup(f, view)
    check_expectation(f, view)
    check_requests(f, view)
    check_corroboration(f, view)
    check_hash_links(f, view)
    check_decisions(f, view)
    check_closure(f, view)
    check_remediation(f, view)
    check_verdicts(f, view)
    check_design(f, view)
    check_actor(f, view)
