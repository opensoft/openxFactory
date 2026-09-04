# Realization evidence — add-signed-execution-chain (tranche one)

**REALIZED IN TWO ACTS, and this file is the working record of act two.** Act one:
PR #524, squash `9af98c4d` — the five schemas, the packaged corpus, the named
reader, the running gate; tasks §3 and §4.1–§4.4. **Act two: THIS CUT,
`contract-v2.5`** — task 4.7, the registration and the additive bundle, performed
by a separate cutting session in its own pull request from an independent clone,
because the number is allocated by MERGE ORDER and act one deliberately declined
to reserve one.

`contracts/CHANGELOG.md` § `contract-v2.5` is the published version of these
facts. This file carries what a changelog entry has no place for: the count as it
was actually taken, the outputs measured at the branch tip, the one pin the bump
forced, the membership asymmetry a reviewer will ask about, and what is NOT here.

The change does NOT archive with the cut. It carries a code surface, so the
archive gate (`docs/release-realization-flow.md`) wants the merge and a green run
first — and it carries two boxes that are not any author's to close.

## The bundle number, fresh-counted at the cut — the THIRD count

Task 4.7 required the count to be re-taken rather than inherited, and it earned
that requirement: **this number has now moved twice.**

| count | taken at | read | what happened |
| --- | --- | --- | --- |
| first | the packet's tip | `contract-v2.3` | superseded — `contracts/manifest.yaml` declared `contract-v2.2` then; PR #514 took v2.3 |
| second | the realization's tip (`9af98c4d`) | `contract-v2.4` | superseded — `add-binding-consumer-identity` cut AND tagged v2.4 alone (#526, `afdf0e88`) |
| **third** | **this branch's tip** | **`contract-v2.5`** | **taken here** |

The third count, as taken:

```text
contracts/manifest.yaml:3        contract_bundle_version: contract-v2.4
contracts/releases/             inventory files present through contract-v2.4
git ls-remote --tags origin 'refs/tags/contract-v2*'
                                contract-v2.0 contract-v2.1 contract-v2.2
                                contract-v2.3 contract-v2.4
grep -i unreleased contracts/CHANGELOG.md
                                only historical prose inside older entries
grep -c signed-execution-chain contracts/releases/contract-v2.4.digests.yaml
                                0
```

`contract-v2.4` is SPENT — declared, tagged, and carrying **ZERO** members of this
family, verified by grep rather than assumed — so it covers none of this
capability. The next available additive number is **`contract-v2.5`**, and this
cut takes it.

**THE RULE THAT MADE THE RENUMBERING FREE.** *"A proposed change MUST NOT reserve
a minor number before merge order is known."* Act one wrote the re-count
INSTRUCTION into `tasks.md` and wrote no number into any contract byte, so when
v2.4 was taken by a sibling there was nothing to renumber — no manifest row, no
changelog heading, no inventory file, no consumption rule. The one place a number
WAS written is `proposal.md`'s `target_release: contract-v2.3` front-matter, which
is left standing: see the last section.

## What the cut moved, and in what order

The versioning policy's realization order is serialized, and step 2 requires
every release surface to move ATOMICALLY with the contract files in one candidate
commit. In authoring order, with the inventory LAST:

1. `contracts/manifest.yaml` — `contract_bundle_version` `contract-v2.4` →
   `contract-v2.5`, plus the `signed-execution-chain` family block registering all
   FIVE schemas with per-file `sha256`. **167 rows → 172**;
   `validate-manifest-digests.py` **150 → 155 digests verify**.
2. `contracts/CHANGELOG.md` — the `contract-v2.5` entry: ADDITIVE (minor), the
   nothing-narrows MEASUREMENT, the fresh count, the residuals and the
   registration-is-not-enforcement section, and the `contract-v2.3` discharge.
3. `contracts/README.md` and `contracts/signed-execution-chain/README.md` — the
   three **REALIZED and NOT YET REGISTERED** sentences act one wrote, resolved to
   the literal `contract-v2.5`. Each keeps its enforcement line.
4. `docs/contract-versioning-policy.md` — the `contract-v2.3` instance recorded
   in § Untagged Bundles After Enforcement Began.
5. `tests/intent-compliance/test_release_boundary.py` — the boundary pin
   ADVANCED, not broadened (below).
6. `tests/signed_execution_chain/test_manifest_row_digests.py` — new, the
   standing check on the five rows this cut adds (below).
7. `openspec/changes/add-signed-execution-chain/tasks.md`, `README.md`,
   `ideation/staging/INDEX.md` — 4.7 ticked with its evidence; the active-change
   entry and the staged topic's detail section record the cut and that TWO boxes
   remain open.
8. `contracts/releases/contract-v2.5.digests.yaml` — built LAST, by
   `scripts/validate-contract-release.py build`, never hand-edited. Built THREE
   TIMES for that reason: once after items 1–7; DISCARDED AND REBUILT when review
   of the entry text moved two members; and DISCARDED AND REBUILT AGAIN when the
   second rebase brought PR #532's edit to `contracts/CHANGELOG.md`, which is an
   inventory member. "Inventory built last" means last, not first-drafted — and
   "last" is measured against the LANDED base, not against the moment the author
   stopped typing.

## The inventory, built LAST

```text
python3 scripts/validate-contract-release.py build \
    --tag contract-v2.5 --output contracts/releases/contract-v2.5.digests.yaml
release build: pass
  bundle_tag=contract-v2.5
  entries=283
```

**MEMBERSHIP IS UNCHANGED: 283 entries in `contract-v2.4`, 283 in
`contract-v2.5`, zero added and zero removed.** That is what an additive release
looks like in an inventory — the growth is in what a member ASSERTS, not in which
members exist. Exactly **five** digests move, and each is a file this cut edited:

```text
contracts/CHANGELOG.md
contracts/README.md
contracts/manifest.yaml
docs/contract-versioning-policy.md
tests/intent-compliance/test_release_boundary.py
```

`contracts/releases/contract-v2.3.digests.yaml` and
`contracts/releases/contract-v2.4.digests.yaml` are untouched.

## THE ASYMMETRY A REVIEWER WILL ASK ABOUT

**The five schemas this cut registers are in `contracts/manifest.yaml` and are NOT
release-inventory members.** Their absence from the 283 is not an omission and not
a coverage gap. Inventory membership is computed by
`scripts/hermes_runtime_validation/release.py::_collect_members` from
`contracts/hermes-runtime/contract-index.yaml` (`release_member: true`), the
intent-compliance surface, the indexed fixtures, the validator package, the named
validators, the mandatory auxiliaries and the modified normative docs. The
`signed-execution-chain` family belongs to none of those sets — exactly as
`contracts/schemas/xfactory-credential-contracts.schema.yaml` did at
`contract-v2.4`, whose evidence file records the same asymmetry.

**SO THE IDENTITY TRAVELS BY THE MANIFEST ROW `sha256`**, and the invariant that
carries it is checked two ways:

* `scripts/validate-manifest-digests.py` — the estate-wide sweep, 155 rows,
  green at this cut.
* `tests/signed_execution_chain/test_manifest_row_digests.py` — NEW here, and it
  exists because **the sweep is wired into nothing.**
  `grep -rn validate-manifest-digests` finds it in a README line, in changelog
  history and in task lists — and in no workflow and no test. A tool that catches
  drift only when a human remembers to run it is the same failure mode it was
  written to close, one level up: it exists at all because one stale row rode
  through THREE bundle cuts undetected.

What the new test holds, scoped to the rows this family owns so a red reds for
THIS capability's reason:

* the registration is CLOSED IN BOTH DIRECTIONS — five rows, five schemas, and
  the on-disk set is derived from the DIRECTORY, so a sixth schema added without
  a row reds rather than shipping unregistered;
* each row's digest recomputed from the file on disk;
* each row's `consumption_rule` naming the bundle that registered it and the
  verify-before-current rule a consumer reads.

**IT WAS RED-PROVEN, NOT ASSUMED**, against two mutation classes on the
`chain-inception` row, each reverted after measurement:

| mutation | before the fix | after |
| --- | --- | --- |
| digest replaced with `deadbeefcafe0000…` | `AssertionError` naming both digests and the remedy | unchanged |
| digest replaced with `0000…0000` (64 zeros) | **`TypeError`** at the message f-string | `AssertionError`, recorded value `'0'` |
| the `conformance-declaration` row deleted entirely | 3 failures — the closure test plus that row's two parametrized cases | unchanged |

**THE ZEROS CASE IS THE FINDING, AND IT IS THE REALIZATION'S OWN ROUND-THREE
LESSON ARRIVING IN ITS OWN GATE.** An unquoted all-digit YAML scalar is parsed by
PyYAML as an INT, so slicing it raised `TypeError` — a HARNESS FAILURE — where a
MISMATCH was the answer owed. *Every refusal must reach the caller as the same
kind of answer.* The repair is `str()` on the recorded value (the sweeper's own
precedent) plus an explicit `isinstance(..., str)` assertion, because an
int-parsed digest also silently loses its leading zeros. The test was written,
the mutation was run, the crash was found by running it — not by reading it.

## The one pin the bump forced, and why it was advanced rather than broadened

`tests/intent-compliance/test_release_boundary.py` classifies the declared bundle
from an ENUM OF NAMED VALUES and fails loudly on one it has not been told about.
**THE TRIPWIRE IS THE POINT.** The library floor is `INTENT_RELEASE_FLOOR = (2, 3)`
and the membership rule is an AT-OR-AFTER comparison, so `release_membership`
accepts `contract-v2.5` silently and correctly; the enum is the only place in the
estate where a human is required to state which side of the boundary a new bundle
falls on.

`contract-v2.5` is past the floor, the intent-compliance family is registered in
`contracts/manifest.yaml`, and its files are present — so it is classified WITH
the introducing release and asserts exactly the same membership. **And the reason
it needs a hand act is sharper here than at v2.4**: this cut registers a
DIFFERENT family, so nothing about it touches intent-compliance's membership —
which is precisely the fact a human has to state, because the library cannot tell
"unchanged" from "unnoticed".

ADVANCED, NOT BROADENED. The tempting fix is to replace the enum with the
library's own `>= (2, 3)` comparison, which would make this and every future bump
pass silently and delete the only mechanism that forces a conscious
classification at a cut. So the enum gains ONE named member,
`FEATURE_SUCCESSOR_2 = "contract-v2.5"`, handled by the SAME match arm as the
introducing release, and the next bundle trips it again. **13 tests in that file
before, 13 after**; none added, removed, renamed, weakened or skipped.

The file is a release-inventory member (`tests/intent-compliance/` is inside the
family's membership), which is why it is item 5 above and the inventory is item 8.

## The cut's own bot round — ONE finding, real, and taken

Codex: **no major issues** at `3587ea8456`. Copilot: **one finding on the new
test, and it was right.**

| Round | Finding | Where it landed |
| --- | --- | --- |
| 1 | **Copilot** — the closure test derived the on-disk schema set with `Path.glob("*.schema.yaml")`, which reads the family ROOT ONLY. A schema placed in a SUBDIRECTORY would bypass the closure and ship UNREGISTERED while the test stayed green, and the layout is reachable rather than hypothetical: this repository already carries `contracts/hermes-runtime/migrations/v1-to-v2-mapping.schema.yaml`, the only nested schema under `contracts/` today. **Pre-fix, measured**: with an unregistered nested sixth schema on disk, `glob` returned exactly the five expected paths and the test PASSED | `rglob`, with the reason in the docstring. `glob` and `rglob` return the identical five paths at this cut, so the fix changes nothing today and closes the hole for whoever adds the sixth file |

**THIS IS THE SAME DEFECT CLASS THE REALIZATION SPENT THREE ROUNDS ON**, arriving
one level up in the cut's own instrument: a check that LOOKED like it was doing
its job. The docstring said *"derived from the DIRECTORY"* while the code read one
level of it, and the assertion passed for a reason unrelated to the property —
which is exactly the shape `tasks.md` §4 records as untestable from the rule's own
wording. It was confirmed by RUNNING the mutation against the pre-fix predicate,
not by reasoning about it. **The instrument gets the same scrutiny as the thing it
measures** — the third time this capability has had to apply that to its own
harness, and the second time in this file.

Sourcery is an upsell stub on this repository and returned no review.

## The rebase onto the final integration point

Policy step 1 is *"fetch and rebase onto the final integration point, then
IMMEDIATELY recheck bundle/tag availability"*, and step 4 makes a different
commit a NEW CANDIDATE whose gates rerun. Both applied: `origin/main` advanced
from `9af98c4d` to **`95a22a42`** (PR #531, the doc-health `--previous-report`
identity refusal) while this cut was being authored, so the branch was rebased
onto it and the count was RE-TAKEN rather than assumed:
`contracts/releases/` still holds inventories through `contract-v2.4`, the remote
still publishes tags through `contract-v2.4` and no `contract-v2.5`, and
`grep -c signed-execution-chain contracts/releases/contract-v2.4.digests.yaml`
still returns 0. **`contract-v2.5` still stands as the next available additive
number.**

The inventory did NOT need rebuilding, and that is measured rather than assumed:
`git diff --name-only 9af98c4d 95a22a42` is `docs/doc-health.md`,
`scripts/doc_health/report.py`, `scripts/doc_health/runner.py` and
`tests/doc-health/test_suite.py` — **not one release-inventory member**, so no
member's bytes moved under the rebase and `verify-commit` is green at the rebased
tip against the same inventory. Every gate below was re-run at the rebased
candidate, including the full suite and both doc-health sides.

## Gates at the branch tip

| gate | result |
| --- | --- |
| `validate-contract-release.py verify-commit --commit HEAD` at the cut commit | GREEN — `release verify-commit: pass`, `inventory=contracts/releases/contract-v2.5.digests.yaml`, exit 0, zero findings |
| `validate-contract-release.py verify-promotion --commit HEAD --remote origin --tag contract-v2.5` | 6 findings, ALL reachability-class: `HGR-RELEASE-CANDIDATE-UNREACHABLE` + 5 × `HGR-RELEASE-SURFACE-DRIFT`. EXPECTED pre-merge; reported, not chased (below) |
| `validate-contract-release.py verify-tag --remote origin --tag contract-v2.3` | `release verify-tag: pass` (see the predecessor-tags section below) |
| `validate-contract-release.py verify-tag --remote origin --tag contract-v2.4` | `release verify-tag: pass` |
| `validate-manifest-digests.py` | `OK contracts/manifest.yaml: 155 per-file digest(s) verify` |
| `verify-openxwallet-pin.py` | `OK openxwallet-pin verified: openXwallet@6b248d4050e1f88b3ca75c1290ad2c81f465300c (tag label wallet-v1.3), gitlink read from HEAD, 8 digest(s) recomputed` |
| `validate-signed-execution-chain.py .` | `0 error(s), 1 warning(s)` — the standing `reader-not-required` warning, which is 4.5's absence speaking, not a defect |
| `openspec validate add-signed-execution-chain --strict` | `Change 'add-signed-execution-chain' is valid` |
| `openspec validate --all --strict` | `Totals: 80 passed, 0 failed (80 items)` |
| every other `scripts/validate-*.py` | green; the one non-zero is PRE-EXISTING and identical on both sides (below) |
| `pytest tests/ -q -m "not postgres"` | **8363 passed, 21 skipped, 338 deselected, 46 subtests passed, 0 failed / 0 errors**, exit 0, ~24m, RE-RUN at each rebased candidate with the identical result (1440s at the first, 1421s at the final). 8363 + 21 + 338 = 8722, so the run covers everything collection sees, and exactly 21 skipped — no pin moved a count. Twelve of the passes are this cut's new file (2 closure + 5 digest + 5 consumption-rule); the run at the pre-rebase candidate reported 8355, and the 8 additional are PR #531's own new doc-health tests, which the rebase brought in |

### The one non-zero validator, measured on both sides

`scripts/validate-ideation-cross-reference.py .` exits 1 with **16 errors** — and
reports the identical 16 at `origin/main` `9af98c4d`, measured by stashing this
branch's only edit to a file that validator reads (`ideation/staging/INDEX.md`)
and re-running the same invocation. The findings are in
`examples/pattern-ledger/` and `tests/ideation-dashboard/fixtures/`, which this
cut does not touch. **PRE-EXISTING, ZERO NEW, ZERO CHANGED**, and not this cut's
to fix.

### `verify-promotion` IS REPORTED, NOT CHASED

Its six findings are all one class: the candidate is not an ancestor of published
`main` because it is not merged, and the five release-surface blobs differ from
`main` for exactly that reason. What matters is the half that measures the
CUT — the inventory-and-version agreement at the commit — and that it reports no
`HGR-RELEASE-TAG-EXISTS`, meaning the `contract-v2.5` name is free on the remote.
The class clears on merge.

## doc-health, same-clock, both directions

Two checkouts, **both named exactly `openxFactory`** — the finding identity is
`(family, repo, path)` and the repo is the basename, so a differently-named
baseline manufactures phantom findings (issue #342) — one at `origin/main`
`96b8a616` and one at this branch, run in the same session at
`--as-of 2026-08-31` with `python3 scripts/doc-health.py --single-repo <path>`:

| | critical | error | warning | info | findings | `release-inventory-drift` |
| --- | --- | --- | --- | --- | --- | --- |
| baseline `origin/main` `96b8a616` | 5 | 4 | 38 | 13 | 60 | 2 |
| branch, at the cut commit | 5 | 4 | 38 | 11 | **58** | **0** |

The set difference was taken in BOTH DIRECTIONS over the machine block, not
inferred from the headline. Findings present on the branch and absent from the
baseline: **NONE, of any family.** Findings present on the baseline and absent
from the branch: **exactly two**, and both are `release-inventory-drift` against
the standing `contract-v2.4` inventory — `contracts/README.md` (the realization's
two index rows) and `contracts/CHANGELOG.md` (PR #532's subsection). Both are the
findings this cut discharges; the second only exists at the FINAL base, which is
why the baseline moved from one drift finding to two. Every other family is identical on both sides:
staged-topic-template 26, register-lifecycle-consistency 10,
modified-block-currency 8, tag-hygiene 4, record-immutability 4,
staged-candidate-aging 3, ratified-provenance 1, ideation-routing 1,
document-catalog 1.

The finding the cut discharges, quoted from the baseline:

```text
- severity=info family=release-inventory-drift repo=openxFactory
  path=contracts/CHANGELOG.md
  rule="bytes differ from the digest 'contract-v2.4' records (editorial member —
  expected between cuts)"
  action="cut a release through the bundle realization order; never hand-edit an
  inventory or contract_bundle_version to make this comparison pass"
  class="auto-fixable"
- severity=info family=release-inventory-drift repo=openxFactory
  path=contracts/README.md
  rule="bytes differ from the digest 'contract-v2.4' records (editorial member —
  expected between cuts)"
  ... (same action and class)
```

**THE REMEDY LINE IS THE INSTRUCTION THIS CUT FOLLOWED**, and the one thing it
forbids is the shortcut: hand-editing an inventory or the
`contract_bundle_version` to make the comparison pass.

A MEASUREMENT NOTE WORTH CARRYING, because it cost a false reading. This family
reads the declared bundle from `contracts/manifest.yaml` **AT THE COMMIT**, by
design — so a run against a DIRTY working tree still reports the old bundle's
drift, and the branch showed the v2.4 finding until the cut was committed. The
zero above is measured at the cut commit, not before it.

## The predecessor tags, and the SECOND rebase they caused

**THIS IS THE PART OF THE CUT THAT MOVED UNDER IT TWICE, and the sibling-PR lesson
is the transferable bit.** The fresh count surfaced that `contract-v2.3` — recorded
by the `contract-v2.4` entry as declared and NEVER TAGGED, with publication PENDING
an owner act — had since been tagged. So the first draft of this cut MEASURED and
RECORDED that discharge itself, in both the `contract-v2.5` changelog entry and the
versioning policy.

**AND THEN `origin/main` ADVANCED TO `96b8a616` — PR #532, whose entire subject is
that same publication**, landed by another lane while this branch sat green. It
records BOTH tags (not just v2.3), peels each tag object, runs `verify-commit` at
both targets, and re-validates the targeting rule against a live control
(`contract-v2.2` → `8ccfb67b`, matching its already-published tag). It is the
better record, and it is now the record.

WHAT THAT COST AND WHAT IT CHANGED:

* `contracts/CHANGELOG.md` is a RELEASE-INVENTORY MEMBER, and #532 moved its
  bytes. `verify-commit` went red at the rebased tip with exactly one finding —
  `HGR-RELEASE-DIGEST-MISMATCH` on `contracts/CHANGELOG.md` — which is the check
  doing its job on a real drift, not the editorial uncut state. The inventory was
  REBUILT (third build) and `verify-commit` is green again.
* This cut's changelog subsection was rewritten from a MEASUREMENT into a
  CITATION. Two records of one measurement is how they drift apart, and the v2.4
  entry is where a reader of that bundle looks.
* The POLICY record was KEPT AND WIDENED, because #532 explicitly declines that
  half: it names the structural cause — issue **#528**, that no gate anywhere
  asserts a declared bundle has a published tag — observes that the policy's
  *"every bundle from `contract-v1.7` … is now tagged"* **has been false twice
  while nothing noticed**, and correctly refuses to correct the prose a third
  time. So the policy section now carries `contract-v2.3` AND `contract-v2.4` as
  instances FOUR and FIVE beside the three the 2026-08-25 ruling discharged, with
  the untagged windows, the consumption of v2.3-as-spent inside its window, why it
  recurred, and the plain statement that **a record is not a check** and #528 is
  open.

**THE LESSON, AND IT IS ONE THIS ESTATE HAS ALREADY WRITTEN DOWN ONCE**: check for
a sibling branch or PR on your subject the minute before you author a record about
it, not only at the start. This cut counted the tags at its tip, was correct, and
was still overtaken — because the count surfaced a fact interesting enough that
somebody else was already writing it up. The check that would have caught it is
`gh pr list` on the subject, not on the change.

**NOTHING IN THIS CUT TAGS OR RE-TAGS ANYTHING**, in either draft.

## What is NOT here

* **The `contract-v2.5` TAG.** Policy steps 1–2 allocate the version and build
  the inventory at realization; step 5 publishes the annotated tag against the
  commit that actually LANDS. Until this branch merges there is nothing honest to
  name, and publication is verified from an independently refreshed checkout
  afterwards.
* **Tasks 4.5 and 4.6, and they are the ones that matter.** 4.5 makes the named
  reader a REQUIRED check in the branch ruleset — an OPERATOR act whose evidence
  is the live ruleset state and never a merged workflow file
  (`add-wallet-carried-review-authority` task 2.5 established that distinction
  for `wallet-validation`, org ruleset **21538893**). 4.6 is its canary evidence
  and is BLOCKED ON 4.5 BY CONSTRUCTION: three of its four conjuncts are
  producible today and the fourth cannot be READ until the ruleset changes, and a
  box closed on three of four would be the closure-on-intention this family
  refuses. **Until 4.5 is performed, requirement 9 is UNMET rather than partially
  met**, the packaged declaration records `is_required_in_ruleset: false`, and the
  reader warns on every run. A bundle number confers nothing here; a registered
  family that nothing walks is documentation.
* **The archive.** The change stays ACTIVE in the README OpenSpec Records. It
  carries a code surface, so the archive wants the merge and a green run — and it
  carries two open boxes besides.

  **SUPERSEDED BY EVENT, 2026-08-31 — and the sentence above is left standing
  because it was true when it was written.** The change ARCHIVED on Brett Heap's
  order of that day, once #533 had merged and the tag was published: the archive
  gate's two demands — merged code on the implemented target and a green run —
  were both met and both re-read at the archive act rather than inherited from
  this file. **The two open boxes did NOT close and were not treated as closing
  conditions**: § 4.5 (the operator act making the check REQUIRED) and § 4.6 (its
  canary evidence, blocked on 4.5 by construction) survive the archive UNTICKED by
  decision, restated as dispositions in `tasks.md` § 4.5, § 4.6 and § 6.1, and
  carried forward at **openxFactory issue #534** so the obligation is not recorded
  only inside an archived packet. Requirement 9 therefore reaches canon meeting its
  own degraded case, which is the honest reading and not a workaround: the reader
  exists, is unrequired, warns on every run, and the shipped declaration says
  `is_required_in_ruleset: false`. The full act — mechanism, counts, byte-for-byte
  promotion check and the blob-id hazard verification — is recorded at `tasks.md`
  § 6.1.
* **Any edit to `proposal.md`.** Its `target_release: contract-v2.3` front-matter
  is LEFT STANDING. The packet is RATIFIED; the line itself says the number
  *"remains ALLOCATED AT REALIZATION BY MERGE ORDER … and the realization confirms
  the number against the manifest at ITS tip"*; and rewriting a ratified line to
  agree with today's state is the move this repository refuses everywhere else
  (§1.11 left the clarify sitting's superseded sentence standing for the same
  reason). The confirmed number lives in `tasks.md` 4.7, in
  `contracts/manifest.yaml` and in `contracts/CHANGELOG.md` — the surfaces a
  consumer reads. A later reader landing on `contract-v2.3` there should know it
  was superseded rather than missed: v2.3 is another change's published bundle
  (`add-standing-policy-compliance-contract`, PR #514), and this family has no
  members in it.

  **A DERIVED-VIEW CONSEQUENCE THIS BULLET DID NOT NAME, RAISED BY THE ARCHIVE
  PR'S BOT ROUND (Codex, P2, 2026-08-31) AND RECORDED RATHER THAN FIXED BY
  REWRITING.** The reasoning above is about prose honesty and it stands, but the
  field is also read by a MACHINE: `scripts/ideation_dashboard/generator.py`
  `_release_frontmatter` (`:378-387`) lifts `target_release` into the dashboard
  snapshot (`:542-547`), and archived folders are in scope
  (`_archived_change`, `:202-214`) — so the dashboard's tile for this ARCHIVED
  change reports this line, not `contract-v2.5`. **THE PRESCRIBED FIX WAS
  REFUSED, on this repository's own doctrine**: rewriting a RATIFIED proposal's
  front-matter to agree with today's state is the move refused everywhere else,
  and doing it inside an ARCHIVE commit would additionally make the archived
  packet differ from the text that was ratified — a worse defect than a
  superseded number. **THE LINE IS ALSO NOT FALSE**: `_header_value` returns the
  WHOLE physical line, so what the dashboard renders carries the caveat inline —
  the same sentence says the number *"remains ALLOCATED AT REALIZATION BY MERGE
  ORDER … and the realization confirms the number against the manifest at ITS
  tip"*. Every authoritative surface says **`contract-v2.5`**:
  `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, `tasks.md` § 4.7, the
  published tag, and the README's archived row. What a reader of the dashboard
  tile alone would miss is the confirmed number, and **that gap is now written
  down here rather than left to be rediscovered** — the honest home for it is a
  derived-view concern (should the dashboard prefer a realization-confirmed
  number over a proposal-time one?), not an edit to a ratified line.
* **Tranches two and three.** Named successors, not drafted, and their absence at
  this tranche is not a defect.
* **Anything belonging to another lane.** This cut touches no other active
  change's packet, registers no other family, and moves no submodule pin.
