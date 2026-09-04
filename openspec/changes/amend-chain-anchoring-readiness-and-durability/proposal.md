---
code_surface: openxFactory — additive amendments to the ratified `chain-anchoring` contract family and its canonical validator; no deployable gateway, chain client, scheduler, or credential surface
target_release: next additive contract minor, allocated at realization by merge order
sequenced_after: [add-chain-anchoring]
---

# Amend Chain-Anchoring Readiness and Durability

Status: draft

## Why

The repository owner selected the already-ratified `add-chain-anchoring` packet
as the surviving tranche-three change and retired the stale competing
`add-signed-execution-chain-anchoring` draft. The surviving packet is stronger
on receipt integrity, timing, privacy, and witness failure, but the comparison
originally found three useful contract obligations that must not disappear
with the superseded draft: an operational-PKI realization gate, deterministic
fixed-UTC durability membership, and an explicit distinction between network
submission and independently verified confirmation. **The first of those three
— the operational-PKI realization gate — was dropped by the owner's ruling of
2026-09-04, after `add-chain-anchoring` realized without it; see "Requirement 1
removed" below.** The two that remain, fixed-UTC durability membership and the
submitted-versus-confirmed witness distinction, are re-presented in this PR on
their own merits.

## Requirement 1 removed — owner's ruling 2026-09-04

Brett Heap, repository owner, ruled on this PR (2026-09-04, in session, lane
openxfactory-1d): **"bring 548 forward after 629 lands, drop requirement 1."**
The fuller ruling, posted on PR #548, reasons through why: requirement 1
("Realization waits for the released chain and an operational PKI plane")
gated `chain-anchoring` schema and validator **authoring** on an operational
PKI plane that does not exist yet. PR #629 (squash `11feff75`, merged
2026-09-04) has already realized `chain-anchoring`'s twelve schemas and its
canonical validator against the ratified `add-chain-anchoring` basis — without
that gate, and without a shared Speckit feature linking the two packets — and
the owner separately ruled on #629 itself ("merge 629, register now"),
completing its manifest registration. Ratifying requirement 1 now, after that
realization has already landed, would retroactively declare the landed
realization illegitimate for authoring schema and validator text before an
operational PKI plane existed. Requirement 1 conflated two different gates
that the schemas themselves keep apart (contract **realization** — schema and
validator authorship — versus runtime **commissioning**, which does need a
named operational signed-log instance); only the latter plausibly needs a live
PKI plane, and #629's OPEN item 2 already tracks the still-unmet
`[OPERATOR]` conditions for that separately.

Requirement 1's full text is not deleted from the project's history — it
remains readable at this branch's pre-removal commit `adccf578` and earlier —
and is dropped from `specs/chain-anchoring/spec.md`'s `## ADDED Requirements`
block by the commit that lands this section. Requirements 2 (*Fixed UTC
durability batches account for every accepted event exactly once*) and 3
(*Witness submission and confirmation remain distinct evidence states*) are
unmodified by that removal — byte-identical to their pre-removal text — and
are re-presented below, on their own merits, for the owner's ratification.

## What Changes

- Add a fixed-UTC durability profile whose trusted log acceptance time and
  atomic admission transaction determine one immutable daily batch, including
  deterministic dedupe, late-arrival treatment, a closed non-recursive event
  denominator bound to a window-snapshotted eligibility-registry digest and
  uniquely selected effective interval, plus an atomic close watermark and
  resolving signed-log checkpoint that prove complete event inclusion. Empty-day
  continuity checkpoints link by the preceding daily item's anchored digest.
  One released, digest-bound Merkle construction profile makes every daily root
  independently reproducible.
  Event membership produces a daily batch root, canonical manifest bytes produce
  the material digest, and the complete mint-time configuration produces the
  anchored digest whose identity aggregation root enters both witnesses. This
  preserves the ratified configuration-bound multi-anchor receipt.
- Require witness state to distinguish submission from confirmation. Kaspa
  interface acceptance is not Kaspa confirmation; OpenTimestamps submission is
  not Bitcoin confirmation; long-horizon claims require the latter. Confirmation
  transitions are governed by an append-only registry of immutable versioned
  operator-approved profiles with activation checkpoints, content digests,
  current standing, anti-rollback refusals, and one per-witness snapshot for each
  UTC window, not implementation-selected thresholds.
- Preserve the surviving packet's existing receipt/state split, timing model,
  configured-witness binding, privacy boundary, and claim-not-factory failure
  semantics unchanged.
- Record the disposition of the superseded draft: its provider-neutral gateway
  enforcement text belongs to consumer/runtime governance and is not imported
  into the neutral anchoring capability; its remaining requirements are already
  covered or strengthened by `add-chain-anchoring`.

**(Requirement 1's realization-gate prerequisite and its shared-Speckit-feature
/ basis-archives-first linkage are dropped along with requirement 1 — see
"Requirement 1 removed" above. `add-chain-anchoring` has since realized, at PR
#629, without either mechanism.)**

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `chain-anchoring`: Add fixed-UTC complete durability batches, deterministic
  dedupe/lateness rules, and submitted-versus-confirmed witness semantics
  without changing the ratified witness configuration. (Realization readiness
  — requirement 1 — is no longer part of this amendment; see above.)

## Impact

- **openxFactory contracts:** `add-chain-anchoring`'s twelve schemas and
  canonical validator already realized at PR #629 (squash `11feff75`), ahead
  of and without this amendment. If ratified, requirements 2 and 3 owe a
  **follow-on realization pass** against those already-landed schemas before
  they ship in a contract bundle — see "Realization cost if ratified" below —
  rather than landing inside the basis packet's original realization as first
  drafted.
- **Runtime owners:** must provide the declared scheduling, persistence,
  retry, and network adapters that the durability and confirmation profiles
  require; those runtime surfaces remain outside this repository. (The
  operational-PKI evidence obligation was requirement 1's and is dropped with
  it.)
- **Consumers:** receive one stable capability id, `chain-anchoring`, and can
  pin exact release/version/digest evidence without relying on the superseded
  draft id.
- **MedxFactory:** its draft usage-control packet can reference the surviving
  capability while keeping executable conformance blocked until the amended
  contracts are released and consumer conformance passes.
- **Compatibility:** the basis, `add-chain-anchoring`, has already realized
  (PR #629) but is NOT yet released — no contract bundle has cut its schemas;
  `contract-v3.3` remains unspent. The additive first-release path survives
  only if requirements 2 and 3 ratify and their follow-on realization pass
  lands **before** the next `chain-anchoring` bundle cut; if a bundle ships
  those schemas first, compatibility and version class must be re-evaluated
  before this packet proceeds, because a released receipt is never silently
  reinterpreted.

## Realization cost if ratified

PR #629 already realized `chain-anchoring`'s twelve schemas and canonical
validator (`scripts/validate-chain-anchoring.py`) against the basis alone.
#629's own body says so directly, under "Relationship to #548": *"Measured,
not assumed: the family carries no confirmation-profile registry (zero
references anywhere under `contracts/chain-anchoring/` or in the reader), and
the anchor-state's per-witness enumeration is `in_flight | landed |
terminally_failed`... If #548 lands, this realization needs a follow-on
pass."*

Independently re-measured on this branch's merged head, over every landed
`chain-anchoring` schema and the reader:

```
grep -rniE "confirmation|profile" contracts/chain-anchoring/*.schema.yaml \
  scripts/validate-chain-anchoring.py
```

returns **zero matches**. (`\bsubmitted\b|\bconfirmed\b` alone returns three
incidental prose hits — none a state member, enum value, or field name — so
neither term names anything the schemas or reader currently recognize either.)
`contracts/chain-anchoring/anchor-state.schema.yaml`'s `witness_status_row`
carries the closed, three-member `status` enum `[in_flight, landed,
terminally_failed]`, which distinguishes in-flight from landed but is not
requirement 3's interface-submitted-versus-independently-verified-confirmed
distinction, and binds no confirmation-profile id, version, content digest,
activation checkpoint, or standing anywhere in the mint-time configuration
block.

If requirements 2 and 3 are ratified, landing them requires a **follow-on
realization pass** against these already-shipped schemas, before they ship in
a contract bundle at the next cut (so the pinned shape is the amended one, not
a since-superseded one):

- **Requirement 3** needs a new confirmation-profile registry contract (or an
  extension of an existing one), a widened or replaced `witness_status_row`
  `status` vocabulary that separates `submitted` from `confirmed` per network,
  and a confirmation-profile id/version/content-digest/activation-checkpoint
  binding added to the receipt's mint-time configuration block — a
  **breaking** change to the `status` enum's closed member set as currently
  shipped, not a purely additive one, since every existing `landed` value
  would need to be re-evaluated against the new submitted/confirmed split.
- **Requirement 2** needs the fixed-UTC durability batch, eligibility
  registry, and daily-Merkle construction-profile machinery added on top of
  the realized receipt/anchor-state pair — additive schema and validator work,
  but unstarted, since #629 realized none of it (its OPEN items 2-5 name only
  the pre-existing basis's own unclosed operator conditions, not this
  amendment's durability profile).

Whichever way the owner rules on requirements 2 and 3, this follow-on pass is
a **new, separate realization PR**, sequenced after this proposal's
ratification and before the next `chain-anchoring` contract bundle cut.
