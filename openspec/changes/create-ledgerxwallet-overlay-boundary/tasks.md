# Tasks: create-ledgerxwallet-overlay-boundary

Dependency-ordered, in `design.md`'s Migration Plan order. **Only §1 is this
change's own openxFactory work**; §2–§7 are realized as SPECKIT features in the
repositories they name — per the convener's standing correction that OpenSpec
ratifies the boundary and Speckit builds it. Nothing here is ticked before
ratification.

**Repository tags.** Untagged = openxFactory (this packet). `[LedgerxWallet]` =
`opensoft/LedgerxWallet`, the repository this change creates. `[LedgerxFactory]`
= `opensoft/LedgerxFactory`. `[OPERATOR]` = only Brett can perform it (a
repository creation, a ruleset, a tag, a ratification). `[GOVERNANCE]` = it needs
a ruling or an OpenSpec change before the work is legal.

**Preconditions, both stated as tasks because neither is enforceable by a
checker.** P5b is DISCHARGED (§2.0). The feature-016 live window is NOT, and
§5.6 is the guard.

**The pin is ONE act.** §3.4 and §3.5 land in the SAME commit or the ratified
same-commit rule is broken; §4.2 and §4.3 likewise.

---

## 1. This change: the openxFactory packet

- [ ] 1.1 `proposal.md` — the five ratified rules carried as CONSTRAINTS rather
      than questions; the § Why built on the post-P5b two-candidate finder; the
      MOVES/STAYS table with a reason per row; the delegating bar entry; the
      three-way pin invariant; nested-only placement with its governance-
      visibility price named; Q2 carried with its recommendation. `Status: draft`.
- [ ] 1.2 `.openspec.yaml` — `origin.kind: ad_hoc`, id
      `openxFactory:adhoc:2026-08-27-create-ledgerxwallet-overlay-boundary`,
      `reason` quoting the parent's § Successors named and `tasks.md` 12.1
      verbatim and claiming NO staging origin, `approved_by` recording Brett's
      2026-08-27 "approved. do all of these" as an ADMISSION and not a
      ratification, `approved_on: 2026-08-27`.
- [ ] 1.3 `specs/ledgerxwallet-overlay-boundary/spec.md` — ONE ADDED capability,
      five requirements: the pin declared twice in one commit; the descendant as
      the sole consumption path with the three-way agreement; profile-not-estate-
      not-fork; coverage-survives-the-move with the declared estate root; lazy
      creation binding the four sibling names.
- [ ] 1.4 `design.md` — D1 pin shape (MedxChart's, not MedxAvatar's; the
      annotated-tag dereference); D2 nested-only and its price; D3 the
      profile/instance TEST plus D3a the one named seam exception; D4 the
      delegating bar entry; D5 one candidate and a declared estate root; D6 the
      expected set; D7 three declarations and what actually checks them; D8
      custody posture as NEW; D9 the prepared-window repoint; D10 `git mv` not a
      carve.
- [ ] 1.5 Alignment review, two reviewers (QA lead, stack architect); every
      MISMATCH / DRIFT / GAP / OVERCLAIM applied or explicitly declined with a
      reason. Records retained in the packet.
- [ ] 1.6 Council, three seats (product advocate, systems architect, adversary
      engineer); the adversary tasked at LS-A3-class claims and pin skew. All
      verdicts dispositioned; NOTED-class constraints carried into
      `clarifications.md`. Records retained.
- [ ] 1.7 `clarifications.md` — the council-identified constraints, each with its
      raiser, the concern, and the design impact.
- [ ] 1.8 `tasks.md` — this file.
- [ ] 1.9 openxFactory `README.md` — one entry in the "OpenSpec Records" active
      block, naming the ADDED capability, the MOVES/STAYS split, Q2's
      recommendation, the review and council tallies, and the fact that
      `domain-descendant-boundary` is RATIFIED-IN-CHANGE and not yet promoted.
- [ ] 1.10 `OPENSPEC_TELEMETRY=0 openspec validate create-ledgerxwallet-overlay-boundary --strict`
      and `--all --strict` both green.
- [ ] 1.11 Doc-health: NO NET NEW findings. Measured baseline-vs-head on the same
      `origin/main` (64 → 64). The single difference is a rule-STRING rename on
      one pre-existing `location-conformance` finding at
      `ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md`,
      because `_staged_exit_changes()` returns `sorted(...)` and
      `create-ledgerxwallet-overlay-boundary` sorts before `split-openxwallet-repo`.
      Same path, family, severity and `contested` class. Recorded here so nobody
      later reads it as a regression this packet caused.
- [ ] 1.12 Proposal-only pull request against `opensoft/openxFactory` `main`. No
      realization in the same PR.
- [ ] 1.13 **[OPERATOR]** Ratification. Not performed by this packet.

## 2. Preconditions

- [x] 2.0 **P5b DISCHARGED.** LedgerxFactory PR #30, merge `b131286`, work commit
      `1a8ec62`, Speckit feature `019-openxwallet-consumer-repoints`, 2026-08-27:
      the finder narrowed to two candidates (`tests/validate_wallet_estate.py:53-78`)
      and `stack.yaml` gained the declared sibling `openxwallet:` block
      (`:51-62`) at `contract_ref: 63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`,
      `contract_source: openxFactory-nested-submodule-pin`.
- [ ] 2.1 Confirm NOTHING ELSE gates P6, and record the check: P4 (the
      aggregation's root `openXwallet` gitlink) is open and P6 touches no
      aggregation path; P3b (codexFactory's merge-gate floor) is codexFactory's
      and P6 touches no codexFactory path; the operator's openXwallet tag is
      already cut (`wallet-v1.1`).
- [ ] 2.2 Re-verify on the day of realization that
      `contracts/openxwallet-pin.yaml` in openxFactory still names
      `63f5a1ad…`, so §3.4's commit is the one the domain already declares.

## 3. `[LedgerxWallet]` Create and scaffold

- [ ] 3.1 **[OPERATOR]** Create `opensoft/LedgerxWallet`, private, EMPTY — no
      template, no history import, no `filter-repo`. Verified absent
      2026-08-27 (`gh repo view opensoft/LedgerxWallet` → "Could not resolve to a
      Repository").
- [ ] 3.2 **[OPERATOR]** Create the branch-protection ruleset in EVALUATE mode.
      Promotion to ACTIVE is §6.1, after a check has reported once.
- [ ] 3.3 Scaffold: `README.md`, `CLAUDE.md` + `AGENTS.md` pointing at the
      user-global protocol per house style, `.github/CODEOWNERS` naming
      `@opensoft/xfactory` path-scoped over `/contracts/`, `/profile/`, `/tests/`
      and `/.github/` — path-scoped for the reason LedgerxFactory's own CODEOWNERS
      states, that an org ruleset naming nobody requires nothing.
- [ ] 3.4 `contracts/openxwallet-pin.yaml` per D1: `schema_version: 1`,
      `kind: ledgerxwallet_openxwallet_pin`, `repository: opensoft/openXwallet`,
      `remote`, `revision` resolved as **`wallet-v1.1^{commit}`** (the tag is
      ANNOTATED — tag object `021cdeef…`, commit `63f5a1ad…`; a bare `rev-parse`
      would write a tag id into a `revision_kind: commit` field),
      `revision_kind: commit`, `contract_bundle_tag: wallet-v1.1`,
      `submodule_path: openXwallet`,
      `relationship: pinned_upstream_composition`. NO `source_path`, NO per-file
      digest block (D1's rejected alternative, recorded there).
- [ ] 3.5 Nested `openXwallet` submodule gitlink at the SAME commit, **in the
      SAME COMMIT as 3.4** — the ratified same-commit rule is what makes the two
      declarations one act.
- [ ] 3.6 `README.md` provenance block per D10: the origin repository, the
      authoring change
      (`modify-ledgerx-posting-authority-for-segregation-of-duties`, ratified
      2026-08-08 by Brett Heap), the Speckit features that amended each moved file
      (016, 017, 019), and the LedgerxFactory commit each file was taken from —
      because a fresh-repo scaffold loses `git log` and prose provenance is
      weaker than history.

## 4. `[LedgerxWallet]` The profile moves in

- [ ] 4.1 `templates/wallet-exercise.template.yaml` — moved unchanged. Its
      `kind: ledgerx_wallet_exercise_template` and
      `instantiates: xfactory_wallet_grant_exercise` are NOT renamed (parent R2
      freezes the prefix).
- [ ] 4.2 `profile/distinct-holder-constraints/dhc-lx-create-post-01.yaml` — the
      DHC moved out of `tenants/ledgerxcorp/wallets/`, content unchanged.
      `constraint_id` is unchanged, so `runsheet.md:174`'s by-ID reference
      survives without an edit.
- [ ] 4.3 `tests/validate_wallet_estate.py` — moved, with exactly three
      mechanical changes and no rule change: (a) `VALIDATOR_CANDIDATES` and the
      five-level walk DELETED, replaced by the single fixed relative path
      `openXwallet/scripts/validate-openxwallet.py` governed by 3.4's pin (D5);
      (b) a declared ESTATE ROOT parameter defaulting to the parent of the
      LedgerxWallet checkout, refusing with a named exit when that root holds no
      `tenants/*/wallets/` (D5); (c) `EXPECTED_WALLETS` / `EXPECTED_GRANTS` read
      from the estate manifest of §5.3 instead of being literals (D6).
      `EXPECTED_CONSTRAINT`, `ENVIRONMENT_EVIDENCING`, `PLATFORM_VERIFIABLE`,
      `PIN_VERDICTS` and every negative-probe corpus are BYTE-UNCHANGED.
- [ ] 4.4 `profile/custody-posture.yaml` — **NEW, not a move** (D8): the declared
      Ledgerx posture (`holder_readable`, environment-evidencing, authority
      ceiling `act`, audit records say "environment" never "holder"), citing the
      2026-08-08 ratification as its authority. Separable: cutting this task to a
      successor costs nothing else in the packet.
- [ ] 4.5 The validator checks the tenant records against 4.4's posture, so the
      posture is validated rather than asserted.
- [ ] 4.6 Prove the fork-freedom property D4 names: every rule, threshold,
      expected set and probe corpus appears in EXACTLY ONE file across both
      repositories. A grep-based check, recorded as evidence.

## 5. `[LedgerxFactory]` Nest, delegate, and repoint — ONE commit

- [ ] 5.1 `.gitmodules` gains `[submodule "LedgerxWallet"] path = LedgerxWallet
      url = git@github.com:opensoft/LedgerxWallet.git`, and the gitlink. Section
      name MATCHES the path — noted because the existing entry is
      `[submodule "ledgerXavatar"]` against `path = LedgerxAvatar`, and this
      change does not propagate that mismatch.
- [ ] 5.2 Delete the three moved paths.
- [ ] 5.3 Write the estate manifest (D6) beside the records it enumerates: the
      two wallet ids and the two grant→wallet bindings, declared as data.
- [ ] 5.4 Write the DELEGATING bar entry at the SAME path
      `tests/validate_wallet_estate.py` (D4): resolve
      `LedgerxWallet/tests/validate_wallet_estate.py` from the repo root, read
      and compare the THREE pin declarations (D7) and refuse on disagreement,
      invoke with this tree as the estate root, propagate the exit code, and
      REFUSE with a named exit plus the remediation string
      `git submodule update --init LedgerxWallet` when the submodule is
      uninitialized. It holds NO rule, NO threshold, NO expected set, NO probe
      corpus.
- [ ] 5.5 `stack.yaml` — `openxwallet.contract_source` re-sourced from
      `openxFactory-nested-submodule-pin` to `LedgerxWallet-nested-submodule-pin`,
      and the block's derivation comment rewritten to name the descendant's pin.
      `contract_ref` UNCHANGED (`63f5a1ad…`), so the re-homing is bisectable
      against a re-pin. The preserve-this-block comment stays.
- [ ] 5.6 **THE LIVE-WINDOW GUARD (D9).** Repoint
      `specs/016-posting-segregation-of-duties/runsheet.md:23` — the relative
      link `[templates/wallet-exercise.template.yaml](../../templates/wallet-exercise.template.yaml)`
      — and `quickstart.md:15`'s relative validator invocation, IN THIS COMMIT.
      The runsheet is `Status: prepared (this feature performs NONE of it)`, its
      phases 1–6 have not run, and
      `modify-ledgerx-posting-authority-for-segregation-of-duties` is still
      ACTIVE. LINKS ONLY: no step, actor, abort condition or evidence
      requirement is touched.
- [ ] 5.7 **[OPERATOR]** Tell the window's operator that the two references
      moved, before the window runs. Not a file edit and therefore its own task.
- [ ] 5.8 `tests/validate_document_estate_surface.py` — amend the allowed-kind
      registration for `ledgerx_wallet_exercise_template`, whose artifact has left
      the tree, in the style the surrounding entries use (a dated note recording
      what changed and why), so a surface gate does not carry a registration for
      an absent artifact.
- [ ] 5.9 `README.md` (the feature-016 entry's `tests/validate_wallet_estate.py`
      and `tenants/ledgerxcorp/wallets/` references), `.github/CODEOWNERS` (a
      `/LedgerxWallet` line), and `models/protected-surface.yaml`'s PROSE mention
      at `:438` — a pointer amendment only. Verified: that file carries NO digest
      row for any of the three moved paths, so no digest re-pin is owed.

## 6. Evidence and close

- [ ] 6.1 **[OPERATOR]** Promote the LedgerxWallet ruleset to ACTIVE once a check
      has reported once; tag `lxw-v1.0`.
- [ ] 6.2 The LedgerxFactory bar green: every `tests/validate_*.py` by exit code,
      with the wallet estate reached THROUGH the delegator. Baseline count
      recorded before and after, so a silently-dropped validator is visible as a
      count delta.
- [ ] 6.3 The three-way pin agreement printed by the delegator (gitlink, pin
      manifest `revision`, `stack.yaml` `contract_ref`), and a RED proof: mutate
      one of the three and show the refusal.
- [ ] 6.4 A RED proof that the delegator refuses with the remediation string on
      an uninitialized `LedgerxWallet` submodule, and that it does not skip.
- [ ] 6.5 A RED proof that the moved validator refuses on an estate root holding
      no `tenants/*/wallets/`.
- [ ] 6.6 A RED proof that the deleted candidate walk cannot resolve: with no
      `openXwallet` gitlink initialized under LedgerxWallet, the validator refuses
      rather than finding a validator by walking up into openxFactory or the
      aggregation.
- [ ] 6.7 `[openxFactory]` DTN-026's detail section notes the FIRST DESCENDANT
      EXISTS, and its status advances only on the register's own definition (the
      domain re-pin and local-copy retirement COMPLETE) — not on ratification.
- [ ] 6.8 Archive this change only on merged plus green realization evidence, per
      `release-realization`. It declares a code surface, so it does NOT archive on
      landing.

## 7. Explicitly NOT done

- [ ] 7.1 No `xFactories/LedgerxWallet` aggregation gitlink (D2). If a later
      change takes it, the ratified rule binds both gitlinks to one commit, AND
      D5's relative estate-root default becomes a required argument.
- [ ] 7.2 No `MedxWallet`, `codexWallet`, `OpsxWallet` or `AdxWallet` — none has a
      wallet profile artifact, and rule 5 forbids creating an empty boundary.
- [ ] 7.3 No change to `opensoft/openXwallet`.
- [ ] 7.4 No LedgerxFactory GitHub Actions workflow. The three-way check is
      running code in a human-run bar, and the absence of a required check is a
      named successor rather than an implied enforcement.
- [ ] 7.5 No `kind:` / capability-id / finding-code / filename rename (parent R2).
- [ ] 7.6 No move of the tenant estate or the platform seam (Q2, D3a).
