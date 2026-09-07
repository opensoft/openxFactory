"""The openXdox column of the dashboard serve: the projection and snapshot
routes (`split-opendox-two-layer-product` § 2.4, PR 3 of 4).

Design § D3's "projection and snapshot" cluster — the MECHANISM openXdox owns —
lifted out of `serve.py` UNCHANGED, byte for byte, as a mixin
`DashboardHandler` composes: the snapshot read, the index roster, the read-only
`/source/` pass-through and the per-entry keying that confines it. Every
`self.<name>` these methods use (`_send_json`, `_serve_bytes`, `_active_entry`,
`_divergence_headers`, `loopback`, `source`, `checkout_root`, `snapshot_path`)
resolves through the MRO to `serve.py`'s own core implementation.

WHAT ARRIVES THROUGH THE SEAM AND WHAT STAYS A CORE ARM. `/snapshot-index.json`,
`/source` and `/source/` are CONTRIBUTED here (`ProjectionRoutesExtension`
below, assembled in `profile_openxfactory.py`), so `_route` no longer branches on
them. `/snapshot.json` deliberately does NOT become a binding: its arm tests
`path == self.snapshot_route`, a PER-SERVER class attribute fed by
`build_server(snapshot_route=…)`, and a `RouteBinding.pattern` is a frozen
string — contributing it would silently break that public keyword for any caller
who set it. So the METHOD moved here with its neighbours and the ARM stayed core,
which is the only split that keeps both the column boundary and the keyword. See
the PR body's "Design decisions taken".

THE `/source` PAIR MOVES TOGETHER, and that is load-bearing rather than tidy.
`if path == "/source" or path == "/source/"` was PARTLY DEAD in `_route`: the
`startswith("/source/")` arm above it fired first, so `/source/` reached
`_serve_source("")` and answered 404 with divergence headers and a zero-length
body — never `send_error(404, "no source path")`. Moving only the prefix would
have promoted the surviving core arm above the binding and changed that answer to
an HTML error body. `collect_bindings` returns every EXACT binding before every
PREFIX one, so an exact `/source` binding plus a `/source/` prefix binding
reproduces today's order exactly. `_refuse_bare_source` below is the one
non-move in this file: a `send_error` line lifted out of that `if`.

INVOCATION (design D12): `serve.py` runs BOTH as a script and as a module, so
this module uses ABSOLUTE `ideation_dashboard.*` imports, never `from . import`,
and self-inserts `scripts/` on the import path for the bare `route_extension`
import the same way `serve.py` and `snapshot_registry.py` do.
"""

from __future__ import annotations

import json
import sys
import urllib.parse
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:  # plain-script parity with serve.py (D12)
    sys.path.insert(0, str(_SCRIPTS_DIR))

import route_extension  # noqa: E402

from ideation_dashboard import snapshot_registry as registry_mod  # noqa: E402
from ideation_dashboard.serve_wire import (  # noqa: E402
    HOSTED_SESSION_REFUSAL,
    JSON_CTYPE,
    hosted_index,
    hosted_ref_refused,
)

SNAPSHOT_INDEX_ROUTE = "/snapshot-index.json"
SOURCE_PREFIX = "/source/"
#: The BARE `/source` route, with no file named. A module constant now because
#: it is a declared binding pattern rather than a literal inside an `if`; the
#: string, the status and the message are exactly what the core arm answered.
BARE_SOURCE_ROUTE = "/source"


# --------------------------- source-path containment (pure) ---------------------------

def resolve_source_path(checkout_root: Path, url_tail: str) -> Path | None:
    """Resolve a `/source/<tail>` request to an absolute file under
    `checkout_root`, or None to reject. Rejects absolute paths, NUL bytes, any
    escape of the root (via `..`, encoded `..`, or a symlink), and non-files.
    Percent-decoding happens BEFORE the containment check so `%2e%2e` cannot slip
    past.

    The containment check itself now lives in `snapshot_registry.resolve_within`
    so the SAME rule applies per registry entry (task 2.2); this stays the
    single-root entry point every existing caller and test uses."""
    return registry_mod.resolve_within(Path(checkout_root), url_tail)


class ProjectionRoutes:
    """The projection column, mixed into `DashboardHandler`."""

    def _query_key(self) -> tuple[str | None, str | None]:
        """The optional `?repository=&ref=` of a read route. Absent repository
        means the ACTIVE entry — which is what every pre-existing caller sends,
        so today's behaviour is unchanged."""
        query = urllib.parse.urlsplit(self.path).query
        params = urllib.parse.parse_qs(query)
        repository = (params.get("repository") or [None])[0]
        ref = (params.get("ref") or [None])[0]
        return repository, ref

    # ---- snapshot ----
    def _read_snapshot(self) -> bytes | None:
        """The ACTIVE snapshot's bytes, through the registry when one is bound
        (the in-process derived cache included) and from the configured path
        otherwise."""
        entry = self._active_entry()
        if entry is not None:
            return entry.read_bytes()
        try:
            return Path(self.snapshot_path).read_bytes()
        except OSError:
            return None

    def _serve_snapshot(self, head_only: bool) -> None:
        """`/snapshot.json` — the active snapshot, or any registered
        (repository, ref) named by the query. An unknown pair is a 404; the
        active view the client already has stays untouched.

        On the HOSTED plane a non-`main` ref refuses before resolution (FR-048):
        the serving index legitimately advertises a live session row (FR-014), so
        without this a hosted request could name one."""
        repository, ref = self._query_key()
        if hosted_ref_refused(self.loopback, ref):
            self._send_json(403, {"ok": False, "error": "session_unavailable",
                                  "message": HOSTED_SESSION_REFUSAL})
            return
        if repository and self.source is not None:
            entry = self.source.registry.resolve(repository, ref)
            if entry is None:
                # An AGGREGATE id (declared, or register-derived per project —
                # add-project-merged-projection D11) composes at the default
                # ref only. Off-loopback, members at unpublishable refs are
                # dropped before composition (the hosted_index projection,
                # applied to content).
                composed = None
                if registry_mod.is_publishable_ref(ref):
                    composed = self.source.compose_view(
                        repository, publishable_only=not self.loopback)
                if composed is not None:
                    self._serve_bytes(json.dumps(composed).encode("utf-8"),
                                      JSON_CTYPE, head_only)
                    return
                self.send_error(404, "no such snapshot")
                return
            if self._hosted_entry_refused(entry):
                return
            self._serve_bytes(entry.read_bytes(), JSON_CTYPE, head_only, entry=entry)
            return
        if repository and self.source is None:
            self.send_error(404, "no such snapshot")
            return
        # THE REF-LESS HOLE (PR #49 review finding 14, composing with finding
        # 10b): a request that NAMES no ref resolves to the ACTIVE entry, and
        # `hosted_ref_refused` only ever inspected the ref a request named. A
        # non-`main` active entry would therefore have been served off-loopback
        # with no key in sight. The refusal now follows the RESOLVED entry.
        if self._hosted_entry_refused(self._active_entry()):
            return
        self._serve_bytes(self._read_snapshot(), JSON_CTYPE, head_only)

    def _hosted_entry_refused(self, entry) -> bool:
        """Refuse (and answer) when the entry a request RESOLVED to is
        session-local and this is the hosted plane. Returns whether it answered."""
        if entry is None or not hosted_ref_refused(self.loopback, getattr(entry, "ref", None)):
            return False
        self._send_json(403, {"ok": False, "error": "session_unavailable",
                              "message": HOSTED_SESSION_REFUSAL})
        return True

    def _serve_index(self, head_only: bool) -> None:
        """`/snapshot-index.json` — the roster the selector reads, composed from
        the registry. No registry (a hand-built handler) means no index, which
        is exactly how the renderer degrades to a single snapshot."""
        if self.source is None:
            self.send_error(404, "no snapshot index")
            return
        document = self.source.index_document()
        # belt AND braces on the hosted plane (FR-048, finding 14): the bootstrap
        # above admits no session rows off-loopback, and this projection would
        # drop them anyway — a handler constructed by hand, or a registry a future
        # route populates, cannot reopen the hole.
        if not self.loopback:
            document = hosted_index(document)
        body = json.dumps(document).encode("utf-8")
        self._serve_bytes(body, JSON_CTYPE, head_only)

    # ---- source pass-through ----
    def _keyed_source(self, tail: str):
        """Split an optional `<repository>@<ref>/` prefix off a `/source/` tail.
        The prefix is honoured ONLY when it names a REGISTERED pair, so a real
        file whose first path segment happens to contain `@` still resolves as a
        path. Returns (repository, ref, remaining tail).

        A SESSION ref CONTAINS a slash (`draft/<topic>`, `cluster/<id>`), so the
        key is not always one path segment: the split is tried at every separator,
        shortest prefix first, and the first candidate naming a REGISTERED pair
        wins. Registration remains the whole admission test — an unregistered pair
        falls through to the plain path exactly as before — so widening the split
        cannot make an unknown key addressable. Both spellings work: the browser
        percent-encodes the whole key (`repo%40draft%2Ftopic`, one segment) and the
        runbook's `curl` writes it plainly (`repo@draft/topic`, two)."""
        if self.source is None or "/" not in tail:
            return None, None, tail
        parts = tail.split("/")
        for cut in range(1, len(parts)):
            rest = "/".join(parts[cut:])
            if not rest:
                break
            parsed = registry_mod.parse_key_id(
                urllib.parse.unquote("/".join(parts[:cut])))
            if parsed is None:
                continue
            if self.source.registry.get(*parsed) is not None:
                return parsed[0], parsed[1], rest
        return None, None, tail

    def _serve_source(self, tail: str, head_only: bool) -> None:
        repository, ref, rest = self._keyed_source(tail)
        # the keyed form is the OTHER route that names a ref (FR-048): a hosted
        # plane serves no session worktree's bytes, keyed or not
        if hosted_ref_refused(self.loopback, ref):
            self._send_json(403, {"ok": False, "error": "session_unavailable",
                                  "message": HOSTED_SESSION_REFUSAL})
            return
        entry = None
        if self.source is not None:
            target = self.source.registry.resolve_source(repository, ref, rest)
            entry = self.source.registry.resolve(repository, ref)
            # the UNKEYED form resolves to the ACTIVE entry, which the query never
            # named — the same ref-less hole `_serve_snapshot` closes above
            if self._hosted_entry_refused(entry):
                return
        else:
            target = resolve_source_path(Path(self.checkout_root), rest)
        if target is None:
            self.send_response(404)
            self._divergence_headers(entry)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        try:
            body = target.read_bytes()
        except OSError:
            self.send_error(404, "unreadable source")
            return
        ctype = "text/markdown; charset=utf-8" if target.suffix == ".md" else "text/plain; charset=utf-8"
        self._serve_bytes(body, ctype, head_only, entry=entry)

    def _refuse_bare_source(self, head_only: bool) -> None:
        """`GET /source` with no file named — refused, exactly as before.

        THE ONE NON-MOVE IN THIS FILE (see the module docstring). This body is
        the `send_error` line that used to sit inside `_route`'s
        `if path == "/source" or path == "/source/"` arm, lifted into a method
        so it can be NAMED by a `RouteBinding`. `head_only` is accepted and
        unused for the same reason the core arm ignored it: `send_error`
        suppresses the body on a HEAD itself.
        """
        self.send_error(404, "no source path")


class ProjectionRoutesExtension:
    """openXdox's projection contribution: the index roster and the `/source`
    pair. Conforms to `route_extension.RouteExtension` STRUCTURALLY, so this
    column imports nothing from the core it contributes to.
    """

    def routes(self) -> tuple[route_extension.RouteBinding, ...]:
        return (
            route_extension.RouteBinding("GET", SNAPSHOT_INDEX_ROUTE, False,
                                         "_serve_index"),
            # ORDER-INSENSITIVE by construction: `collect_bindings` groups every
            # exact binding ahead of every prefix one, so `/source` cannot be
            # swallowed by `/source/` however these two are declared here.
            route_extension.RouteBinding("GET", BARE_SOURCE_ROUTE, False,
                                         "_refuse_bare_source"),
            route_extension.RouteBinding("GET", SOURCE_PREFIX, True,
                                         "_serve_source"),
        )
