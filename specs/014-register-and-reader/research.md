# Research: The Register and Its Reader (S4)

**Feature**: 014-register-and-reader | **Grounded**: 2026-08-25

## Governing texts (verified verbatim this session)

1. **Ratified requirement "The register and the reader are ratified together"**
   (specs delta :47-66): one change or the capability is not realized; MVP
   shape normative (one file/fixed path/one holder/one target/one act/tier
   act/one expires_at); reader's only obligation = fail admission of a holder
   with no active row.
2. **Requirement "A grant with no reader in a required check confers nothing"**
   (:30-45): enforcement statements must NAME the check; blesses
   `scripts/validate-openxwallet.py` as the named home.
3. **Design D11** (:259-268): NO register contract schema - "the register's
   shape is a declared successor rather than a contract authored now… softened
   from 'no schema' to 'no new GRANT schema', because a register with a
   reader IS a shape." Rule-of-three: one named consumer.
4. **D4/D5/D6**: register+reader one change; file-based first with revocation
   surface honestly deferred (Q1c); permanently human-only, floor entry BY
   NAME.
5. **N7/N8**: same-tree residency (satisfied - register joins
   governance/review-authority/); reader computes expiry from expires_at and
   treats stale `state` as a finding.
6. **Task 5.5**: Q1c constraint recorded IN the register's own documentation ✓
   (header of register.yaml).
7. **Day-one order + operator rulings 2026-08-25**: grant+register together;
   target opensoft/openxFactory; expires ~90 days.

## Substrate facts verified in code

8. `Context` indexes scanned records into `ctx.wallets`/`ctx.grants` keyed by
   id BEFORE validation; register checks consume the index (repo_scan wiring).
9. Packaged examples are excluded from repo_scan; kindless YAML is skipped -
   which is why the negative coverage for register rules lives as SYNTHESIZED
   TREES in the self-test (S2 anchor-block precedent), not as corpus fixtures.
10. `REVIEW_ACT_TOKEN`/`ROOT_ISSUER_OPERATOR_TOKEN` constants exist from S2;
    the new grant is the FIRST positive exercise of both rules (OXWR-R1/R2).
11. Approval-posture keys are validated dynamically against the Hermes
    job-envelope vocabulary; the three keys used are the packaged example's.
12. Docstring rule letters ran (t) after S2; the register rules land as (u).

## Rulings consumed (Brett Heap, 2026-08-25, in-session)

- First grant minted within S4 (root, anchored issuer).
- Single target repository: opensoft/openxFactory.
- expires_at: ~90-day term → 2026-11-23T12:00:00Z.

## Base-drift note

origin/main advanced +5 commits after branch point dda06ba3 (#340 merge,
contract-v1.42 retro-tags, promotion-fidelity sync). Zero overlap with files
touched here (verified: diff stat on scripts/validate-openxwallet.py and
wallet_yaml_syntax_gate between dda06ba3..origin/main is empty).
