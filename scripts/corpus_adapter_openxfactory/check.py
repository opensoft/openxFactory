"""This corpus's own verdict machinery, mapped onto the neutral finding shape.

WHAT CROSSES THE SEAM AND WHAT DOES NOT. Design D2 says the check operation must
NOT know "doc-health's family names, thresholds or taxonomy". It does not: a
neutral `Finding` carries a severity, a subject, an OPAQUE `code` and a message,
and this module is free to put `"<grouping>/<rule>"` inside that code string
precisely because no consumer across the seam is permitted to parse it. The
severities need no remapping at all — `doc_health` already defines exactly
`critical | error | warning | info`, which is the neutral vocabulary.

SUBJECTS ARE NORMALIZED, AND THAT IS NOT COSMETIC. The checker reports findings
against paths that are not governed documents — a pin, a tag, a workflow file —
and the interface says a finding's subject is a document identity OR the corpus
name. So a finding whose path the adapter's own listing did not return becomes a
CORPUS-WIDE finding, with its original path carried into the message rather than
dropped. A reader can always tell which it was; nothing is lost and the
interface's own rule stays literally true.

WHY `Context` IS BUILT HERE RATHER THAN THROUGH `build_context`. That helper
takes argparse arguments, so calling it would make the adapter depend on a
command-line shape. The context is a plain dataclass; building it directly is
both smaller and honest about what the verdict actually needs.

THE GROUPING NARROWING IS DATA, NOT A PRIVILEGED ROUTE. `groups=None` runs
everything this corpus knows how to check. A caller may construct a verdict over
fewer groupings — which the conformance suite does, because a full home verdict
is a two-minute run and that suite is a per-pull-request gate. Narrowing is a
construction argument any implementation of the seam may offer over its own
corpus; it adds no operation and it is reachable from no route the interface
does not define.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from doc_health import DEFAULT_THRESHOLDS, corpus as dh_corpus
from doc_health.families import FAMILIES
from doc_health.runner import Context, run_suite

# #872 (RULED OQ-Q): pinned openDox copy, not the local replica — see
# `adapter.py`'s header for the reach and the manifest reason it stays in tree.
_OPENDOX_SRC = Path(__file__).resolve().parents[2] / "openDox" / "code" / "src"
if not (_OPENDOX_SRC / "opendox" / "corpus_adapter.py").is_file():
    raise ImportError(
        "corpus_adapter_openxfactory.check: the pinned openDox corpus-adapter "
        f"interface is not at {_OPENDOX_SRC / 'opendox' / 'corpus_adapter.py'}. "
        "Run `git submodule update --init --recursive openDox` from the "
        "repository root.")
sys.path.insert(0, str(_OPENDOX_SRC))

from opendox.corpus_adapter import Finding, ResolvedCorpus

from .shape import Verdict


def _context(location: Path, name: str) -> Context:
    """One repository in scope, loaded exactly the way a self-gate run loads it."""
    docs = dh_corpus.load_docs(name, location)
    lifecycle_docs = dh_corpus.load_lifecycle_docs(name, location)
    return Context(
        repo_paths={name: location},
        docs=docs,
        capabilities={name: dh_corpus.spec_capabilities(location)},
        change_ids={name: dh_corpus.change_ids(location)},
        git=dh_corpus.RealGit(),
        thresholds=dict(DEFAULT_THRESHOLDS),
        as_of=date.today(),
        agg_root=None,
        lifecycle_docs=lifecycle_docs,
    )


def doc_health_verdict(*, groups: tuple[str, ...] | None = None) -> Verdict:
    """A `Verdict` over this repository's own checker.

    `groups` names the check groupings to run; None runs every one. An unknown
    grouping raises immediately rather than silently running nothing — a verdict
    that quietly checks less than it was asked to is the false-green shape this
    repository guards against everywhere else.
    """
    if groups is not None:
        unknown = sorted(set(groups) - set(FAMILIES))
        if unknown:
            raise ValueError(
                f"no such check grouping: {', '.join(unknown)} "
                f"(known: {', '.join(sorted(FAMILIES))})")

    def verdict(resolved: ResolvedCorpus, known_keys: frozenset,
                subjects: tuple[str, ...] | None) -> tuple[Finding, ...]:
        location = Path(resolved.location)
        name = resolved.ref.name
        ctx = _context(location, name)
        if groups is None:
            result = run_suite(ctx, None, set())
        elif len(groups) == 1:
            result = run_suite(ctx, groups[0], set())
        else:
            result = run_suite(ctx, None, set(FAMILIES) - set(groups))

        wanted = None if subjects is None else set(subjects)
        rows: list[Finding] = []
        for row in result.findings:
            if wanted is not None and row.path not in wanted:
                continue
            if row.path in known_keys:
                subject, message = row.path, row.action
            else:
                subject, message = name, f"{row.path}: {row.action}"
            rows.append(Finding(severity=row.severity, subject=subject,
                                code=f"{row.family}/{row.rule}", message=message))
        return tuple(rows)

    return verdict
