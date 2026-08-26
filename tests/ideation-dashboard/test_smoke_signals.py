"""The Playwright smoke's browser-signal ORACLE, tested without a browser
(007-workbench-branch-sessions T088; PR #49 adversarial review finding 19b).

The smoke itself is not collected — CI has no `node` — so its verdict was the one
piece of this branch's evidence that nothing checked. Finding 19b measured what
that verdict could not distinguish: with the task-5.8 URL declared, a bare
substring filter returned `clean=True` for the expected single 404 AND for an HTTP
500 at the same URL, AND for five duplicate 404s, AND for ZERO events, AND for an
unrelated `TypeError` whose text merely mentioned the URL — while printing
`accounted-for server answers: 1` in every one of those cases, because it printed
the number of DECLARATIONS rather than observations.

Each scenario below is one of those five, inverted: the four that must now FAIL do
fail, the baseline still passes, and the two controls the finding used to bound the
blast radius (`pageerror` unfilterable, a wrong URL still unexpected) still hold.
The printed line now reports OBSERVATIONS, which is asserted too.
"""

from __future__ import annotations

import json

from smoke_signals import CONSOLE, PAGE_ERROR, REQUEST_FAILED, Errors

# the shapes Chromium actually produces, in the exact strings `Errors.wire`
# assembles them from (`f"{m.type}: {m.text} @ {m.location}"` and
# `f"{r.method} {r.url} — {r.failure}"`).
URL = "/source/openxFactory%40main/ideation/staging/demo-topic/session-smoke-note.md"
WHY = "task 5.8 opens the created document on a main-keyed page (FR-001/FR-014a)"


def console_status(url: str, status: int, phrase: str = "Not Found") -> str:
    return (f"error: Failed to load resource: the server responded with a status "
            f"of {status} ({phrase}) @ {{'url': 'http://127.0.0.1:8000{url}', "
            "'lineNumber': 0, 'columnNumber': 0}")


def aborted(url: str) -> str:
    return f"GET http://127.0.0.1:8000{url} — net::ERR_ABORTED"


def declared() -> Errors:
    errors = Errors()
    errors.account(URL, WHY, status=404, console=1, requestfailed=1)
    return errors


# --------------------------------------------------------------------------
# the baseline the realization note claims
# --------------------------------------------------------------------------

def test_the_declared_single_404_and_its_aborted_twin_is_clean():
    errors = declared()
    errors.console_errors.append(console_status(URL, 404))
    errors.failed_requests.append(aborted(URL))

    assert errors.clean() is True
    assert errors.unsatisfied() == []
    assert errors.unexpected() == {PAGE_ERROR: [], CONSOLE: [], REQUEST_FAILED: []}
    assert errors.observed_total() == 2 and errors.expected_total() == 2


def test_the_summary_line_reports_observations_not_declarations():
    """The old line read `1` whether the event happened zero, one, or five times."""
    errors = declared()
    assert "0 observed / 2 declared" in errors.summary_line()

    errors.console_errors.append(console_status(URL, 404))
    errors.failed_requests.append(aborted(URL))
    assert "2 observed / 2 declared" in errors.summary_line()
    assert "1 declaration(s)" in errors.summary_line()


def test_a_declaration_accounts_for_events_that_arrive_before_it_is_made():
    """`account()` is called mid-run, so the verdict is recomputed from the
    collected lists rather than counted as events arrive."""
    errors = Errors()
    errors.console_errors.append(console_status(URL, 404))
    errors.failed_requests.append(aborted(URL))
    errors.account(URL, WHY)
    assert errors.clean() is True


# --------------------------------------------------------------------------
# the four blindnesses finding 19b measured — all of them now fail
# --------------------------------------------------------------------------

def test_a_500_at_the_declared_url_is_not_absorbed():
    """The declaration names an ANSWER, not just a URL: a server error where a
    404 was declared is a defect, and used to be filtered away."""
    errors = declared()
    errors.console_errors.append(console_status(URL, 500, "Internal Server Error"))
    errors.failed_requests.append(aborted(URL))

    assert errors.clean() is False
    assert errors.unexpected()[CONSOLE] == [console_status(URL, 500,
                                                          "Internal Server Error")]
    # and the 404 it declared never happened, which is reported separately
    gaps = {(g["channel"], g["observed"]) for g in errors.unsatisfied()}
    assert (CONSOLE, 0) in gaps


def test_duplicate_declared_404s_are_not_absorbed():
    """"A single HTTP 404" is a COUNT claim. Five satisfied the old filter."""
    errors = declared()
    for _ in range(5):
        errors.console_errors.append(console_status(URL, 404))
    errors.failed_requests.append(aborted(URL))

    assert errors.clean() is False
    gap = next(g for g in errors.unsatisfied() if g["channel"] == CONSOLE)
    assert gap["expected"] == 1 and gap["observed"] == 5
    assert errors.unexpected()[CONSOLE] == [], (
        "duplicates are an UNSATISFIED declaration, not unaccounted signals")


def test_a_declared_answer_that_never_happens_fails_the_run():
    """The important direction, and the one a filter can never see: if the 404
    stops happening, the ratified task-5.8 jump changed and the realization note
    is stale. Silence must not read as success."""
    errors = declared()

    assert errors.clean() is False
    assert [(g["channel"], g["expected"], g["observed"]) for g in errors.unsatisfied()] == [
        (CONSOLE, 1, 0), (REQUEST_FAILED, 1, 0)]
    assert not any(errors.unexpected().values()), (
        "nothing arrived — the failure is the MISSING declared answer")


def test_an_unrelated_console_error_mentioning_the_url_is_not_absorbed():
    """A real page defect whose message happens to quote the URL used to be
    filtered out entirely, because the filter looked at nothing else."""
    errors = declared()
    errors.console_errors.append(console_status(URL, 404))
    errors.failed_requests.append(aborted(URL))
    defect = (f"error: TypeError: cannot read properties of null while loading {URL} "
              "@ {'url': 'http://127.0.0.1:8000/views/viewer.js'}")
    errors.console_errors.append(defect)

    assert errors.clean() is False
    assert errors.unexpected()[CONSOLE] == [defect]


# --------------------------------------------------------------------------
# the bounds the finding credited, still held
# --------------------------------------------------------------------------

def test_a_page_error_is_never_filtered_even_at_the_declared_url():
    """An uncaught exception or a failed module load is never a server answer, so
    no declaration can excuse one — `pageerror` has no filter at all."""
    errors = declared()
    errors.console_errors.append(console_status(URL, 404))
    errors.failed_requests.append(aborted(URL))
    errors.page_errors.append(f"Error: boom while fetching {URL}")

    assert errors.clean() is False
    assert errors.unexpected()[PAGE_ERROR] == [f"Error: boom while fetching {URL}"]


def test_a_failure_at_another_url_stays_unexpected():
    errors = declared()
    errors.console_errors.append(console_status(URL, 404))
    errors.failed_requests.append(aborted(URL))
    other = console_status("/actions/gate/open-pr", 500, "Internal Server Error")
    errors.console_errors.append(other)

    assert errors.clean() is False
    assert errors.unexpected()[CONSOLE] == [other]


def test_a_requestfailed_with_an_undeclared_failure_reason_is_unexpected():
    """The twin is declared as an ERR_ABORTED — a connection reset at the same URL
    is a different event and must not inherit the declaration."""
    errors = declared()
    errors.console_errors.append(console_status(URL, 404))
    reset = f"GET http://127.0.0.1:8000{URL} — net::ERR_CONNECTION_RESET"
    errors.failed_requests.append(reset)

    assert errors.clean() is False
    assert errors.unexpected()[REQUEST_FAILED] == [reset]


# --------------------------------------------------------------------------
# the report a failing run prints
# --------------------------------------------------------------------------

def test_the_report_carries_the_gap_and_every_raw_signal():
    errors = declared()
    errors.console_errors.append(console_status(URL, 500, "Internal Server Error"))
    payload = json.loads(errors.report())

    assert payload["unsatisfied_declarations"], payload
    assert payload["accounted_for"][0]["expects"] == {CONSOLE: 1, REQUEST_FAILED: 1}
    assert payload["accounted_for"][0]["observed"] == {CONSOLE: 0, REQUEST_FAILED: 0}
    # the raw channels are printed in full, unfiltered, as they always were
    assert payload["all_console_errors"] == [console_status(URL, 500,
                                                           "Internal Server Error")]


# `test_the_smoke_imports_this_oracle_rather_than_defining_its_own` stayed with
# `specs/007-workbench-branch-sessions/playwright-smoke.py` in codexFactory
# (adopt-neutral-tooling-home tranche B, 2026-08-03): the Playwright smoke lives
# in that Speckit engineering surface, which is not part of the ratified move,
# so the pin that reads it lives beside it. NOTE for tranche C: the smoke
# imports `smoke_signals` from THIS suite, which now lives in openxFactory —
# the shedding change must repoint or adopt it.
