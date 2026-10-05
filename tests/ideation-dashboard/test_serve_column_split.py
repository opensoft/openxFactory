"""THE CONTRIBUTED DISPATCH TABLE, and the gating it must not lose
(`split-opendox-two-layer-product` § 2.4, PR 3 of 4).

PR 3 is the first slice where the route seam carries live traffic: five read
and write arms left `_route`/`do_POST`'s fixed tables and arrive as
`RouteBinding`s instead. `test_extension_point_parity.py` pins what is LEFT in
those tables; this file pins what LEFT them, at the same strength and in the
same shape — a literal tuple, ordered, compared whole — so the two files
together still describe the entire dispatch of this server.

FIVE THINGS, because each answers a different question a reviewer of a move has:

  1. **The methods still resolve on the class the server binds.** A move that
     fell out of the base list, or a mixin that failed to compose, would leave
     the handler without the method — which `route_extension.resolve_handlers`
     refuses at build time, but only for routes that are BOUND. The ones that
     stayed core arms (`_serve_snapshot`) have no binding to refuse them. The
     lanes column is composed in by the host profile's handler contribution
     from plan 034's T011 on, so it is resolved on the bound class, not on
     `DashboardHandler` (T045).
  2. **The profile is what the server is assembled with.** Three extensions,
     each conforming to the protocol, in a declared order.
  3. **The flattened binding set, exactly.** Method, pattern, prefix-ness and
     handler name for all seven (nine at PR 3; `/source` + `/source/` left for
     a fixed core arm at § 3.4 slice S6, RULED Q4), in consult order — the
     table the pinned `ROUTE_ARMS`/`DO_POST_ARMS` no longer cover.
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
#:
#: `_keyed_source`/`_serve_source`/`_refuse_bare_source` LEFT this dict at § 3.4
#: slice S6 (RULED Q4, `#656` comment `5642758731`): `/source` returned from
#: CONTRIBUTED to FIXED, and the three methods moved AGAIN, this time to
#: `opendox.serve` itself rather than to a sibling column's mixin — so "did the
#: move compose back onto DashboardHandler through a mixin" is not even the
#: right question for them any more; they are declared directly on the request
#: handler's own module now. That property (fixed, ordered ahead of the § 2.4
#: consult, unshadowable) is proven at the repository that owns it —
#: `opensoft/openDox-code`'s `tests/test_source_core_arm.py`, § 2's dispatch-
#: order and unshadowability tests — not here.
#:
#: The snapshot arm's four handlers LEFT this dict at plan 034's phase-3 pin
#: (T094): openXdox-code's T086 trimmed `ProjectionRoutes` to `_serve_index`,
#: because the four have been `DashboardHandler`'s own since T055 and the
#: handler-contribution facet refuses a mixin that shadows a core name. They
#: are held as the core's own in `SNAPSHOT_ARM_HANDLERS` below, and the test
#: that walks this dict walks them too, with `DashboardHandler` as the owner.
MOVED_HANDLERS = {
    "_handle_gate_action": serve_gate.GateRoutes,
    "_log_gate_failure": serve_gate.GateRoutes,
    "_serve_index": serve_projection.ProjectionRoutes,
    "_handle_dtn_seed": serve_openxfactory_lanes.LaneRoutes,
    "_handle_staging_seed": serve_openxfactory_lanes.LaneRoutes,
    "_handle_apply_register_edits": serve_openxfactory_lanes.LaneRoutes,
    "_handle_refresh_action": serve_openxfactory_lanes.LaneRoutes,
    "_run_refresh": serve_openxfactory_lanes.LaneRoutes,
    "_serve_committed_intents": serve_openxfactory_lanes.LaneRoutes,
}

#: THE `/snapshot.json` ARM'S FOUR HANDLERS, which openDox-code #59
#: (`fa140875`, plan 034 T055) made `DashboardHandler`'s own again, so a
#: standalone server answers the arm without openXdox's column. From plan
#: 034's phase-3 pin (T094) openXdox's column no longer carries them: T086
#: trimmed `serve_projection.ProjectionRoutes` to `_serve_index`, and T084
#: retired openDox's Late stand-ins, so the column arrives through the facet
#: and the core handler's own four are the only ones. They stay rows of
#: `test_every_moved_handler_still_resolves_on_the_request_handler`, owned by
#: `DashboardHandler` now, rather than a test of their own: the carve's test
#: mapping counts this file's test functions by their definition marker, raw
#: (`scripts/carve_test_mapping.py`, `count`), and pins the total
#: (`tests/carve_test_mapping/`), so a ninth would move a figure that file
#: pins. The marker is not spelled out here for the same reason: a comment
#: carrying it counts.
SNAPSHOT_ARM_HANDLERS = (
    "_hosted_entry_refused", "_query_key", "_read_snapshot", "_serve_snapshot")

#: The rows the moved-handler test walks: every moved handler with the column
#: that owns it, and the snapshot arm's four with the core handler.
RESOLVED_HANDLERS = sorted(
    [*MOVED_HANDLERS.items(),
     *((name, serve_mod.DashboardHandler) for name in SNAPSHOT_ARM_HANDLERS)])


def _snapshot_arm_is_core() -> bool:
    """Whether the pinned openDox leg's core handler owns the four handlers
    (from T055) or none of them (before it). A leg defining some and not the
    others is neither layout, and is refused."""
    core = [name for name in SNAPSHOT_ARM_HANDLERS
            if name in vars(serve_mod.DashboardHandler)]
    assert core in ([], list(SNAPSHOT_ARM_HANDLERS)), (
        f"DashboardHandler defines {core} of the snapshot arm's four handlers "
        f"{list(SNAPSHOT_ARM_HANDLERS)}: all four are the core's from T055, and "
        "none before it")
    return bool(core)


#: The CONTRIBUTED table, in `collect_bindings`' consult order: every exact
#: binding in declaration order, then every prefix binding in declaration order.
#: Seven, not ten: `/snapshot.json` stayed a core arm (see the module docstring
#: of `serve_projection.py` for why a frozen pattern cannot carry the
#: `build_server(snapshot_route=…)` keyword), and `/source` + `/source/` LEFT
#: at § 3.4 slice S6 (RULED Q4, `#656` comment `5642758731`) for a FIXED core
#: arm in `opendox/serve.py` — a route-ownership correction, not a behaviour
#: change (`test_a_bare_source_request_still_answers_the_same_refusal` below
#: proves the wire answer is unchanged).
CONTRIBUTED_BINDINGS = (
    ("GET", "/snapshot-index.json", False, "_serve_index"),
    ("GET", "/committed-intents.json", False, "_serve_committed_intents"),
    ("POST", "/actions/refresh", False, "_handle_refresh_action"),
    ("POST", "/actions/dtn-seed", False, "_handle_dtn_seed"),
    ("POST", "/actions/staging-seed", False, "_handle_staging_seed"),
    ("POST", "/actions/apply-register-edits", False,
     "_handle_apply_register_edits"),
    ("POST", "/actions/gate/", True, "_handle_gate_action"),
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


@pytest.mark.parametrize("name,owner", RESOLVED_HANDLERS)
def test_every_moved_handler_still_resolves_on_the_request_handler(
        tmp_path, name, owner):
    """Through the MRO of the class a real `build_server` BINDS, from the
    column module that now owns it.

    RESOLVED WHERE THE SERVER BINDS IT, not on `DashboardHandler` (plan 034
    T045, R1Q1 (a), `#656` comment `5817152735`; a NAMED composition test
    under R1Q2 (a)). openDox-code's T011 took `LaneRoutes` off
    `DashboardHandler`'s bases, and the host profile now contributes it
    through the handler-contribution facet, which `build_server` composes into
    the class it binds. So from that pin on, the six lanes methods resolve on
    the bound class and on `DashboardHandler` not at all. The bound class
    answers every moved method at both pins, which is the property this test
    exists for: a column that failed to compose leaves the server without it.
    A lanes method must also BE the column's own function, since the facet
    only adds: never a copy, a forwarder or a core method of the same name."""
    with serving(tmp_path) as (httpd, _host, _port):
        bound = handler_class(httpd)
    resolved = getattr(bound, name, None)
    assert resolved is not None and callable(resolved), (
        f"{name} no longer resolves on the class build_server binds — the "
        "column mixin holding it is not composed into it")
    assert name in vars(owner), (
        f"{name} is not defined on {owner.__module__}.{owner.__qualname__}; "
        "the move landed somewhere else than this file records")
    if owner is serve_mod.DashboardHandler:
        # The `/snapshot.json` arm's four (T055): the core's own, no copy on
        # openXdox's column (T086's trim), and the bound class resolves the
        # core's definition.
        assert _snapshot_arm_is_core()
        assert name not in vars(serve_projection.ProjectionRoutes), (
            f"openXdox's ProjectionRoutes carries a copy of the core's {name}")
        assert resolved is vars(owner)[name], (
            f"{name} does not resolve to DashboardHandler's own")
        return
    assert name not in vars(serve_mod.DashboardHandler), (
        f"{name} is defined on DashboardHandler AS WELL as on "
        f"{owner.__qualname__} — a second copy that would shadow the column's, "
        "which is a fork of the route, not a move of it")
    # EVERY COLUMN ARRIVES THROUGH THE FACET from plan 034's phase-3 pin
    # (T094): openXdox's two as the lanes column does since T045, with no
    # Late stand-in forwarding them, so each method IS the column's own.
    assert resolved is vars(owner)[name], (
        f"{name} resolves on the bound class to {resolved!r}, not to "
        f"{owner.__qualname__}'s own function")


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


# `test_the_exact_source_binding_is_consulted_before_the_prefix_one` LEFT
# here at § 3.4 slice S6 (RULED Q4, `#656` comment `5642758731`): its subject,
# `/source` exact-before-prefix ordering, moved from `collect_bindings`'
# consult order (a property of the CONTRIBUTED table this file pins) to
# `opendox/serve.py`'s own FIXED-arm dispatch order — a property of code that
# now lives outside this file's domain entirely, not merely renamed. It is
# proven there instead: `opensoft/openDox-code`'s
# `tests/test_source_core_arm.py::test_route_dispatches_the_exact_arm_before_
# the_prefix_arm` asserts the identical ordering trap this test used to pin
# (bare-before-prefix, by direct source inspection of `_route`), at the
# repository that can now break it.


def test_a_bare_source_request_still_answers_the_same_refusal(tmp_path):
    """The wire-level half of the `/source` ordering trap, over a real server —
    UNCHANGED by § 3.4 slice S6 moving `/source` from a contributed binding to
    a fixed core arm (RULED Q4, `#656` comment `5642758731`, "a route-
    ownership correction, not a new capability"): the same two requests must
    still get the same two answers regardless of which mechanism serves them.
    The ordering property itself (why they must) is now pinned at
    `opensoft/openDox-code`'s `tests/test_source_core_arm.py` instead of
    immediately above this test, where it used to live."""
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


def test_serve_hands_the_hosted_index_to_its_new_home_and_keeps_no_copy():
    """S-3's re-home, at its POST-SLICE-2B resting place.

    S-3 moved `hosted_index` out of the wire module into the projection column
    and `serve.py` re-exported it so the public name kept resolving. BUILD
    slice 2b then dropped that re-export with a reason this test records
    rather than fights (`opendox/serve.py`:201-206): the statement "named
    openXdox at import time", and `hosted_index` is one of the FOUR re-exports
    that "had no reader anywhere in this repository" — it is "the column's own
    verb", and it "stays reachable at `openxdox.serve_projection`, which is
    where they live". The other two of the six kept their names in `serve.py`
    precisely because they DO have readers, and `test_oqb_replumb_2.py`'s
    predicate test covers that half.

    So what S-3 promised is asserted where S-3's subject now is: exactly ONE
    definition, on the projection column, and no copy left behind on either
    `serve_wire` or `serve` — a second copy is the drift S-3 existed to end,
    and a re-export openDox deleted for a layering reason is not one."""
    assert callable(getattr(serve_projection, "hosted_index", None))
    assert getattr(serve_wire, "hosted_index", None) is None
    assert getattr(serve_mod, "hosted_index", None) is None, (
        "`opendox.serve` binds `hosted_index` again — BUILD slice 2b dropped "
        "it because the statement named openXdox at import time and nothing "
        "in openDox read it; a restored re-export is that layering undone")
