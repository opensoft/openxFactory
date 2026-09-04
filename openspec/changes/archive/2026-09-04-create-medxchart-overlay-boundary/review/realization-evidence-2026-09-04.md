# Realization evidence: create-medxchart-overlay-boundary § 5, 2026-09-04

Status: record
Kind: report
Captured: 2026-09-04, in lane `openxfactory-max001` (session `5e783e4d`), on
branch `change/archive-create-medxchart-overlay-boundary`, cut from `main` at
`48dc9b67c87377cdad31d2840666c7028a212cf7`. **This record is CAPTURED AT MERGE
of the archive pull request that carries it**, which is the same rule
`review/ratification-2026-09-03.md` states of itself; after that merge it is
written once and never edited.

**Why this file exists.** `tasks.md` 5.4 says: *"Record the ruleset id and one
green required run in this change's `review/` directory as realization evidence,
then and only then open the archive gate."* This is that record, and it is what
opens the gate. The ratification record's § 5 says the same thing from the other
side — *"5.4 records the ruleset id and one green required run as realization
evidence and is what opens the archive gate"* — and `release-realization`'s
realization archive gate requires a change with a non-empty `code_surface` to
archive only on MERGED code plus GREEN evidence, measured after landing and
never assumed.

**What is asserted here, and on whose reading.** Every id, sha and timestamp
below was verified by the convening coordinator through the GitHub API, and
re-read a second time by this lane through `gh api` while this file was being
written. Where the two readings differ from the summary this lane was handed,
the API is authoritative and the difference is stated rather than smoothed: the
ruleset ids guessed in session before the console act (`21987654` / `21987655`)
were **wrong**, and the ids recorded here are the ones the API returns.

---

## 1. The ruling this discharges

Three words of Brett Heap's, in session on 2026-09-04, in the order they were
given:

1. **"do the pin validators"** — the authority to build § 5.1 and § 5.2 in
   `opensoft/MedxChart` and in `opensoft/MedxPractice`.
2. **"merge both when aligned and green"** — the authority to land the two
   descendant pull requests once their validators agreed in shape and their
   checks were green.
3. **"rulesets created … do 5.4 and archive both"** — the operator's report
   that § 5.3 (his own console act) was performed, and the authority for this
   record and for the archive act that follows it.

**5.3 IS AN OPERATOR ACT AND NO AGENT PERFORMED IT.** `tasks.md` 5.3 is marked
`[OPERATOR]` and says in its own text that "an agent-reported 'ruleset created'
without the console act is not evidence". The console act was Brett's; what this
lane did was read the result back through the API, which is why the ruleset's
id, shape and creation time are quoted below from `gh api` output rather than
from anyone's report of them.

## 2. § 5.1 — the validator, and that it is the thing that refuses

`opensoft/MedxChart` **PR #1**, *"Add the descendant pin validator and its
pin-validation check (create-medxchart-overlay-boundary § 5.1–5.2)"*, merged
**`8bc39a8ce8bb4e9cf54484e400644114a41b852a`** at **2026-09-04T13:05:59Z** into
`main`.

Five files, all of them in that one landing:

| File | Status | Lines |
| --- | --- | --- |
| `tests/validate_pin.py` | added | 384 |
| `tests/test_validate_pin.py` | added | 213 |
| `.github/workflows/pin-validation.yml` | added | 74 |
| `.gitignore` | added | 15 |
| `README.md` | modified | +8 (a Validation section) |

**`.gitignore` is a fifth file and is named rather than folded into "the
validator and its workflow"** — it is ordinary Python/`__pycache__` hygiene that
the self-test run would otherwise leave in the tree, and a checkout the
validator's own check 4 would then report as DIRTY.

**The validator refuses on exactly the four conditions 5.1 names**, fail-closed,
offline, each with its own refusal token so a red run says which condition
failed:

1. `pin-gitlink-disagrees` / `pin-gitlink-absent` — the recorded `openChart`
   gitlink and `contracts/openchart-pin.yaml`'s `pin.revision` name different
   commits, or either is absent.
2. `pin-manifest-absent` / `pin-manifest-unreadable` — the manifest is missing,
   does not parse as YAML, or carries no `pin:` mapping.
3. `pin-manifest-shape` / `pin-revision-invalid` — top-level `schema_version` is
   not `1` or `kind` is not `medxchart_openchart_pin`; or the `pin:` mapping is
   missing any of `repository`, `remote`, `revision`, `submodule_path`,
   `source_path`, `relationship: pinned_upstream_composition`; or
   `pin.revision` is not a well-formed 40-hex commit id.
4. `pin-checkout-drift` — the CHECKED-OUT `openChart/` is not at the recorded
   revision, or is dirty.

**Check 4 is the one 5.1 called out and the one a declaration-only pin misses.**
Checks 1–3 compare declarations to each other; only check 4 compares a
declaration to the bytes that will execute, which is what catches a fork
running at another commit while all three declarations still agree.

**The validator's module docstring names its two deviations from LedgerxWallet's
check set rather than leaving them to be discovered**, and both follow from
5.1's own wording: LedgerxWallet's `pin-not-a-commit` check keys on
`revision_kind` and `contract_bundle_tag` manifest fields that
`contracts/openchart-pin.yaml` does not carry, so the format of `pin.revision`
is checked instead; and LedgerxWallet's `pin-split-commit` (HEAD against its
first parent) is not among the four conditions 5.1 enumerates and is not
implemented.

**SEVEN self-tests** ship beside it in `tests/test_validate_pin.py` and run
BEFORE the validator in CI: `test_clean_tree_passes`,
`test_gitlink_and_pin_disagree`, `test_manifest_absent`,
`test_manifest_shape_wrong_kind`, `test_checkout_drift`,
`test_uninitialized_submodule_refuses`, `test_dirty_checkout_refuses` — one per
refusal category plus the passing case and the two states (uninitialized,
dirty) that a gate defaulting to a pass would wave through.

**THE PIN IDENTITY THE GATE NOW ENFORCES IS THE ONE THIS PACKET VERIFIED BY
HAND ON 2026-08-23 AND RE-VERIFIED ON 2026-09-03**: MedxChart's nested
`openChart` gitlink and `contracts/openchart-pin.yaml`'s `pin.revision` both
read **`d2376a31dbafa413d8e5ba032f4a2620a75d578e`**. What changed today is not
the value but its standing: `tasks.md` 4.1's appended note said "**Nothing in
the repository ENFORCES that agreement today** — that is § 5's whole subject",
and as of `8bc39a8c` something does.

## 3. § 5.2 — the workflow, and the check name it must surface

`.github/workflows/pin-validation.yml`, `name: pin-validation`, triggering on
`pull_request` against `main` **and** on `push` to `main` — both triggers, which
is what 5.2 asks for and one more than LedgerxWallet's copy carries. The job is
`pin-validation` and carries **no display name on purpose**, so the status check
surfaces as exactly the literal token `pin-validation` that § 5.3's ruleset
pins; a display name would silently de-advise the gate.

There is **no `paths:` filter**, deliberately: a required context that does not
run on some pull requests never reports on them, and a required context that
never reports blocks the merge forever.

`openChart` is PUBLIC, so the workflow rewrites `git@github.com:` to
`https://github.com/` and initializes the nested checkout anonymously — no App
token is minted and no `secrets:` are read.

## 4. § 5.3 — THE RULESET, read back from the API

**Ruleset `22272824`, "MedxChart pin-gate"**, on `opensoft/MedxChart`. Created
by Brett Heap's console act at **2026-09-04T09:17:59.179-04:00
(= 13:17:59Z)**; last updated `2026-09-04T09:24:15.912-04:00 (= 13:24:15Z)`.

```console
$ gh api repos/opensoft/MedxChart/rulesets/22272824
{
  "id": 22272824,
  "name": "MedxChart pin-gate",
  "target": "branch",
  "source_type": "Repository",
  "source": "opensoft/MedxChart",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"},
    {"type": "required_status_checks", "parameters": {
      "strict_required_status_checks_policy": false,
      "do_not_enforce_on_create": false,
      "required_status_checks": [{"context": "pin-validation", "integration_id": 15368}]}}
  ],
  "bypass_actors": [
    {"actor_id": null, "actor_type": "OrganizationAdmin", "bypass_mode": "always"},
    {"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}
  ],
  "created_at": "2026-09-04T09:17:59.179-04:00",
  "updated_at": "2026-09-04T09:24:15.912-04:00"
}
```

It is **REPOSITORY-sourced** (not organization-sourced), **`enforcement:
active`**, scoped to `~DEFAULT_BRANCH`, and it makes **`pin-validation` a
REQUIRED status check**. `strict_required_status_checks_policy` is `false`, so
a branch is not forced up to date with `main` before merging — which matches
the precedent and is the setting a two-file pin gate wants.

### 4.1 THE DEVIATION FROM THE LEDGERXWALLET PRECEDENT, RECORDED AS OBSERVED AND NOT AS A DEFECT

`tasks.md` 5.3 says the ruleset is created "on the shape of ruleset
`21701436`". The shapes are close but **not identical**, and the differences are
stated here rather than glossed, because a later reader comparing the two will
find them and should not have to decide whether they were noticed:

| | LedgerxWallet `21701436` | MedxChart `22272824` |
| --- | --- | --- |
| name | LedgerxWallet pin-gate (require pin-validation) | MedxChart pin-gate |
| source_type / target / enforcement | Repository / branch / active | **same** |
| ref_name include | `~DEFAULT_BRANCH` | **same** |
| required check | `pin-validation`, strict `false` | **same** |
| other rules | *(none)* | `deletion`, `non_fast_forward` |
| bypass actors | `OrganizationAdmin: always` | `OrganizationAdmin: always`, **`RepositoryRole` (id 5): always** |

**Two additions, in opposite directions, and neither is failure of the gate this
group commissions.** The `deletion` and `non_fast_forward` rules make MedxChart's
default branch STRICTLY MORE protected than LedgerxWallet's. The extra bypass
actor — `RepositoryRole` id `5`, the repository admin role — makes the required
check bypassable by ONE MORE class of actor than the precedent allows. That
second one is the one worth writing down: it does not weaken what the check
computes, and it does not weaken what a non-admin sees, but it does mean the
gate on MedxChart is escapable by a repository admin where LedgerxWallet's is
escapable only by an organization admin.

**Recorded as an OBSERVED DEVIATION, not a defect, and not repaired here.** The
ruleset is an operator artifact created by a console act; an agent editing it to
match a precedent would be performing exactly the act 5.3 reserves. What this
record owes is an accurate reading, and this is it. `opensoft/MedxPractice`'s
ruleset `22273105` carries the identical shape including both deviations, so
this is one operator pattern applied twice rather than a one-off slip in either
repository.

## 5. § 5.4 — ONE GREEN RUN **UNDER** THE RULESET

The word that does the work in 5.4 is **"required"**: a green run is only
evidence of the gate if the gate was in force when it ran.

```console
$ gh api repos/opensoft/MedxChart/actions/runs/33876197016
{
  "id": 33876197016,
  "name": "pin-validation",
  "head_sha": "8bc39a8ce8bb4e9cf54484e400644114a41b852a",
  "event": "push",
  "run_attempt": 2,
  "created_at": "2026-09-04T13:06:02Z",
  "run_started_at": "2026-09-04T13:25:34Z",
  "status": "completed",
  "conclusion": "success",
  "updated_at": "2026-09-04T13:25:47Z"
}
```

**Run `33876197016`, head `8bc39a8c`, conclusion `success`.** The timeline is
the point:

- `13:05:59Z` — PR #1 merges; `8bc39a8c` lands on `main`.
- `13:06:02Z` — the `push` run is created. **This first attempt PREDATES the
  ruleset** and is therefore green under no required regime at all.
- `13:17:59Z` — Brett creates ruleset `22272824`; `pin-validation` becomes a
  required status check.
- `13:25:34Z` — **`run_attempt: 2`**, a deliberate re-run of the same workflow
  at the same head, now under the ruleset.
- `13:25:47Z` — completed, **`success`**.

**IT IS THE RE-RUN, NOT THE FIRST ATTEMPT, THAT IS THE EVIDENCE 5.4 ASKS FOR**,
and the distinction is made explicitly because the run id is the same in both
cases and a reader who only saw the id could not tell them apart. `run_attempt`
is `2` and `run_started_at` is twelve minutes after `created_at`; those two
fields are what make the claim checkable.

## 6. § 5.5 — discharged by the sibling's ratified text, not by a decision taken here

5.5 asks this packet to "decide … whether `opensoft/MedxPractice` takes the same
validator". **It has already been decided, in ratified text, by the packet that
owns MedxPractice.** `create-medxpractice-overlay-boundary`'s `tasks.md` § 5
carries a titled paragraph — **"THIS GROUP ANSWERS THE SIBLING'S OPEN 5.5"** —
whose answer is *"YES, and it is recorded here because this is the packet that
owns MedxPractice"*, on the ground that the two descendants carry the identical
two-pin shape and "one validator shape covers one pin shape and a second shape
would be two answers to one question". That paragraph closes by naming exactly
this act:

> **This paragraph is the answer; the sibling's 5.5 checkbox cannot be ticked
> from this pull request and is left for the sibling's own pass to tick with a
> pointer here.**

This is that pass, and 5.5 is ticked with that pointer. The decision is
**confirmed by what was built**: `opensoft/MedxPractice` PR #1 merged
`f7fd8364e033df4a6c5b0f84080b7bde5d156fb4` at 2026-09-04T13:05:10Z carrying the
same five files at the same sizes — `tests/validate_pin.py` (384 lines),
`tests/test_validate_pin.py` (213), `.gitignore` (15), `README.md` (+8) and a
`.github/workflows/pin-validation.yml` differing only in its two-line comment
about the sibling — a literal-only diff over the product name and the four
values that follow from it. Its pin identity is
`9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d`, its ruleset is `22273105`, and its
green run under that ruleset is `33876124444`. **Those MedxPractice facts are
recorded HERE only as confirmation that one answer covered one shape; the
evidence that opens THAT packet's archive gate is its own § 5.4 record, written
in its own `review/` directory by its own pull request.**

## 7. What this evidence does NOT establish

- **It does not make MedxChart a citable precedent for creating descendants.**
  The empty-boundary position (`review/ratification-2026-09-03.md` § 4,
  `tasks.md` § 6) is untouched: a validator over a pin does not add a profile
  artifact, and MedxChart's tracked tree is still composition metadata plus,
  now, its own gate.
- **It does not move a contract byte.** No `contracts/` file, schema, manifest
  row, digest or release tag moves in the descendants or here; no bundle is cut
  and no version is owed.
- **It does not close openxFactory issue #318**, which
  `review/ratification-2026-09-03.md` § 2 records as open and unclaimed and
  which this packet's history raised without settling.
- **It does not re-open anything ratified on 2026-09-03.** The ratified baseline
  is unchanged; `.openspec.yaml` is untouched, as
  `release-realization`'s origin-retention rule requires the archive gate to
  find it.
