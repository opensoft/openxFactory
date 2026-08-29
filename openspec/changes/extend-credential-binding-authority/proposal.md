---
code_surface: openxFactory — a SCHEMA CHANGE plus its validator, fixtures and tests. `contracts/schemas/xfactory-credential-contracts.schema.yaml` gains THREE ADDITIVE OPTIONAL FIELDS on each entry of `credential_bindings` in the existing `xfactory_credential_binding_template`: `consumer`, `fetch_identity` and `requirement_id`. `scripts/validate-credential-contracts.py` gains one new refusal (`shared-fetch-identity`), one refinement of an existing refusal (`shared-secret-identity` gains a narrowly-conditioned exemption that opens only on positive declarations), and its FIRST WARNING CHANNEL (`binding-authority-undeclared`, warning at this major and error at the next). `examples/credential-contracts/` gains one positive fixture and two negatives; `tests/credential_contracts/test_dispatch_credential_contract.py` moves with them, including the self-test count string it asserts. NO NEW RECORD KIND. NO REQUIRED FIELD. `contracts/` IS UNTOUCHED BY THIS PROPOSAL — the release ritual is scheduled in tasks.md § 5 for realization, and no bundle is cut by the packet that proposes it.
target_release: THE NEXT ADDITIVE MINOR, DELIBERATELY NOT NUMBERED HERE. `docs/contract-versioning-policy.md` states the rule this front-matter obeys: "A proposed change MUST NOT reserve a minor number before merge order is known." Measured on this branch's base rather than recalled: `contracts/manifest.yaml:3` declares `contract-v2.1` and `contracts/CHANGELOG.md:12` heads at `contract-v2.1 — 2026-08-28`, so `contract-v2.1` IS SPENT and any earlier note naming it, or any other specific number, as this work's target is stale. `contract-v2.2` is the EXPECTED allocation and is deliberately NOT RESERVED here, because the active ratified packet `add-credential-escrow-checkout` edits the same schema file and owes the same next minor — a number written here is a number another packet may spend first, which is what the policy sentence above exists to prevent. That packet's front-matter declines to number itself for exactly this reason, and the `contract-v1.28` renumber sweep is the standing precedent for the cost of doing otherwise. The number is allocated at realization by merge order (tasks.md § 5.2). WHY A CUT IS OWED AT ALL, MEASURED RATHER THAN ASSUMED: parsed on 2026-08-29, `contracts/releases/contract-v2.1.digests.yaml` holds 192 entries, exactly five of them under `contracts/schemas/`, and `xfactory-credential-contracts.schema.yaml` IS NOT ONE OF THEM — neither is its validator, nor anything under `examples/`. So the cut is NOT forced by `release-inventory-drift`, which is the usual reason a schema edit owes one. It is owed by the VERSIONING POLICY instead: the schema is a registered bundle contract (`contracts/manifest.yaml`, `id: credential-contracts`), and a registered contract gaining optional fields and validator warnings is that policy's ADDITIVE (MINOR) class verbatim, under which "Domain repos on the same major version remain conformant without changes". The three fields becoming REQUIRED is the BREAKING (MAJOR) class and is scheduled for the next major, not for this cut.
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
`xfactory_credential_binding_template` requires `[provider, secret_ref, owner,
rotation_policy]` with `vault` optional. There is no field for who consumes the
credential and none for what identity reaches the store, and
`scripts/validate-credential-contracts.py` compares no authorities at all. Two
bindings naming one vault principal validate cleanly today. So does one binding
naming two — the record cannot tell the difference, which means no check can.

**The unclaimed key already exists in this repository, in a contract
artifact.** This is the forcing fact, and it was found by reading the tree
rather than by reasoning about it.
`contracts/avatar-client/broker-server-key-binding.template.yaml` is
`kind: xfactory_credential_binding_template` — the very record kind this packet
extends — and it already carries `fetch_identity:
install_federated_workload_identity`, in a document-level `resolution:` block
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

**Three optional fields, on the binding, in the estate's own words.** Each entry
of `credential_bindings` may declare `consumer` (the consuming system),
`fetch_identity` (the identity that consumer authenticates to the secret store
with), and `requirement_id` (the credential requirement the binding resolves).
No new record kind, no new envelope, no required field.

**`fetch_identity`, not a second spelling.** The promoted requirements already
say the lane receives "an opaque secret reference and a fetch-identity
identifier" and that reference delivery is "a vault URI plus the runtime's own
fetch identity"; a shipped record of this kind already uses the key. "Access
identity", the custody packet's prose and the projection documentation's, names
the same thing — the synonym stands in prose and the RECORD gets one spelling.
The ratified custody text is not edited to match: a ratified delta is not
rewritten for a successor's convenience, and the requirement states the
synonymy instead.

**One new refusal.** `shared-fetch-identity`: two bindings declaring the same
fetch identity while naming different consumers. That collision IS the
violation of "one identity may be shared, one authority may not", and it is now
a finding rather than a review note.

**One refinement, opened only by saying more.** `shared-secret-identity` keeps
refusing a shared `secret_ref` EXCEPT where every binding sharing it declares
the same `requirement_id` and pairwise-distinct `consumer` and `fetch_identity`.
Every existing record is adjudicated exactly as before, because each condition
is a positive declaration no existing record makes — including the packaged
negative, which stays red.

**A warning channel the validator has never had.** A binding declaring neither a
consumer nor a fetch identity warns, naming both fields, and stays valid. New
optional fields plus new validator warnings is the additive class; the fields
become required at the next major, which is the breaking class and owes at least
one full minor of warnings first. This is the `contract-v1.34` pattern — deprecate
in a minor with the removal version named in the changelog, refuse at the major.

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
identities" would admit the exact record `examples/credential-contracts/negative/
dispatch-reuses-content-secret.yaml` exists to refuse. Only "the sharing
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

- **Affected specs.** `credential-contracts` — 3 ADDED requirements. **NO
  requirement is MODIFIED**, deliberately and after checking: two of the seven
  promoted requirements already carry live deltas from active changes
  (`add-credential-escrow-checkout` on "Canonical credential record shapes",
  `add-notebook-projection-identity` on "The credential vault operator is an
  execution binding"), and a second live delta on one requirement is the exact
  hazard the custody packet's design refused. The obligations here are additive
  in substance as well as in bookkeeping: representability is not a refinement
  of the shapes requirement, it is a new fact the record must be able to state.
  Carrying no MODIFIED block also means this packet owes no
  `modified-block-currency` carriage-ledger registration.
- **Affected code, at realization**: the schema's three optional fields, the
  validator's new refusal, refined refusal and warning channel, three fixtures,
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
  Whichever lands second rebases onto the first; whether the two ship one
  combined cut or two sequential ones is a question for the review, put in
  design.md.
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
4. **Three fields rather than two.** Task 4.5 names two (consumer and access
   identity); `requirement_id` is this packet's addition, and it is what carries
   the position in decision 1. Cutting it forces the alternative.
5. **Warning now, required at the next major**, rather than required
   immediately — which the versioning policy forbids without a minor of warnings
   first.
6. **No `additionalProperties: false` on the binding object**, so a second
   spelling is not machine-refused at this minor; closing the object is a
   narrowing reserved for the major, and the limit is stated in the requirement
   rather than left for a reader to discover.
7. **One combined cut or two sequential ones**, with `add-credential-escrow-checkout`.

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
