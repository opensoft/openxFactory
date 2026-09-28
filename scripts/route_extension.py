"""The route extension point: how a layer above the app server CONTRIBUTES a
route instead of forking the server (`split-opendox-two-layer-product` § 2.4,
design § D2).

WHAT THIS EXISTS TO PREVENT, in D2's own words: the app server "cannot be split
last" because one file carries the app server AND the corpus server, and the
layer above "CONTRIBUTES snapshot, `/source` and projection routes through an
EXTENSION POINT" the app server exposes. "Without the extension point the
integration layer forks the server, which is a fork rather than a profile and
breaks the same rule `domain-descendant-boundary` applies one level down" — that
rule being *A descendant carries profile, never fork*: "anything the profile
cannot express SHALL be an UPSTREAM change in the product repository, released
and re-pinned, rather than a local edit". A contributed route is the profile;
a second copy of the dispatch is the fork.

WHY THIS MODULE SITS AT THE TOP OF `scripts/` AND BELONGS TO NEITHER PACKAGE.
The same three justifications `corpus_adapter.py` records, unchanged: BOTH sides
of the eventual carve consume it (the app server declares the point, the layer
above declares bindings against it); it travels with the carve, to a repository
where the checker package does not exist; and it therefore imports NOTHING from
either package — stdlib and `typing` only, which is a property a test asserts by
PARSING (`tests/ideation-dashboard/test_route_extension.py`, over
`tests/import_scan.py`) rather than an accident of the current body.

WHY A `runtime_checkable` `Protocol` AND NOT AN ABC. An ABC forces
`class X(RouteExtension)`, and an extension authored in the repository that will
pin this one must be able to conform WITHOUT importing anything from here —
structural conformance is the property the seam exists for, and nominal
conformance would make the seam exactly the dependency it was drawn to remove.
House precedent: `corpus_adapter.CorpusAdapter`,
`doxbench_model.WorkbenchModelPort`.

CLOSED MEMBERSHIP, ONE MEMBER, AND IT IS A METHOD. `MEMBERS` is the closure a
companion test reads `RouteExtension.__protocol_attrs__` against, so the surface
cannot grow a second verb by accident. A `runtime_checkable` Protocol with a
non-method member supports `isinstance()` but not `issubclass()`; the single
member here is a method, so both work, and the test pins that rather than
trusting it.

THE LOAD-BEARING CONSTRAINT: A CONTRIBUTED ROUTE IS NOT A PRIVILEGED ROUTE.
`RouteBinding.handler` is the NAME of a method, dispatched `getattr(handler_obj,
binding.handler)` against the LIVE request handler — never a free function
handed a stripped request object, and never a callable the binding carries. That
is deliberate and it is the whole safety argument: a contributed route reaches
the request through the SAME OBJECT every core route reaches it through, so the
SAME PRIMITIVES are REACHABLE to it — the loopback verdict, the capability
dict, the resolved actor, the console-host and console-token checks, the
session repository. That is a reachability guarantee, not an enforcement one:
nothing here calls `self.loopback` (or any other gate) on a contributed
handler's behalf, exactly as nothing calls it on a core route's behalf either
— every core WRITE route checks it itself, as its first statement (e.g.
`serve.py`'s `_handle_notebook_action`). A correctly written extension checks
the same way a core route does, because it is handed the same object to check
it on; a contributed POST handler that skips its own `self.loopback` check
executes off-loopback exactly as a core write route that skipped it would. It
is the direct analogue of `corpus-adapter-seam` requirement 4, "no privileged
route", and of the scan
`tests/corpus-adapter/test_no_privileged_route.py` keeps over the home corpus.

A binding therefore cannot introduce a handler the server does not already have.
That is not a limitation to be worked around later: it is the invariant. The
extraction PRs that follow move handler methods onto the handler class and
declare bindings for them; they do not gain a way to attach a callable at
request time, because a callable attached at request time is precisely the
privileged route this shape forbids.

WHERE A CONTRIBUTED ROUTE'S METHODS COME FROM: THE HANDLER-CONTRIBUTION FACET
(R1Q1 (a), Brett Heap, openxFactory#656 comment 5817152735). The invariant
above carried a consequence it did not state. If a binding may only name a
method the handler class already has, then the class a column's methods live
on had to be one of the handler's BASES, written where the core handler is
written. That is how a descendant's own column came to be a base of openDox's
core handler, and with it an import-time reach into a package openDox can
never have.

So the class the server binds is COMPOSED at build time rather than written at
import time. A host profile, or a route extension, MAY declare
`HANDLER_CONTRIBUTIONS`, the mixin classes that hold the methods its bindings
name. The server reads the facet off the profile and off every extension it
collected bindings from. `collect_handler_contributions` checks the mixins
against the core handler class, and `compose_handler` builds the bound class
with the core handler FIRST among its bases and the contributions after it.
`resolve_handlers` is unchanged, and it runs after the composition. So every
binding is still checked against the class that will dispatch it, and a
binding still cannot introduce a handler: the method must be on the composed
class before the server binds. That class is composed ONCE, at wiring time,
and never at request time. No core module names a contributor, because each
contributor names itself, on its own profile or extension.

A CONTRIBUTION MAY ONLY ADD. It is refused with the same `RouteBindingError`
wherever it would do more:
  * a name the core handler already resolves. Replacing a core method is the
    fork this module exists to prevent. A contributed method that the core
    shadows is worse: its binding would dispatch the core's method, silently;
  * a name the core handler sets on its INSTANCES (the request path, the
    output stream, the headers), which no class's `dir()` lists. These names
    are measured at wiring time from the source of every class in the core's
    MRO. Each method's assignments are read through ITS receiver, the first
    positional parameter, whatever it is called: `self.<name> = ...`, and
    `setattr(self, "<name>", ...)` with a literal name. A `staticmethod` has no
    receiver, and a nested class's methods receive that class's instances, so
    neither is read. The instance's own attribute takes precedence over a
    contributed method, so a binding naming one would pass `resolve_handlers`,
    which looks on the class, and then dispatch the core's value. Core code
    that probes such a name before it sets it (`hasattr(self,
    "_headers_buffer")`) would find the contribution instead. A class whose
    source cannot be read (`object`, a class built at run time) contributes no
    measured names;
  * a name another contribution also defines. Which of the two answered would
    be decided by assembly order, the accident `collect_bindings` refuses to
    depend on;
  * a dunder beyond the ones a `class` statement writes by itself, which
    include `__orig_bases__` where a base resolved through `__mro_entries__`.
    `__getattr__`, `__getattribute__`, `__init__` and their kin reach the
    OBJECT PROTOCOL, which is why `RouteBinding` refuses a dunder handler name.
    A contributed `__getattribute__` would sit in front of every gate the core
    reads off `self`;
  * a DATA DESCRIPTOR: a `property`, a named slot, anything whose type defines
    `__set__` or `__delete__`. A data descriptor takes precedence over an
    instance's own attributes, so it would intercept the core's per-instance
    state under its name, including state set in a way the measurement above
    cannot read. A contribution holds METHODS. The bookkeeping names are
    exempt from the dunder rule by name, so their VALUES are checked too: a
    data descriptor under one is refused unless the core answers that name
    itself, ahead of it in the MRO;
  * a DESCRIPTOR THAT IS NOT A METHOD: anything whose type defines `__get__`
    and is not exactly a function, a `staticmethod` or a `classmethod`, such
    as a `functools.cached_property` or a `__get__` of the contribution's own.
    Python binds those three the same way on the class and on an instance,
    and `resolve_handlers` checks each binding on the class. Any other
    descriptor may answer the two differently, so its binding could pass at
    wiring time and fail at request time;
  * a METACLASS other than the core handler's own, or one it derives from. The
    composed class would take it, and a metaclass decides how the class itself
    is called, compared, hashed and asked for a name. A metaclass whose
    `__getattr__` answered any name would pass `resolve_handlers`, which looks
    each binding's method up on the class, for a method no instance has;
  * an ancestor it shares with the core handler, other than `object`. So
    composing it can never reorder the core's MRO, which stays a prefix of the
    composed class's own;
  * a declaration that is not a plain TUPLE of classes (a set's order would
    hang on hashing, a generator would compose nothing on a second build, and
    a tuple subclass may iterate however it likes), a class declared twice, or
    classes `type()` cannot compose at all. That last one
    `collect_handler_contributions` finds by composing once, before the build
    does its expensive work.

Classes are compared by IDENTITY throughout, never by hash or equality, which
belong to a class's metaclass. Every refusal names what it refuses through a
formatter that cannot raise, since a contributor is an object this module
cannot vet. The checks bound what a contribution does to the composed class.
They are not a sandbox: a contributor is host code, running in the same
process.

The facet is OPTIONAL, and its absence is not a defect: a profile or an
extension that declares none contributes no mixin, and the server binds the
core handler alone. It is read by PRESENCE, as `opendox.view_extension` reads
`VIEW_EXTENSIONS`: an absent facet and a declared `None` both contribute
nothing, and any other value is a declaration, refused if it is malformed.

CORE ARMS ARE CONSULTED FIRST, so a contributed route can never SHADOW a core
one. The app server's fixed dispatch runs to completion before these bindings
are consulted, and the fallback (static serve on a read, "unknown action" on a
write) runs after. A binding that duplicates a core pattern is simply never
reached — silently unreachable rather than silently overriding, which is the
safe direction of that failure.

AMONG BINDINGS, EXACT BEFORE PREFIX, THEN DECLARATION ORDER. With several
independent extensions the order of the tuple is an accident of whatever
assembled it, and a broad prefix from the first extension must not swallow an
exact route from the second. `collect_bindings` therefore returns every exact
binding first, each group in declaration order, and `match` takes the first hit.
Since the overlap refusal below, no two bindings can both answer one live
request at all, so this grouping no longer decides anything a refusal has not
already prevented — it is kept as defence in depth, and because the consult
order is observable and pinned.

AND NO OVERLAP AT ALL: A PATTERN THAT SITS UNDER A DECLARED PREFIX IS REFUSED
(Brett Heap's RULING A, 2026-09-07, over Copilot review `PRRT_kwDOTAvnrs6f_iG1`
on PR #761). Ordering exact ahead of prefix decides a tie; it does not make the
tie SAFE. A prefix is where a column puts the gating its whole subtree shares —
`ACTIONS_GATE_PREFIX` carries the gate console's loopback, capability, actor
and human-console refusals; `SOURCE_PREFIX` carries the containment check — so
an EXACT binding declared under one wins the match and takes that single path
OUT of the prefix's hands, and the prefix's handler never runs for it. That is
a hijack of another column's gating rather than an extension of it, and it is
precisely the profile-vs-fork boundary the § 3 carve puts a REPOSITORY boundary
on. `collect_bindings` therefore refuses any pattern that sits under an
already-declared prefix pattern (`str.startswith` — the dispatcher's own test,
`RouteBinding.matches`), in EITHER declaration order, with the same
`RouteBindingError` a literal duplicate raises. Method-aware on the same slot
rule the duplicate check uses (`_claimed_collision_keys`): a POST exact under a
POST prefix collides; a GET and a HEAD binding collide, because a GET binding
answers HEAD; a GET exact under a POST prefix does NOT, because no live request
is ever offered to both.

TWO CONSEQUENCES OF READING "UNDER" AS `startswith`, both deliberate. An exact
pattern EQUAL to a prefix minus its trailing slash is NOT under it —
`"/source".startswith("/source/")` is False, and no request path reaches both —
so the in-tree projection column's `/source` + `/source/` pair stays legal and
this assembly still builds. That pair is why the test is `startswith` on the
raw patterns and not a segment-wise one. And NESTED PREFIXES are refused too,
decided on evidence rather than symmetry: the in-tree profile declares exactly
two prefixes, POST `/actions/gate/` and GET `/source/`, and neither sits under
the other, so no legitimate declaration needs the case — while which of two
nested prefixes answered a path they both cover would be settled by the
assembly order this module refuses to depend on, leaving the loser silently
unreachable across its whole subtree. Fail closed: the day a real declaration
needs nesting it can be admitted with a rule and a test, rather than inherited
by accident.

A ROUTE THAT CANNOT BE SERVED MUST NOT START. `resolve_handlers` is called at
WIRING time, against the handler class the server is about to bind, and raises
`RouteBindingError` naming the binding whose method does not resolve. Discovering
a typo'd handler name on the first request — as a stack trace on a live
connection — is the failure this converts into a refusal at build.

FOUR CALL SHAPES, MIRRORING THE CORE ARMS EXACTLY, so an extracted route needs no
signature change:

  * read, exact:  `handler(head_only)`
  * read, prefix: `handler(remainder, head_only)`
  * write, exact: `handler()`
  * write, prefix:`handler(remainder)`

`remainder` is the path with the prefix removed — what the core prefix arms
compute inline today.

A "GET" BINDING ANSWERS BOTH GET AND HEAD, because every core read arm does: one
dispatch, a `head_only` flag, one body-suppression decision. "HEAD" is declarable
for a binding that answers HEAD alone; it exists so the vocabulary can express
that, not because anything needs it yet.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

#: The closed member set. A companion test reads
#: `RouteExtension.__protocol_attrs__` against this tuple, so growing the
#: surface is a two-file act somebody has to mean.
MEMBERS: tuple[str, ...] = ("routes",)

#: The request methods a binding may declare. "GET" answers GET and HEAD both
#: (see the module docstring); "HEAD" answers HEAD alone; "POST" answers POST.
#: Deliberately small: a method this dispatch has no arm for cannot be honoured,
#: and a binding that silently never fires is worse than one that refuses.
METHODS: tuple[str, ...] = ("GET", "HEAD", "POST")


class RouteBindingError(ValueError):
    """A binding that cannot be served, refused where it is DECLARED or WIRED.

    One exception for every wiring defect in this module — a malformed binding,
    a duplicate, an extension that does not conform, a handler name that does
    not resolve, a handler contribution that cannot be composed — because a
    caller does nothing different for any of them: they are all "this server
    must not start".
    """


@dataclass(frozen=True)
class RouteBinding:
    """One contributed route: a method, a path, and the NAME of the handler.

    Frozen, and validated where it is constructed rather than where it is
    dispatched: a binding is declared once at import time and consulted on every
    request, so the cheap place to find a malformed one is the first.
    """

    method: str      #: one of METHODS
    pattern: str     #: the exact path, or the prefix, always rooted at "/"
    is_prefix: bool  #: True where `pattern` is a prefix and the rest is the handler's
    handler: str     #: the name of a method ON THE REQUEST HANDLER — never a callable

    def __post_init__(self) -> None:
        if self.method not in METHODS:
            raise RouteBindingError(
                f"route binding method {self.method!r} is not one of "
                f"{list(METHODS)} (pattern {self.pattern!r})")
        if not isinstance(self.pattern, str) or not self.pattern.startswith("/"):
            raise RouteBindingError(
                f"route binding pattern {self.pattern!r} must be a path rooted "
                "at '/'")
        if "?" in self.pattern or "#" in self.pattern:
            # The dispatcher strips the query and the fragment before matching,
            # so a pattern carrying either could never fire — a binding that can
            # never match is a defect, not a no-op.
            raise RouteBindingError(
                f"route binding pattern {self.pattern!r} must carry no query or "
                "fragment: the dispatcher matches the path alone")
        if not isinstance(self.is_prefix, bool):
            raise RouteBindingError(
                f"route binding is_prefix must be a bool, got {self.is_prefix!r} "
                f"(pattern {self.pattern!r})")
        if self.is_prefix and not self.pattern.endswith("/"):
            # Both core prefixes end in "/" and that is not cosmetic: without it
            # "/sourceless" matches the "/source" prefix and the remainder is a
            # fragment of a sibling route's name.
            raise RouteBindingError(
                f"route binding prefix {self.pattern!r} must end with '/' so the "
                "remainder is a whole path segment")
        if not isinstance(self.handler, str) or not self.handler.isidentifier():
            raise RouteBindingError(
                f"route binding handler {self.handler!r} must be the NAME of a "
                f"method on the request handler (pattern {self.pattern!r})")
        if self.handler.startswith("__"):
            # A name dispatched by string must be a plain method name. A dunder
            # reaches the object protocol rather than the server's own surface,
            # and nothing legitimate needs one.
            raise RouteBindingError(
                f"route binding handler {self.handler!r} must not be a dunder: "
                "a contributed route dispatches a method of the server, not the "
                "object protocol")

    @property
    def key(self) -> tuple[str, str, bool]:
        """What makes two bindings the SAME route — never the handler.

        Two bindings that claim one (method, pattern, shape) are a collision
        whichever handlers they name: the second is unreachable, and an
        unreachable route that looks declared is the defect
        `collect_bindings` refuses.
        """
        return (self.method, self.pattern, self.is_prefix)

    def matches(self, method: str, path: str) -> bool:
        """Whether this binding answers `method` for `path`.

        `method` is the REQUEST's method. A "GET" binding answers a HEAD request
        too, exactly as every core read arm does.
        """
        if self.method == method:
            pass
        elif self.method == "GET" and method == "HEAD":
            pass
        else:
            return False
        if self.is_prefix:
            return path.startswith(self.pattern)
        return path == self.pattern

    def remainder(self, path: str) -> str:
        """The path with the prefix removed — "" for an exact binding.

        The same slice the core prefix arms compute inline
        (`path[len(PREFIX):]`), computed once here so an extracted route keeps
        the argument it already takes.
        """
        return path[len(self.pattern):] if self.is_prefix else ""


@runtime_checkable
class RouteExtension(Protocol):
    """One method. Nothing else, ever — see `MEMBERS`."""

    def routes(self) -> tuple[RouteBinding, ...]:
        """Every route this extension contributes, in its own declared order.

        Called ONCE at wiring time, never per request: the set of contributed
        routes is a property of how the server was assembled, and an extension
        that answered differently on a later call would make the dispatch table
        unreadable — which is the thing the extraction is for.
        """


def _claimed_collision_keys(binding: RouteBinding) -> tuple[tuple[str, str, bool], ...]:
    """Every collision-check key `binding` ANSWERS, not just its own `.key`.

    A "GET" binding answers a live HEAD request too (`RouteBinding.matches`,
    module docstring), so a "GET" binding and a "HEAD" binding at the same
    (pattern, is_prefix) both answer a HEAD request — the same unreachable-
    route defect `collect_bindings` already refuses for two identical keys,
    just reached through the request method the SECOND binding never
    receives. Checking (and recording) only the literal key would miss it in
    either declaration order, so a "GET" binding also claims the "HEAD" slot
    and a "HEAD" binding also claims the "GET" slot; "POST" claims only itself
    — nothing answers a live POST but a "POST" binding.
    """
    keys = (binding.key,)
    if binding.method == "GET":
        keys += (("HEAD",) + binding.key[1:],)
    elif binding.method == "HEAD":
        keys += (("GET",) + binding.key[1:],)
    return keys


def _claimed_methods(binding: RouteBinding) -> tuple[str, ...]:
    """Every request method `binding` ANSWERS — the METHOD half of
    `_claimed_collision_keys`, derived from it rather than restated.

    The containment refusal asks the same GET/HEAD question the key-equality
    refusal asks, but about a PAIR OF PATTERNS rather than one slot, so it
    needs the methods without the patterns. Taking them from
    `_claimed_collision_keys` keeps ONE place where "a GET binding also answers
    HEAD" is written down; a second copy of that rule is exactly the drift that
    would let one refusal fire and the other not.
    """
    return tuple(key[0] for key in _claimed_collision_keys(binding))


def _share_a_method_slot(one: RouteBinding, other: RouteBinding) -> bool:
    """Whether one live request could ever be offered to BOTH bindings."""
    return bool(set(_claimed_methods(one)) & set(_claimed_methods(other)))


def _sits_under(outer: RouteBinding, inner: RouteBinding) -> bool:
    """Whether `outer` is a PREFIX binding whose pattern covers `inner`'s.

    Plain `str.startswith`, which is the dispatcher's OWN test for a prefix hit
    (`RouteBinding.matches`) — so this asks the question the live dispatch
    asks, not a second, approximate one. Note what it therefore does NOT call a
    containment: an exact `/source` does not sit under the prefix `/source/`,
    because `"/source".startswith("/source/")` is False and no request path
    ever reaches both. That pair is the in-tree projection column's own
    declaration and must keep building.
    """
    return outer.is_prefix and inner.pattern.startswith(outer.pattern)


def _overlapping_previous(binding: RouteBinding, accepted):
    """The first already-accepted binding that OVERLAPS `binding`, as
    `(outer, inner)` — the prefix and what sits under it — or None.

    Scanned in declaration order and in BOTH directions, because the ruling is
    order-independent: the prefix may have been declared first (a later exact
    route sits under it) or second (it swallows an exact route already
    declared), and either way one of the two is reached for a path the other
    was declared to answer.
    """
    for previous in accepted:
        if not _share_a_method_slot(previous, binding):
            continue
        if _sits_under(previous, binding):
            return previous, binding
        if _sits_under(binding, previous):
            return binding, previous
    return None


def _containment_message(outer: RouteBinding, inner: RouteBinding) -> str:
    """Name BOTH bindings by their OWN declared method and pattern — the same
    discipline `_collision_message` keeps, for the same reason: a message that
    borrowed a method from whichever slot matched would misreport a HEAD
    binding as a GET one.
    """
    slot = (f"{inner.method} {inner.pattern!r} (prefix={inner.is_prefix}) sits "
            f"under the {outer.method} prefix {outer.pattern!r}")
    if outer.method != inner.method:
        slot += (" — a GET binding answers HEAD too, so one live request is "
                 "offered to both")
    if inner.is_prefix:
        because = (
            "Which of two NESTED prefixes answers a path they both cover would "
            "be decided by the order the extensions happened to be assembled "
            "in — the accident this module refuses to depend on — leaving the "
            "loser unreachable across the whole of the other's subtree.")
    else:
        because = (
            "Every exact binding is consulted before every prefix one, so the "
            "exact route would take that one path OUT of the prefix's hands, "
            "and a prefix is where a column puts the gating its whole subtree "
            "shares — this is a hijack of that gating, not an extension of "
            "it.")
    return (f"{slot}: {inner.handler!r} and {outer.handler!r}. {because} "
            "Declare a pattern that does not sit under another binding's "
            "prefix.")


def _collision_message(previous: RouteBinding, current: RouteBinding) -> str:
    """Name each colliding binding by ITS OWN declared method — never a
    method borrowed from whichever collision key happened to match.

    Reporting `claimed_key[0]` (the SLOT that matched) rather than each
    binding's actual `.method` made a GET/HEAD collision misreport itself as
    "two route bindings claim GET", even where the second binding was
    declared HEAD, not GET — Copilot review, `PRRT_kwDOTAvnrs6fwTVh`,
    `scripts/route_extension.py:296`. `previous` is captured whole (not just
    its handler name) so this can always name what it actually was.
    """
    if previous.method == current.method:
        claim = f"two route bindings claim {previous.method} {current.pattern!r}"
    else:
        # The only cross-method collision this module has: a "GET" binding
        # already answers HEAD (`_claimed_collision_keys`), so a "GET" and a
        # "HEAD" binding at the same (pattern, is_prefix) both answer a live
        # HEAD request even though neither is declared as the other.
        claim = (f"{previous.method} {previous.pattern!r} and {current.method} "
                  f"{current.pattern!r} claim the same GET/HEAD slot")
    return (
        f"{claim} (prefix={current.is_prefix}): {previous.handler!r} and "
        f"{current.handler!r}. The second could never be reached, and a "
        "route that looks declared and never fires is worse than one that "
        "refuses.")


def collect_bindings(extensions) -> tuple[RouteBinding, ...]:
    """Flatten the extensions into ONE consult order, refusing what cannot serve.

    Refuses an object that does not conform, a `routes()` that yields anything
    but `RouteBinding`s, and two bindings claiming one route — the last being
    the collision that would otherwise leave a declared route silently
    unreachable. A "GET" binding and a "HEAD" binding at the same (pattern,
    is_prefix) collide too, because a "GET" binding already answers HEAD
    (`_claimed_collision_keys`) — the "HEAD" binding would never be reached on
    the one request method it exists to answer.

    AND REFUSES A PATTERN THAT SITS UNDER AN ALREADY-DECLARED PREFIX, in either
    declaration order (RULING A, 2026-09-07 — the module docstring carries the
    argument in full). An EXACT binding beats a PREFIX one in `match`, so an
    exact route declared under a contributed prefix would take that one path
    out of the prefix's hands and the prefix's handler — the gate console's
    loopback/capability/actor/human-console refusals, `/source/`'s containment
    check — would never run for it: a hijack of the gating a column put on its
    whole subtree, and unlike a literal duplicate it fails OPEN rather than
    loudly. Two nested PREFIXES are refused on the same rule, because which one
    answers a path they both cover is otherwise decided by assembly order.
    Method-aware exactly as the duplicate check is (`_share_a_method_slot`), so
    a GET exact under a POST prefix is legal — nothing offers one live request
    to both — and an exact pattern equal to a prefix minus its trailing slash
    is NOT under it, which is what keeps this assembly's own `/source` +
    `/source/` pair legal.

    Returns every exact binding first and every prefix binding after, each group
    in declaration order, for the reason the module docstring gives: tuple order
    across independent extensions is an accident, and a prefix must not swallow
    a sibling's exact route because of it.
    """
    exact: list[RouteBinding] = []
    prefix: list[RouteBinding] = []
    #: Every binding accepted so far, in DECLARATION order — what the
    #: containment check scans. Kept beside `seen` rather than derived from
    #: `exact + prefix`, so the binding a refusal names is the one that was
    #: actually declared first.
    accepted: list[RouteBinding] = []
    #: The FULL previous binding, not just its handler name — so a collision
    #: message can name what the previous binding was actually DECLARED as
    #: (`_collision_message`), rather than the collision-check key that
    #: happened to match, which is not always the previous binding's own
    #: method.
    seen: dict[tuple[str, str, bool], RouteBinding] = {}
    for extension in extensions:
        if not isinstance(extension, RouteExtension):
            raise RouteBindingError(
                f"{extension!r} does not conform to RouteExtension: it must "
                f"declare {list(MEMBERS)}")
        declared = extension.routes()
        for binding in declared:
            if not isinstance(binding, RouteBinding):
                raise RouteBindingError(
                    f"{extension!r} contributed {binding!r}, which is not a "
                    "RouteBinding")
            for claimed_key in _claimed_collision_keys(binding):
                previous = seen.get(claimed_key)
                if previous is not None:
                    raise RouteBindingError(_collision_message(previous, binding))
            # AFTER the exact-key check, so a literal duplicate keeps reporting
            # itself as a duplicate: two identical patterns also "sit under"
            # each other, and the narrower message is the truer one.
            overlap = _overlapping_previous(binding, accepted)
            if overlap is not None:
                raise RouteBindingError(_containment_message(*overlap))
            seen[binding.key] = binding
            accepted.append(binding)
            (prefix if binding.is_prefix else exact).append(binding)
    return tuple(exact) + tuple(prefix)


# ---------------------------------------------------------------------------
# THE HANDLER-CONTRIBUTION FACET (R1Q1 (a)). The module docstring carries the
# argument; what follows is the mechanism and its refusals.
# ---------------------------------------------------------------------------

#: The OPTIONAL attribute under which a host profile or a route extension
#: declares the mixin classes its bindings' methods live on: a tuple of
#: classes. Absent, or `None`, declares none.
HANDLER_FACET = "HANDLER_CONTRIBUTIONS"

#: How much of a `repr` a refusal quotes before it stops being read.
_NAME_LIMIT = 120


def _is_dunder(name: str) -> bool:
    return len(name) > 4 and name.startswith("__") and name.endswith("__")


def _is_class(obj) -> bool:
    """Whether `obj` is a class, decided by its REAL type. `isinstance` would
    also consult the `__class__` the object reports, which an object this
    module cannot vet may make raise."""
    return issubclass(type(obj), type)


def _is_one_of(obj, candidates) -> bool:
    """Membership by IDENTITY. A class's hash and equality belong to its
    metaclass, and a contributed class may have one that refuses both."""
    return any(candidate is obj for candidate in candidates)


def _is_data_descriptor(value) -> bool:
    """A `property`, a named slot, or anything else whose type defines
    `__set__` or `__delete__`: an attribute that takes precedence over an
    instance's own."""
    return any("__set__" in vars(kind) or "__delete__" in vars(kind)
               for kind in type(value).__mro__)


#: The descriptors a contribution may carry. Python binds these three the same
#: way whether they are looked up on the class or on an instance, so a
#: binding checked on the class is dispatched as checked. The test is on the
#: EXACT type, because a subclass may define a `__get__` of its own.
_METHOD_KINDS = (type(_is_dunder), staticmethod, classmethod)


def _is_foreign_descriptor(value) -> bool:
    """A descriptor other than a method: its type defines `__get__`, and it is
    not exactly a function, a `staticmethod` or a `classmethod`."""
    return (not _is_one_of(type(value), _METHOD_KINDS)
            and any("__get__" in vars(kind) for kind in type(value).__mro__))


def _receiver_targets(node, receiver: str) -> set[str]:
    """The names a syntax tree assigns on `receiver`: plain, augmented,
    annotated and unpacked assignment, a `for` or `with` target, and
    `setattr(<receiver>, "<name>", ...)` with a literal name."""
    import ast   # local, like the measurement's other imports: see below

    names: set[str] = set()
    for node in ast.walk(node):
        if isinstance(node, ast.Assign):
            targets = list(node.targets)
        elif isinstance(node, (ast.AugAssign, ast.AnnAssign, ast.For,
                               ast.AsyncFor)):
            targets = [node.target]
        elif isinstance(node, ast.withitem) and node.optional_vars is not None:
            targets = [node.optional_vars]
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "setattr" and len(node.args) >= 2 \
                and isinstance(node.args[0], ast.Name) \
                and node.args[0].id == receiver \
                and isinstance(node.args[1], ast.Constant) \
                and isinstance(node.args[1].value, str):
            names.add(node.args[1].value)
            continue
        else:
            continue
        while targets:
            target = targets.pop()
            if isinstance(target, (ast.Tuple, ast.List)):
                targets.extend(target.elts)
            elif isinstance(target, ast.Starred):
                targets.append(target.value)
            elif isinstance(target, ast.Attribute) \
                    and isinstance(target.value, ast.Name) \
                    and target.value.id == receiver:
                names.add(target.attr)
    return names


def _methods(class_node):
    """Each function a class body defines, however conditionally: a `def`
    under an `if` or a `try`, or a `lambda` in a class-level expression. It
    does not descend into a nested class, whose methods receive that class's
    instances, or into a method's own body."""
    import ast

    pending = list(class_node.body)
    while pending:
        node = pending.pop()
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            yield node
        elif not isinstance(node, ast.ClassDef):
            pending.extend(ast.iter_child_nodes(node))


def _decorator_name(decorator) -> str:
    import ast

    while isinstance(decorator, ast.Call):
        decorator = decorator.func
    if isinstance(decorator, ast.Attribute):
        return decorator.attr
    return decorator.id if isinstance(decorator, ast.Name) else ""


def _receiver(method) -> str | None:
    """The name a method's receiver goes by: its first positional parameter,
    WHATEVER it is called. A `staticmethod` has none. A `classmethod`'s is
    the class, and what it assigns there is state as well: a name the core
    sets on its class at run time would replace a contributed one."""
    import ast

    if not isinstance(method, ast.Lambda) and any(
            _decorator_name(decorator) == "staticmethod"
            for decorator in method.decorator_list):
        return None
    params = [*method.args.posonlyargs, *method.args.args]
    return params[0].arg if params else None


def _assigned_by_methods(tree) -> set[str]:
    """The names the methods of the class a source tree defines assign on
    their receivers."""
    import ast

    names: set[str] = set()
    for class_node in (node for node in tree.body
                       if isinstance(node, ast.ClassDef)):
        for method in _methods(class_node):
            receiver = _receiver(method)
            if receiver is not None:
                names |= _receiver_targets(method, receiver)
    return names


#: Each core class measured so far, keyed by `id()` and holding the class, so
#: the key cannot be reused while the entry lives. A class is measured once
#: per process, and a build that composes nothing measures nothing.
_MEASURED: dict[int, tuple[type, frozenset[str]]] = {}


def _assigned_on_self(klass: type) -> frozenset[str]:
    """The names `klass`'s own source assigns on its instances.

    Each method's assignments are read through ITS receiver, the first
    positional parameter, whatever it is called. The measurement reads the
    class's source with `inspect`, so a class whose source cannot be read,
    such as `object` or a class built at run time, measures as assigning
    nothing. The imports are local: `inspect` is not small, and only a build
    that composes a contribution needs it.
    """
    held = _MEASURED.get(id(klass))
    if held is not None and held[0] is klass:
        return held[1]
    import ast
    import inspect
    import textwrap

    try:
        tree = ast.parse(textwrap.dedent(inspect.getsource(klass)))
    except (OSError, TypeError, SyntaxError):
        names = frozenset()
    else:
        names = frozenset(_assigned_by_methods(tree))
    _MEASURED[id(klass)] = (klass, names)
    return names


def _instance_state(base: type) -> dict[str, type]:
    """Each name the classes of `base`'s MRO assign on their instances,
    mapped to the first of them in MRO order that does, so a refusal can name
    it."""
    state: dict[str, type] = {}
    for klass in base.__mro__:
        for name in sorted(_assigned_on_self(klass)):
            state.setdefault(name, klass)
    return state


class _ClassStatementBookkeeping:
    """Never composed. It exists to be asked, once at import, which dunders a
    `class` statement writes into a class namespace BY ITSELF on the running
    interpreter.

    Measuring the set keeps the refusal of object-protocol names from carrying
    a list that a later Python release adds to. 3.13, for one, added
    `__firstlineno__` and `__static_attributes__` to every class. The
    annotation and the instance store below are there so that the entries
    those two features write are included.
    """

    probe: int

    def _probe(self) -> None:
        self.probe = 0


class _ResolvedRoot:
    """The class `_ResolvedBookkeeping`'s base resolves to."""


class _ResolvesToRoot:
    """A base that is not a class. It resolves to one at class creation
    through `__mro_entries__`, as a generic alias does."""

    def __mro_entries__(self, bases):
        return (_ResolvedRoot,)


class _ResolvedBookkeeping(_ResolvesToRoot()):
    """Never composed. It is the second measurement: which dunders a `class`
    statement writes BY ITSELF when a base was resolved. That is
    `__orig_bases__`, the record of the bases as written. It is kept apart
    from the probe above, because a base of its own would move `__dict__` and
    `__weakref__` off the class being measured."""


#: The dunders a mixin carries because it IS a class, not because it asked for
#: behaviour: the bookkeeping the two probes measure, plus two names no probe
#: can measure alone.
#: * `__slots__` declares a layout rather than a hook. An empty one adds
#:   nothing, and a named slot is a data descriptor, refused as one.
#: * `__type_params__` is written by the class statement of a class that
#:   declares type parameters (PEP 695). Such a class always takes
#:   `typing.Generic` as an implicit base, and a probe built that way would
#:   also measure the `__parameters__` that `Generic.__init_subclass__` writes,
#:   which is a hook's work, not bookkeeping. A generic mixin is refused for
#:   `Generic`'s own `__init_subclass__` and `__class_getitem__`. Exempting
#:   this one name keeps that refusal naming the hooks.
_CLASS_BOOKKEEPING = frozenset(
    name for probe in (_ClassStatementBookkeeping, _ResolvedBookkeeping)
    for name in vars(probe) if _is_dunder(name)
) | {"__slots__", "__type_params__"}


def _class_name(obj) -> str:
    if not _is_class(obj):
        return ""
    return f"{str.__str__(obj.__module__)}.{str.__str__(obj.__qualname__)}"


def _given_name(obj) -> str:
    return str.__str__(getattr(obj, "__name__", ""))


def _short_repr(obj) -> str:
    text = str.__str__(repr(obj))
    return text if len(text) <= _NAME_LIMIT else text[:_NAME_LIMIT - 1] + "…"


def _describe(obj) -> str:
    """A contributor's or a contribution's name, for a refusal. NEVER RAISES
    an `Exception`: a refusal that fails while formatting itself replaces the
    reader's problem with a worse one, and a contributor is an object this
    module cannot vet.

    A class says `module.qualname`. Anything else says its `__name__` if it has
    a string one (a profile MODULE), and otherwise its `repr`, truncated. Each
    of those reads runs code the object's own type supplies, so each is tried
    in turn, and a plain `str` is taken from whichever answers. An object that
    none of them can name is described by its type. A lazy profile proxy
    refuses dunder lookups by design, and its `repr` does not resolve the
    profile, so the proxy reaches the `repr` branch.
    """
    for read in (_class_name, _given_name, _short_repr):
        try:
            text = read(obj)
        except Exception:          # noqa: BLE001 — naming must never out-raise
            continue
        if text:
            return text
    try:
        return f"a {str.__str__(type(obj).__name__)}"
    except Exception:              # noqa: BLE001
        return "an object that cannot be named"


def declared_handler_contributions(contributor) -> tuple[type, ...]:
    """What ONE contributor declares under `HANDLER_FACET`.

    Returns `()` when the contributor declares nothing, and the classes when it
    declares some. A malformed declaration is refused: the value must be a
    plain TUPLE of classes. Every refusal names what it was handed through
    `_describe`, so a declaration whose `repr` raises is still refused with
    `RouteBindingError`.

    `contributor` is a host profile (or the lazy proxy over one) or a route
    extension. Nothing about its type is checked, because this module may name
    neither kind: this is the same structural neutrality `RouteExtension`
    keeps. The facet is read with `getattr(..., None)`, and a profile proxy
    that finds the facet missing raises an `AttributeError` subclass, precisely
    so that spelling answers "none".
    """
    declared = getattr(contributor, HANDLER_FACET, None)
    if declared is None:
        return ()
    if type(declared) is not tuple:
        raise RouteBindingError(
            f"{_describe(contributor)} declares {HANDLER_FACET} = "
            f"{_describe(declared)}, which is not a plain tuple of classes. "
            "Declare the mixins as a tuple, even for one: `(Mixin,)`, not "
            "`Mixin`. A list, a set, a generator or a tuple subclass is "
            "refused too. A set would make the composed class's MRO depend on "
            "hashing, a generator would compose nothing the second time a "
            "server is built, and a subclass may iterate however it likes.")
    for item in declared:
        if not _is_class(item):
            raise RouteBindingError(
                f"{_describe(contributor)} declares {_describe(item)} under "
                f"{HANDLER_FACET}, which is not a class. A handler "
                "contribution is a mixin CLASS whose methods a binding names; "
                "it is composed into the class the server binds, so it cannot "
                "be an instance, a function or a name.")
    return declared


def _refuse_an_unsafe_composition(base: type, contributions, *,
                                  namespace=()) -> None:
    """Refuse any contribution that would do more than ADD to `base`.

    The rules are the module docstring's, and so is the argument for each.
    `namespace` holds the class attributes the composed class will carry
    itself; a contributed name that one of them would shadow is refused as
    well.

    The metaclass is checked FIRST, from `type(mixin)` alone, because every
    later read of the mixin (its MRO, its namespace, its name) runs through
    it. Classes are compared by identity throughout (`_is_one_of`).
    """
    core = base.__mro__
    core_metaclasses = type(base).__mro__
    answered = set(dir(base))
    instance_state = _instance_state(base) if contributions else {}
    own_attributes = set(namespace)
    owner: dict[str, type] = {}
    for mixin in contributions:
        if not _is_class(mixin):
            raise RouteBindingError(
                f"{_describe(mixin)} is not a class, so it cannot be composed "
                f"onto {_describe(base)}: a handler contribution is a mixin "
                "CLASS.")
        if not _is_one_of(type(mixin), core_metaclasses):
            raise RouteBindingError(
                f"the handler contribution {_describe(mixin)} is built by the "
                f"metaclass {_describe(type(mixin))}, which is neither the "
                f"core handler {_describe(base)}'s metaclass "
                f"({_describe(type(base))}) nor one it derives from. The "
                "composed class would take that metaclass, and a metaclass "
                "decides how the class itself is called, compared, hashed and "
                "asked for a name: the OBJECT PROTOCOL of the class. One whose "
                "`__getattr__` answered any name would pass `resolve_handlers`, "
                "which looks each binding's method up on the class, for a "
                "method no instance has.")
        if _is_one_of(mixin, core):
            raise RouteBindingError(
                f"the handler contribution {_describe(mixin)} is already in "
                f"{_describe(base)}'s MRO, so declaring it composes nothing. "
                "A declaration that changes nothing is refused, for the "
                "reason a binding that never fires is.")
        chain = [klass for klass in mixin.__mro__ if klass is not object]
        if _is_one_of(base, chain):
            raise RouteBindingError(
                f"the handler contribution {_describe(mixin)} subclasses the "
                f"core handler {_describe(base)}. That makes it a second "
                "handler, not a mixin, and a second handler is a fork of the "
                "core rather than a contribution to it.")
        shared = [klass for klass in chain if _is_one_of(klass, core)]
        if shared:
            raise RouteBindingError(
                f"the handler contribution {_describe(mixin)} shares ancestry "
                f"with the core handler {_describe(base)} "
                f"({[_describe(klass) for klass in shared]}). Composing it "
                "would reorder the core's MRO. A contribution is a plain "
                "mixin, which shares nothing with the core but `object`.")
        hooks = sorted({name for klass in chain for name in vars(klass)
                        if _is_dunder(name) and name not in _CLASS_BOOKKEEPING})
        if hooks:
            raise RouteBindingError(
                f"the handler contribution {_describe(mixin)} defines {hooks}. "
                "A dunder reaches the OBJECT PROTOCOL rather than the server's "
                "own surface, so a contributed one would change how the core "
                "handler itself behaves. That is a privileged route, not a "
                "contributed one, and the reason `RouteBinding` refuses a "
                "dunder handler name.")
        # Class bookkeeping passes the refusal above by NAME, so its VALUE is
        # checked here. Where the core answers a bookkeeping name itself, as
        # it answers `__dict__`, the core's copy precedes the contribution in
        # the MRO and a contributed one is never reached. Where the core does
        # not, a descriptor under that name would answer on every instance.
        reached = [(name, value) for klass in chain
                   for name, value in vars(klass).items()
                   if not (_is_dunder(name) and name in answered)]
        descriptors = sorted({name for name, value in reached
                              if _is_data_descriptor(value)})
        if descriptors:
            raise RouteBindingError(
                f"the handler contribution {_describe(mixin)} defines "
                f"{descriptors} as DATA DESCRIPTORS (a property, a named slot, "
                "anything whose type defines `__set__` or `__delete__`). A data "
                "descriptor takes precedence over an instance's own "
                "attributes, so it would intercept the core handler's "
                "per-instance state under its name, including state set in a "
                "way no wiring-time measurement can read. A contribution holds "
                "METHODS.")
        foreign = sorted({name for name, value in reached
                          if _is_foreign_descriptor(value)})
        if foreign:
            raise RouteBindingError(
                f"the handler contribution {_describe(mixin)} defines "
                f"{foreign} as descriptors that are not methods: each has a "
                "`__get__` of its own, where a contribution may carry only a "
                "function, a `staticmethod` or a `classmethod`. Such a "
                "descriptor may answer the class and an instance differently, "
                "and `resolve_handlers` checks each binding on the CLASS, so a "
                "binding naming one could pass at wiring time and fail at "
                "request time. A contribution holds METHODS.")
        names = {name for klass in chain for name in vars(klass)
                 if not _is_dunder(name)}
        shadowed = sorted(names & answered)
        if shadowed:
            where = ", ".join(
                f"{name} on "
                f"{_describe(next((k for k in base.__mro__ if name in vars(k)), base))}"
                for name in shadowed)
            raise RouteBindingError(
                f"the handler contribution {_describe(mixin)} defines names "
                f"the core handler {_describe(base)} already has ({where}). A "
                "contribution may only ADD a method. Replacing a core method "
                "is the fork this seam exists to prevent. A contributed method "
                "the core shadows is a binding that silently dispatches the "
                "core's method instead of its own.")
        on_instances = sorted(names & set(instance_state))
        if on_instances:
            where = ", ".join(f"{name} by {_describe(instance_state[name])}"
                              for name in on_instances)
            raise RouteBindingError(
                f"the handler contribution {_describe(mixin)} defines names "
                f"the core handler {_describe(base)} sets on each INSTANCE "
                f"({where}, measured from its source). An instance's own "
                "attribute takes precedence over a contributed method, so a "
                "binding naming one would pass `resolve_handlers`, which looks "
                "on the class, and then dispatch the core's value instead. "
                "Core code that probes the name before setting it would find "
                "the contribution. A contribution may only ADD.")
        clashes = sorted(name for name in names if name in owner)
        if clashes:
            first = sorted({_describe(owner[name]) for name in clashes})
            raise RouteBindingError(
                f"the handler contributions {first} and {_describe(mixin)} "
                f"both define {clashes}. Which one answered would be decided by "
                "the order the contributions happened to be assembled in, the "
                "accident `collect_bindings` refuses to depend on.")
        overridden = sorted(names & own_attributes)
        if overridden:
            raise RouteBindingError(
                f"the handler contribution {_describe(mixin)} defines "
                f"{overridden}, which the composed class sets as its own class "
                "attributes. The contributed names would never be reached.")
        for name in names:
            owner[name] = mixin


def _compose(name: str, base: type, contributions: tuple,
             namespace) -> type:
    """`type(name, (base, *contributions), namespace)`, with the `TypeError`
    that `type` raises for an MRO, layout or metaclass conflict converted into
    the module's one refusal."""
    try:
        return type(name, (base, *contributions), dict(namespace))
    except TypeError as exc:
        raise RouteBindingError(
            f"the handler contributions "
            f"{[_describe(mixin) for mixin in contributions]} cannot be "
            f"composed onto {_describe(base)}: {exc}") from exc


def collect_handler_contributions(contributors, *, base: type) -> tuple[type, ...]:
    """Every mixin the contributors declare, in declaration order, checked
    against `base`, the core request-handler class they will be composed onto.

    Called at WIRING time beside `collect_bindings`, and for the same reason: a
    contribution that cannot be composed refuses the build before a socket, a
    checkout read or a session bootstrap. So the checks are not all it runs. It
    also composes the contributions onto `base` ONCE, as a throwaway class, so
    that an MRO or layout conflict that only `type()` can find is found here,
    before any of that work, rather than at the end of the build.

    The same class declared twice is refused, whether one contributor declared
    it twice or two contributors declared it once each: which declaration
    composed it would be an accident of assembly. "The same" is identity,
    never a hash, which a contributed class's metaclass may refuse.

    The composition itself belongs to `compose_handler`, which repeats these
    checks against the class it actually creates.
    """
    declared: list[tuple[type, object]] = []
    for contributor in contributors:
        for mixin in declared_handler_contributions(contributor):
            earlier = [by for seen, by in declared if seen is mixin]
            if earlier:
                raise RouteBindingError(
                    f"the handler contribution {_describe(mixin)} is declared "
                    f"twice, by {_describe(earlier[0])} and by "
                    f"{_describe(contributor)}. Declare each mixin once, beside "
                    "the bindings whose methods it holds.")
            declared.append((mixin, contributor))
    collected = tuple(mixin for mixin, _by in declared)
    _refuse_an_unsafe_composition(base, collected)
    if collected:
        _compose("_ComposabilityPreflight", base, collected, {})
    return collected


def compose_handler(name: str, base: type, contributions, namespace) -> type:
    """The request-handler class a server binds: `base` first, then each
    contribution, carrying `namespace` as its own class attributes.

    `type(name, (base, *contributions), namespace)`, and nothing cleverer. It
    runs after the checks `collect_handler_contributions` makes, repeated here
    because this is the function that creates the class, and a guarantee about
    a class belongs where the class is made. With no contributions it is
    exactly `type(name, (base,), namespace)`, the class a server bound before
    this facet existed. A `TypeError` from `type` itself, such as an MRO or
    layout conflict, is converted into the module's one refusal.

    `contributions` is a plain TUPLE, as `collect_handler_contributions`
    returns it, for the reason the facet is one: the composition must not
    depend on iteration state.
    """
    if type(contributions) is not tuple:
        raise RouteBindingError(
            f"compose_handler takes the contributions as a plain tuple, as "
            f"collect_handler_contributions returns them, not "
            f"{_describe(contributions)}.")
    duplicates = sorted({_describe(mixin)
                         for index, mixin in enumerate(contributions)
                         if _is_one_of(mixin, contributions[:index])})
    if duplicates:
        raise RouteBindingError(
            f"the handler contributions {duplicates} are each listed more "
            "than once. Compose each mixin once.")
    _refuse_an_unsafe_composition(base, contributions, namespace=namespace)
    return _compose(name, base, contributions, namespace)


#: Sentinel distinguishing "no such attribute" from "the attribute is None" —
#: `getattr(..., default)` cannot use `None` itself, several handler-holder
#: seams (`adapter_factory`, `pull_request_factory`, ...) default to `None`.
_UNRESOLVED = object()


def resolve_handlers(bindings, handler_holder) -> None:
    """Refuse, at WIRING time, any binding whose handler does not resolve to a
    CALLABLE attribute of the live handler.

    `handler_holder` is the request-handler CLASS the server is about to bind
    (an instance answers the same `hasattr`/`callable`, and either is accepted —
    this module knows nothing about the shape of the server it serves). A route
    that cannot be served must not start; the alternative is finding the typo —
    or the name of a plain attribute rather than a method — as a stack trace on
    a live connection (`TypeError: '<type>' object is not callable`, raised
    inside the request thread that first matches the binding).

    THIS DOES NOT CHECK CALL SHAPE (a prefix binding is called with the
    remainder the exact form never receives — see the module docstring's FOUR
    CALL SHAPES). `RouteBinding` does not declare which shape its handler
    expects, and the handler's own `inspect.signature` is not a reliable
    stand-in for one: the same handler name can be resolved through the CLASS
    (self still an explicit parameter) or an INSTANCE (self already bound) —
    `resolve_handlers` accepts both by design — and the attribute itself may be
    a plain function, a `staticmethod`, a `classmethod`, or a decorated
    wrapper, each stripping a different set of leading parameters; a handler
    may also default an argument an arm never supplies, or take `*args`.
    Telling a handler that is merely FLEXIBLE about its arguments from one that
    is genuinely the WRONG shape needs signature introspection this module has
    no cheap, reliable way to perform — exactly the heavy validation framework
    this module's neutrality argues against. A wrong-shape handler still fails
    LOUDLY, on the first request that reaches it, with a `TypeError` naming the
    mismatched argument count — a normal Python arity error surfacing on first
    use, not a silent misroute — so this refusal's job is the narrower one a
    build-time check CAN do reliably: a binding whose named attribute does not
    exist at all, or exists but cannot be called (a class attribute, a plain
    field — the crash class this refusal was added for), never starts.
    """
    unresolved = []
    not_callable = []
    for b in bindings:
        resolved = getattr(handler_holder, b.handler, _UNRESOLVED)
        if resolved is _UNRESOLVED:
            unresolved.append(f"{b.method} {b.pattern!r} -> {b.handler}()")
        elif not callable(resolved):
            not_callable.append(
                f"{b.method} {b.pattern!r} -> {b.handler} (resolves to "
                f"{resolved!r}, which is not callable)")
    if unresolved or not_callable:
        clauses = []
        if unresolved:
            clauses.append(
                "route bindings name handlers the request handler does not "
                f"have: {unresolved}")
        if not_callable:
            clauses.append(
                "route bindings name attributes that exist but are not "
                f"callable: {not_callable}. Dispatch is `getattr(self, "
                "binding.handler)()` — a non-callable attribute would crash "
                "the first live request that reaches it with `TypeError: "
                "'<type>' object is not callable`, exactly the failure this "
                "refusal exists to convert into a build-time error")
        raise RouteBindingError(
            "; ".join(clauses) + ". A contributed route dispatches a callable "
            "method of the server itself — that is what makes it reach the "
            "same gating every core route reaches — so the method must exist "
            "and be callable before the server binds.")


def match(bindings, method: str, path: str):
    """The first binding that answers `method` for `path`, with its remainder.

    Returns `(binding, remainder)` or None. Pure, and the whole matching rule
    lives here rather than in the two dispatch arms, so the read path and the
    write path cannot drift into two readings of one binding.
    """
    for binding in bindings:
        if binding.matches(method, path):
            return binding, binding.remainder(path)
    return None
