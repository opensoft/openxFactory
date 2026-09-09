# Clarify questions — 033-add-consent-custody-rederivation-record

**Round 1 (STOP A), 2026-09-09, lane `opsXfactory-1`. ANSWERED 2026-09-09 by
the architect seat after a cross-model adversarial review of the draft answers;
every answer is written inline beneath its question, and Q2 is PARKED FOR BRETT
with a planned-on default.** Twelve questions. The
reused F.3 rulings (Q1 tick-with-evidence and the `3b530009` amendment form, Q4
dual evidence, Q5 same-commit, Q9 full Speckit tree, Q10 frozen ratified prose)
are taken as settled and are NOT re-asked. Everything below is something they do
not settle, each stated with what was MEASURED on branch
`033-add-consent-custody-rederivation-record` (base `main` `6df21737`).

---

## Q1 — `contract-v3.5` is free. How do § 5.2–5.5 land when the merge IS the cut? (re-cut as `contract-v3.6` on 2026-09-09 after #866 took v3.5 — see [#630 comment 5609442856](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5609442856))

**Measured.** `contracts/manifest.yaml:3` declares `contract-v3.4`;
`contracts/releases/` holds `contract-v3.4.digests.yaml` as its highest (283
entries); `git tag -l 'contract-v*'` tops out at an annotated `contract-v3.4`.
No surface carries `contract-v3.5`. `contract-v2.6` is the SPENT number, not
this one. **The next additive minor is `contract-v3.5`** (re-cut as `contract-v3.6` on 2026-09-09 after #866 took v3.5 — see [#630 comment 5609442856](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5609442856)) — a measurement, and
§ 5.1's claim on issue #630 row 4 is the LANE's to post, not mine.

**Measured precedent.** `contract-v3.4` was cut by PR #653 and landed as a
SQUASH commit `807a4f47` (one parent, committer GitHub, subject `… (#653)`) —
so the landed commit is NOT the reviewed candidate, and
`docs/contract-versioning-policy.md` § *Bundle Realization Order* step 4 says
the landed commit then "becomes the new candidate and every gate and review
reruns before tagging."

**Ask.** (a) ONE pull request carrying §§ 2–5 together, or TWO (the growth
first, the cut second on a re-measured number)? (b) Given the squash, is § 5.5
ticked on the pre-merge gate evidence at the exact candidate, with the post-merge
re-run recorded as OWED to whoever lands it — or is § 5.5 a NOT-OWED for me
because I neither merge nor land?

**ANSWER — 2026-09-09, architect seat (lane `opsXfactory-1`), after cross-model
adversarial review.**

**(a) ONE pull request carrying §§ 2–5.** Mandated by
`docs/contract-versioning-policy.md` § *Version Identity*: *"The manifest and
changelog update SHALL be committed atomically with the contract files."* Two
PRs would separate them.

**The version number is re-measured and CLAIMED BY THE LANE at the LAST
merge-from-main before the merge** — the ratification record lines 109–111 and
task 5.1 both say *"at cut time and not before"*, and the policy forbids a
reservation before merge order is known. The PR body names `contract-v3.5` (re-cut as `contract-v3.6` on 2026-09-09 after #866 took v3.5 — see [#630 comment 5609442856](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5609442856)) as
the MEASURED candidate, explicitly provisional. **The orchestrator re-measures
at every merge-from-main and reports.**

**THE LANDING CONTRACT (record it in `plan.md`).** Landing is a MERGE COMMIT —
allowed, there is no linear-history rule on this repository. The lane performs
the final merge-from-main inside its Rule 6 window, RE-RUNS the gates (policy
step 4: the merge commit *is* "a different commit"), then merges. The annotated
tag (§ 5.6, Brett's act) targets the LANDED MERGE COMMIT. If `main` advanced
under `contracts/` between integration and merge, the lane REPEATS the
integration.

**(b) § 5.5 and § 5.6 are NOT-OWED-HERE.** The lane ticks § 5.5 in a follow-up
bookkeeping commit while the packet is still live; Brett tags.

---

## Q2 — WITHHELD needs an exit-status class, and this repository has ruled none

**Measured.** Every `Exit codes:` docstring in `scripts/` tops out at **2** —
most read `0 ok, 1 findings, 2 harness error`, and **this script's own reads
`0 ok, 1 findings, 2 dependency/harness error` at line 80**, which is the
ratified wording the growth must KEEP rather than narrow (panel F10). The only `3` in the tree is
`scripts/avatar-metering-alert.py` — "nothing crossed a paging threshold" —
which is a different meaning. `Findings` in
`scripts/validate-consent-instruments.py` carries `errors` / `warnings` /
`notes` and nothing else. Task 3.4b asks for "the one the repository rules for
'needs a human decision'". **There is no such rule to read.**

**HARD CONSTRAINT, measured.** § 4.8c puts a WITHHELD fixture INSIDE the
packaged corpus, and the packaged self-test runs on every invocation. So
whatever class is chosen, `python3 scripts/validate-consent-instruments.py
--strict` with no path argument MUST still exit 0 over the packaged corpus, or
this feature reddens every caller — the same failure mode
`validate-release-tag-gate.py`'s own header records for `release-tag-publication`
in September.

**Ask.** Which:

- **(a)** a new exit code `3` for a REAL instrument that withholds, with the
  packaged self-test's withheld fixture explicitly not raising it (the fixture
  is an *expected* withholding, like a negative is an expected failure);
- **(b)** exit `0` always, WITHHELD carried only in the report line and the
  named outcome, leaving the exit-status escalation to the consumer's gate;
- **(c)** exit `3` unconditionally, and CI callers are changed to tolerate it;
- **(d)** something else you name.

If (a) or (c), name the code — I will not invent an exit-status vocabulary for
this repository.

**ANSWER — first PARKED FOR BRETT and planned on (a); now RULED. Both halves
are kept, because the reasoning that produced the default is what the ruling
confirms.**

**RULED 2026-09-09 BY BRETT HEAP — NO LONGER PARKED.**

Given in session, first-hand to lane `opsXfactory-1`, by MULTIPLE-CHOICE
SELECTION at approximately **2026-09-09T14:2xZ**; relayed to and recorded by
this orchestrator at **2026-09-09T14:40:16Z** (`date -u`, measured at the
receipt rather than reconstructed). **Option text selected, verbatim:**

> **"Exit 3 = needs a human decision (Recommended)"**

The alternatives offered and **NOT** chosen, recorded so the ruling reads as a
choice rather than a default: *"Exit 1, same as findings"* and *"Exit 0, report
only"*.

**THIS IS THE REPOSITORY RULE task 3.4b ASKED FOR.** The task required *"the
exit status the repository rules for 'needs a human decision'"*, and until this
selection the repository had ruled none — every `Exit codes:` docstring in
`scripts/` read `0 / 1 / 2`. It now has one. The lane posts the RULING on
openxFactory issue #630 as the repository-level record.

**What is applied:**

- **Exit `3` = "needs a human decision"**, returned for a REAL instrument that
  WITHHOLDS with no error present.
- **The PACKAGED withheld fixture is EXEMPT** — an expected withholding is to
  the third bucket what an expected failure is to a negative — so the packaged
  self-test still exits `0`.
- The script's docstring becomes
  **`Exit codes: 0 ok, 1 findings, 2 dependency/harness error, 3 withheld — needs a human
  decision`**, extended in THIS SCRIPT ONLY.
- **A single named constant** still carries the number, and the ruling is cited
  at that constant, in the design note and in the realization evidence — with
  the verbatim option text and the channel.

---

**THE DRAFT ANSWER THIS RULING CONFIRMS (kept as authored, 2026-09-09):**

The cross-model reviewer REFUTED option (b) on two measured grounds, and the
refutation is accepted:

1. **Exit 0 contradicts ratified text.** Task 3.4b requires *"the exit status the
   repository rules for 'needs a human decision'"*, and the delta (line 173)
   says WITHHELD is *"never a pass"*. An exit code of 0 IS a pass to every
   caller that reads one.
2. **The hard constraint in Q2 was unsupported.** Measured: **NO caller reads
   this validator's exit code today** — not one of the twelve workflows, no
   pytest, and no OpsxFactory leg. So a new nonzero code reddens nothing.

**Plan on (a):** a NEW exit code meaning "needs a human decision",
**provisionally `3`**, with:

- the packaged withheld fixture **EXEMPT** — an expected withholding is to the
  third bucket what an expected failure is to a negative;
- the shared `Exit codes:` docstring vocabulary extended **in this script only**;
- a design note recording that **the NUMBER is Brett's ruling to make**;
- tasks 3.4b and 4.8c written so the code is a **single named constant**, so if
  Brett rules differently the constant moves and nothing else does.

---

## Q3 — Where does the withheld fixture live, and how does `self_test` hold a third bucket?

**Measured.** `self_test` has exactly two loops: `EXAMPLES_DIR.glob("*.example.yaml")`
(must validate cleanly, else `expected a valid example`) and
`NEGATIVE_DIR.glob("*.yaml")` against `EXPECTED_NEGATIVE_FINDINGS` (must fail
for a declared code, with fail-closed both ways for unregistered/missing files).
A withheld fixture in either loop breaks it. The corpus today is **6 valid + 7
negative + 2 purpose probes**.

**Ask.** (a) A THIRD directory `examples/consent-instrument/withheld/` with an
`EXPECTED_WITHHELD_OUTCOMES` table mirroring the negatives' fail-closed
discipline — or the fixture kept among the positives with an opt-out set? (b)
Does layer 2 (`repo_scan`, real artifacts under a path argument) need the same
third bucket, or does it simply report WITHHELD as it finds it?

**ANSWER.** **(a)** A third directory `examples/consent-instrument/withheld/`
with an `EXPECTED_WITHHELD_OUTCOMES` table, **fail-closed both ways** — a
fixture on disk with no table entry and a table entry with no fixture are each
errors, exactly as `EXPECTED_NEGATIVE_FINDINGS` already is.

**(b)** `repo_scan` reports WITHHELD **as it finds it**. It already excludes
`examples/`, so no bucket discipline is owed there.

---

## Q4 — Do any schema identity fields other than `contract_schema_version` move?

**Measured.** The file carries `$schema` (draft 2020-12), `$id:
"consent-instrument.schema.yaml"`, `contract_schema_version: 2`, and the record
property `schema_version: const: 1`. The `contract-v1.33` precedent
(`add-client-identity-roster`, `1 -> 2`) moved `contract_schema_version` ONLY —
`$id` unchanged, `const: 1` unchanged, and the manifest row's own
`schema_version: 1` field unchanged.

**Ask.** Confirm the same here: `contract_schema_version` `2 → 3` and NOTHING
else — `$id` frozen, the record envelope's `const: 1` frozen, and the
`contracts/manifest.yaml` `consent-instrument` row's `schema_version: 1` frozen.

**ANSWER.** Confirmed. **Only `contract_schema_version` moves, `2 → 3`.**
`$id` frozen, the record envelope's `schema_version: const: 1` frozen, and the
`contracts/manifest.yaml` row's own `schema_version: 1` frozen.

---

## Q5 — When does the manifest's `consent-instrument` digest move?

**Measured, and it forces half the answer.** The row pins `sha256:
13b0fe46fdb8791020b426dcd763aced2a3280a82923b32d3a0d0877ab6ad441`, and
`sha256sum` over the file returns exactly that. `python3
scripts/validate-manifest-digests.py` verifies **189 per-file digests** and is
run inside `pytest-suite` by `tests/manifest_digests/test_manifest_digest_sweep.py`.
So the moment the schema file changes, the digest is stale and the REQUIRED
pytest gate is red until it is re-derived. It cannot wait for § 5.2.

**Measured, second leg.** `contracts/schemas/consent-instrument.schema.yaml` is
**NOT** a member of the release digest inventory —
`contract-v3.4.digests.yaml` carries five `contracts/schemas/*` paths and this
is not one of them. So the schema edit re-bases a manifest row and adds no
inventory row.

**Ask.** (a) Confirm the `sha256` re-derivation rides the § 2 schema commit
(forced by the gate above) while `contract_bundle_version` and the
`consumption_rule` prose ride the § 5.2 candidate commit — three edits to one
file across two commits. (b) The `consumption_rule` today ends with the
`contract-v1.33` paragraph; does § 5.2 APPEND a `contract-v3.5` paragraph in
that same style (what grew, that it is additive, that the envelope stayed), or
rewrite the rule? (c) Confirm `consent-instrument-class-registry`'s row is
untouched — nothing in this change reaches class declarations.

**ANSWER — revised TWICE. The second revision, by the consistency panel (F2),
is the OPERATIVE ruling; the first is kept below because its reasoning about
ungated intermediate commits is true and was simply not the deciding factor.**

**OPERATIVE (panel F2, 2026-09-09).** The split runs on WHAT THE FIELD IS:

- the `consent-instrument` row's **`sha256` is INTEGRITY BOOKKEEPING FOR THE
  EDITED FILE**, not a release surface → it rides the **§ 2 schema commit**;
- **`contract_bundle_version`, the appended `consumption_rule` paragraph,
  `contracts/CHANGELOG.md`, the digest inventory and the cut-coupled tests** are
  **VERSION IDENTITY**, which is what policy step 2's atomicity concerns → they
  ride the ONE **§ 5.2 candidate commit**.

**Consequence: every intermediate commit is GREEN, and the declared constitution
deviation is WITHDRAWN** — FR-049 and T079a are removed, and T017 now re-derives
the digest instead of declaring it stale.

---

**THE FIRST REVISION, kept as authored:**

**(a) NO SPLIT.** Task 5.2 and policy step 2 both require every release surface
to move in ONE candidate commit. The question's constraint — that
`tests/manifest_digests` reddens the moment the schema changes — does not bind,
because **intermediate commits on a branch are ungated: CI runs at the PR
head**, not at every commit. So the manifest edit — digest re-derivation AND
`contract_bundle_version` AND the `consumption_rule` paragraph — rides the
SINGLE § 5.2 candidate commit. **§ 2's schema commit leaves the digest stale on
purpose, and its commit message says so.**

**(b)** APPEND the `contract-v3.5` (re-cut as `contract-v3.6` on 2026-09-09 after #866 took v3.5 — see [#630 comment 5609442856](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5609442856)) paragraph in the `contract-v1.33` style —
what grew, that it is additive, that the envelope stayed.

**(c)** Confirmed: `consent-instrument-class-registry`'s row is untouched.

---

## Q6 — How much does the `contract-v3.5` CHANGELOG entry have to name? (re-cut as `contract-v3.6` on 2026-09-09 after #866 took v3.5 — see [#630 comment 5609442856](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5609442856))

**Measured.** `git diff --name-status contract-v3.4 HEAD -- contracts/` reports
**4 additions and 14 modifications**, none of them this session's: added
`openspec-cli-pin.yaml`, `openspec-cli-pin.1.12.0.package-lock.json`,
`policies/repository-identity.yaml`, `review-lane-repin-binding.template.yaml`;
modified `README.md`, `manifest.yaml`, `openreposhape-pin.yaml`,
`openxwallet-pin.yaml`, `review-lane-pin.yaml`, `review-lane-floor-snapshot.yaml`
and eight `hermes-domain-overlay` / `omnigent` example fixtures. Separately,
`2026-09-08-publish-openspec-cli-pin-as-contract-member` chose **A-defer** over
**A-cut** (`contract-v3.5` in that PR), unvetoed — so that registration is
waiting for THIS bundle to publish it.

Task 5.3 says the entry "names what changed in the bundle, not what this session
intended", and the `contract-v3.4` entry did exactly that, attributing every
moved path to its originating pull request.

**Ask.** Confirm the § 5.3 entry attributes ALL of the above by originating
change/PR — and confirm the change class is ADDITIVE (minor): one new optional
property, one `contract_schema_version` bump, no field removed, no enumeration
narrowed, every existing instrument valid unchanged.

**ANSWER.** Confirmed. The § 5.3 entry attributes **all 4 additions and all 14
modifications since `contract-v3.4`** by originating change/PR — including the
`publish-openspec-cli-pin-as-contract-member` **A-defer** registration, which
this bundle is what finally publishes. **Change class: ADDITIVE (minor)** — one
new optional property, one `contract_schema_version` bump, no field removed, no
enumeration narrowed, every existing instrument valid unchanged.

---

## Q7 — Where do the two new tests live, and what proves the blob walk?

**Measured.** There is no `tests/consent*` directory. Sibling test packages mix
conventions: `tests/client-identity-roster` and `tests/doc-health` use hyphens;
`tests/manifest_digests`, `tests/sequenced_after`, `tests/scope_globs` use
underscores. CI runs `python3 -m pytest tests/ -q -m "not postgres"`.

**Ask.** (a) Directory name for the new package — `tests/consent_instruments/`
(underscore, importable) or `tests/consent-instruments/` (hyphen, matching the
contract family's spelling)? (b) Is task 3.5's blob-walk extension proved by the
§ 4.8b negative fixture ALONE (self-test), or does it also get a pytest? (c)
Task 3.3's no-git assertion — is a source-level assertion (no `import
subprocess`, no `git` token, no filesystem read of a locator in the module)
sufficient, or do you want a runtime assertion that patches `subprocess` and
`Path.open` and proves neither is reached?

**ANSWER.** **(a)** `tests/consent_instruments/` — underscore, importable.

**(b)** **BOTH**: the § 4.8b fixture in the self-test AND a **parametrized
pytest** proving the walk reaches each of the four free strings.

**(c)** **BOTH**: the source-level ban (no `subprocess` import, no `git` token,
no locator file read anywhere in the module) AND a **runtime patch** of
`subprocess.run` and `Path.open` exercised over **ALL THREE buckets** —
positive, negative and withheld — not only the positives. A no-git assertion
that runs only the happy path is not an assertion about the withheld leg, which
is the leg most likely to reach for a repository.

---

## Q8 — Four README sentences this realization falsifies, and one substrate

**Measured.** `README.md` carries four statements about this packet's box count:

1. **line 856–857**, its own OpenSpec Records row: *"**all 46 boxes in
   `tasks.md` stay unticked**"* — becomes FALSE.
2. **line 2950**, inside `govern-archived-record-edits`' row: *"exactly as the
   sibling `add-consent-custody-rederivation-record` left its 46"* — past tense,
   arguably survives.
3. **line 3022**, inside the `add-pre-archive-citation-gate` narrative: *"that
   packet is a ratified PROPOSAL with all 46 boxes unticked, so the three pins
   are still broken"* — present tense, becomes FALSE (the pins DO stay broken:
   that half is § 6, the consumer's).
4. **line 3098–3100** (the sentence ends at 3100): *"measured 2026-09-09 UTC at `main` `6cc06288`, that
   packet still carries all 46 boxes unticked"* — a DATED measurement, stays
   true as written.

**Ask.** (a) Which of 1–4 take the `3b530009` amendment form, and which are left
as true-when-written? (b) `README.md`'s OpenSpec Records block is a row-3 shared
substrate on issue #630 under Lane Collision Protocol Amendment 1 Rule 7 — does
amending an EXISTING row (adding no new one) need a fresh substrate claim from
the lane before I write, or does the change's standing row-3 claim
(`5571680388`, 2026-09-07) already cover it?

**ANSWER.** **(a)** Amend in the `3b530009` form:

- **sentence 1** — this packet's own OpenSpec Records row (`README.md:856–857`),
  *"all 46 boxes in `tasks.md` stay unticked"*;
- **sentence 3** — `README.md:3022`, the present-tense box count. **KEEP
  "the three pins are still broken"**: that half stays true, because the repair
  is § 6 and § 6 is the consumer's;
- **a FIFTH site the reviewer found**, and it is the load-bearing one:
  **`README.md:2993`**, inside the `govern-archived-record-edits` row —
  *"the consent family's is PROPOSED only (`contract_schema_version: 2`, no
  `custody_rederivations` property, `contract-v3.4`, 46/46 boxes unticked)"*.
  **False on all four counts after this lands**, and it is the premise of that
  rule's TRANSITION CLAUSE (report-until-declared → refuse-on-declaration).

Leave **sentence 2** (past tense, *"left its 46"*) and **sentence 4** (a dated
measurement at a named commit) as **true-when-written**.

**(b)** **The LANE posts the substrate note** for the SIBLING-row sentences
(3 and 5) **before you write them**. This packet's own row is covered by its
standing row-3 claim (`5571680388`, 2026-09-07).

---

## Q9 — How far does `examples/consent-instrument/README.md` grow?

**Measured.** It carries `Status: draft` and four sections: a Layout tree with a
one-line annotation per file, a *Schema → example map* table, a *Named cases
from the spec* list, and *Validating locally*. This feature adds roughly 4
positives, 10 negatives and 1 withheld — nearly tripling the tree.

**Ask.** (a) Do all four sections grow (tree entries, table cells, one *Named
case* bullet per new spec scenario), or is the growth confined to the tree and
the table with ONE consolidated *Named case* covering the custody-chain family?
(b) Does the withheld bucket get its own row in the *Schema → example map*
table, which today has only "Valid example(s)" and "Negative example(s)"
columns?

**ANSWER.** Tree and table **complete**. *Named cases from the spec* grows
**one bullet per refusal code (7) + one positive chain-shapes bullet + one
withheld bullet** = 9 new bullets. The *Schema → example map* table gains a
**third column** for the withheld bucket.

---

## Q10 — Are the candidate finding codes adopted as written?

**Measured.** `tasks.md` offers them as "candidates", and the ratified delta
names no finding code at all: `custody-chain-unanchored`,
`custody-chain-broken-link`, `custody-chain-locator-gap`,
`custody-chain-out-of-order`, `custody-pin-rewritten`,
`custody-path-class-digests-differ`, `custody-content-class-withheld`.

**Ask.** Adopt all seven verbatim, or do you want different names? (Adopting
them verbatim is my recommendation — they match the file's existing
`custody-sha256-malformed` / `embedded-original-content` style and a fixture
table will pin each one, so renaming later is a corpus-wide edit.)

**ANSWER.** Adopt all seven codes **verbatim**:
`custody-chain-unanchored`, `custody-chain-broken-link`,
`custody-chain-locator-gap`, `custody-chain-out-of-order`,
`custody-pin-rewritten`, `custody-path-class-digests-differ`,
`custody-content-class-withheld`.

---

## Q11 — Is a local `release-tag-gate` run tickable evidence for § 5.4?

**Measured.** `release-tag-gate` is a GitHub workflow evaluating pull requests
that touch `contracts/manifest.yaml` or `contracts/releases/`; its logic is
`scripts/validate-release-tag-gate.py`, runnable locally with `--head` / `--base`.
I do not open pull requests, so I cannot observe the workflow.

**Ask.** Is § 5.4 ticked on the local run of all five gates against the exact
candidate (with the transcripts in `evidence/`), leaving the workflow's own
green as the lane's post-open observation — or does § 5.4 stay unticked until a
workflow run exists?

**ANSWER.** § 5.4 is **ticked on the local run of all five gates against the
exact candidate**, with the transcripts in `evidence/`. The workflow's own green
is the **lane's PR-open observation**, not this feature's tick condition.

---

## Q12 — Exactly which entry fields does the extended `walk_strings` cover?

**Measured.** Today `check_custody` walks EVERY string under `custody` and skips
only `custody.sha256`, so `custody.locator` IS walked. Task 3.5 names
`ruling_ref` and `.recorded_by` as the target and adds that "the locators are
opaque POINTERS and are walked on the same footing as `custody.locator` is
today."

**Ask.** Walk the whole entry with the same two-digest skip (`previous_sha256`,
`observed_sha256`) — which also covers `commit`, `at`, `diff_class` and `reason`
harmlessly, since a pattern/enum/format already bounds each — or walk EXACTLY
the four free strings (`previous_locator`, `observed_locator`, `ruling_ref`,
`recorded_by`)? The first is the "wherever it hides" posture the guard exists
for; the second is narrower and cheaper to explain.

**ANSWER.** Walk **the whole entry minus the two digests**
(`previous_sha256`, `observed_sha256`). That is the "wherever it hides" posture
the guard exists for, and the incidentally-covered fields (`commit`, `at`,
`diff_class`, `reason`) are each already bounded by a pattern, a format or a
closed enumeration, so the walk costs nothing there.

---

**ROUND 1 IS RULED, ALL TWELVE.** Q2's exit-code NUMBER was parked for Brett
Heap and was RULED by him on 2026-09-09 — **exit `3`, "needs a human decision"**
— so nothing in this round is now open. The constant stays a single named
constant regardless, because that is good practice and not a hedge. Two additions from the
review (A1, A2) are carried above.


---

## A1 — `contracts/README.md` carries a corpus count task 4.9 does not name

**RAISED BY THE CROSS-MODEL REVIEW, MEASURED AND CONFIRMED.**
`contracts/README.md` line 102 — the row for
`scripts/validate-consent-instruments.py` + `examples/consent-instrument/` —
reads *"self-testing over 5 positives, 5 indexed negatives, and 2 purpose
probes"*. It is **already false at 6/7 before this feature adds a byte**, and
task 4.9 names only `examples/consent-instrument/README.md` and the
`contracts/manifest.yaml` comment.

**RULING: add a task** correcting it with the RE-MEASURED counts (three buckets,
not two), in the same "re-measured rather than adjusted by arithmetic"
discipline task 4.9 sets. It is carried as an ADDITIONAL realization act, not as
an edit to the ratified task list's numbering.

---

## A2 — Landing this realization arms a cross-repo consequence no task performs

**RAISED BY THE CROSS-MODEL REVIEW. STATE IT; DO NOT ACT ON IT.**

`govern-archived-record-edits` is now canon in both repositories. Its
**transition clause** makes an edit of a pinned target **REPORTED** while the
target's family has declared no re-derivation rule, and **a REFUSAL for that
family the day it declares**. Measured at that rule's authoring, the premise was
*"NO family anywhere has a declared re-derivation rule today — the consent
family's is PROPOSED only"*.

**Landing this realization DECLARES the consent family's rule.** So for the
consent-custody family the posture converts from REPORTED to REFUSED **once
F.2's gate exists** — a cross-repo consequence that **no task in this packet
arms, schedules or owns** (§ 7.1 puts F.2's gate in OpsxFactory's own change).

**RULING:** record it as a **dated note in the realization evidence** and in the
neighbourhood of § 7 in the packet's `tasks.md`. **Do not build it, do not
schedule it, and do not tick anything for it.**
