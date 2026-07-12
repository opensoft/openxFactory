# Planning Contract: Hermes Runtime Validator CLI

Status: draft

## Entrypoint

```text
scripts/validate-hermes-runtime-contracts.py [OPTIONS]
```

## Options

| Option | Meaning |
|---|---|
| `--strict` | Treat every warning and required evidence omission as failure |
| `--case <case-id>` | Execute one indexed fixture and its dependencies |
| `--phase structural|semantic|all` | Select non-database validation phase |
| `--json` | Emit deterministic machine-readable findings/result |
| `--require-candidate` | Require complete pre-commit candidate metadata/inventory but not remote commit/tag evidence |
| `--require-realization` | Require realized release metadata and external Git evidence |
| `--repo <path>` | Optional alternate repo root for clean-clone verification; must resolve to a Git root |
| `--domain-repo <canonical-repo>=<checkout>` | Repeatable mapping to a Git checkout/bare mirror containing exact regression objects |
| `--domain-repo-root <path>` | Root containing canonical repository mirrors resolved by the regression inventory |
| `--handoff-receipt <path>` | Validate the external Hermes Gate receipt before OpenSpec task 5 acceptance |
| `--consumer-repo <canonical-repo>=<checkout>` | Repeatable mapping for exact downstream receipt objects; Gate G0 requires `opensoft/xFactory-Hermes-Install` |
| `--consumer-repo-root <path>` | Root containing canonical consumer mirrors, using the same deterministic layout as domain mirrors |

## Exit Codes

| Code | Meaning |
|---:|---|
| `0` | All selected checks passed |
| `1` | Contract/conformance findings |
| `2` | Missing dependency, invalid harness, or unavailable required external evidence |

## Validation Phases

1. Contract-index membership and unique IDs/paths.
2. Strict YAML-to-JSON loading.
3. Draft 2020-12 meta-schema and offline `$ref` closure.
4. Indexed structural cases.
5. Pure semantic cases at fixture-supplied evaluation time.
6. Acceptance-map/OpenSpec/evidence parity.
7. Overlay and exact-Git-object pin validation.
8. Optional realization/release validation.

## Finding Shape

```yaml
code: HCS-TOPOLOGY-CUSTOMER-MIN
severity: error
case_id: topology-operational-zero-customers
path: layer_instances
message: operational topology requires at least one active Customer layer
```

Finding codes are stable fixture assertions. Human and JSON outputs sort by case, path, and code. A negative fixture passes only when its required primary code is present.

## Content Resolution

- Fixture resolver: reads only indexed regular files within the contract fixture root.
- Git resolver: reads exact commit/tree/blob objects through Git plumbing.
- Domain resolver: reads only inventory-declared `commit:path` objects from explicit repo mappings or a mirror cache. Under a root, canonical `owner/repo` resolves only to `<root>/<owner>/<repo>` or `<root>/<owner>/<repo>.git`; ambiguity, a missing exact object, or an unavailable authenticated fetch exits 2 and fails release.
- Consumer resolver: first requires receipt `consumer_repository` to equal `opensoft/xFactory-Hermes-Install`, then applies the same exact-object and deterministic-root rules. It independently reads the downstream closure packet plus every recorded manifest/checker/runtime-binding/evidence path from the receipt's exact landed commit; receipt claims are never accepted from working-tree bytes alone. The wrong-product fixture using `FarHeap/Hermes-Install` fails before any object lookup with `HGR-HANDOFF-CONSUMER-REPOSITORY`.
- Final release/pin evidence never trusts mutable working-tree bytes.
- Network `$ref` retrieval and unregistered file resolution are forbidden.
