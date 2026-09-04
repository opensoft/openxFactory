---
code_surface: openxFactory (`scripts/doc_health/proposal_origin.py` — the family gains two finding classes and one reader: the `ad_hoc` arm splits into three states (claims approval / claims drafting / claims neither), the two field pairs become named module constants, and `_declared_standing` reads ONE packet's own `Status:` through `corpus.parse_status` + `promotion_fidelity.declared_standing`, the single lifecycle-header reader and the single standing grammar, never a private regex. `scripts/proposal-support.py` — the gate arm of the same three-state rule in `origin_errors` so `verify` and the nightly agree, the two field pairs copied with a stated reason and an agreement test, `write_origin_block` writing whichever pair(s) the origin carries and refusing one that completes neither, and `declare-adhoc` gaining `--proposed-by`/`--proposed-on` with the approval pair no longer argparse-required. `tests/doc-health/test_proposal_origin.py` — the new matrix in both directions. `tests/doc-health/test_lifecycle_scan_set.py` — ONE comment on an existing `NON_READERS` entry, no assertion and no behaviour. `tests/doc-health/test_modified_block_currency_self_gate.py` — `_LEDGER_SUBJECTS` gains this packet's own two MODIFIED blocks, the EXACT named set that self-gate compares with `==`; it failed first, by name, naming both, which is the assertion working, and the two rows carry the per-unit explanation and the retirement condition that set's own convention requires. `docs/document-lifecycle.md` — § Gates In Practice's origin paragraph. NO new family, no registration, no count ripple, no threshold, no severity flip, no change to the report schema, the regression-diff rule, the governed corpus, the lifecycle scan set, or any other family's behaviour.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, no release tag is owed. The archive gate is therefore merge-plus-green on `main`, following `add-release-tag-publication-check` and `add-duplicate-packet-check` exactly: `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose severity counts move by exactly what § Measured effect predicts and in no other line. The change therefore ships ACTIVE and archives only after the merge — a code-surface packet does not archive on landing.
Status: ratified
Proposed: 2026-09-03
Ratified: 2026-09-03 by Brett Heap (repository owner) — in session, verbatim: "implement your recommendations on all these", given over the lane's written recommendations for issues #561/#339, #318, #511, #553 and the #543 fix (b), and recorded for this issue as the RULING comment on openxFactory issue #318. That comment states the resolution this packet implements: shape 1, an origin state that declares provenance without asserting approval, so an unapproved packet is expressible and lawful, with `approved_on` appearing when the approval does and a `Status: ratified` proposal still requiring it. The ruling settles the SHAPE and authorizes the VEHICLE; it does not cover the six design decisions in § Orchestrator Decisions, which are flagged there for veto. Record: `review/ratification-2026-09-03.md`.
Origin: openxFactory issue #318 — "A drafted-but-unapproved change packet has no lawful origin shape — every draft is a proposal-origin error until it is approved", surfaced by the `add-release-inventory-drift-check` drafting (issue #312) and deliberately left alone there, because "inventing an approval date to make a check pass is the exact move that change's own policy correction now forbids in writing."
---

# Proposal: add-drafted-proposal-origin

## Why

**A DRAFTED PACKET COULD NOT BE HONEST.** The promoted origin contract offers
exactly two shapes and both accuse a drafted-but-unapproved change:

| `.openspec.yaml` shape | doc-health verdict |
|---|---|
| `origin.kind: ad_hoc`, no `approved_on` | `error` — "ad-hoc origin lacks required `approved_on`" |
| no `origin:` block at all | `error` — "proposal carries no origin declaration" |

There is no third option, and `approved_on` records a date that, for an
unapproved draft, does not exist. So the mechanical remedies were: approve the
change, delete the draft, or write the date anyway. **The third is the defect
the field exists to catch**, and issue #318 says so in the sentence that
routed the fix out of #312 rather than into it.

**THE STATE HAD A POPULATION, AND IT WAS IN THE BASELINE.** Three packets on
`main` sat in it — `create-medxchart-overlay-boundary`,
`create-medxpractice-overlay-boundary`, and
`add-release-inventory-drift-check` while it awaited rulings — the first two
long enough to become part of the standing error baseline that every session's
zero-new gate is measured against. A permanent known-red finding nobody can
clear without approving or deleting is the erosion the drift check in #312 was
wanted to prevent in the first place.

**THE WORKFLOW PRODUCES THIS STATE DELIBERATELY.** A "scout and draft, do not
implement" assignment — which is how #312 was scoped — is SUPPOSED to yield a
packet that exists, validates, and is not yet approved. A rule that cannot
tell that lawful intermediate state from a governance defect is not measuring
governance; it is measuring how recently somebody was available to rule.

**And the medx packets show what the missing shape cost even after they were
cleared.** Both were admitted by ruling on 2026-08-25, so both now carry
`approved_by`/`approved_on` — and both spend a paragraph of `approved_by`
prose insisting the approval is an admission and NOT a ratification of
content, in capitals, because the only field available to record "somebody
said this packet may exist" is the field named for approval. The vocabulary
was doing two jobs and had one word for them.

## What Changes

- **`document-lifecycle` gains the state.** ONE MODIFIED requirement
  ("Proposal origin declaration"): an `ad_hoc` origin carries a required
  `reason` and EITHER approval provenance (`approved_by` + `approved_on`) OR
  drafting provenance (`proposed_by` + `proposed_on`) — one pair in full,
  never neither and never half of one. The requirement had to admit the state
  before a checker could accept it: the family enforces the origin contract
  BY REFERENCE, so a family accepting a shape its owning requirement forbids
  would be holding a second, private definition of the contract, which is the
  exact drift the "by reference" clause exists to prevent. Three properties
  are stated with it: the origin's IDENTITY (`kind`, `id`, `path`) is what is
  immutable, so **approval is an ADDITION and never a rewrite**; approval
  SHALL appear when a status claims it; and the state MUST NOT be entered to
  quiet a check on a proposal claiming ratification.
- **`doc-health` gains the two findings.** ONE MODIFIED requirement
  ("Proposal-origin checks enforced by reference"): the family's finding
  classes go from five to seven, named in the requirement,
  `drafting-provenance-incomplete` and `unapproved-origin-at-ratification`
  added, with the second at `error` and resolution class `contested`. Five
  existing scenarios carried byte-identically, five added.
- **The implementation lands in this change**, on the
  `add-release-tag-publication-check` precedent: the family, the gate arm
  that keeps `verify` and the nightly from disagreeing, the sanctioned
  writer's new arm, and 18 new tests over the matrix in both directions.

## Impact

- **Affected specs**: `document-lifecycle` (MODIFIED), `doc-health`
  (MODIFIED).
- **Affected code**: `scripts/doc_health/proposal_origin.py`,
  `scripts/proposal-support.py`, `tests/doc-health/` (the family's own suite,
  one `NON_READERS` comment, and the `modified-block-currency` self-gate's
  named subject set), `docs/document-lifecycle.md`.
- **Measured effect on this repository's own health run**: `proposal-origin`
  reads **0 findings before and 0 after**; the headline moves by **+2 `info`
  and nothing else**, both of them this packet's own two MODIFIED blocks
  appearing in `modified-block-currency`'s carriage ledger — the editorial
  arm that "CANNOT distinguish a deliberate rewording from stale text and
  does not claim to", which every active reworded MODIFIED block in this
  corpus currently produces one of (8 in the baseline, all from other active
  changes). **Zero new `critical`, `error` or `warning` findings.**
- **THE NEW FINDINGS HAVE AN EMPTY POPULATION BY CONSTRUCTION, and it is
  measured rather than assumed.** Both key on `proposed_by`/`proposed_on`,
  fields that exist in **no packet in this repository**: all **109** ad-hoc
  origins across the active and archived corpus carry a complete approval
  pair, **0** carry neither, **0** carry half of one. Nothing this change
  adds can fire on anything that exists today, in any repository, and nothing
  it changes can fire on more than it did — the one behavioural change to an
  existing class (D4) reports strictly FEWER findings on the same input.
- **Nothing already lawful changes shape.** `approved_on` is still required
  for an ad-hoc approval, in full, wherever approval is claimed. The two medx
  packets, and every other approved ad-hoc origin, are byte-untouched and
  keep their verdicts.

## Orchestrator Decisions — FLAGGED FOR VETO

The ruling settles shape 1 and authorizes the vehicle. It does not cover the
six decisions below; `design.md` argues each at length and each is reversible
on a word.

**D1 — The encoding: `ad_hoc` + `proposed_by`/`proposed_on`, NOT a third
`kind: drafted`.** The ruling offered both spellings. Only one of them can
express approval as an ADDITION: a `drafted` kind must become `ad_hoc` when
the approval lands, and `kind` is one of the fields the support manifest
REPEATS, so the transition writes a manifest/packet disagreement that this
same family reports as post-ratification mutation at `error` with resolution
class `contested`. Keeping the `:adhoc:` id under a `drafted` kind only moves
the mutation from `id` to `kind`; both are manifest-repeated. Under the
chosen encoding the identity never moves — same `kind`, same durable id,
minted once at drafting — and approval is two added lines. A design that must
mutate an identity the contract calls immutable in order to record an approval
has put the defect in the happy path.

**D2 — The status rule keys on the packet's own declared `Status:`, and fires
only where the unapproved state is POSITIVELY declared.** Not on archival: an
archived packet may lawfully declare a pre-ratification standing — the C5
exemption `promotion-fidelity` and `duplicate-packet` both read through
`declares_pre_ratification` — so reading "it archived" as "it was approved"
would invent an approval the record does not carry, in the family whose whole
subject is not inventing approvals. And silence is not the drafted state: an
origin that merely omits its approval has declared no provenance state and is
reported as such, so a packet cannot buy the lenient treatment by leaving
fields out.

**D3 — `unapproved-origin-at-ratification` is `contested`;
`drafting-provenance-incomplete` is mechanical.** Resolving the first either
transcribes an approval act that happened or withdraws a status claim that
should not have been made — both governance acts, and the third option
(writing a date nobody gave) is the defect. A mechanical class invites the
third. The second is a half-written pair completed from the record of who
drafted it, which is exactly the mechanical-visibility band its sibling
`adhoc-provenance-incomplete` already sits in.

**D4 — An origin declaring NEITHER state produces ONE finding, not one per
absent field.** It has not half-claimed anything; it has claimed nothing, and
the remedy is a single choice between two shapes. Measured before changing it:
109 ad-hoc origins here, ZERO in that state, so the corpus movement is nil.
Everywhere else the direction is strictly fewer findings on identical input,
never more.

**D5 — The gate accepts the state; the ratified-status rule stays in the
family.** The first half is not optional: a state the nightly calls lawful
while `proposal-support.py verify` rejects it is not a lawful state, it is a
state with two answers. The second half is a boundary: `origin_errors` runs at
creation and at transition, when a packet's status claim is `draft` by
construction, and the violation D2 names can only arise later — which is when
the nightly measures. The gate also has no business reading a sibling document
to judge an origin record.

**D6 — `declare-adhoc` gains `--proposed-by`/`--proposed-on`, and
`write_origin_block` writes whichever pair(s) it is given.** A lawful shape
the repository's own sanctioned writer cannot emit is a shape only hand-authorable,
and the writer would then disagree with the gate that accepts it. The approval
that arrives LATER is still a hand amendment — `write_origin_block` refuses to
overwrite an existing declaration, which is the immutability guard, and
transcribing an authority's words is not a thing to automate — and that
residue is disclosed in `tasks.md` § 4 rather than quietly left.

## What this proposal does NOT claim

It does not claim any packet needs the new state today: both medx packets were
approved on 2026-08-25 and are untouched, so this change lands with an empty
population and **repairs no baseline finding** — the baseline it removes is
the one the NEXT drafted packet would have added. It does not weaken
`approved_on`, which is still required in full wherever approval is claimed.
It does not decide that a drafted packet may ratify without approval — the
second finding class exists precisely to make that unstateable. It does not
adopt the issue's shape 2 (an origin not required while `proposal.md` says
`draft`), which the ruling did not choose and which `design.md` argues against
on its own terms: it makes the presence of a required field depend on a value
in a different file, and it leaves "unapproved" undetectable rather than
expressible. And it does not touch `docs/doc-health.md`'s check-family table,
whose family rows this change adds none to.
