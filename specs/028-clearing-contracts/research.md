# Research: contracts/clearing

**Feature**: 028-clearing-contracts | **Date**: 2026-09-03

Every finding below was MEASURED at this branch's tip (`origin/main` @ `6a39d2ab`),
not remembered. Where a number is quoted, the command that produced it is named.

## R1 — Which additive minor does this realization allocate?

**Decision**: `contract-v3.3`.

**Rationale**. `docs/contract-versioning-policy.md` § *Version Identity*: *"A
proposed change MUST NOT reserve a minor number before merge order is known."*
So the number is read at THIS tip, and the packet's own front matter is stale by
design — it recorded `contract-v2.5` at authoring time in September 1st's tree.

Measured here:

- `contracts/manifest.yaml:3` declares `contract_bundle_version: contract-v3.2`.
- `contracts/releases/` holds inventories through `contract-v3.2.digests.yaml`.
- `git ls-remote --tags origin` publishes tags through `contract-v3.2`.
- No open pull request cuts a bundle (`gh pr list --state open`, 10 open PRs,
  none a cut).

**The two cuts the packet said were ahead of it have resolved.** The
`add-chain-attestation` realization landed and was CARRIED at `contract-v3.0`
(CHANGELOG line 305: *"add-chain-attestation tranche two — eight new schemas …
PR #556, squash 518c670b"*). The `add-chain-anchoring` realization has NOT
landed — no `contract-v*` entry names it, and the only open chain-anchoring work
is proposal #548. So neither claim stands ahead of this one now, and the next
available additive minor is `contract-v3.3`.

**The class is ADDITIVE.** A new contract family; no existing schema changes
shape, no required field is added to an existing record, and no consumer pinned
at `contract-v3.2` becomes non-conformant. The one edit to an existing schema —
`digest-construction.schema.yaml` — ADDS an enum member (see R4), which widens
what validates and narrows nothing.

**Alternatives considered**: reserving a number in the plan (refused by the
policy verbatim); deferring registration to a separate cut PR, as
`contract-v3.0`/`v3.1`/`v3.2` were cut. The separate-cut shape is the estate's
recent habit, but the ratified `tasks.md` §6.8 puts registration IN this
realization ("Register in `contracts/manifest.yaml` and `contracts/CHANGELOG.md`
at the next additive bundle cut"), so registration lands here. **The annotated
TAG does not.** Bundle Realization Order step 5 publishes the tag at the exact
LANDED commit after `verify-commit` passes there; publishing it against an
unmerged branch head is what made `contract-v3.1` defective. The tag is
therefore named as a post-merge act in the CHANGELOG entry and the PR body.

## R2 — Is the existing `contracts/schemas/dispatch-record.schema.yaml` this ledger?

**Decision**: No. Build `contracts/clearing/dispatch-record.schema.yaml` as a new
file. Do not move, rename, or extend the existing one.

**Rationale**. The existing file is `kind: dispatch_record`, `$id:
"dispatch-record.schema.yaml"`, and its own description names its owner: *"One
record per dispatch-junction decision (add-capability-steward … Canonical
validator: scripts/validate-capability-steward.py)"*. Its required members are
`family_match`, `capability_ref`, `effect_class`, `path` (`crystallized|ai|dual`),
`fallback_cause`, `postconditions`, `overhead`. It answers *which execution path
served a capability request*. The clearing ledger answers *what was cleared to a
governed execution host, and what was refused*. They share an English word.

Merging them would put two capabilities' vocabularies into one shape — the exact
defect `add-clearing-dispatch-boundary`'s "NO SECOND VOCABULARY" section exists
to prevent, running in the opposite direction. Renaming the capability-steward
file would break a shipped `$id` and a registered manifest row for no gain.

**Mitigation for the name collision**: the new schema's description names the
other file explicitly, so a reader who greps `dispatch-record` lands on the
distinction rather than on a coincidence.

## R3 — How does the closed register ship?

**Decision**: schema + instance, as `permitted-operations.schema.yaml` +
`permitted-operations.registry.yaml`, mirroring
`contracts/trust-anchor/chain-custody-registry.schema.yaml` +
`contracts/trust-anchor/trust-anchor-chain-custody.registry.yaml`.

**Rationale**. That pair IS the `openxwallet-custody` convention the proposal
cites: a `.schema.yaml` declaring `registry_id` (a `const`), `registry_version`
and a member array, and a `.registry.yaml` instance carrying the closed set, with
the CANONICAL VALIDATOR enforcing what the schema cannot — in trust-anchor's case
a derivation (`evidences` from two booleans) and a cross-registry mapping. Here
the validator-side rule is CLOSURE: the ratified member set is a frozen constant
in the validator, and an instance member outside it is refused by name.

The manifest registers the instance with `type: registry` (the trust-anchor row
`trust-anchor-chain-custody-registry` is the precedent) and each schema with
`type: schema`.

**Honesty about the mechanism**: the register, the validator and the tests share
a repository with the changes they police, so one diff can edit both sides. This
is the same limit the ratified L4 guard requires be STATED rather than
overclaimed, and the family README states it in those terms: the refusal is a
TRIPWIRE that makes an addition visible and costly, backed by review, not an
unforgeable refusal.

## R4 — Where does the manifest digest's SUBJECT come from?

**Decision**: add ONE member, `sealed_bundle_manifest`, to
`contracts/signed-execution-chain/digest-construction.schema.yaml`'s
`$defs/digest_subject` enum AND to `scripts/signed_execution_chain/canonical.py`'s
`SUBJECTS` frozenset. Define no construction.

**Rationale**. `add-cpc-clearing-boundary`'s MODIFIED requirement is explicit:
the manifest digest and the origin signature over it *"SHALL use the estate's
canonical JSON construction `xfc-jcs-sha256-1`, which requires the manifest to be
admitted as a SUBJECT of that construction's closed `digest_subject` enumeration
— a tranche widening of SUBJECTS, never a second construction … Until that
subject exists, this requirement is UNREALIZABLE as written."* The chain's own
schema header agrees: *"A LATER TRANCHE ADDS NO SECOND RULE. Any digest a later
tranche introduces is computed under this construction, with its subject added to
the enumeration below."*

Both places move because both are the enumeration: the schema is the contract,
and `canonical.SUBJECTS` is the reader's frozen copy whose own comment says *"The
enumeration is the contract's; it is repeated here as a frozen set the validator
checks against."* Widening one and not the other would leave the reader refusing
a subject the contract admits.

**Not added**: `sealed_return`, which `add-cpc-clearing-boundary` `tasks.md` §2.9
names in the same breath. Nothing in this realization computes a digest over a
sealed return — the return path belongs to the finalizer successor — and an enum
member with no shipped consumer is a widening no shape exercises. Recorded here
so the successor's author finds the reason rather than the omission.

**Per-file hashes stay OUT of the construction.** The same MODIFIED requirement:
*"PER-FILE CONTENT HASHES ARE NOT JSON VALUES: they SHALL be plain
algorithm-tagged SHA-256 over the file's BYTES."* The manifest schema types them
as `^sha256:[0-9a-f]{64}$` with no `construction`/`subject` members, and the
validator refuses a per-file hash carrying a construction tag as a category
error.

## R5 — How does the validator reuse existing code rather than re-deriving?

**Decision**: three imports, no reimplementation, and a REFUSAL rather than a
fallback for each.

| need | reused from | why not local |
|---|---|---|
| `xfc-jcs-sha256-1` serialization + digest | `scripts/signed_execution_chain/canonical.py` — `canonical.digest(value)`, `canonical.CONSTRUCTION`, `canonical.SUBJECTS` | one construction, one implementation; the module is family-agnostic and already has known-answer vector tests in `tests/signed_execution_chain/test_digest_construction.py` |
| Ed25519 signature verification | `scripts/signed_execution_chain/ed25519.py` — `verify(public_key, message, signature)` | stdlib-only, small-order-point checked, already the estate's verifier; the pinned wallet reader does NOT verify signatures |
| public-key decoding + fingerprint | the PINNED `openXwallet/scripts/validate-openxwallet.py` — `decode_public_key_multibase`, `fingerprint_of_public_key`, loaded by `importlib.util.spec_from_file_location` | `scripts/validate-factory-identity.py` establishes this precedent verbatim: *"a local reimplementation of base58btc or of the fingerprint spelling would be the second implementation this file exists to prevent"*; the validator REFUSES with a `git submodule update --init openXwallet` instruction when the gitlink is absent |

The import shape is the one already in the tree
(`scripts/validate-signed-execution-chain.py:132-137`):

```python
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.signed_execution_chain import canonical, ed25519  # noqa: E402
```

`.github/workflows/pytest-suite.yml` already runs `git submodule update --init
openXwallet` before the suite, so `tests/clearing/` may depend on the pinned
reader without introducing a SKIP — which matters, because that workflow pins
`EXPECT_SKIPPED: "21"` EXACTLY while `MIN_SELECTED`/`MIN_PASSED` are floors that
only rise. New tests are therefore free; new skips are not.

## R6 — House conventions this family must satisfy

Measured from the newest families (`signed-execution-chain` @ `contract-v2.5`,
`trust-anchor` @ `contract-v1.37`, `factory-identity` @ #610):

- **Finding format**: `ERROR [code] message` / `WARN  [code] message` / `note  message`
  from a `Findings` dataclass. Codes are kebab-case and family-scoped
  (`clearing-*`), matching `factory-identity-*`. Record-INTERNAL closed
  enumerations (a refusal GROUND carried in a record's own field) are snake_case
  — `unregistered_operation`, `unknown_lane_selector` — because those are
  contract values, not validator findings. Both spellings already coexist and the
  distinction is deliberate.
- **CLI**: `argparse`, optional positional `path` (omit to self-test only),
  `--strict` promoting warnings to errors. Exit `0` clean, `1` findings,
  `2` harness failure.
- **Self-test**: the packaged corpus is adjudicated on every run. Each negative
  fixture carries a `# expected_failure: <code>` header (optionally
  `# expected_failure_detail: <substring>`), must fail for THAT code, and every
  code in the validator's closed refusal set must be probed by at least one
  fixture — `clearing-refusal-code-without-probe` otherwise.
- **Examples**: `contracts/<family>/examples/*.example.yaml` and
  `contracts/<family>/examples/negative/*.yaml`. (The older root-level
  `examples/<family>/` layout is not used by any family added since
  `identity-brokering`.)
- **Schema headers**: `schema_version`, `kind`, `name`, `$schema`, `$id`
  (absolute, `https://xforge.us/schemas/openxfactory/<family>/v1/<file>`),
  `contract_id`, `contract_schema_version`, `title`, `description`.
- **Manifest rows**: `id`, `path`, `source_path`, `type` (`schema`|`registry`),
  `schema_version`, `sha256`, `compatibility: canonical_openxfactory_contract`,
  `adapter_owner: openxFactory`, `consumption_rule` (folded prose). The
  validator, README and examples corpus get NO rows — they are content-addressed
  by commit, the precedent every family since openxWallet follows.
- **Release inventory**: `contracts/releases/<tag>.digests.yaml` is built by
  `python3 scripts/validate-contract-release.py build --tag contract-v3.3
  --output contracts/releases/contract-v3.3.digests.yaml`. Its membership is
  CLOSED over the release surface (Hermes runtime family, named validators,
  auxiliary members including `contracts/manifest.yaml`, `CHANGELOG.md`,
  `README.md`, and modified normative docs) — a NEW neutral family is
  deliberately NOT a member, exactly as `signed-execution-chain` was not at
  `contract-v2.5`. Its identity travels by manifest-row `sha256`.
- **Per-family digest test**: `tests/<family>/test_manifest_row_digests.py`,
  closed in BOTH directions — every expected row is registered, and every
  `*.schema.yaml` on disk carries a row — plus a per-row recomputation. The
  estate-wide `tests/manifest_digests/` sweep independently recomputes every row.
- **CI gate**: a job whose ID IS the required-check token, with NO `name:` key
  (a display name silently de-advises the gate), and a POSITIVE assertion step
  that greps the log for proof-of-work notes as well as for the absence of
  findings — because a green check that walked nothing is a vacuous pass.

## R7 — How is a fixture key written so nothing looks like real key material?

**Decision**: two distinct techniques, one per purpose.

1. **Where only a public value is needed** (a register row that must not verify,
   a wallet whose key is never used to check a signature): derive it from a
   LABELLED sha256 digest, the way `tests/factory_identity/test_validator.py`
   does — *"the keys these tests use are derived from labelled sha256 digests, so
   a reader can see at a glance that nobody holds a private half."* A digest-derived
   value has no known private half by construction.
2. **Where a signature must actually VERIFY** (the packaged positive manifest,
   and the origin-signature verification test): generate an EPHEMERAL keypair
   once, sign the canonical bytes, and commit the PUBLIC half and the SIGNATURE
   only. The private half is never written to disk in the repository. This is the
   `signed-execution-chain` corpus's own practice — its packaged chain examples
   carry `did:key:z…` public halves and signatures its self-test genuinely
   verifies — and a public key is not a secret.

Neither technique writes a PEM private block, a JWK with a `d` member, or a bare
43-character base64url literal presented as a secret. There is no `.gitleaks.toml`
in this repository (checked: `find . -iname '*gitleaks*'` returns nothing, and no
workflow invokes it), so the discipline here is the repository's own: the pinned
wallet reader's `check_no_key_material` refuses private-key-shaped content in
governed trees, and the fixture register this family packages lives under
`contracts/clearing/examples/`, not under `governance/`, so it cannot be mistaken
for a live identity.

## R8 — What does this realization NOT do, and where is that recorded?

Carried from the ratified `code_surface` paragraph into `tasks.md`'s own
out-of-scope section and the family README: the factory-side packaging
realization (`realize-factory-bundle-packaging`), the CODING operation, the
hosted finalizer, any runner/group/label/host/credential, the `deliberation`
register member (codexFactory #165, a LATER governed change), the L4 guard and
L5 attestation IMPLEMENTATIONS in `opensoft/xFactory`, and any spec delta.
