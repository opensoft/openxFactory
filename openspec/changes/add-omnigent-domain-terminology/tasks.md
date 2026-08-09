# Tasks — add-omnigent-domain-terminology

## 1. Direction and ratification

- [x] 1.1 Direction 2026-08-09 by Brett Heap: keep the neutral cross-domain
      spine, but render all user notices and logs in domain best-practice,
      well-adopted terminology so domain experts can read them. Analysis
      recorded in the proposal: annotate, never rename — renaming would point
      each domain at a different framework and churn load-bearing ids.
- [ ] 1.2 **Brett ratifies this change** — the optional `terminology` block,
      the descriptive-crosswalk rule, and the human-facing rendering
      requirement.

## 2. Contract (drafted, validator-green)

- [x] 2.1 `contracts/omnigent/omnigent-domain-overlay.schema.yaml`: optional
      `terminology` block (workers with `display_label` + optional
      `standards_alignment`; `job_types`, `stop_conditions`, `routing` as
      label maps via the new `label_map` $def). Additive and optional —
      all five existing overlays verified still valid.
- [x] 2.2 `scripts/validate-omnigent-contracts.py`: semantic checks — orphan
      terminology keys, duplicate display labels within a vocabulary,
      `no_clean_equivalent` without a note (per body), and crosswalk body ids
      resolving to the canonical registry.
- [x] 2.2b MULTI-BODY revision (Brett 2026-08-09: "if there are well adopted
      multiple standards, then we should have multiple mappings: one for each
      large body"). `standards_alignment` changed from a single object to a
      map keyed by standards-body id — at most one entry per body, multiple
      bodies expected. Revised while still draft, before ratification.
- [x] 2.2c `contracts/policies/standards-bodies.yaml` — canonical registry of
      recognized bodies (id, steward, `names`, scope, attribution note).
      `names` is load-bearing: bodies name different KINDS of thing
      (practices / processes / skills / roles / controls / competencies /
      clinical concepts), and a crosswalk is only honest if the kind is
      visible. Seeded with the cross-domain and per-domain menu; SOURCING
      CAVEAT recorded in the file — term spellings and framework versions are
      from working knowledge and MUST be verified against each body's current
      publication before a domain commits its crosswalk (task 3.x).
- [x] 2.3 Positive example extended to demonstrate terminology + both
      crosswalk shapes (a mapped term and an honest `no_clean_equivalent`).
      Note: authoring this caught its own bug — the first draft referenced
      ids the example does not declare, and the new orphan-key check
      rejected it, which is the check working.
- [x] 2.4 Three negative fixtures with `# expect:` markers (one per rule):
      `overlay-terminology-orphan-label.yaml`,
      `overlay-terminology-unmapped-without-note.yaml`,
      `overlay-terminology-unknown-body.yaml`. All rejected as expected;
      full contract-family check green.

## 3. Domain follow-ups (each its own change, in its own repo)

- [ ] 3.0 Per domain, VERIFY the chosen bodies' current terms and versions
      against each body's own publication before committing a crosswalk (the
      registry's sourcing caveat). A wrong term is worse than none.
- [ ] 3.1 Populate `terminology` in OpsxFactory. Candidate bodies: `itil4`
      (practices), `sfia` (skills — closest to worker shape), `apqc_pcf` 7.0
      (processes), `cobit_2019` (audit-facing), `nist_csf` (security-adjacent
      reviewers). `no_clean_equivalent` expected for `blast_radius_reviewer`
      and `credential_grant_reviewer`, which have no clean counterpart in a
      process framework.
- [ ] 3.2 Populate `terminology` in LedgerxFactory. Candidate bodies:
      `apqc_pcf` 8.0 (processes — 8.2 AP, 8.3 AR, 8.4 general accounting),
      `coso_icif` (controls — the natural home for the segregation-of-duties
      boundary), `ima_mac` (competencies), `aicpa` (standards/competencies).
      NOT GAAP/IFRS: those are REPORTING standards governing what the books
      say, not what a worker is — ledgerx's reporting-standard grounding
      already lives in the subject books-design layer.
- [ ] 3.3 Populate `terminology` in AdxFactory. Candidate bodies:
      `apqc_pcf` 3.0 (processes), `iab` (ad-tech specs/taxonomies — fits the
      media and audience classes, not the creative or compliance ones),
      `cim` (competencies), `ama_marketing` (concept definitions).
- [ ] 3.4 Populate `terminology` in codexFactory. Candidate bodies:
      `swebok` (knowledge areas), `sfia` (skills), `iso_iec_ieee_12207`
      (life-cycle processes), `apqc_pcf` 2.0.
- [ ] 3.5 Populate `terminology` in MedxFactory — WITH CARE. The provider
      taxonomies (`nucc_taxonomy`, `hl7_fhir_practitionerrole`) describe
      humans holding CLINICAL STANDING; medical Omnigent workers are
      reasoning agents and hold none. Mapping a reasoning agent onto a
      provider role would imply standing it must never appear to have, so
      `no_clean_equivalent` is expected to be the honest answer for most
      medical worker classes. `snomed_ct` fits artifact/job_type labels (the
      clinical CONTENT reasoned about), never the worker roles.

## 4. Consumer follow-up (named, not assumed)

- [ ] 4.1 Domain surfaces that render human-facing vocabulary OUTSIDE the
      overlay — e.g. OpsxFactory's fixed-order adjudication refusals, which
      name internal check ids (`tenant_managed`, `environment_operable`) in
      messages a human reads — adopt the same render-the-domain-label
      principle in their own contracts. The principle is not scoped to
      omnigent alone.

## 5. Explicitly out of scope

- [ ] 5.1 Renaming any worker class id, archetype, permission, or credential
      family — the whole point is that presentation changes and identity
      does not.
- [ ] 5.2 Asserting conformance with or certification by any named framework.
- [ ] 5.3 Choosing each domain's crosswalk framework (that is 3.1–3.4, per
      domain, with the domain's owner).
