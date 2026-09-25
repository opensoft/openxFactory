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

  * the CORPUS input revision — openxFactory, the last commit touching its
    baked inputs (`CORPUS_BAKED_PATHS`): the eight paths the Dockerfile
    copies, plus the render unit that makes the snapshot it copies (the two
    product gitlinks and the host bootstrap, #1161);
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
(`verify_one_revision`) — never the generation of the snapshot the image
bakes, the build or the assertion's call site. The parent's pre-dispatch
render (`precheck_sealed_render`) renders the same seal only to run the
child's publication gate early; its snapshot is discarded and never baked.

`--strict` IS THE PUBLICATION GATE and it precedes the push. Zero errors AND
zero warnings, and a validator that could not RUN fails too; a non-zero exit
means no tag, no push, no digest, no branch, no pull request — there is nothing
to retract because nothing was published. The child's run of it is the gate.
The parent runs the same sealed validator over the same sealed render first,
so a seal the gate would refuse is recorded as `strict_failed`, with the
validator's own output, and is never dispatched.

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
parent already has, the same of the two pinned product code legs that render
the snapshot, one contents read of the single-file recipe, and a copy of the
pinned openxdox product's own validator composed with its schemas, which the
parent RUNS once before it seals, so a copy that cannot run never reaches the
child. Then the parent renders the snapshot FROM THE SEAL, through the same
entry point the child will run, and runs the sealed validator over it under
`--strict`: a seal whose snapshot the child's publication gate would refuse is
never dispatched, and the refusal carries the validator's own findings. See
the seal section for why the validator comes from the product rather than the
corpus, and why the render unit is sealed where it is.

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
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from output_boundary import OutputBoundary  # noqa: E402

LANE = "ideation-dashboard-refresh"
STATUS_NAME = "refresh-status.json"
DEFAULT_OUT_DIR = "health/ideation-dashboard"

# What the served plane's Dockerfile COPIES out of the corpus (`COPY
# openxFactory/...` plus the two script packages), which correctly ignores
# `tests/` and `experiments/` (169 MB, referenced by zero docs).
CORPUS_COPIED_PATHS: tuple[str, ...] = (
    "contracts",
    "docs",
    "examples",
    "ideation",
    "openspec",
    "scripts/doc_health",
    "scripts/ideation_dashboard",
    "templates",
)

# THE RENDER UNIT'S CORPUS SIDE (openxFactory #1161). The image bakes the
# SNAPSHOT as well as the corpus, and the snapshot is whatever the renderer
# makes of the corpus, so the renderer is a baked input too. Until the
# split-opendox § 5.2 shed (`cc4ae9d3`) it lived in `scripts/ideation_dashboard`,
# which the Dockerfile also copies, so the copied set covered it by coincidence.
# The shed moved it to the pinned openDox and openXdox products. openxFactory
# reaches them through its own pin (RULED Q7) and its own host bootstrap, so the
# renderer is now the two product gitlinks plus five files: the entry, and the
# four its host bootstrap is made of (`RENDER_BOOTSTRAP`). MEASURED, not listed
# from memory: an audit hook over the real render (`RENDER_ENTRY generate`) at
# `57af6927` opened nothing else under `scripts/` outside the two copied
# packages, and nothing under either product outside its code leg's `src/`.
# A test repeats that measurement, so a render that grows an import outside
# this set fails in the suite rather than in the child.
#
# A gitlink path is a path `git log` answers for, so a product re-pin is corpus
# movement exactly as a renderer edit in `scripts/ideation_dashboard` was.
RENDER_LEG_GITLINKS: tuple[str, ...] = ("openDox", "openXdox")
# The product's own command line, behind openxFactory's host bootstrap. The
# worker child runs it from the sealed corpus root, and so does the parent's
# own pre-dispatch render.
RENDER_ENTRY = "scripts/ideation-dashboard-cli.py"
CORPUS_RENDER_PATHS: tuple[str, ...] = (
    *RENDER_LEG_GITLINKS,
    "scripts/carved_reach.py",
    RENDER_ENTRY,
    "scripts/opendox_host.py",
    "scripts/profile_openxfactory.py",
    "scripts/wire_messages.py",
)
# The host bootstrap the entry imports before it reaches either product: the
# render paths less the two gitlinks and the entry itself. The intake requires
# each one, since a seal missing any of them fails only once the render starts.
RENDER_BOOTSTRAP: tuple[str, ...] = tuple(
    path for path in CORPUS_RENDER_PATHS
    if path not in RENDER_LEG_GITLINKS and path != RENDER_ENTRY)

# The corpus repository's BAKED INPUTS: what the image copies, plus what
# renders the snapshot it copies. This is the decision's scope. Sorted, because
# the tuple is written into the pin as the SCOPE the comparison was made with
# and two spellings of one scope would read as a scope change.
CORPUS_BAKED_PATHS: tuple[str, ...] = tuple(
    sorted({*CORPUS_COPIED_PATHS, *CORPUS_RENDER_PATHS}))

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


def exact_git(repo_dir, *arguments: str) -> list[str]:
    """The argv of an EXACT-CONTENT git read the seal makes:
    `git --no-replace-objects -C <repo> ...`. Pass it with
    `env=exact_git_environment()`.

    Every read and archive the seal's record depends on goes through it: the
    revision reads, the committer date, the gitlink reads and both archives.
    A replace ref would otherwise hand `git archive` another commit's tree
    under the pinned commit's name, and the archive's own recorded revision
    would still read as the pin (Copilot, PR #1166). The decision's
    path-scoped `log` and its `fetch` are not exact-content reads and keep the
    plain form."""
    return ["git", "--no-replace-objects", "-C", str(repo_dir), *arguments]


def exact_git_environment() -> dict[str, str]:
    """The environment of an `exact_git` read: `carved_reach`'s scrubbed,
    replacement-free one, REUSED rather than copied, as
    `scripts/carve_test_mapping.py` and the carve-conformance verifier reuse
    it. An ambient `GIT_DIR`, alternate object directory, command-scoped
    configuration or replace-ref base would otherwise make `-C <repo>` read
    some other store than the checkout named (Copilot, PR #1166)."""
    from carved_reach import _sanitized_git_environment
    return _sanitized_git_environment()


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
    caller, not its reason to exist. An exact-content read (`exact_git`)."""
    result = runner(exact_git(repo_dir, "rev-parse", ref),
                    env=exact_git_environment())
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
# THE VALIDATOR COMES FROM THE PRODUCT, NOT FROM THE CORPUS (openxFactory
# #1158). Until the split-opendox § 5.2 shed (`cc4ae9d3`, #940) the seal set
# was `CORPUS_BAKED_PATHS ∪ {scripts/validate-ideation-dashboard-contracts.py}`:
# `snapshot.find_validator` walked UP to that TOP-LEVEL file, and a `git
# archive` over the baked path list does not carry it. The shed moved the file
# to openXdox-code, and from then on asking the archive for it refused EVERY
# real corpus (`fatal: pathspec 'scripts/validate-ideation-dashboard-
# contracts.py' did not match any files`, measured at `1edbb3dd`). The presence
# check behind it named a file this repository no longer carries. Two more
# facts close the old route for good. From openXdox-code `e28930bf` the locator
# CONFINES to the product's own tree (split-opendox-two-layer-product § 8.9
# residue (iii)), so it never adopts a copy a seal puts outside that tree. And
# FOUND IS NOT RUNNABLE: at the code leg the script reads no `contracts/` of
# its own, and exits 2 before it reads a snapshot (#1157).
#
# So the validator is resolved by the SNAPSHOT LANE'S OWN resolver,
# `nightly_lane._pinned_validator()`: the product's validator, composed with
# its schemas by `doxbench_contracts._composed_validator`. The seal carries
# that composed unit as regular files under its own root, `validator/`
# (`scripts/` beside `contracts/schemas/`), where the script's own `parents[1]`
# is the unit and its schemas resolve. Then the parent RUNS the sealed copy
# once, through the product's own `snapshot.validate_snapshot` in an
# allowlisted environment, over a minimal snapshot-kind probe, and refuses
# unless the validator reached a verdict. So
# what the child's `--strict` runs is a byte-for-byte copy of the unit the
# snapshot lane validates with, and that copy has run once, here, to a verdict.
# The probe's verdict is not a verdict on the corpus and is never read as one:
# judging the corpus stays the child's `--strict`.
#
# The validator's path is not in the decision scope: adding it would make
# `_same_scope` fire `REASON_SCOPE_CHANGED` against every recorded pin and
# force one rebuild for nothing. The old asymmetry holds in its new shape: the
# validator is sealed but not baked. `validator/` sits BESIDE the corpus rather
# than under it, so no context root the child copies out of the corpus can
# reach it, and the image cannot COPY it.
#
# THE RENDER UNIT RIDES INSIDE THE CORPUS HALF (openxFactory #1161). The child
# used to render with `python -m ideation_dashboard.cli` out of the sealed
# `scripts/`. The shed moved that module to openDox-code, so the child found
# nothing to run. The renderer is now the pinned products behind openxFactory's
# host bootstrap (`CORPUS_RENDER_PATHS`), so the seal carries both halves of
# it, laid out where the SEALED tree's own `carved_reach` looks for them:
#
#   * the bootstrap files, by the same `git archive` as the rest of the corpus
#     (`CORPUS_SEAL_PATHS` is the baked set less the two gitlinks, which an
#     archive cannot carry the contents of);
#   * each product's code leg, at the commit the SEALED CORPUS pins it at, as
#     `git archive` of its `src/` from the leg this parent has materialized,
#     extracted under `openxFactory/<gitlink>/<leg>/`. The pinned commit is
#     read from `source_head`'s own tree, never from the checkout's HEAD, and
#     the materialized leg must BE that commit. A parent whose legs sit at
#     another pin refuses by name rather than rendering main's corpus with a
#     renderer main does not pin. The legs are also where the sealed validator
#     is resolved from, so the same check keeps the renderer and the validator
#     one product revision.
#
# Then the parent RENDERS FROM THE SEAL, through `RENDER_ENTRY`, exactly as the
# child will, and runs the sealed validator over the result under `--strict`
# (`precheck_sealed_render`). A render that fails is a refusal. A render the
# validator rejects is a refusal the lane records as `strict_failed`, with the
# validator's own findings, and nothing is dispatched. The snapshot is written
# outside the seal and discarded: the child still generates the one the image
# bakes, and the child's `--strict` is still the publication gate.
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
# 2.0.0 FROM #1158, AND THE MAJOR MOVES ON PURPOSE. A 1.x seal carried its
# validator INSIDE the corpus, at `openxFactory/scripts/validate-ideation-
# dashboard-contracts.py`, and a 1.x reader looks for it there. A 2.x seal
# carries the product's validator at `SEAL_VALIDATOR_RELPATH` instead. That
# makes it a layout a 1.x reader cannot consume. The right refusal is "not a
# major this reader reads", which is legible. A reader expecting 1.x that
# refused over a "missing" validator would name a file the seal does carry,
# only elsewhere.
#
# 2.1.0 FROM #1161, AND ONLY THE MINOR MOVES. The corpus half now carries the
# render unit (`render_entry`, `render_legs`) and the manifest records the
# parent's pre-dispatch render (`precheck`). Every 2.0.0 field keeps its name,
# place and meaning, so a 2.0 reader still reads the seal. A 2.1 reader
# refuses a 2.0 seal by what it lacks, naming it: a seal with no render unit
# is one the child could not render from.
SEAL_SCHEMA_VERSION = "2.1.0"
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

# The corpus half's `git archive` pathspec: the baked set less the two product
# gitlinks, whose CONTENTS an archive of this repository cannot carry. They are
# sealed as legs instead (`RENDER_LEGS`). The one path that used to widen the
# set left the corpus at the shed (see the section note above). The manifest
# records it as `seal_paths`, beside `corpus_baked_paths`; a reader comparing
# the two finds them differing by exactly `RENDER_LEG_GITLINKS`, and finds
# those under `render_legs`.
CORPUS_SEAL_PATHS: tuple[str, ...] = tuple(
    path for path in CORPUS_BAKED_PATHS if path not in RENDER_LEG_GITLINKS)

# The render unit's product half: each product gitlink, the leg under it that
# carries the code, and the package that leg must carry. It is the layout
# `carved_reach.LEGS` reads, so the sealed tree's own bootstrap finds each leg
# where it looks. Only `src/` travels: the measured render reads nothing else
# of either leg.
RENDER_LEGS: tuple[tuple[str, str, str], ...] = (
    ("openDox", "code", "opendox"),
    ("openXdox", "code", "openxdox"),
)
RENDER_LEG_PATHS: tuple[str, ...] = ("src",)
# Each product's OTHER leg. Nothing of it is sealed as a leg, but the sealed
# validator's schemas are composed from it (`doxbench_contracts.
# _composed_validator`, through the carve rows), so it is held to its pin as
# the code leg is, and its revision is recorded beside the code leg's.
SCHEMA_LEG = "spec"
# The one leg the sealed validator is resolved from. Its revision is held
# equal to `validator_revision`, so the renderer and the validator are one
# product revision (see `seal_source`).
VALIDATOR_LEG = ("openXdox", "code")
# The product module the parent classifies the sealed validator's runs with,
# inside the sealed validator leg's package: the product's own
# three-outcome `validate_snapshot`.
SEALED_PRODUCT_MODULE = "snapshot.py"

# The sealed validator unit, and its layout. `VALIDATOR_SCRIPT_PATH` is the
# script's path INSIDE the unit. It is also the product's own
# `snapshot.VALIDATOR_RELPATH`, and a test holds the two equal. It is spelled
# here rather than imported because this module must import without the carve
# legs on disk. The unit sits at `SEAL_VALIDATOR_ROOT`, beside the corpus and
# the recipe, so it is sealed and never baked.
SEAL_VALIDATOR_ROOT = "validator"
VALIDATOR_SCRIPT_PATH = "scripts/validate-ideation-dashboard-contracts.py"
VALIDATOR_SCHEMAS_PATH = "contracts/schemas"
SEAL_VALIDATOR_RELPATH = f"{SEAL_VALIDATOR_ROOT}/{VALIDATOR_SCRIPT_PATH}"

# The one instance the parent runs the sealed validator over. It is a
# snapshot-kind document with nothing else in it. The validator can reach a
# verdict on it (exit 1, findings) only when it launches from the seal, reads
# the unit's own `contracts/schemas/`, and has loaded the snapshot schema. It
# exits 2, a harness failure that `snapshot.validate_snapshot` reports as
# unavailable, when that schema or every schema is missing. "Available" on
# this probe therefore means the sealed copy RUNS, over the schema the child
# validates against. That the copy carries the rest of the unit is held by
# the copy itself (`seal_validator` refuses an entry it cannot copy), not by
# the probe: the validator asks for another family schema only when an
# instance needs it. Measured on the composed unit: rc 1 with 9 findings.
# Without the snapshot schema: rc 2. With no schemas: rc 2.
VALIDATOR_PROBE = {"kind": "ideation-dashboard-snapshot"}

# What a 2.x seal's intake requires of the unit beyond its script. First, the
# schema the child validates against, by the name the product's own validator
# asks for it; a test drops exactly this name and has the product refuse,
# naming it. Second, the outcomes of the parent's one run that mean the copy
# RAN to a verdict: the product's `snapshot.VALIDATED` and
# `snapshot.NOT_CONFORMANT`, which a test holds equal. Both are spelled here
# because this module must import without the carve legs on disk.
VALIDATOR_SNAPSHOT_SCHEMA = "ideation-dashboard-snapshot.schema.yaml"
VALIDATOR_VERDICT_OUTCOMES = ("validated", "not-conformant")

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


class StrictGateRejected(SealRefused):
    """The sealed validator REJECTED, under `--strict`, the snapshot this seal
    renders. The child's publication gate would refuse the same snapshot, so
    nothing is dispatched.

    A SUBCLASS, deliberately. Every caller that handles a refusal handles this
    one: no manifest is written and no child is dispatched. It is the one
    refusal that is a verdict ON THE CORPUS rather than a fault of the parent,
    so it also carries the validator's own output, bounded, and the lane
    records it as `strict_failed` rather than as a skip."""

    def __init__(self, message: str, detail=()) -> None:
        super().__init__(message)
        self.detail = [str(line) for line in detail][:DETAIL_CAP]


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


def _contained_relpath(root, relpath: str) -> Path:
    """A relative path named by the seal — a `manifest["files"]` key, a
    `seal_paths` entry, the validator path — made safe to join under `root`.
    THE CONTAINMENT CHECK RUNS BEFORE ANY JOIN OR OPEN.

    `verify_seal` is the reference implementation of the CHILD's intake check
    (S3): the manifest it reads is exactly as trustworthy as whatever tampered
    it, so a `files` key of `../../etc/passwd` or `/etc/passwd` must never
    reach `root / relpath` at all, let alone `is_file()` or a hash read.
    Refuses, in this order: an unusable (empty or non-string) value; a
    backslash anywhere (never a valid separator here, and exactly what an
    attacker reaches for once forward slashes and `..` are refused — it would
    also defang a Windows-style absolute path, which is not otherwise
    `PurePosixPath.is_absolute`); a leading `/`; any `.`, `..`, or empty
    ('a//b', 'a/') component; a symlink at ANY component of the path — walked
    root to leaf, so a symlinked ancestor directory that itself resolves back
    inside `root` is still refused, because it is not the file the manifest
    named; and finally a resolved location outside `root`
    (`is_relative_to`), which also catches whatever the literal-component
    walk cannot.

    Raises `SealRefused`; never returns a path outside `root`. Shared by the
    seal WRITER (`seal_file_index`, `seal_source`) and the reference VERIFIER
    (`verify_seal`) so the two enforce one rule rather than two that could
    drift apart."""
    root = Path(root)
    value = relpath if isinstance(relpath, str) else ""
    if not value:
        raise SealRefused(f"the seal names an unusable path: {relpath!r}")
    if "\\" in value:
        raise SealRefused(
            f"the seal names a path with a backslash: {relpath!r}")
    if value.startswith("/"):
        raise SealRefused(f"the seal names an absolute path: {relpath!r}")
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise SealRefused(f"the seal names an unsafe path: {relpath!r}")
    root_resolved = root.resolve()
    candidate = root
    for part in parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise SealRefused(
                f"the seal names a symlinked path: {relpath!r}")
    resolved = candidate.resolve()
    if not resolved.is_relative_to(root_resolved):
        raise SealRefused(
            f"the seal names a path outside the seal: {relpath!r}")
    return candidate


def seal_file_index(seal_dir) -> dict[str, str]:
    """Every regular file under the seal, by POSIX relative path, to its
    sha256. The manifest itself is excluded — it carries this index and cannot
    hash itself — and a non-regular entry is a refusal rather than a skip:
    `upload-artifact@v4` neither preserves symlinks nor restores execute bits,
    so an index that silently omitted one would promise something the download
    cannot deliver. `_contained_relpath` is applied to every entry too, so the
    writer refuses the same symlinked or escaping path the reference verifier
    would (Copilot, PR #648) — the walk already lands on real filesystem
    entries, so this is belt-and-suspenders, not the primary gate."""
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
        contained = _contained_relpath(root, relpath)
        index[relpath] = file_sha256(contained)
    return index


# Whether this platform opens a file relative to a directory handle. Every
# parent the nightly runs on does. One that cannot falls back to paths.
_DIR_FD = os.open in os.supports_dir_fd and os.stat in os.supports_dir_fd


def _open_directory(path) -> int | None:
    """A handle on the directory at `path`, opened without following a link
    at its last component, or None where the platform opens nothing relative
    to a handle."""
    if not _DIR_FD:
        return None
    return os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                   | getattr(os, "O_NOFOLLOW", 0))


def _replaced_seal_directory() -> SealRefused:
    return SealRefused(
        "the seal directory is no longer the one the lane created: sealed "
        "code ran inside it, and the manifest is never written anywhere else")


def _seal_directory_identity(seal_dir) -> tuple[int, int]:
    """The seal directory as created, as `(st_dev, st_ino)`. It must be a
    directory, not a link to one."""
    info = os.lstat(seal_dir)
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        raise SealRefused(
            f"the seal directory {seal_dir} is not a directory of its own "
            "(a link, or not a directory at all)")
    return info.st_dev, info.st_ino


def _occupied_manifest_path(what: str) -> SealRefused:
    return SealRefused(
        f"the seal already holds a {SEAL_MANIFEST_NAME} the lane did not write "
        f"({what}): sealed code runs before the manifest is written, and the "
        "manifest is never written through anything it left")


def _refuse_an_occupied_manifest_path(seal_dir) -> None:
    """Refuse the seal when anything at all sits at the manifest's path: a
    file, a directory, or a symbolic link, dangling or not."""
    path = Path(seal_dir) / SEAL_MANIFEST_NAME
    if path.is_symlink():
        raise _occupied_manifest_path("a symbolic link")
    if path.is_dir():
        raise _occupied_manifest_path("a directory")
    if os.path.lexists(path):
        raise _occupied_manifest_path("a file")


def _create_new_file(target, data: bytes, *, dir_fd=None) -> None:
    """Create `target`, which must not exist yet, and write `data` to it.
    `O_EXCL` fails on ANY existing entry, a link included, wherever it
    points, so the bytes land at `target` itself or nowhere. Raises
    `FileExistsError` when something is already there."""
    flags = (os.O_WRONLY | os.O_CREAT | os.O_EXCL
             | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_BINARY", 0))
    descriptor = os.open(target, flags, 0o666, dir_fd=dir_fd)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(data)


def _write_new_manifest(seal_dir, text: str, *, identity=None) -> None:
    """Create the manifest, which must not exist yet. `O_EXCL` fails on ANY
    existing entry, a symbolic link included, wherever it points, so the bytes
    land at the manifest's own path or nowhere.

    It is created relative to a handle on the seal directory, opened without
    following a link. With `identity`, the directory as created, the handle
    must be that very directory, so a seal directory replaced after it was
    created is refused rather than written into (Copilot, PR #1166)."""
    try:
        directory = _open_directory(seal_dir)
    except OSError as exc:
        raise _replaced_seal_directory() from exc
    try:
        if directory is not None and identity is not None:
            info = os.fstat(directory)
            if (info.st_dev, info.st_ino) != tuple(identity):
                raise _replaced_seal_directory()
        target = (SEAL_MANIFEST_NAME if directory is not None
                  else Path(seal_dir) / SEAL_MANIFEST_NAME)
        try:
            _create_new_file(target, text.encode("utf-8"), dir_fd=directory)
        except FileExistsError as exc:
            raise _occupied_manifest_path(
                "one that appeared while the lane was writing it") from exc
    finally:
        if directory is not None:
            os.close(directory)


# THE SEAL RESULT IS THE LANE'S OWN FILE (Copilot, PR #1166). It sits outside
# the seal, at a fixed path the workflow reads to gate the dispatch, and
# sealed code runs before it is written. So its path is cleared before the
# seal starts, and anything found there afterwards is an entry sealed code
# made: the seal is refused, the entry is removed without being followed,
# and the lane's own result is created in its place, exclusively.
SEAL_RESULT_PLANTED = (
    "the seal result's path held an entry the lane did not write: sealed "
    "code ran before the result was written, so the seal is refused rather "
    "than dispatched")


def _clear_result_path(path) -> None:
    """Remove whatever sits at `path` without following it: a file or a link
    is unlinked, and a directory is left for the exclusive create to refuse."""
    try:
        info = os.lstat(path)
    except FileNotFoundError:
        return
    if not stat.S_ISDIR(info.st_mode):
        os.unlink(path)


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
    # The query `generator.RealGitDates.commit_date` makes, `--`
    # end-of-options marker included, so the stamp the child receives through
    # `--generated-at` is the SAME STRING the pre-seal child derived inside
    # its own checkout — the change moves where the value comes from, never
    # what it says, and the snapshot stays byte-identical across it. It runs
    # as an exact-content read (`exact_git`), which changes the answer only
    # where a replace ref would have changed it.
    result = runner(exact_git(repo_dir, "show", "-s", "--format=%cI",
                              revision, "--"),
                    env=exact_git_environment())
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


def _refuse_unsafe_member(name: str, dest: Path) -> None:
    """Refuse a tar entry that could be written outside `dest`.

    Checked on the MEMBER NAMES, before extraction, and therefore on BOTH
    extraction branches. The `data` filter below would catch these on a modern
    interpreter, but the `TypeError` fallback for an interpreter without
    extraction filters would not, and "the archive is produced by git so its
    names are fine" is exactly the assumption an extraction hazard is made of.
    """
    if not name or name.startswith("/") or name.startswith("\\"):
        raise SealRefused(
            f"the source archive holds an absolute member path: {name!r}")
    parts = PurePosixPath(name).parts
    if ".." in parts or PurePosixPath(name).is_absolute():
        raise SealRefused(
            f"the source archive holds a traversing member path: {name!r}")
    resolved = (dest / name).resolve()
    if resolved != dest.resolve() and dest.resolve() not in resolved.parents:
        raise SealRefused(
            f"the source archive member {name!r} would be written outside the "
            "seal")


def _extract_seal_archive(archive_path, dest) -> int:
    """Extract the archive under `dest`. Refuses any entry that is not a plain
    file or a directory, and any entry whose name could land outside `dest`,
    BEFORE extracting anything — then extracts under the `data` filter where
    the interpreter has one."""
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
                _refuse_unsafe_member(member.name, dest)
            try:
                archive.extractall(dest, filter="data")
            except TypeError:      # an interpreter without extraction filters
                archive.extractall(dest)
            return sum(1 for member in members if member.isfile())
    except tarfile.TarError as exc:
        raise SealRefused(
            f"the source archive could not be read: {exc}") from exc
    except OSError as exc:
        raise SealRefused(
            f"the source archive could not be extracted: {exc}") from exc


def _decision_field(decision: dict, key: str) -> str:
    value = str((decision or {}).get(key) or "").strip().lower()
    if not _FULL_REVISION_RE.match(value):
        raise SealRefused(
            f"the parent decision carries no usable {key} ({value or 'absent'!r})")
    return value


@dataclass(frozen=True)
class PinnedValidator:
    """The validator the seal will carry, as its resolver answered.

    `runnable` is the COMPOSED script. Its `parents[1]` is a self-contained unit
    holding `scripts/` beside `contracts/schemas/`, and that unit is what the
    seal copies. `product_root` is the product tree the validator was found in.
    It is read only to record which revision the sealed copy came from, and
    None records none."""

    runnable: Path
    product_root: Path | None = None


def _snapshot_lane():
    """`nightly_lane`, imported LAZILY, and only by the seal.

    It cannot be imported everywhere this module is. It reads `openxdox` from
    the pinned carve legs at import, and a checkout whose legs are not
    materialized refuses that import by name
    (`carved_reach.CarveReachUnavailable`, an `ImportError`). The decide, pin,
    report and record-pr phases must keep running in such a checkout. That is
    the case for the nightly's finalize job today (openxFactory #1161).
    """
    from ideation_dashboard import nightly_lane
    return nightly_lane


def resolve_pinned_validator() -> PinnedValidator:
    """THE SNAPSHOT LANE'S OWN RESOLVER, `nightly_lane._pinned_validator()`.

    This is the same function the snapshot lane validates with. It resolves the
    product's own validator, composed with its schemas, so the two lanes cannot
    come to disagree about which validator is the pinned one (#1157, #1158).
    Nothing here re-derives it.

    It raises `SealRefused`, naming where the validator was looked for, when
    none can be resolved: the carve legs are not on disk, or the product tree
    carries no validator. It never returns None."""
    unreachable = ("the child's validator would be unreachable and --strict "
                   "would fail with no finding to read")
    try:
        nightly_lane = _snapshot_lane()
        runnable = nightly_lane._pinned_validator()
    except ImportError as exc:  # `CarveReachUnavailable` is one
        raise SealRefused(
            "the pinned openxdox validator cannot be resolved on this parent "
            f"({type(exc).__name__}: {exc}) — {unreachable}") from exc
    if runnable is None:
        raise SealRefused(
            "the pinned openxdox validator was not found "
            f"({nightly_lane._pinned_validator_missing()}) — {unreachable}")
    return PinnedValidator(runnable=Path(runnable),
                           product_root=nightly_lane.snapshot_mod.product_root())


def _validator_said(result) -> str:
    """The validator's own last line, from stderr first, so a refusal carries its
    words and not only an exit code. Bounded, because it lands in one status
    field."""
    for stream in (result.stderr, result.stdout):
        lines = [line.strip() for line in (stream or "").splitlines()
                 if line.strip()]
        if lines:
            return lines[-1][:400]
    return ""


def _enclosing_repository(path: Path) -> Path | None:
    """The nearest directory at or above `path` that holds a `.git` of its
    own: the repository, or a submodule's worktree, a file belongs to."""
    for parent in path.parents:
        if (parent / ".git").exists():
            return parent
    return None


def _uncommitted_unit_sources(pinned: PinnedValidator, *,
                              runner=subprocess_runner) -> list[str]:
    """Each file the composed unit was built from that its repository's HEAD
    does not hold as it is: modified, untracked, ignored, or in no repository
    at all. Empty when every one is committed.

    The unit is composed from WORKTREES (Copilot, PR #1166): the script is
    copied from the product's code leg, and each schema is a link into a
    product's spec leg or into this checkout. The seal holds those HEADs to
    their pins, but a HEAD says nothing about uncommitted bytes. So each
    source is asked of its own repository, and the copied script is also held
    equal to the file it was copied from."""
    sources = [Path(pinned.product_root) / VALIDATOR_SCRIPT_PATH]
    problems: list[str] = []
    if (not sources[0].is_file() or Path(pinned.runnable).read_bytes()
            != sources[0].read_bytes()):
        problems.append(f"{VALIDATOR_SCRIPT_PATH} (the unit's copy is not the "
                        f"file at {pinned.product_root})")
    schemas = Path(pinned.runnable).parents[1] / VALIDATOR_SCHEMAS_PATH
    if schemas.is_dir():
        sources += [entry.resolve() for entry in sorted(schemas.iterdir())]
    by_repository: dict[Path, list[str]] = {}
    for source in sources:
        repository = _enclosing_repository(source)
        if repository is None:
            problems.append(f"{source} (in no repository)")
            continue
        by_repository.setdefault(repository, []).append(
            source.relative_to(repository).as_posix())
    for repository, relpaths in by_repository.items():
        result = runner(exact_git(repository, "status", "--porcelain=v1",
                                  "--untracked-files=all", "--ignored=matching",
                                  "--", *relpaths),
                        env=exact_git_environment())
        if not result.ok:
            problems.append(f"{repository} (its status could not be read)")
            continue
        problems += [f"{repository.name}/{line[3:]} ({line[:2].strip()})"
                     for line in result.stdout.splitlines() if line.strip()]
    return problems


def seal_validator(seal_root, pinned: PinnedValidator, *,
                   runner=subprocess_runner) -> dict:
    """Copy the pinned validator's composed unit into the seal, then RUN the
    sealed copy once. It returns the manifest's validator fields. It raises
    `SealRefused` when the product's revision cannot be read, when the unit
    cannot be copied whole, or when the sealed copy cannot run.

    REGULAR FILES ONLY. The composed unit is a script COPY beside schema LINKS
    to the pinned bytes. `upload-artifact@v4` preserves no symlink, and
    `seal_file_index` refuses one, so each schema is copied THROUGH its link:
    the seal holds the pinned bytes, never the link. An entry that does not
    resolve to a regular file (a dangling link, a directory) is REFUSED by
    name, never skipped. Skipping it would seal a narrower unit than the one
    the snapshot lane validates with, and the probe below could not see the
    difference: the validator asks for a family schema only when an instance
    needs it.

    THE RUN IS OF THE SEALED COPY, from inside the seal. It goes through the
    product's own three-outcome `snapshot.validate_snapshot`, which is the call
    the snapshot lane makes, over `VALIDATOR_PROBE`. "Available" is the only
    thing it reads: the probe's own verdict is a finding by construction, and
    it is never a verdict on the corpus. The probe lives in a scratch directory
    outside the seal, so nothing it touches is sealed. The copy is sealed code,
    so it runs in the pre-dispatch render's allowlisted environment, not this
    job's, and its run is classified by the SEALED product module
    (`validate_in_render_environment`, `sealed_product_module`). The render
    legs are sealed before this runs."""
    # WHICH PRODUCT REVISION the copy comes from, read FIRST. A unit resolved
    # from a product source tree records that tree's HEAD. A HEAD that cannot
    # be read as a full revision REFUSES the seal, because the manifest
    # promises that provenance and a null would silently drop it. Only a unit
    # with no product tree at all (an injected stand-in) records none.
    revision = None
    if pinned.product_root is not None:
        head = (git_head_revision(pinned.product_root, runner=runner)
                or "").strip().lower()
        if not _FULL_REVISION_RE.match(head):
            read = repr(head) if head else "nothing"
            raise SealRefused(
                "could not resolve the pinned product's revision at "
                f"{pinned.product_root} to a commit (read {read}) — the sealed "
                "validator's provenance would go unrecorded")
        revision = head
        # THE UNIT'S BYTES ARE COMMITTED BYTES. A revision is recorded, and
        # held equal to the sealed leg's, only for bytes that revision holds.
        dirty = _uncommitted_unit_sources(pinned, runner=runner)
        if dirty:
            raise SealRefused(
                "the validator unit is composed from uncommitted bytes: "
                f"{', '.join(dirty[:5])}"
                + (f" and {len(dirty) - 5} more" if len(dirty) > 5 else "")
                + " — the seal would carry a validator no commit describes, "
                "so it could not be held to the render's revision")
    root = Path(seal_root) / SEAL_VALIDATOR_ROOT
    script = root / VALIDATOR_SCRIPT_PATH
    script.parent.mkdir(parents=True)
    shutil.copyfile(pinned.runnable, script)
    schemas = root / VALIDATOR_SCHEMAS_PATH
    # Created even when the unit has none, deliberately. The validator prefers
    # its OWN `contracts/schemas/` whenever that directory exists, so an ambient
    # `CONTRACTS_DIR` can never stand in for a schema the seal does not carry.
    schemas.mkdir(parents=True)
    carried = 0
    source = Path(pinned.runnable).parents[1] / VALIDATOR_SCHEMAS_PATH
    if source.is_dir():
        for entry in sorted(source.iterdir(), key=lambda path: path.name):
            if not entry.is_file():    # follows the link to the pinned bytes
                raise SealRefused(
                    f"the composed validator unit carries {entry.name}, which "
                    f"does not resolve to a regular file ({entry}) — sealing "
                    "it without that entry would seal a narrower unit than "
                    "the one the snapshot lane validates with")
            shutil.copyfile(entry, schemas / entry.name)
            carried += 1
    try:
        product = _snapshot_lane().snapshot_mod
    except ImportError as exc:
        raise SealRefused(
            "the sealed validator cannot be run on this parent "
            f"({type(exc).__name__}: {exc})") from exc
    # THE PROBE IS SEALED CODE TOO, run with the seal writable. So the tree
    # it runs in is indexed before it runs and again after, and a probe that
    # changed it is refused (Copilot, PR #1166).
    before = seal_file_index(seal_root)
    with tempfile.TemporaryDirectory(prefix="dfr-probe-") as scratch:
        probe = Path(scratch) / "validator-probe.json"
        probe.write_text(json.dumps(VALIDATOR_PROBE, sort_keys=True) + "\n",
                         encoding="utf-8")
        result = validate_in_render_environment(
            product, probe, validator=script, strict=False,
            seal_root=seal_root,
            module_file=sealed_product_module(seal_root))
    if seal_file_index(seal_root) != before:
        raise SealRefused(
            "the sealed validator's probe changed the sealed tree, so the "
            "seal would no longer be the tree its validator was run in")
    if not result.available:
        said = _validator_said(result)
        raise SealRefused(
            "the sealed validator could NOT RUN, so the child's --strict "
            f"could not run it either: {result.unavailable_reason}"
            + (f" — it said: {said}" if said else ""))
    return {
        "validator_relpath": SEAL_VALIDATOR_RELPATH,
        "validator_revision": revision,
        "validator_schema_count": carried,
        "validator_probe": {"kind": VALIDATOR_PROBE["kind"],
                            "outcome": result.outcome,
                            "returncode": result.returncode},
    }


def _gitlink_at(repo_dir, treeish: str, path: str, *,
                runner=subprocess_runner) -> str | None:
    """The commit `treeish` pins at `path`, read out of that tree, or None when
    the entry is not a gitlink.

    `git ls-tree <treeish> -- <path>` prints `160000 commit <sha>\\t<path>` for
    a gitlink. It is asked of the tree being SEALED, never of the checkout's
    HEAD: this parent's corpus checkout sits at the aggregation's pin, and the
    seal is of `source_head`."""
    result = runner(exact_git(repo_dir, "ls-tree", treeish, "--", path),
                    env=exact_git_environment())
    if not result.ok:
        return None
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        return None
    meta, _, name = lines[0].partition("\t")
    fields = meta.split()
    if name != path or len(fields) != 3 or fields[:2] != ["160000", "commit"]:
        return None
    sha = fields[2].strip().lower()
    return sha if _FULL_REVISION_RE.match(sha) else None


def _materialized_head(checkout, *, runner=subprocess_runner) -> str | None:
    """The HEAD of a submodule checkout this parent HAS, or None.

    `.git` must be present AT the directory. An unmaterialized gitlink is an
    empty directory, and `git -C` from inside one climbs to the SUPERPROJECT
    and answers that repository's HEAD instead, which would read as a
    materialized leg at the wrong commit."""
    if not (Path(checkout) / ".git").exists():
        return None
    head = (git_head_revision(checkout, runner=runner) or "").strip().lower()
    return head if _FULL_REVISION_RE.match(head) else None


def seal_render_legs(*, corpus_checkout, source_head: str, corpus_root,
                     runner=subprocess_runner) -> list[dict]:
    """Seal each product's code leg under the sealed corpus, at the commit the
    SEALED corpus pins it at. Returns the manifest's `render_legs` records.

    For each `RENDER_LEGS` entry, the product commit comes from `source_head`'s
    own tree, and the leg commit comes from THAT product commit's tree. The
    checkout this parent materialized must be exactly those two commits. The
    leg's `src/` is then archived at its commit, the archive's own recorded
    revision is checked as the corpus half's is, and it is extracted where the
    sealed tree's own `carved_reach` looks for it.

    NOTHING IS FETCHED. The legs are the ones the finalize job materialized for
    the snapshot lane, and a parent whose legs sit at another pin than
    `source_head`'s REFUSES, naming both: sealing main's corpus with a renderer
    main does not pin would publish a snapshot no pin describes.

    Raises `SealRefused`, naming the gitlink, for anything it cannot prove."""
    corpus_checkout = Path(corpus_checkout)
    corpus_root = Path(corpus_root)
    init = "`git submodule update --init --recursive openDox openXdox`"
    sealed: list[dict] = []
    for gitlink, leg, package in RENDER_LEGS:
        pinned = _gitlink_at(corpus_checkout, source_head, gitlink,
                             runner=runner)
        if pinned is None:
            raise SealRefused(
                f"{_short(source_head)} pins no {gitlink} gitlink, so the "
                "render unit cannot be sealed and the child would have no "
                "renderer to run")
        product = corpus_checkout / gitlink
        head = _materialized_head(product, runner=runner)
        if head is None:
            raise SealRefused(
                f"the pinned {gitlink} product is not materialized at "
                f"{product}, and the render unit is sealed from it — run "
                f"{init} in the corpus checkout")
        if head != pinned:
            raise SealRefused(
                f"this parent's {gitlink} is at {_short(head)}, but "
                f"{_short(source_head)} pins {gitlink}@{_short(pinned)} — the "
                "seal would render the corpus with a product it does not pin. "
                "The parent materializes the products the aggregation's "
                "openxFactory pin names; its next pin-sync brings them level, "
                "and the next run seals")
        leg_pinned = _gitlink_at(product, pinned, leg, runner=runner)
        if leg_pinned is None:
            raise SealRefused(
                f"{gitlink}@{_short(pinned)} pins no {leg} leg, so the render "
                "unit cannot be sealed")
        leg_dir = product / leg
        leg_head = _materialized_head(leg_dir, runner=runner)
        if leg_head is None:
            raise SealRefused(
                f"the {gitlink} {leg} leg is not materialized at {leg_dir} — "
                f"run {init} in the corpus checkout")
        if leg_head != leg_pinned:
            raise SealRefused(
                f"this parent's {gitlink}/{leg} is at {_short(leg_head)}, but "
                f"{gitlink}@{_short(pinned)} pins it at {_short(leg_pinned)} "
                "— the seal would carry a leg its product does not pin")
        schema_pinned = _schema_leg_at_its_pin(product, gitlink, pinned, init,
                                               runner=runner)
        dest = corpus_root / gitlink / leg
        with tempfile.TemporaryDirectory(prefix="dfr-leg-") as staging:
            archive_path = Path(staging) / "leg.tar"
            result = runner(exact_git(leg_dir, "archive", "--format=tar",
                                      f"--output={archive_path}", leg_pinned,
                                      "--", *RENDER_LEG_PATHS),
                            env=exact_git_environment())
            if not result.ok:
                raise SealRefused(
                    f"git archive of the {gitlink} {leg} leg failed at "
                    f"{_short(leg_pinned)}: {result.stderr.strip()[:200]}")
            recorded = git_archive_revision(archive_path)
            if recorded != leg_pinned:
                raise SealRefused(
                    f"the {gitlink} {leg} leg archive's own recorded revision "
                    f"({recorded or 'absent'}) is not its pinned commit "
                    f"({leg_pinned})")
            count = _extract_seal_archive(archive_path, dest)
        modules = dest / "src" / package
        if not (modules.is_dir() and any(modules.glob("*.py"))):
            raise SealRefused(
                f"the sealed {gitlink} {leg} leg carries no module under "
                f"src/{package}, so the child's bootstrap would refuse it")
        sealed.append({
            "gitlink": gitlink,
            "gitlink_revision": pinned,
            "leg": leg,
            "leg_revision": leg_pinned,
            "package": package,
            "relpath": f"{SEAL_CORPUS_RELPATH}/{gitlink}/{leg}",
            "paths": list(RENDER_LEG_PATHS),
            "file_count": count,
            "schema_leg": SCHEMA_LEG,
            "schema_leg_revision": schema_pinned,
        })
    return sealed


def _schema_leg_at_its_pin(product: Path, gitlink: str, pinned: str,
                           init: str, *, runner=subprocess_runner) -> str:
    """The commit `gitlink@pinned` pins its `SCHEMA_LEG` at, once this parent's
    checkout of that leg is proven to BE that commit (Copilot, PR #1166). The
    sealed validator's schemas are composed from this checkout, so one at
    another commit would seal schema bytes no pin describes."""
    schema_pinned = _gitlink_at(product, pinned, SCHEMA_LEG, runner=runner)
    if schema_pinned is None:
        raise SealRefused(
            f"{gitlink}@{_short(pinned)} pins no {SCHEMA_LEG} leg, so the "
            "sealed validator's schemas would have no pin")
    schema_dir = product / SCHEMA_LEG
    schema_head = _materialized_head(schema_dir, runner=runner)
    if schema_head is None:
        raise SealRefused(
            f"the {gitlink} {SCHEMA_LEG} leg is not materialized at "
            f"{schema_dir}, and the sealed validator's schemas are composed "
            f"from it — run {init} in the corpus checkout")
    if schema_head != schema_pinned:
        raise SealRefused(
            f"this parent's {gitlink}/{SCHEMA_LEG} is at "
            f"{_short(schema_head)}, but {gitlink}@{_short(pinned)} pins it at "
            f"{_short(schema_pinned)} — the seal would carry schemas its "
            "product does not pin")
    return schema_pinned


# The repository id the pre-dispatch render names, the one the child's own
# generate passes. The snapshot lane and the served image use the same id.
RENDER_REPOSITORY = "openxFactory"
# The one pre-dispatch outcome a manifest can record: the product's own
# `snapshot.VALIDATED` spelling, restated so `verify_seal` never imports the
# product (a test holds the two equal).
PRECHECK_VALIDATED = "validated"
# Measured at `57af6927`: about five seconds for the real corpus. The bound is
# for a render that hangs, not for a slow one. Each run of the sealed
# validator gets the same bound, because the product's own call has none, and
# a validator that hangs must not hold the rest of the nightly.
PRECHECK_TIMEOUT_SECONDS = 600
# The ONLY variables of this job's environment the pre-dispatch render
# receives, by name, and by prefix for the locale. It runs code read out of the
# seal, and this job holds the App token, a token-bearing git configuration and
# whatever else the runner exports. So the environment is BUILT from an
# allowlist rather than filtered by a denylist, which would pass any
# credential it had not thought to name (Copilot, PR #1166). What is kept is
# what an interpreter needs to start and read files in this locale:
# `LD_LIBRARY_PATH` because the runner's toolcache interpreter can load its
# own shared library from it; the Windows system variables because a child on
# a Windows rider runs the same entry. The child's worker holds no
# credential to begin with.
_RENDER_ENV_KEPT = ("PATH", "LD_LIBRARY_PATH", "LANG", "LANGUAGE", "TZ",
                    "TMPDIR", "TEMP", "TMP", "SYSTEMROOT", "SYSTEMDRIVE",
                    "WINDIR", "COMSPEC", "PATHEXT")
_RENDER_ENV_KEPT_PREFIXES = ("LC_",)


def _render_environment(seal_root, home) -> dict[str, str]:
    """The environment of the parent's pre-dispatch render: the allowlisted
    variables (`_RENDER_ENV_KEPT`), and nothing else of this job's.

    Beyond them, the settings below make the render the child's. `HOME` is a
    scratch directory. No bytecode is written, so the render cannot add a file
    to the tree the index is about to cover. `git` may not climb out of the
    seal: this parent's seal sits INSIDE the aggregation checkout, while the
    child's has no repository above it. And git reads no global or system
    configuration."""
    env = {key: value for key, value in os.environ.items()
           if key in _RENDER_ENV_KEPT
           or key.startswith(_RENDER_ENV_KEPT_PREFIXES)}
    env.update({
        "HOME": str(home),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONIOENCODING": "utf-8",
        "GIT_CEILING_DIRECTORIES": str(Path(seal_root).resolve()),
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
    })
    return env


# THE SEALED VALIDATOR RUNS IN THAT ENVIRONMENT TOO (Copilot, PR #1166). The
# product's `snapshot.validate_snapshot` launches the validator with no `env`
# of its own. Called in THIS process, it would hand the sealed copy every
# credential the job holds. So the call is made in a fresh interpreter whose
# whole environment is `_render_environment`'s, working in a scratch
# directory. It is still the product's own function, with its own three-outcome
# reading, and everything it launches inherits the allowlist. The module is
# the SEALED one, out of the seal's openXdox leg (`sealed_product_module`):
# the exact code the seal carries, never this parent's worktree, which could
# be dirty (Copilot, PR #1166). The harness ends without a verdict if the
# name resolves to any other file. It hands the product's result back as the
# last line of its stdout. The validator's own output never reaches that
# stream, because the product captures it.
_VALIDATE_HARNESS = """\
import json, sys
from pathlib import Path
module_file, target, validator, strictness = sys.argv[1:5]
if sys.path and sys.path[0] == "":
    sys.path.pop(0)
sys.path.insert(0, str(Path(module_file).parents[1]))
from openxdox import snapshot
if Path(snapshot.__file__).resolve() != Path(module_file).resolve():
    sys.exit(f"openxdox.snapshot resolved to {snapshot.__file__}, not to "
             f"{module_file}")
result = snapshot.validate_snapshot(Path(target), validator=Path(validator),
                                    strict=strictness == "strict")
print(json.dumps({"ok": result.ok, "returncode": result.returncode,
                  "stdout": result.stdout, "stderr": result.stderr,
                  "outcome": result.outcome,
                  "unavailable_reason": result.unavailable_reason}))
"""
# The shape of the verdict the harness prints: each field, and its type.
_HARNESS_VERDICT_SHAPE = {"ok": bool, "returncode": int, "stdout": str,
                          "stderr": str, "outcome": str}


def _harness_verdict(stdout, outcomes) -> dict | None:
    """The product's result as the harness printed it, on the last line of its
    stdout, or None when that line is not one: not JSON, not an object, a
    field missing or of another type, or an outcome not in `outcomes`."""
    lines = [line for line in (stdout or "").splitlines() if line.strip()]
    if not lines:
        return None
    try:
        verdict = json.loads(lines[-1])
    except ValueError:
        return None
    if not isinstance(verdict, dict):
        return None
    if any(type(verdict.get(name)) is not kind
           for name, kind in _HARNESS_VERDICT_SHAPE.items()):
        return None
    if not isinstance(verdict.get("unavailable_reason"), (str, type(None))):
        return None
    return verdict if verdict["outcome"] in outcomes else None


def sealed_product_module(seal_root) -> Path:
    """Where the seal carries the product module the validator's runs are
    classified with: `SEALED_PRODUCT_MODULE` in the sealed `VALIDATOR_LEG`'s
    package."""
    package = next(package for gitlink, leg, package in RENDER_LEGS
                   if (gitlink, leg) == VALIDATOR_LEG)
    gitlink, leg = VALIDATOR_LEG
    return (Path(seal_root).resolve() / SEAL_CORPUS_RELPATH / gitlink / leg
            / "src" / package / SEALED_PRODUCT_MODULE)


def validate_in_render_environment(product, target, *, validator, strict: bool,
                                   seal_root, module_file,
                                   run=subprocess.run,
                                   timeout: int = PRECHECK_TIMEOUT_SECONDS):
    """The product's own `validate_snapshot(target, validator=...,
    strict=...)`, imported from `module_file` and run in the pre-dispatch
    render's environment rather than this job's (see `_VALIDATE_HARNESS`).
    Returns a `ValidationResult`, the parent's `product` supplying only that
    record's type and the outcome spellings.

    Git may climb neither out of the seal nor out of the scratch directory the
    validator runs in. A harness that cannot be launched, does not finish, or
    returns no verdict is reported the way the product reports a validator
    that cannot run: outcome `VALIDATOR_UNAVAILABLE`, with the reason. Nothing
    is then known about the target, and both callers refuse on that
    outcome."""
    validator = Path(validator).resolve()
    module_file = Path(module_file).resolve()

    def unavailable(reason: str, *, returncode: int = -1, stderr: str = ""):
        return product.ValidationResult(
            False, returncode, "", stderr, validator,
            product.VALIDATOR_UNAVAILABLE, reason)

    with tempfile.TemporaryDirectory(prefix="dfr-validate-") as scratch:
        scratch_root = Path(scratch).resolve()
        home = scratch_root / "home"
        home.mkdir()
        env = _render_environment(seal_root, home)
        env["GIT_CEILING_DIRECTORIES"] = os.pathsep.join(
            (env["GIT_CEILING_DIRECTORIES"], str(scratch_root.parent)))
        argv = [sys.executable, "-c", _VALIDATE_HARNESS, str(module_file),
                str(Path(target).resolve()), str(validator),
                "strict" if strict else "lenient"]
        try:
            proc = run(argv, cwd=str(scratch_root), env=env,
                       capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return unavailable(f"the validator did not finish within {timeout}s")
        except OSError as exc:
            return unavailable(
                "the validator could not be launched in the render's "
                f"environment ({type(exc).__name__}: {exc})")
    verdict = _harness_verdict(
        proc.stdout, (product.VALIDATED, product.NOT_CONFORMANT,
                      product.VALIDATOR_UNAVAILABLE))
    if proc.returncode != 0 or verdict is None:
        # Its stderr is kept, since a harness that could not import the product
        # says why there. Its stdout carries nothing but a verdict line.
        return unavailable(
            f"the validator's harness returned no verdict (exit "
            f"{proc.returncode})", returncode=proc.returncode,
            stderr=proc.stderr or "")
    return product.ValidationResult(
        verdict["ok"], verdict["returncode"], verdict["stdout"],
        verdict["stderr"], validator, verdict["outcome"],
        verdict["unavailable_reason"])


# STRICT FINDINGS THAT HAVE A TRACKING ISSUE: (finding code, the value the
# finding names, the issue). A rejection whose findings include one is cited
# against that issue, so a reader of the nightly learns that this is the known
# defect and where it is tracked, rather than a new breakage. The match is on
# the validator's own finding code AND the value it names, so the citation
# retires itself. Once the corpus is fixed the finding is gone, and a
# different rejection is never cited against an issue that is not its own.
KNOWN_STRICT_FINDINGS = (
    ("snapshot-dangling-cluster-ref", "'cl-plane-1'",
     "opensoft/openxFactory#1159"),
)
# The validator's per-finding lines: `ERROR [<code>] <path>: <message>`, and
# the same shape for a warning.
_FINDING_LINE_RE = re.compile(r"^(ERROR|WARNING) \[([a-z0-9-]+)\] ")


def _output_lines(result, *, scrub=(), cap: int | None = DETAIL_CAP) -> list[str]:
    """A process's own output, stdout then stderr, blank lines dropped, capped
    at `cap` (None for every line): the per-finding record a one-line reason
    cannot carry. Each `scrub` path is replaced by its file name, so a finding
    names `snapshot.json` rather than this parent's scratch directory."""
    lines: list[str] = []
    for stream in (getattr(result, "stdout", ""), getattr(result, "stderr", "")):
        for line in (stream or "").splitlines():
            if line.strip():
                for path in scrub:
                    line = line.replace(str(path), Path(path).name)
                lines.append(line.rstrip())
    return lines if cap is None else lines[:cap]


def known_finding_citation(lines) -> str:
    """Which tracking issues `KNOWN_STRICT_FINDINGS` cites for these findings,
    as one clause, or "" when none applies.

    The clause says how many of the findings are the known ones, so a
    rejection that ALSO carries a new finding never reads as fully tracked."""
    findings = [line for line in lines if _FINDING_LINE_RE.match(line)]
    issues: list[str] = []
    tracked = 0
    for line in findings:
        code = _FINDING_LINE_RE.match(line).group(2)
        hits = [issue for known, value, issue in KNOWN_STRICT_FINDINGS
                if code == known and value in line]
        if hits:
            tracked += 1
            issues += [issue for issue in hits if issue not in issues]
    if not issues:
        return ""
    untracked = len(findings) - tracked
    return (f"known defect, tracked as {', '.join(issues)} ({tracked} of "
            f"{len(findings)} finding(s)"
            + (f"; {untracked} tracked by no known issue" if untracked else "")
            + ")")


def _not_a_file_of_its_own(info: os.stat_result) -> str:
    """What `info` is, when it is anything but a regular file with one link;
    "" when it is one."""
    if stat.S_ISLNK(info.st_mode):
        return "a symbolic link"
    if stat.S_ISDIR(info.st_mode):
        return "a directory"
    if not stat.S_ISREG(info.st_mode):
        return "not a regular file"
    if info.st_nlink != 1:
        return "a hard link to another file"
    return ""


def _render_output_refused(what: str) -> SealRefused:
    return SealRefused(
        f"the sealed render's output is {what}, not a file of its own, so "
        "the parent will not read it: a link could hand the parent any file "
        "on this host to validate and quote")


def _render_output_present(name, *, dir_fd=None) -> bool:
    """Whether anything at all sits at `name`, relative to `dir_fd` when it is
    given, a dangling link included."""
    try:
        os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
    except FileNotFoundError:
        return False
    return True


def _read_render_output(name, *, dir_fd=None) -> bytes:
    """The bytes the sealed render wrote at `name`, which must be a regular
    file of its own: not a symbolic link, not a hard link, nothing else. The
    render is sealed code, and a link would have the parent validate, and
    quote in its findings, whatever file on this host it named (Copilot,
    PR #1166). `name` is read relative to `dir_fd`, a handle on the directory
    the parent made, when one is given, so a directory swapped in on the way
    to it cannot redirect the read. The file is opened without following a
    link and checked again through the open descriptor, so a swap after the
    first check is refused too."""
    try:
        before = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
    except OSError as exc:
        raise SealRefused(
            f"the sealed render's output cannot be read ({exc})") from exc
    what = _not_a_file_of_its_own(before)
    if what:
        raise _render_output_refused(what)
    flags = (os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
             | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_BINARY", 0))
    try:
        descriptor = os.open(name, flags, dir_fd=dir_fd)
    except OSError as exc:
        raise _render_output_refused(
            f"something that could not be opened without following a link "
            f"({exc.strerror})") from exc
    with os.fdopen(descriptor, "rb") as handle:
        after = os.fstat(handle.fileno())
        what = _not_a_file_of_its_own(after)
        if not what and (after.st_dev, after.st_ino) != (before.st_dev,
                                                         before.st_ino):
            what = "a file that was swapped after it was checked"
        if what:
            raise _render_output_refused(what)
        return handle.read()


def _run_the_sealed_render(entry, corpus_root, seal_root, home, snapshot,
                           output, scratch_fd, *, source_head: str,
                           source_committed_at: str, run, timeout: int) -> bytes:
    """Run `RENDER_ENTRY generate` from the sealed corpus root, as the child
    does, writing `snapshot`, and return the bytes it wrote. They are read
    through `scratch_fd`, the handle on the directory `snapshot` was made in,
    under the name `output` (`_read_render_output`)."""
    argv = [sys.executable, str(entry), "generate",
            "--repo-root", str(corpus_root),
            "--repository", RENDER_REPOSITORY,
            "--source-revision", source_head,
            "--generated-at", source_committed_at,
            "--output", str(snapshot), "--no-validate"]
    try:
        proc = run(argv, cwd=str(corpus_root),
                   env=_render_environment(seal_root, home),
                   capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise SealRefused(
            f"the sealed render did not finish within {timeout}s, so the "
            "child's generate would not either") from exc
    except OSError as exc:
        raise SealRefused(
            f"the sealed render could not be launched: {exc}") from exc
    if (proc.returncode != 0
            or not _render_output_present(output, dir_fd=scratch_fd)):
        said = _validator_said(proc)
        raise SealRefused(
            "the sealed render unit could not render the snapshot (exit "
            f"{proc.returncode}), so the child's generate would fail the "
            "same way" + (f": {said}" if said else ""))
    return _read_render_output(output, dir_fd=scratch_fd)


def precheck_sealed_render(seal_root, *, source_head: str,
                           source_committed_at: str,
                           run=subprocess.run,
                           timeout: int = PRECHECK_TIMEOUT_SECONDS) -> dict:
    """Render the snapshot FROM THE SEAL and run the sealed validator over it
    under `--strict`, exactly as the child will. Returns the manifest's
    `precheck` record.

    THE CHILD'S OWN INVOCATION, in the child's own tree. `RENDER_ENTRY` runs
    from the sealed corpus root, with the seal's two anchors as its
    `--source-revision` and `--generated-at`, and `--no-validate` because
    validation is the sealed unit's job. Then the sealed validator runs over
    the result, through the product's own three-outcome `validate_snapshot`,
    as the probe does. Both run in the allowlisted environment
    (`_render_environment`, `validate_in_render_environment`), never in this
    job's. The snapshot is written to a scratch directory outside the seal and
    discarded. The child generates the one the image bakes, and the child's
    `--strict` stays the publication gate.

    Every path either run is handed is absolute. The nightly names its seal
    relative to the job's working directory (`--seal-out dfr-seal`), and the
    render runs from inside the seal, where a relative path would name
    nothing.

    Raises `SealRefused` when the render fails, when it drops either anchor,
    or when the validator cannot run. Raises `StrictGateRejected`, carrying
    the validator's own output, when the validator REJECTS the snapshot. That
    is a verdict on the corpus, and the lane records it as one."""
    seal_root = Path(seal_root).resolve()
    corpus_root = seal_root / SEAL_CORPUS_RELPATH
    entry = corpus_root / RENDER_ENTRY
    validator = seal_root / SEAL_VALIDATOR_RELPATH
    try:
        product = _snapshot_lane().snapshot_mod
    except ImportError as exc:
        raise SealRefused(
            "the sealed render cannot be checked on this parent "
            f"({type(exc).__name__}: {exc})") from exc
    # `ignore_cleanup_errors`, because the render may have left the scratch
    # path a link, which the cleanup refuses to follow; the refusal below is
    # the one to report.
    with tempfile.TemporaryDirectory(prefix="dfr-precheck-",
                                     ignore_cleanup_errors=True) as scratch:
        scratch_root = Path(scratch)
        snapshot = scratch_root / "snapshot.json"
        scrub = (snapshot.resolve(), snapshot)
        home = scratch_root / "home"
        home.mkdir()
        # THE SCRATCH DIRECTORY IS HELD BEFORE THE RENDER RUNS (Copilot, PR
        # #1166). The render may replace its path with a link to another
        # directory. The output is read through this handle, from the
        # directory this parent made, whatever the path names afterwards.
        scratch_fd = _open_directory(scratch_root)
        output = snapshot.name if scratch_fd is not None else snapshot
        try:
            written = _run_the_sealed_render(
                entry, corpus_root, seal_root, home, snapshot, output,
                scratch_fd, source_head=source_head,
                source_committed_at=source_committed_at, run=run,
                timeout=timeout)
        finally:
            if scratch_fd is not None:
                os.close(scratch_fd)
        try:
            rendered = json.loads(written.decode("utf-8"))
        except ValueError as exc:
            raise SealRefused(
                f"the sealed render wrote no readable snapshot ({exc})") from exc
        generation = rendered.get("generation") if isinstance(rendered, dict) \
            else None
        generation = generation if isinstance(generation, dict) else {}
        if (generation.get("source_revision") != source_head
                or generation.get("generated_at") != source_committed_at):
            raise SealRefused(
                "the sealed render did not carry the seal's two anchors "
                f"(source_revision {generation.get('source_revision')!r}, "
                f"generated_at {generation.get('generated_at')!r}), so the "
                "child's one-revision assertion would refuse it")
        documents = rendered.get("documents")
        document_count = len(documents) if isinstance(documents, list) else 0
        # THE VALIDATOR JUDGES THE BYTES READ ABOVE, from a copy in a
        # directory made after the render exited. Nothing the render left
        # behind can stand between what was checked and what is judged.
        with tempfile.TemporaryDirectory(prefix="dfr-judged-") as judged_dir:
            judged = Path(judged_dir).resolve() / snapshot.name
            judged.write_bytes(written)
            scrub = (*scrub, judged)
            result = validate_in_render_environment(
                product, judged, validator=validator, strict=True,
                seal_root=seal_root,
                module_file=sealed_product_module(seal_root), run=run,
                timeout=timeout)
    if not result.available:
        said = _validator_said(result)
        raise SealRefused(
            "the sealed validator could NOT RUN over the snapshot this seal "
            f"renders, so the child's --strict could not either: "
            f"{result.unavailable_reason}"
            + (f" — it said: {said}" if said else ""))
    if not result.ok:
        # EVERY line is read for the citation, and the detail the verdict
        # carries is capped afterwards (`StrictGateRejected`). A tracked
        # finding past the cap is still cited (Copilot, PR #1166).
        findings = _output_lines(result, scrub=scrub, cap=None)
        citation = known_finding_citation(findings)
        raise StrictGateRejected(
            f"--strict REJECTED the snapshot this seal renders "
            f"({result.summary()})"
            + (f", a {citation}" if citation else "")
            + "; the child's publication gate would refuse it the same way, "
            "so nothing is dispatched",
            detail=findings)
    return {"entry": RENDER_ENTRY, "documents": document_count,
            "strict": True, "outcome": result.outcome,
            "returncode": result.returncode}


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
    resolve_validator=None,
    seal_legs=None,
    precheck_render=None,
) -> dict:
    """Materialize the bounded source artifact and return its manifest.

    Order matters and is the order of the refusals:
      * a decision that did not ask for a build seals nothing;
      * a revision that cannot be resolved seals nothing;
      * a validator that cannot be resolved seals nothing, and is found out
        BEFORE the corpus is archived, since the corpus no longer supplies it;
      * a render leg that `source_head` does not pin, that this parent has not
        materialized at exactly that pin, or whose archive does not record it
        seals nothing, and so does a product whose schema leg this parent
        holds at any other commit than its pin; both are found out before the
        corpus is archived;
      * an archive whose own recorded commit is not `source_head` seals
        nothing;
      * a validator whose product revision cannot be read, whose unit cannot
        be copied whole, whose sealed copy cannot RUN, or whose run changed
        the sealed tree seals nothing;
      * a validator copied from another revision of the product than the
        sealed openXdox leg seals nothing;
      * a recipe that cannot be read seals nothing;
      * a sealed render unit that cannot render the snapshot, or a sealed
        validator that cannot run over it, seals nothing;
      * a snapshot the sealed validator REJECTS under `--strict` seals
        nothing, and is raised as `StrictGateRejected`, carrying the
        validator's own findings;
      * a pre-dispatch render that changed the sealed tree, or replaced the
        seal directory itself, seals nothing;
      * a `manifest.json` the lane did not write, left by the sealed code that
        ran before it, seals nothing.
    Only a seal that passed all twelve gets a `manifest.json`, and the
    manifest's presence is therefore the artifact's own statement that the
    parent stands behind it.

    `resolve_validator`, `seal_legs` and `precheck_render` are injectable for
    the same reason `read_recipe` is. Left None they are
    `resolve_pinned_validator` (the snapshot lane's own resolver),
    `seal_render_legs` and `precheck_sealed_render`.

    Raises `SealRefused` — never returns a partial seal."""
    decision = decision or {}
    # Canonicalized ONCE, here, because the artifact NAME and the manifest's
    # `correlation_id` are compared against each other by the child: a value
    # with surrounding whitespace would otherwise be stripped for the name and
    # recorded unstripped in the manifest, and the child's own check would
    # refuse a perfectly good seal over a space.
    correlation_id = (correlation_id or "").strip()
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
    # THE VALIDATOR IS RESOLVED BEFORE THE CORPUS IS ARCHIVED. It no longer
    # comes out of the corpus, so nothing about it waits for the corpus, and a
    # parent that cannot resolve it is told so before the whole corpus
    # (44,492,413 bytes at `1edbb3dd`) is archived for nothing. It is SEALED
    # and RUN below, once the seal tree exists.
    pinned = (resolve_validator or resolve_pinned_validator)()
    seal_root.mkdir(parents=True, exist_ok=True)
    # THE SEAL DIRECTORY AS CREATED. Sealed code runs inside it before the
    # manifest is written (the probe and the render), so the manifest is
    # written only into this very directory (Copilot, PR #1166).
    seal_identity = _seal_directory_identity(seal_root)
    corpus_root = seal_root / SEAL_CORPUS_RELPATH
    # THE RENDER LEGS ARE SEALED BEFORE THE CORPUS IS ARCHIVED, for the reason
    # the validator is resolved first: a parent whose legs sit at another pin
    # than `source_head`'s is told so before the corpus is archived for
    # nothing. Neither archive touches the other's paths: `seal_paths` names
    # no gitlink, so the corpus extract lands beside the legs.
    render_legs = (seal_legs or seal_render_legs)(
        corpus_checkout=corpus_checkout, source_head=source_head,
        corpus_root=corpus_root, runner=runner)
    # The intermediate tar lives OUTSIDE the seal (and outside the checkout):
    # it is not part of the artifact, and `git archive --output=` means the
    # bytes never pass through this module's text-mode runner.
    with tempfile.TemporaryDirectory(prefix="dfr-seal-") as staging:
        archive_path = Path(staging) / "source.tar"
        result = runner(exact_git(corpus_checkout, "archive", "--format=tar",
                                  f"--output={archive_path}", source_head,
                                  "--", *seal_paths),
                        env=exact_git_environment())
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
    if not any(_contained_relpath(corpus_root, path.split("/", 1)[0]).exists()
               for path in seal_paths):
        raise SealRefused(
            "the sealed corpus is empty — none of the seal paths materialized")
    # The #179 trap, refused at the seal rather than at `--strict` three steps
    # later. A validation that could not RUN is a strict failure with no
    # finding to read, so the sealed copy is RUN here, and a copy that cannot
    # reach a verdict is refused (see `seal_validator`).
    validator_fields = seal_validator(seal_root, pinned, runner=runner)
    # ONE PRODUCT REVISION. The validator is resolved from this parent's own
    # openXdox leg, and the render unit carries `source_head`'s. They are the
    # same checkout whenever the legs above were sealed, so a disagreement is
    # a parent whose validator came from somewhere else. That parent is
    # refused rather than recorded, because the child's `--strict` would
    # judge the snapshot with a product revision the render did not use.
    validator_leg = next((leg for leg in render_legs
                          if (leg.get("gitlink"), leg.get("leg"))
                          == VALIDATOR_LEG), None)
    validator_revision = validator_fields.get("validator_revision")
    if (validator_revision is not None and validator_leg is not None
            and validator_revision != validator_leg.get("leg_revision")):
        raise SealRefused(
            f"the sealed validator was copied from openXdox code at "
            f"{_short(validator_revision)}, but the sealed render unit carries "
            f"it at {_short(validator_leg.get('leg_revision'))} — the child "
            "would validate the snapshot with a product revision its render "
            "did not use")

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
    # THE CHILD'S RENDER AND ITS `--strict`, RUN HERE FIRST, over exactly the
    # tree the index above covers. A seal whose render unit cannot render, or
    # whose snapshot its own validator rejects, would only fail on the worker.
    # Finding that out here costs one render, and it keeps the verdict in this
    # run's own report.
    precheck = (precheck_render or precheck_sealed_render)(
        seal_root, source_head=source_head,
        source_committed_at=source_committed_at)
    if seal_file_index(seal_root) != index:
        raise SealRefused(
            "the pre-dispatch render changed the sealed tree, so the seal "
            "would no longer be the tree its own render was checked on")
    # THE MANIFEST'S OWN PATH IS STILL EMPTY (Copilot, PR #1166). The index
    # excludes `manifest.json`, the one path it cannot cover, so it cannot see
    # what sealed code left there, and the probe and the render have both run
    # by now. Whatever is there refuses the seal. The write below also creates
    # the file exclusively, so nothing put there later is followed either.
    _refuse_an_occupied_manifest_path(seal_root)
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
        # Where the sealed validator is, which product revision it was copied
        # from, how many schemas travel with it, and what its one run answered.
        # The run is RECORDED on every seal, like `file_count`, rather than
        # reconstructed from a run log.
        **validator_fields,
        # THE RENDER UNIT (#1161). The child runs `render_entry` from the
        # sealed corpus. It reaches the two products' code legs that
        # `render_legs` records, at the commits `source_head` pins them at,
        # and `precheck` is what that same render and `--strict` answered on
        # this parent before anything was dispatched.
        "render_entry": RENDER_ENTRY,
        "render_legs": render_legs,
        "precheck": precheck,
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
    _write_new_manifest(seal_root,
                        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                        identity=seal_identity)
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
    sha256, the tree digest recomputing, the recorded revisions matching the
    parent decision the child was dispatched with, the sealed validator unit
    whole, and the render unit whole. A whole validator unit means its script,
    its schemas, and a recorded run that reached a verdict. A whole render unit
    means the entry, both products' code legs at recorded commits, and a
    recorded pre-dispatch render that passed `--strict`
    (`_render_unit_problems`).

    Returns the problems, empty when the seal verifies. It is a list rather
    than an exception because the child must report ALL of what is wrong before
    it fails — a seal that is missing four files and disagrees about the
    revision is one diagnosis, not four runs.

    NOTE FOR THE CHILD (S3). This function lives INSIDE the corpus the seal
    carries, so calling it from the seal is the artifact vouching for itself.
    The child implements the same check in its own workflow, from its own
    checkout; this is the shape it implements and the unit-tested definition of
    the digest rule.

    `manifest["files"]` IS ATTACKER-CONTROLLED DATA. Every key is routed
    through `_contained_relpath` before it is joined to `seal_dir` — refusing
    an absolute path, a `..` escape, a symlinked component, or a resolved
    location outside the seal root, all BEFORE the join/open — because this
    is the reference for the child-side gate: a tampered manifest whose
    `files` index reads `../../etc/passwd` and whose `tree_digest` was
    recomputed to match must be refused, not followed (Copilot, PR #648)."""
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
        # THE CONTAINMENT CHECK RUNS BEFORE THE JOIN. `files` is manifest data
        # — exactly as trustworthy as whatever produced the manifest — so an
        # absolute path, a `..` escape, or a symlink must be refused here,
        # never followed by `is_file()`/`open()` (Copilot, PR #648).
        try:
            path = _contained_relpath(root, relpath)
        except SealRefused as exc:
            problems.append(str(exc))
            continue
        if not path.is_file():
            problems.append(f"a required path is absent: {relpath}")
            continue
        actual = file_sha256(path)
        recomputed[relpath] = actual
        if actual != files[relpath]:
            problems.append(f"sha256 mismatch: {relpath}")
    # AND NOTHING ELSE IS THERE (Copilot, PR #1166). `files` says what may
    # exist, not only what must. The child renders, validates and bakes out
    # of this tree, so a file the index does not name is bytes the digest
    # never covered, and an extra module under a leg's `src/` would be
    # importable.
    unlisted = sorted(
        path.relative_to(root).as_posix() for path in root.rglob("*")
        if (path.is_symlink() or not path.is_dir())
        and path.relative_to(root).as_posix() != SEAL_MANIFEST_NAME
        and path.relative_to(root).as_posix() not in files)
    problems += [f"the seal holds {relpath}, which its index does not name"
                 for relpath in unlisted[:10]]
    if len(unlisted) > 10:
        problems.append(
            f"... and {len(unlisted) - 10} more the index does not name")
    if len(recomputed) == len(files):
        # Recomputed whenever every indexed path WAS hashed, and deliberately
        # NOT suppressed by an unrelated problem above (a wrong `kind`, a
        # correlation-id disagreement): this function's contract is to report
        # all of what is wrong in one pass, and the whole-tree disagreement is
        # the most useful line in the list. A per-file mismatch will also show
        # up here, which is one cause reported twice — the right side of that
        # trade for a diagnosis a human reads once.
        digest = tree_digest(recomputed)
        if digest != manifest.get("tree_digest"):
            problems.append(
                f"tree_digest mismatch: recomputed {digest}, manifest records "
                f"{manifest.get('tree_digest')}")
    for label, expected, key in (
            ("correlation id", correlation_id, "correlation_id"),
            ("corpus revision", corpus_revision, "corpus_revision"),
            ("recipe revision", recipe_revision, "recipe_revision")):
        if expected and str(manifest.get(key) or "").lower() != str(expected).lower():
            problems.append(
                f"{label} mismatch: manifest records "
                f"{manifest.get(key)!r}, the dispatch carried {expected!r}")
    # The validator is the PRODUCT's, sealed beside the corpus (#1158), so it is
    # looked for where a 2.x seal carries it and nowhere else. A validator
    # inside the corpus is a 1.x layout and satisfies nothing here.
    if manifest.get("validator_relpath") != SEAL_VALIDATOR_RELPATH:
        problems.append(
            f"validator_relpath is {manifest.get('validator_relpath')!r}, "
            f"expected {SEAL_VALIDATOR_RELPATH!r}")
    if SEAL_VALIDATOR_RELPATH not in files:
        problems.append(
            f"the seal does not carry {SEAL_VALIDATOR_RELPATH} — strict "
            "validation could not run")
    # THE UNIT, NOT ONLY ITS SCRIPT (Copilot review of #1162). The script by
    # itself validates nothing. Without its schemas it exits 2 before it reads
    # a snapshot, which is the #179 trap in the unit's shape. So the intake
    # also requires the schemas to be indexed, the recorded count to equal the
    # indexed count, the snapshot schema to be among them, and the parent's
    # one recorded run to have reached a verdict.
    schemas_prefix = f"{SEAL_VALIDATOR_ROOT}/{VALIDATOR_SCHEMAS_PATH}/"
    indexed_schemas = sum(1 for relpath in files
                          if relpath.startswith(schemas_prefix))
    if not indexed_schemas:
        problems.append(
            f"the seal indexes no schema under {schemas_prefix} — strict "
            "validation could not run")
    schema_count = manifest.get("validator_schema_count")
    if isinstance(schema_count, bool) or schema_count != indexed_schemas:
        problems.append(
            f"validator_schema_count is {schema_count!r}, but the seal "
            f"indexes {indexed_schemas} schema(s) under {schemas_prefix}")
    if schemas_prefix + VALIDATOR_SNAPSHOT_SCHEMA not in files:
        problems.append(
            f"the seal does not carry {schemas_prefix}"
            f"{VALIDATOR_SNAPSHOT_SCHEMA}, the schema the child validates "
            "against")
    probe = manifest.get("validator_probe")
    if not (isinstance(probe, dict)
            and probe.get("kind") == VALIDATOR_PROBE["kind"]
            and probe.get("outcome") in VALIDATOR_VERDICT_OUTCOMES):
        problems.append(
            f"validator_probe is {probe!r} — the manifest does not record "
            "that the sealed validator ran to a verdict")
    # Null only for a unit with no product tree; anything else it records must
    # be a full revision, which the seal refuses to write otherwise.
    validator_revision = manifest.get("validator_revision")
    if validator_revision is not None and not (
            isinstance(validator_revision, str)
            and _FULL_REVISION_RE.match(validator_revision)):
        problems.append(
            f"validator_revision is {validator_revision!r}, expected a full "
            "commit revision or null")
    # A malformed revision is reported once, above, and never also compared.
    problems += _render_unit_problems(
        manifest, files,
        validator_revision if isinstance(validator_revision, str)
        and _FULL_REVISION_RE.match(validator_revision) else None)
    if manifest.get("recipe_relpath") not in files:
        problems.append("the seal does not carry the build recipe")
    return problems


def _render_unit_problems(manifest: dict, files: dict,
                          validator_revision) -> list[str]:
    """What is wrong with the seal's RENDER UNIT (#1161), for `verify_seal`.

    The child runs `render_entry` from the sealed corpus, and it can reach
    only what the seal carries. So the entry and its host bootstrap
    (`RENDER_BOOTSTRAP`) must be indexed, and each `RENDER_LEGS` product must
    have its record: the commit the sealed corpus
    pins the product at, the leg commit that product pins, and indexed modules
    under the leg's `src/<package>/`. The file count must match what is
    indexed, and a validator copied from a product tree must be that openXdox
    leg's own revision. The pre-dispatch render must be recorded as validated
    under `--strict`, since the parent seals nothing else."""
    problems: list[str] = []
    entry = manifest.get("render_entry")
    if entry != RENDER_ENTRY:
        problems.append(
            f"render_entry is {entry!r}, expected {RENDER_ENTRY!r} — the "
            "child would have no renderer to run")
    elif f"{SEAL_CORPUS_RELPATH}/{RENDER_ENTRY}" not in files:
        problems.append(
            f"the seal does not carry {SEAL_CORPUS_RELPATH}/{RENDER_ENTRY}, "
            "the renderer the child runs")
    for path in RENDER_BOOTSTRAP:
        if f"{SEAL_CORPUS_RELPATH}/{path}" not in files:
            problems.append(
                f"the seal does not carry {SEAL_CORPUS_RELPATH}/{path}, which "
                "the renderer imports before it reaches either product")
    legs = manifest.get("render_legs")
    if not isinstance(legs, list):
        return problems + [
            f"render_legs is {legs!r} — the seal records no render unit, so "
            "the child's render would reach no product"]
    expected = [(gitlink, leg, package) for gitlink, leg, package in RENDER_LEGS]
    recorded = [(record.get("gitlink"), record.get("leg"), record.get("package"))
                if isinstance(record, dict) else None for record in legs]
    if recorded != expected:
        return problems + [
            f"render_legs records {recorded!r}, expected {expected!r}"]
    for record in legs:
        gitlink, leg, package = record["gitlink"], record["leg"], record["package"]
        name = f"the {gitlink} {leg} leg"
        if record.get("schema_leg") != SCHEMA_LEG:
            problems.append(
                f"{name} records schema_leg {record.get('schema_leg')!r}, "
                f"expected {SCHEMA_LEG!r}")
        for key in ("gitlink_revision", "leg_revision", "schema_leg_revision"):
            value = record.get(key)
            if not (isinstance(value, str) and _FULL_REVISION_RE.match(value)):
                problems.append(
                    f"{name} records {key} {value!r}, expected a full commit "
                    "revision")
        relpath = f"{SEAL_CORPUS_RELPATH}/{gitlink}/{leg}"
        if record.get("relpath") != relpath:
            problems.append(
                f"{name} records relpath {record.get('relpath')!r}, expected "
                f"{relpath!r}")
        if record.get("paths") != list(RENDER_LEG_PATHS):
            problems.append(
                f"{name} records paths {record.get('paths')!r}, expected "
                f"{list(RENDER_LEG_PATHS)!r}")
        indexed = [path for path in files if path.startswith(relpath + "/")]
        # A leg is sealed as its `src/` alone, so nothing else of it may be
        # indexed, whatever `file_count` says (Copilot, opensoft/xFactory PR
        # #526).
        sealed_under = tuple(f"{relpath}/{path}/" for path in RENDER_LEG_PATHS)
        stray = sorted(path for path in indexed
                       if not path.startswith(sealed_under))
        if stray:
            problems.append(
                f"{name} indexes {len(stray)} file(s) outside "
                f"{', '.join(sealed_under)} ({stray[0]}), and a leg is sealed "
                "as its src/ alone")
        modules = f"{relpath}/src/{package}/"
        if not any(path.startswith(modules) and path.endswith(".py")
                   for path in indexed):
            problems.append(
                f"the seal indexes no module under {modules} — the child's "
                "render could not import it")
        count = record.get("file_count")
        if isinstance(count, bool) or count != len(indexed):
            problems.append(
                f"{name} records file_count {count!r}, but the seal indexes "
                f"{len(indexed)} file(s) under {relpath}/")
        if ((gitlink, leg) == VALIDATOR_LEG and validator_revision is not None
                and record.get("leg_revision") != validator_revision):
            problems.append(
                f"validator_revision {validator_revision!r} is not the sealed "
                f"{gitlink} {leg} leg's revision "
                f"{record.get('leg_revision')!r}")
    precheck = manifest.get("precheck")
    if not (isinstance(precheck, dict)
            and precheck.get("entry") == RENDER_ENTRY
            and precheck.get("strict") is True
            and precheck.get("outcome") == PRECHECK_VALIDATED):
        problems.append(
            f"precheck is {precheck!r} — the manifest does not record that "
            "the sealed render passed its own validator under --strict")
    return problems


def seal_result_payload(*, sealed: bool, reason: str | None,
                        manifest: dict | None,
                        artifact_name: str | None = None,
                        strict_failed: bool = False,
                        detail=()) -> dict:
    """What the workflow gates the dispatch on. Deliberately small: sealed or
    not, why not, and the four values the dispatch and the child's own check
    need.

    `strict_failed` is True only for a seal refused because the sealed
    validator REJECTED the snapshot under `--strict` (`StrictGateRejected`).
    `detail` then carries the validator's own findings, bounded, so the step
    that records the outcome can record the verdict rather than a skip."""
    manifest = manifest or {}
    return {
        "kind": "ideation-dashboard-seal-result",
        "sealed": bool(sealed),
        "reason": reason,
        "strict_failed": bool(strict_failed) and not sealed,
        "detail": [str(line) for line in detail][:DETAIL_CAP],
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


def _confined_path(path, base) -> str:
    """`path`'s canonical form, when that names something inside `base`, or
    `ValueError`. The canonical path is what is checked, never the spelling,
    so neither `..` nor a link leads out of `base`."""
    resolved = os.path.realpath(path)
    root = os.path.realpath(base)
    if resolved != root and not resolved.startswith(root + os.sep):
        raise ValueError(f"{path!r} is outside {base}")
    return resolved


def read_strict_verdict(path, *, within) -> tuple[str, list[str]] | None:
    """The strict verdict a seal result records, as `(reason, findings)`, or
    None.

    None unless the file is a seal result that did NOT seal, says
    `strict_failed: true`, and gives a reason. Anything else is recorded as the
    skip the workflow already named, so a malformed or older seal result can
    never turn a skip into a verdict. The file is read only from inside
    `within`, the checkout this lane runs over, where the seal phase writes
    it. A path that resolves anywhere else is never opened."""
    try:
        with open(_confined_path(path, within), encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, TypeError, ValueError):
        return None
    if not isinstance(payload, dict):
        return None
    reason = payload.get("reason")
    if (payload.get("kind") != "ideation-dashboard-seal-result"
            or payload.get("sealed") is not False
            or payload.get("strict_failed") is not True
            or not isinstance(reason, str) or not reason.strip()):
        return None
    detail = payload.get("detail")
    findings = ([str(line) for line in detail][:DETAIL_CAP]
                if isinstance(detail, list) else [])
    return reason.strip(), findings


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
# How many of a strict verdict's findings the report lists. The status
# artifact keeps up to `DETAIL_CAP` of them.
REPORT_FINDINGS_CAP = 20


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
    if status.get("result") == RESULT_STRICT_FAILED and status.get("detail"):
        # A strict verdict's findings belong in the report. A reader who sees
        # "strict_failed" and has to find a run log to learn WHICH document
        # failed has been handed half the verdict.
        findings = [str(line) for line in status["detail"]]
        lines.append("- Findings (the validator's own output, "
                     f"{len(findings)} line(s)):")
        lines += [f"  - `{line.replace('`', "'")}`"
                  for line in findings[:REPORT_FINDINGS_CAP]]
        if len(findings) > REPORT_FINDINGS_CAP:
            lines.append(f"  - … {len(findings) - REPORT_FINDINGS_CAP} more "
                         "in refresh-status.json")
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
    skip_result: str = RESULT_SKIPPED,
    skip_detail=(),
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

    Never raises. `skip_reason` is a verdict handed down by the workflow: an
    unready worker skips before any input is read, and there is deliberately no
    hosted fallback. A refused seal is handed down the same way, and a seal
    refused because its own validator REJECTED the snapshot under `--strict`
    arrives with `skip_result=RESULT_STRICT_FAILED` and the validator's
    findings as `skip_detail`. It is recorded as the verdict it is. Any other
    `skip_result` is recorded as a skip."""
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
        handed = (skip_result if skip_result in (RESULT_SKIPPED,
                                                 RESULT_STRICT_FAILED)
                  else RESULT_SKIPPED)
        return _emit(RefreshOutcome(handed, skip_reason, None,
                                    detail=list(skip_detail)[:DETAIL_CAP]))

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
# phase here builds an image or pushes one. The only source materialization is
# the parent's own `git archive` of a revision it already holds, sealed beside
# a copy of the pinned product validator.
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    """CLI entry. Void by contract, like the snapshot lane's, but only for a
    VALID phase: every path through the lane's own logic for `decide`, `seal`,
    `pin`, `report` or `record-pr` — including a total failure, reported as
    SKIPPED (a refused seal included) — falls through and the process exits 0,
    so the deterministic doc-health results and the delivered report are never
    affected. A phase argparse
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
                         "own decision (--decision-in) at one revision, with "
                         "the two products' code legs it pins, plus the "
                         "pinned recipe, plus the pinned openxdox validator "
                         "composed with its schemas and run once, plus a "
                         "manifest — into --seal-out, after rendering the "
                         "child's snapshot from it once under --strict, and "
                         "write the dispatch gate to --seal-result-out. "
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
    ap.add_argument("--seal-result-in", default=None,
                    help="with --skip-reason: the seal phase's own "
                         "--seal-result-out file. A seal refused because its "
                         "own validator REJECTED the snapshot under --strict "
                         "(strict_failed) is recorded as strict_failed, with "
                         "the validator's findings, instead of as a skip")
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
        strict_failed, strict_detail = False, []
        result_out = Path(args.seal_result_out) if args.seal_result_out else None
        if result_out is not None:
            try:
                _clear_result_path(result_out)
            except OSError as exc:
                print(f"  ::warning::could not clear the seal result: {exc}")
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
            except StrictGateRejected as exc:
                # A verdict on the corpus, and recorded as one: the step that
                # records the outcome reads `strict_failed` and the findings.
                reason = str(exc)
                strict_failed, strict_detail = True, list(exc.detail)
            except SealRefused as exc:
                reason = str(exc)
            except Exception as exc:  # noqa: BLE001 — a seal never fails the run
                reason = f"{type(exc).__name__}: {exc}"
        payload = seal_result_payload(sealed=manifest is not None, reason=reason,
                                      manifest=manifest,
                                      strict_failed=strict_failed,
                                      detail=strict_detail)
        if result_out is not None:
            if os.path.lexists(result_out):
                manifest, reason = None, SEAL_RESULT_PLANTED
                strict_failed, strict_detail = False, []
                payload = seal_result_payload(sealed=False, reason=reason,
                                              manifest=None)
            try:
                _clear_result_path(result_out)
                _create_new_file(result_out, (json.dumps(
                    payload, indent=2, sort_keys=True) + "\n").encode("utf-8"))
            except OSError as exc:
                print(f"  ::warning::could not write the seal result: {exc}")
        if manifest is not None:
            print(f"::notice::{LANE}: SEALED {manifest['artifact_name']} — "
                  f"source_head={_short(manifest['source_head'])}, "
                  f"{manifest['file_count']} files, "
                  f"{manifest['total_bytes']} bytes, "
                  f"tree_digest={manifest['tree_digest'][:12]}")
        elif strict_failed:
            print(f"::warning::{LANE}: STRICT FAILED — {reason}")
            for line in strict_detail:
                print(f"  {line}")
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

    skip_reason, skip_result, skip_detail = args.skip_reason, RESULT_SKIPPED, []
    if skip_reason and args.seal_result_in:
        verdict = read_strict_verdict(args.seal_result_in, within=repo_root)
        if verdict is not None:
            skip_result = RESULT_STRICT_FAILED
            skip_reason, skip_detail = verdict

    outcome = run_refresh_lane(
        repo_root, out_dir=args.out_dir, image=args.image,
        corpus_repo=args.corpus_repo, recipe_repo=args.recipe_repo,
        overlay_path=args.overlay_path, read_inputs=_read, build=build,
        pin_out=args.pin_out, run_url=args.run_url,
        skip_reason=skip_reason, skip_result=skip_result,
        skip_detail=skip_detail)

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
