# Factory Origin Key — Mint Runbook

Status: ratified
Ratified by: add-cpc-clearing-boundary
Realizes: tasks 2.1–2.4 of `openspec/changes/add-cpc-clearing-boundary/tasks.md`,
  capability `factory-origin-identity`

The operator procedure for minting the ONE Ed25519 origin key an originating
repository holds, and for landing its public half in
[`governance/factory-identity/`](../governance/factory-identity/README.md).

**THIS IS THE ONLY GOVERNED DOCUMENT THAT NAMES THE SECRET.** The ratified
requirement forbids "a private key, a seed, a passphrase, a secret name
resolvable to key material, or any credential value" anywhere in the
factory-identity register family, so the environment-variable name is written
here and nowhere under `governance/factory-identity/` —
[`scripts/validate-factory-identity.py`](../scripts/validate-factory-identity.py)
refuses that tree if an environment-variable-shaped token naming key material
ever appears in it. That is a deliberate divergence from
`governance/review-authority/register.yaml`, which does name its seat secrets in
prose; the divergence is the ratified sentence, not an oversight.

---

## What is being minted, and what it is not

ONE Ed25519 key pair per ORIGINATING REPOSITORY. Its public half is registered
here; its private half exists only in that repository's own hosted packaging
environment. A signature under it evidences ONE fact and no other: **this sealed
bounded request came from that repository's own environment.**

It is **NOT** a review key, **NOT** a council seat key, and **NOT** a key that
decides anything. The origin act and the review or seat act are distinct acts
carried by distinct keys in distinct registers — and the enforceable half of that
distinctness is a checked rule: no `key_id`, decentralized identifier or
public-key fingerprint may appear in both register families. If a mint ever
reuses an existing key, the gate refuses and names the shared value.

**A refusal at READ TIME is NOT in force and must not be claimed.** The pinned
openXwallet reader indexes every wallet and grant record in a scanned tree into
one context, so an origin wallet in this sibling tree is still resolvable BY IT
as a review row's `wallet_ref`. Scoping that reader is an openXwallet dependency
(`add-cpc-clearing-boundary` tasks 5.1/5.2, OQ3). Until it lands, the
disjointness rule below is the WHOLE of the enforcement, and any document, gate
or report saying otherwise is refused by the capability's own scenario.

---

## Before you start

| | |
| --- | --- |
| Who | The responsible operator under the Human Escalation Contract (`docs/roles-and-authority.md:103-140`). Nobody else, and no agent. |
| Where | A HOST SHELL you control. Not a container an agent can read, not a governed repository working tree, not CI. |
| What you need | Python 3.12 with `cryptography` installed, and the openXwallet gitlink initialized (`git submodule update --init openXwallet`). |
| Time | Under ten minutes. The PR review is the long pole, not the ceremony. |

The private half must reach EXACTLY ONE destination and no other: the
originating repository's own hosted packaging environment. Not a governed
execution host, not a workstation clone, not a shared runner, not a bundle, not
a password manager, not a second repository. The ratified requirement refuses
each of those by name. **There is no backup copy.** If the key is lost, the
recovery is a fresh mint that SUPERSEDES the old row — which is cheap, and which
is why a backup copy is not worth its blast radius.

---

## Step 1 — Generate the seed, offline

```bash
python3 - <<'PY'
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base64, secrets
seed = secrets.token_bytes(32)
sk = Ed25519PrivateKey.from_private_bytes(seed)
pk = sk.public_key().public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw)
print("PRIVATE (paste into the CI secret, then close this terminal):")
print(seed.hex())
print()
print("PUBLIC (safe to publish):")
print(base64.urlsafe_b64encode(pk).decode().rstrip("="))
PY
```

**The encoding is 64 lowercase hex characters of the raw seed**, matching the
council seat keys minted 2026-08-28: the loader accepts hex OR unpadded
base64url of 32 bytes, and hex was chosen because its LENGTH ALONE disambiguates
it, which is the property that makes a mis-set secret fail by name rather than
by silent misbehaviour.

Do not write the private line to a file. Do not paste it into an agent session,
an issue, a chat, or a commit message. Nothing that reads this repository ever
needs it.

## Step 2 — Derive the three public values

The estate has ONE derivation path, and it is the pinned openXwallet reader's.
Do not compute these by hand, and do not use a second tool:

```bash
python3 scripts/validate-factory-identity.py --derive <PUBLIC-from-step-1>
```

It prints `did`, `key_fingerprint` and `public_key_multibase`, having
round-tripped every value back through the PINNED decoders before printing —
so a value it emits cannot disagree with the reader that will judge it. It
takes the PUBLIC half only; hand it a 64-hex seed and it refuses by shape.

The encodings, stated once so nobody re-derives them from memory:

| Value | Encoding |
| --- | --- |
| `public_key_multibase` | `z` + base58btc(`0xED 0x01` ‖ 32 raw bytes) — `did:key`'s own encoding |
| `did` | `did:key:` + that same multibase string |
| `key_fingerprint` | `"sha256:" + sha256(32 raw public bytes).hexdigest()` |
| `public_key` (mint record only) | canonical unpadded base64url, 43 characters |

## Step 3 — Store the private half, in exactly one place

Repository → Settings → Environments → **`worker-credentials`** → Environment
secrets → New secret:

- **Name:** `FACTORY_ORIGIN_SIGNING_KEY`
- **Value:** the 64 hex characters from step 1

**Why that name, and why there is no suffix.** The seat keys are
`COUNCIL_SEAT_SIGNING_KEY_<SEAT>` because a council has several seats. An
originating repository holds **exactly one** origin identity — the ratified
requirement says so, and a second concurrent row is refused — so a suffix would
imply a plurality the contract forbids, and the first person to add
`_PRIMARY` would be recording a fact the register cannot hold. The name is
scoped by the ENVIRONMENT it lives in, not by a suffix.

**Why the `worker-credentials` environment.** It is the environment class the
repository's own hosted jobs already run under, and the one the four seat
signing keys already occupy — so the custody determination is the same one
already attested for them: the key is readable in the holder's own execution
context, each use requires no authorization outside it, and a signature under it
evidences **the environment**. That is `holder_readable` exactly, whose registry
ceiling is authority tier `act`.

Then close the terminal from step 1.

## Step 4 — Paste the public halves into the register family

Replace every `FILL-IN-AT-MINT` sentinel. There are five, in two files:

| File | Field |
| --- | --- |
| `governance/factory-identity/wallets/<wallet>.yaml` | `key_reference.did` |
| | `key_reference.key_fingerprint` |
| | `key_reference.public_key_multibase` |
| `governance/factory-identity/attestations/custody-attest-<wallet>.yaml` | `attested_key_fingerprint` |
| | `verified_at` (the RFC3339 instant you performed step 3) |

If the mint happens on a later date than the register's drafted `issued_at`,
re-stamp **in the same commit**: the grant's `issued_at`, the grant's
`expires_at` (= `issued_at` + 90 days, never more), and the row's `expires_at`
**character-for-character equal** to the grant's. The reader compares them; two
expiries for one authority is one of them being wrong.

**Do not invent a plausible value to make a check pass.** A 43-character
base64url literal that is not a real key is worse than a sentinel, because it
merges — and every downstream reader will then treat a key nobody holds as the
repository's identity.

## Step 5 — Run the gate locally, before you push

```bash
git submodule update --init openXwallet
python3 scripts/verify-openxwallet-pin.py
python3 openXwallet/scripts/validate-openxwallet.py .
python3 scripts/validate-factory-identity.py .
python3 -m pytest tests/factory_identity/ -q
```

All four must be clean. The last one pins the sentinel count, so it goes green
exactly when the mint is complete and not before.

## Step 6 — Write the mint record, then open the PR

Land the record in the ORIGINATING repository — for codexFactory that is
`hermes/domain/factory-identity/records/<YYYY-MM-DD>-factory-origin-key-minted.md`,
beside the seat-key mint record it mirrors — and reference it from the PR.

The register PR is a change to a **permanently human-only surface**: it is never
landable by an autonomous or council-cleared approval path, and
`governance/factory-identity/` is entered BY NAME in codexFactory's
never-clearable floor
(`scripts/merge_master/openxfactory-review-authority-floor.yaml`) so that a
candidate touching it parks rather than clears.

---

## The mint record template

Mirrors `opensoft/codexFactory`
`hermes/domain/review-councils/records/2026-08-28-seat-signing-keys-minted.md`.

````markdown
# Record: the codexFactory origin signing key is minted and provisioned

Status: record
Qualifies: tasks 2.1–2.4 of openxFactory `add-cpc-clearing-boundary`
  (capability `factory-origin-identity`), and task 4.2 of the same packet's
  codexFactory realization.
Recorded: <YYYY-MM-DD>
Ruled by: Brett Heap, in session <YYYY-MM-DD> — "<the recorded word>".

## The obligation this discharges

<Which ratified requirement, and which exit was taken. Name what was NOT
changed as explicitly as what was: the seat keys are untouched, no key was
re-minted, no existing custody declaration moved.>

## What was minted

One Ed25519 key pair, the ORIGIN identity of `opensoft/codexFactory`. Exactly
one: the ratified requirement admits one origin identity per originating
repository, and a second concurrent row is refused.

| Repository | Key id | Public key (unpadded base64url, 32 raw bytes) | Key fingerprint |
| --- | --- | --- | --- |
| `opensoft/codexFactory` | `key-factory-codexfactory-0001` | `<43 chars>` | `sha256:<64 hex>` |

The fingerprint is the one spelling the estate computes everywhere —
`"sha256:" + sha256(raw 32-byte public key).hexdigest()` — and it RECOMPUTES
from the public key beside it, which is what
`scripts/validate-factory-identity.py` checks rather than trusts, through the
PINNED openXwallet decoder rather than a second implementation.

The `did` and `public_key_multibase` recorded in the wallet record are
`did:key`'s own encoding of that same public half: `z` + base58btc of the
ed25519 multicodec prefix and the 32 raw bytes.

## Where the private half is, and where it is not

The private half is a 32-byte Ed25519 seed, held ONLY as an encrypted GitHub
Actions secret in the `worker-credentials` environment of
`opensoft/codexFactory`, under the name `FACTORY_ORIGIN_SIGNING_KEY`.

There is no suffix because there is exactly one origin identity. There is no
second copy: not on a governed execution host, not on a workstation, not on a
shared runner, not in any bundle, not in a vault. No private half was written
to any git working tree, appeared in any log, or left the minting shell; the
minting terminal was closed and the shell history cleared.

**The encoding is 64 lowercase hex characters of the raw seed**, matching the
seat keys, because its length alone disambiguates it from a base64url public
half — the property that makes a mis-set secret fail by name.

## How the encoding was proven, not assumed

<The round trip you actually performed: the public half loaded back through the
PINNED decoder, the fingerprint recomputed from it, the `did` compared against
`did:key:` + the multibase, and the whole family read by
`scripts/validate-factory-identity.py` with zero findings. State what verified
what, and against which pinned revision.>

## What this does NOT discharge

<Name the remaining work in order, and say precisely what still refuses until
it lands. At minimum, as of this realization:>

1. this record (done) — the mint, the public half, the custody attestation;
2. the `digest_subject` tranche widening
   (`contracts/signed-execution-chain/digest-construction.schema.yaml`): the
   enumeration is CLOSED at seventeen members and none of them is a request,
   return or bundle manifest, so an origin signature over the manifest has no
   admitted subject yet and the requirement reports UNREALIZABLE rather than
   satisfied (tasks 2.9);
3. the register PROJECTION path to the clearing workflow — OQ1 names four
   shapes and chooses none. Until one is settled, revocation propagates no
   faster than the view a consumer holds, and the register's declared
   `revocation_staleness_bound` is the honest ceiling on that lag. **Origin
   revocation at the moment of clearing is NOT in force and must not be
   claimed** (tasks 3.5);
4. the openXwallet reader scoping (tasks 5.1/5.2) — until it lands, the
   read-time refusal of an origin key presented for a review act is NOT in
   force, and the checked disjointness rule is the whole of the enforcement;
5. the hosted packaging workflow that actually signs with this key
   (tasks 4.1–4.3).
````

---

## Rotation, and revocation

**Rotation SUPERSEDES a row; it never adds a second.** A new mint produces a new
wallet, a new grant and a NEW row whose `supersedes:` names the row it replaces;
the old row moves to `superseded` and stays in the file. A revoked row NEVER
returns to `active` — resumption is a new row, always.

**Expiry is the propagation mechanism that actually works today.** An origin
grant runs 90 days and no longer, unconditionally, because no projection path
exists that could revoke it at the moment of clearing. Renewal is a governed
re-issuance on this same human-only surface, not an edit to the expiry line.
