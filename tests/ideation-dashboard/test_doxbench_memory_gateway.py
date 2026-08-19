"""doxBench's `memory-gateway` conformance DECLARATION — the subject-free local
consumer class, asserted as an executable artifact rather than read as prose
(add-doxbench-editing-phase-b, design §7.1; the `memory-gateway` delta's
`Subject-Free Local Consumers Declare Their Inapplicable Rails`).

Every scenario of that requirement has a test here, and three of them are
CONSTRUCTIVE rather than descriptive: a consumer holding a provider credential,
addressing a customer subject, or routing to a networked provider never obtains
a declaration at all, and one that acquires any of them loses the one it had.

The declaration is also tied to the REALIZATION here rather than to its own
prose: the facts it asserts about this surface (no credential, no network, no
graph, rails before I/O, one promotion act) are each checked against the module
that actually implements them, because a declaration nobody cross-examines is
the unnamed absence the class exists to replace.
"""

from __future__ import annotations

import inspect
import re

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import doxbench_knowledge as kn  # noqa: E402
from ideation_dashboard import doxbench_memory_gateway as mg  # noqa: E402
from ideation_dashboard import doxbench_packet as pk  # noqa: E402
from ideation_dashboard import doxbench_telemetry as tel  # noqa: E402

MODULE_PATH = (REPO_ROOT / "scripts" / "ideation_dashboard"
               / "doxbench_memory_gateway.py")
SPEC_PATH = REPO_ROOT / "openspec" / "specs" / "memory-gateway" / "spec.md"


# ===========================================================================
# THE ROSTER — transcribed, and asserted against the capability itself
# ===========================================================================


def test_the_roster_is_exactly_the_promoted_capabilitys_requirements():
    """The declaration is only complete if the roster it is complete OVER is
    the capability's own. Read from the promoted spec, so a requirement added
    upstream fails here rather than becoming a silent gap in the declaration."""
    published = {
        line[len("### Requirement: "):].strip()
        for line in SPEC_PATH.read_text(encoding="utf-8").splitlines()
        if line.startswith("### Requirement: ")
    }
    assert published == set(mg.CAPABILITY_REQUIREMENTS)


def _published_tiers() -> dict[str, str]:
    """The spec's OWN tier block, parsed: requirement name -> the tier line it
    is named on."""
    spec = SPEC_PATH.read_text(encoding="utf-8")
    block = spec.split("```text", 1)[1].split("```", 1)[0]
    published: dict[str, str] = {}
    for match in re.finditer(r"(M\d):((?:.|\n)*?)(?=\nM\d:|\Z)", block):
        tier, body = match.group(1), " ".join(match.group(2).split())
        for name in body.split(";"):
            published[name.strip().rstrip(".")] = tier
    return published


def test_the_tier_column_is_TRANSCRIBED_not_invented():
    """RE-PINNED (adversarial review, F7). The roster test checked NAMES only,
    so two wrong tier values sat in the column unchallenged: one requirement
    carried `M0` although the spec's tier block never tiers it at all, and
    `Expert Memory And Knowledge DBs Are Gateway-Governed` was FLATTENED to
    `M4` although the spec says in as many words that it follows the tier of
    the operation it mirrors. Both are now transcribed, and this test reads the
    spec's own block so neither error can recur silently."""
    published = _published_tiers()
    for requirement, declared in mg.CAPABILITY_REQUIREMENTS.items():
        named = [line for line in published
                 if line.lower().startswith(requirement.lower())]
        if not named:
            # Not tiered by the spec at all -- which the column must SAY.
            assert declared == mg.TIER_UNTIERED, requirement
            continue
        line = named[0]
        if line != requirement:
            # The spec qualifies this row rather than tiering it outright.
            assert declared == mg.TIER_MIRRORS_OPERATION, requirement
            assert "follows the tier of the operation it mirrors" in line
            continue
        assert declared == published[line], requirement


def test_the_untiered_requirement_really_is_absent_from_the_tier_block():
    published = _published_tiers()
    untiered = [name for name, tier in mg.CAPABILITY_REQUIREMENTS.items()
                if tier == mg.TIER_UNTIERED]
    assert untiered == [
        "Derived memory bindings validate against the neutral schema"]
    for name in untiered:
        assert not any(line.lower().startswith(name.lower())
                       for line in published)


def test_every_requirement_carries_a_disposition_and_a_reason():
    declared = mg.DECLARATION.by_requirement()
    assert set(declared) == set(mg.CAPABILITY_REQUIREMENTS)
    for requirement, row in declared.items():
        assert row.disposition in mg.DISPOSITIONS, requirement
        assert row.reason.strip(), requirement


def test_an_incomplete_declaration_is_refused_rather_than_read_as_a_pass():
    """The delta's `A declared rail is skipped without being named` scenario:
    a consumer that does not name a rail it is not running fails validation."""
    short = tuple(row for row in mg.DOXBENCH_DISPOSITIONS
                  if row.requirement != "Consent Profiles Are A First-Class Contract")
    with pytest.raises(mg.DeclarationRefused) as raised:
        mg.declare_subject_free_local_consumer(
            mg.DOXBENCH_SHAPE, dispositions=short,
            promotion_act=mg.DOXBENCH_PROMOTION_ACT)
    assert "Consent Profiles Are A First-Class Contract" in str(raised.value)
    assert "never infers it from silence" in str(raised.value)


def test_a_disposition_without_a_reason_is_refused():
    with pytest.raises(mg.DeclarationRefused):
        mg.RequirementDisposition("Erasure Is Distinct From Revocation",
                                  mg.INAPPLICABLE, "   ")


def test_the_same_requirement_may_not_be_dispositioned_twice():
    doubled = mg.DOXBENCH_DISPOSITIONS + (
        mg.RequirementDisposition("Erasure Is Distinct From Revocation",
                                  mg.REALIZED, "a second answer"),)
    with pytest.raises(mg.DeclarationRefused) as raised:
        mg.declare_subject_free_local_consumer(
            mg.DOXBENCH_SHAPE, dispositions=doubled,
            promotion_act=mg.DOXBENCH_PROMOTION_ACT)
    assert "two answers to one requirement is no answer" in str(raised.value)


@pytest.mark.parametrize("requirement", mg.NEVER_INAPPLICABLE)
def test_the_declaration_may_not_reduce_what_remains_applicable(requirement):
    """"The declaration SHALL NOT reduce what remains applicable" — expressed
    as a refusal, so the seven requirements that always bind cannot be
    declared away by any consumer of the class."""
    with pytest.raises(mg.DeclarationRefused) as raised:
        mg.RequirementDisposition(requirement, mg.INAPPLICABLE, "convenient")
    assert "does not reduce what remains applicable" in str(raised.value)


def test_the_declared_class_names_every_inapplicable_rail_with_its_reason():
    """The delta's first scenario: consent, subject safety, provider bindings
    and grants, and provider mapping are named inapplicable WITH the reason."""
    named = dict(mg.DECLARATION.inapplicable_rails())
    for rail in ("Consent Profiles Are A First-Class Contract",
                 "Subject Safety Rail Handles Adult And Minor Subjects",
                 "Provider Access Uses Bindings And Short-Lived Grants",
                 "Memory Provider Mapping Is Traceable"):
        assert rail in named, rail
        assert len(named[rail].split()) >= 8, rail


# ===========================================================================
# THE THREE REFUSAL CONDITIONS — constructive, not annotated
# ===========================================================================


@pytest.mark.parametrize("field,needle", [
    ("holds_provider_credential", "provider credential"),
    ("addresses_customer_subject", "customer subject"),
    ("routes_to_networked_provider", "networked provider"),
])
def test_a_disqualified_consumer_never_obtains_the_declaration(field, needle):
    shape = mg.ConsumerShape(consumer="a different consumer", **{field: True})
    with pytest.raises(mg.DeclarationRefused) as raised:
        mg.declare_subject_free_local_consumer(
            shape, dispositions=mg.DOXBENCH_DISPOSITIONS,
            promotion_act=mg.DOXBENCH_PROMOTION_ACT)
    assert needle in str(raised.value)
    assert "the full tier applies" in str(raised.value)


@pytest.mark.parametrize("field", ["holds_provider_credential",
                                   "addresses_customer_subject",
                                   "routes_to_networked_provider"])
def test_a_consumer_that_acquires_one_LOSES_the_declaration(field):
    """The delta's third scenario. A loss, not a warning: the previously
    declared inapplicability MUST NOT survive as a standing exemption, so
    `revalidate` raises rather than returning an annotated declaration."""
    acquired = mg.ConsumerShape(consumer=mg.CONSUMER, **{field: True})
    with pytest.raises(mg.DeclarationLost) as raised:
        mg.revalidate(mg.DECLARATION, acquired)
    assert "loses the" in str(raised.value)
    assert "satisfy the applicable tier before continuing" in str(raised.value)


def test_revalidating_an_unchanged_shape_keeps_the_declaration():
    kept = mg.revalidate(mg.DECLARATION, mg.DOXBENCH_SHAPE)
    assert kept.dispositions == mg.DECLARATION.dispositions
    assert kept.shape == mg.DOXBENCH_SHAPE


# ===========================================================================
# CONFORMANCE IS READ, NEVER INFERRED
# ===========================================================================


def test_conformance_is_refused_when_there_is_no_declaration_to_read():
    """The delta's last scenario: a consumer presenting no declaration and no
    failing rail is NOT conformant by default."""
    with pytest.raises(mg.ConformanceNotDeclared) as raised:
        mg.assess_conformance(None)
    assert "never inferred from silence" in str(raised.value)


def test_the_reading_never_claims_a_whole_tier():
    reading = mg.assess_conformance(mg.DECLARATION)
    assert reading.claims_whole_tier() is False
    assert "Usage Metering Is Gateway-Owned" in reading.partial
    assert "Promotions Are Explicit And Reviewed" in reading.narrowed
    # RE-VERIFY NF1: pinned BY NAME. This disposition was corrected from
    # REALIZED to NARROWED by the adversarial review (F4) — and nothing failed
    # when it was flipped back, because no test named it. The correction is a
    # claim about what this surface does NOT do, which is exactly the kind that
    # rots silently unless something asserts it.
    assert "Gateway Conformance Is Testable" in reading.narrowed
    assert "Gateway Conformance Is Testable" not in reading.realized
    assert "Rails Run Before Provider I/O" in reading.realized
    # No tier is claimed whole, and M0 is the one that would be tempting: it
    # holds inapplicable requirements alongside realized ones.
    m0 = {name for name, tier in mg.CAPABILITY_REQUIREMENTS.items()
          if tier == mg.TIER_M0}
    assert m0 & set(reading.inapplicable)
    assert m0 & set(reading.realized)


def test_the_declaration_serializes_to_plain_auditable_data():
    data = mg.DECLARATION.as_dict()
    assert data["capability"] == "memory-gateway"
    assert data["consumer_class"] == mg.CONSUMER_CLASS
    assert len(data["dispositions"]) == len(mg.CAPABILITY_REQUIREMENTS)
    assert data["promotion_act"]["verb"] == "create-document"


# ===========================================================================
# THE DECLARATION IS TIED TO THE REALIZATION, not to its own prose
# ===========================================================================


def test_the_promotion_act_is_the_one_the_tool_boundary_actually_routes_to():
    """"the declaration SHALL name that act" — and the tool that promotes reads
    it from HERE, so the two cannot say different things."""
    backend = kn.build_backend(kn.SELF_HOSTED_LOCAL_EMBEDDED)
    boundary = kn.KnowledgeToolBoundary(backend)
    request = boundary.promote_finding("the topic needs a delta type",
                                       provenance=("ideation/staging/t/t.md",))
    assert request.act_verb == mg.DECLARATION.promotion_act.verb
    assert request.act_review == mg.DECLARATION.promotion_act.review


def test_the_no_credential_and_no_network_claims_hold_of_the_v1_profile():
    profile = kn.LOCAL_EMBEDDED_PROFILE
    assert profile.credentialed is False
    assert profile.networked is False
    assert profile.graph is False
    assert mg.DOXBENCH_SHAPE.holds_provider_credential is False
    assert mg.DOXBENCH_SHAPE.routes_to_networked_provider is False


def test_the_partial_metering_claim_matches_the_telemetry_absences():
    """`Usage Metering Is Gateway-Owned` is declared PARTIAL because four
    fields have no value here. The telemetry module declares exactly those
    four, so the claim is checkable rather than a hedge."""
    row = mg.DECLARATION.by_requirement()["Usage Metering Is Gateway-Owned"]
    assert row.disposition == mg.PARTIAL
    assert set(tel.declared_absences()) == {
        "client", "domain", "bill_to", "customer_subject_ref"}
    for named in ("client", "domain", "bill-to"):
        assert named in row.reason.lower(), named
    # every declared absence carries a REASON, which is the auditable half
    for field, reason in tel.declared_absences().items():
        assert reason.strip(), field


def test_the_rails_before_io_claim_names_rails_this_surface_really_runs():
    """The realized claim is checked against the assembler's own public rails
    rather than against the sentence that makes it."""
    row = mg.DECLARATION.by_requirement()["Rails Run Before Provider I/O"]
    assert row.disposition == mg.REALIZED
    for rail in ("confined_refs", "exemption_rail", "bounds_rail"):
        assert callable(getattr(pk, rail)), rail


# ===========================================================================
# NEGATIVE SPACE
# ===========================================================================

_FORBIDDEN_MODULE_NEEDLES = [
    # a declaration declares; it never implements a rail, reaches a provider,
    # or carries a credential
    ("import os", "an os import"),
    ("open(", "a direct file open"),
    ("subprocess", "a subprocess invocation"),
    ("urllib", "a network client"),
    ("socket", "a network socket"),
    ("requests", "an HTTP client"),
    ("api_key", "a credential field"),
    ("os.environ", "an environment read a credential could arrive through"),
]
# `endpoint`, `credential` and `subject` DO appear in this module — inside the
# REASONS that say why each is inapplicable, which is the artifact's whole
# point. So the negative for those three is asserted against the PUBLIC
# SURFACE below rather than against the text, where a field named for one would
# actually be a defect.


@pytest.mark.parametrize("needle,label", _FORBIDDEN_MODULE_NEEDLES,
                         ids=[needle for needle, _ in _FORBIDDEN_MODULE_NEEDLES])
def test_the_declaration_module_contains_no_forbidden_spelling(needle, label):
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert needle not in source, (
        f"doxbench_memory_gateway.py must not contain {label}: {needle!r}")


def test_the_module_exposes_no_exemption_or_waiver_callable():
    """The class "grants no exemption and relaxes no rail" — asserted against
    the public surface, because that is where a helpful waiver would appear."""
    public = {name for name in vars(mg) if not name.startswith("_")}
    for name in public:
        lowered = name.lower()
        assert "exempt" not in lowered, name
        assert "waive" not in lowered, name
        assert "override" not in lowered, name
        # and no CARRIER for the three things whose absence is being declared
        assert "endpoint" not in lowered, name
        assert "credential_value" not in lowered, name
        assert not lowered.startswith("subject_id"), name


def test_the_declaration_is_built_through_the_refusing_constructor():
    """The module's own declaration goes through the same gate any other
    consumer's would, so it cannot hold one its rules would have refused."""
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert "DECLARATION = declare_subject_free_local_consumer(" in source
    assert isinstance(mg.DECLARATION, mg.SubjectFreeLocalConsumerDeclaration)
    assert "shape" in inspect.signature(
        mg.declare_subject_free_local_consumer).parameters
