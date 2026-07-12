# Contract release identity and stack-surface gaps

Status: brainstorm
Kind: note
Origin: codexFactory changes harden-conformance-gate and
realize-credential-contracts (both ratified 2026-07-12); seeds a future
openxFactory-side proposal.

Three upstream gaps surfaced while hardening codexFactory's conformance
gate; none are codexFactory-fixable:

- No `contract-v*` git tags exist, so the tag form of the domain pin
  (`contract_ref_type: tag`) is unsatisfiable; commit-SHA pinning is the
  only working form.
- Bundle version identity is inconsistent: at codexFactory's previous pin
  (3d51c3ed) `contracts/manifest.yaml` declared `contract-v1.3` while the
  same commit's `contracts/CHANGELOG.md` listed `contract-v1.6`; the
  manifest also omits the v1.4 (workflow schema) and v1.6 (credential
  schema) contract entries.
- The domain-stack schema has no `credentials:` manifest slot (OQ1 of
  realize-credential-contracts): a domain's credential surface cannot be
  declared in `stack.yaml` the way `schemas.required`/`workflows.required`
  are, so `validate-domain-factory.py` cannot require it and absence passes
  silently — exactly how codexFactory's credential gap stayed invisible.

Candidate shape: one proposal covering release tagging discipline
(annotated `contract-v*` tags + manifest/CHANGELOG consistency check) and a
`credentials.required` stack manifest slot; codexFactory's pin-drift WARN
threshold could then harden to ERROR on tagged releases (OQ3 of
harden-conformance-gate).
