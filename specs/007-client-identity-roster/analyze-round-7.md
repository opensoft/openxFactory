# Analyze round 7 — 007-client-identity-roster

Date: 2026-08-14. Fresh full-dimension pass over the post-round-6 artifacts,
with the previous 43 fixes treated as attack surface. Round 6's four fixes
compose correctly through the rule text, the task bodies, the fixture lists and
the counts (verified: plan's negative tree holds 28 entries and claims 28; 31
rule-homes; 33 probes; task 4.1 says SEVENTEEN and lists seventeen filenames) —
but they did NOT compose through three SUMMARY surfaces that restate the record
in shorter form, which is where this round's findings are.

## Findings

### F-044 — MEDIUM — Key Entities still describes the admission act and the declared excess without the facts rounds 5–6 added

*Artifacts*: spec.md Key Entities, "Admission act" ("surface, act, achieved
scope, enforcement mode, evidence of a successful call, and verification time")
and "Declared excess" ("the record of provider-forced breadth or achieved-class
overshoot").

Key Entities is the section a reader consults for what a record CONTAINS, and
it is the only place in the spec that enumerates the act's contents in one
breath. It now under-describes both:

- the act no longer stops at verification time — it declares
  `exceeds_governed_unit`, which is what makes the union computable and the
  degradation checkable (FR-002, FR-003);
- the declared excess is no longer only about surfaces and class — a SCOPE
  excess inside one surface (the worked case's no-selector act) is now the
  third thing it covers, and is the one the change exists for.

A reader who builds from Key Entities alone would author a record that fails
2.5's rule and cannot express SC-003's worked case.

*Fix applied*: both entities restated to carry the added facts, with the
"union, not the narrower act" derivation named on the act and the scope excess
named on the declared excess.

### F-045 — MEDIUM — the Constitution I gate asserts an opacity the design no longer has, which is the one row that must be exact

*Artifact*: plan.md Constitution Check, row I ("… `granted_permissions[]` /
`achieved_scope` stay provider-native and opaque to the neutral layer").

Row I is the constitutional gate for "contract-first, domain-neutral core" — a
PASS asserted on a description of the design, so the description has to be the
design. After F-037 and F-040 it is not: `granted_permissions[]` members carry
NEUTRAL annotations (`achieves`, `reaches[]`) beside the provider-native `id`,
and each admission act carries one neutral fact about its provider-native
`achieved_scope` (`exceeds_governed_unit`). Both are governed, deliberate and
argued — and both are precisely the kind of neutral-layer claim about provider
values that this principle exists to police, so leaving the row saying
"opaque" hides the very thing an architect reviewing the gate should look at.

The design still passes, and for a stronger reason than the old row gave: the
provider-native values are never INTERPRETED by the neutral layer — the
identifier rides verbatim in `id`, the scope token rides verbatim in
`achieved_scope`, and every neutral fact about them is DECLARED by the domain
that owns the fact rather than inferred from its spelling.

*Fix applied*: row I restated to say exactly that, naming both annotations and
the reason the PASS holds (declaration by the fact's owner, never inference by
the neutral layer).

### F-046 — LOW/MEDIUM — the Assumptions block covers the class mapping but not the surface-reach declaration FR-009 now reads

*Artifact*: spec.md Assumptions ("the mapping from a permission identifier to
an achieved authority class is declared in the record").

F-037 added TWO declared facts per permission, because FR-004 and FR-009 each
need one: `achieves` (the class) and `reaches[]` (the surfaces). The Assumption
— which is the sentence that justified the whole object form — names only the
first, so FR-009's check appears to rest on nothing.

*Fix applied*: the assumption names both declarations and the requirement each
serves.

### F-047 — LOW — plan.md's worked-case paragraph omits the exceedance declaration its own rule now requires

*Artifact*: plan.md Cluster D (the BC transcription paragraph), against
tasks.md 3.2, which round 6 updated.

The plan describes the second act as "the tenant-wide admin-center Entra-app
authorization with no scope selector" and the entry as carrying a declared
excess, but never says the act declares `exceeds_governed_unit: true` — so the
plan's own worked case would, read literally, trip the rule the plan added two
clusters earlier.

*Fix applied*: the paragraph names the declaration and its discrimination
partner (`scope-exceeds-unit-undeclared.yaml`).

## Dimension sweep result

- **Requirement coverage**: FR-002/FR-003/FR-010 rows carry the new task and
  fixture; every FR and SC still maps to at least one task; FR-016's 16 named
  rules remain 16 homed.
- **Terminology**: `exceeds_governed_unit` spelled identically across spec (3),
  plan (9), research (1), tasks (7); no new closed vocabulary; snake_case
  dialect intact.
- **Constraint fidelity**: no ratified text contradicted; the FR-038 alias
  tuple keeps its four ratified elements with the new flag explicitly excluded;
  `achieved_scope` and permission identifiers still ride verbatim.
- **Dependency soundness**: field (1.6) → rule (2.5) → positive (3.2) →
  negative (4.1) is the existing phase shape; no ordering changed.
- **Ambiguity residue**: counts reconcile (28/31/33, seventeen in 4.1); the
  rule is scoped to VERIFIED acts, matching FR-003's exclusion of unverified
  ones.

## Escalations

None.
