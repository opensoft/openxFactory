# doc-health

## MODIFIED Requirements

### Requirement: Governed corpus membership and the lifecycle scan set
The doc-health capability SHALL declare two document sets and SHALL keep them distinct.

The **governed corpus** is the set of Markdown documents under the governed
roots `contracts/`, `docs/`, `examples/`, `ideation/` and `templates/` of each
repository in scope, excluding `installs/`, `tests/`, `node_modules/`,
`__pycache__/` and any nested git working copy. It is the sole input to the
per-stage census, the governance and canon word totals, the canon-share
headline, the shared inventory, and the document catalog. `openspec/` is NOT
a governed root: promoted specs join the inventory as promoted specs and are
counted toward canon, and no other document under `openspec/` enters the
governed corpus.

The **lifecycle scan set** is a separately declared set of paths carrying
lifecycle headers outside the governed corpus. It SHALL be declared as an
explicit path pattern set rather than as a directory, and it SHALL comprise
each change packet's `proposal.md` and EVERY `review/` record under
`openspec/changes/`, whether or not that record's subject is a ratification.
A document in the lifecycle scan set is subject to the `document-lifecycle`
status and ratification-citation rules and to no other family's rules; the
citation half of that pair binds only a document whose status is `ratified`,
so a `review/` record carrying another taxonomy value is checked for its
status and for nothing else.

The scan set SHALL NOT reach a document that is byte-exact evidence rather
than live prose. A path carrying a `supporting-docs`, `source-snapshots` or
`evidence` segment SHALL be excluded from the set even where it otherwise
matches a declared pattern, because a frozen record reported for the state it
preserves is a false finding.

Widening either set is a governed change: a promoted OpenSpec change SHALL
record the new membership together with the measured effect on finding
counts by family, on the canon-share headline, and on the existing test
suite, because a corpus measurement whose scope changes silently reports the
scope rather than the corpus.

#### Scenario: A proposal carries an uncited ratified header
- **WHEN** a document in the lifecycle scan set carries `Status: ratified` with no ratification citation in either sanctioned spelling
- **THEN** the run MUST emit a `ratified-provenance` finding against that document's path
- **AND** the finding MUST carry the same severity it would carry for a governed-corpus document, because the defect is the same defect

#### Scenario: A proposal's lifecycle header sits outside the header window
- **WHEN** a document in the lifecycle scan set carries its `Status:` header past the header window, so the header reads as absent
- **THEN** the run MUST emit a `status-validity` finding of missing status header
- **AND** the run MUST NOT rely on `ratified-provenance` to catch it, because a document whose status does not parse is not a `ratified` document to that family

#### Scenario: The lifecycle scan set does not move the corpus metrics
- **WHEN** a doc-health run executes with a non-empty lifecycle scan set
- **THEN** the per-stage counts, the governance and canon word totals, the canon-share headline, the shared inventory, and the catalog snapshot MUST be identical to a run with an empty lifecycle scan set over the same corpus
- **AND** only the four families that read the set MAY report additional findings

#### Scenario: A family outside the declared four is added later
- **WHEN** a check family not named as a reader of the lifecycle scan set executes
- **THEN** it MUST read the governed corpus alone
- **AND** an automated check MUST hold that boundary, so that a family added later does not acquire or lose the wider scope by accident

#### Scenario: A document is byte-exact evidence rather than live prose
- **WHEN** a change packet holds a byte-exact snapshot of a staged fragment, illustrative malformed markers, or other evidence whose content is fixed by what it records
- **THEN** it MUST NOT be in the lifecycle scan set, because reporting a frozen record for the state it preserves is a false finding

#### Scenario: A finding is grandfathered by a recorded disposition
- **WHEN** a finding this family raises against a document under `openspec/changes/archive/` is named by an entry in the aggregation's `health/dispositions.yaml` carrying this family, that repository, that path, a date, and a non-empty `cite`
- **THEN** the run MUST report that finding at `info` rather than at the severity its own arm assigned, and MUST quote the recorded citation in the finding, because the record is IMMUTABLE and no repair is available to anyone — a permanent defect reported at `critical` teaches a reader to disbelieve the band, and a defect withheld altogether hides a standing population behind a file nobody opens
- **AND** the finding MUST keep its family, its repository and its path, so the population stays countable in the report and in every comparison between two reports
- **AND** the citation MAY be quoted as a bounded single-line excerpt, a ranked-plan row being one line and the entry's own key being the lookup into the file it was taken from
- **AND** a finding against a document under an ACTIVE change packet MUST NOT be downgraded by such an entry, an active record's header being a plain fix rather than a ruling's subject
- **AND** an entry carrying no `cite` MUST change nothing, an entry that records no decision having disposed nothing under every other reader of this file
- **AND** a run that has no aggregation checkout in scope MUST report every finding of this family at its own severity, the dispositions file living at the aggregation root and a single-repository run having none

#### Scenario: A recorded disposition matches no finding
- **WHEN** an entry in the aggregation's `health/dispositions.yaml` that this family would honour — carrying this family, a repository the run enumerated, a path, a date and a non-empty `cite` — names no finding this run raised, the record it names having been repaired or its path having vanished
- **THEN** the run MUST emit a `ratified-provenance` finding at `warning` against the dispositions file's own path in the aggregation, naming the entry's repository and path and quoting the recorded citation, because an entry that has stopped disposing anything is drift that no artifact a reader reads reports today and that the file keeps for as long as nobody re-reads it by hand
- **AND** the finding MUST NOT be raised against the record the entry names, that record being conformant or absent and its path therefore the wrong subject for a defect that is a line of another file
- **AND** an entry naming a repository the run READ NO DOCUMENT FROM MUST NOT be reported, the absence of a finding from a repository nobody read being no evidence about that entry — the scope of this class being the repositories that contributed a document to THIS FAMILY'S OWN SCAN SCOPE, which is the governed corpus TOGETHER WITH the lifecycle scan set, rather than the repositories the run enumerated, an unmaterialized pin being capable of enumerating as a repository and yielding no document of either set
- **AND** an entry this family would not honour — carrying no date, no `cite`, or another family's name — MUST NOT be reported, one entry-side admission rule serving both halves of the comparison so that the file converges on a set every reader of it agrees with
- **AND** the archived-path boundary of the scenario above MUST NOT narrow this class further, that boundary being a property of the FINDING the downgrade moves rather than of the entry, so an entry naming a path outside `openspec/changes/archive/` that names no finding this run raised MUST be reported like any other — an entry that can never dispose anything is the strongest case of an entry that disposes nothing rather than an exception to it
- **AND** a run that has no aggregation checkout in scope MUST report nothing of this class, the dispositions file living at the aggregation root and a single-repository run having none
