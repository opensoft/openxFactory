# Staged: Client credential escrow registry — one break-glass key, operator-side custody

Status: staged
Kind: architecture
Summary: Every managed xFactory domain install accumulates secrets whose
runtime source of truth is a per-install vault inside the client's estate.
The disaster the vault cannot survive is the destruction of that estate
itself. This topic defines a per-client, SOPS-encrypted credential escrow
registry held OPERATOR-side in the Client Hermes tree, recoverable with
exactly ONE break-glass key in the operator's password manager, and makes
escrow an explicit contract obligation of managed
(`opsxfactory_executed`) installs.
Topics: credentials, escrow, disaster-recovery, break-glass, sops, age, key-custody, client-hermes, opsxfactory-executed, client-infrastructure
Repository context: openxFactory owns the neutral contract (likely a delta to `credential-contracts`, plus the sanctioned repo-policy exception); the registry realization lands in the operator's Client Hermes tree (`xFactory-Hermes-Install` `config/clients/<client_ref>/credentials/`); install repos (e.g. `Omnigent-Install`) gain the escrow step in their secret-handling runbooks; OpsxFactory gains the managed-install escrow obligation in its workflow contracts
Staging ID: openxFactory:staging:client-credential-escrow-registry
Source: named by Brett Heap during track-1 QA secret-custody design, 2026-07-19 ("we need a way to keep only 1 key in 1pass for the break glass DR ... if this client install is managed by opsXfactory, then the client will assume that we have stored that kv in a creds registry for DR and have the DR key"); first concrete case: the opensoft self-client QA install's `kv-opensoft-xfactory-qa` (three secrets at its gate 3) and the Flux deploy key
Target capabilities: credential-contracts (MODIFIED — escrow registry + break-glass custody; possibly a sixth canonical record kind), client-infrastructure-liaison (touch — the client-assumption obligation)

The runtime pattern is settled per install: secrets live in a per-install
vault (Key Vault + CSI on the QA install), workloads read them there, git
carries only `vaultref://<org>/<scope>/<secret-name>` references. What has
no contract is the layer above: when the OPERATOR manages the install
(`opsxfactory_executed`), the client reasonably assumes the operator can
restore every credential after total loss of the client estate — Azure
tenant gone, client GitHub gone, vault gone with them. Today that
assumption is folklore. Meeting it ad hoc (values scattered across a
password manager) fails the operator's own constraint: the password
manager should hold exactly ONE thing per operator scope — the break-glass
key — not a growing pile of per-install values.

## Claims

1. **Escrow is a distinct layer, not a second runtime source.** The
   registry is written when a secret is created or rotated and read ONLY
   at break-glass. The runtime vault remains the sole source workloads
   consume. This distinction is what makes the earlier "no secrets in
   git" rulings and this topic compatible: the objection was to dual
   runtime sources that drift; escrow has one writer-moment and one
   reader-moment, both governed.

2. **age + SOPS, asymmetric on purpose.** Escrow files are SOPS-encrypted
   to an age recipient whose PUBLIC half is committed (`.sops.yaml`);
   the PRIVATE half is the break-glass key — exactly one per operator
   scope, held only in the operator's password manager (1Password),
   touched only during DR. Because encryption needs only the public
   recipient, routine escrow writes NEVER handle the break-glass key:
   day-to-day operation cannot weaken custody.

3. **Multi-recipient solves the client dimension.** SOPS encrypts each
   file to multiple recipients: the operator's master key always; a
   client-held recipient optionally (giving a `client_managed` client
   independent recovery power — a copy of the KEY, never custody of the
   REGISTRY). The operator's obligation stands regardless of whether the
   client adds a key.

4. **Custody rule: operator-side, outside the client estate.** The
   registry survives the exact event it exists for, so it may live in
   neither the client tenant nor the client's GitHub org. Its home is the
   operator's Client Hermes per-client tree —
   `config/clients/<client_ref>/credentials/` in
   `xFactory-Hermes-Install` — beside the governance records whose
   `vaultref://` strings it escrows. A dedicated tightly-ACLed registry
   repo is the named escalation if metadata sensitivity (client list,
   secret names) or readership of the Hermes tree demands it.

5. **Registry entries mirror `vaultref://` one-to-one, and store
   recoverable VALUES.** Where the runtime vault deliberately holds only
   a derivative (the QA dashboard's htpasswd HASH), the registry holds
   the recoverable value (the password). Recovery = any clone of the
   repo + the one key from the password manager; nothing else.

6. **Under `opsxfactory_executed`, escrow is an explicit, testable
   obligation.** The client assumption becomes contract: a managed
   install is not `ready` until every runtime-vault secret has a registry
   entry and the break-glass custody is attested. Escrow writing is part
   of the SAME gated step that sets the runtime secret (runbook step now;
   OpsxFactory workflow obligation once execution transfers), and a drift
   audit — every `vaultref://` has a registry entry — is checkable
   without decrypting anything.

7. **The repo no-secrets rules gain one narrow, sanctioned exception.**
   Install and Hermes repos rightly ban committed secret values; the
   contract must carve out SOPS-encrypted escrow blobs under the
   registry path explicitly, so the exception is policy, not precedent.

## Idea notes (pre-document, non-documented)

None recorded at staging.

## Conflicts

No conflicts recorded.

## Open questions

1. **Delta shape**: MODIFIED `credential-contracts` (a sixth canonical
   record kind, e.g. `xfactory_credential_escrow_registry`, plus custody
   requirements) versus a new ADDED capability that references it. Leans
   MODIFIED — escrow is meaningless apart from the credential records it
   protects.
2. **Master-key rotation and blast radius**: one key per operator scope
   spans every client registry. Rotation/compromise procedure (new
   recipient + `sops updatekeys` sweep + password-manager swap) needs to
   be a written, rehearsed runbook; is per-client keys-with-master-added
   ever warranted, or does the multi-recipient client key cover it?
3. **Break-glass authorization topology**: which role may retrieve the
   key (composed liaison role `integration_credential_steward`?), what
   evidence a break-glass use must leave, and whether post-break-glass
   rotation of every touched credential is mandatory (leans yes).
4. **Escalation criteria** for the dedicated registry repo (metadata
   sensitivity vs. Hermes-tree readership) — thresholds, not vibes.
5. **Scope boundary of MUST-escrow**: runtime-vault secrets clearly; what
   about install-plumbing credentials that live outside any vault (the
   QA Flux deploy key's private half currently exists only in a session
   scratchpad — the immediate motivating example)? Leans: anything whose
   loss blocks rebuild of the install MUST be escrowed.
6. **Validation**: registry structure + SOPS-metadata lint (correct
   recipients, no plaintext) as an openxFactory validator, so escrow
   health is checkable in CI without any decryption capability.

## Exit

One OpenSpec change in openxFactory (`code_surface`: openxFactory schema +
spec deltas; realizations tracked per repo — `xFactory-Hermes-Install`
client trees, install-repo runbook steps, OpsxFactory workflow
obligation). Realization evidence for archiving: the first escrowed
install (opensoft self-client QA) with every runtime-vault secret + the
Flux deploy key in the registry, drift audit green, and one REHEARSED
break-glass restore drill recorded (key from password manager + fresh
clone → values recovered).
