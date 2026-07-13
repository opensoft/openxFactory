# Tasks: Proposal Origin Contract

## 1. Sequencing And Contract Baseline

- [ ] 1.1 Realize `add-cross-factory-ideation-routing` (fourteenth family) first; then verify the promoted doc-health spec matches the wording this change's enumeration delta was declared against, rebasing the delta if intervening changes altered it, and re-run strict OpenSpec validation.
- [ ] 1.2 Verify this change's own `.openspec.yaml` staged origin, support manifest origin repetition, and staging-header linkage as the self-application acceptance proof.

## 2. Origin Contract And Gates (openxFactory)

- [ ] 2.1 Document the origin block (staged and ad-hoc field sets, durable-id grammar, immutability after ratification) in the lifecycle guidance that transition operators follow, referencing the promoted requirements without duplicating them.
- [ ] 2.2 Wire strict proposal validation to reject: missing origin, unknown or malformed kind or id, unresolvable staged id/path at transition, staging-header/packet/manifest disagreement, incomplete ad-hoc approval provenance, and dual origin declarations.
- [ ] 2.3 Wire the archive gate to verify the origin declaration is unchanged, staged origins are retained in the compressed support manifest, and ad-hoc reason/approval provenance survives archive with or without a bundle.

## 3. Migration (openxFactory)

- [x] 3.1 Amend the archived `add-proposal-supporting-doc-lifecycle` packet with its explicit ad-hoc origin (`openxFactory:adhoc:2026-07-09-proposal-support-lifecycle-bootstrap`, recorded reason and approval). Evidence: applied verbatim from `supporting-docs/origin-contract.md` Migration item 1; see `migration-evidence.md`.
- [x] 3.2 Backfill changes carrying staged support manifests as `staged`, deriving durable ids from the recorded repository and staging topic; classify changes with no historical staging source as `ad_hoc` without fabricating folders or history. Evidence: 22 archived changes backfilled (12 `staged` from `supporting-docs.manifest.yaml` `origin_path`, 10 `ad_hoc` from packet/README/git-history evidence); 4 already-compliant changes left untouched; see `migration-evidence.md`.
- [x] 3.3 Record migration provenance in a reviewable evidence file so every backfilled origin cites the record it was derived from. Evidence: `openspec/changes/add-proposal-origin-contract/migration-evidence.md` (Status: record, Kind: report) cites, per change, the quoted manifest field or git commit each origin derives from.

## 4. Fifteenth Deterministic Family (codexFactory)

- [ ] 4.1 Add `scripts/doc_health/proposal_origin.py` and register it as the fifteenth deterministic family in the registry, runner, configuration, and report output, after the routing family lands.
- [ ] 4.2 Implement the checks by reference: missing origin on active or archived proposals, malformed kind/id, staged origin resolution against recorded provenance, header/packet/manifest mismatch, incomplete ad-hoc provenance, and post-ratification mutation (contested class).
- [ ] 4.3 Extend transition tooling to write the staged origin block automatically at the proposal gate and to require explicit reason/approval arguments for ad-hoc creation rather than silently defaulting.
- [ ] 4.4 Add deterministic fixtures and tests: staged origin accepted and copied into the manifest; ad-hoc accepted with complete provenance; missing origin rejected; both kinds rejected; staged id/path/header mismatch rejected; active-to-archive identity preserved; archived bootstrap exception resolvable; backfilled origins validated against migration evidence without fabricated history.

## 5. Records And Guidance

- [ ] 5.1 Keep the openxFactory README "OpenSpec Records" entry current through ratification, realization, and archive.
- [ ] 5.2 On archive, confirm the staged `proposal-origin-contract` INDEX entry still correctly describes the remaining regulated-traceability rationale as future work.
