# doc-health

## MODIFIED Requirements

### Requirement: Aging threshold defaults
The contract SHALL define default aging thresholds so reports are comparable
across runs: staged topics and `xspec:candidate` blocks untouched 30 days are
`warning` findings escalating to `error` at 90 days; an `xspec:supersedes`
marker without `change=` is `warning` at 14 days escalating to `error` at 45
days; `draft` documents have their age distribution reported always (`info`)
with a `warning` at 60 days without a lifecycle transition; after catalog
baseline, a document classification that remains `pending` for 30 days SHALL be
a `warning` and SHALL escalate to `error` at 90 days from its preserved
facet-level `state_since`; and routing records in `intake`, `triaging`, or
incomplete `split` state whose latest transition is 30 days old are `warning`
findings escalating to `error` at 90 days. `routed`, `rejected`, and explicitly
`deferred` routing records SHALL NOT age as unresolved work.

A staged topic SHALL NOT age as unresolved work once it records the outcome it
reached. Two records SHALL stop it, and no others: its primary fragment
carrying `Status: superseded` or `Status: retired`, or an `Exit taken:` line —
in the repository's staging index entry for that topic, or in the primary
fragment itself where the repository keeps no index — naming an OpenSpec change
that has ARCHIVED. A citation of an ACTIVE change SHALL NOT stop it, because
that topic's proposal is in flight and its staged material is the move the
`location-conformance` family is concurrently reporting.

`Exit taken:` is a record and NOT a lifecycle status: this contract SHALL NOT
introduce a deferred state for staged topics, and a topic parked behind a named
gate SHALL keep ageing. A topic's age measures whether the work moved, not
whether someone approves of it standing still. The aging action line SHALL
therefore name the records that do stop it rather than a state that does not
exist.

#### Scenario: An item crosses an aging threshold
- **WHEN** an item's untouched age crosses a threshold
- **THEN** the run MUST emit the finding at the threshold's severity
- **AND** crossing an escalation boundary produces a new `error` finding subject to the regression rule

#### Scenario: A staged topic's primary fragment is closed
- **WHEN** a staged topic's primary fragment carries `Status: superseded` or `Status: retired`
- **THEN** the run MUST NOT emit a staged-topic aging finding for that topic, at any age
- **AND** the closing header remains subject to `succession-integrity`, which requires a resolvable successor or a stated reason, so the silence cannot be bought by an empty claim

#### Scenario: A staged topic records the exit it took
- **WHEN** a staged topic's staging-index entry or primary fragment carries an `Exit taken:` line naming a change that has archived
- **THEN** the run MUST NOT emit a staged-topic aging finding for that topic
- **AND** the remedy the finding would have stated — raise a proposal — names an act already performed and closed

#### Scenario: A staged topic cites an exit that is still active
- **WHEN** a staged topic's `Exit taken:` line names only changes that are still active
- **THEN** the run MUST still emit the staged-topic aging finding at its threshold severity

#### Scenario: A staged topic is deferred behind a named gate
- **WHEN** a staged topic records a deferral and names the gate it waits on
- **THEN** the run MUST still emit the staged-topic aging finding, because no deferred state exists for a staged topic and a schedule is not a standing

#### Scenario: A draft lives long legitimately
- **WHEN** a `draft` document ages without transition
- **THEN** it MUST appear in age reporting and, past 60 days, as a `warning` ranked-plan item — never as `critical` or `error` on age alone

#### Scenario: Catalog classification remains pending
- **WHEN** a post-baseline catalog facet remains pending from the same `state_since` for 30 or 90 days
- **THEN** the run MUST emit a warning at 30 days and an error at 90 days

#### Scenario: Catalog pending threshold is overridden
- **WHEN** a run uses non-default catalog-pending thresholds
- **THEN** the report MUST disclose the configured thresholds

#### Scenario: Active routing work ages
- **WHEN** an `intake`, `triaging`, or incomplete `split` record's latest transition reaches 30 or 90 days
- **THEN** the run MUST emit a warning at 30 days and an error at 90 days

#### Scenario: Deferred routing is intentional
- **WHEN** a routing record is explicitly `deferred` with its reason recorded
- **THEN** it MUST NOT be reported as abandoned unresolved intake

#### Scenario: Routing threshold is overridden
- **WHEN** a run uses non-default routing-aging thresholds
- **THEN** the report MUST disclose the configured thresholds
