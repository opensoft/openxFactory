"""Human scaffold-create + select-to-edit launch; agent create-only capture
(plan "authoring.py"; change tasks 3.6/3.7; US8 T030/T031).

Two DISTINCT entrypoints, mirroring `boundary.py`'s "machinery vs. HumanGate"
split so per-actor authority is structural, not a runtime flag:

  HUMAN PATH (`create_scaffold` / `edit_target` / `edit_command`)
      `create_scaffold` renders a header-compliant skeleton (H1 with the
      family's ` — Brainstorm` suffix, `Status:`/`Kind:`/`Summary:`/`Topics:`/
      `Repository context:`/`Captured:` pre-filled, plus a `## Possible feats`
      seed section per the openxFactory `ideation/README.md` "Ideation Header
      Format") into the CHOSEN ideation area and writes it through
      `boundary.OutputBoundary.create_document` — create-only, so scaffolding
      over an existing path refuses as a SOURCE_EDIT (never silently
      overwritten). `edit_target`/`edit_command` back "select-to-edit": they
      resolve the absolute path and the `$EDITOR`/`xdg-open`-style argv a
      caller (the CLI's `edit` subcommand or the guarded local dashboard action)
      MAY launch — this module never executes anything itself. The dashboard's
      whole contribution to an edit is launching the human's own editor;
      content mutation is entirely theirs.
      (spec "Human document authoring" scenario 2: "the dashboard itself
      modifies nothing").

  AGENT PATH (`agent_capture` / `agent_attempt_edit` / `agent_attempt_delete`)
      `agent_capture` enforces the required ideation headers AT THE
      ENTRYPOINT — a header-incomplete submission is refused (recorded on the
      boundary's ledger, same as every other refusal) before it ever reaches
      `boundary.create_document`, so an agent cannot backdoor a malformed
      capture through this path. WHICH headers, and whether a line carries one,
      is the CORPUS's answer since `split-opendox-two-layer-product` § 2.3:
      `missing_required_headers` asks the corpus-adapter seam's `classify`
      rather than applying a list of its own (see that function, and the
      contract comment below). `agent_attempt_edit`/`agent_attempt_delete`
      are named passthroughs to the boundary's explicit refusals — this
      module has NO route that mutates or removes an existing corpus
      document; every "attempt" is wired only to a refusal (spec "Agent
      create-only capture" scenario 2: "the attempt MUST be rejected and
      reported").

Deliberately NOT handled here (spec "Notebook set-removal semantics" is a
DISTINCT requirement): removing a doc/source from a workbench (`xf-wb-*`)
manifest is `workbench.Workbench.remove_member` (T026/T029); removing a
source from a LIFECYCLE PROJECTION notebook (`xf-ideation-<repo>`/
`xf-drafts`/`xf-canon`) is restored on the next `scripts/sync-notebooklm-books.py` run
BY CONSTRUCTION — that script's `sync_book` recomputes each book's desired
membership straight from the corpus's declared `Status:` headers on every
call, so a manual removal never survives a re-sync (test_authoring_agent.py
verifies this against the real `sync_book` function).
"""

from __future__ import annotations

import shlex
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from .boundary import HEADER_INCOMPLETE, AGENT, OutputBoundary
from .workbench import slug

# --------------------------------------------------------------------------
# shared header contract (openxFactory ideation/README.md "Ideation Header
# Format"): H1 (`— Brainstorm` suffix) then the obliged fields, in the order
# the contract declares them.
#
# THE FIELD LIST IS NOT WRITTEN DOWN HERE ANY MORE
# (`split-opendox-two-layer-product` § 2.3; design § D2). It was, until this
# task, and the pair it formed was the defect: this module authored the six
# names and applied them with a scan of its own over
# `doc_health.corpus.STATUS_SCAN_LINES` — one header contract with two authors
# in two packages, agreeing by convention and by nothing else. Convention is
# what `align-status-reader-to-real-lines` already found ten disagreeing
# spellings of, and the damage there was FALSE FINDINGS: a correct document
# reported as lacking a header it plainly carried.
#
# So the question is put to the corpus instead, through the one interface that
# answers it — `classify`, whose response carries both which fields a document's
# kind requires and which of them it is missing (`design.md` § D2: "what KIND is
# this document, and which fields does its kind require — the operation
# `authoring.py`'s `REQUIRED_HEADER_FIELDS` becomes, instead of a constant").
# `REQUIRED_HEADER_FIELDS` survives as a NAME (see `__getattr__` at the foot of
# this module) and no longer as a value: reading it asks the corpus.
# --------------------------------------------------------------------------
BRAINSTORM_SUFFIX = " — Brainstorm"
# The status EVERY created document carries unless a human names another one
# (add-workbench-bullseye-and-create, Brett's 2026-07-25 ruling on open
# question 1): `brainstorm`, in every area, because a created document's tie to
# a staging packet is its PLACEMENT in that packet's folder and not its status
# header. No area-derived status.
DEFAULT_STATUS = "brainstorm"
# A human may still promote at create time; `staged` is the organized-fragment
# stage of `docs/document-lifecycle.md`, reachable only by saying so.
STAGED_STATUS = "staged"
# The statuses this create path may stamp: a NEW ideation document is captured
# thinking, staged material, or an explicit draft — it is never born `ratified`,
# `standard`, `superseded`, `retired`, or `record`, so a request naming one of
# those is refused rather than silently written.
CREATABLE_STATUSES: tuple[str, ...] = (DEFAULT_STATUS, STAGED_STATUS, "draft")
DEFAULT_KIND = "note"
DEFAULT_AREA = "ideation/brainstorm/"
DEFAULT_POSSIBLE_FEAT = "TODO — a candidate feat this thinking could spawn."
# The GOVERNED tree a create may write into. Enforced (see `area_refusal`), not
# merely described: the refusal message has always said "a repo-relative ideation
# directory" while only the TRAVERSAL half was checked (PR #49 wave-2 critic).
IDEATION_PREFIX = "ideation/"


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------
# HUMAN PATH — create action (scenario 1) + select-to-edit (scenario 2)
# --------------------------------------------------------------------------

def render_scaffold(
    *, title: str, summary: str, topics: Sequence[str], repository_context: str,
    kind: str = DEFAULT_KIND, status: str = DEFAULT_STATUS,
    possible_feats: Sequence[str] = (), source: str | None = None,
    now: str | None = None,
) -> str:
    """Render a header-compliant skeleton for a NEW ideation document: the H1
    with the family's ` — Brainstorm` suffix (so `grep '— Brainstorm$'` finds
    it), then `Status:`/`Kind:`/`Summary:`/`Topics:`/`Repository context:`/
    `Captured:` in the README's declared order, then a `## Possible feats`
    seed section every design-exploration brainstorm carries at capture.

    `source` (add-workbench-bullseye-and-create) appends ONE optional
    `Source:` line AFTER the six controlled fields — the provenance citation a
    gated create carries ("WHY this document exists": the workbench scope, or
    the keyword-lens recipe at a named `source_revision`). It is additive: the
    six required fields keep their declared order and their positions, so every
    existing header check still passes and a scaffold with no source is
    byte-identical to what this function rendered before."""
    now = now or _utcnow()
    heading = title if title.endswith(BRAINSTORM_SUFFIX) else f"{title}{BRAINSTORM_SUFFIX}"
    topics_line = ", ".join(t.strip() for t in topics if t and t.strip())
    feats = [f for f in possible_feats if f and f.strip()] or [DEFAULT_POSSIBLE_FEAT]
    feat_lines = "\n".join(f"- {f}" for f in feats)
    source_line = f"Source: {source.strip()}\n" if source and source.strip() else ""
    return (
        f"# {heading}\n\n"
        f"Status: {status}\n"
        f"Kind: {kind}\n"
        f"Summary: {summary}\n"
        f"Topics: {topics_line}\n"
        f"Repository context: {repository_context}\n"
        f"Captured: {now[:10]}\n"
        f"{source_line}"
        "\n"
        "Brainstorm — contradiction and half-formed options are legal here.\n\n"
        "## Possible feats\n\n"
        f"{feat_lines}\n"
    )


def normalized_area(area: str) -> str:
    """`area` with the one trailing slash `scaffold_relpath` assumes."""
    return area if area.endswith("/") else area + "/"


def area_refusal(area: str) -> str | None:
    """Why `area` is not a directory a create may write into, or None when it is.

    ONE definition, called by the ONE body validator both surfaces use
    (`gate_routes.parse_create_document_body`), so the HTTP route and the CLI
    cannot diverge on where a document may land (FR-020).

    THREE conditions, and the third is not a refinement of the second:

      * no leading `/` and no `..` segment — the traversal check, unchanged, with
        its message unchanged because both surfaces' tests pin that sentence.
      * INSIDE `ideation/`. The refusal message asserted this from the beginning
        and nothing enforced it, so `--area openspec/changes/`, `scripts/`,
        `.github/workflows/` and a bare `escape/` were all ACCEPTED on both
        surfaces and committed on the session branch (PR #49 wave-2 critic,
        reproduced). A create is an IDEATION capture — brainstorm or a staging
        packet — and every other tree in this repository is governed by a
        different gate.
      * NOT inside `session_git.GATE_RECORDS_PREFIX`, which is inside `ideation/`
        and therefore survives the check above. That prefix is the ONE path the
        served checkout's immovability fingerprint deliberately filters out (plan
        Constraint 10, `served_checkout_fingerprint(declared_only=…)`), because
        the gate's own records legitimately land there. A DOCUMENT routed into it
        would therefore be invisible to SC-002's oracle: once such a create
        reaches the served checkout through a merged session PR, its bytes can be
        altered or the file removed with the fingerprint reporting NO CHANGE
        (reproduced by the wave-2 critic; the control one directory up under
        `ideation/staging/` reports the tampering correctly). The blind spot must
        stay a blind spot for RECORDS only, so governed content is refused
        entry — which is what makes the finding-18 lane's closing property (the
        records prefix is a blind spot that CANNOT swallow governed content) true
        rather than merely intended. That property was asserted while this
        confinement did not exist, so the finding-18 note in
        `specs/007-workbench-branch-sessions/tasks.md` carries the correction and
        names this function: the two residuals were assessed in separate lanes and
        their COMPOSITION was never checked until the wave-2 critic checked it."""
    from .session_git import GATE_RECORDS_PREFIX

    text = normalized_area(area)
    if text.startswith("/") or ".." in text.split("/"):
        return "area must be a repo-relative ideation directory"
    if not text.startswith(IDEATION_PREFIX):
        return (f"area must be a repo-relative ideation directory — it must sit "
                f"inside {IDEATION_PREFIX!r} (a brainstorm capture or a staging "
                f"packet). Every other tree in this repository is governed by a "
                f"different gate, and a create is not the way into one")
    if text.startswith(GATE_RECORDS_PREFIX):
        return (f"area must not be inside {GATE_RECORDS_PREFIX!r}: that prefix "
                "holds the gate's own action RECORDS and is the one path the "
                "served checkout's immovability fingerprint excludes, so a "
                "document written there could later be altered or removed in the "
                "served tree with the check reporting no change (SC-002). Capture "
                "it under ideation/brainstorm/ or the topic's staging folder")
    return None


def scaffold_relpath(area: str, title: str) -> str:
    """The scaffold's target path: `<area>/<slug(title)>.md` — `slug` mirrors
    `workbench.slug` so a hostile title never traverses the workspace."""
    return f"{normalized_area(area)}{slug(title)}.md"


def create_scaffold(
    boundary: OutputBoundary, *, area: str = DEFAULT_AREA, title: str, summary: str,
    topics: Sequence[str], repository_context: str, kind: str = DEFAULT_KIND,
    status: str | None = None, possible_feats: Sequence[str] = (),
    source: str | None = None, now: str | None = None,
) -> Path:
    """The human create action (spec "Human document authoring" scenario 1):
    scaffold a header-compliant skeleton into the chosen ideation AREA and
    write it through `boundary.create_document` — create-only (an existing
    target refuses as SOURCE_EDIT; `create_document` does not consult the
    boundary's output allowlist at all, which is deliberate: `area` is a
    SOURCE directory like `ideation/brainstorm/`, never a declared output
    path). Opening the file in the human's editor is the caller's job
    (`cli.py create` composes this with `edit_command`); this function's only
    effect is the one write.

    `status` defaults to `DEFAULT_STATUS` (`brainstorm`) in EVERY area — Brett's
    2026-07-25 ruling on `add-workbench-bullseye-and-create` open question 1,
    "these are brainstorm docs". The area is NOT consulted: a created document's
    tie to a staging packet is carried by its PLACEMENT inside that packet's
    folder — which is what the folder-scoped health and readiness derivations
    already read — and never by its status header, so a just-captured thought
    is `brainstorm` wherever it sits. (An earlier realization pass derived
    `staged` from an `ideation/staging/` area; the ruling REVERSED that and the
    `status_for_area` helper it needed is gone.) `source` records the optional
    provenance citation. Both are additive: omitting them reproduces the
    previous behaviour exactly."""
    rel = scaffold_relpath(area, title)
    text = render_scaffold(title=title, summary=summary, topics=topics,
                            repository_context=repository_context, kind=kind,
                            status=status or DEFAULT_STATUS,
                            possible_feats=possible_feats, source=source, now=now)
    return boundary.create_document(rel, text)


def edit_target(repo_root: Path | str, relpath: str) -> Path:
    """Resolve the absolute path a select-to-edit affordance opens. Pure and
    read-only: this NEVER writes anything — the human's own editor performs
    the edit (spec scenario 2: "the dashboard itself modifies nothing")."""
    root = Path(repo_root).resolve()
    resolved = (root / relpath).resolve()
    if resolved != root and not resolved.is_relative_to(root):
        raise ValueError(f"{relpath!r} escapes the repository root {root}")
    return resolved


def edit_command(repo_root: Path | str, relpath: str, *, editor: str | None = None) -> list[str]:
    """The convenience argv a CLI `edit <doc>` launches: `$EDITOR <path>` when
    an editor is given/configured, else an `xdg-open`-style opener. Returns an
    argv list; THIS FUNCTION NEVER EXECUTES IT — invocation (if any) is the
    caller's job."""
    path = edit_target(repo_root, relpath)
    opener = editor or "xdg-open"
    return [*shlex.split(opener), str(path)]


# --------------------------------------------------------------------------
# AGENT PATH — create-only capture (scenario 1) + edit/delete refusal (scenario 2)
# --------------------------------------------------------------------------

#: Where a proposal is staged when the corpus is asked about it. Under
#: `IDEATION_PREFIX` because that is the tree this create path writes into and
#: the tree the header contract governs; the basename is arbitrary and never
#: reaches the answer.
PROPOSAL_KEY = IDEATION_PREFIX + "proposal.md"


def _classify_proposal(text: str):
    """What this corpus makes of a body it does not hold yet.

    A CORPUS OF ONE, AND THE ALTERNATIVE WAS A PRIVATE DOOR. The corpus-adapter
    interface answers about documents a corpus HOLDS — `classify` reads through
    `read`, so an identity the corpus does not list refuses rather than being
    invented. A create gate's whole question is about a body that is not in the
    corpus yet, so the proposal is presented as a corpus of one: staged in a
    throwaway tree under the same prefix the create path writes into, resolved
    through `home_corpus()` like any other location, and classified through the
    same six operations every other caller gets. The shortcut — importing the
    package's classifier and calling it on a string — is exactly the route
    `corpus-adapter-seam` requirement 4 forbids ("no privileged direct call, no
    bypass of the interface for openxFactory's own corpus"), and
    `tests/corpus-adapter/test_no_privileged_route.py` fails the build for it.

    The imports are function-local for the reason `home.py`'s own were: this
    module's dependence on the seam sits at ONE readable point, and no import
    ordering between the two packages can turn into a cycle.

    Bodies are staged as UTF-8 with `errors="replace"`, the same decoding the
    corpus loader uses on the way back, so a body that survives a round trip is
    read exactly as it was written and one that cannot be encoded is read the
    way this corpus would read it rather than raising inside a gate.
    """
    import sys as _sys

    # #872 (RULED OQ-Q): pinned openDox copy, not the local replica.
    _opendox_src = Path(__file__).resolve().parents[2] / "openDox" / "code" / "src"
    if not (_opendox_src / "opendox" / "corpus_adapter.py").is_file():
        raise ImportError(
            "ideation_dashboard.authoring: the pinned openDox corpus-adapter "
            f"interface is not at {_opendox_src / 'opendox' / 'corpus_adapter.py'}. "
            "Run `git submodule update --init --recursive openDox` from the "
            "repository root.")
    if str(_opendox_src) not in _sys.path:
        _sys.path.insert(0, str(_opendox_src))

    from opendox.corpus_adapter import DocumentId
    from corpus_adapter_openxfactory import home_corpus

    with tempfile.TemporaryDirectory(prefix="xf-proposal-") as staged:
        document = Path(staged) / PROPOSAL_KEY
        document.parent.mkdir(parents=True, exist_ok=True)
        document.write_bytes(text.encode("utf-8", errors="replace"))
        adapter, ref = home_corpus(staged)
        resolved = adapter.resolve(ref)
        return adapter.classify(resolved,
                                DocumentId(corpus=ref.name, key=PROPOSAL_KEY))


def required_header_fields() -> tuple[str, ...]:
    """The header fields this corpus obliges of a new ideation document.

    `classify`'s answer, asked of the corpus itself, never restated here — which
    is the whole of `split-opendox-two-layer-product` § 2.3. An empty body is
    the cheapest thing to ask about: the obligation is a property of the kind
    and the tree, not of what the body happens to carry.
    """
    return _classify_proposal("").required_fields


def missing_required_headers(text: str) -> list[str]:
    """Required ideation headers absent — OR value-empty — in `text`'s header
    window.

    THE ANSWER IS THE CORPUS'S, not this module's: it is the `missing_fields`
    of `classify`'s response (§ 2.3). What that buys is stated most simply as a
    subtraction — this function used to be one of the readers
    `doc_health.lines` enumerates as "readers of a lifecycle header that must
    agree", carrying its own window and its own present-rule, and it is not one
    any more. It cannot drift from the corpus's reader because it no longer
    reads.

    The rule it delegates to is unchanged and still requires a non-empty VALUE
    (`STATUS_RE = ^Status:\\s*(.+?)\\s*$`; `parse_kind` returns `None` for a bare
    `Kind:`): a header line with no value is NOT a carried header. Enforcing
    that at the agent gate closes the empty-header bypass — a valueless
    `Status:` would otherwise pass the gate yet make the generator emit
    `stage: null`, failing the pinned snapshot schema (`stage` is required and
    enumerated) — and the window is still the REAL-line one
    (`doc_health.lines.split_keepends`), because that is the window the corpus
    itself scans.
    """
    return list(_classify_proposal(text).missing_fields)


def agent_capture(boundary: OutputBoundary, *, path: str, text: str) -> Path:
    """Add a NEW corpus document on an agent's behalf (spec "Agent create-only
    capture" scenario 1). Required headers are enforced HERE, at the
    entrypoint: a header-incomplete submission is refused — recorded on
    `boundary.refusals` and raised as a `BoundaryViolation`, exactly like every
    other boundary refusal — before it ever reaches `boundary.create_document`.
    A submission at an EXISTING path still refuses there as a SOURCE_EDIT
    (create-only semantics), which is scenario 2's "attempt" case for the
    create route specifically."""
    missing = missing_required_headers(text)
    if missing:
        raise boundary.refuse(
            HEADER_INCOMPLETE, str(path),
            f"missing required header(s): {', '.join(missing)}")
    return boundary.create_document(path, text)


def agent_attempt_edit(boundary: OutputBoundary, path) -> None:
    """An agent's explicit edit attempt on an existing corpus document — always
    refused and reported (spec scenario 2). Named passthrough to
    `boundary.refuse_edit` so the agent capture path exposes a complete,
    self-contained surface (create + the two attempted mutations it can never
    perform) without callers reaching into `boundary.py` directly."""
    boundary.refuse_edit(path)


def agent_attempt_delete(boundary: OutputBoundary, path) -> None:
    """An agent's explicit delete attempt on an existing corpus document —
    always refused and reported (spec scenario 2). See `agent_attempt_edit`."""
    boundary.refuse_delete(path)


def agent_boundary(root: Path | str, allowlist: Sequence[str] = ()) -> OutputBoundary:
    """Convenience constructor: an `OutputBoundary` tagged `actor=AGENT`, the
    only actor label the agent capture path uses."""
    return OutputBoundary(root, allowlist, actor=AGENT)


def __getattr__(name: str):
    """`REQUIRED_HEADER_FIELDS` — the NAME, kept; the constant, gone (§ 2.3).

    PEP 562, and the laziness is the point rather than a flourish. A
    module-level `REQUIRED_HEADER_FIELDS = required_header_fields()` would ask
    the corpus at IMPORT time, which is both a filesystem read during an import
    and an ordering hazard between this module and the adapter package that
    answers it. Resolved on access, the name is a thin alias for the corpus's
    own answer: `tests/ideation-dashboard/test_authoring_classify_derivation.py`
    proves it by making `classify` answer differently and watching the alias
    follow, and by parsing this file for an assignment that no longer exists.

    It is kept rather than deleted because `completeness.GOVERNANCE_HEADER_FIELDS`
    deliberately RESTATES the block to keep its own import graph free of
    anything that touches the filesystem, and `test_completeness.py`
    cross-checks the two so they cannot drift. Keeping the name turns that
    existing cross-check into a check against the CORPUS's answer; deleting it
    would either delete the cross-check or force into `completeness.py` the
    import it was written not to have.
    """
    if name == "REQUIRED_HEADER_FIELDS":
        return required_header_fields()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
