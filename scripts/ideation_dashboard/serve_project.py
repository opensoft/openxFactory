"""The openDox column of the dashboard serve: the project and hosted-actor
routes (`split-opendox-two-layer-product` § 2.4, PR 2 of 4).

The project-register projection, the "Open in NotebookLM" tile action and the
human select-to-edit escape hatch — design § D3's "projects" and "hosted actor
and account" clusters — lifted out of `serve.py` UNCHANGED, byte for byte, as a
mixin `DashboardHandler` composes, on the same reasoning
`serve_workbench.py`'s docstring gives.

THEY ARE STILL FIXED CORE ROUTES: `_route()` and `do_POST()` dispatch to
`_serve_project_register`, `_handle_notebook_action` and `_handle_edit_action`
by the same names in the same order as before the move.

WHAT DELIBERATELY DID NOT COME WITH THEM. Two neighbours the § 2.4 memo listed
under this column stay in `serve.py`:

  * `_session_repository()` — the memo's own § 1 names it among the CENTRAL
    GATING PRIMITIVES, and the `/capabilities` arm and the gate-verb handler
    both call it. A gating primitive belongs to the core that every column
    reaches, not to one column;
  * the `/capabilities` arm itself — it is answered inline in `_route`, and the
    dispatch table pinned by `test_extension_point_parity.py` records exactly
    which primitives that arm reaches. Moving it would have changed the pinned
    table, which is a behaviour change by the only definition this PR has.

`_make_adapter()` stays too: `_session_notebook` (the openXdox column) calls it
as well, so it is shared rather than this column's.

INVOCATION (design D12): `serve.py` runs BOTH as a script and as a module, so
this module uses ABSOLUTE `ideation_dashboard.*` imports, never `from . import`.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from ideation_dashboard import action_errors
from ideation_dashboard.serve_wire import (
    AGENT_INVOCATION_REFUSAL,
    JSON_CTYPE,
    JSON_OBJECT_BODY_REQUIRED,
)


def _launch_editor(command: list[str], *, configured_editor: bool,
                   popen=subprocess.Popen):
    """Launch an edit command with the streams its invocation style requires.

    A configured ``$EDITOR`` may be a terminal program, so it must inherit the
    server's terminal and remain in its session.  The desktop-opener fallback
    has no interactive contract and is detached from the dashboard process.
    ``popen`` is injectable so tests never start either kind of program.
    """
    if configured_editor:
        return popen(command)
    return popen(
        command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL, start_new_session=True)


def _listed_source_paths(entry) -> frozenset[str]:
    """Source paths the selected snapshot actually projects into the UI.

    The viewer can be reached from the corpus-wide document list, a staged-topic
    folder, or an active/archived change folder.  Root confinement alone is not
    enough for select-to-edit: without this projection check, a console-token
    holder could ask the route to open any existing file under the registered
    checkout, including one the dashboard never listed.
    """
    snapshot = entry.read_json() if entry is not None else None
    if not isinstance(snapshot, dict):
        return frozenset()

    paths: set[str] = set()
    for document in snapshot.get("documents") or []:
        if isinstance(document, dict) and isinstance(document.get("path"), str):
            paths.add(document["path"])
    for collection in ("staged_topics", "changes"):
        for item in snapshot.get(collection) or []:
            if not isinstance(item, dict):
                continue
            paths.update(path for path in (item.get("files") or [])
                         if isinstance(path, str))
    return frozenset(paths)


def _edit_request_fields(body) -> tuple[tuple[str, str, str] | None, str | None]:
    """Validate the select-to-edit wire body without touching the filesystem."""
    if not isinstance(body, dict):
        return None, JSON_OBJECT_BODY_REQUIRED
    path = body.get("path")
    repository = body.get("repository")
    ref = body.get("ref")
    if not all(isinstance(field, str) and field
               for field in (path, repository, ref)):
        return None, "path, repository, and ref must be non-empty strings"
    return (path, repository, ref), None


def _resolved_listed_edit_entry(source, path: str, repository: str | None,
                                ref: str | None):
    """Return the selected entry only when its projected file is editable."""
    registry = getattr(source, "registry", None) if source is not None else None
    if registry is None:
        return None
    entry = registry.resolve(repository, ref)
    target = registry.resolve_source(repository, ref, path)
    if (entry is None or entry.source_root is None or target is None
            or not target.is_file() or path not in _listed_source_paths(entry)):
        return None
    return entry


class ProjectRoutes:
    """The project/notebook/edit half of `DashboardHandler`.

    A mixin for the same reason `WorkbenchRoutes` is one: every method is a
    request handler on the live handler instance, answering through the core's
    own send/refuse primitives. Never instantiated on its own.
    """

    # ---- select-to-edit route (US8 T030; the dashboard itself writes nothing) ----
    def _handle_edit_action(self) -> None:
        """Launch the selected source file in the human's local editor.

        The route deliberately shares the human-console boundary with session
        verbs: loopback + real checkout + resolved actor + per-serve token. The
        target is resolved through the selected registry entry, so neither a
        traversal nor a repository/ref mismatch can fall back to another root.
        """
        if not self.loopback:
            self._send_json(403, {"ok": False, "error": "loopback_only",
                                  "message": "select-to-edit is loopback-only"})
            return
        if not self.capabilities.get("actions", {}).get("edit") or not self.actor:
            self._send_json(403, {"ok": False, "error": "action_unavailable",
                                  "message": "select-to-edit is unavailable "
                                             "(no resolved actor/checkout)"})
            return
        console_refusal = self._not_the_human_console()
        if console_refusal is not None:
            sys.stderr.write(
                f"[actions/edit] agent_invocation refused: {console_refusal}\n")
            self._send_json(403, {"ok": False, "error": "agent_invocation",
                                  "message": AGENT_INVOCATION_REFUSAL})
            return
        fields, body_error = _edit_request_fields(self._read_json_body())
        if fields is None:
            self._send_json(400, {"ok": False, "error": "invalid_body",
                                  "message": body_error or JSON_OBJECT_BODY_REQUIRED})
            return
        path, repository, ref = fields

        entry = _resolved_listed_edit_entry(self.source, path, repository, ref)
        if entry is None:
            self._send_json(404, {"ok": False, "error": "document_unavailable",
                                  "message": "the selected document is unavailable"})
            return

        editor = os.environ.get("EDITOR")
        # Tests install a recorder on this server instance. Production preserves
        # the console for a configured terminal editor; only the desktop-opener
        # fallback is detached with its streams closed.
        launcher = getattr(self.server, "editor_launcher", None) or (
            lambda command: _launch_editor(
                command, configured_editor=bool(editor)))
        try:
            from ideation_dashboard import authoring
            argv = authoring.edit_command(entry.source_root, path, editor=editor)
            launcher(argv)
        # The wire response is fixed; full detail stays in the local server log.
        except Exception as exc:  # noqa: BLE001
            sys.stderr.write(
                f"[actions/edit] editor launch failed: {type(exc).__name__}: {exc}\n")
            self._send_json(500, {"ok": False, "error": "editor_launch_failed",
                                  "message": "the editor could not be opened; "
                                             "see the server log"})
            return
        self._send_json(200, {"ok": True, "path": path})

    def _handle_notebook_action(self) -> None:
        if not self.loopback:
            self._send_error_code(action_errors.ERR_LOOPBACK_ONLY)
            return
        if not self.capabilities.get("actions", {}).get("notebook"):
            self._send_error_code(action_errors.ERR_ACTION_UNAVAILABLE)
            return
        body = self._read_json_body()
        if not isinstance(body, dict):
            self._send_error_code(action_errors.ERR_INVALID_BODY)
            return
        from ideation_dashboard import notebook_action
        self._run_notebook_action(notebook_action, body.get("tile_kind"), body.get("tile_id"))

    def _run_notebook_action(self, notebook_action, tile_kind, tile_id) -> None:
        try:
            snapshot = json.loads(Path(self.snapshot_path).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            self._send_error_code(notebook_action.ERR_SNAPSHOT_UNAVAILABLE)
            return
        adapter = self._make_adapter()
        if adapter is None:
            # unreachable while the capability agrees with the declaration
            # (`_probe_nlm`), and fail-closed if it ever does not
            self._send_error_code(notebook_action.ERR_ACTION_UNAVAILABLE)
            return
        try:
            result = notebook_action.run_notebook_action(
                tile_kind=tile_kind, tile_id=tile_id, snapshot=snapshot,
                checkout_root=Path(self.checkout_root), adapter=adapter)
        except notebook_action.NotebookActionError as exc:
            self._log_action_failure(exc.code, exc.log_detail)
            self._send_json(exc.status, exc.body())
            return
        except Exception:  # noqa: BLE001
            # never leak a traceback over the wire
            self._send_error_code(notebook_action.ERR_ACTION_FAILED)
            return
        self._send_json(200, result)

    def _log_action_failure(self, code: str, detail: str | None) -> None:
        """Server-side-only diagnostics for a refused/failed action — the wire
        carries only the fixed catalog message; the operator sees the detail."""
        if detail:
            sys.stderr.write(f"[actions/notebook] {code}: {detail}\n")

    def _serve_project_register(self, head_only: bool) -> None:
        """`/project-register.json` — the register PROJECTION the project
        picker reads (add-project-scoped-selection). Read per request (the
        register is human-editable between requests), reduced to the
        navigation fields only, and 404 when no register is reachable — the
        picker hides and the selector renders today's ungrouped roster.

        TWO PLANES in one document (design D-e): `projects` is TRUTH (the
        register), `pending` is INTENT — dispatched, undelivered
        create-project commissions read from the same records scan the
        duplicate guard uses, so a fresh commission is visible as pending
        instead of looking like it did nothing. A pending id the register
        already carries is dropped: the register wins the moment the
        fulfilment lands, even before the descriptor's status flips."""
        import yaml
        from ideation_dashboard.gate_console import DEFAULT_RECORDS_DIR
        from ideation_dashboard.kickoff import (
            dispatched_commission_rows, dispatched_commissions,
            discover_project_register)
        source = discover_project_register(Path(self.checkout_root))
        register = None
        if source is not None:
            try:
                register = yaml.safe_load(source.read_text(encoding="utf-8"))
            except (OSError, yaml.YAMLError):
                register = None
        if not isinstance(register, dict):
            self.send_error(404, "no project register")
            return
        projects = [
            {"id": p.get("id"), "name": p.get("name") or p.get("id"),
             "repositories": [str(r) for r in (p.get("repositories") or [])]}
            for p in (register.get("projects") or [])
            if isinstance(p, dict) and p.get("id")
        ]
        real_ids = {p["id"] for p in projects}
        records_root = Path(self.checkout_root) / DEFAULT_RECORDS_DIR

        def _job(descriptor):
            try:
                doc = yaml.safe_load(descriptor.read_text(encoding="utf-8"))
            except (OSError, yaml.YAMLError):
                doc = None
            return doc if isinstance(doc, dict) else {}

        pending = []
        for pid, descriptor in sorted(
                dispatched_commissions(records_root, "create-project").items()):
            if pid in real_ids:
                continue
            job = _job(descriptor)
            pending.append({
                "id": pid,
                "name": job.get("project_name") or pid,
                "repositories": [str(r) for r in (job.get("repositories") or [])],
                "dispatched_at": job.get("dispatched_at"),
            })
        # add-opendox-project-header (D15): dispatched, undelivered MEMBERSHIP
        # edits — the popover badges the affected rows until the fulfilment
        # lands. Same two-plane posture as `pending` above. EVERY queued edit
        # rides (edits queue, topic D18), oldest first — including edits on a
        # project that so far exists only as a pending creation, so the apply
        # affordance's count stays honest; an edit whose project is in
        # neither plane is dropped (nothing to badge).
        pending_ids = {p["id"] for p in pending}
        pending_edits = []
        for pid, _descriptor, job in dispatched_commission_rows(
                records_root, "edit-project"):
            if pid not in real_ids and pid not in pending_ids:
                continue
            pending_edits.append({
                "project_id": pid,
                "add": [str(r) for r in (job.get("add") or [])],
                "remove": [str(r) for r in (job.get("remove") or [])],
                "dispatched_at": job.get("dispatched_at"),
            })
        document = {
            "kind": "project-register-projection",
            "projects": projects,
            "pending": pending,
            "pending_edits": pending_edits,
        }
        self._serve_bytes(json.dumps(document).encode("utf-8"), JSON_CTYPE,
                          head_only)
