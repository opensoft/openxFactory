# OpsxFactory Current-Standards Handoff

Handoff from `update-standards-body-current-publications` to
`adopt-neutral-omnigent-overlay`.

## Registry inputs

| Body id | Current publication | Opsx use | Constraint |
|---|---|---|---|
| `itil5` | ITIL Version 5 | available for descriptive practice crosswalk review | proprietary; no product-config permission established |
| `sfia` | SFIA 9 | available under the recorded operator override | override is unverified and conflicts with the official licence reading |
| `apqc_pcf` | Cross-Industry PCF 8.0 | all nine worker classes may be evaluated against IT-process terms | carry APQC attribution; mapping remains descriptive |

## Required consumer behavior

- Preserve the neutral worker ids and archetypes.
- Use at most one mapping per standards body per worker.
- Do not copy framework hierarchy, practice guidance, skill definitions, or
  process definitions into the overlay.
- Never infer execution authority, credential access, certification, or
  endorsement from a crosswalk.
- Use `no_clean_equivalent` with a reason when an exact counterpart is not
  honest; the authorization to evaluate all nine APQC mappings is not an order
  to force nine matches.

## Follow-up ownership

The OpsxFactory change owns the actual worker crosswalk and the APQC attribution
in its shipped overlay. The SFIA written-permission/legal review remains an
operator follow-up; this handoff does not resolve it.
