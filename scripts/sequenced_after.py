"""The `sequenced_after:` ordered-delta parent substrate (release-realization).

Realizes the `release-realization` requirements ADDED by
`add-sequenced-after-substrate` (ratified 2026-09-01, as authored):

  * "Machine-readable ordered-delta parent declaration" — the OPTIONAL
    front-matter sibling field `sequenced_after:`, a SEQUENCE of parent change
    references, where `sequenced_after: []` is a POSITIVE,
    RATIFICATION-COVERED ROOT CLAIM and ABSENCE is NO DECLARATION AT ALL.
  * "Repository-qualified parent-reference syntax" — bare `<change-id>` or
    `<repository>:<change-id>`, with a self-qualified entry normalized to bare.
  * "Parent-declaration validation" — shape, grammar, resolvability of every
    BARE entry, and CYCLE refusal; NO depth limit and NO fan-out limit.
  * "Ordered-delta identity survives archival" — resolution over EXACTLY TWO
    ANCHORED locations, exactly-one, never resolved by preference.
  * "Parent-declaration retention at archive" — the freeze: the declaration's
    bytes may not change between ratification and archive.

ABSENCE IS FAIL-CLOSED AND IS NOT A ROOT CLAIM. `read_declaration` returns the
`ABSENT` sentinel — NOT `[]` — when the field is missing, and the two are
DIFFERENT FACTS: `[]` is a positive root claim covered by the change's
ratification, absence is no declaration about chain position at all. A parser
that conflated them would destroy the whole root-proof doctrine, because before
adoption no change carries the field and "absence is the root" would make every
chain read as a depth-one root.

NO WALK POLICY LIVES HERE. This module declares no depth ceiling, no fan-out cap
and no scope- or authority-composition operator — those are the AUTHORIZATION
POLICY of a consuming gate (codexFactory's provenance-tie verifier: FOUR hops
inclusive of the terminal change, INTERSECTION composition), declared in that
gate's own specification where it is enforced and can be measured. What the
substrate owes is that the chain be WELL-FORMED and WALKABLE: resolvable,
acyclic, unambiguous and frozen. A CYCLE is refused here because it is a
WELL-FORMEDNESS defect — no consumer's policy can resolve a chain that revisits
an id to a root — while depth is not refused because a number baked into a
neutral field would bind repositories that never adopt the consuming axis and
would drift from the one gate that enforces it.

THE FIELD IS READ THROUGH THE SHARED STRICT LOADER
(`scripts/frontmatter_strict.py`), the same one `scripts/scope_globs.py` reads
`scope_globs:` through: duplicate keys at any level, anchors, aliases, merge
keys, non-UTF-8 bytes, YAML directives, more than one document and an
over-ceiling block are REFUSED rather than silently resolved. A permissive
loader here would not merely under-enforce — it would show a reviewer one parent
and walk another.

Deterministic: text/YAML reads and `git show` object reads only; no model calls,
no writes, no network.
"""

from __future__ import annotations

import datetime
import importlib.util
import json
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path


def _sibling(name: str):
    """Import a sibling module from THIS file's directory WITHOUT mutating
    `sys.path` — the same route `scripts/scope_globs.py` takes, and for the same
    reason: a library module that inserts its own directory at `sys.path[0]`
    changes import resolution for every caller in the process. The plain import
    is tried first (the ordinary CLI route), with a by-location fallback for the
    route that loads this file directly by path.
    """
    try:
        return importlib.import_module(name)
    except ImportError:
        pass
    if name in sys.modules:  # pragma: no cover - a partially imported sibling
        return sys.modules[name]
    path = Path(__file__).resolve().parent / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ImportError(f"cannot locate the sibling module {name} at {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


fms = _sibling("frontmatter_strict")

#: The field name, once, so no caller spells it.
FIELD = "sequenced_after"

#: The repository this substrate's own corpus belongs to. A consumer validating
#: ANOTHER repository's corpus passes its own name — the token only decides which
#: qualified entries normalize to the bare form, and mis-naming it would make a
#: self-qualified entry read as foreign (declarable, unresolved) rather than as
#: the local reference it is.
DECLARING_REPOSITORY = "openxFactory"


class SequencedAfterError(Exception):
    """Raised when a `sequenced_after` declaration is malformed, ungrammatical,
    unresolvable, ambiguous, or cyclic.

    The message names the offending change, the offending entry and the rule it
    breaks, so the house validate run can report it directly.
    """


class _Absent:
    """The sentinel for A FIELD THAT IS NOT THERE, distinct from `[]`.

    A singleton with a falsy truth value and a legible repr, so a caller that
    writes `if declaration is ABSENT` reads correctly and a caller that
    accidentally writes `if declaration:` at least does not read absence as a
    non-empty chain.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:  # pragma: no cover - diagnostics only
        return "<no sequenced_after declaration>"


#: Absence — NO DECLARATION MADE. Never equal to `[]`, which is a root CLAIM.
ABSENT = _Absent()


# --- front-matter reading ----------------------------------------------------


def read_front_matter(source: str | bytes | Path) -> dict:
    """The realization-axis front matter, read through the SHARED strict loader.

    Raises `SequencedAfterError` for any strict-loader refusal, preserving the
    loader's message (which names the construct and its line).
    """
    try:
        return fms.read_front_matter(source)
    except fms.StrictFrontMatterError as exc:
        raise SequencedAfterError(str(exc)) from exc


def read_declaration(proposal: str | bytes | Path) -> object:
    """Return the RAW `sequenced_after` value from a proposal.

    Returns `ABSENT` when the field is not declared at all, and the raw value
    otherwise — INCLUDING `None` for a `sequenced_after:` line with no value,
    which is PRESENT-but-malformed and is refused by `validate_shape`, not
    silently read as absence. Presence is decided by the KEY, never by the value.
    """
    front = read_front_matter(proposal)
    if FIELD not in front:
        return ABSENT
    return front[FIELD]


# --- the reference grammar ---------------------------------------------------
#
# `<change-id>` and `<repository>` token grammars are the ones the corpus
# already uses: change-folder names are lower-kebab, and the repository token is
# the same one `scripts/doc_health/proposal_origin.py`'s origin-id regexes take.

#: A change id: lower-case alphanumerics and hyphens, starting alphanumeric, and
#: NEVER containing `/` — so a reference can never name a nested path.
CHANGE_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")

#: A repository token, as in the origin-id declarations.
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+$")


@dataclass(frozen=True)
class ParentRef:
    """One resolved-syntax `sequenced_after` entry.

    `repository` is None for a reference into the DECLARING repository's own
    corpus — which is what both a bare entry and a SELF-QUALIFIED entry become,
    since a qualified entry naming the declaring repository is equivalent to the
    bare form.
    """

    change_id: str
    repository: str | None = None
    raw: str = ""

    @property
    def is_local(self) -> bool:
        return self.repository is None

    @property
    def is_foreign(self) -> bool:
        return self.repository is not None

    def canonical(self) -> str:
        """The normalized text of the reference: bare for local, qualified for
        foreign. Two entries with the same canonical form are ONE reference."""
        return self.change_id if self.is_local else f"{self.repository}:{self.change_id}"


def parse_entry(
    value: object,
    where: str = FIELD,
    declaring_repository: str = DECLARING_REPOSITORY,
) -> ParentRef:
    """Parse ONE entry into a `ParentRef`, or raise naming the rule it breaks."""
    if isinstance(value, bool) or not isinstance(value, str):
        raise SequencedAfterError(
            f"{where} entries must be non-empty strings; found {value!r} "
            f"({type(value).__name__})")
    if not value:
        raise SequencedAfterError(
            f"{where} entries must be non-empty strings; found an empty string")
    if value != value.strip():
        raise SequencedAfterError(
            f"{where} entry {value!r} carries leading or trailing whitespace; a "
            "reference is compared exactly and is never trimmed for the author")
    if value.count(":") > 1:
        raise SequencedAfterError(
            f"{where} entry {value!r} carries more than one ':'; the syntax is "
            f"either a bare <change-id> or a single <repository>:<change-id>")
    if ":" in value:
        repository, change_id = value.split(":", 1)
        if not REPOSITORY.match(repository):
            raise SequencedAfterError(
                f"{where} entry {value!r} has repository half {repository!r}, "
                f"which does not match {REPOSITORY.pattern} (an empty or "
                f"path-shaped repository token is refused)")
    else:
        repository, change_id = None, value
    if not CHANGE_ID.match(change_id):
        raise SequencedAfterError(
            f"{where} entry {value!r} has change-id half {change_id!r}, which "
            f"does not match {CHANGE_ID.pattern}; a change id is lower-kebab and "
            f"never contains '/', so a reference can never name a nested path")
    if repository is not None and repository == declaring_repository:
        # A self-qualified entry IS the bare form, normalized here so a chain
        # walk, a duplicate check and a resolution cannot disagree about it.
        repository = None
    return ParentRef(change_id=change_id, repository=repository, raw=value)


# --- schema / shape ----------------------------------------------------------


@dataclass(frozen=True)
class SequencedAfter:
    """A validated `sequenced_after` declaration: an ordered tuple of parents."""

    entries: tuple[ParentRef, ...]

    @property
    def is_root_claim(self) -> bool:
        """True for the EXPLICIT `[]` — a positive, ratification-covered claim
        that the change is a chain root. Never true for absence, which never
        reaches this type."""
        return self.entries == ()

    def local_ids(self) -> tuple[str, ...]:
        return tuple(e.change_id for e in self.entries if e.is_local)

    def foreign_refs(self) -> tuple[ParentRef, ...]:
        return tuple(e for e in self.entries if e.is_foreign)

    def canonical_entries(self) -> tuple[str, ...]:
        return tuple(e.canonical() for e in self.entries)


def validate_shape(
    value: object,
    where: str = FIELD,
    declaring_repository: str = DECLARING_REPOSITORY,
) -> SequencedAfter:
    """Validate the STRUCTURE and GRAMMAR of a raw `sequenced_after` value.

    Shape contract: a SEQUENCE — possibly empty — of non-empty strings, with no
    null members, no nested collections, and no duplicate entries after
    normalization. Each entry must conform to the repository-qualified
    parent-reference syntax. Raises `SequencedAfterError` naming the offending
    entry otherwise. RESOLVABILITY is a separate concern (`resolve`,
    `validate_resolvable`); this function never touches the filesystem.
    """
    if value is ABSENT:
        raise SequencedAfterError(
            f"{where} is absent; absence is NO DECLARATION and is never "
            f"validated as one — a caller must branch on the ABSENT sentinel "
            f"rather than hand it here")
    if isinstance(value, (str, bytes)) or not isinstance(value, (list, tuple)):
        raise SequencedAfterError(
            f"{where} must be a sequence of parent change references, not "
            f"{type(value).__name__}; a bare string is refused rather than "
            f"coerced to a one-entry list, because coercion is an interpretation "
            f"the writer chooses")
    entries: list[ParentRef] = []
    seen: dict[str, str] = {}
    for member in value:
        if isinstance(member, (list, tuple, dict, set)):
            raise SequencedAfterError(
                f"{where} entries must be strings; found the nested "
                f"{type(member).__name__} {member!r}")
        ref = parse_entry(member, where=where,
                          declaring_repository=declaring_repository)
        canonical = ref.canonical()
        if canonical in seen:
            raise SequencedAfterError(
                f"{where} names {canonical!r} twice (as {seen[canonical]!r} and "
                f"{ref.raw!r}); a parent is declared once, and a self-qualified "
                f"entry is the same reference as the bare form")
        seen[canonical] = ref.raw
        entries.append(ref)
    return SequencedAfter(entries=tuple(entries))


# --- resolution over the ACTIVE and ARCHIVED corpora -------------------------
#
# ANCHORED ON BOTH SIDES, and exactly-one. A prefix strip or a split on the first
# hyphen would mis-resolve a change id that itself contains digits and hyphens,
# and an unanchored active side would admit a nested
# `openspec/changes/<id>/openspec/changes/<id2>/`.

#: An archived change directory: a `YYYY-MM-DD-` date prefix whose remainder is
#: the change id EXACTLY.
ARCHIVE_DIR = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<id>.+)$")


def changes_root(repo_root: str | Path) -> Path:
    return Path(repo_root) / "openspec" / "changes"


def active_change_dirs(repo_root: str | Path) -> dict[str, Path]:
    """Change id -> directory, for the ACTIVE corpus (never `archive/`)."""
    root = changes_root(repo_root)
    found: dict[str, Path] = {}
    if not root.is_dir():
        return found
    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name == "archive":
            continue
        found[child.name] = child
    return found


def archived_change_dirs(repo_root: str | Path) -> dict[str, list[Path]]:
    """Change id -> ALL matching archived directories.

    A LIST rather than a single path on purpose: two archive dates for one id is
    an AMBIGUITY the resolver must be able to report, not a collision to resolve
    by taking the newest.
    """
    root = changes_root(repo_root) / "archive"
    found: dict[str, list[Path]] = {}
    if not root.is_dir():
        return found
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        match = ARCHIVE_DIR.match(child.name)
        if match is None:
            continue
        found.setdefault(match.group("id"), []).append(child)
    return found


def archive_dates(repo_root: str | Path) -> dict[str, str]:
    """Change id -> the DATE ITS ARCHIVED DIRECTORY IS NAMED WITH.

    Only ids with EXACTLY ONE archived directory appear. Two dated directories
    for one id is the ambiguity `resolve` reports; picking one here would decide
    it silently, and the caller of this function is a provenance stamp, which is
    the last place to guess.

    The archive date is a FACT ON DISK — the directory name the OpenSpec CLI
    wrote — and it is what `moved_on` records for an archived row: the day the
    change entered canon. Issue #790: the pinned CLI names that directory from
    its OWN clock and the ledger seeder stamped `moved_on` from the machine's
    local one, so the two could disagree and nothing compared them.
    """
    found: dict[str, str] = {}
    for change_id, dirs in archived_change_dirs(repo_root).items():
        if len(dirs) != 1:
            continue
        match = ARCHIVE_DIR.match(dirs[0].name)
        # A REAL CALENDAR DATE, not merely a digit-shaped one — `ARCHIVE_DIR`
        # accepts `2026-13-45` and `is_moved_on` does not. A directory named
        # that is a different defect from the one this function serves, and
        # stamping it onto a row would produce a ledger the renderer's own
        # read-back then refuses.
        if match is not None and is_moved_on(match.group("date")):
            found[change_id] = match.group("date")
    return found


def candidate_dirs(repo_root: str | Path, change_id: str) -> list[Path]:
    """Every directory the EXACTLY TWO anchored locations offer for `change_id`."""
    candidates: list[Path] = []
    active = changes_root(repo_root) / change_id
    if active.is_dir():
        candidates.append(active)
    candidates.extend(archived_change_dirs(repo_root).get(change_id, []))
    return candidates


def resolve(repo_root: str | Path, change_id: str, where: str = FIELD) -> Path:
    """Resolve `change_id` to EXACTLY ONE change directory, or raise.

    Zero candidates is UNRESOLVABLE; two or more is AMBIGUOUS. Neither is
    resolved by preference — one id matching two directories on a surface that
    authorizes anything is not a case to decide by precedence, and an archived
    hop's declarations are read from the ARCHIVED directory precisely because it
    carries the frozen ratified text.
    """
    candidates = candidate_dirs(repo_root, change_id)
    if not candidates:
        raise SequencedAfterError(
            f"{where} entry {change_id!r} resolves to no change directory in "
            f"this repository's corpus (neither openspec/changes/{change_id}/ "
            f"nor an anchored openspec/changes/archive/<YYYY>-<MM>-<DD>-"
            f"{change_id}/); a dangling parent reference is unwalkable")
    if len(candidates) > 1:
        listed = ", ".join(str(c.relative_to(Path(repo_root))) for c in candidates)
        raise SequencedAfterError(
            f"{where} entry {change_id!r} is AMBIGUOUS — it matches "
            f"{len(candidates)} directories ({listed}); resolution requires "
            f"exactly one and MUST NOT prefer either")
    return candidates[0]


def declaration_of(change_dir: Path) -> object:
    """The raw `sequenced_after` of a change directory, or `ABSENT`.

    Read from the directory GIVEN — for an archived hop that is the archived
    directory, which carries the frozen ratified text.
    """
    proposal = Path(change_dir) / "proposal.md"
    if not proposal.is_file():
        return ABSENT
    return read_declaration(proposal)


# --- validation: grammar + resolvability + acyclicity ------------------------


def validate_resolvable(
    repo_root: str | Path,
    declaration: SequencedAfter,
    where: str = FIELD,
) -> None:
    """Every BARE entry SHALL resolve to exactly one change in this corpus.

    A QUALIFIED FOREIGN entry is checked for WELL-FORMEDNESS ONLY (already done
    by the grammar): the neutral validator cannot read another repository's
    corpus and MUST NOT pretend to. Its DISPOSITION is the consumer's, which
    refuses it under a named identifier rather than skipping it — skipping would
    fabricate a root out of a declaration that says the opposite.
    """
    for entry in declaration.entries:
        if entry.is_local:
            resolve(repo_root, entry.change_id, where=where)


def validate_acyclic(
    repo_root: str | Path,
    change_id: str,
    where: str = FIELD,
    declaring_repository: str = DECLARING_REPOSITORY,
) -> None:
    """Refuse a CYCLE reachable within this repository's own corpus.

    Depth-first over the LOCAL entries, with the refusal keyed on the CURRENT
    PATH rather than on everything ever seen: a DIAMOND (two parents that share
    a grandparent) re-visits a node without revisiting it ON THE PATH and is
    NOT a cycle — a global seen-set would refuse an honest fan-in.

    NO DEPTH LIMIT AND NO FAN-OUT LIMIT is imposed. A malformed or unresolvable
    hop encountered mid-walk is NOT re-reported here (`validate_resolvable`
    owns that message for the declaring change, and a hop's own validation owns
    it for the hop): the walk simply stops descending, because a cycle through a
    hop that cannot be read is not a cycle this validator can prove.
    """
    on_path: list[str] = []
    finished: set[str] = set()

    def descend(current: str) -> None:
        if current in finished:
            return
        if current in on_path:
            cycle = " -> ".join(on_path[on_path.index(current):] + [current])
            raise SequencedAfterError(
                f"{where} forms a CYCLE through {current!r} ({cycle}); no "
                f"consumer's policy can resolve a cycle to a root, so it is a "
                f"well-formedness defect rather than a policy judgement")
        on_path.append(current)
        try:
            change_dir = resolve(repo_root, current, where=where)
        except SequencedAfterError:
            on_path.pop()
            finished.add(current)
            return
        raw = declaration_of(change_dir)
        if raw is not ABSENT:
            try:
                declaration = validate_shape(
                    raw, where=f"{where} of {current}",
                    declaring_repository=declaring_repository)
            except SequencedAfterError:
                declaration = None
            if declaration is not None:
                for parent in declaration.local_ids():
                    descend(parent)
        on_path.pop()
        finished.add(current)

    descend(change_id)


def validate_declaration(
    repo_root: str | Path,
    change_id: str,
    raw: object,
    declaring_repository: str = DECLARING_REPOSITORY,
) -> SequencedAfter:
    """Full validation of ONE change's raw declaration: shape, grammar,
    resolvability of every bare entry, and acyclicity. Returns the validated
    declaration. Imposes NO depth limit and NO fan-out limit — a two-parent
    declaration and a chain deeper than any gate would walk both VALIDATE."""
    where = f"{FIELD} of {change_id}"
    declaration = validate_shape(
        raw, where=where, declaring_repository=declaring_repository)
    validate_resolvable(repo_root, declaration, where=where)
    validate_acyclic(repo_root, change_id, where=where,
                     declaring_repository=declaring_repository)
    return declaration


def chain_depth(
    repo_root: str | Path,
    change_id: str,
    declaring_repository: str = DECLARING_REPOSITORY,
) -> int:
    """The LONGEST resolvable declared chain from `change_id`, in HOPS.

    Zero hops means the change declares no local parent (an explicit `[]`, an
    absent field, or only foreign entries). Reported as a MEASUREMENT for the
    corpus sweep, never enforced: the depth ceiling belongs to the consuming
    gate. Assumes an acyclic corpus (`validate_acyclic` is the gate for that)
    and stops descending at anything it cannot read.
    """
    memo: dict[str, int] = {}
    on_path: set[str] = set()

    def resolves(candidate: str) -> bool:
        try:
            resolve(repo_root, candidate)
        except SequencedAfterError:
            return False
        return True

    def depth(current: str) -> int:
        if current in memo:
            return memo[current]
        if current in on_path:  # pragma: no cover - a cycle is refused upstream
            return 0
        on_path.add(current)
        best = 0
        try:
            raw = declaration_of(resolve(repo_root, current))
        except SequencedAfterError:
            raw = ABSENT
        if raw is not ABSENT:
            try:
                declaration = validate_shape(
                    raw, declaring_repository=declaring_repository)
            except SequencedAfterError:
                declaration = None
            if declaration is not None:
                for parent in declaration.local_ids():
                    # AN UNRESOLVED HOP IS NOT A RESOLVED HOP. The measure is the
                    # deepest chain the sweep RESOLVES, so a dangling parent — a
                    # validation failure elsewhere — must not inflate it.
                    if resolves(parent):
                        best = max(best, 1 + depth(parent))
        on_path.discard(current)
        memo[current] = best
        return best

    if not resolves(change_id):
        return 0
    return depth(change_id)


# --- parent-declaration retention at archive (the FREEZE) --------------------
#
# Mirrors `scope_globs.scope_retention_at_archive` and the "Origin retention at
# archive" gate: a ratified chain position is auditable and immutable, so a
# change cannot silently re-parent itself — or PROMOTE ITSELF TO A ROOT —
# between ratification and archive, which under any narrowing composition would
# be a widening. Contested class: reversing this reverses a gate decision.


def _canonical(value: object) -> object:
    """A comparable canonical form of a raw declaration.

    `ABSENT` and `None` stay DISTINGUISHABLE from `[]`: absence, an empty
    declaration and a null value are three different facts, and a comparison
    that flattened them would let a change promote itself to a declared root
    between ratification and archive without registering as a mutation. Entry
    ORDER is significant (the frozen declaration is compared as authored), and
    entries are NFC-normalized so a canonically-equivalent re-spelling is not
    read as a change. An unparseable value becomes a sentinel so that a mutation
    INTO malformed shape still registers rather than crashing the gate.
    """
    if value is ABSENT:
        return ("__absent__",)
    if value is None:
        return ("__null__",)
    try:
        declaration = validate_shape(value)
    except SequencedAfterError:
        return ("__unparseable__", repr(value))
    return tuple(unicodedata.normalize("NFC", e)
                 for e in declaration.canonical_entries())


def retention_problem(ratified: object, current: object) -> str | None:
    """Return a contested-class problem string when `current` differs from the
    `ratified` declaration, or None when unchanged.

    Both may be `ABSENT` (no declaration — the common case, trivially retained).
    Adding, removing, re-parenting, promoting to a root, and reordering all
    register as mutations.
    """
    if _canonical(ratified) == _canonical(current):
        return None
    return (
        f"{FIELD} was mutated after ratification (ratified: {ratified!r}; "
        f"current: {current!r}); a ratified chain position is frozen — a change "
        f"may not silently re-parent itself, or promote itself to a root, "
        f"between ratification and archive. Restoring or accepting the mutation "
        f"is a contested-class act requiring an explicit disposition"
    )


def _git_toplevel(path: Path) -> Path:
    """The work-tree root containing `path`.

    Raises `SequencedAfterError` — never a `CalledProcessError` traceback —
    when `path` is not inside a git work tree at all. A mistyped or
    non-existent CHANGE_DIR is the SAME CLASS of operator error #705 filed on
    the sibling gate, and it must arrive at the CLI as a named "cannot run"
    finding (exit 2) rather than as a stack trace. The sibling
    `scope_globs._git_toplevel` converts this case in exactly this shape
    (#723); this is the mirror of that arm, so the two archive gates refuse the
    same input the same way.
    """
    directory = path if path.is_dir() else path.parent
    out = subprocess.run(
        ["git", "-C", str(directory), "rev-parse", "--show-toplevel"],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        detail = out.stderr.strip() or f"git rev-parse exited {out.returncode}"
        raise SequencedAfterError(
            f"{str(directory)!r} is not inside a git work tree, so the "
            f"ratified-side proposal cannot be read: {detail}")
    return Path(out.stdout.strip())


def _ref_names_a_commit(repo_root: Path, ref: str) -> bool:
    """Whether `ref` resolves to a COMMIT in `repo_root`.

    Checked BEFORE the by-id lookup so an unresolvable ref (a typo, a deleted
    branch) or a ref naming a non-commit object is reported as what it is. The
    lookup's own probes (`_blob_exists_at_ref`, `_archive_dir_names_at_ref`)
    deliberately swallow git's exit status, so without this a bad ref would be
    reported in the wording of a change that is absent at a good one —
    pointing the operator at the wrong thing. Mirrors
    `scope_globs._ref_names_a_commit` (#723).
    """
    out = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "--verify", "--quiet",
         f"{ref}^{{commit}}"],
        capture_output=True, text=True,
    )
    return out.returncode == 0


def change_id_of_dir(change_dir: str | Path) -> str:
    """The change id a CURRENT directory names — active or archived.

    An active directory `openspec/changes/<id>` names `<id>` directly. An
    archived directory `openspec/changes/archive/<YYYY-MM-DD>-<id>` names
    `<id>` with the date prefix stripped, via the SAME `ARCHIVE_DIR` naming
    convention `archived_change_dirs` already parses — reused here rather than
    re-invented, so the two readings of the convention cannot drift apart.
    "Archived" is decided by the PARENT directory's name, not by whether the
    directory's own name happens to match the date-prefix shape, so an active
    id that coincidentally looks date-prefixed is never misread.
    """
    path = Path(change_dir)
    if path.parent.name == "archive":
        match = ARCHIVE_DIR.match(path.name)
        if match is not None:
            return match.group("id")
    return path.name


def _blob_exists_at_ref(repo_root: Path, ref: str, rel_path: str) -> bool:
    """Whether `rel_path` names a blob in `ref`'s tree — checked without
    touching the working tree or the index (`git cat-file -e`, no checkout)."""
    out = subprocess.run(
        ["git", "-C", str(repo_root), "cat-file", "-e", f"{ref}:{rel_path}"],
        capture_output=True, text=True,
    )
    return out.returncode == 0


def _archive_dir_names_at_ref(repo_root: Path, ref: str) -> list[str]:
    """Directory names directly under `openspec/changes/archive/` in `ref`'s
    tree — empty when that path did not exist there yet. Read with `ls-tree`,
    never a checkout."""
    out = subprocess.run(
        ["git", "-C", str(repo_root), "ls-tree", "--name-only", ref,
         "openspec/changes/archive/"],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        return []
    return [line.rsplit("/", 1)[-1] for line in out.stdout.splitlines() if line]


def proposal_path_at_ref(repo_root: Path, ref: str, change_id: str) -> str:
    """The repo-relative `proposal.md` path for `change_id` AS IT STOOD AT
    `ref`, resolved BY CHANGE ID against `ref`'s OWN tree — never derived from
    the caller's CURRENT directory, which may name a location the id never
    occupied at `ref` (a change archived after `ref` had no archived path
    there; one archived before `ref` had no active one).

    Tries the active location first
    (`openspec/changes/<change_id>/proposal.md`), then any archived directory
    at `ref` matching `openspec/changes/archive/<YYYY-MM-DD>-<change_id>/`
    (the same `ARCHIVE_DIR` convention `archived_change_dirs` parses on the
    working tree). Raises `SequencedAfterError` naming the id, the ref and
    both paths tried when NEITHER exists at `ref` — never lets the underlying
    git failure propagate as a traceback.
    """
    active_rel = f"openspec/changes/{change_id}/proposal.md"
    if _blob_exists_at_ref(repo_root, ref, active_rel):
        return active_rel
    for name in sorted(_archive_dir_names_at_ref(repo_root, ref)):
        match = ARCHIVE_DIR.match(name)
        if match is None or match.group("id") != change_id:
            continue
        archived_rel = f"openspec/changes/archive/{name}/proposal.md"
        if _blob_exists_at_ref(repo_root, ref, archived_rel):
            return archived_rel
    raise SequencedAfterError(
        f"{change_id!r} has no proposal.md at ref {ref!r} — tried "
        f"{active_rel!r} and any "
        f"'openspec/changes/archive/<YYYY-MM-DD>-{change_id}/proposal.md'; "
        f"neither exists in that ref's tree")


def declaration_at_ref(repo_root: Path, ref: str, proposal_rel: str) -> object:
    """The declaration as it stood at git `ref` (the ratified snapshot), or
    `ABSENT` when the field was not declared there."""
    out = subprocess.run(
        ["git", "-C", str(repo_root), "show", f"{ref}:{proposal_rel}"],
        capture_output=True, text=True, check=True,
    )
    return read_declaration(out.stdout)


def retention_at_archive(change_dir: str | Path, ratified_ref: str) -> str | None:
    """Archive-gate freeze check for one change directory.

    Reads the declaration from the change's `proposal.md` at `ratified_ref`
    and from the current working tree and returns a contested-class problem
    string if they differ (None when retained). The ratified-side proposal is
    located BY CHANGE ID at `ratified_ref` (`proposal_path_at_ref`) — never by
    reusing `change_dir`'s CURRENT path — so the gate keeps working after the
    change has moved from its active location to
    `openspec/changes/archive/<date>-<id>/` between ratification and archive:
    that move is exactly the case this gate exists to check. The gate ALSO
    proves the archive does not REWRITE declarations: since it compares the
    entries as authored, any date-prefixing, re-pointing or normalization
    performed on archival would register here as a mutation.

    `change_dir` is RESOLVED to an absolute path before its change id is read.
    The id is decided from the directory's own name and its PARENT's name
    (`archive` or not), so a cwd-relative spelling — `.` from inside the
    archived directory, or `<date>-<id>` from inside `archive/` — would
    otherwise be read against components the relative path does not carry, and
    the gate would refuse a directory it can perfectly well check.

    CHANGE_DIR must live under `openspec/changes/` of its repository: the
    ratified-side lookup is anchored there (active path first, then
    `openspec/changes/archive/<date>-<id>/`), which is the same anchoring the
    sibling gate uses and the only layout this corpus has.

    Raises `SequencedAfterError` (never a traceback) whenever it cannot READ
    what it compares: when `change_dir` is not inside a git work tree at all,
    when `ratified_ref` does not name a commit, when `change_id` has no
    proposal.md at `ratified_ref`, when `change_dir` carries no `proposal.md`
    IN THE WORKING TREE — the CURRENT declaration cannot be read, so the gate
    cannot run — and when the front matter on EITHER side is malformed or
    unparseable (`read_declaration` refuses it). Every one of those arms is
    also refused, in the same order and with the same exit code, by the sibling
    `scope_globs.scope_retention_at_archive`: the two archive gates read the
    same corpus over the same trees, so they refuse the same inputs alike
    (#749, mirroring #723).
    """
    change_path = Path(change_dir).resolve()
    proposal = change_path / "proposal.md"
    repo_root = _git_toplevel(change_path)
    if not _ref_names_a_commit(repo_root, ratified_ref):
        # NAMED AS AN UNRESOLVABLE REF, NOT AS AN ABSENT CHANGE. Without this
        # probe a typo or a deleted branch fell through to the by-id lookup,
        # whose git probes swallow their exit status, and was reported as
        # "<id> has no proposal.md at ref <ref>" — the wording of a change that
        # is genuinely absent at a resolvable ref. That sends the operator to
        # look for a missing directory when the ref is what is wrong.
        raise SequencedAfterError(
            f"the ratified ref {ratified_ref!r} does not name a commit in "
            f"{str(repo_root)!r} — the ratified-side proposal was not looked "
            "up at all; this is an unresolvable ref, NOT a change that is "
            "absent at a resolvable one")
    change_id = change_id_of_dir(change_path)
    ratified_rel = proposal_path_at_ref(repo_root, ratified_ref, change_id)
    ratified = declaration_at_ref(repo_root, ratified_ref, ratified_rel)
    if not proposal.is_file():
        # A MISSING CURRENT-SIDE PROPOSAL IS "CANNOT RUN", NOT A COMPARISON
        # INPUT. Reading it as `ABSENT` made the gate answer a question it had
        # not asked: a change that declared nothing at ratification reported
        # RETAINED, and one that DID declare reported a contested MUTATION — a
        # declaration nobody removed, because the file that would hold it is
        # simply not there. Both readings are verdicts about a declaration the
        # gate never read, and `ABSENT` is a load-bearing FACT in this module
        # ("no declaration was made"), not a stand-in for "the proposal is
        # missing" — conflating them is exactly the conflation the ABSENT
        # sentinel exists to prevent.
        #
        # THE SIBLING GATE ALREADY REFUSES THIS CASE:
        # `scope_globs.scope_retention_at_archive` raises
        # `ScopeGlobsResolutionError` here (#723, which recorded the divergence
        # as a follow-on because this file was outside its declared scope).
        # This is that follow-on: the two archive gates now read the case alike,
        # each as a named "CANNOT RUN" finding with exit 2.
        raise SequencedAfterError(
            f"the change directory {str(change_path)!r} carries no proposal.md "
            f"in the working tree ({str(proposal)!r}), so the CURRENT "
            f"{FIELD} declaration cannot be read at all — the gate cannot run; "
            f"this is NOT a proposal that exists and makes no declaration "
            f"(the ABSENT reading), which would report a mutation nobody made "
            f"or a retention nobody earned")
    current = read_declaration(proposal)
    return retention_problem(ratified, current)


# --- the CORPUS SWEEP: a shipped, RE-RUNNABLE report -------------------------
#
# Task 5.4, and the "Chain-walk policy belongs to the consumer, and its bound
# SHALL be measured" requirement. A one-off measurement recorded in prose ages
# into a stale sentence; a re-runnable report is what makes the
# MEASURED-NOT-ASSUMED obligation discharge over time. A ZERO reading of the
# deepest chain is ZERO EVIDENCE about any gate's ceiling — never evidence that
# the ceiling is sufficient.

#: A requirement heading in a spec delta or a promoted spec.
REQUIREMENT_HEADING = re.compile(r"^###\s+Requirement:\s*(?P<title>.+?)\s*$")

#: The PROSE `Sequenced-after:` header some proposals carry — free text no schema
#: validates, counted so the substitution of a validated field for it is visible.
PROSE_HEADER = re.compile(r"^Sequenced-after:", re.IGNORECASE)


def normalize_requirement_title(title: str) -> str:
    """NFC + whitespace-collapsed + case-folded.

    The same normalization the authoring measurement used, and the reason it is
    needed: two changes that write the same requirement under a re-wrapped or
    re-cased title are co-modifiers, and a raw string comparison would report
    them as two sole modifiers — the exact under-count that would make the chain
    shape look like an edge case.
    """
    return unicodedata.normalize("NFC", " ".join(title.split())).casefold()


def requirement_keys(change_dir: Path) -> set[tuple[str, str]]:
    """The (capability-id, normalized-requirement-title) pairs a change writes.

    REQUIREMENT-GRANULAR on purpose: two changes touching the same CAPABILITY
    but no shared requirement are not ordered deltas on each other, and a
    capability-granular count would inflate the co-modified population.
    """
    keys: set[tuple[str, str]] = set()
    specs = Path(change_dir) / "specs"
    if not specs.is_dir():
        return keys
    for spec in sorted(specs.rglob("spec.md")):
        capability = spec.parent.name
        try:
            text = spec.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):  # pragma: no cover - defensive
            continue
        for line in text.splitlines():
            match = REQUIREMENT_HEADING.match(line)
            if match:
                keys.add((capability,
                          normalize_requirement_title(match.group("title"))))
    return keys


def corpus_change_dirs(repo_root: str | Path) -> dict[str, Path]:
    """Change id -> its directory, over the ACTIVE and ARCHIVED corpora both.

    Where an id is AMBIGUOUS the FIRST candidate is used for the population
    count only; ambiguity is a validation failure reported by `resolve`, and the
    sweep is a measurement rather than a gate.
    """
    found = dict(active_change_dirs(repo_root))
    for change_id, dirs in archived_change_dirs(repo_root).items():
        found.setdefault(change_id, dirs[0])
    return found


@dataclass(frozen=True)
class Sweep:
    """One reading of the corpus. Every field is a COUNT of something measured,
    never an assumption."""

    change_ids: int
    active: int
    archived: int
    co_modified: int
    sole_modifiers: int
    active_co_modified: int
    active_sole: int
    declaring: int
    root_claims: int
    prose_headers: int
    prose_headers_archived: int
    deepest_chain: int
    deepest_chain_change: str | None
    declaring_ids: tuple[str, ...]

    def render(self) -> str:
        deepest = (f"{self.deepest_chain} hop(s)"
                   + (f", from {self.deepest_chain_change}"
                      if self.deepest_chain_change else ""))
        lines = [
            "sequenced_after corpus sweep",
            "----------------------------",
            f"change ids ({self.active} active + {self.archived} archived): "
            f"{self.change_ids}",
            f"co-modified at requirement granularity (each would owe a "
            f"declaration): {self.co_modified}",
            f"sole modifiers (each would declare `sequenced_after: []`): "
            f"{self.sole_modifiers}",
            f"ACTIVE changes: co-modified / sole: {self.active_co_modified} / "
            f"{self.active_sole}",
            f"declaring `sequenced_after:`: {self.declaring}"
            + (f" ({', '.join(self.declaring_ids)})" if self.declaring_ids else ""),
            f"declaring an explicit `[]` root claim: {self.root_claims}",
            f"prose `Sequenced-after:` headers: {self.prose_headers} "
            f"({self.prose_headers_archived} archived)",
            f"DEEPEST DECLARED CHAIN RESOLVED: {deepest}",
        ]
        if self.deepest_chain == 0:
            lines.append(
                "  NOTE: a deepest-chain reading of ZERO is ZERO EVIDENCE about "
                "any consuming gate's depth ceiling. It is not evidence that a "
                "ceiling is sufficient; it means no honest chain has ever bound "
                "one.")
        return "\n".join(lines)


def corpus_sweep(
    repo_root: str | Path,
    declaring_repository: str = DECLARING_REPOSITORY,
) -> Sweep:
    """Measure the corpus: population, the co-modified/sole split at requirement
    granularity, adoption of the field, and THE DEEPEST DECLARED CHAIN."""
    repo_root = Path(repo_root)
    corpus = corpus_change_dirs(repo_root)
    active = set(active_change_dirs(repo_root))

    keys = {cid: requirement_keys(path) for cid, path in corpus.items()}
    owners: dict[tuple[str, str], set[str]] = {}
    for cid, cid_keys in keys.items():
        for key in cid_keys:
            owners.setdefault(key, set()).add(cid)

    co_modified = {cid for cid, cid_keys in keys.items()
                   if any(len(owners[key]) > 1 for key in cid_keys)}
    sole = set(corpus) - co_modified

    declaring: list[str] = []
    root_claims = 0
    prose = 0
    prose_archived = 0
    deepest = 0
    deepest_change: str | None = None
    for cid, path in sorted(corpus.items()):
        proposal = path / "proposal.md"
        if not proposal.is_file():
            continue
        try:
            raw = read_declaration(proposal)
        except SequencedAfterError:
            raw = ABSENT  # a refused document declares nothing measurable
        if raw is not ABSENT:
            declaring.append(cid)
            if raw == []:
                root_claims += 1
            depth = chain_depth(repo_root, cid,
                               declaring_repository=declaring_repository)
            if depth > deepest:
                deepest, deepest_change = depth, cid
        try:
            text = proposal.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):  # pragma: no cover - defensive
            continue
        if any(PROSE_HEADER.match(line) for line in text.splitlines()):
            prose += 1
            if cid not in active:
                prose_archived += 1

    return Sweep(
        change_ids=len(corpus),
        active=len(active),
        archived=len(corpus) - len(active),
        co_modified=len(co_modified),
        sole_modifiers=len(sole),
        active_co_modified=len(co_modified & active),
        active_sole=len(sole & active),
        declaring=len(declaring),
        root_claims=root_claims,
        prose_headers=prose,
        prose_headers_archived=prose_archived,
        deepest_chain=deepest,
        deepest_chain_change=deepest_change,
        declaring_ids=tuple(declaring),
    )


# --- the PER-CHANGE ledger ---------------------------------------------------
#
# WHY A LEDGER AND NOT FIVE SCALARS. The sweep above is the MEASUREMENT the
# "Chain-walk policy belongs to the consumer, and its bound SHALL be measured"
# requirement obliges, and re-running it is what makes that obligation discharge
# over time. What ages badly is not the measurement but the way it was PINNED: a
# handful of corpus-wide TOTALS asserted as literals in one test. Every change
# that is authored, ratified, adopted or archived moves at least one total, so
# two pull requests in flight edit the SAME LINES, git cannot auto-merge them,
# and whichever lands second owes a merge-from-main and a re-derivation for each
# CI window. The measurement is right; the pin serializes the queue.
#
# THE LEDGER IS THE SAME READING, KEYED BY CHANGE ID. One row per change carries
# what the sweep reads ABOUT THAT CHANGE — its corpus (active/archived), its
# co-modified/sole class, its declaration, its resolved chain depth, and whether
# it carries the legacy prose header — and EVERY total the `Sweep` reports is
# DERIVED from the rows. A pull request then edits ITS OWN ROW, and a partner's
# row when its own `## MODIFIED Requirements` block flips that partner from sole
# to co-modified. Two disjoint changes touch disjoint lines and merge without a
# conflict; two changes that really do move the same fact still collide, which
# is correct — that collision is a real disagreement about one row.
#
# ONE RESIDUE, MEASURED RATHER THAN ARGUED AWAY. Two NEW change ids that sort
# ADJACENTLY, with no existing row between them, share ONE INSERTION POINT and
# still conflict. Measured on a 159-row base by varying the gap: 0 intervening
# rows CONFLICTS, and ONE intervening row is already enough to merge clean (git
# needs context lines to separate two hunks, and a one-line row supplies them).
# Sorted order therefore shrinks the collision surface from "every change-dir
# pull request" to "two ids that sort with nothing between them"; it does not
# remove it, and the remainder is the landing window's (issue #618 item 1).
#
# THE DERIVATION IS DELIBERATELY INDEPENDENT OF `corpus_sweep`. `classify_corpus`
# walks the corpus again rather than being refactored out of the sweep, so
# `sweep_from_readings(classify_corpus(root)) == corpus_sweep(root)` is a
# CROSS-CHECK between two computations of the same totals rather than a
# tautology. The cost is one duplicated traversal of a corpus of a few hundred
# directories, paid so that a classifier bug cannot silently populate a ledger
# that then agrees with itself.

#: The ledger's location, relative to the repository root. It sits BESIDE the
#: test that reads it rather than under `contracts/`, because it is a test
#: fixture recording a measurement of this repository's own corpus — not a
#: neutral contract any consumer pins.
LEDGER_REL = Path("tests") / "sequenced_after" / "corpus-ledger.yaml"

LEDGER_SCHEMA_VERSION = 1
LEDGER_KIND = "sequenced_after_corpus_ledger"

#: The two corpora a change can sit in, and the two classes it can hold.
STATE_ACTIVE = "active"
STATE_ARCHIVED = "archived"
CLASS_SOLE = "sole"
CLASS_CO_MODIFIER = "co-modifier"

#: The row token for A FIELD THAT IS NOT THERE. Rendered as a bare word rather
#: than as YAML `~`, because `null` is a VALUE `sequenced_after:` can carry (a
#: key with no value, which `read_declaration` returns as `None` and
#: `validate_shape` refuses), and a ledger that spelled absence `~` could not
#: tell the two apart. A declaration is always a SEQUENCE, so no real
#: declaration can collide with the word.
DECLARES_ABSENT = "absent"

#: `#<number>`, the pull request that last moved a row, and an ISO date.
MOVED_BY = re.compile(r"^#[0-9]+$")
MOVED_ON = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")


def is_moved_on(value: object) -> bool:
    """A REAL ISO date, not merely a digit-shaped one: the pattern alone accepts
    `2026-13-45`, and a provenance date nobody can place is no provenance."""
    if not isinstance(value, str) or not MOVED_ON.match(value):
        return False
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return False
    return True

#: The row keys, in the order they are rendered. `depth` is present only on a
#: row that declares, because a chain depth is not a property a change without a
#: declaration has — reporting `0` for it would read as a resolved root claim.
ROW_KEYS = ("state", "class", "declares", "depth", "prose")
PROVENANCE_KEYS = ("moved_by", "moved_on")


@dataclass(frozen=True)
class Reading:
    """What the corpus says about ONE change — the per-change half of a `Sweep`.

    `declares` is `None` for a field that is not there (or one the strict loader
    refused, which the sweep reads the same way) and a TUPLE otherwise, with the
    empty tuple being the positive `[]` ROOT CLAIM. The `ABSENT`/`[]` distinction
    the whole root-proof doctrine rests on therefore survives into the ledger.
    """

    state: str
    modifier_class: str
    declares: tuple[str, ...] | None
    depth: int | None
    prose_header: bool

    def row(self) -> dict[str, object]:
        """The row body — the DERIVED half, without the provenance keys."""
        body: dict[str, object] = {
            "state": self.state,
            "class": self.modifier_class,
            "declares": (DECLARES_ABSENT if self.declares is None
                         else list(self.declares)),
        }
        if self.declares is not None:
            body["depth"] = self.depth
        body["prose"] = self.prose_header
        return body


def classify_corpus(
    repo_root: str | Path,
    declaring_repository: str = DECLARING_REPOSITORY,
) -> dict[str, Reading]:
    """Change id -> its `Reading`, over the ACTIVE and ARCHIVED corpora both.

    The per-change derivation the ledger records. Reads exactly what
    `corpus_sweep` reads and makes the same allowances — an unreadable proposal
    declares nothing and carries no prose header, because a measurement is not a
    gate and `validate_corpus` is where a refusal is reported.

    TWO KINDS OF REFUSAL, AND THEY LAND DIFFERENTLY. A STRICT-LOADER refusal (a
    duplicate key, an anchor, an alias) raises out of `read_declaration`, so the
    change reads as declaring NOTHING. A SHAPE refusal (`sequenced_after:
    add-other` — a scalar where a sequence is owed) does NOT: the field is
    present, `read_declaration` returns its raw value, and the change is recorded
    as DECLARING, exactly as `corpus_sweep` counts it. That is why a `declares`
    entry can be something no reference grammar would accept, and why the
    renderer quotes an entry that would not read back as itself.
    """
    repo_root = Path(repo_root)
    corpus = corpus_change_dirs(repo_root)
    active = set(active_change_dirs(repo_root))

    keys = {cid: requirement_keys(path) for cid, path in corpus.items()}
    owners: dict[tuple[str, str], set[str]] = {}
    for cid, cid_keys in keys.items():
        for key in cid_keys:
            owners.setdefault(key, set()).add(cid)

    readings: dict[str, Reading] = {}
    for cid, path in sorted(corpus.items()):
        co_modified = any(len(owners[key]) > 1 for key in keys[cid])
        declares: tuple[str, ...] | None = None
        depth: int | None = None
        prose = False
        proposal = path / "proposal.md"
        if proposal.is_file():
            try:
                raw = read_declaration(proposal)
            except SequencedAfterError:
                raw = ABSENT
            if raw is not ABSENT:
                # A NON-LIST value is PRESENT-but-malformed (a `sequenced_after:`
                # key with no value reads as `None`). The sweep counts it as a
                # declaration, so the ledger records it as one and records what
                # it read; `validate-sequenced-after.py` with no flag is what
                # REFUSES it, and stays red independently of this measurement.
                declares = tuple(str(entry) for entry in raw) if isinstance(
                    raw, list) else (str(raw),)
                depth = chain_depth(repo_root, cid,
                                    declaring_repository=declaring_repository)
            try:
                text = proposal.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):  # pragma: no cover
                text = ""
            prose = any(PROSE_HEADER.match(line) for line in text.splitlines())
        readings[cid] = Reading(
            state=STATE_ACTIVE if cid in active else STATE_ARCHIVED,
            modifier_class=CLASS_CO_MODIFIER if co_modified else CLASS_SOLE,
            declares=declares,
            depth=depth,
            prose_header=prose,
        )
    return readings


def sweep_from_readings(readings: dict[str, Reading]) -> Sweep:
    """Derive the whole `Sweep` from the per-change readings — EVERY field.

    No total survives as a hand-carried number: the population, both splits,
    adoption, the prose headers and the DEEPEST DECLARED CHAIN are all folds
    over the rows. The deepest-chain tie-break is the sweep's own — strictly
    greater, over change ids in sorted order — so the derived reading names the
    same change the measurement does.
    """
    ordered = sorted(readings.items())
    active = [cid for cid, r in ordered if r.state == STATE_ACTIVE]
    archived = [cid for cid, r in ordered if r.state == STATE_ARCHIVED]
    co = [cid for cid, r in ordered if r.modifier_class == CLASS_CO_MODIFIER]
    sole = [cid for cid, r in ordered if r.modifier_class == CLASS_SOLE]
    declaring = [cid for cid, r in ordered if r.declares is not None]

    deepest = 0
    deepest_change: str | None = None
    for cid in declaring:
        depth = readings[cid].depth or 0
        if depth > deepest:
            deepest, deepest_change = depth, cid

    return Sweep(
        change_ids=len(ordered),
        active=len(active),
        archived=len(archived),
        co_modified=len(co),
        sole_modifiers=len(sole),
        active_co_modified=len(set(co) & set(active)),
        active_sole=len(set(sole) & set(active)),
        declaring=len(declaring),
        root_claims=sum(1 for cid in declaring if readings[cid].declares == ()),
        prose_headers=sum(1 for _, r in ordered if r.prose_header),
        prose_headers_archived=sum(
            1 for _, r in ordered
            if r.prose_header and r.state == STATE_ARCHIVED),
        deepest_chain=deepest,
        deepest_chain_change=deepest_change,
        declaring_ids=tuple(declaring),
    )


def sweep_mismatches(derived: Sweep, measured: Sweep) -> list[str]:
    """Field-by-field disagreements between two readings of one corpus.

    NAMES THE FIELD AND BOTH VALUES. A bare `assert derived == measured` on a
    fourteen-field dataclass tells an author that something moved and not what,
    which is the failure mode this whole change exists to remove.
    """
    problems: list[str] = []
    for field in Sweep.__dataclass_fields__:
        left, right = getattr(derived, field), getattr(measured, field)
        if left != right:
            problems.append(
                f"derived total mismatch: {field}: ledger-derived {left!r} != "
                f"measured {right!r}")
    return problems


@dataclass(frozen=True)
class Ledger:
    """One parsed ledger file: its rows, the ORDER they were written in, and the
    provenance each row carries."""

    schema_version: object
    kind: object
    seeded_from: object
    order: tuple[str, ...]
    rows: dict[str, dict[str, object]]


def ledger_path(repo_root: str | Path) -> Path:
    return Path(repo_root) / LEDGER_REL


def load_ledger(source: str | bytes | Path) -> Ledger:
    """Parse a ledger file under the STRICT loader's duplicate-key refusal.

    A DUPLICATE CHANGE ID IS THE ONE FAILURE A PERMISSIVE LOADER WOULD HIDE:
    `yaml.safe_load` applies last-duplicate-wins silently, so a ledger carrying
    two rows for one change would show a reviewer the first row and check the
    second — the same defect the realization-axis front-matter loader exists to
    refuse, and the reason this file is read through that loader's own
    `StrictLoader` rather than through `safe_load`.

    The front-matter BYTE CEILING is deliberately NOT applied: it bounds an
    authorization surface parsed out of a document a human wrote, while this
    file's size is a function of how many changes the corpus holds and grows by
    construction. A ceiling here would convert corpus growth into a refusal.
    """
    # A `Path` is a FILE and a `str` is TEXT — the same convention
    # `frontmatter_strict.source_text` takes, so a caller cannot pass a path as
    # a string and have it parsed as a one-line YAML document.
    try:
        text = fms.source_text(source)
    except fms.StrictFrontMatterError as exc:
        raise SequencedAfterError(f"malformed ledger: {exc}") from exc

    for number, line in enumerate(text.split("\n"), start=1):
        if line.startswith("%"):
            raise SequencedAfterError(
                f"malformed ledger: a YAML directive ({line.strip()!r}) at line "
                f"{number}")
    if fms.yaml is None:  # pragma: no cover - pyyaml is a suite dependency
        raise SequencedAfterError(
            "pyyaml is required to read the per-change sweep ledger")
    try:
        fms._scan_refused_constructs(text)  # anchors, aliases, merge keys
        documents = list(fms.yaml.load_all(text, Loader=fms.StrictLoader))
    except fms.StrictFrontMatterError as exc:
        raise SequencedAfterError(f"malformed ledger: {exc}") from exc
    except fms.yaml.YAMLError as exc:
        raise SequencedAfterError(f"malformed ledger: does not parse: {exc}") \
            from exc
    if len(documents) != 1 or not isinstance(documents[0], dict):
        raise SequencedAfterError(
            "malformed ledger: exactly one YAML mapping document is required")
    document = documents[0]

    raw_rows = document.get("rows")
    if not isinstance(raw_rows, dict):
        raise SequencedAfterError(
            "malformed ledger: the `rows:` mapping is missing")
    rows: dict[str, dict[str, object]] = {}
    for change_id, row in raw_rows.items():
        # A NON-STRING KEY IS REFUSED, NOT COERCED. `str()` on the key would
        # collapse two keys YAML holds APART: `123` resolves to an int and
        # `"123"` to a string, so the strict loader's duplicate refusal — which
        # compares keys as YAML typed them — never fires, and the second row
        # then silently overwrites the first. That is the exact
        # last-duplicate-wins defect this loader exists to refuse, reproduced
        # one level down, on the file that IS the pin. A change id is a string
        # by the reference grammar, so nothing legitimate is lost.
        if not isinstance(change_id, str):
            raise SequencedAfterError(
                f"malformed ledger: the row key {change_id!r} is "
                f"{type(change_id).__name__}, not a string; quote it — an "
                "unquoted all-digit or boolean-looking change id is a "
                "different key to YAML than its quoted form, and coercing the "
                "two together would hide a duplicate row")
        if not isinstance(row, dict):
            raise SequencedAfterError(
                f"malformed ledger: the row for {change_id!r} is not a mapping")
        rows[change_id] = row
    order = tuple(raw_rows)
    # THE STRUCTURAL BACKSTOP. The two refusals above should make this
    # unreachable; it is asserted anyway because it is the property every later
    # check depends on — `ledger_problems` compares SETS of ids and would read a
    # collapsed pair as one row that simply agrees.
    if len(rows) != len(order):
        raise SequencedAfterError(
            f"malformed ledger: {len(order)} row keys collapsed to "
            f"{len(rows)} rows; two keys name the same change")
    return Ledger(
        schema_version=document.get("schema_version"),
        kind=document.get("kind"),
        seeded_from=document.get("seeded_from"),
        order=order,
        rows=rows,
    )


class _Missing:
    def __repr__(self) -> str:  # pragma: no cover - trivial
        return "<not in the row>"


_MISSING = _Missing()


def _row_value(row: dict[str, object], key: str) -> object:
    """The row's value for `key`, with the ledger's list/absent spelling
    normalized to the `Reading.row()` shape so the two compare directly."""
    value = row.get(key, _MISSING)
    if key == "declares" and isinstance(value, list):
        return [str(entry) for entry in value]
    return value


def ledger_problems(
    readings: dict[str, Reading],
    ledger: Ledger,
) -> list[str]:
    """Every disagreement between the ledger and the live corpus, NAMED.

    Each problem names the change id and, for a stale value, the key with the
    ledger's reading beside the live one — so an author reads WHICH ROW TO MOVE
    off the failure rather than re-deriving a total to find out.
    """
    problems: list[str] = []
    if ledger.schema_version != LEDGER_SCHEMA_VERSION:
        problems.append(
            f"malformed ledger: schema_version is {ledger.schema_version!r}, "
            f"expected {LEDGER_SCHEMA_VERSION!r}")
    if ledger.kind != LEDGER_KIND:
        problems.append(
            f"malformed ledger: kind is {ledger.kind!r}, expected "
            f"{LEDGER_KIND!r}")

    if list(ledger.order) != sorted(ledger.order):
        out_of_place = [cid for cid, expected
                        in zip(ledger.order, sorted(ledger.order))
                        if cid != expected]
        problems.append(
            "unsorted ledger: the rows are not in change-id order; first out of "
            f"place: {', '.join(out_of_place[:5])}. Sorted order is what keeps "
            "two changes' insertions apart in the diff")

    for change_id in sorted(set(readings) - set(ledger.rows)):
        problems.append(
            f"missing row: {change_id} is in the corpus and has no ledger row; "
            "add one (`validate-sequenced-after.py . --seed-ledger "
            "--moved-by '#<PR>'`)")
    for change_id in sorted(set(ledger.rows) - set(readings)):
        problems.append(
            f"extra row: {change_id} has a ledger row and is in neither the "
            "active nor the archived corpus")

    for change_id in sorted(set(readings) & set(ledger.rows)):
        row = ledger.rows[change_id]
        expected = readings[change_id].row()
        for key in ROW_KEYS:
            if key not in expected:
                if key in row:
                    problems.append(
                        f"stale row: {change_id}: {key}: ledger "
                        f"{row[key]!r}, live <not applicable> (a change that "
                        "declares nothing has no chain depth)")
                continue
            found = _row_value(row, key)
            if found != expected[key]:
                problems.append(
                    f"stale row: {change_id}: {key}: ledger {found!r}, live "
                    f"{expected[key]!r}")
        for key in PROVENANCE_KEYS:
            value = row.get(key)
            ok = (isinstance(value, str) and bool(MOVED_BY.match(value))
                  if key == "moved_by" else is_moved_on(value))
            if not ok:
                problems.append(
                    f"malformed provenance: {change_id}: {key} is {value!r}; "
                    "every row records the pull request that last moved it and "
                    "the date")
        for key in sorted(set(row) - set(ROW_KEYS) - set(PROVENANCE_KEYS),
                          key=str):
            problems.append(
                f"stale row: {change_id}: unknown key {key!r}")
    return problems


def archive_date_problems(
    repo_root: str | Path,
    ledger: Ledger,
    require_equal: bool = False,
) -> list[str]:
    """Archived rows whose `moved_on` CONTRADICTS their directory's date.

    TWO READINGS, AND THE DEFAULT IS THE ONE THAT IS ALWAYS TRUE.

    The default (`require_equal=False`) reports a `moved_on` EARLIER than the
    directory's date prefix. That is a contradiction under any reading: the row
    says `archived`, and a row cannot record its last move BEFORE the archive
    that put it in that state — the flip is the earliest move an archived row
    can carry, and every later move only pushes the date forward. It is also
    exactly the shape a CLI clock running AHEAD of UTC produces (issue #790:
    under `Pacific/Kiritimati` the pinned CLI names tomorrow's directory for
    today's archive), and it was measured CLEAN across all 143 archived rows
    before it was made a gate.

    `require_equal=True` additionally reports every archived row whose
    `moved_on` is merely DIFFERENT from the directory's date. That is the
    stronger reading issue #790 asked for, and it is opt-in rather than the
    default because `release-realization`'s per-subject-row requirement defines
    `moved_on` as the date the ROW last moved — so an archived row legitimately
    moved later by another change carries a later date, and 124 of this corpus's
    143 archived rows do. Requiring equality would report a correct ledger as
    stale. `--strict-archive-dates` is what asks for it.

    NEITHER READING CATCHES A CLOCK RUNNING BEHIND UTC — the direction #780's
    archive actually took — because a `moved_on` LATER than the directory is
    indistinguishable from a legitimate later move. That direction is caught at
    the moment it happens, by `proposal-support.py archive` asserting the name
    the CLI produced, and not here.

    KEPT OUT OF `ledger_problems` DELIBERATELY. That function is what
    `--ledger-diff` gates on AND what `render_ledger` re-runs over its own
    output before returning it, so a finding added there would make the seeder
    refuse to write the very file that repairs the drift.

    Rows are only checked where all four inputs exist: the id is archived in
    the LIVE corpus (an id both active and archived reads as ACTIVE and is
    skipped — that ambiguity is `resolve`'s finding), it has exactly one dated
    directory, it has a row, and THAT ROW SAYS `archived`. A missing row, an
    extra row and a row still saying `active` for an id archived on disk are all
    `ledger_problems`'s to name, and naming one of them twice would send an
    author to two repairs for one fact.
    """
    # READ WITHOUT `classify_corpus`, which walks every declaration and resolves
    # every chain: this arm runs on the PLAIN validator run, and the only two
    # facts it needs are on the directory names. The archived/active test is the
    # classifier's own — an id present in both corpora reads as ACTIVE there, so
    # it reads as active here and is skipped.
    active = set(active_change_dirs(repo_root))
    dates = archive_dates(repo_root)
    problems: list[str] = []
    for change_id, date_on_disk in sorted(dates.items()):
        if change_id in active:
            continue
        row = ledger.rows.get(change_id)
        if row is None:
            continue
        if row.get("state") != STATE_ARCHIVED:
            # A ROW THAT DOES NOT SAY `archived` IS A STALE ROW, AND SAYING SO
            # IS `--ledger-diff`'S JOB. The finding below reads "an archived row
            # cannot record a move that predates the archive that made it
            # archived" — a sentence about a row that CLAIMS to be archived. An
            # `active` row for an id that is archived on disk claims no such
            # thing; it is simply out of date, which `ledger_problems` already
            # reports by name and in the vocabulary whose repair is a re-seed.
            # Reporting it here as an archive-date contradiction would name one
            # fact twice and send the author to two different repairs.
            continue
        moved_on = row.get("moved_on")
        if not is_moved_on(moved_on):
            # `ledger_problems` already reports unreadable provenance by name;
            # comparing a value that is not a date would report the same defect
            # twice, in a vocabulary that sends the author to the wrong repair.
            continue
        if moved_on < date_on_disk:
            problems.append(
                f"archive-date contradiction: {change_id}: the row says it "
                f"last moved on {moved_on!r}, BEFORE the archive directory it "
                f"describes ({date_on_disk!r}); an archived row cannot record "
                f"a move that predates the archive that made it archived")
        elif require_equal and moved_on != date_on_disk:
            problems.append(
                f"archive-date drift: {change_id}: the archived directory is "
                f"dated {date_on_disk!r} and the row's moved_on is "
                f"{moved_on!r}; --strict-archive-dates asks for the stronger "
                f"reading in which an archived row's moved_on IS its archive "
                f"date")
    return problems


def readings_from_ledger(ledger: Ledger) -> dict[str, Reading]:
    """The ledger's OWN reading of the corpus, as `Reading`s.

    This is what makes "the totals are DERIVED from the rows" literal rather
    than a description of a re-classification: the totals a check asserts are
    folded from THESE readings, and `ledger_problems` is what ties them back to
    the live corpus row by row. A row too malformed to read is refused here
    rather than silently defaulted, a defaulted row being an invented reading.
    """
    readings: dict[str, Reading] = {}
    for change_id in sorted(ledger.rows):
        row = ledger.rows[change_id]
        state, klass = row.get("state"), row.get("class")
        if state not in (STATE_ACTIVE, STATE_ARCHIVED):
            raise SequencedAfterError(
                f"malformed ledger: {change_id}: state is {state!r}")
        if klass not in (CLASS_SOLE, CLASS_CO_MODIFIER):
            raise SequencedAfterError(
                f"malformed ledger: {change_id}: class is {klass!r}")
        raw = row.get("declares")
        if raw == DECLARES_ABSENT:
            declares, depth = None, None
        elif isinstance(raw, list):
            declares = tuple(str(entry) for entry in raw)
            depth = row.get("depth")
            if not isinstance(depth, int) or isinstance(depth, bool):
                raise SequencedAfterError(
                    f"malformed ledger: {change_id}: depth is {depth!r} on a "
                    "row that declares")
        else:
            raise SequencedAfterError(
                f"malformed ledger: {change_id}: declares is {raw!r}; expected "
                f"{DECLARES_ABSENT!r} or a sequence")
        prose = row.get("prose")
        if not isinstance(prose, bool):
            raise SequencedAfterError(
                f"malformed ledger: {change_id}: prose is {prose!r}")
        readings[change_id] = Reading(
            state=str(state), modifier_class=str(klass), declares=declares,
            depth=depth, prose_header=prose)
    return readings


#: An entry safe to write UNQUOTED inside a `[...]` flow sequence. Deliberately
#: narrow: bare `add-foo` and repository-qualified `openxFactory:add-foo` — the
#: only two shapes the reference grammar allows — both match, so the ordinary
#: file keeps its stable one-line format and nothing is quoted for show.
_PLAIN_ENTRY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+-]*$")


def _render_entry(entry: str) -> str:
    """One `declares` entry, quoted only when it would not read back as itself.

    A MALFORMED DECLARATION IS A REAL INPUT HERE. `classify_corpus` records what
    the sweep READ, and the sweep reads a shape-refused declaration as a
    declaration (only a strict-LOADER refusal reads as absence), so an entry may
    contain a comma, a bracket or a colon-space. Written raw, `["a, b"]` would
    read back as TWO entries and `["a] b: {c"]` would not parse at all — and the
    seeder is documented as the REPAIR tool, so it must never be the thing that
    writes a file it cannot read.
    """
    if _PLAIN_ENTRY.match(entry):
        try:
            if fms.yaml is not None and fms.yaml.safe_load(entry) == entry:
                return entry
        except Exception:  # pragma: no cover - a scalar PyYAML will not resolve
            pass
    # A JSON string IS a valid YAML double-quoted scalar: the escape set is a
    # subset, so this needs no hand-rolled escaping to get right.
    return json.dumps(entry)


def _render_row(body: dict[str, object], moved_by: str, moved_on: str) -> str:
    parts: list[str] = []
    for key in ROW_KEYS:
        if key not in body:
            continue
        value = body[key]
        if key == "declares" and isinstance(value, list):
            rendered = "[" + ", ".join(_render_entry(e) for e in value) + "]"
        elif isinstance(value, bool):
            rendered = "true" if value else "false"
        else:
            rendered = str(value)
        parts.append(f"{key}: {rendered}")
    # QUOTED THE SAME WAY AS EVERY OTHER SCALAR IN THIS FILE. These two are
    # pattern-validated before they arrive, so hand-quoting them was safe --
    # but "safe because something upstream checked" is the reasoning that made
    # `declares` unsafe, and one quoting strategy is easier to keep right than
    # three. The output is byte-identical for every valid value.
    parts.append("moved_by: " + json.dumps(moved_by))
    parts.append("moved_on: " + json.dumps(moved_on))
    return "{" + ", ".join(parts) + "}"


LEDGER_HEADER = """\
schema_version: {schema_version}
kind: {kind}

# THE PER-CHANGE SWEEP LEDGER — one row per change id, sorted, machine-derived.
#
# What the `sequenced_after` corpus sweep reads ABOUT EACH CHANGE, carried per
# change instead of as a handful of corpus-wide totals. Every total the sweep
# reports is DERIVED from these rows and none is asserted as a literal anywhere,
# so a pull request moves ITS OWN ROW (and a partner's row when its
# `## MODIFIED Requirements` block flips that partner from sole to co-modifier)
# rather than a shared number every other pull request in flight also edits.
#
# HOW TO MOVE YOUR ROW. Run
#   python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#<PR>'
# which rewrites the file from the live corpus, stamps `moved_by`/`moved_on` on
# the rows that ACTUALLY MOVED and leaves every other row's provenance exactly as
# it was. Then read the diff: it is the list of rows your change moved.
#   python3 scripts/validate-sequenced-after.py . --ledger-diff
# prints the same finding set without writing anything, and exits non-zero when
# the ledger is stale.
#
# ROW KEYS
#   state     `active` | `archived` — which corpus the change dir sits in.
#   class     `sole` | `co-modifier` — whether ANY requirement key this change
#             writes (capability + normalized requirement title) is also written
#             by another change in the corpus. Membership is BOOLEAN: sharing
#             three titles with one partner flips a change once, not three times.
#   declares  `absent` when the proposal declares no `sequenced_after:` field —
#             or declares one the strict loader refuses, which the sweep reads
#             the same way and `validate-sequenced-after.py` reports separately.
#             A sequence otherwise, with `[]` the POSITIVE root claim. Absence
#             and `[]` are DIFFERENT FACTS and the ledger keeps them apart.
#   depth     the longest resolvable declared chain from this change, in hops.
#             Present only on a row that declares: a change with no declaration
#             has no chain depth, and `0` would read as a resolved root.
#   prose     whether the proposal carries a legacy free-text `Sequenced-after:`
#             header, which is NOT a machine-readable declaration.
#   moved_by  the pull request that last moved this row's DERIVED keys.
#             AUTHOR-SUPPLIED AND UNVERIFIED: only its SHAPE is checked
#             (`#<digits>`), never that the pull request exists, that it touched
#             this row, or that it had landed when the row was stamped. It is a
#             pointer for a human reading the history, not evidence.
#   moved_on  the date it did, IN UTC. Shape- and calendar-checked, likewise
#             unverified. A row FLIPPING active -> archived takes the date its
#             `archive/<YYYY-MM-DD>-<id>` directory carries, because at that one
#             moment the row's move and the archive are the same act; every
#             other move records the day it happened.
#             `validate-sequenced-after.py` reports any archived row whose
#             moved_on PREDATES its directory, which no move can (issue #790).
#
# FILE KEYS (not row keys)
#   seeded_from  the commit this file was FIRST seeded from, once, as history.
#                It is PRESERVED across re-seeds and therefore goes further out
#                of date with every landing — the ledger is NOT consistent with
#                the corpus at that commit and was never claimed to be.
#                **IT IS NOT THE SHA A RECORD CITES.** A record cites the head
#                at which `--ledger-diff` last ran clean.
#
# WHAT A `Status: record` FILE CITES. Its own change's row(s) and "the ledger is
# consistent with the corpus at <sha>", where <sha> is THE HEAD THE AUTHOR RAN
# `--ledger-diff` ON AND SAW EXIT 0 — never `seeded_from`, and never a
# corpus-wide total. A total moves whenever anyone else lands, so a record that
# quoted one would owe re-derivation on every merge from main; a row moves only
# when the fact it states about that change moves.
#
# THE HAND-WRITTEN NARRATIVE STAYS IN ONE PLACE and it is not this file: the
# MOVEMENT LOG in `tests/sequenced_after/test_sweep.py`, appended only when a
# move is NOT explained by the row diff itself.

seeded_from: {seeded_from}

rows:
"""


def moved_rows(
    readings: dict[str, Reading],
    previous: Ledger | None,
) -> tuple[str, ...]:
    """The change ids whose DERIVED keys a re-seed actually moves, in order.

    THE ONE PLACE THAT DECIDES "did this row move?", so the provenance a re-seed
    stamps and the summary it prints cannot disagree — counting rows that merely
    already carry the same pull request would report unmoved rows as moved. A
    row is moved when it is NEW, when any derived key differs, or when it
    carries a key the row grammar does not know (which a re-seed drops, and
    dropping a key is a move).
    """
    if previous is None:
        return tuple(sorted(readings))
    moved: list[str] = []
    for change_id, reading in sorted(readings.items()):
        row = previous.rows.get(change_id)
        if row is None:
            moved.append(change_id)
            continue
        body = reading.row()
        unchanged = all(_row_value(row, key) == body.get(key, _MISSING)
                        for key in ROW_KEYS)
        extra = set(row) - set(ROW_KEYS) - set(PROVENANCE_KEYS)
        prior_by, prior_on = row.get("moved_by"), row.get("moved_on")
        readable = (isinstance(prior_by, str) and bool(MOVED_BY.match(prior_by))
                    and is_moved_on(prior_on))
        if not (unchanged and not extra and readable):
            moved.append(change_id)
    return tuple(moved)


def flips_to_archived(
    change_id: str,
    reading: Reading,
    previous: Ledger | None,
) -> bool:
    """Is this row FLIPPING `active` -> `archived` in this re-seed?

    THE ONE PLACE THAT DECIDES IT, so the renderer's stamp and the seeder's
    refusal cannot disagree about which rows the archive date applies to — the
    same reason `moved_rows` exists.

    A row with no predecessor is NOT a flip: it is being created for a change
    that is already archived, and its move is its creation. Neither is a row
    that was already `archived` and moved for some other reason.
    """
    if reading.state != STATE_ARCHIVED or previous is None:
        return False
    row = previous.rows.get(change_id)
    return row is not None and row.get("state") == STATE_ACTIVE


def render_ledger(
    readings: dict[str, Reading],
    moved_by: str,
    moved_on: str,
    previous: Ledger | None = None,
    seeded_from: str | None = None,
    archive_dates: dict[str, str] | None = None,
) -> str:
    """Render the whole ledger, PRESERVING the provenance of unmoved rows.

    A row whose derived keys are unchanged keeps the `moved_by`/`moved_on` it
    already carried, so re-seeding after a merge stamps only the rows that
    actually moved and the diff stays readable as "these rows moved, and this
    pull request moved them".

    `archive_dates` — `archive_dates(repo_root)` — makes a row FLIPPING
    `active` -> `archived` take `moved_on` FROM ITS DIRECTORY'S DATE PREFIX
    rather than from the run's date. At the flip, and ONLY there, the two are
    one fact: the row moves BECAUSE the change archived, and the archiving pull
    request seeds its own row in that same act (issue #790).

    EVERY OTHER ARCHIVED ROW KEEPS THE RUN'S DATE, and that is a correction
    taken from review rather than an omission. `release-realization`'s
    "A pinned corpus measurement is carried per subject" requirement defines the
    provenance pair as "the pull request that last moved it AND THE DATE" — the
    date of THAT MOVE. A September pull request that flips an already-archived
    row from sole to co-modifier moved it in September; writing the August
    archive date beside a September `moved_by` would make the pair state two
    different moves. A row created for a change that was ALREADY archived is
    likewise not a flip: its move is its creation, today.

    Passing nothing keeps the run's date for every row, which is what a caller
    with no corpus in hand can honestly say; `validate-sequenced-after.py
    --seed-ledger` always passes them.
    """
    archive_dates = archive_dates or {}
    if not MOVED_BY.match(moved_by):
        raise SequencedAfterError(
            f"--moved-by must be a pull request reference like '#620', not "
            f"{moved_by!r}")
    if not is_moved_on(moved_on):
        raise SequencedAfterError(
            f"--moved-on must be an ISO date, not {moved_on!r}")
    if seeded_from is None and previous is not None:
        seeded_from = (str(previous.seeded_from)
                       if previous.seeded_from is not None else None)
    lines = [LEDGER_HEADER.format(
        schema_version=LEDGER_SCHEMA_VERSION,
        kind=LEDGER_KIND,
        # NOT hand-quoted: `--seeded-from` is caller-supplied and, unlike the
        # provenance pair, is NOT pattern-validated, so a value carrying a
        # quote, a backslash or a newline would have produced a header the
        # round-trip below then refused -- a refusal caused by the renderer
        # rather than by the input.
        seeded_from=json.dumps(seeded_from) if seeded_from else "~",
    )]
    moved = set(moved_rows(readings, previous))
    for change_id, reading in sorted(readings.items()):
        body = reading.row()
        if change_id in moved or previous is None:
            by = moved_by
            on = moved_on
            if flips_to_archived(change_id, reading, previous):
                # THE FLIP TAKES THE ARCHIVE'S DATE, AND OVERWRITES THE RUN'S.
                # At the flip the row's move and the archive are the SAME ACT —
                # the state change this row records is "became archived", and
                # that happened on the day the directory carries — so the pair
                # reads "recorded by <this pull request>, moved on <the archive
                # date>". A `--moved-on` that contradicts it is refused rather
                # than silently overridden (see the seeder), so the rule cannot
                # be worked around by accident.
                #
                # THE SHARP EDGE, NAMED RATHER THAN LEFT TO BE FOUND (Codex
                # round 2, P1): `flips_to_archived` reads only the PREVIOUS row
                # state, so it cannot tell "the archiving change seeded its own
                # row" from "the archiving change forgot, and a later repair is
                # seeding it now". Both are flips, and both take the archive's
                # date — so a delayed repair's row states the repair's pull
                # request beside the original archive's day, and there is no way
                # to record the repair's own date instead.
                #
                # THAT IS DELIBERATE AND IS NOT CHANGED HERE. `moved_on` is the
                # date the ROW MOVED, and the move a flip records is the archive
                # — which happened when the directory says it did, whoever wrote
                # the row down afterwards. The alternative reading (a delayed
                # repair stamps its own day) is defensible and would still pass
                # the validator's archive-date arm, but choosing between them is
                # a reading of `release-realization`'s per-subject-row
                # requirement, not an implementation detail to settle in a fix
                # round: it changes what every future flipped row means. Named
                # in the pull request as a successor.
                on = archive_dates.get(change_id, moved_on)
        else:
            row = previous.rows[change_id]
            by, on = str(row["moved_by"]), str(row["moved_on"])
        lines.append(f"  {change_id}: {_render_row(body, by, on)}\n")
    text = "".join(lines)

    # THE RENDERER PROVES ITS OWN OUTPUT BEFORE RETURNING IT. The seeder is the
    # REPAIR tool, so the one thing it must never do is report "wrote" for a
    # file that does not read back — which is exactly what an unquoted
    # malformed entry used to produce. Re-reading here costs one parse of a
    # file of a few hundred lines and converts a silent corruption into a
    # refusal at the point of writing.
    try:
        parsed = load_ledger(text)
    except SequencedAfterError as exc:
        raise SequencedAfterError(
            f"the rendered ledger does not read back: {exc}") from exc
    problems = ledger_problems(readings, parsed)
    if problems:
        raise SequencedAfterError(
            "the rendered ledger does not read back as what was rendered: "
            + "; ".join(problems[:3]))
    return text
