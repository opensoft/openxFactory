---
code_surface: openxFactory (this spec delta on `roles-authority-model` — the neutral eligibility doctrine — is this change's ONLY diff; it is a doctrine/authority-doc change with no code. The human-readable projection into `docs/roles-and-authority.md` lands only once this ordered delta and its base change `add-substantive-review-lane` are promoted/archived — it is NOT a standalone edit this change performs now, matching the `add-wallet-carried-review-authority` front-matter precedent). The codexFactory REALIZATION is downstream and explicitly NOT built by this change: the provenance-tie verifier, the class-floor guard in `scripts/merge_master/council_clearance.py`, an ORDERED-DELTA MODIFIED on codexFactory `merge-master-approval`'s definition-time `clearable`-eligibility predicate (today that predicate admits `clearable` intent ONLY for docs-/derived-shaped classes and is the primary enforcement of the floor — realizing a provenance-eligible code class requires widening it), and any `gate_rules_council` record wiring a provenance-eligible class are a dependent follow-on change tracked in tasks.md, archived only on merged, green realization evidence per release-realization.
target_release: none (no `contracts/schemas/` bundle artifact — this amends the neutral `roles-authority-model` authority doctrine and cross-repo rules-as-code; realization lands as a verifier + council-clearance + spec change in codexFactory under a separate change).
---

# Proposal: add-provenance-gated-autonomous-merge

Status: ratified
Authored: 2026-08-27, from the convener's ruling of the same date. This packet
was authored via `opsx:propose`; its alignment-review and council-debate gates
run against this draft before design/tasks are generated.
Directed by: Brett Heap (convener), 2026-08-27.

## Why

Autonomous clearance is ratified for exactly one shape of change. The
`add-substantive-review-lane` "Constitutional floor for autonomous clearance"
requirement (openxFactory `roles-authority-model`, ratified 2026-08-22) makes
autonomous clearance eligible **only for candidate classes whose blast radius
is docs- or derived-artifact-shaped** — today, exactly the proven docs class.
A real CODE pull request, however completely governed, is categorically
ineligible: blast-radius is the only admission axis, and code is not
docs-shaped.

The convener's end state is different: **when the entire build is governed and
watched from the proposal down and the whole pipeline is green, auto-merge is
mechanically safe for code — and its safety comes from the COMPLETE
TRACEABILITY CHAIN, not from review quality.** The design is deliberately
INDEPENDENT of review quality: its safety basis is the governed provenance of
the change — a mechanically verifiable, unbroken chain from a ratified proposal
down to a green pipeline — not the judgment or composition of whoever reviewed
it.

Because that safety basis does not depend on review quality, this design also
does not depend on the still-OPEN question of whether council seat diversity
improves review outcomes (`seat_diversity_disposed_on_soak_evidence`, PARKED for
a future bench — codexFactory `add-regular-pr-council-clearance` /
`hermes/domain/review-councils/records/2026-08-22-seeded-adversarial-corpus.md`).
This proposal takes NO position on that question and cites NO "nil-benefit"
finding: the seeded-corpus record explicitly warns that "anyone citing this
record for the proposition that seat diversity is unnecessary is citing it
wrongly" (`:359-364`), and openxFactory's own `add-wallet-carried-review-authority`
already declined to build an argument on it. The provenance axis needs neither
outcome of that question, which is precisely why it is a sound interim basis.

The full end-to-end pipeline is not built yet. This change proposes the DOCTRINE
for an **interim, provenance-gated eligibility path** so that a code PR whose
provenance is fully governed can become autonomously clearable now, under a
mechanically checkable criterion, with the full-pipeline-green end state named
as its documented successor. Ratifying this doctrine unlocks no autonomous merge
by itself: it requires `add-repo-enrollment`'s live enrollment canary, the
codexFactory definition-time-predicate widening, a machine-readable path-scope
substrate for the tie check (see below), and the new provenance-tie verifier —
all not yet complete — before any PR benefits.

## What Changes

- **A new, orthogonal eligibility axis for autonomous clearance.** Today the
  admission test is blast-radius alone. This change makes autonomous clearance
  eligible for a candidate **whose blast radius is docs-/derived-artifact-shaped
  (the existing axis), OR whose provenance is fully governed** (the new interim
  axis). The two axes are independent: a candidate qualifies if EITHER holds.
  Neither axis ever relaxes the never-clearable floor.

- **The interim provenance-completeness criterion, stated verbatim.** A code
  pull request MAY become autonomously clearable if and only if ALL of:
  1. the repository is **ENROLLED** (council enrollment via
     `.github/merge-approval-envelope.yml`);
  2. the PR is **TIED TO A RATIFIED PROPOSAL** — mechanically verified: PR head
     → its OpenSpec change → `Status: ratified` + a council ratification record;
  3. **ALL required checks are GREEN**, including the advisory council verdict =
     `ready`;
  4. the candidate is **STILL OUTSIDE the never-clearable floor** — the floor
     ALWAYS binds; a PR touching the decision core, the suites that prove it, or
     the gate/governance surfaces stays HUMAN-ONLY even when fully governed
     (this prevents a ratified proposal from auto-merging a change to its own
     checker).

  Two terms in criterion (3) are reconciled against the ratified rules-as-code
  vocabulary so the criterion is not read as self-defeating. "The advisory
  council verdict = `ready`" refers to the council's ROLE — it advises; the
  Merge Master stays the mechanical enforcer — and to the required green
  check-run `council-verdict/merge-readiness` carrying verdict `ready`. It does
  NOT mean the codexFactory `classification_intent: advisory` rules-as-code
  value, which is structurally incapable of producing an autonomous approval
  even on a unanimous `ready` verdict (`add-classification-intent-and-substantive-classes`,
  `specs/merge-master-approval/spec.md:26`). Realizing a real autonomous merge
  for a provenance-eligible code class therefore requires that class to carry
  `clearable` intent under a WIDENED definition-time eligibility predicate (see
  the next bullet and Impact), not `advisory`.

- **The never-clearable floor is restated as non-negotiable and unchanged.**
  The provenance axis is ADDITIVE to eligibility only; it grants nothing the
  floor forbids. Criterion (4) is the floor, binding identically on both axes.

- **The doctrine records that realizing the provenance axis requires widening
  the definition-time `clearable`-eligibility predicate.** Today codexFactory's
  ratified `merge-master-approval` makes a class eligible for `clearable` intent
  ONLY when every admitted pattern is within the docs-/derived-artifact shape,
  and that definition-time predicate is "the PRIMARY enforcement of the
  constitutional floor" (`add-classification-intent-and-substantive-classes`,
  `specs/merge-master-approval/spec.md:92`). So satisfying (1)–(4) cannot
  produce a real autonomous merge for code UNTIL that predicate is widened to
  admit a provenance-eligible, non-docs-shaped `clearable` class WITHOUT
  weakening the floor. This proposal states that widening as a REQUIRED part of
  the downstream codexFactory realization (an ordered-delta MODIFIED on
  `merge-master-approval`), so the interim path is genuinely buildable rather
  than doctrine that no realization can honor.

- **The floor stays PRIMARY, and its coverage is proven per enrolled repo — the
  widening never demotes it silently.** Today the definition-time predicate
  (a static, worst-case per-class judgment: is every path this class could ever
  admit docs-/derived-shaped?) is the PRIMARY floor enforcement, and the
  never-clearable surfaces are enforced through one union-judged walk over a
  class's whole allowlist. This doctrine requires that (a) any provenance-eligible
  class route through that SAME union-judged definition-time walk, never a
  structurally separate check that could bypass it; (b) the doctrine state
  explicitly which enforcement is PRIMARY for the provenance axis — if the class
  allowlist is broad, the per-PR provenance-tie verifier becomes primary and the
  definition-time floor is a MANDATORY backstop, and this is stated, not implied;
  and (c) each enrolling repo publish its OWN tree-validated floor covering that
  repo's decision core, gate, workflow, credential, governance, and
  council-record surfaces BEFORE any non-docs class is enabled for it — because
  the floor's meaning is tree-specific (`scripts/**` = "the decision core" holds
  in codexFactory, not necessarily in the openxFactory pilot). A class whose
  allowlist intersects any of those surfaces MUST be refused at definition time.

- **The scope check needs a machine-readable substrate that does not exist
  yet.** The ratified `code_surface:` field is repository-granularity prose
  (`release-realization` "Proposal declarations", `:7-8`), so it cannot bound a
  changed-path set. This doctrine names, as an explicit PRECONDITION of the
  realization, a structured path-scope declaration ratified changes must carry —
  a glob allowlist, added either as a schema amendment to `code_surface` or a new
  sibling field (itself an `openspec/`-touching, human-gated change). Until that
  substrate lands, no provenance-eligible code class can be published; the
  verifier is not buildable-as-described against prose `code_surface`.

- **A provenance-tie VERIFIER is named as the buildable core.** The one new
  mechanism this doctrine requires — and it does not exist yet — is a
  mechanical check, run at clearance time from the BASE branch, that: (i)
  resolves the tie from an EXPLICIT anchor (not a fuzzy title match), and
  CORROBORATES it against a source the PR head cannot author — a base-branch
  record naming the effort/branch — so an author-controlled string alone (the
  `change/<slug>` head branch or a PR-body change reference) NEVER establishes
  the tie; (ii) follows PR head → its OpenSpec change → currently-`ratified`
  status (re-resolved at evaluation time, never cached) + a SIGNED,
  identity-bound council ratification record (the record is trusted only if it
  transports as a signed artifact, mirroring the verdict check-run, never as a
  plain committed file any tree-writer could fabricate); (iii) confirms the PR's
  changed paths fall WITHIN the ratified change's MACHINE-READABLE path scope —
  a glob allowlist, NOT prose `code_surface` — so the tie proves the diff was
  authorized, not merely that a same-named ratified change exists; a change whose
  scope is prose or repository-level is INELIGIBLE, never "all paths in scope";
  and (iv) FAILS CLOSED (parks for human review) on any broken, ambiguous,
  out-of-scope, stale-status, unsigned-record, or non-enumerable-scope link,
  RECORDING which criterion/sub-check failed. This change specifies the
  verifier's contract as doctrine; codexFactory realizes it. (Resolving a change
  chain that spans multiple ordered deltas is a realization detail left to the
  follow-on, not fixed by this doctrine.)

- **FULL-PIPELINE-GREEN is named as the successor that retires the interim
  gate, with a testable retirement trigger.** The end state — the whole build
  governed and watched from the proposal down, the whole pipeline green — is the
  documented successor that SUPERSEDES the interim provenance criterion. The
  interim gate is explicitly time-boxed doctrine, not a permanent second regime:
  the doctrine carries a SUNSET clause requiring that the interim criterion be
  retired by a NAMED successor change raised on pilot evidence (mirroring how
  `add-substantive-review-lane` defers its tier vocabulary to "a named follow-up
  change raised on pilot evidence"). Until that successor lands, the interim
  criterion (1)–(4) governs; the exact evidence bar for supersession is an open
  question deferred to that successor rather than fixed here.

- **Safety basis is stated to rest on provenance-completeness, NOT review
  quality.** The doctrine records that the safety basis is the complete,
  mechanically verified governed traceability chain — not review-quality or seat
  composition — and takes no position on the still-open seat-diversity question
  (`seat_diversity_disposed_on_soak_evidence`, parked), citing no "nil-benefit"
  finding (see the "Why" section for the record and its own anti-misreading
  warning).

## Capabilities

### New Capabilities
<!-- none — the eligibility doctrine belongs in the existing neutral roles/authority model. -->

### Modified Capabilities

- `roles-authority-model`: the "Constitutional floor for autonomous clearance"
  requirement is MODIFIED so autonomous eligibility is **blast-radius-shaped OR
  fully-governed-provenance-shaped** (orthogonal axes), with the never-clearable
  floor unchanged and still binding on both axes. FOUR requirements are ADDED:
  (a) the interim provenance-completeness eligibility criterion (1)–(4);
  (b) the provenance-tie verifier contract (base-read corroboration, signed
  ratification record, machine-readable path-scope containment, currency
  re-resolution, park legibility, fail-closed);
  (c) floor-primacy and per-repo floor instantiation for the provenance axis; and
  (d) the full-pipeline-green successor with the interim sunset clause.
  Because `add-substantive-review-lane` is ratified-but-active and already
  modifies that requirement, this change's deltas are declared RELATIVE TO that
  change's outcome per `release-realization` "Ordered deltas" — an ordered-delta
  relationship, not a base-spec edit.

## Impact

- **openxFactory (this change's ONLY diff):** the `roles-authority-model` spec
  delta. No code. The human-readable projection into `docs/roles-and-authority.md`
  is NOT edited by this change; it lands when this ordered delta and its base
  `add-substantive-review-lane` are promoted/archived (matching the
  `add-wallet-carried-review-authority` precedent).
- **codexFactory (downstream follow-on, NOT built here):** (a) the provenance-tie
  verifier; (b) a class-floor guard in `scripts/merge_master/council_clearance.py`
  that keeps the never-clearable floor binding on provenance-eligible candidates;
  (c) an ORDERED-DELTA MODIFIED on the `merge-master-approval` definition-time
  `clearable`-eligibility predicate to admit a provenance-eligible, non-docs-shaped
  `clearable` class WITHOUT weakening the floor (required — today that predicate
  admits `clearable` only for docs-/derived-shaped classes and forecloses code,
  so without this widening (1)–(4) can never produce a real autonomous merge);
  and (d) a `gate_rules_council` record declaring at least one provenance-eligible
  candidate class with its rationale. Tracked as a dependent second change,
  archived only on merged + green realization evidence per `release-realization`.
- **Sequencing precondition (criterion 1):** the reviewed enrollment front door
  from `add-repo-enrollment` is contract-ratified but its dashboard/intake
  deployment and first live enrollment canary are not yet complete, and
  enrollment coverage is per-effort/per-class, not merely repo-level (Speckit
  feature `011-council-feature-clearance`, FR-006). Criterion (1) therefore has
  no satisfying live instance until an enrolled repo exists; the interim path
  activates per enrolled effort, not the moment this doctrine ratifies.
- **Structured-path-scope precondition (criterion 2, verifier step iii):** the
  ratified `code_surface:` field is repository-granularity prose
  (`release-realization`, `:7-8`). A machine-readable path-scope substrate — a
  glob allowlist on ratified changes, as a `code_surface` schema amendment or a
  new sibling field — is an explicit, human-gated PRECONDITION the realization
  depends on; it must land before any provenance-eligible code class is
  published. Named as its own dependency, not folded silently into the verifier.
- **Per-repo floor precondition (criterion 4):** each enrolling repo must publish
  its OWN tree-validated never-clearable floor covering that repo's decision core,
  gate, workflow, credential, governance, and council-record surfaces before any
  non-docs class is enabled for it; the floor's semantics are tree-specific and
  do not transfer between repositories.
- **Checkout caveat (not a proposal defect):** the aggregation repo's pinned
  `xFactories/codexFactory` submodule was observed stale relative to the
  classification-intent/enrollment realization (which lives on codexFactory
  `origin/main`); the current floor there (`PROTECTED_CLASS_SURFACES`) is
  stronger than a stale checkout shows. The realization change must be scoped
  against codexFactory `origin/main`, and the aggregation's next pin-sync should
  pick this up per the three-file pin-sync invariant in `xFactory/CLAUDE.md`.
- **Ordered-delta / co-modifier relationships:**
  - `add-substantive-review-lane` (openxFactory, ratified-but-active) — this
    change modifies its "Constitutional floor for autonomous clearance"
    requirement; deltas declared relative to its outcome. Archive ordering is a
    consequence of that mechanism, not a substitute for it.
  - `add-repo-enrollment` (codexFactory, ratified 2026-08-26) — criterion (1)
    consumes its front door: enrollment is a machine-prepared, owner-verified PR
    against the target repo's protected `.github/merge-approval-envelope.yml`
    base-branch path. The verifier reads enrollment from that base-branch record
    and MUST NOT provide any bypass of the enrollment route.
  - `add-classification-intent-and-substantive-classes` (codexFactory, ratified
    2026-08-25) — the class floor and definition-time class-floor predicate this
    doctrine's criterion (4) binds through; a provenance-eligible class is
    declared under that machinery, and the definition-time floor derivation stays
    structurally unreachable for floor-touching surfaces.
  - `add-wallet-carried-review-authority` (openxFactory, ratified-but-active) —
    authority-as-grant; the provenance path grants eligibility, never authority,
    and never originates a verdict. No competing authority is introduced.
- **Explicitly NOT in scope:** implementing the verifier, editing
  `council_clearance.py`, any push or merge, and any change to the tier
  vocabulary or per-tier clearance eligibility (those remain deferred exactly as
  `add-substantive-review-lane` leaves them).

## Ratification record

Ratified: 2026-08-28 by the gate_rules_council (agent-seat mode; full declared
membership — lead-architect, lead-security, lead-quality, company-policy-lead,
the vacant symbolic intent-owner slot — plus the client-security-compliance-officer
conjunction pull-in, which FIRED and was seated by convener act) — RATIFIED AS
AMENDED (5/5). Convener disposition ACCEPT-AS-AMENDED accepted 2026-08-28 by
Brett Heap. Record:
hermes/domain/review-councils/records/2026-08-28-gate-rules-provenance-gated-autonomous-merge.md
(codexFactory). CRITICAL #1 (global-floor parameterization + mandatory-minimum
trust-root floor) folded into this spec delta; the remaining CRITICAL (#2 interim
narrow+floor-disjoint / static primary; #3 positive pilot mandatory and never on
authority code) and all HIGH + deferred amendments are carried as BINDING
PRECONDITIONS on the realization change `realize-provenance-gated-autonomous-merge`
and its first pilot — the provenance axis is ESTABLISHED by this ratification but
SHALL NOT be EXERCISED (realization shipped / any pilot run) until those
preconditions hold.
