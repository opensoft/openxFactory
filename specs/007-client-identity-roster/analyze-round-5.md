# Analyze round 5 — 007-client-identity-roster

Date: 2026-08-14. Final round under the loop's five-round cap. Run fresh
against the post-round-4 artifacts, with the residual-pattern sweep clean (no
"legend entry never used", no "or its roster sibling", no unqualified
"(task 3.x)", no "FIVE tmp_path", no "six vocabulary negatives", no
"enforcing_check", no "both roots resolvable") and both `openspec validate`
invocations green.

This round attacks one question the earlier rounds under-asked: **is every rule
implementable from the record the plan declares, without a provider catalogue,
a network call, or an invented heuristic?** Four findings, all in that class —
three of them pre-existing gaps the earlier rounds walked past, one introduced
by round 2's own `consent_ref` addition.

## Findings

### F-036 — MEDIUM — the `consent_ref` resolution added in round 2 names no mechanism

*Artifacts*: spec.md FR-014, plan.md Cluster B, research.md Decision 7,
tasks.md 2.9, 4.5 fixture 6, 6.5 — all as edited in rounds 2–3.

Every other repo-context rule names its mechanism (the gate obligation resolves
against `workflows/<name>.yaml`; the sweep matches `kind:
xfactory_client_identity_roster` outside `credentials/client-identity-roster/`).
The consent resolution says only "against the target repo's own
consent-instrument records" — no kind, no matched field. Measured: the
consent family has no declared placement in a domain repo, and its own
validator finds instruments by sweeping the target for `kind:
xfactory_consent_instrument` (`contracts/schemas/consent-instrument.schema.yaml:62`),
with `instrument_id` (`:63`) the record's identity.

*Fix applied*: the mechanism is named in all four artifacts — a kind sweep for
`xfactory_consent_instrument` over the target repo (the consent validator's own
mechanism, `SKIP_DIR_NAMES` and all), matching `consent_ref` against the
record's `instrument_id`, and reading `status` for "in force". 6.5's fixture
obligation and 4.5's fixture 6 inherit the same wording.

### F-037 — HIGH — `granted_permissions[]` as bare strings makes FR-004 and FR-009 unimplementable

*Artifacts*: plan.md Cluster A (`granted_permissions[]` | "provider-native
strings, `minItems: 1`"), tasks.md 1.5 and 2.6 — against spec.md FR-004,
FR-009 and the Assumptions block.

FR-004 requires `authority_class_achieved` to be "checkable against"
`granted_permissions[]`, and FR-009 requires undeclared reach to be reported
"naming the surface and the permission that reaches it". Neither is decidable
from a list of opaque provider strings unless the validator either resolves
them against a provider catalogue (forbidden: network-free, FR-029) or infers
class and reach from the identifier's spelling (an invented heuristic about
provider semantics, which the neutral layer has no standing to make and which
SC-011's determinism standard would carry only by accident).

The spec already says which way this goes, in the Assumptions block: "the
mapping from a permission identifier to an achieved authority class **is
declared in the record** and checked for internal consistency, not resolved
against any provider catalogue". The plan's bare-string shape contradicts its
own spec's assumption, and 4.4's negative
(`achieved-class-contradicted-by-permissions.yaml`, ruling A-11's addition) has
nothing to contradict.

*Fix applied*: each `granted_permissions[]` member is an OBJECT — `id` (the
provider-native identifier, verbatim, which is what ruling R7 protects),
`achieves` (`observe|mutate`), and `reaches[]` (admission-surface members) —
so FR-004 is "`authority_class_achieved` equals the maximum declared
`achieves`" and FR-009 is "every `reaches[]` member is the entry's own surface
or a declared `spanned_surfaces[]` member", both record-internal and
deterministic. Recorded in plan.md Cluster A, its decisions list, and tasks 1.5
/ 2.6 / 3.2, with the alias rule's "same `granted_permissions[]` SET"
(FR-038) read over normalized member tuples.

### F-038 — MEDIUM — `per_unit_principal_available` is declared as a bare boolean where FR-008 requires it per surface

*Artifacts*: plan.md Cluster A ("boolean, per surface"), tasks.md 1.7 (same).

FR-008 and the roster delta both say "Each entry SHALL declare, **per admission
surface**, whether a principal scoped to the governed blast-radius unit is
available" — and the multi-surface reader (FR-019, SC-002's fourth positive)
is precisely an entry whose reach spans two surfaces, where one answer cannot
serve both. "Boolean, per surface" reads as a bare boolean to an implementer,
and a bare boolean cannot express the mandated case.

*Fix applied*: declared as a MAPPING keyed by `admission_surface` member with
boolean values, covering the entry's own surface plus every
`declared_excess.spanned_surfaces[]` member; the FR-008 rules read the entry's
surface key, and the multi-surface positive declares both.

### F-039 — MEDIUM — FR-010's "name or stated purpose" reads a field the ratified record does not have

*Artifacts*: spec.md FR-010, plan.md Cluster B, tasks.md 2.6 ("a name or stated
purpose describing narrower authority than it achieves refused"), with the
packaged negative `name-understates-achieved-authority.yaml`.

The ratified field list (FR-001, packet task 2.1) carries no `purpose` field, so
"stated purpose" resolves to nothing and the rule can only read `identity_ref` —
the identity's own provider-facing name, which is exactly where the worked case
lives (`opsx-farheap-bc-observer` achieving mutation). No artifact says that,
and none says how a name is judged to "describe observation", leaving the
feature's most quotable finding to an unstated heuristic.

*Fix applied*: the rule is stated as operating on `identity_ref` (the record has
no other name-bearing field), fired in ONE direction only — an
observation-suggesting token in the name while `authority_class_achieved` is
`mutate` — against a SMALL CLOSED token list declared in the validator module
and inspectable there (`observer`, `observe`, `reader`, `read`, `readonly`,
`viewer`, `audit`), matched case-insensitively on word boundaries. Deterministic,
inspectable, and conservative: it cannot fire on a `mutate`-named entry and it
names the token it matched. Recorded as a plan-phase decision for architect
review rather than buried in the validator.

## Loop status at the cap

Round 5 found four findings and fixed all four; the loop therefore reaches its
five-round cap WITHOUT a formally zero round. Nothing is known to remain
unfixed — the four fixes above are applied in full, and the residual-pattern
sweep, the identifier sweep, the count reconciliation and both `openspec
validate` runs are clean.

What a sixth round would look at, stated so the next reader inherits the
thread rather than the illusion of completion: the same implementability
question, pushed one level further into the rules that read `admission[]`
(effective-reach union and the `achieved_scope` comparison across acts), where
`achieved_scope` is provider-native by ruling R7 and therefore comparable only
as an opaque token — which is sufficient for the alias rule's equality test and
for the per-unit pair's INEQUALITY test, and is the reason no finding is raised
here, but is worth one deliberate look before implementation begins.

Every plan-phase shape decision this round introduced is listed in plan.md's
"Decisions this plan makes" section (items 21–23), which is the architect's
review surface for them.

## Escalations

None across all five rounds. No fix required changing a ruling, a ratified
constraint, Brett's Decisions A or B, or any packet text.
