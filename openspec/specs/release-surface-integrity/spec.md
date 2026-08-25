# release-surface-integrity Specification

## Purpose
TBD - created by archiving change add-release-inventory-drift-check. Update Purpose after archive.
## Requirements
### Requirement: The declared bundle describes the release surface
The contract bundle a repository DECLARES at a commit SHALL describe that
commit's release surface. Concretely: for every member of the declared
bundle's release digest inventory, the blob at that commit SHALL match the
digest the inventory records, except for the EDITORIAL MEMBERS named below
between cuts.

THE EDITORIAL MEMBERS are `contracts/CHANGELOG.md`, `contracts/manifest.yaml`
and `contracts/README.md` — the three inventory members that legitimately
move between releases, because a change that touches no contract still records
itself in the changelog and still updates a consumption rule or a per-file
digest. Drift confined to them is an EXPECTED, BOUNDED state that the next cut
re-baselines, and it SHALL NOT be reported as a defect.

Drift in ANY OTHER member is a defect: a normative contract's bytes moved
while the repository continued to declare a bundle that describes different
bytes, so the declared version no longer identifies what a consumer would
receive. This is the same defect the `contract-v1.36` cut carried — its
`contract_bundle_version` was left at the previous release, so the tree was
measured against the wrong inventory — and that case is detectable by this
rule at the commit, before any tag is published.

This requirement states the OBLIGATION only. Whether and how it is CHECKED is
`doc-health`'s to define, in the same by-reference relationship the tag-hygiene
family already has with `document-lifecycle`'s marker grammar. Nothing here
requires a gate, a severity, or a report section.

THE EDITORIAL SET IS EXACTLY THREE MEMBERS and `contracts/README.md` is one of
them by ruling (Brett, 2026-08-24), not by observation: it had not drifted in
the window measured, so its inclusion is a decision about what may legitimately
move between cuts rather than a description of what has.

A published annotated tag is NOT the reference point, deliberately: a declared
bundle need not have one. `contract-v1.33`, `contract-v1.35` and
`contract-v1.39` are recorded in the changelog and the manifest with no
published tag, so a rule anchored on a tag would be unevaluable for them. The
inventory FILE at the commit is the reference, and it is present whenever the
bundle is declared.

#### Scenario: A normative contract drifts from the declared bundle
- **WHEN** a commit declares a bundle and a non-editorial member of that bundle's inventory does not match its recorded digest at that commit
- **THEN** the declared bundle no longer describes the release surface and the condition MUST be reportable as a defect
- **AND** the remedy is a release cut through the bundle realization order, never a hand-edit of the inventory to match the tree

#### Scenario: Only the editorial members have moved
- **WHEN** the only members differing from the declared bundle's inventory are the changelog, the manifest and the README
- **THEN** the state is expected between cuts and MUST NOT be reported as a defect
- **AND** the next release cut re-baselines the inventory as part of the realization order

#### Scenario: A cut forgets to advance the declared bundle
- **WHEN** a release candidate updates contract files but leaves `contract_bundle_version` naming the previous bundle
- **THEN** the changed contracts appear as non-editorial drift against that previous bundle's inventory, and the condition is detectable at the commit rather than only at tag-verify time

#### Scenario: The declared bundle was never tagged
- **WHEN** the declared bundle has no published annotated tag
- **THEN** the obligation is still evaluable, because the reference is the inventory file recorded at the commit rather than a tag

