## Context

The standards-body registry is the canonical vocabulary source for descriptive
domain terminology crosswalks. Its original IT-operations entries were written
from working knowledge and retained historical ids, but they did not carry a
complete current-publication record. The current primary-source review identifies
ITIL Version 5, SFIA 9, and APQC PCF 8.0 as the current publications, with
materially different reuse postures.

The change is upstream of DomainxFactory overlays. It must update registry facts
without copying protected framework content into the registry or changing any
workflow, adapter, credential, or provider behavior.

## Goals / Non-Goals

**Goals:**

- Add a distinct `itil5` body id while preserving `itil4` for historical
  consumers.
- Record current-version and primary-source metadata for ITIL, SFIA, and APQC.
- Make licensing status and operator overrides explicit and machine-readable.
- Preserve the descriptive-only nature of terminology crosswalks.
- Authorize a later OpsxFactory process crosswalk to APQC for all nine classes,
  with APQC attribution carried by the derivative overlay.

**Non-Goals:**

- No ITIL practice text, SFIA skill definitions, or APQC process hierarchy is
  copied into this repository.
- No DomainxFactory overlay is modified by this upstream amendment.
- No certification, conformance, endorsement, or worker authority is asserted.
- No contract release bundle is allocated.

## Decisions

### D1 — Preserve historical ITIL identity

Add `itil5` rather than renaming `itil4`. Existing archived evidence and
consumers retain their original meaning; new consumers can resolve the current
publication explicitly. The alternatives—renaming or silently aliasing—would
make historical records ambiguous.

### D2 — Represent the SFIA operator override without laundering it

Update the SFIA entry to current version SFIA 9 and retain the official primary
licensing evidence. Brett selected product-config `yes` without licence
evidence. The registry therefore records an explicit operator override and its
unverified legal status beside the requested product-config value. A validator
must reject an override that lacks approver, date, rationale, and source
conflict evidence. This preserves the decision while preventing readers from
mistaking it for a verified licence grant.

### D3 — Keep APQC broad enough for the authorized Opsx follow-up

Retain APQC PCF 8.0 as current and conditionally reusable with the required
attribution. The registry records the IT-process category as an available
crosswalk scope in addition to existing finance scope; it does not embed the
PCF hierarchy. The later Opsx change may map all nine workers, but each mapping
remains descriptive and carries no authority.

### D4 — No contract bundle

This is policy metadata and evidence, not a neutral contract schema change.
Archive requires merged registry content, validator-green evidence, and a
clean source record; no contract version is allocated.

## Risks / Trade-offs

- **[Risk]** The SFIA override may conflict with the steward's licence terms.
  **Mitigation:** retain the official conflict evidence, label the override
  unverified, and require a named future legal/licensing review.
- **[Risk]** Adding `itil5` can cause consumers to assume ITIL content is
  redistributable. **Mitigation:** retain proprietary licensing metadata and
  keep crosswalks descriptive only.
- **[Risk]** Mapping all nine Opsx classes to APQC could force poor process
  matches. **Mitigation:** the later crosswalk may use `no_clean_equivalent`
  with a reason, despite the authorization to evaluate all nine.
- **[Risk]** Registry metadata drift from source publications. **Mitigation:**
  require current-version, source URL, confidence, and verification date for
  current entries and test the required fields.

## Migration Plan

1. Add evidence and update the registry in openxFactory.
2. Run registry and Omnigent terminology validators plus the relevant tests.
3. Merge and archive this registry amendment without a contract bundle.
4. Update OpsxFactory in its own follow-up change using the now-resolvable
   current ids and APQC attribution.

Rollback is one revert of the registry amendment. Historical `itil4` remains
untouched, so rollback does not invalidate existing archived references.

## Open Questions

- Who will provide the written SFIA permission or legal review that can replace
  the unverified operator override?
- Which exact APQC PCF 8.0 IT-process terms are honest counterparts for each of
  the nine Opsx worker classes? The Opsx follow-up must answer this per class.
