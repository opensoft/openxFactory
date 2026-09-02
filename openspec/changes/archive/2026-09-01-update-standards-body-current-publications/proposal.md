# Update Standards-Body Current Publications

code_surface: openxFactory (`contracts/policies/standards-bodies.yaml` and
verification evidence)
target_release: none — registry and evidence content only; no contract bundle
Status: draft
Commissioned: 2026-09-01 by Brett Heap — upstream-registry-first ruling from
the OpsxFactory `adopt-neutral-omnigent-overlay` close-out.

## Why

The standards-body registry records historical ITIL 4 and SFIA references but
does not identify the current ITIL Version 5 and SFIA 9 publications. APQC PCF
8.0 is current and has a conditional in-document reuse grant, but its registry
entry must remain explicit about attribution. Domain overlays need a stable,
current registry vocabulary before they can make descriptive crosswalks without
silently using stale versions or overstating licensing rights.

## What Changes

- Add a distinct `itil5` registry body while preserving `itil4` for historical
  consumers and record provenance; do not silently rename the existing id.
- Update the SFIA registry metadata to identify SFIA 9 as current while keeping
  its product-configuration licensing restriction explicit.
- Re-verify the APQC PCF 8.0 current-version metadata and retain the mandatory
  attribution condition for any derivative configuration that embeds PCF terms.
- Add primary-source evidence for current publication, steward, term kind,
  version, and reuse/licensing status for each body.
- Keep crosswalks descriptive only: this change adds no framework hierarchy,
  practice text, skill definitions, process definitions, certification claim,
  or worker authority.
- Add validator coverage for current-version fields and registry-id
  resolution where the existing contract requires it.
- Authorize a later OpsxFactory crosswalk update for all nine worker classes to
  use APQC process terms, provided the required APQC attribution travels with
  the derivative configuration.

## Capabilities

### New Capabilities

- `standards-body-registry`: current-publication metadata, licensing posture,
  historical-id retention, and explicit operator overrides for descriptive
  crosswalk consumers.

### Modified Capabilities

- None. The existing Omnigent terminology requirement already requires
  crosswalk ids to resolve through this registry; its behavior is not widened
  by this amendment.

## Impact

- Affects `openxFactory/contracts/policies/standards-bodies.yaml`, its
  registry-validation tests/fixtures, and dated research evidence.
- Enables a later OpsxFactory overlay change to use current registry ids only
  after the relevant licensing and attribution ruling is satisfied.
- Does not modify any DomainxFactory overlay, workflow, adapter, credential,
  provider, or deployment surface.

## Primary sources to verify

- ITIL Version 5: <https://www.peoplecert.org/news-and-announcements/itil-version-5-explained>
- ITIL framework: <https://www.peoplecert.org/Frameworks-Professionals/ITIL-framework>
- SFIA 9: <https://sfia-online.org/en/sfia-9>
- SFIA licensing: <https://sfia-online.org/en/about-sfia/licensing-sfia/using-and-licensing-sfia>
- APQC PCF 8.0: <https://www.apqc.org/resource-library/resource-listing/apqc-process-classification-framework-pcf-cross-industry-pdf-13>
- APQC PCF FAQ: <https://www.apqc.org/process-frameworks/pcf-faqs>

## Decisions recorded for design

- **D1 — ITIL identity:** add `itil5` as a distinct registry id and retain
  `itil4` for historical consumers; no silent rename.
- **D2 — SFIA product configuration:** Brett selected the product-config
  `yes` option without licence evidence. The implementation MUST preserve the
  official SFIA licensing source and label this as an explicit operator
  override, not as a verified legal conclusion. The design must decide how
  that override is represented without making an unqualified licence claim.
- **D3 — APQC scope:** authorize all nine Opsx worker classes for a later
  APQC process crosswalk. The crosswalk remains descriptive and carries the
  APQC attribution; it confers no process authority on a worker.
- **D4 — Release:** no contract bundle or contract-version allocation is owed;
  this remains a standards-policy and evidence update.
