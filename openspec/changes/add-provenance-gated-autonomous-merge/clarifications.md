# Clarifications

_Captured during the `opsx:propose` alignment review and council debate on
2026-08-28. These constrain the design and the downstream codexFactory
realization. Open questions at the end need the convener's ruling._

## Alignment review outcome (2 agents: stack-architect + qa-lead)

- **MISMATCH (fixed):** the change's `.openspec.yaml` lacked the required
  `origin:` block (mechanically enforced by `document-lifecycle` "Proposal
  origin declaration") and carried a future `created:` date. Added an `ad_hoc`
  origin and set `created: 2026-08-27`.
- **DRIFT (fixed):** front-matter over-claimed a present-tense edit to
  `docs/roles-and-authority.md`. Rescoped to the spec delta only; the projection
  lands on promotion, per the `add-wallet-carried-review-authority` precedent.
- **MISMATCH (fixed, load-bearing):** the task framing's "Q3 nil-diversity
  benefit finding" is a mis-citation — `add-substantive-review-lane` Q3 is the
  Company-policy-lead per-PR seating question, and the seat-diversity question
  (`seat_diversity_disposed_on_soak_evidence`) is PARKED for a future bench, with
  the seeded-corpus record explicitly warning that citing it for "diversity is
  unnecessary" is citing it wrongly. The proposal was reframed to rest on
  provenance-completeness and to take NO position on the parked question, citing
  no nil-benefit finding. See Open Question 1.
- **MISMATCH (fixed, load-bearing):** criterion (3)'s "advisory council verdict"
  collides with the ratified `classification_intent: advisory` rules-as-code
  value, which structurally forbids autonomous approval. Reconciled: "advisory"
  = the council's ROLE (it advises; Merge Master enforces) and the required
  green `council-verdict/merge-readiness` check-run; a real autonomous merge
  needs `clearable` intent under a widened definition-time predicate.

## Council-identified constraints (NOTED — for design.md and the realization)

### The scope check is the load-bearing safety claim and needs a real substrate
**Raised by:** adversary-engineer (Concern 1, HIGH), systems-architect (Concern 2, HIGH)
**Design impact:** "changed paths within the ratified change's scope" cannot be
checked against prose `code_surface` (repo-granularity per `release-realization`
`:7-8`). The realization DEPENDS ON a structured path-scope declaration
(glob allowlist) landing first, as a schema amendment or sibling field — itself
a human-gated `openspec/`-touching change. Prose/repo-level scope ⇒ ineligible,
never "all paths in scope". Encoded as a verifier requirement + a named
precondition. See Open Question 2.

### The tie anchor must be corroborated, not merely present
**Raised by:** adversary-engineer (Concern 3, HIGH)
**Design impact:** branch name and PR-body references are author-controlled. The
verifier must corroborate the tie against a base-read source the PR head cannot
author (a change/effort record read from base) AND require path-allowlist
containment; a string alone never establishes the tie. Encoded in the verifier
requirement.

### Floor primacy and per-repo floor instantiation
**Raised by:** systems-architect (Concern 1 & 3), adversary-engineer (Concern 2 & 5)
**Design impact:** the definition-time predicate is today the PRIMARY floor
enforcement via one union-judged walk over a class's whole allowlist. Widening it
to admit a broad, non-docs class must (a) route through that same walk; (b) state
explicitly whether the per-PR verifier becomes primary with the definition-time
floor as a mandatory backstop; (c) require each enrolling repo to publish its own
tree-validated floor (decision core, gate, workflow, credential, governance,
council-records) before any non-docs class is enabled — floor semantics are
tree-specific. Realization tests must include a negative fixture proving a
provenance-eligible class reaching `scripts/**` or `openspec/changes/**` is
refused at definition time, mirroring existing golden-characterization discipline.

### Ratification currency and record integrity
**Raised by:** adversary-engineer (Concern 4 MEDIUM & 5 MEDIUM), product-advocate (Concern 2, HIGH)
**Design impact:** `Status: ratified` is a mutable markdown field. The tie must be
re-resolved from the current base at clearance time (never cached), assert a
CURRENTLY-ratified (non-superseded, non-retired) state, and pin to the same
head/base SHA pair as the verdict so any base advance re-runs it. The council
ratification record must transport as a signed, identity-bound artifact (mirror
the verdict check-run), not a plain committed file. Encoded in the verifier
requirement + scenarios.

### Park legibility
**Raised by:** product-advocate (Concern 1, HIGH)
**Design impact:** the park record must name which of criteria (1)–(4) / verifier
sub-check (i)–(iv) failed, mirroring the existing "name the absent class" pattern.
Encoded as a verifier scenario.

### Multi-hop ordered-delta chains (deferred to realization)
**Raised by:** product-advocate (Concern 4, LOW-MEDIUM)
**Design impact:** a code PR built against a chain of ratified ordered-deltas may
not resolve to one single change. Left explicitly to the realization; noted in
the verifier bullet so the follow-on design is not blindsided.

### Submodule pin-lag (context, not a defect)
**Raised by:** stack-architect (alignment note), systems-architect
**Design impact:** scope the realization against codexFactory `origin/main`, not
the stale local `xFactories/codexFactory` checkout; the aggregation's next
pin-sync picks this up per the three-file invariant.

## codexFactory-realization disposition (VALID — recorded)

The codexFactory realization is a SEPARATE, dependent follow-on change, NOT tasks
inside this change. Rationale: it has its own code surface, its own reviewing
council/record, its own archive-on-green-evidence gate, and depends on a
human-gated `code_surface` schema precondition. This openxFactory change ships
doctrine only. tasks.md tracks the realization as an explicit downstream group
with no code performed here.

## Open questions for the convener

1. **The "Q3 nil-diversity-benefit" premise is not supported by the record.** The
   directive asked to address a finding that seat diversity showed nil measured
   benefit; the corpus shows that question is PARKED, not ruled, and warns against
   the "diversity is unnecessary" reading. The proposal now rests on
   provenance-completeness and takes no position on it. CONFIRM this reframing, or
   supply the specific record if a nil-benefit finding was in fact ratified
   elsewhere.

2. **Structured path-scope substrate — schema amendment vs sibling field.** The
   scope check needs a machine-readable path allowlist on ratified changes. Should
   this amend the `code_surface` contract in `release-realization`, or add a new
   sibling field? Either is a human-gated `openspec/` change and a hard
   precondition for the realization. Convener to choose the route (or defer to the
   realization proposal).

3. **Floor primacy for a broad provenance class.** If a provenance-eligible class
   carries a broad allowlist, the per-PR verifier — not the static definition-time
   predicate — becomes the primary floor enforcement. CONFIRM that shift is
   intended (with the definition-time floor retained as a mandatory backstop), or
   require provenance classes to keep narrow allowlists so the static predicate
   stays primary.

4. **Supersession evidence bar.** The interim gate sunsets via a named successor
   change raised on pilot evidence; the exact evidence bar is deferred to that
   successor rather than fixed here. CONFIRM deferral, or set the bar now.
