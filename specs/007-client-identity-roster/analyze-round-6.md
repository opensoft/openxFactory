# Analyze round 6 — 007-client-identity-roster

Date: 2026-08-14. Continuation round (the loop runs to ZERO, not to the earlier
cap). Leads with the question round 5's record named and then re-runs the full
dimension set fresh, treating the previous 39 fixes as attack surface.

## Lead question: is opaque-token comparison sufficient for every rule that touches `achieved_scope`?

`achieved_scope` is provider-native by ruling R7 and therefore comparable only
as an OPAQUE TOKEN: two tokens are equal or unequal, and nothing in the neutral
layer may read breadth out of one. Every rule that touches it was enumerated
from the artifacts and tested against that limit.

| Rule | What it needs of `achieved_scope` | Sufficient? |
|---|---|---|
| Alias rule (FR-038): "same admission acts by (surface, act, `achieved_scope`, `enforcement_mode`)" | EQUALITY of tokens | YES — equality is exactly what the predicate asks |
| Genuine per-unit pair (FR-017, SC-002): two entries "differing in `achieved_scope`" | INEQUALITY of tokens | YES |
| Uniqueness tuple (FR-006) | does not read `achieved_scope` | n/a |
| Drift record (FR-035): `roster_value` / `observed_value` | carries tokens verbatim | YES |
| Per-unit principal / enforcement (FR-008) | reads `per_unit_principal_available` + `enforcement_mode` | YES — no scope reading at all |
| Undeclared reach (FR-009) | reads each permission's `reaches[]` (F-037) | YES |
| Achieved-vs-intended class (FR-004, FR-010) | reads `achieves` (F-037) | YES |
| **Effective reach as "the union, NOT the narrower act" (FR-003, US1 scenario 3, roster delta)** | must know that a no-selector act's scope EXCEEDS the governed unit | **NO — see F-040** |
| **Declared excess on the worked case (FR-010, SC-003)** | must know the tenant-wide act reaches beyond `sandbox1` | **NO — see F-040** |

Eight of ten are sufficient on token comparison alone; the two that are not are
the same fact, and it is the fact this change exists to expose.

## Findings

### F-040 — HIGH — the structural→logical degradation has no firing rule, because the fact it needs is in no field

*Artifacts*: spec.md FR-002 / FR-003 / FR-010; plan.md Cluster A
(`admission[]` members) and Cluster B (2.5's rules); tasks.md 1.6, 2.5.

The ratified proposal's second measured input is the reason this change exists:
"Some second keys silently convert structural bounds into logical ones … A
degradation of this kind must be a **declared, checkable, tested** fact"
(proposal.md, Why §2). The roster delta mechanizes it as "the effective reach is
the union, **not the narrower act**", and the worked case is exactly it: act 1
is a per-environment application user in Sandbox1 (provider-enforced), act 2 is
the admin-center Entra-app authorization with NO SCOPE SELECTOR, reaching every
environment in the tenant.

Measured against the artifacts as they stand, nothing fires when that second
act's excess is NOT declared:

- FR-009's undeclared-reach rule is about SURFACES (now checkable through a
  permission's `reaches[]`), not about a scope inside one surface.
- FR-010's excess rule is about CLASS (`authority_class_achieved` vs
  `_intended`), now checkable through `achieves`.
- FR-008's rules read `per_unit_principal_available` and `enforcement_mode`;
  for `business_central` a per-unit principal both EXISTS and is USED (by act
  1), so the per-surface rule is satisfied while act 2's tenant-wide reach goes
  unexamined.

So an entry may declare a no-selector, tenant-wide act, omit `declared_excess`
entirely, and pass every rule in the corpus. The degradation is declarable but
not checkable — and "checkable" is the ratified word.

It cannot be fixed by reading the token: `achieved_scope` is provider-native and
opaque, so "Sandbox1" versus "all environments in this tenant" are two unequal
strings and nothing more. Comparing the token to the legend's binding for the
entry's `blast_radius_unit` would detect DIFFERENCE, not EXCESS, and would fire
on a legitimately NARROWER act — a false positive on the permissive axis.

*Fix applied* (the F-037 pattern — declare the fact, do not infer it): every
`admission[]` member additionally declares **`exceeds_governed_unit`**
(boolean, required) — whether the scope that act achieves reaches BEYOND the
entry's `blast_radius_unit`. It is an addition to the act's ratified field list
on the same footing as the legend and `duty_separation_rationale`: the ratified
requirement cannot be evaluated without it. It changes no ratified spelling —
`achieved_scope` stays provider-native and verbatim (ruling R7) — and the
FR-038 alias tuple stays EXACTLY the four ratified elements; the flag is not
part of observational identity.

Two consequences encoded with it:

1. **The rule that now fires**: a VERIFIED act declaring
   `exceeds_governed_unit: true` REQUIRES `declared_excess` carrying its four
   fields; absent, the finding `undeclared-scope-excess` names the act, its
   achieved scope, and the governed unit it exceeds. New packaged negative
   `negative/scope-exceeds-unit-undeclared.yaml` (task 4.1), with the worked
   case (3.2) as its discrimination partner — same shape, excess declared,
   zero findings.
2. **The union becomes computable** (F-041).

### F-041 — MEDIUM — "effective reach is the union, computed never declared" names neither what the union IS nor where it is reported

*Artifacts*: plan.md Cluster A ("Effective reach is the union of verified acts,
computed, never declared"); tasks.md 2.5 ("effective reach is COMPUTED as the
union of verified acts, never declared"); against spec.md FR-003 ("effective
reach MUST be the union of verified acts") and US1 scenario 2 ("the effective
reach REPORTED is the union of the VERIFIED acts only").

"Union" over opaque tokens is undefined until someone says what is being
unioned, and the spec requires the result to be REPORTED — so a validator that
computes nothing and prints nothing satisfies neither. As written, two
implementers produce two different artifacts, and US1 scenario 2's measurement
has nothing to read.

*Fix applied*: the union is defined concretely and its report site named — the
set of `(surface, achieved_scope)` pairs over VERIFIED acts only, plus the
derived flag `exceeds_governed_unit = OR over verified acts` (F-040), emitted
as a per-entry note line by the validator. That derived OR is precisely the
delta's "the union, not the narrower act": one verified no-selector act makes
the whole entry's reach exceed the governed unit, whatever the narrower act
says, and it is now computed rather than asserted.

### F-042 — MEDIUM — three sites still describe FR-004's negative in pre-F-037 terms, re-implying the inference F-037 removed

*Artifacts*: plan.md Cluster C (`achieved-class-contradicted-by-permissions.yaml`
… "while its `granted_permissions[]` carry a write/delete permission");
research.md Decision 7 (same, "write- or delete-capable permission"); tasks.md
4.4 (same).

Round 5's F-037 made `granted_permissions[]` members objects carrying a DECLARED
`achieves`, precisely so no rule reads provider semantics out of an identifier's
spelling. These three descriptions still define the negative by what the
permission "is" (write-capable), which an implementer can only determine by
reading the string — the inference F-037 exists to forbid. The fixture would
then be authored to trip a rule that no longer exists.

*Fix applied*: all three restated in the object form — the entry declares
`authority_class_achieved: observe` while a `granted_permissions[]` member
declares `achieves: mutate`, so the contradiction is between two declarations in
the record and the check is a comparison, not a reading.

### F-043 — LOW — the alias predicate's "same `granted_permissions[]` SET" is spelled without the member form in two of its three sites

*Artifacts*: plan.md Cluster B (alias rule), tasks.md 2.4 — against plan.md
Cluster A, which since F-037 states the comparison as normalized member tuples
`(id, achieves, sorted(reaches))`.

With members now objects, "same SET" is ambiguous about what is compared (ids
only? whole objects? order-sensitively?), and comparing whole mappings
order-sensitively would break a legitimate pair.

*Fix applied*: both sites now say "the same `granted_permissions[]` set,
compared as normalized member tuples `(id, achieves, sorted(reaches))`", which
is what Cluster A already fixed. spec.md FR-038's ratified-facing wording ("the
same `granted_permissions[]` set") is left as is — it is the requirement, and
the normalization is its implementation.

## Full dimension re-run (fresh)

- **Requirement coverage**: the new rule is homed (1.6 declares the field, 2.5
  enforces it, 4.1 carries its negative, 3.2 is its discrimination partner) and
  the FR-002/FR-003/FR-010 coverage rows updated. FR-016's sixteen named rules
  remain 16 homed / 0 unhomed — the new negative is one of the "at minimum"
  additions, not a named rule.
- **Terminology**: `exceeds_governed_unit` spelled identically in all four
  artifacts; snake_case member dialect preserved; no new closed vocabulary
  introduced (a boolean, deliberately, so FR-034's six closed sets — a list
  derived from ruling R7 — stay six).
- **Constraint fidelity**: no ratified text contradicted. The addition is
  justified by the ratified "declared, checkable, tested" and is recorded as
  such; `achieved_scope` remains provider-native; the FR-038 alias tuple keeps
  exactly its four ratified elements.
- **Dependency soundness**: no ordering changes — the field lands in Phase 1,
  its rule in Phase 2, its negative in Phase 4, its positive in Phase 3, which
  is the existing shape.
- **Ambiguity residue**: counts re-reconciled after the 28th packaged negative
  (below).

**Counts after this round**: packaged negatives 27 → **28**; task 4.1 sixteen →
**seventeen** files (twelve FR-016-named + five "at minimum" confirmations);
rule-homes 30 → **31**; refusing probes 32 → **33**. FR-016's own count is
untouched at 16 named / 16 homed / 0 unhomed.

## Escalations

None.
