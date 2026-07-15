# Agent Wallets and Drift-Triggered Certification — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Every AI agent carries its own wallet (DID + signing key);
qualification at a certified level grants scoped autonomous authority as
a verifiable credential bound to the agent's quantified identity — and
when the agent changes beyond tolerance, it is no longer the certified
agent and must recertify.

Origin: 2026-07-15 session with Brett, extending the patient/practitioner
wallet model in
[git-native-record-vault.md](git-native-record-vault.md) to AI agents.
Brainstorm-stage: free-form, nothing normative.

## The principle (Brett, 2026-07-15)

Certify agents that pass qualifications at a level; the cert conveys
autonomous authority. But once certified, the agent must be QUANTIFIED —
"if it changes by x%, it needs to recertify, since we no longer know if
this is the same agent and will act in the same way."

The stack already practices this at small scale: the document-cataloger's
prompt-contract version bump (v1→v3, 2026-07-14/15) automatically
invalidated every prior classification — a judgment by prompt-v1 is not
the same classifier's judgment. This generalizes that invalidation rule
from an agent's OUTPUTS to its AUTHORITY.

## Agent identity: two change triggers

An agent = model version + prompt contract + tool manifest + policy
version + parameters (+ retrieval corpus where applicable).

1. **Declared change — binary, automatic decert.** Any component of the
   configuration hash changes → the certified identity no longer exists →
   authority revoked instantly; recert required. No percentage involved.
   Enforcement hook already exists: Omnigent readiness heartbeats attest
   `worker_version`/`profile_versions`/`policy_version` — extend to a
   full config hash; every gate refuses an agent whose attested hash
   differs from its certified hash.
2. **Measured drift — continuous, the "x%".** For what cannot be hashed
   meaningfully (a provider silently updating a pinned model; dependency
   drift), the agent periodically re-runs a fixed CERTIFICATION BATTERY
   of golden tasks. Drift = score/behavior delta beyond a statistical
   tolerance band (agents are stochastic; the band absorbs run-to-run
   noise, the threshold catches genuine change). Beyond the band →
   decert → recert.

## The credential

A verifiable credential in the agent's wallet: issuer = the certification
gate (first issuance is a human ratify-style Hermes gate), subject =
agent DID, claims = qualification level + autonomous-authority scope +
certified configuration hash + battery scores + expiry.

Authority scope already has a home: the neutral job envelope's
`approval_policy` field (`report_only_v1` today). Certification levels ARE
the set of approval policies an agent may run under — level 1 =
report-only (every current lane), higher levels = bounded autonomy.

## Composition with the wallet architecture

- Agents sign their work with their wallet key: today's `Co-Authored-By`
  trailer upgrades to cryptographic commit signing per agent identity.
- Agent access to vault records rides the same possession-bound,
  time-boxed capability grants as practitioners.
- Delegation chains respect certification: a practitioner (or another
  agent) can delegate to an agent only up to the agent's certified
  level; every link signed; a decert breaks the chain immediately.
- License-revocation propagation (the vault doc's OQ) applies verbatim:
  a decertified agent's unexpired grants die with the cert.

## Open questions

- **Battery design**: who authors the golden tasks per lane, how large a
  battery is statistically sufficient, and are batteries themselves
  versioned/certified artifacts (they must be — a changed battery
  changes what "same agent" means)?
- **Tolerance calibration**: what drift band per qualification level?
  Higher authority should presumably mean tighter bands.
- **Recert cadence**: periodic (nightly with doc-health?) vs
  event-driven (on any dependency/pin movement) vs both.
- **Cert authority**: is issuance always a human gate, or can a
  sufficiently-certified certifier agent issue lower-level certs
  (auditable chain)?
- **Provider opacity**: hosted model endpoints can change beneath a
  pinned ID; is detectable-drift-via-battery sufficient, or do high
  levels require locally-pinned weights?

## Exit

Likely exits as an openxFactory contract change (agent-identity /
certification-credential / battery schemas + gate verification rules)
composing with the roles-authority-model and credential-contracts
capabilities, plus omnigent-install adoption (config-hash attestation in
heartbeats). Cross-references: the wallet and grant sections of
[git-native-record-vault.md](git-native-record-vault.md); the
model-worker prompt-version invalidation precedent in the archived
add-document-cataloging change.
