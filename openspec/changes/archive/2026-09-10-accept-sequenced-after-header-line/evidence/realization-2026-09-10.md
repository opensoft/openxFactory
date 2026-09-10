# Evidence: the realization, met 2026-09-10 — merged, green, and READ BY A CONSUMER

Status: record
Kind: report
Date: 2026-09-10

Measured by lane `codexfactory-1` (session window `codeXfactory-1`) on
2026-09-10 at the archive gate, on branch
`archive/accept-sequenced-after-header-line`. **Every number below is a
command's own output taken here, or a merge fact read from the forge API — not
transcribed from this packet's authoring measurement, which was taken over a
different corpus snapshot and is cited separately where it is used.**

**WHAT THIS FILE IS FOR.** `proposal.md`'s `target_release:` says this packet
has a non-empty `code_surface` and therefore archives, under
`release-realization`, on **merged-plus-green realization evidence rather than
on landing**. Its § Impact adds the second half in its own words: *"The corpus
that moves is codexFactory's, and it moves at ITS re-pin, not at this
landing."* So the gate has two arms — the change is merged and green, AND at
least one consumer reads the site — and this record cites both.

## 1. Merged

| fact | value |
| --- | --- |
| pull request | [opensoft/openxFactory#886](https://github.com/opensoft/openxFactory/pull/886) |
| merge commit on `main` | `b91af6eab605021118e625a013961123ac9796e2` |
| merged at | 2026-09-10T12:33:38Z |
| ratified head | `f36d2bc2` (record `review/ratification-2026-09-10.md`) |
| ratifier | Brett Heap, repository owner, first-hand, in session, verbatim ***"ratify 886, 0.2 as narrowed, 0.3 pure moves"***, 2026-09-10T11:31:31Z |

## 2. Green — 10 of 10 required checks, re-read at the gate rather than inherited

`gh pr checks 886 -R opensoft/openxFactory`, read 2026-09-10T16:1xZ. Every
required check **pass**: `SonarCloud Code Analysis` (1m17s),
`clearing-dispatch-gate`, `lane-line`, `merge-master-approval`,
`openreposhape-pin`, `openspec-cli-pin`, **`pytest-suite` (20m43s)**,
`release-tag-gate`, `signed-execution-chain-gate`, `wallet-validation`.
(`Sourcery review` reports `skipping` and is not a required check.) The
`pytest-suite` run is `34475351186` job `102864681885` — the suite that carries
`tests/sequenced_after/test_header_line.py`, this change's only proof.

## 3. Read by a consumer — the re-pin, and the byte-equality arm RE-RUN HERE

| fact | value |
| --- | --- |
| pull request | [codeXfactory/codexFactory#333](https://github.com/codeXfactory/codexFactory/pull/333) |
| merge commit on `main` | `8be1a855325e89b6b0ea943db130ba4724089580` |
| merged at | 2026-09-10T16:09:02Z |
| `stack.yaml` `xfactory.contract_ref` | `724a2a4f` → **`b91af6eab605021118e625a013961123ac9796e2`** |
| `contract_declared_at` | `"2026-09-10"` |
| what moved with it | all FOUR vendored rows re-copied byte-for-byte, `vendored-scope-globs.pin.yaml` advanced in the same commit (one `source_contract_ref` for all four captures) |

**A recorded digest pins a copy to ITSELF; only the source comparison pins it to
the pin.** That arm SKIPS locally without an openxFactory checkout, so it was
given one and run:

```
cd <codexFactory worktree at 8be1a855>
OPENXFACTORY_ROOT=<openxFactory worktree> python3 -m pytest \
    tests/merge-master/test_vendored_sequenced_after.py \
    tests/merge-master/test_vendored_scope_globs.py -q
  -> 84 passed in 2.82s, exit 0        (0 skipped: the byte-equality arm RAN)
```

Without `OPENXFACTORY_ROOT` the same file reports `19 passed, 1 skipped`, the
skip being `test_the_vendored_bytes_equal_the_source_at_the_pinned_contract_version`
itself — which is why this record does not accept that run as evidence.
**codexFactory's vendored `sequenced_after.py` and `frontmatter_strict.py` ARE
openxFactory's bytes at `b91af6ea`**, and the reader the consumer executes is
therefore the reader this change specifies.

## 4. What the consumer's corpus reads — ONE corpus, TWO readers

The realization claim is not "a test passes"; it is *"eight declarations exist
that the reader cannot see"* becoming *"the reader sees them"*. Measured on
**one tree** — codexFactory `main` at `8be1a855` — swept twice, once by the
openxFactory reader at the pin codexFactory LEFT and once at the pin it now
HOLDS. The corpus byte is identical between the two runs; only the reader
changes.

```
python3 scripts/validate-sequenced-after.py <codexFactory @ 8be1a855> --sweep
```

| reader | `declaring sequenced_after:` | deepest resolved chain |
| --- | --- | --- |
| openxFactory `724a2a4f` (the old pin) | **0** | 0 hops — *"no honest chain has ever bound one"* |
| openxFactory `b91af6ea` (this change, the new pin) | **8** | **4 hops**, from `relocate-review-authority-floor` |

The eight, named by the sweep itself: `add-floor-regeneration-automation`,
`add-mcp-transport-adapters`, `admit-hosted-artifact-to-contract-manifest`,
`advance-openxfactory-pin-b91af6ea`, `amend-floor-regeneration-merge-authority`,
`amend-floor-regeneration-predicate`,
`extend-merge-master-envelope-to-floor-bot-lanes`,
`relocate-review-authority-floor`. Both runs exit **0** — the sweep is a
measurement, not a gate, and neither reading is a failure.

**Provenance of the eight, and it is three separate acts:** THREE were admitted
by this change's fifteen-real-line window alone (`add-floor-regeneration-automation`,
`amend-floor-regeneration-predicate`,
`extend-merge-master-envelope-to-floor-bot-lanes`); FOUR were brought inside it
by the **0.3 pure line moves** — codexFactory
[#331](https://github.com/codeXfactory/codexFactory/pull/331) →
`36ecb9bcca97c87e280a24ad5b8b57a1d7826c6f`, merged 2026-09-10T13:49:20Z, each a
pure move whose pre-image and post-image are the same multiset of lines; and ONE
is the re-pin packet's own declaration, `advance-openxfactory-pin-b91af6ea`,
written through the grammar it vendored — *the first witness of the site is the
change that acquired it.*

**A FIFTH move was ruled and then REVERTED, and the revert is part of the
record**: `archive/2026-09-05-add-floor-addition-grace` (real line 20) was
restored byte-for-byte at `cd3eb14` on Brett Heap's word, first-hand, in
session, 2026-09-10, verbatim ***"merge 401, revert the archived line in
331"***. An archived packet is a record; a parent proposal does not need to
declare against one to stay valid. So the beyond-window five resolved as FOUR
moves and ONE deliberate non-move — reported, not rounded to five.

## 5. The freeze, which is door (b)'s central claim, still untripped

`retention_at_archive` read through this change's reader against each admitted
carrier's OWN ratified head — the authoring measurement, cited rather than
re-taken, because the ratified heads it names have not moved:
`add-floor-regeneration-automation` at `c551e281`,
`amend-floor-regeneration-predicate` at `efeebd6`, and
`extend-merge-master-envelope-to-floor-bot-lanes` at `8f601982` each read
IDENTICALLY on both sides → **RETAINED, none contested**. Under door (a) all
three would have turned `ABSENT` into a declaration on already-ratified packets,
the contested-class mutation `sequenced_after.retention_problem` names by that
word. The four pure moves of #331 ARE such mutations on ratified carriers, and
they are dispositioned by name — Brett Heap's *"0.3 pure moves"* — which is
exactly what task 4.3 said such a move owes.

## 6. What this record does not claim

- **It does not claim codexFactory's whole suite is green.** On #333's head
  `e8a77642` the required `validate` (3m47s) and `merge-master-approval` pass,
  and **`browser-ui-repair` FAILS** — for the fixture-timeline chronology cause
  #333's own body flags at length (the pin advanced past `FIXTURE_DATE`, ruled
  route B, re-issued at `e8a7764`), and the merge was taken on Brett Heap's own
  word. That failure belongs to a fixture clock in another repository and
  touches nothing this change reads or writes; the codexFactory gate that
  executes the vendored grammar is `validate`, which passes.
- **It does not claim any other consumer has re-pinned.** None has, and none is
  advanced from here — `tasks.md` § 4.4 carries that as DEFERRED to their own
  lanes. The requirement is realized once ANY consumer reads the site.
- **It measures no openxFactory corpus movement, because there is none.** This
  repository fences its proposals and carries zero unfenced header lines, which
  `test_no_openxFactory_proposal_gains_or_loses_a_declaration` asserts by
  enumeration rather than by claim.
