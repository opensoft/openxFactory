# Implementation Notes — 012-wallet-issuer-anchor

## Phase status: clarify closed; implementation not yet started

Spec authored and clarified (see [clarify-questions.md](clarify-questions.md));
checklist all-pass. Plan, tasks, and code realization follow in later phases.
Counts asserted in SC-002 are recorded as evidence at implementation time.

## Grounding facts (researcher, 2026-08-23)

- Validator currently reads `issued_by` through zero rules — S2 is the field's
  first real enforcement.
- Packaged corpus exposure: five grant positives, all transaction-act class,
  none carrying `issued_by`; the widening must cost them nothing (US3 boundary
  guard, FR-008).
- Root-vs-child shape follows existing attenuation logic; S2 adds no
  child-specific rule unless a ratified gap surfaces.

## Rulings encoded

- Class marker: scope `acts` vocabulary; canonical token `review` as named
  validator constant beside the custody-registry path reference (architect;
  confirmed against ratified vocabulary).
- Anchor: validator constant citing the Human Escalation Contract at
  `docs/roles-and-authority.md:103-140`; machine tokens and legacy `opensoft`
  refused at roots; exact-match `Brett Heap` accepted (convener).
- Specimens: three negatives under `contracts/openxwallet/examples/negative/`
  (`grant-review-authority-omits-issued-by.yaml`,
  `grant-review-root-issuer-is-a-machine.yaml`,
  `grant-review-root-issuer-says-opensoft.yaml`).

## Durable relay obligation — wallet-substrate linkage (convener-accepted, 2026-08-24)

From the R4 × `add-regular-pr-council-clearance` reconciliation: the clearance
draft amends the two authorship requirements so human-authored PRs become
tier-2-clearable **after soak — with zero reference to the wallet substrate**
(trust anchor = verdict quality + soak evidence), while the wallet arc premises
autonomy over authored logic on authority *provenance*: grants binding the three
deliberation seats, arriving at S3+. Both postures are internally coherent; they
differ on whether provenance is a precondition or a parallel track.

Convener accepted the recommended minimum: **enrollment activation carries a
recorded accepted-risk note referencing the wallet arc**. That note is now
recorded on the codexFactory side
(`openspec/changes/add-regular-pr-council-clearance/clarifications.md`, entry
*"Wallet substrate provenance vs soak-evidence-only activation"*) and MUST be
surfaced at that change's Gate-Rules convening before any enrolled surface
activates. If S3's exercise-record substrate lands first, activation must be
re-examined against grant-carried seats rather than soak evidence alone.

This section is the durable openxFactory-side copy: S2's artifact set travels to
PR with the obligation restated here regardless of where the codexFactory change
stands at merge time.

## Related withdrawal (recorded for the archive)

The interim R4-B sketch (schema-level `classification_intent` field,
codexFactory side) is withdrawn permanently — superseded by absorption into the
clearance draft's third rule state `advisory`. Recorded so no successor effort
resurrects it.
