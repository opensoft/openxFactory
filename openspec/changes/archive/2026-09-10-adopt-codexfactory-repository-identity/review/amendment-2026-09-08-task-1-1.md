# Task Amendment: adopt-codexfactory-repository-identity task 1.1

Status: record

Decision date: 2026-09-08

Amender: Brett Heap (convener) — in session, interactive walkthrough, lane
`provenance-autonomous-merge`.

Verbatim ruling:

> **Amend task 1.1: this change creates the file (Recommended)**

Realized by: openxFactory pull request opened from branch
`030-mapping-row-amendment`, Speckit feature
`specs/030-realize-codexfactory-identity/` task **T069**.

Ratified head this amends: `5bfdcf3c06478167bd7509f1576db3528ce4ede1`
(ratification 2026-09-07, verbatim *"accept all [A] and ratify 763"*, record
`review/ratification-2026-09-07.md`). Merged as PR **#763**, `eb30db7a`.
Realization slice A merged as PR **#799**, merge commit `131adf11`,
2026-09-08T14:32:34Z.

---

## 1. What was blocked

Task 1.1 as ratified forbade this change from creating the mapping file, on the
premise that the exemplar would author it first. **The premise did not hold in
time.** Measured at openxFactory `main` `e8021fed` on 2026-09-08:

```sh
git ls-tree origin/main -- contracts/policies/repository-identity.yaml   # empty
```

`adopt-medxsoft-repository-identity` is still active, still `Status: draft`, and
**unrealized** — no Speckit feature under `specs/` realizes it. Task **0.2**'s
conditional fires only if the exemplar is *"archived or withdrawn"*; it is
neither, so 0.2's premise held, 1.1's instruction stood, and **group 1 could not
be realized at all**. The blocker was recorded on codexFactory tracking issue
[#279](https://github.com/opensoft/codexFactory/issues/279) with the two
available exits, and the convener took the second.

## 2. The original wording, quoted

From `tasks.md` § 1, as ratified 2026-09-07:

> - [ ] 1.1 Add the codexFactory row to
>       `contracts/policies/repository-identity.yaml` — the file
>       `adopt-medxsoft-repository-identity` authors at ITS task 1.1. **Do not
>       create the file here.** The row: `former: opensoft/codexFactory`,
>       `current: codeXfactory/codexFactory`, `transferred_on: <the transfer
>       date>`, and a `redirect` note stating that the provider redirect lapses if
>       `opensoft` reuses the name — which it may, `opensoft` remaining an active
>       organization that holds the aggregation repository.

And task 1.4, which the amendment necessarily re-derives:

> - [ ] 1.4 Confirm no second registration is owed: the file's
>       `contracts/manifest.yaml` entry and its `consumption_rule` are created by
>       the exemplar's task 1.3. Adding a row does not add an entry. Re-verify the
>       per-file `sha256` moves with the row and is recomputed, not hand-edited.

## 3. The amended wording

Task 1.1's **row content is unchanged**. What changes is the authorship clause
and, consequentially, `transferred_on`:

> - [ ] 1.1 **AMENDED 2026-09-08.** **CREATE**
>       `contracts/policies/repository-identity.yaml` — this change authors the
>       file, with the schema both repositories' rows need and its own row.
>       `adopt-medxsoft-repository-identity` APPENDS its two 2026-08-26 rows to
>       `transfers:` when it realizes. The row: `former: opensoft/codexFactory`,
>       `current: codeXfactory/codexFactory`, `transferred_on: null` with
>       `transfer_state: pending` until the transfer is CONFIRMED at runbook step
>       1.2, and a `redirect` note stating that the provider redirect lapses if
>       `opensoft` reuses the name.

Task 1.4 is re-derived from "confirm no registration is owed" to "**the
registration IS owed here**": the `contracts/manifest.yaml` entry, its
`consumption_rule` and the recomputed per-file `sha256` are authored by this
change, because the file it registers is now authored by this change. The
`sha256` is **computed, never hand-edited**, which the original wording already
required and which survives verbatim.

Tasks **1.2** and **1.3** are untouched in wording and are realized as written:
their content is per-row and does not depend on who created the file.

## 4. What the amendment does NOT change

- **No requirement moves.** The four ADDED requirements on `repository-identity`
  in `specs/repository-identity/spec.md` are untouched. This is an amendment to
  an implementation task, not to a ratified delta, so **no re-ratification of the
  spec is owed**.
- **`sequenced_after: [adopt-medxsoft-repository-identity]` is NOT edited**, and
  that is deliberate. See § 5.
- **The row's content is unchanged** from the fragment prepared and reviewed in
  PR #799 (`specs/030-realize-codexfactory-identity/contracts/repository-identity-row.md`),
  except `transferred_on`, which becomes explicit rather than a placeholder.
- **`proposal.md` and `design.md` are not edited.** `proposal.md` § "The
  precedent this follows, cited" states *"This packet does NOT re-author that
  policy file"*; that sentence is now superseded by this record and is left
  standing as the ratified text, which is how this corpus treats a ratified
  statement that a later dated act overtakes.

## 5. The consequence for `sequenced_after`, recorded and NOT acted on

The declared dependency's **justification inverts**. `design.md` § 4 called it
*"load-bearing twice over"* partly because the exemplar authored the file this
change adds a row to. After this amendment, **this change authors the file and
the exemplar appends to it** — so the file-creation half of the dependency now
points the other way.

**The declaration is nonetheless left exactly as ratified**, for two reasons:

1. `scripts/validate-sequenced-after.py --archive-gate` is a **parent-declaration
   retention (freeze) gate**: it compares the ratified-side declaration against
   the current one and reports a declaration MUTATION as exit 1. Editing
   `sequenced_after` here would break that gate — the freeze exists precisely so
   a realization cannot quietly re-point a ratified dependency.
2. The other half of the dependency is undisturbed: both changes touch the same
   `transfers:` list and the same `contracts/manifest.yaml` region, so an
   ordering relation between them is still real.

**Re-deriving the declaration is therefore a separate governed question** — the
one task 0.2 anticipated when it said `sequenced_after` is *"re-derived rather
than kept out of habit"*. It is named here so the next lane finds it rather than
discovering it at the archive gate.

## 6. The consequence for the exemplar's lane, recorded

`adopt-medxsoft-repository-identity`'s remaining group-1 work is **reduced, not
redirected**, and nothing of it is done twice:

| exemplar task | before | after this amendment |
| --- | --- | --- |
| 1.1 (author the file + two rows) | authors the file and both 2026-08-26 rows | **APPENDS its two rows** to the existing `transfers:` list |
| 1.2 (record the owner-segment-only rule) | authors the rule | **already present** as the file-level `owner_segment_rule`, written to its wording so it re-authors nothing |
| 1.3 (register in `contracts/manifest.yaml` with `consumption_rule`) | authors the entry | **already present**; its rows change the file's bytes, so it **recomputes the per-file `sha256`** |

**This record does not edit that packet.** Editing another lane's unmerged
change is a lane collision (`proposal.md` § What this deliberately does not
change: *"other lanes' in-flight change packets — 74 across 32 … Editing another
lane's unmerged `proposal.md`, `design.md`, `tasks.md` or ratification record is
a lane-collision"*). The consequence is recorded here and on issue #279 so the
owning lane reads it before its next touch.

## 7. Why the row is SAFE NOW even though the transfer has not happened

The realization's central ordering fact is that the transfer is an OPERATOR
ceremony and is **unperformed**: `gh api repos/codeXfactory/codexFactory` returns
**HTTP 404**, and `gh api repos/opensoft/codexFactory` returns
`{"full_name":"opensoft/codexFactory","private":true,"visibility":"private"}`.
Four rename slices are held in draft for exactly that reason
(#801, #802, #805, #806).

**The mapping row is not one of them**, and the file makes that rigorous rather
than asserting it:

- `transferred_on: null` with `transfer_state: pending` — the field records a
  completed act, and a date written before the act would be a falsehood in the
  one file whose purpose is that a frozen spelling stays trustworthy.
- **`pending_row_rule`**, a file-level clause: *a row whose `transfer_state` is
  `pending` DECLARES a ruled identity change that HAS NOT HAPPENED … A reader
  MUST NOT resolve `former` -> `current` for any LIVE reference while the row is
  `pending`.*

So the row publishes the ruled canonical identity and the OQ-6 spellings without
instructing anything to resolve the new address. **Nothing reads this file at CI
time**, and the clause means nothing may act on the row until the ceremony sets
the date. That is what makes group 1 landable ahead of Phase 1 while groups 3-5
are not.
