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
- **WHEN** an aggregation-checkout run (`Context.agg_root` set — never `--single-repo`, which reads no disposition of any family) sees the aggregation's `health/dispositions.yaml` carry a dated, cited entry naming a check family, a repository and a path, and this capability declares no disposition reading for that family
- **THEN** the entry MUST change no finding OF THE FAMILY IT NAMES — not its severity, not its action, not whether that finding is reported at all — because a family-side disposition is read by the arm the family's OWN requirement declares, and a family whose requirement declares none has NO FAMILY-SIDE ARM to read it, which is a statement about that family's own arm and not about the family-neutral rule below
- **AND** the entry MUST still be read by the contested-resolution rule above, which reaches a DERIVED finding and never the named family's own row: where a finding the entry names was reported `contested` and the LATER run EVALUATED that family and that repository and no longer reports it, the derived `uncited resolution` error MUST NOT be emitted against it — the one effect an entry of such a family has ever had
- **AND** where the later run RECORDED the named family or the named repository as unavailable to that rule — a lane whose findings are folded in after the deterministic render, a family EXCLUDED BY THIS RUN'S OWN CONFIGURATION (named by `--skip-family`, or every other family under a single `--family` run), or a repository the baseline's stamped identity puts outside this run's scope — that rule MUST NOT emit the derived error whether an entry exists or not, an absence that only means the check did not run being no resolution to cite
- **AND** where a run's scope excludes a family or a repository WITHOUT recording it as unavailable — including a family's OWN check function returning an ordinary `Skip` result rather than being named by `--skip-family` — this requirement MUST be read as stating nothing and ratifying nothing about that case, the change that adds this scenario reporting three such measured gaps rather than repairing them
- **AND** where the entry's own key was NOT recorded `contested` IN THE PREVIOUS REPORT, the entry MUST reach nothing through that rule, which iterates the previous report's contested rows and not the later run's resolution classes — so a family whose rows are never classified `contested` can never put a key there, while a key recorded `contested` once stays eligible even if that family's later rows are `auto-fixable`
- **AND** an entry naming the `uncited-resolution` family itself MUST change nothing at all, that family's rows never entering the contested set the rule above iterates

#### Scenario: A recorded disposition names a family this capability does give a reading
- **WHEN** an aggregation-checkout run (`Context.agg_root` set — never `--single-repo`, which reads no disposition of any family) sees the aggregation's `health/dispositions.yaml` carry a dated, CITED entry naming a check family, a repository and a path, matching the further key shape that family's own reader requires, for which family this capability DOES declare a disposition reading in that family's own requirement — an entry carrying no cite, or missing a key its family's own reader requires (a string `content_sha256`, for `neutrality-drift`), recording no decision and being admitted by no reader
- **THEN** the entry MUST be read over THAT FAMILY'S OWN FINDINGS exactly as that family's own declaration says and by that declaration alone, whether it suppresses or downgrades
- **AND** the family-neutral contested-resolution rule above MUST still reach the entry WHEREVER THAT RULE'S OWN EVALUATION SCOPE REACHES THE NAMED FAMILY AND REPOSITORY, the words "by that declaration alone" governing the family-side effect and never displacing that rule
- **AND** where that rule's scope excludes the named family — a lane whose findings are folded in after the deterministic render, or a family EXCLUDED BY THIS RUN'S OWN CONFIGURATION (named by `--skip-family`, or every other family under a single `--family` run) — the entry MUST reach nothing through it, this requirement declaring no new reachability for any family
- **AND** the preceding scenario MUST neither widen nor narrow any such declaration, its condition being the ABSENCE of one
