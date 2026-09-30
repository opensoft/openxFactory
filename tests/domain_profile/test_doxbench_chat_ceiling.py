"""The doxBench chat's browser ceiling is pinned to the RELEASED `maxLength`:
a composition test moved here under R1Q2 (a), on F11.1's `HOST_TESTS`
surface.

MOVED HERE by plan 034 T035 (opensoft/openDox-code#51, landed `80acead1`).
The case left `tests/test_doxbench_chat_view.py` at openDox-code `68be484a`
(`:4148-4166`), where it FAILED: it read
`contracts/schemas/xfactory-workbench-chat-turn.schema.yaml` from the leg's own
tree, and the carve sent that released schema to openDox-SPEC
(`moved_verbatim` -> `opendox_spec`), which openDox-code does not compose.
openxFactory mounts both of openDox's legs, so here the case reads each file
where the carve placed it, through `carved_reach.source` and each file's own
manifest row: the schema at the pinned `openDox/spec`, and
`doxbench-chat-model.js` at the pinned `openDox/code`.

The case's body is #51's source, verbatim, except for the one path that named
the leg's own tree. openDox-code kept the other side of the triangle: its
`test_the_browser_ceiling_equals_the_servers_ceiling` holds the browser's
constant to the server's, and the server's to the released 500.

WHY `tests/domain_profile/`, AND NOT THE PROPOSED `tests/ideation-dashboard/`
PATH. `tests/ideation-dashboard/` is inside the carve surface
(`docs/opendox-carve-manifest.yaml` `moved_paths:`), where
`scripts/validate-carve-manifest.py` refuses a NEW file that no row declares
(`carve-file-undeclared`), and F11.1 forbids adding the row. This directory is
outside that surface, and it is F11.1's own `HOST_TESTS` prefix. The root
`tests/conftest.py` installs the reach and makes the host's one call here too,
so a case that composes the pinned legs composes the same ones it would have
composed there.
"""

from __future__ import annotations

from carved_reach import source as carved_source

CHAT_MODEL_JS = carved_source(
    "scripts/ideation_dashboard/web/views/doxbench-chat-model.js")
CHAT_TURN_SCHEMA = carved_source(
    "contracts/schemas/xfactory-workbench-chat-turn.schema.yaml")


def test_the_browser_ceiling_is_pinned_to_the_RELEASED_maxLength():
    """The JS constant cannot read the schema, so it is pinned to the released
    bytes here — the same discipline `serve.CONTEXT_REDUCED_REASON_MAX_LENGTH`
    gets. Three restatements of one bound, and a test for each pair, so they
    cannot drift into three ceilings."""
    import re
    import yaml

    schema = yaml.safe_load(CHAT_TURN_SCHEMA.read_text(encoding="utf-8"))
    released = schema["$defs"]["context_packet"]["properties"][
        "reduced_reason"]["maxLength"]
    source = CHAT_MODEL_JS.read_text(encoding="utf-8")
    match = re.search(
        r"export const CONTEXT_REDUCED_REASON_MAX_LENGTH = (\d+);", source)
    assert match, "the browser-side ceiling constant moved or was renamed"
    assert int(match.group(1)) == released
