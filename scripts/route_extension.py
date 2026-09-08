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
