"""The release-tag publication family (`add-release-tag-publication-check`).

WHAT IT ANSWERS. `docs/contract-versioning-policy.md` holds that "a bundle is
not published until its tag exists" and that "the tag SHALL point to that
realized commit". Nothing checked either. No workflow calls the release
validator; `verify_tag` is exercised only by unit tests over synthetic
repositories; `release-surface-integrity` deliberately does not anchor on tags
so its own drift obligation stays evaluable in the window before one exists; and
`tag-hygiene` is `document-lifecycle`'s PROSE-tag grammar over document text,
which is the trap in its name. The declaring commit and the published tag are
two acts by two actors with nothing joining them.

THE CLASS IS NOT HYPOTHETICAL — IT HAPPENED TWICE, and both catches were human.
`contract-v1.33`, `contract-v1.35` and `contract-v1.39` went untagged for weeks
and were discharged only on a ruling of 2026-08-25. `contract-v2.3` and
`contract-v2.4` repeated it on 2026-08-30/31, and the cut that landed the second
wrote a careful disposition subsection for the FIRST one's missing tag while
standing in the same gap — which is what a process with no place to notice looks
like.

WHY DISTANCE AND NOT TIME. The interval between declaring a bundle and tagging
it is legitimate: a cut declares, the owner tags afterwards. A family that fired
on the declaration would redden every correct release, and a family nobody can
leave green gets configured away. Distance is counted in FIRST-PARENT COMMITS ON
PUBLISHED `main`, never wall time, because landings are what the policy's own
retro-publication rule counts and wall time punishes a quiet week.

WHY THE TWO FAILURES ARE DIFFERENT FINDINGS. An ABSENT tag is an incomplete
release. A tag that peels to a commit NOT declaring the bundle is MISPLACED: it
satisfies every check that asks only whether a tag exists, it is what consumers
pin, and it is worse than absence because it looks like completion. Reported
alike, the common one would hide the serious one.

WHAT THIS FAMILY DOES NOT PROVE, disclosed rather than hidden (proposal D4). The
policy's target is "the EARLIEST FIRST-PARENT COMMIT on published `main` that
DECLARES the bundle and at which `verify-commit` PASSES". The second conjunct is
a digest verification per candidate and is out of scope here, so a tag on a
LATER declaring commit passes this family and remains a defect under the policy.

NOT BUILT ON `verify_tag`, deliberately (proposal D5). That helper cannot
distinguish "I have not fetched" from "this tag is unreachable from `main`":
`git merge-base --is-ancestor` exits 128 when an argument is not a commit in the
local object store and that is folded in with the genuine negative (#338).
Observed live, it fails identically on `contract-v2.2`, whose tag is correct. A
family built on it would report the benign case in the serious case's words.

THE THIRD STATE — SPENT (`declare-spent-bundle-state`, ratified 2026-09-02;
openxFactory issue #575). Between *published* and *owes a tag* sits a number
that was cut, was never publishable, and never will be: `contract-v2.6`, whose
one first-parent declaring commit fails `verify-commit` five ways and which
declares change class ADDITIVE over a tree that refuses three shapes
`contract-v2.5` accepted. The action the SUPERSEDED finding prescribes —
retro-publication — is UNPERFORMABLE for it by anyone, and a finding whose only
prescribed action cannot be taken is one a reader learns to skip.

SILENCE IS NEVER A DECLARATION, and that sentence carries the whole of this
state's fail-closed character. A superseded untagged bundle no declaration names
reads exactly as it did before this state existed, at `error` and in the same
words. The state is entered ONLY by an explicit reserved-form line in
`contracts/CHANGELOG.md` at the PUBLISHED TIP, written inside the changelog entry
of the bundle that superseded it — so the declaring act is the LATER CUT that
allocates the replacement, and a bundle can never declare itself spent.

AND THE SUCCESSOR GUARD IS WHAT MAKES IT UNABUSABLE (ruled by Brett Heap,
2026-09-02). A declaration is quiet only where the superseding bundle it names is
itself CUT, itself PUBLISHED, and STRICTLY LATER — so the only way to retire a
number is to publish its replacement's tag, which is the very act this family
exists to compel. Cut but unpublished is PROVISIONAL: one `warning`, and the
superseded `error` is suppressed in its favour, because the successor is the
bundle the manifest now declares and is graded by the distance arm on its own
account. Never cut, not later, malformed, duplicated, in the wrong entry, or
naming the live bundle: `error`, accepting nothing, with the superseded `error`
standing alongside so a bad declaration removes nothing.

WHY THE FINDINGS OF THIS STATE LEAVE `contracts/manifest.yaml`. A finding's
identity is `(family, repo, path)` and ignores its rule text. Every other finding
here lands on the manifest, so a spent state landed there would share an identity
with all of them and its disappearance would be masked by any surviving sibling;
two bundles declared spent would share `contracts/CHANGELOG.md` for the same
reason. The per-bundle inventory `contracts/releases/<bundle>.digests.yaml` is the
one path unique to the bundle BY CONSTRUCTION — it is the artifact whose existence
made the bundle enumerable in `cut_bundles` at all. ONE finding has no such path
to land on and keeps the changelog: a declaration whose SUBJECT was never cut
disposes nothing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from . import ERROR, INFO, WARNING, Finding, Skip

FAMILY = "release-tag-publication"
MANIFEST = "contracts/manifest.yaml"
RELEASES = "contracts/releases"

# THE SPENT STATE'S RECORD, and the only document it is read from
# (`declare-spent-bundle-state` OD-1). Three facts pick it: it is a member of
# every release digest inventory, so the record travels with the bundle a
# consumer pins; it is one of the THREE EDITORIAL MEMBERS the versioning policy
# allows to move between cuts, so a disposition can be written when the fact
# arises rather than waiting for a bundle that may never be cut; and it is
# already where this estate records supersessions. NOT `health/dispositions.yaml`
# — that file keys on `(family, repo, path)`, so one row would suppress every
# finding this family could ever raise about a repository, and it lives at the
# aggregation root where a `--single-repo` self-gate cannot see it at all.
CHANGELOG = "contracts/CHANGELOG.md"

# Mandatory publication begins at contract-v1.7; contract-v1.0 through v1.6 are
# an explicitly recovered legacy sequence and carry no tags BY DESIGN, per the
# changelog's own baseline note. Reporting them would emit seven permanent
# findings nobody may act on, which is how a report teaches its readers to stop
# reading it.
ENFORCEMENT_FLOOR = (1, 7)

# RULED BY BRETT HEAP, 2026-08-31: five first-parent landings. The calibration
# it answers to: `contract-v2.3` sat untagged across SIX first-parent landings
# before a human noticed, so any threshold above five would have stayed silent
# through the recurrence this family exists to catch.
DEFAULT_THRESHOLD = 5

_BUNDLE = re.compile(r"^contract_bundle_version:\s*(\S+)\s*$", re.M)
_VERSION = re.compile(r"^contract-v(\d+)\.(\d+)$")

_SUPERSEDED_ACTION = (
    "publish the annotated tag retrospectively at the commit the versioning "
    "policy's rule identifies — RETRO-PUBLISHED, NOT RE-DATED, as the "
    "2026-08-25 discharge did for contract-v1.33, v1.35 and v1.39")
_ABSENT_ACTION = (
    "publish the annotated tag at the commit the versioning policy's rule "
    "identifies — the earliest first-parent commit on published main that "
    "declares the bundle and at which verify-commit passes — never edit the "
    "manifest, the changelog or the inventory to match the absence")
_MISPLACED_ACTION = (
    "re-point the annotated tag at a commit that declares this bundle, or "
    "withdraw it; a tag on a commit declaring something else is what "
    "consumers will pin")
_LIGHTWEIGHT_ACTION = (
    "replace the lightweight ref with an ANNOTATED tag; the policy requires "
    "one, and a lightweight ref carries no tagger, no date and no message")

# --- the SPENT state's four actions ----------------------------------------
#
# BESIDE the four above rather than folded into them. The absent-tag action
# prescribes publishing a tag; none of these does, because the whole subject of
# this state is a number for which that act is unperformable.
_SPENT_ACCEPTED_ACTION = (
    "no action, and this is NOT the tag obligation having been met — it was "
    "EXTINGUISHED, by an owner act, at the cost of a version number, and the "
    "record says which; the state is permanent, and never edit the manifest, "
    "the changelog or the inventory to stop it being reported")
_SPENT_UNPROVEN_ACTION = (
    "publish the SUPERSEDING bundle's annotated tag at the commit the "
    "versioning policy's rule identifies; a bundle is not published until its "
    "tag exists, so until then this supersession is a claim and not evidence — "
    "and the superseding bundle is graded on its own account meanwhile")
_SPENT_REFUSED_ACTION = (
    "repair the SPENT declaration in contracts/CHANGELOG.md or withdraw it — "
    "one reserved-form line, inside the superseding bundle's own entry, naming "
    "a cut, published and STRICTLY LATER bundle, its cause, the ruling's author "
    "and date, and the measurement of record; the superseded bundle stays "
    "reported until a declaration is ACCEPTED, and never edit the manifest, the "
    "changelog or the inventory to match the absence")
_SPENT_ORPHAN_ACTION = (
    "correct the SUBJECT of the SPENT declaration in contracts/CHANGELOG.md: as "
    "written it names a bundle this repository never cut, so it disposes "
    "nothing, and the bundle it was meant to name is still reported by this "
    "family")


def parse_bundle(manifest: bytes | str | None) -> str | None:
    """The declared bundle, or None where the manifest does not declare one.

    ACCEPTS BYTES, because `blobs_at` answers raw Git blob bytes — the release
    inventory's identity rule is computed over them and naming text
    canonicalization an invalid digest source, so the shared reader hands every
    caller bytes. A version string is the one thing in that file it is safe to
    decode, and decoding with `replace` keeps a mis-encoded byte elsewhere in
    the manifest from turning a readable declaration into a crash.
    """
    if not manifest:
        return None
    if isinstance(manifest, bytes):
        manifest = manifest.decode("utf-8", errors="replace")
    found = _BUNDLE.search(manifest)
    return found.group(1) if found else None


def inventory_path(bundle: str) -> str:
    """The release inventory that made `bundle` enumerable, which is where every
    finding of the SPENT state lands but one. Unique to the bundle BY
    CONSTRUCTION, which is the whole of OD-5's argument."""
    return f"{RELEASES}/{bundle}.digests.yaml"


# --- the SPENT declaration reader -------------------------------------------
#
# THE RESERVED OPENER. No other text in `contracts/CHANGELOG.md` may begin a
# line with it, and a line that begins with it and does not complete the form is
# a MALFORMED DECLARATION rather than prose to be ignored — which is why the
# reader below REPORTS what it could not read instead of skipping the line. The
# form, whole:
#
#     **SPENT BUNDLE:** `<bundle>` — SUPERSEDED BY `<superseding bundle>` — CAUSE: <text> — RULED BY <author>, <YYYY-MM-DD> — MEASUREMENT: <citation>
#
# A HANDLE ON THE RECORD AND NOT A SECOND RECORD: it is written INSIDE the human
# disposition subsection the cut writes anyway, in the pattern
# `document-lifecycle`'s reserved `Modified over` marker already sets.
SPENT_OPENER = "**SPENT BUNDLE:**"

# --- THE CONTAINING ENTRY, AND ITS BOUNDARIES -------------------------------
#
# `contracts/CHANGELOG.md`'s bundle entries are `##` headings whose first token
# is the bundle name; the declaring act is the SUPERSEDING bundle's own entry,
# so this is what decides whether a declaration was written by the cut that
# allocated the replacement or by somebody else. It is the guard the ratified
# requirement leans on hardest — *"accepted only where the changelog entry
# CONTAINING it is the entry of the bundle it names as the superseding one"*.
#
# EVERY WAY OF CLOSING AN ENTRY THE READER DOES NOT KNOW ABOUT IS AN ACCEPT.
# That is the asymmetry the hardening turns on: a declaration under an
# unrecognized boundary keeps the PREVIOUS release entry's authority, matches
# the bundle it names, and quiets the superseded-and-never-published `error`
# this family exists to raise. Ten such escapes were measured against the first
# implementation of this rule (PR #584's five bot rounds, and the read-only
# comparison of them against this module recorded in that PR's 2026-09-02
# 17:05Z comment); the lesson of them is structural rather than per-case, so
# the rule now lives in ONE function — `_entry_boundary` — that every heading
# shape passes through, rather than in one regex a reader has to re-derive.
#
# OVER-CLOSING IS FAIL-CLOSED AND UNDER-CLOSING IS NOT, which decides every
# judgment below. Closing an entry can only move a declaration OUT of one, and
# a declaration inside no entry is REFUSED with the superseded `error` standing
# beside it. Failing to close one can only leave a declaration holding
# authority nobody granted it. So a boundary is recognized wherever CommonMark
# says a heading may be, while a boundary OPENS an entry only in the single
# shape the requirement names.

# ATX headings at level ONE and TWO close the open entry; level THREE and
# deeper do not, and that exclusion is LOAD-BEARING rather than tidy: this
# repository's own reserved line lives inside a
# ``### `contract-v2.6` disposition`` subsection OF the `## contract-v3.0`
# entry, so a rule that closed on `###` would refuse the live declaration.
# Up to three leading spaces, because CommonMark says an ATX heading may carry
# them — `  ## Deprecations` IS a heading and was being missed; FOUR spaces is
# an indented code block and is not a heading at all. The trailing lookahead is
# `[ \t]|$` so that `##` ALONE is a boundary (a legal EMPTY ATX heading) while
# `#550 example` — real text in this repository's changelog — is correctly not
# a heading, because `#` followed immediately by a non-space is none.
#
# AND IT IS `[ \t]` RATHER THAN `\s`, WHICH IS AN ESCAPE AND NOT A STYLE
# PREFERENCE (Codex P1, round 3 on PR #589). CommonMark's ATX opening sequence
# must be followed by a SPACE, a TAB or the end of line; Python's `\s` also
# matches U+00A0 and the other Unicode spaces. So `## contract-v3.0` is
# PARAGRAPH TEXT to every renderer and opened a FICTITIOUS `contract-v3.0`
# entry here — measured, and a declaration below it was ACCEPTED under a
# heading that does not exist. The narrower class is fail-closed in both
# directions: such a line now neither opens an entry nor closes one, matching
# what the document actually means.
_ATX_BOUNDARY = re.compile(r"^ {0,3}#{1,2}(?!#)(?=[ \t]|$)")

# Any ATX heading, at any legal level, used only to decide what CANNOT be the
# text of a Setext heading. Seven or more `#` is not a heading in CommonMark,
# which is what the negative lookahead says; `[ \t]` for the reason above.
_ATX_ANY = re.compile(r"^ {0,3}#{1,6}(?!#)(?=[ \t]|$)")

# THE VERSION TOKEN MUST BE COMPLETE, AND `\b` IS NOT THAT TEST. `\b` matches
# between `0` and `.`, so `## contract-v3.0.1` and `## contract-v3.0-notes`
# each OPENED an entry named `contract-v3.0`, containing a declaration the
# `contract-v3.0` entry never wrote. `## contract-v3.01` is deliberately NOT in
# that class and still opens an entry: it is a well-formed bundle name (major
# 3, minor 01), and a declaration under it is refused later for naming a
# DIFFERENT bundle, which is the honest reason.
#
# BOTH SPACE CLASSES ARE `[ \t]` for the reason `_ATX_BOUNDARY` records: the
# separator after `##` because a Unicode space there means the line is not a
# heading at all, and the one after the version token so that a name followed
# by U+00A0 is not read as a complete token.
_ENTRY_HEADING = re.compile(
    r"^ {0,3}##(?!#)[ \t]+(contract-v\d+\.\d+)(?=[ \t]|$)")

# SETEXT HEADINGS CLOSE AN ENTRY AND NEVER OPEN ONE. `Title` over `===` is an
# H1 and `Title` over `---` an H2 — both boundaries. Neither opens an entry:
# the requirement names `##` entries, and under-opening is the fail-closed half
# (a declaration below a Setext bundle name then sits in no entry and is
# refused, where reading it as an opener would accept a containment nobody
# wrote as an entry). A run of `=` or `-` is an UNDERLINE only where a
# paragraph line precedes it, which is exactly what separates `Title`/`---`
# from the thematic break `---` standing after a blank line, and from a
# `|---|---|` table rule, which does not match at all.
_SETEXT_UNDERLINE = re.compile(r"^ {0,3}(=+|-+)[ \t]*$")

# A FENCED BLOCK IS OPAQUE — TO HEADINGS AND TO DECLARATIONS ALIKE — and this
# is the one escape the LIVE document could already hit, because
# `contracts/CHANGELOG.md` carries a fenced block. Both directions were
# measured: a fenced `## contract-v3.0` REOPENED an entry, so a declaration
# under a later `## Notes` read as contained by the v3.0 entry and was
# ACCEPTED.
#
# THE SUPPRESSION EXTENDS TO THE RESERVED OPENER, deliberately, and it is
# fail-closed in BOTH directions: a declaration shown as an EXAMPLE inside a
# fence cannot spend a bundle, and a real declaration HIDDEN inside a fence
# does not count — which leaves the superseded `error` standing rather than
# quieting it. The reserved opener is therefore reserved over the document's
# PROSE, and a fence is where the form may be DOCUMENTED without being
# PERFORMED. This REPLACES the module's earlier "no fence tracking,
# deliberately" reading, whose stated fear — a declaration hidden by
# indentation — is not reachable here: the opener is matched at column zero.
#
# A CLOSER IS NOT MERELY ANOTHER OPENER. It must use the SAME fence character,
# be AT LEAST as long, and be followed by nothing but whitespace, which is why
# the closer is its own pattern: ```` ```yaml ```` opens a block and does not
# close one.
#
# AND A BACKTICK FENCE'S INFO STRING MAY NOT CONTAIN A BACKTICK, which
# CommonMark says and the omission of which is an ESCAPE rather than a nicety
# (Codex P1, round 1 on PR #589). ```` ```bad`info ```` opens NO fence, so a
# reader that thinks it does is one fence out of phase with the document: the
# next bare ```` ``` ```` closes the reader's fictitious block while OPENING a
# real one, every boundary inside the real block is then read as prose, and a
# declaration inside it is read as a record — measured, and it was accepted from
# under a `## Notes` heading. A TILDE fence's info string MAY carry backticks,
# so the two openers are separate patterns rather than one with a shared class.
_FENCE_OPEN_BACKTICK = re.compile(r"^ {0,3}(`{3,})([^`]*)$")
_FENCE_OPEN_TILDE = re.compile(r"^ {0,3}(~{3,})")
_FENCE_CLOSE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*$")

# --- RAW HTML BLOCKS, which are opaque for the same reason fences are --------
#
# A ```-shaped line inside a raw HTML block is HTML CONTENT, not a fence
# delimiter, and a reader that treats it as one goes a fence OUT OF PHASE with
# the document — the failure round 1 and round 4 each found by a different
# route. CommonMark's seven kinds, of which all can hold such a line:
#
#   1  `<pre` `<script` `<style` `<textarea`, ending at the matching close tag,
#      SPANNING BLANK LINES — which is what makes it the useful hiding place
#   2  `<!--` … `-->`        3  `<?` … `?>`
#   4  `<!` + letter … `>`   5  `<![CDATA[` … `]]>`
#   6  one of CommonMark's own block-tag names, ending at a BLANK line
#   7  any COMPLETE tag alone on its line, ending at a blank line, and unable
#      to interrupt a paragraph
#
# KIND 6'S LIST IS COMMONMARK'S AND NOTHING WIDER, and kind 7 demands a
# complete tag, because OVER-approximating an HTML block is an escape of its
# own in the same silent direction: a line of prose read as HTML content would
# swallow a real `## Notes` boundary and leave a declaration below it holding
# an entry it is not inside. `<not a tag` opens nothing.
# `[ \t\v\f]` IS COMMONMARK'S WHITESPACE CLASS, and the omission of VT and FF
# was reachable only after round 4 stopped splitting lines on them (Codex,
# round 7): `<pre<VT>x>` is a kind-1 opener CommonMark recognizes and this
# pattern did not, so the fence-shaped line inside the block opened a fictitious
# fence and a declaration below was ACCEPTED. Measured for both characters.
#
# U+00A0 IS DELIBERATELY NOT HERE, and that half of the finding is REFUSED with
# a measurement: CommonMark's "whitespace character" is space, tab, newline, VT,
# FF or CR, and U+00A0 is none of them. `<pre<U+00A0>x>` is therefore NOT a
# kind-1 opener, and a reader that treated it as one would be MORE opaque than
# any renderer — the under-closing direction this whole guard exists to close.
# Measured: the reader's current answer for that line is already the
# CommonMark-correct one.
_HTML_TYPE1_OPEN = re.compile(
    r"^ {0,3}<(pre|script|style|textarea)([ \t\v\f>]|$)", re.I)
_HTML_TYPE6_TAGS = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|col"
    "|colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure"
    "|footer|form|frame|frameset|h1|h2|h3|h4|h5|h6|head|header|hr|html|iframe"
    "|legend|li|link|main|menu|menuitem|nav|noframes|ol|optgroup|option|p"
    "|param|search|section|summary|table|tbody|td|tfoot|th|thead|title|tr"
    "|track|ul")
_HTML_OPENERS = (
    ("html1", _HTML_TYPE1_OPEN),
    ("html2", re.compile(r"^ {0,3}<!--")),
    ("html3", re.compile(r"^ {0,3}<\?")),
    ("html5", re.compile(r"^ {0,3}<!\[CDATA\[")),
    # AFTER kind 5, because `<![CDATA[` also matches kind 4's shape and the two
    # have different closers — ordering is the whole difference between ending
    # at `]]>` and ending at the first `>`.
    # UPPERCASE, because the document is rendered by GitHub and GFM's spec
    # (CommonMark 0.29) says kind 4 is `<!` followed by an UPPERCASE ASCII
    # letter — CommonMark 0.30 later relaxed it to any letter (Codex, round 7).
    # The narrower class is also the safe one: accepting `<!doctype` would make
    # this reader MORE opaque than the renderer, which swallows boundaries.
    ("html4", re.compile(r"^ {0,3}<![A-Z]")),
    ("html6", re.compile(rf"^ {{0,3}}</?({_HTML_TYPE6_TAGS})([ \t\v\f]|/?>|$)",
                         re.I)),
)
# KIND 1 ENDS ON ANY OF THE FOUR END TAGS, AND THE SPEC SAYS SO IN WORDS:
# "line contains an end tag </script>, </pre>, </style>, or </textarea>
# (case-insensitive; IT NEED NOT MATCH THE START TAG)".
#
# ROUND 6 GOT THIS WRONG IN BOTH DIRECTIONS AT ONCE, AND IT IS THE MOST
# INSTRUCTIVE FAILURE ON THIS BRANCH. Codex and Copilot INDEPENDENTLY asked for
# a matching closer, twenty-five minutes apart, and their agreement was taken as
# corroboration — two reviewers converging on a precise mechanism. Both were
# wrong on the specification, and the fix they asked for INTRODUCED the very
# escape class it claimed to close: requiring `</pre>` to end a `<pre>` block
# made this reader MORE OPAQUE than CommonMark, so a real `## Notes` heading
# after a `</script>` was swallowed and a declaration below it was ACCEPTED
# under an entry it is not inside. Measured against a reference CommonMark
# implementation, which ends the block exactly where the spec says.
#
# WHAT IT COST TO FIND: nothing a bot round produced. Both bots had reviewed the
# fix and neither retracted it; it surfaced only when the reader's boundary
# decisions were run as a DIFFERENTIAL against a reference parser over every
# construct this branch had touched. Bot agreement is not evidence about a
# specification — a differential is.
_HTML_CLOSERS = {
    "html1": re.compile(r"</(pre|script|style|textarea)>", re.I),
    "html2": re.compile(r"-->"),
    "html3": re.compile(r"\?>"),
    "html4": re.compile(r">"),
    "html5": re.compile(r"\]\]>"),
}
_HTML_TAGNAME = r"[A-Za-z][A-Za-z0-9-]*"
_HTML_ATTR = (r"(?:[ \t\v\f]+[A-Za-z_:][A-Za-z0-9_.:-]*"
              r"(?:[ \t\v\f]*=[ \t\v\f]*"
              r"(?:[^\s\"'=<>`]+|'[^']*'|\"[^\"]*\"))?)")
_HTML_TYPE7 = re.compile(
    rf"^ {{0,3}}(?:<{_HTML_TAGNAME}{_HTML_ATTR}*[ \t\v\f]*/?>"
    rf"|</{_HTML_TAGNAME}[ \t\v\f]*>)[ \t\v\f]*$")

# A THEMATIC BREAK IS NOT PARAGRAPH CONTENT, so a run of `=` or `-` below one is
# a second thematic break and NOT a Setext underline (Codex P2, round 1). This
# is the one exclusion that moves the reader toward UNDER-closing and is still
# right to make: CommonMark is unambiguous about it, and the alternative refused
# a CORRECTLY CONTAINED declaration written below a horizontal rule.
_THEMATIC_BREAK = re.compile(
    r"^ {0,3}((\*[ \t]*){3,}|(-[ \t]*){3,}|(_[ \t]*){3,})$")

_SUBJECT_PROBE = re.compile(re.escape(SPENT_OPENER) + r"\s*`([^`]+)`")
_RULING_PROBE = re.compile(r"^(?P<author>.+?),\s*(?P<ruled_on>\d{4}-\d{2}-\d{2})$")
_RULING_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})\s*$")

# READ BY LABEL, IN ORDER, AND NOT BY SPLITTING ON THE SEPARATOR. Splitting a
# line on " — " would misread any declaration whose CAUSE carries an em dash —
# and would then name the WRONG element as the missing one, handing an author the
# wrong repair for a defect that is right there. Each label is found from the end
# of the one before it, so the order the form states is enforced by the search
# itself, and each element's value runs to the next label that was actually
# found.
_SUPERSEDING_LABEL = " — SUPERSEDED BY "
_CAUSE_LABEL = " — CAUSE: "
_RULED_LABEL = " — RULED BY "
_MEASUREMENT_LABEL = " — MEASUREMENT: "
_LABELS = (
    (_SUPERSEDING_LABEL, "the superseding bundle"),
    (_CAUSE_LABEL, "the cause"),
    (_RULED_LABEL, "the ruling"),
    (_MEASUREMENT_LABEL, "the measurement of record"),
)


@dataclass(frozen=True)
class SpentDeclaration:
    """One line of the reserved form, read for PRESENCE and never for truth.

    The family verifies that each element is present and non-empty, and verifies
    the superseding bundle MECHANICALLY. It does NOT and CANNOT verify that a
    cited ruling was really made, and that residue is disclosed rather than
    hidden: what makes the state safe is the successor guard, which cannot be
    satisfied by writing anything.
    """

    subject: str | None
    superseding: str | None
    cause: str | None
    author: str | None
    ruled_on: str | None
    measurement: str | None
    entry: str | None
    missing: tuple[str, ...]
    line: int

    def owed_elements_present(self) -> bool:
        return not self.missing


def _read_elements(line: str) -> tuple[dict[str, str], tuple[str, ...]]:
    """`({label: value}, missing element names)` for one candidate line."""
    found: dict[str, int] = {}
    pos = 0
    for label, _ in _LABELS:
        idx = line.find(label, pos)
        if idx < 0:
            continue
        found[label] = idx
        pos = idx + len(label)
    values: dict[str, str] = {}
    missing: list[str] = []
    labels = [label for label, _ in _LABELS]
    for index, (label, name) in enumerate(_LABELS):
        if label not in found:
            missing.append(name)
            continue
        start = found[label] + len(label)
        end = len(line)
        for later in labels[index + 1:]:
            if later in found:
                end = found[later]
                break
        value = line[start:end].strip()
        if not value:
            missing.append(name)
            continue
        values[label] = value
    return values, tuple(missing)


# COMMONMARK'S LINE ENDINGS, AND ONLY THOSE — a CARRIAGE RETURN, a LINE FEED,
# or the two together. `str.splitlines()` also breaks on U+2028, U+2029,
# U+0085, VT, FF and the information separators, and that difference is an
# ESCAPE rather than a nicety (Codex P1, round 4 on PR #589, and the same class
# as round 1's one layer down): ```` ```bad<U+2028>`info ```` is ONE line to
# CommonMark and an INVALID backtick opener, because its info string carries a
# backtick — but `splitlines()` hands the reader ```` ```bad ```` as a VALID
# opener and ```` `info ```` as its content. The reader is then one fence out of
# phase again: a `## Notes` boundary is swallowed as code, the next bare fence
# closes the fictitious block while opening a real one, and a declaration inside
# the real block is read under the earlier release entry. Measured: ACCEPTED,
# for all seven of the separators CommonMark does not recognize.
_LINE_ENDING = re.compile(r"\r\n|\r|\n")


def _lines(text: str) -> list[str]:
    """The document's lines, split on CommonMark's line endings and no others.

    A single trailing empty element is dropped so a document ending in a
    newline has the line count a reader would count, which is what the `line`
    field of a `SpentDeclaration` is compared against by a human repairing one.
    """
    out = _LINE_ENDING.split(text)
    if out and out[-1] == "":
        out.pop()
    return out


def _fence_opener(line: str) -> str | None:
    """The fence marker `line` OPENS, or None where it opens none.

    Two patterns rather than one, because the backtick form forbids a backtick
    in its info string and the tilde form does not.
    """
    backtick = _FENCE_OPEN_BACKTICK.match(line)
    if backtick is not None:
        return backtick.group(1)
    tilde = _FENCE_OPEN_TILDE.match(line)
    return tilde.group(1) if tilde is not None else None


def _html_opener(line: str, after_paragraph: bool) -> tuple[str, str] | None:
    """`(kind, tag)` for the CommonMark HTML block `line` opens, or None.

    `tag` is the kind-1 element name and is empty for every other kind, because
    kind 1 is the only one whose END CONDITION depends on which tag opened it.

    `after_paragraph` gates kind 7 alone, because kind 7 is the one CommonMark
    forbids from interrupting a paragraph — a line of prose that happens to end
    in a bare tag is prose.
    """
    one = _HTML_TYPE1_OPEN.match(line)
    if one is not None:
        return ("html1", one.group(1).lower())
    for kind, pattern in _HTML_OPENERS:
        if pattern.match(line):
            return (kind, "")
    if not after_paragraph and _HTML_TYPE7.match(line):
        return ("html7", "")
    return None


def _html_closed(kind: str, tag: str, line: str) -> bool:
    """Whether `line` satisfies the END CONDITION of an open HTML block.

    ASKED OF THE OPENING LINE TOO, which is round 6's finding from Codex and
    Copilot alike: a kind 1 to 5 block may open AND close on ONE line, and a
    reader that returns the new state without testing that line keeps the block
    open through everything after it. Measured on `<!-- first -->` … `## Notes`
    … `<!-- second -->` … declaration: the first comment stayed open THROUGH the
    real heading and used the SECOND comment as its delayed close, so the
    declaration kept the earlier entry and was ACCEPTED. Reproduced for all five
    of comment, declaration, processing instruction, CDATA and `<pre>`.
    """
    end = _HTML_CLOSERS.get(kind)
    if end is not None:
        return end.search(line) is not None
    # Kinds 6 and 7 end at the first BLANK line, which is not part of the block
    # — and which an opening line can never be, since it begins with `<`.
    return not line.strip()


def _opaque_state(line: str, state: tuple[str, str] | None,
                  after_paragraph: bool) -> tuple[str, str] | None:
    """`(kind, marker)` for the OPAQUE REGION open after `line`, or None.

    ONE STATE MACHINE FOR EVERY OPAQUE REGION, and that is the point rather
    than a tidiness: a fenced block and a raw HTML block are MUTUALLY
    EXCLUSIVE in CommonMark — a fence-shaped line inside an HTML block is HTML
    content, and an HTML-block opener inside a fence is code — so two machines
    running side by side would each be wrong about the other's region. Codex's
    round-5 P1 on PR #589 is exactly that: a ```-shaped line inside `<pre>`
    opened a FICTITIOUS fence, the reader went one fence out of phase, a
    `## Notes` boundary was swallowed, and a declaration inside the next real
    fence was read under the earlier release entry. Measured ACCEPTED for all
    EIGHT of the HTML-block kinds that can contain such a line.

    WHY THIS CLASS TERMINATES HERE, stated because three rounds of it have not.
    A phase error needs a line the reader calls a fence delimiter and
    CommonMark does not, at column 0 to 3. Every construct that can hold such a
    line is now accounted for: another fenced block (this machine's own state),
    a raw HTML block (these eight kinds), an indented code block (whose content
    is at column 4 or more, which the `^ {0,3}` in every pattern here
    excludes), and a block quote or list item (whose content carries its
    marker, so a bare fence at column 0 is a new block at document level, and a
    fence cannot be lazily continued). Nothing else remains — and the reverse
    error, MISSING a real fence at column 0 to 3, cannot happen either, because
    `_fence_opener` now rejects exactly what CommonMark rejects there.

    AND MATCHING COMMONMARK IS THE CRITERION, NOT MAXIMISING SUPPRESSION.
    Over-approximating an HTML block is an escape in its own right, in the same
    silent direction: a line of prose read as HTML content would swallow a real
    `## Notes` boundary and leave a declaration below it holding an entry it is
    not in. So kind 6 is CommonMark's tag list and nothing wider, kind 7 is a
    COMPLETE tag alone on its line and may not interrupt a paragraph, and
    `<not a tag` opens nothing.
    """
    if state is None:
        marker = _fence_opener(line)
        if marker is not None:
            return ("fence", marker)
        opened = _html_opener(line, after_paragraph)
        if opened is None:
            return None
        # THE OPENING LINE IS TESTED AGAINST ITS OWN END CONDITION, because a
        # kind 1 to 5 block may open and close on one line and a block left
        # open past its close swallows every boundary after it.
        return None if _html_closed(*opened, line) else opened
    kind, marker = state
    if kind == "fence":
        closer = _FENCE_CLOSE.match(line)
        if (closer is not None and closer.group(1)[0] == marker[0]
                and len(closer.group(1)) >= len(marker)):
            return None
        return state
    # Kinds 1 to 5 end on their own closing string, ANYWHERE on the line, and
    # that line is part of the block — so they span blank lines, which is what
    # makes `<pre>` able to hold a fence-shaped line at all. Kinds 6 and 7 end
    # at a blank line.
    return None if _html_closed(kind, marker, line) else state


def _paragraph_line(line: str, closes: bool, opaque: bool) -> bool:
    """Whether `line` IS PARAGRAPH CONTENT — the only thing a Setext underline
    may underline, and therefore the only state under which a run of `=` or `-`
    is a heading rather than a thematic break.

    ASKED OF WHAT THE LINE DID, NOT OF WHAT IT LOOKS LIKE, which is Codex's
    round-2 P1 on PR #589 and was a hole this reader's own round-1 fix opened.
    That fix excluded any line MATCHING the underline pattern, and in
    `## contract-v3.0` / `===` / `---` the `===` matches while ACTING as
    nothing: no paragraph precedes it, so CommonMark makes it paragraph TEXT and
    the `---` below it a real Setext H2. Excluding it by syntax lost that
    boundary and the entry stayed open — measured, and the declaration below was
    ACCEPTED. `closes` is therefore passed IN, from the same decision the caller
    already made, so an underline that really underlined is excluded and one
    that only looked like it is not.

    THE REMAINING EXCLUSIONS ARE DELIBERATELY FEW, AND THAT IS A JUDGMENT WITH
    A DIRECTION. Every form added here moves the reader toward UNDER-CLOSING,
    which is the escape direction this whole guard exists to close, so only what
    CommonMark is UNAMBIGUOUS about is excluded: blank lines, ATX headings at
    any level, fenced content, entry boundaries, and thematic breaks.
    CommonMark has other block starts — list items, block quotes, link
    reference definitions, HTML blocks, indented code — under which a following
    run of dashes is SOMETIMES not an underline and sometimes is (an indented
    line cannot interrupt a paragraph, so it is lazy continuation and the dashes
    below it genuinely ARE one). Those are NOT excluded, and the residue is
    disclosed rather than hidden: the failure mode there is a FALSE REFUSAL —
    one `error` beside the superseded `error`, quieting nothing, repaired by
    moving one line — where guessing wrong in the other direction is silence
    about the finding this family exists to raise. Full CommonMark block parsing
    is the honest fix and is out of this guard's scope.
    """
    if opaque or closes or not line.strip():
        return False
    return not (_ATX_ANY.match(line) or _THEMATIC_BREAK.match(line))


def _entry_boundary(line: str, after_paragraph: bool,
                    in_opaque: tuple[str, str] | None
                    ) -> tuple[bool, str | None]:
    """`(closes, opens)` for one line of the changelog.

    ONE STRUCTURAL FUNCTION FOR EVERY HEADING SHAPE, which is this hardening's
    whole shape. `closes` is whether the line ENDS the open entry; `opens` is
    the bundle whose entry it BEGINS, or None where it begins none. A line that
    closes and opens nothing leaves the reader inside NO entry, which is the
    state a containment refusal is made of — and the state seven measured
    escapes were each a way of never reaching.

    `after_paragraph` is whether the line ABOVE was paragraph content, which a
    Setext underline needs and no other shape does — a BOOLEAN and not the
    previous line's text, because the question is what that line ACTED as and
    the caller is the one that knows. `in_opaque` is the open OPAQUE REGION —
    a fenced block or a raw HTML block — or None; the function is TOTAL over
    that state rather than trusting its caller to have skipped opaque lines, so
    a second caller cannot reintroduce the escape by forgetting to.
    """
    if in_opaque is not None:
        # Inside a fenced block or a raw HTML block nothing is a heading — not
        # a line that looks exactly like one, and not one that names a bundle.
        return (False, None)
    if _ATX_BOUNDARY.match(line):
        heading = _ENTRY_HEADING.match(line)
        return (True, heading.group(1) if heading else None)
    if after_paragraph and _SETEXT_UNDERLINE.match(line):
        return (True, None)
    return (False, None)


def parse_spent_declarations(changelog: bytes | str | None
                             ) -> list[SpentDeclaration]:
    """Every line of `contracts/CHANGELOG.md` beginning with the reserved opener.

    ONE PURE FUNCTION FROM BYTES TO DECLARATIONS, taking bytes because
    `blobs_at` answers raw Git blob bytes — the release inventory's identity rule
    is computed over them, so the shared reader hands every caller bytes and
    naming text canonicalization an invalid digest source. Decoded with
    `replace` for the same reason `parse_bundle` is: a mis-encoded byte
    elsewhere in a 4000-line changelog must not turn a readable declaration into
    a crash.

    REJECTS RATHER THAN SKIPS. A line carrying the opener and completing nothing
    is returned WITH its `missing` list rather than dropped, because the opener
    is reserved and a malformed declaration is worse than none: it looks like a
    record.

    OPAQUE REGIONS ARE OPAQUE — fenced code blocks and raw HTML blocks alike —
    and the entry a declaration sits in is decided by `_entry_boundary` for
    every line. See the boundary block above for the rule and for the thirteen
    measured escapes it answers. An opaque region is one in which neither a
    heading nor a declaration exists, so the form can be DOCUMENTED there
    without being PERFORMED.
    """
    if not changelog:
        return []
    if isinstance(changelog, bytes):
        changelog = changelog.decode("utf-8", errors="replace")
    out: list[SpentDeclaration] = []
    entry: str | None = None
    opaque_state: tuple[str, str] | None = None
    after_paragraph = False
    for number, line in enumerate(_lines(changelog), start=1):
        # THE DELIMITERS BELONG TO THE BLOCK, not to the prose either side of
        # it: a line is opaque if a region was open BEFORE it or is open AFTER
        # it, which makes both the opener and the closer part of the region and
        # neither of them prose that could carry a record.
        opaque = opaque_state is not None
        closes, opens = _entry_boundary(line, after_paragraph, opaque_state)
        opaque_state = _opaque_state(line, opaque_state, after_paragraph)
        opaque = opaque or opaque_state is not None
        # CARRIED FORWARD FROM WHAT THIS LINE DID, not from what it looks like,
        # so a Setext underline that really underlined ends the paragraph and
        # one that only looked like an underline does not.
        after_paragraph = _paragraph_line(line, closes, opaque)
        if closes:
            entry = opens
            continue
        if opaque or not line.startswith(SPENT_OPENER):
            continue
        subject_match = _SUBJECT_PROBE.match(line)
        subject = subject_match.group(1) if subject_match else None
        values, missing = _read_elements(line)
        # THE GAP BETWEEN THE SUBJECT AND THE FIRST LABEL, checked so that junk
        # spliced into the middle of the form is a MALFORMED declaration rather
        # than an accepted one: the form admits exactly the separator there and
        # nothing else. Checked only where both halves were read, because
        # otherwise the missing half is the finding and this would be a second
        # name for it.
        if (subject_match and _SUPERSEDING_LABEL in values
                and not line[subject_match.end():].startswith(
                    _SUPERSEDING_LABEL)):
            missing = missing + ("the reserved form's own shape",)
        superseding = values.get(_SUPERSEDING_LABEL)
        if superseding is not None:
            # A code span, exactly as the subject is. Backticks around an empty
            # name read as the element being absent, which is what it is.
            superseding = superseding.strip("`").strip() or None
            if superseding is None:
                missing = missing + ("the superseding bundle",)
        author = ruled_on = None
        ruling = values.get(_RULED_LABEL)
        if ruling:
            parsed = _RULING_PROBE.match(ruling)
            if parsed:
                author = parsed.group("author").strip() or None
                ruled_on = parsed.group("ruled_on")
            if not (author and ruled_on):
                # THE RULING IS ONE ELEMENT WITH TWO HALVES, and a clause
                # carrying only one of them is named for the half it is MISSING
                # rather than for the element, because the repair for an absent
                # date is not the repair for an absent author. A clause carrying
                # BOTH halves and still not completing the form is named for
                # neither: what is missing there is the separator.
                date = _RULING_DATE.search(ruling)
                named = (ruling[:date.start()] if date else ruling)
                named = named.strip().rstrip(",").strip()
                missing = tuple(m for m in missing if m != "the ruling")
                if not named:
                    missing = missing + ("the ruling's author",)
                if not date:
                    missing = missing + ("the ruling's date",)
                if named and date:
                    missing = missing + ("the ruling's own shape",)
                author = ruled_on = None
        out.append(SpentDeclaration(
            subject=subject,
            superseding=superseding,
            cause=values.get(_CAUSE_LABEL),
            author=author,
            ruled_on=ruled_on,
            measurement=values.get(_MEASUREMENT_LABEL),
            entry=entry,
            missing=missing,
            line=number))
    return out


def version_of(bundle: str | None) -> tuple[int, int] | None:
    """`contract-v2.4` -> (2, 4). None for anything not of that shape, which is
    a bundle name this family cannot compare against the enforcement floor and
    therefore declines to judge."""
    if not bundle:
        return None
    found = _VERSION.match(bundle)
    return (int(found.group(1)), int(found.group(2))) if found else None


def _at_or_above_floor(bundle: str | None) -> bool:
    """Whether this family may report on `bundle` at all."""
    version = version_of(bundle)
    return version is not None and version >= ENFORCEMENT_FLOOR


def _below_floor(bundle: str | None) -> bool:
    """Whether `bundle` is a WELL-FORMED name below the enforcement floor.

    NOT THE NEGATION OF `_at_or_above_floor`, and the gap between them is
    exactly the distinction the orphan sweep turns on: a name of the wrong
    SHAPE is neither above the floor nor below it, because there is no version
    to compare. A declaration naming `contract-v1.3` is out of this family's
    scope; one naming `not-a-bundle` is a defect in the record.
    """
    version = version_of(bundle)
    return version is not None and version < ENFORCEMENT_FLOOR


def cut_bundles(git, repo_path: Path, tip: str) -> set[str] | None:
    """Every bundle this repository has CUT, from its release inventories.

    WHY NOT JUST THE DECLARED ONE — this is the defect Codex found on PR #544,
    and it is the exact recurrence the family exists for. A bundle is silent
    while its declaring commit is the tip, which is correct; then the NEXT cut
    advances the manifest, and a family that reads only the current declaration
    starts checking the new bundle and never revisits the old one. Run against
    the real incident it would have read ZERO through the whole of it: v2.3
    untagged, v2.4 declared on top, nothing reported.

    An inventory file under `contracts/releases/` is the machine-readable fact
    that a bundle was cut, which is what makes the set enumerable at all.
    """
    paths = git.ls_tree_paths(repo_path, tip, RELEASES)
    if paths is None:
        return None
    bundles = set()
    for path in paths:
        name = path.rsplit("/", 1)[-1]
        if name.endswith(".digests.yaml"):
            bundles.add(name[: -len(".digests.yaml")])
    return bundles


def _finding(sev, repo, rule, action, resolution="auto-fixable", path=MANIFEST):
    return Finding(sev, FAMILY, repo, path, rule, action,
                   resolution=resolution)


# --- the SPENT ladder --------------------------------------------------------
#
# ORDERED, AND EXACTLY ONE STATE PER DECLARATION. Each return below excludes
# every state under it, so one declaration yields at most one finding and a
# reader is never handed a choice between two true descriptions of one defect.
# The order is the requirement's own: what the line IS before what it SAYS
# (unreadable, orphan, duplicated, the live bundle), then whether it is well
# formed, then where it sits, then the successor guard's two halves.
def _declaration_state(decl: SpentDeclaration, count: int, cut: set[str],
                       declared: str) -> tuple[str, str] | None:
    """`(code, why)` for a declaration this family refuses, or None where it is
    well formed, correctly placed, and names a cut and STRICTLY LATER
    superseding bundle. None is NOT yet acceptance — publication of that
    successor is read afterwards, against the refs."""
    if decl.subject is None:
        return ("unreadable", "the line carries the reserved opener and no "
                              "readable subject, so it names no bundle at all")
    if decl.subject not in cut:
        return ("orphan-subject",
                f"this repository holds no release inventory for "
                f"{decl.subject}, so the declaration disposes nothing")
    if count > 1:
        return ("duplicate",
                f"{count} SPENT declarations name {decl.subject}, and two "
                f"records of one disposition is how they come to disagree")
    if decl.subject == declared:
        # BEFORE THE FORM CHECKS, because it is a fact about WHAT is claimed
        # rather than about HOW: a declaration of the number the manifest still
        # declares is refused whatever its shape, and that bundle goes on being
        # graded by distance exactly as it is today.
        return ("live-bundle",
                f"{decl.subject} is the bundle {MANIFEST} declares at the "
                f"published tip, and a repository declaring a bundle it also "
                f"calls spent asserts two incompatible things about one number")
    if decl.missing:
        return ("malformed",
                "the declaration is missing " + ", ".join(decl.missing))
    if decl.entry != decl.superseding:
        return ("wrong-entry",
                f"the declaration names {decl.superseding} as the superseding "
                f"bundle but sits inside "
                + (f"{decl.entry}'s changelog entry" if decl.entry
                   else "no bundle's changelog entry")
                + ", and the act that spends a number is the LATER CUT that "
                  "allocates its replacement")
    if decl.superseding not in cut:
        return ("successor-never-cut",
                f"this repository holds no release inventory for "
                f"{decl.superseding}, so the declaration retires a number by "
                f"pointing at one that was never cut")
    spent_version, next_version = version_of(decl.subject), version_of(
        decl.superseding)
    if (spent_version is None or next_version is None
            or next_version <= spent_version):
        return ("successor-not-later",
                f"{decl.superseding} is not STRICTLY LATER than {decl.subject}, "
                f"and a tag that already existed before {decl.subject} was cut "
                f"is not a replacement for it — a guard satisfied by an earlier "
                f"release has been walked around backwards rather than met")
    return None


_REFUSAL_SEVERITY = {
    "unreadable": ERROR,
    # A WARNING RATHER THAN AN ERROR, and the one finding of this state with no
    # per-bundle inventory to land on: a mistyped subject leaves the REAL bundle
    # undeclared and still reported at `error` by the scenarios above, which is
    # the fail-closed behaviour a typo must not be able to defeat.
    "orphan-subject": WARNING,
    "duplicate": ERROR,
    "live-bundle": ERROR,
    "malformed": ERROR,
    "wrong-entry": ERROR,
    "successor-never-cut": ERROR,
    "successor-not-later": ERROR,
}


def _refusal_findings(repo: str, decls: list[SpentDeclaration],
                      cut: set[str], declared: str
                      ) -> tuple[list[Finding], dict[str, SpentDeclaration]]:
    """`(findings, {subject: declaration})` for the declarations this run read.

    THE SECOND HALF IS A CANDIDATE SET AND NOT AN ACCEPTED ONE. A declaration
    that survives every check here has said everything it owes; whether the
    bundle it names is actually PUBLISHED is read from the refs afterwards,
    because that is the half nobody can satisfy by writing a sentence.

    THIS PASS RUNS OVER EVERY DECLARATION, whatever the tag state of its
    subject, because these are defects in the RECORD rather than in a bundle's
    publication — a declaration naming the live bundle is two incompatible
    claims about one number whether or not that number happens to be tagged.
    Acceptance, by contrast, reaches the ABSENT-tag arm and nothing else.
    """
    counts: dict[str | None, int] = {}
    for decl in decls:
        counts[decl.subject] = counts.get(decl.subject, 0) + 1
    findings: list[Finding] = []
    candidates: dict[str, SpentDeclaration] = {}
    reported_duplicate: set[str] = set()
    for decl in decls:
        if _below_floor(decl.subject):
            # A BELOW-FLOOR SUBJECT LEAVES THE WHOLE SWEEP, not one branch of
            # it — Codex's round-7 P2 on PR #589, and it was right that
            # exempting only the orphan arm was half a rule. The enforcement
            # floor says this family reports NOTHING about a bundle under
            # `contract-v1.7`; a declaration naming one therefore disposes
            # nothing whatever its shape, and every state below would be a
            # finding ABOUT A BUNDLE THIS FAMILY MAY NOT SPEAK OF — landing, at
            # that, on an inventory path for a bundle it does not grade.
            # Measured before the change: a legacy repository declaring
            # `contract-v1.6` and naming it spent emitted a `live-bundle`
            # error; malformed and wrong-entry below-floor declarations emitted
            # theirs.
            #
            # SUBJECTS OF THE WRONG SHAPE AND UNREADABLE SUBJECTS ARE NOT
            # EXCLUDED, which is the other half and the hole this exclusion
            # could open: `_below_floor` is false for both, so `not-a-bundle`
            # still raises the orphan warning and a line carrying the opener
            # and no subject at all is still `unreadable`. Neither is an
            # out-of-scope NAME; both are defects.
            continue
        state = _declaration_state(decl, counts[decl.subject], cut, declared)
        if state is None:
            candidates[decl.subject] = decl
            continue
        code, why = state
        if code == "duplicate":
            # ONE finding for the pair, not one per member: the defect is that
            # there are two, and they share a path and would share a rule.
            if decl.subject in reported_duplicate:
                continue
            reported_duplicate.add(decl.subject)
        if code == "unreadable":
            findings.append(_finding(
                _REFUSAL_SEVERITY[code], repo,
                f"a SPENT declaration in {CHANGELOG} (line {decl.line}) is "
                f"MALFORMED: {why} — a line carrying the reserved opener and "
                f"not completing the reserved form is a malformed declaration "
                f"rather than prose to be ignored, and a malformed declaration "
                f"is worse than none because it looks like a record",
                _SPENT_REFUSED_ACTION, path=CHANGELOG))
            continue
        if code == "orphan-subject":
            findings.append(_finding(
                _REFUSAL_SEVERITY[code], repo,
                f"a SPENT declaration in {CHANGELOG} (line {decl.line}) names "
                f"{decl.subject} as the bundle it spends, and {why} — a "
                f"mistyped subject leaves the real bundle undeclared and still "
                f"reported, which is the fail-closed behaviour a typo must not "
                f"defeat",
                _SPENT_ORPHAN_ACTION, path=CHANGELOG))
            continue
        findings.append(_finding(
            _REFUSAL_SEVERITY[code], repo,
            f"{decl.subject}'s SPENT declaration is REFUSED and accepts "
            f"nothing: {why}",
            _SPENT_REFUSED_ACTION, path=inventory_path(decl.subject)))
    return findings, candidates


def distance_from_tip(git, repo_path: Path, bundle: str, tip: str,
                      window: int) -> int | None:
    """First-parent landings on published `main` ABOVE the earliest commit in
    the window that declares `bundle`.

    Bounded on purpose, and the bound is `threshold + 2` for a reason worth
    stating: A LANDING DOES NOT TOUCH THE MANIFEST, so every commit above the
    cut still DECLARES the bundle, and the walk is looking for where the
    declaration STOPS rather than where it starts. A window of `threshold + 1`
    would saturate — "at the threshold" and "far past it" would both come back
    as the window's edge — and the error band would never be reached. With one
    commit of headroom the two are distinguishable, and where the whole window
    declares, the answer is a FLOOR (at least this far) which is all the error
    band needs, since it prints no number. An unbounded walk would read a
    manifest blob per commit over the whole history to answer a question with
    three outcomes.

    Returns None where the walk itself could not be performed, which the caller
    turns into a skip rather than a finding.
    """
    shas = git.first_parent_shas(repo_path, tip, window)
    if not shas:
        return None
    earliest_declaring = None
    for index, sha in enumerate(shas):
        blobs = git.blobs_at(repo_path, sha, [MANIFEST])
        if blobs is None:
            return None
        if parse_bundle(blobs.get(MANIFEST)) == bundle:
            earliest_declaring = index
        else:
            break
    if earliest_declaring is None:
        # The published tip does not declare it. The bundle is declared
        # somewhere this window does not reach, and grading it would be a guess.
        return None
    return earliest_declaring


def _tag_state(git, repo_path: Path, bundle: str):
    """(kind, detail) for one bundle's published tag.

    kind is "unlistable", "absent", "lightweight", "misplaced" or "ok".
    """
    ref = git.tag_ref(repo_path, bundle)
    if ref is None:
        return ("unlistable", None)
    objecttype, peeled = ref
    if objecttype is None:
        return ("absent", None)
    if objecttype != "tag":
        return ("lightweight", None)
    target = git.blobs_at(repo_path, peeled, [MANIFEST])
    if target is None or target.get(MANIFEST) is None:
        # Same conflation guarded at the other read: a tag peeling to a commit
        # this clone has not fetched must not be reported as a tag pointing at
        # a commit that declares nothing.
        return ("unlistable", None)
    declared_there = parse_bundle(target.get(MANIFEST))
    if declared_there == bundle:
        return ("ok", peeled)
    return ("misplaced", (peeled, declared_there))


def check_repo(repo: str, repo_path: Path, git,
               threshold: int = DEFAULT_THRESHOLD):
    """One repository. `Skip` where the question could not be asked, a list of
    findings otherwise — empty when the obligation is met.

    EVERY BUNDLE THIS REPOSITORY HAS CUT IS INSPECTED, not only the one the
    manifest currently declares. The distance grading applies to the CURRENT
    declaration, which is the only one still inside its legitimate window; a
    SUPERSEDED bundle's window closed when the next cut replaced it, so an
    untagged one is unambiguously unpublished and is reported at `error`
    without grading — UNLESS an accepted SPENT declaration names it, which is
    the third state and the only thing that quiets that arm.
    """
    tip = git.remote_main_sha(repo_path)
    if tip is None:
        return Skip(FAMILY, f"{repo}: published main could not be resolved, so "
                            f"no landing distance can be counted")
    blobs = git.blobs_at(repo_path, tip, [MANIFEST, CHANGELOG])
    if blobs is None:
        # BOTH MEMBERS OF THE BATCH, NAMED. `blobs_at` collapses to None only
        # when GIT ITSELF failed, which fails the whole two-member read — so a
        # message naming one document sends an operator to a file when neither
        # was obtained. The other return shape is per-path None, which each
        # guard below answers in its own words; conflating the two is the #338
        # class one layer down.
        return Skip(FAMILY, f"{repo}: version control could not be consulted "
                            f"for {MANIFEST} or {CHANGELOG} — the whole batch "
                            f"read failed, so NEITHER document was obtained")
    manifest = blobs.get(MANIFEST)
    if manifest is None:
        # NOT "no bundle declared". `blobs_at` answers None PER PATH for a blob
        # it cannot read, and the commonest cause is that the published tip is
        # not in the local object store — a clone that has not fetched it. This
        # is the #338 conflation, and this family repeated it once before this
        # line existed: it reported "no contract bundle declared" against a
        # repository declaring contract-v2.5, because main had advanced past the
        # last fetch. Not fetched is not an answer.
        return Skip(FAMILY, f"{repo}: {MANIFEST} could not be read at the "
                            f"published tip {tip[:9]} — the commit may not be "
                            f"present locally, which is not the same fact as "
                            f"declaring no bundle")
    declared = parse_bundle(manifest)
    if declared is None:
        return Skip(FAMILY, f"{repo}: no contract bundle declared")
    if version_of(declared) is None:
        return Skip(FAMILY, f"{repo}: declared bundle {declared!r} is not of "
                            f"the contract-v<major>.<minor> shape this family "
                            f"compares against the enforcement floor")

    cut = cut_bundles(git, repo_path, tip)
    if cut is None:
        return Skip(FAMILY, f"{repo}: the release inventories under "
                            f"{RELEASES}/ could not be listed, so the set of "
                            f"cut bundles is unknown")
    # EVERY BUNDLE THIS FAMILY MAY SPEAK ABOUT, computed once. The floor is
    # applied here rather than inside the loop so that the SPENT read below can
    # be gated on whether anything is in scope at all — which is the honest
    # condition, and the one that satisfies two findings at once.
    in_scope = sorted(bundle for bundle in cut | {declared}
                      if _at_or_above_floor(bundle))

    changelog = blobs.get(CHANGELOG)
    if changelog is None:
        # THE SAME #338 GUARD ONE DOCUMENT OVER, AND IT IS GATED ON
        # IN-SCOPE-NESS RATHER THAN ON POSITION. `blobs_at` answers None PER
        # PATH for a blob it cannot read, and the commonest cause is a checkout
        # that has not fetched the published tip; NOT FETCHED IS NOT AN ANSWER,
        # in either direction, because reading a declaration this run could not
        # LOOK FOR as an absent declaration turns an unfetched clone into an
        # `error` nobody can act on.
        #
        # BUT A REPOSITORY WITH NOTHING IN SCOPE IS NOT OWED THAT SKIP, and
        # standing above `parse_bundle` this guard fired before the bundle was
        # known — so a below-floor repository holding no `contracts/CHANGELOG.md`
        # at all, which this family had always answered with silence, became a
        # silent "not checked" instead. There is no bundle here whose state a
        # declaration could change, so the answer is the one it always was.
        if not in_scope:
            return []
        return Skip(FAMILY, f"{repo}: {CHANGELOG} could not be read at the "
                            f"published tip {tip[:9]}, so a SPENT declaration "
                            f"could not be looked for for "
                            f"{', '.join(in_scope)} — which is not the same "
                            f"fact as there being none")
    declarations = parse_spent_declarations(changelog)
    findings, candidates = _refusal_findings(repo, declarations, cut, declared)
    for bundle in in_scope:
        kind, detail = _tag_state(git, repo_path, bundle)
        if kind == "unlistable":
            return Skip(FAMILY, f"{repo}: the published refs for {bundle} "
                                f"could not be consulted")
        if kind == "ok":
            continue
        if kind == "lightweight":
            findings.append(_finding(
                ERROR, repo,
                f"the ref named {bundle} is a LIGHTWEIGHT tag, not an "
                f"annotated one, so it does not satisfy the policy's "
                f"requirement",
                _LIGHTWEIGHT_ACTION))
            continue
        if kind == "misplaced":
            peeled, declared_there = detail
            findings.append(_finding(
                ERROR, repo,
                f"{bundle}'s annotated tag is MISPLACED: it peels to "
                f"{peeled[:9]}, which declares "
                + (f"{declared_there}" if declared_there else "no bundle at all")
                + f", not {bundle} — a tag on the wrong commit satisfies every "
                  f"check that asks only whether a tag exists, and it is what "
                  f"consumers pin",
                _MISPLACED_ACTION, resolution="contested"))
            continue

        # absent — AND THE ONLY ARM THE SPENT STATE REACHES. It does not quiet a
        # MISPLACED tag, does not quiet a LIGHTWEIGHT ref, and does not quiet the
        # distance grading of the bundle the manifest currently declares: the
        # branches above have already `continue`d past this point, so the scope
        # rule holds BY CONSTRUCTION rather than by care.
        if bundle != declared:
            decl = candidates.get(bundle)
            if decl is not None:
                kind, _ = _tag_state(git, repo_path, decl.superseding)
                if kind == "unlistable":
                    return Skip(FAMILY,
                                f"{repo}: the published refs for "
                                f"{decl.superseding}, named as {bundle}'s "
                                f"superseding bundle, could not be consulted")
                if kind == "ok":
                    # ACCEPTED. Recorded, never silent — ruled by Brett Heap on
                    # 2026-09-02 on an alternative put to him and declined —
                    # and `contested`, so a spent state that stops being
                    # reported without a cited change is re-raised.
                    findings.append(_finding(
                        INFO, repo,
                        f"{bundle} is declared SPENT: it was cut, has no "
                        f"published annotated tag, and {decl.superseding} — "
                        f"itself cut, itself published and strictly later — "
                        f"superseded it. The record is {CHANGELOG} § "
                        f"{decl.superseding} — RULED BY "
                        f"{decl.author}, {decl.ruled_on}; MEASUREMENT: "
                        f"{decl.measurement}. The tag obligation was not met, "
                        f"it was EXTINGUISHED by an owner act at the cost of a "
                        f"version number",
                        _SPENT_ACCEPTED_ACTION, resolution="contested",
                        path=inventory_path(bundle)))
                    continue
                # PROVISIONAL, not refused: ONE finding and not two. The
                # superseded `error` is SUPPRESSED in favour of this `warning`,
                # which is the ruled outcome for this case, and nothing is lost
                # by the suppression — the successor is the bundle the manifest
                # now declares, so the distance arm grades it on its own
                # account and the obligation has MOVED rather than gone.
                findings.append(_finding(
                    WARNING, repo,
                    f"{bundle} is declared SPENT and the supersession is "
                    f"UNPROVEN: {decl.superseding} has a release inventory and "
                    f"no published annotated tag peeling to a commit that "
                    f"declares it — a bundle is not published until its tag "
                    f"exists, and a successor that is not published cannot yet "
                    f"be shown to have carried anything forward",
                    _SPENT_UNPROVEN_ACTION, path=inventory_path(bundle)))
                continue
            findings.append(_finding(
                ERROR, repo,
                f"{bundle} was cut and SUPERSEDED without ever being "
                f"published: it has a release inventory, the manifest has "
                f"moved on to {declared}, and it has no published annotated "
                f"tag — under the versioning policy it was never released, "
                f"and its window closed when the next cut replaced it",
                _SUPERSEDED_ACTION))
            continue
        distance = distance_from_tip(git, repo_path, bundle, tip, threshold + 2)
        if distance is None:
            return Skip(FAMILY, f"{repo}: the earliest commit declaring "
                                f"{bundle} could not be resolved")
        if distance == 0:
            continue
        if distance <= threshold:
            findings.append(_finding(
                WARNING, repo,
                f"{bundle} is declared and has no published annotated tag, "
                f"{distance} first-parent landing(s) after the commit that "
                f"declared it",
                _ABSENT_ACTION))
        else:
            findings.append(_finding(
                ERROR, repo,
                f"{bundle} is declared and has no published annotated tag "
                f"more than {threshold} first-parent landings after the "
                f"commit that declared it — under the versioning policy it is "
                f"NOT PUBLISHED, and its presence in the manifest is not a "
                f"release",
                _ABSENT_ACTION))
    return findings


def fam_release_tag_publication(ctx):
    """Every repository in scope that declares a contract bundle.

    A PER-REPOSITORY SKIP IS REPORTED, NOT DROPPED, for the reason
    `release-inventory-drift` records for the same shape: the ratified
    obligation is per-repository, most pinned repositories declare no bundle at
    all, and a design that only spoke up when EVERY repository skipped would be
    silent about nearly all of them on every run — which is the "silently
    omitted" the requirement forbids. Each skip contributes an `info`, and the
    family-level `Skip` is kept for the case it genuinely describes: nothing in
    scope was askable at all.
    """
    results: list[Finding] = []
    skips: list[str] = []
    scoped = sorted(ctx.repo_paths.items())
    if not scoped:
        return Skip(FAMILY, "no repository in scope")
    threshold = getattr(ctx, "tag_publication_threshold", DEFAULT_THRESHOLD)
    for repo, repo_path in scoped:
        outcome = check_repo(repo, Path(repo_path), ctx.git, threshold)
        if isinstance(outcome, Skip):
            skips.append(outcome.reason)
            results.append(_finding(
                INFO, repo, f"not checked: {outcome.reason}",
                "no action — this repository's tag obligation was not "
                "evaluated, and the reason is recorded rather than omitted",
                resolution="auto-fixable"))
            continue
        results.extend(outcome)
    if len(skips) == len(scoped):
        return Skip(FAMILY, "; ".join(skips))
    return results
