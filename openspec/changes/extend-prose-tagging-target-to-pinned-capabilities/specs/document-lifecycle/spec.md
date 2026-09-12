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
NOT contain a colon.

THE PINNED FORM'S LEXICAL GRAMMAR IS CLOSED, AND IT IS CHECKED BEFORE ANY PATH
IS BUILT. The value after `pinned:` SHALL be exactly TWO components separated by
exactly ONE `/`, and each component SHALL match `[a-z0-9]+(-[a-z0-9]+)*` — so a
component can carry no `/`, no `.`, no `:`, no whitespace and no upper-case
letter, and cannot be empty. A pinned value that does not match this grammar —
an extra `/` segment, a dotted or traversal component, an empty component — MUST
be reported as a malformed pinned target, and the deterministic pass MUST make
that judgement BEFORE it constructs any pin-record path, performs any pin
lookup, or reads any file for it. The marker regexes accept any non-whitespace
attribute value and are NOT the guard; this grammar is. The PINNED form is admitted in an `xspec:candidate`
marker's `target=` attribute ONLY. An `xspec:supersedes` marker's
`spec=<capability>/<requirement-slug>` value MUST NOT carry the `pinned:`
prefix, and a `spec=` value that carries it MUST be reported: the spelling is
RESERVED AND REFUSED rather than merely undefined, because a `spec=` value
already carries a separator of its own and no pinned parse for it is defined —
a deferred form fails closed.

A PINNED target resolves when its `<pin-id>` resolves to a NEUTRAL-PRODUCT pin
record this repository carries — a `contracts/<pin-id>-pin.yaml` declaring
`kind: pinned_contract_manifest`, the shape `neutral-product-pin` requires for
an external neutral product. A pin-shaped record of another kind, such as
`kind: pinned_workflow`, MUST NOT resolve a pinned target: it pins executable
governance code rather than a product whose units are capabilities, so it has
no capability set for the name to be about. A pin record that EXISTS but
cannot be read as a mapping carrying a `kind` — invalid YAML, a non-mapping
document, or no `kind` member — MUST be reported as an unreadable pin record
and MUST NOT resolve a pinned target, and the pass MUST complete rather than
abort: a corrupt record in the registry is a controlled finding, never an
exception that takes the run down with it. The `<capability>` segment MUST be well formed, and it MUST
additionally appear in the pin record's own capability enumeration WHERE THAT
RECORD CARRIES ONE; where the record carries no such enumeration, resolution
rests on the pin alone and the capability name is taken as declared. A PIN
RECORD'S CAPABILITY ENUMERATION IS ONE NAMED MEMBER AND NOT A SEARCH: a
top-level `capabilities:` sequence of capability names on the pin record. A
record without that member carries no enumeration for this purpose, and the
pass MUST NOT read capability names out of any other member — a file list, a
digest list or a member list is not a capability list, and inferring one from
them is non-deterministic. The enumeration SHALL be NON-EMPTY: an empty
sequence is not a statement that the product has no capabilities, it is a
broken member, and it MUST NOT be read as a valid enumeration nor as an absent
one. A `capabilities:` member that is PRESENT but is not a NON-EMPTY sequence of
well-formed capability names — including an empty sequence, a null value, a
scalar, a mapping, or a sequence carrying an item that is not a capability-shaped
name — MUST be reported as a malformed enumeration against the pin record, and MUST NOT be read as an absent
enumeration; while it is malformed, a pinned target naming that record does NOT
resolve. THAT OBLIGATION IS REACHED THROUGH THE MARKER AND NOT BY A SWEEP: the
pass reads a pin record because a live marker names it, and this capability
imposes NO registry-wide scan of pin records no live marker references. A pin
record's own well-formedness, unreferenced, is `neutral-product-pin`'s business
and not the marker grammar's. A deferred or broken enumeration fails closed rather than degrading
open. Whether a pin record may carry `capabilities:` is owned by
`neutral-product-pin`, not by this capability. This
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
- **WHEN** a marker names an IN-TREE `target=<capability>` or `spec=<capability>/<requirement-slug>` — a value carrying no `pinned:` prefix — that does not exist under `openspec/specs/` or in an active change's spec deltas
- **THEN** the deterministic health pass MUST report it as a hygiene finding
- **AND** a target carrying the `pinned:` prefix is NOT judged by this scenario, which would otherwise report every well-formed pinned target

#### Scenario: A marker names a capability of a pinned neutral product
- **WHEN** a marker names a lexically well-formed `target=pinned:<pin-id>/<capability>`, `<pin-id>` resolves to a pin record this repository carries that declares `kind: pinned_contract_manifest`, and that record EITHER carries no `capabilities:` member OR carries a well-formed non-empty one in which `<capability>` appears
- **THEN** the target MUST resolve
- **AND** where the record carries no `capabilities:` member, resolution MUST rest on the pin alone and the pass MUST NOT read the pinned product over the network
- **AND** a malformed enumeration, and a well-formed enumeration in which `<capability>` does not appear, are OUTSIDE this scenario and are judged by their own scenarios below

#### Scenario: A pinned capability is absent from the pin record's enumeration
- **WHEN** a marker names `target=pinned:<pin-id>/<capability>`, the record for `<pin-id>` carries a well-formed non-empty `capabilities:` member, and `<capability>` does not appear in it
- **THEN** the deterministic health pass MUST report it as a hygiene finding naming the enumeration
- **AND** the target MUST NOT resolve

#### Scenario: A pinned target names a record that is not a neutral-product pin
- **WHEN** a marker names `target=pinned:<pin-id>/<capability>` and the record for `<pin-id>` declares a kind other than `pinned_contract_manifest`
- **THEN** the deterministic health pass MUST report it as a hygiene finding
- **AND** the target MUST NOT resolve on the strength of that record

#### Scenario: A pinned target is lexically malformed
- **WHEN** a marker names a `target=pinned:…` value that is not exactly two `[a-z0-9]+(-[a-z0-9]+)*` components separated by one `/`
- **THEN** the deterministic health pass MUST report it as a malformed pinned target
- **AND** the pass MUST NOT construct a pin-record path, perform a pin lookup, or read any file for that value

#### Scenario: A pin record's capability enumeration is malformed
- **WHEN** a live marker names `target=pinned:<pin-id>/<capability>` and the record for `<pin-id>` carries a `capabilities:` member that is not a NON-EMPTY sequence of well-formed capability names, an empty sequence among those shapes
- **THEN** the deterministic health pass MUST report a malformed-enumeration finding against that pin record
- **AND** that pinned target MUST NOT resolve while the enumeration is malformed
- **AND** the pass MUST NOT treat the malformed member as an absent enumeration
- **AND** the pass MUST NOT be required to scan pin records that no live marker names: this obligation is reached through the marker

#### Scenario: A pin record named by a marker cannot be read
- **WHEN** a live marker names `target=pinned:<pin-id>/<capability>` and the record for `<pin-id>` exists but is not readable as a mapping carrying a `kind` — invalid YAML, a non-mapping document, or no `kind` member
- **THEN** the deterministic health pass MUST report it as a hygiene finding against that pin record
- **AND** the target MUST NOT resolve
- **AND** the pass MUST complete rather than abort

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
