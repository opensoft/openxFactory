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
same change. Section 2a below is that conversion. A FOCUSED RE-VERIFY of that
realization found four further mechanical items (findings F1-F4; F4 falls
under the already-ruled wide scope, no new ruling needed) — section 2b. A
SECOND focused re-verify, running the sweep method `corpus.py`'s own comment
now prescribes (bare `splitlines()` over document text, not just the
`[:N]`-windowed idiom), found one more survivor (F5, also under the
already-ruled wide scope) plus a mis-pointing docstring (F6) and confirmed
the remaining hits are genuinely out of scope — section 2c.

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

## 2b. Focused re-verify round 2 (findings F1-F4, 2026-08-19)

No new ruling needed — F4 falls under the already-ruled wide scope (every
reader of a lifecycle header). Four mechanical items from a focused
re-verify of round 2a's dispositions.

- [x] 2b.1 (F4, IN SCOPE) `ideation_dashboard.completeness._Prepared.lines`
      converts to `doc_health.lines.split_keepends`: `_has_header` reads the
      SAME six lifecycle header fields, in the SAME 15-line window, as
      `authoring.missing_required_headers` and `corpus.parse_status`, and its
      own comment already claimed the mirror. Demonstrated: same document,
      `authoring` said the header block COMPLETE, `completeness` said
      `governance_header_block` ABSENT. Converting `.lines` itself (not
      `_has_header` alone) fixes every consumer coherently — `_headings`,
      `_has_heading`, the `h1_title`/`section` checks, and
      `_open_question_items` all already treated `.lines` as an opaque
      `Sequence[str]`. The module's stated "imports `re` and nothing else"
      purity claim is corrected to admit `doc_health.lines` (itself pure),
      and the AST-based purity test is updated to match and to assert
      `doc_health.lines`'s own import set stays `{__future__, re}`.
- [x] 2b.2 The SWEEP BLIND SPOT that hid F4 recorded: `p.lines[:HEADER_WINDOW]`
      puts the `splitlines()` call and the window slice on different source
      lines, so `grep "splitlines()\[:"` cannot match either. Recorded in
      `corpus.py`'s sweep comment: the next sweep should grep bare
      `splitlines()` over document text generally, not just the windowed
      idiom.
- [x] 2b.3 MUTATION GAP closed: `inventory._header_value`,
      `organizer_dispatch._header_value`, `generator._header_value`, and
      `authoring.missing_required_headers` had NO dedicated test at all — the
      reviewer reverted all four simultaneously and nothing failed. One
      shared exotic-fixture test per package added
      (`tests/doc-health/test_header_value_readers.py` for the doc-health
      pair, `tests/ideation-dashboard/test_header_value_readers.py` for the
      ideation-dashboard pair), each with an embedded mutation-check test,
      PLUS a live source-level one-at-a-time revert of all four (each
      reverted alone, confirmed to fail exactly the test it should, restored)
      as a manual verification pass.
- [x] 2b.4 (F1) The false claim that `outline-model.js`'s `outlineSections`
      splits on the same real-line regex as `endsInsideFence`/`insertSection`
      — corrected in `test_round_trip.py`. `outlineSections` is LF-only
      (`text.split("\n")` at outline-model.js:46); the real-line regex lives
      only at :273/:319. Demonstrated divergent on a CR-only document. The
      JS-internal inconsistency is pre-existing, out of scope, and held by
      NO test here (no fixture in this suite carries a bare CR) — not
      claimed to be fixed or pinned, and the JS itself is not touched.
- [x] 2b.5 (F2/F3) Three prose spots corrected that overclaimed the Python
      line-split side was now singular while `families._template_gaps`
      (two of its own unbounded `text.splitlines()` loops, demonstrated
      divergent on a form-feed fragment) survives unconverted:
      `doc_health/lines.py`'s module docstring ("the ONE separate
      implementation" — now correctly attributes that status only to
      lifecycle-header readers, and names `_template_gaps` as a remaining
      Python-side sibling), `corpus.py`'s sweep comment ("plus one UNBOUNDED
      sibling defect" — now points at the second sweep-gap note rather than
      implying `_scan_lines` was the only one), and `families._scan_lines`'s
      own docstring ("this WAS a live second Python line rule" — past tense
      corrected to scope the claim to `_scan_lines` itself, not the corpus).
      `_template_gaps` recorded in §7 Deferred below with the disposition.

## 2c. Second focused re-verify (findings F5-F6, 2026-08-19)

The reviewer ran the sweep method `corpus.py`'s own comment prescribes —
`grep -rn "\.splitlines()"` over document-text scanners, not just the
`[:N]`-windowed idiom the ORIGINAL sweep pattern targeted — and found one
more true survivor plus a mis-pointing docstring. Zero baseline cost
pre-measured on all of it (0 of 1227).

- [x] 2c.1 (F5, IN SCOPE under the already-ruled wide scope) `doc_health
      .ideation_readiness._parse_header` converts to
      `doc_health.lines.split_keepends`. Reads `Status:`/`Topics:`/`Target
      capabilities:` for `derive_clusters`, which is on a LIVE path
      (`ideation_readiness_dispatch`, `readiness_dispatch.py`) reading the
      SAME document `corpus.parse_status` reads. Demonstrated: an exotic
      separator can embed a `Status:`-shaped substring mid-line inside a
      DIFFERENT field's value (e.g. `Target capabilities: foo<FF>Status:
      staged`) — the old pseudo-line scan split that into two lines and
      extracted a false `Status: staged` field (clustering the document as
      'staged'), while `corpus.parse_status`, reading real lines, correctly
      finds no `Status:` header at all on the same document.
- [x] 2c.2 `_parse_header`'s TWIN, `scripts/bootstrap-ideation-cross-
      reference.py`'s `parse_header` (the two docstrings each declare
      "identical to" the other), converts too: verified (not assumed) that
      this standalone script CAN import `doc_health.lines` — both live
      directly under `scripts/`, so Python's own `sys.path[0]` insertion
      (the invoked script's containing directory) makes it reachable with
      no extra path manipulation. A new agreement test
      (`test_parse_header_agrees_with_the_bootstraps_own_parse_header`)
      pins the two to match, including on the F5 exotic fixture, rather
      than trusting the docstrings' claim.
- [x] 2c.3 THE SWEEP ITSELF re-run and recorded, so F5 is the last survivor
      found by this method, not the next one to be found by a future
      review. Verified the reviewer's pre-classification of the remaining
      `\.splitlines()` hits over document/config text, all genuinely out of
      scope (none reads the SIX lifecycle header fields; none is a
      `Status:`/`Kind:`/etc. reader):
        - `report.py:36` — a PRIOR doc-health REPORT's own machine-generated
          ranked-plan line syntax, not a governed document.
        - `ideation_routing.py:191`, `nightly_lane.py:150,320` — `.gitmodules`
          INI parsing and subprocess stdout/stderr, neither a governed
          document.
        - `neutrality_dispatch.py:465` — the domain-neutralization register's
          own `### DTN-XXX:` section-heading convention, not the lifecycle
          header block.
        - `families.py` (record-immutability blob diff; register-lifecycle-
          consistency's `| DTN-XXX | ... |` table rows) — whole-document line-
          SET comparison and a table-row format, neither a header read.
        - Every `validate-*.py` per-repo validator's own `splitlines()[0]`/
          subprocess-output reads (spot-checked
          `validate-capability-steward.py`) — each is that validator's OWN
          contract (YAML fixture first-line conventions, subprocess output),
          not the doc-health/document-lifecycle header contract; per-repo
          validators are already documented as divergent
          (root `CLAUDE.md` working rule 5).
      DISPOSITION, `families._staged_exit_changes` (BORDERLINE — reads
      governed-document text, shares the naive `splitlines()` idiom, but is
      it a lifecycle-header reader?): RULED OUT OF SCOPE. It reads
      `Proposed by:`/`Proposal:`/`Exit:`/`Exits via:` lines and an `## Exit`
      BODY SECTION — none of the six `GOVERNANCE_HEADER_FIELDS`/
      `REQUIRED_HEADER_FIELDS` the wide ruling's every-*header*-reader clause
      names, and not read from a bounded header window at all (it scans the
      WHOLE document for exit-criteria citations, a different governed
      vocabulary serving a different check — "has this staged fragment
      already been promoted"). Sharing the naive-`splitlines()` PATTERN is
      not the same as being a reader of THAT header; not converted.
- [x] 2c.4 (F6, recorded, not converted) `doc_health.ideation_routing
      ._scan_lines` is an unconverted byte-for-byte copy of
      `families._scan_lines` as it existed BEFORE this change, and its
      docstring pointed at "families `_scan_lines` precedent" as if
      following that pointer would land on matching (now-converted)
      behavior — it would not. Docstring corrected so the pointer doesn't
      mislead; added to §7 beside `_template_gaps` with the same disposition
      shape: not a lifecycle-header reader (scans for markdown provenance
      references and fence state), latent (0 of 1227 files diverge), found
      by the corrected sweep.
- [x] 2c.5 Four prose spots corrected that had gone stale or undercounted
      again: `proposal.md`'s `code_surface:` "EVERY reader ... scans real
      lines through it" (false until 2c.1 landed; true after — verified,
      and `_parse_header`/the bootstrap twin added to the enumeration);
      `doc_health/lines.py`'s module docstring (both the lifecycle-header
      reader list and the "TWO Python rules ... plus one JS rule" count for
      the narrower heading/fence-boundary question, corrected to THREE
      Python rules — this module's shared one, `_template_gaps`,
      `ideation_routing._scan_lines` — and TWO JS rules — `outlineSections`'s
      LF-only split at outline-model.js:46 vs. `endsInsideFence`/
      `insertSection`'s real-line regex at :273/:319, per finding F1);
      `families.py`'s `_scan_lines` docstring (same undercount, same fix).

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
      reason to stop and explain, not to accept the diff. RE-RUN AGAIN after
      2b: `completeness.py`/`generator.py`/`authoring.py` are not on the
      doc-health report's own path (they feed the ideation-dashboard
      generator, not the doc-health suite), but the gate is re-run anyway
      rather than assumed unaffected. RE-RUN AGAIN after 2c: unlike 2b's
      three, `ideation_readiness.py` (`_parse_header`, feeding
      `derive_clusters`) IS on the doc-health report's own path (the
      `ideation-readiness` finding family) — this run carries real
      information, not a belt-and-braces re-check.

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
- [ ] 7.2 `doc_health.families._template_gaps` (families.py, two unbounded
      `text.splitlines()` loops over document text) — DEFERRED, with the
      reviewer's ruling recorded (focused re-verify, 2026-08-19): it is NOT a
      lifecycle-header reader — it scans `## `/`### Q` TEMPLATE headings for
      conformance checking, never the `Status:`/`Kind:`/etc. header window —
      so it sits honestly OUTSIDE this change's every-*header*-reader clause,
      not inside it by omission. It is latent (0 of 1227 governed aggregation
      files diverge between its pseudo-line reading and a real-line one) and
      demonstrably divergent on a form-feed fragment when one is constructed.
      It shares the exact grep blind spot that hid F4
      (`completeness._Prepared.lines`): a bare unbounded `splitlines()` over
      document text, not the `splitlines()[:N]` windowed idiom the sweep's
      grep pattern targets. Left for its own change and its own baseline
      diff, same as 7.1 above — not a gate excuse, an honest scope boundary.
- [ ] 7.3 `doc_health.ideation_routing._scan_lines` (finding F6, second
      focused re-verify, 2026-08-19) — DEFERRED, same disposition shape as
      7.2: an unconverted byte-for-byte copy of `families._scan_lines` as it
      existed BEFORE this change (unbounded `text.splitlines()`, same naive
      fence toggle), used for markdown provenance-reference scanning and
      fence-state tracking — never a `Status:`/`Kind:`/etc. header read, so
      it too sits outside the every-*header*-reader clause. Latent (0 of
      1227 files diverge). Its docstring used to point at "families
      `_scan_lines` precedent," which a reader could take as "matches the
      converted behavior" — corrected to say plainly that it does not.
- [ ] 7.4 `doc_health.families._staged_exit_changes` (BORDERLINE, second
      focused re-verify, 2026-08-19; see §2c.3 for the fuller reasoning) —
      RULED OUT OF SCOPE, not deferred as unbuilt work: it reads `Proposed
      by:`/`Proposal:`/`Exit:`/`Exits via:` lines and an `## Exit` body
      section for `fam_location_conformance`'s "staged material already
      cites a proposal" check. None of those four fields is one of the six
      `GOVERNANCE_HEADER_FIELDS`/`REQUIRED_HEADER_FIELDS` the wide ruling's
      every-*header*-reader clause names, and the scan is unbounded over the
      WHOLE document rather than a header window — a genuinely different
      reading purpose (exit-criteria citation, not lifecycle-header
      declaration) that happens to share the naive `splitlines()` idiom.
      Recorded here rather than left silently unconverted, so the next
      sweep does not have to re-derive this judgment.
- [ ] 7.5 `scripts/proposal-support.py` (finding F7, third focused re-verify,
      2026-08-19) — three unshared lifecycle-`Status:` rules AS OF THIS
      BRANCH's base, demonstrated: a reader in `proposed_content` (:287,
      `re.search(r"^Status:...$", text, re.M)` — LF-only, raises a hard
      `SupportError` on a plain CR-only file), the writer beside it (:291,
      the same LF-only `re.sub`), and `_declares_staged_status` (:505,
      pseudo-line `str.splitlines()` plus its own fence toggle). RULED OUT
      OF SCOPE FOR CONVERSION, not deferred as unbuilt work: the promoted
      delta's requirement is titled "The deterministic pass reads a
      document's lifecycle header by real lines" and its purpose clause is
      about what THE PASS reports; `proposal-support.py` is a standalone
      mover that reports nothing to the deterministic pass, so it never was
      inside the requirement's own boundary — the earlier drafts' "EVERY
      reader" phrasing in `code_surface:` overclaimed past that boundary,
      now corrected there too. Distinguished from a broken twin on a second
      ground: `:287`'s divergence from `corpus.parse_status` is 251-of-1227
      files, its OWN PRE-EXISTING CONTRACT (single-token values, unbounded
      by any 15-line window) rather than a regression this change's line
      rule could cause — the LINE-rule divergence proper (what an exotic
      separator does to line boundaries) is the same 0-of-1227 latent shape
      as every other deferred item here.

      THE SIBLING BRANCH LARGELY REALIZES THIS ALREADY. Fetched and read
      `origin/change/refine-demote-round-trip-mechanics`'s version of
      `scripts/proposal-support.py` (its own rewrite of exactly these
      sites, not part of this change): it carries a fourth private
      real-line/fence primitive (`_split_keepends`/`_fenced_flags`,
      CR/LF/CRLF-only — the same "cannot import, so keep a local copy
      joined by an agreement test" shape `doc_health.lines`'s own docstring
      names for `web/views/outline-model.js`, applied here because this is
      a standalone script a human may run against a checkout without the
      dashboard package importable). The old LF-only `re.M` reader/writer
      pair is GONE, replaced by a fence-aware, row-based `_status_row` +
      `record_authorship` pair sharing that primitive; `_declares_staged_status`
      was moved onto the same primitive too. `tests/ideation-dashboard
      /test_round_trip.py` on that branch adds `proposal-support.py` as an
      explicit "FOURTH implementation" to the shared-fixture fence
      agreement test. ONE STALE SPOT SURVIVES even there:
      `_declares_staged_status`'s docstring still reads "`doc_health
      .families._scan_lines` already tracks fences for the same reason;
      this mirrors it rather than inventing a second convention" — true in
      spirit now that `families._scan_lines` is also real-line-based (this
      change's own 2a.2), but the claim was written for fence-tracking, not
      the real-line split, and it does not say which. FOLLOW-UP, not fixed
      here or on the sibling: reword that one docstring line after BOTH
      branches merge, whichever lands second — not on this branch, per an
      explicit constraint: editing `scripts/proposal-support.py` here would
      manufacture a merge conflict with work that already supersedes it.
