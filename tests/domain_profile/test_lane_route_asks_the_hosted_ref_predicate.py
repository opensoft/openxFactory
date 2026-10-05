"""The lanes column's refresh route asks the hosted-ref predicate (plan 034 T094).

WHERE THIS CHECK CAME FROM. openXdox-code's
`tests/test_session_snapshot.py::test_the_hosted_session_arrival_path_is_recorded_and_not_built`
asked every serve route that accepts a ref, `_handle_refresh_action` among
them, whether it calls `hosted_ref_refused(`. `_handle_refresh_action` is
openxFactory's lanes column (`scripts/ideation_dashboard/serve_openxfactory_lanes.py`,
a `stays_openxfactory_adapter` row, RULING DQ-1), so it never arrived at that
leg, and at T086 (opensoft/openXdox-code#37, Q8 (a)) the loop was narrowed to
the leg's own two routes. The property moves here, to the lane's owner, instead
of disappearing: FR-048, "a hosted request naming a non-`main` ref MUST
refuse", on the one write-ish route the hosted plane reaches (the read-only
`refetch` binding is offered there by design).

It is asserted twice: on the route's own body, as the leg's test asked it, and
by driving the route on a hosted plane with a ref the predicate refuses, so a
call that is present but no longer decides the answer fails too.
"""

from __future__ import annotations

import inspect

from ideation_dashboard import serve_openxfactory_lanes as lanes  # noqa: E402
from openxdox import snapshot_registry as registry_mod  # noqa: E402
from wire_messages import HOSTED_SESSION_REFUSAL  # noqa: E402

#: A ref the hosted plane may not see: not `main`, so not publishable.
SESSION_REF = "session/t094-hosted-ref-probe"


class _Probe:
    """The attributes `_handle_refresh_action` reads, and nothing else: a
    hosted plane (not loopback) offering the read-only `refetch` binding,
    whose source is present, and a body naming `SESSION_REF`."""

    loopback = False
    capabilities = {"refresh": {"binding": registry_mod.BINDING_REFETCH}}
    source = object()

    def __init__(self, body: dict) -> None:
        self._body = body
        self.sent: list[tuple[int, dict]] = []
        self.refreshed: list[tuple[object, object]] = []

    def _read_json_body(self):
        return self._body

    def _send_json(self, status: int, payload: dict) -> None:
        self.sent.append((status, payload))

    def _run_refresh(self, repository, ref) -> None:
        self.refreshed.append((repository, ref))


def test_the_refresh_route_body_asks_the_predicate():
    body = inspect.getsource(lanes.LaneRoutes._handle_refresh_action)
    assert "hosted_ref_refused(" in body, (
        "_handle_refresh_action does not ask the predicate")
    # and the name it asks is openXdox's predicate, the one the module imports
    assert lanes.hosted_ref_refused.__module__ == "openxdox.serve_projection"


def test_a_hosted_refresh_naming_a_session_ref_is_refused_before_it_runs():
    # the premise, read off the predicate itself: the ref is refused when
    # hosted and untouched on loopback
    assert lanes.hosted_ref_refused(False, SESSION_REF) is True
    assert lanes.hosted_ref_refused(True, SESSION_REF) is False

    probe = _Probe({"ref": SESSION_REF})
    lanes.LaneRoutes._handle_refresh_action(probe)
    assert probe.refreshed == []
    assert probe.sent == [(403, {"ok": False, "error": "session_unavailable",
                                 "message": HOSTED_SESSION_REFUSAL})]

    # and the refusal is the predicate's: a ref-less refresh on the same
    # hosted plane runs
    probe = _Probe({})
    lanes.LaneRoutes._handle_refresh_action(probe)
    assert probe.sent == []
    assert probe.refreshed == [(None, None)]
