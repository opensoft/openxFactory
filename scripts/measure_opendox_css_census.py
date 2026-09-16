#!/usr/bin/env python3
"""RE-MEASURE the gate loop's CSS census — RULED Q7 (`opensoft/openxFactory#656`
comment `5648049748`): *"a contributed binding's CSS lives WITH THE BINDING, in
its own sheet; openDox's declared design tokens (the `--st-*` family, S7) are
the one stable styling surface; nothing else in `styles.css` is."*

    python3 scripts/measure_opendox_css_census.py \\
        <openDox-code checkout> <openXdox-code checkout> [--json out.json]
        [--gate-dir <dir>]

`openxdox.view_extensions.STYLE_RESIDUE` records 51 exclusive / 24 shared
classes MEASURED at openDox-code `cb343ae8` — three slices ago. This re-derives
both halves at whatever heads it is pointed at, and adds the two things the old
figure did not carry: WHICH RULE BLOCKS the exclusive classes own (so an
extraction has bytes to move, not just names), and which of those blocks READ a
`--st-*` token (so the sheet that leaves can be checked against Q7's "the one
stable styling surface" rule).

THE SCANNER IS THE LEG'S OWN. String literals come from `_js_spans`, copied
verbatim in behaviour from openDox-code `tests/test_web_boundary.py` (slice S7's
regex-literal-aware span walk) rather than from a fresh regex, so a token this
tool says a module names is a token that leg's own suite would see.

THE EXTRACTION READS THE TWO SIDES DIFFERENTLY, and the asymmetry is the whole
safety argument: the GATE side must be a CLASS-BEARING position (or a
concatenation prefix), because a stray label equal to a selector token would
otherwise move an openDox rule to another leg; the openDox side is the BROAD
scan, because over-including there only KEEPS a rule. `extract_class` is that
rule and is what decides which blocks leave; `class` and `narrow_class` are
reported beside it so the difference is visible rather than asserted.

CLASSIFICATION, per class token declared as a real selector in `styles.css`:
  gate_exclusive  named by >=1 of openXdox's six contributed modules and by NO
                  file of openDox's own bundle (app.js, index.html, views/*.js)
  shared          named by both columns
  opendox_only    named by openDox's bundle and not by the six
  unreferenced    named by no file on either side (a literal search cannot see a
                  token built by concatenation; these NEVER leave)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# ONE DEFINITION OF A LINE, the floor's (RULED Q-L8 (c), `scripts/carve_lines.py`).
# This census reports a line COUNT and a line EXTENT per block, and the
# manifest's `web/styles.css` row cites both — so they have to be numbered in
# the definition `validate-carve-manifest.py` bounds declared lines against and
# `verify-carve-arrival.py` checks them at the destination. `sys.path` rather
# than a package import because `scripts/` is a directory of programs, and this
# one is also loaded by file location from `tests/carve_manifest/`.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import carve_lines  # noqa: E402

# --------------------------------------------------------------------------
# openDox-code tests/test_web_boundary.py's span walk, behaviour-for-behaviour.
#
# ITS ONE KNOWN LIMIT, MEASURED AND LEFT DELIBERATELY (Copilot review of
# openxFactory #1068, round 5). The `${...}` walk counts braces without lexing
# the interpolation's own strings, so `${cond ? "{" : ""}` would never balance
# and the span would swallow the rest of the file. It does not bite here: over
# the 44 JavaScript files this census reads (openXdox-code `0a0265f7`'s six
# contributed modules and openDox-code `0b4e8bbf`'s bundle) there are 34
# interpolations and NONE carries a brace inside a string inside one, and no
# string span exceeds 1,500 characters — a runaway would be visible as a span
# reaching the end of the file.
#
# AND IT IS NOT THIS ACT'S TO REPAIR. The walk is copied behaviour-for-
# behaviour from openDox-code's own `tests/test_web_boundary.py`, which is the
# tool's whole guarantee: a token this census says a module names is a token
# that leg's own suite would see. Diverging here would break that in the
# direction that matters, so the repair belongs in that suite and this copy
# together — REGISTERED FOR A LATER DECLARED ACT.
# --------------------------------------------------------------------------
_JS_REGEX_PREFIX = re.compile(
    r"(?:[=(,:;!&|?{}\[\+\-*%<>~^]|^|\breturn\b|\btypeof\b|\bcase\b|\bin\b|\bof\b"
    r"|\bnew\b|\bdelete\b|\bvoid\b|\binstanceof\b|\bdo\b|\belse\b|\byield\b"
    r"|\bawait\b)\s*$"
)


def _js_spans(text: str) -> list[tuple[str, int, int]]:
    spans: list[tuple[str, int, int]] = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if c == "/" and nxt == "/":
            j = text.find("\n", i)
            j = n if j < 0 else j
            spans.append(("comment", i, j)); i = j; continue
        if c == "/" and nxt == "*":
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            spans.append(("comment", i, j)); i = j; continue
        if c in "\"'`":
            quote, j = c, i + 1
            while j < n:
                if text[j] == "\\":
                    j += 2; continue
                if text[j] == quote:
                    break
                if quote == "`" and text[j] == "$" and j + 1 < n and text[j + 1] == "{":
                    depth, k = 1, j + 2
                    while k < n and depth:
                        if text[k] == "{":
                            depth += 1
                        elif text[k] == "}":
                            depth -= 1
                        k += 1
                    j = k; continue
                j += 1
            end = min(j + 1, n)
            spans.append(("string", i, end)); i = end; continue
        if c == "/":
            before = text[max(0, i - 40):i]
            if _JS_REGEX_PREFIX.search(before):
                j, in_class = i + 1, False
                while j < n:
                    ch = text[j]
                    if ch == "\\":
                        j += 2; continue
                    if ch == "[":
                        in_class = True
                    elif ch == "]":
                        in_class = False
                    elif ch == "/" and not in_class:
                        break
                    elif ch == "\n":
                        break
                    j += 1
                if j < n and text[j] == "/":
                    spans.append(("regex", i, j + 1)); i = j + 1; continue
        i += 1
    return spans


_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
_LINE_COMMENT = re.compile(r"//[^\n]*")


def _is_concatenation(text: str, lo: int, hi: int) -> bool:
    r"""True where the two string literals around `text[lo:hi]` are joined by
    `+` and nothing else.

    GROUPING AND COMMENTS ARE NOT OPERANDS (Copilot review of openxFactory
    #1068, round 13): `("ga" + "te") + "bar"` and `"ga" /* c */ + "te"` are
    concatenations, and a separator test of `\s*\+\s*` alone saw an unrelated
    pair. This is the BROAD scan — the KEEP side — so a chain missed here can
    mark a class unreferenced and EXTRACT the block that styles it.

    AND A CALL'S `)` IS NOT A GROUPING `)` (round 16). Allowing any
    parenthesis let `label("ga") + "te"` join into `gate`: the left operand is
    a CALL RESULT and the literal inside it is that call's argument, so the
    concatenation the join claims never happens. Each `)` in the separator is
    matched back to its `(`, and a `(` that follows an identifier, a `]` or a
    `)` opens a CALL — the run breaks there.

    Anything with a NAME in the separator is still not a concatenation of
    these two: `f("a") + g("b")` has `g` between them, which is the
    conservative half of the same rule.
    """
    raw = text[lo:hi]
    blanked = _LINE_COMMENT.sub(lambda m: " " * len(m.group(0)),
                                _BLOCK_COMMENT.sub(
                                    lambda m: " " * len(m.group(0)), raw))
    if not re.fullmatch(r"[\s()]*\+[\s()]*", blanked):
        return False
    for k, ch in enumerate(blanked):
        if ch != ")":
            continue
        depth, j = 1, lo + k - 1
        while j >= 0 and depth:
            if text[j] == ")":
                depth += 1
            elif text[j] == "(":
                depth -= 1
            j -= 1
        if j >= 0 and re.match(r"[A-Za-z0-9_$\]\)]", text[j]):
            return False
    return True


def js_literal_text(text: str) -> str:
    """Every string literal of a module — comments and regexes out.

    AND EVERY ADJACENT PAIR JOINED ACROSS A `+` (Copilot review of openxFactory
    #1068, round 8). `el("div", "gate" + "bar")` writes a class NEITHER literal
    contains, and `_PREFIX` does not see it either — a prefix has to end in `-`
    or run into a `${…}`. This is the BROAD scan, the one the KEEP side of the
    decision runs on, so a reference it misses is a rule wrongly EXTRACTED:
    exactly the error direction the asymmetry exists to prevent, arriving
    through the seam instead of the token.

    The join is emitted BESIDE the literals, never instead of them, so nothing
    a literal names stops being named. MEASURED at openDox-code `0b4e8bbf` /
    openXdox-code `0a0265f7`: 294 adjacent pairs, all of them prose messages
    split across source lines, and the census is UNCHANGED.
    """
    spans = [(a, b) for kind, a, b in _js_spans(text) if kind == "string"]
    out = [text[a + 1:b - 1] for a, b in spans]
    run: list[str] = []

    def flush() -> None:
        # EVERY CONTIGUOUS SUB-RUN, not only the pairs and not only the whole
        # chain (Copilot review, round 10): `"ga" + "te" + "bar"` writes
        # `gatebar`, which a pairwise join (`gate`, `tebar`) never produces.
        # The class can be any contiguous stretch of the chain, and a MISS on
        # this side EXTRACTS a rule openDox still uses.
        for i in range(len(run)):
            for j in range(i + 2, len(run) + 1):
                out.append("".join(run[i:j]))
        run.clear()

    for k, (a, b) in enumerate(spans):
        if run and not _is_concatenation(text, spans[k - 1][1], a):
            flush()
        run.append(text[a + 1:b - 1])
    flush()
    return "\n".join(out)


# --------------------------------------------------------------------------
# TWO SCANS, and the census publishes the second while the extraction obeys the
# first.
#
# BROAD  — the token appears anywhere inside a string literal, on the class
#          alphabet's own word boundary. It cannot MISS a reference, so a class
#          it says openDox does not name is a class openDox does not name: this
#          is the scan the "does this block leave?" decision runs on, and being
#          over-inclusive on openDox's side is exactly the direction an
#          extraction wants to err in.
# NARROW — the token appears in a CLASS-BEARING position: after a `.` in a
#          literal that IS a selector (`.foo`, `.foo.bar`, `.a .b` — NOT
#          `div.foo`, which reads exactly like `error.foo`; see
#          `selector_class_tokens`), inside a `class="…"` attribute of a
#          template literal or of `index.html`, or as one of a literal that is
#          a bare class list. This is what `STYLE_RESIDUE`'s
#          51 / 24 at `cb343ae8` counted — reproduced exactly by this tool at
#          that commit — so it is the figure the record moves forward.
# --------------------------------------------------------------------------
_CLASSTOK = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")


#: A class token BUILT BY CONCATENATION — `el("button", "disposebtn dispose-" +
#: v.outcome, …)` (`dispose.js`:275) — is named by no literal a word-boundary
#: search can see, and `STYLE_RESIDUE`'s 51 is exactly what that blindness
#: costs: `.dispose-accepted`, `.dispose-rejected` and `.dispose-deferred` are
#: the gate column's own and were counted `unreferenced` at `cb343ae8`. A
#: literal ENDING in a class-alphabet fragment that ends in `-`, or one whose
#: fragment runs straight into a `${…}` substitution, is a PREFIX: every
#: declared token starting with it is named by that file.
_PREFIX = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*-)(?:\$\{|$)")


def _literals(text: str, suffix: str) -> list[str]:
    if suffix == ".js":
        return [text[a + 1:b - 1] for kind, a, b in _js_spans(text)
                if kind == "string"]
    # ONE TAG-AWARE PARSER FOR BOTH SIDES (Copilot review of openxFactory
    # #1068, rounds 11 and 15). A regex over the whole page read `class=`
    # inside a `title`, inside a comment and inside `<script>` text as live
    # attributes, and could not see `<i class=gatebar>` at all. The markup
    # walk the JavaScript templates already go through answers both: inside an
    # open tag, outside every quoted value, `class` a whole attribute name,
    # and the value in either quote or none.
    return markup_class_runs(text, r"[A-Za-z0-9_ -]*", r"[A-Za-z0-9_-]*")


#: A BARE LITERAL IS A CLASS ONLY IN ARGUMENT OR ASSIGNMENT POSITION, and this
#: is the parser-free discriminator that makes the gate side safe to act on
#: (Copilot review of openxFactory #1068, round 3). `el("div", "gatebar")` and
#: `node.className = "gatebar"` name a class; `{ kind: "summary" }` and
#: `state === "summary"` name a VALUE, and under a rule that counted every bare
#: literal a value equal to a selector token could send an openDox rule to
#: another leg.
#:
#: WHY THE RULE CANNOT SIMPLY BE DROPPED INSTEAD: 46 of the 54 classes this
#: census finds at `0b4e8bbf`/`0a0265f7` rest on a bare literal and nothing
#: else, because this bundle's element helper takes the class as its SECOND
#: ARGUMENT (`el(tag, className, text)`). A scan without bare literals answers
#: 5 where the truth is 54 — it is the dominant class-bearing form here, not
#: noise to be filtered out.
#:
#: AND AN ASSIGNMENT COUNTS ONLY WHERE THE TARGET SAYS IT IS A CLASS (Copilot
#: review of openxFactory #1068, round 5). A bare `x = "…"` rule made every
#: assigned string a class write, so `const message = "gatebar"` — or
#: `btn.title = "commission this staging topic"`, whose every word is on the
#: class alphabet and two of which (`topic`, `staging`) `styles.css` declares —
#: claimed ownership of an openDox rule. The target is now named: `className`,
#: `class`, `cls`, `classes`, `classList` (`+=` included, which is how a class
#: is appended). MEASURED at `0b4e8bbf`/`0a0265f7`: the census is UNCHANGED at
#: 54 gate-exclusive classes / 59 exclusive blocks / 89 lines — WHAT LEAVES IS
#: UNCHANGED — because every one of the 46 bare-literal classes here arrives in
#: ARGUMENT position (`el(tag, className, text)`), not by assignment. What does
#: change is the SHARED count: `topic` was shared only through
#: `btn.title = "commission proposal authoring for this staging topic "`
#: (`dispose.js`:402), and shared classes STAY either way. Comparison is
#: excluded by construction — `==`, `!=`, `<=`, `>=` end in `=` but none of
#: them follows a class-named target.
#:
#: AND A VALUE UNDER A CLASS-NAMING KEY IS CLASS-BEARING, which is the one
#: context an argument/assignment rule alone gets wrong here: `dispose.js`:202-206
#: declares its five outcome classes as `{ ok: { label: "applied", cls: "is-ok" } }`
#: — a TABLE of classes, and the key says what the value is. Without this
#: clause the census loses exactly those five (`is-ok`, `is-queued`,
#: `is-stalled`, `is-refused`, `is-error`) and answers 49 where the truth is 54.
#: `{ kind: "summary" }` is still a value and still names nothing, because
#: `kind` is not a class-naming key — which is the distinction the whole rule
#: is for.
_ARG_OR_ASSIGN = re.compile(
    r"(?:[(,]"
    r"|\b(?:cls|class|className|classes|classList)\s*\+?="
    r"|\b(?:cls|class|className|classes)\s*:)\s*$")


def _bare_literal_is_class_bearing(text: str, start: int) -> bool:
    """True where the literal opening at `start` sits where a class is passed."""
    return bool(_ARG_OR_ASSIGN.search(text[max(0, start - 40):start]))


#: A DOT IS A SELECTOR ONLY INSIDE A SELECTOR (Copilot review of openxFactory
#: #1068, round 5). Reading `\.token` out of ANY string literal made every
#: dotted route, module specifier, filename and sentence a class declaration:
#: `"/api/gate.css"` handed the gate `css`, `"./helpers.js"` handed it `js`,
#: `"gate.lens: ctx.model."` handed it `lens` and `model`, `"proposal.md"`
#: handed it `md`. MEASURED over openXdox-code `0a0265f7`'s six contributed
#: modules: the old rule found 14 dotted tokens, and 13 of them were of exactly
#: that kind. Two conditions now hold together, and both are things a selector
#: satisfies by construction:
#:   SHAPE — the whole literal is on the selector alphabet. A path or a URL
#:           carries `/`, which no selector outside an attribute value does, and
#:           a sentence carries punctuation and stops.
#:   POSITION — the `.` does not follow an identifier character. `.gatebar` and
#:           `.a .b` are selectors; `gate.lens` and `error.foo` are a view id
#:           and a message, and `div.foo` is the one real selector form this
#:           refuses — a loss in the SAFE direction, since under-reading the
#:           gate side KEEPS a rule in openDox (the asymmetry `extract_class`
#:           is built on). MEASURED: what leaves is unchanged — 54
#:           gate-exclusive classes, 59 exclusive blocks, 89 lines, the same 59
#:           selectors at the same extents. `g` (from `"e.g. Field Pilots"`,
#:           `gate-projects.js`) and `lens` (from `"gate.lens: …"`, a view id)
#:           stop being counted shared, which is the finding biting.
_SELECTOR_SHAPED = re.compile(r"^[A-Za-z0-9_\-.#>+~*:\[\]=\"',()\s]+$")

#: AND SHAPE ALONE IS NOT SELECTORHOOD (Copilot review of openxFactory #1068,
#: round 7). `showError("see .gatebar")` is on the selector alphabet from end
#: to end — letters, a space and a dot — so the shape test passed it and
#: `.gatebar` was read as a selector: an ordinary message in a contributed
#: module could MOVE an openDox rule, which is the one error the gate side of
#: this census is built to refuse.
#:
#: THE MISSING CONDITION is the one a selector satisfies by construction and
#: prose does not: a bare word in a selector can only be a TYPE SELECTOR, and
#: a type selector is an ELEMENT NAME. `see`, `expected` and `commission` are
#: not element names; `div`, `h2` and `button` are, so `h2 .gate-title` and
#: `button.gatebar` are read exactly as before (the latter still naming
#: nothing, by the element-qualified rule). Anything led by `.`, `#`, `[`,
#: `*`, `:` or a combinator is selector text on its face and is not asked.
#:
#: MEASURED at openDox-code `0b4e8bbf` / openXdox-code `0a0265f7`: the census
#: is UNCHANGED — 54 gate-exclusive classes, 18 shared, 59 exclusive blocks,
#: 89 lines, 10 reading a token — so nothing this tool reports today rests on
#: a dotted sentence. The rule is narrowed anyway, because "no message in this
#: tree happens to carry a dotted word" is not a guarantee about the next one.
#: AND A SELECTOR IS WHAT A SELECTOR API IS GIVEN (Copilot review of
#: openxFactory #1068, round 8). Shape and element names still leave
#: `showError(".gatebar")` — a DIAGNOSTIC MESSAGE that happens to be written as
#: a selector — claiming a class on the side of the census where a claim MOVES
#: an openDox rule. The branch now asks for the context as well: the literal
#: must be the argument of an API that takes a selector.
#:
#: MEASURED over the 44 scanned files at `0b4e8bbf` / `0a0265f7`: EVERY
#: selector-shaped literal that yields a class token on the gate side sits at
#: `querySelector`, `querySelectorAll` or `closest` — 6 in `wheel.js`, 2 in
#: `doc-wheel.js`, 2 in `viewer.js`, and one each in `dispose.js`, `lens.js`,
#: `app.js` and the rest — so the census is UNCHANGED by the requirement. What
#: it refuses are the literals that reach this branch from a concatenation or a
#: message, which is the whole finding.
_SELECTOR_CALL = re.compile(
    r"\b(?:querySelector|querySelectorAll|closest|matches)\??\.?\(\s*$")

_HTML_ELEMENTS = frozenset("""
a abbr address area article aside audio b base bdi bdo blockquote body br
button canvas caption cite code col colgroup data datalist dd del details dfn
dialog div dl dt em embed fieldset figcaption figure footer form h1 h2 h3 h4
h5 h6 head header hgroup hr html i iframe img input ins kbd label legend li
link main map mark menu meta meter nav noscript object ol optgroup option
output p picture pre progress q rp rt ruby s samp script search section select
slot small source span strong style sub summary sup table tbody td template
textarea tfoot th thead time title tr track u ul var video wbr
""".split())
_IDENT = re.compile(r"[A-Za-z0-9_-]+")
_CLASS_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_-]*")


def selector_class_tokens(selector: str) -> set[str]:
    """The CLASS tokens of a selector, walked left to right.

    A regex with a "not after an identifier character" lookbehind got
    `.foo.bar` wrong — the second dot follows `o`, so only `foo` came back
    (Copilot review of openxFactory #1068, round 6), and a gate module using a
    compound selector would have had its rule read as mixed and kept. The walk
    below carries the one bit a lookbehind cannot: WHETHER THE IDENTIFIER RUN
    JUST CONSUMED WAS ITSELF A CLASS. `.foo.bar` is two classes; `div.foo` is
    an element and a class, and `gate.lens` / `error.foo` / `proposal.md` are a
    view id, a message and a filename — none of them selectors.

    WHAT IS NOT PART OF THE COMPOUND IS REMOVED FIRST, AND WITHOUT LEAVING A
    GAP — attribute selectors, IDs, pseudo-classes and pseudo-elements, each
    for the same reason and each found by a review round:

    * `[data-state=".gatebar"]` is an attribute VALUE and not a class (round
      5), and blanking it to a SPACE turned `div[x].gatebar` into
      `div .gatebar`, which reads as a compound the element-qualified rule
      refuses (round 12). Removed outright, the two spell the same thing.
    * `:hover` (round 7) and `#id` (round 9) do not break a compound —
      `.foo:hover.bar` and `.foo#id.bar` are two classes each — and do not MAKE
      one either: `div:hover.foo` and `div#id.foo` stay element-qualified.
    * A PSEUDO-FUNCTION'S ARGUMENT IS A SELECTOR OF ITS OWN (round 14). Walking
      it inline let `div:not(.bar).foo` accept `.foo`, because `.bar` set the
      compound bit for a compound it is not in. The argument is parsed
      SEPARATELY — its classes are still named, since the module does name
      them — and what remains at the top level is `div.foo`, refused.

    A descendant combinator survives all of this, because its space sits
    outside the brackets and parentheses that are removed.
    """
    text = _without_attribute_selectors(selector)
    out: set[str] = set()

    # Pseudo parts out (arguments parsed on their own), then IDs out.
    stripped: list[str] = []
    i, n = 0, len(text)
    while i < n:
        m = re.match(r"::?[A-Za-z-]+", text[i:])
        if m:
            j = i + m.end()
            if j < n and text[j] == "(":
                depth, k = 1, j + 1
                while k < n and depth:
                    if text[k] == "(":
                        depth += 1
                    elif text[k] == ")":
                        depth -= 1
                    k += 1
                out |= selector_class_tokens(text[j + 1:k - 1])
                i = k
            else:
                i = j
            continue
        if text[i] == "#":
            name = _IDENT.match(text, i + 1)
            i = name.end() if name else i + 1
            continue
        stripped.append(text[i])
        i += 1
    text = "".join(stripped)

    i, n, prev_was_class = 0, len(text), False
    while i < n:
        ch = text[i]
        if ch == ".":
            name = _CLASS_NAME.match(text, i + 1)
            starts_here = i == 0 or not _IDENT.match(text[i - 1]) or prev_was_class
            if name and starts_here:
                out.add(name.group(0))
                prev_was_class = True
                i = name.end()
                continue
            prev_was_class = False
            i = name.end() if name else i + 1
            continue
        run = _IDENT.match(text, i)
        if run:
            prev_was_class = False
            i = run.end()
            continue
        i += 1
    return out


def is_selector_text(s: str) -> bool:
    """True where `s` could only be selector text — see `_HTML_ELEMENTS`.

    Every whitespace- or combinator-separated piece that BEGINS with a bare
    word must begin with an element name. A piece led by `.`, `#`, `[`, `*`,
    `:` or nothing at all is selector text on its face.
    """
    for piece in re.split(r"[\s,>+~]+", s):
        head = re.match(r"[A-Za-z][A-Za-z0-9-]*", piece)
        if head and head.group(0).lower() not in _HTML_ELEMENTS:
            return False
    return True


_TAG_OPEN = re.compile(r"<[A-Za-z][A-Za-z0-9-]*")

#: Elements whose CONTENT is text and not markup. A `class="…"` inside one of
#: these is a string the page displays or runs, never an attribute it applies.
_RAW_TEXT_ELEMENTS = frozenset({"script", "style", "textarea", "title"})


def markup_class_runs(s: str, group: str, unquoted: str) -> list[str]:
    """The `class="…"` runs of `s` THAT SIT INSIDE AN HTML TAG.

    `class=` ANYWHERE IN A STRING IS NOT MARKUP (Copilot review of
    openxFactory #1068, round 7, thread `PRRT_kwDOTAvnrs6jCcPV`). The scans
    below read a `class="…"` run as class-bearing by construction, which is
    true of a template that writes markup and false of a message that talks
    about one: `const message = 'expected class="dispose-"'` registered
    `dispose-` as a concatenation PREFIX, and on the gate's narrow prefix
    table a prefix claims every declared class beginning with it — 20-odd
    `dispose-*` rules, moved by a sentence.

    The condition is the markup itself: an unclosed `<tag` must open before
    the `class`, with no `>` between them, which is exactly where an attribute
    can sit. A literal whose opening tag is in a DIFFERENT literal (markup
    concatenated in pieces) is read as prose — under-reading the gate side,
    which KEEPS a rule, the direction this tool errs in on purpose.

    MEASURED at openDox-code `0b4e8bbf` / openXdox-code `0a0265f7`: the census
    is UNCHANGED — 54 / 18 / 59 blocks / 89 lines — because every `class=` in
    these six modules and this bundle is written inside its own tag.
    """
    live = _tag_name_positions(s)
    return [next(g for g in m.groups() if g is not None)
            for m in _CLASS_ATTR(group, unquoted).finditer(s)
            if live[m.start()]]


def _CLASS_ATTR(group: str, group_unquoted: str) -> re.Pattern[str]:
    """`class="…"`, `class='…'` or `class=…`, and NOT `data-class=…`.

    TWO CORRECTIONS, both Copilot review of openxFactory #1068, round 9:
    a SINGLE-QUOTED attribute is as valid as a double-quoted one and was
    skipped (`<div class='gatebar'>` named nothing, so a gate-owned rule would
    have been left behind), and `class` must be a WHOLE ATTRIBUTE NAME —
    `<div data-class="gatebar">` matched on its suffix and claimed a class the
    template never applies, which on the gate side MOVES a rule.
    """
    # QUOTED AND UNQUOTED ARE DIFFERENT GRAMMARS (Copilot review, round 10):
    # with one optional quote, `<i class=gatebar data-state=summary>` captured
    # `gatebar data-state`, because the class alphabet includes the space that
    # ENDS an unquoted value — and a false token on the gate side moves a rule.
    # An unquoted value stops at whitespace (and at `>`); a quoted one runs to
    # its own quote.
    return re.compile(
        rf'(?<![A-Za-z0-9_-])class\s*=\s*'
        rf'(?:"({group})|\'({group})|({group_unquoted}))')


def _tag_name_positions(s: str) -> list[bool]:
    """Which offsets of `s` sit where an ATTRIBUTE NAME can be written.

    AND `class=` INSIDE ANOTHER ATTRIBUTE'S VALUE IS THAT ATTRIBUTE'S (Copilot
    review of openxFactory #1068, round 8). A `rfind("<")` plus "no `>` in
    between" test says yes to `<div title='class="gatebar"'>`, where `class=`
    is part of the TITLE — and a false class run on the gate side moves an
    openDox rule. The tag is walked instead, with quote state carried, so an
    offset counts only where it is inside an open tag AND outside every quoted
    value. `>` inside a quoted value no longer closes the tag either, which the
    substring test also got wrong.
    """
    live = [False] * (len(s) + 1)
    i, n = 0, len(s)
    while i < n:
        # A COMMENT IS NOT MARKUP, AND NEITHER IS RAW TEXT (Copilot review,
        # round 16): `<!-- <div class="gatebar"> -->` and a `<script>` body
        # carrying the same string were walked as live tags, so a class the
        # page never applies was named — and on the gate side that MOVES a
        # rule.
        if s.startswith("<!--", i):
            j = s.find("-->", i + 4)
            i = n if j < 0 else j + 3
            continue
        m = _TAG_OPEN.match(s, i)
        if m:
            j, quote = i + 1, ""
            while j < n:
                c = s[j]
                if quote:
                    if c == quote:
                        quote = ""
                elif c in "\"'":
                    quote = c
                elif c == ">":
                    break
                else:
                    live[j] = True
                j += 1
            i = j + 1
            name = m.group(0)[1:].lower()
            if name in _RAW_TEXT_ELEMENTS:
                close = re.compile(rf"</{re.escape(name)}\b",
                                   re.I).search(s, i)
                i = close.start() if close else n
            continue
        i += 1
    return live


def js_class_spans(text: str) -> list[tuple[str, int]]:
    """Every string literal, AND every contiguous `+` chain of them.

    THE CHAIN RULE REACHES BOTH SCANS (Copilot review of openxFactory #1068,
    round 14). Round 10 taught the BROAD scan that `"ga" + "te" + "bar"` writes
    `gatebar`, but the class-bearing scans still read one literal at a time, so
    a contributed module writing `el("div", "ga" + "te" + "bar")` named no
    class and `"dispose" + "-" + outcome` registered no prefix — a gate-owned
    block would have been left in openDox's sheet as unreferenced.

    Each chain is reported at the offset of its FIRST literal, which is where
    the whole expression sits, so `_bare_literal_is_class_bearing` asks its
    question about the position the value is written into.
    """
    spans = [(a, b) for kind, a, b in _js_spans(text) if kind == "string"]
    out = [(text[a + 1:b - 1], a) for a, b in spans]
    run: list[tuple[int, int]] = []

    def flush() -> None:
        for i in range(len(run)):
            for j in range(i + 2, len(run) + 1):
                out.append(("".join(text[a + 1:b - 1] for a, b in run[i:j]),
                            run[i][0]))
        run.clear()

    for k, (a, b) in enumerate(spans):
        if run and not _is_concatenation(text, spans[k - 1][1], a):
            flush()
        run.append((a, b))
    flush()
    return out


def prefix_refs(text: str, suffix: str, *,
                class_bearing_only: bool = False) -> set[str]:
    """Every class-name PREFIX this file concatenates onto.

    `class_bearing_only` puts prefixes under THE SAME ASYMMETRY the token scans
    already obey (Copilot review of openxFactory #1068, round 5): an ungated
    prefix rule let any hyphen-terminated word in any string — `"status-"` in a
    sentence, a route fragment — claim every declared class starting with it,
    and on the GATE side that claim MOVES an openDox rule. Gated, a prefix
    counts only from a `class="…"` run (class-bearing by construction, which is
    how a template writes one) or from a literal in argument/assignment
    position AND ITSELF A BARE CLASS LIST — the same two conditions
    `narrow_refs` puts on a bare literal, so the prefix rule and the token rule
    agree about what a class-bearing literal is. The openDox side stays
    ungated, because over-reading there only
    KEEPS a rule — the same direction the broad token scan errs in.
    """
    out: set[str] = set()
    if suffix == ".js":
        spans = js_class_spans(text)
    else:
        spans = [(run, 0) for run in
                 markup_class_runs(text, r"[A-Za-z0-9_ -]*", r"[A-Za-z0-9_-]*")]

    def register(piece: str) -> None:
        m = _PREFIX.match(piece)
        if m:
            out.add(m.group(1))

    for s, start in spans:
        # A `class="…"` run INSIDE A TAG is class-bearing either way; one in
        # ordinary prose is prose — see `markup_class_runs`. (An `index.html`
        # span is an attribute VALUE already, so it carries no `class=` of its
        # own and this loop is the JavaScript side's.)
        for run in markup_class_runs(s, r"[A-Za-z0-9_ -]*(?:\$\{)?",
                                     r"[A-Za-z0-9_-]*(?:\$\{)?"):
            for piece in run.split():
                register(piece)
        parts = s.split()
        if class_bearing_only and suffix == ".js" and not (
                parts and all(_CLASSTOK.match(q) for q in parts)
                and _bare_literal_is_class_bearing(text, start)):
            continue
        for piece in parts:
            register(piece)
    return out


def narrow_refs(text: str, suffix: str) -> set[str]:
    """Every class token `text` names in a class-bearing position."""
    out: set[str] = set()
    if suffix == ".js":
        spans = js_class_spans(text)
    else:
        spans = [(run, 0) for run in
                 markup_class_runs(text, r"[A-Za-z0-9_ -]*", r"[A-Za-z0-9_-]*")]
    for s, start in spans:
        # A SELECTOR STRING is class-bearing wherever it sits — but it has to
        # BE a selector: SHAPE (`_SELECTOR_SHAPED`), a bare word only where an
        # element name can stand (`is_selector_text`), and the dot's own
        # position (`selector_class_tokens`). All three, or a sentence with a
        # dotted word in it moves an openDox rule.
        stripped = s.strip()
        if stripped and _SELECTOR_SHAPED.match(stripped) \
                and is_selector_text(stripped) \
                and (suffix != ".js" or _SELECTOR_CALL.search(text[max(0, start - 60):start])):
            out.update(selector_class_tokens(stripped))
        # A `class="…"` INSIDE A TAG is class-bearing by construction; one in
        # prose is prose (`markup_class_runs`).
        for run in markup_class_runs(s, r"[A-Za-z0-9_ -]*", r"[A-Za-z0-9_-]*"):
            out.update(p for p in run.split() if _CLASSTOK.match(p))
        # A BARE class list only where a class is PASSED or ASSIGNED.
        parts = s.split()
        if not parts or not all(_CLASSTOK.match(p) for p in parts):
            continue
        if suffix != ".js" or _bare_literal_is_class_bearing(text, start):
            out.update(parts)
    return out


# --------------------------------------------------------------------------
# The stylesheet, parsed into RULE BLOCKS with their line extents.
# --------------------------------------------------------------------------
_TOKEN = re.compile(r"\.([A-Za-z_][A-Za-z0-9_-]*)")


def _blank_comments(css: str) -> str:
    """The scan copy: COMMENTS AND STRINGS blanked, every newline kept.

    Strings are blanked for the same reason comments are, and the omission was
    a real defect (Copilot review of openxFactory #1068, round 5): the brace
    walk below counts `{` and `}` characters, and a declaration as ordinary as
    `content: "}"` or `content: "{"` moved the count inside a string — closing
    the block early or swallowing the rules after it, and every line extent
    from there on would be wrong. Blanking preserves OFFSETS and LINES exactly,
    so `line_of` and every `css[...]` slice still read the real file.
    """
    out, i, n = [], 0, len(css)
    while i < n:
        if css[i] == "/" and i + 1 < n and css[i + 1] == "*":
            j = css.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append(re.sub(r"[^\n]", " ", css[i:j]))
            i = j
            continue
        if css[i] in "\"'":
            quote, j = css[i], i + 1
            while j < n:
                if css[j] == "\\":
                    j += 2; continue
                if css[j] == quote or css[j] == "\n":   # CSS strings do not span lines
                    break
                j += 1
            j = min(j + 1, n)
            out.append(re.sub(r"[^\n]", " ", css[i:j]))
            i = j
            continue
        out.append(css[i]); i += 1
    return "".join(out)


def parse_blocks(css: str) -> list[dict]:
    """Every rule block, with its at-rule ancestry and 1-based line extent.

    A block is `{selector, at_rule, start, end, body}` where `start`/`end` are
    the first and last line of the whole construct AS IT SITS IN THE FILE
    (a nested rule's extent is its own, never its `@media`'s).
    """
    scan = _blank_comments(css)
    blocks: list[dict] = []
    stack: list[str] = []
    i, n, seg_start = 0, len(scan), 0

    def line_of(off: int) -> int:
        return css.count("\n", 0, off) + 1

    while i < n:
        c = scan[i]
        if c == "{":
            prelude = scan[seg_start:i].strip()
            pre_off = seg_start + (len(scan[seg_start:i]) - len(scan[seg_start:i].lstrip()))
            depth, j = 1, i + 1
            while j < n and depth:
                if scan[j] == "{":
                    depth += 1
                elif scan[j] == "}":
                    depth -= 1
                j += 1
            inner = scan[i + 1:j - 1]
            if prelude.startswith("@") and "{" in inner:
                stack.append(prelude)
                blocks.extend(parse_nested(css, scan, i + 1, j - 1, prelude, line_of))
                stack.pop()
                blocks.append({"selector": prelude, "at_rule": None,
                               "kind": "at_rule_wrapper",
                               "start": line_of(pre_off), "end": line_of(j - 1),
                               "body": css[i + 1:j - 1]})
            else:
                blocks.append({"selector": prelude, "at_rule": None,
                               "kind": "rule",
                               "start": line_of(pre_off), "end": line_of(j - 1),
                               "body": css[i + 1:j - 1]})
            i = j
            seg_start = j
            continue
        if c == ";" :
            seg_start = i + 1
        i += 1
    return blocks


def parse_nested(css: str, scan: str, lo: int, hi: int, at_rule: str,
                 line_of) -> list[dict]:
    """The rules inside an at-rule — RECURSIVELY, at every depth.

    A single level was a real defect (Copilot review of openxFactory #1068,
    round 5): `@media … { @supports (…) { .gatebar { … } } }` recorded the
    `@supports` prelude AS A RULE and never emitted `.gatebar`, so an exclusive
    block nested two deep would be missed and left in the wrong leg. The
    ancestry is kept as the at-rule preludes joined, so a nested block reports
    WHERE it sits as well as what it is.
    """
    out: list[dict] = []
    i, seg_start = lo, lo
    while i < hi:
        if scan[i] == "{":
            prelude = scan[seg_start:i].strip()
            pre_off = seg_start + (len(scan[seg_start:i]) - len(scan[seg_start:i].lstrip()))
            depth, j = 1, i + 1
            while j < hi + 1 and depth:
                if scan[j] == "{":
                    depth += 1
                elif scan[j] == "}":
                    depth -= 1
                j += 1
            if prelude.startswith("@") and "{" in scan[i + 1:j - 1]:
                out.extend(parse_nested(css, scan, i + 1, j - 1,
                                        f"{at_rule} {prelude}", line_of))
                out.append({"selector": prelude, "at_rule": at_rule,
                            "kind": "at_rule_wrapper",
                            "start": line_of(pre_off), "end": line_of(j - 1),
                            "body": css[i + 1:j - 1]})
            else:
                out.append({"selector": prelude, "at_rule": at_rule,
                            "kind": "rule",
                            "start": line_of(pre_off), "end": line_of(j - 1),
                            "body": css[i + 1:j - 1]})
            i = j
            seg_start = j
            continue
        if scan[i] == ";":
            seg_start = i + 1
        i += 1
    return out


def _without_attribute_selectors(selector: str) -> str:
    """`selector` with every `[…]` removed, QUOTES AND ESCAPES RESPECTED.

    `re.sub(r"\\[[^\\]]*\\]", …)` closes at the first `]` wherever it sits,
    so `[data-label="x] .gatebar"]` was reduced to text carrying `.gatebar`
    and the census invented a class selector for a rule that has none
    (Copilot review of openxFactory #1068, round 15). An attribute value is a
    CSS string and ends at its own quote.

    Removed rather than blanked, because an attribute is part of the compound
    (round 12): `div[x].gatebar` must read as `div.gatebar` and not as
    `div .gatebar`. A descendant combinator keeps its space, which sits
    outside the brackets.
    """
    out, i, n = [], 0, len(selector)
    while i < n:
        if selector[i] == "[":
            j, quote = i + 1, ""
            while j < n:
                c = selector[j]
                if c == "\\":
                    j += 2
                    continue
                if quote:
                    if c == quote:
                        quote = ""
                elif c in "\"'":
                    quote = c
                elif c == "]":
                    break
                j += 1
            i = min(j + 1, n)
            continue
        out.append(selector[i])
        i += 1
    return "".join(out)


def _selector_branches(selector: str) -> list[str]:
    """A selector LIST, split at its top-level commas.

    A comma inside `[…]` or `:not(…)` is not a branch separator, which is why
    this is a walk and not `selector.split(",")`.
    """
    out: list[str] = []
    depth, cur = 0, []
    for ch in selector:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    return [part.strip() for part in out if part.strip()]


def _outside_pseudo_functions(selector: str) -> str:
    """`selector` with every `:pseudo(…)` argument removed, nesting included.

    What is left is what the branch SELECTS ON at the top level. A class inside
    `:not(…)`, `:is(…)` or `:where(…)` is a condition on the match, not the
    hook the rule is anchored by, and the two must not be confused where the
    answer decides whether a block leaves the bundle.
    """
    out, i, n = [], 0, len(selector)
    while i < n:
        m = re.match(r"::?[A-Za-z-]+\(", selector[i:])
        if m:
            depth, j = 1, i + m.end()
            while j < n and depth:
                if selector[j] == "(":
                    depth += 1
                elif selector[j] == ")":
                    depth -= 1
                j += 1
            i = j
            continue
        out.append(selector[i])
        i += 1
    return "".join(out)


def selector_tokens(selector: str) -> dict:
    """What a selector list is MADE of — the census's whole discrimination.

    ATTRIBUTE VALUES ARE NOT SELECTOR TEXT, and reading class tokens before
    removing them was a real defect (Copilot review of openxFactory #1068,
    round 5): `[data-state=".gatebar"]` yielded the class `gatebar`, so a rule
    with no class selector at all could be classified gate-exclusive and
    extracted. `[...]` goes first now, for classes as it already did for
    elements.
    """
    outside = _without_attribute_selectors(selector)
    classes = sorted(set(_TOKEN.findall(outside)))
    without = _TOKEN.sub(" ", outside)
    ids = sorted(set(re.findall(r"#([A-Za-z_][A-Za-z0-9_-]*)", without)))
    without = re.sub(r"#[A-Za-z_][A-Za-z0-9_-]*", " ", without)
    without = re.sub(r"::?[A-Za-z-]+(\([^)]*\))?", " ", without)
    elements = sorted({t for t in re.findall(r"[A-Za-z][A-Za-z0-9-]*", without)})
    return {"classes": classes, "ids": ids, "elements": elements}


def main() -> int:
    dox = Path(sys.argv[1]).resolve()
    xdox = Path(sys.argv[2]).resolve()
    out_json = None
    if "--json" in sys.argv:
        out_json = Path(sys.argv[sys.argv.index("--json") + 1])

    web = dox / "src" / "opendox" / "web"
    css_path = web / "styles.css"
    # READ AFTER THE PATH CHECKS BELOW (Copilot review, round 10): reading
    # here turned a missing or mistyped openDox checkout into an unhandled
    # `FileNotFoundError` traceback, where a missing contributed-module
    # directory gets the named refusal this tool is careful about.

    gate_dir = xdox / "src" / "openxdox" / "web" / "views"
    if "--gate-dir" in sys.argv:
        gate_dir = Path(sys.argv[sys.argv.index("--gate-dir") + 1]).resolve()
    # A MISSING CHECKOUT IS A REFUSAL, NOT A ZERO (Copilot review, round 5).
    # `glob` on a path that does not exist yields nothing, and the run would
    # report `0 gate-exclusive classes, 0 blocks` — a mistyped argument reading
    # as a measured "nothing to extract", which is the worst answer this tool
    # can give: it is the same output a COMPLETED extraction produces.
    # `web/views` IS CHECKED TOO (Copilot review, round 6): openDox's own view
    # modules live there, and a missing subdirectory globs to nothing — so
    # every class only openDox's views name would read as named by nobody, and
    # a gate class would look exclusive when it is shared. The openDox side is
    # the side that KEEPS rules; an empty scan of it is the unsafe emptiness.
    for label, path in (("openDox-code's served bundle", web),
                        ("openDox-code's own view modules", web / "views"),
                        ("openXdox-code's contributed modules", gate_dir)):
        if not path.is_dir():
            raise SystemExit(
                f"{label}: {path} is not a directory. This tool measures TWO "
                "checkouts, and a path that is not there yields an empty scan "
                "and a census of zero — indistinguishable from a bundle with "
                "nothing left to extract")
    # AND THE STYLESHEET ITSELF IS A NAMED REFUSAL TOO. The BYTES are what the
    # floor counts lines in, the text is what the parser walks; read once, so
    # the two cannot be of different revisions.
    if not css_path.is_file():
        raise SystemExit(
            f"openDox-code's served stylesheet: {css_path} is not a file. "
            "This tool measures a stylesheet against two checkouts, and a "
            "missing one is a mistyped path, never an empty census")
    css_bytes = css_path.read_bytes()
    css = css_bytes.decode("utf-8")
    # AND SO ARE THE TWO FILES THE BUNDLE ALWAYS HAS (Copilot review, round
    # 11): `app.js` and `index.html` are added unconditionally below, so a
    # checkout missing either passed every check above and then raised
    # `FileNotFoundError` out of `haystack`.
    for label, path in (("openDox-code's shell module", web / "app.js"),
                        ("openDox-code's served page", web / "index.html")):
        if not path.is_file():
            raise SystemExit(
                f"{label}: {path} is not a file. Both are read as openDox's "
                "own side of the census, and a bundle without one is an "
                "incomplete checkout, never a bundle that names nothing")
    gate_files = sorted(p for p in gate_dir.glob("*.js"))
    if not gate_files:
        raise SystemExit(
            f"{gate_dir} carries no `.js` file. The contributed modules are "
            "what the gate side of this census is measured FROM; an empty set "
            "reports every class as openDox's own and no block as leaving")
    #: A gate module is NEVER counted on openDox's side of the census, wherever
    #: it physically sits. Before slice S5 landed the six lived in openDox's own
    #: `views/`, so a name-blind sweep would call every gate class `shared` and
    #: the tool would answer differently at `cb343ae8` for a reason that is not
    #: about the stylesheet at all.
    gate_names = {p.name for p in gate_files}
    dox_files = [web / "app.js", web / "index.html"] + sorted(
        p for p in (web / "views").glob("*.js") if p.name not in gate_names)

    def haystack(path: Path) -> str:
        text = path.read_text(encoding="utf-8", errors="replace")
        if path.suffix == ".js":
            return js_literal_text(text)
        return text                      # index.html: attributes are the hooks

    gate_text = {p.name: haystack(p) for p in gate_files}
    dox_text = {p.name: haystack(p) for p in dox_files}
    gate_narrow = {p.name: narrow_refs(p.read_text(encoding="utf-8",
                                                   errors="replace"), p.suffix)
                   for p in gate_files}
    dox_narrow = {p.name: narrow_refs(p.read_text(encoding="utf-8",
                                                  errors="replace"), p.suffix)
                  for p in dox_files}
    gate_prefix = {p.name: prefix_refs(p.read_text(encoding="utf-8",
                                                   errors="replace"), p.suffix)
                   for p in gate_files}
    dox_prefix = {p.name: prefix_refs(p.read_text(encoding="utf-8",
                                                  errors="replace"), p.suffix)
                  for p in dox_files}
    # The NARROW prefix table, for the side of the decision where an
    # over-reading moves a rule. See `prefix_refs`' own note.
    gate_prefix_narrow = {p.name: prefix_refs(p.read_text(encoding="utf-8",
                                                          errors="replace"),
                                              p.suffix, class_bearing_only=True)
                          for p in gate_files}

    def by_prefix(token: str, table: dict[str, set[str]]) -> list[str]:
        return sorted(n for n, ps in table.items()
                      if any(token.startswith(p) for p in ps))

    blocks = parse_blocks(css)
    rules = [b for b in blocks if b["kind"] == "rule"]
    declared = sorted({t for b in rules for t in selector_tokens(b["selector"])["classes"]})

    def namers(token: str, corpus: dict[str, str]) -> list[str]:
        pat = re.compile(rf"(?<![A-Za-z0-9_-]){re.escape(token)}(?![A-Za-z0-9_-])")
        return [name for name, text in corpus.items() if pat.search(text)]

    def classify(g: list[str], d: list[str]) -> str:
        if g and not d:
            return "gate_exclusive"
        if g and d:
            return "shared"
        return "opendox_only" if d else "unreferenced"

    census: dict[str, dict] = {}
    for token in declared:
        pg, pd = by_prefix(token, gate_prefix), by_prefix(token, dox_prefix)
        png = by_prefix(token, gate_prefix_narrow)
        g = sorted(set(namers(token, gate_text)) | set(pg))
        d = sorted(set(namers(token, dox_text)) | set(pd))
        ng = sorted({n for n, s in gate_narrow.items() if token in s} | set(png))
        nd = sorted({n for n, s in dox_narrow.items() if token in s} | set(pd))
        # THE EXTRACTION DECISION IS ASYMMETRIC, ON PURPOSE (Copilot review of
        # openxFactory #1068, round 3). It reads the GATE side NARROW and the
        # openDox side BROAD, because the two errors are not the same error:
        # over-including on openDox's side KEEPS a rule, and over-including on
        # the gate's side MOVES one. A label, route or message string that
        # happens to equal a selector token must not be able to send an
        # openDox rule to another leg, so only a CLASS-BEARING position (and a
        # concatenation prefix) counts as the gate naming a class.
        #
        # MEASURED: at openDox-code `0b4e8bbf` / openXdox-code `0a0265f7` this
        # asymmetric rule and the all-broad one both answer 54 — the finding
        # has no effect on this tree, and the rule is narrowed anyway because
        # "it happens not to bite here" is not a guarantee.
        census[token] = {"class": classify(g, d), "gate": g, "opendox": d,
                         "narrow_class": classify(ng, nd),
                         "narrow_gate": ng, "narrow_opendox": nd,
                         "extract_class": classify(ng, d),
                         "by_concatenation": bool(pg or pd)}

    def block_class(b: dict) -> str:
        t = selector_tokens(b["selector"])
        if not t["classes"]:
            return "no_class"
        # `extract_class`, not `class`: the gate side read NARROW so a stray
        # literal cannot move an openDox rule, the openDox side read BROAD so
        # any mention at all keeps one. See the note where it is computed.
        kinds = {census[c]["extract_class"] for c in t["classes"] if c in census}
        # AND EVERY BRANCH OF THE LIST MUST BE ANCHORED BY A CLASS (Copilot
        # review of openxFactory #1068, round 11). `selector_tokens` aggregates
        # over the WHOLE list, so `.gatebar, button { … }` read as
        # gate-exclusive on the strength of `.gatebar` alone — and extracting
        # it would have taken openDox's generic `button` styling to another
        # leg. A branch with no class of its own (`button`, `:root`,
        # `[hidden]`) styles something this census cannot attribute, so the
        # block stays.
        # AND THE ANCHOR MUST BE A TOP-LEVEL CLASS (Copilot review, round 12):
        # `:not(.gatebar)` carries a class token but applies to nearly every
        # element, so counting it as the branch's anchor let a rule that styles
        # the whole page leave on the strength of what it EXCLUDES.
        branches = _selector_branches(b["selector"])
        # …AND IT ASKS THE CONSERVATIVE WALKER (Copilot review, round 15).
        # `selector_tokens` reports every class token the selector carries,
        # which is what `kinds` wants; the ANCHOR question is the narrower one
        # `selector_class_tokens` answers, where `div[data-state].gatebar` is
        # element-qualified and names nothing. Asking the wide one here let the
        # decision extract exactly the form the position rule refuses.
        anchored = bool(branches) and all(
            selector_class_tokens(_outside_pseudo_functions(part))
            for part in branches)
        if kinds == {"gate_exclusive"} and not t["ids"] and anchored:
            return "exclusive"
        if "gate_exclusive" in kinds or "shared" in kinds:
            return "mixed"
        return "opendox"

    for b in rules:
        b["tokens"] = selector_tokens(b["selector"])
        # A COMMENT IS NOT A DEPENDENCY (Copilot review of openxFactory #1068,
        # round 5): `/* var(--st-proposed) */` or a commented-out `--st-x:`
        # declaration was reported as a live design-token use, which is the
        # same mistake the selector parser was written to avoid one function
        # up. The same blanking pass answers both.
        live = _blank_comments(b["body"])
        b["reads_st_token"] = bool(re.search(r"var\(\s*--st-", live))
        # A DECLARATION BOUNDARY, NOT A LINE START (Copilot review of
        # openxFactory #1068, round 7): `^\s*--st-` saw only a token declared
        # first on its line, and `.gatebar { color: red; --st-proposed: #123 }`
        # is the same declaration written after another. The block was then
        # extractable and the stable surface left with it — the exact failure
        # the flag was added to stop, one comma away. A custom property can
        # begin only at the start of the body or after a `;`, and `{` opens the
        # body of a block whose braces this parser has already balanced.
        b["declares_st_token"] = bool(re.search(r"(?:^|[;{])\s*--st-", live))
        # AND A BLOCK THAT DECLARES A TOKEN NEVER LEAVES — computed BEFORE the
        # classification that reads it (Copilot review, round 6: it used to be
        # computed after, and nothing consulted it, so `.gatebar { --st-x: red }`
        # was an extractable exclusive block). RULED Q7 makes the `--st-*`
        # family openDox's ONE stable styling surface; a rule that DEFINES one
        # is openDox's by that sentence however gate-only its selector reads,
        # and moving it would take the surface with it.
        b["block_class"] = block_class(b)
        if b["block_class"] == "exclusive" and b["declares_st_token"]:
            b["block_class"] = "declares_st_token"

    kinds = ("gate_exclusive", "shared", "opendox_only", "unreferenced")
    counts = {k: sum(1 for v in census.values() if v["class"] == k) for k in kinds}
    extract_counts = {k: sum(1 for v in census.values() if v["extract_class"] == k)
                      for k in kinds}
    narrow_counts = {k: sum(1 for v in census.values() if v["narrow_class"] == k)
                     for k in kinds}
    exclusive_blocks = [b for b in rules if b["block_class"] == "exclusive"]
    mixed_blocks = [b for b in rules if b["block_class"] == "mixed"]
    token_declaring_blocks = [b for b in rules
                              if b["block_class"] == "declares_st_token"]

    report = {
        "styles_css": {"path": "src/opendox/web/styles.css",
                       # THE CARVE FLOOR'S LINE, and not this file's own
                       # (Copilot review of openxFactory #1068, rounds 5 and
                       # 7). Round 5's `splitlines()` fixed the real half —
                       # `line_of` numbers a final line that carries no
                       # trailing newline and `count("\n")` does not — but
                       # `splitlines()` also breaks on U+2028, U+2029, `\v`,
                       # `\f`, `\x85` and a lone `\r`, which `line_of` does
                       # not, so a stylesheet carrying one of those would have
                       # reported a total the block extents are not numbered
                       # in. `carve_lines.count` IS `line_of`'s numbering
                       # (`\n`-terminated records, `scripts/carve_lines.py`),
                       # which is also the numbering the manifest declares
                       # this file's 89 lines in.
                       "lines": carve_lines.count(css_bytes),
                       "rule_blocks": len(rules),
                       "declared_class_tokens": len(declared)},
        "gate_modules": [p.name for p in gate_files],
        "opendox_bundle_files": len(dox_files),
        "class_counts_broad": counts,
        "class_counts_extraction": extract_counts,
        "class_counts_narrow": narrow_counts,
        # THE PUBLIC LISTS ARE ONE CLASSIFICATION, NAMED (Copilot review of
        # openxFactory #1068, round 14). `gate_exclusive` came from
        # `extract_class` while `shared` and `unreferenced` came from the BROAD
        # `class`, so the report's own three lists answered two different
        # questions and its `shared` did not match the 18 the manifest cites.
        # All three are `extract_class` now — the classification the extraction
        # DECIDES on — and the broad reading is still published beside them
        # under a name that says which it is.
        "narrow_shared": sorted(t for t, v in census.items()
                                if v["narrow_class"] == "shared"),
        "gate_exclusive": sorted(t for t, v in census.items()
                                 if v["extract_class"] == "gate_exclusive"),
        "shared": sorted(t for t, v in census.items()
                         if v["extract_class"] == "shared"),
        "unreferenced": sorted(t for t, v in census.items()
                               if v["extract_class"] == "unreferenced"),
        "shared_broad": sorted(t for t, v in census.items()
                               if v["class"] == "shared"),
        "unreferenced_broad": sorted(t for t, v in census.items()
                                     if v["class"] == "unreferenced"),
        "exclusive_blocks": [
            {"selector": b["selector"], "at_rule": b["at_rule"],
             "start": b["start"], "end": b["end"],
             "reads_st_token": b["reads_st_token"],
             "declares_st_token": b["declares_st_token"]}
            for b in exclusive_blocks],
        "mixed_blocks": [
            {"selector": b["selector"], "at_rule": b["at_rule"],
             "start": b["start"], "end": b["end"],
             "gate_exclusive_tokens": [c for c in b["tokens"]["classes"]
                                       if census.get(c, {}).get("class") == "gate_exclusive"],
             "shared_tokens": [c for c in b["tokens"]["classes"]
                               if census.get(c, {}).get("class") == "shared"]}
            for b in mixed_blocks],
        # KEPT DESPITE A GATE-ONLY SELECTOR, because the block DECLARES an
        # `--st-*` token (RULED Q7's stable surface). MEASURED at the cited
        # base commits: this list is EMPTY, so the 59 are the 59 — but a later
        # act that gives a gate-only rule a token declaration will see it here
        # instead of in the extraction.
        "blocks_kept_for_declaring_a_token": [
            {"selector": b["selector"], "at_rule": b["at_rule"],
             "start": b["start"], "end": b["end"]}
            for b in token_declaring_blocks],
        # THE UNION OF THE EXTENTS, not the sum (Copilot review, round 10).
        # Two rules can share a physical line (`.a{…} .b{…}` on one line), and
        # the declared-edit window can name that line ONCE — a sum would report
        # an extraction larger than any set of line numbers could express.
        "exclusive_block_lines": len({n for b in exclusive_blocks
                                      for n in range(b["start"], b["end"] + 1)}),
        "exclusive_blocks_reading_st": sum(1 for b in exclusive_blocks if b["reads_st_token"]),
        "census": census,
    }

    print(json.dumps({k: v for k, v in report.items() if k != "census"}, indent=1))
    if out_json:
        out_json.write_text(json.dumps(report, indent=1), encoding="utf-8")
        print(f"\nfull census (with per-token namers) -> {out_json}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
