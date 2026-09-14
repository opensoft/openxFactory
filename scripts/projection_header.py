#!/usr/bin/env python3
"""THE single source of truth for the ideation cross-reference projection's
`Status:` header (openxFactory #793).

`ideation/cross-reference.md` is a GENERATED projection over the
source-of-truth `ideation/cross-reference.yaml` — rewritten in place from the
YAML on every run, so it has no captured state to be immutable against. It
therefore carries `Status: projection` and never `Status: record`, per
`docs/document-lifecycle.md` and per `declare-generated-projection-status`
(2026-08-28, commit `fc788825`, which changed that very line).

TWO code paths produce that file's content, and each used to declare the status
independently:

* `scripts/render-ideation-cross-reference.py::render_markdown` — the
  standalone renderer, which wrote the literal itself; and
* `scripts/doc_health/ideation_readiness.py::_render_markdown` — the write path
  every nightly/packet run actually takes (reused by
  `doc_health/derive_possibles.py::persist`), which does not render at all: it
  delegates to WHICHEVER copy of the standalone renderer the `OPENXFACTORY_ROOT`
  env var or the ancestor walk happens to resolve. A consuming repository whose
  `.openxfactory-pin/` predates `fc788825` therefore still emitted
  `Status: record` while a direct invocation in openxFactory's own tree emitted
  `Status: projection`.

openxFactory #785 hit exactly that disagreement and worked around it by
re-rendering the landed `.md` with the standalone renderer by hand. The value
now lives HERE, once, and both paths emit it from this module: the renderer
appends `STATUS_LINE`, and the delegating path stamps `STATUS_LINE` onto
whatever the resolved renderer returned. Neither path can emit another value,
whichever snapshot of the renderer is reachable.

Placed beside `scripts/output_boundary.py` — in NEITHER package — for the same
reason that one is: `doc_health` must not import from `ideation_dashboard`
(`tests/doc-health/test_import_direction.py`), and `persist()` already reaches
this directory for its output boundary, so nothing new has to travel alongside
the vendored module for the stamp to work.
"""
from __future__ import annotations

#: The lifecycle status every generated ideation cross-reference projection
#: carries. NOT `record`: see the module docstring.
PROJECTION_STATUS = "projection"

#: The header line itself — what both generators emit, character for character.
STATUS_LINE = f"Status: {PROJECTION_STATUS}"

_STATUS_PREFIX = "Status:"

#: How far into the document a `Status:` line is still a HEADER line. The
#: projection's header block is five lines; anything further down belongs to the
#: rendered body (cluster sections, member tables) and is not ours to rewrite.
_HEADER_SCAN_LINES = 12


def apply_status_line(markdown):
    """Return `markdown` with its header `Status:` line set to `STATUS_LINE`.

    The DELEGATING path calls this, because it cannot vouch for the vintage of
    the renderer copy its lookup resolved. A stale renderer's `Status: record`
    is rewritten to the canonical line; output that already carries the
    canonical line is returned unchanged, byte for byte; output with no header
    status line at all has one inserted after the title rather than landing
    headerless. `None` (the renderer was unreachable and the `.md` write is
    skipped) passes straight through.
    """
    if markdown is None:
        return None
    lines = markdown.split("\n")
    for i, line in enumerate(lines[:_HEADER_SCAN_LINES]):
        if line.startswith(_STATUS_PREFIX):
            if line == STATUS_LINE:
                return markdown
            lines[i] = STATUS_LINE
            return "\n".join(lines)
    # No header status line at all. Seat one directly under the title block
    # when there is one, otherwise at the top, each followed by the blank line
    # the header block expects.
    if len(lines) > 1 and lines[0].startswith("# ") and lines[1] == "":
        lines.insert(2, STATUS_LINE)
    else:
        lines.insert(0, "")
        lines.insert(0, STATUS_LINE)
    stamped = "\n".join(lines)
    # An insertion at the very end of a one-line document would otherwise eat
    # the trailing newline the input had.
    if markdown.endswith("\n") and not stamped.endswith("\n"):
        stamped += "\n"
    return stamped
