# Tasks: create-ledgerxwallet-overlay-boundary

Dependency-ordered, in `design.md`'s Migration Plan order. **Only §1 is this
change's own openxFactory work**; §3–§7 are realized as SPECKIT features in the
repositories they name — OpenSpec ratifies the boundary, Speckit builds it.
Nothing here is ticked before ratification.

**Repository tags.** Untagged = openxFactory (this packet). `[LedgerxWallet]` =
`opensoft/LedgerxWallet`, created by this change. `[LedgerxFactory]` =
`opensoft/LedgerxFactory`. `[OPERATOR]` = only Brett can perform it (a repository
creation, a ruleset, a tag, a ratification).

**Two same-commit sets, and breaking either breaks a ratified rule or a documented
gate.** §3.4+§3.5 (pin manifest + gitlink) are ONE commit — ratified rule 2.
§5 is ONE commit — the gitlink, the finder narrowing, the `stack.yaml` edit AND
its digest re-pin, and every repoint.

---

## 1. This change: the openxFactory packet

- [ ] 1.1 `proposal.md` — the five ratified rules as CONSTRAINTS; the § Why built
      on the post-P5b two-candidate finder AND the second breach site at
      `specs/016/quickstart.md:19`; what moves and the two WITHDRAWN relocations
      with their measurements; the three-way pin invariant and the three
      declarations deliberately outside it; nested-only placement with its
      visibility price; Q2 carried with its recommendation. `Status: draft`.
- [ ] 1.2 `.openspec.yaml` — `origin.kind: ad_hoc`, `reason` quoting the parent's
      § Successors named and `tasks.md` 12.1 verbatim and claiming NO staging
      origin, `approved_by` recording Brett's 2026-08-27 "approved. do all of
      these" as an ADMISSION and not a ratification.
- [ ] 1.3 `specs/ledgerxwallet-overlay-boundary/spec.md` — ONE ADDED capability,
      five requirements. Its creation gate is scoped to LedgerxWallet and CITES
      the ratified rule for the four sibling domains rather than re-legislating
      it.
- [ ] 1.4 `design.md` — D1 pin shape; D2 nested-only and its price; D3 the three
      MEASUREMENTS that narrowed the move; D4 the validator stays + D4a the
      probe MIGRATION; D5 the descendant's four-check validator; D6 three
      declarations plus the fourth read; D7 the `stack.yaml` digest re-pin; D8 the
      live-window repoint; D9 `git mv` not a carve.
- [ ] 1.5 Alignment review, two reviewers — 20 + 17 findings; every MISMATCH /
      DRIFT / GAP / OVERCLAIM applied or declined with a reason in
      `clarifications.md`. Records retained.
- [ ] 1.6 Council, three seats — Product Advocate PROCEED WITH CONSTRAINTS,
      Systems Architect PROCEED WITH CONSTRAINTS, Adversary Engineer
      RESTRUCTURE. The RESTRUCTURE was TAKEN, not argued down; §2b of the
      proposal and D3/D4 are that restructure. Records retained.
- [ ] 1.7 `clarifications.md` — the council-identified constraints, each with its
      raiser, the concern and the design impact, plus the register of findings
      MOOTED by the restructure so the record shows what was answered by
      narrowing rather than by prose.
- [ ] 1.8 `tasks.md` — this file.
- [ ] 1.9 openxFactory `README.md` — one "OpenSpec Records" active-block entry.
- [ ] 1.10 `openspec validate create-ledgerxwallet-overlay-boundary --strict` and
      `--all --strict` both green.
- [ ] 1.11 Doc-health: NO NET NEW findings, measured baseline-vs-head on the same
      `origin/main` (64 → 64). The single difference is a rule-STRING rename on a
      pre-existing `location-conformance` finding at
      `ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md`,
      because `_staged_exit_changes()` returns `sorted(...)` and
      `create-ledgerxwallet-overlay-boundary` sorts before
      `split-openxwallet-repo`. Same path, family, severity and `contested` class.
      Recorded so nobody later reads it as a regression this packet caused.
- [ ] 1.12 Proposal-only pull request. No realization in the same PR.
- [ ] 1.13 **[OPERATOR]** Ratification. Not performed by this packet.

## 2. Preconditions — all discharged, and the check recorded

- [x] 2.1 **P5b DISCHARGED.** LedgerxFactory PR #30, merge `b131286`, work commit
      `1a8ec62`, feature `019-openxwallet-consumer-repoints`: the finder narrowed
      to two candidates (`:53-78`) and `stack.yaml` gained the declared
      `openxwallet:` block (`:51-62`).
- [x] 2.2 **P3b DISCHARGED.** codexFactory PR #117, merge `58bd3cf7`,
      2026-08-27T21:53. The first draft wrongly listed it as open.
- [x] 2.3 **P4 is OPEN and does not gate P6** — the aggregation's root
      `openXwallet` gitlink is absent (`/home/brett/projects/xFactory/.gitmodules`
      pins `openAvatar` at root and no `openXwallet`), and P6 touches no
      aggregation path.
- [ ] 2.4 On the day of realization, re-verify that openxFactory's
      `contracts/openxwallet-pin.yaml` still names
      `63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`, so §3.4's commit is the one the
      domain already declares.

## 3. `[LedgerxWallet]` Create and scaffold

- [ ] 3.1 **[OPERATOR]** Create `opensoft/LedgerxWallet`, private, EMPTY — no
      template, no history import, no `filter-repo`. Verified absent 2026-08-27.
- [ ] 3.2 Scaffold `README.md` (what it may and may not contain; the pin-bump
      procedure; and D9's PROVENANCE block — origin repository, authoring change
      `modify-ledgerx-posting-authority-for-segregation-of-duties` ratified
      2026-08-08, and the LedgerxFactory commit the template came from, because a
      fresh-repo scaffold loses `git log`), `CLAUDE.md` + `AGENTS.md` per house
      style, and `docs/pin-resync-runbook.md`.
- [ ] 3.3 `.github/CODEOWNERS` — `@opensoft/xfactory` path-scoped over
      `/contracts/`, `/templates/`, `/tests/`, `/docs/` and `/.github/`.
      Path-scoped for the reason LedgerxFactory's own CODEOWNERS states: an org
      ruleset naming nobody requires nothing. `/contracts/` is the cheapest
      available human gate over which reader runs.
- [ ] 3.4 `contracts/openxwallet-pin.yaml` per D1: `schema_version: 1`,
      `kind: ledgerxwallet_openxwallet_pin`, `contract_bundle_tag: wallet-v1.1`,
      `verify_pin: tests/validate_pin.py`,
      `resync_runbook: docs/pin-resync-runbook.md`, and a `pin:` MAPPING (nested,
      following `MedxChart/contracts/openchart-pin.yaml:4-10`) holding
      `repository`, `remote`, `revision`, `revision_kind: commit`,
      `submodule_path: openXwallet`, `relationship: pinned_upstream_composition`.
      NO `source_path`; NO per-file digest block (D1 records the rejection and
      § Impact records what it costs). `revision` resolved as
      **`wallet-v1.1^{commit}`** — the tag is ANNOTATED (object `021cdeef…`,
      commit `63f5a1ad…`), and a bare `rev-parse` would write a tag object id into
      a field declared `revision_kind: commit`.
- [ ] 3.5 Nested `openXwallet` gitlink at the SAME commit, **in the SAME COMMIT as
      3.4** — ratified rule 2 is what makes the two declarations one act.
- [ ] 3.6 `tests/validate_pin.py` (D5) — FOUR checks: `git ls-tree HEAD
      openXwallet` equals the pin's `revision`; `revision` is 40 hex with no tag
      id standing in for it; the two declarations moved in the same commit; and
      **the CHECKED-OUT `openXwallet/` is at that revision and clean**
      (`git -C openXwallet rev-parse HEAD` plus `git submodule status`, where a
      leading `+` means the checkout differs from the gitlink). Fail closed with a
      named exit naming `git submodule update --init --recursive openXwallet` AND
      `docs/pin-resync-runbook.md`. Without check 4 a fork or a stale checkout at
      another commit EXECUTES while all recorded declarations agree.
- [ ] 3.7 `.github/workflows/pin-validation.yml` running 3.6 — required, because
      a ruleset cannot be promoted from EVALUATE to ACTIVE until a check has
      reported and nothing else in this change creates one.
- [ ] 3.8 **[OPERATOR]** Branch-protection ruleset in EVALUATE mode.
- [ ] 3.9 RED proof of each of 3.6's four checks: mutate the pin `revision`;
      substitute a tag id; move the gitlink without the manifest; check out
      `openXwallet` at another commit and leave it dirty.

## 4. `[LedgerxWallet]` The profile artifact moves in

- [ ] 4.1 `templates/wallet-exercise.template.yaml` — moved unchanged. Its
      `kind: ledgerx_wallet_exercise_template` and
      `instantiates: xfactory_wallet_grant_exercise` are NOT renamed (parent R2
      freezes the prefix). Its placeholder ids (`:24`, `:34`, `:38`, `:39`, `:48`)
      are NOT generalized — that is a separate act, and the spec's estate refusal
      is scoped to RECORDS so a stub showing which ids to substitute is not
      caught.
- [ ] 4.2 **NOTHING ELSE MOVES.** The distinct-holder constraint, the tenant
      estate, `tests/validate_wallet_estate.py` and
      `schemas/holder-registry.schema.yaml` all stay — D3's three measurements
      (the nested-repository prune, the `>= 5` floor, the `EXPECTED_CONSTRAINT`
      lookup) and D3a. Recorded as a task because the withdrawn version is the one
      a reader reinvents.

## 5. `[LedgerxFactory]` Nest, narrow, repoint — ONE commit

- [ ] 5.1 `.gitmodules` gains `[submodule "LedgerxWallet"] path = LedgerxWallet
      url = git@github.com:opensoft/LedgerxWallet.git`, and the gitlink. Section
      name MATCHES the path — the existing entry is `[submodule "ledgerXavatar"]`
      against `path = LedgerxAvatar`, and this change does not propagate that.
- [ ] 5.2 Delete `templates/wallet-exercise.template.yaml`.
- [ ] 5.3 `tests/validate_wallet_estate.py` — the finder narrows (D4).
      `VALIDATOR_CANDIDATES` (`:53-78`) and the five-level walk in
      `find_openxfactory()` (`:81-116`) are replaced by the single fixed relative
      path `LedgerxWallet/openXwallet/scripts/validate-openxwallet.py` resolved
      from `REPO`. `find_aggregation()` (`:560-595`) and
      `check_pin_reconciliation()` are **UNTOUCHED** — they concern the
      openxFactory BUNDLE pin, a different pin, and the parent's ratified
      `tasks.md` 6.2 makes this bar its only observer. `WALLET_DIR` (`:39`), the
      `>= 5` floor (`:721`, `:725-729`), `EXPECTED_CONSTRAINT` (`:150`,
      `:774-776`), `ENVIRONMENT_EVIDENCING`, `PLATFORM_VERIFIABLE`, `PIN_VERDICTS`
      and the wallet/grant/probe corpora are all BYTE-UNCHANGED.
- [ ] 5.3a **MIGRATE the parent's finder evidence — do not delete it** (D4a).
      `check_finder_candidates()` + `FINDER_PROBES` (`:275-331`),
      `check_finder_loud_failure()` (`:377-401`) and the constants `_NESTED`,
      `_AGGREGATION`, `_LEGACY` are the RUNNING realization evidence of the
      parent's ratified tasks 2.1-2.3 and 10.1, and the parent has NOT archived
      (its `tasks.md` 13.1: "it is a gate, not a report"). Restate them over the
      new shape: the single descendant candidate RESOLVES, and `_NESTED`,
      `_AGGREGATION` and `_LEGACY` each resolve NOTHING — retained as inverted
      probes for exactly the reason P5b retained `_LEGACY`. Keep the loud-failure
      probe's intent unchanged. Cite the parent's task ids in the code so its
      evidence table can be filled from this run rather than orphaned.
      **`FINDER_PROBES` is therefore NOT byte-unchanged**, and 5.3's list says
      which corpora are and which migrate.
- [ ] 5.3b Refusals gain the remediation string **`git submodule update --init
      --recursive LedgerxWallet`** — recursive, because the reader sits two
      gitlinks down and a non-recursive init initializes one of the two — plus the
      path of `LedgerxWallet/docs/pin-resync-runbook.md`, which
      `neutral-product-pin` requires a fail-closed refusal to name alongside the
      command.
- [ ] 5.3c The three-way agreement check (D6), plus the FOURTH read: compare
      `git ls-tree HEAD LedgerxWallet` to the descendant checkout about to be
      read, because nothing in the three declarations names WHICH descendant
      commit and a stale gitlink checkout otherwise yields a self-consistent
      GREEN.
- [ ] 5.4 `stack.yaml` — `openxwallet.contract_source` re-sourced from
      `openxFactory-nested-submodule-pin` to `LedgerxWallet-nested-submodule-pin`,
      and the block's derivation comment rewritten to name the descendant's pin.
      `contract_ref` UNCHANGED (`63f5a1ad…`). The preserve-this-block comment
      stays. The parent's design D9 specified the replaced value; D9 is a design
      decision rather than a spec requirement, so no delta is owed against
      `split-openxwallet-repo`.
- [ ] 5.5 **`models/protected-surface.yaml` DIGEST RE-PIN** (D7) — `stack.yaml` is
      digest-pinned at `:384-385`; recompute it and record a `pinned_by:` reason
      naming this change at `:386`, IN THIS COMMIT, per
      `docs/protected-surface.md:66-70`. The same entry records the cost of
      skipping (`:442-445`: red on main for seventeen days). Gate on
      `python3 tests/validate_onboarding_contracts.py`. Also amend the PROSE
      pointer at `:455` — `:455`, not the `:438` the first draft cited against a
      pre-P5b tree.
- [ ] 5.6 **THE LIVE-WINDOW REPOINT** (D8). `specs/016-posting-segregation-of-duties/runsheet.md:22-23`
      (the relative template link), `quickstart.md:19` (which invokes
      `python3 ../../openxFactory/openXwallet/scripts/validate-openxwallet.py . --strict`
      — a rule-1 breach site in its own right) and `quickstart.md:3-7` (the
      prerequisite prose naming openxFactory's checkout). The runsheet is
      `Status: prepared`, P0.4 is OPEN, phases 1-6 unexecuted, and
      `modify-ledgerx-posting-authority-for-segregation-of-duties` is still
      ACTIVE.
- [ ] 5.6a Add runsheet precondition **P0.5** naming `git submodule update --init
      --recursive LedgerxWallet` — otherwise the operator inherits a procedure
      that cannot read its own template.
- [ ] 5.7 **[OPERATOR]** Tell the window's operator that the template's path and
      the bar's prerequisite moved, BEFORE the window runs. Not a file edit, so
      its own task.
- [ ] 5.8 `tests/validate_document_estate_surface.py` — TWO amendments, not one:
      the `ledgerx_wallet_exercise_template` kind registration with its CHK002
      note (`:1116-1121`), whose artifact leaves the tree; AND the comment block
      at `:1086-1098`, which states the validator "runs from openxFactory's nested
      gitlink … see `find_openxfactory()` … Corrected at P5b". That "Corrected at
      P5b" is proof the prose is maintained and load-bearing.
- [ ] 5.9 **Reference sweep beyond feature 016.** `specs/017-openxwallet-finder/quickstart.md:36,49,97-98`
      (which imports `validate_wallet_estate` and calls
      `check_finder_candidates()`), `specs/018-openxwallet-pin-bump/rollback.md:28`
      and `specs/019-openxwallet-consumer-repoints/rollback.md:37` (rollback
      procedures for MERGED features that operate on the narrowing finder), and
      `specs/016/tasks.md:215` (the template path) plus `:91,:127` and
      `negative-confirmations.md:43`. RECORDS of performed acts keep their
      historical paths; each gains a DATED NOTE saying the finder narrowed at P6
      and what the rollback now means. State explicitly what happens to P5b's
      rollback procedure.
- [ ] 5.10 `README.md` (the feature-016 entry's paths) and `.github/CODEOWNERS`
      gains `/.gitmodules` and `/LedgerxWallet` — the cheapest available human
      gate over which reader runs, and neither is covered today (`:20-29` covers
      `/stack.yaml` and eight directories).

## 6. Evidence and close

- [ ] 6.1 **Precondition, stated because the bar is red-by-construction without
      it:** every green-run claim names the initialized checkout it depended on
      (`git submodule update --init --recursive LedgerxWallet`). In an
      uninitialized workspace the bar refuses, correctly.
- [ ] 6.2 The FULL LedgerxFactory bar green — every `tests/validate_*.py` by exit
      code, count recorded before and after so a silently dropped validator shows
      as a delta.
- [ ] 6.3 The artifact count is STILL 5 and the `>= 5` floor still passes — the
      arithmetic §4.2 exists to protect.
- [ ] 6.4 The pin-reconciliation leg still reports: the
      `PIN RECONCILIATION -- scripts/check-openxfactory-pin.py at pin …` line with
      the same verdict tier as the pre-change baseline.
- [ ] 6.5 The migrated finder probes green (5.3a), with the ratified precedence
      properties still asserted and the parent's task ids cited.
- [ ] 6.6 RED proof: with `LedgerxWallet` uninitialized, the estate validator
      REFUSES with the recursive remediation string and the runbook path, and does
      not skip.
- [ ] 6.7 RED proof: no resolvable candidate exists outside the descendant — the
      two former candidates and the pre-carve path each resolve NOTHING.
- [ ] 6.8 RED proof of the fourth read (5.3c): a stale `LedgerxWallet` checkout is
      caught rather than passing self-consistently.
- [ ] 6.9 `[openxFactory]` DTN-026's detail section notes the FIRST DESCENDANT
      EXISTS; its status advances on the register's own definition (domain re-pin
      and local-copy retirement COMPLETE), not on ratification.
- [ ] 6.10 **[OPERATOR]** Promote the LedgerxWallet ruleset to ACTIVE once
      `pin-validation` has reported; tag `lxw-v1.0`.
- [ ] 6.11 Archive only on merged plus green realization evidence per
      `release-realization`. This change declares a code surface, so it does NOT
      archive on landing.

## 7. Explicitly NOT done

- [ ] 7.1 No `xFactories/LedgerxWallet` aggregation gitlink (D2). If a later
      change takes it, the ratified rule binds both gitlinks to one commit.
- [ ] 7.2 No relocation of the estate validator, the distinct-holder constraint or
      the tenant estate. Each is a named successor with its precondition: a
      validator SPLIT for the first; a descendant-side scan pass that survives the
      nested prune plus a per-root artifact floor for the second; Q2 for the third.
- [ ] 7.3 No declared custody-posture artifact. Withdrawn — nothing would read it
      (the validator keeps its thresholds at `:141-142`, `:770-773`), and a
      repo-level posture beside per-record `custody.model` is a second declaration
      of one fact. The successor decides reader and home together, and under
      LedgerxFactory's own rules an ENFORCED posture belongs in the
      digest-protected `policies/`.
- [ ] 7.4 No change to `opensoft/openXwallet`.
- [ ] 7.5 No LedgerxFactory GitHub Actions workflow. The three-way check is
      running code in a human-run bar; the absence of a required check is a named
      successor, not an implied enforcement.
- [ ] 7.6 No `kind:` / capability-id / finding-code / filename rename (parent R2).
- [ ] 7.7 No generalization of the moved template's placeholder ids.
