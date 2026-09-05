# Realization evidence: add-release-tag-gate § 4, 2026-09-05

Status: record
Kind: report
Captured: 2026-09-05, in lane `openxfactory-max001` (session `5e783e4d`), on
branch `change/archive-add-release-tag-gate`, cut from `main` at
`9e869acc` — two commits above `7ee0e73d`, the merge of openxFactory PR #668
that ratified and realized this packet. **This record is CAPTURED AT MERGE of
the archive pull request that carries it**; after that merge it is written once
and never edited.

**Why this file exists.** `tasks.md` § 4 says, in its own preamble: *"A check
that is not REQUIRED enforces nothing. Until § 4.1 is performed, the obligation
this packet moves out of `pytest-suite` is enforced by a workflow anyone can
merge past, which is strictly weaker than the state before this change.
Ratification does NOT wait on this group; **ARCHIVE DOES.**"* This is that
evidence. Under `release-realization` a change with a non-empty `code_surface`
archives only on MERGED code plus GREEN evidence, measured after landing and
never assumed.

**What is asserted here, and on whose reading.** Every id, sha and timestamp
below was read back from the GitHub API by this lane with `gh api` while this
file was written, and independently by the convening coordinator. **§ 4.1 is an
`[OPERATOR]` act and no agent performed it** — the task's own text says "an
agent-reported 'ruleset created' without the console act is not evidence". The
console act was Brett's; this lane read the result back.

---

## 1. The two rulings this discharges

Brett Heap, in session, in order:

1. **2026-09-05 — _"ratify 668, land it when green"_.** Ratification, recorded
   at `ratification-2026-09-05.md`; it settled the packet's content and its
   landing condition and **explicitly did not settle the `[OPERATOR]` act**,
   which that record's § 4 says in terms.
2. **2026-09-05 — _"ruleset updated, do the evidence and archive it"_.** The
   authority for this record and for the archive act it opens.

## 2. § 4.1 — the required status check, read back rather than reported

`gh api repos/opensoft/openxFactory/rulesets/21538893`:

```json
{
  "id": 21538893,
  "name": "openxFactory wallet-gate (require wallet-validation)",
  "target": "branch",
  "source_type": "Organization",
  "source": "opensoft",
  "enforcement": "active",
  "created_at": "2026-08-26T03:08:36.077-04:00",
  "updated_at": "2026-09-05T00:36:49.902-04:00",
  "conditions": { "include": ["~DEFAULT_BRANCH"], "exclude": [] }
}
```

Its `required_status_checks` rule parameters:

```json
{
  "do_not_enforce_on_create": false,
  "required_status_checks": [
    { "context": "wallet-validation" },
    { "context": "pytest-suite" },
    { "context": "lane-line" },
    { "context": "release-tag-gate" }
  ],
  "strict_required_status_checks_policy": false
}
```

**`release-tag-gate` is the fourth context and it was not there before.** The
ruleset's `created_at` is 2026-08-26 and its `updated_at` is
**2026-09-05T00:36:49.902-04:00 (= 04:36:49Z)** — the console act, ten hours
after this packet's first push and two hours after PR #668 landed.

**No ruleset was created for this.** The task named `21538893` precisely because
it already carried `pytest-suite`, the check the moved assertion came out of, so
the gate now sits beside the suite it left rather than in a ruleset of its own.
The `pin-validation` ruleset `22272824` cited in § 4's preamble is
`opensoft/MedxChart`'s and was only ever the SHAPE precedent for an
`[OPERATOR]` task with evidence before archive; this repository has no
`pin-validation`, which the packet corrected during its adversarial round.

## 3. The same fact from the branch's own side

`gh api repos/opensoft/openxFactory/rules/branches/main` — what `main` actually
enforces, rather than what a ruleset declares:

```json
[
  { "ruleset_id": 21957695, "contexts": ["signed-execution-chain-gate", "lane-line"] },
  { "ruleset_id": 21538893, "contexts": ["wallet-validation", "pytest-suite", "lane-line", "release-tag-gate"] }
]
```

`release-tag-gate` is listed among the contexts `main` requires. **Both halves
are recorded because they can disagree**: a ruleset can be `active` and still
not reach a branch if its conditions do not select one, and the branch-rules
endpoint is the reading that answers "is this enforced HERE".

## 4. § 3 — the realization that is being gated

**openxFactory PR #668**, *"Move the release-tag zero-findings pin out of the
required suite into a gate on the cutting pull request (add-release-tag-gate)"*,
merged **`7ee0e73d655b32d81b70478bd14320633bb5c9f2`** at
**2026-09-05T02:13:55Z**, carrying the workflow, the validator, the moved
assertion, the twenty-four gate tests, the spec delta, the policy paragraph, the
README row, the ledger row and the ratification and verification records.

Its final head `35082aaa` was green on all nine checks, `pytest-suite` reading
`selected=9638 passed=9617 skipped=21 failures=0 errors=0`.

## 5. § 4.2 — one green run under the REQUIRED regime

**The distinction that makes this line worth writing:** every
`release-tag-gate` run before 04:36:49Z was green on a check that was ADVISORY.
A green advisory run is not evidence that a required context reports; a required
context that fails to report blocks the merge forever, which is the failure mode
`tasks.md` § 3.2 designed the missing `paths:` filter against.

The runs before the console act, for completeness — all `success`, all advisory:

| run | branch | created |
| --- | --- | --- |
| `33927889060` | `change/add-release-tag-gate` | 2026-09-04T23:01:33Z |
| `33932616773` | `change/add-release-tag-gate` | 2026-09-05T00:19:55Z |
| `33933031517` | `change/add-release-tag-gate` | 2026-09-05T00:27:21Z |
| `33937403224` | `change/add-release-tag-gate` | 2026-09-05T01:51:24Z |
| `33938798720` | `fix/review-lane-pin-stale-count` | 2026-09-05T02:20:34Z |

**No `release-tag-gate` run has occurred since 04:36:49Z**, so the first green
run under the required regime is **this archive pull request's own**, and it is
cited here rather than borrowed from another branch:

> **FIRST REQUIRED GREEN RUN: `33945259576`** — openxFactory **PR #672**
> (`change/archive-add-release-tag-gate`), head `ac3d4502`, workflow
> `release-tag-gate`, event `pull_request`, started **2026-09-05T04:41:54Z**,
> completed **2026-09-05T04:42:08Z**, `status: completed`,
> **`conclusion: success`**.

**IT IS CONFIRMED REQUIRED, NOT ASSUMED REQUIRED.** `gh pr checks` shows a
green tick; it does not say whether the context is enforced. The GraphQL
`statusCheckRollup` does, per pull request, and it answers for this one:

```
wallet-validation            required=true
pytest-suite                 required=true
signed-execution-chain-gate  required=true
lane-line                    required=true   SUCCESS
release-tag-gate             required=true   SUCCESS
```

**`release-tag-gate` is `isRequired: true` and `SUCCESS`** on this pull request
— five minutes after the console act at 04:36:49Z, and the first run of that
workflow anywhere since it.

It short-circuited, as it must: this pull request touches no release-surface
path. Its log, verbatim:

```
Complete job name: release-tag-gate
no release surface change: none of the 2 changed path(s) between 9e869accf and
491b27670 is contracts/manifest.yaml or under contracts/releases/
```

That is the same proof the packet's own pull request gave, now given **under
enforcement** — and `Complete job name: release-tag-gate` is the second half of
it: the check surfaces under exactly the literal token the ruleset pins, which
is what makes the tick above the same object the ruleset names.

**A LATER HEAD ON THIS PULL REQUEST RE-RUNS THE GATE**, the archive act landing
in a commit after this one. That later run is the same short-circuit over a
larger diff and is not a second discharge; this run is the one § 4.2 cites,
because it is the FIRST under the required regime.

## 6. What this evidence does NOT discharge

**`tasks.md` § 4.3.** The first pull request the gate judges FOR REAL is the
next one that touches `contracts/manifest.yaml` or `contracts/releases/**`.
PR #653 (the `contract-v3.4` cut) is not it — it merged before this packet was
authored and is used only as replay evidence. This archive does not wait on
that, and § 4.3 is carried forward as a recorded successor rather than ticked.

**The accepted `release-inventory-drift` `error`.**
`docs/contract-versioning-policy.md` is a digested member of the published
`contract-v3.4` bundle, so naming the gate in its § Bundle Realization Order is
non-editorial drift that the governing scenario calls a **defect**. It was
ratified knowingly and **persists until the next contract cut re-digests the
member** — an archive does not clear it and this record does not claim it does.
