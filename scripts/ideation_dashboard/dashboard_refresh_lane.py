"""Nightly ideation-dashboard IMAGE REFRESH lane (openxFactory change
`add-nightly-dashboard-refresh`, tasks 4.3/4.3a/4.5/4.6/4.7).

The SNAPSHOT lane beside this one (`nightly_lane.py`) refreshes the committed
snapshot in the aggregation. This lane refreshes the SERVED plane: it decides
whether the hosted openXdox image's BAKED inputs have moved, and when they have
it rebakes them at ONE revision and proposes a digest pin to the served plane's
own delivery path. It never applies anything: no kubeconfig, no cluster
credential, no merge call.

    health/ideation-dashboard/refresh-status.json
        this run's outcome — ``ok`` (built and proposed), ``no_change``,
        ``skipped`` (readiness / unresolvable input) or ``strict_failed`` —
        beside the snapshot lane's ``lane-status.json`` and delivered by the
        same ``git add health/`` rolling-PR step.

THE NO-CHANGE DECISION IS ON INPUT REVISIONS, BEFORE THE BUILD (design
Decision 10). Two revisions are compared against the two recorded with the
currently pinned image:

  * the CORPUS input revision — openxFactory, the last commit touching the
    eight paths the Dockerfile copies (`CORPUS_BAKED_PATHS`);
  * the BUILD-RECIPE input revision — Omnigent-Install, the last commit
    touching `containers/ideation-dashboard` (`RECIPE_BAKED_PATHS`).

Both scopes are the repositories' BAKED INPUTS, never their branch TIPS. The
served plane's `main` advances for reasons that have nothing to do with this
image — including, inevitably, this lane's own merged pin commits — so a
tip-versus-tip comparison would make every landed pin force the next night's
rebuild, which is the churn the requirement exists to prevent. The scope each
side was computed with is RECORDED with the pin, so consecutive runs compare
like with like; a scope that changed is treated as movement rather than
compared across two different questions.

OUTPUT-DIGEST EQUALITY IS BANNED AS THE PREDICATE and this module offers no
way to spell it. The build is not reproducible (a fresh checkout re-stamps file
modification times, so the COPY layers differ byte-wise even when every file's
content is identical; `FROM python:3.12-slim` floats), so that comparison can
never find equality: the short-circuit would never fire and the lane would pin
and deploy content-equivalent images nightly. `digest_note()` retains digest
inequality as a defence-in-depth NOTE on a run that built anyway, never as a
trigger.

PROVENANCE LIVES IN THE PIN'S OWN COMMENT (task 4.3a). The authoritative record
is a stable machine-readable key/value block inside the `images:` entry of the
served plane's overlay — in-repo state a plain read of `main` resolves, needing
no API archaeology through merged pull requests, and already inside the shape
the auto-merge envelope admits. The PR body repeats it for human reviewers and
is explicitly NOT the record this lane reads. Absent or unparseable provenance
(today's hand-pinned bootstrap image) is treated as CHANGED: the lane builds
once and its pin establishes the record every later run reads. Failing OPEN
there is deliberate and bounded — one redundant build, versus a hand-pinned
plane left permanently unrefreshed.

ONE REVISION, NOT TWO (`verify_one_revision`). The snapshot is generated from
the SAME materialized corpus whose roots are baked, so the snapshot's
`generation.source_revision` and the baked `/source` tree are one commit by
construction rather than by an operator's care. The assertion is made where the
build is — on the worker child, before the image exists — so the two-revision
trap is DETECTABLE rather than merely avoidable: an image whose snapshot names
revision X over a corpus at revision Y publishes a freshness header the viewer
cannot satisfy. OF THAT RECIPE, THIS MODULE HOLDS ONLY THE PREDICATE
(`verify_one_revision`) — never the generation, the build or the assertion's
call site.

`--strict` IS THE PUBLICATION GATE and it precedes the push. Zero errors AND
zero warnings, and a validator that could not RUN fails too; a non-zero exit
means no tag, no push, no digest, no branch, no pull request — there is nothing
to retract because nothing was published.

FAILURE SEMANTICS, as the snapshot lane's: every error path is a recorded
outcome and exit 0. The lane never fails the nightly, and its own status write
failing must never take the run down either.

THE PARENT SEALS, THE CHILD CONSUMES (`--phase seal`). Because the worker may
hold no Git credential at all, the source cannot cross by a worker-side read;
it crosses as ONE bounded artifact this module materializes on the credentialed
parent, from the corpus checkout the decision already used, with a manifest
carrying the source head, that commit's own committer date, both path-scoped
input revisions, a per-file sha256 index and one digest over the whole sealed
tree. Sealing is MATERIALIZATION, not building: `git archive` of a revision the
parent already has, plus one contents read of the single-file recipe. See the
seal section for why the seal path set is deliberately WIDER than the baked
path set and why the decision's set must not follow it.

WHAT THIS MODULE DELIBERATELY DOES NOT DO. It opens no pull request and pushes
no branch. It RENDERS the pin (the rewritten overlay text plus a PR body) and
the workflow step does the force-free branch delivery with the App token, the
same division the report step uses. AND IT DOES NOT BUILD: it runs no container
build and no registry login, materializes no repository by a worker-side read,
and offers no CLI phase that would. The recipe lives in exactly ONE place — the
worker child's own workflow — and the requirement this lane is ratified under
prohibits the worker from holding a Git credential at all, so a second
module-side realization of the recipe would contradict the contract even while
unreachable. The decision core is a pure function over three inputs and needs
neither git nor a container runtime to be tested; the build callable is
INJECTED (`run_refresh_lane(build=...)`) and in production is only ever the
`--phase pin` adapter over the digest record the child returned.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from ideation_dashboard.boundary import OutputBoundary  # noqa: E402

LANE = "ideation-dashboard-refresh"
STATUS_NAME = "refresh-status.json"
DEFAULT_OUT_DIR = "health/ideation-dashboard"

# The corpus repository's BAKED INPUTS — exactly the paths the served plane's
# Dockerfile copies (`COPY openxFactory/...` plus the two script packages),
# which correctly ignores `tests/` and `experiments/` (169 MB, referenced by
# zero docs). Sorted, because the tuple is written into the pin as the SCOPE
# the comparison was made with and two spellings of one scope would read as a
# scope change.
CORPUS_BAKED_PATHS: tuple[str, ...] = (
    "contracts",
    "docs",
    "examples",
    "ideation",
    "openspec",
    "scripts/doc_health",
    "scripts/ideation_dashboard",
    "templates",
)

# The served plane's BAKED INPUTS: the build recipe. A Dockerfile change alters
# the image with the corpus untouched and would otherwise be invisible behind a
# digest-only diff, which is why the predicate carries two revisions.
RECIPE_BAKED_PATHS: tuple[str, ...] = ("containers/ideation-dashboard",)

DEFAULT_CORPUS_REPO = "opensoft/openxFactory"
DEFAULT_RECIPE_REPO = "opensoft/Omnigent-Install"
DEFAULT_CORPUS_REF = "origin/main"
DEFAULT_RECIPE_REF = "main"
DEFAULT_OVERLAY_PATH = "deploy/kubernetes/overlays/aks-qa/kustomization.yaml"
DEFAULT_IMAGE = "acropensoftxfactoryqa.azurecr.io/ideation-dashboard"
DEFAULT_PIN_BRANCH = "bot/dox-dashboard-pin"

# Outcome classes (spec: "published-and-proposed, no-change, skipped, and
# strict-validation failure"). `ok` IS the built-and-proposed case and always
# carries a `built_digest`; the spelling matches the snapshot lane's
# lane-status so one reader understands both artifacts.
RESULT_OK = "ok"
RESULT_NO_CHANGE = "no_change"
RESULT_SKIPPED = "skipped"
RESULT_STRICT_FAILED = "strict_failed"

DETAIL_CAP = 50


# --------------------------------------------------------------------------
# The provenance record — the pin comment's machine-readable block (4.3a).
# --------------------------------------------------------------------------

PROVENANCE_VERSION = "v1"
PROVENANCE_KEY = "xf-refresh-provenance"
_KEY_PREFIX = "xf-refresh-"
_REVISION_RE = re.compile(r"^[0-9a-f]{7,40}$")
# One comment line, one key. Deterministic by construction: a fixed key set, a
# single `key: value` split, and no prose to regex-guess at. A line that does
# not match is prose and is left alone.
_KV_RE = re.compile(r"^#\s*(xf-refresh-[a-z-]+)\s*:\s*(\S.*?)\s*$")

_REQUIRED_KEYS = (
    PROVENANCE_KEY,
    "xf-refresh-corpus-repo",
    "xf-refresh-corpus-revision",
    "xf-refresh-corpus-scope",
    "xf-refresh-recipe-repo",
    "xf-refresh-recipe-revision",
    "xf-refresh-recipe-scope",
)


@dataclass(frozen=True)
class Provenance:
    """What the pin records so the NEXT run can make the input-revision
    comparison without archaeology.

    `corpus_revision` / `recipe_revision` are the COMPARANDS — the last commit
    touching each repository's baked inputs under the recorded scope. They are
    deliberately distinct from `source_revision`, which is the corpus
    CHECKOUT's HEAD (the snapshot's `generation.source_revision`, and the
    revision the baked `/source` tree carries). The two differ whenever HEAD
    carries commits that touch nothing the image bakes, and conflating them is
    how a lane starts rebuilding on every unrelated commit."""

    corpus_repo: str
    corpus_revision: str
    corpus_scope: tuple[str, ...]
    recipe_repo: str
    recipe_revision: str
    recipe_scope: tuple[str, ...]
    source_revision: str | None = None
    tag: str | None = None
    generated_at: str | None = None
    run_id: str | None = None

    def as_dict(self) -> dict:
        return {
            "corpus_repo": self.corpus_repo,
            "corpus_revision": self.corpus_revision,
            "corpus_scope": list(self.corpus_scope),
            "recipe_repo": self.recipe_repo,
            "recipe_revision": self.recipe_revision,
            "recipe_scope": list(self.recipe_scope),
            "source_revision": self.source_revision,
            "tag": self.tag,
            "generated_at": self.generated_at,
            "run_id": self.run_id,
        }


def render_provenance(prov: Provenance, indent: str = "    ") -> list[str]:
    """The machine-readable block, as overlay COMMENT lines.

    Emitted beside (never instead of) the human prose the two hand-written pins
    carry: the comment must serve a reader and a parser at once, so this writes
    only `xf-refresh-*` lines and the caller keeps the prose."""
    pairs: list[tuple[str, str]] = [
        (PROVENANCE_KEY, PROVENANCE_VERSION),
        ("xf-refresh-corpus-repo", prov.corpus_repo),
        ("xf-refresh-corpus-revision", prov.corpus_revision),
        ("xf-refresh-corpus-scope", " ".join(prov.corpus_scope)),
        ("xf-refresh-recipe-repo", prov.recipe_repo),
        ("xf-refresh-recipe-revision", prov.recipe_revision),
        ("xf-refresh-recipe-scope", " ".join(prov.recipe_scope)),
    ]
    for key, value in (("xf-refresh-source-revision", prov.source_revision),
                       ("xf-refresh-tag", prov.tag),
                       ("xf-refresh-generated-at", prov.generated_at),
                       ("xf-refresh-run-id", prov.run_id)):
        if value:
            pairs.append((key, str(value)))
    return [f"{indent}# {key}: {value}" for key, value in pairs]


def parse_provenance(lines) -> Provenance | None:
    """Parse the block out of an image entry's comment lines.

    FAILS SAFE, always to None, which every caller reads as CHANGED: an absent
    block, an unknown version, a duplicated key (ambiguous — a merge artifact
    could leave two), a malformed revision, or an empty scope. None is never an
    error and never a reason to skip; it is the bootstrap build."""
    if isinstance(lines, str):
        lines = lines.splitlines()
    found: dict[str, str] = {}
    for raw in lines:
        match = _KV_RE.match(str(raw).strip())
        if match is None:
            continue                      # prose, or another comment entirely
        key, value = match.group(1), match.group(2)
        if key in found:
            return None                   # ambiguous: refuse to guess
        found[key] = value
    if any(key not in found for key in _REQUIRED_KEYS):
        return None
    if found[PROVENANCE_KEY] != PROVENANCE_VERSION:
        return None                       # a version this parser cannot read
    corpus_rev = found["xf-refresh-corpus-revision"].lower()
    recipe_rev = found["xf-refresh-recipe-revision"].lower()
    if not (_REVISION_RE.match(corpus_rev) and _REVISION_RE.match(recipe_rev)):
        return None
    corpus_scope = tuple(found["xf-refresh-corpus-scope"].split())
    recipe_scope = tuple(found["xf-refresh-recipe-scope"].split())
    if not corpus_scope or not recipe_scope:
        return None
    source_rev = found.get("xf-refresh-source-revision")
    return Provenance(
        corpus_repo=found["xf-refresh-corpus-repo"],
        corpus_revision=corpus_rev,
        corpus_scope=corpus_scope,
        recipe_repo=found["xf-refresh-recipe-repo"],
        recipe_revision=recipe_rev,
        recipe_scope=recipe_scope,
        source_revision=(source_rev or "").lower() or None,
        tag=found.get("xf-refresh-tag"),
        generated_at=found.get("xf-refresh-generated-at"),
        run_id=found.get("xf-refresh-run-id"),
    )


# --------------------------------------------------------------------------
# The overlay pin — reading the record, and rewriting exactly one digest line
# plus its adjacent comment (tasks 4.6, 5.2a, 5.3).
# --------------------------------------------------------------------------

@dataclass
class PinEntry:
    """One `images:` entry, located by line index so a rewrite can be proven to
    touch nothing else in the file."""
    image: str
    start: int                 # index of the `- name:` line
    end: int                   # exclusive
    comment_lines: list[str]   # comment lines INSIDE the entry
    digest_index: int | None
    digest: str | None
    indent: str


def _entry_indent(line: str) -> str:
    return line[:len(line) - len(line.lstrip())]


def find_pin_entry(text: str, image: str) -> PinEntry | None:
    """Locate the `images:` entry for `image`.

    Line-based on purpose: a YAML round-trip through PyYAML would drop every
    comment in the file, and the comment is the load-bearing state this design
    put there. So the parse is narrow — the `images:` block, its list items,
    and the `name:`/`digest:` keys inside the one entry."""
    lines = text.splitlines()
    in_images = False
    images_indent = ""
    entries: list[tuple[int, int]] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not in_images:
            if re.match(r"^images\s*:\s*$", line):
                in_images = True
                images_indent = _entry_indent(line)
            continue
        if stripped and not stripped.startswith("#"):
            indent = _entry_indent(line)
            if stripped.startswith("- "):
                if len(indent) > len(images_indent):
                    entries.append((index, len(indent)))
                    continue
            if len(indent) <= len(images_indent):
                break                     # the `images:` block ended
    if not entries:
        return None
    bounds: list[tuple[int, int]] = []
    for position, (start, _) in enumerate(entries):
        end = entries[position + 1][0] if position + 1 < len(entries) else len(lines)
        bounds.append((start, end))
    for start, end in bounds:
        block = lines[start:end]
        name = None
        for line in block:
            match = re.match(r"^\s*-?\s*name\s*:\s*(\S+)\s*$", line)
            if match:
                name = match.group(1).strip("\"'")
                break
        if name != image:
            continue
        digest_index = None
        digest = None
        comment_lines: list[str] = []
        # Trailing blank/comment lines belong to the NEXT entry's comment, not
        # this one; walk back so an entry's block ends at its last real key.
        real_end = end
        while real_end - 1 > start and not lines[real_end - 1].strip():
            real_end -= 1
        for offset, line in enumerate(lines[start:real_end]):
            stripped = line.strip()
            if stripped.startswith("#"):
                comment_lines.append(line)
                continue
            match = re.match(r"^\s*digest\s*:\s*(\S+)\s*$", line)
            if match:
                digest_index = start + offset
                digest = match.group(1).strip("\"'")
        indent = _entry_indent(lines[digest_index]) if digest_index is not None \
            else _entry_indent(lines[start]) + "  "
        return PinEntry(image=image, start=start, end=real_end,
                        comment_lines=comment_lines, digest_index=digest_index,
                        digest=digest, indent=indent)
    return None


def read_pinned_digest(text: str, image: str) -> str | None:
    entry = find_pin_entry(text, image)
    return entry.digest if entry else None


def read_pinned_provenance(text: str, image: str) -> Provenance | None:
    """The record the no-change check reads: the machine block in the pinned
    image's own comment. None (⇒ CHANGED) when the entry is missing, when the
    comment is the human prose the bootstrap pin carries, or when anything
    about the block does not parse."""
    entry = find_pin_entry(text, image)
    if entry is None:
        return None
    return parse_provenance(entry.comment_lines)


def rewrite_pin(text: str, image: str, digest: str,
                prov: Provenance) -> str:
    """Return the overlay with EXACTLY the digest value and this entry's
    machine-provenance comment replaced.

    Envelope-shaped by construction (task 4.6): the human prose in the comment
    is preserved verbatim, no other entry is touched, no key other than
    `digest:` is written, and no other block or file is reachable from here.
    The shape is PRODUCED, never asserted — the receiving repository
    adjudicates the actual diff, and this lane sets no label, title prefix or
    commit-message convention that would claim it."""
    entry = find_pin_entry(text, image)
    if entry is None:
        raise ValueError(f"no images: entry for {image!r} in the overlay")
    if entry.digest_index is None:
        raise ValueError(f"the images: entry for {image!r} carries no digest line")
    lines = text.splitlines()
    trailing_newline = text.endswith("\n")
    block = lines[entry.start:entry.end]
    kept: list[str] = []
    for line in block:
        if _KV_RE.match(line.strip()):
            continue                       # the previous machine block goes
        kept.append(line)
    digest_offset = next(offset for offset, line in enumerate(kept)
                         if re.match(r"^\s*digest\s*:\s*\S+\s*$", line))
    kept[digest_offset] = f"{entry.indent}digest: {digest}"
    rendered = render_provenance(prov, indent=entry.indent)
    kept[digest_offset:digest_offset] = rendered
    out = lines[:entry.start] + kept + lines[entry.end:]
    return "\n".join(out) + ("\n" if trailing_newline else "")


# --------------------------------------------------------------------------
# THE DECISION. A pure function over three inputs — no git, no docker, no
# network — so the ordering it fixes is unit-testable (task 5.2).
# --------------------------------------------------------------------------

# Why the lane acted, in machine-readable form.
REASON_UNCHANGED = "inputs_unchanged"
REASON_BOOTSTRAP = "provenance_absent_or_unparseable"
REASON_SCOPE_CHANGED = "input_scope_changed"
REASON_CORPUS_MOVED = "corpus_moved"
REASON_RECIPE_MOVED = "recipe_moved"
REASON_BOTH_MOVED = "corpus_and_recipe_moved"
REASON_UNRESOLVED = "input_revision_unresolved"


@dataclass(frozen=True)
class RefreshDecision:
    """Build or do nothing, and the four revisions that settled it.

    `build=False` is TWO different things and they must not be conflated:
    `no_change` is a positive finding that both inputs matched (and the status
    artifact names the matching revisions, so "nothing moved" is auditable),
    while `undecidable` means an input revision could not be READ at all and
    the lane skips fail-closed rather than claiming quiet."""

    build: bool
    outcome: str                       # "build" | "no_change" | "undecidable"
    reason: str
    corpus_revision: str | None
    recorded_corpus_revision: str | None
    recipe_revision: str | None
    recorded_recipe_revision: str | None
    corpus_scope: tuple[str, ...] = CORPUS_BAKED_PATHS
    recipe_scope: tuple[str, ...] = RECIPE_BAKED_PATHS
    recorded_corpus_scope: tuple[str, ...] | None = None
    recorded_recipe_scope: tuple[str, ...] | None = None
    bootstrap: bool = False

    @property
    def no_change(self) -> bool:
        return self.outcome == "no_change"

    @property
    def undecidable(self) -> bool:
        return self.outcome == "undecidable"

    def comparands(self) -> dict:
        """The two input revisions, each BESIDE the recorded revision it was
        compared against — the shape the observability requirement fixes."""
        return {
            "corpus": {
                "repository": None,       # filled by the caller that knows it
                "scope": list(self.corpus_scope),
                "current_revision": self.corpus_revision,
                "recorded_revision": self.recorded_corpus_revision,
                "recorded_scope": (list(self.recorded_corpus_scope)
                                   if self.recorded_corpus_scope is not None else None),
                "matched": _same_revision(self.corpus_revision,
                                          self.recorded_corpus_revision),
            },
            "recipe": {
                "repository": None,
                "scope": list(self.recipe_scope),
                "current_revision": self.recipe_revision,
                "recorded_revision": self.recorded_recipe_revision,
                "recorded_scope": (list(self.recorded_recipe_scope)
                                   if self.recorded_recipe_scope is not None else None),
                "matched": _same_revision(self.recipe_revision,
                                          self.recorded_recipe_revision),
            },
        }

    def log_line(self) -> str:
        if self.build:
            return (f"{LANE}: BUILD — {self.reason} "
                    f"(corpus {_short(self.corpus_revision)} vs recorded "
                    f"{_short(self.recorded_corpus_revision)}; recipe "
                    f"{_short(self.recipe_revision)} vs recorded "
                    f"{_short(self.recorded_recipe_revision)})")
        if self.no_change:
            return (f"{LANE}: NO CHANGE — corpus and recipe inputs both match "
                    f"the pinned record (corpus {_short(self.corpus_revision)}, "
                    f"recipe {_short(self.recipe_revision)}); nothing built, "
                    f"nothing proposed")
        return f"{LANE}: SKIPPED — {self.reason}"


def _same_revision(left: str | None, right: str | None) -> bool:
    """Exact equality, case-folded. Deliberately NOT prefix matching: an
    abbreviated recorded revision cannot equal a full one, so it reads as
    movement and costs one redundant build — the same fail-open direction the
    bootstrap rule already takes, and the direction that can never leave a
    stale plane unrefreshed."""
    if not left or not right:
        return False
    return left.strip().lower() == right.strip().lower()


def _same_scope(left, right) -> bool:
    if left is None or right is None:
        return False
    return tuple(sorted(str(x) for x in left)) == tuple(sorted(str(x) for x in right))


def decide_refresh(
    *,
    corpus_revision: str | None,
    recipe_revision: str | None,
    recorded: Provenance | None,
    corpus_scope: tuple[str, ...] = CORPUS_BAKED_PATHS,
    recipe_scope: tuple[str, ...] = RECIPE_BAKED_PATHS,
) -> RefreshDecision:
    """Decide BUILD or NO-OP from the two current baked-input revisions and the
    provenance recorded with the currently pinned image.

    PURE. It runs BEFORE any checkout, so a quiet night costs two revision
    reads instead of a clone, a snapshot generation, a docker build and an ACR
    push. Nothing here can see a built digest, which is the point: output-digest
    equality is banned as the predicate and there is no argument through which
    it could arrive."""
    recorded_corpus = recorded.corpus_revision if recorded else None
    recorded_recipe = recorded.recipe_revision if recorded else None
    recorded_corpus_scope = recorded.corpus_scope if recorded else None
    recorded_recipe_scope = recorded.recipe_scope if recorded else None

    def _decide(build: bool, outcome: str, reason: str,
                bootstrap: bool = False) -> RefreshDecision:
        return RefreshDecision(
            build=build, outcome=outcome, reason=reason,
            corpus_revision=corpus_revision,
            recorded_corpus_revision=recorded_corpus,
            recipe_revision=recipe_revision,
            recorded_recipe_revision=recorded_recipe,
            corpus_scope=tuple(corpus_scope), recipe_scope=tuple(recipe_scope),
            recorded_corpus_scope=recorded_corpus_scope,
            recorded_recipe_scope=recorded_recipe_scope,
            bootstrap=bootstrap)

    # Fail CLOSED on an unreadable input: "I could not look" is not "nothing
    # moved", and recording it as no_change would silently freeze the plane.
    missing = [name for name, value in (("corpus", corpus_revision),
                                        ("recipe", recipe_revision))
               if not value]
    if missing:
        return _decide(False, "undecidable",
                       f"{REASON_UNRESOLVED}: {', '.join(missing)}")

    # Bootstrap: no usable record ⇒ CHANGED. One redundant build, and the pin
    # this run produces establishes the record every later run reads.
    if recorded is None:
        return _decide(True, "build", REASON_BOOTSTRAP, bootstrap=True)

    # A scope that moved makes the two runs different QUESTIONS, so equality of
    # their answers would be meaningless. Rebuild and re-record.
    if not (_same_scope(corpus_scope, recorded_corpus_scope)
            and _same_scope(recipe_scope, recorded_recipe_scope)):
        return _decide(True, "build", REASON_SCOPE_CHANGED)

    corpus_matched = _same_revision(corpus_revision, recorded_corpus)
    recipe_matched = _same_revision(recipe_revision, recorded_recipe)
    if corpus_matched and recipe_matched:
        return _decide(False, "no_change", REASON_UNCHANGED)
    if corpus_matched:
        return _decide(True, "build", REASON_RECIPE_MOVED)
    if recipe_matched:
        return _decide(True, "build", REASON_CORPUS_MOVED)
    return _decide(True, "build", REASON_BOTH_MOVED)


def digest_note(built_digest: str | None, pinned_digest: str | None) -> str | None:
    """Defence-in-depth NOTE for a run that built anyway. Never a trigger, and
    nothing in the decision path calls this: the build is not reproducible, so
    an equal digest here is a curiosity worth logging and an unequal one proves
    nothing at all."""
    if not built_digest or not pinned_digest:
        return None
    if built_digest == pinned_digest:
        return ("note: the built digest equals the pinned digest — a curiosity, "
                "not a predicate (the build is not reproducible)")
    return None


# --------------------------------------------------------------------------
# Reading the current inputs. Impure, injectable, and never reached by the
# decision tests.
# --------------------------------------------------------------------------

@dataclass
class CommandResult:
    argv: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def subprocess_runner(argv, *, cwd=None, env=None) -> CommandResult:
    """The one place this module shells out. Every caller takes a `runner=`
    so the tests never reach git, docker, az or gh."""
    try:
        proc = subprocess.run([str(a) for a in argv], cwd=str(cwd) if cwd else None,
                              env=env, capture_output=True, text=True)
    except OSError as exc:
        return CommandResult(tuple(str(a) for a in argv), 127, "", str(exc))
    return CommandResult(tuple(str(a) for a in argv), proc.returncode,
                         proc.stdout or "", proc.stderr or "")


def git_baked_input_revision(repo_dir, paths, *, ref: str = "HEAD",
                             runner=subprocess_runner) -> str | None:
    """`git log -1 --format=%H <ref> -- <paths>` — the last commit touching the
    baked inputs, in a LOCAL checkout. Path-scoped, never the branch tip."""
    result = runner(["git", "-C", str(repo_dir), "log", "-1", "--format=%H",
                     ref, "--", *paths])
    if not result.ok:
        return None
    value = result.stdout.strip().splitlines()
    return value[0].strip().lower() if value and value[0].strip() else None


def git_head_revision(repo_dir, *, ref: str = "HEAD",
                      runner=subprocess_runner) -> str | None:
    """The HEAD of a checkout the caller ALREADY HAS — a plain `rev-parse`
    read, never a fetch and never a clone. Kept as part of the module's read
    layer beside the two baked-input readers: the retired build recipe was one
    caller, not its reason to exist."""
    result = runner(["git", "-C", str(repo_dir), "rev-parse", ref])
    if not result.ok:
        return None
    return (result.stdout.strip() or None)


def gh_baked_input_revision(repo: str, paths, *, ref: str = "main",
                            runner=subprocess_runner) -> str | None:
    """The same path-scoped question against a repository with NO local
    checkout — the served plane's, which the nightly does not initialise as a
    submodule. One `gh api` per path (the recipe scope is a single path), then
    the newest of them by committer date, which is what `git log -1` over the
    same path set returns."""
    newest: tuple[str, str] | None = None
    for path in paths:
        result = runner(["gh", "api", "--method", "GET",
                         f"repos/{repo}/commits",
                         "-f", f"sha={ref}", "-f", f"path={path}",
                         "-f", "per_page=1"])
        if not result.ok:
            return None
        try:
            payload = json.loads(result.stdout or "[]")
        except json.JSONDecodeError:
            return None
        if not isinstance(payload, list) or not payload:
            continue                       # no commit ever touched this path
        head = payload[0]
        if not isinstance(head, dict):
            return None
        sha = str(head.get("sha") or "").lower()
        when = str(((head.get("commit") or {}).get("committer") or {}).get("date") or "")
        if not sha:
            return None
        if newest is None or when > newest[1]:
            newest = (sha, when)
    return newest[0] if newest else None


def gh_read_file(repo: str, path: str, *, ref: str = "main",
                 runner=subprocess_runner) -> str | None:
    """Read one file from a repository's default branch. A plain read of
    in-repo state is exactly why the overlay comment is the authoritative
    provenance home."""
    result = runner(["gh", "api",
                     "-H", "Accept: application/vnd.github.raw",
                     f"repos/{repo}/contents/{path}?ref={ref}"])
    if result.ok and result.stdout.strip():
        return result.stdout
    # Fall back to the JSON representation, whose content is base64.
    result = runner(["gh", "api", f"repos/{repo}/contents/{path}?ref={ref}",
                     "--jq", ".content"])
    if not result.ok or not result.stdout.strip():
        return None
    try:
        return base64.b64decode(result.stdout.strip()).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return None


@dataclass
class CurrentInputs:
    """One read of the world, before anything is built."""
    corpus_revision: str | None
    recipe_revision: str | None
    overlay_text: str | None
    pinned_digest: str | None
    recorded: Provenance | None
    errors: list[str] = field(default_factory=list)


def read_current_inputs(
    *,
    corpus_checkout,
    corpus_ref: str = DEFAULT_CORPUS_REF,
    corpus_paths=CORPUS_BAKED_PATHS,
    recipe_repo: str = DEFAULT_RECIPE_REPO,
    recipe_ref: str = DEFAULT_RECIPE_REF,
    recipe_paths=RECIPE_BAKED_PATHS,
    overlay_path: str = DEFAULT_OVERLAY_PATH,
    image: str = DEFAULT_IMAGE,
    runner=subprocess_runner,
    fetch: bool = True,
) -> CurrentInputs:
    """Gather the decision's three inputs. Never raises; an unreadable input
    arrives as None and the decision turns it into a fail-closed skip."""
    errors: list[str] = []
    if fetch:
        # The corpus submodule sits at its PIN, which is not the question; the
        # lane asks about `main`. A fetch failure is not fatal here — the
        # revision read below simply answers from what is present, and a stale
        # answer that matches the record makes the lane skip a night, never
        # publish a wrong image.
        remote_ref = corpus_ref.split("/", 1)[-1] if "/" in corpus_ref else corpus_ref
        fetched = runner(["git", "-C", str(corpus_checkout), "fetch", "--quiet",
                          "origin", remote_ref])
        if not fetched.ok:
            errors.append(f"corpus fetch failed: {fetched.stderr.strip()[:200]}")
    corpus_revision = git_baked_input_revision(corpus_checkout, corpus_paths,
                                               ref=corpus_ref, runner=runner)
    if corpus_revision is None:
        errors.append(f"could not read the corpus baked-input revision at {corpus_ref}")
    recipe_revision = gh_baked_input_revision(recipe_repo, recipe_paths,
                                              ref=recipe_ref, runner=runner)
    if recipe_revision is None:
        errors.append(f"could not read the recipe baked-input revision in {recipe_repo}")
    overlay_text = gh_read_file(recipe_repo, overlay_path, ref=recipe_ref,
                                runner=runner)
    if overlay_text is None:
        errors.append(f"could not read {overlay_path} from {recipe_repo}")
    pinned_digest = read_pinned_digest(overlay_text, image) if overlay_text else None
    recorded = read_pinned_provenance(overlay_text, image) if overlay_text else None
    return CurrentInputs(corpus_revision=corpus_revision,
                         recipe_revision=recipe_revision,
                         overlay_text=overlay_text, pinned_digest=pinned_digest,
                         recorded=recorded, errors=errors)


# --------------------------------------------------------------------------
# The one-revision predicate, and the shape a build's result comes back in.
# The build itself lives on the worker child, in the child's own workflow.
# --------------------------------------------------------------------------

class OneRevisionViolation(Exception):
    """The snapshot's `source_revision` and the baked corpus revision are not
    the same commit — the two-revision trap, made detectable. Raised BEFORE the
    image is built, so no such image can exist."""


def verify_one_revision(snapshot_source_revision: str | None,
                        checkout_head: str | None) -> None:
    """The one-revision contract, asserted rather than assumed.

    The freshness header names the snapshot's `source_revision` and the
    document viewer serves the baked tree; an image whose snapshot names X over
    a corpus at Y publishes a claim the viewer cannot satisfy, and every
    document that landed between the two resolves to nothing. So this is a
    defect of the rebake, not a tolerable approximation."""
    if not snapshot_source_revision or not checkout_head:
        raise OneRevisionViolation(
            "cannot prove the snapshot and the baked corpus share one revision "
            f"(snapshot source_revision={snapshot_source_revision!r}, "
            f"checkout HEAD={checkout_head!r})")
    if not _same_revision(snapshot_source_revision, checkout_head):
        raise OneRevisionViolation(
            "the snapshot's source_revision "
            f"({_short(snapshot_source_revision)}) is NOT the corpus checkout's "
            f"HEAD ({_short(checkout_head)}) — the snapshot and the baked "
            "/source tree would name different commits")


@dataclass
class BuildResult:
    """What a build RETURNS — read back by `--phase pin` from the digest
    record the worker child produced. This module never creates one from a
    build of its own, because it performs none."""
    ok: bool
    reason: str | None = None
    strict_failed: bool = False
    digest: str | None = None
    tag: str | None = None
    source_revision: str | None = None
    corpus_revision: str | None = None
    detail: list[str] = field(default_factory=list)


# --------------------------------------------------------------------------
# THE PARENT SEAL. The credentialed hosted parent materializes the source the
# credential-free child consumes, as ONE bounded artifact (re-realization S2;
# spec "The credentialed hosted parent SHALL then materialize fresh
# openxFactory `main` ... into a bounded sealed source artifact carrying the
# source HEAD, source committer timestamp, and both path-scoped input
# revisions").
#
# WHY THE PARENT AND NOT THE CHILD. The child holds no Git credential — the
# requirement prohibits one outright — so it cannot read a private repository
# at all. The parent already holds an installation token and already has the
# corpus submodule initialised with full history for the decision, so the
# materialization costs one `git archive` of a revision it has in hand: no
# second checkout, no working-tree mutation, and nothing cloned.
#
# THE SEAL SET IS NOT THE DECISION SET, and the difference is load-bearing.
# `snapshot.find_validator` walks UP from the tree being scanned for
# `openxFactory/scripts/validate-ideation-dashboard-contracts.py`; that file is
# a TOP-LEVEL `scripts/*.py`, so `CORPUS_BAKED_PATHS` — which names
# `scripts/doc_health` and `scripts/ideation_dashboard` but not their parent —
# does not carry it. A cone-mode sparse checkout dragged it in as a side
# effect; a `git archive` over a path list does not, and a seal without it
# fails `--strict` with "validator unavailable" rather than with a finding.
# So the SEAL set is `CORPUS_BAKED_PATHS ∪ {the validator}` while the DECISION
# set stays exactly `CORPUS_BAKED_PATHS`: widening the decision scope would
# make `_same_scope` fire `REASON_SCOPE_CHANGED` against every recorded pin and
# force one rebuild for nothing. The asymmetry is deliberate — the validator's
# own revision is sealed but not baked, because the image does not COPY it.
#
# THE REVISION IS PROVEN, NOT ASSERTED. `git archive`'s tar output carries the
# commit it was made from in a global extended pax header (`comment=<sha>`),
# written by git itself, and the seal refuses unless that header equals the
# `source_head` the manifest records. That keeps the one-revision property a
# MEASUREMENT on the parent side: after the change the child's own
# `source_revision == HEAD` check reads two fields of one manifest and is
# tautological on its own, so the parent has to hold the end that still touches
# a real repository.
# --------------------------------------------------------------------------

SEAL_MANIFEST_NAME = "manifest.json"
SEAL_MANIFEST_KIND = "ideation-dashboard-sealed-source-manifest"
SEAL_SCHEMA_VERSION = "1.0.0"
SEAL_ARTIFACT_PREFIX = "dashboard-image-source-"
SEAL_DIGEST_ALGORITHM = "sha256"

# The seal's own layout, which the child's generate/build steps address by
# these exact names.
SEAL_CORPUS_RELPATH = "openxFactory"
SEAL_RECIPE_RELPATH = "recipe/Dockerfile"

# Where the recipe is READ from (Omnigent-Install), as against where it LANDS
# in the seal. The directory holds exactly one file, so this is a contents-API
# read at the pinned recipe revision — never a checkout of that repository.
RECIPE_DOCKERFILE_PATH = "containers/ideation-dashboard/Dockerfile"

# The one path the seal adds to the baked set. See the section note above.
VALIDATOR_SEAL_PATH = "scripts/validate-ideation-dashboard-contracts.py"
CORPUS_SEAL_PATHS: tuple[str, ...] = tuple(sorted({*CORPUS_BAKED_PATHS,
                                                   VALIDATOR_SEAL_PATH}))

# The manifest field whose value the child passes to `generate --generated-at`.
# NOT a wall clock: `generation.generated_at` is defined as the source
# revision's committer date (cli.py `--generated-at`, generator
# `_generation_stamp`), and the snapshot render is canonical precisely because
# nothing in it reads the clock. `sealed_at` is the parent's wall clock and is
# diagnostic only — naming the right field here in the artifact itself is
# cheaper than a comment nobody reads at 03:00.
SEAL_GENERATED_AT_FIELD = "source_committed_at"

# The digest the child recomputes. Spelled out IN the manifest so the rule
# travels with the artifact rather than living only in whichever workflow
# happens to read it. The two-space separator makes each line a `sha256sum`
# line, so the per-file index is checkable with `sha256sum -c` unchanged.
TREE_DIGEST_SPEC = (
    "sha256 of the concatenation of one line per sealed file, each line "
    "'<sha256-hex><two spaces><posix-relative-path><LF>', ordered by the UTF-8 "
    "bytes of the relative path, over every regular file under the seal root "
    f"EXCEPT {SEAL_MANIFEST_NAME} itself"
)

_FULL_REVISION_RE = re.compile(r"^[0-9a-f]{40}$")
# Actions artifact names refuse the path and quoting characters; a correlation
# id that cannot be an artifact name must be refused HERE, where the reason is
# legible, rather than by an upload step's own error three minutes later.
_CORRELATION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,119}$")


class SealRefused(Exception):
    """The parent will not seal. Every refusal is a REFUSAL and not a partial
    artifact: the child must never be able to download a seal whose manifest
    the parent could not stand behind, so the phase writes no manifest at all
    and the dispatch is gated on the result it wrote instead."""


def seal_artifact_name(correlation_id: str) -> str:
    """`dashboard-image-source-<correlation_id>` — the name the child names in
    its cross-run download. One prefix, one id, no run-scoped decoration: the
    child already carries the run id separately."""
    value = (correlation_id or "").strip()
    if not _CORRELATION_RE.match(value):
        raise SealRefused(
            f"correlation id {correlation_id!r} cannot name an Actions "
            "artifact (letters, digits, '.', '_' and '-' only, 1-120 chars)")
    return f"{SEAL_ARTIFACT_PREFIX}{value}"


def file_sha256(path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def seal_file_index(seal_dir) -> dict[str, str]:
    """Every regular file under the seal, by POSIX relative path, to its
    sha256. The manifest itself is excluded — it carries this index and cannot
    hash itself — and a non-regular entry is a refusal rather than a skip:
    `upload-artifact@v4` neither preserves symlinks nor restores execute bits,
    so an index that silently omitted one would promise something the download
    cannot deliver."""
    root = Path(seal_dir)
    index: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_dir() and not path.is_symlink():
            continue
        relpath = path.relative_to(root).as_posix()
        if relpath == SEAL_MANIFEST_NAME:
            continue
        if path.is_symlink() or not path.is_file():
            raise SealRefused(f"the seal holds a non-regular entry: {relpath}")
        index[relpath] = file_sha256(path)
    return index


def tree_digest(index: dict[str, str]) -> str:
    """One digest over the whole sealed tree — see `TREE_DIGEST_SPEC`, which is
    written into the manifest so the child implements the rule the artifact
    states rather than the rule it inferred."""
    lines = "".join(
        f"{index[path]}  {path}\n"
        for path in sorted(index, key=lambda value: value.encode("utf-8")))
    return hashlib.sha256(lines.encode("utf-8")).hexdigest()


def git_commit_datetime(repo_dir, revision: str, *,
                        runner=subprocess_runner) -> str | None:
    """`git show -s --format=%cI <rev>` — the committer date, RFC 3339, of the
    revision the seal was made at. This is the value the child hands to
    `generate --generated-at`, and it is a property of the COMMIT, so a seal
    made twice from one revision names one stamp."""
    # Byte-for-byte the call `generator.RealGitDates.commit_date` makes,
    # `--` end-of-options marker included, so the stamp the child receives
    # through `--generated-at` is the SAME STRING the pre-seal child derived
    # inside its own checkout — the change moves where the value comes from,
    # never what it says, and the snapshot stays byte-identical across it.
    result = runner(["git", "-C", str(repo_dir), "show", "-s",
                     "--format=%cI", revision, "--"])
    if not result.ok:
        return None
    value = result.stdout.strip().splitlines()
    return value[0].strip() if value and value[0].strip() else None


def git_archive_revision(archive_path) -> str | None:
    """The revision GIT ITSELF recorded in the archive: the global extended pax
    header `comment`, which `git archive` writes whenever the tree-ish it was
    given resolves to a commit. Reading it back is what makes the parent-side
    revision check a measurement of the produced bytes rather than a restated
    variable."""
    try:
        with tarfile.open(archive_path, "r:") as archive:
            value = (archive.pax_headers or {}).get("comment")
    except (OSError, tarfile.TarError):
        return None
    value = (value or "").strip().lower()
    return value or None


def _extract_seal_archive(archive_path, dest) -> int:
    """Extract the archive under `dest`. Refuses any entry that is not a plain
    file or a directory BEFORE extracting anything, and extracts under the
    `data` filter where the interpreter has one, so nothing can be written
    outside `dest`."""
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    try:
        with tarfile.open(archive_path, "r:") as archive:
            members = archive.getmembers()
            for member in members:
                if not (member.isfile() or member.isdir()):
                    raise SealRefused(
                        "the source archive holds a non-regular entry: "
                        f"{member.name}")
            try:
                archive.extractall(dest, filter="data")
            except TypeError:      # an interpreter without extraction filters
                archive.extractall(dest)
            return sum(1 for member in members if member.isfile())
    except tarfile.TarError as exc:
        raise SealRefused(f"the source archive could not be read: {exc}") from exc
    except OSError as exc:
        raise SealRefused(f"the source archive could not be extracted: {exc}") from exc


def _decision_field(decision: dict, key: str) -> str:
    value = str((decision or {}).get(key) or "").strip().lower()
    if not _FULL_REVISION_RE.match(value):
        raise SealRefused(
            f"the parent decision carries no usable {key} ({value or 'absent'!r})")
    return value


def seal_source(
    *,
    corpus_checkout,
    seal_dir,
    correlation_id: str,
    decision: dict,
    corpus_repo: str = DEFAULT_CORPUS_REPO,
    corpus_ref: str = DEFAULT_CORPUS_REF,
    recipe_repo: str = DEFAULT_RECIPE_REPO,
    recipe_path: str = RECIPE_DOCKERFILE_PATH,
    seal_paths: tuple[str, ...] = CORPUS_SEAL_PATHS,
    corpus_baked_paths: tuple[str, ...] = CORPUS_BAKED_PATHS,
    parent_repository: str | None = None,
    parent_run_id: str | None = None,
    runner=subprocess_runner,
    read_recipe=None,
) -> dict:
    """Materialize the bounded source artifact and return its manifest.

    Order matters and is the order of the refusals: a decision that did not ask
    for a build seals nothing; a revision that cannot be resolved seals
    nothing; an archive whose own recorded commit is not `source_head` seals
    nothing; a recipe that cannot be read seals nothing. Only a seal that
    passed all four gets a `manifest.json`, and the manifest's presence is
    therefore the artifact's own statement that the parent stands behind it.

    Raises `SealRefused` — never returns a partial seal."""
    decision = decision or {}
    if decision.get("build") is not True:
        raise SealRefused(
            "the parent decision did not ask for a build "
            f"(build={decision.get('build')!r}, outcome="
            f"{decision.get('outcome')!r}) — there is nothing to seal")
    corpus_revision = _decision_field(decision, "corpus_revision")
    recipe_revision = _decision_field(decision, "recipe_revision")
    artifact_name = seal_artifact_name(correlation_id)

    source_head = git_head_revision(corpus_checkout, ref=corpus_ref,
                                    runner=runner)
    source_head = (source_head or "").strip().lower()
    if not _FULL_REVISION_RE.match(source_head):
        raise SealRefused(
            f"could not resolve {corpus_ref} in {corpus_checkout} to a commit")
    source_committed_at = git_commit_datetime(corpus_checkout, source_head,
                                              runner=runner)
    if not source_committed_at:
        raise SealRefused(
            f"could not read the committer date of {_short(source_head)}")

    seal_root = Path(seal_dir)
    if seal_root.exists() and any(seal_root.iterdir()):
        # A seal is a FRESH tree, never an overlay on one: `files` is the
        # authority on what the child must find, so a leftover from an earlier
        # attempt would be indexed, digested and shipped as though the parent
        # had sealed it.
        raise SealRefused(
            f"the seal directory {seal_root} is not empty — a seal must be "
            "materialized into a fresh tree")
    seal_root.mkdir(parents=True, exist_ok=True)
    corpus_root = seal_root / SEAL_CORPUS_RELPATH
    # The intermediate tar lives OUTSIDE the seal (and outside the checkout):
    # it is not part of the artifact, and `git archive --output=` means the
    # bytes never pass through this module's text-mode runner.
    with tempfile.TemporaryDirectory(prefix="dfr-seal-") as staging:
        archive_path = Path(staging) / "source.tar"
        result = runner(["git", "-C", str(corpus_checkout), "archive",
                         "--format=tar", f"--output={archive_path}",
                         source_head, "--", *seal_paths])
        if not result.ok:
            raise SealRefused(
                f"git archive failed at {_short(source_head)}: "
                f"{result.stderr.strip()[:200]}")

        # THE PARENT-SIDE ONE-REVISION ASSERTION (design open question 1). The
        # archive names its own commit; if that is not the head we recorded,
        # the two would disagree in a manifest nobody could later disprove.
        recorded = git_archive_revision(archive_path)
        if recorded != source_head:
            raise SealRefused(
                "the source archive's own recorded revision "
                f"({recorded or 'absent'}) is not the sealed source_head "
                f"({source_head})")
        _extract_seal_archive(archive_path, corpus_root)
    if not any((corpus_root / path.split("/", 1)[0]).exists()
               for path in seal_paths):
        raise SealRefused(
            "the sealed corpus is empty — none of the seal paths materialized")
    validator = corpus_root / VALIDATOR_SEAL_PATH
    if not validator.is_file():
        # The #179 trap, refused at the seal rather than at `--strict` three
        # steps later: without this file the child's validation cannot RUN, and
        # a validation that could not run is a strict failure with no finding
        # to read.
        raise SealRefused(
            f"the seal is missing {VALIDATOR_SEAL_PATH} — the child's "
            "validator would be unreachable and --strict would fail with no "
            "finding to read")

    def _read_recipe_from_the_contents_api() -> str | None:
        # The recipe directory holds exactly ONE file, so this is a contents
        # read at the pinned recipe revision — the same `gh api` path
        # `read_current_inputs` already uses for the overlay. The served
        # plane's repository is never checked out.
        return gh_read_file(recipe_repo, recipe_path, ref=recipe_revision,
                            runner=runner)

    recipe_text = (read_recipe or _read_recipe_from_the_contents_api)()
    if not recipe_text or not recipe_text.strip():
        raise SealRefused(
            f"could not read {recipe_path} from {recipe_repo} at "
            f"{_short(recipe_revision)}")
    recipe_file = seal_root / SEAL_RECIPE_RELPATH
    recipe_file.parent.mkdir(parents=True, exist_ok=True)
    recipe_file.write_text(recipe_text, encoding="utf-8")

    index = seal_file_index(seal_root)
    total_bytes = sum((seal_root / relpath).stat().st_size for relpath in index)
    manifest = {
        "schema_version": SEAL_SCHEMA_VERSION,
        "kind": SEAL_MANIFEST_KIND,
        "artifact_name": artifact_name,
        "correlation_id": correlation_id,
        "parent_repository": parent_repository,
        "parent_run_id": parent_run_id,
        "sealed_at": _now_iso(),
        "source_repo": corpus_repo,
        "source_ref": corpus_ref,
        "source_head": source_head,
        "source_committed_at": source_committed_at,
        "generated_at_field": SEAL_GENERATED_AT_FIELD,
        "corpus_relpath": SEAL_CORPUS_RELPATH,
        "corpus_revision": corpus_revision,
        "corpus_baked_paths": list(corpus_baked_paths),
        "seal_paths": list(seal_paths),
        "recipe_repo": recipe_repo,
        "recipe_revision": recipe_revision,
        "recipe_path": recipe_path,
        "recipe_relpath": SEAL_RECIPE_RELPATH,
        "decision": {
            "outcome": decision.get("outcome"),
            "reason": decision.get("reason"),
            "corpus_revision": corpus_revision,
            "recipe_revision": recipe_revision,
        },
        "digest_algorithm": SEAL_DIGEST_ALGORITHM,
        "tree_digest_spec": TREE_DIGEST_SPEC,
        "tree_digest": tree_digest(index),
        "file_count": len(index),
        "total_bytes": total_bytes,
        "files": index,
    }
    (seal_root / SEAL_MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def read_seal_manifest(seal_dir) -> dict | None:
    try:
        payload = json.loads(
            (Path(seal_dir) / SEAL_MANIFEST_NAME).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def verify_seal(seal_dir, *, correlation_id: str | None = None,
                corpus_revision: str | None = None,
                recipe_revision: str | None = None) -> list[str]:
    """The REFERENCE implementation of the child's intake check: manifest
    present and well-formed, every indexed path present with the recorded
    sha256, the tree digest recomputing, and the recorded revisions matching
    the parent decision the child was dispatched with.

    Returns the problems, empty when the seal verifies. It is a list rather
    than an exception because the child must report ALL of what is wrong before
    it fails — a seal that is missing four files and disagrees about the
    revision is one diagnosis, not four runs.

    NOTE FOR THE CHILD (S3). This function lives INSIDE the corpus the seal
    carries, so calling it from the seal is the artifact vouching for itself.
    The child implements the same check in its own workflow, from its own
    checkout; this is the shape it implements and the unit-tested definition of
    the digest rule."""
    problems: list[str] = []
    manifest = read_seal_manifest(seal_dir)
    if manifest is None:
        return [f"{SEAL_MANIFEST_NAME} is absent or is not readable JSON"]
    if manifest.get("kind") != SEAL_MANIFEST_KIND:
        problems.append(f"manifest kind is {manifest.get('kind')!r}, "
                        f"expected {SEAL_MANIFEST_KIND!r}")
    if str(manifest.get("schema_version") or "").split(".", 1)[0] != \
            SEAL_SCHEMA_VERSION.split(".", 1)[0]:
        problems.append(
            f"manifest schema_version {manifest.get('schema_version')!r} is "
            f"not readable by this reader ({SEAL_SCHEMA_VERSION})")
    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        return problems + ["manifest carries no files index"]
    root = Path(seal_dir)
    recomputed: dict[str, str] = {}
    for relpath in sorted(files):
        path = root / relpath
        if not path.is_file():
            problems.append(f"a required path is absent: {relpath}")
            continue
        actual = file_sha256(path)
        recomputed[relpath] = actual
        if actual != files[relpath]:
            problems.append(f"sha256 mismatch: {relpath}")
    if len(recomputed) == len(files) and not problems:
        digest = tree_digest(recomputed)
        if digest != manifest.get("tree_digest"):
            problems.append(
                f"tree_digest mismatch: recomputed {digest}, manifest records "
                f"{manifest.get('tree_digest')}")
    for label, expected, key in (("correlation id", correlation_id, "correlation_id"),
                                 ("corpus revision", corpus_revision, "corpus_revision"),
                                 ("recipe revision", recipe_revision, "recipe_revision")):
        if expected and str(manifest.get(key) or "").lower() != str(expected).lower():
            problems.append(
                f"{label} mismatch: manifest records "
                f"{manifest.get(key)!r}, the dispatch carried {expected!r}")
    if SEAL_CORPUS_RELPATH + "/" + VALIDATOR_SEAL_PATH not in files:
        problems.append(
            f"the seal does not carry {SEAL_CORPUS_RELPATH}/{VALIDATOR_SEAL_PATH} "
            "— strict validation could not run")
    if manifest.get("recipe_relpath") not in files:
        problems.append("the seal does not carry the build recipe")
    return problems


def seal_result_payload(*, sealed: bool, reason: str | None,
                        manifest: dict | None,
                        artifact_name: str | None = None) -> dict:
    """What the workflow gates the dispatch on. Deliberately small: sealed or
    not, why not, and the four values the dispatch and the child's own check
    need."""
    manifest = manifest or {}
    return {
        "kind": "ideation-dashboard-seal-result",
        "sealed": bool(sealed),
        "reason": reason,
        "artifact_name": manifest.get("artifact_name") or artifact_name,
        "correlation_id": manifest.get("correlation_id"),
        "source_head": manifest.get("source_head"),
        "source_committed_at": manifest.get("source_committed_at"),
        "corpus_revision": manifest.get("corpus_revision"),
        "recipe_revision": manifest.get("recipe_revision"),
        "tree_digest": manifest.get("tree_digest"),
        "file_count": manifest.get("file_count"),
        "total_bytes": manifest.get("total_bytes"),
        "generated_at": _now_iso(),
        "run_id": _run_id(),
    }


# --------------------------------------------------------------------------
# The status artifact + the pin proposal the workflow delivers.
# --------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _run_id() -> str | None:
    return os.environ.get("GITHUB_RUN_ID") or None


def _short(revision: str | None) -> str:
    return (revision or "-")[:12]


@dataclass
class RefreshOutcome:
    """One refresh run. `result` is the recorded outcome class; the lane never
    fails the nightly, so there is no failure to propagate."""
    result: str
    reason: str | None
    decision: RefreshDecision | None
    built_digest: str | None = None
    pinned_digest: str | None = None
    tag: str | None = None
    source_revision: str | None = None
    status_path: Path | None = None
    pin_path: Path | None = None
    pr_body_path: Path | None = None
    provenance: Provenance | None = None
    detail: list[str] = field(default_factory=list)

    @property
    def built(self) -> bool:
        return self.result == RESULT_OK and bool(self.built_digest)

    def log_line(self) -> str:
        if self.result == RESULT_OK:
            return (f"{LANE}: OK — built {self.tag} @ {_short(self.built_digest)} "
                    f"(source_revision={_short(self.source_revision)})")
        if self.result == RESULT_NO_CHANGE:
            return (f"{LANE}: NO CHANGE — {self.reason}; no checkout, no "
                    "snapshot, no build, no push, no branch, no pull request")
        if self.result == RESULT_STRICT_FAILED:
            return f"{LANE}: STRICT FAILED — {self.reason}; nothing published"
        return f"{LANE}: SKIPPED — {self.reason}"

    def annotation(self) -> str:
        """A GitHub Actions annotation, so no outcome is invisible in the run
        itself whatever the artifact-delivery lag turns out to be."""
        level = "notice" if self.result in (RESULT_OK, RESULT_NO_CHANGE) else "warning"
        return f"::{level}::{self.log_line()}"


def refresh_status_payload(
    outcome_result: str,
    reason: str | None,
    decision: RefreshDecision | None,
    *,
    corpus_repo: str = DEFAULT_CORPUS_REPO,
    recipe_repo: str = DEFAULT_RECIPE_REPO,
    source_revision: str | None = None,
    built_digest: str | None = None,
    pinned_digest: str | None = None,
    tag: str | None = None,
    pull_request: str | None = None,
    detail=(),
) -> dict:
    """The refresh-status record (task 4.7).

    Diagnostic, not a projection — it carries a wall-clock `generated_at` and
    the CI `run_id`, like the snapshot lane's status. A `no_change` outcome
    NAMES the revisions that matched, so "nothing moved" is auditable rather
    than merely asserted."""
    inputs: dict = {}
    if decision is not None:
        inputs = decision.comparands()
        inputs["corpus"]["repository"] = corpus_repo
        inputs["recipe"]["repository"] = recipe_repo
    return {
        "kind": "ideation-dashboard-refresh-status",
        "lane": LANE,
        "result": outcome_result,
        "reason": reason,
        "decision": (decision.outcome if decision else None),
        "decision_reason": (decision.reason if decision else None),
        "bootstrap": bool(decision.bootstrap) if decision else False,
        "inputs": inputs,
        "source_revision": source_revision,
        "built_digest": built_digest,
        "pinned_digest": pinned_digest,
        "tag": tag,
        "pull_request": pull_request,
        "detail": list(detail)[:DETAIL_CAP],
        "generated_at": _now_iso(),
        "run_id": _run_id(),
    }


def write_refresh_status(out_dir: Path, payload: dict) -> Path | None:
    """Write the status artifact. Its own failure must NEVER take the run
    down — the log line and the run annotation still carry the outcome."""
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    out_dir = Path(out_dir)
    try:
        boundary = OutputBoundary(out_dir, [STATUS_NAME])
        return boundary.write_output(out_dir / STATUS_NAME, text)
    except Exception:  # noqa: BLE001 — status is best-effort reporting
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            path = out_dir / STATUS_NAME
            path.write_text(text, encoding="utf-8")
            return path
        except OSError:
            return None


REPORT_HEADING = "## Ideation-dashboard image refresh"


def render_report_section(status: dict | None, *, this_run_id: str | None = None,
                          stuck_pull_request: str | None = None) -> str:
    """The dated report's refresh section.

    THE ORDERING WRINKLE, stated in the artifact rather than papered over
    (design Decision 6). The refresh stage is deliberately ordered AFTER the
    report delivery, so the status artifact this section can READ is the
    PREVIOUS run's. The requirement is explicit that a lagging outcome must not
    be presented as the current one, so the section names whose outcome it is,
    with that run's own id and stamp. The run's `::notice::`/`::warning::`
    annotations carry THIS run's outcome immediately, which is why the lag is
    acceptable rather than merely tolerated."""
    lines = [REPORT_HEADING, ""]
    if not status:
        lines += [
            "No refresh-status artifact has been delivered yet — the lane has "
            "not run, or its first outcome lands with the next report. The "
            "run's own annotations carry the current outcome.",
            "",
        ]
        return "\n".join(lines)
    recorded_run = status.get("run_id")
    stamp = status.get("generated_at")
    if this_run_id and recorded_run and str(recorded_run) == str(this_run_id):
        whose = f"this run ({recorded_run})"
    else:
        whose = f"the PREVIOUS run ({recorded_run or 'unknown run'})"
    lines += [
        f"Outcome below is {whose}, recorded {stamp or 'unknown'} — the refresh "
        "stage runs after this report is delivered, so its artifact rides the "
        "next report. This is not this run's outcome unless it says so.",
        "",
        f"- Result: `{status.get('result')}`"
        + (f" — {status.get('reason')}" if status.get("reason") else ""),
    ]
    inputs = status.get("inputs") or {}
    for side in ("corpus", "recipe"):
        entry = inputs.get(side) or {}
        if not entry:
            continue
        matched = "matched" if entry.get("matched") else "MOVED"
        lines.append(
            f"- {side.capitalize()} input revision ({entry.get('repository')}): "
            f"`{_short(entry.get('current_revision'))}` vs recorded "
            f"`{_short(entry.get('recorded_revision'))}` — {matched}")
    if status.get("built_digest"):
        lines.append(f"- Built digest: `{status['built_digest']}` "
                     f"(tag `{status.get('tag')}`), replacing "
                     f"`{status.get('pinned_digest') or 'none recorded'}`")
    if status.get("source_revision"):
        lines.append(f"- Snapshot `source_revision`: "
                     f"`{status['source_revision']}`")
    if status.get("pull_request"):
        lines.append(f"- Pin pull request: {status['pull_request']}")
    if stuck_pull_request:
        lines.append(f"- **STUCK CHAIN**: pin pull request "
                     f"{stuck_pull_request} on `{DEFAULT_PIN_BRANCH}` is still "
                     "open at this run — the refresh is parked")
    lines.append("")
    return "\n".join(lines)


def append_report_section(report_path, section: str) -> bool:
    """Append the section to the dated report. Best-effort by design: a report
    that cannot be appended to must never become the reason the lane fails."""
    try:
        path = Path(report_path)
        existing = path.read_text(encoding="utf-8") if path.is_file() else ""
        separator = "" if existing.endswith("\n\n") or not existing else \
            ("\n" if existing.endswith("\n") else "\n\n")
        path.write_text(existing + separator + section, encoding="utf-8")
        return True
    except OSError:
        return False


def record_pull_request(out_dir, reference: str | None) -> bool:
    """Patch the delivered status artifact with the pin pull request's
    reference, once the workflow's delivery step knows it.

    Best-effort, like every other write in this lane: a status artifact that
    cannot be updated must never become the reason a landed pin is reported as
    a failure."""
    if not reference:
        return False
    payload = read_status_artifact(out_dir)
    if payload is None:
        return False
    payload["pull_request"] = reference
    return write_refresh_status(Path(out_dir), payload) is not None


def read_status_artifact(out_dir) -> dict | None:
    """The status artifact already present in the tree — which, because the
    stage follows the delivery, is the PREVIOUS run's."""
    try:
        return json.loads((Path(out_dir) / STATUS_NAME).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def render_pr_body(*, prov: Provenance, digest: str, previous_digest: str | None,
                   tag: str, source_revision: str | None,
                   strict_summary: str = "0 error(s), 0 warning(s) (--strict)",
                   run_url: str | None = None,
                   overlay_path: str = DEFAULT_OVERLAY_PATH) -> str:
    """The pin PR body: the provenance a human would otherwise reconstruct.

    Explicitly a COURTESY restatement. The record this lane READS is the
    overlay comment, never a pull-request body — a merged PR is not a queryable
    state store, and making the lane search merged PRs for its own last
    provenance would be archaeology where a plain read suffices. No label, no
    title prefix and no commit-message convention here CLAIMS the diff shape:
    the receiving repository adjudicates the actual diff."""
    lines = [
        "Nightly ideation-dashboard image refresh: digest-only pin.",
        "",
        f"- Overlay: `{overlay_path}`",
        f"- Image tag: `{tag}`",
        f"- New digest: `{digest}`",
        f"- Previous digest: `{previous_digest or 'none recorded'}`",
        f"- Snapshot `source_revision`: `{source_revision or 'unknown'}`",
        f"- Corpus input revision ({prov.corpus_repo}): `{prov.corpus_revision}`",
        f"  scope: `{' '.join(prov.corpus_scope)}`",
        f"- Build-recipe input revision ({prov.recipe_repo}): `{prov.recipe_revision}`",
        f"  scope: `{' '.join(prov.recipe_scope)}`",
        f"- Strict validation: {strict_summary}",
    ]
    if run_url:
        lines.append(f"- Run: {run_url}")
    lines += [
        "",
        "The snapshot and the baked `/source` corpus come from ONE checkout at "
        "one revision by construction, so the freshness header this image "
        "displays is satisfiable by the `/source` tree in the same image.",
        "",
        "This body is a COURTESY restatement for reviewers. The record the lane "
        "reads is the machine-readable provenance block in the pin's own "
        "comment inside the overlay's `images:` entry — not this description.",
        "",
        "🤖 Generated with [Claude Code](https://claude.com/claude-code)",
    ]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# The lane.
# --------------------------------------------------------------------------

def run_refresh_lane(
    repo_root,
    *,
    out_dir: str = DEFAULT_OUT_DIR,
    image: str = DEFAULT_IMAGE,
    corpus_repo: str = DEFAULT_CORPUS_REPO,
    recipe_repo: str = DEFAULT_RECIPE_REPO,
    overlay_path: str = DEFAULT_OVERLAY_PATH,
    corpus_scope: tuple[str, ...] = CORPUS_BAKED_PATHS,
    recipe_scope: tuple[str, ...] = RECIPE_BAKED_PATHS,
    inputs: CurrentInputs | None = None,
    read_inputs=None,
    build=None,
    build_plan: object | None = None,
    pin_out: Path | str | None = None,
    run_url: str | None = None,
    skip_reason: str | None = None,
    write_status: bool = True,
) -> RefreshOutcome:
    """Decide, then (only then) build, then render the pin proposal.

    ORDERING IS THE CONTRACT, and it is structural rather than advisory:
    `build` is a callable this function invokes at exactly one place, guarded
    by `decision.build`. On a no-change night it is never called, so the tests
    can assert the absence of a checkout, a generation, a build and a push
    rather than merely the absence of a pull request — an outcome-only
    assertion passes even when the build ran. `build_plan` is an OPAQUE handle
    handed straight to that callable: this module neither constructs nor
    interprets one, because it holds no build recipe.

    Never raises. `skip_reason` is the readiness verdict handed down by the
    workflow: an unready worker skips before any input is read, and there is
    deliberately no hosted fallback."""
    out_abs = Path(repo_root) / out_dir

    def _emit(outcome: RefreshOutcome) -> RefreshOutcome:
        if not write_status:
            return outcome
        payload = refresh_status_payload(
            outcome.result, outcome.reason, outcome.decision,
            corpus_repo=corpus_repo, recipe_repo=recipe_repo,
            source_revision=outcome.source_revision,
            built_digest=outcome.built_digest, pinned_digest=outcome.pinned_digest,
            tag=outcome.tag, detail=outcome.detail)
        outcome.status_path = write_refresh_status(out_abs, payload)
        return outcome

    if skip_reason:
        return _emit(RefreshOutcome(RESULT_SKIPPED, skip_reason, None))

    try:
        if inputs is None:
            if read_inputs is None:
                return _emit(RefreshOutcome(
                    RESULT_SKIPPED, "no input reader configured", None))
            inputs = read_inputs()

        decision = decide_refresh(
            corpus_revision=inputs.corpus_revision,
            recipe_revision=inputs.recipe_revision,
            recorded=inputs.recorded,
            corpus_scope=corpus_scope, recipe_scope=recipe_scope)

        if decision.undecidable:
            return _emit(RefreshOutcome(
                RESULT_SKIPPED, decision.reason, decision,
                pinned_digest=inputs.pinned_digest,
                detail=list(inputs.errors)))
        if not decision.build:
            # THE SHORT-CIRCUIT. Nothing below this line runs: no checkout, no
            # snapshot generation, no image build, no push, no branch, no PR.
            return _emit(RefreshOutcome(
                RESULT_NO_CHANGE,
                f"{decision.reason}: corpus {_short(decision.corpus_revision)} "
                f"and recipe {_short(decision.recipe_revision)} both match the "
                "revisions recorded with the pinned image",
                decision, pinned_digest=inputs.pinned_digest))

        if build is None:
            # Decision-only run (the parent's pre-dispatch gate): movement is
            # reported, and the worker child performs the build.
            return _emit(RefreshOutcome(
                RESULT_SKIPPED,
                f"build required ({decision.reason}) but this run performs no "
                "build — the worker child owns the build and the push",
                decision, pinned_digest=inputs.pinned_digest))

        result = build(build_plan) if build_plan is not None else build()
        if not result.ok:
            return _emit(RefreshOutcome(
                RESULT_STRICT_FAILED if result.strict_failed else RESULT_SKIPPED,
                result.reason, decision, pinned_digest=inputs.pinned_digest,
                detail=list(result.detail)))

        prov = Provenance(
            corpus_repo=corpus_repo,
            # The comparand is recorded as the build's own re-read when it has
            # one (the fresh checkout is the authority on its own tree), else
            # the decision's read.
            corpus_revision=(result.corpus_revision or decision.corpus_revision or ""),
            corpus_scope=tuple(corpus_scope),
            recipe_repo=recipe_repo,
            recipe_revision=(decision.recipe_revision or ""),
            recipe_scope=tuple(recipe_scope),
            source_revision=result.source_revision,
            tag=result.tag,
            generated_at=_now_iso(),
            run_id=_run_id())

        outcome = RefreshOutcome(
            RESULT_OK, None, decision, built_digest=result.digest,
            pinned_digest=inputs.pinned_digest, tag=result.tag,
            source_revision=result.source_revision, provenance=prov,
            detail=list(result.detail))

        note = digest_note(result.digest, inputs.pinned_digest)
        if note:
            outcome.detail.append(note)

        if pin_out is not None and inputs.overlay_text is not None:
            pin_dir = Path(pin_out)
            pin_dir.mkdir(parents=True, exist_ok=True)
            rewritten = rewrite_pin(inputs.overlay_text, image, result.digest, prov)
            pin_path = pin_dir / Path(overlay_path).name
            pin_path.write_text(rewritten, encoding="utf-8")
            body_path = pin_dir / "pr-body.md"
            body_path.write_text(render_pr_body(
                prov=prov, digest=result.digest,
                previous_digest=inputs.pinned_digest, tag=result.tag or "",
                source_revision=result.source_revision, run_url=run_url,
                overlay_path=overlay_path), encoding="utf-8")
            outcome.pin_path = pin_path
            outcome.pr_body_path = body_path
        return _emit(outcome)
    except Exception as exc:  # noqa: BLE001 — the lane never fails the nightly
        return _emit(RefreshOutcome(
            RESULT_SKIPPED, f"{type(exc).__name__}: {exc}", None))


# --------------------------------------------------------------------------
# CLI. The PARENT's phases only — decide, seal, pin, report, record-pr. The
# build belongs to the worker child and lives in the child's own workflow; no
# phase here builds an image or pushes one, and the only source materialization
# is the parent's own `git archive` of a revision it already holds.
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    """CLI entry. Void by contract, like the snapshot lane's, but only for a
    VALID phase: every path through the lane's own logic for `decide`, `seal`,
    `pin`, `report` or `record-pr` — including a total failure, reported as
    SKIPPED (a refused seal included) — falls through and the process exits 0, so the deterministic doc-health
    results and the delivered report are never affected. A phase argparse
    itself refuses — an unknown value, including the retired `build` — is a
    USAGE error: argparse prints the fixed choice set and exits non-zero
    (`SystemExit(2)`) before any lane logic runs. That exit code is
    deliberately outside this contract; a workflow still spelling `--phase
    build` should fail loudly, not be swallowed into a silent no-op."""
    ap = argparse.ArgumentParser(
        prog="dashboard-refresh-nightly", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo-root", required=True,
                    help="the aggregation checkout root (where health/ lives)")
    ap.add_argument("--phase",
                    choices=("decide", "seal", "pin", "report", "record-pr"),
                    default="decide",
                    help="decide: the input-revision check only (the parent's "
                         "pre-dispatch gate). "
                         "seal: materialize the bounded source artifact the "
                         "credential-free child consumes — the decide phase's "
                         "own decision (--decision-in) at one revision, plus "
                         "the pinned recipe, plus a manifest — into "
                         "--seal-out, and write the dispatch gate to "
                         "--seal-result-out. "
                         "pin: render the pin proposal from the worker child's "
                         "returned digest (--digest-in) — this module writes "
                         "files and never pushes a branch. "
                         "report: append the delivered status artifact's outcome "
                         "to the dated report (runs BEFORE delivery, so it names "
                         "the previous run's outcome and says so). "
                         "record-pr: patch the pin pull request's reference onto "
                         "the status artifact the pin phase just wrote, once the "
                         "workflow's cross-repo branch delivery knows it "
                         "(--pull-request); best-effort, never fails the run. "
                         "There is deliberately NO build phase: the build "
                         "and the push belong to the worker child, and the "
                         "only materialization here is the parent's seal.")
    ap.add_argument("--out-dir", default=DEFAULT_OUT_DIR)
    ap.add_argument("--image", default=DEFAULT_IMAGE)
    ap.add_argument("--corpus-checkout", default="openxFactory",
                    help="local corpus checkout, relative to --repo-root")
    ap.add_argument("--corpus-repo", default=DEFAULT_CORPUS_REPO)
    ap.add_argument("--corpus-ref", default=DEFAULT_CORPUS_REF)
    ap.add_argument("--recipe-repo", default=DEFAULT_RECIPE_REPO)
    ap.add_argument("--recipe-ref", default=DEFAULT_RECIPE_REF)
    ap.add_argument("--overlay-path", default=DEFAULT_OVERLAY_PATH)
    ap.add_argument("--pin-out", default=None,
                    help="directory to render the pin proposal into (the "
                         "rewritten overlay + the PR body); the workflow does "
                         "the branch delivery, this module never pushes")
    ap.add_argument("--decision-out", default=None,
                    help="write the decision as JSON for the workflow to gate on")
    ap.add_argument("--decision-in", default=None,
                    help="the decide phase's own --decision-out file "
                         "(--phase seal): the seal records the revisions the "
                         "decision was made on, so the child can refuse a "
                         "seal that does not match its dispatch")
    ap.add_argument("--seal-out", default=None,
                    help="directory to materialize the bounded source "
                         "artifact into (--phase seal); the workflow uploads "
                         "it, this module never dispatches")
    ap.add_argument("--seal-result-out", default=None,
                    help="write the seal result as JSON (--phase seal): the "
                         "dispatch gate, plus the values the child's own "
                         "intake check compares against")
    ap.add_argument("--correlation-id", default=None,
                    help="the readiness correlation id (--phase seal); the "
                         "artifact is named "
                         f"{SEAL_ARTIFACT_PREFIX}<correlation-id>")
    ap.add_argument("--recipe-path", default=RECIPE_DOCKERFILE_PATH,
                    help="the recipe file to seal, read from --recipe-repo at "
                         "the decision's recipe revision (--phase seal)")
    ap.add_argument("--parent-repository", default=None,
                    help="the parent run's repository, recorded in the "
                         "manifest so the child's cross-run download has the "
                         "provenance it names (--phase seal)")
    ap.add_argument("--digest-in", default=None,
                    help="the worker child's returned digest record "
                         "(--phase pin): digest, tag, source_revision, "
                         "corpus_revision")
    ap.add_argument("--skip-reason", default=None,
                    help="the readiness verdict: skip fail-closed, read nothing")
    ap.add_argument("--run-url", default=None)
    ap.add_argument("--pull-request", default=None,
                    help="the pin pull request's reference to record on the "
                         "delivered status artifact (--phase record-pr)")
    ap.add_argument("--report-in", default=None,
                    help="dated report to append the refresh section to "
                         "(--phase report)")
    ap.add_argument("--stuck-pull-request", default=None,
                    help="a pin pull request still open at this run — the "
                         "clearest available signal that the chain is parked")
    args = ap.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()

    if args.phase == "report":
        status = read_status_artifact(repo_root / args.out_dir)
        section = render_report_section(
            status, this_run_id=_run_id(),
            stuck_pull_request=args.stuck_pull_request)
        if args.report_in and append_report_section(args.report_in, section):
            print(f"{LANE}: report section appended to {args.report_in}")
        else:
            print(f"{LANE}: report section NOT appended "
                  f"(--report-in={args.report_in!r})")
        if args.stuck_pull_request:
            print(f"::warning::{LANE}: pin pull request "
                  f"{args.stuck_pull_request} is still open — the refresh chain "
                  "is parked")
        return

    if args.phase == "seal":
        # THE PARENT SEAL. Never raises out of here: like every other path in
        # this lane a refusal is a RECORDED outcome and exit 0, and the
        # workflow gates the dispatch on `sealed` rather than on this
        # process's status. A refused seal costs one cycle of served-plane
        # freshness — the same bounded cost the readiness skip costs — and the
        # next run catches up in one hop.
        try:
            decision = json.loads(
                Path(args.decision_in).read_text(encoding="utf-8"))
        except (OSError, TypeError, json.JSONDecodeError) as exc:
            decision, load_error = {}, f"{type(exc).__name__}: {exc}"
        else:
            load_error = None
        manifest: dict | None = None
        if load_error is not None:
            reason = (f"no usable parent decision ({args.decision_in!r}): "
                      f"{load_error}")
        elif not args.seal_out:
            reason = "no --seal-out directory was given"
        else:
            try:
                manifest = seal_source(
                    corpus_checkout=repo_root / args.corpus_checkout,
                    seal_dir=Path(args.seal_out),
                    correlation_id=args.correlation_id or "",
                    decision=decision,
                    corpus_repo=args.corpus_repo, corpus_ref=args.corpus_ref,
                    recipe_repo=args.recipe_repo,
                    recipe_path=args.recipe_path,
                    parent_repository=(args.parent_repository
                                       or os.environ.get("GITHUB_REPOSITORY")),
                    parent_run_id=_run_id())
                reason = None
            except SealRefused as exc:
                reason = str(exc)
            except Exception as exc:  # noqa: BLE001 — a seal never fails the run
                reason = f"{type(exc).__name__}: {exc}"
        payload = seal_result_payload(sealed=manifest is not None, reason=reason,
                                      manifest=manifest)
        if args.seal_result_out:
            try:
                Path(args.seal_result_out).write_text(
                    json.dumps(payload, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
            except OSError as exc:
                print(f"  ::warning::could not write the seal result: {exc}")
        if manifest is not None:
            print(f"::notice::{LANE}: SEALED {manifest['artifact_name']} — "
                  f"source_head={_short(manifest['source_head'])}, "
                  f"{manifest['file_count']} files, "
                  f"{manifest['total_bytes']} bytes, "
                  f"tree_digest={manifest['tree_digest'][:12]}")
        else:
            print(f"::warning::{LANE}: NOT SEALED — {reason}; nothing "
                  "dispatched, next run catches up in one hop")
        return

    if args.phase == "record-pr":
        # The pin phase wrote this run's status; the workflow's cross-repo
        # branch delivery has now opened (or advanced) the PR and hands its
        # reference back here to patch onto that status. Best-effort, like
        # every write in this lane: a status that cannot be updated must never
        # become the reason a landed pin is reported as a failure.
        ok = record_pull_request(repo_root / args.out_dir, args.pull_request)
        print(f"{LANE}: pull-request reference "
              f"{'recorded on' if ok else 'NOT recorded on'} the delivered "
              f"status ({args.pull_request!r})")
        return

    def _read() -> CurrentInputs:
        return read_current_inputs(
            corpus_checkout=repo_root / args.corpus_checkout,
            corpus_ref=args.corpus_ref, recipe_repo=args.recipe_repo,
            recipe_ref=args.recipe_ref, overlay_path=args.overlay_path,
            image=args.image)

    build = None
    if args.phase == "pin":
        # The worker child built and pushed; its ONLY result is the digest.
        # Re-running the decision here is deliberate and cheap: the pin must
        # not be rendered on inputs that moved out from under the build.
        try:
            record = json.loads(Path(args.digest_in).read_text(encoding="utf-8"))
        except (OSError, TypeError, json.JSONDecodeError) as exc:
            print(f"{LANE}: SKIPPED — no usable digest record "
                  f"({args.digest_in!r}): {exc}")
            return
        result = BuildResult(
            bool(record.get("digest")),
            None if record.get("digest") else "the child returned no digest",
            digest=record.get("digest"), tag=record.get("tag"),
            source_revision=record.get("source_revision"),
            corpus_revision=record.get("corpus_revision"))

        def build(plan=None, _result=result):  # noqa: ARG001 — signature parity
            return _result

    outcome = run_refresh_lane(
        repo_root, out_dir=args.out_dir, image=args.image,
        corpus_repo=args.corpus_repo, recipe_repo=args.recipe_repo,
        overlay_path=args.overlay_path, read_inputs=_read, build=build,
        pin_out=args.pin_out, run_url=args.run_url,
        skip_reason=args.skip_reason)

    print(outcome.annotation())
    print(outcome.log_line())
    if outcome.status_path is not None:
        print(f"  status: {outcome.status_path}")
    if args.decision_out:
        decision = outcome.decision
        try:
            Path(args.decision_out).write_text(json.dumps({
                "build": bool(decision.build) if decision else False,
                "outcome": decision.outcome if decision else "undecidable",
                "reason": decision.reason if decision else (outcome.reason or ""),
                "result": outcome.result,
                "corpus_revision": decision.corpus_revision if decision else None,
                "recipe_revision": decision.recipe_revision if decision else None,
            }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        except OSError as exc:
            print(f"  ::warning::could not write the decision file: {exc}")


if __name__ == "__main__":
    main()
