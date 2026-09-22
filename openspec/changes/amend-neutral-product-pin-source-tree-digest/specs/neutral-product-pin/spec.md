# neutral-product-pin — delta

ONE REQUIREMENT, ONE AMENDED CLAUSE. This delta amends the SOURCE-TREE half of
*An external neutral product is pinned by commit and digest, never by tag* so
that a whole-tree digest over a pinned source tree discharges the per-file
`sha256` / `pinned_by_commit_only:` obligation as an EQUIVALENT, rather than
standing beside it as an unwritten exception. It adds one amendment paragraph
and five scenarios and edits not one character of any unit the requirement
already carries.

**THE BLOCK IS WRITTEN OVER `split-opendox-two-layer-product`'s OUTCOME.** That
packet holds an active `## MODIFIED` block on this same requirement, ratified
2026-09-05, and its runtime-deployment clause and two scenarios are carried here
with everything else. The per-requirement record of that declaration stands in
the block itself, in the form the basis used one link up this same chain.

**NOTHING ELSE IN THE CAPABILITY MOVES.** The published-artifact clause, the
enumeration clause and the runtime-deployment clause are carried VERBATIM; the
fail-closed requirement, the required-check requirement and every other
requirement of `neutral-product-pin` are untouched and are not restated here.

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

**Amended by `amend-neutral-product-pin-source-tree-digest` (2026-09-22):** **A
WHOLE-TREE DIGEST IS AN EQUIVALENT DISCHARGE OF THE PER-FILE OBLIGATION THIS
REQUIREMENT OPENS WITH, AND NEVER AN EXEMPTION FROM IT.** Where a pin of a
SOURCE TREE declares a whole-tree digest definition and records a digest
computed over the ENTIRE TREE of the commit it names —
`digest_definition: sorted-ls-tree-r-v1` with `digests.tree_sha256`, the form
this estate's pin family already writes — that digest SHALL discharge the
per-file `sha256` and `pinned_by_commit_only:` obligation. SUCH A PIN CARRIES
NEITHER A PER-FILE `sha256` LIST NOR A `pinned_by_commit_only:` LIST, in the
published-artifact clause's own words and for its own reason: the two forms are
ALTERNATIVES rather than a menu to combine, and a record carrying both declares
two answers to what is enumerated where exactly one is owed. WHAT MAKES THE TWO
FORMS EQUIVALENT is the reasoning the
paragraph above already states for the published-artifact medium, which reaches
a source tree unchanged: the lists exist because a commit is not a digest a
consumer can compare a single file against, so the surface must be ENUMERATED
for completeness to be checkable at all — and a whole-tree digest needs no
enumeration, because it covers EVERY FILE IN THE TREE and therefore SUBSUMES any
list of them. No member can be undeclared, and none can be added, removed or
altered without changing the referent, so the completeness obligation is
DISCHARGED MORE STRONGLY rather than waived. AN ENUMERATION REMAINS LAWFUL AND
REMAINS OWED where no whole-tree digest is recorded: this admits a second form
and retires neither the first nor any pin that carries it. WHERE THE EQUIVALENCE
DOES NOT REACH, written here so it cannot be read wider than it is: it is a
statement about WHICH FORM the digest obligation takes and never about WHETHER
digests are owed, so it authorizes skipping no digest anywhere. AND IT DOES NOT
REACH A PIN THE RUNTIME-DEPLOYMENT CLAUSE BELOW GOVERNS: for a product carrying
a database schema and ordered migrations that clause stands UNMODIFIED, its
trusted referent unchanged and its refusal to read a deployment declaration as
permission to skip the digests unweakened, and whether a whole-tree digest may
discharge the per-file obligation THERE is a question this amendment leaves
unopened rather than answers by implication. A pin that records NEITHER a
per-file list NOR a whole-tree digest over the commit's tree has discharged
nothing.

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

**Modified over `split-opendox-two-layer-product`'s modification by
`amend-neutral-product-pin-source-tree-digest` (2026-09-22):** — the basis
MODIFIES this requirement rather than ADDING it, and was ratified 2026-09-05
ahead of this packet. This block is therefore written over the basis's OUTCOME
and not over canon as it reads while that packet is still active: every unit the
basis carries is carried here — the source-tree clause, the published-artifact
clause, the enumeration clause, the basis's own runtime-deployment clause, its
per-requirement record above and all seven of its scenarios — and the amendment
paragraph and the five scenarios at the end are this packet's own additions on
top, marked in place. The ordering the `modified-block-currency` family reads is
the `sequenced_after: [split-opendox-two-layer-product]` declaration and the
reference to that packet in this one's `proposal.md`; this paragraph is the
per-requirement record of that declaration and is NOT the reserved pairing
marker, whose form is reserved for a basis that ADDS an unpromoted requirement.
Should the basis archive first, this block is written over canon exactly as
promoted and the declaration is the record of why.

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

#### Scenario: A source-tree pin records a whole-tree digest instead of a per-file list
- **WHEN** a pin of a source tree declares `digest_definition: sorted-ls-tree-r-v1`, records a `digests.tree_sha256` over the whole tree of the commit it names, and carries neither a per-file `sha256` list nor `pinned_by_commit_only:`
- **THEN** the completeness obligation is DISCHARGED, that digest covering every file in the tree and therefore subsuming any enumeration of them
- **AND** the absence of the two lists is not a permitted omission but a consequence of the stronger form, no member being undeclarable and none alterable without changing the referent

#### Scenario: A source-tree pin carries both forms
- **WHEN** a pin records a whole-tree digest over the commit's tree AND a per-file `sha256` or `pinned_by_commit_only:` list
- **THEN** it is refused, the two forms being alternatives rather than a menu to combine
- **AND** the refusal is that the record declares two answers to what is enumerated where exactly one is owed, not that either answer is wrong on its own

#### Scenario: A source-tree pin records neither form
- **WHEN** a pin names a commit and carries no per-file `sha256` list, no `pinned_by_commit_only:` and no whole-tree digest over that commit's tree
- **THEN** it is refused, the equivalence admitting a second way to DISCHARGE the obligation and never a way to leave it undischarged

#### Scenario: A runtime product's pin is offered the equivalence
- **WHEN** the pinned product carries a database schema and ordered migrations, so the runtime-deployment clause governs its pin
- **THEN** the equivalence does not reach it, that clause standing unmodified with its trusted referent unchanged
- **AND** whether a whole-tree digest may discharge the per-file obligation there is left unopened, an amendment scoped to one clause not answering for another by implication

#### Scenario: The equivalence is cited as permission to skip a digest
- **WHEN** a pin, a consumer or a runbook cites the whole-tree equivalence to justify verifying no digest at all, or to narrow the runtime-deployment clause's refusal
- **THEN** the reading is refused, the equivalence being about WHICH FORM the digest obligation takes and never about WHETHER digests are owed
