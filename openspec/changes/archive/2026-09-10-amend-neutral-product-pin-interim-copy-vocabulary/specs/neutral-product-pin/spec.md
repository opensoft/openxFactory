# neutral-product-pin

**ONE `## MODIFIED` REQUIREMENT, AND IT IS A VOCABULARY RECONCILIATION RATHER
THAN A RULE CHANGE.** The block below is written OVER CANON — `openspec/specs/neutral-product-pin/spec.md`
as `main` states it — and this change is the SOLE ACTIVE MODIFIER of the
requirement it carries. Measured 2026-09-09 over every active change directory:
exactly one
other active change carries a `neutral-product-pin` delta,
`split-opendox-two-layer-product` (ratified 2026-09-05), and it modifies *An
external neutral product is pinned by commit and digest, never by tag* and *The
consuming repository's pin is authoritative among reachable checkouts* — two
requirements, NEITHER of them this one. No active change writes the requirement
key this block writes, so `modified-block-currency`'s two-writers rule does not
reach the pair and NO ORDERING DECLARATION IS OWED in either direction. The two
blocks share a spec FILE and no requirement, which is not a collision; the
proposal records the measurement and `sequenced_after: []` is the positive root
claim that follows from it.

**WHAT MOVES: TWO SCENARIO BULLETS, ONE ADDED BODY PARAGRAPH, ONE ADDED
SCENARIO. EVERY OTHER WORD OF THE REQUIREMENT IS CANON'S OWN.** The requirement
uses `lawful` for two different statuses — the fallback the requirement itself
admits, and compliance with the promoted *A required check runs the pinned tool,
at the pinned digest* — so the same declared interim copy reads as admitted at
`:373` and as not-compliant at `:344`. The word is reserved for the second, the
first is given TOLERATED, and one added paragraph states the reservation in ONE
place so no later reader has to re-derive the two scopes. The two body sentences
that already used the word correctly — *"a copy is not made lawful by being
current on the day it is taken"* (`:299-300`) and *"Declaring the copy therefore
makes it AUDITABLE and does not make it LAWFUL"* (`:344-345`) — are carried
UNCHANGED, because they are right as written under the reserved reading.

**WHAT IS DELIBERATELY NOT TOUCHED.** No other requirement of this capability is
modified, added, renamed or removed. The strict-validation failure this
specification carries on `main` — `requirements.16.text: Requirement must
contain SHALL or MUST keyword`, which is *A pinned artifact that resolves
dependencies at install time carries a vendored lockfile, and the install runs
through it* at `:645`, whose first body line opens *"Where a pinned external
neutral product is distributed…"* — belongs to a DIFFERENT requirement and a
different sentence, is not inherited by this block (this requirement's first
body line carries SHALL), and is not fixed here: fixing it would be a second
amendment of a requirement no word has been given for.

## MODIFIED Requirements

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

**ONE WORD FOR ONE STATUS, AND THE TWO STATUSES ARE NOT THE SAME.** A declared
consumption copy is TOLERATED: this requirement admits carrying it, on the four
terms above — the `openxFactory` commit it was taken from, the digest of what it
copied, the divergence it accepts, and its retirement when a stack pin is
adopted — and on no others. It is NOT LAWFUL, and the two words SHALL NOT be
traded for one another. WHERE THIS REQUIREMENT SPEAKS OF A CONSUMPTION'S STATUS,
LAWFUL names exactly ONE consumption and SHALL NOT be spent on any other: the
read a repository carrying an `xfactory:` stack pin performs by checking
`openxFactory` out at its own `stack.yaml` `xfactory.contract_ref` and invoking
the entrypoint the registered pin names FROM THAT CHECKOUT. Nothing promotes a
copy across that line — declaring it does not, being current on the day it was
taken does not, and being useful does not — and adopting a stack pin does so
only by ENDING the copy rather than by blessing it. A packet, a review record or
a gate record SHALL NOT describe a tolerated interim as lawful or as compliant,
and SHALL say TOLERATED where it means admitted-as-an-interim.

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
- **THEN** the copy is TOLERATED ONLY as a declared interim naming the `openxFactory` commit it was taken from, the digest of what it copied, and the divergence it accepts, and is never LAWFUL, which this requirement spends on a stack-pinned read alone
- **AND** it is retired when that repository adopts a stack pin, an undeclared duplicate never becoming tolerated by being useful

#### Scenario: The consumer's pinned ref predates the entrypoint
- **WHEN** a consuming repository's `stack.yaml` `xfactory.contract_ref` names an `openxFactory` commit at which the registered entrypoint does not yet exist
- **THEN** the checkout-and-invoke read is unavailable to it, and the remedy is to ADVANCE the pin in that repository's own pin-sync — never to copy the entrypoint, and never to fall through to an ambient installation
- **AND** the published adoption instructions name the earliest commit carrying the entrypoint, and a gate that meets the absence refuses with the missing path and the reason named rather than skipping silently

#### Scenario: A required check is wired off a declared consumption copy
- **WHEN** a repository carrying no stack pin makes a REQUIRED check invoke the entrypoint from its own declared consumption copy
- **THEN** the declaration makes WHICH BYTES RAN auditable, and the promoted requirement *A required check runs the pinned tool, at the pinned digest* — which forbids invoking an in-tree copy, a vendored duplicate or an unpinned installation — has its enforcement claim UNMET for as long as the copy stands
- **AND** the interim is not described as satisfying that requirement, the claim being discharged only when the copy is retired for a stack pin

#### Scenario: A record describes a declared interim copy as lawful
- **WHEN** a packet, a review record or a gate record describes a repository's DECLARED consumption copy as lawful, or as compliant with the required-check requirement, on the strength of its declaration
- **THEN** the description is wrong on this requirement's own vocabulary: a declared consumption copy is TOLERATED as an interim and is never LAWFUL, which names only the read performed from the checkout that repository's own `stack.yaml` `xfactory.contract_ref` fixes
- **AND** the interim's status moves only by the copy being RETIRED for a stack pin, so the reader is owed the word TOLERATED wherever the record means admitted-as-an-interim, and never a word that would let the required-check claim be read as discharged

**Removed from canon by amend-neutral-product-pin-interim-copy-vocabulary (2026-09-09):** ``**THEN** the copy is lawful ONLY as a declared interim naming the `openxFactory` commit it was taken from, the digest of what it copied, and the divergence it accepts``; `**AND** it is retired when that repository adopts a stack pin, an undeclared duplicate never becoming lawful by being useful` — both bullets are REPLACED IN PLACE by the two above them and neither is dropped, and THE TWO EDITS ARE NOT THE SAME SIZE: the AND bullet replaces ONE WORD and nothing else, while the THEN bullet replaces one word AND APPENDS a reservation clause, “and is never LAWFUL, which this requirement spends on a stack-pinned read alone”, so the reservation is stated where the fallback is ADMITTED and a reader meeting this scenario first does not have to reach the added body paragraph to learn it. That appended clause is ratified surface and is declared here rather than left to be found in the diff. This requirement already spends LAWFUL on the required-check claim, twice and unambiguously, while these two bullets spent it on the requirement's OWN admission of the fallback, so one word carried two statuses and a reader reaching the scenario first could certify a declared interim copied gate as compliant — which the body forbids in the next paragraph. Nothing this requirement admits or refuses moves: the same copies are admitted, on the same four terms, and the required-check claim stays unmet for exactly as long as it did before. This reason carries no code span, so the marker names exactly two units under the grammar it is written in.
