# Design: register-gate-rules-council-seats

Lane: hermes-wallet-exercise

Seven decisions, each with the alternative it rejects. The measurement that
grounds D5 was run, not reasoned; §D5 records the command and the reader's own
output.

## Context

`add-wallet-carried-review-authority` (ratified 2026-08-23) built the intake
register for ONE body — codexFactory's `merge_readiness_council` — and its
ratified text calls anything wider *"a named successor"*. The 2026-09-02
register act (PR #583) exercised the re-issuance path on that one body. The
per-seat key surface (openXwallet `add-per-seat-register-entries`,
`wallet-v1.2`) gave that body's four seats their own signing keys.

**This change is the first arrival of a SECOND body**, and almost everything it
finds is a consequence of that: the register, the reader and the consuming gate
were all built correctly for one holder, and the second one exposes where "one"
was written into the machinery rather than into the policy.

## D1 — Which seats, and the two that are deliberately not registered

**Decision.** Register `lead-architect`, `lead-security`, `lead-quality`,
`company-policy-lead` — every seat `gate-rules.yaml` seats BY IDENTIFIER. Defer
`intent_owner_role_slot` (declared `binding: symbolic_until_project_roster`) and
`client-security-compliance-officer` (declared as
`conjunction_pull_in.persona`, with no seat identifier).

**Identity mapping, because the two vocabularies differ.** The roster spells
seats as bare identifiers under `council.members`. The register's per-seat
surface spells a seat as the triple (`seat_id`, `council_ref`, `council_id`) and
the reader checks that `council_ref == "agent:" + council_id.replace("_","-")`.
So `gate_rules_council` maps to `council_ref: agent:gate-rules-council`, and the
roster's `lead-architect` becomes `seat_id: lead-architect` under that pair. The
roster's `members.client.seat: company-policy-lead` is a SEAT (it has an
identifier and `missing_required_seat: refused` names it as required); the same
block's `conjunction_pull_in.persona` is a PERSONA (it has no seat identifier).
The register can hold the first and cannot hold the second without inventing an
identifier for it.

**Alternative rejected: register all six, so nothing is missing later.** The
register's own text refuses it — *"Adding a seat here that the council does not
seat records authority nothing will ever present"* — and inventing an identifier
for a persona would put a value in a permanently human-only surface that no
roster can be checked against. A missing key is a loud failure at the first
convening; an invented seat is a silent authority that outlives the reason it
was invented.

**Alternative rejected: register only the three domain seats.** The tenant seat
is unconditional for THIS body and `missing_required_seat: refused` says a
gate-rules council without its client seat cannot set rules at all. Registering
three of four would produce a body that is refused on every convening.

## D2 — One body, one row, four keys — and no per-seat grant

**Decision.** Mirror `wal-agent-mrc-0001`'s realized arithmetic exactly: one
wallet declaring five keys (an operator-vaulted root plus four seat keys), one
custody attestation, one root grant, one authority row, four `seat_keys`
entries.

**Ground.** The four seats share a holder, a target repository, an act, a tier
and an expiry; the only per-seat fact is a signing key, and a key is not a
grant. Four grants would multiply the surface that must be revoked on a
composition roll by four and would give the drift cascade four objects where the
composition event has one.

**Why the wallet must DECLARE the keys and not merely the register record
them.** The pinned reader's rule (r) refuses an exercise record presenting a key
no wallet declares, and hermes-install writes the REGISTER-RECORDED `key_id`
into `presenting_key_ref`. A register-only recording would make the first signed
gate-rules seat return unrepresentable — the exact defect `wallet-v1.3` was cut
to fix for merge-readiness.

**Alternative rejected: attach the gate-rules seats to `row-mrc-0001`.** Not a
style choice — the reader forbids it. `_check_seat_keys` refuses an entry whose
`council_ref` is not the authorizing row's `holder_ref`
(`register-seat-council-mismatch`), and that row's holder is
`agent:merge-readiness-council`. Attaching them would also be false: it would
record the gate-rules seats as descending from the merge-readiness council's
authority.

## D3 — Composition is pinned in codexFactory FIRST, or no grant is issued

**Decision.** Authoring `review_council_profiles.gate_rules_council` in
codexFactory `hermes/domain/agent-mixes.yaml` and a `composition_source_map` on
`gate-rules.yaml` — mirroring merge-readiness's six declared components
(`model_version`, `prompt_contract`, `tool_manifest`, `policy_version`,
`parameters`, `retrieval_corpus`) with EXACT model identifiers — is a
PREREQUISITE of issuing `grant-grc-0001`, not a follow-up.

**Ground, checked rather than assumed.** `gate-rules.yaml` carries no
`composition_source_map`, and `agent-mixes.yaml`'s `review_council_profiles`
block declares `merge_readiness_council` and nothing else. The ratified
requirement *"A reviewing holder's composition is pinned, and a composition roll
is a governed re-issuance"* has no subject here. Issuing a grant against a
composition that does not exist would create the one review authority in the
estate that no drift cascade can revoke — and it would be held by the body that
SETS the gate rules.

**Q8(d) governs the pin and is not reopened**: exact model versions only, never
a family (rulings-2026-08-26). The reserved half — whether a rule-setting body
gets a composition at all, and the two-body blast radius when the shared roster
flips — is Q-GRC-2 in the proposal, with a recommendation and no decision.

**Alternative rejected: issue the grant now, pin the composition later.** It
inverts the fail-closed direction of the whole arc: the grant would be live
while the fact that revokes it is absent. The 2026-08-31 roster flip is the
worked example of why — it revoked `grant-mrc-0001` precisely because the
composition WAS declared and DID move.

## AMENDED 2026-09-07 — D3 sequencing

Row 3.1 (this design's own PREREQUISITE) was found BLOCKED on execution,
measured on codexFactory main `8f4920ce` and reported on openxFactory PR #717
(<https://github.com/opensoft/openxFactory/pull/717#issuecomment-5564009224>,
2026-09-07T02:09:57Z): the only renderer
(`deliberation_packet.py#seat_system_prompt`) hard-codes
`merge_readiness_council` and refuses `lead-architect` as an unknown seat,
and `lead-architect` had no enrolled pin anywhere. So `prompt_contract`,
`tool_manifest`, `parameters` and `retrieval_corpus.seat_prompts_ref` could
only be ASSERTED against a caller that does not exist — the very thing D3's
own EXACT-identifiers, execution-matched standard (precedent `016e9f43`)
refuses.

Brett Heap ruled, in-session, 2026-09-07T12:40:19Z, verbatim *"R1
lead-architect claude-opus-5, R2 (a) — re-sequence 5.9a first"*
(<https://github.com/opensoft/openxFactory/pull/717#issuecomment-5570774593>):
codexFactory task 5.9a (the `gate_rules_council` caller with seat briefings)
now precedes row 3.1 in this change's § Sequencing — proposal.md's
2026-09-07 AMENDMENT restates the order — and `lead-architect` is pinned to
`claude-opus-5` by the recorded roster-change act
(`guardrails.roster_change: lead_accepted_recorded`). D3's decision that
composition is a PREREQUISITE of the grant, pinned FIRST, is unchanged; what
moves is composition's position relative to the CALLER, not relative to the
grant.

## D4 — The mint is a runbook Brett executes; nothing is minted here

**Decision.** `docs/council-seat-key-mint-runbook.md` (this change's own
artifact, `Status: draft` until ratification) generalizes the 2026-08-28
merge-readiness ceremony — recorded then as a codexFactory record but never
written down as a repeatable procedure — into the operator ceremony for ANY
council body's seat keys. The sequence is fixed and each step is a separate,
verifiable artifact: **mint → wallet + attestation → grant → row**, ONE walk
record for the whole act, in the form of
`walk-2026-09-02-register-act.md`.

**Precedent followed.** `docs/factory-origin-key-mint-runbook.md` (PR #610) puts
the ceremony in `docs/` and the record template inside it; the private half never
enters the repository and only the public half, the `did`, and the recomputing
fingerprint are committed. `docs/governed-reissuance-runbook.md` is the
precedent for a `Status: draft` runbook whose ratification rides its change.

**Alternative rejected: a `scripts/mint-council-seat-keys.py` to match the
origin-key runbook's one-command form.** That script exists for a key openxFactory
provisions into its OWN repository's environment; these private halves are
provisioned into codexFactory's, which openxFactory has no business writing to.
A program that reaches across a repository boundary to store a secret is a worse
artifact than a checklist, and four keys is a ceremony the operator runs once.

**Alternative rejected: put the runbook in the change directory.** The ceremony
outlives the change — a third body will need it — and a runbook that archives
with its change is a runbook nobody finds.

## D5 — The reader widening is openXwallet's, it is REQUIRED, and it was measured

**Decision.** The two defects below are fixed in `opensoft/openXwallet` through
that repository's own OpenSpec change with red-first tests, cut as a bundle tag;
openxFactory then advances `contracts/openxwallet-pin.yaml`. **No reader code is
written in openxFactory** — `scripts/validate-openxwallet.py` has not lived here
since `split-openxwallet-repo` (2026-08-28) and copying it back would fork the
one reader every consumer runs.

**THE MEASUREMENT.** Reproducible, and it is the ground for everything above:

```
# a copy of the live governance/review-authority/ tree, plus row-grc-0001,
# wal-agent-grc-0001, grant-grc-0001, custody-attest-wal-agent-grc-0001,
# and two gate_rules_council seat_keys entries
python3 openXwallet/scripts/validate-openxwallet.py <probe-tree>
```

at the pinned reader (`b7b0fbb3e6d614f60a24737c247e45dada9408aa`,
`wallet-v1.4`) reports:

```
note  intake register read: governance/review-authority/register.yaml (2 row(s))
note  intake register: 4 of 6 per-seat signing key(s) adjudicated and resolved
ERROR [register-minimal-shape-exceeded] …: 2 AUTHORITY rows; the ratified
  first shape is exactly ONE holder/target/act row - wider registers are a
  named successor change.
ERROR [register-seat-duplicate] …:seat_keys[5] (lead-security): seat_id
  'lead-security' is already recorded at seat_keys[1]; a repeated seat_id is
  refused rather than resolved by file order
```

**Defect 1 — `REGISTER_MVP_SINGLE_ROW = 1`.** A second body needs a second
authority row (D2 explains why it cannot share the first). The cap refuses it.

**Defect 2 — global seat-name uniqueness.** `_check_seat_keys` builds
`seen = {"seat_id": {}, "key_id": {}, "key_fingerprint": {}}` over ALL entries
in the file and refuses a repeated `seat_id` regardless of council. Three of
gate-rules' four seats reuse names merge-readiness already records. **This
defect is invisible with one council and fires the moment a second arrives** —
the same shape as the `wallet-v1.4` defect, which was invisible until the first
re-issuance and was found by the act that performed it. `key_id` and
`key_fingerprint` uniqueness are CORRECT as global (a key is one key) and must
not be relaxed with `seat_id`.

**The fix is already written down elsewhere in the estate**, which is the
strongest available evidence for its shape: hermes-install's `derive_projection`
keys its duplicate table on `(council_id, seat_id)` and refuses only *"the
register projects `<council>/<seat>` more than once"*. The reader should adopt
that key.

**Alternative rejected: raise the cap to 2.** Q-GRC-5. Two is as arbitrary as
one and buys one body of headroom.

**Alternative rejected: keep the register at one row and give gate-rules its own
register file.** Two register files means two things the runtime must project
and two paths the floor must name, and the codexFactory floor pins the EXACT
path `governance/review-authority/register.yaml` with wildcards refused — a
second file would be unfloored on the day it was created.

**Alternative rejected: land the register act red and fix the reader after,
citing the 2026-09-02 precedent.** That precedent is the argument AGAINST
repeating it: the act landed red, the walk record had to devote its §9 to
explaining that the red was about the reader, and the required check stayed red
on `main` until the pin moved. Once is a discovery; twice is a practice.

## D6 — The human-only floor, and the gap this change widens

**Decision.** State three things and close none of them by assertion:

1. **The register stays permanently human-only** and its exact path stays a
   never-clearable floor member in codexFactory's
   `scripts/merge_master/openxfactory-review-authority-floor.yaml`. Nothing here
   moves or renames it; the floor refuses wildcards, so a rename would silently
   unfloor it.
2. **`gate_rules_council` is the sharpest case of the ratified
   self-clearance refusal**, because it is the body that SETS the never-clearable
   list. A change to its own register rows is cleared by the OPERATOR ONLY: not
   by that council, and not by merge-readiness either, since both bodies now hold
   authority conferred by the same file. The refusal is not "a council may not
   clear its own row"; it is "no council clears a candidate that edits this
   file", which is what the register already says and what this change keeps
   true with a second body present.
3. **This change WIDENS a pre-existing floor gap and says so.** The floor names
   `governance/review-authority/register.yaml`,
   `contracts/openxwallet-pin.yaml`, the `openXwallet` gitlink and
   `contracts/review-lane-pin.yaml`. It does NOT name
   `governance/review-authority/{grants,wallets,attestations}/` — recorded at
   `split-openxwallet-repo` §8.3 as pre-existing, with lead-security's
   2026-08-26 floor-reachability finding still standing. This change adds three
   files into that unfloored space, one of which (`grant-grc-0001.yaml`) confers
   the rule-setting body's own review authority. **Tasks §4 names the owner; the
   gap is not declared closed and must not be inferred closed from the
   register's own entry.**

**Alternative rejected: close the floor gap in this change.** It is a
codexFactory floor act on a document the gate-rules council itself governs, with
its own convening and its own movement ledger. Folding it in would put a
codexFactory floor widening inside an openxFactory register proposal and would
give this change two ratifying bodies.

## D7 — The staleness bound is one line, and the downstream acts are named, not tasked

**Decision.** `revocation_staleness_bound: P7D` is a FILE-LEVEL declaration and
governs both rows. It is not touched by this change — not tightened as a
tidy-up, not duplicated per body.

**What the runtime actually reads, checked rather than assumed.** The runtime
does not read `register.yaml`; it reads an operator-established PROJECTION.
hermes-install's `project-register` verb derives it
(`src/hermes_install/lifecycle/project_register.py`), narrows it
(`review_authority/derivation.py`), validates it against
`hermes-review-authority-register-projection.schema.yaml` (schema_version 2,
no cap on `seats`), and publishes ConfigMap `hermes-register-projection` from
CronJob `hermes-register-projection-refresher` (schedule `0 */2 * * *`,
deployed 2026-08-30). `revocation_staleness_bound` travels verbatim into
`projected_from.staleness_bound`.

**The projection is ALREADY multi-council capable** — `_rows_by_id` joins each
seat to its own row, `seen` is keyed on `(council_id, seat_id)`, and `councils`
is a sorted set of the projected `council_id`s. Nothing in hermes-install needs
a change for a second body. The visible signal that the refresh happened is
`seat_count` moving 4 → 8 and `councils` gaining `gate_rules_council`.

**The owed acts downstream, with owners, stated as OWED ACTS and not as tasks
this change discharges:**

| Owed act | Owner | Why it is not a task here |
|---|---|---|
| Projection refresh after the register act lands | operator / hermes-install CronJob | An operator act on a cluster; the CronJob reads the DEFAULT BRANCH, so it is invisible to this pull request by construction |
| Observe a SCHEDULED refresher firing | hermes-install | Already on that repository's follow-up list; no scheduled firing has been observed on record, only a manual migration job |
| A caller that convenes `gate_rules_council` and returns signed seat returns | codexFactory (task 5.9a) | The roster itself says the missing piece is a caller; a definition-time council must not be wired to per-PR facts to close the gap |
| The FIRST SIGNED gate-rules convening | codexFactory + hermes-install | This is what makes the queuing ruling's *"so later convenings are signed"* true, and no register act can produce it |

**Alternative rejected: declare a tighter bound for the new body.** One
projection has one age. A per-body bound would be a number the runtime has
nowhere to apply.

**Alternative rejected: treat the projection refresh as this change's task.**
Stopping at the register act is the commonest way to think this runbook is
finished when it is not — but the act belongs to the operator and the cluster,
and a checkbox here would let this change archive on a projection nobody ran.

---

## AMENDED 2026-09-11 — Q-GRC-4 discharge for the CSC seat (D8-D12)

**D1-D7 above are NOT rewritten, narrowed or reopened.** This section is
APPENDED. Record:
`review/amendment-2026-09-11-q-grc-4-discharge.md`. Rulings: Brett Heap, in
session, window `codeXfactory-2`, **2026-09-11T14:59:26Z**, verbatim *"amend
register-gate-rules-council-seats, lead-architect route, same model pin as
lead-security"*. Tasks: § 6.
**D8-D12 RULED: Brett Heap, in session, window `codeXfactory-2`, no comment URL,
2026-09-11T17:08:42Z, verbatim *"accept all A on 971, merge slice 3 when
green"*, its FIRST clause** — each of OQ-1..OQ-5 at
option **(a)**, its RECOMMENDED one, so every decision below stands exactly as
it was written and **not one byte of the delta moves**. The amendment record's
§ 9 carries the five `RULED` lines; `tasks.md` § 6.1 and § 6.1a carry the ticks.

Five decisions, each stated with the alternative it rejects, and each mapped
**1:1 onto one of the amendment record § 9's open questions** — so a reader who
takes a ruling on OQ-n knows exactly which decision it moves, and a ruling that
takes the recommendation moves no byte.

| decision | open question | what it decides | RULED 2026-09-11T17:08:42Z |
| --- | --- | --- | --- |
| **D8** | **OQ-1** | who mints and holds the fifth seat keypair | **(a)** — Brett Heap, host-side, the task 3.2 ceremony generalized to one seat; `holder_readable`; secret `COUNCIL_SEAT_SIGNING_KEY_GRC_CLIENT_SECURITY_COMPLIANCE_OFFICER` |
| **D9** | **OQ-2** | `expires_at` on the re-issued grant | **(a)** — `2027-06-30T00:00:00Z`, unchanged |
| **D10** | **OQ-3** | whether the new seat owes a soak or an activation pass before it sits | **(a)** — bind now, soak later; no soak and no `activation_gate` pass gates the binding |
| **D11** | **OQ-4** | the act's shape across two remotes — one T1/T2 pair, or a further split | **(a)** — the T1/T2 PAIR: one codexFactory PR (H1), then one openxFactory PR (H2) |
| **D12** | **OQ-5** | whether C2 doubles as the seat's first live convening | **(a)** — a SEPARATE proof convening precedes C2, on a re-verified clean candidate |

### D8 — The fifth key is minted by the operator, host-side, in the task 3.2 ceremony generalized to one seat (OQ-1) — RULED (a), 2026-09-11T17:08:42Z

**Decision.** The same ceremony D4 already decided for the first four: an
operator act, host-side, with the seed generated in-process and never written to
disk, passed to `gh secret set` on stdin with `--body` omitted, and the private
half held ONLY as a GitHub Actions secret in codexFactory's `worker-credentials`
environment under the GRC-namespaced name. Custody `holder_readable` — **Q-GRC-1
already ruled this for this body on 2026-09-06T14:13:46Z and was never scoped to
four seats**, so no second custody ruling is owed and none is taken.

**Alternative rejected: mint through the repository-committed
`scripts/mint-factory-origin-key.py`.** That script is the ORIGIN-key ceremony
for the one key an originating repository holds, and D4 already decided the seat
mint is a runbook Brett executes rather than a script this repository ships.
Nothing about a fifth seat reopens that.

**Alternative rejected: a different custody model for this key alone.** It would
give one seat of one bench a key its own holder job cannot read, and would make
the custody attestation describe two postures for one wallet.

### D9 — `expires_at` stays `2027-06-30T00:00:00Z` unless a pin says otherwise, and today none does (OQ-2) — RULED (a), 2026-09-11T17:08:42Z

**Decision.** Q-GRC-3's ruled date, unchanged. Its reason — one re-issuance
ceremony covers both bodies and the two grants cannot silently diverge — is
untouched by a fifth seat, and `grant-mrc-0002` still carries that date.

**Alternative examined and found to return the same value: recompute from the
earliest published retirement floor among the council's pinned identifiers**,
by the 2026-09-11 walk's own method. The fifth pin IS `claude-opus-5`, already
on this bench under `lead-architect` and `lead-security`, so **the computed
floor cannot move**. The alternative therefore differs only in showing its
working — which is why it is offered as OQ-2 (b) rather than silently taken.

**Alternative rejected: a shorter expiry for the new seat.** Refused by shape,
not by preference. The grant is addressed to the WALLET and the row carries one
expiry; there is no per-seat expiry field to set, and inventing one would fail
the reader's exact field-set check.

### D10 — Bind now, soak later: the lead-architect precedent, and the soak that costs nothing today (OQ-3) — RULED (a), 2026-09-11T17:08:42Z

**Decision.** The seat is bound and its key registered in this act; any soak
follows. This is R1's order exactly — R1 bound `lead-architect`'s pin on
2026-09-07 and LQ-C1's four-class integration soak was commissioned AFTER it and
is still open. **C13 re-opens this body's soak from zero** (`soak_gate`'s
`seat_roster_fixed_and_recorded_before_first_soak_row`: *"a soak run on roster A
cannot license activation on roster B"*), and **that costs nothing today for
exactly the reason it cost nothing at R1**: no gate-rules convening has ever run
a seat through the deliberation lane and no soak row exists.

**Alternative rejected: require an LQ-C1-shaped fresh soak before the seat may
sit.** It parks C2 behind a soak that has never gated any seat of this body, and
inverts the order R1 set four days ago on the same council. The soak is owed;
it is not a precondition of binding.

**Alternative rejected: declare a `gate_rules_council` `activation_gate`.**
MEASURED: none exists. `activation_gate` as a literal key belongs to the
ENROLLED merge-readiness surface
(`scripts/merge_master/codexfactory-routine-code-clearance.yaml` and siblings);
neither `gate-rules.yaml` nor this profile declares one. Declaring one here is
NEW machinery invented mid-act, not an existing gate being honoured — and D3's
own standard (declare against what exists, execution-matched, never asserted)
refuses it.

**What DOES carry unchanged is LQ-C4's `tool_manifest` bound**: this council
declares no tools, no workspace and no browser for any seat, and whether a
packet-only seat can meet its charge without running anything remains untested.
A fifth seat neither worsens nor cures that, and the record says so rather than
letting a new seat imply new capability.

### D11 — Two pull requests because there are two remotes; ONE governed act because the hold spans them (OQ-4) — RULED (a), 2026-09-11T17:08:42Z

**Decision.** The T1/T2 pair: one codexFactory pull request (H1 — the binding,
the composition, the briefing, the record, the digest re-pin), merged at T1
under a hold posted BEFORE the merge; then one openxFactory pull request (H2 —
revoke, mint, repoint, the fifth seat key, the fifth wallet key, the consumer
gate's literal count, the walk record), merged at T2. This is the shape this
lane exercised end to end on 2026-09-11 (cxF #374 → oxF #941).

**Alternative rejected: split H1 further** — mint record, roster act and
composition re-pin as separate codexFactory pull requests. It re-introduces
precisely the window Q-GRC-4's *"the same governed act must register its key"*
exists to close: a landed roster that names a seat whose key is not yet
registered, with the first convening that seats it discovering the gap.

**Alternative unavailable: one cross-repository act.** Two remotes cannot share
a commit. The hold is what makes two merges one act, which is why D11's real
content is the hold rather than the PR count.

### D12 — A separate proof convening precedes C2, because C2 is the convening the conjunction FIRES on (OQ-5) — RULED (a), 2026-09-11T17:08:42Z

**Decision.** After the lift, a proof convening on a re-verified clean
candidate, as the 2026-09-11 walk did (§ 15, run `34586762846`, admitted) —
then C2. C2's subject is under `scripts/merge_master/**`, one of the four
declared `security_surfaces`, so C2 is the FIRST convening in this estate at
which `rule_touches_security_posture` both holds AND has a bound seat to pull
in. Proving a five-seat bench on the same dispatch that first exercises the
conjunction conflates two proofs, and a failure would not say which one failed.

**Alternative put as OQ-5 (b) and NOT TAKEN — RULED (a), 2026-09-11T17:08:42Z:
C2 IS the proof convening.** It is cheaper by one pin, and the read-only `resolved-seats`
run (task 6.22) already proves the BINDING without spending anything — so the
only thing the separate convening buys is separating "five seats resolve and
return" from "the conjunction fires correctly". That is a real judgment about
how much evidence a first sitting owes, which is why it went to Brett rather
than being settled here — and he ruled **(a)**, the separate convening, on
2026-09-11T17:08:42Z.

**Alternative rejected: two proof convenings, one on each side of the
conjunction.** The most evidence and the most pins; nothing in the corpus asks
for it, and this bench has no soak row to protect.

### What this section does not decide

- **It does not reopen Q-GRC-4.** Q-GRC-4 ruled *"register neither deferred seat
  NOW"* and named the trigger. This is the trigger arriving, for ONE seat.
- **It does not touch `intent_owner_role_slot`**, whose trigger — the
  subject-layer roster binding — has not arrived.
- **It does not decide the seat identifier string.** That is an authoring
  decision flagged for veto (task 6.1b), not a design decision, and not an OQ.
- **It does not make the discharge an archive condition.** § 5.2 already puts
  § 4 outside the archive gate and task 4.6 lives in § 4; task 6.28 restates it.
