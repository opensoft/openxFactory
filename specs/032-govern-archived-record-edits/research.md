# Phase 0 Research: 032-govern-archived-record-edits

**Date**: 2026-09-08 | **Base**: `main` `68712924` | **Branch**: `032-govern-archived-record-edits`

This feature decides nothing that the ratified packet already decided, so this
file records MEASUREMENTS rather than options. Each is reproducible from the
command beside it.

## M1 — The packet, promoted canon and the § 3.4 target have not moved since ratification

```bash
git merge-base --is-ancestor 3504287a 68712924 && echo ancestor
git log --oneline 3504287a..68712924 -- \
  openspec/changes/govern-archived-record-edits \
  openspec/specs/document-lifecycle \
  docs/document-lifecycle.md
```

`3504287a` (Merge PR #788) IS an ancestor of the base, and the second command
prints NOTHING. Consequence: the ratified bytes this feature must not touch, the
canon the MODIFIED block is checked against, and the document task 3.4 edits are
all in the state ratification left them. The 4.2 currency check is re-run at the
final head anyway — "continuously until archive" is the rule, and an unmoved
canon today is not a measurement of the canon tomorrow.

## M2 — No in-repo `sha256` pin names `docs/document-lifecycle.md`

```bash
grep -rn 'sha256' --include='*.yaml' --include='*.yml' --include='*.json' . \
  | grep -i 'document-lifecycle'          # → no output
python3 -c "import yaml;..."               # contracts/manifest.yaml → 0 docs/-prefixed path values
```

The only pairings of that path with a digest live in
`examples/document-cataloging/*.yaml`, which are ILLUSTRATIVE FIXTURES for the
cataloging schema, not live pins. Consequence: the second ADDED requirement's
re-derivation obligation does not attach to this feature's own edit. The claim is
scoped to IN-REPO pointers, which is exactly the scope task 1.2a ratified
("every in-repo sha256 pointer to an in-repo target"); nothing here is a claim
about pins held in another repository.

## M3 — doc-health scans `docs/` and does not scan the Speckit tree

`scripts/doc_health/corpus.py`: `GOVERNED_ROOTS = ("contracts", "docs",
"examples", "ideation", "templates")`, and `EXCLUDED_PARTS` drops `.git`,
`installs`, `node_modules`, `tests`, `__pycache__`. Root `specs/` is not a
governed root, so this feature's own Speckit files cannot move the finding set;
`docs/document-lifecycle.md` is inside one, so the § 3.4 bullet is the ONLY act
here that can. Gate 4.4 therefore diffs the branch's finding set against `main`'s.

## M4 — `evidence/` is outside the lifecycle scan set

`corpus.py`: `LIFECYCLE_SCAN = ("openspec/changes/**/proposal.md",
"openspec/changes/**/review/*.md")` and `EVIDENCE_PARTS = frozenset({"supporting-docs",
"source-snapshots", "evidence"})`, applied as a segment filter after the globs
resolve. Consequence: `openspec/changes/govern-archived-record-edits/evidence/realization-2026-09-08.md`
owes no lifecycle header and cannot raise a lifecycle finding, while a
`review/` record would owe one under the very requirement this packet modifies.

## M5 — The corpus ticks `[OPERATOR]` boxes on the act, and marks a not-owed box with a line

Ticked operator boxes, verified in this tree:

- `openspec/changes/archive/2026-09-04-create-medxchart-overlay-boundary/tasks.md:136`
  — `- [x] 5.3 **[OPERATOR]** Create the branch-protection ruleset …`, with the
  console act read back (`ruleset 22272824`) rather than reported.
- `openspec/changes/archive/2026-09-05-add-release-tag-gate/tasks.md:127`
  — `- [x] 4.1 **[OPERATOR]** Make release-tag-gate a REQUIRED status check …`.

A not-owed box left unticked with a dated line:
`openspec/changes/archive/2026-09-05-mirror-floor-addition-grace/tasks.md:346`
— `- [ ] 6.3 NOT OWED HERE, and named so it is not silently assumed …`.

Tick ratios of the six most recently archived changes: 28/0, 28/1, 21/0, 39/0,
40/0, 26/0 (ticked/unticked). An archived packet whose boxes are all open would
be the outlier, not the norm.

## M6 — The § 0 and § 5.1 bookkeeping already landed

`tests/sequenced_after/corpus-ledger.yaml:214` reads
`govern-archived-record-edits: {state: active, class: co-modifier, declares:
[govern-openspec-corpus-membership], depth: 1, prose: false, moved_by: "#788",
moved_on: "2026-09-08"}`; `README.md:659` carries the packet's Records row.
Consequence: those two boxes are ticked as ALREADY DONE and neither file is
rewritten by this feature.

## M7 — The precedent for amending a ratified sentence in place

Commit `3b530009` (2026-09-06, "Name the superseded sentence in the archive-time
header amendment") is the shape FR-017 follows: the amendment NAMES the sentence
it supersedes and gives the reason, rather than silently rewriting it. The
precedent for correcting a narrow ratified enumeration is
`openspec/changes/archive/2026-08-21-align-status-reader-to-real-lines`
(Brett Heap's 2026-08-19 correction).

## M8 — The doc-adoption precedent lands BEFORE archive

`govern-openspec-corpus-membership` wrote its bullet into
`docs/document-lifecycle.md` in commit `7157fa3e` (2026-08-23) and archived in
`01ff3434` (same day, later). The bullet carries its citation inline — "Ratified
by `govern-openspec-corpus-membership` (2026-08-23)" — written while the change
was still active. Consequence: FR-003's citation form is the corpus's own, not an
invention, and adopting on the realization branch rather than at archive is the
established order.

## M9 — The OpsxFactory twin HAS LANDED

```bash
git clone --filter=blob:none git@github.com:opensoft/OpsxFactory.git <tmp>
git -C <tmp> merge-base --is-ancestor bbbef015cd394e2de31586b9718356586c413884 origin/main
git -C <tmp> log -1 --format='%H %ad %s' --date=iso-strict bbbef015…
```

`bbbef015cd394e2de31586b9718356586c413884` — "Merge pull request #279 from
opensoft/change/govern-archived-record-edits", 2026-09-08T11:28:23-04:00 =
**2026-09-08T15:28:23Z** — IS an ancestor of that repository's `main`. Read-only
clone; nothing in OpsxFactory is written by this feature. Consequence: task 3.1's
act is done, the "no merge sha exists" reading is superseded by measurement, and
the tick rests on the cross-citation check T012a performs rather than on the
merge alone.

## M10 — The packet holds SIX files

`.openspec.yaml`, `design.md`, `proposal.md`, `tasks.md`,
`review/ratification-2026-09-08.md`, `specs/document-lifecycle/spec.md`. The
ratification record's "five files and no others" describes the RATIFIED BASELINE,
which predates its own review record; carrying that number forward into a
realization-era enumeration would state a false count.

## M11 — doc-health stamps the checkout's directory basename

`runner.build_context` puts the basename into `repo=<basename>` on every finding
line, into the `Repo-Identity:` header and into the "scope limited to single repo
<name>" line. A baseline taken in a differently-named directory therefore differs
on EVERY line, and `--previous-report` refuses outright on the mismatch. The
comparison uses an identically-named baseline checkout, or normalizes all three
places, and is proven main-vs-main before it is trusted.

## M12 — The passages the realization supersedes, located rather than guessed

`openspec/changes/govern-archived-record-edits/tasks.md`: line 7 (preamble,
"EVERY BOX IS UNTICKED"), lines 58–66 (§ 0.1, "THE BOX STAYS UNTICKED", with the
stale-but-true-when-written "this packet is `Status: draft` awaiting ratification
at task 1.1" at line 60), line 68 (§ 1 heading), line 70 ("GIVEN 2026-09-08, AND
THE BOXES BELOW STAY UNTICKED"), line 73 ("The heading is left as written because
it names what the section was raised to hold"), lines 74–78 (the re-assertion),
line 161 (§ 3 heading). `proposal.md`: lines 17 and 44, each asserting every box
stays unticked. `README.md`: line 671, "all 28 boxes in `tasks.md` stay unticked",
inside this change's Records row.

## M8a — The doc-adoption precedent is the ONLY one of its kind in this document

Re-measured at base `68712924`: `docs/document-lifecycle.md` § *Status Claim
Rules* carries exactly ONE bullet citing its ratifying change inline
(`govern-openspec-corpus-membership`, 2026-08-23, at lines 104–105), and the
citation is the LAST clause of that bullet's parent prose with sub-bullets
following. So the form FR-003 adopts is not a common pattern read loosely — it is
the single precedent, quoted from the file rather than remembered.

## Open questions

None. The ten of round 1 were answered by the architect seat on 2026-09-08 and
are recorded in `clarify-questions.md` and § *Clarifications* of `spec.md`.
