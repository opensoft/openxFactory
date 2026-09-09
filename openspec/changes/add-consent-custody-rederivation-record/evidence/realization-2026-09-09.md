# Realization record — add-consent-custody-rederivation-record

Status: record
Lane: opsXfactory-1
Realized: 2026-09-09, branch `033-add-consent-custody-rederivation-record`,
Speckit feature `specs/033-add-consent-custody-rederivation-record`

**WHAT THIS FILE IS.** The packet-side half of the realization evidence. The
raw gate transcripts, the fixture-corpus design, the doc-health report pair and
the tick audit live in the feature tree at
`specs/033-add-consent-custody-rederivation-record/evidence/`; this file records
what was DONE, what was DELIBERATELY NOT done, and where each claim is proven.

## What landed

| § | Act | Commit |
| --- | --- | --- |
| 2 | The schema grows the closed `custody_rederivations[]` sibling; `contract_schema_version` 2 → 3; the `consent-instrument` row's digest re-derived in the same commit | `f59a587d` |
| 3, 4 | The validator's internal legs, the WITHHELD third outcome and exit `3`, the extended blob walk, seventeen fixtures across three buckets, the three corpus-count surfaces — **and `tests/consent_instruments/`**, because box 3.3 asks for a TEST that pins an absence and a tick cannot precede its own evidence | `f420cd50` |
| — | Q8's three README amendments, in the `3b530009` form | `7c79f524` |
| 5 | **THE CUT — `contract-v3.5`**, every release surface in ONE candidate commit, plus the cut-coupled `test_release_boundary.py` edits | `d54d89ca` |

Integration point: `origin/main` at `587f21a0`, merged in (never rebased —
opensoft org ruleset 8981805 forbids non-fast-forward updates).

## The number

`contract-v3.5` was **MEASURED FREE at the integration point on all three
surfaces** — `contracts/manifest.yaml:3`, the highest `contracts/releases/`
inventory, and the highest `contract-v*` tag. **A measurement, never a
reservation.** The CLAIM on openxFactory issue #630 row 4 is the LANE's, at cut
time, and is not made by any commit on this branch (box 5.1).

## Gates

Five against the exact unchanged candidate `d54d89ca`, transcripts at
`specs/.../evidence/phaseG-T064-gates.txt`: `release-tag-gate` rc=0 with an
EXPLICIT `--base` (the default would have diffed the wrong tree and looked like
a pass); the full suite 10662 passed / 36 skipped / 1 failed, that failure
proven pre-existing by a baseline in a separate clone at pristine `origin/main`;
`validate-manifest-digests.py` rc=0 at 189 digests; `verify-commit` rc=0;
`validate-consent-instruments.py --strict` rc=0. doc-health as a two-report pair
added **ZERO** findings at any severity and REMOVED three.

## Boxes

**35 ticked + 3 NOT-OWED-HERE + 8 NOT-OWED = 46.** Every tick rides the same
commit as its evidence, proven from history at
`specs/.../evidence/phaseH-T083-tick-audit.txt`.

## THREE THINGS ARE RECORDED HERE AND DELIBERATELY NOT DONE

### 1. The cross-repo consequence is RECORDED, NOT ARMED (clarify A2)

Landing this realization **DECLARES** the consent family's re-derivation rule.
Under `govern-archived-record-edits`' transition clause, an edit of a consent
pinned target therefore converts from **REPORTED** to **REFUSED** for that
family — **once F.2's gate exists**, and that gate is OpsxFactory's (§ 7.1).
Nothing here builds it, schedules it or arms it. It is written down so the
conversion is a known consequence of landing rather than something discovered
afterwards. The same note sits beside § 7 in `tasks.md`.

### 2. The identical-locators `path_only` gap is an OWED FINDING

**(a) The defect.** `path_only` means *only the locator changed*. An entry
declaring it with `previous_locator == observed_locator` — and so, by task
3.4c's leg, equal digests — records an event that did not occur. Nothing in the
schema, the validator as realized, or the ratified delta refuses it.
**(b) The leg it would need, and why it is NEUTRAL.** A check that
`previous_locator != observed_locator` whenever `diff_class: path_only`. Design
C-7's placement test puts it on this side of the line: both locators are fields
of the record, so the contradiction is derivable from the record's own bytes
without opening a repository — the same test that placed `path_only` digest
equality here.
**(c) Its home.** F.2's custody-digest gate (§ 7.1, OpsxFactory's) or a
successor openxFactory change. **No refusal leg was added**: no ratified task
names it, and this packet's rule is realize-what-was-ratified.

### 3. A DEFECT IN A RATIFIED TASK'S PARAPHRASE, found by a fixture

Task 3.2's shorthand — refuse when `custody.sha256` equals **any** entry's
`observed_sha256` while a later entry exists — **refuses `design.md`'s own
prescription I**, the estate's measured repair, because a `path_only` move
changes zero bytes and so makes the pin equal e1's observed digest BY
CONSTRUCTION. Applied literally it makes `reason: archive_move` unusable by any
conforming record — the exact failure C-6a was raised to fix. **The delta
governs**: it speaks of a digest *"written back into `custody.sha256`"* and of
leaving the pin *"verbatim"*, both claims about the pin having CHANGED, so the
implemented leg is ANCHOR-RELATIVE and `custody-pin-rewritten` still fires on a
genuinely rewritten pin. **No ratified text was altered**; `tasks.md` § 3.2
keeps its wording. Full write-up:
`specs/.../evidence/FINDING-pin-leg-contradiction-2026-09-09.md`.

## Not this change's, and named so

§ 6 is the CONSUMER's — the `stack.yaml` re-pin in lockstep with the
worker-enrollment-broker, the three NON-UNIFORM prescriptions, the declared
custody store mapping and the operated custody-digest check. **No OpsxFactory
file is written by this realization**, so the three broken custody pins stay
broken until the consumer acts, and F.1 stays ADDRESSED rather than discharged.
§ 5.5's landing tick and § 5.6's annotated tag are the lane's and the operator's.
