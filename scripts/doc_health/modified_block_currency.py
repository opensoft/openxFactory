"""The twenty-second deterministic family: currency of an active change's
`## MODIFIED Requirements` blocks (`add-modified-block-currency-check`).

WHAT IT ANSWERS. OpenSpec's `MODIFIED` REPLACES a requirement wholesale; it does
not merge. So whatever a MODIFIED block says is what canon says after the
archive act, and every clause and scenario the block does not restate is deleted
silently. `openspec validate --strict` checks a delta's SHAPE — the heading, the
keyword on the first line, at least one scenario — and never what promotion will
do to the requirement being replaced.

THE CLASS IS NOT HYPOTHETICAL. It happened four times in this repository in one
week and a human caught it every time. `add-doxchat-model-intake` (issue #351)
was holding the deletion of six body clauses, two scenarios and one REVERTED
scenario line, with `validate --strict` green throughout; and
`add-release-inventory-drift-check`, `add-promotion-fidelity-check` and
`add-duplicate-packet-check` each restated ONE of the eight scenarios of
`doc-health`'s own "Deterministic check families" (issue #329).

THE DEFECT IS A FUNCTION OF TIME, NOT OF CARE. #351's block was written on
2026-08-21 against a pre-`02a71d6e` canon and was correct when written. Canon
moved; nothing re-read the block; four days later it was holding a nine-item
deletion. Issue #357 states the gap in the sentence this family exists to
retire: "a long-lived active change that MODIFIES a requirement goes stale as
canon moves".

COUNTING CANNOT SEE IT. The `add-release-inventory-drift-check` case nearly
escaped because the FILE-LEVEL scenario count did not move: that change's own
ADDED requirement brought seven scenarios and its MODIFIED block was about to
drop seven, so `doc-health/spec.md` read 98 -> 98. Only per-requirement
accounting shows it.

AND THE FAMILY WHOSE WHOLE JOB IS DELTA-VERSUS-SPEC FIDELITY IS STRUCTURALLY
BLIND TO IT (#330). `promotion_fidelity` compares an ARCHIVED delta to the
promoted spec, and after the archive act canon IS the delta — a block that
dropped seven scenarios and a canon now missing them agree perfectly. The
comparison that can see the loss is between an ACTIVE delta and the canon it has
not yet replaced: a different document pair, read at a different moment, which
is why this is a separate family rather than a wider reading of that one.

THREE ARMS, FIVE FINDING CLASSES, AND THE NUMBERS DIFFER ON PURPOSE:

1. **Scenario-title completeness** (`_LAUNCH_SEVERITY`, `warning`). Every
   `#### Scenario:` title canon carries must appear as a scenario title in the
   block. Short titled strings rather than prose, reporting deletion at the
   granularity the defect occurs at. THIS is the arm that carries the family's
   gate, and the only arm the flip in `tasks.md` § 7.2 moves.
2. **The carriage ledger** (`_LEDGER_SEVERITY`, `info`). Every body unit and
   every scenario bullet the block does not carry, as AT MOST ONE finding per
   requirement. It CANNOT distinguish a deliberate rewording from stale text and
   its rule text says so: it is the list a reviewer reads to confirm each
   divergence was intended.
3. **Title resolution and ordering** (`_RESOLUTION_SEVERITY`, `warning`). A
   block whose title resolves to nothing, and an ordering between two active
   RATIFIED writers that no declaration settles.
4. **Marker defects** (`_LEDGER_SEVERITY`, `info`) — not an arm. A marker that
   names a unit the block still carries declares nothing and is reported itself.
   It does NOT inherit the ledger's hedge, because a marker naming a carried
   unit is wrong with certainty.
5. **Unplaced-finding drift** (`_DRIFT_SEVERITY`, `warning`) — not an arm
   either, and not a comparison between documents at all: it reads THIS MAP's
   own verdict on the findings the arms just emitted. Where the map cannot place
   a rule text, one `warning` per DISTINCT unplaced rule SHAPE says so, names
   how many findings carry that shape and quotes the first of them verbatim.
   Added by `add-unclassified-finding-class`, because the residual row below is
   prose: it has no severity, so no `--fail-on` reaches it, and it is not a
   finding, so the ranked plan never carries it. The row STAYS beside the
   finding — it is what makes the tally sum to the rows it is printed above.

MATCHING IS SAME-KIND AND EXACT, and both halves of that are load-bearing.
CONTAINMENT IS FORBIDDEN: canon's bullet `**THEN** the selector MUST show
exactly the available catalog entries and their data-handling badges` is a
SUBSTRING of the widened line `add-doxchat-model-intake` replaced it with, so a
containment rule reports nothing on the very defect PR #358 had to repair by
hand. SIMILARITY IS FORBIDDEN TOO: a threshold high enough to pass an ordinary
reword also passes a clause whose meaning has been REVERSED, and #351's ninth
item was exactly that. And normalization stops at whitespace — see `normalize`,
which is deliberately NOT `promotion_fidelity.norm`.

CLASSIFICATION AT LAUNCH IS ADVISORY IN BOTH HALVES: `warning`/`info`
severities, AND deliberate absence from `families.FAMILY_RESOLUTION`. The second
half is the one that is easy to lose — `report.uncited_resolutions` turns a
`contested` finding that VANISHES between reports into an `error`, so a
`contested` advisory family reds the nightly the first time anyone corrects a
block, which is enforcement through the back door on the run that proves the
launch worked. Both halves flip together, by ruling, on the discharge of a
measured population.

THREE READINGS THE DELTA DOES NOT SPELL OUT, RULED 2026-08-27 AND RECORDED HERE
SO A LATER READER FINDS THEM WITHOUT RE-DERIVING THEM:

- **CARRIAGE IS SET-BASED, NOT MULTISET.** Where canon states one normalized unit
  TWICE inside a requirement, a block carrying it once carries both. 13 of this
  corpus's 513 promoted requirements do that today — a clause repeated across two
  scenarios, most often a `**WHEN**` line. Set semantics cannot lose a DISTINCT
  obligation: every distinct unit is still compared, and the only thing forgiven
  is a duplicate that says nothing the first one did not. Multiset semantics
  would report a block for de-duplicating canon's own repetition, which is an
  editorial improvement rather than a deletion. Recorded as decision O11 in the
  feature plan, flagged for veto.
- **A MARKER NAME THAT MATCHES NO CANON UNIT IS IGNORED, FAIL-CLOSED.** It
  suppresses nothing and is not itself reported. The unit the author MEANT is
  therefore still reported by whichever arm owns it, so a mistyped name costs a
  finding rather than buying silence. Reporting the dangling name too would be a
  second obligation this change has no standing to add; it is a plausible later
  ruling.
- **A FENCED REGION IN CANON IS NEVER REQUIRED CARRIAGE.** The exclusion runs on
  both sides of every comparison, so a block need not restate canon's fenced
  examples — including the two written-out marker forms in this family's own
  requirement, which promote into canon and would otherwise parse as complete
  markers on the requirement that defines them.

THIS MODULE READS THE CHECKED-OUT TREE AND NOTHING ELSE. The live-`main` basis
`promotion_fidelity` carries is ruled for that family alone and would be
actively wrong here: an active change lives on a branch, so a family reading
`main` would measure a delta `main` does not carry against canon the branch may
have moved.

ITS DOCUMENT SET IS THREE FILES PER CHANGE, NOT TWO: the active delta, the
promoted spec it has not yet replaced, and the change's own `proposal.md` — the
last one read ONLY to resolve whether one active writer declares itself relative
to another, which is the ordering rule `release-realization` owns. None of the
three is a governed-corpus document or a lifecycle-scan-set document, so this
family moves no census, word count, canon-share figure, inventory entry or
catalog record.
"""

from __future__ import annotations

import re
from pathlib import Path

from . import INFO, SEVERITY_RANK, WARNING, Finding, Skip
from . import corpus
from . import duplicate_packet
from . import promotion_fidelity
from .promotion_fidelity import norm, parse_delta

# `duplicate_packet._mention` is the whole-token change-id matcher the delta
# names BY REFERENCE ("the whole-token match the duplicate packet family already
# uses"), so it is imported rather than re-spelled. No cycle: neither sibling
# imports this module, and `families.py` already imports all three.
_mention = duplicate_packet._mention

FAMILY = "modified-block-currency"

# THE SEVERITIES, FOUR OF THEM, NAMED APART ON PURPOSE.
#
# `_LAUNCH_SEVERITY` is the identifier `promotion_fidelity`, `duplicate_packet`
# and `family_enumeration` all carry, and it is the grep that ties every reader
# of a launch decision together. Here it belongs to the SCENARIO-TITLE arm,
# because that is the one arm the flip reserved in
# `add-modified-block-currency-check` tasks.md § 7.2 moves — raising it to
# `error` AND adding the `contested` classification, together, in one commit,
# after the standing population is discharged.
#
# The other two are separate constants precisely so that flip cannot drag them.
# A single shared constant would take the title-resolution arm to `error` at the
# same time, which no ruling asked for; and the carriage ledger has NO flip
# proposed at all, its population being standing by construction — every
# legitimate MODIFIED block edits something, so an editorial band is the honest
# launch state and a permanent yellow row for a condition nobody should act on
# is how a report stops being read.
#
# `_DRIFT_SEVERITY` is the FOURTH, added by `add-unclassified-finding-class` for
# the fifth finding class, and the same argument applies to it word for word:
# § 7.2 flips `_LAUNCH_SEVERITY` and this class must not ride that flip. Here
# the drag would also be INVISIBLE — `FindingClass.band` reads the constant and
# the registry pin reads the band off the class, so a shared constant would move
# the rendered caption and the emitted finding together and no pin would notice.
# `test_the_reserved_flip_of_the_launch_severity_does_not_drag_the_drift_class`
# simulates the flip over this module's own source and is what makes that
# falsifiable rather than merely written down. The class is also DESIGNED to
# stop being emitted as soon as somebody extends the map, and § 7.2 raises the
# `contested` classification with the severity — which would turn that
# disappearance into an `error` under the uncited-resolution rule.
_LAUNCH_SEVERITY = WARNING
_RESOLUTION_SEVERITY = WARNING
_LEDGER_SEVERITY = INFO
_DRIFT_SEVERITY = WARNING

# The two document sets, and there is no third. `archive/` is excluded by the
# reader rather than by the glob, because a glob that happened to match an
# archived path would be a silent widening of this family's scope.
# The one active-delta pattern, glob-ready and repo-relative. BOTH readers use
# it: a second hardcoded copy is how two readers of one document set come to
# disagree about which documents they read.
DELTA_GLOB = "openspec/changes/*/specs/*/spec.md"
# Position of the change directory inside a `DELTA_GLOB` match, named so the
# indexing below is readable: openspec / changes / <change> / specs / <cap> /
# spec.md
_CHANGE_PART = 2
CANON_TEMPLATE = "openspec/specs/{capability}/spec.md"

_ACTION = ("restate the requirement as canon currently states it, or declare "
           "the deletion with a `Removed from canon by` marker")


BODY = "body"
SCENARIO_TITLE = "scenario-title"
SCENARIO_BULLET = "scenario-bullet"

# The mask filler. It must be neither whitespace nor a sentence terminator, or
# masking a code span would CREATE a sentence boundary instead of hiding one.
_FILLER = "\x00"


def normalize(text: str) -> str:
    """The comparison spelling of a normative unit: whitespace, and nothing else.

    Runs of whitespace collapse to a single space; the ends are stripped. THAT
    IS THE WHOLE LIST, and its shortness is the rule rather than an omission —
    `add-modified-block-currency-check`'s doc-health delta says "matched in full
    after whitespace normalization ... no normalization beyond it applies", in
    the same paragraph that forbids containment and similarity.

    DELIBERATELY NOT `promotion_fidelity.norm`, which also CASEFOLDS. That is
    correct for a requirement TITLE — "a title's case is a rendering choice no
    reader acts on differently", as its own docstring says — and wrong for a
    unit, because promotion writes the block's BYTES into canon, so a case
    change is a text change. That module's docstring also names the wider
    normalizations it refuses (backticks, punctuation, trailing periods) and the
    gap that hid inside one, and every one of them is refused here for the same
    reason. `promotion_fidelity.norm` IS still reused by this family — for the
    requirement-title lookup and the disposition key, where the shared
    mechanism's spelling is what matters.
    """
    return " ".join(text.split())


def mask_code_spans(text: str) -> str:
    """`text` with the INTERIOR of every CommonMark code span filled, LENGTH
    PRESERVED.

    Sentence boundaries are computed on this string and every emitted unit is
    sliced from the ORIGINAL at those offsets, which is why the length has to
    match: a shorter mask loses the offsets, and a mask applied to the emitted
    text would put filler characters in a finding a human reads.

    The rule is CommonMark's. A run of N backticks opens a span and the closer
    is the next run of EXACTLY N; an unterminated run is literal text and masks
    nothing. The backticks themselves stay in place — only what they enclose is
    filled — so a longer fence still reads as a longer fence.

    WHY IT IS FIRST, before any split: the review measured 118 backticked tokens
    with internal periods in this corpus's requirement bodies
    (`.openspec.yaml`, `promotion_fidelity.py`, version strings). A naive split
    on `. ` shatters those into fragments that never match anything, and the
    carriage ledger becomes noise.
    """
    out = list(text)
    i, n = 0, len(text)
    while i < n:
        if text[i] != "`":
            i += 1
            continue
        j = i
        while j < n and text[j] == "`":
            j += 1
        run = j - i
        close = _closing_run(text, j, run)
        if close is None:
            i = j            # unterminated: the run is literal text
            continue
        for x in range(j, close):
            out[x] = _FILLER
        i = close + run
    return "".join(out)


def _closing_run(text: str, start: int, run: int) -> int | None:
    """The offset of the next backtick run of EXACTLY `run` at or after `start`."""
    k, n = start, len(text)
    while k < n:
        if text[k] != "`":
            k += 1
            continue
        m = k
        while m < n and text[m] == "`":
            m += 1
        if m - k == run:
            return k
        k = m
    return None


def split_sentences(paragraph: str) -> list[str]:
    """`paragraph` split at a `.`, `?` or `!` followed by whitespace or its end.

    The terminator stays with the sentence it ends. Boundaries are found on
    `mask_code_spans(paragraph)` and the returned strings are sliced from
    `paragraph` itself, so `version 1.13 ships.` is one sentence and
    `` Reads `.openspec.yaml` now. Then stops. `` is two.

    A run of terminators (`Really?!`) breaks only after the LAST of them,
    because only the last is followed by whitespace.
    """
    masked = mask_code_spans(paragraph)
    out, start = [], 0
    for i, ch in enumerate(masked):
        if ch not in ".?!":
            continue
        if i + 1 < len(masked) and not masked[i + 1].isspace():
            continue
        piece = paragraph[start:i + 1].strip()
        if piece:
            out.append(piece)
        start = i + 1
    tail = paragraph[start:].strip()
    if tail:
        out.append(tail)
    return out


class Unit:
    """One comparable fragment of a requirement, carrying its KIND.

    `text` is normalized on construction, so it is both what a finding names and
    the comparison spelling; `key` is an alias for that one string, kept as a
    property rather than a second field because two copies of one value is how
    they come to disagree.

    `scenario` is the normalized title of the scenario a BULLET sits under IN
    ITS OWN DOCUMENT. It is recorded but is NOT part of equality, and that is
    the delta's rule rather than a convenience: bullets are compared across ALL
    bullets of the block, never scenario by scenario, or a block could retitle a
    scenario, declare the retitle, and drop the bullets underneath it
    unreported. `scenario` exists for exactly one other rule — "the bullets that
    scenario carried IN CANON", which a genuine removal declares.
    """

    __slots__ = ("kind", "text", "scenario")

    def __init__(self, kind: str, text: str, scenario: str | None = None):
        self.kind = kind
        self.text = normalize(text)
        self.scenario = scenario

    def pair(self) -> tuple[str, str]:
        return (self.kind, self.text)

    def __repr__(self) -> str:  # pragma: no cover - diagnostics only
        return f"Unit({self.kind!r}, {self.text!r})"


def carried(canon_units, block_units) -> list[Unit]:
    """The canon units the block does NOT carry, in canon order.

    A canon unit is carried iff some block unit has the SAME KIND and the SAME
    normalized text. Two rules are enforced by that one line and both are on the
    record:

    **CONTAINMENT IS NOT CARRIAGE.** A block unit that CONTAINS canon's unit has
    REPLACED it. Canon's bullet `**THEN** the selector MUST show exactly the
    available catalog entries and their data-handling badges` is a substring of
    the widened line `add-doxchat-model-intake` put in its place, so a
    containment rule reports nothing on the very defect PR #358 repaired by
    hand. Widening a line is the commonest way a clause is silently replaced.

    **SAME KIND.** A canon body sentence is not carried by a scenario bullet
    that happens to repeat it, and vice versa. Without the kind, a block could
    satisfy the ledger by quoting canon's obligations in prose while deleting
    the scenarios that made them testable.

    Similarity is absent for a third reason, ruled in the corpus already: "a
    rule loose enough to conflate the two would report the ordinary case", and
    here a threshold high enough to pass a reword also passes a clause whose
    meaning has been REVERSED — which is #351's ninth item.
    """
    have = {u.pair() for u in block_units}
    return [u for u in canon_units if u.pair() not in have]


# THE CHANGE-ID TOKEN, and it is a GRAMMAR rather than a lookup. `dh:126-127`
# asks for "a resolvable change-id"; read as "names a change that exists" every
# marker would rot the moment the change that wrote it archives, which
# contradicts the same delta's durability rule (`dh:179-183`: a marker promotes
# into canon with the requirement). So a marker's id must PARSE, not EXIST.
# Recorded as decision O7 in the feature plan, flagged for veto.
_CHANGE_ID = r"[a-z0-9][a-z0-9-]*"
_ISO = r"\d{4}-\d{2}-\d{2}"

# The two prefixes, ANCHORED AND COMPLETE — the bold run, a change-id token, an
# ISO date in parentheses, and the closing colon. `dh:125-133` calls this anchor
# load-bearing and says why: this requirement's own text and
# `document-lifecycle`'s both print the two templates in prose that PROMOTES
# INTO CANON, and a looser test would read those paragraphs as markers and
# exempt them from carriage — the check quietly declining to check the
# paragraphs that define it. A quoted template carries `<change-id>` and
# `<YYYY-MM-DD>`, which match neither group.
_REMOVED_PREFIX = re.compile(
    rf"^\*\*Removed from canon by ({_CHANGE_ID}) \(({_ISO})\):\*\*")
# The destination is matched as "one or more backticks, then anything" and then
# resolved by `extract_code_spans`, never by a nested backtick regex, so a
# destination containing a backtick obeys the same longer-fence rule as a name.
_MERGED_PREFIX = re.compile(
    rf"^\*\*Merged into (`+.*?`+) by ({_CHANGE_ID}) \(({_ISO})\):\*\*")

_FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")

# A dated bold note: the paragraph OPENS a bold run and that run carries an ISO
# date. The predicate the delta does not write (decision O6, flagged for veto) —
# `dh:103-107` makes the note ONE undivided unit and gives the reason without
# saying how to recognize one. This reading is the corpus's own convention in
# all five instances the review examined.
_DATED_BOLD = re.compile(rf"^\*\*[^*]*{_ISO}[^*]*\*\*")

_BULLET = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+")
_SCENARIO_LINE = re.compile(r"^####\s+Scenario:\s*(.+?)\s*$")


def extract_code_spans(text: str) -> list[tuple[int, int, str]]:
    """Every CommonMark code span in `text` as `(start, end, content)`.

    A run of N backticks opens and the next run of EXACTLY N closes; one leading
    and one trailing space are stripped from the content when BOTH are present,
    which is CommonMark's own rule and is what lets a span carry a backtick at
    either end. An unterminated run yields nothing.

    THE FORBIDDEN ALTERNATIVE is a non-greedy `` `([^`]*)` ``. It truncates at
    the first inner backtick, so a marker naming a clause that cites
    `openxFactory` would name a fragment that is not a unit at all — and the
    delta requires extraction "in order, per CommonMark", never by splitting on
    punctuation.
    """
    out: list[tuple[int, int, str]] = []
    i, n = 0, len(text)
    while i < n:
        if text[i] != "`":
            i += 1
            continue
        j = i
        while j < n and text[j] == "`":
            j += 1
        run = j - i
        close = _closing_run(text, j, run)
        if close is None:
            i = j
            continue
        content = text[j:close]
        if len(content) >= 2 and content[0] == " " and content[-1] == " ":
            content = content[1:-1]
        out.append((i, close + run, content))
        i = close + run
    return out


def fenced_regions(lines) -> set[int]:
    """The indices of every line inside a fenced code block, fences included.

    RULED 2026-08-27: those lines are neither units nor markers, in canon or in
    a block. The delta does not say so and did not have to notice — but its OWN
    written-out marker examples live inside a fenced block (`dh:187-190`) which
    promotes into canon with the requirement, and those two lines are COMPLETE
    markers: a real change id, a real ISO date, a closing colon. Without this
    rule the requirement that DEFINES the marker declares two of its own units
    removed, and the same class applies to every fenced example the corpus
    writes.

    A fence opens on a run of three or more backticks or tildes and closes on the
    next run of the same character that is at least as long; an unclosed fence
    runs to the end of the block, which is the conservative direction (text
    nobody can prove is prose is not compared).
    """
    inside: set[int] = set()
    opener: str | None = None
    for i, line in enumerate(lines):
        m = _FENCE.match(line)
        if opener is None:
            if m:
                opener = m.group(1)
                inside.add(i)
            continue
        inside.add(i)
        if m and m.group(1)[0] == opener[0] and len(m.group(1)) >= len(opener):
            opener = None
    return inside


class Marker:
    """One declaration paragraph, recognized by FORM and never by prose.

    The form is NEW, and the corpus's existing dated bold note is deliberately
    not reused: every such note in this corpus records a caught near-miss and a
    RESTORATION, never a deletion — `doc-health`'s own "Deterministic check
    families" carries one naming SEVEN of its eight scenario titles in backticks
    as the seven that were restored. A rule that read deletion out of prose
    would therefore read a faithful restatement of that very requirement as
    declaring seven scenarios deleted, on the requirement whose truncation is
    issue #329. Form, not prose, is what makes the declaration falsifiable.

    `paragraph` is the normalized text, carried for DIAGNOSTICS ONLY: it is read
    by a test's failure message and by nothing in the shipping path — the
    marker-defect finding names the change id, the date and the offending unit,
    which is what a reader acts on. Kept rather than dropped because a marker
    that fails to parse the way its author expected is debugged from its own
    bytes, and re-deriving them from the block costs the reader the parse.
    """

    __slots__ = ("form", "change_id", "date", "names", "destination", "reason",
                 "paragraph")

    def __init__(self, form: str, change_id: str, date: str, names: list[str],
                 destination: str | None, reason: str | None, paragraph: str):
        self.form = form
        self.change_id = change_id
        self.date = date
        self.names = names
        self.destination = destination
        self.reason = reason
        self.paragraph = paragraph

    def __repr__(self) -> str:  # pragma: no cover - diagnostics only
        return f"Marker({self.form!r}, {self.change_id!r}, {self.names!r})"


def parse_marker(paragraph: str) -> Marker | None:
    """A `Marker`, or None for every other paragraph in the corpus.

    FORM-BLIND BY DESIGN: handed a line of marker form this returns a `Marker`,
    whatever document the line came from. What keeps the delta's own fenced
    EXAMPLES from declaring their own units removed is `fenced_regions`, which
    never offers them — not a special case here. A parser that tried to guess
    which markers were "real" would be a prose rule wearing a form rule's
    clothes.
    """
    text = normalize(paragraph)
    m = _REMOVED_PREFIX.match(text)
    form, destination = "removed", None
    if m:
        change_id, date = m.group(1), m.group(2)
    else:
        m = _MERGED_PREFIX.match(text)
        if not m:
            return None
        form = "merged"
        spans = extract_code_spans(m.group(1))
        if not spans:
            return None
        destination = normalize(spans[0][2])
        change_id, date = m.group(2), m.group(3)
    tail = text[m.end():]
    spans = extract_code_spans(tail)
    names = [normalize(c) for _s, _e, c in spans]
    reason = None
    if spans:
        after = tail[spans[-1][1]:]
        if after.startswith(" — "):
            reason = normalize(after[3:]) or None
    return Marker(form, change_id, date, names, destination, reason, text)


def is_dated_bold_note(paragraph: str) -> bool:
    """Does `paragraph` OPEN a bold run carrying an ISO date?

    THE ONE PREDICATE THE DELTA DOES NOT WRITE (decision O6, flagged for veto).
    `dh:99-107` makes the derivation normative and makes a dated bold note ONE
    undivided unit — "a note being a single editorial statement whose sentences
    mean nothing apart" — without saying how to recognize one. This reading is
    the corpus's own convention in every instance the review examined, and
    `test_the_real_notes_this_corpus_carries_are_each_one_unit` measures it
    against the notes canon actually carries rather than trusting it.

    PRECONDITION: `parse_marker` has already returned None. The two forms
    OVERLAP BY CONSTRUCTION — a marker is also a dated bold paragraph — so
    testing this first would swallow every marker and the whole declaration
    mechanism would vanish in silence. `derive_units` enforces the order.
    """
    return _DATED_BOLD.match(normalize(paragraph)) is not None


def _blocks(lines: list[str]):
    """`(kind, text)` groups of one region: `("bullet", ...)` or `("para", ...)`.

    A BULLET is a line opening with a list marker, plus every following non-blank
    line that is not itself a bullet — Markdown's lazy continuation, which is
    what makes a WRAPPED bullet one bullet. A PARAGRAPH is a run of non-blank
    lines terminated by a blank line or by a bullet.
    """
    out: list[tuple[str, list[str]]] = []
    for line in lines:
        if not line.strip():
            out.append(("gap", []))
            continue
        if _BULLET.match(line):
            out.append(("bullet", [_BULLET.sub("", line, count=1)]))
            continue
        if out and out[-1][0] in ("bullet", "para"):
            out[-1][1].append(line)
            continue
        out.append(("para", [line]))
    return [(k, " ".join(v)) for k, v in out if k != "gap" and v]


def derive_units(lines) -> tuple[list[Unit], list[Marker]]:
    """The SINGLE derivation, run over canon's block and the delta's block alike.

    That single-ness is the property that protects the comparison: a derivation
    bug is symmetric and can only make the family quiet, never make it invent a
    finding.

    ORDER IS NORMATIVE:

    0. FENCED CODE BLOCKS ARE DROPPED FIRST (ruled 2026-08-27). A fence can
       contain anything — including this very delta's two written-out marker
       examples, which are of complete marker form and promote into canon.
    1. Split into the BODY region — everything above the first
       `#### Scenario:` — and one region per scenario.
    2. Group each region into bullets and paragraphs.
    3. Classify each PARAGRAPH: marker form first (no unit at all), then dated
       bold note (ONE undivided unit), then sentences.
    4. Each BULLET is one unit with its list marker stripped. Applied on BOTH
       sides, so it cannot make an absent unit look present — it can only stop a
       change of list marker from being reported as a lost obligation.

    KINDS follow position: body region -> `body`; a `#### Scenario:` heading ->
    `scenario-title` carrying the title text alone; a bullet inside a scenario
    region -> `scenario-bullet` with its owning title recorded. A non-bullet
    PARAGRAPH inside a scenario region is a `body` unit (decision O9): it is
    requirement text somebody must carry, and dropping it would let a block move
    an obligation into scenario prose where neither carriage arm could see it.
    """
    lines = list(lines)
    fenced = fenced_regions(lines)
    live = [ln for i, ln in enumerate(lines) if i not in fenced]

    regions: list[tuple[str | None, list[str]]] = [(None, [])]
    for line in live:
        m = _SCENARIO_LINE.match(line)
        if m:
            regions.append((normalize(m.group(1)), []))
            continue
        regions[-1][1].append(line)

    units: list[Unit] = []
    markers: list[Marker] = []
    for scenario, region in regions:
        if scenario is not None:
            units.append(Unit(SCENARIO_TITLE, scenario))
        for kind, text in _blocks(region):
            if kind == "bullet":
                units.append(
                    Unit(SCENARIO_BULLET, text, scenario) if scenario
                    else Unit(BODY, text))
                continue
            marker = parse_marker(text)
            if marker is not None:
                markers.append(marker)
                continue
            if is_dated_bold_note(text):
                units.append(Unit(BODY, text))
                continue
            for sentence in split_sentences(text):
                units.append(Unit(BODY, sentence))
    return units, markers


_ARCHIVE = "archive"


class PromotedRequirement:
    """One `### Requirement:` block of a promoted spec, reduced to units."""

    __slots__ = ("capability", "title", "spec_rel", "units", "scenario_titles")

    def __init__(self, capability: str, title: str, spec_rel: str,
                 units: list[Unit]):
        self.capability = capability
        self.title = title
        self.spec_rel = spec_rel
        self.units = units
        self.scenario_titles = [u.text for u in units
                                if u.kind == SCENARIO_TITLE]


class ActiveBlock:
    """One `### Requirement:` block inside an active change's MODIFIED section."""

    __slots__ = ("change", "capability", "title", "delta_rel", "units",
                 "markers", "renames", "standing")

    def __init__(self, change: str, capability: str, title: str, delta_rel: str,
                 units: list[Unit], markers: list[Marker],
                 renames: list[tuple[str, str]], standing: str | None):
        self.change = change
        self.capability = capability
        self.title = title
        self.delta_rel = delta_rel
        self.units = units
        self.markers = markers
        self.renames = renames
        self.standing = standing


def parse_spec_requirements(text: str, capability: str, spec_rel: str
                            ) -> dict[str, PromotedRequirement]:
    """`{norm(title): PromotedRequirement}` from one promoted spec.

    THE HEADING GRAMMAR IS IMPORTED, not restated: `promotion_fidelity`'s
    `_REQUIREMENT` is the one reader four families already share, and a second
    grammar for the same heading is how two readers of one document come to
    disagree about what it says (`align-status-reader-to-real-lines`).

    THE SECTION STOP IS THE SUBTLE PART. A requirement block ends at the next
    `### Requirement:` heading OR at the next `## ` heading that is not a
    `### ` — the same stop `family_enumeration.requirement_prose` takes. Without
    it the LAST requirement in a spec swallows every trailing `## ` section as
    body units, and every block that modifies it is reported for failing to
    carry text that was never part of the requirement. Silent, and only visible
    on the last requirement of a file.
    """
    req_re = promotion_fidelity._REQUIREMENT
    lines = text.splitlines()
    starts: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        m = req_re.match(line)
        if m:
            starts.append((i, m.group(1)))

    out: dict[str, PromotedRequirement] = {}
    for pos, (start, title) in enumerate(starts):
        limit = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        end = limit
        for i in range(start + 1, limit):
            line = lines[i]
            if line.startswith("## ") and not line.startswith("### "):
                end = i
                break
        units, _markers = derive_units(lines[start + 1:end])
        out[norm(title)] = PromotedRequirement(capability, title, spec_rel,
                                              units)
    return out


def promoted(root: Path, capability: str
             ) -> dict[str, PromotedRequirement] | None:
    """The promoted spec of `capability` in the CHECKED-OUT tree, or None.

    No `WorkingTree`, no `GitRefTree`, no basis option, no `FAMILY_NOTES` entry.
    `dh:206-210` gives this family exactly one basis and says the live-`main`
    reading "would be actively wrong here": an active change lives on a BRANCH,
    so a family reading `main` would measure a delta `main` does not carry
    against canon the branch may have moved. Offering the switch at all would
    advertise a second basis this family must never have.
    """
    rel = CANON_TEMPLATE.format(capability=capability)
    path = root / rel
    if not path.is_file():
        return None
    return parse_spec_requirements(
        path.read_text(encoding="utf-8", errors="replace"), capability, rel)


def _standing(root: Path, change: str) -> str | None:
    """The lifecycle standing an active change's own proposal declares.

    Read for ONE purpose — the two-writers arm's `ratified` scoping, which
    `release-realization` owns and this family does not widen. It NEVER gates
    whether a block is read: `dh:30-36` makes the arms read every active change
    regardless of standing, because a `draft` packet's block is as capable of
    restating stale canon as a `ratified` one.

    Through `corpus.parse_status` and `promotion_fidelity.declared_standing` —
    the one lifecycle header reader and the one annotation-tolerant token
    reader — never a private regex.
    """
    path = root / "openspec" / "changes" / change / "proposal.md"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    return promotion_fidelity.declared_standing(corpus.parse_status(text))


def active_blocks(root: Path) -> list[ActiveBlock]:
    """Every MODIFIED requirement block of every ACTIVE change, in a stable order.

    `openspec/changes/archive/` is excluded HERE rather than in the glob: an
    archived block can no longer destroy canon, and `promotion-fidelity` and
    `duplicate-packet` are the families that read those. Excluding it in the
    reader keeps the exclusion visible and testable instead of hidden in a
    pattern.

    The delta is read through `parse_delta`, which already returns operations,
    titles, scenario titles, the raw body lines "in file order and unmodified",
    and the change's `RENAMED` pairs — everything title resolution needs.
    """
    changes = root / "openspec" / "changes"
    if not changes.is_dir():
        return []
    out: list[ActiveBlock] = []
    standings: dict[str, str | None] = {}
    for path in sorted(root.glob(DELTA_GLOB)):
        rel_parts = path.relative_to(root).parts
        change = rel_parts[_CHANGE_PART]
        if change == _ARCHIVE:
            continue
        capability = rel_parts[-2]
        requirements, renames = parse_delta(
            path.read_text(encoding="utf-8", errors="replace"))
        modified = [r for r in requirements if r.op == "MODIFIED"]
        if not modified:
            continue
        if change not in standings:
            standings[change] = _standing(root, change)
        delta_rel = path.relative_to(root).as_posix()
        for req in modified:
            units, markers = derive_units(req.body)
            out.append(ActiveBlock(change, capability, req.title, delta_rel,
                                   units, markers, list(renames),
                                   standings[change]))
    return out



def _finding(severity: str, repo: str, block: ActiveBlock, rule: str) -> Finding:
    return Finding(severity, FAMILY, repo, block.delta_rel, rule, _ACTION)


def _arm_titles(repo: str, block: ActiveBlock, basis: PromotedRequirement,
                suppressed: set[tuple[str, str]] = frozenset()
                ) -> list[Finding]:
    """ARM 1 — scenario-title completeness. The arm that carries the gate.

    Every `#### Scenario:` title the basis carries that the block does not, and
    that no marker declares. ONE finding per requirement, listing every omitted
    title IN FULL and in canon order.

    NO TRUNCATION, deliberately unlike `promotion_fidelity`'s "+N more" at
    three: that family's reader opens the archived delta next, while this arm's
    whole value is a list the author can act on without opening anything. Titles
    are short.

    THIS is the arm `add-modified-block-currency-check` § 7.2 reserves for the
    flip to `error`, and the reason is its inputs: short titled strings rather
    than prose, reporting deletion at the granularity the defect occurs at. Its
    standing population on this repository is ONE finding, so the precedent rule
    — a flip "SHALL follow the discharge of the standing population rather than
    precede it" — is satisfied by a single marker line rather than a campaign.
    """
    canon_titles = [u for u in basis.units if u.kind == SCENARIO_TITLE]
    block_titles = [u for u in block.units if u.kind == SCENARIO_TITLE]
    missing = [u for u in carried(canon_titles, block_titles)
               if u.pair() not in suppressed]
    if not missing:
        return []
    named = ", ".join(repr(u.text) for u in missing)
    return [_finding(
        _LAUNCH_SEVERITY, repo, block,
        f"active MODIFIED block for {block.title!r} omits {len(missing)} of the "
        f"{len(canon_titles)} scenarios {basis.spec_rel} currently states for "
        f"it: {named}")]




# The elision width for a unit quoted inside a ledger finding. Deterministic and
# dumb on purpose: document order, a fixed character cut, and the COUNT always
# stated in full. Nothing is ordered by length, nothing is hashed, and nothing is
# dropped — a reader who needs the whole unit opens the spec the finding names.
_QUOTE_WIDTH = 140

_KIND_LABEL = {BODY: "body", SCENARIO_TITLE: "title", SCENARIO_BULLET: "bullet"}


def _quote(unit: Unit) -> str:
    text = unit.text
    if len(text) > _QUOTE_WIDTH:
        text = text[:_QUOTE_WIDTH].rstrip() + "…"
    return f"[{_KIND_LABEL[unit.kind]}] {text!r}"


def _arm_ledger(repo: str, block: ActiveBlock, basis: PromotedRequirement,
                suppressed: set[tuple[str, str]] = frozenset()
                ) -> list[Finding]:
    """ARM 2 — the carriage ledger. Editorial, and it says so in the finding.

    Every BODY unit and every SCENARIO BULLET of the basis the block does not
    carry, as AT MOST ONE finding per requirement.

    BULLETS ARE POOLED ACROSS THE WHOLE BLOCK, never compared scenario by
    scenario. `carried` gets that for free — `Unit.scenario` is not part of
    equality — and it is the delta's rule for a measured reason: the review's
    fixture renamed a scenario, declared the rename, dropped two of four
    bullets, and a scenario-paired comparison saw NOTHING. Four obligations
    gone, zero findings. The chosen consequence is stated rather than
    discovered: a bullet moved verbatim under a DIFFERENT heading is carried and
    this arm says nothing about it, because the arm reads carriage, not meaning,
    and cannot tell a sensible relocation from a careless one. What it
    guarantees is that the obligation is still written somewhere in the block.

    THE HEDGE IS PART OF THE FINDING, not a footnote in the docs. `dh:252-255`
    requires the finding not to assert that a divergence is unintended, and the
    only place that promise can be kept is the text a reader actually sees.
    """
    kinds = (BODY, SCENARIO_BULLET)
    canon_units = [u for u in basis.units if u.kind in kinds]
    block_units = [u for u in block.units if u.kind in kinds]
    missing = [u for u in carried(canon_units, block_units)
               if u.pair() not in suppressed]
    if not missing:
        return []
    listed = "; ".join(_quote(u) for u in missing)
    return [_finding(
        _LEDGER_SEVERITY, repo, block,
        f"active MODIFIED block for {block.title!r} does not carry "
        f"{len(missing)} of the {len(canon_units)} body units and scenario "
        f"bullets {basis.spec_rel} currently states for it — a divergence this "
        f"arm CANNOT distinguish from a deliberate rewording, and does not "
        f"claim to: {listed}")]


def suppression(markers: list[Marker], canon_units: list[Unit],
                block_units: list[Unit]
                ) -> tuple[set[tuple[str, str]], list[Marker]]:
    """`(suppressed, defective)` — what the block's markers declare, and which of
    them declare nothing.

    THE THREE-WAY RESOLUTION, per name, against canon units of ANY kind:

    - the name matches an ABSENT canon unit -> that unit is suppressed;
    - the name matches a canon unit the block still CARRIES -> the MARKER is
      reported and nothing is suppressed by that name, because a declaration
      that does not describe the block is a declaration no reader can rely on;
    - the name matches NO canon unit -> nothing suppressed, nothing reported.
      That third case is fail-closed and is deliberately NOT a finding: the
      delta mandates exactly one reporting case for a marker, and adding a
      second is an obligation this feature has no standing to invent. Recorded
      as a plausible later ruling.

    THEN THE SCENARIO-TITLE EXTENSION, and it is gated. Where a `Removed from
    canon` marker names an absent scenario TITLE **and the block adds no
    scenario title canon does not already carry**, the bullets that scenario
    carried in canon are declared removed with it — unless they appear as
    bullets anywhere in the block, in which case they are carried and nothing is
    reported either way.

    WHERE THE BLOCK DOES ADD A NEW TITLE the extension does not apply AT ALL.
    That shape is a RETITLE whatever the marker calls it, and treating it as a
    removal reopens the defect the bullet arm exists to close: name the old
    title removed, add a replacement carrying two of its four bullets, and two
    obligations leave canon with nothing reported. The author's instrument for a
    retitle is `Merged into`, whose bullets must be carried somewhere in the
    block or named individually.

    The `Merged into` DESTINATION is never a name — it states where the
    superseded scenarios went and is present in the block by construction, so
    reading it as a named unit would make every valid merge marker report
    itself.

    **A MARKER IS VOIDED PER NAME, NOT WHOLLY. RULED 2026-08-27.** A marker
    naming three units, one of which the block still carries, is REPORTED — and
    it still suppresses the two that are genuinely absent. The alternative,
    voiding the whole marker, would turn one wrong name into a cascade: the two
    sound declarations would be discarded too and their units would surface as
    fresh carriage findings, so the author would be shown three problems where
    they made one mistake, and the two rows they had already deliberated would
    come back. Per-name keeps the report proportional to the error, and the
    marker-defect finding names exactly which name failed. `dh:153-156` supports
    it directly: suppression is defined per unit ("only the units it names AND
    that are in fact absent"), and the reporting rule is about the marker rather
    than about its other names.
    """
    have = {u.pair() for u in block_units}
    by_text: dict[str, list[Unit]] = {}
    for u in canon_units:
        by_text.setdefault(u.text, []).append(u)

    canon_titles = {u.text for u in canon_units if u.kind == SCENARIO_TITLE}
    block_titles = {u.text for u in block_units if u.kind == SCENARIO_TITLE}
    adds_new_title = bool(block_titles - canon_titles)

    suppressed: set[tuple[str, str]] = set()
    defective: list[Marker] = []
    for marker in markers:
        for name in marker.names:
            matches = by_text.get(name)
            if not matches:
                continue                    # names nothing; buys nothing
            if any(u.pair() in have for u in matches):
                if marker not in defective:
                    defective.append(marker)
                continue
            for unit in matches:
                suppressed.add(unit.pair())
                if (unit.kind == SCENARIO_TITLE
                        and marker.form == "removed"
                        and not adds_new_title):
                    for bullet in canon_units:
                        if (bullet.kind == SCENARIO_BULLET
                                and bullet.scenario == unit.text
                                and bullet.pair() not in have):
                            suppressed.add(bullet.pair())
    return suppressed, defective


_MARKER_ACTION = ("name a unit the block does not restate, or drop the "
                  "declaration — a marker that does not describe the block "
                  "declares nothing")


def _arm_marker_defects(repo: str, block: ActiveBlock, defective: list[Marker],
                        ) -> list[Finding]:
    """THE FOURTH FINDING CLASS — a defect in a DECLARATION, not a comparison.

    Three arms, five classes, and the numbers differ on purpose: the arms read
    two documents against each other, this reads one paragraph against the block
    it sits in, and the fifth reads the class map's own verdict. It carries the ledger's `info` band so the advisory launch
    holds in both halves, and it deliberately does NOT carry the ledger's hedge:
    a marker naming a unit the block still restates is wrong with certainty.
    """
    out: list[Finding] = []
    for marker in defective:
        named = ", ".join(repr(n) for n in marker.names)
        out.append(Finding(
            _LEDGER_SEVERITY, FAMILY, repo, block.delta_rel,
            f"active MODIFIED block for {block.title!r} carries a "
            f"{marker.form!r} marker by {marker.change_id} ({marker.date}) "
            f"naming {named}, which the block still restates — a declaration "
            f"that does not describe the block", _MARKER_ACTION))
    return out


_RATIFIED = "ratified"


def sibling_titles(root: Path) -> set[tuple[str, str]]:
    """`{(capability, norm(title))}` that some ACTIVE change ADDS or RENAMES to.

    A MODIFIED title landing here is PENDING, not absent (`dh:278-280`), and
    pending means there is nothing to compare: the promoted requirement does not
    exist yet, so no basis is synthesized from the sibling's ADDED text. RULED
    2026-08-27 — the earlier reading, which built a basis from the addition,
    would have measured all seven of this corpus's
    MODIFIED-over-a-sibling's-ADDED pairs against text no promoted requirement
    carries.
    """
    changes = root / "openspec" / "changes"
    if not changes.is_dir():
        return set()
    out: set[tuple[str, str]] = set()
    for path in sorted(root.glob(DELTA_GLOB)):
        parts = path.relative_to(root).parts
        if parts[_CHANGE_PART] == _ARCHIVE:
            continue
        capability = parts[-2]
        requirements, renames = parse_delta(
            path.read_text(encoding="utf-8", errors="replace"))
        for req in requirements:
            if req.op == "ADDED":
                out.add((capability, norm(req.title)))
        for _old, new in renames:
            out.add((capability, norm(new)))
    return out


def resolve(block: ActiveBlock, canon: dict[str, PromotedRequirement] | None,
            siblings: set[tuple[str, str]]):
    """`(basis, status)` for one block. `status` is why, and the caller reports it.

    THE ORDER IS THE DELTA'S (`dh:58-64`):

    1. canon carries the title -> compare against it;
    2. else the change's OWN `## RENAMED Requirements` renames a promoted
       requirement TO this title -> compare against canon under the OLD NAME, and
       the three arms RUN, because a rename changes a title rather than the
       content a block must carry. Without this the family would report every
       rename-and-amend change as unresolved AND compare nothing where it should
       compare everything;
    3. else an active sibling ADDS or RENAMES to this title -> PENDING; nothing
       is compared and nothing is reported;
    4. else -> unresolved, and reported.
    """
    key = norm(block.title)
    if canon and key in canon:
        return canon[key], "canon"
    for old, new in block.renames:
        if norm(new) == key and canon and norm(old) in canon:
            return canon[norm(old)], "own-rename"
    if (block.capability, key) in siblings:
        return None, "pending"
    return None, "unresolved"


def declarations(root: Path, blocks: list[ActiveBlock]
                 ) -> set[tuple[str, str]]:
    """`{(declarer, declared)}` among `blocks`, read from each change's proposal.

    THE DECLARATION IS THE ORDERING (ruled 2026-08-27, Brett, verbatim "By
    declaration"). `release-realization`'s "Ordered deltas and branch
    vocabulary" already requires the later proposal to reference the earlier
    change and declare its deltas relative to that change's outcome, so the
    change that makes the declaration IS the later writer and nothing else needs
    to decide it. No folder name, commit timestamp or `created:` date is
    consulted — a second authority for an ordering one rule already owns is the
    defect "Explicit delta rule" names.

    The match is `duplicate_packet._mention`, IMPORTED rather than re-spelled:
    the delta names it by reference ("the whole-token match the duplicate packet
    family already uses"), its boundaries are `[\\w-]` rather than `\\b` because
    change ids are hyphenated, and one change id occurring inside a longer one
    satisfies nothing. Its docstring carries the false-exemption channel that
    shape closes.

    ONE ACCEPTED CONSEQUENCE, noted rather than hidden: `/` is a boundary, so a
    proposal citing `openspec/changes/<sibling>/tasks.md` counts as naming the
    sibling. A proposal citing a sibling's path IS referencing that change in the
    ordinary reading of the rule, and the alternative is a second, stricter
    matcher for a question one function already owns.
    """
    texts: dict[str, str] = {}
    for change in {b.change for b in blocks}:
        path = root / "openspec" / "changes" / change / "proposal.md"
        texts[change] = (path.read_text(encoding="utf-8", errors="replace")
                         if path.is_file() else "")
    out: set[tuple[str, str]] = set()
    changes = sorted(texts)
    for declarer in changes:
        for declared in changes:
            if declarer == declared:
                continue
            if _mention(declared).search(texts[declarer]):
                out.add((declarer, declared))
    return out


def _as_basis(block: ActiveBlock) -> PromotedRequirement:
    """One active block AS the outcome its declaring sibling is measured against.

    `MODIFIED` REPLACES A REQUIREMENT WHOLESALE, so the outcome of the earlier
    writer's block simply IS that block — there is nothing of canon left to
    merge. The `spec_rel` carried here is the SIBLING'S DELTA PATH, so a finding
    says where the text it was measured against actually came from rather than
    naming a promoted spec that does not yet hold it.
    """
    return PromotedRequirement(block.capability, block.title, block.delta_rel,
                               block.units)


def _arm_ordering(repo: str, group: list[ActiveBlock], declared: set
                  ) -> tuple[dict[str, PromotedRequirement], list[Finding]]:
    """`(basis_override, findings)` for one (capability, requirement) group.

    Exactly TWO active RATIFIED writers with EXACTLY ONE declaration between them
    is the ordered case: the declarer is the later writer and its basis becomes
    the other's block. That substitution IS THE WHOLE EFFECT — the arms then run
    unchanged, so an addition the sibling makes that the declaring block does not
    carry is reported BY THE CARRIAGE ARMS. A separate finding here would report
    at `warning` the same units the ledger reports at `info`, and `dh:264` asks
    for the addition to be reported, not reported twice.

    Everything else among two-or-more ratified writers is an UNSTATED ordering,
    reported against every one of their blocks, each measured against canon:

    - NEITHER declaring — "no reader being able to tell which text canon will
      keep";
    - BOTH declaring — "mutual declaration deciding nothing";
    - THREE OR MORE ratified writers, whatever they declare. The delta gives no
      rule for that shape (`dh:262` says "two or more" and then describes a
      pair), one declaration orders a pair and leaves the third unstated, and
      inventing a chain rule for a population of zero would be inventing
      authority. Reported, and the gap is named in the feature plan.

    An UNRATIFIED writer creates no obligation either way: `release-realization`
    scopes the rule to an active RATIFIED change and this family does not widen
    it. Its block is still read, because the arms are advisory.
    """
    ratified = [b for b in group if b.standing == _RATIFIED]
    if len(ratified) < 2:
        return {}, []
    pairs = {(a.change, b.change) for a in ratified for b in ratified
             if (a.change, b.change) in declared}
    if len(ratified) == 2 and len(pairs) == 1:
        declarer, other = next(iter(pairs))
        by_change = {b.change: b for b in ratified}
        return {declarer: _as_basis(by_change[other])}, []

    names = ", ".join(sorted(b.change for b in ratified))
    if len(ratified) > 2:
        why = (f"{len(ratified)} active ratified changes write it and the "
               f"ordering rule states no order for more than two")
    elif pairs:
        why = (f"{len(pairs)} declarations stand between them, and mutual "
               f"declaration decides nothing")
    else:
        why = ("neither names the other, so the ordering is unstated rather "
               "than merely unrecorded")
    findings = [
        _finding(_RESOLUTION_SEVERITY, repo, block,
                 f"the ordering of MODIFIED blocks for {block.title!r} is "
                 f"undecided: {names} — {why}; each block is meanwhile measured "
                 f"against canon, the only basis a reader can name")
        for block in ratified]
    return {}, findings


def _report_order(finding):
    """The family's own report order: severity, then repo, then path, then rule.

    Named rather than inlined because it is now applied TWICE — once to the
    arms' findings, and again after the fifth class's emit appends to them. Two
    copies of an ordering rule is how two orderings come to differ.
    """
    return (SEVERITY_RANK[finding.severity], finding.repo, finding.path,
            finding.rule)


def fam_modified_block_currency(ctx):
    """Every active MODIFIED block, against the canon it has not yet replaced.

    A finding lands on the DELTA's own path, not on the promoted spec's, because
    the delta is the document making the claim that went unmet and — unlike
    promotion fidelity's archived paths — it is a document somebody can still
    edit. That is the whole point of asking the question here: the remedy is one
    line at authoring time instead of a repair at an archive gate.
    """
    scoped = [(repo, Path(path)) for repo, path in sorted(ctx.repo_paths.items())
              if (Path(path) / "openspec" / "changes").is_dir()]
    if not scoped:
        return Skip(FAMILY, "no repository in scope carries an "
                            "`openspec/changes/` directory this family can read")

    dispositions = promotion_fidelity.load_dispositions(ctx, FAMILY)
    findings: list[Finding] = []
    for repo, root in scoped:
        blocks = active_blocks(root)
        if not blocks:
            continue
        siblings = sibling_titles(root)
        declared = declarations(root, blocks)
        canon_cache: dict[str, dict[str, PromotedRequirement] | None] = {}

        def canon_for(capability: str, root=root):
            if capability not in canon_cache:
                canon_cache[capability] = promoted(root, capability)
            return canon_cache[capability]

        groups: dict[tuple[str, str], list[ActiveBlock]] = {}
        for block in blocks:
            groups.setdefault((block.capability, norm(block.title)),
                              []).append(block)

        for key in sorted(groups):
            group = groups[key]
            override, ordering = _arm_ordering(repo, group, declared)
            findings.extend(
                f for f in ordering
                if not promotion_fidelity.disposed(dispositions, repo, f.path,
                                                   group[0].title))
            for block in group:
                if promotion_fidelity.disposed(dispositions, repo,
                                               block.delta_rel, block.title):
                    continue
                basis, status = resolve(block, canon_for(block.capability),
                                        siblings)
                if status == "pending":
                    continue
                if basis is None:
                    findings.append(_unresolved_finding(repo, block, root))
                    continue
                basis = override.get(block.change, basis)
                suppressed, defective = suppression(
                    block.markers, basis.units, block.units)
                findings.extend(_arm_titles(repo, block, basis, suppressed))
                findings.extend(_arm_ledger(repo, block, basis, suppressed))
                findings.extend(_arm_marker_defects(repo, block, defective))
    # SORTED BY THE FAMILY ITSELF, SEVERITY FIRST. `runner.run_suite` sorts the
    # whole report, so an unsorted family is invisible there and visible
    # immediately in a `--family` run — which is the run a session uses while
    # fixing a block, and the run a regression diff is taken from.
    #
    # SEVERITY LEADS THE KEY BY RULING (2026-08-27), and it is not cosmetic. The
    # ledger's population is standing by construction — every legitimate MODIFIED
    # block edits something — so on any real tree the ONE gate-bearing `warning`
    # is outnumbered by editorial `info` rows, and under a path-first sort it
    # rendered somewhere in the middle of them. The arm the flip in § 7.2
    # reserves must be the arm a reader sees first, or the precise signal is
    # buried in the editorial ones, which is the exact failure the delta split
    # the arms to avoid. `SEVERITY_RANK` is the package's own ordering
    # (critical, error, warning, info), so this agrees with the report-wide sort
    # rather than inventing a second one.
    findings.sort(key=_report_order)
    # THE FIFTH CLASS'S EMIT — `add-unclassified-finding-class`. AFTER the arms
    # and, load-bearingly, AFTER the sort: "the FIRST of that shape" is defined
    # in the family's own report order and is undefined over an unsorted list.
    #
    # AND THERE IS NO SECOND SORT, deliberately. The first cut appended and then
    # re-sorted, which read as tidy and was dead code: `runner.run_suite` sorts
    # the whole result by `Finding.sort_key` and `report.render` sorts again
    # before it prints, so the order this list is RETURNED in reaches no reader.
    # A mutation round proved it — deleting that second sort killed nothing —
    # and a line no test can fail is a line that will be trusted for a guarantee
    # it does not give. The sort ABOVE stays because it decides which finding
    # each drift warning names, which is a fact about the OUTPUT.
    findings.extend(_drift_findings(findings))
    return findings


def _unresolved_finding(repo: str, block: ActiveBlock, root: Path) -> Finding:
    """A block modifying nothing — reported, because its promotion "adds text
    nobody reviewed as an addition".

    The two shapes are named apart in the rule text. A capability with NO
    promoted spec at all is a different code path from a spec that exists
    without the title, and a reader who is told which one it is knows whether to
    look for a missing file or a missing requirement.
    """
    spec_rel = CANON_TEMPLATE.format(capability=block.capability)
    if not (root / spec_rel).is_file():
        why = f"capability {block.capability!r} has no promoted spec at all"
    else:
        why = f"{spec_rel} states no requirement under that title"
    return _finding(
        _RESOLUTION_SEVERITY, repo, block,
        f"active MODIFIED block for {block.title!r} resolves to no promoted "
        f"requirement, no rename of its own, and no active sibling's addition: "
        f"{why}")


# ============================================================================
# THE REPORT SECTION — F4 (`022-modified-block-currency-reporting`, packet § 5)
# ============================================================================
#
# WHY ANY OF THIS EXISTS. The classes above are already distinct FINDINGS
# with distinct severities, which is what the delta requires ("SHALL report them
# as distinct finding classes so that a precise signal is never buried in an
# editorial one"). The REPORT did not carry the distinction: `report.render`
# prints a family's findings as a flat list of rows, and on any real tree the one
# gate-bearing `warning` sits among a standing population of editorial `info`
# rows, each of them long enough to fill three lines. Learning "one scenario was
# dropped, eight blocks diverge editorially" meant reading all nine and tallying.
# Packet § 5.1 asks for the split to be visible WITHOUT COUNTING.
#
# WHAT IS ADDED IS A RENDERING, NOT A MEASUREMENT. `class_summary` is a function
# of the findings the report is about to print and of nothing else — no context,
# no second corpus read, no re-run. Nothing here is ever wrapped in a `Finding`,
# so nothing here reaches the ranked plan, the headline counts, the regression
# diff or the uncited-resolution rule. The precedent is `families.FAMILY_NOTES`,
# whose lines render in the same position for the same reason; the difference is
# that a note answers "which tree did this family measure" (a fact about the
# RUN) while this answers "how did its findings split" (a fact about the
# FINDINGS), which is why it is a sibling registry and not a widening of that
# one.


class FindingClass:
    """One of this family's five finding classes, as a value.

    `band` and `action` are read from the module constants rather than
    re-spelled. They are used differently and the difference matters:

    - `band` IS RENDERED, in the subtotal's parenthetical, so § 7.2's flip of
      `_LAUNCH_SEVERITY` to `error` moves the rendered caption with it. A
      literal `"warning"` here would keep rendering after the flip and would
      then describe the report wrongly — a caption that outlives its subject.
    - `action` IS NOT RENDERED by `class_summary`; the ranked plan is where a
      finding's action appears, via `report.plan_line`. It is carried here so
      the per-class pin has a single source
      (`test_every_finding_carries_its_class_s_band_and_action`), which is what
      keeps `_ACTION` and `_MARKER_ACTION` attached to the classes that use
      them rather than re-spelled in a test.

    `gloss` is the parenthetical a reader gets beside the band. Two of the five
    carry one and three do not: the scenario-title arm's says it carries the
    gate, and the ledger's repeats the hedge every one of its findings already
    states. Adding a gloss to the other three would pad a line whose whole value
    is being short enough to read at a glance.
    """

    __slots__ = ("id", "label", "band", "action", "gloss")

    def __init__(self, id: str, label: str, band: str, action: str,
                 gloss: str = ""):
        self.id = id
        self.label = label
        self.band = band
        self.action = action
        self.gloss = gloss


CLASS_TITLES = "scenario-titles"
CLASS_LEDGER = "carriage-ledger"
CLASS_RESOLUTION = "title-resolution"
CLASS_MARKERS = "marker-defects"
# THE FIFTH, AND NEITHER THE ID NOR THE LABEL MAY CONTAIN `unclassified`.
# `test_a_finding_the_map_cannot_place_is_counted_and_named` asserts that
# string's ABSENCE from a fully-classified summary, and a class label renders
# even at a count of zero — so the obvious name would have reddened a standing
# pin for a real reason. `unplaced` says the same thing about the FINDING that
# `unclassified` says about the residual, which is the distinction this class
# exists to draw.
CLASS_DRIFT = "unplaced"

# The fifth class's action, and it names BOTH remedies. NO INTERPOLATED PATH:
# `test_every_finding_carries_its_class_s_band_and_action` compares
# `f.action == klass.action` against a class constant, so a per-finding path
# here would make every drift finding's action differ from its class's. The
# delta path is already the finding's own `path` field, and the drifted rule
# text is quoted in the finding itself.
_DRIFT_ACTION = ("extend the class map in "
                 "`scripts/doc_health/modified_block_currency.py`, or fix the "
                 "drifted rule text the finding names")

# The residual bucket's name. NOT a class — a class is something the delta
# defines, and this is the report saying that the map and the arms have drifted
# apart.
UNCLASSIFIED = "unclassified"

# ORDERED, and the order is the contract. The gate-bearing arm reads FIRST, for
# the same reason `fam_modified_block_currency` sorts its own findings
# severity-first (see its ruling of 2026-08-27): the arm the flip in § 7.2
# reserves must be the arm a reader meets first, or the precise signal is buried
# in the editorial ones — the exact failure the delta split the arms to avoid.
#
# FIVE ENTRIES FOR SIX RULE SHAPES. The delta's third arm is "Title resolution
# and ordering": a block resolving to nothing and an ordering no declaration
# settles are two shapes of ONE arm, sharing a severity and an action, named
# together in the requirement. Splitting them here would claim a class the delta
# does not define; merging any other pair would hide a severity difference. The
# sixth shape is the fifth class's own finding, which the map must place or the
# count would name itself.
CLASSES = (
    FindingClass(CLASS_TITLES, "scenario-title completeness",
                 _LAUNCH_SEVERITY, _ACTION,
                 " — the arm carrying this family's gate"),
    FindingClass(CLASS_LEDGER, "carriage ledger",
                 _LEDGER_SEVERITY, _ACTION,
                 " — editorial, and the arm says so in every finding"),
    FindingClass(CLASS_RESOLUTION, "title resolution and ordering",
                 _RESOLUTION_SEVERITY, _ACTION),
    FindingClass(CLASS_MARKERS, "marker defects",
                 _LEDGER_SEVERITY, _MARKER_ACTION),
    # LAST, because it is not an arm and the ordering comment above is about the
    # arms: "the gate-bearing arm reads FIRST" is unchanged by appending here.
    # NO GLOSS, on the rule stated in `FindingClass` — the label already says
    # what it is, and a fifth parenthetical would pad the one line whose whole
    # value is being short enough to read at a glance.
    FindingClass(CLASS_DRIFT, "unplaced-finding drift",
                 _DRIFT_SEVERITY, _DRIFT_ACTION),
)

# A requirement title as the arms write it: `{title!r}`, which is single-quoted
# unless the title contains a single quote, in which case Python switches to
# double quotes. Both admitted, escapes included.
_TITLE_REPR = r"(?:'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\")"

# THE ANCHOR, AND IT IS LOAD-BEARING. Every pattern below matches from the START
# of the rule and past the CLOSING QUOTE of the title, because titles come from
# the corpus and may contain any phrase — including another class's. Measured: a
# carriage-ledger finding for a requirement titled
# `'X omits 1 of the 2 scenarios Y'` matches an unanchored titles probe as well
# as the ledger one, and a first-match-wins classifier files an `info` row under
# the gate-bearing arm. That is a wrong number on the one line § 5.1 exists so a
# reader can trust without counting.
_BLOCK_HEAD = r"^active MODIFIED block for " + _TITLE_REPR + " "

_CLASS_PATTERNS = (
    (CLASS_TITLES, re.compile(
        _BLOCK_HEAD + r"omits \d+ of the \d+ scenarios ")),
    (CLASS_LEDGER, re.compile(
        _BLOCK_HEAD + r"does not carry \d+ of the \d+ body units and scenario "
                      r"bullets ")),
    (CLASS_MARKERS, re.compile(
        _BLOCK_HEAD + r"carries a '\w+' marker by ")),
    (CLASS_RESOLUTION, re.compile(
        _BLOCK_HEAD + r"resolves to no promoted requirement, ")),
    (CLASS_RESOLUTION, re.compile(
        r"^the ordering of MODIFIED blocks for " + _TITLE_REPR
        + r" is undecided: ")),
    # THE FIFTH CLASS, AND ITS ANCHOR IS LOAD-BEARING TWICE OVER. This finding
    # QUOTES a rule text the map could not place, and that quotation may itself
    # begin in the shape of an arm's — so an unanchored probe would file the
    # drift finding under whichever class its QUOTATION resembles, which is the
    # misfiling `_BLOCK_HEAD` was measured into existence to prevent. And in the
    # other direction: a requirement may be TITLED with this class's own opening
    # phrase, in which case its ledger finding's rule text contains that phrase;
    # a `.*`-prefixed probe (which `re.match` accepts) would match that ledger
    # finding too, and two patterns matching one rule reds the partition pin.
    # Measured on both:
    # `test_a_drift_finding_quoting_an_arm_shaped_rule_text_is_not_misfiled` and
    # `test_a_title_that_embeds_the_drift_phrase_still_matches_exactly_one_pattern`.
    (CLASS_DRIFT, re.compile(
        r"^this family's own class map has no pattern for \d+ findings? this "
        r"run emitted, ")),
)


def classify(finding) -> str:
    """The class id of one of this family's findings, or `UNCLASSIFIED`.

    FAIL-CLOSED (constitution VII). A rule text this map does not recognize is
    NOT absorbed into a neighbouring class: it returns `UNCLASSIFIED` and the
    summary renders a named residual row for it. The alternative — a nearest
    match, or a silent drop — turns a rule-text edit into a wrong number on a
    line a reader is being asked to trust instead of counting.

    Read off the RULE TEXT rather than off a field of `Finding`, because
    `Finding` is shared by twenty-two families and the semantic lanes: a field
    added for one family's report line would be a change to a shared grammar for
    a local need. The drift that reading costs is made loud two ways —
    `test_every_finding_over_the_fixture_corpus_lands_in_exactly_one_class` over
    thirteen fixture trees and the real tree, and the residual row on the
    artifact itself.
    """
    for class_id, pattern in _CLASS_PATTERNS:
        if pattern.match(finding.rule):
            return class_id
    return UNCLASSIFIED


# The fifth class's rule text. `{n}` is how many of the run's findings carry the
# shape, `{s}` pluralizes it, and `{rule}` is the FIRST of them VERBATIM —
# plain, never `repr`-wrapped, because a `repr` would escape the rule's own
# quotes and the quotation would stop being byte-equal to the rule it names.
# It goes LAST in the sentence so nothing after it can be mistaken for this
# family's own prose.
#
# THE OPENING PHRASE IS DELIBERATELY NOT `_UNCLASSIFIED_LINE`'s. The residual row
# says "its own class map does not place"; this says "has no pattern for". Two
# readings of one fact, two spellings — so that
# `test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree`'s
# probe can be asserted to be THIS constant's wording rather than matching the
# row's as well, which would make its positive control pass against the wrong
# thing.
_DRIFT_RULE = (
    "this family's own class map has no pattern for {n} finding{s} this run "
    "emitted, which share one rule shape the map has drifted behind; the first "
    "of them in this family's own report order reads, verbatim: {rule}")

# THE SHAPE MASK, and its grammar is the class map's own (`_TITLE_REPR` and
# `\d+`) so a reader can check a grouping by eye. TWO placeholders, not one: a
# single filler would make `'a'` and `1` indistinguishable, and a mask that
# loses information is an identity function that merges two remedies into one.
# Deliberately NOT `_FILLER`, which belongs to the DERIVATION's code-span mask —
# two unrelated masks sharing a constant is how one of them acquires the other's
# constraints.
#
# SCOPED TO THIS FAMILY. `add-unclassified-finding-class` § 4.4: this is written
# for this family's rule-text grammar and is NOT a general finding-identity rule
# for the package. Nothing else may import it as one without its own change.
_SHAPE_QUOTED = re.compile(_TITLE_REPR)
_SHAPE_DIGITS = re.compile(r"\d+")
_SHAPE_OPENERS = "'\""


def _shape(rule: str) -> str:
    """The identity two unplaced findings are grouped by.

    Quoted spans first, then digit runs — the order the delta states. The result
    is immaterial to the order (a digit inside a quoted span is masked either
    way, the whole span being replaced), but a reader checking this by eye reads
    it in the delta's order.

    A LEFT-TO-RIGHT CONSUMER, NOT A GLOBAL `re.sub`, AND THE DIFFERENCE IS A BUG
    THIS FUNCTION SHIPPED WITH. These rule texts are FIXED PROSE interleaved
    with `repr`-emitted spans, and one of the fixed prose strings contains an
    apostrophe: `_unresolved_finding`'s "no active sibling's addition:". A global
    substitution pairs THAT apostrophe with the opening quote of the NEXT repr,
    masks the prose between them, and leaves the repr's own content — the
    capability name — exposed. Two unresolved blocks differing only in their
    capability then read as two shapes, and the family reports two remedies for
    one. Measured: `capability 'absent-a'` and `capability 'absent-b'` grouped
    apart.

    So a quote only OPENS a span where a `repr` could have emitted one: at the
    start of the rule, or after a non-alphanumeric. Every one of this family's
    five templates interpolates its `repr` after a space, and an apostrophe
    inside a word never can be. The scan is then unambiguous in both directions
    a regex is not: `_TITLE_REPR`'s two alternatives begin with DIFFERENT
    characters, so at most one can match at any position, and an accepted span
    is jumped past whole, so the scanner never re-enters one it has consumed.

    THE PROSE IS NOT THE FIX. Rewording "sibling's" would change a rule text
    readers and pins depend on, to work around a masking bug; the mask is what
    was wrong.
    """
    out: list[str] = []
    index, end = 0, len(rule)
    while index < end:
        char = rule[index]
        if char in _SHAPE_OPENERS and (index == 0
                                       or not rule[index - 1].isalnum()):
            span = _SHAPE_QUOTED.match(rule, index)
            if span:
                out.append("<Q>")
                index = span.end()
                continue
        out.append(char)
        index += 1
    return _SHAPE_DIGITS.sub("<N>", "".join(out))


def _drift_findings(findings) -> list[Finding]:
    """ONE `warning` per DISTINCT unplaced rule SHAPE — the fifth class's emit.

    NOT AN ARM. The three arms read two documents against each other; this reads
    the CLASS MAP's own verdict on the findings the arms just emitted, which is
    why it lives beside `classify` rather than beside them.

    PER SHAPE, NOT PER RUN AND NOT PER REPOSITORY (`add-unclassified-finding-class`
    D3). Per repository would put ONE remedy into an aggregation run's ranked
    plan once for every repository in scope, the class map being a module
    constant compiled once per process — the reading `family_enumeration`
    already recorded for its missing-direction invariant. Per run collapses two
    genuinely different drifted shapes into one finding quoting only one of
    them.

    THE GRAIN IS NOT "ONE PER REMEDY", AND SAYING SO WOULD BE FALSE. It is ONE
    FINDING PER DISTINCT ARM TEXT AFTER QUOTED-SPAN AND DIGIT MASKING, which is
    FINER. A rule text's UNQUOTED parts are shape-bearing under the delta's
    identity rule — the promoted spec's path, the `[body]`/`[bullet]` kind list
    a ledger finding quotes, a change-id list, an unresolved block's `why`
    clause — so findings a human would discharge with ONE new map entry can be
    several shapes. MEASURED: dropping `carriage-ledger` on this repository
    leaves SEVEN unplaced findings in SIX shapes, and one map entry places all
    seven.

    That is the ratified delta working as written, not a defect here: its third
    scenario pins "rule texts that differ outside their quoted spans and digit
    runs MUST yield two additional findings". Masking the arm's whole TEMPLATE
    instead — every interpolated field, not only the quoted ones — would take
    six to one and would contradict that scenario, so it is a DELTA AMENDMENT
    and not a change this module may make on its own. Open, and recorded in
    `specs/026-unplaced-finding-drift/plan.md`;
    `test_the_drift_grain_is_one_finding_per_masked_arm_text_not_one_per_remedy`
    measures the six so the amendment has a figure to move.

    THE REPRESENTATIVE IS THE FIRST OF ITS SHAPE IN THE FAMILY'S OWN REPORT
    ORDER, so the emit is deterministic: the caller sorts before calling, the
    dict preserves first-appearance order, and the caller sorts again.

    WHAT THIS GIVES UP, NAMED: on an aggregation run one finding names ONE
    example per shape, so a second repository's instance of the SAME shape is
    counted but not quoted.
    """
    shapes: dict[str, list[Finding]] = {}
    for finding in findings:
        if classify(finding) == UNCLASSIFIED:
            shapes.setdefault(_shape(finding.rule), []).append(finding)
    out: list[Finding] = []
    for group in shapes.values():
        first = group[0]
        out.append(Finding(
            _DRIFT_SEVERITY, FAMILY, first.repo, first.path,
            _DRIFT_RULE.format(n=len(group),
                               s="" if len(group) == 1 else "s",
                               rule=first.rule),
            _DRIFT_ACTION))
    return out


def class_counts(findings) -> dict:
    """`{class id -> count}` for every class, plus `UNCLASSIFIED`.

    Every class present including the zeros: a class that vanishes from the line
    when it reads nothing is a class a reader cannot tell from one that was never
    measured.
    """
    counts = {klass.id: 0 for klass in CLASSES}
    counts[UNCLASSIFIED] = 0
    for finding in findings:
        counts[classify(finding)] += 1
    return counts


_SUMMARY_LEAD = ("Finding classes, counted apart so the gate-bearing arm is "
                 "never read as one of the editorial rows:")

_UNCLASSIFIED_LINE = (
    "- " + UNCLASSIFIED + ": {n} — findings this family emitted that its own "
    "class map does not place; the map has drifted from the arms and the "
    "counts above are short by this many")


def class_summary(findings) -> list[str]:
    """The report lines that split this family's findings by class.

    Rendered under the family's own heading, BEFORE its rows, by
    `report.render` through `families.FAMILY_SUMMARIES`. Handed exactly the
    findings the report is about to print for this family, and reading nothing
    else — no context, no filesystem, no second run of the family. That is
    asserted structurally rather than promised
    (`test_the_summary_reads_the_findings_and_nothing_else`).

    THE COUNTS ALWAYS SUM TO THE ROWS. Where they would not, the residual line
    says so and by how many, which is the one honest thing a tally can do about
    its own drift. It is never an exception: a presentational defect must not be
    able to abort a nightly report.
    """
    counts = class_counts(findings)
    lines = [_SUMMARY_LEAD]
    for klass in CLASSES:
        lines.append(f"- {klass.label}: {counts[klass.id]} "
                     f"(`{klass.band}`{klass.gloss})")
    if counts[UNCLASSIFIED]:
        lines.append(_UNCLASSIFIED_LINE.format(n=counts[UNCLASSIFIED]))
    return lines
