# Gate-panel rulings — 007-client-identity-roster, pre-implementation gate

Date: 2026-08-15. Seat: architect. Status: **ruled — apply all fixes below,
then the gate closes.**

Provenance: 5 closed-world lenses → 49 findings → refute-biased triage killed
36 → 13 survive-verdicts collapsing to 9 distinct → final independent
refuters: 8 CONFIRMED, 1 REFUTED (SR-05, leaving one editorial gloss).
Verdict records live in the panel/triage/refuter transcripts; the confirmed
substance is restated here in full so this file alone suffices.

Two fixes amend the OpenSpec packet (G5, G7). Both are realization-fidelity
completions INSIDE capabilities the ratified change already declares MODIFIED
(consent-instrument; doc-health) — the archive operates per REQUIREMENT, so a
declared capability still silently rewrites (or deletes) any promoted
requirement its delta fails to restate. Both are therefore architect-level,
flagged to Brett in the gate report. Record-immutability discipline applies:
amendments are recorded in a SIBLING review record, never an append.

## G1 — retired entries vs the in-force rule (RS-02 ≡ CI-2 ≡ SR-03, triple-lens)

FR-014's in-force resolution has no lifecycle scoping, so the ratified
cascade's own end state (withdrawal/termination → identity retirement, with
FR-013 mandating the retired entry RETAIN its record) leaves the blocking
gate permanently red. FIX: scope FR-014 — every entry's `consent_ref` MUST
RESOLVE to an instrument record; for entries with `lifecycle_state: retired`
the instrument need NOT be in force (an ended instrument is the expected
state); all other entries require `executed|amended`. State it in spec.md
FR-014, plan.md Cluster B, tasks.md 2.9. Fixtures: the 3.5 `retired` positive
cites a `terminated` (or `withdrawn`) instrument and validates clean; a
non-retired entry citing that same instrument is refused (new negative if the
corpus lacks one; keep fail-for-its-own-reason discipline).

## G2 — the client-residency comparand (RS-03 ≡ VI-03, double-lens)

The `client_tenant_single` enforcement predicate has nothing to compare
`home_tenant` against (fragment carries only the `client_ref` slug). Two
candidate fixes were proposed; RULING: the DECLARED FIELD, not the
containment rule — a fragment-level `client_tenant` (provider tenant
identifier), because `home_tenant ∈ principal_locations[]` cannot catch an
identity homed in the WRONG client's tenant, and a declared comparand follows
the estate's fix pattern (F-037, F-040: declare the fact, never infer it).
Predicate: under `residency_model: client_tenant_single`, `home_tenant ==
fragment.client_tenant` AND every `principal_locations[]` member ==
`fragment.client_tenant`; finding names `home_tenant`. Add the field to
FR-001/Cluster A/task 1.x schema work; pin
`vendor-homed-declared-client-resident.yaml` to this code; the cross-domain
family MAY additionally check that two fragments for the same client declare
the same `client_tenant` (consistency, reported not blocking).

## G3 — the nested-placement hole (RS-09)

A roster instance at `credentials/client-identity-roster/<sub>/x.yaml` is
inside the misplacement predicate's directory-prefix reading and outside the
flat validating glob — covered by nothing, violating SC-005 and narrowing
ruling R1 in transit (the spec is internally split: FR-036 carries the prefix
reading; R1/SC-005/spec.md:465-468 carry the file-pattern reading). FIX =
exact-path predicate (option B), NOT recursive validation: reword FR-036,
plan.md:537-539, tasks.md:482-484 so misplacement = any `*.y*ml` file
carrying the kind that is not a DIRECT CHILD of
`credentials/client-identity-roster/` — the two passes exactly complementary
over the same `*.y*ml` universe. Add repo fixture 7 (nested instance →
nonzero, `misplaced-roster-instance`); extend plan.md:736 rule row and the
SC-005 measurement; amend CHK1212 (its "hardest placement" is now the
inside-but-nested case). Fixture lives under `tests/` so the self-scan
exclusion keeps `tasks.md:505-508` green.

## G4 — the shared-identity-material disjunct (VI-05 ≡ SR-04, double-lens)

The second disjunct reads "same provider-native application identifier in
`principal_locations[]`", but that field carries TENANT identifiers — read
literally the disjunct intersects on the shared client tenant and refuses the
ratified FR-024 non-finding. RULING: adopt the FIELD option, not deletion —
add optional entry field `provider_object_ref` (provider-native object
identifier, e.g. Entra `app_id`; the BC identity evidence record carries
exactly this). The disjunct fires only when BOTH entries declare it and the
values are equal; `identity_ref` equality remains the first disjunct.
Fixtures: a 6.5 cross-domain fixture with equal `provider_object_ref` under
different `identity_ref` spellings → `shared-identity-material`; the FR-024
discrimination fixture stays a non-finding. Update tasks.md 6.3,
research.md decision 6, plan.md decision 8, and the field lists.

## G5 — the missing consent-lifecycle MODIFIED requirement (CI-1) — PACKET AMENDMENT

Proven by EXECUTED archive on a scratch copy: the promoted consent spec's
"The Lifecycle Enum Is Closed With Declared Aliases" (five states) survives
archive untouched — the delta names only the cascade requirement — so the
promoted capability would contradict itself and the shipped six-member enum.
FIX: append to `openspec/changes/add-client-identity-roster/specs/consent-instrument/spec.md`
under the existing `## MODIFIED Requirements` EXACTLY this requirement
(validated end-to-end by the refuter: strict valid, --all 58/58, archive
yields the six-state lifecycle in place):

```markdown
### Requirement: The Lifecycle Enum Is Closed With Declared Aliases
The instrument status SHALL be the closed six-state lifecycle `draft →
pending_signatures → executed → amended → terminated`, with `withdrawn` a
second terminal state reachable once the instrument is past execution;
`withdrawn` is a DISTINCT member and MUST NOT be declared as an alias of
`terminated`, because withdrawal by the consenting party and termination are
distinct events that both raise the cascade obligation. A domain spelling
outside the enum maps via an alias DECLARED at conformance time, and a class
may skip `pending_signatures` only when its class declaration says so —
class-appropriate skipping, never silent.

#### Scenario: A domain alias maps at conformance time

- **WHEN** the Ledgerx record carries `status: active`
- **THEN** its conformance declaration maps `active` → `executed`
- **AND** the underlying record keeps its domain spelling

#### Scenario: A non-signature class enters executed directly

- **WHEN** a `portal_acceptance` instrument is accepted
- **THEN** it may enter `executed` without `pending_signatures` because
  its class declares no signature phase
- **AND** an undeclared skip is nonconformant

#### Scenario: Withdrawal is its own terminal state, never an alias

- **WHEN** a consenting party withdraws an executed instrument
- **THEN** the record carries `status: withdrawn`, not `terminated`
- **AND** a class registry declaring `withdrawn` as an alias of `terminated`
  is nonconformant
```

RIDERS (same edit window): (a) extend proposal.md's consent-modification
description (~line 178) to name the lifecycle growth — it currently
understates the modification exactly as the pre-Decision-A text understated
the pack; (b) add two prose sites to task 8.x's sweep:
`scripts/validate-consent-instruments.py:356`'s "closed five-state enum"
message and `contracts/schemas/consent-instrument.schema.yaml:195`'s
"CLOSED five-state lifecycle" comment; (c) correct research.md:554-557 and
plan.md decision 15 to say the archive rewrites only requirements a delta
carries (root cause: ruling N1 conflated capability-level declaration with
per-requirement archive mechanics — note this correction against N1 in the
amendment record).

## G6 — FR-010's missing cure conjunct (SR-01)

spec.md contradicts itself: US1 acceptance scenario 4 mandates
cure-on-declaration (ratified verbatim) while FR-010's operational rule is a
bare two-conjunct trigger — as written it fires on the mandated BC positive
that three artifacts require to validate with zero findings. FIX: add the
cure conjunct at spec.md:664-669, plan.md:1279-1285, tasks.md:409-415 — the
name finding fires only when (observation token AND `authority_class_achieved:
mutate`) AND the entry declares no `declared_excess` covering the class
overshoot ("covering" = present, since `declared_excess` is a single object;
if a per-excess split ever lands, re-key to the class-overshoot member).
Specify the negative sharply: `name-understates-achieved-authority.yaml`
carries `authority_class_intended: mutate` AND `authority_class_achieved:
mutate` with an observation-suggesting `identity_ref` and NO
`declared_excess`, so the name code fires ALONE (fail-for-its-own-reason;
with intended=achieved there is no excess to declare, hence no cure).
State FR-010's post-cure residual explicitly: an honestly-declared `mutate`
identity with a misleading name has no declarable excess and must be renamed.
Add the missing parenthetical at tasks.md:637; check plan.md:749.

## G7 — the doc-health delta rebase (XCC-1, CRITICAL) — PACKET AMENDMENT

Proven three ways (tool source, live buildUpdatedSpec execution, 8/8
replacement across the archive history): archiving the current 2-scenario
delta DELETES six promoted scenarios and guts the seventh. FIX: replace the
delta's "Deterministic check families" MODIFIED block with the rebased
version the refuter built and validated — restate all SEVEN promoted
scenarios verbatim (including the five THEN/AND bullets of "A run executes
the check families" with the per-repo+preflight coverage clause and the
"reported as skipped, never silently omitted" clause), sixteen-family
enumeration (already present at delta lines 6-12), append the new
roster-composition scenario, and add ONE owning-requirement AND-bullet whose
target is `client-identity-roster`'s "The roster composes across domains from
published fragments" requirement (NOT a doc-health-internal requirement —
none exists for this family, the bullet would dangle). The refuter's working
cure is at
`/tmp/claude-1000/-home-brett-projects-xFactory-xFactories-OpsxFactory/af342a91-d20e-4518-ae91-43c3ec1e3ccd/scratchpad/xcc1-sandbox/fix/rebuilt-fixed.md`
— verify it against the promoted spec yourself before adopting text from it.
Add a tasks.md assertion task: before archive, the doc-health delta is
verified rebased onto the promoted scenario set (precedent:
archive/2026-08-04-add-ideation-cross-reference-readiness/tasks.md:5).

## G8 — the document-catalog false-red (XCC-2)

The feature's own new/edited governed docs trip the aggregation
document-catalog family on THREE arms (coverage for the new README;
stale-entry for CHANGELOG/README edits; revision re-staling at merge), making
FR-025's "doc-health MUST report no new finding against the feature"
unmeetable as worded — while the state is lagging aggregation-catalog data
cured mechanically by the nightly merge phase (one-cycle self-heal, proven by
the openxdox-naming.md precedent). FIX (primary = qualification, not a run):
at FR-025 (spec.md:841-843), tasks.md:1114-1116 (task 10.3), and
plan.md:1122-1124, narrow the green condition to exclude the
`document-catalog` family's `coverage` and `stale-entry` finding classes
against this change's documents, naming them as lagging catalog state cured
by the nightly catalog lane, citing the one-cycle precedent. OPTIONAL
demonstration task only if cheap: run the merge phase in a THROWAWAY
aggregation checkout (`--catalog-unavailable-reason worker_unavailable`);
NEVER in the shared `/home/brett/projects/xFactory` checkout (it would leave
uncommitted runs/ and .sequence/ state the porcelain guard does not cover).

## G9 — editorial residual from refuted SR-05

One-clause gloss: spec.md:379's "reach into a surface a domain did not
declare" → "reach into a surface a domain publishes no entry for", aligning
the US5 narrative with the three operative predicate sites. Nothing else
about SR-05 is adopted — the predicate itself was upheld as deliberate and
correct.

## Not escalated to Brett (and why) — but reported

G5 and G7 amend the ratified packet; both complete the realization of
capabilities the ratified proposal ALREADY declares modified, per the
archive's per-requirement mechanics. No new capability is declared, no
ratified position changes, no scope is added or reduced. They are the same
class as the encode-phase amendment that Decisions A+B authorized in kind —
carrying declared modifications faithfully into delta text. Both are flagged
in the gate report so Brett can overrule.
