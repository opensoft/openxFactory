# Alignment review — stack-architect

Status: draft
Round: alignment, 2026-08-27
Subject: `adopt-council-cleared-merge-gate`, first draft
Verdict: **APPLIED IN FULL** — eleven findings, all accepted; two inverted a
load-bearing argument in the draft.

Retained per the packet convention of `add-wallet-carried-review-authority` and
`split-openxwallet-repo`. Findings are recorded with the disposition applied, so
a later reader can see what the draft got wrong rather than only what it now
says.

## Findings and dispositions

1. **MISMATCH — six spec citations did not resolve.** The draft cited
   `openspec/specs/roles-authority-model/spec.md:284-296`, `:323-344`, `:184-196`
   and four `openspec/specs/review-authority-intake/` lines. The promoted
   `roles-authority-model` spec is 181 lines and contains none of them; there is
   no promoted `review-authority-intake` at all. Both requirements live in
   **ratified-but-unpromoted deltas** under `openspec/changes/`. The quoted text
   was accurate; only the paths were wrong. **The same hazard was already flagged
   in `add-wallet-carried-review-authority/alignment-stack-architect.md:122`** —
   so this packet repeated a known error.
   **APPLIED:** every citation re-pathed to
   `openspec/changes/<change>/specs/<cap>/spec.md:<line>`, with the citation form
   explained in-line at first use and labelled ratified-but-unpromoted.

2. **MISMATCH — the self-reference deadlock argument's premise was false.** The
   draft rejected a required `merge-master-approval` check partly on the ground
   that escaping self-reference would need "an exclude-self-by-name rule that the
   corpus does not have". It has one:
   `xFactory/.github/merge-approval-envelope.yml:85-87` carries
   `check_exclusions: [merge-master-approval]`, and R1's header cites that
   mechanism as the reason its job id must be that literal string.
   **APPLIED:** rejection ground 1 rewritten — the exclusion exists, so the
   hazard is an invariant openxFactory's envelope must carry, not an
   inescapable deadlock. Grounds 2-4 carry the rejection alone.

3. **MISMATCH — G4's floor widening was not expressible in the file it named.**
   `openxfactory-review-authority-floor.yaml` is `kind: repository_gate_floor`;
   `repository_floor.py` refuses wildcards outright and `matching_paths` is exact
   set membership. A directory class cannot be floored there.
   **APPLIED:** G4(c) split into c-i (a glob floor in an
   `openxfactory-*-clearance.yaml`, the carrier
   `codexfactory-routine-code-clearance.yaml` already demonstrates), c-ii (exact
   file entries in the `repository_gate_floor`), and c-iii (nothing — the
   repo-independent class floor already covers the rest).

4. **MISMATCH — `.github/**` is not CODEOWNERS-routed.** Only
   `.github/workflows/` is. `.github/CODEOWNERS` itself, and a new
   `.github/merge-approval-envelope.yml`, are not — so the draft's claim that
   authoring the envelope is "a CODEOWNERS-routed human act" was false, and it
   was load-bearing in G4(a).
   **APPLIED:** corrected in the flagged-questions block, with the note that
   codexFactory floors `.github/**` precisely because CODEOWNERS "can be wrong",
   and a CODEOWNERS-widening realization task now owed.

5. **MISMATCH — Q1 was largely already answered, and framed on a misreading.**
   `require_extra_approval_for_unattributed_changes` keys on the pull request's
   **author** (GitHub documents it for unattributed Copilot-authored pull
   requests, raising the count by one), not on the reviewer. And on
   `opensoft/xFactory` — same ruleset `18962101`, unmodified since 2026-07-14 —
   PRs #85 and #100 each carried one `APPROVED` review from the App
   `codexfactory` and GitHub computed `reviewDecision: APPROVED`.
   **APPLIED:** independently re-verified via `gh pr view`; Q1 narrowed to the
   repository-specific residual (does this installation hold write here), the
   general form recorded as CLOSED with the evidence.

6. **DRIFT — consequence 3's protection is inherited from the ruleset this change
   can least defend.** `dismiss_stale_reviews_on_push: true` comes from
   `18834180` (`~ALL` repos); `18962101` sets it false; both carry
   `require_last_push_approval: false`.
   **APPLIED:** an `[OPERATOR]` hardening task adds
   `dismiss_stale_reviews_on_push: true` and `require_last_push_approval: true`
   to `21538893`, which is openxFactory-scoped — zero blast radius. It is now
   the only ruleset edit the change proposes, and it is a hardening.

7. **DRIFT — `21538893` was one day old and edited the same day.**
   **APPLIED:** the table row is date-stamped and both required contexts'
   producing workflows recorded, so a job rename is detectable.

8. **GAP — no gate landed the thing that would cast the review.** R1 is
   structurally read-only (`pull-requests: read`; "NO APPROVAL … The absence is
   STRUCTURAL"). G3 landed the advisory reader, G4 put the class in codexFactory,
   G5 installed the App — and nothing landed the openxFactory-side workflow that
   reads the envelope, computes the class and submits `APPROVE`. The kill switch
   also attributed minting to R1, which cannot mint.
   **APPLIED:** new gate **G4b** added, and the kill switch rewritten against the
   approval-capable caller's credential. This was the draft's most serious
   defect.

9. **GAP — the App's approval act has no register row.** One row exists,
   `act: review`, held by the council. The review/approval separation requirement
   is therefore satisfied vacuously.
   **APPLIED:** Q4 restated as a missing artifact rather than an interpretive
   question.

10. **GAP — the house precedent was invoked selectively.** The draft cited
    codexFactory's `/scripts/` gating to justify `scripts/**` human-only, while
    placing `openspec/changes/**` — which the same rule floors — in its
    *clearable* list.
    **RESOLVED BEFORE THIS REVIEW LANDED**, by the class-boundary rewrite that
    moved `openspec/**` to human-only on the code's own authority. Recorded
    because the seam it names is real: precedent must be cited whole.

11. **GAP — no owner for the pin advance, and no task ends the bypass.**
    **APPLIED:** G4(d) names `@brettheap` as the accountable advancer via the
    code-owned path and requires the pin's own re-point ceremony, with the
    `DERIVED_ARTIFACT_ROOTS`/xFactory-PR-#153 paired-landing discipline carried
    as precedent. Separately, a new subsection states plainly that all three
    gating rulesets keep `OrganizationAdmin / bypass_mode: always`, that this
    change narrows nothing, and that what ends is the bypass's **routine use** —
    with Q6 raised for whether the actor should be narrowed.

## Verified correct, recorded so it is not re-checked

- `18962101` targets exactly seven repositories: AdxFactory, LedgerxFactory,
  MedxFactory, OpsxFactory, codexFactory, openxFactory, xFactory.
- All three gating rulesets carry exactly one bypass actor,
  `OrganizationAdmin` / `always`.
- Every rule on `main` is `ruleset_source_type: Organization`; openxFactory has
  no repository-level ruleset.
- **The bypass ritual is real and measured:** the last 25 merges to openxFactory
  `main` all show `reviewDecision: REVIEW_REQUIRED` with `mergedBy: brettheap`.
- The floor file at R1's pinned `58bd3cf7` is **byte-identical to codexFactory
  `origin/main`** — the pin is behind main in general but **not stale for this
  file**, and the `governance/review-authority/{grants,wallets,attestations}/`
  gap is recorded verbatim in its header.
- `openspec/specs/roles-authority-model/spec.md:80-84` is genuinely the
  "Low-risk enforcement envelope" requirement — the one citation in the draft
  that resolved.
