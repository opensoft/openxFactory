# client-layer-tuning Specification

## Purpose
The neutral tenant-layer contract set: the house-team roster (10 deciders
incl. the Finance & Accounting Officer + the liaison capability, voice floor
locked), the client content schemas incl. the seedable
`hermes_client_overlay`, and the canonical stricter-only comparability
validator (`scripts/validate-client-content.py`) consumed by the wizard at
write time and the seeder at validation time. Realized at `contract-v1.17`
and live-proven by the opensoft tenant flip (2026-07-24). (Created by
archiving change add-client-layer-tuning-contracts.)
## Requirements
### Requirement: The neutral house-team roster is declared content
openxFactory SHALL declare the client-layer Plane-1 house team under `templates/client-layer/roles/`: a `house_style` baseline with `respectful` and `discreet` locked, `warmth` floored at `moderate`, and per-axis tunable ranges; ten decider personas including a Finance & Accounting Officer owning cost reporting and the tracking-granularity contract; and the Client Infrastructure Liaison declared as a composed capability the team convenes, never a member.

#### Scenario: Roster completeness
- **WHEN** the roles directory is read
- **THEN** the ten deciders and the liaison capability are present, each with authority, disposition (locked), voice (tunable within declared ranges inheriting the house style), and the character-never-overrides-authority guardrail

#### Scenario: The voice floor is locked
- **WHEN** any persona or the house style is read
- **THEN** `respectful` and `discreet` are not client-tunable and `warmth` cannot be tuned below `moderate`

### Requirement: Client content shapes are contract-validated
openxFactory SHALL define schemas for `client_policy_overrides`, `client_memory_boundaries`, `client_integration_boundaries`, and the seedable `hermes_client_overlay` (canonical path `config/clients/<client_ref>/overlay.yaml`, declared via the install repo's overlay descriptor, digest-pinned in the install's `client_overlays[]`), with self-testing packaged examples and intended-reason negatives.

#### Scenario: Positive examples validate, negatives fail for their reason
- **WHEN** the canonical validator runs its self-test
- **THEN** every packaged example passes and every negative fails for its declared reason

#### Scenario: The client overlay carries the enforceable tenant slice
- **WHEN** a `hermes_client_overlay` is validated
- **THEN** it carries the client identity, the policy-overrides block with `relation_to_domain: stricter_only`, budget envelopes with the tracking-granularity contract, the approval matrix with its human-ratified auto-clear envelope reference, and the integration boundaries — with no raw secret anywhere

### Requirement: Stricter-only is checked by the comparability spec
The canonical validator SHALL implement the comparability semantics — allowlists subset, denylists superset, numeric ceilings at-or-below, floors at-or-above, clearance requirements add-only, conjunctive envelope conditions add-only, ordered enums at-or-above — verifying a client document against a domain baseline, and SHALL park any field with no defined partial order as `review_required`, never passing it silently.

#### Scenario: A weakening override fails closed
- **WHEN** a client document loosens any comparable field relative to the baseline (removes an envelope conjunct, raises a ceiling, shrinks a denylist)
- **THEN** validation fails naming the field and the rule violated

#### Scenario: No-order fields park for review
- **WHEN** a field has no defined comparison semantics
- **THEN** the verdict is `review_required` for that field, never a silent pass

#### Scenario: One implementation, two enforcement points
- **WHEN** the wizard writes client content or the seeder validates a client overlay
- **THEN** both consume this same canonical validator, so the wizard can never write what the seeder would reject
