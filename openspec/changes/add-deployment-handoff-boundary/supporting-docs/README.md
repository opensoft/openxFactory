# Supporting Documents — add-deployment-handoff-boundary

Origin: `ideation/staging/deployment-handoff-boundary/` (staging ID
`openxFactory:staging:deployment-handoff-boundary`), moved here at the
proposal gate on 2026-07-28 per the document lifecycle. The staging INDEX
row and detail section were retired in the same commit; the promoted-list
pointer lives in `ideation/README.md`.

Contents:

- [deployment-handoff-boundary.md](deployment-handoff-boundary.md) — the
  primary staged doc: the managed-subject rule and test, six claims, the
  layered enforcement table, the seven clarifying resolutions
  (2026-07-24, Brett), residual decisions, and the exit conditions. All
  normative content is represented in the proposal, design, and spec
  deltas; this copy is provenance under the proposal-support archive
  gate.

Disposition map:

- The rule, test, actor scope, and tier calibration → capability
  requirement "The managed-subject test routes deployment execution".
- Claim 2 (crossing artifact) → requirement "The handoff crosses as a
  client infrastructure request".
- Claim 3 (credential non-possession; resolutions 1, 3) → requirement
  "No standing deployment credentials outside the managing factory".
- Claim 4 (structural channels) → requirement "Managed surfaces admit
  change through structural channels".
- Claim 5 (detectability; resolution 4) → requirement "Out-of-band
  change is detectable".
- Resolution 5 (benches) → requirement "Cadenced publication rides a
  standing maintenance request".
- Resolution 2 (phasing) → requirement "Adoption is phased, never
  gapped".
- Resolution 6 (break-glass custody) → design decision 7 and the escrow
  coordination task; resolution 7 (first consumer) → design decision 9.
- The release-realization correlation delta → the MODIFIED
  "Realization archive gate" requirement.
- Residual decisions → design Open Questions (QA calibration, ACR scope
  map, preview threshold, break-glass window).
