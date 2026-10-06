# Contract: the finding's neutral shape

Status: draft

**Feature**: 038 · **Authority**: R2Q22 (a) (`#656` `6003486656`): openDox-spec
owns this shape as one of three schemas; openDox-code carries a digest-checked
copy. Boxes 14.5, 14.6, 15.2, 15.7; answers R2Q10 (a), R2Q25 (a). **RULED with
the plan** (`#656` `6013547504`, every decision as recommended: N-3, N-13,
OQ-H15-18, OQ-H15-19). Review round 1 made the id position-independent (ADV-07)
and bounded `message` (ADV-27); its re-check settled id collisions (§ The id
rule).

**Where it lands.** T040 authors it as a JSON Schema in openDox-spec, in that
repository's existing schema layout. T060 moves the openDox root's spec pin to it
and cuts the bundle. T041 copies it into openDox-code at the commit the root pins,
in the existing copy record (`src/opendox/contracts/copies.yaml`), and
`opendox.health_contract` (the ONE contract module packs may import, N-3) carries
the matching constants. The finding shape is a copy the engine reads, not a kind
the validator validates (tier 3's N-15).

## Shape

One finding is a JSON object. A family or pack produces it with every field
below that it supplies; the engine stamps the rest. `health list --json` emits an
array of them, with at least the fields 14.5 declares (`id`, `resolution_class`,
`path`, `severity`, `evidence`, `pack_id`, `pack_version`), and WITHOUT
`identity`, which is engine-internal (its row below).

| field | type | required | rule |
|---|---|---|---|
| `id` | string | yes | `^[a-z0-9-]+\.[a-z0-9-]+\.[0-9a-f]{16}$`: `<pack_id>.<kind>.<h16>`. Set by the ENGINE; a pack's own value is ignored. A valid ref-name component (R2Q10 (a)) |
| `kind` | string | yes | the family, `^[a-z0-9-]+$` |
| `pack_id` | string | yes | `^[a-z0-9-]+$`; `opendox` for the product's own families (OQ-H15-19). Stamped by the engine from the manifest entry (15.7) |
| `pack_version` | string | yes | the manifest entry's version; for `opendox`, the installed version (OQ-H15-18). Stamped by the engine (15.7) |
| `path` | string | yes | corpus-relative, `/`-separated, no `..`; empty string for an install-level or pre-run finding |
| `identity` | object | yes, in a family's or pack's output | the POSITION-INDEPENDENT key the family supplies (R2Q10 (a)'s "locator the family supplies", read as a key that survives edits elsewhere): a link target as written, a pair of paths, a heading key. Never a line number, never document text beyond such a key. ENGINE-INTERNAL: the engine hashes it into `id` at run time and neither stores nor emits it, so `list --json`, the HTTP response and the store carry `id` alone (R2Q25 (a); Copilot's review of `2076f24b`; data-model.md § Finding) |
| `locator` | object | no | DISPLAY ONLY, outside the id: `{"line_start": int, "line_end": int}` and/or `{"target": string}` |
| `severity` | string | yes | `error` \| `warning` \| `info` |
| `resolution_class` | string | yes | `auto-fix` \| `assisted` \| `human-only` (14.6, spelled exactly) |
| `message` | string | yes | one line, at most 200 characters, written by the family from its own words; never document text (ADV-27) |
| `evidence` | object | yes; the engine sets `{}` when a family or pack supplies none, so every emitted finding carries it (14.5; FR-011; Copilot's review of `3f807204`) | locators only (R2Q25 (a)): paths, line spans, link targets as written, digests, a family's own `family_version`, a refused patch's `refused_patch` and `reason` (15.2a). Any string longer than 200 characters, or any key named `excerpt`, `text`, `content` or `quote`, is refused |
| `baseline_class` | string | no | set by the engine: `new` \| `pack-upgrade` \| `persistent` (R2Q12 (a)); there is no fourth value (I-2 (a), ruled) |

## The id rule (ADV-07, a conforming refinement of R2Q10 (a))

```text
key  = canonical JSON, sorted keys, no whitespace, UTF-8, of
       {"identity": <identity>, "kind": <kind>, "pack_id": <pack_id>, "path": <path>}
h16  = first 16 hex digits of sha256(key)
id   = pack_id + "." + kind + "." + h16
```

An edit ABOVE a finding moves its `locator` and leaves its `id`; an exception keyed
by that id keeps suppressing it (requirement 15).

**Engine-authored findings have engine-owned identity keys**, so they too satisfy
the schema and keep one id across runs:
- an install-level or pre-run finding (no live sandbox, a fetch or digest
  failure, a refused manifest entry, a pack that crashed, timed out, hit a bound
  or returned refused output): `{"category": <the failure's category>, "entry":
  <the manifest entry's id, or "" for none>}`;
- the collision finding below: `{"collided_id": <the colliding id>}`;
- the re-raise of an uncited disappearance (data-model.md § Baseline classes):
  `{"disappeared_id": <the original's id>}`, with `pack_id` `opendox`, `kind`
  `uncited-disappearance`, `path` the original's, `human-only`, and the
  original's id and the baseline run in `evidence`. It has its own id, never
  the original's, and it is never itself measured as a disappearance, so it is
  raised in one run only (Copilot's review of `67d6f28b`).
T041 fixes the categories with the id rule, and T056's tests hold each id
stable across two runs (Copilot's review of `f9cc2d02`).

**A collision is a finding against its producer.** If two findings in one run
have the same id (the same `pack_id`, `kind`, `path` and identity key, or a
16-digit hash collision), NEITHER is stored, as itself or as a duplicate. The
engine records ONE finding against the family or pack that produced them
instead: `pack_id` that producer's (`opendox` for a built-in family, the
manifest entry's id for a pack), `kind` `identity-collision`, `path` the
colliding findings' path when they share one and the empty string when they do
not (a hash collision across paths), `human-only`, with the colliding id, the
count and every colliding path in `evidence`. A family or pack must supply an
identity key that tells its findings apart; the engine never truncates the id
further or disambiguates it by position. The ENGINE detects collisions, over
the whole run, built-in families and packs alike, before anything is stored
(T046 owns it and tests it; Copilot's review of `8cee8007`).

**An accepted limit: a hash collision ACROSS runs is not detected.** Two
different identities whose ids share the 16 hex digits in DIFFERENT runs read
as one finding to the baseline and to an exception. The id's 16-digit form is
the ruled one (R2Q10 (a), a ref-name component; N-13), and nothing outside the
id is stored that could tell them apart (`identity` is engine-internal, R2Q25
(a)). By chance the odds are about n²/2⁶⁵ per corpus, about 3 in a trillion
for 10,000 findings; a deliberate collision needs about 2³² SHA-256
evaluations over crafted document text, and it can only mislabel a class or
suppress one finding, never land anything (every repair still lands through
`land`). Widening the id would change the ruled shape, so it is the holder's to
raise with Brett (Copilot's review of `6f073ed2`).

## Rules

- **Refusals.** The store refuses a finding without `pack_id` or `pack_version`
  (15.7). The engine refuses a pack finding whose `resolution_class` is outside
  the three, whose `message` or `evidence` breaks the bounds above, or that
  declares a baseline or landing rule; each refusal is itself a finding against
  that pack (15.5, 15.6). Two findings with one id are such a finding too
  (§ The id rule).
- **Install-level findings** (`no-sandbox`, a manifest entry that cannot be
  fetched or whose digest differs, a pack that crashed or timed out) carry
  `pack_id` `opendox` or the entry's id, an empty `path`, and `human-only`.
- **The view renders `message` and labels as TEXT**, never HTML, and reads any
  passage it shows from git at render time (R2Q25 (a)).

## Example

The engine's internal object for one finding, AFTER stamping: `id`,
`pack_id`, `pack_version` and `baseline_class` are the engine's, and a family
or pack supplies the rest, `identity` included (a pack's own `id`, if any, is
ignored). `list --json` emits the same object without `identity`:

```json
{"id": "opendox.broken-link.3c1f0e9a7b2d4c65", "kind": "broken-link",
 "pack_id": "opendox", "pack_version": "0.2.0", "path": "notes/plan.md",
 "identity": {"target": "../old/brief.md"},
 "locator": {"line_start": 12, "line_end": 12},
 "severity": "warning", "resolution_class": "auto-fix",
 "message": "link target does not exist; a unique file of that name exists elsewhere",
 "evidence": {"candidate": "archive/brief.md", "family_version": "1"},
 "baseline_class": "new"}
```
