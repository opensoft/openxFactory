# Tasks (draft): add-domain-hermes-councils-and-memory

Status: draft
Draft slice of: ../codexfactory-domain-hermes-content.md

## 0. Gate

- [ ] 0.1 Confirm the `add-omnigent-domain-overlay` codexFactory realization
      has landed (archetype-shaped `omnigent/domain-overlay.yaml`); carry
      forward `directed_by` on all 11 classes and archetype the two change-A
      workers if the realization has not already done so.

## 1. Agent mixes

- [ ] 1.1 Author `agent-mixes.yaml`: four profiles, the trigger→seats table
      for `council_small`, the enumerated `council_large` triggers, and the
      guardrails block (advisory-only, context packet, no standing
      credentials, Lead-accepted roster changes).
- [ ] 1.2 Wire `spend_over_envelope` to the client FAO budget-envelope
      reference (domain declares the trigger only; un-tuned client parks).

## 2. Review councils

- [ ] 2.1 Author `review-councils/merge-readiness.yaml` (per-PR; LQ/LS/LI).
- [ ] 2.2 Author `review-councils/gate-rules.yaml`: domain seats LA/LS/LQ,
      client seat company-policy-lead (+ CSC conjunction pull-in), project
      seat = intent-owner role-slot (symbolic), human acknowledgement step,
      Merge Master envelope as the enforcement artifact.
- [ ] 2.3 Encode failure semantics: split → park for liaison; missing
      required seat → REFUSED; council output is a recommendation the
      convener must accept or reject on the record.

## 3. Escalation rules

- [ ] 3.1 Author `escalation-rules.yaml` elevating routing + stop conditions
      from the archetype-shaped overlay onto persona ids; flag cross-layer
      targets; add `credential_required_not_held`; `on_stop: park_fail_closed`.
- [ ] 3.2 Verify consistency with the personas' own `escalates` blocks
      (change A applied the escalation-target audit — no drift).

## 4. Memory boundaries + practice catalog

- [ ] 4.1 Author `memory-boundaries.yaml` (gateway vocabulary,
      worker-proposes/Lead-accepts, de-id contract, seeded `finding_class`
      starter vocabulary).
- [ ] 4.2 Author `practice-catalog.yaml` (four profiles, `promoted_in` +
      `owning_lead`, proportional signing note).

## 5. Validate & close out

- [ ] 5.1 `openspec validate add-domain-hermes-councils-and-memory --strict`
      and `scripts/validate-docs.sh` green.
- [ ] 5.2 README doc-index + OpenSpec Records updates; staging INDEX row
      updated in openxFactory.
