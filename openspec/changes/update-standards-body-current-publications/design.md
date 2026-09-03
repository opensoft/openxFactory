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

### D5 — Key the completeness obligation to the CLAIM, not to `status: current`

**ADDED 2026-09-03 on PR #593, Copilot review round 2, and it is a correction
rather than a refinement.** The requirement as first drafted obliged "every body
marked current" to carry a complete current-publication record including a
verification date. Measured against the registry it governs: of 45 bodies, **32
carry `status: current` and exactly 3 carry a verification date** — the three
this change read against primary sources. The requirement would have been FALSE
of 29 records on the day it was promoted, and the validator's three-id allowlist
was quietly doing something narrower than the requirement claimed, which is the
worse half of the defect: a rule nobody could see was not being applied.

Two ways to make it true were available and both were refused. Backfilling 29
verification dates is the fabrication the registry's own header forbids in terms
— those entries are "drawn from working knowledge, not verified against each
body's current publication", an asymmetry it calls "deliberate rather than
hidden". Demoting 29 records out of `status: current` would misstate their
currency to satisfy a checker.

So the obligation is keyed to `verified_on`, which IS the verification claim: a
body declaring one asserts its facts were read from that body's own material on
that date and owes the whole record; a body declaring none asserts nothing and is
left as it stands. The named three are a FLOOR on top of that, so the claim
cannot be withdrawn to escape a finding. The rule is now true of every record
that makes a claim, enforced on every record added or amended from here, and
silent about records that assert nothing.

**The 29 are not thereby blessed.** Re-verifying them is real work, named in
Open Questions below and owed to a successor; this change does not pretend it
away and does not attempt it.

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
- **Who re-verifies the 29 `status: current` bodies that carry no verification
  date, and in what order?** Measured 2026-09-03 (D5): 32 bodies are marked
  current and 3 carry a claim. The gap is the registry's original sourcing
  caveat, unresolved rather than introduced here, and it is the reason this
  change's completeness obligation is keyed to the claim. A successor doing that
  work needs only to add `verified_on` plus the record beside it, one body at a
  time — the checker already enforces the whole record the moment a claim
  appears, so the migration is incremental by construction and cannot land
  half-done in a single body.
