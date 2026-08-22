# Design: sanction-ratified-record-spelling

Status: draft (authored 2026-08-22)

Records the decisions this change makes that are not obvious from the
requirement text: why the floor is three-way and disjunctive, why the family's
widened read is a two-prefix read rather than a prefix match on the bare word,
and why the rule is promoted rather than only corrected in prose.

## D1 — The floor is disjunctive, and it is a floor

**Decision.** A `Ratified:` citation must name at least ONE of: an approver, a
date, or a resolvable record path. Not all three. Not a fixed field set.

**Why not a fixed shape.** The obvious alternative is a grammar —
`Ratified: <date> by <approver> — record: <path>` — and it is wrong for this
corpus, because the honest citations already written do not share a shape.
Measured across the 15 live `Ratified:` lines in `openspec/changes/`:

| shape | count | example |
| --- | --- | --- |
| date + approver + verbatim instruction | 9 | `Ratified: 2026-08-10 by Brett Heap — in-session, verbatim: "ratified"` |
| date + approver + record pointer | 3 | `Ratified: 2026-08-21 by Brett Heap — record: the 2026-08-22 in-session ruling round captured in docs/archive-record-discrepancies.md` |
| date + record pointer, no `by <approver>` clause (the approver appears inside the record parenthetical) | 2 | ``Ratified: 2026-08-19 — record: `review/ratification-2026-08-19.md` (Brett; …)`` |
| date + record pointer, NO approver anywhere on the line | 1 | ``Ratified: 2026-07-23 — record: the archive commit `e8c2970`, titled "Ratify and archive add-governed-derived-model"`` |

Each of those is the most a real record supported. The approver-less form
exists because `docs/archive-record-discrepancies.md` C2 ruled, on
`add-governed-derived-model`, that "no prose anywhere names a ratifier" and
that git authorship "is git metadata, not a recorded attribution, and is
deliberately NOT cited as one". A grammar demanding an approver would have
forced exactly the invention that ruling refused. A floor accepts the honest
line and rejects only the empty one.

**Why three and not two.** Approver, date and record are the three axes the
register's own analysis uses to decide whether a citation is real — B1 asks
which of them `.openspec.yaml` supplies, C2 asks which of them each of the
seven headerless proposals supplies ("where the record names an approver
and/or a date"), and C7 turns on Brett supplying a date the archive did not
have. Any one of them makes the claim checkable by a reader: a name to ask, a
day to look at, or a file to open. None of them, and the line is decoration.

**What the floor is NOT.** It is not applied to `Ratified by:`. That form's
named change IS a resolvable record, and 13 of the 29 governed documents
carrying it name the change and nothing else. Applying the floor across both
spellings would convert those 13 from correct to CRITICAL in one commit, on a
rule change nobody asked for. The scoping is written into the requirement text
rather than left to the implementation, because it is the single most likely
way for the realization to go wrong.

**RULED (2026-08-22, Brett, in-session multiple choice): recommendation adopted, unopposed in prose — the floor stays at ONE of the three (OQ-3); a stricter floor would force invented dates. See proposal.md for the full ruling.**

## D2 — The widened read is two prefixes, never one shorter prefix

**Decision.** `fam_ratified_provenance` reads `Ratified by:` and `Ratified:`
as two distinct prefixes. It MUST NOT be simplified to
`_header_line(doc, "Ratified")`.

**Why this is a trap and not a style note.** `_header_line` matches with
`body.startswith(prefix)` over the first 15 real lines
(`corpus.STATUS_SCAN_LINES`, via `doc_health.lines.split_keepends` — the real-line
rule `align-status-reader-to-real-lines` established for every reader of the
lifecycle header). A prefix of `"Ratified"` matches any line beginning with the
word, and the corpus has such lines:
`docs/domain-ontology-semantic-decisions.md:201` opens a section with
`Ratified: YAML-serialized JSON-Schema contracts under…` as a decision label,
and `openspec/changes/archive/2026-08-08-add-openxwallet/proposal.md:123` opens
a sentence with `Ratified together with the two decisions already carried into
the…`. Both sit well below line 15 today, so the short prefix would not
mis-fire on THEM — which is exactly what makes it dangerous: it would pass
every test written against today's corpus and break on the first document that
opens with such a line inside its header window.

Two prefixes also keep the two rules separable, which the requirement demands:
the change-id resolution path runs for `Ratified by:` and the floor runs for
`Ratified:`. A single merged read would have to re-derive which spelling it
found before choosing a rule, and that re-derivation is the thing the two-prefix
read makes unnecessary.

**Consequence for the header-window boundary.** The requirement states that a
ratification citation is read in the lifecycle header and that body prose
beginning with the same word is not one. That is not new behavior — it is the
existing 15-line window, stated so the realization cannot quietly widen it
while "fixing" the read.

## D3 — Why the rule is promoted rather than only corrected in prose

The ratification-citation rule is, today, prose in
`docs/document-lifecycle.md` with no promoted requirement behind it: the
promoted `Controlled document status taxonomy` requirement carries scenarios
for the `standard` claim, the `record` artifact and the `superseded` pointer —
three of § Status Claim Rules' four bullets — and none for the ratified
citation. `doc-health`'s promoted spec nevertheless names "a dangling
`Ratified by:` reference" as a lifecycle violation, and
`fam_ratified_provenance` enforces it at CRITICAL. So a CRITICAL check is
enforcing a rule that exists only as unpromoted prose.

Correcting the prose alone would leave that standing. The delta promotes the
rule in the same act that widens it, which is also what makes the doc-health
enumeration change (OQ-1) coherent: the check family can then cite a promoted
requirement for both spellings instead of one prose bullet for one of them.

**RULED (2026-08-22, Brett, in-session multiple choice): recommendation adopted — KEEP the `doc-health` delta in this change (OQ-1); see proposal.md for the full ruling.**
