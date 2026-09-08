# Tasks: split-openxwallet-repo

Dependency-ordered, in `design.md`'s Migration Plan order. **Only §1 is this
change's own work**; §2–§12 are the named successors P5a.1, P2, P2b, P2.5, P5a.2,
P3, P3b, P4, P5b, P4b and P6, listed here so the wave's build order is one
document rather than eleven, and so nothing the proposal names loses its home.
Each successor carries its OWN `code_surface` and archives on merged, green
realization evidence per `release-realization` — do not tick a successor's boxes
from this change. §13 is the close, and §14 records the two spec deltas the
archive tooling cannot apply.

**Repository tags.** Untagged = openxFactory. `[openXwallet]` =
`opensoft/openXwallet`, the repository this wave creates, and its own OpenSpec
instance. `[LedgerxFactory]`, `[OpsxFactory]`, `[codexFactory]` = those
repositories. `[xFactory]` = the aggregation repo. `[OPERATOR]` = only Brett can
perform it (a repository creation, a ruleset, a tag, a ratification).
`[GOVERNANCE]` = it needs a ruling or an OpenSpec change before the work is
legal.

**Two standing sequencing guards, restated as tasks** (§7.1 and §7.26) rather
than as prose, because both are unenforceable by any checker: the register row's
`expires_at` clock, and the unenforceable manifest freeze across P2.5 → P3.

**The byte-identity floor is proven ONCE, against the NAMED CARVE COMMIT, at
`wallet-v1.0`** (§3.23–§3.24). `wallet-v1.1` (§4) is one auditable additive-minor
diff on top and touches none of the eight digested artifacts; openxFactory's pin
at P3 records `wallet-v1.1`.

---

## 1. This change: doctrine, deltas, bookkeeping

- [x] 1.1 `proposal.md` — R1–R8 carried as LOCKED constraints; the
      RATIFIES / AUTHORIZES split (`a physical act needs its own realization
      evidence`); the byte-identity floor with its ONE named prose carve-out; the
      alias-preserved `wallet-validation` token; ten non-negotiable sequencing
      items; the realization-evidence table as a gate; Q1–Q5 with recommended
      answers and destinations; the successors named. The header read
      `Status: draft` as authored; 1.13 superseded that, and it now carries
      `Status: ratified` with its `Ratified:` provenance line and the
      `## Ratification record, 2026-08-26`. (Corrected in Speckit feature
      `016-openxwallet-split-bookkeeping`.)
- [x] 1.2 **Seven spec deltas, 30 requirement blocks.** ADDED 14 —
      `domain-descendant-boundary` (5: descendant repository, pin-by-commit
      twice, profile-never-fork, ratified placement, lazy consumer-gated
      creation) and `neutral-product-pin` (9: commit-and-digest never tag,
      refusal-names-its-remedy, consumer's-pin-authoritative, required check runs
      the pinned tool at the pinned digest, no-scan-target refuses, pin-plus-register
      is human-only, the one vendored openxFactory contract, vendored copy
      digest-verified before read, pinned validator IS the conformance validator
      from the major forward). REMOVED 11 — `openxwallet` (8) and
      `openxwallet-agent-profile` (3), all titles verbatim. MODIFIED 5 —
      `review-authority-intake` (3), `shared-contract-ownership` (1),
      `trust-anchor` (1).
- [x] 1.3 **The eleven REMOVED titles verified byte-identical** against both
      promoted specs AND the archived `2026-08-08-add-openxwallet` delta, because
      `scripts/doc_health/promotion_fidelity.py` keys on (capability, normalized
      title) and one character of drift leaves the 2026-08-08 `ADDED` writer
      authoritative and the removal invisible.
- [x] 1.4 `design.md` — D1–D14 with their rejected alternatives, seven risks, the
      ordered migration plan with a rollback per step, and Q1–Q5 restated with
      what design decided (Q4, Q5) versus what travels (Q1, Q2, Q3).
- [x] 1.5 `clarifications.md` — the eight council-identified constraints that
      constrain design (remediation strings, the `relocating:` emitter and shape,
      pin verifiers in both directions, the sweep-exclusion mechanism, the nested
      fetch plus PASS/SKIP pinning, LedgerxFactory's declared pin shape, the
      invocation test, the CONSUMED-member row).
- [x] 1.6 The five review records RETAINED in the packet, not folded into the
      proposal: `alignment-qa-lead.md`, `alignment-stack-architect.md`,
      `council-systems-architect.md`, `council-adversary-engineer.md`,
      `council-product-advocate.md` — 30 alignment findings (all applied bar each
      reviewer's missing-`specs/` finding, deferred to the specs phase and
      discharged by §1.2) and 14 council verdicts, ALL VALID and none DISMISSED,
      two raised jointly, with the 8 NOTED-class constraints in
      `clarifications.md`. (PR #391, 2026-08-26)
- [x] 1.7 Reconcile `proposal.md` with the three design findings it contradicted,
      surgically and without renumbering R1–R8 or touching the LOCKED block:
      **(a)** the register-read evidence becomes the POSITIVE conjunction the
      pinned reader actually produces (the `repo scan:` note plus the absence of
      `no intake register at this tree` and of any `register-*` code) with the
      durable NOTE landing upstream at `wallet-v1.1` — a NOTE, never a warning,
      because LedgerxFactory runs `--strict`; **(b)** the nested-repository sweep
      exclusion is UPSTREAM code cut as `wallet-v1.1` (successor P2b) and
      **openxFactory's pin at P3 is `wallet-v1.1`**, with `wallet-v1.0` left as
      the byte-identical pure move the floor is proven against; **(c)** P5a splits
      into P5a.1 (finder, before P2) and P5a.2 (`stack.yaml` bump, after P2.5's
      cut, before P3).
- [x] 1.8 `OPENSPEC_TELEMETRY=0 openspec validate split-openxwallet-repo
      --strict` green, and `--all --strict` green. (PR #391, 2026-08-26)
- [x] 1.9 List the change in `README.md`'s `## OpenSpec Records` →
      `Active changes:` block, at the top, in the existing entries' shape.
      (PR #391, 2026-08-26)
- [x] 1.10 `python3 scripts/doc-health.py --single-repo .` shows NO new finding
      attributable to this change directory or the README entry, measured against
      the same command's report on the tree before the packet's completion.
      **MEASURED, and the numbers are recorded rather than summarized as
      "green".** Pre-packet `5ef6d8d2^1` = `64486a51`: 5 critical, 6 error, 41
      warning, 4 info. Post-packet `5ef6d8d2`: 5 critical, 7 error, 41 warning,
      4 info. The differential is **exactly one finding**, and it is NOT in
      1.10's scope: `family=location-conformance`,
      `path=ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md`,
      `rule="staged material already cites proposal split-openxwallet-repo"`,
      `class="contested"`. Zero findings attributable to
      `openspec/changes/split-openxwallet-repo/` or to 1.9's README entry, which
      is what this task asserts. The one finding is the standard staged-topic-exit
      signal — `scripts/doc_health/families.py` `fam_location_conformance` fires
      when a `staged` fragment cites a change id that now exists on disk — so it
      is triggered by the packet's EXISTENCE, not by a defect in it. It is
      deliberately NOT remedied here: the remedy is a lifecycle act on a staged
      topic (moving material into `supporting-docs/`) that §1 does not authorize,
      the topic is still the reference for §2–§12, and a `contested` finding is
      resolved only by a cited change or a recorded disposition — never by a
      silent edit. Left for the wave's archive step or its own change.
      (Speckit feature `016-openxwallet-split-bookkeeping`)
- [x] 1.11 **Amendment 2 to `docs/openxdox-naming.md`** — THIS CHANGE'S OWN DIFF,
      not a successor, because R1 contradicts a `ratified` record. TWO edits, both
      quoted verbatim in the proposal so the diff is checkable. **(a)** The new
      `## Amendment 2 — openXwallet leaves the exception list (2026-08-26)`
      section appended after Amendment 1 in Amendment 1's shape (amended, never
      rewritten; the wire label stays lowercase; `openXwallet-Install` registered
      as a NAME with no repository created, per Q4). **(b)** The inline pointer at
      `:23-25`, whose sentence names TWO exceptions and MUST stay GRAMMATICAL when
      one leaves: "(the lowercase `openxFactory` spelling is the family exception,
      not the rule; `openXwallet` left this list in Amendment 2)" — singular verb,
      singular noun. A mechanical substitution there leaves a `ratified` record
      ungrammatical.
      **DONE** in `docs/openxdox-naming.md`: (a) Amendment 2 appended as the
      file's new final section (`:111-127`), body byte-equal to the proposal's
      quoted block modulo wrapping; (b) the § Decision bullet rewritten at
      `:23-25` — singular `spelling`/`is`/`exception`, so the record body above
      Amendment 2 carries zero `openxWallet` occurrences (the two inside
      Amendment 2 are the ratified text naming the retired spelling as history).
      The lifecycle header is byte-identical and still carries exactly ONE
      ratification citation line, per Amendment 1's precedent and
      `docs/document-lifecycle.md` § Status Claim Rules. The whole diff is two
      hunks: one append, one bullet — amended, never rewritten.
      **Left OPEN for the human merge gate — not merged.**
      (commit `b08184e`, PR #396, Speckit feature
      `016-openxwallet-split-bookkeeping`, 2026-08-26)
- [x] 1.12 **[xFactory]** Amend `CLAUDE.md` § "Working rules" item 1 to the
      replacement text quoted verbatim in the proposal — neutral contracts live in
      openxFactory **or in a neutral `open*` product repository openxFactory pins
      by commit and digest**. THIS CHANGE'S OWN DIFF per the RATIFIES list. Until
      P4 lands, the rule as written is the one in force and this change
      contradicts it; that is stated in the proposal rather than discovered later.
      **DONE** in xFactory `CLAUDE.md` rule 1 (`:61-64`), replaced with the
      proposal's verbatim four-line text; one file changed, four insertions and
      two deletions, `## Working rules` heading and rules 2 onward byte-identical,
      no `.gitmodules`/gitlink/submodule pin touched. Authored in the dedicated
      worktree `xFactory-worktrees/openxwallet-working-rule` and committed with an
      explicit `-- CLAUDE.md` pathspec per that repo's own working rule #2.
      **Left OPEN for the human merge gate — not merged.**
      (xFactory commit `b66db51`, PR opensoft/xFactory#157, 2026-08-26)
- [x] 1.13 **[OPERATOR] [GOVERNANCE]** Ratify or return the proposal. Nothing in
      §2 onward is authorized work until this is discharged; record the
      ratification in the proposal header and set `Ratified by:`.
      **RATIFIED AS PROPOSED 2026-08-26** by Brett Heap in session, after both
      required checks reported green — `Status: ratified`, the `Ratified:`
      provenance line and `## Ratification record, 2026-08-26` are in the
      proposal header; R1–R8 stand and Q1–Q5 are carried at design's
      dispositions; the build path is **Speckit features per group**, NOT
      `/opsx:apply`. (PR #391, 2026-08-26)

## 2. P5a.1 — LedgerxFactory forward-compatible finder (lands FIRST, before P2)

*Forward-compatible by construction: candidate three is today's behaviour.*

- [x] 2.1 **[LedgerxFactory]** `find_openxfactory()`
      (`tests/validate_wallet_estate.py:47-63`) resolves in THREE ordered
      candidates: `openxFactory/openXwallet/scripts/validate-openxwallet.py`,
      then `openXwallet/scripts/validate-openxwallet.py`, then
      `openxFactory/scripts/validate-openxwallet.py`.
      **Evidence:** REALIZED — [LedgerxFactory #25](https://github.com/opensoft/LedgerxFactory/pull/25)
      merged `e2cedb683019ae8bfee5a520f60cdbbc85ef90fd`. The three candidates land
      in exactly this order, tried at every level of the existing five-parent
      upward walk. Speckit feature `017-openxwallet-finder`.
- [x] 2.2 **[LedgerxFactory]** The NESTED candidate leads, and the reason is
      recorded in the code: the finder walks UP and would otherwise resolve the
      AGGREGATION's root gitlink — a different commit, which
      `contracts/openxwallet-pin.yaml` does not govern.
      **Evidence:** REALIZED — [LedgerxFactory #25](https://github.com/opensoft/LedgerxFactory/pull/25)
      merged `e2cedb683019ae8bfee5a520f60cdbbc85ef90fd`. The reason is in the code
      rather than only in the packet, and level order is OUTER with candidate order
      INNER, because candidates 1 and 2 both resolve at the aggregation level to
      different commits and only the tie-break makes the pinned one win.
- [x] 2.3 **[LedgerxFactory]** Candidate three is retained and its removal is
      declared as P5b's work, so pre-P3 checkouts keep resolving; `VALIDATOR =
      find_openxfactory()` at `:66` is unchanged in shape and still returns
      `None` (a loud failure, never a skip).
      **Evidence:** REALIZED — [LedgerxFactory #25](https://github.com/opensoft/LedgerxFactory/pull/25)
      merged `e2cedb683019ae8bfee5a520f60cdbbc85ef90fd`. Candidate three is retained
      with its removal declared in the code as P5b's work; `VALIDATOR =
      find_openxfactory()` is byte-identical, and the ninth probe reaches `main()`'s
      import-time guard and observes it print "a failure, not a skip" and exit 1.
- [x] 2.4 **[LedgerxFactory]** Evidence: a green estate run on a tree where ONLY
      candidate three exists — the run id, plus `run_validator()`'s `repo scan:`
      count still ≥ 5.
      **Evidence:** REALIZED — [LedgerxFactory #25](https://github.com/opensoft/LedgerxFactory/pull/25)
      merged `e2cedb683019ae8bfee5a520f60cdbbc85ef90fd`. `WALLET ESTATE: PASS`
      resolving `…/openxFactory/scripts/validate-openxwallet.py` — candidate three,
      i.e. exactly the tree this task names — with `repo scan: 5` satisfying its
      `>= 5`. **There is no CI run id to give**: LedgerxFactory runs no gate other
      than the Copilot reviewer (run 33018077104), so the estate run is the local
      `validate_wallet_estate.py` output quoted in the pull request, and this clause's
      "the run id" is recorded as unavailable rather than substituted.
- [x] 2.5 **[LedgerxFactory]** Rollback recorded before the step: revert;
      candidate three alone is today's behaviour.
      **Evidence:** RECORDED BEFORE THE STEP, in two places — `design.md:532` in the
      migration plan ("revert; candidate three is today's behaviour") and again as
      the pull request's own `## Rollback` section, which cites this task as its
      authority. Taken and not reverted:
      [LedgerxFactory #25](https://github.com/opensoft/LedgerxFactory/pull/25) merged
      `e2cedb683019ae8bfee5a520f60cdbbc85ef90fd`.

## 3. P2 — carve, scaffold, prove, tag `wallet-v1.0`

*From the NAMED CARVE COMMIT. The carve COPIES and deletes nothing; openxFactory
is untouched by this whole section.*

- [x] 3.1 **[OPERATOR]** The case-variant repository-name check, BEFORE the
      carve and recorded: GitHub names are case-insensitive-unique, so
      `openxwallet`, `OpenXWallet` or any other casing anywhere in the org — or in
      a fork — collides with `openXwallet`. Discovering it after a carve costs the
      carve.
- [x] 3.2 **[openXwallet]** `docs/openxwallet-cutover-runbook.md` authored BEFORE
      the carve it describes, with a rollback written before each phase is taken,
      and carrying the two-part byte-identity proof table and the NAMED CARVE
      COMMIT.
- [x] 3.3 Name the carve commit — one 40-hex openxFactory sha, recorded in the
      cutover runbook and (at P3) in `contracts/openxwallet-pin.yaml`'s
      `carve_commit:`. **Never "HEAD"**, which is no referent across a multi-PR
      wave.
- [x] 3.4 **[OPERATOR]** Create `opensoft/openXwallet`, private.
- [x] 3.5 **[openXwallet]** `git filter-repo` with one `--path` per set, exact
      paths, NO globs and NO `--path-rename`, over the twelve path sets:
      `contracts/openxwallet/`, `contracts/openxwallet-agent-profile/`,
      `scripts/validate-openxwallet.py`, `scripts/wallet-yaml-syntax-gate.py`,
      `tests/wallet_yaml_syntax_gate/`, `.github/workflows/wallet-validation.yml`,
      `openspec/specs/openxwallet/`, `openspec/specs/openxwallet-agent-profile/`,
      `openspec/changes/archive/2026-08-08-add-openxwallet/`,
      `specs/006-openxwallet-contracts/`, `specs/010-wallet-validator-ci/`,
      `specs/012-wallet-issuer-anchor/`. Full path history.
- [x] 3.6 **[openXwallet]** Completeness check: `git ls-tree -r --name-only
      <carve_commit> --` over the twelve paths, sorted, EQUALS the same listing at
      `wallet-v1.0` filtered to those prefixes. Evidence is the diff of the two
      sorted listings, empty.
- [x] 3.7 **[openXwallet]** The two counts a shorthand loses, asserted
      explicitly: **7** files under `specs/006-openxwallet-contracts/` (its
      `evidence/` included) and **36** under
      `contracts/openxwallet/examples/negative/`.
- [x] 3.8 **[openXwallet]** Examples-prefix preservation, an acceptance line and
      not a hope: both `examples/` directories exist at IDENTICAL relative paths
      in the carved tree, because `repo_scan`'s corpus exclusion keys on
      `"examples" in path.parts` AND an `openxwallet*` part — a rename
      re-adjudicates the 36 intended-invalid negatives as LIVE records inside a
      REQUIRED check.
- [x] 3.9 **[openXwallet]** Governed-repo scaffold: `README.md` (what the
      repository is, the two contract families, the doc index, the pin
      relationship in both directions) and `CLAUDE.md` / `AGENTS.md` pointing at
      the user-global OpenSpec/Speckit protocol, in the house form.
- [x] 3.10 **[openXwallet]** `.github/CODEOWNERS` — the validator, the syntax
      gate, `contracts/`, `contract_pin.yaml` and the workflows.
- [x] 3.11 **[openXwallet]** `contracts/manifest.yaml` at `wallet-v1.0`: the
      EIGHT owned rows carried with the publisher's nine fields (`id / path /
      source_path / type / schema_version / sha256 / compatibility /
      adapter_owner / consumption_rule`) and their sha256 values UNCHANGED from
      the carve commit; the content-addressed-by-commit note for the validator,
      the gate, both `examples/` trees and both family READMEs.
- [x] 3.12 **[openXwallet]** The CONSUMED-member row for the vendored envelope
      schema, in the same manifest: publisher's nine fields with `compatibility:
      canonical_openxfactory_contract`, `adapter_owner: openxFactory` and a
      `sha256` EQUAL to the pinned openxFactory row's, plus three declared
      fields — `member_class: consumed`, `release_surface: false`,
      `pinned_openxfactory_bundle: contract-v<pinned>`. It satisfies
      `shared-contract-ownership:142`'s all-markers-together test without claiming
      ownership of an openxFactory contract.
- [x] 3.13 **[openXwallet]** Release tooling selects `member_class: owned` ONLY
      for `wallet-vN.M.digests.yaml` — exclusion by DECLARED FIELD, never by a
      `contracts/schemas/` path heuristic, which breaks the day openXwallet
      publishes a schema of its own there.
- [x] 3.14 **[openXwallet]** `carved_from: {repository, commit}` in
      `contracts/manifest.yaml` — the machine-read one of the three provenance
      records (the other two are `carve_commit:` in openxFactory's pin file and
      the runbook's procedure). No bare `CARVE_COMMIT` file.
- [x] 3.15 **[openXwallet]** `contracts/CHANGELOG.md` seeded with the
      `wallet-v1.0` entry: a byte-identical carve from openxFactory
      `<carve_commit>`, the twelve path sets, the two prose edits, and no content
      change.
- [x] 3.16 **[openXwallet]** The vendored copy at EXACTLY
      `contracts/schemas/hermes-job-envelope.schema.yaml` — the identical
      repository-relative path — added by the SCAFFOLD commit and not by the
      carve, so `ENVELOPE_SCHEMA_PATH` (`:218`) and its `.relative_to(ROOT)`
      print need no edit and R6's empty diff survives.
- [x] 3.17 **[openXwallet]** `contract_pin.yaml` on openAvatar's model, with a
      NAMED `verify_pin` that FAILS CLOSED pre-sync (a recomputed digest can never
      equal an empty recorded digest → drift → fail before any test), and the
      pinned openxFactory bundle identified.
- [x] 3.18 **[openXwallet]** `docs/pin-resync-runbook.md` on openAvatar's shape:
      Preconditions, Checklist, re-verify the pin offline, re-run the offline gate
      suite. It exists from day one because an `openxwallet` core delta costs a
      wallet release, an openxFactory pin bump and a LedgerxFactory re-pin.
- [x] 3.19 **[openXwallet]** `.github/workflows/wallet-validation.yml` — job id
      `wallet-validation`, deliberately the same token name as openxFactory's
      (distinct repositories are distinct namespaces), with the vendored-schema
      `verify_pin` step running BEFORE the validator, because `main()` checks only
      `ENVELOPE_SCHEMA_PATH.is_file()` — presence, not identity — while rule (g)
      reads the approval-scope vocabulary out of that file.
- [x] 3.20 **[openXwallet]** `.github/workflows/pytest-suite.yml` over the carved
      `tests/wallet_yaml_syntax_gate/`.
- [x] 3.21 **[openXwallet]** Prose edit one of two: the `openxFactory SHALL` →
      `openXwallet SHALL` subject at `openspec/specs/openxwallet/spec.md:8` and
      `openspec/specs/openxwallet-agent-profile/spec.md:8`. Outside the floor,
      which covers `contracts/` BYTES and does not reach spec prose.
- [x] 3.22 **[openXwallet]** Prose edit two of two: the `## Purpose` placeholder
      at `:4` of each promoted spec ("TBD - created by archiving change
      add-openxwallet…"), written in the move because a moved spec whose Purpose
      names another repository's archiving change is not a pure move either.
- [x] 3.23 **[openXwallet]** Byte-identity proof, part one: for each of the eight
      digested artifacts, `sha256sum` at `wallet-v1.0` EQUALS the `sha256:`
      recorded at the NAMED CARVE COMMIT. Evidence is the eight-row table in the
      cutover runbook and in P2's evidence row.
- [x] 3.24 **[openXwallet]** Byte-identity proof, part two: `git diff` EMPTY over
      `contracts/openxwallet/`, `contracts/openxwallet-agent-profile/`,
      `scripts/validate-openxwallet.py`, `scripts/wallet-yaml-syntax-gate.py`,
      `tests/wallet_yaml_syntax_gate/`, the three Speckit sets and the archive
      packet, against the carve commit — AND diff-limited-to-two-lines over each
      promoted spec, asserted line by line at `:4` and `:8`, which is the declared
      scope of the one carve-out rather than a described one.
- [x] 3.25 **[OPERATOR]** Create openXwallet's branch-protection ruleset in
      **EVALUATE** mode. Record in the runbook that **day-one REQUIRED is
      impossible** — GitHub cannot require a check that has never reported — as
      unachievable rather than promised.
- [x] 3.26 **[OPERATOR]** Land one trivial pull request so `wallet-validation`
      reports once and becomes selectable.
- [x] 3.27 **[OPERATOR]** Promote the ruleset to **ACTIVE**. Evidence: `GET
      repos/opensoft/openXwallet/rules/branches/main` showing
      `required_status_checks → [wallet-validation]`.
- [x] 3.28 **[OPERATOR]** Tag `wallet-v1.0` — ONLY after §3.23–§3.24 are green.
- [x] 3.29 **[openXwallet]** Evidence rows: first green `wallet-validation` plus
      the §3.6 carve-completeness check; first green `pytest-suite` plus the
      byte-identity proof against the named carve commit.
- [x] 3.30 **[openXwallet]** Evidence row (V8): the `wallet-validation` log line
      showing the vendored envelope schema digest-verified against
      `contract_pin.yaml` BEFORE the validator ran, PLUS a red run with a
      deliberately mutated copy — a verifier that has never refused is not known
      to refuse.
- [x] 3.31 Rollback recorded before the step: nothing pins openXwallet yet —
      delete the repository or leave it unpinned; openxFactory is untouched.

### P2 realization evidence — recorded 2026-08-26

Realized by openxFactory Speckit feature **`017-openxwallet-carve`**.

| | |
| --- | --- |
| Repository | **https://github.com/opensoft/openXwallet** (PRIVATE) |
| NAMED CARVE COMMIT | `30565e48ffe3d8a9773e10af33425701845e10f6` |
| `main` head at the tag | `936ceb2066705d82fa60b333bea3babe6297a1b7` |
| Tag | **`wallet-v1.0`** — annotated, object `de74c8ccf10dee4f36bd69cd7162f04cea569167` |
| Ruleset | **21607344** — created `evaluate`, promoted **`active`**; `required_status_checks → [wallet-validation, pytest-suite]` on `~DEFAULT_BRANCH` |
| Bootstrap PR | openXwallet **#1**, merged `936ceb20` |
| Green `wallet-validation` | run **33024308629** |
| Green `pytest-suite` | run **33024308567** |

**§3.1** every case variant of `openxwallet` absent in `opensoft` and absent from
an org-scoped and an unscoped repository search, checked and recorded at create
time. **§3.5–3.6** `git filter-repo`, one `--path` per set, twelve sets, no globs
and no renames; **the completeness diff of the two sorted listings is EMPTY at 100
files**, and the carved history is 26 commits (17 of them touching
`scripts/validate-openxwallet.py`). **§3.23–3.24** part one **8/8** three-way
(carved bytes == openXwallet manifest == openxFactory manifest at the carve
commit); part two EMPTY on every floored path, re-established by git blob+mode
identity at **100/100 at the carve layer** and **97/100 after the scaffold**, the
three exceptions being the two promoted specs and `wallet-validation.yml`. **§3.30**
the verifier was observed REFUSING a mutated vendored copy (exit 1, both
remediation strings), and the CI log shows the digest verified **253 ms before the
validator started**.

**Three facts diverged from this group's own text, and each was resolved in the
open rather than absorbed** (full record:
`specs/017-openxwallet-carve/clarify-questions.md`):

1. **§3.7's "36 under `contracts/openxwallet/examples/negative/`"** — that
   directory holds **32**; the other **4** are in
   `contracts/openxwallet-agent-profile/examples/negative/`. 32 + 4 = 36. Asserted
   as 32 / 4 / 36 because asserting 36 in the core family alone would FAIL against
   a correct carve. The validator independently confirms 36 negatives across 13/13
   requirements. This is §3.7's own failure mode, applied to §3.7's text.
2. **§3.12's "sha256 EQUAL to the pinned openxFactory row's"** — openxFactory's
   row for `contracts/schemas/hermes-job-envelope.schema.yaml` carries **no
   `sha256` at all** (`copied_from_source_commit` from `Omnigent-Install`,
   content-addressed by commit). The digest is COMPUTED over the pinned bytes,
   which is the value the text intends; the absence upstream is noted on the row.
3. **§3.27's `required_status_checks → [wallet-validation]`** — ruleset 21538893,
   the shape D8 says to mirror, requires **both** tokens as of 2026-08-26 17:39.
   Both are required, which satisfies the named minimum and matches the precedent.

**One ratified path is deliberately NOT in the byte-identity floor**, per §3.24's
own enumeration: `.github/workflows/wallet-validation.yml`. §3.19 positively
requires the verify step to run *before the validator*, which two independent
workflows cannot order, so the step is prepended inside the `wallet-validation`
job and that one-hunk edit is declared in the proof record.

**openxFactory gained exactly two paths from this feature** —
`specs/017-openxwallet-carve/` and these ticks — and lost nothing. The carve
COPIES; P3's deletions are P3's own commit.

**Still open for P2b** (`wallet-v1.1`, before P3): the nested-repository prune in
`repo_scan`, and the register-read `f.note` D3's positive proof rests on.

## 4. P2b — `wallet-v1.1`, the tag openxFactory actually pins

*Two additive-minor changes, ONE auditable diff on top of the byte-identical
release. It lands BEFORE P3 because the sweep hazard sits inside a REQUIRED
check.*

- [x] 4.1 **[openXwallet]** `repo_scan` prunes any file whose path descends from a
      directory OTHER than the scan root that carries a `.git` entry, **file or
      directory** — a submodule's `.git` is a FILE, which is all today's
      `SKIP_DIR_NAMES` catches. (Feature `013-nested-repo-prune-register-note`,
      openXwallet PR opensoft/openXwallet#2, merged 2026-08-27 at
      `63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`, tag `wallet-v1.1`. Proven
      end-to-end on openxFactory's own tree: NOTE `nested repositories pruned
      (not adjudicated): installs/omnigent-install`, 87 files dropped from the
      sweep, finding set unmoved, exit 0.)
- [x] 4.2 **[openXwallet]** The prune is written as a general nested-repository
      rule, NOT by adding `openXwallet` to `SKIP_DIR_NAMES`: hard-coding one
      consumer's directory name into the product's validator is the exact coupling
      the split removes, and it misses every other nested repository. It also
      closes the same pre-existing hole for `installs/omnigent-install`, which the
      sweep walks into today. (Same PR/tag as 4.1. The general rule closes the
      hole directly: end-to-end proof on openxFactory's own tree shows NOTE
      `nested repositories pruned (not adjudicated): installs/omnigent-install`,
      with no `openXwallet`-named hard-coding involved.)
- [x] 4.3 **[openXwallet]** `main()`'s argparse is UNCHANGED — no `--exclude`
      flag. An exclusion the caller supplies is one the caller can omit (the
      vacuous-pass class), and both R6's zero-refactor proof and the pinned
      invocation test key on that signature. (Same PR/tag as 4.1: zero
      finding-code / message / `--strict` / argparse changes; PR checks
      `wallet-validation` and `pytest-suite` both pass.)
- [x] 4.4 **[openXwallet]** A test proving a YAML file inside a nested repository
      is no longer swept, and that a file at the same relative path OUTSIDE any
      nested repository still is. (`tests/nested_repo_prune/test_prune_and_register_note.py`:
      `test_nested_repo_with_a_dot_git_FILE_is_not_adjudicated`,
      `test_nested_repo_with_a_dot_git_DIRECTORY_is_not_adjudicated`, and the
      control `test_the_control_same_record_outside_any_nested_repo_IS_adjudicated`,
      plus `test_the_scan_root_is_never_pruned_by_its_own_dot_git`. Verified
      against openXwallet `main` at `63f5a1ad`.)
- [x] 4.5 **[openXwallet]** The register-read `f.note` naming the resolved
      register path when the register IS read — an `f.note`, **never a warning**,
      because `:2107` reds a `--strict` run on warnings and LedgerxFactory runs
      `--strict`. (Same PR/tag as 4.1: `check_register` emits the happy-path NOTE
      `intake register read: <path> (N row(s))`. Proven end-to-end on
      openxFactory's own tree: NOTE `intake register read:
      governance/review-authority/register.yaml (1 row(s))`.)
- [x] 4.6 **[openXwallet]** The corpus exclusion at `:2050-2053` still keys on
      path PARTS, so the 36 negatives and 17 positives stay excluded inside a
      submodule; assert it, because the real hazard is the non-`examples/` YAML the
      carve brought along (`specs/006-openxwallet-contracts/evidence/`,
      `tests/wallet_yaml_syntax_gate/`, openXwallet's own OpenSpec instance) plus
      the canonical custody registry being re-indexed as a live record.
      (`tests/nested_repo_prune/test_prune_and_register_note.py`:
      `test_the_packaged_corpus_exclusion_still_keys_on_path_parts`,
      `test_the_repository_itself_still_reports_its_own_corpus`,
      `test_this_repository_adjudicates_with_no_error_and_no_warning`, and
      `test_the_previous_version_adjudicates_the_corpus_identically`, which
      recovers the wallet-v1.0 validator and compares finding sets — 17
      positives / 36 negatives unchanged. Verified against openXwallet `main`
      at `63f5a1ad`.)
- [x] 4.7 **[openXwallet]** `contracts/CHANGELOG.md` entry: additive minor, both
      changes named, none of the eight digested artifacts touched — so the eight
      sha256s at `wallet-v1.1` still equal the carve commit's rows.
      (`contracts/CHANGELOG.md:22` `## wallet-v1.1 — 2026-08-26 (additive minor;
      validator behaviour only)`, stating the eight digests still equal the
      named carve commit's rows. Verified against openXwallet `main` at
      `63f5a1ad`.)
- [x] 4.8 **[OPERATOR]** Tag `wallet-v1.1`, with its own
      `wallet-v1.1.digests.yaml` over `member_class: owned` members only. (Tag
      `wallet-v1.1`, annotated `021cdeef`, targets `63f5a1ad`, pushed
      2026-08-27; 8/8 contract digests unchanged, `contract_bundle_version:
      wallet-v1.1`.)
- [x] 4.9 **[LedgerxFactory]** Evidence: a GREEN estate run on the v1.1 reader.
      The prune changes consumer behaviour, so this is a correctness check, not a
      formality — Ledgerx wallet records live at `tenants/ledgerxcorp/wallets/*`
      and not in a submodule, so `run_validator()`'s ≥5 assertion must be
      unaffected, and the `--strict` run must stay green through §4.5's NOTE.
      (**GREEN, and each of the three assertions checked separately** — LedgerxFactory PR opensoft/LedgerxFactory#30 at `1a8ec624`, feature `019-openxwallet-consumer-repoints`, evidence
      `specs/019-openxwallet-consumer-repoints/evidence/estate-run.md`. Run on a
      purpose-made aggregation clone with BOTH gitlinks initialized, so
      candidate 1 won against a live rival rather than by default: resolved
      `openxFactory/openXwallet/scripts/validate-openxwallet.py`; `repo scan: 5
      openxWallet artifact(s) validated, 602 document(s) skipped as another
      kind` — the ≥5 assertion HOLDS, so the nested-repository prune does not
      reach records outside a submodule; `0 error(s), 0 warning(s)` under
      `--strict`, with §4.5's register read emitted as `note  no intake register
      at this tree` and NOT as a warning — the whole reason §4.5 insisted on an
      `f.note`, since this consumer runs `--strict`; exit 0. **A finding this
      run surfaced:** the shared workspace could NOT have produced this evidence
      — both gitlinks uninitialized, and its `openxFactory` checkout 174 behind
      and STILL carrying the shed validator — so before §10.1 it resolved
      candidate 3 and went green against a contract version nothing pins. That
      is the hazard §10.1 removes, now measured rather than asserted.)
- [x] 4.10 Rollback recorded before the step: openxFactory pins `wallet-v1.0` and
      **P3 is BLOCKED** until the prune lands.
      **Evidence:** RECORDED BEFORE THE STEP — `design.md:538` in the migration plan
      ("*Rollback:* openxFactory pins `wallet-v1.0` and P3 is blocked until the prune
      lands"), written when P2b was authored and before openXwallet #2 was opened.
      The step was taken and NOT reverted: `wallet-v1.1` is the tag openxFactory
      actually pins (§7.2), so the rollback is a recorded path that was never
      exercised, which is the state this task asks be provable.

## 5. P2.5 — the openxFactory deprecating minor

*A precondition of P3's class: `docs/contract-versioning-policy.md:250-252` makes
a removed shape BREAKING and requires one full preceding minor.*

- [x] 5.1 Each of the eight manifest rows at `contracts/manifest.yaml:1967-2082`
      gains ONE sibling key as a nested mapping: `relocating: {to:
      opensoft/openXwallet, tag: wallet-v1.0, since: contract-v<the P2.5 minor>}`.
      **Evidence:** REALIZED (feature 018-openxwallet-deprecation-minor, `contract-v1.47`): all eight rows carry
      `relocating: {to: opensoft/openXwallet, tag: wallet-v1.1, since: contract-v1.47}`
      as their LAST key. **Tag is `wallet-v1.1`, not this line's `wallet-v1.0`** —
      that literal predates P2b; this file's own preamble says openxFactory's P3
      pin records `wallet-v1.1` and the proposal calls it the tag openxFactory
      actually pins. The block is at `contracts/manifest.yaml:1992-2107` today,
      not `:1967-2082`.
- [x] 5.2 **NO `removed_at` on the row.** `:245-247` puts the removal version and
      the migration path in the CHANGELOG, and naming the next MAJOR is permitted
      where naming the minor is not — `:30-31` forbids reserving a MINOR before
      merge order is known, and there is exactly one next major.
      **Evidence:** REALIZED: no removal key on any row. The removal version is in the
      changelog only, named concretely as `contract-v2.0` per the three existing
      entries in the policy's "Deprecations Currently In Force" list.
- [x] 5.3 `contracts/CHANGELOG.md` gains the deprecation entry stating BOTH
      required facts: removal at the next MAJOR bundle, and the migration path via
      `contracts/openxwallet-pin.yaml` plus
      `openXwallet/docs/pin-resync-runbook.md`.
      **Evidence:** REALIZED: `contracts/CHANGELOG.md` § `contract-v1.47` states both required
      facts — removal at `contract-v2.0`, and the migration path via
      `contracts/openxwallet-pin.yaml` plus `openXwallet/docs/pin-resync-runbook.md`,
      with the validator-moves-with-the-contracts discharge of `:251-252` spelled
      out. The policy doc's in-force list gains a matching entry (the
      `contract-v1.34` precedent).
- [x] 5.4 The emitter is `scripts/check-openxfactory-pin.py` — the only candidate
      with a warning tier (`PASS, WARN, ERROR, SKIP` at `:35`, returned by
      `classify()` at `:43`). It warns when a domain pins a bundle carrying
      `relocating:` rows.
      **Evidence:** REALIZED: `scripts/check-openxfactory-pin.py` reads the manifest AT THE
      CONSUMER'S PINNED COMMIT and emits a WARN naming every relocating artifact
      with target and tag. `classify()` is byte-unchanged; the notice is additive
      to the verdict; exit stays `1 if verdict == ERROR else 0`. Six new tests in
      `tests/conformance-gate/test_conformance_checks.py`.
- [x] 5.5 Record why `scripts/validate-domain-openxfactory-pins.py` is NOT the
      emitter: no `warn` token in its 138 lines, so making it emit would force a
      relocation notice to be an ERROR and red every domain pinning the deprecation
      minor — precisely the failure the manifest-carried marker was chosen to
      avoid.
      **Evidence:** RECORDED — and in the code, not only here: the reason now lives in
      `scripts/check-openxfactory-pin.py`'s module docstring, so it survives
      without this file. `validate-domain-openxfactory-pins.py` is untouched.
- [x] 5.6 **`scripts/validate-openxwallet.py` is NOT edited in openxFactory by
      P2.5.** The withdrawn validator-warning reading stays withdrawn, on all three
      re-verified reasons: LedgerxFactory runs `--strict`, `:2107` reds on `strict
      and f.warnings`, and openxFactory's own gate runs WITHOUT `--strict` so
      nothing required would surface it anyway.
      **Evidence:** HONOURED: `scripts/validate-openxwallet.py` is untouched, and the whole
      byte-identity floor verifies empty against the base commit.
- [x] 5.7 `contracts/releases/<the P2.5 minor>.digests.yaml` over a release
      surface that STILL CONTAINS the eight artifacts — a minor that skips it is a
      non-conformant release under `release-surface-integrity`.
      **Evidence:** REALIZED: `contracts/releases/contract-v1.47.digests.yaml`, 192 members,
      generated by `validate-contract-release.py build` and byte-reproducible.
      **Correction for P3's author**: inventory membership is catalog-driven from
      `contracts/hermes-runtime/contract-index.yaml`, so the eight artifact FILES
      have never been inventory members — not at `contract-v1.45` either. The
      surface "still contains" them TRANSITIVELY: `contracts/manifest.yaml` IS a
      digested member and the digest recorded is an eight-row manifest's.
- [x] 5.8 **[OPERATOR]** Allocate the minor number AT MERGE ORDER, never before
      (`:30-31`), and cut the tag — a bundle is not published until its tag exists.
      **NOT TICKED — deliberately.** Feature 018 authors the bundle as
      `contract-v1.47` and states in its pull request that the number is
      RE-VERIFIED at merge order per `:30-31`; four places carry it (the
      manifest line, the eight `since:` keys, the changelog heading, the
      inventory filename) and they move together if another bundle lands
      first. The tag is NOT created: `contract-v1.44` and `contract-v1.45`
      are both annotated tags cut by the operator and no workflow makes
      them. This box closes when Brett cuts the tag on the merged commit.
      **CLOSED 2026-08-27.** The operator cut the annotated tag `contract-v1.47`
      on `af7ac0fa4d31ffeec45524a0fe74524ba5b5b22c`, and `python3
      scripts/validate-contract-release.py verify-tag --remote origin --tag
      contract-v1.47` returns `release verify-tag: pass`. The number HELD at merge
      order — no other bundle landed between authoring and merge, so none of the
      four places carrying it had to move. P2.5 is therefore a PUBLISHED bundle
      (`docs/contract-versioning-policy.md:31-32`), which is the precondition P3's
      major needs to exist at all. Ticked by feature `023-openxwallet-consume-shed`.
- [x] 5.9 Evidence row: the eight `relocating:` rows, the CHANGELOG migration
      note, `check-openxfactory-pin.py`'s WARN output, AND the minor's own
      `contracts/releases/<tag>.digests.yaml`.
      **Evidence:** REALIZED: the four evidence items are the eight rows, the changelog
      section, `specs/018-openxwallet-deprecation-minor/evidence/warn-sample.txt`
      (the checker's literal output against a fixture consumer pinned to this
      bundle), and the digests inventory. The cut also discharges a pre-existing
      error-class release-inventory-drift finding on
      `scripts/validate-hermes-runtime-contracts.py`.
- [x] 5.10 Rollback recorded before the step: a published bundle is not
      unpublished. The honest reversal is a FOLLOWING minor that removes the
      marker, never a revert of the cut.
      **Evidence:** RECORDED before the step, in `contracts/CHANGELOG.md` § `contract-v1.47`
      "Rollback posture": a published bundle is not unpublished; the honest
      reversal is a FOLLOWING minor that removes the marker.
## 6. P5a.2 — LedgerxFactory `stack.yaml` bump to the P2.5 minor

*After P2.5 is cut, before P3. A second pull request, because one pull request
cannot both precede P2 and pin a bundle P2.5 has not published.*

- [x] 6.1 **[LedgerxFactory]** `stack.yaml` `xfactory.contract_ref` bumped from
      openxFactory `39539fd4…` (`:13-14`) to the P2.5 minor, at
      `contract_ref_type: commit`.
      **Evidence:** REALIZED — [LedgerxFactory #29](https://github.com/opensoft/LedgerxFactory/pull/29)
      merged `e09902d7c6a5cd9abfe3cdeda6599496833c3b09`. `contract_ref` goes
      `39539fd4…` → `af7ac0fa…` (openxFactory `contract-v1.47`, the deprecating
      minor) in exactly two changed lines, with `contract_ref_type` still `commit`;
      `models/protected-surface.yaml` re-pins `stack.yaml`'s digest in the same
      commit, per that surface's own admission rule. Speckit feature
      `018-openxwallet-pin-bump`.
- [x] 6.2 **[LedgerxFactory]** Add one invocation of the pinned
      `check-openxfactory-pin.py` to the estate run, so the relocation warning is
      OBSERVED by the one live consumer; without this half the deprecation window
      is unobserved and the policy's precondition is a formality.
      **Evidence:** REALIZED — [LedgerxFactory #29](https://github.com/opensoft/LedgerxFactory/pull/29)
      merged `e09902d7c6a5cd9abfe3cdeda6599496833c3b09`. One sibling check,
      `check_pin_reconciliation()`, plus a pure `read_pin_report()` and two probe
      suites, in pure insertions. The checker is extracted from the commit
      `stack.yaml` pins (`git show <pin>:scripts/check-openxfactory-pin.py`) rather
      than read off a neighbouring working tree — the first cut reproduced the exact
      bug this task exists to prevent, observing nothing while the bar went green
      against a checkout predating the minor.
- [x] 6.3 **[LedgerxFactory]** Evidence: a green estate run with the
      `relocating:` warning in the run log — the checker's OUTPUT, not the manifest
      rows.
      **Evidence:** REALIZED — [LedgerxFactory #29](https://github.com/opensoft/LedgerxFactory/pull/29)
      merged `e09902d7c6a5cd9abfe3cdeda6599496833c3b09`. The run log carries `WARN:
      the pinned openxFactory bundle contract-v1.47 carries 8 relocating contract
      row(s)` and names all eight rows individually, inside `WALLET ESTATE: PASS`,
      exit 0. Both the local-checkout run and the `origin/main` run are captured
      deliberately, because presenting one alone would misreport the other. Copilot
      reviewer run 33108631778; LedgerxFactory runs no other CI gate.
- [x] 6.4 **[LedgerxFactory]** Rollback recorded before the step: revert to
      `39539fd4…`.
      **Evidence:** RECORDED BEFORE THE STEP — `design.md:547` ("*Rollback:* revert
      to `39539fd4…`") and the feature's own `rollback.md`, cited in
      [LedgerxFactory #29](https://github.com/opensoft/LedgerxFactory/pull/29), merged
      `e09902d7c6a5cd9abfe3cdeda6599496833c3b09`. Not exercised.

## 7. P3 — openxFactory consumes and sheds, ONE atomic pull request. BREAKING

*One PR because `scripts/validate-trust-anchor.py:2582-2586` exits 2 when the
custody registry is absent: no ordering of two commits leaves a green
intermediate.*

- [x] 7.1 **[OPERATOR]** **Sequencing guard, and there is no third option:**
      `governance/review-authority/register.yaml:37` carries `expires_at:
      "2026-11-23T12:00:00Z"` and `check_register` raises `register-row-expired`
      as an ERROR past that instant, reddening the REQUIRED gate on every later
      pull request — the wave's own included — and making its evidence rows
      unfillable. **Either re-issue the row before 2026-11-23, or do not schedule
      P3 after 2026-11-01.** Record which was chosen.
      **Evidence:** RECORDED — **the second option was chosen: P3 is not scheduled
      after 2026-11-01.** This pull request is opened 2026-08-27, 66 days inside the
      window, so the row is not re-issued and `expires_at: "2026-11-23T12:00:00Z"`
      is left exactly as it stands. The gate proves the row is live today: the
      consumer-gate log carries `intake register read:
      governance/review-authority/register.yaml (1 row(s))` and NO
      `register-row-expired`. If the merge slips past 2026-11-01 the choice
      re-opens and the row must be re-issued first; there is still no third
      option.
- [x] 7.2 Add the nested submodule `openXwallet/` at `wallet-v1.1`, plus the
      `.gitmodules` entry keeping `git@github.com:` (openXwallet is PRIVATE; an
      anonymous HTTPS clone fails and a token is needed either way, while an HTTPS
      URL makes every human clone prompt for credentials).
      **Evidence:** REALIZED. `.gitmodules` gains `[submodule "openXwallet"] path =
      openXwallet / url = git@github.com:opensoft/openXwallet.git`; the recorded
      gitlink is `63f5a1adac89f017e70bab9a4ffe7cf02d6e6705` and
      `git -C openXwallet describe --tags` returns `wallet-v1.1`. The tag is an
      ANNOTATED tag (object `021cdeef…`) whose `object.sha` is that commit, resolved
      through the API rather than assumed.
- [x] 7.3 `contracts/openxwallet-pin.yaml` — `kind: pinned_contract_manifest`
      reused UNCHANGED, on the realized keycloak-install shape field for field,
      plus `submodule_path: openXwallet` (borrowed from
      `MedxChart/contracts/openchart-pin.yaml:8`, because a pin with no path
      cannot be checked against a gitlink) and `carve_commit:` (in the FILE, not
      only the runbook, because the byte-identity referent must survive into the
      tree the gate reads).
      **Evidence:** REALIZED at `contracts/openxwallet-pin.yaml`. `kind:
      pinned_contract_manifest` reused byte-unchanged; `submodule_path:
      openXwallet`; `carve_commit: "30565e48ffe3d8a9773e10af33425701845e10f6"` in the
      FILE. One field beyond D1's shape: `verify_pin:
      scripts/verify-openxwallet-pin.py`, mirroring the sibling pin
      (`openXwallet/contract_pin.yaml`) so clarification N3's "running code, not
      prose" is declared in the pin itself rather than only in the workflow.
- [x] 7.4 The pin's `files:` carries the EIGHT digested members (seven under
      `contracts/openxwallet/` plus
      `openxwallet-agent-profile/openxwallet-agent-composition.schema.yaml`) and
      `pinned_by_commit_only:` carries the validator, the syntax gate, both
      `examples/` directories and both family READMEs — path only, with no invented
      per-file digests for members the publisher declares content-addressed by
      commit. `revision_kind: commit` with a 40-hex `commit`; `contract_bundle_tag:
      wallet-v1.1` is a LABEL beside them and never the trusted referent, and a
      tag-only pin is refused.
      **Evidence:** REALIZED. `files:` carries the EIGHT digested members — the seven
      under `contracts/openxwallet/` plus
      `openxwallet-agent-profile/openxwallet-agent-composition.schema.yaml` — with the
      `sha256` values copied from the manifest rows AND independently recomputed
      against the submodule (two derivations, one answer). `pinned_by_commit_only:`
      carries six path-only members: both scripts, both `examples/` directories and
      both family READMEs. `revision_kind: commit` with a 40-hex `commit`;
      `contract_bundle_tag: wallet-v1.1` sits beside them as a label and a tag-only
      pin is refused (`pin-tag-only`).
- [x] 7.5 `scripts/verify-openxwallet-pin.py` — six ordered checks: `openXwallet/.git`
      **exists** (a submodule's `.git` is a FILE, so not `is_dir()`); the RECORDED
      gitlink (`git ls-tree HEAD -- openXwallet`) equals `commit`; the CHECKED-OUT
      revision (`git -C openXwallet rev-parse HEAD`) equals `commit` — both,
      because a detached checkout can differ from the recorded gitlink and only one
      comparison catches each case; each of the eight `files:` members recomputes
      to its `sha256`; every `pinned_by_commit_only:` path exists; `revision_kind`
      is `commit` and `commit` is 40 hex.
      **Evidence:** REALIZED at `scripts/verify-openxwallet-pin.py` — six ordered
      checks exactly as specified, including `.exists()` rather than `is_dir()` on
      `openXwallet/.git` and the two SEPARATE comparisons (recorded gitlink, then
      checked-out revision). One documented addition: when `git ls-tree HEAD --
      openXwallet` is empty because the gitlink is staged and not yet committed, the
      recorded gitlink is read from the INDEX and the output says so — CI always has
      it in HEAD, and a pre-commit local run must still be checkable rather than
      silently unrunnable.
- [x] 7.6 Its refusals exit 2 with NAMED codes —
      `pin-submodule-uninitialized`, `pin-gitlink-mismatch`,
      `pin-checkout-mismatch`, `pin-digest-mismatch`, `pin-member-missing`,
      `pin-tag-only` — and every fail-closed refusal in this wave prints the one
      fixed remediation trailer: `git submodule update --init
      openXwallet` (NOT `--recursive`; the wave's init is deliberately scoped),
      and `openXwallet/docs/pin-resync-runbook.md` if the pin itself
      is stale.
      **Evidence:** REALIZED. All six codes exit 2 and are reproduced hermetically in
      `tests/openxwallet_pin/test_verify_pin.py` (35 cases, zero skips). The one fixed
      trailer is the module constant `REMEDIATION`: *Remediation: run `git submodule
      update --init openXwallet` (NOT --recursive; this wave's init is deliberately
      scoped). If the pin itself is stale, follow
      `openXwallet/docs/pin-resync-runbook.md`.* A seventh code `pin-unreadable`
      covers a pin that states no checkable claim; it is deliberately NOT in
      `REFUSAL_CODES`, and a test asserts that.
- [x] 7.7 `scripts/verify-openxwallet-pin.py --aggregation-root <path>` mode: the
      root-gitlink-equals-nested-gitlink check P4 invokes. One implementation, one
      refusal vocabulary, living in openxFactory.
      **Evidence:** REALIZED. `--aggregation-root <path>` reads the aggregation's
      root-level `openXwallet` gitlink (HEAD, index fallback) and compares it against
      the pin's `commit` — which IS the nested gitlink, since checks 2 and 3 have
      already pinned both nested values to it, so there is one referent rather than
      two that must be kept equal. Run against `/home/brett/projects/xFactory` today
      it refuses `pin-member-missing`, correctly: the aggregation carries no such
      gitlink until P4.
- [x] 7.8 `scripts/validate-trust-anchor.py`: `OPENXWALLET_REGISTRY_PATH`
      (`:322-323`) stays a MODULE-SCOPE plain `Path`, rebased onto the pin's
      `submodule_path` as a pure string join with NO I/O — because
      `tests/trust-anchor/test_negative_corpus.py:47` and
      `test_declaration_perimeter.py:55` both call
      `MODULE.load_yaml(MODULE.OPENXWALLET_REGISTRY_PATH)` at setup, and any
      resolution that can fail at import kills every trust-anchor test at
      collection.
      **Evidence:** REALIZED. `OPENXWALLET_REGISTRY_PATH = ROOT / "openXwallet" /
      "contracts" / "openxwallet" / "openxwallet-custody.registry.yaml"` — module
      scope, plain `Path`, pure string join, no I/O, `openXwallet` as a LITERAL rather
      than read from the pin (reading the pin here would be import-time I/O).
      `pytest tests/trust-anchor/ -q --collect-only` collects 93 with no errors, which
      is the property the constraint exists to protect. `:2614`'s
      `relative_to(ROOT)` still resolves and the note now names the path under
      `openXwallet/`.
- [x] 7.9 The pin-and-digest check runs inside `main()`, never at import, and
      the bare file-absent exit at `:2582-2586` is REPLACED by the verifier's
      call — so the refusal gains identity where it had only presence. Rule (f)
      (`:1146-1176`) fails closed on an uninitialized submodule or a digest
      disagreeing with the pin.
      **Evidence:** REALIZED. The bare `is_file()` exit is replaced inside `main()` by
      `refuse_unless_openxwallet_pinned()`, which loads the verifier LAZILY (this
      module is imported by the tests, so an import-scope load makes them
      uncollectable), calls `verify(ROOT)`, and prints the composition context before
      the verifier's own refusal so the fixed trailer stays last. A verifier that will
      not load is itself a refusal — never a fallback to presence. No `--strict` gate,
      no opt-in, no warning tier.
- [x] 7.10 `tests/trust-anchor/` follows the repoint: the negative corpus and the
      declaration perimeter read the wallet registry through the `openXwallet/`
      gitlink, and two new cases cover the uninitialized-submodule and
      digest-disagreement refusals by their named codes.
      **Evidence:** REALIZED. `tests/trust-anchor/test_openxwallet_pin_refusal.py`
      covers `pin-submodule-uninitialized` and `pin-digest-mismatch` by NAMED CODE,
      each asserting the code, its membership in the verifier's `REFUSAL_CODES`, the
      remediation trailer in stderr, exit 2 and EMPTY stdout (proving short-circuit,
      not warn-through). Three further cases were added because the change introduced
      the paths: a verifier-unloadable case where the registry IS present (proving
      presence buys nothing), the literal-vs-`submodule_path` agreement check, and an
      import-with-nothing-on-disk subprocess probe. The negative corpus and the
      declaration perimeter needed no edit — both already read through
      `MODULE.OPENXWALLET_REGISTRY_PATH` — and were deliberately not churned.
      `tests/trust-anchor/`: 93 passed, 0 skipped.
- [x] 7.11 Delete the twelve path sets' openxFactory copies — with the THREE
      deliberate exceptions: the two promoted specs empty when `openspec archive`
      applies the REMOVED deltas, and
      `openspec/changes/archive/2026-08-08-add-openxwallet/` is a record that is
      ANNOTATED, never removed.
      **Evidence:** REALIZED — 92 files deleted, which is the carve's 100 minus the
      three exceptions' 8, and that arithmetic IS the completeness check. Deleted:
      `contracts/openxwallet/`, `contracts/openxwallet-agent-profile/`,
      `scripts/validate-openxwallet.py`, `scripts/wallet-yaml-syntax-gate.py`,
      `tests/wallet_yaml_syntax_gate/`, `.github/workflows/wallet-validation.yml`,
      `specs/006-openxwallet-contracts/`, `specs/010-wallet-validator-ci/`,
      `specs/012-wallet-issuer-anchor/`. Left in place: the two promoted specs (for
      `openspec archive` to empty via the ratified REMOVED deltas) and
      `openspec/changes/archive/2026-08-08-add-openxwallet/`, annotated in `README.md`
      and `docs/archive-record-discrepancies.md` and never removed.
- [x] 7.12 `.github/workflows/wallet-validation.yml` →
      `.github/workflows/openxwallet-consumer-gate.yml`, with `jobs:
      wallet-validation:` **RETAINED**. Ruleset 21538893 is edited by NOTHING in
      this wave; the token reports on P3's own pull-request head from the new file;
      no operator act stands between P3 and merge.
      **Evidence:** REALIZED. `.github/workflows/openxwallet-consumer-gate.yml`
      declares `jobs:` key `wallet-validation` and carries no job `name:`;
      `wallet-validation.yml` is deleted in the same commit. Ruleset 21538893 is
      untouched by this feature. A test asserts the job id, the absence of a display
      name, and that the retired FILE does not survive alongside the new one — two
      workflows declaring the same required job id would let the ruleset be satisfied
      by whichever ran the weaker gate.
- [x] 7.13 The consumer gate's steps, in order: `create-github-app-token@v2` →
      `git config --global url."https://x-access-token:$TOKEN@github.com/".insteadOf
      "git@github.com:"` BEFORE checkout → checkout → scoped `git submodule update
      --init openXwallet` (NOT `--recursive`) → `verify-openxwallet-pin.py` →
      `python3 openXwallet/scripts/wallet-yaml-syntax-gate.py .` → `python3
      openXwallet/scripts/validate-openxwallet.py . | tee wallet-gate.log` (no
      `--strict`, unchanged from `wallet-validation.yml:34`) → the positive
      register assertion.
      **Evidence:** REALIZED in that order. One correction of substance: the token is
      minted from `OPENXFACTORY_APP_ID` / `OPENXFACTORY_APP_PRIVATE_KEY`, not
      `XFACTORY_APP_*`. The org secret `XFACTORY_APP_ID` is visibility-`selected` and
      openxFactory is NOT one of its two repositories, so the ratified name would have
      resolved to EMPTY here and the nested clone would have failed with a 403 that
      reads like a missing submodule. The PATTERN is the ratified one; the secret names
      are this repository's own content App (App `4253636`, installation `145372182`,
      `repository_selection: all`, so no installation edit was needed). Recorded in
      `specs/023-openxwallet-consume-shed/research.md` R1 and
      `evidence/operator-acts.md`. The validator step additionally declares
      `shell: bash` so it runs under `-o pipefail`: the default `run` shell does not
      set it, and `| tee` would otherwise return 0 over a failing validator.
- [x] 7.14 `tests/openxwallet_consumer_gate/test_gate_invocation.py`, collected by
      the REQUIRED `pytest-suite`: it loads the workflow YAML, asserts `jobs`
      contains `wallet-validation`, and asserts one step's `run` is EXACTLY
      `python3 openXwallet/scripts/validate-openxwallet.py .` — the argument
      present AND equal to `.`, because `repo_scan` runs only `if args.path is not
      None` and reads the register only `if sweep`, where `sweep =
      target.is_dir()`. A missing or file-valued argument is a green check that
      opened no register.
      **Evidence:** REALIZED at `tests/openxwallet_consumer_gate/test_gate_invocation.py`
      (14 cases). It asserts `jobs` contains `wallet-validation`, that exactly ONE step
      invokes the pinned validator, that its `run` equals the whole ratified line
      `python3 openXwallet/scripts/validate-openxwallet.py . | tee wallet-gate.log`,
      AND that the command half equals exactly `python3
      openXwallet/scripts/validate-openxwallet.py .` — which honours 7.13's line and
      7.14's "present AND equal to `.`" together and is strictly stronger than either.
      Also pinned: no `--strict`, `shell: bash`, the step ORDER, the scoped init, the
      ABSENCE of a blanket `submodules:` on the checkout, and that neither departing
      openxFactory reader exists.
- [x] 7.15 The register assertion is POSITIVE and needs no edit to the pinned
      code: the gate log carries the `repo scan: N openxWallet artifact` note AND
      carries neither `no intake register at this tree` nor any `register-*`
      finding code, which together prove `reg_path.exists()` was true AT the scan
      target. The test asserts that conjunction AND `wallet-v1.1`'s
      register-read NOTE, so it does not go stale across the tag.
      **Evidence:** REALIZED as the POSITIVE conjunction, in the workflow and in the
      test. Measured locally against the pinned reader on the post-shed tree:
      `note  intake register read: governance/review-authority/register.yaml (1
      row(s))` and `note  repo scan: 2 openxWallet artifact(s) validated, 1612
      document(s) skipped as another kind`, with no `no intake register at this tree`
      line and no `[register-*]` code. The scan count moved 3 → 2 across the shed
      because openxFactory's own copy of the custody registry was being adjudicated as
      a live record and is gone; the remaining two are the live grant and attestation
      under `governance/review-authority/`, which is exactly the population R6 keeps
      here.
- [x] 7.16 `.github/workflows/pytest-suite.yml`: the same app-token +
      `insteadOf` + scoped-init pattern added to its checkout (`:203-206`, which
      has none of it today) — `submodules: true` alone is NOT sufficient and is
      explicitly not the fix.
      **Evidence:** REALIZED. `pytest-suite.yml` gains the app-token step, an
      `insteadOf` step with `working-directory: .` (the job's default
      working-directory is `openxFactory`, which does not exist before checkout), and a
      scoped `git submodule update --init openXwallet` after checkout.
      `submodules: true` is deliberately NOT added, exactly as this task requires, and
      the consumer-gate test asserts the equivalent for the gate: a blanket init would
      also fetch `installs/omnigent-install`, which no test here reads.
- [x] 7.17 `pytest-suite.yml`'s pinned header count at `:37` becomes a pinned
      TRIPLE — collected, passed, SKIPPED — read from the JUnit XML attributes
      rather than grepped from the human summary, so a silently skipped
      `tests/trust-anchor/` moves a pinned number and fails.
      **Evidence:** REALIZED. A new step parses `pytest-report.xml`'s `<testsuite>`
      attributes and pins a TRIPLE — selected (the JUnit `tests` attribute, which is
      collection minus the `-m "not postgres"` deselection), passed, and SKIPPED —
      additionally requiring `failures` and `errors` to be zero. The header records why
      SELECTED is not `--collect-only`'s number, because conflating the two is how a
      pin like this goes stale in one direction and unnoticed in the other. The values
      are pinned from CI's OWN run, not from a developer machine: this worktree sits
      under the aggregation, so locally-resolving self-skip guards make the two
      environments differ by design — which is the same two-skip difference the
      workflow header already documented.
- [x] 7.18 `pytest-suite.yml`'s three `wallet-validation.yml` references at `:5`,
      `:14` and `:148` renamed to `openxwallet-consumer-gate.yml`.
      **Evidence:** REALIZED — all three references now read
      `openxwallet-consumer-gate.yml`, and
      `grep wallet-validation.yml .github/workflows/pytest-suite.yml` is empty.
- [x] 7.19 `.github/workflows/doc-health-reusable.yml`: BOTH non-recursive
      governed-submodule init filters (`:154-158`, `:815-819`) gain a second
      scoped init for `openxFactory/openXwallet`. Not `--recursive`, which would
      pull `installs/omnigent-install` and every domain's nested submodules into
      every aggregation doc-health run.
      **Evidence:** REALIZED at BOTH sites. Each gains `git -C openxFactory submodule
      update --init openXwallet` — note the `-C openxFactory`: `openXwallet` is a
      submodule OF a submodule, so the existing filter cannot reach it (it reads the
      AGGREGATION's `.gitmodules`, which declares `openxFactory` and nothing below it).
      NOT `--recursive`. One addition beyond the ratified text: the init is GUARDED on
      the nested `.gitmodules` actually declaring `submodule.openXwallet.path`, because
      the aggregation's openxFactory pin moves in a LATER pull request (P4 after P3)
      and an unguarded invocation would fail the nightly for the wave's ordering rather
      than for a defect.
- [x] 7.20 `contracts/manifest.yaml`: the eight rows at `:1967-2082` DELETED, and
      the seven incoming citations at `:2089`, `:2146`, `:2251`, `:2287`, `:2423`,
      `:2473-2475` and `:2494-2495` REWORDED to the pin — never deleted, because
      the precedent each cites still holds.
      **Evidence:** REALIZED. The eight rows AND their family header comment are
      deleted (the header is the "content-addressed by commit" declaration for the
      family that left) and replaced by a comment pointing at the pin and the migration
      path. The SEVEN incoming citations were re-located BY CONTENT because the line
      numbers had drifted, and all seven are REWORDED, none deleted: the two
      no-per-file-digest precedents, the credential-contracts holder citation, the
      trust-anchor precedent, the revocation-vocabulary constant, the PATH-BEARING
      custody-correspondence citation (now
      `openXwallet/contracts/openxwallet/openxwallet-custody.registry.yaml`, with the
      refusal named), and the chain-custody correspondence prose.
      `contract_bundle_version: contract-v2.0`.
- [x] 7.21 `contracts/README.md:106-108` collapses to ONE "consumed at pin" row;
      `contracts/CHANGELOG.md` gains the MAJOR entry with the removal and the
      migration path; `contracts/releases/<the major>.digests.yaml` over a release
      surface that NO LONGER contains the eight artifacts.
      **Evidence:** REALIZED. `contracts/README.md`'s three wallet rows collapse to ONE
      "consumed at pin" row, and the two trust-anchor rows that cited the wallet
      registry by path are repointed. `contracts/CHANGELOG.md` gains the MAJOR entry,
      which discharges all three `:250-254` clauses EXPLICITLY — including the third by
      naming the move itself as the conformance-validator update.
      `contracts/releases/contract-v2.0.digests.yaml` was built by `python3
      scripts/validate-contract-release.py build --tag contract-v2.0` (192 entries) and
      a second build is byte-identical. Also `docs/contract-versioning-policy.md` moves
      the openxWallet deprecation from "Currently In Force" into a new "Deprecations
      Executed" section — recorded, not deleted, because a consumer upgrading ACROSS
      the removal needs the migration path readable at the version it upgrades TO.
- [x] 7.22 `README.md` at every range the proposal names: `:217-228` (the wallet
      validation gate section — the workflow FILE is renamed while the ruleset
      TOKEN is deliberately unchanged), `:286-293`, `:310`, `:805`, `:873-927`
      (including `:896`'s "advisory until an operator marks it required", already
      STALE against ruleset 21538893 and corrected in this wave; `:909-912`'s
      declined-floor prose stands unchanged; `:920-921` names the retiring
      workflow and both departing scripts), `:2523-2536` — **not** `:2254-2265`,
      which is `align-demote-to-round-trip-rule` — and `:2612`.
      **Evidence:** REALIZED at every range, re-located BY CONTENT since the numbers
      had drifted. The gate section now describes the CONSUMER gate, the pinned
      readers, the POSITIVE register assertion and the alias, and its owner-routing
      list is the new surface set. The contract-index entry is marked CONSUMED AT PIN.
      The trust-anchor index citation and the `add-trust-anchor` ledger citation are
      repointed to the pin, not deleted. The STALE "advisory until an operator marks it
      required" is corrected in place, with its own history stated (true at authoring,
      stale from 2026-08-26). The declined-floor prose stands unchanged. The S1
      successor sentence is put in the past tense with the successor named. The
      `add-openxwallet` archive-ledger entry is ANNOTATED, never rewritten. The
      active-change ledger gains a realization note naming all four Speckit features
      and what is still open.
- [x] 7.23 `.github/CODEOWNERS` drops the two validator lines (`:3-4`) and gains
      `contracts/openxwallet-pin.yaml` and the `openXwallet` gitlink.
      **Evidence:** REALIZED. `.github/CODEOWNERS` drops
      `/scripts/validate-openxwallet.py` and `/scripts/wallet-yaml-syntax-gate.py` and
      gains `/contracts/openxwallet-pin.yaml`, `/scripts/verify-openxwallet-pin.py`,
      `/openXwallet` and `/.gitmodules`, with a comment stating the reason: those four
      are what determine WHICH READER RUNS, which is the class the 2026-08-23 ruling
      routes to an owner.
- [x] 7.24 `docs/archive-record-discrepancies.md` row 7 gains a "carried to
      openXwallet" NOTE. Records are annotated, never rewritten into agreement.
      **Evidence:** REALIZED. Row 7 gains a "carried to openXwallet" NOTE naming the
      tag, the pin and the fact that the archived packet STAYS. The row's own
      discrepancy is untouched — a record is annotated, never rewritten into agreement
      with a later tree. The file already carried a pre-existing `record-immutability`
      critical finding on `origin/main`; the annotation adds no new one, proven by the
      identical doc-health finding sets recorded in
      `specs/023-openxwallet-consume-shed/evidence/validation.md`.
- [x] 7.25 `add-wallet-carried-review-authority` — FOUR live-change edits, not
      record annotations: `tasks.md:81`, `:100`, `:134` and `:204` each name the
      departing script inside an ACTIVE change. Plus an addendum recording that
      task 2.6's red-proof is RETARGETED at the consumer gate, and that S3/S5's
      `openxwallet` / `openxwallet-agent-profile` core deltas are authored in
      openXwallet from here on (its `tasks.md` 8.1 ruling itself needs no edit).
      **Evidence:** REALIZED — FIVE live-change edits rather than four, because the S1
      realization bullet naming the retiring workflow FILE is the same class as the four
      the proposal enumerated and would otherwise have been left naming a file that no
      longer exists. Plus the addendum, which records BOTH obligations the proposal
      names: task 2.6's red-proof RETARGETED at the consumer gate (with the reason it
      cannot discharge in openXwallet — that tree has no
      `governance/review-authority/`), and S3/S5's `openxwallet` /
      `openxwallet-agent-profile` core deltas authored in openXwallet from here on. Its
      `tasks.md` 8.1 ruling is unchanged, as ratified.
- [x] 7.26 **Sequencing guard: the declared manifest freeze is UNENFORCEABLE.**
      P3 REBASES and RE-VERIFIES the eight digests immediately before merge, and
      THAT re-verification — not a P2-era artifact reused — is what P3's evidence
      row carries. Commits use explicit pathspecs.
      **Note (feature `023-openxwallet-consume-shed`, 2026-08-27): DELIBERATELY OPEN.**
      The authoring-time verification is done and green — `python3
      scripts/verify-openxwallet-pin.py` recomputes all eight digests against the
      pinned submodule and exits 0 — but this task's whole point is that the
      authoring-time artifact is NOT what the evidence row carries. It closes on the
      pre-merge rebase and RE-verification, which is the operator's last act before
      merging. Commits in this pull request use explicit pathspecs, as required.
      **Evidence:** REALIZED AT MERGE. Immediately before merging, `main`
      (`4def2274…`) was ONE commit ahead of the merge-base (`94933adf…`) with NO
      overlapping files — `comm -12` of the two changed-file sets (17 files on
      `main`, 123 on the pull request) is empty. `python3
      scripts/verify-openxwallet-pin.py` on the pull request head printed `OK
      openxwallet-pin verified: openXwallet@63f5a1adac89f017e70bab9a4ffe7cf02d6e6705
      (tag label wallet-v1.1), gitlink read from HEAD, 8 digest(s) recomputed`, and
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` reported `76 passed, 0
      failed`. The merge landed at `c9a1500e1a960be827cd714d8024d9aacb40aeb2` (merge
      commit, PR #431), and the SAME verifier line re-ran there — reconfirmed in this
      evidence pass with the submodule freshly initialized: `OK openxwallet-pin
      verified: openXwallet@63f5a1adac89f017e70bab9a4ffe7cf02d6e6705 (tag label
      wallet-v1.1), gitlink read from HEAD, 8 digest(s) recomputed`. Tag
      `contract-v2.0` is cut on that commit and `validate-contract-release.py
      verify-tag --remote origin --tag contract-v2.0` returns `release verify-tag:
      pass`. Commits in this pull request used explicit pathspecs, as required.
- [x] 7.27 `governance/review-authority/` STAYS — all four files (R6). Assert it
      in the pull request: nothing under that directory is touched by P3.
      **Evidence:** ASSERTED and CHECKED. `git diff --stat origin/main -- governance/`
      is EMPTY: all four files under `governance/review-authority/` are untouched by
      this pull request, and the pull request body carries the same assertion. The
      register is also proven LIVE by the gate log's `intake register read:` NOTE — the
      data stayed and only the reader travelled.
- [x] 7.28 Evidence row: green `wallet-validation` (the token, from the renamed
      file) on P3's OWN head, plus the post-rebase digest re-verification.
      **Note (feature `023-openxwallet-consume-shed`, 2026-08-27): HALF DISCHARGED — the
      ALIAS IS PROVEN.** Pull request
      [#431](https://github.com/opensoft/openxFactory/pull/431) reports
      **`wallet-validation: pass`** on its own head, produced by
      `.github/workflows/openxwallet-consumer-gate.yml` — run
      **33109575651**, job **98648509131**, 2026-08-27. Ruleset 21538893 was edited by
      nothing. That settles the only question the alias resolution could have got
      wrong — and it settled it FOUR TIMES, on every head this pull request has had
      (runs 33109575651, 33111235422, 33112622519, **33114027225**), each produced by
      the new file. `pytest-suite` is green alongside it on the final head (run
      **33114027245**, job **98663924140**, 13m39s,
      `selected=7116 passed=7096 skipped=20 failures=0 errors=0`).
      The row stays OPEN for its SECOND half: the post-rebase digest
      re-verification of 7.26, taken immediately before merge. A green run against a
      pre-rebase head does not discharge that half.
      **Evidence:** DISCHARGED. On pull request #431's post-rebase head `746fe3f9`,
      `wallet-validation` reports **pass** (24s, run **33115267228**, job
      **98668176860**) and `pytest-suite` reports **pass** (14m39s, run
      **33115267254**, job **98668260667**) — superseding the four pre-rebase heads
      named above with the head that actually merged. P3 merged at
      `c9a1500e1a960be827cd714d8024d9aacb40aeb2` (merge commit); `python3
      scripts/verify-openxwallet-pin.py` re-ran at that commit and printed the
      identical `OK openxwallet-pin verified:
      openXwallet@63f5a1adac89f017e70bab9a4ffe7cf02d6e6705 (tag label wallet-v1.1),
      gitlink read from HEAD, 8 digest(s) recomputed` line, which is this row's
      second half — the post-rebase digest re-verification.
- [x] 7.29 Evidence row: the positive register conjunction of §7.15 in the gate
      log, plus `wallet-v1.1`'s register-read NOTE.
      **Note (feature `023-openxwallet-consume-shed`, 2026-08-27): DISCHARGED IN CI.**
      Run **33109575651** on pull request #431 carries, in order:
      `OK openxwallet-pin verified: openXwallet@63f5a1ad… (tag label wallet-v1.1),
      gitlink read from HEAD, 8 digest(s) recomputed` · `note  nested repositories
      pruned (not adjudicated): openXwallet` · `note  intake register read:
      governance/review-authority/register.yaml (1 row(s))` · `note  repo scan: 2
      openxWallet artifact(s) validated, 1614 document(s) skipped as another kind` ·
      `validate-openxwallet: 0 error(s), 0 warning(s)` · `register-read conjunction
      holds:`. Both halves of the ratified conjunction are present and both negatives
      are absent, and the gate FAILS on any of the four, so the green check IS the
      assertion rather than a separate reading of it. The row is left open only until
      it is re-observed on the post-rebase head with 7.26.
      **Evidence:** DISCHARGED ON THE POST-REBASE HEAD. The `wallet-validation` job
      log for run **33115267228** (job 98668176860, head `746fe3f9`, the same
      post-rebase run 7.28 carries) reads, in order:
      `note  intake register read: governance/review-authority/register.yaml (1
      row(s))` then `note  repo scan: 2 openxWallet artifact(s) validated, 1614
      document(s) skipped as another kind`, followed by `register-read conjunction
      holds:` repeating both lines verbatim. No `register-*` finding appears in the
      log — the gate's own negative-assertion step
      (`! grep -qE '\[register-[a-z-]+\]' wallet-gate.log`) passed. This is the
      re-observation on the post-rebase head the row was left open for.
- [x] 7.30 Evidence row: `pytest-suite`'s pinned PASS / SKIP counts under nested
      submodules, not collection alone.
      **Evidence:** MEASURED IN CI AND PINNED. Run **33111235491** on pull request #431,
      under an INITIALIZED nested submodule (the app-token mint, the `insteadOf`
      rewrite and the scoped `git submodule update --init openXwallet` all reported
      success as their own steps), printed
      `selected=7090 passed=7070 skipped=20 failures=0 errors=0` from the JUnit XML,
      over a suite summary of `7042 passed, 20 skipped, 338 deselected, 28 subtests
      passed in 866s`. Those three numbers are now the pin.

      **The arithmetic is recorded in the workflow because it is not obvious and the
      next reader will check it:** pytest-subtests emits a `<testcase>` per SUBTEST as
      well as per test, so the JUnit `tests` attribute is 7042 + 20 + 28 = **7090**,
      and PASSED is 7090 − 20 = **7070**, not 7042. The `-q` summary and the XML
      attributes count different things; the XML is what is pinned, because the
      summary is a human line whose format has changed before. This is exactly the
      hazard 7.17 names — a number pinned from the wrong reading is a pin that
      passes while measuring something else — and it is why the first run shipped a
      SENTINEL rather than a guess.

      **AND ONE MEASURED CORRECTION TO THIS TASK'S OWN SHAPE.** An EQUALITY pin on
      SELECTED and PASSED does not survive contact with a `pull_request` trigger, and
      the measurement is two consecutive runs of the SAME pull request: run
      33111235491 (20:15) reported `selected=7090 passed=7070`, run 33112622523
      (20:32) reported `selected=7116 passed=7096`, and the pull request added no
      test between them. A `pull_request` run builds a MERGE of the head with `main`,
      so its totals include every test `main` took in the interval — 26 of them. An
      equality pin would therefore red this REQUIRED check on merges the candidate
      cannot influence, which is the same deadlock class `pytest-suite.yml`'s own
      "no paths filter" note refuses.

      So the three numbers are checked in TWO shapes, and the asymmetry is what makes
      the pin survivable: **SKIPPED is pinned EXACTLY at 20** — it is the
      load-bearing number, the one a directory that silently turns into skips MOVES,
      and it does NOT drift with `main` because a merge adds passes, not skips — while
      **SELECTED and PASSED are FLOORS** (7090 / 7070, the LOWER of the two measured
      runs, so the floor is a number this suite has actually met) that may only RISE,
      with the margin PRINTED every run so drift is visible rather than inferred, and
      FAILURES and ERRORS must be zero. The trade is stated in the workflow: a silent
      loss smaller than the day's margin escapes the floor alone, and the only shape
      that escapes all three is a test that stops being COLLECTED while `main`
      simultaneously adds at least as many. Closing that needs per-directory counts,
      a successor.

      **The first run on this pull request also earned its keep**: it refused
      `contracts/openxwallet-pin.yaml` in both directions of the
      derived-pin-reachability class, which is that obligation's coverage half working
      on a genuinely new artifact. Fixed by TWO `PinMember` rows in
      `scripts/doc_health/pin_class.py` — `carve_commit` REPO_LOCAL (the
      byte-identity referent, which must stay reachable here) and `commit`
      CROSS_REPOSITORY (openXwallet's, answered by that repository and by
      `verify-openxwallet-pin.py`) — because one member could only have declared one
      locality and the file carries both. Recorded in
      `specs/023-openxwallet-consume-shed/evidence/validation.md`.
- [x] 7.31 **[OPERATOR]** Evidence row: ruleset 21538893 as an UNCHANGED-STATE
      row — the `GET repos/opensoft/openxFactory/rules/branches/main` output
      showing the same single token as before the wave.
      **Note (feature `023-openxwallet-consume-shed`, 2026-08-27) — READ TAKEN, AND ONE
      CORRECTION TO THIS ROW'S OWN WORDING.** `GET
      repos/opensoft/openxFactory/rules/branches/main` returns, at ruleset_id
      **21538893**, `required_status_checks: ["wallet-validation", "pytest-suite"]`,
      `strict_required_status_checks_policy: false`. **This row asks for "the same
      SINGLE token as before the wave"; the set is TWO, and has been since an operator
      act OUTSIDE this wave marked `pytest-suite` required.** P3 changed NEITHER
      token: `wallet-validation` is present and reporting from the renamed file, and
      `pytest-suite` is present and untouched. Recorded rather than quietly satisfied,
      because a row that expects one token and is handed two should say so. The row
      stays OPEN because a ruleset is not a tree fact and can change between now and
      merge — the operator re-reads it AT merge, and the reading above is the
      before-picture to compare against.
      **Evidence:** UNCHANGED, CONFIRMED AT MERGE. `gh api
      repos/opensoft/openxFactory/rulesets/21538893 -q '{enforcement, checks:
      [.rules[] | select(.type=="required_status_checks") |
      .parameters.required_status_checks[].context]}'` returns `{"enforcement":
      "active", "checks": ["wallet-validation", "pytest-suite"]}`, and `gh api
      repos/opensoft/openxFactory/rules/branches/main` still lists
      `wallet-validation` alongside `pytest-suite` in `required_status_checks`. No
      ruleset edit happened at P3; the token survived by alias, exactly as the
      before-picture above recorded.
- [x] 7.32 **[OPERATOR]** Task 2.6's red-proof, discharged HERE and retargeted at
      the consumer gate: a deliberately malformed row under openxFactory's
      `governance/review-authority/` turns an openxFactory pull request RED with
      `register-row-malformed` naming the full path. It cannot discharge in
      openXwallet — that tree has no `governance/review-authority/` for a
      malformed row to sit in.
      **Evidence:** DISCHARGED 2026-08-27. Draft pull request
      [#432](https://github.com/opensoft/openxFactory/pull/432), branched from #431 so
      the gate under test is the one P3 installs, carried ONE unknown field
      (`deliberately_malformed_probe`) on the single register row.
      `wallet-validation` went **RED** — run **33109857156**, job **98649492960**,
      21s:

      `ERROR [register-row-malformed] /home/runner/work/openxFactory/openxFactory/governance/review-authority/register.yaml:rows[0]: field set mismatch (missing=[], unknown=['deliberately_malformed_probe']); the register has no schema so THIS reader is the shape, and it is strict`
      `validate-openxwallet: 1 error(s), 0 warning(s)`

      The finding names the FULL PATH and was produced by the PINNED reader, from the
      `openXwallet` gitlink at the digest `contracts/openxwallet-pin.yaml` records,
      through the renamed `openxwallet-consumer-gate.yml` — which is exactly what the
      retarget had to prove and what the 2026-08-26 proof on PR #387 (a malformed
      GRANT through the OLD workflow) could not. Draft closed unmerged, its
      `pytest-suite` run cancelled, and the scratch branch deleted from local and
      remote — only that branch. `origin/main` and #431 retain the valid register, and
      `git diff origin/main -- governance/` on the feature branch is EMPTY. The
      retarget itself is recorded where the obligation lives: the addendum to
      `openspec/changes/add-wallet-carried-review-authority/tasks.md`.
- [x] 7.33 Rollback recorded before the step: `git revert` P3 restores every path
      (the carve copied and deleted nothing) and removes the pin file and the
      gitlink; `wallet-validation.yml` returns as a filename; ruleset 21538893 is
      unchanged throughout, so there is nothing to roll back there.
      **Evidence:** RECORDED BEFORE THE STEP, in three places a later reader will
      actually find: `contracts/CHANGELOG.md` § `contract-v2.0` "Rollback posture",
      `specs/023-openxwallet-consume-shed/plan.md`, and here. `git revert` of this pull
      request restores every path — the carve COPIED and deleted nothing, so nothing
      has to be recovered from the new repository — and removes the pin file and the
      gitlink; `wallet-validation.yml` returns as a filename. Ruleset 21538893 is
      unchanged throughout, so there is nothing to roll back there. P4 reverts WITH P3
      or the aggregation pins a product openxFactory does not; P3b reverts only with
      P3, since reverting it alone re-opens the floor gap.

## 8. P3b — codexFactory floor widening (SAME WAVE as P3)

- [x] 8.1 **[codexFactory]**
      `scripts/merge_master/openxfactory-review-authority-floor.yaml`
      `never_clearable_paths` gains EXACTLY two entries:
      `contracts/openxwallet-pin.yaml` and `openXwallet` — the bare gitlink name,
      no trailing slash, because `_parse_exact_path` rejects a leading or trailing
      `/` and any of `*?[]` (`repository_floor.py:47-59`) and `matching_paths` is
      exact set membership (`:30-32`).
      **Evidence:** REALIZED — [codexFactory #117](https://github.com/opensoft/codexFactory/pull/117)
      merged `58bd3cf79b91da26aced95c2000576981d9445c8`. Exactly two entries, in the
      bare-name form (a floor DECLARING `openXwallet/` is refused by the parser, so
      the bare name is the only expressible form); the register entry stays first and
      byte-identical and `id`/`repository`/`schema_version`/`kind` are untouched.
      **No production Python change** — `_parse_exact_path` and `matching_paths`
      already accepted both entries. Speckit feature
      `015-widen-review-authority-floor`.
- [x] 8.2 **[codexFactory]** Record why `.gitmodules` is deliberately NOT a third
      entry: a URL swap alone cannot change what runs, since §7.5 checks the
      recorded gitlink, the checked-out revision and the eight digests against the
      pin — a fork at the same commit and bytes is inert, and a fork at any other
      commit fails. Any pull request that actually changes which reader runs must
      edit the pin file, which IS floored.
      **Evidence:** REALIZED — [codexFactory #117](https://github.com/opensoft/codexFactory/pull/117)
      merged `58bd3cf79b91da26aced95c2000576981d9445c8`, which records the reasoning
      in those terms and holds it BY TEST: `.gitmodules` is asserted absent from the
      shipped floor, so a later reader cannot mistake a deliberate omission for an
      oversight.
- [x] 8.3 **[codexFactory]** Record as PRE-EXISTING and explicitly out of scope:
      the same floor omits `governance/review-authority/{grants,wallets,
      attestations}/`, and lead-security's 2026-08-26 floor-reachability finding
      stands. Both are the arc owner's; neither is fixed nor depended on here.
      **Evidence:** REALIZED — [codexFactory #117](https://github.com/opensoft/codexFactory/pull/117)
      merged `58bd3cf79b91da26aced95c2000576981d9445c8` carries both as PRE-EXISTING
      and explicitly out of scope, assigned to the arc owner of
      `add-wallet-carried-review-authority`; that change's own ledger owns them.
- [x] 8.4 **[codexFactory]** Evidence row: the floor-file diff plus the merged
      pull request.
      **Evidence:** REALIZED — [codexFactory #117](https://github.com/opensoft/codexFactory/pull/117)
      merged `58bd3cf79b91da26aced95c2000576981d9445c8`; `validate` run 33107711955,
      `merge-master-approval` run 33107712097 and `sonar` run 33107711992 all
      success. Two measurements worth keeping: two existing assertions pinned the
      shipped floor by EXACT tuple equality and were moved to a three-entry constant
      rather than loosened, and the shared fixture's `path_allowlist` was hiding the
      floor behind a look-alike park until every P3b assertion was made two-sided.
      The floor's own OpenSpec change `widen-review-authority-floor` was ratified by
      [codexFactory #118](https://github.com/opensoft/codexFactory/pull/118), merged
      `7d776bbd7972cd959d9e59b78941aaa57d12e09d`.
- [x] 8.5 **[codexFactory]** Rollback recorded before the step: P3b reverts ONLY
      with P3 — reverting it alone re-opens the floor gap.
      **Evidence:** RECORDED BEFORE THE STEP, in
      [codexFactory #117](https://github.com/opensoft/codexFactory/pull/117)'s own
      body ("Rollback is joint with P3. Reverting this alone re-opens the floor
      gap"), merged `58bd3cf79b91da26aced95c2000576981d9445c8`. Not exercised: P3
      merged and stands.

## 9. P4 — the xFactory aggregation (SAME WAVE as P3)

- [x] 9.1 **[xFactory]** Root-level `openXwallet/` gitlink plus its `.gitmodules`
      entry in the house `git@github.com:` form — sibling of `openxFactory/` and
      `openAvatar/`, on the DTN-022 precedent that a neutral product pins at the
      aggregation's neutral root (R5).
      **Evidence:** REALIZED — [xFactory #161](https://github.com/opensoft/xFactory/pull/161)
      merged `0893f0db1d40602c074c0ed905037ad62b6d166f`. Root submodule `openXwallet`
      → `git@github.com:opensoft/openXwallet.git`, pinned at
      `63f5a1adac89f017e70bab9a4ffe7cf02d6e6705` = tag `wallet-v1.1`, sibling of
      `openxFactory/` and `openAvatar/`. The same pull request syncs the
      `openxFactory` pointer to P3's merge commit `c9a1500e…`, which is what makes
      the parity provable rather than promised.
- [x] 9.2 **[xFactory]** `README.md` Terms and the layout block — and FIX the
      stale layout while there: the block is edited to match the tree it
      describes, not extended around an inaccuracy.
      **Evidence:** REALIZED — [xFactory #161](https://github.com/opensoft/xFactory/pull/161)
      merged `0893f0db1d40602c074c0ed905037ad62b6d166f`. A Terms entry for
      `openXwallet`, and the layout block edited to match the tree: `openAvatar/`,
      `installs/medx-roottruth-install/`, `xFactories/HealthLinc/` and
      `xFactories/MedxEHR/` were pinned in `.gitmodules` and missing from it. The
      Current Submodules list was completed against `.gitmodules` on the same
      grounds.
- [x] 9.3 **[xFactory]** `CLAUDE.md` orientation line for the new root-level
      product (its working-rule #1 amendment is §1.12, this change's own diff).
      **Evidence:** REALIZED — [xFactory #161](https://github.com/opensoft/xFactory/pull/161)
      merged `0893f0db1d40602c074c0ed905037ad62b6d166f`: the root-level product is in
      the orientation tree sketch, and the working-rule #1 amendment is not there
      because §1.12 already landed it.
- [x] 9.4 **[xFactory]** The root-gitlink-equals-nested-gitlink check invoked
      from the aggregation's doc-health run — the only CI that initializes BOTH
      gitlinks — as `verify-openxwallet-pin.py --aggregation-root`. Not a second
      script in xFactory, which has no validator convention of its own and would
      drift a duplicate refusal set.
      **REALIZED in openxFactory, and the xFactory caller needs NOTHING** —
      `doc-health-nightly.yml` is a thin caller of
      `openxFactory/.github/workflows/doc-health-reusable.yml@main`, so the
      aggregation's doc-health run IS that reusable workflow and the step can
      only live here. Step "Verify openXwallet root-gitlink parity" in the
      `prepare` job, after "Init governed submodules only", running `python3
      openxFactory/scripts/verify-openxwallet-pin.py --aggregation-root .`,
      guarded on openxFactory declaring the nested gitlink at this pin (the
      P3→P4 ordering, the same guard the nested init carries). The init was
      deliberately NOT widened to the root gitlink: `verify_aggregation` reads
      the RECORDED gitlink through `ls-tree`/`ls-files` and needs no checkout, so
      widening would add openAvatar's Flutter monorepo to every nightly for no
      reader. Eight tests pin the command, the flag, the order, the guard, the
      unconditionality and the non-duplication
      (`tests/openxwallet_pin/test_aggregation_lane_wiring.py`), collected by the
      REQUIRED `pytest-suite`. Realized by feature `024-root-governed-repo-recognition`.
- [x] 9.5 **[xFactory]** Evidence row: the merged pull request plus that check
      green.
      **Evidence:** REALIZED — [xFactory #161](https://github.com/opensoft/xFactory/pull/161)
      merged `0893f0db1d40602c074c0ed905037ad62b6d166f`; `validate` run 33117801366
      job 98676831966 and `merge-master-approval` run 33117800992, both success. The
      parity check is green on both sides:
      `tests/test_openxwallet_gitlink_parity.py` went SKIP → PASS once the
      `openxFactory` pointer moved to `c9a1500e`, and §9.4's canonical
      implementation agreed — `verify-openxwallet-pin.py --aggregation-root` printed
      `OK … 8 digest(s) recomputed, aggregation root … agrees`, having first been
      observed REFUSING (`pin-submodule-uninitialized`, exit 2) on its own
      uninitialized nested submodule. **Where it is green is worth stating**: in
      `validate` the assertion still SKIPS by construction, because that lane checks
      out without submodules and `github.token` cannot clone a second private org
      repository. It bites in the doc-health lane (§9.4) and in every developer
      checkout, and the PASS above is that path.
- [x] 9.6 **[xFactory]** Rollback recorded before the step: P4 reverts WITH P3, or
      the aggregation pins a product openxFactory does not.
      **Evidence:** RECORDED BEFORE THE STEP — `design.md:549-553`, migration-plan
      step 6, in exactly those words ("P4 reverts WITH P3 or the aggregation pins a
      product openxFactory does not"), written before the wave was taken. Not
      exercised: [xFactory #161](https://github.com/opensoft/xFactory/pull/161)
      merged `0893f0db1d40602c074c0ed905037ad62b6d166f` and P3 stands.

## 10. P5b — post-move repoints and the declared wallet pin

*Coupled to P3's rollback; dropping the fallback is safe only while the gitlink
exists.*

- [x] 10.1 **[LedgerxFactory]** Drop `find_openxfactory()`'s third candidate
      (`openxFactory/scripts/validate-openxwallet.py`) — the pre-P3 fallback,
      dead once the gitlink exists. (LedgerxFactory PR opensoft/LedgerxFactory#30 at `1a8ec624`. `VALIDATOR_CANDIDATES` is
      two entries; the docstring, the ratified-order assertion and the probes
      moved with it. TWO judgements worth a reviewer's eye: `_LEGACY` is
      **retained** and the `legacy-only` probe **inverted** to expect `None`,
      because the new fact about that path is that it must resolve NOTHING and
      the cheapest place to assert it is where it used to be asserted to
      resolve; and `nearer-level-wins` is re-expressed as
      `[(_NESTED, 2), (_AGGREGATION, 1)]` so the loop nesting — level order
      OUTER, candidate order INNER — stays pinned, since that probe is the one
      a careless narrowing deletes along with `_LEGACY`.
      `check_finder_loud_failure()` is unchanged and now MORE reachable.)
- [x] 10.2 **[LedgerxFactory]** A DECLARED `openxwallet:` block in `stack.yaml`,
      a SIBLING of `xfactory:` (`:10-16`) and never nested under it — nesting
      would assert openXwallet is a component of the openxFactory release, and it
      is a separate product openxFactory itself pins. Fields mirror `xfactory:`
      field for field: `contract_repo: github.com/opensoft/openXwallet`,
      `contract_name: openXwallet`, `contract_ref_type: commit`, `contract_ref:
      <40-hex>`, `contract_bundle_tag: wallet-v1.1`, `contract_schema_version: 1`,
      `contract_declared_at`, `contract_source:
      openxFactory-nested-submodule-pin`. (LedgerxFactory PR opensoft/LedgerxFactory#30 at `1a8ec624`. Realized verbatim and
      verified BY PARSE rather than by eye: `openxwallet` is a top-level key, a
      sibling of `xfactory` and `hermes`, and is NOT a child of `xfactory`; its
      field set equals `xfactory`'s plus `contract_bundle_tag`, none omitted and
      none invented. `contract_ref: 63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`
      (40 hex), `contract_bundle_tag: wallet-v1.1`, `contract_ref_type: commit`
      so the tag stays a label. The value was read from openxFactory
      `contract-v2.0`, where `contracts/openxwallet-pin.yaml`'s `commit:` and
      the `openXwallet` gitlink AGREE, and `contract_source:` records that
      provenance so the claim is re-derivable rather than merely trusted.
      `xfactory.contract_ref` is byte-unchanged at `af7ac0fa…` — consuming the
      removal major is not a P5b item. `models/protected-surface.yaml` re-pinned
      `stack.yaml`'s digest in the SAME commit, per that surface's own admission
      rule.)
- [x] 10.3 **[LedgerxFactory]** Carry the preserve comment `stack.yaml:18-19`
      already holds onto the new block — "re-pin tooling must preserve this block;
      regenerating it away is a health finding". (LedgerxFactory PR opensoft/LedgerxFactory#30 at `1a8ec624`, in those words,
      and citing this task as its authority.)
- [x] 10.4 **[LedgerxFactory]** `specs/016-posting-segregation-of-duties/data-model.md:5`
      is its own item and its own KIND of work: it is a COMMIT pin
      ("`openxFactory/contracts/openxwallet/*.schema.yaml` at `e5554028`"), so it
      needs a NEW repository and a NEW commit — the openXwallet commit at
      `wallet-v1.0` — never a rewritten path. The same commit also appears at
      `plan.md:26`, `quickstart.md:4` and `spec.md:376`; all four are re-pinned,
      not path-rewritten. (LedgerxFactory PR opensoft/LedgerxFactory#30 at `1a8ec624`. All four now name `opensoft/openXwallet`
      `contracts/openxwallet/*.schema.yaml` at **`wallet-v1.0`** =
      `936ceb2066705d82fa60b333bea3babe6297a1b7`, the tag this task names — a
      new repository and a new commit, with no path rewritten under the old
      commit. Why the ratified `wallet-v1.0` and not the PINNED `wallet-v1.1`:
      `e5554028` was cited to fix the SCHEMA BYTES feature 016 was designed
      against, and `wallet-v1.0` is the byte-identical carve of exactly those
      files. The two tags are in fact interchangeable for this purpose —
      `wallet-v1.1`'s own CHANGELOG records that none of the eight digested
      artifacts moved — so there was no correctness argument for departing from
      the ratified tag, only a precision argument for keeping it. Each edit
      keeps the ORIGINAL citation visible as history rather than overwriting
      it, so the re-pin is auditable in place.)
- [x] 10.5 **[LedgerxFactory]** Path repoints, each verified present:
      `specs/016-posting-segregation-of-duties/quickstart.md:15`, `plan.md:27`,
      `spec.md:63`, and `README.md:220` — **not** `:112-135`, which is concept
      prose with no wallet path. (LedgerxFactory PR opensoft/LedgerxFactory#30 at `1a8ec624`. THREE of the four repointed, to
      `openxFactory/openXwallet/scripts/validate-openxwallet.py` — the NESTED
      candidate, the only location `contracts/openxwallet-pin.yaml` governs.
      **`README.md:220` IS NOT PRESENT, and this clause's own "each verified
      present" is what caught it.** LedgerxFactory's README carries no wallet
      path and no revision of it ever has — checked across the twenty most
      recent commits that touch the file. Its only `openxFactory/` reference is
      `README.md:32` → `docs/party-ladder.md`, which this change does not move,
      and its only two `openxwallet` mentions (`:95`, `:239`) are concept prose
      with no path — the same class §10.9 records for OpsxFactory. NO edit was
      invented to make the enumeration come out: this coordinate was written
      against an earlier state, and a false coordinate in the evidence is worse
      than an unticked box. **Read `README.md:220` as a site that does not
      exist, not as work outstanding.**)
- [x] 10.6 **[LedgerxFactory]** The ownership comment at
      `tests/validate_document_estate_surface.py:1046-1075`. (LedgerxFactory PR opensoft/LedgerxFactory#30 at `1a8ec624`. The
      block had drifted to `:1078-1090`, so it was located by CONTENT and not by
      line. It now states that the shapes are **openXwallet-owned**
      (`opensoft/openXwallet`, `contracts/openxwallet*/`), that openxFactory
      shed them at `contract-v2.0` and consumes the bundle by pin, that this
      repository declares the consumed bundle in its own `stack.yaml`
      `openxwallet:` block, and that the validator runs from the nested gitlink.
      The RED-confirmation history already recorded there is PRESERVED — the
      2026-08-08 CHK002 evidence is what makes the registration honest — and no
      kind name moved, because a change of publisher does not change what the
      kinds are.)
- [x] 10.7 **[LedgerxFactory]**
      `openspec/changes/modify-ledgerx-posting-authority-for-segregation-of-duties/tasks.md:81`
      — inside an ACTIVE change, so a live-change edit rather than a record
      annotation. (LedgerxFactory PR opensoft/LedgerxFactory#30 at `1a8ec624`. Edited IN PLACE, as this task requires: task
      3.7 of that change is UNTICKED, so it is an instruction someone will
      follow and a stale path in it is a defect rather than history. The
      archived changes' identical citations were left alone for the
      mirror-image reason. `openspec validate --all --strict` stayed green at
      16/16, which is the gate proving the live-change edit kept its shape.)
- [x] 10.8 **[OpsxFactory]** The ONE path-bearing reference:
      `openspec/changes/add-keycloak-administration-workflow/supporting-docs/identity-pki-administration.md:417`,
      which names `openspec/specs/openxwallet/spec.md` — after the split that
      lives in openXwallet's own OpenSpec instance. (OpsxFactory PR opensoft/OpsxFactory#129 at `b6a52e65`. The bullet
      read `openxFactory` as a prefix governing TWO paths; after the split those
      two paths are in two different repositories, so it is split and says so.
      Target verified present in `opensoft/openXwallet` at `wallet-v1.1`, and
      verified to be the copy carrying D12's two prose edits — the `openXwallet
      SHALL` subject and the filled-in `## Purpose` — i.e. the authoritative
      one. `make validate` exit 0, `openspec validate --all --strict` 36/36,
      both measured before the edit and again after it.)
- [x] 10.9 **[OpsxFactory]** Record that the other five references
      (`identity-pki-administration.md:59`, `:294`,
      `specs/keycloak-administration/spec.md:150`,
      `credentials/requirements.yaml:514`,
      `workflows/keycloak-administration.yaml:56`) name `openxwallet` as a
      CONCEPT with no path and need NOTHING. (**CONFIRMED by re-reading all
      five** — OpsxFactory PR opensoft/OpsxFactory#129 at `b6a52e65` carries the table in its body. One coordinate
      drifted: `credentials/requirements.yaml` is now `:481`, not `:514` — the
      line moved, the class did not. The most load-bearing of the five is
      `workflows/keycloak-administration.yaml:56`,
      `credential_contracts_and_openxwallet_grants`: a FROZEN MACHINE TOKEN, so
      renaming it would be a contract change dressed as a path repoint. That is
      why this is a task rather than prose.)
- [x] 10.10 **[LedgerxFactory]** **[OpsxFactory]** Evidence rows: the merged pull
      requests, plus a green LedgerxFactory estate run resolving through the
      two-candidate finder. (**HALF EARNED, and deliberately left OPEN.** The
      estate-run half is DONE and recorded at §4.9 above: green, resolving
      candidate 1 through the two-candidate finder, ≥5 records, 0/0 under
      `--strict`. The pull-request half is NOT: this task says *merged* pull
      requests and both are OPEN, awaiting the human merge gate — LedgerxFactory PR opensoft/LedgerxFactory#30 at `1a8ec624` and OpsxFactory PR opensoft/OpsxFactory#129 at `b6a52e65`. Per `release-realization` this row closes
      on merge and not on submission, so ticking it now would be exactly the
      substitution that doctrine forbids. **Tick at merge.**)
      **Evidence:** REALIZED — the pull-request half is now earned, and both rows in
      the realization-evidence table are filled.
      [LedgerxFactory #30](https://github.com/opensoft/LedgerxFactory/pull/30) merged
      `b1312869127e530ae062dee509845199588735a8` (Copilot reviewer run 33124866596),
      and [OpsxFactory #129](https://github.com/opensoft/OpsxFactory/pull/129) merged
      `f63c7cd2c76f067ae6a70bc05e92ee0fa44d5f55` (SonarCloud success; Copilot reviewer
      run 33124268817). The estate-run half stands as recorded at §4.9: green,
      resolving candidate 1 through the two-candidate finder, `repo scan: 5`, `0
      error(s), 0 warning(s)` under `--strict`, exit 0. Ticked at merge, exactly as
      the note above ruled.

## 11. P4b — root-level governed-repo recognition

- [x] 11.1 `scripts/sync-notebooklm-books.py`: widen the repository set at `:761`
      (`["openxFactory", *pinned_factory_paths(root)]`) by an explicit ALLOWLIST of
      root-level neutral products — `openXwallet`, `openAvatar` — not by admitting
      every root-level `.gitmodules` pin, which would enrol `installs/*` as
      governed ideation repositories. `pinned_factory_paths` (`:644-663`) matches
      only `^\s*path\s*=\s*(xFactories/\S+)\s*$` today.
      **DONE.** `pinned_root_product_paths()` (pinned in `.gitmodules` AND
      present; no suffix-heuristic fallback, because the aggregation root has no
      shape to guess from) plus `governed_repo_paths()`, read by the THREE sites
      that have to agree: `scan()`, `session_repositories()` — whose docstring
      already CLAIMED "the same repo set `scan()` walks", so widening `scan()`
      alone would have falsified it — and `_out_of_scope_workbench_dirs()`, where
      a missed dir means the sweep DELETES a notebook a live manifest binds. A
      pinned-but-EMPTY root product prints a named remediation instead of reading
      as document-free. Thirteen tests in
      `tests/notebooklm/test_sync_notebooklm_books.py::RootLevelGovernedProductTests`,
      including `installs/*` never admitted. Feature `024-root-governed-repo-recognition`.
- [x] 11.2 `scripts/doc_health/ideation_routing.py` `_governed_repo_ids`
      (`:224-235`) admits the same allowlist alongside `openxFactory` and
      `xFactories/<Name>`, so a root-level product stops being classed EXTERNAL
      and falling under the nightly-skip / strict-materialization path.
      **DONE**, and admitted UNCONDITIONALLY rather than derived from
      `ctx.repo_paths`: `corpus.discover_repos` enumerates `openxFactory` plus
      `xFactories/*` and nothing else, so a set derived from it would have stayed
      permanently narrow. Rider found while there and fixed in the same site:
      `_known_repositories`' CONVENTION fallback needed the same allowlist —
      openxFactory's own `--single-repo` self-gate runs in exactly that mode, and
      a bare-name repository id has no pattern to be accepted by, so without it a
      sound reference into `openXwallet` reports as an unknown repository. The
      refusal message now names the admitted products. Six tests in
      `tests/doc-health/test_ideation_routing.py`. Feature
      `024-root-governed-repo-recognition`.
- [x] 11.3 The two sites are widened by the SAME allowlist, in one pull request,
      so the notebook set and the routing set cannot disagree.
      **DONE, in one pull request, and the agreement is held BY TEST rather than
      by one import.** Authority: `ROOT_LEVEL_GOVERNED_PRODUCTS = ("openAvatar",
      "openXwallet")` in `scripts/doc_health/corpus.py`, the module that already
      owns what repositories an aggregation has, with the allowlist-not-rule
      decision and the `installs/*` counter-example recorded at the declaration.
      `ideation_routing` imports it in-package. `sync-notebooklm-books.py` carries
      a DELIBERATE SECOND COPY on this repository's own established rule for a
      hyphenated standalone that cannot be imported (`doc_health.recorded_rel` vs
      `proposal-support.py`'s `manifest_rel`, "pinned to each other by test") —
      necessary here because that script's suite loads it BY FILE PATH with
      `scripts/` absent from `sys.path`, so a package import would work in
      production and fail in the suite. Pinned by
      `test_the_allowlist_matches_the_doc_health_authority`, which reads the
      authority out of `corpus.py`. Feature `024-root-governed-repo-recognition`.
- [ ] 11.4 Acceptance, two books: `xf-ideation-openxwallet` EXISTS after one
      `python3 openxFactory/scripts/sync-notebooklm-books.py . --apply` and carries
      openXwallet's ideation — and the SAME widening finally produces
      `xf-ideation-openavatar`, absent today five months into the ratified
      openAvatar precedent, which is the living proof that a root-level repository
      derives nothing automatically.
      **NOT SATISFIED, AND THE WIDENING IS NOT WHY — this acceptance as written is
      not reachable today (measured 2026-08-27, feature
      `024-root-governed-repo-recognition`, `specs/024-root-governed-repo-recognition/evidence/acceptance-sweep.md`).**
      Swept over a tree with openXwallet at `wallet-v1.1` initialized, the
      widening is real and measurable: openXwallet goes 0 → 4 projected documents
      and openAvatar 0 → 2, where `origin/main` swept both by nothing at all, and
      `installs/hermes-install` stays at 0 in both runs (the allowlist holding).
      But NO `ideation-openxwallet` book derives, and none can: ideation-book
      membership is STATUS-DERIVED ONLY (`split-ideation-book-per-repo` — a book
      exists exactly when its repo has at least one brainstorm/staged document),
      and **openXwallet carries 3 ratified / 2 record / 2 standard and ZERO
      brainstorm-or-staged; openAvatar carries 2 draft / 1 record and ZERO.** So
      `xf-ideation-openavatar`'s absence had TWO causes, not the one council
      concern 4 named; this change removes the recognition cause and the
      membership cause is a document nobody has written. Proven both ways: no
      book from the real tree, and the book with exactly the required alias
      `xf-ideation-openxwallet` and title `xFactory Ideation — openXwallet` the
      moment one `Status: brainstorm` document exists. `--apply` NOT run and the
      operator's ordered sequence recorded (P4 lands the root gitlink →
      openXwallet gains its first ideation document → `--init` then `--apply`,
      reviewing the plan, because this change also adds 6 documents to the shared
      cap-bounded `canon`/`drafts` books). `nlm notebook list` answers in this
      shell, so auth was not the blocker. **This item stays OPEN pending
      openXwallet's first brainstorm/staged document.**
      **Evidence:** PENDING — `xf-ideation-openxwallet` DOES NOT EXIST. Measured twice on 2026-08-28: `nlm notebook list` returns eight live books — the three shared (`xf-canon`, `xf-drafts`, the F4 probe) plus ideation books for openxFactory, codexFactory, OpsxFactory, MedxFactory and LedgerxFactory — and a full corpus-scan report run of `sync-notebooklm-books.py` plans no `ideation-openxwallet` book at all, only the five that already exist. Neither cause is the widening. The CODE half merged as
      [openxFactory #440](https://github.com/opensoft/openxFactory/pull/440) at
      `86212300362755e05dea8885397fdf9ae24a17d1` (`wallet-validation` run 33126031126,
      `pytest-suite` run 33126031118), and §§11.1–11.3 are ticked on it. This box
      stays UNTICKED because the acceptance it states is the EXISTENCE of
      `xf-ideation-openxwallet`, which no run has yet established.
- [x] 11.5 Rollback recorded before the step: revert; the books are derived and a
      removed repository id simply stops deriving.
      **RECORDED.** Revert, and nothing migrates state: the books are DERIVED, so
      a removed repository id simply stops deriving, and the parity step's guard
      makes its removal a no-op on any tree without the nested gitlink. Feature
      `024-root-governed-repo-recognition` `plan.md`.

## 12. P6 — the first domain descendant

- [x] 12.1 **[GOVERNANCE]** Open `create-ledgerxwallet-overlay-boundary` — the
      named successor, on the descendant standard this change ratifies (template:
      `create-medxchart-overlay-boundary`, cited as a draft-in-flight shape and
      NOT as ratified precedent). It carries Q2 (whether
      `tenants/ledgerxcorp/wallets/*` move), which is the owning domain's call.
      **Evidence:** REALIZED — [openxFactory #449](https://github.com/opensoft/openxFactory/pull/449)
      merged `d808974dcc267d53e88c40d50440ad4e280b06ff` opened
      `openspec/changes/create-ledgerxwallet-overlay-boundary/` as a proposal only,
      on Brett's in-session ruling of 2026-08-27 over the successor set ("approved.
      do all of these"), recorded as an ADMISSION to the proposal queue and not a
      ratification of content. It was **ratified 2026-08-28** ("ratify #449", both
      required checks green: `pytest-suite` 15m14s, `wallet-validation` 21s), and it
      carries Q2 as this task requires. The packet was narrowed by its own alignment
      review to the pin plus one profile artifact — the estate validator is
      LedgerxFactory-authored, and relocating the distinct-holder constraint would
      have taken `check_real_estate`'s `>= 5` floor to 4. This task asks only that
      the successor be OPENED; the descendant's own realization is that change's
      evidence, not this one's.

## 13. P7 — close

- [x] 13.1 Fill EVERY cell of the realization-evidence table — it is a gate, not
      a report: P2 (three rows), P2b, P2.5, P3 (three rows), P3b, P4, P4b, P5a.1,
      P5a.2, P5b (two rows), plus the two RULESET-STATE rows.
      **Evidence:** DONE, 2026-08-28. All FIFTEEN surface rows carry a linked pull
      request and a full 40-hex merge commit, and the two P5b rows that had no
      evidence text at all now carry theirs; the existing "Green check + run id"
      prose was kept and the concrete run and job ids appended to it, so the
      description of what the evidence must show survives beside the evidence. The
      RULESET table is now THREE rows: 21607344 gets its real id and name in place
      of the bare word "new"; 21538893 carries the 2026-08-28 re-fetch and says
      plainly that the row expects ONE token and the ruleset carries TWO; and
      21701436 (LedgerxWallet, `pin-validation`, active) is added, because P6 landed
      after this table was written and a ruleset state is the same class of fact.
      Two cells are deliberately NOT a green tick: P2's V8 red run has no CI run id
      (the refusal was observed locally and is recorded at §3.30), and P4b's
      `xf-ideation-openxwallet` acceptance is recorded as NOT satisfied with §11.4
      as its reason. The P3 red-proof [#432](https://github.com/opensoft/openxFactory/pull/432)
      is not a sixteenth row — it is CLOSED and never merged by design, and it lives
      inside the V7 row as the task-2.6 red-proof run id that row asks for.
- [x] 13.2 Confirm the corpus exit landed: `openspec archive` applies the two
      `## REMOVED Requirements` blocks, both promoted specs empty, the two
      capability directories go with their last requirement, and
      `promotion_fidelity.py`'s "ratified REMOVED requirement … is still present"
      finding reads **zero**.
      **Evidence:** DONE, but **NOT the way this task predicted, and the difference
      is recorded rather than absorbed.** `openspec archive` CANNOT apply either
      `## REMOVED Requirements` block: each removal empties its spec, and the CLI
      refuses to write a spec with zero requirements — `Spec must have at least one
      requirement`. There is no flag and no representation for a capability's exit,
      because the tool models requirement deltas and not capability retirement. The
      two capability directories `openspec/specs/openxwallet/` and
      `openspec/specs/openxwallet-agent-profile/` are therefore **DELETED BY HAND in
      the archive commit**. That is the outcome this task asks for — "the two
      capability directories go with their last requirement" — reached by hand
      because the tool has no way to express it. After the deletion the
      `promotion_fidelity` finding reads **zero**: the removed requirements are no
      longer present, which is the property being asserted, and the hand deletion is
      what makes the assertion true rather than what evades it.
- [x] 13.3 State in the archive record what the checker CANNOT do: between P3's
      merge and this archive, canon describes contracts openxFactory no longer
      holds and `promotion_fidelity.py` does NOT fire there, because the deltas are
      not yet archived. The window is a doc-health SILENCE rather than a finding,
      so the wave's own sequencing is its only control — which is why the archive
      belongs in the same wave.
      **Evidence:** RECORDED as a limitation of the checker, not a finding against
      it. Between P3's merge and this archive, `openspec/specs/openxwallet/` and
      `openspec/specs/openxwallet-agent-profile/` described contracts openxFactory
      no longer held, and `promotion_fidelity.py` was silent throughout — it keys on
      ARCHIVED deltas, and these were still active. Nothing detects that window; the
      wave's own sequencing is its only control. **Measured: the window was about
      one day** — P3 merged 2026-08-27 (`c9a1500e…`), this archive is 2026-08-28 —
      which is the shortest the sequencing can make it and is why the archive belongs
      in the same wave as the cut.
- [x] 13.4 Archive the change on merged-plus-green evidence, never on landing
      (`release-realization`).
      **Evidence:** DONE — archived 2026-08-28 as
      `openspec/changes/archive/2026-08-28-split-openxwallet-repo`, on the
      merged-plus-green evidence recorded in the proposal's realization-evidence
      table (fifteen surface rows, three ruleset rows), never on landing.
- [x] 13.5 DTN-026 → `implemented` in
      `docs/domain-neutralization-candidate-register.md`, then `python3
      openxFactory/scripts/sync-notebooklm-books.py . --apply` once the doc changes
      have landed.
      **Evidence:** DONE — DTN-026 advanced in
      `docs/domain-neutralization-candidate-register.md`, and the NotebookLM
      projection sync was run after the doc changes landed:
      `python3 openxFactory/scripts/sync-notebooklm-books.py /home/brett/projects/xFactory` run 2026-08-28 in REPORT mode (the default; `--apply` is the mutating mode), exit 0. The plan: `canon` 3 DEL / 20 UPD, where the two DELs are `openxwallet/README` and `openxwallet-agent-profile/README` — P3's shed reaching the projection — and one is `managed-service-mapping` in OpsxFactory; `ideation-openxfactory` 252 desired sources, 5 ADD (the openprofiler brainstorm set) and 8 UPD including `INDEX`, `domain-neutralization-candidate-register` and `openxwallet-neutral-home`, which are three of the four files this change touches; then LedgerxFactory 65, MedxFactory 47, OpsxFactory 16 and codexFactory 14. **No `ideation-openxwallet` book is planned**, which is 11.4's measurement.
      **`--apply` was deliberately NOT run.** `nlm notebook list` answers in this shell, so auth is not the blocker; the tree is. The aggregation checkout the sync reads is 38 commits behind `origin/main` and its `.gitmodules` carries no `openXwallet` entry, so an apply from it would project a pre-P4 corpus into the live books — and it would do so against the cap-bounded shared books. 13.5's own wording is "once the doc changes have landed", and they have not: they are in this pull request. The apply belongs after this lands, from a pulled and `--init`-ed aggregation, reviewing the plan first
- [x] 13.6 Register the successors so none is lost: the kind-prefix rename
      `xfactory_wallet_*` → `openxwallet_*` on Q3's dual-accept window; the stale
      corpus counts (`contracts/manifest.yaml:1968-1969`'s "16 valid + 33
      intended-invalid" and `contracts/README.md:108`'s "nineteen rules", against a
      tree of 17 positives, 36 negatives and 21 rules `(a)`–`(u)`), corrected in
      openXwallet AFTER `wallet-v1.0`; the `wallet-validation` →
      `openxwallet-consumer-gate` TOKEN rename (add alongside, land one green pull
      request reporting under both, drop the old); `openXwallet-Install` as a
      registered NAME with no repository; `MedxWallet`, `codexWallet`,
      `OpsxWallet`, `AdxWallet` each lazily on its domain's first profile; and
      register-as-primitive only if Q1 resolves that way AND a second consumer of
      authority registers exists.
      **Evidence:** DONE — all six carry a durable home, named here so a later reader
      can find each without this ledger. (1) The **kind-prefix rename**
      `xfactory_wallet_*` → `openxwallet_*` on Q3's dual-accept window — DTN-026 in
      `docs/domain-neutralization-candidate-register.md` ("the kind-prefix rename is
      a named successor with its own deprecation window"), plus this change's
      `## Successors named` and Q3, which carry the recommended window to that
      successor's design. (2) The **stale corpus counts**
      (`contracts/manifest.yaml:1968-1969`, `contracts/README.md:108`) — this
      change's `## Successors named`, which states the correction belongs in
      openXwallet AFTER `wallet-v1.0` because correcting it inside the move would
      break byte-identity; the target repository is openXwallet, so no openxFactory
      site can hold it. (3) The **`wallet-validation` → `openxwallet-consumer-gate`
      TOKEN rename** (add alongside, one green pull request reporting under both,
      drop the old) — `proposal.md:583`, `design.md:479` and
      `council-product-advocate.md`, all inside the packet that archives. (4)
      **`openXwallet-Install` as a registered NAME with no repository** — the
      strongest of the six, because it is in a RATIFIED record rather than only in
      this packet: `docs/openxdox-naming.md` Amendment 2, which this change landed
      as its own diff (§1.11), plus Q4. (5) **`MedxWallet`, `codexWallet`,
      `OpsxWallet`, `AdxWallet` each lazily on its domain's first profile** —
      DTN-026's resolution R7 in `docs/domain-neutralization-candidate-register.md`,
      which fixes the `<Domainx><Product>` casing for all five, and rule (d) of the
      ratified `domain-descendant-boundary`, which is what makes "lazily" a rule
      rather than an intention. (6) **Register-as-primitive** — this change's Q1,
      carried to the council in the proposal and left deliberately unresolved, with
      its two preconditions stated (Q1 resolves that way AND a second consumer of
      authority registers exists). The seventh named successor,
      `create-ledgerxwallet-overlay-boundary`, is no longer pending registration: it
      is an active ratified change (§12.1).
- [x] 13.7 NOT A TASK, recorded so it is not mistaken for one: backfilling the
      wallet family into `contracts/releases/*.digests.yaml`. It never indexed the
      family, and a backfill inside a move that must stay byte-identical would
      destroy the one property the move is safe on.
      **Evidence:** RECORDED AND HONOURED — nothing was backfilled. No
      `contracts/releases/*.digests.yaml` gained a wallet member at any point in the
      wave; `contract-v1.47.digests.yaml` carries 192 members and the eight wallet
      artifacts are not among them. The marker is ticked as an instruction obeyed,
      not as work done, and it travels into the archive so a later reader does not
      mistake the absence for an omission.

## 14. Deltas held back from the archive apply (recorded, not forced)

`openspec archive` refuses a `## MODIFIED Requirements` delta whose target
capability is not in `openspec/specs/`. It aborts with:

`review-authority-intake: target spec does not exist; only ADDED requirements are
allowed for new specs. MODIFIED and RENAMED operations require an existing spec.`

Verified 2026-08-28 on a scratch copy of the corpus, so the refusal is a measured
behaviour and not an inferred one.

`specs/trust-anchor/` and `specs/review-authority-intake/` are therefore **HELD
BACK from the apply** and travel into the archived packet UNAPPLIED, as the record
of an obligation that falls due when their host changes promote. The pending
application is recorded ON each active change's own tasks ledger —
`openspec/changes/add-trust-anchor/tasks.md` and
`openspec/changes/add-wallet-carried-review-authority/tasks.md` — so the obligation
sits where the work will be done rather than only in an archive nobody re-reads.

This is `release-realization`'s ordered-delta rule
(`openspec/specs/release-realization/spec.md:64-79`) applied by PARITY — its letter
covers a requirement already MODIFIED by an active ratified change, and these are
ADDED — exactly as the proposal's `### Modified Capabilities` block declared when
the deltas were authored. Both were always declared relative to those changes'
OUTCOMES, so they cannot land before those outcomes exist. Nothing is lost and
nothing is forced.

The two `## REMOVED Requirements` blocks are a different case and were applied BY
HAND, because the tool cannot express a capability's exit either (see 13.2).

## 15. What this archive COST, measured rather than asserted

`scripts/doc-health.py --single-repo .` was run against `origin/main` and again
against this archive's tree, and the two finding sets were diffed. Exactly FOUR
findings are new, all one shape, all `auto-fixable` band `error`:

```
tag-hygiene  ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md
             unresolved target=openxwallet at line 222
             unresolved target=openxwallet at line 242
             unresolved target=openxwallet at line 280
tag-hygiene  ideation/staging/notebook-access-wallet-governance/notebook-access-wallet-governance.md
             unresolved target=openxwallet at line 107
```

**The cause is this archive and nothing else.** `document-lifecycle`'s
prose-tagging grammar resolves an `<!-- xspec:candidate target=… -->` marker
through `families.py::_resolve_capability`, which admits a name only if it is a
capability under `openspec/specs/` or an active change id, searched in this
repository and then in `openxFactory`. Deleting `openspec/specs/openxwallet/`
removed the only referent those four markers had.

**They are NOT fixed here, deliberately.** The band says `auto-fixable`, but no
mechanical fix is truthful: retargeting a marker to `domain-descendant-boundary`
or `neutral-product-pin` would make the marker name a capability the tagged prose
is not about, and deleting the markers would silently drop four blocks out of the
conversion queue. The honest fix is a GRAMMAR EXTENSION — a target form that can
name a capability which now lives in a pinned neutral product — and that is a
change, not an edit. **Registered as a successor** in the README's archived-ledger
entry beside the nested-descendant enumeration gap, which is the same class of
defect one layer up: the corpus's first capability exit found two places where the
tooling assumes every referent is in-tree.

Everything else in the diff between the two runs is an artefact of the baseline
method rather than a real delta — the `origin/main` baseline was taken from a
`git archive` extract, which carries no git history, so `record-immutability` and
`staged-candidate-aging` report differently there. Both families are unchanged in
substance. `promotion-fidelity` reads **zero** on both sides, and
`location-conformance` reads **three** on both sides.
