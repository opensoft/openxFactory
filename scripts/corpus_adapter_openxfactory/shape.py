"""The construction DATA an `OpenxFactoryCorpusAdapter` is built from.

THE ONE DESIGN DECISION THAT MAKES THE SEAM'S FOURTH REQUIREMENT TESTABLE.
`corpus-adapter-seam`'s fourth requirement forbids openxFactory's own adapter
any route the interface does not define — "no privileged direct call, no bypass
of the interface for `openxFactory`'s own corpus". A class that carried the home
layout in its own body would have exactly that route: a literal, unreachable
from outside and untestable against any other corpus. So the class carries NO
path literal and NO home special case. The layout is a `CorpusShape` VALUE, one
of several, and `home.py` is simply the module that builds one of them.

That is what lets design D6 part 3's neutral conformance corpus — "no
`openspec/`, no `contracts/`, no lifecycle headers" — be served by the SAME
class with no `if home:` branch anywhere, which the design calls "the only
mechanical proof that `corpus-adapter-seam`'s no-privileged-route requirement
holds for the home corpus". A hardcoded scan root would make the home adapter
refuse that corpus, and the proof would simply be unavailable.

Nothing in this module names a path, a header word or a governance noun; every
one of those arrives as a value at construction time. `tests/corpus-adapter/
test_no_home_vocabulary.py` enforces it, and `home.py` and `write_path.py` are
the two modules exempted from that scan because naming this repository's own
layout is precisely their job.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

from corpus_adapter import Finding, ResolvedCorpus

#: What a verdict provider is handed, and what it gives back.
#:
#: `(resolved corpus, known_keys, subjects) -> neutral findings`. `known_keys`
#: is the set of identities the adapter's own listing returned, so a provider
#: can tell a finding about a listed document from a finding about the corpus at
#: large; `subjects` is None for "the whole corpus" and otherwise the identities
#: the caller asked about. A corpus with no verdict machinery declares None and
#: the adapter honestly answers with an empty result — which the interface says
#: is an answer, not a refusal.
Verdict = Callable[
    [ResolvedCorpus, frozenset, tuple[str, ...] | None], tuple[Finding, ...]]


@dataclass(frozen=True)
class Scope:
    """One declared scope: which globs it resolves, and what it drops.

    The exclusion set is PER SCOPE rather than shared, because this repository
    already learned that two scopes over one tree can have deliberately
    different membership rules and that merging them is a defect
    (`govern-openspec-corpus-membership`, ruled 2026-08-23). One field, two
    values, no union.
    """

    globs: tuple[str, ...]
    excluded_parts: frozenset[str] = frozenset()


@dataclass(frozen=True)
class WriteProposal:
    """What a caller proposes: the whole of it, and nothing about how."""

    document_key: str
    content: bytes
    actor: str
    basis_revision: str
    reason: str = ""


@dataclass(frozen=True)
class WritePath:
    """A corpus's DECLARED governed write path, as an injectable descriptor.

    The adapter never learns what the path IS. It asks this object for the
    request artifact and the correlation identifier, hands the artifact to
    `dispatch`, and returns a receipt.

    `dispatch is None` means DECLARED AND UNREACHABLE — which is the state this
    repository's own path is in today, and the reason the interface carries a
    `write_path_available` flag at all. Flipping it is one construction
    argument, not a code path, so the task that hardens the path turns a
    refusal into a receipt without touching the adapter.

    `routes` answers whether one document identity has a target on this path at
    all; None from it is a refusal naming the path, never a fallback write.
    """

    name: str
    build_request: Callable[[WriteProposal], Mapping]
    correlation_id: Callable[[Mapping], str]
    routes: Callable[[str], str | None]
    dispatch: Callable[[Mapping, WriteProposal], None] | None = None
    unavailable_reason: str = ""

    @property
    def available(self) -> bool:
        return self.dispatch is not None


@dataclass(frozen=True)
class CorpusShape:
    """Everything an `OpenxFactoryCorpusAdapter` needs in order to serve ONE
    corpus, and the only thing it is constructed from.

    `scan_roots` is the STRUCTURAL test `resolve` applies: a tree holding none
    of them cannot be this corpus. `scopes` drives every listing. `kind_field`
    names the header a document's kind is read from; a document that carries no
    value for it is UNCLASSIFIABLE — reported, named, and still listed.

    `required_fields_by_kind`'s `None` key is the DEFAULT: the fields obliged of
    a kind not separately listed, and of an unclassifiable document too. That
    second half matters — a document missing the kind header is missing a
    required field, so the same answer covers both, and the parity test against
    this repository's own header reader depends on it.

    `obliged_prefixes` bounds WHERE the field obligation applies. Empty means
    everywhere. It exists because a corpus can carry one header contract over
    part of itself and none over the rest, and reporting the rest as
    field-incomplete would be a false finding — the failure class this
    repository has paid for before.
    """

    scan_roots: tuple[str, ...]
    scopes: Mapping[str, Scope]
    header_scan_lines: int
    kind_field: str | None = None
    required_fields_by_kind: Mapping = None  # type: ignore[assignment]
    obliged_prefixes: tuple[str, ...] = ()
    verdict: Verdict | None = None
    write_path: WritePath | None = None

    def __post_init__(self) -> None:
        if self.required_fields_by_kind is None:
            object.__setattr__(self, "required_fields_by_kind", {})
