# codexFactory Domain Policy: store the delta, not the textbook — Brainstorm

Status: brainstorm
Kind: process
Summary: Answers the load-bearing question for filling the domain layer — since
every capable model already knows software-engineering best practice on the fly,
what actually belongs in *stored* domain policy/memory, and why. The principle:
store only the **delta from generic competence** — the choices that must be
consistent, the rules a gate must enforce, the boundaries that must fail closed,
the positions the domain stakes on contested calls, and the learning it has
accumulated — and let the model improvise everything a competent generalist
gets right anyway. This doc gives the store-vs-improvise decision test, the
domain policy categories that pass it (filled with concrete codex positions),
and the anti-list of what we deliberately do NOT store. Parent:
`codexfactory-domain-hermes-content.md`.
Topics: codexfactory, domain-hermes, domain-policy, store-vs-improvise,
determinism, enforceability, domain-memory, best-practices, governance-gates,
layer-content-seeding
Repository context: openxFactory (targets codexFactory hermes/domain/policies/ + memory-boundaries)
Captured: 2026-07-21

## Possible feats

- **Author `hermes/domain/policies/`** with the stored-delta categories below.
- **A neutral "store-vs-improvise" authoring test** so every domain (not just
  codex) decides consistently what to pin.
- **Domain memory seed** — recurring findings / known-bad patterns / practice
  effectiveness, feeding the ratified memory gateway.
- **Project-override contract** — which domain defaults a project may override
  and which are locked.

## The principle: store the delta, not the textbook

A capable model, on the fly, already writes clear code, knows OWASP-level
security, structures tests sensibly, and gives a reasonable answer to almost any
"what's best practice here?" question. Re-stating that in stored policy is worse
than useless — it bloats the content, rots as practice evolves, and creates a
false sense of governance (a paragraph of advice a gate cannot enforce governs
nothing).

Stored domain content earns its place only when improvisation *fails us*. It
fails in six specific ways, and each is a reason to pin:

1. **Consistency / determinism.** On-the-fly reasoning varies run to run and
   model to model. Governance needs the *same* answer to the same input every
   time — a gate that gives different verdicts on identical facts is not a gate.
2. **Enforceability.** A stored rule can be checked by a gate at write time (the
   hybrid seam). An improvised judgment *is* the thing being governed; you
   cannot gate on a vibe.
3. **Our-way choices.** Among several equally valid options (branching model,
   merge style, coverage floor, language-version floor) the model picks *a* good
   one — not *our* one, and not the same one twice. These are arbitrary-but-must-
   be-consistent.
4. **Contested positions + rationale.** Where best practice is genuinely debated,
   the domain *stakes a position* and records *why* — the domain staking its
   reputation. A model hedges or varies.
5. **Fail-closed boundaries.** Safety prohibitions must be fixed and fail closed;
   you never want "never commit secrets" or "deploy is not a standing capability"
   to be improvised or reasoned around.
6. **Accumulated learning.** What *this* domain has seen across projects —
   recurring findings, known-bad patterns, what worked — is history the model
   does not have. This is memory, and it is the whole point of a *learning*
   domain.

**The decision test (one line):** *if two competent engineers — or two model
runs — could reasonably differ, and it matters that they don't, pin it; if any
reasonable answer is fine, leave it to the model.* Equivalently: store the
choices, the bindings, the boundaries, and the memory; improvise the rest.

## What we store (domain policy, filled with codex positions)

Each row passes the test above; "why" names the failure mode it guards, and
"gate" names the enforcement point where one exists.

| Category | Our stored position (concrete) | Why (test) | Gate |
| --- | --- | --- | --- |
| **Branching & change model** | trunk-based; short-lived branches; PR-only into protected branches (no direct push); squash-merge; Conventional Commits | our-way choice | branch protection (repo-owned) |
| **Review requirement** | a change is admitted only when the governed-review verdict is ADMIT with **no undispositioned conditions**; security-sensitive paths (auth, crypto, secrets, CI config, dependency manifests) require a Lead Security verdict | enforceability + boundary | `governed_review_evaluated` |
| **Required checks** | `secret_scan`, `branch_review`, `traceability_validation` all pass; `allow_pending_required_checks: false`; coverage must not decrease and new code meets the domain floor | our-way + enforceability | `admission_evaluated` |
| **Change size & reversibility** | bounded to approved scope; small and reversible; *ordinary revert must suffice as rollback* — anything that doesn't needs elevated handling | binding discipline | merge envelope |
| **Security must-nots (fail-closed)** | never commit secrets; `production`/`deploy`/`package_publish` are never standing worker capabilities; no new external network call or foreign-input trigger without Lead Security clearance; **on security ambiguity, park — never proceed** | boundary / fail-closed | envelope + Lead Security |
| **Traceability** | every change maps feature → spec → task → test | our-way + enforceability | `traceability_validation` |
| **Stack standards** | domain sets defaults (formatter/linter, minimum language version, dependency-pinning policy); projects may override only the allowed set, never the security must-nots | our-way + boundary | check matrix |
| **Authority & escalation** | the roster's owns/decides/escalates (see roster draft) | consistency / governance | routing rules |

These consolidate what today is scattered across `profiles/software-team.yaml`
(checks, admission/merge policy), the merge envelope (`revert suffices`), the
Omnigent constitution (prohibited actions), `credentials/requirements.yaml`
(capability families), `roles-and-authority.md` (review verdict), and the
traceability docs — into `hermes/domain/policies/` as enforceable content.

## Domain memory (stored because it is learned, not because it is a rule)

Distinct from policy: this is evidence/history the domain accumulates and the
model cannot know. Seed and grow it, feeding the ratified memory gateway's
`domain_learning_candidates`:

- **Recurring review findings** — the "we keep seeing X" register.
- **Known-bad patterns** — anti-patterns this domain has been burned by.
- **Flaky-test / regression history.**
- **Practice-effectiveness signal** — which adopted practices actually paid off
  (feeds the practice catalog).

Memory boundary: this is *cross-client* domain learning (what the domain knows
in general), promoted only through the gateway's gate — never reaching into any
client's private memory.

## What we deliberately do NOT store (leave to the model)

Storing these would be bloat that drifts and governs nothing:

- Clean-code, naming, readability idioms; good PR-description writing.
- Algorithm/data-structure choices; language-specific idioms.
- Generic security awareness the model already has (the *specific* must-nots
  above are stored; the general knowledge is not).
- How to write a good test *in general* (the coverage *floor* is stored; the
  craft is not).

Rule of thumb: the domain policy is the **diff** against "a competent engineer
doing the obvious right thing," not a re-derivation of it.

## Store-vs-improvise is the same seam as the runtime hybrid

This maps straight onto the content-seeding decision (`hermes-layer-content-
seeding.md`): the **stored delta is the enforceable slice** materialized into
runtime records so gates can check it; the **improvised remainder is the
reference behavior** the model supplies at job time. Same line, drawn once:
pin what must be enforced/consistent/ours/forbidden/remembered; improvise the
textbook.

## Open questions

- **Coverage floor value** — pick a concrete number, or express as "no decrease
  + new-code threshold" only? (Leaning the latter — absolute floors age badly.)
- **Domain default vs. project override granularity** — exactly which stack
  standards are domain-locked vs. project-overridable? (`tenant_overrides_allowed`
  already lists `repository_check_commands`, `required_check_extensions`.)
- **Contested positions** — do domain positions on debated practices carry an
  explicit rationale field + a review cadence, so a stale position is visible?
- **Memory write authority** — who/what may add to domain memory (a worker
  proposes, a Lead accepts?), and does it need ratification like policy does?
