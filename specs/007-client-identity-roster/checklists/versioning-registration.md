# Versioning and Registration Mechanics Checklist: Client Identity Roster

Status: draft

**Purpose**: Release-gate validation of the requirements governing REGISTRATION —
the `contract-v1.32` bundle cut, manifest rows and digests, the CHANGELOG class,
the two version numbers that are easy to confuse, and the additivity claim the
bundle is held to.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)

## Bundle and rows

- [x] CHK501 Is the target bundle version stated, with the current version it is derived from and the date that was re-confirmed? [Clarity, Spec §FR-021, §Assumptions]
- [x] CHK502 Are the manifest row fields enumerated, so a row cannot be authored short? [Completeness, Spec §FR-021]
- [x] CHK503 Is the requirement stated that EVERY schema the feature edits gets its row refreshed in the same bundle, not only the new one? [Completeness, Spec §FR-021]
- [x] CHK504 Is the case of a schema with NO row to refresh dispositioned as a first registration, and recorded rather than performed silently? [Ambiguity, plan §decision 13, research §A registration gap]
- [x] CHK505 Is the trap between the row's `schema_version` (the record envelope const) and the file's `contract_schema_version` stated where a row is authored? [Clarity, tasks §9.1, research §A registration gap]
- [x] CHK506 Is the requirement that the record envelope's const must NOT change stated with its consequence (changing it invalidates every existing instrument)? [Clarity, plan §Cluster I, §Constitution VI]
- [x] CHK507 Is the single-row-for-two-kinds decision reconciled with FR-021's singular language, rather than read distributively? [Consistency, research §Decision 2]
- [x] CHK508 Is the consequence of one row for two kinds stated (both kinds share an envelope version)? [Consistency, ruling A-2, plan §Cluster A]
- [x] CHK509 Is the consumption rule's required content specified (declared placement AND the expected skip-with-notice), rather than left as prose? [Completeness, Spec §FR-020, tasks §9.1]
- [x] CHK510 Is the row shape anchored to a named precedent (the v1.31 rows), including its closing sentence? [Clarity, research §Registration mechanics]

## Digests and the release inventory

- [x] CHK511 Is digest verification named as a specific check that fails closed, rather than as "digests verify"? [Measurability, Spec §FR-021, tasks §9.6]
- [x] CHK512 Is the distinction between the manifest's per-file digests and the release digest INVENTORY stated, since they are different artifacts with different membership? [Clarity, research §Registration mechanics]
- [x] CHK513 Is the inventory's membership stated as closed over a named path set, with the explicit instruction that roster paths must not be hand-added? [Clarity, tasks §9.4]
- [x] CHK514 Is the reason the inventory regenerates at all (manifest and changelog digests change) stated, so an implementer does not conclude it should not change? [Clarity, tasks §9.4, research §Registration mechanics]
- [x] CHK515 Is the ORDER between the release-surface edits and the inventory generation specified? [Dependency, tasks §9.4] — FIXED: `contracts/CHANGELOG.md` and `contracts/README.md` are release-surface members, but Phase 9 marked 9.2/9.3 `[P]` and declared only `9.1 → 9.4 → 9.6` sequential, so the inventory could be built over files still being edited. tasks §9.4, the parallel-opportunities note, and plan §Cluster E now require 9.1–9.3 to land first.
- [x] CHK516 Is the atomicity requirement (one commit for the registration cluster) stated with its constitutional basis? [Clarity, plan §Cluster E, §Constitution VI]

## Change class and additivity

- [x] CHK517 Is the change class declared (additive/minor) and held to the tree's own definition of that class? [Measurability, plan §Cluster E, §Constitution VI]
- [x] CHK518 Is the additivity claim stated in terms a run can falsify (a conformant domain record on the same major version stays conformant)? [Measurability, research §Decision 3]
- [x] CHK519 Is the one measurement that would falsify the claim identified and scheduled? [Measurability, tasks §7.4]
- [x] CHK520 Is the additivity argument made for each modification independently rather than as a blanket claim? [Completeness, Spec §FR-030] — FIXED: the consent cascade gate's reach widening was outside the argument; FR-030 now names it and gives its narrow argument.
- [x] CHK521 Is the `Unreleased` CHANGELOG block's fate specified (folded, not left beside the new entry)? [Completeness, tasks §9.2, research §Registration mechanics]
- [x] CHK522 Is the CHANGELOG entry required to STATE the additivity argument rather than only to carry the class label? [Clarity, tasks §9.2]

## Consumability and documentation of the registration

- [x] CHK523 Is the consumer's path to the contract stated (pinned `xfactory.contract_ref` plus per-file digest), so "registered" means reachable? [Clarity, Spec §US2]
- [x] CHK524 Are the documentation surfaces that must list the new family enumerated (contracts README table, root README index)? [Completeness, tasks §9.3, §9.5]
- [x] CHK525 Is the root README's stale OpenSpec Records block scheduled for correction as a completion condition rather than as a nicety? [Completeness, tasks §9.5]
- [x] CHK526 Is the correction's CONTENT specified (four Modified Capabilities naming Decisions A and B), so it cannot be under-applied? [Clarity, tasks §9.5]
- [x] CHK527 Is the new family README's status header specified with the precedent it follows? [Consistency, tasks §3.1, research §Examples layout]
- [x] CHK528 Is registration required to be verifiable independent of the feature's own tests (a repo-level digest check)? [Measurability, tasks §9.6, §10.4]

## Rollback and the failure paths of a bundle cut

- [x] CHK529 Is the behaviour on a digest mismatch specified as fail-closed rather than warn? [Fail-closed, tasks §9.6, research §Registration mechanics]
- [x] CHK530 Is the recovery path from a bad cut implicit in the artifact set (the previous bundle's inventory remains on disk and consumers pin a version)? [Recovery, research §Registration mechanics]
- [x] CHK531 Is the case of a consumer pinned to the PREVIOUS bundle addressed by the additivity claim rather than by a migration step? [Recovery, research §Decision 3, plan §Cluster E]
- [x] CHK532 Are the phases whose content must be final before digests are computed identified as dependencies of the registration phase? [Dependency, tasks §Phase 9 header]

## Notes

- One item carried a defect (CHK515) and one inherited a fix from the scope checklist
  (CHK520). The ordering defect would have surfaced as a release-verifier failure over a
  file this same commit touched — a green-bar failure with a confusing cause.
