# Architect rulings at completion — mirror

Status: record
Lane: opsXfactory-1

**This is the Speckit-tree MIRROR of the block appended to**
`openspec/changes/add-consent-custody-rederivation-record/evidence/realization-2026-09-09.md`
(architect ruling 032-Q4: the evidence lives in BOTH trees). The packet-side
file is the one the change archives on; this copy is byte-equivalent in
substance so a reader of the feature tree needs no cross-repository hop.

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
