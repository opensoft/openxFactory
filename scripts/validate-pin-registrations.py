#!/usr/bin/env python3
"""A pin's REGISTRATION is checked: path, entrypoint, rule — and its citations.

THE GAP THIS CLOSES (issue #776, second assertion).
`publish-openspec-cli-pin-as-contract-member` registered one consumption pin in
`contracts/manifest.yaml` and wrote NO CHECK — its own `tasks.md` § 5.4 says so
in its heading: *a registration is not a check*. The registered row's
`consumption_rule` QUOTES a path (`scripts/validate-openspec-cli-pin.py`); the
pin file NAMES that same path in its own `consumer_entrypoint:` field; and
nothing in this repository compared the two. `design.md` D2 carried that
coupling as DISCLOSED. The only comparison of `consumer_entrypoint:` against
anything in the tree — `tests/proposal-support/test_pinned_openspec_cli.py` —
compares `proposal-support`'s own constant against the PIN, never the MANIFEST
ROW against the pin, and stays green through exactly the failure this file
exists to catch.

THE FAILURE MODE, NAMED. A rename that moved the entrypoint and updated the pin
but not the row's prose — or moved the pin and not the row — leaves the
PUBLISHED register quoting a path that does not exist, silently, to precisely
the audience the register exists for: a cross-repository consumer reading
`contracts/manifest.yaml` to learn how to consume. Declining the row's `sha256`
(D2's stated choice, because the pin moves on every disposition added or
retired) did not remove that coupling; it made it ONE STRING wide instead of one
file wide, and one string is still uncompared.

WHAT CANON REQUIRES, AND NOTHING MORE. `openspec/specs/neutral-product-pin/`'s
promoted requirement *A consumption pin that another repository reads is a
PUBLISHED contract member, adopted by pin-sync* obliges the registration to
carry "an `id`, its `path`, a `type`, its `intended_consumers`,
`adapter_owner: openxFactory`, and a `consumption_rule` that states the
checkout-at-the-pinned-ref recipe"; it fixes the recipe as "check `openxFactory`
out at its own `stack.yaml` `xfactory.contract_ref` and invoke the entrypoint
the registered pin names FROM THAT CHECKOUT"; and it holds that "WHERE THE TWO
GOVERNED ACTS ARE REACHED BY TWO DIFFERENT COMMANDS, THE REGISTER SHALL NAME
BOTH … published adoption instructions SHALL name the ACTUAL command for each
governed act they cover". Its own scenario for an unexecutable instruction is
that "a consumer following it literally falls back to the ambient tool", which
is the state the pin exists to end. The three assertions below are those
sentences and no further rule.

WHAT THIS FILE DELIBERATELY DOES NOT ASSERT. Issue #776's FIRST assertion —
that a pin some OTHER repository reads IS registered at all — needs a machine
test for "is read", which canon does not carry and which that issue leaves
explicitly unpicked (read the pin's `intended_consumers`, read the row's, take
the union, or require the pin to declare its own answer, "all defensible and all
have costs"). Choosing one is a governed act, not a plain fix, so this checker
walks the REGISTERED rows and asks only whether each is internally coherent. The
two pin files that sit unregistered on `main` are the sibling question, filed
separately as issue #775, and this file neither answers nor forecloses it.

WHY A CHECKER OF ITS OWN, BESIDE THE FAMILIES RATHER THAN INSIDE ONE. § 5.4
placed it beside `release-inventory-drift` rather than in it: that family grades
whether the derived release membership has drifted from the declared bundle — a
different question from whether the consumption register is internally coherent
— and folding two questions into one family makes the finding text unable to say
which failed. The same sentence rules out folding it into
`scripts/validate-manifest-digests.py`, whose docstring scopes itself to rows
CARRYING a `sha256` and declares rows without one "out of scope by design" — and
a pin row has no `sha256`, by D2's deliberate choice. And it rules out adding it
to `scripts/validate-openspec-cli-pin.py`, which is vendored BYTE-IDENTICAL into
three sibling repositories: a check added there grows the re-vendor debt for a
question that is openxFactory's alone. Neither the pin file nor that vendored
validator is touched by this change.

TWO SHARPENINGS TAKEN FROM THE REVIEW BENCH, both of them the same defect class
this file is about — a comparison that passes without measuring. Copilot and
Codex each raised that `ROOT / <claimed>` DISCARDS the root for an absolute path
and follows a `..` out of the tree, so a row naming a host path would be
reported "in this tree" whenever the HOST carries that file while no consumer's
checkout does; `resolve_in_tree` refuses both, mirroring
`scripts/validate-avatar-client.py`'s containment helper and Article IV's
"Committed files MUST NOT contain host-absolute paths". Codex raised that a bare
substring test reports `scripts/tool.py.old` as naming `scripts/tool.py` — the
exact rename drift this lane exists to catch, passing; `rule_names_entrypoint`
requires a delimited path token.

AND THEN THE SAME DEFECT CLASS ARRIVED INSIDE THE PIN (issue #840, the fourth
assertion). A `dispositions[]` entry ACCEPTS one ERROR-level finding of the
pinned tool, and the pin's header rests the whole mechanism on one sentence:
"A DISPOSITION WITHOUT A CITATION IS REFUSED, not ignored … `cited_to:` is
required and must be non-empty", because "an uncited exception is the thing this
estate refuses everywhere else it appears". `validate-openspec-cli-pin.py`
enforces that the field is a non-empty list, PRINTS its members in the
disposition report a reviewer reads — and never opens one. PR #834 renamed a
change directory; two citations in the live pin went on naming
`prepare-openspec-1.12-readiness`; `--all --no-cache` exited 0 before and after;
and the drift was caught by a human reading a diff. That is this file's own
failure mode one level down — a value the register publishes and nothing
compares — so it is this file's fourth assertion rather than a new checker.
`check_citations` and `read_citation` carry the reasoning, the grammar the
pin actually documents, and the four things the arm deliberately does not assert.

A THIRD BENCH ROUND, ON THE ARM ITSELF, AND IT WAS THE SAME DEFECT CLASS AGAIN.
The arm's first version read the LAST TOKEN of a citation's referent region as
its referent. Codex found both halves of what that costs: a citation whose line
continues past its path (`openspec/missing.md: gone`, or the same line after a
YAML reconstruction that turned `false` into `False`) classified as PROSE, so the
path was never opened and the run exited 0 — this arm's own silence, in the shape
it exists to end; and a citation with ordinary prose before its path (`the packet
at openspec/…`) was called another repository's on the strength of having more
than one token, so it went unresolved too. Both were one root, and it ran deeper
than the token rule: the arm was classifying `yaml.safe_load`'s VALUE
where the pin's grammar, its own reader and its own printed report all carry the
LINE. A general YAML parser does not give that line back — measured on the live
pin, two citations come back single-key MAPPINGS and three come back TRUNCATED at
the ` #` of a forge reference. So `citation_lines_by_entry` reads the `cited_to:`
lines from the pin's bytes, `check_citations` aligns them against the parsed
structure (and refuses the field outright if the two readings disagree, rather than
attach a finding to the wrong item), and `read_citation` reads EVERY token of the
line's referent region, deciding the kind by form (`://`, then `#`, then `/`) and
reserving "another repository's" for a path immediately preceded by a repository
name the pin ITSELF declares in its `repo:` fields. The readers' disagreement is
still measured and named for a successor, but no verdict rests on it any more.

A FOURTH BENCH ROUND MADE THE BYTE READER STRUCTURAL (issue #851, Codex and
Copilot on PR #842). Its first version matched a `cited_to:` key ANYWHERE in the
bytes and stopped a list at the first non-item line, and equal GLOBAL counts were
its proof of alignment — so a `cited_to:`/`- …` pair quoted inside a folded
`why: >-` and a `#` comment swallowing a real item CANCEL, and a dangling
citation after the comment is never opened while the run exits 0.
`citation_lines_by_entry` now skips a block scalar's body whole, treats a comment
or a blank line inside a list as the non-member it is, and returns every line
BOUND to the `dispositions[]` entry that carries it, which is what
`check_citations` compares entry by entry. It also applies the production
reader's own `_unquote` to each line, so quoting a scalar — the repair this arm
names for a successor — can actually clear the divergence it was made for
instead of making it permanent.

Run: python3 scripts/validate-pin-registrations.py (also exercised by
tests/pin_registrations/test_pin_registration_sweep.py on every required-suite
pass, the same lane `tests/manifest_digests/` gives the estate-wide digest
sweep, so the checker IS run rather than merely runnable).
Exit codes: 0 every registered pin coheres, 1 named findings, 2 harness error.
`WARN` lines report a thing MEASURED that this file may not repair — they name
it, and they do not move the exit code.
"""
from __future__ import annotations

import re
import string
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "contracts" / "manifest.yaml"

PIN_TYPE = "pin"
ENTRYPOINT_FIELD = "consumer_entrypoint"
RULE_FIELD = "consumption_rule"
DISPOSITIONS_FIELD = "dispositions"
CITATION_FIELD = "cited_to"

# The citation grammar this arm reads: what the pin's header DOCUMENTS, what its
# own reader ADMITS, and — stated as such — what this corpus's citations are
# observed to do. NOT one character more. See `read_citation`.
#
# `—` (EM DASH) separates a citation's REFERENT from the prose gloss that says
# why it is cited; every citation in the live pin is written that way.
# `§` introduces a section inside the referent's document.
# A trailing parenthetical is an aside about the referent (`codexFactory PR #216
# (prepare-openspec-1.12-readiness, head b2a6af34)`), never part of it.
CITATION_GLOSS = "\u2014"
CITATION_SECTION = "\u00a7"
_TRAILING_PAREN = re.compile(r"\((?:[^()]*)\)\s*$")
_LINE_SUFFIX = re.compile(r"^(?P<path>.+?)(?::(?P<line>\d+))?$")
_URL_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://")

# A citation's tokens carry the corpus's own emphasis and punctuation around
# their referent (```openspec/…```, `(…)`, a trailing comma); none of it is part
# of the path. `:` is NOT trimmed here — the `:<line>` suffix is read and
# stripped by `_LINE_SUFFIX`, which is the only place a colon means anything.
_TOKEN_DECORATION = "`'\"\u201c\u201d()[]{}<>,;" + CITATION_SECTION

# The `cited_to:` block, read from the pin's own bytes. The pin's verifier reads
# its items as `^      - (\S.*)$`; the indentation is matched RELATIVE to the
# key here rather than fixed at six spaces, because `yaml.safe_dump` writes a
# sequence at its key's own column and the tests' fixtures are written that way.
# See `citation_lines_by_entry`.
_CITED_TO_KEY = re.compile(r"^(?P<indent> *)(?P<dash>- )?" + CITATION_FIELD
                           + r":\s*$")
_LIST_ITEM = re.compile(r"^(?P<indent> *)- (?P<text>\S.*?)\s*$")

# THE THREE THINGS THAT MAKE THE READER STRUCTURAL RATHER THAN GLOBAL (issue
# #851, Codex on PR #842). A `cited_to:` key line or a `- ` item written inside
# FOLDED PROSE is content, not structure — a disposition's `why: >-` may quote
# the very grammar this reader matches — so a block scalar's body is skipped
# whole; a comment or a blank line between two items does NOT end a list; and
# the walk stays inside `dispositions:` and counts its entries, so every line is
# bound to the entry that carries it instead of to a position in a global list.
# `>-` is the only style the production reader admits, but EVERY style and every
# key spelling is matched HERE, because this reader's job at the opener is to skip
# a body, and a body it failed to recognise is exactly the decoy the bench found.
# The first cut of this pattern took an identifier-shaped key (`[A-Za-z_]\w*`),
# which is one repository's house style and not YAML's — a hyphenated `INV-2: >-`
# or a quoted `"a: b": >-` opens a folded scalar just as well, and its body would
# have been walked as structure (Copilot, PR #863). The key is now any plain
# scalar up to the `: ` separator, or a quoted one, and a trailing comment on the
# header line is admitted because YAML admits it. ONE BOUNDARY IS DELIBERATE: a
# KEYLESS block scalar (`- >-` as a whole sequence entry) is not matched, because
# a line of that shape inside an open `cited_to:` list is a CITATION under the
# pin's own production and is read as one. Such an entry cannot hide a decoy
# either — it is not a mapping, so it contributes no parsed citation while its
# body's lines bind to its entry index, and the per-entry comparison refuses the
# field.
_DISPOSITIONS_KEY = re.compile(r"^(?P<indent> *)" + DISPOSITIONS_FIELD + r":\s*$")
_BLOCK_SCALAR_KEY = re.compile(
    r"^(?P<indent> *)(?P<dash>- )?"
    r"(?:\"[^\"]*\"|'[^']*'|[^\s#][^:]*)"
    r":[ \t]+[|>][0-9+-]*(?:[ \t]+#.*)?[ \t]*$")
_SEQUENCE_ITEM = re.compile(r"^(?P<indent> *)- ")
_COMMENT_OR_BLANK = re.compile(r"^\s*(?:#.*)?$")

# The spellings that mean THIS repository where a citation qualifies a path with
# a repository name. Restated from `scripts/doc_health/pin_class.py`'s
# `OWN_REPOSITORY_SPELLINGS` rather than imported — that module is a doc-health
# package member that reaches for git, and this checker is a standalone script —
# and `tests/pin_registrations/` pins the two sets equal so a divergence reds
# rather than drifts.
OWN_REPOSITORY_SPELLINGS = frozenset({"openxfactory", "opensoft/openxfactory"})

# A path token continues across these; a delimited occurrence of the entrypoint
# is one that neither of them runs into. See `rule_names_entrypoint` below.
NAME_CHARS = frozenset(string.ascii_letters + string.digits + "._-")
TRAILING_CHARS = NAME_CHARS | frozenset("/")


def resolve_in_tree(claimed):
    """The claimed path resolved inside `ROOT`, or a REFUSAL REASON.

    Returns `(path, None)` or `(None, reason)`. Mirrors
    `scripts/validate-avatar-client.py`'s containment helper rather than
    inventing a second dialect for the same question, and exists because
    `Path(root) / "/abs"` DISCARDS the root: a row naming an absolute or
    `..`-escaping path would otherwise be reported "in this tree" whenever the
    HOST happens to carry that file, while no consumer's checkout contains it.
    The constitution's Article IV says the same thing about the corpus —
    "Committed files MUST NOT contain host-absolute paths; use repo-relative
    paths or runtime resolution" — so a register naming one is a finding on its
    own terms and not merely an unreadable path.
    """
    if not isinstance(claimed, str) or not claimed.strip():
        return None, ("is not a non-empty string path, and `ROOT / "
                      "<non-string>` raises rather than reporting")
    candidate = Path(claimed)
    if candidate.is_absolute():
        return None, ("is an ABSOLUTE path; joining one to the repository root "
                      "discards the root entirely, and no consumer's checkout "
                      "carries a host path")
    if ".." in candidate.parts:
        return None, ("contains a '..' segment, which walks out of the "
                      "repository the register speaks for")
    root = ROOT.resolve()
    target = (root / candidate).resolve()
    if not target.is_relative_to(root):
        return None, (f"resolves to {target}, which is outside the repository; "
                      f"refused rather than read")
    return target, None


def rule_names_entrypoint(rule: str, entrypoint: str) -> bool:
    """True when `rule` names `entrypoint` as a DELIMITED path token.

    A bare substring test is too weak for the drift this lane exists to catch:
    a stale rule saying `scripts/tool.py.old` CONTAINS `scripts/tool.py`, so the
    rename that produced it would be reported coherent. An occurrence therefore
    counts only when the text does not continue the token — a following name
    character, `.`, `-`, `_` or `/` all mean the rule is naming a DIFFERENT
    path.

    A LEADING `/` is deliberately allowed while a leading name character is not:
    `.openxfactory-pin/scripts/tool.py` is the same entrypoint named through the
    checkout directory a consumer is told to make, which is exactly the recipe
    the register publishes, whereas `myscripts/tool.py` is another file.
    """
    start = 0
    while True:
        index = rule.find(entrypoint, start)
        if index == -1:
            return False
        before = rule[index - 1] if index else ""
        end = index + len(entrypoint)
        after = rule[end] if end < len(rule) else ""
        if before not in NAME_CHARS and after not in TRAILING_CHARS:
            return True
        start = index + 1


def _unquote(raw: str) -> str:
    """The production reader's unquoting rule, applied to a citation LINE.

    RESTATED FROM `scripts/validate-openspec-cli-pin.py`'s `_unquote`, not
    imported: that file is hyphenated and therefore unimportable, and this
    checker is a standalone script — the same reason `OWN_REPOSITORY_SPELLINGS`
    is restated above, and pinned equal to its source by a test in
    `tests/pin_registrations/` so a divergence reds rather than drifts.

    WHY THE RULE HAS TO BE THE SAME ONE (issue #851, Codex on PR #842). The
    production reader passes every `^      - (\\S.*)$` item through `_unquote`
    before it is anything, so a QUOTED citation scalar has no quotes in the text
    the pin's own verifier prints and compares. The obvious repair for the ` #`
    and `: ` ambiguities this arm measures is to quote those scalars — and if
    this reader kept the quotes, the repair would turn a divergence WARN that
    names a real disagreement into a permanent one that names only the quotes.
    A repair that cannot clear the warning it was made for is not a repair.
    """
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def citation_lines_by_entry(text: str) -> list[tuple[int, str]]:
    """Every `cited_to:` list-item LINE, paired with the `dispositions[]` entry
    (1-based, counting every sequence item as `parsed_citations_of` does) whose
    block carries it, in file order.

    THE CITATION IS THE LINE, AND THAT IS THE FIELD'S DOCUMENTED GRAMMAR. The
    pin's header says of `cited_to:` only that it "is required and must be
    non-empty"; the whole of the rest is its own reader's production —
    `^      - (\\S.*)$`, the remainder of the line, verbatim, one citation per
    line, whose members it deliberately never parses because flattening them
    "would make the reader guess a delimiter that a citation could itself
    contain". That line is also exactly what its disposition report PRINTS for a
    human to open. So the line is what this arm classifies — after `_unquote`,
    which is the one transformation the production reader itself applies to that
    same production, so a quoted scalar means here what it means there.

    AND A GENERAL YAML PARSER DOES NOT GIVE THAT LINE BACK — measured, twice, on
    the live pin. Two citations quote the tool's own output (```Totals: 23
    passed, 2 failed (25 items)```), and a bare `: ` in a plain scalar makes the
    line a single-key MAPPING to `yaml.safe_load`. Three more contain `PR #444` /
    `codexFactory PR #216`, and a ` #` in a plain scalar is a COMMENT, so the
    parser hands back `"PR"` and `"codexFactory PR"` with the referent cut off.
    An arm that classified the parser's value would read those three as prose —
    and a citation whose path sat after a `#` would never be opened at all, which
    is the silence this whole arm exists to end. `yaml.safe_load` stays the
    reader of the pin's STRUCTURE (which entry, which item, in what order); the
    citation itself is read from the bytes.

    THE WALK IS STRUCTURAL, AND EQUAL GLOBAL COUNTS ARE NO LONGER THE PROOF
    (issue #851, and the arm's first version is what it is written against).
    That version matched a `cited_to:` key ANYWHERE in the bytes and stopped a
    list at the first line that was not an item, so a `cited_to:`/`- …` pair
    quoted inside a folded `why: >-` was admitted as structure while a `#`
    comment between two real items ENDED the real list — and the two errors
    cancel: the counts agree, `zip` pairs the wrong lines, and a dangling
    citation after the comment is never opened while the run exits 0. Three
    rules answer that, and each is one of the two mistakes:

      * a BLOCK SCALAR's body is skipped whole (blank lines and every line
        indented past the key's own column), so nothing written inside a
        disposition's prose is ever read as the pin's structure;
      * a COMMENT or a BLANK line inside a list is skipped and does not end it,
        because neither is a member of the sequence in YAML either;
      * the walk stays inside `dispositions:` and counts its entries, so each
        line comes back BOUND to the entry whose block carries it. The caller
        compares that binding against the parsed structure entry by entry, and a
        decoy that cancels a swallowed item no longer agrees with anything.

    A list item is admitted at or below the key's own indentation because that is
    where both writers put one: the live pin indents its items under
    `cited_to:`, and `yaml.safe_dump` (which the tests' fixtures use) writes a
    sequence at the key's own column — and writes the key itself as `- cited_to:`
    where it is the first key of a sequence entry, whose items then sit two
    columns in.
    """
    pairs: list[tuple[int, str]] = []
    section: int | None = None      # the indentation of `dispositions:`
    entry_indent: int | None = None  # the indentation of its sequence items
    entry_index = 0
    list_depth: int | None = None    # an open `cited_to:` list's item floor
    block_at: int | None = None      # an open block scalar's key column
    for raw in text.splitlines():
        indent = len(raw) - len(raw.lstrip(" "))
        if block_at is not None:
            # A blank line and every more-indented line are the scalar's own
            # content; the first line at or left of the key's column ends it and
            # is read here as structure.
            if not raw.strip() or indent > block_at:
                continue
            block_at = None
        if _COMMENT_OR_BLANK.match(raw):
            continue

        key = _DISPOSITIONS_KEY.match(raw)
        if key is not None:
            section = len(key.group("indent"))
            entry_indent = None
            entry_index = 0
            list_depth = None
            continue

        opener = _BLOCK_SCALAR_KEY.match(raw)
        if section is None:
            if opener is not None:
                block_at = len(opener.group("indent")) + (
                    2 if opener.group("dash") else 0)
            continue

        sequence = _SEQUENCE_ITEM.match(raw)
        item = _LIST_ITEM.match(raw)
        if sequence is not None and entry_indent is None and indent >= section:
            entry_indent = indent

        if sequence is not None and indent == entry_indent:
            # A new `dispositions[]` entry. Its first key may be `cited_to:` or a
            # block scalar, both of which are read from this same line below.
            entry_index += 1
            list_depth = None
        elif list_depth is not None and item is not None and indent >= list_depth:
            pairs.append((entry_index, _unquote(item.group("text"))))
            continue
        elif indent <= section:
            # The mapping has left `dispositions:`; a sibling key at or left of
            # its column is another field entirely.
            section = None
            entry_indent = None
            list_depth = None
            if opener is not None:
                block_at = len(opener.group("indent")) + (
                    2 if opener.group("dash") else 0)
            continue
        else:
            # Any other key line inside an entry closes an open list, which is
            # what the pin's own reader does with it too.
            list_depth = None

        if opener is not None:
            block_at = len(opener.group("indent")) + (
                2 if opener.group("dash") else 0)
            continue
        cited = _CITED_TO_KEY.match(raw)
        if cited is not None:
            list_depth = len(cited.group("indent")) + (
                2 if cited.group("dash") else 0)
    return pairs


def citation_lines_in(text: str) -> list[str]:
    """The citation LINES alone, in file order — `citation_lines_by_entry`
    without the binding, for a caller that only needs the text."""
    return [line for _entry, line in citation_lines_by_entry(text)]


def yaml_reading_of(citation):
    """What `yaml.safe_load` made of one citation line, as text, or `None`.

    Used ONLY to report the divergence between the two readers — never to decide
    what a citation names. A single-key mapping is rejoined as `<key>: <value>`
    so the comparison is against the line the parser would have had to produce;
    anything else (a list, a number, a boolean, a null, a multi-key mapping) has
    no line to compare and comes back `None`.
    """
    if isinstance(citation, str):
        return citation
    if isinstance(citation, dict) and len(citation) == 1:
        (key, value), = citation.items()
        if isinstance(key, str):
            return f"{key}: {value}"
    return None


def repository_qualifiers(pin) -> frozenset[str]:
    """The repository names THIS pin declares, lowercased.

    READ FROM THE PIN AND NOT INVENTED HERE. The header holds that dispositions
    are "SCOPED BY REPOSITORY, because one pin governs the whole estate", every
    entry carries `repo:`, and the pin's own verifier admits exactly the entries
    whose `repo:` equals the validated tree's identity — which it reads from
    `git config --get remote.origin.url`, "AND NOT FROM THE DIRECTORY NAME". So
    the set of repository NAMES this mechanism speaks about is declared, in the
    file, in a field with a documented meaning; that declared set is the
    vocabulary a citation's qualifier is read against, and a word outside it is
    not a repository name to this arm. See `read_citation`.
    """
    dispositions = pin.get(DISPOSITIONS_FIELD)
    if not isinstance(dispositions, list):
        return frozenset()
    return frozenset(entry["repo"].strip().lower()
                     for entry in dispositions
                     if isinstance(entry, dict)
                     and isinstance(entry.get("repo"), str)
                     and entry["repo"].strip())


def referent_region(citation: str) -> str:
    """The part of a citation line that names its referent, gloss removed.

    `—` (EM DASH) separates a citation's REFERENT from the prose gloss that says
    why it is cited; every citation in the live pin is written that way. `§`
    introduces a section inside the referent's document, and a trailing
    parenthetical is an aside about it (`codexFactory PR #216
    (prepare-openspec-1.12-readiness, head b2a6af34)`) — neither is part of the
    referent. All three are observed conventions of this corpus, stated as such:
    the pin's header documents no citation punctuation at all.

    THE GLOSS IS NOT SCANNED, deliberately. A gloss is prose about the referent,
    and prose carries slashes that are not paths (`and/or`, a date, `§5.1/§12.0`,
    the quoted `Totals: 23 passed, 2 failed (25 items)`); reading those as paths
    would report findings against citations that are perfectly sound. The cost is
    stated where it falls: a referent written after the em dash is not resolved,
    and no citation in this corpus is written that way.
    """
    head = citation.split(CITATION_GLOSS, 1)[0]
    head = head.split(CITATION_SECTION, 1)[0]
    return _TRAILING_PAREN.sub("", head).strip()


def read_citation(citation: str, declared=frozenset()):
    """Every machine referent ONE `cited_to:` line names, in its own order.

    Returns a list of `(kind, referent)` pairs, where `kind` is one of:

      * `"tree-path"`   — an UNQUALIFIED repo-relative path; this tree resolves it
      * `"url"`         — an absolute URL, resolved by the network and not here
      * `"reference"`   — `#N` or `owner/repo#N`, resolved by a forge and not here
      * `"qualified"`   — a path a DECLARED repository name puts in another tree;
                          this tree is not the tree it names, so it is not resolved

    An EMPTY list means the line names no machine referent at all (`council
    LA-A1`, `1.12.0`, a bare gloss) — recognised, counted, never a finding.

    EVERY TOKEN OF THE REFERENT REGION IS READ, AND THE LAST-TOKEN RULE IS GONE.
    The arm's first version took the region's LAST token as the referent, and the
    review bench found both halves of what that costs. A citation whose line
    continues past its path — `openspec/missing.md: gone` — classified as PROSE,
    so the path was never opened and the run exited 0: this arm's own silence, in
    the shape it exists to end. And a citation with ordinary prose in front of
    its path — `the packet at openspec/changes/foo/tasks.md` — was called another
    repository's on the strength of having more than one token, so it went
    unresolved too. Reading every token answers both, and it answers them the way
    the field's own grammar reads: the pin admits a citation as one line that may
    CONTAIN a referent, and never says where in the line it sits.

    THE FORM DECIDES THE KIND, in this order, because the three forms are
    mutually exclusive and only one of them is this tree's to resolve. A `://`
    means a URL. A `#` means a forge reference — `PR #444`, `#673`,
    `owner/repo#12` — and it is tested BEFORE the path rule because
    `owner/repo#12` carries a slash too. A `/` then means a repo-relative path;
    a token with no `/` names no directory and is not read as one, because a bare
    dotted token is as likely a version (`1.12.0`) or a change id
    (`prepare-openspec-1-12-readiness`) as a filename.

    A QUALIFIER IS A DECLARED REPOSITORY NAME AND NOTHING ELSE. `codexFactory
    openspec/changes/…` is codexFactory's path and this tree may not report it
    missing; `the packet at openspec/changes/…` is this tree's, with prose in
    front of it. The two are told apart by `repository_qualifiers` — the `repo:`
    vocabulary the pin itself declares — read on the token IMMEDIATELY before the
    path, and a qualifier naming THIS repository (`OWN_REPOSITORY_SPELLINGS`, the
    spelling set `scripts/doc_health/pin_class.py` already committed for this
    question) leaves the path this tree's. Two boundaries, stated: a qualifier
    that is not immediately adjacent to its path is not read as one, and a
    repository the pin never declares is not in the vocabulary — so a citation
    naming one gets its path resolved here and reported missing. That direction
    is chosen: a loud finding a reader answers by declaring the repository, over
    a silent pass on a path nobody opened.

    The `:<line>` suffix is a READING AID and the FILE is the referent: it is
    stripped and NOT checked, because a line number drifts with every edit above
    it, and a checker that failed on that would report a finding on unrelated
    insertions while the citation still names the right document. The pin's
    header documents no line grammar to enforce either way.
    """
    tokens = [token for token in referent_region(citation).split() if token]
    readings: list[tuple[str, str]] = []
    for index, token in enumerate(tokens):
        bare = token.strip(_TOKEN_DECORATION)
        if not bare:
            continue
        if _URL_SCHEME.match(bare):
            readings.append(("url", bare))
            continue
        if "#" in bare:
            readings.append(("reference", bare))
            continue
        if "/" not in bare:
            continue
        match = _LINE_SUFFIX.match(bare)
        # `,;` end a clause and `:` ends a token whose remainder the line
        # continues past (`openspec/foo.md: gone`, the shape the last-token rule
        # used to read as prose); none of the three is part of a path, and a
        # `:<line>` suffix has already been read off by `_LINE_SUFFIX`.
        claimed = (match.group("path") if match else bare).rstrip(",;:")
        if not claimed:
            continue
        previous = (tokens[index - 1].strip(_TOKEN_DECORATION).lower()
                    if index else "")
        if previous in declared and previous not in OWN_REPOSITORY_SPELLINGS:
            readings.append(("qualified", claimed))
        else:
            readings.append(("tree-path", claimed))
    return readings


def parsed_citations_of(dispositions):
    """`(entry index, item, citation)` for every parsed citation, in file order.

    The order `citation_lines_by_entry` is aligned against — the entry index is
    the one the byte reader binds each line to. A disposition that carries
    no `cited_to:` list contributes nothing and is counted as uncited by the
    caller: the pin's own verifier owns that refusal.
    """
    for index, entry in enumerate(dispositions, start=1):
        if not isinstance(entry, dict):
            continue
        citations = entry.get(CITATION_FIELD)
        if not isinstance(citations, list) or not citations:
            continue
        item = str(entry.get("item", "unnamed"))
        for citation in citations:
            yield index, item, citation


def _per_entry(indices) -> str:
    """`1x4, 2x3` — how many citations each entry carries, for a finding that has
    to show a reader WHERE two readings of the same file part company."""
    counts: dict[int, int] = {}
    for index in indices:
        counts[index] = counts.get(index, 0) + 1
    return ", ".join(f"{index}x{counts[index]}"
                     for index in sorted(counts)) or "none"


def check_citations(row_id, raw_path, pin, pin_text, findings):
    """Every `dispositions[].cited_to` path resolves; return True if all do.

    THE GAP THIS CLOSES (issue #840). A disposition is an ACCEPTED EXCEPTION to a
    pinned tool's judgment, and the pin's header states the whole of what makes
    one lawful: "A DISPOSITION WITHOUT A CITATION IS REFUSED, not ignored …
    `cited_to:` is required and must be non-empty", on the ground that "an
    uncited exception is the thing this estate refuses everywhere else it
    appears". `scripts/validate-openspec-cli-pin.py` enforces that the field is
    a non-empty list and PRINTS its members in the disposition report a reviewer
    reads — and it never opens one. So a citation could name a path that no
    longer exists and every run would still exit 0, which is the state PR #834
    produced by renaming a change directory: two citations in the live pin went
    on naming `prepare-openspec-1.12-readiness`, the entrypoint's `--all
    --no-cache` run exited 0 before and after, and the drift was found by a
    reviewer reading a diff rather than by anything that asks. A citation nobody
    can open is a suppression with a footnote, and the footnote is the only
    difference the header rests the mechanism on.

    WHAT IT ASSERTS. The pin's `cited_to:` LINES are read from its bytes
    (`citation_lines_by_entry`), each one BOUND to the `dispositions[]` entry
    whose block carries it, and ALIGNED in file order against the citations
    `yaml.safe_load` parsed — so a finding can name the entry and the item it
    belongs to while the text it classifies is the line the pin's own reader
    admits. Every machine referent of every line is then read by
    `read_citation`; the referents that name an UNQUALIFIED repo-relative path
    are resolved inside this tree with the same containment helper the registered
    `path` and `consumer_entrypoint:` go through; and a path that is absent — or
    absolute, or `..`-escaping — is a named finding and exit 1. `.exists()` and
    not `.is_file()`, because a citation legitimately names a change packet's
    directory. The counts are printed so a pass cannot be vacuous: a reader is
    told how many referents were read, how many of them this tree owns, and how
    many were recognised and left to a forge, a network or another repository.

    THE ALIGNMENT IS PROVED, NOT ASSUMED, AND EQUAL TOTALS ARE NOT THE PROOF
    (issue #851). What is compared is the SEQUENCE OF ENTRY NUMBERS the two
    readers produce: if a line does not fall in the same `dispositions[]` entry
    as the parsed citation it would be paired with — whether because the counts
    differ at all, or because they differ per entry and cancel in the total —
    this arm refuses the whole field with one finding instead of classifying
    anything. An off-by-one would attach every finding to the wrong item; a
    citation written in a flow sequence (`cited_to: [a, b]`) or spread over two
    lines is a form the pin's own line-based reader does not admit either; and a
    `cited_to:` quoted inside folded prose cancelling an item swallowed at a
    comment is exactly what a global count cannot see. Refusing loudly is the one
    behaviour that cannot mislead.

    WHAT IT DELIBERATELY DOES NOT ASSERT. Not the `:<line>` suffix, the gloss, or
    a qualifier's adjacency (`read_citation`). Not a URL's reachability, a forge
    reference's existence, or another repository's path: this checker reads one
    tree and says so, and a network or a sibling checkout is not in it. Not
    `cited_to:`'s presence or shape — the pin's own verifier refuses that as
    `pin-disposition-malformed`, in its own words, and restating another
    checker's refusal in different words is what § 5.4 refused when it kept these
    questions in separate families. Not `dispositions[].path`, which the
    entrypoint reconciles against the tool's report and which this checker has no
    report to compare against. And not the two readers' DISAGREEMENT itself: it
    is measured and named for a successor (`WARN`), because the obvious repair —
    quoting the scalar — changes what that line-based reader CAPTURES in a file
    vendored byte-identical into three sibling repositories, which is a governed
    act with a re-vendor cost and not a path a plain fix may take.
    """
    dispositions = pin.get(DISPOSITIONS_FIELD)
    if dispositions is None:
        print(f"OK {row_id}: `{raw_path}` carries no `{DISPOSITIONS_FIELD}:`, so "
              f"the citation assertion does not apply")
        return True
    if not isinstance(dispositions, list) or not dispositions:
        print(f"OK {row_id}: `{raw_path}` records "
              f"`{DISPOSITIONS_FIELD}: {dispositions!r}`, which carries no entry "
              f"to read a citation from; the pin's own verifier owns that "
              f"refusal (`pin-disposition-malformed`) and it is not restated here")
        return True

    declared = repository_qualifiers(pin)
    parsed = list(parsed_citations_of(dispositions))
    bound = citation_lines_by_entry(pin_text)
    lines = [line for _entry, line in bound]
    uncited = sum(1 for entry in dispositions
                  if not isinstance(entry, dict)
                  or not isinstance(entry.get(CITATION_FIELD), list)
                  or not entry[CITATION_FIELD])

    # THE BINDING IS THE PROOF, ENTRY BY ENTRY. Equal global counts were the
    # first version's proof and they are not one: a decoy admitted from folded
    # prose and a real item swallowed at a comment cancel out (issue #851). What
    # is compared now is the SEQUENCE OF ENTRY NUMBERS the two readers produce,
    # so a line and the citation it is paired with belong to the same
    # `dispositions[]` block or the field is refused whole.
    if [entry for entry, _line in bound] != [index for index, _i, _c in parsed]:
        if len(lines) != len(parsed):
            findings.append(
                f"FAIL {row_id}: `{raw_path}` carries {len(lines)} "
                f"`{CITATION_FIELD}:` line(s) in its bytes and {len(parsed)} "
                f"parsed citation(s) in its structure, so this arm cannot say "
                f"WHICH disposition a line belongs to — it refuses the whole "
                f"field rather than attach findings to the wrong entry. A "
                f"citation is one line (`^      - (\\S.*)$` is the pin's own "
                f"production); a flow sequence or a citation spread over two "
                f"lines is a form the pin's own reader does not admit either")
            print(f"MEASURED {row_id}: the citation bytes and the parsed "
                  f"structure disagree about how many citations there are; "
                  f"nothing classified")
        else:
            findings.append(
                f"FAIL {row_id}: `{raw_path}` carries {len(lines)} "
                f"`{CITATION_FIELD}:` line(s) and {len(parsed)} parsed "
                f"citation(s), but they do not fall in the same "
                f"`{DISPOSITIONS_FIELD}[]` entries "
                f"(bytes {_per_entry(entry for entry, _line in bound)}, "
                f"structure {_per_entry(index for index, _i, _c in parsed)}), so "
                f"this arm cannot say WHICH disposition a line belongs to — it "
                f"refuses the whole field rather than attach findings to the "
                f"wrong entry. Equal totals are not an alignment: a `{CITATION_FIELD}:`"
                f" written inside folded prose and an item swallowed at a comment "
                f"cancel each other out in a global count")
            print(f"MEASURED {row_id}: the citation bytes and the parsed "
                  f"structure agree on how many citations there are but not on "
                  f"which disposition carries them; nothing classified")
        return False

    ok = True
    counts = {"tree-path": 0, "url": 0, "reference": 0, "qualified": 0}
    referents = 0
    unreferenced = 0
    truncated = 0
    mapped = 0
    for (index, item, citation), line in zip(parsed, lines):
        where = f"{DISPOSITIONS_FIELD}[{index}]"
        # NEVER A FINDING, AND NEVER A VERDICT EITHER. In the pin's OWN grammar
        # each of these lines is a well-formed citation — its reader takes the
        # whole line, and its report prints the whole line — so what is measured
        # here is that the same bytes mean two different things to two readers.
        # The classification below reads the LINE, so no verdict rests on the
        # divergence; it is REPORTED because a successor with a re-vendor budget
        # should see it, and silently passing a measured disagreement is the
        # habit this lane exists to break.
        reading = yaml_reading_of(citation)
        if isinstance(citation, dict):
            mapped += 1
            exact = " (rejoined byte for byte)" if reading == line else ""
            print(f"WARN {row_id}: {where} ({item}) — `yaml.safe_load` reads "
                  f"this citation as a single-key MAPPING{exact}, because the "
                  f"bare `: ` inside its quoted tool output is a key/value "
                  f"separator to a general YAML parser")
        elif reading != line:
            truncated += 1
            how = (f"TRUNCATES it to {citation!r} at the ` #` it reads as a "
                   f"comment" if isinstance(citation, str)
                   and line.startswith(citation)
                   else f"reads it as {citation!r}, which is not the line")
            print(f"WARN {row_id}: {where} ({item}) — `yaml.safe_load` {how}; "
                  f"the pin's own reader takes the whole line, and this arm "
                  f"classifies the LINE")
        readings = read_citation(line, declared)
        if not readings:
            unreferenced += 1
            continue
        for kind, referent in readings:
            referents += 1
            counts[kind] += 1
            if kind != "tree-path":
                continue
            target, refusal = resolve_in_tree(referent)
            if refusal is not None:
                findings.append(
                    f"FAIL {row_id}: {where} ({item}) cites `{referent}`, which "
                    f"{refusal} — a citation is opened from the pinned checkout, "
                    f"and a path outside it is unreadable there")
                ok = False
                continue
            if not target.exists():
                findings.append(
                    f"FAIL {row_id}: {where} ({item}) cites `{referent}`, but no "
                    f"such path is in this tree — a disposition rests on its "
                    f"citation, and a citation a reader cannot open is a "
                    f"suppression with a footnote")
                ok = False

    measured = (f"{counts['tree-path']} name a path in this tree, "
                f"{counts['url']} a URL, {counts['reference']} a forge "
                f"reference, {counts['qualified']} a path qualified to another "
                f"repository")
    if unreferenced:
        measured += f"; {unreferenced} citation(s) name no machine referent"
    diverged = truncated + mapped
    if diverged:
        measured += (f"; {diverged} line(s) the two readers read differently "
                     f"({truncated} truncated at a `#`, {mapped} read as a "
                     f"single-key mapping), classified from the line")
    if uncited:
        measured += (f"; {uncited} disposition(s) carry no `{CITATION_FIELD}:` "
                     f"list, which the pin's own verifier refuses as "
                     f"`pin-disposition-malformed`")
    if diverged:
        print(f"WARN {row_id}: {diverged} of {len(parsed)} citation line(s) mean "
              f"one thing to `yaml.safe_load` and another to the pin's own "
              f"line-based reader. QUOTING THEM IS A GOVERNED REPAIR, NOT THIS "
              f"ARM'S: that reader captures the whole line INCLUDING the quotes, "
              f"and it is vendored byte-identical into three sibling "
              f"repositories, so the fix carries a re-vendor cost. Named here "
              f"for a successor rather than silently passed or silently forced")
    if ok:
        print(f"OK {row_id}: {len(dispositions)} disposition(s) carry "
              f"{len(parsed)} citation(s) naming {referents} referent(s) — "
              f"{measured}; every in-tree path resolves")
    else:
        print(f"MEASURED {row_id}: {len(dispositions)} disposition(s) carry "
              f"{len(parsed)} citation(s) naming {referents} referent(s) — "
              f"{measured}")
    return ok


def iter_pin_rows(node):
    """Every mapping registering `type: pin`, wherever it sits in the manifest.

    The walk is recursive on `validate-manifest-digests.py`'s precedent rather
    than indexing `contracts:` directly, so a row nested under a future grouping
    key is still measured instead of silently unmeasured.
    """
    if isinstance(node, dict):
        if node.get("type") == PIN_TYPE:
            yield node
        for value in node.values():
            yield from iter_pin_rows(value)
    elif isinstance(node, list):
        for item in node:
            yield from iter_pin_rows(item)


def check_row(row, findings):
    """Append a named finding per failed assertion; return True if the row is ok.

    Every assertion is reported independently: a row can fail more than one, and
    a reader who is told only the first has to re-run to learn the rest.
    """
    row_id = str(row.get("id", "<row with no id>"))
    ok = True

    raw_path = row.get("path")
    if not raw_path:
        findings.append(
            f"FAIL {row_id}: registered as `type: {PIN_TYPE}` but the row carries "
            f"no `path`, so the register names no pin at all")
        return False

    pin_path, refusal = resolve_in_tree(raw_path)
    if refusal is not None:
        findings.append(
            f"FAIL {row_id}: the row registers `{raw_path!r}`, which {refusal} — "
            f"a register naming a path outside the tree publishes bytes no "
            f"consumer's checkout contains")
        return False

    if not pin_path.is_file():
        findings.append(
            f"FAIL {row_id}: the row registers `{raw_path}` but no such file is "
            f"in this tree — the register publishes a pin a consumer cannot read")
        return False

    try:
        pin_text = pin_path.read_text(encoding="utf-8")
        pin = yaml.safe_load(pin_text)
    except (OSError, yaml.YAMLError) as exc:
        findings.append(
            f"FAIL {row_id}: the pin at `{raw_path}` is registered but does not "
            f"parse as YAML ({exc.__class__.__name__}), so nothing can be "
            f"compared against it")
        return False

    if not isinstance(pin, dict):
        findings.append(
            f"FAIL {row_id}: the pin at `{raw_path}` is registered but is not a "
            f"YAML mapping, so it names no `{ENTRYPOINT_FIELD}:` to compare")
        return False

    # THE CITATION ARM RUNS FIRST, and unconditionally, because the entrypoint
    # assertions below are terminal for a row on their own refusals: reaching
    # this question afterwards would mean a pin whose `consumer_entrypoint:` is
    # unreadable hides every dangling citation it carries behind that one
    # finding, and a reader told only the first has to re-run to learn the rest.
    citations_ok = check_citations(row_id, raw_path, pin, pin_text, findings)

    entrypoint = pin.get(ENTRYPOINT_FIELD)
    if entrypoint is None:
        # A pin that names no entrypoint reaches neither of the two assertions
        # below, and canon obliges no pin to carry the field. Reported as
        # measured rather than passed over in silence, so a reader can tell an
        # inapplicable assertion from an unmade one.
        # `OK` ONLY WHERE THE ROW IS OK (Copilot on PR #842). This branch returns
        # the CITATION arm's verdict, so a row failing on a dangling citation
        # would otherwise carry an unconditional `OK` line about the assertions
        # that did not apply — a label no reader should have to discount.
        print(f"{'OK' if citations_ok else 'MEASURED'} {row_id}: `{raw_path}` is "
              f"registered and present; it names no `{ENTRYPOINT_FIELD}:`, so the "
              f"entrypoint assertions do not apply")
        return citations_ok

    # NOT coerced with `str()` before the containment helper runs: that would
    # turn `consumer_entrypoint: 17` into the string "17" and report it as a
    # merely-missing file, silently swallowing the helper's own non-string
    # refusal — the bench caught the coercion doing exactly that. The raw YAML
    # value is the claimed path, and it is a string only once the helper says so.
    entrypoint_path, refusal = resolve_in_tree(entrypoint)
    if refusal is not None:
        findings.append(
            f"FAIL {row_id}: the pin names `{ENTRYPOINT_FIELD}: {entrypoint!r}`, "
            f"which {refusal} — the published recipe invokes the entrypoint FROM "
            f"THE PINNED CHECKOUT, and a path outside it is unreachable there")
        # Terminal for this row: `consumption_rule` is compared against a PATH,
        # and there is no path to compare against. Reporting a second finding
        # that the rule "never names 17" would be noise, not an assertion.
        return False

    entrypoint = str(entrypoint)
    if not entrypoint_path.is_file():
        findings.append(
            f"FAIL {row_id}: the pin names `{ENTRYPOINT_FIELD}: {entrypoint}` but "
            f"no such file is in this tree — a consumer following the published "
            f"recipe literally gets a missing-file error and falls through to the "
            f"ambient tool, the state the pin exists to end")
        ok = False

    rule = row.get(RULE_FIELD)
    if rule is None:
        findings.append(
            f"FAIL {row_id}: the row carries no `{RULE_FIELD}`, so it names no "
            f"command for any governed act while the pin names "
            f"`{entrypoint}` — the register must state the "
            f"checkout-at-the-pinned-ref recipe")
        ok = False
    elif not rule_names_entrypoint(str(rule), entrypoint):
        findings.append(
            f"FAIL {row_id}: the row's `{RULE_FIELD}` never names `{entrypoint}` "
            f"as a whole path — a longer path that merely CONTAINS it is a "
            f"different file and is exactly the rename drift this asks about; "
            f"the entrypoint this pin's `{ENTRYPOINT_FIELD}:` field carries — the "
            f"register must name the ACTUAL command for each governed act, and a "
            f"rule that names none is not executable by the consumer it is "
            f"published for")
        ok = False

    if ok and citations_ok:
        print(f"OK {row_id}: `{raw_path}` is present, its "
              f"`{ENTRYPOINT_FIELD}: {entrypoint}` resolves, and the row's "
              f"`{RULE_FIELD}` names that same path")
    return ok and citations_ok


def main() -> int:
    if not MANIFEST.is_file():
        print(f"ERROR {MANIFEST} is missing: the consumption register is the "
              f"surface this checker reads, and its absence is a harness error "
              f"rather than a clean corpus", file=sys.stderr)
        return 2
    try:
        doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"ERROR {MANIFEST} does not load ({exc.__class__.__name__}): the "
              f"register cannot be read, which is a harness error and never an "
              f"empty pass", file=sys.stderr)
        return 2

    findings: list[str] = []
    rows = list(iter_pin_rows(doc))
    for row in rows:
        check_row(row, findings)

    for finding in findings:
        print(finding)
    if findings:
        print(f"FAIL {len(findings)} finding(s) over {len(rows)} pin "
              f"registration(s) in contracts/manifest.yaml")
        return 1
    print(f"OK contracts/manifest.yaml: {len(rows)} pin registration(s) cohere")
    return 0


if __name__ == "__main__":
    sys.exit(main())
