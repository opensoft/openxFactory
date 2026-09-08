# Proposal Ratification: adopt-configured-notebook-hosting-identity

Status: record

Decision date: 2026-09-08

Ratifier: Brett Heap (convener) — in session, lane
`provenance-autonomous-merge`, through the interactive multi-choice
walkthrough, **2026-09-08, ~12:20Z–12:35Z UTC**. Unlike the exemplar
`adopt-codexfactory-repository-identity` (ratified via a PR comment), this
word was given first-hand to the orchestrating session rather than posted to
openxFactory PR [#783](https://github.com/opensoft/openxFactory/pull/783);
this record is the primary evidence of it, and the PR comment posted after
this record lands is a cross-reference to it, not the other way around.

## Decision

Brett Heap ruled the packet's five open questions and then ratified the
packet, verbatim, in the order asked:

> OQ-A (where the LIVE declaration lives): "hermes-install
> config/clients/opensoft/"
>
> OQ-B (archived `add-notebook-projection-identity` delta cross-reference
> note): "No note"
>
> OQ-C (committed synthetic instance path): "Keep the path, mark
> hosting.instance: example"
>
> OQ-D (actor names in the synthetic example): "Yes, placeholders for actors
> too"
>
> OQ-E (roster record of seven grants + one denial): "Moves intact with the
> declaration"
>
> Ratification: "Ratify 783 and merge"

**Ratified baseline: this change as committed at the head this word was given
against — `fd7a74fe3f9d6257bbdeb5b950c040d50a8038fb`** (`proposal.md`,
`design.md`, `tasks.md`, `.openspec.yaml`, and the
`## MODIFIED Requirements` delta at
`specs/lifecycle-notebook-projection/spec.md`, exactly as authored). This
branch was subsequently merged forward with `origin/main` to clear a routine
divergence (no conflicts; the merge commit is
`da5beed7eb0e10d03403ab51961d4f4be4515e45`), so the content Brett ratified is
identical to the content landing under this record — the merge carries none of
this packet's own files — and the head this record's own commit lands on is
the newer one.

## What is ratified

- **The proposal as written**, `code_surface` / `target_release` /
  `sequenced_after` front-matter included: the single `## MODIFIED
  Requirements` delta on `lifecycle-notebook-projection`, the configured-path
  resolver shape (Group 2), the public instance becoming synthetic (Group 3),
  the test-fixture rewrite (Group 4), the operator move of the live record
  (Group 5, not performed by this ratification), and the documents/records
  group (Group 6).
- **All five open questions**, ruled exactly as recommended in the proposal's
  own `## Open questions` section — see the ledger below.
- **`tasks.md`'s nine groups**, as authored, with no realization box ticked by
  this ratification beyond task 0.2, the ratification-recording task itself.

## The rulings ledger

| OQ | status | ruling |
| --- | --- | --- |
| OQ-A | **RULED** | The live declaration lives in `installs/hermes-install`, at `config/clients/opensoft/notebook-projection-hosting.yaml` — the proposal's recommended option, adopted as given. |
| OQ-B | **RULED** | No cross-reference note is added to the archived `add-notebook-projection-identity` delta. |
| OQ-C | **RULED** | The committed instance keeps its path, `examples/notebook-projection-hosting.yaml`, and is marked synthetic inside the record (`hosting.instance: example`) rather than renamed. |
| OQ-D | **RULED** | The actor names in the synthetic instance go to role placeholders too. |
| OQ-E | **RULED** | The roster record (seven grants and one recorded denial) moves intact with the declaration to its new configured home; the public tree keeps a pointer, not a synthesized replacement. |

All five open questions this packet named are now ruled; none remains open.
Realization proceeds as a Speckit feature, sequenced after the org-move
realization (`~/session-prompts/runbook-codexfactory-org-transfer.md` step
10.2 — realizing `adopt-codexfactory-repository-identity`) is itself
sequenced, consistent with `tasks.md` 0.3's premise check and the packet's
own `sequenced_after: [add-notebook-projection-identity]` declaration.

## What this ratification does NOT do

- **No realization.** No row is added to
  `config/clients/opensoft/notebook-projection-hosting.yaml` in
  `installs/hermes-install`, the promoted spec is not yet amended by the
  archive act, the committed example is not yet rewritten, no test fixture
  changes, no resolver is written, and no box in `tasks.md` Groups 1-9 is
  ticked by this ratification — the one exception is task 0.2, the
  ratification-recording task itself, ticked because this record is the diff
  that discharges it, under the same house practice
  `adopt-codexfactory-repository-identity` task 0.3 and
  `disposition-codexfactory-declared-renames` task 5.4 used for their own
  ratification-recording boxes.
- **No merge.** Brett's word included "and merge", but per Rule 6 (a
  `openspec/changes/` pull request) the landing lane posts LANDING/LANDED at
  merge time and this lane's brief is explicit that it does not merge.
  This record is written and pushed on the branch, before any merge; the PR
  is updated to say it is ratified and awaiting Rule 6 landing, and merging
  it is a separate, later act.
- **OQ-A's realization is still an operator act.** The ruling names the
  home; it does not itself write
  `config/clients/opensoft/notebook-projection-hosting.yaml`, move the live
  eighteen lines there, or update the resolver — `tasks.md` Group 5 remains
  the operator's, on Brett's own word, at realization.

## Records

- This packet's pull request: openxFactory
  [#783](https://github.com/opensoft/openxFactory/pull/783), branch
  `change/adopt-configured-notebook-hosting-identity`.
- Ratified head: `fd7a74fe3f9d6257bbdeb5b950c040d50a8038fb`. Landing head
  (after the forward merge with `origin/main`):
  `da5beed7eb0e10d03403ab51961d4f4be4515e45`.
- Context this ruling realizes: Q2 of
  `~/session-prompts/redaction-outside-ideation-decision-2026-09-07.md`,
  ruled by Brett Heap 2026-09-08T03:36Z, option [A] ("one small governed
  change (proposal -> your ratification -> Speckit realization)").
- Sibling packets of the same decision sheet: the docs pull request covering
  Q1 and Q3 — openxFactory #786 — merged 2026-09-08T12:28Z, landing at
  `e8021fed`; the ideation-removal pull request — openxFactory #785 — merged,
  landing at `97f14f76`. Both are ancestors of this record's landing head via
  the forward merge above.
- The governed half of the forcing fact: `adopt-codexfactory-repository-identity`
  (ratified 2026-09-07, on main at `eb30db7a`), whose own realization is
  runbook step 10.2 in
  `~/session-prompts/runbook-codexfactory-org-transfer.md`.

Lane: provenance-autonomous-merge
