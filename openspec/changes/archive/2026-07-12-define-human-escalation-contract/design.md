# Design — Define Human Escalation Contract

## Context

Three human-touchpoint surfaces exist today and only one is well-defined:
gates the human already visits (ratify, admission — well-defined, batched),
Merge Master's "request human or team review for medium/high-risk actions"
(undefined risk tiers), and the domains' ambiguity routing (codexFactory's
overlay routes six ambiguity classes to *agent* authorities and its six
stop conditions block — correctly, but with no contract saying that
blocking-over-interrupting is the rule). The dangling `HR when present`
consultation in the engineering escalation table dates to the original
canonical roles doc and survived the DTN-013 split because nothing defined
what would summon it.

The governing asymmetry: **blocking is nearly free, interrupting is
expensive and compounding.** A parked workflow waits at a gate the human
visits on their own schedule; an interrupt claims attention now, and each
unnecessary one erodes the signal value of all future ones.

## Goals / Non-Goals

**Goals:**

- One neutral contract answering "when exactly is a human summoned?" with
  a bar high enough that the answer is almost always "not now — park it."
- Merge Master's autonomy envelope defined positively (what it MAY approve
  alone) so everything outside it has a defined non-interrupting path.
- Interrupts auditable and self-limiting (cite-the-class rule).

**Non-Goals:**

- No new roles. `HR` is not defined; the dangling reference is *replaced*
  by the ladder (domain follow-through). The human in the loop is whoever
  holds the relevant gate authority in the deployment.
- No notification/paging mechanics (channels, schedules, on-call) — that
  is deployment instantiation, like group definitions.
- No change to gate structure or workflow contracts; the ladder plugs into
  the existing `blocked` state and existing gates.
- No interrupt-rate tooling (noted as a doc-health family candidate).

## Decisions

### D1 — Ladder with strict precedence, not a risk-scoring matrix

Route → Park → Interrupt, each rung legal only when the previous rung
cannot hold the situation. *Alternative considered:* a risk-scoring rubric
(likelihood × impact tiers) — rejected: scores invite calibration drift
and are exactly how "medium risk" becomes an interrupt at 2am; a
precedence ladder makes the default path structural, not judgmental.

### D2 — Interrupt = containment failure, enumerated closed-set

The interrupt test is conjunctive: (a) the situation actively deteriorates
while parked, AND (b) no agent can contain it within declared permissions.
The classes are a closed set (live secret exposure beyond agent
revocation; active unauthorized access; in-flight irreversible action with
no agent halt authority). A closed set can grow by proposal; an open set
grows by rationalization. Deadline pressure is explicitly named
non-interrupting because it is the most common rationalization.

### D3 — Park is the default human path, and it reuses `blocked`

No new workflow state. Parking = the existing `blocked` state plus a
decision-ready packet queued at the owning gate. This means the ladder
needs zero changes to workflow contracts — domains already reach `blocked`
from any workflow. The packet contract (one screen, ≤3 options, one
recommendation, consequences including of-no-decision) is what makes
batching cheap; dedupe by root cause is what keeps queues short.

### D4 — Silence is fail-closed

No answer means it stays blocked; a timeout never escalates autonomy or
re-pings. *Alternative considered:* timeout-then-interrupt escalation —
rejected: it converts every parked decision into a delayed interrupt and
inverts the bar.

### D5 — Low-risk envelope defined positively and conjunctively

Merge Master MAY act alone only when ALL hold: required deterministic
checks pass; policy-required governed review verdict is ADMIT with no
undispositioned conditions; ordinary revert suffices as rollback; the
action is within approved scope; no open security findings. Fails-any →
park at the merge gate. This replaces "low/medium/high-risk" adjectives
with checkable conditions and makes the existing external-enforcement text
("must route human review for risk that exceeds its authority")
mechanical.

### D6 — Neutral contract, domain-instantiated examples

openxFactory owns the ladder, classes, and delivery rules (it declares
ownership of escalation policy); each domain maps the interrupt classes to
domain examples in its role instantiation doc (engineering: what counts as
a live-exposure or in-flight-irreversible case in GitHub terms). Mirrors
the DTN-013 split exactly.

### D7 — Parking is encoded in external enforcement where supported

Wherever the domain's enforcement system can require human review, the
parked human gates are declared there as rules (named/counted required
reviewers, path-scoped ownership, deployment approval reviewers) rather
than existing only as factory policy. Two independent layers result:
factory agents lack merge/deploy authority by permission, and the
enforcement system refuses the action until the human act occurs — parking
holds even against a misbehaving agent. A pending required review is a
park by construction (the enforcement system holds the door without
paging), and the enforcement configuration becomes the machine-readable
answer to "is a human gate present here?" — eliminating the prose
ambiguity that produced `HR when present`. Path scoping is what lets the
human gates and the Merge Master low-risk lane coexist: human-declared
surfaces always demand the human; other surfaces may clear through the
envelope once the enforcement system accepts the Merge Master identity.
For engineering the mechanisms are GitHub branch protection/rulesets,
CODEOWNERS, and environment required reviewers; other domains map to their
enforcement systems' equivalents (named in the domain instantiation, not
here).

## Risks / Trade-offs

- [A true emergency outside the closed set] → the conjunctive test (a)+(b)
  is itself the backstop: any situation satisfying both is interrupt-legal
  even while the class list catches up via proposal; the audit record then
  drives the list amendment.
- [Bar so high that parked queues silently rot] → parked packets are
  visible at gates the human already visits, and consequence-of-no-decision
  is a required packet field; queue-aging is a natural future doc-health
  family (out of scope here).
- [Domains ignore the ladder and keep ad-hoc pinging] → the cite-the-class
  audit rule makes violations detectable; conformance rides the same
  review lanes as every other governance doc.
- [Merge Master envelope too tight, throughput suffers] → the envelope is
  conjunctive but every condition is already produced by the existing
  pipeline (checks, review verdicts, scope refs); if throughput data later
  justifies loosening, that is a spec-level change with evidence.

## Open Questions

- **OQ1 (Brett):** should the interrupt classes include a
  tenant-contractual class (e.g. an external system the factory operates
  is down for a paying customer), or is that deployment policy layered on
  by tenants? Proposal drafts it OUT (tenant policy may add classes; the
  neutral set stays minimal).
- **OQ2:** once codexFactory's `harden-conformance-gate` lands, should its
  parity checker also verify that domain role docs reference the ladder
  instead of undefined consultation IDs (a lint for future `HR`-style
  danglers)? Candidate follow-up, not blocking.
