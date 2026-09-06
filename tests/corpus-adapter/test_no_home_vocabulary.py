"""RULING C2: the engineering vocabulary does not cross the seam.

C2 (`opensoft/openxFactory` issue #656, 2026-09-04T17:47Z) places the
nine-word lifecycle taxonomy, the governance nouns and the checker's grouping
names in the ENGINEERING descendant — "or ... openxFactory as its own adapter
over the corpus-adapter interface" — and the reason it gives is not tidiness:
*because a clinician using a descendant would then see the word requirement.*
A word that reaches the interface reaches every descendant of it, in every
industry, forever.

TWO SCANS OF DIFFERENT STRICTNESS, AND THE DIFFERENCE IS DELIBERATE.

  * **The interface is scanned over its WHOLE SOURCE TEXT** — literals,
    comments and docstrings alike. It is the file that travels to openDox and
    is read by every implementer of the standard; a governance noun explaining
    itself in a docstring is still a governance noun in the artifact a clinical
    descendant's author reads. That file therefore says what it needs to say
    without them, which is a real constraint and was met.
  * **The adapter package is scanned over its STRING LITERALS only.** Its
    docstrings must be free to name what it delegates to — `doc_health`, the
    apply lane, the ruled scan sets — because that documentation is how the
    delegation stays reviewable, and a scan that forbade it would be an
    argument for deleting it. What must not appear is a home path or a home
    header word as a VALUE, because a value is a behaviour: it is precisely the
    hardcoded layout that would give the class a private door
    (`corpus-adapter-seam` requirement 4).

`home.py` AND `write_path.py` ARE EXEMPT, and that exemption is the shape of
the design rather than a hole in the test. Naming this repository's roots, its
header words, its lane and its verb is their entire job; every other module in
the package receives those as DATA. `test_no_privileged_route.py`'s fourth scan
is the other half — nothing in the package's neutral core may even IMPORT
`home.py`, so a value that arrives there cannot leak sideways.

Precedent for a vocabulary scan as a conformance gate:
`scripts/validate-omnigent-contracts.py`'s `LEGACY_KEY_SEGMENT` check.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "tests"))

from import_scan import string_literals  # noqa: E402

INTERFACE = REPO_ROOT / "scripts" / "corpus_adapter.py"
PACKAGE = REPO_ROOT / "scripts" / "corpus_adapter_openxfactory"

#: Exempt: naming the home layout is what these two are FOR.
NAMING_MODULES = frozenset({"home.py", "write_path.py"})

#: Governance nouns, matched case-INSENSITIVELY: `Change`, `CHANGES` and
#: `changed` are the same word wearing different clothes.
GOVERNANCE_NOUNS = (
    "openspec", "ideation", "contracts", "templates", "examples",
    "requirement", "change", "spec", "family", "proposal",
)

#: Header words, matched case-SENSITIVELY and for a reason: `kind` is a
#: perfectly neutral field name (a refusal has a kind; a classification has a
#: kind), while `Kind:` is THIS corpus's header. Case is the only thing that
#: separates the general word from the home artifact, so case is what the scan
#: reads.
HEADER_WORDS = ("Status", "Kind")

#: Path shapes. Only meaningful as a literal — prose may cite a document by
#: name — so this one is scanned in literals alone.
PATH_SHAPES = (".md",)


def offending(text: str, *, nouns=GOVERNANCE_NOUNS, headers=HEADER_WORDS,
              shapes=()) -> list[str]:
    lowered = text.lower()
    hits = [noun for noun in nouns if noun in lowered]
    hits += [word for word in headers if word in text]
    hits += [shape for shape in shapes if shape in lowered]
    return hits


def test_the_interface_carries_no_home_vocabulary_anywhere_in_its_source():
    """The strict scan: literals, comments and docstrings alike."""
    hits = offending(INTERFACE.read_text(encoding="utf-8"))
    assert hits == [], (
        f"{INTERFACE.name} carries home vocabulary: {sorted(set(hits))}. This "
        "file travels to openDox and is what every implementer of the standard "
        "reads — RULING C2 keeps the engineering nouns on the engineering side "
        "of the seam, in prose as much as in values, 'because a clinician using "
        "a descendant would then see the word requirement'.")


def test_the_adapter_package_carries_no_home_vocabulary_in_its_values():
    """The literal scan, over every module except the two that name the home."""
    offenders = []
    scanned = 0
    for path in sorted(PACKAGE.glob("*.py")):
        if path.name in NAMING_MODULES:
            continue
        scanned += 1
        for value, line in string_literals(path):
            hits = offending(value, shapes=PATH_SHAPES)
            if hits:
                offenders.append(
                    f"{path.name}:{line} {value!r} carries {sorted(set(hits))}")
    assert offenders == [], (
        "a home path or header word appearing as a VALUE in the adapter's "
        "neutral core is a hardcoded layout, which is the private door "
        "`corpus-adapter-seam` requirement 4 forbids — it must arrive from a "
        f"`CorpusShape` instead. Offenders: {offenders}")
    assert scanned >= 5, (
        f"only {scanned} modules scanned in {PACKAGE} — the scan lost its "
        "subject")


def test_the_two_naming_modules_are_present_and_really_do_name_the_home():
    """The exemption must cover something, or it is a hole rather than a design.

    If `home.py` stopped carrying the layout, the exemption would be silently
    covering nothing while the layout had moved somewhere unexempted — and the
    literal scan above would be passing for the wrong reason."""
    for name in sorted(NAMING_MODULES):
        path = PACKAGE / name
        assert path.is_file(), f"{name} is exempted from the scan but absent"
        values = [value for value, _line in string_literals(path)]
        assert any(offending(value, shapes=PATH_SHAPES) for value in values), (
            f"{name} is exempted from the vocabulary scan because naming the "
            "home layout is its job, and it names none — either the layout "
            "moved to a module that is NOT exempt, or the exemption is stale")


def test_the_scanner_catches_a_hardcoded_root_and_spares_its_explanation(tmp_path):
    """The negative control, and the docstring exemption, in one file.

    Both halves matter. A scanner that missed `ROOTS = ("openspec",)` would let
    the private door in; a scanner that flagged the docstring EXPLAINING why
    that value is forbidden would make the test an argument for deleting the
    explanation, which is how a corpus loses its documentation."""
    module = tmp_path / "would_be_offender.py"
    module.write_text(
        '"""This module explains that a hardcoded openspec root is forbidden,\n'
        'and that a Status: header must arrive as data."""\n'
        'ROOTS = ("openspec",)\n'
        'HEADER = "Status"\n'
        'SUFFIX = ".md"\n'
        'INNOCENT = "the path does not exist"\n',
        encoding="utf-8")
    flagged = {value: sorted(set(offending(value, shapes=PATH_SHAPES)))
               for value, _line in string_literals(module)
               if offending(value, shapes=PATH_SHAPES)}
    assert flagged == {"openspec": ["openspec", "spec"], "Status": ["Status"],
                       ".md": [".md"]}, (
        f"the scanner flagged {flagged}: it must catch all three values (the "
        "root twice, since one noun sits inside the other), must not catch the "
        "innocent message, and must not reach into the docstring that explains "
        "the rule")
