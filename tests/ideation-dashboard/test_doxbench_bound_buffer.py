"""THE F2 OBLIGATION, VERIFIED DISCHARGED (add-doxbench-editing-phase-b task
13.5; design D17).

Phase A tried to name a turn's bound buffer with a server-side-only
`PromptEnvelope.bound_buffer`, and its review killed that on two counts:

  1. UNREADABLE — nothing serialized, persisted or rendered it, so no reader
     could ever consult it, and "the record names the bound buffer" was a claim
     with no reader; and
  2. MIS-DERIVABLE — it was derived from `active_document_path`, so a human
     working the OUTLINE with a document loaded was recorded as bound to the
     document. The two fields answer different questions, and the derivation
     silently answered the wrong one.

Both failure modes are forbidden by the ratified delta, and §13's release is
what makes discharging them possible: the widened envelope carries the DECLARED
binding on the request and echoes it in the durable record. This module proves
the two NEGATIVES the way `doxbench_threads.py` proves its no-parallel-store
negative — against the source and the public surface, not against a description
of them — and pins the POSITIVE beside them, because a negative alone would pass
on a runtime that carried no binding at all.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from conftest import REPO_ROOT, serve_surface_paths, serve_surface_source
from ideation_dashboard import doxbench_contracts, doxbench_turns

RUNTIME = REPO_ROOT / "scripts" / "ideation_dashboard"
SERVE_PY = RUNTIME / "serve.py"
TURNS_PY = RUNTIME / "doxbench_turns.py"
CHAT_JS = RUNTIME / "web" / "views" / "doxbench-chat.js"
WORKBENCH_JS = RUNTIME / "web" / "views" / "staging-workbench.js"
SCHEMA = (REPO_ROOT / "contracts" / "schemas"
          / "xfactory-workbench-chat-turn.schema.yaml")


# ---------------------------------------------------------------------------
# NEGATIVE 1: no server-side-only bound-buffer field, anywhere
# ---------------------------------------------------------------------------

def test_the_prompt_envelope_carries_no_bound_buffer_field():
    """The killed field, asserted against the CLASS rather than its docstring.

    `build_prompt_envelope` still takes the declared binding -- it is a
    validation input, handed to `revalidate_scope` -- and still refuses a binding
    naming no supplied buffer. What it must never do is keep it as a claim on an
    object nothing serializes."""
    fields = set(doxbench_turns.PromptEnvelope.__dataclass_fields__)
    for name in fields:
        assert "bound" not in name, (
            f"PromptEnvelope.{name} reads as a bound-buffer claim; an internal "
            f"field no reader can consult cannot discharge the obligation to "
            f"NAME the bound buffer in a turn's durable record")
    # …and the positive half of the same fact: the binding is still CHECKED.
    parameters = doxbench_turns.build_prompt_envelope.__kwdefaults__
    assert "bound_buffer_key" in parameters


def test_no_runtime_module_stores_a_bound_buffer_on_the_envelope():
    """The same negative over the SOURCE, so a field added back under another
    spelling still trips it. The check is deliberately narrow -- it looks for an
    assignment of a binding onto the envelope, not for the words `bound_buffer`,
    which the validation input and the released wire field both legitimately
    use."""
    # EVERY FILE THE SERVE IS MADE OF, plus the turns module (§ 2.4 PR 2 of 4
    # moved the chat-turn route to `serve_workbench.py`). `serve.py` alone now
    # carries NO occurrence of `bound_buffer` at all, so a negative asserted
    # over it would have kept passing while asserting nothing about the code it
    # is named for. Widened, never narrowed: `serve.py` is still scanned.
    for module in serve_surface_paths() + (TURNS_PY,):
        source = module.read_text(encoding="utf-8")
        for forbidden in ("envelope.bound_buffer", "prompt_envelope.bound_buffer",
                          "self.bound_buffer", "bound_buffer=bound_buffer,",
                          "bound_buffer: str | None"):
            assert forbidden not in source, (
                f"{module.name} carries {forbidden!r}: the binding is carried "
                f"on the wire, never as an unreadable server-side value")


# ---------------------------------------------------------------------------
# NEGATIVE 2: no inference from `active_document_path`
# ---------------------------------------------------------------------------

def test_the_widened_request_envelope_has_no_active_document_path():
    """The strongest form of the negative available: on the widened envelope the
    field the mis-derivation read is not merely unused, it is UNREPRESENTABLE.
    The envelope is closed, so a request carrying one is refused by the schema
    itself rather than by a rule someone has to remember."""
    document = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    request = document["$defs"]["request_v2"]
    assert request["additionalProperties"] is False
    assert "active_document_path" not in request["properties"]
    assert "bound_buffer" in request["properties"]
    assert "bound_buffer" in request["required"]
    # The RECORD names it too -- the whole point of the release.
    success = document["$defs"]["success_v2"]
    assert "bound_buffer" in success["properties"]
    assert "bound_buffer" in success["required"]


def test_a_widened_request_carrying_an_active_document_path_is_refused():
    """The same negative EXECUTED against the released validator, because a
    schema read in a test and a schema read by the route are only the same thing
    if something checks."""
    request = yaml.safe_load(
        (REPO_ROOT / "examples" / "ideation-dashboard"
         / "workbench-chat-turn-v2-loaded-set.example.yaml")
        .read_text(encoding="utf-8"))
    assert doxbench_contracts.validate_instance(request) == []
    smuggled = dict(request, active_document_path="ideation/staging/x/y.md")
    errors = doxbench_contracts.validate_instance(smuggled)
    assert errors, "the closed widened envelope must refuse the field"


@pytest.mark.parametrize("module", [CHAT_JS, WORKBENCH_JS],
                         ids=lambda path: path.name)
def test_no_browser_module_derives_a_binding_from_an_active_document_path(module):
    """The browser half. `activeDocumentPath` was the option the shell handed the
    rail and the rail put on the wire; the binding is now read from the one
    selection authority (`state.active_buffer`) instead, so the option is gone
    rather than left as a second answer to the same question."""
    # CODE only: a comment RECORDING what was removed is what a later reader
    # needs, and stripping the comments is what keeps this a measurement of the
    # module's behaviour rather than of its prose.
    source = "\n".join(
        line for line in module.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("//"))
    assert "activeDocumentPath" not in source, (
        f"{module.name} still carries an activeDocumentPath seam; the declared "
        f"binding is the SELECTED buffer's key, read from the state authority")
    assert "active_document_path" not in source, (
        f"{module.name} still names the v1 wire field; the widened envelope "
        f"carries no such key for anything to infer a binding from")


def test_the_route_reads_the_declared_binding_rather_than_an_adjacent_field():
    """serve.py's own half, asserted on the source because the alternative is a
    live route with a provider. The v1 lane's parser MAY read
    `active_document_path` -- it is that envelope's own declared field, and
    reading a KEY off a declared path is a spelling change -- but the handler
    must pass the PARSED binding, whichever family it came from."""
    # THE SERVE SURFACE, not one file of it (§ 2.4 PR 2 of 4 moved this
    # code to a sibling module; the scan widened rather than narrowed).
    source = serve_surface_source()
    assert "bound_buffer_key=bound_buffer_key" in source
    assert "bound_buffer_key=active_document_path" not in source, (
        "the handler must pass the parsed binding, not re-derive one from the "
        "deprecated envelope's adjacent field")
