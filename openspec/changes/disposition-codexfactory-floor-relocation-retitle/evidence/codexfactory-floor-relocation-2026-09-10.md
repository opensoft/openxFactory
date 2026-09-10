# codexFactory's floor-relocation retitle, dispositioned — the runs, verbatim

Status: record
Kind: report
Measured on: 2026-09-10
Base: openxFactory `main` at `3b45c037`, in a FRESH CLONE at branch
`change/disposition-codexfactory-floor-relocation-retitle`. The consuming trees
measured are codeXfactory/codexFactory at `32743fb7ebe0a89dc4a5ab0b53396530cf2d9ee5`
(the head of PR #318, `change/archive-floor-regeneration-option-b`) and
codeXfactory/codexFactory `main` at `0dfed9a483ff861ebaa9af5debfd34f675467ac3`,
BOTH READ-ONLY CLONES: no byte of codexFactory is written by this packet.
Measured by: lane `openxfactory-2` (display `openXfactory-2`), session 504bd370
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
decides a sequence, measured rather than predicted (§ 3).

---

## 0. The trees

| tree | commit | identity (`git config --get remote.origin.url`, basename) |
| --- | --- | --- |
| codexFactory, PR #318 head | `32743fb7ebe0a89dc4a5ab0b53396530cf2d9ee5` | `codexFactory` |
| codexFactory, `main` | `0dfed9a483ff861ebaa9af5debfd34f675467ac3` | `codexFactory` |
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
        why: The scenario is RETITLED AND RE-CONDITIONED, not dropped — canon's "The human gate is unchanged" becomes "The human gate is whatever the document's path routes to" — and the retitle is declared in the block itself with the reserved `Merged into` marker (codexFactory PR #333). `relocate-review-authority-floor` was ratified to make the floor document's review routing whatever ITS PATH routes to, so restoring the old title would reinstate the fixed human gate that relocation was ratified to replace, and would stand in the same block as its own successor.
        cited to: openspec/specs/doc-health/spec.md:1793 — the promoted `Merged into` marker requirement, written out in the exact form the codexFactory block uses; openspec/specs/doc-health/spec.md:1773 — "That shape is a retitle, whatever the marker calls it", the line that makes `Merged into` the instrument here and `Removed from canon` the wrong one; council LA-A1 — the ruling that reserved the marker forms; codexFactory PR #318 (change/archive-floor-regeneration-option-b, head 32743fb7) — the archive that promoted the requirement and thereby raised this finding; codexFactory PR #318 validate run 34481981940 (head 32743fb7, conclusion failure) — the consuming repository's own gate reading this finding at the pinned CLI; openspec/changes/disposition-codexfactory-floor-relocation-retitle/evidence/codexfactory-floor-relocation-2026-09-10.md — the measurement this entry rests on, before and after, on #318's tree and on codexFactory main; codexFactory openspec/changes/relocate-review-authority-floor/specs/repository-gate-floor/spec.md — the `Merged into` marker itself, in the block the finding names; codexFactory #232 (comment 5619832944) — the same ruling recorded on the consuming repository's own governing issue
        accepted by: Brett Heap, 2026-09-10, "go A, ratify the disposition entry as encoded" (https://github.com/opensoft/openxFactory/issues/745#issuecomment-5619833296)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 3 finding(s) are ACCEPTED EXCEPTIONS, named above.
EXIT=0
```

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
than a footnote.

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

The correct order is **#318 first, the pin advance second** (coordinated on
codexFactory #333). An early advance would red codexFactory `main` on this
entry — loudly, by name, with the remedy printed — which is the failure mode
this estate prefers to a silent one, but it is still avoidable by taking the
two acts in the order measured here.

---

## 4. openxFactory's own tree — the gate's LITERAL invocation

`.github/workflows/openspec-cli-pin-gate.yml` runs this, with no `--repo` and
no cache:

```
$ python3 scripts/validate-openspec-cli-pin.py --all --no-cache
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (/tmp/openspec-cli-pin-…/node_modules/.bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
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
$ python3 -m pytest tests/openspec_cli_pin tests/pin_registrations -q -p no:cacheprovider
215 passed in 17.42s
EXIT=0
```

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

```
$ python3 scripts/validate-pin-registrations.py
… (see § 7 for the full local check list)
```

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
* **It does not claim the `Merged into` marker is in place.** The sibling lane's
  codexFactory PR #333 adds it; the disposition cites it at its path and is
  lawful without it, because the marker is `doc-health`'s instrument and the
  pinned CLI is blind to it either way.
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
