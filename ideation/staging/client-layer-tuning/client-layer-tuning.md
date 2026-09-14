# Staged: Client Layer Tuning (scaffold roles, content schemas, validators, wizard)

Status: superseded
Superseded by: openspec/changes/archive/2026-07-24-add-client-layer-tuning-contracts (openxFactory), [codexFactory 2026-07-24-add-client-layer-defaults](https://github.com/opensoft/codexFactory/tree/main/openspec/changes/archive/2026-07-24-add-client-layer-defaults), and [hermes-install 2026-07-24-add-client-tuning-and-seeding](https://github.com/opensoft/xFactory-Hermes-Install/tree/main/openspec/changes/archive/2026-07-24-add-client-tuning-and-seeding)
Kind: architecture
Summary: Make the Client ("Company Policy") layer tunable: extend the neutral
scaffold with the house-team `roles/` (11 personas incl. the new Finance &
Accounting Officer) and the `cost_reporting_steward` worker; ship the client
content schemas + the shared `validate-client-content` check implementing the
stricter-only comparability spec; and build the policy wizard (avatar-assisted
first, CLI on the same elicitation schema) whose ratified output commits as a
per-client overlay that seeds through the standard pipeline.
Topics: client-hermes, company-policy, house-team, policy-wizard,
auto-clear-envelope, stricter-only, validators, finance-accounting-officer,
park-map, layer-content-seeding
Repository context: openxFactory (scaffold + schemas + validator) + codexFactory hermes/client/ (domain defaults) + installs/hermes-install (wizard verb)
Staging ID: openxFactory:staging:client-layer-tuning
Source: ideation/brainstorm/ — client-layer-scaffold.md, client-layer-roster-draft.md,
client-layer-content-draft.md, client-policy-wizard.md; decisions recorded
2026-07-22; risk/legal details in client-risk-and-assurance-model.md and
hermes-legal-compliance-model.md (still brainstorm).

## Outcome (recorded 2026-08-28)

COMPLETE. All three exit changes were ratified, realized and ARCHIVED on
2026-07-24, and each archive was verified at its own tree on 2026-08-28:

| Exit | Repository | Archived packet |
| --- | --- | --- |
| 2a scaffold + content schemas + validator | openxFactory | `openspec/changes/archive/2026-07-24-add-client-layer-tuning-contracts` (canonical spec `client-layer-tuning`, `contract-v1.17`) |
| 2b domain client defaults | codexFactory | `openspec/changes/archive/2026-07-24-add-client-layer-defaults` |
| 2c policy wizard + unified client seeding | xFactory-Hermes-Install | `openspec/changes/archive/2026-07-24-add-client-tuning-and-seeding` |

The opensoft tenant is tuned and seeded live. The topic folder and its
drafts are retained as PROVENANCE — the reason this document is
`superseded` rather than deleted — and the open questions listed below
were carried into those proposals and answered there; they are read here
as the record of what the topic asked, never as live work.

## Claims (decided 2026-07-22)

1. **Shape settled.** `roles/` joins the client shape (prescribed model doc to
   be updated alongside the `customer/` → `subject/` rename); the liaison is a
   convened capability, not a member; Plane 1 = 10 deciders + 1 capability;
   the scaffold's steward count corrects to 19 (+1 new below).
2. **Roster settled.** House team under the shared house style with a decided
   voice floor (respect + discretion locked, warmth ≥ moderate, ranges
   elsewhere); trait values conform to vocabulary v1; **Finance & Accounting
   Officer added** (owns cost reporting, budget envelopes, and the tracking
   granularity the subject layer must honor) + a new `cost_reporting_steward`
   worker; CSC/domain-Lead-Security conjunction rule.
3. **Content rules settled.** The facts rule (domain-default vs. wizard-only);
   stricter-only enforced mechanically per the comparability spec with review
   fallback; customer-memory seam confirmed (operator's view vs. subject's
   view, never merged).
4. **Wizard settled.** Avatar-assisted first, CLI drives the same elicitation
   schema; the auto-clear envelope is always human-ratified (per-unit
   envelopes allowed, per-client default); every run emits the park-map
   (manual-surface report); the final step packages the tuned tree as a
   per-client overlay, committed and digest-pinned, seeding through the
   standard pipeline.

## Exit path

- **openxFactory change — client scaffold + content contracts:** scaffold
  `roles/` (11 personas, house style with floor), `cost_reporting_steward`,
  the content schemas (`client_policy_overrides`, `client_memory_boundaries`,
  `client_integration_boundaries`, wizard output kinds) and
  `validate-client-content` implementing the comparability spec.
- **codexFactory change — `hermes/client/` domain defaults:** engineering-org
  specialization (`role-overrides`, `policy-overrides` defaults per the facts
  rule, `memory-boundaries`, `integration-boundaries`). After the neutral
  change.
- **hermes-install change — the wizard verb:** elicitation schema, envelope
  drafting + ratification gate, park-map evidence, overlay packaging + pin.
  The avatar-led surface arrives with the avatar staging topics; the schema
  and CLI do not wait for it.

## Idea notes (pre-document, non-documented)

None recorded at staging.

## Conflicts

No conflicts recorded.

## Open questions (carried to the proposals)

- Which repo hosts the shared validator implementation (openxFactory scripts,
  as usual?).
- Wizard overlay signing: who signs the per-client overlay's digest pin and
  where it is recorded (shared with the materialization topic).
- Default aggressiveness of domain-shipped values (softened by
  ratify-before-auto-clear, but still a UX calibration).
- Reputation & Brand Steward's hands (only decider with no directed steward).
- FAO ↔ domain efficiency-audit seam (roll-up format without exposing
  client-private financials) — `cost-accountability-and-efficiency-model.md`.
- Avatar-flow prerequisites (which staging avatar capabilities the guided
  flow needs before it can lead).

## Readiness

Neutral scaffold/schema change is ready to iterate now. The wizard change is
gated on the schemas and shares the seeding pipeline with the materialization
topic; the avatar surface is gated on the avatar topics.
