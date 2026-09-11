#!/usr/bin/env python3
"""Entrypoint wrapper so the dashboard serve runs from THIS repository, POST-SHED
(mirrors `scripts/ideation-dashboard-nightly.py` and `scripts/doc-health.py`):

    python3 scripts/ideation-dashboard-serve.py --snapshot … --checkout-root …

WHY A WRAPPER APPEARED HERE. Before `split-opendox-two-layer-product` § 5.2 the
serve was `python3 -m ideation_dashboard.serve` with `PYTHONPATH=scripts`, and
that one line did three things at once: it found the module, it found every
sibling column the module imports, and it got openxFactory's composition point
bound because `serve.py` sat in the same package as `profile_openxfactory.py`.
The shed moved `serve.py` to openDox-code and deleted the profile's old path
(the manifest's single `deleted_at_carve` row), so the old line now finds
nothing — and would still be wrong if it did, because none of the three things
it used to do happens by itself any more:

  * the module is at a PINNED leg, and reading it lawfully means reading it
    through this repository's own pin (RULED Q7, `#656` `5626248666`);
  * the serve's columns span BOTH legs — `openxdox.serve_gate` and
    `openxdox.serve_projection` are openXdox's — so one `src/` on the path is
    not enough and a single-leg install fails on the seventeenth import
    (measured: `ideation/brainstorm/opendox-shed-exit-a-post-shed-mode-measured.md`);
  * `build_server` names `profile_openxfactory` as a BARE GLOBAL with no
    import anywhere, so the profile has to be REGISTERED with it — § 4.3's
    hole, answered by RULED ASK-2 option (2) (`#656` `5628886636`).

`carved_reach` does all three, and this file is the one place a person or a
service unit runs to get them. It is what `scripts/reserve-dashboard.sh`
executes; the Copilot finding that prompted it (`PRRT_kwDOTAvnrs6hbVwB`) is
exactly that a registration performed only by two pytest conftests is not a
registration a real server process ever receives.

REFUSES RATHER THAN DEGRADES. `require()` is the EAGER check — this process is
about to serve, so an uninitialized gitlink is a checkout that cannot do the
job, not a condition to work around, and finding out here beats finding out at
the first request. The message it raises names the leg, the missing path and
the command that fixes it.

AND IT COMPOSES THE WEB ROOT, WHICH IS THE SAME ACT ONE LAYER DOWN. The serve's
static bundle split at the carve exactly as its Python did: 42 of the 43 files
under `scripts/ideation_dashboard/web/` moved to openDox-code and ONE stayed —
`views/intent-feed.js`, openxFactory's own adapter view. `serve.py`'s
`--web-dir` defaults to its OWN packaged `web/`, so a wrapper that passed no
root would serve a tree whose `views/dispose.js:26` and `views/wheel.js:76`
both `import … from "./intent-feed.js"` — a file that is not beside them. The
server would start, `/index.html` would answer 200, and the browser's module
graph would fail on a 404 nobody sees in a log (Copilot
`PRRT_kwDOTAvnrs6hcZ8F`).

`_composed_web_root()` below builds the tree the pre-shed directory WAS, from
the manifest: `carved_reach.sources_under()` answers every row under the web
surface with where that file is today — the moved ones at the pinned leg, the
retained one here — and each is linked into its own pre-shed relative position.
So the composition is DERIVED, and the day a row moves between the legs, or a
second adapter asset stays, the served tree follows the manifest with no edit
here. An explicit `--web-dir` from the operator always wins: composing over a
root somebody chose deliberately would be the wrapper overriding its caller.
"""

import atexit
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import carved_reach  # noqa: E402

#: The pre-shed directory the served bundle was one tree at. Named here as the
#: MANIFEST SURFACE it is, not as a destination — `sources_under()` turns it
#: into today's locations, across both sides of the split.
WEB_SURFACE = "scripts/ideation_dashboard/web"


def _composed_web_root() -> Path:
    """The served static tree, re-composed from the carve manifest.

    A directory of symlinks rather than copies: nothing is duplicated on disk,
    an edit to the retained adapter asset is live in the next request the way
    it was before the shed, and the whole tree is removed at exit. Directories
    are created rather than linked, so a row that ever moves to a different
    subdirectory lands where the manifest says and not where its neighbour is.
    """
    root = Path(tempfile.mkdtemp(prefix="openxfactory-dashboard-web-"))
    atexit.register(shutil.rmtree, root, ignore_errors=True)
    for pre_shed, today in carved_reach.sources_under(WEB_SURFACE).items():
        link = root / Path(pre_shed).relative_to(WEB_SURFACE)
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(today)
    return root


def _argv_with_web_root(argv: list[str]) -> list[str]:
    """`argv`, with the composed web root appended unless one was given."""
    if any(a == "--web-dir" or a.startswith("--web-dir=") for a in argv):
        return argv
    return [*argv, "--web-dir", str(_composed_web_root())]


carved_reach.require()
carved_reach.install()
carved_reach.bind_composition_point()

from opendox.serve import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(_argv_with_web_root(sys.argv[1:])))
