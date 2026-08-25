"""The family enumeration in canon, derived-verified against the code registry
(`add-family-enumeration-check`).

WHAT IT ANSWERS. `doc-health`'s "Deterministic check families" requirement
NAMES every check family and COUNTS them, three times, in prose: the total
("SHALL implement twenty check families"), the scan-set split ("Four of the
twenty"), and the remainder ("the other sixteen families"). Every new family
must restate that whole requirement to add itself to the list. Nothing checked
that the restatement was complete, or that the numerals still matched the
families that actually exist.

THE CLASS IS NOT HYPOTHETICAL — IT HAPPENED THREE TIMES IN THREE DAYS, and all
three catches were human. `add-release-inventory-drift-check`,
`add-promotion-fidelity-check` and `add-duplicate-packet-check` each wrote a
`MODIFIED` block restating ONE of the requirement's EIGHT scenarios; two were
caught at their own archive gates and one by a parallel lane. The enumeration
half went wrong the same way: the count sentence had already drifted once
before that — `staged-topic-template` registered 2026-08-15 and stayed
uncounted until 2026-08-23 — because a number only a human re-reads is a number
that drifts. `add-duplicate-packet-check` § 5.5 recorded the structural reading
and commissioned this check: "a requirement whose text every new family must
restate is a requirement every new family can truncate — and the fix is to stop
restating it: derive the enumeration and the counts from `FAMILIES` rather than
re-typing them into canon".

THE TWO HALVES, and the second is the one that actually prevents anything:

1. **CANON.** The promoted `openspec/specs/doc-health/spec.md` enumeration must
   name exactly the families the registry registers, and its three numerals
   must be arithmetically true of that set.

2. **ACTIVE DELTAS.** Any ACTIVE change whose delta restates the requirement
   must carry the COMPLETE enumeration, consistent with the same tree's
   registry. This fires at AUTHORING time, before promotion can destroy canon —
   which is the whole §5.3 near-miss class caught where it is cheap instead of
   at an archive gate.

CANON IS CHECKED ONLY WHERE NO ACTIVE DELTA RESTATES THE REQUIREMENT, and that
is not a loophole — it is the only reading that does not fire on every
legitimate in-flight family. A change adding family N+1 registers N+1 in its
own tree while canon still says N, because canon does not move until the change
archives. Canon is not diverging there; it is PENDING, and the delta half is
what holds the change honest. Where two or more active deltas restate the
requirement — the exact situation that produced the three truncations — EACH is
checked independently against the registry, because `MODIFIED` replaces a
requirement wholesale and whichever archives last is the one canon keeps.

THE REGISTRY IS `families.FAMILIES`, not `FAMILY_IDS`. That module's own
docstring says so — "`FAMILIES` at the bottom of this module is the count" —
and it is the right authority because it is what `run_suite` actually iterates.
`FAMILY_IDS` is the REPORTING list — the order `report.render` emits
"## Findings By Family" sections in — and it is now required to MIRROR the
registry exactly. It did not, for months: `staged-topic-template` (registered
2026-08-15) and `proposal-origin` were both absent, so between them 61 findings
— three of them ERRORS — counted in the headline and appeared in the ranked plan
while rendering under no section at all. Recorded here as a deferred omission
three separate times, and ruled fixed 2026-08-25 (Brett, "fix the FAMILY_IDS
drift"); `set(FAMILY_IDS) == set(FAMILIES)` is now pinned by test, so the DRIFT
CLASS is closed rather than the instance. That equality does not make the
reporting list a second authority for which families exist — `FAMILIES` remains
the sole one — it makes it that authority's complete projection. ORDER stays
unpinned, being presentational.

This family's own runtime check covers the PHANTOM direction only (an entry for
a family the registry does not register, which would render a heading nothing
fills). The missing direction is a test-time invariant rather than a finding,
because both values are constants in this one package: a runtime finding would
fire identically on every run for every repository and say nothing a reader of
a report could act on.

CLASSIFICATION AT LAUNCH IS ADVISORY IN BOTH HALVES — WARNING severity and
deliberate absence from `families.FAMILY_RESOLUTION` — the house pattern its
three sibling families all launched under, and kept here even though the corpus
measures clean, because sequencing a flip behind a measured population is the
rule rather than an obstacle. The flip is a recorded task box.

THE IRONY IS DELIBERATE AND IS THE ACCEPTANCE TEST. Adding this check as the
twenty-first family forces exactly the enumeration restatement it polices — so
this change's own delta is checked BY THIS CHECK, in its own branch, before it
can land. A wrong restatement here cannot reach canon, because the thing it
would corrupt is the thing standing at the gate.
"""

from __future__ import annotations

import re
from pathlib import Path

from . import Finding, Skip, WARNING

FAMILY = "family-enumeration"

# The launch severity, named once. WARNING keeps the family out of
# `runner.main`'s `{CRITICAL}` and `{CRITICAL, ERROR}` gates; absence from
# `families.FAMILY_RESOLUTION` keeps a resolved finding out of the
# uncited-resolution ERROR path. Both halves flip together, by ruling —
# `tasks.md` § 5.1.
_LAUNCH_SEVERITY = WARNING

REQUIREMENT_TITLE = "Deterministic check families"
CANON_REL = "openspec/specs/doc-health/spec.md"
DELTA_GLOB = "openspec/changes/*/specs/doc-health/spec.md"

_REQ_LINE = re.compile(r"^###\s+Requirement:\s*(.+?)\s*$")

# The three numeral-bearing sentences, matched against the requirement's prose
# with all newlines collapsed — the enumeration wraps across six lines in canon
# today and its wrapping is not a fact anyone should have to preserve.
_TOTAL = re.compile(
    r"SHALL implement ([a-z\-]+) check families over the whole factory "
    r"family's governance corpus:\s*(.+?)\.(?:\s|$)")
_SPLIT = re.compile(r"\b([A-Z][a-z]+) of the ([a-z\-]+)\s*—")
_REMAINDER = re.compile(r"the other ([a-z\-]+) families")

# Number words, one direction only. Written out rather than computed because
# the corpus's own spelling is what has to be matched, hyphen included
# ("twenty-one"), and a generated table would be a second grammar for the
# thing this family exists to stop trusting.
_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
    "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "twenty-one": 21, "twenty-two": 22, "twenty-three": 23,
    "twenty-four": 24, "twenty-five": 25, "twenty-six": 26,
    "twenty-seven": 27, "twenty-eight": 28, "twenty-nine": 29,
    "thirty": 30, "thirty-one": 31, "thirty-two": 32, "thirty-three": 33,
    "thirty-four": 34, "thirty-five": 35,
}

WORD_FOR = {v: k for k, v in _WORDS.items()}


def word_to_int(word: str) -> int | None:
    """`"twenty-one"` -> 21, and an unrecognized word -> None.

    None rather than a raise, and rather than 0: a numeral this family cannot
    read is a finding it must REPORT (naming the unreadable word), never a
    silent zero that then fails an arithmetic check for the wrong reason.
    """
    return _WORDS.get(word.strip().lower())


# Prose family names normalize to registry ids MECHANICALLY — lowercase, then
# `/` and whitespace to `-` — for nineteen of today's twenty. The alias below
# is the ONE that does not, and it is declared rather than absorbed into a
# looser rule: canon's "client identity roster composition" is registered
# `client-identity-composition` (no `roster`), because the family id predates
# the prose. A wider normalization that happened to bridge that gap would also
# bridge gaps this family exists to report.
#
# `test_every_alias_is_load_bearing` asserts each entry is still NEEDED, so a
# rename that makes an alias redundant fails loudly instead of leaving a
# private dictionary of forgiveness behind.
ALIASES = {
    "client-identity-roster-composition": "client-identity-composition",
}


def normalize_family_name(prose: str) -> str:
    """The registry id a prose family name denotes.

    Mechanical, then the declared alias table, and NOTHING else. A name that
    normalizes to no registered id is reported as unknown rather than guessed
    at — the whole point of deriving the enumeration is that a name nobody can
    resolve is a defect, not a puzzle to solve with a fuzzier matcher.
    """
    slug = re.sub(r"[\s/]+", "-", prose.strip().lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return ALIASES.get(slug, slug)


def split_enumeration(listing: str) -> list[str]:
    """The prose enumeration `"a, b, and c"` as its member strings.

    The Oxford `and` is stripped from the final member; a member is never split
    on its own internal punctuation, because none of today's names carry a
    comma and a name that did would be a naming problem rather than a parsing
    one.
    """
    parts = [p.strip() for p in listing.replace("\n", " ").split(",")]
    out = []
    for part in parts:
        part = re.sub(r"^and\s+", "", part.strip())
        part = " ".join(part.split())
        if part:
            out.append(part)
    return out


class Statement:
    """One document's statement of the enumeration requirement."""

    __slots__ = ("rel", "kind", "names", "total_word", "readers_word",
                 "split_total_word", "remainder_word")

    def __init__(self, rel: str, kind: str):
        self.rel = rel
        self.kind = kind          # "canon" | "delta"
        self.names: list[str] = []
        self.total_word: str | None = None
        self.readers_word: str | None = None
        self.split_total_word: str | None = None
        self.remainder_word: str | None = None


def requirement_prose(text: str, title: str = REQUIREMENT_TITLE) -> str | None:
    """The requirement's prose — everything above its first scenario.

    Returns None where the document does not state the requirement at all,
    which is how a delta that touches `doc-health` without restating this
    requirement is passed over rather than reported.
    """
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        m = _REQ_LINE.match(line)
        if m and m.group(1).strip() == title:
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if (line.startswith("#### Scenario:") or _REQ_LINE.match(line)
                or (line.startswith("## ") and not line.startswith("### "))):
            end = i
            break
    return "\n".join(lines[start:end])


def parse_statement(rel: str, kind: str, text: str) -> Statement | None:
    """One document's enumeration and its three numerals, or None."""
    prose = requirement_prose(text)
    if prose is None:
        return None
    st = Statement(rel, kind)
    # WHITESPACE FLATTENED FIRST, and that is not cosmetic: canon wraps this
    # requirement's sentences mid-phrase across six lines, and where the line
    # breaks fall is an editing artefact nobody should have to preserve for a
    # numeral to be readable. The first cut matched against the raw prose and
    # silently found no total at all, which would have reported the
    # requirement as unreadable rather than as correct.
    flat = " ".join(prose.split()) + " "
    m = _TOTAL.search(flat)
    if m:
        st.total_word = m.group(1)
        st.names = split_enumeration(m.group(2))
    m = _SPLIT.search(flat)
    if m:
        st.readers_word, st.split_total_word = m.group(1), m.group(2)
    m = _REMAINDER.search(flat)
    if m:
        st.remainder_word = m.group(1)
    return st


def _canon_statement(tree_root: Path) -> Statement | None:
    path = tree_root / CANON_REL
    if not path.is_file():
        return None
    return parse_statement(CANON_REL, "canon",
                           path.read_text(encoding="utf-8", errors="replace"))


def _delta_statements(tree_root: Path) -> list[Statement]:
    """Every ACTIVE change delta that restates the requirement.

    Archived packets are deliberately OUT of scope: their deltas are already
    promoted or deliberately not, they can no longer destroy canon, and
    `promotion-fidelity` and `duplicate-packet` are the families that read
    them. This family watches what is still in flight.
    """
    out = []
    changes = tree_root / "openspec" / "changes"
    if not changes.is_dir():
        return out
    for path in sorted(changes.glob("*/specs/doc-health/spec.md")):
        if "archive" in path.relative_to(changes).parts[:1]:
            continue
        st = parse_statement(path.relative_to(tree_root).as_posix(), "delta",
                             path.read_text(encoding="utf-8", errors="replace"))
        if st is not None:
            out.append(st)
    return out


def _registry() -> list[str]:
    """The families the suite actually runs, in registration order.

    Read from the RUNNING code rather than parsed out of a repository's source,
    because the running registry is what `run_suite` iterates and therefore
    what the requirement is making a claim about. On a self-gate run — the PR,
    which is this family's prevention point — the running code and the checked
    tree are the same tree.
    """
    from .families import FAMILIES
    return list(FAMILIES)


def _check(st: Statement, registry: list[str], repo: str) -> list[Finding]:
    """Every way one statement can disagree with the registry."""
    findings: list[Finding] = []
    expected = set(registry)
    where = ("the promoted requirement" if st.kind == "canon"
             else "this active delta's restatement")
    action = ("restate the enumeration and its counts from "
              "`families.FAMILIES` — every registered family named once, "
              "and every numeral derived rather than re-typed")

    def add(rule):
        findings.append(Finding(_LAUNCH_SEVERITY, FAMILY, repo, st.rel,
                                rule, action))

    if st.total_word is None or not st.names:
        add(f"{where} of {REQUIREMENT_TITLE!r} does not state a readable "
            f"family enumeration, so its agreement with the "
            f"{len(registry)}-family registry cannot be established")
        return findings

    resolved, unknown = [], []
    for prose in st.names:
        ident = normalize_family_name(prose)
        if ident in expected:
            resolved.append(ident)
        else:
            unknown.append((prose, ident))

    for prose, ident in unknown:
        add(f"{where} names check family {prose!r}, which resolves to "
            f"{ident!r} and is not a registered family")

    missing = [f for f in registry if f not in set(resolved)]
    if missing:
        shown = ", ".join(repr(f) for f in missing[:4])
        if len(missing) > 4:
            shown += f", +{len(missing) - 4} more"
        add(f"{where} omits {len(missing)} of the {len(registry)} registered "
            f"check families: {shown}")

    duplicates = sorted({f for f in resolved if resolved.count(f) > 1})
    if duplicates:
        add(f"{where} names {', '.join(repr(d) for d in duplicates)} more "
            f"than once")

    # --- the three numerals -------------------------------------------------
    total = word_to_int(st.total_word)
    if total is None:
        add(f"{where} states a total this check cannot read: "
            f"{st.total_word!r}")
    elif total != len(registry):
        add(f"{where} says {st.total_word!r} check families, but "
            f"{len(registry)} are registered — expected "
            f"{WORD_FOR.get(len(registry), len(registry))!r}")

    if st.split_total_word is not None:
        split_total = word_to_int(st.split_total_word)
        if split_total is None:
            add(f"{where} states a scan-set split total this check cannot "
                f"read: {st.split_total_word!r}")
        elif split_total != len(registry):
            add(f"{where} says {st.readers_word!r} of "
                f"{st.split_total_word!r}, but {len(registry)} families are "
                f"registered")

    if st.remainder_word is not None and st.readers_word is not None:
        remainder = word_to_int(st.remainder_word)
        readers = word_to_int(st.readers_word)
        if remainder is None:
            add(f"{where} states a remainder this check cannot read: "
                f"{st.remainder_word!r}")
        elif readers is None:
            add(f"{where} states a scan-set reader count this check cannot "
                f"read: {st.readers_word!r}")
        elif total is not None and remainder != total - readers:
            add(f"{where} says {st.readers_word!r} of {st.total_word!r} read "
                f"the lifecycle scan set and 'the other "
                f"{st.remainder_word}' do not, which does not add up — "
                f"expected "
                f"{WORD_FOR.get(total - readers, total - readers)!r}")
    return findings


def _check_reporting_list(repo: str, registry: list[str]) -> list[Finding]:
    """`FAMILY_IDS` may not promise a report section for an unregistered
    family.

    ONE DIRECTION ONLY, deliberately. A phantom entry would render a heading
    for a family that never runs, which no other check would notice. The
    opposite direction — a registered family MISSING from `FAMILY_IDS`, so it
    reports findings with no section of its own — is true of two families
    today (`proposal-origin`, which that capability already records as a known
    defect, and `staged-topic-template`) and is deliberately NOT reported here:
    it predates this change, and repairing another capability's registration
    inside this one would put unrelated report output on this feature's
    evidence. Measured in `tasks.md` § 4, boxed in § 5.2.
    """
    from . import FAMILY_IDS
    phantom = [f for f in FAMILY_IDS if f not in set(registry)]
    if not phantom:
        return []
    return [Finding(
        _LAUNCH_SEVERITY, FAMILY, repo, "scripts/doc_health/__init__.py",
        f"`FAMILY_IDS` promises a report section for "
        f"{', '.join(repr(f) for f in phantom)}, which "
        f"{'is' if len(phantom) == 1 else 'are'} not registered in "
        f"`families.FAMILIES`",
        "remove the entry, or register the family")]


def fam_family_enumeration(ctx):
    """Canon's family enumeration, and every active restatement of it,
    derived-verified against the code registry."""
    registry = _registry()
    scoped = []
    for repo, path in sorted(ctx.repo_paths.items()):
        root = Path(path)
        if (root / CANON_REL).is_file():
            scoped.append((repo, root))
    if not scoped:
        return Skip(FAMILY, "no repository in scope carries a promoted "
                            "doc-health specification")

    findings: list[Finding] = []
    for repo, root in scoped:
        deltas = _delta_statements(root)
        for st in deltas:
            findings.extend(_check(st, registry, repo))
        # Canon is PENDING, not divergent, while an active delta restates the
        # requirement — see this module's docstring.
        if not deltas:
            canon = _canon_statement(root)
            if canon is not None:
                findings.extend(_check(canon, registry, repo))
        findings.extend(_check_reporting_list(repo, registry))
    return findings
