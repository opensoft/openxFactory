# codexFactory's floor-relocation retitle, dispositioned — the runs, verbatim

Status: record
Kind: report
Measured on: 2026-09-10
Base: openxFactory `main` at `3b45c037`, in a FRESH CLONE at branch
`change/disposition-codexfactory-floor-relocation-retitle`. The consuming trees
measured are codeXfactory/codexFactory at `32743fb7ebe0a89dc4a5ab0b53396530cf2d9ee5`
(the head of PR #318, `change/archive-floor-regeneration-option-b`),
codeXfactory/codexFactory `main` at `0dfed9a483ff861ebaa9af5debfd34f675467ac3`
and again at `9b1b0a21be4440639107335cf87f755beca1ecbd` after PR #339 landed the
`Merged into` marker mid-authoring, and #318's head MERGED with that main at
`89ee5e84dce6da343e05bb03933fe745c0704549`. THE WHOLE PAIR WAS THEN RE-TAKEN AT
COMMIT TIME (§ 3b) at codexFactory `main` `2e744d4bfcad3e84759c86d5df0a2969c930d10c`
and at #318's head merged with THAT main, `8effa57a0814dceb1edc0477d5d67c8bfcf9dfac`,
because a `main` that moves three times in an afternoon leaves earlier transcripts
unreproducible. ALL READ-ONLY: every clone is local, every merge is local and pushed
nowhere, the measurement clones carry a deliberately unusable push URL, and no byte of
codexFactory is written by this packet.
Measured by: lane `openxfactory-2` (display `openXfactory-2`), sessions 504bd370
(§§ 1-3a) and a25e6327 (§ 3b and the commit)
Ruling this packet acts on: Brett Heap, 2026-09-10 ~14:0xZ, verbatim **"go A,
ratify the disposition entry as encoded"**, recorded on openxFactory #745
(comment 5619833296) and codexFactory #232 (comment 5619832944).

Every block below is copied from a terminal in this lane. Where a line is
elided it is marked `…`, and nothing is elided from a totals line, a verdict
line or an exit code. Absolute scratch paths are shortened to `<…>`. The pinned
CLI is `@fission-ai/openspec@1.12.0`, resolved by content address on every run,
with its 80-package closure installed through the committed lockfile:

```
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (<…>/node_modules/.bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
openspec-cli-pin: dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages); lockfile_integrity sha512-aw5lIN45tQq2WZll… verified; installed with `npm ci --ignore-scripts`
```

**What is being proved, in four sentences.** That the finding this entry
accepts is REAL and quoted whole from the tool's own report (§ 1). That adding
the entry turns it from UNDISPOSITIONED into an ACCEPTED EXCEPTION on #318's
tree, with the tool's own totals unchanged (§ 2). That the entry is invisible —
neither applied nor stale — on openxFactory's own tree, which is the property
this repository's required gate depends on (§ 4). And that the entry is STALE on
codexFactory `main` TODAY, because #318 has not merged — a live coupling that
decides a sequence, measured rather than predicted (§ 3). All four of those runs
were RE-TAKEN at commit time against a `main` that had moved again, with the same
verdicts and the transcript that matches the committed YAML byte for byte (§ 3b).

---

## 0. The trees

| tree | commit | identity (`git config --get remote.origin.url`, basename) |
| --- | --- | --- |
| codexFactory, PR #318 head | `32743fb7ebe0a89dc4a5ab0b53396530cf2d9ee5` | `codexFactory` |
| codexFactory, `main` (§ 3, first) | `0dfed9a483ff861ebaa9af5debfd34f675467ac3` | `codexFactory` |
| codexFactory, `main` after PR #339 (§ 3, again) | `9b1b0a21be4440639107335cf87f755beca1ecbd` | `codexFactory` |
| codexFactory, #318 head MERGED with that main (§ 3a) | `89ee5e84dce6da343e05bb03933fe745c0704549` | `codexFactory` |
| codexFactory, `main` at commit time (§ 3b) | `2e744d4bfcad3e84759c86d5df0a2969c930d10c` | `codexFactory` |
| codexFactory, #318 head MERGED with THAT main (§ 3b) | `8effa57a0814dceb1edc0477d5d67c8bfcf9dfac` | `codexFactory` |
| openxFactory, this branch | `change/disposition-codexfactory-floor-relocation-retitle` off `3b45c037` | `openxFactory` |

The org move of 2026-09-09 does not change the identity: `remote.origin.url` is
`git@github.com:codeXfactory/codexFactory.git` and the basename the verifier
reads is `codexFactory`, the same string the four standing entries use.

**The invocation is codexFactory's own.** `.github/workflows/validate.yml`
checks openxFactory out at `stack.yaml`'s `xfactory.contract_ref` into
`.openxfactory-pin`, exports `OPENXFACTORY_ROOT` to it, and
`scripts/validate-docs.sh` runs
`python3 "$OPENX/scripts/validate-openspec-cli-pin.py" --repo "$REPO_ROOT" --all --no-cache`
(the `--no-cache` being CI-only). The runs below are that command with
`OPENXFACTORY_ROOT` = THIS clone, so a draft entry is tested end to end before
it lands.

---

## 1. BEFORE — codexFactory PR #318's tree, with the pin as it stood

```
$ python3 scripts/validate-openspec-cli-pin.py --all --repo <cdx-318> --cache-dir <pincache>
…
change/relocate-review-authority-floor
  ✗ [ERROR] repository-gate-floor/spec.md: MODIFIED "An automated floor regeneration only ever proposes" omits scenario(s) the current spec still has: "The human gate is unchanged". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
…
Totals: 26 passed, 3 failed (29 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (2 applied) — this run is NOT a clean tree:
  ✗→D add-regular-pr-council-clearance / merge-master-approval/spec.md
        …
  ✗→D amend-composition-selector-labelling / domain-hermes-content/spec.md
        …
openspec-cli-pin: the pinned CLI reported 1 failure(s) this pin does not disposition. The PIN held — this is a finding about the deltas, not about which tool ran.
  ✗ relocate-review-authority-floor / repository-gate-floor/spec.md: MODIFIED "An automated floor regeneration only ever proposes" omits scenario(s) the current spec still has: "The human gate is unchanged". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
  Remedy for each: FIX IT, or DISPOSITION IT in contracts/openspec-cli-pin.yaml with a canon citation (`cited_to:`, non-empty) and an authority (`ratified_by:`). An undispositioned ERROR is not a tolerated one, and a disposition with no citation is refused rather than read as 'none needed'.
EXIT=1
```

**Three facts are established here and none is decoration.**

1. **The `finding:` text in `contracts/openspec-cli-pin.yaml` is QUOTED FROM
   THIS RUN**, not transcribed from a report somebody else produced. The matcher
   compares the whole message after whitespace normalization
   (`normalized_finding`), keyed on `(repo, item, path, finding)`, so a
   paraphrase would have failed to match and gone stale in the same breath.
   The gate keys this one as: repo `codexFactory`, item
   `relocate-review-authority-floor`, path `repository-gate-floor/spec.md`,
   level `ERROR`.
2. **The two standing codexFactory entries were APPLIED on this same run**, so
   the mechanism was already working over this tree before this packet existed;
   only the third finding was undispositioned.
3. **The same finding is codexFactory's own CI verdict.** `validate` run
   [34481981940](https://github.com/codeXfactory/codexFactory/actions/runs/34481981940)
   on head `32743fb7` concluded `failure` reading it.

**Why this finding exists at all, in one sentence.** codexFactory PR #318
ARCHIVED `add-floor-regeneration-automation`, which PROMOTED the requirement
"An automated floor regeneration only ever proposes" into
`openspec/specs/repository-gate-floor/spec.md` carrying canon's scenario "The
human gate is unchanged" — and the ratified, still-ACTIVE
`relocate-review-authority-floor` holds a `## MODIFIED` block for that same
requirement whose scenario list carries "The human gate is whatever the
document's path routes to" instead
(`openspec/changes/relocate-review-authority-floor/specs/repository-gate-floor/spec.md:50`).
Nothing in either change moved: a promotion made a declared retitle visible to
a marker-blind check.

---

## 2. AFTER — codexFactory PR #318's tree, with the entry added

```
$ python3 scripts/validate-openspec-cli-pin.py --all --repo <cdx-318> --cache-dir <pincache>
…
Totals: 26 passed, 3 failed (29 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (3 applied) — this run is NOT a clean tree:
  ✗→D add-regular-pr-council-clearance / merge-master-approval/spec.md
        …
  ✗→D amend-composition-selector-labelling / domain-hermes-content/spec.md
        …
  ✗→D relocate-review-authority-floor / repository-gate-floor/spec.md
        MODIFIED "An automated floor regeneration only ever proposes" omits scenario(s) the current spec still has: "The human gate is unchanged". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
        why: The scenario is RETITLED AND RE-CONDITIONED, not dropped — canon's "The human gate is unchanged" becomes "The human gate is whatever the document's path routes to" — and the retitle is declared in the block itself with the reserved `Merged into` marker (codexFactory PR #339). `relocate-review-authority-floor` was ratified to make the floor document's review routing whatever ITS PATH routes to, so restoring the old title would reinstate the fixed human gate that relocation was ratified to replace, and would stand in the same block as its own successor.
        cited to: openspec/specs/doc-health/spec.md:1793 — the promoted `Merged into` marker requirement, written out in the exact form the codexFactory block uses; openspec/specs/doc-health/spec.md:1773 — "That shape is a retitle, whatever the marker calls it", the line that makes `Merged into` the instrument here and `Removed from canon` the wrong one; council LA-A1 — the ruling that reserved the marker forms; codexFactory PR #318 (change/archive-floor-regeneration-option-b, head 32743fb7) — the archive that promoted the requirement and thereby raised this finding; codexFactory PR #318 validate run 34481981940 (head 32743fb7, conclusion failure) — the consuming repository's own gate reading this finding at the pinned CLI; openspec/changes/disposition-codexfactory-floor-relocation-retitle/evidence/codexfactory-floor-relocation-2026-09-10.md — the measurement this entry rests on, before and after, on PR 318's tree and on codexFactory main; codexFactory openspec/changes/relocate-review-authority-floor/specs/repository-gate-floor/spec.md:15 — the reserved `Merged into` marker itself, in the block the finding names, LANDED on codexFactory main at 9b1b0a21 by codexFactory PR 339; the dated note is at that packet's tasks.md:384; codexFactory #232 (comment 5619832944) — the same ruling recorded on the consuming repository's own governing issue
        accepted by: Brett Heap, 2026-09-10, "go A, ratify the disposition entry as encoded" (https://github.com/opensoft/openxFactory/issues/745#issuecomment-5619833296)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 3 finding(s) are ACCEPTED EXCEPTIONS, named above.
EXIT=0
```

**RE-MEASURED AFTER A CORRECTION, AND THE BLOCK ABOVE IS THE RE-RUN.** The
first capture of this section named the sibling marker pull request as
codexFactory **#333**. That was WRONG and a reader would have followed it to the
wrong place: #333 is `change/advance-openxfactory-pin-b91af6ea`, the PIN
ADVANCE. The marker pull request is **#339**
(`change/relocate-floor-scenario-retitle-marker`), whose marker lands at
`openspec/changes/relocate-review-authority-floor/specs/repository-gate-floor/spec.md:15`
— read from the tree, not predicted. #339 has since MERGED (main
`9b1b0a21be4440639107335cf87f755beca1ecbd`, GitHub `merged_at`
2026-09-10T14:33:55Z, the merge commit's own committer date
2026-09-10T10:33:54-04:00), so the marker citation now names the LANDED commit
rather than a pull request's moving head. The entry's `why:` and its marker
citation were corrected and this section was RE-MEASURED rather than left
quoting a string the pin no longer carries — and the `cited to:` line printed
above is the one the COMMITTED pin renders, re-captured a second time in § 3b
after that final wording landed. A transcript that stopped matching the file it
transcribes would be the one kind of evidence this estate cannot use.

**`Totals:` IS IDENTICAL BEFORE AND AFTER — `26 passed, 3 failed (29 items)`.**
That is the honesty property working: the pin does not make the tool report
fewer failures. It records that three of them are accepted, prints each with its
reason, its citations and the human who granted it, and REFUSES TO CALL THE
RESULT CLEAN. The verdict is derived from the RECONCILED findings, not from the
CLI's exit code.

**No `pin-disposition-stale` over openxFactory's own pair on this run.**
`add-chain-attestation` and `add-composed-view-authoring` are absent from
codexFactory's corpus because they were never in it, and the run does not
confuse that with a change that archived.

---

## 3. codexFactory `main` — THE LIVE COUPLING, AND IT IS A REFUSAL

This is the measurement a reader would most want left out, so it is § 3 rather
than a footnote. It was taken first at main `0dfed9a4` and RE-TAKEN at
`9b1b0a21` after codexFactory PR #339 landed; both runs are below and § 3a
carries the re-take.

```
$ python3 scripts/validate-openspec-cli-pin.py --all --repo <cdx-main> --cache-dir <pincache>
…
Totals: 31 passed, 2 failed (33 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (2 applied) — this run is NOT a clean tree:
  ✗→D add-regular-pr-council-clearance / merge-master-approval/spec.md
        …
  ✗→D amend-composition-selector-labelling / domain-hermes-content/spec.md
        …
REFUSE pin-disposition-stale: the pin disposes findings this run did not produce:
  • relocate-review-authority-floor / repository-gate-floor/spec.md (repo codexFactory)

The condition each was granted for no longer occurs — typically because the change archived out of the `--all` corpus, or because the pinned CLI now words the finding differently. A suppression that outlives its condition is a standing exemption nobody re-read, so it is REFUSED rather than tolerated: delete the entry from `dispositions:` in contracts/openspec-cli-pin.yaml, in a change that says the condition is gone
EXIT=2
```

**AND THE BASELINE, so this is read as a coupling and not as a pre-existing
red.** The same tree, the same command, with the pin exactly as `origin/main`
carries it today:

```
$ python3 scripts/validate-openspec-cli-pin.py --all --repo <cdx-main> --cache-dir <pincache> --pin <origin/main's openspec-cli-pin.yaml>
Totals: 31 passed, 2 failed (33 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (2 applied) — this run is NOT a clean tree:
  …
OK openspec-cli-pin: … every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
EXIT=0
```

**WHY, exactly.** The scenario-currency check compares an active `## MODIFIED`
block against CANON. On codexFactory `main`, #318 is still OPEN, so
`openspec/specs/repository-gate-floor/spec.md` carries NO requirement "An
automated floor regeneration only ever proposes" at all — measured,
`grep -c` returns `0` — and `add-floor-regeneration-automation` is still an
ACTIVE change. With no canon scenario to compare against, the check raises
nothing, the entry matches no finding, and a whole-corpus run REFUSES rather
than passes. **That is the stale-refused property working exactly as designed**:
the mechanism will not let an exception outlive its condition, and it cannot
tell "not yet" from "no longer" — nor should one file try to.

**WHAT IT MEANS, AND IT IS AN ORDER RATHER THAN A DEFECT.** Nothing about this
touches openxFactory's own gate (§ 4). It constrains ONE act, in codexFactory,
and the constraint is now written into the entry's own `retires_when:`:

> codexFactory's DECLARED openxFactory PIN MUST NOT ADVANCE TO THIS CHANGE'S
> MERGE COMMIT BEFORE #318 MERGES.

The correct order is **#318 first, the pin advance second**. The coordination
point is codexFactory **#333** (`change/advance-openxfactory-pin-b91af6ea`),
which as it stands moves `stack.yaml`'s `xfactory.contract_ref` from `724a2a4f`
to `b91af6ea` for openxFactory #886 — **a commit BEFORE this change, so #333 as
written does not deliver this entry**, and a further advance is owed either way.
An early advance would red codexFactory `main` on this entry — loudly, by name,
with the remedy printed — which is the failure mode this estate prefers to a
silent one, but it is still avoidable by taking the two acts in the order
measured here.

### 3a. THE MARKER LANDED MID-AUTHORING, AND THE CLAIM WAS RE-RUN RATHER THAN ARGUED

The one thing this whole mechanism rests on is that the pinned CLI is BLIND to
the reserved `Merged into` marker. While this packet was being authored, the
sibling lane's **codexFactory PR #339 merged** — main
`9b1b0a21be4440639107335cf87f755beca1ecbd`, 2026-09-10T14:33:55Z — putting the
marker into the very block this entry accepts a finding against, at
`openspec/changes/relocate-review-authority-floor/specs/repository-gate-floor/spec.md:15`:

```
**Merged into `The human gate is whatever the document's path routes to` by relocate-review-authority-floor (2026-09-10):** `The human gate is unchanged` — a RETITLE AND RE-CONDITIONING, not a drop: the gate is no longer "unchanged" by definition once the document's path routes it; the scenario's substance survives under the new title.
```

**That is a falsification test arriving unasked, so it was taken.** #318's head
was merged with that main in a LOCAL clone (`89ee5e84`, pushed nowhere) and both
pins were run over it:

```
$ python3 scripts/validate-openspec-cli-pin.py --all --repo <cdx-318-merged> --cache-dir <pincache> --pin <origin/main's openspec-cli-pin.yaml>
…
Totals: 27 passed, 3 failed (30 items)
openspec-cli-pin: the pinned CLI reported 1 failure(s) this pin does not disposition. The PIN held — this is a finding about the deltas, not about which tool ran.
  ✗ relocate-review-authority-floor / repository-gate-floor/spec.md: MODIFIED "An automated floor regeneration only ever proposes" omits scenario(s) the current spec still has: "The human gate is unchanged". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
EXIT=1

$ python3 scripts/validate-openspec-cli-pin.py --all --repo <cdx-318-merged> --cache-dir <pincache>
…
Totals: 27 passed, 3 failed (30 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (3 applied) — this run is NOT a clean tree:
  …
OK openspec-cli-pin: … every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 3 finding(s) are ACCEPTED EXCEPTIONS, named above.
EXIT=0
```

**THE FINDING IS BYTE-IDENTICAL WITH AND WITHOUT THE MARKER**, checked by
comparing the two captures in code rather than by eye:

```
pre-marker  (#318 head 32743fb7): MODIFIED "An automated floor regeneration only ever proposes" omits scenario(s) the current spec still has: "The human gate is unchanged". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
post-marker (merged   89ee5e84): MODIFIED "An automated floor regeneration only ever proposes" omits scenario(s) the current spec still has: "The human gate is unchanged". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
BYTE-IDENTICAL: True
PIN finding == measured: True
```

The last line is `normalized_finding(entry["finding"]) == normalized_finding(measured)`
read out of the verifier's own module: the text this pin records is the text the
matcher will compare, on the tree codexFactory will actually validate.

**`Totals:` moved 29 → 30 items** because the marker's merge brought the rest of
codexFactory main with it (one more change in the corpus). The numbers that
matter did not move: 3 failed, 3 applied, **0 undispositioned**.

**AND THE STALENESS ON `main` SURVIVED THE MARKER TOO.** The same pair of runs
over codexFactory main at `9b1b0a21`: the pre-edit pin exits **0** with 2
applied; this pin exits **2**, `REFUSE pin-disposition-stale`, naming
`relocate-review-authority-floor / repository-gate-floor/spec.md (repo
codexFactory)`. The reason is unchanged and re-measured —
`grep -c "An automated floor regeneration only ever proposes"
openspec/specs/repository-gate-floor/spec.md` still returns `0` on main, #318
being still OPEN — so § 3's conclusion about the ORDER stands at the newer main.

---

### 3b. THE FINAL RE-MEASUREMENT — the trees as they stand at commit time, and the transcript that matches the committed file

The runs above were taken as the packet was written, against a `main` that has
since moved twice. **A record whose transcripts a reader cannot reproduce is
half a record**, so the whole pair was re-taken at commit time by a second
author in the same lane, on trees named by SHA, with the pin file exactly as
this branch commits it. Nothing below is elided from a totals line, a verdict
line, an exit code, or from the `cited to:` line — which is the one line that
proves the transcript and the committed YAML are the same text.

**The trees.** codexFactory `main` at
`2e744d4bfcad3e84759c86d5df0a2969c930d10c` (2026-09-10T14:49:20Z), which
carries the marker: `9b1b0a21` is an ancestor
(`git merge-base --is-ancestor` → yes) and the marker reads at
`openspec/changes/relocate-review-authority-floor/specs/repository-gate-floor/spec.md:15`.
And #318's head `32743fb7` MERGED with that main in a LOCAL clone at
`8effa57a0814dceb1edc0477d5d67c8bfcf9dfac`
(parents `32743fb7` and `2e744d4b`), pushed nowhere. **THE MERGE HAD ONE
CONFLICT AND IT IS DECLARED**: `README.md`, resolved `--ours` (#318's side).
Nothing under `openspec/` conflicted, and `openspec/` is the entire subject of
this gate — but a conflict resolved silently inside a measurement tree is a
thumb on the scale, so it is named. GitHub's own `refs/pull/318/merge`
(`ff23b2f0`) was fetched first and REJECTED for this purpose: it was computed
against main `950c9a68` at 13:20Z and does not carry the marker at all.

**BEFORE — the merged tree, with the pin as `origin/main` carries it today.**

```
$ python3 scripts/validate-openspec-cli-pin.py --all --repo <cdx-318-merged> --cache-dir <pincache> --pin <origin/main's openspec-cli-pin.yaml>
…
Totals: 26 passed, 3 failed (29 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (2 applied) — this run is NOT a clean tree:
  …
openspec-cli-pin: the pinned CLI reported 1 failure(s) this pin does not disposition. The PIN held — this is a finding about the deltas, not about which tool ran.
  ✗ relocate-review-authority-floor / repository-gate-floor/spec.md: MODIFIED "An automated floor regeneration only ever proposes" omits scenario(s) the current spec still has: "The human gate is unchanged". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
  Remedy for each: FIX IT, or DISPOSITION IT in contracts/openspec-cli-pin.yaml with a canon citation (`cited_to:`, non-empty) and an authority (`ratified_by:`). An undispositioned ERROR is not a tolerated one, and a disposition with no citation is refused rather than read as 'none needed'.
EXIT=1
```

**AFTER — the same tree, this branch's pin, IN THE GATE'S OWN CI FORM**
(`--repo … --all --no-cache`, the literal `scripts/validate-docs.sh` runs under
`CI`, with `OPENXFACTORY_ROOT` = this clone):

```
$ python3 scripts/validate-openspec-cli-pin.py --repo <cdx-318-merged> --all --no-cache
…
Totals: 26 passed, 3 failed (29 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (3 applied) — this run is NOT a clean tree:
  ✗→D add-regular-pr-council-clearance / merge-master-approval/spec.md
        …
  ✗→D amend-composition-selector-labelling / domain-hermes-content/spec.md
        …
  ✗→D relocate-review-authority-floor / repository-gate-floor/spec.md
        MODIFIED "An automated floor regeneration only ever proposes" omits scenario(s) the current spec still has: "The human gate is unchanged". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
        why: The scenario is RETITLED AND RE-CONDITIONED, not dropped — canon's "The human gate is unchanged" becomes "The human gate is whatever the document's path routes to" — and the retitle is declared in the block itself with the reserved `Merged into` marker, LANDED on codexFactory main at 9b1b0a21 by codexFactory PR #339. `relocate-review-authority-floor` was ratified to make the floor document's review routing whatever ITS PATH routes to, so restoring the old title would reinstate the fixed human gate that relocation was ratified to replace, and would stand in the same block as its own successor.
        cited to: openspec/specs/doc-health/spec.md:1793 — the promoted `Merged into` marker requirement, written out in the exact form the codexFactory block uses; openspec/specs/doc-health/spec.md:1773 — "That shape is a retitle, whatever the marker calls it", the line that makes `Merged into` the instrument here and `Removed from canon` the wrong one; council LA-A1 — the ruling that reserved the marker forms; codexFactory PR #318 (change/archive-floor-regeneration-option-b, head 32743fb7) — the archive that promoted the requirement and thereby raised this finding; codexFactory PR #318 validate run 34481981940 (head 32743fb7, conclusion failure) — the consuming repository's own gate reading this finding at the pinned CLI; openspec/changes/disposition-codexfactory-floor-relocation-retitle/evidence/codexfactory-floor-relocation-2026-09-10.md — the measurement this entry rests on, before and after, on PR 318's tree and on codexFactory main; codexFactory openspec/changes/relocate-review-authority-floor/specs/repository-gate-floor/spec.md:15 — the reserved `Merged into` marker itself, in the block the finding names, LANDED on codexFactory main at 9b1b0a21 by codexFactory PR 339; the dated note is at that packet's tasks.md:384; codexFactory #232 (comment 5619832944) — the same ruling recorded on the consuming repository's own governing issue
        accepted by: Brett Heap, 2026-09-10, "go A, ratify the disposition entry as encoded" (https://github.com/opensoft/openxFactory/issues/745#issuecomment-5619833296)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 3 finding(s) are ACCEPTED EXCEPTIONS, named above.
EXIT=0
```

**`Totals:` UNCHANGED — `26 passed, 3 failed (29 items)` on both sides.** One
finding moved from UNDISPOSITIONED to ACCEPTED and the tool's own count of
failures did not move a digit, which is the whole honesty property of this
mechanism.

**AND codexFactory `main`, THE SAME PAIR, AT THE SAME NEW SHA — STILL A
REFUSAL.** This is the measurement a reader would most want left out, so it is
re-taken rather than allowed to age out:

```
$ python3 scripts/validate-openspec-cli-pin.py --all --repo <cdx-main> --cache-dir <pincache> --pin <origin/main's openspec-cli-pin.yaml>
Totals: 30 passed, 2 failed (32 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (2 applied) — this run is NOT a clean tree:
  …
OK openspec-cli-pin: … every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
EXIT=0

$ python3 scripts/validate-openspec-cli-pin.py --repo <cdx-main> --all --no-cache
Totals: 30 passed, 2 failed (32 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (2 applied) — this run is NOT a clean tree:
  …
REFUSE pin-disposition-stale: the pin disposes findings this run did not produce:
  • relocate-review-authority-floor / repository-gate-floor/spec.md (repo codexFactory)

The condition each was granted for no longer occurs — typically because the change archived out of the `--all` corpus, or because the pinned CLI now words the finding differently. A suppression that outlives its condition is a standing exemption nobody re-read, so it is REFUSED rather than tolerated: delete the entry from `dispositions:` in contracts/openspec-cli-pin.yaml, in a change that says the condition is gone
EXIT=2
```

**WHY IT IS STALE THERE, READ OUT OF THE TOOL RATHER THAN INFERRED.** On the
merged tree the pinned CLI reports the item as `"valid": false` with an
`ERROR`; on `main` it reports THE SAME ITEM as `"valid": true` with an `INFO`,
and the gate only reconciles BLOCKING findings:

```
merged (8effa57a): {"id": "relocate-review-authority-floor", "type": "change", "valid": false,
  "issues": [{"level": "ERROR", "path": "repository-gate-floor/spec.md",
              "message": "MODIFIED \"An automated floor regeneration only ever proposes\" omits scenario(s) the current spec still has: \"The human gate is unchanged\". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them)."}]}

main (2e744d4b):  {"id": "relocate-review-authority-floor", "type": "change", "valid": true,
  "issues": [{"level": "INFO", "path": "repository-gate-floor/spec.md",
              "message": "Archive would refuse this delta: repository-gate-floor MODIFIED failed for header \"### Requirement: An automated floor regeneration only ever proposes\" - not found"}]}
```

The INFO says it in the tool's own words: on `main` the header is **not
found**, because #318 has not merged and canon carries no such requirement to
compare a MODIFIED block against (`grep -c` over
`openspec/specs/repository-gate-floor/spec.md` returns `0` on `main` and `1` on
the merged tree). No blocking finding, nothing for the entry to match, and a
whole-corpus run refuses rather than passes. § 3's conclusion about the ORDER
therefore stands unchanged at the newest `main`: **#318 first, codexFactory's
pin advance second.**

**AND THE PIN'S RECORDED TEXT IS THE TEXT THE MATCHER WILL COMPARE**, checked
by importing the verifier's own module rather than by eye:

```
$ python3 -c "…import scripts/validate-openspec-cli-pin.py as m; compare the entry with the CLI's own --json record…"
pin finding == measured message (raw bytes): True
normalized_finding(pin) == normalized_finding(measured): True
pin path == measured path: True
pin level == measured level: True
```

**AND THE MARKER STILL CHANGES NOTHING ABOUT THE TOOL.** The pre-marker capture
of this item (§ 1, #318's tree at `32743fb7` before `9b1b0a21` existed) and the
post-marker capture above differ in no character of `message`, `path` or
`level`; the JSON records differ only in the CLI's own `durationMs`.

---

## 4. openxFactory's own tree — the gate's LITERAL invocation

`.github/workflows/openspec-cli-pin-gate.yml` runs this, with no `--repo` and
no cache:

```
$ python3 scripts/validate-openspec-cli-pin.py --all --no-cache
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (<…>/node_modules/.bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
…
Totals: 101 passed, 2 failed (103 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied) — this run is NOT a clean tree:
  ✗→D add-chain-attestation / signed-execution-chain/spec.md
        …
        accepted by: Brett Heap, 2026-09-05, "take exit 2"
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md
        …
        accepted by: Brett Heap, 2026-09-05, "take exit 2"
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
EXIT=0
```

**THIS IS THE RESULT THE PACKET LIVES OR DIES BY.** Exit 0. openxFactory's own
two applied, by name, with Brett's *"take exit 2"* beside them. **ALL THREE
codexFactory entries appear in NEITHER list — not applied, and NOT STALE** —
including the one added here, and including the one § 3 shows refusing on
codexFactory's own tree. Had any of them gone stale here, this repository's own
required gate would be red on every pull request for a finding in a tree it
does not own.

**The reason is one line, not a promise.**
`scripts/validate-openspec-cli-pin.py:1748`:

```python
in_scope = [entry for entry in dispositions if entry.get("repo") == identity]
```

`keyed` is built from `in_scope`; `applied` is filled only from `keyed` hits;
`stale` is `[entry for key, entry in keyed.items() if key not in matched]`. An
entry whose `repo:` differs from the validated tree's identity is in neither
collection by construction, and there is no branch by which it could enter one.

**`Totals:` reads 103 items**, up from the 95 the precedent measured on
2026-09-05, because the active corpus has grown — this packet's own change
directory is one of them. The number that matters is unchanged: **0
undispositioned**.

---

## 5. The pinned CLI on this packet — `skip_specs` accepted, not assumed

```
$ <pincache>/node_modules/.bin/openspec --version
1.12.0
$ OPENSPEC_TELEMETRY=0 <pincache>/node_modules/.bin/openspec validate disposition-codexfactory-floor-relocation-retitle --strict
Change 'disposition-codexfactory-floor-relocation-retitle' is valid
ℹ [INFO] file: skip_specs is set in .openspec.yaml: change declares no spec-level behavior changes, zero deltas accepted
EXIT=0
```

The declaration is READ and reported at INFO, not silently tolerated. `1.12.0`
defines it at `dist/core/change-metadata/schema.js`
(`skip_specs: z.boolean().optional()`) and enforces its other half — a change
declaring `skip_specs` that ALSO carries a file under `specs/` is refused
`CHANGE_SKIP_SPECS_CONFLICT`. This is the SECOND use of `skip_specs` in this
corpus; the first was `disposition-codexfactory-declared-renames`, whose
evidence records the same check and the fact that a rollback to `1.2.0` would
not honour the key.

---

## 6. The suites

```
$ python3 -m pytest tests/openspec_cli_pin tests/pin_registrations tests/sequenced_after -q -p no:cacheprovider
485 passed in 45.93s
EXIT=0

$ python3 -m pytest tests/ -q -k "pin or disposition" -p no:cacheprovider
1 failed, 1124 passed, 6 skipped, 10118 deselected, 6 warnings, 58 subtests passed in 275.88s (0:04:35)
FAILED tests/ideation-dashboard/test_snapshot.py::test_find_validator_locates_pinned_checkout
```

**THE ONE FAILURE IS THE CHECKOUT'S NAME AND NOT THIS PACKET, and it is named
rather than waved away.** `test_find_validator_locates_pinned_checkout` fails in
ANY checkout whose directory is not called `openxFactory`; this lane works in a
clone called `oxf-dispo`, and the precedent's evidence records the identical
failure for the same reason in a worktree called `oxf-disp`. **TEN OTHER
FAILURES WERE MEASURED AND THEN REMOVED BY INITIALIZING A SUBMODULE**, which is
recorded because the first reading looked worse than the tree was: every
`tests/openxwallet_pin/` and `tests/trust-anchor/` failure came from a fresh
clone with `openXwallet` uninitialized. After
`git submodule update --init openXwallet` (checked out at `f3eb929b`,
`wallet-v1.5`), `pytest tests/openxwallet_pin tests/trust-anchor -q` reads
`135 passed`. The authority for the whole suite is CI on this branch's head, and
it is reported on the pull request.

```
$ python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#898'
wrote tests/sequenced_after/corpus-ledger.yaml (194 rows, 1 moved by #898).
  - disposition-codexfactory-floor-relocation-retitle
```

**Exactly one row moved**, this change's own:
`disposition-codexfactory-floor-relocation-retitle: {state: active, class: sole,
declares: [], depth: 0, prose: false, moved_by: "#898", moved_on: "2026-09-10"}`.
`class: sole` because a change with no spec delta writes no requirement key and
can therefore share none; `declares: []` is the positive ROOT CLAIM the
proposal's front matter makes, and it is true — nothing in this corpus has to
land before this delta-less packet. No MOVEMENT LOG entry is owed: a row ADDED
is a move the row diff itself states.

```
$ python3 scripts/validate-pin-registrations.py
OK openspec-cli-pin: 5 disposition(s) carry 29 citation(s) naming 24 referent(s) — 12 name a path in this tree, 0 a URL, 6 a forge reference, 6 a path qualified to another repository; 5 citation(s) name no machine referent; 10 line(s) the two readers read differently (8 truncated at a `#`, 2 read as a single-key mapping), classified from the line; every in-tree path resolves
OK openspec-cli-pin: `contracts/openspec-cli-pin.yaml` is present, its `consumer_entrypoint: scripts/validate-openspec-cli-pin.py` resolves, and the row's `consumption_rule` names that same path
OK contracts/manifest.yaml: 1 pin registration(s) cohere
EXIT=0
```

**Four of this entry's citation lines are among the ten the two readers read
differently, and that is DISCLOSED rather than hidden.** `yaml.safe_load`
truncates a plain scalar at a ` #`, so `codexFactory PR #318 …` comes back as
`codexFactory PR`; the pin's own line-based reader — the one the gate and the
report use — takes the whole line, and `validate-pin-registrations.py`
classifies the LINE and WARNs about the divergence. The repair is to quote those
scalars, which that checker's own docstring calls a GOVERNED act with a
re-vendor cost in three sibling repositories, so this packet does not take it:
it writes its citations in the file's existing house style and leaves the
standing WARN where its owner can see it. One avoidable case WAS removed — a
` #318` inside a gloss became `PR 318` — because a gloss costs nothing to
reword.

**The citation arm of `validate-pin-registrations.py` OPENED THIS FILE, and it
found it missing first.** On the run before this file existed, the required
suite failed with

```
AssertionError: citations naming paths that are gone: ['openspec/changes/disposition-codexfactory-floor-relocation-retitle/evidence/codexfactory-floor-relocation-2026-09-10.md']
```

which is `check_citations` (issue #840) doing precisely what it was written for
— a citation nobody can open is a suppression with a footnote — against a
citation this packet had written before the file it names. Recorded because a
gate that catches its author is worth more evidence than one that never fires.

Two tests in `tests/openspec_cli_pin/test_openspec_cli_pin.py` moved with this
packet, both DELIBERATELY and both recorded in `design.md` § 4: the
count-pinning test 4 → 5 keeping its per-repository split, and
`test_every_real_disposition_cites_canon_and_names_who_granted_it` tightened
from two shared literals to PER-ITEM maps of the measurement each entry rests on
and the word each was granted by.

---

## 7. What this evidence does NOT claim

* **It does not claim codexFactory #318 goes green.** This entry removes ONE
  reason its `validate` is red. Whether others remain is codexFactory's
  verdict, on codexFactory's tree.
* **It does not claim the marker made any difference to the tool** — and § 3a
  measures that it made none. codexFactory PR #339 LANDED the reserved
  `Merged into` marker on main `9b1b0a21` while this packet was authored; the
  disposition cites it at its path and was lawful without it, because the marker
  is `doc-health`'s instrument and the pinned CLI is blind to it either way.
* **It does not claim codexFactory's pin has advanced.** It has not, and § 3 is
  the reason it must not advance before #318 merges.
* **It does not claim the disagreement is resolved.**
  `Fission-AI/OpenSpec#1793` — *"`validate --strict`: scenario-currency check
  has no way to declare a deliberate scenario rename, so a narrowing reads as an
  omission"* — was filed 2026-09-05 and is not fixed. When a release honours a
  declared rename, the next pin bump re-derives the list against it, all five
  entries are matched by nothing, and the pin REFUSES `pin-disposition-stale`
  until every one is deleted. That is how these exceptions are meant to end, and
  the reason none of them is written to be permanent.
