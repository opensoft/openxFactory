# neutral-product-pin Specification

The FIRST MODIFIED requirement is written OVER `add-openspec-cli-pin`'s block for
the same requirement, on the ordering declaration recorded below; the SECOND is
written over CANON, `add-openspec-cli-pin` carrying no delta on it and no other
active change carrying one either.

**THE ORDERING DECLARATION IS MADE, AND THIS PARAGRAPH REPLACES THE ONE THAT
RECORDED IT AS OWED.** When these deltas were authored **no active change carried
a delta on this capability** — checked over all 31 active change directories at
`origin/main` `a858e5b0`, 2026-09-04. That measurement went stale inside the same
week: `add-openspec-cli-pin` was ratified 2026-09-04 (Brett Heap, *"ratify 667"*)
and LANDED as `opensoft/openxFactory#667`, carrying its own `## MODIFIED` block
over *An external neutral product is pinned by commit and digest, never by tag* —
the same requirement this delta's first block modifies. Two ACTIVE RATIFIED
writers then held that requirement and neither named the other, so
`modified-block-currency` reported the ordering as undecided against both blocks
(two `contested` warnings, measured 2026-09-05).

**Brett Heap ruled *"declare and land"*** at 2026-09-05T12:49Z
(`https://github.com/opensoft/openxFactory/issues/656#issuecomment-5551928470`).
This packet ratified 2026-09-05T01:38Z and `add-openspec-cli-pin` on 2026-09-04,
so under `release-realization`'s *Ordered deltas and branch vocabulary* THIS
packet is the LATER writer. Its `proposal.md` now REFERENCES
`add-openspec-cli-pin` by name — that reference IS the ordering the family reads
— and the first MODIFIED block below is written over that change's OUTCOME rather
than over canon: all 26 units of the earlier block are carried and none dropped,
this packet's own addition is marked in place with a `Modified by` lead-in, and
the requirement body carries a per-requirement record of the declaration.

**The reserved ``Modified over `<basis>`'s addition by <change-id> (<date>):``
pairing form is deliberately NOT used here, and the reason is a distinction that
form itself makes.** It declares a block written over a requirement the promoted
specification does not yet carry, which an active sibling ADDS or RENAMES to.
`add-openspec-cli-pin` MODIFIES a requirement canon already carries; the pairing
arm does not reach this shape, and a marker of that form here would assert an
addition that does not exist. What this shape owes is the proposal reference, and
the in-body paragraph records it in the parallel wording without borrowing the
reserved anchor.

**Why this capability has to grow, in two places.** The capability was written
for a pin whose CONSUMPTION IS A FILE READ: `openxFactory` pins `openXwallet`,
a required check runs the pinned validator over a tree, and a pin bump is a
commit. Two facts of this extraction are outside that shape.

1. **A pin whose consumption is a DEPLOYMENT.** openDox is an application with a
   database and ordered migrations (RULING Q2, 2026-09-04T15:31Z: FastAPI +
   Postgres on the `xFactory-Hermes-Install` pattern), and RULING Q3 makes every
   tenant's instance its own deployment with its own store. Bumping that pin is a
   scheduled OPERATION against N live instances, not an edit — and nothing in this
   capability contemplates a pin bump that has downtime.
2. **A pin CHAIN two levels deep.** RULING Q4 (15:34Z) points the dependency ONE
   way: openXdox depends on openDox, never the reverse. So a descendant pins
   openXdox, openXdox pins openDox, and `openxFactory` reaches openDox only
   THROUGH openXdox. The capability's existing rule settles which of several
   REACHABLE CHECKOUTS wins; it does not say who may declare a transitive
   upstream's commit, and two levels each free to declare the same product's
   commit is the same "two answers to which bytes are pinned" defect one level
   down.

**RULED OQ-2 (`opensoft/openxFactory` issue #656, 2026-09-04T22:16Z): TWO
MODIFIED REQUIREMENTS AND NO THIRD.** This packet had recommended a third — a
one-field "which layer do you pin" declaration, so a consumer could pin openDox
directly. Brett ruled against it in terms: *"Inside the xFactory family there is
ONE chain: openDox is pinned only by openXdox, and every domain descendant pins
openXdox … No third MODIFIED requirement is added to `neutral-product-pin`."* The
mapping core is never bypassed and there is one consumption shape to validate.
**This does not close openDox**: *"Anyone outside the family uses openDox freely
as open source — this ruling governs the pin chain only"*, so RULING Q7's
public-from-day-one posture and RULING C3's standalone student both stand. The
CHAIN clause below is therefore the whole of what one chain needs, and the absent
third requirement is a ruled omission rather than an oversight. Rejected: a
direct pin for docs-only installs; deferring to the first request.

**What is deliberately NOT modified here.** *An unanswerable pin question refuses,
and the refusal names its remedy*, *A required check runs the pinned tool, at the
pinned digest*, *A pinned validator invoked with no scan target refuses*,
*Repointing the reader and editing what it reads is one human-only act*, *A
neutral product may vendor one openxFactory contract, and names the version it
pins*, *A vendored foreign contract is digest-verified before it is read* and
*The pinned validator is the contract family's conformance validator from the
major forward* are unchanged and reach the new shapes as written.

## MODIFIED Requirements

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

WHERE THE PRODUCT IS DISTRIBUTED AS A PUBLISHED, CONTENT-ADDRESSED ARTIFACT
RATHER THAN AS A SOURCE TREE, the pin SHALL carry that ARTIFACT'S DIGEST as its
referent and SHALL declare `revision_kind` accordingly, and the release NAME —
the version string — is a LABEL recorded beside it on exactly the terms a tag is
recorded beside a commit. The distinction is the same one and it is not weakened
by the change of medium: a digest over the published bytes cannot be moved,
whereas a version name is kept stable by a REGISTRY'S POLICY and an operator who
administers it, and a policy is not a content address.

Such a pin carries NEITHER a per-file `sha256` list NOR a `pinned_by_commit_only:`
list, and their absence is not a permitted omission but a consequence of the
medium. Those two lists exist because a commit is not a digest a consumer can
compare a single file against, so the surface must be ENUMERATED for
completeness to be checkable at all. A published artifact needs no enumeration:
ONE digest addresses EVERY byte inside it, so no member can be undeclared and
none can be added or altered without changing the referent. The completeness
obligation is therefore DISCHARGED MORE STRONGLY here rather than waived, and a
pin of this kind SHALL record every field the consumer's verifier checks —
including any secondary address the registry publishes — so that no declared
field goes unverified.

**Modified by `split-opendox-two-layer-product`:** **WHERE THE PINNED PRODUCT IS
A RUNTIME, THE PIN SHALL DECLARE THAT ITS CONSUMPTION IS A DEPLOYMENT AND NAME
THE OPERATION A BUMP REQUIRES.** A pin whose
product carries a database schema and ordered migrations SHALL declare the
migration RANGE the bump crosses, whether the bump is reversible, and the runbook
that performs it — beside the commit and the digests, in the pin file, not only in
a runbook nobody reads at bump time. A pin bump for such a product is an
OPERATION against every running instance and not an edit of a file, so a
repository that moves the pin and merges has NOT completed the consumption: the
instances are still running the previous commit until the operation runs, and a
pin the fleet has not reached is a declared fact that is not yet true. The
declaration SHALL NOT be read as permission to skip the digests — commit and
per-file `sha256` remain the trusted referent exactly as for a file-read pin, and
the deployment declaration is what the digests are consumed BY. It reaches a
different medium from the published-artifact clause above and narrows none of
it: an artifact-digest pin whose product is also a runtime owes both.

**Modified over `add-openspec-cli-pin`'s modification by
split-opendox-two-layer-product (2026-09-05):** — the basis MODIFIES this
requirement rather than ADDING it, was ratified 2026-09-04 and landed as
`opensoft/openxFactory#667`; this packet ratified later, 2026-09-05T01:38Z, and
Brett Heap ruled *"declare and land"* at 2026-09-05T12:49Z on
`opensoft/openxFactory` issue #656. This block is therefore written over the
basis's OUTCOME and not over canon: all 26 of its units are carried — the
published-artifact clause, the enumeration clause and both of its scenarios
included — and the runtime-deployment clause above with the two scenarios at the
end are this packet's own additions on top, marked in place. The ordering the
`modified-block-currency` family reads is the reference to
`add-openspec-cli-pin` in this packet's `proposal.md`; this paragraph is the
per-requirement record of that declaration and is NOT the reserved pairing
marker, whose form is reserved for a basis that ADDS an unpromoted requirement.

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

#### Scenario: The product is published as an artifact rather than as a source tree
- **WHEN** the consumed product is distributed as a published package whose registry publishes a digest over its bytes
- **THEN** the pin records that digest as the referent, declares a `revision_kind` naming it, and records the version string only as a label
- **AND** the pin carries no per-file list, one digest over the artifact addressing every file inside it and leaving nothing undeclared

#### Scenario: A published-artifact pin records only a version
- **WHEN** such a pin names a version, a dist-tag or a range and records no digest over the artifact
- **THEN** it is refused on the same ground a tag-only pin is refused, a name whose stability is a registry's policy not being the thing that is trusted

#### Scenario: A pin bump crosses a migration
- **WHEN** the pinned commit of a product carrying a database schema moves across one or more ordered migrations
- **THEN** the pin declares the migration range, the bump's reversibility and the runbook that performs it
- **AND** the bump is not complete when the pin file merges; it is complete when the operation has run on every instance the pin governs

#### Scenario: A runtime product's pin declares no operation
- **WHEN** a pin for a product with a schema records a commit and digests and says nothing about the migration its bump crosses
- **THEN** the pin is incomplete, because the consumer cannot tell an edit from an outage from the file it is asked to trust

### Requirement: The consuming repository's pin is authoritative among reachable checkouts
A resolver SHALL prefer the pin recorded in the CONSUMING repository wherever more than one checkout of a pinned neutral product is reachable from a consuming tree, and that pin SHALL be authoritative;
and the aggregation's ROOT gitlink for a product `openxFactory` pins SHALL EQUAL
`openxFactory`'s NESTED gitlink commit, checked in the aggregation. Without this,
a walk-up resolver in a
consumer repository silently reads whichever checkout it meets first — the
aggregation root or the nested one — and only the nested one is governed by
`contracts/<product>-pin.yaml`.

**A PIN CHAIN IS RESOLVED ONE HOP AT A TIME, AND ONLY THE DIRECT UPSTREAM IS
DECLARED.** Where a neutral product itself pins a second neutral product, each
level SHALL declare ITS OWN DIRECT UPSTREAM by commit and digest and SHALL NOT
re-declare a transitive upstream's commit: the transitive commit is READ from the
intermediate's own pin, at the commit this level pins, and it is a DERIVED fact.
A consumer that needs the transitive commit SHALL resolve it through the chain and
MAY record it as a derived value clearly marked as derived, never as a second
authority. Two levels each free to declare the same product's commit reproduces,
one level up, the defect the reachable-checkouts rule exists to end — two answers
to "which bytes are pinned" is no answer, whether the two answers come from two
checkouts or from two pin files.

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

#### Scenario: A consumer needs a product it reaches only through an intermediate
- **WHEN** a repository pins product B, and product B pins product A, and the repository needs A's commit
- **THEN** it resolves A's commit from B's own pin at the commit it pins of B, and records it only as a derived value
- **AND** a second declaration of A's commit at the consuming level is refused, because the chain then has two authorities for one answer

#### Scenario: An intermediate's pin and a consumer's re-declaration disagree
- **WHEN** a consumer has re-declared a transitive upstream's commit and it differs from the commit the intermediate's own pin records
- **THEN** the disagreement is refused rather than resolved in either direction, on the same reasoning as the two-gitlink case
