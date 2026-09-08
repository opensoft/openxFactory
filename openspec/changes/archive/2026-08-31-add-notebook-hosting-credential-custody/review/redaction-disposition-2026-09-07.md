# Redaction Disposition: add-notebook-hosting-credential-custody, archived record set

Status: record
Kind: decision record
Decision date: 2026-09-07
Ruler: Brett Heap (repository owner) — in-session, interactive multi-choice walkthrough
Ruled: 2026-09-08T03:36Z by Brett Heap — Q3[A] of the redaction-outside-ideation
decision sheet (`redaction-outside-ideation-decision-2026-09-07`, a lane session
artifact held outside this tree): a DATED immutability-exception disposition plus
in-place redaction of the convener's addresses to role placeholders
Applies to: `.openspec.yaml` and `proposal.md` of this archived change
Lane: provenance-autonomous-merge

## 1. The exception, in one paragraph

`docs/document-lifecycle.md` treats an archived OpenSpec change as immutable
evidence: editing one is a contradiction unless it is dispositioned. openxFactory
is going PUBLIC (Brett Heap's ruling of 2026-09-07, "openXfactory should be
public"), and two files of this archived change name Opensoft's hosting account
in cleartext. This record is the disposition: that address is replaced by the
role placeholder PR #771 (`757d029a`) already used inside `ideation/`, and
nothing else in the packet moves.

## 2. What was redacted

| address | placeholder | file | address lines |
| --- | --- | --- | --- |
| `xFactor001@opensoft.one` | `<service-account-identity>` | `.openspec.yaml` | 1 |
| `xFactor001@opensoft.one` | `<service-account-identity>` | `proposal.md` | 1 |

Two lines, two occurrences. Neither of this change's personal-identity siblings
appears here; the sister disposition
`openspec/changes/archive/2026-08-31-add-notebook-projection-identity/review/redaction-disposition-2026-09-07.md`
covers the other seven files redacted in the same act, and carries the full
placeholder table and the history ruling.

Each of the two files carries ONE added header line, right after its
front-matter or `Status:` header block, naming this record and the pre-redaction
commit — a `#` comment in `.openspec.yaml`, a one-line blockquote in
`proposal.md`.

## 3. This is the ONLY content change

No requirement, scenario, task tick, count, date or ruling moved. The
ratification of 2026-08-23 (`review/ratification-2026-08-23.md`) stands exactly
as ruled, including the accepted residency redirect. The change remains archived
at this path.

## 4. Where the original bytes are

At `543d47a96970d48b1c988e2293927c800bb1ff08` — openxFactory `origin/main` at the
moment the redaction branch was cut — and in every commit before it. The history
is NOT rewritten, by ruling (Q0[A]): every consumer pins openxFactory by commit
and digest, so a rewrite would invalidate every pin. Redaction at HEAD removes
the address from browse, search and clone-at-HEAD only.

## 5. doc-health

Measured per family against the same tree before and after, `--single-repo`: no
new finding is attributable to either file.
