"""THE CONTRIBUTED DISPATCH TABLE, and the gating it must not lose
(`split-opendox-two-layer-product` § 2.4, PR 3 of 4).

PR 3 is the first slice where the route seam carries live traffic: five read
and write arms left `_route`/`do_POST`'s fixed tables and arrive as
`RouteBinding`s instead. `test_extension_point_parity.py` pins what is LEFT in
those tables; this file pins what LEFT them, at the same strength and in the
same shape — a literal tuple, ordered, compared whole — so the two files
together still describe the entire dispatch of this server.

FIVE THINGS, because each answers a different question a reviewer of a move has:

  1. **The methods still resolve on `DashboardHandler`.** A move that fell out
     of the base list, or a mixin that failed to compose, would leave the
     handler without the method — which `route_extension.resolve_handlers`
     refuses at build time, but only for routes that are BOUND. The ones that
     stayed core arms (`_serve_snapshot`) have no binding to refuse them.
  2. **The profile is what the server is assembled with.** Three extensions,
     each conforming to the protocol, in a declared order.
  3. **The flattened binding set, exactly.** Method, pattern, prefix-ness and
     handler name for all nine, in consult order — the table the pinned
     `ROUTE_ARMS`/`DO_POST_ARMS` no longer cover.
  4. **Every moved WRITE route still refuses off-loopback**, driven through a
     real `build_server`, giving the SAME status and the SAME error code a core
     write route gives. This is the property the whole by-name dispatch shape
     exists to preserve (`corpus-adapter-seam` requirement 4's analogue, one
     level up): a contributed route reaches `self.loopback` because it is
     dispatched against the live handler, not because its author remembered to
     check.
  5. **The pre-carve column re-homing stays done.** Split S-3 (§ 3.1) moved
     `hosted_index` out of `serve_wire.py` — the module that goes WHOLE to
     openDox — into this openXdox column, leaving NO re-export behind, because
     the carve manifest files each path under exactly one column. Re-adding it
     to the wire module (or importing it back there for convenience) would put
     openXdox content into an openDox file again with nothing else red.

WHAT THIS FILE IS NOT. It is not a second copy of the behavioural suites. Every
moved route keeps its own tests — `test_repo_selector.py` for refresh and the
index, `test_renderer.py`/`test_source_dot_directories.py` for `/source`,
`test_session_verbs.py`/`test_branch_session.py` for the gate verbs,
`test_intent_plane_boundary.py` for the committed-intent feed — and those run
UNMODIFIED, which is the actual proof that the move changed no behaviour.
"""

from __future__ import annotations

import http.client
import json
import threading
from contextlib import contextmanager

import pytest

from conftest import (BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit,
                      dashboard_web_root)

import route_extension  # noqa: E402

# The composition point, at its POST-SHED home. `scripts/
# ideation_dashboard/profile_openxfactory.py` is the carve manifest's one
# `deleted_at_carve` row and the shed removed it; openxFactory's profile now
# lives at `scripts/profile_openxfactory.py` (plain top-level spelling), and
# `opendox_host.register_openxfactory()` — called from the conftest — hands it
# to `opendox.domain_profile` for both consumers' lazy proxy to resolve: the
# openxFactory half of RULED ASK-2 option (2) (`#656` comment `5628886636`).
import profile_openxfactory  # noqa: E402
from opendox import serve as serve_mod  # noqa: E402
from ideation_dashboard import serve_openxfactory_lanes  # noqa: E402
from openxdox import serve_gate  # noqa: E402
from opendox import serve_wire  # noqa: E402
from openxdox import serve_projection  # noqa: E402
from openxdox.generator import generate_snapshot  # noqa: E402

# The dashboard's asset root, DERIVED from `web/index.html`'s manifest row
# (§ 5.2, RULED (a), `#656` `5625573095`). The assets moved to openDox-code
# with the serve and `dashboard_web_root()` reads where from the row rather
# than spelling the destination here; its docstring records the one
# `not_moved` asset — openxFactory's own intent-feed view — and why a merged
# asset root is § 4.3 composition work rather than this constant's job.
WEB = dashboard_web_root()

#: The handlers PR 3 moved out of `serve.py`, with the module each landed in.
#: `_serve_snapshot` is here too although its ARM stayed core: the method moved,
#: and a method that moved and did not compose back is exactly what this checks.
MOVED_HANDLERS = {
    "_handle_gate_action": serve_gate.GateRoutes,
    "_log_gate_failure": serve_gate.GateRoutes,
    "_query_key": serve_projection.ProjectionRoutes,
    "_read_snapshot": serve_projection.ProjectionRoutes,
    "_serve_snapshot": serve_projection.ProjectionRoutes,
    "_hosted_entry_refused": serve_projection.ProjectionRoutes,
    "_serve_index": serve_projection.ProjectionRoutes,
    "_keyed_source": serve_projection.ProjectionRoutes,
    "_serve_source": serve_projection.ProjectionRoutes,
    "_refuse_bare_source": serve_projection.ProjectionRoutes,
    "_handle_dtn_seed": serve_openxfactory_lanes.LaneRoutes,
    "_handle_staging_seed": serve_openxfactory_lanes.LaneRoutes,
    "_handle_apply_register_edits": serve_openxfactory_lanes.LaneRoutes,
    "_handle_refresh_action": serve_openxfactory_lanes.LaneRoutes,
    "_run_refresh": serve_openxfactory_lanes.LaneRoutes,
    "_serve_committed_intents": serve_openxfactory_lanes.LaneRoutes,
}

#: The CONTRIBUTED table, in `collect_bindings`' consult order: every exact
#: binding in declaration order, then every prefix binding in declaration order.
#: Nine, not ten: `/snapshot.json` stayed a core arm (see the module docstring of
#: `serve_projection.py` for why a frozen pattern cannot carry the
#: `build_server(snapshot_route=…)` keyword).
CONTRIBUTED_BINDINGS = (
    ("GET", "/snapshot-index.json", False, "_serve_index"),
    ("GET", "/source", False, "_refuse_bare_source"),
    ("GET", "/committed-intents.json", False, "_serve_committed_intents"),
    ("POST", "/actions/refresh", False, "_handle_refresh_action"),
    ("POST", "/actions/dtn-seed", False, "_handle_dtn_seed"),
    ("POST", "/actions/staging-seed", False, "_handle_staging_seed"),
    ("POST", "/actions/apply-register-edits", False,
     "_handle_apply_register_edits"),
    ("POST", "/actions/gate/", True, "_handle_gate_action"),
    ("GET", "/source/", True, "_serve_source"),
)

#: The moved WRITE routes, each with a body a real client would send. Every one
#: must refuse off-loopback with the SAME verdict a core write route gives.
MOVED_WRITE_ROUTES = (
    "/actions/refresh",
    "/actions/dtn-seed",
    "/actions/staging-seed",
    "/actions/apply-register-edits",
    "/actions/gate/ratify",
)

#: The core comparator: a fixed arm of `do_POST` whose first clause is the same
#: `if not self.loopback` refusal (`serve_project.ProjectRoutes`).
CORE_WRITE_ROUTE = "/actions/edit"


@contextmanager
def serving(tmp_path):
    snap = tmp_path / "snapshot.json"
    snap.write_text(json.dumps(generate_snapshot(
        BASE_REPO, "fixture-repo", source_revision=PINNED_REVISION,
        git=FakeGit())), encoding="utf-8")
    httpd = serve_mod.build_server(WEB, snap, BASE_REPO, head=PINNED_REVISION,
                                   actor="brett")
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address[:2]
    try:
        yield httpd, host, port
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def handler_class(httpd):
    return getattr(httpd.RequestHandlerClass, "func", httpd.RequestHandlerClass)


def post(host, port, path, body):
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request("POST", path, body=json.dumps(body),
                 headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    raw = resp.read()
    conn.close()
    try:
        return resp.status, json.loads(raw.decode("utf-8") or "{}")
    except ValueError:
        return resp.status, None


# ---------------------------------------------------------------------------
# 1. the methods composed back
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name,owner", sorted(MOVED_HANDLERS.items()))
def test_every_moved_handler_still_resolves_on_the_request_handler(name, owner):
    """Through the MRO, from the column module that now owns it."""
    resolved = getattr(serve_mod.DashboardHandler, name, None)
    assert resolved is not None and callable(resolved), (
        f"{name} no longer resolves on DashboardHandler — the column mixin "
        "holding it is not composed into the base list")
    assert name in vars(owner), (
        f"{name} is not defined on {owner.__module__}.{owner.__qualname__}; "
        "the move landed somewhere else than this file records")
    assert name not in vars(serve_mod.DashboardHandler), (
        f"{name} is defined on DashboardHandler AS WELL as on "
        f"{owner.__qualname__} — a second copy that would shadow the column's, "
        "which is a fork of the route, not a move of it")


# ---------------------------------------------------------------------------
# 2. the profile
# ---------------------------------------------------------------------------


def test_the_in_tree_profile_declares_exactly_three_conforming_extensions():
    extensions = profile_openxfactory.ROUTE_EXTENSIONS
    assert len(extensions) == 3, extensions
    for extension in extensions:
        assert isinstance(extension, route_extension.RouteExtension), extension
    assert [type(e).__name__ for e in extensions] == [
        "GateRoutesExtension", "ProjectionRoutesExtension",
        "LaneRoutesExtension"]


# ---------------------------------------------------------------------------
# 3. the contributed dispatch table
# ---------------------------------------------------------------------------


def test_the_contributed_dispatch_table_is_exactly_the_routes_that_moved():
    flat = tuple((b.method, b.pattern, b.is_prefix, b.handler)
                 for b in route_extension.collect_bindings(
                     profile_openxfactory.ROUTE_EXTENSIONS))
    assert flat == CONTRIBUTED_BINDINGS, (
        "the contributed route table changed. Together with "
        "test_extension_point_parity.ROUTE_ARMS/DO_POST_ARMS this tuple is the "
        "WHOLE dispatch of this server: a route that appears in neither is "
        "unreachable, and one that appears in both is a collision.")


def test_the_exact_source_binding_is_consulted_before_the_prefix_one():
    """The `/source` ordering trap, pinned.

    `if path == "/source" or path == "/source/"` was partly dead in `_route`:
    the `startswith("/source/")` arm fired first, so `/source/` reached
    `_serve_source("")` and NEVER `send_error(404, "no source path")`. Moving
    only the prefix would have promoted the surviving core arm above the
    binding and changed that answer. `collect_bindings` groups exact ahead of
    prefix, which reproduces the old order — but only as long as `/source`
    stays EXACT and `/source/` stays a PREFIX.
    """
    bindings = route_extension.collect_bindings(
        profile_openxfactory.ROUTE_EXTENSIONS)
    bare = route_extension.match(bindings, "GET", "/source")
    trailing = route_extension.match(bindings, "GET", "/source/")
    nested = route_extension.match(bindings, "GET", "/source/a/b.md")
    assert bare is not None and bare[0].handler == "_refuse_bare_source"
    assert trailing is not None and trailing[0].handler == "_serve_source"
    assert trailing[1] == "", "the trailing-slash form must serve an EMPTY tail"
    assert nested is not None and nested[0].handler == "_serve_source"
    assert nested[1] == "a/b.md"


def test_a_bare_source_request_still_answers_the_same_refusal(tmp_path):
    """The wire half of the trap above, over a real server."""
    with serving(tmp_path) as (_httpd, host, port):
        conn = http.client.HTTPConnection(host, port, timeout=5)
        conn.request("GET", "/source")
        bare = conn.getresponse()
        bare.read()
        conn.close()
        conn = http.client.HTTPConnection(host, port, timeout=5)
        conn.request("GET", "/source/")
        trailing = conn.getresponse()
        trailing_body = trailing.read()
        trailing_divergence = trailing.getheader("X-Snapshot-Divergence")
        conn.close()
    assert bare.status == 404
    # the trailing-slash form is the OTHER answer: the source route's own 404,
    # with divergence headers and a zero-length body — not an HTML error page
    assert trailing.status == 404
    assert trailing_body == b""
    assert trailing_divergence is not None


# ---------------------------------------------------------------------------
# 4. the gating a contributed route must not lose
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("path", MOVED_WRITE_ROUTES)
def test_every_moved_write_route_refuses_off_loopback_like_a_core_one(
        tmp_path, path):
    """One parity test per moved write route (§ 2.4 PR 3's own gate).

    The handler is reached by name against the LIVE `DashboardHandler`, so it
    meets the same `self.loopback` the core comparator meets. Anything else —
    a binding carrying its own callable, a handler resolved against a stripped
    request object — would let a contributed route answer differently, and this
    is the assertion that would go red.
    """
    with serving(tmp_path) as (httpd, host, port):
        handler_class(httpd).loopback = False
        contributed_status, contributed = post(host, port, path, {})
        core_status, core = post(host, port, CORE_WRITE_ROUTE, {})
    assert core_status == 403 and core["error"] == "loopback_only"
    assert contributed_status == core_status, (
        f"{path} answered {contributed_status} off-loopback where the core "
        f"route {CORE_WRITE_ROUTE} answered {core_status}")
    assert contributed["error"] == core["error"], contributed


def test_the_off_loopback_probe_is_not_vacuous(tmp_path):
    """The negative control: the same routes on a LOOPBACK plane must NOT give
    `loopback_only`, or the parametrized test above would pass against a server
    that refuses everything for some unrelated reason."""
    with serving(tmp_path) as (_httpd, host, port):
        verdicts = {path: post(host, port, path, {}) for path in
                    MOVED_WRITE_ROUTES}
    for path, (status, payload) in verdicts.items():
        assert not (status == 403 and (payload or {}).get("error")
                    == "loopback_only"), (
            f"{path} answered loopback_only on a LOOPBACK bind — the parity "
            "test above is asserting nothing")


# ---------------------------------------------------------------------------
# 5. the pre-carve column re-homing (split S-3, § 3.1)
# ---------------------------------------------------------------------------


def test_the_hosted_index_projection_belongs_to_the_projection_column():
    """`hosted_index` is defined HERE and is not reachable on `serve_wire`.

    Both halves matter and neither implies the other for the carve manifest:
    the wire module is an openDox row, so an openXdox rule defined in it — or
    merely RE-EXPORTED from it for a caller's convenience — is a path with two
    columns, which is the shape § 3.1 cannot file. `getattr` catches both,
    since a `def` and an `import` set the same module attribute.
    """
    assert callable(getattr(serve_projection, "hosted_index", None))
    assert getattr(serve_wire, "hosted_index", None) is None, (
        "`hosted_index` is reachable on `serve_wire` again — S-3 re-homed it "
        "into `serve_projection` and left no re-export; see `serve_wire.py`'s "
        "module docstring")


def test_serve_re_exports_the_hosted_index_from_its_new_home():
    """The public surface S-3 preserved: `serve.hosted_index` still resolves,
    and resolves to the projection column's function rather than to a second
    copy left in the wire module."""
    assert serve_mod.hosted_index is serve_projection.hosted_index
