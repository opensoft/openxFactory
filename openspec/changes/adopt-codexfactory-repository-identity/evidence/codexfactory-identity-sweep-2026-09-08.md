# Recorded classification sweep — `opensoft/codexFactory` -> `codeXfactory/codexFactory`

**Change**: `adopt-codexfactory-repository-identity` (ratified 2026-09-07, merged PR #763 `eb30db7a`)
**Realizes**: tasks **2.1, 2.2, 2.3**, and the gating axis that tasks 3–5 need
**Realization head**: `e8021fed` (openxFactory `main`, 2026-09-08)
**Baseline compared against**: `64aad02e`, 2026-09-07 — 281 occurrences / 150 files
**Speckit feature**: `specs/030-realize-codexfactory-identity/`
**Lane**: `provenance-autonomous-merge`

**This file is EVIDENCE, not a decision.** It records a measurement and the
class the published rule assigns to each occurrence. It rules nothing, and where
it disagrees with the packet it says so and cites the rule rather than
substituting a judgment.

## 1. The command, recorded so the count is reproducible without this file

```sh
git grep -ic "opensoft/codexfactory" -- .
```

**`-ic`, not `-Ic`.** `-I` means "skip binary files" and leaves the match
case-SENSITIVE; run that way the same sweep reports **4** hits, because the
all-lowercase literal `opensoft/codexfactory` occurs exactly four times in the
corpus. The lowercase `-i` is the case-insensitive flag and is the one the
packet's command carries.

Per-class totals come from restricting the same pattern to each `design.md` § 2
pathspec:

```sh
cls() {
  label="$1"; shift
  git grep -ic "opensoft/codexfactory" -- "$@" \
    | awk -F: -v L="$label" '{s+=$NF; f++} END{printf "%-46s %4d %4d\n", L, s+0, f+0}'
}
cls "contracts (not signed-chain)  RENAME" 'contracts/' ':!contracts/signed-execution-chain/'
cls "tests                         RENAME" 'tests/'
cls ".github                       RENAME" '.github/'
cls "governance                    RENAME" 'governance/'
cls "scripts                       RENAME" 'scripts/'
cls "docs (not decisions)          RENAME" 'docs/' ':!docs/decisions/'
cls "README.md                     RENAME" 'README.md'
cls "signed-execution-chain        FROZEN" 'contracts/signed-execution-chain/'
cls "openspec archive              FROZEN" 'openspec/changes/archive/'
cls "specs                         FROZEN" 'specs/'
cls "docs/decisions                FROZEN" 'docs/decisions/'
cls "active packets            NOT SWEPT" 'openspec/changes/' ':!openspec/changes/archive/'
cls "ideation                  NOT SWEPT" 'ideation/'
cls "ALL                             ---" '.'
```

## 2. The measurement at `e8021fed` (task 2.1)

| class | pathspec | hits | files | disposition |
| --- | --- | ---: | ---: | --- |
| contracts-live | `contracts/` `:!contracts/signed-execution-chain/` | 30 | 23 | RENAME |
| tests | `tests/` | 23 | 8 | RENAME |
| workflows | `.github/` | 16 | 4 | RENAME |
| governance | `governance/` | 6 | 3 | RENAME (human-only surface) |
| scripts | `scripts/` | 5 | 3 | RENAME |
| docs-live | `docs/` `:!docs/decisions/` | 35 | 18 | RENAME |
| readme | `README.md` | 9 | 1 | RENAME, 3 lines FROZEN (§ 5) |
| **RENAME subtotal** | | **124** | **60** | |
| signed-chain | `contracts/signed-execution-chain/` | 44 | 34 | FROZEN — cryptographic |
| archive | `openspec/changes/archive/` | 15 | 10 | FROZEN — immutable |
| specs | `specs/` | 18 | 9 | FROZEN — dated verification |
| decisions | `docs/decisions/` | 1 | 1 | FROZEN — dated decision |
| **FROZEN subtotal** | | **78** | **54** | |
| active-packets | `openspec/changes/` `:!openspec/changes/archive/` | 106 | 36 | NOT SWEPT — owning lanes |
| ideation | `ideation/` | 19 | 13 | NOT SWEPT — pre-governance |
| **NOT SWEPT subtotal** | | **125** | **49** | |
| **TOTAL** | `.` | **327** | **163** | |

## 3. The arithmetic, closed against the baseline (task 2.2)

The packet closed at `64aad02e` on 2026-09-07 as
**281 / 150 = 123/60 + 78/54 + 80/36**. At the realization head it closes as
**327 / 163 = 124/60 + 78/54 + 125/49**. A drift in the total is expected — the
corpus moves daily. **A drift that does not classify under the published rule is
a finding.** There is none. Cause by cause:

| class | delta | attributed cause |
| --- | ---: | --- |
| RENAME | **+1 hit, +0 files** | `README.md` 8 → 9. The added occurrence is this packet's own OpenSpec Records entry, landed by PR #763 in the proposing commit (task 8.1). Classified `readme` / RENAME by pathspec; the per-line test then sends that particular line to the FREEZE (§ 5). |
| FROZEN | **0, 0** | none. The frozen set is byte-identical to the baseline, which is itself the first piece of freeze evidence: 44/34 signed-chain, 15/10 archive, 18/9 `specs/`, 1/1 `docs/decisions/`, unchanged. |
| active-packets | **+32 hits, +4 files** | **+29 hits / +4 files is this packet's own directory**, now on `main`: `.openspec.yaml` (1), `design.md` (16), `proposal.md` (7), `tasks.md` (5). Other lanes' packets are **77 / 32**, up +3 hits at unchanged file count — three occurrences added by owning lanes to packets that already carried some. NOT SWEPT either way (`proposal.md` § What this deliberately does not change). |
| ideation | **+13 hits, +9 files** | the OQ-3 ideation split (openxFactory #771, #772, #785, #786) reorganized `ideation/`, so brainstorm and staging fragments that already named the repository now count under different paths. Still pre-governance free-form input; still NOT SWEPT. |
| **TOTAL** | **+46 / +13** | fully attributed. **No finding is recorded under task 2.2.** |

## 4. Occurrences that appeared since the baseline, classified by the published rule (task 2.3)

Classified by rule — coverage test first, then the records-and-assertions test —
and **not** by a fresh judgment.

| new occurrence | rule applied | class |
| --- | --- | --- |
| `contracts/clearing/examples/negative/attestation-with-one-estate-wide-expected-set.yaml` and the other clearing negatives added by lane `hermes-wallet-exercise`'s `admit-deliberation-clearing-operation` | pathspec `contracts/**` outside `signed-execution-chain/`; an unsigned negative fixture asserts what a refusal looks like | **RENAME** |
| `openspec/changes/adopt-codexfactory-repository-identity/{.openspec.yaml,design.md,proposal.md,tasks.md}` (29) | active change packet, not archive. It is *this* packet, and its occurrences name the FORMER identity as the SUBJECT of the change | **NOT SWEPT** |
| `README.md:629` — this packet's OpenSpec Records entry | pathspec `README.md` → RENAME class; records-and-assertions test per line → the sentence records a dated measurement (`Measured at origin/main 64aad02e: 281 occurrences across 150 files`) | RENAME class, **FROZEN line** |
| the `ideation/` re-count (+13/+9) | pathspec `ideation/**` | **NOT SWEPT** |
| three further occurrences in other lanes' active packets | active change packet, not archive | **NOT SWEPT** |

**A packet count corrected, not absorbed.** Task 3.8 names *"the four negatives
under `examples/negative/`"*, six clearing files in total. At this head there are
**five** negatives carrying the string —
`attestation-claiming-full-completeness-before-admission.yaml` (2),
`attestation-filing-a-dark-lane-as-a-widening.yaml` (2),
`attestation-with-one-estate-wide-expected-set.yaml` (1),
`deliberation-return-carrying-a-verdict.yaml` (1),
`deliberation-return-that-does-not-match-its-shape.yaml` (1) — so the clearing
corpus is **seven files / eleven occurrences**, not six. The fifth negative
arrived after 2026-09-07. The rule classifies it; the count is corrected here.

**A packet premise falsified, and recorded rather than worked around.** Task 5.4
says the custody attestation *"names the repository"*.
`governance/factory-identity/attestations/custody-attest-wal-origin-codexfactory-0001.yaml`
carries **no `opensoft/` owner segment at all** — only the BARE forms
`wal-origin-codexfactory-0001`, `grant-origin-codexfactory-0001`,
`attest-custody-wal-origin-codexfactory-0001` and the prose *"codexFactory's own
hosted packaging environment"*. Task 6.4 is explicit that a transfer moves the
OWNER segment only and that bare member names are correct before and after, so
5.4's respell half is a **no-op** and editing the file would violate 6.4. Its
validator half still runs.

## 5. `README.md` per line, as task 4.8 requires

The packet's line numbers (316, 409, 530, 531, 642, 644, 1172, 1184) have
shifted — the README grew — and there are now nine occurrences, not eight.
The records-and-assertions test applied per line, with the outcome recorded:

| line | what it is | verdict |
| ---: | --- | --- |
| 316 | *"Engineering-domain implementation docs now belong in `opensoft/codexFactory`."* | **RENAME** — asserts what IS |
| 409 | the `## Domain Implementations` list entry naming the engineering domain stack | **RENAME** — asserts what IS |
| 629 | this packet's own Records entry: *"… `opensoft/codexFactory` as repository identity inside governed contract content. Measured at `origin/main` `64aad02e`: 281 occurrences across 150 files …"* | **FROZEN** — records a dated measurement, and the former identity is the change's SUBJECT. Respelling it would make the record claim the change is about the identity it moves TO |
| 678 | `[codexFactory #232](https://github.com/opensoft/codexFactory/issues/232)` | **RENAME** — kept-current index citation; issue NUMBERS carry through a transfer |
| 679 | `[codexFactory #272](https://github.com/opensoft/codexFactory/pull/272)` | **RENAME** — same |
| 790 | `[#232](https://github.com/opensoft/codexFactory/issues/232)` | **RENAME** — same |
| 792 | `[#203](https://github.com/opensoft/codexFactory/issues/203)` | **RENAME** — same |
| 1335 | *"… the first originating repository `opensoft/codexFactory` — plus the disjointness validator …"*, inside **REALIZATION COMPLETE AT THIS PR** | **FROZEN** — narrates a completed dated act |
| 1347 | *"The realization for `opensoft/codexFactory` is therefore COMPLETE at this PR"* | **FROZEN** — same |

**Consequence for task 6.5.** Three `README.md` lines join the freeze, so the
frozen total for the *"zero remaining live occurrences outside the frozen and
not-swept sets"* check is **81 occurrences**, not 78. The FILE count does not
move: `README.md` is a mixed file, renamed in six lines and frozen in three.
Task 4.8 asked for exactly this — *"decide against the test, do not sweep, and
record which way each went"* — and named two candidates; a third (line 629) did
not exist when the packet was written.

## 6. The second axis: the transfer has not happened (the gating class)

**This is the one thing this evidence file adds that the packet does not carry,
and it exists because of a fact rather than a preference.** The GitHub transfer
is an OPERATOR act, it is unperformed at this head, and the runbook places the
whole governed realization at **Phase 10 — after the Phase 1 transfer**. This
realization was launched early on the convener's word, which creates a state the
packet does not describe.

Measured, not assumed:

```sh
gh api repos/codeXfactory/codexFactory --jq '.full_name'
# {"message":"Not Found", ... "status":"404"}
gh api repos/opensoft/codexFactory --jq '{full_name,private,visibility}'
# {"full_name":"opensoft/codexFactory","private":true,"visibility":"private"}
gh api orgs/codeXfactory --jq '.plan.name'
# enterprise      (OQ-1, verified 2026-09-07T16:41:04Z)
```

**GitHub redirects OLD→NEW after a transfer and never NEW→OLD before it**, so a
reference respelled early gets no grace period at all — the opposite of the
grace `proposal.md` § Why discusses. The test applied to each RENAME occurrence:

> An occurrence is **SAFE NOW** iff respelling it (1) states nothing false about
> the present **and** (2) breaks no resolution that works today.

| occurrence shape | (1) false today? | (2) breaks today? | verdict |
| --- | --- | --- | --- |
| synthetic example / negative fixture `repository:` illustrating a shape | no | no | **SAFE NOW** |
| the real domain's canonical key in the regression denominator | yes | no | GATED |
| a workflow `repository:` consumed by `actions/checkout` | yes | **yes** — `pytest-suite`, `merge-master-approval`, both required checks | GATED |
| `SOURCE_REPOSITORY` passed to `gh api repos/<x>` | yes | **yes** | GATED |
| the origin register a live sealed request is compared against | yes | **yes, in reverse** — it would refuse today's real dispatches | GATED |
| a `gh api` line an operator pastes from a runbook | yes | **yes, at the terminal** | GATED |
| a `https://github.com/opensoft/codexFactory/...` citation URL | yes | **yes** — 404 until the move | GATED |
| prose asserting where engineering content lives, in the present tense | yes | no | GATED |
| a mapping row carrying `transferred_on` | yes — the act has not happened | no | GATED |

Two of those are worth stating in full because they are not obvious:

- **`.github/workflows/pytest-suite.yml:396` is a literal `uses: actions/checkout@v4`
  with `repository: opensoft/codexFactory`**, and `merge-master-approval.yml`
  checks out the same at the commit `contracts/review-lane-pin.yaml` pins.
  Respelling either today reds a required check on every openxFactory pull
  request, including other lanes'.
- **Re-issuing the origin register early performs the revocation in the wrong
  direction.** `scripts/validate-clearing-dispatch.py` compares a sealed
  request's `origin.repository` against
  `governance/factory-identity/register.yaml`, and codexFactory's live
  dispatches today originate at `opensoft/codexFactory`. Respelling the register
  now refuses TODAY's real requests — the same revocation `design.md` § 4.3
  warns the transfer will cause, applied a day early.

**Runbook step 1.2** is named as the gate on every held pull request because it
is the first step at which the new address is proved to exist:
*"OPERATOR. Confirm the destination and the visibility … MUST read
`codeXfactory/codexFactory`, `private: true`."*

## 7. The gating class per file, and the closed arithmetic

| file | hits | path class | slice / gate |
| --- | ---: | --- | --- |
| `.github/merge-approval-envelope.yml` | 1 | workflows | B1 gated:1.2 |
| `.github/workflows/merge-master-approval.yml` | 12 | workflows | B1 gated:1.2 |
| `.github/workflows/pytest-suite.yml` | 1 | workflows | B1 gated:1.2 |
| `.github/workflows/review-lane-repin.yml` | 2 | workflows | B1 gated:1.2 |
| `README.md` | 9 | readme | B4 gated:1.2 |
| `contracts/clearing/examples/deliberation-return.example.yaml` | 1 | contracts-live | B2 gated:1.2 HUMAN-ONLY |
| `contracts/clearing/examples/factory-identity-fixture/register.yaml` | 2 | contracts-live | B2 gated:1.2 HUMAN-ONLY |
| `contracts/clearing/examples/negative/attestation-claiming-full-completeness-before-admission.yaml` | 2 | contracts-live | B2 gated:1.2 HUMAN-ONLY |
| `contracts/clearing/examples/negative/attestation-filing-a-dark-lane-as-a-widening.yaml` | 2 | contracts-live | B2 gated:1.2 HUMAN-ONLY |
| `contracts/clearing/examples/negative/attestation-with-one-estate-wide-expected-set.yaml` | 1 | contracts-live | B2 gated:1.2 HUMAN-ONLY |
| `contracts/clearing/examples/negative/deliberation-return-carrying-a-verdict.yaml` | 1 | contracts-live | B2 gated:1.2 HUMAN-ONLY |
| `contracts/clearing/examples/negative/deliberation-return-that-does-not-match-its-shape.yaml` | 1 | contracts-live | B2 gated:1.2 HUMAN-ONLY |
| `contracts/clearing/examples/single-door-attestation.example.yaml` | 3 | contracts-live | B2 gated:1.2 HUMAN-ONLY |
| `contracts/hermes-domain-overlay/examples/hermes-subject-overlay.example.yaml` | 1 | contracts-live | A safe-now |
| `contracts/hermes-domain-overlay/examples/negative/subject-undeclared-kind/hermes/subject/project-alfa/overlay.yaml` | 1 | contracts-live | A safe-now |
| `contracts/hermes-runtime/README.md` | 1 | contracts-live | B3 gated:1.2 |
| `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` | 1 | contracts-live | B3 gated:1.2 |
| `contracts/hermes-runtime/fixtures/regression/digest-mismatch.yaml` | 1 | contracts-live | B3 gated:1.2 |
| `contracts/hermes-runtime/fixtures/regression/duplicate-repository.yaml` | 1 | contracts-live | B3 gated:1.2 |
| `contracts/hermes-runtime/fixtures/regression/missing-exclusion-reason.yaml` | 1 | contracts-live | B3 gated:1.2 |
| `contracts/omnigent/examples/fixtures/negative/manifest-dual-domain-overlay.yaml` | 1 | contracts-live | A safe-now |
| `contracts/omnigent/examples/fixtures/negative/manifest-legacy-vocabulary.yaml` | 1 | contracts-live | A safe-now |
| `contracts/omnigent/examples/fixtures/negative/manifest-missing-effective-profiles.yaml` | 1 | contracts-live | A safe-now |
| `contracts/omnigent/examples/fixtures/negative/manifest-parallel-identity.yaml` | 1 | contracts-live | A safe-now |
| `contracts/omnigent/examples/fixtures/negative/manifest-semantic-duplicate-worker.yaml` | 1 | contracts-live | A safe-now |
| `contracts/omnigent/examples/omnigent-install-manifest.example.yaml` | 1 | contracts-live | A safe-now |
| `contracts/review-lane-pin.yaml` | 2 | contracts-live | B1 gated:1.2 |
| `contracts/review-lane-repin-binding.template.yaml` | 2 | contracts-live | B1 gated:1.2 |
| `docs/architecture.md` | 1 | docs-live | B4 gated:1.2 |
| `docs/contract-versioning-policy.md` | 1 | docs-live | B3 gated:1.2 |
| `docs/deployment-worker-model.md` | 1 | docs-live | B4 gated:1.2 |
| `docs/dogfood-content-migration-plan.md` | 2 | docs-live | B4 gated:1.2 |
| `docs/factory-origin-key-mint-runbook.md` | 6 | docs-live | B1 gated:1.2 |
| `docs/feature-decomposition.md` | 1 | docs-live | B4 gated:1.2 |
| `docs/governed-reissuance-runbook.md` | 1 | docs-live | B4 gated:1.2 |
| `docs/merge-council.md` | 1 | docs-live | B4 gated:1.2 |
| `docs/merge-master.md` | 1 | docs-live | B4 gated:1.2 |
| `docs/omnigent-constitution.md` | 2 | docs-live | B4 gated:1.2 |
| `docs/pr-admission.md` | 1 | docs-live | B4 gated:1.2 |
| `docs/review-lane-repin-runbook.md` | 5 | docs-live | B1 gated:1.2 |
| `docs/roles-and-authority.md` | 3 | docs-live | B4 gated:1.2 |
| `docs/spec-kit-stage-ownership.md` | 1 | docs-live | B4 gated:1.2 |
| `docs/terminology-and-repo-topology.md` | 1 | docs-live | B3 gated:1.2 |
| `docs/traceability-model.md` | 3 | docs-live | B4 gated:1.2 |
| `docs/workflow-contract.md` | 1 | docs-live | B4 gated:1.2 |
| `docs/xfactory-domain-factory-model.md` | 3 | docs-live | B3 gated:1.2 |
| `governance/factory-identity/grants/grant-origin-codexfactory-0001.yaml` | 3 | governance | B2 gated:1.2 HUMAN-ONLY |
| `governance/factory-identity/register.yaml` | 2 | governance | B2 gated:1.2 HUMAN-ONLY |
| `governance/factory-identity/wallets/wal-origin-codexfactory-0001.yaml` | 1 | governance | B2 gated:1.2 HUMAN-ONLY |
| `scripts/doc_health/pin_class.py` | 1 | scripts | B1 gated:1.2 |
| `scripts/mint-factory-origin-key.py` | 3 | scripts | B1 gated:1.2 |
| `scripts/review_lane_repin.py` | 1 | scripts | B1 gated:1.2 |
| `tests/clearing/test_attestation.py` | 3 | tests | B2 gated:1.2 HUMAN-ONLY |
| `tests/clearing/test_origin_signature.py` | 5 | tests | B2 gated:1.2 HUMAN-ONLY |
| `tests/factory_identity/test_mint_script.py` | 1 | tests | B1 gated:1.2 |
| `tests/factory_identity/test_validator.py` | 8 | tests | B2 gated:1.2 HUMAN-ONLY |
| `tests/hermes_runtime_contracts/test_domain_regression.py` | 2 | tests | B3 gated:1.2 |
| `tests/review_lane_pin/test_floor_snapshot.py` | 1 | tests | B1 gated:1.2 |
| `tests/review_lane_pin/test_repin_lane.py` | 2 | tests | B1 gated:1.2 |
| `tests/review_lane_pin/test_review_lane_caller.py` | 1 | tests | B1 gated:1.2 |

| slice / gate | hits | files |
| --- | ---: | ---: |
| A safe-now | 8 | 8 |
| B1 gated:1.2 | 41 | 15 |
| B2 gated:1.2 HUMAN-ONLY | 35 | 14 |
| B3 gated:1.2 | 12 | 9 |
| B4 gated:1.2 | 28 | 14 |
| **RENAME total** | **124** | **60** |

**The arithmetic closes on both axes.** 8 + 41 + 35 + 12 + 28 = **124** hits and
8 + 15 + 14 + 9 + 14 = **60** files, matching the RENAME subtotal of § 2 exactly.
No occurrence is `UNASSIGNED`.

## 8. What each slice is, and which pull request carries it

| slice | gate | pull request | packet tasks |
| --- | --- | --- | --- |
| **A** — 8/8: the six omnigent example fixtures and the two hermes-domain-overlay examples | **SAFE NOW** | the feature's normal pull request, with this evidence file | 3.9, 3.10 |
| **B1** — 41/15: the decision-core pin and everything that asserts it, `merge-master-approval.yml`, `pytest-suite.yml`, the envelope citation, the mint script, and the two operator runbooks | **GATED — runbook step 1.2** | DRAFT | 3.5, 3.6, 3.7, 3.12, 4.5 |
| **B2** — 35/14: the origin register, wallet and grant, the clearing corpus, and the tests that assert the live register | **GATED — runbook step 1.2**, and **HUMAN MERGE WORD ONLY** | DRAFT | 5.1–5.6, 3.8, 3.11, 3.13 |
| **B3** — 12/9: the eight `contract-v3.4` inventoried members plus the test that pins the denominator | **GATED — runbook step 1.2** | DRAFT | 3.1, 3.2, 3.3, 3.4, 4.2, 4.3, 4.4 |
| **B4** — 28/14: the remaining live documents and `README.md` (25 respelled, 3 frozen) | **GATED — runbook step 1.2** | DRAFT | 4.1, 4.6, 4.7, 4.8 |
| **B5** — the mapping row | **GATED — runbook step 1.2** *and* **BLOCKED** | not opened; the row is prepared verbatim at `specs/030-realize-codexfactory-identity/contracts/repository-identity-row.md` | 1.1–1.4 |

**Why B3 is one slice and not four.** Re-verified at this head against
`contracts/releases/contract-v3.4.digests.yaml` (283 entries): all eight named
members are present, and **none of the other 52 renamed files is**, so
`design.md` § 5's arithmetic holds unchanged. None of the eight is in
`scripts/doc_health/release_inventory.py`'s three-path `EDITORIAL` set, so each
moved blob is an `ERROR`-severity `release-inventory-drift` finding and a red
`verify-commit` until the cut re-baselines the inventory. **Splitting the eight
puts a subset of that transient on `main` with no cut available to repair it**,
because a cut needs all eight.

## 9. The blocker on task 1.1, recorded because it cannot be worked around

**`contracts/policies/repository-identity.yaml` does not exist on `main`.**

```sh
git ls-tree origin/main -- contracts/policies/repository-identity.yaml   # empty
```

Task 1.1 says, in as many words, *"Do not create the file here"* —
`adopt-medxsoft-repository-identity` authors it at ITS task 1.1 and registers it
in `contracts/manifest.yaml` at its task 1.3, and *"authoring it twice would
produce two files claiming to be the mapping."* That change is active on `main`,
`Status: draft`, and **unrealized**; no Speckit feature under `specs/` realizes
it. Task **0.2**'s conditional — *"if that change is archived or withdrawn …
task 1.1 changes from 'add a row' to 'author the file'"* — does **not** fire,
because it is neither archived nor withdrawn. **So the premise of 0.2 holds, the
instruction of 1.1 stands, and group 1 waits on the exemplar.**

Two independent gates hold the row, and both must lift:

1. **BLOCKED** — the exemplar's task 1.1 must land the file (and its task 1.3
   the manifest entry), **or** the convener must amend task 1.1 to author the
   file here.
2. **GATED at runbook step 1.2** — `transferred_on` records a completed act, so
   the row cannot be finished before the transfer is confirmed.

The row's full text, ready to apply, is at
`specs/030-realize-codexfactory-identity/contracts/repository-identity-row.md`
and carries everything tasks 1.1, 1.2 and 1.3 require: `former`, `current`,
`transferred_on` (placeholder), the redirect-lapse note, the case-sensitivity
divergence, the GHCR lowercasing recorded as a derived tool-imposed spelling per
**OQ-6** (ruled 2026-09-08T03:51Z), and the three reference shapes the redirect
does not cover.

## 10. A name that collides and is unrelated

`disposition-codexfactory-declared-renames` is the one pre-existing
`openspec validate --all --strict` failure and its name reads like this work.
**It is not.** It disposes of **OpenSpec CLI 1.12.0 scenario-currency findings**
over two declared, ratified **SCENARIO retitles** in codexFactory changes
(`add-regular-pr-council-clearance`, `amend-composition-selector-labelling`) by
adding two `dispositions:` entries to `contracts/openspec-cli-pin.yaml`. It has
nothing to do with repository renames, it is **not** the sweep-record mechanism
group 2 could have used, and it fails `--strict` because it is a deltaless
packet — `Status: ratified`, realized on the openxFactory main line, awaiting
archive. `proposal.md` § Impact predicts the same result and this sweep confirms
it: the failure is neither caused nor repaired here.

## 11. Self-reference

**This file lands inside the `active-packets` class and adds its own
occurrences to it.** The measurement in § 2 was therefore taken at `e8021fed`,
**before** this file existed, and every count above is against that tree — which
is also why the § 2 numbers are reproducible from § 1's commands only at
`e8021fed`, not at the pull request's head. A later re-run of the sweep reads a
known delta rather than an unexplained one: this file's own occurrences, plus the
eight slice-A occurrences that leave the RENAME class when slice A lands.

## 12. Recorded validator and check results at this evidence's head

Run in the feature worktree, on the tree carrying slice A only.

| check | invocation | result |
| --- | --- | --- |
| omnigent contracts (task 3.9) | `python3 scripts/validate-omnigent-contracts.py` — **no argument**; a path argument selects REPO mode, which fails on this tree because openxFactory is not a domain repository | `All omnigent contract checks passed` — every one of the six respelled fixtures still rejected for its own reason |
| hermes-domain-overlay (task 3.10) | `python3 scripts/validate-hermes-domain-overlay.py .` | `self-test ok: 23 fixture(s)`, `repo validation ok`; `subject-undeclared-kind/` still fails for the undeclared-kind reason |
| signed execution chain (task 6.2) | `python3 scripts/validate-signed-execution-chain.py .` | `0 error(s), 0 warning(s)`; `113 packaged record(s) validated across 2 coherent corpora, 108 negative fixture(s) confirmed invalid for their intended reason, 95/95 closed refusal codes red-proven`. **This is the recorded evidence that no corpus-wide `sed` was run** |
| OpenSpec, this change (task 8.2) | `OPENSPEC_TELEMETRY=0 openspec validate adopt-codexfactory-repository-identity --strict` | `Change 'adopt-codexfactory-repository-identity' is valid` |
| OpenSpec, corpus (task 8.2) | `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` | `Totals: 99 passed, 1 failed (100 items)`. The single failure is `change/disposition-codexfactory-declared-renames` — the pre-existing deltaless packet of § 10. The packet predicted `98 passed / 1 failed`; the corpus has since grown by one item, and the FAILURE COUNT and its identity are unchanged, which is what the prediction was about |
| sequenced-after (task 8.3) | `python3 scripts/validate-sequenced-after.py . --ledger-diff` | green — `per-change sweep ledger consistent with the corpus (183 rows)`; this change is among the 10 active changes declaring the field; `DEEPEST DECLARED CHAIN RESOLVED: 2 hop(s)`; no cycle |
| freeze by diff (tasks 6.1, 6.3) | `git diff --stat origin/main -- <frozen and not-swept pathspecs>` | **empty** for `contracts/signed-execution-chain/`, `openspec/changes/archive/`, `docs/decisions/`, `ideation/`, `specs/` outside this feature's directory, and `openspec/changes/` outside this packet's directory |
| bare-name check (task 6.4) | the per-file comparison in `specs/030-realize-codexfactory-identity/quickstart.md` § 6 | **PASS** — 8 pre-existing files changed, owner-less `codexFactory` count identical in all 8; `git diff --diff-filter=R` empty, so no file was renamed either |

### A correction to the packet's predicted transient (task 7.5)

Task 7.5 predicts that `release-inventory-drift` reports **eight** `ERROR`
findings between the renames and the cut, implying a baseline of zero.
**The baseline is one, not zero.** Measured on the tree carrying slice A only —
which touches no inventoried member:

```sh
python3 scripts/doc-health.py --single-repo . --family release-inventory-drift
# severity=error family=release-inventory-drift path=docs/contract-versioning-policy.md
#   rule="bytes differ from the digest 'contract-v3.4' records" class="auto-fixable"
# severity=info  ... path=contracts/README.md      (editorial member — expected between cuts)
# severity=info  ... path=contracts/manifest.yaml  (editorial member — expected between cuts)
```

`git diff origin/main -- docs/contract-versioning-policy.md` is empty, so the
`ERROR` is **pre-existing on `main`** and not caused by this realization: that
file already drifts from the `contract-v3.4` digest and already owes the next
cut. The other two are `EDITORIAL` members reporting at `info`, which is the
family's documented between-cuts state.

**Consequence, recorded so nobody reads a miscount as a defect**: when slice B3
lands, the family reports **eight** `ERROR` findings — the seven inventoried
members this realization moves that are not already drifting, plus the one
already drifting. It does NOT report nine. The predicted number is right; the
arithmetic behind it is one member different, and that member's drift is somebody
else's owed cut, discharged by the same cut this change owes.

---

## 13. Addendum: the corpus moved WHILE this sweep was being filed

Recorded because the packet's task 2.2 says *"a drift in the total is expected
(the corpus moves daily); a drift that does not classify under the published
rule is a finding"* — and the honest way to discharge that is to show the drift
happening rather than to describe it.

**Between this sweep's head `e8021fed` and the pull request that files it,
openxFactory `main` advanced nine commits to `e7c53012`** — Brett Heap merged
PR **#783** (`adopt-configured-notebook-hosting-identity`, ratified
2026-09-08, *"Ratify 783 and merge"*). What it moved that matters here:

- **`README.md`** — a new OpenSpec Records entry. **It added no
  `opensoft/codexFactory` occurrence**: the file still carries exactly nine, and
  the per-line verdicts of § 5 are unchanged. The LINE NUMBERS shifted for the
  second time since the packet was written (629 → 704, 678/679 → 753/754,
  790/792 → 865/867, 1335 → 1410, 1347 → 1422), which is why § 5 records a
  verdict per line CONTENT and the rename is applied against that set
  programmatically — a script that refuses on any `README.md` occurrence it has
  no verdict for, so a tenth occurrence is a stop and never a silent sweep.
- **`tests/sequenced_after/corpus-ledger.yaml`** — one row added, so the
  `--ledger-diff` gate had to be re-run rather than trusted.

### Re-measured at the merged head (this pull request's tip)

| class | at `e8021fed` | at the merged tip | attributed cause |
| --- | ---: | ---: | --- |
| contracts-live RENAME | 30 / 23 | **22 / 15** | **slice A landed**: the six omnigent and two hermes-domain-overlay example fixtures left the class, exactly 8 hits / 8 files |
| tests, `.github`, governance, scripts, docs-live, README RENAME | 94 / 37 | 94 / 37 | unchanged — every remaining rename is held in a draft slice |
| `specs/**` FROZEN | 18 / 9 | **54 / 17** | **+36 / +8 is this feature's own documents** (`specs/030-realize-codexfactory-identity/`, 30 occurrences plus 6 more across the checklist and contract fragment). A Speckit feature's spec, plan, research and task list are dated point-in-time plans, which is exactly what the `specs/**` class freezes; they name the former identity as the SUBJECT of the work |
| active packets NOT SWEPT | 106 / 36 | **123 / 37** | **+17 / +1 is THIS EVIDENCE FILE**, the self-reference § 11 predicted |
| other classes | — | unchanged | — |
| **TOTAL** | 327 / 163 | **372 / 164** | fully attributed; **still no occurrence that fails to classify under the published rule** |

### Gates re-run at the merged head

| check | at `e8021fed` | at the merged tip |
| --- | --- | --- |
| `openspec validate --all --strict` | `99 passed, 1 failed` | **`100 passed, 1 failed`** — the corpus gained #783's change; the FAILURE is still exactly `change/disposition-codexfactory-declared-renames` and nothing else |
| `validate-sequenced-after.py . --ledger-diff` | green, 183 rows | **green, 184 rows** — the ledger tracked #783's new row, so it is consistent rather than stale |
| `release-inventory-drift` | 1 `ERROR` (pre-existing) | 1 `ERROR` (pre-existing) — slice A moves no inventoried member |

**The point of this addendum is the mechanism, not the numbers.** A hand
enumeration of 124 paths would now be wrong in its line numbers for the second
time in two days. A rule over path classes plus a re-runnable command is right
at every head, and that is the substance of the packet's third new requirement.

---

## 14. The gate FIRED, and it refined itself

Slice B1's pull request (openxFactory **#801**) ran `pytest-suite` and it went
**RED** — which is the classification of § 6 being proved rather than argued.
The run:

```
selected=10333 passed=10310 skipped=23 failures=0 errors=0
floors: selected>=7090 (margin 3243) passed>=7070 (margin 3240) skipped==21
```

**Zero failures, zero errors, both floors clear by ~3,240 — no test regressed.**
The job failed on three assertions that are all one fact:

```
##[error] skipped 23, pinned exactly 21 — a directory that silently turned into
         skips is exactly what this pin exists to catch
##[error] snapshot freshness verifier did not run — pinned core checkout unavailable
         (tests.review_lane_pin.test_floor_snapshot.TheFreshnessVerifier::
          test_the_snapshot_is_byte_identical_to_the_pinned_core is 'skipped')
##[error] vector replay did not run — pinned core checkout unavailable
         (tests.review_lane_pin.test_floor_snapshot.TheVectorReplay::
          test_every_vector_replays is 'skipped')
```

`.github/workflows/pytest-suite.yml`'s *"Check out the pinned decision core"*
step now names `repository: codeXfactory/codexFactory`, which does not exist.
The step is `continue-on-error: true`, so the two cross-repository tests SKIP
rather than error — the skipped count moves 21 → 23 and the two named verifiers
report `skipped` where the workflow demands `passed`.

**`EXPECT_SKIPPED: 21` is therefore a live, fail-closed probe for whether the
cross-repository checkout resolved.** After the transfer and the App re-grant,
`pytest-suite` on that branch must read `skipped=21` with both verifiers
`passed`; that number is the merge-time check, and it is better evidence than
reading the checkout step's own warning because it is a required check.

### The refinement: slice B1's gate is Phase 1 COMPLETE, not step 1.2 alone

Step **1.2** only confirms the repository exists. The checkout authenticates
with `steps.app-token.outputs.token`, minted by the openxFactory GitHub App —
and **App installations are per organization and do NOT travel with a transfer**
(`design.md` § 7, item 6). So slice B1 additionally needs runbook step **1.6**
(*reinstall the Apps on `codeXfactory` and re-grant repository access*).
Without it the repository exists, the token still cannot read it, and
`pytest-suite` stays red for the same three assertions.

Runbook step **1.3** (`access_level=enterprise`) governs cross-organization
**reusable-workflow `uses:` resolution** — what OQ-1 exists for — and is a
precondition of the aggregation's `uses:` paths in Phase 2 rather than of this
`actions/checkout`. All three steps sit inside the Phase 1 window, so the
practical instruction keeps its shape: **the gated slices merge after Phase 1
completes**, and "runbook step 1.2" on their pull requests should be read as
"Phase 1 complete, 1.6 included".

**Recorded rather than corrected in place** on the slice pull requests, because
the runbook is the operator's document and this is a finding about it, not an
edit to it.
