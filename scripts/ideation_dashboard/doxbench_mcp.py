"""The STDIO MCP SERVER that exposes the ONE knowledge tool boundary to the
harness (add-doxbench-editing-phase-b task 10.2's owed note, realized at §11;
`verification-findings.md` §3.2).

WHY IT EXISTS HERE AND NOT IN §10. Task 10.2's boundary is IN-PROCESS and the
ratified delta asks for "exactly ONE tool boundary declaring a small tool
contract" — it never says MCP. What 10.2 recorded as OWED was the transport:
a harness that can actually reach those four tools, and the mount-name pin
§3.2 asks for. §11 is the first slice with a harness to expose them to, so the
transport lands here, in front of the SAME `KnowledgeToolBoundary` — not beside
a second one.

WHAT §3.2 VERIFIED, HANDS-ON, AND WHAT THIS RELIES ON:

* OMP is a genuine MCP client with real mid-turn tool calling — discovery,
  connect, schema inline, model-issued call, real subprocess dispatch, result,
  next turn — proven end to end against a hand-rolled stdio server implementing
  `initialize`, `tools/list` and `tools/call` per the MCP 2025-03-26 spec.
  This module implements exactly those three methods and the
  `notifications/initialized` acknowledgement, and nothing else.
* Tools are not native function-schema entries: they are mounted as `xd://`
  devices whose docs and JSON schema are inlined into the system prompt, and
  invoked by the model writing the JSON argument object to `xd://<mount name>`.
* Discovery is ASYNCHRONOUS, so a turn issued before it completes simply does
  not see the tool that turn — degrading to design §3.4's "no knowledge
  service" reduced-packet posture, which is the correct fallback ALREADY
  specified. This module therefore adds no wait-for-discovery mechanism; the
  bridge registers before the first turn of a thread that needs the service,
  and that is the whole guarantee on offer.

**THE MOUNT NAME IS PINNED, AND ITS ONE CONTRADICTION IS RECORDED.** See
`MOUNT_SEPARATOR`.

**CONFINEMENT TRAVELS WITH THE MOUNT.** A server process is started for ONE
tile's confined set, declared in a manifest the bridge writes; every `search`
and `get_source` is confined to exactly those refs, which is the same rail
`doxbench_packet.confined_refs` computes in-process. A mount cannot be talked
into reaching another tile, because the refs it could name are the only ones it
was ever given.

Pure standard library, and no network: the transport is this process's own
stdin and stdout.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import re
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path

# THIS MODULE IS ALSO A PROCESS ENTRYPOINT, and the harness starts it (P1-6).
# The child is launched from the bridge's session root with an allowlisted
# environment that carries no `PYTHONPATH`, so an import of the package this
# file lives in has to be made to work from the file's own location — exactly
# what `serve.py` does for the same reason. Placed ABOVE the package import
# because that import is what needs it.
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from ideation_dashboard import doxbench_knowledge  # noqa: E402

# ---------------------------------------------------------------------------
# identity and the mount name (verification §3.2's realization note)
# ---------------------------------------------------------------------------

# The name this server is REGISTERED under. Short and underscore-free on
# purpose: the mount name is composed from it, and a server name carrying the
# separator's own characters makes the composed string unreadable.
MCP_SERVER_NAME = "doxbench"
MCP_SERVER_VERSION = "1"

# The protocol revision §3.2's hands-on proof was written against.
MCP_PROTOCOL_VERSION = "2025-03-26"

# The `xd://` device scheme and the MCP mount prefix, from §3.2's evidence.
XDEV_SCHEME = "xd://"
MOUNT_PREFIX = "mcp__"

# THE CONTRADICTION IN THE RECORDED FINDING — SETTLED 2026-08-19, AGAINST THE
# HARNESS'S OWN SOURCE AND A LIVE MOUNT.
#
# `verification-findings.md` §3.2 stated the convention twice and the two
# statements disagreed: its PROSE wrote `xd://mcp__<server>__<tool>` (a DOUBLE
# underscore), while its own EVIDENCE wrote `xd://mcp__verify_echo_echo` for a
# server whose one tool was `echo`, and `xd://mcp__sonarqube_*` for that host's
# ambient servers (a SINGLE underscore). This module originally took the prose.
#
# THE EVIDENCE WAS RIGHT. The source of truth is `createMCPToolName`
# (`packages/coding-agent/src/mcp/tool-bridge.ts:345-358`, v17.3.7):
#
#     return `mcp__${sanitizedServerName}_${normalizedToolName}`;
#
# a SINGLE underscore — and `sanitizeMCPToolNamePart` (`:335-343`) collapses
# `_+` to `_`, so a double separator is not merely unused, it is UNPRODUCIBLE.
# Corroborated at `builtin-names.ts:67`, and LIVE-CAPTURED with this very server
# registered as `doxbench` against real `omp --mode rpc`, verbatim from the
# running system prompt:
#
#     xd://mcp__doxbench_search
#     xd://mcp__doxbench_get_source
#     xd://mcp__doxbench_promote_finding
#     xd://mcp__doxbench_reindex
#
# `verification-findings.md` §3.2 carries a dated correction note recording the
# same thing at its source. The one-constant isolation did its job: settling the
# contradiction cost this line and three pinned test strings.
MOUNT_SEPARATOR = "_"

# The harness's own sanitiser, restated so `mount_name` can refuse a name whose
# mount would not be the name this module composed. `sanitizeMCPToolNamePart`
# lowercases, replaces every run of non-`[a-z_]` with `_`, collapses `_+`, and
# strips leading/trailing `_` — so a server or tool name carrying a digit, a
# hyphen or an uppercase letter mounts under a DIFFERENT string than it is
# spelled with, and a pin that did not know this would pin a lie.
_MOUNT_SAFE = re.compile(r"^[a-z]+(?:_[a-z]+)*$")


def mount_name(tool: str) -> str:
    """The exact `xd://` device name the harness mounts one of this server's
    tools as. ONE composition, pinned by a test string-for-string, so a rename
    breaks a test rather than a session."""

    if tool not in doxbench_knowledge.DECLARED_TOOLS:
        raise doxbench_knowledge.UnknownTool(
            f"{tool!r} is not a tool this boundary declares; the declared "
            f"names are {doxbench_knowledge.DECLARED_TOOLS}")
    # The composed name is only the real mount name if the harness's sanitiser
    # would leave both halves alone. Refusing here means a rename that WOULD be
    # rewritten by the harness fails at this function rather than silently
    # mounting under a string nothing in this repo pins.
    for part, label in ((MCP_SERVER_NAME, "server name"), (tool, "tool name")):
        if not _MOUNT_SAFE.match(part):
            raise doxbench_knowledge.KnowledgeError(
                f"{part!r} is not a mount-safe {label}: the harness lowercases "
                "it, replaces every run of non-[a-z_] with '_' and collapses "
                "repeats, so this would mount under a different string than it "
                "is spelled with")
    return (f"{XDEV_SCHEME}{MOUNT_PREFIX}{MCP_SERVER_NAME}"
            f"{MOUNT_SEPARATOR}{tool}")


def mounted_tool_names() -> tuple[str, ...]:
    """Every mount name this server puts in a harness's system prompt, in the
    boundary's own declared order. `graph_query` is NOT among them: it is
    reserved and unimplemented, and a mount that always refuses is a tool the
    model spends prompt budget reading about and can never use."""

    return tuple(mount_name(tool)
                 for tool in doxbench_knowledge.IMPLEMENTED_TOOLS)


# ---------------------------------------------------------------------------
# the tool contract, as MCP declares it
# ---------------------------------------------------------------------------

_REF_SCHEMA = {"type": "string", "minLength": 1}

TOOL_SCHEMAS: Mapping[str, Mapping[str, object]] = {
    doxbench_knowledge.TOOL_SEARCH: {
        "description": (
            "Search this tile's confined staged set. Returns ranked refs with "
            "their scores; the content itself comes from get_source."),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer", "minimum": 1,
                          "maximum": doxbench_knowledge.MAX_RETRIEVAL_LIMIT},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    doxbench_knowledge.TOOL_GET_SOURCE: {
        "description": (
            "Fetch one confined source's exact text by ref. A ref outside this "
            "tile's staged set and the promoted findings is refused."),
        "inputSchema": {
            "type": "object",
            "properties": {"ref": _REF_SCHEMA},
            "required": ["ref"],
            "additionalProperties": False,
        },
    },
    doxbench_knowledge.TOOL_PROMOTE_FINDING: {
        "description": (
            "Route a finding to the reviewed act that can make it durable. "
            "Writes nothing and stores nothing: it returns the request, and a "
            "human performs the act."),
        "inputSchema": {
            "type": "object",
            "properties": {
                "finding": {"type": "string", "minLength": 1},
                "provenance": {"type": "array", "items": _REF_SCHEMA,
                               "minItems": 1},
            },
            "required": ["finding", "provenance"],
            "additionalProperties": False,
        },
    },
    doxbench_knowledge.TOOL_REINDEX: {
        "description": (
            "Rebuild this mount's index from its declared manifest. Takes no "
            "sources from the caller: the confined set is the mount's, not the "
            "model's."),
        "inputSchema": {"type": "object", "properties": {},
                        "additionalProperties": False},
    },
}


# ---------------------------------------------------------------------------
# the confined mount manifest (what makes a mount one TILE's)
# ---------------------------------------------------------------------------

MANIFEST_SCHEMA_VERSION = 1
MANIFEST_KIND = "doxbench-knowledge-mount"


class MountManifestRefused(ValueError):
    """A manifest that does not declare a confined set this server may serve."""


@dataclasses.dataclass(frozen=True, slots=True)
class MountManifest:
    """ONE tile's confined set, as the file the bridge writes beside the
    registration. The manifest IS the confinement: this process can name no ref
    that is not in it, so a mount cannot be talked into another tile."""

    sources: tuple[tuple[str, str], ...]
    profile_id: str = doxbench_knowledge.PROFILE_LOCAL_EMBEDDED

    def as_dict(self) -> dict:
        return {
            "schema_version": MANIFEST_SCHEMA_VERSION,
            "kind": MANIFEST_KIND,
            "profile_id": self.profile_id,
            "sources": {ref: path for ref, path in self.sources},
        }

    @classmethod
    def from_dict(cls, payload: object) -> "MountManifest":
        if not isinstance(payload, Mapping):
            raise MountManifestRefused("a mount manifest is an object")
        if payload.get("schema_version") != MANIFEST_SCHEMA_VERSION \
                or payload.get("kind") != MANIFEST_KIND:
            raise MountManifestRefused(
                "a mount manifest declares this module's own schema_version "
                "and kind; another shape is another file")
        sources = payload.get("sources")
        if not isinstance(sources, Mapping) or not sources:
            raise MountManifestRefused(
                "a mount manifest declares the confined set it serves; an "
                "empty one would be a mount with nothing to confine")
        rows = []
        for ref, path in sources.items():
            if not isinstance(ref, str) or not ref.strip() \
                    or not isinstance(path, str) or not path.strip():
                raise MountManifestRefused(
                    "every confined source names a ref and a readable path")
            rows.append((ref, path))
        profile = payload.get("profile_id")
        return cls(sources=tuple(rows),
                   profile_id=str(profile) if profile
                   else doxbench_knowledge.PROFILE_LOCAL_EMBEDDED)

    def confined_refs(self) -> frozenset[str]:
        return frozenset(ref for ref, _ in self.sources)

    def indexed_sources(self) -> tuple[doxbench_knowledge.IndexedSource, ...]:
        """Read the confined set's bytes. An unreadable entry is SKIPPED, the
        same verdict `serve._indexed_sources` reaches: a document nobody can
        read is one the packet will not carry, never a reason to fail."""

        rows = []
        for ref, path in self.sources:
            try:
                text = Path(path).read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            rows.append(doxbench_knowledge.IndexedSource(ref=ref, text=text))
        return tuple(rows)


# ---------------------------------------------------------------------------
# registration (the bridge writes this BEFORE the first turn)
# ---------------------------------------------------------------------------

# The project-scoped config file the harness discovers a stdio server from
# (verification §3.2: `.omp/mcp.json`, `stdio` transport, `command`). Written
# into the BRIDGE's own session root, which is the child's cwd and is outside
# every git worktree — so registering a mount never writes into the corpus.
MCP_CONFIG_DIR = ".omp"
MCP_CONFIG_FILE = "mcp.json"
MANIFEST_FILE = "doxbench-knowledge-mount.json"


def registration_document(argv: Sequence[str]) -> dict:
    """The `.omp/mcp.json` document declaring THIS server, and only it."""

    args = list(argv)
    if not args:
        raise ValueError("a stdio registration names the command that runs it")
    return {
        "mcpServers": {
            MCP_SERVER_NAME: {
                "type": "stdio",
                "command": args[0],
                "args": args[1:],
            },
        },
    }


def server_argv(manifest_path: Path | str, *, python: str | None = None
                ) -> list[str]:
    """The command line that starts THIS server for one manifest.

    PATH-BASED, not `-m` — corrected 2026-08-19 after the adversarial review's
    P1-6. The registration used to name `-m ideation_dashboard.doxbench_mcp`,
    which the harness runs from the bridge's session root with an allowlisted
    environment carrying no `PYTHONPATH`:

        $ cd <session-root> && env -i PATH=… HOME=… /usr/bin/python3 \
            -m ideation_dashboard.doxbench_mcp --manifest …
        Error while finding module specification for
        'ideation_dashboard.doxbench_mcp'
        (ModuleNotFoundError: No module named 'ideation_dashboard')

    so the mount could never start. An ABSOLUTE PATH to this file works from any
    cwd and with no environment plumbing, because the file bootstraps its own
    package directory onto `sys.path` at import (see the top of this module).
    That keeps the registration free of an `env` block, which is the right shape
    for a config file the harness reads: nothing about this server's location is
    the operator's to keep in step."""

    return [python or sys.executable, str(Path(__file__).resolve()),
            "--manifest", str(manifest_path)]


def write_registration(root: Path | str, manifest: MountManifest, *,
                       python: str | None = None) -> tuple[Path, Path]:
    """Write the manifest and the harness's own discovery config under ``root``.

    Returns both paths. The caller is the bridge, and it calls this BEFORE the
    child starts: discovery is asynchronous, so registration-before-first-turn
    is the guarantee on offer, and a turn that races it degrades to the reduced
    packet rather than waiting on a mechanism nobody specified."""

    base = Path(root)
    (base / MCP_CONFIG_DIR).mkdir(parents=True, exist_ok=True)
    manifest_path = base / MANIFEST_FILE
    manifest_path.write_text(
        json.dumps(manifest.as_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    config_path = base / MCP_CONFIG_DIR / MCP_CONFIG_FILE
    config_path.write_text(
        json.dumps(registration_document(
            server_argv(manifest_path, python=python)),
            indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    return manifest_path, config_path


# ---------------------------------------------------------------------------
# the JSON-RPC surface
# ---------------------------------------------------------------------------

JSONRPC_VERSION = "2.0"
ERR_METHOD_NOT_FOUND = -32601
ERR_INVALID_PARAMS = -32602

METHOD_INITIALIZE = "initialize"
METHOD_INITIALIZED = "notifications/initialized"
METHOD_TOOLS_LIST = "tools/list"
METHOD_TOOLS_CALL = "tools/call"

SUPPORTED_METHODS: tuple[str, ...] = (
    METHOD_INITIALIZE, METHOD_INITIALIZED, METHOD_TOOLS_LIST, METHOD_TOOLS_CALL)


class KnowledgeMcpServer:
    """The MCP surface over ONE `KnowledgeToolBoundary` and ONE confined set.

    It adds no tool the boundary does not declare, and it decides nothing the
    boundary decides: a reserved name still answers with the boundary's own
    fixed governance refusal, an undeclared name still answers as unknown, and
    the two stay different verdicts on this transport exactly as they are
    in-process — a typo must never read as a governance verdict."""

    def __init__(self, boundary: doxbench_knowledge.KnowledgeToolBoundary, *,
                 confined_to: frozenset[str],
                 manifest: "MountManifest | None" = None) -> None:
        self._boundary = boundary
        self._confined = frozenset(confined_to)
        self._manifest = manifest

    # -- the three methods -------------------------------------------------

    def initialize(self) -> dict:
        return {
            "protocolVersion": MCP_PROTOCOL_VERSION,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": MCP_SERVER_NAME,
                           "version": MCP_SERVER_VERSION},
        }

    def list_tools(self) -> dict:
        """The FOUR implemented tools, in the boundary's own declared order.

        `graph_query` is deliberately absent: it is RESERVED and unimplemented,
        and a mount that always refuses is a tool the model spends system-prompt
        budget reading about and can never use. Its reservation is still visible
        on this transport — a `tools/call` naming it answers with the boundary's
        fixed governance refusal rather than as an unknown name."""

        return {"tools": [
            {"name": tool,
             "description": TOOL_SCHEMAS[tool]["description"],
             "inputSchema": TOOL_SCHEMAS[tool]["inputSchema"]}
            for tool in doxbench_knowledge.IMPLEMENTED_TOOLS]}

    def call_tool(self, name: object, arguments: object) -> dict:
        args = arguments if isinstance(arguments, Mapping) else {}
        try:
            payload = self._invoke(name, args)
        except doxbench_knowledge.KnowledgeError as refusal:
            # The boundary's OWN text: it is this surface's governance
            # vocabulary, written here, and carries no corpus content.
            return {"content": [{"type": "text", "text": str(refusal)}],
                    "isError": True}
        return {"content": [{"type": "text",
                             "text": json.dumps(payload, sort_keys=True)}],
                "isError": False}

    def _invoke(self, name: object, args: Mapping[str, object]) -> object:
        if name == doxbench_knowledge.TOOL_SEARCH:
            query = args.get("query")
            if not isinstance(query, str):
                raise doxbench_knowledge.KnowledgeError(
                    "search takes the query it is to run")
            limit = args.get("limit")
            hits = self._boundary.search(
                query, confined_to=self._confined,
                limit=int(limit) if isinstance(limit, int)
                and not isinstance(limit, bool)
                else doxbench_knowledge.MAX_RETRIEVAL_LIMIT)
            return [{"ref": hit.ref, "score": hit.score} for hit in hits]
        if name == doxbench_knowledge.TOOL_GET_SOURCE:
            ref = args.get("ref")
            if not isinstance(ref, str):
                raise doxbench_knowledge.KnowledgeError(
                    "get_source takes the ref it is to fetch")
            source = self._boundary.get_source(ref, confined_to=self._confined)
            if source is None:
                return {"ref": ref, "text": None}
            return {"ref": source.ref, "text": source.text}
        if name == doxbench_knowledge.TOOL_PROMOTE_FINDING:
            request = self._boundary.promote_finding(
                args.get("finding"), provenance=args.get("provenance") or ())
            return dataclasses.asdict(request)
        if name == doxbench_knowledge.TOOL_REINDEX:
            # THE MOUNT'S OWN MANIFEST IS THE ONLY SOURCE SET, and the caller
            # supplies none. A reindex that took sources from the model would
            # put material outside the tile's staged set INSIDE the confinement,
            # which is the one thing the confinement rail exists to prevent — so
            # the tool is offered with an empty argument schema and rebuilds
            # from the declared manifest.
            if self._manifest is None:
                raise doxbench_knowledge.RetrievalRefused(
                    "this mount declares no manifest, so there is nothing it "
                    "could rebuild its index from")
            report = self._boundary.reindex(self._manifest.indexed_sources())
            return dataclasses.asdict(report)
        # RESERVED before UNKNOWN, and through the boundary's own table, so
        # this transport cannot invent a third verdict.
        return self._boundary.call(name if isinstance(name, str) else "")

    # -- the JSON-RPC envelope --------------------------------------------

    def handle(self, request: object) -> dict | None:
        """One request in, one response out — or `None` for a notification,
        which JSON-RPC forbids answering."""

        if not isinstance(request, Mapping):
            return _error(None, ERR_INVALID_PARAMS, "a request is an object")
        method = request.get("method")
        request_id = request.get("id")
        if method == METHOD_INITIALIZED or request_id is None:
            return None
        if method == METHOD_INITIALIZE:
            return _result(request_id, self.initialize())
        if method == METHOD_TOOLS_LIST:
            return _result(request_id, self.list_tools())
        if method == METHOD_TOOLS_CALL:
            params = request.get("params")
            params = params if isinstance(params, Mapping) else {}
            return _result(request_id, self.call_tool(
                params.get("name"), params.get("arguments")))
        return _error(request_id, ERR_METHOD_NOT_FOUND,
                      f"this server implements {list(SUPPORTED_METHODS)}")


def _result(request_id: object, payload: object) -> dict:
    return {"jsonrpc": JSONRPC_VERSION, "id": request_id, "result": payload}


def _error(request_id: object, code: int, message: str) -> dict:
    return {"jsonrpc": JSONRPC_VERSION, "id": request_id,
            "error": {"code": code, "message": message}}


def build_server(manifest: MountManifest) -> KnowledgeMcpServer:
    backend = doxbench_knowledge.build_backend(
        doxbench_knowledge.SELF_HOSTED_LOCAL_EMBEDDED)
    boundary = doxbench_knowledge.KnowledgeToolBoundary(backend)
    boundary.reindex(manifest.indexed_sources())
    return KnowledgeMcpServer(boundary, confined_to=manifest.confined_refs(),
                              manifest=manifest)


def serve_stdio(server: KnowledgeMcpServer, stdin, stdout) -> None:
    """The line-delimited JSON-RPC loop. A malformed line is answered rather
    than fatal: a server that died on one bad frame would take the turn with
    it."""

    for raw in stdin:
        line = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else str(raw)
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except ValueError:
            response = _error(None, ERR_INVALID_PARAMS, "malformed JSON frame")
        else:
            response = server.handle(request)
        if response is None:
            continue
        payload = json.dumps(response, sort_keys=True) + "\n"
        try:
            stdout.write(payload)
        except TypeError:                       # a binary stream
            stdout.write(payload.encode("utf-8"))
        stdout.flush()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="doxbench-knowledge-mcp",
        description="the doxBench knowledge tool boundary, over stdio MCP")
    parser.add_argument("--manifest", required=True,
                        help="the confined mount manifest this server serves")
    args = parser.parse_args(list(argv) if argv is not None else None)
    manifest = MountManifest.from_dict(
        json.loads(Path(args.manifest).read_text(encoding="utf-8")))
    serve_stdio(build_server(manifest), sys.stdin, sys.stdout)
    return 0


if __name__ == "__main__":  # pragma: no cover - the process entrypoint
    raise SystemExit(main())
