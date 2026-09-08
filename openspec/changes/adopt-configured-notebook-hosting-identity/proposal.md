---
Status: draft
Proposed: 2026-09-08
Lane: provenance-autonomous-merge
code_surface: >-
  openxFactory — NOT `none`, and the surface is measured at main `543d47a9`
  rather than described. FIVE FILES CARRY THE FORTY LINES Q2 CLASSIFIES, and
  they are three different kinds of surface:
  (1) `openspec/specs/lifecycle-notebook-projection/spec.md` (1 line, the third
  bullet of the promoted scenario *An operating party declares the company
  account*) — reachable only through the `## MODIFIED Requirements` delta in
  `specs/lifecycle-notebook-projection/spec.md`;
  (2) `examples/notebook-projection-hosting.yaml` (18 lines: `hosting.account`,
  `hosting.migration.from_account`, seven `share_out[].hosting_account`, seven
  `share_out[].user`, one `denied[].hosting_account`, and two prose comment
  lines) — this file IS the live declaration today, so the change does not
  redact it, it SPLITS it: a synthetic instance stays here and the live record
  moves to a configured, private home;
  (3) `tests/notebooklm/test_nlm_auth.py` (2: the `STORED` / `LEGACY`
  module constants), `tests/notebooklm/test_sync_notebooklm_books.py` (11: the
  `HOSTING_DECLARED` / `HOSTING_PENDING` fixture texts and the assertions over
  them) and `tests/notebooklm/test_validate_hosting.py` (8: the `BASE` and
  `ENTRY` fixture texts and the assertions over them) — 21 fixture literals.
  AND TWO RUNTIME ARTIFACTS CHANGE BEHAVIOUR, which is why this surface is not
  `none`: `scripts/sync-notebooklm-books.py` (`HOSTING_REL`,
  `read_hosting_declaration()`, `_refuse_unusable_declaration()`,
  `enforce_hosting_profile()`) and
  `scripts/validate-notebook-projection-hosting.py` (`DEFAULT_REL` and
  `main()`'s path resolution) gain a CONFIGURED-PATH RESOLVER and a refusal for
  a configured path that resolves to the shipped example. Plus
  `docs/lifecycle-notebook-projection.md` § *The declaration* and § *The
  approval lane* (structural, not redaction — the Q1 docs pull request owns the
  three address lines there) and `README.md`'s doc index if the doc's section
  titles move.
  NOT THIS CHANGE'S SURFACE, each for a stated reason: `scripts/nlm_auth.py`
  (its two lines are DOCSTRINGS and belong to Q1's docs pull request; the
  script reads the real username from the vault and hard-codes nothing);
  the eight prose files of Q1 and the nine archived records of Q3 (separate
  arms of the same ruling, landing in ONE docs pull request under Rule 6); the
  history (Q0[A] accepted exposure at HEAD-redaction only); and the LIVE
  RECORD'S NEW HOME, which is an OPERATOR act in a private repository and is
  recorded here rather than performed — see `tasks.md` Group 5.
target_release: implemented
  # openxFactory's own main line. NO CONTRACT BUNDLE IS OWED, and that is
  # measured rather than assumed: none of the five files, and neither of the
  # two scripts, appears in `contracts/releases/contract-v3.4.digests.yaml`
  # (283 entries, checked by exact path), none is registered in
  # `contracts/manifest.yaml`, and the record's own header states why it is
  # deliberately NOT a `contracts/` member — "no other repository, install or
  # domain consumes it, and nothing pins it". So no digest set moves, no
  # `contract_bundle_version` is spent, no release tag is owed, and
  # `release-inventory-drift` predicts ZERO new findings. The archive gate is
  # `release-realization`'s merged-plus-green realization evidence for a
  # non-empty code surface: the pytest suite green with the new fixture
  # literals, and the validator green against BOTH the synthetic example and
  # the relocated live record.
sequenced_after: [add-notebook-projection-identity]
Origin: >-
  Convener ruling on a decision sheet. Brett Heap, 2026-09-08T03:36Z, Q2 option
  [A] on `~/session-prompts/redaction-outside-ideation-decision-2026-09-07.md`
  ("Rulings: Q0[A] Q1[A] Q2[A] Q3[A] — Brett, via the interactive multi-choice
  walkthrough"). The forcing fact behind the sheet is Brett's 2026-09-07 ruling
  that openxFactory becomes public, whose governed half is
  `adopt-codexfactory-repository-identity` (ratified 2026-09-07, on main at
  `eb30db7a`). THE RULING AUTHORIZED THIS PACKET AND DID NOT RATIFY ITS
  CONTENT; it explicitly left the live record's home to the realization, which
  is why OQ-A exists rather than a decision. The machine-readable declaration
  is `.openspec.yaml` `origin` (`kind: ad_hoc`, id
  `openxFactory:adhoc:2026-09-08-adopt-configured-notebook-hosting-identity`),
  and this header is its prose restatement, not a second claim.
---

# Proposal: adopt-configured-notebook-hosting-identity

**THIS PACKET IS A PROPOSAL AND ITS LANDING RATIFIES NOTHING.** It carries
`Status: draft`, cites no ratification, and owes none until its content is
ratified as a separate act of Brett Heap's (`tasks.md` 0.2). Nothing below is
performed by the merge.

## Why

**A repository that is about to become public carries one real service-account
address inside a PROMOTED capability spec, and eighteen more inside a file that
is not an example at all — it is the live record.** Every other line the
redaction sheet found outside `ideation/` is prose, and prose redacts in a docs
pull request. These forty do not, for three separate reasons.

**1. A promoted requirement can only be changed by a delta.** The third bullet
of `lifecycle-notebook-projection`'s scenario *An operating party declares the
company account* reads, today, that "Opensoft's own install is such a
declaration" and then names the live Workspace service-account address itself —
quoted here in role terms on purpose, a proposal that reprinted the value to
argue for removing it having removed nothing. That is canon. Editing canon
directly is the
one edit OpenSpec exists to prevent, and `promotion_fidelity` would report the
divergence between canon and the archived delta that ratified it. So the
address in the promoted spec is reachable ONLY through a `## MODIFIED
Requirements` block — which is a governed change, which is this packet.

**2. `examples/notebook-projection-hosting.yaml` is misnamed: it is Opensoft's
live hosting declaration, and its identities are load-bearing values.** The
sync reads it (`HOSTING_REL`, `read_hosting_declaration()`) and
`enforce_hosting_profile()` compares `hosting.account` — or
`hosting.migration.from_account` while a migration is pending — against the
address the `nlm` CLI profile is ACTUALLY signed in as, refusing the run when
they differ:

```text
hosting: profile 'company' is signed in as <address>, but this install expects
<declared>. Refusing: the profile name matches and the ACCOUNT does not, which
is exactly the mix-up a declared identity exists to catch.
```

**Replacing that address with a role placeholder does not redact the record; it
disarms the guard.** The same is true of the roster: seven `share_out` rows and
one `denied` row are the RECORD OF EIGHT GOVERNED ACTS that the promoted
requirement *Access to the projection is shared out from the hosting account,
and each share act is recorded* obliges the install to keep. A placeholder
there does not anonymise a record — it falsifies one. The only honest move is
the one Q2 names: **two files instead of one.** A synthetic instance stays in
the public tree as the shape's example and the validator's default fixture; the
live record — declaration, roster and denial together — MOVES, intact, to a
private home, and is resolved from configuration.

**3. Twenty-one test literals mirror the live values, and they can go synthetic
with nothing lost — which is a measured claim, not a hope.** No test in
`tests/notebooklm/` reads the committed record in order to learn an address.
`test_sync_notebooklm_books.py` writes its own declaration text into a
temporary workspace (`_declare_hosting()`); `test_validate_hosting.py` writes
its own into a temporary directory (`_validate()`). The literals are fixture
text, and a fixture proves the same thing about a synthetic address as about a
real one. **Exactly ONE test is different and it is the one that matters**:
`test_the_committed_record_conforms` runs the validator over
`validator.DEFAULT_REL` and asserts "this install's own declaration must pass".
That test is the only automatic conformance check the LIVE declaration has
today, and it works only because the live record and the committed file are the
same file. Splitting them **costs that check**, and this change is obliged to
replace it rather than lose it — which is why the delta's second added
paragraph makes validation of the resolved path a requirement, and why
`tasks.md` carries it as work rather than as a note.

**And the flip is one-way.** A public repository's history is published whole
(Q0[A]: history exposure accepted, HEAD redaction only), so the value of this
change is not that the address becomes unknowable — it is that the address
stops being a FUNCTIONAL VALUE that a public clone must carry in order to work.
After it, the public tree contains a shape; the identity lives where the
credential that opens it already lives.

## What Changes

- **MODIFY the promoted requirement** *The projection's hosting identity is
  declared at install* in `lifecycle-notebook-projection`: the identity bullet
  states the role, not the address; two body paragraphs are ADDED (the
  declaration's location resolves from configuration and any committed instance
  is synthetic; a resolved live declaration stays subject to every rule and to
  the same validator); two scenarios are ADDED (*The committed example carries
  no real identity*, *The live declaration resolves from configuration*). Every
  other promoted unit of that requirement is carried verbatim, and no other
  requirement of the capability is touched.
- **Add a configured-path resolver** to `scripts/sync-notebooklm-books.py` and
  `scripts/validate-notebook-projection-hosting.py`: an environment variable,
  then a workspace-local configuration file, then UNDECLARED. The committed
  example stops being a declaration source and becomes a fixture, and a
  configured path that resolves to it is a REFUSAL rather than a binding.
- **Make `examples/notebook-projection-hosting.yaml` a synthetic instance** —
  every identity-bearing value fictional, `example.invalid` per this
  repository's existing synthetic-address convention, and the actor names role
  placeholders so the validator's `granted_by == approval.designated_actor`
  equality still holds.
- **Move Opensoft's live declaration, intact, to a private home** (OQ-A;
  recommended: `installs/hermes-install` `config/clients/opensoft/`) — an
  OPERATOR act, recorded here and performed by Brett.
- **Switch twenty-one test-fixture literals to synthetic values**, and add the
  tests the resolver owes: env-var resolution, config-file resolution, absent
  configuration is UNDECLARED, and a configured path resolving to the shipped
  example refuses.
- **Update `docs/lifecycle-notebook-projection.md`** § *The declaration* and
  § *The approval lane* to describe the two-file model — a STRUCTURAL update,
  sequenced after the Q1 docs pull request that redacts that document's three
  address lines.

## What this deliberately does not change

- **`scripts/nlm_auth.py`.** Its two occurrences are docstrings and belong to
  Q1's docs pull request. The script never hard-codes the address: it reads the
  username from the vault, and `merge_profile_metadata()` compares
  case-insensitively against what the CLI stored. No functional value of it
  lives in this repository, so there is nothing here for a governed change to
  do.
- **The eight Q1 prose files and the nine Q3 archived records.** Same ruling,
  different arms, ONE docs pull request under Rule 6. This packet neither
  redacts nor blesses them; § Ordering states the only dependency between them.
- **The four archived changes' own text.** `add-notebook-projection-identity`
  and `add-notebook-hosting-credential-custody` are immutable evidence. Q3[A]
  disposes of their addresses with a dated immutability exception; this change
  touches no archived byte and needs none — see OQ-B, where the reason no
  cross-reference note is owed is measured rather than asserted.
- **The custody block.** It names a BINDING (`binding_kind`, `binding_client`,
  `binding_id`) and never a secret or an address. It moves with the live record
  and is otherwise unchanged.
- **The other real-looking addresses in `examples/` and `contracts/`** —
  `brett@opensoft.one`, `Brett.Heap@opensoft.one`,
  `ledgerx-test-intake@opensoft.one` and two siblings. They are outside the
  sheet's four-address set, they are not part of Q2, and this packet does not
  quietly widen its own scope to reach them. If they are wanted, that is a
  further ruling.
- **The git history.** Q0[A]. The bytes stay reachable at every commit that
  held them, and the flip's runbook records the residual.

## Capabilities

### Modified Capabilities

- `lifecycle-notebook-projection`: ONE `## MODIFIED Requirements` block over
  *The projection's hosting identity is declared at install* — one bullet
  reworded, two body paragraphs and two scenarios added, every other promoted
  unit carried.

## Impact

- **Affected specs:** `lifecycle-notebook-projection` (MODIFIED, one
  requirement). No other capability is touched, restated or widened;
  `credential-contracts` and `document-lifecycle` are CITED.
- **Affected contracts:** NONE. The record is deliberately not a `contracts/`
  member and nothing pins it.
- **Affected runtime artifacts:** `scripts/sync-notebooklm-books.py`,
  `scripts/validate-notebook-projection-hosting.py`.
- **Affected examples:** `examples/notebook-projection-hosting.yaml` (becomes
  synthetic). `examples/lifecycle-notebook-workspaces.yaml` is NOT touched —
  its two lines are comments and belong to Q1.
- **Affected tests:** `tests/notebooklm/test_nlm_auth.py`,
  `test_sync_notebooklm_books.py`, `test_validate_hosting.py` — 21 literals,
  plus four new resolver tests and one re-aimed test
  (`test_the_committed_record_conforms` keeps its assertion and changes its
  subject to the synthetic instance; the live record's conformance becomes the
  resolver's own test plus an operator check).
- **Affected docs:** `docs/lifecycle-notebook-projection.md` (two sections,
  structural), `README.md` (this Records entry; the doc index only if a section
  title moves).
- **Predicted check movement, stated so a reviewer can falsify it:**
  `openspec validate --all --strict` moves from 100 passed / 1 failed to 101
  passed / 1 failed, the one pre-existing failure being
  `disposition-codexfactory-declared-renames`, a deltaless disposition packet
  unrelated to this change and not repaired by it.
  `release-inventory-drift` ZERO (no inventoried blob moves).
  `promotion-fidelity` ZERO: it compares requirement and scenario TITLES only,
  the block keeps all five promoted titles, and its latest-writer rule makes
  this delta the authoritative writer once archived.
  `modified-block-currency` scenario-title arm ZERO; **carriage ledger ONE
  `info` finding**, for the one bullet the block deliberately does not carry.
  That finding is UNAVOIDABLE and is the reason it is declared in the delta's
  own header instead of suppressed: `document-lifecycle`'s reserved
  `Removed from canon by` marker names the retired unit as a code span
  carrying its EXACT TEXT, which here would reprint the address this change
  exists to remove, inside the delta that removes it. `info` carries no gate.
  The `pytest-suite` SKIPPED pin does not move (no test is added skipped) and
  the SELECTED/PASSED floors only rise (four new tests).
- **Sweep ledger:** ONE row added and no partner row moved, seeded at PR #783
  and measured rather than predicted:
  `adopt-configured-notebook-hosting-identity: {state: active, class:
  co-modifier, declares: [add-notebook-projection-identity], depth: 1}`. The
  archived `add-notebook-projection-identity` writes the same requirement title
  and is ALREADY `co-modifier`, so it does not flip; `depth: 1` is the one hop
  to that declared parent (an earlier draft of this line said `depth: 0`, which
  the tool corrected — a chain of one hop is a chain, and `0` would read as a
  resolved root).

## Ordering

Three constraints, and only the first is hard:

1. **The Q1/Q3 docs pull request lands FIRST.** It redacts
   `docs/lifecycle-notebook-projection.md`'s three address lines; this change's
   realization then rewrites two of that document's sections structurally. Both
   touching the same file in the other order is a conflict for no gain. It also
   touches `openspec/changes/`, so it carries the Rule 6 LANDING/LANDED window
   — this packet's own pull request touches `openspec/changes/` too and takes
   the same window at ITS merge.
2. **Ratification precedes realization.** Nothing below Group 0 of `tasks.md`
   is performed by this packet's landing, per Brett's standing rule that
   OpenSpec ratifies and Speckit builds.
3. **The public flip waits for the live record's move.** Not for THIS packet —
   for the operator step it schedules (Group 5). Flipping visibility with the
   live declaration still in the tree publishes the address as a functional
   value, which is the whole finding.

## Open questions

Five, and the first two are the ones that need a word before realization
starts. Full statements, alternatives and consequences are in `design.md` § 6.

- **OQ-A — WHERE DOES THE LIVE DECLARATION LIVE?** The Q2 ruling named two
  candidates and left the choice to the realization ("hermes-install config or
  a private aggregation path — the realization decides, both are already
  private"), and a third is available (the vault, beside the username the
  harness already reads).
  **RECOMMENDED: `installs/hermes-install`, at
  `config/clients/opensoft/notebook-projection-hosting.yaml`.** Three measured
  reasons. (i) The record's own `custody:` block already points there —
  `binding_client: opensoft`, `binding_kind:
  xfactory_credential_binding_template` — and its header states the residency
  rule Brett accepted at ratification: "neutral obligations here, live binding
  instances in the installs". The declaration and the binding it references
  then live in one place instead of two. (ii) hermes-install already holds
  `config/clients/opensoft/runtime-manifest.yaml`, the committed
  stack-identity manifest, so a per-client committed governance record is an
  established shape there rather than a new one. (iii) It stays RESOLVABLE from
  the same workspace the sync already walks:
  `installs/hermes-install/config/clients/opensoft/…` is one workspace-relative
  path, so the resolver needs no absolute path and no second checkout.
  AGAINST the aggregation root: the aggregation deliberately tracks only
  `README.md`, `.gitmodules`, `.gitignore` and two dated review documents, and
  a config directory there breaks a rule its own `CLAUDE.md` states. AGAINST
  the vault: the record is a GOVERNANCE ARTIFACT, not a secret — it needs
  diff review, a commit history and a validator run, none of which a vault
  item has, and `credential-contracts` puts material in the vault precisely so
  that non-material can stay reviewable.
- **OQ-B — DOES THE ARCHIVED `add-notebook-projection-identity` DELTA NEED A
  CROSS-REFERENCE NOTE?** **RECOMMENDED: NO, and the reason is measured rather
  than stylistic.** `promotion_fidelity` compares an archived delta to canon by
  requirement and scenario TITLES only — never by body or bullet text (see
  `parse_promoted()` and the missing-scenario branch) — so the archived delta's
  one address bullet is invisible to it, before and after this change. Its
  "latest writer wins" rule then makes THIS delta the authoritative writer of
  that requirement the moment it archives, and the archived one stops being
  compared at all. A note would therefore document nothing a check reads and
  would add a byte to an immutable packet that Q3[A] is already dispositioning
  for its own reason. If Brett wants the pointer anyway, the lawful home is
  Q3's `review/redaction-disposition-2026-09-07.md` in that archived change —
  a file Q3 is creating regardless — and NOT an edit to the delta.
- **OQ-C — Does the committed instance keep its PATH?** Recommended: **yes,
  keep `examples/notebook-projection-hosting.yaml`**, and mark it synthetic
  INSIDE the record (`hosting.instance: example`) rather than renaming it to
  `notebook-projection-hosting.example.yaml`. A rename touches six documents
  and two scripts for a signal a field carries better, and the marker is what
  the resolver's refusal branch reads. The `.example.yaml` convention is real
  and the alternative is recorded, not foreclosed.
- **OQ-D — Do the ACTOR NAMES in the synthetic instance go to role
  placeholders too?** Recommended: **yes.** "Brett Heap" is not sensitive —
  it is on hundreds of public governance lines — but in a SYNTHETIC instance a
  real person's name asserts a grant that instance did not make. The validator
  ties `share_out[].granted_by` to `approval.designated_actor` by equality, so
  both move together or neither does.
- **OQ-E — Does the ROSTER RECORD move, or does it stop existing in the
  governed tree?** Recommended: **it MOVES, intact.** Seven grants and one
  recorded denial from 2026-08-27 are the discharge of a ratified obligation;
  they are evidence, not configuration. The private declaration carries them
  verbatim, and the public tree keeps only a pointer that says a roster exists
  and where. Deleting them to synthesise a clean example would redact a record
  of governed acts, which is the one thing `document-lifecycle` forbids
  outright.

## Authoring decisions, flagged for veto

D-1..D-6 are in `design.md` § 5: the resolver's precedence order (env, then
workspace config, then UNDECLARED); refusing rather than binding when
configuration resolves to the example; `example.invalid` as the synthetic
domain; keeping the record's shape byte-for-byte identical between the
synthetic and live copies; replacing the lost CI conformance check with a
resolver test plus an operator step; and declaring `sequenced_after:
[add-notebook-projection-identity]` rather than nothing.

**RATIFICATION HAS NOT HAPPENED AND IS NOT SOUGHT BY THIS PACKET'S LANDING.**
Brett authorized the DRAFT through the Q2[A] ruling. Every judgment this
session took is listed above or in `design.md` rather than presented as
settled.
