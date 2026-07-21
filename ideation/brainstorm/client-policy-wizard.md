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
Topics: client-hermes, policy-wizard, client-tuning, auto-clear-envelope,
operating-policy, approval-matrix, house-style, re-tuning, elicitation,
client-layer, layer-content-seeding
Repository context: openxFactory (wizard is a hermes-install runtime act writing config/clients/<client>/)
Captured: 2026-07-21

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
| Spend | runner-minute / compute ceilings | `operating-policy.yaml` |
| Security posture | who clears new external calls / foreign-input triggers | `operating-policy.yaml` |
| Approvers | named change + security approval authorities | `approval-matrix.yaml` |
| Escalation | ordered escalation contacts; out-of-band recovery path | `escalation-map.yaml` |
| Integrations | permitted integration classes; credential bindings (refs) | `integration-map.yaml` |
| Memory & consent | what may promote as domain-learning; consent profile | `memory-boundaries` tuning |
| House voice | warmth / formality / verbosity within the tunable bounds | `house_style` tuning |

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

## Authority & validation

- **Who runs it.** The company-policy `responsible_operator` (Brett, in the
  opensoft self-client). An open question: does the resulting envelope need the
  same thin-independent-approval floor the install already recorded, or is
  acknowledgement enough (mirroring the gate-rules council's human step)?
- **Validation.** The written tree is validated by the existing
  `openxFactory/scripts/validate-client-infrastructure.py` from the pinned
  openxFactory checkout (the opensoft tree already passes) — the wizard's output
  is not trusted until it validates.
- **Stricter-only guard.** The wizard must reject any answer that would make a
  gate *weaker* than the domain (the `stricter_only` invariant).

## Open questions

- **Interface.** Is the wizard a CLI lifecycle verb, an avatar-assisted flow
  (the scaffold's `user_interaction_scaffold` lists guided surfaces), or both?
- **Envelope ratification.** Auto-generate vs. always-human-ratify the conjunctive
  conditions (leaning: generate + one human acknowledgement).
- **Partial tuning UX.** How does the wizard show what is still defaulting to
  "park" so the operator knows the manual surface they are carrying?
- **Multi-unit clients.** One envelope per client, or per operating unit /
  customer class?
