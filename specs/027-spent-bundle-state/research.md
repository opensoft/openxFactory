# Research — the third state, Phase 0

Six questions this design turned on. Each was answered by READING THE CODE, and
each records what else was on the table. Nothing here re-opens OD-1 … OD-9.

## R1 — Does the family read the working tree or the published tip?

**Answer: the PUBLISHED TIP, over the network.** `corpus.RealGit.remote_main_sha`
runs `git ls-remote origin refs/heads/main`, and `check_repo` reads the manifest
(and now the changelog) with `blobs_at(repo_path, tip, …)` at THAT sha.

**Consequence, and it is the single most important fact in this feature.**
`tests/doc-health/test_release_tag_publication.py::test_this_repository_reads_zero_and_the_probe_can_fire`
therefore reads the LIVE remote `main`'s changelog. This branch's declaration
is invisible to it until the squash lands, so that test CANNOT be made green
in-branch and MUST NOT be edited: the packet says it *"goes GREEN as a
consequence rather than by being edited."* It is the exactly-one failure in
this PR's `pytest-suite`, byte-identical to `main`'s failure since `ff9ed815`.

**What was done instead of editing it**: the mechanism is proved with the
file's real-git fixtures, where the test controls its own origin; and the
post-merge state is proved once against a bare repository whose `main` IS this
branch — see [`evidence/post-merge-proof.md`](./evidence/post-merge-proof.md).
Rejected alternative: reading the working tree as a fallback. That would make
the family's answer depend on which checkout ran it, and the requirement says
"at the published tip" for the reason that what a consumer can see is what the
family must read.

## R2 — Where exactly must the finding land, and why not the manifest?

**Answer: `contracts/releases/<bundle>.digests.yaml`.**
`Finding.match_key()` is `(family, repo, path)` and IGNORES the rule text
(`scripts/doc_health/__init__.py:187`). Every pre-existing finding of this
family passes `MANIFEST`, so a spent `info` there would share one identity with
all of them and its disappearance would be masked by any surviving sibling.

`contracts/CHANGELOG.md` — the first proposal's choice — is the same defect one
step over, which Codex found on PR #578: two bundles legitimately declared
spent would share THAT path, so withdrawing one declaration while the other
stood would leave the shared key in the current set and
`report.uncited_resolutions()` would raise nothing. The per-bundle inventory is
unique BY CONSTRUCTION: it is the artifact whose existence made the bundle
enumerable in `cut_bundles` at all.

## R3 — Is `uncited_resolutions` really severity-agnostic for an `info`? (OQ-3)

**Answer: yes, and it is now PROVED rather than inherited.** Two readers are
involved and both had to be checked:

* `report.plan_line` emits `class="{f.resolution}"` for EVERY finding, and
  `report.render` writes a ranked-plan row for every finding regardless of
  severity (`report.py:673-680`).
* `report.parse_previous` adds a key to `contested` on
  `m.group(7) == "contested"` with NO severity test — the severity test
  (`m.group(1) in (CRITICAL, ERROR)`) gates only the `keys` set used for
  regressions (`report.py:376-381`).

So a contested `info` joins `previous_contested` and its disappearance raises
an `uncited-resolution` ERROR. Measured in
`test_a_contested_spent_info_that_vanishes_raises_an_uncited_resolution` and,
per-bundle, in
`test_removing_ONE_of_two_spent_declarations_raises_only_ITS_uncited_resolution`.
The complement is pinned too
(`test_a_disposition_citing_the_change_silences_the_uncited_resolution`), so the
first two cannot be read as "a spent state can never be retired."

## R4 — `health/dispositions.yaml`: measured, not assumed (OD-1)

`promotion_fidelity.load_dispositions` keys entries by `(family, repo, path)`,
and every finding this family raised before this feature passes `MANIFEST` —
so one row would suppress EVERY absent-tag, misplaced-tag and lightweight-ref
finding about that repository, including the next genuinely abandoned bundle.
Its own docstring records the second defect: the file lives at the aggregation
root, so *"a `--single-repo` self-gate run has no aggregation root, so no
disposition applies in that scope"* — and the red self-gate IS a `--single-repo`
run. A dispositions row would not even have cleared the red.

## R5 — Is `contracts/CHANGELOG.md` writable between cuts?

**Yes, and it is one of exactly three that are.**
`release_inventory.EDITORIAL` is
`{contracts/CHANGELOG.md, contracts/manifest.yaml, contracts/README.md}`
(`release_inventory.py:62`), and the family labels an editorial member's drift
*"editorial member — expected between cuts"* at `info`, while a non-editorial
member's drift is an unconditional `error`.

`docs/contract-versioning-policy.md` is artifact
`docs-contract-versioning-policy.md` in
`contracts/releases/contract-v3.0.digests.yaml` and is NOT editorial — which is
OD-6's whole basis, and the reason § 3.1 is routed to the next cut rather than
taken here. Measured at HEAD:
`verify-commit --commit HEAD` reports exactly two mismatches,
`contracts/CHANGELOG.md` (this feature, editorial) and
`docs/contract-versioning-policy.md` (inherited from #577, already red on
`main`).

## R6 — What does an unlistable successor ref mean here?

`_tag_state` returns `"unlistable"` where `tag_ref` answers None, which is *"the
refs could not be listed"* and NOT *"there is no such tag"* — the #338
distinction this family declines to build on `verify_tag` for. When the
SUCCESSOR's refs cannot be listed, the ladder returns a `Skip` NAMING the
successor, in the family's existing shape, rather than guessing PROVISIONAL.

A successor carrying a LIGHTWEIGHT ref or a MISPLACED annotated tag is NOT
published (*"an annotated tag peeling to a commit that declares it"* is the
test), so it lands in the PROVISIONAL band — and the successor's own
lightweight/misplaced `error` is raised on its own account by the arms above,
which is exactly the "MUST NOT suppress the SUCCESSOR's own finding" the
requirement asks for.
