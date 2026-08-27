# Council — adversary-engineer seat

Status: draft
Round: council, 2026-08-27
Subject: `adopt-council-cleared-merge-gate`, post-alignment draft
**SEAT VERDICT: APPROVE WITH CONDITIONS** — ten conditions, four of them
blocking in effect ("the boundary may not be ratified as written"). All ten
accepted.

Primary hunt: **LS-A3, "a described control treated as existing"** — this
packet's own subject matter, and therefore the likeliest place for it to hide.
The seat found it four times, twice by executing the shipped enforcer rather
than reading it.

## The LS-A3 audit

| Control relied on | Status | Finding |
| --- | --- | --- |
| `class_floor_problem` "already refuses … for every repository, wired or not" | **SPECIFIED-ONLY for openxFactory** | It validates a *gate rule*, taking `(rule, candidate)`. Two callsites: `validate_rule:1500`, guarded `if candidate is not None`, and `evaluate_with_clearance:2071`. **A repo with no rule gets no evaluation at all** — today's protection is the absence of a mechanism, not a running control. Worse, `:1084 if is_advisory(rule): return None`, so the floor is a **no-op on both classes this change enrolls**. `load_rule()` never passes a candidate and `_config_governs:289` returns False cross-repo, so codexFactory CI validating openxFactory's rule resolves no candidate and skips the floor permanently. `would_pass_class_floor` and `advisory_as_currently_defined` — the helpers that *would* judge an advisory class — have **zero production callsites; tests only.** |
| `GATE_INTEGRITY_FLOOR` | RUNNING | Verified. Correctly floors this packet's own diff. |
| The four proposed allowlist patterns | RUNNING; all four pass | Executed against `origin/main`; `README.md` confirmed absent from `PROTECTED_ROOT_FILES`. Implementable — but see F1/F2. |
| `dismiss_stale_reviews_on_push` composition | RUNNING (inherited); the hardening was **DESCRIBED ONLY** | Named in prose and in no gate. `21538893` also sets `strict_required_status_checks_policy: false`, so an approval surviving a **base** advance was unaddressed. |
| CODEOWNERS as "native, un-spoofable human floor" | RUNNING but **structurally unsatisfiable** | Un-spoofable against the App: correct. But `@brettheap` is the sole owner **and** the `OrganizationAdmin` bypass actor, and GitHub bars self-approval — so for the sole owner this floor can only ever be discharged **by the bypass this change exists to end**, and widening the route to `.github/` *enlarges* that surface. (A pull request cannot edit its own route — GitHub reads CODEOWNERS from base — and `.github/` is class-floored, so that vector is genuinely closed.) |
| The three-stop kill switch | **1 of 3 running** | Stop 2 (`human.kill_switch`, `:1995`, `:2023`) runs; stop 3 (credential removal) is real; **stop 1 depends on S5, which this change itself records as unbuilt.** "Three independent stops" was two. G6's expiry safety rested on the same unbuilt S5. |
| `tasks.md` "carries them as ordered, tagged tasks" | **DID NOT EXIST at review time** | Asserted in front matter and in the gates section; the directory held only `.openspec.yaml`, two alignment records, `proposal.md` and `specs/`. A described ledger treated as existing, in the packet written to prevent that. |

## Findings

- **F1 — the prose class admits agent-instruction files.** `PROTECTED_ROOT_FILES`
  is applied **root-exact** (`:1045`), so `docs/**/*.md` admits `docs/AGENTS.md`,
  `docs/CLAUDE.md`, `docs/sub/AGENTS.md`; verified with `envelope.path_matches`.
  The enforcer's own comment (`:886-894`) records the 2026-08-22 reasoning that
  such files are "gate-bearing, whatever directory it sits in" **and states that
  "the CLASS floor did not follow."** Clearing one is, verbatim, "prompt
  injection into the governance loop." The draft's human-only list said
  "`CLAUDE.md`; `AGENTS.md`" unqualified, converting a root-only control into a
  claimed universal one.
- **F2 — the derived class's allowlist was entirely comparator.**
  `health/neutrality-drift/**` admits
  `health/neutrality-drift/baseline/codexFactory.yaml`, which exists today and
  which `neutrality.py:89-92,599-620` documents as the **immutable** baseline
  `load_baseline` reads back to decide "the docs the scout has already judged."
  `PROTECTED_PATH_SEGMENTS = ("baseline",)` guards **patterns**, not changed
  files: `health/neutrality-drift/**/baseline/**` is refused, the broader glob
  passes, and **no PR-time segment guard exists**. The docstring at `:929-950`
  names the cost verbatim — "a derived root re-admitting its own PREV comparator
  … Exactly what R5 protected, **reachable by moving one glob**." This proposal
  wrote that glob.
- **F3 — `pull-requests: write` is not review-submission-only.** It also permits
  **dismissing a human's `CHANGES_REQUESTED` review**, editing bodies and
  labelling. G4b's evidence constrained neither.
- **F4 — the gate ordering maximises the hazard it names.** G4b and G5 land an
  approval-capable caller with a live token **before** G7's flip, after which the
  only restraint is `is_advisory(rule)` — one field, in a different repository,
  reached through a pin. The proposal names this hazard and then adopts the
  ordering that maximises it. G4(c) also had no stated dependency on G4(a).
- **F5 — the canary records itself.** No recorder named, no mechanical check that
  six records exist, no blinding, so a disagreement is discoverable-then-editable
  by whoever writes the file. **The mitigation the packet should have claimed and
  did not:** `evidence/canary/` sits under `openspec/changes/**`, which
  `GATE_INTEGRITY_FLOOR` floors — so the record **cannot be self-cleared**.
- **F6 — G1 admits a present-but-skipped test.** It demanded the test's path and
  name, not that it run green in CI on hermes-install main. G2's runbook-walk
  record named no verifier.

## The seat's strongest case for refusal, and why it discounted it

> Ratifying a boundary whose mechanism does not exist converts unverified
> preconditions into a standing authorization. A later session reads
> `Status: ratified` as "the boundary is settled, only the gates remain" — and
> the gates are the weakest artifact here. That is LS-A3 relocated one level up,
> from the controls to the packet.

Discounted **conditionally**: the alternative — build the approval path, then
ratify — is exactly what R1's header refuses, and R1 is open now awaiting this
statement. The seat credited the packet's structural honesty as "real and rare"
(it floors its own diff, kills the convener's sketch on doctrine, and adds G4b
against itself) and located the defects in the boundary **text**, "which is
precisely what conditions can fix before ratification rather than after."

## Dispositions

1. **AE-C1 VALID/HIGH — APPLIED.** Prose class carries a depth-independent
   PR-time refusal of the twelve `PROTECTED_ROOT_FILES` basenames;
   `:1045` root-exactness recorded; the unqualified "`CLAUDE.md`; `AGENTS.md`"
   struck from the human-only enumeration and replaced with a root-scoped
   statement that names why the class needs its own guard.
2. **AE-C2 VALID/HIGH — APPLIED, and further than asked.** `health/neutrality-drift/**`
   is **removed entirely**, not narrowed: the tree's only tracked file *is* the
   comparator, so the allowlist contained no legitimate traffic at all. Combined
   with the product-advocate's measurement (three PRs ever touched either derived
   tree), the whole derived class is **demoted to a successor change**. The
   missing PR-time `baseline` segment guard is recorded as an owed codexFactory
   task rather than an assumed control.
3. **AE-C3 VALID/HIGH — APPLIED.** G4 c-iii rewritten. The claim "nothing further
   is owed" is withdrawn and replaced by the two acts actually owed: wire
   `would_pass_class_floor` / `advisory_as_currently_defined` into a production
   gate so an advisory class's floor status is computed rather than skipped, and
   require G7's evidence to include that call returning `None` for the class
   against the real base-branch candidate. **This was the packet's single largest
   reliance and it was specified-only.**
4. **AE-C4 VALID/HIGH — APPLIED.** `tasks.md` authored (13 groups, tagged
   `[OPERATOR]` / `[hermes-install]` / `[codexFactory]` / `[openxFactory]`),
   carrying the `21538893` hardening, the CODEOWNERS widening and the canary
   recorder as gated tasks. The qa-lead's finding 10 is re-marked **APPLIED IN
   PART** at the time the adversary reviewed, and APPLIED now.
5. **AE-C5 VALID/HIGH — APPLIED.** G4b evidence extended: the installation's
   permission set enumerated, `POST /pulls/{n}/reviews` named as the only write
   performed, and a test asserting the caller never calls a review-dismissal
   endpoint.
6. **AE-C6 VALID/MEDIUM — APPLIED.** Ordering restated as
   G4(a) → G4(c) → G4(b) → G5, immediately before G7, so an approval-capable
   token does not idle across an unbounded interval.
7. **AE-C7 VALID/MEDIUM — APPLIED.** The kill switch now states **two** stops
   until G2 is green, with stop 1's dependency on unbuilt S5 named. Same
   correction applied to G6.
8. **AE-C8 VALID/MEDIUM — APPLIED.** Consequence 4 restated: CODEOWNERS is
   un-spoofable against the App and **unsatisfiable by its sole owner**, who is
   also the only bypass actor, so the assembly floor is discharged by bypass and
   widening the route enlarges that surface. Folded into Q6.
9. **AE-C9 VALID/LOW — APPLIED.** G1 requires the named test **green in CI on
   hermes-install main**, not merely present. G2 names the verifier.
10. **AE-C10 VALID/LOW — APPLIED.** Verified and recorded:
    `21538893` sets `strict_required_status_checks_policy: false`, so the
    stale-approval analysis covered head pushes only. The `[OPERATOR]` hardening
    task now also sets `strict`.
