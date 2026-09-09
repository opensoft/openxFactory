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
| 3, 4 | The validator's internal legs, the WITHHELD third outcome and exit `3`, the extended blob walk, eighteen fixtures across three buckets (3 positive, 14 negative, 1 withheld — counted by listing), the three corpus-count surfaces — **and `tests/consent_instruments/`**, because box 3.3 asks for a TEST that pins an absence and a tick cannot precede its own evidence | `f420cd50` |
| — | Q8's three README amendments, in the `3b530009` form | `7c79f524` |
| 5 | ~~**THE CUT — `contract-v3.5`**, every release surface in ONE candidate commit, plus the cut-coupled `test_release_boundary.py` edits~~ **WITHDRAWN 2026-09-09** — `contract-v3.5` was taken by openxFactory #866 (`a37ae0cd`, tagged) on Brett Heap's ordering ruling; the cut is RE-MADE as `contract-v3.6`. See § *Cut re-made as `contract-v3.6`* below | ~~`d54d89ca`~~, remade `e9a688d3` — **both withdrawn** |
| 5 | **THE CUT — `contract-v3.6`**, every release surface in ONE candidate commit over the integration point `fee36588`, plus the cut-coupled `test_release_boundary.py` edits | THIS COMMIT (sha filed by the follow-up evidence commit) |

Integration point: `origin/main` at `587f21a0`, merged in (never rebased —
opensoft org ruleset 8981805 forbids non-fast-forward updates). **SUPERSEDED
2026-09-09: the live integration point is `fee36588`, the merge of
`origin/main@17167481`** — see § *Cut re-made as `contract-v3.6`*.

## The number

**SUPERSEDED 2026-09-09 — the live number is `contract-v3.6`; see § *Cut
re-made as `contract-v3.6`*. The paragraph below is the withdrawn record.**

`contract-v3.5` was **MEASURED FREE at the integration point on all three
surfaces** — `contracts/manifest.yaml:3`, the highest `contracts/releases/`
inventory, and the highest `contract-v*` tag. **A measurement, never a
reservation.** The CLAIM on openxFactory issue #630 row 4 is the LANE's, at cut
time, and is not made by any commit on this branch (box 5.1).

## Gates

**SUPERSEDED 2026-09-09 — these transcripts certify the WITHDRAWN candidate
`d54d89ca`, and the `release-tag-gate` reading below was later measured wrong
(exit 2, REFUSED, read from a transcript's tail rather than its header). The
live gates are in § *Cut re-made as `contract-v3.6`*.**

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

## Architect rulings at completion — 2026-09-09T18:28Z

The orchestrator reported three items to the architect seat (lane
`opsXfactory-1`, the main session) at the end of realization. Two were DECLARED
DEVIATIONS put up for ruling rather than taken silently; both are **ACCEPTED**,
and the third is confirmed as recorded rather than acted on. Recorded here so
the acceptances are part of the packet's evidence and not only of a session.

**1. Phases C, D and E ride ONE commit (`f420cd50`) — ACCEPTED.** The reason is
the invariant, not convenience: **box 3.3 asks for a TEST that pins an absence**
(*"A test pins that absence so a helpful later edit fails on the developer's
machine first"*), so `tests/consent_instruments/` IS box 3.3's evidence and its
tick cannot precede it. Splitting the phases across commits would have broken
tick-rides-its-evidence (FR-041, architect ruling 032-Q5). **The invariant
outranks the phase boundary**, and the phase boundary is a `plan.md` sequencing
aid that `tasks.md` never states as a commit rule — `tasks.md` prescribes "one
commit" only for § 2 and for the § 5 candidate. Each phase still filed its own
raw transcript (FR-042b).

**2. The cut-coupled `contracts/README.md` consent-row amendment — ACCEPTED.**
The row now reads *amended at `contract-v1.33` (1 → 2) and again at
`contract-v3.5` (2 → 3, additive)*. **No ratified task names this edit**; it is
DERIVED from T061a's measurement and declared as such. `git show --stat 807a4f47`
— the `contract-v3.4` cut — moved SIX files, `contracts/README.md` among them,
and its two lines there were REGISTRATION-STATE rows for the family that cut
published. This cut's registration state also moves, so the same slot takes the
same kind of note. **It is admitted in the same class as the cut-coupled tests
(panel F1): a declared, attributed, measured cut-coupled act — not invented
scope.**

**3. The carried findings stay RECORDED, NOT ARMED — confirmed.** The task 3.2
paraphrase defect (the delta governs; the leg is anchor-relative; no ratified
text was altered), the identical-locators `path_only` gap (owed to F.2 or a
successor; **no refusal leg added here**), and clarify A2's REPORT → REFUSAL
conversion (which needs F.2's gate, and that gate is OpsxFactory's) all stay as
written. Nothing is built, scheduled or armed by this realization.

### The full-suite baseline, stated once and plainly

`python3 -m pytest tests/ -q -m "not postgres"` at the candidate `d54d89ca`:
**1 failed, 10662 passed, 36 skipped, 338 deselected**, rc=1. Re-run at the
Phase H head: identical counts.

- The single failure is
  `tests/ideation-dashboard/test_snapshot.py::test_find_validator_locates_pinned_checkout`.
  It resolves a **pinned checkout that exists only in an aggregation workspace
  layout**, which a linked worktree is not.
- It is **PROVEN PRE-EXISTING by a baseline, not by assertion**: the same node id
  fails identically in a SEPARATE CLONE at pristine `main` **`e86eca35`**,
  carrying none of this branch's bytes.
- The second failure seen in the Phase E run — a **30-second subprocess-ceiling
  flake** on a loaded workstation
  (`test_release_mode_field_is_preserved_on_the_real_repository`) — **PASSED on
  re-run**, which is why it was baselined rather than chased.
- **ZERO failures name a consent surface**: none under
  `tests/consent_instruments/`, none touching `examples/consent-instrument/`,
  `scripts/validate-consent-instruments.py`,
  `contracts/schemas/consent-instrument.schema.yaml` or `contracts/manifest.yaml`.
- **THE `openXwallet` GITLINK MUST BE INITIALIZED, AS CI DOES IT.** Without
  `git submodule update --init openXwallet` this gate reports **96 failed and 50
  errors** that are entirely the submodule's absence —
  `tests/clearing/conftest.py` REFUSES rather than degrading to a skip, and
  `tests/trust-anchor/`, `tests/openxwallet_pin/` and
  `tests/signed_execution_chain/` read the same gitlink. CI initializes it in a
  dedicated App-token step before the suite because openXwallet is a second,
  private org repository. Anyone re-running this gate must do the same, or read
  146 findings that say nothing about the code.

## Refutation panel on `528c690c` — findings taken, 2026-09-09T20:31Z

PASS AFTER FIXES. Every gate was reproduced twice independently by the panel.
Eight findings, all prose or evidence; the code half is R7. **Two of them are
counting defects in `contracts/CHANGELOG.md`, which is a `contracts/` byte
INSIDE the certified candidate `d54d89ca` — they are recorded here and NOT
edited into it**, because remaking the candidate to fix a prose count would
invalidate every gate transcript taken against it. The candidate's `contracts/`
tree is asserted byte-identical after these edits.

### R2 — the bundle count in the v3.5 entry is short by one addition and one modification

**The entry says FOUR additions and FIFTEEN modifications. Measured at the
candidate it is FIVE and SIXTEEN:**

```
$ git diff --name-status contract-v3.4 d54d89ca -- contracts/
      5 A     16 M
```

**Cause, named exactly:** the count was taken at the INTEGRATION POINT
`9d658813`, before the cut's own two members existed. The two the entry does not
attribute are **self-referential** — `M contracts/CHANGELOG.md` (the entry
itself) and `A contracts/releases/contract-v3.5.digests.yaml` (the inventory the
entry describes). Nothing substantive is missing: no contract, no schema, no
pin, no fixture is unnamed.

**THE v3.4 PRECEDENT WAS CHECKED, AND IT DOES NOT EXCUSE THE OMISSION — IT
CONTRADICTS IT.** `contract-v3.4`'s own entry carries a table row naming exactly
these two members for itself:

> `| M contracts/CHANGELOG.md, A contracts/releases/contract-v3.4.digests.yaml | **THIS CUT** — this entry and the rebuilt inventory |`

So attributing the self-referential members is the house form, and their absence
from the v3.5 entry is a DEFECT rather than a convention. Recorded as such
rather than argued away.

**Disposition: NOT REPAIRED IN THIS CANDIDATE, and the choice is the
coordinator's.** Either the candidate is REMADE with the corrected count and
every gate re-runs against the new commit (the packet's own rule — a candidate
is remade, never patched), or the correction rides the NEXT cut's entry, which
must then also say why v3.5's numbers read low. This seat took neither on its
own authority.

### R3 — two release-surface members outside `contracts/` are unattributed

Both moved since `contract-v3.4` and neither is named in the v3.5 entry, which
scopes itself to `contracts/`:

- **`docs/contract-versioning-policy.md`** — moved by `0083a71d`, *"Move the
  release-tag zero-findings pin into a gate on the cutting pull request"*. It is
  a `NORMATIVE_DOCS` **and** a `RELEASE_SURFACE_PATHS` member, so it is inside
  the release inventory even though it is outside `contracts/`. **It moved on
  `main` before this cut reached it.**
- **`tests/intent-compliance/test_release_boundary.py`** — moved by the
  candidate `d54d89ca` ITSELF: the cut-coupled tripwire edit (T061b). An
  inventory member, and this cut is what moved it.

Same disposition as R2: recorded here, not edited into the frozen candidate. The
substantive point is already carried — the entry's additive argument measures
the intent-compliance member set directly and finds ZERO changed paths, and
`docs/contract-versioning-policy.md` is one of the three registered rows the
T060 measurement and the doc-health pair both independently found had moved.

### R1 and R8 — two further owed findings

Recorded in full beside § 7 of the packet's `tasks.md`, and summarized here:
**#3**, the `status`/`custody_rederivations` conflict the ratified scenario calls
nonconformant and nothing refuses — a NEUTRAL leg by C-7's placement test, with
the literal *"solely"* wording not decidable from the record and the
empty-`amendments` form the honest approximation; **#4**, the consent schema's
absence from the release digest inventory, a pre-existing static-membership
divergence between `release.py` and the versioning policy that predates this cut
at every bundle which carried the schema. **No leg and no inventory row was
added for either.**

### R5, R6, R7 — taken

- **R5**: the fixture count is **18** (3 positive, 14 negative, 1 withheld),
  corrected at all three prose sites that said seventeen.
- **R6**: `release-tag-gate` at the BRANCH HEAD exits 2 with *"3 first-parent
  landing(s) after the commit that declared it"*, while the candidate and the
  PR merge tree are green. Both results and the reason — the gate counts
  landings, not only tree bytes — are recorded at T081's transcript.
- **R7**: the `bucket` parametrize in `test_no_git_rederivation.py` was
  decorative (all three cases called `self_test`, which walks all three buckets).
  Each case now drives `validate_record` over ITS OWN bucket and asserts that
  bucket's own outcome, so a per-bucket regression fails its own case:
  positive 9 files / 0 errors, negative 21 / 25 errors, withheld 1 / 0 errors and
  1 withholding. The open-guard case additionally asserts that a file of its own
  bucket was actually opened, because a guard that watches nothing cannot refuse
  anything. `pytest tests/consent_instruments -q`: **34 passed**.

### R4 — the feature tree's own boxes

The T083 audit proves the tick discipline over the PACKET's 46 boxes. The
Speckit feature tree's 79 `T###` boxes were never ticked; they are ticked now
with per-phase dated evidence pointers, and T065/T066 carry NOT-OWED-HERE lines
because they mirror boxes 5.5 and 5.6.

## Cut re-made as `contract-v3.6` — recorded 2026-09-09T22:52Z

**EVERYTHING ABOVE THIS SECTION ABOUT `contract-v3.5` DESCRIBES A WITHDRAWN
CANDIDATE.** The realization itself — the schema (`f59a587d`), the validator,
corpus and tests (`f420cd50`, `0cbd022a`) and the README amendments
(`7c79f524`) — is unchanged and stands. Only the CUT is redone.

### The ordering ruling

Brett Heap, **2026-09-09T22:11Z**, selected option verbatim:

> *"#866 first, I re-cut as v3.6 (Recommended)"*

openxFactory PR **#866** (lane `provenance-autonomous-merge`, the
`adopt-codexfactory-repository-identity` cut) landed on `main` as **`a37ae0cd`**
at **21:47:48Z**, and Brett Heap published the annotated tag **`contract-v3.5`**
(`6c602f3c` → `a37ae0cd`). The ruling and the RELEASE of this lane's own
`contract-v3.5` claim are recorded on openxFactory issue **#630**, comments
`5609050869` (claim) and `5609442856` (release + correction). The row-4 claim for
the new number is
<https://github.com/opensoft/openxFactory/issues/630#issuecomment-5609660878>,
posted 2026-09-09T22:34:39Z at the integration point.

### The two withdrawn candidates, and the three defects an audit found

`d54d89ca` (the first cut) and `e9a688d3` (its forward-only remake) both declared
`contract-v3.5`. Neither was ever published — no merge to `main`, no tag — and
both are WITHDRAWN. Beyond the number being taken, an audit of `e9a688d3` found
three defects, each of which is answered at the new candidate rather than argued
away:

1. **The release-tag gate was RED, and the earlier readings were misreads.**
   `scripts/validate-release-tag-gate.py` exited **2, REFUSED**:
   *"contract-v3.5 is declared and has no published annotated tag more than 5
   first-parent landings after the commit that declared it — under the versioning
   policy it is NOT PUBLISHED, and its presence in the manifest is not a
   release"*. The DECLARING commit was `d54d89ca`, by then six to seven
   first-parent landings back. The readings that had called the gate green came
   from a transcript whose header looks clean while its exit code sits at the
   tail. Raw: `AUDIT/gate-f04f8f4d.txt`. **At the new candidate the declaring
   distance is ZERO**, because the candidate is the branch tip.
2. **Two inventory members outside `contracts/` were unattributed.** The entry
   said *"Two inventory members live outside `contracts/`"* while FOUR had moved;
   `docs/terminology-and-repo-topology.md` and
   `docs/xfactory-domain-factory-model.md` (both moved by `44fc8063`) were named
   nowhere. Raw: `AUDIT/invdiff-e9a688d3.txt`, `AUDIT/drift.txt`. **At the new
   candidate the attribution is taken from an inventory diff over all 283
   members**, and all three `NORMATIVE_DOCS` are byte-unchanged because
   `contract-v3.5` itself re-baselined them.
3. **The candidate was not atomic.** `e9a688d3` carried only
   `contracts/CHANGELOG.md` and the rebuilt inventory while
   `contracts/manifest.yaml`, `contracts/README.md` and the cut-coupled tripwire
   stayed behind at `d54d89ca` — not the single atomic candidate
   `docs/contract-versioning-policy.md` § *Bundle Realization Order* step 2 and
   this packet's **FR-034a** require. **At the new candidate every release
   surface moves in ONE commit.**

### The integration point

**`fee36588`** — a MERGE of `origin/main` at **`17167481`** INTO
`033-add-consent-custody-rederivation-record`, never a rebase (opensoft org
ruleset **8981805** forbids non-fast-forward updates, so a candidate only ever
advances forward). Four conflicts, each resolved toward the published record:

| file | resolution |
| --- | --- |
| `contracts/CHANGELOG.md` | TAKE MAIN entirely — main carries #866's `## contract-v3.5` entry; this branch's unpublished v3.5 entry survives nowhere |
| `contracts/releases/contract-v3.5.digests.yaml` | TAKE MAIN (add/add) — #866's is the inventory the published tag peels to |
| `tests/intent-compliance/test_release_boundary.py` | TAKE MAIN — #866's `FEATURE_SUCCESSOR_9` and its boundary paragraph stand as published |
| `contracts/manifest.yaml` | TAKE MAIN, then re-apply ONE key: the `consent-instrument` row's `sha256` `13b0fe46…` → `2b834492…`, so no commit on this branch carries a stale digest. `contract_bundle_version` and the consumption-rule paragraph were left to the candidate |

`contracts/README.md` auto-merged and kept both sides. Measured at `fee36588`:
`validate-manifest-digests.py` rc=0, *"189 per-file digest(s) verify"*;
`verify-commit --commit fee36588` rc=1 with EXACTLY TWO findings,
`contracts/README.md` and `contracts/manifest.yaml`, both EDITORIAL members —
the bounded state § *What a red `verify-commit` at HEAD means* describes, whose
*"remedy is a release cut, never a hand-edit"*, and which this candidate is.

### The number, re-measured

`contract-v3.5` on all three surfaces and `contract-v3.6` ABSENT from all three,
with no `Unreleased` block pending. Transcript:
`specs/.../evidence/phaseI-recut-v3.6-number-measurement.txt`.

### The candidate

THIS COMMIT — its sha is filed by the follow-up evidence commit. ONE commit, its
own declaring commit, carrying `contracts/manifest.yaml`,
`contracts/CHANGELOG.md`, `contracts/releases/contract-v3.6.digests.yaml` (BUILT
by the tool, 283 entries), `contracts/README.md`,
`tests/intent-compliance/test_release_boundary.py` and this bookkeeping.

### The inventory diff — the whole 283-member surface

283 entries at both ends, **ZERO added, ZERO removed**, no `git_mode` and no
non-digest field changed, **FOUR digests re-baselined**:

| member | `contract-v3.5` | `contract-v3.6` | outside `contracts/` | attributed to |
| --- | --- | --- | --- | --- |
| `contracts/manifest.yaml` | `93564e191379…` | `db09218b28b9…` | no | `f59a587d`, `fee36588`, **THIS CUT** |
| `contracts/README.md` | `f3a959fa223d…` | `a8f1ac59abf8…` | no | `f420cd50`, `d54d89ca`, **THIS CUT** |
| `contracts/CHANGELOG.md` | `a2b65ff30b9c…` | `d3e4ddbfba4c…` | no | **THIS CUT** |
| `tests/intent-compliance/test_release_boundary.py` | `a235e1c55947…` | `3ad36da5ca35…` | **YES** | **THIS CUT** |

**Ninety-one inventory members live outside `contracts/`; exactly ONE moves
here**, the cut-coupled tripwire. Every moved member is named by exact path in
the `## contract-v3.6` entry: zero unattributed. Transcript:
`specs/.../evidence/phaseI-recut-v3.6-inventory-diff.txt`.

### Gates that ride this commit — command, rc, summary line

| gate | rc | summary |
| --- | --- | --- |
| `validate-manifest-digests.py` | 0 | `OK contracts/manifest.yaml: 189 per-file digest(s) verify` |
| `validate-consent-instruments.py --strict` | 0 | `validate-consent-instruments: 0 error(s), 0 warning(s), 0 withheld` (9 valid / 21 negative / 1 withheld / 2 purpose probes) |
| `validate-openspec-cli-pin.py --change add-consent-custody-rederivation-record --strict` | 0 | `Totals: 1 passed, 0 failed (1 items)` |
| `validate-openspec-cli-pin.py --all --strict` | 0 | `every target validated --strict with 0 UNDISPOSITIONED failures … 2 finding(s) are ACCEPTED EXCEPTIONS` |
| `validate-sequenced-after.py .` | 0 | `sequenced_after validation passed (39 active changes, 9 declaring the field).` |
| `validate-sequenced-after.py . --ledger-diff` | 0 | `per-change sweep ledger consistent with the corpus (190 rows).` |
| `validate-scope-globs.py` | 0 | `scope_globs validation passed (all active changes conform).` |
| `pytest tests/consent_instruments tests/intent-compliance/test_release_boundary.py -q` | 0 | `47 passed` |
| `pytest tests/clearing/test_clearing_manifest_rows.py -q` | 0 | `20 passed` — T061c re-measured: NO EDIT owed |
| `validate-contract-release.py build --tag contract-v3.6` | 0 | `release build: pass … entries=283` |

**The commit-addressed gates cannot ride this commit and are not claimed to.**
`validate-release-tag-gate.py --head <candidate>`,
`verify-commit --commit <candidate>` and the full suite address the candidate BY
SHA; they run against the EXACT UNCHANGED candidate immediately after it is
formed, and their transcripts plus the candidate's sha are filed by a FOLLOW-UP
EVIDENCE-ONLY commit that touches no release surface.

### Still NOT DONE, and still owed elsewhere

Boxes **5.5** (the lane's landing) and **5.6** (the operator's annotated tag at
the LANDED merge commit) stay UNTICKED. `TAG OWED` is the expected state at this
candidate, not a finding. Everything in § *THREE THINGS ARE RECORDED HERE AND
DELIBERATELY NOT DONE* above is unchanged by the re-cut.
