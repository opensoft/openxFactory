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
- **WHEN** an aggregation-checkout run (`Context.agg_root` set — never `--single-repo`, which reads no disposition of any family) sees the aggregation's `health/dispositions.yaml` carry a CITED entry naming a check family, a repository and a path, and this capability declares no FAMILY-SIDE disposition reading for that family — the family-neutral contested-resolution rule above is a separate, existing reading, and "no" here negates only a reading in that family's own requirement
- **THEN** the entry MUST change no finding OF THE FAMILY IT NAMES — not its severity, not its action, not whether that finding is reported at all — because a family-side disposition is read by the arm the family's OWN requirement declares, and a family whose requirement declares none has NO FAMILY-SIDE ARM to read it, which is a statement about that family's own arm and not about the family-neutral rule above
- **AND** the entry MUST still be read by the contested-resolution rule above, which reaches a DERIVED finding and never the named family's own row: where a finding the entry names was reported `contested` and the LATER run EVALUATED that family and that repository and no longer reports it, the derived `uncited resolution` error MUST NOT be emitted against it — the one effect an entry of such a family has ever had — EXCEPT where the entry names `semantic-contradiction` or `semantic-normative-prose`: the ALREADY-PROMOTED *Semantic finding disposition authority* requirement (this file, *A layer without standing disposes a finding*) governs those two families' dispositions on its own terms — an authority other than the finding's named disposer — and this scenario's admission shape (a cited, keyed entry) is not proof of that authority; this scenario neither overrides nor discharges that requirement for the semantic pair
- **AND** the preceding exception states a boundary rather than a reading: this capability does not test disposition authority for any family, semantic or otherwise, and the contested-resolution rule's own code does not either — the exception exists so this scenario's blanket MUST NOT is not read as silently satisfying a DIFFERENT, already-ratified requirement it was never written to satisfy
- **AND** where the later run RECORDED the named family or the named repository as unavailable to that rule — a lane whose findings are folded in after the deterministic render, a family EXCLUDED BY THIS RUN'S OWN CONFIGURATION (named by `--skip-family`, or every other REGISTERED family under a single `--family` run — `runner.FAMILIES` only; the semantic pair is not a member and is NOT excluded even then, the gap § 7.6(b) records), or a repository the baseline's stamped identity puts outside this run's scope — that rule MUST NOT emit the derived error whether an entry exists or not, an absence that only means the check did not run being no resolution to cite
- **AND** where a run's scope excludes a family or a repository WITHOUT recording it as unavailable — including a family's OWN check function returning an ordinary `Skip` result rather than being named by `--skip-family` — this requirement MUST be read as stating nothing and ratifying nothing about that case, the change that adds this scenario reporting three such measured gaps rather than repairing them
- **AND** where the entry's own key was NOT recorded `contested` IN THE IMMEDIATELY PREVIOUS REPORT, the entry MUST reach nothing through that rule, which iterates that ONE previous report's contested rows — `parse_previous` reads a single `--previous-report`, never a history of them — and not the later run's resolution classes: so a family whose rows the immediately previous report never classified `contested` can never put a key there for this transition, while a key that report DID record `contested` stays eligible FOR THIS ONE TRANSITION regardless of what class the family's rows carry in the later, current run — an eligibility that does not compound or persist beyond this single previous-report-to-current-run comparison
- **AND** an entry naming the `uncited-resolution` family itself MUST change nothing at all, that family's rows never entering the contested set the rule above iterates

#### Scenario: A recorded disposition names a family this capability does give a reading
- **WHEN** an aggregation-checkout run (`Context.agg_root` set — never `--single-repo`, which reads no disposition of any family) sees the aggregation's `health/dispositions.yaml` carry a CITED entry naming a check family, a repository and a path, for which family this capability DOES declare a disposition reading in that family's own requirement — an entry carrying no cite recording no decision and being admitted by no reader
- **THEN**, PROVIDED the entry also satisfies whatever FURTHER admission predicate that family's own reader declares beyond the cite (a `date` for `ratified-provenance`, `families.py:445-456` — that reader separately requires the MATCHED FINDING's own path, not the entry's, to sit under the archive prefix, `families.py:527-528`; a string `content_sha256` for `neutrality-drift`, `neutrality.py:669-677`), the entry MUST be read over THAT FAMILY'S OWN FINDINGS exactly as that family's own declaration says and by that declaration alone, whether it suppresses or downgrades — an entry failing that further predicate is left to the family-neutral reader above, admitted or not on that reader's own terms and never this one's
- **AND** the family-neutral contested-resolution rule above MUST still reach the entry WHEREVER THAT RULE'S OWN EVALUATION SCOPE REACHES THE NAMED FAMILY AND REPOSITORY, the words "by that declaration alone" governing the family-side effect and never displacing that rule
- **AND** a CITED entry missing a key that family's own reader further requires (a string `content_sha256`, for `neutrality-drift`) is still ADMITTED by the family-NEUTRAL reader above, which tests only the cite and not that further key — admission alone, and the following bullet's scope-exclusion still governs whether the contested-resolution rule ever reaches it, `neutrality-drift` itself being one of the lanes that bullet excludes UNCONDITIONALLY (folded in after the deterministic render, `runner.py:830`)
- **AND** where that rule's scope excludes the named family — a lane whose findings are folded in after the deterministic render, or a family EXCLUDED BY THIS RUN'S OWN CONFIGURATION (named by `--skip-family`, or every other REGISTERED family under a single `--family` run — `runner.FAMILIES` only; the semantic pair is not a member and is NOT excluded even then, the gap § 7.6(b) records) — the entry MUST reach nothing through it, this requirement declaring no new reachability for any family
- **AND** the preceding scenario MUST neither widen nor narrow any such declaration, its condition being the ABSENCE of one
