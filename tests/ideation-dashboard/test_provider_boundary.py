"""THE NARROWED PROVIDER BOUNDARY (add-model-provider-broker task 2.3).

WHAT THIS FILE REPLACES, AND WHY IT IS NOT A DELETION. Before this change the
claim was "no provider is contacted from this repository", and it was enforced
by a family of PER-MODULE source scans — `test_doxbench_model.py`'s
`FORBIDDEN_SOURCE_SNIPPETS`, `test_doxbench_turns.py`'s copy of it,
`test_doxbench_packet.py`'s, `test_doxbench_knowledge.py`'s,
`test_doxbench_threads.py`'s, `test_doxbench_memory_gateway.py`'s,
`test_doxbench_bridge.py`'s credential-name scan, and the browser-side scans in
`test_doxbench_privacy.py` / `test_doxbench_transport.py` /
`test_doxbench_mutation_boundary.py`. Every one of those still exists, still
scans exactly what it scanned, and still passes UNMODIFIED — this file pins
their continued existence by name at the bottom, precisely so the narrowing
cannot be achieved by deleting the guard it narrows.

What none of them ever did was sweep the PACKAGE. Each names one module, so a
NEW module added under `scripts/ideation_dashboard/` inherited no check at all
— which is exactly the gap a change that introduces a provider client must
close rather than widen. So the boundary is restated here in the form the
ratified delta gives it:

    Exactly ONE named module may hold a provider endpoint, a provider SDK, or a
    minted token, and every other module in this repository stays free of all
    three.

and it is enforced package-wide, over every `*.py` under
`scripts/ideation_dashboard/`, with exactly one exemption whose name the module
itself declares (`doxbench_provider.PROVIDER_CLIENT_MODULE`).

TWO TIERS, because the honest rule has two. The PROVIDER tier — SDK imports,
provider hosts and paths, this repository's own minted-token type — is exempt
for one module and one module only. The generic HTTP-CLIENT tier
(`urllib.request`, `Authorization`, `Bearer `) has a second, NAMED holder:
`snapshot_registry.py`, whose bearer token is the SNAPSHOT DATA SOURCE's, taken
only from an operator-named environment variable, and is not a provider
credential in any sense. Rather than let that exemption blur the rule, this
file asserts POSITIVELY that `snapshot_registry.py` holds nothing from the
provider tier — so its presence on the second list cannot become a doorway to
the first.

THE VIEWS CLAUSE STAYS ABSOLUTE. No browser module is exempt from anything: a
token in a page is exfiltratable by anything able to run script there, and the
provider call is made server-side precisely so no page ever holds one.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from conftest import REPO_ROOT

from ideation_dashboard import doxbench_provider as provider_mod

PACKAGE = REPO_ROOT / "scripts" / "ideation_dashboard"
WEB = PACKAGE / "web"

#: The ONE module the boundary permits. Read from the module's own constant so
#: the test and the module cannot drift into naming two different files.
PROVIDER_CLIENT_MODULE = provider_mod.PROVIDER_CLIENT_MODULE

#: The SECOND holder of the generic HTTP-client needles, and of nothing from
#: the provider tier. See this file's docstring for why it is named rather than
#: silently tolerated.
SNAPSHOT_SOURCE_MODULE = "snapshot_registry.py"

# --- tier one: PROVIDER endpoints, PROVIDER SDKs, MINTED TOKENS -------------
#
# Every needle here is absent from every module in the package except the one
# named above — measured, not assumed, on the tree this change landed on.
PROVIDER_NEEDLES: tuple[str, ...] = (
    # provider SDKs
    "import openai",
    "import anthropic",
    "from openai",
    "from anthropic",
    "boto3",
    "google.generativeai",
    "mistralai",
    "import cohere",
    "import ollama",
    # provider endpoints
    "api.openai.com",
    "api.anthropic.com",
    "generativelanguage.googleapis.com",
    "openai.azure.com",
    "/v1/chat/completions",
    "/v1/completions",
    "/v1/messages",
    # credential-shaped header and field spellings a provider client needs
    "apiKey",
    "api-key",
    "x-api-key",
    "access_token",
    "refresh_token",
    "client_secret",
    # THIS repository's own minted-token type and provider-call helpers: the
    # names by which a second module would have to hold a token to use one
    "MintedToken",
    "_post_to_provider",
    "PROVIDER_STATUS_TOKEN_EXPIRED",
    "PROVIDER_REQUEST_PROMPT_FIELD",
)

# --- tier two: the generic HTTP client -------------------------------------
HTTP_CLIENT_NEEDLES: tuple[str, ...] = (
    "urllib.request",
    "Authorization",
    "Bearer ",
)


def _package_modules() -> list[Path]:
    return sorted(PACKAGE.rglob("*.py"))


def _source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ===========================================================================
# the package sweep
# ===========================================================================


def test_exactly_one_module_may_hold_a_provider_endpoint_or_a_minted_token():
    """THE NARROWED BOUNDARY, swept over every module in the package."""
    offenders: list[str] = []
    for module in _package_modules():
        if module.name == PROVIDER_CLIENT_MODULE:
            continue
        source = _source(module)
        for needle in PROVIDER_NEEDLES:
            if needle in source:
                offenders.append(f"{module.name}: {needle}")
    assert not offenders, (
        "the provider boundary is exactly one module wide; these modules "
        f"crossed it: {offenders}")


def test_the_exemption_is_not_vacuous():
    """The named module really IS the one holding the transport.

    Without this, the sweep above would pass just as well if the provider
    client were deleted, or if it never contacted a provider at all — and a
    boundary drawn around an empty room proves nothing. It also pins the
    module's self-declaration equal to the name this file exempts."""
    module = PACKAGE / PROVIDER_CLIENT_MODULE
    assert module.is_file(), PROVIDER_CLIENT_MODULE
    source = _source(module)
    for needle in ("urllib.request", "Authorization", "Bearer ", "MintedToken",
                   "_post_to_provider"):
        assert needle in source, needle
    assert provider_mod.PROVIDER_CLIENT_MODULE == module.name


def test_the_generic_http_client_has_exactly_two_named_holders():
    """`urllib.request` / `Authorization` / `Bearer ` are HTTP-client facts, not
    provider facts, so the second holder is named rather than swept away."""
    permitted = {PROVIDER_CLIENT_MODULE, SNAPSHOT_SOURCE_MODULE}
    offenders: list[str] = []
    holders_seen: set[str] = set()
    for module in _package_modules():
        if module.name in permitted:
            source = _source(module)
            if any(needle in source for needle in HTTP_CLIENT_NEEDLES):
                holders_seen.add(module.name)
            continue
        source = _source(module)
        for needle in HTTP_CLIENT_NEEDLES:
            if needle in source:
                offenders.append(f"{module.name}: {needle}")
    assert not offenders, offenders
    # "Exactly two" means both halves: no third holder above, and each named
    # holder really holds — an exemption for a module with no needles would be
    # a stale permit waiting to hide a future offender.
    assert holders_seen == permitted, holders_seen


def test_the_snapshot_source_holds_nothing_from_the_provider_tier():
    """The second holder's exemption reaches tier two and stops there.

    Its bearer token is the snapshot data source's, taken only from an
    operator-named environment variable; it is not a provider credential, and
    this assertion is what keeps that distinction from eroding into a second
    doorway."""
    source = _source(PACKAGE / SNAPSHOT_SOURCE_MODULE)
    for needle in PROVIDER_NEEDLES:
        assert needle not in source, needle


# ===========================================================================
# the views clause — ABSOLUTE, no module exempt
# ===========================================================================

BROWSER_NEEDLES: tuple[str, ...] = (
    "Authorization",
    "Bearer",
    "api_key",
    "apiKey",
    "api-key",
    "x-api-key",
    "access_token",
    "MintedToken",
    "https://",
    "api.openai.com",
    "api.anthropic.com",
)


def _browser_modules() -> list[Path]:
    return sorted(path for path in WEB.rglob("*.js")
                  if "vendor" not in path.relative_to(WEB).parts)


@pytest.mark.parametrize("needle", BROWSER_NEEDLES)
def test_no_browser_module_carries_a_provider_endpoint_or_a_token(needle):
    """A minted token NEVER crosses to the browser, and no page names a
    provider. Absolute: the one-module exemption does not reach here, because
    the browser is where a token would be most exfiltratable and least
    necessary."""
    offenders = [path.relative_to(WEB).as_posix()
                 for path in _browser_modules()
                 if needle in _source(path)]
    assert not offenders, f"{needle} appears in {offenders}"


# ===========================================================================
# the guard this one narrows still exists
# ===========================================================================

#: (test module, the assertion or constant that must survive in it). A clobber
#: that "passed" this file by deleting the per-module scans it narrows would
#: fail here instead.
PRESERVED_SCANS: tuple[tuple[str, str], ...] = (
    ("test_doxbench_model.py", "FORBIDDEN_SOURCE_SNIPPETS"),
    ("test_doxbench_model.py",
     "def test_module_source_contains_no_network_or_provider_or_schema_markers"),
    ("test_doxbench_model.py", "FORBIDDEN_PORT_MEMBERS"),
    ("test_doxbench_turns.py",
     "def test_module_source_contains_no_network_provider_serve_or_logging_markers"),
    ("test_doxbench_packet.py",
     "def test_the_packet_module_contains_no_forbidden_spelling"),
    ("test_doxbench_status_exemption.py",
     "def test_the_carved_module_contains_no_forbidden_spelling"),
    ("test_doxbench_knowledge.py",
     "def test_the_knowledge_module_contains_no_forbidden_spelling"),
    ("test_doxbench_threads.py",
     "def test_the_thread_module_contains_no_forbidden_spelling"),
    ("test_doxbench_memory_gateway.py",
     "def test_the_declaration_module_contains_no_forbidden_spelling"),
    ("test_doxbench_bridge.py",
     "def test_the_bridge_module_declares_no_credential_shaped_name"),
    ("test_doxbench_privacy.py", "FORBIDDEN_SOURCE_NEEDLES"),
    ("test_doxbench_mutation_boundary.py", "_FORBIDDEN_NEEDLES"),
)


@pytest.mark.parametrize("module_name,marker", PRESERVED_SCANS)
def test_the_per_module_scans_this_boundary_narrows_still_exist(module_name,
                                                                marker):
    text = (Path(__file__).parent / module_name).read_text(encoding="utf-8")
    assert marker in text, f"{module_name} no longer carries {marker}"


def test_doxbench_model_stays_free_of_the_provider_client():
    """The seam's own module is NOT the exempt one, and never becomes it.

    `doxbench_model.py` declares the port protocol and the pure catalog types;
    its own scan bans `urllib`, `subprocess` and every credential spelling. The
    provider client is a separate module BEHIND that seam, which is what keeps
    the protocol free of a provider verb (`FORBIDDEN_PORT_MEMBERS`)."""
    source = _source(PACKAGE / "doxbench_model.py")
    assert PROVIDER_CLIENT_MODULE.removesuffix(".py") not in source
    assert "urllib" not in source
