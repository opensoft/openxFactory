# Realization evidence: create-medxpractice-overlay-boundary § 5, 2026-09-04

Status: record
Kind: report
Captured: 2026-09-04, in lane `openxfactory-max001` (session `5e783e4d`), on
branch `change/archive-create-medxpractice-overlay-boundary`, cut from `main` at
`bc1bd4ee2221ea91d1011778c8ffbf539ba5b7e6` — the merge of openxFactory PR #654,
which archived the SIBLING `create-medxchart-overlay-boundary`. **This record is
CAPTURED AT MERGE of the archive pull request that carries it**; after that
merge it is written once and never edited.

**Why this file exists.** `tasks.md` 5.4 says: *"Record the ruleset id and one
green required run in this change's `review/` directory as realization evidence,
then and only then open the archive gate."* This is that record. Under
`release-realization` a change with a non-empty `code_surface` archives only on
MERGED code plus GREEN evidence, measured after landing and never assumed.

**What is asserted here, and on whose reading.** Every id, sha and timestamp
below was verified by the convening coordinator through the GitHub API and
re-read by this lane through `gh api` while this file was written. The ruleset
ids guessed in session before the console act (`21987654` / `21987655`) were
**wrong**; the ids recorded here are the ones the API returns.

---

## 1. The ruling this discharges

Brett Heap, in session on 2026-09-04, in order: **"do the pin validators"** →
**"merge both when aligned and green"** → **"rulesets created … do 5.4 and
archive both"** → **"land it and do medxpractice"**. The last of those is the
authority for this packet's archive, given after the sibling landed.

**5.3 IS AN OPERATOR ACT AND NO AGENT PERFORMED IT.** `tasks.md` 5.3 is marked
`[OPERATOR]` and says in its own text that "an agent-reported 'ruleset created'
without the console act is not evidence". The console act was Brett's; this lane
read the result back through the API.

## 2. § 5.1 — the validator

`opensoft/MedxPractice` **PR #1**, *"Add the descendant pin validator and its
pin-validation check (create-medxpractice-overlay-boundary § 5.1–5.2)"*, merged
**`f7fd8364e033df4a6c5b0f84080b7bde5d156fb4`** at **2026-09-04T13:05:10Z** into
`main` — **forty-nine seconds BEFORE its MedxChart sibling**, the two having
been landed together on *"merge both when aligned and green"*.

| File | Status | Lines |
| --- | --- | --- |
| `tests/validate_pin.py` | added | 384 |
| `tests/test_validate_pin.py` | added | 213 |
| `.github/workflows/pin-validation.yml` | added | 72 |
| `.gitignore` | added | 15 |
| `README.md` | modified | +8 (a Validation section) |

**The validator refuses on exactly the four conditions 5.1 names**, fail-closed
and offline, with seven distinct refusal tokens so a red run says which
condition failed: `pin-gitlink-disagrees` / `pin-gitlink-absent`;
`pin-manifest-absent` / `pin-manifest-unreadable`; `pin-manifest-shape` /
`pin-revision-invalid`; `pin-checkout-drift`.

**5.1 asks for one thing the MedxChart task did not, and it is present.** This
packet's 5.1 spells out that the manifest is **NESTED** — "two declaration
fields above and six pin fields under `pin:`, and a validator that reads them
flat passes a file that does not exist". The shape check reads top-level
`schema_version`/`kind` (`1` / `medxpractice_openpractice_pin`) AND requires the
`pin:` mapping to carry every one of `repository`, `remote`, `revision`,
`submodule_path`, `source_path` and `relationship: pinned_upstream_composition`.

**SEVEN self-tests** run BEFORE the validator in CI: `test_clean_tree_passes`,
`test_gitlink_and_pin_disagree`, `test_manifest_absent`,
`test_manifest_shape_wrong_kind`, `test_checkout_drift`,
`test_uninitialized_submodule_refuses`, `test_dirty_checkout_refuses`.

### 2.1 "One validator shape for one pin shape" — MEASURED, not asserted

The sibling's `tasks.md` 5.5 answered YES to whether MedxPractice takes the same
validator, on the ground that one shape covers one pin shape. **That claim is
checkable and was checked here rather than repeated.** Normalizing MedxChart's
`tests/validate_pin.py` through the product vocabulary
(`openChart`→`openPractice`, `MedxChart`→`MedxPractice`, and the same in lower
case) and diffing against MedxPractice's leaves **three lines**, and all three
are the uppercase banner string (`MEDXCHART PIN` → `MEDXPRACTICE PIN`) the
substitution did not cover. The same normalization over
`tests/test_validate_pin.py` leaves **one** line, the same banner inside an
assertion. **The two validators are literal-only variants of one file** — one
answer, one shape, confirmed by comparison rather than by report.

**THE PIN IDENTITY THE GATE NOW ENFORCES** is
**`9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d`**, declared twice — the nested
`openPractice` gitlink and `contracts/openpractice-pin.yaml`'s `pin.revision`.

## 3. § 5.2 — the workflow

`.github/workflows/pin-validation.yml`, `name: pin-validation`, on
`pull_request` against `main` **and** `push` to `main` — both triggers 5.2 asks
for. The job carries **no display name**, so the status check surfaces as
exactly the literal `pin-validation` that § 5.3's ruleset pins, and there is
**no `paths:` filter**, because a required context that does not run on some
pull requests never reports on them and blocks the merge forever.

It is **two lines shorter than MedxChart's** (72 vs 74) for one reason, stated
in its own header: MedxChart's copy carries a two-line note about discharging
ITS 5.5 (the sibling-validator decision), which has no analogue here.

## 4. § 5.3 — THE RULESET, read back from the API

**Ruleset `22273105`, "MedxPractice pin-gate"**, on `opensoft/MedxPractice`,
created by Brett Heap's console act at **2026-09-04T09:23:13.758-04:00
(= 13:23:13Z)**.

```console
$ gh api repos/opensoft/MedxPractice/rulesets/22273105
{
  "id": 22273105,
  "name": "MedxPractice pin-gate",
  "target": "branch",
  "source_type": "Repository",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"]}},
  "rules": ["deletion", "non_fast_forward", "required_status_checks"],
  "required_status_checks": [{"context": "pin-validation"}],
  "strict_required_status_checks_policy": false,
  "bypass_actors": [
    {"actor_type": "OrganizationAdmin", "bypass_mode": "always"},
    {"actor_type": "RepositoryRole", "bypass_mode": "always"}
  ],
  "created_at": "2026-09-04T09:23:13.758-04:00"
}
```

**It made `pin-validation` a REQUIRED status check on the default branch of a
repository that, when this packet was ratified, had ZERO workflows and no
repository-level ruleset at all** — `tasks.md` § 5 recorded that measurement on
2026-09-03 (`{"total_count":0,"workflows":[]}`, and only two ORGANIZATION-sourced
rulesets, neither requiring a status check). Both halves of that gap are now
closed, and 5.3's own note that this would be "a repository-level addition and
not an edit of either" organization ruleset is borne out: `source_type` is
`Repository`.

### 4.1 THE SAME OBSERVED DEVIATION AS THE SIBLING, REPORTED AND NOT REPAIRED

`tasks.md` 5.3 asks for a ruleset "on the shape of ruleset `21701436`"
(LedgerxWallet). The shapes differ in two directions, identically to
MedxChart's `22272824`:

| | LedgerxWallet `21701436` | MedxPractice `22273105` |
| --- | --- | --- |
| source / target / enforcement | Repository / branch / active | same |
| ref_name include | `~DEFAULT_BRANCH` | same |
| required check | `pin-validation`, strict `false` | same |
| other rules | *(none)* | `deletion`, `non_fast_forward` |
| bypass actors | `OrganizationAdmin: always` | `OrganizationAdmin: always`, **`RepositoryRole`: always** |

The extra rules make the branch **strictly more protected**; the extra bypass
actor makes the required check escapable by **one more class of actor**
(repository admin) than the precedent allows. **Recorded as an OBSERVED
DEVIATION, not a defect, and not repaired** — editing an operator's ruleset is
the act 5.3 reserves to the console. **That both descendants carry the identical
deviation is itself the finding**: this is one operator pattern applied twice,
not a slip in either repository.

## 5. § 5.4 — ONE GREEN RUN **UNDER** THE RULESET

```console
$ gh api repos/opensoft/MedxPractice/actions/runs/33876124444
{
  "id": 33876124444,
  "name": "pin-validation",
  "head_sha": "f7fd8364e033df4a6c5b0f84080b7bde5d156fb4",
  "event": "push",
  "run_attempt": 2,
  "created_at": "2026-09-04T13:05:15Z",
  "run_started_at": "2026-09-04T13:25:37Z",
  "status": "completed",
  "conclusion": "success",
  "updated_at": "2026-09-04T13:25:59Z"
}
```

**Run `33876124444`, head `f7fd8364`, conclusion `success`.** The timeline is
what makes it evidence:

- `13:05:10Z` — PR #1 merges; `f7fd8364` lands on `main`.
- `13:05:15Z` — the `push` run is created. **This first attempt PREDATES the
  ruleset** and is green under no required regime at all.
- `13:23:13Z` — Brett creates ruleset `22273105`; `pin-validation` becomes required.
- `13:25:37Z` — **`run_attempt: 2`**, a deliberate re-run at the same head, now
  under the ruleset.
- `13:25:59Z` — completed, **`success`**.

**IT IS THE RE-RUN, NOT THE FIRST ATTEMPT, THAT DISCHARGES 5.4.** Both attempts
share one run id, so `run_attempt` and the twenty-minute gap between
`created_at` and `run_started_at` are what make the claim checkable.

## 6. § 5.5 — NOT DISCHARGED, AND SAID SO PLAINLY

**5.5 IS THE ONE ITEM OF THIS GROUP THAT REMAINS OPEN.** It asks that, while the
MedxPractice tree was open, the known limitation `design.md` records be closed:
MedxPractice's own `.gitmodules` names the PUBLIC `opensoft/openPractice` over
`git@`, so an anonymous `git clone --recursive` cannot initialize the nested
checkout even though that upstream would clone over HTTPS without credentials.

**It was not done, and PR #1 did not do it.** Read back at the merge commit:

```console
$ gh api "repos/opensoft/MedxPractice/contents/.gitmodules?ref=f7fd8364…"
[submodule "openPractice"]
	path = openPractice
	url = git@github.com:opensoft/openPractice.git
```

**Nor was it silently discharged by the workflow.** `pin-validation.yml` sets
`git config --global url."https://github.com/".insteadOf "git@github.com:"`
before initializing the submodule, which makes CI's clone work — and its own
header names that rewrite as the workaround for "the open item blocking a truly
anonymous clone that `create-medxpractice-overlay-boundary` tasks.md 5.5 already
names". The workflow *routes around* 5.5; it does not close it. A human running
`git clone --recursive` anonymously still cannot initialize `openPractice/`.

**Why this lane did not simply do it.** The fix is a commit in
`opensoft/MedxPractice` that would move that entry to an `https://` URL — and
`design.md` deliberately declined it, on a stated ground: the `git@` form
"matches every sibling submodule entry in the aggregation, which is what makes
one convention rather than two", and the cost of the limitation is "real but
small" because MedxPractice is itself PRIVATE, so every clone of it is already
authenticated. That reasoning is part of what was ratified on 2026-09-03.
Reversing it is an owner's call, not a lane's, and the aggregation has already
paid once for changing a submodule URL form on an agent's judgment: the relative
`../MedxChart` / `../MedxPractice` experiment killed every xFactory nightly from
2026-08-24 until `386e7ee2` normalized both back.

**5.5 does not gate this archive, and its own text says so** — *"This is a `[ ]`
because it is a commit in another repository, not because it gates anything — it
does NOT gate the archive, which 5.4 alone opens."* How the box is disposed of
at archive is recorded in `tasks.md` and in this pull request, not decided here.

## 7. The sibling's delta moved, and the ratified text was NOT edited

This packet's **R3** — *"MedxPractice is aggregated at the cited placement and
named by MedxFactory"* — cites the amendment it relies on **by two paths**, and
one of them has moved:

1. **The promoted requirement**, `openspec/specs/domain-descendant-boundary/spec.md:76-85`.
   **STILL CORRECT.** PR #654 promoted the amendment into exactly that file, and
   *"A descendant is placed at a ratified placement"* begins at line 76 of `main`
   at `bc1bd4ee`, carrying the RATIFIED 2026-09-03 `xFactories/` half and naming
   `xFactories/MedxPractice` (gitlink `d8d73195…`) among its two realized
   placements. This is the citation that carries the authority, and it resolves.
2. **The sibling's delta file**, cited as
   `openspec/changes/create-medxchart-overlay-boundary/specs/domain-descendant-boundary/spec.md`.
   **HISTORICAL SINCE `bc1bd4ee`.** That change archived on 2026-09-04, so the
   file now lives at
   **`openspec/changes/archive/2026-09-04-create-medxchart-overlay-boundary/specs/domain-descendant-boundary/spec.md`**.

**THE REQUIREMENT TEXT IS LEFT EXACTLY AS RATIFIED, BY DESIGN AND ON THE
OWNER'S RULING.** R3 was ratified on 2026-09-03 and promotes verbatim; an
archive act is not the place to rewrite ratified requirement text, and the
citation is not broken in the sense that matters — the rule's home is the
promoted spec, which the same sentence names first and which resolves today.
What moved is a pointer to the *delta that made* the amendment, and a delta
travelling into `openspec/changes/archive/<date>-<id>/` on archive is the
ordinary lifecycle of every delta in this corpus, not a defect in the text that
cites it. **The path above is the redirection**, recorded here so a reader who
follows the ratified citation and finds nothing has one place to learn where it
went.

## 8. What this evidence does NOT establish

- **It does not make MedxPractice a citable precedent for creating
  descendants.** The empty-boundary position (`tasks.md` § 6.1) is untouched: a
  validator over a pin adds no profile artifact, and MedxPractice's tracked tree
  is still composition metadata plus, now, its own gate.
- **It does not move a contract byte.** No `contracts/` file, schema, manifest
  row, digest or release tag moves; no bundle is cut and no version is owed.
- **It does not re-open anything ratified on 2026-09-03**, and `.openspec.yaml`
  is untouched, as `release-realization`'s origin-retention rule requires the
  archive gate to find it.
- **It does not close § 5.5**, which § 6 above reports as open.
