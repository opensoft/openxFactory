"""The knowledge boundary's STDIO MCP TRANSPORT and its MOUNT-NAME PIN
(add-doxbench-editing-phase-b task 10.2's owed note, realized at §11;
`verification-findings.md` §3.2).

The mount-name test is the one §3.2 explicitly asked the realization for: the
`xd://` name is derived from the server name plus the tool name, not from the
bare tool name the contract declares, so it is pinned STRING FOR STRING here —
a rename then breaks a test rather than a session.

The protocol tests drive the real JSON-RPC surface and, for the loop, a real
line-delimited stream, because the failure this transport actually has is a
malformed frame taking the server down with it.
"""

from __future__ import annotations

import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import doxbench_knowledge as kn  # noqa: E402
from ideation_dashboard import doxbench_mcp as mcp  # noqa: E402


def _manifest(tmp_path):
    corpus = tmp_path / "corpus"
    corpus.mkdir(exist_ok=True)
    (corpus / "alpha.md").write_text(
        "Status: ratified\n\ndoc health checks run nightly against the corpus",
        encoding="utf-8")
    (corpus / "beta.md").write_text(
        "Status: draft\n\nthe DTN register lists promotion candidates",
        encoding="utf-8")
    return mcp.MountManifest(sources=(
        ("ideation/brainstorm/alpha.md", str(corpus / "alpha.md")),
        ("ideation/brainstorm/beta.md", str(corpus / "beta.md")),
    ))


def _server(tmp_path):
    return mcp.build_server(_manifest(tmp_path))


def _call(server, method, params=None, request_id=1):
    request = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params is not None:
        request["params"] = params
    return server.handle(request)


# ===========================================================================
# THE MOUNT NAME (verification §3.2's explicit realization ask)
# ===========================================================================


def test_the_mount_names_are_pinned_string_for_string():
    """CORRECTED after the adversarial review's P1-2 and LIVE-CAPTURED: with
    this server registered as `doxbench` against real `omp --mode rpc`, the
    running system prompt carried exactly these four names."""
    assert mcp.mount_name(kn.TOOL_SEARCH) == "xd://mcp__doxbench_search"
    assert mcp.mount_name(kn.TOOL_GET_SOURCE) == "xd://mcp__doxbench_get_source"
    assert mcp.mount_name(kn.TOOL_PROMOTE_FINDING) == \
        "xd://mcp__doxbench_promote_finding"
    assert mcp.mount_name(kn.TOOL_REINDEX) == "xd://mcp__doxbench_reindex"


def test_the_mounted_set_is_the_boundary_s_implemented_tools_in_its_own_order():
    assert mcp.mounted_tool_names() == tuple(
        f"xd://mcp__doxbench_{tool}" for tool in kn.IMPLEMENTED_TOOLS)


def test_the_mount_name_is_composed_the_way_the_harness_composes_it():
    """`createMCPToolName` (tool-bridge.ts:345-358) is
    `mcp__${server}_${tool}` — a SINGLE underscore — and
    `sanitizeMCPToolNamePart` collapses `_+` to `_`, so a double separator is
    not merely unused, it is UNPRODUCIBLE. This test re-implements the harness's
    own composition and asserts this module agrees with it, so the pin is
    against the rule rather than against four literals."""
    assert mcp.MOUNT_SEPARATOR == "_"

    def harness_name(server, tool):
        import re as _re

        def sanitize(value, fallback):
            out = _re.sub(r"_+", "_",
                          _re.sub(r"[^a-z_]+", "_", value.lower())).strip("_")
            return out or fallback

        server_part = sanitize(server, "server")
        tool_part = sanitize(tool, "tool")
        if tool_part.startswith(server_part + "_"):
            tool_part = tool_part[len(server_part) + 1:]
        return f"mcp__{server_part}_{tool_part}"

    for tool in kn.IMPLEMENTED_TOOLS:
        assert mcp.mount_name(tool) == (
            mcp.XDEV_SCHEME + harness_name(mcp.MCP_SERVER_NAME, tool))


def test_a_name_the_harness_would_rewrite_is_refused_rather_than_pinned():
    """The harness lowercases, replaces every run of non-`[a-z_]` with `_` and
    collapses repeats — so a server or tool name carrying a digit, a hyphen or
    a capital mounts under a DIFFERENT string than it is spelled with, and a pin
    that did not know that would pin a lie."""
    import ideation_dashboard.doxbench_mcp as module

    original = module.MCP_SERVER_NAME
    try:
        for unsafe in ("dox-bench", "doxBench", "doxbench2"):
            module.MCP_SERVER_NAME = unsafe
            with pytest.raises(kn.KnowledgeError):
                module.mount_name(kn.TOOL_SEARCH)
    finally:
        module.MCP_SERVER_NAME = original


def test_an_undeclared_tool_has_no_mount_name():
    with pytest.raises(kn.UnknownTool):
        mcp.mount_name("delete_everything")


# ===========================================================================
# THE PROTOCOL (MCP 2025-03-26: initialize, tools/list, tools/call)
# ===========================================================================


def test_initialize_answers_the_protocol_revision_the_finding_verified(tmp_path):
    result = _call(_server(tmp_path), "initialize")["result"]
    assert result["protocolVersion"] == "2025-03-26"
    assert result["serverInfo"]["name"] == mcp.MCP_SERVER_NAME
    assert "tools" in result["capabilities"]


def test_the_initialized_notification_is_acknowledged_with_no_response(tmp_path):
    server = _server(tmp_path)
    assert server.handle({"jsonrpc": "2.0",
                          "method": "notifications/initialized"}) is None


def test_tools_list_declares_the_four_implemented_tools_and_not_the_reserved_one(
        tmp_path):
    tools = _call(_server(tmp_path), "tools/list")["result"]["tools"]
    assert [tool["name"] for tool in tools] == list(kn.IMPLEMENTED_TOOLS)
    assert kn.RESERVED_TOOL_GRAPH_QUERY not in [tool["name"] for tool in tools]
    for tool in tools:
        assert tool["inputSchema"]["type"] == "object"
        assert tool["description"]


def test_search_answers_ranked_confined_refs(tmp_path):
    result = _call(_server(tmp_path), "tools/call",
                   {"name": "search",
                    "arguments": {"query": "doc health checks"}})["result"]
    assert result["isError"] is False
    hits = json.loads(result["content"][0]["text"])
    assert hits, "the mount returned nothing; this proves nothing"
    assert {hit["ref"] for hit in hits} <= {
        "ideation/brainstorm/alpha.md", "ideation/brainstorm/beta.md"}


def test_get_source_hands_back_the_exact_text(tmp_path):
    result = _call(_server(tmp_path), "tools/call",
                   {"name": "get_source",
                    "arguments": {"ref": "ideation/brainstorm/alpha.md"}})["result"]
    payload = json.loads(result["content"][0]["text"])
    assert payload["text"].startswith("Status: ratified")


def test_a_ref_outside_the_mount_s_confined_set_is_refused(tmp_path):
    """The confinement travels WITH the mount: the manifest is the whole set of
    refs this process can name, so another tile's document is unreachable
    through this transport, not merely unranked."""
    result = _call(_server(tmp_path), "tools/call",
                   {"name": "get_source",
                    "arguments": {"ref": "ideation/staging/other/secret.md"}})["result"]
    assert result["isError"] is True
    assert "outside this tile's staged set" in result["content"][0]["text"]


def test_promote_finding_returns_a_request_and_writes_nothing(tmp_path):
    server = _server(tmp_path)
    corpus_before = sorted((tmp_path / "corpus").iterdir())
    result = _call(server, "tools/call",
                   {"name": "promote_finding",
                    "arguments": {"finding": "the register is stale",
                                  "provenance": ["ideation/brainstorm/beta.md"]}}
                   )["result"]
    payload = json.loads(result["content"][0]["text"])
    assert payload["act_verb"] and payload["act_review"]
    assert payload["provenance"] == ["ideation/brainstorm/beta.md"]
    assert sorted((tmp_path / "corpus").iterdir()) == corpus_before


def test_an_unattributed_finding_is_refused_on_this_transport_too(tmp_path):
    result = _call(_server(tmp_path), "tools/call",
                   {"name": "promote_finding",
                    "arguments": {"finding": "no provenance"}})["result"]
    assert result["isError"] is True


def test_reindex_rebuilds_from_the_MOUNT_S_manifest_and_takes_none(tmp_path):
    result = _call(_server(tmp_path), "tools/call",
                   {"name": "reindex", "arguments": {}})["result"]
    report = json.loads(result["content"][0]["text"])
    assert report["source_count"] == 2
    # the schema offers the model no way to hand sources in
    schema = mcp.TOOL_SCHEMAS[kn.TOOL_REINDEX]["inputSchema"]
    assert schema["properties"] == {}
    assert schema["additionalProperties"] is False


def test_the_reserved_tool_answers_with_the_GOVERNANCE_refusal(tmp_path):
    result = _call(_server(tmp_path), "tools/call",
                   {"name": "graph_query", "arguments": {}})["result"]
    assert result["isError"] is True
    assert "RESERVED and unimplemented" in result["content"][0]["text"]
    assert "GRADUATION TRIGGER" in result["content"][0]["text"]


def test_an_undeclared_name_answers_as_unknown_not_as_a_verdict(tmp_path):
    """A typo must never read as a governance verdict — the same two-verdict
    distinction the in-process boundary keeps, kept on this transport."""
    result = _call(_server(tmp_path), "tools/call",
                   {"name": "grpah_query", "arguments": {}})["result"]
    assert result["isError"] is True
    text = result["content"][0]["text"]
    assert "not a tool this boundary declares" in text
    assert "RESERVED" not in text


def test_an_unknown_method_answers_a_jsonrpc_error(tmp_path):
    response = _call(_server(tmp_path), "resources/list")
    assert response["error"]["code"] == mcp.ERR_METHOD_NOT_FOUND


# ===========================================================================
# THE LOOP
# ===========================================================================


def test_a_malformed_frame_is_answered_rather_than_fatal(tmp_path):
    out = io.StringIO()
    mcp.serve_stdio(
        _server(tmp_path),
        io.StringIO('not json\n{"jsonrpc":"2.0","id":7,"method":"tools/list"}\n'),
        out)
    lines = [json.loads(line) for line in out.getvalue().splitlines()]
    assert lines[0]["error"]["code"] == mcp.ERR_INVALID_PARAMS
    assert lines[1]["id"] == 7 and lines[1]["result"]["tools"]


def test_the_REGISTERED_command_runs_with_no_PYTHONPATH_from_a_foreign_cwd(
        tmp_path):
    """P1-6. The registration used to name `-m ideation_dashboard.doxbench_mcp`,
    which the harness runs from the bridge's session root under an allowlisted
    environment carrying no `PYTHONPATH` — `ModuleNotFoundError`, every time, so
    the mount could never start. The registered command is now taken VERBATIM
    from the written config and run exactly as the harness would run it."""
    root = tmp_path / "sessroot"
    root.mkdir()
    manifest = _manifest(tmp_path)
    _manifest_path, config_path = mcp.write_registration(root, manifest)
    document = json.loads(config_path.read_text(encoding="utf-8"))
    entry = document["mcpServers"][mcp.MCP_SERVER_NAME]
    assert "env" not in entry, (
        "the entrypoint bootstraps its own package directory; an env block "
        "would be a second thing an operator has to keep in step")
    child = subprocess.Popen(
        [entry["command"], *entry["args"]],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        # THE HARNESS'S OWN CONDITIONS: the bridge's session root as cwd, and
        # an environment with no PYTHONPATH.
        cwd=str(root), env={"PATH": "/usr/bin:/bin", "HOME": str(tmp_path)},
        text=True)
    stdout, stderr = child.communicate(
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}) + "\n",
        timeout=60)
    assert child.returncode == 0, stderr
    answer = json.loads(stdout.splitlines()[0])
    assert [tool["name"] for tool in answer["result"]["tools"]] == list(
        kn.IMPLEMENTED_TOOLS)


def test_the_server_runs_as_a_real_child_over_real_pipes(tmp_path):
    """END TO END on the transport §3.2 verified the harness speaks: a real
    process, a real stdin/stdout pipe, the three methods in order."""
    manifest = _manifest(tmp_path)
    manifest_path = tmp_path / "mount.json"
    manifest_path.write_text(json.dumps(manifest.as_dict()), encoding="utf-8")
    environment = {"PATH": "/usr/bin:/bin",
                   "PYTHONPATH": str(REPO_ROOT / "scripts")}
    child = subprocess.Popen(
        [sys.executable, "-m", "ideation_dashboard.doxbench_mcp",
         "--manifest", str(manifest_path)],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env=environment, text=True)
    frames = "\n".join(json.dumps(frame) for frame in (
        {"jsonrpc": "2.0", "id": 1, "method": "initialize"},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
         "params": {"name": "get_source",
                    "arguments": {"ref": "ideation/brainstorm/alpha.md"}}},
    )) + "\n"
    stdout, stderr = child.communicate(frames, timeout=60)
    assert child.returncode == 0, stderr
    answers = [json.loads(line) for line in stdout.splitlines() if line.strip()]
    assert [answer["id"] for answer in answers] == [1, 2, 3]
    assert answers[0]["result"]["protocolVersion"] == "2025-03-26"
    payload = json.loads(answers[2]["result"]["content"][0]["text"])
    assert payload["text"].startswith("Status: ratified")


# ===========================================================================
# THE MANIFEST
# ===========================================================================


def test_a_manifest_of_another_shape_is_refused():
    with pytest.raises(mcp.MountManifestRefused):
        mcp.MountManifest.from_dict({"schema_version": 1, "kind": "something",
                                     "sources": {"a": "/b"}})


def test_an_empty_confined_set_is_refused_rather_than_served():
    with pytest.raises(mcp.MountManifestRefused):
        mcp.MountManifest.from_dict({"schema_version": 1,
                                     "kind": mcp.MANIFEST_KIND, "sources": {}})


def test_an_unreadable_source_is_skipped_rather_than_fatal(tmp_path):
    manifest = mcp.MountManifest(sources=(
        ("gone.md", str(tmp_path / "not-there.md")),
        ("here.md", str(tmp_path / "here.md"))))
    (tmp_path / "here.md").write_text("present", encoding="utf-8")
    assert [source.ref for source in manifest.indexed_sources()] == ["here.md"]
    # …but the confinement still names BOTH, so a skipped document is absent
    # rather than reachable from somewhere else
    assert manifest.confined_refs() == frozenset({"gone.md", "here.md"})


def test_the_manifest_round_trips_through_its_own_document(tmp_path):
    manifest = _manifest(tmp_path)
    assert mcp.MountManifest.from_dict(manifest.as_dict()) == manifest
