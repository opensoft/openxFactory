# Pre-Realization Review — add-ideation-cross-reference-readiness

Status: record
Kind: report
Repository context: openxFactory
Captured: 2026-07-14
Reviewer: Opus review agent (Fable-orchestrated), pre-dispatch.

Verdict: **READY WITH CONDITIONS** — dispatch realization; all conditions
are realization-gate work. The change was proposed and ratified 2026-07-12
and left untouched while two sibling changes landed; its deltas are stale,
not wrong, except where noted.

## Conditions

- **C1** — Task 1.1 must rebase the doc-health MODIFIED delta onto the
  wording promoted AT REALIZATION TIME. As proposed it hardcodes "fifteen"
  deterministic families and copies routing/proposal-origin family names,
  scenario bullets, and the ideation-organizer lane mention — none of which
  this change owns and only thirteen of which are promoted today. Rebase
  down to the promoted count/list; keep only the two edits this change
  owns (readiness scoring in the agentic clause; `ideation-readiness` in
  the lane list). Strict-validation passes silently on the stale text, so
  the rebase is a human obligation, not a validator catch.
- **C2** — Task 2.1's index must be a STRUCTURED schema (not markdown-
  only): `ideation/cross-reference.yaml` as source of truth with
  `ideation/cross-reference.md` as a generated human projection (the
  notebook-projection / doc-health-report precedent; the change's own spec
  calls the index a generated projection). It must fix the register
  kernel's provisional embedding field (`possibles_register`, $ref to
  `contracts/schemas/ideation-possibles-register.schema.yaml`) and carry
  the envelope (`kind` + `schema_version`), open/additive posture.
- **C3** — Task 2.3's validator must co-load the register kernel + the
  dashboard snapshot schema in one registry (the cross-file `evidence_pin`
  $ref) and must NOT duplicate register-entry/transition validation owned
  by `validate-ideation-dashboard-contracts.py` — ownership line:
  index envelope/embedding/scores/fit-citations here; register-entry shape
  and transitions delegated.
- **C4** — Task 2.1 must model the human-seen-cluster recommendation entry
  (the dashboard's "Human-seen cluster intake" requirement lands on this
  change's cluster entry; dashboard task 3.5 is blocked on it).
- **C5** — The codexFactory scorer module must not be named `readiness.py`
  (collides with `scripts/doc_health/readiness.py`, the fail-closed infra
  evaluator); use `ideation_readiness.py`.

## Precision notes

- The evidence contract to reuse is the ORGANIZER recommendation schema
  (`xfactory-ideation-organizer-recommendations.schema.yaml`: source_ref
  with revision/section/passage_sha256, rationale, confidence,
  alternatives, `disposition: pending_review`) — not the cataloger facet
  schema. The organizer schema is committed but owned by the still-active
  routing change; pin/track that source at 3.2.
- The readiness lane degrades fail-closed to "skipped" exactly like the
  analysis and cataloger lanes; realization evidence must NOT require live
  host dispatch (a skipped lane report is a valid landed state). The
  readiness-scorer omnigent profile is a mechanical third clone of the
  doc-analysis/cataloger profiles.
- Bootstrap scale is tens of entries (~23 header-bearing ideation docs,
  ~10–15 multi-doc clusters). Two soft risks: the clustering rule (3.3)
  is the fuzziest surface — write the design note before implementing;
  the domain tier will often be unscoreable at launch (Hermes layer
  migration), so the min>=8 gate rarely fires initially — expected
  soft-launch behavior, not a defect.

## Cross-change effects

Wave 1 (2.1) closes the register kernel's dangling $ref and unblocks the
dashboard's tasks 1.1 and 3.5 — prerequisite to the dashboard's archive.
Discharge the dashboard's 1.1 verification in the same wave.
