# Alignment review — qa-lead

Status: draft
Round: alignment, 2026-08-27
Subject: `adopt-council-cleared-merge-gate`, first draft
Verdict: **APPLIED IN FULL** — fifteen findings. One was stale by hours and one
named a structural defect in how the draft derived its boundary.

## The structural finding, recorded first because it explains the rest

Findings 2-6 and 9 shared one root: **the draft derived its class boundary from
ratified prose in openxFactory and never checked it against implemented
rules-as-code in codexFactory.** The prose reading was defensible; the code is
stricter, more specific, and already answered three of the draft's five open
questions. Reversing the derivation — start from `council_clearance.py`'s
constants and the named-class schema, assert only what the code does not cover —
was applied, and it shortened the class-boundary section, closed three
questions, and shrank G4.

**This is the LS-A3 failure mode caught in its own proposal.** A packet written
to prevent "a described control treated as existing" had itself described a
boundary the enforcer would have refused to implement.

## Findings and dispositions

1. **MISMATCH — G3's core claim was false and stale by hours.** The draft said R1
   was "an unpushed local branch; there is no pull request for it". **PR #439 is
   OPEN**, non-draft, head `f012eb10`, opened 2026-08-27T22:42:40Z,
   `wallet-validation` SUCCESS. The sub-claim survived: `merge-master-approval`
   has never reported, on `main` or on #439.
   **APPLIED:** G3 restated against PR #439; the same correction made in the
   proposal's opening section and in `.openspec.yaml`'s origin `reason`. The
   lesson generalized: every gate now carries a verified-at date, and the packet
   states that gate states must be re-verified at adoption, never inherited.

2. **MISMATCH — the draft's headline clearable entry was floored twice.** It
   listed `openspec/changes/**` and `openspec/specs/**` first among
   autonomously clearable paths. `openspec/` is in `PROTECTED_CLASS_SURFACES`
   (`council_clearance.py:852`) **and** `openspec/changes/**` is in
   `GATE_INTEGRITY_FLOOR` (`:136`, "the change records"). Enrolling it would
   require **narrowing** a floor, which
   `regular-pr-council-clearance/spec.md:55` forbids outright ("may be widened
   and SHALL NOT be narrowed").
   **APPLIED:** `openspec/**` moved to human-only. The consequence is stated
   prominently rather than buried — openxFactory's dominant traffic *is*
   `openspec/changes/**`, so the premise "most openxFactory PRs qualify" is
   false, and this proposal's own diff would not qualify under its own boundary.

3. **MISMATCH — three further clearable entries were refused by shipped code.**
   `CLAUDE.md` and `AGENTS.md` are in `PROTECTED_ROOT_FILES` (`:900`);
   `health/**` was narrowed by R5 on 2026-08-26 from a whole root to eight
   subtrees, of which two are openxFactory's, with `health/dispositions.yaml`
   and `health/envelopes/` refused by name in `CONTRACT_CONSUMED_PATHS`; and
   `governance/` is wholly protected, so the draft's "`governance/**` except
   `governance/review-authority/**`" carve-out was inverted.
   **APPLIED:** all three corrected; the two openxFactory derived roots named
   exactly.

4. **MISMATCH — bare `**` globs fail the floor regardless of subject.**
   `DOCS_FILE_SUFFIXES` is `(".md",)` and the docs branch tests the suffix; a
   directory glob with no suffix pin falls through to deny, and any pattern
   starting with a wildcard is refused ("LOCATION MUST WIN OVER EXTENSION").
   **APPLIED:** every clearable entry respelled suffix-pinned with a non-empty
   literal prefix — `docs/**/*.md`, `ideation/**/*.md`.

5. **GAP — the boundary was drawn in paths; the doctrine is drawn in named
   classes plus declared intent.** The implemented object is a four-layer
   classification: declared class intent → path allowlist → gate-integrity
   denylist → per-condition predicates, with the envelope candidate bound to a
   per-repo gate rule by explicit `applies_to.candidate_id` and
   `classification_intent` as the sole authority for intent. The draft supplied
   only layer two and never named a class.
   **APPLIED:** **two named candidate classes** —
   `openxfactory-governance-prose` and `openxfactory-derived-health-artifact` —
   each declared `advisory` on enrollment (mandatory: `_validate_defined_not_wired`
   refuses `clearable` for an unwired repository), each owing a `risk_tier`, an
   owning seat and a resolvable `intent_reference`. The human-only enumeration
   is now explicitly a reader's aid, not the control, since an allowlist admits
   only what it names.

6. **MISMATCH — the draft's Q5 was already ruled by code, more broadly than it
   asked.** `scripts/` and `tests/` sit in both floors; `contracts/` and
   `schemas/` in the class floor. The draft presented these as its own boundary
   calls owed a CODEOWNERS task.
   **APPLIED:** closed as answered by shipped rules-as-code, with the note that
   presenting a shipped control as an owed one is the same class of error as the
   reverse.

7. **MISMATCH — a miscitation.** The draft attributed the conjunctive envelope to
   `roles-authority-model:80-84`, which is "Reviewer and enforcer identity
   separation from the author". The correct requirement is *Fail-closed
   substantive review envelope* at `:96`, whose first conjunct is "matches a
   `gate_rules_council`-defined candidate class".
   **APPLIED:** corrected, routed through the promoted low-risk envelope for the
   check-pass conjunct.

8. **MISMATCH — the floor's source of truth is a six-member condition list.** The
   draft treated "contract bytes, gate or workflow definitions, credential
   surfaces, or security posture" as the floor's four terms. The requirement
   names its source of truth as codexFactory's 2026-07-23 `gate_rules_council`
   record, whose floor has six members — identity, head ref, failed checks,
   secret findings, security-touching paths, gate-weakening changes — four of
   which are not path-shaped.
   **APPLIED:** a new opening subsection presents the boundary as the
   path-shaped subset of a six-condition floor and raises Q5 for who restates
   the other four.

9. **GAP — G4(b) conflated two floors and over-scoped the widening.** The
   definition-time class floor is repo-independent and already refuses
   `contracts/`, `.github/`, `scripts/`, `tests/`, `governance/`, `openspec/`
   and `schemas/` for every repository, wired or not.
   **APPLIED:** G4(c) split, with c-iii recording explicitly that nothing
   further is owed and citing `class_floor_problem` at `:1065`.

10. **GAP — the packet asserted a `specs/` delta and a `tasks.md` that did not
    exist.** The front matter declared three deltas; `specs/` was empty and
    there was no `tasks.md`.
    **APPLIED:** both authored, with byte-faithful delta text, since
    `promotion_fidelity.py` compares deltas against promoted text at archive
    time.

11. **Verified correct — G1, G2, G4(a).** `6.1 [x]`, `6.2`-`6.8` all `[ ]`;
    hermes-install PR #46 MERGED 2026-08-27, seven files all under `openspec/`,
    its own body "Governance only. This PR changes no runtime code"; no
    wallet/exercise/signature/revocation module under hermes-install `src/`;
    `7.1`-`7.7` all `[ ]`; `add-substantive-review-lane` task 3.2 `[ ]` and
    codexFactory's `gate-rules.yaml` carries no openxFactory entry.

12. **GAP (LS-A3, live) — gate evidence was loose enough to wave through.** G1
    cited checkbox numbers that exist in **two** packets, where ticking one does
    not tick the other; G2's "rehearsed test in 7.7" named a prose `**Gate:**`
    line, not a test; G5 — the gate the whole mechanism turns on — required only
    "one verification", closable by a sentence in a session log.
    **APPLIED:** G1 names both task paths and demands the test file's path and
    name; G2 demands a named test path plus a dated runbook-walk record at a
    stated path; G5 demands a throwaway PR, the App's cast `APPROVE`, and
    captured `gh api` JSON committed at
    `evidence/g5-app-review.md`. G6 was already well-formed.

13. **DRIFT — the packet rests on codexFactory `58bd3cf7`, behind `origin/main`.**
    The `DERIVED_ARTIFACT_ROOTS` narrowing was a **paired landing** with
    `opensoft/xFactory` PR #153, a cross-repo sequencing dependency the draft did
    not mention.
    **APPLIED:** the paired-landing discipline carried into G4(d) as the ordering
    precedent for any pin advance. Note the stack-architect independently
    established that the floor file at `58bd3cf7` is byte-identical to
    `origin/main`, so the pin is not stale for the artifact this packet quotes.

14. **Canary — the pilot reading is correct; the "≥2 classes" half was not
    satisfiable as scoped.** The ≥3-PR/≥2-class bar sits in *Adoption beyond the
    pilot*, whose subject is extension beyond the pilot, and openxFactory is the
    named pilot — so the draft's disclaimer was right. But it then **borrowed
    that requirement's counting rule as permission** while disclaiming its
    applicability; and with one class enrolled, N=5 could not detect a
    class-boundary error, which is the failure mode a canary on a classification
    change exists for.
    **APPLIED:** N raised to **6, split ≥3 per class** across the two now-named
    classes; the counting rule recited as analogous reasoning adopted by choice,
    not as permission; and each canary pair required to land at a named record
    path, since "the council records a verdict" is not an observation without
    one.

15. **GAP — record filenames.** The packet retained none of the five.
    **APPLIED:** the current sibling convention adopted verbatim —
    `alignment-qa-lead.md`, `alignment-stack-architect.md`,
    `council-adversary-engineer.md`, `council-product-advocate.md`,
    `council-systems-architect.md`, plus `clarifications.md`, `design.md`,
    `tasks.md`, `specs/`. `add-substantive-review-lane`'s older `review/`
    subdirectory form was **not** followed. `Status: draft` carried on every new
    document. Doc-health: `proposal-origin` is satisfied by the complete
    `ad_hoc` origin block; `ratified-provenance` and `promotion-fidelity` stay
    quiet while unratified; `staged-candidate-aging` does not apply.
