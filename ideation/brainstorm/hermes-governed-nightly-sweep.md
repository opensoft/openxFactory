# Hermes-Governed Nightly Sweep: who sets up the trigger, who reviews the output — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The nightly doc-health sweep is triggered by a GitHub Actions
cron a human wired by hand, and its rolling PR is reviewed by a
rules-as-code envelope plus Brett. Both facts should become OUTPUTS of
the three-layer Hermes flow: the Domain Hermes autonomously generates
"this repo should run this sweep" as a best-practice suggestion, the
Client (Company Policy) Hermes clears it, and the Project (Customer)
Hermes implements the GitHub Action on the repo. Companions:
`domain-practice-suggestion-generation.md` (how the domain generates)
and `practice-clearance-and-project-realization.md` (how policy clears
and the project realizes). Substrate: `hermes-layer-content-seeding.md`
(how the three layers get the content this pipeline assumes they have).

## The inversion

Today's chain, bottom-up and hand-made:

- `doc-health-nightly.yml` in the aggregation repo fires on
  `cron: "17 2 * * *"` and calls codexFactory's reusable doc-health
  workflow. A human decided this repo should have it, authored it, and
  merged it.
- The run gates itself on a readiness-attested runner plus an
  authenticated Hermes heartbeat (≤300s old) — served since 2026-07-19
  by the migrated hermes-readiness surface on the QA cluster.
- Findings land as a bot-authored rolling PR. `merge-master-approval.yml`
  auto-approves ONLY the low-risk envelope; everything else parks for
  the human gate (Brett).

The inversion: in a governed factory, *the existence of that cron* is
itself expert output. "Repos of this shape should run a nightly
doc-health sweep, reviewed like this" is Software Engineering domain
knowledge — exactly what the Domain Hermes layer (codexFactory) is FOR.
The GitHub Action should not be something a person remembered to add;
it should be something the domain SUGGESTED, policy CLEARED, and the
project REALIZED — with the whole chain on the traceability record.

## The three-layer flow (target shape)

Canonical layering: Customer / Client / Domain — Project / Company
Policy / Software Engineering in the opensoft self-client instance.

1. **Domain Hermes generates** (autonomous, read-only): the domain
   maintains a practice catalog bound to its capabilities
   (doc-health-checker is a promoted capability; its adoption profile
   says "repos holding governed docs SHOULD wire the thin nightly
   caller"). A periodic gap scan compares governed subjects (repos)
   against the catalog and emits a `practice_adoption_suggestion` for
   each gap. Generation is suggestion-only — no privileged act, so
   autonomy is safe by construction. Mechanics in
   `domain-practice-suggestion-generation.md`.
2. **Client (Policy) Hermes clears**: the suggestion is evaluated
   against company policy — spend, security posture, repo-boundary
   policy, credential implications. Two-tier decision exactly like the
   Merge Master precedent, one level up: a reviewed rules-as-code
   envelope auto-clears mature, low-risk practices ("likely yes"); the
   contested tail parks for the human policy liaison. Cleared output is
   an approval record with conditions.
3. **Project (Customer) Hermes realizes**: the cleared practice becomes
   an implementation job on the target repo — author the workflow file,
   open a PR through the factory's own review lane, merge under the
   factory's own gates. The realization is self-hosting: the machinery
   that reviews code reviews the PR that installs the reviewer's
   trigger. Details in `practice-clearance-and-project-realization.md`.
4. **Domain observes adoption**: the next gap scan sees the practice
   live (the Action exists, runs green, emits reports) and closes the
   suggestion with adoption evidence. Drift detection falls out for
   free: if someone deletes the workflow, the gap reopens and the
   suggestion regenerates.

## The second half: the review of the sweep's OUTPUT moves to Hermes too

The same inversion applies one level down. The rolling PR's review
today = rules-as-code envelope + Brett. The deployed QA Hermes runtime
has the approval machinery in schema (`hermes_approval_requests`,
`hermes_approvals` — empty; manager-review composition was explicitly
deferred by the runtime foundation change). Target: the nightly files
an approval request into Hermes; Hermes composes the review across the
three layers (domain judges technical soundness, policy judges
envelope/risk, project holds subject context); the composed approval
materializes as the PR review. Brett's gate narrows to what Hermes
escalates. Merge Master's envelope logic becomes a POLICY INPUT to that
composition rather than a freestanding GitHub workflow.

## Why both halves are the same pattern

Practice adoption (who wires the trigger) and output review (who
approves the PR) are both instances of: **domain expertise proposes,
policy clears, project executes, evidence closes the loop** — with a
rules-as-code envelope handling the high-confidence middle and humans
holding the contested tail. One contract family should serve both, or
we will grow two divergent approval vocabularies.

## Open questions (free-form; contradictions welcome)

- Is `practice_adoption_suggestion` a new record kind or a profile of
  the existing client-infrastructure-request family? The request family
  already carries subjects, execution bindings, approvals, evidence —
  but its subjects are infrastructure, not repo-practice gaps.
- Bootstrap recursion: the PR that installs the review machinery needs
  a review. Today's answer is Brett; is that formally the
  `thin-independent-approval` accepted-risk pattern again?
- The aggregation repo is the caller today. Is the "subject" of this
  practice the aggregation repo, the reusable-workflow owner
  (codexFactory), or the pair? Suggestion records need a crisp subject.
- Cadence: is the domain gap scan itself a nightly (a meta-sweep), and
  what stops suggestion loops (sweep suggests sweep)? Idempotency keys
  and dispositions, presumably — same as doc-health's contested class.
- Does a REJECTED suggestion suppress regeneration forever, for a term,
  or until the practice's maturity status changes? (Document lifecycle
  statuses — `standard` vs `ratified` — likely drive both generation
  eligibility and auto-clearance eligibility.)
- Multi-client future: one domain serves many clients; the same
  suggestion goes to each client's policy layer independently. Where
  does per-client suppression state live? (The Client Hermes tree,
  presumably — `config/clients/<ref>/`.)

## Exit path

Brainstorm → staging topic (feat-spec-shaped, claims + open questions)
once the shape stabilizes; likely lands as an openxFactory neutral
contract (suggestion/clearance/realization records) + a hermes-install
manager-review-composition change (the deferred piece) + a codexFactory
practice-catalog realization. First pilot: retro-adopt the EXISTING
doc-health-nightly action as a governed practice record with provenance,
so the pipeline's first suggestion is one whose answer is known.
