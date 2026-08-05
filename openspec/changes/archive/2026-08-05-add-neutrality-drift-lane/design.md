# Design: add-neutrality-drift-lane

## D1. Seed-first altitude — the lane files DTN candidates, not OpenSpec changes

"Create a proposal to move it" is realized at the register's altitude:
the lane drafts a DTN seed (row + detail section + evidence), because
that is the family's ratified promotion queue and its lifecycle
(`seed → staged → openspec → implemented → adopted`) already encodes
the human gates. Auto-authoring full OpenSpec move-changes would skip
the staging the DTN process requires and bury Brett in artifacts he has
not asked for yet. The manual precedent is exactly this shape: the
2026-08-03 sweep filed DTN-018..023 as seeds; approved ones became
`adopt-neutral-utility-pack` and the openAvatar extraction within a day.

## D2. Two-stage detection — deterministic pre-filter, model scout second

Stage 1 (pure code, no model calls, cheap every night): candidate
signals — near-duplicate similarity against openxFactory's tree (the
contract-copy-drift family's machinery generalized), schemas/scripts
with zero hits against the domain's own lexicon (each factory's
ontology/term registry), cross-repo consumers (other repos' docs or
workflows referencing the file), and tooling uninventoried in the
domain's stack.yaml. Stage 2 (model-driven, bounded, only over stage-1
survivors plus files changed since the last run): the neutrality rubric
from the sweep — "would another domain need this essentially
unchanged?" — under a versioned prompt contract returning structured
candidates (paths, neutrality evidence, counter-evidence,
domain-local exclusions). Stage 2 follows the organizer/cataloger
dispatch pattern: deterministic selection, bounded batch, structured
output validated before anything is written.

## D3. Delivery and approval ride existing mechanisms

Candidates land in the rolling health PR as (a) a drafted register
addition and (b) ranked-plan items — the same surfaces Brett already
reviews. Approval is his merge of the register addition; rejection is a
recorded disposition in `health/dispositions.yaml` keyed by
(repo, path, content digest), which suppresses re-filing until the
content changes. No new inbox, no new approval surface.

## D4. Nothing moves automatically — ever

The lane's write surface is exactly: register-draft text and plan items
inside the rolling PR, plus its own state file. It never edits a domain
repo, never opens a move PR, never touches contracts. The existing
doc-health authority requirement covers this; the spec delta restates
it in the lane's own scenario so the boundary survives quoting out of
context.

## D5. Scope — the five domain factories

`xFactories/*` pinned repos only. openxFactory is the destination, not
a subject; installs (agenttower, hermes-install, omnigent-install) are
runtime realizations whose code is expected to be install-specific, and
openAvatar is already neutral — all excluded from v1. Widening later is
a register-visible dial, not a code fork.

## D6. Cadence and cost — incremental by default

Rides the existing nightly. Stage 2 reviews only stage-1 survivors and
content changed since the lane's last recorded run (the cataloger's
incremental-selection precedent), with a bounded per-night batch and a
carry-over queue, so cost stays flat and a quiet week costs near zero.
A `neutrality-baseline` manual dispatch input allows a one-time full
sweep per repo (the 2026-08-03 codexFactory sweep is the recorded
baseline for codexFactory).
