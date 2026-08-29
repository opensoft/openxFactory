---
code_surface: none — SPEC AND CAPABILITY TEXT ONLY, and the honest reason is that the two artifact kinds this packet defines have no consumer yet. `openspec/specs/subject-establishment/spec.md` is created on promotion; nothing under `contracts/`, `scripts/` or `tests/` moves, and no file in this repository is edited outside `openspec/changes/add-subject-establishment/`, the staging bookkeeping (`ideation/staging/INDEX.md`, `ideation/README.md`, the regenerated `ideation/cross-reference.*`), the DTN register row and section, and the README OpenSpec Records entry. **THE SCHEMAS ARE DELIBERATELY NOT HERE AND THAT IS OD-1, FLAGGED FOR VETO.** The staged topic's own Exit path names "the two artifact kinds … WITH THEIR SCHEMAS", so this packet departs from its declared exit and says so rather than quietly narrowing it: `contracts/schemas/xfactory-subject-design.schema.yaml`, `contracts/schemas/xfactory-platform-realization.schema.yaml` and a `scripts/validate-subject-establishment.py` are named as the successor `add-subject-establishment-contracts`, to be authored against a domain instantiation rather than ahead of one. A LIVE COUNTER-PRECEDENT EXISTS AND IS RECORDED RATHER THAN OMITTED: the identical decision in the sibling packet `add-credential-escrow-checkout` — its OD-2, "this packet carries no schema surface" — was VETOED by Brett on 2026-08-28 over PR #479, on the reasoning that content Brett had ALREADY RULED the shape of should not wait for a successor. That reasoning does not transfer unchanged here (no ruling has fixed either artifact kind's fields, and the second consumer's mapping is not yet authored anywhere), but a reviewer is owed the fact that the same call went the other way six hours earlier.
target_release: none. Nothing in this packet is a member of any contract bundle, so no cut is owed and none is reserved — established by parse rather than by grep: `contracts/releases/contract-v2.0.digests.yaml` was loaded and its 192 entries walked, and NO path this change writes appears among them; the three editorial members `scripts/doc_health/release_inventory.py:62-66` names (`contracts/CHANGELOG.md`, `contracts/manifest.yaml`, `contracts/README.md`) are untouched as well, so the release-inventory-drift family has nothing to report either way. If OD-1 is VETOED this field becomes "next additive contract bundle, allocated AT REALIZATION per `docs/contract-versioning-policy.md` and NOT reserved here" — `contract-v2.0` is the declared bundle (`contracts/manifest.yaml:3`) and the `contract-v1.28` renumber sweep is the standing precedent for why a proposal must not spend a minor before merge order is known — and the archive gate grows the cut. As authored, the archive gate is merge plus green PLUS the ruling round (OD-6), which is stricter than what `code_surface: none` alone would require.
Status: ratified
Ratified: 2026-08-28 by Brett — one selection over the orchestrating session's triage survey of the ageing staging topics, verbatim: "Progress both". The survey's Group-4 recommendation — that `subject-establishment` and the escrow topic be progressed — was the ORCHESTRATING SESSION'S wording; the SELECTION was Brett's, and the two voices are kept apart deliberately rather than merged into one quotation. **THE CITATION COVERS THE DECISION TO FILE AND NOTHING ELSE.** It does not cover this packet's requirement text, the capability's name, the decision to carry no schema surface, or any other decision in § Orchestrator decisions below; those are the authoring session's and every one of them is flagged there for veto. The six § Open Questions carry a recommendation and NO decision, and they come back to Brett. No approving OpenSpec change exists to name, so the citation takes the record spelling `sanction-ratified-record-spelling` sanctions for exactly that case, and clears its three-way floor: approver (Brett), date (2026-08-28), and a resolvable record path (this file, § What Brett ruled, and this packet's `.openspec.yaml`).
Proposed: 2026-08-28
Origin: Staged topic `subject-establishment` (staged 2026-07-28 from Brett's naming of the generalization while designing LedgerxFactory's company provisioning), taking ITS OWN DECLARED EXIT PATH on Brett's ruling of 2026-08-28. Both of the topic's stated exit gates are clear: the LedgerxFactory first instantiation reached proposal and ARCHIVED on 2026-08-04 (`2026-08-04-add-ledgerx-company-provisioning-and-setup-audit`, `2026-08-04-add-ledgerx-msbc-company-realization`, `2026-08-04-modify-ledgerx-ap-intake-for-onboarding-readiness`, verified in the LedgerxFactory checkout on 2026-08-28), and the second consumer was DECIDED on 2026-07-28 as codexFactory new-project. This is a FULL promotion — the topic's one file moves to `supporting-docs/` and its row and detail section leave `ideation/staging/INDEX.md`.
---

# Proposal: add-subject-establishment

## Why

**Five domains are inventing the same pipeline separately, and one of them has
already finished.** LedgerxFactory built it for a new client company and
archived three changes on 2026-08-04 doing so. MedxFactory's new patient,
codexFactory's new engineering project, OpsxFactory's new managed estate and
AdxFactory's new campaign subject are the same motion with different nouns:
establish provenance-graded facts about a newly admitted subject, design the
best-practice setup for it IN DOMAIN TERMS, decide which external system it
will live in, map the design into that system, review, apply, verify. Brett
named the generalization on 2026-07-28, while the Ledgerx work was still in
front of him: *"this concept of intake is also a general startup. it is the
same as new patient or new engineering project. there is a setup of facts and
then the best practice way to setup that subject in that domain. some of this
neutral concept should be elevated to openXfactory."* Four domains have not yet
built it. This packet is the difference between them instantiating a contract
and each deriving one.

**The load-bearing neutral idea is the design/realization split, and the stack
already runs it one level up.** A neutral contract plus a per-domain overlay is
the idiom this repository is built on. Here it is a neutral subject design plus
a per-platform realization, and it buys the same three things: portability (the
design survives a platform migration), reviewability (a licensed expert reviews
domain judgment, not vendor trivia), and cheap second-platform support (a
mapping, not a redesign). The five-domain table in the staged topic is the DTN
test made concrete — the columns differ and the pipeline does not.

**The second consumer surfaced something the first structurally could not.**
Brett decided codexFactory new-project as the second consumer on 2026-07-28,
and its mapping exposed the finding that decides this packet's shape: **GitHub
administration is an OpsxFactory capability, not a codexFactory one**. So for
codex the DESIGNING domain and the APPLYING administrator are DIFFERENT
FACTORIES. Ledgerx hid this — it designs and applies inside its own estate — so
a contract written from Ledgerx alone would quietly assume one actor and would
be wrong for the second consumer on the day it landed. Requirement 7 is that
finding made into a contract obligation, and it consumes an existing seam
rather than inventing one (§ The cross-factory seam, below).

**And the topic's own exit gates are clear.** Its Exit path gated promotion on
LedgerxFactory reaching proposal and on a second domain naming its instance.
The Ledgerx gate CLEARED on 2026-08-04 — three changes archived, verified in
the LedgerxFactory checkout rather than assumed — and the second-domain gate
cleared on 2026-07-28. The topic has been sitting past both for over three
weeks, which is what put it in front of Brett as an ageing-topic finding at all.

## What Brett ruled, 2026-08-28

One selection, and it is worth recording exactly because it is small. The
orchestrating session ran a triage survey over the fourteen staging topics
`doc-health`'s `staged-candidate-aging` family was warning on, grouped them,
and recommended for Group 4 that `subject-establishment` and
`client-credential-escrow-registry` both be progressed to proposals. Brett's
ruling was two words, verbatim: **"Progress both"**.

The RECOMMENDATION is the orchestrating session's wording. The SELECTION is
Brett's, and it is the origin act — the instruction-as-origin-act shape that
`govern-derived-pin-reachability`, `supersede-lost-pin-baseline` and
`fix-release-reachability-race` set. The two voices are kept apart on purpose,
because attributing the survey's phrasing to the approver would credit an
authoring session's words to Brett.

**What that ruling does NOT cover** is everything below it. It admitted the
topic to the proposal queue; it did not ratify a capability name, a requirement
count, a scope boundary, or the decision to leave the schemas out. Six
orchestrator decisions and six open questions are waiting on a ruling round,
and this packet says so in every place a reader might otherwise assume
otherwise.

## What this changes

**ELEVEN ADDED requirements on a NEW neutral capability
`subject-establishment`, 37 scenarios, and no MODIFIED block anywhere.** No
promoted requirement in any capability moves a word.

1. **Subject establishment is one neutral pipeline over two artifact kinds.**
   The ordered motion — fact set, neutral design, system-of-record selection,
   platform realization, tiered review, apply, verify — plus the two artifact
   kinds it carries. Domains instantiate rather than re-derive; a step outside
   the ordering is an amendment to this capability, not a domain extension.
   Collapsing the two artifacts into one does not conform, because the split IS
   the portability, the reviewability and the second-platform property.
2. **Every fact carries a provenance grade.** Authoritative registry, subject
   self-report, and factory observation are not the same evidence and are not
   recorded as if they were. Grades are re-evaluable with the superseded grade
   legible, so a design approved under weaker evidence can be found later. This
   is `governed-derived-model`'s full-provenance requirement applied to the
   establishment fact set rather than a second provenance mechanism, and a
   domain already declaring the assumptions-forbidden form satisfies it by that
   form.
3. **The neutral design names semantic roles and no vendor object.** A design
   element expressed as a G/L number, a repository ruleset id, or a chart
   section code does not conform — it belongs in the realization under the role
   it was standing in for. This is the requirement that makes 4 possible at
   all.
4. **The platform realization is a separate artifact naming exactly ONE system
   of record.** Every realization element traces to a design element; every
   design element is mapped or explicitly recorded as unrealizable with a
   reason; an unmapped realization object is drift, because an object nobody
   designed is an object nobody reviewed. A realization spanning two systems
   does not conform, because the per-platform overlay is what makes the mapping
   reviewable by that platform's specialist and replaceable at migration.
5. **The reference archetype accelerates and measures, never overrides.**
   Versioned archetype-level designs that research starts from and that serve as
   the conformance yardstick; the per-subject design stays authoritative; a
   harvested deviation resolution produces a NEW archetype version rather than
   mutating the one existing subjects were measured against, so an archetype
   improvement never manufactures retroactive non-conformance.
6. **Conformance tiering is the ratified escalation ladder applied, not a new
   mechanism.** Conforming designs ROUTE and decide within the domain's
   standing envelope; deviating designs PARK with a decision-ready packet at
   the domain expert's own gate and never interrupt on deviation alone. A
   domain that names no expert seat does not conform, because an unnamed gate
   is an unreachable one and everything would route.
7. **A realization crossing to a different applying factory rides the ratified
   handoff.** The cross-factory seam, below.
8. **An apply is not conformant until it is verified by read-back.** Read the
   resulting state from the system of record, diff it against the realization
   that was applied, resolve the diff before the subject is established. The
   read-back must traverse the same authorization path a real change does —
   a probe a platform answers BEFORE it authorizes proves nothing, which is
   the sharp lesson Ledgerx already paid for on Business Central.
9. **Establishing and migrating are different authority classes and never share
   a grant.** A new subject in an empty environment is low-risk because the
   remedy for a wrong result is to discard and re-provision; an established
   subject carrying history is proposal, approval, apply, verify, in that
   order, in every domain. An establishment-class grant presented against a
   subject that already holds state is refused.
10. **The audit mirror lifts existing configuration into the neutral design.**
    The commercial half — read what a subject actually has, lift it to neutral
    through the SAME mapping the realization declares, diff against the design
    research would produce today, propose the difference as a migration-class
    act. Where the lift and the mapping disagree, the MAPPING is defective; one
    mapping read in two directions is what makes the mirror trustworthy.
11. **Layer ownership is fixed; storage is not.** Subject layer holds the facts
    and the subject's design, tenant layer holds the archetype library, the
    standard and the system-of-record selection, domain layer holds the
    correctness criteria. Which STORE any layer uses stays a realizing
    repository's choice (OD-5).

## The cross-factory seam, and the seam it consumes

The staged topic asked whether the handoff shape "is very likely the same seam
as the staged `deployment-handoff-boundary` topic — check before inventing a
second mechanism." Checked, and the answer is stronger than the topic could
know when it was written: that topic is no longer staged. It is RATIFIED CANON
(`add-deployment-handoff-boundary`, ratified 2026-07-29 and archived 2026-07-30), and it already fixes
every part of the crossing this capability needs.

- **Who applies** is decided by its managed-subject test
  (`openspec/specs/deployment-handoff-boundary/spec.md:6-33`) — does the target
  resolve to a registered subject in the managing factory's service-subject
  model.
- **What crosses** is fixed by its requirement *"The handoff crosses as a
  client infrastructure request"* (`:35-49`), which states in as many words
  that the crossing is a `client_infrastructure_request` or a
  requirements-profile of it and that **"a new record kind SHALL NOT be
  introduced for this purpose"**. That sentence is the whole reason requirement
  7 defines no design-handoff record: it would be exactly the refused thing.
- **What binds the three artifacts together** is its out-of-band-detectability
  requirement (`:91-106`), which already stamps a correlation identifier into
  the change surfaces execution touches. Requirement 7 adds one obligation to
  that machinery and no mechanism: the DESIGN joins the correlated set, so an
  observed change resolves back past the request to the domain judgment that
  asked for it.

The register's DTN-017 detail section already recorded this linkage on
2026-07-30 (that change's task 2.3). This packet is the first artefact that
makes it an obligation rather than a note.

## What this deliberately does not change

- **No schema, no validator, no fixtures** (OD-1). Named as the successor
  `add-subject-establishment-contracts`, to be authored against a real domain
  instantiation. The staged topic's Exit named schemas; this packet departs
  from that and flags the departure rather than narrowing the exit quietly.
- **No delta on `deployment-handoff-boundary`** (OD-4). Measured against its
  promoted text: its three requirements already fix who applies, what crosses
  and what correlates. Requirement 7 SUPPLIES a new payload for a mechanism
  that is already general, and a MODIFIED block there would restate a ratified
  requirement to add a noun.
- **No delta on `roles-authority-model`.** Its escalation ladder and its
  low-risk envelope are APPLIED to a new decision class, which is what a
  neutral requirement is for.
- **No delta on `governed-derived-model`.** Its full-provenance requirement is
  CITED by requirement 2 and re-legislated by neither. Whether the conformance
  DIAL can also be expressed through its tiering rather than through the
  escalation ladder is OQ2 and is genuinely open.
- **No design content.** A chart of accounts, a care-plan template, a
  branch-protection baseline, an endpoint baseline — irreducibly domain
  material, and this capability says so by saying nothing about it.
- **No list of supported platforms, and no mapping tables.** Per-domain
  overlays.
- **No named expert seat.** Requirement 6 obliges a domain to name one and
  refuses to name it for them; a licensed accountant, a clinician and a staff
  engineer are not interchangeable and neutral text pretending otherwise would
  be worse than silence.

### Named follow-ups, out of scope here

- **The LedgerxFactory back-citation gap, owned by LedgerxFactory.** Its three
  archived packets of 2026-08-04 are the first instantiation of this pipeline
  and cite NOTHING neutral, because on 2026-08-04 there was nothing neutral to
  cite. That is not a defect in those packets and this change does not touch
  them — archived records are immutable and this repository holds no authority
  over that one. The follow-up is a LedgerxFactory act: record the conformance
  of its company-provisioning capability to this one in a NEW record, once this
  capability is promoted. Recorded in `tasks.md` § Open.
- **OpsxFactory as a consumer in its own right**, not merely as the applier for
  codex's realizations. Its new-managed-estate motion is the same pipeline and
  the topic names it, but no Opsx mapping has been authored. OQ6.
- **The `company-provisioning` staged topic in LedgerxFactory** remains that
  repository's own record; nothing here retires or edits it.

## Orchestrator decisions — ALL SIX FLAGGED FOR VETO

Brett's "Progress both" admitted this topic to the queue. It ruled nothing
below. Every decision here was taken by the authoring session, each is stated
with the cost of vetoing it, and each comes back for a ruling.

**OD-1 — This packet carries NO schema surface; the contracts are a named
successor.** The staged topic's Exit path says "the two artifact kinds …
**with their schemas**", so this is a departure from the topic's own declared
exit and is flagged as one. The argument for the departure: a schema for the
neutral subject design and one for the platform realization would be authored
here against ZERO instantiations of either — the Ledgerx realization predates
the neutral vocabulary and the codex mapping exists only as a table in the
staged topic. Schemas written ahead of both would fix field names by taste and
then be MODIFIED by the first domain that tried to use them, putting a
days-old canon edit on the record for no gain. The requirements above are
exactly the part that does not depend on field names. **Cost if vetoed:**
`contracts/schemas/xfactory-subject-design.schema.yaml`,
`contracts/schemas/xfactory-platform-realization.schema.yaml` and
`scripts/validate-subject-establishment.py` come into this packet with packaged
positive and negative fixtures; `code_surface` becomes a contract surface;
`target_release` becomes the next additive bundle allocated at realization; and
the archive gate grows a contract cut. **The counter-precedent, recorded rather
than hidden:** the same decision in `add-credential-escrow-checkout` (its OD-2)
was VETOED on 2026-08-28. The distinguishing fact is that Brett had already
ruled that packet's record shape and this packet has no such ruling to
implement — but that is the authoring session's distinction, not Brett's, and
he may not draw it the same way.

**OD-2 — ONE capability carrying two authority classes, not two capabilities.**
The staged topic asked (its open question 1) whether establishment and
audit/migration mirror Ledgerx's pair at the neutral layer. The delta is
authored as ONE capability: requirement 9 draws the authority boundary and
requirement 10 puts the mirror inside it. The argument: the mirror consumes the
design vocabulary, the archetype, the realization mapping and the read-back
obligation — all four — so a split would duplicate four requirements by
reference in order to separate a grant boundary that one requirement already
draws. Ledgerx's pair is a domain packaging choice about workflows, not
evidence about the neutral shape. **Cost if vetoed:** requirements 9 and 10
move to a second capability (`subject-audit-migration` or similar), both
capabilities carry cross-references to the other's four shared requirements,
and the register gains a second DTN row.

**OD-3 — The capability is named `subject-establishment`.** Collision-checked
at authoring rather than assumed: no promoted spec under `openspec/specs/`
carries the name, and enumerating every `specs/<capability>/` directory across
every non-archived change returns no match either. The topic's own Target
capabilities line hedged — "`subject-establishment` or similar" — so the name
is the authoring session's. **Cost if vetoed:** a rename before merge, cheap
now and expensive once a domain repo cites it.

**OD-4 — The cross-factory handoff is CONSUMED from `deployment-handoff-boundary`
with no MODIFIED block there.** Measured against that capability's promoted
text, quoted in § The cross-factory seam: it already fixes who applies, what
crosses, and that a crossing gets no new record kind. Requirement 7 names the
realization as a payload of a mechanism that is already general. **Cost if
vetoed:** a MODIFIED block on `deployment-handoff-boundary` adding the
realization artifact to its enumeration — a promoted-canon edit whose entire
content is a noun this packet can state from its own side.

**OD-5 — Layer ownership is stated; the STORE is not.** The staged topic's
open question 5 asked whether Ledgerx's storage rule (subject design in Subject
Hermes memory, archetypes and standard in Tenant Hermes memory, the applied
version's digest in the grant evidence) is neutral. Requirement 11 lifts the
LAYER half and deliberately leaves the STORE half behind. The argument: layer
ownership is a governance fact that survives any persistence choice, while
"Hermes memory" is a Ledgerx realization detail that would bind every consuming
domain to a Hermes-shaped store this capability does not otherwise need.
**Cost if vetoed:** requirement 11 gains a storage clause and every domain
instantiating this capability inherits a store it may not have.

**OD-6 — The archive gate is merge plus green PLUS the ruling round, which is
stricter than `code_surface: none` alone.** The standing rule archives a
`none`-surface proposal on landing. This packet declines that, because a
promoted capability carrying six unruled open questions and six unvetoed
decisions is canon with holes in it, and the holes would be invisible once the
delta is folded into `openspec/specs/`. The change stays ACTIVE until the
ruling round completes. **Cost if vetoed:** the change archives on merge, the
open questions are inherited by whoever writes the successor, and the ODs
become settled by silence rather than by ruling.

## Open Questions — SIX, EACH WITH A RECOMMENDATION AND NO DECISION

Every one of these comes back to Brett. None is decided here, and the delta is
authored so that none of them is decided by implication either.

**OQ1 — Is "system of record" new neutral vocabulary, or the existing estate /
client-infrastructure vocabulary generalized?** The staged topic flagged this
(its open question 2): Ledgerx's `ledgerx-ledger-estate` carries a binding dial
(operator-hosted vs client-hosted, identity per estate) that looks like a
domain instance of something neutral, and Opsx's managed-estate model may be
another. **Recommendation:** do NOT mint a neutral estate record kind in this
packet. Requirement 4 uses "system of record" as a NAMED TARGET and states no
shape for it, which keeps the question open. A measurement pass against
`client-infrastructure-request`'s existing execution-binding vocabulary and
`client-identity-roster` should decide it, and that pass belongs with the
successor that would author the schema — because the answer changes a field,
not a requirement.

**OQ2 — How much of the conformance dial genuinely composes
`governed-derived-model` rather than restating it?** Requirement 6 expresses
tiering through `roles-authority-model`'s route/park/interrupt ladder, which is
one of the two candidates the topic named (its claim 3 named the other:
`governed-derived-model`'s tiered conformance, plus DTN-015's
correction→promotion loop for the harvest). **Recommendation:** the ladder is
the right home for the REVIEW ROUTING, because the ladder is about who decides
and when to interrupt, which is precisely the tiering question. The ARCHETYPE
HARVEST of requirement 5 is the half that looks like DTN-015's
correction→promotion loop, and DTN-015 is still `seed` — so requirement 5
states the harvest's invariants (new version, no retroactive invalidation)
without naming a mechanism, and re-expressing it through DTN-015 when that
lands is a follow-up rather than a gap. Worth a ruling because the alternative
reading — that the whole dial belongs to `governed-derived-model` — would move
requirement 6.

**OQ3 — Who owns the conformance verdict when the applier and the designer
disagree on read-back?** The staged topic called this "a real governance
question, not a detail", and it only exists because of the cross-factory seam.
**Recommendation:** the DESIGNER owns the conformance verdict, because it owns
the intent the diff is taken against; the APPLIER owns the applied-state fact,
because it is the only party with authority in the target system. A
disagreement is therefore never a negotiation — it is a finding against the
realization MAPPING, resolved the same way requirement 10 resolves a
lift/mapping disagreement. Both parties MAY read back; only the designer's diff
decides conformance. Requirement 8 is authored to be true under either
allocation, so a ruling the other way changes a scenario and not the
requirement.

**OQ4 — May a factory's own governed store BE the system of record?** The
topic's not-neutral list raised it: "whether a domain even HAS a system of
record to configure. Some subjects may be established entirely inside the
factory." Requirement 4 requires a realization and names no answer.
**Recommendation:** YES, but the realization stays REQUIRED with the factory's
own store as its named target — never optional. Making realization optional
would let a domain skip the design/realization split by declaring itself
system-of-record-free, which is exactly the discipline this capability exists
to impose, and the read-back obligation of requirement 8 is if anything easier
to meet against a store the factory owns.

**OQ5 — Does a consented self-reported fact carry the consent instrument, and
is that this capability's obligation or DTN-016's?** The topic's claim 2 noted
the fact set overlaps `credential-contracts`' consent references and the
consent-instrument topic. Requirement 2 grades a fact's EVIDENCE and says
nothing about the authority under which it was collected. **Recommendation:**
leave it to `consent-instrument` (DTN-016, `adopted`). A provenance grade
answers "how good is this fact"; a consent instrument answers "were we
permitted to hold it" — two different questions, and folding the second into
requirement 2 would put a consent obligation in a capability with no consent
vocabulary. Medx's new-patient instantiation is where the two meet and is the
right place to prove the composition.

**OQ6 — Is OpsxFactory a named consumer in its own right in this packet?** The
topic calls Opsx "a de facto third consumer of this capability (its own
new-managed-estate motion) AND the applier for codex's", and warns that the
contract must not be written as if consumers are isolated. Requirement 7 covers
the APPLIER role; nothing here covers Opsx's own establishment motion.
**Recommendation:** name Opsx in the register and in this packet's Impact as a
third consumer, but do NOT wait on an Opsx mapping before promoting — two
structurally different platforms (MSBC and GitHub) already exercise the
design/realization split, which is the claim under test. If Brett wants a third
mapping before promotion, that is a hold on this packet and is worth saying so
explicitly rather than discovering later.

## Impact

- **Capability:** `subject-establishment` — NEW, eleven ADDED requirements, 37
  scenarios. No other capability's spec text moves.
- **Consumes:** `deployment-handoff-boundary` (the cross-factory crossing and
  its correlation), `roles-authority-model` (the escalation ladder and the
  standing envelope), `governed-derived-model` (full provenance).
- **Registered as:** DTN-017, whose register status moves `staged` →
  `openspec` in this packet's commit.
- **First instantiation, already landed:** LedgerxFactory's company
  provisioning (three changes archived 2026-08-04). It predates this capability
  and cites nothing neutral; the back-citation is a LedgerxFactory follow-up in
  `tasks.md` § Open, not a defect this packet fixes.
- **Second consumer, decided 2026-07-28:** codexFactory new-project — and the
  applier for it is OpsxFactory, which is why requirement 7 exists.
- **Named third consumer:** OpsxFactory's own new-managed-estate motion (OQ6).
- **Named successor:** `add-subject-establishment-contracts` — the two artifact
  kinds' schemas, the validator, and the packaged fixtures (OD-1), plus OQ1's
  system-of-record measurement pass.
- **Staging:** FULL promotion. `subject-establishment.md` moves to
  `supporting-docs/`, the topic's row and detail section leave
  `ideation/staging/INDEX.md`, and the pointer lands in `ideation/README.md`'s
  "Active proposals promoted from staging" list.
