"""THE ONE PROCESS-START REGISTRATION — openxFactory as openDox's host.

WHAT THIS FILE IS. `split-opendox-two-layer-product` § 4.3 and § 4.4 each end at
the same place: a HOST that registers its own domain profile once, at process
start, with the two neutral legs it drives. This module is that host side, and
it is the whole of it. Every openxFactory process that builds an openDox PARSER
or an openDox SERVER calls `register_openxfactory()` before it builds, and
nothing else in this repository touches either leg's registry.

THE TWO RULINGS IT REALIZES.

* RULED ASK-2 option (2) (`openxFactory#656` comment `5628886636`): openDox's
  `cli.build_parser()` and `serve.build_server()` read their contributed
  subcommands and routes from `profile_openxfactory`, a LAZY PROXY in
  openDox-code, and *"openxFactory registers the real module at process
  start"*. The proxy landed as openDox-code #11 (`a99eba03`); before it, this
  repository stood in with `carved_reach.bind_composition_point()`, an import
  hook that bound the module into each consumer's globals. That stand-in said
  of itself: *"When openDox-code's lazy proxy lands, the consumers will import
  the proxy themselves and this becomes the single `register(profile)` call the
  ruling describes; the finder below goes away with the hole it covers."* It
  has, and it did.
* RULING C2 and RULED ASK-4 (`5634195861`): openXdox's lifecycle engine reads
  its status vocabulary, per-kind terminal statuses, immutability point,
  transitions and authorities from a registered `DomainProfile` built from a
  canonical YAML — `contracts/domain-profiles/openxfactory-engineering.yaml`,
  beside this file's own repository's document-lifecycle policy. *"A hardcoded
  status word is a defect under `domain-mapping-declaration`."*

ONE REGISTRATION, TWO ACCESSORS — AND WHY THERE IS ONLY ONE CALL BELOW.
RULED ASK-4 Q5 is "one registration, two accessors", and the legs implement it
by DELEGATION rather than by two hooks. openXdox's registry names openDox's
verbatim — `_UPSTREAM_REGISTRY = "opendox.domain_profile"`
(`openxdox/domain_profile.py:135`) — and its `current()` consults
`_upstream()` (`:1135`, called at `:1173`) whenever its own registry is empty,
accepting the upstream object only when it `isinstance(..., DomainProfile)`.
openDox's own registry docstring states the consequence and names the shape
this file builds:

    "A host that wants ONE object to serve both therefore registers a profile
    that satisfies both readers — e.g. an `openxdox.domain_profile.DomainProfile`
    subclass carrying the two extension tuples. That composition is the HOST's"
    (`opendox/domain_profile.py:74-79`)

and REFUSES the alternative in the same breath: *"THE ALTERNATIVE REJECTED:
'the host calls BOTH legs' `register()` in one documented process-start hook'
… It is TWO registrations wearing one hook's name"* (`:49-59`). So
`register_openxfactory()` makes exactly one call,
`opendox.domain_profile.register(...)`, and openXdox reaches the same object
through its delegation. Nothing here imports `openxdox` in order to register
with it.

REFUSAL, NOT A DEFAULT. A process that forgets this call does not get an empty
profile; it gets `opendox.domain_profile.ProfileNotRegistered` or
`openxdox.domain_profile.DomainProfileNotRegistered`, each naming its own
registration call. That is the ruled stance on both legs and it is not softened
here: this module has no fallback profile, composes nothing when the YAML is
missing, and lets a malformed profile's `DomainProfileInvalid` out unchanged.

A CREATED FILE: no row in `docs/opendox-carve-manifest.yaml`, which declares
what LEAVES this repository and never what it assembles (RULED OQ-C).
"""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any

import carved_reach

__all__ = [
    "FACETS",
    "PROFILE_PATH",
    "build_profile",
    "profile",
    "register_openxfactory",
]

REPO_ROOT = Path(__file__).resolve().parents[1]

#: The canonical declaration. RULED ASK-4 Q1: the YAML is canonical and the
#: dataclass `load()` builds from it is the runtime form, so a malformed
#: profile is refused ONCE on the way in rather than at each site that reads it.
PROFILE_PATH = REPO_ROOT / "contracts" / "domain-profiles" / "openxfactory-engineering.yaml"

#: THE FACETS openDox READS, and the only names this host's profile forwards to
#: `scripts/profile_openxfactory.py`. The first two are exactly what
#: `opendox.profile_proxy._LateProfile.READERS` maps to a reader —
#: `SUBCOMMAND_EXTENSIONS` for `cli.build_parser()`, `ROUTE_EXTENSIONS` for
#: `serve.build_server()`. `cli_gate` is not read by either leg; it is read by
#: this repository's own `test_cli_column_split.py`, whose
#: `test_a_library_caller_gets_the_columns_of_its_own_core` asserts
#: `profile.cli_gate is gate` — the profile's reference to the column must be
#: the SAME module object a sibling import produces.
#:
#: A NARROW LIST RATHER THAN BLANKET FORWARDING, on purpose. A leg that comes to
#: read a third facet should fail with `ProfileFacetMissing` naming it — the
#: refusal that sends a host to its own profile rather than to its
#: registration — and the fix is a declared row here. Forwarding everything
#: would answer a facet this repository never decided to contribute.
FACETS: tuple[str, ...] = ("SUBCOMMAND_EXTENSIONS", "ROUTE_EXTENSIONS", "cli_gate")

_PROFILE_CLASS: type | None = None
_COMPOSED: Any = None


def _profile_class() -> type:
    """The composite class, built on first use rather than at import time.

    ITS BASE CLASS LIVES AT A PINNED LEG. `openxdox.domain_profile.DomainProfile`
    is reachable only once `carved_reach.install()` has put
    `openXdox/code/src` on the path, so a `class X(DomainProfile)` statement at
    module scope would make THIS module unimportable in a checkout whose
    gitlinks are not materialized — and would do it with an `ImportError` from
    an import line, which is precisely the failure `carved_reach` exists to
    replace with a refusal that names the missing leg and the command that
    fixes it. Built here instead, once, and cached.
    """
    global _PROFILE_CLASS
    if _PROFILE_CLASS is not None:
        return _PROFILE_CLASS

    from openxdox import domain_profile as engine

    class OpenxFactoryProfile(engine.DomainProfile):
        """openxFactory's `DomainProfile`, carrying openDox's two facets.

        Frozen and read-only by construction, like the base: this adds an
        attribute FORWARDER and no state. The forward target is
        `scripts/profile_openxfactory.py`, which holds the real route and
        subcommand contributions and resolves `SUBCOMMAND_EXTENSIONS` on first
        access (PEP 562) so that a server process never pays for the CLI
        column's dependency chain. Forwarding rather than copying the tuples in
        at compose time is what preserves that: reading `ROUTE_EXTENSIONS` off
        this object touches the module's module-level tuple, and reading
        `SUBCOMMAND_EXTENSIONS` runs its `__getattr__` at that moment and not
        before.
        """

        __slots__ = ()

        def __getattr__(self, name: str) -> Any:
            # Only the DECLARED facets, and never an underscore name. A frozen
            # dataclass instance answers its own fields by ordinary lookup, so
            # this runs for nothing the base already carries; the guard is for
            # the probes — `copy`, `pickle`, `inspect`, pytest's assertion
            # rewriting — that ask arbitrary objects for dunders and expect an
            # `AttributeError` rather than a forwarded lookup.
            if name in FACETS:
                import profile_openxfactory
                return getattr(profile_openxfactory, name)
            raise AttributeError(
                f"{type(self).__name__} carries the domain profile "
                f"{self.mapping_id!r} and forwards only openxFactory's declared "
                f"composition facets {list(FACETS)}; {name!r} is neither a "
                "field of the profile nor one of them. If a leg has come to "
                "read a new facet, declare it in scripts/opendox_host.py's "
                "FACETS and contribute it from scripts/profile_openxfactory.py "
                "— openxFactory decides what it contributes, and a silently "
                "forwarded name would answer for a decision nobody made.")

    _PROFILE_CLASS = OpenxFactoryProfile
    return _PROFILE_CLASS


def build_profile() -> Any:
    """Load the canonical YAML and compose the object BOTH legs read.

    Returns a fresh composite every call; `register_openxfactory()` holds the
    one this process registers. Public because a test that wants a profile
    without touching either registry should not have to reach a private name.
    """
    from openxdox import domain_profile as engine

    loaded = engine.load(PROFILE_PATH)
    cls = _profile_class()

    # A FACET THAT COLLIDES WITH A PROFILE FIELD WOULD BE SILENTLY LOST.
    # `__getattr__` runs only when ordinary lookup FAILS, so a facet named like
    # one of `DomainProfile`'s own fields or methods (`acts`, `basis`, `source`,
    # `status`, …) would hand openDox the dataclass's value and never reach
    # `profile_openxfactory` — a wrong answer rather than a refusal. Checked
    # here, once, where both names are in hand.
    collisions = sorted(f for f in FACETS if hasattr(loaded, f))
    if collisions:
        raise RuntimeError(
            f"openxFactory's composition facets {collisions} collide with "
            f"fields or methods of openxdox.domain_profile.DomainProfile. A "
            "colliding facet is never forwarded — attribute lookup finds the "
            "profile's own value first — so openDox would read the wrong "
            "object with nothing to report it. Rename the contribution in "
            "scripts/profile_openxfactory.py and in FACETS.")

    return cls(**{f.name: getattr(loaded, f.name) for f in dataclasses.fields(loaded)})


def profile() -> Any:
    """This process's composite profile, composed on first use."""
    global _COMPOSED
    if _COMPOSED is None:
        _COMPOSED = build_profile()
    return _COMPOSED


def register_openxfactory() -> Any:
    """THE ONE CALL. Every openxFactory assembly point makes it before it builds.

    IDEMPOTENT. The composite is composed once and cached, so a second call
    re-registers the SAME object, which `opendox.domain_profile.register()`
    treats as a no-op — an assembly point that is entered twice, a conftest
    that is loaded under two rootdirs, a test that re-enters the hook, none of
    them is punished.

    NOT IDEMPOTENT ACROSS A *DIFFERENT* PROFILE, deliberately. If something
    else has registered another profile into this process, `AlreadyRegistered`
    is raised and NOT swallowed: one process composing from two profiles, half
    its readers on each, is the failure the ruled single registration exists to
    prevent, and it is worth an exception rather than a log line. A deliberate
    swap calls `opendox.domain_profile.unregister()` first.

    AND THE SAME REFUSAL IS OWED ON THE OTHER REGISTRY, which the openDox call
    alone cannot give (Copilot review, PR #984). The delegation that makes ONE
    call serve both accessors is `openxdox.domain_profile.current()` consulting
    `_upstream()` *only when its own registry is empty* (`:1173`) — so a process
    where something has already called `openxdox.domain_profile.register(other)`
    is the exact split this function's own contract forbids, and the openDox
    registry cannot see it: `opendox…current()` would answer the composite while
    `openxdox…current()` answered `other`, and this call would return
    successfully with half its readers on each profile. Checked FIRST, through
    openXdox's own public `is_registered()`/`current()`, and BEFORE the openDox
    registry is touched, so a refused process is left with NEITHER registry
    mutated rather than half-registered.

    IT DOES NOT FIRE ON THIS MODULE'S OWN REGISTRATION, because this module
    never writes to openXdox's registry: after `register_openxfactory()` the
    openXdox registry is still empty and the composite is reached by delegation,
    so `is_registered()` there stays False and the idempotent second call takes
    exactly the path the first did.

    WHO CALLS IT — every process that builds an openDox parser or server, AND
    every process that reaches the § 4.4 ENGINE. § 4.3's landing note recorded
    the first widening (*"scope grew: every openxFactory process that builds a
    SERVER needs the hook too, not only a parser"*); § 4.4 is the second, and it
    is wider than the note, because the lifecycle engine is reached by lanes
    that build neither a parser nor a server (Copilot review, PR #984).

    PARSER / SERVER:

      * `scripts/ideation-dashboard-serve.py`, the serve entrypoint
        `scripts/reserve-dashboard.sh` executes — the production caller.
      * `tests/conftest.py` and `tests/ideation-dashboard/conftest.py`, for the
        suites that build servers and parsers in-process.
      * `tests/ideation-dashboard/test_cli_column_split.py`'s BOOTSTRAP, the
        source string its two subprocess invocations of the real command line
        run before `runpy`.

    ENGINE. `openxdox.generator` and `openxdox.gate_console` are the only two
    modules at the pinned leg that call `openxdox.domain_profile.current()`, and
    two openxFactory lanes import them. Each registers at its own `main()`:

      * `scripts/ideation_dashboard/nightly_lane.py` — `generate_snapshot()`
        resolves the profile while deriving cluster lineage. Reached by
        `scripts/ideation-dashboard-nightly.py` AND by `python3 -m
        ideation_dashboard.nightly_lane`, which is the form
        `scripts/reserve-dashboard.sh`:69 runs, so the wrapper alone would not
        have covered it. This lane reports every error as SKIPPED and exits 0
        by contract, so an unregistered process published the refusal as a
        green-looking skip rather than failing.
      * `scripts/ideation_dashboard/intent_apply_lane.py` — reaches both engine
        readers.

    `scripts/ideation_dashboard/dashboard_refresh_lane.py` has a `__main__` of
    its own and does NOT call it: it imports neither engine module, and a hook
    where none is needed would be the blanket registration this file's FACETS
    list refuses in the other direction.

    A COLUMN must NOT call it: `ideation_dashboard/serve_openxfactory_lanes.py`
    is imported BY `profile_openxfactory`, so a column that registered the
    composition point would re-enter its own half-executed module. That is why
    `carved_reach.install()` does not fold this in — see its docstring.
    """
    # Idempotent, and required: the composite's base class and both registries
    # live at the pinned legs. An assembly point normally installs the reach
    # itself; doing it here too costs nothing and keeps this call the only
    # thing a new assembly point has to remember.
    carved_reach.install()

    from opendox import domain_profile as registry
    from openxdox import domain_profile as engine

    composite = profile()

    # THE OTHER REGISTRY, CHECKED BEFORE EITHER IS TOUCHED. `is_registered()`
    # answers openXdox's OWN registry without resolving or refusing, so it does
    # not consult the delegation and cannot be satisfied by this call's own
    # effect. Only a DIFFERENT object refuses: an `openxdox` registration of the
    # very composite being registered is the same one profile reached twice,
    # which is a no-op and not a split.
    if engine.is_registered() and engine.current() is not composite:
        raise engine.AlreadyRegistered(
            "openxdox.domain_profile already holds a different profile, so "
            "registering this one with openDox would leave the two accessors "
            "answering two profiles: openxdox.domain_profile.current() reads "
            "its OWN registry before it consults the openDox upstream, so the "
            "delegation that makes one registration serve both legs would be "
            "bypassed and half of this process's readers would compose from "
            "each. Neither registry has been written. Call "
            "openxdox.domain_profile.unregister() first if the swap is "
            "deliberate.")

    return registry.register(composite)
