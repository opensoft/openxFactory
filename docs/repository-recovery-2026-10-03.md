# Repository recovery disposition, 2026-10-03

Status: record

## Shared-checkout rescue

The snapshot `rescue/shared-checkout-2026-09-30` at
`157fde825b2c08365ba8d1c700f6f097c94cff23` carried eleven changed paths.
Standards registry, policy and validator changes were adopted and hardened by
[PR #593](https://github.com/opensoft/openxFactory/pull/593): the licensing
source is separate from the publication source, duplicate mapping keys are
refused at load time, and verification claims determine the validation scope.
The corrected delta was promoted through
[PR #615](https://github.com/opensoft/openxFactory/pull/615).

The nightly proposal/design/spec/task edits and smoke implementation were
adopted with dated amendments and per-task evidence through
[PR #595](https://github.com/opensoft/openxFactory/pull/595), followed by its
realization and re-homing. Its archive packet is
`openspec/changes/archive/2026-09-16-add-nightly-dashboard-refresh/`.
The usage-controlled-evidence-chain index entry is already preserved on
`docs/add-usage-controlled-evidence-chain`,
[PR #518](https://github.com/opensoft/openxFactory/pull/518).

No unique rescue implementation is carried forward. The local rescue ref was
removed after an independent restoration of its exact tip and complete
reachable history from the verified cleanup bundle.

## Compliance archive

The snapshot `archive/015-intent-compliance-contract-1b48b028` at
`1b48b0286f82349f8d81929710c4f574295819af` was compared with its consolidated
implementation and current main. Its bounded Git-blob pre-read check is
recovered; old candidate releases and module layouts are superseded.
The publication evidence and open first-conformer obligations are recorded in
[the realization record](../openspec/changes/add-standing-policy-compliance-contract/realization-evidence.md).
The archival ref can be removed once the reviewed bounded-read correction
lands; the original snapshot remains recoverable from the cleanup bundle.

## Recovery storage

The operator-local cleanup archive contains verified Git bundles, original
working-file snapshots, commit/ref inventories, per-path disposition records,
and independent restoration evidence. `RECOVERY.md` in that archive explains
how to restore any deleted branch by fetching its named ref from the bundle.
The archive lives outside the repository; deleting local refs does not merge
unreviewed work or alter published tags.
