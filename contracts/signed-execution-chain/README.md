# Signed Execution Chain Contract Family (tranche one)

Status: ratified
Ratified by: add-signed-execution-chain (ratified 2026-08-29 by Brett Heap,
repository owner, in session; record
`openspec/changes/add-signed-execution-chain/review/ratification-2026-08-29.md`)
Kind: reference
Repository context: openxFactory owns this neutral contract. It is REALIZED and
**registered at `contract-v2.5`** in `contracts/manifest.yaml` +
`contracts/CHANGELOG.md` — `tasks.md` 4.7, performed by the cutting session
rather than by the realization, per
[Contract Versioning Policy](../../docs/contract-versioning-policy.md), because a
proposed change MUST NOT reserve a minor number before merge order is known. The
number was fresh-counted at the cut and had already moved twice. All five schemas
below carry a per-file `sha256` in the manifest; the corpus, this README, the
reader and its pytest wiring are content-addressed by commit.
**REGISTRATION IS NOT ENFORCEMENT** — see § What this family does NOT do, which
is still true in the present tense.

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
gate**, which is what Brett Heap's Q4 ruling of 2026-08-29 fixed. Tranche two
(the attestation links) and tranche three (on-chain anchoring) are NAMED
successors: nothing here mints an attestation identity, holds a certificate, or
places anything on any chain.

## The five files

| File | What it declares |
| --- | --- |
| [`digest-construction.schema.yaml`](digest-construction.schema.yaml) | **THE ONE CONSTRUCTION IN FORCE**, `xfc-jcs-sha256-1`, and the digest shape every record takes by `$ref`. It declares NO record kind: it exists so the family cannot grow a second construction rule beside the first |
| [`chain-inception.schema.yaml`](chain-inception.schema.yaml) | Links 1 and 2 as ONE signed act — the `signed_ratification` block the signature covers, and the chain identity that is its digest |
| [`traveling-contract.schema.yaml`](traveling-contract.schema.yaml) | Link 3 — the signed ratification carried WITH the work, checkable at the point of use with no live service in reach |
| [`transparency-log-leaf.schema.yaml`](transparency-log-leaf.schema.yaml) | One signed, hash-linked leaf of the append-only log that is this capability's primary chain of custody |
| [`conformance-declaration.schema.yaml`](conformance-declaration.schema.yaml) | A realization's obligation-by-obligation declaration, on `add-trust-anchor`'s ratified declared-shortfall pattern |

The canonical reader is
[`scripts/validate-signed-execution-chain.py`](../../scripts/validate-signed-execution-chain.py),
self-testing over the packaged corpus in [`examples/`](examples/) and
[`examples/negative/`](examples/negative/).

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
tranche-three anchoring, and never papered over.

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

## The eight ordered checks, and the four rules that are not among them

The gate walks eight checks over links 1–3 — signature, chain-identity
recomputation, the `object_ref` replay comparison, the inception leaf's
commitment, the traveling contract's carried values, the actor binding, the proof
of possession, and standing plus holder class. **The list is closed, and closing
it is itself an obligation**: every requirement of this capability is either
walked there or has its enforcement point named. Four rules are enforced over the
SCOPE rather than at the gate, because a gate sees only chains that were incepted
and only the chain in front of it — atomicity, per-ratification uniqueness, the
log's append-only property, and the conformance declaration. Both lists are in
the validator's own docstring, where the reader that runs them is.

## What this family refuses, by name

Twenty-four closed refusal codes over 34 packaged negatives, **each code with a negative that provokes
it** — the self-test refuses a code with no probe. The nine `tasks.md` 4.2 names
are among them: missing proof, failed verification, revoked-at-exercise, orphan
chain identity, digest mismatch on the traveling contract, mix-and-match
continuity, missing link, unevaluable chain, and a machine holder as ratifying
authority.

Two obligations are refused BY SHAPE instead, because unrepresentable is stronger
than refused: an actor carrying no wallet attestation, and a ratification whose
actor binding sits outside the signed bytes.

## What this family does NOT do

- **It confers and refuses nothing yet.** `signed-execution-chain-gate` runs on
  every pull request and is **not required** in the branch ruleset, so these
  records are documentation that governs nothing. A merged workflow file is not
  evidence that a check is required; the live ruleset state is
  (`add-wallet-carried-review-authority` tasks 2.5/2.6 drew that distinction for
  `wallet-validation`, org ruleset **21538893**). The conformance declaration
  says this in the present tense.
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
- **It holds no anchor, witness, commitment or receipt**, and no attestation
  identity of any kind. Those are the named tranche-three and tranche-two
  successors, and their absence at this tranche is NOT a defect.
