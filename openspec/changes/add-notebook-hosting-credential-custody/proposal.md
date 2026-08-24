---
code_surface: openxFactory (`examples/notebook-projection-hosting.yaml` — a `custody:` block carrying a BY-REFERENCE pointer to the governed binding, never secret material; `scripts/validate-notebook-projection-hosting.py` — the rule enforcing that, including the refusal of anything secret-shaped in the record; `docs/lifecycle-notebook-projection.md` §12 and `docs/notebook-projection-migration-runbook.md` — the custody story and its honest reach; optionally one packaged reference fixture under `examples/credential-contracts/`, which forces the self-test count in `tests/credential_contracts/` to be updated with it). The LIVE binding instances are NOT an openxFactory surface — see "Where the bindings live". No `contracts/` artifact is added or changed.
target_release: none — this change moves no contract bytes. The credential binding-template shape it uses is already published (`xfactory_credential_binding_template`, `contracts/schemas/xfactory-credential-contracts.schema.yaml`), so no schema changes, no manifest row, no bundle. Realization lands as spec text plus the hosting-record and documentation surfaces named above; the bundle stays at `contract-v1.40`.
---

# Proposal: add-notebook-hosting-credential-custody

Status: draft
Proposed: 2026-08-23, the same day `add-notebook-projection-identity` was
ratified and realized. This is its follow-up, authored on Brett Heap's
direction; ratification is a separate act, still PENDING.

THE REALIZATION RUNS POST-RATIFICATION. No hosting-record, validator, doc or
example edit lands with this proposal itself, and **no live secret is created,
moved, or read by authoring it**. Putting the actual password into the vault is
an operator's act under the landed rule, evidenced per `credential-contracts`.

## Why

`add-notebook-projection-identity` made the projection's hosting identity a
declared fact and named Opensoft's account: `xFactor001@opensoft.one`. It
deliberately said nothing about the account's CREDENTIAL. That leaves the
governance half-built — the account is named, and the password authenticating
it lives wherever the person who created it put it.

Brett ruled the remedy on 2026-08-23, verbatim: *"this is a xFactor001 login.
and we want to store the password in a kv and have xFactory and openXdox login
with its own authority."* Three refinements followed, all his:

1. **The vault** is the EXISTING QA-estate Azure Key Vault already serving the
   hermes/openXdox QA lanes — `kv-opensoft-xfactory-qa`, the vault the openXdox
   dispatch binding names — holding the account password and any 2FA/TOTP
   secret the account needs.
2. **The authority shape** is ONE Google account whose secret each consuming
   system reaches through its OWN governed binding: its own vault access
   identity, its own grant, its own rotation visibility, its own audit trail.
   No shared ambient session; no system borrowing the other's authority.
3. **The sequencing** is parallel: the migration proceeds now on Brett's
   interactive login, and this custody change lands beside it.

The gap this closes is not theoretical. An account whose password has no
custody cannot be operated by anyone but its creator, which is the personal-
account failure the declared-identity change existed to retire — moved one
level down rather than removed.

## What Changes

**Custody becomes a positive obligation, not just a prohibition.** The ratified
generalization already says contract artifacts SHALL NOT hard-code an operated
identity's credential. That is a prohibition; it does not require custody to
exist. This change adds the positive half: an operated identity's credential is
held in a governed store and reached only by reference, and an identity with no
declared custody is not governed — it is undocumented.

**Custody covers the whole credential set.** Where the platform enforces a
second factor, its seed is part of what must be held. A password in a vault
beside a TOTP seed on someone's phone is a single point of failure wearing
governance.

**One identity, per-system authority.** Where more than one system authenticates
as the same operated identity, each reaches it through its own binding, its own
access identity, its own grant, its own rotation visibility and its own audit
trail. One identity may be shared; one authority may not. This is Brett's ruling
2, and it turns out to be independently required by a rule this family already
promotes — see the design's session-class finding.

**The hosting record names its custody, by reference only.** The record that
already names the account gains a pointer to the binding that resolves its
credential — sufficient to find it through the governed path, insufficient to
obtain it without one. No password, recovery code, TOTP seed, session cookie or
exported profile in the record, the repository, or any projection artifact. A
self-hosted declaration owes no custody: no operator exists to bear it.

## Where the bindings live — and why not here

The ruling's route asked for the concrete binding instances on the
`credential-contracts` side. **This repository's own residency model forbids
that**, and the constraint is stated in the manifest rather than inferred:
`contracts/manifest.yaml` records that *"openxFactory ships no instance records
(they live in client installs, credential-contracts residency model)"*, and
`docs/domain-factory-starter-pack.md` says the same from the other side —
*"Bindings belong to client or tenant deployments, not the domain repo. Domain
repos provide templates only."*

So the split this change proposes:

- **openxFactory** carries the neutral obligations (the three requirements
  below) and, optionally, ONE packaged reference fixture under
  `examples/credential-contracts/` showing the two-consuming-system shape.
  Everything under `examples/` there is a fixture, not a live record — the one
  existing binding example is literally named `*.binding-template.example.yaml`.
- **The live xFactory sync-lane binding** is declared where the estate is
  governed: the install's `credentials/` tree, the same place the deployment
  handoff already puts `cir-opensoft-qa-dox-dispatch-minter`.
- **The live openXdox binding** is its own successor packet in its own lane, as
  the ruling already directs — openXdox pins openxFactory's contracts and
  declares its own binding.

This is the same ownership test that kept the hosting record out of
`contracts/`, applied to the layer below it, and it is FLAGGED for the
ratification read rather than decided quietly: the ruling asked for the
instances here, and the repository's rule says they go there.

## Impact

- **Affected specs.** `credential-contracts` — 2 ADDED requirements (governed
  custody reached by reference; per-consuming-system authority).
  `lifecycle-notebook-projection` — 1 ADDED requirement (the hosting record
  declares its custody, by reference only).
- **No requirement is MODIFIED**, deliberately. The generalization these hang
  on is carried by `add-notebook-projection-identity`'s own MODIFIED delta,
  which is ratified but NOT YET PROMOTED — it promotes when that change
  archives on its migration evidence. Modifying the same requirement from a
  second active change would put two live deltas on one requirement text.
- **Affected code, at realization**: the hosting record's `custody:` block, the
  validator rule enforcing by-reference-only, and the two documentation
  surfaces. A packaged example under `examples/credential-contracts/` would
  additionally require updating the self-test count asserted in
  `tests/credential_contracts/`.
- **`contracts/` is untouched.** The binding-template shape is already
  published; nothing here changes a schema, a manifest row or a digest, and no
  bundle is cut. `target_release: none`.
- **No live secret is created, moved, or read by this change.**

## Honest gaps, recorded rather than assumed away

- **Custody is not automation.** Storing the password does NOT make the
  projection's sign-in unattended. `nlm` authenticates through a browser flow
  with roughly 20-minute sessions; `--cdp-url` exists, and Google may demand
  2FA or a device check at any time. Automated login is FUTURE work, gated on
  proving the flow — the same discipline as the manual approval lane and the
  §12 platform correction. A custody record that implies unattended access the
  install does not have is worse than none.
- **A TOTP seed may itself need custody**, and whether the account will enforce
  2FA is not yet known. The requirement covers the case by naming the whole
  credential set rather than the password alone, but the concrete seed does not
  exist yet.
- **The session profile is NOT a custody subject.** See the design: this family
  already refuses to distribute refreshable session state, and the `nlm`
  profile is exactly that class.
- **The generalization this builds on is unpromoted** until
  `add-notebook-projection-identity` archives, which waits on the migration.
