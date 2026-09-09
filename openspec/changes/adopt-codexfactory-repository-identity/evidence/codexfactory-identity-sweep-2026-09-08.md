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

---

## 15. Addendum: group 1 realized under the amended task 1.1, and TWO new occurrence classes

**Task 1.1 was AMENDED on 2026-09-08** by Brett Heap (convener), interactive
walkthrough, verbatim **"Amend task 1.1: this change creates the file
(Recommended)"** — resolving the blocker § 9 recorded. Record:
`review/amendment-2026-09-08-task-1-1.md`. Slice A merged first as PR **#799**,
merge commit `131adf11`, 2026-09-08T14:32:34Z; this addendum is measured on the
branch `030-mapping-row-amendment`, cut from `origin/main` at that merge.

`contracts/policies/repository-identity.yaml` now exists, carrying the schema
both repositories' rows need and the codexFactory row. Tasks **1.2** and **1.3**
are realized on the row as written; task **1.4** is RE-DERIVED — the
`contracts/manifest.yaml` entry, its `consumption_rule` and the computed
per-file `sha256` are owed HERE, not by the exemplar, because the file it
registers is now authored here.

### 15.1 A NEW disposition class: the mapping's own lookup key

The new file adds **2 occurrences of `opensoft/codexFactory` inside a
`contracts/**` path** — the RENAME class by pathspec:

```
contracts/policies/repository-identity.yaml:2
```

They are `former: opensoft/codexFactory` and the row's own section comment.
**They are the mapping's LOOKUP KEY and must never be renamed** — renaming them
would delete the very entry that makes every frozen spelling resolvable, and the
rule would be eating itself. This is a class the packet's § 2 table has no row
for, because at authoring time the file did not exist:

| class | hits | files | disposition |
| --- | ---: | ---: | --- |
| **mapping key** — `contracts/policies/repository-identity.yaml` | **2** | **1** | **PERMANENTLY the former spelling, by construction** |

**Consequence for task 6.5.** *"Zero remaining live occurrences of
`opensoft/codexFactory` outside the frozen and not-swept sets"* must exclude the
mapping file, exactly as it already excludes the frozen sets. Stated here so a
later reader does not respell the key to satisfy a literal count.

### 15.2 A NEW occurrence no slice covers: `governance/review-authority/grants/grant-grc-0001.yaml`

Discharging task **2.3** at this head found an occurrence that did not exist at
`e8021fed`:

```
governance/review-authority/grants/grant-grc-0001.yaml:2
```

Added by commit `4719f07f`, *"Register act §3.3–3.7: commission
agent:gate-rules-council (PLACEHOLDERS)"*, Brett Heap, 2026-09-07 — the
`register-gate-rules-council-seats` mint-and-register ceremony.

**Classified by the published rule, not by fresh judgment**: `governance/**` →
RENAME. But both occurrences are unusual enough to write out, because they are
**counterfactual**: they appear in a header comment explaining why `objects:` is
`opensoft/openxFactory` and deliberately **NOT** `opensoft/codexFactory` —

> `objects: [opensoft/openxFactory]` — STANDS, AND IT NEEDS AN EXPLICIT
> SENTENCE BECAUSE IT LOOKS WRONG AT FIRST READING. This body governs
> codexFactory's gate rules, so a reader expects `opensoft/codexFactory`
> here. … A row naming `opensoft/codexFactory` would be a row this estate
> cannot resolve, not a wider authority.

The sentence is present-tense and asserts what a reader *would expect*, so it
respells at the transfer to keep being true. **It is NOT edited by this lane, and
it is in no open slice.** Three reasons, in order of weight:

1. It belongs to **another lane's live ceremony artifact**, mid-construction, with
   unfilled `@@…@@` operator placeholders and five Ed25519 keypairs Brett mints
   on his own host. The commit message says the work *"MUST NOT be pushed until
   the values are substituted"*.
2. It is a **review-authority grant** — a key-custody surface, adjacent to the
   permanently human-only class.
3. The four rename slices are already authored and under review; adding a file to
   one of them now would collide with that review.

**Disposition: RENAME, deferred to the `register-gate-rules-council-seats` lane's
next touch, or to a fifth slice after that ceremony completes.** Flagged on
codexFactory issue #279 so the owning lane reads it rather than discovering it.

### 15.3 The arithmetic, re-closed at this head

| bucket | hits | files |
| --- | ---: | ---: |
| slice A — LANDED in #799 | −8 | −8 |
| B1 #801 + B2 #802 + B3 #805 + B4 #806, still open | 116 | 52 |
| **NEW, unassigned** — `grant-grc-0001.yaml` (§ 15.2) | **2** | **1** |
| **NEW, never renamed** — the mapping key (§ 15.1) | **2** | **1** |
| **total in RENAME pathspecs at this head** | **120** | **54** |

Measured: `git grep -ic "opensoft/codexfactory"` over the RENAME pathspecs
returns **120 / 54**. `116 + 2 + 2 = 120` and `52 + 1 + 1 = 54` — **it closes**,
and the RENAME subtotal of § 2 rises from 124 to **126** for the two new
occurrences, one of which is never swept.

### 15.4 Group 6 re-verified against the new file

| check | result |
| --- | --- |
| **6.1** frozen classes byte-unchanged (`contracts/signed-execution-chain/`, `openspec/changes/archive/`, `docs/decisions/`, `specs/`) | **empty diff** |
| **6.2** `validate-signed-execution-chain.py .` | **`0 error(s), 0 warning(s)`** |
| **6.3** not-swept: other lanes' active packets and `ideation/` | **empty diff** |
| **6.4** no bare name edited | **PASS** — all four changed pre-existing files are **ADD-ONLY**, so nothing could have been edited. **The check itself had to be rewritten**: see § 15.5 |
| **6.5** live occurrences outside frozen / not-swept / **mapping key** | 118 — the 116 held in the four gated slices plus § 15.2's 2, all accounted |

### 15.5 The 6.4 check was WRONG for an add-only diff, and is now fixed

The form published with slice A compared the count of owner-less `codexFactory`
occurrences per changed pre-existing file and demanded **equality**. On this
slice it reported a false positive:

```
!!! BARE NAME EDITED:
  contracts/README.md: 3 -> 4
  contracts/manifest.yaml: 25 -> 27
```

Nothing was edited. The counts rose because the added lines are prose about this
work, and **the change id `adopt-codexfactory-repository-identity` contains the
bare string itself**. The corrected test, in
`specs/030-realize-codexfactory-identity/quickstart.md` § 6:

- a file whose diff **removes no line** cannot have edited anything → PASS by
  construction, whatever the count does;
- a file whose diff removes lines is compared on the **multiset of bare
  occurrences in the removed lines against those in the added lines** — every
  bare occurrence that left must come back.

Under it, this slice reads *"add-only diffs (cannot have edited anything): 4"*
and the four rename slices still pass, since their diffs have removals and their
multisets are preserved. **Recorded rather than quietly swapped**, because slice
A's pull request body quoted the old form's output.

### 15.6 Gates at this head

| check | result |
| --- | --- |
| `openspec validate adopt-codexfactory-repository-identity --strict` | valid |
| `openspec validate --all --strict` | **`100 passed, 1 failed`** — the failure is still exactly `change/disposition-codexfactory-declared-renames` (§ 10) and nothing else |
| `validate-sequenced-after.py . --ledger-diff` | **green**, ledger consistent (**185 rows**), no cycle |
| `doc-health --single-repo` error+critical | **19 findings on the branch, 19 on `origin/main` `131adf11`, and the two sets are IDENTICAL** — measured by diffing both runs; **this slice introduces no doc-health finding**, and `contracts/policies/repository-identity.yaml` appears in none |
| `release-inventory-drift` | **1 `ERROR`**, the pre-existing `docs/contract-versioning-policy.md` (§ 12). Registering a new contract adds no finding: `contracts/manifest.yaml` and `contracts/README.md` are EDITORIAL members and report at `info` |
| `pytest tests/manifest_digests tests/doc-health/test_release_inventory.py tests/hermes_runtime_contracts/test_release_inventory.py tests/credential_contracts/test_manifest_row_digest.py tests/clearing/test_clearing_manifest_rows.py tests/intent-compliance/test_release_boundary.py tests/sequenced_after` | **320 passed** — the manifest digest sweep is what proves the new row's `sha256` was computed and not hand-edited |

### 15.7 `sequenced_after` now points the other way, and is DELIBERATELY not edited

The amendment inverts the file-creation half of
`sequenced_after: [adopt-medxsoft-repository-identity]`: this change authors the
file and the exemplar appends to it. **The declaration is left exactly as
ratified**, because `validate-sequenced-after.py --archive-gate` is a
parent-declaration RETENTION gate and reports a declaration mutation as exit 1 —
the freeze exists so a realization cannot quietly re-point a ratified
dependency. Re-deriving it is the separate governed question task **0.2**
anticipated. Named in § 5 of the amendment record so the next lane finds it at
the packet rather than at the gate.

## 18. Addendum, 2026-09-09: the four GATED slices reconciled to a MOVING `main`, and the arithmetic re-closed there

**Numbered 18, not 16 or 17, and that is deliberate.** Two addenda to this file
are already authored and UNMERGED, each on a different draft: **§ 16 on #802**
(slice B2) and **§ 17 on #801** (slice B1). This one lands on **#806** (slice
B4). The three will meet in this file when the slices land in ceremony order,
and skipping to 18 is what keeps the section numbers from colliding at that
merge — the numbers are not a claim about landing order, and § 16 and § 17 are
NOT missing when you read this on #806's branch.

### 18.1 What this addendum records, and what it does not

It records ONE act: reconciling the four GATED drafts with `origin/main` on
2026-09-09 (runbook step **10.2**, ordered by Brett Heap that day), and
re-closing the sweep arithmetic at the head they were reconciled to. **It rules
nothing.** Every occurrence it assigns is assigned by a rule already published
in this file, cited per assignment, and no verdict here is new.

### 18.2 `main` MOVED FIVE TIMES DURING THE RECONCILIATION, and that is the finding

The reconciliation began against `ca4a1558` and finished against `7681e409`.
In between, `origin/main` advanced through **six** commits in five landings:

| head | what landed |
| --- | --- |
| `86651a58` | #827 (specs/019 FR-016 restated), #828 (pin registration is checked) |
| `9a67d42c` | #826 (`openspec-cli-pin.yaml` header), #824 (`govern-archived-record-edits`) |
| `82c9f059` | **#829 — M-1 step (3) of `relocate-review-authority-floor-mirror`** |
| `7681e409` | #830 (merge-approval envelope, ruling D-10 (a)), #176 (the bot's `intents/rolling`) |

**Each of the four branches was merged to the SAME final head, `7681e409`**, and
every number below is measured there. Slice B1 took **three** merges rather
than one, because two of those landings rewrote the exact lines it edits.

**This is a fact about the corpus, not a complaint.** A repository with an
autonomous merge lane and three active governed lanes does not hold still for a
four-pull-request reconciliation, so *"reconciled"* is only ever a claim about a
NAMED head. Every commit message on the four branches names its head for that
reason, and a slice that sits unmerged long enough will need this done again.

### 18.3 The one conflict class, and how it was resolved — twice

`.github/workflows/review-lane-repin.yml`'s `env:` block conflicted with B1 at
`86651a58` and AGAIN at `82c9f059`, both times because
`relocate-review-authority-floor-mirror` was rewriting the line IMMEDIATELY
BELOW `SOURCE_REPOSITORY:`:

* at **#817/#818** the single `FLOOR_IN_SOURCE:` became the two-entry ordered
  `FLOOR_IN_SOURCE_CANDIDATES:` with a status-classifying fetch loop (M-1 step
  (1), the migration window OPENED);
* at **#829** that list returned to ONE entry at the successor path, with the
  `candidate N of M` witness machinery (M-1 step (3), the window CLOSED).

**The resolution rule was the same both times, and it is the rule this addendum
recommends for the next collision: take the relocating lane's structure
VERBATIM, and re-apply only this change's spelling inside it.** Nothing about
the floor relocation was re-litigated in a rename slice — B1 contributes exactly
`SOURCE_REPOSITORY: codeXfactory/codexFactory` to that block, and the relocated
fetch loop reads the moved repository ONLY through `${SOURCE_REPOSITORY}`, so
the whole loop and its refusal messages inherit the rename with no further edit.
`docs/review-lane-repin-runbook.md` conflicted the same way at `82c9f059` and
was resolved the same way.

### 18.4 Occurrences `main` added while the slices sat, assigned by the published rule

`git grep -o -i 'opensoft/codexFactory'`, `f03fd875` (the branch point) ->
`7681e409`: **nine** new occurrences, in four places. None was left unassigned.

| where | count | class, and the rule that says so | slice |
| --- | ---: | --- | --- |
| `README.md` — `relocate-review-authority-floor-mirror`'s OpenSpec Records entry, citing codexFactory #232 (twice) and #293 (twice) | 4 | **RENAME.** § 5 already ruled this exact shape four times over for the citations B4 respells at `:1001`, `:1002`, `:1113`, `:1115`: *"kept-current index citation; issue NUMBERS carry through a transfer"* | **B4**, respelled |
| `docs/review-lane-repin-runbook.md:354` — #829's rewritten snapshot re-copy, `gh api "repos/opensoft/codexFactory/contents/${FLOOR}?ref=${CORE}"` | 1 | **RENAME.** A live operator command against the moved repository, in a machine-adjacent runbook B1 owns and already respells | **B1**, respelled |
| `tests/review_lane_pin/test_review_lane_caller.py:90` — #830's comment naming where the `path_allowlist` glob authority lives | 1 | **RENAME.** A live pointer at the moved repository, four lines from the same file's `PINNED_REPOSITORY = "codeXfactory/codexFactory"` | **B1**, respelled |
| `openspec/changes/relocate-review-authority-floor-mirror/{proposal.md, review/ratification-2026-09-08.md}` | 3 | **NOT SWEPT** — another lane's in-flight packet, and one of the two is a dated ratification record. § 7's published disposition, unchanged | none, by design |

**#829's net effect on the total was ZERO** and that is worth stating so a
future reader does not conclude nothing needed doing: the same commit deleted
the runbook's old fetch line, so `git grep | wc -l` read 412 before and after
while the occurrence that needed respelling was a different one.

### 18.5 The arithmetic, re-closed at `7681e409`

`git grep -o -i 'opensoft/codexFactory'` on `origin/main@7681e409`:
**413 occurrences across 174 files**.

| slice | respells | files |
| --- | ---: | ---: |
| **B1** (#801) — decision-core pin, workflows, operator tools | **42** | 15 |
| **B2** (#802) — factory-origin identity re-issue, clearing examples | **37** | 15 |
| **B3** (#805) — the eight contract-v3.4 inventoried members | **12** | 9 |
| **B4** (#806) — remaining live documents and `README.md` | **30** | 15 |
| **UNION** | **121** | **54** |

**The four file sets are DISJOINT**, checked rather than asserted: 15 + 15 + 9 +
15 = 54, and no file appears in two slices' respelling sets.

Residual — of `main`'s own 413, what the four slices deliberately leave:

| occurrences | files | disposition |
| ---: | ---: | --- |
| 44 | 34 | `contracts/signed-execution-chain/` — **FROZEN**, digest-pinned chain content; the *"cannot be respelled at all"* set |
| 91 | 38 | `openspec/changes/` — **NOT SWEPT**, other lanes' in-flight packets |
| 59 | 6 | `openspec/changes/adopt-codexfactory-repository-identity/` — **FROZEN**, this packet's own records (§ 11 self-reference) |
| 55 | 17 | `specs/` — **FROZEN**, Speckit feature directories |
| 19 | 13 | `ideation/` — **NOT SWEPT** |
| 17 | 10 | `openspec/changes/archive/` — **FROZEN**, archived packets |
| 3 | 1 | `README.md` — **FROZEN** per line (§ 5): the packet's own dated measurement, and the two completed-mint sentences |
| 2 | 1 | `contracts/policies/repository-identity.yaml` — the `former:` mapping key, **NEVER SWEPT by design**; respelling it would delete the mapping |
| 1 | 1 | `docs/decisions/0002-xfactory-aggregation-repo.md` — **FROZEN**, ADR record |
| 1 | 1 | `docs/dogfood-content-migration-plan.md:49` — **FROZEN** line, B4's per-line verdict |
| **292** | **122** | **TOTAL RESIDUAL** |

**BOTH AXES CLOSE, and the closure is the check.** Occurrences: 121 + 292 = 413,
`main`'s exact total. Files: 54 respelled + 122 residual − 2 MIXED = 174,
`main`'s exact file count. The two mixed files are `README.md` (ten lines
renamed, three frozen) and `docs/dogfood-content-migration-plan.md` (renamed
lines plus one frozen). An arithmetic that closes on both axes is what tells you
no occurrence was silently dropped between the slices.

### 18.6 The twenty-two literals the slices ADD, and why they are not a regression

Three of this packet's own record files carry MORE `opensoft/codexFactory`
literals on the branches than on `main` — **+8** and **+7** in this evidence file
(§ 17 on B1, § 16 on B2) and **+3** in
`review/addendum-2026-09-08-token-namespace.md` (B1), plus **+4** in this
addendum itself — **twenty-two**, counted from the diff rather than
estimated. Every one is a QUOTATION inside a record of the change, which § 11
already classifies as self-reference and freezes. Task 6.5's
zero-residual check is a check over LIVE surfaces; a record that quotes the
former identity in order to say what moved is not a live surface, and a sweep
that respelled these would make each record claim it is about the identity it
moves TO.

### 18.7 Gates at this reconciliation

Every branch was measured at its own head against `origin/main@7681e409`
measured in a THROWAWAY WORKTREE at that commit — never against a remembered
baseline.

| check | B1 (#801) | B2 (#802) | B3 (#805) | B4 (#806) |
| --- | --- | --- | --- | --- |
| `pytest tests/review_lane_pin tests/clearing tests/credential_contracts -q` | 626 passed, 2 skipped, 48 subtests | 624 / 2 / 48 | 624 / 2 / 48 | 624 / 2 / 48 |
| `openspec validate --all --strict` | 101 passed / 3 failed | same | same | same |
| `validate-sequenced-after.py . --ledger-diff` | consistent, 189 rows | same | same | same |
| doc-health `--single-repo .` critical+error | **IDENTICAL to `main`** | **IDENTICAL** | **+7, all `release-inventory-drift`** | **IDENTICAL** |
| freeze check (`contracts/signed-execution-chain/`, `openspec/changes/archive/`, `specs/`, `docs/decisions/`, `ideation/`) | EMPTY | EMPTY | EMPTY | EMPTY |

**`openspec validate --all --strict` now fails THREE, not one, and none of the
three is ours.** § 15.6 recorded `100 passed, 1 failed` with
`change/disposition-codexfactory-declared-renames` (§ 10) as the only failure.
`main` has since gained two more, both measured at `7681e409` in the throwaway
worktree: `change/pin-openspec-cli-dependency-closure` — its ADDED requirement
*"A pinned artifact that resolves dependencies at install time carries a
vendored lockfile…"* does not carry SHALL or MUST **on its first body line**,
which is the parser's rule — and `spec/repo-boundary-governance`. **Recorded
here rather than fixed here**: they belong to #813 and #828's lanes, and a
rename slice must not edit another packet's requirement text to make a shared
gate read green. The number to compare against on these four drafts is **3**,
and any FOURTH failure is a real defect in the slice reporting it.

**B3's seven ERRORs are the predicted transient, and the delta was measured by
NAME, not by count**: `contracts/hermes-runtime/README.md`,
`contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml`, the three
`fixtures/regression/` negatives, `docs/terminology-and-repo-topology.md` and
`docs/xfactory-domain-factory-model.md`. With the pre-existing
`docs/contract-versioning-policy.md` the family reports EIGHT — task **7.5**'s
prediction — and the bundle cut (ceremony row 4) discharges all eight. No other
family moves on any of the four branches, and nothing that stands on `main`
disappears.

### 18.8 What this addendum does NOT discharge

* **Task 6.5 stays open.** It is a whole-corpus zero-residual check to be run
  after the transfer and after all four slices land, and it is strictly last.
  This addendum re-derives the arithmetic it will need; it does not perform it.
* **Task 7.5's zero-findings row stays unticked** — only the cut can tick it.
* **The `identity_namespace` question at
  `contracts/review-lane-repin-binding.template.yaml:103` stays open**, awaiting
  Brett Heap's word on the record in
  `review/addendum-2026-09-08-token-namespace.md`. Nothing in this
  reconciliation touched that line.
* **One staleness in another lane's prose is REPORTED, NOT EDITED.**
  `README.md`'s `relocate-review-authority-floor-mirror` Records entry still
  describes the workflow constant as `FLOOR_IN_SOURCE` at `:138`; #818 renamed
  it to `FLOOR_IN_SOURCE_CANDIDATES` and #829 moved its value again. It carries
  no identity occurrence, so it is outside every slice's class, and a rename
  slice correcting another lane's ratified narrative would be exactly the
  boundary violation this packet's design forbids. Raised on codexFactory #279
  for that lane.
