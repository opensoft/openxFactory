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

THE HEADER-LINE FORM (`accept-sequenced-after-header-line`, ADDED requirement
"Equivalent declaration sites for the ordered-delta parent declaration"; ruled by
Brett Heap 2026-09-10, verbatim "do door b", on codexFactory issue #268). A
governed corpus may carry its lifecycle headers UNFENCED — codexFactory's does,
49 of its 50 proposals, the one exception being an archived 2026-08 packet — and
there a `sequenced_after:` line is a declaration its author wrote and this reader
could not see (measured on codexFactory main `2ade133`: EIGHT proposals carry
one, and `sequenced_after.corpus_sweep` still reported `declaring = 0`).
`read_header_line` reads ONE named field from a
BOUNDED LIFECYCLE HEADER WINDOW: the first `HEADER_WINDOW_LINES` REAL lines of
the document, the same window and the same line rule `doc_health.corpus`'s
`parse_status`/`parse_kind` already apply to the same document set. It is
offered to `sequenced_after:` ALONE and is NOT wired to `scope_globs:` — see
`read_header_line`'s own note for why widening a path-authorization surface is a
different act from making a position declaration legible.

THE WINDOW IS THE BOUND, AND THE BOUND IS THE POINT. Front matter was chosen for
these fields because a fence delimits; the alternative it refused was UNBOUNDED
PROSE PARSING, where a `sequenced_after:` written inside a paragraph on line 400
would authorize as loudly as one written in a header. A line-bounded window keeps
that refusal — beyond it, the same bytes are prose and declare nothing — while
letting an unfenced corpus's real headers be read.

THE LINE RULE IS DEFINED HERE RATHER THAN IMPORTED, AND THAT IS HELD BY AN
AGREEMENT TEST RATHER THAN BY CONVENTION. `doc_health.lines.split_keepends` owns
the corpus's real-line rule and `doc_health.corpus.STATUS_SCAN_LINES` owns the
window number, but THIS FILE IS VENDORED BYTE-FOR-BYTE into codexFactory
(`scripts/merge_master/frontmatter_strict.py`, pinned at `stack.yaml`'s
`contract_ref`), where no `doc_health` package exists — so an import of it would
break the vendored copy at load time. `align-status-reader-to-real-lines`'s
ratified requirement names the remedy for exactly this case: "Where the corpus
cannot share an implementation across language boundaries, the divergence SHALL
be held by an explicit agreement test rather than by convention." The boundary
here is a VENDORING boundary rather than a language one and takes the same
remedy: `tests/sequenced_after/test_header_line.py` asserts, over the corpus and
over exotic-separator fixtures, that `split_real_lines` agrees with
`doc_health.lines.split_keepends` and that `HEADER_WINDOW_LINES` EQUALS
`doc_health.corpus.STATUS_SCAN_LINES`. A drift in either is a test failure, not
a convention nobody re-checks.

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

#: The BOUNDED LIFECYCLE HEADER WINDOW, in REAL lines of the document, within
#: which a header-line field declaration is read.
#:
#: THE SAME NUMBER `doc_health.corpus.STATUS_SCAN_LINES` DECLARES, and it is
#: restated here rather than imported because this file is vendored into a
#: repository with no `doc_health` package (see the module docstring). Equality
#: with that constant is asserted by `tests/sequenced_after/test_header_line.py`
#: — a drift is a test failure. One window for every lifecycle header of a
#: document, so `Status:` and `sequenced_after:` are found or missed together
#: and no reader has a private idea of where a document's header ends.
HEADER_WINDOW_LINES = 15

_FENCE = "---"
_TOP_LEVEL = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(.*)$")

#: Only the three REAL line endings separate lines: CR, LF, CRLF. NOT
#: `str.splitlines()`, which also breaks on \x0b, \x0c, \x1c-\x1e, \x85, U+2028
#: and U+2029 — so a document carrying one of those would have its 15-line
#: window counted in FRAGMENTS rather than in lines, and a header the writer
#: plainly wrote could go unfound. Mirror of `doc_health.lines._EOL`.
_EOL = re.compile(r"\r\n|\r|\n")


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


def split_real_lines(text: str) -> list[str]:
    """`text` as a list of REAL lines — CR, LF and CRLF only.

    The corpus's shared line rule, restated here because this file is vendored
    into a repository with no `doc_health` package to import it from; equality
    with `doc_health.lines.split_keepends` is held by an explicit agreement test
    (see the module docstring). A reader that splits more aggressively than the
    writer can fail to find a header the writer just wrote correctly, and then
    reports a document as lacking a declaration it plainly carries — a FALSE
    finding, which costs more trust than a crash.
    """
    rows: list[str] = []
    at, size = 0, len(text)
    while at < size:
        match = _EOL.search(text, at)
        if match is None:
            rows.append(text[at:])
            break
        rows.append(text[at:match.start()])
        at = match.end()
    return rows


def fence_span(lines: list[str]) -> int | None:
    """The index of the CLOSING `---` of a leading front-matter fence, or None
    when the document carries no well-formed (opened AND closed) fence.

    ONE fence rule for both readers. `fenced_lines` takes the lines INSIDE the
    span and the header-line reader SKIPS them, so a field declared in the fence
    is read once, by the front-matter reader, and never counted a second time as
    a header line of the same document.
    """
    if not lines or lines[0].strip() != _FENCE:
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == _FENCE:
            return index
    return None  # no closing fence


def fenced_lines(source: str | bytes | Path) -> list[str] | None:
    """The lines inside the leading `---`-fenced front-matter block, or None when
    the document carries no well-formed (opened AND closed) fence.

    Split on REAL lines (`split_real_lines`) rather than `str.splitlines()`, so
    the fence span and the lifecycle header window agree about where this
    document's lines are. Measured before the conversion over every `proposal.md`
    in both clones — the openxFactory (191) and codexFactory (50) corpora plus
    the 131 test fixtures carrying their own `openspec/changes/` trees, 372 files
    in all: the two splittings return an IDENTICAL block for every one, so the
    change costs a zero baseline diff and buys one line rule instead of two.
    """
    lines = split_real_lines(source_text(source))
    closing = fence_span(lines)
    if closing is None:
        return None
    return lines[1:closing]


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


# --- the header-line form -----------------------------------------------------


class _NoHeaderLine:
    """The sentinel for A FIELD NOT DECLARED AS A HEADER LINE.

    Distinct from `None`, which is what a header line WITH NO VALUE
    (`sequenced_after:` alone) reads as — present-but-null, refused downstream by
    the field's own shape validation. Presence is decided by the KEY, never by
    the value, on both reading paths.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:  # pragma: no cover - diagnostics only
        return "<no header-line declaration>"


#: No header-line declaration. Never equal to `None` or to `[]`.
NO_HEADER_LINE = _NoHeaderLine()


def read_header_line(
    source: str | bytes | Path,
    field: str,
    window: int = HEADER_WINDOW_LINES,
) -> object:
    """Read `field` declared as a LIFECYCLE HEADER LINE, or `NO_HEADER_LINE`.

    A header-line declaration is a line matching ``^<field>:`` — the field's OWN
    name, at column 0, case-sensitively — that sits within the first `window`
    REAL lines of the document and OUTSIDE any leading `---` fence. Its value is
    everything after the colon ON THAT ONE LINE, loaded through `strict_load`,
    so the header-line form and the front-matter form are read by ONE loader and
    refuse the same constructs.

    OFFERED TO `sequenced_after:` ALONE, AND THE ASYMMETRY IS THE DECISION. This
    function is generic, but the only caller is `sequenced_after.read_declaration`
    and `scripts/scope_globs.py` is deliberately UNCHANGED. `scope_globs:`
    authorizes WHICH PATHS an autonomous merge may write, so a new place to
    declare it is a new place to widen a path grant; `sequenced_after:` declares
    WHERE IN A CHAIN a change sits, and its consumer applies its own root proof,
    its own co-modifier cross-check and its own refusals on top — so making an
    author's existing declaration legible authorizes nothing that absence did
    not already refuse. Widening the path field is a separate act needing its own
    ruling, and this change does not take it.

    THE DECLARATION IS ONE LINE, AND THAT IS A CONSEQUENCE OF BEING UNFENCED. A
    fence supplies a closing delimiter; an unfenced document has none, so a
    multi-line value's END is undefined and a window boundary falling inside it
    would show a reviewer three parents and authorize two — the same
    show-one-authorize-another defect the strict loader exists to refuse. A flow
    value (`field: [a, b]`) is self-delimiting on its line and is therefore the
    only unfenced form admitted. A `field:` line whose value is EMPTY and whose
    next line is an INDENTED continuation is a block-sequence attempt and is
    REFUSED BY NAME rather than silently read as null, because the author of
    those bytes declared parents and is owed the reason the reader will not take
    them.

    TWO header lines for one field are REFUSED as the duplicate key they are:
    both matched lines are handed to `strict_load` together, so the refusal is
    the loader's own duplicate-key message and no second rule is written.

    FENCE LINES ARE SKIPPED BUT STILL COUNT toward the window: the window is the
    first `window` lines OF THE DOCUMENT — one window rule, the one
    `doc_health.corpus.parse_status` already applies to the same document set —
    rather than a second window measured from wherever a fence happens to end.
    A fenced document declares in its front matter and needs no header line.

    Raises `StrictFrontMatterError` for every refused form.
    """
    lines = split_real_lines(source_text(source))
    closing = fence_span(lines)
    if closing is None and lines and lines[0].strip() == _FENCE:
        # AN OPENED-BUT-NEVER-CLOSED LEADING FENCE DECLARES NOTHING ON EITHER
        # PATH. `fence_span` returns None for it, so without this the scan would
        # start at line 0 and read a `field:` line from INSIDE a span the author
        # plainly meant as front matter — showing a reviewer fenced front matter
        # while the reader took a header line out of it, one document apart. It
        # would also flip this module's existing, deliberate posture (see the
        # docstring): a document with no well-formed fence "still reads as NO
        # FRONT MATTER — which is fail-CLOSED here". The header-line site keeps
        # that posture rather than becoming the one way a malformed fence starts
        # declaring. Silent rather than refused, exactly as the fenced reader is
        # silent about the same malformation: a new refusal for a form the
        # shipped reader tolerates is not in this change's set.
        return NO_HEADER_LINE
    start = 0 if closing is None else closing + 1
    pattern = re.compile(rf"^{re.escape(field)}:(.*)$")

    matched: list[tuple[int, str]] = []
    for index in range(start, min(window, len(lines))):
        match = pattern.match(lines[index])
        if match:
            matched.append((index, lines[index]))
    if not matched:
        return NO_HEADER_LINE

    for index, line in matched:
        value = pattern.match(line).group(1)
        if value.strip():
            continue
        following = lines[index + 1] if index + 1 < len(lines) else ""
        if following.strip() and following[:1].isspace():
            raise StrictFrontMatterError(
                f"the `{field}` header line at line {index + 1} carries no value "
                f"on its own line and is followed by an indented continuation: "
                f"the header-line form is a SINGLE LINE, because an unfenced "
                f"document supplies no closing delimiter and a value the header "
                f"window cuts in half would show a reader one declaration and "
                f"authorize another. Declare a block value inside a `---` fence, "
                f"or write the flow form `{field}: [...]` on one line")

    block = "\n".join(line for _index, line in matched)
    check_ceiling(block, f"the `{field}` header line")
    parsed = strict_load(block, what=f"the `{field}` header line")
    if isinstance(parsed, dict):
        if field not in parsed:  # pragma: no cover - defensive
            raise StrictFrontMatterError(
                f"the `{field}` header line does not declare `{field}` at its "
                f"top level")
        return parsed[field]
    return parsed
