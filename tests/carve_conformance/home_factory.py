"""openxFactory's DECLARED reader for FLOOR PART 3, and the worked example a
destination copies (`split-opendox-two-layer-product` § 3.7, RULED OQ-1).

WHY THIS FILE IS SO SMALL, WHICH IS THE ARGUMENT AND NOT AN APOLOGY. § 3.7
requires `openxFactory`'s own adapter from § 2.2a to pass the same neutral
corpus every other destination passes, and "the only mechanical proof that the
home corpus has no privileged route" is that it does so through the ordinary
front door. What a destination has to write in order to be measured is
therefore exactly this: name your reader, and say how to point it at a
location. Nine lines. A destination that needs more than that has built
something the interface cannot address, which is itself the finding.

WHY IT SITS UNDER `tests/` AND NOT IN THE ADAPTER PACKAGE. Two reasons, and
both are rules already in force. `tests/corpus-adapter/test_no_privileged_route.py`
holds every module under `scripts/` importing `corpus_adapter_openxfactory` to
the package's two public names, and a factory naturally reaches for
`CorpusShape` and `Scope` as well — `tests/corpus-adapter/test_conformance.py`
already reaches for them from the test side, which is the precedent this
follows. And `tests/corpus-adapter/test_no_home_vocabulary.py` scans the
adapter package's string literals for header words and path shapes; the
neutral corpus's own `Type:`/`Title:` vocabulary and its glob are neither home
words nor home paths, but the scan cannot know that, and carving an exemption
into a vocabulary guard to hold a nine-line convenience would be a worse trade
than putting the nine lines where they already belong.

THE SHAPE BELOW BELONGS TO THE NEUTRAL CORPUS, NOT TO THIS REPOSITORY: two
roots of its own (`notes/`, `papers/`), a two-field header vocabulary of its
own, no governed write path and no verdict machinery. It is the same object
`tests/corpus-adapter/test_conformance.py` declares, restated here rather than
imported from a `pytest` module, because this file is loaded by a command-line
runner that does not collect tests.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

from corpus_adapter import SCOPE_ALL  # noqa: E402
from corpus_adapter_openxfactory import OpenxFactoryCorpusAdapter  # noqa: E402
from corpus_adapter_openxfactory.shape import CorpusShape, Scope  # noqa: E402

NEUTRAL_SHAPE = CorpusShape(
    scan_roots=("notes", "papers"),
    scopes={SCOPE_ALL: Scope(globs=("**/*.md",))},
    header_scan_lines=6,
    kind_field="Type",
    required_fields_by_kind={None: ("Type", "Title")},
)


def neutral_reader(name: str, location: str) -> OpenxFactoryCorpusAdapter:
    """The factory FLOOR PART 3 asks for: a reader pointed at one location.

    The location rides in the `CorpusRef` the corpus builds, so the adapter
    itself is constructed from the corpus's shape alone — which is precisely
    the property that makes it usable over a corpus openxFactory does not own.
    """
    return OpenxFactoryCorpusAdapter(NEUTRAL_SHAPE)
