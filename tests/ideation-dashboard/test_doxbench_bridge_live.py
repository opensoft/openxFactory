"""THE LIVE SMOKE: the real bridge against a REAL `omp --mode rpc`.

MANDATED BY THE ADVERSARIAL REVIEW'S P1-7, and it is the test whose absence let
six P1 defects ship: every hermetic bridge test passed against a fixture that
spoke three invented frames, so "the bridge works" was only ever a statement
about the fixture.

**NO GATE MAY REQUIRE THIS.** `omp` is not installed on most hosts and is not a
dependency of anything in this repository. The whole module SKIPS cleanly unless
a harness is discoverable AND a keyless local provider is reachable, and it
never installs, downloads, or writes outside its own `tmp_path`.

DISCOVERY, in order, so a developer can point it anywhere:

  1. `DOXBENCH_OMP_BINARY`   — an explicit path to the harness binary
  2. `shutil.which("omp")`   — an omp on PATH
  3. `DOXBENCH_OMP_HOME`     — a directory holding `bin/omp`

and, for the model, `DOXBENCH_OMP_MOCK_BASE_URL` (default
`http://127.0.0.1:8931/v1`), which must answer an OpenAI-shaped completion. The
provider is declared keyless (`auth: none`) in a models file this test writes
into its OWN temporary HOME, so no credential of any kind is used or assumed and
no real provider is ever contacted.

WHAT IT PROVES, and each of these was FALSE before this fix round:

  * the launch line starts a real harness at all              (P1-1)
  * `set_model` is accepted                                    (P1-5)
  * `dispatch` returns the model's OWN text, not ""            (P1-3, P1-4)
  * `/shake` round-trips with its free-text summary            (§3.6)
  * `get_state` yields a real session path for a thread        (11.4)
  * the memory backend really is `off` inside the session      (11.5)

RECORDED, because it cost an hour to find: `providers.tinyModel`,
`.memoryModel` and `.autoThinkingModel` default to `online`, and on a host with
no egress the agent turn BLOCKS on them before it ever reaches the local model.
The smoke overlay pins all three local. That is a property of an air-gapped
install, not of the bridge — but an operator running this bridge somewhere
without egress will meet it, so it is written down here and in task 11.1.
"""

from __future__ import annotations

import json
import os
import shutil
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import doxbench_bridge as br  # noqa: E402
from ideation_dashboard import doxbench_mcp as mcp  # noqa: E402
from ideation_dashboard.doxbench_model import (  # noqa: E402
    ModelCatalog, ModelCatalogEntry,
)

DEFAULT_MOCK_BASE_URL = "http://127.0.0.1:8931/v1"
MOCK_MODEL_ID = "local-model"
MOCK_PROVIDER_ID = "local-proxy"
LIVE_TIMEOUT_SECONDS = 120.0


def _harness_binary() -> str | None:
    explicit = os.environ.get("DOXBENCH_OMP_BINARY")
    if explicit and Path(explicit).is_file():
        return explicit
    found = shutil.which(br.HARNESS_COMMAND)
    if found:
        return found
    home = os.environ.get("DOXBENCH_OMP_HOME")
    if home:
        candidate = Path(home) / "bin" / br.HARNESS_COMMAND
        if candidate.is_file():
            return str(candidate)
    return None


def _mock_base_url() -> str | None:
    base = os.environ.get("DOXBENCH_OMP_MOCK_BASE_URL", DEFAULT_MOCK_BASE_URL)
    request = urllib.request.Request(
        base.rstrip("/") + "/chat/completions", method="POST",
        data=json.dumps({"model": MOCK_MODEL_ID, "messages": [],
                         "stream": False}).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=5) as answer:  # noqa: S310
            if answer.status == 200:
                return base
    except (urllib.error.URLError, OSError, ValueError):
        return None
    return None


@pytest.fixture(scope="module")
def live_harness():
    binary = _harness_binary()
    if binary is None:
        pytest.skip(
            "no omp harness discoverable (set DOXBENCH_OMP_BINARY or "
            "DOXBENCH_OMP_HOME); no gate requires one")
    base = _mock_base_url()
    if base is None:
        pytest.skip(
            "no keyless local provider answering at "
            f"{os.environ.get('DOXBENCH_OMP_MOCK_BASE_URL', DEFAULT_MOCK_BASE_URL)}; "
            "this smoke never contacts a real provider")
    return binary, base


@pytest.fixture()
def live_bridge(live_harness, tmp_path):
    """A real bridge whose child is a real harness, in a throwaway HOME."""
    binary, base = live_harness
    home = tmp_path / "home"
    agent_dir = home / ".omp" / "profiles" / br.BRIDGE_PROFILE / "agent"
    agent_dir.mkdir(parents=True)
    # A KEYLESS provider. `auth: none` — there is no credential here to hold.
    (agent_dir / "models.yml").write_text(
        "providers:\n"
        f"  {MOCK_PROVIDER_ID}:\n"
        f"    baseUrl: {base}\n"
        "    api: openai-completions\n"
        "    auth: none\n"
        "    models:\n"
        f"      - id: {MOCK_MODEL_ID}\n"
        "        name: Local Mock Model\n"
        "        contextWindow: 32768\n"
        "        maxTokens: 4096\n",
        encoding="utf-8")

    # The bridge's OWN overlay, plus the air-gap pins this host needs.
    overlay = dict(br.BRIDGE_OVERLAY)
    overlay["providers"] = {"tinyModel": "local", "memoryModel": "local",
                            "autoThinkingModel": "local"}
    catalog = ModelCatalog.from_entries([ModelCatalogEntry(
        model_id=MOCK_MODEL_ID, label="Local Mock Model",
        provider_class="self_hosted", available=True,
        input_limit_bytes=200_000, output_limit_bytes=64_000,
        data_handling="stays on this host")])
    launch = br.LaunchConfig(session_dir=tmp_path / "bridge", command=binary,
                             provider_id=MOCK_PROVIDER_ID, overlay=overlay)
    logged: list[str] = []
    bridge = br.OmpHarnessBridge(
        catalog, session_root=tmp_path / "bridge", launch=launch,
        timeout_seconds=LIVE_TIMEOUT_SECONDS, log=logged.append,
        environment={"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
                     "HOME": str(home)})
    bridge.live_log = logged           # noqa: SLF001 - the test reads the sink
    try:
        yield bridge
    finally:
        bridge.stop()


class _Section:
    def __init__(self, key, text):
        self.key = key
        self.text = text


class _Envelope:
    model_id = MOCK_MODEL_ID
    sections = (
        _Section("system_contract", "You are the doxBench editor-chat assistant."),
        _Section("human_message", "Human message:\nsay OK"),
    )


def test_a_real_turn_returns_the_models_own_text(live_bridge):
    """P1-1 + P1-3 + P1-4 + P1-5, all four at once. Before this fix round the
    launch line was rejected outright; worked around, `dispatch` returned
    `{'assistant_prose': ''}` at 1.97 s while the answer arrived ~20 s later."""
    started = time.monotonic()
    answer = live_bridge.dispatch(_Envelope())
    elapsed = time.monotonic() - started
    assert isinstance(answer, dict)
    assert set(answer) == {"assistant_prose", "proposals"}
    assert answer["assistant_prose"].strip(), (
        f"the harness answered nothing in {elapsed:.2f}s — the exact defect "
        "P1-4 recorded")
    assert answer["proposals"] == []
    # the child really did start, and only when a turn needed it
    assert live_bridge.started is True
    assert live_bridge.available is True


def test_the_launch_line_the_bridge_builds_is_one_a_real_binary_accepts(
        live_bridge):
    """P1-1's own regression: `--setting` made the child exit before answering.
    A started, live, answering child IS the proof, and the stderr sink must be
    clean of a flag complaint."""
    live_bridge.select_thread("ideation/staging/live/a.md")
    assert live_bridge.started is True
    joined = "\n".join(live_bridge.live_log)
    assert "unknown flag" not in joined, joined


def test_shake_round_trips_against_the_real_harness(live_bridge):
    """§3.6's exact surface: a `prompt` frame carrying slash text, answered with
    `agentInvoked: false` and a FREE-TEXT summary — no structured payload."""
    report = live_bridge.shake()
    assert report.agent_invoked is False
    assert isinstance(report.summary, str)


def test_a_thread_gets_a_real_session_path_from_the_harness(live_bridge):
    """11.4 against the real thing: `get_state.sessionFile` is a real file under
    the bridge's own `--session-dir`."""
    path = live_bridge.select_thread("ideation/staging/live/a.md")
    assert path, "the harness reported no session file"
    session = Path(path)
    assert session.suffix == br.SESSION_FILE_SUFFIX
    assert str(session).startswith(str(live_bridge.launch.session_dir))


def test_the_memory_backend_really_is_off_inside_the_running_session(
        live_bridge):
    """11.5's "install fact, not policy", made observable. `/memory diagnose`
    answers from the harness's OWN resolved settings, so this reads the pin back
    out of the running session rather than trusting the file the bridge wrote.
    With `backend: local` in the same slot the harness answers differently."""
    answer = live_bridge.run_command("/memory diagnose")
    report = "\n".join(answer.command_output)
    assert "off" in report.lower(), report


def test_the_knowledge_mount_registers_and_the_harness_lists_it(live_bridge,
                                                                tmp_path):
    """P1-6 end to end: the registration the bridge writes is discovered by a
    real harness started from that same session root, and `/mcp list` names it."""
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "note.md").write_text("Status: ratified\n\nlive mount check",
                                    encoding="utf-8")
    manifest = mcp.MountManifest(
        sources=(("ideation/brainstorm/note.md", str(corpus / "note.md")),))
    manifest_path, config_path = live_bridge.register_knowledge_mount(manifest)
    assert manifest_path.is_file() and config_path.is_file()
    # a fresh child, so discovery runs with the registration already in place
    live_bridge.stop()
    answer = live_bridge.run_command("/mcp list")
    listing = "\n".join(answer.command_output)
    assert mcp.MCP_SERVER_NAME in listing, listing
