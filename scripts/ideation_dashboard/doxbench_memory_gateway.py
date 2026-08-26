"""doxBench's `memory-gateway` conformance DECLARATION — the subject-free local
consumer class, expressed as a machine-readable artifact rather than as prose
(add-doxbench-editing-phase-b, design §7.1; the `memory-gateway` delta's
`Subject-Free Local Consumers Declare Their Inapplicable Rails`).

The capability's M0 set is written for consumers that have a CUSTOMER SUBJECT
and a CREDENTIALED PROVIDER. This surface has neither: it assembles bounded
context packets over its own repository corpus behind an in-process local
index, with no subject anywhere in its path and no credential anywhere near it.
The contract's own delta creates a third option for exactly that consumer — one
that names every rail it declares inapplicable AND WHY, grants no exemption,
relaxes no rail, and is REFUSED to any consumer that holds a provider
credential, addresses a customer subject, or routes to a networked provider.

This module is that declaration, and it is DATA a reader can execute:

  * ``CAPABILITY_REQUIREMENTS`` is the capability's own requirement roster with
    its published tiers, transcribed from ``openspec/specs/memory-gateway/``.
  * ``DECLARATION`` is THIS surface's declaration over that roster: every
    requirement carries a disposition and a reason, because the delta's last
    scenario says conformance validation reads the declaration and never infers
    it from silence — so a requirement nobody mentioned is a validation
    FAILURE here rather than a quiet pass.
  * ``declare_subject_free_local_consumer`` refuses a consumer SHAPE that holds
    a credential, addresses a subject, or routes to a networked provider, and
    ``revalidate`` LOSES an existing declaration the moment a shape acquires
    one. The refusal is constructive: there is no path that produces a
    declaration for such a consumer and then annotates it.

WHAT IS NOT HERE: no rail implementation, no provider, no packet, and no
retrieval. This module declares what this surface's OTHER modules must do; the
rails run in ``doxbench_packet``, the provider profile lives in
``doxbench_knowledge``, and the metering shape in ``doxbench_telemetry``. A
declaration that also implemented a rail would be a declaration nobody could
audit against an independent realization.

Stdlib only, pure, and no I/O of any kind — a companion test greps this module
for every provider, credential, and network spelling it must not contain.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Mapping, Sequence

CAPABILITY = "memory-gateway"

# The class the `memory-gateway` delta adds, spelled once.
CONSUMER_CLASS = "subject-free local consumer"

# ---------------------------------------------------------------------------
# the capability's own roster (transcribed from openspec/specs/memory-gateway/)
# ---------------------------------------------------------------------------

TIER_M0 = "M0"
TIER_M1 = "M1"
TIER_M2 = "M2"
TIER_M3 = "M3"
TIER_M4 = "M4"

# TWO VALUES THAT ARE NOT TIERS, and both are transcriptions rather than
# inventions (adversarial review, F7). The column used to carry a plain tier
# for each, which was wrong in two different ways: one requirement was given a
# tier the spec's own tier block never assigns it, and one was FLATTENED to a
# single tier the spec explicitly refuses to flatten.
#
# A companion test asserts every value here against the spec's tier block, so
# neither error can recur silently.
TIER_UNTIERED = "untiered"
TIER_MIRRORS_OPERATION = (
    "follows the tier of the operation it mirrors "
    "(rails at M0, promotion at M1, migration at M4)")

# Every requirement the promoted capability publishes, with the tier its own
# spec header assigns it. Transcribed rather than inferred, and asserted against
# the spec file itself by a companion test, so a requirement added upstream
# turns into a failing test here rather than into a silent gap in the
# declaration below.
CAPABILITY_REQUIREMENTS: Mapping[str, str] = {
    "Gateway Mediates Governed Memory Access": TIER_M0,
    "Canonical Ports Are Product Neutral": TIER_M0,
    "Provider Profiles Declare Capability": TIER_M0,
    "Expert Memory And Knowledge DBs Are Gateway-Governed": TIER_MIRRORS_OPERATION,
    "Rails Run Before Provider I/O": TIER_M0,
    "Provider Access Uses Bindings And Short-Lived Grants": TIER_M0,
    "Subject Safety Rail Handles Adult And Minor Subjects": TIER_M2,
    "Context Packets Bound Runtime Memory": TIER_M0,
    "Customer Memory Fill And Maintenance Modes Are Canonical": TIER_M1,
    "Promotions Are Explicit And Reviewed": TIER_M1,
    "Revocation And Tombstones Preserve Audit": TIER_M1,
    "Usage Metering Is Gateway-Owned": TIER_M3,
    "Memory Migration Preserves Hermes Continuity": TIER_M4,
    "Memory Provider Mapping Is Traceable": TIER_M0,
    "Worker-Local Memory Remains Separate": TIER_M1,
    "Gateway Callers Are Authenticated And Hold No Provider Credentials": TIER_M0,
    "Consent Profiles Are A First-Class Contract": TIER_M0,
    "Fail Modes Are Explicit And Break-Glass Is Audited": TIER_M0,
    "Erasure Is Distinct From Revocation": TIER_M1,
    "Gateway Conformance Is Testable": TIER_M0,
    "Derived memory bindings validate against the neutral schema": TIER_UNTIERED,
    # PROMOTED 2026-08-22 by add-doxbench-editing-phase-b's own archive: this is
    # the requirement THIS change added to the capability to describe what this
    # surface does, so the roster grew the moment the delta promoted. UNTIERED
    # because the spec's tier block does not tier it (checked, not assumed — a
    # companion test asserts its absence there).
    "Subject-Free Local Consumers Declare Their Inapplicable Rails":
        TIER_UNTIERED,
}

# The dispositions a declaration may give a requirement. There is deliberately
# no `unknown` and no `deferred`: the whole point of the class is that an
# absence is a recorded decision.
REALIZED = "realized"
NARROWED = "narrowed"
PARTIAL = "partial"
INAPPLICABLE = "inapplicable"
DISPOSITIONS: tuple[str, ...] = (REALIZED, NARROWED, PARTIAL, INAPPLICABLE)

# What the delta says a declaration SHALL NOT reduce. These requirements may
# never be declared inapplicable by ANY subject-free consumer, because the class
# exists to make an absence auditable, not to shrink the applicable set.
NEVER_INAPPLICABLE: tuple[str, ...] = (
    "Gateway Mediates Governed Memory Access",
    "Canonical Ports Are Product Neutral",
    "Provider Profiles Declare Capability",
    "Rails Run Before Provider I/O",
    "Context Packets Bound Runtime Memory",
    "Worker-Local Memory Remains Separate",
    "Promotions Are Explicit And Reviewed",
)


# ---------------------------------------------------------------------------
# refusals
# ---------------------------------------------------------------------------


class MemoryGatewayDeclarationError(ValueError):
    """Base class for every refusal this module raises."""


class DeclarationRefused(MemoryGatewayDeclarationError):
    """Raised when a consumer's SHAPE may not hold the class at all, or when a
    declaration over that shape is incomplete or reduces the applicable set."""


class DeclarationLost(MemoryGatewayDeclarationError):
    """Raised when a consumer that HELD the declaration acquires a provider
    credential, a networked provider route, or a customer-subject scope. The
    previously declared inapplicability does not survive as a standing
    exemption, so this is a loss rather than a warning."""


class ConformanceNotDeclared(MemoryGatewayDeclarationError):
    """Raised when conformance is asked for with no declaration to read. A tier
    claim is read from a declaration, never from the absence of a complaint."""


# ---------------------------------------------------------------------------
# the consumer shape the class is granted to, or refused
# ---------------------------------------------------------------------------

CREDENTIAL_REFUSAL = (
    "a consumer that holds or can read a provider credential does not hold the "
    "subject-free local consumer class: for it the full tier applies"
)
SUBJECT_REFUSAL = (
    "a consumer that addresses a customer subject does not hold the "
    "subject-free local consumer class: for it the full tier applies"
)
NETWORK_REFUSAL = (
    "a consumer that routes to a networked provider does not hold the "
    "subject-free local consumer class: for it the full tier applies"
)


@dataclasses.dataclass(frozen=True, slots=True)
class ConsumerShape:
    """The three facts the delta makes the class conditional on, carried as
    DATA so the refusal can be constructive.

    Every field defaults to the disqualifying answer's opposite only because
    that is what this surface is; a caller states all three explicitly at the
    one place the declaration is built, and ``revalidate`` re-asks them."""

    consumer: str
    holds_provider_credential: bool = False
    addresses_customer_subject: bool = False
    routes_to_networked_provider: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.consumer, str) or not self.consumer.strip():
            raise DeclarationRefused("a declaration names its consumer")
        for field in ("holds_provider_credential", "addresses_customer_subject",
                      "routes_to_networked_provider"):
            if not isinstance(getattr(self, field), bool):
                raise DeclarationRefused(f"{field} is a boolean fact, not a hint")

    def disqualifications(self) -> tuple[str, ...]:
        """Every reason this shape may not hold the class, in a fixed order."""
        reasons: list[str] = []
        if self.holds_provider_credential:
            reasons.append(CREDENTIAL_REFUSAL)
        if self.addresses_customer_subject:
            reasons.append(SUBJECT_REFUSAL)
        if self.routes_to_networked_provider:
            reasons.append(NETWORK_REFUSAL)
        return tuple(reasons)


# ---------------------------------------------------------------------------
# the promotion act, named rather than assumed
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True, slots=True)
class PromotionAct:
    """The REVIEWED act that satisfies `Promotions Are Explicit And Reviewed`
    where the promotion target is not a Hermes memory layer.

    The delta is exact about this: "the promotion requirement SHALL be
    satisfied by the reviewed act that creates the target object, and the
    declaration SHALL name that act — promotion stays explicit and reviewed,
    and what changes is the target, never the gate." So the act is a FIELD, and
    the surface that promotes reads it from here rather than restating it."""

    verb: str
    review: str
    reason: str

    def __post_init__(self) -> None:
        for field in ("verb", "review", "reason"):
            value = getattr(self, field)
            if not isinstance(value, str) or not value.strip():
                raise DeclarationRefused(
                    f"the promotion act names its {field}")


# The act on THIS surface: a finding becomes durable by a human creating the
# target object through the governed `create-document` gate action — the same
# one-commit-per-gate-action path every other document takes — and that commit
# reaches review through the session's pull request. No automatic durability
# exists anywhere in this path, and no parallel decision store is created.
DOXBENCH_PROMOTION_ACT = PromotionAct(
    verb="create-document",
    review="the session pull request that carries the created object",
    reason=(
        "this consumer's promotion target is a document in the lifecycle — an "
        "idea note, a fragment, or a disposition on the topic — and not a "
        "Hermes memory layer, so the reviewed act that CREATES that object is "
        "what satisfies the promotion requirement; the gate is unchanged and "
        "only the target differs"),
)


# ---------------------------------------------------------------------------
# the declaration
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True, slots=True)
class RequirementDisposition:
    """One requirement's disposition and the reason for it. The reason is
    REQUIRED for every disposition, not only the inapplicable ones: a
    requirement claimed as realized without saying by what is the same
    unauditable assertion in the other direction."""

    requirement: str
    disposition: str
    reason: str

    def __post_init__(self) -> None:
        if self.requirement not in CAPABILITY_REQUIREMENTS:
            raise DeclarationRefused(
                f"{self.requirement!r} is not a requirement of {CAPABILITY}")
        if self.disposition not in DISPOSITIONS:
            raise DeclarationRefused(
                f"{self.disposition!r} is not one of {DISPOSITIONS}")
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise DeclarationRefused(
                f"{self.requirement!r} is dispositioned without a reason; an "
                "unexplained disposition is the unnamed absence this class "
                "exists to replace")
        if (self.disposition == INAPPLICABLE
                and self.requirement in NEVER_INAPPLICABLE):
            raise DeclarationRefused(
                f"{self.requirement!r} may not be declared inapplicable: the "
                "class names absences, it does not reduce what remains "
                "applicable")

    @property
    def tier(self) -> str:
        return CAPABILITY_REQUIREMENTS[self.requirement]


@dataclasses.dataclass(frozen=True, slots=True)
class SubjectFreeLocalConsumerDeclaration:
    """A complete, machine-readable declaration of the class.

    COMPLETE is load-bearing: the roster is closed, and every requirement in it
    carries a disposition. Validation therefore reads this object; it never
    reads a shorter list and infers that the rest were fine."""

    shape: ConsumerShape
    consumer_class: str
    dispositions: tuple[RequirementDisposition, ...]
    promotion_act: PromotionAct

    def __post_init__(self) -> None:
        if self.consumer_class != CONSUMER_CLASS:
            raise DeclarationRefused(
                f"this module declares the {CONSUMER_CLASS!r} class")
        seen: dict[str, RequirementDisposition] = {}
        for row in self.dispositions:
            if not isinstance(row, RequirementDisposition):
                raise DeclarationRefused(
                    "dispositions are RequirementDisposition values")
            if row.requirement in seen:
                raise DeclarationRefused(
                    f"{row.requirement!r} is dispositioned twice; two answers "
                    "to one requirement is no answer")
            seen[row.requirement] = row
        missing = tuple(sorted(set(CAPABILITY_REQUIREMENTS) - set(seen)))
        if missing:
            raise DeclarationRefused(
                "every requirement of the capability carries a disposition; "
                f"undeclared: {', '.join(missing)} — conformance validation "
                "reads the declaration and never infers it from silence")

    # -- readers -----------------------------------------------------------

    def by_requirement(self) -> Mapping[str, RequirementDisposition]:
        return {row.requirement: row for row in self.dispositions}

    def with_disposition(self, disposition: str) -> tuple[str, ...]:
        return tuple(row.requirement for row in self.dispositions
                     if row.disposition == disposition)

    def inapplicable_rails(self) -> tuple[tuple[str, str], ...]:
        """Every rail declared inapplicable, WITH its reason — the pair the
        delta's first scenario asks a declaration to carry."""
        return tuple((row.requirement, row.reason) for row in self.dispositions
                     if row.disposition == INAPPLICABLE)

    def declared_tiers(self) -> Mapping[str, tuple[str, ...]]:
        """The dispositions grouped by the capability's published tier, so a
        reader can see at a glance that no tier is claimed WHOLE."""
        grouped: dict[str, list[str]] = {}
        for row in self.dispositions:
            grouped.setdefault(row.tier, []).append(
                f"{row.requirement}: {row.disposition}")
        return {tier: tuple(rows) for tier, rows in sorted(grouped.items())}

    def as_dict(self) -> dict[str, object]:
        """The declaration as plain data, for a report or a fixture. Carries no
        content of any kind — requirement names, dispositions, and reasons
        this module wrote itself."""
        return {
            "capability": CAPABILITY,
            "consumer": self.shape.consumer,
            "consumer_class": self.consumer_class,
            "promotion_act": {
                "verb": self.promotion_act.verb,
                "review": self.promotion_act.review,
                "reason": self.promotion_act.reason,
            },
            "dispositions": [
                {"requirement": row.requirement, "tier": row.tier,
                 "disposition": row.disposition, "reason": row.reason}
                for row in self.dispositions
            ],
        }


def declare_subject_free_local_consumer(
    shape: ConsumerShape,
    *,
    dispositions: Sequence[RequirementDisposition],
    promotion_act: PromotionAct,
) -> SubjectFreeLocalConsumerDeclaration:
    """Build the declaration, or REFUSE the shape.

    The refusal is the point and it is constructive: a consumer that holds a
    provider credential, addresses a customer subject, or routes to a networked
    provider never obtains an object it could later be asked to annotate."""

    if not isinstance(shape, ConsumerShape):
        raise DeclarationRefused("a declaration is made over a ConsumerShape")
    disqualified = shape.disqualifications()
    if disqualified:
        raise DeclarationRefused(
            f"{shape.consumer}: " + "; ".join(disqualified))
    return SubjectFreeLocalConsumerDeclaration(
        shape=shape,
        consumer_class=CONSUMER_CLASS,
        dispositions=tuple(dispositions),
        promotion_act=promotion_act,
    )


def revalidate(declaration: SubjectFreeLocalConsumerDeclaration,
               shape: ConsumerShape) -> SubjectFreeLocalConsumerDeclaration:
    """Re-ask the three questions of a consumer that already holds the class.

    A shape that has acquired any of them LOSES the declaration — it does not
    keep it with a note — and must satisfy the applicable tier before it may
    continue."""

    if not isinstance(declaration, SubjectFreeLocalConsumerDeclaration):
        raise DeclarationRefused("revalidate re-asks an existing declaration")
    if not isinstance(shape, ConsumerShape):
        raise DeclarationRefused("revalidate re-asks over a ConsumerShape")
    disqualified = shape.disqualifications()
    if disqualified:
        raise DeclarationLost(
            f"{shape.consumer} loses the {CONSUMER_CLASS} declaration and must "
            "satisfy the applicable tier before continuing: "
            + "; ".join(disqualified))
    return dataclasses.replace(declaration, shape=shape)


@dataclasses.dataclass(frozen=True, slots=True)
class ConformanceReading:
    """What a validator may say about this consumer after READING the
    declaration. It never says "conformant to M0": a subject-free consumer is
    not conformant to a tier whose requirements it declares inapplicable, so
    the reading states the tier's requirements one by one."""

    consumer: str
    consumer_class: str
    realized: tuple[str, ...]
    narrowed: tuple[str, ...]
    partial: tuple[str, ...]
    inapplicable: tuple[str, ...]

    def claims_whole_tier(self) -> bool:
        return False


def assess_conformance(
    declaration: SubjectFreeLocalConsumerDeclaration | None,
) -> ConformanceReading:
    """Read a declaration. With none to read, REFUSE rather than pass.

    This is the delta's last scenario expressed as code: a consumer presenting
    no declaration and no failing rail is not conformant by default, because a
    tier claim is read from a declaration and never from the absence of a
    complaint."""

    if declaration is None:
        raise ConformanceNotDeclared(
            f"no {CONSUMER_CLASS} declaration was presented: conformance is "
            "read from a declaration, never inferred from silence")
    if not isinstance(declaration, SubjectFreeLocalConsumerDeclaration):
        raise ConformanceNotDeclared(
            "conformance is read from a declaration of the declared class")
    return ConformanceReading(
        consumer=declaration.shape.consumer,
        consumer_class=declaration.consumer_class,
        realized=declaration.with_disposition(REALIZED),
        narrowed=declaration.with_disposition(NARROWED),
        partial=declaration.with_disposition(PARTIAL),
        inapplicable=declaration.with_disposition(INAPPLICABLE),
    )


# ---------------------------------------------------------------------------
# THIS SURFACE'S OWN DECLARATION (design §7.1)
# ---------------------------------------------------------------------------

CONSUMER = "doxBench staged-set knowledge service"

DOXBENCH_SHAPE = ConsumerShape(
    consumer=CONSUMER,
    # Each of these is a FACT about the realization, and each has an
    # independent test: the v1 retrieval profile is in-process and declares
    # itself credential-free and non-networked, and no surface anywhere in this
    # path names a customer subject.
    holds_provider_credential=False,
    addresses_customer_subject=False,
    routes_to_networked_provider=False,
)

_D = RequirementDisposition

DOXBENCH_DISPOSITIONS: tuple[RequirementDisposition, ...] = (
    _D("Gateway Mediates Governed Memory Access", REALIZED,
       "every governed read is routed through the staged-set knowledge "
       "service; no direct index or corpus read is treated as authoritative "
       "context, and the assembler is the only caller of a retrieval provider"),
    _D("Canonical Ports Are Product Neutral", REALIZED,
       "the internal ASSEMBLY PORT is the product-neutral surface a retrieval "
       "backend implements, separate from the caller-facing tool boundary, so "
       "a backend swap changes neither"),
    _D("Provider Profiles Declare Capability", REALIZED,
       "the v1 local-hybrid backend is expressed as a declared provider "
       "profile — capability declared, authority not granted — naming its "
       "signals, its bound, and that it is neither networked nor credentialed"),
    _D("Expert Memory And Knowledge DBs Are Gateway-Governed", INAPPLICABLE,
       "no Domain Omnigent expert and no external knowledge DB, vector "
       "service, graph store, or case store is in this path: the corpus is "
       "this repository's own staged set, read in-process, and delivered only "
       "as a bounded packet"),
    _D("Rails Run Before Provider I/O", REALIZED,
       "stated PRECISELY, because design §3.1's own step 2 both contains the "
       "evidence search AND is described as preceding every provider: the rail "
       "that GOVERNS the retrieval provider is the CONFINEMENT, and it is "
       "computed first and handed to that provider rather than applied to its "
       "answers afterwards; selection, the lifecycle-status exemption and the "
       "bounds fit all complete before the MODEL provider is reached; and the "
       "index the retrieval provider searches is built only from the tile's "
       "own staged set, so it is a subset of the confinement by construction. "
       "A refusal at any of them discloses no packet content"),
    _D("Provider Access Uses Bindings And Short-Lived Grants", INAPPLICABLE,
       "v1's provider is an in-process local index with no credential and no "
       "endpoint, so there is no binding to resolve and no grant to scope; an "
       "API-backed model or a hosted retrieval backend gets its credential "
       "from the ratified broker lane, which IS this mechanism, and declaring "
       "one loses this class"),
    _D("Subject Safety Rail Handles Adult And Minor Subjects", INAPPLICABLE,
       "no customer subject exists anywhere on this surface — the material is "
       "governance documents in a repository — so there is no subject to "
       "classify and no safety profile to apply"),
    _D("Context Packets Bound Runtime Memory", REALIZED,
       "per-turn context is a bounded context packet declaring purpose, the "
       "exact sources it carries with refs, its bound scope, and its expiry, "
       "and it is invalid for another purpose, another scope, or after expiry"),
    _D("Customer Memory Fill And Maintenance Modes Are Canonical", INAPPLICABLE,
       "there is no customer memory to fill or maintain: the corpus is a "
       "repository the surface reads and never a subject's memory"),
    _D("Promotions Are Explicit And Reviewed", NARROWED,
       "the RULE is realized — nothing durable without review, and no "
       "automatic path from raw chat to the corpus — while the requirement's "
       "layer vocabulary (customer memory moving into client or domain "
       "layers) does not apply, because this consumer's promotion target is a "
       "document in the lifecycle; the reviewed act is named in promotion_act"),
    _D("Revocation And Tombstones Preserve Audit", INAPPLICABLE,
       "revocation is consent-shaped, and with no subject and no consent "
       "profile there is nothing to revoke; the corpus's own history is git's, "
       "which this surface never rewrites"),
    _D("Usage Metering Is Gateway-Owned", PARTIAL,
       "per-turn and per-session telemetry is emitted content-free, but a "
       "self-hosted authoring console has no client, domain, or bill-to "
       "target — those fields are DECLARED absent with their reason rather "
       "than placeholder-filled, so this is compatibility, not conformance"),
    _D("Memory Migration Preserves Hermes Continuity", INAPPLICABLE,
       "there is no Hermes memory to migrate and no provider route to move; "
       "the derived index is regenerable from the repository at any time"),
    _D("Memory Provider Mapping Is Traceable", INAPPLICABLE,
       "provider mapping maps canonical Customer Hermes objects to provider "
       "refs; this surface holds no canonical Hermes object and its refs are "
       "repository-relative paths that need no mapping to be traced"),
    _D("Worker-Local Memory Remains Separate", REALIZED,
       "the sidecar thread files are the record: a harness's native memory "
       "never holds a thread, and where any harness-local memory is enabled "
       "it is non-authoritative and ranked last by the source hierarchy"),
    _D("Gateway Callers Are Authenticated And Hold No Provider Credentials",
       REALIZED,
       "the caller is the loopback console's resolved human actor, fail-closed "
       "on an unresolved actor, and neither the assembler nor the v1 retrieval "
       "provider holds, reads, or logs a credential of any kind"),
    _D("Consent Profiles Are A First-Class Contract", INAPPLICABLE,
       "consent is a subject's; with no customer subject there is no consent "
       "profile to carry, honour, or withdraw"),
    _D("Fail Modes Are Explicit And Break-Glass Is Audited", REALIZED,
       "the declared degraded posture is the reduced packet with its posture "
       "stated, and there is NO break-glass path on this surface at all — a "
       "rail is never bypassed to reach a provider"),
    _D("Erasure Is Distinct From Revocation", INAPPLICABLE,
       "erasure is a subject-data obligation; this surface stores no subject "
       "data, and its derived index holds nothing that is not already in the "
       "repository it was derived from"),
    _D("Gateway Conformance Is Testable", NARROWED,
       "the requirement's own scenarios are about a DomainxFactory declaring a "
       "stack.yaml memory_gateway block that the canonical domain-factory "
       "validator checks, and this surface is not a domain factory and has no "
       "such block; what it realizes is the requirement's RULE — that a "
       "conformance claim is executable rather than asserted — through a "
       "declaration a validator can read and a companion test suite that "
       "executes every refusal condition and cross-examines each claim against "
       "the module that realizes it. NARROWED rather than realized, and "
       "deliberately: no gate outside this repository's own test run reads "
       "this declaration today, so claiming the requirement whole would be the "
       "unchecked assertion it exists to prevent"),
    _D("Derived memory bindings validate against the neutral schema",
       INAPPLICABLE,
       "a hermes_memory_binding is the projection of a LAYER's seeded memory "
       "boundary; this surface is not a Hermes layer, seeds no boundary, and "
       "produces no binding for rails to consume"),
    _D("Subject-Free Local Consumers Declare Their Inapplicable Rails",
       REALIZED,
       "this declaration IS the act that requirement describes: the whole "
       "roster carries a disposition and a reason, every inapplicable rail is "
       "named with why, the constructor REFUSES the declaration to a consumer "
       "holding a credential, addressing a customer subject, or routing to a "
       "networked provider, and nothing here reduces what stays applicable — "
       "the seven requirements the delta forbids narrowing are dispositioned "
       "realized or partial, never inapplicable, and a test asserts that"),
)

# The surface's declaration, built through the same refusing constructor any
# other consumer would use — never assembled by hand — so the module cannot
# hold a declaration its own rules would have refused.
DECLARATION = declare_subject_free_local_consumer(
    DOXBENCH_SHAPE,
    dispositions=DOXBENCH_DISPOSITIONS,
    promotion_act=DOXBENCH_PROMOTION_ACT,
)
