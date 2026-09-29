"""The NotebookLM sync's `--session-ref` re-sync registers the host first
(plan 034 T047; admitted by T007 batch E on RULED `5856475254`, item 2).

`scripts/sync-notebooklm-books.py` builds neither an openDox parser nor a
server, and imports no engine module. But its `session_source_set()` calls
`workbench.session_documents`, and from openDox-code's T025 on that function
lists the REGISTERED home corpus under the registered session-notebook scope.
Only `opendox_host.register_openxfactory()` fills those two seams (T046). So
the script has to make that call before it reaches the reader, or the re-sync
refuses `ADAPTER_NOT_REGISTERED` at the pinned leg.

The tests below hold the ORDER: the registration comes first, and the reader
is reached only after it. `tests/notebooklm/test_sync_notebooklm_books.py`
drives the real reader in this same process, where `tests/conftest.py` has
already registered; this file is what notices if the script stops doing it
for itself.

THE LAST TEST RUNS IN A CLEAN INTERPRETER, because only there does nothing
else install the carved reach or register first (Copilot, PR #1181). The
script imports the host before any reach is installed, so the order holds only
because the host's one call installs the reach itself. That test loads the
script as its entry point does and drives `session_source_set()` twice.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import textwrap
import types
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "sync-notebooklm-books.py"

# `tests/conftest.py` has already installed the reach and made the ONE call.
import opendox_host                                          # noqa: E402


def _load_sync() -> types.ModuleType:
    """The sync script as a module, under a name of this file's own, so it
    never shares state with `tests/notebooklm`'s copy of it."""
    name = "sync_notebooklm_books_host_registration"
    spec = importlib.util.spec_from_file_location(name, SCRIPT)
    assert spec is not None and spec.loader is not None, SCRIPT
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


@pytest.fixture
def sync():
    module = _load_sync()
    yield module
    sys.modules.pop(module.__name__, None)


def _recording_world(monkeypatch, sync):
    """Stand in for the registration and the reader, recording the order in
    which the script reaches them."""
    calls: list[str] = []
    monkeypatch.setattr(opendox_host, "register_openxfactory",
                        lambda: calls.append("register"))

    def session_documents(worktree, *, repository=None):
        calls.append("session_documents")
        return [("ideation/brainstorm/a.md", "Status: brainstorm\n")]

    workbench = types.SimpleNamespace(session_documents=session_documents)

    def dashboard_module(name):
        assert name == "workbench", name
        calls.append("load workbench")
        return workbench

    monkeypatch.setattr(sync, "_dashboard_module", dashboard_module)
    return calls


def test_the_session_source_set_registers_the_host_before_it_reads(
        monkeypatch, sync, tmp_path: Path) -> None:
    calls = _recording_world(monkeypatch, sync)
    target = types.SimpleNamespace(worktree=tmp_path, repository="openxFactory")

    documents = sync.session_source_set(target)

    assert documents == [("ideation/brainstorm/a.md", "Status: brainstorm\n")]
    assert calls == ["register", "load workbench", "session_documents"], calls


def test_a_refused_registration_reaches_no_reader(monkeypatch, sync,
                                                  tmp_path: Path) -> None:
    """The registration's own refusal is not swallowed, and the reader is
    never reached behind it: a process that could not register must not list
    a corpus some other registration left behind."""
    calls = _recording_world(monkeypatch, sync)

    def refuse():
        calls.append("register")
        raise opendox_host.HostProfileNotRegistered("planted refusal")

    monkeypatch.setattr(opendox_host, "register_openxfactory", refuse)
    target = types.SimpleNamespace(worktree=tmp_path, repository="openxFactory")

    with pytest.raises(opendox_host.HostProfileNotRegistered,
                       match="planted refusal"):
        sync.session_source_set(target)
    assert calls == ["register"], calls


def test_the_registration_is_the_hosts_one_call() -> None:
    """The helper names `opendox_host.register_openxfactory` and nothing
    else: no second registration path that could drift from the host's."""
    source = SCRIPT.read_text(encoding="utf-8")
    assert source.count("opendox_host.register_openxfactory()") == 1, (
        "the sync script should make the host's one call exactly once")
    assert "register_home(" not in source
    assert "register_session_notebook_scope(" not in source


#: What the clean interpreter runs: the script loaded as its entry point
#: loads it, then the registration step and the reader, twice.
_STANDALONE = textwrap.dedent("""
    import importlib.util, sys, types
    from pathlib import Path
    root = Path({root!r})
    spec = importlib.util.spec_from_file_location("sync_books", {script!r})
    sync = importlib.util.module_from_spec(spec)
    sys.modules["sync_books"] = sync
    spec.loader.exec_module(sync)
    print("loaded", "opendox" in sys.modules, "opendox_host" in sys.modules)
    target = types.SimpleNamespace(worktree=root, repository="openxFactory")
    first = sync.session_source_set(target)
    import opendox, opendox_host
    from opendox import corpus_adapter, domain_profile, workbench
    profile = domain_profile.current()
    leg = (root / "openDox" / "code" / "src").resolve()
    print("registered", profile is opendox_host.profile(),
          corpus_adapter.home() is opendox_host.home_corpus,
          workbench.session_notebook_scope(),
          Path(opendox.__file__).resolve().is_relative_to(leg))
    second = sync.session_source_set(target)
    print("again", bool(first), second == first,
          domain_profile.current() is profile)
""")


def test_a_standalone_run_registers_for_itself_in_a_clean_interpreter(
        tmp_path: Path) -> None:
    """Copilot, PR #1181: a standalone run imports the host before any reach
    is installed, and nothing else registers for it.
    - Loading the script imports neither `opendox` nor the host.
    - The first `session_source_set()` then installs the pinned leg's reach,
      registers this host's profile, home corpus and scope, and reads.
    - The second reads the same documents through the same profile.
    With no `PYTHONPATH`, and from a directory that is not the checkout, so
    the reach can come only from the host's own call."""
    env = {key: value for key, value in os.environ.items()
           if key != "PYTHONPATH"}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    program = _STANDALONE.format(root=str(REPO_ROOT), script=str(SCRIPT))
    proc = subprocess.run([sys.executable, "-c", program], capture_output=True,
                          text=True, cwd=str(tmp_path), env=env, timeout=300)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.splitlines() == [
        "loaded False False",
        "registered True True documents True",
        "again True True True",
    ], proc.stdout
