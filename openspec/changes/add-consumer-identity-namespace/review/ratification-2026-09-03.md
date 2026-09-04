# Proposal Ratification: add-consumer-identity-namespace

Status: ratified
Decision date: 2026-09-03
Ratifier: Brett Heap (repository owner) — in-session ruling
Ratified: 2026-09-03 by Brett Heap (repository owner) — in session, verbatim
"implement your recommendations on all these", over written recommendations for
five queued items of which TWO are this packet's. Record: this file.
Ratified baseline: this change as committed in the commit carrying this record
(`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`,
`specs/credential-contracts/spec.md` — 2 MODIFIED requirements, 0 ADDED, 31
scenarios), validated `--strict` and `--all --strict`.

## Decision

**RATIFY, ON TWO RULINGS OF ONE DAY CARRIED BY ONE PACKET.**

Brett Heap ruled in session on 2026-09-03, on a lane's written recommendations
for openxFactory issues #561/#339, #318, **#511**, **#553** and #543 fix (b),
verbatim:

> **"implement your recommendations on all these"**

Two of the five land inside ONE requirement of `credential-contracts`, so they
ride in one `## MODIFIED Requirements` block. Both rulings are recorded as
comments on their issues, dated 2026-09-03T14:42Z, and both are quoted below in
full so this record is readable without leaving it.

## Ruling one — openxFactory #511

> **Add `identity_namespace`** as an additive optional member of the `consumer:`
> block naming the issuing directory/account/tenant WITHIN the provider;
> `shared-authority-identity` compares on `(identity_namespace, fetch_identity)`
> and falls back to the bare identity when the member is absent, so the rule
> still REPORTS rather than clears. Lands under the change's declared-at-the-
> minor / constrained-at-the-major phasing as the ninth warning shape. Vehicle:
> an OpenSpec change on `credential-contracts` with a code surface (schema,
> validator, fixtures, CHANGELOG, manifest row); the contract CUT is NOT part of
> it and follows the release ritual.

**The origin of the finding**, carried from the issue rather than re-derived: the
2026-08-29 `merge_readiness_council` convening on PR #493, seat `lead-security`,
finding **LS-F3** (with #493 decision 9); ported on Brett's 2026-08-30 ruling
closing #493 as superseded by #497, and RE-VERIFIED against #497's ratified text
by prototype on 2026-08-30 — so it applies to the ratified line and not only to
the superseded draft.

## Ruling two — openxFactory #553

> **AMEND the promoted scenario, do not broaden the resolver.**
> `credential-contracts`' scenario "The requirement reference resolves to more
> than one record" is amended so canon states the per-document scope the frozen
> resolver enforces (more than one record IN THE DOCUMENT THE REFERENCE NAMES);
> ids stay namespaced by document, and repository-wide uniqueness is not a rule.
> Vehicle: one doc-only OpenSpec change (`code_surface: none`). The resolver, its
> `ambiguous` status and `tasks.md` § 3.4's freeze are untouched.

**THE VEHICLE MOVED AND THE RULING DID NOT.** The ruling names "one doc-only
OpenSpec change"; this packet carries a code surface, and #553's edits inside it
carry none — no code, no status, no severity, no resolver line. The change of
vehicle is recorded on issue #553 itself (comment of 2026-09-03T14:51Z) with the
reason, and the reason is a governance fact: a `## MODIFIED Requirements` block
REPLACES a requirement wholesale, #553's target sits inside the requirement #511
must modify, and two live blocks on one requirement cannot both survive — the
second to archive silently reverts the first. The lane holding #553 stood down
before authoring; its branch is deleted.

## What this ratification covers

The SUBSTANCE both rulings state, and the recommendations they were given over:

- the member, its name, and its optionality;
- the comparison on the pair, and the fallback that REPORTS rather than clears;
- the ninth warning shape under the block's existing phasing;
- the per-document scope of the ambiguity, with ids namespaced by document and
  repository-wide uniqueness not a rule;
- the exclusion of the contract CUT from this change;
- the resolver, its `ambiguous` status, and § 3.4's freeze staying untouched.

## What this ratification does NOT cover

**IT IS NOT A READ OF THIS TEXT, and saying so is the point of this section.**
The ruling was given over written recommendations, not over the requirement
prose in `specs/credential-contracts/spec.md`, the decisions in `design.md`, or
the realization in `tasks.md`. Nothing in those was ruled on; they are the
authoring session's, and § Authoring decisions in `proposal.md` states each with
the alternative that was rejected so it can be ruled the other way.

**NO COUNCIL SAT AND NONE WAS PRESCRIBED.** Unlike its predecessor
`add-binding-consumer-identity`, this packet was not put to a §7.4-shaped bench.
That is a consequence of the ruling's form — one word over five items — and it
is recorded as such rather than presented as a bench that agreed.

**IT DOES NOT AUTHORIZE A CUT.** No release tag, no digest inventory, no
version-headed `contracts/CHANGELOG.md` entry. `tasks.md` § 5 prescribes that
entry verbatim for whoever cuts.

**IT DOES NOT SETTLE THE THREE OPEN QUESTIONS** in `proposal.md`. OQ-1 (a
namespace on the holder side, for a cross-repository comparison), OQ-2
(reconciling a declared namespace against the provider) and OQ-3 (`MAJOR_RELEASE`
reading `contract-v3.0` in the validator while the policy entry has been restated
to `contract-v4.0`) are OPEN and routed, and OQ-3 in particular is a drift this
packet OBSERVED and deliberately did not repair.

## Conscious-acceptance notes

1. **The comparison change is a SUBTRACTION.** It can only make a pair that is
   reported today go silent, and only when both bindings declare a grammatical
   namespace and the two DIFFER. Every other combination falls back to the bare
   identity and behaves exactly as the shipped validator behaves.
2. **ONE narrowing is taken and it is named**: `baked-secret` over the third
   free string, under `add-binding-consumer-identity` § 2.6's own precedent.
3. **The ninth code's deprecation window opens at ITS OWN minor**, not at
   `contract-v2.4` — stated in `docs/contract-versioning-policy.md`, because a
   row that borrowed a window it never served is the exact defect that entry
   exists to prevent.
4. **No live secret is created, moved, or read.** The member names a directory;
   it holds no material, and the packaged fixtures carry SYNTHETIC identifiers
   under the ruling of 2026-08-29 that governs this corpus.
5. **Two `release-inventory-drift` findings are expected and are the CUT's.**
   `contracts/manifest.yaml` and `docs/contract-versioning-policy.md` are members
   of the standing `contract-v3.0` inventory. The family's own remedy line
   forbids hand-editing an inventory to make the comparison pass, and this packet
   does not.

## Next

Realization rides with this packet in one PR — the schema member, the shared
predicate, the ninth code, the five fixtures, the tests, the manifest row and
the docs. The change archives on merged code plus green evidence per
`release-realization`; the CUT is a separate act and follows the release ritual.
