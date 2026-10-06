# Proposal Ratification: add-worker-input-budget

Status: ratified
Kind: report
Decision date: 2026-10-06
Ratifier: Brett Heap (openxFactory repository owner)
Ratified: 2026-10-06 by Brett Heap (openxFactory repository owner) — in
session to lane `openxfactory-1`, verbatim *"0.4: (a) ratify as they stand"*,
recorded as a RULED line on the estate's lane register at
**2026-10-06T13:55:03Z** (`opensoft/brett-wip` commit
`06709554ec852cf39ef26bcc6a749682a946f8a8`, `lanes/log/openxfactory-1.md`).
Ratified baseline: the packet as it stands on `main` at `92010d3e`, unmoved
since #1198 landed at `51887c6f` (2026-09-29); its spec delta unmoved since
#1137 landed at `9da52e31` (2026-09-22).

## Decision

**RATIFIED AS THEY STAND.** Both `doc-health` spec deltas in
`specs/doc-health/spec.md` are ratified with no amendment. No requirement or
scenario text moves:

- the MODIFIED requirement *Sweep sequencing and snapshot consistency*: its
  restated body and its three scenarios (*A nightly run executes both
  passes*, *The deterministic pass fails* and *The input budget holds
  documents back*);
- the ADDED requirement *Bounded worker input budget*: its body and its six
  scenarios.

The ratified text is the delta file's blob
`9a817d65b3c38d3b4c9d8acc1f1f7cfc33366900`. It is the same blob at #1137's
merge commit `9da52e31` and on `main` at `92010d3e`.

## 1. The word, and the question it answers

> 0.4: (a) ratify as they stand

Brett Heap gave this word on 2026-10-06, in session to lane `openxfactory-1`.
It answers `tasks.md` 0.4, *"Ratify or amend the two spec deltas"*. The
question was put to him as, verbatim, *"task 0.4: (a) ratify the two
doc-health deltas as they stand, or (b) amend first"*, and he chose (a).

The lane recorded the word the same hour as a RULED line on the estate's lane
register, at 2026-10-06T13:55:03Z, object
`opensoft/openxFactory:openspec/changes/add-worker-input-budget`
(`opensoft/brett-wip` commit `06709554`, `lanes/log/openxfactory-1.md`). The
lane has held this change's claim since 2026-09-24T16:33:03Z, on the same
register.

## 2. What the word does not decide

- **The Group 4 sequencing question on 4.1 stays open.** The `tasks.md`
  Group 4 note, *"Sequencing tension, named rather than hidden"*, puts a
  question to Brett Heap. Was the operational word *"land the input-size
  guard when green"* the approved exception the house rule contemplates, or
  should 0.4 have gated 4.1 regardless? This word ratifies the spec text and
  does not answer that question. The note does not move.
- **No archive.** `code_surface:` is non-empty, so `release-realization`'s
  archive gate needs merged, green realization evidence, which Group 4
  records. The archive itself is a separate later act on Brett Heap's word.
  This record promotes nothing into `openspec/specs/`.
- **No realization moves.** The realization landed on 2026-09-22: #1137 at
  `9da52e31` and `opensoft/xFactory#481` at `b2479b6e`. It landed under the
  separate operational word that task 4.1 records. This record neither
  re-authorizes nor revisits it.
- **No proposal substance moves.** OQ-1, OQ-2 and OQ-3 stand as resolved, and
  `code_surface:` and `target_release:` stand as landed. The packet has no
  `design.md`.

## 3. What this pull request changes

None of these changes is requirement or scenario text.

- **`proposal.md`:** `Status: draft` becomes `Status: ratified`, with one
  `Ratified:` citation line beside it in the front-matter header.
- **`tasks.md`:** box 0.4 is ticked, with the word and this record.
- **`README.md`:** the *Active changes* entry's status, and its closing
  sentence, which said the status was unchanged.
- **This record.**
- **`.openspec.yaml`, new, on a second ruling.** Brett Heap, 2026-10-06, in
  session to lane `openxfactory-1`, verbatim *"#1250: (i) add the origin
  file"*. It is recorded as a RULED line on the estate's lane register at
  2026-10-06T17:24:57Z (`opensoft/brett-wip` commit `f739ab74`,
  `lanes/log/openxfactory-1.md`).
  - **Why it was needed.** Copilot's finding `r4196698454` on this pull
    request was correct against canon. `document-lifecycle` § *Proposal
    origin declaration* says that a proposal whose `Status:` declares
    `ratified` SHALL carry approval provenance in its origin. This packet
    had no `.openspec.yaml`, and it was the only active change without one.
  - **What it declares.** It is hand-written in the form of the 2026-08-25
    origin sweep `b7513733`. Every value is derived from this packet's own
    record:
    - `created: 2026-09-22`, from the packet's true first commit,
      `ee2185d6` (2026-09-22T01:26:47Z);
    - `kind: ad_hoc`, because no `Staging ID:` header and no staging topic's
      exit names this change, checked in both directions;
    - `id: openxFactory:adhoc:2026-09-22-add-worker-input-budget`;
    - a folded `reason` that quotes this ruling;
    - the drafting pair: lane `openxfactory-1`, on Brett Heap's word *"brief
      a writer to add the input-size guard"*, 2026-09-22;
    - the approval pair: the 0.4 word of § 1, dated 2026-10-06.
  - **What it changes in the measurements.** `proposal-support.py verify`
    now passes for this change, where `main` refuses it with *"no origin
    declaration"*. The `proposal-origin` family's WARNING for the missing
    declaration is gone. § 5 carries the figures.

Two files do not move, and each has a reason:

- **`specs/doc-health/spec.md`:** the word ratifies the deltas as they stand.
- **`tests/sequenced_after/corpus-ledger.yaml`:** the row records the
  change's state (`active`), class and declaration. Ratification moves none
  of them.

## 4. A disclosure, not an amendment

`proposal.md` § Impact reads *"`doc-health` (two requirements MODIFIED, one
ADDED)"*. The delta has carried ONE `## MODIFIED` requirement and ONE
`## ADDED` requirement since its first commit, `ee2185d6`.

The proposal's § *Why this is normative and not an implementation detail*
names a second reached point, *The semantic sweep is unavailable*. In canon
that is a scenario, not a requirement. The ADDED requirement's scenario *A
prior finding's document was deferred* is the text that answers it.

The word ratifies the deltas as they stand, which means the two requirements
named above. The Impact line is proposal text, so this record does not
correct it. It is reported to the lane with this record.

## 5. What was measured

Each gate ran at the same time in two full clones of the same kind:
- one at `main` `51456835`;
- one at this pull request's merged head `9e67f838`, which is `main`
  `51456835` plus this pull request.

The only change made after that head is this section's own text. An earlier
pair of runs, taken before the origin file existed, measured `main`
`92010d3e` against the ratifying commit and found every result identical.

| gate | `main` `51456835` | this pull request |
| --- | --- | --- |
| `scripts/validate-openspec-cli-pin.py --all --strict` | exit 0; 112 passed and 1 failed of 113 items. The one is `add-chain-attestation`'s accepted exception; 0 UNDISPOSITIONED | the same |
| `scripts/validate-openspec-cli-pin.py --change add-worker-input-budget` | exit 0; 1 passed, 0 failed | the same |
| `scripts/validate-code-surface.py .`, `scripts/validate-target-release.py .`, `scripts/validate-scope-globs.py .` | exit 0 | the same output |
| `scripts/validate-sequenced-after.py .`, and with `--ledger-diff` | exit 0 | the same output; this packet's ledger row does not move |
| `scripts/proposal-support.py . verify add-worker-input-budget` | exit 1, *"no origin declaration"* | **exit 0**, *"proposal support verification ok"* |
| `scripts/doc-health.py --single-repo . --as-of 2026-10-06` | 284 finding lines. Two name this packet: the `proposal-origin` WARNING for the missing origin, and the `modified-block-currency` INFO that records the MODIFIED block's deliberate rewording of canon's *"is exactly"* bullet | 282 finding lines: the same set without the `proposal-origin` WARNING's two lines. **No new finding**; the INFO stays |
| `pytest` over `tests/doc-health`, `sequenced_after`, `review_lane_pin`, `proposal-support`, `code_surface`, `target_release`, `packet_reference`, `citation_remainder`, `scope_globs`, `former_id_arrival` and `openspec_cli_pin` | 3581 passed, 7 failed and 3 skipped | the same; the same 7 tests fail. All 7 come from the clone, whose `openDox` and `openXdox` legs were not initialized |

This record and the `Ratified:` line in `proposal.md` are each inside
`ratified-provenance`'s scan set, and neither draws a finding. A probe on a
throwaway copy proved the scan. Damaging either citation, or giving this
record a status other than `ratified`, raised a CRITICAL finding naming the
damaged file.

A second probe ran the archive gate's origin-retention walk
(`proposal-support.py`'s `origin_retention_errors`) on throwaway copies of
both possible landings of this pull request onto `main` `51456835`:

- **A squash landing:** the squash commit is the ratifying commit, so the
  origin is part of it. The walk reports *"ORIGIN RETAINED … declaration
  unchanged since the ratifying commit"*.
- **A merge landing:** the walk takes `a93865f0` as the ratifying commit.
  That commit declares no origin, so the walk reports *"ORIGIN RETENTION NOT
  COMPARABLE"*, which the gate treats as lawful.
