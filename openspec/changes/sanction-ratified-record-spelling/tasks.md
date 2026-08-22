# Tasks: sanction-ratified-record-spelling

Nothing below §1 may start before §1 completes. This change proposes a rule
the ratifier's own instruction already operates under; the ratification is
what makes it a rule rather than an observation.

## 1. Ratification (Brett)

- [x] 1.1 Brett reads the proposal and rules OQ-1 through OQ-5. RULED
      2026-08-22, in-session, multiple-choice round: every recommended
      option adopted (OQ-3 unopposed in prose) — OQ-1 KEEP the `doc-health`
      delta; OQ-2 sanction BOTH spellings; OQ-3 floor stays at ONE of
      approver/date/resolvable-record; OQ-4 EXACTLY ONE citation line per
      document; OQ-5 a floor violation is CRITICAL, same tier as a dangling
      `Ratified by:` reference.
- [x] 1.2 Brett ratifies or declines. On ratification, flip `Status: draft` →
      `Status: ratified` in `proposal.md` front matter and add the citation
      line in the spelling this change itself sanctions: `Ratified by:` if an
      approving OpenSpec change is named, otherwise `Ratified:` naming
      approver, date, or record. The change is its own first conformance test.
      Ratified 2026-08-22; `proposal.md` front matter now carries
      `Status: ratified` and a `Ratified:` line (no approving OpenSpec change
      exists for this proposal, so it cites itself in the record-citing
      spelling it sanctions — approver, date, and a resolvable record all
      named, exceeding its own one-of-three floor).
- [x] 1.3 If OQ-1 is ruled "defer", delete `specs/doc-health/spec.md` from
      this change and record the deferral here, naming the follow-up.
      Re-validate `--all --strict` after the deletion. NOT TAKEN — OQ-1 was
      ruled KEEP, not defer; `specs/doc-health/spec.md` stays in this change.
- [x] 1.4 Record each ruling inline under its Open Question in `proposal.md`
      (the RULED-line convention `add-doxchat-model-intake` uses), so a later
      reader finds the decision beside the question rather than only in a
      commit message. Done: each of the five Open Questions in `proposal.md`
      carries its own RULED line in place (alternatives' text kept, not
      deleted), and design.md's D1 and D3 (where OQ-3 and OQ-1 are discussed)
      each carry a matching RULED note pointing back to proposal.md.

## 2. Realize the prose (`docs/document-lifecycle.md`)

- [ ] 2.1 Replace the single § Status Claim Rules bullet ("A `ratified`
      header names the approving OpenSpec change (`Ratified by: <change>`)")
      with the two-spelling rule and the three-way floor, worded to match the
      ratified requirement text rather than paraphrasing it.
- [ ] 2.2 State the condition of use explicitly in the prose — primary where
      an approving change exists, record-citing only where none does — since
      the prose is what authors actually read at authoring time.
- [ ] 2.3 State that the floor applies to `Ratified:` only, and that a
      `Ratified by:` line naming its change and nothing else is complete.
- [ ] 2.4 Do NOT edit any other document. No existing citation line in the
      corpus is rewritten by this change; verify with
      `git diff --stat` that `docs/document-lifecycle.md` is the only
      governed document touched.

## 3. Realize the check (`fam_ratified_provenance`)

- [ ] 3.1 Widen the read to TWO prefixes, `Ratified by:` and `Ratified:`.
      Per design D2, do NOT collapse them into `_header_line(doc, "Ratified")`
      — that matches body prose and would pass every test written against
      today's corpus while breaking on the first document whose header window
      opens with such a line.
- [ ] 3.2 Leave the `Ratified by:` path byte-for-byte behaviourally
      unchanged: change-id intersection, then `_link_targets` resolution,
      then the cross-repo `openxFactory` escape hatch.
- [ ] 3.3 Implement the floor for the `Ratified:` path: pass when the line
      names an approver, a date, or a resolvable record path; fail when it
      names none. Reuse `_resolves`/`_link_targets` for the record axis
      rather than adding a second resolution rule.
- [ ] 3.4 Emit a distinct finding message for the floor failure — the
      existing "Ratified by: missing or does not resolve to an OpenSpec
      change" is false when the document carries a `Ratified:` line. Severity
      per the OQ-5 ruling.
- [ ] 3.5 Report a `ratified` document carrying NEITHER prefix under a
      message that names both spellings, not just the primary.
- [ ] 3.6 Tests in `tests/doc-health/`, each pinning one boundary:
      (a) `Ratified by:` naming a change id — pass, unchanged;
      (b) `Ratified by:` naming a change id and nothing else — pass, the
      floor does not reach it (this is the 13-document regression guard);
      (c) `Ratified by:` dangling — CRITICAL, unchanged;
      (d) `Ratified:` with approver only, date only, and record only — three
      passing cases;
      (e) `Ratified:` with none of the three — finding;
      (f) `Status: ratified` with no citation line at all — finding;
      (g) a document whose header window opens with `Ratified together with…`
      or a `Ratified: <prose>` section label — NOT read as a citation;
      (h) a citation past `STATUS_SCAN_LINES` — not found, window unchanged.
- [ ] 3.7 Mutation-validate the new assertions: revert each behavioural change
      one at a time and confirm the matching test fails. Per the
      platform-inert-mutation lesson, a mutation that survives because the
      assertion only checks a value that happens to coincide does not count —
      pin the structure, not the coincidence.
- [ ] 3.8 Measure, do not assume: run doc-health before and after over the
      same tree and record that the severity counts are identical. A moved
      count means the widening reached a document it should not have.

## 4. Gates, record, archive

- [ ] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate sanction-ratified-record-spelling --strict`
      and `--all --strict`, exit codes read directly, not through a pipe.
- [ ] 4.2 `python3 -m pytest tests/doc-health` and
      `python3 -m pytest tests/ideation-dashboard -k workbench`, both green,
      exit codes read directly (`pipefail` discipline: never `| tail`).
- [ ] 4.3 README "OpenSpec Records" row updated from the Active block to the
      realization state as the change lands, and to the archived form at
      archive.
- [ ] 4.4 Archive only on merge-plus-green on the openxFactory main line, per
      `target_release: implemented`. No contract bundle is cut and no release
      tag is owed; the archive-gate evidence is the merged PR plus the green
      runs, named in this file before the archive commit.
- [ ] 4.5 On archive, confirm the promoted `document-lifecycle` requirement
      carries all seven scenarios (three restated, four added) and that the
      promoted `doc-health` requirement's other seven scenarios are
      byte-identical to their pre-change text — the MODIFIED-delta
      scenario-drop failure mode, checked rather than trusted.

## 5. Explicitly out of scope

- [ ] 5.1 `openspec/` joining `GOVERNED_ROOTS` — the event that makes the 15
      latent lines live. Separate decision, much larger blast radius.
- [ ] 5.2 `2026-08-22-add-doxbench-editing-phase-b`'s missing citation and
      `2026-08-22-add-roster-device-admission-surface`'s out-of-window one.
      Both are archived-record edits, which the register routes through a
      citing change and a ruling per record.
- [ ] 5.3 Rewriting any existing citation line to a preferred shape.
