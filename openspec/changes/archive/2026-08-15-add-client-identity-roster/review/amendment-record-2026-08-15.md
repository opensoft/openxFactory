# Amendment record: add-client-identity-roster — delta fidelity (G5, G7)

Status: record
Date: 2026-08-15
Ruled by: architect seat, pre-implementation gate panel for Speckit feature
`007-client-identity-roster`
(`specs/007-client-identity-roster/gate-panel-rulings-2026-08-15.md`,
rulings G5 and G7), both flagged to Brett in the gate report so they can be
overruled.
Sibling to: `amendment-record-2026-08-14.md` and `decision-review-2026-08-14.md`
(both `Status: record`) — written as a NEW record rather than appended to
either, per the record-immutability rule.

## The shared defect: a declared modification the delta text does not carry

Both amendments cure one mechanic, discovered by executing the archive rather
than by reading it. **The OpenSpec archive rewrites a promoted capability PER
REQUIREMENT, not per capability.** It replaces exactly those requirements a
delta restates by heading, wholesale from the delta's text, and leaves every
other promoted requirement untouched. Two consequences the packet had not
accounted for:

1. A promoted requirement that the change CHANGES in substance but no delta
   RESTATES survives the archive unchanged — so the promoted capability keeps
   text the shipped artifacts contradict.
2. A requirement a delta DOES restate is replaced whole — so any promoted
   scenario the delta's version omits is DELETED on landing.

Defect 1 is G5; defect 2 is G7. Neither declares a new capability, changes a
ratified position, or adds or removes scope: each completes the realization of
a modification the ratified proposal ALREADY declares
(`consent-instrument`, `doc-health`). They are the same class as the
encode-phase amendments Decisions A and B authorized in kind — carrying a
declared modification faithfully into delta text.

### Root cause, recorded against clarify ruling N1

Clarify ruling N1 (`specs/007-client-identity-roster/clarify-rulings-2026-08-14.md`)
grew the consent status enum by `withdrawn` and justified it with
"consent-instrument IS a declared MODIFIED capability". That reasoning
conflated CAPABILITY-LEVEL DECLARATION with PER-REQUIREMENT archive
mechanics: declaring the capability modified rewrites nothing by itself. N1's
substance stands unchanged — `withdrawn` is a distinct terminal member and the
cascade fires on both events — but its stated mechanism was wrong, and the
downstream artifacts inherited it. The same wrong mechanism is corrected in
`research.md` (the consent-lifecycle section) and `plan.md` (decision 15),
which had both recorded "the archive step rewrites promoted spec text" without
the per-requirement qualification.

## G5 — the missing consent-lifecycle MODIFIED requirement

**What was missing.** The packet's `specs/consent-instrument/spec.md` carried
only the cascade requirement. The promoted capability's separate requirement
"The Lifecycle Enum Is Closed With Declared Aliases"
(`openspec/specs/consent-instrument/spec.md:69-74`) declares a CLOSED
five-state lifecycle and was not restated anywhere in the packet — while the
change ships a six-state enum in the schema, the class registry and the
validator (FR-039, tasks 8.1–8.2).

**Proof.** The archive was EXECUTED against a scratch copy of the promoted
spec. The five-state requirement survived byte-identical: the delta names only
the cascade requirement, so the archive had nothing to replace it with. On
landing, the promoted capability would have declared a closed five-state
lifecycle while its own cascade requirement obliges behaviour on "terminated
or withdrawn" and the shipped artifacts admit six states — a capability
contradicting itself and the tree.

**The amendment.** `specs/consent-instrument/spec.md` gains one MODIFIED
requirement, "The Lifecycle Enum Is Closed With Declared Aliases", restating
the promoted requirement in six-state form: `withdrawn` a DISTINCT terminal
member reachable past execution, explicitly never an alias of `terminated`,
with the promoted alias-mapping and class-skip clauses carried verbatim and
both promoted scenarios preserved, plus a third scenario making the
non-aliasing rule falsifiable. Validated end-to-end before adoption: strict
validation passes, `--all --strict` passes 58/58, and the archive rebuild
yields the six-state lifecycle in place of the five-state one.

**Riders carried in the same window.**

- `proposal.md`'s `consent-instrument` modification description now names the
  lifecycle growth. It had understated the modification in exactly the way the
  pre-Decision-A text understated the packet.
- Task 8.1 gains the two count-bearing PROSE sites that say "five" of a set
  becoming six: `contracts/schemas/consent-instrument.schema.yaml:195` and
  `scripts/validate-consent-instruments.py:356`.
- `research.md` and `plan.md` decision 15 are corrected to state the
  per-requirement archive mechanic (see "Root cause" above).

## G7 — the doc-health delta rebase

**What was missing.** The packet's `specs/doc-health/spec.md` restated the
MODIFIED requirement "Deterministic check families" with the sixteen-family
enumeration and TWO scenarios. The promoted requirement carries SEVEN, and its
first scenario ("A run executes the check families") carries five THEN/AND
bullets including the per-repo-plus-preflight coverage clause and the
"reported as skipped, never silently omitted" clause.

**Proof, three ways.** (a) The archive tool's source: a restated requirement is
replaced wholesale. (b) `buildUpdatedSpec` executed live against the current
delta: the rebuilt promoted spec lost six scenarios and kept only a gutted
seventh. (c) An 8-of-8 replacement audit across the archive history: every
archived change that restated a requirement replaced it entirely, with no case
of scenario merging.

**The amendment.** The delta's MODIFIED block is REBASED onto the promoted
requirement: all seven promoted scenarios restated verbatim (verified by diff
against `openspec/specs/doc-health/spec.md` — the only differences are this
change's own additions), the sixteen-family enumeration and the cross-domain
scoping sentence retained, the roster-composition scenario appended, and ONE
owning-requirement AND-bullet added to the run scenario. That bullet points at
`client-identity-roster`'s requirement "The roster composes across domains
from published fragments" — the capability that owns the family's definition —
rather than at a doc-health-internal requirement, because none exists for this
family and the bullet would have dangled.

**Rider.** `tasks.md` gains task 10.7, a pre-archive assertion that the
doc-health delta is verified rebased onto the promoted scenario set as it
stands at archive time (and the same check for the consent lifecycle
requirement), following the precedent recorded at
`openspec/changes/archive/2026-08-04-add-ideation-cross-reference-readiness/tasks.md:5`.

## Consequences recorded

- Modified Capabilities are unchanged at four: `consent-instrument`,
  `doc-health`, `domain-conformance-checks`, `credential-contracts`.
- The `consent-instrument` delta now carries two requirements; the `doc-health`
  delta now carries one requirement with eight scenarios.
- Archive blockers are unchanged. Task 10.7 is a pre-archive verification, not
  a new blocker.
- Strict validation re-run over the amended packet and over the whole OpenSpec
  corpus before this amendment was committed.
- The mechanic itself is now stated in the artifacts (plan.md decision 15,
  research.md, task 10.7) so a later change in this family cannot inherit the
  N1 conflation again.
