#!/usr/bin/env python3
"""RE-MEASURE the gate loop's CSS census — RULED Q7 (`opensoft/openxFactory#656`
comment `5648049748`): *"a contributed binding's CSS lives WITH THE BINDING, in
its own sheet; openDox's declared design tokens (the `--st-*` family, S7) are
the one stable styling surface; nothing else in `styles.css` is."*

    measure-css-census.py <opendox-code checkout> <openxdox-code checkout> [--json out.json]

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

# --------------------------------------------------------------------------
# openDox-code tests/test_web_boundary.py's span walk, behaviour-for-behaviour.
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


def js_literal_text(text: str) -> str:
    """Every string literal of a module, concatenated — comments and regexes out."""
    return "\n".join(text[a + 1:b - 1] for kind, a, b in _js_spans(text)
                     if kind == "string")


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
# NARROW — the token appears in a CLASS-BEARING position: after a `.` (a
#          selector string, `div.foo`, `.foo.bar`), inside a `class="…"`
#          attribute of a template literal or of `index.html`, or as one of a
#          literal that is a bare class list. This is what `STYLE_RESIDUE`'s
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
    return (re.findall(r'class\s*=\s*"([^"]*)"', text)
            + re.findall(r"class\s*=\s*'([^']*)'", text))


def prefix_refs(text: str, suffix: str) -> set[str]:
    """Every class-name PREFIX this file concatenates onto."""
    out: set[str] = set()
    for s in _literals(text, suffix):
        for piece in s.split():
            m = _PREFIX.match(piece)
            if m:
                out.add(m.group(1))
    return out


def narrow_refs(text: str, suffix: str) -> set[str]:
    """Every class token `text` names in a class-bearing position."""
    out: set[str] = set()
    if suffix == ".js":
        literals = [text[a + 1:b - 1] for kind, a, b in _js_spans(text)
                    if kind == "string"]
    else:
        literals = (re.findall(r'class\s*=\s*"([^"]*)"', text)
                    + re.findall(r"class\s*=\s*'([^']*)'", text))
    for s in literals:
        out.update(re.findall(r"\.([A-Za-z_][A-Za-z0-9_-]*)", s))
        for m in re.finditer(r'class\s*=\s*"?([A-Za-z0-9_ -]*)', s):
            out.update(p for p in m.group(1).split() if _CLASSTOK.match(p))
        parts = s.split()
        if parts and all(_CLASSTOK.match(p) for p in parts):
            out.update(parts)
    return out


# --------------------------------------------------------------------------
# The stylesheet, parsed into RULE BLOCKS with their line extents.
# --------------------------------------------------------------------------
_TOKEN = re.compile(r"\.([A-Za-z_][A-Za-z0-9_-]*)")


def _blank_comments(css: str) -> str:
    out, i, n = [], 0, len(css)
    while i < n:
        if css[i] == "/" and i + 1 < n and css[i + 1] == "*":
            j = css.find("*/", i + 2)
            j = n if j < 0 else j + 2
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
            out.append({"selector": prelude, "at_rule": at_rule, "kind": "rule",
                        "start": line_of(pre_off), "end": line_of(j - 1),
                        "body": css[i + 1:j - 1]})
            i = j
            seg_start = j
            continue
        if scan[i] == ";":
            seg_start = i + 1
        i += 1
    return out


def selector_tokens(selector: str) -> dict:
    """What a selector list is MADE of — the census's whole discrimination."""
    classes = sorted(set(_TOKEN.findall(selector)))
    without = _TOKEN.sub(" ", selector)
    ids = sorted(set(re.findall(r"#([A-Za-z_][A-Za-z0-9_-]*)", without)))
    without = re.sub(r"#[A-Za-z_][A-Za-z0-9_-]*", " ", without)
    without = re.sub(r"\[[^\]]*\]", " ", without)
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
    css = css_path.read_text(encoding="utf-8")

    gate_dir = xdox / "src" / "openxdox" / "web" / "views"
    if "--gate-dir" in sys.argv:
        gate_dir = Path(sys.argv[sys.argv.index("--gate-dir") + 1]).resolve()
    gate_files = sorted(p for p in gate_dir.glob("*.js"))
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
        g = sorted(set(namers(token, gate_text)) | set(pg))
        d = sorted(set(namers(token, dox_text)) | set(pd))
        ng = sorted({n for n, s in gate_narrow.items() if token in s} | set(pg))
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
        if kinds == {"gate_exclusive"} and not t["ids"]:
            return "exclusive"
        if "gate_exclusive" in kinds or "shared" in kinds:
            return "mixed"
        return "opendox"

    for b in rules:
        b["block_class"] = block_class(b)
        b["tokens"] = selector_tokens(b["selector"])
        b["reads_st_token"] = bool(re.search(r"var\(\s*--st-", b["body"]))
        b["declares_st_token"] = bool(re.search(r"^\s*--st-", b["body"], re.M))

    kinds = ("gate_exclusive", "shared", "opendox_only", "unreferenced")
    counts = {k: sum(1 for v in census.values() if v["class"] == k) for k in kinds}
    extract_counts = {k: sum(1 for v in census.values() if v["extract_class"] == k)
                      for k in kinds}
    narrow_counts = {k: sum(1 for v in census.values() if v["narrow_class"] == k)
                     for k in kinds}
    exclusive_blocks = [b for b in rules if b["block_class"] == "exclusive"]
    mixed_blocks = [b for b in rules if b["block_class"] == "mixed"]

    report = {
        "styles_css": {"path": "src/opendox/web/styles.css",
                       "lines": css.count("\n"),
                       "rule_blocks": len(rules),
                       "declared_class_tokens": len(declared)},
        "gate_modules": [p.name for p in gate_files],
        "opendox_bundle_files": len(dox_files),
        "class_counts_broad": counts,
        "class_counts_extraction": extract_counts,
        "class_counts_narrow": narrow_counts,
        "narrow_shared": sorted(t for t, v in census.items()
                                if v["narrow_class"] == "shared"),
        "gate_exclusive": sorted(t for t, v in census.items()
                                 if v["extract_class"] == "gate_exclusive"),
        "shared": sorted(t for t, v in census.items() if v["class"] == "shared"),
        "unreferenced": sorted(t for t, v in census.items()
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
        "exclusive_block_lines": sum(b["end"] - b["start"] + 1 for b in exclusive_blocks),
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
