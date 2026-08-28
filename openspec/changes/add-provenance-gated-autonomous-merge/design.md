# Design: add-provenance-gated-autonomous-merge

## Context

Autonomous merge clearance in the xFactory estate is today admitted on ONE axis.
`add-substantive-review-lane` (openxFactory `roles-authority-model`, ratified
2026-08-22) ratified a "Constitutional floor for autonomous clearance" that makes
autonomous clearance "eligible only for candidate classes whose blast radius is
docs- or derived-artifact-shaped." A fully governed CODE pull request is
therefore categorically ineligible.

The convener's target end state is that when the entire build is governed and
watched from the proposal down and the whole pipeline is green, auto-merge is
mechanically safe for code — its safety resting on the COMPLETE TRACEABILITY
CHAIN, not on review quality. The full pipeline is not built. This change is the
neutral DOCTRINE for an interim, provenance-gated eligibility path, plus a
mechanically checkable criterion and a named successor. Realization is a
downstream codexFactory change (see Non-Goals and Migration Plan).

This design was hardened by the `opsx:propose` alignment review (2 agents) and
council debate (product / systems / adversary). The load-bearing corrections are
recorded in `clarifications.md` and reflected below.

## Goals / Non-Goals

**Goals**
- Add an ORTHOGONAL eligibility axis: docs-/derived-shaped blast radius OR fully
  governed provenance. Either qualifies; neither relaxes the floor.
- Specify the interim criterion (1)–(4) and the provenance-tie verifier CONTRACT
  as neutral doctrine, so codexFactory can realize it against a fixed target.
- Keep the never-clearable floor non-negotiable and binding on both axes.
- Name full-pipeline-green as the successor with an explicit interim sunset.

**Non-Goals**
- Implementing the verifier, editing `scripts/merge_master/council_clearance.py`,
  or bumping any tier vocabulary. All realization is a separate codexFactory
  change, archived only on merged + green evidence per `release-realization`.
- Fixing the supersession evidence bar (deferred to the successor change).
- Projecting the doctrine into `docs/roles-and-authority.md` (lands on promotion,
  per the `add-wallet-carried-review-authority` precedent).

## Decisions

### D1 — Provenance is an orthogonal eligibility axis, not a floor exception
The provenance criterion is added as a NEW eligibility axis and the floor
requirement is MODIFIED to make eligibility an either-or judgment on two
independent axes. Alternative considered: encode provenance as an exception
WITHIN the blast-radius clause. Rejected — it would entangle two different safety
arguments and invite reading provenance as a floor override. The chosen shape
keeps the floor a single, axis-independent invariant.

### D2 — Safety basis is provenance-completeness, explicitly NOT review quality
The doctrine's safety rests on a mechanically verifiable, unbroken governed
traceability chain. It deliberately does NOT depend on review quality or council
seat composition, and takes NO position on the parked seat-diversity question
(`seat_diversity_disposed_on_soak_evidence`). The task's "Q3 nil-diversity
benefit finding" framing was found to be a mis-citation (that record is parked
and warns against the "diversity is unnecessary" reading; openxFactory's own
`add-wallet-carried-review-authority` already declined to build on it). We do not
encode a nil-benefit finding; we make the design independent of the question.
See Open Question 1.

### D3 — The provenance-tie verifier is the buildable core, specified as a contract
The one genuinely new mechanism is a verifier that, at clearance time from the
BASE branch, establishes PR head → OpenSpec change → currently-ratified +
signed council record, and proves the diff was authorized. Its contract:
- **Corroborated anchor.** The tie is resolved from an explicit anchor and
  corroborated against a base-branch effort/change record the PR head cannot
  author. An author-controlled string (head branch / PR body) alone never
  establishes the tie. (Adversary Concern 3.)
- **Currency, not history.** Ratification status is re-resolved at evaluation
  time (never cached) and must be CURRENTLY ratified — superseded/retired after
  the PR opened loses eligibility. (Product Concern 2, Adversary Concern 4.)
- **Signed record.** The council ratification record is trusted only as a signed,
  identity-bound artifact, mirroring the verdict check-run — never a plain
  committed file. (Adversary Concern 5.)
- **Machine-readable scope containment.** Changed paths must fall within the tied
  change's glob allowlist. Prose or repository-level scope ⇒ ineligible, never
  "all paths in scope." (Adversary Concern 1, Systems Concern 2.)
- **SHA pinning.** The tie pins to the same head/base pair as the verdict; a base
  advance re-runs it.
- **Fail-closed + legible.** Any broken/ambiguous/out-of-scope/stale/unsigned/
  non-enumerable link parks, and the park record names which condition or
  sub-check failed. (Product Concern 1.)

### D4 — The floor stays PRIMARY; widening never demotes it silently
Today the definition-time predicate (a static, worst-case per-class judgment) is
the primary floor enforcement via one union-judged walk over a class's whole
allowlist; current codexFactory `PROTECTED_CLASS_SURFACES` already covers
`.github/`, `hermes/` (councils and records), `credentials/`, workflow contracts,
`omnigent/`, `openspec/`, `scripts/`, `tests/`. The doctrine requires: (a) any
provenance-eligible class route through that SAME walk; (b) the realization state
explicitly which enforcement is primary for the provenance axis (if the allowlist
is broad, the per-PR verifier is primary and the definition-time floor a
mandatory backstop); (c) each enrolling repo publish its OWN tree-validated floor
before any non-docs class is enabled, because floor semantics are tree-specific
(`scripts/**` = "the decision core" in codexFactory, not necessarily elsewhere;
the pilot is `opensoft/openxFactory`). Alternative considered: rely on the
current floor membership as sufficient. Rejected — the doctrine must be
membership-independent and portable across enrolled repos. (Systems Concerns 1
and 3, Adversary Concerns 2 and 5.) CRITICAL #1 (global-floor parameterization +
mandatory-minimum trust-root floor) was folded into the `roles-authority-model`
spec delta per the 2026-08-28 convener disposition (record: codexFactory
`hermes/domain/review-councils/records/2026-08-28-gate-rules-provenance-gated-autonomous-merge.md`).

### D5 — codexFactory realization is a SEPARATE dependent change
The realization (verifier, `council_clearance.py` guard, the ordered-delta
MODIFIED on `merge-master-approval`'s definition-time predicate, the per-repo
floor, and a `gate_rules_council` record) is its own change: it has its own code
surface, its own reviewing council and record, its own archive-on-green gate, and
depends on a human-gated structured-path-scope precondition (D6). Folding it into
this doctrine change would violate the release-realization archive gate and mix a
doc-only change with a code change. Disposition recorded in `clarifications.md`.

### D6 — A machine-readable path-scope substrate is a hard precondition
The scope-containment check (D3) has no substrate today: `code_surface:` is
repository-granularity prose (`release-realization` `:7-8`). The realization
depends on a structured path-scope declaration on ratified changes — a glob
allowlist — added as a `code_surface` schema amendment or a new sibling field,
itself a human-gated `openspec/`-touching change. Until it lands, no
provenance-eligible code class can be published. Named as its own dependency, not
folded silently into the verifier. See Open Question 2.

## Risks / Trade-offs

- **Prose `code_surface` cannot bound blast radius** → the scope check is
  ineligible-by-default until the D6 substrate lands; prose/repo-level scope is
  explicitly treated as ineligible, never "all in scope."
- **Widening the definition-time predicate could open a gate self-weakening loop**
  → provenance classes route through the shared union-judged floor walk; each
  enrolling repo instantiates its own tree-validated floor; negative fixtures in
  the realization prove a class reaching `scripts/**` or `openspec/changes/**` is
  refused at definition time.
- **Forged/borrowed provenance tie** → base-read corroboration + signed record +
  path-allowlist containment; author-controlled strings alone are insufficient.
- **TOCTOU on ratification currency** → re-resolve at evaluation time, require
  currently-ratified, SHA-pin to the verdict.
- **Interim regime ossifies into a permanent second lane** → explicit sunset;
  retirement by a named full-pipeline-green successor.
- **Nil-near-term value** → doctrine unlocks no merge by itself; it needs
  enrollment's live canary, the predicate widening, the D6 substrate, and the
  verifier. Foregrounded in the proposal's "Why".

## Migration Plan

1. Ratify this openxFactory doctrine change (ordered-delta relative to
   `add-substantive-review-lane`; archive ordering follows that mechanism).
2. Land the D6 structured-path-scope substrate (human-gated `openspec/` change).
3. Author the dependent codexFactory realization change: the provenance-tie
   verifier; the ordered-delta MODIFIED on `merge-master-approval`'s
   definition-time predicate (widen to admit a provenance-eligible non-docs
   `clearable` class without weakening the floor, stating primary enforcement);
   the `council_clearance.py` guard + negative fixtures; per-repo tree-validated
   floor for the pilot; a `gate_rules_council` record declaring the first
   provenance-eligible class. Scope it against codexFactory `origin/main` (the
   local submodule pin was observed stale).
4. Enroll the pilot repository via the `add-repo-enrollment` owner-verified,
   machine-prepared PR route against base-branch
   `.github/merge-approval-envelope.yml` — never bypassed.
5. Run a pilot; raise the named full-pipeline-green successor on that evidence;
   the successor retires this interim criterion.

**Rollback:** the doctrine is additive; reverting the ordered-delta restores the
blast-radius-only eligibility. No provenance-eligible merge can occur before the
realization + substrate land, so ratifying the doctrine alone changes no runtime
behavior.

## Open Questions

1. **The "Q3 nil-diversity-benefit" premise is unsupported by the record.**
   Reframed to provenance-completeness with no position on the parked question.
   Convener to confirm, or supply a ratified nil-benefit record if one exists.
2. **Structured path-scope substrate route** — `code_surface` schema amendment vs
   a new sibling field (D6). Convener to choose or defer to the realization.
3. **Floor primacy for a broad provenance class** — confirm the per-PR verifier
   becomes primary with the definition-time floor as mandatory backstop, or
   require provenance classes to keep narrow allowlists.
4. **Supersession evidence bar** — confirm deferral to the named successor, or set
   the bar now.
