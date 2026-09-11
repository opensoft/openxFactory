"""openxFactory's OWN adapter column of the dashboard serve: the lane routes
(`split-opendox-two-layer-product` § 2.4, PR 3 of 4; RULING DQ-1, OQ-3).

Neither openDox nor openXdox. These routes answer questions only THIS
repository's governance has — the DTN candidate register, the staging queue, the
project-register edit lane, the snapshot refresh bindings and the committed-intent
feed — so under DQ-1 they stay behind with the openxFactory adapter rather than
travelling with either half of the carve. They are lifted out of `serve.py`
UNCHANGED, byte for byte, as a mixin `DashboardHandler` composes.

THEY REACH THE SEAM THE SAME WAY openXdox DOES, deliberately. Nothing stops the
repository that OWNS the extension point from contributing through it, and doing
so is what proves the seam is a seam rather than a courtesy extended to one
column: after PR 3 the `/actions/refresh`, `/actions/dtn-seed`,
`/actions/staging-seed`, `/actions/apply-register-edits` and
`/committed-intents.json` arms are gone from `do_POST`/`_route` and arrive as
`RouteBinding`s instead, dispatched by name against the LIVE handler so every one
of them still meets `self.loopback` and `self.capabilities` first.

THE TWO `doc_health` IMPORTS THAT TRAVEL. `from doc_health import shared_identity`
and `from doc_health import staging_seed` move FILE, never TARGET: they stay
function-local, they still reach `doc_health` directly, and nothing is re-plumbed
through `corpus_adapter_openxfactory` here (§ 2.4's hard constraint). `serve.py`
keeps its third direct `doc_health` import, `_head_of`'s `RealGit`, which
`build_server` calls and which is therefore core rather than a lane handler.

THE INTENT FEED IS A PURE MOVE. `_serve_committed_intents` lands exactly as PR
#718 left it — no behaviour edit, not one character — and belongs here under
RULING Q1: the apply lane is a permanent fixture of the openxFactory mapping
specifically.

INVOCATION (design D12): `serve.py` runs BOTH as a script and as a module, so
this module uses ABSOLUTE `ideation_dashboard.*` imports, never `from . import`,
and self-inserts `scripts/` on the import path for the bare `route_extension`
import the same way `serve.py` and `snapshot_registry.py` do.
"""

from __future__ import annotations

import json
import sys
import urllib.parse
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:  # plain-script parity with serve.py (D12)
    sys.path.insert(0, str(_SCRIPTS_DIR))

# § 5.2 SHED REACH (RULED (a) / RULED Q7, `#656`): the modules this file reads
# from `opendox.*` / `openxdox.*` below left openxFactory at the carve and are
# read from the two PINNED legs through the ONE resolver. See
# `scripts/carved_reach.py`.
from carved_reach import install as _install_carved_reach  # noqa: E402

_install_carved_reach()

import route_extension  # noqa: E402

# The three fixed wire strings, at their own neutral home rather than through
# the wire module (openDox under design D3): same reason as the predicate
# below, and a `str` literal carries no dependency, so the treatment OQ-B
# B-1 gave `slug` — a neutral module beside `output_boundary` — was
# available to them, which is where the ruling sent them. OQ-B B-2.
from wire_messages import (  # noqa: E402
    HOSTED_SESSION_REFUSAL,
    JSON_CTYPE,
    JSON_OBJECT_BODY_REQUIRED,
)

from openxdox import snapshot_registry as registry_mod  # noqa: E402
# The hosted-plane ref confinement, at its own home rather than through the
# wire module (openDox under design D3): this column is openxFactory's own
# engineering adapter and STAYS, so the import it used to make is the edge
# RULING OQ-2 forbids. `serve_projection` is openXdox, which is the allowed
# direction and the one OQ-B B-3 already took for the sessions reach.
# OQ-B re-plumb B-2, ruled on `#656` 2026-09-09 ("rule B-2 (i')").
from openxdox.serve_projection import hosted_ref_refused  # noqa: E402

# add-ideation-intent-plane task 4.4 (Brett Heap's ruling D-1, openxFactory
# #656): the COMMITTED half of the hosted intent feed — the applied/refused
# intents the apply lane already wrote under `ideation/dashboard/intents/`,
# served read-only from the SAME checkout `/source/` is served from. No new
# write path and no credential: the pod reads files it already has (D16).
#
# DELIBERATELY NOT `/intents`. That path belongs to the intent INBOX: the
# dox-auth gateway routes `/intents`, `/intents/*` and `/intents?*` to the
# inbox pod and everything else here (Omnigent-Install `dox_auth/server.py`
# `upstream_for`), so a route of that name would be unreachable in the only
# deployment that needs it. The two feeds are two origins-of-truth reachable
# same-origin, and the browser joins them; naming this one after the inbox
# would have made that join impossible to test and impossible to serve.
COMMITTED_INTENTS_ROUTE = "/committed-intents.json"
ACTIONS_REFRESH_ROUTE = "/actions/refresh"
# add-register-edit-lane: the header's apply button — the serve runs the
# fulfilment lane once (Brett's ruling: the click is the deliberate human
# act; only RECORDED commissions are ever applied, so D2's boundary holds).
ACTIONS_APPLY_REGISTER_EDITS_ROUTE = "/actions/apply-register-edits"
# add-shared-identity-seeds: DRAFT a DTN candidate-register seed from a
# repository-lens region. Read-only by construction — it returns TEXT the
# human merges and never opens the register for writing — so it is loopback-
# gated like every local action but needs NO gate capability, which is also
# what lets it answer from a composed (read-only) view.
ACTIONS_DTN_SEED_ROUTE = "/actions/dtn-seed"
# The STAGING-QUEUE seed: the same seed-first, write-nothing contract for a
# set of documents the human selected in the lens matrix. It drafts the
# fragment `ideation/staging/<topic>/` expects; the human places it.
ACTIONS_STAGING_SEED_ROUTE = "/actions/staging-seed"


class LaneRoutes:
    """openxFactory's own lane routes, mixed into `DashboardHandler`.

    Every gating primitive these handlers reach (`loopback`, `capabilities`,
    `actor`, `_send_json`, `_read_json_body`, `source`, `checkout_root`)
    resolves through the MRO to `serve.py`'s core, which is what makes a
    contributed route refuse exactly where a fixed core arm refused.
    """

    # ---- refresh route (add-dashboard-repo-selector, design D7) ----
    def _handle_dtn_seed(self) -> None:
        """Draft a DTN candidate-register seed from a project's SHARED
        IDENTITIES (add-shared-identity-seeds): the identities two or more of
        the named member repositories carry, which is the promotion process's
        first candidate rule computed rather than eyeballed.

        WRITES NOTHING. The response is the register row + detail section as
        TEXT, in the register's own format and numbering, for a human to
        merge — the same seed-first discipline the neutrality-drift lane
        records. That is why this route asks for loopback but not the gate
        capability, and why it can answer while a composed, read-only view is
        on screen.

        The carriers are recomputed HERE from the serve's own composed view;
        the client names the project, the visible subset, and (optionally)
        the exact carrier COMBINATION a lens region stands for — never the
        evidence itself. `combination` is what keeps a seed honest to the
        region it was drafted from: a row reading "carried by 3" drafts those
        identities and no others."""
        if not self.loopback:
            self._send_json(403, {"ok": False, "error": "loopback_only",
                                  "message": "seed drafting is loopback-only"})
            return
        body = self._read_json_body()
        if body is None:
            return
        project = str(body.get("project_id") or "").strip()
        if not project:
            self._send_json(400, {"ok": False, "error": "bad_request",
                                  "message": "project_id is required"})
            return
        repositories = body.get("repositories")
        combination = body.get("combination")
        for name, value in (("repositories", repositories),
                            ("combination", combination)):
            if value is not None and not isinstance(value, list):
                self._send_json(400, {"ok": False, "error": "bad_request",
                                      "message": f"{name} must be a list"})
                return
        if self.source is None:
            self._send_json(403, {"ok": False, "error": "action_unavailable",
                                  "message": "no snapshot source on this plane"})
            return
        composed = self.source.compose_view(project)
        if composed is None:
            self._send_json(404, {"ok": False, "error": "unknown_project",
                                  "message": f"no composed view for {project!r}"})
            return

        import datetime
        from doc_health import shared_identity as si
        rows = si.shared_identities(composed.get("documents"),
                                    repositories=repositories,
                                    exactly=combination)
        if not rows:
            self._send_json(200, {
                "ok": False, "error": "nothing_shared",
                "message": "no document identity is carried by two or more of "
                           "the named repositories — there is no candidate to "
                           "draft, which is itself the honest answer"})
            return
        register = Path(self.checkout_root) / si.REGISTER_PATH
        try:
            register_text = register.read_text(encoding="utf-8")
        except OSError:
            register_text = ""       # no register reachable: number from zero
        draft = si.draft_seed(
            register_text, rows, project=project,
            as_of=datetime.date.today().isoformat())
        payload = draft.as_dict()
        payload["ok"] = True
        payload["register"] = si.REGISTER_PATH
        self._send_json(200, payload)

    def _handle_staging_seed(self) -> None:
        """Draft a STAGING-QUEUE fragment from the documents the human selected
        in the lens matrix (Brett, 2026-08-08: "I should have a checkbox on
        each one to generate the seed from checked").

        WRITES NOTHING, like the register seed beside it: the response is the
        fragment as TEXT plus the path it belongs at. That is why this route
        asks for loopback but not the gate capability, and why it can answer
        while a read-only composed view is on screen.

        The client names the DOCUMENTS; their terms and repositories are read
        HERE from the serve's own snapshot. A client that could supply the
        terms could draft a fragment claiming a convergence the corpus does
        not have, and the fragment's whole value is that its evidence is
        checkable against the tree.
        """
        if not self.loopback:
            self._send_json(403, {"ok": False, "error": "loopback_only",
                                  "message": "seed drafting is loopback-only"})
            return
        body = self._read_json_body()
        if body is None:
            return
        project = str(body.get("project_id") or "").strip()
        wanted = body.get("documents")
        if not isinstance(wanted, list) or not wanted:
            self._send_json(400, {"ok": False, "error": "bad_request",
                                  "message": "documents must be a non-empty list"})
            return
        if self.source is None:
            self._send_json(403, {"ok": False, "error": "action_unavailable",
                                  "message": "no snapshot source on this plane"})
            return

        # a composed project view when the plane has one, else the active
        # snapshot — the keyword lens runs on both, so the seed must too
        snapshot = self.source.compose_view(project) if project else None
        if snapshot is None:
            entry = self.source.registry.resolve(None)
            snapshot = entry.read_json() if entry is not None else None
        if not isinstance(snapshot, dict):
            self._send_json(404, {"ok": False, "error": "unknown_project",
                                  "message": "no snapshot to read the "
                                             "selected documents from"})
            return

        by_id = {}
        for doc in snapshot.get("documents") or []:
            if not isinstance(doc, dict):
                continue
            for key in (doc.get("id"), doc.get("path")):
                if key:
                    by_id.setdefault(str(key), doc)
        rows, missing = [], []
        for name in wanted:
            doc = by_id.get(str(name))
            if doc is None:
                missing.append(str(name))
            else:
                rows.append(doc)
        if missing:
            self._send_json(404, {
                "ok": False, "error": "unknown_document",
                "message": "not in this snapshot: " + ", ".join(missing[:5])})
            return

        import datetime
        from doc_health import staging_seed as ss
        existing = []
        staging_root = Path(self.checkout_root) / ss.STAGING_DIR
        try:
            existing = sorted(p.name for p in staging_root.iterdir() if p.is_dir())
        except OSError:
            existing = []       # no queue reachable: no collision to avoid
        draft = ss.draft_staging_seed(
            rows, project=project or (snapshot.get("repository") or "corpus"),
            as_of=datetime.date.today().isoformat(),
            repository=str(snapshot.get("repository") or "openxFactory"),
            existing=existing)
        payload = draft.as_dict()
        payload["ok"] = True
        payload["index"] = ss.STAGING_INDEX
        self._send_json(200, payload)

    def _handle_apply_register_edits(self) -> None:
        """Run the register-edit fulfilment lane once
        (add-register-edit-lane): apply every dispatched
        project-register-edit commission, validate, deliver, commit + push
        the register file alone. Loopback + gate-actor only — the same
        human-console boundary as the gate verbs — and only RECORDED
        commissions are ever applied."""
        if not self.loopback:
            self._send_json(403, {"ok": False, "error": "loopback_only",
                                  "message": "applying register edits is "
                                             "loopback-only"})
            return
        if not self.capabilities.get("actions", {}).get("gate") or not self.actor:
            self._send_json(403, {"ok": False, "error": "action_unavailable",
                                  "message": "applying register edits needs "
                                             "the human gate capability"})
            return
        from openxdox.register_edit_lane import fulfil_once
        try:
            report = fulfil_once(Path(self.checkout_root))
        except Exception as exc:  # noqa: BLE001 - a lane crash must answer, not hang
            self._send_json(500, {"ok": False, "error": "lane_failed",
                                  "message": str(exc)[:300]})
            return
        payload = report.as_dict()
        payload["ok"] = report.error is None
        self._send_json(200 if payload["ok"] else 409, payload)

    def _handle_refresh_action(self) -> None:
        """ONE affordance, TWO bindings, chosen by the PLANE and never by the
        client body (a client cannot ask a served plane to regenerate, nor a
        local plane to re-fetch). Fail-closed: no binding refuses before any body
        parse, and the writing binding refuses off-loopback.

        UNGATED by ruling (D7 / open question 3's recommendation, stated
        explicitly): the artifact is derived, regeneration mutates nothing
        governed, and no build, rollout, or publication path exists here (D1)."""
        binding = self.capabilities.get("refresh", {}).get("binding")
        if not binding or self.source is None:
            self._send_json(403, {"ok": False, "error": "action_unavailable",
                                  "message": "refresh is unavailable on this plane "
                                             "(no data source and no served checkout)"})
            return
        if binding != registry_mod.BINDING_REFETCH and not self.loopback:
            self._send_json(403, {"ok": False, "error": "loopback_only",
                                  "message": "the regenerate binding is loopback-only"})
            return
        body = self._read_json_body()
        if body is None:
            body = {}  # a plain POST means "refresh the active snapshot"
        if not isinstance(body, dict):
            self._send_json(400, {"ok": False, "error": "invalid_body",
                                  "message": JSON_OBJECT_BODY_REQUIRED})
            return
        repository = body.get("repository")
        ref = body.get("ref")
        if repository is not None and not isinstance(repository, str):
            self._send_json(400, {"ok": False, "error": "invalid_body",
                                  "message": "repository must be a string"})
            return
        if ref is not None and not isinstance(ref, str):
            self._send_json(400, {"ok": False, "error": "invalid_body",
                                  "message": "ref must be a string"})
            return
        # FR-048 again, on the one WRITE-ish route reachable off-loopback: the
        # read-only `refetch` binding is available on the hosted plane by design,
        # so a hosted client could otherwise ask it to refresh a session ref.
        # (`regenerate` has already refused above, being loopback-only.)
        if hosted_ref_refused(self.loopback, ref):
            self._send_json(403, {"ok": False, "error": "session_unavailable",
                                  "message": HOSTED_SESSION_REFUSAL})
            return
        self._run_refresh(repository, ref)

    def _run_refresh(self, repository: str | None, ref: str | None) -> None:
        """Run the binding. EVERY failure keeps the registry as it was, so the
        previously rendered snapshot stays renderable and the client reports the
        failure inline (spec scenario "A refresh fails")."""
        try:
            result = self.source.refresh(repository=repository, ref=ref)
        except registry_mod.PublicationRefused:
            self._send_json(403, {"ok": False, "error": "publication_refused",
                                  "message": "a non-main snapshot is never published"})
            return
        except registry_mod.DataSourceError as exc:
            sys.stderr.write(f"[actions/refresh] data source unreachable: {exc}\n")
            self._send_json(502, {"ok": False, "error": "source_unreachable",
                                  "message": "the data source could not be read; "
                                             "the previous snapshot is still shown"})
            return
        except ValueError as exc:
            sys.stderr.write(f"[actions/refresh] {exc}\n")
            self._send_json(404, {"ok": False, "error": "unknown_snapshot",
                                  "message": "no such (repository, ref) is registered"})
            return
        except Exception:  # noqa: BLE001 — never leak a traceback over the wire
            self._send_json(500, {"ok": False, "error": "action_failed",
                                  "message": "refresh failed; see the server log"})
            return
        # Keep the handler's own divergence anchor in step with the new active
        # snapshot, so a subsequent read reports the refreshed revision.
        active = self._active_entry()
        if active is not None:
            type(self).source_revision = active.source_revision
        self._send_json(200, {"ok": True, **result})

    def _serve_committed_intents(self, head_only: bool) -> None:
        """`/committed-intents.json` — the CORPUS half of the intent feed
        (add-ideation-intent-plane task 4.4; Brett Heap's ruling D-1 on
        openxFactory #656: "the applied/refused feed is SERVED FROM THE CORPUS
        ... read-only beside the inbox's pending list — no new write path, the
        hosted pod stays credential-free").

        The apply lane commits every decision it makes — applied AND refused —
        under `ideation/dashboard/intents/`, and that directory is inside the
        checkout this serve already exposes read-only through `/source/` (the
        hosted image bakes `openxFactory/ideation/` and points
        `--checkout-root` at it). So the feed is a directory walk of files this
        process can already read, and the pod gains no authority it did not
        have: no network call, no token, no write.

        Read PER REQUEST rather than at startup, exactly as
        `_serve_project_register` is: the lane commits between polls, and on the
        hosted plane a rebake replaces the baked tree under a running pod.

        An absent or empty directory is an EMPTY FEED, not a 404 — a checkout
        with no intents yet is the ordinary first state, and the overlay must
        be able to say "nothing yet" rather than "the feed is broken". The only
        404 here is a serve with no checkout root at all.

        Filters mirror the inbox's `GET /intents?actor=&status=` so one client
        can ask both feeds the same question, plus `?target=` (the tile the
        overlay is decorating) and `?limit=`. Bounded on every axis by
        `intent_feed`; `truncated` says so when a bound bit.

        DISCLOSES NOTHING NEW. Every byte this returns is already readable at
        `/source/ideation/dashboard/intents/...` on the same serve — this route
        parses those files rather than reaching new ones, which is why it sits
        with the other unguarded read routes rather than behind the loopback
        console token (that token guards process-launch authority, and this
        route carries none).
        """
        from ideation_dashboard import intent_feed
        if not self.checkout_root:
            self.send_error(404, "no checkout")
            return
        params = urllib.parse.parse_qs(
            urllib.parse.urlsplit(self.path).query)
        try:
            limit = int((params.get("limit") or [intent_feed.DEFAULT_LIMIT])[0])
        except (TypeError, ValueError):
            limit = intent_feed.DEFAULT_LIMIT
        document = intent_feed.read_committed_intents(
            Path(self.checkout_root),
            actor=(params.get("actor") or [None])[0],
            status=(params.get("status") or [None])[0],
            target=(params.get("target") or [None])[0],
            limit=limit)
        self._serve_bytes(json.dumps(document).encode("utf-8"), JSON_CTYPE,
                          head_only)


class LaneRoutesExtension:
    """openxFactory's route contribution: one read feed and four write lanes.

    Conforms to `route_extension.RouteExtension` STRUCTURALLY — this column
    imports nothing from the core it contributes to, which is the direction the
    § 3 carve needs even for the column that stays.
    """

    def routes(self) -> tuple[route_extension.RouteBinding, ...]:
        return (
            route_extension.RouteBinding("GET", COMMITTED_INTENTS_ROUTE, False,
                                         "_serve_committed_intents"),
            route_extension.RouteBinding("POST", ACTIONS_REFRESH_ROUTE, False,
                                         "_handle_refresh_action"),
            route_extension.RouteBinding("POST", ACTIONS_DTN_SEED_ROUTE, False,
                                         "_handle_dtn_seed"),
            route_extension.RouteBinding("POST", ACTIONS_STAGING_SEED_ROUTE,
                                         False, "_handle_staging_seed"),
            route_extension.RouteBinding("POST",
                                         ACTIONS_APPLY_REGISTER_EDITS_ROUTE,
                                         False, "_handle_apply_register_edits"),
        )
