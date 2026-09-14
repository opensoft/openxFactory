# Proposal Amendment: split-opendox-two-layer-product — the § 5.2 shed's own prerequisite, resolved as exit (a) POST-SHED MODE

Status: record
Kind: decision record
Decision date: 2026-09-10
Lane: openxfactory-4-opendox-extraction (formerly openxfactory-opendox)
Ruler: Brett Heap (repository owner), in session, over the addendum's three
costed exits (a)/(b)/(c), the addendum presented first.
Ruled: 2026-09-10T21:1xZ, verbatim: *"rule (a) post-shed mode, merge 924 when
green."*
Ruling URL:
<https://github.com/opensoft/openxFactory/issues/656#issuecomment-5625573095>
Addendum (the measurement this ruling decided over): `#656` comment
`5625144570`, 2026-09-10T20:3xZ.
Amends: `split-opendox-two-layer-product`, RATIFIED 2026-09-05 (record
`review/ratification-2026-09-05.md`), previously amended 2026-09-05
(repository shape, record `review/amendment-2026-09-05-repository-shape.md`)
and 2026-09-09 (FLOOR PART 2 restated as a mapping, record
`review/amendment-2026-09-09-floor-part-2-mapping.md`).

**THIS IS AN AMENDMENT, NOT A RE-RATIFICATION.** The packet stays ratified.
RULING OQ-1's four-part floor is not reopened and no part of it changes shape;
what this amendment adds is a fifth capability of FLOOR PART 1's own
instrument — the manifest validator — needed because FLOOR PART 1 was
authored to run only up to the carve, and the shed runs the same validator
past it. Every edit is VISIBLE in the tree as an inline `> Amended
2026-09-10.` note in the lifecycle's own form (`docs/document-lifecycle.md`),
following the same discipline the 2026-09-05 and 2026-09-09 amendments used.

## What was found, and why it is a prerequisite rather than a build detail

The § 5-remainder session's reality-check record
(`review/reality-check-2026-09-10-section-4-and-the-shed.md`, `Status:
record`, § 2, "The § 5.2 shed cannot land while the manifest stands") probed
the shed on two throwaway commits, discarded after measurement:

- **Probe 1** — deleting the ONE `deleted_at_carve` row alone
  (`scripts/ideation_dashboard/profile_openxfactory.py`) already refuses:
  `FAIL docs/opendox-carve-manifest.yaml: carve-path-absent — 1 row(s) name
  path(s) DELETED SINCE THE CARVE`, `exit=2`, and the required-suite seat goes
  `1 failed, 197 passed` against a `198 passed` baseline.
- **Probe 2** — the whole shed, all 319 rows — refuses identically, from the
  first row rather than the last.

`check_surface`'s walk in `scripts/validate-carve-manifest.py`, unmodified,
refuses ANY tree in which a manifest row's declared source path has been
deleted, because it reads that path at the revision under test and a row does
not stop naming it just because the bytes already arrived at their
destination. **The § 5.2 shed deletes 319 of the manifest's rows BY
CONSTRUCTION**, so this is not a bug to fix inside the shed commit — it is an
unresolved prerequisite of § 5.2 that the record explicitly left "owed a
ruling — a post-shed mode on `validate-carve-manifest.py`, a re-cut at the
shed, or a declared retirement of the manifest as the shed lands. Nothing in
this record chooses among them." This amendment is that ruling, applied.

## What the ruling decides: exit (a), POST-SHED MODE

One optional manifest key, `phase: carve | post-shed` — no CLI flag, no
`shed_commit`. The addendum's spike (opus-max, throwaway clone, nothing
pushed; measurement note `ideation/brainstorm/opendox-shed-exit-a-post-shed-mode-measured.md`,
openxFactory #929, landing) measured it over the FULL shed tree (all 319 rows
deleted):

```
OK … phase post-shed, 456 row(s) … 318 digest(s) recomputed; 456 file(s) in
the declared surface with none undeclared; 319 shed row(s) absent at source
as declared
```

exit 0; carve suites `209 passed` (baseline 198, +11 for the new phase logic's
own tests). The UNMODIFIED validator over the identical tree reproduces the
`1 failed, 197 passed` finding exactly.

- **The two arms of `carve-path-absent` that read a row's source path change
  what they expect there.** Under `phase: post-shed`, a moved row's source is
  EXPECTED absent rather than required present; every other check — 1, 2
  (ANCESTOR), 5, 6, the 318 referent digests, the 794 line bounds — is
  unaffected by the phase.
- **Symmetric guard, so the flip and the deletions are one act.** A moved row
  still PRESENT at its source under `phase: post-shed` refuses under a NEW
  code, `carve-shed-incomplete`. A manifest that claims `post-shed` while any
  moved file still sits at its old path is refused, not silently accepted —
  there is no state in which the phase says "shed" and the tree says
  "carve," even transiently.
- **Nothing about identity moves.** `carve_commit` stays
  `b075fd91dc8fced8e1373825ba80220c33536bae` (tag `opendox-carve-0`); every
  digest recorded at that commit is unchanged; **zero rows change
  disposition**. Arrival stays `verify-carve-arrival.py`'s own job, undisturbed
  by the phase (three legs' phase-B summaries measured byte-identical
  pre/post shed in the spike; the fourth needs its recorded `--replica-at`
  flags identically, which is a build detail of PR-2, not of this ruling).
- **The diff that realizes exit (a) is small and does not touch arrival.**
  Measured: 482 added / 17 removed over 4 files (the validator, its tests, the
  manifest's own `phase:` documentation +18/−1, the runbook +24/−2). **Zero
  lines** in `verify-carve-arrival.py`, `carve_lines.py`,
  `tests/carve_arrival/`, `pytest-suite.yml`.

## What was NOT taken, and why (from the same addendum)

- **(b) A re-cut AT the shed.** Costed at zero: it can describe only 137
  files, 0 moved rows, 0 declared lines (9 of 39 `moved_paths:` prefixes
  vacuous) — the mapping is thereby DELETED, not re-cut — plus 15 files / 40
  lines of fresh provenance across four repositories and two of Brett Heap's
  own acts, and it leaves runbook § 11 step 6 with nothing to re-verify. NOT
  TAKEN.
- **(c) Declaring the manifest retired.** Costed at zero lines, green
  immediately via the validator's own not-fail-closed branch (`NO MANIFEST …
  (nothing to validate)`, `198 passed`) — but it drops the 318 referent
  digests, the 794 line bounds, the 456-file completeness walk, the
  frozen-surface `appeared` guard and the 137 retained rows' presence
  requirement; it makes 7 real-manifest tests vacuous; and it makes
  `verify-carve-arrival.py` unrunnable at every destination
  (`arrival-unreadable`). NOT TAKEN.

## Realization: two pull requests, one atomic act each side of the gate

- **PR-1 — the post-shed mode CAPABILITY** (starts on this ruling; does not
  wait on PR-2's sub-questions). The `phase:` key, the `carve-shed-incomplete`
  refusal code, their tests, the manifest's own documented `phase:` field
  (staying `carve` until the shed actually flips it), and runbook § 8 text —
  **openxFactory #928**, landing at the time of this amendment.
- **PR-2 — the shed itself.** The phase flip to `post-shed`, the 319
  deletions, and whatever `tasks.md` § 5.2's three still-open sub-questions
  (2), (6), (7) decide, as ONE atomic pull request under Rule 6 (a partial
  shed leaves the tree in a state neither this ruling nor FLOOR PART 1
  describes). NOT STARTABLE until those three are answered.

Standing and unchanged by this ruling: "start § 3.7 and merge it when green"
(#920, Rule 6), and #924's independent landing (the § 4 boxes record + the
5.1 tick), which this amendment does not revisit.

## What this amendment does NOT move

- **RULING OQ-1 is not reopened.** The four-part floor keeps its four parts;
  this amendment is an operating-mode addition to FLOOR PART 1's own
  instrument, not a redefinition of any part.
- **No promoted requirement is authored, modified or removed.**
  `openspec/specs/` is untouched by this amendment, for the same reason § D6
  gives for the floor overall: the obligation binds this change directly
  rather than through a spec delta.
- **`docs/opendox-carve-manifest.yaml`, `scripts/validate-carve-manifest.py`,
  `scripts/verify-carve-arrival.py`, `scripts/carve_lines.py` and
  `.github/workflows/pytest-suite.yml` are not edited by this amendment.**
  This record is packet-side text; PR-1 carries the code and manifest edits
  the ruling authorizes.
- **The two lane-default items the ruling comment names for PR-1** ("(3)
  correct the two places documenting `--at <carve_commit>`"; "(4) the seventh
  refusal code joins the tuple") **are PR-1's own scope**, not this amendment's
  — recorded here only because they are part of the same ruling comment.
  **One correction of fact, carried rather than repeated:** the ORDINAL in (4)
  is wrong and the ruling's substance is not. `REFUSAL_CODES` in
  `scripts/validate-carve-manifest.py` stood at ELEVEN members when the ruling
  was worded, so `carve-shed-incomplete` joins as the **12th of 12 refusal
  codes**, not the seventh — it is written in the tuple's eleventh position,
  ahead of `carve-unreadable`, which the tuple deliberately keeps last as the
  ENVIRONMENT-and-ENCODING code. PR-1 (#928 → `0e76e789`) landed it there, and
  `RATIFIED_CODES` in `tests/carve_manifest/test_carve_manifest.py` restates all
  twelve as a literal so neither the count nor the order can drift unremarked.

## What changed, file by file

| file | before | after |
| --- | --- | --- |
| `design.md` header | two `Amended:` lines (2026-09-05, 2026-09-09) | a THIRD, naming RULING (a), the verbatim word, the comment id and this record |
| `design.md` § D6, end of part (1) | no mention of the shed's own prerequisite | an inline `> Amended 2026-09-10.` block: the measured refusal, the ruling verbatim, exit (a)'s semantics, exits (b)/(c) named and costed, the two-pull-request realization plan |
| `tasks.md` § 5.1 tick note | aside: "moved in PR #917's one commit (… nothing else in that diff)" | corrected: names commit `7f76f978` explicitly, states the three files the aside omitted, and affirms 5.1's own text (pin + gitlink, same commit) still holds |
| `tasks.md` § 5.2 (still open) | the deletion list alone, no ruling citation | a dated STATUS paragraph: RULING (a) with the comment id, PR-1's status, PR-2's three named sub-questions, and the probe-1 "4 errors" → 27 correction, citing the immutable record rather than editing it |
| `proposal.md` header | `Ratified:` + two `Amended:` lines (2026-09-05, 2026-09-09) | a THIRD `Amended:` line naming RULING (a), the verbatim word, the comment id and this record; `Status:`, `Ratified:`, `Lane:` and both prior lines UNTOUCHED |
| `proposal.md` § *Rulings carried as LOCKED constraints* item 12 (RULED OQ-1) | FLOOR PART 1 as *"a mapping manifest with per-file digests at the cut plus a CLOSED edit-class list"* | the same sentence with an inline amendment clause naming the optional `phase:` key, its two values, the symmetry and the ruling's comment id. The other three parts and both rejected alternatives are byte-identical, and part 2's 2026-09-09 clause is untouched |
| `proposal.md` `code_surface` items (1) and (3) (RULING F) | *"`openxFactory` does NOT pin openDox's assembly root directly"* / *"never separately declared, pinned or mounted here"* | each keeps its original sentence and gains an `AMENDED 2026-09-10 — RULED Q7` note: TWO direct upstreams, the LOCKSTEP invariant that preserves RULING OQ-2's one chain, and openxFactory #932 → `f4fb4ffc`. Nothing is deleted |
| `design.md` § D12's pin discussion | *"openDox's commit there is a DERIVED value read through openXdox's own pin"* | the sentence is kept and followed by the RULED Q7 amendment note: the direct `openDox` gitlink and `contracts/opendox-pin.yaml`, the LOCKSTEP invariant as what survives of RULING F, its verifier and its test, and § 5.2 as the reason the mount exists at all |
| `README.md` OpenSpec Records row | ratified + two amendments | a third amendment clause in the same form, with FLOOR PART 1's unchanged referents and the one-act symmetry |
| this record, § *Scope* | the ruling comment's *"(4) the seventh refusal code"* quoted without comment | the quote kept, with the ordinal corrected in place: `carve-shed-incomplete` is the **12th of 12**, written eleventh in the tuple ahead of `carve-unreadable` |
| `review/amendment-2026-09-10-shed-exit-post-shed-mode.md` | — | this file |

**Nine sites, four files plus this record** — as first written this record said
*"four sites, two files"* and declared `proposal.md` and `README.md` NOT
touched, "a later hand extending this amendment to `proposal.md`'s header and
eleven-acts list and to `README.md`'s OpenSpec Records row (the form both prior
amendments used) would be completing the convention, not contradicting it."
PR-2 is that later hand and took the extension, so the footprint now matches
the 2026-09-05 and 2026-09-09 amendments' own rather than being narrower than
them. The original sentence is quoted here rather than deleted.

## Verification

- `OPENSPEC_TELEMETRY=0 openspec validate split-opendox-two-layer-product --strict`
  and `--all --strict`, through the repository's pinned CLI entrypoint.
- `python3 scripts/proposal-support.py . verify split-opendox-two-layer-product`.
- No code, manifest or workflow file is touched by THIS AMENDMENT's own text,
  so no suite run is owed by it beyond the doc-health / lifecycle checks that
  read `Status:` headers and requirement structure. *(Read with care: the PULL
  REQUEST that carries this record — PR-2, the § 5.2 shed — does touch the
  manifest, the tree and `.github/workflows/pytest-suite.yml`, and it runs the
  whole required suite. The sentence above scopes the amendment, not its
  carrier.)*
