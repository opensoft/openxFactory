# ideation-dashboard Specification

## Purpose

Define the dashboard as a generated projection, never a source of truth: one
deterministic generator scans a single repository at a single ref and emits
the schema-versioned `ideation-dashboard-snapshot` that every renderer reads
through the snapshot index, and when the rendered view disagrees with the
repository it is the view that is regenerated. Build the human's working
surfaces on that one snapshot — the six-column docs-first realization funnel
and its secondary views, the cluster canvas, the keyword-lens set builder,
the workbench's temporary reference sets, the drill-down explorer and
read-only viewer, and the repository / project / project-group navigation the
project register resolves. Fix the interactivity boundary as the capability's
spine: the generator, renderers, workbench actions and every agent path are
non-mutating over source documents and may never execute a lifecycle gate,
while humans create, edit and gate through the console, branch sessions and
the doxBench editor, each act producing the same governed artifacts as the
manual path plus a recorded action, and kickoff dispatching the ratified
change's next step under the workflow-gate contract rather than running it
here. Keep the model-facing work equally bounded — grounded chat turns and
distilled abstracts are explicitly invoked, session-local, reached through
one narrow provider boundary with broker-minted tokens, and never snapshot
fields.

## Requirements

### Requirement: The doxBench chat-turn v1 envelope family is REMOVED at contract-v3.0
The three doxBench chat-turn v1 envelope kinds — `workbench-chat-turn`, `workbench-chat-turn-success` and `workbench-chat-turn-failure` — SHALL be removed at `contract-v3.0`, together with their `$defs` in `contracts/schemas/xfactory-workbench-chat-turn.schema.yaml`, their entries in that file's top-level `oneOf`, the file's whole `deprecated_envelopes` block, their kind constants and dispatch arms in the runtime and the contract validator, their packaged instances, and the committed byte-identity baseline that exists to prove the deprecated bytes never moved.

THE PHASING IS SERVED AND MEASURED. The family was deprecated at
`contract-v1.34` with the deprecation stated MACHINE-READABLY — a top-level
`deprecated_envelopes` block carrying `superseded_by`, `deprecated_in` and
`removal_target` per kind — and the contract validator has WARNED on every
instance of it since, which is the only one of issue #522's three entries whose
warning actually fires. Thirteen minors and one major have passed. The Breaking
class's *"at least one full minor release where the old shape produced
deprecation warnings"* is discharged many times over, so no new deprecation
window is owed.

THE BASELINE TEST RETIRES WITH THE FAMILY, AND ITS RETIREMENT IS NAMED RATHER
THAN PERFORMED SILENTLY. The committed baseline asserts that the v1 `$defs` and
the shared definitions they `$ref` are byte-identical to their `contract-v1.31`
bytes. That assertion exists to protect a shape consumers are pinned to; when
the shape leaves the published surface, the assertion has no subject. Deleting
it as an incidental casualty of a schema edit would be indistinguishable from
deleting it because it had become inconvenient, so the removal states what the
test was for and why it ends.

THE SHARED DEFINITIONS DO NOT LEAVE WITH THE ENVELOPES. `content_hash`,
`confined_path`, `scope_key`, `buffer_state`, `transcript_turn` and
`typed_proposal` are `$ref`-ed by the v1 envelopes AND reachable from the
surviving family; only definitions reachable from the removed envelopes ALONE
may be removed, and each such removal is measured from the surviving family's
own reference closure rather than assumed.

#### Scenario: A v2 turn meets the new major
- **WHEN** a client submits a turn in the surviving `workbench-chat-turn-v2` family at `contract-v3.0`
- **THEN** it MUST validate and be served exactly as before, with no field added, removed or renamed by this removal
- **AND** the surviving family's reference closure MUST still resolve, every shared definition it reaches being retained

#### Scenario: A v1 turn meets the new major
- **WHEN** a client submits a turn carrying one of the three removed v1 kinds against a runtime at `contract-v3.0`
- **THEN** it MUST be refused, no schema branch, no kind constant and no dispatch arm remaining that accepts it
- **AND** the refusal MUST be answered under the unrecognized-kind rule below, never by a surviving copy of the removed family

#### Scenario: A consumer pinned below the removal validates a v1 instance
- **WHEN** a consumer pinned below `contract-v3.0` validates a v1 chat-turn instance against the schema bytes it pins
- **THEN** it MUST still validate, and MUST still receive the deprecation warning it received before, because compatibility flows from the consumer and no new release reaches backwards into an old pin

#### Scenario: The packaged corpus is retired with the family
- **WHEN** the removal lands
- **THEN** every packaged instance declaring a removed kind MUST be retired with it — including the NEGATIVE fixtures, which outnumber the positive ones
- **AND** any refusal case those negatives covered that has no equivalent in the surviving family's corpus MUST be either re-expressed against the surviving family or recorded as a stated coverage loss, never dropped in silence

#### Scenario: The machine-readable deprecation block is removed
- **WHEN** the three kinds leave the schema
- **THEN** the file's `deprecated_envelopes` block MUST be removed with them, because a block declaring the deprecation of kinds the file no longer defines names nothing
- **AND** the deprecation record MUST NOT vanish with it: the entry MUST move to `docs/contract-versioning-policy.md` § Deprecations Executed, where a consumer upgrading across the removal can still read the migration path

#### Scenario: The validator's deprecation warnings after the removal
- **WHEN** the contract validator is run over a clean checkout at `contract-v3.0`
- **THEN** it MUST report ZERO chat-turn deprecation warnings, where a default run before the removal reported four, all naming a spent removal target
- **AND** `--strict` MUST stop failing on the packaged chat-turn fixtures for that reason

#### Scenario: Prose that survives its own subject
- **WHEN** documentation states that a condition holds "until the removal target `contract-v2.0` retires the fixtures with the family"
- **THEN** it MUST be repaired in the same cut as the removal, that sentence having been false since `contract-v2.0` shipped on 2026-08-27 and nothing having noticed

> **ERRATUM, 2026-09-16 — NOT PART OF THE RATIFIED REQUIREMENT ABOVE, AND THE
> REQUIREMENT IS UNEDITED.** One clause of "THE SHARED DEFINITIONS DO NOT LEAVE
> WITH THE ENVELOPES" was measured FALSE by this requirement's own realization:
> `typed_proposal` is **not** reachable from the surviving `-v2` family. The
> widened family restates the shape as `keyed_typed_proposal` and never points at
> `typed_proposal`, so the reference closure puts it outside. The measurement is
> `retire-doxbench-chat-turn-v1` `tasks.md` § 2.1 — *"the premise is false for one
> of the six"* — and the disposition is that packet's § 6.8, added at the
> `contract-v3.0` cut for this purpose.
>
> **THE OUTCOME THE SENTENCE ASSERTS STILL HOLDS; ITS REASON DOES NOT.**
> `typed_proposal` did not leave, and is **RETAINED, unreferenced, with the
> reason recorded** — not because the surviving family reaches it, but because
> removing a definition from a published contract file that no deprecation entry
> announced and no minor warned on is what § Change Classes *Breaking (major)*
> forbids at this major. A removal owes its own deprecating minor first. The
> decision stands in `contracts/CHANGELOG.md` § `contract-v3.0` and in the
> Executed row of `docs/contract-versioning-policy.md`.
>
> **WHY THE CLAUSE STANDS UNEDITED.** It is ratified text, carried here by the
> archive act that closed `split-opendox-two-layer-product` § 6.2, and a closure
> is not a licence to rewrite what was ratified. It also caught its own error:
> the requirement demands that each removal be *"measured from the surviving
> family's own reference closure rather than assumed"*, and applying that rule is
> exactly what falsified the list beside it. The rule is sound; one of its
> examples was not, and that is recorded here so a reader of canon meets the
> correction where the claim is, rather than two directories away.
>
> **AND ONE SCENARIO OF THIS REQUIREMENT IS BOUNDED BY THE REMOVAL THIS CUT
> PERFORMS.** *An older client sends a released v1 turn* says such a turn "MUST
> still validate and MUST still be served". That held for the whole life of the
> deprecation and is FALSE from `contract-v3.0`: the changelog's own Executed row
> records the doxBench chat-turn **v1** family as removed there, and that "a v1
> instance is refused only from `contract-v3.0`". The scenario is RATIFIED and is
> NOT edited; it is to be read as bounded to the window it was written in — after
> `contract-v1.34` deprecated the family, before `contract-v3.0` removed it.
>
> **AND ONE COUNT IN THE PROSE ABOVE IS SHORT.** "Thirteen minors and one major
> have passed" counts the v1 line alone. What governs the count is the TAG, not
> the changelog heading: `docs/contract-versioning-policy.md`
> § *`contract-v2.6` — Instance Six* rules that **"a bundle that can never be
> tagged is not thereby released; it is permanently unreleased"**. Measured at
> the source — `git ls-remote --tags origin 'contract-v*'`, 56 tags — the
> PUBLISHED run after the deprecating `contract-v1.34`, up to and including the
> removal at `contract-v3.0`, is `v1.35`–`v1.47` (THIRTEEN minors),
> `contract-v2.0` (major), `v2.1`–`v2.5` (FIVE further minors) and
> `contract-v3.0` (this cut's major): **TWENTY published releases** between the
> deprecation and the removal. Two numbers inside that span are NOT releases and
> are not counted — `contract-v2.6`, which has a changelog heading and no tag and
> can never have one (*SPENT, NEVER VERIFIABLE, NEVER PUBLISHED, SUPERSEDED*),
> and `contract-v2.7`, which this cut's own § *The number, FRESH-COUNTED at the
> cut, and why it is a MAJOR rather than `contract-v2.7`* records as declined.
> The discharge the sentence claims — *"at
> least one full minor release where the old shape produced deprecation
> warnings"* — is satisfied many times over on either reading, which is why the
> ratified sentence stands unedited and the fuller measurement is recorded here.
>
> (Both found by Copilot's review on PR #1066 at `c431a3e3`. The count took
> THREE passes to get right, and every wrong pass counted a changelog heading as
> a release: Copilot said FIVE v2 minors, which the tags say is correct; this
> erratum first said SEVEN and invented a `contract-v2.7`; its second pass said
> SIX by counting the unpublishable `contract-v2.6`, which Copilot caught at
> `91644a2d` against the versioning policy. The rule the erratum kept
> re-learning is its own: re-measure at the source — here the tags on the
> remote — rather than count a document that names numbers it never published.)

### Requirement: An unrecognized chat-turn kind is refused in the SURVIVING family, never coerced into a removed one
An unrecognized or absent chat-turn `kind` SHALL be answered in the SURVIVING envelope family's failure shape, carrying an explicit unknown-kind error code, and MUST NOT be coerced into any family the release has removed; where the request carries no wire-valid turn identity, the existing pre-identity refusal shape SHALL be used unchanged, because the surviving failure envelope requires a `client_turn_id` and no identity may be invented to obtain one.

THIS IS A REDESIGN, NOT A DELETION, AND THE DIFFERENCE IS THE WHOLE POINT. While
two families were served, the route read the family off the request's own `kind`
and answered in the family the request arrived in — with the v1 family as the
DEFAULT for anything unrecognized, on the stated reason that *"a request that
never named a family it could be answered in gets the posture it would have got
before this release"*. That reason dies with v1: after the removal the default
names a family that does not exist, and a realization that merely deleted the v1
arm would leave the `else` branch dispatching to a parser and an envelope builder
that are gone.

THE SURVIVING FAILURE ENVELOPE CAN CARRY THE CODE, AND THAT IS A MEASUREMENT.
The released `workbench-chat-turn-v2-failure` shape requires
`schema_version`, `kind`, `client_turn_id`, `error` and `message`, and constrains
`error` only by a lowercase-identifier PATTERN — no enum at the schema layer, and
the delegated validator that judges it applies no code vocabulary either. A new
explicit code is therefore contract-permitted without widening anything. The
CLOSED list is the server's own error catalog, which maps code to status and to
a fixed message; the new code is registered there in the same cut, or the refusal
path raises instead of refusing.

THE ALTERNATIVE IS RECORDED RATHER THAN LEFT UNSAID. The other honest posture is
to refuse every unrecognized kind OUTSIDE any contract envelope, in the
pre-identity shape, whatever identity the request supplied. It is simpler and
asserts less. It is not taken because it discards an identity the request DID
supply, hands the client a body carrying no `kind` its own dispatch can route,
and makes the refusal invisible to the contract corpus — three costs paid to
avoid registering one error code.

#### Scenario: An unrecognized kind arrives with a wire-valid turn identity
- **WHEN** a chat-turn request carries a `kind` that is not the surviving family's request kind, and a wire-valid `client_turn_id`
- **THEN** it MUST be refused in the surviving family's failure envelope, carrying an explicit unknown-kind error code and that turn identity
- **AND** the envelope MUST be self-validated against the released schema before it is sent, exactly as every other refusal in this family is

#### Scenario: An unrecognized kind arrives with no wire-valid turn identity
- **WHEN** a chat-turn request carries an unrecognized `kind` and no wire-valid `client_turn_id`
- **THEN** the existing pre-identity refusal shape MUST be used, unchanged
- **AND** no turn identity MUST be invented in order to reach the contract envelope

#### Scenario: A realization deletes the fallback instead of redesigning it
- **WHEN** a realization removes the v1 family and leaves the kind-discrimination default naming it
- **THEN** it MUST be rejected — the default would dispatch to a parser and an envelope builder that no longer exist, turning an unrecognized kind into a server fault rather than a refusal

#### Scenario: The new code is not registered
- **WHEN** an unknown-kind code is answered without being registered in the server's closed error catalog
- **THEN** the refusal path raises instead of refusing, so the registration MUST land in the same cut as the code

#### Scenario: A removed kind is treated as merely unrecognized
- **WHEN** the unrecognized kind is one of the three the release removed
- **THEN** it MUST take exactly this path and no other, because after the removal a retired kind and a kind that never existed are the same fact about the wire
