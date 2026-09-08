# Design: adopt-configured-notebook-hosting-identity

## 0. Convener brief

Eight lines, for the read that decides whether to ratify.

1. openxFactory becomes public. Outside `ideation/`, **119 lines across 22
   files** carry one of four real addresses (measured at main `543d47a9`; the
   sheet counted 123 at `f2355208`). **Forty of them, across five files, are
   FUNCTIONAL VALUES rather than prose** — and that is the whole of Q2.
2. One of the forty is a bullet inside a **PROMOTED capability spec**, so it is
   reachable only through a delta. That alone makes this a governed change.
3. Eighteen of them are `examples/notebook-projection-hosting.yaml`, which is
   **not an example** — it is Opensoft's live hosting declaration, and its
   addresses are the values `enforce_hosting_profile()` compares against the
   account a `nlm` CLI profile is signed in as. **A placeholder there disarms a
   guard; it does not redact a record.**
4. Eight of its lines are worse than configuration: they are the **RECORD OF
   EIGHT GOVERNED ACTS** (seven share grants and one recorded denial, 2026-08-27)
   that a ratified requirement obliges the install to keep.
5. So the fix is **two files, not one edit**: a synthetic instance stays public
   as the shape's example and the validator's fixture; the live record moves
   intact to a private home and is **resolved from configuration**.
6. **The split costs a check, and the change is obliged to replace it.**
   `test_the_committed_record_conforms` is today the only automatic conformance
   check the live declaration has, and it works only because the live record and
   the committed file are the same file.
7. **Nothing is realized here.** No promoted byte moves, no literal changes, no
   resolver is written, no file is moved. Five open questions are named; OQ-A
   (where the live record lives) and OQ-B (whether the archived delta owes a
   note) need a word.
8. **No contract bundle is owed**, checked by exact path against
   `contract-v3.4.digests.yaml`'s 283 entries.

## 1. The current data flow, read from the code rather than described

### 1.1 Who reads the record, and how

Two readers, and they do not agree about the path root — which is itself part of
the finding.

| reader | path it uses | how it parses |
| --- | --- | --- |
| `scripts/sync-notebooklm-books.py` | `HOSTING_REL = "openxFactory/examples/notebook-projection-hosting.yaml"`, joined onto the WORKSPACE root the sync is given | a deliberately NARROW SCALAR READER (`read_hosting_declaration()`): the script carries no YAML dependency, so it reads only the `hosting:` block's two-space scalars plus its `migration:` sub-block |
| `scripts/validate-notebook-projection-hosting.py` | `DEFAULT_REL = "examples/notebook-projection-hosting.yaml"`, joined onto the REPO root, overridable by `argv[1]` | a full `yaml.safe_load`, and the authority on the whole record including the roster |

Nothing else consumes it: no contract registers it, no manifest pins it, no
other repository reads it. The record's own header says why —
"no other repository, install or domain consumes it, and nothing pins it" — and
that is exactly what makes a configured home cheap here and expensive elsewhere.

### 1.2 What the values DO, which is the reason they cannot be redacted in place

`enforce_hosting_profile(root)` (sync, l.2598) does five things in order:

1. `read_hosting_declaration(root)` — absent file is the ONE undeclared case;
   a present-but-unparsable file yields an empty dict, which
   `_refuse_unusable_declaration()` turns into a REFUSAL rather than the
   undeclared branch, on the stated reasoning that "an unreadable declaration
   is not an absent one".
2. picks the binding target: `nlm_profile` normally,
   `migration.from_nlm_profile` while `migration.state == "pending"`, because
   "a declaration is not a migration" and the books have to be reconciled where
   they actually are.
3. compares the CLI's process-global active profile against that target and
   refuses on mismatch, quoting the exact `nlm login switch` remedy.
4. **compares the ADDRESS**: `profile_account(profile)` — the `email` the CLI
   recorded in `profiles/<name>/metadata.json` — against `hosting.account`, or
   against `migration.from_account` while pending, case-insensitively. Mismatch
   is a refusal whose message is the one quoted in `proposal.md` § Why.
5. binds the profile for the run, and `assert_still_bound()` re-reads the
   config file before EVERY subsequent CLI invocation, because another terminal
   can switch the process-global profile mid-run.

Step 4 is the load-bearing one. `hosting.account` is not a label for a human to
read: it is one side of an equality test whose other side is a live Google
account. `migration.from_account` is the same test during a migration window.
The roster's `hosting_account` and `user` are read by the validator's uniqueness
key `(hosting_account, user, book_or_alias)` and by its
`granted_by == approval.designated_actor` equality — so the roster's addresses
are the identity of a RECORD, and two rows that differ only by a redacted
address collapse into one under that key.

`scripts/nlm_auth.py` closes the loop from the other side: the `company`
profile's stored `email` "set from the vault-held username precisely so the sync
could check it", carried forward by `merge_profile_metadata()` rather than
nulled. **The real address is already held in the vault and in a local CLI
profile store; this repository is the third copy and the only public one.**

### 1.3 The one thing the tests do that fixture literals cannot

Everything in `tests/notebooklm/` writes its own declaration text into a
temporary tree — `_declare_hosting(root, text)` for the sync,
`_validate(text)` for the validator — so twenty of the twenty-one literals are
fixture text and prove exactly as much when synthetic.

The twenty-first is `test_the_committed_record_conforms`:

```python
errors = validator.validate(REPO_ROOT / validator.DEFAULT_REL)
self.assertEqual(errors, [], "this install's own declaration must pass")
```

That assertion's SUBJECT is the live record, and its truth depends on the two
being one file. After the split it still passes — over the synthetic instance —
but it stops asserting anything about the live declaration. **This is the only
thing this change takes away, and § 3.4 is how it is put back.**

## 2. The target flow

### 2.1 Resolution order, once, shared by both readers

```text
hosting_declaration_path(root):
  1. $XFACTORY_NOTEBOOK_HOSTING_DECLARATION   -> absolute, or workspace-relative
  2. <workspace>/.xfactory/notebook-hosting.yaml   (uncommitted, gitignored)
         declaration_path: installs/hermes-install/config/clients/opensoft/notebook-projection-hosting.yaml
  3. nothing                                  -> UNDECLARED
```

Three properties, each chosen against a named alternative:

- **The committed example is NOT step 3.** Today an absent file is the undeclared
  case and a present one is the declaration; after this change the committed
  file is neither — it is a fixture, and the resolver never reaches it. The
  alternative (default to the committed example) was rejected because it makes
  every fresh clone declare an install it is not: the sync would bind to a
  profile named in a fixture, or refuse for the wrong reason.
- **Absent configuration is UNDECLARED, which the requirement already defines.**
  It is a transition state, reported as unmet, and the sync falls back to the
  CLI's default profile exactly as it does today for a pre-requirement install.
  Nothing breaks in a clone that has no configuration, which is what a public
  repository must be able to be.
- **A configured path that RESOLVES TO the committed example is a REFUSAL.**
  This is the fail-closed arm, and it is why the synthetic instance carries a
  marker in the record (`hosting.instance: example`, OQ-C) rather than only in a
  comment: the refusal has to be decidable by the same narrow scalar reader the
  sync already uses, without a YAML dependency and without comparing paths that
  symlinks and worktrees make unreliable.

### 2.2 What each reader does with it

- **The sync**: `HOSTING_REL` stops being a constant and becomes the resolver's
  output. `read_hosting_declaration()` is unchanged in its parsing and gains one
  branch — a declaration marked as an example is not a declaration.
  `_refuse_unusable_declaration()` gains the matching refusal.
  `enforce_hosting_profile()`'s five steps are untouched: same comparisons, same
  refusals, same messages, against a record read from a different place.
- **The validator**: `main()` already accepts `argv[1]`, so the change is
  precedence, not plumbing — `argv[1]`, then the resolver, then `DEFAULT_REL` as
  the fixture. A `--resolved` flag makes the operator check explicit and
  scriptable, and is what Group 5's task runs after the move.

### 2.3 Why every validator stays meaningful with synthetic values

The validator asks eight questions of the record, and not one of them is about
WHICH real account is named:

1. the two-case vocabulary (`operator_hosted` / `self_hosted`);
2. the value is a user-shaped address at all (`@` present, no
   `.gserviceaccount.com` marker);
3. an operator-hosted declaration names `account_type:
   google_workspace_user`;
4. the account's domain **equals the declared domain** — a relation between two
   fields of the record, true or false regardless of what the strings are;
5. `nlm_profile` is present, because a run binds through it;
6. a PENDING migration names both `from_account` and `from_nlm_profile`;
7. the roster's six fields, its `(hosting_account, user, book_or_alias)`
   uniqueness, and its role vocabulary;
8. `granted_by == approval.designated_actor` — again a relation INSIDE the
   record.

Every one of the eight is a property of the record's SHAPE or an equality
between two of its own fields. Synthetic literals satisfy or violate each of
them exactly as real ones do, which is why the negative tests keep their teeth:
`test_a_service_account_cannot_host_a_projection` mutates the account into a
`.iam.gserviceaccount.com` address and still fires; the domain-mismatch test
still mismatches; the roster-uniqueness tests still collide. **The one test that
loses its subject is the one named in § 1.3, and it loses it because its subject
moves — not because synthetic values are weaker.**

## 3. Migration, in the order it must happen

### 3.1 Land the packet (this pull request)

Proposal, design, tasks, delta, README entry, sweep-ledger row. Nothing else.

### 3.2 Ratify

Brett's word on this packet's content. Groups 1-6 of `tasks.md` are gated on it.

### 3.3 Realize, in one Speckit feature, in this order

1. **The resolver first, with the committed record still live.** Both readers
   learn the resolution order; behaviour with no configuration is UNDECLARED and
   with configuration pointing at the current committed path is IDENTICAL to
   today. Provable before anything moves.
2. **The operator move (Group 5).** Brett copies the live record — declaration,
   custody reference, roster, denial, verbatim — into the private home OQ-A
   settles, writes the configuration, and proves the sync still binds. **Until
   this step the public tree still holds the live record**, which is why the
   public flip is gated on it and not on the packet.
3. **The public instance becomes synthetic**, only after step 2 has proven the
   live record is readable from its new home. The reverse order leaves an
   install unable to sync between the two commits.
4. **The delta's text is applied to canon by the archive act**, not by hand.
5. **The fixtures go synthetic** and the four resolver tests land with them.
6. **The docs are rewritten** for the two-file model, after the Q1 docs pull
   request has landed its redactions in the same file.

### 3.4 Replace the check the split costs

Three things, together, are what `test_the_committed_record_conforms` was:

- `test_the_committed_example_conforms` — the same assertion over the synthetic
  instance, which keeps the SHAPE gated in CI;
- `test_a_resolved_declaration_is_validated` — the resolver's output is
  validated, proved over a synthetic declaration in a temporary tree;
- an OPERATOR step in the runbook: `python3
  scripts/validate-notebook-projection-hosting.py --resolved` before any sync
  `--apply`, whose green line is the live record's conformance evidence. The
  live record cannot be checked by this repository's CI without publishing it,
  which is the trade the ruling accepts; what must not happen is the check
  quietly disappearing.

## 4. Why this is a MODIFIED block and not an ADDED requirement

The obligation being changed is the one the promoted requirement already
states — WHERE the declaration is and WHAT may be committed as an instance of
it — so an ADDED requirement would leave canon asserting an address as a
normative example while a second requirement said not to. That is the exact
condition `modified-block-currency` and `added-over-canon` exist to report.

The block therefore carries all four promoted body paragraphs byte-identically,
all five promoted scenario titles, and every promoted bullet except one. The
delta's own header states the divergence and why the reserved
`Removed from canon by` marker is not used: the marker names the retired unit as
a code span carrying its exact text, and that text is the address. **A marker
naming a redacted spelling would name nothing** — `_suppression()` skips a name
that matches no canon unit ("names nothing; buys nothing"), so it would buy no
suppression and produce no defect either. Prose in the delta header is the
honest instrument, and the one `info` carriage-ledger finding is the intended
record.

## 5. Authoring decisions, flagged for veto

- **D-1 — Resolution precedence is env, then workspace config, then
  UNDECLARED.** The environment variable is first because a one-off operator run
  and a CI job both need to override without editing a file; the workspace
  config is second because it is the durable per-machine answer; UNDECLARED is
  last because it is the state the requirement already defines. Alternative
  considered: config first, env as override-only. Rejected as the same order
  written less plainly.
- **D-2 — A configured path resolving to the shipped example REFUSES.**
  Alternative: treat it as UNDECLARED. Rejected: configuration that names a
  fixture is a mistake somebody made, and the undeclared branch would run the
  sync unbound under whatever profile happens to be active — the failure the
  capability exists to retire.
- **D-3 — `example.invalid` for synthetic addresses.** This repository already
  uses it (`demo-intake@example.invalid`, `SENTINEL_EMAIL_0@example.invalid`,
  `hunter2@db.example.invalid`), and RFC 2606 guarantees it never resolves.
  Alternative: `example.com`. Rejected — it is a real registered domain and one
  line in `contracts/` already uses it, so the corpus would carry two synthetic
  conventions.
- **D-4 — The synthetic instance keeps the record's SHAPE byte-for-byte.**
  Same keys, same order, same comment structure, same roster arity — only the
  identity-bearing values change. A reader diffing the example against the live
  record should see identities and nothing else, and a fixture that drifted in
  shape would stop proving the shape.
- **D-5 — The lost CI check is replaced by three things, not one** (§ 3.4).
  Alternative: accept the loss and note it. Rejected: an unchecked live
  declaration is how the original defect arrived — a projection created under
  whoever ran `nlm login` first.
- **D-6 — `sequenced_after: [add-notebook-projection-identity]`.** That change
  ratified both the requirement this delta modifies and the record this change
  splits, so it is genuinely the parent whose OUTCOME this is an ordered delta
  against. `add-notebook-hosting-credential-custody` is NOT declared: it
  authored the `custody:` block, which this change carries unchanged, so
  declaring it would state a fork where there is none. The field is optional;
  declaring it is a choice and this is the reasoning.

## 6. Open questions, in full

### OQ-A — Where does the live declaration live?

**Asked because the ruling deliberately did not answer it**: "hermes-install
config or a private aggregation path — the realization decides, both are already
private". Three candidates, one recommendation.

| candidate | for | against |
| --- | --- | --- |
| **`installs/hermes-install`, `config/clients/opensoft/notebook-projection-hosting.yaml` — RECOMMENDED** | the record's own `custody:` block already names `binding_client: opensoft` and the ratified residency rule puts "live binding instances in the installs"; `config/clients/opensoft/runtime-manifest.yaml` is an existing committed per-client governance record there; private today; **resolvable as ONE workspace-relative path** from the same workspace the sync already walks | one more submodule the sync's resolution may reach into; a checkout without the submodule initialized reads as UNDECLARED (which is correct, and is why that state must stay non-breaking) |
| a private path in the `opensoft/xFactory` aggregation | closest to the sync's own workspace root | the aggregation tracks only `README.md`, `.gitmodules`, `.gitignore` and two dated review documents by its own stated rule; a config tree there is a new precedent for the sake of one file |
| the vault, beside the username `nlm_auth.py` already reads | the credential is already there; nothing new to protect | the record is a GOVERNANCE ARTIFACT: it needs diff review, a commit history, a validator run and a roster that survives a laptop. A vault item has none of those, and `credential-contracts` exists so that MATERIAL goes to the vault and the record pointing at it stays reviewable |

### OQ-B — Does the archived `add-notebook-projection-identity` delta owe a
cross-reference note?

**Recommended: NO.** Measured, not stylistic:

1. `promotion_fidelity` reads TITLES ONLY. `parse_promoted()` builds
   `{requirement_title: [scenario_titles]}` and the comparison branches are
   "requirement absent", "requirement present but scenario titles missing", and
   "REMOVED requirement still present". **No body text and no bullet is ever
   compared**, so the archived delta's address bullet is invisible to the family
   both before and after this change.
2. Its **latest-writer-wins** rule means that once this change archives, IT is
   the authoritative writer of that requirement and the archived one is not
   compared at all.
3. An archived packet is immutable evidence. Q3[A] already dispositions its
   addresses with a dated immutability exception; adding a second edit for a
   different reason would spend that exception twice.

**If the pointer is wanted anyway**, its lawful home is the
`review/redaction-disposition-2026-09-07.md` that Q3 is creating inside that
archived change — one line naming this change as the later writer — and NOT an
edit to the delta itself.

### OQ-C — Does the committed instance keep its path?

Recommended: **keep `examples/notebook-projection-hosting.yaml`** and mark the
instance inside the record (`hosting.instance: example`). The repository's
`.example.yaml` convention for instantiation stubs is real, and renaming would
express the same fact in the filename — but the blast radius, measured by
`grep -c` at `543d47a9`, is **twenty-one references across eight files**:
`docs/lifecycle-notebook-projection.md` (4),
`docs/notebook-projection-migration-runbook.md` (3),
`docs/notebooklm-sync-open-item.md` (2),
`docs/notebook-projection-migration-evidence-2026-08-24.md` (1),
`scripts/sync-notebooklm-books.py` (4),
`scripts/validate-notebook-projection-hosting.py` (4),
`tests/notebooklm/test_validate_hosting.py` (2) and
`tests/notebooklm/test_sync_notebooklm_books.py` (1) — for a signal the
resolver cannot read anyway. The marker is read; a filename is not.

### OQ-D — Do the actor names go to role placeholders?

Recommended: **yes** — `declared_by`, `approval.designated_actor`,
`approval.declared_by`, every `granted_by` and the denial's `decided_by`. Not
because the name is sensitive (it is on hundreds of public governance lines),
but because a synthetic instance that names a real person asserts that they
granted access they did not grant. The validator's
`granted_by == designated_actor` equality means they move together.

### OQ-E — Does the roster record move, or stop existing in the governed tree?

Recommended: **it MOVES, intact.** Seven grants and one recorded denial of
2026-08-27 discharge the ratified obligation that "each share act is recorded",
and the denial exists precisely because leaving a request unrecorded was the
failure the whole lane was raised against. They are evidence. The private
declaration carries them verbatim; the public tree keeps a pointer saying a
roster exists and where it is; the git history keeps the original bytes under
Q0[A]. Synthesising a clean roster in the public file and deleting the real one
would redact a record of governed acts, which `document-lifecycle` forbids.

## 7. Non-goals

- Redacting prose. That is Q1, in a docs pull request, with no governed change.
- Editing archived records. That is Q3, with a dated disposition.
- Rewriting history. Q0[A] accepted HEAD redaction only, because every consumer
  pins openxFactory by commit and digest and a rewrite invalidates every pin.
- Touching `scripts/nlm_auth.py`. Docstrings only; Q1 owns them.
- Reaching the other real-looking addresses in `examples/` and `contracts/`.
  Outside the sheet's four-address set and outside this packet's scope.
- Performing the public flip, or any part of it.
