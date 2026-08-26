# Proposal (draft): add-domain-hermes-roles-and-policies

Status: draft
Draft slice of: ../codexfactory-domain-hermes-content.md
Target repo at promotion: codexFactory `openspec/changes/add-domain-hermes-roles-and-policies/`
code_surface: codexFactory (hermes/domain/ + omnigent/domain-overlay.yaml — governed content, no runtime code)

## Why

The three-layer Hermes runtime can now seed a domain overlay read-only
(hermes-install `layer-content-seeding`, realized 2026-07-22), and the next
runtime increment — materializing the enforceable slice — is **content-starved**:
codexFactory ships a 32-line structural `overlay.yaml` and nothing else. The
domain's actual expertise (who decides, what positions the domain stakes) is
scattered across prose docs and the Omnigent overlay. This change authors the
first half of the Domain Hermes content: the Plane-1 persona roster and the
stored policy delta, with the Omnigent overlay extended in lockstep so the
seed-time closure check can hold.

## What Changes

- **`hermes/domain/roles/*.yaml` — the eight Plane-1 personas** from the
  ratified roster draft (LA, LE, LC, LQ, LS, LI, SC, LR): authority blocks
  (owns/decides/escalates with the 2026-07-22 escalation-target audit
  applied), trait vocabulary v1 (4 disposition + 5 voice axes, 3-level scale),
  per-axis `client_tunable` ranges, `directs_workers`, `deliberation_mix`
  references (two-tier councils), authored prose frames for the three
  flagships, and the `character_never_overrides_authority` guardrail
  (decide-then-speak).
- **`hermes/domain/policies/` — the stored delta**, per the policy model:
  the eight-category position table as policy files (branching/change model,
  review requirement, required checks + coverage ratchet, change
  size/reversibility, security must-nots, traceability, stack standards,
  authority/escalation), with contested positions carrying the
  `rationale`/`alternatives_rejected`/`staked_at`/`review_by` schema.
- **`hermes/domain/overlay.yaml` — extend `codex_owns`** to close the
  authority-closure matrix (system_architecture, security_posture,
  fail_closed_defaults, quality_gates, review_standards, release_readiness,
  versioning, cadence, flow_and_wip_health) so persona authority never claims
  scope the overlay doesn't stake.
- **`omnigent/domain-overlay.yaml` — lockstep extension:** add the two
  referenced-but-missing worker classes (`scrum_master_worker`,
  `release_note_agent`, minimal permissions) and the upward
  `directed_by` persona references (bidirectional refs, seed-checked).
- **Not in this change (change B):** `review-councils/`, `agent-mixes.yaml`,
  `escalation-rules.yaml`, `memory-boundaries.yaml`, the practice catalog.

## Impact

- Content-only: YAML + prose under `hermes/domain/` and `omnigent/`; no
  runtime code. Validated by codexFactory's doc/validator pass.
- Unblocks: hermes-install seeding increment 2 (real enforceable fields to
  materialize) and the openxFactory neutral `hermes_domain_overlay` schema
  (a real, full instance to validate against).
- Risk: the personas' enforceable authority blocks become governed content —
  the escalation-audit corrections must be applied at authoring time, not
  copied from the brainstorm YAML as-is.

## Open questions (to resolve in design)

- File naming: one YAML per persona (`roles/lead-architect.yaml`) — assumed.
- Whether `codex_owns` extension entries need scenario coverage in
  codexFactory's own spec set.
- Minimal permission set for the two new worker classes.
