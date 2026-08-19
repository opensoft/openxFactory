# Tasks: align-status-reader-to-real-lines

A shared primitive placed where the dependency direction already runs, then
EVERY reader of the lifecycle header pointed at it. Sections 1-6 below were
first realized against a NARROWER cut (`corpus.parse_status`/`parse_kind`
only); an adversarial review of that realization returned FIX-FIRST over a
spec contradiction it surfaced (the delta's "SHALL hold for every reader of
that header" vs. the narrower `code_surface:` front matter), and Brett's
same-day ruling (2026-08-19, in-session multiple choice, recommended option
adopted) resolved it WIDE: the delta governs, the narrow front matter was the
drafting error, and all six remaining pseudo-line readers convert in this
same change. Section 2a below is that conversion.

## 1. The shared primitive

- [x] 1.1 New `scripts/doc_health/lines.py` carrying the line rule: split on CR, LF
      and CRLF only, and rejoin losslessly. Carry the existing implementation from
      `ideation_dashboard/round_trip.py` rather than re-deriving it, including its
      `join(split(t)) == t` property — every guarantee stated in terms of "these bytes
      survive" depends on that pair being exact.
- [x] 1.2 Placed in `doc_health`, not `ideation_dashboard`, on the measured
      dependency direction: module-level imports run `ideation_dashboard` →
      `doc_health` at five call sites, and `doc_health` reaches back only lazily
      inside two functions marked `# lazy: house guard`. Inverting that for a text
      helper would put the checker layer downstream of the dashboard runtime and make
      those lazy back-references load-bearing.
- [x] 1.3 A dedicated module rather than more of `corpus.py`: neither the reader nor
      the writer owns the definition of a line, and this corpus has already paid for
      one three-implementation scanning hazard. A named home is how a fourth gets
      prevented instead of discovered.

## 2. The readers

- [x] 2.1 `corpus.parse_status` counts real lines through the primitive.
- [x] 2.2 `corpus.parse_kind` too — it sits beside `parse_status` with the same
      `text.splitlines()[:STATUS_SCAN_LINES]` scan and the same blindness. Fixing one
      and not the other would leave the divergence half-closed a second time, which is
      the shape this change exists to stop.
- [x] 2.3 Sweep for any further reader using the same idiom before declaring the set
      complete — grep `splitlines()[:` across `scripts/`, and record what was found so
      the next reader knows the sweep happened rather than re-running it. UPDATED under
      the wide ruling: the sweep record in `corpus.py` now also states the six sites
      were converted (2a below), not deferred.

## 2a. The wide-scope conversion (FIX-FIRST review, Brett's ruling 2026-08-19)

Findings C1-C3 from the adversarial review, demonstrated with commands: a
U+2028-heavy ratified doc got a real `Status:`/provenance line from `corpus`
but a false CRITICAL finding from `families` reading the SAME header through a
different, wider window (C1); `doxbench_packet.lifecycle_status`'s own comment
claimed a rule it did not follow (C2); `families._scan_lines` was a live
second Python line rule, making "reduces the Python side to one" false (C3).
Reviewer-measured baseline cost of converting all of it: 1227 governed
aggregation files, zero exotic separators, zero window differences, zero
value changes.

- [x] 2a.1 `families._header_line` (families.py) converts to
      `doc_health.lines.split_keepends`. Closes C1: `fam_ratified_provenance`,
      `fam_standard_backing`, `fam_succession_integrity` all read through this
      one function, so all three stop disagreeing with `corpus.parse_status`
      about where the header ends.
- [x] 2a.2 `families._scan_lines` (families.py) converts too — the UNBOUNDED
      second Python line rule C3 named, not caught by the `splitlines()[:`
      grep pattern because it has no window slice. Its fence-toggle PREDICATE
      (the naive ``` check) is a separate, narrower rule and stays as its own
      textually-pinned spelling (`test_the_shared_predicate_is_spelled_the_same_in_all_three`)
      — only the line-splitting underneath it converts.
- [x] 2a.3 `inventory._header_value`, `organizer_dispatch._header_value`
      (doc_health) convert.
- [x] 2a.4 `doxbench_packet.lifecycle_status`, `authoring.missing_required_headers`,
      `generator._header_value` (ideation_dashboard) convert, at module-level
      imports (the established clean direction: `ideation_dashboard` →
      `doc_health`).
- [x] 2a.5 `doc_health/lines.py`'s module docstring and the `corpus.py` sweep
      comment (C4) are rewritten to state the CURRENT set of converted readers
      and the ruling, not the narrow cut's "deliberately untouched" framing.
- [x] 2a.6 The proposal's `code_surface:` front matter widens to the full
      reader list; the `Ratified:` line gets the second ruling appended in
      house style; the APPROVED-BUT-NOT-YET-REALIZED banner (C5) is reworded
      truthfully — it is not dropped, its factual claims are corrected to
      match what this branch actually built.

## 3. The writer stops carrying its own copy

- [x] 3.1 `ideation_dashboard/round_trip.py` imports the primitive instead of
      defining `split_keepends` / `join_rows`. Its module docstring's explanation of
      WHY the rule exists moves with it — the reasoning is the valuable part and must
      not be left behind on a re-export.
- [x] 3.2 `gate_console._flip_status` follows whatever `round_trip` re-exports, so
      the writer's behavior is unchanged by construction. Assert that: the two
      demonstrated damages must stay closed.

## 4. Tests

- [x] 4.1 A U+2028-bearing header parses: the status is found, and the document is
      NOT reported as lacking one. This is the false-finding shape and it is the
      test the change exists for.
- [x] 4.2 The 15-line window counts real lines — a document whose pseudo-line count
      exceeds the window while its real-line count does not.
- [x] 4.3 `parse_kind` gets the same coverage as `parse_status`, so 2.2 cannot
      silently regress.
- [x] 4.4 The `join(split(t)) == t` property travels with the primitive, over the
      same ending shapes it is asserted on today.
- [x] 4.5 The existing three-way fence agreement test still passes. LEGITIMATELY
      re-ticked after 2a.2: with `families._scan_lines` now sharing
      `round_trip.py`'s exact line-split primitive, the LINE-COUNTING half of what
      `test_all_three_fence_implementations_agree` compares is ONE Python
      behavior (not two independently-splitting ones) against JS — two
      implementations, not three. The naive ```` ```-fence-toggle PREDICATE
      itself is unaffected and stays three textually independent spellings
      (`test_the_shared_predicate_is_spelled_the_same_in_all_three`), which is a
      different, narrower rule this change does not touch. The test module's
      docstring is updated to say this precisely rather than conflate the two.
- [x] 4.6 The two demonstrated writer damages stay closed (form feed in a `Status:`
      line; exotic separators overrunning the window).
- [x] 4.7 (C1) `families._header_line`'s false-finding shape, reproduced: a
      ratified document whose header carries an exotic separator gets
      `corpus.parse_status` == "ratified" but must NOT get a false
      `ratified-provenance` "missing" finding from `families`. MUTATION-CHECKED:
      reverting `_header_line` alone to `splitlines()` must fail this test.
- [x] 4.8 (C2) `doxbench_packet.lifecycle_status` agreement with
      `corpus.parse_status`, made NON-VACUOUS with a SYNTHETIC exotic-separator
      fixture — the existing real-corpus-only agreement test
      (`test_the_status_read_agrees_with_the_repositorys_own_corpus_reader`)
      passes vacuously because the corpus itself carries no exotic separator
      (the 0-of-1227 measurement), so it proves nothing about the two readers'
      RULES agreeing, only that today's corpus doesn't exercise the
      disagreement.
- [x] 4.9 (C6) `test_round_trip.py`'s scheduled `ends_inside_fence` upgrade,
      built: a form-feed fence fixture and a U+2028 fence fixture added to
      `ENDS_FENCE_FIXTURES`, and the docstring's stale "blocked ... which this
      change deliberately does not touch" corrected — this branch removed that
      blocker.

## 5. Gates

- [x] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate align-status-reader-to-real-lines
      --strict`, then `--all --strict`, from the `openxFactory/` root.
- [x] 5.2 `python3 -m pytest tests/doc-health -q` and `tests/ideation-dashboard -q` —
      exit codes read DIRECTLY. `tests/doc-health` carries four known pre-existing
      `test_client_identity_composition.py` failures; enumerate and assert the set is
      unchanged rather than counting.
- [x] 5.3 doc-health full run diffed against a baseline: findings MUST be IDENTICAL.
      RE-RUN after 2a's conversion, since `families.py`/`inventory.py` are now
      changed readers too and this gate carries real information again — a
      moved finding means a corpus document carries a separator the
      0-of-1227 aggregation-wide measurement did not see, and that is a
      reason to stop and explain, not to accept the diff.

## 6. Bookkeeping

- [x] 6.1 README "OpenSpec Records" active block — done at proposal time.
- [ ] 6.2 Realization evidence recorded at the archive gate; `implementation_pending`
      means this does NOT archive on landing the requirement.

## 7. Deferred (recorded, not done)

- [ ] 7.1 (reviewer P2, OPTIONAL) A bounded split so `parse_status` stops
      materializing whole documents (e.g. a separate `first_rows(text, n)`
      helper with its own property test) — SKIPPED. Reason, honestly: every
      call site in this change's scope already reads the whole document into
      memory before calling a header reader (`load_docs`, `families.py`'s
      per-doc scans, the ideation-dashboard readers all take an in-memory
      `text: str`), so a bounded split would save no allocation any caller
      here actually avoids, and building `first_rows` correctly (its own
      `join(split(t))==t`-shaped exactness proof over a PREFIX rather than the
      whole text) is real, non-trivial work for a saving nothing currently
      measures. Not invented as a gate excuse — no gate forbids this; it is
      deferred because it is unbuilt and its cost was not judged worth paying
      in this change.
