# OpenSpec CLI pin bump 1.2.0 → 1.12.0 — measurement, 2026-09-05

Status: record
Kind: report
Measured on: 2026-09-05
Base: openxFactory `main` at `6f3301fa` — the landing of #673
(`prepare-openspec-1.12-readiness`). Branch
`change/bump-openspec-cli-pin-to-1.12`, worktree of that commit.
Measured by: lane `codexfactory-0d`
Ruling this packet acts on: Brett Heap, 2026-09-05, verbatim **"take exit 2"** —
exit 2 of the three #673's record enumerated: *carry a dispositioned exception
for the two*.

**THIS PACKET BUMPS THE PIN.** `contracts/openspec-cli-pin.yaml` moves from
`@fission-ai/openspec@1.2.0` (#667) to `1.12.0`, and the target-version evidence
the ratified requirement demands is this file.

---

## 1. The referent, recomputed over the real bytes

`npm pack @fission-ai/openspec@1.12.0`, then SHA-512 and SHA-1 recomputed in
this lane rather than copied from the registry's own output. **Had either
disagreed, the lane was instructed to refuse and would have.**

```
file      fission-ai-openspec-1.12.0.tgz   477,381 bytes   389 files
integrity sha512-oFE2Lj7WVSc87nSibk6qe9HjHIOlxhcPAXbPey44DlLvJzBl5+9BZVrNiozOwv++CQhW+MG0kuP1XLZ/uQrrWw==
shasum    c844543999f673cdd72445879b86a4abea4c07ef
tarball   https://registry.npmjs.org/@fission-ai/openspec/-/openspec-1.12.0.tgz
```

Both equal the values `npm` reports for the published artifact. The verifier
re-computes both on EVERY run, cache or no cache, before anything is installed —
the cache reuses only the INSTALL, and only from a directory named by and
stamped with the verified content address.

The previous referent is recorded in the pin as `rollback:`, in the pin's own
grammar:

```
version   1.2.0
integrity sha512-2XDmPZcVY0Bs014lP9aoxe3VoEU8hFvqaBFxQaiJO2nhC8vTKCyo6sT/5YpQcOTfR/a64Hht2anTyqLR4eNhlg==
shasum    0fd5333520c8846f0ac51727379b8812e2f13c1b
```

A rollback moves those four fields back TOGETHER and **deletes the dispositions
with them** — the two entries exist only because `1.12.0` raises findings
`1.2.0` does not, so a rollback that kept them would refuse
`pin-disposition-stale` on its first run.

---

## 2. Totals, verbatim

### BEFORE — the pinned `1.2.0` entrypoint, at `6f3301fa`, no diff

```
python3 scripts/validate-openspec-cli-pin.py --all --strict
Totals: 90 passed, 0 failed (90 items)
OK openspec-cli-pin: @fission-ai/openspec@1.2.0 verified against its content address and every target validated --strict clean
```

exit 0.

### AFTER — the pinned `1.12.0` entrypoint, this branch

```
python3 scripts/validate-openspec-cli-pin.py --all --strict
Totals: 89 passed, 2 failed (91 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied) — this run is NOT a clean tree:
  …
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
```

**exit 0, and `2 failed` is printed in the same output.** The raw total is
`89 passed, 2 failed (91 items)` — 91 rather than #673's 90 because this
packet's own change directory is the +1 — and it is shown, never hidden: the
tool derives its verdict from the RECONCILED findings and prints the CLI's own
totals line beside it, so nobody can mistake a dispositioned pass for a clean
tree. The two failures are the two dispositions and nothing else.

### CROSS-CHECK — the OLD pin over the NEW branch

```
python3 <1.2.0-era entrypoint> --all --strict --pin <1.2.0 pin>
Totals: 91 passed, 0 failed (91 items)
OK openspec-cli-pin: @fission-ai/openspec@1.2.0 verified against its content address and every target validated --strict clean
```

The diff introduces no finding at either version. `1.2.0` reads
prior-count-plus-one and zero failed; `1.12.0` reads prior-count-plus-one and
the same two failures it read before the diff.

### THE RAW SUCCESSOR, with no entrypoint at all

```
OPENSPEC_TELEMETRY=0 npx -y @fission-ai/openspec@1.12.0 validate --all --strict
✗ change/add-chain-attestation
✗ change/add-composed-view-authoring
Totals: 89 passed, 2 failed (91 items)
```

Identical. The entrypoint changes what the run MEANS, not what the tool SAYS.

---

## 3. The two dispositioned findings, printed by the run

```
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied) — this run is NOT a clean tree:
  ✗→D add-chain-attestation / signed-execution-chain/spec.md
        MODIFIED "A gate validates the short chain as a hash-linked chain" omits scenario(s) the current spec still has: "a tranche-two link does not exist yet". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
        why: The scenario is RENAMED AND RE-CONDITIONED, not dropped, and the rename is declared in the block itself with the reserved `Merged into` marker; restoring the old title would reinstate the very permission council LA-A1 was raised to close.
        cited to: openspec/specs/doc-health/spec.md:1770 — the promoted `Merged into` marker requirement, whose two written forms this block uses; council LA-A1 — the contradiction the tranche's re-conditioning was raised to close; openspec/changes/prepare-openspec-1.12-readiness/evidence/openspec-1.12-readiness-2026-09-05.md § "The two refusals" — the measurement and the refusal, #673; openspec/changes/add-chain-attestation/specs/signed-execution-chain/spec.md — the marker, in the block the finding names
        accepted by: Brett Heap, 2026-09-05, "take exit 2"
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md
        MODIFIED "Composed views are read-only with a repository jump" omits scenario(s) the current spec still has: "Gate verbs hide on a composed view". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
        why: "Gate verbs hide on a composed view" became "Tile-bound gate verbs hide on a composed view" because the same change deliberately ADMITS document creation there; this exact pair is the worked example canon uses to define the marker, so restoring the old title contradicts both the sibling scenario and the requirement that governs the form.
        cited to: openspec/specs/doc-health/spec.md:1770 — canon's worked example IS this rename, byte for byte; PR #444 — the landed change that declared the rename with the `Merged into` marker; council LA-A1 — the ruling that reserved the marker forms; openspec/changes/prepare-openspec-1.12-readiness/evidence/openspec-1.12-readiness-2026-09-05.md § "The two refusals" — the measurement and the refusal, #673
        accepted by: Brett Heap, 2026-09-05, "take exit 2"
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
```

Both are the same disagreement twice: `1.12.0`'s scenario-currency check is
BLIND to this estate's reserved narrowing marker
``**Merged into `<destination>` by <change-id> (<date>):**``, and demands the
restoration of two scenario titles that two ratified changes deliberately
narrowed. `doc-health`'s promoted marker requirement uses the composed-view pair
as its **worked example** at `openspec/specs/doc-health/spec.md:1770`. The
factual basis, the refusal, and the three exits are #673's record:
`openspec/changes/prepare-openspec-1.12-readiness/evidence/openspec-1.12-readiness-2026-09-05.md`
§ *The two refusals*.

**Neither is remedied and neither is hidden.** Each is declared with its owner,
which is what the ratified bump requirement asks for where a target version's
failures are pre-existing conditions.

---

## 4. The old binary on PATH is now REFUSED

The bump makes yesterday's global install the wrong tool, and the entrypoint
says so rather than running it:

```
$ openspec --version
1.2.0
$ python3 scripts/validate-openspec-cli-pin.py --all --strict --path-mode
REFUSE pin-version-mismatch: /home/brett/.npm-global/bin/openspec reports version '1.2.0', but the pin records '1.12.0'. Strict validation and archive verdicts differ between OpenSpec versions — trees clean at the pin fail under a later CLI on pre-existing conditions — so a run at the wrong version is not a weaker check but a different one, and it is refused rather than reported
Remediation: … If the PIN itself is stale rather than the environment, a version bump is a HUMAN-ONLY governed change …
```

exit 2. **The DEFAULT mode is unaffected**, which is the property the pin exists
for: it never consults PATH, so the same machine's gate run is green.

---

## 5. The consuming repository — OpsxFactory

OpsxFactory's own wiring (#219, feature 012) consumes this entrypoint, so the
bump reaches it. Measured through the **new** entrypoint, from this pinned
checkout, against a READ-ONLY worktree of `OpsxFactory` at `origin/main`
`3ca4925f` — **nothing was committed, staged or written in that repository**:

```
python3 scripts/validate-openspec-cli-pin.py --all --strict --repo <OpsxFactory>
Totals: 47 passed, 0 failed (47 items)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address and every target validated --strict clean
```

exit 0. **No disposition is needed and none is in scope**: both entries name
`repo: openxFactory`, the run resolves this tree's identity as `OpsxFactory`
from its git remote, and out-of-scope entries are neither applied nor treated as
stale. The success line correctly says *clean* rather than the
dispositioned-pass wording, because nothing was suppressed.

**A note on the expected figure.** This work was commissioned expecting
`46 / 0` at `1884942a`. The measured figure is **47 / 0**, and it is 47 at
`1884942a` as well as at `3ca4925f` — re-measured at both commits to be sure the
difference was not #218 landing under the work. The corpus is one item larger
than the brief expected; the material fact, **0 failed**, is unchanged.

---

## 6. Tests

```
pytest tests/openspec_cli_pin/ -q
81 passed
```

41 before this packet, 81 after. The 41 that existed are unchanged in substance
and still assert the five original checks, their ORDER, the refusal vocabulary,
the cache's re-verification property and the gate workflow's freedom from a
second copy of the version; only the version CONSTANTS moved, and the two
PATH-mode tests now use `1.2.0` as the wrong version rather than `1.12.0`.

The 40 new ones cover: the disposition grammar and its two admitted YAML forms
(with a negative control for the forms that are not admitted); the mandatory
citation and authority, parameterized over every field whose absence makes an
entry unreviewable; duplicate entries; both `--json` array shapes parsed from
**captured real `1.12.0` bytes** in `tests/openspec_cli_pin/fixtures/`; an
offline reconciliation of the PIN's own `finding:` strings against those
captured bytes, so a transcription slip surfaces on a developer's machine; the
repository-identity resolver against a REAL `git init`ed worktree deliberately
named for a branch; and the four verdicts —

| verdict | test | exit |
| --- | --- | --- |
| two dispositions cover two findings | `…_and_the_run_passes_saying_so` | 0 |
| a finding no disposition covers | `…_fails_and_the_failure_names_its_remedy` | 1 |
| **a disposition no finding matches** | `…_refuses_so_an_exception_cannot_outlive_its_cause` | **2** |
| a disposition for another repository | `…_is_neither_applied_nor_stale` | 0 |

**How stale-refusal is tested.** The same pin, the same repository identity, and
a report in which the dispositioned finding NO LONGER OCCURS — which is exactly
the corpus the day `add-composed-view-authoring` archives out of `--all`. The
run must exit 2 with `pin-disposition-stale`, name the orphaned entry, and carry
the remediation trailer. A second test proves the upgrade-coupling half of the
same property: a finding whose message has been REWORDED (a later CLI) also
refuses, because the disposition matches the message whole.

**And its boundary, found by running the tool.** `--change
add-composed-view-authoring` against the real corpus REFUSED, over
`add-chain-attestation`'s untouched entry, because a scan that never opens that
change cannot produce its finding. Staleness is a claim about the WHOLE corpus,
so only `--all` decides it: a narrowed run now applies the dispositions it
matches, decides no staleness, and PRINTS that it checked none, so a green
narrowed run is never mistaken for an audit of the list. Both halves are held by
tests. Verified against the real corpus after the fix:

```
$ python3 scripts/validate-openspec-cli-pin.py --change add-composed-view-authoring
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md …
  (this run scanned named targets, not the whole corpus, so NO disposition was checked for staleness here — only `--all` can establish that a finding no longer occurs)
OK openspec-cli-pin: … 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 1 finding(s) are ACCEPTED EXCEPTIONS, named above.
                                                                        (exit 0)
```

---

## 7. Scope kept

No consuming repository was edited. `.github/workflows/openspec-cli-pin-gate.yml`
took NO logic edit — it never carried the version, which this bump is the first
live test of and which CI confirms green at the new pin. One explanatory comment
in it is corrected, where it named `1.2.0`'s `engines.node` floor; `1.12.0`
declares the same floor and the comment now says which artifact it describes.
The pin header's dependency-closure paragraph is likewise re-derived at the new
version — TEN dependencies now, nine caret-ranged and one (`cross-spawn 7.0.6`)
exact, where `1.2.0` declared nine all caret — because a declared shortfall
restated with stale numbers is not a declared shortfall. `.github/workflows/pytest-suite.yml`'s literal
`@fission-ai/openspec@1.2.0` is deliberately NOT in this diff: it is #667's open
task 5.1, it now disagrees with the pin, and that disagreement is recorded in
this packet's `tasks.md` § 6.2 rather than left to be discovered. No contract
row, no digest inventory, no release tag moves.
