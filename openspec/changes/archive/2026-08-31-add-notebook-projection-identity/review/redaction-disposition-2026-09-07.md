# Redaction Disposition: add-notebook-projection-identity, archived record set

Status: record
Kind: decision record
Decision date: 2026-09-07
Ruler: Brett Heap (repository owner) — in-session, interactive multi-choice walkthrough
Ruled: 2026-09-08T03:36Z by Brett Heap — Q3[A] of the redaction-outside-ideation
decision sheet (`redaction-outside-ideation-decision-2026-09-07`, a lane session
artifact held outside this tree): a DATED immutability-exception disposition plus
in-place redaction of the convener's addresses to role placeholders
Applies to: the seven files of this archived change listed in § 2
Lane: provenance-autonomous-merge

## 1. The exception, in one paragraph

`docs/document-lifecycle.md` treats an archived OpenSpec change and a
`record`-status document as immutable evidence: editing one is a contradiction
unless it is dispositioned. openxFactory is going PUBLIC (Brett Heap's ruling of
2026-09-07, "openXfactory should be public"), and seven files of this archived
change carry the convener's real personal and organizational email addresses in
cleartext. This record is the disposition: the addresses are replaced by the
role placeholders PR #771 (`757d029a`) already used inside `ideation/`, and
nothing else in the packet moves.

## 2. What was redacted

The four addresses, everywhere they appear in this change's tree. They are named
here by ROLE, not spelled out: repeating them in this record would put back at
HEAD exactly what the act removes.

| address | placeholder |
| --- | --- |
| the convener's managed Workspace identity | `<convener-workspace-identity>` |
| the convener's personal consumer mailbox, dotted spelling | `<convener-personal-mailbox>` |
| the same mailbox, undotted spelling | `<convener-personal-mailbox>` |
| the operating party's declared hosting account | `<service-account-identity>` |

Both Gmail spellings map to ONE placeholder because they are one mailbox — the
dotted/undotted pair Gmail treats as the same account. Where a sentence's point
was the dotted/undotted retry itself (`tasks.md` § 4.7), the sentence names "the
same mailbox undotted" rather than repeating the placeholder, so the measurement
it records stays legible.

| file | address lines | occurrences |
| --- | --- | --- |
| `.openspec.yaml` | 4 | 4 |
| `proposal.md` | 6 | 6 |
| `design.md` | 3 | 3 |
| `tasks.md` | 20 | 22 |
| `specs/lifecycle-notebook-projection/spec.md` | 1 | 1 |
| `review/ratification-2026-08-23.md` | 2 | 2 |
| `review/retirement-gate-clearance-2026-08-26.md` | 4 | 5 |
| **total** | **40** | **43** |

Each of the seven carries ONE added header line, right after its front-matter or
`Status:` header block, naming this record and the pre-redaction commit — a `#`
comment in `.openspec.yaml`, a one-line blockquote in the six Markdown files.

## 3. This is the ONLY content change

No requirement, scenario, task tick, count, date, ruling, verdict or evidence
claim moved. The ratification of 2026-08-23
(`review/ratification-2026-08-23.md`) and the retirement-gate clearance of
2026-08-26 (`review/retirement-gate-clearance-2026-08-26.md`) stand exactly as
ruled, including § 4.7's re-scope to 7 of 7 and § 5.1's standing disposition.
The change remains archived at this path and the README OpenSpec Records block
is unchanged.

## 4. Where the original bytes are

At `543d47a96970d48b1c988e2293927c800bb1ff08` — openxFactory `origin/main` at the
moment the redaction branch was cut — and in every commit before it.

The history is NOT rewritten, by ruling: Q0[A] of the same sheet accepts the
historical exposure, because every consumer pins openxFactory by commit and
digest (MedxSoft, LedgerxFactory, codexFactory, the aggregation) and a
`filter-repo` rewrite or fresh-history republish would invalidate every one of
those pins the same way the already-refused fork would. Redaction at HEAD
removes the addresses from browse, search and clone-at-HEAD only.

## 5. One deliberate, temporary divergence from canon

`specs/lifecycle-notebook-projection/spec.md`'s ratified bullet now reads
"naming `<service-account-identity>`" while the PROMOTED
`openspec/specs/lifecycle-notebook-projection/spec.md` still names the real
account. That is Q2[A] on the same sheet — a SEPARATE governed change, authored
in parallel, that moves the promoted scenario, the committed hosting example and
the test fixtures — and this PR deliberately touches none of those five files.
The `promotion-fidelity` family compares requirement and scenario TITLES, not
body bullets, so the divergence raises no finding; it closes when Q2's change
lands.

## 6. doc-health

Measured per family against the same tree before and after, `--single-repo`: no
new finding is attributable to any file of this change. `record-immutability`
reads the governed corpus (`contracts/`, `docs/`, `examples/`, `ideation/`,
`templates/`) and not `openspec/changes/`, so this packet's `record` document is
outside its scope; the one `record` document redacted in the same PR that IS in
scope, `docs/notebook-projection-migration-evidence-2026-08-24.md`, was already
one of the four `record-immutability` findings standing on `main` before this
change, so its finding persists rather than arrives.
