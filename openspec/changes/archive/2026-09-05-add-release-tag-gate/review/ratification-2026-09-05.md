# Proposal Ratification: add-release-tag-gate

Status: record
Kind: report
Decision date: 2026-09-05
Ratifier: Brett Heap (openxFactory operator authority) — in session
Ratified: 2026-09-05 by Brett Heap (openxFactory operator authority) —
in-session, verbatim: *"ratify 668, land it when green"*, given after a
presentation that carried `design.md` **D1** and **D2** as the two readings most
worth a veto. **Neither was vetoed.**
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/doc-health/spec.md` (**ONE MODIFIED requirement**, *"Release-tag
publication"*, restated in full with all 24 promoted scenarios and **SIX added**)
— together with its realization in `scripts/validate-release-tag-gate.py`,
`.github/workflows/release-tag-gate.yml`,
`tests/doc-health/test_release_tag_gate.py`,
`tests/doc-health/test_release_tag_publication.py`,
`docs/contract-versioning-policy.md`, `README.md` and
`tests/sequenced_after/corpus-ledger.yaml`, with
`openspec validate add-release-tag-gate --strict` and `--all --strict` green and
the verification run captured beside this file at `verification-2026-09-05.md`.

**This record is CAPTURED AT MERGE, not at first push, and it was RE-DERIVED
PRE-CAPTURE.** `record-immutability` forbids editing a `Status: record` document
AFTER capture; capture is the merge of the pull request that establishes it, and
nothing is merged yet. Every number in `verification-2026-09-05.md` was
re-derived on the tree this record sits in — see that file § 8 for the branch's
merge history and what each merge moved. A commit cannot write its own hash into
its own tree, so the ratification commit is named here by its subject and its
position on the branch rather than by a hash.

## 1. What was ratified, and what it says

**One requirement is MODIFIED and none is added.** `doc-health`'s promoted
*Release-tag publication* is restated in full — every body unit and all 24
promoted scenario titles, byte-faithful — and gains seven paragraphs and six
scenarios saying that the release-tag condition is:

1. **REPORTED** by the `release-tag-publication` family nightly, at the
   severities that requirement already sets, unchanged by this packet;
2. **ENFORCED at cut time** by a required `release-tag-gate` check on the pull
   request that changes the release surface — `contracts/manifest.yaml` or
   `contracts/releases/**`, and nothing else; and
3. **NOT ALSO PINNED** as a zero-findings assertion over this repository inside
   its own test suite.

No file is added under `openspec/specs/`, so **no codexFactory floor advance is
owed**. The block **drops no unit of canon**, so no `Removed from canon by` and
no `Merged into` marker is owed — verified by a probe shown capable of firing
(§ 5).

## 2. Why the packet exists, in one measurement

`tests/doc-health/test_release_tag_publication.py::test_this_repository_reads_zero_and_the_probe_can_fire`
asserted, inside the REQUIRED `pytest-suite`, that this repository reads ZERO
`release-tag-publication` findings. The annotated tag for a new bundle is
published **after** the cutting pull request merges, at the merge commit, by a
second actor holding tag rights — the versioning policy's own realization order
puts tagging at step 5, after the landing at step 4. Measured from each merge
commit's committer time to its tag's creation:

| bundle | merge commit | gap |
| --- | --- | --- |
| `contract-v3.1` | `19d00872` (PR #616) | 6s |
| `contract-v3.2` | `9a773a31` (PR #624) | 23s |
| `contract-v3.3` | `16b85614` (PR #636) | 44s |
| `contract-v3.4` | `807a4f47` (PR #653) | 69s |

So the repository genuinely carries the finding for the length of that window,
and the pin turned it into a failure of a required check on **every open pull
request**: PR #628 declared `contract-v3.3` untagged at 22:27Z on 2026-09-03 and
main plus every lane failed on that one test until the tag landed after PR #636
and main went green at `92e662cf` (04:02Z). **Five and a half hours, every lane,
none of them the cause and none of them able to fix it.**

## 3. The two decisions ratified knowingly, with the framing they carried

Both were put to the ratifier as veto points and both stand.

### D1 — a cutting pull request is NOT required to carry its own tag

The admitting ruling's own item 1 read *"FAIL when that tree declares a bundle
whose tag is not published on the remote"*. Read literally and alone that makes
the cutting pull request unpassable, the tag being unable to exist before the
merge (§ 2). **No new judgement was invented:** the promoted requirement's own
scenario *The declaring commit is still the published tip* already emits nothing
for a bundle whose declaring commit is the tip, and **on a merge tree the
cutting commit IS the tip**. The gate therefore passes the cut and **RECORDS**
the owed tag — `TAG OWED: …` in the check summary and as a `::notice` — with the
nightly still reporting it and the next release-surface pull request refused
until the tag exists.

**The framing put to the ratifier:** *if you want the tag required at the head
before merge, that is a different packet — it changes the versioning policy's
realization order itself, and the evidence says the estate does not work that
way, four times out of four.* Ratified as designed.

### D2 — `gate-version-reuse` stays, scoped to the moved declaration

The one arm beyond the admitting ruling's text: where a pull request MOVES the
manifest declaration onto a bundle whose tag is already published and peels
somewhere other than the tree under judgment, the gate refuses. It is the one
release defect the family cannot see — at a tip where declaration and tag agree
`_tag_state` reads `ok` — and the policy's *"a version number is never reused"*
is what it enforces.

**Its reach is stated rather than implied**, and was narrowed during the
adversarial round: it reaches only the MOVED declaration, so the same-number
race in which the loser's base already declares the number never enters the arm.
That case is answered by the realization order's own rebase-and-recheck step,
and this gate does not claim it.

**The framing put to the ratifier:** *not in the ruling; deleting it is one `if`
block, two tests, one scenario and one table row* — `tasks.md` § 1.3 carries
that deletion verbatim so the cost of reversing the decision sits beside it.
Ratified as designed; § 1.3 records the deletion as NOT TAKEN.

### D3 and D4, likewise not vetoed

**D3** — the obligation is recorded in the check summary and a `::notice`
annotation rather than in a pull-request comment, because a commenting workflow
needs `pull-requests: write`, which is read-only for a fork, so the comment
would fail silently in exactly the case where a visible obligation matters most.
**D4** — a `warning` refuses too, because that is the bar the retired pin held
(*no `error` and no `warning`*) and failing only on `error` would quietly relax
it under cover of a relocation.

## 4. What the ratifying word did NOT settle

*"land it when green"* settles ratification and the landing condition. It
settles **nothing** about the `[OPERATOR]` act.

**`tasks.md` § 4 remains outstanding: adding `release-tag-gate` to ruleset
`21538893` ("openxFactory wallet-gate", today `wallet-validation`,
`pytest-suite`, `lane-line`) as a REQUIRED status check on `main`.** It gates
**ARCHIVE, not ratification**, with the ruleset id and one green run read back
from the API as evidence. Until it is performed, the obligation this packet
moves out of `pytest-suite` is enforced by a workflow anyone can merge past,
which is strictly weaker than the state before this change. **A ratified packet
is not a discharged one, and this section exists so that cannot be misread.**

An earlier draft of § 4 named `pin-validation` as the neighbouring required
context. **This repository has none** — that is `opensoft/MedxChart`'s
(ruleset `22272824`), cited here only as the SHAPE precedent for an
`[OPERATOR]` task with evidence before archive. Corrected on adversarial review.

## 5. Independent review, recorded including its absences

- **Codex: REFUSED THREE TIMES on usage limits** — requested at 22:45:52Z
  2026-09-04 (refused 22:46:02Z), again on the fix-round head, and again after
  it. **No Codex round ran at any point on this pull request.**
- **Sourcery:** the private-repo upsell stub, as always in this repository.
- **Copilot: three rounds.** Round 1 found ONE real defect — `_run` documented
  itself as degrading to `None`, but `subprocess.run` RAISES `OSError` when git
  cannot be executed, which would have exited the tool with an uncontrolled code
  and broken its own "0 or 2, never 1" contract. Round 2: zero new comments.
  Round 3: four comments, all taken (§ 6).
- **An INDEPENDENT ADVERSARIAL REVIEW found the defect neither bot did**, and
  that is the reading of record for how much the bot bench was worth here.

**A positive control on the `## MODIFIED` block itself.** The
`modified-block-currency` family reports nothing about this change — which alone
cannot be distinguished from a block it never read. One promoted scenario title
was deliberately mutated and the family re-run: it fired (*"omits 1 of the 24
scenarios … 'The published tag is lightweight rather than annotated'"*); the
delta was restored and the family went silent again. **All 24 promoted scenario
titles and every body unit are carried, verified by a probe shown capable of
firing.**

## 6. The adversarial review and the fix round, disposed item by item

**P2-1 was a real hole and it is the reason this section leads with it.** `git
diff` detects renames by default and prints only the DESTINATION path, so a pull
request doing nothing but `git mv contracts/releases/<bundle>.digests.yaml
docs/…` — or the same move of `contracts/manifest.yaml` — came back as a single
`docs/…` path, the scope test saw nothing under the release surface, and the
gate exited **0 saying "no release surface change" while the pull request had
REMOVED a release member**. Fixed with `--no-renames`; two tests, each asserting
first that git's default really does hide the source side, so they test the flag
rather than a hypothesis.

| item | disposition |
| --- | --- |
| **P2-0** | `release-surface-integrity` was cited by the WRONG scenario. The governing one is *A normative contract drifts from the declared bundle* ("MUST be reportable as a **defect**"); the editorial exemption names three members not including this document. "rather than a defect" deleted; D8 re-cited and restated as an **accepted defect**. Nothing reclassified. |
| **P2-1** | Fixed with `--no-renames` + two tests (above). |
| **P2-2** | The delta said FOUR scenarios were added; there are **SIX**. Corrected. |
| **P2-3** | The scenario about the retired pin had no enforcing test. Added: it scans the publication suite for a `repo_paths`/`REPO_ROOT` binding, with the probe shown firing on the retired line itself. |
| **P3-1** | Test count corrected (sixteen → **twenty-four** after the later rounds). |
| **P3-2** | `ls-remote` figures re-measured: **51 inventories**; **52 round trips / 75s** on a non-cut release-surface pull request, **54 / 85s** on a cut. |
| **P3-3** | `pin-validation` named as a neighbour that does not exist here; real contexts read from the API (§ 4). |
| **P3-4** | The `807a4f47` replay passes through the **PRE-PUBLISHED** arm, not the `TAG OWED` arm a live cut takes. Named. |
| **P3-5** | D2's reach softened to the moved-declaration case, in design **and** a new scenario bullet (§ 3). |
| **P3-6** | The refusal table was asserted one-directionally. Now an **equality**, with both formerly unreachable arms driven by fault injection at the git seam. |
| **P3-7** | `tasks.md` 3.7 ticked; the `release-tag-gate` run id and the `actionlint` result recorded under 5.5/5.6. |
| **P3-8** | Recorded in design: the `ls-remote` cost grows one round trip per cut, forever; the remedy is a change to the family's `tag_ref` seam and therefore a different packet. |
| **P3-9** | Recorded in `tasks.md` § 5.7 (§ 5 above). |
| **Copilot r3** | Two stale `68s` docstrings corrected to **69s**; workflow-command escaping added (`workflow_command_safe`, `%` first) — **with its reach corrected rather than accepted**: it is not reachable today, both emission sites being narrower than the review assumed, so it is DEFENCE IN DEPTH and two tests pin the two facts separately. |
| **Timing basis** | The `contract-v3.4` gap is **69s** on the merge-commit basis, and the basis is now stated wherever the figure appears. |

## 7. The one finding this packet knowingly adds

`docs/contract-versioning-policy.md` is the document this gate enforces, so the
gate belongs in its § Bundle Realization Order. It is also a **digested member**
of the published `contract-v3.4` bundle and is not one of the three EDITORIAL
members (`contracts/CHANGELOG.md`, `contracts/manifest.yaml`,
`contracts/README.md`) that may legitimately move between cuts. Editing it
raises one `release-inventory-drift` **`error`**.

**It is a DEFECT, accepted knowingly, and cleared at the next cut**, which
re-digests the member — the remedy the governing scenario itself names, *"never
a hand-edit of the inventory to match the tree"*. Hand-editing
`contracts/releases/contract-v3.4.digests.yaml` is forbidden: that bundle is
published, tagged and immutable provenance. The estate accepts the same state
for this same document routinely — `95c2cf6a` (PR #622) and `2898b104`
(PR #577) both carried it between cuts. It is **not** reclassified anywhere: it
is reported at `error`, counted at `error`, and owed a cut.

## 8. What lands, and what is still owed

**Lands with this ratification:** the workflow, the validator, the moved
assertion, the tests, the delta, the policy paragraph, the README row and the
ledger row.

**Still owed, and not by this word:**

1. **`tasks.md` § 4 — the `[OPERATOR]` act**, gating ARCHIVE (§ 4).
2. **`tasks.md` § 4.3** — the first pull request this gate judges for real is
   the next one touching `contracts/manifest.yaml` or `contracts/releases/**`.
   **PR #653 is not it**; it merged before this packet was authored and is used
   only as replay evidence.
3. **The next cut** clears § 7's `error` by re-digesting the policy document.
