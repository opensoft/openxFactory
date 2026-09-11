# doc-health

## MODIFIED Requirements

### Requirement: Finding severity and regression handling
Every finding SHALL carry one severity from `critical` (governance
integrity broken), `error` (contract violation), `warning` (drift or
first-stage aging), or `info` (inventory and metrics); one resolution class
from `auto-fixable` (mechanical defect: malformed marker, broken link,
missing header, formatting) or `contested` (resolution would change a
deliberately-set state, arbitrate between rules, or reverse a prior gate
decision); and a regression — any `critical` or `error` finding not present
in the previous report, matched by check family and path — MUST open a
single issue per run in the aggregation repo listing the new findings.

#### Scenario: A new error-level finding appears
- **WHEN** a run emits a `critical` or `error` finding absent from the previous report
- **THEN** one issue for the run MUST be opened in the aggregation repo listing all such new findings

#### Scenario: Findings persist unchanged
- **WHEN** a finding present in the previous report recurs
- **THEN** it MUST appear in the report and plan but MUST NOT open or duplicate an issue

#### Scenario: A contested finding is resolved
- **WHEN** a finding classified `contested` stops appearing between consecutive reports
- **THEN** its resolution MUST cite an OpenSpec change or a recorded human disposition against the finding id
- **AND** a contested finding that disappears via a state or status change with no such citation MUST be emitted as a new `error` finding ("uncited resolution") naming the original finding

#### Scenario: A session works a report's plan
- **WHEN** a session resolves ranked-plan items from a report
- **THEN** it MAY apply `auto-fixable` items directly
- **AND** it MUST NOT apply state-changing edits for `contested` items — those are escalated for a change proposal or human disposition

#### Scenario: The headline metric declines
- **WHEN** canon share by words drops between runs
- **THEN** the decline is trend data in the report, not a regression — no issue is opened for it alone

#### Scenario: A recorded disposition names a family this capability gives no reading
- **WHEN** the aggregation's `health/dispositions.yaml` carries a dated, cited entry naming a check family, a repository and a path, and this capability declares no disposition reading for that family
- **THEN** the entry MUST change no standing finding — not its severity, not its action, not whether it is reported at all — because a disposition is read by the arm the family's OWN requirement declares, and a family whose requirement declares none has no arm to read it
- **AND** the entry MUST still be read by the contested-resolution rule above, so that when the finding it names later stops being reported the `uncited resolution` error is not emitted against it — which is the one effect an entry of such a family has ever had
- **AND** an entry naming the `uncited-resolution` family itself MUST change nothing at all, that family's rows never entering the contested set the rule above iterates

#### Scenario: A recorded disposition names a family this capability does give a reading
- **WHEN** the aggregation's `health/dispositions.yaml` carries an entry naming a check family for which this capability DOES declare a disposition reading in that family's own requirement
- **THEN** the entry MUST be read exactly as that family's own declaration says and by that declaration alone, whether it suppresses or downgrades
- **AND** the preceding scenario MUST neither widen nor narrow any such declaration, its condition being the ABSENCE of one
