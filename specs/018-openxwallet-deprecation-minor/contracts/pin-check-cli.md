# Interface contract: `scripts/check-openxfactory-pin.py` output

The one external interface this feature changes. Consumers of this contract are
DomainxFactory estate runs (LedgerxFactory first, at P5a.2) that invoke the
pinned checker and read its stdout/stderr and exit code.

## Invocation (unchanged)

```
check-openxfactory-pin.py <repo_root> [--aggregation-root PATH]
```

## Exit codes (unchanged — FR-008)

| condition | exit |
|---|---|
| PASS | 0 |
| WARN (stale-behind pin) | 0 |
| **WARN (relocation notice)** — NEW | **0** |
| SKIP (not an aggregation checkout) | 0 |
| ERROR (divergent pin) | 1 |

The added notice cannot change an exit code. The implementation keeps the literal
expression `1 if verdict == ERROR else 0`, where `verdict` is still the value
`classify()` returned.

## Streams (unchanged rule, new line)

- The pin verdict line goes to **stderr** when it is `ERROR`, otherwise stdout.
- The relocation notice goes to **stdout** always — it is never an error.

## Output grammar

Line 1 is the existing pin verdict, byte-for-byte as today:

```
PASS: stack pin matches aggregation submodule pointer (abc123def456)
WARN: stack pin abc123def456 is stale-behind the aggregation submodule pointer def456abc123; refresh with: update stack.yaml xfactory.contract_ref to <full-sha> and contract_declared_at to today
ERROR: stack pin abc123def456 is not an ancestor of the aggregation submodule pointer def456abc123: the declared contract is off the submodule's history
SKIP: pin reconciliation skipped (not an aggregation checkout)
```

**NEW** — emitted after line 1, only when the pinned bundle carries relocating
rows:

```
WARN: the pinned openxFactory bundle <bundle> carries <N> relocating contract row(s); each artifact's canonical home is moving and it is removed at a later major bundle — read contracts/CHANGELOG.md at this pin for the removal version and the migration path:
  <artifact_id> -> <to> @ <tag>
  <artifact_id> -> <to> @ <tag>
  …
```

`<bundle>` is the pinned manifest's `contract_bundle_version`. Rows appear in
manifest order. One indented line per relocating artifact.

## Worked sample (the eight rows of this feature)

```
PASS: stack pin 5f3a91c8de77 matches aggregation submodule pointer (5f3a91c8de77)
WARN: the pinned openxFactory bundle contract-v1.46 carries 8 relocating contract row(s); each artifact's canonical home is moving and it is removed at a later major bundle — read contracts/CHANGELOG.md at this pin for the removal version and the migration path:
  openxwallet-record -> opensoft/openXwallet @ wallet-v1.1
  openxwallet-custody-registry-schema -> opensoft/openXwallet @ wallet-v1.1
  openxwallet-custody-registry -> opensoft/openXwallet @ wallet-v1.1
  openxwallet-grant -> opensoft/openXwallet @ wallet-v1.1
  openxwallet-grant-exercise -> opensoft/openXwallet @ wallet-v1.1
  openxwallet-distinct-holder-constraint -> opensoft/openXwallet @ wallet-v1.1
  openxwallet-subject-attestation -> opensoft/openXwallet @ wallet-v1.1
  openxwallet-agent-composition -> opensoft/openXwallet @ wallet-v1.1
```

Exit code: **0**.

## Silence conditions (no relocation line at all)

- The pinned manifest has no row carrying `relocating:`. This is the case for
  every bundle up to and including `contract-v1.45`.
- The pinned commit is not present in the local openxFactory checkout.
- `contracts/manifest.yaml` is absent at that commit.
- The manifest does not parse as YAML, or does not parse to a mapping.
- No aggregation root was resolved (the run already SKIPs and returns before the
  question is asked).

In every one of these the run behaves exactly as it does today.

## Composition with ERROR

An ERROR pin and a relocation notice are independent facts and both print:

```
ERROR: stack pin abc123def456 is not an ancestor of the aggregation submodule pointer def456abc123: the declared contract is off the submodule's history   [stderr]
WARN: the pinned openxFactory bundle contract-v1.46 carries 8 relocating contract row(s); …                                                               [stdout]
```

Exit code: **1** — the ERROR's, unchanged. The notice never substitutes for a
verdict and never suppresses one.

## Backward compatibility

A consumer that greps for `^PASS:` / `^WARN:` / `^ERROR:` on the FIRST line is
unaffected. A consumer that asserts total output equality against a bundle with
no relocating rows is unaffected. A consumer that asserts total output equality
while pinned to a bundle WITH relocating rows will see the new line — which is
the entire point of D5, and the reason P5a.2 adds the invocation deliberately
rather than inheriting it.

## What is NOT part of this contract

- `scripts/validate-domain-openxfactory-pins.py` emits nothing new (FR-011). It
  has no warning tier, so a relocation notice there would be an ERROR and would
  red every domain pinning this legal bundle.
- `scripts/validate-openxwallet.py` is not edited (FR-012). The withdrawn
  validator-warning reading stays withdrawn: LedgerxFactory runs it `--strict`,
  which reds on any warning, and openxFactory's own gate runs it WITHOUT
  `--strict`, so nothing required would surface it anyway.
