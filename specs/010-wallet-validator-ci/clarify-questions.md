# Clarification Record — 010-wallet-validator-ci

Session parameters (owner-approved overrides of the global protocol):

- Respondent: `architect` persona via `opencode run --agent architect` (model
  `opencode/x-preview-f-free`, read-only tools). Orchestrator poses; architect disposes.
- Question cap: raised from 25 to an effective 1000 by owner instruction (2026-08-23),
  on the standing rule that questioning stops when material ambiguities are resolved.
- Escalation: any answer that would alter doctrine or governance scope is parked for the
  convener (Brett Heap) rather than encoded.
- Answers are encoded inline in `spec.md` under `## Clarifications` and mirrored here.

## Session 2026-08-23

### Q1 — Scan scope and negative-specimen handling

**Asked**: What tree scope must every PR's wallet-validation check evaluate, and how are
intentionally-invalid example specimens treated so main stays green while malformed grants
are still caught? Options: A whole-tree/no-exemptions · B whole-tree/named exclusion ·
C wallet-paths-only · D changed-paths-only.

**Architect's answer** (verbatim final line):

> ANSWER: B | SCOPE: whole | EXEMPTIONS: named-allowlist | SPECIMENS-ALL-VALID: no |
> RATIONALE: FR-002 mandates evaluating the tree and the S1 doctrine requires an
> un-bypassable gate, ruling out path-narrowed (C) and changed-only (D) scans, while 18
> files under examples/negative/ are unmistakably intentional violations by name so a
> no-exemption scan (A) would redden main against FR-005/SC-003. A single named exclusion
> of examples/negative/** in the check's scoping layer (validator untouched per FR-002)
> keeps main green while FR-004's same-run self-test proves the check still catches
> malformed grants.

**Key finding**: the corpus already contains 18 intentional negative specimens under
`contracts/openxwallet/examples/negative/` — they become FR-004's self-test corpus.

**Disposition**: encoded into spec.md (Clarifications section; FR-004 rewritten;
FR-009 added; Assumptions item resolved). Doctrine check: CI-scoping mechanics only,
validator untouched — no convener escalation required.

### Q2 — Canonical check name and operator-instruction home

**Asked**: (1) Which stable name string should branch protection reference forever?
A validate-openxwallet · B wallet-validation · C openxwallet-intake-gate · D own.
(2) Where must the FR-007 operator instruction live? a README section · b docs/+pointer ·
c workflow comments · d specs dir only.

**Architect's answer** (verbatim final line):

> ANSWER: B:wallet-validation ; a | RATIONALE: Branch protection pins the literal check
> string forever, and a mismatch silently de-advises the gate with no failing signal
> anywhere, so use the exact term the spec itself canonizes (SC-001's "wallet-validation")
> rather than the validator-tool name it must remain distinct from. A top-level README
> section is the only placement reachable in under a minute post-merge without knowing
> which workflow file exists, while specs dirs get archived and workflow comments are
> invisible from the Settings UI.

**Disposition**: encoded into spec.md (Clarifications bullet Q2; FR-007 rewritten with the
literal name). Doctrine check: operational naming/docs only — no escalation required.

### Q3 — Warning semantics and timeout budget

**Asked**: (1) Validator exits zero with non-fatal warnings: A pass/log-only ·
B pass+PR-annotation · C warning=failure. (2) Wall-clock budget before fail-closed:
A 2 min · B 5 min · C 10 min · D runner default.

**Architect's answer** (verbatim final line):

> ANSWER: A ; C | RATIONALE: Exit-zero is the validator's own verdict under FR-002's
> unmodified-semantics lock, and US2/SC-003 require exactly that manual-invocation verdict
> with zero false positives, so warnings may only be logged. FR-006's fail-closed-on-timeout
> needs an explicit cap to be timely (runner defaults are ~hours), and a generous 10-minute
> bound over this small tree eliminates timeout false-reds on a required gate — the
> bypass-training noise US2 explicitly guards against.

**Disposition**: encoded into spec.md (FR-006 amended with 10-min budget; FR-010 added).
Doctrine check: failure-semantics engineering only — no escalation required.

### Q4 — Trigger matrix confirmation

**Asked**: Confirm or correct: every PR targeting main incl. drafts; no push-to-main runs;
no scheduled runs; nothing else. Add belt-and-braces now or keep S1 wiring-only?

**Architect's answer** (verbatim final line):

> ANSWER: confirmed | CHANGES: none | RATIONALE: The ratified S1 gate is defined solely at
> the PR plane ("malformed grant fails the PR"), and FR-001 plus mandatory draft coverage
> satisfies both clauses while push-plane gaps are correctly dispositioned as operator
> settings acts per the spec's existing PART III pattern. Adding push/cron triggers now
> would exceed the verbatim-adopted successor text and constitute scope creep into
> later-stage enforcement territory.

**Disposition**: no spec change required; matrix stands as specced.

## Session totals

4 consults · 6 sub-questions asked and answered · 0 escalations to convener ·
cap 1000, stopped under the resolution rule (remaining taxonomy categories Clear).

### Q5 — Validator-native semantics true-up (plan phase)

**Asked**: Discovery showed layer 1 already asserts the whole negative corpus fails for
declared reasons every invocation, and layer 2's sweep already excludes packaged
examples. Does the check still need its own scoping/self-test code?

**Architect's answer** (R5 consult, verbatim final line):

> ANSWER: blessed | CHANGES: none | HOLE: none | RATIONALE: Discovered validator
> semantics natively satisfy FR-004 (whole negative corpus asserts failure every run)
> and FR-009 (packaged-example exclusion in the layer-2 sweep), so the zero-scoping-code
> wiring plus NO --strict exactly matches FR-002/FR-006/FR-007/FR-010 and the Q3 ruling.
> The only bypass vectors (direct push, admin merge, non-family-kind encodings) are
> explicitly out-of-scope operator/validator boundaries the spec already rules on, not
> gaps this gate leaves open.

**Disposition**: spec Clarifications Q5 added; FR-004/FR-009 mapping trued-up; negative
corpus count corrected 18 → 29. Execution notes adopted: unnamed job (check displays as
`wallet-validation`), job-level `timeout-minutes: 10`, least-privilege permissions
(later corrected from `{}` to `contents: read` — see implementation-notes Round 5).

### Q6 — Convener authorization: invalid-YAML hardening + enforcement-plane routing

**Ruling source**: Brett Heap, 2026-08-23, on QA round-3 escalations (recorded in
implementation-notes.md Round 3).

**Rulings**: (1) fail-open on syntactically-invalid YAML — "authorized hardening":
check-layer kind-aware syntax gate as committed helper `scripts/wallet-yaml-syntax-gate.py`
(architect option C), vocabulary imported from the validator module; FR-011 added;
Q5's zero-code ruling amended for this hole only. (2) enforcement-plane — "fix this
vulnerability": `.github/CODEOWNERS` routing the three gate surfaces to @brettheap,
routing-only.

**Disposition**: Phase 7 tasks T008–T010 landed; verification in implementation-notes
Round 6; QA round 7 PASS-WITH-NOTES (residual: lexically-encoded kind spellings such as
`gr\u0061nt` remain outside raw-text containment by design wording — documented
residual risk for a future upstream fix).
