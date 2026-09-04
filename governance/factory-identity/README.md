# `governance/factory-identity/` — the sibling ORIGIN register

Status: ratified
Ratified by: add-cpc-clearing-boundary

The registered ORIGIN identity of each originating repository: the public half
of the ONE Ed25519 key whose signature evidences that a sealed bounded request
came from that repository's own hosted environment.

A **sibling** of `governance/review-authority/`, never an extension of it.
That register answers "may this holder decide about this repository's objects";
this one answers "did this request come from this repository". Provenance, not
decision authority — and no `key_id`, decentralized identifier or public-key
fingerprint may appear in both families.

| | |
| --- | --- |
| `register.yaml` | rows, and this register's OWN staleness bound and ceiling. Deliberately kindless: the reader is the shape. |
| `wallets/` | one wallet record per originating repository, `holder_class: organisation`, public key reference only |
| `grants/` | the grant conferring the `originate` act, its scope and its 90-day expiry |
| `attestations/` | the custody attestation that lifts the unattested cap; kindless, like its review-authority counterpart |

**Reader:** [`scripts/validate-factory-identity.py`](../../scripts/validate-factory-identity.py),
run inside the REQUIRED `wallet-validation` check. Without it this tree confers
nothing.

**To mint or rotate a key:**
[`docs/factory-origin-key-mint-runbook.md`](../../docs/factory-origin-key-mint-runbook.md).
That runbook is also the ONLY governed document that names the CI secret — the
ratified requirement forbids a secret name resolvable to key material anywhere
in THIS tree, and the reader refuses one.

**This is a permanently human-only surface.** No autonomous or council-cleared
approval path may ever land a change here; the directory is entered BY NAME in
codexFactory's never-clearable merge floor.
