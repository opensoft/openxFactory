## 1. Contracts

- [x] 1.1 Add the five record schemas under `contracts/schemas/`
      (`pattern-ledger-episode`, `-outcome-label`, `-recurrence-family`,
      `-recurrence-forecast`, `-crystallization-candidate`), each with
      `schema_version` + `kind`, default-deny consent, and the controlled
      vocabularies (label sources, replayability, family states, rungs for
      `suggested_rung`).
- [x] 1.2 Add positive and negative examples per kind — negatives MUST
      include: praise-only candidate rationale, mixed-tenant family, mutable
      outcome verdict, candidate without idempotency key, forecast below
      minimum evidence.
- [x] 1.3 Seed the MVP fixture corpus: hand-derive 2–3 `episode` examples
      for the packet-capture family (topic decision D8) from real audit
      history, with their `outcome_label` streams.
- [x] 1.4 Register schemas and examples in `contracts/manifest.yaml`,
      reconcile `contracts/CHANGELOG.md`, and update `contracts/README.md`.
      — contracts/README "Contracts Pending Realization" rows added
      2026-07-29; manifest + CHANGELOG registration correctly waits for the
      archive bundle cut per that section's policy (avatar-client
      precedent). Remaining at archive: manifest entries + CHANGELOG entry
      + version allocation. Discharged at the contract-v1.19 cut
      (2026-07-29): manifest entries with per-file sha256 — including the
      xfactory-derived-model-conformance catch-up the CHANGELOG Unreleased
      note assigned to this cut — plus the CHANGELOG section.

## 2. Validator

- [x] 2.1 Implement `scripts/validate-pattern-ledger.py`: schema
      conformance, vocabulary enforcement, default-deny consent, family
      transition legality (recorded merges/splits only), candidate
      idempotency/suppression, evidence-citation rule (episodes + forecast
      required; praise-only rejected), forecast maturity/score pairing.
- [x] 2.2 Add validator fixtures and tests wired into the repo's validate
      path so `scripts/validate-*.py` discipline covers the new family.

## 3. Documentation

- [x] 3.1 Link the capability into the openxFactory README doc index and,
      at raise, the "OpenSpec Records" block. — OpenSpec Records entry
      landed at raise 2026-07-29; the doc-index link lands with the
      promoted capability spec at archive — added at the 2026-07-29
      archive.
- [x] 3.2 Add a pointer from `docs/knowledge-lifecycle-model.md`'s
      experiential path to the procedural promotion target (pointer only —
      no normative duplication; that doc is `Status: draft`).
- [x] 3.3 Update the staging INDEX row/detail on partial promotion (the
      `pattern-ledger-contracts.md` fragment moves to `supporting-docs/`).

## 4. Validation and realization evidence

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate add-pattern-ledger
      --strict` and `--all --strict` green — verified at raise, ratify, and
      realization (2026-07-29).
- [x] 4.2 Declare staged origin (`openxFactory:staging:recurrence-crystallization`)
      in `.openspec.yaml`; verify the supporting-docs manifest and hashes.
- [x] 4.3 Realization evidence per `release-realization`: the declared
      code surface (schemas + validator) merged and green; contract version
      allocated per `docs/contract-versioning-policy.md`; archive follows
      evidence, never precedes it. — Evidence: realization commit 78403e0
      merged and green (validator self-test 7/7 both directions; openspec
      --all --strict 50/50); contract-v1.19 allocated at the 2026-07-29
      archive cut with its annotated tag.
- [x] 4.4 Obtain ratification approval and stamp the proposal front matter
      (`Status: ratified`, `Ratified by:`) — ratified by Brett 2026-07-29.
