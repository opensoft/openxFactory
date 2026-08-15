# Amendment record: add-client-identity-roster — the packaged multi-surface case (Decision C)

Status: record
Date: 2026-08-15
Ruled by: **Brett Heap, 2026-08-15 — Decision C: RELOCATE TO FIXTURE.**
Escalated to Brett by the architect seat after the A-16 escalation ruling's own
verification obligation fired and established that the authority was Brett's,
not the architect's (`specs/007-client-identity-roster/a16-escalation-ruling-2026-08-15.md`,
"Jurisdiction correction and outcome").
Sibling to: `amendment-record-2026-08-14.md`, `amendment-record-2026-08-15.md`
and `decision-review-2026-08-14.md` (all `Status: record`) — written as a NEW
record rather than appended to any of them, per the record-immutability rule.
The living task list `tasks.md` is edited IN PLACE; this record is the sibling
that documents why.

## What was amended

`tasks.md` task 2.3's packaged case list. It read four cases — (i) the Business
Central two-admission-act worked case, **(ii) a provider-forced multi-surface
reader**, (iii) a duty-separated pair, (iv) one `planned` entry. It now reads
THREE, and case (ii) is relocated to a synthetic representability fixture in
the test corpus.

Nothing else in the packet changes. No capability is declared or undeclared, no
ratified position moves, no scope is added or reduced, and no requirement in
any of the five deltas is touched.

## Why: the provider fact does not exist, and was verified not to exist

Ruling A-16 (plan gate, 2026-08-14) had already mechanized this as a
PRECONDITION rather than a discovery — the multi-surface reader's provider fact
was to be verified BEFORE the packaged-examples cluster began, so that an
escalation would be cheap rather than arrive after a corpus had been built
around an assumption. That precondition was executed as task 0.1 of the Speckit
task list on 2026-08-15, offline (FR-029 forbids a live provider call), across
the pinned feature checkout and the entire aggregation checkout including the
OpsxFactory evidence chain and its archived changes. It was run twice,
independently, reaching the same verdict.

The fact required was a conjunction, and **both clauses fail**:

1. **No spanning permission is citable.** No provider-native permission, app
   role, or Entra directory role reaching BOTH the `business_central` and the
   `exchange` read surfaces is named anywhere in the estate. `Global Reader`,
   `Dynamics 365 Administrator`, `Business Central Administrator`,
   `Exchange Administrator` and `View-Only Organization Management` return zero
   hits. Seven candidates were examined and each failed on the record; the
   candidate table is preserved in the implementing session's escalation record
   and restated in the A-16 ruling.
2. **The "no narrower path exists" clause is affirmatively FALSIFIED, not
   merely uncited** — and it fails in opposite directions on the two surfaces:
   - **Exchange DOES offer a surface-scoped read-only path.** Graph application
     `Mail.Read`, bounded to exactly one mailbox by a provider-enforced
     application access policy, ratified at OpsxFactory
     `openspec/specs/exchange-administration/spec.md:46-56` and live-verified
     with an attempted-overreach proof at
     `openspec/changes/archive/2026-07-24-add-exchange-execution-surface/exchange-bringup-rung2-4-evidence.md:234-480`.
   - **Business Central offers NO read-only path at all.** OpsxFactory
     `openspec/specs/business-central-administration/spec.md:93-101`:
     "Business Central offers no read-only administration role: its service
     principal exposes exactly `Automation.ReadWrite.All`, `app_access`,
     `API.ReadWrite.All` and `AdminCenter.ReadWrite.All`."

A provider-forced multi-surface READER therefore has no truthful instance
inside the first-release vocabulary that ratified answer 5 closes to
`business_central` and `exchange`. The one real multi-surface identity class in
the estate, `microsoft_managed_node_inventory_reader`, spans Entra, Intune and
Windows 365 — every one of them a surface answer 5 excludes — so it cannot be
transcribed either.

## Why relocation rather than a synthesized packaged example

A packaged governed example is an INSTANTIATION TEMPLATE and a truthful worked
case: a domain copies it. Writing one whose `declared_excess.provider_reason`
asserts that no narrower permission exists — when the estate's own ratified
records say the opposite for one surface and say nothing at all for the other —
would put a fabricated provider fact into the contract family this change
exists to make falsifiable. That is the failure mode the whole feature is built
against: FR-004 and FR-009 are record-internal precisely so no check ever
infers a provider fact, and research.md Decision 8 already carried the standing
rule that "a packaged example may not assert a provider fact the builder cannot
cite."

The alternatives Brett was offered, and declined:

- **Keep it packaged, marked hypothetical.** Declined: a packaged example
  marked "hypothetical" is still copied, and the marker is the first thing a
  domain deletes. It also inverts the family's own posture — declare the fact,
  never infer it.
- **Widen the first-release vocabulary** so a real spanning identity becomes
  representable. Declined: that is a real scope change against ratified answer
  5, and the vocabulary's extension route is a surface arriving with the
  promotion of the capability that governs it.

## What relocated, and where

The provider-forced multi-surface reader becomes a **synthetic representability
fixture** in the test corpus, carrying an explicit dated header stating: that
it is SYNTHETIC; that as of 2026-08-15 no in-vocabulary provider-forced
multi-surface permission exists, with both citations from the section above;
that it exists to prove killed-flaw (a) REPRESENTABILITY — an entry declaring
spanned surfaces with its forced breadth declared validates with ZERO findings
— and to stand ready for vocabulary growth.

The killed-flaw acceptance obligation is unimpaired. It requires that a
declared provider-forced multi-surface reader PASS CLEAN; it never required
that fixture to be a packaged example. The obligation is now measured where the
other killed-flaw regression positives are measured.

## What did NOT change — stated so a later reader cannot mistake the scope

- **Every forced-breadth mechanism stays**: `declared_excess` with its
  `spanned_surfaces[]`, `provider_reason`, `bound_mechanism`, `gate_obligation`
  and `enforcement_test_ref`; the permission-side and act-side reach rules; the
  per-surface `per_unit_principal_available` mapping and its coverage rule.
- **Every named negative stays**, including `undeclared-reach.yaml` and
  `undeclared-act-surface.yaml`, whose discrimination partner is now the
  relocated fixture rather than a packaged file.
- **The ratified conditional requirement is untouched.** The roster delta's
  "Provider-forced breadth is declared, never silently absorbed" and its
  scenario "A single provider permission spans surfaces" ("**WHEN** the
  narrowest available permission reaches more than one admission surface")
  mandate behaviour IF such a permission exists and assert that none does. The
  contract must carry the capability even while no in-vocabulary instance
  exists — which is exactly what the relocated fixture proves.
- **The two-member `admission_surface` vocabulary is untouched** (ratified
  answer 5), as are the uniqueness key, the authority-class closure, and both
  killed-flaw guarantees.
- Modified Capabilities remain four: `consent-instrument`, `doc-health`,
  `domain-conformance-checks`, `credential-contracts`. Archive blockers are
  unchanged.

## Jurisdiction, recorded

The A-16 ruling carried its own item-5 verification obligation: sweep the
ratified packet for any text mandating a PACKAGED multi-surface example, and
STOP if one is found, because the ruling would then need Brett rather than the
architect. **The obligation fired.** Packet `tasks.md` task 2.3 — ratified
verbatim 2026-08-14 and named "the authority for SCOPE" by the Speckit
specification, whose sibling tasks 2.1 and 2.2 the artifacts already cite as
binding ratified text — opens on "Packaged" and enumerated the multi-surface
reader inside its case list. Relocating it REDUCES a ratified line, which the
pre-existing supersession of the sketch did not cover: that supersession is
scoped explicitly to PACKAGING CONVENTION (a single file becoming a per-family
directory) and preserved every case.

The stop was taken before any encoding, the question was put to Brett as
Decision C with three options, and this record documents the answer. Strict
validation was re-run over the amended packet and over the whole OpenSpec
corpus before this amendment was committed.
