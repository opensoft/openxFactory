## MODIFIED Requirements

### Requirement: Explicit delta rule
Documents SHALL express any change to, contradiction of, or restatement of
promoted policy outside `ideation/brainstorm/` as an explicit change from
current state: an OpenSpec change proposal, or prose carrying the canonical
supersedes marker
`<!-- xspec:supersedes spec=<capability>/<requirement-slug> change=<change-id> -->`
naming the affected spec requirement. Prose designated for conversion to a
spec or contract SHALL be selected with the canonical block-level candidate
marker `<!-- xspec:candidate target=<capability> -->` ...
`<!-- /xspec:candidate -->`; candidacy is block-level only and no document
lifecycle status value expresses conversion candidacy. Accidental
restatement of promoted policy in differing words SHALL be treated as a
defect.

#### Scenario: Prose contradicts a promoted spec
- **WHEN** a document outside `ideation/brainstorm/` asserts behavior that conflicts with a promoted spec requirement
- **THEN** the document MUST either carry an `xspec:supersedes` marker naming that requirement (gaining a `change=` id once the OpenSpec change exists), or be corrected
- **AND** health tooling MUST report unmarked contradictions as findings

#### Scenario: Prose is tagged for conversion
- **WHEN** an author designates prose as needing conversion to a spec or contract
- **THEN** the designation MUST be an `xspec:candidate` block fence pair around the passage, naming the target capability
- **AND** only prose inside well-formed candidate blocks is queued for conversion
- **AND** the document's `Status:` header MUST NOT be used to express candidacy (no `spec-candidate` status exists)

#### Scenario: A staged fragment enters the queue
- **WHEN** a fragment lives in `ideation/staging/<topic>/` with a header declaring target capability and delta type
- **THEN** it is queued structurally by that header
- **AND** it MUST NOT require inline `xspec:` markers to be queued

## ADDED Requirements

### Requirement: Prose tagging marker hygiene
All `xspec:` markers SHALL be machine-checkable contract surface: every
occurrence of the literal string `xspec:` in governance Markdown MUST parse
against the canonical grammar (`xspec:candidate` open fence,
`/xspec:candidate` close fence, `xspec:supersedes` inline marker, with
space-separated unquoted `key=value` attributes), every marker target MUST
resolve, and candidate blocks MUST be properly fenced — no nesting, no
crossing of Markdown heading boundaries, and no unmatched open or close
fence. Deterministic health tooling SHALL report violations as findings.

#### Scenario: A marker is malformed or unknown
- **WHEN** the string `xspec:` occurs in a governance document but does not parse as a canonical `xspec:candidate`, `/xspec:candidate`, or `xspec:supersedes` marker
- **THEN** the deterministic health pass MUST report it as a hygiene finding

#### Scenario: A marker target does not resolve
- **WHEN** a marker names a `target=<capability>` or `spec=<capability>/<requirement-slug>` that does not exist under `openspec/specs/` or in an active change's spec deltas
- **THEN** the deterministic health pass MUST report it as a hygiene finding

#### Scenario: A candidate block is structurally invalid
- **WHEN** an `xspec:candidate` block nests inside another candidate block, spans a Markdown heading, or lacks a matching open or close fence
- **THEN** the deterministic health pass MUST report it as a hygiene finding

#### Scenario: A supersedes marker never acquires a change id
- **WHEN** an `xspec:supersedes` marker persists without a `change=` attribute beyond the doc-health aging threshold
- **THEN** the health pass MUST report it as an aging finding rather than accepting it as a permanent state
