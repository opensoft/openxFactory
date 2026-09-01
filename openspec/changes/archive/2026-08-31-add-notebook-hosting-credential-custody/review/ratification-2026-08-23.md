# Proposal Ratification: add-notebook-hosting-credential-custody

Status: ratified
Decision date: 2026-08-23
Ratifier: Brett Heap (repository owner) — in-session via question prompts
Ratified: 2026-08-23 by Brett Heap (repository owner) — in-session via question prompts
Ratified baseline: this change as committed in the ratification commit
carrying this record (proposal.md, design.md, tasks.md, .openspec.yaml,
specs/credential-contracts/spec.md — 2 ADDED requirements,
specs/lifecycle-notebook-projection/spec.md — 1 ADDED requirement), validated
`--strict` and `--all --strict`.

## Decision

Brett ratified the change and, in the same read, ruled the one architectural
question it put to him. Two acts, recorded separately because they are not the
same act:

1. **THE RESIDENCY REDIRECT IS ACCEPTED.** The neutral obligations live in
   openxFactory; the LIVE binding instances land in the consuming installs as
   named successors. The repository's own rule holds — `contracts/manifest.yaml`
   records that *"openxFactory ships no instance records (they live in client
   installs, credential-contracts residency model)"*, and
   `docs/domain-factory-starter-pack.md` says the same from the other side. His
   original direction had asked for the concrete instances on the
   credential-contracts side; the packet flagged the conflict rather than
   resolving it silently, and this is his resolution of it. The residency model
   is NOT changed by this ratification.
2. **RATIFY.** The requirement set stands as it is at this record's commit.

The change carries `target_release: none` and moves no contract bytes. It
archives on its realization evidence per `release-realization`; this record
authorizes that realization, it does not perform it.

## The three flagged items, all before him at the read

The packet deliberately put three things to the ratifier rather than deciding
them quietly. All three were in view, and he ratified with them in view.

1. **The residency redirect** — ruled, see Decision item 1.
2. **The unpromoted-generalization sequencing.** These requirements presume the
   operated-identity generalization carried by `add-notebook-projection-identity`,
   which is RATIFIED but NOT YET PROMOTED: it promotes when that change archives
   on its migration evidence. Until then a reader of the promoted
   `credential-contracts` text sees only the credential-vault framing. Nothing
   breaks — the new requirements stand on their own terms — and no requirement
   is MODIFIED here precisely so that two active changes never hold two live
   deltas on one requirement text.
3. **The enforcement gap, admitted rather than papered over.** Per-system
   authority is NOT machine-provable today: the published
   `xfactory_credential_binding_template` requires only `[provider, secret_ref,
   owner, rotation_policy]` with optional `vault`, carries no consumer or
   access-identity field, and `scripts/validate-credential-contracts.py`
   compares no authorities — so two bindings naming the same vault principal
   validate cleanly. The invariant is held TODAY by review and by estate
   wiring. Making it provable means extending `contracts/schemas/`, which
   carries the full contract-release ritual, and is named as an owed successor
   (tasks §4.5) rather than folded in here.

## Pre-ratification review

A bot round ran on PR #282 before this read. Four findings, all verified
against the repository and all taken (commit `f2fd609d`).

- **Codex P1 — per-system bindings are not per-system containment.** The
  requirement had claimed, unconditionally, that separate bindings are
  independently revocable and that revoking one does not disturb the other. For
  a shared BEARER secret that overclaims: revocation stops FUTURE fetches only;
  it cannot un-disclose a password already fetched or end a session already
  established with it. Evicting a consumer that holds the secret requires
  ROTATION, which necessarily reaches every consumer. The requirement now scopes
  the guarantee to fetching, states the bearer-secret limit under its own
  heading, obliges an adopting change to record the shared rotation cost, and
  carries a scenario for it.
- **Codex — the invariant is not representable in the published shape.**
  Verified against schema lines 140-146 and the validator. Now stated in the
  requirement (its own scenario), in the Impact section, and as the named
  schema successor. This is flagged item 3 above.
- **Codex — the planned fixture would have failed this change's own gate.**
  `shared-secret-identity` fires whenever two bindings in one template share a
  `secret_ref`, and two consumers of one account password is exactly that
  shape. The packaged fixture is DECLINED with the reasoning recorded: distinct
  references would misrepresent the estate (there is one secret), and relaxing
  the rule would weaken a check that exists to keep the dispatch and content
  credentials apart.
- **Copilot — the record names the binding, not the secret.** Task 1.1 had
  asked the hosting record to carry the `secret_ref` while the requirement says
  it identifies the BINDING. Corrected, and the validator will refuse a
  `secret_ref` in the hosting record.

## Conscious-acceptance notes (Brett, at ratification)

1. **Custody is not automation, and the packet says so in four places.**
   Holding the password governs who may obtain it and proves who did; it does
   not make the sign-in unattended. `nlm` drives a browser with roughly
   20-minute sessions and Google may interpose 2FA or a device check at any
   time. Automated login remains future work gated on proving the flow.
2. **The eviction cost is shared and accepted.** Per-system bindings separate
   fetching, grants and audit; they cannot separate rotation. Evicting one
   consumer of the shared account credential reaches the other, and that is a
   property of the credential class rather than a defect in the bindings.
3. **A TOTP seed may itself need custody.** Whether the account will enforce a
   second factor is not yet known; the requirement covers the case by naming
   the whole credential set rather than the password alone.
4. **The `nlm` session profile is NOT a custody subject** and must not become
   one — it is refreshable session state, the class `credential-contracts`
   already refuses to distribute. This is what makes the no-shared-session rule
   independently required rather than merely preferred.
5. **No live secret was created, moved, or read** by authoring or ratifying
   this change. Placing the password into `kv-opensoft-xfactory-qa` is an
   operator's act under the landed rule, evidenced per `credential-contracts`.

## Next

Realization per tasks §1-§3 and §5 (the hosting record's custody block, the
validator rule, the two documentation surfaces), and then the successors this
thread now owes, each in its own lane: the live xFactory sync-lane binding in
the install's `credentials/` tree, the live openXdox binding in openXdox's own
lane, and the consumer/access-identity extension to the binding shape — which,
unlike everything in this change, carries the contract-release ritual.
