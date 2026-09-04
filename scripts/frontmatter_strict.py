"""The STRICT loader for the realization-axis front-matter block.

Realizes the `release-realization` requirement "Strict loading of the
realization-axis front-matter block", ADDED by `add-sequenced-after-substrate`
(ratified 2026-09-01; **convener ruling OQ-1: the retrofit lands INSIDE that
change**, so this module is the loader for BOTH structured fields of the block —
`scope_globs:` and `sequenced_after:` — and `scripts/scope_globs.py` reads
through it rather than through `yaml.safe_load`).

WHY A LOADER AND NOT A SCAN. `yaml.safe_load` applies LAST-DUPLICATE-KEY-WINS
SILENTLY. A proposal carrying two `scope_globs:` blocks therefore shows a human
reviewer the FIRST and authorizes the LAST, and the same defect applied to
`sequenced_after:` would show a reviewer one parent and walk another. Duplicate
refusal is therefore done BY CONSTRUCTION — a `yaml.SafeLoader` subclass whose
`construct_mapping` raises on a repeated key — so NESTING DEPTH CANNOT SMUGGLE A
DUPLICATE PAST A TOP-LEVEL CHECK: a nested duplicate authorizes exactly as well
as a top-level one.

THE REFUSED SET MIRRORS THE CONSUMING VERIFIER'S STRICT LOADER, and that parity
is a BUILD OBLIGATION rather than a coincidence (`add-sequenced-after-substrate`
task 2.5). The authority is codexFactory
`scripts/merge_master/change_digest.py` — `StrictLoader`, `_refuse_anchor`,
`_refuse_merge_key`, `_strict_construct_mapping`, `_scan_refused_constructs`,
`strict_load`, `CAP_STRICT_YAML_BYTES` — transcribed here byte-for-behaviour
because openxFactory cannot import that module (it lives in a sibling submodule
that is not vendored into openxFactory's CI tree), exactly as the glob dialect in
`scripts/scope_globs.py` is mirrored. **A change to either refused set MUST be
made in lockstep with the other**, or the neutral validator and the consuming
verifier disagree about what the same bytes mean — and a corpus that passes
validation would refuse at the gate while a corpus that fails validation could
pass it.

The refused set:

  * DUPLICATE KEYS at any mapping level (by construction, NFC-normalized first,
    because `café` composed and `café` decomposed are one key to every human
    reading the file and two to the machine);
  * YAML ANCHORS (`&`) — no value may be reused by reference;
  * YAML ALIASES (`*`) — an alias makes one authorization input appear in two
    places under one edit;
  * MERGE KEYS (`<<:`) — a merge key makes a mapping's content depend on a
    mapping the reader is not looking at;
  * NON-UTF-8 BYTES — refused rather than replaced, since a replacement
    character is an interpretation the reader did not choose;
  * a document over the DECLARED BYTE CEILING, `CEILING_BYTES = 65_536`, applied
    BEFORE the parse (bounding a parser with its own output is no bound at all);
  * `%YAML` / `%TAG` DIRECTIVES and MORE THAN ONE DOCUMENT — the two extras the
    consuming verifier also refuses, kept here so the two sets are IDENTICAL. A
    declared version PyYAML does not implement makes `yes`/`no`/`on`/`off` and
    leading-zero integers mean one thing to the human reading the directive and
    another to the machine authorizing from it; a second `---` boundary would
    read as front matter to a human and as body text to the machine. Measured
    2026-09-01: no proposal in the corpus carries either, so refusing costs
    nothing and closes both classes outright.

WHAT THIS MODULE DELIBERATELY DOES NOT CHANGE. The openxFactory proposal
front-matter block is a set of PROSE HEADERS with two structured fields in it —
not a strict-YAML document — so the block as a whole is still never YAML-parsed
at once, and a prose header is still returned as its raw joined string. Only the
STRUCTURED fields are loaded, and they are loaded strictly. A document with no
well-formed fence, or one whose fence does not begin at line 1 (a UTF-8 BOM or a
leading blank line), still reads as NO FRONT MATTER — which is fail-CLOSED here
(absence of `scope_globs` means "not provenance-eligible"; absence of
`sequenced_after` means "no declaration made"), while the consuming verifier
refuses a BOM outright on its own path. Tightening that is not in this
requirement's refused set and is not done here.

Deterministic: text/YAML reads only, no model calls, no writes, no network.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - pyyaml is a suite dependency
    yaml = None


#: The byte ceiling, applied BEFORE the parse. An OPERATIVE NUMBER rather than a
#: gesture at one, and the SAME number the consuming verifier declares
#: (`change_digest.CAP_STRICT_YAML_BYTES`). Measured 2026-09-01: the largest
#: front-matter block in this corpus is 9,085 bytes
#: (`archive/2026-08-28-declare-sentinel-pin-vocabulary`), so the ceiling sits
#: about seven times above the observed maximum — high enough that no honest
#: proposal meets it, low enough to bound the parser.
CEILING_BYTES = 65_536

#: The STRUCTURED fields of the realization-axis block — the ones read through
#: the strict loader. Every other front-matter field is a prose header.
STRUCTURED_FIELDS = ("scope_globs", "sequenced_after")

_FENCE = "---"
_TOP_LEVEL = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(.*)$")


class StrictFrontMatterError(Exception):
    """A strict-loader refusal.

    Carries a message naming the construct refused and, where the parser knows
    it, the line it sits on. Callers with their own error vocabulary
    (`scope_globs.ScopeGlobsError`, `sequenced_after.SequencedAfterError`) catch
    this and re-raise in their own type, preserving the message — a refusal that
    named a different condition than the one that fired would be worse than no
    refusal.
    """


# --- the loader ---------------------------------------------------------------


if yaml is not None:

    class StrictLoader(yaml.SafeLoader):
        """``SafeLoader`` with anchors, aliases, merge keys and duplicates
        REFUSED rather than resolved."""

    def _refuse_anchor(loader, parent, index):
        event = loader.peek_event()
        if isinstance(event, yaml.events.AliasEvent):
            raise StrictFrontMatterError(
                f"a YAML alias (*{event.anchor}) at line "
                f"{event.start_mark.line + 1}: an alias makes one authorization "
                "input appear in two places under one edit")
        anchor = getattr(event, "anchor", None)
        if anchor is not None:
            raise StrictFrontMatterError(
                f"a YAML anchor (&{anchor}) at line "
                f"{event.start_mark.line + 1}: anchors are refused so no value "
                "can be reused by reference")
        return yaml.composer.Composer.compose_node(loader, parent, index)

    def _refuse_merge_key(loader, node):
        for key_node, _value_node in node.value:
            if key_node.tag == "tag:yaml.org,2002:merge":
                raise StrictFrontMatterError(
                    f"a `<<:` merge key at line "
                    f"{key_node.start_mark.line + 1}: a merge key makes a "
                    "mapping's content depend on a mapping the reader is not "
                    "looking at")

    def _strict_construct_mapping(loader, node, deep: bool = False):
        _refuse_merge_key(loader, node)
        seen: set = set()
        for key_node, _value_node in node.value:
            key = loader.construct_object(key_node, deep=True)
            hashable = key if isinstance(key, (str, int, float, bool, tuple)) else str(key)
            if isinstance(hashable, str):
                hashable = unicodedata.normalize("NFC", hashable)
            if hashable in seen:
                raise StrictFrontMatterError(
                    f"the duplicate key {key!r} at line "
                    f"{key_node.start_mark.line + 1}: `yaml.safe_load` applies "
                    "last-duplicate-wins SILENTLY, so a reader would see the "
                    "first value and the machine would authorize from the last")
            seen.add(hashable)
        return yaml.constructor.SafeConstructor.construct_mapping(
            loader, node, deep=deep)

    StrictLoader.compose_node = _refuse_anchor
    StrictLoader.construct_mapping = _strict_construct_mapping
    StrictLoader.flatten_mapping = _refuse_merge_key


def _scan_refused_constructs(text: str) -> None:
    """Name the MOST SPECIFIC refused construct in the event stream.

    The loader guards are the enforcement; this scan exists so the REFUSAL IS
    LEGIBLE. Composition reaches an anchor before it reaches the alias or the
    merge key that uses it, so a loader-order refusal would report "an anchor"
    for all three constructs and the three negative fixtures would then key on
    one message — the collapse a per-construct refused set exists to prevent.
    Priority is most-specific-first: a merge key, else an alias, else a bare
    anchor. (Mirror of the consuming verifier's `_scan_refused_constructs`.)

    ``yaml.parse`` yields EVENTS without composing, so an alias here needs no
    anchor resolution and a merge key is seen as the plain scalar ``<<`` it is.
    """
    anchors: list[str] = []
    aliases: list[str] = []
    merges: list[int] = []
    try:
        for event in yaml.parse(text, Loader=StrictLoader):
            if isinstance(event, yaml.events.AliasEvent):
                aliases.append(
                    f"*{event.anchor} at line {event.start_mark.line + 1}")
                continue
            anchor = getattr(event, "anchor", None)
            if anchor:
                anchors.append(
                    f"&{anchor} at line {event.start_mark.line + 1}")
            if (isinstance(event, yaml.events.ScalarEvent)
                    and event.value == "<<" and event.style is None):
                merges.append(event.start_mark.line + 1)
    except yaml.YAMLError:
        return  # the load below reports the parse error itself
    if merges:
        raise StrictFrontMatterError(
            f"a `<<:` merge key at line {merges[0]}: a merge key makes a "
            "mapping's content depend on a mapping the reader is not looking at")
    if aliases:
        raise StrictFrontMatterError(
            f"a YAML alias ({aliases[0]}): an alias makes one authorization "
            "input appear in two places under one edit")
    if anchors:
        raise StrictFrontMatterError(
            f"a YAML anchor ({anchors[0]}): anchors are refused so no value can "
            "be reused by reference")


def check_ceiling(text: str, what: str = "the document") -> None:
    """Refuse `text` when it exceeds `CEILING_BYTES`, measured in UTF-8 bytes.

    Applied BEFORE any parse: a parser is the thing being bounded, so bounding
    it with its own output is no bound at all. Refuses rather than truncating —
    a truncated authorization surface is a widened one.
    """
    size = len(text.encode("utf-8", "surrogateescape"))
    if size > CEILING_BYTES:
        raise StrictFrontMatterError(
            f"{what} is {size} bytes, above the {CEILING_BYTES}-byte ceiling; "
            "the ceiling is applied before the parse and refuses rather than "
            "truncating")


def strict_load(text: str, what: str = "the document") -> object:
    """Load EXACTLY ONE YAML document from `text` under the strict loader.

    Raises `StrictFrontMatterError` for every refused form. Returns the loaded
    document (which may be None for an empty one).
    """
    if yaml is None:  # pragma: no cover - pyyaml is a suite dependency
        raise StrictFrontMatterError(
            "pyyaml is required to read the realization-axis front-matter block")
    check_ceiling(text, what)
    for number, line in enumerate(text.split("\n"), start=1):
        if line.startswith("%"):
            raise StrictFrontMatterError(
                f"a YAML directive ({line.strip()!r}) at line {number}: a "
                "declared version PyYAML does not implement makes the reader "
                "and the machine read one document two ways")
    _scan_refused_constructs(text)
    try:
        documents = list(yaml.load_all(text, Loader=StrictLoader))
    except StrictFrontMatterError:
        raise
    except yaml.YAMLError as exc:
        raise StrictFrontMatterError(f"{what} does not parse: {exc}") from exc
    if len(documents) > 1:
        raise StrictFrontMatterError(
            f"{len(documents)} YAML documents where exactly one is required; a "
            "second `---` boundary would read as front matter to a human and as "
            "body text to the machine")
    return documents[0] if documents else None


# --- front-matter reading -----------------------------------------------------


def decode_utf8(raw: bytes, what: str = "the document") -> str:
    """Decode `raw` as STRICT UTF-8, refusing rather than replacing.

    A replacement character is an interpretation the reader did not choose, and
    on an authorization surface an unreadable byte must refuse rather than
    become `\\ufffd`.
    """
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StrictFrontMatterError(
            f"{what} is not valid UTF-8 (byte {exc.start}: {exc.reason}); "
            "non-UTF-8 bytes are refused rather than replaced, because a "
            "replacement character is an interpretation the reader did not "
            "choose") from exc


def source_text(source: str | bytes | Path) -> str:
    """The document text for a path, byte string, or text source."""
    if isinstance(source, Path):
        return decode_utf8(source.read_bytes(), what=str(source))
    if isinstance(source, bytes):
        return decode_utf8(source)
    return source


def fenced_lines(source: str | bytes | Path) -> list[str] | None:
    """The lines inside the leading `---`-fenced front-matter block, or None when
    the document carries no well-formed (opened AND closed) fence."""
    text = source_text(source)
    lines = text.splitlines()
    if not lines or lines[0].strip() != _FENCE:
        return None
    body: list[str] = []
    for line in lines[1:]:
        if line.strip() == _FENCE:
            return body
        body.append(line)
    return None  # no closing fence


def field_blocks(lines: list[str]) -> dict[str, list[str]]:
    """Split front-matter lines into top-level fields, each mapped to its
    ORIGINAL lines (its `field:` line plus every following indented or
    continuation line up to the next top-level key).

    A field declared TWICE keeps BOTH blocks under one key, in document order,
    so a structured field's duplicate declaration reaches the strict loader as
    the duplicate key it is and is refused there by name.
    """
    blocks: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines:
        m = _TOP_LEVEL.match(line)
        if m:
            current = m.group(1)
            blocks.setdefault(current, []).append(line)
        elif current is not None:
            blocks[current].append(line)
    return blocks


def read_front_matter(
    source: str | bytes | Path,
    structured_fields: tuple[str, ...] = STRUCTURED_FIELDS,
) -> dict:
    """Return the realization-axis front-matter of a `proposal.md` as a dict.

    Accepts document text, bytes, or a path. Every field in `structured_fields`
    (default: `scope_globs`, `sequenced_after`) is read from ITS OWN sub-block
    THROUGH THE STRICT LOADER and returned as its structured value; every other
    field is returned as its raw joined string, because the surrounding block is
    prose headers rather than YAML. A structured field PRESENT with an empty
    value is returned as None UNDER ITS KEY — presence and absence are different
    facts and a reader that conflated them would destroy the root-proof doctrine
    the `sequenced_after` field rests on.

    Returns an empty dict when there is no well-formed front-matter fence.
    Raises `StrictFrontMatterError` for every refused form.
    """
    lines = fenced_lines(source)
    if lines is None:
        return {}
    check_ceiling("\n".join(lines), "the front-matter block")
    result: dict[str, object] = {}
    for field, block in field_blocks(lines).items():
        if field in structured_fields:
            text = "\n".join(block)
            parsed = strict_load(text, what=f"the `{field}` front-matter block")
            if isinstance(parsed, dict):
                if field not in parsed:
                    raise StrictFrontMatterError(
                        f"the `{field}` front-matter block does not declare "
                        f"`{field}` at its top level")
                result[field] = parsed[field]
            else:
                result[field] = parsed
        else:
            first = _TOP_LEVEL.match(block[0])
            rest = [first.group(2)] + block[1:] if first else block
            result[field] = "\n".join(rest).strip()
    return result
