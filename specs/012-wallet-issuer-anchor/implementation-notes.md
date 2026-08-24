# Implementation Notes — 012-wallet-issuer-anchor

## Round 1 — Implementation landed (2026-08-24)

Validator widened per data-model.md; three specimens joined
`contracts/openxwallet/examples/negative/`; boundary guard added to self-test.

Gate evidence (all run on this branch):

- Baseline (pre-S2 tree, stashed): exit 0 — `17 positives / 33 negatives across
  11/11 requirements`.
- Post-S2 sweep: exit 0 — `17 positives / 36 negatives across 13/13 requirements`.
  The five packaged grant positives pass unchanged (FR-007); all three new
  negatives fail for exactly their declared reasons, machine specimen pinned on
  its subject token, legacy specimen pinned on the branch wording.
- Boundary guard (US3): synthesized non-review root grant without `issued_by`
  validates clean inside the self-test.
- `pytest tests/wallet_yaml_syntax_gate/ -q`: 4 passed (S1's gate untouched).
- `openspec validate --all --strict`: 73 passed, 0 failed.

**SC-002 count disclosure**: the spec phrased coverage as "17→20
positives-equivalent"; actual positive FILE count stays 17 — S2 adds only the
three negatives FR-005 names, and no requirement of S2 adds a positive fixture.
The negative and requirement counts match the spec exactly (33→36, 11→13).
Flagged at PR review as an arithmetic slip in SC-002's first clause, to be
corrected in that review rather than silently reinterpreted here.

## Round 2 — verdicts, blocker fix, hardening, authorized schema widening (2026-08-24)

Independent verdicts on commit 9e85277b:

- **Code-reviewer (gpt-5.6-terra route): REVISE** — one MAJOR: SC-002's
  "17→20 positives-equivalent" arithmetic slip. ADDRESSED: SC-002 corrected to
  actual counts (positives 17 unchanged; negatives 33→36; coverage 11→13).
- **QA (adversarial): FAIL** — one BLOCKER + six surviving mutants.
  - BLOCKER (schema-invalid non-string `issued_by` reached `in ctx.wallets`,
    unhashable → exit-2 harness crash): FIXED with a type guard; regression
    probe now exits 1 with named findings instead of crashing.
  - Mutant survivors exposed self-test blind spots: no anchored-root positive,
    no drift-negative, no child/root separation probe, unnamed fixture
    reliance, strippable detail pins. FIXED: S2 anchor-assertion block in
    self_test (anchored root clean; ` brett heap` refused without
    normalization; machine and legacy wordings pinned; synthetic parent+child
    pair proving child exemption; named-probe presence + mandatory detail pins
    for the three S2 fixtures).
- **MINOR (spec conflict)**: §3.1 "no contracts/ edit" vs FR-005 fixtures —
  resolved by precision edit (fixtures are corpus content) … then superseded by
  the discovery below.

**Material discovery at the hardening step**: the new anchored-root assertion
failed — the grant schema's identifier grammar (`^[A-Za-z0-9][A-Za-z0-9._:/-]*$`)
cannot carry ANY operator identity: no spaces (killing `Brett Heap`) AND no `@`
(killing even an email form). No packaged anchored positive had ever existed to
expose this. Escalated twice; convener re-ruled: anchor token =
`Brett.Heap@opensoft.one`, with explicit authorization for a SURGICAL schema
widening — `$defs/issuer_identifier` used by `issued_by` alone; every other
identifier field keeps the strict grammar. Landed per Contract Versioning
Policy: manifest sha256 refreshed, CHANGELOG Unreleased additive bullet, bundle
cut still deferred. The initial display-name ruling is recorded as superseded in
clarify Q3/Q4.

Gate evidence after Round 2: sweep exit 0 (`17 positives / 36 negatives across
13/13 requirements`, anchored-root assertion green); unhashable-issued_by
regression probe exits 1 with named findings; pytest wallet_yaml_syntax_gate 4
passed; openspec validate --all --strict rerun at commit.

## Phase status

Clarify CLOSED; Rounds 1–2 LANDED with gate evidence above. Pending before
merge: nothing outstanding from reviewer or QA; PR next.

## Grounding facts (researcher, 2026-08-23)

Spec authored and clarified (see [clarify-questions.md](clarify-questions.md));
checklist all-pass. Plan, tasks, and code realization follow in later phases.
Counts asserted in SC-002 are recorded as evidence at implementation time.

## Grounding facts (researcher, 2026-08-23)

- Validator currently reads `issued_by` through zero rules — S2 is the field's
  first real enforcement.
- Packaged corpus exposure: five grant positives, all transaction-act class,
  none carrying `issued_by`; the widening must cost them nothing (US3 boundary
  guard, FR-008).
- Root-vs-child shape follows existing attenuation logic; S2 adds no
  child-specific rule unless a ratified gap surfaces.

## Rulings encoded

- Class marker: scope `acts` vocabulary; canonical token `review` as named
  validator constant beside the custody-registry path reference (architect;
  confirmed against ratified vocabulary).
- Anchor: validator constant citing the Human Escalation Contract at
  `docs/roles-and-authority.md:103-140`; machine tokens and legacy `opensoft`
  refused at roots; exact-match `Brett Heap` accepted (convener).
- Specimens: three negatives under `contracts/openxwallet/examples/negative/`
  (`grant-review-authority-omits-issued-by.yaml`,
  `grant-review-root-issuer-is-a-machine.yaml`,
  `grant-review-root-issuer-says-opensoft.yaml`).

## Durable relay obligation — wallet-substrate linkage (convener-accepted, 2026-08-24)

From the R4 × `add-regular-pr-council-clearance` reconciliation: the clearance
draft amends the two authorship requirements so human-authored PRs become
tier-2-clearable **after soak — with zero reference to the wallet substrate**
(trust anchor = verdict quality + soak evidence), while the wallet arc premises
autonomy over authored logic on authority *provenance*: grants binding the three
deliberation seats, arriving at S3+. Both postures are internally coherent; they
differ on whether provenance is a precondition or a parallel track.

Convener accepted the recommended minimum: **enrollment activation carries a
recorded accepted-risk note referencing the wallet arc**. That note is now
recorded on the codexFactory side
(`openspec/changes/add-regular-pr-council-clearance/clarifications.md`, entry
*"Wallet substrate provenance vs soak-evidence-only activation"*) and MUST be
surfaced at that change's Gate-Rules convening before any enrolled surface
activates. If S3's exercise-record substrate lands first, activation must be
re-examined against grant-carried seats rather than soak evidence alone.

This section is the durable openxFactory-side copy: S2's artifact set travels to
PR with the obligation restated here regardless of where the codexFactory change
stands at merge time.

## Related withdrawal (recorded for the archive)

The interim R4-B sketch (schema-level `classification_intent` field,
codexFactory side) is withdrawn permanently — superseded by absorption into the
clearance draft's third rule state `advisory`. Recorded so no successor effort
resurrects it.
