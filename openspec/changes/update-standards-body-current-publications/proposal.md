---
code_surface: openxFactory (`scripts/standards_body_registry.py` — a NEW stdlib-only reader module owning the registry's completeness and override rules, in the pattern `scripts/scope_globs.py` and `scripts/frontmatter_strict.py` already set: a pure `registry_errors(document)` over a loaded mapping, with no I/O, no CLI and no gate of its own. `scripts/validate-omnigent-contracts.py` — TWO LINES: the import, and one loop in `main()` that fails the existing validator on any registry finding, so the reader is reached by a gate that already runs rather than by a new one. `tests/test_standards_body_registry.py` and `tests/fixtures-standards-body-registry-unqualified-override.yaml` — five scenarios over the live registry plus one negative fixture for the incomplete-override arm. `contracts/policies/standards-bodies.yaml` — the registry content itself: a new `itil5` body, SFIA's current-publication and operator-override fields, and APQC's `verified_on` plus `crosswalk_scopes`. NO change to any file under `contracts/schemas/`, to `contracts/manifest.yaml`, to any `contracts/releases/*.digests.yaml`, to the omnigent overlay or install-manifest schemas, to `semantic_errors`, to any DomainxFactory overlay, or to any credential, provider or deployment surface.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle: no schema under `contracts/schemas/` moves, no digest set moves, and no release tag is owed by it, so the archive gate is merge-plus-green in the shape `add-release-tag-publication-check` and `add-family-enumeration-check` both used — `python3 -m pytest -q tests/test_standards_body_registry.py` green, `python3 scripts/validate-omnigent-contracts.py` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green. MEASURED, NOT ASSUMED, and the reason `target_release` is `implemented` rather than a bundle id: `contracts/policies/standards-bodies.yaml` is NOT a member of `contracts/releases/contract-v3.0.digests.yaml` (283 entries, ZERO under `contracts/policies/`) and is NOT listed in `contracts/manifest.yaml` (which carries three policies — `hermes-governance-agents.yaml`, `merge-risk-policy.yaml`, `layer-vocabulary.yaml` — and not this one), so editing it between cuts raises NO `release-inventory-drift` finding and owes no bundle. The original packet's `target_release: none` was WRONG on the release-realization contract's own terms rather than on this fact: `none` is reserved for a doc-only change, and this packet ships a module, a validator line and tests.
Status: ratified
Ratified: 2026-09-03 by Brett Heap — in-session, verbatim "merge 210 and ratify and merge 593"; D1–D4 adopted as written (D2 the SFIA operator override, D3 the later APQC crosswalk authorization scope), ratifying the rescued packet as adopted by lane openxfactory-f2 in PR #593
Proposed: 2026-09-01
Origin: no staged topic — searched `ideation/staging/` and its `INDEX.md` for the registry, ITIL, SFIA and APQC subjects and found none. Commissioned in session by Brett Heap on 2026-09-01, as the upstream-registry-first half of the OpsxFactory `adopt-neutral-omnigent-overlay` close-out. **THE COMMISSIONING IS THE PACKET'S OWN RECORD, CARRIED FORWARD FROM THE RESCUED SNAPSHOT AND NOT RE-VERIFIED BY THE ADOPTING LANE** — see `.openspec.yaml` `origin.approved_by`, which says so in the same words. The SEPARATE and later act this branch stands on is Brett Heap's ruling of 2026-09-03, in session, that PR #593 be ADOPTED and owned by lane `openxfactory-f2`; that ruling authorizes the ADOPTION and RESHAPING of a stranded packet and is NOT a ratification of its content. `Status:` stayed `draft` through adoption and was flipped to `ratified` on 2026-09-03 by Brett Heap's in-session word (see `Ratified:`).
---

# Update Standards-Body Current Publications

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

- Affects `openxFactory/contracts/policies/standards-bodies.yaml`, the new
  `scripts/standards_body_registry.py` reader, the two lines in
  `scripts/validate-omnigent-contracts.py` that reach it, the
  registry-validation tests/fixtures, and dated research evidence.
- **NOT a contract-bundle member.** `contracts/policies/standards-bodies.yaml`
  appears in neither `contracts/manifest.yaml` nor
  `contracts/releases/contract-v3.0.digests.yaml`, so this edit raises no
  `release-inventory-drift` finding and owes no cut.
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
  this remains a standards-policy and evidence update. The front matter
  therefore reads `target_release: implemented` — the openxFactory main line —
  and NOT `target_release: none`, which the release-realization contract
  reserves for a change with `code_surface: none`. The registry file's
  non-membership of the declared bundle is what makes that reading available;
  it is measured in the front matter rather than assumed.
