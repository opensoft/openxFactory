# Addendum: the `identity_namespace` the sweep does not cover

Status: record

Recorded: 2026-09-08

Recorder: lane `provenance-autonomous-merge`, adversarial-review fix round on
the four gated realization slices (runbook step 10.2).

Raised by: the Opus adversarial review of pull request
[#801](https://github.com/opensoft/openxFactory/pull/801),
[B-1 recommendation 3](https://github.com/opensoft/openxFactory/pull/801#issuecomment-5587040705)
— *"Respell `identity_namespace` at
`contracts/review-lane-repin-binding.template.yaml:103`, or record on the row
why one namespace still covers two organizations."*

**NEEDS BRETT'S WORD.** No file was changed for this finding. The contract line
stands as it is on `main` until the convener rules, because the field is a
governed contract member that the ratified packet does not name, and because
either answer is a claim about what is true rather than a spelling.

---

## 1. The gap, stated precisely

`tasks.md` § 3.5, as ratified 2026-09-07, enumerates its own file list line by
line. For this file it names **two** lines:

> `contracts/review-lane-repin-binding.template.yaml` (lines 46, 110)

Line **46** is the binding's header prose naming the decision core; line **110**
is `privileges.source_repository.repository`. Both are respelled by slice B1 and
both are unambiguously about the repository that MOVES.

Line **103** is a third occurrence of the `opensoft` owner segment in the same
file, in a different member:

```yaml
    consumer:
      holder_ref: "openxfactory:workflow:review-lane-repin"
      fetch_identity: "github-actions:openxfactory:review-lane-repin"
      identity_namespace: "github:opensoft"
```

It is **not** in task 3.5's list, and it is not in any other task's list — the
sweep's per-line verdicts for this file cover 46 and 110 only. It is also not a
`opensoft/codexFactory` literal, so `git grep -i 'opensoft/codexfactory'`
never sees it: the sweep's completeness arithmetic is unaffected by whatever is
decided here, in either direction. This is the same blindness class as
`docs/xfactory-domain-factory-model.md:868` (#805 M-1) and
`docs/dogfood-content-migration-plan.md:49` (#806 M-3) — prose or machine text
that becomes false BECAUSE an occurrence moved, carrying no moved literal of its
own.

## 2. What actually reads the field

`scripts/validate-credential-contracts.py`, and nothing else in the workspace.
Three facts about how it reads it, each checked rather than recalled:

1. **It is declared, optional and grammar-checked, not value-checked.**
   `CONSUMER_MEMBERS` at `:178` admits the member; `IDENTIFIER` at `:201` is
   `^[A-Za-z0-9][A-Za-z0-9._:/-]*$`. **Both candidate values pass that
   grammar**, so this is not a grammar question and no refusal turns on it.
2. **Its only executable effect is on the `shared-authority-identity`
   comparison**, which is rescoped from a bare string to the PAIR
   `(identity_namespace, fetch_identity)` — and only WHERE BOTH bindings of a
   pair declare a grammatical namespace (`:373`, `:385`; canon at
   `openspec/specs/credential-contracts/spec.md:503-514`).
3. **There is no pair.** `git grep -n 'secret_ref:' -- contracts/` returns
   exactly two bindings in this repository, on two different secrets
   (`openxfactory-review-lane-repin-app` and
   `avatar-broker-openai-internal-live`). Nothing else declares
   `secret_ref: openxfactory-review-lane-repin-app`. The pair comparison
   therefore **cannot fire on this record today**, so the field's value has
   **no executable consequence** at either spelling. What it has is a recorded
   claim, and the whole question is whether that claim is true after the
   transfer.

## 3. The two readings

### Reading A — the namespace is the CONSUMER's issuing directory, and it does not move

Canon defines the member by what issued the **fetch identity**, not by what the
binding reads:

> `consumer.identity_namespace` names the ISSUING DIRECTORY, ACCOUNT OR TENANT
> WITHIN THE PROVIDER that minted the fetch identity.
> — `docs/credential-access-model.md:249-250`

> A FETCH IDENTITY IS A NAME, AND A NAME IS UNIQUE ONLY INSIDE THE DIRECTORY
> THAT ISSUED IT. The block SHALL therefore carry an ADDITIVE OPTIONAL
> `identity_namespace` naming the ISSUING DIRECTORY, ACCOUNT OR TENANT WITHIN
> THE PROVIDER that mints the fetch identity…
> — `openspec/specs/credential-contracts/spec.md:322-326`

The fetch identity on this row is `github-actions:openxfactory:review-lane-repin`,
and the file's own comment above it says what it is: *"THE IDENTITY IT
AUTHENTICATES TO THE STORE WITH."* The store is the GitHub Actions secret store
of `opensoft/openxFactory` — the repository that holds this workflow, this
binding and these secrets, and which **does not move in this change at all**.
`consumer.holder_ref` on the line above is likewise
`openxfactory:workflow:review-lane-repin`, an openxFactory workflow. Under
Reading A the row is already true and stays true: `github:opensoft` is the
directory that issued the name `github-actions:openxfactory:review-lane-repin`,
and it will still be that directory after the transfer.

Under Reading A the finding's premise — *"one namespace covering two
organizations"* — does not arise, because the field was never covering the
source repository's organization. The two organizations appear under
`privileges:`, where each entry names its repository in full and needs no
namespace.

### Reading B — the namespace is the estate the binding operates across, and it becomes misleading

The counter-reading takes the row as the record's single statement of WHICH
GitHub organization this credential lives and works in, sitting three lines
above a `privileges.source_repository.repository` that slice B1 moves to
`codeXfactory/codexFactory`, and — after the B-1 recommendation-2 fix landed in
`22125ea1` — above a mint in `.github/workflows/review-lane-repin.yml` that now
resolves its installation with `owner: codeXfactory`. A reader of the finished
record sees `github:opensoft` immediately above two members that say
`codeXfactory`, and the estate's own warning applies: a record whose plain
reading is false is worse than one that reports too much.

Reading B does not have a single obviously-correct replacement value, which is
part of why it needs a ruling rather than an edit:

- `github:codeXfactory` — grammatical, but false under canon's definition: the
  Actions secret this identity names is not issued by `codeXfactory`.
- `github:opensoft` **plus a comment** stating in as many words that the
  namespace is the CONSUMER's directory and that the source repository's
  organization is carried by `privileges.source_repository.repository` — a
  record change with no value change.
- a second `consumer:` member — not available: the block is closed at the next
  major and its members are enumerated by schema
  (`contracts/schemas/xfactory-credential-contracts.schema.yaml:236`). Adding
  one is a contract-family change, not a realization act.

## 4. Proposed ruling

> **Keep `identity_namespace: "github:opensoft"` unchanged, and add a comment
> above it — in slice B1, in the same commit as the two lines task 3.5 does
> name — stating that this member names the directory that issued the CONSUMER's
> fetch identity (`opensoft/openxFactory`'s Actions secret store, which does not
> move), and that the source repository's organization is carried by
> `privileges.source_repository.repository` below. Record the field as
> DELIBERATELY NOT RESPELLED, with that reason, in the sweep evidence file's
> per-line form.**

The reasoning, in one line each:

- **Canon settles the truth question in Reading A's favour.** The member is
  defined by what issued the fetch identity, and that is `opensoft`.
- **Reading B's real complaint is legibility, and a comment answers exactly
  that** — while a value change would answer it with a false value.
- **Nothing executable turns on it either way** (§ 2.3), so there is no CI
  outcome, no green and no red riding on this decision — which is precisely why
  it should be decided on truth rather than on convenience.
- **A comment is inside slice B1's blast radius already**; the file is in B1's
  diff, so no new file, no new slice and no re-measure of the sweep is needed.

**Neither the value nor the comment is in the diff today.** The proposal above
is a proposal; at slice B1's current head the file carries exactly the two
respellings task 3.5 names, and `:103` is byte-identical to `main`. The comment
is a one-paragraph edit to a file already in the diff and can be made at the
window in seconds once the word is given.

## 5. If the convener rules the other way

If the ruling is Reading B with a value change, the act is **one line** in slice
B1's existing diff (`contracts/review-lane-repin-binding.template.yaml:103` →
`identity_namespace: "github:codeXfactory"`), plus a per-line entry in the
evidence file recording that task 3.5's list was extended by convener ruling at
the fix round. No test asserts the value, `openspec validate` does not read it,
and `validate-credential-contracts.py` accepts either — so the change carries no
check risk. It should NOT be made silently, which is why this record exists.

## 6. Not decided here

- Whether a deterministic check family should verify that no live surface makes
  a containment claim falsified by a mapped former identity. That is task
  **9.6**'s open question and its dual; this field, `:868` of the domain-factory
  model and `:49` of the dogfood plan are its three concrete instances so far.
  Recorded on [#279](https://github.com/opensoft/codexFactory/issues/279) with
  the review summary.

---

## RULED 2026-09-09 — Brett Heap (convener): respell to `github:codeXfactory`

Decided in session, interactive walkthrough, lane `provenance-autonomous-merge`.

Both readings above were presented to the convener:

- **Reading A** — the namespace names the CONSUMER's issuing directory (the
  Actions secret store of `opensoft/openxFactory`, which does not move), so
  `github:opensoft` is already true and stays true; the finding's premise does
  not arise.
- **Reading B** — the namespace is read, in practice, as the estate the
  binding operates across, sitting three lines above two members that now say
  `codeXfactory`; a reader of the finished record sees `github:opensoft`
  immediately above them and the plain reading is misleading.

**The convener chose the source-repository reading (Reading B).** Verbatim
option chosen: *"Respell to github:codeXfactory."* The field is respelled to
`identity_namespace: "github:codeXfactory"` at
`contracts/review-lane-repin-binding.template.yaml:103`, in slice B1
(pull request [#801](https://github.com/opensoft/openxFactory/pull/801)), per
§ 5 above. Task 3.5 is amended to cover this line; see
`review/amendment-2026-09-09-task-3-5.md`. The per-line verdict is recorded in
the sweep evidence file's § 17.

**Status stays `record`.** This section records the ruling; it does not
reopen §§ 1-6 above, which stand as the analysis that produced the two
readings the convener chose between.
