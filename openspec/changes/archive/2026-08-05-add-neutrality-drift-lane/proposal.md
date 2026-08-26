---
code_surface: openxFactory (scripts/doc_health/ neutrality lane + prompt contract + dispatch wiring + tests; reusable nightly workflow input; no domain-repo or aggregation code)
target_release: none
Status: ratified
Ratified: Brett's approval of `add-neutrality-drift-lane` on 2026-08-04 (PR #64 review), with D1-D6 carried as decided (seed-first altitude, two-stage detection, rolling-PR delivery, never-moves boundary, xFactories/* v1 scope, incremental cadence)
---

# Proposal: add-neutrality-drift-lane

## Why

The 2026-08-03 codexFactory neutrality sweep found ~73k LOC of
domain-neutral content that had accumulated in one domain repo — found
manually, years of drift late, and only because Brett asked the
question. The drift mechanism is permanent: domain factories are where
work happens, so neutral-shaped schemas, validators, process docs, and
tools are born there and stay there until someone looks. The family now
has everything such a check needs except the check itself: the
doc-health pipeline runs nightly over every pinned repo from
openxFactory (relocated by `adopt-neutral-tooling-home`), it already
operates model-driven lanes under prompt contracts with deterministic
dispatch (organizer, cataloger, readiness scorer, possibles deriver),
it already delivers findings through a rolling PR a human approves, and
the DTN candidate register plus the domain-to-neutral promotion process
are the ratified queue for exactly this kind of finding. What is
missing is the standing scout (Brett, 2026-08-04: "add to the nightly
run to check the domain factories for anything that belongs in
openxFactory... create a proposal to move it and then ask for Brett to
approve that proposal").

## What Changes

- MODIFIED `doc-health` — ADD the neutrality-drift lane: a nightly,
  incremental, model-driven review of domain-factory content against the
  domain-neutral boundary, behind deterministic pre-filter signals
  (duplicate/near-duplicate of a neutral artifact, zero domain-lexicon
  hits in a schema/script, external consumers reaching into the repo,
  uninventoried tooling mass). The lane runs under a versioned prompt
  contract with the same dispatch discipline as the existing lanes.
- The lane's OUTPUT is a staged proposal, never an action: each finding
  becomes a drafted DTN-register seed candidate (register row + detail
  section with evidence paths and domain-local exclusions, the
  register's own format) plus a ranked-plan item, delivered through the
  existing rolling health PR. Brett's approval of the seed — merging the
  register addition and dispositioning the item — is the gate; movement
  itself then follows the ratified domain-to-neutral promotion process
  (staged topic → OpenSpec change → tranche moves), never the nightly.
- Suppression is first-class: a candidate Brett rejects gets a recorded
  disposition (the existing `health/dispositions.yaml` mechanism) and is
  not re-filed while the content is unchanged.
- No new authority: the doc-health ownership requirement ("health
  tooling reports and stages, it never approves or merges another
  factory's content") governs this lane verbatim.

## Impact

- Spec: `doc-health` MODIFIED (one ADDED requirement block via delta).
- Code: a new lane module + prompt contract + dispatch wiring in
  `scripts/doc_health/`, tests under `tests/doc-health/`, and one
  opt-out input on the reusable nightly workflow (default on).
- Consumers: the aggregation nightly needs no change (`secrets:
  inherit`, new input defaulted); the rolling health PR gains a
  "neutrality candidates" section when the lane finds something.
- The DTN register becomes partially machine-fed; its Status lifecycle,
  format, and the promotion process are unchanged — the lane only
  drafts seeds for human approval.
