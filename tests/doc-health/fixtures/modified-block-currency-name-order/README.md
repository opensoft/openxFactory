# Fixture: the declaration orders the pair AGAINST change-id name order

**SYNTHESIZED** — this text is invented and reproduces no historical instance.

## Which rule this exists for

`add-modified-block-currency-check` § 3.10's last clause, audit row **A15** —
re-verdicted from `satisfied` to `partial` at the plan review of 2026-08-27.

> Where two active changes carry a MODIFIED block for ONE promoted requirement,
> ORDER IS BY DECLARATION AND NEVER BY DATE. … **No folder name, commit
> timestamp, or `created:` date SHALL be consulted.**
> — `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`

## DO NOT "TIDY" THE CHANGE IDS

`add-zz-first` is the **declarer** and therefore the **later** writer, and it
sorts **LAST** alphabetically. `add-aa-second` declares nothing, is the
**earlier** writer, and sorts **FIRST**. **The disagreement between the names
and the declaration is the entire point of this fixture.** Renaming either id
into agreement destroys the discrimination and leaves the test passing while
testing nothing.

## Why not a reconstruction

This corpus has never carried two active changes that both MODIFY one
requirement with a declaration between them — measured at 0 pairs at the packet's
branch point and 1 with its own § 2.1 block present, and that one pair's names
happen to agree with its declaration.

F1's `test_no_date_folder_or_created_field_decides_the_ordering` cannot
discharge the clause and says so in its own docstring: "`add-oc-earlier` sorts
BEFORE `add-oc-later` by name and by any date a fixture could carry, **and the
declaration points the same way**". It falls back to a structural grep over the
module source, whose forbidden patterns cover `_archive_date(`,
`first_commit_timestamp(`, `.created`, `strftime(`, `datetime.` and the date
imports — but **nothing forbids ordering by folder or change-id name**, which
the delta prohibits in the same breath as dates. A build that sorted the
ratified group by `b.change` passes every F1 test.

## What the family reports here

One `info`, on **`add-zz-first`'s** path — the declarer's. The basis
substitution is visible in the finding itself: the spec it names is
`openspec/changes/add-aa-second/specs/name-order/spec.md`, the SIBLING'S DELTA,
not the promoted spec, and what it reports is the sibling's addition that the
declaring block does not carry.

`add-aa-second`'s own block is measured against canon and is quiet. The ordering
arm emits nothing, because exactly one declaration between two ratified writers
IS the ordered case.

**Under name-ascending ordering the roles invert and the finding lands on the
other path.**

Tests: `test_the_declaration_orders_the_pair_against_name_order`,
`test_the_name_order_fixture_would_invert_under_name_ordering`.
