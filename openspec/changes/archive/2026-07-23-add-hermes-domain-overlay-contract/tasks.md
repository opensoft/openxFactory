# Tasks — add-hermes-domain-overlay-contract

## 1. Schemas

- [x] 1.1 Author `contracts/hermes-domain-overlay/hermes-domain-overlay.schema.yaml`
      (identity, approval scopes, required fields, authority boundaries,
      no-overlap rule).
- [x] 1.2 Author `contracts/hermes-domain-overlay/overlay-descriptor.schema.yaml`
      (per-role path declaration; documented convention fallback).
- [x] 1.3 Contract README documenting shape, fallback rule, and consumers.

## 2. Validator + fixtures

- [x] 2.1 Implement `scripts/validate-hermes-domain-overlay.py` (schema check,
      no-overlap, descriptor path existence; repo-path argument like the
      other canonical validators).
- [x] 2.2 Fixtures: one positive (modeled on codexFactory's live overlay),
      negatives for missing block, empty list, overlapping boundaries,
      dangling descriptor path.
- [x] 2.3 Prove against the real consumer: validator passes on
      `xFactories/codexFactory` unmodified.

## 3. Publication + close out

- [x] 3.1 Register in `contracts/manifest.yaml`; version per
      `docs/contract-versioning-policy.md` (additive bundle allocated at
      realization).
- [x] 3.2 `OPENSPEC_TELEMETRY=0 openspec validate
      add-hermes-domain-overlay-contract --strict` and the openxFactory
      validator suite green.
- [x] 3.3 README OpenSpec Records entry; staging INDEX
      (`layer-content-materialization`) updated; note the hermes-install
      adoption handoff (seeding increment 2 pins the released bundle).

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` real line 5 was respelled `Ratified by:` to `Ratified:` by slice
5B of `govern-openspec-corpus-membership` — the prefix only. Every byte after
the colon is carried verbatim, asserted identical at the edit, so the original
line is recovered exactly by reading `Ratified by:` back in its place and
nothing else on the page moved. The ruling is OQ-4's RULED extension of
2026-08-23 (Brett Heap, in-session), which widens the class to the sixteen
lines whose named change id is the DOCUMENT'S OWN. A change is not its own
approving change, and such a line passed `fam_ratified_provenance` only by
self-reference. This one emitted NO finding, so the respell is corrective
rather than a discharge and clears nothing from the census. The record that
justifies this line is the user approval of 2026-07-23 named on the line,
carried into the record by commit `5ad71a7` of the same day, "Archive
add-hermes-domain-overlay-contract (ratified 2026-07-23, released
contract-v1.15)". An append on a single-valued header is mechanically
impossible — `doc_health.corpus.STATUS_RE` swallows any trailing annotation —
so this is an in-place overwrite and an extension of Brett's 2026-08-10 append
ruling, named as one, and it is entered in
`docs/archive-record-discrepancies.md`.
