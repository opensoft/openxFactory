---
code_surface: openxFactory (receives the three domain-conformance check scripts + tests/conformance-gate/, scripts/proposal-support.py + tests/proposal-support/, and the Hermes layer-template schema at contracts/hermes-domain-overlay/hermes-layer-template.schema.json), codexFactory (sheds the same surface in a named follow-up PR — change/shed-neutral-utility-pack: validate-docs.sh repoints to the pinned-checkout copies; stack.yaml + schemas/README.md drop the hermes-template inventory entries)
target_release: none
Status: ratified
Ratified: Brett's 2026-08-03 approval of the presented DTN-018/019/021 scope ("do both - the utility pack change and the runbook move")
---

# Proposal: adopt-neutral-utility-pack

## Why

Three DTN candidate-register entries, all surfaced by the 2026-08-03
codexFactory neutrality sweep, describe small neutral utilities still hosted
in the engineering domain repo. In the register's own words
(`docs/domain-neutralization-candidate-register.md`):

1. **DTN-018 — Domain-repo conformance-gate check pack.** "Three generic
   domain-repo conformance checks live in codexFactory with no engineering
   vocabulary: stack.yaml ↔ on-disk ↔ README required-artifact agreement,
   workflow `.md` transition targets ↔ `.yaml` gate `produces[]` parity, and
   stack.yaml `contract_ref` ancestry vs the aggregation pin. Every domain
   factory has a `stack.yaml`, workflow doc pairs, and an openxFactory pin;
   the workflow-gate-contract rule already says canonical validators run
   from the pinned checkout, never copied into domain repos, and
   `check-openxfactory-pin.py` partially duplicates
   `validate-domain-openxfactory-pins.py`." The run-from-pinned rule is the
   point: the checks belong where the rule says domain repos must consume
   them from.
2. **DTN-019 — Proposal-support lifecycle tool.** "Sharpened by
   `adopt-neutral-tooling-home`: the doc-health checker (family 5, proposal
   supporting-document integrity) now lives in openxFactory while the only
   producer of the artifacts it checks remains a codexFactory script. The
   tool moves staged supporting documents into an active change, rewrites
   links, and preserves the bundle through OpenSpec archive with sha256
   manifests — zero domain vocabulary in 545 LOC." That
   producer-in-one-repo / consumer-in-another inversion is exactly the class
   `adopt-neutral-tooling-home` was ratified to end.
3. **DTN-021 — Subject/tenant Hermes layer template schema.**
   "`hermes-template.schema.json` carries no domain vocabulary at all —
   `subject_kinds`, `required_subject_fields`, `layer_name`, `role`, `owns`,
   `must_not_own` — and the neutral home family already exists
   (`contracts/hermes-domain-overlay/`,
   `domain-installation-overlay.schema.yaml`)." The receiving family is
   already promoted canon; only the file is missing from it.

## What Changes

- ADDED `domain-conformance-checks` — a new capability: openxFactory owns
  the neutral conformance-check pack (inventory consistency, workflow state
  parity, openxFactory pin ancestry), run from the pinned checkout against a
  target domain repo, never copied into domain repos; and the three verified
  properties a conformant domain repo must hold.
- `document-lifecycle` — one ADDED requirement: the canonical
  supporting-document mover (`scripts/proposal-support.py`) is
  openxFactory-owned, implementing the already-promoted proposal-owned
  supporting-document and archive-retention requirements; doc-health
  family 5 checks its artifacts.
- `hermes-domain-overlay` — one ADDED requirement: the neutral
  subject/tenant layer-template schema joins the overlay contract family as
  `contracts/hermes-domain-overlay/hermes-layer-template.schema.json`
  (design D4: this promoted capability governs
  `contracts/hermes-domain-overlay/`, so the requirement lands here rather
  than in `domain-conformance-checks` — wrong altitude).
- codexFactory sheds the moved surface in a named follow-up PR
  (`change/shed-neutral-utility-pack`); its `validate-docs.sh` repoints the
  three checks at the resolved pinned-checkout copies with path-only edits
  (design D2) and its `stack.yaml`/`schemas/README.md` drop the
  hermes-template inventory entries (verified at the adoption pin).
- Register rows DTN-018/019/021 move to `implemented` in this change;
  `adopted` waits for the codexFactory shed and gate repoint.

## Impact

- Specs: `domain-conformance-checks` (new), `document-lifecycle` (+1
  requirement), `hermes-domain-overlay` (+1 requirement).
- Files adopted (provenance: codexFactory main@
  `1568c54b65e0de1dc63d9eef771f299ddbe60fcf`, copy-with-provenance, no
  history graft — design D1): `scripts/check-inventory-consistency.py`,
  `scripts/check-workflow-state-parity.py`,
  `scripts/check-openxfactory-pin.py`, `scripts/proposal-support.py`
  (~870 source LOC), `tests/conformance-gate/`, `tests/proposal-support/`
  (~500 test LOC), and the layer-template schema (74 lines, JSON retained).
- `proposal-support.py` is adopted byte-identical; the three checks carry
  only classified hygiene edits (capability naming, help text, and the
  wrong-target self-repo CLI defaults dropped — tasks 1.2); the schema
  differs from source only in `$id`/title/description (design D4).
- The adopted suites run under openxFactory's pytest surface beside the
  tranche-A/B suites; the existing hermeticity guard (`nlm`/`gh`) covers
  them with no new seams.
- No contract bundle change: `contracts/manifest.yaml` is untouched; bundle
  publication of the layer-template schema rides the next contract release
  (spec delta scenario). `target_release: none`.
