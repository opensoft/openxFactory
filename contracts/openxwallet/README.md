# openxWallet Contract Family

Status: ratified
Ratified by: add-openxwallet (approved Brett Heap 2026-08-07; registered in
`contracts/manifest.yaml` + `contracts/CHANGELOG.md` at `contract-v1.31`,
per [Contract Versioning Policy](../../docs/contract-versioning-policy.md))
Kind: reference
Repository context: openxFactory owns the neutral capability; the first
consumer is LedgerxFactory's posting segregation-of-duties control

The neutral contract for **what a wallet is, what authority it can carry, and
what a signature under it actually proves** — holder-class agnostic, and
optional for every domain.

A wallet is a signing key anchored to a decentralized identifier and held by a
HOLDER, where a holder is any subject class the family recognises: a person, a
practitioner, an organisation, or an agent. Everything agent-specific lives in
the sibling family
[`contracts/openxwallet-agent-profile/`](../openxwallet-agent-profile/README.md),
which is a NEW capability over this core rather than a modification of it.
Patient and practitioner profiles arrive the same way, each gated on a consumer
of its own — the seam is structural, not a promise.

## Why this exists

Two domains needed wallets and neither had one, which is the moment to define
one view rather than the moment after two have diverged.

LedgerxFactory made posting agent-executed on 2026-08-06 and lost the
platform-level refusal that had been holding up "agents never post". The
replacement control — refuse a post when the requesting agent created the
transaction — proved unbuildable, because every agent reaches Business Central
through ONE application user: the agent that created purchase invoice
`LXRP0002` and the agent that posted it are the same `userSecurityId`.
Segregation of duties is not a control anyone is declining to enforce; it is a
property the platform cannot see. These contracts are what make it visible.

MedxFactory had already ruled on the shape from the other side, and its two
ratified constraints are adopted here as a core requirement rather than worked
around: a wallet address is not identity proof, and custody stays
wallet-neutral and reconstructable with no wallet available.

## The three decisions this family carries

**Grants are the primitive.** Authority travels as attenuated capability
grants, never as access to a key. A raw key can be neither expired nor
revoked, and a shared key destroys attribution. The job envelope's
`approval_policy` survives as a legal scope VOCABULARY rather than a parallel
mechanism, so an agent's authority and a job's approval posture are stated
once instead of twice and kept in agreement.

**The core is holder-class agnostic.** Composition hashing is meaningful for
an agent and meaningless for a patient. A core carrying it would force every
future profile to explain why it ignores half the contract.

**Key custody is DECLARED from a closed set and CAPS authority.** Neither
mandated — which would have stalled every consumer, there being no key
infrastructure in the stack — nor unstated, which would let a key readable by
its own execution context masquerade as proof the HOLDER acted. That is worse
than having no control, because the audit record would then assert something
false.

## The custody enumeration, and the collapse it refuses

What each custody model EVIDENCES is contract content, not an implementation
detail. The closed set lives in
[`openxwallet-custody.registry.yaml`](openxwallet-custody.registry.yaml).

| model | key readable by holder's execution context | per-use authorization outside it | evidences | ceiling |
|---|---|---|---|---|
| `holder_readable` | yes | no | environment | `act` |
| `isolated_invocable` | no | no | environment | `act` |
| `isolated_per_use_authorized` | no | yes | **holder** | `act_unsupervised` |

`evidences` is **derived, never asserted**:

```
evidences = holder  iff  (not readable) and per_use_authorization
           environment otherwise
```

The validator enforces the derivation, refuses a top-of-ladder ceiling that
does not evidence the holder — keyed on RANK rather than on the tier's name,
so a registry cannot disable the rule by renaming its top tier — and refuses
any model evidencing only the environment sitting at or above a model that
evidences the holder.
Collapsing the two cases is therefore structurally impossible rather than
merely discouraged — which matters, because a collapsed enumeration is the one
failure mode that would otherwise validate cleanly.

Isolation without per-use authorization contains the KEY (it cannot be
exfiltrated and replayed off-platform) but does not attribute the ACT: a
compromised environment still signs anything the holder could. Saying that
plainly, rather than promoting it, is what keeps the contract honest.

Two deliberate NON-members are recorded in the registry so they are not
re-litigated as oversights: asserted (keyless) identity, and shared
credentials.

## The record kinds

| Kind | Purpose |
|---|---|
| `xfactory_wallet_record` | A holder, a key REFERENCE, a declared custody model. Never key material. |
| `xfactory_wallet_custody_registry` | The closed custody set, what each member evidences, and the ordered authority ladder it caps. |
| `xfactory_wallet_grant` | Audience, scope, expiry, optional parent. Derivation narrows monotonically. |
| `xfactory_wallet_grant_exercise` | Proof of possession, key attribution, revocation checked at use, distinct-holder evaluation. |
| `xfactory_wallet_distinct_holder_constraint` | Two acts on one object that must be exercised by different holders. Opt-in. |
| `xfactory_wallet_subject_attestation` | The optional wallet reference a subject may carry — attestation, never identity. |

## What this family deliberately does not do

No runtime, wallet infrastructure, issuance service, key storage, or signing
implementation. Contracts and schemas only. It creates no key, credential or
wallet, modifies no existing capability, and obliges no domain to adopt
wallets — a domain operating with none is conformant and is refused by
nothing.

It also cannot check that a DECLARED custody model is the REAL one. Custody
declaration is what keeps this honest, and it works only if consumers declare
truthfully; a validator can check that a model is declared and that authority
does not exceed it, and cannot check that the declaration is true.

Nor does it recompute expiry from timestamps at exercise: revocation and
expiry are enforced through the grant's recorded `state` (an exercise
permitted against a grant whose state is `expired` or `revoked` is refused,
and the revocation check is required at use), but an exercise whose
`occurred_at` falls after its grant's `expires_at` while the grant still
reads `active` is a state-keeping failure in the issuing system, not one this
validator adjudicates.

The `openxVault` boundary Brett set on 2026-07-16 is preserved rather than
re-litigated: the vault owns custody and its gate CONSUMES these grants; this
family owns identity, keys and authority.

## Validation

```sh
python3 scripts/validate-openxwallet.py                 # family self-test
python3 scripts/validate-openxwallet.py <repo-path>     # repo mode
python3 scripts/validate-openxwallet.py --strict         # warnings are errors
```

The self-test runs the packaged corpus under
[`examples/`](examples/): every positive must pass every rule, and every file
under [`examples/negative/`](examples/negative/) must FAIL for the reason
declared in its own first lines. Each negative carries
`# expected_failure:`, an optional `# expected_failure_detail:` pin, and a
required `# requirement:` attribution — and the validator fails if any
requirement of either capability has no negative confirmation, so a
requirement cannot quietly lose its probe.

Coverage closure is PER REQUIREMENT, not per rule: every requirement carries
at least one probe, and the recorded red-proof shows every finding code the
corpus exercises is load-bearing — but not every enforced rule has a fixture
of its own.
