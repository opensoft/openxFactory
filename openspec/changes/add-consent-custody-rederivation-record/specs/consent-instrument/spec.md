# consent-instrument

## MODIFIED Requirements

### Requirement: The Signed Original Never Enters A Product Repo
The signed original SHALL be referenced only by opaque locator plus
sha256 (the document-cataloging custody pattern); embedding original
content in a product repo is nonconformant, while record-INSTANCE
placement (repo tenant tree vs governed store) is declared domain policy
driven by data sensitivity.

The `custody` object SHALL remain closed to exactly `locator` and `sha256`, and
`custody.sha256` — the pin — SHALL NOT be rewritten once the instrument is
executed. The pin is the half of the custody pair that proves the pointed-at
original; rewriting it to match a moved target destroys the only evidence that a
divergence occurred while producing a record that verifies.

Where an authorized act moves the bytes of the target `custody.locator` names,
the instrument SHALL record that fact in a SIBLING of `custody` —
`custody_rederivations`, an ordered array — and never inside `custody` itself,
whose closure exists so that no property can hold the signed original's content.
Each entry SHALL be closed (`additionalProperties: false`) and SHALL carry all
of: the time it was recorded; the commit at which the target's bytes changed;
the digest the link starts from; the digest observed at that commit; the class
of the difference; the reason the act was authorized; a declared pointer to the
record that authorized ACCEPTING the divergence; and who recorded it. An entry
missing the authorizing reference or the recorder is nonconformant — an
unattributed, uncited acceptance is an unauthorized re-pin in a record's
clothing.

The difference class and the reason SHALL each be a CLOSED enumeration —
minimally `header_only` and `content` for the class, and
`lifecycle_header_edit`, `archive_move` and `other_ruled_edit` for the reason —
so that a novel class arrives as a contract question rather than as a silently
admitted string. `other_ruled_edit` is not a bare escape hatch: it carries the
same authorizing-reference obligation as every named member. The declared class
is itself re-derivable from the two commits it names, and a class contradicted
by the measured difference is a finding against the instrument.

The growth is ADDITIVE: an instrument that declares no re-derivations remains
valid unchanged, and the record envelope's `schema_version` does not move.

#### Scenario: Custody is a pointer, not a payload

- **WHEN** an instrument record is committed
- **THEN** it carries locator + sha256 for the signed original and no
  original content
- **AND** Medx's governed-store mandate and Ledgerx's tenant-tree
  placement both conform because each is declared domain policy

#### Scenario: A re-derivation is recorded beside custody, never inside it

- **WHEN** a ruled edit moves the bytes of the target an executed instrument's `custody.locator` names, leaving the content unchanged
- **THEN** the instrument records the divergence as an entry in the sibling `custody_rederivations` array
- **AND** `custody` still carries exactly `locator` and `sha256`, and an equivalent history written inside `custody` is nonconformant

#### Scenario: The executed pin is never rewritten to match the moved target

- **WHEN** an executed instrument's target no longer hashes to `custody.sha256`
- **THEN** the repair records the divergence and leaves `custody.sha256` verbatim
- **AND** an instrument whose pin was rewritten to the observed digest is nonconformant even though it now verifies

#### Scenario: An unattributed or uncited acceptance is refused

- **WHEN** a re-derivation entry omits the reference to the record that authorized accepting the divergence, or omits who recorded it
- **THEN** the entry is nonconformant
- **AND** the omission is refused at the contract rather than reported as advisory

#### Scenario: An unknown class or reason is refused at the contract

- **WHEN** a re-derivation entry declares a difference class or a reason outside the closed enumerations
- **THEN** the record is refused
- **AND** admitting a new member is a contract change, never a value an author may coin

#### Scenario: An instrument that declares no re-derivations is unaffected

- **WHEN** an existing executed instrument carries no `custody_rederivations` array
- **THEN** it remains valid under the grown contract with no edit
- **AND** the growth is additive, so no conformance declaration and no record envelope version moves

## ADDED Requirements

### Requirement: Custody Currency Is Re-Derived From Git History Or Refused
An instrument's custody SHALL be treated as CURRENT only when one of two
conditions holds, and a checker that cannot re-derive the evidence SHALL REFUSE
rather than admit.

**Direct.** The instrument declares no re-derivations (the array is absent or
empty) AND the target named by `custody.locator` hashes at HEAD to
`custody.sha256`.

**Chained.** With the declared entries read in order as `e₁…eₙ`, ALL of the
following hold:

- `e₁`'s starting digest equals `custody.sha256` — the chain is anchored to the
  executed pin and to nothing else;
- every later entry's starting digest equals its predecessor's observed digest —
  the chain has no gap;
- for EVERY entry, the target hashes at that entry's commit's PARENT to the
  entry's starting digest, and at that entry's commit to the entry's observed
  digest — every link is re-derived from git history rather than trusted on the
  record's own word;
- the target hashes at HEAD to the LAST entry's observed digest — the chain
  terminates where the repository actually is;
- the entries' recorded times do not decrease in declared order.

Any other outcome is NOT CURRENT. In particular a first entry whose starting
digest is not the pin, a broken link between consecutive entries, a HEAD digest
matching no terminus, an unreachable or absent commit, a target absent at a
commit's parent, and a rewritten history are each a REFUSAL — never an
admission — because each means the checker cannot see the evidence, and
converting "cannot tell" into "verified" is the exact failure the record exists
to prevent. The record is an INDEX INTO EVIDENCE and never a substitute for it.

The obligation is SPLIT and the split SHALL be explicit rather than inferred.
The canonical neutral validator SHALL check every leg derivable from the
record's own bytes — the anchor to the pin, the linkage between entries, the
declared order, the closed enumerations, the closed entry shape, and that no
entry's digest has been written back into `custody.sha256` — and SHALL NOT
attempt the git re-derivation, because it is network-free, reads one repository,
and the targets live in consuming repositories. The re-derivation legs SHALL be
performed by the consuming repository's custody-digest check, where the target's
bytes and history are. Neutral validation passing is therefore NOT a statement
that a pin is current, and SHALL NOT be reported as one.

#### Scenario: A direct pin verifies with no chain

- **WHEN** an instrument declares no re-derivations and its locator target hashes at HEAD to `custody.sha256`
- **THEN** custody is current
- **AND** no entry is owed, and writing one would be a false record of an event that did not occur

#### Scenario: An unbroken chain is admitted, link by link

- **WHEN** an instrument's chain anchors to the pin, each link starts where its predecessor observed, every link re-derives at its commit and at that commit's parent, and HEAD hashes to the last observed digest
- **THEN** custody is current
- **AND** the admission cites the commits it re-derived, so any reader can repeat the measurement

#### Scenario: A broken link is refused, not repaired

- **WHEN** one entry's starting digest does not equal the previous entry's observed digest
- **THEN** the check refuses and names the entry and the two digests
- **AND** it does not fall back to comparing HEAD against the last observed digest, because a chain whose middle is fiction is not evidence of anything

#### Scenario: A chain that does not anchor to the pin is refused

- **WHEN** the first entry's starting digest is any value other than `custody.sha256`
- **THEN** the check refuses
- **AND** an instrument cannot acquire a new anchor by declaring one

#### Scenario: A chain that cannot be re-derived is refused, never admitted

- **WHEN** a declared commit is unreachable, the target is absent at a declared commit or its parent, or history has been rewritten under the chain
- **THEN** the check refuses and reports that the evidence could not be re-derived
- **AND** it does not admit the chain on its internal consistency alone, and does not downgrade the outcome to a warning

#### Scenario: The neutral pass is not a currency claim

- **WHEN** the canonical neutral validator passes an instrument carrying a re-derivation chain
- **THEN** it has checked anchoring, linkage, order, enumerations, entry closure and the unmoved pin, and nothing about the target's bytes
- **AND** the currency verdict belongs to the consuming repository's custody-digest check, which re-derives every link where the target lives
