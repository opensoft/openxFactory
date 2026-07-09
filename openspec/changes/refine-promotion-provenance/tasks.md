# Tasks: Refine Promotion Provenance

## 1. Process Doc

- [ ] 1.1 Add the three rules (drafting ownership, provenance fields,
      mid-promotion authority) to
      `docs/domain-to-neutral-promotion-process.md` — a Domain Adoption
      subsection edit citing this change.

## 2. Contract Schema

- [ ] 2.1 Add optional `promoted_from` and `specializes` fields to
      `contracts/schemas/xfactory-domain-stack.schema.yaml`.
- [ ] 2.2 Record the addition in `contracts/CHANGELOG.md` per the contract
      versioning policy (backward-compatible optional fields).

## 3. Staged Topic Closure

- [ ] 3.1 Update `ideation/staging/promotion-refinements/open-questions.md`:
      reference this change, note the standalone-vs-fold reversal, mark the
      topic's exit satisfied.

## 4. Validation

- [ ] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate refine-promotion-provenance --strict`
      and `--all --strict` pass.
- [ ] 4.2 `scripts/validate-domain-factory.py` still passes against a domain
      repo (schema fields optional, no breakage).
