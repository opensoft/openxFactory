# neutral-product-pin Specification

## ADDED Requirements

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
