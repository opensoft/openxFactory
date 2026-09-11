"""The ROUTE EXTENSION POINT (`split-opendox-two-layer-product` § 2.4, PR 1 of
4), tested where it matters: over a REAL ephemeral `ThreadingHTTPServer` built
by `build_server`, with a contributed route dispatched against the LIVE request
handler.

WHAT THE SEAM PROMISES, and therefore what is asserted here:

  1. **A contributed route reaches the same gating as a core one.** The binding
     names a METHOD, and the dispatch is `getattr(self, name)` on the live
     handler — so a contributed write route consults `self.loopback` and answers
     the same refusal a core gate verb answers, and this file proves that by
     asking BOTH off-loopback and comparing the two answers. This is the
     analogue of `corpus-adapter-seam` requirement 4's "no privileged route",
     which `tests/corpus-adapter/test_no_privileged_route.py` keeps over the
     home corpus.
  2. **Nothing else moved.** A path no binding claims still falls through to the
     static handler on a read and to `ERR_UNKNOWN_ACTION` on a write, and a
     server built with no extensions has an empty table. The wider "zero
     behaviour change" proof — the golden help text and the pinned core
     dispatch table — is `test_extension_point_parity.py`.
  3. **A route that cannot be served does not start.** A binding naming a method
     the handler does not have refuses the BUILD, rather than becoming a stack
     trace on a live connection.
  4. **The interface is neutral and closed.** It imports neither package (an
     AST scan, over `tests/import_scan.py`), and it has exactly one member.

WHY THE PROBE HANDLERS ARE INSTALLED ON `DashboardHandler` ITSELF. Because that
is where a contributed handler will actually live: the extraction PRs that
follow move methods onto the handler and declare bindings for them. A test that
attached a callable to the binding instead would be testing a shape the seam
deliberately does not have — the very side door that would let a contributed
route skip the gating. `monkeypatch.setattr` installs them for one test and
removes them after, so the handler class this suite shares is never left with a
probe on it.
"""

from __future__ import annotations

import http.client
import json
import sys
import threading
from contextlib import contextmanager

import pytest

from conftest import (BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit,
                      dashboard_web_root)

sys.path.insert(0, str(REPO_ROOT / "tests"))

import route_extension  # noqa: E402
from import_scan import imported_modules, names_a_forbidden_package  # noqa: E402

from opendox import action_errors  # noqa: E402
# The composition point, at its POST-SHED home. `scripts/
# ideation_dashboard/profile_openxfactory.py` is the carve manifest's one
# `deleted_at_carve` row and the shed removed it; openxFactory's profile now
# lives at `scripts/profile_openxfactory.py` (plain top-level spelling) and is
# registered with `opendox.serve`/`opendox.cli` by
# `carved_reach.bind_composition_point()` from the conftest — the openxFactory
# half of RULED ASK-2 option (2) (`#656` comment `5628886636`).
import profile_openxfactory  # noqa: E402
from opendox import serve as serve_mod  # noqa: E402
from openxdox.generator import generate_snapshot  # noqa: E402

# The dashboard's asset root, DERIVED from `web/index.html`'s manifest row
# (§ 5.2, RULED (a), `#656` `5625573095`). The assets moved to openDox-code
# with the serve and `dashboard_web_root()` reads where from the row rather
# than spelling the destination here; its docstring records the one
# `not_moved` asset — openxFactory's own intent-feed view — and why a merged
# asset root is § 4.3 composition work rather than this constant's job.
WEB = dashboard_web_root()
MODULE = REPO_ROOT / "scripts" / "route_extension.py"

#: The probe handler names. Deliberately not `_handle_*`: nothing about the seam
#: depends on a naming convention, and a probe that borrowed the core prefix
#: would make the parity scans in `test_extension_point_parity.py` harder to read.
PROBE_READ = "_probe_read"
PROBE_READ_PREFIX = "_probe_read_prefix"
PROBE_WRITE = "_probe_write"
PROBE_WRITE_PREFIX = "_probe_write_prefix"

READ_ROUTE = "/probe.json"
READ_PREFIX = "/probe-read/"
WRITE_ROUTE = "/actions/probe"
WRITE_PREFIX = "/actions/probe-prefix/"


class ProbeExtension:
    """A conforming extension. Structural, and it imports nothing from the
    server — which is the point of a Protocol rather than a base class."""

    def __init__(self, bindings):
        self._bindings = tuple(bindings)

    def routes(self):
        return self._bindings


class NotAnExtension:
    """Conforms to nothing. Named for what it is, so the refusal reads."""


def _probe_read(self, head_only):
    """A contributed READ route, exact form: `handler(head_only)`.

    Reports state only the LIVE handler has — the bound snapshot route, the
    resolved actor, the loopback verdict and this request's own path — so a
    passing assertion proves dispatch against the real instance and not against
    some stripped stand-in.
    """
    payload = {"probe": "read", "path": self.path,
               "snapshot_route": self.snapshot_route,
               "actor": self.actor, "loopback": self.loopback}
    self._serve_bytes(json.dumps(payload).encode("utf-8"),
                      serve_mod.JSON_CTYPE, head_only)


def _probe_read_prefix(self, remainder, head_only):
    """A contributed READ route, prefix form: `handler(remainder, head_only)`."""
    self._serve_bytes(
        json.dumps({"probe": "read-prefix", "remainder": remainder}).encode("utf-8"),
        serve_mod.JSON_CTYPE, head_only)


def _probe_write(self):
    """A contributed WRITE route, exact form: `handler()`.

    Its first clause is the one every core write route opens with, spelled the
    same way, because it is reaching the same attribute on the same object.
    """
    if not self.loopback:
        self._send_json(403, {"ok": False, "error": "loopback_only",
                              "message": "probe actions are loopback-only"})
        return
    self._send_json(200, {"ok": True, "probe": "write", "actor": self.actor})


def _probe_write_prefix(self, remainder):
    """A contributed WRITE route, prefix form: `handler(remainder)`."""
    if not self.loopback:
        self._send_json(403, {"ok": False, "error": "loopback_only",
                              "message": "probe actions are loopback-only"})
        return
    self._send_json(200, {"ok": True, "probe": "write-prefix",
                          "remainder": remainder})


PROBE_METHODS = {
    PROBE_READ: _probe_read,
    PROBE_READ_PREFIX: _probe_read_prefix,
    PROBE_WRITE: _probe_write,
    PROBE_WRITE_PREFIX: _probe_write_prefix,
}

PROBE_BINDINGS = (
    route_extension.RouteBinding("GET", READ_ROUTE, False, PROBE_READ),
    route_extension.RouteBinding("GET", READ_PREFIX, True, PROBE_READ_PREFIX),
    route_extension.RouteBinding("POST", WRITE_ROUTE, False, PROBE_WRITE),
    route_extension.RouteBinding("POST", WRITE_PREFIX, True, PROBE_WRITE_PREFIX),
)


@pytest.fixture
def probes(monkeypatch):
    """Install the probe methods on the handler class for ONE test."""
    for name, func in PROBE_METHODS.items():
        monkeypatch.setattr(serve_mod.DashboardHandler, name, func, raising=False)
    return ProbeExtension(PROBE_BINDINGS)


@contextmanager
def serving(tmp_path, *, route_extensions=(), actor="brett"):
    snap = tmp_path / "snapshot.json"
    snap.write_text(json.dumps(generate_snapshot(
        BASE_REPO, "fixture-repo", source_revision=PINNED_REVISION,
        git=FakeGit())), encoding="utf-8")
    httpd = serve_mod.build_server(WEB, snap, BASE_REPO, head=PINNED_REVISION,
                                   actor=actor,
                                   route_extensions=route_extensions)
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
    """The bound `DashboardHandler` subclass, unwrapped from the partial —
    the same unwrap `test_doxbench_routes.py` uses."""
    return getattr(httpd.RequestHandlerClass, "func", httpd.RequestHandlerClass)


def request(host, port, method, path, *, body=None, headers=None):
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request(method, path,
                 body=None if body is None else json.dumps(body),
                 headers=headers or {})
    resp = conn.getresponse()
    raw = resp.read()
    try:
        payload = json.loads(raw.decode("utf-8") or "{}")
    except ValueError:
        payload = None
    conn.close()
    return resp.status, payload, raw


# ---------------------------------------------------------------------------
# 1. neutrality — a property of imports, not of where the file sits
# ---------------------------------------------------------------------------

#: Both spellings of both packages. `scripts/__init__.py` exists, so every
#: package under `scripts/` is importable as a top-level name AND as
#: `scripts.<name>`; a one-spelling list is a hole, for the reason
#: `tests/import_scan.py` states in its own header.
FORBIDDEN = ("ideation_dashboard", "scripts.ideation_dashboard",
             "doc_health", "scripts.doc_health")


def test_the_extension_point_imports_neither_package():
    """It travels to openDox with the carve, where the checker package does not
    exist — so an import of either side would make it un-carveable, and would
    put the cycle the seam was drawn to remove back one level down. PARSED, not
    grepped: this module NAMES both packages in prose, deliberately."""
    offenders = [f"{MODULE.name}:{line} imports {module!r}"
                 for module, line in imported_modules(MODULE)
                 if names_a_forbidden_package(module, FORBIDDEN)]
    assert offenders == [], (
        "the route extension point must import NEITHER reader package: it is "
        "consumed by both sides of the carve and it travels with the carve. "
        f"Offending imports: {offenders}")


def test_the_extension_point_imports_only_the_standard_library():
    """Stronger than the scan above and the actual rule `corpus_adapter.py`
    states: stdlib and `typing` only. A third-party import would travel to a
    repository that has no such dependency declared."""
    third_party = [f"{module} (line {line})"
                   for module, line in imported_modules(MODULE)
                   if module.split(".")[0] not in sys.stdlib_module_names]
    assert third_party == [], (
        f"the extension point imports non-stdlib modules: {third_party}")


def test_the_neutrality_scan_would_catch_the_import_it_is_meant_to_catch(tmp_path):
    """The negative control, because the two scans above prove an ABSENCE."""
    scratch = tmp_path / "would_be_offender.py"
    scratch.write_text(
        "from ideation_dashboard import serve\n"
        "import scripts.doc_health.corpus\n"
        "from typing import Protocol\n", encoding="utf-8")
    caught = [m for m, _ in imported_modules(scratch)
              if names_a_forbidden_package(m, FORBIDDEN)]
    assert caught == ["ideation_dashboard", "scripts.doc_health.corpus"], caught


# ---------------------------------------------------------------------------
# 2. closure — one member, and it is a method
# ---------------------------------------------------------------------------


def test_the_protocol_is_closed_at_its_declared_members():
    """`MEMBERS` and `__protocol_attrs__` are one set, so growing the surface is
    a two-file act somebody has to mean — `WorkbenchModelPort`'s pattern."""
    assert set(route_extension.RouteExtension.__protocol_attrs__) == \
        set(route_extension.MEMBERS)


def test_every_member_is_a_method_so_both_checks_work():
    """A `runtime_checkable` Protocol with a non-method member keeps
    `isinstance` and loses `issubclass`. Pinned rather than trusted: a
    `@property` added later would take it away from every consumer silently."""
    assert isinstance(ProbeExtension(()), route_extension.RouteExtension)
    assert issubclass(ProbeExtension, route_extension.RouteExtension)
    assert not isinstance(NotAnExtension(), route_extension.RouteExtension)


# ---------------------------------------------------------------------------
# 3. the binding refuses what it cannot serve, where it is declared
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("kwargs,because", [
    (dict(method="PUT", pattern="/x", is_prefix=False, handler="h"),
     "a method the dispatch has no arm for"),
    (dict(method="GET", pattern="x", is_prefix=False, handler="h"),
     "a pattern not rooted at /"),
    (dict(method="GET", pattern="/x?y=1", is_prefix=False, handler="h"),
     "a pattern carrying a query the dispatcher has already stripped"),
    (dict(method="GET", pattern="/x#f", is_prefix=False, handler="h"),
     "a pattern carrying a fragment"),
    (dict(method="GET", pattern="/x", is_prefix=True, handler="h"),
     "a prefix that does not end at a segment boundary"),
    (dict(method="GET", pattern="/x", is_prefix=False, handler="not an identifier"),
     "a handler name that is not a name"),
    (dict(method="GET", pattern="/x", is_prefix=False, handler="__init__"),
     "a dunder, which reaches the object protocol and not the server"),
    (dict(method="GET", pattern="/x", is_prefix=False, handler=""),
     "an empty handler name"),
])
def test_a_malformed_binding_is_refused_where_it_is_declared(kwargs, because):
    with pytest.raises(route_extension.RouteBindingError):
        route_extension.RouteBinding(**kwargs)


def test_a_well_formed_binding_is_accepted():
    """The positive control: the refusals above must not be refusing everything."""
    binding = route_extension.RouteBinding("POST", "/actions/x/", True, "_h")
    assert binding.key == ("POST", "/actions/x/", True)
    assert binding.remainder("/actions/x/y/z") == "y/z"
    assert route_extension.RouteBinding("GET", "/x", False, "_h").remainder("/x") == ""


# ---------------------------------------------------------------------------
# 4. collection: one consult order, exact before prefix, no collisions
# ---------------------------------------------------------------------------


def test_exact_bindings_are_consulted_before_prefix_bindings():
    """Across independent extensions the tuple order is an accident of whatever
    assembled it, so the collection groups every exact binding ahead of every
    prefix one.

    REPOINTED ONTO A LEGAL PAIR BY RULING A (2026-09-07). This test used to
    build the SAME-method pair — a GET prefix `/a/` and a GET exact `/a/exact`
    — which `collect_bindings` now REFUSES outright, because the exact route
    would take that path out of the prefix's gating
    (`test_a_pattern_under_a_declared_prefix_refuses_the_build`). The pair here
    is the legal one that still exercises the grouping: a GET exact under a
    POST prefix, which is not a collision because nothing answers a live POST
    but a POST binding. Same assertion, same strength — the ORDER of the
    returned tuple, which is this module's declared contract and what
    `test_serve_column_split.py`'s nine-binding pin reads — and it now also
    pins that the containment refusal is METHOD-AWARE rather than fired on
    patterns alone.
    """
    broad = ProbeExtension((
        route_extension.RouteBinding("POST", "/a/", True, "_wide"),))
    narrow = ProbeExtension((
        route_extension.RouteBinding("GET", "/a/exact", False, "_narrow"),))
    bindings = route_extension.collect_bindings((broad, narrow))
    assert [b.handler for b in bindings] == ["_narrow", "_wide"]
    matched = route_extension.match(bindings, "GET", "/a/exact")
    assert matched is not None and matched[0].handler == "_narrow"
    assert route_extension.match(bindings, "POST", "/a/exact")[0].handler == "_wide"
    assert route_extension.match(bindings, "POST", "/a/other")[0].handler == "_wide"


def test_two_bindings_claiming_one_route_refuse_the_build():
    """The second could never be reached, and a route that looks declared and
    never fires is worse than one that refuses."""
    first = ProbeExtension((
        route_extension.RouteBinding("GET", "/a", False, "_one"),))
    second = ProbeExtension((
        route_extension.RouteBinding("GET", "/a", False, "_two"),))
    with pytest.raises(route_extension.RouteBindingError) as err:
        route_extension.collect_bindings((first, second))
    assert "_one" in str(err.value) and "_two" in str(err.value)


@pytest.mark.parametrize("first_method,second_method", [
    ("GET", "HEAD"),
    ("HEAD", "GET"),
])
def test_a_get_and_a_head_binding_for_the_same_route_refuse_the_build(
        first_method, second_method):
    """A "GET" binding already answers a HEAD request (the module docstring,
    and `RouteBinding.matches`), so a "HEAD" binding at the same (pattern,
    is_prefix) could never be reached on the one request method it exists to
    answer — the same unreachable-route defect two identical keys are refused
    for, just reached through the request method the second binding never
    receives. Parametrized over declaration order because the collision must
    be caught either way, not only when the "GET" binding is declared first.

    The message must name EACH binding by ITS OWN declared method — not the
    collision-check key that happened to match, which used to misreport a
    HEAD binding's collision as "two route bindings claim GET" (Copilot
    review `PRRT_kwDOTAvnrs6fwTVh`): asserting `first_method`/`second_method`
    each appear beside their own binding's pattern would fail on that bug,
    since a HEAD binding's own method never appeared in the old message at
    all.
    """
    first = ProbeExtension((
        route_extension.RouteBinding(first_method, "/a", False, "_first"),))
    second = ProbeExtension((
        route_extension.RouteBinding(second_method, "/a", False, "_second"),))
    with pytest.raises(route_extension.RouteBindingError) as err:
        route_extension.collect_bindings((first, second))
    message = str(err.value)
    assert "_first" in message and "_second" in message
    assert f"{first_method} {'/a'!r}" in message
    assert f"{second_method} {'/a'!r}" in message


def test_a_get_and_a_head_binding_for_DIFFERENT_routes_do_not_collide():
    """The positive control: the GET/HEAD collision check must not over-fire
    on two bindings that do not actually share a (pattern, is_prefix)."""
    get_a = ProbeExtension((
        route_extension.RouteBinding("GET", "/a", False, "_get_a"),))
    head_b = ProbeExtension((
        route_extension.RouteBinding("HEAD", "/b", False, "_head_b"),))
    bindings = route_extension.collect_bindings((get_a, head_b))
    assert {b.handler for b in bindings} == {"_get_a", "_head_b"}


#: `(outer, inner)` — the PREFIX binding and the binding that sits under it,
#: each as `RouteBinding` arguments. Every pair is exercised in BOTH
#: declaration orders by the test below.
OVERLAPPING_PAIRS = (
    # the ruling's own case: the gate console's prefix, and an exact verb path
    # under it — the hijack `r3`'s live probe demonstrated at this PR's head
    (("POST", "/actions/gate/", True, "_gate"),
     ("POST", "/actions/gate/ratify", False, "_hijack")),
    # GET/HEAD share one slot, so the containment is cross-method too
    (("GET", "/source/", True, "_serve"),
     ("HEAD", "/source/x.md", False, "_hijack")),
    # NESTED PREFIXES, refused on the same rule (fail closed — the in-tree
    # profile declares no nested pair; see the module docstring)
    (("GET", "/a/", True, "_outer"),
     ("GET", "/a/b/", True, "_inner")),
    # a pattern EQUAL to a prefix but declared EXACT does sit under it:
    # `"/a/".startswith("/a/")` is True and the exact one wins the match
    (("GET", "/a/", True, "_outer"),
     ("GET", "/a/", False, "_inner")),
)


@pytest.mark.parametrize("outer,inner", OVERLAPPING_PAIRS)
@pytest.mark.parametrize("prefix_first", [True, False])
def test_a_pattern_under_a_declared_prefix_refuses_the_build(
        outer, inner, prefix_first):
    """RULING A (Brett Heap, 2026-09-07), over Copilot review
    `PRRT_kwDOTAvnrs6f_iG1` on PR #761.

    Ordering exact ahead of prefix decides a tie; it does not make the tie
    SAFE. A prefix is where a column puts the gating its whole subtree shares
    — `ACTIONS_GATE_PREFIX` carries the gate console's loopback, capability,
    actor and human-console refusals — so an exact binding declared under one
    wins the match and takes that single path out of the prefix's hands, and
    the prefix's handler never runs for it. `collect_bindings` refuses it with
    the same `RouteBindingError` a literal duplicate raises.

    Parametrized over DECLARATION ORDER because a refusal that only fired when
    the prefix happened to be declared first would be no refusal at all across
    independent extensions, whose tuple order is an accident; over GET/HEAD
    because that pair shares one slot; and over two nested prefixes because
    those are refused on the same rule.

    The message must name BOTH bindings by their OWN declared method and
    pattern — the discipline `_collision_message` already keeps, so a reader
    who gets this error can see which two declarations to change without
    reading the module — and must name the prefix AS a prefix, since which of
    the two is the container is the whole content of the complaint.
    """
    outer_ext = ProbeExtension((route_extension.RouteBinding(*outer),))
    inner_ext = ProbeExtension((route_extension.RouteBinding(*inner),))
    declared = (outer_ext, inner_ext) if prefix_first else (inner_ext, outer_ext)
    with pytest.raises(route_extension.RouteBindingError) as err:
        route_extension.collect_bindings(declared)
    message = str(err.value)
    assert outer[3] in message and inner[3] in message
    assert f"{inner[0]} {inner[1]!r}" in message
    assert f"{outer[0]} prefix {outer[1]!r}" in message


@pytest.mark.parametrize("prefix_method,exact_method", [
    ("POST", "GET"),
    ("POST", "HEAD"),
    ("GET", "POST"),
])
def test_an_exact_binding_under_a_prefix_of_ANOTHER_METHOD_does_not_collide(
        prefix_method, exact_method):
    """The positive control on the ruling's method-awareness: containment is
    refused only where one live request could be offered to BOTH bindings.

    Nothing answers a live POST but a "POST" binding, so a GET (or HEAD) exact
    route under a POST prefix is two independent routes that never contend —
    and a refusal that fired here would make the seam unusable for the
    commonest legitimate shape, a read route living inside a write prefix's
    path space.
    """
    wide = ProbeExtension((
        route_extension.RouteBinding(prefix_method, "/a/", True, "_wide"),))
    narrow = ProbeExtension((
        route_extension.RouteBinding(exact_method, "/a/x", False, "_narrow"),))
    bindings = route_extension.collect_bindings((wide, narrow))
    assert {b.handler for b in bindings} == {"_wide", "_narrow"}


def test_an_exact_pattern_equal_to_a_prefix_minus_its_slash_does_not_collide():
    """The pair this assembly ACTUALLY declares must keep building.

    `"/source".startswith("/source/")` is False — the bare route does not sit
    inside the prefix and no request path reaches both — so the projection
    column's `/source` + `/source/` pair is legal, and the containment refusal
    reads "under" as exactly that `startswith` rather than as a segment-wise
    or "same stem" test that would have refused this assembly's own profile.
    Asserted twice: on the pair alone, and on the whole in-tree profile, whose
    nine bindings must still collect.
    """
    pair = ProbeExtension((
        route_extension.RouteBinding("GET", "/source", False, "_bare"),
        route_extension.RouteBinding("GET", "/source/", True, "_under"),))
    assert [b.handler for b in route_extension.collect_bindings((pair,))] == \
        ["_bare", "_under"]
    profile = route_extension.collect_bindings(
        profile_openxfactory.ROUTE_EXTENSIONS)
    assert len(profile) == 9, (
        "the in-tree profile no longer collects — RULING A's containment "
        "refusal must not fire on `/source` beside `/source/`")


def test_a_non_conforming_extension_is_refused():
    with pytest.raises(route_extension.RouteBindingError):
        route_extension.collect_bindings((NotAnExtension(),))


def test_an_extension_that_contributes_a_non_binding_is_refused():
    class Sloppy:
        def routes(self):
            return ("GET /a -> _h",)

    with pytest.raises(route_extension.RouteBindingError):
        route_extension.collect_bindings((Sloppy(),))


# ---------------------------------------------------------------------------
# 5. matching: a GET binding answers HEAD, exactly as every core read arm does
# ---------------------------------------------------------------------------


def test_a_get_binding_answers_head_and_a_head_binding_does_not_answer_get():
    get_only = route_extension.RouteBinding("GET", "/a", False, "_h")
    head_only = route_extension.RouteBinding("HEAD", "/b", False, "_h")
    post_only = route_extension.RouteBinding("POST", "/c", False, "_h")
    assert get_only.matches("GET", "/a") and get_only.matches("HEAD", "/a")
    assert head_only.matches("HEAD", "/b") and not head_only.matches("GET", "/b")
    assert post_only.matches("POST", "/c") and not post_only.matches("GET", "/c")
    assert not get_only.matches("POST", "/a")


def test_a_prefix_does_not_match_a_longer_sibling_name():
    """The reason a prefix must end at a segment boundary: without it
    "/sourceless" matches the "/source" prefix and the remainder is a fragment
    of another route's name."""
    binding = route_extension.RouteBinding("GET", "/source/", True, "_h")
    assert binding.matches("GET", "/source/a.md")
    assert not binding.matches("GET", "/sourceless")


def test_no_match_is_None_and_not_an_empty_tuple():
    """`match` returning a falsey-but-not-None value would make the dispatch
    clause's `is not None` read as a bug rather than as the rule."""
    assert route_extension.match((), "GET", "/anything") is None


# ---------------------------------------------------------------------------
# 6. wiring: a route that cannot be served does not start
# ---------------------------------------------------------------------------


def test_a_binding_naming_a_missing_handler_refuses_the_build(tmp_path):
    """At BUILD time, against the class the dispatch will `getattr` on —
    otherwise the typo is found as a stack trace on a live connection."""
    bogus = ProbeExtension((
        route_extension.RouteBinding("GET", "/nope.json", False,
                                     "_no_such_handler_exists"),))
    with pytest.raises(route_extension.RouteBindingError) as err:
        with serving(tmp_path, route_extensions=(bogus,)):
            pass
    assert "_no_such_handler_exists" in str(err.value)


def test_a_binding_naming_a_non_callable_attribute_refuses_the_build(tmp_path):
    """`hasattr` alone is not enough: `"loopback"` (and `"capabilities"`,
    `"route_bindings"`) are REAL attributes of `DashboardHandler` — a
    `bool`, a `dict`, a `tuple` — so a binding naming one of them used to pass
    `build_server` and only crash the first live request that reached it
    (`TypeError: 'bool' object is not callable`). It must now refuse at build
    time instead, with a message that names the attribute as non-callable
    rather than missing, so the two failure modes read differently."""
    non_callable = ProbeExtension((
        route_extension.RouteBinding("GET", "/loopback.json", False,
                                     "loopback"),))
    with pytest.raises(route_extension.RouteBindingError) as err:
        with serving(tmp_path, route_extensions=(non_callable,)):
            pass
    message = str(err.value)
    assert "loopback" in message
    assert "not callable" in message
    # and it must not be mistaken for the missing-handler case: nothing here
    # is actually MISSING, so that clause must not fire.
    assert "does not have" not in message


def test_resolve_handlers_refuses_a_non_callable_and_a_missing_handler_together():
    """Both defects can be named in one refusal, each with its own clause."""
    missing = route_extension.RouteBinding("GET", "/x", False,
                                           "_no_such_handler_exists")
    non_callable = route_extension.RouteBinding("GET", "/y", False,
                                                "route_bindings")
    with pytest.raises(route_extension.RouteBindingError) as err:
        route_extension.resolve_handlers((missing, non_callable),
                                         serve_mod.DashboardHandler)
    message = str(err.value)
    assert "_no_such_handler_exists" in message and "does not have" in message
    assert "route_bindings" in message and "not callable" in message


def test_resolve_handlers_accepts_a_class_or_an_instance():
    """`route_extension` knows nothing about the shape of the server it serves,
    so it asks the plain question `hasattr`/`callable` answers for both."""
    binding = route_extension.RouteBinding("GET", "/x", False, "routes")
    route_extension.resolve_handlers((binding,), ProbeExtension)
    route_extension.resolve_handlers((binding,), ProbeExtension(()))


def test_a_server_built_with_no_extensions_carries_exactly_the_in_tree_profile(
        tmp_path):
    """What a caller who adds nothing gets: this assembly's OWN routes, and
    nothing else.

    REPOINTED by § 2.4 PR 3 of 4, disclosed in that PR's body. When PR 1 landed
    the extension point, nothing was registered through it and the table was
    genuinely empty; PR 3 moved the gate, projection and lane routes into it, so
    `build_server` now composes `profile_openxfactory.ROUTE_EXTENSIONS` ahead of
    whatever the caller passes. The assertion is the same one at the same
    strength — the table a default build carries, named exactly — and it is
    strictly harder to satisfy than `== ()`: a stray binding added to the
    profile, a member dropped from it, or a caller's tuple leaking into a
    default build all fail here.
    """
    with serving(tmp_path) as (httpd, _host, _port):
        assert handler_class(httpd).route_bindings == \
            route_extension.collect_bindings(
                profile_openxfactory.ROUTE_EXTENSIONS)


def test_a_caller_s_extensions_are_added_to_the_profile_and_never_replace_it(
        tmp_path, probes):
    """The composition, stated as a property rather than left to the docstring.

    `route_extensions` is ADDITIVE: a caller that contributes routes still gets
    this assembly's own, and the caller's land after them. A future edit that
    made the keyword REPLACE the profile would leave every existing call site
    building a server with no `/snapshot-index.json`, no `/source/` and no gate
    verbs — silently, because those call sites pass nothing.
    """
    profile_bindings = route_extension.collect_bindings(
        profile_openxfactory.ROUTE_EXTENSIONS)
    with serving(tmp_path, route_extensions=(probes,)) as (httpd, _host, _port):
        got = handler_class(httpd).route_bindings
    assert set(profile_bindings) <= set(got)
    assert set(PROBE_BINDINGS) <= set(got)
    assert len(got) == len(profile_bindings) + len(PROBE_BINDINGS)


# ---------------------------------------------------------------------------
# 7. LIVE dispatch, over a real server
# ---------------------------------------------------------------------------


def test_a_contributed_read_route_is_dispatched_against_the_live_handler(
        tmp_path, probes):
    with serving(tmp_path, route_extensions=(probes,)) as (_httpd, host, port):
        status, payload, _raw = request(host, port, "GET", READ_ROUTE)
    assert status == 200
    assert payload["probe"] == "read"
    assert payload["path"] == READ_ROUTE
    # state only the BOUND handler carries: the injected actor, the loopback
    # verdict and the snapshot route this server was built with
    assert payload["actor"] == "brett"
    assert payload["loopback"] is True
    assert payload["snapshot_route"] == serve_mod.SNAPSHOT_ROUTE


def test_a_contributed_read_route_answers_head_with_no_body(tmp_path, probes):
    """A "GET" binding answers HEAD, and the SAME handler suppresses the body
    off the `head_only` flag — one dispatch, one body decision, exactly as
    every core read arm works."""
    with serving(tmp_path, route_extensions=(probes,)) as (_httpd, host, port):
        status, _payload, raw = request(host, port, "HEAD", READ_ROUTE)
    assert status == 200
    assert raw == b""


def test_a_contributed_prefix_read_route_receives_the_remainder(tmp_path, probes):
    with serving(tmp_path, route_extensions=(probes,)) as (_httpd, host, port):
        status, payload, _raw = request(
            host, port, "GET", READ_PREFIX + "nested/doc.md")
    assert (status, payload["probe"]) == (200, "read-prefix")
    assert payload["remainder"] == "nested/doc.md"


def test_a_contributed_write_route_is_dispatched(tmp_path, probes):
    with serving(tmp_path, route_extensions=(probes,)) as (_httpd, host, port):
        status, payload, _raw = request(host, port, "POST", WRITE_ROUTE, body={})
    assert (status, payload["ok"], payload["probe"]) == (200, True, "write")
    assert payload["actor"] == "brett"


def test_a_contributed_prefix_write_route_receives_the_remainder(tmp_path, probes):
    with serving(tmp_path, route_extensions=(probes,)) as (_httpd, host, port):
        status, payload, _raw = request(
            host, port, "POST", WRITE_PREFIX + "verb", body={})
    assert (status, payload["probe"], payload["remainder"]) == \
        (200, "write-prefix", "verb")


def test_a_contributed_write_route_refuses_off_loopback_exactly_like_a_core_one(
        tmp_path, probes):
    """THE POINT OF THE WHOLE SHAPE (`corpus-adapter-seam` requirement 4's
    analogue): the contributed route and a CORE gate verb are asked the same
    question off-loopback and give the same answer, because the by-name dispatch
    put them both in front of the same `self.loopback`.

    A binding that carried its own callable could have answered differently, and
    nothing in the server would have noticed. That is the door this shape does
    not have.

    THE CORE COMPARATOR IS `/actions/edit`, repointed by § 2.4 PR 3 of 4 and
    disclosed in that PR's body. It was `/actions/gate/ratify`, which PR 3 turned
    INTO a contributed route — leaving this test comparing contributed against
    contributed while its own docstring claimed contributed against CORE. That is
    a silent weakening: it stays green either way. `/actions/edit` is a fixed core
    arm of `do_POST` dispatching `serve_project.ProjectRoutes._handle_edit_action`,
    whose first clause is the same `if not self.loopback` refusal with the same
    `loopback_only` code, so the comparison is the one this test names.
    """
    with serving(tmp_path, route_extensions=(probes,)) as (httpd, host, port):
        handler_class(httpd).loopback = False
        contributed = request(host, port, "POST", WRITE_ROUTE, body={})
        contributed_prefix = request(host, port, "POST", WRITE_PREFIX + "v",
                                     body={})
        core = request(host, port, "POST", serve_mod.ACTIONS_EDIT_ROUTE,
                       body={})
    assert core[0] == 403 and core[1]["error"] == "loopback_only"
    assert contributed[0] == core[0]
    assert contributed[1]["error"] == core[1]["error"]
    assert contributed_prefix[0] == core[0]
    assert contributed_prefix[1]["error"] == core[1]["error"]


def test_an_unclaimed_read_path_still_falls_through_to_the_static_handler(
        tmp_path, probes):
    """The clause sits BEFORE the fallback, not instead of it."""
    with serving(tmp_path, route_extensions=(probes,)) as (_httpd, host, port):
        status, _payload, _raw = request(host, port, "GET",
                                         "/no-such-page-anywhere")
        served, _p, raw = request(host, port, "GET", "/index.html")
    assert status == 404
    # and the static bundle is still served, so the fallthrough is real
    assert served == 200 and raw


def test_an_unclaimed_write_path_still_answers_the_unknown_action_refusal(
        tmp_path, probes):
    with serving(tmp_path, route_extensions=(probes,)) as (_httpd, host, port):
        status, payload, _raw = request(host, port, "POST", "/actions/nonesuch",
                                        body={})
    expected_status, expected_message = \
        action_errors.ERROR_CATALOG[action_errors.ERR_UNKNOWN_ACTION]
    assert (status, payload) == (
        expected_status,
        {"error": action_errors.ERR_UNKNOWN_ACTION, "message": expected_message})


def test_a_contributed_route_cannot_shadow_a_core_route(tmp_path, probes):
    """The core arms run to completion first, so a binding that duplicates a
    core pattern is unreachable rather than overriding — which is the safe
    direction of that failure."""
    shadow = ProbeExtension((
        route_extension.RouteBinding("GET", serve_mod.SNAPSHOT_ROUTE, False,
                                     PROBE_READ),))
    with serving(tmp_path, route_extensions=(shadow,)) as (_httpd, host, port):
        status, payload, _raw = request(host, port, "GET",
                                        serve_mod.SNAPSHOT_ROUTE)
    assert status == 200
    assert "probe" not in payload, (
        "a contributed binding answered a CORE route — the extension clause has "
        "moved above the fixed arms, and every core route is now overridable")
    assert "generation" in payload   # the real snapshot, unchanged


@pytest.mark.parametrize("method,prefix,core_handler,probe", [
    ("POST", serve_mod.ACTIONS_GATE_PREFIX, "_handle_gate_action", PROBE_WRITE),
    ("GET", serve_mod.SOURCE_PREFIX, "_serve_source", PROBE_READ),
])
def test_an_exact_caller_binding_under_a_contributed_prefix_refuses_the_build(
        tmp_path, probes, method, prefix, core_handler, probe):
    """RULING A (Brett Heap, 2026-09-07), asserted where it actually bites: a
    real `build_server`.

    FLIPPED from `…_wins_the_match`, which pinned the gap this PR opened as a
    characterization. § 2.4 PR 3 moved the gate console and the projection
    routes off `serve.py`'s fixed tables, and while a hard-coded `if` could not
    be reached by a caller-supplied binding, a CONTRIBUTED prefix binding could
    — a caller who passes `route_extensions` could declare an exact binding
    under `ACTIONS_GATE_PREFIX` or `SOURCE_PREFIX`, the build accepted it, and
    it won the match, so `_handle_gate_action` (and its loopback, capability,
    actor and human-console refusals) never ran for that one path. That was
    demonstrated live at this branch's head — a probe binding answering
    `POST /actions/gate/<verb>` with its own 200.

    It is now impossible at BUILD: `collect_bindings` refuses the overlap
    before `build_server` opens a socket, reads a checkout or bootstraps a
    session, and the refusal names both the caller's binding and this
    assembly's own. Parametrized over the two security-sensitive prefixes the
    PR contributed, because the ruling is about the shape and not about the
    gate console alone.
    """
    verb_path = prefix + "fake-verb"
    override = ProbeExtension((
        route_extension.RouteBinding(method, verb_path, False, probe),))
    with pytest.raises(route_extension.RouteBindingError) as err:
        with serving(tmp_path, route_extensions=(override,)):
            pass          # never reached: the refusal precedes the socket
    message = str(err.value)
    assert f"{method} {verb_path!r}" in message
    assert f"{method} prefix {prefix!r}" in message
    assert probe in message and core_handler in message


def test_the_query_string_is_stripped_before_a_binding_is_matched(tmp_path, probes):
    """The dispatch matches the PATH, as every core arm does — so a contributed
    route keeps its own query handling and does not have to re-split."""
    with serving(tmp_path, route_extensions=(probes,)) as (_httpd, host, port):
        status, payload, _raw = request(host, port, "GET",
                                        READ_ROUTE + "?repository=x&ref=y")
    assert (status, payload["probe"]) == (200, "read")
    assert payload["path"] == READ_ROUTE + "?repository=x&ref=y"
