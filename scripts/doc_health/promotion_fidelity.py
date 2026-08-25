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

THREE RULES DO THE WORK, and each one is load-bearing against a false
positive this corpus actually contains:

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

3. **A delta is checked only where its own proposal claims ratification.**
   See `_is_ratified_for_promotion` below; this is the C5 exemption and it
   is keyed on a header the corpus already carries, not on a marker invented
   here.

CLASSIFICATION AT LAUNCH IS ADVISORY, deliberately. Every finding is
WARNING, so `--fail-on error` (and `--fail-on critical`) cannot red on this
family, and the family is deliberately ABSENT from
`families.FAMILY_RESOLUTION` — see `_LAUNCH_SEVERITY`'s note for why
registering it as `contested` would have re-opened an enforcement path
through the back door. The flip to enforcing is an open task in
`openspec/changes/add-promotion-fidelity-check/tasks.md`, not a judgement
call available here.
"""

from __future__ import annotations

import re
from pathlib import Path

from . import Finding, Skip, WARNING
from . import corpus

FAMILY = "promotion-fidelity"

# The launch severity, named once. Advisory means WARNING: `runner.main`'s
# gate is `{CRITICAL}` or `{CRITICAL, ERROR}`, so a WARNING family reports
# without reddening anything. The `staged-topic-template` family is the
# house precedent for exactly this shape ("reports non-conformance and
# DELIBERATELY NEVER BLOCKS A GATE").
#
# The family is ALSO absent from `families.FAMILY_RESOLUTION`, which is the
# less obvious half of the same decision. A `contested` resolution class
# would be the semantically right label — the remedy here is a governance
# act, not a mechanical edit — but `report.uncited_resolutions` turns a
# contested finding that VANISHES between reports into an ERROR under the
# `uncited-resolution` family. That would mean the first time anyone
# actually promoted a delta this family reported, the nightly went red: an
# enforcement channel arriving through the back door on the very run that
# proves the advisory launch worked. Severity and resolution class flip
# TOGETHER, once, by ruling.
_LAUNCH_SEVERITY = WARNING

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


def _is_ratified_for_promotion(change_dir: Path) -> bool:
    """Did this archived change's own proposal claim ratification?

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

    So the rule is simply that a delta is checked for arrival only where its
    own proposal claims the ratification that would have obliged the
    arrival. A `draft` packet's deltas are archived design evidence and this
    family says nothing about them.

    MEASURED, because an exemption that swallows the population is worse
    than none: across openxFactory's 89 archived changes carrying deltas, 88
    proposals read `ratified` and exactly ONE reads `draft` — C5's. The
    exemption is as narrow as the record it implements.

    A packet with no `proposal.md` at all, or with no `Status:` header in
    its window, makes no claim of ratification and is therefore NOT checked.
    That is the same conservative direction as the rest of this family, and
    it is not a silent hole: `fam_status_validity` already reports a
    proposal missing its status header, over the lifecycle scan set
    `govern-openspec-corpus-membership` declared.

    The status is read through `corpus.parse_status` — the ONE lifecycle
    header reader — never through a private regex.
    """
    proposal = change_dir / "proposal.md"
    if not proposal.is_file():
        return False
    return corpus.parse_status(
        proposal.read_text(encoding="utf-8", errors="replace")) == "ratified"


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


def _collect_writers(repo_path: Path) -> dict[tuple[str, str], list[Writer]]:
    """Every archived delta statement in one repo, grouped by its target.

    A RENAMED pair contributes a `RENAMED` writer against the OLD title —
    which is how a rename retires it — and nothing against the new one: the
    same change's MODIFIED block already carries the new header, because
    `openspec archive` requires it to.
    """
    writers: dict[tuple[str, str], list[Writer]] = {}
    archive = repo_path / "openspec" / "changes" / "archive"
    if not archive.is_dir():
        return writers
    for change_dir in sorted(p for p in archive.iterdir() if p.is_dir()):
        if not _is_ratified_for_promotion(change_dir):
            continue
        specs = change_dir / "specs"
        if not specs.is_dir():
            continue
        for delta in sorted(specs.glob("*/spec.md")):
            capability = delta.parent.name
            rel = delta.relative_to(repo_path).as_posix()
            requirements, renames = parse_delta(
                delta.read_text(encoding="utf-8", errors="replace"))
            # Renames first, and given a sequence number below every
            # requirement in the same file: `openspec archive` applies
            # RENAMED before MODIFIED, so within one change the rename is
            # the earlier statement.
            for i, (old, _new) in enumerate(renames):
                writers.setdefault((capability, norm(old)), []).append(
                    Writer(change_dir.name, capability, "RENAMED", old, [],
                           rel, -len(renames) + i))
            for req in requirements:
                writers.setdefault((capability, norm(req.title)), []).append(
                    Writer(change_dir.name, capability, req.op, req.title,
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


def _tie_ranker(repo_path: Path, git):
    """A memoized `change -> sortable archive-commit rank` for tie-breaking.

    Resolved LAZILY and only for the changes a tie actually involves: a full
    sweep would spend one `git log` per archived packet on every run to
    answer a question nineteen pairs ask.
    """
    cache: dict[str, int] = {}
    reader = getattr(git, "first_commit_timestamp", None)

    def rank(change: str) -> int:
        if change not in cache:
            stamp = None
            if reader is not None:
                stamp = reader(
                    repo_path, f"openspec/changes/archive/{change}")
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
    scoped = [(repo, Path(path)) for repo, path in sorted(ctx.repo_paths.items())
              if (Path(path) / "openspec" / "changes" / "archive").is_dir()]
    if not scoped:
        return Skip(FAMILY, "no repository in scope carries an OpenSpec "
                            "change archive")

    dispositions = _load_dispositions(ctx)
    findings: list[Finding] = []
    for repo, repo_path in scoped:
        writers = _collect_writers(repo_path)
        if not writers:
            continue
        tie_rank = _tie_ranker(repo_path, ctx.git)
        promoted_cache: dict[str, dict[str, list[str]] | None] = {}

        def promoted(capability: str):
            if capability not in promoted_cache:
                spec = repo_path / "openspec" / "specs" / capability / "spec.md"
                promoted_cache[capability] = parse_promoted(
                    spec.read_text(encoding="utf-8", errors="replace")
                ) if spec.is_file() else None
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
