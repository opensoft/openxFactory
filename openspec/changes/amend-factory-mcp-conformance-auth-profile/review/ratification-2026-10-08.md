# Proposal Ratification: amend-factory-mcp-conformance-auth-profile

Status: ratified
Kind: report
Decision date: 2026-10-08
Ratifier: Brett Heap (openxFactory repository owner)
Ratified: 2026-10-08T20:2xZ by Brett Heap (openxFactory repository owner) - in session to lane `openXfactory-5`, verbatim *"Ratify, OQs as recommended (Recommended)"*, a multiple-choice answer; RULED on the estate's lane register at 2026-10-08T20:33:25Z. RATIFIED AS DRAFTED, with all six open questions of `design.md` adopted at the recommended answer, so no requirement or scenario text moved. It is a ratify word only: not a landing word, and it archives nothing.

## Decision

**RATIFIED AS DRAFTED.** The delta `specs/factory-mcp-conformance/spec.md` is
ratified exactly as it stood at the pull request's head when the ratifying seat
began, `843d7267`: blob `51fc770d`, the same blob in the ratifying commit. FOUR
`## ADDED` requirements (*Hosted declarations carry an authorization block*,
*RS256 token-signing baseline*, *Audience bound to the server's own resource*,
*Per-domain error vocabularies*) and ONE `## MODIFIED` requirement, *Lossless
results and explicit failures*, whose body and *Unavailable dependency*
scenario are narrowed to a dependency failure reported through the error
inventory. No requirement or scenario text moves in the ratifying commit, and
`git diff` of the delta across it is empty.

## 1. The word, and what it reaches

> Ratify, OQs as recommended (Recommended)

Brett Heap gave this word on 2026-10-08, in session to lane `openXfactory-5`,
as the answer to a multiple-choice question. Its option label is quoted
verbatim above, and the lane read it as: ratify this change as drafted, and
take all six open questions of `design.md`, OQ-1 to OQ-6, at the recommended
answer in the design's table. The lane recorded that reading as a RULED line
on the estate's lane register at 2026-10-08T20:33:25Z.

**The instant of the word is written to the precision it was taken at and no
finer.** The minute is `20:2xZ`, not a minute the record does not carry, which
is the house form this repository's earlier ratifications use for a word given
in session. The register line's own time, 20:33:25Z, is when the lane
recorded the word, not when he gave it.

The three rulings of the same day (*"RS256 baseline (Recommended)"*, *"Narrow
to error codes (Recommended)"* and *"Per domain, profile maps (Recommended)"*)
decided what the packet must say. They are quoted in `proposal.md` and are not
this word: this word is the ratification of the packet's exact text.

## 2. The six open questions, as ruled

Each is RULED as recommended. `design.md`'s open-questions table marks the
ruling beside each question. The right-hand column records, for the ratifying
read, where the recommended answer is already carried, so the word moves no
requirement text.

| OQ | Question | RULED | Where the recommended answer already stands |
| --- | --- | --- | --- |
| OQ-1 | Admit the `issuer_assigned` audience binding beside `resource_uri`? | **As recommended: yes.** | Requirement *Audience bound to the server's own resource* ("bound either to the service's canonical resource URI or to an identifier the issuer assigns to this resource alone") and its scenario *Issuer-assigned audience*; design D1 (`audience.binding` is `resource_uri` or `issuer_assigned`) and D3 |
| OQ-2 | Keep the admitted algorithms closed at RS256 (required) and EdDSA (optional)? | **As recommended: yes.** | Requirement *RS256 token-signing baseline* ("SHALL name RS256, MAY also name EdDSA, and SHALL name no other algorithm") and its scenarios *RS256 absent*, *EdDSA beside RS256* and *An algorithm the profile does not admit*; design D2 and D7 |
| OQ-3 | How is the metadata path derived for a resource URI with a path, and is a query refused? | **As recommended: RFC 9728 § 3.1 insertion, and the query is refused.** | Requirement *Hosted declarations carry an authorization block* (the metadata path "SHALL be the well-known location that RFC 9728 § 3.1 derives from the canonical resource URI"; for a deployed service the URI "SHALL carry no query component") and its scenarios *Metadata off the well-known path* and *Hosted resource URI with a query*; design D4 and D7 |
| OQ-4 | Must the block cite evidence or a gap under a new `auth` concern? | **As recommended: yes.** | The same requirement ("SHALL cite evidence or an explicit gap for its claims") and its scenario *Unsupported authorization claim* (a gap-only block is valid-with-gaps); design D5 and D7 |
| OQ-5 | Keep `schema_version: 1` and `profile: advisory-v1`, and first-bundle the declaration at the next additive minor? | **As recommended: yes.** | Not requirement text. The delta changes neither constant, and design D10 first-bundles the declaration at the next additive minor, with `target_release: deferred-allocation` in `proposal.md`. The number is allocated at the cut, never reserved here |
| OQ-6 | One issuer per hosted server, or a list? | **As recommended: exactly one.** | The requirement's "the token issuer" is singular; design D1's block shape carries one `issuer` string, and D4 says "One issuer per hosted server" |

OQ-5 and OQ-6 rest on the design's shape and the delta's singular wording
rather than on a requirement sentence that names them. The word adopts both
as drafted, so neither needs a requirement sentence added, and none was.

## 3. What the word does not decide

- **No landing.** It is a ratify word. This pull request stays a draft, and
  its landing takes a separate word under the Rule 6 landing window, with
  every required check green and Copilot's and Codex's reviews read at the
  exact head.
- **No archive.** `code_surface` is not empty, so the archive follows merged,
  green realization evidence (`tasks.md` § 4) and its own word. Nothing under
  `openspec/specs/` is edited, and canon keeps its eight requirements until
  that act.
- **No realization and no contract cut.** The Speckit feature (`tasks.md`
  § 2) is now allowed and is not part of this pull request. No schema,
  validator, test, runbook or contract-manifest byte moves, and no version
  number is reserved. The contract cut needs its own claim of row 4 on #630.
- **No downstream act.** The engineering domain's RS256 slice, the hosting
  plan's issuer correction and the operations gateway's intake alignment stay
  outside this change (`tasks.md` § 5).
- **One act is complete, and one is still owed.** The amendment of the #630
  claim, to say the seeder also flipped the partner ledger row and added the
  `_LEDGER_SUBJECTS` row (`tasks.md` 1.3), is DONE: #630 comment
  `6068473680`, 2026-10-08T20:29Z, before the word at 20:33:25Z. A Codex
  review is still missing, the connector having declined each trigger for
  want of quota, and stays with the lane's coordinator.

## 4. What the ratifying commit changes

None of these changes is requirement or scenario text.

- **`proposal.md`:** `Status: draft` becomes `Status: ratified`, with one
  `Ratified:` citation line, a ratified paragraph in place of the draft
  paragraph, and a short `## Ratification` section.
- **`design.md`:** `Status: ratified` with one `Ratified by:` line; the
  open-questions table gains a *Ruling* column, and the section's lead
  paragraph and the preface name the word.
- **`tasks.md`:** `Status: ratified` with one `Ratified by:` line; boxes 0.1
  and 0.2 are ticked with the word and this record.
- **`.openspec.yaml`:** `approved_by` and `approved_on` are ADDED to the
  origin after the drafting pair. Every field the declaration already carried
  is unchanged, so the approval is an addition and not a re-minting. The
  `proposal-origin` family requires the pair the moment a status claims
  approval.
- **`README.md`:** the *Active changes* entry's status and its closing
  sentences.
- **This record.**

Four files do not move, each for a reason:

- **`specs/factory-mcp-conformance/spec.md`:** the word ratifies the delta as
  drafted.
- **`tests/sequenced_after/corpus-ledger.yaml`:** the rows record state
  (`active`), class and declaration, and ratification moves none of them.
- **`tests/doc-health/test_modified_block_currency_self_gate.py`:** the
  `_LEDGER_SUBJECTS` row names the MODIFIED block, which does not change. It
  retires at the archive.
- **`tasks.md` 1.4:** the gates at the ratified head stay open, because that
  box names the required `pytest-suite` check, which is read at the exact
  head on the pull request and not in this file.

## 5. Corrections after the word, none of them requirement or scenario text

Copilot's review of the ratifying head `89506b51` raised five findings. All
five are corrections to design, task and record text, and none touches the
delta `specs/factory-mcp-conformance/spec.md` (blob `51fc770d`, unchanged):

- **`design.md` D7 and `tasks.md` 2.2.** D5 already said the block's
  `evidence_ids` and `gap_ids` resolve as a tool's do, with
  `missing_support_reference` and `duplicate_support_reference`. D7 now lists
  both codes with their `/service/auth/...` locations, and task 2.2 names a
  dangling and a repeated id as red-first cases. The requirement already says
  the block cites evidence or a gap, so no requirement sentence changes.
- **`tasks.md` 4.1.** The archive step now names the deferred-allocation
  transition `release-realization` requires before an archive: resolve the
  declaration to the literal release the cut allocated, citing the bundle
  version observed and the release surface carrying it.
- **`proposal.md` Claims, `tasks.md` 1.3, this record's § 3 and the README
  row.** The #630 claim amendment is recorded as done (comment `6068473680`,
  2026-10-08T20:29Z), which the draft text still called owed.
