"""`DocumentAbstract` and its verifier — the model-derived distilled abstract's
type and the rule that decides whether it renders at all
(add-doxbench-distilled-abstract, ruling 4(a), design D3/D4, tasks §4.1-§4.6).

The four things this file pins, and each is a REFUSAL rather than a preference:

  * the guarantees are STRUCTURAL — a caller cannot construct an authoritative
    abstract, or one that claims to be regenerable from anything but its own
    document, any more than it can construct an authoritative `DocumentThread`
    (`doxbench_threads.py:619`);
  * the verification base is the SNAPSHOT'S OWN declared fields — its `topics`
    and its `destinations`, the same fields `documentAbstract` reads
    (`staging-workbench-model.js:1566-1573`) — so the rule fires on generation
    #1 and not only on a regeneration, and a previously generated abstract is
    an ADDITIONAL base and never the only one;
  * the one clause the response BYTES can decide: name the subject, name no
    repository path the request did not carry — which refuses the
    wrong-document answer and the leaked-neighbour answer together; and
  * a verification failure renders NOTHING. The refusal type carries no prose,
    no abstract and no text field, so there is nothing downstream COULD render
    unverified even if it wanted to — the downgrade this change exists to
    prevent is impossible by construction rather than by discipline.

Every `dispatch_result` here is HAND-SEEDED (clarification N5):
`FakeWorkbenchModelPort.dispatch` returns a CONSTANT, so a verifier suite run
against the default fake would prove only that the happy path does not crash.
One test drives that constant deliberately, to show it is REFUSED.
"""

from __future__ import annotations

import dataclasses
import hashlib
import inspect

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import doxbench_knowledge as kn  # noqa: E402
from ideation_dashboard import doxbench_packet as pk  # noqa: E402
from ideation_dashboard import doxbench_threads as dt  # noqa: E402

MODULE_PATH = (REPO_ROOT / "scripts" / "ideation_dashboard"
               / "doxbench_knowledge.py")

# ---------------------------------------------------------------------------
# the fixture subject: one document, its saved bytes, and the SNAPSHOT'S own
# declared fields for it
# ---------------------------------------------------------------------------

SUBJECT_PATH = "ideation/staging/rails/notes.md"
SUBJECT_TITLE = "Rails before the provider call"
NEIGHBOUR_PATH = "ideation/staging/coffee/private-notes.md"

DOCUMENT_TEXT = ("Status: draft\n\n"
                 "The packet assembler runs its rails before any provider "
                 "call.\n")
DIGEST = hashlib.sha256(DOCUMENT_TEXT.encode("utf-8")).hexdigest()
OTHER_DIGEST = hashlib.sha256(
    (DOCUMENT_TEXT + "an edit\n").encode("utf-8")).hexdigest()
MODEL_ID = "workbench-fake-1"

# The snapshot's shape, taken from the fields `documentAbstract` reads: a
# `topics` array and a `destinations` object of kind -> names.
DECLARED_TOPICS = ("packet assembly", "confinement")
DECLARED_DESTINATIONS = {
    "capability": ("ideation-dashboard",),
    "spec": ("workflow-gate-contract",),
}
FLAT_DESTINATIONS = ("capability: ideation-dashboard",
                     "spec: workflow-gate-contract")

# --- hand-seeded dispatch results, one per class -----------------------------

COVERED = ("ideation/staging/rails/notes.md sets out how packet assembly runs "
           "its rails before any provider call, and what confinement means "
           "for the staged set.")
COVERED_BY_DESTINATION_ONLY = (
    "ideation/staging/rails/notes.md lands in the ideation-dashboard "
    "capability and says nothing else about itself.")
COVERED_BY_TITLE_ONLY = (
    "Rails before the provider call is a note about packet assembly.")
NO_DECLARED_SUBJECT_MENTIONED = (
    "ideation/staging/rails/notes.md is a short note about brewing coffee in "
    "the morning.")
NAMES_A_FOREIGN_PATH = (
    "ideation/staging/rails/notes.md restates packet assembly, and see also "
    "ideation/staging/coffee/private-notes.md.")
NAMES_A_FOREIGN_DIRECTORY = (
    "ideation/staging/rails/notes.md restates packet assembly, which also "
    "lands in openspec/specs/ideation-dashboard.")
NAMES_THE_WRONG_SUBJECT = (
    "ideation/staging/coffee/private-notes.md is a note about packet assembly "
    "and confinement.")
NAMES_NO_SUBJECT_AT_ALL = (
    "The note covers packet assembly and confinement in about a page.")
ORDINARY_SLASH_PAIRS = (
    "ideation/staging/rails/notes.md sets out packet assembly, the read/write "
    "ordering and the input/output bounds.")


def _verify(dispatch_result: str, **overrides: object) -> object:
    arguments: dict[str, object] = {
        "subject_path": SUBJECT_PATH,
        "subject_digest": DIGEST,
        "model_id": MODEL_ID,
        "declared_topics": DECLARED_TOPICS,
        "declared_destinations": DECLARED_DESTINATIONS,
        "request_paths": (SUBJECT_PATH,),
        "subject_title": SUBJECT_TITLE,
    }
    arguments.update(overrides)
    return kn.verify_document_abstract(dispatch_result, **arguments)


def _abstract(**overrides: object) -> object:
    fields: dict[str, object] = {
        "subject_path": SUBJECT_PATH,
        "subject_digest": DIGEST,
        "model_id": MODEL_ID,
        "prose": COVERED,
    }
    fields.update(overrides)
    return kn.DocumentAbstract(**fields)


# ===========================================================================
# 4.1 — THE GUARANTEES ARE STRUCTURAL, NOT DECLARED
# ===========================================================================


def test_an_authoritative_abstract_cannot_be_constructed():
    """`DocumentThread`'s discipline (`doxbench_threads.py:619`) in the sibling
    type: the refusal lands where the CLAIM is made, so no cache, renderer or
    route can ever hold an abstract that says it is authoritative."""
    with pytest.raises(kn.AbstractFormatRefused) as raised:
        _abstract(authority="authoritative")
    assert kn.NON_AUTHORITATIVE in str(raised.value)


def test_an_abstract_regenerable_from_anything_but_its_document_is_refused():
    with pytest.raises(kn.AbstractFormatRefused) as raised:
        _abstract(regenerable_from="transcript")
    assert kn.REGENERABLE_FROM_DOCUMENT in str(raised.value)


def test_the_two_guarantees_are_fields_with_one_legal_value_each():
    abstract = _abstract()
    assert abstract.authority == kn.NON_AUTHORITATIVE
    assert abstract.regenerable_from == kn.REGENERABLE_FROM_DOCUMENT
    names = {field.name for field in dataclasses.fields(kn.DocumentAbstract)}
    assert {"authority", "regenerable_from"} <= names


def test_the_abstract_is_frozen_so_a_holder_cannot_promote_it_in_place():
    abstract = _abstract()
    with pytest.raises(dataclasses.FrozenInstanceError):
        abstract.authority = "authoritative"


def test_the_abstract_carries_its_source_path_digest_and_model():
    abstract = _abstract()
    assert abstract.subject_path == SUBJECT_PATH
    assert abstract.subject_digest == DIGEST
    assert abstract.model_id == MODEL_ID


@pytest.mark.parametrize("digest", [
    DIGEST.upper(),          # a key that differs only in case is two keys
    DIGEST[:63],             # short
    "z" * 64,                # not hex
    "",
])
def test_the_source_digest_is_sha256_hex_lowercase(digest):
    with pytest.raises(kn.AbstractFormatRefused):
        _abstract(subject_digest=digest)


def test_the_digest_helper_is_the_one_spelling_of_the_cache_key_half():
    """The store keys on `(subject path, content digest)`; a second spelling of
    the digest would be a second key for one document."""
    assert kn.document_content_digest(DOCUMENT_TEXT) == DIGEST


@pytest.mark.parametrize("path", [
    "/etc/passwd", "../outside/notes.md", "back\\slash.md", "", "   ",
])
def test_the_subject_path_is_repository_relative_posix(path):
    with pytest.raises(kn.AbstractFormatRefused):
        _abstract(subject_path=path)


def test_generation_is_a_monotonic_sequence_and_never_a_wall_clock():
    """No timestamp anywhere: this surface's determinism culture is that a
    snapshot's bytes do not move because a clock did."""
    names = {field.name for field in dataclasses.fields(kn.DocumentAbstract)}
    for forbidden in ("generated_at", "timestamp", "created_at", "when",
                      "time", "clock", "date"):
        assert forbidden not in names, forbidden
    assert _abstract(generation=3).generation == 3
    with pytest.raises(kn.AbstractFormatRefused):
        _abstract(generation=-1)
    source = MODULE_PATH.read_text(encoding="utf-8")
    for needle in ("import time", "datetime", "time.time"):
        assert needle not in source, needle


# ===========================================================================
# 4.2 — SUBJECT-MENTION COVERAGE, BASED ON THE SNAPSHOT'S DECLARED FIELDS
# ===========================================================================


def test_an_abstract_mentioning_no_declared_subject_is_refused_on_generation_1():
    """The falsified requirement verified an abstract against the PREVIOUS
    abstract, so generation #1 was unverifiable. The base is the snapshot's own
    declared topics and destinations, so the rule fires with no previous
    abstract present."""
    verdict = _verify(NO_DECLARED_SUBJECT_MENTIONED, previous=None)
    assert isinstance(verdict, kn.AbstractRefused)
    assert verdict.code == kn.ABSTRACT_REFUSED_COVERAGE
    assert "declared" in verdict.reason


def test_one_declared_topic_is_enough_coverage():
    abstract = _verify(COVERED)
    assert isinstance(abstract, kn.DocumentAbstract)
    assert "packet assembly" in abstract.covered


def test_a_declared_destination_alone_is_coverage():
    """`destinations` is half the base, not decoration: an abstract that names
    only where the document lands has mentioned a declared subject."""
    abstract = _verify(COVERED_BY_DESTINATION_ONLY)
    assert isinstance(abstract, kn.DocumentAbstract)
    assert "ideation-dashboard" in abstract.covered


def test_the_flattened_destination_shape_is_accepted_too():
    """The surface flattens `destinations` to `kind: name` lands
    (`staging-workbench-model.js:1566-1571`); the verifier takes either shape so
    the route is not forced to reshape a snapshot field to be verified."""
    abstract = _verify(COVERED_BY_DESTINATION_ONLY,
                       declared_destinations=FLAT_DESTINATIONS)
    assert isinstance(abstract, kn.DocumentAbstract)
    assert "ideation-dashboard" in abstract.covered


def test_a_subject_with_no_declared_fields_has_no_base_to_verify_against():
    """A document the snapshot carries no derivation for cannot be verified, and
    an unverifiable abstract renders nothing rather than rendering unchecked."""
    verdict = _verify(COVERED, declared_topics=(), declared_destinations=())
    assert isinstance(verdict, kn.AbstractRefused)
    assert verdict.code == kn.ABSTRACT_REFUSED_NO_DECLARED_BASE


def test_a_previous_abstract_is_an_additional_base_and_never_the_only_one():
    """It can only TIGHTEN: a regeneration that drops every declared subject its
    predecessor covered is refused, and a previous abstract never substitutes
    for the snapshot's fields."""
    previous = _abstract(covered=("packet assembly", "confinement"))
    verdict = _verify(COVERED_BY_DESTINATION_ONLY, previous=previous)
    assert isinstance(verdict, kn.AbstractRefused)
    assert verdict.code == kn.ABSTRACT_REFUSED_PREVIOUS_COVERAGE
    # and it cannot rescue an abstract the DECLARED fields refuse
    rescued = _verify(NO_DECLARED_SUBJECT_MENTIONED, previous=previous)
    assert isinstance(rescued, kn.AbstractRefused)


def test_a_previous_abstract_for_another_subject_is_a_caller_defect():
    previous = _abstract(subject_path="ideation/staging/coffee/notes.md")
    with pytest.raises(kn.AbstractFormatRefused):
        _verify(COVERED, previous=previous)


def test_the_default_fake_ports_constant_answer_is_refused():
    """Clarification N5, executable. `FakeWorkbenchModelPort.dispatch` returns
    the same constant for every envelope, so a suite that only ran the default
    fake through the verifier would prove nothing. It is REFUSED: the constant
    names no subject at all."""
    from ideation_dashboard.doxbench_model import FakeWorkbenchModelPort

    port = FakeWorkbenchModelPort()
    result = port.dispatch(object())
    verdict = _verify(result["assistant_prose"])
    assert isinstance(verdict, kn.AbstractRefused)
    assert verdict.code == kn.ABSTRACT_REFUSED_SUBJECT_NOT_NAMED


def test_an_empty_answer_is_refused_rather_than_rendered_as_an_empty_abstract():
    verdict = _verify("   \n  ")
    assert isinstance(verdict, kn.AbstractRefused)
    assert verdict.code == kn.ABSTRACT_REFUSED_EMPTY


# ===========================================================================
# 4.3 — THE ONE CLAUSE THE RESPONSE BYTES CAN DECIDE
# ===========================================================================


def test_naming_the_subjects_own_path_passes():
    abstract = _verify(COVERED)
    assert isinstance(abstract, kn.DocumentAbstract)
    assert abstract.subject_path == SUBJECT_PATH
    assert abstract.prose == COVERED


def test_naming_the_subjects_title_instead_of_its_path_passes():
    abstract = _verify(COVERED_BY_TITLE_ONLY)
    assert isinstance(abstract, kn.DocumentAbstract)


def test_a_repository_path_the_request_did_not_carry_is_refused():
    """The leaked-neighbour answer: the request carried exactly one document, so
    a second path in the response came from somewhere the request did not."""
    verdict = _verify(NAMES_A_FOREIGN_PATH)
    assert isinstance(verdict, kn.AbstractRefused)
    assert verdict.code == kn.ABSTRACT_REFUSED_FOREIGN_PATH
    assert NEIGHBOUR_PATH in verdict.reason


def test_a_foreign_directory_path_is_refused_too():
    verdict = _verify(NAMES_A_FOREIGN_DIRECTORY)
    assert isinstance(verdict, kn.AbstractRefused)
    assert verdict.code == kn.ABSTRACT_REFUSED_FOREIGN_PATH


def test_naming_the_wrong_subject_is_refused():
    """The wrong-document answer and the leak are the same bytes-decidable
    fact — a path the request did not carry — and one rule refuses both."""
    verdict = _verify(NAMES_THE_WRONG_SUBJECT)
    assert isinstance(verdict, kn.AbstractRefused)
    assert verdict.code == kn.ABSTRACT_REFUSED_FOREIGN_PATH


def test_an_abstract_naming_neither_a_path_nor_a_title_is_refused():
    verdict = _verify(NAMES_NO_SUBJECT_AT_ALL)
    assert isinstance(verdict, kn.AbstractRefused)
    assert verdict.code == kn.ABSTRACT_REFUSED_SUBJECT_NOT_NAMED


def test_an_ordinary_slash_pair_is_not_a_repository_path():
    """`read/write` is not a leak. A path rule that refused ordinary prose would
    be turned off by its first false refusal."""
    abstract = _verify(ORDINARY_SLASH_PAIRS)
    assert isinstance(abstract, kn.DocumentAbstract)


def test_a_path_the_request_did_carry_is_not_foreign():
    verdict = _verify(NAMES_A_FOREIGN_PATH,
                      request_paths=(SUBJECT_PATH, NEIGHBOUR_PATH))
    assert isinstance(verdict, kn.DocumentAbstract)


# ===========================================================================
# 4.4 — A FAILURE RENDERS NOTHING AND STATES A REFUSAL
# ===========================================================================


def test_a_refusal_carries_no_field_that_could_render_the_unverified_text():
    """The strongest available form of "never silently downgraded": the refused
    bytes do not leave the verifier, so no renderer COULD show them."""
    verdict = _verify(NAMES_A_FOREIGN_PATH)
    names = {field.name for field in dataclasses.fields(kn.AbstractRefused)}
    for forbidden in ("prose", "abstract", "text", "body", "unverified",
                      "content", "answer"):
        assert forbidden not in names, forbidden
    assert NAMES_A_FOREIGN_PATH not in repr(verdict)
    assert not isinstance(verdict, kn.DocumentAbstract)


def test_every_refusal_class_states_a_code_and_a_reason():
    for seeded in (NO_DECLARED_SUBJECT_MENTIONED, NAMES_A_FOREIGN_PATH,
                   NAMES_THE_WRONG_SUBJECT, NAMES_NO_SUBJECT_AT_ALL, "  "):
        verdict = _verify(seeded)
        assert isinstance(verdict, kn.AbstractRefused)
        assert verdict.code in kn.ABSTRACT_REFUSAL_CODES
        assert verdict.reason.strip()
        assert verdict.subject_path == SUBJECT_PATH


def test_a_refusal_shows_the_not_yet_generated_caption_not_a_new_one():
    verdict = _verify(NAMES_NO_SUBJECT_AT_ALL)
    assert verdict.caption_state == kn.CAPTION_NOT_YET_GENERATED


def test_verification_returns_one_of_exactly_two_types():
    """No third "unverified" shape exists for a caller to reach for."""
    assert isinstance(_verify(COVERED), kn.DocumentAbstract)
    assert isinstance(_verify(NAMES_NO_SUBJECT_AT_ALL), kn.AbstractRefused)
    assert not issubclass(kn.AbstractRefused, kn.DocumentAbstract)
    assert not issubclass(kn.DocumentAbstract, kn.AbstractRefused)


def test_the_refusal_is_a_returned_value_and_a_caller_defect_is_an_exception():
    """A model that answered badly is not a programming error; a caller handing
    the verifier a non-string is. The two must not arrive by the same route."""
    assert isinstance(_verify(NAMES_NO_SUBJECT_AT_ALL), kn.AbstractRefused)
    with pytest.raises(kn.AbstractFormatRefused):
        _verify(object())


# ===========================================================================
# 4.5 — THE CHECK IS NAMED, AND IT IS NOT NAMED FIDELITY
# ===========================================================================


def test_the_check_is_named_subject_mention_coverage_in_the_code():
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert "subject-mention coverage" in source
    # and the reason it is NOT fidelity is stated where the check is written,
    # with its citation: one opaque string comes back from `dispatch_turn`.
    assert "NOT a fidelity check" in source
    assert "doxbench_model.py:985" in source


def test_no_public_name_claims_fidelity_or_faithfulness():
    public = {name for name in vars(kn) if not name.startswith("_")}
    for name in public:
        lowered = name.lower()
        for forbidden in ("fidelity", "faithful", "accuracy", "verified_true"):
            assert forbidden not in lowered, name


def test_the_refusal_reason_says_coverage_and_never_says_fidelity():
    verdict = _verify(NO_DECLARED_SUBJECT_MENTIONED)
    assert "coverage" in verdict.reason.lower()
    for forbidden in ("fidelity", "faithful", "accurate"):
        assert forbidden not in verdict.reason.lower()


def test_the_verifier_takes_a_dispatch_result_and_never_a_turn_or_a_prompt():
    """This module's standing rule (`doxbench_knowledge.py:39-42`): no function
    here takes a turn, a message, or a prompt, asserted against the SIGNATURE."""
    parameters = inspect.signature(kn.verify_document_abstract).parameters
    assert "dispatch_result" in parameters
    for forbidden in ("turn", "prompt", "message", "envelope", "transcript",
                      "packet", "buffer"):
        assert forbidden not in parameters, forbidden


def test_the_five_ruled_caption_states_are_exposed_for_the_route_and_renderer():
    """Ruling 5's five captions, as an enum the surfaces share rather than five
    string literals that drift apart."""
    assert kn.CAPTION_STATES == (
        kn.CAPTION_MODEL_DERIVED,
        kn.CAPTION_DETERMINISTIC,
        kn.CAPTION_STALE,
        kn.CAPTION_NOT_YET_GENERATED,
        kn.CAPTION_HOSTED_PLANE,
    )
    assert len(set(kn.CAPTION_STATES)) == 5
    assert set(kn.RULED_CAPTIONS) == set(kn.CAPTION_STATES)
    for state, caption in kn.RULED_CAPTIONS.items():
        assert caption.strip(), state
    # the load-bearing rule under all five: who derived it, and what it is not
    assert "not authoritative" in kn.RULED_CAPTIONS[kn.CAPTION_MODEL_DERIVED]
    assert "regenerable" in kn.RULED_CAPTIONS[kn.CAPTION_MODEL_DERIVED]
    assert "headers" in kn.RULED_CAPTIONS[kn.CAPTION_DETERMINISTIC]
    assert "distil" not in kn.RULED_CAPTIONS[kn.CAPTION_DETERMINISTIC].lower()
    assert "plane" in kn.RULED_CAPTIONS[kn.CAPTION_HOSTED_PLANE]


def test_no_caption_implies_the_abstract_may_be_cited():
    for state, caption in kn.RULED_CAPTIONS.items():
        lowered = caption.lower()
        for forbidden in ("of record", "authoritative account", "citable",
                          "ai-powered", "source of truth"):
            assert forbidden not in lowered, (state, forbidden)


def test_a_moved_on_subject_is_stale_rather_than_current_or_discarded():
    """Ruling 3: an abstract whose subject has moved past its digest is SHOWN and
    LABELLED, and the label is the ruled state rather than an invented one."""
    abstract = _verify(COVERED)
    assert abstract.caption_state_for(
        current_digest=DIGEST) == kn.CAPTION_MODEL_DERIVED
    assert abstract.caption_state_for(
        current_digest=OTHER_DIGEST) == kn.CAPTION_STALE


# ===========================================================================
# 4.6 — THE SIBLING DID NOT TAKE LAYER TWO'S OWNERSHIP
# ===========================================================================


def test_layer_two_still_names_compact_thread_as_its_owner():
    """Design D4, asserted rather than assumed. `CompressionLayer.owner` is a
    ONE-owner field, so a sibling layer-2-class artifact that edited it would
    degrade the fidelity checker to a comment."""
    assert pk.layer(2).owner == "doxbench_threads.compact_thread"
    assert callable(dt.compact_thread)


def test_the_fidelity_checker_still_refuses_a_wrong_claim_about_layer_two():
    with pytest.raises(pk.FidelityClaimRefused):
        pk.assert_fidelity(2, pk.FIDELITY_LOSSLESS_BY_REFERENCE)
    pk.assert_fidelity(2, pk.FIDELITY_LOSSY_BY_DESIGN)


def test_the_sibling_added_no_fourth_layer_and_owns_none_of_the_three():
    assert len(pk.COMPRESSION_LAYERS) == 3
    for row in pk.COMPRESSION_LAYERS:
        assert "doxbench_knowledge" not in row.owner
        assert "abstract" not in row.owner.lower()


def test_the_abstract_is_a_layer_2_class_sibling_not_a_thread():
    """It is not `DocumentThread` reused: that type fixes `regenerable_from` to
    the transcript (`doxbench_threads.py:593`) and its refusal rule keys on
    evidence refs and pending actions a document abstract has none of."""
    assert kn.REGENERABLE_FROM_DOCUMENT != dt.REGENERABLE_FROM_TRANSCRIPT
    assert kn.NON_AUTHORITATIVE == dt.NON_AUTHORITATIVE
    assert not isinstance(_abstract(), dt.DocumentThread)
    abstract_fields = {field.name
                       for field in dataclasses.fields(kn.DocumentAbstract)}
    assert "turns" not in abstract_fields
    assert "state" not in abstract_fields
