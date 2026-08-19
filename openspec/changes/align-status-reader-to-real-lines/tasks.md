# Tasks: align-status-reader-to-real-lines

Small change, one careful part: a shared primitive placed where the dependency
direction already runs, then two readers pointed at it.

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
      the next reader knows the sweep happened rather than re-running it.

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
- [x] 4.5 The existing three-way fence agreement test still passes and now holds two
      implementations rather than three — the JavaScript side cannot import Python, so
      that divergence remains and stays held by the test.
- [x] 4.6 The two demonstrated writer damages stay closed (form feed in a `Status:`
      line; exotic separators overrunning the window).

## 5. Gates

- [x] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate align-status-reader-to-real-lines
      --strict`, then `--all --strict`, from the `openxFactory/` root.
- [x] 5.2 `python3 -m pytest tests/doc-health -q` and `tests/ideation-dashboard -q` —
      exit codes read DIRECTLY. `tests/doc-health` carries four known pre-existing
      `test_client_identity_composition.py` failures; enumerate and assert the set is
      unchanged rather than counting.
- [x] 5.3 doc-health full run diffed against a baseline: findings MUST be IDENTICAL.
      This is the one gate that carries real information for this change — a moved
      finding means a corpus document carries a separator the 0-of-1079 measurement
      did not see, and that is a reason to stop and explain, not to accept the diff.

## 6. Bookkeeping

- [x] 6.1 README "OpenSpec Records" active block — done at proposal time.
- [ ] 6.2 Realization evidence recorded at the archive gate; `implementation_pending`
      means this does NOT archive on landing the requirement.
