"""openxFactory's own domain profile, and the ONE process-start registration.

WHAT THIS FILE POLICES — the openxFactory half of `split-opendox-two-layer-
product` § 4.3 and § 4.4:

  1. `contracts/domain-profiles/openxfactory-engineering.yaml` LOADS through the
     neutral engine's own loader, and its vocabulary is the one
     `docs/document-lifecycle.md` declares — READ OUT OF THE DOCUMENT, never
     transcribed here, so the profile and the policy cannot drift apart
     silently. RULING C2's defect is a hardcoded status word; a test that
     hardcoded the same nine words would reproduce it one layer up.
  2. `opendox_host.register_openxfactory()` composes: after it, openDox's lazy
     proxy resolves BOTH facets `cli.build_parser()` and `serve.build_server()`
     read, and openXdox's engine answers every question its migrated sites ask.
  3. ONE registration serves BOTH legs, by DELEGATION rather than by two hooks
     (RULED ASK-4 Q5, `#656` comment `5634195861`) — `openxdox.domain_profile
     .current()` hands back the very object this host registered with openDox.
  4. The refusals stand: nothing registered is a REFUSAL and not an empty
     profile, and a SECOND, different profile is refused rather than applied.

THE REGISTRY IS PROCESS-WIDE, so the two tests that need an EMPTY registry run
in a SUBPROCESS. Unregistering in-process would pull the composition point out
from under every other test in the session — the exact fixture-teardown defect
openDox-code #11's review found and fixed on its own side.
"""

from __future__ import annotations

import re
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
PROFILE_PATH = REPO_ROOT / "contracts" / "domain-profiles" / "openxfactory-engineering.yaml"
LIFECYCLE_DOC = REPO_ROOT / "docs" / "document-lifecycle.md"
SCRIPTS = REPO_ROOT / "scripts"

# `tests/conftest.py` has already installed the reach and made the ONE call, so
# every name below resolves the way it does in a real assembly point.
import opendox_host                                        # noqa: E402
from opendox import domain_profile as opendox_registry     # noqa: E402
from opendox import cli as opendox_cli                     # noqa: E402
from opendox.profile_proxy import ProfileFacetMissing      # noqa: E402
from opendox.profile_proxy import profile_openxfactory as proxy  # noqa: E402
from openxdox import domain_profile as openxdox_registry   # noqa: E402


# --------------------------------------------------------------------------
# 1. the declaration
# --------------------------------------------------------------------------

#: Rows of the controlled `Status:` table in `docs/document-lifecycle.md`:
#: `| ``word`` | lifecycle state | meaning |`.
_TABLE_ROW = re.compile(r"^\|\s*`(?P<status>[a-z-]+)`\s*\|\s*(?P<role>[^|]+?)\s*\|")


def controlled_statuses() -> tuple[str, ...]:
    """The controlled taxonomy, read out of the policy document itself.

    The document is the source of truth (`Status: standard`, and the promoted
    requirement at `openspec/specs/document-lifecycle/spec.md` behind it); this
    profile follows it and does not lead it. Reading the table rather than
    listing them here is what makes this an agreement test instead of a second
    declaration free to drift.
    """
    found: list[str] = []
    for line in LIFECYCLE_DOC.read_text(encoding="utf-8").splitlines():
        match = _TABLE_ROW.match(line)
        if match and match.group("status") not in found:
            found.append(match.group("status"))
    return tuple(found)


def test_the_controlled_table_is_still_readable():
    """A guard on the guard: a table this parser cannot read must not pass as
    an empty taxonomy that every other assertion below then trivially matches."""
    statuses = controlled_statuses()
    assert len(statuses) >= 8, (
        f"only {statuses} parsed out of {LIFECYCLE_DOC.relative_to(REPO_ROOT)}'s "
        "controlled table — the table's shape changed and this reader did not")


def test_the_profile_loads_through_the_engines_own_loader():
    """RULED ASK-4 Q1: the YAML is canonical and `load()` is the ONE place a
    malformed profile is refused. If it refuses this file, nothing else here
    matters."""
    profile = openxdox_registry.load(PROFILE_PATH)
    assert profile.mapping_id == "openxfactory-engineering"
    assert profile.neutral is False
    assert profile.declared_by == "opensoft/openxFactory"


def test_the_profile_declares_exactly_the_controlled_taxonomy():
    """The nine words, and no tenth.

    `docs/document-lifecycle.md` lines 41-49 carry `brainstorm staged draft
    ratified standard superseded retired record projection`. The eight-word
    reading taken from a stale working tree is retracted at `#656` comment
    `5633989351`; this assertion is against the document as it stands.
    """
    profile = openxdox_registry.load(PROFILE_PATH)
    declared = profile.statuses("governance-document")
    assert declared == controlled_statuses(), (
        "the governance-document vocabulary and the controlled `Status:` table "
        "disagree; the table is the source of truth and this profile follows it")


def test_every_governance_status_carries_a_neutral_role():
    """RESOLVE BY ROLE, NOT BY STRING — the property that makes this a
    parameterization rather than a rename for the next descendant."""
    lifecycle = openxdox_registry.load(PROFILE_PATH).lifecycle_for("governance-document")
    for status in lifecycle.vocabulary:
        assert status.role in openxdox_registry.KNOWN_ROLES, (
            f"{status.id!r} declares role {status.role!r}, which the engine's "
            f"neutral role vocabulary does not carry")


def test_the_register_vocabulary_is_the_registers_own_schema():
    """`register-possible` follows `contracts/schemas/ideation-possibles-
    register.schema.yaml`, not this profile's convenience.

    ASK-4 Q4 ruled `terminal_statuses` PER KIND precisely because the register's
    words are not the document spine's. Read from the register schema's own
    `state` enum so the two cannot drift.
    """
    schema = yaml.safe_load(
        (REPO_ROOT / "contracts" / "schemas" / "ideation-possibles-register.schema.yaml")
        .read_text(encoding="utf-8"))
    enums = [node["enum"] for node in _walk(schema)
             if isinstance(node, dict) and isinstance(node.get("enum"), list)
             and "latent" in node["enum"]]
    assert enums, "no `state` enum carrying `latent` found in the register schema"
    profile = openxdox_registry.load(PROFILE_PATH)
    assert set(profile.statuses("register-possible")) == set(enums[0])


def _walk(node):
    yield node
    if isinstance(node, dict):
        for value in node.values():
            yield from _walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from _walk(value)


def test_the_profile_answers_every_question_the_migrated_engine_asks():
    """The ten literal-taxonomy sites openXdox-code #14 migrated now READ these.

    Each call below is one of the engine's own, spelled as `gate_console.py` and
    `generator.py` spell it. A profile that loads but cannot answer them would
    leave the engine refusing at runtime with nothing here to show it.
    """
    profile = openxdox_registry.current()
    assert profile.destination_role_status("demote", "organized") == "staged"
    assert profile.status("proposed", kind=profile.kind_declaring("demote")) == "draft"
    register = profile.kind_declaring("promote-to-staging")
    assert register == "register-possible"
    assert profile.terminal_statuses(register) == ("rejected", "superseded")
    assert profile.status("captured", kind=register) == "latent"
    assert profile.status("proposed", kind=register) == "picked"


def test_the_projection_kind_never_freezes_and_every_other_kind_does():
    """`domain-mapping-declaration`'s second refusal, both halves.

    "A vocabulary with no declared immutability point SHALL be refused rather
    than defaulted to 'never'" — so the field is required for every kind, and
    the one kind that genuinely never freezes says so IN the field with a
    reason, rather than by omission.
    """
    profile = openxdox_registry.load(PROFILE_PATH)
    never = [kind for kind in profile.kinds()
             if profile.immutability_point(kind).never_freezes]
    assert never == ["projection-document"]
    assert profile.immutability_point("projection-document").note
    assert profile.is_immutable("governance-document", "ratified")
    assert not profile.is_immutable("governance-document", "draft")


# --------------------------------------------------------------------------
# 2 and 3. the ONE registration, and both accessors
# --------------------------------------------------------------------------

def test_the_host_registered_its_profile_with_opendox():
    """§ 4.3's whole point: the assembly point made the call before it built."""
    assert opendox_registry.is_registered()
    assert opendox_registry.current() is opendox_host.profile()
    assert opendox_registry.current().mapping_id == "openxfactory-engineering"


def test_one_registration_serves_both_legs_by_delegation():
    """RULED ASK-4 Q5 — "one registration, two accessors", not two hooks.

    openXdox's registry names openDox's verbatim
    (`_UPSTREAM_REGISTRY = "opendox.domain_profile"`) and `current()` consults
    it when its own registry is empty, accepting only an object that IS a
    `DomainProfile`. This asserts the consequence that shape exists for: the
    object openXdox's engine reads is the very object the host handed openDox,
    so the two accessors cannot disagree.
    """
    assert not openxdox_registry.is_registered(), (
        "openXdox's OWN registry should be empty — openxFactory makes ONE call, "
        "to openDox, and openXdox reaches it by delegation")
    assert openxdox_registry.current() is opendox_registry.current()
    assert isinstance(openxdox_registry.current(), openxdox_registry.DomainProfile)


def test_the_proxy_resolves_both_facets_the_composition_points_read():
    """`_LateProfile.READERS`: `SUBCOMMAND_EXTENSIONS` for `cli.build_parser()`,
    `ROUTE_EXTENSIONS` for `serve.build_server()`. Both come off the REAL
    module, forwarded by the composite rather than copied into it."""
    import profile_openxfactory

    assert proxy.ROUTE_EXTENSIONS is profile_openxfactory.ROUTE_EXTENSIONS
    assert len(proxy.ROUTE_EXTENSIONS) == 3
    assert len(proxy.SUBCOMMAND_EXTENSIONS) == 1
    assert proxy.cli_gate is profile_openxfactory.cli_gate


def test_the_parser_builds_from_the_registered_profile():
    """`cli.build_parser()` is one of the two composition points § 4.3 names;
    building it is the end-to-end proof the registration reaches it."""
    parser = opendox_cli.build_parser()
    actions = {action.dest for action in parser._actions}
    assert actions, "build_parser() produced a parser with no actions"


def test_the_servers_route_table_collects_from_the_registered_profile():
    """The SERVER half — `build_server()` reads `ROUTE_EXTENSIONS` and hands it
    to `route_extension.collect_bindings`. § 4.3's landing note recorded that
    the scope grew to servers, not only parsers."""
    import route_extension

    bindings = route_extension.collect_bindings(tuple(proxy.ROUTE_EXTENSIONS))
    assert bindings, "the registered profile contributed no route bindings"


def test_a_facet_the_profile_does_not_carry_is_named_rather_than_defaulted():
    """A registered profile lacking a facet is a gap in the PROFILE, and the
    refusal says so — distinct from "nothing registered", which sends a host to
    its process-start hook instead."""
    with pytest.raises(ProfileFacetMissing) as excinfo:
        proxy.A_FACET_NO_HOST_CONTRIBUTES
    assert "A_FACET_NO_HOST_CONTRIBUTES" in str(excinfo.value)


def test_registering_is_idempotent():
    """An assembly point entered twice — two conftests under two rootdirs, a
    test that re-enters the hook — must not be punished."""
    first = opendox_registry.current()
    assert opendox_host.register_openxfactory() is first
    assert opendox_host.register_openxfactory() is first


def test_a_second_different_profile_is_refused_rather_than_applied():
    """ONE registration is the contract. A swap under a live process would
    leave a parser built from the first profile while every later reader saw
    the second, with nothing to report it."""
    other = opendox_host.build_profile()
    assert other is not opendox_registry.current()
    with pytest.raises(opendox_registry.AlreadyRegistered):
        opendox_registry.register(other)
    # untouched by the refusal
    assert opendox_registry.current() is opendox_host.profile()


# --------------------------------------------------------------------------
# 4. the refusal, in a process that never registered
# --------------------------------------------------------------------------

_UNREGISTERED = textwrap.dedent("""
    import sys
    sys.path.insert(0, {scripts!r})
    import carved_reach
    carved_reach.install()
    from opendox import domain_profile as odp
    from openxdox import domain_profile as xdp
    for registry, expected in ((odp, "ProfileNotRegistered"),
                               (xdp, "DomainProfileNotRegistered")):
        try:
            registry.current()
        except Exception as exc:
            print(type(exc).__name__, "|", "register(" in str(exc))
        else:
            print("NO REFUSAL")
    from opendox.profile_proxy import profile_openxfactory as proxy
    try:
        proxy.ROUTE_EXTENSIONS
    except Exception as exc:
        print(type(exc).__name__, "|", "register(" in str(exc))
    else:
        print("NO REFUSAL")
""")


def test_a_process_that_never_registered_refuses_and_names_the_call():
    """REFUSAL, NOT A DEFAULT, on both legs and through the proxy.

    In a SUBPROCESS: the registry is process-wide, and unregistering in-process
    would pull the composition point out from under the rest of the session.
    """
    proc = subprocess.run(
        [sys.executable, "-c", _UNREGISTERED.format(scripts=str(SCRIPTS))],
        capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert proc.returncode == 0, proc.stderr
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    assert lines == [
        "ProfileNotRegistered | True",
        "DomainProfileNotRegistered | True",
        "ProfileNotRegistered | True",
    ], proc.stdout


def test_the_host_registration_is_what_makes_a_bare_process_work():
    """The same process, with the ONE call added, composes."""
    program = textwrap.dedent("""
        import sys
        sys.path.insert(0, {scripts!r})
        import carved_reach
        carved_reach.install()
        import opendox_host
        opendox_host.register_openxfactory()
        from opendox.profile_proxy import profile_openxfactory as proxy
        from openxdox import domain_profile as xdp
        print(len(proxy.ROUTE_EXTENSIONS), xdp.current().mapping_id)
    """).format(scripts=str(SCRIPTS))
    proc = subprocess.run([sys.executable, "-c", program],
                          capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "3 openxfactory-engineering"


def test_a_facet_colliding_with_a_profile_field_is_refused_at_compose_time():
    """`__getattr__` runs only when ordinary lookup FAILS, so a facet named like
    one of `DomainProfile`'s own fields would hand openDox the dataclass's value
    and never reach `profile_openxfactory` — a wrong answer rather than a
    refusal. `build_profile()` refuses instead."""
    original = opendox_host.FACETS
    opendox_host.FACETS = original + ("mapping_id",)
    try:
        with pytest.raises(RuntimeError) as excinfo:
            opendox_host.build_profile()
        assert "mapping_id" in str(excinfo.value)
    finally:
        opendox_host.FACETS = original
