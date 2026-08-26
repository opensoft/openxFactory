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

WIDENED BY add-model-provider-broker (ratified 2026-08-26), and the four claims
above all survive the widening. This module now makes a SECOND declaration
beside the harness one: when the checkout declares a model-provider BINDING,
`declared_model_port_factory` resolves the broker-backed
`doxbench_provider.BrokeredProviderPort` instead of the harness bridge. It
still names no endpoint (the endpoint arrives in the broker's mint answer, and
lives only in `doxbench_provider`), still holds no credential and no token
(both live in `doxbench_provider`, the one module permitted to hold them), and
still reads no credential-shaped environment variable. What it gained is a
CHOICE between two declarations, which is exactly the kind of install-time fact
this module exists to make readable in one place.

THE UNCONFIGURED POSTURE IS UNCHANGED, BYTE FOR BYTE. A checkout with no
bindings document, or one declaring no bindings, resolves the SAME
`model_port_factory(session_root)` the entrypoints have always resolved, so an
install that never heard of a broker behaves precisely as it did before this
change — and a plane with no factory at all still refuses
`model_capability_unavailable` exactly as it always has.

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

import sys
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


# --------------------------------------------------------------------------
# the BROKERED declaration (add-model-provider-broker tasks 2.2/2.5)
# --------------------------------------------------------------------------

# Limits for a brokered provider, narrowing the server ceilings exactly as the
# harness entry's do. Conservative on purpose: a binding names a provider this
# repository has never measured, so the declaration promises the smaller number
# rather than the schema's maximum.
BROKERED_INPUT_LIMIT_BYTES = 200_000
BROKERED_OUTPUT_LIMIT_BYTES = 64_000

# The handling badge a brokered entry carries. It states the posture PLAINLY
# and in the opposite direction from the harness entry's, because it is the
# opposite posture: this one leaves the host.
BROKERED_DATA_HANDLING = (
    "leaves this host: a hosted provider reached with a short-lived token the "
    "credential broker minted")

# The `provider_class` a brokered entry declares. Free-form by the catalog
# contract, and this is the honest word for it: the model is reached through a
# broker's credential rather than run on this host.
BROKERED_PROVIDER_CLASS = "brokered"


def brokered_catalog(binding) -> ModelCatalog:
    """The one-entry catalog a BINDING discloses.

    Built FROM the binding rather than declared beside it, so the menu an
    operator sees names the binding they declared — its id and its label — and
    cannot drift from it. The id is the binding's id for the same reason: a
    catalog handle that did not match the binding would make a turn's chosen
    model unresolvable back to the declaration that reached it.

    AVAILABLE ON PURPOSE, and it is a claim about the DECLARATION exactly as the
    harness catalog's is: `BrokeredProviderPort.catalog()` marks every entry
    unavailable the moment a mint has refused, which is the honest posture for a
    broker that cannot answer, while declaring it unavailable up front would say
    the same thing about a binding that works."""
    return ModelCatalog.from_entries([
        ModelCatalogEntry(
            model_id=binding.id,
            label=binding.label,
            provider_class=BROKERED_PROVIDER_CLASS,
            available=True,
            input_limit_bytes=BROKERED_INPUT_LIMIT_BYTES,
            output_limit_bytes=BROKERED_OUTPUT_LIMIT_BYTES,
            data_handling=BROKERED_DATA_HANDLING,
        ),
    ])


def brokered_model_port_factory(binding, *, runner=None, opener=None,
                                clock=None, notice=None):
    """The ZERO-ARGUMENT factory for a BROKER-BACKED port, memoized per process.

    Same shape and same reason as `model_port_factory` above: the accessor is
    called per REQUEST, and a port built per call would mint a fresh token for
    every turn and discard a live one. The seams (`runner`, `opener`, `clock`,
    `notice`) pass through so a test can exercise a turn without a broker and
    without a provider; production declares none of them."""
    from ideation_dashboard import doxbench_provider as provider_mod

    seams = {name: value for name, value in (
        ("runner", runner), ("opener", opener), ("clock", clock),
        ("notice", notice)) if value is not None}
    catalog = brokered_catalog(binding)
    lock = threading.Lock()
    holder: dict[str, object] = {}

    def resolve():
        port = holder.get("port")
        if port is not None:
            return port
        with lock:
            port = holder.get("port")
            if port is None:
                port = provider_mod.BrokeredProviderPort(
                    binding, catalog, **seams)
                holder["port"] = port
            return port

    return resolve


def declared_model_port_factory(session_root: Path | str, *,
                                checkout_root: Path | str,
                                bindings_path: Path | str | None = None,
                                spawn=None):
    """THE declaration both entrypoints make (task 2.5).

    ONE rule, in one place, so `cli.cmd_generate_and_open` and `serve.serve()`
    cannot drift into two answers for "what does this install talk to":

      * a checkout declaring a model-provider BINDING resolves the brokered
        port for the FIRST declared binding, and every provider endpoint and
        every minted token it needs lives inside `doxbench_provider`;
      * a checkout declaring NONE resolves exactly what these entrypoints have
        always resolved — the harness bridge — so the unconfigured posture is
        unchanged byte for byte;
      * a bindings document that will not READ (malformed YAML, a wrong kind, a
        record naming an unknown key) resolves the harness declaration too, and
        says so on stderr. Refusing to serve at all would make one bad line in
        an operator's settings file take the whole console down, and silently
        serving a DIFFERENT provider than the one declared would be worse than
        either.

    THE FIRST DECLARED BINDING, and that is a stated limitation rather than a
    design: the model seam takes ONE port, so an install talks to one provider
    at a time. Choosing among several declared bindings needs a selection rule
    this change does not have and must not invent — see tasks.md 2.5."""
    from ideation_dashboard import doxbench_binding as binding_mod

    store = binding_mod.BindingStore(
        bindings_path if bindings_path is not None
        else binding_mod.bindings_path(checkout_root))
    try:
        declared = store.list()
    except binding_mod.BindingRefused as error:
        sys.stderr.write(
            f"[model-provider] the bindings document could not be read "
            f"({error}); serving the local harness declaration instead\n")
        declared = ()
    if not declared:
        return model_port_factory(Path(session_root), spawn=spawn)
    return brokered_model_port_factory(declared[0])
