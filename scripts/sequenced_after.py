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

import importlib.util
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
    out = subprocess.run(
        ["git", "-C", str(path if path.is_dir() else path.parent),
         "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True,
    )
    return Path(out.stdout.strip())


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

    Reads the declaration from the change's `proposal.md` at `ratified_ref` and
    from the current working tree and returns a contested-class problem string
    if they differ (None when retained). The gate ALSO proves the archive does
    not REWRITE declarations: since it compares the entries as authored, any
    date-prefixing, re-pointing or normalization performed on archival would
    register here as a mutation.
    """
    change_path = Path(change_dir)
    proposal = change_path / "proposal.md"
    repo_root = _git_toplevel(change_path)
    proposal_rel = proposal.resolve().relative_to(repo_root.resolve()).as_posix()
    ratified = declaration_at_ref(repo_root, ratified_ref, proposal_rel)
    current = read_declaration(proposal) if proposal.is_file() else ABSENT
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
