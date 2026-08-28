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
- [x] 1.13 **[OPERATOR]** Ratification. **DONE 2026-08-28** — Brett Heap,
      in-session ("ratify #449") on PR #449 with both required checks green
      (`pytest-suite` 15m14s, `wallet-validation` 21s). Ratified as proposed,
      meaning the NARROWED v1; **Q2 RULED STAY**; the custody-posture cut and the
      nested-only enumeration gap both STAND. Recorded at `proposal.md`
      § Ratification record, 2026-08-28. The MERGE is the convener's own act and is
      not this packet's.

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
- [x] 2.4 On the day of realization, re-verify that openxFactory's
      `contracts/openxwallet-pin.yaml` still names
      `63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`, so §3.4's commit is the one the
      domain already declares.
      **DONE 2026-08-28.** RE-VERIFIED on the day of realization. openxFactory `origin/main` `contracts/openxwallet-pin.yaml` names `commit: "63f5a1adac89f017e70bab9a4ffe7cf02d6e6705"` and `git ls-tree origin/main openXwallet` records `160000 commit 63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`. §3.4's commit is the one the domain already declares.
## 3. `[LedgerxWallet]` Create and scaffold

- [x] 3.1 **[OPERATOR]** Create `opensoft/LedgerxWallet`, private, EMPTY — no
      template, no history import, no `filter-repo`. Verified absent 2026-08-27.
      **DONE 2026-08-28.** `opensoft/LedgerxWallet` created private and EMPTY (repo id `1349143890`), https://github.com/opensoft/LedgerxWallet. No template, no history import, no `filter-repo`. Case-variant absence re-verified immediately before creation: `LedgerxWallet`, `ledgerxwallet`, `LedgerXWallet` all resolved to no repository, and `gh search repos ledgerxwallet --owner opensoft` returned nothing.
- [x] 3.2 Scaffold `README.md` (what it may and may not contain; the pin-bump
      procedure; and D9's PROVENANCE block — origin repository, authoring change
      `modify-ledgerx-posting-authority-for-segregation-of-duties` ratified
      2026-08-08, and the LedgerxFactory commit the template came from, because a
      fresh-repo scaffold loses `git log`), `CLAUDE.md` + `AGENTS.md` per house
      style, and `docs/pin-resync-runbook.md`.
      **DONE 2026-08-28.** Commit `4a72d43`. `README.md` carries what the repository may and may not contain, the pin-bump procedure, and D9's PROVENANCE block (origin `opensoft/LedgerxFactory`; authoring change `modify-ledgerx-posting-authority-for-segregation-of-duties` ratified 2026-08-08; origin commit `b1312869127e530ae062dee509845199588735a8`; last touching commit `a46d2c22a083b4b84617caade0b00130a259735d`; blob `dda063c0e9ef62da40677b249d2ca296b17791de`, reproducible with `git hash-object` in either repository). `CLAUDE.md` + `AGENTS.md` per house style (openXwallet's shape: global protocol pointers plus repo-specific non-negotiables). `docs/pin-resync-runbook.md` distinguishes a BUMP from a DISAGREEMENT and carries a per-check repair table.
- [x] 3.3 `.github/CODEOWNERS` — `@opensoft/xfactory` path-scoped over
      `/contracts/`, `/templates/`, `/tests/`, `/docs/` and `/.github/`.
      Path-scoped for the reason LedgerxFactory's own CODEOWNERS states: an org
      ruleset naming nobody requires nothing. `/contracts/` is the cheapest
      available human gate over which reader runs.
      **DONE 2026-08-28.** Commit `bf8ccf9`. `@opensoft/xfactory` path-scoped over `/contracts/`, `/templates/`, `/tests/`, `/docs/` and `/.github/`, with the reason recorded in the file. The team was granted `maintain` on the repository in the same session, because a CODEOWNERS team WITHOUT write access is silently ignored by GitHub — which would leave the file in the names-nobody-requires-nothing state it exists to leave.
- [x] 3.4 `contracts/openxwallet-pin.yaml` per D1: `schema_version: 1`,
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
      **DONE 2026-08-28.** Commit `304cd3c`, WITH 3.5. Shape exactly as specified: `schema_version: 1`, `kind: ledgerxwallet_openxwallet_pin`, `contract_bundle_tag: wallet-v1.1`, `verify_pin: tests/validate_pin.py`, `resync_runbook: docs/pin-resync-runbook.md`, and a nested `pin:` MAPPING holding `repository`, `remote`, `revision`, `revision_kind: commit`, `submodule_path: openXwallet`, `relationship: pinned_upstream_composition`. NO `source_path`; NO per-file digest block, with the rejection and its cost recorded in the file. `revision` resolved as `wallet-v1.1^{commit}`: the tag is ANNOTATED, `rev-parse wallet-v1.1` = `021cdeefbae50127946f147c23edf98c653aa4a5` (a tag object) and `rev-parse 'wallet-v1.1^{commit}'` = `63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`, which is what the file records.
- [x] 3.5 Nested `openXwallet` gitlink at the SAME commit, **in the SAME COMMIT as
      3.4** — ratified rule 2 is what makes the two declarations one act.
      **DONE 2026-08-28.** Commit `304cd3c` — the SAME commit as 3.4, which is what makes the two declarations one act. `git show --stat 304cd3c` lists exactly `.gitmodules`, `contracts/openxwallet-pin.yaml` and `openXwallet`.
- [x] 3.6 `tests/validate_pin.py` (D5) — FOUR checks: `git ls-tree HEAD
      openXwallet` equals the pin's `revision`; `revision` is 40 hex with no tag
      id standing in for it; the two declarations moved in the same commit; and
      **the CHECKED-OUT `openXwallet/` is at that revision and clean**
      (`git -C openXwallet rev-parse HEAD` plus `git submodule status`, where a
      leading `+` means the checkout differs from the gitlink). Fail closed with a
      named exit naming `git submodule update --init --recursive openXwallet` AND
      `docs/pin-resync-runbook.md`. Without check 4 a fork or a stale checkout at
      another commit EXECUTES while all recorded declarations agree.
      **DONE 2026-08-28.** Commit `89bd9e5`. FOUR checks, each with a stable finding name: `pin-gitlink-disagrees`, `pin-not-a-commit`, `pin-split-commit`, `pin-checkout-drift`. Check 3 compares HEAD against its FIRST PARENT, so on a `pull_request` run — a merge of head with base — it reads the pull request's NET effect; a shallow clone REFUSES as unverifiable rather than passing because it could not look. Check 4 reads `git submodule status` (`-`/`+`/`U` all distinct refusals), `git -C openXwallet rev-parse HEAD`, and `git -C openXwallet status --porcelain` for cleanliness. Every refusal names `git submodule update --init --recursive openXwallet` AND `docs/pin-resync-runbook.md`. Two refusals beyond the four are carried and are not scope creep: a gitlink committed as ORDINARY FILES (a vendored copy wearing a submodule's name) and a `contract_bundle_tag` that dereferences to a commit other than `revision` (a label naming a release the pin is not).
- [x] 3.7 `.github/workflows/pin-validation.yml` running 3.6 — required, because
      a ruleset cannot be promoted from EVALUATE to ACTIVE until a check has
      reported and nothing else in this change creates one.
      **DONE 2026-08-28.** Commit `89bd9e5`. Job id `pin-validation`, NO display name, so the status check surfaces as exactly the token the ruleset pins. `fetch-depth: 0` because check 3 needs the parent commit. The private nested gitlink is reached by the house App-token pattern (`openxFactory/.github/workflows/pytest-suite.yml` and `doc-health-reusable.yml:140-158`): mint, rewrite the SSH URL with `insteadOf` BEFORE the submodule fetch, then `git submodule update --init --recursive openXwallet` by name. `github.token` is scoped to one repository and cannot clone `opensoft/openXwallet`. **This required an org-secret grant** — `XFACTORY_APP_ID` and `XFACTORY_APP_PRIVATE_KEY` are visibility-`selected`, and `opensoft/LedgerxWallet` was added to both allowlists (purely additive; the prior members `opensoft/Omnigent-Install` and `opensoft/xFactory` are untouched). VERIFIED in CI, not assumed: run `33137519688` logged `Submodule path 'openXwallet': checked out '63f5a1adac89f017e70bab9a4ffe7cf02d6e6705'` and then check 4 passing on those real bytes.
- [x] 3.8 **[OPERATOR]** Branch-protection ruleset in EVALUATE mode.
      **DONE 2026-08-28.** Ruleset **`21701436`**, `LedgerxWallet pin-gate (require pin-validation)`, created in `enforcement: evaluate` mirroring openXwallet's `21607344`: `target: branch`, `conditions.ref_name.include: ["~DEFAULT_BRANCH"]`, one `required_status_checks` rule with `strict_required_status_checks_policy: false`, `do_not_enforce_on_create: false`, context `pin-validation`, `OrganizationAdmin` bypass. NOTE for the runbook: `PATCH /repos/{o}/{r}/rulesets/{id}` returns **404**; the working promotion is `PUT` with the full ruleset body.
- [x] 3.9 RED proof of each of 3.6's four checks: mutate the pin `revision`;
      substitute a tag id; move the gitlink without the manifest; check out
      `openXwallet` at another commit and leave it dirty.
      **DONE 2026-08-28.** SIX mutations, each REFUSED with exit 1, on a scratch clone. (1) pin `revision` mutated to another well-formed 40-hex commit -> `pin-gitlink-disagrees`. (2) the ANNOTATED TAG OBJECT id `021cdeefbae50127946f147c23edf98c653aa4a5` substituted -> `pin-not-a-commit`, reporting `whose object type is 'tag' and not `commit``. (3) gitlink moved alone -> `pin-split-commit`. (4) manifest moved alone -> `pin-split-commit`, the other direction. (5) `openXwallet` checked out at `936ceb20` (`wallet-v1.0`) -> `pin-checkout-drift` via the `+` flag, the fork detector. (6) checkout at the pinned commit but DIRTY -> `pin-checkout-drift` naming the modified file. A seventh, uninitialized, also refuses rather than skipping. An all-zero revision additionally proved the YAML int-coercion path is handled: `0000…0000` parses as the integer `0`, and the non-string case refuses.
## 4. `[LedgerxWallet]` The profile artifact moves in

- [x] 4.1 `templates/wallet-exercise.template.yaml` — moved unchanged. Its
      `kind: ledgerx_wallet_exercise_template` and
      `instantiates: xfactory_wallet_grant_exercise` are NOT renamed (parent R2
      freezes the prefix). Its placeholder ids (`:24`, `:34`, `:38`, `:39`, `:48`)
      are NOT generalized — that is a separate act, and the spec's estate refusal
      is scoped to RECORDS so a stub showing which ids to substitute is not
      caught.
      **DONE 2026-08-28.** Commit `8d09311`. BYTE-IDENTICAL: `git hash-object` yields `dda063c0e9ef62da40677b249d2ca296b17791de` in both repositories, and sha256 is `7ea6703fbbe4e8c557ae75c4370599871f3793c98dc4520a0b2b6b0e3a7b633a`. `kind: ledgerx_wallet_exercise_template` and `instantiates: xfactory_wallet_grant_exercise` unchanged; placeholder ids unchanged.
- [x] 4.2 **NOTHING ELSE MOVES.** The distinct-holder constraint, the tenant
      estate, `tests/validate_wallet_estate.py` and
      `schemas/holder-registry.schema.yaml` all stay — D3's three measurements
      (the nested-repository prune, the `>= 5` floor, the `EXPECTED_CONSTRAINT`
      lookup) and D3a. Recorded as a task because the withdrawn version is the one
      a reader reinvents.
      **DONE 2026-08-28.** HELD. `tenants/ledgerxcorp/wallets/*`, `schemas/holder-registry.schema.yaml`, the distinct-holder constraint and `tests/validate_wallet_estate.py` are all still in LedgerxFactory, and PR #31 moves none of them. The arithmetic §4.2 protects is measured at 6.3 below.
## 5. `[LedgerxFactory]` Nest, narrow, repoint — ONE commit

- [x] 5.1 `.gitmodules` gains `[submodule "LedgerxWallet"] path = LedgerxWallet
      url = git@github.com:opensoft/LedgerxWallet.git`, and the gitlink. Section
      name MATCHES the path — the existing entry is `[submodule "ledgerXavatar"]`
      against `path = LedgerxAvatar`, and this change does not propagate that.
      **DONE 2026-08-28.** LedgerxFactory PR **#31**, commit `2c96b0b`, feature `020-ledgerxwallet-descendant-nest`. `[submodule "LedgerxWallet"]` with `path = LedgerxWallet` — the section name MATCHES the path, and the existing `[submodule "ledgerXavatar"]` against `path = LedgerxAvatar` is NOT propagated. Gitlink at `0a0141cafc1fecd5d0e38b14e4f40a67a54a08d3`.
- [x] 5.2 Delete `templates/wallet-exercise.template.yaml`.
      **DONE 2026-08-28.** Deleted in `2c96b0b`. `git diff --cached --stat` shows the file at -52 lines in the same commit that adds the gitlink.
- [x] 5.3 `tests/validate_wallet_estate.py` — the finder narrows (D4).
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
      **DONE 2026-08-28.** `VALIDATOR_CANDIDATES` and the five-level walk in `find_openxfactory()` are GONE, replaced by `_DESCENDANT = "LedgerxWallet/openXwallet/scripts/validate-openxwallet.py"` resolved from `REPO` with no walk. `find_aggregation()` and `check_pin_reconciliation()` are UNTOUCHED. `WALLET_DIR`, the `>= 5` floor, `EXPECTED_CONSTRAINT`, `ENVIRONMENT_EVIDENCING`, `PLATFORM_VERIFIABLE`, `PIN_VERDICTS` and the wallet/grant/probe corpora are byte-unchanged.
- [x] 5.3a **MIGRATE the parent's finder evidence — do not delete it** (D4a).
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
      **DONE 2026-08-28.** MIGRATED, not deleted. `check_finder_candidates()`, `check_finder_loud_failure()` and `_NESTED`/`_AGGREGATION`/`_LEGACY` all survive; the parent's task ids 2.1-2.3 and 10.1 are cited in the code so its evidence table can be filled from this run. The probe set is now NINE: the descendant RESOLVES; `_NESTED`, `_AGGREGATION` and `_LEGACY` each resolve NOTHING alone and in every combination; and one NEW probe, `descendant-outside-the-repo-resolves-nothing`, asserts the same relative path ONE LEVEL UP resolves nothing — the single assertion that distinguishes a fixed path from a search, which no probe in the parent's set could make. The loud-failure probe's intent is unchanged.
- [x] 5.3b Refusals gain the remediation string **`git submodule update --init
      --recursive LedgerxWallet`** — recursive, because the reader sits two
      gitlinks down and a non-recursive init initializes one of the two — plus the
      path of `LedgerxWallet/docs/pin-resync-runbook.md`, which
      `neutral-product-pin` requires a fail-closed refusal to name alongside the
      command.
      **DONE 2026-08-28.** `INIT_DESCENDANT` and `DESCENDANT_RUNBOOK` are module constants, spelled once so the strings cannot drift and spelled IDENTICALLY to the descendant's own refusals. Both appear in every refusal this change adds, RED-proven at 6.6.
- [x] 5.3c The three-way agreement check (D6), plus the FOURTH read: compare
      `git ls-tree HEAD LedgerxWallet` to the descendant checkout about to be
      read, because nothing in the three declarations names WHICH descendant
      commit and a stale gitlink checkout otherwise yields a self-consistent
      GREEN.
      **DONE 2026-08-28.** `check_descendant_pin_agreement()`, called from `main()` between `check_pin_reconciliation()` and `check_real_estate()`. The FOURTH READ runs FIRST — `git ls-tree HEAD LedgerxWallet` against `git submodule status` and the descendant's own HEAD — because everything after it reads that checkout. Green line: `DESCENDANT PIN -- openXwallet 63f5a1adac89 agrees across LedgerxWallet's gitlink, LedgerxWallet's pin manifest and stack.yaml; LedgerxWallet itself at 0a0141cafc1f as recorded`.
- [x] 5.4 `stack.yaml` — `openxwallet.contract_source` re-sourced from
      `openxFactory-nested-submodule-pin` to `LedgerxWallet-nested-submodule-pin`,
      and the block's derivation comment rewritten to name the descendant's pin.
      `contract_ref` UNCHANGED (`63f5a1ad…`). The preserve-this-block comment
      stays. The parent's design D9 specified the replaced value; D9 is a design
      decision rather than a spec requirement, so no delta is owed against
      `split-openxwallet-repo`.
      **DONE 2026-08-28.** `contract_source: openxFactory-nested-submodule-pin` -> `LedgerxWallet-nested-submodule-pin`; the derivation comment rewritten to name the descendant's pin, to say the VALUE is unchanged on purpose, and to record that openxFactory may now advance its pin independently without that being an error. `contract_ref` UNCHANGED at `63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`. The preserve-this-block managed-provenance comment is byte-unchanged.
- [x] 5.5 **`models/protected-surface.yaml` DIGEST RE-PIN** (D7) — `stack.yaml` is
      digest-pinned at `:384-385`; recompute it and record a `pinned_by:` reason
      naming this change at `:386`, IN THIS COMMIT, per
      `docs/protected-surface.md:66-70`. The same entry records the cost of
      skipping (`:442-445`: red on main for seventeen days). Gate on
      `python3 tests/validate_onboarding_contracts.py`. Also amend the PROSE
      pointer at `:455` — `:455`, not the `:438` the first draft cited against a
      pre-P5b tree.
      **DONE 2026-08-28.** DIGEST RE-PINNED IN THE SAME COMMIT: `5f589a7d095aedba85f41ad07d16158b665090e21cbe6a8147280eba39a4b8bc` -> `5cb73a02b81401771c2b39776134b3f68c7520196591a233c538d3d7c904f816`, with a `pinned_by:` reason naming this change, the feature and exactly what moved, and retaining the previous entry's full text. Gated: `python3 tests/validate_onboarding_contracts.py` exits 0. The PROSE pointer was amended at its actual line (`:455` in the pre-change file, inside the same folded block) with a dated note that the validator no longer walks up into a neighbouring checkout.
- [x] 5.6 **THE LIVE-WINDOW REPOINT** (D8). `specs/016-posting-segregation-of-duties/runsheet.md:22-23`
      (the relative template link), `quickstart.md:19` (which invokes
      `python3 ../../openxFactory/openXwallet/scripts/validate-openxwallet.py . --strict`
      — a rule-1 breach site in its own right) and `quickstart.md:3-7` (the
      prerequisite prose naming openxFactory's checkout). The runsheet is
      `Status: prepared`, P0.4 is OPEN, phases 1-6 unexecuted, and
      `modify-ledgerx-posting-authority-for-segregation-of-duties` is still
      ACTIVE.
      **DONE 2026-08-28.** All three sites repointed IN THE SAME COMMIT. `runsheet.md:22-23` -> `../../LedgerxWallet/templates/wallet-exercise.template.yaml`. `quickstart.md:19` -> `python3 LedgerxWallet/openXwallet/scripts/validate-openxwallet.py . --strict`, with the old line quoted beneath it and named as a rule-1 breach rather than a stale path, and the scan target held at `.` with the register-reader reason. `quickstart.md:3-7` prerequisite prose rewritten to the descendant. LINKS AND PREREQUISITES ONLY: no step, actor, abort condition or evidence requirement touched.
- [x] 5.6a Add runsheet precondition **P0.5** naming `git submodule update --init
      --recursive LedgerxWallet` — otherwise the operator inherits a procedure
      that cannot read its own template.
      **DONE 2026-08-28.** **P0.5** added after P0.4, naming `git submodule update --init --recursive LedgerxWallet` with the recursion explained, the runbook path, and an explicit statement that it ADDS NO ACTOR AND NO ABORT CONDITION to any step below.
- [ ] 5.7 **[OPERATOR]** Tell the window's operator that the template's path and
      the bar's prerequisite moved, BEFORE the window runs. Not a file edit, so
      its own task.
      **STILL OPEN 2026-08-28 — needs Brett.** Not performed by this realization: it is a communication to the live window's operator, not a file edit, and the runsheet's new P0.5 does not substitute for it. The operator must be told that the exercise-record template now lives at `LedgerxWallet/templates/wallet-exercise.template.yaml` and that the quickstart bar's prerequisite is now `git submodule update --init --recursive LedgerxWallet` rather than a workspace-root openxFactory checkout — BEFORE the window runs. The window is still `Status: prepared` with P0.4 open and phases 1-6 unexecuted, so there is time; that is a reason to send it now, not later.
- [x] 5.8 `tests/validate_document_estate_surface.py` — TWO amendments, not one:
      the `ledgerx_wallet_exercise_template` kind registration with its CHK002
      note (`:1116-1121`), whose artifact leaves the tree; AND the comment block
      at `:1086-1098`, which states the validator "runs from openxFactory's nested
      gitlink … see `find_openxfactory()` … Corrected at P5b". That "Corrected at
      P5b" is proof the prose is maintained and load-bearing.
      **DONE 2026-08-28.** BOTH amendments. The `ledgerx_wallet_exercise_template` registration STAYS, with the reason MEASURED rather than asserted: the surface adjudicates the feature WARRANT (baseline diff plus the owned paths in `specs/001-document-estate-read/warrant.yaml`), no warrant entry names `LedgerxWallet/` or the template's old path, and the kind is a machine key R2 freezes. An earlier draft of this comment claimed the scan reaches inside the gitlink; that was checked, found FALSE, and corrected — the comment now states explicitly that nothing here reads inside the gitlink. The `:1086-1098` resolution-path comment is repointed, keeping its "Corrected at P5b" line as the proof the prose is maintained.
- [x] 5.9 **Reference sweep beyond feature 016.** `specs/017-openxwallet-finder/quickstart.md:36,49,97-98`
      (which imports `validate_wallet_estate` and calls
      `check_finder_candidates()`), `specs/018-openxwallet-pin-bump/rollback.md:28`
      and `specs/019-openxwallet-consumer-repoints/rollback.md:37` (rollback
      procedures for MERGED features that operate on the narrowing finder), and
      `specs/016/tasks.md:215` (the template path) plus `:91,:127` and
      `negative-confirmations.md:43`. RECORDS of performed acts keep their
      historical paths; each gains a DATED NOTE saying the finder narrowed at P6
      and what the rollback now means. State explicitly what happens to P5b's
      rollback procedure.
      **DONE 2026-08-28.** DATED NOTES added to `specs/017-openxwallet-finder/quickstart.md`, `specs/017-openxwallet-finder/spec.md`, `specs/018-openxwallet-pin-bump/rollback.md`, `specs/019-openxwallet-consumer-repoints/rollback.md` and `specs/019-openxwallet-consumer-repoints/spec.md`. Historical paths are KEPT — they are records of performed acts. **What happens to P5b's rollback procedure, stated explicitly:** it is SUPERSEDED, not merely stale — reverting it would restore a candidate tuple that no longer exists in the file. The live rollback for the finder is P6's own, a reverse of feature 020's single commit, taken as one act for the same reason the change was.
- [x] 5.10 `README.md` (the feature-016 entry's paths) and `.github/CODEOWNERS`
      gains `/.gitmodules` and `/LedgerxWallet` — the cheapest available human
      gate over which reader runs, and neither is covered today (`:20-29` covers
      `/stack.yaml` and eight directories).
      **DONE 2026-08-28.** `README.md`'s feature-016 entry repointed and given the recursive-init warning. `.github/CODEOWNERS` gains `/.gitmodules` and `/LedgerxWallet` under `@opensoft/xfactory`, with the reason recorded: LedgerxFactory has no workflow, so a code-owner review is the cheapest available human gate over which reader runs.
## 6. Evidence and close

- [x] 6.1 **Precondition, stated because the bar is red-by-construction without
      it:** every green-run claim names the initialized checkout it depended on
      (`git submodule update --init --recursive LedgerxWallet`). In an
      uninitialized workspace the bar refuses, correctly.
      **DONE 2026-08-28.** STATED on every claim below: `git submodule update --init --recursive LedgerxWallet`, then `git submodule status` reporting ` 0a0141cafc1f… LedgerxWallet (heads/main)` and ` 63f5a1adac89… openXwallet (wallet-v1.1)` — both leading-space, neither `-` nor `+`. The uninitialized case is 6.6.
- [x] 6.2 The FULL LedgerxFactory bar green — every `tests/validate_*.py` by exit
      code, count recorded before and after so a silently dropped validator shows
      as a delta.
      **DONE 2026-08-28.** **17 PASS / 0 FAIL**, every `tests/validate_*.py` by exit code. Count **17 before and 17 after**, so no validator was silently dropped.
- [x] 6.3 The artifact count is STILL 5 and the `>= 5` floor still passes — the
      arithmetic §4.2 exists to protect.
      **DONE 2026-08-28.** `note  repo scan: 5 openxWallet artifact(s) validated, 601 document(s) skipped as another kind` — STILL 5, and the `>= 5` floor passes. This is the arithmetic §4.2 exists to protect, measured rather than assumed.
- [x] 6.4 The pin-reconciliation leg still reports: the
      `PIN RECONCILIATION -- scripts/check-openxfactory-pin.py at pin …` line with
      the same verdict tier as the pre-change baseline.
      **DONE 2026-08-28.** `PIN RECONCILIATION -- scripts/check-openxfactory-pin.py at pin af7ac0fa4d31, aggregation /home/brett/projects/xFactory (exit 1):` — same line shape and the SAME verdict tier (the `ERROR: stack pin … is not an ancestor of the aggregation submodule pointer` leg, plus the 8-row relocation notice) as the pre-change baseline. Reported, never enforced, exactly as before.
- [x] 6.5 The migrated finder probes green (5.3a), with the ratified precedence
      properties still asserted and the parent's task ids cited.
      **DONE 2026-08-28.** All NINE migrated probes green, run individually and named. RED-PROVEN TO BITE rather than merely to pass: restoring an upward walk over the two former candidates raises **5** probe errors, including `finder probe nested-resolves-nothing: expected None, got '…'`. The ratified precedence properties survive as the stronger claim that nothing outside the descendant resolves at all, and the parent's task ids are cited in the code.
- [x] 6.6 RED proof: with `LedgerxWallet` uninitialized, the estate validator
      REFUSES with the recursive remediation string and the runbook path, and does
      not skip.
      **DONE 2026-08-28.** RED-PROVEN. With `LedgerxWallet` deinitialized, `validate_wallet_estate.py` exits **1** with `WALLET ESTATE: 1 error(s)` and the message `the pinned openxWallet reader was not found at LedgerxWallet/openXwallet/scripts/validate-openxwallet.py; the wallet bar CANNOT run and that is a failure, not a skip … Remedy: `git submodule update --init --recursive LedgerxWallet` … the repair is in `LedgerxWallet/docs/pin-resync-runbook.md``. It does not skip.
- [x] 6.7 RED proof: no resolvable candidate exists outside the descendant — the
      two former candidates and the pre-carve path each resolve NOTHING.
      **DONE 2026-08-28.** RED-PROVEN on scratch trees. `openxFactory/openXwallet/scripts/validate-openxwallet.py` -> `None`; `openXwallet/scripts/validate-openxwallet.py` -> `None`; `openxFactory/scripts/validate-openxwallet.py` -> `None`. Alone, pairwise, and all three together.
- [x] 6.8 RED proof of the fourth read (5.3c): a stale `LedgerxWallet` checkout is
      caught rather than passing self-consistently.
      **DONE 2026-08-28.** RED-PROVEN. With `LedgerxWallet/` checked out at `4a72d43` while the repository records `0a0141ca`, the bar exits 1: `LedgerxWallet/ is checked out at a DIFFERENT commit than this repository records … so the three declarations could agree with one another about a tree this repository does not pin -- a self-consistent GREEN against the wrong descendant`. Caught by the FOURTH READ, before any of the three declarations is compared.
- [x] 6.9 `[openxFactory]` DTN-026's detail section notes the FIRST DESCENDANT
      EXISTS; its status advances on the register's own definition (domain re-pin
      and local-copy retirement COMPLETE), not on ratification.
      **DONE 2026-08-28.** DTN-026's detail section records **THE FIRST DESCENDANT EXISTS, 2026-08-28**, with the realization enumerated, and states explicitly that the STATUS DOES NOT ADVANCE on it: the register's own definition requires the domain re-pin and the local-copy retirement to be COMPLETE, and the re-pin is open as PR #31 while P4 has not landed. The summary row is updated to match, and the nested-only enumeration gap is recorded there as a registered successor covering all three nested descendants.
- [ ] 6.10 **[OPERATOR]** Promote the LedgerxWallet ruleset to ACTIVE once
      `pin-validation` has reported; tag `lxw-v1.0`.
      **HALF DONE 2026-08-28.** The PROMOTION is done: `pin-validation` reported on LedgerxWallet PR #1 (run `33137519688`, 14s, green), that PR merged, and ruleset `21701436` was promoted to `enforcement: active`. Evidence captured: `GET repos/opensoft/LedgerxWallet/rules/branches/main` returns a `required_status_checks` rule with `"context": "pin-validation"` and `"ruleset_id": 21701436`, alongside the two org rulesets. **The TAG `lxw-v1.0` is NOT cut** — it is an `[OPERATOR]` act that was not among the ones authorized for this realization, and it is left for Brett.
- [ ] 6.11 Archive only on merged plus green realization evidence per
      `release-realization`. This change declares a code surface, so it does NOT
      archive on landing.
      **NOT MET, correctly.** This change declares a code surface, so it does not archive on landing. Two gates remain: LedgerxFactory PR #31 is OPEN rather than merged, and 5.7 and the `lxw-v1.0` half of 6.10 are unperformed. The LedgerxWallet side IS merged and green.
## 7. Explicitly NOT done

- [x] 7.1 No `xFactories/LedgerxWallet` aggregation gitlink (D2). If a later
      change takes it, the ratified rule binds both gitlinks to one commit.
      **CONFIRMED HELD 2026-08-28.** `/home/brett/projects/xFactory/.gitmodules` is UNTOUCHED by this realization and declares no `xFactories/LedgerxWallet`. The aggregation was not opened.
- [x] 7.2 No relocation of the estate validator, the distinct-holder constraint or
      the tenant estate. Each is a named successor with its precondition: a
      validator SPLIT for the first; a descendant-side scan pass that survives the
      nested prune plus a per-root artifact floor for the second; Q2 for the third.
      **CONFIRMED HELD 2026-08-28.** PR #31 moves none of the three: `tests/validate_wallet_estate.py` stays (only its RESOLUTION changed), the distinct-holder constraint and `tenants/ledgerxcorp/wallets/*` stay, and `schemas/holder-registry.schema.yaml` stays. Measured at 6.3: the artifact count is still 5.
- [x] 7.3 No declared custody-posture artifact. Withdrawn — nothing would read it
      (the validator keeps its thresholds at `:141-142`, `:770-773`), and a
      repo-level posture beside per-record `custody.model` is a second declaration
      of one fact. The successor decides reader and home together, and under
      LedgerxFactory's own rules an ENFORCED posture belongs in the
      digest-protected `policies/`.
      **CONFIRMED HELD 2026-08-28.** LedgerxWallet carries no custody-posture artifact and no `policies/` directory.
- [x] 7.4 No change to `opensoft/openXwallet`.
      **CONFIRMED HELD 2026-08-28.** `opensoft/openXwallet` received no commit, no branch, no tag and no ruleset change. It is CONSUMED at `wallet-v1.1` through two read-only nested checkouts.
- [x] 7.5 No LedgerxFactory GitHub Actions workflow. The three-way check is
      running code in a human-run bar; the absence of a required check is a named
      successor, not an implied enforcement.
      **CONFIRMED HELD 2026-08-28.** LedgerxFactory `origin/main` carries no `.github/workflows/` at all (only `CODEOWNERS` and `copilot-instructions.md`), and PR #31 adds none. The three-way check is running code in a human-run bar; the absence of a required check remains a named successor.
- [x] 7.6 No `kind:` / capability-id / finding-code / filename rename (parent R2).
      **CONFIRMED HELD 2026-08-28.** `kind: ledgerx_wallet_exercise_template` and `instantiates: xfactory_wallet_grant_exercise` are byte-identical after the move; the filename is unchanged; the `ledgerx_wallet_exercise_template` registry row is retained rather than removed; `find_openxfactory()` KEEPS its historical name even though it now reaches neither openxFactory nor a candidate list, because renaming it is a separate act.
- [x] 7.7 No generalization of the moved template's placeholder ids.
      **CONFIRMED HELD 2026-08-28.** Blob `dda063c0e9ef62da40677b249d2ca296b17791de` in both repositories: the placeholder ids at `:24`, `:34`, `:38`, `:39` and `:48` are byte-identical.
