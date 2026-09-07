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
    not resolve — because a caller does nothing different for any of them: they
    are all "this server must not start".
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


def collect_bindings(extensions) -> tuple[RouteBinding, ...]:
    """Flatten the extensions into ONE consult order, refusing what cannot serve.

    Refuses an object that does not conform, a `routes()` that yields anything
    but `RouteBinding`s, and two bindings claiming one route — the last being
    the collision that would otherwise leave a declared route silently
    unreachable. A "GET" binding and a "HEAD" binding at the same (pattern,
    is_prefix) collide too, because a "GET" binding already answers HEAD
    (`_claimed_collision_keys`) — the "HEAD" binding would never be reached on
    the one request method it exists to answer.

    Returns every exact binding first and every prefix binding after, each group
    in declaration order, for the reason the module docstring gives: tuple order
    across independent extensions is an accident, and a prefix must not swallow
    a sibling's exact route because of it.
    """
    exact: list[RouteBinding] = []
    prefix: list[RouteBinding] = []
    seen: dict[tuple[str, str, bool], str] = {}
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
                    raise RouteBindingError(
                        f"two route bindings claim {claimed_key[0]} "
                        f"{binding.pattern!r} (prefix={binding.is_prefix}): "
                        f"{previous!r} and {binding.handler!r}. The second could "
                        "never be reached, and a route that looks declared and "
                        "never fires is worse than one that refuses.")
            seen[binding.key] = binding.handler
            (prefix if binding.is_prefix else exact).append(binding)
    return tuple(exact) + tuple(prefix)


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
