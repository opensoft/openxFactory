# Design: add-drafted-proposal-origin

Status: ratified
Ratified by: add-drafted-proposal-origin

The ruling settles the SHAPE — "an origin state that declares provenance
without asserting approval" — and names two spellings without choosing
between them: "a `drafted` kind, or `proposed_on` without `approved_on`".
This document chooses, and argues the choice against the two costs issue #318
states and against the alternative the issue itself offered.

## The two costs the change must remove

Issue #318 names them exactly:

1. "a real error in the baseline that nobody can clear without either
   approving the change or deleting the draft";
2. "the erosion that follows from a permanent known-red finding — the reason
   a drift check was wanted in #312 in the first place."

Both encodings remove both. Neither cost discriminates between them, so the
decision has to be made on what each encoding does to the REST of the origin
contract — which is where they differ sharply.

## D1 — Why `ad_hoc` + `proposed_by`/`proposed_on`, and not `kind: drafted`

**The contract calls the origin immutable, and one of the two encodings
cannot honour that while recording an approval.**

The origin's durable identity is not a private field. `document-lifecycle`'s
"Proposal-owned supporting documents" requires that the support manifest
REPEAT `origin.kind` and `origin.id` — and, for staged origins,
`origin.path` — and that "those values MUST match the change's
`.openspec.yaml`". The `proposal-origin` family enforces exactly that
(`origin-mismatch`), and for an archived change it reports a disagreement as
post-ratification mutation: `error`, resolution class `contested`, because
resolving it reverses a gate decision.

Now run each encoding through the moment the approval arrives.

**`kind: drafted` → `kind: ad_hoc`.** The state is spelled in `kind`, so
approval must rewrite `kind`. `kind` is manifest-repeated. A packet whose
manifest was written at transition therefore acquires a manifest/packet
disagreement on the day it is approved, reported by this very family at
`error`/`contested`. The obvious dodge — keep the `:adhoc:` id under
`kind: drafted` so only the kind moves — does not help: it is the kind that
moves, and the kind is repeated. The other dodge — mint a `:drafted:` id and
re-spell it at approval — moves the mutation onto `id`, which is repeated
too, and additionally makes a "durable id" one that changes state. Either
way the design puts a contested-class mutation on the happy path of every
packet that gets approved.

**`ad_hoc` + `proposed_by`/`proposed_on`.** The identity is `kind: ad_hoc`
and a durable `:adhoc:` id minted once, at drafting, and never touched again.
Approval is two ADDED lines in a block whose identity fields did not move, so
no manifest anywhere comes to disagree with any packet. Nothing already
lawful changes shape, structurally rather than by test: the approval arm of
the checker is untouched, and an origin that claims approval owes the whole
pair exactly as it did before.

Three smaller arguments point the same way.

- **`kind` answers a different question.** `staged` versus `ad_hoc` is
  *where the change came from* — an organized staging topic, or a deliberate
  exception. Approved-versus-unapproved is *whether anyone has said yes yet*.
  They are orthogonal, and folding a second axis into `kind` is what makes
  the enumeration grow one member per combination the day a staged origin
  ever needs the distinction.
- **The grammar stays closed.** No third id form, no third branch in the
  `id`/`kind` agreement check, no new regex. The existing
  `<repo>:adhoc:<date>-<slug>` grammar already fits, and the date it carries
  is the DECLARATION date — measured, not assumed: `create-medxchart-overlay-boundary`
  carries `:adhoc:2026-08-23-…` and was approved on 2026-08-25.
- **The record reads honestly at every stage.** "proposed by X on D" then
  "approved by Y on E" is the sentence the packet's history actually makes.

**What the chosen encoding costs, stated rather than hidden.** `kind: ad_hoc`
no longer implies approval on its own — a reader must look at the fields.
That is a real loss of at-a-glance legibility, and it is bounded: the fields
were always the load-bearing part (`reason` and the approver were required
before this change too), and both the family and the gate now name the state
in the finding text so a reader is never left to infer it.

## D2 — Where the ratified-status rule keys

The rule the ruling requires — "a `Status: ratified` proposal still requires
it" — needs an input, and there are three candidates: the packet's declared
`Status:`, the fact of archival, and a citation somewhere else.

**The declared `Status:`, read once, through the shared reader.** The family
now calls `corpus.parse_status` and `promotion_fidelity.declared_standing`
— the single lifecycle-header reader (`align-status-reader-to-real-lines`'s
real-line rule) and the single standing grammar (which strips annotations and
punctuation, so `Status: ratified (superseded by X)` declares `ratified`).
A second reading of one header is how two families come to disagree about
what one packet claims; that lesson is already written down in
`promotion_fidelity`'s own module and this family follows it rather than
re-deriving it. The set it compares against is
`promotion_fidelity.RATIFIED_OR_BEYOND`, which already exists and already
means exactly "declared a standing at or beyond ratification" — so
`standard`, `superseded` and `retired` are covered without this family
inventing a second opinion about what is beyond what.

**NOT archival.** An archived packet may lawfully declare a
pre-ratification standing — the C5 exemption, read by both
`promotion-fidelity` and `duplicate-packet` through
`declares_pre_ratification`, exists because "a packet that never claimed
ratification discharged no ruling". Treating the archive act as an approval
would invent an approval the record does not carry, inside the family whose
whole subject is not inventing approvals.

**And the state is DECLARED, never inferred.** The class fires only where
the packet positively carries drafting provenance. An origin that merely
omits its approval has declared no provenance state at all and is reported
as such (D4). This is what stops the new state from becoming a loophole:
you cannot reach the lenient treatment by deleting fields, only by adding
them.

## D3 — The resolution classes

`unapproved-origin-at-ratification` is `error` with resolution class
`contested`. The class is argued, not inherited: the finding has exactly two
lawful remedies — transcribe an approval act that happened, or withdraw a
status claim that should not have been made — and both are governance acts,
one of which reverses a gate decision. The third move, writing a date nobody
gave, is the defect the whole change exists to prevent, and a mechanical
class is an invitation to it. `contested` also brings the corpus's
uncited-resolution discipline: a contested finding that DISAPPEARS via a
status change with no citation is itself reported.

`drafting-provenance-incomplete` is a plain `error` in the mechanical band,
beside its sibling `adhoc-provenance-incomplete`: a half-written pair is
completed from the record of who drafted it, and completing it decides
nothing.

## D4 — One finding for an origin that declares no provenance state

Before this change, an ad-hoc origin carrying only `reason` produced TWO
findings, one per absent approval field. That was right when the approval
pair was the only lawful destination. It is wrong now: such an origin has
not half-written a claim, it has made none, and the remedy is a single choice
between two shapes — which is what the one finding names.

Measured before changing it: **109 ad-hoc origins** in this repository's
active and archived corpus, **0** in that state and **0** carrying half a
pair. The corpus movement is nil here, and everywhere else the direction is
strictly FEWER findings on identical input — this restructure cannot add a
finding to any repository.

## D5 — What the gate takes and what it leaves

`proposal-support.py`'s `origin_errors` gains the same three-state arm. This
is not optional: a state the nightly family calls lawful while
`proposal-support.py verify` rejects it is not a lawful state, it is a state
with two answers, and the packet in it would still be unable to pass its own
gate.

The gate does NOT take the ratified-status rule. `origin_errors` is called
at creation and at transition, when a packet's status claim is `draft` by
construction; the violation can only arise later, which is when the nightly
measures. And a per-change origin gate reading a sibling document to judge an
origin record widens its input for a case it cannot see.

**The duplication is deliberate and held by a test.** The two field pairs
are copied into `proposal-support.py` rather than imported, on the criterion
that file already states for its other copies: `doc_health.pin_sentinels`
earned an import by depending on nothing outside the standard library, and
`doc_health.proposal_origin` depends on PyYAML and two further package
modules, exactly as the id grammars above it are copied. A copied rule is
held by a test or by nothing — hence
`test_the_gate_and_the_family_name_the_same_provenance_fields`.

## D6 — The writer

`write_origin_block` now emits whichever pair(s) the origin dict carries and
raises `SupportError` when neither is complete; `declare-adhoc` gains
`--proposed-by`/`--proposed-on` and the approval pair is no longer
argparse-required (exactly one complete pair is). A lawful shape the
repository's own sanctioned writer cannot emit is hand-authorable only, and
the writer would then disagree with the gate that accepts it.

The approval that arrives LATER is still a hand amendment. `write_origin_block`
refuses to overwrite an existing declaration — that refusal IS the
immutability guard — and transcribing an authority's words into a `reason`
block is not a thing to automate. Recorded as a live limitation in
`tasks.md` § 4 rather than left for a reader to discover.

## Why not the issue's shape 2 (a draft window)

The issue's second candidate: `origin` is not required while `proposal.md`
carries `Status: draft`, becoming required at ratification. The ruling did
not choose it, and it is worth recording why it is the weaker shape on its
own terms rather than only by authority:

- It makes the presence of a REQUIRED FIELD in one file depend on a value in
  a DIFFERENT file, so the gate that validates a packet's `.openspec.yaml`
  cannot answer from the packet's own record.
- It leaves "unapproved" UNDETECTABLE rather than expressible, which is the
  sentence the issue ends on. A draft with no origin block and a draft whose
  origin was forgotten look identical, and the second is a real defect.
- It would delete provenance rather than record it: the drafting session's
  identity and date — the only trace of who drafted a packet and when —
  would have nowhere to live until an approval arrived to carry them.

## What this design does not settle

It does not give a staged origin a drafting state: a staged origin's
provenance is its topic and its transition record, it has never carried an
approval pair, and nothing in this change asks it to start. It does not
automate the approval amendment (D6). And it does not migrate anything: the
new state has an empty population by construction, and no packet on `main`
is moved into it by this change.
