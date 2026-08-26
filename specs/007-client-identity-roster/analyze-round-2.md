# Analyze round 2 — 007-client-identity-roster

Date: 2026-08-14. Same scope and dimensions as round 1, run fresh against the
post-round-1 artifacts. Round 1's fifteen findings are re-checked below and
none regressed; this round drives deeper into (a) the packet's own task 2.1/2.2
field and vocabulary text, (b) requirement clauses no task claims, and (c) the
006 precedents the artifacts cite by name.

Newly verified this round: `GOVERNED_ROOTS = ("contracts", "docs", "examples",
"ideation", "templates")` with `tests` excluded — so `specs/**` is outside
doc-health's corpus (these analyze records and the feature docs trip no
status-validity finding, and `examples/client-identity-roster/README.md` DOES
need its `Status:` line within the first 15 lines, which `STATUS_SCAN_LINES`
fixes); `FAMILIES` at `families.py:674-690` and `FAMILY_IDS` at
`__init__.py:52-70` exactly; the conformance-gate `make_repo(tmp_path)` inline
template idiom; the consent validator's five self-test failure modes; the
release inventory's four `contracts/schemas/` members are Hermes-runtime gate
and workbench schemas (no openxwallet / consent / credential path — 0 hits), so
"roster paths do not enter it" holds by construction, not by luck; and
`specs/006-openxwallet-contracts/traceability.yaml`'s actual field set.

## Findings

### F-016 — MEDIUM — `admission_surface` members carry no act-and-mechanism documentation, though FR-007 and the packet require it

*Artifacts*: tasks.md 1.2 (closed vocabularies: "each carrying a `description`
naming its extension route"); plan.md Cluster A field table
(`admission_surface | closed enum: business_central, exchange`).

FR-007's second clause — "each entry naming the admission act and the scoping
mechanism that make it a surface" — is not the roster entry's `admission[].act`
(which records what was DONE for one identity). It is the vocabulary member's
own definition, and the packet says so verbatim at task 2.2: "Each entry names
its admission act and scoping mechanism (BC: the per-environment application
user AND the admin-center Entra-app authorization, which is the two-act worked
case)." The roster delta's first requirement carries the same SHALL. No task and
no plan text homes it, so the one thing that makes the surface axis falsifiable
— that a member is defined by an act rather than by a brand — would ship
undocumented in the schema.

*Fix applied*: task 1.2 and plan.md Cluster A now require each
`admission_surface` member's `description` to name its admission act and its
scoping mechanism (for `business_central`, BOTH acts per packet task 2.2), and
extend research.md Decision 8's standing rule to them: a surface description may
not assert a provider fact the builder cannot cite, and an uncitable `exchange`
act/mechanism escalates by the same route ruling A-16 defines for the
multi-surface reader rather than being invented. The `authority_class`
description likewise names FR-005's conformant expression, so 2.3's refusal can
cite the route rather than only the closed set.

### F-017 — MEDIUM — the delta's "two acts → two surfaces" scenario is never reconciled with the BC worked case

*Artifacts*: research.md Decision 1 (the BC record's two acts); plan.md Cluster
D; tasks.md 3.2 — against the roster delta's scenario "One product name has two
admission acts … THEN each act is its own admission surface".

The BC worked case is ONE entry on `business_central` with TWO admission acts
(spec FR-002, US1 scenario 3, SC-003). Read alone, the delta scenario says the
two acts are two surfaces — which the ratified first-release vocabulary
(exactly `business_central` and `exchange`, answer 5 / FR-007) cannot express,
and which would make the mandated worked case nonconformant. A builder
authoring 3.2 has to resolve this and no artifact tells them how.

It is settled by the packet, not by judgment: task 2.2 binds BOTH BC acts to the
single `business_central` member ("BC: the per-environment application user AND
the admin-center Entra-app authorization, which is the two-act worked case"),
and the measured fact behind it is that the two acts are JOINTLY required — the
investigation held admin-consented permissions for six days and still got `401`
until the admin-center act — so neither act is an INDEPENDENT admission act in
the delta's sense. The scenario governs acts that admit independently, in
separate administrative surfaces.

*Fix applied*: the reconciliation recorded in research.md Decision 1 (with the
packet citation and the jointly-required evidence), pointed at from plan.md
Cluster D and tasks.md 3.2, so the worked case is authored as two acts of one
surface deliberately rather than by accident.

### F-018 — MEDIUM — `traceability.yaml` is specified in a shape the 006 precedent it cites does not use

*Artifacts*: tasks.md 10.1 ("the 006 shape … `id`, `artifact`,
`enforcing_check`, `negative_confirmation`, `red_proven`"); plan.md
documentation-structure block (same wording).

Measured against `specs/006-openxwallet-contracts/traceability.yaml`: the file
carries a record envelope (`schema_version: 1`, `kind:
openxfactory_realization_traceability`, `feature`, `ratified_change`,
`capabilities`) and rows keyed by requirement id under `requirements:` with
`statement`, `artifact`, **`enforced_by`**, `negative_confirmation`,
`red_proven`. Three divergences: the field is renamed (`enforcing_check`), the
envelope is dropped — and the repo's own rule is that every YAML carries
`schema_version` + `kind`, which plan.md's Constitution Check IV asserts for
this feature — and `red_proven` is weakened from 006's meaning ("suppressing
the rule's finding code turns the packaged corpus red … proves the probe fails
FOR ITS OWN REASON rather than incidentally") to "whether the check was
observed to FAIL on its negative", which is the weaker measurement FR-018
explicitly refuses to accept.

*Fix applied*: 10.1 and the plan's structure block now name the 006 field set
verbatim, restore the envelope, keep `statement`, and define `red_proven` as
006 does — with the note that the SC rows extend the 006 shape (006 carries
requirement rows only) and that the red proof is reproduced by 2.2's
break-one-negative procedure rather than by a new script.

### F-019 — LOW — "the delta's FOUR pack scenarios" miscounts across two deltas

*Artifact*: tasks.md 5.1.

The `domain-conformance-checks` delta carries THREE roster scenarios (roster
nonconformance fails the gate; roster entry conformance; a target repo
publishing no fragment). The fourth behaviour 5.1 tests — a `mutate` entry with
no ratified capability failing the gate rather than reporting — comes from the
ROSTER delta's "A mutate identity has no ratified capability" scenario.

*Fix applied*: 5.1 now names both deltas and which scenario each behaviour
comes from.

### F-020 — HIGH — the alias rule's third predicate reads a field no artifact declares

*Artifacts*: spec.md FR-038 and FR-001; plan.md Cluster A entry table and the
alias-rule paragraph; tasks.md 1.5, 2.4, 3.5 — against ruling R7.

R7 and FR-038 make "declares no duty-separation rationale" one of three
conjunctive predicates, and FR-017/SC-002's genuine duty pair may qualify
"differing in granted permissions OR declaring the duty-separation rationale".
The rationale is therefore load-bearing twice: it can suppress an alias finding
and it is one of the two ways a mandated ZERO-finding positive stays clean. But
no artifact says WHERE it is declared: it is absent from FR-001's field list,
from the packet's task 2.1 list (checked verbatim), from plan.md's entry table,
and from tasks 1.5. As written, 2.4 cannot implement its own rule and 3.5
cannot author its own fixture.

FR-001 forbids REDUCING the ratified list and records the legend as an addition
the 2026-08-14 rulings make; the rationale is the second such addition, from the
same ruling (R7), so naming it is an encoding of the ruling rather than an
extension of ratified scope.

*Fix applied*: `duty_separation_rationale` declared as an OPTIONAL entry
property (string) in spec.md FR-001/FR-038, plan.md Cluster A, and tasks.md 1.5,
with 2.4 and 3.5 naming it. FR-001's closing sentence now records both
ruling-driven additions instead of one.

### F-021 — MEDIUM — the standing-credential attestation has no declared shape, so FR-013's finding is unfalsifiable — and invites a live-observation implementation

*Artifacts*: plan.md Cluster A (`standing_credential_attestation` | "object: the
claim plus its evidence pointer"); tasks.md 1.7, 2.7, 4.1's
`false-standing-credential-attestation.yaml`.

FR-013 requires that "a credential held outside an approved grant window MUST
make the attestation false and be reported against that entry". The validator is
network-free, single-repo and observes no credential store (FR-029, FR-015), so
the only checkable form is a RECORD-INTERNAL contradiction — and no artifact
says that. Left as is, the rule is either unimplementable or an implementer
reaches for a grant-record read, which is exactly the boundary FR-029 draws.

*Fix applied*: the attestation's shape fixed in plan.md Cluster A and tasks 1.7
as the claim (`no_standing_credential`, boolean), the approved grant-window
reference, and the evidence pointer; 2.7 now states that the finding is raised
on the record-internal contradiction (a claim of none against a declared held
credential or an expired/absent window reference) and that NO live credential
store is consulted, which is what 4.1's negative encodes.

### F-022 — HIGH — FR-014's "resolving to an instrument in force" is implemented nowhere

*Artifacts*: tasks.md 2.8 (presence only) and 2.9 (repo-context rules: sweep,
placement, gate obligation); plan.md Cluster B; research.md Decision 7 — against
FR-014 and the roster delta's "the instrument citation SHALL resolve to an
instrument in force".

The change's central claim is that consent, not our own ratification,
authorizes standing in another party's tenant. FR-014 encodes it with TWO
clauses: the entry names both roots, AND the consent citation resolves to an
instrument in force. Only the first is implemented: 2.8 refuses an entry with no
instrument, and nothing resolves the citation. The same gap sits on
`ratified_by`: "names no ratified capability" (delta) has an absence reading and
a non-resolution reading, and the corpus currently spends two probes (a packaged
negative AND repo fixture 2) on the absence reading alone.

Resolution belongs in layer 2 and is INTRA-REPO, exactly like FR-011's gate
obligation and unlike FR-037's cross-repo `evidence_ref`: a domain's consent
instruments live in the target repo (the BC chain's own
`tenants/farheap-bc-administration-consent.yaml` is the worked example), so no
repository boundary is crossed and hermeticity is untouched.

*Fix applied*: `consent_ref` and `ratified_by` RESOLUTION added to 2.9's
repo-context rules and to plan.md Cluster B / research.md Decision 7; "in force"
fixed as the consent family's own executed-or-amended states (never `draft`,
`pending_signatures`, `terminated`, `withdrawn`) and recorded in the plan's
open-decisions list for architect review; repo fixture 2 sharpened to the
NON-RESOLUTION case (so it and its packaged sibling become a discrimination
rather than two probes for one rule); and a SIXTH repo fixture added for an
unresolvable consent citation, with the counts and the FR-014 coverage row
updated. spec.md FR-014 now states that resolution is intra-repo, against the
target repository, so no implementer reaches across repos to satisfy it.

### F-023 — MEDIUM — the contested-classification rule has no test

*Artifacts*: tasks.md 6.6 (test list: both finding classes, the FR-024
non-finding, both skips, no intra-repo code, determinism) — against FR-023's
"MUST classify a finding that contradicts a ratified capability as contested
rather than auto-fixable" and US5 acceptance scenario 5.

The classification is authored at 6.3 and measured by nothing. A `Finding` that
silently keeps the dataclass default (`auto-fixable`) would pass every test in
6.6's list while inverting the rule doc-health's disposition machinery depends
on.

*Fix applied*: 6.6's test list now carries the resolution-class assertion — a
finding contradicting a ratified capability is `CONTESTED`, a finding that does
not keeps the default — with the fixture that produces the contested case named
in 6.5.

### F-024 — MEDIUM — 6.7 asserts exit 0 over fixtures 6.5 never requires to be conformant

*Artifacts*: tasks.md 6.5 (three fixture repos) and 6.7 (ruling A-N4: run the
roster validator over each, assert exit 0).

A-N4's whole point is that the shared identity is intra-repo CONFORMANT and the
finding is therefore composition-only. That holds only if each fixture
fragment satisfies every intra-repo rule — closed vocabularies, the legend,
verified admission, both roots, resolvable gate obligations. 6.5 asks only for
fragments that exercise the two finding classes and the skip, so a minimal
fixture (no `consent_ref`, no legend) makes 6.7 fail for reasons that have
nothing to do with what it measures.

*Fix applied*: 6.5 now requires every fixture fragment to be intra-repo
conformant and names 6.7 as the reason; 6.7 cites 6.5's conformance obligation
so the dependency is visible from both ends.

### F-025 — MEDIUM — FR-023's "registered … with a resolution class" reads as the blanket registry the design deliberately avoids

*Artifact*: spec.md FR-023, against plan.md Cluster G, research.md Decision 6
and tasks.md 6.3.

`FAMILY_RESOLUTION` (verified, `families.py:44-51`) assigns ONE class per
family. FR-023 simultaneously requires a resolution class at registration AND
contested-only-for-contradictions, which no blanket entry can satisfy; the
plan resolves it by staying out of `FAMILY_RESOLUTION` and setting
`resolution` per `Finding` (the three late families' precedent). The spec's
wording still points the other way, and a builder following it literally would
blanket-classify every finding as contested.

*Fix applied*: FR-023 now says the family is registered in `FAMILIES` (and
`FAMILY_IDS`) while each finding carries its own resolution class, naming why
the blanket registry cannot express the rule.

### F-026 — LOW/MEDIUM — FR-027's "no mutation" is asserted in a schema description and measured nowhere

*Artifacts*: tasks.md coverage row FR-027 → 1.9; 10.6 (boundary measurements:
no domain file modified, no credential minted, hermeticity guard active).

US6's Independent Test asks for exactly this confirmation ("no code path in the
feature can create, modify, widen, narrow, or remove an identity, permission, or
admission"), and 10.6 is where the feature's other boundary claims are measured.
A description in a schema is not a verification.

*Fix applied*: 10.6 extended with the FR-027 source-level confirmation (no
module in the feature writes to a roster fragment, a permission set, or an
admission record — the drift path reads and records only), and the coverage row
now reads 1.9, 10.6.

## Round 1 findings re-checked

All fifteen hold after their fixes; none regressed and none was re-opened by
this round's edits. Specifically re-verified: no hyphenated member spelling
survives outside prose and kebab-case FILE names (which follow the tree's
fixture-naming convention); the legend rule set is exactly FR-034's two
findings with exactly two negatives; `tests/doc-health/test_suite.py` is now
listed only under NOT EDITED, matching its measured content; and the
27/16/13-2-1 counts still reconcile.

## Escalations

None. F-020 and F-022 both encode ratified text that was under-encoded (ruling
R7's alias predicate; FR-014's and the roster delta's resolution clause) — no
fix required changing a ruling, a ratified constraint, Decisions A or B, or any
packet text.
