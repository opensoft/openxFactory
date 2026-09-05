---
code_surface: openxFactory — FIVE artifacts, all of them this repository's own tooling, tests and CI, none of them a neutral contract any consumer pins. (1) `scripts/validate-release-tag-gate.py` is NEW: it diffs the tree under judgment against its base, short-circuits when the pull request touches neither `contracts/manifest.yaml` nor `contracts/releases/**`, and otherwise runs the EXISTING `release-tag-publication` family over the merge tree by overriding exactly one seam method (`remote_main_sha`). (2) `.github/workflows/release-tag-gate.yml` is NEW: `on: pull_request` against `main`, no `paths:` filter, job and check name `release-tag-gate`, `fetch-depth: 0`. (3) `tests/doc-health/test_release_tag_publication.py` loses the zero-findings half of one test and KEEPS its positive control, renamed to say what it now asserts. (4) `tests/doc-health/test_release_tag_gate.py` is NEW: twenty-two tests over real git fixtures with real origins, one per gate condition plus the workflow's wiring. (5) `docs/contract-versioning-policy.md` gains one paragraph inside § Bundle Realization Order naming the gate and the post-merge tag obligation — that document IS a digested member of the published `contract-v3.4` bundle and is not one of the three EDITORIAL members, so this edit raises the designed `release-inventory-drift` `error` that the next cut clears by re-digesting it (§ Impact carries the measurement and the precedent). NOTHING in `scripts/doc_health/` changes — not the family, not a severity, not the threshold, not the enforcement floor, not `Finding`, not the report grammar, not `FAMILIES`, so the family enumeration and its counts do not move. NO NEW BUNDLE IS CUT and no release tag is owed by this change; the one bundle MEMBER it edits is the policy document named above.
target_release: implemented — the openxFactory main line. Realization = the workflow exists and runs on every pull request against `main`; the gate short-circuits green on pull requests that touch no release path and refuses on each condition its tests name; the suite no longer asserts zero findings over this repository. The archive gate is merge-plus-green PLUS the `[OPERATOR]` evidence in tasks § 4: a check that is not REQUIRED enforces nothing, so the ruleset id and one green run are named before this packet archives. No aggregation-repo bundle is cut: `contracts/manifest.yaml` is untouched, no inventory is written, and the one digested member this change edits is `docs/contract-versioning-policy.md`, whose drift the next cut re-digests.
Status: draft
Proposed: 2026-09-04
Origin: openxFactory issue **#664**, and Brett Heap's ruling on it the same day, in session, lane `openxfactory-max001`, verbatim: *"do your recommendation"* — given against three presented options and settling option 2. THAT INSTRUCTION ADMITTED THE PACKET TO THE QUEUE AND DID NOT RATIFY ITS CONTENT; ratification is a separate act and has not happened.
---

# Proposal: add-release-tag-gate

Status: draft
Proposed: 2026-09-04, on Brett Heap's in-session ruling of the same day — lane
`openxfactory-max001`, verbatim *"do your recommendation"* — given on
openxFactory issue **#664**, which states the problem, presents three options
and records the ruling as option 2. **That instruction supplied the origin and
approval pair the proposal-origin contract requires and nothing more: it
ADMITTED this packet to the queue and did not ratify its content.**

## Why

**A pin on a fact that a correct release makes false, held inside a check every
pull request must pass.**

`tests/doc-health/test_release_tag_publication.py::test_this_repository_reads_zero_and_the_probe_can_fire`
asserted, inside the REQUIRED `pytest-suite`, that this repository reads ZERO
`release-tag-publication` findings. The family reports a bundle declared in
`contracts/manifest.yaml` — or carrying an inventory under
`contracts/releases/` — without a published annotated tag.

**The two acts are performed by two actors, in that order, and the interval
between them is legitimate.** The versioning policy's own realization order says
so: step 4 lands the reviewed commit, step 5 publishes the annotated tag *at the
commit that landed*. Measured over every `contract-v3.x` cut this repository has
made, the tag is created AFTER the merge and points AT THE MERGE COMMIT:

| bundle | merge commit | merged | tag created | gap |
| --- | --- | --- | --- | --- |
| `contract-v3.1` | `19d00872` (PR #616) | 2026-09-03 20:49:41Z | 20:49:47Z | 6s |
| `contract-v3.2` | `9a773a31` (PR #624) | 2026-09-03 21:42:57Z | 21:43:20Z | 23s |
| `contract-v3.3` | `16b85614` (PR #636) | 2026-09-04 03:35:19Z | 03:36:03Z | 44s |
| `contract-v3.4` | `807a4f47` (PR #653) | 2026-09-04 19:56:21Z | 19:57:30Z | 69s |

(Merge-commit committer time to tag creation, one basis for all four.)

So between the cut landing and the tag being published, the repository GENUINELY
carries the finding — and the pin turned that legitimate window into a failure of
a required check on EVERY OPEN PULL REQUEST. **Measured 2026-09-03/04
(issue #664): PR #628 (`0d5e1ba9`, 22:27Z) declared `contract-v3.3` untagged;
main and every open lane failed on that one test until the tag was published
after PR #636 (`16b85614`) and main went green at `92e662cf` (04:02Z). Five and
a half hours. Every lane. None of them the cause, and none of them able to fix
it** — the remedy is a tag act by a second actor with tag rights.

**The signal is right and its placement was wrong.** The class the family exists
to catch is real and recurrent: `contract-v1.33`, `contract-v1.35`,
`contract-v1.39` went untagged for weeks; `contract-v2.3` and `contract-v2.4`
repeated it; `contract-v2.6` is a bundle no tag can ever reach. Nothing here
softens any of that. What moves is WHERE the condition blocks a merge: onto the
one pull request that is changing the release surface, and off every pull
request that is not.

## What Changes

**One requirement is MODIFIED and no requirement, file or capability is added
under `openspec/specs/`.** The delta restates `doc-health`'s promoted
*Release-tag publication* in full — all 24 promoted scenarios, every body unit,
byte-faithful — and adds seven paragraphs and six scenarios saying that the
condition is (1) REPORTED by the family nightly at its existing severities,
(2) ENFORCED at cut time by a required `release-tag-gate` check on the pull
request that changes the release surface, and (3) NOT ALSO PINNED as a
zero-findings assertion over this repository in its own test suite.

The realization:

1. **`.github/workflows/release-tag-gate.yml`** — `on: pull_request` against
   `main`. **No `paths:` filter, deliberately**: a required status context that
   does not report on some pull requests is *expected forever* and blocks them,
   so the scope test lives inside the job. **Not on `push: main` either** — a
   gate that ran on main after a cut merged would re-create the exact red this
   packet removes. The job carries no display name, so the check surfaces as the
   literal `release-tag-gate` a ruleset can pin (the rule
   `openxwallet-consumer-gate.yml` and `pytest-suite.yml` each write down for
   themselves). `fetch-depth: 0`, because both the base diff and the family's
   first-parent walk need history.
2. **`scripts/validate-release-tag-gate.py`** — resolves the tree under judgment
   (on a `pull_request` run, the merge commit GitHub builds) and its base (that
   commit's first parent, which is the base tip); exits 0 printing *"no release
   surface change"* when the diff touches neither `contracts/manifest.yaml` nor
   `contracts/releases/**`; otherwise runs `fam_release_tag_publication` over
   that tree by way of a `RealGit` subclass overriding ONE method,
   `remote_main_sha`. Refusals: `gate-findings` (any `error` or `warning`),
   `gate-version-reuse`, `gate-unaskable` (fail closed on a family skip),
   `gate-unreadable-head` / `-base` / `-diff` / `-manifest`. Exit 0 or 2, never
   1, on `validate-openreposhape-pin.py`'s stated rule.
3. **`tests/doc-health/test_release_tag_publication.py`** — the pinned test
   keeps ONLY its positive control and is renamed
   `test_the_probe_can_fire_over_a_tree_constructed_to_be_untagged`. Its
   docstring carries the whole history of the move so a reader arriving at it is
   not left guessing where the other half went.
4. **`tests/doc-health/test_release_tag_gate.py`** — twenty-two tests over real
   git repositories with real origins (the sibling file's discipline: this subject
   is the difference between a published ref and a local one, and a faked tag
   would prove nothing). One per condition, plus two on the workflow's wiring.
5. **`docs/contract-versioning-policy.md`** — a minimal addition inside
   § Bundle Realization Order. `Status: ratified`, unchanged.

## Impact

**Lanes: nothing goes red outside the cutting pull request.** A pull request
that touches no release path never consults the family at all. The
`pytest-suite` stops carrying this repository's live tag state, which also makes
it hermetic where it was not: the dropped assertion made ~52 `ls-remote` round
trips to the live remote on every run of the suite, and removing it takes
`tests/doc-health/test_release_tag_publication.py` from **110s to 19s** measured
locally.

**The cutting pull request carries the red, and only conditions it can act on.**
Replayed against the real history: openxFactory `807a4f47` — the `contract-v3.4`
cut, PR #653 — passes this gate (`exit 0`), and its own pull request would have
passed it before merging too, `contract-v3.3` having been tagged first. **THE
REPLAY PASSES THROUGH A DIFFERENT ARM FROM A LIVE CUT, and saying so is the
difference between evidence and a coincidence:** `contract-v3.4`'s tag now peels
to that very commit, so the replay is answered PRE-PUBLISHED, while the same
tree judged before the merge would have taken the distance-zero silence and the
`TAG OWED` record. PR #636,
which touched `contracts/releases/contract-v3.3.digests.yaml` while
`contract-v3.3` was declared and untagged, is exactly the pull request this gate
is for.

**Nightly reporting: unchanged, at unchanged severities.** The ruling keeps the
signal; a cut merged on administrative bypass without a tag stays visible in the
doc-health report.

**Doc-health counts: ONE finding moves, and it is predicted here rather than
discovered.** Measured `--single-repo` against a SAME-CLOCK CONTROL — a
worktree at `origin/main` (`9420472e`) run minutes apart from the branch, rather
than a baseline taken hours earlier, because this report ages by the calendar
and three `warning`s crossed a 30-day threshold during authoring: **main
6 critical / 4 error / 30 warning / 13 info → branch 6 critical / 5 error /
30 warning / 13 info**, and a line-by-line diff of the two reports differs by
EXACTLY ONE finding. The one new `error` is `release-inventory-drift` on
`docs/contract-versioning-policy.md`: that document is a DIGESTED MEMBER of the
published `contract-v3.4` bundle and is not one of the three EDITORIAL members
allowed to move between cuts, so editing it is the non-editorial drift
`release-surface-integrity`'s scenario *A normative contract drifts from the
declared bundle* says "MUST be reportable as a defect", and
`docs/contract-versioning-policy.md` says the same of "any OTHER member".
**It is a DEFECT, accepted knowingly and cleared at the next cut, which
re-digests the member** — the remedy that scenario itself names, "never a
hand-edit of the inventory to match the tree". The estate accepts it routinely
for this same document: `95c2cf6a` (PR #622) and `2898b104` (PR #577) both
carried it between cuts. The alternative — hand-editing
`contracts/releases/contract-v3.4.digests.yaml` — is forbidden: that bundle is
published, tagged and immutable provenance.

The `## MODIFIED` block is a new active-change delta, so
`modified-block-currency` reads it. It drops no canon unit, so it owes no
`Removed from canon by` marker and raises **no** currency finding — verified by a
`--family modified-block-currency` run naming this change zero times. The
`proposal-origin` family's declaration is carried in
`openspec/changes/add-release-tag-gate/.openspec.yaml` (`kind: ad_hoc`, id
`openxFactory:adhoc:2026-09-04-add-release-tag-gate`).

**Required-check inventory: one added, by Brett.** Making `release-tag-gate`
REQUIRED on `main` is a console act, recorded as tasks § 4 with the ruleset id
and one green run as evidence BEFORE ARCHIVE — not before ratification. The
precedent is `create-medxchart-overlay-boundary` § 5.3/5.4 (`pin-validation`,
ruleset `22272824`).

**PR #653 is not the first pull request this gate would judge — it merged at
19:56Z on 2026-09-04, before this packet was authored.** The first will be the
next pull request that touches the release surface, and the first proof of the
short-circuit is THIS packet's own pull request, which touches no release path
and must therefore report green while touching the machinery.

## Orchestrator Decisions — FLAGGED FOR VETO

The four decisions this session took that the ruling did not settle are
recorded in `design.md` as **D1** (what the gate may honestly fail on),
**D2** (the `gate-version-reuse` arm — the one addition beyond the ruling's
text, and a one-line deletion if vetoed), **D3** (no pull-request comment) and
**D4** (a `warning` refuses too). D1 and D2 are the ones to read first.

## What this proposal does NOT claim

- It does not claim the tag obligation is discharged by a passing gate. The
  gate says the surface is in order at the moment of the cut; the tag is still
  owed, is named in the check's report, and is still reported nightly.
- It does not claim to verify release digests. `release-inventory-drift`,
  `scripts/validate-manifest-digests.py` and the `manifest_digests` suite
  already do, in the same required `pytest-suite`.
- It does not widen or narrow what the family reads, and it changes no
  severity, threshold or enforcement floor.
- It does not claim `release-surface-integrity` is affected. That capability
  deliberately does not anchor on tags, so its obligation stays evaluable in the
  window before one exists; it is cited here and not modified.
