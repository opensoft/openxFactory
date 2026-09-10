# Kaspa Execution Surface Decision Study — Brainstorm

Status: brainstorm
Kind: report
Summary: V1 should enforce usage policy off chain through a provider-neutral gateway and use direct Kaspa L1 payload commitments as the operational witness, deferring Toccata, Kasplex, and Igra execution until explicit maturity gates pass.
Topics: usage-controlled-evidence-chain, kaspa-execution-surface, kaspa, toccata, kasplex, igra
Repository context: openxFactory neutral chain boundary and future promotion criteria
Captured: 2026-08-29

## Possible feats

- **Provider-neutral policy gateway contract** — define the authorization,
  receipt, and adapter seam without binding consumers to one chain runtime.
- **Kaspa execution experiments** — evaluate Toccata and EVM layers behind
  non-production promotion gates without moving enforcement out of the gateway.

## Focus

This study resolves the v1 meaning of "Kaspa contract." A public chain can
validate its own state transitions, but it cannot directly prevent an EMR,
FHIR server, or KMS from releasing data through credentials that bypass it.
The component controlling those provider calls must remain the enforcement
point.

## Decision recommendation

```text
provider-neutral policy contract/service
  -> authenticate actor and workload
  -> evaluate purpose, scope, consent, role, expiry, and revocation
  -> issue a short-lived capability
  -> enforce the EMR/FHIR or KMS call
  -> emit signed allow/deny/use/revoke evidence
  -> anchor an opaque keyed commitment directly to Kaspa L1
  -> include every event in the daily OTS/Bitcoin checkpoint
```

Kaspa is the primary operational witness, not the authorization engine. The
policy contract is provider-neutral application logic with versioned inputs,
outputs, and receipts. Direct provider credentials must not permit callers to
bypass the gateway.

The Kaspa payload should contain only a domain separator, sequence, policy or
receipt root, and high-entropy keyed commitment. It must not contain PHI,
patient or payer identifiers, EMR resource IDs, policy details, stable public
subjects, or reusable authorization tokens.

## Surface comparison

| Surface | V1 disposition | Reason |
| --- | --- | --- |
| Direct Kaspa L1 payload | **Adopt as witness** | Simple, fast, sufficient for compact opaque commitments, and avoids a second execution trust boundary. |
| Toccata L1 covenants and ZK | **Experiment only** | Real UTXO programmability, but new script/compiler/ZK dependencies and still unable to call an external EMR or KMS directly. |
| Kasplex zkEVM | **Defer** | Adds L2, bridge, upgrade, indexing, and admin-control assumptions without removing the enforcing gateway. |
| Igra EVM | **Defer** | Adds adapter, execution, wallet-worker, asynchronous L1 broadcast, RPC, and operator dependencies without direct provider enforcement. |
| Off-chain provider-neutral policy | **Adopt as enforcement** | Lowest PHI exposure, immediate future-use revocation, provider adapters, review/rollback, and direct control of EMR/KMS access. |

## Proof and failure rules

- Record Kaspa submission and confirmation as separate states.
- Capture the serialized transaction, accepting DAG reference, inclusion proof,
  node/version, confirmation state, and local signed receipt at anchor time.
- Treat ordinary-node pruning as a proof-retention obligation, not a later
  lookup strategy.
- Keep network publication asynchronous to otherwise authorized care and
  business operations; use `anchor_pending`, durable retry, and escalation.
- Fail closed when required policy, consent, identity, or KMS authority cannot
  be evaluated; chain publication failure alone is not an authorization result.
- Upgrade OpenTimestamps evidence only after Bitcoin confirmation; a submitted
  OTS proof is not yet Bitcoin durability.

## Promotion gates

Toccata may become a policy-adjacent settlement or registry layer only after at
least twelve months of stable post-activation operation, independent audits of
the covenant, builder, compiler, and any ZK path, reproducible test vectors,
documented upgrade/migration, no undisclosed mutable admin key, and successful
verification from retained post-pruning artifacts. The gateway remains the
EMR/KMS enforcement point.

Kasplex or Igra may become a non-custodial policy registry only after twelve to
twenty-four months of public operating history, complete bridge/sequencer/
upgrade/emergency-key documentation, independent end-to-end audits, replayable
archive data, demonstrated censorship recovery and failover, and no single
operator or key able to silently rewrite policy state.

Kaspa must not become the sole long-horizon durability witness until
independent archival operators and external auditors can reproduce old
transactions and proofs from retained artifacts without one explorer or
service. Bitcoin/OpenTimestamps remains the second witness through any later
promotion period.

## Interfaces and boundaries

openxFactory owns neutral evidence and adapter contracts, not deployable
provider credentials or medical policy. Product owners enforce their own
resource operations. A future runtime/install owner operates gateways, Kaspa
clients, archival evidence, OpenTimestamps, KMS integration, and monitoring.

## Sources to verify during proposal

- [Kaspa transaction payload](https://docs.kaspa.org/integrate/transaction-payload)
- [Kaspa accepted transactions and pruning](https://docs.kaspa.org/integrate/accepted-transactions)
- [Kaspa Toccata developer guide](https://docs.kaspa.org/toccata)
- [Kaspa covenants](https://docs.kaspa.org/programmability/covenants)
- [Kaspa inline ZK](https://docs.kaspa.org/toccata/inline-zk)
- [Kasplex documentation](https://docs.kasplex.org/)
- [Igra Labs repositories](https://github.com/IgraLabs)
- [OpenTimestamps](https://opentimestamps.org/)
- [HL7 FHIR security](https://www.hl7.org/fhir/security.html)

## Alternatives and tensions

- On-chain execution offers shared state and independent validation, but adds
  public metadata and runtime trust without controlling provider credentials.
- Off-chain policy is conventional, but its integrity depends on versioned
  releases, protected signing, complete audit, and mandatory gateway routing.

## Open questions

- Which repository owns the deployable gateway and chain runtime?
- What exact Kaspa confirmation policy changes `submitted` to `confirmed`?
- Which non-production Toccata experiment would test value without PHI or
  production authority?

## Relationships

The neutral artifacts are explored in
[Anchor Kernel](usage-controlled-evidence-chain-anchor-kernel.md). Witness
timing is explored in
[Dual-Witness Cadence](usage-controlled-evidence-chain-dual-witness-cadence.md).
Their lifecycle is described in
[Synthesis: Witness Lifecycle](usage-controlled-evidence-chain-synthesis-witness-lifecycle.md).
