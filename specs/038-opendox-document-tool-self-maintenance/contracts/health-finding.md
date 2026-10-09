# Contract: the finding's neutral shape

Status: draft

**Feature**: 038 · **Authority**: R2Q22 (a) (`#656` `6003486656`): openDox-spec
owns this shape as one of three schemas; openDox-code carries a digest-checked
copy. Boxes 14.5, 14.6, 15.2, 15.7; answers R2Q10 (a), R2Q25 (a). **RULED with
the plan** (`#656` `6013547504`, every decision as recommended: N-3, N-13,
OQ-H15-18, OQ-H15-19). Review round 1 made the id position-independent (ADV-07)
and bounded `message` (ADV-27); its re-check settled id collisions (§ The id
rule). The holder's ruling `6018624750` STORES and EMITS `identity`, as T040's
schema has it (its row below).

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
`path`, `severity`, `evidence`, `pack_id`, `pack_version`) and `identity`, which
is stored and emitted (its row below).

| field | type | required | rule |
|---|---|---|---|
| `id` | string | yes | `^[a-z0-9-]{1,40}\.[a-z0-9-]{1,40}\.[0-9a-f]{16}$`: `<pack_id>.<kind>.<h16>`, at most 98 characters, so `health-fix-<id>` is at most 109, far below a ref path component's 255-byte limit (Copilot's review of `55cc1334`). Set by the ENGINE; a pack's own value is ignored. A valid ref-name component (R2Q10 (a)) |
| `kind` | string | yes | the family, `^[a-z0-9-]{1,40}$` |
| `pack_id` | string | yes | `^[a-z0-9-]{1,40}$`; `opendox` for the product's own families (OQ-H15-19). Stamped by the engine from the manifest entry (15.7) |
| `pack_version` | string | yes | the manifest entry's version; for `opendox`, the installed version (OQ-H15-18). Stamped by the engine (15.7) |
| `path` | string | yes | corpus-relative, `/`-separated, no `..`; no C0 or C1 control character (U+0000 to U+001F, U+007F to U+009F) and no lone surrogate (U+D800 to U+DFFF), as the pinned finding schema's `path-is-corpus-relative` pattern has it (the holder, `6086098003` item 3); empty string for an install-level or pre-run finding |
| `identity` | object | yes, in a family's or pack's output | the POSITION-INDEPENDENT key the family supplies (R2Q10 (a)'s "locator the family supplies", read as a key that survives edits elsewhere): a link target as written, a pair of paths, a heading key. Never a line number, never document text beyond such a key. STORED AND EMITTED (the holder, `6018624750`, reversing the engine-internal refinement of Copilot's review of `2076f24b`): the engine hashes it into `id` AND stores it as a `health_findings` column, in canonical sorted-key JSON, and `list --json` and the HTTP response emit it. It is bounded as openDox-spec's finding schema (T040, landed) bounds it: no key named `excerpt`, `text`, `content` or `quote`, no number, every string at most 200 characters; a pathless finding's identity is `{category, entry}` and a collision's is `{collided_id}`. T041 also refuses U+0000 in any key or string, and bounds a pathless finding's `category` and `entry` further (§ Rules). The engine caps its serialized size, stricter than the schema's, as it caps `pack_id` and `kind`; the cap is T041's, since the contract module owns the field bounds, and T042 stores what T041 bounds (R2Q25 (a); data-model.md § Finding) |
| `locator` | object | no | DISPLAY ONLY, outside the id: `{"line_start": int, "line_end": int}` and/or `{"target": string}`; U+0000 in `target` is refused (§ Rules) |
| `severity` | string | yes | `error` \| `warning` \| `info` |
| `resolution_class` | string | yes | `auto-fix` \| `assisted` \| `human-only` (14.6, spelled exactly) |
| `message` | string | yes | one line, at most 200 characters, written by the family from its own words; never document text (ADV-27); U+0000 is refused (§ Rules) |
| `evidence` | object | yes; the engine sets `{}` when a family or pack supplies none, so every emitted finding carries it (14.5; FR-011; Copilot's review of `3f807204`) | locators only (R2Q25 (a)): paths, line spans, link targets as written, digests, a family's own `family_version`, a refused patch's `refused_patch` and `reason` (15.2a). Any string longer than 200 characters, any key named `excerpt`, `text`, `content` or `quote`, or any key or string that holds U+0000 (§ Rules), is refused |
| `baseline_class` | string | yes in the store, where `0003_` makes it NOT NULL (the holder, `6069507373`); the finding schema's `finding-keys` rule lists it as optional | set by the engine: `new` \| `pack-upgrade` \| `persistent` (R2Q12 (a)); there is no fourth value (I-2 (a), ruled) |

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
  <the manifest entry's id, or "" for none>}`. The categories (the holder,
  `6069024023` item 1) are the nine T041 drafted, `no-sandbox`, `entry-refused`,
  `fetch-failed`, `digest-mismatch`, `declaration-refused`, `pack-crashed`,
  `pack-timed-out`, `pack-bound-hit` and `pack-output-refused`, and two more:
  `dispositions-refused`, a refused dispositions file, an install-level, pathless
  finding (contracts/health-exceptions.md § Rules) that T054 raises; and
  `manifest-refused`, a whole-file refusal of `health/packs.yaml`, with `entry`
  `""`. A category is also the finding's `kind`. The mappings:
  - stdout over the cap is `pack-bound-hit`;
  - non-JSON or contract-breaking pack output is `pack-output-refused`;
  - one finding per (category, entry) per run, with the reasons in `evidence`;
  - the identity's `category` and `entry` are bounded, and `entry` is fixed by the
    category (§ Rules; the holder, `6072197564` and `6073087924`);
  - each category's `pack_id`, as dox-v1.2's schema text for `pack_id` has it
    (the holder, `6072086385` item 1, which replaces `6069024023` item 1's "one
    `pack_id` per category"):
    - a finding against a VALID manifest entry's pack takes that entry's id:
      `fetch-failed`, `digest-mismatch`, `declaration-refused`, `pack-crashed`,
      `pack-timed-out`, `pack-bound-hit` and `pack-output-refused`;
    - every other category is against the product and takes `opendox`:
      `no-sandbox`, `manifest-refused`, `dispositions-refused` and
      `entry-refused`. A refused entry's id may be malformed, reserved or
      repeated, so it names no pack; the entry rides only in `identity.entry`;
- the collision finding below: `{"collided_id": <the colliding id>}`;
- the re-raise of an uncited disappearance (data-model.md § Baseline classes),
  with `pack_id` `opendox`, `kind` `uncited-disappearance` and `human-only`, in
  one of two forms (option (D), the holder, `6069024023` item 2):
  - when the original has a path: `{"disappeared_id": <the original's id>}`,
    `path` the original's, and the original's id and the baseline run in
    `evidence`;
  - when the original's path is empty: the pathless form the schema requires
    (`pathless-identity-is-category-and-entry`) and FR-011 states, `path` `""`
    and `{"category": <the original's kind>, "entry": <its entry, or "">}`, with
    `disappeared_id` and the baseline run in `evidence`. The schema does not
    change.

  Either way it has its own id, never the original's, and it is never itself
  measured as a disappearance, so it is raised in one run only (Copilot's review
  of `67d6f28b`).
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

**An accepted limit: a hash collision ACROSS runs.** Two different identities
whose ids share the 16 hex digits in DIFFERENT runs read as one finding to the
baseline and to an exception. The id's 16-digit form is the ruled one (R2Q10
(a), a ref-name component; N-13), and the cross-run collision stays an accepted
limit (the holder, `6018624750`). A stored `identity` makes a cross-run
collision between STORED findings detectable; an exception-only finding is never
stored, and whether the engine reports it remains T046's concern. By chance the odds are about n²/2⁶⁵ per corpus, about 3 in a trillion
for 10,000 findings; a deliberate collision needs about 2³² SHA-256
evaluations over crafted document text, and it can only mislabel a class or
suppress one finding, never land anything (every repair still lands through
`land`). Widening the id would change the ruled shape, so it is the holder's to
raise with Brett (Copilot's review of `6f073ed2`).

## Rules

- **Refusals.** The store refuses a finding without `pack_id` or `pack_version`
  (15.7). The engine refuses a pack finding whose `resolution_class` is outside
  the three, whose `message`, `evidence` or `identity` breaks the bounds above, or that
  declares a baseline or landing rule; each refusal is itself a finding against
  that pack (15.5, 15.6). Two findings with one id are such a finding too
  (§ The id rule).
- **Install-level findings** (`no-sandbox`, a manifest entry that cannot be
  fetched or whose digest differs, a pack that crashed or timed out) carry an
  empty `path` and `human-only`. Their `pack_id` splits by category (the holder,
  `6072086385` item 1; § The id rule):
  - the entry's id, for a finding against a valid manifest entry's pack
    (`fetch-failed`, `digest-mismatch`, `declaration-refused`, `pack-crashed`,
    `pack-timed-out`, `pack-bound-hit`, `pack-output-refused`);
  - `opendox` for every other category (`no-sandbox`, `manifest-refused`,
    `dispositions-refused`, `entry-refused`), with a refused entry riding only
    in `identity.entry`.
- **A pathless finding's identity** (the holder, `6072197564`, on lane 3's
  REVIEW-W1 T041 NAMES points (b), (c) and (e)):
  - its `identity.category` is from a CLOSED set: an engine category (§ The id
    rule) or `identity-collision`. The re-raise of a pathless original (option
    (D), `6069024023` item 2) takes the original's `kind` as its category, which
    is itself one of those. Packs never raise pathless findings: T045 refuses a
    pack finding with an empty `path` (`6072086385` item 3);
  - its `entry` is at most 200 characters, not 40. A per-entry category's entry
    is also its `pack_id`, which is where the 40-character name rule applies,
    and the check, not `make_finding`, is what binds it (below, `6082100803`);
    only `entry-refused` carries an id that may be malformed, and its form is
    fixed below (`6086098003` item 4), under the same bound of 200;
  - `no-sandbox`, `manifest-refused` and `dispositions-refused` take `entry` `""`,
    and a non-empty entry is REFUSED. A run raises ONE `no-sandbox` finding, never
    one per entry, as data-model.md § Sandbox probe and canary says ("ONE
    install-level finding", R2Q16 (a)). Only the per-entry categories and
    `entry-refused` take a non-empty entry;
  - refined (the holder, `6073087924`, on lane 3's REVIEW-W1 T041 MINOR at
    `health_contract.py:693`): a pathless identity's `entry` is fixed by its
    category, exactly as the engine builds it:
    - the seven per-entry categories (`fetch-failed`, `digest-mismatch`,
      `declaration-refused`, `pack-crashed`, `pack-timed-out`, `pack-bound-hit` and
      `pack-output-refused`) REQUIRE a non-empty entry, the valid entry's id
      (`6072086385` item 1). The check refuses an entry that is empty, the
      reserved `opendox` (contracts/health-packs-manifest.md, the `id` line of
      its example, "`opendox` is reserved (15.7)"), or not a 1-to-40-character
      name, the pack-id name rule (the holder, `6088732352` item 6 (c), encoding
      `6082100803`, on lane 3's REVIEW-W1 T041 MINOR at `health_contract.py:706-707`).
      `6072197564` (c) assumed that the 40-character rule binds through
      `make_finding`; it does not for a re-raise, whose `pack_id` is `opendox`, so
      for a per-entry category's entry the rule binds through this check;
    - `no-sandbox`, `manifest-refused`, `dispositions-refused` and
      `identity-collision` REQUIRE `entry` `""`: the re-raise's original, when it is
      a collision, always takes the entry `""`;
    - `entry-refused` takes either `""` or a non-empty entry, in the form fixed
      below (`6086098003` item 4), which replaces "the refused entry as written"
      for an entry that does not conform;
    - the contract's check refuses any other form, so it admits exactly what the
      engine builds.
  - `entry-refused`'s `identity.entry` (the holder, `6086098003` item 4, on
    Copilot `4230698859` at openxFactory#1283): the pinned schema wins, so "the
    refused entry as written" (`6072197564` (c), `6073087924`) holds only where
    the entry conforms. The form is:
    - `""` when the entry has no id;
    - the id as written, when it is a string matching `[a-z0-9-]+` of at most 200
      characters;
    - otherwise `sha256-` followed by the lowercase hexadecimal SHA-256 of the
      id's canonical text (below), taken over that text's ASCII bytes: 71
      characters, inside the schema's `[a-z0-9-]` pattern and the 200-character
      bound. This covers a malformed or over-long id, a non-string id, and one
      carrying U+0000. It is never truncated and never a schema exception. It is
      `6069507373` T044 item 7's rule (a string over the bound becomes its SHA-256
      hex) in the only form a closed `{category, entry}` identity allows.

    T041 builds it with a helper that is deterministic, total over anything the
    manifest parser yields, distinct for distinct ids but for the accepted limit
    below, and never raising.

    **The canonical text of a refused entry's id** (the holder, `6088484643` item
    5, on Copilot `4232974858` at openxFactory#1283) is its JSON text with sorted
    keys, no whitespace and ASCII-only escapes: Python's
    `json.dumps(id, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
    allow_nan=True, default=str)`.
    - So every value the manifest's YAML parser yields has one spelling.
    - A value JSON cannot represent (a YAML date, timestamp or binary) is spelled
      by its `str()`.
    - If that call raises (a mapping whose keys JSON cannot spell or cannot sort,
      or a self-referencing value), the canonical text is `ascii(id)`, Python's
      `repr()` with every non-ASCII character escaped (the holder, `6088732352`
      item 6 (b), on Copilot `4234200849`), so the canonical text is always ASCII
      and the digest never raises.

    **An accepted limit** (the holder, `6088732352` item 6 (a) and `6089449884`
    item 7, on Copilot `4234200786` and `4234624749`, under `5988818366`): the
    canonical text is not injective across YAML value types.
    - A date or timestamp and its `str()` can share a digest: with `default=str`,
      a YAML date or timestamp id digests like a malformed string id that spells
      its `str()`. A conforming string such as `2026-10-09` is kept as written, so
      it never collides with a date.
    - A non-string mapping key and its JSON spelling can share a digest, because
      `json.dumps` spells such a key in its JSON form: `{1: "a"}` and `{"1": "a"}`
      share one, and so do `True` and `"true"`, and `None` and `"null"`.
    - Each needs two crafted refused entries in one manifest, which makes it
      operator-only and exotic. It is never silent: two findings with one identity
      raise `identity-collision`, which reports any such collision.
    - Making the text injective would need a typed encoding of every value at
      every depth, which is out of proportion to a refused entry's identity.
- **U+0000 is refused** (the NUL seam, the holder, `6072086385` item 4). Postgres
  `jsonb` cannot store U+0000 in a string (SQLSTATE 22P05), so a finding that
  carries it can never be stored.
  - T041 refuses U+0000 in every string a finding carries, keys and values alike
    (`identity`, `evidence`, `locator` and `message`, and `path`, whose bound is its
    row's above), with `FindingRefused` and a bounded `where`. For a pack's
    output, that refusal is T045's whole-output `pack-output-refused` (§ The id
    rule's mapping), so a broken or hostile pack loses its own output, never the
    run.
  - T042's store refuses it too, as `RefusedError` and never a raw driver error
    (defence in depth), in every text parameter it binds, `path` among them
    (`6086098003` item 3), naming the column, before any statement.
  - T044's families never emit it: a document string that contains it takes the
    SHA-256 form under a distinct key (`6069507373` T044 item 7), never
    truncation or silent replacement.
- **The view renders `message` and labels as TEXT**, never HTML, and reads any
  passage it shows from git at render time (R2Q25 (a)).

## Example

The engine's internal object for one finding, AFTER stamping: `id`,
`pack_id`, `pack_version` and `baseline_class` are the engine's, and a family
or pack supplies the rest, `identity` included (a pack's own `id`, if any, is
ignored). `list --json` emits the same object, `identity` included:

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
