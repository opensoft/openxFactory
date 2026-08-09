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
      terminology keys, duplicate display labels within a vocabulary, and
      `no_clean_equivalent` without a note.
- [x] 2.3 Positive example extended to demonstrate terminology + both
      crosswalk shapes (a mapped term and an honest `no_clean_equivalent`).
      Note: authoring this caught its own bug — the first draft referenced
      ids the example does not declare, and the new orphan-key check
      rejected it, which is the check working.
- [x] 2.4 Two negative fixtures with `# expect:` markers:
      `overlay-terminology-orphan-label.yaml`,
      `overlay-terminology-unmapped-without-note.yaml`. Both rejected as
      expected; full contract-family check green.

## 3. Domain follow-ups (each its own change, in its own repo)

- [ ] 3.1 Populate `terminology` in OpsxFactory (IT-operations vocabulary;
      candidate crosswalk framework ITIL or COBIT — Brett picks, and
      `no_clean_equivalent` is expected for classes like
      `blast_radius_reviewer` that have no process-framework counterpart).
- [ ] 3.2 Populate `terminology` in LedgerxFactory (accounting vocabulary;
      candidate crosswalk AICPA/GAAP role conventions). Distinct from the
      subject books-design industry-archetype registry, which is a different
      layer.
- [ ] 3.3 Populate `terminology` in AdxFactory (marketing vocabulary;
      candidate crosswalk IAB or agency org conventions).
- [ ] 3.4 Populate `terminology` in codexFactory and MedxFactory (the two
      reference conformers) so the family is consistent.

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
