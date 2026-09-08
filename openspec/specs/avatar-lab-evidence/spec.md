# avatar-lab-evidence Specification

## Purpose

Establish openxFactory's ownership of the neutral, content-addressed
acceptance artifacts the avatar client lab is measured against, so that no
consumer serves itself the evidence it is judged by. Define the avatar-state
derivation table that maps the closed kernel `media.states` and the AVC-12
`control_health` and `session_outcome` values onto the six avatar
presentation states totally, with its fail-closed invariants embedded and
every mapping either source-cited or explicitly ratified, and the
capability-scenario register that addresses the lab's requirements and
scenarios by stable ID with byte-verbatim titles machine-checked against the
promoted spec. Adopt the deterministic fixture families that close the
state-reachability denominator through kernel fields alone, each fixture's
evidence ids resolving in an acceptance map. Fix how these artifacts reach
the contract surface — only through an additive release cut carrying
manifest digests, a changelog entry, and a tag, leaving every already
released bundle byte-identical, with a released `deferred` entry discharged
by a successor register rather than an in-place flip.
## Requirements
### Requirement: Neutral avatar-state derivation table
openxFactory SHALL own a content-addressed avatar-state derivation table
(`contracts/avatar-client-lab/avatar-state-derivation-table.md` + `.yaml`)
that maps the authoritative runtime axes — the ten closed `media.states` and
the AVC-12 `control_health`/`session_outcome` values, resolved with
`session_lifecycle`/`workflow_projection` where the table so names — to the
six avatar presentation states, totally (no uncovered combination), embedding
the normative derivation invariants (`control_lost`/`control_degraded` ⇒
`blocked` never `speaking`; unknown ⇒ fail-closed; `handoff` ⇒ `handoff`; the
consent-withdraw revocation terminal leaves `speaking` to a non-speaking,
non-`blocked` state), with every mapping either source-cited or explicitly
ratified in this change.

#### Scenario: Table is total over the axis combinations
- **WHEN** `check_avatar_state_derivation_table` runs against the landed table
- **THEN** the outputs set MUST equal the six avatar states, the `media_states` set MUST equal the closed ten, and every named axis combination MUST resolve to exactly one avatar state

#### Scenario: Table contradicts a normative invariant
- **WHEN** any table row maps `control_lost` or `control_degraded` to a state other than `blocked`, or maps an unknown-value guard to a non-fail-closed state
- **THEN** validation MUST fail closed and the release cut MUST be blocked

#### Scenario: Landed seeds reproduce under the table
- **WHEN** each landed deterministic seed's kernel condition is resolved through the table's precedence rules
- **THEN** the resolved avatar state MUST equal the seed's stated avatar state

#### Scenario: Unsourced candidate mapping reaches ratification
- **WHEN** a candidate mapping carries no source citation (including the candidate's open questions OQ-1..OQ-6)
- **THEN** landing MUST record either a citation or an explicit product-owner ratification replacing it, and an unratified mapping MUST block the table's landing task

### Requirement: Capability-scenario register
openxFactory SHALL own a content-addressed capability-scenario register
(`contracts/avatar-client-lab/capability-scenario-register.yaml`) enumerating
the avatar-client-lab capability scenarios with stable per-scenario IDs and
verbatim titles — exactly 9 requirements and exactly 22 scenarios in source
document order — machine-checked fail-closed against the capability spec's
`### Requirement:` / `#### Scenario:` headings, so that gate (ix)(b)
scenario-resolution can address the capability set by stable ID from a
pinned, offline-readable artifact.

#### Scenario: Register fidelity is machine-checked
- **WHEN** the register validator runs against the capability spec source
- **THEN** requirement count MUST equal 9, scenario count MUST equal 22, and every title MUST byte-match its heading in the same document order, failing closed on any fabricated, renamed, dropped, or reordered entry

#### Scenario: Capability spec promotes after landing
- **WHEN** `implement-avatar-client-lab` archives and its capability spec promotes to `openspec/specs/avatar-client-lab/spec.md`
- **THEN** the register fidelity check MUST re-verify against the promoted path and a mismatch MUST fail validation

#### Scenario: Consumer retires its interim enumeration
- **WHEN** a consumer (the codexFactory lab) pins the landed register
- **THEN** the consumer MUST source gate (ix)(b) enumeration from the pinned register and MUST retire any interim transcribed checklist and its faithfulness guard

### Requirement: Adopted deterministic fixture families
The deterministic fixture corpus SHALL include, under
`examples/avatar-first-ui/fixtures/deterministic/`, the adopted
intake-remainder, takeover/recovery, interrupted/handoff, and
kernel-`media.state` coverage families (the P7/P8/P11/P12/P13 candidate sets,
landed verbatim from their panel-confirmed source commit apart from the
status-header convention), each fixture evidencing its denominator state or
scenario exclusively through kernel fields, with every evidence id resolving
in an acceptance map and any discharge of a released `deferred` entry
expressed only as a successor-register entry.

#### Scenario: Denominator state evidenced via kernel fields
- **WHEN** an adopted fixture claims a closed `media.state`, `control_health`, or `session_outcome` condition
- **THEN** the claim MUST be carried by kernel fields (AVC-12 snapshot `media_state`, `control_health`, `session_outcome`) and MUST NOT rely on the presentation `media_state`

#### Scenario: Adopted fixtures pass the upstream validators
- **WHEN** `validate-avatar-first-ui.py` (baseline and realization) and `validate-avatar-client.py` run with the adopted families present
- **THEN** all checks MUST pass, including evidence-id parity for every new fixture

#### Scenario: Deferred entry discharge is attempted in place
- **WHEN** a landing edit flips a released evidence-register entry from `deferred` to `evidenced` in place
- **THEN** validation MUST fail closed; the discharge MUST exist only as a successor-register entry with `discharges_deferred: true` and a matching `owner_change`

### Requirement: Additive release registration
The adopted artifacts SHALL enter the contract surface only through the next
additive release cut (`contract-v1.12`): manifest membership with computed
per-file digests for the new client-lab artifacts, the adopted fixture
families, and `evidence-register.implement-avatar-client-lab.yaml`; a
changelog entry; and a release tag — while every file of the released
`contract-v1.7` and `contract-v1.8` bundles remains byte-identical.

#### Scenario: Release cut registers the new artifacts
- **WHEN** `contract-v1.12` is cut
- **THEN** `contracts/manifest.yaml` MUST list each new artifact with its sha256, the changelog MUST record the adoption, and the successor evidence register MUST become manifest-registered so its recorded discharge can take effect

#### Scenario: Released bundles are disturbed
- **WHEN** any file belonging to the released `contract-v1.7` or `contract-v1.8` sets differs byte-wise after the adoption commits
- **THEN** the release cut MUST be blocked and the deviation reverted

#### Scenario: Realization completes on the consumer
- **WHEN** the codexFactory lab resyncs its pin to `contract-v1.12`
- **THEN** the lab MUST vendor the new artifacts content-addressed, retire the interim P10 guard, un-skip its P8-blocked assertions, and prove its nine offline gates green before this change claims realization

