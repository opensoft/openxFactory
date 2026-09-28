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
"""

from __future__ import annotations

import importlib.util
import sys
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
