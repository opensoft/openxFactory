"""The outline surface and openxFactory's doc_health family agree on the
contract: a composition test moved here under R1Q2 (a), on F11.1's
`HOST_TESTS` surface.

MOVED HERE by plan 034 T034 (opensoft/openDox-code#50, landed `71b631bc`).
The case left `tests/test_outline_model.py` at openDox-code `19370adc`, where
it could not stay: it holds `views/outline-model.js`'s `REQUIRED_SECTIONS` and
`QUESTION_SUBFIELDS` equal to `doc_health.families` (`_TEMPLATE_SECTIONS`,
`_QUESTION_SUBFIELDS`), and `doc_health` is openxFactory's, which openDox can
never install. openDox has no checker of its own until Group 6 (release 2), so
there is no openDox contract to rewrite it against.

It composes the two here: the checker is this repository's own
`scripts/doc_health/families.py`, and the model is the pinned openDox leg's
copy of `outline-model.js`, read through `carved_reach.source` from the
file's manifest row. The case's body is #50's, verbatim; only `MODEL_JS` names
the pinned leg's file instead of the leg's own tree.

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

from pathlib import Path

from carved_reach import source as carved_source

REPO_ROOT = Path(__file__).resolve().parents[2]

MODEL_JS = carved_source("scripts/ideation_dashboard/web/views/outline-model.js")


def test_the_model_and_the_doc_health_family_agree_on_the_contract():
    """The surface and the checker must mean the same thing by conformance."""
    import sys
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from doc_health import families

    js = MODEL_JS.read_text(encoding="utf-8")
    for _needle, label in families._TEMPLATE_SECTIONS:
        assert f'label: "{label}"' in js, f"model omits required section {label}"
    for field in families._QUESTION_SUBFIELDS:
        assert f'"{field}"' in js, f"model omits sub-field {field}"
