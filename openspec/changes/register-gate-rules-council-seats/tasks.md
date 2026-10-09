# Tasks: register-gate-rules-council-seats

Lane: hermes-wallet-exercise

Dependency-ordered, and the order is a finding rather than a preference (design
D5): there is no interleaving in which the register carries a second authority
row and the REQUIRED `wallet-validation` check is green at the pinned reader.

**Tags.** Untagged = openxFactory. `[openXwallet]` = `opensoft/openXwallet` and
its own OpenSpec instance. `[codexFactory]` = `opensoft/codexFactory`.
`[hermes-install]` = `opensoft/xFactory-Hermes-Install`. `[OPERATOR]` = only
Brett can perform it — a key, a human-only surface write, a ratification, a
platform setting. `[GOVERNANCE]` = it needs a ruling or an OpenSpec change
before the work is legal.

**Nothing in §3 is an agent act.** `governance/review-authority/register.yaml`
is a permanently human-only surface by ratified requirement and a
never-clearable floor member by exact path in codexFactory's gate rules. §3 is
written as a WALK for Brett to execute and to record; no agent writes those
files.

---

## 1. Governance — this change's own work

- [x] 1.1 **[OPERATOR] [GOVERNANCE]** Ratify or return this proposal. Nothing
      below §1 is legal until this is ticked. Ratification alone REALIZES
      NOTHING — no key is minted, no row is written, no pin moves.
      **RATIFIED 2026-09-06T14:13:46Z, Brett Heap, verbatim: "lets take them in
      your recommended order all approved"** —
      `review/ratification-2026-09-06.md`.
- [x] 1.2 **[OPERATOR] [GOVERNANCE]** Rule **Q-GRC-1** — where the four private
      halves live, given that `gate_rules_council` has no automated lane.
      Recommendation on record: mint into codexFactory `worker-credentials` now,
      `holder_readable`, with the custody attestation naming the OWED job as the
      holder execution context and saying plainly that it does not exist yet.
      **RULED (i)** — 2026-09-06T14:13:46Z: "mint the four private halves into
      codexFactory's `worker-credentials` now, `holder_readable`; the custody
      attestation names the OWED job (codexFactory task 5.9a) as the holder
      execution context and states plainly that it does not exist yet."
- [x] 1.3 **[OPERATOR] [GOVERNANCE]** Rule **Q-GRC-2** — the composition pin for
      a rule-setting body that has none, and the two-body blast radius of one
      shared-roster flip. Q8(d) (exact versions only) is ALREADY RULED and is
      not reopened by this row.
      **RULED** — 2026-09-06T14:13:46Z: "pin the composition exactly, from the
      same enrolled roster (Q8(d) of 2026-08-26 stands; not reopened). The
      two-body coupling is accepted openly: a roster pin flip revokes both
      bodies' grants and parks both; re-issuance is a scheduled two-body
      ceremony with one walk record per body."
- [x] 1.4 **[OPERATOR] [GOVERNANCE]** Rule **Q-GRC-3** — the expiry horizon for
      `grant-grc-0001`. Recommendation on record: `2027-06-30T00:00:00Z`,
      matching `grant-mrc-0002` so one ceremony covers both bodies.
      **RULED** — 2026-09-06T14:13:46Z: "`expires_at: 2027-06-30T00:00:00Z`,
      the same date as `grant-mrc-0002`, so one re-issuance ceremony covers
      both bodies."
- [x] 1.5 **[OPERATOR] [GOVERNANCE]** Rule **Q-GRC-4** — the two deferred seats
      (`intent_owner_role_slot`, `client-security-compliance-officer`):
      confirm they are NOT registered now and that whichever codexFactory roster
      act binds them registers their keys in the same governed act.
      **RULED** — 2026-09-06T14:13:46Z: "register neither deferred seat now;
      delete neither. `intent_owner_role_slot` and
      `client-security-compliance-officer` are recorded as owed registrations
      that trigger on a codexFactory roster act, which must register the key
      in the same governed act."
- [x] 1.6 On ratification, flip `docs/council-seat-key-mint-runbook.md` from
      `Status: draft` to `Status: ratified` and add
      `Ratified by: register-gate-rules-council-seats`.
      DONE 2026-09-08: header now reads `Status: ratified` /
      `Ratified by: register-gate-rules-council-seats`, the form
      `docs/factory-origin-key-mint-runbook.md` and `docs/roles-and-authority.md`
      already use and the primary spelling `docs/document-lifecycle.md:66`
      requires. The "why this document is draft" paragraph is REWRITTEN rather
      than deleted — it now records that it WAS draft, why, and which ruling
      flipped it — and it carries the limit the runbook's own last bullet
      states: ratified is not enforced; no gate refuses a register act that
      skips this document.
- [x] 1.7 `OPENSPEC_TELEMETRY=0 openspec validate register-gate-rules-council-seats
      --strict` and `--all --strict` clean from the repository root; the change
      is listed in `README.md`'s `## OpenSpec Records` block and the runbook in
      the README doc index; the `sequenced_after` corpus ledger carries this
      change's row.
      **DONE 2026-10-05, every clause read on oxF `main` `20ce593e8`.**
      **Validation** ran through the repository's PINNED entrypoint, never a
      bare `openspec` (CLAUDE.md, "OpenSpec authoring notes"; the command above
      is the unpinned spelling). `python3 scripts/validate-openspec-cli-pin.py
      --change register-gate-rules-council-seats --strict` reports `Totals: 1
      passed, 0 failed (1 items)` and `every target validated --strict clean`.
      `--all --strict` exits 0 with `Totals: 110 passed, 1 failed (111 items)`
      and `0 UNDISPOSITIONED failures`, **and the entrypoint itself prints "THIS
      IS NOT A CLEAN TREE"**: the one failure is `add-chain-attestation`
      (`signed-execution-chain`'s MODIFIED block), an ACCEPTED EXCEPTION (Brett
      Heap, 2026-09-05, *"take exit 2"*) that is not this change's. "Clean" is
      read here as no failure attributable to this change and none
      undispositioned, not as a failure-free tree. **Listings:** the change is
      the `## OpenSpec Records` entry at `README.md:1815`, and the runbook is
      the doc-index entry at `README.md:129` (*"Council Seat Signing Keys — Mint
      and Register Act"*, under `## Documentation`). **Ledger:**
      `tests/sequenced_after/corpus-ledger.yaml:282` carries
      `register-gate-rules-council-seats` (`state: active`, `class: sole`,
      `declares: [add-wallet-carried-review-authority,
      openXwallet:widen-register-reader-for-a-second-council]`, `moved_by:
      "#717"`), and `python3 scripts/validate-sequenced-after.py .
      --ledger-diff` reports `per-change sweep ledger consistent with the corpus
      (229 rows)`. See walk-2026-09-12-register-act.md § 13.6 bookkeeping note 2
      (appended 2026-10-05).**

## 2. The reader, and the pin — the hard prerequisite

- [x] 2.1 **[openXwallet] [GOVERNANCE]** Open the reader-widening change
      (proposed id `widen-register-reader-for-a-second-council`, declared in this
      proposal's `sequenced_after:`). Two defects, both MEASURED at
      `b7b0fbb3e6d614f60a24737c247e45dada9408aa` / `wallet-v1.4` (design D5):
      `register-minimal-shape-exceeded` on a second AUTHORITY row, and
      `register-seat-duplicate` on `lead-security` — a seat name both councils
      seat.
      **DONE 2026-10-05, realized in `opensoft/openXwallet`; rows 2.1-2.6 all
      rest on the same two landings, openXwallet PR #16 → `6ec84b1b` (merged
      2026-09-06T23:42:00Z) and PR #18 → `f3eb929b` (merged
      2026-09-07T00:49:00Z).** openXwallet's change
      `widen-register-reader-for-a-second-council` (its `tasks.md` row 1.1,
      ticked) carries exactly the id this proposal declares in
      `sequenced_after:` (`proposal.md:4`). The `[GOVERNANCE]` bar is its row
      1.2: ratified 2026-09-06T23:25:11Z by Brett Heap, operator authority,
      verbatim *"ratify 16 and archive add-per-seat-register-entries"*
      (Q-WRR-1..5 ruled with it, its rows 1.3-1.7). Both defects were
      re-measured at the pinned reader (its `design.md` D0): the reader at
      openXwallet `05007e26` is BYTE-IDENTICAL to `b7b0fbb3` / `wallet-v1.4`
      (`git diff b7b0fbb3 05007e26 -- scripts/validate-openxwallet.py` is empty,
      re-run 2026-10-05, and the same holds at `6ec84b1b`), and the probe draws
      `register-minimal-shape-exceeded` on the second authority row plus
      `register-seat-duplicate` on `lead-security` (and on `lead-quality` and
      `company-policy-lead`), with the note reading `5 of 8`; this change's own
      design D5 measured the same two codes at the same pin on a two-seat probe
      (`4 of 6`). The lane that did that work, `hermes-wallet-exercise`, is this
      lane's former register key (cut over to `codeXfactory-2` on 2026-09-14;
      the § 13.3 lift sentence says *"same lane, same window"*). See
      walk-2026-09-12-register-act.md § 13.6 bookkeeping note 2 (appended
      2026-10-05).**
- [x] 2.2 **[openXwallet]** RED FIRST. Two failing tests before either fix:
      (a) a fixture register with TWO authority rows, each resolving end to end
      to its own wallet, grant and attestation, asserted CLEAN; (b) a fixture
      register whose `seat_keys` carries the same `seat_id` under two different
      `council_id`s, asserted CLEAN, together with a third that carries the same
      `seat_id` TWICE under ONE `council_id`, asserted REFUSED with
      `register-seat-duplicate`. Both must fail against the reader as it stands.
      **DONE 2026-10-05, in openXwallet (its rows 2.1-2.8, ticked), and the RED
      state was MEASURED, not read.**
      `tests/widen_register_reader/test_second_council.py` landed with the
      proposal, before any fix (openXwallet PR #16 → `6ec84b1b`). Checked out at
      `6ec84b1b`, whose reader is byte-identical to the pinned `b7b0fbb3` (2.1),
      `pytest tests/widen_register_reader` gives `8 passed, 2 xfailed`, the two
      being `xfail(strict=True)`: (a)
      `test_a_second_commissioned_body_resolving_end_to_end_is_admitted`
      (openXwallet row 2.2: two authority rows, the second resolving end to end
      to its own wallet, root grant and custody attestation, asserted CLEAN;
      XFAIL, naming `REGISTER_MVP_SINGLE_ROW`) and (b)
      `test_two_councils_may_seat_the_same_role_name` (its row 2.3: one
      `seat_id` under two `council_id`s, asserted CLEAN; XFAIL, naming the
      `seat_id`-only duplicate table). The third fixture is
      `test_one_council_naming_a_seat_twice_is_refused` (its row 2.4): the same
      `seat_id` twice under ONE `council_id`, asserted REFUSED with
      `register-seat-duplicate`. It PASSES at `6ec84b1b` and after, by design:
      the fix narrows the trigger and keeps the refusal, so "must fail" binds
      the two CLEAN assertions and not this one. Two further tests passing at
      `6ec84b1b` pin, by exact code, the two refusals the pinned reader emits:
      `register-minimal-shape-exceeded` on the second row and
      `register-seat-duplicate` on the shared seat names. At `f3eb929b` the same
      file reads `11 passed`, no xfail left. See walk-2026-09-12-register-act.md
      § 13.6 bookkeeping note 2 (appended 2026-10-05).**
- [x] 2.3 **[openXwallet]** Fix defect 2: key the seat-entry duplicate table on
      the PAIR `(council_id, seat_id)`. **Leave `key_id` and `key_fingerprint`
      uniqueness GLOBAL** — a key is one key, and two bodies presenting it are
      two claims on one identity.
      **DONE 2026-10-05, in openXwallet (its row 3.1, commit `9ebc686`, PR #18 →
      `f3eb929b`).** At `f3eb929b`, `scripts/validate-openxwallet.py:2958-2959`
      keys the table by `(council_id, entry[field])` for `seat_id` and by the
      bare value for `key_id` and `key_fingerprint` (`scoped = field ==
      "seat_id"`). The refusal keeps the code `register-seat-duplicate` and its
      message now names the council. Global uniqueness is asserted ACROSS
      councils by `test_key_id_and_fingerprint_stay_globally_unique[key_id]` and
      `[key_fingerprint]` (both pass) and by two self-test probes, and it BITES:
      changing `scoped = field == "seat_id"` to `scoped = True` in a scratch
      copy of the reader and running it on openXwallet itself reds exactly those
      two probes (2 findings, re-run 2026-10-05, matching its
      `realization-evidence-2026-09-06.md` § 3; nothing was committed). See
      walk-2026-09-12-register-act.md § 13.6 bookkeeping note 2 (appended
      2026-10-05).**
- [x] 2.4 **[openXwallet] [GOVERNANCE]** Fix defect 1 per the Q-GRC-5 ruling:
      retire `REGISTER_MVP_SINGLE_ROW` in favour of the invariants it stood in
      for (every row resolves end to end; every seat entry attaches to a row
      that commissions its body; the pair is unique), rather than substituting
      the number 2 for the number 1.
      **DONE 2026-10-05, in openXwallet (its row 3.2, commit `9ebc686`, PR #18 →
      `f3eb929b`).** Read at `f3eb929b`: `REGISTER_MVP_SINGLE_ROW` has no
      reference left in the reader's syntax tree, and the one string constant
      that mentions `register-minimal-shape-exceeded` is `check_register`'s
      docstring, so the code is not a literal anything can emit or assert (both
      read with `ast`, 2026-10-05;
      `test_the_retired_row_count_refusal_is_emitted_by_nothing` asserts the
      second and passes). The comment block where the constant stood
      (`:2578-2616`) names this row's three invariants, each on the code that
      already enforced it and with NO new finding code: (i) every authority row
      resolves end to end (`check_register`'s row loop,
      `register-wallet-unresolved` through `register-row-malformed`); (ii) every
      seat entry attaches to a row that commissions its body
      (`_check_seat_keys`: `register-seat-row-unresolved` and
      `register-seat-council-mismatch`); (iii) the pair is unique (2.3). No
      number replaces the cap: it is not raised to two. The `[GOVERNANCE]` bar:
      Q-GRC-5 was ruled in `review/ratification-2026-09-06.md` as this change's
      recorded ask of openXwallet, and openXwallet decided it in its own change
      — Q-WRR-1 (retire by name) and Q-WRR-2 (no numeric bound), its rows 1.3
      and 1.4, ratified 2026-09-06T23:25:11Z. The removed refusal carries a
      migration note in openXwallet's `contracts/CHANGELOG.md` (`##
      wallet-v1.5`). See walk-2026-09-12-register-act.md § 13.6 bookkeeping note
      2 (appended 2026-10-05).**
- [x] 2.5 **[openXwallet]** Extend the reader's own S4 self-test block with the
      two-row and two-council probes, so a later edit cannot silence the
      invariant while the self-test stays green.
      **DONE 2026-10-05, in openXwallet (its row 3.4, commit `9ebc686`, PR #18 →
      `f3eb929b`).** The self-test block runs in the validator's ordinary
      invocation, so inside the REQUIRED check every consumer runs. At
      `f3eb929b` it carries (`:2484-2557`):
      `self-test/register-two-bodies-clean` (two rows; it asserts the notes
      positively, `2 row(s)` and `6 of 6`),
      `register-two-councils-one-seat-name`,
      `register-seat-duplicate-within-one-council` and
      `register-second-row-unresolved`, plus two probes this row did not name,
      `register-seat-attached-to-another-bodys-row` and
      `seat-duplicate-across-councils[key_id]` / `[key_fingerprint]`. The two
      probes that asserted the retired code were removed in the same edit.
      `validate-openxwallet.py .` on openXwallet itself reads `0 error(s), 0
      warning(s)`, plain and `--strict`, and the probes BITE: replacing the pair
      key with the bare `seat_id` in a scratch copy reds four findings
      (`register-two-bodies-clean` twice, `register-two-councils-one-seat-name`,
      `register-second-row-unresolved`), the four its
      `realization-evidence-2026-09-06.md` § 3 records (re-run 2026-10-05;
      nothing was committed). See walk-2026-09-12-register-act.md § 13.6
      bookkeeping note 2 (appended 2026-10-05).**
- [x] 2.6 **[openXwallet]** Cut the bundle tag (`wallet-v1.5` or as allocated)
      and publish the digests in `contracts/manifest.yaml`.
      **DONE 2026-10-05, in openXwallet (its rows 4.1-4.3).** The tag
      `wallet-v1.5` is ANNOTATED (`git cat-file -t` → `tag`, tag object
      `ff9ac797`, dated 2026-09-07T00:51:35Z; its message says the lane
      coordinator tagged on Brett Heap's word *"cut wallet-v1.5"*, openXwallet
      row 4.1) and peels to `f3eb929b9ab6d78bf30e26bf1d7a99af86a7016e`, PR #18's
      merge commit and an ancestor of openXwallet `main`; `git ls-remote --tags
      https://github.com/opensoft/openXwallet` lists `refs/tags/wallet-v1.5^{}`
      at that sha (read 2026-10-05). At `f3eb929b`, `contracts/manifest.yaml`
      reads `contract_bundle_version: wallet-v1.5`, the only line that moved in
      that file; `contracts/releases/wallet-v1.5.digests.yaml` (eight entries)
      differs from `wallet-v1.4`'s in exactly one line, `bundle_tag`. All eight
      digests, recomputed 2026-10-05 as sha256 over the raw git blobs at
      `f3eb929b`, equal BOTH the release inventory's and the manifest's: 8 of 8.
      **Read plainly, "publish the digests in `contracts/manifest.yaml`" was
      realized as: the manifest carries `wallet-v1.5` and the eight digests,
      none of which moved because no contract byte did, and the NEW published
      artifact is the release inventory.** oxF's side is 2.7:
      `contracts/openxwallet-pin.yaml` names `f3eb929b` / `wallet-v1.5` and the
      `openXwallet` gitlink is the same commit (read at `20ce593e8`). See
      walk-2026-09-12-register-act.md § 13.6 bookkeeping note 2 (appended
      2026-10-05).**
- [x] 2.7 Advance `contracts/openxwallet-pin.yaml`: `commit:` and
      `contract_bundle_tag:` ONLY. **No `files:` digest row moves** —
      `scripts/validate-openxwallet.py` sits under `pinned_by_commit_only:` and
      a reader-only release moves no contract byte. Reverify the other eight
      digests by recomputation at the new commit rather than carrying them on
      trust, and re-record `carve_commit:` only if a digest actually moved.
      DONE 2026-09-07: `commit:` → `f3eb929b9ab6d78bf30e26bf1d7a99af86a7016e`,
      `contract_bundle_tag:` → `wallet-v1.5`; all eight `files:` digests
      recomputed at the new commit and unchanged (`carve_commit:` untouched);
      gitlink `openXwallet` moved with the pin in the same commit, matching the
      wallet-v1.4 precedent (`9cfdeca5`). openxFactory PR (lane
      hermes-wallet-exercise), DO NOT MERGE pending Brett's word.
- [x] 2.8 Move the consumer gate's LITERAL assertions in
      `.github/workflows/openxwallet-consumer-gate.yml` IN THE SAME PULL REQUEST
      as 2.7 — a stale literal is a red REQUIRED check on a human-only surface,
      which is the parked-candidate shape this whole arc exists to end:
      - `intake register: 4 of 4 per-seat signing key(s) adjudicated and resolved`
        → `8 of 8`;
      - a NEW assertion that `wal-agent-grc-0001`'s five declared keys were
        adjudicated, beside the existing `wal-agent-mrc-0001` one;
      - keep every count LITERAL. A wildcard would let a register that lost a
        body pass the positive proof.
      2026-09-07: literal flip DEFERRED to the register act (§ 3.6/3.7) per the
      coordinator disposition on PR #717 — 2.9's neutrality gate governs; on a
      one-row register the widened reader emits `4 of 4`.
      DONE 2026-09-08 — **PERFORMED IN THIS ACT**, per proposal.md's 2026-09-07
      AMENDMENT (newest of the three texts and therefore governing; § 2.8's own
      body sentence "IN THE SAME PULL REQUEST as 2.7" was never edited and is
      superseded). `.github/workflows/openxwallet-consumer-gate.yml`: `:153`
      `4 of 4` → `8 of 8` with its failure message's "four" → "eight"; a NEW,
      SEPARATE assertion `^note  wallet 'wal-agent-grc-0001': 5 declared key\(s\)
      adjudicated ` beside the mrc one at `:193` (NOT a widening — the runbook's
      § 4: "add one for the new wallet, do not widen the existing one"); and
      `:196`'s conjunction echo gains `wal-agent-grc-0001` so the new line is
      shown rather than merely asserted. Every count stays LITERAL.
      **The test that pins those literals moved in the SAME act, because it is
      the same precondition one file over:**
      `tests/openxwallet_consumer_gate/test_gate_invocation.py` —
      `test_the_four_per_seat_keys_are_asserted_as_adjudicated` renamed to
      `..._eight_...` with its literal moved (measured: it FAILED on the flipped
      tree before the move, which would have reddened the REQUIRED
      `pytest-suite` check), plus a new sibling
      `test_the_second_bodys_wallet_is_asserted_separately` holding the grc grep
      in place as a SECOND test rather than a widened one. 17 passed in
      `tests/openxwallet_consumer_gate`.
      **VERIFIED BY REPLAY, not by reading:** every `grep` in the workflow's two
      assertion steps was extracted verbatim and run against this tree's
      `wallet-gate.log` / `factory-identity-gate.log` — **13 of 13 PASS**,
      including `:161` (`8 of 8`), `:193` (the grc wallet) and `:196` (the echo,
      which surfaces 5 lines with both wallets among them). Recorded in the walk
      at § 5.1.
- [x] 2.9 **Gate:** with 2.7 + 2.8 landed and the register still carrying ONE
      row, `wallet-validation` is GREEN and the log's `intake register read:`
      note still says `1 row(s)`. The pin advance must be provably neutral
      BEFORE the register moves.
      DONE 2026-09-07: with 2.7 landed (2.8 deferred per the coordinator
      disposition), `validate-openxwallet.py .` at the new pin is rc=0 clean
      (plain and `--strict`) with `intake register read: … (1 row(s))` and
      `intake register: 4 of 4 per-seat signing key(s) adjudicated and
      resolved`; output diffed byte-identical against the same command run at
      the old pin (`b7b0fbb3`). Local proof recorded; CI `wallet-validation`
      watched on the PR.

## 3. Brett's operator WALK — the mint and the register act

**[OPERATOR] throughout.** Executed against
`docs/council-seat-key-mint-runbook.md`, recorded in ONE walk file
`openspec/changes/register-gate-rules-council-seats/walk-<YYYY-MM-DD>-register-act.md`
in the form of `walk-2026-09-02-register-act.md`. Do not start §3 until §2's
gate is green: at the old reader every one of these writes is refused.

- [x] 3.1 **[codexFactory]** PREREQUISITE (design D3): author
      `review_council_profiles.gate_rules_council` in
      `hermes/domain/agent-mixes.yaml` and a `composition_source_map` on
      `hermes/domain/review-councils/gate-rules.yaml`, mirroring
      merge-readiness's six declared components with EXACT model identifiers.
      **No grant is issued against a composition that does not exist.**
      **AMENDED 2026-09-07** (R1/R2, Brett Heap, in-session
      2026-09-07T12:40:19Z, verbatim *"R1 lead-architect claude-opus-5, R2
      (a) — re-sequence 5.9a first"*,
      <https://github.com/opensoft/openxFactory/pull/717#issuecomment-5570774593>):
      **3.1 realizes AFTER 5.9a.** R1 pins `lead-architect` to
      `claude-opus-5` via the recorded roster-change act
      (`guardrails.roster_change: lead_accepted_recorded`); R2(a) sequences
      codexFactory slice `041-gate-rules-convening-caller` (task 5.9a, the
      `gate_rules_council` caller with seat briefings) BEFORE this row, so
      the six mirrored components are declared against a caller that exists
      rather than asserted. See proposal.md's 2026-09-07 AMENDMENT for the
      restated § Sequencing.
      **DONE 2026-09-07, on codexFactory `main`** — bookkeeping tick only; the
      work is another repository's and no openxFactory byte moves for it.
      Landed by codexFactory **PR #277 → merge `511d95c5`** (branch
      `041-gate-rules-convening-caller`, 2026-09-07T12:42:49-04:00), which
      carries BOTH halves this row asks for:
      `hermes/domain/agent-mixes.yaml#review_council_profiles.gate_rules_council`
      (`holder_ref: agent:gate-rules-council`, `all_possible_seats`,
      `model_assignments` with EXACT identifiers) and
      `hermes/domain/review-councils/gate-rules.yaml#council.composition_source_map`
      — six components mirrored from merge-readiness component for component
      per R2(a), each `source` pointing into THIS body's own profile, plus a
      `deferred_seats` block recording Q-GRC-4's two absences beside the
      components. R2(a)'s re-sequencing is satisfied: the same PR is task 5.9a's
      caller, so the content components are EXECUTION-MATCHED against a live
      render rather than asserted. R1's pin (`lead-architect` →
      `claude-opus-5`) entered through the recorded roster-change act
      `hermes/domain/review-councils/records/2026-09-07-gate-rules-roster-lead-architect-pin.md`,
      with Lead Quality's ACCEPT AS AMENDED (LQ-C1..C4) at
      `records/2026-09-07-seat-returns/lead-quality.md`. **Read with LQ-C1 and
      LQ-C3 attached**: the pin stands on the operator's judgment alone, no
      soak has been recorded at `claude-opus-5` for this seat, and the
      accepting seat disclosed an uncured conflict.
- [x] 3.2 Mint FOUR Ed25519 keypairs, one per registered seat —
      `lead-architect`, `lead-security`, `lead-quality`, `company-policy-lead` —
      plus the body's root key `key-grc-0001`. Private halves NEVER enter git,
      CI logs or an agent session; provision the four seat halves per the
      Q-GRC-1 ruling. Record the public halves, the `did`s and the recomputing
      fingerprints in a codexFactory mint record, as the 2026-08-28 mrc mint
      did.
      EVIDENCE (PENDING VALUES): mint record drafted at codexFactory
      `hermes/domain/review-councils/records/2026-09-08-gate-rules-seat-signing-keys-minted.md`;
      five keypairs (`key-grc-0001` root, four `key-grc-seat-<seat>-0001`);
      four private halves provisioned as
      `COUNCIL_SEAT_SIGNING_KEY_GRC_{LEAD_ARCHITECT,LEAD_SECURITY,LEAD_QUALITY,COMPANY_POLICY_LEAD}`
      on codexFactory environment `worker-credentials` at 2026-09-08T04:19:00Z;
      root private half in the operator's vault only. Public values derived
      through the pinned decoders (`scripts/validate-factory-identity.py
      --derive`), never a second tool.
      DONE 2026-09-08. **MINTED BY THE OPERATOR (Brett Heap)** with a
      lane-authored, HOST-SIDE program that is in NO repository —
      `~/session-prompts/mint-grc-council-seats/tools/mint-grc-council-seats.py`,
      mirroring openxFactory's own `scripts/mint-factory-origin-key.py` in form
      (23 tests, passing when the mint ran; they now ERROR AT SETUP because
      their fixture copies `walk-PENDING-register-act.md`, which the fill step
      renamed — no assertion fails). Seeds generated in-process
      (`secrets.token_bytes(32)`), never written to disk; passed to `gh secret
      set` ON STDIN with no `--body`, so no seed is ever an argv element; public
      values derived in-process through `scripts/validate-factory-identity.py`'s
      own `derive` entry point (the PINNED decoders), never a second tool.
      Command log (argv and stdin LENGTHS only, content never logged):
      `~/session-prompts/mint-grc-council-seats/mint-grc-command-log.txt`.
      Public values: `~/session-prompts/mint-grc-council-seats/values.json` —
      PUBLIC ONLY; both programs refuse outright on any 64 bare hex characters
      without a `sha256:` prefix, and a re-scan of all nine files this act
      touches found ZERO such strings.
      **CUSTODY, stated plainly.** Four seat halves (64 lowercase hex) stored
      into `opensoft/codexFactory` environment `worker-credentials` and each
      confirmed present: `COUNCIL_SEAT_SIGNING_KEY_GRC_LEAD_ARCHITECT`
      2026-09-08T04:18:53Z, `..._GRC_LEAD_SECURITY` 04:18:55Z,
      `..._GRC_LEAD_QUALITY` 04:18:57Z, `..._GRC_COMPANY_POLICY_LEAD` 04:19:00Z
      — the fourth being the attestation's `verified_at`. The ROOT
      (`key-grc-0001`) seed was printed ONCE to the operator's terminal shortly
      after 04:19:00Z and stayed on that screen until he had stored it in his
      own vault (1Password; runbook § 2.1 and the 2026-08-28 mrc precedent name
      no vault tool) and pressed Enter at 12:29:23Z — a window of 8h10m, on the
      record because it happened and because no rule in this estate bounds it.
      The program then emitted the clear-screen + scrollback sequence and the
      operator confirmed the seed was gone (`clear_sequence_emitted: true`,
      `operator_confirmed_clear: true`). Run completed 2026-09-08T12:31:36Z.
      **No shred is claimed and none was needed for key material: no seed was
      ever on disk.**
      MINT RECORD (codexFactory): `hermes/domain/review-councils/records/
      2026-09-08-gate-rules-seat-signing-keys-minted.md`, opened as codexFactory
      **PR #290** (<https://github.com/opensoft/codexFactory/pull/290>), which
      also links the record from `hermes/domain/README.md`'s
      `gate_rules_council` paragraph. This act's own openxFactory PR is **#798**
      (<https://github.com/opensoft/openxFactory/pull/798>).
      Full narrative: the walk record § 3B.
- [x] 3.3 Write `governance/review-authority/wallets/wal-agent-grc-0001.yaml`:
      holder `agent:gate-rules-council`, custody `holder_readable`, root key
      `key-grc-0001` in `key_reference`, the four seat keys in `keys:` with
      per-key custody. FIVE declared keys — the shape rule (r) needs so a seat
      return naming a per-seat key is representable.
      EVIDENCE (PENDING VALUES): written — five declared keys
      (`key_reference` = `key-grc-0001` with did/multibase and NO fingerprint;
      four `keys[]` entries each with did/key_id/key_fingerprint/multibase/
      signature_algorithm/display_label/custody), outside any `examples/`
      path.
      DONE 2026-09-08: values filled. **Structure diffed against
      `wal-agent-mrc-0001.yaml` and IDENTICAL** — every key path, in order,
      compared programmatically rather than by eye. `key_reference` =
      `key-grc-0001` (`did:key:z6Mkqohim…`, no `key_fingerprint`, the mrc
      asymmetry); four `keys[]` entries with the seat fingerprints;
      `declared_at`/`created_at` = `2026-09-08T12:31:36Z`, the one Effective
      instant. The pinned reader adjudicated all five:
      `note  wallet 'wal-agent-grc-0001': 5 declared key(s) adjudicated
      (key-grc-0001, key-grc-seat-company-policy-lead-0001,
      key-grc-seat-lead-architect-0001, key-grc-seat-lead-quality-0001,
      key-grc-seat-lead-security-0001)`.
- [x] 3.4 Write
      `governance/review-authority/attestations/custody-attest-wal-agent-grc-0001.yaml`.
      Without it the unattested cap applies and the grant reaches only
      `request`. State the honest posture, including that the holder execution
      context is NAMED AND OWED rather than observed (Q-GRC-1).
      EVIDENCE (PENDING VALUES): written, KINDLESS (no `kind:`), `verified_at`
      = the secret-provisioning instant. **The posture Q-GRC-1 anticipated has
      MOVED and the attestation records the moved fact rather than the
      ruling's premise:** the holder execution context
      (codexFactory `.github/workflows/gate-rules-convening.yml`,
      `environment: worker-credentials`) is no longer OWED — it LANDED with
      task 5.9a (PR #277 → `511d95c5`). It EXISTS, has NEVER RUN (workflow id
      352457764, `total_count: 0`), refuses today with
      `seat_signing_unavailable`, and its wiring is PRESENCE-ONLY: no signing
      step consumes the four secrets yet, so provisioning them lifts the
      refusal and produces no signed return. The mint runbook's own rule
      governs the correction — "Do not describe a context you have not seen."
      NOTE (2026-09-08): the holder-context wording above was ruled by Brett
      Heap — "B2 as recommended", in-session 2026-09-08T03:20:24Z —
      https://github.com/opensoft/openxFactory/pull/717#issuecomment-5578601346
      DONE 2026-09-08: `verified_at: "2026-09-08T04:19:00Z"` — the FOURTH seat
      secret's confirmation, i.e. the instant custody of the seat halves became
      complete and therefore never earlier than any single one. KINDLESS
      confirmed by measurement: `repo scan` counts **2120** skipped documents
      (up one) while adjudicating **9** artifacts (up two — the wallet and the
      grant), which is exactly the attestation being skipped by `repo_scan` and
      consumed by the register reader. Its key set matches
      `custody-attest-wal-agent-mrc-0001.yaml` plus ONE deliberate addition,
      `holder_execution_context`, which carries the B2 wording; the reader
      accepts it and no `[register-tier-act-unattested]` is raised, so
      `grant-grc-0001` holds tier `act`.
- [x] 3.5 Write `governance/review-authority/grants/grant-grc-0001.yaml`: a ROOT
      grant (no `parent_grant_ref`), `issued_by` the anchored operator,
      `acts: [review]`, `objects: [opensoft/openxFactory]`,
      `authority_tier: act`, `approval_posture` byte-identical to
      `grant-mrc-0002`'s, `expires_at` per the Q-GRC-3 ruling. Re-examine each
      scope element deliberately and record WHY it stands, so a later reader can
      tell a decision from a paste.
      EVIDENCE (PENDING VALUES): written — ROOT grant, no `parent_grant_ref`;
      `approval_posture` diffed BYTE-IDENTICAL against `grant-mrc-0002`'s three
      lines; `expires_at: "2027-06-30T00:00:00Z"` per Q-GRC-3; `issued_by:
      Brett.Heap@opensoft.one`. Each scope element carries its own recorded
      reason on the file's face, including an explicit paragraph on why
      `objects: [opensoft/openxFactory]` and not `opensoft/codexFactory` —
      set-equality with the row's `target_repo`, and a cross-repository
      audience has no resolution path today (clarifications N7).
      DONE 2026-09-08: `issued_at: "2026-09-08T12:31:36Z"`. Key set diffed
      against `grant-mrc-0002.yaml` and IDENTICAL; `approval_posture`'s three
      lines compared as raw text and byte-identical.
- [x] 3.6 Write the second authority row in
      `governance/review-authority/register.yaml`: `row-grc-0001`, exactly the
      nine fields, `expires_at` CHARACTER-FOR-CHARACTER equal to 3.5's because
      the reader compares the two. **`row-mrc-0001` is not touched.**
      EVIDENCE: written — `row-grc-0001`, exactly nine fields (checked by
      parse), `expires_at` character-for-character equal to 3.5's. The edit is
      APPEND-ONLY and that is measured, not asserted: `git diff --numstat` on
      `register.yaml` reports `129  0` — zero deletions — so `row-mrc-0001`
      and `revocation_staleness_bound: P7D` are byte-untouched.
      DONE 2026-09-08: the reader now reports
      `note  intake register read: governance/review-authority/register.yaml
      (2 row(s))` with NO `register-minimal-shape-exceeded` and no
      `[register-*]` finding of any kind.
- [x] 3.7 Append the FOUR `seat_keys` entries: `council_ref:
      agent:gate-rules-council`, `council_id: gate_rules_council`,
      `authorizing_row: row-grc-0001`, one `key_id` and one recomputing
      `key_fingerprint` each. Key ids are namespaced (`key-grc-seat-<seat>-0001`)
      because `key_id` uniqueness stays global.
      EVIDENCE (PENDING VALUES): four entries appended, exactly seven fields
      each (checked by parse), `council_ref: agent:gate-rules-council`,
      `council_id: gate_rules_council`, `authorizing_row: row-grc-0001`. Three
      seat ids (`lead-security`, `lead-quality`, `company-policy-lead`) now
      appear TWICE in the file under two `council_id`s — legal only at
      `wallet-v1.5`, whose duplicate table is keyed on the PAIR. Key ids carry
      the `grc` namespace because `key_id` and `key_fingerprint` uniqueness
      stays GLOBAL, and because `COUNCIL_SEAT_SIGNING_KEY_LEAD_SECURITY`
      already holds the merge-readiness seat's seed.
      **2.8's deferred literal flip is performed in this same act** (per the
      2026-09-07 disposition and proposal.md's AMENDMENT, which is newest and
      governs): `.github/workflows/openxwallet-consumer-gate.yml` moves
      `4 of 4` → `8 of 8`, gains a SEPARATE
      `wal-agent-grc-0001': 5 declared key(s) adjudicated` assertion beside the
      mrc one rather than widening it, and its conjunction echo names both
      wallets. Every count stays LITERAL. Note tasks.md § 2.8's own body still
      says "IN THE SAME PULL REQUEST as 2.7" — that sentence was never edited
      and is superseded by the disposition beneath it.
      DONE 2026-09-08, with the public halves filled:
      `lead-architect` / `key-grc-seat-lead-architect-0001` /
      `sha256:858abc4c…`; `lead-security` / `key-grc-seat-lead-security-0001` /
      `sha256:71976b6c…`; `lead-quality` / `key-grc-seat-lead-quality-0001` /
      `sha256:e76138bb…`; `company-policy-lead` /
      `key-grc-seat-company-policy-lead-0001` / `sha256:72a6fea0…`. All four
      adjudicated and resolved by the pinned reader (`8 of 8`), no
      `register-seat-duplicate` despite three seat ids now appearing twice, and
      `validate-factory-identity.py` reports **`0 shared`** identifiers across
      the two registers (4 here, 46 there).
- [x] 3.8 Run the gate LOCALLY before pushing:
      `python3 openXwallet/scripts/validate-openxwallet.py .` must be clean, and
      the log must say `intake register read: … (2 row(s))` and
      `intake register: 8 of 8 per-seat signing key(s) adjudicated and resolved`.
      BASELINE RECORDED BEFORE THE EDIT (the walk cites a before/after): at
      `origin/main` `6a09a2d4` with the submodule at `f3eb929b` /
      `wallet-v1.5`, `verify-openxwallet-pin.py` OK (8 digests recomputed),
      `wallet-yaml-syntax-gate.py` rc=0, and `validate-openxwallet.py .`
      **0 error(s), 0 warning(s)** with `intake register read: … (1 row(s))`
      and `intake register: 4 of 4 …`. AFTER: pending Brett's values — the
      validator refuses `@@…@@` placeholders by shape, which is the reader
      working as designed and is NOT to be worked around with stand-in values.
      SHAPE PROBE ALREADY RUN AGAINST THE REAL READER, and it discharges the
      mint runbook's precondition 1 empirically rather than by argument. On the
      placeholder tree the reader emits
      `intake register read: … (**2 row(s)**)` — no
      `register-minimal-shape-exceeded` — and
      `wallet 'wal-agent-grc-0001': **5** declared key(s) adjudicated
      (key-grc-0001, key-grc-seat-company-policy-lead-0001,
      key-grc-seat-lead-architect-0001, key-grc-seat-lead-quality-0001,
      key-grc-seat-lead-security-0001)`, which is exactly the line 2.8's new
      assertion greps for. It counts EIGHT seat entries (`4 of 8` resolved) and
      raises **no** `register-seat-duplicate` despite `lead-security`,
      `lead-quality` and `company-policy-lead` each appearing twice. All 35
      errors are placeholder-shape and nothing else — 21 `[schema]`, 4
      `[register-seat-key-malformed]`, 4 `[register-seat-fingerprint-malformed]`,
      4 `[declared-key-fingerprint-mismatch]`, 1 `[attestation-malformed]`
      (`verified_at is not an RFC3339 timestamp`) and the
      `[register-tier-act-unattested]` that follows from it. **No structural
      finding.**
      DONE 2026-09-08 — **AFTER, on the filled tree, branch
      `act/register-act-grc-0001` at base `6a09a2d4` (deliberately NOT merged
      forward, so the only difference from the baseline is this act), run from
      the worktree root with `set -o pipefail`.** The two literal lines the task
      names, verbatim from `wallet-gate.log`:

          note  intake register read: governance/review-authority/register.yaml (2 row(s))
          note  intake register: 8 of 8 per-seat signing key(s) adjudicated and resolved

      plus `note  wallet 'wal-agent-grc-0001': 5 declared key(s) adjudicated
      (key-grc-0001, key-grc-seat-company-policy-lead-0001,
      key-grc-seat-lead-architect-0001, key-grc-seat-lead-quality-0001,
      key-grc-seat-lead-security-0001)`, `note  repo scan: 9 openxWallet
      artifact(s) validated, 2120 document(s) skipped as another kind`, and
      `validate-openxwallet: 0 error(s), 0 warning(s)`. **NO `[register-*]`
      line** (`grep -c '[register-' wallet-gate.log` = 0).
      **`--strict` rc 0**, 0 error(s) 0 warning(s). Also green on the same tree:
      `verify-openxwallet-pin.py` (openXwallet@`f3eb929b`, tag label
      `wallet-v1.5`, 8 digests recomputed) rc 0;
      `wallet-yaml-syntax-gate.py .` rc 0; `validate-factory-identity.py .`
      rc 0 (`disjointness holds … 0 shared`).
- [x] 3.9 Record the walk: what each step produced, the citations the act is
      fixed at, the rulings as spoken, the honest limits — including that no
      gate-rules convening has ever run and that the seats are therefore
      registered and unexercised.
      EVIDENCE (PENDING VALUES): drafted at
      `openspec/changes/register-gate-rules-council-seats/walk-2026-09-08-register-act.md`
      (held at `walk-PENDING-register-act.md` until the date is known), in the
      form of `walk-2026-09-02-register-act.md`.
      DONE 2026-09-08: `openspec/changes/register-gate-rules-council-seats/
      walk-2026-09-08-register-act.md` — renamed from
      `walk-PENDING-register-act.md` on the day it was actually walked, and
      completed in the 2026-09-02 precedent's form. It carries § 0 the headline;
      § 1 what each step produced; § 2 the five preconditions; § 3 the roster
      read before minting; **§ 3A the four citations the act is fixed at, each
      OPENED AND READ** (the ratification `review/ratification-2026-09-06.md`;
      the R1/R2 amendment in `proposal.md` / PR #751; codexFactory
      `records/2026-09-07-gate-rules-roster-lead-architect-pin.md`; the signed
      `operator-identity-record-2026-09-01.md`); **§ 3B the mint itself** — the
      program, the command log and the custody timeline; § 4 the acts verbatim
      with THE RULINGS AS SPOKEN including B2; § 5 the gate before/after and
      **§ 5.1 the consuming gate's 13 assertions replayed**; § 6 the capacity
      disclosure; § 7 the projection NOT performed; § 8 the honest limits
      (LQ-C1..C4 and LQ-A1 carried, no gate-rules convening has EVER run, the
      seats are REGISTERED AND UNEXERCISED, the projection is not refreshed by
      this act, the four secrets are read presence-only, the mint program is in
      no repository, the root seed's 8h10m screen window) and the runbook's own
      mandatory sentence: "It does not enforce itself. No gate in this estate
      refuses a register act that skips this document." Effective instant
      `2026-09-08T12:31:36Z`, following the predecessor's definition of that
      field exactly — one instant taken once, written into the grant's
      `issued_at` and the wallet's `declared_at`/`created_at`; NOT the merge
      instant.
- [x] 3.10 **Gate:** the pull request carrying §3 is GREEN on
      `wallet-validation`, and it is human-landed by construction — the register
      is a never-clearable floor member and no council verdict clears it.
      DONE 2026-09-08: §3 landed as openxFactory PR #798 → merge commit
      `eea40d17` (2026-09-08T14:17Z), **9/9 checks pass** including
      `wallet-validation` and `pytest-suite`. **Human-landed**: the register
      is the never-clearable floor member per this gate's own text, and #798
      was landed via OrganizationAdmin bypass on Brett Heap's word ("merge
      both") — not by a council verdict. Rule 6 posted on the PR: LANDING
      `14:17:14Z`, LANDED `14:17:23Z`. Companion codexFactory mint record
      landed as codexFactory PR #290 → merge commit `c7b4d96b`.

## 4. Downstream owed acts — named with owners, not discharged here

- [x] 4.1 **[OPERATOR] / [hermes-install]** Refresh the register projection
      after §3 lands: the next `hermes-register-projection-refresher` tick, or a
      manual `project-register` run against the merged revision. The visible
      signal is `seat_count` 4 → 8 and `councils` gaining `gate_rules_council`.
      **Until it is re-derived the runtime keeps refusing with
      `review_authority.root_key_mismatch` and no authority flows.** Nothing in
      hermes-install needs a code change: `derive_projection` already keys on
      `(council_id, seat_id)` and already reports `councils` as a set.
      DONE 2026-09-09: Brett Heap's operator read, in-session, verbatim
      "source-revision is 68712924, seat_count 8" — the AKS QA
      `hermes-register-projection` ConfigMap annotations. Rule 2 record:
      https://github.com/opensoft/openxFactory/pull/717#issuecomment-5593896064.
      seat_count 4 → 8; `councils` now `[gate_rules_council,
      merge_readiness_council]`. Refreshed on a SCHEDULED tick of
      `CronJob/hermes-register-projection-refresher` — no manual Job was run.
      Companion: hermes-install PR #74 → merge commit `985f5027` (feature 022:
      two-council fixture at openxFactory 68712924, byte-exact expected
      projection, +22 tests, evidence doc
      `docs/evidence/register-projection-refresh-2026-09-08.md`); zero
      production lines — the refresher already resolved openxFactory's
      default-branch head each tick, and derivation was already council-aware
      on `(council_id, seat_id)`. The projection now carries 8 seats.
- [x] 4.2 **[hermes-install]** Observe a SCHEDULED refresher firing. Already on
      that repository's follow-up list; only a manual migration job is on record
      to date, so the standing manual re-projection duty is not retired by this
      change.
      DONE 2026-09-09: the refresh recorded under 4.1 IS that observation —
      Brett Heap's operator read of the AKS QA `hermes-register-projection`
      ConfigMap annotations (source-revision 68712924, seat_count 8) reflects
      a refresh driven by a SCHEDULED tick of
      `CronJob/hermes-register-projection-refresher`, not a manual Job. The
      standing manual re-projection duty remains not retired by this change
      (unchanged).
- [x] 4.3 **[codexFactory]** Close the floor-reachability gap this change WIDENS
      (design D6): `governance/review-authority/{grants,wallets,attestations}/`
      are not named in
      `scripts/merge_master/openxfactory-review-authority-floor.yaml`, and §3
      adds three files there — one of them the grant conferring the rule-setting
      body's own authority. Pre-existing per `split-openxwallet-repo` §8.3 with
      lead-security's 2026-08-26 finding standing; **owner: the arc owner of
      `add-wallet-carried-review-authority`.** Not closed by this change and not
      inferable from the register's own floor entry.
      **OWNER, RULED 2026-10-07 — NOT TICKED.** RULED 2026-10-07 by Brett Heap,
      first-hand in lane codeXfactory-2's session (multiple choice; he selected
      'This lane'). He was asked as a multiple-choice question with a
      recommendation, at his own request (*"ask the decisions by me in multi
      choice with recomendations"*), and selected the recommended option.
      **Lane codeXfactory-2 owns this gap.** That REPLACES "the arc owner of
      `add-wallet-carried-review-authority`" in the row above as the ACTING
      owner; the arc's design ownership is unchanged. **The codexFactory fix is
      draft PR codeXfactory/codexFactory#534** (read 2026-10-08: OPEN, DRAFT,
      head `ac615fbc9bc5f68c7122f5b0f69d8bad832b6fc3`, authored by this lane),
      which floors the register's own records by name. The row stays `[ ]`: it
      asks for the gap to be CLOSED, a ruling on who owns it closes nothing, and
      #534 is unmerged. This note records ownership and names the fix. It does
      not re-measure the gap, edits no codexFactory file, and does not move this
      row into or out of the archive gate (§ 5.2 stands as written). The row's
      own "owner:" words above are not edited. See the walk's § 13.6
      bookkeeping note 3 (appended 2026-10-07).
      **DONE 2026-10-08 — TICKED: THE GAP IS CLOSED BY TWO MERGES, AND A
      NARROWER RESIDUAL IS OWNED.** Bookkeeping tick only: the work is another
      repository's and no openxFactory byte moves for it beyond the re-pin
      below. (1) **codeXfactory/codexFactory PR #534 →
      `ce9236363d044bc6d8cf9b9f7a5bd15ecaff9559`**, merged 2026-10-08T21:35:33Z
      on Brett Heap's word *"Land when green after fixes (Recommended)"*.
      codexFactory's floor (`floor/openxfactory-review-authority-floor.yaml`)
      now names BY NAME the nine records under `governance/review-authority/`
      this row said it omitted: two wallets, five grants and two custody
      attestations. It is anchored on the ratified requirement this change
      carries, `specs/review-authority-intake/spec.md:90-98` (the records
      *"SHALL be entered there BY NAME"*), with this row and design D6 as the
      secondary cite. (2) **openxFactory PR #1277 →
      `40d6e5c1bbed6fb976e7933200236e353777ee47`**, merged
      2026-10-08T23:15:55Z, the review-lane re-pin that makes (1) effective
      here: `contracts/review-lane-pin.yaml` `core_commit` →
      `ce9236363d044bc6d8cf9b9f7a5bd15ecaff9559`, and the vendored floor
      snapshot's `sha256` → `9a42e76f…` and `entry_count` 75 → 84. #534's own
      description says the change is inert for openxFactory until that re-pin
      lands. Read at `40d6e5c1b`, the pin and the snapshot carry those values
      and the snapshot lists all nine paths. **No convening is owed**: Brett
      Heap, 2026-10-08, first-hand, *"No convening owed (Recommended)"*,
      because the ratified requirement already mandates the act (cxF #279
      comment `6066532414`). The tick itself is the lane's on his word *"Merge
      #1277 when green"*, whose option text said *"Then this lane ticks
      Q-GRC-4 task 4.3 in openxFactory, citing both merges"* (as relayed by
      the lane coordinator). **THE RESIDUAL, OWNED BY LANE codeXfactory-2 AS
      FOLLOW-UPS** (*"This lane, as follow-ups (Recommended)"*, 2026-10-08,
      noted on #279): the floor is an ENUMERATION, so a record ADDED later
      under these directories is unfloored until it is named, and #534's
      independent review left two latent gaps: the pinned reader keeps only the
      last attestation per wallet (opensoft/openXwallet#29), and the opt-in
      floor check measures only at the floor block's own pin
      (codeXfactory/codexFactory#536). Both were OPEN when read 2026-10-08.
      This tick does not close them. The 2026-10-07 OWNER note above stays as
      written, and this tick supersedes its "NOT TICKED". § 5.2 stands: § 4
      is outside the archive gate. See the walk's § 13.6 bookkeeping note 4
      (appended 2026-10-08).
- [ ] 4.4 **[codexFactory]** The CALLER (task 5.9a): a convening path that seats
      `gate_rules_council`, resolves its seats from the projection and returns
      SIGNED seat returns. The roster says in terms that the missing piece is a
      caller, and that a definition-time council must not be evaluated against
      per-PR facts to close the gap.
- [ ] 4.5 **[codexFactory] / [hermes-install]** The FIRST SIGNED gate-rules
      convening. This is what makes the queuing ruling's *"so later convenings
      are signed"* true. It is the arc's gate and it is NOT this change's to
      perform.
- [ ] 4.6 **[codexFactory]** When the subject-layer roster binds
      `intent_owner_role_slot`, or when the roster gives
      `client-security-compliance-officer` a seat identifier, register that
      seat's key IN THE SAME GOVERNED ACT (Q-GRC-4), so the first convening that
      seats it is not the one that discovers a missing key.

## 5. Archive gate

- [x] 5.1 `code_surface` is NOT `none`, so per `release-realization` this change
      archives only on MERGED, GREEN REALIZATION EVIDENCE. The evidence set is
      exactly:
      - §2.7 + §2.8 merged and `wallet-validation` green at the advanced pin
        with the register still at one row (§2.9);
      - §3 merged and `wallet-validation` green with the log reading
        `2 row(s)` and `8 of 8 per-seat signing key(s) adjudicated and
        resolved`;
      - the walk record (§3.9) committed;
      - §1.2–§1.5 ruled and recorded.
      **DONE 2026-10-05, each of the four items read against what landed. Two
      things to read with it, stated and not reworded.** (1) THE LITERAL `8 of
      8` IS SUPERSEDED BY `9 of 9`. T2 (oxF PR #1006 → `765d8c6f`,
      2026-09-13T22:30:20Z) added the fifth gate-rules seat key, so the log on
      `main` now reads `2 row(s)` (unchanged: a seat is not a holder, walk §
      5.3) and `9 of 9 per-seat signing key(s) adjudicated and resolved` (walk §
      13.6 bookkeeping note). The bullet's text is not edited. (2) THE FIRST
      ITEM'S ORDER WAS RE-SEQUENCED by `proposal.md`'s 2026-09-07 AMENDMENT
      (newest, and governing, as § 2.8's own DONE note says): §2.8's literal
      flip was deferred out of the pin-advance PR and performed in the register
      act, so "§2.7 + §2.8 merged ... with the register still at one row" never
      held as one state. §2.9, ticked above, is the gate that was kept: the pin
      advance neutral at one row. **The evidence.** Each measurement was taken
      on the landed commit, with the reader the gitlink names there (`f3eb929b`
      at all three). **Item 1, §2.7:** oxF PR #740 → `30eccf0ca` (merged
      2026-09-07T02:00:32Z), `wallet-validation` and `pytest-suite` SUCCESS; the
      reader on `30eccf0ca` reads `1 row(s)`, `4 of 4`, `0 error(s), 0
      warning(s)` (§2.9). §2.8 landed with the next item. **Item 2, §3:** oxF PR
      #798 → `eea40d175` (merged 2026-09-08T14:17:18Z by the `brettheap` login,
      on his word *"merge both"*, row 3.10), `wallet-validation` and
      `pytest-suite` SUCCESS on its head `85ca4c9a`; the reader on `eea40d175`
      reads `2 row(s)`, `8 of 8`, `0 error(s), 0 warning(s)`, no `[register-`
      line. **Item 3, the walk record:** `walk-2026-09-08-register-act.md` is in
      `eea40d175`'s tree (972 lines, the same merge). **Item 4, §1.2–§1.5:**
      rows 1.2–1.5 above, each RULED 2026-09-06T14:13:46Z and recorded in
      `review/ratification-2026-09-06.md`. For the current state, the reader at
      T2 (`765d8c6f`) reads `2 row(s)`, `9 of 9`, `0 error(s), 0 warning(s)`.
      See walk-2026-09-12-register-act.md § 13.6 bookkeeping note 2 (appended
      2026-10-05).**
- [ ] 5.2 §4 is EXPLICITLY OUT of the archive gate and must not be folded into
      it. Those acts belong to other repositories and other owners; holding this
      change open on a convening nobody can yet run would park the register act
      indefinitely, and ticking them from here would tick another repository's
      boxes.
- [ ] 5.3 Before archive, re-read the seat list against codexFactory
      `hermes/domain/review-councils/gate-rules.yaml` at the then-current
      `origin/main`. A roster that moved between ratification and realization
      means the registered set is stale, and a stale seat set records authority
      that no convening presents.
      **OPEN — NOT TICKED. DATED READING 2026-10-05 recorded beside it; to be
      re-run and ticked at archive.** The clause binds this row to "the
      then-current `origin/main`" at archive, and archive is blocked on the
      `sequenced_after` order, so a tick today would read as archive-time
      verification that has not happened. **The reading (2026-10-05,
      codexFactory `main` `cc85a3cc29caabb6a2894d3e935d1e965e84d007`; `gh api
      repos/codeXfactory/codexFactory/branches/main`, and the local
      `origin/main` is the same sha):** the five roster seats equal the
      register's five `gate_rules_council` seats, and `intent_owner_role_slot`
      is still deferred. In `hermes/domain/review-councils/gate-rules.yaml`,
      `council.members.domain` is `[lead-architect, lead-security,
      lead-quality]`; `members.client.seat` is `company-policy-lead`;
      `members.client.conjunction_pull_in.seat` is
      `client-security-compliance-officer` (`:203`; its former `deferred_seats`
      entry now sits in `discharged_seats`); `members.project.seat` is
      `intent_owner_role_slot` (`binding: symbolic_until_project_roster`), still
      the one `deferred_seats` entry. The register's `gate_rules_council`
      `seat_keys`, parsed from `register.yaml` at `20ce593e8`, are
      `lead-architect`, `lead-security`, `lead-quality`, `company-policy-lead`
      and `client-security-compliance-officer`: FIVE, set-equal to the roster's
      five declared seats, with `intent_owner_role_slot` the deferred sixth and
      unregistered (Q-GRC-4, task 4.6). `agent-mixes.yaml`'s
      `review_council_profiles.gate_rules_council` lists the same five in
      `all_possible_seats`, `model_assignments` and `prompt_contract.seats`. The
      registered set is not stale at that reading. **Re-run it against
      `origin/main` on the day of the archive and tick this row then, with
      `intent_owner_role_slot` the seat most likely to have moved.** See
      walk-2026-09-12-register-act.md § 13.6 bookkeeping note 2 (appended
      2026-10-05).**

**2026-10-07 — ARCHIVE ORDER RULED: THIS CHANGE WAITS FOR THE DECLARED
`sequenced_after` ORDER. NOTHING IN § 5 TICKS.** RULED 2026-10-07 by Brett
Heap, first-hand in lane codeXfactory-2's session (multiple choice; he selected
'Wait for declared order'). He was asked as a multiple-choice question with a
recommendation, at his own request (*"ask the decisions by me in multi choice
with recomendations"*), and selected the recommended option. Archive WAITS: this
change archives only after `add-wallet-carried-review-authority`, the member
`proposal.md:4` declares (`sequenced_after: [add-wallet-carried-review-authority,
openXwallet:widen-register-reader-for-a-second-council]`), and that change
itself waits on `add-substantive-review-lane` (its own "Archive-ordering note
(2026-09-05)": *"`add-substantive-review-lane` archives FIRST"*). Both are
still active at this note's base, `origin/main` `16779816`, and again at
`c9dfd4f88` (2026-10-08). 5.1 was ticked 2026-10-05, and 5.2 and 5.3 stay
`[ ]`. **5.3's archive-time re-read stays OPEN and is to be re-run against the
then-current `origin/main` on the day of the archive**, as its 2026-10-05 note
says; this ruling does not stand in for it and waives none of it. The ruling is
about WHEN to archive: it edits no row of this section, changes no part of 5.1's
evidence set, and moves no § 4 row into the gate (§ 5.2 stands). See the walk's
§ 13.6 bookkeeping note 3 (appended 2026-10-07).

---

## 6. Q-GRC-4 discharge (AMENDMENT 2026-09-11)

Lane: hermes-wallet-exercise

**ADDED BY AMENDMENT, 2026-09-11.** Record:
`review/amendment-2026-09-11-q-grc-4-discharge.md`. Rulings: Brett Heap, in
session, window `codeXfactory-2`, **2026-09-11T14:59:26Z**, verbatim
*"amend register-gate-rules-council-seats, lead-architect route, same model pin
as lead-security"*. Standing ruling this discharges: **`α, park C2 until
Q-GRC-4 is discharged`** — 2026-09-11T14:23:26Z, cxF #279 comment
[`5635898767`](https://github.com/codeXfactory/codexFactory/issues/279#issuecomment-5635898767).

**This group SPECIFIES task 4.6's owed act for ONE of its two seats** —
`client-security-compliance-officer`. `intent_owner_role_slot` stays deferred on
its own unchanged trigger and **4.6 does not tick** until both are discharged or
the packet's own successor re-scopes it. **§ 6 IS NOT AN ARCHIVE CONDITION** —
§ 5.2 already puts § 4 outside the archive gate, and 4.6 lives in § 4; § 6.9
restates it so a later reader does not fold this group in by reflex.

**6.1 AND 6.1a ARE NOW TICKED, AGAINST BRETT HEAP'S RATIFICATION WORD —
2026-09-11T17:08:42Z, verbatim *"accept all A on 971, merge slice 3 when
green"*, whose FIRST clause is this ruling, in session, window
`codeXfactory-2`, no comment URL. NOTHING ELSE BELOW IS TICKED, AND THE PULL
REQUEST THAT TICKS THEM PERFORMS NO OTHER ACT.** 6.1b stays open — the seat
identifier string is an authoring decision flagged for VETO, not one of the five
questions the word ruled, so it still owes its own confirmation before 6.2.
Nothing below 6.1a is authored by that pull request either: **H1 is built AFTER
ratification, through Speckit, in codexFactory; H2 is Brett's operator act on a
permanently human-only surface.** OQ-1..OQ-5 are RULED at option **(a)**
throughout, and the rows that named an OQ as undecided now name its ruled
value: 6.8 (OQ-1), 6.10 (OQ-2), 6.6 (OQ-3), 6.18 (OQ-4), 6.24 (OQ-5).

**2026-09-12 — WHAT THE H2 PRE-STAGE PULL REQUEST TICKS, AND WHAT IT
DELIBERATELY DOES NOT.** T1 has landed (codexFactory PR #439 →
`eff9ae191d78c396800a72cdec9fffe0caf866d7`, 2026-09-12T15:59:10Z) and the H2
pull request is composed and PRE-STAGED on `register/q-grc-4-h2-grant-grc-0003`.

**TICKED, each against landed evidence:** **6.1b** (Brett Heap's
2026-09-12T03:23:17Z word), **6.2-6.7** (H1, realized by #439), **6.16** (the
hold, posted 15:57:19Z) and **6.17** (T1 itself).

**NOT TICKED, and each for its own reason:**

* ~~**6.8 — THE MINT HAS NOT HAPPENED.** It is Brett Heap's host-side act and
  it is the **PRECONDITION** of everything below. The H2 pull request carries
  ONE PLACEHOLDER where the public half goes and **cannot merge until it is
  filled**; its five slots and the fill recipe are
  `walk-2026-09-12-register-act.md` § 6.3.~~ **IT HAS SINCE HAPPENED AND 6.8
  IS TICKED** — see the 2026-09-13 note below. The line is struck rather than
  deleted, so the state this block was written in stays legible.
* **6.9-6.15 — COMPOSED BUT NOT PERFORMED.** The bytes exist on the branch; an
  act is performed when it lands. These tick at T2, in the merge commit or
  immediately after it — never at draft.
* **6.18-6.26 — the ceremony after T2**, in order, none of them started.
* **6.27 / 6.28 — bookkeeping this group does not do**, unchanged.

Rule 1 `CLAIMED` and Rule 6 `LANDING`/`LANDED` are owed **AT LANDING**, per
6.28, and none is posted at draft.

**2026-09-13 — WHAT THE FILL COMMIT CHANGES ABOUT THE BLOCK ABOVE.** The block
above describes the act as it stood PRE-STAGED on 2026-09-12 and is left
standing in that tense. ONE row of it has moved since: **6.8 IS NOW TICKED.**
Brett Heap minted the fifth keypair host-side and the secret
`COUNCIL_SEAT_SIGNING_KEY_GRC_CLIENT_SECURITY_COMPLIANCE_OFFICER` was
provisioned in codexFactory's `worker-credentials` environment at
**2026-09-13T02:12:15Z**; the public half is published in the codexFactory mint
record (**cxF PR #452**) and written into this act's five slots by the fill
commit, derived through the pinned decoder alone. The REQUIRED
`wallet-validation` gate now reads `0 error(s), 0 warning(s)`,
`9 of 9 per-seat signing key(s)` and `6 declared key(s)`. The act's effective
instant was RE-STAMPED at the fill, `2026-09-12T16:33:01Z` →
`2026-09-13T02:20:48Z`, under walk record § 6.3 step 2 (the fill was not
same-day). **NOTHING ELSE MOVED:** 6.9-6.15 and 6.18 still tick at T2 and
6.19-6.28 are still untouched, exactly as the block above says. The merge is
still Brett Heap's, and the merge is T2.

**2026-10-04 — BOOKKEEPING: WHAT T2 TICKED, AND THE TWO ROWS IT DID NOT.** The
two blocks above stay in the tense they were written in. T2 landed
2026-09-13T22:30:20Z (oxF PR #1006 → `765d8c6f`, Brett Heap's word *"merge
1006"*), and §§ 13.1–13.5 have since been booked. **6.9–6.14 are now ticked**
against T2. **6.15 and 6.18 are not**: each has a dated note naming the one
clause the landed record does not meet. See the walk record's § 13.6
bookkeeping note (appended 2026-10-04).

### 6.1 Governance

- [x] 6.1 **[OPERATOR] [GOVERNANCE]** Ratify this amendment, or return it.
      Nothing in §§ 6.2-6.10 is legal until this is ticked. **Ratification
      REALIZES NOTHING** — no seat is bound, no key is minted, no grant moves.
      **RATIFIED** — Brett Heap, in session, window `codeXfactory-2`, no
      comment URL, **2026-09-11T17:08:42Z**, verbatim *"accept all A on 971,
      merge slice 3 when green"*, whose FIRST clause is this ruling. The
      ratification's own record is
      `review/ratification-2026-09-11-amendment-2.md` (`Status: ratified`, one
      `Ratified:` citation) with its gate capture beside it at
      `review/verification-2026-09-11-amendment-2.md`; the amendment record
      keeps `Status: record` and gains one ADDED `Ratification:` header line,
      because a record's header states the act that MADE it and an amendment
      adds a line rather than rewriting one (amendment record § 8).
      §§ 6.2-6.10 are now legal to BUILD **subject to 6.1b, which is still
      open and still gates 6.2**: ratification lifted the 6.1 bar, not that one,
      and the seat identifier string owes its confirmation BEFORE 6.2 exactly as
      6.1b says. Nothing in §§ 6.2-6.10 has been performed.
- [x] 6.1a **[OPERATOR] [GOVERNANCE]** Rule **OQ-1..OQ-5** (amendment record
      § 9): the minter of the fifth keypair; `grant-grc-0003`'s `expires_at`;
      whether the CSC briefing owes a soak or an `activation_gate` pass before
      sitting live; one T1/T2 PR pair or a further split; whether C2 doubles as
      the seat's first live convening. **Every recommendation is what this
      packet already encodes, so taking all five moves no byte** — in which case
      this row ticks with that as its reason. **RULED, ALL FIVE AT OPTION (a),
      THE RECOMMENDED ONE, AND THAT IS EXACTLY THE REASON THIS ROW TICKS** —
      Brett Heap, in session, window `codeXfactory-2`, no
      comment URL, **2026-09-11T17:08:42Z**, verbatim *"accept all A on 971,
      merge slice 3 when green"*, whose FIRST clause is this ruling:
      **OQ-1 (a)** Brett Heap mints and holds the fifth keypair host-side, the
      task 3.2 ceremony generalized to one seat — fresh and TTY-gated,
      `holder_readable`, secret
      `COUNCIL_SEAT_SIGNING_KEY_GRC_CLIENT_SECURITY_COMPLIANCE_OFFICER`;
      **OQ-2 (a)** `grant-grc-0003`'s `expires_at` is `2027-06-30T00:00:00Z`,
      unchanged; **OQ-3 (a)** bind now, soak later — the lead-architect
      precedent, no soak and no `activation_gate` pass gating the binding;
      **OQ-4 (a)** the T1/T2 PAIR, one codexFactory pull request then one
      openxFactory pull request; **OQ-5 (a)** a SEPARATE proof convening
      precedes C2, on a re-verified clean candidate. Encoded at
      `proposal.md` § AMENDMENT — 2026-09-11 (§ Rulings table), `design.md`
      D8-D12, and the record § 9; **the spec delta moved no byte.**
- [x] 6.1b **[GOVERNANCE]** The seat identifier string
      `client-security-compliance-officer` is an AUTHORING decision flagged for
      veto, not a ruling (amendment record § 4). Confirm or replace it BEFORE
      6.2 — it is written into six places and a late change is six edits plus a
      re-mint of the secret name.
      **CONFIRMED — NOT VETOED.** Brett Heap, in session, window
      `codeXfactory-2`, no comment URL, **2026-09-12T03:23:17Z**, verbatim:
      *"confirm client-security-compliance-officer, proceed with T1"*. The
      string stands in all six places and the secret name
      `COUNCIL_SEAT_SIGNING_KEY_GRC_CLIENT_SECURITY_COMPLIANCE_OFFICER` stands
      with it. **The disposition PRECEDED 6.2's landing** — the word was given
      at 03:23:17Z and T1 merged at 15:59:10Z — so the bar this row set
      ("confirm or replace it BEFORE 6.2") was met in the order it required and
      not ratified after the fact. Ticked here, in the H2 cycle, because the
      word was spoken in a codexFactory session and this is the first
      openxFactory act that follows it.

### 6.2 H1 — the codexFactory roster act (built via Speckit, after 6.1)

- [x] 6.2 **[codexFactory]** `hermes/domain/review-councils/gate-rules.yaml`:
      add `seat: client-security-compliance-officer` beside `persona:` under
      `members.client.conjunction_pull_in` (`:152-161` @ `a990cba5`). This is
      the edit `scripts/merge_master/seat_resolution.py:566`
      (`seat = pull_in.get("seat")`) reads, and the ONLY one that moves `:582`'s
      `seat_identity` from `UNBOUND` to `declared`.
      **DONE — LANDED AT T1**, codexFactory PR #439 → `eff9ae191d78c396800a72cdec9fffe0caf866d7`, merged
      2026-09-12T15:59:10Z. The key sits at `gate-rules.yaml:203`. Measured,
      not asserted: against the real C2 subject the resolver answers
      `unbound_conjunction_seats: []`, `seat_identity: "declared"`,
      `unbound_why: null` — it answered `UNBOUND` on the same subject before.
- [x] 6.3 **[codexFactory]** Same file: rewrite the `deferred_seats` CSC entry
      (`:100-114`) as a DISCHARGED entry pointing at 6.6's record — **do not
      delete it silently**, per its own block comment (`:92-93`).
      `intent_owner_role_slot` (`:115-126`) stays byte-identical.
      **DONE AT T1** (`eff9ae191d78c396800a72cdec9fffe0caf866d7`). The entry RELOCATED to a new
      `discharged_seats` sibling carrying its original `why` verbatim plus
      `discharged_on: "2026-09-12"` and a `discharged_by` naming Amendment 2
      and Brett Heap's 2026-09-11T14:59:26Z ruling — **not deleted**.
      `intent_owner_role_slot` stays deferred, byte-identical.
- [x] 6.4 **[codexFactory]** `hermes/domain/agent-mixes.yaml`, profile
      `gate_rules_council`: add the identifier to `all_possible_seats`
      (`:271-275`) and rewrite the Q-GRC-4 comment above it (`:251-270`) to
      record the discharge; add the `model_assignments` entry (`:312-372`) with
      `selector: claude-opus-5`, `selector_kind: exact_provider_version`,
      `pin_status: pinned` COPIED FIELD BY FIELD from `lead-security` (`:334-336`)
      under ruling (3), `authority_layer: domain`, and an `authority_ref` naming
      **6.6's own record** in `lead-architect`'s shape (`:327-328`) — **never
      `lead-security`'s `authority_ref` (`:338-339`), which points at the
      enrolled merge-readiness roster and would attribute this pin to an act
      that never made it.**
      **DONE AT T1** (`eff9ae191d78c396800a72cdec9fffe0caf866d7`). `all_possible_seats` 4 → 5; the
      `model_assignments` entry carries `selector: claude-opus-5`,
      `selector_kind: exact_provider_version`, `pin_status: pinned` (copied
      field by field from `lead-security`), `authority_layer: domain`, and
      `authority_ref: hermes/domain/review-councils/records/2026-09-12-gate-rules-roster-csc-pin.md#operator-ruling-q-grc-4-discharge`
      — **correctly UNCOPIED**, which is the half **LQ2-C1** names as making a
      citation of this pin lawful.
- [x] 6.5 **[codexFactory]** Same file: add the identifier to
      `prompt_contract.seats` (`:378-382`) and **WRITE the seat's briefing** as
      a new entry in `.github/workflows/scripts/deliberation_packet.py`'s
      `GATE_RULES_SEAT_FOCUS` (`:225-258`). **There is nothing to copy** — the
      other four were written from what this body's convenings charged them with
      (`agent-mixes.yaml:390-394`) and CSC has never sat; the only raw material
      is the tenant's own specialization
      (`hermes/client/role-overrides.yaml:83-88`). Then re-pin the digests
      (`:445-467`): recompute `rendered_set_digest` from the LIVE RENDER over
      all five seats in LEXICOGRAPHIC order (`client-security-…` sorts FIRST, so
      every byte after it shifts and the digest cannot be patched), add the
      fifth `seat_digests` entry, advance `pinned_on` and set
      `previously_pinned_on: "2026-09-10"`.
      **DONE AT T1** (`eff9ae191d78c396800a72cdec9fffe0caf866d7`). `rendered_set_digest`
      `sha256:aac9b60e…` → **`sha256:0ea5f7afd8a55f286129206470ab4ad377ac73535644f95fc3811515a44321ad`**;
      fifth entry
      `client-security-compliance-officer: sha256:09d59e06a9fb6d2bca9caa5c27e407f9a28e5a0962682b12d99dbd00409487f2`;
      `pinned_on: "2026-09-12"`, `previously_pinned_on: "2026-09-10"`. **The
      four pre-existing seat digests are byte-identical**, which is the proof
      that nothing but the new entry entered the set.
- [x] 6.6 **[codexFactory]** Write the `roster_change: lead_accepted_recorded`
      record at
      `hermes/domain/review-councils/records/<date>-gate-rules-roster-csc-pin.md`
      in R1's shape
      (`records/2026-09-07-gate-rules-roster-lead-architect-pin.md`): § 0 no
      seat was convened; § 2 the ruling verbatim with its UTC; § 3 the roster
      this fixes, **recording that the 2:2 opus/sonnet split becomes 3:2**; § 5
      **no comparative claim — no soak has run on this bench or this seat**;
      § 6 **Lead Quality's acceptance, OWED, at `claude-sonnet-5`, as an actual
      seat return**; § 7 C13 re-opens the soak from zero and costs nothing today
      (`agent-mixes.yaml:299-305`). Carry LQ-C4's `tool_manifest` bound onto the
      new seat unchanged. **OQ-3 RULED (a) — BIND NOW, SOAK LATER**
      (2026-09-11T17:08:42Z): the soak is OWED and is **not** a precondition of
      binding, and no `gate_rules_council` `activation_gate` is declared (none
      exists). Nothing in §§ 6.16-6.26 waits on a soak row.
      **DONE AT T1** (`eff9ae191d78c396800a72cdec9fffe0caf866d7`) at
      `hermes/domain/review-councils/records/2026-09-12-gate-rules-roster-csc-pin.md`.
      § 6's OWED acceptance slot is DISCHARGED by a real seat return —
      `records/2026-09-12-seat-returns/lead-quality.md`, commit `7d7ee39a`,
      produced by `lead-quality` at its own pin `claude-sonnet-5` on Brett
      Heap's commissioning word of 2026-09-12T03:05:02Z. **Position: ACCEPT AS
      AMENDED**; five `should_fix` conditions **LQ2-C1..C5**, none blocking,
      **NONE discharged by their own recording — they are the convener's.** No
      condition required a pre-T1 change to H1.
- [x] 6.7 **[codexFactory]** Prove it, do not assert it: re-render all five
      seats and show `rendered_set_digest` matches the live render
      (`test_gate_rules_holder_composition.py`); prove digest coupling BOTH ways
      (edit-without-repin FAILS, edit-with-repin PASSES), as cxF PR #374 did;
      run `deliberation_packet.py resolved-seats` against a security-surface
      packet and record the output.
      **DONE AT T1** (`eff9ae191d78c396800a72cdec9fffe0caf866d7`). Against baseline `main` `3c31a2e4`:
      full pytest **+5 passed / +1 skipped** with the 163 pre-existing
      FAILED+ERROR ids byte-identical (all in
      `tests/browser-ui-repair/test_whole_chain_validation.py`, none ours); the
      three gate-rules test files **144 passed / 1 skipped**;
      `resolved-seats` on the real C2 subject returns
      `unbound_conjunction_seats: []` with CSC `seat_identity: "declared"`;
      validate-docs 5071/33 ok; openspec strict failure set = main's. All eight
      required and optional checks green on #439 at merge.
- [x] 6.8 **[OPERATOR]** Mint the fifth Ed25519 keypair (**OQ-1**): seed
      generated in-process and never written to disk, `gh secret set` on stdin
      with `--body` OMITTED, private half stored ONLY as
      `COUNCIL_SEAT_SIGNING_KEY_GRC_CLIENT_SECURITY_COMPLIANCE_OFFICER` in
      codexFactory's `worker-credentials` environment, custody
      `holder_readable` (**Q-GRC-1, already ruled 2026-09-06T14:13:46Z and never
      scoped to four seats**). Publish the PUBLIC half, the `did:key:` and the
      fingerprint in a codexFactory mint record mirroring
      `records/2026-09-08-gate-rules-seat-signing-keys-minted.md`. **No seed,
      ever, in any file.** **OQ-1 RULED (a) — BRETT HEAP MINTS AND HOLDS IT**,
      host-side, the task 3.2 ceremony generalized to one seat, as a FRESH
      TTY-gated ceremony and never a rerun of stored state
      (2026-09-11T17:08:42Z). (b) — minting through the committed
      `scripts/mint-factory-origin-key.py` — and (c) — a different custody model
      for this one key — are not taken.
      **DONE — Brett Heap, host-side.** Secret
      `COUNCIL_SEAT_SIGNING_KEY_GRC_CLIENT_SECURITY_COMPLIANCE_OFFICER`
      provisioned in `codeXfactory/codexFactory` environment
      `worker-credentials` at **`2026-09-13T02:12:15Z`** (the confirming
      `gh secret list` read). PUBLIC half published in the codexFactory mint
      record, **cxF PR #452** —
      `hermes/domain/review-councils/records/2026-09-12-gate-rules-seat-signing-key-minted-csc.md`:
      `public_key` `cxm-qmZVKXb_B5aucwuNzeOrXbgLPMKqa6D6DX1DUiQ`,
      `key_fingerprint` `sha256:85a4f47606f68a65be7c40f4abb392321d8bc6604ed7c27bef7418ac18df3310`,
      `did:key` `did:key:z6MknCZhXWq3KkPXubK4TTcKCSxXLfC3r2GBQ24Qcrwf9fp7`.
      Derived through the PINNED decoder only
      (`scripts/validate-factory-identity.py --derive`, openXwallet `f3eb929b`
      / `wallet-v1.5`) and written into the five slots of this act by the fill
      commit; `validate-openxwallet.py .` then reads `0 error(s)`,
      `9 of 9 per-seat signing key(s)` and `6 declared key(s)`. **No seed in any
      file.** FOOTNOTE: a first seed provisioned `2026-09-13T00:33:05Z` was
      DELETED UNUSED — its public half was lost to a swallowed non-TTY stdout,
      nothing ever registered or consumed it (walk record § 6.8). The act's
      effective instant was RE-STAMPED at the fill, `2026-09-12T16:33:01Z` →
      `2026-09-13T02:20:48Z`, under the walk record § 6.3 step 2 rule (the fill
      was not same-day).

### 6.3 H2 — the openxFactory register act (OPERATOR walk; no agent writes these)

- [x] 6.9 **[OPERATOR]** REVOKE `governance/review-authority/grants/grant-grc-0002.yaml`
      in place — `state: active` → `revoked`, plus `revocation.revoked_at` and a
      `revocation.reason` of class **DRIFT** whose free text names SEAT ADDITION
      (the 2026-09-11 precedent's named the prompt-corpus pin move). The
      revocation is unconditional and automatic: H1 landing is the composition
      event.
      **DONE 2026-09-13: LANDED AT T2. oxF PR #1006 →
      `765d8c6fcd3fbfdb71540903858e8fca74f04929`, merged 2026-09-13T22:30:20Z,
      on Brett Heap's word in session, verbatim *"merge 1006"*
      (2026-09-13T22:29Z; #1006 LANDING comment `5656603800`). `grant-grc-0002`
      is revoked IN PLACE: T2's diff appends a header block and the
      `revocation` block and changes one existing line, `state: active` →
      `state: revoked`. `revocation.revoked_at: "2026-09-13T02:20:48Z"` is the
      act's effective instant (re-stamped at the fill from
      2026-09-12T16:33:01Z). `revocation.reason` opens *"DRIFT: declared
      composition change — SEAT ADDITION."* and is 575 characters against the
      schema's 600 (re-measured 2026-10-04). The cause is T1 (`eff9ae19`,
      2026-09-12T15:59:10Z), and the grant has been void since then by
      declaration. The act is his. The bytes were composed by the lane and the
      merge keystroke was the lane's (walk § 7.2, § 13.3 mismatch (2)). See
      walk-2026-09-12-register-act.md § 5.1 and the § 13.6 bookkeeping note
      (appended 2026-10-04).**
- [x] 6.10 **[OPERATOR]** MINT `grants/grant-grc-0003.yaml` in
      `grant-grc-0002.yaml`'s shape — new `grant_id`, `state: active`,
      `issued_at` = the revocation instant, `issued_by` the ratifying human,
      `expires_at` **`2027-06-30T00:00:00Z`** — **OQ-2 RULED (a)**,
      2026-09-11T17:08:42Z: Q-GRC-3's date UNCHANGED, the date
      `grant-mrc-0002` still carries, so the two bodies' grants cannot
      silently diverge — scope re-examined rather than copied, and
      **no `parent_grant_ref`**: a superseding grant is a ROOT grant.
      **DONE 2026-09-13: LANDED AT T2. oxF PR #1006 →
      `765d8c6fcd3fbfdb71540903858e8fca74f04929`, merged 2026-09-13T22:30:20Z,
      on Brett Heap's word in session, verbatim *"merge 1006"*
      (2026-09-13T22:29Z; #1006 LANDING comment `5656603800`). New file
      `grant-grc-0003.yaml`: `grant_id: grant-grc-0003`, `state: active`,
      `issued_at: "2026-09-13T02:20:48Z"` (equal to `grant-grc-0002`'s
      `revocation.revoked_at`), `issued_by: Brett.Heap@opensoft.one`,
      `expires_at: "2027-06-30T00:00:00Z"` (OQ-2 (a)), and no
      `parent_grant_ref`, so it is a ROOT grant. Its key paths are the same as
      `grant-grc-0002`'s (parsed and compared 2026-10-04). The scope was
      re-examined rather than copied: each of its four elements carries its
      own reason in the grant's header section *"THE SCOPE — CARRIED FORWARD
      DELIBERATELY, EACH ELEMENT RE-EXAMINED"*. The act is his; the bytes and
      the keystroke were the lane's. See walk-2026-09-12-register-act.md § 5.2
      and the § 13.6 bookkeeping note (appended 2026-10-04).**
- [x] 6.11 **[OPERATOR]** REPOINT `governance/review-authority/register.yaml`
      `row-grc-0001` (`:182-190`): `grant_ref` → `grant-grc-0003` and nothing
      else. **NO second row** — D2's one-body-one-row shape is unchanged and a
      seat is not a holder.
      **DONE 2026-09-13: LANDED AT T2. oxF PR #1006 →
      `765d8c6fcd3fbfdb71540903858e8fca74f04929`, merged 2026-09-13T22:30:20Z,
      on Brett Heap's word in session, verbatim *"merge 1006"*
      (2026-09-13T22:29Z; #1006 LANDING comment `5656603800`). Parsing
      `register.yaml` at T2's first parent (`ee251d6c`) and at T2 shows
      `row-grc-0001` with one field changed: `grant_ref` `grant-grc-0002` →
      `grant-grc-0003`. `rows` still holds two entries of nine fields each,
      so no second row was added, and `row-mrc-0001` is unchanged. The act is
      his; the bytes and the keystroke were the lane's. See
      walk-2026-09-12-register-act.md § 5.3 and the § 13.6 bookkeeping note
      (appended 2026-10-04).**
- [x] 6.12 **[OPERATOR]** ADD the fifth `seat_keys` entry to `register.yaml`
      after `company-policy-lead` (`:358-364`), in the seven-field shape at
      `:333-339`: `seat_id: client-security-compliance-officer`,
      `council_ref: agent:gate-rules-council`,
      `council_id: gate_rules_council`,
      `key_id: key-grc-seat-client-security-compliance-officer-0001`,
      `public_key` VERBATIM from 6.8's mint record, `key_fingerprint`
      recomputed by the reader, `authorizing_row: row-grc-0001`.
      **DONE 2026-09-13: LANDED AT T2. oxF PR #1006 →
      `765d8c6fcd3fbfdb71540903858e8fca74f04929`, merged 2026-09-13T22:30:20Z,
      on Brett Heap's word in session, verbatim *"merge 1006"*
      (2026-09-13T22:29Z; #1006 LANDING comment `5656603800`). `seat_keys`
      goes from 8 to 9 entries and the first eight are unchanged. The ninth
      sits directly after the gate-rules `company-policy-lead` entry and has
      the seven fields: `seat_id: client-security-compliance-officer`,
      `council_ref: agent:gate-rules-council`,
      `council_id: gate_rules_council`,
      `key_id: key-grc-seat-client-security-compliance-officer-0001`,
      `public_key: cxm-qmZVKXb_B5aucwuNzeOrXbgLPMKqa6D6DX1DUiQ`,
      `key_fingerprint: sha256:85a4f47606f68a65be7c40f4abb392321d8bc6604ed7c27bef7418ac18df3310`,
      `authorizing_row: row-grc-0001`. The `public_key` is
      character-for-character the one in 6.8's mint record (cxF PR #452 →
      `58f1e909`). The pinned reader recomputes the fingerprint and resolves
      the entry. Re-run 2026-10-04 on oxF `main` `0e01ca85` at openXwallet
      `f3eb929b`, it reads `9 of 9 per-seat signing key(s) adjudicated and
      resolved` and `0 error(s), 0 warning(s)`. The act is his; the bytes and
      the keystroke were the lane's. See walk-2026-09-12-register-act.md § 5.4
      and the § 13.6 bookkeeping note (appended 2026-10-04).**
- [x] 6.13 **[OPERATOR]** ADD the fifth key to
      `governance/review-authority/wallets/wal-agent-grc-0001.yaml`'s `keys:`
      array in the entry shape at `:125-135` (`did`, `key_id`,
      `key_fingerprint` byte-identical to 6.12's, `public_key_multibase`,
      `signature_algorithm: ed25519`, `display_label`, `custody.model:
      holder_readable`), with `did`/multibase DERIVED through the PINNED
      decoders (`scripts/validate-factory-identity.py --derive`) and never a
      second tool. **BOTH places are required** — the pinned validator's rule
      (r) refuses a presenting key no wallet declares. Edit the block comment at
      `:114-124` to record the discharge, leaving `intent_owner_role_slot` named
      as still absent.
      **DONE 2026-09-13: LANDED AT T2. oxF PR #1006 →
      `765d8c6fcd3fbfdb71540903858e8fca74f04929`, merged 2026-09-13T22:30:20Z,
      on Brett Heap's word in session, verbatim *"merge 1006"*
      (2026-09-13T22:29Z; #1006 LANDING comment `5656603800`).
      `wal-agent-grc-0001.yaml` `keys:` goes from 4 to 5 entries, and the first
      four and `key_reference` are unchanged. The fifth has the same seven
      fields as the four above it: `did`
      `"did:key:z6MknCZhXWq3KkPXubK4TTcKCSxXLfC3r2GBQ24Qcrwf9fp7"`, `key_id`,
      a `key_fingerprint` byte-identical to 6.12's, `public_key_multibase`
      `z6MknCZhXWq3KkPXubK4TTcKCSxXLfC3r2GBQ24Qcrwf9fp7`,
      `signature_algorithm: ed25519`, `display_label`, and
      `custody.model: holder_readable`. The `did` and multibase were derived
      through `scripts/validate-factory-identity.py --derive` (walk § 6.8).
      The block comment records the discharge in an append-only
      `2026-09-12 ADDENDUM` inside the same comment block, citing cxF #439 →
      `eff9ae19`, and names `intent_owner_role_slot` as still deliberately
      absent; the original paragraph is left as written. Re-run 2026-10-04,
      the pinned reader reads `wal-agent-grc-0001': 6 declared key(s)
      adjudicated`. The act is his; the bytes and the keystroke were the
      lane's. See walk-2026-09-12-register-act.md § 5.5 and the § 13.6
      bookkeeping note (appended 2026-10-04).**
- [x] 6.14 **[OPERATOR]** Move `.github/workflows/openxwallet-consumer-gate.yml`'s
      LITERAL per-seat key-count assertion for this body from four to five **in
      the same act** — `code_surface` already requires it, *"because a wildcard
      there would let a register that lost a body pass the positive proof."*
      **DONE 2026-09-13: LANDED AT T2. oxF PR #1006 →
      `765d8c6fcd3fbfdb71540903858e8fca74f04929`, merged 2026-09-13T22:30:20Z,
      on Brett Heap's word in session, verbatim *"merge 1006"*
      (2026-09-13T22:29Z; #1006 LANDING comment `5656603800`). The literals
      moved in commit `764006df`, the same commit as the register and wallet
      writes: `8 of 8` → `9 of 9 per-seat signing key(s) adjudicated and
      resolved`, and `wal-agent-grc-0001': 5 declared key(s)` →
      `6 declared key(s)`. Both stay literal, and `wal-agent-mrc-0001` stays
      at `5`. `tests/openxwallet_consumer_gate/test_gate_invocation.py` moved
      with them (`test_the_nine_per_seat_keys_…`), and it passes 18 of 18 on
      re-run 2026-10-04. On "four to five": the gate has no per-body literal 4
      or 5. This body's seat keys go from four to five inside the two literals
      above, which is how the amendment record § 5 words it (*"This act takes
      the gate-rules half from four keys to five; the assertion that names the
      count moves with it, in H2's own commit."*). The act is his; the bytes
      and the keystroke were the lane's. See walk-2026-09-12-register-act.md
      § 5.6 and the § 13.6 bookkeeping note (appended 2026-10-04).**
- [x] 6.15 **[OPERATOR] / [lane]** Write ONE walk record at
      `walk-<T2-date>-register-act.md` (the holder's established home, task 3.9)
      carrying R8's five minimum fields, the runbook § 0.3 three-capacity
      disclosure, and — R6/R7 still PENDING — the composition recorded as
      declaring-commit plus digests by the 2026-09-11 walk's own method.
      **OPEN — NOTED 2026-10-04, NOT TICKED: one clause is not evidenced.**
      What landed at T2 (oxF PR #1006 → `765d8c6fcd3fbfdb71540903858e8fca74f04929`,
      2026-09-13T22:30:20Z, *"merge 1006"*) is ONE walk record for this act,
      `walk-2026-09-12-register-act.md`. It carries R8's five fields (§ 6),
      the § 0.3 capacity disclosure (§ 7: three capacities plus two
      machine-held), and the composition as declaring commit `eff9ae19` plus
      the six digests, by the 2026-09-11 walk's method (§§ 3.3, 6.1).
      MISSING: the path `walk-<T2-date>-register-act.md`. T2 fell on
      2026-09-13 and the file is named for 2026-09-12, the day it was walked.
      Walk § 6.8 calls this *"ONE NAMING TENSION, DISCLOSED AND NOT
      RESOLVED"* and leaves it to the ratifying human (*"The ratifying human
      may have Part C re-date it."*). Part C (§§ 13.1–13.5) did not re-date
      it, and no ruling either way is on record. This row ticks on Brett
      Heap's word accepting the walked-day name, or after a re-date he rules.
      See the walk's § 13.6 bookkeeping note (appended 2026-10-04).
      **DONE 2026-10-07 — TICKED ON BRETT HEAP'S WORD, ACCEPTING THE WALKED-DAY
      NAME.** RULED 2026-10-07 by Brett Heap, first-hand in lane
      codeXfactory-2's session (multiple choice; he selected 'Accept walked-day
      name'). He was asked as a multiple-choice question with a
      recommendation, at his own request (*"ask the decisions by me in multi
      choice with recomendations"*), and selected the recommended option. The
      walked-day name `walk-2026-09-12-register-act.md` is ACCEPTED as
      satisfying this row. That
      was the one clause the 2026-10-04 note above found not evidenced, and it
      is the naming tension walk § 6.8 left to the ratifying human. Every other
      clause was already evidenced in that note (R8's five fields § 6, the
      § 0.3 capacity disclosure § 7, the composition as declaring commit plus
      digests §§ 3.3 and 6.1) and is not re-checked here. No re-date was ruled
      or performed: the file is not renamed and the files that cite its path
      are not edited. The 2026-10-04 note above stays as written, and this tick
      supersedes its "NOT TICKED". See the walk's § 13.6 bookkeeping note 3
      (appended 2026-10-07).

### 6.4 The ceremony

- [x] 6.16 **[lane]** Post the **HOLD** on the tracking issue, the H1 pull
      request and `LANES.md` **BEFORE** the H1 merge (precedent cxF #374, hold
      posted 2026-09-10T23:20:38Z, ~14 minutes ahead of its own merge).
      **DONE — POSTED 2026-09-12T15:57:19Z**, codexFactory issue #279 comment
      [`5646989264`](https://github.com/codeXfactory/codexFactory/issues/279#issuecomment-5646989264),
      **one minute fifty-one seconds ahead of the T1 merge** and in the order
      Brett Heap's word required (*"merge H1 when green, post the hold first"*,
      2026-09-12T03:14:35Z). **THE HOLD IS IN FORCE**: no
      `agent:gate-rules-council` convening may be dispatched until the lift at
      6.21. Rule 6 landing window recorded as N/A — #439 touched no
      `openspec/changes/` path.
- [x] 6.17 **T1** — H1 merges on Brett's word. `grant-grc-0002` is void from
      that instant and `gate_rules_council` convenings park.
      **DONE — T1 = `2026-09-12T15:59:10Z`**, codexFactory PR #439 → `eff9ae191d78c396800a72cdec9fffe0caf866d7`.
      `grant-grc-0002` has been VOID since that instant, by the declared
      composition change itself and not by any later act. The body is parked
      under 6.16's hold. **The merge word: Brett Heap, 2026-09-12T03:14:35Z,
      verbatim *"merge H1 when green, post the hold first"*.**
- [x] 6.18 **T2** — H2 merges (6.9-6.15). **OQ-4 RULED (a)**,
      2026-09-11T17:08:42Z: **ONE T1/T2 PAIR** — one codexFactory pull request
      (H1, §§ 6.2-6.8) then one openxFactory pull request (H2, §§ 6.9-6.15).
      H1 is **not** split into separate mint / roster / composition pull
      requests; two remotes, ONE governed act, the hold spanning them.
      **OPEN — NOTED 2026-10-04, NOT TICKED: the merge is evidenced; the
      pair shape as written is not.** Evidenced: T2 is oxF PR #1006 →
      `765d8c6fcd3fbfdb71540903858e8fca74f04929`, merged 2026-09-13T22:30:20Z on
      Brett Heap's word *"merge 1006"* (2026-09-13T22:29Z). It is ONE
      openxFactory pull request carrying 6.9–6.15. The hold spanned T1 to T2:
      posted 2026-09-12T15:57:19Z, lifted 2026-09-14T09:10:05Z (walk § 13.3).
      MISSING: *"one codexFactory pull request (H1, §§ 6.2-6.8)"* and *"H1
      is not split into separate mint / roster / composition pull
      requests"*. The codexFactory half landed as TWO pull requests. H1 is
      cxF #439 → `eff9ae19` (6.2–6.7, T1). 6.8's mint record is cxF #452 →
      `58f1e909`, merged 2026-09-13T22:32:20Z, two minutes AFTER T2, on Brett
      Heap's word *"merge 452 when green"* (2026-09-13T02:15:52Z). The mint
      itself came after T1 (provisioned 2026-09-13T02:12:15Z). That is the
      shape OQ-4 option (b) named (*"mint record, roster act, composition
      re-pin as separate codexFactory PRs"*), which the ruling did not take.
      The packet does not agree with itself here: `proposal.md` lists the mint
      under H2, and the mint record calls itself *"the mint half of the T2
      register act"*. No word on record decides #439 + #452 against OQ-4
      (a). This row ticks on Brett Heap's word that it meets OQ-4 (a), or on
      a ruling that re-scopes the row. See the walk's § 13.6 bookkeeping note
      (appended 2026-10-04).
      **DONE 2026-10-07 — TICKED ON BRETT HEAP'S WORD, ACCEPTING THE DEVIATION
      AND NOTING IT.** RULED 2026-10-07 by Brett Heap, first-hand in lane
      codeXfactory-2's session (multiple choice; he selected 'Accept, note
      deviation'). He was asked as a multiple-choice question with a
      recommendation, at his own request (*"ask the decisions by me in multi
      choice with recomendations"*), and selected the recommended option. This
      is the word the 2026-10-04 note above said would close the row. **The
      deviation, noted, with every fact as the 2026-10-04 note read it:** (1) ONE
      hold spanned T1 to T2, posted 2026-09-12T15:57:19Z (6.16) and lifted
      2026-09-14T09:10:05Z (6.21; walk § 13.3). (2) ONE openxFactory H2, oxF PR
      #1006 → `765d8c6fcd3fbfdb71540903858e8fca74f04929`, carried 6.9 to 6.15.
      (3) The codexFactory half landed as H1, cxF PR #439 →
      `eff9ae191d78c396800a72cdec9fffe0caf866d7` (6.2 to 6.7, T1), PLUS 6.8's
      mint RECORD as its own pull request, cxF PR #452 → `58f1e909`, merged
      2026-09-13T22:32:20Z, two minutes after T2. **The governed act's shape
      held. Only the record of the mint landed separately.** The mint itself
      (secret provisioned 2026-09-13T02:12:15Z) came before T2; what landed
      after it is the record. The OQ-4 (a) text above is not edited and the row
      is not re-scoped: it ticks on his acceptance, with this deviation noted.
      With 6.15 ticked above, every row of 6.9-6.15, the range this row names,
      is now `[x]`. See the walk's § 13.6 bookkeeping note 3 (appended
      2026-10-07).
- [x] 6.19 **[lane]** The 3.8-equivalent window check: prove NO
      `gate_rules_council` convening ran between T1 and T2 —
      `gh run list --workflow gate-rules-convening-trigger.yml` cross-checked
      against `records/` commits in the window, by walk § 13.1's method.
      **DONE 2026-09-13T22:4xZ — walk-2026-09-12-register-act.md § 13.1
      (appended 2026-09-14). Finding: EMPTY.**
- [x] 6.20 **[OPERATOR WORD REQUIRED — NOT SELF-SERVE]** Step 5b: a read-only
      cluster read confirming the `hermes-register-projection` ConfigMap's
      `hermes.opensoft.one/source-revision` annotation is at or after T2's merge
      sha. **This is now RATIFIED, not merely dispositioned** —
      `amend-register-act-5b-projection-proof`, openxFactory PR #960 →
      `ac688c40`, ratified on Brett's word *"accept all A on 960"*
      (2026-09-11T13:09:12Z). **Do NOT attempt it via a convening dispatch**:
      the admission path reads the domain-content projection only, so an
      admitted convening returns a green result against a pre-act projection
      that reads exactly like the proof.
      **DONE 2026-09-14T08:56:47Z — walk-2026-09-12-register-act.md § 13.2
      (appended 2026-09-14): source-revision 96895259 ahead of T2 765d8c6f; by
      source revision only, three row-level fields OWED.**
- [x] 6.21 **[lane]** LIFT the hold, citing T2's merge commit and the
      walk-record path, and naming any wording mismatch as the precedent's lift
      text did.
      **DONE 2026-09-14T09:10:05Z — LIFTED on cxF #279 (5661634651), PR #439 (5661635340) and LANES.md (837c9e9); walk-2026-09-12-register-act.md § 13.3 (appended 2026-09-14). Three wording mismatches named, none reworded.**
- [x] 6.22 **[lane]** Re-run `deliberation_packet.py resolved-seats` against a
      security-surface-touching subject and **confirm
      `unbound_conjunction_seats` is EMPTY.** This is the concrete verification
      the whole act exists for, and it spends no pin.
      **DONE 2026-09-14T09:1xZ — resolved-seats against the C2 packet on cxF main 3cbb4bd9: five required seats, CSC seat_identity 'declared', unbound_conjunction_seats [] (α lifted); walk-2026-09-12-register-act.md § 13.4 pre-note (appended 2026-09-14). Proof-convening candidate handed to Brett: cxF #471 head 4a92ee67 on the 2026-09-09 packet (#279 5661759632).**

### 6.5 C2 unparks

- [x] 6.23 **[lane]** Re-select a CLEAN C2 dispatch candidate at that moment
      (heads and pins will have moved): `git merge-base --is-ancestor <T1> <head>`;
      `gh api .../commits/<head> --jq '.files[].filename'` (first-parent for
      merges) excluding `hermes/domain/agent-mixes.yaml` and
      `hermes/domain/review-councils/gate-rules.yaml`; confirm the pin was never
      previously convened; confirm the C2 packet (cxF PR #407 → `76f2e771`) is
      still in that candidate's tree.
      **DONE 2026-10-04T17:4xZ: SELECTED, NOT DISPATCHED. The candidate is cxF
      #470 head `cd5ee34082a63b59b4037a6732138602996a4f1f` (MERGED
      2026-09-14T08:55:47Z → `046e9c51`; `gh pr view` re-read
      2026-10-04T17:44:38Z, head unmoved). It was pre-selected in § 13.5's
      2026-09-15 pre-note and pre-screened clean on cxF main `bdbbdb82` (#279
      5734187903). Re-checked against cxF main `cb504bec`: single-parent; one
      file (`openspec/changes/realize-provenance-gated-autonomous-merge/tasks.md`),
      neither excluded path; T1 `eff9ae19` is an ancestor; the pin was never
      convened (the only post-T1 runs pinned `4a92ee67` and `926212af`); the
      C2 packet is in its tree (#407's text as amended by #446's LQ2-C4
      re-route, the same blob as main's); `resolved-seats` gives FIVE required
      seats, conjunction `required: true`, CSC `declared`,
      `unbound_conjunction_seats` `[]`. RE-VERIFY AT DISPATCH: 6.25 is Brett
      Heap's act. See walk-2026-09-12-register-act.md § 13.5 selection note
      (appended 2026-10-04).**
- [x] 6.24 **[OPERATOR]** The proof convening — **OQ-5 RULED (a)**,
      2026-09-11T17:08:42Z: it is **SEPARATE, and it PRECEDES C2**, on a
      re-verified clean candidate, exactly as the 2026-09-11 walk did
      (§ 15, run `34586762846`, admitted). C2 does not double as it: C2 is the
      convening the conjunction FIRES on, and one dispatch cannot say which of
      two proofs failed. Brett dispatches: the workflow's federated credential is
      `ref:refs/heads/main`-scoped and reads the factory origin key.
      **DONE 2026-09-18: ADMITTED AND SEALED. Run `35358405192`
      (2026-09-18T14:47:21Z, `success`), convening
      `GRC-CONVENE-926212af191a-35358405192`, on Brett Heap's word in session,
      verbatim *"re-dispatch on 475"* (2026-09-18T14:4xZ, lane log RULED; no
      comment URL). The identity was his (`actor`/`triggering_actor`
      `brettheap`); the keystroke was the lane's. Subject: cxF #475 pin
      `926212af191a3f138b1378c5bc4504461b193e83`, on the 2026-09-09 packet;
      bench of four, `unseated_conjunction_seats:
      ["client-security-compliance-officer"]`. This is NOT 6.22's #471. Its
      pin `4a92ee67` was SPENT by the first dispatch, run `35135959678`
      (2026-09-16, word *"dispatch it"*), which was admitted and then refused
      with no verdict by `build_run_spec`'s surplus guard. cxF #482 →
      `cd3f8a7c` (*"merge 482"*) fixed that before the re-dispatch. Record:
      cxF `records/2026-09-18-gate-rules-proof-convening-under-grant-grc-0003.md`
      plus its sealed bundle, landed by cxF #489 → `f000014c` (*"merge 489"*);
      PROOF CONVENING LANDED on #279 as comment 5734334758. See
      walk-2026-09-12-register-act.md § 13.4 post-note (appended
      2026-10-04).**
- [x] 6.25 **[OPERATOR]** Dispatch **C2** — `gate-rules-convening-trigger.yml`
      with the C2 packet ref, the fresh candidate's head sha and its PR number.
      Expect **FIVE** resolved seats and an admitted, sealed convening.
      Discharges Brett's carried-forward word `convene C2`
      (2026-09-11T13:26:14Z).
      **DONE 2026-10-04: DISPATCHED, ADMITTED AND SEALED. Run `37230435234`
      (dispatched 2026-10-04T20:00:34Z, `success`; `claim`
      20:00:41Z→20:00:48Z, `convene / convene` 20:00:52Z→20:01:12Z), convening
      `GRC-CONVENE-cd5ee34082a6-37230435234`, on Brett Heap's word in session,
      verbatim *"dispatch C2"* (2026-10-04; lane log NOTED line
      2026-10-04T20:01:50Z; no comment URL of his own), carrying his
      *"merge the packet PR when green then convene C2"*
      (2026-09-11T13:26:14Z), whose second clause is the word this row
      discharges. The identity was his (`actor`/`triggering_actor`
      `brettheap`); the keystroke was the lane's. Inputs, read from the
      `claim` job's own log: the 2026-09-11 packet
      (`2026-09-11-routine-code-clearance-repository-respelling.md`),
      `subject_pin` `cd5ee34082a63b59b4037a6732138602996a4f1f` (cxF #470 head,
      selected at 6.23) and `candidate_pull_number` `470`, from cxF `main`
      `cb504bec`. **FIVE seats** resolved and sealed:
      `resolved bench (5 seats)`, with `client-security-compliance-officer`
      declared on `claude-opus-5` and `unseated_conjunction_seats: []` in the
      sealed `run-spec.json`. The 2026-09-18 proof convening seated four.
      Posted on #279 as comments 5983851562 (DISPATCHED, 20:01:36Z) and
      5983881686 (ADMITTED AND SEALED, 20:05:04Z). See
      walk-2026-09-12-register-act.md § 13.5 post-note (appended
      2026-10-05).**
- [x] 6.26 **[lane]** On admission: hand-write the convening record (mirroring
      `records/2026-09-10-gate-rules-first-signed-convening.md`), commit the
      sealed bundle **before its 1-day artifact retention expires**, open the C2
      record PR and merge on green under Brett's standing word
      *"merge the C2 record PR when green"* (2026-09-11T13:27:23Z), and post
      `C2 DISCHARGED` on cxF #279 — closing α and all three carried-forward C2
      words in one motion.
      **DONE 2026-10-04: RECORDED, LANDED, DISCHARGED. The record is cxF
      `hermes/domain/review-councils/records/2026-10-04-gate-rules-c2-convening-under-grant-grc-0003.md`.
      It mirrors the 2026-09-18 proof convening record section for section,
      which in turn mirrored `records/2026-09-10-gate-rules-first-signed-convening.md`.
      Its sealed bundle `…/2026-10-04-gate-rules-c2-convening-sealed-bundle/`
      holds a README plus the six sealed files (the manifest and its five
      named members). It was first committed in `c1729b71`
      (2026-10-04T20:26:52Z), after the bytes were preserved in brett-wip
      `f28360b2e` (20:03:34Z), against an artifact expiry of
      2026-10-05T20:01:07Z. cxF PR #500 →
      `cc85a3cc29caabb6a2894d3e935d1e965e84d007`, merged 2026-10-04T21:34:43Z
      on Brett Heap's carried word *"merge the C2 record PR when green"*
      (2026-09-11T13:27:23Z). Main's two required contexts, `validate` and
      `lane-line`, were green at the merge, and it was an admin merge over
      the review rule. `C2 DISCHARGED` was posted on #279 as comment
      5984628943 (21:34:50Z). THE THREE WORDS are the amendment record
      § 7's, and all three are closed: α, lifted at 6.22; `convene C2`,
      spent by 6.25; and the merge word, spent by #500. This row's *"α and
      all three"* counts α once more than § 7 does, and the post names the
      merge word only. Both differences are named, not reworded. The record
      is *"NOT A DISPOSITION, AND NOT A SITTING"*, and *"NO SEAT WAS
      CONVENED, NO MODEL WAS INVOKED, AND NO SEAT RETURN WAS SIGNED"*, so 4.4
      and 4.5 stay open. See walk-2026-09-12-register-act.md § 13.5
      post-note (appended 2026-10-05).**

### 6.6 Bookkeeping this group does NOT do

- [ ] 6.27 **Task 4.6 does not tick here.** It names TWO seats; this group
      discharges one. It ticks when `intent_owner_role_slot` is likewise bound,
      or when a successor re-scopes it — and either way that is § 4's row to
      tick, not § 6's.
- [ ] 6.28 **§ 6 is NOT folded into the archive gate.** § 5.2 puts § 4 outside
      it and 4.6 lives in § 4. What § 5.3's pre-archive re-read DOES gain is a
      fifth seat to find. Rule 1 CLAIMED and Rule 6 LANDING/LANDED are owed AT
      LANDING, not at draft.
