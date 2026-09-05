---
code_surface: openxFactory — THREE existing artifacts moved in substance, one comment corrected, and one fixture pair added, all in this pull request, none of them a registered contract row. (1) `contracts/openspec-cli-pin.yaml`: `version` `1.2.0` → `1.12.0`, the referent re-cut from the real registry bytes to `sha512-oFE2Lj7WVSc87nSibk6qe9HjHIOlxhcPAXbPey44DlLvJzBl5+9BZVrNiozOwv++CQhW+MG0kuP1XLZ/uQrrWw==` (shasum `c844543999f673cdd72445879b86a4abea4c07ef`, tarball `https://registry.npmjs.org/@fission-ai/openspec/-/openspec-1.12.0.tgz`), a new `rollback:` block recording the previous referent in the grammar's own terms, and a new `dispositions:` block carrying TWO cited exceptions. (2) `scripts/validate-openspec-cli-pin.py`: a sixth check that reads the pinned CLI's `--json` verdict and reconciles every ERROR-level finding against the declared dispositions in BOTH directions, four new refusal codes (`pin-disposition-malformed`, `pin-disposition-stale`, `pin-report-unreadable`, `pin-repo-unidentified`), and one admitted grammar widening (a folded `>-` scalar and a one-level nested `cited_to:` list). The five original checks, the refusal vocabulary that existed, the exit-code semantics, the integrity-before-install ordering and the PATH-mismatch refusal are unchanged, and a pin declaring NO disposition takes the original streaming path with no `--json`, no parsing and no repository-identity call. (3) `tests/openspec_cli_pin/test_openspec_cli_pin.py`: 41 tests → 81, the new ones covering the disposition grammar, the citation requirement, per-repository scope, both `--json` array shapes against CAPTURED REAL 1.12.0 bytes, and the four verdicts (applied, undispositioned, stale, out-of-scope). (4) `tests/openspec_cli_pin/fixtures/*.json`, two captures of the real `1.12.0` report on this corpus. NOT THIS CHANGE'S SURFACE: no consuming repository's wiring moves (OpsxFactory's #219/feature 012 already consumes this entrypoint and is MEASURED here, not edited); `.github/workflows/openspec-cli-pin-gate.yml` needs no LOGIC edit because it never carried the version, and takes only a one-line comment correction where an explanatory note named the old artifact's `engines.node` floor; `.github/workflows/pytest-suite.yml`'s literal `@fission-ai/openspec@1.2.0` line remains #667's open task 5.1 and is deliberately not ridden on this diff; the pinned artifact's DEPENDENCY CLOSURE remains the declared shortfall the pin's own header states and is not repaired here.
target_release: implemented (the openxFactory main line). No contract-bundle involvement: `contracts/openspec-cli-pin.yaml` is a CONSUMPTION pin and is not a registered row in `contracts/manifest.yaml` nor in any `contracts/releases/*.digests.yaml` inventory, so no digest set moves, no `contract_bundle_version` is spent and no release tag is owed. The archive gate is `release-realization`'s merged-plus-green evidence for a non-empty code surface: this packet's own gate run at the NEW pin, green with zero UNDISPOSITIONED failures, plus the consuming-repository measurement in `evidence/pin-bump-1.12-2026-09-05.md`.
Status: ratified
---

# Proposal: bump-openspec-cli-pin-to-1.12

Status: ratified
Ratified: Brett Heap, 2026-09-05 — verbatim "ratify 677", heard first-hand by
session opsXfactory-1; record at `review/ratification-2026-09-05.md`, which also
records that the merge preceded the record on Brett's word in the authoring lane.
Proposed: 2026-09-05
Origin: Operator ruling, Brett Heap, 2026-09-05, in session, verbatim:
*"take exit 2"* — deciding among the three exits
`openspec/changes/prepare-openspec-1.12-readiness/evidence/openspec-1.12-readiness-2026-09-05.md`
enumerated for the two ERROR-level findings it refused to clear. Exit 2 is
*"carry a dispositioned exception for the two"*. **The ruling settles WHICH
EXIT is taken. It does not ratify this packet's text**, which carries
`Status: draft` and owes a ratification citation from a separate act.

**THIS IS THE BUMP #667 NAMED.** `contracts/openspec-cli-pin.yaml` was cut at
`@fission-ai/openspec@1.2.0` because that is where the estate was green, and
the change that cut it said the upgrade would be "a later, separate,
human-only governed change that must land its target-version evidence with
it". That evidence is `evidence/pin-bump-1.12-2026-09-05.md`, in this packet,
measured by this packet, at the version this packet pins.

## Why

**The precondition #667 set has been met, and the last two findings are a
disagreement between the tool and this estate's canon rather than a defect in
either.**

#667 measured the cost of an unpinned upgrade and refused to pay it:
on 2026-09-04, openxFactory read `48 passed / 41 failed of 89` under `1.12.0`
and OpsxFactory `34 / 10 of 44`, every failure a PRE-EXISTING condition. Two
readiness packets then did the work — **#673** here (39 placeholder `## Purpose`
sections written, one task-group header supplied) and **#220** in OpsxFactory.
Re-measured 2026-09-05 at `1.12.0`:

| tree | at `1.2.0` | at `1.12.0` | undispositioned |
| --- | --- | --- | --- |
| openxFactory `6f3301fa` | 90 passed / 0 failed | **88 passed / 2 failed (90)** | **0** |
| OpsxFactory `3ca4925f` | — | **47 passed / 0 failed (47)** | **0** |

**OpsxFactory is clean outright.** openxFactory's two are the whole of what
remains, and they are the same disagreement twice:

```
✗ change/add-chain-attestation
  ✗ [ERROR] signed-execution-chain/spec.md: MODIFIED "A gate validates the short chain as a hash-linked chain" omits scenario(s) the current spec still has: "a tranche-two link does not exist yet". …
✗ change/add-composed-view-authoring
  ✗ [ERROR] ideation-dashboard/spec.md: MODIFIED "Composed views are read-only with a repository jump" omits scenario(s) the current spec still has: "Gate verbs hide on a composed view". …
```

**Both omissions are DELIBERATE, DECLARED, and RATIFIED.** Each is a narrowing
announced inside the MODIFIED block itself with this estate's reserved marker,
``**Merged into `<destination>` by <change-id> (<date>):**`` — the form council
LA-A1 reserved and #444 landed. `doc-health`'s promoted marker requirement
defines that form and uses the composed-view pair as its **worked example**,
written into canon at `openspec/specs/doc-health/spec.md:1770`:

```
**Merged into `Tile-bound gate verbs hide on a composed view` by add-example-change (2026-08-27):** `Gate verbs hide on a composed view`
```

That is, byte for byte, the rename `1.12.0` rejects. **The check is
marker-blind**: it compares scenario title sets and cannot read the declaration
this corpus requires. The only edit that satisfies it restores the old titles —
which in `add-chain-attestation` reinstates the permission council LA-A1 was
raised to close, and in `add-composed-view-authoring` contradicts the sibling
scenario that same change landed. **Both would revert a ratified decision.**

**The house's own reader grades the same two blocks at `severity=info`,
`class=contested`.** `scripts/doc-health.py` says of them, in its own rule
text, that this is "a divergence this arm CANNOT distinguish from a deliberate
rewording, and does not claim to". Two readers, one fact, two gradings — which
is precisely the situation a DISPOSITION exists for.

**So the finding is not something to fix. It is something to ACCEPT, in
writing, with a citation** — and until this packet there was no way to do that
for this pin. `scripts/validate-openspec-cli-pin.py` had no disposition support
at all (`grep`: zero hits), so the estate's only two options were a red gate or
a reverted decision.

### Why not the other two exits

#673's record named three, and this packet is explicit about the two it does
not take.

**Exit 1 — sequence the bump after both changes archive. REJECTED, and the
rejection is measured rather than impatient.** `add-chain-attestation` carries
**eight open task boxes** including §5.8, its canary pair is **not producible**,
and issue **#579** is unresolved; nobody can name the quarter it archives in.
Waiting means the estate keeps running its archive gate on a tool the estate
has already measured, remediated for, and decided to move to — and it means
`.github/workflows/pytest-suite.yml`'s stale literal and every laptop's global
install stay pointed at `1.2.0` indefinitely. A bump held hostage to an
unrelated packet's §5.8 is not a safety property.

**Exit 3 — take it upstream. NOT REJECTED, and DRAFTED, but not filed by this
lane.** `evidence/upstream-issue-draft-merged-into-marker.md` is a
ready-to-file issue for `fission-ai/openspec` asking that the
scenario-currency check honour a declared narrowing marker or offer per-finding
suppression, with the minimal reproduction and this estate's citations.
**Filing it is Brett's act, not this lane's**, and the two exits are not
exclusive: exit 2 is what this estate does about its own gate today, exit 3 is
what it asks of the tool. If upstream lands a fix, the dispositions go STALE on
the next bump and the mechanism forces their removal — which is the outcome
everybody wants.

## What Changes

1. **The pin moves to `1.12.0` by CONTENT ADDRESS.** Both hashes were
   recomputed over the real registry tarball's bytes by this lane, exactly as
   #667 did, and the verifier re-verifies them on every run before anything is
   installed. The `version` string remains a LABEL; the referent remains the
   SHA-512.
2. **A DISPOSITION mechanism, in the pin and in the verifier.** A declared
   exception names `repo`, `item`, `path` and the finding's text; carries a
   non-empty `cited_to:` and one of `ratified_by:`/`recorded_by:`; and says
   `why` in one line. The verifier PASSES only when every ERROR-level finding is
   matched by exactly one in-scope disposition, and it PRINTS every applied
   exception by name so a pass cannot be mistaken for a clean tree.
3. **Stale refusal, which is what keeps a disposition list from rotting into a
   suppression list.** A disposition matched by NO finding in a WHOLE-CORPUS run
   refuses (`pin-disposition-stale`, exit 2); a narrowed `--change` run applies
   its dispositions, decides no staleness, and says so, because only `--all` can
   establish that a finding no longer occurs. `add-composed-view-authoring` has one open
   box left; the day it archives, its finding leaves the corpus and this pin
   fails until its entry is deleted. That is the archive forcing a re-reading,
   by design.
4. **The previous referent is recorded as the ROLLBACK**, in the pin's own
   grammar rather than in prose, together with the fact that a rollback must
   drop the dispositions with the version.
5. **ONE ADDED requirement** on `neutral-product-pin`, stating the three
   properties a dispositioned finding must have.

## Impact

- **`contracts/openspec-cli-pin.yaml`** — version, referent, rollback,
  dispositions. HUMAN-ONLY under the ratified requirement; not clearable by a
  council.
- **`scripts/validate-openspec-cli-pin.py`** — check 6 and its refusals. The
  five existing checks and their ordering are unchanged and re-asserted by the
  41 tests that already pinned them, all still green.
- **`tests/openspec_cli_pin/`** — 81 tests and two captured real-report
  fixtures.
- **Every consuming repository** — the entrypoint's contract is unchanged for a
  tree with no dispositions in scope. OpsxFactory's wiring (#219, feature 012)
  consumes this entrypoint and is MEASURED in this packet's evidence at
  47 passed / 0 failed under the new pin, with no disposition needed.
- **Every engineer with a global `openspec`** — `--path-mode` now REFUSES a
  `1.2.0` on PATH, `pin-version-mismatch`, with the remedy in the message. That
  refusal is demonstrated in the evidence record rather than asserted.
- **`.github/workflows/openspec-cli-pin-gate.yml`** — NO logic edit, and
  correctly so: it never carried the version, so the bump reaches it through the
  pin file alone. This is the first live test of that design decision and it
  passes (CI green at the new pin on this pull request). One explanatory COMMENT
  is corrected, where it named `1.2.0`'s `engines.node` floor; the floor is the
  same at `1.12.0` and the comment now says which artifact it is about.
