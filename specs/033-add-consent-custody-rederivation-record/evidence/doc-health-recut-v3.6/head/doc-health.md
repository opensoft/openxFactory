# Doc-Health Report — 2026-09-09

Status: record
Kind: report
Repo-Identity: openxFactory

## Headline

Canon share by words: 39.7% (360528 canon words / 908284 governance words, promoted specs included).
Findings: 10 critical, 6 error, 57 warning, 13 info. New regressions vs previous report: 0.

Non-default configuration (cross-run comparisons must account for this):
- scope limited to single repo openxFactory

Skipped families (never silently omitted):
- `client-identity-composition` — single-repo run: no aggregation checkout
- `notebook-projection-drift` — nlm unauthenticated or sync unavailable; family runs in operator-triggered runs only
- `submodule-pin-drift` — single-repo run: no aggregation checkout

## Per-Stage Counts

| Status | Docs | Words |
| --- | --- | --- |
| brainstorm | 185 | 154065 |
| draft | 70 | 152043 |
| projection | 1 | 37693 |
| ratified | 33 | 82996 |
| record | 29 | 38680 |
| retired | 1 | 1273 |
| staged | 66 | 153828 |
| standard | 6 | 17057 |
| superseded | 5 | 10174 |
| (promoted specs) | — | 260475 |

## Preflight

- ok: openxFactory `python3 scripts/validate-avatar-first-ui.py` — OK xFactory avatar-first UI standard surface [mode=baseline]
- ok: openxFactory `python3 scripts/validate-installation-templates.py` — OK xFactory installation templates
- ok: openxFactory `python3 scripts/validate-intake-templates.py` — OK xFactory intake templates
- ok: openxFactory `python3 scripts/validate-memory-gateway.py` — OK xFactory Memory Gateway contracts, examples, fixtures, and runtime smoke

## Findings By Family

### status-validity

- [error] openxFactory:openspec/changes/adopt-codexfactory-repository-identity/proposal.md — missing status header
- [error] openxFactory:openspec/changes/disposition-codexfactory-declared-renames/review/ratification-2026-09-05.md — missing status header

### staged-topic-template

- [warning] openxFactory:ideation/staging/agent-wallet-identity/agent-wallet-identity.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/avatar-pilot-hardening/avatar-pilot-hardening.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/client-credential-escrow-registry/client-credential-escrow-registry.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/client-layer-tuning/client-layer-tuning.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/context-compression-runtime/context-compression-runtime.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/dashboard-project-scoping/dashboard-project-scoping.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/dashboard-repo-selector/dashboard-repo-selector.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/github-administration-plane/multi-app-identity-and-github-administration.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/hermes-stack-topology-per-client/hermes-stack-topology-per-client.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/ideation-action-plane/ideation-action-plane.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/layer-content-materialization/layer-content-materialization.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/layer-vocabulary-machine-migration/layer-vocabulary-machine-migration.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/manager-review-approval-scope-kind/manager-review-approval-scope-kind.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/mobile-dashboard-surface/mobile-dashboard-surface.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/openxdox-install-app-provisioning/openxdox-install-app-provisioning.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/proposal-origin-contract/fda-samd-traceability-rationale.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section; no open questions section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/recurrence-crystallization/recurrence-crystallization.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/session-notebook-reconciliation/session-notebook-reconciliation.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/tier2-council-clearance-pattern/tier2-council-clearance-pattern.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/workbench-branch-sessions/workbench-branch-sessions.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/worker-host-app/worker-host-app.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked
- [warning] openxFactory:ideation/staging/workstation-app-shell/workstation-app-shell.md — primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked

### standard-backing

No findings.

### ratified-provenance

- [critical] openxFactory:openspec/changes/add-sequenced-after-substrate/proposal.md — Ratified by: missing or does not resolve to an OpenSpec change
- [critical] openxFactory:openspec/changes/add-structured-scope-substrate/proposal.md — ratified header carries no citation in either sanctioned spelling
- [critical] openxFactory:openspec/changes/adopt-configured-notebook-hosting-identity/proposal.md — Ratified: names none of an approver, a date, or a resolvable record path
- [critical] openxFactory:openspec/changes/archive/2026-09-05-mirror-floor-addition-grace/proposal.md — ratified header carries no citation in either sanctioned spelling
- [critical] openxFactory:openspec/changes/archive/2026-09-05-mirror-floor-addition-grace/review/ratification-2026-09-05.md — ratified header carries no citation in either sanctioned spelling
- [critical] openxFactory:openspec/changes/mirror-floor-regeneration-automation/proposal.md — ratified header carries no citation in either sanctioned spelling

### succession-integrity

No findings.

### location-conformance

No findings.

### record-immutability

- [critical] openxFactory:docs/archive-record-discrepancies.md — record document changed after capture
- [critical] openxFactory:docs/domain-ontology-adoption-handoff.md — record document changed after capture
- [critical] openxFactory:docs/domain-ontology-pilot-report.md — record document changed after capture
- [critical] openxFactory:docs/notebook-projection-migration-evidence-2026-08-24.md — record document changed after capture

### staged-candidate-aging

- [warning] openxFactory:docs/deploy-artifacts-plan.md — draft without transition for 63 days
- [warning] openxFactory:docs/domain-stack-pin-implementation-plan.md — draft without transition for 63 days
- [warning] openxFactory:docs/factory-taxonomy-model.md — draft without transition for 63 days
- [warning] openxFactory:docs/intake-and-installer-plan.md — draft without transition for 63 days
- [warning] openxFactory:docs/runtime-services-plan.md — draft without transition for 63 days
- [warning] openxFactory:docs/self-hosted-runtime-binding-plan.md — draft without transition for 63 days
- [warning] openxFactory:docs/tui-spec-questionnaire.md — draft without transition for 63 days
- [warning] openxFactory:docs/workflow-gap-solutions.md — draft without transition for 62 days
- [warning] openxFactory:examples/README.md — draft without transition for 62 days
- [warning] openxFactory:examples/memory-gateway/README.md — draft without transition for 62 days
- [warning] openxFactory:examples/pre-run-simulations/README.md — draft without transition for 62 days
- [warning] openxFactory:ideation/staging/agent-wallet-identity — staged topic untouched 34 days
- [warning] openxFactory:ideation/staging/client-credential-escrow-registry — staged topic untouched 52 days
- [warning] openxFactory:ideation/staging/dashboard-project-scoping — staged topic untouched 33 days
- [warning] openxFactory:ideation/staging/manager-review-approval-scope-kind — staged topic untouched 30 days
- [warning] openxFactory:ideation/staging/recurrence-crystallization — staged topic untouched 38 days
- [warning] openxFactory:ideation/staging/session-notebook-reconciliation — staged topic untouched 30 days
- [warning] openxFactory:ideation/staging/tier2-council-clearance-pattern — staged topic untouched 33 days
- [warning] openxFactory:ideation/staging/workbench-branch-sessions — staged topic untouched 33 days
- [warning] openxFactory:templates/installation/README.md — draft without transition for 63 days
- [warning] openxFactory:templates/intake/README.md — draft without transition for 63 days
- [warning] openxFactory:templates/intake/subtypes/README.md — draft without transition for 63 days
- [warning] openxFactory:templates/ui/README.md — draft without transition for 63 days
- [info] openxFactory:(drafts) — draft age distribution days: min=0 max=63 n=70

### register-lifecycle-consistency

- [warning] openxFactory:docs/domain-neutralization-candidate-register.md — DTN-002: adopted without resolvable artifact
- [warning] openxFactory:docs/domain-neutralization-candidate-register.md — DTN-003: adopted without resolvable artifact
- [warning] openxFactory:docs/domain-neutralization-candidate-register.md — DTN-004: adopted without resolvable artifact
- [warning] openxFactory:docs/domain-neutralization-candidate-register.md — DTN-013: adopted without resolvable artifact
- [warning] openxFactory:docs/domain-neutralization-candidate-register.md — DTN-016: adopted without resolvable artifact
- [warning] openxFactory:docs/domain-neutralization-candidate-register.md — DTN-018: adopted without resolvable artifact
- [warning] openxFactory:docs/domain-neutralization-candidate-register.md — DTN-019: adopted without resolvable artifact
- [warning] openxFactory:docs/domain-neutralization-candidate-register.md — DTN-021: adopted without resolvable artifact
- [warning] openxFactory:docs/domain-neutralization-candidate-register.md — DTN-022: adopted without resolvable artifact
- [warning] openxFactory:docs/domain-neutralization-candidate-register.md — DTN-026: adopted without resolvable artifact

### tag-hygiene

- [error] openxFactory:ideation/staging/notebook-access-wallet-governance/notebook-access-wallet-governance.md — unresolved target=openxwallet at line 107
- [error] openxFactory:ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md — unresolved target=openxwallet at line 222
- [error] openxFactory:ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md — unresolved target=openxwallet at line 242
- [error] openxFactory:ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md — unresolved target=openxwallet at line 280

### submodule-pin-drift

Skipped: single-repo run: no aggregation checkout

### contract-copy-drift

No findings.

### notebook-projection-drift

Skipped: nlm unauthenticated or sync unavailable; family runs in operator-triggered runs only

### document-catalog

- [info] (baseline):(progress) — [coverage] baseline coverage 0/0 entries (0.0%) across 0/0 repositories

### ideation-routing

- [warning] openxFactory:ideation/brainstorm/cross-domain/XFI-2026-002/routing.yaml — [aging] routing record in 'split' state untouched 34 days (latest transition; warning at 30, error at 90)
- [warning] openxFactory:ideation/brainstorm/inbox/XFI-2026-001/routing.yaml — [aging] routing record in 'triaging' state untouched 34 days (latest transition; warning at 30, error at 90)
- [info] xFactory:xFactories/LedgerxFactory — [external-path] referenced pinned repository 'xFactories/LedgerxFactory' is not materialized; external-path resolution reported as skipped (nightly)

### proposal-origin

No findings.

### client-identity-composition

Skipped: single-repo run: no aggregation checkout

### promotion-fidelity

Basis: the pinned checkout — the same tree every other family measures.

No findings.

### release-inventory-drift

No findings.

### duplicate-packet

No findings.

### family-enumeration

No findings.

### modified-block-currency

Finding classes, counted apart so the gate-bearing arm is never read as one of the editorial rows:
- scenario-title completeness: 0 (`error` — the arm carrying this family's gate)
- carriage ledger: 9 (`info` — editorial, and the arm says so in every finding)
- title resolution and ordering: 0 (`warning`)
- marker defects: 0 (`info`)
- sibling-pairing declaration: 0 (`warning`)
- added-over-canon collision: 0 (`warning`)
- unplaced-finding drift: 0 (`warning`)

- [info] openxFactory:openspec/changes/add-chain-attestation/specs/signed-execution-chain/spec.md — active MODIFIED block for 'A gate validates the short chain as a hash-linked chain' does not carry 9 of the 58 body units and scenario bullets openspec/specs/signed-execution-chain/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [body] 'openxFactory SHALL operate, FROM THIS TRANCHE, a gate that validates links 1–3 before permitting the terminal act, and SHALL validate them a…'; [body] '**At this tranche continuity is therefore established BY DERIVATION AND COMPARISON, not by a third signature**, and the gate SHALL validate…'; [body] '**THE LIST IS CLOSED, AND CLOSING IT IS ITSELF AN OBLIGATION.** Because the gate validates EXACTLY these checks before the terminal act, **e…'; [body] '| Requirement | Where it is enforced | | --- | --- | | Presentation proven by possession, bound to this ratification, standing current at ex…'; [body] "The gate's scope at this tranche is links 1–3 and it SHALL NOT report the absence of a later tranche's link as a break, because a gate canno…"; [bullet] 'WHEN any of links 1–3 is absent'; [bullet] 'WHEN the gate walks a chain that carries no attestation link'; [bullet] 'THEN it validates links 1–3 and returns a verdict scoped to them'; [bullet] 'AND the absent later link is not reported as a break'
- [info] openxFactory:openspec/changes/add-composed-view-authoring/specs/ideation-dashboard/spec.md — active MODIFIED block for 'Composed views are read-only with a repository jump' does not carry 2 of the 6 body units and scenario bullets openspec/specs/ideation-dashboard/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [body] 'On a composed snapshot every gate-bearing affordance SHALL hide — a gate verb binds to one served checkout, and a composed view has none — a…'; [bullet] 'THEN no gate-bearing affordance renders anywhere in the view'
- [info] openxFactory:openspec/changes/add-credential-escrow-checkout/specs/credential-contracts/spec.md — active MODIFIED block for 'Canonical credential record shapes' does not carry 3 of the 20 body units and scenario bullets openspec/specs/credential-contracts/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [body] 'Credential contract records SHALL validate against the canonical `contracts/schemas/xfactory-credential-contracts.schema.yaml`, which owns t…'; [bullet] '**WHEN** a DomainxFactory adds or edits a file under `credentials/` carrying one of the five kinds'; [bullet] '**WHEN** a credentials file carries a kind outside the five contract kinds'
- [info] openxFactory:openspec/changes/add-doxchat-model-intake/specs/ideation-dashboard/spec.md — active MODIFIED block for 'doxBench model catalog and provider boundary' does not carry 1 of the 38 body units and scenario bullets openspec/specs/ideation-dashboard/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [bullet] '**THEN** the selector MUST show exactly the available catalog entries and their data-handling badges'
- [info] openxFactory:openspec/changes/adopt-configured-notebook-hosting-identity/specs/lifecycle-notebook-projection/spec.md — active MODIFIED block for "The projection's hosting identity is declared at install" does not carry 1 of the 23 body units and scenario bullets openspec/specs/lifecycle-notebook-projection/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [bullet] "**AND** Opensoft's own install is such a declaration, naming `xFactor001@opensoft.one`"
- [info] openxFactory:openspec/changes/declare-client-standing-policy-contract/specs/client-layer-tuning/spec.md — active MODIFIED block for 'Client content shapes are contract-validated' does not carry 1 of the 5 body units and scenario bullets openspec/specs/client-layer-tuning/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [bullet] '**THEN** every packaged example passes and every negative fails for its declared reason'
- [info] openxFactory:openspec/changes/qualify-avatar-live-voice/specs/avatar-client-lab/spec.md — active MODIFIED block for 'Repository and ownership boundary' does not carry 1 of the 5 body units and scenario bullets openspec/specs/avatar-client-lab/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [body] 'The Flutter avatar client application and its generated Dart bindings SHALL live in codexFactory under `apps/avatar-client-lab/`, while open…'
- [info] openxFactory:openspec/changes/qualify-avatar-live-voice/specs/avatar-client-runtime/spec.md — active MODIFIED block for 'Redacted telemetry and latency evidence' does not carry 1 of the 6 body units and scenario bullets openspec/specs/avatar-client-runtime/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [body] 'Latency evidence in this kernel SHALL be structured logging with monotonic timestamps for broker setup, sideband attach, media connected, an…'
- [info] openxFactory:openspec/changes/qualify-avatar-live-voice/specs/avatar-client-runtime/spec.md — active MODIFIED block for 'Versioned neutral avatar-client contract kernel' does not carry 1 of the 17 body units and scenario bullets openspec/specs/avatar-client-runtime/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [body] 'AVC-03 and AVC-05 are absorbed as described; AVC-09 and AVC-10 remain reserved for the live-qualification successor change and their identif…'

### release-tag-publication

- [info] openxFactory:contracts/releases/contract-v2.6.digests.yaml — contract-v2.6 is declared SPENT: it was cut, has no published annotated tag, and contract-v3.0 — itself cut, itself published and strictly later — superseded it. The record is contracts/CHANGELOG.md § contract-v3.0 — RULED BY Brett Heap, 2026-09-02; MEASUREMENT: PR #565 comment `5502452624`. The tag obligation was not met, it was EXTINGUISHED by an owner act at the cost of a version number

### semantic-normative-prose

No findings.

### semantic-contradiction

No findings.

### preflight

No findings.

## Ranked Plan

- severity=critical family=ratified-provenance repo=openxFactory path=openspec/changes/add-sequenced-after-substrate/proposal.md rule="Ratified by: missing or does not resolve to an OpenSpec change" action="point Ratified by: at an existing active or archived change" class="auto-fixable"
- severity=critical family=ratified-provenance repo=openxFactory path=openspec/changes/add-structured-scope-substrate/proposal.md rule="ratified header carries no citation in either sanctioned spelling" action="add Ratified by: <change> where an approving OpenSpec change exists, otherwise Ratified: naming an approver, a date, or a resolvable record path" class="auto-fixable"
- severity=critical family=ratified-provenance repo=openxFactory path=openspec/changes/adopt-configured-notebook-hosting-identity/proposal.md rule="Ratified: names none of an approver, a date, or a resolvable record path" action="name at least one of an approver, a date, or a resolvable record path — or cite the approving change with Ratified by: if one exists" class="auto-fixable"
- severity=critical family=ratified-provenance repo=openxFactory path=openspec/changes/archive/2026-09-05-mirror-floor-addition-grace/proposal.md rule="ratified header carries no citation in either sanctioned spelling" action="add Ratified by: <change> where an approving OpenSpec change exists, otherwise Ratified: naming an approver, a date, or a resolvable record path" class="auto-fixable"
- severity=critical family=ratified-provenance repo=openxFactory path=openspec/changes/archive/2026-09-05-mirror-floor-addition-grace/review/ratification-2026-09-05.md rule="ratified header carries no citation in either sanctioned spelling" action="add Ratified by: <change> where an approving OpenSpec change exists, otherwise Ratified: naming an approver, a date, or a resolvable record path" class="auto-fixable"
- severity=critical family=ratified-provenance repo=openxFactory path=openspec/changes/mirror-floor-regeneration-automation/proposal.md rule="ratified header carries no citation in either sanctioned spelling" action="add Ratified by: <change> where an approving OpenSpec change exists, otherwise Ratified: naming an approver, a date, or a resolvable record path" class="auto-fixable"
- severity=critical family=record-immutability repo=openxFactory path=docs/archive-record-discrepancies.md rule="record document changed after capture" action="revert the content edit or re-issue as a new record" class="contested"
- severity=critical family=record-immutability repo=openxFactory path=docs/domain-ontology-adoption-handoff.md rule="record document changed after capture" action="revert the content edit or re-issue as a new record" class="contested"
- severity=critical family=record-immutability repo=openxFactory path=docs/domain-ontology-pilot-report.md rule="record document changed after capture" action="revert the content edit or re-issue as a new record" class="contested"
- severity=critical family=record-immutability repo=openxFactory path=docs/notebook-projection-migration-evidence-2026-08-24.md rule="record document changed after capture" action="revert the content edit or re-issue as a new record" class="contested"
- severity=error family=status-validity repo=openxFactory path=openspec/changes/adopt-codexfactory-repository-identity/proposal.md rule="missing status header" action="add a Status: header from the controlled taxonomy" class="auto-fixable"
- severity=error family=status-validity repo=openxFactory path=openspec/changes/disposition-codexfactory-declared-renames/review/ratification-2026-09-05.md rule="missing status header" action="add a Status: header from the controlled taxonomy" class="auto-fixable"
- severity=error family=tag-hygiene repo=openxFactory path=ideation/staging/notebook-access-wallet-governance/notebook-access-wallet-governance.md rule="unresolved target=openxwallet at line 107" action="name a capability under openspec/specs/ or an active change (document-lifecycle grammar)" class="auto-fixable"
- severity=error family=tag-hygiene repo=openxFactory path=ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md rule="unresolved target=openxwallet at line 222" action="name a capability under openspec/specs/ or an active change (document-lifecycle grammar)" class="auto-fixable"
- severity=error family=tag-hygiene repo=openxFactory path=ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md rule="unresolved target=openxwallet at line 242" action="name a capability under openspec/specs/ or an active change (document-lifecycle grammar)" class="auto-fixable"
- severity=error family=tag-hygiene repo=openxFactory path=ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md rule="unresolved target=openxwallet at line 280" action="name a capability under openspec/specs/ or an active change (document-lifecycle grammar)" class="auto-fixable"
- severity=warning family=ideation-routing repo=openxFactory path=ideation/brainstorm/cross-domain/XFI-2026-002/routing.yaml rule="[aging] routing record in 'split' state untouched 34 days (latest transition; warning at 30, error at 90)" action="progress the routing record or record an explicit deferral" class="contested"
- severity=warning family=ideation-routing repo=openxFactory path=ideation/brainstorm/inbox/XFI-2026-001/routing.yaml rule="[aging] routing record in 'triaging' state untouched 34 days (latest transition; warning at 30, error at 90)" action="progress the routing record or record an explicit deferral" class="contested"
- severity=warning family=register-lifecycle-consistency repo=openxFactory path=docs/domain-neutralization-candidate-register.md rule="DTN-002: adopted without resolvable artifact" action="point the adopted entry at its promoted artifact" class="contested"
- severity=warning family=register-lifecycle-consistency repo=openxFactory path=docs/domain-neutralization-candidate-register.md rule="DTN-003: adopted without resolvable artifact" action="point the adopted entry at its promoted artifact" class="contested"
- severity=warning family=register-lifecycle-consistency repo=openxFactory path=docs/domain-neutralization-candidate-register.md rule="DTN-004: adopted without resolvable artifact" action="point the adopted entry at its promoted artifact" class="contested"
- severity=warning family=register-lifecycle-consistency repo=openxFactory path=docs/domain-neutralization-candidate-register.md rule="DTN-013: adopted without resolvable artifact" action="point the adopted entry at its promoted artifact" class="contested"
- severity=warning family=register-lifecycle-consistency repo=openxFactory path=docs/domain-neutralization-candidate-register.md rule="DTN-016: adopted without resolvable artifact" action="point the adopted entry at its promoted artifact" class="contested"
- severity=warning family=register-lifecycle-consistency repo=openxFactory path=docs/domain-neutralization-candidate-register.md rule="DTN-018: adopted without resolvable artifact" action="point the adopted entry at its promoted artifact" class="contested"
- severity=warning family=register-lifecycle-consistency repo=openxFactory path=docs/domain-neutralization-candidate-register.md rule="DTN-019: adopted without resolvable artifact" action="point the adopted entry at its promoted artifact" class="contested"
- severity=warning family=register-lifecycle-consistency repo=openxFactory path=docs/domain-neutralization-candidate-register.md rule="DTN-021: adopted without resolvable artifact" action="point the adopted entry at its promoted artifact" class="contested"
- severity=warning family=register-lifecycle-consistency repo=openxFactory path=docs/domain-neutralization-candidate-register.md rule="DTN-022: adopted without resolvable artifact" action="point the adopted entry at its promoted artifact" class="contested"
- severity=warning family=register-lifecycle-consistency repo=openxFactory path=docs/domain-neutralization-candidate-register.md rule="DTN-026: adopted without resolvable artifact" action="point the adopted entry at its promoted artifact" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=docs/deploy-artifacts-plan.md rule="draft without transition for 63 days" action="ratify, supersede, or retire the draft" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=docs/domain-stack-pin-implementation-plan.md rule="draft without transition for 63 days" action="ratify, supersede, or retire the draft" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=docs/factory-taxonomy-model.md rule="draft without transition for 63 days" action="ratify, supersede, or retire the draft" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=docs/intake-and-installer-plan.md rule="draft without transition for 63 days" action="ratify, supersede, or retire the draft" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=docs/runtime-services-plan.md rule="draft without transition for 63 days" action="ratify, supersede, or retire the draft" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=docs/self-hosted-runtime-binding-plan.md rule="draft without transition for 63 days" action="ratify, supersede, or retire the draft" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=docs/tui-spec-questionnaire.md rule="draft without transition for 63 days" action="ratify, supersede, or retire the draft" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=docs/workflow-gap-solutions.md rule="draft without transition for 62 days" action="ratify, supersede, or retire the draft" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=examples/README.md rule="draft without transition for 62 days" action="ratify, supersede, or retire the draft" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=examples/memory-gateway/README.md rule="draft without transition for 62 days" action="ratify, supersede, or retire the draft" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=examples/pre-run-simulations/README.md rule="draft without transition for 62 days" action="ratify, supersede, or retire the draft" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=ideation/staging/agent-wallet-identity rule="staged topic untouched 34 days" action="progress the topic to a proposal, or record the outcome it already reached — the primary fragment superseded/retired, or an Exit taken: line naming the archived change" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=ideation/staging/client-credential-escrow-registry rule="staged topic untouched 52 days" action="progress the topic to a proposal, or record the outcome it already reached — the primary fragment superseded/retired, or an Exit taken: line naming the archived change" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=ideation/staging/dashboard-project-scoping rule="staged topic untouched 33 days" action="progress the topic to a proposal, or record the outcome it already reached — the primary fragment superseded/retired, or an Exit taken: line naming the archived change" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=ideation/staging/manager-review-approval-scope-kind rule="staged topic untouched 30 days" action="progress the topic to a proposal, or record the outcome it already reached — the primary fragment superseded/retired, or an Exit taken: line naming the archived change" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=ideation/staging/recurrence-crystallization rule="staged topic untouched 38 days" action="progress the topic to a proposal, or record the outcome it already reached — the primary fragment superseded/retired, or an Exit taken: line naming the archived change" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=ideation/staging/session-notebook-reconciliation rule="staged topic untouched 30 days" action="progress the topic to a proposal, or record the outcome it already reached — the primary fragment superseded/retired, or an Exit taken: line naming the archived change" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=ideation/staging/tier2-council-clearance-pattern rule="staged topic untouched 33 days" action="progress the topic to a proposal, or record the outcome it already reached — the primary fragment superseded/retired, or an Exit taken: line naming the archived change" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=ideation/staging/workbench-branch-sessions rule="staged topic untouched 33 days" action="progress the topic to a proposal, or record the outcome it already reached — the primary fragment superseded/retired, or an Exit taken: line naming the archived change" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=templates/installation/README.md rule="draft without transition for 63 days" action="ratify, supersede, or retire the draft" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=templates/intake/README.md rule="draft without transition for 63 days" action="ratify, supersede, or retire the draft" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=templates/intake/subtypes/README.md rule="draft without transition for 63 days" action="ratify, supersede, or retire the draft" class="contested"
- severity=warning family=staged-candidate-aging repo=openxFactory path=templates/ui/README.md rule="draft without transition for 63 days" action="ratify, supersede, or retire the draft" class="contested"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/agent-wallet-identity/agent-wallet-identity.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/avatar-pilot-hardening/avatar-pilot-hardening.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/client-credential-escrow-registry/client-credential-escrow-registry.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/client-layer-tuning/client-layer-tuning.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/context-compression-runtime/context-compression-runtime.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/dashboard-project-scoping/dashboard-project-scoping.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/dashboard-repo-selector/dashboard-repo-selector.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/github-administration-plane/multi-app-identity-and-github-administration.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/hermes-stack-topology-per-client/hermes-stack-topology-per-client.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/ideation-action-plane/ideation-action-plane.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/layer-content-materialization/layer-content-materialization.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/layer-vocabulary-machine-migration/layer-vocabulary-machine-migration.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/manager-review-approval-scope-kind/manager-review-approval-scope-kind.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/mobile-dashboard-surface/mobile-dashboard-surface.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/openxdox-install-app-provisioning/openxdox-install-app-provisioning.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/proposal-origin-contract/fda-samd-traceability-rationale.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section; no open questions section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/recurrence-crystallization/recurrence-crystallization.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/session-notebook-reconciliation/session-notebook-reconciliation.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/tier2-council-clearance-pattern/tier2-council-clearance-pattern.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/workbench-branch-sessions/workbench-branch-sessions.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/worker-host-app/worker-host-app.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=warning family=staged-topic-template repo=openxFactory path=ideation/staging/workstation-app-shell/workstation-app-shell.md rule="primary fragment does not meet the outline template (no pre-document idea notes section; no conflicts section) — staged before the template ratified, so conformance is opt-in — rewrite it when the topic is next worked" action="add the missing sections, or give every open question its Context / Recommended answer / Explanation / Disposition status sub-fields" class="auto-fixable"
- severity=info family=document-catalog repo=(baseline) path=(progress) rule="[coverage] baseline coverage 0/0 entries (0.0%) across 0/0 repositories" action="resume the sharded baseline build to enable complete-coverage enforcement" class="auto-fixable"
- severity=info family=ideation-routing repo=xFactory path=xFactories/LedgerxFactory rule="[external-path] referenced pinned repository 'xFactories/LedgerxFactory' is not materialized; external-path resolution reported as skipped (nightly)" action="materialize the repository to resolve referenced paths, or run the strict organize/proposal gate" class="auto-fixable"
- severity=info family=modified-block-currency repo=openxFactory path=openspec/changes/add-chain-attestation/specs/signed-execution-chain/spec.md rule="active MODIFIED block for 'A gate validates the short chain as a hash-linked chain' does not carry 9 of the 58 body units and scenario bullets openspec/specs/signed-execution-chain/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [body] 'openxFactory SHALL operate, FROM THIS TRANCHE, a gate that validates links 1–3 before permitting the terminal act, and SHALL validate them a…'; [body] '**At this tranche continuity is therefore established BY DERIVATION AND COMPARISON, not by a third signature**, and the gate SHALL validate…'; [body] '**THE LIST IS CLOSED, AND CLOSING IT IS ITSELF AN OBLIGATION.** Because the gate validates EXACTLY these checks before the terminal act, **e…'; [body] '| Requirement | Where it is enforced | | --- | --- | | Presentation proven by possession, bound to this ratification, standing current at ex…'; [body] \"The gate's scope at this tranche is links 1–3 and it SHALL NOT report the absence of a later tranche's link as a break, because a gate canno…\"; [bullet] 'WHEN any of links 1–3 is absent'; [bullet] 'WHEN the gate walks a chain that carries no attestation link'; [bullet] 'THEN it validates links 1–3 and returns a verdict scoped to them'; [bullet] 'AND the absent later link is not reported as a break'" action="restate the requirement as canon currently states it, or declare the deletion with a `Removed from canon by` marker" class="contested"
- severity=info family=modified-block-currency repo=openxFactory path=openspec/changes/add-composed-view-authoring/specs/ideation-dashboard/spec.md rule="active MODIFIED block for 'Composed views are read-only with a repository jump' does not carry 2 of the 6 body units and scenario bullets openspec/specs/ideation-dashboard/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [body] 'On a composed snapshot every gate-bearing affordance SHALL hide — a gate verb binds to one served checkout, and a composed view has none — a…'; [bullet] 'THEN no gate-bearing affordance renders anywhere in the view'" action="restate the requirement as canon currently states it, or declare the deletion with a `Removed from canon by` marker" class="contested"
- severity=info family=modified-block-currency repo=openxFactory path=openspec/changes/add-credential-escrow-checkout/specs/credential-contracts/spec.md rule="active MODIFIED block for 'Canonical credential record shapes' does not carry 3 of the 20 body units and scenario bullets openspec/specs/credential-contracts/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [body] 'Credential contract records SHALL validate against the canonical `contracts/schemas/xfactory-credential-contracts.schema.yaml`, which owns t…'; [bullet] '**WHEN** a DomainxFactory adds or edits a file under `credentials/` carrying one of the five kinds'; [bullet] '**WHEN** a credentials file carries a kind outside the five contract kinds'" action="restate the requirement as canon currently states it, or declare the deletion with a `Removed from canon by` marker" class="contested"
- severity=info family=modified-block-currency repo=openxFactory path=openspec/changes/add-doxchat-model-intake/specs/ideation-dashboard/spec.md rule="active MODIFIED block for 'doxBench model catalog and provider boundary' does not carry 1 of the 38 body units and scenario bullets openspec/specs/ideation-dashboard/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [bullet] '**THEN** the selector MUST show exactly the available catalog entries and their data-handling badges'" action="restate the requirement as canon currently states it, or declare the deletion with a `Removed from canon by` marker" class="contested"
- severity=info family=modified-block-currency repo=openxFactory path=openspec/changes/adopt-configured-notebook-hosting-identity/specs/lifecycle-notebook-projection/spec.md rule="active MODIFIED block for \"The projection's hosting identity is declared at install\" does not carry 1 of the 23 body units and scenario bullets openspec/specs/lifecycle-notebook-projection/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [bullet] \"**AND** Opensoft's own install is such a declaration, naming `xFactor001@opensoft.one`\"" action="restate the requirement as canon currently states it, or declare the deletion with a `Removed from canon by` marker" class="contested"
- severity=info family=modified-block-currency repo=openxFactory path=openspec/changes/declare-client-standing-policy-contract/specs/client-layer-tuning/spec.md rule="active MODIFIED block for 'Client content shapes are contract-validated' does not carry 1 of the 5 body units and scenario bullets openspec/specs/client-layer-tuning/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [bullet] '**THEN** every packaged example passes and every negative fails for its declared reason'" action="restate the requirement as canon currently states it, or declare the deletion with a `Removed from canon by` marker" class="contested"
- severity=info family=modified-block-currency repo=openxFactory path=openspec/changes/qualify-avatar-live-voice/specs/avatar-client-lab/spec.md rule="active MODIFIED block for 'Repository and ownership boundary' does not carry 1 of the 5 body units and scenario bullets openspec/specs/avatar-client-lab/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [body] 'The Flutter avatar client application and its generated Dart bindings SHALL live in codexFactory under `apps/avatar-client-lab/`, while open…'" action="restate the requirement as canon currently states it, or declare the deletion with a `Removed from canon by` marker" class="contested"
- severity=info family=modified-block-currency repo=openxFactory path=openspec/changes/qualify-avatar-live-voice/specs/avatar-client-runtime/spec.md rule="active MODIFIED block for 'Redacted telemetry and latency evidence' does not carry 1 of the 6 body units and scenario bullets openspec/specs/avatar-client-runtime/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [body] 'Latency evidence in this kernel SHALL be structured logging with monotonic timestamps for broker setup, sideband attach, media connected, an…'" action="restate the requirement as canon currently states it, or declare the deletion with a `Removed from canon by` marker" class="contested"
- severity=info family=modified-block-currency repo=openxFactory path=openspec/changes/qualify-avatar-live-voice/specs/avatar-client-runtime/spec.md rule="active MODIFIED block for 'Versioned neutral avatar-client contract kernel' does not carry 1 of the 17 body units and scenario bullets openspec/specs/avatar-client-runtime/spec.md currently states for it — a divergence this arm CANNOT distinguish from a deliberate rewording, and does not claim to: [body] 'AVC-03 and AVC-05 are absorbed as described; AVC-09 and AVC-10 remain reserved for the live-qualification successor change and their identif…'" action="restate the requirement as canon currently states it, or declare the deletion with a `Removed from canon by` marker" class="contested"
- severity=info family=release-tag-publication repo=openxFactory path=contracts/releases/contract-v2.6.digests.yaml rule="contract-v2.6 is declared SPENT: it was cut, has no published annotated tag, and contract-v3.0 — itself cut, itself published and strictly later — superseded it. The record is contracts/CHANGELOG.md § contract-v3.0 — RULED BY Brett Heap, 2026-09-02; MEASUREMENT: PR #565 comment `5502452624`. The tag obligation was not met, it was EXTINGUISHED by an owner act at the cost of a version number" action="no action, and this is NOT the tag obligation having been met — it was EXTINGUISHED, by an owner act, at the cost of a version number, and the record says which; the state is permanent, and never edit the manifest, the changelog or the inventory to stop it being reported" class="contested"
- severity=info family=staged-candidate-aging repo=openxFactory path=(drafts) rule="draft age distribution days: min=0 max=63 n=70" action="trend data — no action required" class="contested"
