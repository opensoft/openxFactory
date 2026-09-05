# codexFactory's two declared renames, dispositioned — the runs, verbatim

Status: record
Kind: report
Measured on: 2026-09-05
Base: openxFactory `main` at `b6804991`. Branch
`change/disposition-codexfactory-declared-renames`, worktree of that commit.
The consuming tree measured is codexFactory at `b2a6af34`, the head of
codexFactory PR #216 (`prepare-openspec-1.12-readiness`), read-only.
Measured by: lane `codexfactory-1`
Ruling this packet acts on: Brett Heap, 2026-09-05, verbatim **"use recommended
name, go on 3 repo shape"** — accepting for codexFactory's pair the same exit he
ruled **"take exit 2"** for openxFactory's own pair the same day, and naming the
three-step order this packet is step 2 of.
Pull request: openxFactory #697.

Every block below is copied from a terminal in this lane. Where a line is
elided it is marked `…` and nothing is elided from a totals line, a verdict
line or an exit code. The pinned CLI is `@fission-ai/openspec@1.12.0`, resolved
by content address on every run.

**What is being proved, in one sentence.** That two entries naming a repository
this one does not own can be added to `contracts/openspec-cli-pin.yaml` — a file
openxFactory's own required gate reads on every pull request — and be APPLIED on
codexFactory's tree while being **neither applied nor stale** on openxFactory's.

---

## 0. The trees

| tree | commit | identity (`git config --get remote.origin.url`, basename) |
| --- | --- | --- |
| codexFactory, PR #216 head | `b2a6af34ae73c355570ae4a8853a195c18475a34` | `codexFactory` |
| openxFactory, this branch | `change/disposition-codexfactory-declared-renames` off `b6804991` | `openxFactory` |

---

## 1. BEFORE — codexFactory's tree, with the pin as it stood

```
$ python3 scripts/validate-openspec-cli-pin.py --all --repo <cdx-61> --cache-dir <pincache>
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (…/bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
-> …/bin/openspec validate --all --strict --json  (in …/cdx-61)
change/add-regular-pr-council-clearance
  ✗ [ERROR] merge-master-approval/spec.md: MODIFIED "Bounded autonomous surface" omits scenario(s) the current spec still has: "A human-authored pull request is never auto-approved". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
change/amend-composition-selector-labelling
  ✗ [ERROR] domain-hermes-content/spec.md: MODIFIED "The merge-readiness holder composition is declared from governed sources" omits scenario(s) the current spec still has: "Current aliases do not masquerade as immutable versions". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
…
Totals: 23 passed, 2 failed (25 items)
openspec-cli-pin: the pinned CLI reported 2 failure(s) this pin does not disposition. The PIN held — this is a finding about the deltas, not about which tool ran.
  ✗ add-regular-pr-council-clearance / merge-master-approval/spec.md: MODIFIED "Bounded autonomous surface" omits scenario(s) the current spec still has: "A human-authored pull request is never auto-approved". …
  ✗ amend-composition-selector-labelling / domain-hermes-content/spec.md: MODIFIED "The merge-readiness holder composition is declared from governed sources" omits scenario(s) the current spec still has: "Current aliases do not masquerade as immutable versions". …
  Remedy for each: FIX IT, or DISPOSITION IT in contracts/openspec-cli-pin.yaml with a canon citation (`cited_to:`, non-empty) and an authority (`ratified_by:`). An undispositioned ERROR is not a tolerated one, and a disposition with no citation is refused rather than read as 'none needed'.
EXIT=1
```

**Two facts are established here and neither is decoration.** First, the finding
text in `contracts/openspec-cli-pin.yaml` is QUOTED FROM THIS RUN and not
transcribed from a report somebody else produced — the matcher compares the
whole message after whitespace normalization, so a paraphrase would have failed
to match and gone stale. Second, openxFactory's OWN two dispositions were
already in the pin at this point and this run **did not refuse
`pin-disposition-stale`** over them: they were out of scope on this tree before
this packet existed. The mechanism worked across the boundary in the direction
that costs nothing before it was asked to work in the direction that does.

---

## 2. AFTER — codexFactory's tree, with the two entries added

```
$ python3 scripts/validate-openspec-cli-pin.py --all --repo <cdx-61> --cache-dir <pincache>
…
Totals: 23 passed, 2 failed (25 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (2 applied) — this run is NOT a clean tree:
  ✗→D add-regular-pr-council-clearance / merge-master-approval/spec.md
        MODIFIED "Bounded autonomous surface" omits scenario(s) the current spec still has: "A human-authored pull request is never auto-approved". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
        why: A RETITLE AND NARROWING declared with the reserved `Merged into` marker — converted from a `Removed from canon` marker by codexFactory PR #216 on Brett Heap's 2026-09-05 ruling, because canon holds that a block adding a title canon does not carry is a retitle whatever the marker calls it. A human-authored pull request is still never approved by the tier-1 envelope alone; approval may now ALSO come from tier-2 council clearance pinned to the candidate's exact head SHA, which is the BREAKING change that packet declares. Copying the old scenario back would reinstate a bar the change was ratified to lower.
        cited to: openspec/specs/doc-health/spec.md:1770 — the promoted `Merged into` marker requirement, whose written form the codexFactory block uses; openspec/specs/doc-health/spec.md:1750 — "That shape is a retitle, whatever the marker calls it", the line that makes `Merged into` the right instrument here and `Removed from canon` the wrong one; council LA-A1 — the ruling that reserved the marker forms; codexFactory PR #216 (prepare-openspec-1.12-readiness, head b2a6af34) — the packet that converted the marker and measured what survived; codexFactory openspec/changes/prepare-openspec-1.12-readiness/evidence/openspec-1.12-readiness-2026-09-05.md — the measurement, `Totals: 23 passed, 2 failed (25 items)`, and § "The two refusals"; codexFactory openspec/changes/add-regular-pr-council-clearance/specs/merge-master-approval/spec.md:139 — the marker itself, in the block the finding names
        accepted by: Brett Heap, 2026-09-05, "use recommended name, go on 3 repo shape"
  ✗→D amend-composition-selector-labelling / domain-hermes-content/spec.md
        MODIFIED "The merge-readiness holder composition is declared from governed sources" omits scenario(s) the current spec still has: "Current aliases do not masquerade as immutable versions". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
        why: The scenario is RETITLED to "A selector is labelled for what it is, and none masquerades as an immutable revision", declared in the block with the reserved `Merged into` marker on Brett Heap's 2026-08-31 ruling that the old title's THEN clause needed a reading to stay true after the roster model-pin flip. The retitle restates the THEN for both exact identifiers and aliases so canon states the rule directly; restoring the old title would put back the clause the ruling found required a reading.
        cited to: openspec/specs/doc-health/spec.md:1770 — the promoted `Merged into` marker requirement, whose written form the codexFactory block uses; openspec/specs/doc-health/spec.md:1750 — "That shape is a retitle, whatever the marker calls it"; council LA-A1 — the ruling that reserved the marker forms; codexFactory hermes/domain/review-councils/records/2026-08-31-enrolled-roster-model-pin-flip.md §5.1/§12.0 — Brett Heap's 2026-08-31 ruling, the reason for the retitle; codexFactory PR #216 (prepare-openspec-1.12-readiness, head b2a6af34) — the packet that measured what survived; codexFactory openspec/changes/amend-composition-selector-labelling/specs/domain-hermes-content/spec.md:19 — the marker itself, in the block the finding names
        accepted by: Brett Heap, 2026-09-05, "use recommended name, go on 3 repo shape"
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
EXIT=0
```

**`Totals:` is IDENTICAL before and after — `23 passed, 2 failed (25 items)`.**
That is the honesty property working: the pin does not make the tool report
fewer failures, it records that two of them are accepted, prints each with its
reason, its citations and the human who granted it, and refuses to call the
result clean. The verdict is derived from the RECONCILED findings, not from the
CLI's exit code.

**No `pin-disposition-stale` over openxFactory's pair.** `add-chain-attestation`
and `add-composed-view-authoring` are absent from codexFactory's corpus because
they were never in it, and the run does not confuse that with a change that
archived.

---

## 3. openxFactory's own tree — the gate's LITERAL invocation

`.github/workflows/openspec-cli-pin-gate.yml` runs this, with no `--repo` and no
cache:

```
$ python3 scripts/validate-openspec-cli-pin.py --all --no-cache
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (/tmp/openspec-cli-pin-jzoo7l9d/prefix/bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
-> /tmp/openspec-cli-pin-jzoo7l9d/prefix/bin/openspec validate --all --strict --json  (in …/oxf-disp)
…
Totals: 93 passed, 2 failed (95 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied) — this run is NOT a clean tree:
  ✗→D add-chain-attestation / signed-execution-chain/spec.md
        MODIFIED "A gate validates the short chain as a hash-linked chain" omits scenario(s) the current spec still has: "a tranche-two link does not exist yet". …
        accepted by: Brett Heap, 2026-09-05, "take exit 2"
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md
        MODIFIED "Composed views are read-only with a repository jump" omits scenario(s) the current spec still has: "Gate verbs hide on a composed view". …
        accepted by: Brett Heap, 2026-09-05, "take exit 2"
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
EXIT=0
```

**THIS IS THE RESULT THE PACKET LIVES OR DIES BY.** Exit 0. Its own two
applied, by name, with Brett's *"take exit 2"* beside them. The two codexFactory
entries appear in NEITHER list — not applied, and **not stale**. Had they gone
stale, this repository's own required gate would be red on every pull request
for a finding in a tree it does not own.

**The reason is one line, not a promise.**
`scripts/validate-openspec-cli-pin.py:1145`:

```python
in_scope = [entry for entry in dispositions if entry.get("repo") == identity]
```

`keyed` is built from `in_scope`; `applied` is filled only from `keyed` hits;
`stale` is `[entry for key, entry in keyed.items() if key not in matched]`. An
entry whose `repo:` differs from the validated tree's identity is in neither
collection by construction, and there is no branch by which it could enter one.

**`Totals:` reads 95 items, not the bump's 90**, because the active corpus has
grown since #677 measured it — this packet's own change directory is one of
them. The number that matters is unchanged: **0 undispositioned**.

---

## 4. The pinned CLI on this packet — `skip_specs` accepted, not assumed

```
$ <pincache>/bin/openspec --version
1.12.0
$ OPENSPEC_TELEMETRY=0 <pincache>/bin/openspec validate disposition-codexfactory-declared-renames --strict
Change 'disposition-codexfactory-declared-renames' is valid
ℹ [INFO] file: skip_specs is set in .openspec.yaml: change declares no spec-level behavior changes, zero deltas accepted
EXIT=0
```

The declaration is READ and reported at INFO, not silently tolerated. `1.12.0`
defines it at `dist/core/change-metadata/schema.js`
(`skip_specs: z.boolean().optional()`) and enforces its other half — a change
declaring `skip_specs` that ALSO carries a file under `specs/` is refused
`CHANGE_SKIP_SPECS_CONFLICT`.

**`1.2.0` DOES NOT KNOW THE KEY, CHECKED RATHER THAN ASSERTED.** The rollback
artifact was fetched and its digests recomputed in this lane, and both equal the
values the pin's `rollback:` block records:

```
$ curl -sL -o openspec-1.2.0.tgz https://registry.npmjs.org/@fission-ai/openspec/-/openspec-1.2.0.tgz   # 204,816 bytes
sha512-2XDmPZcVY0Bs014lP9aoxe3VoEU8hFvqaBFxQaiJO2nhC8vTKCyo6sT/5YpQcOTfR/a64Hht2anTyqLR4eNhlg==
0fd5333520c8846f0ac51727379b8812e2f13c1b
$ grep -rn "skip_specs" package/
$ ls package/dist/core/change-metadata
ls: cannot access 'package/dist/core/change-metadata': No such file or directory
```

The string `skip_specs` occurs NOWHERE in `1.2.0`, and it has no change-metadata
schema to read one from. (`skipSpecs` does occur — twice, in
`dist/core/archive.js` — but it is an ARCHIVE OPTION passed in code, not a
marker read from `.openspec.yaml`, and it is not the same thing.)

**WHAT THAT DOES AND DOES NOT ESTABLISH.** It establishes that `1.2.0` CANNOT
honour this packet's `skip_specs: true`: a reader cannot act on a key its bytes
never mention. It does NOT establish what `1.2.0` then reports — that was not
measured, because running it would need its ten unpinned dependencies resolved
and this lane declined to install an unpinned tree in order to predict a verdict
nobody is asking for. So the fact recorded is the fact checked: a rollback to
`1.2.0` loses the dispositions AND loses the honouring of this change's
zero-delta declaration, and the second half is a cost the next person to
consider a rollback should find written down rather than discover.

**This is the first use of `skip_specs` in this corpus** (`grep -rn skip_specs`
over the tree returned nothing before this packet). It is recorded because a
first of this kind should be noticed: it is a DECLARATION that a change changes
no requirement, checkable and reported, not a way of not answering the question.

---

## 5. The suites

```
$ python3 -m pytest tests/openspec_cli_pin tests/sequenced_after -q -p no:cacheprovider
255 passed in 11.49s
EXIT=0
```

**93 of those are `tests/openspec_cli_pin`, against 92 on `origin/main`.** The
net is +1 because the count-pinning test is REPLACED by a tightened one — the
per-repository split rather than a single-repository set — and a second test is
added for the out-of-scope property proven in § 3.

```
$ python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#697'
wrote tests/sequenced_after/corpus-ledger.yaml (174 rows, 1 moved by #697).
  - disposition-codexfactory-declared-renames
```

**Exactly one row moved**, this change's own:
`disposition-codexfactory-declared-renames: {state: active, class: sole,
declares: absent, prose: false, moved_by: "#697", moved_on: "2026-09-05"}`.
`class: sole` because a change with no spec delta writes no requirement key and
can therefore share none.

The full suite is recorded in § 6.

---

## 6. Full suite

**The authority is CI, and CI is green.** `pytest-suite` on this branch's head
`1525980c`:

```
pytest-suite	pass	22m30s	https://github.com/opensoft/openxFactory/actions/runs/33987829523
```

All nine required checks pass on that commit — `openspec-cli-pin`,
`pytest-suite`, `merge-master-approval`, `signed-execution-chain-gate`,
`clearing-dispatch-gate`, `wallet-validation`, `openreposhape-pin`,
`release-tag-gate`, `lane-line`.

Locally, in this lane's worktree:

```
$ python3 -m pytest tests/ -q -m "not postgres" -p no:cacheprovider
4 failed, 9615 passed, 36 skipped, 338 deselected, 9 warnings, 61 subtests passed in 2104.36s (0:35:04)
FULL_SUITE_EXIT=1
```

**All four are the environment, and each is checked rather than waved away.**
None touches a file this packet edits.

* `tests/ideation-dashboard/test_snapshot.py::test_find_validator_locates_pinned_checkout`
  fails in ANY checkout whose directory is not named `openxFactory` — this lane
  works in a worktree named `oxf-disp` — which the workflow header documents.
  **Reproduced on a clean `origin/main` worktree in the same session**, where it
  fails identically with `find_validator(...) is None`.
* `tests/hermes_runtime_contracts/test_validator_cli.py::test_candidate_mode_on_the_real_repository_requires_domain_mirrors`
  and `…::test_release_mode_field_is_preserved_on_the_real_repository[…]` (two
  parameterizations) fail with
  `subprocess.TimeoutExpired: … 'validate-hermes-runtime-contracts.py' … timed
  out after 30 seconds`. That is a WALL-CLOCK budget on a host carrying a load
  average of 20–24 from other lanes' suites, not a verdict about the corpus.
  **Re-run in isolation on this branch, 26 of 27 pass** and only the
  `--require-realization` parameterization times out again; the same test also
  fails on the clean `origin/main` worktree.

The measurement recorded is therefore: **9,615 local passes, four
host-attributable failures reproduced off this branch, and a green CI run of the
same suite on the same commit.**

---

## 7. What this evidence does NOT claim

* **It does not claim codexFactory's gate is wired.** It is not. Step 3
  (`adopt-openspec-cli-pin-gate`, in codexFactory) does that, with the
  `stack.yaml` re-pin to an openxFactory commit at or after this change's merge.
  The runs above were issued from an openxFactory checkout with `--repo`, which
  is how a consuming tree is measured before it owns the leg.
* **It does not claim the two codexFactory changes are near archive.** Both
  carry `Status: draft` and their ratification is Brett's. When either archives,
  **codexFactory's** run refuses `pin-disposition-stale` until its entry is
  deleted — which is the mechanism forcing a re-reading, and is stated in each
  `retires_when:`.
* **It does not claim the disagreement is resolved.** Exit 3 — teaching
  1.12.0's scenario-currency check to read the reserved marker forms — remains
  drafted and unfiled in #677's packet. Filing it would retire all four entries
  at once. Four standing exceptions are the price of not having filed it.
