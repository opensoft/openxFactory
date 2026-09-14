# Verification record: honour-grandfather-dispositions-in-ratified-provenance, after the FIFTH bench round, 2026-09-11

Status: record
Kind: report
Date: 2026-09-11
Ratified by: honour-grandfather-dispositions-in-ratified-provenance — 2026-09-11, Brett Heap, D1 "info row carrying the citation" / D2 "Archived-only boundary" (record `review/ratification-2026-09-11.md`)

**THIS IS A SECOND CAPTURE AT ITS OWN PATH, WHICH IS WHY IT EXISTS RATHER THAN
AN EDIT TO `review/verification-2026-09-11.md`.** That file is a dated one-shot
run report; a committed capture is never rewritten, and a later run writes a
new file beside it. Its subject, like this one's, is the GATE RUN and not the
ratification, so it keeps `Status: record`.

**WHAT MOVED THE TREE AFTER THAT CAPTURE.** Copilot reviewed once more at
2026-09-11T12:23:01Z, on `5a8bba3e`, and opened two threads. Both were TAKEN,
in the commit this file is committed in:

1. **`scripts/doc_health/runner.py` — AN UNHASHABLE ENTRY KEY IN THE RUNNER'S
   OWN READ.** `tasks.md` § 3.10 carries it. The read is unconditional on every
   aggregation run and predates this packet's arm; a list- or dict-valued
   `family`, `repo` or `path` in an otherwise well-formed list file made the
   `(family, repo, path)` tuple unhashable and `set.add` raised `TypeError`
   out of the whole nightly.
2. **The README active row still read *20 new tests*.** It had in fact already
   moved to *21 / 1689 → 1710* in the ratification encode `e60ad2ff`, minutes
   before the comment; this round moves it once more, to the final figure
   below.

## 1. The measurement, both ways

```
$ python3 -m pytest tests/doc-health/test_grandfather_dispositions.py -q -k runners_own_read   # guard REMOVED, probe build
>                   dispositions.add((d.get("family"), d.get("repo"),
                                      d.get("path")))
E                   TypeError: unhashable type: 'list'
scripts/doc_health/runner.py:770: TypeError
1 failed, 21 deselected
```

```
$ python3 -m pytest tests/doc-health/test_grandfather_dispositions.py -q     # on the fix
22 passed in 3.00s
```

**exit 0 on the fix, exit 1 on the pre-fix module**, with the exact
`TypeError` the thread names. The test goes END TO END through `runner.main`
over a real aggregation root, because that is the only path that executes this
read — which is precisely why the § 3.7 entry tests, which call the family
directly, could not have caught it.

**IT NARROWS NOTHING.** The guard skips only an entry whose key cannot be
HASHED. Such a key could never have entered the set, and could never have
matched a real finding's `(family, repo, path)`, whose three fields are always
strings. The dispositioned set is identical either way; only the exception is
gone.

## 2. The counts, re-taken, and now final

| measurement | value |
| --- | --- |
| `grep -c '^def test_' tests/doc-health/test_grandfather_dispositions.py` | **22** |
| `python3 -m pytest tests/doc-health --collect-only -q`, this tree | **1711 tests collected** |
| `python3 -m pytest tests/doc-health/test_grandfather_dispositions.py -q`, this tree | **22 passed**, exit 0 |
| `python3 -m pytest tests/doc-health -q`, this tree BEFORE this round's test | **1710 passed**, exit 0 (`review/verification-2026-09-11.md` § 7) |
| `python3 -m pytest tests/doc-health -q`, `origin/main` `38c076d1` worktree | **1689 passed**, exit 0 (unchanged — no control input moved) |
| rise | **+22**, the new file entire |

**THE 1711 IS A COLLECTED COUNT AND A SUM, AND THIS FILE SAYS WHICH RATHER
THAN IMPLYING A RUN IT DOES NOT HAVE.** Collection over the whole directory
returns 1711; the new file's 22 all pass; the same directory returned 1710
passing on this tree one test ago, and 1689 on the control. The whole-suite
re-run at this exact head is the pull request's `pytest-suite` required check,
whose state is stated in this pull request's freeze comment; no figure in this
packet rests on a run that was not taken.

**THE EARLIER READINGS ARE SUPERSEDED, NOT CONTRADICTED**: 1706 (17 tests),
1708 (+19), 1709 (20 tests) and 1710 (21 tests) were each taken at a head
before the § 5.11, § 5.12 and § 5.14 rounds added their tests. `proposal.md`'s
front matter, `tasks.md` § 3.7, § 3.8, § 5.8 and § 5.14, the README active row
and the pull request body all now state **22 / 1689 → 1711** and no other
figure.

## 3. The gates re-run after the fix

```
$ OPENSPEC_TELEMETRY=0 openspec validate honour-grandfather-dispositions-in-ratified-provenance --strict
Change 'honour-grandfather-dispositions-in-ratified-provenance' is valid
```
**exit 0.**

```
$ python3 scripts/proposal-support.py . verify honour-grandfather-dispositions-in-ratified-provenance
proposal support verification ok
```
**exit 0.**

`python3 scripts/validate-sequenced-after.py .` **exit 0**;
`… --ledger-diff` **exit 0**; `python3 scripts/validate-scope-globs.py .`
**exit 0**.

## 4. What was NOT re-run, and why that is sound rather than lazy

`openspec validate --all --strict` on both binaries, `doc-health.py
--single-repo .`, the four-directory pytest selection and the aggregation
measurement (§ 10 and § 11 of `review/verification-2026-09-11.md`) are NOT
re-taken here. **THE ONLY CODE THIS ROUND CHANGED IS A GUARD THAT CHANGES NO
REPORT**: it skips an entry that could never have been in the dispositioned
set, so every finding, every severity and every count those gates measure is
the same by construction — the same property the earlier capture PROVED by
diff for the sibling guards, where a probe build with both of them removed
produced a report byte-identical to the guarded one. The markdown edits
alongside it are packet documents, which the governed-corpus word totals do
not read at all and which drew no finding in the earlier capture. The
authority for the whole-repository suite is the pull request's `pytest-suite`
required check on this head, not this file.

## 5. The bench after this round

Copilot's threads on this pull request now number **seven across five
rounds**. Every one is **TAKEN**, and each is dispositioned by name in
`review/ratification-2026-09-11.md` § 4 (rounds 1–4) and in `tasks.md` § 5.14
(round 5), with the two round-3 REFUSALS and their reasons in `tasks.md`
§ 5.11. Codex answered the one review request with a usage-limit notice and
never reviewed at any head — an ABSENCE, recorded as one, quoted in
`review/verification-2026-09-11.md` § 12. Sourcery posted a guide and no
finding. SonarCloud's quality gate passed.
