"""The FIXED WIRE STRINGS the dashboard serve puts on the wire verbatim — one
JSON content type and two fixed refusal messages — belonging to neither
package.

WHY THIS MODULE SITS AT THE TOP OF `scripts/` AND BELONGS TO NEITHER PACKAGE.
It joins `output_boundary.py` (`split-opendox-two-layer-product` § 2.1 / design
D2), the one neutral module in this tree, and it was created for the same
reason that one was: a seam cannot be drawn through an import that crosses it
in the forbidden direction. OQ-B B-1 creates a second, `path_slug.py`, for the
same reason again — it is NOT in this tree, it is in flight on its own PR
(#843), and this file does not depend on it either way. All three strings
lived in `ideation_dashboard/serve_wire.py` — the shared wire vocabulary, an
openDox module under design D3's three-column assignment — and
`ideation_dashboard/serve_openxfactory_lanes.py`, which is openxFactory's own
engineering adapter column and STAYS, imported them from there. RULING OQ-2
says openDox is pinned ONLY by openXdox and § 5.1 (RULING F) says openxFactory
pins the openXdox assembly root and nothing else, so an openxFactory to
openDox import is an edge the carve cannot tolerate. Ruled by Brett Heap on
2026-09-09 (`#656`, "rule B-2 (i')"): OQ-B re-plumbs every such edge BEFORE
the carve, and **the string half of B-2 is this file**.

WHY A STRING CAN COME HERE AND THE PREDICATE COULD NOT. These three names are
`str` literals: they carry no dependency at all, so they are neutral by
construction. B-2's fourth name, `hosted_ref_refused`, could not follow them —
its body reaches `snapshot_registry.is_publishable_ref`, and
`snapshot_registry` is the openXdox column, so a module replicated at every
destination could not resolve it and restating the ref rule here would be the
second spelling `serve_wire.py`'s own import comments exist to refuse. That
name went to `ideation_dashboard/serve_projection.py` instead, beside
`hosted_index` (the same ruling, option (i'); pre-carve split S-3's
precedent).

WHAT NEUTRAL MEANS HERE, AND HOW IT IS PROVEN. The module imports NOTHING from
`scripts/ideation_dashboard/` and nothing from `scripts/doc_health/`; it
imports nothing but `__future__` at all. That is the property, not an accident
of the current body, and it is asserted by PARSING the import statements
rather than by reading — `tests/ideation-dashboard/test_oqb_replumb_2.py`
mirrors, for this module, the instrument
`tests/doc-health/test_import_direction.py` keeps over `output_boundary.py`.

AT THE CARVE. `not_moved`, reason `replicated_at_destination` (RULED OQ-A and
OQ-C, 2026-09-09): a neutral module is replicated at every destination rather
than shared across a repository boundary with no pin, so openDox gets a
replica and this copy stays. It therefore has NO row of its own in the carve
manifest's moved set beyond that disposition.

CALLERS. `ideation_dashboard/serve_wire.py` re-exports all three below — the
SAME OBJECTS rather than copies (`ideation_dashboard/boundary.py`'s precedent)
— so `serve_wire.JSON_CTYPE` and its two siblings keep resolving for every
existing caller: `serve.py`, `serve_workbench.py`, `serve_project.py` and
`serve_gate.py` (openDox and openXdox readers, whose direction the carve
permits) and the suites that read them off `serve`. Only
`serve_openxfactory_lanes.py` — the openxFactory adapter column this file
exists for — imports from here directly.
"""

from __future__ import annotations


JSON_CTYPE = "application/json; charset=utf-8"
JSON_OBJECT_BODY_REQUIRED = "a JSON object body is required"

# The refusal message every hosted non-`main` request gets, verbatim. Fixed text:
# nothing request-derived reaches the wire (the response discipline `serve_wire`
# already keeps for the notebook action).
HOSTED_SESSION_REFUSAL = ("a ref other than 'main' is session-local data and is "
                          "not available on this plane")
