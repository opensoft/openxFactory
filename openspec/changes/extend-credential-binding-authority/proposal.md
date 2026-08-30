---
code_surface: openxFactory — a SCHEMA CHANGE plus its validator, fixtures and tests. `contracts/schemas/xfactory-credential-contracts.schema.yaml` gains FOUR ADDITIVE OPTIONAL FIELDS on each entry of `credential_bindings` in the existing `xfactory_credential_binding_template`: `consumer`, `fetch_identity`, `identity_namespace` and `requirement_id`. `scripts/validate-credential-contracts.py` gains one new refusal (`shared-fetch-identity`), one refinement of an existing refusal (`shared-secret-identity` gains a narrowly-conditioned exemption that opens only on positive declarations, AND is regrouped onto the qualified key `(provider, vault, secret_ref)` rather than the bare `secret_ref` it groups by today, WITH A FALLBACK to the bare grouping wherever any member of a matching `(provider, secret_ref)` set omits `vault` — decision 8, the one change this packet makes to a check it did not author), and its FIRST WARNING CHANNEL, carrying two codes (`binding-authority-undeclared`, warning across the current major line and error at the next major version; and `authority-scope-indeterminate`, SECRET COMPARISON ONLY, where an omitted optional `vault` leaves two matching secret references un-adjudicable). The two comparison keys are qualified and DELIBERATELY DIFFERENT — `(provider, identity_namespace, fetch_identity)` for the authority, `(provider, vault, secret_ref)` for the secret — because a principal granted on two vaults is ONE authority and a vault-qualified identity key would report nothing on exactly the record the ratified per-system rule forbids. BOTH keys FALL BACK toward reporting where their qualifier is undeclared: the secret key to the bare reference, the identity key to `provider` alone. `examples/credential-contracts/` gains NINE fixtures, enumerated here by name so the count is checkable rather than recalled — THREE POSITIVES (`notebook-hosting.binding-template.example.yaml`, the two-consumer shape; a cross-provider positive; and `two-namespaces.binding-template.example.yaml`, a same-named principal in two declared namespaces) and SIX NEGATIVES (`negative/shared-fetch-identity.yaml`; `negative/shared-secret-different-requirements.yaml`; `negative/shared-fetch-identity-across-vaults.yaml`, which pins the identity key against re-acquiring `vault`; `negative/authority-scope-indeterminate.yaml`; `negative/shared-secret-vault-undeclared.yaml`, which pins the grouping-side fallback by proving a refusal survives an omitted `vault`; and `negative/exemption-one-sided-namespace.yaml`, which pins the EXEMPTION-side scope by proving a one-sided `identity_namespace` does not buy the exemption) — and `tests/credential_contracts/test_dispatch_credential_contract.py` moves with them, including the self-test count string it asserts, which is derived once at realization rather than written here. NO NEW RECORD KIND. NO REQUIRED FIELD. `contracts/` IS UNTOUCHED BY THIS PROPOSAL — the release ritual is scheduled in tasks.md § 5 for realization, and no bundle is cut by the packet that proposes it.
target_release: THE NEXT ADDITIVE MINOR, DELIBERATELY NOT NUMBERED HERE. `docs/contract-versioning-policy.md` states the rule this front-matter obeys: "A proposed change MUST NOT reserve a minor number before merge order is known." FRESH-COUNTED AGAINST `origin/main` ON 2026-08-30, BECAUSE THIS TRAIN MOVES FASTER THAN A PROPOSAL SITS: `contracts/manifest.yaml` declares `contract-v2.2` and `contracts/CHANGELOG.md` heads at `contract-v2.2 — 2026-08-29`, with the annotated tag `contract-v2.2` PUBLISHED. So `contract-v2.2` is SPENT, and the earlier revisions of this front-matter that named it as this packet's expected allocation are stale — as were the ones before that naming `contract-v2.1`, and as any number written here will eventually be. Further: the MERGED `add-signed-execution-chain` already names `contract-v2.3` as its own target, so the earliest number this packet could take is `contract-v2.4`, and even that is not claimed. NOTHING IS RESERVED HERE, under the policy sentence above. Three packets now contend for the next additive minors — this one, `add-credential-escrow-checkout` (same schema file), and the signed-execution-chain train — and a number written in a proposal is a number another packet may spend first, which is exactly what the rule exists to prevent; the `contract-v1.28` renumber sweep is the standing precedent for the cost. The number is allocated AT REALIZATION by merge order (tasks.md § 5.2), and § 5.2 instructs a re-count at that moment rather than trusting this paragraph. WHY A CUT IS OWED AT ALL, MEASURED RATHER THAN ASSUMED: parsed on 2026-08-29, `contracts/releases/contract-v2.1.digests.yaml` holds 192 entries, exactly five of them under `contracts/schemas/`, and `xfactory-credential-contracts.schema.yaml` IS NOT ONE OF THEM — neither is its validator, nor anything under `examples/`. So the cut is NOT forced by `release-inventory-drift`, which is the usual reason a schema edit owes one. It is owed by the VERSIONING POLICY instead: the schema is a registered bundle contract (`contracts/manifest.yaml`, `id: credential-contracts`), and a registered contract gaining optional fields and validator warnings is that policy's ADDITIVE (MINOR) class verbatim, under which "Domain repos on the same major version remain conformant without changes". `consumer` and `fetch_identity` becoming REQUIRED is the BREAKING (MAJOR) class and is scheduled for the next major, not for this cut; `requirement_id` stays optional across it, because its absence never warns and a major may not break what no minor deprecated.
---

# Proposal: extend-credential-binding-authority

Status: draft
Proposed: 2026-08-29
Origin: the NAMED SUCCESSOR owed by task 4.5 of
`add-notebook-hosting-credential-custody`, ratified by Brett Heap on
2026-08-23 with that task's admitted enforcement gap in view. Full origin
declaration in this packet's `.openspec.yaml`.

THE RATIFICATION THAT NAMES THIS SUCCESSOR AUTHORIZED AUTHORING IT AND NOTHING
MORE. The field names, the rule shapes, and this packet's position on the
question task 4.1 left open are the authoring session's and are put to the
council review and to Brett in § Decisions put to the review. This packet is
`Status: draft` until that ruling.

## Why

**A ratified requirement is currently held by review, and its own packet said
so.** `add-notebook-hosting-credential-custody` ratified two obligations about
operated identities. The second is per-system authority: where more than one
system authenticates as the same operated identity, each SHALL reach it through
its own binding, with its own access identity, grant, rotation visibility and
audit trail — one identity may be shared, one authority may not. That packet
then recorded, in its own Impact section and in a scenario of the ratified
delta, that the published record cannot express it:

> the shape carries no consumer or access-identity field, so the per-system
> authority is asserted by the binding's owner and its estate wiring rather
> than proven by the record

Its task 4.5 names the remedy — extend the published binding shape so the
per-system authority is REPRESENTABLE — and explains why it was deferred rather
than smuggled in: extending `contracts/schemas/` carries the full
contract-release ritual. This packet is that successor, and it carries the
ritual.

**The gap is measurable, not rhetorical.**
`xfactory_credential_binding_template` requires `[provider, secret_ref, owner, rotation_policy]` with `vault` optional. There is no field for who consumes the
credential and none for what identity reaches the store, and
`scripts/validate-credential-contracts.py` compares no authorities at all. Two
bindings naming one vault principal validate cleanly today. So does one binding
naming two — the record cannot tell the difference, which means no check can.

**The unclaimed key already exists in this repository, in a contract
artifact.** This is the forcing fact, and it was found by reading the tree
rather than by reasoning about it.
`contracts/avatar-client/broker-server-key-binding.template.yaml` is
`kind: xfactory_credential_binding_template` — the very record kind this packet
extends — and it already carries `fetch_identity: install_federated_workload_identity`, in a document-level `resolution:` block
that the schema neither declares nor forbids. That is precisely the defect this
same schema's `issuance_preconditions` vocabulary was added to retire, in the
words of its own description: *"the mechanism existed as a domain-local extra
key riding a neutral schema that neither declared nor forbade it, so a refusal
had no neutral home to be declared against."* The same species, on the same
schema, one record family over. The estate has already reached for this field
and had nowhere to put it.

**And the absent field has already cost a fixture.** Task 4.1 of the custody
packet DECLINED to package an example of its own ratified two-consumer shape,
because `shared-secret-identity` fires whenever two bindings in one template
share a `secret_ref` and two systems reaching one account's password is exactly
that shape. The requirement text had to carry the shape instead. A ratified
obligation whose conforming example cannot be packaged without tripping the
repository's own validator is the clearest possible statement that the record is
short a field.

## What Changes

**Four optional fields, on the binding, in the estate's own words.** Each entry
of `credential_bindings` may declare `consumer` (the consuming system),
`fetch_identity` (the identity that consumer authenticates to the secret store
with), `identity_namespace` (the directory, account or tenant within the
provider that ISSUES that identity), and `requirement_id` (the credential
requirement the binding resolves). No new record kind, no new envelope, no
required field. Two of the four — `consumer` and `fetch_identity` — become
required at the next major; `identity_namespace` and `requirement_id` do not,
because neither one's absence ever warns and a major may not break a shape no
minor deprecated.

**`fetch_identity`, not a second spelling.** The promoted requirements already
say the lane receives "an opaque secret reference and a fetch-identity
identifier" and that reference delivery is "a vault URI plus the runtime's own
fetch identity"; a shipped record of this kind already uses the key. "Access
identity", the custody packet's prose and the projection documentation's, names
the same thing — the synonym stands in prose and the RECORD gets one spelling.
The ratified custody text is not edited to match: a ratified delta is not
rewritten for a successor's convenience, and the requirement states the
synonymy instead.

**Sameness is decided on the QUALIFIED name, never the bare string.** `provider`
and `vault` are per-binding and unconstrained, so `fetch_identity` is a name in a
provider's identity namespace and `secret_ref` a name in a vault. Two consumers
labelling their principals `runtime_identity` against unrelated providers are not
one authority, and refusing them would be a collision the checker invented. Every
comparison is qualified, and the two keys DIFFER ON PURPOSE:
`(provider, fetch_identity)` for the authority and `(provider, vault, secret_ref)`
for the secret. An identity does not live in a vault — one principal granted on
two vaults is ONE authority, and folding `vault` into the identity key would
report nothing on exactly the record the ratified per-system rule forbids. On the
secret side `vault` is optional, so where it is declared on one side only the
record cannot say, and that warns rather than refuses. This corrects the same latent defect in the published
`shared-secret-identity`, which groups by bare `secret_ref` today — the proposed
rule would have been its second appearance, so it is fixed once for both.

**One new refusal.** `shared-fetch-identity`: two bindings declaring the same
qualified fetch identity while naming different consumers. That collision IS the
violation of "one identity may be shared, one authority may not", and it is now
a finding rather than a review note.

**One refinement, opened only by saying more.** `shared-secret-identity` keeps
refusing a shared `secret_ref` EXCEPT where every binding sharing it declares
the same `requirement_id` and pairwise-distinct `consumer` and `fetch_identity`.
Every existing record is adjudicated exactly as before, because each condition
is a positive declaration no existing record makes — including the packaged
negative, which stays red.

**A warning channel the validator has never had.** A binding that does not
declare BOTH a consumer and a fetch identity warns, naming whichever is missing,
and stays valid — on either absence, not only on both, since the two are refused
together at the next major version and a shape that never warned cannot be broken there. New
optional fields plus new validator warnings is the additive class; THOSE TWO
fields become required at the next major, which is the breaking class and owes
at least one full minor of warnings first. `requirement_id` is deliberately not
on that path — its absence never warns, so no major may require it — and it is
obligatory only where a record claims the shared-secret exemption. This is the `contract-v1.34` pattern — deprecate
in a minor with the removal version named in the changelog, refuse at the next major version.

**The fixture task 4.1 could not write.** With the record able to tell the two
cases apart, the custody packet's own two-consumer shape becomes packageable, so
this change adds it as a positive fixture — and adds the negative that proves
the exemption is NOT the naive one.

## The decision this packet puts to the review

Task 4.1 left one question explicitly open and made it a precondition of any
fixture: should `shared-secret-identity` distinguish "two credentials collapsed
into one" from "two consumers of one credential"?

**This packet's position: YES, distinguish — and the discriminator is the SHARED
REQUIREMENT, never the distinct consumer.**

The argument is executable, and it is why the obvious answer is wrong. The fault
the check exists to catch is a dispatch credential and a content-write
credential resolved to one secret. Those two bindings HAVE distinct consumers —
a zero-write serving tier and a privileged CI apply lane — and under the
promoted dispatch-only separation requirement they must also hold distinct
identities. So an exemption keyed on "distinct consumers and distinct fetch
identities" would admit the exact record `examples/credential-contracts/negative/dispatch-reuses-content-secret.yaml` exists to refuse. Only "the sharing
bindings resolve the SAME credential requirement" separates one key serving two
PURPOSES from one key serving two CONSUMERS of one purpose.

**The alternative, recorded so the council rules on a choice and not on a
recommendation:** leave `shared-secret-identity` unconditional. Its honest cost
is that the ratified two-consumer shape then has no conforming single-document
representation, so the estate either splits the two bindings across template
documents — which evades the rule silently, because the comparison is
per-document and always was — or collapses two authorities into one binding
carrying a list of consumers. The list shape was considered and declined; the
reasoning is in design.md § What was considered and declined.

Both options and the two declined shapes are laid out in design.md. The full set
of decisions this packet takes on its own authority, each flagged for veto, is
in § Decisions put to the review.

## Impact

- **Affected specs.** `credential-contracts` — 3 ADDED requirements AND 1
  MODIFIED. The MODIFIED block is on "Dispatch-only credential least privilege
  and serving-tier separation", added on the council's ruling: this packet
  changes the behaviour of the check that enforces that requirement's
  distinct-binding half, so the requirement that PUBLISHED the check now states
  the grouping and its fallback rather than having its enforced meaning change
  silently underneath it. **The block is scenario-complete** — all three canon
  scenarios restated verbatim, plus one for the fallback — and the
  double-delta hazard was checked and does not reach it: the two live MODIFIED
  deltas in active changes are on "Canonical credential record shapes"
  (`add-credential-escrow-checkout`) and "The credential vault operator is an
  execution binding" (`add-notebook-projection-identity`), neither of them this
  requirement. Measured after writing it, the `modified-block-currency` family
  reports NO finding against this block — it carries every promoted unit — so no
  `_LEDGER_SUBJECTS` registration is owed, and registering one would fail that
  gate's own fresh/gone check.
- **Affected code, at realization**: the schema's four optional fields, the
  validator's new refusal, refined refusal and warning channel, nine fixtures,
  and the test file that asserts the self-test counts.
- **The promoted dispatch-only separation requirement is untouched**, in text
  and in force: its bindings resolve two requirements, so the exemption's first
  condition is never satisfied for them.
- **`contracts/` is untouched by this proposal.** The ritual — changelog
  allocation, `contract_bundle_version` bump, inventory rebuild, `verify-commit`,
  `verify-promotion`, annotated tag — is scheduled in tasks.md § 5 and performed
  at realization. Nothing in this packet moves a bundle member, so ratifying it
  drifts no release inventory.
- **Merge-order coupling, named rather than discovered later.**
  `add-credential-escrow-checkout` is active, ratified, and edits the SAME
  schema file and the SAME validator, and owes the same next additive minor.
  RULED: two sequential cuts, this packet first, with that packet rebasing onto
  it — see decision 7 and tasks § 5.7.
- **No live secret is created, moved, or read by this change**, and none is by
  its realization either: the surface is a schema, a validator, and fixtures.

## Decisions put to the review

Each was taken by the authoring session on the evidence cited in design.md, and
each is flagged for veto. None is covered by the origin citation.

1. **The `shared-secret-identity` position** — distinguish, on the shared
   requirement. § The decision this packet puts to the review, above.
2. **`fetch_identity` as the record's single spelling**, with "access identity"
   surviving as a prose synonym and the ratified custody text left unedited.
3. **`requirement_id` rather than a new `requirement_ref`**, matching the grant
   template's existing field name.
4. **Four fields rather than the two task 4.5 names** (consumer and access
   identity). `requirement_id` is this packet's addition and carries the position
   in decision 1 — cutting it forces the alternative. `identity_namespace` is the
   council's addition under decision 9, and cutting it returns the cross-tenant
   over-report along with an escape clause naming an act the record cannot
   perform.
5. **Warning now, and `consumer`/`fetch_identity` required at the next major**,
   rather than required immediately — which the versioning policy forbids
   without a minor of warnings first. `requirement_id` is excluded from that
   path by the same rule, since its absence never warns.
6. **No `additionalProperties: false` on the binding object**, so a second
   spelling is not machine-refused at this minor; closing the object is a
   narrowing reserved for the next major version, and the limit is stated in the requirement
   rather than left for a reader to discover.
7. **TWO SEQUENTIAL CUTS, THIS PACKET FIRST** (ruled, no longer open), with
   `add-credential-escrow-checkout` rebasing onto this one. The coupling is NOT
   fixture residency — it is `_self_test` itself: `EXAMPLES_DIR` is hard-coded to
   `examples/credential-contracts` and `NEGATIVE_EXPECTATIONS` is a single
   module-level dict, so BOTH packets edit the same count string and the same
   registry whatever tree their fixtures live in. The rebase obligation is
   therefore certain rather than conditional, and it is written into tasks § 5.7
   naming the party that owes it.
8. **Regrouping the PUBLISHED `shared-secret-identity` check** onto the qualified
   key `(provider, vault, secret_ref)` instead of the bare `secret_ref` it groups
   by today, **WITH A FALLBACK TO THE BARE GROUPING WHEREVER THE QUALIFICATION IS
   UNESTABLISHED**. This is a behaviour change to a check this packet did not
   author, and it is the one place this packet reaches beyond its own surface.
   **THE UNCONDITIONAL FORM OF THIS REGROUPING WAS WRONG, AND THE CORRECTION IS
   RECORDED RATHER THAN QUIETLY APPLIED.** An earlier revision of this decision
   claimed it "only ever narrows a refusal, and only where the two secrets are
   genuinely distinct". **That claim is false and was disproven by execution in
   review**: where any member of a matching `(provider, secret_ref)` set omits
   the optional `vault`, an unconditional qualified key SPLITS the group and
   REMOVES a refusal that stands today — and the packaged negative
   `negative/dispatch-reuses-content-secret.yaml` is ONE OPTIONAL LINE from being
   exactly that record, so the backward-compatibility proof this packet relied on
   was one deletion from going green. With the fallback, the claim becomes true:
   the refinement removes no refusal in force today, keeps every genuine
   narrowing (two declared vaults, two declared providers), and
   `authority-scope-indeterminate` ACCOMPANIES a verdict instead of replacing
   one. Vetoing the regrouping leaves the exemption resting on a qualified
   identity test beside an unqualified secret test — see the honest gaps.
9. **A FOURTH OPTIONAL FIELD, `identity_namespace`, AT THIS MINOR** — the
   directory, account or tenant within the provider that issues the identity.
   Added rather than deferred, because the requirement's own escape clause ("or
   records the distinction") named a record the shape could not carry, which
   made the escape rhetorical. It is now bound to this field, so the escape is
   real. **RECONCILED WITH THE SECRET RULE SO BOTH FALLBACKS POINT THE SAME
   WAY**: absent the field, same-named principals under one provider are STILL
   REPORTED (silence is not distinctness); present and distinct, they are not.
   An earlier revision had the two rules pointing opposite ways — the secret side
   clearing on an omitted field while the identity side reported — and that
   incoherence is corrected rather than left standing.

## Honest gaps, recorded rather than assumed away

- **The declaration is an assertion, not a proof.** Nothing here reads the
  store's grants. A record naming two fetch identities that are in fact one
  principal is conforming and wrong. What this change buys is that the claim
  becomes writable, checkable and attributable — not that it becomes verified.
- **The comparison is per-document.** Two consumers split across two template
  files are not compared, so the rule can be evaded without any record saying
  so. That bound was already true of `shared-secret-identity` and is now stated
  instead of implied; cross-document comparison is owed to a successor.
- **A second spelling validates silently at this minor.** See decision 6.
- **Qualification is no defence against a false record.** A binding that
  misdeclares its provider or vault escapes every comparison here, because
  nothing reads the store. Qualification removes false refusals; it does not
  make a declared authority true.
- **`vault` is optional, so the SECRET qualification is sometimes
  indeterminate.** The packet warns rather than guessing in either direction,
  which means a real collision can sit behind an omitted optional field with
  only a warning against it. Making `vault` required would close that and is a
  narrowing this minor may not perform. The identity comparison never reaches
  this state, because `provider` is required.
- **The identity namespace is only as fine as what the record declares.** With
  `identity_namespace` present and distinct, two same-named principals are two
  authorities. With it ABSENT the comparison falls back to `provider` alone and
  reports them — chosen over the silent opposite, and now escapable by declaring
  the field rather than by an instruction with nowhere to record it.
- **`provider` and `vault` are PLACEHOLDERS BY RULE in this repository's own
  neutral templates, not merely sometimes-absent.**
  `contracts/avatar-client/broker-server-key-binding.template.yaml` declares
  `provider: "<per-install-vault-provider>"` and `vault: "<per-install-vault-name>"`
  — placeholders by rule in its own words, because a neutral template may not
  name a store. So in `contracts/` template records the qualification adjudicates
  TOKENS rather than stores, and two placeholders that resolve to one real vault
  would split a group that should not split. This is not the misdeclared-record
  gap above: it is a CORRECT record following the repository's own template
  idiom. It is also a second, independent argument for the fallback, which does
  not depend on `vault` values being meaningful.
- **Declaring the map key's meaning makes a new pattern lawful.** Stating that
  the map key is a binding identifier and `requirement_id` the declared relation
  legalises multiple bindings per requirement — a shape previously not forbidden
  so much as never contemplated, its unavailability inferable only from the
  silence of every packaged example. That is a widening of what a conforming
  record may look like, and it is recorded as one rather than presented as pure
  clarification.
- **The shipped `resolution.fetch_identity` in
  `contracts/avatar-client/broker-server-key-binding.template.yaml` is not
  migrated by this change.** It stays valid — nothing narrows — and
  reconciling it to the per-binding field is named as owed to
  `qualify-avatar-live-voice`, which is active and owns that record. A packet
  that adds a field does not edit another active change's artifact to use it.
- **Representability is not containment.** The custody packet already recorded
  that revoking one binding cannot un-disclose a fetched password nor end an
  established session, and that eviction requires rotation reaching every
  consumer. Making the authorities visible in the record changes none of that,
  and this packet claims no part of it.
