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

- [ ] 1.1 **[OPERATOR] [GOVERNANCE]** Ratify or return this proposal. Nothing
      below §1 is legal until this is ticked. Ratification alone REALIZES
      NOTHING — no key is minted, no row is written, no pin moves.
- [ ] 1.2 **[OPERATOR] [GOVERNANCE]** Rule **Q-GRC-1** — where the four private
      halves live, given that `gate_rules_council` has no automated lane.
      Recommendation on record: mint into codexFactory `worker-credentials` now,
      `holder_readable`, with the custody attestation naming the OWED job as the
      holder execution context and saying plainly that it does not exist yet.
- [ ] 1.3 **[OPERATOR] [GOVERNANCE]** Rule **Q-GRC-2** — the composition pin for
      a rule-setting body that has none, and the two-body blast radius of one
      shared-roster flip. Q8(d) (exact versions only) is ALREADY RULED and is
      not reopened by this row.
- [ ] 1.4 **[OPERATOR] [GOVERNANCE]** Rule **Q-GRC-3** — the expiry horizon for
      `grant-grc-0001`. Recommendation on record: `2027-06-30T00:00:00Z`,
      matching `grant-mrc-0002` so one ceremony covers both bodies.
- [ ] 1.5 **[OPERATOR] [GOVERNANCE]** Rule **Q-GRC-4** — the two deferred seats
      (`intent_owner_role_slot`, `client-security-compliance-officer`):
      confirm they are NOT registered now and that whichever codexFactory roster
      act binds them registers their keys in the same governed act.
- [ ] 1.6 On ratification, flip `docs/council-seat-key-mint-runbook.md` from
      `Status: draft` to `Status: ratified` and add
      `Ratified by: register-gate-rules-council-seats`.
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
- [ ] 2.7 Advance `contracts/openxwallet-pin.yaml`: `commit:` and
      `contract_bundle_tag:` ONLY. **No `files:` digest row moves** —
      `scripts/validate-openxwallet.py` sits under `pinned_by_commit_only:` and
      a reader-only release moves no contract byte. Reverify the other eight
      digests by recomputation at the new commit rather than carrying them on
      trust, and re-record `carve_commit:` only if a digest actually moved.
- [ ] 2.8 Move the consumer gate's LITERAL assertions in
      `.github/workflows/openxwallet-consumer-gate.yml` IN THE SAME PULL REQUEST
      as 2.7 — a stale literal is a red REQUIRED check on a human-only surface,
      which is the parked-candidate shape this whole arc exists to end:
      - `intake register: 4 of 4 per-seat signing key(s) adjudicated and resolved`
        → `8 of 8`;
      - a NEW assertion that `wal-agent-grc-0001`'s five declared keys were
        adjudicated, beside the existing `wal-agent-mrc-0001` one;
      - keep every count LITERAL. A wildcard would let a register that lost a
        body pass the positive proof.
- [ ] 2.9 **Gate:** with 2.7 + 2.8 landed and the register still carrying ONE
      row, `wallet-validation` is GREEN and the log's `intake register read:`
      note still says `1 row(s)`. The pin advance must be provably neutral
      BEFORE the register moves.

## 3. Brett's operator WALK — the mint and the register act

**[OPERATOR] throughout.** Executed against
`docs/council-seat-key-mint-runbook.md`, recorded in ONE walk file
`openspec/changes/register-gate-rules-council-seats/walk-<YYYY-MM-DD>-register-act.md`
in the form of `walk-2026-09-02-register-act.md`. Do not start §3 until §2's
gate is green: at the old reader every one of these writes is refused.

- [ ] 3.1 **[codexFactory]** PREREQUISITE (design D3): author
      `review_council_profiles.gate_rules_council` in
      `hermes/domain/agent-mixes.yaml` and a `composition_source_map` on
      `hermes/domain/review-councils/gate-rules.yaml`, mirroring
      merge-readiness's six declared components with EXACT model identifiers.
      **No grant is issued against a composition that does not exist.**
- [ ] 3.2 Mint FOUR Ed25519 keypairs, one per registered seat —
      `lead-architect`, `lead-security`, `lead-quality`, `company-policy-lead` —
      plus the body's root key `key-grc-0001`. Private halves NEVER enter git,
      CI logs or an agent session; provision the four seat halves per the
      Q-GRC-1 ruling. Record the public halves, the `did`s and the recomputing
      fingerprints in a codexFactory mint record, as the 2026-08-28 mrc mint
      did.
- [ ] 3.3 Write `governance/review-authority/wallets/wal-agent-grc-0001.yaml`:
      holder `agent:gate-rules-council`, custody `holder_readable`, root key
      `key-grc-0001` in `key_reference`, the four seat keys in `keys:` with
      per-key custody. FIVE declared keys — the shape rule (r) needs so a seat
      return naming a per-seat key is representable.
- [ ] 3.4 Write
      `governance/review-authority/attestations/custody-attest-wal-agent-grc-0001.yaml`.
      Without it the unattested cap applies and the grant reaches only
      `request`. State the honest posture, including that the holder execution
      context is NAMED AND OWED rather than observed (Q-GRC-1).
- [ ] 3.5 Write `governance/review-authority/grants/grant-grc-0001.yaml`: a ROOT
      grant (no `parent_grant_ref`), `issued_by` the anchored operator,
      `acts: [review]`, `objects: [opensoft/openxFactory]`,
      `authority_tier: act`, `approval_posture` byte-identical to
      `grant-mrc-0002`'s, `expires_at` per the Q-GRC-3 ruling. Re-examine each
      scope element deliberately and record WHY it stands, so a later reader can
      tell a decision from a paste.
- [ ] 3.6 Write the second authority row in
      `governance/review-authority/register.yaml`: `row-grc-0001`, exactly the
      nine fields, `expires_at` CHARACTER-FOR-CHARACTER equal to 3.5's because
      the reader compares the two. **`row-mrc-0001` is not touched.**
- [ ] 3.7 Append the FOUR `seat_keys` entries: `council_ref:
      agent:gate-rules-council`, `council_id: gate_rules_council`,
      `authorizing_row: row-grc-0001`, one `key_id` and one recomputing
      `key_fingerprint` each. Key ids are namespaced (`key-grc-seat-<seat>-0001`)
      because `key_id` uniqueness stays global.
- [ ] 3.8 Run the gate LOCALLY before pushing:
      `python3 openXwallet/scripts/validate-openxwallet.py .` must be clean, and
      the log must say `intake register read: … (2 row(s))` and
      `intake register: 8 of 8 per-seat signing key(s) adjudicated and resolved`.
- [ ] 3.9 Record the walk: what each step produced, the citations the act is
      fixed at, the rulings as spoken, the honest limits — including that no
      gate-rules convening has ever run and that the seats are therefore
      registered and unexercised.
- [ ] 3.10 **Gate:** the pull request carrying §3 is GREEN on
      `wallet-validation`, and it is human-landed by construction — the register
      is a never-clearable floor member and no council verdict clears it.

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
