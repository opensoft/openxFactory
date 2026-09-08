"""openxFactory's own conformant corpus adapter (`split-opendox-two-layer-product`
§ 2.2a, RULING DQ-1).

TWO PUBLIC NAMES, AND THAT IS THE POINT. `OpenxFactoryCorpusAdapter` is the
implementation; `home_corpus()` builds one over this repository's own corpus and
hands back the reference to resolve it with. Everything else in the package —
the shape, the home layout, the classifier, the verdict, the write path — is
construction detail, and a caller reaching for it directly would be reaching for
openxFactory's corpus by a route the corpus-adapter interface does not define,
which the seam's fourth requirement forbids.

`tests/corpus-adapter/test_no_privileged_route.py` enforces exactly that: any
module under `scripts/` importing this package may bind these two names and
nothing else.

`home_corpus()` is a FUNCTION rather than a constant so that importing this
package never imports the home layout — a package whose import pulls in
openxFactory's own paths could not be exercised against a corpus it does not
own, and that exercise is the only mechanical proof the fourth requirement
holds (design D6 part 3).
"""

from __future__ import annotations

from pathlib import Path

from .adapter import OpenxFactoryCorpusAdapter

__all__ = ("OpenxFactoryCorpusAdapter", "home_corpus")


def home_corpus(location: Path | str | None = None, *,
                verdict_groups: tuple[str, ...] | None = None):
    """An adapter over this repository's corpus, plus the reference to resolve.

    The home layout is imported HERE, on the call, not at package import — see
    the module docstring.
    """
    from .home import home_corpus as _home_corpus
    return _home_corpus(location, verdict_groups=verdict_groups)
