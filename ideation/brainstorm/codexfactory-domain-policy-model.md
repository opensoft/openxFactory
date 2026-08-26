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
Topics: codexfactory-domain, codexfactory, domain-hermes, domain-policy, store-vs-improvise,
determinism, enforceability, domain-memory, best-practices, governance-gates,
layer-content-seeding
Repository context: openxFactory (targets codexFactory hermes/domain/policies/ + memory-boundaries)
Captured: 2026-07-21

Updated: 2026-07-22 (coverage / contested-position / memory-write decisions; kind map; DTN candidate)

## Decided (2026-07-22)

- **Coverage floor: ratchet, no absolute number.** Coverage never decreases,
  and new/changed code meets the new-code threshold — no repo-wide absolute
  floor (they age badly). The threshold value itself is set in the policy file,
  not here.
- **Contested positions carry `rationale` + `review_by`.** Every staked
  position records why, what was rejected, and a review-by date; an overdue
  `review_by` is a doc-health-style finding. Schema below.
- **Domain memory writes: worker proposes, Lead accepts.** Any Plane-2 worker
  or sweep may propose an entry; the owning Lead accepts it into domain memory.
  No full ratification — memory is learning, not policy. (Policy changes keep
  their heavier path.)

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

**How the rows materialize** (record shape decided 2026-07-22 in
`hermes-layer-seeding-mechanism.md`: generic `layer_content` kernel +
specialized views): rows 1–7 seed as `content_kind: policy_position`
(contested ones with the schema below), row 8 as `role_authority` /
`escalation_rule`. The "gate" column names the view/check that reads each —
no longer aspirational.

## Contested-position record shape (draft)

Category 4 made authorable — the fields a staked position carries so staleness
is mechanically visible:

```yaml
kind: policy_position
contested: true
position: "squash-merge into protected branches"
rationale: >-
  Linear history is worth more to us than merge-commit fidelity; bisection
  and revert discipline depend on it.
alternatives_rejected:
  - merge-commit (history fidelity argument — rejected: bisection cost)
  - rebase-ff (rejected: rewrites shared history)
staked_at: 2026-07-22
staked_by: lead-integration        # the owning Lead
review_by: 2027-01-22              # overdue => doc-health-style finding
supersedes: null                   # or the prior position's id
evidence: []                       # optional links to what informed it
```

Uncontested positions omit `contested`/`alternatives_rejected`/`review_by` —
the ceremony is proportional to how debatable the call is.

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

## The test, neutralized (DTN candidate)

The decision test is already domain-free; the neutral wording for openxFactory:

> *A domain SHALL store a policy element only when improvisation fails it:
> when two competent practitioners — or two model runs — could reasonably
> differ AND it matters that they don't (consistency, enforceability, our-way
> choice, staked position, fail-closed boundary, accumulated learning). If any
> reasonable answer is acceptable, the element is left to the model and MUST
> NOT be stored.*

Exit: register as a DTN promotion candidate
(`openxFactory/docs/domain-neutralization-candidate-register.md`) — the
store-vs-improvise test as a neutral authoring contract every domain's
`policies/` is validated against. Medx/Ledgerx/Opsx/Adx get the same filter
codex used, and "policy bloat" becomes a checkable finding rather than taste.

## Store-vs-improvise is the same seam as the runtime hybrid

This maps straight onto the content-seeding decision (`hermes-layer-content-
seeding.md`): the **stored delta is the enforceable slice** materialized into
runtime records so gates can check it; the **improvised remainder is the
reference behavior** the model supplies at job time. Same line, drawn once:
pin what must be enforced/consistent/ours/forbidden/remembered; improvise the
textbook.

## Open questions

- ~~**Coverage floor value**~~ — DECIDED 2026-07-22: ratchet only (§Decided).
- **Domain default vs. project override granularity** — exactly which stack
  standards are domain-locked vs. project-overridable? (`tenant_overrides_allowed`
  already lists `repository_check_commands`, `required_check_extensions`.)
- ~~**Contested positions**~~ — DECIDED 2026-07-22: rationale + `review_by`
  (§Decided; schema in §Contested-position record shape).
- ~~**Memory write authority**~~ — DECIDED 2026-07-22: worker proposes, Lead
  accepts; no ratification for memory entries (§Decided). Sync this into
  `codexfactory-domain-memory-and-practices.md`, which carries the same question.
- ~~**Record shape for the stored delta**~~ — DECIDED 2026-07-22 in
  `hermes-layer-seeding-mechanism.md`: generic `layer_content` kernel +
  specialized views; the categories map per the "How the rows materialize"
  note above.
