---
code_surface: openxFactory — `scripts/doc_health/families.py` and the tests that pin it in `tests/doc-health/test_grandfather_dispositions.py` (NEW). ONE LAST PASS IS ADDED TO ONE FAMILY AND NOTHING ELSE MOVES: `fam_ratified_provenance` returns `_honour_grandfather_dispositions(ctx, findings)` instead of `findings`, and that pass downgrades a finding to `info` exactly when the finding's `(repo, path)` carries a DATED, cited `family: ratified-provenance` entry in the aggregation's `health/dispositions.yaml` AND the path is under `openspec/changes/archive/`. The admission rule is NOT re-decided here — `promotion_fidelity.load_dispositions`, the estate's one reader of that file, is asked which entries are RECORDED and this module supplies only the citation TEXT a downgraded finding quotes, narrowing that set by the `date` the scenario asks for and by nothing else (a narrowing, never a widening). NOTHING ELSE MOVES: no arm, no scope, no document set, no threshold, no resolution class, no other family, no report field, no workflow, no contract member, no schema and no path; every finding the five existing arms build is returned as they built it, by identity, unless it is one of the dispositioned archived rows. NINETEEN tests are ADDED in one new file (`tests/doc-health` 1689 -> 1708); NO existing test is edited, renamed, flipped or deleted.
target_release: implemented (the openxFactory main line). No contract bundle is cut, nothing under `contracts/` is touched, no digest set moves, no `contract_bundle_version` is spent and no release tag is owed. Under `release-realization` a non-empty code surface archives on MERGED-PLUS-GREEN REALIZATION EVIDENCE rather than on landing, so this packet realizes through its own task list in this pull request and its realization evidence is that pull request's green `pytest-suite` run at the tree the merge carries.
sequenced_after: []
---

# Proposal: honour-grandfather-dispositions-in-ratified-provenance

Status: draft
Proposed: 2026-09-11, in lane `openxfactory-1` (display `openXfactory-1`),
session `a9c24afc`, on Brett Heap's word of 2026-09-11 at approximately 01:3xZ
— a MULTIPLE-CHOICE ruling whose chosen option is verbatim
**"Commission the packet"**.
Origin: openxFactory
[#939](https://github.com/opensoft/openxFactory/issues/939), filed by this lane
at that commissioning, standing on
[#877](https://github.com/opensoft/openxFactory/issues/877) (the records) and
[#878](https://github.com/opensoft/openxFactory/issues/878) (the arm that
reports them).

**THAT WORD COMMISSIONS THE AUTHORING, NOT THE CONTENT. RATIFICATION IS OWED
AND IT IS BRETT HEAP'S ACT.** Nothing below is ratified by being authored; no
requirement here may be cited as approved until he rules on this packet itself;
`.openspec.yaml` declares drafting provenance with **no approval pair**, and
every document in this packet carries `Status: draft` to match. **NOTHING IS
PROMOTED** — this pull request edits no file under `openspec/specs/`. Every
judgment this authoring session took is listed in `design.md` as **D0 through
D6**, each with a recommendation and each put for veto; the two most worth one
are **D1** (an `info` row against silence) and **D2** (the archived-only
boundary).

## Why

**EIGHTEEN ARCHIVED RECORDS STAND AT `critical` IN THE NIGHTLY WITH NO REPAIR
AVAILABLE TO ANYONE AND A RECORDED RULING SAYING NONE IS OWED.**

Fifteen openxFactory ratification records were grandfathered on issue
[#877](https://github.com/opensoft/openxFactory/issues/877) — the disposition
act is `opensoft/xFactory` PR #420 → `5bfa1fe4` — and codexFactory's three on
`opensoft/xFactory` PR #412. Each of the eighteen has an entry in the
aggregation's `health/dispositions.yaml` carrying `family:
ratified-provenance`, its repository, its path, a `date`, and a `cite` quoting
Brett Heap first-hand. Each of the eighteen is **ARCHIVED**, which is the whole
ground of the grandfather: `record-immutability` and `govern-archived-record-edits`
put an archived packet's bytes beyond a plain fix, so the owner ruled instead
of editing.

**AND THE FAMILY HAS NEVER HEARD OF ANY OF IT.** `scripts/doc_health/families.py`
`fam_ratified_provenance` builds every one of its findings at `CRITICAL`, from
five arms, and consults no disposition at any of them.

The runner does read that file — but not for this.

```python
    dispositions = set()
    dispo_path = (ctx.agg_root / "health" / "dispositions.yaml"
                  if ctx.agg_root else None)
    ...
    result.findings += report.uncited_resolutions(
        result.findings, previous_contested, dispositions, ...)
```

`report.uncited_resolutions` adjudicates a **CONTESTED** finding that was in a
previous report and is absent from this one. It silences a DISAPPEARANCE, never
a standing finding; and `ratified-provenance` is not in
`families.FAMILY_RESOLUTION`, so its findings are `auto-fixable` and are not
even in the `previous_contested` set that arm reads. The disposition is a
governance record that moves nothing a reader sees.

**THE ONE OTHER LANE THAT READS THE FILE SHOWS WHAT THE MECHANISM IS FOR.** The
`neutrality-drift` lane consumes the same vocabulary directly
(`docs/doc-health.md`, *Dispositions keying*), and so do three deterministic
families through one shared reader, `promotion_fidelity.load_dispositions`:
promotion fidelity, duplicate packet and modified-block currency. Four promoted
requirements already carry a *A finding is dispositioned* scenario. This family
needed one and never got one.

## Why this is NOT a plain fix

**BECAUSE THE PROMOTED REQUIREMENT DOES NOT SAY IT.** `doc-health`'s *Governed
corpus membership and the lifecycle scan set* is where this family's reporting
duty over a scan-set document is written:

> #### Scenario: A proposal carries an uncited ratified header
> - **WHEN** a document in the lifecycle scan set carries `Status: ratified` with no ratification citation in either sanctioned spelling
> - **THEN** the run MUST emit a `ratified-provenance` finding against that document's path
> - **AND** the finding MUST carry the same severity it would carry for a governed-corpus document, **because the defect is the same defect**

Nothing in that requirement admits a severity that moves for any reason.
Lowering a band canon fixes, in code, with no delta, is the shape this
repository refuses — and refused in terms on PR #780: *"Rewording the
requirement here would edit ratified text with no word behind it."* So the
remedy is a `## MODIFIED` block with the realization in the same pull request
under `release-realization`'s merged-plus-green rule, which is the shape
`amend-marker-defect-reporting` and `amend-marker-declaring-nothing` were both
authored on.

## What changes

**ONE `## MODIFIED` REQUIREMENT, ONE SCENARIO ADDED AT ITS END, AND NOT ONE
BYTE OF PROMOTED TEXT EDITED.** The block is canon's own bytes — lines
**878–936** of `openspec/specs/doc-health/spec.md`, sliced rather than
transcribed, `sha256
d32aaa43dc6ad118af3a57d58a2a3ffcb80c66ae128ca36b2921224a30bfdbe3` on both sides
— with one `#### Scenario:` appended. No body paragraph is added, edited or
removed; no promoted scenario moves, is retitled or loses a bullet; no marker is
declared, there being nothing removed to declare. Verified after the fact by the
family's own derivation: **29 canon units, 0 uncarried, 5 of 5 promoted scenario
titles carried, 8 units added (one scenario title and its seven bullets), 0
markers on either side.**

The added scenario, *A finding is grandfathered by a recorded disposition*,
says four things: an ARCHIVED-path finding named by a dated, cited entry for
this family is reported at **`info`** with the citation quoted and its family,
repo and path unmoved; the citation MAY be a bounded single-line excerpt; an
**ACTIVE** packet's record is never downgraded by such an entry; and an entry
with no `cite`, or a run with no aggregation checkout, changes nothing.

**THE REALIZATION RIDES THIS PULL REQUEST.** `scripts/doc_health/families.py`
gains a last pass, `_honour_grandfather_dispositions`, and two small helpers.
The admission rule is **delegated, not re-decided**: `promotion_fidelity.load_dispositions`
— the one reader promotion fidelity, duplicate packet and modified-block
currency already share — is asked which entries are live under this family's
name, and this module supplies only the citation TEXT that reader does not
return. A second admission rule written here is exactly how two readers of one
file come to disagree about which entries are live.

## The measurement, taken before the design

Measured on `main` @ `96b4835b`, against the REAL aggregation dispositions file
(`opensoft/xFactory` @ `bc84d325`, 40 entries, 18 of them
`family: ratified-provenance`), with `openxFactory` @ `96b4835b` and
`codexFactory` @ `a67fb0ae` materialized under an aggregation checkout —
`python3 scripts/doc-health.py --repo-root <aggregation> --family ratified-provenance`:

| | rows | critical | info |
| --- | ---: | ---: | ---: |
| before | 41 | 41 | 0 |
| after | 41 | 23 | 18 |

The **same 41 paths** on both sides. The eighteen that move are **exactly** the
eighteen `family: ratified-provenance` entries the file carries — a set
equality, not a count — and all eighteen are archived paths. The other
**twenty-three rows are byte-identical**: severity, rule, action and resolution
class alike. Nothing else in the report moves except the headline count that
sums the bands.

**THE DOWNGRADE TAKES THE EIGHTEEN OUT OF BOTH COMPARISONS, WHICH IS THE RIGHT
ANSWER AND IS MEASURED RATHER THAN ASSUMED.** `report.parse_previous` admits
only `critical`/`error` rows to `keys`, and `report.regressions` considers only
`critical`/`error` findings, so an `info` row can neither be a regression nor
make one. `report.uncited_resolutions` reads the `contested` set alone, which
this `auto-fixable` family is never in. The eighteen leave the regression axis
and enter no other.

## What this proposal does NOT do

- **It does not repair a record.** No archived record's bytes move, here or
  ever; that is what makes them the subject of a ruling rather than of a fix.
- **It does not add or remove a disposition.** `health/dispositions.yaml` lives
  in `opensoft/xFactory` and is not touched by this pull request at all.
- **It does not change which documents the family reads**, what it looks for,
  or what it finds. Only the band and the action of eighteen already-reported
  rows move.
- **It does not widen the mechanism to another family.** The entries are keyed
  `(family, repo, path)`; an entry naming another family disposes nothing here,
  and this arm disposes nothing anywhere else.
- **It does not touch `document-lifecycle`.** The rule that a ratification
  record carries `Status: ratified` is unchanged and unweakened; what changes is
  how `doc-health` REPORTS a violation nobody may repair (`design.md` D4).
- **It does not promote anything.** No file under `openspec/specs/` is edited.
- **It does not close the origin issue.** `code_surface` is non-empty, so the
  archive is a separate act on merged-plus-green realization evidence and a
  separate word, and openxFactory issue 939 is closed THERE, by a closing
  keyword written in the archive pull request and in no commit message on this
  branch.
