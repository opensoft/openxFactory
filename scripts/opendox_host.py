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
`register_openxfactory()` registers the PROFILE with exactly one call,
`opendox.domain_profile.register(...)`, and openXdox reaches the same object
through its delegation. Nothing here imports `openxdox` in order to register
with it.

AND THE SEAMS, IN THE SAME CALL (plan 034 T046; #1144 tasks 4.1 and 4.3).
openDox-code's phase 1 turned eight deferred reaches into this repository into
seams a host fills at process start: the home corpus (`register_home`), the
session notebook's scope, the scoped health check, the doxBench validators and
the status-exemption rail. `register_openxfactory()` fills each of them with
the code the reach used to import, after the profile, and asserts that the
profile it registered is the one the registry answers (R1Q4 (a)). The block
"THE SEAMS" below carries the reasoning. A pinned leg that predates the seams
declares none of them, and nothing is registered there.

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
    "HostProfileNotRegistered",
    "HostSeamsIncomplete",
    "PROFILE_PATH",
    "SESSION_NOTEBOOK_SCOPE",
    "build_profile",
    "doxbench_validators",
    "home_corpus",
    "profile",
    "register_openxfactory",
    "register_seams",
    "scoped_doc_health",
    "seams",
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
#: `DISPLAY` is a FOURTH kind of reader (§ 3.4 slice S7's landing precondition,
#: openxFactory#656 comment `5649744596`): `opendox.display_profile
#: .host_display()` reads it for `serve.py`'s `/capabilities` payload, which is
#: neither `cli.build_parser()` nor `serve.build_server()` and so is not in
#: `_LateProfile.READERS` either — `host_display()` reads it through
#: `getattr(profile_openxfactory, "DISPLAY", None)`, a 3-argument `getattr`
#: whose default absorbs `ProfileFacetMissing` cleanly (it subclasses
#: `AttributeError`), which is how "registered, no facet declared" stays
#: distinct from a crash. `scripts/profile_openxfactory.py`'s own module
#: docstring ("THE FOURTH FACET") carries the rest of the reasoning.
#:
#: `HANDLER_CONTRIBUTIONS` is the FIFTH (plan 034 T045, R1Q1 (a), `#656`
#: comment `5817152735`). `serve.build_server()` reads it off the registered
#: profile, through the same lazy proxy, and composes the mixins it names into
#: the class it binds (openDox-code T010). openxFactory contributes its lanes
#: column there, because T011 took `LaneRoutes` off the bases of openDox's
#: `DashboardHandler`. `scripts/profile_openxfactory.py`'s declaration says
#: why the column is the only member. A leg that predates the facet never asks
#: for it.
#:
#: A NARROW LIST RATHER THAN BLANKET FORWARDING, on purpose. A leg that comes to
#: read a facet not listed here should fail with `ProfileFacetMissing` naming
#: it — the refusal that sends a host to its own profile rather than to its
#: registration — and the fix is a declared row here. Forwarding everything
#: would answer a facet this repository never decided to contribute.
FACETS: tuple[str, ...] = (
    "SUBCOMMAND_EXTENSIONS", "ROUTE_EXTENSIONS", "cli_gate", "DISPLAY",
    "HANDLER_CONTRIBUTIONS",
)

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


# --------------------------------------------------------------------------
# THE SEAMS (plan 034 T046; #1144 tasks 4.1 and 4.3, the host's half)
# --------------------------------------------------------------------------
#
# Eight of openDox-code's deferred reaches used to import this repository's
# packages by name, inside function bodies, so they passed every import check
# and failed only when called in a tree without this repository. Phase 1 of
# plan 034 turned each into a SEAM that a host fills with ONE registration at
# process start (openDox-code T020, T025, T026 and T027), in
# `opendox.domain_profile`'s idiom: the same object again is a no-op, a
# different one is refused, and an empty seam refuses naming itself. This host
# is the one whose packages the reaches named, so it registers the very code
# they reached, and what a hosted request gets is unchanged.
#
# EACH IMPLEMENTATION IS RESOLVED WHEN IT IS CALLED, as the reach it replaces
# was. The two factories below import their package on every call, so the
# registration adds nothing to a process's imports that the old reach did not,
# and it moves no import earlier. That matters for one of them in particular:
# `corpus_adapter_openxfactory` puts the pinned `openDox/code/src` at the head
# of `sys.path` when it is imported (#872, RULED OQ-Q), so importing it here,
# at process start, would change which copy of a top-level module such as
# `route_extension` every later import finds. The status-exemption rail is the
# exception, because the seam checks a rail's two names when it is
# registered: it is registered as the module itself, which imports only
# `re` and `doc_health.lines`, so the seven names the packet module forwards
# are that module's own objects, as openxFactory's tests read them.

#: The scope of this host's corpus that the session notebook lists (T025,
#: T046). `corpus_adapter_openxfactory`'s `documents` scope is the governed
#: roots, and it lists the same documents as the rule the reach it replaces
#: applied (`doc_health.corpus.load_docs`, filtered on a declared `Status:`
#: header): 398 of them at openxFactory `c415c3d1`, where `all` lists 794
#: (plan 034 T006). Spelled here rather than imported, because a module under
#: `scripts/` may bind only the adapter package's two public names
#: (`tests/corpus-adapter/test_no_privileged_route.py`), and pinned to the
#: adapter's declared scopes by `tests/domain_profile/`.
SESSION_NOTEBOOK_SCOPE = "documents"


def home_corpus(root: str) -> Any:
    """The home-corpus factory this host registers (T020's seam, T046).

    `adapter, ref = home_corpus(root)`, which is the shape
    `opendox.corpus_adapter.register_home()` takes. It is
    `corpus_adapter_openxfactory.home_corpus`, imported and called on each
    call, so every call builds a FRESH adapter: the adapter caches each
    listing per location, revision and scope for as long as it lives, and an
    uncommitted add moves no revision, so one shared adapter would hand a
    session notebook re-sync a stale listing (openDox-code #43's hand-off).
    """
    from corpus_adapter_openxfactory import home_corpus as build
    return build(root)


def scoped_doc_health(repo_root: Path, documents, *, repository: str, as_of,
                      families):
    """The scoped health check this host registers (T026's seam, T046).

    Its body is the code openDox-code #39 took out of
    `opendox.workbench.run_scoped_doc_health`, where it imported this
    repository's `doc_health` by name, so a scoped run answers exactly what it
    answered before. The seam resolves `repo_root`, defaults `repository` and
    `as_of`, and keeps only the findings on the requested documents. This
    function builds the `Context`: with no `lifecycle_docs`, so
    `status-validity`'s lifecycle scope is the scoped list itself.

    A family `doc_health` does not carry is refused with
    `opendox.workbench.WorkbenchError`, naming it, as it was before the seam.
    One thing is not carried over. The reach degraded to `not-available` when
    `doc_health` could not be imported, because openDox ships in trees that
    lack it. This is `doc_health`'s own repository, so a failed import here is
    a defect, and it reaches the caller rather than being reported as a clean
    `not-available`.
    """
    from doc_health import DEFAULT_THRESHOLDS, corpus as dh_corpus
    from doc_health.families import FAMILIES
    from doc_health.runner import Context, run_suite
    from opendox import workbench

    wanted = set(documents)
    docs = [d for d in dh_corpus.load_docs(repository, repo_root)
            if d.path in wanted]
    ctx = Context(
        repo_paths={repository: repo_root}, docs=docs, capabilities={},
        change_ids={}, git=dh_corpus.RealGit(),
        thresholds=dict(DEFAULT_THRESHOLDS), as_of=as_of, agg_root=None,
    )
    findings: list = []
    for family in families:
        if family not in FAMILIES:
            raise workbench.WorkbenchError(
                f"unknown doc-health family {family!r}")
        # only_family != None, so run_suite skips its preflight
        findings.extend(run_suite(ctx, family, set()).findings)
    return workbench.HealthCheckRun(findings=tuple(findings),
                                    documents_checked=len(docs))


def doxbench_validators() -> dict:
    """The doxBench schema-validators factory this host registers (T027, T046).

    The body of the reach it replaces, `serve_wire.default_doxbench_validators`
    before openDox-code #41: `ideation_dashboard.doxbench_contracts` is
    imported on the call and its `validators()` answered, so the pin is
    re-verified per request, a `ContractPinError` reaches the route as a
    fail-closed refusal as it did, and the module's PyYAML and `jsonschema`
    imports stay off every process that never serves a model route.
    """
    from ideation_dashboard import doxbench_contracts
    return doxbench_contracts.validators()


class HostProfileNotRegistered(RuntimeError):
    """This host registered its profile, and the registry answers another.

    R1Q4 (a) (`#656` comment `5817152735`): openDox now ships a default
    profile, which an entry point registers where no host has. A host running
    on that default would build a working-looking server with none of its own
    routes, so the host asserts at its own start that the registered profile
    is the one it registered.
    """


class HostSeamsIncomplete(RuntimeError):
    """The pinned openDox leg declares some of phase 1's seams and not others."""


def seams() -> tuple[tuple[Any, str, Any], ...]:
    """Every seam this host fills, as `(module, registration call, what it
    registers)`, in the order `register_openxfactory()` registers them.

    Resolved on the call, like everything else here that lives at a pinned
    leg. Importing these modules adds nothing that reaches `sys.path`
    (see "EACH IMPLEMENTATION IS RESOLVED WHEN IT IS CALLED" above).
    """
    from ideation_dashboard import doxbench_status_exemption
    from opendox import corpus_adapter, doxbench_packet, serve_wire, workbench

    return (
        (corpus_adapter, "register_home", home_corpus),
        (workbench, "register_session_notebook_scope", SESSION_NOTEBOOK_SCOPE),
        (workbench, "register_health_check", scoped_doc_health),
        (serve_wire, "register_doxbench_validators", doxbench_validators),
        (doxbench_packet, "register_status_exemption", doxbench_status_exemption),
    )


def _seam_name(module: Any, call: str) -> str:
    return f"{module.__name__}.{call}"


def register_seams() -> tuple[str, ...]:
    """Fill every seam the pinned openDox leg declares. Returns the calls made.

    ALL OR NONE, AND NONE IS A LEG, NOT A GAP. A pinned leg that predates
    plan 034's phase 1 declares none of the five calls: its reaches still
    import this repository's packages by name, and `carved_reach.install()`
    has put them on the path, so there is nothing to register and nothing is.
    A leg that declares some and not the others is refused, naming the
    missing calls: no pin names such a leg, since the phase-1 seams arrive at
    the one openDox-code commit a phase pins (plan 034 § "Pins and landing
    order"), and filling only some of them would leave a hosted request
    reading this repository's code through some seams and meeting an empty
    seam's refusal, or openDox's own default, at the rest.

    Each call's own refusal reaches the caller unchanged: a DIFFERENT object
    already registered is the split every seam refuses, and it is not
    swallowed here.
    """
    declared = seams()
    missing = [_seam_name(module, call) for module, call, _ in declared
               if not callable(getattr(module, call, None))]
    if len(missing) == len(declared):
        return ()
    if missing:
        raise HostSeamsIncomplete(
            f"the pinned openDox leg declares only some of the seams "
            f"openxFactory fills: {missing} are missing. The five arrive "
            "together, at the openDox-code commit plan 034's phase 1 pins "
            "(T020, T025, T026, T027), so a leg with some of them is a pin "
            "between those landings. Filling only the ones present would "
            "leave hosted requests reaching openxFactory's code through "
            "some seams and an empty seam, or openDox's own default, at the "
            "others. Pin a leg that carries all five, or one that carries "
            "none; see contracts/opendox-pin.yaml.")
    for module, call, implementation in declared:
        getattr(module, call)(implementation)
    return tuple(_seam_name(module, call) for module, call, _ in declared)


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

    THEN IT ASSERTS THE REGISTRATION, AND FILLS THE SEAMS (plan 034 T046). Once
    `register()` has returned, the registry must answer the composite, or
    `HostProfileNotRegistered` is raised (R1Q4 (a)). A process that built a
    parser or a server from openDox's own default before calling this is
    refused earlier, by `register()` itself (R1Q3 (ii)), and that
    `AlreadyRegistered` is not swallowed either. Then `register_seams()` fills
    every seam the pinned leg declares, after the profile and never before it,
    so a refused profile leaves no seam written. Each seam's registration is
    idempotent for the object this module registers, so the second call is a
    no-op there too.

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

    registered = registry.register(composite)

    # THE HOST ASSERTS ITS OWN REGISTRATION (R1Q4 (a), `#656` comment
    # `5817152735`). `register()` replaces openDox's default while nothing has
    # been built from it and refuses once something has (R1Q3 (ii)), so after
    # it returns the registry should answer the composite. Checked, not
    # assumed: a registry that answered anything else would leave this
    # process serving openDox's own default with none of openxFactory's
    # routes, which looks exactly like a working server.
    answered = registry.current()
    if answered is not composite:
        raise HostProfileNotRegistered(
            "opendox.domain_profile.register() accepted openxFactory's "
            "profile, and opendox.domain_profile.current() answers "
            f"{type(answered).__name__} instead, so this process would compose "
            "from a profile that is not openxFactory's. R1Q4 (a) has the host "
            "assert its own registration at its start, and this is that "
            "assertion refusing.")

    register_seams()
    return registered
