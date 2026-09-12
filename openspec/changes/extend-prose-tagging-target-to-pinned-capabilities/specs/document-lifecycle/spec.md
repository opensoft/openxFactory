# document-lifecycle — spec delta

## MODIFIED Requirements

### Requirement: Prose tagging marker hygiene
All `xspec:` markers SHALL be machine-checkable contract surface: every
occurrence of the literal string `xspec:` in governance Markdown MUST parse
against the canonical grammar (`xspec:candidate` open fence,
`/xspec:candidate` close fence, `xspec:supersedes` inline marker, with
space-separated unquoted `key=value` attributes), every marker target MUST
resolve, and candidate blocks MUST be properly fenced — no nesting, no
crossing of Markdown heading boundaries, and no unmatched open or close
fence. Deterministic health tooling SHALL report violations as findings.

A marker target resolves in ONE of two forms. The IN-TREE form names a spec
capability id under `openspec/specs/`, or a capability in an active change's
`specs/` while it is pre-promotion. The PINNED form, `pinned:<pin-id>/<capability>`,
names a capability of a NEUTRAL PRODUCT THIS REPOSITORY PINS: `<pin-id>` is the
identifier of a pin record the repository carries, and `<capability>` is the
capability name as the pinned product holds it. The literal prefix `pinned:` is
RESERVED and is the discriminator between the two forms; a capability id MUST
NOT contain a colon. The PINNED form is admitted in an `xspec:candidate`
marker's `target=` attribute ONLY. An `xspec:supersedes` marker's
`spec=<capability>/<requirement-slug>` value MUST NOT carry the `pinned:`
prefix, and a `spec=` value that carries it MUST be reported: the spelling is
RESERVED AND REFUSED rather than merely undefined, because a `spec=` value
already carries a separator of its own and no pinned parse for it is defined —
a deferred form fails closed.

A PINNED target resolves when its `<pin-id>` resolves to a pin record this
repository carries. The `<capability>` segment MUST be well formed, and it MUST
additionally appear in the pin record's own capability enumeration WHERE THAT
RECORD CARRIES ONE; where the record carries no such enumeration, resolution
rests on the pin alone and the capability name is taken as declared. This
conditional arm is deliberate: it binds automatically, with no further grammar
delta, as soon as a pin record enumerates capabilities. It is NOT a licence to
read the pinned product over the network — the deterministic pass reads this
repository's tree and nothing else.

WHEN A TARGET CAPABILITY EXITS THE CORPUS, the marker SHALL either take the
pinned form naming the product that now holds the capability, or the block
SHALL be unfenced. A stale target MUST NOT be silently retargeted to a
different capability, and MUST NOT be silently deleted: retargeting makes the
marker name a capability the tagged prose is not about, and deleting the marker
drops the block out of the conversion queue without a record that it was
dropped. Unfencing is a lawful outcome that is CHOSEN and visible in the diff,
not the thing that happens when nobody decides.

#### Scenario: A marker is malformed or unknown
- **WHEN** the string `xspec:` occurs in a governance document but does not parse as a canonical `xspec:candidate`, `/xspec:candidate`, or `xspec:supersedes` marker
- **THEN** the deterministic health pass MUST report it as a hygiene finding

#### Scenario: A marker target does not resolve
- **WHEN** a marker names a `target=<capability>` or `spec=<capability>/<requirement-slug>` that does not exist under `openspec/specs/` or in an active change's spec deltas
- **THEN** the deterministic health pass MUST report it as a hygiene finding

#### Scenario: A marker names a capability of a pinned neutral product
- **WHEN** a marker names `target=pinned:<pin-id>/<capability>` and `<pin-id>` resolves to a pin record this repository carries
- **THEN** the target MUST resolve
- **AND** where that pin record enumerates capabilities, the named capability MUST appear in the enumeration or the pass MUST report a hygiene finding
- **AND** where it enumerates none, resolution MUST rest on the pin alone and the pass MUST NOT read the pinned product over the network

#### Scenario: A pinned target names a pin the repository does not carry
- **WHEN** a marker names `target=pinned:<pin-id>/<capability>` and no pin record for `<pin-id>` exists in this repository
- **THEN** the deterministic health pass MUST report it as a hygiene finding
- **AND** the finding MUST name the pin registry as the thing that failed to resolve, not `openspec/specs/`

#### Scenario: A supersedes marker carries the reserved pinned prefix
- **WHEN** an `xspec:supersedes` marker's `spec=` value begins with the reserved `pinned:` prefix
- **THEN** the deterministic health pass MUST report it as a hygiene finding
- **AND** the finding MUST state that the pinned form is admitted only in a candidate marker's `target=` attribute

#### Scenario: A target capability leaves the corpus
- **WHEN** a change removes a capability that live `xspec:` markers target
- **THEN** each affected marker MUST take the pinned form naming the product that now holds the capability, or its block MUST be unfenced
- **AND** the marker MUST NOT be retargeted to a different capability, nor deleted, as a way of clearing the finding

#### Scenario: A candidate block is structurally invalid
- **WHEN** an `xspec:candidate` block nests inside another candidate block, spans a Markdown heading, or lacks a matching open or close fence
- **THEN** the deterministic health pass MUST report it as a hygiene finding

#### Scenario: A supersedes marker never acquires a change id
- **WHEN** an `xspec:supersedes` marker persists without a `change=` attribute beyond the doc-health aging threshold
- **THEN** the health pass MUST report it as an aging finding rather than accepting it as a permanent state
