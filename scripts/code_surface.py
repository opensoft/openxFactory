"""The house reader and judge for the `code_surface:` realization-axis
declaration (release-realization / gate-code-surface-declarations).

WHY THIS MODULE EXISTS. `release-realization`'s promoted requirement
*Realization axis declaration* is one sentence with two halves —
`code_surface:` and `target_release:`. The sibling packet
`gate-realization-axis-vocabulary` gated the SECOND half and ruled in its own
ratified `tasks.md` § 6.3 that it was NOT gating the first. This module is that
first half, gated: measured at the packet's drafting, the only machine reader of
the `code_surface:` value in this repository was
`scope_globs.code_surface_repositories`, which split the WHOLE declaration —
prose gloss included — on `[\\s,()/]+` and returned every word that was not
`none`, yielding 3,421 distinct "repository" tokens across 45 active
declarations and a NON-EMPTY repository set for 3 of the 4 changes that declared
the EMPTY surface. A declaration whose repositories cannot be told from its
explanation is a declaration no reader can act on.

THE DECLARATION IS A DECLARED HEAD FOLLOWED BY AN OPTIONAL PROSE GLOSS, and
that is the corpus's own form rather than a rule invented here: measured over
the 45 active declarations at the packet's drafting, 38 already opened with a
repository identifier (or with `none`) and handed off to a gloss through an
opening parenthesis (19), an em dash (17) or a full stop (2). So this module
judges the HEAD and never the gloss. The opener set is widened only by the
three the archive and the house style also write — an en dash, a colon, a
semicolon — so the gate cannot refuse a form the estate's own corpus uses.

THE GATE JUDGES A REPOSITORY IDENTIFIER'S SHAPE AND NEVER ITS MEMBERSHIP, and
that is a finding rather than a shortcut. Searched before the design: this
repository defines NO inventory of the estate's repositories to resolve
against — `contracts/policies/repository-identity.yaml` is a former-to-current
TRANSFER map carrying one row, `contracts/hermes-runtime/fixtures/
domain-regression-inventory.yaml` is a five-row domain-factory FIXTURE that
does not name `openxFactory` itself, and `contracts/*-pin.yaml` carries one
`source_repository:` each. A gate that resolved membership against a place that
does not exist would refuse every non-`none` declaration on the day it landed.
The stated cost is that a plausible misspelling passes; the successor that
would lift it is named in the packet's `tasks.md` § 6.1.

`none` IS THE EMPTY-SURFACE SENTINEL AND IS RESERVED OUT OF REPOSITORY
IDENTIFIER. A head is EITHER the single token `none` and nothing else, OR a
list in which that token appears nowhere. The exclusivity is enforced rather
than left to a reader's good sense because the two readings differ by an
AUTHORIZATION: `none` matches the repository-name shape like any other
lowercase word, so a grammar that merely `or`-ed the two alternatives would
read `none, openxFactory` as a two-member list and derive a NON-EMPTY set for a
change whose declaration says the surface is empty. The refusal is a refusal
rather than a precedence rule, because both precedence rules silently discard
something an author wrote.

ABSENCE IS LAWFUL AND IS NOT A FINDING. The promoted sentence makes a proposal
without the declarations a doc-only change (`code_surface: none`,
`target_release: implemented`) BY DEFAULT, so a proposal that declares nothing
declares the default and passes. Only a PRESENT declaration is judged — and a
declaration present with no value is REFUSED, because the author wrote the key
and the default was available by omitting it.

ARCHIVED PROPOSALS ARE READ AND NEVER JUDGED. An archived packet's front matter
is frozen record — `record-immutability` and `govern-archived-record-edits` put
it beyond a plain fix — so the scan counts what the archive carries and reports
it, and refuses nothing there. A gate that demanded an edit nobody may make
would be a standing finding with no remedy.

THE DECLARATION IS READ THROUGH THE HOUSE STRICT LOADER
(`frontmatter_strict.read_front_matter`) rather than through a private scan, so
this gate and the loader refuse the same documents and no proposal can mean one
thing to one reader and another to the next. `code_surface:` is a PROSE HEADER
of the realization-axis block and not one of its STRUCTURED fields, so this
module neither realizes nor contradicts `add-sequenced-after-substrate`'s ADDED
requirement *Strict loading of the realization-axis front-matter block*: it adds
no structured field and asks for no new strictness, and it CONSUMES that
loader's refusals — a document the loader refuses is reported here as a finding
against that document rather than crashing the run.

A REPEATED DECLARATION IS REFUSED RATHER THAN HALF-READ. `code_surface:` is a
PROSE header, so the shared loader JOINS a repeat into one raw string instead of
refusing it as the duplicate key a STRUCTURED field's repeat would be. A block
declaring one repository and then another would show a reviewer two declarations
and authorize the first — so `declaration` refuses the repeat by name, on the
value the loader returned, without writing a second front-matter parser.

THE CLOSED REGISTER IS A RATCHET, NOT AN AMNESTY, and it SUPPLIES NO REPOSITORY
SET. See `scripts/code-surface-register.yaml`'s own header for the measurement
that forced it and for the asymmetry it borrows from the sibling and from
`contracts/openspec-cli-pin.yaml` `dispositions:`: an UNREADABLE DECLARATION
THE REGISTER DOES NOT NAME FAILS, and an ENTRY THAT MATCHES NOTHING REFUSES. An
entry suspends the grammar's refusal for ONE declaration and does nothing else —
the head it tolerates is a head no reader can parse, so there is no set to
supply, and a consumer that needs one FAILS CLOSED on that proposal
(`scope_globs.code_surface_repositories`, and the requirement *The declared
repository set is derived from the head and never from the gloss*).

NOTHING AUTHOR-CONTROLLED BECOMES A PATH BEFORE IT IS SHAPE-CHECKED. A register
entry's `change:` must match `CHANGE_ID_RE` before `load_register` returns it,
because every consumer resolves that name under `openspec/changes/`; and no
path this module opens is reached through a symlink, at the leaf or at any
ancestor (`load_register`, `_has_symlinked_ancestor`, `_unescaped`).

Deterministic: text/YAML reads only, no model calls, no writes, no network.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - pyyaml is a suite dependency
    yaml = None

import frontmatter_strict as fm

#: The declaration this module reads.
FIELD = "code_surface"

#: The EMPTY-SURFACE SENTINEL, and the one token that is never a repository.
#:
#: MATCHED EXACTLY, case and all. The promoted sentence spells it `none`, the
#: four carriers measured at the packet's drafting all spell it `none`, and a
#: case-insensitive sentinel would quietly read `None` — a perfectly ordinary
#: word to start a sentence with — as the empty surface. A head that opens
#: `None of this repository's …` is prose running into the declaration and is
#: refused as such, by the opener rule, which is the finding its author needs.
NONE = "none"

#: The register, beside the validator that reads it.
REGISTER_PATH = Path(__file__).resolve().parent / "code-surface-register.yaml"

CHANGES_DIR = Path("openspec") / "changes"

#: A REPOSITORY NAME'S SHAPE, restated from the ratified grammar
#: (`design.md` D1, `name := [A-Za-z][A-Za-z0-9._-]*[A-Za-z0-9]`) rather than
#: widened here: a letter, then name characters, ending on a letter or a digit.
#: It admits every spelling the corpus carries (`openxFactory`, `xFactory`,
#: `hermes-install`, `OpenXPKI-Install`) and stops before the punctuation that
#: opens a gloss, which is what makes the opener rule do the work.
_NAME = r"[A-Za-z][A-Za-z0-9._-]*[A-Za-z0-9]"

#: A REPOSITORY IDENTIFIER IS EITHER A BARE NAME OR AN `<owner>/<name>`
#: ADDRESS, and BOTH ARE ADMITTED because the corpus carries both
#: (`openxFactory`, `opensoft/LedgerxWallet`). Exactly one owner segment: a
#: two-slash path is not an address this estate writes, and admitting one would
#: make a URL fragment parse as a repository.
REPOSITORY_RE = re.compile(rf"{_NAME}(?:/{_NAME})?")

#: THE LIST SEPARATORS, EXACTLY THE THREE THE GRAMMAR ADMITS — a comma, ` and `,
#: ` + ` — plus the `, and ` the corpus writes when it spells a list out. Tried
#: in this order so `, and ` is consumed whole rather than as a bare comma
#: followed by a head that opens with the word `and`.
_SEPARATOR_RE = re.compile(
    r",[ \t\n]+and[ \t\n]+"      # ", and "
    r"|,[ \t\n]*"                # ","  (with or without a following space)
    r"|[ \t\n]+and[ \t\n]+"      # " and "
    r"|[ \t\n]+\+[ \t\n]+"       # " + "
)

#: THE GLOSS OPENERS — THE SET THE CORPUS ALREADY USES, NOT THE SET A GATE
#: WOULD PREFER. An em dash, an en dash or an opening parenthesis, each
#: introduced by whitespace; or a full stop, a colon or a semicolon, each
#: followed by whitespace or by the end of the declaration. The whitespace side
#: of each is what separates an opener from a character INSIDE an identifier:
#: `openxFactory.io` is one name, `openxFactory. The surface …` is a head and a
#: gloss.
_GLOSS_OPENER_RE = re.compile(r"[ \t\n]+[—–(]|[.:;](?:[ \t\n]|$)")

#: THE YAML FOLDING INDICATORS, REFUSED BY NAME. `code_surface:` is a PROSE
#: HEADER that no YAML loader reads, so an author who writes `code_surface: >-`
#: to fold a long declaration gets those two characters back as the first thing
#: in the value, where a repository name belongs — and nothing tells them. The
#: corpus carried one such declaration at the packet's drafting. The refusal
#: says what it is rather than merely reporting an unreadable head, because the
#: author was reaching for a structure this field does not have.
_BLOCK_SCALAR_RE = re.compile(r"^[>|][+-]?(?:[0-9][+-]?)?(?:[ \t\n]|$)")

#: A register entry's `change:` IS A DIRECTORY NAME AND NEVER A PATH. It is
#: resolved under `openspec/changes/` by every consumer of the register, so —
#: the sibling's rule, restated — it is shape-checked where the register is
#: loaded rather than at each use: one segment, no separator, no leading dot, so
#: neither `..` nor `a/b` can be written into the register and reach a path.
CHANGE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

#: A SECOND `code_surface:` HEADER INSIDE THE ONE THIS READER WAS HANDED.
#: The shared loader JOINS a repeated prose header into one raw string rather
#: than refusing it as the duplicate key a STRUCTURED field's repeat would be,
#: so a block declaring one repository and then another comes back as
#: `'openxFactory\ncode_surface: openXwallet'`. Parsing that judges the FIRST
#: declaration and silently ignores the rest, which is the
#: show-one-authorize-another defect the strict loader exists to close.
#:
#: ANCHORED AT COLUMN 0, WHICH IS THE LOADER'S OWN NOTION OF A HEADER LINE
#: (`frontmatter_strict._TOP_LEVEL`). An INDENTED line is a CONTINUATION of the
#: gloss, not a declaration, so a gloss line that happened to read
#: `  code_surface: is what this field is called` must pass — the requirement
#: says judge the head and NEVER the gloss.
_REPEATED_HEADER_RE = re.compile(rf"(?m)^{FIELD}[ \t]*:")

#: THE CLOSED CLASS SET — the four classes the divergence was measured in
#: (`design.md` D0). The register is CLOSED and a new admission is a change to
#: the SPECIFICATION rather than an edit to a data file, so the classes a
#: divergence may be filed under are enumerated here, beside the loader that
#: enforces them, rather than only in a test over the live register: a
#: constraint the requirement states and no loader checks is a constraint a
#: consuming tree does not have.
REGISTER_CLASSES = (
    "block-scalar",
    "possessive",
    "apposition",
    "list-runs-into-prose",
)

#: EVERY KEY A REGISTER ENTRY SHALL CARRY, AND THE SHAPE IT SHALL CARRY IT IN.
#: The ADDED requirement *Standing code-surface divergence is named in a closed
#: register* has each entry carry "its declaration text as it stands, the class
#: of divergence, the reason, a citation, and the event that retires the entry"
#: — five things — so all five are enforced at the LOAD and not merely asserted
#: by a test over the register this repository happens to carry. `cited_to` is
#: the one that is a LIST: a divergence can stand on more than one written
#: reason, and an entry with no citation would tolerate an unreadable
#: declaration on nobody's word, which is the failure the register exists to
#: prevent.
_REQUIRED_ENTRY_KEYS = {
    "change": "text",
    "declaration": "text",
    "class": "text",
    "why": "text",
    "cited_to": "list",
    "retires_when": "text",
}


def declaration_digest(text: str) -> str:
    """The SHA-256 of a declaration's exact UTF-8 bytes, as the closed baseline
    records it.

    WHY THE BASELINE IS A DIGEST AND NOT THE TEXT. The sibling's baseline pairs
    a change with its VALUE TOKEN, which is one word. A `code_surface:`
    declaration is not one word: the widest of the seven standing divergences
    runs to hundreds of bytes and one of them is MULTI-LINE, so a baseline
    carrying the text verbatim would be a wall nobody could review — and a
    baseline carrying a PREFIX of it would pin an arbitrary number of
    characters and tolerate an edit past that point. The digest is exact at any
    length: an entry the register did not carry at this gate's landing, or an
    entry whose declaration text is edited by a byte, does not match and is
    REFUSED. The act stays legible because the register carries the declaration
    VERBATIM in the same pull request's diff, beside the change id this baseline
    names.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


#: THE REGISTER'S CLOSED BASELINE — the `(change, declaration-digest)` pairs the
#: register carries at this gate's landing, and the whole of what it may ever
#: carry.
#:
#: WHY A BASELINE AND NOT A COUNT OR AN HONOUR SYSTEM. The requirement makes the
#: register CLOSED — removable, never addable — and the register file says so in
#: its own header, but a rule stated in two prose headers and checked by nobody
#: is the defect this whole packet is about. The sibling's own bench found
#: exactly this hole in the sibling's own register. Without this, a later pull
#: request could append an entry and make any unreadable declaration pass with
#: the gate green, which is the ratchet failing silently in the one direction
#: that matters. An entry the baseline does not carry is REFUSED, so admitting
#: one takes a second, deliberate, reviewable edit HERE, in the module, beside
#: the reason.
#:
#: A BASELINE MAY BE A STRICT SUPERSET, AND USUALLY WILL BE: removal is lawful
#: (a corrected declaration or an archived packet retires its entry, and
#: `Report.stale` REFUSES until the entry is deleted), so a pair stays here
#: after its entry goes. This is a ceiling, never a floor.
#:
#: IT BINDS THE HOUSE REGISTER ONLY. `--register PATH` exists so the tests can
#: put a known register in front of a known tree and so a consuming tree can
#: name its own; those registers are not this one and are not measured by this
#: baseline. `load_register` applies it when, and only when, it is reading the
#: register this repository carries.
#:
#: THE POPULATION IS A FACT ABOUT A TREE AND WAS RE-MEASURED AT THE HEAD THIS
#: GATE LANDS ON, never carried from the tree the packet was drafted against
#: (the requirement's own scenario *The corpus moves between drafting and
#: landing*). Seven at drafting (`origin/main` `bcde1575`); re-measured here.
CLOSED_REGISTER = (
    # class: block-scalar
    ("adopt-configured-notebook-hosting-identity",
     "e0e129ab4b32ad67b11e09be78c179eae0a1d397b47d16f39de54b216c9e50c6"),
    # class: possessive
    ("amend-kill-switch-to-declared-test-companion",
     "ef4fe232c960862b095bca0bac4672bd372cf7124c126b221679bca59cbc4aea"),
    # class: apposition
    ("add-substantive-review-lane",
     "d9f97ae474a88645db1c0c23adcedb9b92c13329bfff86ad466892b16cd2a4a3"),
    # class: list-runs-into-prose
    ("admit-review-lane-repin-to-merge-approval-envelope",
     "a9b74cf9abea4736646c6dd63cc14a2c431cac4bd7d3f263d069b40845791a49"),
    ("amend-mirror-floor-regeneration-merge-authority",
     "05a7603ca57cd4c83ddf66b2068c94891634f9c49efbefd818771a1247af4ae6"),
    ("extend-merge-master-envelope-to-floor-bot-lanes",
     "2854d3889fb1cb79e8f1cabaf64c7287a2b073e72130f5098a81e946bea825e8"),
    ("split-opendox-two-layer-product",
     "60f4e11d53e6d0772ff642280fcf626dafcabebafa0c7c4e537d8eae8a54d058"),
)


class CodeSurfaceError(Exception):
    """A refusal this module raises: a declaration whose head the grammar
    cannot read, a proposal that cannot be read at all, or a register that
    cannot be used. Carries the message naming what was refused."""


@dataclass(frozen=True)
class Head:
    """A DECLARED HEAD the grammar admits.

    `repositories` is the head's identifiers in the order they were declared,
    and is EMPTY for the `none` head — an empty set the head DECLARES, which is
    a different fact from the ABSENCE of a head-derived set (a declaration the
    register carries, which has no `Head` at all).
    """
    repositories: tuple[str, ...]
    is_none: bool


@dataclass(frozen=True)
class Finding:
    """One active declaration whose head the grammar does not admit."""
    change: str
    path: str
    declaration: str
    detail: str


@dataclass(frozen=True)
class Report:
    """The whole-corpus result. Counts are facts about the tree, not estimates."""
    active_total: int
    active_declaring: int
    inside_none: int
    inside_repositories: int
    registered: tuple[tuple[str, str], ...]
    findings: tuple[Finding, ...]
    stale: tuple[str, ...]
    archived_total: int
    archived_declaring: int
    archived_off_grammar: int


def _excerpt(text: str, limit: int = 120) -> str:
    """The declaration as a finding quotes it: one line, bounded.

    A finding names "the text the declaration carries" (the requirement's own
    words), and some of these declarations run to hundreds of bytes across
    several lines. An unbounded echo would bury the finding in the gloss it is
    refusing to judge.
    """
    flat = " ".join(text.split())
    return flat if len(flat) <= limit else flat[:limit - 1] + "…"


def parse_head(raw: object) -> Head:
    """The DECLARED HEAD of one declaration, or a refusal naming the defect.

    THE HEAD IS JUDGED AND THE GLOSS NEVER IS. The head is read left to right
    as `none`, or as repository identifiers separated by a comma, by ` and ` or
    by ` + `; what follows it must be a GLOSS OPENER or the end of the
    declaration. A head that runs into ordinary prose with no opener — a
    possessive, an apposition, or a sentence continued by `, and …` — is
    REFUSED, because there is then no point in the string at which the
    declaration stops and the explanation starts, and every reader must guess a
    different one.

    Raises `CodeSurfaceError` for every head the grammar does not admit.
    """
    text = raw if isinstance(raw, str) else "" if raw is None else str(raw)
    if not text.strip():
        raise CodeSurfaceError(
            f"declares `{FIELD}:` with no value. The promoted doc-only default "
            f"(`{FIELD}: none`) is available by OMITTING the key, so a key "
            "written with nothing after it is a declaration the author began "
            "and did not make")
    if _BLOCK_SCALAR_RE.match(text):
        indicator = text.split()[0] if text.split() else text[:2]
        raise CodeSurfaceError(
            f"opens with the YAML folding indicator `{indicator}`. "
            f"`{FIELD}:` is a PROSE HEADER that no YAML loader reads, so the "
            "indicator is not consumed as YAML syntax — it survives into the "
            "value and becomes the first thing a reader sees where a "
            "repository name belongs. Write the declaration on the key's own "
            "line, with the explanation after a gloss opener")

    names: list[str] = []
    position = 0
    length = len(text)
    while True:
        match = REPOSITORY_RE.match(text, position)
        if match is None:
            raise CodeSurfaceError(
                f"carries no repository identifier at `{_excerpt(text[position:], 60)}`"
                f" — a head is either the single token `{NONE}` or a list of "
                "repository identifiers (a bare name, or an `<owner>/<name>` "
                f"address). Declaration: `{_excerpt(text)}`")
        names.append(match.group(0))
        position = match.end()
        if position >= length:
            break
        opener = _GLOSS_OPENER_RE.match(text, position)
        if opener is not None:
            break
        separator = _SEPARATOR_RE.match(text, position)
        if separator is None:
            raise CodeSurfaceError(
                f"its head runs into prose at `{_excerpt(text[position:], 60)}` "
                "with no gloss opener between them. A declaration is a HEAD "
                "then, optionally, a GLOSS introduced by an em dash, an en "
                "dash, an opening parenthesis, a full stop, a colon or a "
                "semicolon — so a possessive, an apposition or a sentence "
                "continued by `, and …` leaves no point at which the "
                "declaration stops and the explanation starts. "
                f"Declaration: `{_excerpt(text)}`")
        position = separator.end()
        if position >= length:
            raise CodeSurfaceError(
                "ends on a list separator with no repository identifier after "
                f"it. Declaration: `{_excerpt(text)}`")

    if NONE in names:
        if len(names) == 1:
            return Head(repositories=(), is_none=True)
        raise CodeSurfaceError(
            f"mixes the empty-surface sentinel `{NONE}` with "
            f"{len(names) - 1} repository identifier(s) "
            f"({', '.join(n for n in names if n != NONE)}). A head is EITHER "
            f"the single token `{NONE}` OR a list in which that token appears "
            "nowhere: parsed as a list, this head derives a NON-EMPTY "
            "repository set for a change whose declaration says the surface is "
            "empty. A head that declares the empty surface beside a named one "
            "is self-contradictory rather than wide, and the correction is the "
            f"author's. Declaration: `{_excerpt(text)}`")
    return Head(repositories=tuple(names), is_none=False)


def declaration(proposal: Path) -> tuple[bool, str | None]:
    """`(present, raw declaration text)` for one proposal.

    Raises `CodeSurfaceError` when the document cannot be read at all — a
    strict-loader refusal, bytes that are not UTF-8, or a block that declares
    the field twice. Reported by the caller as a finding against the file,
    never as a traceback.
    """
    try:
        front = fm.read_front_matter(proposal)
    except fm.StrictFrontMatterError as exc:
        raise CodeSurfaceError(str(exc)) from exc
    except OSError as exc:
        raise CodeSurfaceError(f"cannot be read: {exc}") from exc
    if FIELD not in front:
        return False, None
    raw = front[FIELD]
    text = raw if isinstance(raw, str) else str(raw)
    if _REPEATED_HEADER_RE.search(text):
        raise CodeSurfaceError(
            f"declares `{FIELD}:` more than once in one front-matter block. "
            "The block is prose headers, so the shared loader JOINS the "
            "repeats into one value instead of refusing them as the duplicate "
            "key a structured field's repeat would be, and a reader that "
            "parsed the join would judge the FIRST head and silently ignore "
            "the second declaration. Declare it once")
    return True, text


def _has_symlinked_ancestor(path: Path) -> bool:
    """Whether any directory between `path` and its own top is a symlink.

    `path.is_symlink()` answers only for the LEAF. `linkdir/register.yaml`,
    where `linkdir` is a symlink to an external directory, has an entirely
    ORDINARY leaf — `register.yaml` itself is a regular file — so the leaf
    check alone passes it, and `read_text()` still follows `linkdir` and reads
    bytes from wherever it points, silently and differently per runner.

    THE WALK IS UNANCHORED, AND THAT IS THE SIBLING'S EXACT SHAPE
    (`target_release._has_symlinked_ancestor`) RATHER THAN AN APPROXIMATION OF
    IT: a register named on `--register` is deliberately allowed to live
    wherever a test tree or a consuming repository puts it, so there is no
    `REPO_ROOT` to check "outside of" the way `_unescaped` checks outside one.
    The walk therefore climbs `path`'s OWN ancestors one directory at a time —
    stopping at `/` for an absolute path, or at `.` for a relative one, so a
    caller's working directory is no more implicated than `_unescaped`
    implicates `repo_root`'s own approach to it.
    """
    current = path.parent
    while True:
        if current.is_symlink():
            return True
        parent = current.parent
        if parent == current:
            return False
        current = parent


def load_register(path: Path = REGISTER_PATH,
                  closed: tuple[tuple[str, str], ...] | None = None
                  ) -> list[dict]:
    """The register entries, shape-checked, and measured against the CLOSED
    baseline where one applies.

    A register that cannot be used REFUSES rather than being ignored: ignoring
    a malformed exception file would silently re-fail every declaration it
    covers, or silently admit one it does not.

    `closed` is the baseline of `(change, declaration-digest)` pairs the
    register may carry. Passing it binds ANY register; passing None binds the
    HOUSE register — the one beside this module — to `CLOSED_REGISTER` and
    leaves a register named on the command line unbaselined, because such a
    register belongs to a test tree or a consuming repository and its closure is
    that repository's own record to keep.

    NO PATH IS REACHED THROUGH A SYMLINK, AT THE LEAF OR AT ANY ANCESTOR, and
    the check runs UNCONDITIONALLY before `is_file()` or `read_text()` — so it
    is the same guard whether `path` is the default argument or one a caller
    supplies, and no branch can forget one of them. `Path.is_file()` and
    `Path.read_text()` BOTH follow symlinks, so without this a committed link
    here would make the gate consume exception data from OUTSIDE the checkout,
    silently and differently per runner. This is
    `target_release.load_register`'s guard mirrored exactly rather than
    approximated: a guard that is NEARLY the sibling's is a guard whose gaps
    nobody has measured.
    """
    if yaml is None:  # pragma: no cover - pyyaml is a suite dependency
        raise CodeSurfaceError("pyyaml is required to read the register")
    if path.is_symlink() or _has_symlinked_ancestor(path):
        raise CodeSurfaceError(
            f"the register {path} is reached through a symlink, refused "
            "unread rather than followed: a committed symlink here — at "
            "the register's own name, or at any directory between it and "
            "the top — would let the gate consume bytes from outside the "
            "checkout and vary by runner. Replace it with a regular file "
            "at an ordinary, unsymlinked path")
    if not path.is_file():
        raise CodeSurfaceError(f"the register {path} does not exist")
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise CodeSurfaceError(f"the register {path} cannot be read: {exc}")
    try:
        doc = fm.strict_load(raw, what=f"the register {path.name}")
    except fm.StrictFrontMatterError as exc:
        raise CodeSurfaceError(f"the register {path.name} is refused: {exc}")
    if not isinstance(doc, dict) or not isinstance(doc.get("register"), list):
        raise CodeSurfaceError(
            f"the register {path.name} must carry a top-level `register:` list")
    if closed is None and path.resolve() == REGISTER_PATH.resolve():
        closed = CLOSED_REGISTER
    entries: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for index, entry in enumerate(doc["register"], start=1):
        if not isinstance(entry, dict):
            raise CodeSurfaceError(f"register entry {index} is not a mapping")
        for field, shape in _REQUIRED_ENTRY_KEYS.items():
            value = entry.get(field)
            if shape == "text":
                if not isinstance(value, str) or not value.strip():
                    raise CodeSurfaceError(
                        f"register entry {index} ({entry.get('change')!r}) is "
                        f"missing a non-empty `{field}:`")
                continue
            if not isinstance(value, list) or not value:
                raise CodeSurfaceError(
                    f"register entry {index} ({entry.get('change')!r}) is "
                    f"missing a non-empty `{field}:` list; the requirement has "
                    f"every standing entry carry a citation, and an entry "
                    f"without one tolerates an unreadable declaration on "
                    f"nobody's word")
            for position, item in enumerate(value, start=1):
                if not isinstance(item, str) or not item.strip():
                    raise CodeSurfaceError(
                        f"register entry {index} ({entry.get('change')!r}) "
                        f"carries a `{field}:` item ({position}) that is not "
                        f"non-empty text")
        if not CHANGE_ID_RE.match(entry["change"]):
            raise CodeSurfaceError(
                f"register entry {index} names `change: {entry['change']}`, "
                "which is not a change-directory name — one segment, no "
                "separator and no leading dot; the name is resolved under "
                "openspec/changes/, so a path written here would reach one")
        if entry["class"] not in REGISTER_CLASSES:
            raise CodeSurfaceError(
                f"register entry {index} ({entry['change']}) declares "
                f"`class: {entry['class']}`, which is not one of "
                f"{', '.join(REGISTER_CLASSES)}; the register is CLOSED and a "
                "new class is a change to the specification, not a register "
                "edit")
        key = (entry["change"], entry["declaration"])
        if key in seen:
            raise CodeSurfaceError(
                f"register entry {index} repeats {key[0]}; one entry per "
                "declaration, so a stale entry cannot hide behind a live twin")
        if closed is not None:
            baseline_key = (entry["change"],
                            declaration_digest(entry["declaration"]))
            if baseline_key not in closed:
                raise CodeSurfaceError(
                    f"register entry {index} names {entry['change']} with a "
                    f"declaration the CLOSED baseline does not carry "
                    f"(sha256 {baseline_key[1]}). The register is REMOVABLE, "
                    "NEVER ADDABLE: an entry appended here would make an "
                    "unreadable declaration pass with the gate green and the "
                    "ratchet would have failed in the one direction that "
                    "matters. If the exception is genuinely owed, add the pair "
                    "to `CLOSED_REGISTER` in the same pull request, where the "
                    "diff shows the act for what it is")
        seen.add(key)
        entries.append(entry)
    return entries


def register_entry_for(change: str, text: str,
                       register: list[dict]) -> dict | None:
    """The register entry tolerating `change`'s declaration `text`, or None.

    THE MATCH IS ON THE DECLARATION AS IT STANDS, not on the change alone: an
    entry records the text it tolerates, so an author who corrects the
    declaration stops matching it and the run REFUSES until somebody deletes
    the entry. That is the requirement's stale arm, and it is the event that
    forces the re-examination.
    """
    for entry in register:
        if entry["change"] == change and entry["declaration"] == text:
            return entry
    return None


def _unescaped(repo_root: Path, relative: Path) -> Path | None:
    """`repo_root / relative`, but ONLY when it is a REAL, UNESCAPED path under
    `repo_root` — no symlink ANYWHERE between the two, not only at the leaf —
    and `None` otherwise.

    `Path.is_file()` FOLLOWS SYMLINKS, so a committed
    `openspec/changes/<id>/proposal.md` symlink — or an ordinary `proposal.md`
    inside a symlinked CHANGE DIRECTORY, or under a symlinked `openspec/` —
    would otherwise be read as an active proposal of the scanned tree, and
    `declaration()` would judge bytes that live outside it. A dangling link is
    the same defect wearing the other face: the proposal vanishes from the scan
    and the tree is judged on a corpus it does not have. NEITHER is a judgment
    about the scanned tree, which is the only thing this gate is entitled to
    make — which is why a path that fails this test is DROPPED rather than
    reported as a finding.

    The leaf's own `is_symlink()` does not settle it: a REGULAR file reached
    through a symlinked parent is not itself a symlink, and ordinariness is a
    property of the ONE component checked. So the test is: resolve everything,
    and require that you land where a symlink-free tree would have put you —
    which closes the escape at every component in ONE comparison rather than one
    component at a time as each is found. `repo_root` is resolved on BOTH sides,
    so a `repo_root` that is ITSELF reached through a symlink (a scratch tree
    under a symlinked `/tmp`, say) is not mistaken for the escape.

    `target_release._unescaped` is the exact shape this mirrors.
    """
    candidate = repo_root / relative
    try:
        resolved = candidate.resolve(strict=True)
        resolved_root = repo_root.resolve(strict=True)
    except OSError:
        return None
    if resolved != resolved_root / relative:
        return None
    return candidate


def _proposals(repo_root: Path, archived: bool) -> list[Path]:
    """Every `proposal.md` the scanned tree really carries, active or archived.

    THE SCAN IS TOP-LEVEL AND THAT IS LOAD-BEARING (the sibling's reason, and
    `validate-scope-globs.py`'s): a recursive scan would reach the roughly one
    hundred `tests/doc-health/fixtures/**/proposal.md` documents that carry this
    front matter as fixture text for other families, and make this gate a tax on
    every fixture the estate writes.

    EVERY PATH IS TAKEN THROUGH `_unescaped`, never through a bare `is_file()`.
    """
    changes = _unescaped(repo_root, CHANGES_DIR)
    if changes is None or not changes.is_dir():
        return []
    if archived:
        archive_rel = CHANGES_DIR / "archive"
        archive = _unescaped(repo_root, archive_rel)
        if archive is None or not archive.is_dir():
            return []
        found = []
        for child in sorted(archive.iterdir()):
            if not child.is_dir():
                continue
            proposal = _unescaped(
                repo_root, archive_rel / child.name / "proposal.md")
            if proposal is not None and proposal.is_file():
                found.append(proposal)
        return found
    found = []
    for child in sorted(changes.iterdir()):
        if not child.is_dir() or child.name == "archive":
            continue
        proposal = _unescaped(repo_root, CHANGES_DIR / child.name / "proposal.md")
        if proposal is not None and proposal.is_file():
            found.append(proposal)
    return found


def scan(repo_root: Path, register: list[dict] | None = None) -> Report:
    """Judge every ACTIVE proposal in `repo_root`; count the archive."""
    if register is None:
        register = load_register()
    covered = {(e["change"], e["declaration"]): e for e in register}
    matched: set[tuple[str, str]] = set()

    findings: list[Finding] = []
    registered: list[tuple[str, str]] = []
    inside_none = inside_repositories = 0
    active_declaring = 0

    active = _proposals(repo_root, archived=False)
    for proposal in active:
        change = proposal.parent.name
        rel = str(proposal.relative_to(repo_root))
        try:
            present, text = declaration(proposal)
        except CodeSurfaceError as exc:
            findings.append(Finding(
                change, rel, "<unreadable>",
                f"its front matter cannot be read — {exc}"))
            continue
        if not present:
            continue  # the promoted default; declaring nothing declares it
        active_declaring += 1
        assert text is not None  # `present` is True only with a value
        try:
            head = parse_head(text)
        except CodeSurfaceError as exc:
            key = (change, text)
            if key in covered:
                matched.add(key)
                registered.append((change, covered[key]["class"]))
                continue
            findings.append(Finding(change, rel, _excerpt(text), str(exc)))
            continue
        if head.is_none:
            inside_none += 1
        else:
            inside_repositories += 1

    stale = tuple(
        f"{change} / {_excerpt(text, 60)!r}" for (change, text) in covered
        if (change, text) not in matched)

    archived_paths = _proposals(repo_root, archived=True)
    archived_declaring = 0
    archived_off = 0
    for proposal in archived_paths:
        try:
            present, text = declaration(proposal)
        except CodeSurfaceError:
            continue  # read, never judged
        if not present or text is None:
            continue
        archived_declaring += 1
        try:
            parse_head(text)
        except CodeSurfaceError:
            archived_off += 1

    return Report(
        active_total=len(active),
        active_declaring=active_declaring,
        inside_none=inside_none,
        inside_repositories=inside_repositories,
        registered=tuple(sorted(registered)),
        findings=tuple(findings),
        stale=tuple(sorted(stale)),
        archived_total=len(archived_paths),
        archived_declaring=archived_declaring,
        archived_off_grammar=archived_off,
    )
