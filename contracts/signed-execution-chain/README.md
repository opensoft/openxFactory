# Signed Execution Chain Contract Family (tranches one and two)

Status: ratified
Ratified by: add-signed-execution-chain (tranche one, ratified 2026-08-29 by
Brett Heap, repository owner, in session; record
`openspec/changes/add-signed-execution-chain/review/ratification-2026-08-29.md`)
and add-chain-attestation (tranche two, ratified 2026-09-01 by Brett Heap at
`f54cb5bc`, re-ratified at `6d7ef17b` after the amendments that head's own
verdict forced)
Kind: reference
Repository context: openxFactory owns this neutral contract. It is REALIZED and
**registered at `contract-v2.5`** in `contracts/manifest.yaml` +
`contracts/CHANGELOG.md` — `tasks.md` 4.7, performed by the cutting session
rather than by the realization, per
[Contract Versioning Policy](../../docs/contract-versioning-policy.md), because a
proposed change MUST NOT reserve a minor number before merge order is known. The
number was fresh-counted at the cut and had already moved twice. **Tranche two
registers at `contract-v2.6`** (`add-chain-attestation` task 5.9): its eight new
schemas carry per-file `sha256` rows, and the four tranche-one schemas its
additive extension moved carry refreshed digests with the extension noted inside
each row's rule. All thirteen schemas below carry a per-file `sha256` in the
manifest; the corpora, this README, the reader and its pytest wiring are
content-addressed by commit.
**REGISTRATION IS NOT ENFORCEMENT, AND ENFORCEMENT ARRIVED SEPARATELY.** The cut
published bytes; the ruleset act made them bite. Since **2026-08-31**
`signed-execution-chain-gate` is a REQUIRED check on `main` — opensoft org
ruleset **21957695** (`tasks.md` 4.5), seen refusing a real pull request on canary
**#549** (`tasks.md` 4.6) — so this family now confers and refuses what it says it
does. See § What this family does NOT do for what is still outstanding.
**TWO OF THE FIVE SCHEMAS HAVE MOVED SINCE THAT CUT, ADDITIVELY, AND THE NEXT CUT
IS OWED RATHER THAN TAKEN HERE.** `add-chain-anchoring` widens the `leaf_type`
enumeration by twelve, adds ONE optional member (`anchor_event`) and widens
`digest_subject` by eleven: no required field is added, no shape is removed, and
no existing member's meaning changes, so every instance valid at `contract-v2.5`
stays valid — measured by re-validating the whole packaged corpus at the new head
rather than claimed. The manifest's per-file `sha256` for
`transparency-log-leaf` and `digest-construction` moved with those bytes so the
rows stay true; the version number and its CHANGELOG entry are the cutting
session's, per the same rule that kept `tasks.md` 4.7 out of the realization —
**a proposed change must not reserve a minor number before merge order is
known**.

## What this family is for

**The family already signs the decision, and then loses the signature.**
`add-wallet-carried-review-authority` made review authority a wallet-carried
grant with a root issuer anchored to a named operator. That is a signed
ratification. What happens next is unsigned: the work runs in a lane that cannot
prove it descended from that ratification, and the merge gate that lets it land
cannot ask.

**A validated chain is not an audit trail — it is a permission.** An audit trail
is written after the fact and can be forged after the fact. A chain a gate WALKS
before it permits the terminal act cannot be, because the act does not happen
without it.

Tranche one is **links 1–3 plus the signed transparency log plus the short-chain
gate**, which is what Brett Heap's Q4 ruling of 2026-08-29 fixed. **Tranche two
is links 4–6 and 10 — what actually ran, said by the chain itself**: the harness
controller attesting the environment it prepared and COMMITTING to the expected
attestation set; per-task runner attestations signed AT the controller on
RECORDED, ATTRIBUTED requests under composed tier-2 identities; the pull-request
open as a signed, chain-bound decision; and CLOSURE, where the governed
post-merge test the ratified subject names is what completes the chain and a
merged-but-unclosed chain is a REFUSING state. Tranche three (on-chain
anchoring, `add-chain-anchoring`) is the remaining NAMED successor: nothing here
operates a certificate authority, holds a private key, or places anything on any
chain.

**AND TRANCHE THREE NOW HAS ITS LEAF KINDS IN THIS GRAMMAR, WHICH IS A DIFFERENT
THING FROM HAVING AN ANCHOR.** `add-chain-anchoring` tasks.md 5.3 settles the
twelve leaf kinds its requirements 3, 4, 7 and 8 mandate **inside
`transparency-log-leaf.schema.yaml`**, on its own stated ground — *"This packet
adds no second grammar and must not, so tranche one's grammar is where each event
discriminator and its required fields are settled"* — and adds its eleven digest
subjects to the single `digest_subject` enumeration on
`digest-construction.schema.yaml`'s own written invitation. See
[`../chain-anchoring/`](../chain-anchoring/) for the family that produces those
leaves. **The sentence above is unchanged by that**: still nothing here mints an
anchor, configures a witness, captures a receipt or places anything on any chain,
and `add-chain-anchoring`'s operator conditions are ungated and unticked. What
changed is that when an anchoring realization writes its evidence, it writes it
as leaves of THIS log under THIS grammar — and a shape exists to refuse a
malformed one.

## The thirteen files

Tranche one's five, then tranche two's eight (`add-chain-attestation`, an
ADDITIVE extension — four of the five earlier files moved additively with it and
not one published member was removed, renamed or narrowed).

| File | What it declares |
| --- | --- |
| [`digest-construction.schema.yaml`](digest-construction.schema.yaml) | **THE ONE CONSTRUCTION IN FORCE**, `xfc-jcs-sha256-1`, and the digest shape every record takes by `$ref`. It declares NO record kind: it exists so the family cannot grow a second construction rule beside the first |
| [`chain-inception.schema.yaml`](chain-inception.schema.yaml) | Links 1 and 2 as ONE signed act — the `signed_ratification` block the signature covers, and the chain identity that is its digest |
| [`traveling-contract.schema.yaml`](traveling-contract.schema.yaml) | Link 3 — the signed ratification carried WITH the work, checkable at the point of use with no live service in reach |
| [`transparency-log-leaf.schema.yaml`](transparency-log-leaf.schema.yaml) | One signed, hash-linked leaf of the append-only log that is this capability's primary chain of custody. **The leaf grammar for the whole estate**: its `leaf_type` enumeration carries this capability's four acts, tranche two's seven record kinds AND the twelve `add-chain-anchoring` settles here rather than in a second family |
| [`conformance-declaration.schema.yaml`](conformance-declaration.schema.yaml) | A realization's obligation-by-obligation declaration, on `add-trust-anchor`'s ratified declared-shortfall pattern — closed over NINE obligations at tranche one and over all EIGHTEEN for a declaration naming any tranche-two obligation, with the `attestation_design` block carrying the three obligations a gate cannot see |
| [`attestation-common.schema.yaml`](attestation-common.schema.yaml) | Tranche two's shared definitions, taken by `$ref`: the signature block with THE SIGNER'S PUBLIC KEY CARRIED BESIDE IT, the predecessor hash link, the per-fact EVIDENCE CLASS (closed at three members, composing with the ratified trust-anchor chain-custody registry in a declared ORDER), and the recorded signing request |
| [`setup-attestation.schema.yaml`](setup-attestation.schema.yaml) | Link 4 — the controller attests the environment IT PREPARED and COMMITS to the expected attestation set inside the same signed bytes, under a certificate whose anchor, issuance evidence and standing-at-signing are named |
| [`commitment-extension.schema.yaml`](commitment-extension.schema.yaml) | The same commitment written later, for fan-outs discovered as the work runs, with the deadline at DISPATCH — an extension written after dispatch is a description, not a commitment |
| [`signed-chain-binding.schema.yaml`](signed-chain-binding.schema.yaml) | The third leg of a tier-2 identity's composed issuance: subject scope, the CLOSED enumeration of authorized record kinds, and THE CHAIN IDENTITY SERVED — consuming `add-trust-anchor`'s `certificate-record` and `issuance-evidence` and redefining neither |
| [`runner-attestation.schema.yaml`](runner-attestation.schema.yaml) | Link 5 — what actually ran, per task, signed AT the controller on a RECORDED request attributed from the controller's own provisioning, corroborated against link 4 and never notarized |
| [`pr-open-decision.schema.yaml`](pr-open-decision.schema.yaml) | Link 6 — opening the pull request as a signed decision under the chain-scoped identity, enumerating EVERY committed attestation and binding the PR identifier and head revision inside the signed bytes. PROPOSING IS NOT PERMITTING |
| [`closure-record.schema.yaml`](closure-record.schema.yaml) | Link 10 — the point a chain COMPLETES: the governed post-merge test the ratified subject names, controller-dispatched, on exactly the merge commit, authenticated and PASSING, with the three amendment-lineage limbs verified against the inception's signed lineage |
| [`remediation-declaration.schema.yaml`](remediation-declaration.schema.yaml) | The ONE admitted consumer of an unclosed chain — itself a full chain, its exemption non-inheritable, its own closure owed |

The canonical reader is
[`scripts/validate-signed-execution-chain.py`](../../scripts/validate-signed-execution-chain.py),
self-testing over TWO packaged corpora, each adjudicated alone: tranche one's in
[`examples/`](examples/) and [`examples/negative/`](examples/negative/), and
tranche two's in [`examples/tranche-two/`](examples/tranche-two/) and
[`examples/tranche-two/negative/`](examples/tranche-two/negative/). The split is
forced by the log rather than chosen — the append-only rule is a store-wide
obligation, and a tranche-two chain sharing tranche one's store would have
collided with the leaf positions its shipped negatives probe.

## The three things settled at realization

`tasks.md` §3 required these to be fixed BEFORE schemas were authored, because
they are contract content — cheap now and expensive after a bundle ships. The
`openxwallet` custody enumeration is the standing precedent for how quietly a
wrong set re-opens the hole the rule was written to close.

### 1. The chain-identity digest — algorithm, and the exact byte range

`xfc-jcs-sha256-1`: **RFC 8785 JSON Canonicalization Scheme** over the digest
subject, restricted to the value classes this family admits (object, array,
string, integer, boolean, null — a non-integer number is REFUSED rather than
serialized), then **SHA-256**, rendered `sha256:` + 64 lowercase hex. Chosen
against a published standard rather than invented, and BOUNDED rather than
half-implemented: ECMAScript number serialization is the one part of JCS a
second implementation reliably gets wrong, and a digest two readers compute
differently is worse than a digest one of them refuses.

**THE EXACT BYTE RANGE IS THE `signed_ratification` BLOCK** — the block the
ratifying signature covers, and nothing outside it. The signature sits beside
that block, not inside it, so the digest is well defined and the signature input
does not depend on the completed signature.

**Three digests, three subjects, and every digest NAMES its own.** The
ratification's CONTENT digest is taken over the subject ratified and is what an
exercise's `object_ref` carries. The CHAIN IDENTITY is taken over the signed
ratification — a strict superset, since the signed bytes also carry the
presentation reference, the per-act value and the actor binding. A LEAF digest is
taken over a leaf's content. The content digest and the chain identity MUST NOT
be equated: the equation rejects every conforming chain, and it is unbuildable in
the other direction because `object_ref` would then commit to a signature not
yet made.

### 2. The leaf grammar — what a leaf carries, and how leaves hash-link

Chosen against **RFC 6962 / Certificate Transparency and Sigstore Rekor**, taken
as a **hash-linked signed leaf sequence**. Each leaf carries its `leaf_index`,
the `tree_size` it completes, its predecessor's digest, its own digest (over the
leaf content — the record with `leaf_digest` and `leaf_signature` removed) and
its own signature.

**THE HEAD IS THE NEWEST LEAF.** Because every leaf commits to its predecessor
and is signed, any leaf is a signed head of the prefix ending at it, and no
separate tree-head record exists or is needed. A consistency proof against a
previously observed head is the re-derivation of the link chain from that
observed leaf forward.

**What a verifier reads to detect an edit**: the link chain. Alter or drop a leaf
inside a prefix some party has observed and every subsequent predecessor digest
stops matching; and every traveling contract carries the digest of the leaf that
recorded its inception, so a truncation dropping an observed leaf is caught at
the point of use. **What it does not detect** is suffix truncation nobody has yet
observed — DECLARED in the conformance declaration's SEC-R6 entry, closed by
tranche-three anchoring, and never papered over. **The leaf kinds for that
anchoring are settled in this grammar as of `add-chain-anchoring`, and settling a
leaf kind witnesses nothing**: SEC-R6 stays declared and open until an anchor
actually lands.

**HOW THE TWELVE ARE PAIRED TO THEIR FIELDS, AND WHY IT IS STRONGER THAN THE
VERDICT PAIRING BESIDE IT.** One new OPTIONAL member, `anchor_event`, carries the
per-kind fields, and thirteen `if/then` conditionals close the shape over all
sixteen leaf types: each anchoring type REQUIRES its own `anchor_event` shape and
FORBIDS `verdict`; the four tranche-one types FORBID `anchor_event`. Each shape
pins `event` to a `const` equal to its leaf type, so an event block from another
kind is UNREPRESENTABLE rather than merely refused by a reader. Tranche one left
the equivalent verdict pairing to the canonical validator; this is the family's
own stated preference applied — *"where a shape can refuse a thing, the shape
refuses it"* — and the older, weaker handling is named as such in the schema
rather than presented as equivalent. **One kind is DELIBERATELY EXCLUDED**:
`add-chain-anchoring` requirement 4 also mandates a validation-failure leaf, and
that is a GATE VERDICT which `gate_verdict` already carries — settling it a
second time would mint exactly the second grammar 5.3 forbids.

### 3. The log's home — the register precedent, in this repository

The log lives **in the repository that holds the records**, on the precedent
`governance/review-authority/register.yaml` set: a tracked file whose READER is
the shape. The decision is forced rather than preferred. Requirement 9 requires a
named validator running as a required check **on the repository that holds the
records**; and requirement 5 requires a point-of-use checker to establish a
traveling contract's consistency **with no live service in reach**. A governed
store outside the tree satisfies neither.

**No live log instance exists yet, and that is the honest state.** Inception is a
human act with a wallet-held key; this realization mints no chain, so there is
nothing to append. `scripts/validate-signed-execution-chain.py` says so in its
repo-scan note rather than reporting an empty sweep as a pass.

## The eleven ordered checks, and the rules that are not among them

The gate walks eight checks over links 1–3 — signature, chain-identity
recomputation, the `object_ref` replay comparison, the inception leaf's
commitment, the traveling contract's carried values, the actor binding, the proof
of possession, and standing plus holder class — and, SINCE TRANCHE TWO, three
further legs at their own positions in THE SAME ONE WALK: the setup attestation
established and committed, the runner attestations equal to the committed
expectation, and the open decision bound to its chain and its pull request. **It
is the same required check reading further, never a second gate** (`tasks.md`
4.5 of the tranche-two packet), and a new `links_1_3` verdict over a chain
carrying tranche-two records is refused as understated. **The list is closed,
and closing it is itself an obligation**: every requirement of this capability
is either walked there or has its enforcement point named — including the three
tranche-two obligations a gate CANNOT see, which are declared in the
conformance declaration's `attestation_design` block and refused there by name.
The rules enforced over the SCOPE rather than at the gate — atomicity,
per-ratification uniqueness, the log's append-only property, the conformance
declaration, and tranche two's chain-completeness horizon rules — are in the
validator's own docstring, where the reader that runs them is.

## What this family refuses, by name

**Ninety-five closed refusal codes over 108 packaged negatives** — tranche one's
twenty-four over 34, tranche two's seventy-one over 74 — **each code with a
negative that provokes it**; the self-test refuses a code with no probe. The
nine tranche-one `tasks.md` 4.2 names are among them, and so is tranche two's
full roster: the forged lane-minted identity refused at issuance, the dropped
attestation caught by the committed expectation, the notarized self-report, the
custody-ceiling promotion, the orphan pull request, the reused link-6 decision,
the lane-claimed pass, the replayed review, the unsupported lineage, the
merged-but-never-closed chain, the inherited exemption, and the design breaches
declared in `attestation_design` — key-in-worker, co-located controller,
reachable hardware custody, reusable delegation, execute-then-verify and the
rest.

Obligations refused BY SHAPE instead, because unrepresentable is stronger than
refused: an actor carrying no wallet attestation, a ratification whose actor
binding sits outside the signed bytes, a record with no recorded signing
request (the member is REQUIRED), an unclassed attested fact, and a second
digest construction (every digest member is `$ref` to the one construction and
its name is `const`).

## What this family does NOT do

- **It confers and refuses only what a required check can.** This entry read *"it
  confers and refuses nothing yet"* until 2026-08-31, and that was the true
  reading: `signed-execution-chain-gate` ran on every pull request and was **not
  required**, so these records were documentation that governed nothing. It is
  required now — opensoft org ruleset **21957695**, `~DEFAULT_BRANCH` of
  openxFactory, enforcement active — and the distinction that made the wait
  meaningful is unchanged: a merged workflow file is not evidence that a check is
  required; the live ruleset state is (`add-wallet-carried-review-authority` tasks
  2.5/2.6 drew it for `wallet-validation`, org ruleset **21538893**). The reader
  was then SEEN refusing rather than assumed to refuse, on canary PR **#549**. The
  conformance declaration records `is_required_in_ruleset: true` and the standing
  `reader-not-required` warning no longer fires. **What that does NOT mean**: the
  ruleset carries an `OrganizationAdmin: always` bypass, as every ruleset in this
  org does, so the gate is as strong as the estate's other required checks and no
  stronger.
- **It defines no second identity, grant, proof-of-possession or certificate
  vocabulary.** The presentation is the shipped `xfactory_wallet_grant_exercise`
  and the signing wallet the shipped `xfactory_wallet_record`, consumed at the
  `wallet-v1.3` digest pin ([`../openxwallet-pin.yaml`](../openxwallet-pin.yaml));
  the actor is `identity-brokering`'s `actor_subject_reference` carrying an
  `xfactory_wallet_subject_attestation`. Carried blocks are validated against the
  PINNED schemas whenever the `openXwallet/` gitlink is present, and the gate
  passes `--require-pinned-wallet-vocabulary` so a run that cannot reach the pin
  refuses rather than degrading silently.
- **It is not 025 FR-008's enrollment.** Chain inception creates no
  `merge-approval-envelope`, names no candidate class, touches no ruleset and
  produces no verdict; FR-008 stays gated exactly where the 2026-08-28 convening
  left it.
- **It defines the attestation vocabulary and operates none of it.** This
  realization creates no certificate authority, mints no tier-2 identity, holds
  no private key and dispatches no controller — the fixture keys in the packaged
  corpus exist as public halves, digests and signatures only. The two §5 gates
  the tranche-two packet names stay open until the PKI plane
  (`implement-openxpki-install-repo`) has ISSUED and the omnigent layer has
  REFUSED, and SEC-R18 is declared UNMET rather than partially met until then.
- **It holds no anchor, witness, commitment or receipt VALUE**, and no attestation
  identity of any kind. Those are the named tranche-three and tranche-two
  successors, and their absence at this tranche is NOT a defect. This entry read
  *"It holds no anchor, witness, commitment or receipt"* until
  `add-chain-anchoring` settled its twelve leaf kinds in this family's leaf
  grammar, and the correction is to the NOUN and not to the claim: what the
  family now holds is the EVENT-RECORDING GRAMMAR for those acts — the twelve
  `leaf_type` members, the `anchor_event` shapes and the eleven digest subjects —
  which is a different object from a value. No anchor is minted here, no witness
  is configured, no receipt is captured, nothing reaches any network, and this
  repository operates no anchoring subsystem: `add-chain-anchoring`'s operator
  conditions are ungated and unticked. **Settling a leaf kind is not running
  one**, and no reading of a leaf claims external undeniability the log alone
  does not provide.
