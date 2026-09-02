# Red log — and one honest correction about the ORDER

**THE ORDER IS RECORDED AS TAKEN, NOT AS PRESCRIBED.** This feature's tasks.md
declares a RED GATE requiring every test to be written and seen to fail before
the module moves. **That is not the order this session worked in.** The module
and the tests were authored in the same pass, module first, and the red was
then demonstrated by REVERTING the module against the landed tests. The
distinction matters and is not smoothed over: a retro-red proves the tests
depend on the module, which is weaker than proving the tests were written
against the delta's words before any code existed.

**What IS red-first in the strict sense, because the packet requires it by
name** (§ 2.6, *"Include the RED-FIRST proof for 2.1's verification: the
declaration removed, the `error` returns"*): the declaration-removal control.
It is not a one-off measurement — it is the second half of a PERMANENT test
(`test_a_superseded_bundle_declared_SPENT_with_a_published_successor_is_an_info`)
and it is re-taken over the real repository in
[`post-merge-proof.md`](./post-merge-proof.md) § B.

---

## A. The landed tests against the PRE-FEATURE module

Command, from a detached worktree at this head with the pre-feature module and
pre-feature changelog checked out over it:

```bash
git checkout f4fddf7c -- scripts/doc_health/release_tag_publication.py contracts/CHANGELOG.md
python3 -m pytest tests/doc-health/test_release_tag_publication.py -q
```

Result:

```text
E   AttributeError: module 'doc_health.release_tag_publication' has no attribute 'CHANGELOG'
ERROR tests/doc-health/test_release_tag_publication.py
1 error in 0.22s
```

**NOT ONE of the 27 new tests can be COLLECTED against the pre-feature module.**
The red is total and blunt: the file's own module-level `CHANGELOG = rtp.CHANGELOG`
is the first thing that does not exist. Recorded as the bluntest available red
rather than dressed up as a per-test one.

## B. The 4.1 baseline, RE-TAKEN rather than quoted

Same worktree, pre-feature module AND pre-feature test file:

```text
FAILED tests/doc-health/test_release_tag_publication.py::test_this_repository_reads_zero_and_the_probe_can_fire
1 failed, 18 passed in 71.71s
```

**18 passed, 1 failed** — exactly the packet's § 4.1 measurement, and exactly
the same failing test. The inherited red is reproduced, not cited.

## C. The same file at this head

```text
1 failed, 47 passed in 82.07s
```

**47 passed, 1 failed.** The failure is the SAME test for the SAME reason: it
reads the LIVE remote `main` (`git ls-remote origin refs/heads/main`), which
this branch's declaration is invisible to until the squash. It is not edited —
the packet says it *"goes GREEN as a consequence rather than by being edited"* —
and § A of [`post-merge-proof.md`](./post-merge-proof.md) shows it passing once
that is true.

19 → 47 tests, +28: eleven reader tests with no repository, fourteen ladder
scenarios over real git fixtures, and three report-integration proofs.

## D. What a fourth measurement would and would not have added

A run of the NEW module and NEW tests with the declaration removed from THIS
repository's changelog was started and abandoned as redundant: the fixtures
carry their own declarations, so the only test that reads this repository's own
changelog is the self-gate — which is already failing pre-merge for exactly
that reason. The measurement that answers the question is § B of
[`post-merge-proof.md`](./post-merge-proof.md), where the declaration can
actually be removed from a `main` the family reads.
