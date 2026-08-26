"""The staged-topic health fixture shapes (add-staging-workbench).

ONE definition of "ready", "blocked", and "underdone", shared by the scoring
tests, the readiness-gate tests, and the branch-session harness's scratch repo.

It lives in a PLAINLY NAMED module rather than in `conftest.py` deliberately (PR
#49 review finding 19a). `session_fixtures.build_scratch_repo` used to reach these
shapes with `from conftest import staging_fragment` executed inside the fixture
BODY, and `conftest` is an ambient name: pytest deletes `sys.modules["conftest"]`
before importing each directory's conftest, so at fixture time that name resolves
to whichever conftest was imported LAST. Collection order therefore decided
whether the harness found its own shapes — running
`pytest tests/ideation-dashboard/... tests/doc-health/...` in that order raised
`ImportError: cannot import name 'staging_fragment' from 'conftest'` at setup.
A distinct module name is unambiguous regardless of collection order, and
`conftest.py` re-exports both functions so `from conftest import staging_fragment`
keeps working for the test modules that already spell it that way.
"""

from __future__ import annotations


def staging_fragment(title: str, topics: str, *, resolved: bool = True,
                     markers: tuple[str, ...] = ()) -> str:
    """A feat-spec-shaped staging fragment (`Kind: staging-packet`) carrying
    every expected structural element and a body past the length threshold, so
    with both defaults its completeness score sits ABOVE `READY_MIN_SCORE` with
    ZERO standing open items — i.e. a topic whose health is `ready`.

    `resolved=False` leaves its two open questions STANDING (the heading drops
    its resolution annotation); `markers` appends literal standing-marker lines
    (`TODO`/`TBD`/`FIXME`/`??`) to the body. Either one blocks the topic."""
    questions = ("## Open questions — resolved 2026-07-25" if resolved
                 else "## Open questions")
    marker_block = ("\n" + "\n".join(f"- {m}" for m in markers) + "\n") if markers else ""
    return (
        f"# {title}\n"
        "\n"
        "Status: staged\n"
        "Kind: staging-packet\n"
        f"Summary: Fixture staging fragment for {topics} — the readiness gate's\n"
        "worked-to-done shape.\n"
        f"Topics: {topics}\n"
        "Repository context: fixture-repo\n"
        "Captured: 2026-07-25\n"
        "\n"
        "## Target capability\n"
        "\n"
        f"The fixture capability `{topics}` this fragment exits into. The gate\n"
        "reads the topic folder's own corpus documents and nothing else, so this\n"
        "fragment alone decides the topic's health. It is deliberately long\n"
        "enough to clear the length saturation threshold without padding, and\n"
        "structured enough to present every element the staging kind expects.\n"
        "\n"
        "## Claims\n"
        "\n"
        "1. A staged fragment worked to done presents its target capability, its\n"
        "   claims, its questions, and its exit path, and leaves no standing\n"
        "   open item behind for the next reader to rediscover.\n"
        "2. Structural doneness is a deterministic property of the pinned tree,\n"
        "   which is what lets one scoring pass serve both the rendered health\n"
        "   indicator and the gate's refusal message.\n"
        "3. The human judgment stays human: clearing the gate is permission to\n"
        "   decide, never the decision itself.\n"
        "\n"
        f"{questions}\n"
        "\n"
        "1. Whether the fixture corpus needs a second staged topic — settled by\n"
        "   giving each gate case its own folder rather than mutating one.\n"
        "2. Whether the fragment should carry a longer body — settled by writing\n"
        "   enough prose here to sit past the saturation threshold, so the length\n"
        "   signal is not what any assertion turns on.\n"
        f"{marker_block}"
        "\n"
        "## Exit\n"
        "\n"
        "An OpenSpec change authored from this fragment, reviewed and ratified\n"
        "through the ordinary lane.\n"
    )


def thin_fragment(title: str, topics: str) -> str:
    """A header-complete staging fragment with NO sections and a one-line body:
    ZERO standing open items, but a completeness score BELOW `READY_MIN_SCORE`
    — the gate's "every question closed, document still underdone" case."""
    return (
        f"# {title}\n"
        "\n"
        "Status: staged\n"
        "Kind: staging-packet\n"
        "Summary: Fixture staging fragment that is barely started.\n"
        f"Topics: {topics}\n"
        "Repository context: fixture-repo\n"
        "Captured: 2026-07-25\n"
        "\n"
        "One line of body, no sections, nothing left standing.\n"
    )
