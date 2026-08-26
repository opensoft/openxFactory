"""The INSTALL-TIME model-provider declaration a doxBench entrypoint makes.

WHY A MODULE AND NOT A LINE IN `cli.py`. The entrypoint already makes two
install-time declarations in exactly this idiom — `adapter_factory=
serve_mod.real_notebook_adapter` and `knowledge_declaration=
knowledge_mod.SELF_HOSTED_LOCAL_EMBEDDED` — for the reason those call sites give
in as many words: *an operator must be able to read what their install talks
to*. The model provider is the same kind of fact and it is declared the same
way, so this module holds the three inputs `OmpHarnessBridge` cannot supply
itself, beside each other, in one readable place:

  * `HARNESS_CATALOG` — the approved model choices this install discloses. A
    DECLARATION CONSTANT, never a per-turn parameter. It matters that it is not
    the constructor's default: `OmpHarnessBridge`'s `catalog` defaults to
    `EMPTY_CATALOG` (`doxbench_model.EMPTY_CATALOG`), so a bare declaration would
    resolve, disclose nothing, and look to an operator exactly like a working
    install with nothing approved.
  * a SESSION ROOT — where the harness child's session files, its artifact
    directories and the bridge's own config overlay land. Supplied by the
    entrypoint (a CLI flag, defaulted beside the served snapshot), because
    `OmpHarnessBridge.__init__` has a keyword-only `session_root` with NO
    default: the adapter is unconstructible bare, deliberately, so nobody can
    declare one without saying where it writes.
  * a `LaunchConfig` — `provider_id` and `command`, the harness-side half of the
    declaration. `provider_id` lives on the launch and NOT on a catalog entry;
    that placement is a recorded ruling (`ModelCatalogEntry`'s own docstring, and
    `LaunchConfig`'s), and this module honours it rather than reopening it.

WHAT THIS MODULE IS NOT. It is not a provider adapter, it holds no credential,
reads no credential-shaped environment variable, and names no endpoint. The
harness child's environment is an allowlist (`doxbench_bridge.
INHERITED_ENVIRONMENT`) that no credential-shaped variable can pass, and an
API-backed provider's credential is provisioned into the `doxbench-bridge`
harness profile by the ratified broker lane — never held here.

ONE INSTANCE PER PROCESS, and that is a requirement rather than an optimisation.
`_workbench_model_port` is called PER REQUEST, and `OmpHarnessBridge` is
STATEFUL: it holds the per-document-thread harness sessions and the selected
one. A factory that constructed a bridge per call would break the
one-session-per-document-thread correspondence BY CONSTRUCTION and would restart
a supervised child on every request. So `model_port_factory` returns a
ZERO-ARGUMENT callable — the shape `serve.py`'s accessor calls, with no
arguments — that closes over the declaration and hands back the SAME bridge for
the life of the served process.

CONSTRUCTION IS LAZY, resolution is not. The bridge is built on the first
resolution rather than at import or at parse time, so an entrypoint that is
never asked for a model builds nothing; and the bridge itself starts its child
only at the first TURN that needs one, so resolving a port — which every
capabilities probe does — spawns no harness process.
"""

from __future__ import annotations

import threading
from pathlib import Path

from ideation_dashboard import doxbench_bridge as bridge_mod
from ideation_dashboard.doxbench_model import ModelCatalog, ModelCatalogEntry

# --------------------------------------------------------------------------
# the harness-side declaration
# --------------------------------------------------------------------------

# The harness provider the approved models are registered under, in the
# bridge's own `doxbench-bridge` profile. `local-proxy` is the keyless,
# on-this-host posture the catalog badge below states: a local OpenAI-shaped
# endpoint the operator runs, which is why no credential appears anywhere in
# this module.
HARNESS_PROVIDER_ID = "local-proxy"

# The one approved choice this install discloses. An OPAQUE UI handle, not a
# provider model name (the catalog contract says so in as many words), so
# changing which local model answers is an operator-side change to the harness
# profile and not a change to this id.
HARNESS_MODEL_ID = "omp-local"

# Limits NARROW the server ceilings, they never widen them: 1,048,576 request
# bytes and 900,000 output bytes are the released schema's maxima.
HARNESS_INPUT_LIMIT_BYTES = 200_000
HARNESS_OUTPUT_LIMIT_BYTES = 64_000

HARNESS_CATALOG = ModelCatalog.from_entries([
    ModelCatalogEntry(
        model_id=HARNESS_MODEL_ID,
        label="Local harness model",
        provider_class="self_hosted",
        available=True,
        input_limit_bytes=HARNESS_INPUT_LIMIT_BYTES,
        output_limit_bytes=HARNESS_OUTPUT_LIMIT_BYTES,
        data_handling="stays on this host: a local harness child, no hosted provider",
    ),
])
"""The install's approved model catalog — the declaration an operator reads.

AVAILABLE ON PURPOSE, and it is a claim about the DECLARATION, not a probe: the
bridge marks every entry unavailable the moment it knows itself dead or
unstartable (`OmpHarnessBridge.catalog`), which is the honest posture for a
harness that never started. Declaring the entry unavailable up front would say
the same thing about an install that works."""

# Where a serve's harness sessions live when the entrypoint was not told
# otherwise: beside the served snapshot, in the run directory this process
# already owns. NEVER inside the served checkout and never a corpus path — the
# child's cwd is its own session directory, so a harness tool that reaches for
# the filesystem lands in scratch space rather than in the corpus.
MODEL_SESSIONS_DIRNAME = "model-sessions"


def session_root_beside(snapshot_path: Path | str) -> Path:
    """The default session root for a serve of `snapshot_path`.

    One rule for both entrypoints — `cli.py`'s `generate-and-open` and
    `serve()` — so the two cannot drift into writing harness sessions in two
    different places."""
    return Path(snapshot_path).resolve().parent / MODEL_SESSIONS_DIRNAME


def harness_launch(session_root: Path | str) -> bridge_mod.LaunchConfig:
    """The launch this install declares: the harness command and the provider
    its approved models are registered under, rooted at `session_root`.

    `command` is named explicitly rather than left to the dataclass default so
    the declaration an operator reads is complete on its own."""
    root = Path(session_root)
    return bridge_mod.LaunchConfig(session_dir=root,
                                   command=bridge_mod.HARNESS_COMMAND,
                                   provider_id=HARNESS_PROVIDER_ID)


def model_port_factory(session_root: Path | str, *,
                       catalog: ModelCatalog = HARNESS_CATALOG,
                       launch: bridge_mod.LaunchConfig | None = None,
                       spawn=None):
    """The ZERO-ARGUMENT `model_port_factory` an entrypoint declares.

    Returns a callable taking NO arguments — the shape
    `serve.DashboardHandler._workbench_model_port` calls — which resolves to the
    SAME `OmpHarnessBridge` every time, for the life of this process. The lock
    is not decoration: the server is a `ThreadingHTTPServer`, so two requests
    really can resolve the port at once, and two bridges would be two disjoint
    session tables.

    `spawn` is the bridge's own child-process seam, passed through so a caller
    that must exercise a turn can inject a double; production declares none and
    the bridge uses its real spawn."""
    root = Path(session_root)
    declared_launch = launch if launch is not None else harness_launch(root)
    lock = threading.Lock()
    holder: dict[str, bridge_mod.OmpHarnessBridge] = {}

    def resolve() -> bridge_mod.OmpHarnessBridge:
        port = holder.get("port")
        if port is not None:
            return port
        with lock:
            port = holder.get("port")
            if port is None:
                port = bridge_mod.OmpHarnessBridge(
                    catalog, session_root=root, launch=declared_launch,
                    spawn=spawn)
                holder["port"] = port
            return port

    return resolve
