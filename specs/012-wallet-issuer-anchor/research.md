# Research: Validator & Corpus Facts Behind the S2 Rulings

**Feature**: 012-wallet-issuer-anchor | **Date**: 2026-08-24

Researcher-consult facts (2026-08-23 session) plus direct code reads, recorded so
the rulings in clarify-questions.md are auditable against the tree they were made
on.

## R1 — `issued_by` is read by zero rules today

`scripts/validate-openxwallet.py` never references `issued_by`. The grant schema
declares it optional (`openxwallet-grant.schema.yaml:90`,
`{$ref: '#/$defs/identifier'}`). S2 is therefore the field's FIRST enforcement —
US1's "first real enforcement of the issuer anchor" claim is literal.

## R2 — Corpus exposure: five positives, all legacy-issued, none review-class

The packaged core corpus carries exactly five `xfactory_wallet_grant` positives
(`grant-posting-parent`, `grant-posting-derived`, `grant-revoked-parent`,
`grant-revoked-derivation`, `grant-creator-software-custody`). All name
`issued_by: opensoft` — the legacy org-level string. None contains the bare act
token `review` in `scope.acts` (grepped; only substrings inside unrelated words),
so class detection cannot re-classify an existing positive and US2's
non-grandfathering refusal cannot disturb the packaged set.

## R3 — Ratified text already fixes most mechanics

`openspec/changes/add-wallet-carried-review-authority/specs/review-authority-intake/spec.md`
requirement *"Every review-authority grant names its issuer, and a root grant's
issuer is anchored outside the register"* prescribes: `issued_by` SHALL be named;
no-`parent_grant_ref` defines ROOT; root issuer = responsible operator; anchor =
the Human Escalation Contract **cited in the register**, not a register row;
machine-named root issuers refused. Only representation questions needed the
architect round: the matchable class marker, the anchor constant's form, and the
specimen set.

## R4 — Negative-fixture mechanics (validator contract)

A negative fixture declares its intended failure in first-line comments:
`# expected_failure: <code>` (required), `# expected_failure_detail: <substring>`
(optional pin, checked against the fired finding lines), `# requirement: <REQ-ID>`
(required, must exist in REQUIREMENTS or the self-test refuses). Each negative
validates in an ISOLATED context, so specimens cannot collide with each other or
with positives. Coverage closure is bidirectional: every REQUIREMENTS row needs ≥1
negative; every fixture's claimed REQ-ID must exist.

## R5 — Where S1 left CI

S1 (`010-wallet-validator-ci`) wired this validator into a `wallet-validation`
pull_request check (drafts included, 10-minute fail-closed budget) with the
kind-aware YAML syntax gate beside it. The operator act marking it required is
post-merge and already documented — S2's new failures therefore become live gate
surface on merge without any workflow edit here.
