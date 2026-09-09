# Tasks: prepare-openspec-1-12-readiness

Status: draft

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request, measured under both CLI versions and recorded in
`evidence/openspec-1.12-readiness-2026-09-05.md`. Group 4 is REFUSED work and
group 5 is OWED work; neither is ticked and each names why.

**RATIFICATION HAS NOT HAPPENED.** Brett Heap admitted this packet to the
queue on 2026-09-05 (*"start the 1.12 upgrade fixes"*). Task 7.1 records
ratification when it happens and nothing below decides it.

---

## 1. The 39 placeholder Purposes (main specs, edited directly)

Each spec's `## Purpose` read the sentence `openspec archive` writes for a new
capability: `TBD - created by archiving change <X>. Update Purpose after
archive.` Each is replaced by a Purpose derived from that spec's own
requirement headers and the CREATING change's archived proposal. **The main
spec is edited directly, and no delta is written**, per the rule the 1.12
message itself states: a `## Purpose` in a delta is read only when the
capability is created.

- [x] 1.1 `avatar-brokered-call-feasibility` — Purpose written from its own `### Requirement`
      headers and from `archive/*-qualify-avatar-brokered-call-feasibility/proposal.md`.
- [x] 1.2 `avatar-client-lab` — Purpose written from its own `### Requirement`
      headers and from `archive/*-implement-avatar-client-lab/proposal.md`.
- [x] 1.3 `avatar-client-runtime` — Purpose written from its own `### Requirement`
      headers and from `archive/*-define-avatar-client-contract-kernel/proposal.md`.
- [x] 1.4 `avatar-first-ui` — Purpose written from its own `### Requirement`
      headers and from `archive/*-align-avatar-first-ui-standard/proposal.md`.
- [x] 1.5 `avatar-lab-evidence` — Purpose written from its own `### Requirement`
      headers and from `archive/*-adopt-avatar-client-lab-candidates/proposal.md`.
- [x] 1.6 `avatar-reference-runtime` — Purpose written from its own `### Requirement`
      headers and from `archive/*-implement-avatar-reference-runtime/proposal.md`.
- [x] 1.7 `capability-health` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-capability-steward/proposal.md`.
- [x] 1.8 `chain-anchoring` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-chain-anchoring/proposal.md`.
- [x] 1.9 `client-identity-roster` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-client-identity-roster/proposal.md`.
- [x] 1.10 `client-infrastructure-liaison` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-client-infrastructure-liaison/proposal.md`.
- [x] 1.11 `client-infrastructure-request` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-client-infrastructure-liaison/proposal.md`.
- [x] 1.12 `consent-instrument` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-consent-instrument/proposal.md`.
- [x] 1.13 `crystallization-build` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-crystallizer-contracts/proposal.md`.
- [x] 1.14 `crystallization-consent` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-crystallizer-contracts/proposal.md`.
- [x] 1.15 `crystallization-decision` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-crystallizer-contracts/proposal.md`.
- [x] 1.16 `crystallization-dispatch` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-capability-steward/proposal.md`.
- [x] 1.17 `crystallized-capability-registry` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-capability-steward/proposal.md`.
- [x] 1.18 `deployment-handoff-boundary` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-deployment-handoff-boundary/proposal.md`.
- [x] 1.19 `document-cataloging` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-document-cataloging/proposal.md`.
- [x] 1.20 `domain-conformance-checks` — Purpose written from its own `### Requirement`
      headers and from `archive/*-adopt-neutral-utility-pack/proposal.md`.
- [x] 1.21 `domain-descendant-boundary` — Purpose written from its own `### Requirement`
      headers and from `archive/*-split-openxwallet-repo/proposal.md`.
- [x] 1.22 `domain-ontology-lifecycle` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-domain-ontology-layer/proposal.md`.
- [x] 1.23 `governed-derived-model` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-governed-derived-model/proposal.md`.
- [x] 1.24 `ideation-cross-reference` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-ideation-dashboard/proposal.md`.
- [x] 1.25 `ideation-dashboard` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-ideation-dashboard/proposal.md`.
- [x] 1.26 `ideation-routing` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-cross-factory-ideation-routing/proposal.md`.
- [x] 1.27 `layer-vocabulary` — Purpose written from its own `### Requirement`
      headers and from `archive/*-adopt-subject-tenant-domain-vocabulary/proposal.md`.
- [x] 1.28 `medxchart-overlay-boundary` — Purpose written from its own `### Requirement`
      headers and from `archive/*-create-medxchart-overlay-boundary/proposal.md`.
- [x] 1.29 `medxpractice-overlay-boundary` — Purpose written from its own `### Requirement`
      headers and from `archive/*-create-medxpractice-overlay-boundary/proposal.md`.
- [x] 1.30 `neutral-product-pin` — Purpose written from its own `### Requirement`
      headers and from `archive/*-split-openxwallet-repo/proposal.md`.
- [x] 1.31 `omnigent-domain-overlay` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-omnigent-domain-overlay/proposal.md`.
- [x] 1.32 `omnigent-install-manifest` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-omnigent-domain-overlay/proposal.md`.
- [x] 1.33 `pattern-ledger` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-pattern-ledger/proposal.md`.
- [x] 1.34 `release-realization` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-release-realization-flow/proposal.md`.
- [x] 1.35 `release-surface-integrity` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-release-inventory-drift-check/proposal.md`.
- [x] 1.36 `signed-execution-chain` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-signed-execution-chain/proposal.md`.
- [x] 1.37 `subject-establishment` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-subject-establishment/proposal.md`.
- [x] 1.38 `workstation-intake` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-xfactory-installer-repository/proposal.md`.
- [x] 1.39 `xfactory-semantic-kernel` — Purpose written from its own `### Requirement`
      headers and from `archive/*-add-domain-ontology-layer/proposal.md`.

## 2. The one spec delta

- [x] 2.1 ONE `## ADDED Requirements` delta on `document-lifecycle` — *A
      promoted specification carries a written Purpose, repaired in the
      promoted specification*. **Written because strict validation DEMANDS a
      delta** (`1.2.0`: *"Change must have at least one delta. No deltas
      found."*), not because doctrine was wanted; and it states only what this
      packet had to learn to do group 1 at all — the archive act writes the
      placeholder, and a delta's `## Purpose` is read solely at capability
      creation, so the promoted spec is the only surface the repair lands on.
      Placed on `document-lifecycle` beside its existing *Ratified spec deltas
      reach the promoted specification* and its two MODIFIED-block rules.
      Three scenarios; no existing requirement touched.

## 3. The task-group header

- [x] 3.1 `add-doxchat-model-intake/tasks.md` gains the `## 4.` header its
      tasks `4.1` and `4.2` always belonged under. **NOTHING RENUMBERED:** the
      pair is cited as "4.1"/"4.2" in five places already written down —
      `proposal.md` twice, task 0.3, and the Amendment Record twice — one of
      which is a dated amendment that renumbering would have falsified. The
      tasks, their text and their unticked state are untouched.
- [x] 3.2 A dated note recording 3.1 added to that packet's own Amendment
      Record, where its next reader will meet it.

## 4. The four archive-refusal orderings (INFO, recorded not repaired)

Read rather than assumed, all four are one shape: a MODIFIED delta whose
target is ADDED by a DIFFERENT change that is also still active. **No delta is
repointed and no intent is rewritten** — each is correct as written and waiting
on archive ORDER, which no packet may take on another's behalf. These are
`[INFO]` in `validate` and **do not count against the 0-failed target.**

- [x] 4.1 `add-wallet-carried-review-authority` → `roles-authority-model`
      § *Pilot repository and reviewing domain*, ADDED by
      `add-substantive-review-lane`. Verified by locating the header in that
      change's `## ADDED Requirements` block; the delta's own 2026-08-31
      marker already states the dependency in words. Historical intent read at
      PR #583, the S5 register act, per the readiness manifest. Dated note
      added to the modifying change's `tasks.md`.
- [x] 4.2 `implement-keycloak-install-repo` → `repo-boundary-governance`
      § *Keycloak install repository boundary*, ADDED by
      `add-identity-brokering`. Same method, same shape. Dated note added.
- [x] 4.3 `implement-openxpki-install-repo` → `repo-boundary-governance`
      § *OpenXPKI install repository boundary*, ADDED by `add-trust-anchor`.
      Same method, same shape — 4.2 and 4.3 are ONE pattern (an install-repo
      boundary requirement promoted by the change that establishes the
      product, consumed by the change that builds the repository) and are
      treated identically. Dated note added.
- [x] 4.4 `add-cpc-clearing-boundary` → the whole `clearing-dispatch-boundary`
      spec, which does not exist because `add-clearing-dispatch-boundary`
      creates it and has not archived. `admit-deliberation-clearing-operation`
      validates clean against the same absent spec because ADDED on a new spec
      is legal, which is the control that proves the shape. Dated note added.

## 5. REFUSED — the two ERROR-level items, and why they stay

**THE PACKET'S VETO POINT.** Not ticked, and not to be ticked by this packet.

- [ ] 5.1 `add-chain-attestation` :: `signed-execution-chain` MODIFIED
      *"A gate validates the short chain as a hash-linked chain"* omits
      canon's *"a tranche-two link does not exist yet"*. The block carries the
      house RESERVED MARKER declaring the rename, and the successor scenario
      exists because the old antecedent had become a PERMISSION for exactly
      the chain this tranche refuses (council LA-A1). **Restoring the title
      reinstates the contradiction the change was ratified to close.**
- [ ] 5.2 `add-composed-view-authoring` :: `ideation-dashboard` MODIFIED
      *"Composed views are read-only with a repository jump"* omits canon's
      *"Gate verbs hide on a composed view"*, renamed to *"Tile-bound gate
      verbs hide on a composed view"* by the same change, declared by its own
      landed marker (#444). **The promoted `doc-health` requirement
      *"Currency of an active change's MODIFIED requirement blocks"* uses THIS
      EXACT PAIR of titles as its own worked example of a correct
      `Merged into` marker.** Restoring the unqualified title would also
      contradict the sibling scenario admitting document creation.
- [ ] 5.3 **For the convener, not for this lane:** 1.12.0's scenario-currency
      check is marker-blind and contradicts promoted canon. Pick one — sequence
      the bump after both changes archive (both findings then vanish, archived
      changes being outside `--all`); carry a dispositioned exception; or take
      it upstream so the check reads the two reserved marker forms. **Until one
      is picked, `1.12.0 --strict` cannot read 0 failed here and
      `openspec archive` at 1.12.0 would refuse both changes.**

## 6. OWED — not taken here, and stated so it is not lost

- [ ] 6.1 All four changes in group 4 read `declares: absent` in
      `tests/sequenced_after/corpus-ledger.yaml`, and this repository already
      has the instrument for their dependency — the `sequenced_after:`
      front-matter field. Declaring it would edit four ratified proposals this
      packet has no mandate over and move four ledger rows beyond its own, and
      `add-sequenced-after-substrate`, which builds the validator that reads
      them, is itself still active and unrealized. Owed to those packets.
- [ ] 6.2 THREE of those four MODIFIED blocks carry NO basis marker, and
      promoted canon requires one: `document-lifecycle` § *A MODIFIED block
      over a requirement no promoted specification carries declares its basis
      by marker*. `add-wallet-carried-review-authority` HAS its marker, dated
      2026-08-31 — which is how its ordering was read here in the first place.
      `implement-keycloak-install-repo`, `implement-openxpki-install-repo` and
      `add-cpc-clearing-boundary` owe theirs. **NOT SUPPLIED HERE:** a basis
      marker goes inside another packet's MODIFIED block, where it is a unit
      the `modified-block-currency` reader counts, so writing three of them
      from outside those packets is a change to three ratified deltas rather
      than a note beside them. Owed to those packets; the dated ordering note
      group 4 added to each points at it.

## 7. Ratification and verification

- [ ] 7.1 Brett ratifies or amends this packet. The 2026-09-05 word admitted
      it to the queue and settled nothing in group 5.
- [x] 7.2 `python3 scripts/validate-openspec-cli-pin.py --all --strict` — the
      PINNED entrypoint, unchanged at `1.2.0`. Before and after recorded
      verbatim in the evidence record.
- [x] 7.3 `OPENSPEC_TELEMETRY=0 npx -y @fission-ai/openspec@1.12.0 validate
      --all --strict` — before and after recorded verbatim, with the residual
      `[INFO]` lines listed.
- [x] 7.4 Doc-health, the house validators that read specs or changes, and
      `pytest tests/sequenced_after/ tests/doc-health/`. Tails in the evidence
      record.
- [x] 7.5 Ledger row seeded with the command the sweep's own failure names.
