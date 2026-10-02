"""The host registers openXdox's governed projection (plan 034 T064).

WHAT THIS FILE POLICES. From openXdox-code `839492d9` (#35, T059), openXdox
contributes its governed generator, snapshot registry, corpus-root predicate,
writer and validators at openDox's seams through
`openxdox.projection_contributions.register()`. `openxdox.domain_profile.register()`
makes that call, but openxFactory registers its profile with openDox alone, so
`opendox_host.register_openxfactory()` makes it itself. The holder decided this
on 2026-09-29 at T059, revising the decision of 2026-09-27 at T052. Without the
call, every openDox entry point projects through openDox's neutral defaults.

  1. The one call registers the contributions, and a fresh process holds none
     of them before it.
  2. It registers them AFTER openDox answers the profile and BEFORE the host's
     own seams.
  3. A second call is a no-op: the same objects stay registered.
  4. If openDox refuses the profile, no projection seam is written, and
     openDox's unread defaults stay where they were (Copilot, #1215).
     Contributions the process already held stay too. If the contribution
     is refused, the profile stays registered and no seam of the host's is
     written.
  5. MUTATION: with the contribution call made a no-op, the property in 1
     fails, so 1 is what the line keeps.

THE SEAMS ARE PROCESS-WIDE, so every case but the first runs in a SUBPROCESS,
as `test_openxfactory_host_wiring.py` explains for the registries. Each child
asks `projection_contributions.is_registered()`, which reads each seam where it
keeps its registration and so never closes a default's window.
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts"

# `tests/conftest.py` has already installed the reach and made the ONE call.
from opendox import generator_seam                          # noqa: E402
from openxdox import projection_contributions               # noqa: E402

#: Every child starts the same way: the scripts directory on the path, the
#: pinned reach installed, and nothing registered yet.
_PRELUDE = """
    import sys
    sys.path.insert(0, {scripts!r})
    import carved_reach
    carved_reach.install()
    import opendox_host
    from opendox import domain_profile as odp
    from opendox import generator_seam
    from openxdox import projection_contributions as pc
"""


def _run(program: str) -> subprocess.CompletedProcess:
    source = textwrap.dedent(_PRELUDE) + textwrap.dedent(program)
    return subprocess.run(
        [sys.executable, "-c", source.format(scripts=str(SCRIPTS))],
        capture_output=True, text=True, cwd=str(REPO_ROOT))


def _words(program: str) -> list[str]:
    proc = _run(program)
    assert proc.returncode == 0, proc.stderr
    return proc.stdout.split()


# --------------------------------------------------------------------------
# 1. the one call registers openXdox's governed projection
# --------------------------------------------------------------------------

def test_this_process_holds_the_governed_projection():
    """The conftest's one call left every contribution at its seam, and the
    generator seam answers openXdox's governed generator."""
    assert projection_contributions.is_registered()
    assert generator_seam.current() is projection_contributions.GENERATOR


def test_a_fresh_process_holds_it_only_after_the_call():
    """Importing the host registers nothing. The call registers every
    contribution, and the generator seam then answers the governed one."""
    assert _words("""
        print(pc.is_registered())
        opendox_host.register_openxfactory()
        print(pc.is_registered(), generator_seam.current() is pc.GENERATOR)
    """) == ["False", "True", "True"]


# --------------------------------------------------------------------------
# 2. after the profile, before the host's seams
# --------------------------------------------------------------------------

def test_the_contributions_follow_the_profile_and_precede_the_seams():
    """openDox's `register()` is reached with no contribution written, and
    `register_seams()` with every one in place."""
    assert _words("""
        real_register, real_seams = odp.register, opendox_host.register_seams
        def spy_register(profile):
            print("AT_PROFILE", pc.is_registered())
            return real_register(profile)
        def spy_seams():
            print("AT_SEAMS", pc.is_registered())
            return real_seams()
        odp.register = spy_register
        opendox_host.register_seams = spy_seams
        opendox_host.register_openxfactory()
    """) == ["AT_PROFILE", "False", "AT_SEAMS", "True"]


# --------------------------------------------------------------------------
# 3. idempotent
# --------------------------------------------------------------------------

def test_a_second_call_is_a_no_op():
    """The second call returns the same profile, refuses nothing, and leaves
    the same contribution objects registered."""
    assert _words("""
        first = opendox_host.register_openxfactory()
        generator = generator_seam.current()
        second = opendox_host.register_openxfactory()
        print(first is second, pc.is_registered(),
              generator_seam.current() is generator is pc.GENERATOR)
    """) == ["True", "True", "True"]


# --------------------------------------------------------------------------
# 4. a refusal leaves no seam half written
# --------------------------------------------------------------------------

def test_a_refused_profile_writes_no_projection_seam():
    """openDox refuses the profile. The refusal reaches the caller unchanged,
    and no seam has been written, so the process is neither half registered
    nor half governed."""
    assert _words("""
        def refuse(profile):
            raise odp.AlreadyRegistered("refused for the test")
        odp.register = refuse
        try:
            opendox_host.register_openxfactory()
        except odp.AlreadyRegistered as exc:
            print("REFUSED", "refused for the test" in str(exc))
        else:
            print("NO REFUSAL")
        print(pc.is_registered(), generator_seam.is_registered())
    """) == ["REFUSED", "True", "False", "False"]


def test_a_refused_profile_leaves_openDoxs_unread_defaults_in_place():
    """Copilot's case on #1215. openDox's entry-point defaults are installed
    and unread when openDox refuses the profile. Each default is still the
    one its seam answers afterwards, because nothing was written over it."""
    assert _words("""
        from opendox import default_generator, default_projection
        from opendox import default_registry, projection_seams
        generator_seam.register_default(default_generator.GENERATOR)
        projection_seams.register_defaults()
        def refuse(profile):
            raise odp.AlreadyRegistered("refused for the test")
        odp.register = refuse
        try:
            opendox_host.register_openxfactory()
        except odp.AlreadyRegistered:
            print("REFUSED")
        kind = default_projection.OWN_KINDS[0]
        print(generator_seam.current() is default_generator.GENERATOR,
              projection_seams.registry.current() is default_registry,
              projection_seams.corpus_root.current()
              is default_projection.CORPUS_ROOT,
              projection_seams.writer.current() is default_projection.WRITER,
              projection_seams.validators.for_kind(kind)
              is default_projection.VALIDATORS[kind])
    """) == ["REFUSED", "True", "True", "True", "True", "True"]


def test_a_refused_profile_leaves_contributions_the_process_already_held():
    """Contributions registered before the call are the process's, not the
    call's, so a refusal does not take them away."""
    assert _words("""
        pc.register()
        def refuse(profile):
            raise odp.AlreadyRegistered("refused for the test")
        odp.register = refuse
        try:
            opendox_host.register_openxfactory()
        except odp.AlreadyRegistered:
            print("REFUSED")
        print(pc.is_registered())
    """) == ["REFUSED", "True"]


def test_a_refused_contribution_leaves_the_profile_and_writes_no_host_seam():
    """The contribution is refused once the profile is registered. The refusal
    reaches the caller unchanged, the profile stays registered, as a refusal
    inside `register_seams()` leaves it, and the host's seams are not
    reached, so the home corpus is still unregistered."""
    assert _words("""
        def refuse():
            raise RuntimeError("contribution refused for the test")
        pc.register = refuse
        try:
            opendox_host.register_openxfactory()
        except RuntimeError as exc:
            print("REFUSED", "refused for the test" in str(exc))
        print(odp.current() is opendox_host.profile())
        from opendox import corpus_adapter
        try:
            corpus_adapter.home()
        except corpus_adapter.CorpusRefused:
            print("NO_HOST_SEAM")
        else:
            print("A_HOST_SEAM_WAS_WRITTEN")
    """) == ["REFUSED", "True", "True", "NO_HOST_SEAM"]


# --------------------------------------------------------------------------
# 5. mutation
# --------------------------------------------------------------------------

def test_mutation_without_the_contribution_the_property_fails():
    """MUTATION. With the contribution call made a no-op, the host still
    registers its profile, and the governed projection is absent: the state
    case 1 refuses."""
    assert _words("""
        pc.register = lambda: ()
        opendox_host.register_openxfactory()
        print(odp.current() is opendox_host.profile(), pc.is_registered())
    """) == ["True", "False"]
