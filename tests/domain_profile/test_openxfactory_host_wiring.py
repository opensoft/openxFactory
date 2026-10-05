"""openxFactory's host wiring for openDox's phase-1 seams (plan 034 T045, T046).

WHAT THIS FILE POLICES, the openxFactory half of #1144 tasks 2.2, 4.1 and 4.3:

  1. **T045, the lanes column** (R1Q1 (a), `#656` comment `5817152735`).
     `scripts/profile_openxfactory.py` declares `LaneRoutes` under openDox's
     handler-contribution facet, and the composite profile forwards it, so the
     class openDox's server binds carries the lanes column's methods, each the
     column's own function, and a real server serves the column's five routes
     through them.
  2. **T046, the other host wiring.** One process-start call,
     `opendox_host.register_openxfactory()`, fills every seam openDox-code's
     phase 1 declared with the code its reach used to import: the home corpus
     (4.1), the session notebook's scope (R1Q9 (a)), the scoped health check,
     the doxBench validators and the status-exemption rail (4.3). Its start
     asserts that the profile it registered is the one openDox answers (R1Q4
     (a)).
  3. **What a hosted request gets is unchanged.** The session notebook lists
     the same documents with the same bytes as the rule it replaces, a scoped
     health run answers what the old in-process run answered, and the doxBench
     validators and rail are the host's own.

TWO PINNED SHAPES, AND EVERY TEST HOLDS AT BOTH. Until plan 034's T047 moves
`contracts/opendox-pin.yaml`, the pinned openDox leg predates the seams: its
`DashboardHandler` still takes `LaneRoutes` as a base, and its reaches import
this repository's packages by name. From T047's pin on, the leg carries T010's
facet, T011's handler without the lanes base, and the five seams. A test whose
subject exists only at the second shape asserts, at the first, the fact that
makes it absent, so no test passes by skipping. `LEG_HAS_THE_SEAMS` is read
off the leg's own classes, never off openxFactory's replica of
`route_extension`, and `test_the_pinned_leg_is_one_of_the_two_shapes` refuses
any third one.

THE REGISTRIES ARE PROCESS-WIDE, so a test that needs a fresh one runs in a
SUBPROCESS, as `test_openxfactory_profile.py` explains for the profile.
"""

from __future__ import annotations

import http.client
import json
import subprocess
import sys
import textwrap
import threading
import types
from contextlib import contextmanager
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts"

# `tests/conftest.py` has already installed the reach and made the ONE call.
import opendox_host                                          # noqa: E402
import profile_openxfactory                                  # noqa: E402
from corpus_adapter_openxfactory import home_corpus as adapter_home_corpus  # noqa: E402
from doc_health import corpus as dh_corpus                   # noqa: E402
from ideation_dashboard import doxbench_contracts            # noqa: E402
from ideation_dashboard import doxbench_status_exemption     # noqa: E402
from ideation_dashboard import serve_openxfactory_lanes      # noqa: E402
from opendox import corpus_adapter                           # noqa: E402
from opendox import doxbench_packet                          # noqa: E402
from opendox import doxbench_trust                           # noqa: E402
from opendox import domain_profile as opendox_registry      # noqa: E402
from opendox import serve as serve_mod                       # noqa: E402
from opendox import serve_wire                               # noqa: E402
from opendox import workbench                                # noqa: E402
from opendox.profile_proxy import profile_openxfactory as proxy  # noqa: E402
from openxdox import serve_gate, serve_projection           # noqa: E402

LANE_ROUTES = serve_openxfactory_lanes.LaneRoutes

#: The columns the bound handler composes after the core, in the order the
#: facet collects them: the profile's own first, then each route extension's
#: (plan 034 T094; openXdox's two arrive through its extensions from T086).
CONTRIBUTED_COLUMNS = (LANE_ROUTES, serve_gate.GateRoutes,
                       serve_projection.ProjectionRoutes)

#: The six registration calls this host makes, each on the module that
#: declares it, in the order the host registers them: the five openDox-code's
#: phase 1 declared (T020, T025, T026, T027), and the binding-trust policy
#: T100 declared (plan 034 T094, #1144 16.3a), with the home corpus last
#: (`opendox_host.seams()` says why).
SEAM_CALLS = (
    (workbench, "register_session_notebook_scope"),
    (workbench, "register_health_check"),
    (serve_wire, "register_doxbench_validators"),
    (doxbench_packet, "register_status_exemption"),
    (doxbench_trust, "register"),
    (corpus_adapter, "register_home"),
)

#: Which of the two pinned shapes this run composes, read off the LEG: T011
#: took `LaneRoutes` off `DashboardHandler`'s bases in the same phase-1 commit
#: that carries the five seams.
LEG_HAS_THE_SEAMS = LANE_ROUTES not in serve_mod.DashboardHandler.__mro__


def _lane_methods() -> tuple[str, ...]:
    return tuple(sorted(name for name in vars(LANE_ROUTES)
                        if not (name.startswith("__") and name.endswith("__"))))


def _run(program: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-c", textwrap.dedent(program).format(scripts=str(SCRIPTS))],
        capture_output=True, text=True, cwd=str(REPO_ROOT))


# --------------------------------------------------------------------------
# 0. the pinned leg is one of the two shapes this file knows
# --------------------------------------------------------------------------

def test_the_pinned_leg_is_one_of_the_two_shapes():
    """The seams and T011's handler arrive in one phase-1 commit, so a leg has
    all of them or none. A leg with some of each is a pin between those
    landings, which `register_seams()` refuses too, and every two-shape test
    below would be asserting the wrong half."""
    declared = [f"{module.__name__}.{call}" for module, call in SEAM_CALLS
                if callable(getattr(module, call, None))]
    if LEG_HAS_THE_SEAMS:
        assert len(declared) == len(SEAM_CALLS), (
            f"LaneRoutes is off DashboardHandler's bases, so the leg carries "
            f"plan 034 T011, yet it declares only {declared} of the six seams")
    else:
        assert declared == [], (
            f"LaneRoutes is still a base of DashboardHandler, so the leg "
            f"predates plan 034 T011, yet it declares {declared}")


# --------------------------------------------------------------------------
# 1. T045: the lanes column, through the handler-contribution facet
# --------------------------------------------------------------------------

def test_the_profile_declares_the_lanes_column_under_the_handler_facet():
    """R1Q1 (a): the host names its own mixin. Forwarded by the composite, not
    copied into it, like every facet `opendox_host.FACETS` lists."""
    assert "HANDLER_CONTRIBUTIONS" in opendox_host.FACETS
    assert profile_openxfactory.HANDLER_CONTRIBUTIONS == (LANE_ROUTES,)
    assert type(profile_openxfactory.HANDLER_CONTRIBUTIONS) is tuple, (
        "openDox refuses a facet that is not a plain tuple of classes")
    assert proxy.HANDLER_CONTRIBUTIONS is profile_openxfactory.HANDLER_CONTRIBUTIONS
    assert opendox_host.profile().HANDLER_CONTRIBUTIONS is (
        profile_openxfactory.HANDLER_CONTRIBUTIONS)


def test_no_route_extension_declares_a_second_copy_of_the_column():
    """openDox refuses a mixin declared twice, so each column is declared in
    ONE place. The lanes column is this host's, declared by the profile and by
    no extension. From plan 034's T086 openXdox's two columns are declared by
    openXdox's own route extensions (RULED Q2 (a) at T086), and the profile
    names neither of them."""
    declared = [mixin for extension in profile_openxfactory.ROUTE_EXTENSIONS
                for mixin in (getattr(extension, "HANDLER_CONTRIBUTIONS", None)
                              or ())]
    assert LANE_ROUTES not in declared, (
        "a route extension declares LaneRoutes as well as the profile")
    assert sorted(declared, key=lambda c: c.__name__) == sorted(
        CONTRIBUTED_COLUMNS[1:], key=lambda c: c.__name__), declared
    assert len(declared) == len(set(declared)), declared
    for column in CONTRIBUTED_COLUMNS[1:]:
        assert column not in profile_openxfactory.HANDLER_CONTRIBUTIONS, (
            f"the profile declares openXdox's {column.__name__} as well as "
            "its route extension")


def test_the_lanes_column_arrives_where_the_pinned_leg_binds_it():
    """Before T011 the column is a base of openDox's `DashboardHandler`. From
    T011 on it is composed in at build time, by the SAME `route_extension`
    module `opendox.serve` builds with, after the core handler, and every one
    of its six methods resolves to the column's own function.

    Read through `serve_mod.route_extension`, the module the server really
    uses. `route_extension` is a top-level module with three copies in this
    composition: the openDox leg's, openXdox-code's `src/route_extension.py`
    and openxFactory's `scripts/route_extension.py`. `carved_reach.install()`
    puts `openXdox/code/src` first, so the first copy found need not be the
    leg's. A copy that predates the facet fails here, naming its file, rather
    than at the first `build_server`."""
    methods = _lane_methods()
    assert len(methods) == 6, methods
    if not LEG_HAS_THE_SEAMS:
        assert LANE_ROUTES in serve_mod.DashboardHandler.__mro__
        for name in methods:
            assert getattr(serve_mod.DashboardHandler, name) is vars(LANE_ROUTES)[name]
        return

    seam = serve_mod.route_extension
    assert hasattr(seam, "collect_handler_contributions"), (
        f"opendox.serve builds with {seam.__file__}, which has no "
        "handler-contribution facet, while the pinned openDox leg's "
        "DashboardHandler no longer carries LaneRoutes, so the lanes routes "
        "cannot be bound. That copy of route_extension predates openDox-code "
        "T010 and is found ahead of the leg's own on sys.path.")
    contributed = seam.collect_handler_contributions(
        (proxy, *profile_openxfactory.ROUTE_EXTENSIONS),
        base=serve_mod.DashboardHandler)
    assert contributed == CONTRIBUTED_COLUMNS, contributed
    bound = seam.compose_handler("BoundDashboardHandler",
                                 serve_mod.DashboardHandler, contributed, {})
    assert bound.__mro__ == ((bound,) + serve_mod.DashboardHandler.__mro__[:-1]
                             + CONTRIBUTED_COLUMNS + (object,))
    for name in methods:
        assert name not in vars(serve_mod.DashboardHandler)
        assert getattr(bound, name) is vars(LANE_ROUTES)[name], name


#: The dashboard fixture tree the ideation-dashboard suite serves, and the
#: revision it stamps (`tests/ideation-dashboard/conftest.py`).
BASE_REPO = REPO_ROOT / "tests" / "ideation-dashboard" / "fixtures" / "base-repo"
PINNED_REVISION = "abcd1234" * 5


class _FakeGit:
    def head_sha(self, repo) -> str:
        return PINNED_REVISION

    def commit_date(self, repo, revision: str) -> str:
        return "2026-07-12T00:00:00+00:00"


@contextmanager
def _serving(tmp_path):
    """A real server over the fixture tree, built through the registered
    profile, as `tests/ideation-dashboard/test_serve_column_split.py` builds
    one. The asset root is read off its manifest row, never spelled."""
    import carved_reach
    from openxdox.generator import generate_snapshot

    web = carved_reach.source("scripts/ideation_dashboard/web/index.html").parent
    snap = tmp_path / "snapshot.json"
    snap.write_text(json.dumps(generate_snapshot(
        BASE_REPO, "fixture-repo", source_revision=PINNED_REVISION,
        git=_FakeGit())), encoding="utf-8")
    httpd = serve_mod.build_server(web, snap, BASE_REPO, head=PINNED_REVISION,
                                   actor="brett")
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield httpd.server_address[:2]
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def _request(host, port, method: str, path: str):
    conn = http.client.HTTPConnection(host, port, timeout=5)
    try:
        conn.request(method, path, body=b"" if method == "POST" else None)
        resp = conn.getresponse()
        raw = resp.read()
    finally:
        conn.close()
    return resp.status, json.loads(raw.decode("utf-8") or "null")


def test_the_five_lane_routes_are_served_by_the_columns_own_methods(
        tmp_path, monkeypatch):
    """T045's falsifier, "the five lane routes are served", at the wire.

    A request to each of the column's five routes, on a real server built
    through the registered profile, reaches the column's own method, whichever
    way the pinned leg composes the column. Each method is replaced, for this
    test only, by a probe that answers with its own name, so the four write
    routes run no refresh and no seed: what each route does keeps its own
    suites, which run unmodified. The read route is also served for real,
    below."""
    bindings = tuple(serve_openxfactory_lanes.LaneRoutesExtension().routes())
    assert len(bindings) == 5, bindings
    assert all(binding.handler in vars(LANE_ROUTES) for binding in bindings)

    reached: list[str] = []

    def probe(name: str):
        def handler(self, *args):
            reached.append(name)
            payload = json.dumps({"served_by": name}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        return handler

    for binding in bindings:
        monkeypatch.setattr(LANE_ROUTES, binding.handler, probe(binding.handler))
    with _serving(tmp_path) as (host, port):
        answers = [_request(host, port, binding.method, binding.pattern)
                   for binding in bindings]
    assert answers == [(200, {"served_by": binding.handler})
                       for binding in bindings]
    assert reached == [binding.handler for binding in bindings]


def test_the_lanes_read_route_answers_from_a_real_server(tmp_path):
    """The read route with the column's real method: the committed-intent
    feed, as `test_intent_plane_boundary.py` reads it."""
    with _serving(tmp_path) as (host, port):
        status, body = _request(host, port, "GET",
                                serve_openxfactory_lanes.COMMITTED_INTENTS_ROUTE)
    assert status == 200, body
    assert body["kind"] == "committed-intent-feed", body


# --------------------------------------------------------------------------
# 2. T046: the host asserts its own registration (R1Q4 (a))
# --------------------------------------------------------------------------

def test_the_registered_profile_is_this_hosts_own():
    assert opendox_registry.current() is opendox_host.profile()
    assert opendox_host.register_openxfactory() is opendox_host.profile()


def test_the_host_refuses_when_the_registry_answers_another_profile():
    """The assertion is real: a registry that accepted the composite and then
    answered something else is refused, and no seam is written. In a
    SUBPROCESS, because the registry is process-wide."""
    proc = _run("""
        import sys
        sys.path.insert(0, {scripts!r})
        import carved_reach
        carved_reach.install()
        import opendox_host
        from opendox import domain_profile as odp
        stranger = object()
        odp.current = lambda: stranger
        try:
            opendox_host.register_openxfactory()
        except opendox_host.HostProfileNotRegistered as exc:
            print("REFUSED", "R1Q4 (a)" in str(exc))
        else:
            print("NO REFUSAL")
        from opendox import corpus_adapter
        if hasattr(corpus_adapter, "home"):
            try:
                corpus_adapter.home()
            except corpus_adapter.CorpusRefused:
                print("NO SEAM WRITTEN")
            else:
                print("A SEAM WAS WRITTEN")
        else:
            print("NO SEAM WRITTEN")
    """)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.split() == ["REFUSED", "True", "NO", "SEAM", "WRITTEN"], proc.stdout


def test_the_host_replaces_the_default_until_something_is_built_from_it():
    """R1Q3 (ii), with the host's side of it: registering over openDox's own
    default before any build replaces it, and registering after a build from
    it is refused with `AlreadyRegistered`, which the host does not swallow.
    In a SUBPROCESS, because the registry is process-wide."""
    proc = _run("""
        import sys
        sys.path.insert(0, {scripts!r})
        import carved_reach
        carved_reach.install()
        import opendox_host
        from opendox import domain_profile as odp
        if not hasattr(odp, "register_default"):
            print("LEG HAS NO DEFAULT")
            raise SystemExit(0)
        from opendox import default_profile
        odp.register_default(default_profile)
        opendox_host.register_openxfactory()
        print("REPLACED", odp.current() is opendox_host.profile())
        odp.unregister()
        odp.register_default(default_profile)
        odp.current_for_build()
        try:
            opendox_host.register_openxfactory()
        except odp.AlreadyRegistered:
            print("REFUSED AFTER A BUILD")
        else:
            print("NO REFUSAL")
    """)
    assert proc.returncode == 0, proc.stderr
    if LEG_HAS_THE_SEAMS:
        assert proc.stdout.splitlines() == ["REPLACED True", "REFUSED AFTER A BUILD"], proc.stdout
    else:
        assert proc.stdout.splitlines() == ["LEG HAS NO DEFAULT"], proc.stdout


# --------------------------------------------------------------------------
# 3. T046: every seam holds this host's implementation
# --------------------------------------------------------------------------

def test_every_seam_the_leg_declares_holds_this_hosts_implementation():
    """Identity through each seam's own public refusal: re-registering this
    host's object is a no-op, and a different object is refused, so the one
    registered is this host's. Nothing below writes a seam."""
    if not LEG_HAS_THE_SEAMS:
        assert opendox_host.register_seams() == ()
        return
    assert corpus_adapter.home() is opendox_host.home_corpus
    assert workbench.session_notebook_scope() == opendox_host.SESSION_NOTEBOOK_SCOPE
    assert workbench.health_check_registered()
    assert serve_wire.doxbench_validators_registered()
    assert doxbench_packet.status_exemption_registered()
    assert doxbench_trust.current() is opendox_host.binding_trust_policy()

    with pytest.raises(workbench.WorkbenchError):
        workbench.register_session_notebook_scope(corpus_adapter.SCOPE_ALL)
    with pytest.raises(workbench.WorkbenchError):
        workbench.register_health_check(lambda *args, **kwargs: None)
    with pytest.raises(serve_wire.DoxbenchValidatorsAlreadyRegistered):
        serve_wire.register_doxbench_validators(lambda: {})
    other_rail = types.SimpleNamespace(lifecycle_status=lambda text: None,
                                       is_compression_exempt=lambda text: False)
    with pytest.raises(doxbench_packet.StatusExemptionAlreadyRegistered):
        doxbench_packet.register_status_exemption(other_rail)
    with pytest.raises(doxbench_trust.TrustPolicyAlreadyRegistered):
        doxbench_trust.register(doxbench_trust.MachineTrust())

    assert opendox_host.register_seams() == tuple(
        f"{module.__name__}.{call}" for module, call in SEAM_CALLS)
    assert corpus_adapter.home() is opendox_host.home_corpus


def test_the_seams_are_filled_only_for_this_hosts_profile():
    """Copilot, PR #1181: `register_seams()` asserts R1Q4 (a) itself, before
    it writes anything, so reaching it without `register_openxfactory()`
    fills no seam: not with no profile registered, and not with another
    profile answering. In a SUBPROCESS, because the registries are
    process-wide."""
    proc = _run("""
        import sys
        sys.path.insert(0, {scripts!r})
        import carved_reach
        carved_reach.install()
        import opendox_host
        from opendox import corpus_adapter, workbench
        from opendox import domain_profile as odp
        def written():
            if not hasattr(workbench, "register_health_check"):
                return "leg has no seams"
            return (workbench.session_notebook_scope(),
                    workbench.health_check_registered())
        for case in ("none", "another"):
            if case == "another":
                stranger = object()
                odp.current = lambda: stranger
            try:
                opendox_host.register_seams()
            except opendox_host.HostProfileNotRegistered as exc:
                print(case, "REFUSED", "R1Q4 (a)" in str(exc), written())
            else:
                print(case, "NO REFUSAL")
    """)
    assert proc.returncode == 0, proc.stderr
    empty = "('all', False)" if LEG_HAS_THE_SEAMS else "leg has no seams"
    assert proc.stdout.splitlines() == [
        f"none REFUSED True {empty}", f"another REFUSED True {empty}"], proc.stdout


def test_a_leg_with_only_some_seams_is_refused_naming_the_missing(monkeypatch):
    """ALL OR NONE (`register_seams()`'s docstring). A leg that carries some of
    the five and not the others is refused before any seam is written."""
    written = []
    present = types.SimpleNamespace(__name__="present",
                                    register_home=written.append)
    absent = types.SimpleNamespace(__name__="absent")
    monkeypatch.setattr(opendox_host, "seams", lambda: (
        (present, "register_home", "the factory"),
        (absent, "register_health_check", "the check"),
    ))
    with pytest.raises(opendox_host.HostSeamsIncomplete) as excinfo:
        opendox_host.register_seams()
    assert "absent.register_health_check" in str(excinfo.value)
    assert written == []


def test_a_leg_with_no_seams_registers_nothing(monkeypatch):
    monkeypatch.setattr(opendox_host, "seams", lambda: (
        (types.SimpleNamespace(__name__="bare"), "register_home", "the factory"),
    ))
    assert opendox_host.register_seams() == ()


def test_the_seam_table_is_the_six_calls_in_their_registration_order():
    table = opendox_host.seams()
    assert [(module, call) for module, call, _ in table] == list(SEAM_CALLS)
    assert [value for _, _, value in table] == [
        opendox_host.SESSION_NOTEBOOK_SCOPE,
        opendox_host.scoped_doc_health,
        opendox_host.doxbench_validators,
        doxbench_status_exemption,
        opendox_host.binding_trust_policy(),
        opendox_host.home_corpus,
    ]


def test_every_seam_but_the_last_can_be_taken_back():
    """A refusal takes back what the call wrote, through each seam's own
    public calls, so every seam before the last has them. The last is the home
    seam, which openDox gives no call that empties it, and which refuses
    nothing callable, so nothing can refuse after it is written."""
    calls = [call for _, call in SEAM_CALLS]
    assert calls[-1] == "register_home"
    assert sorted(opendox_host._TAKE_BACK) == sorted(calls[:-1])
    if not LEG_HAS_THE_SEAMS:
        return
    for module, call in SEAM_CALLS[:-1]:
        query, empty = opendox_host._TAKE_BACK[call]
        for name in filter(None, (query, empty)):
            assert callable(getattr(module, name, None)), f"{module.__name__}.{name}"
    assert workbench.session_notebook_scope() != workbench.DEFAULT_SESSION_NOTEBOOK_SCOPE, (
        "the host's scope reads as registered through the query the "
        "take-back uses")


def test_the_host_replaces_opendoxs_own_default_home():
    """Copilot, PR #1181: the home seam refuses nothing callable, so what its
    overwrite can meet is openDox's OWN default, which an entry point
    registers through `register_default_home()` only where nothing answers
    `home()`. The host replaces it, as it replaces openDox's default profile
    before anything is built from it (R1Q3 (ii)). In a SUBPROCESS, because
    the seams are process-wide."""
    proc = _run("""
        import sys
        sys.path.insert(0, {scripts!r})
        import carved_reach
        carved_reach.install()
        import opendox_host
        from opendox import corpus_adapter
        if not hasattr(corpus_adapter, "register_default_home"):
            print("LEG HAS NO SEAMS")
            raise SystemExit(0)
        def opendox_default(root):
            raise AssertionError("never called: a registration is unevaluated")
        corpus_adapter.register_default_home(opendox_default)
        print("default", corpus_adapter.home() is opendox_default)
        opendox_host.register_openxfactory()
        print("replaced", corpus_adapter.home() is opendox_host.home_corpus)
    """)
    assert proc.returncode == 0, proc.stderr
    if LEG_HAS_THE_SEAMS:
        assert proc.stdout.splitlines() == [
            "default True", "replaced True"], proc.stdout
    else:
        assert proc.stdout.splitlines() == ["LEG HAS NO SEAMS"], proc.stdout


def test_another_hosts_home_is_never_reached_by_the_overwrite():
    """Copilot, PR #1181: a home another host registered cannot meet this
    host's overwrite. That host registered its own profile first, and a
    profile that is not this host's composite is refused before any seam is
    written, by `register()` and again by `register_seams()` itself (R1Q4
    (a)), so the other host's home is still the one `home()` answers. In a
    SUBPROCESS, because the registries are process-wide."""
    proc = _run("""
        import sys
        sys.path.insert(0, {scripts!r})
        import carved_reach
        carved_reach.install()
        import opendox_host
        from opendox import corpus_adapter
        from opendox import domain_profile as odp
        if not hasattr(corpus_adapter, "register_home"):
            print("LEG HAS NO SEAMS")
            raise SystemExit(0)
        def other_home(root):
            raise AssertionError("never called: a registration is unevaluated")
        odp.register(object())                    # another host's profile,
        corpus_adapter.register_home(other_home)  # and then its home
        try:
            opendox_host.register_openxfactory()
        except odp.AlreadyRegistered:
            print("register REFUSED")
        else:
            print("register NO REFUSAL")
        try:
            opendox_host.register_seams()
        except opendox_host.HostProfileNotRegistered:
            print("seams REFUSED")
        else:
            print("seams NO REFUSAL")
        print("home kept", corpus_adapter.home() is other_home)
    """)
    assert proc.returncode == 0, proc.stderr
    if LEG_HAS_THE_SEAMS:
        assert proc.stdout.splitlines() == [
            "register REFUSED", "seams REFUSED", "home kept True"], proc.stdout
    else:
        assert proc.stdout.splitlines() == ["LEG HAS NO SEAMS"], proc.stdout


class _FakeSeams:
    """Four seams in the shapes openDox's own take, plus a home seam with no
    call that empties it: the same object again is a no-op, a different one
    is refused, and each has the public query and emptying calls the host's
    take-back reads."""

    class Refused(Exception):
        pass

    def __init__(self, **held):
        self.state = {"scope": None, "check": None, "validators": None,
                      "rail": None, "home": None, **held}
        self.workbench = types.SimpleNamespace(
            __name__="fake_workbench", DEFAULT_SESSION_NOTEBOOK_SCOPE="all",
            register_session_notebook_scope=self._register("scope"),
            session_notebook_scope=lambda: self.state["scope"] or "all",
            unregister_session_notebook_scope=self._empty("scope"),
            register_health_check=self._register("check"),
            health_check_registered=lambda: self.state["check"] is not None,
            unregister_health_check=self._empty("check"))
        self.serve_wire = types.SimpleNamespace(
            __name__="fake_serve_wire",
            register_doxbench_validators=self._register("validators"),
            doxbench_validators_registered=lambda: self.state["validators"] is not None,
            unregister_doxbench_validators=self._empty("validators"))
        self.packet = types.SimpleNamespace(
            __name__="fake_packet",
            register_status_exemption=self._register("rail"),
            status_exemption_registered=lambda: self.state["rail"] is not None,
            unregister_status_exemption=self._empty("rail"))
        self.corpus = types.SimpleNamespace(
            __name__="fake_corpus_adapter",
            register_home=lambda factory: self.state.update(home=factory))

    def _register(self, key):
        def register(value):
            if self.state[key] is not None and self.state[key] != value:
                raise self.Refused(key)
            self.state[key] = value
        return register

    def _empty(self, key):
        return lambda: self.state.update({key: None})

    def table(self, scope="documents"):
        return (
            (self.workbench, "register_session_notebook_scope", scope),
            (self.workbench, "register_health_check", "host check"),
            (self.serve_wire, "register_doxbench_validators", "host validators"),
            (self.packet, "register_status_exemption", "host rail"),
            (self.corpus, "register_home", "host home"),
        )


def test_a_refused_seam_leaves_none_of_this_calls_writes_behind(monkeypatch):
    """Copilot, PR #1181: the seams are registered one by one, so a seam that
    refuses must not leave the ones before it written. Here the validators
    seam already holds another host's factory."""
    fake = _FakeSeams(validators="another host's validators")
    monkeypatch.setattr(opendox_host, "seams", fake.table)
    with pytest.raises(_FakeSeams.Refused):
        opendox_host.register_seams()
    assert fake.state == {"scope": None, "check": None,
                          "validators": "another host's validators",
                          "rail": None, "home": None}


@pytest.mark.parametrize("seam, dropped", [
    ("workbench", "unregister_session_notebook_scope"),
    ("workbench", "health_check_registered"),
    ("serve_wire", "unregister_doxbench_validators"),
    ("packet", "status_exemption_registered"),
])
def test_a_seam_without_its_take_back_calls_is_refused_before_any_write(
        monkeypatch, seam, dropped):
    """Copilot, PR #1181: a leg that carries every registration and not one
    of the calls that take a registration back is refused before anything is
    written. Otherwise a refusal later in the call would reach a take-back
    that raises `AttributeError`, masking the refusal and leaving the earlier
    seams written. The leg's own calls are held to the same table by
    `test_every_seam_but_the_last_can_be_taken_back`."""
    fake = _FakeSeams()
    module = getattr(fake, seam)
    delattr(module, dropped)
    monkeypatch.setattr(opendox_host, "seams", fake.table)
    with pytest.raises(opendox_host.HostSeamsIncomplete) as excinfo:
        opendox_host.register_seams()
    assert f"{module.__name__}.{dropped}" in str(excinfo.value)
    assert fake.state == {"scope": None, "check": None, "validators": None,
                          "rail": None, "home": None}


def test_a_refusal_keeps_what_this_host_had_already_registered(monkeypatch):
    """An idempotent second call writes nothing where the seam already holds
    this host's object, so a refusal later in that call empties nothing the
    first call registered."""
    fake = _FakeSeams(scope="documents", check="host check",
                      rail="another host's rail")
    monkeypatch.setattr(opendox_host, "seams", fake.table)
    with pytest.raises(_FakeSeams.Refused):
        opendox_host.register_seams()
    assert fake.state == {"scope": "documents", "check": "host check",
                          "validators": None, "rail": "another host's rail",
                          "home": None}


def test_a_default_scope_registered_before_this_call_is_not_taken_back(
        monkeypatch):
    """Copilot, PR #1181: `session_notebook_scope()` answers the default both
    when nothing is registered and when the default name was registered
    explicitly. A table that registers the default name therefore cannot tell
    whether its registration wrote anything, and a refusal later in the call
    leaves the scope as it found it rather than emptying a registration made
    before the call."""
    fake = _FakeSeams(scope="all", validators="another host's validators")
    monkeypatch.setattr(opendox_host, "seams", lambda: fake.table(scope="all"))
    with pytest.raises(_FakeSeams.Refused):
        opendox_host.register_seams()
    assert fake.state["scope"] == "all"
    assert fake.state["check"] is None


def test_the_hosts_own_scope_is_never_the_ambiguous_one():
    """The one state the scope's public query cannot tell apart matters only
    for the default name, and this host registers another."""
    assert opendox_host.SESSION_NOTEBOOK_SCOPE != corpus_adapter.SCOPE_ALL
    if LEG_HAS_THE_SEAMS:
        assert (opendox_host.SESSION_NOTEBOOK_SCOPE
                != workbench.DEFAULT_SESSION_NOTEBOOK_SCOPE)


def test_a_refused_seam_on_the_pinned_leg_takes_the_others_back():
    """The same on the leg's own seams, in a SUBPROCESS, because they are
    process-wide."""
    proc = _run("""
        import sys
        sys.path.insert(0, {scripts!r})
        import carved_reach
        carved_reach.install()
        import opendox_host
        from opendox import corpus_adapter, doxbench_packet, serve_wire, workbench
        from opendox import domain_profile as odp
        odp.register(opendox_host.profile())   # the profile alone, no seam
        if not hasattr(serve_wire, "register_doxbench_validators"):
            print("LEG HAS NO SEAMS", opendox_host.register_seams())
            raise SystemExit(0)
        other = lambda: {{}}
        serve_wire.register_doxbench_validators(other)
        try:
            opendox_host.register_seams()
        except serve_wire.DoxbenchValidatorsAlreadyRegistered:
            print("REFUSED")
        print("scope", workbench.session_notebook_scope())
        print("check", workbench.health_check_registered())
        print("rail", doxbench_packet.status_exemption_registered())
        try:
            corpus_adapter.home()
        except corpus_adapter.CorpusRefused:
            print("home empty")
        serve_wire.unregister_doxbench_validators()
        print("after", opendox_host.register_seams()[-1])
    """)
    assert proc.returncode == 0, proc.stderr
    if LEG_HAS_THE_SEAMS:
        assert proc.stdout.splitlines() == [
            "REFUSED", "scope all", "check False", "rail False", "home empty",
            "after opendox.corpus_adapter.register_home"], proc.stdout
    else:
        assert proc.stdout.splitlines() == ["LEG HAS NO SEAMS ()"], proc.stdout


def test_registering_imports_neither_factorys_package():
    """The two factories import their package ON THE CALL, as the reaches they
    replace did. `corpus_adapter_openxfactory` puts the pinned `openDox/code/
    src` at the head of `sys.path` when it is imported, so importing it at
    process start would change which copy of `route_extension` every later
    import finds. In a SUBPROCESS, so the imports measured are this call's."""
    proc = _run("""
        import sys
        sys.path.insert(0, {scripts!r})
        import carved_reach
        carved_reach.install()
        head = list(sys.path)
        import opendox_host
        opendox_host.register_openxfactory()
        print("adapter", "corpus_adapter_openxfactory" in sys.modules)
        print("contracts", "ideation_dashboard.doxbench_contracts" in sys.modules)
        print("route_extension", "route_extension" in sys.modules)
        print("path_unchanged", sys.path == head)
    """)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.split() == [
        "adapter", "False", "contracts", "False",
        "route_extension", "False", "path_unchanged", "True"], proc.stdout


# --------------------------------------------------------------------------
# 4. T046: what a hosted request gets is unchanged
# --------------------------------------------------------------------------

def test_the_scope_the_host_registers_is_one_its_corpus_declares():
    adapter, ref = adapter_home_corpus(REPO_ROOT)
    scopes = adapter.resolve(ref).scopes
    assert opendox_host.SESSION_NOTEBOOK_SCOPE in scopes, scopes
    assert opendox_host.SESSION_NOTEBOOK_SCOPE != corpus_adapter.SCOPE_ALL


def test_the_home_factory_builds_a_fresh_adapter_over_the_root_it_is_given(tmp_path):
    first, first_ref = opendox_host.home_corpus(str(tmp_path))
    second, _ = opendox_host.home_corpus(str(tmp_path))
    assert first is not second, (
        "the adapter caches listings for as long as it lives, so a shared one "
        "would give a session notebook re-sync a stale listing")
    assert first_ref.location == str(tmp_path)
    assert first_ref.name == tmp_path.name


def test_the_hosted_session_notebook_is_unchanged():
    """T046's falsifier (R1Q9 (a)). The notebook's source set, by document and
    by bytes, is what the rule it replaces gave: `doc_health`'s governed roots
    plus a declared `Status:` header, each document within the size cap.

    Compared as a mapping, because the projection sorts by path before it
    syncs (`workbench._sync_sources`), so the order of the list is not part of
    what a notebook receives. Before T047's pin, `session_documents` IS that
    rule; from it on, the rule is the registered adapter's `documents` scope."""
    listed = workbench.session_documents(REPO_ROOT)
    keys = [key for key, _ in listed]
    assert len(keys) == len(set(keys)), "a document is listed twice"
    expected = {doc.path: doc.text
                for doc in dh_corpus.load_docs(REPO_ROOT.name, REPO_ROOT)
                if doc.status and len(doc.text.encode("utf-8"))
                <= workbench._MAX_SESSION_SOURCE_BYTES}
    assert len(expected) > 100, "the rule selected almost nothing to compare"
    got = dict(listed)
    assert sorted(set(got) ^ set(expected)) == []
    assert got == expected


_BAD_STATUS = "# Bad status\n\nStatus: not-a-lifecycle-word\n\nBody.\n"
_GOOD_STATUS = "# Good status\n\nStatus: brainstorm\n\nBody.\n"


def _old_scoped_run(root: Path, documents, families):
    """The in-process run `run_scoped_doc_health` made before openDox-code
    #39, restated as the oracle: this test's own copy, so the host's
    `scoped_doc_health` is compared with it rather than with itself."""
    from doc_health import DEFAULT_THRESHOLDS
    from doc_health.runner import Context, run_suite

    wanted = set(documents)
    docs = [d for d in dh_corpus.load_docs(root.name, root) if d.path in wanted]
    ctx = Context(repo_paths={root.name: root}, docs=docs, capabilities={},
                  change_ids={}, git=dh_corpus.RealGit(),
                  thresholds=dict(DEFAULT_THRESHOLDS), as_of=date(2026, 9, 27),
                  agg_root=None)
    findings = []
    for family in families:
        findings.extend(run_suite(ctx, family, set()).findings)
    return [f for f in findings if f.path in wanted], len(docs)


def test_a_scoped_health_run_answers_what_the_in_process_run_answered(tmp_path):
    (tmp_path / "ideation" / "brainstorm").mkdir(parents=True)
    (tmp_path / "ideation" / "brainstorm" / "bad.md").write_text(_BAD_STATUS)
    (tmp_path / "ideation" / "brainstorm" / "good.md").write_text(_GOOD_STATUS)
    documents = ["ideation/brainstorm/bad.md", "ideation/brainstorm/good.md"]
    families = workbench.DEFAULT_SCOPED_FAMILIES

    result = workbench.run_scoped_doc_health(
        tmp_path, documents, as_of=date(2026, 9, 27))
    findings, checked = _old_scoped_run(tmp_path.resolve(), documents, families)

    assert findings, "the oracle found nothing, so the comparison is vacuous"
    assert result.status == "completed", result.detail
    assert list(result.findings) == findings
    assert result.detail == (
        f"{len(findings)} finding(s) over {checked} scoped doc(s) "
        f"(families: {', '.join(families)})")


def test_a_scoped_health_run_refuses_a_family_doc_health_does_not_carry(tmp_path):
    with pytest.raises(workbench.WorkbenchError) as excinfo:
        workbench.run_scoped_doc_health(tmp_path, [], families=("no-such-family",))
    assert "no-such-family" in str(excinfo.value)


def test_the_doxbench_validators_are_the_contract_pins_own():
    """Before the seam `default_doxbench_validators()` called
    `doxbench_contracts.validators()`; through it, the host's factory does."""
    assert sorted(serve_wire.default_doxbench_validators()) == sorted(
        doxbench_contracts.validators())


#: The rail's seven names that the packet module answers, as
#: `tests/ideation-dashboard/test_doxbench_status_exemption.py` spells them
#: (`CARVED_NAMES`).
RAIL_NAMES = (
    "_STATUS_RE", "STATUS_SCAN_LINES", "EXEMPT_STATUSES", "_STATUS_DECORATORS",
    "lifecycle_status", "status_word", "is_compression_exempt",
)


def test_the_packet_module_answers_the_rails_own_names():
    """The seven names the packet module answers are the rail module's own
    objects, as `tests/ideation-dashboard/test_doxbench_status_exemption.py`
    reads them: before the seam because the packet module imports them, and
    through it because the host registers the module itself."""
    for name in RAIL_NAMES:
        assert getattr(doxbench_packet, name) is getattr(doxbench_status_exemption, name), name
