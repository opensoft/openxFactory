"""The eighteenth deterministic family: promotion fidelity of archived
spec deltas (`add-promotion-fidelity-check`).

WHAT IT ANSWERS. An OpenSpec change ratifies a spec delta; archiving the
change is supposed to apply that delta to the promoted
`openspec/specs/<capability>/spec.md`. Nothing checked that it did.
`openspec --strict` validates a delta's SHAPE, never its ARRIVAL, and the
four lifecycle families read a packet's headers, never its bodies. So a
ratified requirement could be archived and silently never reach canon, and
the corpus would report itself healthy.

THE CLASS IS NOT HYPOTHETICAL. codexFactory's archived
`2026-08-08-activate-nightly-sweep-council-clearance` ratified a MODIFIED
requirement carrying SIX scenarios; the promoted
`openspec/specs/merge-master-approval/spec.md` carried the title with TWO,
and the archive commit never touched that file. Found by a human reading
carefully, applied by codexFactory PR #85 on 2026-08-24, and recorded in
`docs/archive-record-discrepancies.md` under FU-DOM-CODEX with the sentence
this family exists to retire: "What does NOT close: no check yet compares
archived deltas to promoted specs, so the class stays unreported."

THREE RULES DO THE WORK. The first two are load-bearing against a false
POSITIVE this corpus actually contains; the third was re-cut on 2026-08-24
because its first spelling was load-bearing against a false NEGATIVE it was
also creating:

1. **Latest writer wins.** A requirement is authoritatively stated by the
   MOST RECENT archived delta that touches it, and by that one alone.
   Measured over openxFactory: 478 distinct (capability, requirement) pairs,
   59 of them written by more than one archived change and one written by
   TEN. Checking every writer instead of the latest fires 20 findings where
   the latest-writer rule fires 2 — the other 18 are superseded text that
   canon is CORRECT to have moved past.

2. **RENAMED retires the old title.** `openspec archive` applies a RENAMED
   block before MODIFIED, so a later rename legitimately removes an earlier
   delta's title from canon. Without this rule `ideation-dashboard`'s
   "Staging workbench scoped view" — renamed to "doxBench scoped view" by
   `2026-08-02-add-workbench-integrated-editor-chat` — fires against all
   THREE of its earlier writers.

3. **A delta is exempt only where its own proposal EXPLICITLY declares
   pre-ratification standing.** See `_is_exempt_from_promotion` below; this is
   the C5 exemption and it is keyed on a header the corpus already carries,
   not on a marker invented here. It was narrowed by ruling on 2026-08-24
   (task 4.1, PR #315) after measurement showed the original
   `Status == "ratified"` spelling silently exempting more than fifty
   requirements that nobody had decided to exempt.

THE MEASUREMENT BASIS IS DECLARED, not assumed. `_open_tree` reads either the
checked-out tree (the default, and what every other family measures) or a
repository's own `origin/main`. The nightly runs this ONE family against live
mains by ruling — see `_open_tree` and `basis_notes` for why, and for how the
report is made to say which basis produced its findings.

CLASSIFICATION IS NOW ENFORCING, by ruling and in both of its halves. Every
finding is ERROR, so `--fail-on error` reds on this family, and the family is
registered `contested` in `families.FAMILY_RESOLUTION`, so a finding that
vanishes between reports owes a citation. It launched ADVISORY — WARNING, and
absent from that table — and the flip was taken as ONE decision on 2026-08-24
(Brett, task 4.1's four-question round, PR #315: "ENFORCING, SEQUENCED"),
after the standing population it would have gated on was discharged first.
See `_LAUNCH_SEVERITY` for why the two halves could not move apart, and
`openspec/changes/add-promotion-fidelity-check/tasks.md` §4.2/§4.3 for the
ruling and the discharge evidence.
"""

from __future__ import annotations

import re
from pathlib import Path

from . import ERROR, Finding, Skip, TAXONOMY
from . import corpus

FAMILY = "promotion-fidelity"

# The lifecycle standings that sit BELOW ratification, in the taxonomy
# `docs/document-lifecycle.md` promotes and `doc_health.TAXONOMY` carries.
# A packet whose proposal explicitly declares one of these never claimed the
# approval that obliges promotion, so its deltas are archived design evidence.
# Everything else — `ratified`, the post-ratification standings, an
# unrecognized value, an annotation the taxonomy does not know — is a packet
# that ARCHIVED, and archiving is what this family presumes ratification from.
#
# Split rather than a single set so `RATIFIED_OR_BEYOND` can be asserted to
# exhaust the taxonomy by test: a ninth standing added to the taxonomy and
# forgotten here would otherwise land in the presumed-ratified bucket in
# silence, which is precisely the class of silence the 2026-08-24 ruling
# closed.
PRE_RATIFICATION = frozenset({"brainstorm", "staged", "draft"})
RATIFIED_OR_BEYOND = frozenset({"ratified", "standard", "superseded",
                                "retired", "record"})

# The two measurement bases, named once. `pinned` is the checked-out tree —
# what every other family measures and the default here. `live-main` is this
# family's ruled nightly basis (task 4.1, PR #315).
BASIS_PINNED = "pinned"
BASIS_LIVE_MAIN = "live-main"
LIVE_REF = "origin/main"

# This family's severity, named once. The name records where the value
# STARTED, and the value records the ruling that moved it: ERROR now, so
# `runner.main`'s `--fail-on error` gate (`{CRITICAL, ERROR}`) reds on a
# ratified delta that never reached canon. It launched WARNING, on the
# `staged-topic-template` precedent ("reports non-conformance and
# DELIBERATELY NEVER BLOCKS A GATE"), because nobody had yet measured what
# the domain factories' archives would say.
#
# The family is ALSO registered `contested` in `families.FAMILY_RESOLUTION`,
# and that is the less obvious half of the SAME decision — the two cannot
# move apart. `report.uncited_resolutions` turns a contested finding that
# VANISHES between reports into an ERROR under the `uncited-resolution`
# family. Under the advisory launch that was a back door: the nightly would
# have gone red the first time anyone actually promoted a delta this family
# reported, on the very run that proved the advisory launch worked. Under
# enforcement it is the discipline the ruling wanted — the remedy here is a
# governance act, not a mechanical edit, so a finding that disappears owes a
# citation. Taking either half alone produces a family nobody chose: severity
# alone gates without the disposition discipline; the contested class alone
# gates through `uncited-resolution`, under a family name that does not say
# what happened.
#
# FLIPPED 2026-08-24 by ruling — Brett, task 4.1's four-question round
# (PR #315), verbatim "ENFORCING, SEQUENCED" — and sequenced behind the
# discharge of the standing population, per `govern-openspec-corpus-
# membership`'s rule that "a gate that goes red on the commit that
# introduces it teaches everyone to route around the gate". The discharge
# evidence is tasks.md §4.3.
_LAUNCH_SEVERITY = ERROR

_SECTION = re.compile(r"^##\s+(ADDED|MODIFIED|REMOVED|RENAMED)\s+Requirements\s*$")
_REQUIREMENT = re.compile(r"^###\s+Requirement:\s*(.+?)\s*$")
_SCENARIO = re.compile(r"^####\s+Scenario:\s*(.+?)\s*$")
# The RENAMED block's two-line shape, as `openspec` writes and reads it:
#   - FROM: `### Requirement: Staging workbench scoped view`
#   - TO: `### Requirement: doxBench scoped view`
# Backticks are optional so a packet that omits them still parses.
_RENAME_FROM = re.compile(r"^-\s+FROM:\s*`?###\s+Requirement:\s*(.+?)`?\s*$")
_RENAME_TO = re.compile(r"^-\s+TO:\s*`?###\s+Requirement:\s*(.+?)`?\s*$")

_ARCHIVE_DATE = re.compile(r"^(\d{4}-\d{2}-\d{2})-")

CHECKED_OPS = ("ADDED", "MODIFIED", "REMOVED")


def norm(title: str) -> str:
    """The comparison spelling of a requirement or scenario title.

    Whitespace-collapsed and casefolded, and NOTHING ELSE. A wider
    normalization (stripping backticks, punctuation, trailing periods) would
    quietly forgive the exact class of drift this family exists to report —
    the codex gap included a `tier-2`-to-`tier 2` normalization INSIDE a
    scenario body, and a rule loose enough to ignore punctuation in a title
    is a rule that would have ignored that too. Casefolding survives because
    a title's case is a rendering choice no reader acts on differently.
    """
    return " ".join(title.split()).casefold()


class DeltaRequirement:
    """One `### Requirement:` block inside one archived delta file."""

    __slots__ = ("op", "title", "scenarios", "seq")

    def __init__(self, op: str, title: str, seq: int):
        self.op = op
        self.title = title
        self.scenarios: list[str] = []
        self.seq = seq


def parse_delta(text: str) -> tuple[list[DeltaRequirement], list[tuple[str, str]]]:
    """`(requirements, renames)` from one `specs/<cap>/spec.md` delta file.

    Requirements are returned in file order with their operation and their
    own scenario titles; renames as `(from_title, to_title)` pairs. A
    `#### Scenario:` line before any `### Requirement:` belongs to nothing
    and is dropped rather than attached to whatever came before.
    """
    requirements: list[DeltaRequirement] = []
    renames: list[tuple[str, str]] = []
    op: str | None = None
    current: DeltaRequirement | None = None
    pending_from: str | None = None
    for line in text.splitlines():
        m = _SECTION.match(line)
        if m:
            op, current, pending_from = m.group(1), None, None
            continue
        if op is None:
            continue
        if op == "RENAMED":
            m = _RENAME_FROM.match(line)
            if m:
                pending_from = m.group(1)
                continue
            m = _RENAME_TO.match(line)
            if m and pending_from is not None:
                renames.append((pending_from, m.group(1)))
                pending_from = None
                continue
        m = _REQUIREMENT.match(line)
        if m:
            current = DeltaRequirement(op, m.group(1), len(requirements))
            requirements.append(current)
            continue
        m = _SCENARIO.match(line)
        if m and current is not None:
            current.scenarios.append(m.group(1))
    return requirements, renames


def parse_promoted(text: str) -> dict[str, list[str]]:
    """`{requirement_norm: [scenario_norm, ...]}` from a promoted spec.

    The SAME two heading regexes the delta reader uses, deliberately: a
    second grammar for the same headings is how two readers of one document
    come to disagree about whether it says something (the lesson
    `align-status-reader-to-real-lines` paid for over lifecycle headers).
    """
    promoted: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        m = _REQUIREMENT.match(line)
        if m:
            current = norm(m.group(1))
            promoted.setdefault(current, [])
            continue
        m = _SCENARIO.match(line)
        if m and current is not None:
            promoted[current].append(norm(m.group(1)))
    return promoted


def _archive_date(folder: str) -> str:
    """The `YYYY-MM-DD` prefix an archived packet folder carries, or `""`.

    A folder without the prefix sorts BEFORE every dated one, which is the
    conservative direction: an undated legacy packet is never treated as the
    latest writer over a dated successor.
    """
    m = _ARCHIVE_DATE.match(folder)
    return m.group(1) if m else ""


_ARCHIVE_PREFIX = "openspec/changes/archive/"


class WorkingTree:
    """The repository as it is CHECKED OUT — the basis every family reads.

    In an aggregation run that is the submodule at its committed PIN, which is
    the whole reason `GitRefTree` exists beside it.
    """

    __slots__ = ("_root", "basis", "detail", "ref")

    def __init__(self, repo_path: Path, detail: str = ""):
        self._root = repo_path
        self.basis = BASIS_PINNED
        self.detail = detail
        self.ref = None

    def has_archive(self) -> bool:
        return (self._root / "openspec" / "changes" / "archive").is_dir()

    def archive_changes(self) -> list[str]:
        archive = self._root / "openspec" / "changes" / "archive"
        if not archive.is_dir():
            return []
        return sorted(p.name for p in archive.iterdir() if p.is_dir())

    def delta_specs(self, change: str) -> list[str]:
        specs = (self._root / "openspec" / "changes" / "archive" / change
                 / "specs")
        if not specs.is_dir():
            return []
        return sorted(p.relative_to(self._root).as_posix()
                      for p in specs.glob("*/spec.md"))

    def read(self, rel: str) -> str | None:
        path = self._root / rel
        if not path.is_file():
            return None
        return path.read_text(encoding="utf-8", errors="replace")


class GitRefTree:
    """One repository's `origin/main`, read WITHOUT touching the checkout.

    Every path comes from a single `git ls-tree -r` of the ref, and every body
    from `git show <ref>:<path>`. Nothing is checked out, nothing is reset, and
    no other family's input moves — which is the constraint the ruling put on
    this basis: THIS family measures live mains, and only this family.
    """

    __slots__ = ("_repo", "_git", "_paths", "basis", "detail", "ref", "sha")

    def __init__(self, repo_path: Path, git, ref: str, sha: str,
                 paths: list[str]):
        self._repo = repo_path
        self._git = git
        self._paths = frozenset(paths)
        self.basis = BASIS_LIVE_MAIN
        self.ref = ref
        self.sha = sha
        self.detail = f"{ref} {sha[:12]}"

    def _under_archive(self) -> set[str]:
        names = set()
        for path in self._paths:
            if path.startswith(_ARCHIVE_PREFIX):
                head = path[len(_ARCHIVE_PREFIX):].split("/", 1)
                if len(head) == 2:
                    names.add(head[0])
        return names

    def has_archive(self) -> bool:
        return any(p.startswith(_ARCHIVE_PREFIX) for p in self._paths)

    def archive_changes(self) -> list[str]:
        return sorted(self._under_archive())

    def delta_specs(self, change: str) -> list[str]:
        prefix = f"{_ARCHIVE_PREFIX}{change}/specs/"
        return sorted(p for p in self._paths
                      if p.startswith(prefix) and p.endswith("/spec.md")
                      and p.count("/", len(prefix)) == 1)

    def read(self, rel: str) -> str | None:
        # The membership test first: a promoted spec that does not exist is
        # the COMMON case here (a capability never promoted at all is one of
        # this family's findings), and paying a subprocess to be told so on
        # every miss would make the live basis cost what it does not need to.
        if rel not in self._paths:
            return None
        return self._git.show_blob(self._repo, self.ref, rel)


def _open_tree(repo_path: Path, git, requested: str):
    """The tree this family reads for one repository, and how it says so.

    RULED 2026-08-24 (Brett, four-question round; task 4.1, PR #315): **the
    nightly measures LIVE MAINS for this family, and for this family alone.**
    The evidence was a corpus-wide run against the aggregation's committed
    PINS, where this family's coverage collapsed — 0% in three repositories —
    and where it could not see the very gap (#301) that a lagging codexFactory
    pin was hiding. A promotion gap is a fact about a repository's own main;
    measuring it through a pin reports the state of the PIN, and reports it in
    the vocabulary of the repository, which is the shape of a false negative.

    THE FALL-BACK IS LOUD, NEVER SILENT. `origin/main` has to be present
    locally (the nightly fetches it; a developer checkout usually has it; a
    fresh shallow clone may not). Where it is not, this repository is read
    from its checkout and `basis_notes` names it as having FALLEN BACK. The
    alternative — refusing to measure the repository at all — trades a stale
    true positive for silence, and silence is the failure mode the ruling
    exists to close.
    """
    if requested != BASIS_LIVE_MAIN:
        return WorkingTree(repo_path)
    resolve = getattr(git, "resolve_ref", None)
    ls_tree = getattr(git, "ls_tree_paths", None)
    if resolve is None or ls_tree is None:
        return WorkingTree(repo_path, "FELL BACK to the pinned checkout — "
                                      "this run cannot read git refs")
    sha = resolve(repo_path, LIVE_REF)
    if sha is None:
        return WorkingTree(repo_path, f"FELL BACK to the pinned checkout — "
                                      f"{LIVE_REF} is not present locally")
    paths = ls_tree(repo_path, LIVE_REF, "openspec")
    if paths is None:
        return WorkingTree(repo_path, f"FELL BACK to the pinned checkout — "
                                      f"{LIVE_REF} {sha[:12]} is unreadable")
    return GitRefTree(repo_path, git, LIVE_REF, sha, paths)


def normalize_basis(value: str) -> str:
    """The ONE choke point every reader of the basis value must share.

    `runner.build_context` (deciding whether the headline deviation line
    says "measured against live main") and `requested_basis` below (deciding
    which TREE the family actually reads) used to each answer that question
    on their own: `build_context` treated anything other than `'pinned'` as
    live-main for the headline, while this function's old body silently
    coerced anything unrecognized BACK to `'pinned'`. A value neither of
    them recognized — a typo, or a basis built programmatically rather than
    through the CLI's own `argparse` `choices=` gate — could therefore make
    the headline claim live-main while the family measured pinned, or the
    reverse. Routing BOTH call sites through this one function closes that:
    they either agree, because they read the same normalization, or the run
    aborts before either one has decided anything.

    Raises `ValueError` for anything but `BASIS_PINNED` or `BASIS_LIVE_MAIN`.
    The CLI can never trigger this — `argparse`'s `choices=` rejects an
    unknown `--promotion-fidelity-basis` before `build_context` runs — so a
    value that reaches here unrecognized can only have arrived through a
    hand-built `Context`, and it fails loudly rather than being silently
    reinterpreted as either basis.
    """
    if value not in (BASIS_PINNED, BASIS_LIVE_MAIN):
        raise ValueError(
            f"unknown promotion-fidelity basis {value!r}; expected "
            f"{BASIS_PINNED!r} or {BASIS_LIVE_MAIN!r}")
    return value


def requested_basis(ctx) -> str:
    """The basis this run asked for. Absent the field, the pinned checkout —
    so a Context built before this option existed behaves as it always did.

    Reads through `normalize_basis`, the choke point `runner.build_context`
    also reads through, so the two can never disagree about what an unknown
    value means.
    """
    value = getattr(ctx, "promotion_fidelity_basis", BASIS_PINNED)
    return normalize_basis(value)


def repo_trees(ctx) -> list[tuple[str, Path, object]]:
    """`(repo, path, tree)` for every repository in scope that has an archive.

    Called twice per run — once by the family, once by `basis_notes` — because
    the note must describe the basis the findings ACTUALLY came from, and the
    only way to be sure of that is to resolve it the same way. Resolution is
    one `rev-parse` plus one `ls-tree` per repository in live mode and no
    subprocess at all in the pinned default, so the second call is cheap.
    """
    out = []
    basis = requested_basis(ctx)
    for repo, path in sorted(ctx.repo_paths.items()):
        tree = _open_tree(Path(path), ctx.git, basis)
        if tree.has_archive():
            out.append((repo, Path(path), tree))
    return out


def basis_notes(ctx) -> list[str]:
    """The report lines that say WHICH TREE produced this family's findings.

    A reader must never mistake a live-main finding for a pinned one: the two
    answer different questions, and the ruling that separated them is only
    honoured if the report carries the separation. So the basis is stated on
    every run, including the pinned default — a line that appears only in the
    unusual case is a line nobody has learnt to look for.
    """
    basis = requested_basis(ctx)
    trees = repo_trees(ctx)
    if basis == BASIS_PINNED:
        return ["Basis: the pinned checkout — the same tree every other "
                "family measures."]
    notes = ["Basis: each repository's live `origin/main`, RULED for this "
             "family alone (task 4.1, PR #315); every other family in this "
             "report measures the pinned checkout."]
    for repo, _path, tree in trees:
        notes.append(f"- {repo}: {tree.detail}")
    if not trees:
        notes.append("- no repository in scope carries an archive on either "
                     "basis")
    return notes


def declared_standing(status: str | None) -> str | None:
    """The taxonomy standing a `Status:` value declares, or None.

    `corpus.STATUS_RE` captures the WHOLE rest of the header line, so a
    packet that annotates its standing — `Status: ratified (superseded by
    <change>)`, the shape hermes-install's archive carries — parses to a value
    no equality test against a taxonomy word will ever match. The leading
    token is what the header declares; the annotation is prose about it.

    Applied SYMMETRICALLY, which is the whole reason it is one function: an
    annotated `draft` declares `draft` for exactly the same reason an
    annotated `ratified` declares `ratified`. A second grammar for the two
    directions is how one reader comes to disagree with itself about what a
    header says.

    Punctuation the corpus wraps headers in (`` ` ``, `*`, `_`) is stripped;
    the value is casefolded. An unrecognized word returns None rather than
    itself, so a typo can never be mistaken for a standing.
    """
    if not status:
        return None
    token = status.split()[0].strip("`*_").casefold()
    return token if token in TAXONOMY else None


def _is_exempt_from_promotion(tree, change: str) -> bool:
    """Does this archived packet EXPLICITLY disclaim the ratification that
    would have obliged promotion?

    THE C5 EXEMPTION, keyed on the header the record actually uses rather
    than on a marker invented for this family. `docs/archive-record-
    discrepancies.md` C5 records `2026-06-26-enable-live-openxfactory` as
    the one archived change whose spec deltas were DELIBERATELY not promoted
    — "archived by Brett's own PR #28 with `--skip-specs`, retaining the
    four spec deltas as archived design evidence rather than promoting
    them" — and its 2026-08-23 supersession addendum backfilled exactly one
    header onto it to say so in the corpus's own vocabulary:
    `Status: draft`, with no ratification citation, because "`draft` records
    the honest value this folder has always supported: never ratified".

    RULED 2026-08-24 (Brett, four-question round; task 4.1, PR #315):
    **an archived packet is PRESUMED ratified by the act of archiving, and the
    exemption applies ONLY where the header explicitly parses to `draft` or a
    lower taxonomy standing.** The first cut asked the opposite question —
    "does the status read exactly `ratified`?" — and that spelling made the
    exemption a FALSE-NEGATIVE CHANNEL rather than a narrow record:

    - an ANNOTATED ratification (`Status: ratified (superseded ...)`) is not
      the string `ratified`, so it was exempt;
    - a packet carrying NO `Status:` header at all was exempt, which meant
      the corpus could buy silence by omitting a header.

    MEASURED, on live `origin/main`s, both before the ruling and again on
    realization. Four packets were exempt for no decision anyone took, and
    with them 54 requirements: hermes-install's ANNOTATED
    `2026-07-19-implement-three-layer-hermes-runtime-foundation` (23) and
    HEADERLESS `2026-07-22-add-seed-layer-content` (4), and
    medx-roottruth-install's headerless `2026-08-10-add-runtime-scaffold`
    (16) and `2026-08-11-add-tiered-ingestion-and-probe` (11). Those two
    repositories reported zero findings at 57.8% and 0% coverage, and
    reported it as health.

    (The ruling's own record says 57, from a run taken at a different
    reference point. The packets and the shapes are the same four; the count
    here is the one this implementation re-derived. Both are kept — see
    tasks §4.1.)

    THE RELAXATION COST MEASURED ZERO. 88 of openxFactory's 89
    delta-carrying packets read exactly `ratified` and the 89th is C5's
    `Status: draft`, so both spellings give the same two findings; across
    every other reachable repository the examined-requirement count and the
    finding count are unchanged. +54 requirements examined, +0 findings
    anywhere.

    THE PRESUMPTION IS THE CONSERVATIVE DIRECTION NOW, and it was not before:
    an unexamined ratified delta is a governance gap reporting itself healthy,
    while a wrongly examined one is a finding that a `draft` header or a cited
    disposition retires. (The relaxation was ruled while this family was still
    advisory, so that finding was a WARNING then and is an ERROR now — the
    asymmetry the argument turns on is unchanged, but the cost of being on the
    wrong side of it is not, which is why both retiring routes are named.)
    A packet with no proposal at all, or with
    a status the taxonomy does not recognize, is therefore examined —
    `fam_status_validity` already reports the missing or invalid header
    itself, over the lifecycle scan set `govern-openspec-corpus-membership`
    declared, so nothing here has to double as that check.

    The status is read through `corpus.parse_status` — the ONE lifecycle
    header reader — never through a private regex.
    """
    text = tree.read(f"openspec/changes/archive/{change}/proposal.md")
    if text is None:
        return False
    return declared_standing(corpus.parse_status(text)) in PRE_RATIFICATION


class Writer:
    """One archived delta's statement about one (capability, requirement)."""

    __slots__ = ("change", "capability", "op", "title", "scenarios",
                 "delta_rel", "seq")

    def __init__(self, change: str, capability: str, op: str, title: str,
                 scenarios: list[str], delta_rel: str, seq: int):
        self.change = change
        self.capability = capability
        self.op = op
        self.title = title
        self.scenarios = scenarios
        self.delta_rel = delta_rel
        self.seq = seq


def _collect_writers(tree) -> dict[tuple[str, str], list[Writer]]:
    """Every archived delta statement in one repo, grouped by its target.

    A RENAMED pair contributes a `RENAMED` writer against the OLD title —
    which is how a rename retires it — and nothing against the new one: the
    same change's MODIFIED block already carries the new header, because
    `openspec archive` requires it to.

    Reads through a TREE (`WorkingTree` or `GitRefTree`) rather than through
    `Path` directly, so the live-main basis is a different reader of the same
    rules instead of a second copy of the rules.
    """
    writers: dict[tuple[str, str], list[Writer]] = {}
    for change in tree.archive_changes():
        deltas = tree.delta_specs(change)
        if not deltas or _is_exempt_from_promotion(tree, change):
            continue
        for rel in deltas:
            capability = rel.rsplit("/", 2)[-2]
            body = tree.read(rel)
            if body is None:
                continue
            requirements, renames = parse_delta(body)
            # Renames first, and given a sequence number below every
            # requirement in the same file: `openspec archive` applies
            # RENAMED before MODIFIED, so within one change the rename is
            # the earlier statement.
            for i, (old, _new) in enumerate(renames):
                writers.setdefault((capability, norm(old)), []).append(
                    Writer(change, capability, "RENAMED", old, [],
                           rel, -len(renames) + i))
            for req in requirements:
                writers.setdefault((capability, norm(req.title)), []).append(
                    Writer(change, capability, req.op, req.title,
                           req.scenarios, rel, req.seq))
    return writers


def _authoritative(writers: list[Writer], tie_rank) -> Writer:
    """The one writer that speaks for a (capability, requirement) today.

    LATEST WRITER WINS, ordered by the archive folder's `YYYY-MM-DD` prefix.
    Two archived changes CAN share a date — nineteen (capability,
    requirement) pairs in openxFactory are written twice or more on their
    latest date — so the tie-break is not decoration:

    - first the packet's own ARCHIVE-COMMIT ORDER, from git, which is the
      real answer to "which of these landed last";
    - then, only where git cannot answer (a shallow clone, an unborn
      repository, a fixture tree with no history), the folder name
      ascending, which is deterministic and needs no history;
    - then file order within one change.

    Folder-name order alone was measured against real archive-commit order
    across all nineteen tie groups and DISAGREED on six of them, so it is
    the fallback and not the rule. The three ties where the choice changes a
    finding all sit in the thirteen where the two agree — which is a fact
    about today's corpus, not a licence to rest the rule on it.
    """
    latest = max(_archive_date(w.change) for w in writers)
    tied = [w for w in writers if _archive_date(w.change) == latest]
    if len(tied) == 1:
        return tied[0]
    return max(tied, key=lambda w: (tie_rank(w.change), w.change, w.seq))


def _tie_ranker(repo_path: Path, git, ref: str | None = None):
    """A memoized `change -> sortable archive-commit rank` for tie-breaking.

    Resolved LAZILY and only for the changes a tie actually involves: a full
    sweep would spend one `git log` per archived packet on every run to
    answer a question nineteen pairs ask.

    `ref` is the commit whose history is walked, and it is the SAME ref the
    statements were read from. A live-main run that broke its ties on HEAD's
    history would be deciding "which packet archived last" in one tree about
    statements taken from another — the two agreeing today is not a rule.
    """
    cache: dict[str, int] = {}
    reader = getattr(git, "first_commit_timestamp", None)

    def rank(change: str) -> int:
        if change not in cache:
            stamp = None
            if reader is not None:
                stamp = reader(
                    repo_path, f"openspec/changes/archive/{change}", ref=ref)
            cache[change] = -1 if stamp is None else int(stamp)
        return cache[change]

    return rank


def _load_dispositions(ctx) -> set[tuple[str, str, str | None]]:
    """Recorded dispositions for this family, as `(repo, path, requirement)`.

    THE EXISTING MECHANISM, not a new one: `health/dispositions.yaml` at the
    aggregation root, entries keyed by `family`/`repo`/`path` and carrying a
    `cite`, exactly as `runner.main` already reads them for the
    uncited-resolution rule and as the neutrality lane already reads them to
    suppress. An entry without a `cite` records no decision and suppresses
    nothing.

    ONE EXTENSION, in the shape the neutrality lane's `content_sha256`
    already set: an optional `requirement:` key narrows an entry to a single
    requirement inside the delta file. Absent it, the entry disposes every
    finding this family raises against that path — which is the coarser
    behaviour every other family's entry already has.

    THE SINGLE-REPO CAVEAT, stated rather than discovered: this file lives
    at the AGGREGATION root and a `--single-repo` self-gate run has no
    aggregation root, so no disposition applies in that scope. That is the
    pre-existing shape of the mechanism (`runner.main` guards the same read
    with `if ctx.agg_root`), not something this family chose.
    """
    out: set[tuple[str, str, str | None]] = set()
    agg_root = getattr(ctx, "agg_root", None)
    if agg_root is None:
        return out
    path = Path(agg_root) / "health" / "dispositions.yaml"
    if not path.is_file():
        return out
    try:
        import yaml
    except ImportError:
        return out
    try:
        entries = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    except (OSError, yaml.YAMLError):
        return out
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("family") != FAMILY:
            continue
        if not entry.get("cite"):
            continue
        repo, doc_path = entry.get("repo"), entry.get("path")
        if not isinstance(repo, str) or not isinstance(doc_path, str):
            continue
        requirement = entry.get("requirement")
        out.add((repo, doc_path,
                 norm(requirement) if isinstance(requirement, str) else None))
    return out


def _disposed(dispositions, repo: str, path: str, title: str) -> bool:
    return ((repo, path, None) in dispositions
            or (repo, path, norm(title)) in dispositions)


_ACTION = ("apply the ratified delta to the promoted spec through an "
           "OpenSpec change, or record the non-promotion as deliberate")


def _finding(repo: str, writer: Writer, rule: str) -> Finding:
    return Finding(_LAUNCH_SEVERITY, FAMILY, repo, writer.delta_rel,
                   rule, _ACTION)


def fam_promotion_fidelity(ctx):
    """Every authoritative archived delta statement, against promoted canon.

    A finding lands on the DELTA's own path, not on the promoted spec's.
    The delta is the document making the claim that went unmet, it is an
    archived record whose path is stable, and it is what a disposition needs
    to key on; the promoted spec it failed to reach is named in the rule
    text, which is what a reader acts on.
    """
    scoped = repo_trees(ctx)
    if not scoped:
        return Skip(FAMILY, "no repository in scope carries an OpenSpec "
                            "change archive")

    dispositions = _load_dispositions(ctx)
    findings: list[Finding] = []
    for repo, repo_path, tree in scoped:
        writers = _collect_writers(tree)
        if not writers:
            continue
        tie_rank = _tie_ranker(repo_path, ctx.git, tree.ref)
        promoted_cache: dict[str, dict[str, list[str]] | None] = {}

        def promoted(capability: str, tree=tree):
            if capability not in promoted_cache:
                body = tree.read(
                    f"openspec/specs/{capability}/spec.md")
                promoted_cache[capability] = (
                    parse_promoted(body) if body is not None else None)
            return promoted_cache[capability]

        for key in sorted(writers):
            writer = _authoritative(writers[key], tie_rank)
            if writer.op not in CHECKED_OPS:
                continue  # a RENAMED writer retires the old title, nothing more
            if _disposed(dispositions, repo, writer.delta_rel, writer.title):
                continue
            canon = promoted(writer.capability)
            spec_rel = f"openspec/specs/{writer.capability}/spec.md"
            if writer.op == "REMOVED":
                if canon is not None and key[1] in canon:
                    findings.append(_finding(
                        repo, writer,
                        f"ratified REMOVED requirement {writer.title!r} is "
                        f"still present in {spec_rel}"))
                continue
            if canon is None:
                findings.append(_finding(
                    repo, writer,
                    f"ratified {writer.op} requirement {writer.title!r} "
                    f"targets capability {writer.capability!r}, which has no "
                    f"promoted spec"))
                continue
            if key[1] not in canon:
                findings.append(_finding(
                    repo, writer,
                    f"ratified {writer.op} requirement {writer.title!r} is "
                    f"absent from {spec_rel}"))
                continue
            missing = [s for s in writer.scenarios
                       if norm(s) not in canon[key[1]]]
            if missing:
                shown = ", ".join(repr(s) for s in missing[:3])
                if len(missing) > 3:
                    shown += f", +{len(missing) - 3} more"
                findings.append(_finding(
                    repo, writer,
                    f"requirement {writer.title!r} reached {spec_rel} without "
                    f"{len(missing)} of its {len(writer.scenarios)} ratified "
                    f"scenarios: {shown}"))
    return findings
