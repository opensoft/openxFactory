# Practice Clearance and Project Realization: policy says yes, the project makes it real — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The second and third legs of the practice-adoption pipeline:
how the Client (Company Policy) Hermes clears a domain suggestion —
auto-clear envelope for the mature/low-risk middle, human liaison for
the contested tail — and how the Project (Customer) Hermes realizes a
cleared practice on the actual repo through the factory's own PR and
review machinery. Umbrella: `hermes-governed-nightly-sweep.md`;
generation side: `domain-practice-suggestion-generation.md`.
Topics: practice-clearance, auto-clear-envelope, project-realization,
client-policy, merge-master-pattern, practice-adoption
Repository context: openxFactory (client clearance + project realization behavior)
Captured: 2026-07-20

## Possible feats

- **Auto-clear envelope** — a ratified rules-as-code artifact for the
  mature/low-risk middle.
- **Clearance approval record** on the deployed approvals tables, carrying
  conditions that travel with the job.
- **Realization job flow** composing `proposed_realization` + conditions through
  the factory's own PR/review front door.

## Clearance at the Client (Policy) layer

The client's question is never "is this good engineering?" (the domain
already staked that); it is "is this allowed HERE?" Policy evaluates
the suggestion against company posture:

- Repo-boundary policy (does the realization put content where it may
  not live?), credential policy (does adoption mint/move credentials —
  the `credential_implications` field), spend (runner minutes, hosted
  compute), security posture (new external calls? new triggers that
  accept foreign input?), and precedent (has this practice class been
  cleared before?).

Two-tier decision, deliberately copying the Merge Master pattern one
level up:

1. **Auto-clear envelope (the "likely yes" path)**: a reviewed
   rules-as-code envelope clears suggestions conjunctively matching:
   practice maturity ≥ `standard`, risk_class low, no new credentials,
   realization is PR-only (no direct pushes), subject is a
   non-production QA-class subject, domain is a trusted first-party.
   The envelope itself is a ratified policy artifact — changing it is
   an OpenSpec change, exactly like merge-master-approval's envelope.
2. **Human gate**: anything failing or unevaluable parks for the
   company-policy liaison (Brett, in the opensoft self-client). The
   liaison's decisions accrete into dispositions that future envelope
   revisions can absorb — the human tail TRAINS the envelope.

Clearance output: an approval record (the deployed runtime's
`hermes_approval_requests`/`hermes_approvals` tables are the natural
home — currently empty, waiting for exactly this) carrying conditions
("runner must be readiness-attested", "workflow pinned to a released
ref", "report artifacts retained N days") that travel with the job.

## Realization at the Project (Customer) layer

A cleared practice becomes an implementation job for the project whose
repo it targets. The load-bearing rule: **the project layer implements
through the factory's own front door** — no side-channel writes.

1. Compose the job from `proposed_realization` + clearance conditions
   (the neutral-job-envelope shape fits).
2. An execution worker (omnigent execution lane) authors the change —
   for the nightly sweep: the thin caller workflow file, pinned to the
   reusable workflow at a released ref — and opens a PR.
3. Identity tiers per the github-administration capability: the
   content-only App identity writes branch content and opens the PR;
   anything needing admin tier (branch protection, runner groups,
   secrets) is a SEPARATE conditioned step through the administration
   workflow, never bundled silently into the content PR.
4. The PR is reviewed by the factory's normal review lane. This is the
   self-hosting move: the machinery that reviews code reviews the PR
   that installs the reviewer's own trigger. The clearance record rides
   along as review context ("policy already said yes to the WHAT; this
   review judges the HOW").
5. Merge → the Action exists → its first scheduled run's green result
   becomes the adoption evidence the domain's next gap scan closes on.

Failure paths stay honest: a realization PR that the review lane
rejects goes BACK as a suggestion disposition ("cleared but
unrealizable as proposed"), not into a silent retry loop.

## The recursion, named and kept

Three loops intentionally close over themselves:

- The sweep that reviews docs is itself installed by a reviewed PR.
- The envelope that auto-clears suggestions is itself a ratified,
  human-reviewed artifact.
- The gap scan that suggests sweeps is itself (eventually) a practice
  the domain suggests for its own runtime.

Each loop bottoms out at a human ratification somewhere — the same
`thin-independent-approval` accepted-risk shape the self-client install
already recorded. That is the answer to "who reviews the reviewer":
recursion with a ratified floor, not turtles all the way down.

## Pilot sketch (opensoft self-client, cheapest honest first run)

1. Retro-adopt: record the EXISTING doc-health-nightly action as an
   adopted practice (catalog entry + adoption evidence + provenance
   "hand-installed pre-pipeline, 2026-07"). No cluster or repo change;
   pure records. Proves the record shapes on a known-true case.
2. First live suggestion: pick a real gap — e.g. a sibling repo that
   holds governed docs but has no sweep caller — and run the pipeline
   end to end: suggestion → envelope evaluation (will likely park for
   Brett; good — exercises the human gate first) → clearance →
   realization PR through the review lane → adoption evidence.
3. Only then wire manager-review composition (the piece the runtime
   foundation change deferred) so clearance and PR review compose IN
   the deployed Hermes rather than in freestanding GitHub workflows —
   Merge Master's envelope folds in as policy input at that point.

## Open questions

- Approval record locality: clearance happens at the Client layer but
  the deployed runtime is one stack serving all three layers — do
  approvals carry a `hermes_layer` discriminator (the transition
  records in the client-infrastructure requests already do)?
- Conditions enforcement: are clearance conditions checked at
  realization time (review lane assertion), at runtime (the sweep's own
  readiness gate), or both? (Leaning both — conditions worth stating
  are worth checking twice.)
- Who is the PR author-of-record — the project Hermes, the execution
  worker, or the domain? (Traceability wants all three on the record;
  GitHub wants one App identity. The traceability edges table exists
  for exactly this.)
- Rollback of an adopted practice: is "remove the sweep" itself a
  suggestion (a negative one), and does it need a HIGHER clearance bar
  than adoption? (Leaning yes: removing governance is riskier than
  adding it.)
- Does the project layer ever refuse a cleared practice? (A project
  with a frozen change window, say. Probably yes — a deferred
  disposition with a term, not a veto.)
