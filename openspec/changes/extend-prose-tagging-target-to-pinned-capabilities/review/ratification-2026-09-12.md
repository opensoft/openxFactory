# Proposal Ratification: extend-prose-tagging-target-to-pinned-capabilities

Status: ratified
Kind: report
Decision date: 2026-09-12 (acts 1-4) and 2026-09-13 (act 5, the re-ruling on 1.2)
Ratifier: Brett Heap (openxFactory repository owner)
Ratified: 2026-09-12 and 2026-09-13 by Brett Heap (openxFactory repository
owner) — FIVE SELECTIONS, not typed sentences, made via the lane's
interactive multi-choice, first-hand, in session, lane `openxfactory-2`
(display `openXfactory-2`). FOUR on 2026-09-12 at approximately 23:20Z, one
question per `tasks.md` § 1 task: "Ratify 1.1 as filed (Recommended) /
Ratify 1.2 as filed / Ratify 1.3 as filed (Recommended) / Confirm 1.4 as
filed (Recommended)". A FIFTH on 2026-09-13T01:25:07Z, RE-RULING task 1.2
over Copilot review thread `PRRT_kwDOTAvnrs6h1H-H` on ratification pull
request #1019: "Tighten to fail-closed after all", which supersedes the
23:20Z selection on that one box and on no other. Recorded, and THE ONE
CITATION for this record, superseding and restating the 23:20Z record:
openxFactory #992, comment
https://github.com/opensoft/openxFactory/issues/992#issuecomment-5649935136
(copy for the lane's status thread: openxFactory #745, comment
https://github.com/opensoft/openxFactory/issues/745#issuecomment-5649935244).

## Decision

**RATIFIED — 1.1, 1.3 and 1.4 AS FILED; 1.2 WITH TIGHTENING (D-2 FAILS
CLOSED)**, by Brett Heap.

## The word, and exactly what it ratifies

Brett Heap's instruction was FIVE SELECTIONS across TWO SITTINGS.

**ACTS 1-4 — 2026-09-12 at approximately 23:20Z**, one question per
`tasks.md` § 1 task:

> **"Ratify 1.1 as filed (Recommended) / Ratify 1.2 as filed / Ratify 1.3 as filed (Recommended) / Confirm 1.4 as filed (Recommended)"**

— first-hand, in session, lane `openxfactory-2` (display `openXfactory-2`).
On 1.4 the option "Confirm, and give the realization word now" was offered
and NOT taken, so no realization word exists.

**ACT 5 — 2026-09-13T01:25:07Z (±3 min), a RE-RULING ON TASK 1.2 ALONE.**
Its trigger was Copilot review thread `PRRT_kwDOTAvnrs6h1H-H` on ratification
pull request [#1019](https://github.com/opensoft/openxFactory/pull/1019),
filed against `review/ratification-2026-09-12.md:80` — that ratifying D-2 as
filed leaves the capability segment open (`pinned:openxwallet/typo` resolves
until a pin record enumerates capabilities), and that "merely recording this
as a live constitutional question does not create an exception or amend the
constitution", constitution § Governance requiring "an explicit Complexity
Tracking justification or a constitution amendment". Put back to Brett Heap,
he selected:

> **"Tighten to fail-closed after all"**

whose description read, VERBATIM: *"Reopens 1.2: D-2 refuses a pinned target
whose record carries no capabilities enumeration; the four markers stay
unresolvable until openXwallet's pin publishes one. Reverts your 23:20Z
selection; a fix round re-encodes and the record changes."* NOT taken:
"Record my as-filed ruling as the explicit justification (Recommended)",
"Same, PLUS name a Principle VII clarification as an owed successor", "Hold
#1019 — I will read the thread myself".

**NO VETO, AND ONE AMENDMENT — act 5 itself.** Act 5 supersedes act 2 on task
1.2 and on nothing else; 1.1, 1.3 and 1.4 stand exactly as ruled at 23:20Z.
Neither word carries a condition on any later act, and neither reopens any
other decision.

**THE HEAD THE WORD WAS GIVEN OVER, AND WHAT MOVED SINCE.** The commit
`dafe8877e4c8f2d3a52cbe94307904b639b7bece` (2026-09-12T23:16:13Z),
openxFactory pull request
[#994](https://github.com/opensoft/openxFactory/pull/994) — this
packet's text at the head acts 1-4 were given over, with every fix round
encoded. No text this packet carries at that head is excepted from the
ratification: `proposal.md`'s account of the four `tag-hygiene` findings and
why no edit clears them honestly, `design.md`'s decisions, the two `## MODIFIED`
spec deltas against `document-lifecycle` and `doc-health`, and every scenario
and task the packet states. **Act 5 then TIGHTENED D-2 at that same head**, and
pull request #1019 re-encodes D-2, both spec deltas, task 1.2's RULED
annotation, § 3's test cases, `proposal.md`, the README bullet, the
`.openspec.yaml` approval text and this record on that word. What is ratified
is therefore the `dafe8877` text for D-1, D-1.1, D-3 and D-5, and the
FAIL-CLOSED D-2 this pull request encodes.

## What is ratified

The proposal as written at `dafe8877e4c8f2d3a52cbe94307904b639b7bece`, and the decisions `design.md`
carries:

- **D-1 — the FORM.** An `xspec:candidate` marker's `target=` may be
  `pinned:<pin-id>/<capability>`, where `<pin-id>` is the stem of a
  `contracts/<pin-id>-pin.yaml` record, the value is EXACTLY TWO
  `[a-z0-9]+(-[a-z0-9]+)*` components separated by EXACTLY ONE `/`, and a value
  that fails that grammar is refused BEFORE any path is built or any file is
  read. D-1.1: the `xspec:supersedes` marker's `spec=` attribute is OUT OF
  SCOPE and CLOSED — a `spec=` value carrying the reserved `pinned:` prefix is
  refused.
- **D-2 — the RESOLUTION RULE, AS TIGHTENED BY ACT 5: IT FAILS CLOSED.** A
  `pinned:<pin-id>/<capability>` target resolves only where ALL THREE
  prerequisites hold. **(a) UNCHANGED FROM THE FILING:** the pin id must
  resolve to a
  neutral-product pin record this repository carries, of
  `kind: pinned_contract_manifest` (`kind: pinned_workflow` is EXCLUDED —
  five of the six pin records qualify today), COMPLETE for its RECORD SHAPE
  against that shape's SHAPE-GUARD-REQUIRED SET — the top-level members its
  in-tree verifier refuses-when-absent in its pure, source-free guards,
  pinned to those guards by a two-leg equivalence test and NECESSARY, by
  design, without being SUFFICIENT for the record's full verifier — rather
  than a member list this grammar writes down, judged through a CODE-FIXED
  route (one shared, pure, non-executing adapter) that never executes,
  imports or opens a path a pin record selects — `verify_pin:` is
  data that route may compare, never a resolution prerequisite — and
  resolved under the same root precedence the in-tree arm already uses,
  whose `contracts` directory must itself be a real, non-redirecting
  directory before any candidate path is read. **(b) THE TIGHTENING:** that
  record must ALSO carry a well-formed, non-empty top-level `capabilities:`
  enumeration, and **(c)** `<capability>` must be a MEMBER of it. An ABSENT
  enumeration is an UNRESOLVED PINNED TARGET — a controlled finding naming
  the record path and the remedy, "the publisher adds `capabilities:`
  through a `neutral-product-pin` change" — exactly as a MALFORMED one
  already was. There is no dormant arm and nothing self-arms. `capabilities:`
  stays RESERVED by this change and is ADDED TO NO RECORD AND NO SCHEMA BY
  IT. **PRINCIPLE VII IS SATISFIED BY CONSTRUCTION**: the capability segment
  is checked against a closed registry — the pin record's own enumeration —
  and a deferred or absent enumeration fails closed rather than degrading
  open, so NO Complexity-Tracking justification and NO constitution amendment
  is owed by this packet. `design.md`'s D-2 keeps the constitutional
  objection in full, as the record of the tension, and closes it with this
  ruling.
- **D-3 — the STALE-TARGET RULE.** When a target capability exits the corpus
  the marker either takes the pinned form or the block is unfenced — never
  silently retargeted, never silently deleted.
- **D-5 — the REALIZATION SPLIT.** ONE later pull request carries the resolver
  arm, its tests, the four retargeted markers, the `docs/document-lifecycle.md`
  section and the stale `ideation/staging/INDEX.md` line together, rather than
  four separate ones.

**BOXES TICKED BY THIS RATIFICATION: 1.1, 1.2, 1.3, 1.4.** NO box in
`tasks.md` § 1 stays open — the word answers all four, and a box ticks on the
word that answers it and on nothing else. **ACT 5 MOVES NO BOX.** 1.2 was
answered at 23:20Z and is answered still; what changed is the ANSWER, so the
box stays `[x]` and its RULED annotation is rewritten to record both acts. The
tightening commits add ONE UNTICKED line to § 3 (3.8), which records a
prerequisite that belongs to openXwallet's publisher and is neither filed,
claimed, nor owed by this change.

## What this ratification does NOT do

- **NO REALIZATION.** No byte of `scripts/doc_health/families.py` moves, no
  module is added under `scripts/doc_health/`, and no byte of
  `scripts/validate-pin-registrations.py` or of any per-product pin
  verifier moves. No marker is retargeted or deleted.
  `docs/document-lifecycle.md` is not touched. `ideation/staging/INDEX.md`
  is not touched. No pin record gains a `capabilities:` member and no
  schema admits one. The four `error`-band `tag-hygiene` findings stand at
  FOUR, unchanged. Realization is a LATER pull request in this same
  repository, on a separate word.
- **NO CLOSURE OF THE FOUR FINDINGS, EVEN AT REALIZATION.** Under the
  fail-closed D-2, no pin record in this tree enumerates capabilities, so when
  the resolver and the four retargeted markers land together the four findings
  CHANGE FORM rather than close — from "unresolved target=openxwallet — name a
  capability under `openspec/specs/`" to "unresolved pinned target —
  `contracts/openxwallet-pin.yaml` carries no `capabilities:` enumeration;
  remedy: the publisher adds one through a `neutral-product-pin` change" —
  still FOUR and still `error`-band. They reach ZERO only on openXwallet's
  publisher's act, through `neutral-product-pin`, which is no part of this
  packet or of its realization.
- **NO ARCHIVE.** `code_surface` is non-empty (`scripts/doc_health/families.py`
  and its tests), so under `release-realization` this packet archives only on
  merged-plus-green realization evidence — not on this ratifying commit. Every
  box in `tasks.md` § 3 and § 4 stays unticked.
- **NO TICK OF ITEM (7) OF THE `split-openxwallet-repo` ARCHIVED-LEDGER ENTRY.**
  That owed successor discharges on ARCHIVE, not on ratification. The archived
  packet is not edited at all, under the archived-record rule.
- **NO MERGE.** This record ratifies text at one head. Landing the pull request
  that carries this ratifying commit is a SEPARATE act under this repository's
  Rule 6 landing-window protocol, because this change touches
  `openspec/changes/`.

## Records

- Governing issue, and the finding this packet answers: openxFactory
  [#992](https://github.com/opensoft/openxFactory/issues/992),
  § 4 "The ask" — the ratifying word's CONSOLIDATED record, which carries all
  five acts and is THE ONE CITATION for this ratification
  (https://github.com/opensoft/openxFactory/issues/992#issuecomment-5649935136).
  It supersedes and restates the 23:20Z record of acts 1-4, which stands in
  place as history.
- The lane's status thread: openxFactory [#745](https://github.com/opensoft/openxFactory/issues/745) — where the consolidated record was copied, verbatim
  (https://github.com/opensoft/openxFactory/issues/745#issuecomment-5649935244).
- The trigger of act 5: Copilot review thread `PRRT_kwDOTAvnrs6h1H-H` on
  openxFactory pull request
  [#1019](https://github.com/opensoft/openxFactory/pull/1019), filed against
  line 80 of this record as it then stood.
- The packet this ratifies: openxFactory pull request
  [#994](https://github.com/opensoft/openxFactory/pull/994), landed
  `dafe8877e4c8f2d3a52cbe94307904b639b7bece`, 2026-09-12T23:16:13Z.
- The cause: `openspec/changes/archive/2026-08-28-split-openxwallet-repo/` —
  its `tasks.md` measured the four findings, rejected both mechanical fixes and
  named this grammar extension as the honest one; its README archived-ledger
  entry carries the owed successor as numbered item (7), UNTICKED by this act.
