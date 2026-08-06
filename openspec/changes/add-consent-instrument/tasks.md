# Tasks: add-consent-instrument

## 1. Contracts (openxFactory)

- [x] 1.1 `contracts/schemas/consent-instrument.schema.yaml`: the
      `xfactory_consent_instrument` record kind — parties by rung (incl.
      estate hosts), scope + stated out-of-scope, delegation clauses,
      autonomy position, `authority_basis` enum (`direct`, `guardian`,
      `delegated`, `court_ordered`), revocation right + SLA, custody
      block (opaque locator + sha256, no original content), closed
      five-state `status`, amendment deltas on transition, dependent
      -artifact references, declared consent-profile mapping (or explicit
      `data_consent: none`), declared instrument class.
      (Done 2026-08-03: closed record shape, no `parent_ref` property
      anywhere per D7; free-shape delegation `access` blocks per D4.)
- [x] 1.2 `contracts/schemas/consent-instrument-class-registry.schema.yaml`:
      the domain-owned CLOSED class registry — every class declares
      custody-anchor kind and execution-evidence kind; optional declared
      lifecycle skips (D3) and status aliases per domain.
      (Done 2026-08-03: `signature_phase` boolean required per class —
      false is the declared direct-to-executed skip; plus the sibling
      `consent-purpose-model.schema.yaml` for the D4 purpose model.)
- [x] 1.3 Packaged examples + negatives: an executed engagement-letter
      instance (Ledgerx-shaped, alias `active` → `executed` declared), a
      portal-acceptance instance entering `executed` directly, a
      terminated instance with cascade-evidence refs; negatives for
      embedded original content, undeclared lifecycle skip, class without
      evidence kinds, citation to a terminated instrument, amendment
      modeled as a child instrument.
      (Done 2026-08-03: `examples/consent-instrument/` — 5 positives incl.
      registry + purpose model, 5 negatives + README map. The
      citation-to-terminated negative is deliberately replaced by
      `purpose-unresolvable.yaml`: citations live on grant artifacts this
      change does not own; R2 termination behavior is covered by the
      terminated positive + cascade-evidence rule.)
- [x] 1.4 `scripts/validate-consent-instruments.py` (D8, standalone):
      schema conformance, lifecycle/alias discipline, custody rules,
      purpose resolution (D4) against a domain-declared purpose model;
      NO technical access-shape checking; self-test over the packaged
      corpus; exit codes 0/1/2 per repo validator convention.
      (Done 2026-08-03: expected-finding table per negative, `--purpose`
      requested-purpose check, termination cascade-evidence + data-consent
      coherence rules; delegation `access` blocks passed over untouched.)
- [x] 1.5 Validate: the new validator's self-test plus
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.
      (Done 2026-08-03: self-test 5 valid / 5 negatives-for-intended-
      finding / 2 purpose probes, 0 errors 0 warnings `--strict`; repo-tree
      scan clean; `openspec validate add-consent-instrument --strict` and
      `--all --strict` pass.)
- [x] 1.6 Contract registration (`contracts/manifest.yaml`,
      `contracts/CHANGELOG.md`, contracts README rows) at the next
      additive bundle cut, per `docs/contract-versioning-policy.md`;
      DTN-016 → `adopted` in the domain-neutralization candidate
      register. (Done 2026-08-06 at **contract-v1.30**, tag published
      from release commit 6c03d78: three schema entries with per-file
      sha256, CHANGELOG entry, contracts-README rows, DTN-016 →
      `adopted` with realized-by note; verify-commit + verify-tag pass,
      manifest digests 124/124, consent validator self-test 0/0,
      OpenSpec --all --strict 53/53.)

## 2. Conformance declarations (coordination, own repos)

- [x] 2.1 LedgerxFactory: `ledgerx_engagement_consent_record` declares
      conformance — field/rung mapping, `active` → `executed` alias,
      `internal_beta_authorization` class registry entry, tenant-tree
      instance placement as declared domain policy (D9).
      (Done 2026-08-06, LedgerxFactory 8b5c03a:
      `policies/consent-instrument-classes.yaml` — registry +
      declaration header carrying the field/rung mapping under the
      ratified layer vocabulary — `policies/consent-purpose-model.yaml`,
      the lxtest neutral projection in the tenant tree, and the stack
      pin to the contract-v1.30 release commit.)
- [x] 2.2 MedxFactory: `medx_patient_consent_record` declares
      conformance — four-class registry mapping, derived consent-profile
      dependent ref (D1/D5), governed-store placement as declared domain
      policy (D9). No change to the archived Medx spec.
      (Done 2026-08-06, MedxFactory 3c7715a:
      `hermes/patient/consent-instrument-classes.yaml` — the four classes
      with custody anchors and evidence kinds verbatim from the archived
      patient-consent-instrument spec — `hermes/patient/
      consent-purpose-model.yaml` mirroring consent-model.yaml,
      the fictional projection example carrying the consent_profile
      dependent ref with derivation basis, and the stack pin to the
      contract-v1.30 release commit; `make validate` green.)

## 3. Docs and lifecycle

- [x] 3.1 README doc index + "OpenSpec Records" entry for this change.
      (Done 2026-08-03: "Consent Instrument Contract Family" row added to
      the README doc index — schemas + canonical validator + packaged
      corpus, pending bundle registration; the "OpenSpec Records" active-
      changes entry already existed from the propose commission.)
- [x] 3.2 Staging promotion executed with the proposal (this change):
      both topic docs moved to `supporting-docs/` with manifest, INDEX
      row + detail section removed, `ideation/README.md` promoted-list
      pointer added. (Substantially done at the 2026-08-03 propose
      commission; completed 2026-08-06 by repairing the hand-rolled
      support manifest to the canonical envelope — format_version,
      origin_path, source_revision 4728635 — and moving both support
      docs from `Status: staged` to `Status: draft` per the proposed-
      prose rule; `proposal-support.py verify` ok.)

## 4. Verification

- [x] 4.1 Validator self-test green over packaged examples/negatives;
      both conformance declarations (2.1, 2.2) accepted by the validator
      run from a pinned checkout in each domain repo.
      (Done 2026-08-06: self-test 5 valid / 5 negatives / 2 probes green;
      the checkout at the contract-v1.30 release commit — both domains'
      declared pin — accepted LedgerxFactory (3 artifacts, 0 errors) and
      MedxFactory (3 artifacts, 0 errors) sweeps.)
- [x] 4.2 Purpose-resolution check proven against the Medx purpose model
      and the Ledgerx engagement scope (one positive, one refusal each).
      (Done 2026-08-06: Ledgerx `--purpose ap-invoice-intake` resolves →
      bookkeeping (0 errors) and `--purpose payroll-support` refuses with
      `purpose-not-covered` against the lxtest projection; Medx
      `--purpose medx.patient.consent.treatment_planning_hypothesis`
      resolves → provider_processing (0 errors) and
      `--purpose medx.patient.consent.research_use` refuses with
      `purpose-not-covered` against the fictional projection example.)
