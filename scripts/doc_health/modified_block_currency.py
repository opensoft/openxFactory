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

THREE ARMS, SEVEN FINDING CLASSES, AND THE NUMBERS DIFFER ON PURPOSE:

1. **Scenario-title completeness** (`_LAUNCH_SEVERITY`, `error` — flipped
   2026-08-31, issue #357; launched `warning`). Every `#### Scenario:` title
   canon carries must appear as a scenario title in the block. Short titled
   strings rather than prose, reporting deletion at the granularity the defect
   occurs at. THIS is the arm that carries the family's gate, and the only arm
   the flip in `tasks.md` § 7.2 moves.
2. **The carriage ledger** (`_LEDGER_SEVERITY`, `info`). Every body unit and
   every scenario bullet the block does not carry, as AT MOST ONE finding per
   requirement. It CANNOT distinguish a deliberate rewording from stale text and
   its rule text says so: it is the list a reviewer reads to confirm each
   divergence was intended.
3. **Title resolution and ordering** (`_RESOLUTION_SEVERITY`, `warning`). A
   block whose title resolves to nothing, and an ordering among active RATIFIED
   writers that no declaration settles — TWO writers by the single declaration
   between them, THREE OR MORE by whether their declarations state one linear
   chain (issue #627, 2026-09-04; before it every larger group was reported
   whatever it declared, on a measured population of zero).
4. **Marker defects** (`_LEDGER_SEVERITY`, `info`) — not an arm, and FIVE
   GROUNDS: three since `amend-marker-defect-reporting` (2026-09-09,
   openxFactory issue #729) and two since `amend-marker-declaring-nothing`
   (2026-09-10, openxFactory issues #856 and #860). A marker that names a unit
   the block still carries; a marker whose REASON quotes a code span exactly
   matching a promoted unit the block leaves out and that marker does not also
   NAME before its reason boundary, which under that boundary declares nothing;
   a marker naming something that matches no unit of the promoted requirement or
   of the block; a marker naming something that matches no unit of the promoted
   requirement and IS a unit the block itself adds, declaring removed from canon
   what canon never carried; and a `Removed from canon` marker whose tail
   carries no code span at all, which names nothing, quotes nothing and declares
   nothing while the paragraph is exempt from carriage for being of marker form.
   Each ground is one finding, because each is one remedy. None of them
   inherits the ledger's hedge: a marker that does not describe the block is
   wrong with certainty.
5. **Sibling pairing** (`_PAIRING_SEVERITY`, `warning`) — not an arm either,
   and it compares NO requirement text. A MODIFIED block whose title resolves
   to an active sibling's ADDITION (or to the `TO:` half of an active rename)
   is the shape `resolve` returns as `pending`, and until
   `govern-sibling-added-modified-deltas` the block was DROPPED before any arm
   looked at it — so the arms' silence read as clearance when it was
   uncomparability. This class reads the PAIRING: the block's `Modified over`
   markers and the set of active additions, in four reported states
   (self-referential, undeclared, misdeclared, undisclosed) and silent on the
   fifth. The three comparison arms still do NOT run against such a block; the
   2026-08-27 ruling against synthesising a basis from the sibling's ADDED text
   is untouched.
6. **Added-over-canon collision** (`_COLLISION_SEVERITY`, `warning`) — not an
   arm, and it reads no MODIFIED block at all. An active `## ADDED
   Requirements` block, or the `TO:` half of an active `## RENAMED
   Requirements` block, naming a title the promoted specification ALREADY
   carries. That is the surviving evidence of the unsafe archive order — the
   modifying writer archived first and its block promoted text nobody reviewed
   as an addition — and it is the only backstop that can exist from inside a
   health run, an archive act being outside what any run can undo.
7. **Unplaced-finding drift** (`_DRIFT_SEVERITY`, `warning`) — not an arm
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

CLASSIFICATION LAUNCHED ADVISORY IN BOTH HALVES: `warning`/`info` severities,
AND deliberate absence from `families.FAMILY_RESOLUTION`. The second half was
the one that is easy to lose — `report.uncited_resolutions` turns a `contested`
finding that VANISHES between reports into an `error`, so a `contested`
advisory family would have red the nightly the first time anyone corrected a
block, which is enforcement through the back door on the run that proves the
launch worked. Both halves were flipped together, by ruling, on the discharge
of the measured population: the 2026-08-30 and 2026-08-31 nightly aggregation
reports read the scenario-title arm's population at ZERO across every governed
repository, and Brett ordered the flip on 2026-08-31 (issue #357). See
`_LAUNCH_SEVERITY`'s own comment for the severities, and the `FAMILY_RESOLUTION`
entry in `families.py` for the one row that carries the second half — which,
because that table has no per-class grain, reaches every class this family
emits rather than the scenario-title arm alone.

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
- **A MARKER NAME THAT MATCHES NO CANON UNIT SUPPRESSES NOTHING, AND SINCE
  `amend-marker-defect-reporting` (2026-09-09) IT IS ALSO REPORTED.** The
  suppression half is unchanged and still fail-closed — the unit the author
  MEANT is reported by whichever arm owns it, so a mistyped name costs a finding
  rather than buying silence. What changed is the silence ABOUT THE MARKER:
  `add-modified-block-currency-check` recorded reporting the dangling name as "a
  plausible later ruling" it had no standing to take, and openxFactory issue
  #729 is that ruling, taken as an amendment of the requirement's own reporting
  sentence rather than as a patch. The name is reported only where it matches no
  unit of the promoted requirement AND no unit of the block.
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

from . import ERROR, INFO, SEVERITY_RANK, WARNING, Finding, Skip
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

# THE SEVERITIES, SIX OF THEM, NAMED APART ON PURPOSE.
#
# `_LAUNCH_SEVERITY` is the identifier `promotion_fidelity`, `duplicate_packet`
# and `family_enumeration` all carry, and it is the grep that ties every reader
# of a launch decision together. Here it belongs to the SCENARIO-TITLE arm,
# because that is the one arm the flip reserved in
# `add-modified-block-currency-check` tasks.md § 7.2 moves — raised to `error`
# AND the family added to `families.FAMILY_RESOLUTION`, together, in one
# commit, after the standing population was discharged (issue #357).
#
# The other two are separate constants precisely so that flip cannot drag them.
# A single shared constant would take the title-resolution arm to `error` at the
# same time, which no ruling asked for; and the carriage ledger has NO SEVERITY
# flip proposed at all, its population being standing by construction — every
# legitimate MODIFIED block edits something, so an editorial band is the honest
# state and a permanent yellow row for a condition nobody should act on is how a
# report stops being read.
#
# `_DRIFT_SEVERITY` is the FOURTH, added by `add-unclassified-finding-class` for
# the fifth finding class, and the same argument applies to it word for word:
# § 7.2 flips `_LAUNCH_SEVERITY` and this class must not ride that flip. Here
# the drag would also be INVISIBLE — `FindingClass.band` reads the constant and
# the registry pin reads the band off the class, so a shared constant would move
# the rendered caption and the emitted finding together and no pin would notice.
# `test_the_realized_flip_of_the_launch_severity_did_not_drag_the_drift_class`
# reads the module's real post-flip state directly and is what makes that
# falsifiable rather than merely written down.
#
# FLIPPED 2026-08-31 by ruling — Brett, "MEASURE FIRST, THEN FLIP" (2026-08-27),
# discharged by the 2026-08-30 and 2026-08-31 nightly aggregation reports
# reading the scenario-title arm's population at ZERO across every governed
# repository, and the flip ordered on 2026-08-31 (issue #357). O8 (research
# R11, `specs/019-modified-block-currency-family/plan.md`) is why the OTHER
# three severity constants below are UNCHANGED by this flip — they are
# separately assignable module attributes for exactly this reason, and O8 says
# so by name: "so § 7.2's flip moves the scenario-title arm alone. A veto (one
# constant) drags the title-resolution arm to `error` on a flip nobody asked
# for." O8 is silent on `families.FAMILY_RESOLUTION`, which has no per-class
# grain — `runner.main` applies it by `Finding.family` alone, a string every
# arm of this module shares — so the ONE row the flip adds there necessarily
# reaches every class this family emits, not the scenario-title arm alone. See
# that row, in `families.py`, for why that is the mechanism's own answer rather
# than a widening this change chose.
_LAUNCH_SEVERITY = ERROR
_RESOLUTION_SEVERITY = WARNING
_LEDGER_SEVERITY = INFO
_DRIFT_SEVERITY = WARNING

# THE FIFTH AND SIXTH, added by `govern-sibling-added-modified-deltas` for the
# two classes that read a PAIRING and a COLLISION rather than a carriage. They
# are separate constants for the reason the four above are, and that reason has
# since been DEMONSTRATED rather than merely reserved: § 7.2's flip landed at
# `7f656980` (PR #529, 2026-08-31) and moved `_LAUNCH_SEVERITY` ALONE. A shared
# constant would have taken these two classes to `error` on a flip no ruling
# asked for — and here the drag would be worse than invisible, because both
# launch against a population the corpus authored before any rule existed.
#
# BOTH ARE `warning` AT LAUNCH, per the two ADDED requirements of this packet's
# `doc-health` delta. That band is the measure-then-flip posture every family of
# this group launched under; raising it is one later decision, taken by ruling
# AFTER the standing population is discharged, and it is not this change's.
#
# THE RESOLUTION CLASS IS NOT A SECOND HALF OF THAT CHOICE, and these constants
# cannot reach it. `families.FAMILY_RESOLUTION` carries this family already
# (`7f656980`), that table has NO per-class grain — `runner.main` applies it by
# `Finding.family` alone — so a finding of either new class is `contested` from
# its first emit. See that row in `families.py`.
_PAIRING_SEVERITY = WARNING
_COLLISION_SEVERITY = WARNING

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


# ============================================================================
# THE ARM TEMPLATES — ONE PLACE THAT KNOWS EACH ARM'S FIXED PROSE
# ============================================================================
#
# WHY THIS REGISTRY EXISTS, AND IT IS NOT TIDYING. `add-unclassified-finding-class`
# emits ONE finding per distinct unplaced rule SHAPE, and its identity rule was
# AMENDED on 2026-08-28 by Brett's ruling, verbatim: "Amend: shape = arm
# template, all interpolations masked". Two rule texts are ONE SHAPE where they
# come from the SAME TEMPLATE, whatever their interpolated values — so one shape
# is one template and one remedy, and the delta requires the family to derive
# that mask FROM ITS OWN ARM TEMPLATES rather than from lexical guessing.
#
# WHAT THE OLD RULE GOT WRONG, MEASURED. Masking only quoted spans and digit
# runs left every UNQUOTED interpolation shape-bearing: the promoted spec's
# repo-relative path, the `[body]`/`[bullet]` unit-kind list, a change-id list,
# an unresolved block's `why` clause. Dropping ONE class pattern on this
# repository then emitted SIX findings for SEVEN unplaced ones, where one new
# map entry would have placed all seven. Nine on `-two-writers`, three on
# `-markers`. Under the amended rule each of those is ONE.
#
# SO THE ARMS RENDER THROUGH THESE TEMPLATES rather than through their own
# f-strings. That is the whole mechanism: the fixed prose has exactly one
# definition, the arm that prints it and the mask that reads it cannot drift
# apart, and adding an arm without registering its template is impossible
# because the arm has nowhere else to get its text from.
#
# THE RENDERED BYTES ARE UNCHANGED. Every template below is the f-string its arm
# carried before, field for field. Nothing new was written to prove that: F1's
# ninety-eight tests and F2's thirteen-tree catalogue already assert this
# family's rule texts against the corpus, and they were green on the refactor's
# first run. What IS new is
# `test_every_finding_matches_exactly_one_arm_template`, which holds the
# property the MASK depends on — that the six are mutually exclusive over
# repr-masked text — and `test_the_arm_templates_are_the_only_place_the_prose_lives`,
# which holds that no arm builds a rule text any other way.

# A `{field}` placeholder in a template, including `{field!r}`. Splitting on it
# yields the FIXED SEGMENTS, in order, which is all the mask needs to know.
_FIELD = re.compile(r"\{[^{}]*\}")


class _ArmTemplate:
    """One arm's rule text: the format string, and the fixed prose inside it.

    PRIVATE, deliberately. The module's public surface is snapshotted by
    `test_this_feature_touches_no_production_module`, and a mechanism for
    computing a local identity is not something another family should reach for
    — `add-unclassified-finding-class` § 4.4 scopes this rule to this family.

    `matches` is asked about a rule whose `repr` spans have ALREADY been masked
    (see `_shape`). That ordering is load-bearing: requirement titles and quoted
    body units come from the CORPUS and may contain any phrase, including
    another arm's, so matching templates against raw text could file one arm's
    finding under another's template. Masked first, the only text left is this
    module's own prose plus placeholders, and the six templates are then
    mutually exclusive — asserted, not assumed, by
    `test_every_finding_matches_exactly_one_arm_template`.
    """

    __slots__ = ("id", "text", "segments", "_pattern")

    def __init__(self, id: str, text: str):
        self.id = id
        self.text = text
        self.segments = tuple(_FIELD.split(text))
        # `\Z` is NEAR-INERT and says so rather than looking load-bearing: four
        # of the six templates END in a field, so their pattern already ends
        # `(?s:.*?)\Z`, which matches whatever is left. It bites only on the two
        # that end in fixed prose (`marker-defects`, `ordering`), where it stops
        # a longer rule text from matching on a prefix. The ANCHOR THAT CARRIES
        # THE WEIGHT is `re.match` in `matches` below — there is no `^` here,
        # and switching that one call to `re.search` files a drift finding under
        # the ledger template through its own quotation.
        self._pattern = re.compile(
            r"(?s:.*?)".join(re.escape(seg) for seg in self.segments) + r"\Z")

    def render(self, **fields) -> str:
        return self.text.format(**fields)

    def matches(self, masked: str) -> bool:
        return self._pattern.match(masked) is not None


TEMPLATE_TITLES = _ArmTemplate("template:scenario-titles", (
    "active MODIFIED block for {title!r} omits {missing} of the {total} "
    "scenarios {spec_rel} currently states for it: {named}"))

TEMPLATE_LEDGER = _ArmTemplate("template:carriage-ledger", (
    "active MODIFIED block for {title!r} does not carry {missing} of the "
    "{total} body units and scenario bullets {spec_rel} currently states for "
    "it — a divergence this arm CANNOT distinguish from a deliberate "
    "rewording, and does not claim to: {listed}"))

# ONE TEMPLATE FOR ALL FIVE MARKER-DEFECT GROUNDS, on the `TEMPLATE_PAIRING`
# precedent below and for the reason stated there: the five grounds share a
# band, a class and an ACTION, and differ only in WHY — so giving any of them
# fixed prose of its own would claim a second remedy where there is one, and
# would add an entry to `_ARM_TEMPLATES` (which is a count of remedies) for a
# remedy nobody has to write. `amend-marker-defect-reporting` (2026-09-09) added
# the second and third grounds and moved the WHY into an interpolated field, and
# `amend-marker-declaring-nothing` (2026-09-10) added the fourth and fifth
# through that same field, THIS TEMPLATE'S TEXT UNMOVED — so the existing
# `CLASS_MARKERS` probe places every new finding, `_ARM_TEMPLATES` stays at
# EIGHT, and the seventh class (`unplaced-finding drift`) stays silent;
# GROUND ONE'S RENDERED TEXT IS BYTE-IDENTICAL TO THE ONE THIS CLASS SHIPPED
# WITH, which is what keeps the class map, the shape mask and every standing pin
# reading exactly as before. The trailing prose is FIXED rather than folded into
# `{why}`, because `_ArmTemplate`'s `\Z` bites only on a template that ends in
# fixed prose and this is one of the two that do.
TEMPLATE_MARKERS = _ArmTemplate("template:marker-defects", (
    "active MODIFIED block for {title!r} carries a {form!r} marker by "
    "{change_id} ({date}) {why} — a declaration that does not describe the "
    "block"))

TEMPLATE_UNRESOLVED = _ArmTemplate("template:title-resolution", (
    "active MODIFIED block for {title!r} resolves to no promoted requirement, "
    "no rename of its own, and no active sibling's addition: {why}"))

TEMPLATE_ORDERING = _ArmTemplate("template:ordering", (
    "the ordering of MODIFIED blocks for {title!r} is undecided: {names} — "
    "{why}; each block is meanwhile measured against canon, the only basis a "
    "reader can name"))

# ONE TEMPLATE FOR ALL FOUR REPORTED PAIRING STATES, and MISDECLARED's four
# grounds inside its own. One template is one SHAPE is one map entry, and the
# four states share a band and an action and differ only in WHY — so giving any
# of them fixed prose of its own would claim a second remedy where there is one.
# The state word and the whole reason go in INTERPOLATED fields, on the
# `TEMPLATE_UNRESOLVED` precedent, and so does MISDECLARED's marker COUNT: fixed
# prose carrying a numeral is a shape the mask cannot strip, and a two-marker
# block and a three-marker one would then read as two remedies.
TEMPLATE_PAIRING = _ArmTemplate("template:sibling-pairing", (
    "active MODIFIED block for {title!r} rests on an active sibling's addition "
    "rather than on canon, and the pairing is {state}: {why}"))

# THE COLLISION CLASS'S TEMPLATE. Its subject is an `## ADDED Requirements`
# block or a rename's `TO:` half, never a MODIFIED block, so it does NOT open
# with `_BLOCK_HEAD`'s "active MODIFIED block for" — and its own class pattern
# is anchored past its title `repr` for the same measured reason that one is.
TEMPLATE_COLLISION = _ArmTemplate("template:added-over-canon", (
    "active {block_kind} block for {title!r} writes a requirement title "
    "{spec_rel} already states: {why}"))

# The fifth class's own rule text is a template like any other, and it is
# registered like any other: a drift finding the map failed to place must group
# by template too, or the count that reports drift would itself be split.
TEMPLATE_DRIFT = _ArmTemplate("template:unplaced-drift", (
    "this family's own class map has no pattern for {n} finding{s} this run "
    "emitted, which share one rule shape the map has drifted behind; the first "
    "of them in this family's own report order reads, verbatim: {rule}"))

# ORDERED, and first match wins, exactly as `_CLASS_PATTERNS` is. The order is
# not load-bearing today — the six are mutually exclusive over masked text and a
# test says so — but a deterministic order is what makes a future collision a
# stable wrong answer instead of an unstable one.
_ARM_TEMPLATES = (TEMPLATE_TITLES, TEMPLATE_LEDGER, TEMPLATE_MARKERS,
                  TEMPLATE_UNRESOLVED, TEMPLATE_ORDERING, TEMPLATE_DRIFT,
                  TEMPLATE_PAIRING, TEMPLATE_COLLISION)


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
# THE THIRD RESERVED FORM (`govern-sibling-added-modified-deltas`,
# `document-lifecycle`'s "A MODIFIED block over a requirement no promoted
# specification carries declares its basis by marker"). Same anchor, same
# completeness, same reason: this packet's own delta text and
# `document-lifecycle`'s both set the template out in prose, and both promote.
#
# THE BASIS is a code span resolved by `extract_code_spans`, exactly as
# `Merged into`'s destination is, and never by a nested backtick regex.
#
# AND RECOGNITION ENDS AT THE CLOSING COLON. The ` — <reason>` tail
# `document-lifecycle` REQUIRES is no part of it, and neither is the equality of
# the `by` identifier to the carrying change. Both are REPORTED STATES rather
# than parse conditions, and folding either into recognition would drop the
# paragraph back to an ordinary body unit — so a block plainly carrying a
# defective declaration would be reported UNDECLARED and its author handed the
# absent-marker remedy for a marker that is right there.
_PAIRING_PREFIX = re.compile(
    rf"^\*\*Modified over (`+.*?`+)'s addition by ({_CHANGE_ID}) "
    rf"\(({_ISO})\):\*\*")
# The one form of this module's three that NAMES NO UNITS, and every
# consequence of that is a consequence of this constant being the `form` of a
# marker whose `names` list is empty: it suppresses nothing, it can never join
# `suppression`'s `defective` list (that list is only appended to from inside
# the per-name loop), and `derive_units` keeps it out of the units on both
# sides like every other marker.
_PAIRING_FORM = "pairing"
# The word `document-lifecycle` reserves for the unratified disclosure, read
# case-insensitively out of the reason clause — a WORD, never a sentence a
# checker would have to arbitrate.
_DISCLOSURE = "unratified"

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


# THE REASON SEPARATOR, and the boundary it draws is a GRAMMAR RULE rather than
# a heuristic. `dh` (Currency of an active change's MODIFIED requirement blocks,
# as amended by `amend-marker-reason-boundary` 2026-09-06): "THE REASON SHALL
# BEGIN AT THE FIRST ` — ` SEPARATOR STANDING OUTSIDE EVERY CODE SPAN: the units
# named are the spans that close before that separator, the reason is everything
# after it, and a code span that falls inside the reason is prose the reason
# quotes rather than a unit the marker names."
#
# WHAT THE RETIRED SENTENCE DID. It measured the reason from BEHIND — "everything
# after the LAST code span's following ` — `" — so every code span an author
# wrote INSIDE the reason was harvested as a declared-removed NAME and the reason
# was shortened to whatever trailed it. Measured 2026-09-06 over this corpus:
# seven unit-naming markers, TWO of them misread that way, each deriving THREE
# names where its author declared one (openxFactory issue #692).
_REASON_SEP = " — "


def _reason_boundary(text: str, spans: list[tuple[int, int, str]]) -> int | None:
    """The offset of the first `_REASON_SEP` in `text` that stands OUTSIDE every
    code span, or None where no separator stands outside one.

    PRIVATE ON PURPOSE. It is one split inside `parse_marker`, not a new public
    reading of a document, and the module's public surface is snapshotted by
    `test_modified_block_currency_fixtures.py::
    test_this_feature_touches_no_production_module`. A helper that changes no
    public callable keeps that guard meaningful for the next name that does.

    A separator INSIDE a span is part of a unit's own bytes — a unit that cites
    `` ` — ` `` is a unit like any other — and the amended rule says so in as
    many words, which is why the test is span membership and never a search for
    the last one. The separator's three characters can never begin a span
    (neither a space nor an em dash is a backtick), so every span lies wholly
    before or wholly after the boundary and `end <= cut` partitions them exactly.
    """
    i = 0
    while True:
        cut = text.find(_REASON_SEP, i)
        if cut == -1:
            return None
        if not any(s < cut and cut + len(_REASON_SEP) <= e for s, e, _c in spans):
            return cut
        i = cut + 1


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
                 "paragraph", "basis", "quoted")

    def __init__(self, form: str, change_id: str, date: str, names: list[str],
                 destination: str | None, reason: str | None, paragraph: str,
                 basis: str | None = None, quoted: list[str] | None = None):
        self.form = form
        self.change_id = change_id
        self.date = date
        self.names = names
        self.destination = destination
        self.reason = reason
        self.paragraph = paragraph
        # THE PAIRING FORM'S BASIS — the change whose ADDITION (or whose rename
        # to the title) this block is written over. `None` for the two
        # unit-naming forms, which declare a fact about UNITS rather than a
        # relation between two documents. A LAST parameter with a default, so
        # every existing positional construction of a `Marker` still reads.
        self.basis = basis
        # THE SPANS THE REASON QUOTES — the code spans of a unit-naming
        # marker's tail that fall AFTER the reason boundary, in order,
        # normalized. `amend-marker-reason-boundary` (2026-09-06) stopped
        # reading them as names, correctly, and DISCARDED them: `parse_marker`
        # filtered them out and no field carried them, so the defect openxFactory
        # issue #729 reports — a reason that quotes a unit the block leaves out,
        # which under the boundary declares nothing — was not mechanically
        # detectable at all. Carried here so `suppression` can resolve them
        # against canon exactly as it resolves a name. EMPTY for the pairing
        # form, whose whole tail is reason by construction and which names no
        # units, so nothing in it can be a would-be declaration; and empty for a
        # marker whose tail carries no boundary, where every span IS a name.
        # ANOTHER LAST PARAMETER WITH A DEFAULT, on the same rule.
        self.quoted = list(quoted or ())

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
    form, destination, basis = "removed", None, None
    if m:
        change_id, date = m.group(1), m.group(2)
    else:
        m = _MERGED_PREFIX.match(text)
        if m:
            form = "merged"
            spans = extract_code_spans(m.group(1))
            if not spans:
                return None
            destination = normalize(spans[0][2])
            change_id, date = m.group(2), m.group(3)
        else:
            m = _PAIRING_PREFIX.match(text)
            if not m:
                return None
            form = _PAIRING_FORM
            spans = extract_code_spans(m.group(1))
            if not spans:
                return None
            basis = normalize(spans[0][2])
            # RESOLVABLE, NOT EXISTENT — decision O7 again, unchanged: a
            # marker's id must PARSE, because reading it as "names a change
            # that exists" would rot every marker the moment its basis
            # archives, which is what a marker of this form is FOR.
            if not re.fullmatch(_CHANGE_ID, basis):
                return None
            change_id, date = m.group(2), m.group(3)
    tail = text[m.end():]
    if form == _PAIRING_FORM:
        # THE REASON IS THE WHOLE TAIL AFTER ` — `, HARVESTED ALWAYS AND
        # NEVER OPTIONALLY. This form names NO units, so the split the two
        # unit-naming forms make below — names before the first separator
        # standing outside a code span, reason after it — has nothing to
        # divide here: every code span in this tail is prose the reason
        # quotes, wherever it falls. Reusing that path would let a span
        # written BEFORE the separator be harvested as a name this form is
        # forbidden to have. (Before `amend-marker-reason-boundary`
        # 2026-09-06 the unit-naming forms measured the reason from the LAST
        # code span, and the note here said so; the reason this branch is
        # separate is unchanged by that amendment.)
        #
        # AND AN ABSENT TAIL IS A VALUE, NOT A PARSE OUTCOME: `reason` is
        # `None` where there is no separator, or one with nothing but
        # whitespace after it, and `_pairing_state` REPORTS that on its fourth
        # misdeclared ground. An empty reason declares exactly what an absent
        # one does, and the disclosure that would have lived in it has no
        # clause to live in.
        # ONE GRAMMAR TOKEN, ONE SPELLING. The separator is `_REASON_SEP` here
        # as it is in the unit-naming path below; the literal this branch used
        # to carry, and its hardcoded `[3:]`, were correct only because the em
        # dash happens to be one code point. The parse is unchanged.
        reason = (normalize(tail[len(_REASON_SEP):]) or None
                  if tail.startswith(_REASON_SEP) else None)
        return Marker(form, change_id, date, [], None, reason, text, basis)
    # THE TWO UNIT-NAMING FORMS, `Removed from canon` and `Merged into`, SPLIT
    # AT THE SAME BOUNDARY. `Merged into`'s destination is matched in the prefix
    # and never here, so the tail after the closing colon is parsed identically
    # in both — which is what the amended sentence states ("The boundary is read
    # the same way in both forms"). The pairing form returned above and takes
    # the WHOLE tail, because it names no units at all.
    spans = extract_code_spans(tail)
    cut = _reason_boundary(tail, spans)
    if cut is None:
        # NO SEPARATOR OUTSIDE A SPAN: every span names a unit and the marker
        # carries no reason — the form the written-out `Merged into` example in
        # canon is in, and unchanged by the amendment.
        names = [normalize(c) for _s, _e, c in spans]
        quoted: list[str] = []
        reason = None
    else:
        # THE FAILURE DIRECTION IS THE CONSERVATIVE ONE. A marker that separated
        # its NAMES with ` — ` has the later ones read as reason: they suppress
        # nothing, and the units their author meant to name are REPORTED rather
        # than silently dropped. No marker in this corpus is written that way
        # (measured 2026-09-06, seven markers).
        names = [normalize(c) for _s, e, c in spans if e <= cut]
        # AND THE SPANS AFTER THE CUT ARE CARRIED RATHER THAN DROPPED
        # (`amend-marker-defect-reporting`, openxFactory issue #729). They are
        # still not names — the amended sentence is unchanged and this changes
        # no parse — but a span that WOULD have named a unit the block leaves
        # out is the defect the marker-defect class's second ground reports, and
        # a discarded span cannot be reported about.
        quoted = [normalize(c) for _s, e, c in spans if e > cut]
        reason = normalize(tail[cut + len(_REASON_SEP):]) or None
    return Marker(form, change_id, date, names, destination, reason, text,
                  quoted=quoted)


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
        TEMPLATE_TITLES.render(title=block.title, missing=len(missing),
                               total=len(canon_titles),
                               spec_rel=basis.spec_rel, named=named))]




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
        TEMPLATE_LEDGER.render(title=block.title, missing=len(missing),
                               total=len(canon_units),
                               spec_rel=basis.spec_rel, listed=listed))]


class _MarkerDefect:
    """ONE MARKER, ONE GROUND ON WHICH IT DECLARES NOTHING — the unit of the
    marker-defect class's report, added by `amend-marker-defect-reporting`
    (2026-09-09, openxFactory issue #729).

    PRIVATE ON PURPOSE, on `_reason_boundary`'s rule: the module's public
    surface is snapshotted by `test_modified_block_currency_fixtures.py::
    test_this_feature_touches_no_production_module`, and a record one function
    hands to one arm inside this module is no new public reading of a document.

    ONE RECORD PER GROUND, NOT PER MARKER — because a ranked plan is a list of
    REMEDIES and the five grounds are five different edits. A marker can
    declare nothing two ways at once (name a unit the block restates AND quote
    an uncarried unit inside its reason) and an author fixes those separately.
    The FIFTH ground is the one exception by construction rather than by rule: a
    marker that names nothing and quotes nothing reaches no other ground, so it
    is always exactly one record.
    WITHIN a ground the record is per MARKER, which is what keeps ground one's
    report exactly the one finding it has always emitted.

    `why` is rendered, already interpolated, into `TEMPLATE_MARKERS`' one
    `{why}` field. Every value a marker or a unit contributes to it goes in as a
    `repr`, so `_mask_repr_spans` strips it before `_shape` matches templates —
    the same discipline every other arm's interpolations keep.
    """

    __slots__ = ("marker", "why")

    def __init__(self, marker: Marker, why: str):
        self.marker = marker
        self.why = why

    def __repr__(self) -> str:  # pragma: no cover - diagnostics only
        return f"_MarkerDefect({self.marker.change_id!r}, {self.why!r})"


# THE FIVE GROUNDS, AS THE `{why}` CLAUSE EACH RENDERS. Named constants rather
# than inline f-strings so that `TEMPLATE_MARKERS` remains the only place this
# class's PROSE lives, which is what
# `test_the_arm_templates_are_the_only_place_the_prose_lives` reads the module
# for. Ground one's text is UNCHANGED and its rendered finding is byte-identical
# to the one that shipped: `naming <names>, which the block still restates — a
# declaration that does not describe the block`.
#
# NEITHER NEW CLAUSE MAY CONTAIN ANOTHER TEMPLATE'S FIXED PROSE, and that is
# checked rather than hoped: `{why}` lands inside `TEMPLATE_MARKERS`' own
# `(?s:.*?)` gap, so a clause carrying the ledger template's " does not carry "
# … " of the " … sequence could make one rule text match two templates and red
# the partition the shape mask depends on. "leaves out" and "matches no unit of"
# are worded to avoid it, and
# `test_each_new_marker_defect_ground_matches_exactly_one_arm_template` holds
# the property instead of trusting the wording.
_WHY_RESTATED = "naming {named}, which the block still restates"
_WHY_UNMATCHED = ("naming {named}, which matches no unit of the promoted "
                  "requirement or of the block")
_WHY_QUOTED = ("whose reason QUOTES {quoted}, a promoted unit of the "
               "requirement this block leaves out, rather than naming it "
               "before the separator that opens the reason")
# THE FOURTH AND FIFTH GROUNDS, ADDED BY `amend-marker-declaring-nothing`
# (2026-09-10, openxFactory issues #856 and #860). Ground four is the residue
# the predecessor pinned as a silence and left for a ruling; ground five is the
# case its own adversarial pass found and could not reach. Both are worded, like
# the two before them, to carry NO other template's fixed prose in order.
_WHY_BLOCK_ADDED = ("naming {named}, which matches no unit of the promoted "
                    "requirement and is text the block itself adds, so the "
                    "marker declares removed from canon what canon never "
                    "carried")
_WHY_NOTHING = ("which names no unit and quotes no span, its tail carrying no "
                "code span at all")


def suppression(markers: list[Marker], canon_units: list[Unit],
                block_units: list[Unit]
                ) -> tuple[set[tuple[str, str]], list[_MarkerDefect]]:
    """`(suppressed, defective)` — what the block's markers declare, and which of
    them declare nothing.

    THE THREE-WAY RESOLUTION, per name, against canon units of ANY kind:

    - the name matches an ABSENT canon unit -> that unit is suppressed;
    - the name matches a canon unit the block still CARRIES -> the MARKER is
      reported and nothing is suppressed by that name, because a declaration
      that does not describe the block is a declaration no reader can rely on;
    - the name matches NO canon unit -> nothing suppressed, and — SINCE
      `amend-marker-defect-reporting` (2026-09-09) — the MARKER is reported
      where the name matches no unit of the block either. The suppression half
      is unchanged and still fail-closed. What changed is the silence:
      `add-modified-block-currency-check` recorded a report here as "a plausible
      later ruling" that the one-reporting-case sentence gave it no standing to
      invent, openxFactory issue #729 is that ruling, and the standing it needed
      is the amended sentence itself. AND SINCE `amend-marker-declaring-nothing`
      (2026-09-10, openxFactory issue #856) the OTHER half of that resolution is
      reported too, on ground FOUR: a name matching a unit the BLOCK carries but
      canon does not is text the block ADDS, so the marker declares removed from
      canon what canon never carried. The predecessor left it silent because the
      rule was unwritten (`design.md` D3 there); it is written now, and the
      sentence states FIVE grounds.

    AND A FIFTH, OVER THE MARKER THAT DECLARES NOTHING AT ALL (openxFactory
    issue #860). A `Removed from canon` marker whose tail carries no code span
    parses to no names and no quoted spans, so it reaches none of the four
    grounds above while the reserved-marker rule exempts its paragraph from
    carriage — a marker of correct form declaring nothing, which is exactly the
    fault the grounds exist to report. It is read on THAT FORM ALONE: the
    pairing form names no units by construction, and a `Merged into` marker
    whose tail names no superseded title is a question nobody has ruled.

    AND A FOURTH RESOLUTION, over the spans the reason QUOTES rather than the
    names, added by the same amendment and NARROW BY DESIGN (`design.md` D1,
    option A): a span after the reason boundary is reported only where it
    EXACTLY MATCHES a promoted unit that the block does not carry and that no
    marker declares removed — a would-be declaration the boundary reads as
    prose. A span matching no unit is canon's own blessed form (a reason quotes,
    and 8 of this corpus's 16 unit-naming markers quote a code span in their
    reason) and is SILENT. That predicate, and not the span's mere position, is
    what separates the defect from the normal form.

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
    # THE BLOCK'S OWN TEXTS, of any kind. Read by the third ground alone: a name
    # matching no canon unit but matching something the block states is text the
    # block ADDS, and the amended sentence reports only a name that matches
    # neither side.
    block_texts = {u.text for u in block_units}
    by_text: dict[str, list[Unit]] = {}
    for u in canon_units:
        by_text.setdefault(u.text, []).append(u)

    canon_titles = {u.text for u in canon_units if u.kind == SCENARIO_TITLE}
    block_titles = {u.text for u in block_units if u.kind == SCENARIO_TITLE}
    adds_new_title = bool(block_titles - canon_titles)

    suppressed: set[tuple[str, str]] = set()
    defective: list[_MarkerDefect] = []
    for marker in markers:
        restated = False
        unmatched: list[str] = []
        block_added: list[str] = []
        for name in marker.names:
            matches = by_text.get(name)
            if not matches:
                # NAMES NOTHING; BUYS NOTHING — and it is now reported either
                # way, on ground THREE where the block does not state the name
                # either, and on ground FOUR where the block itself adds it.
                if name not in block_texts:
                    unmatched.append(name)
                else:
                    block_added.append(name)
                continue
            if any(u.pair() in have for u in matches):
                restated = True
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
        # ONE, THEN THREE, THEN FOUR, THEN FIVE, PER MARKER — a fixed order, so
        # a marker defective on more than one reports the same rows in the same
        # sequence every run, and ground two follows them all in the second pass
        # below. Ground one names ALL of the marker's names, which is the text
        # it has always emitted; grounds three and four name only the names that
        # reached each of them, because those are the ones an author edits, and
        # the two are disjoint by construction — a name matching no canon unit
        # is either stated by the block or it is not.
        if restated:
            defective.append(_MarkerDefect(marker, _WHY_RESTATED.format(
                named=", ".join(repr(n) for n in marker.names))))
        if unmatched:
            defective.append(_MarkerDefect(marker, _WHY_UNMATCHED.format(
                named=", ".join(repr(n) for n in unmatched))))
        if block_added:
            defective.append(_MarkerDefect(marker, _WHY_BLOCK_ADDED.format(
                named=", ".join(repr(n) for n in block_added))))
        # GROUND FIVE IS EXCLUSIVE OF THE OTHER FOUR AND CANNOT DOUBLE-REPORT.
        # It fires only where the marker names nothing and quotes nothing, and
        # every other ground is reached through one of those two lists — so a
        # marker reported here is reported ONCE. It is read on the
        # `Removed from canon` form ALONE: the pairing form names no units by
        # construction (its whole tail is a reason), and a `Merged into` marker
        # whose tail names no superseded title is a question nobody has ruled,
        # its destination standing in the prefix where that form's declaration
        # has always been read.
        if marker.form == "removed" and not marker.names and not marker.quoted:
            defective.append(_MarkerDefect(marker, _WHY_NOTHING))
    # GROUND TWO RUNS IN A SECOND PASS, AND IT HAS TO. Its predicate asks
    # whether the quoted unit is one NO marker declares removed, so it cannot be
    # decided until every marker's names have been resolved — a sibling marker
    # that properly declares the unit gone makes the quotation harmless, and
    # reporting it would tell an author to fix a marker that is already correct.
    for marker in markers:
        offending = [span for span in marker.quoted
                     # A SPAN THE MARKER ALSO NAMES IS A REPEAT, NOT A DEFECT.
                     # The author declared it; quoting it again in the reason
                     # declares nothing new and hides nothing.
                     if span not in marker.names
                     and any(u.pair() not in have
                             and u.pair() not in suppressed
                             for u in by_text.get(span, ()))]
        if offending:
            defective.append(_MarkerDefect(marker, _WHY_QUOTED.format(
                quoted=", ".join(repr(q) for q in offending))))
    return suppressed, defective


_MARKER_ACTION = ("name a unit the block does not restate, or drop the "
                  "declaration — a marker that does not describe the block "
                  "declares nothing")


def _arm_marker_defects(repo: str, block: ActiveBlock,
                        defective: list[_MarkerDefect],
                        ) -> list[Finding]:
    """THE FOURTH FINDING CLASS — a defect in a DECLARATION, not a comparison.

    Three arms, seven classes, and the numbers differ on purpose: the arms read
    two documents against each other, this reads one paragraph against the block
    it sits in, the fifth and sixth read a delta's declarations and the promoted
    index, and the seventh reads the class map's own verdict. It carries the ledger's `info` band so the advisory launch
    holds in both halves, and it deliberately does NOT carry the ledger's hedge:
    a marker naming a unit the block still restates is wrong with certainty.

    FIVE GROUNDS, ONE CLASS, ONE ACTION (`amend-marker-defect-reporting`,
    2026-09-09; `amend-marker-declaring-nothing`, 2026-09-10). `suppression`
    decides them and hands one `_MarkerDefect` per
    ground per marker; this renders each into the one template. They stay ONE
    class deliberately: the remedy is the same edit — name a unit the block does
    not restate, or drop the declaration — so a second class would split a
    reader's plan without giving them a second thing to do, and a second
    template would add an entry to `_ARM_TEMPLATES`, which is a count of
    remedies.
    """
    out: list[Finding] = []
    for defect in defective:
        marker = defect.marker
        out.append(Finding(
            _LEDGER_SEVERITY, FAMILY, repo, block.delta_rel,
            TEMPLATE_MARKERS.render(title=block.title, form=marker.form,
                                    change_id=marker.change_id,
                                    date=marker.date, why=defect.why),
            _MARKER_ACTION))
    return out


_RATIFIED = "ratified"

# The two basis forms, and they are ONE BASIS wherever this corpus reads them:
# `document-lifecycle`'s marker requirement is owed where "an active change ADDS
# or RENAMES to that title", and `release-realization`'s ordering obligation
# reaches both. The discriminator exists for exactly one reading —
# `_pairing_state`'s SELF-REFERENTIAL state, which is the carrier's own
# ADDITION alone.
_BASIS_ADDED = "added"
_BASIS_RENAMED = "renamed"


class _SiblingBasis:
    """One active change's ADDITION of a title, or its rename INTO one.

    PRIVATE. `sibling_titles` returns these beside each `(capability, title)`
    so a pairing can be NAMED in a finding, a self-addition can be told from an
    own-rename, and an undisclosed unratified basis can be seen at all — three
    facts the bare title set this function used to return cannot carry.

    `standing` is read through `_standing`, the module's existing
    `corpus.parse_status` -> `promotion_fidelity.declared_standing` path, and it
    is read HERE because `active_blocks` never reaches a pure adder or a pure
    renamer: that reader skips a change carrying no MODIFIED block.
    """

    __slots__ = ("change", "kind", "standing", "title", "delta_rel")

    def __init__(self, change: str, kind: str, standing: str | None,
                 title: str, delta_rel: str):
        self.change = change
        self.kind = kind
        self.standing = standing
        self.title = title
        self.delta_rel = delta_rel

    def __repr__(self) -> str:  # pragma: no cover - diagnostics only
        return f"_SiblingBasis({self.change!r}, {self.kind!r})"


def sibling_titles(root: Path) -> dict[tuple[str, str], list[_SiblingBasis]]:
    """`{(capability, norm(title)): [_SiblingBasis, ...]}` — every title some
    ACTIVE change ADDS or RENAMES to, and WHO puts it there.

    A MODIFIED title landing here is PENDING, not absent (`dh:278-280`), and
    pending means there is nothing to compare: the promoted requirement does not
    exist yet, so no basis is synthesized from the sibling's ADDED text. RULED
    2026-08-27 — the earlier reading, which built a basis from the addition,
    would have measured all seven of this corpus's
    MODIFIED-over-a-sibling's-ADDED pairs against text no promoted requirement
    carries. **THAT RULING IS UNTOUCHED BY THE WIDENING BELOW**, which adds no
    text to any comparison: what is returned beside each title is the ADDING
    CHANGE, ITS DECLARED STANDING and WHICH BLOCK PUT THE TITLE THERE — three
    facts about the DELTA, never a unit of requirement text.

    THE KEYS ARE WHAT THEY WERE. `resolve` asks this only `(capability, key) in
    siblings`, and a mapping answers that exactly as the set did: both basis
    forms still make a title `pending`, on the promoted rule's own words, "a
    requirement an active sibling change ADDS or RENAMES to".

    THE VALUES ARE WHAT `govern-sibling-added-modified-deltas` NEEDED. The bare
    title set could not name a pairing in a finding, could not see the
    SELF-REFERENTIAL state (it did not exclude the reading change from its own
    sources), and could not see the UNDISCLOSED one (the basis change's standing
    was never read at all). `_collision_findings` reads the same values a second
    time for the other new class — one parse, two uses, rather than a second
    reader of one document set.
    """
    changes = root / "openspec" / "changes"
    if not changes.is_dir():
        return {}
    out: dict[tuple[str, str], list[_SiblingBasis]] = {}
    standings: dict[str, str | None] = {}
    for path in sorted(root.glob(DELTA_GLOB)):
        parts = path.relative_to(root).parts
        if parts[_CHANGE_PART] == _ARCHIVE:
            continue
        change = parts[_CHANGE_PART]
        capability = parts[-2]
        requirements, renames = parse_delta(
            path.read_text(encoding="utf-8", errors="replace"))
        added = [(_BASIS_ADDED, req.title) for req in requirements
                 if req.op == "ADDED"]
        # THE `TO:` HALF AND NEVER THE `FROM:` HALF. A rename's SOURCE is a
        # title canon is expected to carry; its TARGET is the title that
        # becomes pending, and the one the collision class reads.
        renamed = [(_BASIS_RENAMED, new) for _old, new in renames]
        if not added and not renamed:
            continue
        if change not in standings:
            standings[change] = _standing(root, change)
        delta_rel = path.relative_to(root).as_posix()
        for kind, title in added + renamed:
            out.setdefault((capability, norm(title)), []).append(
                _SiblingBasis(change, kind, standings[change], title,
                              delta_rel))
    return out


_PAIRING_ACTION = (
    "declare the basis with ONE `Modified over` marker and no more than one, "
    "name the change carrying the block as that marker's `by` identifier, give "
    "the marker the ` — <reason>` tail its form requires, disclose in that "
    "reason clause where the basis is not ratified, and hold the archive until "
    "the declared change promotes")

# The four REPORTED states. The fifth — declared and resolving — has no name
# here on purpose: it is the state this check exists to produce, and a constant
# for it would be a constant nothing renders.
_PAIRING_SELF = "self-referential"
_PAIRING_UNDECLARED = "undeclared"
_PAIRING_MISDECLARED = "misdeclared"
_PAIRING_UNDISCLOSED = "undisclosed"


def _standing_phrase(standing: str | None) -> str:
    """How a finding says what a basis change's proposal declares.

    A standing NO reader can resolve is treated as not ratified and SAYS so
    rather than reading as ratified by silence: the whole point of the
    disclosure is to warn about text no authority has been shown to accept, and
    a standing nobody can read is no such showing.
    """
    return (f"declared standing `{standing}`" if standing
            else "no standing its proposal header declares")


def _basis_phrase(basis: _SiblingBasis) -> str:
    """One resolved basis, as a finding names it — with its standing WHERE IT
    IS NOT RATIFIED, so a reader sees at a glance whether an obligation or only
    an observation stands behind the row."""
    kind = ("addition" if basis.kind == _BASIS_ADDED
            else "rename to the title")
    if basis.standing == _RATIFIED:
        return f"{basis.change}'s {kind}"
    return (f"{basis.change}'s {kind}, carrying {_standing_phrase(basis.standing)} "
            f"rather than `ratified`")


def _pairing_markers(block: ActiveBlock) -> list[Marker]:
    """Every marker of the reserved `Modified over` form the block carries.

    A LIST, and the classifier is handed the list rather than a member of it.
    `derive_units` preserves every recognized marker in document order, and
    reasoning about "the marker" is how a block carrying one valid declaration
    and one naming a change that adds nothing gets cleared or reported by
    whichever the loop reached first.
    """
    return [m for m in block.markers if m.form == _PAIRING_FORM]


def _pairing_state(block: ActiveBlock,
                   siblings: dict[tuple[str, str], list[_SiblingBasis]]
                   ) -> tuple[str, str] | None:
    """`(state, why)` for one PENDING block, or `None` where it is declared and
    resolving.

    ORDERED, AND EXACTLY ONE STATE PER BLOCK. The five states are mutually
    exclusive BY CONSTRUCTION rather than by convention: each `return` below
    excludes every state under it, and each state's own antecedent in the
    promoted requirement carries the exclusion this order performs. One block
    yields at most one finding of this class, so a reader is never given a
    choice between two true descriptions of one defect.

    1. **THE CARRIER'S OWN ADDITION, FIRST**, because it is a fact about the
       DELTA rather than about the marker. Without the order a self-referential
       block carrying no marker satisfies UNDECLARED as well, and the run emits
       two findings with two remedies for one defect — and the remedy here is
       to withdraw one of the two blocks, which no marker supplies. **READ FROM
       THE CARRIER'S OWN `## ADDED Requirements` BLOCK AND FROM NOTHING ELSE**:
       a carrier's own RENAME to the title is the rename-and-amend shape
       `resolve` settles against canon under the OLD name one step before
       `pending`, so a block of that shape never reaches this function at all
       and reading it here would either report a supported shape or sit as a
       branch no input can reach.
    2. **THEN THE COUNT.** `document-lifecycle` admits AT MOST ONE marker of
       this form per block — one pairing, one declaration — so a plurality is
       placed by a fact about the BLOCK before any single marker's fields are
       read. Zero markers is UNDECLARED.
    3. **THEN THE SINGLE MARKER'S FIELDS, IN THE ORDER ITS FORM WRITES THEM**:
       basis, then `by`, THEN REASON, then disclosure. One finding then names
       the field a repair actually touches, and a marker wrong in two of them
       is repaired from the front.

    **AND THE REASON PRECEDES THE DISCLOSURE, which is not a preference but the
    condition of the disclosure being readable at all.** The disclosure is a
    WORD LOOKED FOR IN THE REASON CLAUSE, so a marker with no clause offers it
    nothing to look in. Read the other way, a prefix-only marker over an
    unratified basis would be told to write `unratified` into a sentence that
    does not exist, while the identical marker over a ratified basis passed in
    silence — one defect named two ways at two titles and unnamed at one of
    them. Reading both would emit two findings for one missing tail.
    """
    key = (block.capability, norm(block.title))
    bases = siblings.get(key, [])
    if any(b.change == block.change and b.kind == _BASIS_ADDED for b in bases):
        return (_PAIRING_SELF,
                "the change carrying the block ALSO ADDS this requirement in "
                "its own `## ADDED Requirements` block, so one change holds two "
                "texts for one requirement where the second is simply the "
                "first; the remedy is to withdraw one of the two blocks, which "
                "no marker supplies and a marker naming this change itself "
                "cannot cure")
    others = [b for b in bases if b.change != block.change]
    markers = _pairing_markers(block)
    if not markers:
        # `others or bases` — AND THE FALLBACK IS NOT DEFENSIVE PADDING. A
        # carrier whose OWN `## RENAMED Requirements` block names a `FROM:`
        # title the promoted specification does NOT carry makes the title
        # pending all by itself: `resolve`'s own-rename precedence requires the
        # old name to be IN CANON, so it does not fire, and the block reaches
        # this check with the carrier as the only writer of the title. It is
        # NOT self-referential — a title pair is no second text — so it is
        # placed here, and the finding names the rename that put the title
        # there rather than naming nothing at all.
        pool = others or bases
        named = "; ".join(sorted({_basis_phrase(b) for b in pool}))
        return (_PAIRING_UNDECLARED,
                f"the block carries no marker of the reserved `Modified over` "
                f"form, and the title resolves to {named}")
    if len(markers) > 1:
        return (_PAIRING_MISDECLARED,
                f"the block carries {len(markers)} markers of the reserved "
                f"`Modified over` form, and one pairing admits ONE "
                f"declaration — a second states a second basis for one text "
                f"rather than adding to the first; withdraw every declaration "
                f"but the one that is true")
    marker = markers[0]
    if marker.basis == block.change:
        return (_PAIRING_MISDECLARED,
                f"the marker names the carrying change `{marker.basis}` as its "
                f"own basis, and a block's basis is a change OTHER than the "
                f"one that writes it")
    declared = [b for b in others if b.change == marker.basis]
    if not declared:
        return (_PAIRING_MISDECLARED,
                f"the marker names `{marker.basis}` as basis, and no active "
                f"change of that id ADDS this requirement or RENAMES to its "
                f"title")
    if marker.change_id != block.change:
        return (_PAIRING_MISDECLARED,
                f"the marker's `by` identifier is `{marker.change_id}` and the "
                f"block is carried by `{block.change}` — a right basis under a "
                f"wrong author is a FALSE PROVENANCE, sending its next reader "
                f"to a packet that declared nothing")
    if not marker.reason:
        return (_PAIRING_MISDECLARED,
                "the marker carries its complete prefix and no ` — <reason>` "
                "tail, so the declaration is one `document-lifecycle` calls "
                "incomplete rather than one this check passes in silence")
    basis = declared[0]
    if (basis.standing != _RATIFIED
            and _DISCLOSURE not in marker.reason.lower()):
        return (_PAIRING_UNDISCLOSED,
                f"the marker declares `{marker.basis}`, which carries "
                f"{_standing_phrase(basis.standing)} rather than `ratified`, "
                f"and its reason clause is silent about that standing — the "
                f"word `{_DISCLOSURE}` that capability reserves is absent from "
                f"it, so the block rests on text no authority has accepted and "
                f"says nothing about it")
    return None


def _arm_pairing(repo: str, block: ActiveBlock,
                 siblings: dict[tuple[str, str], list[_SiblingBasis]]
                 ) -> list[Finding]:
    """THE SIXTH FINDING CLASS — the PAIRING, and no comparison at all.

    NOT AN ARM, on the same reading `_arm_marker_defects` is not one: the three
    arms read two documents against each other, and this reads a delta's own
    markers against the set of active additions. Its inputs contain NO
    requirement text, so the 2026-08-27 ruling against synthesising a basis
    from a sibling's ADDED text is untouched — what changes is only that the
    block is no longer dropped before anything looks at it, so the arms' silence
    stops reading as clearance when it is uncomparability.
    """
    state = _pairing_state(block, siblings)
    if state is None:
        return []
    name, why = state
    return [Finding(
        _PAIRING_SEVERITY, FAMILY, repo, block.delta_rel,
        TEMPLATE_PAIRING.render(title=block.title, state=name, why=why),
        _PAIRING_ACTION)]


_COLLISION_ACTION = (
    "promote nothing further until the collision is resolved, and — where the "
    "requirement genuinely already exists — convert the addition to a "
    "modification declared against canon, or withdraw or re-target the rename "
    "whose `TO:` title canon already carries")

_COLLISION_KIND = {
    _BASIS_ADDED: "`## ADDED Requirements`",
    _BASIS_RENAMED: "`## RENAMED Requirements` `TO:`",
}


def _collision_findings(repo: str,
                        siblings: dict[tuple[str, str], list[_SiblingBasis]],
                        canon_for, dispositions) -> list[Finding]:
    """THE SEVENTH FINDING CLASS — the archive-ordering backstop.

    An active `## ADDED Requirements` block, or the `TO:` half of an active
    `## RENAMED Requirements` block, naming a title the promoted specification
    ALREADY carries. Where a MODIFIED-over-a-sibling's-basis pair archives in
    the SAFE order the requirement enters canon first and every existing check
    resumes; where it archives in the UNSAFE order the modifying block promotes
    text nobody reviewed as an addition, and THIS is the surviving evidence.

    NOTHING IN THE ESTATE READS THAT SHAPE. `promotion-fidelity` compares an
    ARCHIVED delta to canon, and after the archive act canon IS the delta; this
    family reads ADDED and RENAMED blocks only to build the pending set, never
    against canon. Reading it costs one lookup against the promoted index this
    family already builds and one more pass over the entries `sibling_titles`
    already parsed — a second use of one parse rather than a second parser.

    THE `FROM:` HALF IS NEVER READ, and the direction is the whole of what makes
    the check readable: a rename's SOURCE is a title canon is expected to carry,
    so reading it would report every lawful rename in the corpus.

    NOT LIMITED TO THE PAIR THAT MOTIVATES IT. A title canon already carries is
    a defect however it arose — a stale packet, a duplicated title, an addition
    that should have been a modification — and narrowing the check to blocks
    with a MODIFIED partner would decline to report the same defect for a worse
    reason.
    """
    out: list[Finding] = []
    for capability, key in sorted(siblings):
        canon = canon_for(capability)
        if not canon or key not in canon:
            continue
        promoted_requirement = canon[key]
        for basis in siblings[(capability, key)]:
            if promotion_fidelity.disposed(dispositions, repo, basis.delta_rel,
                                           basis.title):
                continue
            if basis.kind == _BASIS_ADDED:
                why = (f"`{basis.change}` is still active and its addition has "
                       f"not promoted, so the title it writes is one canon "
                       f"already states — the surviving evidence of an archive "
                       f"taken in the unsafe order, which no health run can "
                       f"undo")
            else:
                why = (f"`{basis.change}` is still active and renames another "
                       f"requirement INTO a title canon already states; its "
                       f"`FROM:` half is not read here, a rename's source "
                       f"being a title canon is expected to carry")
            out.append(Finding(
                _COLLISION_SEVERITY, FAMILY, repo, basis.delta_rel,
                TEMPLATE_COLLISION.render(
                    block_kind=_COLLISION_KIND[basis.kind],
                    title=basis.title,
                    spec_rel=promoted_requirement.spec_rel, why=why),
                _COLLISION_ACTION))
    return out


def resolve(block: ActiveBlock, canon: dict[str, PromotedRequirement] | None,
            siblings: dict[tuple[str, str], list[_SiblingBasis]]):
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


def _chain(changes: list[str], pairs: set[tuple[str, str]]
           ) -> tuple[list[str] | None, str, list[str]]:
    """`(order, defect, blamed)` for one group's declarations, earliest first.

    THE DECLARATION IS AN EDGE, AND THE EDGE POINTS BACKWARDS. `(a, b)` in
    `pairs` says `a`'s proposal names `b`, which under `release-realization`'s
    "Ordered deltas and branch vocabulary" makes `a` the LATER writer: it is the
    one declaring its deltas relative to `b`'s outcome. So the earliest writer is
    the one that names nobody inside the group.

    RESOLVED MEANS ONE TOTAL ORDER, NOT ONE EDGE PER WRITER, and the difference
    is measured rather than stylistic. OpsxFactory's five-writer chain carries a
    REDUNDANT edge — `reanchor-keycloak-broker-to-syscore2` names both its
    predecessor `admit-secretproviderclass-to-aks-scope` and, three links back,
    `adopt-keycloak-broker-qa`, which it re-anchors and could hardly discuss
    without naming. That edge states nothing the other four do not already imply
    by transitivity, and a rule counting one predecessor per writer would report
    a compliant corpus as forked. The question this answers is therefore whether
    the declarations admit exactly ONE linear order, which is Kahn's algorithm
    with a uniqueness demand at every step.

    THE DEFECT IS NAMED BY WHERE THE UNIQUENESS FAILS, and the three failures are
    distinguishable by construction rather than by guessing:

    - no writer at all is free of in-group declarations -> `cycle` (mutual
      declaration is the two-writer instance of it, and that shape never reaches
      here, `_arm_ordering`'s pair path owning it);
    - MORE THAN ONE writer is free at the FIRST step -> `unanchored`: each of
      them declares relative to nothing inside the group, so the declarations
      state more than one starting point where a chain has exactly one;
    - more than one writer becomes free LATER -> `forked`: each of them is
      declared later than a writer already placed and none is declared later
      than another, so no single chain runs through them.

    `blamed` is the ambiguous or cyclic set, sorted, so the finding can name the
    writers a reader has to go and look at instead of re-deriving them.
    """
    later: dict[str, set[str]] = {c: set() for c in changes}
    for declarer, declared in pairs:
        later[declarer].add(declared)
    remaining = set(changes)
    order: list[str] = []
    while remaining:
        free = sorted(c for c in remaining if not (later[c] & remaining))
        if not free:
            return None, "cycle", sorted(remaining)
        if len(free) > 1:
            return None, ("unanchored" if not order else "forked"), free
        order.append(free[0])
        remaining.discard(free[0])
    return order, "", []


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

    N RATIFIED WRITERS RESOLVE ON THE SAME TERMS WHERE THE DECLARATIONS STATE
    ONE LINEAR CHAIN (issue #627, 2026-09-04). The 2026-08-27 reading reported
    every group of three or more as unstated "whatever they declare", on the
    stated ground that inventing a chain rule for a population of ZERO would be
    inventing authority. The population is no longer zero: OpsxFactory's
    `aks-administration-workflow` 'Bounded action classes for managed workloads'
    has FIVE ratified writers, each declaring its predecessor (PR #182), and
    `release-realization`'s "Ordered deltas and branch vocabulary" obligates that
    declaration from EVERY later writer — so a checker that cannot read an
    N-writer chain cannot read a compliant corpus. Nothing about the RULE
    changed: the declaration is still the ordering, still read whole-token from
    the declaring change's own `proposal.md`, and still the only authority
    consulted. What changed is that the arm now asks whether the declarations
    admit exactly ONE order (see `_chain`) rather than counting them.

    THE BASIS RUNS ALONG THE CHAIN. The earliest writer is measured against
    canon, and every later writer against the block of the writer immediately
    before it — the same substitution the pair makes, applied link by link,
    because `MODIFIED` replaces a requirement wholesale and each block therefore
    IS the outcome of the writer that holds it.

    THE 2-WRITER PATH IS UNTOUCHED, deliberately and structurally: its branch is
    still taken first and still returns the same dict, so no rendered byte of the
    pair case — resolved, mutual or undeclared — moves with this change.

    Everything else is an UNSTATED ordering, reported against every one of their
    blocks, each measured against canon:

    - NEITHER of two declaring — "no reader being able to tell which text canon
      will keep";
    - BOTH of two declaring — "mutual declaration deciding nothing";
    - a group of three or more whose declarations state no single chain, named
      by the defect `_chain` found: `cycle`, `forked`, `unanchored`, or
      `outside` — the last one being an `unanchored` group where a writer's
      declaration names a writer of this requirement that is NOT ratified, which
      explains the missing anchor instead of leaving a reader to find it.

    An UNRATIFIED writer creates no obligation either way: `release-realization`
    scopes the rule to an active RATIFIED change and this family does not widen
    it. Its block is still read, because the arms are advisory; it is not a link
    in the chain, and a declaration pointing at it orders nothing.
    """
    ratified = [b for b in group if b.standing == _RATIFIED]
    if len(ratified) < 2:
        return {}, []
    pairs = {(a.change, b.change) for a in ratified for b in ratified
             if (a.change, b.change) in declared}
    by_change = {b.change: b for b in ratified}
    if len(ratified) == 2 and len(pairs) == 1:
        declarer, other = next(iter(pairs))
        return {declarer: _as_basis(by_change[other])}, []

    defect, blamed = "", []
    if len(ratified) > 2:
        order, defect, blamed = _chain(sorted(by_change), pairs)
        if order is not None:
            return {late: _as_basis(by_change[early])
                    for early, late in zip(order, order[1:])}, []
        unratified = {b.change for b in group} - set(by_change)
        outside = sorted((a, b) for a in blamed for b in unratified
                         if (a, b) in declared)
        if defect == "unanchored" and outside:
            defect, blamed = "outside", list(outside[0])

    names = ", ".join(sorted(b.change for b in ratified))
    listed = ", ".join(blamed)
    if defect == "cycle":
        why = (f"{len(ratified)} active ratified changes write it and their "
               f"declarations run in a cycle, leaving {listed} unplaceable — "
               f"a cycle states no order")
    elif defect == "forked":
        why = (f"{len(ratified)} active ratified changes write it and the "
               f"declarations fork at {listed}: each is declared later than a "
               f"writer already placed and none is declared later than "
               f"another")
    elif defect == "unanchored":
        why = (f"{len(ratified)} active ratified changes write it and {listed} "
               f"each declare relative to no other ratified writer of it, so "
               f"the declarations state {len(blamed)} starting points rather "
               f"than one chain")
    elif defect == "outside":
        why = (f"{len(ratified)} active ratified changes write it and "
               f"{blamed[0]} declares relative to {blamed[1]}, which writes it "
               f"but is not ratified, so that declaration anchors nothing "
               f"inside the ratified group")
    elif pairs:
        why = (f"{len(pairs)} declarations stand between them, and mutual "
               f"declaration decides nothing")
    else:
        why = ("neither names the other, so the ordering is unstated rather "
               "than merely unrecorded")
    findings = [
        _finding(_RESOLUTION_SEVERITY, repo, block,
                 TEMPLATE_ORDERING.render(title=block.title, names=names,
                                          why=why))
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
        siblings = sibling_titles(root)
        canon_cache: dict[str, dict[str, PromotedRequirement] | None] = {}

        def canon_for(capability: str, root=root):
            if capability not in canon_cache:
                canon_cache[capability] = promoted(root, capability)
            return canon_cache[capability]

        # THE COLLISION CLASS RUNS BEFORE THE `not blocks` GUARD, and the order
        # is the class's own subject. Its inputs are an ADDED block and a
        # rename's `TO:` half — a repository carrying NO MODIFIED block at all
        # can still hold the surviving evidence of an archive taken in the
        # unsafe order, and the guard below would have hidden exactly that
        # repository.
        findings.extend(
            _collision_findings(repo, siblings, canon_for, dispositions))
        if not blocks:
            continue
        declared = declarations(root, blocks)

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
                    # THE PAIRING EMIT REPLACES THE DROP, AND REPLACES NOTHING
                    # ELSE (`govern-sibling-added-modified-deltas`). The three
                    # comparison arms still do NOT run against a pending block —
                    # the `continue` below is the same `continue` — and
                    # `resolve` is untouched, so its second step still hands a
                    # rename-and-amend block to canon under the OLD name one
                    # place above and that shape never reaches this branch.
                    findings.extend(_arm_pairing(repo, block, siblings))
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
        TEMPLATE_UNRESOLVED.render(title=block.title, why=why))


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
    """One of this family's seven finding classes, as a value.

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

    `gloss` is the parenthetical a reader gets beside the band. Two of the seven
    carry one and five do not: the scenario-title arm's says it carries the
    gate, and the ledger's repeats the hedge every one of its findings already
    states. Adding a gloss to the other five would pad a line whose whole value
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
# THE TWO `govern-sibling-added-modified-deltas` ADDS. Neither may contain
# `unclassified`, on the rule the fifth class's comment states below.
CLASS_PAIRING = "sibling-pairing"
CLASS_COLLISION = "added-over-canon"
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
# SEVEN ENTRIES FOR EIGHT RULE SHAPES. The delta's third arm is "Title
# resolution and ordering": a block resolving to nothing and an ordering no
# declaration settles are two shapes of ONE arm, sharing a severity and an
# action, named together in the requirement. Splitting them here would claim a
# class the delta does not define; merging any other pair would hide a severity
# difference. The sixth shape is the fifth class's own finding, which the map
# must place or the count would name itself. The seventh and eighth are the two
# `govern-sibling-added-modified-deltas` adds — one template each, so one shape
# each: the pairing class's FOUR reported states share a band, an action and a
# template and differ only in an interpolated clause, which is what makes them
# one shape rather than four.
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
    # INSERTED BEFORE `unplaced`, NOT APPENDED, so BOTH standing ordering claims
    # stay true: the gate-bearing arm reads FIRST, and the drift class — which
    # reads this map's own verdict on everything above it — reads LAST.
    # NO GLOSS on either, on the rule `FindingClass` states: the labels already
    # say what they are, and two more parentheticals would pad the one block
    # whose whole value is being short enough to read at a glance.
    FindingClass(CLASS_PAIRING, "sibling-pairing declaration",
                 _PAIRING_SEVERITY, _PAIRING_ACTION),
    FindingClass(CLASS_COLLISION, "added-over-canon collision",
                 _COLLISION_SEVERITY, _COLLISION_ACTION),
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
    # THE SIXTH AND SEVENTH, ANCHORED PAST THE TITLE'S `repr` LIKE EVERY OTHER
    # ENTRY. The pairing class shares `_BLOCK_HEAD` because its subject IS a
    # MODIFIED block; the collision class cannot, its subject being an ADDED
    # block or a rename's `TO:` half, so it spells its own anchor to the same
    # depth — from the start of the rule and past the closing quote of the
    # title — for the same measured reason: titles come from the corpus and may
    # contain any phrase, including another class's.
    (CLASS_PAIRING, re.compile(
        _BLOCK_HEAD + r"rests on an active sibling's addition rather than on "
                      r"canon, and the pairing is ")),
    (CLASS_COLLISION, re.compile(
        r"^active (?:`## ADDED Requirements`|`## RENAMED Requirements` `TO:`) "
        r"block for " + _TITLE_REPR + r" writes a requirement title ")),
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
    `Finding` is shared by twenty-three families and the semantic lanes: a field
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


# The fifth class's rule text IS one of the arm templates, registered with the
# others at the top of this module. Named here too because the self-gate probes
# it and because a reader of this section should not have to go looking.
_DRIFT_RULE = TEMPLATE_DRIFT.text

# THE SHAPE MASK — AMENDED 2026-08-28 ON BRETT'S RULING, verbatim: "Amend: shape
# = arm template, all interpolations masked".
#
# WHAT IT IS NOW. Two rule texts are ONE SHAPE where they come from the SAME ARM
# TEMPLATE, whatever their interpolated values. So one shape is one template,
# one template is one map entry to write, and the count of drift findings is the
# count of REMEDIES — which is what a ranked plan is a list of.
#
# WHAT IT WAS, AND WHY THAT WAS WRONG. The first ratified rule masked quoted
# spans and digit runs only, which left every UNQUOTED interpolation
# shape-bearing: the promoted spec's repo-relative path, the `[body]`/`[bullet]`
# unit-kind list, a change-id list, an unresolved block's `why` clause. MEASURED
# on this repository: dropping one class pattern emitted SIX findings for SEVEN
# unplaced ones, where a single new map entry would have placed all seven.
# `026-unplaced-finding-drift` shipped that faithfully, measured it, refused to
# widen it unilaterally because the delta's third scenario pinned it, and put it
# up. Brett amended the delta.
#
# TWO STEPS, AND THE ORDER IS LOAD-BEARING.
#
# 1. MASK THE `repr` SPANS, left to right. Requirement titles and quoted body
#    units come from the CORPUS and may contain any phrase, including another
#    arm's fixed prose, so template matching over RAW text could file one arm's
#    finding under another's template. Masked first, the only text left is this
#    module's own prose plus placeholders.
#
#    A CONSUMER, NOT A GLOBAL `re.sub`, and that is a bug this function shipped
#    with. These rule texts are fixed prose interleaved with `repr` spans, and
#    one of the fixed strings carries an apostrophe: `TEMPLATE_UNRESOLVED`'s "no
#    active sibling's addition:". A global substitution pairs THAT apostrophe
#    with the opening quote of the NEXT repr, masks the prose between them, and
#    leaves the repr's own content exposed — which also destroys the fixed prose
#    the template match depends on. So a quote OPENS a span only where a `repr`
#    could have emitted one: at the start, or after a non-alphanumeric. Every
#    one of this family's templates interpolates its `repr` after a space, and
#    an apostrophe inside a word never can be. `_TITLE_REPR`'s two alternatives
#    begin with DIFFERENT characters, so at most one matches at any position,
#    and an accepted span is jumped past whole — no backtracking into a span
#    already consumed.
#
# 2. MATCH THE ARM TEMPLATES, first match wins. The shape IS the template's id.
#
# FAIL-CLOSED FALLBACK. A rule text NO template claims — which means an arm's
# fixed prose itself drifted from its template, or a text arrived from somewhere
# this module does not know — falls back to the old lexical mask rather than
# being merged with any template. Constitution VII: an unrecognized value is
# never absorbed into a neighbouring bucket.
#
# SCOPED TO THIS FAMILY. `add-unclassified-finding-class` § 4.4: this is written
# for this family's rule-text grammar and is NOT a general finding-identity rule
# for the package. Nothing else may import it as one without its own change.
_SHAPE_QUOTED = re.compile(_TITLE_REPR)
_SHAPE_DIGITS = re.compile(r"\d+")
_SHAPE_OPENERS = "'\""


def _mask_repr_spans(rule: str) -> str:
    """Every `repr`-emitted span replaced by one placeholder, left to right.

    Step 1 of `_shape`; see the comment above for why it is a consumer and not
    a global substitution.
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
    return "".join(out)


def _shape(rule: str) -> str:
    """The identity two unplaced findings are grouped by: their ARM TEMPLATE.

    Returns the template's id where one claims the rule, and the old lexical
    mask where none does.
    """
    masked = _mask_repr_spans(rule)
    for template in _ARM_TEMPLATES:
        if template.matches(masked):
            return template.id
    return _SHAPE_DIGITS.sub("<N>", masked)


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

    THE GRAIN IS ONE FINDING PER ARM TEMPLATE, WHICH IS ONE PER REMEDY. Two
    rule texts are one shape where they come from the SAME TEMPLATE, whatever
    their interpolated values — the requirement title, the counts, the promoted
    spec's path, the unit-kind list, a change-id list, an unresolved block's
    `why` clause. One template is one entry somebody has to add to the class
    map, and a ranked plan is a list of remedies.

    THAT IS AN AMENDMENT, RULED 2026-08-28 BY BRETT, verbatim: "Amend: shape =
    arm template, all interpolations masked". As first ratified the rule masked
    quoted spans and digit runs only, which left every UNQUOTED interpolation
    shape-bearing: dropping ONE class pattern on this repository emitted SIX
    findings for SEVEN unplaced ones, and nine unplaced findings on the
    `-two-writers` fixture became four. `026-unplaced-finding-drift` shipped
    that faithfully, measured it, declined to widen it unilaterally because the
    delta's third scenario pinned it, and put the amendment up. All four of
    those measurements now read ONE — the figures are in
    `test_the_drift_grain_is_one_finding_per_arm_template`, which holds them.

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
            TEMPLATE_DRIFT.render(n=len(group),
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
