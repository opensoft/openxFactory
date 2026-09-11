# Research: 033-add-consent-custody-rederivation-record

Measurements, not options. Every figure was taken on branch
`033-add-consent-custody-rederivation-record` at base `main` `6df21737`
(2026-09-09), with the command that produced it. Nothing here is carried
forward from the packet's own authoring-time measurements — where the two
differ, the difference is stated.

## R1 — Feature numbering

`ls specs/` ends at `032-govern-archived-record-edits`. `git branch -r | grep
'03[0-9]-'` returns `origin/031-configured-notebook-hosting-identity` and
`origin/032-govern-archived-record-edits` only. **`033` is free; no collision.**

## R2 — The next additive minor

| Surface | Command | Value |
| --- | --- | --- |
| Manifest | `grep contract_bundle_version contracts/manifest.yaml` | `contract-v3.4` (line 3) |
| Inventories | `ls contracts/releases/` | highest `contract-v3.4.digests.yaml`, **283 entries** |
| Tags | `git tag -l 'contract-v*' \| sort -V \| tail -1` | `contract-v3.4`, annotated, at `807a4f47` |

**`contract-v3.5` is FREE on all three.** (re-cut as `contract-v3.6` on 2026-09-09 after #866 took v3.5 — see [#630 comment 5609442856](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5609442856)) `contract-v2.6` is the SPENT number
(`docs/contract-versioning-policy.md` § *The SPENT State*), not this one. The
only occurrences of the literal `contract-v3.5` in the tree are: this packet's
own "measured, not reserved" sentences; the archived
`2026-09-08-publish-openspec-cli-pin-as-contract-member` recording that it chose
**A-defer** over cutting it; two `tests/clearing/` assertions that the string is
absent from a manifest rule; and one CHANGELOG sentence about a guard. **Nothing
claims it.** (re-cut as `contract-v3.6` on 2026-09-09 after #866 took v3.5 — see [#630 comment 5609442856](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5609442856)) — this enumeration was true at the branch point
`6df21737` and lane `provenance-autonomous-merge` claimed and published the
number on 2026-09-09.

## R3 — The v3.4 precedent for a cut

```bash
git show -s --format='%H %P | %cn | %s' contract-v3.4
```

`contract-v3.4` landed as `807a4f47` — ONE parent, committer `GitHub`, subject
ending `(#653)`: a **squash merge**. Its message records the discipline this
feature follows: one candidate commit over one integration point; the
integration performed as a MERGE of `main` into the cutting branch because
opensoft org ruleset **8981805** forbids non-fast-forward updates; the change
class MEASURED (`git diff --name-status contract-v3.3 HEAD -- contracts/`) and
every moved path attributed to its originating PR; the inventory **built LAST by
the tool, never hand-edited**.

## R4 — Release-inventory membership

`grep 'consent-instrument' contracts/releases/contract-v3.4.digests.yaml`
returns **nothing**. The inventory's five `contracts/schemas/*` members are
`demotion-execution-receipt`, `gate-action-record`, `gate-intent`,
`xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog`.

**Consequence:** the schema edit re-bases a `contracts/manifest.yaml` per-file
digest and adds NO inventory row. Membership is closed over what
`scripts/hermes_runtime_validation/release.py` `_collect_members` enumerates
from the catalog.

## R5 — The manifest digest, and why it is a gate

`contracts/manifest.yaml:2042` pins
`sha256: 13b0fe46fdb8791020b426dcd763aced2a3280a82923b32d3a0d0877ab6ad441`, and
`sha256sum contracts/schemas/consent-instrument.schema.yaml` returns exactly
that value — **the pin is CURRENT today**. `python3
scripts/validate-manifest-digests.py` verifies **189 per-file digests** and is
driven inside `pytest-suite` by
`tests/manifest_digests/test_manifest_digest_sweep.py`.

**The row's own `schema_version: 1` is EXPLICITLY not the schema file's
version**, and the manifest says so in its own words: *"the per-row
schema_version below mirrors that const, not the schema file's
contract_schema_version"*. That sentence is the measured backing for Q4's
ruling that the row field stays put.

**Ruled at Q5, then REVISED BY THE CONSISTENCY PANEL (F2), and the revision is
operative.** The split runs on WHAT THE FIELD IS, not on which commit is
convenient: a per-file `sha256` is INTEGRITY BOOKKEEPING FOR THE EDITED FILE,
so it rides the **§ 2 schema commit** — the commit that makes it stale closes
it. `contract_bundle_version`, the appended `consumption_rule` paragraph, the
CHANGELOG, the inventory and the cut-coupled tests are VERSION IDENTITY, which
is what policy step 2's atomicity concerns, and they ride the ONE § 5.2
candidate. **Every intermediate commit is green; no deviation is declared.**

## R6 — What the bundle carries beyond this session

`git diff --name-status contract-v3.4 HEAD -- contracts/`: **4 additions, 14
modifications**.

| Status | Path |
| --- | --- |
| A | `contracts/openspec-cli-pin.yaml` |
| A | `contracts/openspec-cli-pin.1.12.0.package-lock.json` |
| A | `contracts/policies/repository-identity.yaml` |
| A | `contracts/review-lane-repin-binding.template.yaml` |
| M | `contracts/README.md` |
| M | `contracts/manifest.yaml` |
| M | `contracts/openreposhape-pin.yaml` |
| M | `contracts/openxwallet-pin.yaml` |
| M | `contracts/review-lane-pin.yaml` |
| M | `contracts/review-lane-floor-snapshot.yaml` |
| M | `contracts/hermes-domain-overlay/examples/hermes-subject-overlay.example.yaml` |
| M | `contracts/hermes-domain-overlay/examples/negative/subject-undeclared-kind/hermes/subject/project-alfa/overlay.yaml` |
| M | `contracts/omnigent/examples/omnigent-install-manifest.example.yaml` |
| M | `contracts/omnigent/examples/fixtures/negative/manifest-dual-domain-overlay.yaml` |
| M | `contracts/omnigent/examples/fixtures/negative/manifest-legacy-vocabulary.yaml` |
| M | `contracts/omnigent/examples/fixtures/negative/manifest-missing-effective-profiles.yaml` |
| M | `contracts/omnigent/examples/fixtures/negative/manifest-parallel-identity.yaml` |
| M | `contracts/omnigent/examples/fixtures/negative/manifest-semantic-duplicate-worker.yaml` |

**None is this session's.** The archived
`2026-09-08-publish-openspec-cli-pin-as-contract-member` chose **A-defer**
(register now, cut later) over **A-cut** (`contract-v3.5` in that PR), and the
veto was not exercised — so its registration has been waiting for a bundle, and
**this is the bundle that publishes it** (re-cut as `contract-v3.6` on 2026-09-09 after #866 took v3.5 — see [#630 comment 5609442856](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5609442856)) — the A-defer choice
is a historical fact that stands; only the number this bundle carries moved. Task 5.3 and § *Version Identity*
require the entry to name every one of these; the attribution work is § 5.3's,
not an optional courtesy.

## R7 — The corpus, and three documents that misstate it

`ls examples/consent-instrument/*.example.yaml` → **6** (4 instruments, 1 class
registry, 1 purpose model). `ls examples/consent-instrument/negative/*.yaml` →
**7**. The validator's own self-test note agrees: *"6 valid example(s) …, 7
negative example(s) …, 2 purpose probe(s)"*.

Three documents say otherwise, and all three are already false BEFORE this
feature adds a byte:

| Document | Text | Named by a ratified task? |
| --- | --- | --- |
| `contracts/manifest.yaml:2034` | *"5 valid + 5 invalid + purpose probes"* | YES — task 4.9 |
| `examples/consent-instrument/README.md` | Layout tree + map table over 5/5 | YES — task 4.9 |
| `contracts/README.md:102` | *"self-testing over 5 positives, 5 indexed negatives, and 2 purpose probes"* | **NO** — clarify A1 adds it |

## R8 — The validator's shape

`scripts/validate-consent-instruments.py`, 862 lines. `Findings` carries
`errors` / `warnings` / `notes` and nothing else; `report()` returns
`1 if f.errors or (strict and f.warnings) else 0`. The docstring reads
`Exit codes: 0 ok, 1 findings, 2 dependency/harness error`.

`self_test` has exactly two loops — `EXAMPLES_DIR.glob("*.example.yaml")` (must
validate cleanly) and `NEGATIVE_DIR.glob("*.yaml")` against
`EXPECTED_NEGATIVE_FINDINGS` (must fail for a declared code, optionally
detail-pinned), each **fail-closed both ways**. `repo_scan` (layer 2) excludes
`EXAMPLES_DIR`.

`check_custody` walks every string under `custody` via `walk_strings`, skipping
only `custody.sha256`, and refuses `BASE64_BLOB_RX` (200+ base64 chars), a
`data:` prefix, `PDF_MAGIC_RX` and any embedded newline as
`embedded-original-content`.

## R9 — Nobody reads this validator's exit code

```bash
grep -rn 'validate-consent-instruments' \
  --include='*.yml' --include='*.yaml' --include='*.py' \
  --include='*.sh' --include='Makefile' . \
  | grep -v '^./.git' | grep -v '^./openspec/changes' | grep -v '^./specs/03'
ls .github/workflows/*.yml | wc -l     # 12
```

Every hit is a MENTION — the script's own usage line and print, four schema and
manifest comments naming it as the canonical validator, and three
`specs/007-client-identity-roster/traceability.yaml` rows. **Not one is an
INVOCATION**: `validate-consent-instruments.py` is run by no workflow, no
pytest, no Makefile and no consumer leg. This is the measurement that
refuted the "a withheld fixture would redden CI" premise of clarify Q2, and it
is why a new nonzero exit status is affordable. Existing `Exit codes:`
docstrings across `scripts/` are uniformly `0 / 1 / 2`; the only `3` in the tree
is `scripts/avatar-metering-alert.py`'s *"nothing crossed a paging threshold"*,
a different meaning. **The repository had ruled no status class for "needs a
human decision" — which is exactly what ratified task 3.4b asked for, and why
the question went to Brett Heap. HE RULED IT ON 2026-09-09**, by
multiple-choice selection, verbatim *"Exit 3 = needs a human decision
(Recommended)"*, declining *"Exit 1, same as findings"* and *"Exit 0, report
only"*; recorded by this lane at `2026-09-09T14:40:16Z`. **`3` is therefore the
repository's rule, established by this packet's realization**, and the lane
records it on issue #630.

## R10 — Test-package naming

```bash
ls tests/ | grep -i consent            # (no output)
ls tests/
```

No `tests/consent*` directory exists. Sibling packages mix conventions —
`tests/client-identity-roster`, `tests/doc-health`, `tests/intent-compliance`
(hyphen) against `tests/manifest_digests`, `tests/sequenced_after`,
`tests/scope_globs`, `tests/openspec_cli_pin` (underscore). **Ruled at Q7a:
`tests/consent_instruments/`.**

## R11 — Bookkeeping already performed

- **Task 0.1** — `tests/sequenced_after/corpus-ledger.yaml:82` reads
  `moved_by: "#774"`, the REAL merged pull request, stamped by commit
  `6cfe9ba6`. `validate-sequenced-after.py . --ledger-diff` reports *"per-change
  sweep ledger consistent with the corpus (189 rows)"*.
- **Task 1.1** — the record exists at `review/ratification-2026-09-08.md`;
  `Status: ratified` is on `proposal.md`, `design.md` and `tasks.md`; the
  `Ratified:` line is present; **the README OpenSpec Records row is already
  flipped** (`README.md:848`).
- **Tasks 1.2, 1.3** — the ratification record's *"Task 1.3's operator veto was
  NOT exercised"* section and its *"no veto was exercised on any of the eleven"*
  sentence rule both boxes as written.

## R12 — The ratification citation, and the one thing it cannot say

`gh api repos/opensoft/openxFactory/pulls/774/reviews` returns exactly one
review: `sourcery-ai[bot]`, `COMMENTED`, `2026-09-08T03:26:05Z`, at head
`ab27744b`. **No `APPROVED` state from any user exists.**

`gh api repos/opensoft/openxFactory/pulls/774` → `merged: true`,
`merged_by: brettheap`, `merged_at: 2026-09-08T03:48:44Z`,
`merge_commit_sha: 543d47a96970d48b1c988e2293927c800bb1ff08`, head `0d541576`,
`user: openxfactory[bot]`. Issue comments carry his `LANDING` at
`2026-09-08T03:48:41Z` and `LANDED … PR #774 → 543d47a9…` at
`2026-09-08T03:50:16Z`.

The immediately preceding realization (`specs/032`) could cite a CLI approval
(review `5141756427`, APPROVED `2026-09-08T12:38:36Z`). **This one cannot,
because none exists** — so every § 1 evidence note cites the in-repo record,
the operator's own merge and the LANDED comment instead. A note citing an
approval that was never given would be a false record.

## R13 — Baseline gate state on this branch, before a byte moves

| Gate | Result |
| --- | --- |
| `validate-openspec-cli-pin.py --change … --strict` | 1 passed, 0 failed |
| `validate-openspec-cli-pin.py --all --strict` | **100 passed, 2 failed — both DISPOSITIONED**, `0 UNDISPOSITIONED failures`. The two are the pre-existing `Merged into`-marker exceptions on `add-chain-attestation` and `add-composed-view-authoring`, accepted by Brett Heap 2026-09-05 (*"take exit 2"*). The ratification record measured the same pair at 98 passed; the count moved because other changes landed, the exceptions did not. **A third failure appearing is this feature's defect.** |
| `validate-consent-instruments.py --strict` | 0 errors, 0 warnings; 6 valid / 7 negative / 2 probes |
| `validate-manifest-digests.py` | 189 digests verify |
| `validate-sequenced-after.py . --ledger-diff` | consistent, 189 rows |
| `validate-scope-globs.py` | passed |

## R14 — Two consequences the review surfaced

- **A1** — `contracts/README.md:102` is a corpus-count surface no ratified task
  names. Corrected as an ADDITIONAL realization act.
- **A2** — `govern-archived-record-edits` (canon in both repositories) makes an
  edit of a pinned target REPORTED while its family has declared no
  re-derivation rule, and a REFUSAL **the day it declares**. `README.md:2993`
  records the premise verbatim: *"NO family anywhere has a declared
  re-derivation rule today — the consent family's is PROPOSED only
  (`contract_schema_version: 2`, no `custody_rederivations` property,
  `contract-v3.4`, 46/46 boxes unticked)"*. **Landing this realization falsifies
  all four clauses and DECLARES the rule.** The conversion to REFUSED still
  waits on F.2's gate, which is OpsxFactory's under § 7.1. **Recorded, never
  armed.**
