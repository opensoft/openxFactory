## 1. Contracts

- [ ] 1.1 Add the five record schemas under `contracts/schemas/`
      (`pattern-ledger-episode`, `-outcome-label`, `-recurrence-family`,
      `-recurrence-forecast`, `-crystallization-candidate`), each with
      `schema_version` + `kind`, default-deny consent, and the controlled
      vocabularies (label sources, replayability, family states, rungs for
      `suggested_rung`).
- [ ] 1.2 Add positive and negative examples per kind — negatives MUST
      include: praise-only candidate rationale, mixed-tenant family, mutable
      outcome verdict, candidate without idempotency key, forecast below
      minimum evidence.
- [ ] 1.3 Seed the MVP fixture corpus: hand-derive 2–3 `episode` examples
      for the packet-capture family (topic decision D8) from real audit
      history, with their `outcome_label` streams.
- [ ] 1.4 Register schemas and examples in `contracts/manifest.yaml`,
      reconcile `contracts/CHANGELOG.md`, and update `contracts/README.md`.

## 2. Validator

- [ ] 2.1 Implement `scripts/validate-pattern-ledger.py`: schema
      conformance, vocabulary enforcement, default-deny consent, family
      transition legality (recorded merges/splits only), candidate
      idempotency/suppression, evidence-citation rule (episodes + forecast
      required; praise-only rejected), forecast maturity/score pairing.
- [ ] 2.2 Add validator fixtures and tests wired into the repo's validate
      path so `scripts/validate-*.py` discipline covers the new family.

## 3. Documentation

- [ ] 3.1 Link the capability into the openxFactory README doc index and,
      at raise, the "OpenSpec Records" block.
- [ ] 3.2 Add a pointer from `docs/knowledge-lifecycle-model.md`'s
      experiential path to the procedural promotion target (pointer only —
      no normative duplication; that doc is `Status: draft`).
- [x] 3.3 Update the staging INDEX row/detail on partial promotion (the
      `pattern-ledger-contracts.md` fragment moves to `supporting-docs/`).

## 4. Validation and realization evidence

- [ ] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate add-pattern-ledger
      --strict` and `--all --strict` green.
- [x] 4.2 Declare staged origin (`openxFactory:staging:recurrence-crystallization`)
      in `.openspec.yaml`; verify the supporting-docs manifest and hashes.
- [ ] 4.3 Realization evidence per `release-realization`: the declared
      code surface (schemas + validator) merged and green; contract version
      allocated per `docs/contract-versioning-policy.md`; archive follows
      evidence, never precedes it.
