# Tasks: encode-wallet-authority-rulings-r6-r12

Status: draft
Kind: tasks
Lane: hermes-wallet-exercise

**`code_surface` IS DECLARED AND NOT `none`, so under `release-realization`
this packet archives on MERGED-PLUS-GREEN REALIZATION EVIDENCE and not on
landing.** § 5 holds the archive behind § 3, and § 3 is in another repository
for two of its three legs.

**EVERY BOX BELOW IS UNTICKED, AND THIS PULL REQUEST PERFORMS NO ACT.** No
requirement is promoted, no contract byte moves, no register file is touched,
no grant is issued or revoked, no pin advances, no runbook sentence changes,
and **no box in any other packet is ticked by it** — `add-wallet-carried-review-authority`'s
`tasks.md` is not edited here, by D-6 and by lane discipline both. Each box
names the act that ticks it and the word that authorizes that act.

**Groups, in order:** § 1 ratify → § 2 encode → § 3 realize → § 4 cite back →
§ 5 archive → § 6 residue.

---

## 1. Ratification — Brett Heap's, and nobody else's

- [ ] 1.1 **Rule OQ-1 through OQ-9** (`proposal.md` § Open questions;
      `design.md` D-1 through D-9). Multiple choice, each with a RECOMMENDED
      option and its one-line reason. **Taking every recommendation moves not
      one byte of the delta** — ***"accept all A"*** is a complete ruling.
      Ruling otherwise on OQ-1, OQ-2, OQ-3, OQ-5 or OQ-9 rewrites the
      requirement it names before ratification; ruling otherwise on **OQ-4**
      re-derives live composition digests and, under the shipped drift cascade,
      REVOKES `grant-mrc-0002`; ruling otherwise on OQ-6, OQ-7 or OQ-8 moves
      the packet rather than its wording. Ticks on the ruling, recorded
      verbatim with its UTC instant.
- [ ] 1.2 **Ratify the packet.** `Status: draft` → `ratified` on
      `proposal.md`, `design.md`, `tasks.md` and the delta, each gaining a
      `Ratified:` line naming the human, the instant and the verbatim word,
      plus `review/ratification-<date>.md` carrying the word in full.
      `.openspec.yaml` gains `approved_by` + `approved_on` **ADDED BESIDE** the
      drafting pair, with `kind`, `id`, `reason`, `proposed_by` and
      `proposed_on` left EXACTLY as authored — the addition-not-rewrite shape
      `add-drafted-proposal-origin` (issue #318) defined.
- [ ] 1.3 **Write `proposal.md` § Rulings**, one line per OQ naming the option
      taken, and state in terms whether any delta byte moved as a result.

## 2. Encode — only if a ruling moved a byte

- [ ] 2.1 **Apply any non-recommended option to the delta.** If every OQ took
      its recommendation this box ticks with *"nothing moved"* and the reason,
      which is the honest tick and not a skipped one.
- [ ] 2.2 **Re-validate.** `OPENSPEC_TELEMETRY=0 openspec validate
      encode-wallet-authority-rulings-r6-r12 --strict` PASS, and `--all
      --strict` showing the corpus's pre-existing failures and **zero new
      ones**. Record the counts, not an adjective.
- [ ] 2.3 **Re-run `python3 scripts/validate-sequenced-after.py .`** and record
      exit 0, because 1.2 moves front matter this validator reads.

## 3. Realization — THE SURFACE, NAMED, IN THREE LEGS

**Leg 1 is in this repository. Legs 2 and 3 are the enforcing halves, and leg 2
is in another repository.** None of the three is performed by this packet.

- [ ] 3.1 **[openxFactory] Admit the holder composition as a `digest_subject`.**
      Add ONE member (`holder_composition`) to the closed enumeration in
      `contracts/signed-execution-chain/digest-construction.schema.yaml`, in
      that file's own voice, saying what the digest is taken OVER — the DECLARED
      COMPOSITION and nothing else: not the grant that cites it, not the
      register row, not the candidate repository. **NO SECOND CONSTRUCTION** —
      this is a widening of SUBJECTS, the movement the file's header sanctions
      and `add-cpc-clearing-boundary` already took. **Until this lands, the R7
      requirement is UNREALIZABLE by its own text and SHALL NOT be reported as
      satisfied.**
- [ ] 3.2 **[openxFactory] Move the manifest row and the changelog line.**
      `contracts/manifest.yaml`'s `signed-execution-chain-digest-construction`
      row `sha256:` moves because the bytes move, and
      `contracts/CHANGELOG.md` gains one line. **NO BUNDLE NUMBER IS TAKEN OR
      RESERVED HERE** — the cut and the `contract_bundle_version` bump stay the
      cutting session's act.
- [ ] 3.3 **[openXwallet] Advance the reader to refuse what R6–R12 refuse.**
      A composition digesting an identifier without its provider plane; a
      generation parameter inside `model_version`; a re-issuance record missing
      any of R8's five; a self-attested composition; a park refusal that is not
      NAMED. **AND THE 2026-09-02 WALK'S § 9 DEFECT IS MET IN THIS LEG, NOT
      CREATED BY IT:** `check_register`'s closing loop filters REVIEW-class
      grants by act and never checks `state`, so a correctly revoked grant
      demands a backing active row the one-row cap forbids; the remedy was
      measured green at two lines. Not this packet's deliverable; named because
      this is where a realizing lane meets it.
- [ ] 3.4 **[openxFactory] Advance `contracts/openxwallet-pin.yaml`** from
      `commit: f3eb929b` to the reader that 3.3 lands, commit-pinned with every
      `sha256` re-verified. A pin advance is its own governed edit.
- [ ] 3.5 **[openxFactory] Carry R8's grammar and R9's parking language into
      `docs/governed-reissuance-runbook.md`**, so the document both walks
      followed says what the requirements now require. **TAKE
      `amend-register-act-5b-projection-proof`'s AMENDMENT FIRST, do not race
      it** — that ratified change edits the same file's § 5.2 and § 7, it is
      declared in this packet's `sequenced_after:`, and two lanes editing one
      runbook is the collision the lane protocol exists to prevent.
- [ ] 3.6 **Green evidence, cited by PR and merge sha** for each of 3.1–3.5
      that a ruling leaves in scope, because `release-realization` archives a
      declared surface on merged-plus-green and not on assertion.

## 4. Cite back — what this packet discharges, and who performs the tick

- [ ] 4.1 **Record that Ground 1 is discharged**, in THIS packet, naming the
      ratification instant and word. Ground 1's own text conditions on
      *"until the change carrying R6–R12 is **ratified**"*, so 1.2 is the act
      that moves it (D-6).
- [ ] 4.2 **HAND OFF the 7.6 tick to the lane holding
      `add-wallet-carried-review-authority/tasks.md`.** **THIS PACKET DOES NOT
      EDIT THAT FILE.** The handoff states three things and asserts nothing
      more: Ground 1 is discharged by this ratification; Ground 2's remaining
      question (*"whether the pair discharges 7.6's 'walk it once' limb"*) is
      that lane's to answer on the two walk records
      (`walk-2026-08-31-composition-bump.md`,
      `walk-2026-09-02-register-act.md`); and the tick itself needs its own
      word.
- [ ] 4.3 **Record the packet in `README.md`'s OpenSpec Records block** — done
      at filing; re-check at ratification that the entry says `ratified` and
      names the word.

## 5. Archive — held, and on what

- [ ] 5.1 **Archive `encode-wallet-authority-rulings-r6-r12`**, promoting the
      seven requirements into `openspec/specs/review-authority-intake/spec.md`.
      **HELD ON THREE THINGS, each measurable:** (i) § 3's realization merged
      with green evidence, per the declared `code_surface`; (ii) the capability's
      PROMOTED file existing — created by an AUTHOR of the capability
      (`add-wallet-carried-review-authority` or
      `register-gate-rules-council-seats`), not by this successor, which is why
      both are in `sequenced_after:`; (iii) its own ratification word.
- [ ] 5.2 **Seed / reconcile the sweep ledger row** for this change through the
      sanctioned `python3 scripts/validate-sequenced-after.py . --seed-ledger
      --moved-by '#<PR>'`, never by hand-editing
      `tests/sequenced_after/corpus-ledger.yaml`.

## 6. Residue — named, so it is not rediscovered

- [ ] 6.1 **R1–R5 stay where they are.** R1–R4 need the Gate-Rules Council's
      selection act (with the duty-specific soak evidence the report requires,
      its diversity finding, and the convener's recorded acceptance) plus the
      roster-change Lead's `lead_accepted_recorded`; R5 has its Operator record
      at `add-wallet-carried-review-authority/operator-identity-record-2026-09-01.md`.
      **This packet neither performs, amends nor re-performs any of them.**
- [ ] 6.2 **R12's signer half travels with `signed-execution-chain`** — envelope
      standard, key distribution, signature algorithm, evidence-retention
      location. That capability is PROMOTED
      (`openspec/changes/archive/2026-08-31-add-signed-execution-chain/`), so
      the deferral target exists as canon rather than as a promise.
- [ ] 6.3 **Digest agility is CLOSED by D-3, not deferred.** If a second
      algorithm is ever admitted, it is a new change against the ONE
      construction, and this box is where that reader should start.
- [ ] 6.4 **The gate-rules chain's pending act is not this packet's.**
      `grant-grc-0002` is VOID since codexFactory `eff9ae19`;
      `grant-grc-0003` is pre-staged in openxFactory PR #1006 pending one
      host-side mint. Zero file overlap with this packet (D-7); recorded so a
      later reader does not infer an ordering that was measured absent.
