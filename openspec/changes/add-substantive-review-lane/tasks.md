# Tasks: add-substantive-review-lane

## 1. Ratification gate (BRETT)

- [x] 1.1 `OPENSPEC_TELEMETRY=0 openspec validate add-substantive-review-lane
      --strict` and `--all --strict` green; change listed in the README
      OpenSpec Records block. Both verified 2026-08-22 on the PR #178 branch:
      the single-change validate reports valid, `--all --strict` reports
      `Totals: 67 passed, 0 failed (67 items)` (18 changes, 49 specs), and
      the README row is in the "Active changes:" block.
- [x] 1.2 The five questions this proposal declared open on 2026-08-15 were
      RULED by Brett Heap in-session 2026-08-22 and are encoded — see
      `proposal.md` "Decided questions" and the four new requirements plus
      the rewritten pilot requirement in
      `specs/roles-authority-model/spec.md`. Two rulings departed from the
      written recommendation: Q2 (Brett overrode the two-axis split —
      codexFactory reviews every governed repo) and Q3 (Brett chose a
      bounded conditional pull-in over flat rules-only). Two residues are
      deliberately deferred to a named follow-up change raised on pilot
      evidence: the adoption ORDER beyond the pilot (Q1) and the enumerated
      risk-tier VOCABULARY (Q5).
- [x] 1.3 **RATIFIED 2026-08-22 by Brett Heap** — in-session via question
      prompts at the ratification read. Record:
      `review/ratification-2026-08-22.md`; `proposal.md` `Status:` is
      `ratified` with a `Ratified:` line naming the same record. Four
      read-items were ruled in that round: form elevation of the Q1 bar and
      Q5 floor into promoted requirements ACCEPTED; the Q1 bar counts ANY
      council-cleared verdict, App-approved or human-approved (this overrode
      the encoder's autonomous-only reading — see §5.2); the ordering
      principle stays ABSOLUTE with no waiver clause and no activity scoping,
      escalation to Brett inside a future adoption change being the escape
      path; and ratify. The earlier same-day clarify round (the five Q1–Q5
      rulings, §1.2) is a distinct act and is cross-referenced from the
      ratification record. Sections 3–5 below are now authorized realization
      work rather than parked work.

## 2. Neutral contract delta (this change's own surface)

- [ ] 2.1 Ten ADDED requirements on `roles-authority-model`
      (`specs/roles-authority-model/spec.md`). Six from the authored
      principles: substantive review authority generalization;
      gate-rules-council-defined candidate classes; substantive review
      accountability; reviewer/enforcer identity separation from the author;
      fail-closed substantive review envelope; pilot repository and
      reviewing domain (whose persona-home clause the Q2 ruling rewrote).
      Four from Brett's 2026-08-22 rulings: adoption beyond the pilot
      qualifies on recorded evidence (Q1); company-policy seat participation
      in per-PR councils (Q3); ruleset interaction shape for the substantive
      review lane (Q4); constitutional floor for autonomous clearance (Q5).
- [ ] 2.2 `docs/roles-and-authority.md` (or wherever the neutral roles doc
      lives per the "Neutral authority model ownership" requirement) gains a
      cross-reference to the new requirements, so the human-readable doc and
      the machine-checked spec do not diverge — text-only, no new authority
      concepts beyond what §2.1 already declares.

## 3. codexFactory instantiation (downstream; executed in codexFactory repo)

- [ ] 3.1 `hermes/domain/review-councils/gate-rules.yaml` gains a
      `risk_tier` and `clearance_rule` field per candidate class (schema
      addition to the codexFactory-owned `merge-approval-envelope` mechanics
      contract referenced from `.github/merge-approval-envelope.yml`'s
      header comment), plus the Q5 constitutional floor as enforced data
      rather than prose: a class whose matched PRs can touch contract bytes,
      gate/workflow definitions, credential surfaces, or security posture
      MUST be human-only, and autonomous clearance MUST be refusable for any
      class whose blast radius is not docs-/derived-artifact-shaped.
- [ ] 3.2 `gate_rules_council` produces a record defining
      `opensoft/openxFactory`'s substantive candidate classes (at minimum
      one to prove the generalization; risk tier and clearance rule
      declared per Decision B), with the company-policy-lead seat's
      compliance rationale and a domain seat's best-practice rationale on
      record per the "Substantive candidate classes" requirement.
- [ ] 3.3 Realize the Q3 conditional pull-in (Decision D's superseding
      ruling, no longer an open question). ONE granularity throughout — the
      seat is pulled in when a class's declared CONDITION HOLDS for the pull
      request in front of it, never merely because the pull request matched a
      declaring class (Decision D's GRANULARITY note; Brett's option text
      says a per-PR pull-in condition):
      - `hermes/domain/review-councils/merge-readiness.yaml` gains an
        OPTIONAL `company-policy-lead` seat carrying a `when:` condition,
        mirroring `gate-rules.yaml`'s existing
        `client-security-compliance-officer` / `rule_touches_security_posture`
        conjunction — a conditional seat evaluated per convening.
      - `gate-rules.yaml` gains the per-candidate-class field naming WHICH
        condition that class declares (not a boolean "this class always seats
        the CPL"), settable only by the `gate_rules_council` at
        class-definition time.
      - Both files' existing `missing_required_seat: refused` gives the
        fail-closed behaviour with no new mechanism. Verify all three cases:
        (a) class declares a condition and it HOLDS, seat unavailable → parks;
        (b) class declares a condition and it does NOT hold → convenes
        domain-seats-only, and seat unavailability does NOT park;
        (c) class declares no condition → convenes domain-seats-only.
      - AMEND THE CONFLICTING HEADER WORDING IN THE SAME CHANGE. Both council
        files today mark the rule-setting/rule-applying separation
        "PERMANENTLY DISTINCT... a body that sets the rules must not also
        apply them" (decided 2026-07-22). Adding the conditional seat without
        touching that wording leaves `merge-readiness.yaml` contradicting
        itself on its own face. This task owns the amendment: restate the
        header as the ruled shape — permanent separation as the DEFAULT,
        with a bounded per-class, per-PR exception the rule-setting body
        itself declares — citing Brett's 2026-08-22 ruling as the amending
        authority, and leaving the 2026-07-22 decision legible rather than
        erased. This is the codexFactory-side discharge of the conflict this
        change's own record names as unresolved.

## 4. Aggregation / workflow realization (downstream; executed in xFactory aggregation repo)

- [ ] 4.1 Generalize `.github/merge-approval-envelope.yml`'s `candidates: []`
      matching from the single `doc-health-nightly` entry to a list keyed by
      `(repo, author-shape, path/diff-shape, risk_tier)`, adding
      `opensoft/openxFactory` to `target_repos` for its own new candidate
      class(es) without touching the existing `doc-health-nightly` entry.
- [ ] 4.2 Generalize `.github/workflows/merge-master-approval.yml`'s
      candidate resolution and author/identity checks to iterate the
      candidate list rather than assume the single hard-coded class,
      preserving: base-branch-only rule reads, the anti-spoofing
      `COUNCIL_LANE_APP_ID` binding on the `council-verdict/merge-readiness`
      check-run, the dedicated merge-master token mint, and fail-closed
      parking on any unevaluable condition.
- [ ] 4.3 Verify author/enforcer identity separation holds for
      agent-authored candidates: the enforcer MUST refuse clearance when a
      candidate's author identity matches a participating council seat's
      identity or the merge-master approving identity itself (the
      "Reviewer and enforcer identity separation" requirement's scenario).
- [ ] 4.4 REALIZATION FACT, recorded here so the generalization does not
      discover it late (verified by reading the code 2026-08-22, NOT a
      blocker for ratification): the envelope matcher compares head refs by
      EXACT STRING EQUALITY — codexFactory
      `scripts/merge_master/envelope.py`'s `_find_surface` does
      `head_ref == cand.get("expected_head_ref")`, with no glob, prefix, or
      regex path, and the schema makes `expected_head_ref` a required,
      non-empty field. Every candidate class expressible today is therefore
      pinned to ONE literal branch name. A substantive class covering
      human-authored PRs on arbitrary branches cannot be written against the
      current matcher: §4.1 must add a pattern-capable head-ref predicate
      (and a schema change to accept it) or the pilot's first substantive
      class must itself be fixed-branch. Whichever is chosen, it is a
      matcher change, not a config change.
      **CORRECTED 2026-08-25 — THE FACT ABOVE IS FALSE, AND ITS CONCLUSION IS
      VOID.** Left standing rather than deleted, because this task exists to stop
      the realization discovering the matcher late, and a reader who acts on the
      original text will build something that already ships. The truth:
      - `head_ref_pattern` is part of schema **v1 itself** — `schema_version` is
        `{"const": 1}` and the member is a `oneOf` alternative to
        `expected_head_ref` in codexFactory's
        `schemas/merge-approval-envelope.schema.json`. Glob matching is
        implemented in `scripts/merge_master/envelope.py`
        (`_glob_to_regex`, `_head_ref_matches`).
      - It shipped in codexFactory `9ebe805` on **2026-08-21 — ONE DAY BEFORE
        THIS CHANGE WAS RATIFIED**, and the aggregation's pinned merge-master
        core (`3c35ca8b`) contains it. The capability is live in production now.
      - codexFactory already runs the exact class the original text calls
        impossible: `head_ref_pattern: change/**` on `codexfactory-routine-code`,
        covering human-authored PRs on arbitrary `change/**` branches.
      - So "a substantive class covering human-authored PRs on arbitrary branches
        cannot be written against the current matcher" is false, and "it is a
        matcher change, not a config change" is exactly inverted: for §4.1 it is
        now a CONFIG change and no schema work is owed.
      HOW THE ERROR HAPPENED, recorded so it is not repeated: the original was
      verified 2026-08-22 by reading the aggregation repo's `xFactories/`
      codexFactory SUBMODULE CHECKOUT, whose pin was then `e61f24da` — a commit
      predating `9ebe805`. The reading was accurate about the bytes in front of
      it and wrong about codexFactory. This is the submodule-pin-drift trap:
      verify realization facts against the submodule's own `origin/main`, never
      against the pin the aggregation happens to carry.
      WHAT §4.1 MAY ACTUALLY DO. Pattern classes are available at zero schema
      cost, but availability is not permission. **Brett ruled 2026-08-25** that
      intake-per-effort stands for first-tranche classes — one reviewed exact-ref
      entry per effort — on the anti-spoofing ground alone (Principle VII), the
      schema-cost ground having evaporated with the fact above. First-tranche
      classes are therefore fixed-branch BY RULING, not by mechanism, and any
      future move to patterns is a request to revisit that security judgment on
      recorded pilot evidence rather than a schema proposal.
- [ ] 4.5 REALIZATION FACT, and a thing the realization MUST pin (verified by
      reading the code 2026-08-22, NOT a blocker for ratification). A NAMING
      hazard — stated precisely, because the loose version of it ("one key
      read two ways") is false and would send the realization looking for a
      bug that does not exist. The facts:
      - There are TWO different keys, in two different files, carrying two
        different values. codexFactory's
        `scripts/merge_master/nightly-sweep-council-clearance.yaml` declares
        `rule.repository: opensoft/codexFactory`; the aggregation repo's
        `.github/merge-approval-envelope.yml` declares
        `target_repos: [opensoft/xFactory]` on the candidate whose PRs that
        rule governs.
      - `target_repos` is the ENFORCED scope: `envelope.py`'s `_find_surface`
        and `candidate_head_refs` both filter on it.
      - `rule.repository` is DESCRIPTIVE ONLY and is never read in the
        decision path: `council_clearance.py`'s `validate_rule` neither
        requires nor reads it, and no module under `scripts/merge_master/`
        reads it at all. The 2026-08-05 activation record calls it "the
        rule's descriptive `repository:` field" in as many words.
      - So there is no live dual-read today. The hazard is that a
        repo-shaped, unenforced key sits beside the enforced one holding a
        DIFFERENT value, reading naturally as "which repo's PRs" while
        meaning "whose rules these are". At one rule file it is harmless
        documentation; at per-repo classes across several repos it is an
        invitation for a future reader — or a future code path that starts
        honouring it — to scope rules by the wrong repository.
      The realization MUST pin one meaning explicitly: either rename or
      document `rule.repository` as rules-ownership and keep it unread, or
      make it the enforced PR scope and reconcile the existing file's value.
      What it must not do is leave an unenforced repo-shaped key disagreeing
      with the enforced one.
      **CORRECTED 2026-08-25 — DISCHARGED UPSTREAM; THIS TASK IS RE-RECORDED,
      NOT RE-DONE.** The facts above were true when written and are now stale in
      both directions. What changed, all in codexFactory `9ebe805`
      (**2026-08-21**, the same commit as §4.4's matcher work, and likewise
      missed at ratification because the aggregation's submodule pin was the
      older `e61f24da`):
      - `rule.repository` is NO LONGER descriptive-only. `council_clearance.py`'s
        `select_rule` cross-checks it against the resolved surface's
        `target_repos` and REFUSES the rule when they contradict — fail-closed,
        not advisory. `validate_rule` additionally type-checks the field.
      - Its VALUE was reconciled: `scripts/merge_master/`
        `nightly-sweep-council-clearance.yaml` now declares
        `rule.repository: opensoft/xFactory`, agreeing with the `target_repos`
        of the candidate whose PRs it governs. The disagreement this task was
        written to prevent no longer exists.
      - So the mandate was met, by the SECOND of the two options this task
        offered: the key became enforced and the existing file's value was
        reconciled. Nothing here is owed.
      PRECISION, so the discharge is not over-read: the cross-check is a
      CONSISTENCY GUARD, not the selector. Rule selection still binds on
      `applies_to.candidate_id`; `rule.repository` can only refuse a rule, never
      choose one. A realization that starts scoping rules BY that field would be
      making a new decision, not continuing this one.
      RESIDUE, recorded small and deliberately not fixed here: the hazard class
      migrated rather than closed. `rule.tier_1`, in the same file, is read by no
      code — an unenforced key sitting beside enforced ones, which is the shape
      §4.5 was written about. codexFactory already knows: the ONLY occurrence of
      the name anywhere in `scripts/merge_master/*.py` is a comment in
      `council_clearance.py` that calls the key "a comment with a colon in it",
      attributing the phrase to its own review finding LA-F12. So this is a
      known, named, accepted item rather than a discovery. It is harmless at one
      rule file and worth pinning before per-repo rules multiply, but it belongs
      to whoever owns that file next, not to this change.

## 5. Pilot-repo wiring + records (downstream; executed in openxFactory repo)

- [ ] 5.1 `opensoft/openxFactory` gets its own workflow instance (or a
      cross-repo-capable instance of §4's generalized workflow) and its own
      ruleset wiring, since `pull_request_target` fires in the repo the PR
      targets. The ruleset interaction shape is no longer a per-repo blank
      to fill: wire the Q4-decided standing default — the merge-master App's
      real `APPROVE` review satisfies the required-review rule, the
      `council-verdict/merge-readiness` check-run is NOT configured as a
      ruleset satisfier, and human review stays an always-available
      alternate satisfying path (never App-path-only). Any divergence needs
      its own recorded decision in this repo's own adoption record.
- [ ] 5.2 First live substantive candidate on `opensoft/openxFactory`:
      `gate_rules_council` record exists (§3.2), `merge_readiness_council`
      produces a per-PR verdict record, the signed check-run and audit
      artifact are produced, and a real `APPROVE` review lands from the
      dedicated identity — mirroring the 2026-08-14 xFactory PR #85/#100
      precedent, this time on openxFactory.
      EXPECT A NARROW FIRST CLASS, and do not read that as the lane
      underdelivering (design.md Decision G): Q5 (ii) makes contract bytes,
      gate/workflow definitions, credential surfaces, and security posture
      permanently human-only — most of what an openxFactory PR touches;
      Q5 (iii) confines autonomous eligibility to docs-/derived-artifact-
      shaped blast radii; and §4.4's exact-string head-ref matcher pins any
      class to one literal branch until that work lands. The intersection is
      docs-shaped AND fixed-branch. So the pilot's AUTONOMOUS evidence
      accumulates slowly, and the substantive-PR ambition is exercised
      meanwhile through the council-reviewed-but-human-approved path (real
      deliberation, rationales, audit artifact, `needs_human_review`
      disposition, human casting the approving review). Record BOTH kinds of
      run under §5.3.
      COUNTING RULE — **RULED BY BRETT HEAP 2026-08-22** at the ratification
      read, OVERRIDING this task's earlier draft, which said "only the
      autonomous ones count toward the Q1 evidence bar": ANY COUNCIL-CLEARED
      VERDICT COUNTS. A unanimous `merge_readiness_council` verdict counts
      toward the ≥3 bar whether the approving review was cast by the
      merge-master App or by a human. The bar measures COUNCIL QUALITY, not
      enforcer autonomy — a council that deliberated well and whose verdict a
      human then executed is exactly the evidence the bar exists to collect.
      So the narrow autonomous surface described above slows AUTONOMY, not
      the bar: council-reviewed-but-human-approved runs are countable
      evidence and MUST be recorded under §5.3 as such.
- [ ] 5.3 Record the pilot run's evidence (council records, check-run,
      audit artifact, approval) under this change's own evidence trail for
      the eventual archive.

## 6. Validation and exit

- [ ] 6.1 `openspec validate --all --strict` green; the ten ADDED
      requirements' scenarios reviewed against the six decided principles
      AND the five 2026-08-22 rulings for coverage (no principle and no
      ruling without a requirement; no requirement deciding more than its
      ruling decided — specifically, nothing here enumerates a risk-tier
      vocabulary or names a next adoption repo).
- [ ] 6.2 `scripts/doc-health.py --single-repo .` shows no NEW findings
      beyond a freshly measured, same-clock baseline. Baseline re-measured
      2026-08-22 against `origin/main` at `ca0b9057` in a separate
      openxFactory-basenamed checkout, `--as-of 2026-08-22`:
      **4 critical, 6 error, 78 warning, 3 info**. (This supersedes the
      2026-08-15 authoring-time figure of 3 critical / 6 error / 39 warning
      / 3 info, which had gone stale — the warning count moved with staged
      topics aging, not with anything this change did. Compare only against
      a baseline measured on the same clock; `staged-candidate-aging`
      findings are date-driven and a stale baseline manufactures phantom
      regressions.)
- [ ] 6.3 Archive on realization evidence per `release-realization`: the
      ten requirements alone do not gate archiving (they are the proposal's
      own surface, §2), but downstream sections 3–5 are named follow-ups
      whose own realization changes (or a tracked completion of this one)
      carry their own archive evidence — this proposal itself may archive
      once §2 lands and validates, per the same "spec delta lands, domain
      follow-ups are named not performed" pattern `add-client-identity-roster`
      used for its own domain-fragment tasks.
