# Tasks: openxWallet neutral contracts

**Feature**: `006-openxwallet-contracts` · **Change**: `add-openxwallet`

Realizes the change's handoff tasks 3.1 and 3.2. The change's `tasks.md` stays
governance-level and is not duplicated here.

## Phase 1 — decisions that gate the schema (change tasks 2.2, 3.2)

- [x] 1.1 Settle the closed custody enumeration: three members, two declared
      booleans, `evidences` DERIVED and enforced. Recorded in `research.md`
      with the interpretive call stated (the ratified "only custody
      isolating…" is a necessary condition, not a sufficient one).
- [x] 1.2 Settle what the composition component set covers: per-component
      `binding_mode`, corpora bound by identity and governing configuration
      rather than by contents. Recorded in `research.md`.
- [x] 1.3 Resolve the `approval_policy` dependency: it is an OBJECT with three
      properties, not a flat enum, so the legal scope vocabulary is that
      property set — and the validator reads it from the canonical envelope
      schema at run time rather than restating it.

## Phase 2 — the core family (User Story 1, P1)

- [x] 2.1 `openxwallet-record.schema.yaml` — holder, key reference, declared
      custody; `additionalProperties: false` throughout so no key-shaped
      property can be added at any depth.
- [x] 2.2 `openxwallet-custody-registry.schema.yaml` + the closed instance
      `openxwallet-custody.registry.yaml` — what each model evidences and the
      authority it caps, plus the deliberate non-members.
- [x] 2.3 `openxwallet-grant.schema.yaml` — audience, scope, expiry, parent.
- [x] 2.4 `openxwallet-grant-exercise.schema.yaml` — proof of possession, event
      class, key attribution, revocation check, constraint evaluations.
- [x] 2.5 `openxwallet-subject-attestation.schema.yaml` — the non-substrate
      rule, with the wrong reading made unrepresentable.
- [x] 2.6 `contracts/openxwallet/README.md` with a `Status:` header naming the
      ratifying change.

## Phase 3 — segregation of duties (User Story 2, P2)

- [x] 3.1 `openxwallet-distinct-holder-constraint.schema.yaml` — two acts on
      one object, opt-in, with a declared distinctness floor.
- [x] 3.2 Positive fixtures expressing the first consumer's control end to
      end, including the honest recording of an unattributable act.

## Phase 4 — the agent profile (User Story 3, P3)

- [x] 4.1 `contracts/openxwallet-agent-profile/` as a SIBLING family, so the
      core/profile seam is structural rather than a promise.
- [x] 4.2 `openxwallet-agent-composition.schema.yaml` — composition hash, the
      component set it covers, per-component binding mode, attestation.
- [x] 4.3 `contracts/openxwallet-agent-profile/README.md` with a `Status:`
      header.

## Phase 5 — the validator

- [x] 5.1 `scripts/validate-openxwallet.py` following the repo's
      `validate-*.py` shape: standalone, runtime-resolved root, `Findings`
      with kebab-case codes, self-test plus optional repo scan, exit 0/1/2.
- [x] 5.2 Seventeen lettered rules the shapes cannot express, each citing the
      requirement it enforces.
- [x] 5.3 Read the approval-scope vocabulary from the canonical job envelope
      at run time.

## Phase 6 — the negative-confirmation corpus

- [x] 6.1 Ten probes for the ten violations the change names.
- [x] 6.2 Three further probes for the custody enumeration itself — the
      ruling's sharp edge, including the collapse that distinguishes the two
      cases in NAME while collapsing them in EFFECT.
- [x] 6.3 Three further probes for the clauses that would otherwise go
      unproven: a refusal naming the wrong absence, an unattributable act, and
      a composition change with live grants.
- [x] 6.4 `# requirement:` attribution plus closed coverage checking in both
      directions, so a requirement cannot silently lose its probe.
- [x] 6.5 Red-proof harness (`evidence/red-proof.py`) and its recorded output:
      all fifteen finding codes load-bearing.
- [x] 6.6 `traceability.yaml` — one row per ratified requirement with its
      artifact, its enforcing check, its probe, and its red-proof.

## Phase 7 — registration and the green bar

- [ ] 7.1 Register both families in `contracts/manifest.yaml` with per-file
      digests and bump `contract_bundle_version`.
- [ ] 7.2 `contracts/CHANGELOG.md` entry naming the realizing tasks, the
      validator, and the corpus counts.
- [ ] 7.3 `contracts/README.md` native contract index rows.
- [ ] 7.4 Root `README.md`: `## Conformance` bullet and document-index links.
- [ ] 7.5 `ideation/staging/INDEX.md` row and detail section updated in the
      same commit as the status move.
- [ ] 7.6 Tick the change's own tasks 1.3, 3.1, 3.2, 4.1–4.3, 5.1–5.3.
- [ ] 7.7 Full bar: `validate-openxwallet.py`, `validate-manifest-digests.py`,
      `openspec validate --all --strict`, doc-health with no new finding.
- [ ] 7.8 Commit with explicit pathspecs (shared checkout), push, open the PR.
