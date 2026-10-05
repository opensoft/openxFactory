# Contract: the finding's neutral shape

Status: draft

**Feature**: 038 · **Authority**: R2Q22 (a) (`#656` `6003486656`): openDox-spec
owns this shape as one of three schemas; openDox-code carries a digest-checked
copy. Boxes 14.6, 15.2, 15.7; answers R2Q10 (a), R2Q25 (a). **A PROPOSAL until
Brett rules the plan** (decisions N-3, N-13, OQ-H15-18, OQ-H15-19).

**Where it lands.** T040 authors it as a JSON Schema in openDox-spec, in that
repository's existing schema layout. T041 copies it into openDox-code with its
digest checked, and `opendox.health_contract` (the ONE contract module packs may
import, decision N-3) carries the matching constants. The `dox-v1.y` bundle
(T060) includes it.

## Shape

One finding is a JSON object. `health list --json` emits an array of them; a
pack emits them inside its one stdout document (`contracts/health-packs-manifest.md`).

| field | type | required | rule |
|---|---|---|---|
| `id` | string | yes | `^[a-z0-9-]+\.[a-z0-9-]+\.[0-9a-f]{16}$`: `<pack_id>.<family>.<h16>`, `<h16>` the first 16 hex of SHA-256 over `pack_id`, `kind`, `path` and `locator` joined by NUL. Set by the ENGINE; a pack's own `id` is ignored. A valid ref-name component (R2Q10 (a)) |
| `kind` | string | yes | the family, `^[a-z0-9-]+$` |
| `pack_id` | string | yes | `^[a-z0-9-]+$`; `opendox` for the product's own families (OQ-H15-19). Stamped by the engine (15.7) |
| `pack_version` | string | yes | the pack's declared version; for `opendox`, the installed version (OQ-H15-18). Stamped by the engine (15.7) |
| `path` | string | yes | corpus-relative, `/`-separated, no `..`; empty string for an install-level or pre-run finding |
| `locator` | object | yes | family-supplied position: `{"line_start": int, "line_end": int}` and/or `{"target": string}` (a link target as written). Never document text |
| `severity` | string | yes | `error` \| `warning` \| `info` |
| `resolution_class` | string | yes | `auto-fix` \| `assisted` \| `human-only` (14.6, spelled exactly) |
| `message` | string | yes | one line, written by the family from its own words and the locator; never quotes the document |
| `evidence` | object | no | locators only (R2Q25 (a)): paths, line spans, link targets as written, digests, a family's own `family_version`. Any string longer than 200 characters, or any key named `excerpt`, `text`, `content` or `quote`, is refused |
| `baseline_class` | string | no | set by the engine on store: `new` \| `pack-upgrade` \| `persistent` \| `unclassed` (R2Q12 (a); I-2) |
| `patch` | object | no | a pack's proposed patch (data-model.md § Patch); validated before any branch exists (15.2a) |

## Rules

- **Refusals.** The store refuses a finding without `pack_id` or `pack_version`
  (15.7). The engine refuses a pack finding whose `pack_id` is not the running
  pack's, whose `resolution_class` is outside the three, or whose `evidence`
  breaks the locator rule; each refusal is itself a finding against that pack
  (15.6).
- **Install-level findings** (`no-sandbox`, `no-default-branch`, a manifest
  entry that cannot be fetched, a pack that crashed or timed out) carry
  `pack_id` `opendox` or the entry's id, an empty `path`, and `human-only`.
- **The view renders `message` and labels as TEXT**, never HTML, and reads any
  passage it shows from git at render time.

## Example

```json
{"id": "opendox.broken-link.3c1f0e9a7b2d4c65", "kind": "broken-link",
 "pack_id": "opendox", "pack_version": "0.2.0", "path": "notes/plan.md",
 "locator": {"line_start": 12, "line_end": 12, "target": "../old/brief.md"},
 "severity": "warning", "resolution_class": "auto-fix",
 "message": "link target does not exist; a unique file of that name exists elsewhere",
 "evidence": {"candidate": "archive/brief.md", "family_version": "1"},
 "baseline_class": "new"}
```
