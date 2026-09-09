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
- [ ] 1.7 `OPENSPEC_TELEMETRY=0 openspec validate register-gate-rules-council-seats
      --strict` and `--all --strict` clean from the repository root; the change
      is listed in `README.md`'s `## OpenSpec Records` block and the runbook in
      the README doc index; the `sequenced_after` corpus ledger carries this
      change's row.

## 2. The reader, and the pin — the hard prerequisite

- [ ] 2.1 **[openXwallet] [GOVERNANCE]** Open the reader-widening change
      (proposed id `widen-register-reader-for-a-second-council`, declared in this
      proposal's `sequenced_after:`). Two defects, both MEASURED at
      `b7b0fbb3e6d614f60a24737c247e45dada9408aa` / `wallet-v1.4` (design D5):
      `register-minimal-shape-exceeded` on a second AUTHORITY row, and
      `register-seat-duplicate` on `lead-security` — a seat name both councils
      seat.
- [ ] 2.2 **[openXwallet]** RED FIRST. Two failing tests before either fix:
      (a) a fixture register with TWO authority rows, each resolving end to end
      to its own wallet, grant and attestation, asserted CLEAN; (b) a fixture
      register whose `seat_keys` carries the same `seat_id` under two different
      `council_id`s, asserted CLEAN, together with a third that carries the same
      `seat_id` TWICE under ONE `council_id`, asserted REFUSED with
      `register-seat-duplicate`. Both must fail against the reader as it stands.
- [ ] 2.3 **[openXwallet]** Fix defect 2: key the seat-entry duplicate table on
      the PAIR `(council_id, seat_id)`. **Leave `key_id` and `key_fingerprint`
      uniqueness GLOBAL** — a key is one key, and two bodies presenting it are
      two claims on one identity.
- [ ] 2.4 **[openXwallet] [GOVERNANCE]** Fix defect 1 per the Q-GRC-5 ruling:
      retire `REGISTER_MVP_SINGLE_ROW` in favour of the invariants it stood in
      for (every row resolves end to end; every seat entry attaches to a row
      that commissions its body; the pair is unique), rather than substituting
      the number 2 for the number 1.
- [ ] 2.5 **[openXwallet]** Extend the reader's own S4 self-test block with the
      two-row and two-council probes, so a later edit cannot silence the
      invariant while the self-test stays green.
- [ ] 2.6 **[openXwallet]** Cut the bundle tag (`wallet-v1.5` or as allocated)
      and publish the digests in `contracts/manifest.yaml`.
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

- [ ] 4.1 **[OPERATOR] / [hermes-install]** Refresh the register projection
      after §3 lands: the next `hermes-register-projection-refresher` tick, or a
      manual `project-register` run against the merged revision. The visible
      signal is `seat_count` 4 → 8 and `councils` gaining `gate_rules_council`.
      **Until it is re-derived the runtime keeps refusing with
      `review_authority.root_key_mismatch` and no authority flows.** Nothing in
      hermes-install needs a code change: `derive_projection` already keys on
      `(council_id, seat_id)` and already reports `councils` as a set.
- [ ] 4.2 **[hermes-install]** Observe a SCHEDULED refresher firing. Already on
      that repository's follow-up list; only a manual migration job is on record
      to date, so the standing manual re-projection duty is not retired by this
      change.
- [ ] 4.3 **[codexFactory]** Close the floor-reachability gap this change WIDENS
      (design D6): `governance/review-authority/{grants,wallets,attestations}/`
      are not named in
      `scripts/merge_master/openxfactory-review-authority-floor.yaml`, and §3
      adds three files there — one of them the grant conferring the rule-setting
      body's own authority. Pre-existing per `split-openxwallet-repo` §8.3 with
      lead-security's 2026-08-26 finding standing; **owner: the arc owner of
      `add-wallet-carried-review-authority`.** Not closed by this change and not
      inferable from the register's own floor entry.
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

- [ ] 5.1 `code_surface` is NOT `none`, so per `release-realization` this change
      archives only on MERGED, GREEN REALIZATION EVIDENCE. The evidence set is
      exactly:
      - §2.7 + §2.8 merged and `wallet-validation` green at the advanced pin
        with the register still at one row (§2.9);
      - §3 merged and `wallet-validation` green with the log reading
        `2 row(s)` and `8 of 8 per-seat signing key(s) adjudicated and
        resolved`;
      - the walk record (§3.9) committed;
      - §1.2–§1.5 ruled and recorded.
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
