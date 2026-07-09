# Tasks: Add Doc-Health Contract

## 1. Contract Document

- [x] 1.1 Write `docs/doc-health.md` (`Status: ratified`, `Ratified by:`
      this change): the twelve check families, the report contract and
      ranked-plan item shape, severity levels and the regression rule,
      aging threshold defaults, and the ownership/hosting split —
      referencing `docs/document-lifecycle.md` for the `xspec:` marker
      grammar (never restating it).
- [x] 1.2 Link `docs/doc-health.md` from the README documentation index.

## 2. Ideation Pointers (staged -> proposed gate)

- [x] 2.1 Update `ideation/staging/doc-health-checks/nightly-run-shape.md`:
      reference this change as the first of its two declared exit changes;
      record the resolved open questions (aging thresholds, report format)
      pointing at this change's `design.md`.
- [x] 2.2 Update `ideation/staging/doc-health-checks/status-check-rules.md`:
      reference this change as the contract now carrying its checks.
- [x] 2.3 Update `ideation/staging/doc-health-checks/tag-hygiene-rules.md`:
      reference this change as the contract now carrying its checks (the
      grammar itself stays owned by `document-lifecycle`).

## 3. Implementation Handoff

- [x] 3.1 Write `ideation/staging/doc-health-checks/implementation-handoff.md`
      (staged fragment targeting the follow-on codexFactory change): what
      the implementation MUST include — checker scripts per family, report
      generator emitting the contract schema, reusable workflow in
      codexFactory plus the thin nightly caller and `health/reports/` home
      in the aggregation repo, issue automation for the regression rule,
      notebook dry-run integration (auth strategy open), and the archive-
      discipline decision that change must make as the release-flow pilot.

## 4. Validation

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate add-doc-health-contract
      --strict` and `openspec validate --all --strict` pass from the
      openxFactory root.
- [x] 4.2 Grep-verify the `xspec:` grammar is stated only by
      `docs/document-lifecycle.md` and the prose-tagging change artifacts —
      `docs/doc-health.md` references, never restates, it.
