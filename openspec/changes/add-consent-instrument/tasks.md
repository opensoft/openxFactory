# Tasks: add-consent-instrument

## 1. Contracts (openxFactory)

- [ ] 1.1 `contracts/schemas/consent-instrument.schema.yaml`: the
      `xfactory_consent_instrument` record kind — parties by rung (incl.
      estate hosts), scope + stated out-of-scope, delegation clauses,
      autonomy position, `authority_basis` enum (`direct`, `guardian`,
      `delegated`, `court_ordered`), revocation right + SLA, custody
      block (opaque locator + sha256, no original content), closed
      five-state `status`, amendment deltas on transition, dependent
      -artifact references, declared consent-profile mapping (or explicit
      `data_consent: none`), declared instrument class.
- [ ] 1.2 `contracts/schemas/consent-instrument-class-registry.schema.yaml`:
      the domain-owned CLOSED class registry — every class declares
      custody-anchor kind and execution-evidence kind; optional declared
      lifecycle skips (D3) and status aliases per domain.
- [ ] 1.3 Packaged examples + negatives: an executed engagement-letter
      instance (Ledgerx-shaped, alias `active` → `executed` declared), a
      portal-acceptance instance entering `executed` directly, a
      terminated instance with cascade-evidence refs; negatives for
      embedded original content, undeclared lifecycle skip, class without
      evidence kinds, citation to a terminated instrument, amendment
      modeled as a child instrument.
- [ ] 1.4 `scripts/validate-consent-instruments.py` (D8, standalone):
      schema conformance, lifecycle/alias discipline, custody rules,
      purpose resolution (D4) against a domain-declared purpose model;
      NO technical access-shape checking; self-test over the packaged
      corpus; exit codes 0/1/2 per repo validator convention.
- [ ] 1.5 Validate: the new validator's self-test plus
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.
- [ ] 1.6 Contract registration (`contracts/manifest.yaml`,
      `contracts/CHANGELOG.md`, contracts README rows) at the next
      additive bundle cut, per `docs/contract-versioning-policy.md`;
      DTN-016 → `adopted` in the domain-neutralization candidate
      register.

## 2. Conformance declarations (coordination, own repos)

- [ ] 2.1 LedgerxFactory: `ledgerx_engagement_consent_record` declares
      conformance — field/rung mapping, `active` → `executed` alias,
      `internal_beta_authorization` class registry entry, tenant-tree
      instance placement as declared domain policy (D9).
- [ ] 2.2 MedxFactory: `medx_patient_consent_record` declares
      conformance — four-class registry mapping, derived consent-profile
      dependent ref (D1/D5), governed-store placement as declared domain
      policy (D9). No change to the archived Medx spec.

## 3. Docs and lifecycle

- [ ] 3.1 README doc index + "OpenSpec Records" entry for this change.
- [ ] 3.2 Staging promotion executed with the proposal (this change):
      both topic docs moved to `supporting-docs/` with manifest, INDEX
      row + detail section removed, `ideation/README.md` promoted-list
      pointer added.

## 4. Verification

- [ ] 4.1 Validator self-test green over packaged examples/negatives;
      both conformance declarations (2.1, 2.2) accepted by the validator
      run from a pinned checkout in each domain repo.
- [ ] 4.2 Purpose-resolution check proven against the Medx purpose model
      and the Ledgerx engagement scope (one positive, one refusal each).
