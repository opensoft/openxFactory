"""The home corpus is reachable only the way every other corpus is.

`corpus-adapter-seam`'s fourth requirement, first scenario: "WHEN a consumer
reaches `openxFactory`'s corpus by a call the corpus-adapter interface does not
define, THEN the route is refused, because the seam's whole value is that the
home corpus is reached the same way every other corpus is."

RULING DQ-1 is what makes that load-bearing rather than precautionary. Brett
ruled that openxFactory KEEPS an adapter — "doc-health and OpenSpec stay in
openxFactory, and a small adapter package beside them implements the
corpus-adapter seam" — so this repository is permanently both the owner of a
corpus and the author of a reader over it, which the capability itself calls
"exactly the position in which a private door gets built". Without this scan,
DQ-1 collapses into "the reader never really left".

FOUR SCANS, EACH A DIFFERENT DOOR:

  1. **Reaching past the package's two public names.** An importer may bind
     `OpenxFactoryCorpusAdapter` or `home_corpus`. `from
     corpus_adapter_openxfactory.home import HOME_SHAPE` is a private door with
     a public-looking import statement, and it is the one that would actually
     get written.
  2. A negative control on that scan, because it is a proof of ABSENCE.
  3. **The interface is neutral.** `scripts/corpus_adapter.py` imports neither
     reader package nor the implementation. That is the property that lets it
     travel to openDox, where the checker package does not exist, and it is the
     direct analogue of the guard `tests/doc-health/test_import_direction.py`
     already keeps over `scripts/output_boundary.py`.
  4. **The package's neutral core cannot see the home layout.** Nothing except
     the package's own `__init__` imports `home.py`, so the adapter class
     CANNOT branch on the home corpus — it has no name for it. This is the
     structural half of the requirement, and it is what makes the conformance
     suite's run over a foreign corpus meaningful rather than decorative.

PARSED, NOT GREPPED, for the reason `test_import_direction.py` gives at length:
the modules here must stay free to NAME the packages they delegate to, in
docstrings and comments, and a substring grep would make true documentation
into a test failure.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "tests"))

from import_scan import (  # noqa: E402
    bound_names,
    imported_modules,
    names_a_forbidden_package,
)

SCRIPTS = REPO_ROOT / "scripts"
PACKAGE_NAME = "corpus_adapter_openxfactory"
PACKAGE = SCRIPTS / PACKAGE_NAME
INTERFACE = SCRIPTS / "corpus_adapter.py"

# Both spellings of the same package. Every caller imports it as a top-level
# name off `scripts/`, but `scripts/__init__.py` exists, so
# `scripts.corpus_adapter_openxfactory` resolves too and would reintroduce the
# same route past a one-spelling test. Same reason
# `test_import_direction.py:43-48` gives for its own pair.
PACKAGE_SPELLINGS = (PACKAGE_NAME, f"scripts.{PACKAGE_NAME}")

#: What an importer outside the package may bind — the package's `__all__`,
#: and nothing else.
PUBLIC_NAMES = frozenset({"OpenxFactoryCorpusAdapter", "home_corpus"})

#: Measured at authoring time (228 modules under `scripts/` outside the
#: package); the floor sits ~20% below so an ordinary deletion does not fail the
#: build, while a scan that lost its subject does.
MIN_SCANNED = 182

#: The package's own modules that may import the home layout. `__init__` alone,
#: and only on the call — see its docstring.
MAY_SEE_HOME = frozenset({"__init__.py", "home.py"})


def relative_imports(path: Path):
    """`from . import x` / `from .x import y`, as (module, line).

    `import_scan.imported_modules` deliberately SKIPS relative imports — they
    can never name another top-level package, which is what that scanner is
    for. Inside one package they are the only spelling there is, so scan 4
    needs its own reader.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.level:
            if node.module:
                yield node.module, node.lineno
            else:
                for alias in node.names:
                    yield alias.name, node.lineno


def test_nothing_under_scripts_reaches_past_the_two_public_names():
    """Scan 1: the package's innards are unreachable from `scripts/`."""
    offenders = []
    scanned = 0
    for path in sorted(SCRIPTS.rglob("*.py")):
        if PACKAGE_NAME in path.parts:
            continue
        scanned += 1
        for line, bound in bound_names(path, PACKAGE_SPELLINGS):
            if bound not in PUBLIC_NAMES:
                offenders.append(
                    f"{path.relative_to(REPO_ROOT)}:{line} binds {bound!r}")

    assert offenders == [], (
        "openxFactory's own adapter may be reached only through its two public "
        f"names {sorted(PUBLIC_NAMES)}. Importing a submodule, or importing the "
        "package itself and reaching for an attribute, is a route the "
        "corpus-adapter interface does not define — which is exactly what "
        "`corpus-adapter-seam` requirement 4 forbids for the home corpus. "
        f"Offending imports: {offenders}")

    # Non-vacuity. A scan that found no files would also find no offenders, and
    # would keep passing after a rename of the thing it is meant to police.
    assert scanned >= MIN_SCANNED, (
        f"only {scanned} modules scanned under {SCRIPTS} (floor {MIN_SCANNED}) "
        "— the scan lost its subject; check the path before trusting the "
        "assertion above")


def test_the_scan_would_catch_the_routes_it_is_meant_to_catch(tmp_path):
    """Scan 2: the negative control, asserted on the COUNT recognized.

    Four spellings of the same private door, and every one of them is a thing
    somebody would plausibly write on the way to a quick fix."""
    doors = (
        "from corpus_adapter_openxfactory.home import HOME_SHAPE\n"
        "from corpus_adapter_openxfactory import check\n"
        "import corpus_adapter_openxfactory.classify\n"
        "import scripts.corpus_adapter_openxfactory as pkg\n"
        "from corpus_adapter_openxfactory import OpenxFactoryCorpusAdapter\n"
    )
    scratch = tmp_path / "would_be_offender.py"
    scratch.write_text(doors, encoding="utf-8")
    bound = list(bound_names(scratch, PACKAGE_SPELLINGS))
    caught = [b for _line, b in bound if b not in PUBLIC_NAMES]
    allowed = [b for _line, b in bound if b in PUBLIC_NAMES]
    assert len(caught) == 4, (
        f"the scan recognised {caught} out of {bound} — a real private door "
        "could slip past `test_nothing_under_scripts_reaches_past_the_two_"
        "public_names`")
    assert allowed == ["OpenxFactoryCorpusAdapter"], (
        f"the lawful import must NOT be flagged; got {allowed}")


def test_the_interface_imports_neither_reader_package_nor_the_implementation():
    """Scan 3: neutrality is a property of imports, not of where a file sits.

    `scripts/corpus_adapter.py` is the module BOTH readers will consume (§ 2.3,
    § 2.4) and it travels to openDox with the carve, where the checker package
    does not exist at all. An import of either package from inside it would put
    the seam's own cycle back one level down and make the module un-carveable —
    the same argument `test_import_direction.py` makes for the write guard."""
    forbidden = ("doc_health", "scripts.doc_health",
                 "ideation_dashboard", "scripts.ideation_dashboard",
                 *PACKAGE_SPELLINGS)
    offenders = [
        f"{INTERFACE.name}:{line} imports {module!r}"
        for module, line in imported_modules(INTERFACE)
        if names_a_forbidden_package(module, forbidden)
    ]
    assert offenders == [], (
        "the corpus-adapter interface must depend on NEITHER reader package "
        "NOR any implementation — an implementation depends on the interface, "
        "never the reverse (requirement 1), and the module travels to openDox "
        f"where neither exists. Offending imports: {offenders}")


def test_the_adapters_neutral_core_cannot_see_the_home_layout():
    """Scan 4: the class has no name for the corpus it lives in.

    `home.py` is the one module permitted to name openxFactory's roots, globs
    and header words. If `adapter.py`, `classify.py`, `check.py`, `shape.py` or
    `write_path.py` imported it, a home special case would be one line away and
    the conformance suite's run over a foreign corpus would stop proving
    anything. `__init__.py` imports it INSIDE `home_corpus()`, which is the
    whole reason that name is a function."""
    offenders = []
    for path in sorted(PACKAGE.glob("*.py")):
        if path.name in MAY_SEE_HOME:
            continue
        for module, line in relative_imports(path):
            if module == "home" or module.startswith("home."):
                offenders.append(f"{path.name}:{line} imports .{module}")
    assert offenders == [], (
        "no module in the adapter package may import the home layout except "
        "the package's own entrypoint: a class that can see the home corpus "
        "can branch on it, and requirement 4 is precisely the rule that it must "
        f"not. Offending imports: {offenders}")
    # Non-vacuity: the scan must actually be looking at the package.
    scanned = [p.name for p in PACKAGE.glob("*.py")
               if p.name not in MAY_SEE_HOME]
    assert len(scanned) >= 5, (
        f"only {scanned} scanned in {PACKAGE} — the scan lost its subject")
