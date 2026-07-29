# Client Policy Wizard: turning the scaffold's blanks into a tuned client — Brainstorm

Status: brainstorm
Kind: process
Summary: The guided elicitation that tunes a scaffolded client into a real one —
it asks the operating organization a bounded set of questions and writes the
answers into `config/clients/<client>/` as the operating policy, approval
matrix, integration map, and (its load-bearing output) the auto-clear envelope
the clearance pipeline runs on. Conservative by default: until a policy is set,
everything parks for the human liaison, so an un-tuned client is safe. Re-running
is idempotent re-tuning, and the liaison's accreted dispositions feed the next
pass. Parent: `client-layer-scaffold.md`; writes the content shaped in
`client-layer-content-draft.md`.
Topics: client, client-hermes, policy-wizard, client-tuning, auto-clear-envelope,
operating-policy, approval-matrix, house-style, re-tuning, elicitation,
client-layer, layer-content-seeding
Repository context: openxFactory (wizard is a hermes-install runtime act writing config/clients/<client>/)
Captured: 2026-07-21

Updated: 2026-07-22 (interface + envelope-scope decisions; ratification/facts/seeding sync; cost blocks; park-map)

## Decided (2026-07-22)

- **Interface: avatar-assisted first.** The primary wizard experience is the
  avatar-guided flow (the scaffold's `user_interaction_scaffold` surfaces; ties
  to the avatar pilot work already in staging) — the operating organization is
  interviewed, not handed a form. The **elicitation schema is the contract**;
  a CLI verb drives the same schema as the fallback/automation path, but the
  avatar flow leads.
- **Envelope scope: per-unit allowed, per-client default.** The envelope
  carries a `scope` field; a simple client ratifies one, a multi-unit client
  may ratify one per operating unit / customer class — each separately
  human-ratified.
- **Envelope ratification (synced):** wizard drafts, human **ratifies** —
  stronger than the earlier acknowledgement leaning; nothing auto-clears
  un-ratified (`client-layer-content-draft.md` §Decided).
- **The facts rule governs the question set (synced):** anything justifiable
  for any engineering org is a domain default the wizard merely confirms;
  anything naming a client-specific fact is wizard-only
  (`client-layer-scaffold.md` §Decided).
- **Output is an overlay (synced):** per the unified seeding decision
  (`hermes-layer-seeding-mechanism.md`), the wizard's final step **packages
  the tuned tree as the per-client overlay document, commits it, and records
  its digest pin** — client content then seeds through the same pipeline as
  the domain's (fail-closed digest verify, stricter-only check at step 4).

## Possible feats

- **The wizard tool** (a hermes-install lifecycle verb / guided flow).
- **The elicitation schema** — the bounded question set + defaults.
- **Envelope generator** — compose the auto-clear envelope from answers.
- **Re-tuning + disposition feedback** loop.

## What it is

A scaffolded client (neutral scaffold + domain specialization) has
governance-shaped *blanks*. The wizard fills them by asking the organization,
then writes a validated client tree. It is an **install-runtime act**
(hermes-install), not domain content — the domain ships the questions and
defaults; the wizard collects the client's answers.

## Elicitation (the bounded question set)

Each block maps to a content file (`client-layer-content-draft.md`). Questions
are few, plain-spoken (house style), and every one has a conservative default:

| Block | Asks | Writes |
| --- | --- | --- |
| Identity & tenant | operating units, supported customer kinds | `client-profile.yaml` |
| Offers | which offer shapes this client sells/operates | `offer-catalog.yaml` |
| Repo boundaries | which repos/paths may / may never be touched | `operating-policy.yaml` |
| Realization | PR-only? any exceptions? | `operating-policy.yaml` |
| Credentials | which families allowed; confirm prod/deploy never standing | `operating-policy.yaml` |
| Spend & accounting | budget envelopes (runner minutes, compute, credits/project); **tracking granularity** the subject layer must honor | `operating-policy.yaml` (FAO-owned blocks) |
| Security posture | who clears new external calls / foreign-input triggers | `operating-policy.yaml` |
| Approvers | named change + security approval authorities | `approval-matrix.yaml` |
| Escalation | ordered escalation contacts; out-of-band recovery path | `escalation-map.yaml` |
| Integrations | permitted integration classes; credential bindings (refs) | `integration-map.yaml` |
| Memory & consent | what may promote as domain-learning; consent profile | `memory-boundaries` tuning |
| House voice | warmth / formality / verbosity / humor within the tunable ranges — respect + discretion locked, warmth floored at moderate (roster §Decided) | `house_style` tuning |

## The load-bearing output: the auto-clear envelope

The wizard composes the conjunctive auto-clear envelope from the answers —
practice maturity ≥ standard, risk low, no new credentials, PR-only realization,
non-production subject, trusted first-party domain. This is how a client's
"likely-yes" middle gets defined **without hand-authoring rules-as-code**, and
it is the input the clearance pipeline (`practice-clearance-and-project-
realization.md`) runs on. Anything the envelope does not conjunctively cover
parks for the human liaison.

## Defaults, safety, and re-tuning

- **Conservative defaults.** Every unanswered block defaults to "park for the
  human" — an un-tuned or partially-tuned client is safe, just fully manual. The
  wizard never auto-clears anything it wasn't explicitly told it may.
- **Idempotent re-tuning.** Re-running merges/overwrites the tree; it is the same
  verb as initial tuning. Loading updated company policy is just a re-run.
- **Disposition feedback.** The human liaison's accreted parking dispositions
  (from the clearance pipeline) are surfaced as candidate envelope revisions on
  the next pass — the human tail *trains* the envelope over time.
- **The park-map (manual-surface report).** Every wizard run — full or partial
  — ends by emitting an evidence-shaped **park-map**: exactly which blocks
  still default to "park for the human," and therefore the manual load the
  operator is carrying. Partial tuning stops being invisible; re-tuning
  progress is measurable run over run (the park-map shrinks), and the
  disposition-feedback loop reads it to propose the next questions worth
  answering.

## Authority & validation

- **Who runs it.** The company-policy `responsible_operator` (Brett, in the
  opensoft self-client). An open question: does the resulting envelope need the
  same thin-independent-approval floor the install already recorded, or is
  acknowledgement enough (mirroring the gate-rules council's human step)?
- **Validation.** The written tree is not trusted until it validates. Honest
  scope note: the existing `openxFactory/scripts/validate-client-infrastructure.py`
  covers only the client-*infrastructure* records (the opensoft tree passes it);
  the wizard's new shapes (`operating-policy`, `approval-matrix`,
  `integration-map`, the envelope) need their own schemas + checks — authoring
  those validators is part of this feat, not a given.
- **Stricter-only guard.** The wizard must reject any answer that would make a
  gate *weaker* than the domain (the `stricter_only` invariant).

## Open questions

- ~~**Interface**~~ — DECIDED 2026-07-22: avatar-assisted first, CLI drives
  the same elicitation schema as fallback (§Decided).
- ~~**Envelope ratification**~~ — DECIDED 2026-07-22: wizard drafts, human
  ratifies, always (§Decided).
- ~~**Partial tuning UX**~~ — answered structurally: the park-map report
  (§Defaults, safety, and re-tuning).
- ~~**Multi-unit clients**~~ — DECIDED 2026-07-22: per-unit allowed,
  per-client default, each separately ratified (§Decided).
- **Wizard overlay signing** — the wizard commits a per-client overlay
  (§Decided); who signs its digest pin and where it is recorded is the open
  question shared with `hermes-layer-seeding-mechanism.md`.
- **Avatar-flow prerequisites** — which of the staging avatar capabilities
  (pilot hardening, live voice) the guided flow actually needs before it can
  lead.
