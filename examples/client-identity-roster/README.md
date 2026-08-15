# Client-Identity-Roster Examples

Status: ratified
Ratified by: add-client-identity-roster (registered in
`contracts/manifest.yaml` + `contracts/CHANGELOG.md` at `contract-v1.32`,
per [Contract Versioning Policy](../../docs/contract-versioning-policy.md))
Kind: reference
Repository context: openxFactory owns the neutral contract; the first
publishers are OpsxFactory and LedgerxFactory, which hold standing identities
inside paying clients' Microsoft tenants

Reference examples for the client-identity-roster contract family
(`contracts/schemas/xfactory-client-identity-roster.schema.yaml`). These are
static reference material, not runtime state — see `../README.md` for the
placement policy this directory follows. REAL fragments never live here: a
domain publishes its own at
`credentials/client-identity-roster/<client_ref>.yaml` in its own repository,
one file per (client, domain) pair and a DIRECT CHILD of that directory.

The canonical validator is `scripts/validate-client-identity-roster.py`. Every
run self-tests this directory before it scans anything: each `*.example.yaml`
must validate CLEAN, and each file under `negative/` must FAIL for its
REGISTERED reason. Five failure modes are themselves errors — a registered
probe with no file, a file with no registration, a negative that passes, a
negative that fails for the WRONG code, and a negative whose code fires without
its pinned detail.

## These examples are TRUTHFUL WORKED CASES

Every provider fact in every positive example is transcribed from a record in
the OpsxFactory or LedgerxFactory evidence chain and cited inline by repository,
path and commit — permission identifiers verbatim, tenant and object GUIDs,
achieved scopes, admission acts, verification timestamps.

That is a rule and not a habit. A packaged example is an instantiation template
a domain copies, so a packaged example may not assert a provider fact its author
cannot cite; an uncitable claim escalates rather than being invented. The rule
has already bitten once and held: the originally mandated FOURTH packaged case —
a provider-forced multi-surface reader — was RELOCATED to a synthetic
representability fixture in `tests/client-identity-roster/fixtures/` after the
precondition check established that no in-vocabulary permission reaching both
`business_central` and `exchange` is citable anywhere in the estate. That
fixture carries a dated synthetic header saying exactly that, and it is the ONE
deliberately hypothetical artifact in this feature.

## Layout

```text
client-identity-roster/
├── README.md                                             # this index
├── client-identity-roster-farheap-opsx.example.yaml      # client farheap / domain opsxfactory:
│                                                         #   the BUSINESS CENTRAL WORKED CASE —
│                                                         #   one identity, TWO admission acts on
│                                                         #   ONE surface, union effective reach,
│                                                         #   declared excess; plus the `planned`
│                                                         #   entry (Production, no application
│                                                         #   user) with its UNVERIFIED act
├── client-identity-roster-farheap-ledgerx.example.yaml   # the SAME client held by a SECOND
│                                                         #   domain: the GENUINE DUTY PAIR
│                                                         #   (poster / provisioner) and the
│                                                         #   GENUINE PER-UNIT PAIR (provisioner
│                                                         #   at two governed companies) — the
│                                                         #   killed-flaw positives
├── client-identity-roster-lxtest-ledgerx.example.yaml    # the RETIRED entry, and the corpus's
│                                                         #   only packaged `exchange` instance:
│                                                         #   Mail.Read bounded to one mailbox by
│                                                         #   an application access policy, torn
│                                                         #   down 2026-07-26, record KEPT
├── client-identity-drift-finding.example.yaml            # the second kind: an OPEN finding whose
│                                                         #   identity_ref is the tuple OBJECT and
│                                                         #   which therefore carries no
│                                                         #   disposition_ref
└── negative/                                             # one violation per file, each registered
                                                          #   by filename in the validator's
                                                          #   expectations table
```

## Schema → example map

| Kind | Valid example(s) | Negative example(s) |
| --- | --- | --- |
| `xfactory_client_identity_roster` | `client-identity-roster-farheap-opsx`, `client-identity-roster-farheap-ledgerx`, `client-identity-roster-lxtest-ledgerx` | every file in `negative/` except the three `drift-finding-*` ones |
| `xfactory_client_identity_drift_finding` | `client-identity-drift-finding.example` | `drift-finding-without-roster-value`, `drift-finding-without-observed-value`, `drift-finding-status-out-of-vocabulary` |

## Named cases

- **Two admission acts, ONE surface** — the Business Central entry carries the
  provider-enforced per-environment application user in Sandbox1 AND the
  admin-center Entra-app authorization, which has no scope selector at all. Four
  admin-consented permissions held for SIX DAYS still returned `401` until the
  second act landed, so neither act admits alone; they are jointly required keys
  to one surface, not two surfaces. Effective reach is their UNION.
- **Forced breadth declared is conformant** — the tenant-wide second act
  declares `exceeds_governed_unit: true`, and the entry therefore carries a
  `declared_excess` with its provider reason, bounding mechanism, gate
  obligation and enforcement test. `negative/scope-exceeds-unit-undeclared.yaml`
  is the same shape with the declaration omitted, and is refused.
- **A name may not understate achieved authority** — `opsx-farheap-bc-observer`
  achieves `mutate`, because Business Central exposes no read-only admin-center
  role. It passes only because the excess is declared;
  `negative/name-understates-achieved-authority.yaml` is the uncured form, and
  there the only remedy is to rename the identity.
- **Consent is not admission** — an entry declaring provider consent and no
  admission act is refused (`negative/consent-recorded-as-access.yaml`), and an
  act claiming a verification it cannot evidence is refused as counted access
  (`negative/unverified-act-counted-as-access.yaml`).
- **Per-unit and duty-separated identities are PERMITTED** — the LedgerxFactory
  fragment holds both pairs at zero findings while
  `negative/alias-pair-observationally-identical.yaml` is refused in the same
  run. A rule broad enough to catch all three fails that discrimination, which
  is the whole point of keeping the three together.
- **A `planned` entry is legal and indefinite** — never reported as missing or
  incomplete; nothing in this family derives an expected entry set from any
  inventory.
- **A `retired` entry RETAINS its record** — and is EXEMPT from the consent
  instrument's in-force test, because the ratified cascade runs withdrawal or
  termination through to retirement. That exemption is repo-context and is
  measured against fixture repositories, not here.
- **Recording drift mutates nothing** — the drift example changes no identity,
  no permission and no admission; while `open` it refuses grant issuance for its
  identity, which is our lever and not the client's.

## Validating locally

```bash
# Self-test this directory (positives clean, negatives refused for their
# registered reason) and scan a checkout for real fragments:
python3 scripts/validate-client-identity-roster.py <repo-path>
```

`scripts/validate-credential-contracts.py` skips these files with a notice.
That is EXPECTED and blessed, not a coverage gap: the canonical roster
validator claims this family's path.
