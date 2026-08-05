# doc-health Delta: The Neutrality-Drift Lane

## ADDED Requirements

### Requirement: Neutrality drift is scouted nightly
The doc-health pipeline SHALL include a neutrality-drift lane that reviews domain-factory content against the domain-neutral boundary on the nightly cadence: deterministic pre-filter signals (near-duplication of a neutral artifact, absence of domain vocabulary in a schema or script, cross-repo consumers, tooling absent from the domain's declared inventory) select candidates, and a model-driven scout under a versioned prompt contract judges the survivors and content changed since the lane's last run, returning structured candidates with neutrality evidence, counter-evidence, and domain-local exclusions.

#### Scenario: A neutral-shaped artifact appears in a domain repo

- **WHEN** a domain factory gains a schema, script, or process doc that another domain would need essentially unchanged
- **THEN** a nightly run within the lane's incremental window MUST surface it as a neutrality candidate with evidence and counter-evidence
- **AND** the scout's judgment MUST cite the file's own content, never only its location

#### Scenario: Scope is the domain factories

- **WHEN** the lane selects subjects
- **THEN** it reviews the pinned `xFactories/*` domain repos and MUST NOT review openxFactory, openAvatar, or the install realizations in v1

### Requirement: Candidates become staged proposals under human approval
The lane's findings SHALL be delivered as drafted DTN-register seed candidates (register row plus detail section in the register's own format) and ranked-plan items through the existing rolling health PR; a candidate advances only by Brett's approval of the seed, movement follows the domain-to-neutral promotion process, and the lane SHALL NOT edit any domain repo, open any move PR, or modify any contract.

#### Scenario: A candidate is proposed and approved

- **WHEN** the lane files a neutrality candidate
- **THEN** the rolling health PR carries the drafted register seed and the plan item
- **AND** only the human approval of that seed admits it to the register's lifecycle

#### Scenario: A rejected candidate stays rejected

- **WHEN** Brett dispositions a candidate as not-neutral or not-now
- **THEN** the disposition is recorded in the health dispositions register keyed by repo, path, and content digest
- **AND** the lane MUST NOT re-file the candidate while that content is unchanged

#### Scenario: Authority never transfers

- **WHEN** the lane finds even an unambiguous misplacement
- **THEN** it reports and stages only — content authority stays with the owning factory and every move lands through its own ratified change
