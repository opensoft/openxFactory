---
code_surface: openxFactory — ONE ADDITIVE SCHEMA MEMBER, ONE RESCOPED COMPARISON SHARED BY TWO CALLERS, ONE NEW DEPRECATION CODE, AND FIVE PACKAGED FIXTURES. `contracts/schemas/xfactory-credential-contracts.schema.yaml` gains `identity_namespace` in the `consumer:` block's DESCRIBED member set — described only, like every other member of that block at this minor: no `type`, no `pattern`, no `required:`, no `additionalProperties: false`, all of which arrive at the major with the acts already queued there. `scripts/validate-credential-contracts.py` gains (a) `identity_namespace` in `CONSUMER_MEMBERS`, so a block that carries it stops drawing `consumer-block-unknown-member`; (b) `_namespace`, which returns the declared namespace ONLY where it matches the identifier grammar and `None` otherwise, so an unreadable value is treated exactly as an absent one; (c) `_same_fetch_authority`, ONE predicate called from BOTH places the promoted text states the comparison — the named `shared-authority-identity` finding and the six-condition lift's THIRD condition — because two implementations of one sentence drift; (d) `_authority_label` and `_namespace_hint`, which put the namespace INTO the message where one was read and name the honest remedy where exactly one side declared one; (e) a NINTH `consumer-*` deprecation code, `consumer-identity-namespace-grammar`, inserted beside its family and ahead of the second family's two, so `test_requirement_ref_resolution.py`'s `DEPRECATION_CODES[-2:]` pin still holds and only its length moves; and (f) `CONSUMER_FREE_STRINGS`, which puts the third free string of this record kind under the existing `baked-secret` screen IN THE SAME COMMIT THAT DECLARES IT. Five packaged fixtures, each registered: ONE positive (two tenants of one provider, one principal name, two namespaces — the CLEARING direction, which a corpus holding only the reporting direction cannot tell from a check that fires on everything), THREE negatives (one namespace on both sides; a namespace on ONE side only; a raw secret in the namespace) and ONE warning probe for the ninth code — all five joining the by-name inventory in `tests/credential_contracts/test_dispatch_credential_contract.py` in the same commit, which is the condition on which that file's count is allowed to be DERIVED. `tests/credential_contracts/major_projection.py` adds the member to `CONSUMER_AT_THE_MAJOR` with the identifier `pattern` and does NOT add it to the `then: required` list, because most estates run one directory and requiring a namespace of them would be a narrowing nothing warned about. Nineteen new tests in `test_consumer_identity_refusals.py`, opening with a BASELINE assertion that the shape reports before any namespace is declared — without it a test that passes because the finding was never raised is indistinguishable from one that passes because a namespace cleared it. `contracts/manifest.yaml`: the `credential-contracts` row's `sha256` recomputed from the bytes on disk (`d0e936fc7377…` -> `b8aa4c77e937…`) and its `consumption_rule` extended, both forced rather than chosen — `test_manifest_row_digest.py` reds at the commit on any schema move that leaves the row behind. `docs/contract-versioning-policy.md` § Deprecations Currently In Force: the ninth row, the member in the entry's own enumeration, the SEVEN-to-EIGHT act count, the reconciliation paragraph's ordinal, and a new paragraph stating that THIS row's deprecation window opens at ITS OWN minor rather than at `contract-v2.4`. `docs/credential-access-model.md` (the worked binding, the no-raw-secret sentence widened from two members to three, and a paragraph on the member) and `docs/domain-factory-starter-pack.md` (one clause). NOT THIS CHANGE'S SURFACE, each for a stated reason: `contracts/CHANGELOG.md`, whose version-headed entry belongs to the CUT and is prescribed verbatim in `tasks.md` § 5 instead — writing a number another packet is spending is how a heading gets renumbered by whoever lands second — which this packet then watched happen, PR #616 cutting `contract-v3.1` under it mid-review; the resolver `resolve_requirement`, its `ambiguous` status and `add-requirement-ref-resolution-integrity`'s § 3.4 freeze, which #553's ruling explicitly leaves alone; the domain-starter generator, which emits `consumer: {instantiation_stub: true}` and gains nothing from an optional member; and `MAJOR_RELEASE`, which reads `contract-v3.0` in the validator while the policy entry has been RESTATED to `contract-v4.0` — a real drift, observed and reported rather than repaired inside a packet that did not cause it.
target_release: THE NEXT ADDITIVE MINOR, DELIBERATELY NOT NUMBERED HERE — allocated AT THE CUT by merge order per `docs/contract-versioning-policy.md`, on the same reasoning `add-binding-consumer-identity` gave and for a sharper instance of it. THE BUNDLE FIGURE IS RE-READ AT EACH ACT THAT ADOPTS IT, and it MOVED under this packet mid-review, which is the argument for not writing one. When this proposal was authored `contract-v3.0` was the newest tag and `contract-v3.1` was being SPENT by PR #616, the cut for `add-project-repo-schema`; #616 has since MERGED (`19d00872`), `contract-v3.1` is cut and published, and this branch's merge-base is now that commit. The next additive minor is therefore `contract-v3.2` as this is re-read — and it is still not written here, because the same thing can happen again before this lands and a number written in advance is a number the next packet to cut would have to renumber. THE CLASS IS ADDITIVE (MINOR), and the policy's own definition is what makes that a measurement rather than a preference: *"Additive (minor) — new optional fields, new contracts, new validator warnings"* covers a described-only member and one new warning code exactly. NOTHING NARROWS AT THIS CUT, AND THAT IS VERIFIED BY CONSTRUCTION RATHER THAN ASSERTED. The comparison change is a SUBTRACTION: it can only make a pair that is reported today go silent, and only when BOTH bindings declare a grammatical namespace and the two differ — every other combination falls back to the bare fetch identity and behaves exactly as the shipped validator behaves. `identity_namespace` joining `CONSUMER_MEMBERS` likewise only REMOVES a warning: a block carrying that key draws `consumer-block-unknown-member` today and stops. The ONE genuinely new refusal is `baked-secret` over the third free string, and it is taken deliberately under `add-binding-consumer-identity` § 2.6's own precedent — that task extended this error-level screen to the two members it declared, in the release that declared them, on the ground that a new free-string sink on the record kind whose invariant is *"never bake a secret"* is a gap rather than a permission; declaring a sink at one release and screening it at the next is how the gap § 2.6 closed reopens. The ONE new WARNING, `consumer-identity-namespace-grammar`, reddens nothing and serves an act at the major, and its window opens at THIS minor rather than at `contract-v2.4` — stated in the policy entry, because a row that borrowed a window it never served is exactly the defect that entry exists to prevent. Every consumer pinned at the prior bundle stays conformant until it upgrades: the member is optional, the schema constrains nothing about the block, and the comparison only stops refusing.
---

# Proposal: add-consumer-identity-namespace

Status: ratified
Ratified: 2026-09-03 by Brett Heap (repository owner) — in session, verbatim
"implement your recommendations on all these", over written recommendations for
five queued items of which TWO land in this packet (openxFactory issues #511 and
#553). Record: `review/ratification-2026-09-03.md`, which quotes both rulings
verbatim and states what the word covers and what it does not.
Proposed: 2026-09-03, on the same act. **RATIFICATION AUTHORIZES REALIZATION AND
THE REALIZATION RIDES WITH IT** — this packet carries a code surface, and
proposal and realization land in one PR because the surface is small enough that
splitting them would put a ratified rule and its only proof in different reviews.
The change stays ACTIVE until merged code and green evidence exist, and **the
CUT is not part of it** — that is the ruling's own exclusion, not a deferral this
packet chose.

## Why

**A ratified refusal in this repository fires on a shape that is not the fault,
and the only escape from it is to write a record that is false.**

`add-binding-consumer-identity` raises `shared-authority-identity` whenever two
bindings declare DIFFERENT holder references and the SAME fetch identity —
correctly, and deliberately independent of `secret_ref`, because a shared secret
reference is a proxy for the rule and not the rule. But the fetch identity is
compared as a BARE STRING, and the `consumer:` block carries no member naming
the directory that issued it. The block is `holder_ref`, `fetch_identity`,
`requirement_ref`, `shared_credential_acknowledged`, `instantiation_stub`, and
not one of those says WHERE a principal was minted.

**A principal name is unique only inside the directory that issues it.** Two
genuinely different principals, in two tenants of one provider, may both be
called `runtime_identity`. Prototyped against the ratified text by the seat that
raised it, and reproduced here as the packaged positive:

```yaml
credential_bindings:
  a:
    provider: azure_key_vault
    vault: kvA
    secret_ref: s1
    consumer: {holder_ref: tenantA-sync, fetch_identity: runtime_identity}
  b:
    provider: azure_key_vault
    vault: kvB
    secret_ref: s2
    consumer: {holder_ref: tenantB-sync, fetch_identity: runtime_identity}
```

`shared-authority-identity` fires. The two principals are NOT one authority;
they are two directories' identically-labelled principals, and **the refusal is
a false positive the record cannot escape**, because no member of the block can
carry the distinction.

**THE ESTATE CANNOT SILENCE IT TRUTHFULLY, which is what makes it worse than a
nuisance.** The only workaround available is to RENAME one `fetch_identity` in
the record while the principal keeps its real name in the provider. That makes
the record FALSE about the estate, and it is precisely the misrepresentation
`add-notebook-hosting-credential-custody` task 4.1 already refused. **A REFUSAL
WHOSE ONLY ESCAPE IS A LIE IS WORSE THAN THE OVER-REPORT IT PREVENTS**, because
the over-report is visible and the lie is not.

**The rule's DIRECTION is sound and only its SCOPE is missing**, and the control
that shows it already ships: one principal genuinely shared across two vaults IS
reported, because the finding correctly ignores `vault`. Nothing here weakens the
finding. It stops firing on exactly one shape — two grammatical, DIFFERENT,
DECLARED namespaces — and behaves as it does today on every other.

## What Changes

**ONE MEMBER, ONE PREDICATE, ONE CODE.**

1. **`identity_namespace` is declared** as an ADDITIVE OPTIONAL member of the
   `consumer:` block, naming the ISSUING DIRECTORY, ACCOUNT OR TENANT WITHIN THE
   PROVIDER that minted the fetch identity. It lands under the block's existing
   declared-at-the-minor / constrained-at-the-major phasing — described in the
   schema now, carrying the identifier grammar at the major — because a new
   member of a block that constrains nothing is a member that constrains nothing.

2. **The authority comparison reads the PAIR.** Where BOTH sides of a comparison
   declare a namespace that matches the identifier grammar, the authority a
   binding names is `(identity_namespace, fetch_identity)`. Where either side
   declares none, or declares a value outside the grammar, the comparison FALLS
   BACK to the bare fetch identity **and still REPORTS**.

3. **The fallback reports and never clears, and that is a security property
   rather than a default.** An estate that could silence a real shared authority
   by OMITTING a member on one side would hold a refusal it can turn off without
   ever writing anything false — a worse instrument than the over-report this
   member exists to end. The same reasoning makes an UNGRAMMATICAL namespace
   behave exactly like an absent one: clearing on a value nothing could read is
   the fail-open shape this family has already had to repair once.

4. **ONE predicate, called from BOTH places canon states the comparison.** The
   promoted text states it once — the lift's third condition, *"their fetch
   AUTHORITIES DIFFER"* — and raises the named finding on the same comparison.
   `_same_fetch_authority` is that sentence, and both callers call it. Two
   implementations of one sentence drift, and the first place they would have
   drifted is the one this packet found by execution: rescoping the finding and
   not the lift would have made a two-tenant pair sharing a secret escape the
   named fault and then be refused by `shared-secret-identity` instead — a
   reader repairing the wrong thing, which is the exact defect the *"a refusal
   shall name the fault it found"* rule exists to prevent.

5. **A NINTH `consumer-*` deprecation code**, `consumer-identity-namespace-
   grammar`, with a packaged probe. It is the ninth SHAPE fault and belongs to
   the block's family; it carries its own code rather than joining
   `consumer-member-grammar` because its CONSEQUENCE differs — an unreadable
   namespace is skipped by the comparison, and a reader told only that a member
   failed a grammar would repair a spelling while believing a scoping they
   declared is in force.

6. **The third free string joins the `baked-secret` screen** in the same commit
   that declares it, under § 2.6's own precedent and with the same recorded
   limit: `_B64ISH` requires forty characters, so a 38-character alphanumeric
   secret passes the screen. The screen catches SHAPES it recognises; it is not
   a secret detector and is not described as one.

**AND #553'S AMENDMENT, CARRIED IN THE SAME BLOCK.** Canon's scenario *"The
requirement reference resolves to more than one record"* reached ACROSS
requirements documents while `resolve_requirement` — frozen by
`add-requirement-ref-resolution-integrity` § 3.4 — matches only inside the ONE
document a reference names. Brett ruled AMEND THE SCENARIO rather than broaden
the resolver, so canon now states the per-document scope the resolver enforces,
and the six-conditions sentence's *"in the repository under validation"* is
rescoped with it. **TWO EDITS AND NO MORE**: no code moves, no status moves, no
severity moves, the resolver is untouched, and repository-wide uniqueness of a
requirement id is still not a rule. That is the whole of #553 in this packet, and
`add-requirement-ref-resolution-integrity` § 9.4's obligation — *decide, do not
leave the contradiction standing* — is DISCHARGED by the AMEND branch it names.

## Why the two rulings ride in one packet

**Because a `## MODIFIED Requirements` block replaces a requirement WHOLESALE,
and two live blocks on one requirement cannot both survive.** Whichever archives
second is the text canon keeps; the first writer's edits vanish, and neither
packet's review would have shown it. #553's ruled target — the ambiguity
scenario and the repository-scope clause in the six-conditions sentence — sits
INSIDE the requirement #511 must modify to rescope the fetch-identity condition.

The alternative was to sequence: land one packet, then write the second block
over the amended canon. It was available and it was not taken, for a reason
stated rather than assumed — **both rulings are the SAME ratifier's, of the SAME
day, over the SAME requirement**, so folding them changes no authority, no scope
and no content; it changes only how many blocks write one requirement, and the
number canon supports is one. The lane that held #553 stood down before
authoring, its branch is deleted, and issue #553 records this packet as its
vehicle.

**WHAT THE FOLD MUST NOT DO, and is checked rather than promised**: it must not
let one ruling's edits ride on the other's authority. The two are kept apart
everywhere a reader looks — `.openspec.yaml` records them separately,
`review/ratification-2026-09-03.md` quotes each verbatim under its own heading,
`design.md` § 6 is #553's and touches nothing of #511's, and `tasks.md` marks
every task with the issue it discharges.

## The other writers on this file, and how the three are ordered

**`add-credential-escrow-checkout`** is RATIFIED, ACTIVE, and owes an additive
minor on this same schema file. Its `credential-contracts` delta MODIFIES
*"Canonical credential record shapes"* — a requirement this packet does not
touch — and its schema growth is an `escrow:` block on the same binding kind
plus a sixth record kind. The two additive blocks do not collide in the bytes,
and the coordination that matters is the manifest row: `test_manifest_row_digest.py`
recomputes the `credential-contracts` digest from the file ON DISK, so whichever
writer moves the schema and not the row fails at the commit rather than at a
consumer that pinned a digest for bytes it never received. That invariant binds
every writer without editing a frozen packet, which is why this proposal states
it instead of asking escrow to re-read anything.

**`add-requirement-ref-resolution-integrity`** is RATIFIED, ACTIVE, and its code
is already SHIPPED on `main`. It holds TWO ADDED requirements on this
capability; this packet MODIFIES two requirements it does not hold, so the two
deltas are disjoint. Its § 3.4 freeze and its `ambiguous` status are CITED and
NOT EDITED — #553's ruling is explicit that the resolver does not move.

**`main` is a third writer of `contracts/manifest.yaml`** in its own right, and
PR #616 WAS a fourth writer of it and of `docs/contract-versioning-policy.md`,
being the `contract-v3.1` cut — it has since merged at `19d00872`, and this
branch was REBASED onto it and its manifest digest and policy edits re-verified
there rather than assumed to survive. That is the whole reason `target_release:` above
declines to write a number.

## No `Modified over` marker is owed, and that was CHECKED

`govern-sibling-added-modified-deltas` reserves the `Modified over` form for a
`## MODIFIED Requirements` block whose requirement exists ONLY as an active
sibling's `ADDED` — or as an active sibling's `RENAMED` `TO:` title. Both
requirements this packet modifies are PROMOTED CANON, added by
`add-binding-consumer-identity` and promoted when it ARCHIVED on 2026-08-31. A
marker naming an archived change would be a marker naming no active basis, which
that packet's own misdeclared state reports. The blocks are ordinary blocks over
canon and carry none.

## Honest reach — what this makes provable, and what it does not

- **It does not verify the namespace against the provider.** A declared
  `identity_namespace` states what the binding's owner says the directory is.
  Where the declaration and the directory disagree, the directory governs, and
  detecting that is a live-estate reconciliation with its own home — the same
  posture this capability already takes for a declared fetch identity.
- **It does not make the comparison cross-repository.** The residency model puts
  two consumers' bindings in two installs' own trees; a validator reading one
  repository compares what one document holds. Naming the namespace makes each
  site READABLE; reconciling the sites remains the owed successor it already was.
- **It publishes one more fact about the estate.** The record already names the
  vault, the secret reference, the owner, the holder and the principal; it now
  also names the DIRECTORY that principal lives in. That is a real widening of
  what a reader of the record learns, it is accepted for the same reason the
  block's other members were, and it is why the packaged fixtures carry
  SYNTHETIC identifiers under the 2026-08-29 ruling that governs this corpus.
- **It does not make a namespace REQUIRED, at either release.** Most estates run
  one directory, and a required namespace would be a narrowing nothing warned
  about — arriving, as the block's own requiredness would have, through the front
  door of an optional field.

## Impact

- **Affected specs.** `credential-contracts` — **2 MODIFIED requirements, 0
  ADDED**. Carriage measured rather than claimed: requirement titles
  byte-identical, 12 scenarios in and 16 out on the block requirement, 12 in and
  15 out on the lift requirement, **zero units lost** on either.
- **`contracts/` IS touched by this packet**, and only in the two places a
  schema edit forces: the schema's member description and the manifest row's
  digest and prose. **NO release tag is cut and no inventory is rebuilt** —
  that is the ruling's own exclusion, and the CHANGELOG entry that belongs with
  the cut is prescribed verbatim in `tasks.md` § 5 so the cut has nothing to
  invent.
- **Affected code, at realization**: as enumerated in `code_surface`, and landing
  in this same PR.
- **NOTHING NARROWS EXCEPT ONE SCREEN, AND IT IS NAMED.** The comparison change
  can only make a reported pair go silent. The member joining the declared set
  can only remove a warning. The one added refusal is `baked-secret` over the
  third free string, taken under § 2.6's precedent and stated here rather than
  slipped in.
- **No live secret is created, moved, or read** by this change or its
  realization. The member names a directory; it holds no material.
- **Two `release-inventory-drift` findings are EXPECTED and are the cut's**, not
  this packet's to green: `contracts/manifest.yaml` and
  `docs/contract-versioning-policy.md` are members of the standing
  `contract-v3.0` inventory, so editing them drifts it. The family's own remedy
  line is *"cut a release through the bundle realization order; never hand-edit
  an inventory or `contract_bundle_version` to make this comparison pass"*, and
  this packet follows it. `add-binding-consumer-identity` § 6.3 took exactly the
  same two findings for exactly the same reason and discharged them at its cut.

## Authoring decisions, stated with the alternative that was rejected

None of these is Brett's. Each was taken by the authoring session inside the
ruling's scope, and each is stated so it can be ruled the other way.

- **AD-1 — the ninth code is a `consumer-*` code, not a second family.** The
  sibling entry beside it made the OPPOSITE call on the SAME rule, and the
  distinction is real rather than convenient: those codes are enumerated against
  refusals OF SHAPE, an unresolvable reference is well-formed and *wrong about
  the world*, and an ungrammatical namespace is a value that does not match a
  pattern. **Rejected alternative**: fold it into `consumer-member-grammar`,
  which would have added no code at all — refused because the namespace's
  grammar fault has a consequence the other members' do not, and a code whose
  message cannot carry that consequence is a code that misleads.
- **AD-2 — an ungrammatical namespace is treated as an absent one.** **Rejected
  alternative**: skip the pair entirely when a namespace is malformed, as the
  identifier guard does for `holder_ref`/`fetch_identity`. Refused because that
  guard exists to stop a MINOR refusing what the major accepts, and it is safe
  in that direction; skipping here would CLEAR a finding on an unreadable value,
  which is the fail-open direction.
- **AD-3 — the stub exemption is unchanged.** A block declaring
  `instantiation_stub: true` beside an `identity_namespace` and no identifiers
  keeps its exemption, because naming a DIRECTORY names no principal.
  **Rejected alternative**: treat any namespace as a live value that withdraws
  the exemption — refused because a template written before an install exists
  may legitimately know which tenant will issue its identity, and withdrawing
  the exemption would warn every such scaffold for the whole minor.
- **AD-4 — the CHANGELOG entry waits for the cut.** **Rejected alternative**:
  write a `## contract-v3.x` heading now. Refused because PR #616 is spending
  `contract-v3.1` as this is written, a heading is part of the cut in this
  repository's ritual (`add-binding-consumer-identity` § 5.2 and § 5.3), and a
  half-cut — a version heading with no tag and no digest inventory — is worse
  than an entry that arrives with its release.

## Open questions

- **OQ-1 — does a namespace belong on the OTHER side of the pair?** `holder_ref`
  is an estate reference and needs no directory; but a cross-repository
  comparison, when it is built, will need to know whether two installs' holder
  references are in one namespace. NOT decided here; the owed successor is the
  cross-repository sweep this capability already names.
- **OQ-2 — should the namespace be RECONCILED against the provider?** A declared
  namespace that no directory carries is the same class of defect as a declared
  fetch identity holding no grant, and this capability routes that to live-estate
  reconciliation. Left there, explicitly, rather than implied.
- **OQ-3 — `MAJOR_RELEASE` reads `contract-v3.0` in the validator while the
  policy entry has been RESTATED to `contract-v4.0`.** Every deprecation message
  this validator prints therefore names a major that has already been cut without
  the acts. OBSERVED here, caused by neither ruling, and NOT repaired inside this
  packet — repairing it would move every one of eleven messages under a packet
  nobody read for that purpose. Reported on the PR so it can be filed.
