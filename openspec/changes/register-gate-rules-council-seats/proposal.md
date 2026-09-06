---
code_surface: openxFactory — NOT `none`, and the distinction is load-bearing. This proposal's OWN diff is spec text, one runbook and bookkeeping; but its realization moves four openxFactory surfaces and the change MUST NOT archive until they are merged and green: (1) `governance/review-authority/register.yaml` — a SECOND authority row plus FOUR per-seat key entries, written by Brett's operator act on a permanently human-only surface; (2) `governance/review-authority/{wallets,grants,attestations}/` — `wal-agent-grc-0001.yaml`, `grant-grc-0001.yaml`, `custody-attest-wal-agent-grc-0001.yaml`, likewise operator-written; (3) `contracts/openxwallet-pin.yaml` — `commit:` and `contract_bundle_tag:` advance to the openXwallet release that can represent a second council (NO digest row moves: `scripts/validate-openxwallet.py` is pinned by commit only, `pinned_by_commit_only:`); (4) `.github/workflows/openxwallet-consumer-gate.yml` — the REQUIRED check's LITERAL positive assertions (`4 of 4 per-seat signing key(s)`, and a new one for the second wallet's declared keys) move in the same act, because a wildcard there would let a register that lost a body pass the positive proof. NO reader code is written here: the reader lives in `opensoft/openXwallet` and its widening is that repository's own OpenSpec change, named in tasks §2 as a hard prerequisite.
target_release: none — no contract bundle is cut by openxFactory. Nothing under `contracts/openxwallet/` or `contracts/schemas/` is authored or edited here; the pin advance CONSUMES an openXwallet bundle (`wallet-v1.5` or later) rather than publishing one, and no `contracts/manifest.yaml` row or `contracts/CHANGELOG.md` line is owed on this side.
sequenced_after: [add-wallet-carried-review-authority, openXwallet:widen-register-reader-for-a-second-council]
---

# Proposal: register-gate-rules-council-seats

Status: draft
Proposed: 2026-09-06, on Brett Heap's queuing ruling of 2026-09-05 (below).
Lane: hermes-wallet-exercise
Family: S5 of `add-wallet-carried-review-authority` — the register-act family,
  following `add-per-seat-register-entries` (openXwallet, wallet-v1.2) and the
  2026-09-02 register act (PR #583).

## The ruling this realizes

codexFactory PR #165, the OQ-C ruling — Brett Heap, in session,
2026-09-05T17:15Z
(<https://github.com/opensoft/codexFactory/pull/165#issuecomment-5553459343>),
verbatim:

> RULING for this PR's OQ-C (`gate_rules_council` has no projected seat, so a
> signed convening cannot complete) — Brett Heap, in-session,
> 2026-09-05T17:15Z: **operator ratification now, seats later.** … Registering
> gate-rules seats (mint + rows in openxFactory
> `governance/review-authority/register.yaml`) is QUEUED as its own S5-family
> openxFactory change so later convenings are signed.

**This change is that queued change.** It is a PROPOSAL and it PERFORMS
NOTHING: no key is minted, no wallet, grant, attestation or register row is
written, no pin is advanced, no workflow assertion is moved. The intake
register is a PERMANENTLY HUMAN-ONLY SURFACE by ratified requirement and its
exact path is a never-clearable floor member in codexFactory's gate rules, so
every write to it is Brett's operator act. What this change does is SPECIFY,
SEQUENCE and GATE those acts — and it finds, by measurement rather than by
reading, that they cannot be performed at all until a reader defect in a second
repository is fixed.

## The headline, before the detail

**The gate-rules seats cannot be registered against the pinned reader. Two
distinct defects refuse them, and both were MEASURED, not inferred.**

The probe: a copy of the live `governance/review-authority/` tree with a second
authority row (`row-grc-0001`, holder `agent:gate-rules-council`), a matching
wallet, grant and custody attestation, and two gate-rules seat entries; run
through the reader openxFactory pins today
(`openXwallet/scripts/validate-openxwallet.py`, commit
`b7b0fbb3e6d614f60a24737c247e45dada9408aa`, `wallet-v1.4`). The reader's own
words:

```
ERROR [register-minimal-shape-exceeded] …/register.yaml: 2 AUTHORITY rows;
  the ratified first shape is exactly ONE holder/target/act row - wider
  registers are a named successor change.
ERROR [register-seat-duplicate] …/register.yaml:seat_keys[5] (lead-security):
  seat_id 'lead-security' is already recorded at seat_keys[1]; a repeated
  seat_id is refused rather than resolved by file order
```

1. **The single-row cap.** `REGISTER_MVP_SINGLE_ROW = 1`. A second body needs a
   second AUTHORITY row — it cannot descend from `row-mrc-0001`, because
   `_check_seat_keys` requires an entry's `council_ref` to equal the authorizing
   row's `holder_ref`, and that row's holder is
   `agent:merge-readiness-council`. So the cap is not a stylistic bound here; it
   is the thing that makes a second council unrepresentable.
2. **Seat-name uniqueness is GLOBAL, not per council.** The reader's `seen`
   table is keyed on `seat_id` alone across every entry in the file.
   `gate_rules_council` seats `lead-security` and `lead-quality` and
   `company-policy-lead` — three names `merge_readiness_council` already
   records. Three collisions, refused as duplicates of a different body's
   seats. This defect is invisible until a second council arrives, which is why
   nothing has found it before now.

The runtime side, by contrast, is ALREADY READY — checked, not assumed.
hermes-install's `derive_projection`
(`src/hermes_install/review_authority/derivation.py`) keys its duplicate table
on the PAIR `(council_id, seat_id)`, joins each seat to its own authorizing row
through `_rows_by_id`, and reports `councils` as a sorted set. **The projection
can already carry two bodies; only the reader cannot.**

So the order is fixed and is not negotiable:

**openXwallet reader widening → openxFactory pin advance + gate-literal move →
Brett's mint and register act → projection refresh → the first signed
gate-rules convening.**

## What is specified, and what is performed

| | Specified here | Performed here |
|---|---|---|
| The seats, by id | yes | no |
| The wallet / grant / attestation / row shapes | yes | no |
| The mint ceremony | yes (a runbook) | no key is minted |
| The reader widening | yes (as an owed openXwallet change with its red-first tests named) | no code is written |
| The pin advance and the gate literals | yes (as tasks with exact values) | no |
| The projection refresh and the first signed convening | yes (as named owed acts with owners) | no |

## The seats

From codexFactory `hermes/domain/review-councils/gate-rules.yaml` on
`origin/main`, read by identifier and with nothing invented:

| Seat id | Layer | Status in the roster | This change |
|---|---|---|---|
| `lead-architect` | domain | unconditional member | **REGISTER** |
| `lead-security` | domain | unconditional member | **REGISTER** (name collides with the mrc seat — see defect 2) |
| `lead-quality` | domain | unconditional member | **REGISTER** (name collides) |
| `company-policy-lead` | tenant (`members.client.seat`) | unconditional member; `missing_required_seat: refused` names it *"a gate-rules council without its client seat cannot set rules for that repo"* | **REGISTER** (name collides) |
| `client-security-compliance-officer` | tenant | named as `conjunction_pull_in.persona`, NOT as a seat id | **DEFERRED** — open question Q-GRC-4 |
| `intent_owner_role_slot` | project | `binding: symbolic_until_project_roster`, explicitly SYMBOLIC | **DEFERRED** — open question Q-GRC-4 |

**Four seats are registered. Two are deferred and named**, because the register's
own text refuses a seat the council does not seat: *"Adding a seat here that the
council does not seat records authority nothing will ever present."* A symbolic
slot and a persona with no seat identifier are exactly that.

## What each registered seat gets

ONE body, ONE row, FOUR keys — the same arithmetic the merge-readiness council
already stands on, and deliberately not a per-seat grant:

* **One wallet** — `wal-agent-grc-0001`, holder `agent:gate-rules-council`,
  custody `holder_readable`, carrying an operator-vaulted root key
  (`key-grc-0001`) plus the FOUR declared seat keys. Five declared keys, exactly
  the shape `wal-agent-mrc-0001` took at `wallet-v1.3`, and for the same
  ratified reason: the pinned reader's rule (r) refuses an exercise record
  presenting a key no wallet DECLARES.
* **One custody attestation** — `custody-attest-wal-agent-grc-0001.yaml`.
  Without it the unattested cap applies and the grant reaches only `request`.
* **One root grant** — `grant-grc-0001`: `acts: [review]`, `objects:
  [opensoft/openxFactory]`, `authority_tier: act`, `issued_by` the anchored
  operator, `approval_posture` byte-identical to `grant-mrc-0002`'s.
* **One register row** — `row-grc-0001`, exactly the nine fields the reader
  enforces as an exact set, with `expires_at` character-for-character equal to
  the grant's, because the reader compares the two.
* **Four `seat_keys` entries** — `council_ref: agent:gate-rules-council`,
  `council_id: gate_rules_council` (the reader checks the two denote one body),
  `authorizing_row: row-grc-0001`, one `key_id` and one recomputing
  `key_fingerprint` each.

## What this change refuses to pretend

* **It does not claim the seats will be exercised.** `gate_rules_council` has
  NO automated lane: its own roster says a gate-rules convening *"is an
  assembled packet process, not an automated lane"* and that *"what is still
  missing is a caller"* (codexFactory task 5.9a). Registering the seats makes a
  signed convening POSSIBLE; it does not make one happen, and the ratification
  record for PR #165 says plainly that no seat was run.
* **It does not claim a composition is pinned.** `gate-rules.yaml` carries no
  `composition_source_map` and codexFactory's `hermes/domain/agent-mixes.yaml`
  declares a `review_council_profiles` entry for `merge_readiness_council`
  ONLY. There is nothing to pin today, so authoring it is a prerequisite act in
  codexFactory, not an assumption here.
* **It does not close the floor-reachability gap it widens.** codexFactory's
  floor names `governance/review-authority/register.yaml`,
  `contracts/openxwallet-pin.yaml` and the `openXwallet` gitlink — and omits
  `grants/`, `wallets/` and `attestations/`, a PRE-EXISTING gap recorded at
  `split-openxwallet-repo` §8.3 with lead-security's 2026-08-26
  floor-reachability finding still standing. This change adds THREE MORE files
  into that unfloored space, one of which is the grant conferring the
  rule-setting body's own authority. The gap is named with an owner (tasks §4)
  and is NOT declared closed.

## Delta summary

`specs/review-authority-intake/spec.md` — **7 ADDED requirements**, no MODIFIED
and no REMOVED:

1. A second commissioned body enters the register as its own authority row.
2. Seat identity is the pair (`council_id`, `seat_id`), never the seat name alone.
3. A body with no declared composition is not issued review authority.
4. A symbolic seat and a conditionally pulled-in persona are not registered until the council seats them by identifier.
5. The rule-setting body never clears a candidate that edits the register or the artifacts that confer its own authority.
6. A register act a pinned reader cannot represent is sequenced behind the reader and never worked around.
7. One revocation staleness bound governs the whole register.

**No `## MODIFIED Requirements` block.** The MVP shape requirement in
`add-wallet-carried-review-authority` is not amended: its own scenario *"The
minimal shape is exceeded → the additional scope is a named successor rather
than part of the first shape"* is the door this change walks through, and
requirement 1 is that named successor. Editing an active sibling's ratified
text from outside would be the wrong instrument for a door it already left open.

## Open questions

Every one of these is a QUESTION for Brett, with a recommendation. None is
decided here.

### Q-GRC-1 — Where do the four private halves live, given that no gate-rules lane exists?

The merge-readiness seat keys are `holder_readable` because their private halves
sit in codexFactory's `worker-credentials` environment and the `deliberate` job
reads them out of its own process environment — that job IS the holder's
execution context, so the custody declaration describes reality. **For
gate_rules_council there is no such job.** Two exits:

* **(i) Mint into `worker-credentials` now**, `holder_readable`, with the
  custody attestation naming the OWED job (codexFactory task 5.9a) as the
  holder execution context and saying plainly that it does not exist yet.
* **(ii) Mint operator-vaulted now** and re-declare custody when the lane lands
  — a second ceremony, and a wallet whose custody line changes under a live row.

**Recommendation: (i).** The doctrine that minted the mrc conditional seat with
its unconditional trio — *"a candidate whose class seats `company-policy-lead`
must not be the convening that discovers a missing key"* — argues for minting
ahead of the caller, and (ii) buys nothing except a rotation. The attestation
must state the honest posture: the context is named and owed, not observed.

### Q-GRC-2 — The composition pin for a body that has none (Q8's reserved half)

**Q8(d) IS ALREADY RULED and this change does not reopen it**: *"Exact model
versions only. A hosted holder may NOT pin a model family … today's validation
failure is ratified as intended behavior"* (rulings-2026-08-26). What is
genuinely open is narrower and is the half the queuing ruling reserved:
gate_rules_council is a rule-SETTING body convened as an assembled packet, and
it has no declared composition at all. Does it get one, and what is the blast
radius when it does?

**Recommendation: pin it, exactly, from the same enrolled roster**, mirroring
merge-readiness's six declared components — and accept the coupling openly: one
roster model-pin flip (as on 2026-08-31) then revokes BOTH bodies' grants at
once and parks both, which is a scheduled two-body re-issuance with one walk
record per body, not one act for two. The alternative — leaving the rule-setting
body uncomposed so it never drifts — would give the body that sets the rules the
only authority in the estate that no drift cascade can revoke. That is the wrong
body to exempt.

### Q-GRC-3 — The expiry horizon for `grant-grc-0001`

`grant-mrc-0002` expires `2027-06-30T00:00:00Z`, ruled by Brett as option A3 and
bound to the Operator identity record's own review expiry, itself bound to the
earliest published retirement floor among the pinned seat identifiers.

**Recommendation: the same date, `2027-06-30T00:00:00Z`**, so one re-issuance
ceremony covers both bodies and the two grants cannot silently diverge. The
honest caveat travels with it unchanged: nothing in this estate reads a
retirement date, and the expiry is a scheduled event with a named human owner,
not a control.

### Q-GRC-4 — The two deferred seats

`intent_owner_role_slot` is symbolic until the subject-layer roster lands.
`client-security-compliance-officer` is named as a PERSONA on a conjunction
pull-in, not as a seat id, and its predicate `rule_touches_security_posture` has
an implementation and no caller.

**Recommendation: register neither now; do not delete either.** Record both as
owed registrations that trigger on a codexFactory roster act — the project
roster binding for the first, a seat identifier for the second — and require
that whichever act binds them registers the key in the same governed act, so the
first convening that seats them is not the one that discovers a missing key.

### Q-GRC-5 — Does the second row retire the cap, or raise it?

The reader widening can either DELETE `REGISTER_MVP_SINGLE_ROW` or raise it to
a declared number.

**Recommendation: replace the scalar cap with the invariant it was standing in
for** — every row resolves end to end, every seat entry attaches to a row that
commissions its body, and (`council_id`, `seat_id`) is unique — rather than
substitute the number 2 for the number 1. A cap of 2 would have to be edited
again by the third body and would say nothing true about why two is right. This
is openXwallet's decision to make in its own change; it is recorded here because
this change is the one asking for it.

## Sequencing, restated as a single order

1. **openXwallet** — the reader widening, red-first (tasks §2). Its own OpenSpec
   change, its own bundle tag.
2. **openxFactory** — pin advance (`commit:`, `contract_bundle_tag:`) plus the
   consumer gate's literal assertions, ONE pull request. Both paths are
   never-clearable floor members, so it is human-landed by construction.
3. **codexFactory** — the `gate_rules_council` composition source map and agent
   mix profile (Q-GRC-2), before the grant is issued.
4. **Brett's walk** — mint, attest, grant, row, in that order, one walk record
   (tasks §3). Human-only surface; nothing agent-written.
5. **hermes-install / operator** — the projection refresh; the visible signal is
   `seat_count` moving 4 → 8 and `councils` gaining `gate_rules_council`.
6. **codexFactory** — the caller that convenes gate-rules and returns signed
   seat returns (task 5.9a). The FIRST SIGNED CONVENING is the gate that makes
   the queuing ruling's *"so later convenings are signed"* true, and it is not
   this change's to perform.

Steps 1–2 have no valid interleaving with step 4: there is no ordering in which
the register carries a second row and the required check is green at the pinned
reader. That is the finding, and it is why this proposal is a sequencing
document as much as a specification.
