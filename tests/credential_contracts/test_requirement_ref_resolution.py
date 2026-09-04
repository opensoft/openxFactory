"""The resolution-integrity arm (add-requirement-ref-resolution-integrity §3).

THE PACKET'S OWN REPRODUCTION IS THE FIRST TEST IN THIS FILE, and that is
deliberate. The defect was measured as a tree that PASSED with zero warnings and
zero errors while carrying two defective references, and where making the two
`secret_ref`s equal — ONE BYTE, and no other edit to any file — was enough to
make the same tree speak. A reproduction that lives only in a proposal is a
reproduction nobody re-runs; the two files below are the ones `proposal.md`
§ What was measured § 6 writes out in full, so the claim stays checkable against
whatever this validator becomes.

TWO CODES, NAMED APART, because their remedies live in different files. A
reference resolving to NOTHING is repaired AT THE REFERENCE
(`requirement-ref-unresolved`); a reference resolving to SEVERAL is repaired IN
THE REQUIREMENTS DOCUMENT THE REFERENCE NAMES (`requirement-ref-ambiguous`), and
it is the more dangerous of the two because the matches may differ in
`access_mode`.

PER-DOCUMENT, AND THE BOUNDARY IS TESTED RATHER THAN ASSERTED. The ambiguity
this arm names is ambiguity INSIDE the one document a reference names, which is
what the frozen `resolve_requirement` can see. The same id in a DIFFERENT
requirements document draws nothing — ruled out of scope 2026-09-01 and filed as
**openxFactory issue #553**. The boundary is PINNED by a named test, so the
successor can see exactly what it is changing:
`test_the_same_id_in_ANOTHER_document_draws_nothing_at_this_minor`.

THE MUTATION ROUND'S CONTROL IS A BASELINE, NOT A NAME, on the sibling module's
rule: each mutant records BOTH halves — the named check PASSES against unmutated
code, and FAILS against the mutant — because a named test failing on a mutant
for want of a fixture is ANCHOR-MISSING and not a kill. FIVE MUTANTS.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate-credential-contracts.py"


def _load():
    spec = importlib.util.spec_from_file_location(
        "credential_contracts_validator_resolution", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V = _load()

# --------------------------------------------------------------------------
# THE REPRODUCTION, VERBATIM FROM THE PACKET (proposal.md § What was measured §6)
# --------------------------------------------------------------------------

REQUIREMENTS = """\
# Reproduction support for add-requirement-ref-resolution-integrity.
# Three requirement records: one unambiguous, and one id declared TWICE with
# DIFFERENT access modes so a reference to it resolves to MORE THAN ONE.
schema_version: 1
kind: xfactory_credential_requirements
domain:
  id: example-projection
  product_name: Example Projection Lane
requirements:
  - id: alpha_lane
    purpose: the unambiguous sibling, present so the document is a real requirements record
    access_mode: workload_identity
    minimum_scopes:
      - projection:write
    requires_domain_approval: true
    requires_human_approval: false
    max_grant_minutes: 60
    audit_required: true
  - id: dup_lane
    purpose: the first record carrying this id
    access_mode: workload_identity
    minimum_scopes:
      - projection:write
    requires_domain_approval: true
    requires_human_approval: false
    max_grant_minutes: 60
    audit_required: true
  - id: dup_lane
    purpose: the SECOND record carrying the same id, with a different access mode
    access_mode: dispatch_only
    minimum_scopes:
      - actions:read
    requires_domain_approval: true
    requires_human_approval: false
    max_grant_minutes: 60
    audit_required: true
"""

BINDINGS = """\
# Reproduction for add-requirement-ref-resolution-integrity: TWO defective
# references on bindings whose secret references DIFFER BY ONE BYTE
# (`example-secret-a` / `example-secret-b`), so the shipped validator never
# reaches resolution.
schema_version: 1
kind: xfactory_credential_binding_template
client:
  id: example-client
  display_name: Example Client (reproduction)
credential_bindings:
  zero_resolving_lane:
    provider: azure_key_vault
    vault: kv-example-projection
    secret_ref: example-secret-a
    owner: example-platform
    rotation_policy: operator_managed
    consumer:
      holder_ref: example:service-subject:zero-resolving-lane
      fetch_identity: example-zero-resolving-workload-identity
      requirement_ref:
        requirement_id: no_such_requirement
        requirements_document_ref: credentials/example.requirements.yaml
  multi_resolving_lane:
    provider: azure_key_vault
    vault: kv-example-projection
    secret_ref: example-secret-b
    owner: example-platform
    rotation_policy: operator_managed
    consumer:
      holder_ref: example:service-subject:multi-resolving-lane
      fetch_identity: example-multi-resolving-workload-identity
      requirement_ref:
        requirement_id: dup_lane
        requirements_document_ref: credentials/example.requirements.yaml
"""

# THE CONTROL IS ONE BYTE, COUNTED RATHER THAN CLAIMED. The two templates are
# the same length and differ at exactly one offset — the `b` of the second
# binding's `secret_ref` line, and nothing in the comment header, which names
# both spellings and must stay untouched or the edit stops being one byte. An
# earlier draft of the packet spaced them `-one`/`-two` and called that a
# one-byte edit; it is three, and a reader rerunning it would have measured
# something the text did not describe.
CONTROL = BINDINGS.replace("    secret_ref: example-secret-b\n",
                           "    secret_ref: example-secret-a\n")


def _write_repo(tmp_path: Path, bindings: str, requirements: str = REQUIREMENTS) -> Path:
    repo = tmp_path / "domain"
    (repo / "credentials").mkdir(parents=True)
    (repo / "credentials" / "example.requirements.yaml").write_text(requirements)
    (repo / "credentials" / "example.binding-template.yaml").write_text(bindings)
    return repo


def _scan(repo: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(VALIDATOR), str(repo)],
                          capture_output=True, text=True, check=False)


def test_the_control_is_ONE_BYTE_and_the_templates_are_the_SAME_LENGTH():
    """The falsifiable half of the packet's scenario *The shipped check is silent
    on both of them today*: the spacing between reproduction and control is what
    identifies the SCOPE as the defect rather than the depth of the check. If
    this ever costs more than one byte, the claim below is about a different
    edit."""
    a, b = BINDINGS.encode(), CONTROL.encode()
    assert len(a) == len(b), (len(a), len(b))
    assert [i for i, (x, y) in enumerate(zip(a, b)) if x != y] == [980]


def test_the_reproduction_now_REPORTS_and_the_record_stays_VALID(tmp_path):
    """§7.6, the whole point. The same tree that produced `0 warning(s),
    0 error(s) -> PASS` under the shipped validator now names BOTH defects — and
    the verdict does NOT redden, a warning never being a refusal. Nothing
    narrows at this minor."""
    result = _scan(_write_repo(tmp_path, BINDINGS))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "0 error(s) -> PASS" in result.stdout
    assert "2 warning(s)" in result.stdout
    assert "WARN  [requirement-ref-unresolved]" in result.stdout
    assert "WARN  [requirement-ref-ambiguous]" in result.stdout


def test_the_one_byte_control_still_reports_its_own_shared_secret_ERROR(tmp_path):
    """§7.6's second half. The lift path is UNTOUCHED: equalising the two secret
    references still raises `shared-secret-identity` naming the condition that
    stood, and the new warnings now sit BESIDE it rather than in place of it."""
    result = _scan(_write_repo(tmp_path, CONTROL))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "ERROR" in result.stdout and "shared-secret-identity" in result.stdout
    assert "does not declare shared_credential_acknowledged: true" in result.stdout
    assert "WARN  [requirement-ref-unresolved]" in result.stdout
    assert "WARN  [requirement-ref-ambiguous]" in result.stdout


# --------------------------------------------------------------------------
# The arm, driven directly
# --------------------------------------------------------------------------

DOC = "credentials/projection.requirements.yaml"
OTHER_DOC = "credentials/other.requirements.yaml"
INDEX = {
    DOC: [
        {"id": "projection_sync_lane", "access_mode": "workload_identity"},
        {"id": "projection_editor_surface", "access_mode": "workload_identity"},
    ],
    OTHER_DOC: [
        {"id": "projection_sync_lane", "access_mode": "delegated_api"},
    ],
}
AMBIGUOUS_INDEX = {DOC: INDEX[DOC] + [{"id": "projection_sync_lane",
                                       "access_mode": "delegated_api"}]}


def _ref(requirement_id, document=DOC):
    return {"requirement_id": requirement_id, "requirements_document_ref": document}


def _binding(secret, **consumer):
    binding = {"provider": "azure_key_vault", "vault": "kv-example", "secret_ref": secret,
               "owner": "example-platform", "rotation_policy": "operator_managed"}
    if consumer:
        binding["consumer"] = consumer
    return binding


def _doc(**bindings):
    return {"schema_version": 1, "kind": "xfactory_credential_binding_template",
            "client": {"id": "example-client"}, "credential_bindings": dict(bindings)}


def _lone(requirement_ref=...):
    """ONE binding, sharing its secret with nobody — the shape the shipped check
    was silent on, and the shape every test below drives unless it says
    otherwise. The `...` default is what distinguishes a binding that declares NO
    `requirement_ref` from one declaring it as `None`, which are different
    records and draw different findings."""
    consumer = {"holder_ref": "example:service-subject:projection-sync-lane",
                "fetch_identity": "example-sync-lane-workload-identity"}
    if requirement_ref is not ...:
        consumer["requirement_ref"] = requirement_ref
    return _doc(projection_sync_lane=_binding("its-own-secret", **consumer))


def _codes(doc, index=INDEX):
    return [c for c, _ in V._deprecation_warnings(doc, index)]


def _messages(doc, code, index=INDEX):
    return [m for c, m in V._deprecation_warnings(doc, index) if c == code]


def test_a_reference_that_resolves_to_NOTHING_is_reported_on_a_binding_that_shares_nothing():
    doc = _lone(_ref("no_such_requirement"))
    assert _codes(doc) == ["requirement-ref-unresolved"]


def test_a_reference_that_resolves_to_SEVERAL_is_reported_on_a_binding_that_shares_nothing():
    doc = _lone(_ref("projection_sync_lane"))
    assert _codes(doc, AMBIGUOUS_INDEX) == ["requirement-ref-ambiguous"]


def test_the_report_does_not_depend_on_ANY_other_binding_in_the_document():
    """The delta's first scenario, second bullet: the finding must not depend on
    another binding, nor on the vault, owner, provider or consumer any other
    binding declares. So the SAME defective binding reports the same code
    whether it sits alone or beside a second, unrelated, perfectly conformant
    one."""
    alone = _lone(_ref("no_such_requirement"))
    beside = _doc(
        projection_sync_lane=alone["credential_bindings"]["projection_sync_lane"],
        projection_editor_surface=_binding(
            "a-completely-different-secret",
            holder_ref="example:service-subject:projection-editor-surface",
            fetch_identity="example-editor-surface-workload-identity",
            requirement_ref=_ref("projection_editor_surface")))
    assert _codes(alone) == _codes(beside) == ["requirement-ref-unresolved"]


def test_a_reference_that_RESOLVES_draws_nothing():
    assert _codes(_lone(_ref("projection_sync_lane"))) == []


def test_a_binding_that_declares_NO_reference_draws_nothing():
    """An omission is a different question from a wrong answer. The member is
    OPTIONAL at this release, and a fail-open arm reading absence as failure is
    the shape this family has already had to repair once in a drift check."""
    assert _codes(_lone()) == []


def test_a_stub_block_declaring_no_reference_draws_nothing():
    """The same rule reaching the record kind that is written before any install
    exists: a stub declares the token and names nobody, so there is no reference
    to resolve."""
    doc = _doc(projection_sync_lane=_binding("its-own-secret", instantiation_stub=True))
    assert _codes(doc) == []


def test_the_two_codes_are_NAMED_APART_and_neither_is_reported_as_the_other():
    """One record carrying a reference that resolves to nothing, one carrying a
    reference that resolves to several — reported under DISTINCT codes, because
    their remedies are at the reference and in the requirements document
    respectively."""
    doc = _doc(
        zero_resolving_lane=_binding(
            "secret-a",
            holder_ref="example:service-subject:zero-resolving-lane",
            fetch_identity="example-zero-resolving-workload-identity",
            requirement_ref=_ref("no_such_requirement")),
        multi_resolving_lane=_binding(
            "secret-b",
            holder_ref="example:service-subject:multi-resolving-lane",
            fetch_identity="example-multi-resolving-workload-identity",
            requirement_ref=_ref("projection_sync_lane")))
    assert sorted(_codes(doc, AMBIGUOUS_INDEX)) == [
        "requirement-ref-ambiguous", "requirement-ref-unresolved"]


def test_the_message_names_WHICH_OF_THE_TWO_it_found_and_where_the_repair_is():
    """A code a reader can act on names the file to open. The zero case is
    repaired AT THE REFERENCE; the many case is repaired IN THE REQUIREMENTS
    DOCUMENT THE REFERENCE NAMES, and a reader told only that 'the reference did
    not resolve' has no way to know that two records answered."""
    zero, = _messages(_lone(_ref("no_such_requirement")), "requirement-ref-unresolved")
    assert "resolves to NOTHING" in zero
    assert "THE REPAIR IS AT THE REFERENCE" in zero
    assert "MORE THAN ONE" not in zero

    many, = _messages(_lone(_ref("projection_sync_lane")), "requirement-ref-ambiguous",
                      AMBIGUOUS_INDEX)
    assert "MORE THAN ONE requirement OF THAT ONE DOCUMENT" in many
    assert "THE REPAIR IS IN THE REQUIREMENTS DOCUMENT THE REFERENCE NAMES" in many
    assert "resolves to NOTHING" not in many


def test_the_message_names_the_binding_the_id_and_the_document():
    zero, = _messages(_lone(_ref("no_such_requirement")), "requirement-ref-unresolved")
    for token in ("projection_sync_lane", "no_such_requirement", DOC):
        assert token in zero, token


def test_both_messages_name_the_release_that_refuses_them():
    """The phasing is in the finding a consumer reads, not only in a policy
    document they may never open."""
    zero, = _messages(_lone(_ref("no_such_requirement")), "requirement-ref-unresolved")
    many, = _messages(_lone(_ref("projection_sync_lane")), "requirement-ref-ambiguous",
                      AMBIGUOUS_INDEX)
    assert V.MAJOR_RELEASE in zero and V.MAJOR_RELEASE in many


def test_the_ambiguity_message_cites_the_successor_that_owns_the_wider_arm():
    """§3.4: the realization MUST NOT read as having satisfied the promoted
    scenario's cross-document arm. The citation travels in the finding itself,
    where the reader who hits the per-document boundary is standing."""
    many, = _messages(_lone(_ref("projection_sync_lane")), "requirement-ref-ambiguous",
                      AMBIGUOUS_INDEX)
    assert "#553" in many and "PER-DOCUMENT" in many


# --------------------------- the per-document boundary ---------------------------

def test_the_same_id_in_ANOTHER_document_draws_nothing_at_this_minor():
    """RULED OUT OF SCOPE 2026-09-01 AND FILED AS openxFactory ISSUE #553 — the
    boundary is PINNED here rather than left implicit, so the successor that
    broadens the lookup can see exactly which assertion it is changing.

    `INDEX` declares `projection_sync_lane` in TWO schema-valid documents. The
    frozen `resolve_requirement` matches inside `index.get(document_ref)` over an
    index keyed BY DOCUMENT PATH, so a reference naming either resolves `ok`.
    This change neither created that gap nor closes it, and — since the
    2026-09-01 amendment — no longer claims to."""
    assert len(INDEX[DOC]) + len(INDEX[OTHER_DOC]) > 1
    assert [r["id"] for r in INDEX[OTHER_DOC]] == ["projection_sync_lane"]
    assert _codes(_lone(_ref("projection_sync_lane"))) == []
    assert _codes(_lone(_ref("projection_sync_lane", OTHER_DOC))) == []


# --------------------------- one fault, one finding ---------------------------

@pytest.mark.parametrize("ref,expected", [
    # not the qualified two-member object -> `consumer-member-grammar` owns it
    ("projection_sync_lane", "consumer-member-grammar"),
    ({"requirement_id": "no_such_requirement"}, "consumer-member-grammar"),
    ({"requirement_id": "no_such_requirement", "requirements_document_ref": DOC,
      "extra": 1}, "consumer-member-grammar"),
    # an ungrammatical document reference -> `consumer-requirement-ref-grammar`
    ({"requirement_id": "no_such_requirement",
      "requirements_document_ref": "/etc/r.yaml"}, "consumer-requirement-ref-grammar"),
    # an ungrammatical requirement id -> `consumer-member-grammar` again
    ({"requirement_id": "not an identifier",
      "requirements_document_ref": DOC}, "consumer-member-grammar"),
], ids=["bare-id", "one-member", "extra-member", "absolute-document", "ungrammatical-id"])
def test_a_shape_the_GRAMMAR_arms_already_report_is_not_reported_TWICE(ref, expected):
    """§3.2. Every one of these references also fails to resolve, so an arm that
    reported on `not-found` alone would name each of them twice — and the
    family's rule is that a refusal names the fault it found, and names it once.
    A reader repairing a malformed reference is not helped by being told a second
    time that the malformed reference did not resolve."""
    codes = _codes(_lone(ref))
    assert expected in codes
    assert not any(c.startswith("requirement-ref-") for c in codes), codes


def test_a_MALFORMED_reference_is_reported_rather_than_raised():
    """The block is UNCONSTRAINED at this minor, so a reference may be any shape
    at all. Report, never raise — a crash is not a verdict, and one malformed
    record aborting the scan silences every finding about every other file."""
    for ref in (None, [], 7, {1: "an int key"}, {"requirement_id": None,
                                                 "requirements_document_ref": DOC}):
        assert isinstance(V._deprecation_warnings(_lone(ref), INDEX), list), ref


# --------------------------- the lift keeps its own duty ---------------------------

def _sharing_pair():
    """Two bindings on ONE secret, one of them naming a reference that resolves
    to nothing."""
    return _doc(
        zero_resolving_lane=_binding(
            "one-operated-identity",
            holder_ref="example:service-subject:zero-resolving-lane",
            fetch_identity="example-zero-resolving-workload-identity",
            requirement_ref=_ref("no_such_requirement"),
            shared_credential_acknowledged=True),
        projection_editor_surface=_binding(
            "one-operated-identity",
            holder_ref="example:service-subject:projection-editor-surface",
            fetch_identity="example-editor-surface-workload-identity",
            requirement_ref=_ref("projection_editor_surface"),
            shared_credential_acknowledged=True))


def test_the_sharing_pair_keeps_BOTH_duties_and_neither_replaced_the_other():
    """§3.5 and the delta's sixth scenario. The two findings answer DIFFERENT
    questions — whether this reference is sound, and whether this pair may be
    exempted from the default refusal — so they are not a duplicate under the
    'name it once' rule, which is a rule against two names for one fault and not
    against two faults in one record. A reader repairing the reference discharges
    the first; the second may still stand on a different condition."""
    doc = _sharing_pair()
    findings = V._semantic_findings(doc, INDEX)
    assert len(findings) == 1 and findings[0].startswith("shared-secret-identity")
    assert "resolves to no requirement in the repository under validation" in findings[0]
    assert _codes(doc) == ["requirement-ref-unresolved"]


def _conforming_pair():
    """The packaged two-consumer positive's shape: one operated identity, two
    consuming systems, all SIX lift conditions satisfied — including the sixth,
    each reference's `requirement_id` equalling its own binding's map key."""
    return _doc(
        projection_sync_lane=_binding(
            "one-operated-identity",
            holder_ref="example:service-subject:projection-sync-lane",
            fetch_identity="example-sync-lane-workload-identity",
            requirement_ref=_ref("projection_sync_lane"),
            shared_credential_acknowledged=True),
        projection_editor_surface=_binding(
            "one-operated-identity",
            holder_ref="example:service-subject:projection-editor-surface",
            fetch_identity="example-editor-surface-workload-identity",
            requirement_ref=_ref("projection_editor_surface"),
            shared_credential_acknowledged=True))


def test_the_lift_path_is_UNTOUCHED_and_a_conforming_pair_still_lifts():
    """§3.5's other half, and the control for the test above: if a conforming
    pair ever stopped lifting, that test would be passing on a refusal that was
    never available to lift. Two references that RESOLVE draw nothing from the
    new arm either, whatever the pair shares."""
    doc = _conforming_pair()
    assert V._semantic_findings(doc, INDEX) == []
    assert _codes(doc) == []


def test_the_pair_that_lifts_stops_lifting_when_one_reference_stops_resolving():
    """The one-edit spacing between the two tests above: the ONLY difference
    between the conforming pair and the refused one is a `requirement_id`, and
    it moves BOTH verdicts at once — the lift withheld, and the reference
    reported on its own binding."""
    doc = _conforming_pair()
    doc["credential_bindings"]["projection_sync_lane"]["consumer"]["requirement_ref"] = \
        _ref("no_such_requirement")
    findings = V._semantic_findings(doc, INDEX)
    assert len(findings) == 1 and findings[0].startswith("shared-secret-identity")
    assert _codes(doc) == ["requirement-ref-unresolved"]


# --------------------------- the code family ---------------------------

def test_the_two_codes_are_DECLARED_and_are_not_a_widening_of_the_consumer_block_set():
    """The delta's *The finding is not a widening of an existing code*: a reader
    must be able to tell a resolution failure from a grammar failure BY THE CODE
    ALONE. Filing it under a grammar code would make that code untrue in the
    other direction — a code meaning 'this value does not match the pattern'
    would come to carry a record whose values match every pattern this family
    declares."""
    assert V.DEPRECATION_CODES[-2:] == ("requirement-ref-unresolved",
                                        "requirement-ref-ambiguous")
    # 10 -> 11 by add-consumer-identity-namespace, whose ninth `consumer-*` code
    # joins its OWN family and is inserted BEFORE these two, so the claim this
    # test actually makes — that the resolution pair is a second family and sits
    # apart from the block's shape codes — is unweakened by the move.
    assert len(V.DEPRECATION_CODES) == 11
    for code in V.DEPRECATION_CODES[-2:]:
        assert not code.startswith("consumer-"), code


def test_every_declared_code_carries_a_registered_probe_and_no_probe_is_stray():
    """The self-test's own rule, asserted here too so a code added without a
    fixture fails at the unit level rather than only in a subprocess."""
    probed = set(V.WARNING_EXPECTATIONS.values())
    assert [c for c in V.DEPRECATION_CODES if c not in probed] == []
    assert sorted(c for c in probed if c not in V.DEPRECATION_CODES) == []


def test_no_index_means_no_resolution_finding():
    """A caller that built no index resolved nothing. Reporting `not-found`
    against an index that was never built would be a finding about the caller
    rather than about the record — and every existing caller passing one
    positional argument would start warning on references it never looked up."""
    doc = _lone(_ref("no_such_requirement"))
    assert [c for c, _ in V._deprecation_warnings(doc)] == []
    assert V._requirement_resolution_warnings(list(doc["credential_bindings"].items()),
                                              None) == []


# --------------------------------------------------------------------------
# THE MUTATION ROUND (§3.7)
# --------------------------------------------------------------------------
#
# FIVE MUTANTS. Four are the arms §3.7 enumerates — drop the per-binding call,
# merge the two codes, report on an undeclared member, scope the new arm back to
# `by_secret`. The fifth, reporting the WRONG STATUS, is carried in addition:
# the AD-1 one-code branch that was OFFERED AND DECLINED would have moved the
# fault's name from the CODE into the MESSAGE, and it named exactly this mutant
# as the one the second code was buying. The branch was declined; the mutant is
# cheap, and it proves the two codes are not merely spelled differently but
# routed differently.

_REAL_ARM = V._requirement_resolution_warnings


def _drop_the_call():
    return lambda bindings, index: []


def _merge_the_two_codes():
    def mutant(bindings, index):
        return [("requirement-ref-unresolved", m) for _c, m in _REAL_ARM(bindings, index)]
    return mutant


def _report_the_wrong_status():
    swap = {"requirement-ref-unresolved": "requirement-ref-ambiguous",
            "requirement-ref-ambiguous": "requirement-ref-unresolved"}
    def mutant(bindings, index):
        return [(swap[c], m) for c, m in _REAL_ARM(bindings, index)]
    return mutant


def _report_on_an_undeclared_member():
    def mutant(bindings, index):
        out = list(_REAL_ARM(bindings, index))
        for name, binding in bindings:
            consumer = V._consumer(binding)
            if isinstance(consumer, dict) and "requirement_ref" not in consumer:
                out.append(("requirement-ref-unresolved",
                            f"binding {name!r} declares no requirement_ref"))
        return out
    return mutant


def _scope_back_to_by_secret():
    """THE PRE-CHANGE SHAPE, and the one this whole packet exists to retire: the
    resolution is consulted only where two bindings share a `secret_ref`."""
    def mutant(bindings, index):
        seen: dict[str, int] = {}
        for _name, binding in bindings:
            ref = binding.get("secret_ref")
            if isinstance(ref, str):
                seen[ref] = seen.get(ref, 0) + 1
        sharers = [(n, b) for n, b in bindings if seen.get(b.get("secret_ref"), 0) > 1]
        return _REAL_ARM(sharers, index)
    return mutant


def _ambiguous_doc():
    return _lone(_ref("projection_sync_lane"))


def _both_defects():
    """ONE document carrying ONE of each fault, which is the only shape that can
    tell a MERGED code from a correctly SPLIT one: with a single defective
    binding, a validator emitting one code for both statuses is
    indistinguishable from one emitting the right code for that status."""
    return _doc(
        zero_resolving_lane=_binding(
            "secret-a",
            holder_ref="example:service-subject:zero-resolving-lane",
            fetch_identity="example-zero-resolving-workload-identity",
            requirement_ref=_ref("no_such_requirement")),
        multi_resolving_lane=_binding(
            "secret-b",
            holder_ref="example:service-subject:multi-resolving-lane",
            fetch_identity="example-multi-resolving-workload-identity",
            requirement_ref=_ref("projection_sync_lane")))


MUTANTS = {
    "drop-the-per-binding-call": (
        _drop_the_call(),
        "test_a_reference_that_resolves_to_NOTHING_is_reported_on_a_binding_that_shares_nothing",
        lambda: _lone(_ref("no_such_requirement")), INDEX),
    "merge-the-two-codes": (
        _merge_the_two_codes(),
        "test_the_two_codes_are_NAMED_APART_and_neither_is_reported_as_the_other",
        _both_defects, AMBIGUOUS_INDEX),
    "report-the-wrong-status": (
        _report_the_wrong_status(),
        "test_a_reference_that_resolves_to_SEVERAL_is_reported_on_a_binding_that_shares_nothing",
        _ambiguous_doc, AMBIGUOUS_INDEX),
    "report-on-an-undeclared-member": (
        _report_on_an_undeclared_member(),
        "test_a_binding_that_declares_NO_reference_draws_nothing",
        _lone, INDEX),
    "scope-back-to-by_secret": (
        _scope_back_to_by_secret(),
        "test_a_reference_that_resolves_to_NOTHING_is_reported_on_a_binding_that_shares_nothing",
        lambda: _lone(_ref("no_such_requirement")), INDEX),
}

# The verdict each mutant must change: `(doc builder, index) -> the codes the
# UNMUTATED arm produces`. A mutant DIES when the codes move.
EXPECTED = {
    "drop-the-per-binding-call": ["requirement-ref-unresolved"],
    "merge-the-two-codes": ["requirement-ref-unresolved", "requirement-ref-ambiguous"],
    "report-the-wrong-status": ["requirement-ref-ambiguous"],
    "report-on-an-undeclared-member": [],
    "scope-back-to-by_secret": ["requirement-ref-unresolved"],
}


def test_the_mutant_population_is_an_explicit_count():
    assert len(MUTANTS) == 5
    assert set(MUTANTS) == set(EXPECTED)


@pytest.mark.parametrize("mutant", sorted(MUTANTS))
def test_the_named_test_PASSES_against_unmutated_code(mutant):
    """THE ANCHOR CHECK. Without it, a named test that fails on the mutant
    because its fixture or assertion target is absent is indistinguishable from
    one that fails because the mutation was caught — ANCHOR-MISSING, which is
    not the same state as SURVIVED."""
    _replacement, named, build, index = MUTANTS[mutant]
    assert named in globals(), f"{mutant} names a test that does not exist: {named}"
    assert _codes(build(), index) == EXPECTED[mutant], (
        f"{mutant}: the anchor fixture does not produce the verdict the mutation must change")


@pytest.mark.parametrize("mutant", sorted(MUTANTS))
def test_each_mutant_DIES(mutant, monkeypatch):
    replacement, named, build, index = MUTANTS[mutant]
    monkeypatch.setattr(V, "_requirement_resolution_warnings", replacement)
    assert _codes(build(), index) != EXPECTED[mutant], (
        f"{mutant} SURVIVED — the arm it removes changes no outcome, so the check named "
        f"{named} is passing on something other than that arm")


# --------------------------------------------------------------------------
# The packaged corpus, in both directions
# --------------------------------------------------------------------------

EXAMPLES = ROOT / "examples" / "credential-contracts"


@pytest.mark.parametrize("fixture,code", [
    ("requirement-ref-unresolved.yaml", "requirement-ref-unresolved"),
    ("requirement-ref-ambiguous.yaml", "requirement-ref-ambiguous"),
])
def test_each_packaged_probe_shares_its_secret_with_NOBODY(fixture, code):
    """The probes must fail for the SCOPE this change widens rather than for the
    scope that already reported. A probe that shared a secret would pass against
    the shipped validator too, and would evidence nothing."""
    import yaml
    doc = yaml.safe_load((EXAMPLES / "warning" / fixture).read_text())
    secrets = [b.get("secret_ref") for b in doc["credential_bindings"].values()]
    assert len(secrets) == len(set(secrets))
    assert V.WARNING_EXPECTATIONS[fixture] == code


def test_the_positive_proves_the_SILENT_direction_and_shares_no_secret():
    """§4.3 / OQ-4. A corpus holding only the failing direction cannot tell a
    working check from one that fires on everything, so the silent direction is
    packaged as its own file — and a regression in it names that file."""
    import yaml
    path = EXAMPLES / "resolving-requirement-ref.binding-template.example.yaml"
    doc = yaml.safe_load(path.read_text())
    bindings = doc["credential_bindings"]
    secrets = [b["secret_ref"] for b in bindings.values()]
    assert len(secrets) == len(set(secrets)) == 2
    assert all("requirement_ref" in b["consumer"] for b in bindings.values())
