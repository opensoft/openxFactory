## 1. Evidence and source verification

- [x] 1.1 **DONE 2026-09-01 —** captured in `evidence/current-publications-2026-09-01.md` with primary URLs, publication/version, steward, term kind, verification date, and confidence.
- [x] 1.2 **DONE 2026-09-01 —** captured the SFIA licensing conflict and Brett's explicit operator override as separate facts; the official source finding remains unchanged in the evidence record.
- [x] 1.3 **DONE 2026-09-01 —** captured APQC PCF 8.0's attribution condition and separated PCF hierarchy reuse from process-definition reuse.

## 2. Registry implementation

- [x] 2.1 **DONE 2026-09-01 —** added distinct `itil5` while preserving the existing `itil4` record.
- [x] 2.2 **DONE 2026-09-01 —** updated SFIA to current SFIA 9 and added the explicit unverified operator override selected by Brett.
- [x] 2.3 **DONE 2026-09-01 —** reconciled APQC PCF 8.0 metadata and added the IT-process crosswalk scope plus attribution requirement.
- [x] 2.4 **DONE 2026-09-01 —** retained descriptive-only semantics; no framework hierarchy, practice text, skill definitions, or process definitions were copied.

## 3. Validation and regression coverage

- [x] 3.1 **DONE 2026-09-01, SCOPE CORRECTED 2026-09-03 —** `scripts/standards_body_registry.py` checks current-publication metadata completeness for **every body that claims primary-source verification**, plus the three amended entries as a floor. The correction is D5, forced by Copilot review round 2: the requirement said "every body marked current" while the checker used a three-id allowlist, and MEASURED against the registry — 45 bodies, **32 `status: current`, 3 carrying a verification date** — the requirement was false of 29 records. Backfilling 29 dates nobody performed is the fabrication the registry's own header forbids; demoting 29 records would misstate their currency. The obligation is now keyed to `verified_on`, which IS the claim.
- [x] 3.2 **DONE 2026-09-01 —** validator checks override completeness and requires the explicit unverified status.
- [x] 3.3 **DONE 2026-09-01 —** registry regression tests and the existing unknown-body negative fixture cover the selected positive and negative paths.
- [x] 3.4 **DONE 2026-09-01, RE-RUN 2026-09-03 —** registry tests (5 passed at
      authoring, **9 passed** after the review round below) and
      `scripts/validate-omnigent-contracts.py` both pass with zero findings.
- [x] 3.5 **DONE 2026-09-03 — THE DUPLICATE-KEY DEFECT, FOUND BY REVIEW AND
      CLOSED AS A CLASS.** The `sfia` entry carried `source_url` TWICE — the
      licensing page written 2026-08-09 and the SFIA-9 publication page added by
      this change — and `yaml.safe_load` takes the last silently, so every
      reader saw the publication URL and **the licensing evidence D2 exists to
      preserve was gone from the parsed document while both lines sat visibly in
      the file**. `registry_errors` could not have caught it and no post-parse
      check can: by then there is one key. The licensing URL moved to
      `licence_page` (the field APQC and IAB Tech Lab already use for exactly
      this), and `scripts/standards_body_registry.py` gained `load_registry()`,
      a `SafeLoader` subclass that **refuses a repeated key at any mapping
      level** — the rule `scripts/frontmatter_strict.py` applies to proposal
      front matter, applied here, though not that module reused (its
      65,536-byte ceiling sits below this registry's ~77,000). The validator and
      the tests both read through it; `yaml.safe_load` on the registry is now a
      defect in the caller. Four new tests, one asserting that the permissive
      loader is GREEN on the same bytes, which is the whole point.

## 4. Consumer handoff

- [x] 4.1 **DONE 2026-09-01 —** published `handoff/opsx-overlay-current-standards.md` naming `itil5`, SFIA 9's
      unverified status, and APQC PCF 8.0 as the only current-body inputs.
- [x] 4.2 **DONE 2026-09-01 —** authorized the separate OpsxFactory change to evaluate all nine worker
      classes against APQC IT-process terms without forcing a match.
- [x] 4.3 **DONE 2026-09-01 —** recorded the missing SFIA written permission as an explicit follow-up
      owned by the operator/legal-review seat.

## 5. Release and archive

- [x] 5.1 **DONE 2026-09-01, RE-MEASURED 2026-09-03 —** no contract release
      bundle is owed. The re-measurement is the part that was previously
      asserted rather than checked, and it is the release-inventory question in
      its own terms: `contracts/policies/standards-bodies.yaml` is a member of
      NEITHER `contracts/manifest.yaml` (which lists three policies —
      `hermes-governance-agents.yaml`, `merge-risk-policy.yaml`,
      `layer-vocabulary.yaml` — and not this one) NOR
      `contracts/releases/contract-v3.0.digests.yaml` (283 entries, zero under
      `contracts/policies/`). `scripts/doc_health/release_inventory.py` compares
      only the DECLARED bundle's members, so a non-member edit raises no
      `release-inventory-drift` finding at any severity and needs no editorial
      allowance. **THE POLICY EDIT THEREFORE RIDES THIS PR AND DOES NOT WAIT FOR
      THE NEXT CUT**, and no follow-up commit is split out for it.
- [x] 5.2 **DONE LOCALLY 2026-09-01 —** the registry amendment is integrated in
      the working tree and the required registry and Omnigent validations pass.
      Publication as a Git commit/merge remains an operator action; no commit or
      push was performed by the authoring session.
- [x] 5.3 **SUPERSEDED 2026-09-03 — THE PACKET WAS NOT READY TO ARCHIVE AND WAS
      NOT ARCHIVABLE.** The authoring session wrote the packet directly into
      `openspec/changes/archive/2026-09-01-.../` and promoted its delta into
      `openspec/specs/standards-body-registry/spec.md`, both of which are the
      ARCHIVE STEP's acts and neither of which this packet had earned: it had
      never landed on `main`, was never ratified, and carries a code surface,
      which under `docs/release-realization-flow.md` § The Archive Gate cannot
      archive until its code is merged on the implemented target with a green
      run. Archiving an unrealized code-surface change is a contested-class act
      there. The adopting lane moved the directory to
      `openspec/changes/update-standards-body-current-publications/` (ACTIVE)
      and REMOVED the pre-promoted copy, which duplicated the change's own
      delta verbatim under a `TBD - created by archiving` purpose line.
- [ ] 5.4 **OWED — RATIFICATION.** `Status: draft`. Brett Heap ratifies, or
      vetoes, D1 … D4 — D2 (the SFIA unverified operator override) and D3 (the
      scope of the later APQC crosswalk authorization) in particular, both
      being the authoring session's decisions and neither covered by the
      commissioning citation in `.openspec.yaml`.
- [ ] 5.5 **OWED — REALIZATION EVIDENCE ON `main`.** The code surface lands in
      the same PR as the packet, so the archive gate's merged-plus-green
      condition is discharged by this PR's own merge plus a green
      `pytest-suite` on `main`, recorded on the archive PR rather than claimed
      here.
- [ ] 5.6 **OWED — THE ARCHIVE ACT, SEPARATELY AND THROUGH `proposal-support`.**
      Only then does `specs/standards-body-registry/spec.md` promote into
      `openspec/specs/standards-body-registry/spec.md`, with a real `## Purpose`
      replacing the archiver's `TBD` line.
