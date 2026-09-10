"""THE ONLY MODULE IN THIS PACKAGE THAT NAMES openxFactory's OWN LAYOUT.

Every root, glob, header word and prefix below is a VALUE handed to a
`CorpusShape`. Nothing here is a code path, and no other module in the package
imports this one — which is the structural half of "no privileged route": the
adapter class cannot behave differently over the home corpus, because it cannot
see it. `tests/corpus-adapter/test_no_privileged_route.py` asserts that
direction.

EVERY CONSTANT IS DERIVED WHERE A MODULE OWNS IT. `corpus_root.py` already
wrote the rule down for this exact class of value — the scanned roots are
"DERIVED from `corpus.GOVERNED_ROOTS` rather than restated, so a root added to
the doc-health scan is a root this predicate accepts" — and this repository
spends real effort killing co-authoritative constants. So the roots, the
exclusion sets and the header window all come from the modules that own them.

THE HEADER BLOCK IS THE EXCEPTION, AND THE EXCEPTION IS § 2.3 ITSELF. Until
that task the six field names were `authoring.REQUIRED_HEADER_FIELDS` and this
module imported them; the create gate then applied them with its own scan, over
`doc_health.corpus.STATUS_SCAN_LINES` — one contract with two authors in two
packages, agreeing by convention. § 2.3 inverts the direction: the field block
is a fact about THIS CORPUS's shape, so it is authored here, and the dashboard
asks `classify` for it (`design.md` § D2: "the operation `authoring.py`'s
`REQUIRED_HEADER_FIELDS` becomes, instead of a constant co-authoritative with
`doc_health.corpus.STATUS_SCAN_LINES`"). Deriving it from the dashboard now
would be a cycle, not a derivation: the dashboard's answer comes from this
value. Three values therefore cannot be derived — the field block, the kind
header's name, and the tree the block governs — and each is pinned by a parity
test in `tests/corpus-adapter/test_openxfactory_adapter.py` against the reader
or the gate that must agree with it.

THE TWO SCOPES ARE NOT MERGED, AND THAT IS A RULING, NOT A STYLE.
`govern-openspec-corpus-membership` (OQ-2, ruled 2026-08-23) settled that the
lifecycle scan set is an EXPLICIT PATTERN SET rather than a directory rule: a
directory rule "would have swept in `tasks.md`, `design.md`, the spec deltas,
`supporting-docs/` and `evidence/`", and whether those are governance documents
was left open. So they are two scopes with two exclusion sets, listed
separately, and a test asserts each one is byte-for-byte the set its owning
function returns.

WHY THE FIELD OBLIGATION IS BOUNDED BY PREFIX. The six-field header block is the
IDEATION header contract (`ideation/README.md`, "Ideation Header Format") — it
governs documents under that tree, not the whole governed corpus. Reporting a
`docs/` document as missing `Topics:` would be a FALSE FINDING, which this
repository has already learned costs more trust than a crash. The tree is named
here and `authoring.IDEATION_PREFIX` names it too, for a different question —
which tree a create may WRITE into, a gate that exists whether or not any header
is obliged there. Two questions, two definitions, one tree, and a parity test
holds them equal; importing one from the other would put back the edge § 2.3
removed and answer the second question with the first.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import NamedTuple

from doc_health import corpus

# #872 (RULED OQ-Q): pinned openDox copy, not the local replica — see
# `adapter.py`'s header for the reach and the manifest reason it stays in tree.
_OPENDOX_SRC = Path(__file__).resolve().parents[2] / "openDox" / "code" / "src"
if not (_OPENDOX_SRC / "opendox" / "corpus_adapter.py").is_file():
    raise ImportError(
        "corpus_adapter_openxfactory.home: the pinned openDox corpus-adapter "
        f"interface is not at {_OPENDOX_SRC / 'opendox' / 'corpus_adapter.py'}. "
        "Run `git submodule update --init --recursive openDox` from the "
        "repository root.")
sys.path.insert(0, str(_OPENDOX_SRC))

from opendox.corpus_adapter import CorpusRef

from .adapter import OpenxFactoryCorpusAdapter
from .check import doc_health_verdict
from .shape import CorpusShape, Scope
from .write_path import apply_lane_write_path

#: The checkout this package sits in — `scripts/<package>/home.py` is three
#: levels down from it. A caller serving another checkout of the same corpus
#: passes its own location instead.
REPO_ROOT = Path(__file__).resolve().parents[2]

#: Governance documents are Markdown.
DOCUMENT_SUFFIX = ".md"

#: The promoted-capability root. `corpus_root.SCANNED_ROOTS` adds exactly this
#: one to `corpus.GOVERNED_ROOTS`, and the parity test pins the two together.
PROMOTED_ROOT = "openspec"

#: The scope names this corpus declares, beside the interface's own `all`.
DOCUMENTS = "documents"
LIFECYCLE = "lifecycle"

#: The header a document's kind is read from. NOT derivable —
#: `doc_health.corpus.parse_kind` carries it as a literal inside its body — so
#: it is pinned by a parity test against that reader over the real corpus
#: instead.
KIND_FIELD = "Kind"

#: The header block this corpus obliges of a document under `OBLIGED_PREFIX`,
#: in the order the contract declares it (`ideation/README.md`, "Ideation Header
#: Format"). AUTHORED HERE, and the inversion is § 2.3's whole content — see the
#: module docstring. A field added here is a field the create gate enforces on
#: the next call, without a second edit anywhere.
HEADER_FIELDS: tuple[str, ...] = (
    "Status", "Kind", "Summary", "Topics", "Repository context", "Captured",
)

#: The tree `HEADER_FIELDS` governs. NOT derivable from the create gate's own
#: constant without recreating the cycle § 2.3 removed, so it is pinned equal to
#: it by a parity test instead — the same treatment `scan_roots` gets against
#: `corpus_root.SCANNED_ROOTS` under RULING OQ-4.
OBLIGED_PREFIX = "ideation/"


def home_shape(*, verdict_groups: tuple[str, ...] | None = None) -> CorpusShape:
    """This corpus's shape.

    `verdict_groups` narrows which check groupings a verdict runs; None runs
    every one. It is a construction argument, not an operation — a full verdict
    over this corpus is a two-minute run, and a caller that wants a fast one
    (the conformance suite does) asks for fewer groupings the same way any
    implementation of the seam may over its own corpus.
    """
    return CorpusShape(
        scan_roots=tuple(sorted({*corpus.GOVERNED_ROOTS, PROMOTED_ROOT})),
        scopes={
            DOCUMENTS: Scope(
                globs=tuple(f"{root}/**/*{DOCUMENT_SUFFIX}"
                            for root in corpus.GOVERNED_ROOTS),
                excluded_parts=frozenset(corpus.EXCLUDED_PARTS),
            ),
            LIFECYCLE: Scope(
                globs=tuple(corpus.LIFECYCLE_SCAN),
                # Two filters, and the second belongs to this scope alone:
                # byte-exact evidence is excluded from the lifecycle set even
                # where it matches a ruled glob, because reporting a frozen
                # record for the state it preserves is a false finding.
                excluded_parts=(frozenset(corpus.EXCLUDED_PARTS)
                                | frozenset(corpus.EVIDENCE_PARTS)),
            ),
        },
        header_scan_lines=corpus.STATUS_SCAN_LINES,
        kind_field=KIND_FIELD,
        required_fields_by_kind={None: HEADER_FIELDS},
        obliged_prefixes=(OBLIGED_PREFIX,),
        verdict=doc_health_verdict(groups=verdict_groups),
        write_path=apply_lane_write_path(),
    )


class HomeCorpus(NamedTuple):
    """A ready adapter and the reference to hand it. Two names, one call."""

    adapter: OpenxFactoryCorpusAdapter
    ref: CorpusRef


def home_corpus(location: Path | str | None = None, *,
                verdict_groups: tuple[str, ...] | None = None) -> HomeCorpus:
    """An adapter over this repository's corpus, and the reference to resolve.

    The corpus's NAME is the checkout directory's own name, which is exactly
    what `doc_health.runner.build_context` uses for a single-repository run — so
    a finding this adapter reports and a finding the checker reports name the
    same repository.
    """
    path = Path(location) if location is not None else REPO_ROOT
    shape = HOME_SHAPE if verdict_groups is None else home_shape(
        verdict_groups=verdict_groups)
    return HomeCorpus(
        adapter=OpenxFactoryCorpusAdapter(shape),
        ref=CorpusRef(name=path.name, location=str(path)),
    )


#: The shape as this repository actually stands: every check grouping, and the
#: apply lane declared and unreachable.
HOME_SHAPE = home_shape()
