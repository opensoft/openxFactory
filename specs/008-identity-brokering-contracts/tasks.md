# Tasks: identity-brokering neutral contracts

**Feature**: `008-identity-brokering-contracts` · **Change**:
`add-identity-brokering`

Realizes the change's tasks 1.1–1.10 plus the promotion bookkeeping in 3.1 and
3.2. The change's `tasks.md` stays governance-level and is not duplicated here.

## Phase 1 — settlements that gate the schemas (change task 2.3)

- [x] 1.1 Settle the `actor_subject` field shape: the STRUCTURED REFERENCE
      (issuer + opaque subject + display name at record, plus a provenance
      discriminator). Recorded in `research.md` with the reasoning and with what
      the settlement deliberately leaves to the consuming gate-console change.
- [x] 1.2 Settle pre-broker history: MARK THE BOUNDARY DATE, MAP ON DEMAND,
      never a blanket backfill. Recorded in `research.md`, realized as the three
      provenance classes with the wrong combinations unrepresentable.
- [x] 1.3 Resolve the company-role / layer-vocabulary tension: the enumeration
      is `tenant | served` as the ratified task text fixes it, with an explicit
      bridge to the canonical layers whose targets and reserved terms are read
      from `contracts/policies/layer-vocabulary.yaml` at run time.

## Phase 2 — the persona and the company boundary (User Story 1, P1)

- [x] 2.1 `persona-assertion.schema.yaml` (`kind: persona_assertion`) — issuing
      instance, opaque subject, display name, linked upstream identities,
      organization memberships, assertion time; `additionalProperties: false`
      at every depth so no role, group, grant, project, stack, layer or domain
      can be added (change task 1.1).
- [x] 2.2 `broker-organization.schema.yaml` (`kind: broker_organization`) —
      organization id, company role, routed domains, federated provider
      references, and `governed_record_refs` bounded at ONE item: the
      pointer-not-projection line as a bound rather than as prose (change task
      1.2).
- [x] 2.3 `surface-adoption.schema.yaml`'s `human_accounts_held_by_surface` as
      a required constant `false` — R1's second clause, structural.

## Phase 3 — linking and merge safety (User Story 2, P2)

- [x] 3.1 `identity-link-record.schema.yaml` (`kind: identity_link_record`) —
      mode requiring its actor by shape, the two admissible bases, every
      pre-merge subject with the survivor it remains resolvable to (change task
      1.4).
- [x] 3.2 The three cross-record rules the shape cannot carry: an actor is
      named, every prior subject resolves to the survivor, a self link is
      initiated from a session already holding the persona.
- [x] 3.3 The cross-instance rule: subjects that resolve must resolve within
      the record's own instance (spec R8's personas-do-not-span-instances
      clause).

## Phase 4 — the actor a governed record names (User Story 3, P3)

- [x] 4.1 `actor-subject-reference.schema.yaml`
      (`kind: actor_subject_reference`) — the structured reference and the three
      provenance classes, with `pre_broker.presented_as_persona` a required
      constant `false` (change task 1.3).
- [x] 4.2 The identifier-position rules: no display name, no email address, no
      upstream account name, and never `broker_asserted` for a bare username the
      corpus records as pre-broker.

## Phase 5 — workloads, credentials, posture and isolation

- [x] 5.1 `broker-client-declaration.schema.yaml`
      (`kind: broker_client_declaration`) — the surface served, the stated token
      need, the credential requirement by reference, and the three transport
      constants; no actor role and no membership field exist (change task 1.5).
- [x] 5.2 `surface-adoption.schema.yaml` (`kind: broker_surface_adoption`) —
      declared posture, write actions, governed decision point, retired
      credential, isolation (change task 1.6).
- [x] 5.3 The workload rules: a declared client's subject may not appear as a
      persona nor as a governed record's actor.
- [x] 5.4 The credential rules: references only, plus value detection BY CLASS
      across names, values and values reassembled from adjacent chunks.
- [x] 5.5 The posture and isolation rules: write actions require the stronger
      posture and a named decision point; a restricted population requires a
      dedicated instance; a replaced shared credential must be retired.

## Phase 6 — the family README

- [x] 6.1 `contracts/identity-brokering/README.md` with a `Status:` header
      naming the ratifying change, the nine rules, custody by composition,
      isolation by instance with silence on count, the record-kind table, and
      the named consumers (change task 1.7).

## Phase 7 — the validator

- [x] 7.1 `scripts/validate-identity-brokering.py` following the repo's
      `validate-*.py` shape: standalone, runtime-resolved root, `Findings` with
      kebab-case codes, self-test plus optional repo scan, exit 0/1/2 (change
      task 1.9).
- [x] 7.2 Thirteen lettered rules the shapes cannot express, each citing the
      requirement it enforces.
- [x] 7.3 The closed allow-list DERIVED FROM THE SCHEMA — resolving local
      `$ref`s and unioning branches — rather than written as a second list.
- [x] 7.4 Read the layer vocabulary from the ratified policy, and the link bases
      and resolution point from the family's own schemas, at run time.

## Phase 8 — the negative-confirmation corpus

- [x] 8.1 Fourteen positives, including the two settlements' worked cases (a
      pre-broker reference and its mapped counterpart) and the two ends of the
      isolation rule (a restricted population on a dedicated instance, and an
      unrestricted single-organization deployment on its own) (change task 1.8).
- [x] 8.2 The eighteen negatives the change names, each failing for the rule it
      is named for.
- [x] 8.3 Nine further probes for ratified clauses that would otherwise go
      unproven — including the two that give requirement R2 a probe at all.
- [x] 8.4 `# requirement:` attribution plus closed coverage checking in both
      directions, so a requirement cannot silently lose its probe.
- [x] 8.5 Red-proof harness (`evidence/red-proof.py`) and its recorded output:
      all nineteen finding codes load-bearing.
- [x] 8.6 `traceability.yaml` — one row per ratified requirement with its
      artifact, its enforcing check, its positive, its probe, and its red proof.

## Phase 9 — promotion bookkeeping (change tasks 3.1, 3.2)

- [x] 9.1 Move `ideation/staging/identity-brokering-plane/` into
      `openspec/changes/add-identity-brokering/supporting-docs/` with the
      canonical tool, and confirm the emptied staging folder is gone.
- [x] 9.2 The support manifest: original staging path, source revision,
      transition date, per-file hashes, and the repeated origin values verified
      against `.openspec.yaml`. Promoted prose carries `Status: draft` and
      `Proposed by: add-identity-brokering`. Filename finding recorded in
      `research.md`.

## Phase 10 — the green bar

- [x] 10.1 `python3 scripts/validate-identity-brokering.py . --strict` — 0
      errors, 0 warnings.
- [x] 10.2 `OPENSPEC_TELEMETRY=0 openspec validate add-identity-brokering
      --strict` and `--all --strict` green.
- [x] 10.3 `python3 scripts/validate-ideation-cross-reference.py` — no new
      errors.
- [x] 10.4 `python3 scripts/proposal-support.py . verify add-identity-brokering`
      — ok.
- [x] 10.5 doc-health single-repo run — no finding against this change, its
      promoted supporting docs, the new contract family or the new validator.
- [x] 10.6 Tick the change's own tasks 1.1–1.10, 3.1 and 3.2 with a DONE note
      each.
- [ ] 10.7 Registration at the next additive bundle cut (change task 1.11) and
      the staging-index bookkeeping (change tasks 3.3–3.6) — NOT this feature's
      surface; executed by the change's landing sequence.
