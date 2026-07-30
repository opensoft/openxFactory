---
code_surface: openxFactory (`contracts/domain-ontology/core/` content lifecycle + governed release records + retained snapshots, the regenerated fixture corpus/pilots/gateway examples, the omnigent install example's kernel pin, `contracts/manifest.yaml` kernel digests); MedxFactory + codexFactory kernel_import re-pins in their own commits
target_release: next additive contract bundle (contract-v1.25 — the kernel content bytes change)
Status: ratified
Ratified by: Brett's direction on 2026-07-30 ("lets do kernel-publication decision") — the governed publication decision recorded as pending at the contract-v1.22 cut (add-domain-ontology-layer 8.5 evidence) and re-verified mechanically clean at every review round since
---

# Publish the xFactory Semantic Kernel

## Why

`xf/core` has shipped DRAFT through three bundles by explicit decision:
the ratified bootstrap scenario allowed pending adoption while the
kernel proved itself, and publication was recorded as "a governed
decision for a future cut". Every publication condition is now met and
machine-checked: all 25 concepts and 9 relations carry evidenced
adoption with two independent resolvable adopters each (deduped by
identity), two real domain packages import the kernel by exact digest
(MedxFactory, codexFactory — no longer fixtures), the six-lens reviewer
verified draft→published validates clean in place, and the release
machinery the publication rides was hardened to APPROVED three times
over (per-term publication gate, faithful adoption-carrying rewrite,
superseded-born snapshots). A draft kernel under two real published-line
consumers is now the anomaly.

## What Changes

- The per-term steward act: all 34 kernel terms move `draft → published`
  (openxFactory maintainers as the accountable council; F18's gate makes
  this explicit, never implicit).
- The governed release: `ontology-release.py` publishes `xf/core`
  0.1.0 → 1.0.0 (additive; same compatibility line), writing the release
  record naming `openxfactory-maintainers` and the superseded-born
  retained snapshots for 0.1.0 and 1.0.0. The rewrite carries the
  kernel's package-level adoption block — the exact F21 scenario.
- Downstream pins re-point at the new kernel digest: the fixture corpus
  and pilots regenerate, the gateway and omnigent examples restamp, and
  MedxFactory + codexFactory re-pin `kernel_import` (one-line manifest
  changes, packages unchanged).
- contract-v1.25 registers the published kernel bytes (three refreshed
  digests) with the CHANGELOG entry as the durable decision record.

## Impact

- Affected specs: none — publication EXERCISES the promoted
  `xfactory-semantic-kernel` and `domain-ontology-lifecycle`
  requirements; no requirement changes.
- Affected bytes: kernel content lifecycle lines + manifest; every
  kernel-digest pin downstream; contract-v1.25.
- NOT affected: kernel meaning (no term's label, definition, parents,
  domain, or range changes — `effective_version`s stay), the authority
  firewall, domain package content, and all retained history.
