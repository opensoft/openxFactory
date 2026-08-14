# Tasks: add-client-identity-roster

## 1. Ratification gate (BRETT)

- [ ] 1.1 `OPENSPEC_TELEMETRY=0 openspec validate add-client-identity-roster
      --strict` and `--all --strict` green; change listed in the README
      OpenSpec Records block.
- [ ] 1.2 Brett ratification of the decisions in `design.md`. CLARIFY ROUND 1
      SETTLED four of them 2026-08-14 (`clarify-questions.md`, answers
      recorded inline): residency **class-independent** (client-resident for
      every class; LedgerxFactory's multi-tenant Reader/Poster pair must
      either declare the vendor-tenant-multi model with full obligations or
      move client-resident — named cross-domain follow-up); blocking scope
      **all three as drafted** (intra-repo blocks, cross-domain reports,
      drift refuses grant issuance); enrollment **as drafted** (permissive
      axis, `planned` entries, cost accepted); scope **contract + both
      wirings** (archives only with the consent cascade AND the doc-health
      family). STILL OPEN: Q5, the first-release `admission_surface`
      vocabulary scope. Explicit ratification of the change itself remains
      outstanding. The originally contestable points were:
      (a) **residency** — client-resident single-tenant as the default with a
      fully-obligated vendor-tenant-multi model as the governed alternative;
      this is the expensive decision and the review argued the multi-tenant
      shape is already the shipping architecture for at least two providers;
      (b) **blocking vs reporting** — intra-repo conformance fails the domain
      gate and an open drift finding refuses grant issuance, rather than
      everything being advisory;
      (c) **enrollment cost** — the axis is deliberately permissive about
      per-unit and per-duty identities, which is safer and more expensive;
      the lifecycle state softens the timing, not the total.
      Cross-model review: `review/decision-review-2026-08-14.md` (first draft
      reviewed; two blocking findings fixed by rewrite, verified against the
      tree before adoption). Everything below is parked behind this gate.

## 2. Neutral contract records (full realization pattern)

- [ ] 2.1 `contracts/schemas/xfactory-client-identity-roster.schema.yaml`
      (`schema_version` + `kind`; family `xfactory-` prefix): per-client
      roster fragment — `client_ref`, `domain`, `entries[]` each with
      `identity_ref`, `identity_kind`, `home_tenant`, `principal_locations[]`,
      `residency_model`, `admission_surface`, `duty`, `blast_radius_unit`,
      `authority_class_intended`, `authority_class_achieved`,
      `granted_permissions[]` (provider-native ids), `admission[]` (surface,
      act, `achieved_scope`, `enforcement_mode`, `evidence_ref`,
      `verified_at`), `declared_excess` (with `provider_reason`,
      `gate_obligation`, `enforcement_test_ref`), `per_unit_principal_available`,
      `lifecycle_state`, `standing_credential_attestation`, `ratified_by`
      (domain-qualified), `consent_ref`.
- [ ] 2.2 Closed `admission_surface` vocabulary, Entra-homed at first
      release, each entry naming its admission act and scoping mechanism;
      extension only by the change that governs a new surface. Non-Entra
      providers (client-org GitHub App installations) are named as a
      successor so this and `client-infrastructure-liaison` cannot both claim
      them.
- [ ] 2.3 Packaged `examples/client-identity-roster.example.yaml`: a
      two-domain client with (i) the BC pair as the worked case — TWO
      admission acts, one provider-enforced per-environment and one
      tenant-wide with no selector, declared excess + gate obligation +
      enforcement test; (ii) a provider-forced multi-surface reader; (iii) a
      duty-separated pair; (iv) one `planned` entry.
- [ ] 2.4 `scripts/validate-client-identity-roster.py` (canonical, network-free,
      deterministic) + fixtures: one positive roster, one negative per rule
      (cross-domain shared identity, undeclared reach, unverified admission
      counted as access, achieved>intended without excess, unresolvable gate
      obligation, missing enforcement test, provider-enforced claim with no
      per-unit principal, vendor-homed declared client-resident,
      mutate-without-ratified-capability, false standing-credential
      attestation).
- [ ] 2.5 Declared placement for domain roster fragments (so an instance
      cannot land where `validate-credential-contracts.py` skips it as out of
      scope and nothing else covers it), plus `contracts/manifest.yaml` row
      with sha256 + consumption rule, `contracts/CHANGELOG.md` entry, and the
      contract-bundle version bump.

## 3. Conformance wiring (blocking vs reporting)

- [ ] 3.1 Register the canonical validator in the `domain-conformance-checks`
      pack so intra-repo entry conformance is BLOCKING (nonzero fails the
      domain gate), per design Decision 7.
- [ ] 3.2 doc-health sixteenth family, CROSS-DOMAIN only: assemble per-client
      fragments from every pinned repo; report shared identity material and
      undeclared cross-domain reach; explicitly do NOT duplicate intra-repo
      rules. Severity/resolution classes assigned in the established
      auto-fixable/contested scheme (an entry contradicting a ratified
      capability is contested).
- [ ] 3.3 Wire the grant-issuance refusal: an open drift finding against an
      identity becomes an `issuance_preconditions` failure for grants naming
      it, using the mechanism already ratified on `deployment_operator` /
      `aks_workload_administration`.
- [ ] 3.4 consent-instrument cascade realization: governed identities appear
      in the dependent-reference list, and cascade evidence covers identity
      removal/retirement AND withdrawal of provider-side admission.

## 4. Domain conformance (named; executed in the domain repos)

- [ ] 4.1 OpsxFactory publishes its fragment, including the three findings
      this investigation surfaced: the `opsx-farheap-bc-observer`
      name/purpose mismatch (achieves more than observation), the inert
      Microsoft Graph delegated scope its identity record omits, and the
      tenant-wide admin-center excess with its gate obligation and
      enforcement test. Its BC entry exercises the two-admission-act case.
- [ ] 4.2 LedgerxFactory publishes its `ledgerx-farheap-bc-*` fragment,
      exercising duty separation and — with 4.1 — the cross-domain
      composition rule against a real two-domain client tenant.
- [ ] 4.3 Live client-tenant drift detection remains a domain realization;
      record `add-github-installation-policy` as the reference pattern and
      note the client-tenant variant is its own domain change.

## 5. Validation and exit

- [ ] 5.1 `openspec validate --all --strict` green; canonical validator green
      over fixtures; doc-health family green; the two MODIFIED capabilities'
      own suites unaffected.
- [ ] 5.2 DTN candidate register row if warranted (identity topology is
      neutral by construction).
- [ ] 5.3 Archive on realization evidence per `release-realization` (schema,
      validator, examples, manifest/CHANGELOG/bundle, both wirings landed and
      green). Domain fragments (section 4) are follow-ups, not archive
      blockers.
