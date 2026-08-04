"""The browser-signal oracle for the branch-session Playwright smoke (T088).

It lives here rather than inside `specs/007-workbench-branch-sessions/playwright-smoke.py`
so it can be UNIT-TESTED without a browser (`test_smoke_signals.py`). The smoke
itself is not collected by pytest — CI has no `node` — which is exactly how its
oracle came to be the weakest link in the branch's evidence.

PR #49 adversarial review finding 19b, on the version this replaces: the
"accounted-for" declaration was a bare substring FILTER over the whole signal
text, and the run printed the number of DECLARATIONS rather than the number of
OBSERVATIONS. So the claim in the realization note — "a single HTTP 404 (plus its
ERR_ABORTED twin) on `/source/<repo>%40main/<created path>`" — was not encoded
anywhere: zero events at that URL, five duplicates, an HTTP 500 at that URL, or an
unrelated `TypeError` whose text merely mentioned the URL all satisfied the
verdict identically, and the printed line read `1` in every case.

Here a declaration is an ASSERTION with three parts, and all three must hold:

  * **which URL** — the substring, as before;
  * **which ANSWER** — the console error must name the declared HTTP status, so a
    500 where a 404 was declared is UNEXPECTED rather than absorbed;
  * **how MANY** — per channel, an exact expected count. Zero observations fail
    (a silently-vanished 404 means the ratified task-5.8 viewer jump changed and
    the note is stale), and so do duplicates.

`pageerror` stays entirely unfilterable: an uncaught exception or a failed module
load is never a server answer, and no declaration can excuse one.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

# The channels a declaration can account for. `pageerror` is deliberately absent.
CONSOLE = "console_error"
REQUEST_FAILED = "requestfailed"
PAGE_ERROR = "pageerror"


@dataclass
class Declared:
    """One expected SERVER ANSWER, declared before the run reaches it.

    `console` / `requestfailed` are the EXACT number of signals the answer must
    produce on each channel. `status` is the HTTP status the console error must
    name; `failure_contains` is the network failure text its `requestfailed` twin
    must carry (Chromium reports `net::ERR_ABORTED` for a response body the page
    deliberately never reads)."""

    url_contains: str
    why: str
    status: int = 404
    console: int = 1
    requestfailed: int = 1
    failure_contains: str = "ERR_ABORTED"
    observed: dict[str, list[str]] = field(default_factory=dict)

    def expected(self, channel: str) -> int:
        return self.console if channel == CONSOLE else self.requestfailed

    def matches(self, channel: str, text: str) -> bool:
        if self.url_contains not in text:
            return False
        if channel == CONSOLE:
            # the STATUS must be named: "…responded with a status of 404…". A
            # different status at the same URL is a different answer and must not
            # be absorbed by this declaration.
            return re.search(rf"\b{self.status}\b", text) is not None
        if channel == REQUEST_FAILED:
            return self.failure_contains in text
        return False


class Errors:
    """Every browser-side signal, and the verdict on them.

    A signal is UNEXPECTED unless some declaration matches it on its channel; a
    declaration is UNSATISFIED unless the number of signals it matched is exactly
    the number it declared. `clean()` requires both to be empty, so the run's
    exit code encodes the accounted-for claim instead of merely printing it."""

    def __init__(self) -> None:
        self.page_errors: list[str] = []
        self.console_errors: list[str] = []
        self.failed_requests: list[str] = []
        self.accounted: list[Declared] = []

    # ---- declaration ----
    def account(self, substring: str, why: str, **expectations) -> Declared:
        declared = Declared(url_contains=substring, why=why, **expectations)
        self.accounted.append(declared)
        return declared

    # ---- collection ----
    def wire(self, page) -> None:
        page.on("pageerror", lambda e: self.page_errors.append(str(e)))
        page.on("console", lambda m: (self.console_errors.append(
            f"{m.type}: {m.text} @ {m.location}") if m.type == "error" else None))
        page.on("requestfailed", lambda r: self.failed_requests.append(
            f"{r.method} {r.url} — {r.failure}"))

    def _channels(self) -> dict[str, list[str]]:
        return {CONSOLE: self.console_errors, REQUEST_FAILED: self.failed_requests}

    # ---- the verdict ----
    def observations(self) -> dict[str, list[str]]:
        """Every signal each declaration actually matched, keyed
        `"<url_contains>|<channel>"`. Recomputed from the collected lists, so the
        order of `account()` relative to the events never matters."""
        seen: dict[str, list[str]] = {}
        for declared in self.accounted:
            declared.observed = {}
            for channel, signals in self._channels().items():
                matched = [s for s in signals if declared.matches(channel, s)]
                declared.observed[channel] = matched
                seen[f"{declared.url_contains}|{channel}"] = matched
        return seen

    def unexpected(self) -> dict[str, list[str]]:
        """Signals no declaration accounts for. `pageerror` is never filtered."""
        self.observations()
        out = {PAGE_ERROR: list(self.page_errors)}
        for channel, signals in self._channels().items():
            out[channel] = [s for s in signals
                            if not any(d.matches(channel, s) for d in self.accounted)]
        return out

    def unsatisfied(self) -> list[dict]:
        """Declarations whose observed count is not the declared count — the half
        the old filter could not see at all."""
        self.observations()
        out: list[dict] = []
        for declared in self.accounted:
            for channel in self._channels():
                expected = declared.expected(channel)
                matched = declared.observed.get(channel, [])
                if len(matched) != expected:
                    out.append({"url_contains": declared.url_contains,
                                "channel": channel, "expected": expected,
                                "observed": len(matched), "why": declared.why,
                                "signals": matched})
        return out

    def clean(self) -> bool:
        return not any(self.unexpected().values()) and not self.unsatisfied()

    # ---- reporting ----
    def observed_total(self) -> int:
        """How many signals the declarations actually MATCHED — the number the run
        used to print `len(self.accounted)` for."""
        return sum(len(v) for v in self.observations().values())

    def expected_total(self) -> int:
        return sum(d.expected(c) for d in self.accounted for c in self._channels())

    def summary_line(self) -> str:
        return (f"accounted-for server answers: {self.observed_total()} observed "
                f"/ {self.expected_total()} declared across "
                f"{len(self.accounted)} declaration(s)")

    def report(self) -> str:
        return json.dumps({
            "unexpected": self.unexpected(),
            "unsatisfied_declarations": self.unsatisfied(),
            "accounted_for": [
                {"url_contains": d.url_contains, "why": d.why,
                 "expects": {c: d.expected(c) for c in self._channels()},
                 "observed": {c: len(d.observed.get(c, [])) for c in self._channels()}}
                for d in self.accounted],
            "all_console_errors": self.console_errors,
            "all_failed_requests": self.failed_requests,
        }, indent=2)
