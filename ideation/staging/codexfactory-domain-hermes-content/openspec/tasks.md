# Tasks (draft): add-domain-hermes-roles-and-policies

Status: draft
Draft slice of: ../codexfactory-domain-hermes-content.md

## 1. Roles

- [ ] 1.1 Author `hermes/domain/roles/*.yaml` — eight personas from
      `codexfactory-domain-roster-draft.md`, applying the escalation-target
      audit table (NOT the drafts' original `escalates.to` values).
- [ ] 1.2 Conform every trait value to vocabulary v1 (3-level scale); declare
      per-axis `client_tunable` ranges; flagship prose frames for LA/LQ/LS.
- [ ] 1.3 Set `deliberation_mix` to the two-tier council model
      (`council_small` default; `council_large` triggers named but defined in
      change B's `agent-mixes.yaml`).

## 2. Policies

- [ ] 2.1 Author `hermes/domain/policies/` from the policy-model position
      table — one file per category; store-the-delta filter applied (no
      textbook).
- [ ] 2.2 Contested positions carry `rationale`, `alternatives_rejected`,
      `staked_at`, `staked_by`, `review_by`; coverage expressed as the ratchet
      (no absolute floor).

## 3. Lockstep overlays

- [ ] 3.1 Extend `hermes/domain/overlay.yaml` `codex_owns` per the
      authority-closure matrix; verify closure both directions.
- [ ] 3.2 Add `scrum_master_worker` + `release_note_agent` to
      `omnigent/domain-overlay.yaml` (minimal permissions) with `directed_by`
      upward references; add `directed_by` to the existing nine classes per
      the worker-coverage table.

## 4. Validate & close out

- [ ] 4.1 codexFactory validator pass green (`scripts/validate-docs.sh`).
- [ ] 4.2 Cross-check: every persona `directs_workers` entry exists in the
      Omnigent overlay and vice versa (the bidirectional pair the seeder will
      check).
- [ ] 4.3 README doc-index links; brainstorm sources marked per lifecycle at
      promotion.
