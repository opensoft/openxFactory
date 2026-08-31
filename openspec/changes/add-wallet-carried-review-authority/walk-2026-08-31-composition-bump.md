# Walk record — the 2026-08-31 composition bump, against `docs/governed-reissuance-runbook.md`

Status: record
Kind: report
Repository context: openxFactory
Walked: 2026-08-31
Runbook walked: [`docs/governed-reissuance-runbook.md`](../../../docs/governed-reissuance-runbook.md)
  at openxFactory `65c3a803` (PR #527) — `Status: draft`
The bump: codexFactory **`6edecaf13e88fc56f9a7182b93a0d48cc2e40541`** (PR #146),
  the alias-to-exact enrolled-roster model pin flip
Roster-change record: codexFactory
  `hermes/domain/review-councils/records/2026-08-31-enrolled-roster-model-pin-flip.md`
Commissioned by: task 7.6 — *"Write the governed re-issuance RUNBOOK for a
  provider alias roll, and walk it once against a deliberate composition bump"*,
  with its own constraint that *"the runbook and that flip are one act, not two"*

---

## 0. THE HEADLINE, BEFORE THE DETAIL

**This walk exercised steps 0–4 and step 6's watch. It did NOT exercise step 5,
step 5a or step 5b, because NOTHING WAS REVOKED, RE-ISSUED OR RE-PROJECTED in
this walk.** §5 below says exactly which acts were not performed and what a real
provider roll would additionally exercise.

**The reason is not an omission — it is what this bump was.** The flip was an
**alias-to-exact precision pin** whose C13 question (*does this re-open the
soak?*) was **ruled and discharged in the same act** by the Gate-Rules Council
on the 25/25 and 8/8 identity measurement (2026-08-29 §8.2). Nothing about the
served artifact changed; what changed is that the declaration now names it. A
**provider roll** — the case the runbook is titled for — is the other shape, and
it is the one that drives steps 5/5a/5b.

**So this walk demonstrates the runbook against a real declared composition
change. It does not demonstrate a recovery from a revocation, and it must not be
cited as though it did.**

---

## 1. Step-by-step: what each runbook step produced

| Runbook step | Exercised? | What it produced, and where the evidence lives |
|---|---|---|
| **Before you start** | yes | Ownership confirmed (the declaration is codexFactory's, not this repository's); the ratifying human available; the superseded grant's own file open at §2 below |
| **§0.1 trigger** | yes | `model_version` identified as the single declared component the bump touches — **measured, not assumed** (§2.2) |
| **§0.2 not-a-component** | yes | The runtime and the CLI helper `claude-haiku-4-5-20251001` named as undeclared; carried into the record's §5 and §11 |
| **§0.3 who holds which act** | yes | Six roles kept separate; **three capacities, one human, disclosed** — record §10 |
| **§1 superseded state** | yes | §2 below: the declaration quoted, the active grant and row quoted, the composition identity recorded with its honest substitute label |
| **§2 the bump as ONE change** | yes | §3 below: one commit set, green whole and **red partial, proved** |
| **§3 in-flight (R9)** | **NO — vacuously** | **No convening was in flight and none parked.** §5.1 |
| **§4 re-issuance record (R8)** | yes, **with PENDINGs** | §4 below: all five fields written, two of them PENDING with what they wait on |
| **§5 the register act** | **NOT PERFORMED** | §5 below — it is a pointer in the runbook and it stays owed |
| **§5.1 revoke / mint / repoint** | **NOT PERFORMED** | §5 below |
| **§5.2 step 5b projection** | **NOT PERFORMED** | §5 below |
| **§6.1 lifecycle watch** | yes | Record §11 — three pinned identifiers plus the runtime/reseed row, each with a named human owner, under LQ-C5's own caveat |
| **§6.2 roll recovery** | **NO** | Not a roll. §5.4 states what a roll would additionally exercise |
| **§7 record the act** | yes | This document |

---

## 2. Step 1 — the superseded state, as established

### 2.1 The declaration before the bump

codexFactory at **`01a0c64a49cd46c6b6c6f97330cf66bcc7a81ffd`** (the flip's first
parent), `hermes/domain/agent-mixes.yaml`,
`review_council_profiles.merge_readiness_council.model_assignments` — all four
seats identical in shape:

```yaml
      <seat>:
        selector: opus | sonnet
        selector_kind: mutable_provider_alias
        pin_status: required_by_s5
```

and the tenant's authority record, `hermes/client/role-overrides.yaml`:

```yaml
    seat_representation:
      seat: company-policy-lead
      model: sonnet
      declared_by: gate_rules_council
      decided: "2026-08-26"
```

### 2.2 The composition identity, before and after — and its HONEST LABEL

> **THIS IS NOT THE CANONICAL COMPOSITION HASH, AND MUST NOT BE READ AS ONE.**
> R6 (the plane sits INSIDE the digest) and R7 (JCS / RFC 8785,
> `sha256:<lowercase-hex>`, recorded with the profile name and version) are
> **ratification targets on a change that is not yet authored** — *"none of them
> is implementable until the change that carries them is authored and
> ratified."* The runbook's §1 therefore prescribes recording a **substitute**
> and labelling it as one. This is that substitute.
>
> **Definition, so it is reproducible:** for each of the six declared
> components, the resolved YAML sub-document at the named commit, serialized as
> JSON with sorted keys and `(",", ":")` separators (dates coerced to their
> string form), SHA-256'd. **Local, ad-hoc, and defined here only.**

| Component | Before (`01a0c64a`) | After (`6edecaf1`) | |
|---|---|---|---|
| `model_version` | `3ff506b8af0c…` | `a5c245462beb…` | **MOVED** |
| `prompt_contract` | `03788bddfc3c…` | `03788bddfc3c…` | unchanged |
| `tool_manifest` | `626b16144165…` | `626b16144165…` | unchanged |
| `policy_version` | `6b86b273ff34…` | `6b86b273ff34…` | unchanged |
| `parameters` | `0e72c8e83f10…` | `0e72c8e83f10…` | unchanged |
| `retrieval_corpus` | `144518dda2c8…` | `144518dda2c8…` | unchanged |

In full, for the one that moved:

* before — `sha256:3ff506b8af0c830ea0b254ca10ccc230977ac2f8c0d838a2110d52eae140c73e`
* after — `sha256:a5c245462bebb81dfc8a5cf2743b709a1882674e67eca98a823de09f05388aeb`

**EXACTLY ONE OF SIX MOVED**, which is the runbook's §0.1 claim discharged by
measurement rather than by assertion. The `prompt_contract` component's own
declared `rendered_set_digest`
(`sha256:9e66f1ad83be6dd1e4920a199567b3dc76923077a6c5ed9cd1ba67a3fb1d0140`) was
**independently recomputed** from the canonical builder during the CSC-C1′
inventory and reproduced exactly — a second, differently-derived witness that
the prompt half did not move under a change that opened the same file.

And the declaring-file blob shas the runbook's §1 asks for:

| File | Before | After | |
|---|---|---|---|
| `hermes/domain/agent-mixes.yaml` | `7ce0102f2fb0` | `28f2acb90fb1` | moved |
| `hermes/client/role-overrides.yaml` | `2c71ff01d624` | `a84c26d15c7d` | moved |
| `.github/workflows/council-deliberation-worker.yml` | `a93738a14151` | `6f527ca3e681` | moved |
| `hermes/domain/review-councils/merge-readiness.yaml` | `78e5c651e0be` | `78e5c651e0be` | **unchanged — no seventh component was declared** |

### 2.3 The active grant and its backing row — quoted, and UNCHANGED BY THIS WALK

`governance/review-authority/grants/grant-mrc-0001.yaml`:

```yaml
grant_id: grant-mrc-0001
audience: {wallet_ref: wal-agent-mrc-0001, holder_ref: agent:merge-readiness-council}
scope: {acts: [review], objects: [opensoft/openxFactory], authority_tier: act}
expires_at: "2026-11-23T12:00:00Z"
issued_at:  "2026-08-25T12:45:00Z"
issued_by:  Brett.Heap@opensoft.one
state: active
```

`governance/review-authority/register.yaml`, `rows[row_id: row-mrc-0001]` — all
nine fields, as a set, because the reader enforces exact set-equality over them:
`row_id`, `holder_ref: agent:merge-readiness-council`,
`wallet_ref: wal-agent-mrc-0001`, `target_repo: opensoft/openxFactory`,
`act: review`, `authority_tier: act`, `grant_ref: grant-mrc-0001`,
`expires_at: "2026-11-23T12:00:00Z"`, `state: active`.

**Both are byte-identical after this walk.** Neither file was touched by PR #146,
PR #527 or this record.

---

## 3. Step 2 — the bump, as ONE change

**Identity of the bump: codexFactory merge commit `6edecaf13e88fc56f9a7182b93a0d48cc2e40541` (PR #146).**
codexFactory disallows squash, so the merge commit is the bump and its history is
intact beneath it.

**Green whole.** CI `validate` on codexFactory `main` **after** the merge:
`1657 passed, 12 skipped`, `docs validation ok (1 checks skipped)` (run
`33369133430`). That is the CI number on the landed tree, not a clone's.

**Red partial — proved, not asserted.** The one-commit-set rule was demonstrated
by reverting each half against saved bytes and running the named test:

* domain roster flipped, **tenant not** → `test_R23_the_domain_roster_is_bound_to_the_tenant_declaration` **red**
* tenant flipped, **domain not** → the same test **red**
* a **one-seat partial** flip → `test_the_enrolled_seat_roster_is_the_recorded_map` **red**

**21 mutations in total, each anchor-checked before mutating, all red**, plus two
vacuity probes and two must-stay-green tests
(`test_s5_pin_masquerade_is_rejected`,
`test_the_signed_projection_is_the_posted_seat_block`) green and unmodified. The
full harness output is in PR #146's fix-round comment.

**And the enumerate-before-you-edit step of the runbook found two real defects**,
which is the strongest evidence the step earns its place: a mutation whose
literal had gone stale drifted **nothing** while still passing, and a
forbidden-literal guard was checking for **dead values**. Both were fixed in the
same commit set.

---

## 4. Step 4 — the R8 re-issuance record

The five fields are the **MINIMUM**, and a field that cannot yet be filled says
what it waits on rather than being quietly omitted.

| R8 field | Value |
|---|---|
| **superseded grant reference** | **`grant-mrc-0001`** — the root grant, `state: active`, issued 2026-08-25T12:45:00Z by `Brett.Heap@opensoft.one`, backing `row-mrc-0001` |
| **superseding grant reference** | **PENDING — the register act (runbook step 5) has not been performed.** It does not exist before that act, and inventing an id would be a forgery. See §5 |
| **composition hash issued against** | **PENDING R6/R7** — no canonical digest is implementable yet. Recorded instead as the per-component substitute of §2.2 at codexFactory `6edecaf1`, explicitly labelled a substitute |
| **ratifying human** | **Brett Heap** (`Brett.Heap@opensoft.one`), the anchored responsible operator under the Human Escalation Contract |
| **effective time** | **PENDING with the register act.** The bump's own instant is codexFactory `6edecaf1`; the *effective time of a superseding grant* is set when that grant is minted |

**Beyond the minimum — what this act actually carries** (R8 is a floor, and
adding is the ruling working as intended):

* **the selection**: codexFactory `records/2026-08-29-gate-rules-s5-seat-model-selection.md`, §8 the sole disposition — **CONDITIONAL SELECT, 5/5 unanimous ACCEPT AS AMENDED**, and **5/5 that no slot can carry an unqualified SELECT** on that evidence;
* **the roster change**: `records/2026-08-31-enrolled-roster-model-pin-flip.md`;
* **the acceptance**: that record's §10, spoken by Brett Heap in session on 2026-08-31, with the Lead-Quality conflict disclosed on the face of the act;
* **the identity assertion** linking the alias the 2026-08-26 ratified record ruled to the exact identifier now pinned — `opus → claude-opus-5` 25/25, `sonnet → claude-sonnet-5` 8/8 — cited to the selection record's §2.2 and made load-bearing by a live test;
* **the supersession, IN PROSE**, because §5.1 of the runbook records that no grant field carries it: the pinned grant schema is `additionalProperties: false` with no `supersedes` key, and `parent_grant_ref` means *derived from*;
* **every condition still outstanding**, as the record's §8 table.

---

## 5. What this walk did NOT exercise — and why

### 5.1 Step 3 (R9's in-flight park) — VACUOUSLY NOT EXERCISED

**No convening was in flight when the bump landed, and none parked.** The
runbook's step 3 describes what happens to work already running; there was none.

**And no convening has run at the new pins since.** Every
`council-deliberation-worker` run in the repository's history at the time of
writing is at `01a0c64a` — the flip's first parent. **The first post-flip
convening is still ahead**, which is also why **CSC-C1′ part 2** (the lane
carrying the read-back into a *retained* artifact) is **still not evidenced by a
lane run**; the record says so in its own §4.

### 5.2 Steps 5 and 5.1 (the register act; revoke / mint / repoint) — NOT PERFORMED

**Nothing was revoked, nothing was minted, no row was repointed.**
`grant-mrc-0001` is still `state: active` and `row-mrc-0001` still points at it
(§2.3, verified byte-identical).

**This is the runbook working as written, not a step skipped.** Its §5 is a
**POINTER ONLY**: the register act is sequencing **step 5** of
[`rulings-2026-08-29.md`](rulings-2026-08-29.md), a **human-ratified act on a
permanently human-only surface**, and *"this runbook does not perform step 5,
and walking it does not."*

**THE SUBSTANTIVE GAP, STATED PLAINLY RATHER THAN LEFT TO BE NOTICED.** The
ratified rule is that a declared composition change ends the holder's certified
identity and requires a governed re-issuance. **The declared composition moved
on 2026-08-31 and no re-issuance has been performed**, so the register today
carries an active grant issued against the composition that preceded the bump.
That is precisely the gap the register act closes, and it is **why task 7.7's
gate is not met**.

**It is NOT, today, a mechanical validation failure, and the reason is worth
recording so nobody reports it as one.** The rule that fires — the validator's
`declared-change-not-revoked` — keys on a **wallet composition RECORD** (`kind:
xfactory_wallet_agent_composition`) carrying `grants_state:
revoked_on_composition_change` beside a still-active grant. **No such record
instance exists anywhere in either repository** (verified by search): codexFactory
declares a composition **source map**, which is a different artifact. And the
drift-cascade change's own enforcement surface is **declared and not built**. So
the estate is consistent with what it has declared; what it has not yet done is
the re-issuance.

### 5.3 Step 5b (the projection) — NOT PERFORMED

The Hermes register projection was **not re-derived**, because there was nothing
to project: the register is unchanged. Step 5b exists to reach the runtime after
a register act, and there was no register act.

### 5.4 What a REAL provider roll would additionally exercise

Recorded so the residue of this walk is legible, and so 7.6's remaining half is
a named thing rather than a feeling:

1. **A detection path** — §6.2's mismatch, surfaced by the R-I served-model
   read-back: an exact declaration absent from the served map refuses. Here
   nothing mismatched; the read-back **agreed** at all four seats.
2. **A real park under R9** — an in-flight convening refusing with a named
   refusal, no grandfathering, no admission stamp honoured.
3. **The three atomic writes of §5.1** — revoke with a `revocation` block of
   class DRIFT naming the composition event; mint a new grant; repoint
   `grant_ref`/`expires_at` with the row's own `state` staying `active` — and
   the property that **no order of them is green halfway**.
4. **Step 5b** — the projection re-derived, `revocation_staleness_bound` carried
   verbatim, and **one convening watched admitting**.
5. **The budget interaction** (LQ-C2) — refusals recommission and the budget
   binds at commission (`max_convenings_per_rolling_24h: 12`), so a roll can
   park a surface for reasons unrelated to the roll.

**None of the five happened here. A walk that exercised them is a different,
later walk.**

---

## 6. The honest limits, restated in terms

* **R8 and R9 ARE NOT ENFORCED.** Task 7.6's own sentence: *"neither ruling is
  enforced until the change carrying R6–R12 is ratified."* This walk
  demonstrates the runbook against a real bump; **it does not exercise an
  enforced control**, and no gate in this estate would have refused a bump that
  ignored the runbook entirely.
* **THIS WALK DOES NOT EVIDENCE THE PLANE.** R5 requires the plane to be
  evidenced by read-back and never inferred; that is the **Operator's Packet 2
  identity record**, which is sequencing **step 3** and is **intentionally not
  performed**. The `env -i` scrub was not reproduced in the CSC-C1′ inventory,
  and the runtime-reported `provider` field recorded there is **not** offered as
  plane evidence. *"This Council does not evidence the plane and must not appear
  to."*
* **NO FULLY-PINNED-COMPOSITION CLAIM IS MADE.** `claude-haiku-4-5-20251001`
  executed in 33 of 33 corpus judgments and in **4 of 4** inventory invocations,
  is declared in no composition file, is unpinned by this flip, and carries the
  register's earliest floor (**2026-10-15**). Whether it becomes a seventh
  component or lives under `parameters` belongs to the R6–R12 change. The
  **runtime** is likewise not one of the six.
* **NOTHING IS ACTIVATED.** `lead-integration` remains CONDITIONAL with
  activation **held on LA-C3**, and the whole bench remains blocked at
  `advisory_soak_recorded` and `seat_diversity_disposed_on_soak_evidence`.
* **NOT ONE COMMISSIONED SOAK HAS RUN. NO ROW EXISTS.**

---

## 7. Ledger movement this walk supports

Argued in [`tasks.md`](tasks.md) beside each task, with the task's own text
quoted at the tick. In summary:

* **7.5 — TICKED.** Its text is *"Pin model version and prompt corpus as declared
  components; forbid the candidate repository at HEAD as retrieval corpus"*, and
  all three halves are now declared, pinned and test-enforced. Every blocker its
  own ledger named is discharged **by name**, not by lapse.
* **7.6 — STAYS UNTICKED**, on its own sentence, and on a second independent
  ground: this was a precision-flip walk, not a revocation-class one (§5.4).
* **7.7 — STAYS UNTICKED.** Its gate needs a rehearsed revoked-holder park; §5.1
  and §5.2 record that no park happened and no re-issuance was performed.
