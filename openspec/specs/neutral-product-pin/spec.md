# neutral-product-pin Specification

## Purpose

Govern openxFactory's consumption of an EXTERNAL neutral product, the
direction in which it is the consumer rather than the publisher: the pin
at `contracts/<product>-pin.yaml` carrying commit, `revision_kind`,
per-file `sha256` and `pinned_by_commit_only` — never a tag and never a
range — and the fail-closed behaviour that turns an unanswerable pin
question into a refusal naming its remedy instead of an implicit pass.
The capability makes which reader ran an auditable digest: a required
check invokes the pinned validator and the pinned reader from the pinned
checkout, verifies the pin's digests before reading, refuses a missing
scan target, and resolves the consuming repository's nested checkout ahead
of any other reachable one. It also carries the reverse direction — a
neutral product may vendor exactly one digest-pinned openxFactory contract
as a consumed, never owned, manifest member — and makes repointing the
reader while editing what it reads a human-only act.

## Requirements

### Requirement: An external neutral product is pinned by commit and digest, never by tag
`openxFactory` SHALL declare its consumption of an EXTERNAL neutral product in
`contracts/<product>-pin.yaml`, REUSING `kind: pinned_contract_manifest`
unchanged, and that pin SHALL carry the product's COMMIT, its `revision_kind`, a
per-file `sha256` for every artifact the product's own manifest digests per file,
and `pinned_by_commit_only:` for every artifact the product content-addresses by
commit alone. The pin GRAMMAR is not new — it is the ratified
`pinned_contract_manifest` shape already realized twice under
`repo-boundary-governance`'s per-product requirements
(`installs/keycloak-install/config/contracts/identity-brokering/manifest.yaml:1-20,45-58`
and `installs/openxpki-install/config/contracts/trust-anchor/manifest.yaml:55`);
what is new is only that `openxFactory` is the CONSUMER. A TAG-ONLY pin SHALL be
refused in that shape's own words, "a tag can be moved": a tag MAY be recorded
beside the commit as a human-readable label, never as the thing being trusted,
and a pin SHALL NOT express a version RANGE.

#### Scenario: A pin declares a tag and no commit
- **WHEN** a pin file names a release tag but no commit
- **THEN** the pin is refused, because a tag can be moved and a commit cannot

#### Scenario: The product digests only part of its release surface
- **WHEN** the product's manifest carries per-file digests for some artifacts and content-addresses the rest by commit
- **THEN** the pin carries per-file `sha256` for the former and `pinned_by_commit_only:` for the latter
- **AND** an artifact that appears in neither list is an undeclared consumption, not a permitted omission

#### Scenario: A pin expresses a range
- **WHEN** a pin expresses a version range or a moving reference
- **THEN** it is refused, because the moment a pin trusts a range the fail-closed property is gone

### Requirement: An unanswerable pin question refuses, and the refusal names its remedy
A consumer of a pinned neutral product SHALL FAIL CLOSED: an uninitialized
submodule, an unresolvable checkout, an absent pinned artifact, or a digest
disagreeing with the pin SHALL each produce a REFUSAL with a named exit, and
SHALL NOT resolve to an implicit pass, to "empty", or to a skip — an unreadable
surface must fail rather than degrade. Every such refusal SHALL carry a
REMEDIATION STRING naming the initializing command
(`git submodule update --init <product-dir>`) and the path of the
pin-resync runbook, so the exit is in the message rather than in tribal memory.

#### Scenario: The pinned submodule is uninitialized
- **WHEN** a tool needs a pinned artifact and the product's submodule has not been initialized in the checkout
- **THEN** the run refuses with a named exit
- **AND** the refusal names the init command and the pin-resync runbook's path

#### Scenario: A pinned digest has drifted
- **WHEN** a pinned artifact's recomputed `sha256` differs from the digest recorded in the pin
- **THEN** the run refuses on the request that first sees it, and no later step may treat the artifact as conformant

#### Scenario: A refusal carries no remediation
- **WHEN** a fail-closed path emits a refusal that does not name a command and a runbook
- **THEN** the refusal is itself a defect of this capability, because it tells the operator that something is wrong without telling them what to run

### Requirement: The consuming repository's pin is authoritative among reachable checkouts
A resolver SHALL prefer the pin recorded in the CONSUMING repository wherever more than one checkout of a pinned neutral product is reachable from a consuming tree, and that pin SHALL be authoritative;
and the aggregation's ROOT gitlink for a product `openxFactory` pins SHALL EQUAL
`openxFactory`'s NESTED gitlink commit, checked in the aggregation. Without this,
a walk-up resolver in a
consumer repository silently reads whichever checkout it meets first — the
aggregation root or the nested one — and only the nested one is governed by
`contracts/<product>-pin.yaml`.

#### Scenario: Two checkouts are reachable from one consumer
- **WHEN** a walk-up resolver in a consumer repository can reach both the aggregation's root checkout of the product and `openxFactory`'s nested checkout
- **THEN** it resolves the NESTED checkout, because that is the one the consuming repository's pin governs
- **AND** the candidate order is DECLARED in the consumer rather than left to whichever directory the walk meets first

#### Scenario: The root gitlink and the nested gitlink disagree
- **WHEN** the aggregation's root gitlink and `openxFactory`'s nested gitlink name different commits of the product
- **THEN** the aggregation's own check fails, because two answers to "which bytes are pinned" is no answer

#### Scenario: A resolver's candidate order is unstated
- **WHEN** a consumer resolves the product without a declared candidate order
- **THEN** the ambiguity is a defect, and the order is fixed nested-first in the consuming repository

### Requirement: A required check runs the pinned tool, at the pinned digest
A REQUIRED check that enforces a pinned product's rules SHALL invoke the PINNED
validator and the PINNED reader from the pinned checkout, and SHALL NOT invoke an
in-tree copy, a vendored duplicate or an unpinned installation, so that WHICH
READER RAN is an auditable digest rather than an assumption. The pin's digests
SHALL be verified BEFORE the pinned reader is invoked, by running code rather
than by a stated obligation, and the check's log SHALL name the pinned commit and
the governed surface it read.

#### Scenario: A required check runs an unpinned reader
- **WHEN** a required check invokes a reader that is not the one the pin names
- **THEN** the check does not satisfy the rule it claims to enforce, and the enforcement claim is UNMET

#### Scenario: The pinned reader runs before the pin is verified
- **WHEN** a required check invokes the pinned reader without first verifying the pin's per-file digests and its `pinned_by_commit_only:` set
- **THEN** the check is a green result over unverified bytes and is refused

#### Scenario: The check passes
- **WHEN** the required check reports green
- **THEN** its log names the pinned checkout's commit AND the governed artifact it read, so a green check whose log names neither is a vacuous pass

### Requirement: A pinned validator invoked with no scan target refuses
A required check that invokes a pinned validator WITHOUT a scan target SHALL
cause the validator to REFUSE rather than self-test, because a self-test that
opens no governed surface is a green check that verified nothing. The LITERAL
invocation string SHALL be pinned in a test in the consuming repository, and that
test's assertion SHALL be POSITIVE — that the intended governed surface WAS read
— never merely that an argument was present.

#### Scenario: The validator is invoked with no target
- **WHEN** a required check invokes the pinned validator with no positional scan target
- **THEN** the validator refuses with a named exit rather than reporting success over its own tree

#### Scenario: The scan target names the product instead of the consumer
- **WHEN** the scan target passed to the pinned validator is the product's own pinned directory rather than the consuming repository's root
- **THEN** the consuming repository's governed surface is never opened, and the check refuses

#### Scenario: No test pins the invocation
- **WHEN** the consuming repository carries no test asserting the required check's literal invocation and that the governed surface was read
- **THEN** nothing prevents a silent repoint to a target that reads nothing, and the enforcement claim is UNMET

### Requirement: Repointing the reader and editing what it reads is one human-only act
A pull request SHALL be HUMAN-ONLY where it changes a neutral product's PIN or its GITLINK **and** any file under the review-authority register's directory,
and SHALL NOT be clearable by a council or any other automated authority, because a
candidate could otherwise repoint the very reader that judges its own change. The
pin file and the gitlink SHALL therefore be named in the consuming repository's
merge-gate floor as never-clearable paths; where that floor's matcher is exact
set membership rather than a pattern, they SHALL be named LITERALLY, in the exact
stored form, with no leading or trailing separator.

#### Scenario: One pull request changes both the pin and the register
- **WHEN** one pull request changes the product pin or its gitlink AND any file under the review-authority register's directory
- **THEN** the pull request is human-only, because a candidate could otherwise repoint the very reader that judges its own change

#### Scenario: The floor names the register but not the pin
- **WHEN** a merge-gate floor protects the register file while naming neither the pin nor the gitlink
- **THEN** the floor has a gap and the gap is a finding, because the pin and the gitlink are what determine which reader runs

#### Scenario: The floor matches paths by exact set membership
- **WHEN** the floor's matcher is exact set membership over declared paths
- **THEN** the gitlink is named in its exact stored form, and a wildcard or a trailing separator SHALL NOT be relied on to cover it

### Requirement: A neutral product may vendor one openxFactory contract, and names the version it pins
A neutral product repository MAY keep a DIGEST-PINNED copy of ONE `openxFactory` contract that its own validator reads, and MUST identify the `openxFactory` contract version it pins —
mirroring
`openspec/specs/shared-contract-ownership/spec.md:27`, whose text is scoped to
INSTALL repositories ("an install repo needs a runtime adapter, generated client,
smoke fixture, or pinned schema copy") and therefore does not license this
reverse vendoring on its own. The vendored copy SHALL be registered in the
product's own `contracts/manifest.yaml` as a CONSUMED member and never as an
owned one — `compatibility: canonical_openxfactory_contract`, an `adapter_owner`
naming `openxFactory`, and a digest EQUAL to the pinned `openxFactory` row's — so
that `shared-contract-ownership:142`'s all-markers-together publisher test is met
in the product repository without it claiming ownership of an `openxFactory`
contract; and a CONSUMED member SHALL be excluded from the product's own release
surface and from that release's digests file.

#### Scenario: A product's validator reads an openxFactory schema
- **WHEN** a neutral product's validator needs an `openxFactory` schema to enforce its own vocabulary
- **THEN** the product keeps that schema as a digest-pinned vendored copy AND names the `openxFactory` contract version it pins

#### Scenario: A vendored copy is registered as owned
- **WHEN** a vendored foreign contract is registered as an OWNED manifest member of the product
- **THEN** the registration is false and refused, because the product publishes no `openxFactory` contract

#### Scenario: The product cuts a release bundle
- **WHEN** the product cuts a release and enumerates its release surface
- **THEN** a consumed member is excluded from that surface and from the release's `digests.yaml`, so the product never claims to release bytes it does not own

### Requirement: A vendored foreign contract is digest-verified before it is read
A neutral product repository that keeps a digest-pinned copy of an `openxFactory` contract SHALL VERIFY that copy against its own `contract_pin.yaml` BEFORE the copy is read, and an UNVERIFIABLE copy SHALL REFUSE the run.
PRESENCE IS NOT
IDENTITY: a file-existence check is not a verification, and the verifier SHALL
fail closed pre-sync on the house model — a recomputed digest can never equal an
empty recorded digest, so an empty or absent recorded digest is DRIFT and refuses
before any test runs.

#### Scenario: The validator only checks that the file exists
- **WHEN** a product's entry point checks only that the vendored contract's path is a file
- **THEN** the check is presence rather than identity, and this requirement is UNMET

#### Scenario: The vendored copy is mutated
- **WHEN** the vendored contract's bytes are changed without updating `contract_pin.yaml`
- **THEN** the verify step fails BEFORE the validator runs, and the run is red

#### Scenario: The recorded digest is empty
- **WHEN** `contract_pin.yaml` carries an empty or absent digest for the vendored copy
- **THEN** the verifier treats it as drift and refuses, rather than passing pre-sync

### Requirement: The pinned validator is the contract family's conformance validator from the major forward
The PINNED validator at the digest recorded in `contracts/<product>-pin.yaml` SHALL BE a contract family's conformance validator from the breaking MAJOR release forward, wherever that family's conformance validator MOVES to the neutral product repository that owns the family's shape,
invoked by the consuming
repository's required gate; and that move SHALL be NAMED as the
conformance-validator update `docs/contract-versioning-policy.md:250-255`
requires of a major, rather than left implied. The PRECEDING deprecation minor's
marker SHALL be MANIFEST-CARRIED, and the conformance validator SHALL NOT be
edited to emit that deprecation warning.

#### Scenario: A major removes a shape because the family moved
- **WHEN** a major release removes registered artifact rows from `openxFactory` because the family they belong to moved to its own repository
- **THEN** the policy's "update to the conformance validator" clause is discharged by the validator MOVING to the repository that owns the shape, and the change names that move as the discharge

#### Scenario: The deprecation minor's marker is proposed as a validator warning
- **WHEN** the preceding minor is asked to mark the relocating rows by making the conformance validator emit a warning
- **THEN** the marker is MANIFEST-carried instead, because a new warning reds a consumer that runs the validator `--strict`, is surfaced by no required check in the publisher, and edits a validator inside a move whose safety rests on an empty diff

#### Scenario: A consumer asks which validator is authoritative
- **WHEN** a consumer asks which validator adjudicates the family's conformance after the major
- **THEN** the answer is the validator at the digest recorded in the consuming repository's pin file, and not any copy still resident in the publisher's history

### Requirement: A consumption pin that another repository reads is a PUBLISHED contract member, adopted by pin-sync
A consumption pin SHALL be a PUBLISHED contract member wherever any repository
other than `openxFactory` is expected to read it: registered in
`contracts/manifest.yaml` with an `id`, its `path`, a `type`, its
`intended_consumers`, `adapter_owner: openxFactory`, and a `consumption_rule`
that states the checkout-at-the-pinned-ref recipe and forbids copying; and
indexed in `contracts/README.md` so a human reading the contract index finds it
where every other published contract is found. The pin is the file at
`contracts/<product>-pin.yaml`.

**REGISTRATION IS WHAT MAKES ADOPTION AUTOMATIC, AND THAT IS THE WHOLE REASON
FOR IT.** `contracts/manifest.yaml` is the register a cross-repository consumer
reads to know WHICH BYTES IT PINS. A consumer that advances `stack.yaml`'s
`xfactory.contract_ref` to a commit at or after the registration receives the
registered pin with the rest of the pinned tree, in its ordinary pin-sync, with
no per-repository act needed to LEARN that the pin exists. An UNREGISTERED pin
that consuming repositories nonetheless read is the inverse: a cross-repository
consumption that the register does not declare, discoverable only by a reader
who already knew the path — which is the state in which a pin can govern a
fleet while being invisible to the fleet's own index.

**PUBLISHING THE PIN IS NOT PUBLISHING THE PINNED PRODUCT, and the row SHALL
say so rather than leaving it to be inferred.** `openxFactory` publishes ITS OWN
CLAIM about which artifact adjudicates — the pin file — and does not thereby
own, publish, vendor or take responsibility for the product the pin names. The
product's ownership, its licence and its release cadence are unchanged by the
registration, and the row's `compatibility` and `adapter_owner` describe the
PIN.

**A CONSUMER GATES BY READING THE PIN FROM THE PINNED CHECKOUT, NEVER BY
COPYING IT.** A repository that carries an `xfactory:` stack pin SHALL, where it
gates on the pinned product, check `openxFactory` out at its own
`stack.yaml` `xfactory.contract_ref` and invoke the entrypoint the registered
pin names FROM THAT CHECKOUT. A copy of the pin taken into a consuming
repository is a SECOND pin that moves separately, which is the defect the pin
grammar exists to end; and a copy is not made lawful by being current on the day
it is taken.

**WHERE THE TWO GOVERNED ACTS ARE REACHED BY TWO DIFFERENT COMMANDS, THE
REGISTER SHALL NAME BOTH.** "Run it through the pinned entrypoint" is a claim
about which BYTES adjudicate, not about a single verb: a repository's published
adoption instructions SHALL name the ACTUAL command for each governed act they
cover, and SHALL NOT present one command as accepting a verb it rejects. Where
an act is reached through a second tool that resolves the pin rather than
through the entrypoint itself, that tool SHALL be named, with the fact that it
verifies the content address before invoking the resolved binary — otherwise a
consumer following the instructions literally gets an unrecognized-argument
error and falls back to the ambient tool, which is the state the pin exists to
end.

**THE READ IS AVAILABLE ONLY WHERE THE PINNED REF CARRIES THE ENTRYPOINT, AND
PUBLISHED ADOPTION INSTRUCTIONS SHALL SAY SO.** A consuming repository whose
`stack.yaml` `xfactory.contract_ref` names a commit PREDATING the one that
introduced the registered entrypoint cannot perform the read above at all: the
file is not in the checkout the recipe names, and a reader following the recipe
literally gets a missing-file error and falls through to the ambient tool — the
state the pin exists to end. Published instructions SHALL name the earliest
commit at which the entrypoint exists, and SHALL direct such a consumer to
ADVANCE ITS PIN in its own ordinary pin-sync. A pin behind the entrypoint is a
PIN-SYNC OWED and never a licence for the fallback below, which is admitted only
for a repository carrying NO `xfactory:` stack pin at all. A gate that meets the
absence SHALL REFUSE, naming the missing path and the reason, and SHALL NOT fall
through to an ambient installation or to an unnamed skip, a skip that is not
named being indistinguishable from a pass.

**THE ONE ADMITTED FALLBACK, AND ITS PRICE.** A repository that carries NO
`xfactory:` stack pin cannot perform the read above at all, and MAY therefore
carry a DECLARED consumption copy — a file that names the `openxFactory` commit
the copy was taken from, records the digest of what it copied, and states the
divergence it accepts — as an INTERIM. Such a copy SHALL be retired when that
repository adopts a stack pin, and SHALL NOT be described as consuming the pin
in the sense the paragraph above means. A copy that declares none of this is not
this fallback; it is the undeclared duplicate the fallback is written to
distinguish itself from.

**AND THE FALLBACK DOES NOT DISCHARGE THE ENFORCEMENT CLAIM, WHICH SHALL BE
STATED RATHER THAN LEFT TO A READER TO RECONCILE.** This capability's promoted
requirement *A required check runs the pinned tool, at the pinned digest* holds
that a REQUIRED check *"SHALL NOT invoke an in-tree copy, a vendored duplicate
or an unpinned installation"*. A required check wired off a DECLARED consumption
copy is such an invocation. Declaring the copy therefore makes it AUDITABLE and
does not make it LAWFUL: the declaration is what lets a reader say which bytes
ran, and that requirement's enforcement claim REMAINS UNMET for as long as the
copy stands. A packet admitting the fallback SHALL NOT describe the interim as
satisfying the required-check requirement, and the claim is discharged only when
the copy is retired for a stack pin.

#### Scenario: A consumer pin-syncs to a commit carrying the registration
- **WHEN** a consuming repository advances `stack.yaml`'s `xfactory.contract_ref` to an `openxFactory` commit at or after the pin's registration
- **THEN** the registered pin arrives with the rest of the pinned tree in that ordinary pin-sync
- **AND** no separate adoption act is required for the consumer to LEARN that the pin exists, the contract register being where a consumer looks

#### Scenario: A pin is read across a repository boundary but is registered nowhere
- **WHEN** repositories other than `openxFactory` read a `contracts/<product>-pin.yaml` that appears in neither `contracts/manifest.yaml` nor `contracts/README.md`
- **THEN** the defect is the ABSENT REGISTRATION rather than the read, because the register a consumer is told to read does not declare a consumption those consumers are already performing
- **AND** the remedy is to register it, not to stop reading it

#### Scenario: A consumer copies the pin into its own tree
- **WHEN** a repository that carries an `xfactory:` stack pin copies the pin file, or the entrypoint the pin names, into its own tree and gates on the copy
- **THEN** the copy is a second pin that moves separately and the enforcement claim in that repository is UNMET
- **AND** the copy having been correct on the day it was taken is not a mitigating fact, the defect being that two writings can diverge

#### Scenario: The published instructions name a verb the entrypoint rejects
- **WHEN** adoption instructions tell a consumer to route a governed act through a command that does not accept it
- **THEN** the instruction is not executable, and a consumer following it literally falls back to the ambient tool
- **AND** the register names the actual command for each governed act, including a second tool that resolves the pin and verifies the content address before invoking the resolved binary

#### Scenario: A repository with no stack pin adopts the gate anyway
- **WHEN** a repository that carries no `xfactory:` stack pin wires the gate from a copy
- **THEN** the copy is lawful ONLY as a declared interim naming the `openxFactory` commit it was taken from, the digest of what it copied, and the divergence it accepts
- **AND** it is retired when that repository adopts a stack pin, an undeclared duplicate never becoming lawful by being useful

#### Scenario: The consumer's pinned ref predates the entrypoint
- **WHEN** a consuming repository's `stack.yaml` `xfactory.contract_ref` names an `openxFactory` commit at which the registered entrypoint does not yet exist
- **THEN** the checkout-and-invoke read is unavailable to it, and the remedy is to ADVANCE the pin in that repository's own pin-sync — never to copy the entrypoint, and never to fall through to an ambient installation
- **AND** the published adoption instructions name the earliest commit carrying the entrypoint, and a gate that meets the absence refuses with the missing path and the reason named rather than skipping silently

#### Scenario: A required check is wired off a declared consumption copy
- **WHEN** a repository carrying no stack pin makes a REQUIRED check invoke the entrypoint from its own declared consumption copy
- **THEN** the declaration makes WHICH BYTES RAN auditable, and the promoted requirement *A required check runs the pinned tool, at the pinned digest* — which forbids invoking an in-tree copy, a vendored duplicate or an unpinned installation — has its enforcement claim UNMET for as long as the copy stands
- **AND** the interim is not described as satisfying that requirement, the claim being discharged only when the copy is retired for a stack pin

### Requirement: Registering a pin in the consumption register is not a bundle cut unless it moves the release membership
Publishing a consumption pin as a contract member SHALL be treated as an act on
the CONSUMPTION REGISTER — `contracts/manifest.yaml` and `contracts/README.md` —
and SHALL NOT be treated as requiring a contract-bundle cut UNLESS it also
changes the CLOSED MEMBERSHIP of the release digest inventory. The two registers
answer different questions and are computed differently: the consumption
register is hand-written and says WHAT A CONSUMER MAY READ AND ON WHAT TERMS,
while the release digest inventory is machine-derived over a closed membership
and says WHAT A DECLARED BUNDLE CONTAINS.

**THE TEST IS MECHANICAL AND SHALL BE STATED RATHER THAN ASSUMED.** A
registration that leaves the derived release membership UNCHANGED moves only
editorial members, whose movement between cuts `release-surface-integrity`
already declares an expected, bounded state that the next cut re-baselines; such
a registration owes no cut and no tag. A registration that DOES move the derived
membership changes what the declared bundle contains, and SHALL go through the
bundle realization order — allocating the next available version, re-deriving
the inventory, and leaving the tag owed on the person who lands the cut.

**AND THE MEASUREMENT IS THE AUTHOR'S TO TAKE, IN THE CHANGE THAT REGISTERS.** A
packet that registers a pin SHALL record the derived membership before and after
its own diff, so that "no cut is owed" is a measured fact in the record rather
than a claim a later reader has to re-derive. Silence about the membership is
not evidence that it did not move.

#### Scenario: A registration moves only the editorial members
- **WHEN** a change registers a pin in `contracts/manifest.yaml` and `contracts/README.md` and the derived release membership is unchanged
- **THEN** no bundle cut and no release tag is owed, the two edited files being editorial members whose movement between cuts is expected
- **AND** the change records the before-and-after membership so the conclusion is measured rather than asserted

#### Scenario: A registration adds a file to the closed release membership
- **WHEN** a registration also makes the registered artifact a member of the derived release digest inventory
- **THEN** the declared bundle's contents have moved and the change goes through the bundle realization order rather than landing as a register edit
- **AND** the tag remains owed on the person who lands the cut, exactly as it is for any other cut

#### Scenario: A packet claims no cut is owed and shows no measurement
- **WHEN** a registering packet asserts that no bundle is spent but records no derived-membership reading
- **THEN** the assertion is unevidenced, because the membership is computed rather than obvious and a reader cannot tell an unmoved membership from an unmeasured one
