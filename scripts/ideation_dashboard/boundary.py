"""The interactivity boundary — the single guarded write chokepoint every
machinery and agent write passes through (spec "Interactivity boundary"; plan
"Boundary as one guard").

Three guarantees, enforced by CONSTRUCTION rather than by a runtime role flag:

  1. Declared output-path allowlist. Machinery output writes (snapshot, records,
     manifests, draft-organize skeletons) land only under caller-declared output
     prefixes — never over a corpus source document (FR-018 / SC-003).
  2. Create-only over the corpus. Machinery and agents may add a NEW corpus
     document but never edit or delete an existing one; an edit/delete attempt is
     refused (spec "Agent create-only capture" / FR-015).
  3. Human-only gates. Lifecycle-gate side effects flow ONLY through `HumanGate`,
     a distinct entrypoint machinery code holds no reference to — so a gate side
     effect from a non-human caller is impossible by construction, not gated by an
     `is_human` boolean (D16).

Every refusal is REPORTED, never silent: it is appended to the boundary's
`refusals` ledger AND raised as a `BoundaryViolation` carrying the structured
`Refusal` (spec scenario: an out-of-bounds attempt is rejected AND reported).

The generator/CLI stay path-agnostic: an instance is constructed with the repo
root and an explicit output allowlist; no snapshot/record path is baked in here.
"""

from __future__ import annotations

import contextlib
import os
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

# Actor labels for refusal reports. NOT authority levels — a human gate is a
# different class entirely (see HumanGate), so this string never grants gate power.
MACHINERY = "machinery"
AGENT = "agent"
HUMAN = "human"  # the scaffold-create/select-to-edit path (authoring.py) —
                  # still no gate power; lifecycle gates remain HumanGate-only.

# Refusal kinds — stable strings for reports, tests, and the eventual UI surface.
OUTSIDE_ROOT = "outside-root"
OUTSIDE_ALLOWLIST = "outside-allowlist"
SOURCE_EDIT = "source-edit"
SOURCE_DELETE = "source-delete"
# add-workbench-branch-sessions (T026, FR-015/FR-016): the refusal kind for a
# session rewrite attempted where the narrow allowance does not hold — no session
# worktree was declared, or the target sits outside the one that was.
SESSION_REWRITE = "session-rewrite"
GATE_SIDE_EFFECT = "gate-side-effect"
# The gate console's DOCUMENT target escaping its permitted root (gate_console
# `edit_apply`, the un-confined-document-path trust gap). Its own kind rather
# than OUTSIDE_ROOT because the target here is a corpus SOURCE document a human
# gate action rewrites in place, not an output artifact — an audit consumer
# reading the ledger must be able to tell a traversal attempt against the corpus
# apart from an output write that missed its allowlist.
DOCUMENT_ESCAPE = "document-escape"
HEADER_INCOMPLETE = "header-incomplete"  # authoring.py's agent header-completeness gate

# Structural output-path fragments the contracts fix; the rest of an instance's
# allowlist (the run-local snapshot path, record dirs) is caller-supplied.
WORKBENCH_DIR = "ideation/workbench/"   # gitignored manifests (FR-012)
STAGING_DIR = "ideation/staging/"       # entering staging is a human gate action


def _norm_prefix(prefix: str) -> str:
    p = prefix.replace("\\", "/").lstrip("/")
    return p if p.endswith("/") else p + "/"


@dataclass(frozen=True)
class Refusal:
    """A reported boundary refusal — the durable 'why' behind a rejected write."""
    kind: str
    actor: str
    target: str
    reason: str

    def report(self) -> str:
        return (f"boundary refused {self.kind}: actor={self.actor!r} "
                f"target={self.target!r} — {self.reason}")


class BoundaryViolation(Exception):
    """A refused machinery/agent write. Carries the structured `Refusal` so the
    refusal is reported (message + ledger), never silent."""

    def __init__(self, refusal: Refusal) -> None:
        self.refusal = refusal
        super().__init__(refusal.report())


class OutputBoundary:
    """Machinery/agent write chokepoint. Constructed with the repository root and
    the declared output-path allowlist; has NO gate capability by design (the
    class carries no method that performs a lifecycle-gate side effect)."""

    def __init__(self, root: Path, allowlist: Sequence[str] = (), *,
                 actor: str = MACHINERY, session_root: Path | None = None) -> None:
        self.root = Path(root).resolve()
        self.allowlist: tuple[str, ...] = tuple(_norm_prefix(a) for a in allowlist)
        self.actor = actor
        self.refusals: list[Refusal] = []
        # The DECLARED session worktree, or None. See `rewrite_session_document`:
        # the rewrite allowance exists only when a caller has named the worktree
        # it is confined to, so the allowance is an explicit construction-time
        # DECISION rather than a flag that relaxes `create_document`.
        self.session_root = Path(session_root).resolve() if session_root else None

    # ---- reporting ----
    def _refuse(self, kind: str, target: str, reason: str) -> BoundaryViolation:
        refusal = Refusal(kind, self.actor, target, reason)
        self.refusals.append(refusal)
        return BoundaryViolation(refusal)

    def refuse(self, kind: str, target: str, reason: str) -> BoundaryViolation:
        """PUBLIC refusal hook for callers layering their own refusal kinds on
        top of the boundary's ledger (e.g. `authoring.py`'s `HEADER_INCOMPLETE`
        agent header-completeness gate) — every refusal, from any layer, is
        recorded AND raised the same way (`raise boundary.refuse(...)`), so
        "every refusal is reported, never silent" holds across the whole
        action layer, not just this module's own checks."""
        return self._refuse(kind, target, reason)

    # ---- containment ----
    def _within_root(self, path) -> Path:
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = self.root / candidate
        resolved = candidate.resolve()
        if resolved != self.root and not resolved.is_relative_to(self.root):
            raise self._refuse(
                OUTSIDE_ROOT, str(path),
                f"target escapes the repository root {self.root}")
        return resolved

    def _rel(self, resolved: Path) -> str:
        return resolved.relative_to(self.root).as_posix()

    def _allowed(self, rel: str) -> bool:
        return any(rel == a.rstrip("/") or rel.startswith(a) for a in self.allowlist)

    # ---- machinery output write (snapshot, records, manifests, skeletons) ----
    def permit_output(self, path) -> Path:
        """Resolve a machinery output target, refusing anything outside the root
        or outside the declared allowlist. Returns the absolute path."""
        resolved = self._within_root(path)
        rel = self._rel(resolved)
        if not self._allowed(rel):
            raise self._refuse(
                OUTSIDE_ALLOWLIST, rel,
                f"not under the declared output allowlist {list(self.allowlist)}")
        return resolved

    def write_output(self, path, data: str | bytes) -> Path:
        """The machinery write path: permit_output, then write. All snapshot,
        record, and manifest writes go through here."""
        resolved = self.permit_output(path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, bytes):
            resolved.write_bytes(data)
        else:
            resolved.write_text(data, encoding="utf-8")
        return resolved

    def create_output(self, path, data: str | bytes) -> Path:
        """Create an allowed output exclusively.

        Gate transactions use this when an existing artifact means another
        attempt already owns the action identity.  ``write_output`` deliberately
        retains its historical replace-capable behaviour for projections and
        other callers.
        """
        resolved = self.permit_output(path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, bytes):
            with resolved.open("xb") as stream:
                stream.write(data)
        else:
            with resolved.open("x", encoding="utf-8", newline="") as stream:
                stream.write(data)
        return resolved

    def replace_output(self, path, data: str | bytes) -> Path:
        """Atomically replace an existing allowed output on the same filesystem."""
        resolved = self.permit_output(path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        if not resolved.is_file():
            raise FileNotFoundError(resolved)
        original_mode = stat.S_IMODE(resolved.stat().st_mode)
        temporary: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                    mode="wb", dir=resolved.parent, prefix=f".{resolved.name}.",
                    suffix=".tmp", delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(data if isinstance(data, bytes)
                             else data.encode("utf-8"))
                stream.flush()
                os.fsync(stream.fileno())
            os.chmod(temporary, original_mode)
            os.replace(temporary, resolved)
            temporary = None
        finally:
            if temporary is not None:
                with contextlib.suppress(OSError):
                    temporary.unlink()
        return resolved

    def permit_draft_skeleton(self, path) -> Path:
        """A draft-organize skeleton MUST be written OUTSIDE ideation/staging/ —
        moving material INTO staging is a human gate action (FR-012). Still
        subject to the allowlist."""
        resolved = self.permit_output(path)
        rel = self._rel(resolved)
        if rel == STAGING_DIR.rstrip("/") or rel.startswith(STAGING_DIR):
            raise self._refuse(
                OUTSIDE_ALLOWLIST, rel,
                "draft-organize skeletons are written outside ideation/staging/ "
                "(entering staging is a human gate action)")
        return resolved

    # ---- create-only corpus capture (human scaffold + agent capture) ----
    def create_document(self, path, text: str) -> Path:
        """Add a NEW corpus document. Create-only: an existing target is refused
        as a source edit — machinery and agents never rewrite a corpus document
        (spec 'Agent create-only capture')."""
        resolved = self._within_root(path)
        rel = self._rel(resolved)
        if resolved.exists():
            raise self._refuse(
                SOURCE_EDIT, rel,
                "corpus documents are create-only; an existing document is never "
                "rewritten by machinery or an agent")
        resolved.parent.mkdir(parents=True, exist_ok=True)
        # newline="" pins the bytes exactly as composed (T104 F10 / FR-045):
        # without it, write_text translates \n to os.linesep, so the same
        # buffer would land different bytes on different platforms and the
        # base identity the client hashed would drift from the file.
        # NOTE (wave re-review P3): on Linux CI this argument is unobservable
        # (os.linesep == "\n"), so its regression pin is TEXTUAL —
        # test_boundary.py greps this module for the exact spelling at both
        # governed write sites. Keep the spelling literal.
        resolved.write_text(text, encoding="utf-8", newline="")
        return resolved

    # ---- the ONE rewrite allowance: an existing target inside a session worktree ----
    def rewrite_session_document(self, path, text: str | None) -> Path:
        """Rewrite an EXISTING document inside a DECLARED session worktree
        (add-workbench-branch-sessions T026, FR-015).

        This is a deliberate, narrow allowance and it is stated as a DECISION
        rather than a relaxed flag, because `create_document` above is
        create-only on purpose: machinery and agents never rewrite a corpus
        document, and nothing here changes that. What changed is the ground the
        write happens on. A session worktree is an UNMERGED branch — a private
        working copy whose every change is one gate action, one commit, and one
        pull request away from a human reviewer (FR-006, D18). Rewriting a draft
        there is not editing the corpus; the corpus is what `main` holds, and the
        only route from this branch to `main` is a reviewed merge. So the
        allowance costs the corpus nothing, and the reviewability the create-only
        rule protects is provided by the branch instead.

        Three conditions, all structural, all refused rather than degraded:

          1. A session worktree MUST have been DECLARED at construction
             (`session_root=`). No declaration, no allowance — an ordinary
             boundary keeps refusing an existing target, so no existing caller
             gains rewrite power by accident. This is why the allowance is not a
             method parameter: a caller cannot opt into it per call.
          2. The target MUST resolve INSIDE that worktree. Confinement is a
             refusal, never a fallback to `main` — the whole point is that a
             session write cannot reach the served checkout (FR-004, FR-016).
          3. The target MUST ALREADY EXIST. This verb REWRITES; bringing a
             document into existence stays `create_document`'s create-only job,
             so the two paths cannot be confused for one another (FR-016).

        A delete-shaped call (absent or blank replacement text) is refused as a
        SOURCE_DELETE: no session verb grants delete authority, and an empty file
        is how a delete would be spelled if one tried (FR-016).
        """
        resolved = self._within_root(path)
        rel = self._rel(resolved)
        if self.session_root is None:
            raise self._refuse(
                SESSION_REWRITE, rel,
                "rewriting an existing document requires a DECLARED session "
                "worktree; this boundary has none, and outside a session an "
                "existing document is never rewritten (create-only)")
        if resolved != self.session_root and not resolved.is_relative_to(self.session_root):
            raise self._refuse(
                SESSION_REWRITE, rel,
                f"target resolves outside the declared session worktree "
                f"{self.session_root}; confinement is a refusal, never a "
                "fallback to the served checkout")
        if text is None or not str(text).strip():
            raise self._refuse(
                SOURCE_DELETE, rel,
                "a blank or absent replacement is a delete in disguise; no "
                "session verb grants delete authority")
        if not resolved.is_file():
            raise self._refuse(
                SOURCE_EDIT, rel,
                "this path REWRITES an existing document; bringing a new "
                "document into existence stays the create-only create path")
        # newline="" for the same reason as create_document: the rewritten
        # bytes must be exactly the replacement the buffer's identity
        # describes, on every platform (T104 F10 / FR-045). Same textual pin
        # as create_document's site (test_boundary.py) — keep the spelling
        # literal.
        resolved.write_text(text, encoding="utf-8", newline="")
        return resolved

    # ---- explicit edit/delete refusals (agent asked to mutate an existing doc) ----
    def refuse_edit(self, path) -> None:
        """Refuse (and report) an attempt to edit an existing corpus document."""
        rel = self._rel(self._within_root(path))
        raise self._refuse(
            SOURCE_EDIT, rel,
            "editing an existing corpus document is refused for machinery/agents")

    def refuse_delete(self, path) -> None:
        """Refuse (and report) an attempt to delete an existing corpus document."""
        rel = self._rel(self._within_root(path))
        raise self._refuse(
            SOURCE_DELETE, rel,
            "deleting an existing corpus document is refused for machinery/agents")


class HumanGate:
    """The DISTINCT human-only entrypoint for lifecycle-gate side effects (stage
    transitions and their governed records). It is a separate class with separate
    construction — machinery holds no reference to it — so a gate side effect from
    a non-human caller is impossible BY CONSTRUCTION, not by a role flag (D16).

    Wave 1 establishes the entrypoint and its human-actor requirement; the gate
    console (T033/T034) and kickoff (T035) build their governed writes on it. Gate
    artifacts are still written through an OutputBoundary tagged to the human, so
    the same allowlist discipline applies to gate/kickoff records."""

    def __init__(self, root: Path, allowlist: Sequence[str] = (), *,
                 human_actor: str, session_root: Path | None = None) -> None:
        if not human_actor or not str(human_actor).strip():
            raise ValueError("HumanGate requires an identified human actor "
                             "(a gate action with no human is structurally invalid)")
        self.human_actor = human_actor
        self.output = OutputBoundary(root, allowlist, actor=f"human:{human_actor}",
                                     session_root=session_root)

    @property
    def session_root(self):
        """The DECLARED session worktree, or None (add-workbench-branch-sessions
        T026). Read-only on purpose: the rewrite allowance is decided when the
        gate is constructed, so no caller can grant itself one mid-action."""
        return self.output.session_root

    def write_gate_artifact(self, path, data: str | bytes) -> Path:
        """Write a governed gate/kickoff artifact (demotion/ratification/gate-action/
        workflow-job record) under the declared allowlist, attributed to the human."""
        return self.output.write_output(path, data)

    def create_gate_artifact(self, path, data: str | bytes) -> Path:
        """Create a governed artifact without replacing a competing attempt."""
        return self.output.create_output(path, data)

    def replace_gate_artifact(self, path, data: str | bytes) -> Path:
        """Atomically finalize a governed artifact created by this transaction."""
        return self.output.replace_output(path, data)

    def rewrite_session_document(self, path, text: str | None) -> Path:
        """The session rewrite (FR-015), through the human gate. Delegates to the
        boundary's narrow allowance — see `OutputBoundary.rewrite_session_document`
        for the three structural conditions and why this is not `create_document`
        with a flag flipped."""
        return self.output.rewrite_session_document(path, text)
