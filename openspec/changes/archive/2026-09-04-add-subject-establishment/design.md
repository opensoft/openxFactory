# Design: add-subject-establishment

Six questions. § 1 is why this generalization is real rather than a shape three
domains happen to share. § 2 is why the schemas are not here, argued against a
live counter-precedent from the same day. § 3 is the cross-factory seam — the
one finding the second consumer produced and the first structurally could not —
and why it consumes a ratified capability instead of inventing a mechanism.
§ 4 is why the conformance dial is the escalation ladder and not a new one.
§ 5 is what verify-by-read-back actually costs, and the sharp version Ledgerx
already paid for. § 6 is the boundary this packet refuses to cross: what stays
domain material, and why saying nothing is the strongest thing neutral text can
do about it.

## 1. Why this is a real generalization and not a family resemblance

The DTN test is not "do these look alike". It is: strip the domain nouns and
see whether what remains is a contract or a coincidence.

Stripped, LedgerxFactory's `layered-books-design.md` leaves an ordered pipeline
with two artifact kinds and six obligations. Substitute codex's nouns and every
step lands: fact set becomes language/stack, criticality tier, compliance
regime, data sensitivity; neutral design becomes branch and review policy,
environment topology, quality gates, release discipline; system of record
becomes GitHub; realization becomes rulesets, required checks, environments,
CODEOWNERS. Substitute Medx's and it lands again: problem list, care-plan
structure, medication reconciliation, care-team roles, consent posture, into
chart sections, order sets, encounter templates, flowsheets. Opsx and Adx land
too.

**What makes it a contract rather than a coincidence is the pair of properties
the split BUYS, which no domain gets by accident.** Portability: the design
survives a platform migration because it contains no platform. Reviewability:
the licensed expert reads domain judgment because vendor trivia is somewhere
else. Second-platform cost: a mapping rather than a redesign. A domain that
merely happened to have a similar workflow would get none of these, because
they follow from the SEPARATION, not from the sequence. That is why
requirement 1 refuses a collapsed artifact and requirement 3 refuses a vendor
noun in a design — those two refusals are the whole contract, and everything
else is what has to be true for them to hold.

**And there is direct evidence the vocabulary is already half-present in the
second consumer.** codexFactory's subject-Hermes template already carries
`project` as a first-class subject kind alongside `repository`, `product` and
`feature_initiative`, and `repository` already carries `check_profile` and
`reviewer_group` — which are neutral-design elements wearing domain names. The
second instantiation therefore structures existing material rather than
inventing it, which is a much stronger signal than a table of analogies.

## 2. Why the schemas are not here — argued against a counter-precedent

**The counter-precedent first, because it is six hours old and cuts the other
way.** On 2026-08-28 Brett VETOED the identical decision in
`add-credential-escrow-checkout`: that packet had argued its schema surface
belonged to a successor, and the veto's reasoning was that the shape was
ALREADY RULED, so deferring settled content bought nothing and cost a round
trip. If that reasoning transfers, OD-1 falls the same way and this section is
the losing argument.

**Why the authoring session judges it does not transfer, stated as a
distinction a reader can check.** In the escrow case Brett had ruled the record
kind's contents in as many words — "inventory plus restore target, shaped on
the running prior art" — and a running prior art existed in a live install
repository. Here, neither is true. No ruling has fixed a single field of either
artifact kind. The only existing instantiation, LedgerxFactory's, was authored
against ACCOUNTING vocabulary before the neutral vocabulary existed, so lifting
its field names would import Ledgerx's shape as the neutral one — which is the
exact failure the DTN process exists to prevent. And the second consumer, which
is the one that would falsify a Ledgerx-shaped schema, exists as a mapping
TABLE in a staged topic and nowhere else.

**What that leaves is a schema authored by taste.** Its first real consumer
would then MODIFY it, putting an edit on days-old canon — which is precisely
the cost the escrow packet's authored argument named and the veto judged
absent there. Here it is present.

**The seam is clean, and that is testable rather than asserted.** Every one of
the eleven requirements is stated in terms of what an artifact must MEAN, never
what fields it must carry: provenance grade (not a `provenance:` key), traces
to a design element (not a `design_ref:` key), names one system of record (not
a `system_of_record:` enum). Nothing in the delta becomes false when the field
names are chosen. That is the property that makes the split honest, and if a
reviewer finds a requirement that silently assumes a field name, the split is
wrong at that requirement and should be reported as such.

**The honest cost of being right about this.** A capability with no schema is a
capability with no validator, which means conformance is prose-checked until
the successor lands. A domain could claim conformance and no tool would
contradict it. That is a real gap for the period between this packet and its
successor, and the mitigation is only that the successor is named, not that the
gap is small.

## 3. The cross-factory seam: a finding, and a mechanism already ratified

**The finding.** codexFactory designs an engineering project's setup. GitHub
administration is OpsxFactory's capability (`github-administration-workflow`),
not codexFactory's — Opsx holds the platform authority, the App identity tiers
and the credentials that actually change GitHub. So the DESIGNING domain and
the APPLYING administrator are different factories.

**Why Ledgerx could not have surfaced it.** Ledgerx designs and applies inside
its own estate. A neutral contract derived from Ledgerx alone would have one
actor in it, implicitly, everywhere — and would have been wrong for the second
consumer on the day it promoted. This is the single strongest argument in the
staged topic for why a second consumer was required before promotion, and it is
worth recording that the requirement paid for itself.

**Why the answer is a consumption and not an invention.** The topic guessed the
seam was `deployment-handoff-boundary` and said "check before inventing a
second mechanism". Checked: that topic is no longer staged. It ratified on
2026-07-29 and archived 2026-07-30, and its promoted text fixes all three parts of the crossing —

- **who applies**: the managed-subject test
  (`openspec/specs/deployment-handoff-boundary/spec.md:6-33`);
- **what crosses**: a `client_infrastructure_request` or a
  requirements-profile of it, with the explicit sentence **"a new record kind
  SHALL NOT be introduced for this purpose"** (`:35-49`);
- **what correlates**: a correlation identifier stamped into the change
  surfaces execution touches, joined by a periodic evidence-correlation audit
  (`:91-106`).

That middle sentence is decisive, and it decides against the obvious design.
The obvious design for a handoff-shaped realization is a new
`subject_realization_handoff` record. Ratified canon forbids it by name. So
requirement 7 states what the realization IS in that crossing — the requested
intent inside a request kind that already exists — and adds exactly one thing
the boundary does not say: that the DESIGN joins the correlated set, so an
observed change on the target system resolves back past the request to the
domain judgment that asked for it. Without that addition the boundary
correlates request-to-change and the design dangles; with it, the audit answers
"why is this repository configured this way" rather than only "who was allowed
to configure it".

**What this leaves genuinely open** is who owns the verdict when the two
parties read back and disagree (OQ3). Requirement 8 is deliberately authored to
be true under either allocation — it obliges a read-back and a resolved diff
without naming whose diff decides — so a ruling either way moves a scenario
rather than the requirement.

## 4. Why the conformance dial is the escalation ladder

The staged topic named two candidate homes for "conforming auto-approves,
deviating escalates": `governed-derived-model`'s tiered conformance, and
DTN-015's correction→promotion loop. Requirement 6 uses a third that the topic
did not name — `roles-authority-model`'s route/park/interrupt ladder — and the
reason is that the tiering question is a ROUTING question wearing a conformance
costume.

Read the ladder's promoted text against the dial. "Routed to an agent authority
when one is competent to decide" is the conforming case exactly. "Parked in the
`blocked` state with a decision packet queued at the owning gate when only a
human may decide but the situation is stable" is the deviating case exactly,
including the part domains get wrong: a deviating design is STABLE, so it must
PARK and must not interrupt. And the low-risk enforcement envelope
(`openspec/specs/roles-authority-model/spec.md:80-91`) is already the
conjunctive shape a standing auto-approve envelope needs. Expressing the dial
any other way would restate a ratified mechanism in slightly different words,
which is the failure mode the DTN process exists to avoid on the way IN and
should avoid on the way out too.

**What the ladder does not cover, and where the other candidate belongs.** The
HARVEST — a resolved deviation becoming standard — is not a routing act. It is
DTN-015's correction→promotion loop, and DTN-015 is still `seed`. So
requirement 5 states the harvest's INVARIANTS (a harvest produces a new
archetype version; a new version does not retroactively invalidate subjects
measured against the old one) and names no mechanism, so that expressing it
through DTN-015 later is a refinement rather than a contradiction. This is
OQ2's live half.

**The one invariant worth defending on its own.** "A new archetype version does
not retroactively invalidate an approved subject design" is the difference
between an archetype that improves and an archetype nobody dares improve. If
harvesting a good resolution manufactures non-conformance across every existing
subject, the rational move is to stop harvesting, and the auto-approve share
stops growing — which is the whole payoff of the dial.

## 5. What verify-by-read-back costs, and the sharp version

Every domain in the table applies through external enforcement it does not own:
an EHR, GitHub, Intune, Business Central, an ads platform. Every one of them
can do something other than what was asked, and none of them is obliged to say
so. That is why the obligation belongs in the neutral contract rather than in
each domain's realization: it is a property of applying through someone else's
system, and every domain does.

**The sharp version, already paid for.** Ledgerx's sandbox rehearsal produced
the lesson that Business Central VALIDATES BEFORE IT AUTHORIZES — so a probe
that gets a well-formed answer may never have reached the layer that decides
whether the caller is allowed to do the thing. A green probe under those
conditions proves the request was well-formed and nothing else. Requirement 8
therefore refuses pre-authorization evidence by name rather than requiring
"verification" and trusting each domain's idea of it, because the failure is
not that domains skip verification — it is that they verify the wrong layer and
believe they are done.

**The cost, stated honestly.** Read-back is a second round trip against a
system whose rate limits, eventual consistency and partial-write semantics are
not this capability's to fix. A domain applying a hundred elements pays a
hundred reads or finds a bulk read, and where the platform offers neither, the
domain owes a story this capability does not supply. Requirement 8 states the
obligation and deliberately states no mechanism for meeting it cheaply.

## 6. The boundary this refuses to cross

The staged topic wrote its own not-neutral list, and honouring it is most of
what keeps this packet small. Four things stay domain material and this
capability says nothing about them: the CONTENT of any design or archetype;
which external systems a domain supports and how they map; the expert seat that
reviews a deviating design; and whether a domain's subjects even live in an
external system at all (OQ4).

**The third one is the one worth arguing.** It is tempting for neutral text to
name a reviewer role — "the domain's licensed authority" — and be done. But a
licensed accountant, a clinician and a staff engineer are not one role with
three labels; they differ in what licenses them, what they are liable for, and
what a wrong approval costs. Requirement 6 therefore obliges a domain to NAME
its seat and refuses to name it for them, and adds the one scenario that makes
the obligation checkable: a domain naming no seat does not conform, because
everything would route and the deviating branch would be dead code.

**And the fourth is why requirement 4 says "names exactly one system of record"
rather than "may name a system of record".** Optionality there is an escape
hatch: a domain that finds the split inconvenient declares itself
system-of-record-free and keeps one artifact. OQ4's recommendation is to allow
the factory's own governed store to BE the system of record, which preserves
the discipline while admitting the case the topic raised — but that is a
recommendation, not a decision, and the delta is authored so that either ruling
changes a scenario rather than the requirement.

## Risks

- **A capability with no validator is a capability that cannot refuse
  anything.** Between this packet and its successor, conformance is prose. The
  mitigation is that the successor is named and that OD-1 is flagged for exactly
  this reason — not that the risk is small.
- **The second consumer is a table, not a change.** codexFactory new-project is
  decided and mapped, but no codexFactory change instantiates it. If the codex
  instantiation, when written, cannot express itself in these eleven
  requirements, the requirements are wrong and this packet learns it after
  promotion rather than before. Accepting that is the cost of promoting on two
  mappings instead of two implementations.
- **The Ledgerx instantiation cites nothing neutral and cannot be made to.**
  Three archived packets, immutable, in a repository this one has no authority
  over. The follow-up is a NEW LedgerxFactory record, which means the first
  instantiation's conformance is unproven until that repository acts — and
  nothing here can force it.
- **Requirement 7 depends on a boundary whose own adoption is phased.**
  `deployment-handoff-boundary` holds standing administrative access open as a
  named, dispositioned exception until the break-glass checkout path is proven.
  A cross-factory apply crossing that boundary today crosses a boundary with a
  live exception in it. That is the boundary's own recorded state and not a
  defect this packet introduces, but a domain instantiating requirement 7
  before the exception closes should know it is building on phased ground.
- **OQ1 could move a requirement rather than a field.** The recommendation
  treats "system of record" as a named target with no neutral shape. If the
  measurement pass finds that the existing estate vocabulary already carries
  binding dials this capability needs (operator-hosted versus client-hosted,
  identity per estate), requirement 4 may owe a clause it does not have. The
  packet is authored to make that a successor's amendment rather than a
  correction, but it is a real possibility rather than a formality.
