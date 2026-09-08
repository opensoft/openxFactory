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

Where an authorized act moves the bytes OR THE PATH of the target
`custody.locator` names, the instrument SHALL record that fact in a SIBLING of
`custody` — `custody_rederivations`, an ordered array — and never inside
`custody` itself, whose closure exists so that no property can hold the signed
original's content. Each entry SHALL be closed (`additionalProperties: false`)
and SHALL carry all of: the time it was recorded; the commit at which the
target changed; the LOCATOR THE TARGET WAS AT BEFORE that commit and the LOCATOR
IT IS AT AFTER it (equal when the target did not move); the digest the link
starts from; the digest observed at that commit; the class of the difference;
the reason the act was authorized; a declared pointer to the record that
authorized ACCEPTING the divergence; and who recorded it. An entry missing the
authorizing reference or the recorder is nonconformant — an unattributed,
uncited acceptance is an unauthorized re-pin in a record's clothing.

The difference class and the reason SHALL each be a CLOSED enumeration —
minimally `path_only`, `header_only` and `content` for the class, and
`lifecycle_header_edit`, `archive_move` and `other_ruled_edit` for the reason —
so that a novel class arrives as a contract question rather than as a silently
admitted string. `path_only` exists because a pure relocation changes ZERO
bytes: it is not `header_only`, which requires a header line to have moved, and
calling it `content` would withhold the verdict forever on a target nobody
edited. `other_ruled_edit` is not a bare escape hatch: it carries the
same authorizing-reference obligation as every named member. The declared class
is itself re-derivable from the two commits it names, and a class contradicted
by the measured difference is a finding against the instrument.

A custody re-derivation record is NOT AN AMENDMENT of the instrument and SHALL
NOT transition its status. An amendment is a transition carrying a delta on the
instrument's own terms; a re-derivation records that the repository moved
underneath an unchanged pin, which changes nothing the parties agreed. An
executed instrument that takes a re-derivation entry stays `executed`, and one
moved to `amended` for that reason alone is nonconformant.

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

#### Scenario: A re-derivation does not amend the instrument

- **WHEN** an executed instrument takes a custody re-derivation entry
- **THEN** its status stays `executed` and no `amendments` entry is owed or written
- **AND** an instrument transitioned to `amended` solely for a custody re-derivation is nonconformant, because nothing the parties agreed has changed

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

**Resolution is declared, never guessed.** `custody.locator` is OPAQUE to this
contract and is NOT a path. A repository that holds instruments SHALL DECLARE a
CUSTODY STORE MAPPING that resolves a locator to a retrievable target, and every
re-derivation leg below is evaluated through that declared mapping. A locator a
checker cannot resolve under the declared mapping is a REFUSAL and never a pass;
a checker that resolves a locator by inferring a path the mapping does not
define is nonconformant, because an inferred rewrite can manufacture agreement
between a pin and a file nobody pinned.

**Direct.** The instrument declares no re-derivations (the array is absent or
empty) AND the target resolved from `custody.locator` hashes at HEAD to
`custody.sha256`.

**Chained.** With the declared entries read in order as `e₁…eₙ`, ALL of the
following hold:

- `e₁`'s starting digest equals `custody.sha256`, and `e₁`'s starting locator
  equals `custody.locator` — the chain is anchored to the executed pin AND to
  the executed pointer, and to nothing else;
- every later entry's starting digest equals its predecessor's observed digest,
  and its starting locator equals its predecessor's observed locator — the chain
  has no gap in either the bytes or the path;
- for EVERY entry, the target resolved from that entry's STARTING locator hashes
  at that entry's commit's PARENT to the entry's starting digest, and the target
  resolved from that entry's OBSERVED locator hashes at that entry's commit to
  the entry's observed digest — so a move is re-derived AT BOTH PATHS, each on
  the side of the commit where that path is the live one;
- every entry's commit is an ANCESTOR of the next entry's commit, and the last
  entry's commit is an ANCESTOR of HEAD — the chain lies on the history that
  actually leads to HEAD;
- the target resolved from the LAST entry's observed locator hashes at HEAD to
  the last entry's observed digest — the chain terminates where the repository
  actually is;
- the entries' recorded times do not decrease in declared order.

Any other outcome is NOT CURRENT. In particular a first entry whose starting
digest or starting locator is not the pin's, a broken link between consecutive
entries, a HEAD digest matching no terminus, a locator pair that resolves at
neither path, a commit that is not an ancestor of HEAD, an unreachable or absent
commit, a target absent at a commit's parent, and a rewritten history are each a
REFUSAL — never an admission — because each means the checker cannot see the
evidence, and converting "cannot tell" into "verified" is the exact failure the
record exists to prevent. The record is an INDEX INTO EVIDENCE and never a
substitute for it.

**THE DIFFERENCE CLASSES ARE DEFINED HERE, AND EACH CARRIES ITS CURRENCY
CONSEQUENCE.** The class is a claim about the two sides of one commit, and it is
RE-DERIVABLE from the record's own fields plus the repository:

- **`path_only`** — the target's bytes at (`commit^`, starting locator) and at
  (`commit`, observed locator) are IDENTICAL; only the locator changed. An
  entry declaring `path_only` whose two digests differ is REFUSED.
- **`header_only`** — the difference adds, removes or rewrites lifecycle-header
  lines and changes NO OTHER BYTE. An entry declaring `header_only` whose
  measured difference touches a non-header byte is REFUSED.
- **`content`** — anything else.

**Currency consequence, per class:** a `path_only` or a `header_only` entry MAY
reach CURRENT when every leg above re-derives. A `content` entry SHALL NOT, even
when every digest leg re-derives: a content divergence means the referent of a
signed original moved, which is grounds for RE-EXECUTION rather than for
recording. The verdict is WITHHELD — a THIRD OUTCOME distinct from current and
from refused — pending that act. Recording-and-accepting is available for a
divergence that changed no content, which is the only form the governing ruling
chose it for.

**WITHHELD IS REPRESENTED, NOT MERELY MANDATED.** Because the class is
record-derivable, the CANONICAL NEUTRAL VALIDATOR SHALL compute and report
withholding as a NAMED OUTCOME of its own — never as a pass, and never as a
plain error, since the record is correct and it is the INSTRUMENT that needs
attention. The consuming repository's custody-digest check SHALL PROPAGATE a
withheld verdict and SHALL NOT upgrade it to a pass on the strength of its own
re-derivation succeeding: the digests re-deriving is exactly the condition under
which withholding applies.

The obligation is SPLIT and the split SHALL be explicit rather than inferred.
The canonical neutral validator SHALL check every leg derivable from the
record's own bytes — the anchor to the pin AND to the pin's locator, the linkage
between entries in BOTH digest and locator, the declared order, the closed
enumerations, the closed entry shape, that no entry's digest has been written
back into `custody.sha256`, that a `path_only` entry's two digests are equal,
and the WITHHELD outcome for any `content` entry — and SHALL NOT attempt the git
re-derivation, because it is network-free, reads one repository, and the targets
live in consuming repositories. `ruling_ref` is likewise a DECLARED POINTER that
no checker at either level resolves. The re-derivation legs SHALL be performed
by the consuming repository's custody-digest check, where the target's bytes and
history are, and a repository whose instruments declare `custody_rederivations`
SHALL OPERATE such a check — a re-derivation rule no running code performs is a
convention, not a contract. Neutral validation passing is therefore NOT a
statement that a pin is current, and SHALL NOT be reported as one.

#### Scenario: A direct pin verifies with no chain

- **WHEN** an instrument declares no re-derivations and the target resolved from its `custody.locator` hashes at HEAD to `custody.sha256`
- **THEN** custody is current
- **AND** no entry is owed, and writing one would be a false record of an event that did not occur

#### Scenario: An unbroken chain is admitted, link by link

- **WHEN** an instrument's chain anchors to the pin and its locator, each link starts where its predecessor observed, every link re-derives at its commit and at that commit's parent, every commit is an ancestor of the next and of HEAD, and HEAD hashes to the last observed digest
- **THEN** custody is current
- **AND** the admission cites the commits and locators it re-derived, so any reader can repeat the measurement

#### Scenario: A path move is re-derived at both paths

- **WHEN** an authorized act moves the target to a new path, so the entry's starting and observed locators differ and its two digests are equal
- **THEN** the entry declares `diff_class: path_only`, the check resolves the starting locator at the commit's parent and the observed locator at the commit, and admits the link when each hashes to its declared digest
- **AND** an archive move is admissible for exactly this reason: the target is absent at the new path before the commit and absent at the old path after it, so a single-locator rule could never admit one

#### Scenario: A path_only entry whose digests differ is refused

- **WHEN** an entry declares `diff_class: path_only` and its starting and observed digests are not equal
- **THEN** the check refuses, because bytes changed and the class says none did
- **AND** the entry is not silently re-classified, since the class a record declares is the claim under review

#### Scenario: A header_only claim contradicted by the diff is refused

- **WHEN** an entry declares `diff_class: header_only` and the measured difference between its two sides touches a byte outside the lifecycle-header lines
- **THEN** the check refuses and names the contradicting difference
- **AND** the entry cannot reach CURRENT on a false classification, because the class is what decides whether currency is available at all

#### Scenario: A locator pair that resolves at neither path is refused

- **WHEN** an entry's starting locator does not resolve at the commit's parent, or its observed locator does not resolve at the commit, under the declared custody store mapping
- **THEN** the check refuses and names the locator and the commit it could not resolve it at
- **AND** it does not search for a path that would resolve, because a rewrite the mapping does not define can manufacture agreement with a file nobody pinned

#### Scenario: A content-class divergence withholds the verdict

- **WHEN** an entry declares `diff_class: content` and every internal leg is sound
- **THEN** the canonical neutral validator reports WITHHELD as a named outcome of its own — not a pass and not a plain error, because the record is correct and the instrument is what needs attention
- **AND** the instrument is due for re-execution, because a moved referent is not something a record of the move can repair

#### Scenario: A consumer gate propagates a withheld verdict and never upgrades it

- **WHEN** the consuming repository's custody-digest check re-derives every leg of a chain whose last entry declares `diff_class: content`
- **THEN** it reports WITHHELD, propagating the neutral outcome
- **AND** it MUST NOT report the pin current on the strength of its own re-derivation succeeding, because successful re-derivation is precisely the condition under which withholding applies

#### Scenario: A broken link is refused, not repaired

- **WHEN** one entry's starting digest does not equal the previous entry's observed digest
- **THEN** the check refuses and names the entry and the two digests
- **AND** it does not fall back to comparing HEAD against the last observed digest, because a chain whose middle is fiction is not evidence of anything

#### Scenario: A chain that does not anchor to the pin is refused

- **WHEN** the first entry's starting digest is any value other than `custody.sha256`, or its starting locator is any value other than `custody.locator`
- **THEN** the check refuses
- **AND** an instrument cannot acquire a new anchor, in bytes or in path, by declaring one

#### Scenario: A chain on a commit that is not an ancestor of HEAD is refused

- **WHEN** an entry's commit is reachable in the repository but is not an ancestor of the next entry's commit, or the last entry's commit is not an ancestor of HEAD
- **THEN** the check refuses
- **AND** a HEAD digest that happens to equal the last observed digest does not rescue it, because agreement reached off the history leading to HEAD is coincidence and not derivation

#### Scenario: A HEAD digest matching no terminus is refused

- **WHEN** every link re-derives but the target at HEAD hashes to neither the last entry's observed digest nor anything else the chain declares
- **THEN** the check refuses and reports that the chain does not terminate at the repository's current state
- **AND** the instrument is owed a further entry or a ruling, not an admission

#### Scenario: Entries out of recorded-time order are refused

- **WHEN** an entry's recorded time precedes its predecessor's
- **THEN** the check refuses
- **AND** the declared order is the chain's order, so a record whose own timestamps contradict it cannot be read as evidence of a sequence

#### Scenario: A chain that cannot be re-derived is refused, never admitted

- **WHEN** a declared commit is unreachable, the target is absent at a declared commit or its parent, or history has been rewritten under the chain
- **THEN** the check refuses and reports that the evidence could not be re-derived
- **AND** it does not admit the chain on its internal consistency alone, and does not downgrade the outcome to a warning

#### Scenario: The neutral pass is not a currency claim

- **WHEN** the canonical neutral validator passes an instrument carrying a re-derivation chain
- **THEN** it has checked anchoring, linkage in digest and locator, order, enumerations, entry closure, the unmoved pin, `path_only` digest equality and any withheld outcome, and nothing about the target's bytes
- **AND** the currency verdict belongs to the consuming repository's custody-digest check, which the repository declaring `custody_rederivations` is obliged to operate
