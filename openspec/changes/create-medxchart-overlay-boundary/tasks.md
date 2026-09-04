## 1. Preflight and governance

- [x] 1.1 Confirm the current openChart commit, origin, destination absence,
  and the unrelated dirty/staged state of the shared xFactory and MedxFactory
  checkouts.
  - *2026-09-03 — what the evidence is, appended at ratification and not
    substituting for the original run.* The commit half is RE-VERIFIED and
    reproduced in `review/verification-2026-09-03.md`: MedxChart's nested
    `openChart` gitlink, `contracts/openchart-pin.yaml`'s `pin.revision`, and
    each other all read `d2376a31dbafa413d8e5ba032f4a2620a75d578e`. The
    dirty/staged half was a point-in-time observation of shared working trees on
    2026-08-23 and is NOT reproducible after the fact; it is recorded as an
    unreproducible observation rather than re-asserted. Nothing was committed
    from those trees by this change — the three landing commits carry only the
    paths this packet names, **plus two ordinary submodule pin-syncs**
    (`openxFactory` and `xFactories/MedxFactory`, both moved by `bed2a69`),
    disclosed and measured at `review/verification-2026-09-03.md` § 8.
  - *Amended 2026-09-03, before capture.* As first written the sentence above
    stopped at "the paths this packet names", which CONTRADICTED § 8 of this
    packet's own verification record. Copilot's round-1 review named the
    contradiction; it is taken, and the correction is an append to this note
    rather than an edit of the closed task.
- [x] 1.2 Record the topology decision and implementation handoff in this
  OpenSpec change without adding host-absolute paths.

## 2. Move upstream repository and create MedxChart

- [x] 2.1 Move the canonical standalone openChart checkout from the xFactory
  submodule directory to the projects workspace root, preserving its `.git`
  directory and user files.
- [x] 2.2 Initialize a new local MedxChart Git repository with repository
  guidance, overlay-boundary documentation, and an explicit openChart pin
  manifest.
- [x] 2.3 Add the current openChart commit as MedxChart's nested submodule,
  normalize its committed URL to the portable upstream remote, and commit only
  MedxChart-owned files.

## 3. Replace aggregate boundary

- [x] 3.1 Replace the xFactory `.gitmodules` entry and gitlink from
  `xFactories/openChart` to `xFactories/MedxChart` using a portable relative
  submodule URL.
- [x] 3.2 Update the xFactory project register and repository documentation to
  identify MedxChart as the Medx clinical satellite and openChart as upstream.
- [x] 3.3 Update affected MedxFactory documentation links and local path
  references without rewriting unrelated dirty files or immutable source-digest
  evidence.
  - *2026-09-03 — the evidence, named precisely.* "Affected MedxFactory
    documentation links" is ONE LINE IN ONE FILE: MedxFactory `933c5025`
    ("Point intake plan at MedxChart composition", 2026-08-23), one insertion
    and one deletion in
    `ideation/brainstorm/one-patient-intake-vertical-slice-delivery-plan-and-acceptance-gates.md`,
    repointing row P4 of the delivery-plan table from `openChart` /
    `../../../openChart/openspec/...` to `MedxChart` /
    `../../../MedxChart/openChart/openspec/...`. The plural in the task text
    overstates it, and the correction is appended rather than made by editing
    the task, which is closed. The "immutable source-digest evidence" half is
    the DELIBERATE NON-ACT `design.md` Decision 4 records: MedxFactory's proof
    evidence still names `openChart` as its provenance and was not laundered
    into MedxChart.

## 4. Verification

- [x] 4.1 Verify the nested MedxChart/openChart gitlink, pin manifest, and
  aggregate MedxChart gitlink all resolve to the expected commits.
  - *2026-09-03 — RE-VERIFIED at ratification, in
    `review/verification-2026-09-03.md`.* All three agree:
    `MedxChart:openChart` gitlink and `contracts/openchart-pin.yaml`
    `pin.revision` both `d2376a31dbafa413d8e5ba032f4a2620a75d578e`; the
    aggregation's `xFactories/MedxChart` gitlink
    `68d2f1f5db932cb5099ceac75dab66316ef22579`, equal to `opensoft/MedxChart`'s
    `origin/main`. **Nothing in the repository ENFORCES that agreement today** —
    that is § 5's whole subject.
- [x] 4.2 Verify no committed file contains a host-absolute path and no direct
  aggregate `xFactories/openChart` submodule remains.
- [x] 4.3 Run targeted YAML/Markdown/Git consistency checks and report any
  pre-existing dirty work left untouched.
  - *2026-09-03 — the report this task promised was never written, and the
    checkbox is NOT being unticked.* The checks were run in-session on
    2026-08-23 and their result is not recoverable; what IS recoverable has been
    re-run now and written down, so the reader gets a report rather than a
    claim. See **`review/verification-2026-09-03.md`** (`Status: record`), which
    carries the actually-executed
    `openspec validate create-medxchart-overlay-boundary --strict`,
    `openspec validate --all --strict`, the three-way pin agreement, the
    aggregation `.gitmodules` entry and gitlink, and the host-absolute-path
    sweep, each with its command and its output. The pre-existing dirty work of
    2026-08-23 is the half that cannot be reconstructed; it is reported as
    unreproducible rather than described from memory.

## 5. Bound follow-on — the descendant pin validator (GATES ARCHIVE)

**Commissioned 2026-09-03 by the ratifying ruling, under decision 1 option 1.**
Ratification does NOT wait on this group; **ARCHIVE DOES.** The reason is that
this packet's own § 4.1 verification is a one-time human reading of two files
that nothing re-reads: `domain-descendant-boundary`'s pin rule says a descendant
pins the product BY COMMIT TWICE and that its "own validator REFUSES the tree
rather than preferring either" when the two disagree, and `opensoft/MedxChart`
has no such validator. Until it does, the boundary this change establishes is
asserted rather than enforced. The pattern to copy is LedgerxWallet's, which is
live and named in `docs/domain-neutralization-candidate-register.md:812-820`:
`tests/validate_pin.py` with fail-closed checks, the REQUIRED `pin-validation`
check, ruleset `21701436`.

- [x] 5.1 Author `tests/validate_pin.py` in `opensoft/MedxChart`, fail-closed,
      REFUSING (never warning, never defaulting) when: the nested `openChart`
      gitlink and `contracts/openchart-pin.yaml`'s `pin.revision` name different
      commits; either is absent or unparseable; the pin manifest's
      `schema_version`/`kind` are not `1` / `medxchart_openchart_pin`; or the
      CHECKED-OUT `openChart/` revision differs from the recorded one or is
      dirty — the fourth check being the one that catches a fork executing at
      another commit while all three declarations agree.
  - *2026-09-04 — DONE, on Brett Heap's word "do the pin validators".*
    `opensoft/MedxChart` **PR #1**, merged
    **`8bc39a8ce8bb4e9cf54484e400644114a41b852a`** (2026-09-04T13:05:59Z) on his
    later word *"merge both when aligned and green"*, adds
    `tests/validate_pin.py` (384 lines) with **all four conditions above** as
    named fail-closed refusals — `pin-gitlink-disagrees`/`pin-gitlink-absent`,
    `pin-manifest-absent`/`pin-manifest-unreadable`,
    `pin-manifest-shape`/`pin-revision-invalid`, `pin-checkout-drift` — plus
    `tests/test_validate_pin.py` (213 lines, **seven** self-tests, one per
    refusal category with the passing, uninitialized and dirty cases). The two
    deviations from LedgerxWallet's check set are named in the validator's own
    module docstring rather than left to be found. Evidence, with the API
    readings: `review/realization-evidence-2026-09-04.md` § 2.
- [x] 5.2 Add `.github/workflows/pin-validation.yml` in `opensoft/MedxChart`
      running 5.1 on pull request and on push to `main`, with the check named
      `pin-validation` to match the LedgerxWallet precedent.
  - *2026-09-04 — DONE.* `.github/workflows/pin-validation.yml` (74 lines) in
    the same landing, `name: pin-validation`, on `pull_request` against `main`
    **and** `push` to `main` — both triggers this task asks for — with the job
    carrying no display name so the status check surfaces as exactly the literal
    `pin-validation` the ruleset pins, and no `paths:` filter so the required
    context can never fail to report. Evidence:
    `review/realization-evidence-2026-09-04.md` § 3.
- [x] 5.3 **[OPERATOR]** Create the branch-protection ruleset on
      `opensoft/MedxChart`'s default branch making `pin-validation` a REQUIRED
      status check, on the shape of ruleset `21701436`. This half is Brett's
      console act; no agent performs it, and an agent-reported "ruleset created"
      without the console act is not evidence.
  - *2026-09-04 — DONE BY THE OPERATOR, AND READ BACK RATHER THAN REPORTED.*
    **Ruleset `22272824`, "MedxChart pin-gate"** — Brett's console act,
    performed 2026-09-04, verified by the coordinator via
    `gh api repos/opensoft/MedxChart/rulesets/22272824` and re-read by this lane
    through the same call: Repository-sourced, `target: branch`, `enforcement:
    active`, `~DEFAULT_BRANCH`, required status check `pin-validation` with
    `strict` false, created 2026-09-04T13:17:59Z. His report of it was
    *"rulesets created … do 5.4 and archive both"*. **The id guessed in session
    before the act (`21987654`) was wrong; the API is authoritative.** The shape
    DEVIATES from precedent `21701436` in two directions — two extra rules
    (`deletion`, `non_fast_forward`) and one extra bypass actor (`RepositoryRole`
    id 5, `always`) — recorded as an OBSERVED DEVIATION and not repaired here,
    because editing an operator's ruleset is the act this task reserves:
    `review/realization-evidence-2026-09-04.md` § 4.1.
- [x] 5.4 Record the ruleset id and one green required run in this change's
      `review/` directory as realization evidence, then and only then open the
      archive gate.
  - *2026-09-04 — DONE; this task is the archive gate and it is now OPEN.*
    The record is **`review/realization-evidence-2026-09-04.md`**
    (`Status: record`, `Kind: report`), carrying the ruleset id, its full API
    reading, and **one green run UNDER the ruleset**: run **`33876197016`**,
    head `8bc39a8c`, **`run_attempt: 2`**, started 2026-09-04T13:25:34Z and
    completed **`success`** at 13:25:47Z. The first attempt (created 13:06:02Z)
    PREDATES the ruleset created at 13:17:59Z and is therefore green under no
    required regime; **the re-run is the evidence, and the two are distinguished
    by `run_attempt` because they share one run id**.
- [x] 5.5 Decide, in the same pass, whether `opensoft/MedxPractice` takes the
      same validator. It is the sibling realized placement this change's
      `domain-descendant-boundary` delta names, it carries the identical
      two-pin shape (`contracts/openpractice-pin.yaml`, `kind:
      medxpractice_openpractice_pin`, nested `openPractice` gitlink
      `9526bd9e`), and the sibling change
      `create-medxpractice-overlay-boundary` carries no delta of its own, its
      ratification packet being the one that IS TO CITE this delta — a future
      obligation, not a present fact: no sibling pull request has merged and that
      packet carries no reference to this file yet. Deciding it here keeps one
      answer for one shape; the
      DOING of it belongs to whichever packet the decision assigns.
  - *2026-09-04 — DECIDED, and the decision is not this lane's to make: it is
    already ratified text in the packet that owns MedxPractice.*
    `create-medxpractice-overlay-boundary`'s `tasks.md` § 5 carries the titled
    paragraph **"THIS GROUP ANSWERS THE SIBLING'S OPEN 5.5"**, whose answer is
    *"YES, and it is recorded here because this is the packet that owns
    MedxPractice"* — the two descendants carry the identical two-pin shape, so
    "one validator shape covers one pin shape and a second shape would be two
    answers to one question" — and which closes: *"This paragraph is the answer;
    the sibling's 5.5 checkbox cannot be ticked from this pull request and is
    left for the sibling's own pass to tick with a pointer here."* **This is that
    pass and this note is that pointer.** The decision is confirmed by what was
    built: `opensoft/MedxPractice` PR #1 merged `f7fd8364` (2026-09-04T13:05:10Z)
    with the same five files at the same sizes, a literal-only diff.
    **THE FUTURE-TENSE CLAUSE IN THIS TASK'S OWN TEXT IS NOW SPENT**: "no
    sibling pull request has merged and that packet carries no reference to this
    file yet" was true when written and stopped being true at `0bf37d14`
    (openxFactory #609, 2026-09-03), whose R3 cites this change's
    `domain-descendant-boundary` delta by path. The closed task text is not
    edited; the correction is this append.

## 6. Standing of the boundary itself — reported, not precedent

**6.1 is a REPORT, not a task, and it carries no checkbox.** It was authored as
a NEW checkbox already ticked, which is an agent certifying its own act; the
checkbox is removed rather than left ticked or left unticked, because nothing
here is owed. The evidence is `review/verification-2026-09-03.md` § 5 (the whole
tracked file list of both descendants, read from an independent clone).

**MedxChart is a REPORTED EMPTY BOUNDARY under
`domain-descendant-boundary` "A descendant is created on its first
profile, not before" (`openspec/specs/domain-descendant-boundary/spec.md:103-120`),
and is recorded as such rather than cited.** Its tracked tree at
`68d2f1f5` is composition metadata ONLY — `.gitmodules`, `AGENTS.md`,
`README.md`, `contracts/openchart-pin.yaml`, the `openChart` gitlink, and
two `.gitkeep` placeholders under `openspec/` — with **ZERO openChart
profile artifacts**. That rule's fourth scenario is exactly this shape:
"WHEN a descendant repository exists carrying no profile artifact of the
product THEN it is an empty boundary, and it is reported rather than cited
as precedent for creating more." `opensoft/MedxPractice` at `d8d73195` is
the same shape (`.gitmodules`, `AGENTS.md`, `README.md`,
`contracts/openpractice-pin.yaml`, the `openPractice` gitlink).
**Neither is citable as precedent for creating another descendant.** The
PLACEMENT this change ratifies and the CREATION rule are different
requirements, and ratifying the first grants nothing under the second.
Both boundaries predate the rule that would have gated them
(`split-openxwallet-repo`, 2026-08-28), which is why they are reported
rather than refused.
