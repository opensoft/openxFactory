# Tasks: add-notebook-projection-identity

Status: ratified
Ratified: 2026-08-23 — `review/ratification-2026-08-23.md`. Realization mode: DIRECT
(Brett, at the read). These tasks are AUTHORIZED, not performed, by the
ratification.

NOTHING BELOW RUNS BEFORE RATIFICATION. This change's own diff is the spec
deltas and these records; every task here is realization, authorized by the
ratification read and not by the landing of this proposal.

Sequencing matters in one place: §4 (Opensoft's own migration) is the change's
evidence gate and cannot start before §1 and §2 are real, because it is the
first thing to run under a declared account.

## 1. The declared hosting identity, read and honored

- [x] 1.1 Define where an install declares its hosting identity, and the shape
  of the declaration: the case (operator-hosted / self-hosted), the account
  address, and — for the operator-hosted case — the domain the operating party
  administers. Name the intake surface that carries it; no such flow was named
  at capture, and choosing it is part of this task rather than a prerequisite.
  - REALIZED 2026-08-23: Declared in `examples/notebook-projection-hosting.yaml`, beside the workspace registry for this same projection. FLAGGED: the packet left the intake surface unnamed; for the only live install the declaration must be somewhere `sync-notebooklm-books.py` can read, and that file is where the projection's other governed record already lives. A future multi-install intake flow can source it from there without moving it.
- [x] 1.2 Teach `scripts/sync-notebooklm-books.py` to READ the declaration.
  An undeclared install does not BREAK — it keeps today's default-profile
  behavior — but it is reported as NOT MEETING the requirement, a transition
  state rather than a third legitimate case, and is never silently presented as
  governed.
  - REALIZED 2026-08-23: `read_hosting_declaration()` — a narrow scalar reader, not a YAML parse, because this script carries no YAML dependency (the workspace registry beside it is text-handled for the same reason). Undeclared reports a transition state and proceeds.
- [x] 1.3 Bind every CLI invocation to the declared identity's `nlm` profile.
  The script passes NO profile today — `subprocess.run(["nlm", *args])`, no
  flag, no environment — so this touches the single `nlm()` helper rather than
  each call site. A run that cannot resolve the declared profile FAILS; it must
  not fall back to the default profile silently.
  - HARDENED 2026-08-23 on review (Codex P1 + P2, PR #277): the binding is re-asserted BEFORE EVERY invocation from the CLI's own config file, because a single opening check does not bind a forty-minute run when another terminal can switch the process-global profile; and the declaration's load-bearing rules are enforced inline on the operational path, because nothing the sync ran invoked the validator.
  - REALIZED 2026-08-23: `enforce_hosting_profile()`. CHANGED BY A VERIFIED CLI FACT: of the verbs this sync issues, NONE accepts a per-invocation `--profile` — selection is process-global via `auth.default_profile`. So the binding is VERIFIED and the run REFUSES when the active profile is not the declared one, carrying the exact `nlm login switch` remediation. The sync never switches the profile itself: shared user state, and other sessions race on it. While a migration is pending it binds to the account that still holds the books.
- [x] 1.4 Refuse an operator-hosted declaration naming a consumer account, and
  refuse any non-user principal, each with a message naming the reason (missing
  administrative control; the platform's no-API/user-account-only constraint)
  rather than a bare validation failure.
  - REALIZED 2026-08-23: `scripts/validate-notebook-projection-hosting.py` refuses a consumer account for the operator-hosted case (naming the missing administrative control) and any service account (naming the platform constraint), plus a domain mismatch and a third case.
- [x] 1.5 Record Opensoft's own declaration: operator-hosted,
  `xFactor001@opensoft.one`.

## 2. The share-out roster and the governed approval lane
  - REALIZED 2026-08-23: Opensoft's declaration: operator-hosted, `xFactor001@opensoft.one`, Workspace user in `opensoft.one`, profile `company`, migration pending from `brettheap@gmail.com`/`personal`.
- [x] 2.1 Decide and build the roster's artifact form — a contract-family schema
  with a validator, or a lighter governed record. The requirement fixes the six
  fields an entry carries, the stable `(hosting_account, user, book_or_alias)`
  uniqueness key with the decision fields as attributes, and the roster's role
  as the approval record; the artifact shape is this task's call (see design.md,
  "Honest limitations").
  - REALIZED 2026-08-23: DECIDED: a governed YAML **outside `contracts/`**, at `examples/notebook-projection-hosting.yaml`, validated by a dedicated script. Reasoning, flagged rather than left implicit: the record is the operator's own governance artifact for ONE install's tooling account — no other repository, install or domain consumes it and nothing pins it, which is what `contracts/` membership is for — and its sibling `lifecycle-notebook-workspaces.yaml`, the workspace registry for this same projection read and written by the same script, sits there for exactly that reason. The decision is made on the consumer/ownership test, NOT on the cost of the contract-release ritual; promoting the shape into `contracts/` stays available as a later deliberate act if a second install ever needs to interoperate. **No contract-release ritual fires: `contracts/` is untouched.**
- [x] 2.2 Make the grantee part of the uniqueness key, and prove it with the
  case that broke the client-identity roster: two grantees, one book, one
  hosting account — both entries must stand. Prove the converse too: one
  grantee re-approved or re-roled on the same book UPDATES their single live
  entry, leaving no stale grant asserted beside the current one.
  - REALIZED 2026-08-23: Uniqueness is the stable `(hosting_account, user, book_or_alias)` triple. Both directions are tested: two grantees on one book stay distinct (the case that broke the client-identity roster), and a re-decision on one is refused as a duplicate key so it must update the live entry.
- [x] 2.3 Reference an identity-brokering persona where one resolves, with a
  bare address only where none does. `add-identity-brokering` is ACTIVE and its
  capability is not yet promoted, so this is a soft reference today; do not
  create a hard dependency on an unpromoted capability.
  - REALIZED 2026-08-23: Soft reference by design — `add-identity-brokering` is ACTIVE and unpromoted, so the roster carries addresses today and gains persona references when that capability lands. No hard dependency created.
- [x] 2.4 Write the approval lane's procedure: who the designated
  company-policy actor is, where they act (the hosting account's own UI), and
  how approving WRITES the roster entry and denying is recorded in the same
  lane. No API is designed against; the platform has none.
  - **DONE 2026-08-27.** The task asks for a PROCEDURE, not a name, so all three
    halves are satisfied rather than the first alone.
    **WHO — Brett Heap**, ruled by him that day, declared as
    `approval.designated_actor` in `examples/notebook-projection-hosting.yaml`.
    The standing declaration is deliberately separate from a roster entry's
    `granted_by`: this says who MAY decide, the entry says who DID, and the
    ratified requirement needs the first to exist or a request is "left to
    whoever happens to read the account's mail."
    **WHERE / HOW** are written into `docs/lifecycle-notebook-projection.md` §12
    ("The approval lane"): the hosting account's own interface, `nlm share
    invite` as the same act from a terminal, approving WRITES the roster entry
    (which IS the record, never a log beside it), the
    `(hosting_account, user, book_or_alias)` uniqueness triple so a re-approval
    UPDATES rather than duplicates, denials recorded in `denied`, and
    `automated_approval: false` stated in the record rather than inferred.
- [x] 2.5 **DISCHARGED 2026-08-27 — recorded as DENIED.** Brett Heap, the
  designated actor, ruled the 2026-08-15 request stale: "old request and not
  valid". Written into `denied` in the hosting record with the date, the deciding
  actor and the reason. The task's own text allows either outcome — "granted
  through the new lane or recorded as denied" — and this is the deny.
  The requester is not named because the request never appeared in the provider's
  sharing API and lived only in the legacy account's mail; denying it does not
  require naming them, whereas leaving it unrecorded would have been the failure
  this lane exists to prevent.
  Original text: Retire the standing workaround honestly — the pending request from
  2026-08-15 sitting in `brettheap@gmail.com` is either granted through the new
  lane or recorded as denied. It is not left to expire unrecorded.

## 3. Documentation amendments

- [x] 3.1 `docs/lifecycle-notebook-projection.md` section 1: the "quota is one
  shared account" framing becomes the DECLARED hosting account, with the quota
  point preserved (it is still one account per install; that is now a declared
  fact rather than an accident).
  - REALIZED 2026-08-23: §1 now names the declared hosting identity and the two cases; §9's quota sentence attributes the ceiling to the install's one declared account rather than to "one shared account", keeping the capacity point intact.
- [x] 3.2 Section 6's operator runbook: rewrite the auth flow for a declared
  account, including the profile selection. State honestly what is still
  unsolved about authenticating a Workspace user to the CLI rather than
  implying it is routine.
  - REALIZED 2026-08-23: §6 gains step 0 (read and bind the profile) and step 2b (`--parity`), and says plainly that profile selection is process-global and what is verified is the profile NAME, not the address — the CLI stores no email.
- [x] 3.3 Cross-link the two-case custody rule to `credential-contracts` so the
  runbook does not restate the principle it now consumes.
  - REALIZED 2026-08-23: §12 cross-links the rule to `credential-contracts` rather than restating it.

## 4. Opensoft's own migration — the evidence gate
- [x] 4.1 Add a parity/report mode to the sync. 2026-08-10's parity was
  hand-assembled from `nlm source list`; the migration requirement asks for
  parity to be PROVEN, and proving it by hand a second time is how the first
  gap got missed.
  - REALIZED 2026-08-23: `--parity`: per-book title-set equality plus a union reconciliation against THE CORPUS SCAN, reporting only. A test asserts it issues no mutating verb — a parity proof that changes what it measures is not a proof.
- [x] 4.2 Add a bulk session-migration mode, or an explicit per-session
  procedure. VERIFIED GAP: a plain `--apply` never creates live `xf-session-*`
  notebooks — `--session-ref` handles one named session and returns before the
  lifecycle loop, `--session-sweep` only retires. Without this, live sessions
  stay on the account being abandoned.
  - N1 (review 2026-08-23): `scripts/ideation_dashboard/workbench.py` creates session notebooks through its OWN `subprocess.run(["nlm", ...])`, outside this sync's profile binding — a second unbound path to the same account. Scope-adjacent and explicitly covered by this deferral: binding it rides whichever change gives sessions a bulk migration mode. The runbook says meanwhile to migrate sessions through the sync, not the workbench.
  - PROCEDURE LANDED, code deferred to the migration itself: runbook step 5 gives the explicit per-session procedure the task allows as the alternative to a bulk mode (`--session-ref <branch> --apply`, once per live session, enumerated across every worktree). A bulk mode stays worth adding; nothing is migrated until Brett authenticates, so it is not on this landing's critical path.
  - **TICKED 2026-08-31, ON THE PROCEDURE BRANCH OF ITS OWN DISJUNCTION.** The
    box asks for *"a bulk session-migration mode, **or** an explicit per-session
    procedure"*, and the procedure landed (runbook step 5). It is ticked on the
    branch its own text offers, not on the one it deferred. Three facts settle
    the remainder rather than leaving it implied:
    1. **The two sessions the hold was about are GONE.** Step 5 of
       `docs/notebook-projection-migration-evidence-2026-08-24.md` names them by
       branch — `draft/subject-document-estate` and
       `draft/company-provisioning-ledger-estate-subject-onboarding-intake`.
       Verified at this act: `git ls-remote --heads origin
       refs/heads/draft/subject-document-estate
       refs/heads/draft/company-provisioning-ledger-estate-subject-onboarding-intake`
       returns nothing, and `refs/heads/draft/*` returns nothing at all — origin
       carries no `draft/` head. There is no longer a live session sitting on the
       abandoned account for a bulk mode to move.
    2. **F3 — the refusal that actually blocked the per-session run — was FIXED
       THE SAME DAY.** `live_session_targets` now enumerates every worktree git
       lists for each repository rather than asking only the canonical checkout,
       covered by `test_session_ref_sees_a_session_opened_from_a_feature_worktree`
       (evidence document § Findings, F3). The landed procedure is executable,
       not merely written.
    3. **What is left is a live READ, not a code gap**: a `--session-sweep` under
       the personal profile to confirm zero live sessions remain there. That
       needs the interactive authentication § 5.1 records as unavailable, so it
       is **carried with the § 5.1 successor (#537)** rather than held against a
       box its own terms already satisfy. A bulk mode stays worth adding and is
       not owed here; N1's workbench binding rides whichever change adds it,
       exactly as this box's own deferral says.
- [x] 4.3 Add the explicit workspace-record REPLACEMENT step. VERIFIED GAP:
  `ensure_workspace_record()` derives `record_id` from `spec.key`, unchanged in
  the new account; finding that id with a different `provider_notebook_id` it
  returns WITHOUT registering the replacement. Retiring the old record on top of
  that leaves the company-hosted book unregistered. Leave exactly one active
  record per live book.
  - PROCEDURE LANDED, code gap OPEN and stated: runbook step 5 makes the record replacement an explicit numbered step with the reason `ensure_workspace_record()` will not do it. The function still returns `reconcile by hand`; teaching it to replace is a code change that belongs with the migration run, not before it.
  - **TICKED 2026-08-31 ON THE LANDED PROCEDURE. THE CODE GAP IS FILED, NOT
    FORGIVEN.** The note above deferred the code to "the migration run"; **that
    migration HAS RUN.** § Step 6 of
    `docs/notebook-projection-migration-evidence-2026-08-24.md` records that each
    of the seven records in `examples/lifecycle-notebook-workspaces.yaml` had its
    `provider_notebook_id` updated to the new notebook, that record ids are
    key-derived and unchanged so each record IS still the live book's
    registration, and that **none was retired**, per the runbook's step 8.3 —
    which is precisely this box's demand of *"exactly one active record per live
    book"*, met, by the numbered manual step the procedure branch prescribes.
    **The code half is carried as a successor rather than closed by silence:**
    teaching `ensure_workspace_record()` to register the replacement is filed as
    **opensoft/openxFactory#536**, which quotes this box's gap text verbatim —
    *"finding that id with a different `provider_notebook_id` it returns WITHOUT
    registering the replacement"* — and cites this box at its archived path
    `openspec/changes/archive/2026-08-31-add-notebook-projection-identity/tasks.md`.
    Nothing is currently unregistered; what #536 buys is that the NEXT hosting
    move does not depend on an operator remembering a manual step.
- [x] 4.4 Re-derive the three lifecycle books under `xFactor001@opensoft.one`
  in one `--apply` (precedent: 314 sources, roughly 40 minutes), then migrate
  every live session notebook per §4.2.
  - **DONE 2026-08-24**, evidence in PR #289 (`546e0a98`),
    `docs/notebook-projection-migration-evidence-2026-08-24.md`: 7 books, 626
    managed sources. **THE TICK WAS OWED SINCE THAT DATE** — #289 recorded the
    evidence document but touched no task box, so this list read as unstarted
    work that had in fact run. Ticked 2026-08-26 against that recorded evidence.
    The session-notebook half of this task is the separately HELD step 5 and is
    NOT claimed here.
- [x] 4.5 Prove parity: per-book title-set equality plus a union reconciliation
  against THE CORPUS SCAN — not against the legacy books — then a final dry run
  showing zero pending ADD/DEL/UPD. Record the output as the evidence.
  - **DONE — but ticked against the 2026-08-25 run, not the 2026-08-24 one, and
    the difference is the point.** The 2026-08-24 pass (608/608 titles) was
    produced by a parity mode later proven unable to see this class of gap:
    `add-projection-title-uniqueness` (archived 2026-08-25) established that
    comparing derived TITLES against live TITLES *"reports OK on a book that is
    missing documents"*, and measured three collisions, eight documents, five
    displaced — with `ideation-medxfactory`, which our own evidence recorded as
    `PARITY OK: 48 titles match`, among them.
  - The run that satisfies this task is the one taken AFTER that fix, under the
    amended rule: **`parity: PROVEN`, exit 0**, every book reading *N documents
    in N titles* (canon 113/113, drafts 188/188, openxFactory 246/246,
    LedgerxFactory 65/65, MedxFactory 51/51, OpsxFactory 16/16, codexFactory
    14/14), union 675 derived / 675 live managed, **0 unprojected, 0
    unaccounted**, and a convergence dry run planning ZERO operations. Full
    reasoning: `review/retirement-gate-clearance-2026-08-26.md` § 3.
- [x] 4.6 **EXECUTED 2026-08-26.** Seven legacy notebooks were archive-renamed in
  `brettheap@gmail.com`: renamed=7 skipped=0 failed=0; no alias resolves to a
  legacy id; the seven COMPANY books were verified present and un-retitled in the same
  run. NOTHING DELETED. Recorded output, gate-by-gate transcript, provenance and
  the post-hoc parity in
  `docs/notebook-projection-migration-evidence-2026-08-24.md` §"Step 8 —
  EXECUTED 2026-08-26"; the workspace YAML's header now reads RETIRED.
  Ticked from that recorded output, which is what this task's own text demanded —
  not from the act having happened.
  The prior READY-AWAITING-OPERATOR note is kept below for the record:
  **READY — AWAITING OPERATOR EXECUTION.** The gate is CLEARED: Brett
  Heap ruled 2026-08-26 that the 2026-08-24 retirement hold is discharged on its
  own stated terms — the 228KB spec has a projected form — with the live provider
  check as post-hoc confirmation rather than a precondition. Record:
  `review/retirement-gate-clearance-2026-08-26.md`.
  This box stays UNTICKED because retirement is an ACT and nothing in this
  repository can perform it: it renames seven notebooks inside
  `brettheap@gmail.com`, which needs an `nlm` session bound to the legacy
  account, and profile selection is process-global user state the sync refuses to
  switch. Prepared instead, to be run in one sitting:
  **`docs/notebook-projection-retirement-runbook-step8.md`** — seven exact
  renames with the legacy ids resolved from the legacy→company mapping recorded
  in the block headed `# Legacy (still live, pending
  retirement) -> new (live, registered) ids:` at the head of
  `examples/lifecycle-notebook-workspaces.yaml` — their only source here, cited
  by header because a line citation into a file this change edits rots (the
  records' own `provider_notebook_id` fields carry the COMPANY ids), three
  verifications, and the abort conditions. Tick this from the operator's
  recorded output, not from the runbook existing.
  The original task text, unchanged, is what that runbook performs:
  Retire the personal-hosted books by RECORDED ACT: archive-rename each
  legacy book and DELETE its alias (never repoint). Do NOT retire the workspace
  record §4.3 just made current — its id is key-derived and unchanged, so it IS
  the live book's registration; retire the legacy PROVIDER NOTEBOOK and preserve
  the act in the record's history. (This is where the 2026-08-10 runbook does
  not transfer: its successors carried new record ids, so there was a separate
  legacy record to retire.) Record the act.
- [x] 4.7 **EXECUTED 2026-08-27 — 7 of 14 grants landed, the remainder
  provider-blocked. RE-SCOPED TO 7 OF 7 AND TICKED 2026-08-31 BY BRETT HEAP'S
  RULING (in session, `openxfactory-f5`).** The measured history is restated
  first and unretracted; the ruling follows it.
  Brett named two readers and ruled full edit access on all seven company books.
  Executed through the § 2.4 lane on his recorded instruction:
    * **`brett.heap@farheap.com` — GRANTED as `editor` on all seven books.**
      Verified after the fact with `nlm share status <alias> --json --profile
      company`: every book
      lists it beside the owner. The seven `share_out` entries are the record of
      that act, written from grants actually cast rather than backfilled.
    * **`brett.heap@gmail.com` — REFUSED BY THE PROVIDER on all seven**, with
      `API error (code 7)` (PERMISSION_DENIED) and no reason text. Retried with
      the undotted spelling `brettheap@gmail.com`, which Gmail treats as the same
      account: **identical refusal**, so it is the ACCOUNT that is refused, not
      the string. The farheap.com address — a Workspace domain — succeeded on
      every book in the same session, which isolates the difference to an
      external CONSUMER account.
  **THE RULING, 2026-08-31 (Brett Heap, in session `openxfactory-f5`, by explicit
  multi-choice): THE GMAIL GRANTEE IS DROPPED. THE SECOND READER IS NOT WANTED.**
  The task's satisfying set is therefore the SEVEN grants to
  `brett.heap@farheap.com` — cast through the § 2.4 lane, verified after the
  fact, and recorded as the seven `share_out` entries. **Ticked at 7 of 7.**
  There is no eighth-through-fourteenth grant owed, because the grantee those
  seven were owed to is **withdrawn**, not deferred: the denominator changed by
  ruling, and the numerator did not move.
  **Why this is consistent rather than convenient.** Two prior rulings point the
  same way, and are cited rather than invoked:
    * **2026-08-27 — the wind-down.** Brett ruled the legacy books wound down
      **by deletion, performed by the owner himself in his own Gmail account, on
      his own timing** (`docs/lifecycle-notebook-projection.md` § "The legacy
      books: WIND-DOWN BY OWNER DELETION"). A ruling that ends the Gmail
      account's access to the OLD books cannot sit beside a task that grants it
      edit on the NEW ones. Dropping the grantee is that ruling carried forward,
      not a new direction.
    * **2026-08-24 — the sole-grantor posture.** The Google-side posture is
      **RESTRICTED with the app as the sole grantor**, org-visible REJECTED.
      Fewer standing external principals is the posture's own direction of
      travel.
  **The provider refusal becomes a FINDING, not a debt.** Nothing measured above
  is retracted: `brett.heap@gmail.com` was refused on all seven with `API error
  (code 7)` (PERMISSION_DENIED), the undotted `brettheap@gmail.com` was refused
  identically — so it was the ACCOUNT that was refused and not the string — and
  `brett.heap@farheap.com` succeeded on every book in the same session, which
  isolates the difference to an external CONSUMER account. That measurement is
  the record of a real platform boundary. What the ruling changes is that
  **nobody is owed the act it blocked.**
  **The box's two embedded questions were ALREADY RULED, and neither survives
  into the archive as open:**
    * "**A QUESTION FOR THE SITTING**" — whether the legacy owner's continued
      access is an accepted fact or gets wound down: **RULED 2026-08-27 —
      WOUND DOWN**, by owner deletion, in the section named above. The record
      says which was chosen, which is what the question asked for.
    * "**The one known outstanding decision is task 2.5's 2026-08-15 request**":
      **DISCHARGED 2026-08-27 AS DENIED** by Brett as the designated actor —
      ruled stale ("old request and not valid") and written into `denied` in the
      hosting record with date, actor and reason. See § 2.5, which is ticked.
  **What this tick does NOT claim:** that `brett.heap@gmail.com` can reach the
  company books. It cannot; it is no longer meant to; and the record above says
  so in terms. The current human reader of the seven company books is
  `brett.heap@farheap.com` beside the owner `xFactor001@opensoft.one`.
  **SUPERSEDED BY THE RULING ABOVE — kept verbatim for the record:**
  **This box stays unticked deliberately.** Brett asked to "test that they both
  have access", and that test cannot pass today. Ticking would assert a state he
  would disprove the moment he signed in with the Gmail account.
  **WHAT IS OWED, and by whom:** the Gmail grant needs the provider UI (the
  hosting account's Share dialog) or a Workspace external-sharing policy change —
  an operator/admin act, not a CLI one. Note the account is the same one that
  owns the retired legacy books, so it deliberately gains edit on the new books;
  that is stated rather than incidental.
  Prior mapping, kept for the record: **UNBLOCKED BY 2.4 BUT NOT AGENT-EXECUTABLE — and it needs an input
  that does not exist in this repository.** Mapped 2026-08-27 rather than
  attempted.
  Its own text forbids the shortcut: the first roster entries must be "written by
  the governed act rather than backfilled", so an agent writing `share_out`
  entries would defeat the task instead of completing it.
  **WHO ARE THE CURRENT HUMAN READERS?** Corrected 2026-08-27 after review; an
  earlier draft of this note said "nobody", which was wrong as stated.
  Migration evidence step 9 records it precisely:
    * **COMPANY books — owner-only.** Sole collaborator
      `xFactor001@opensoft.one (owner)`. No third party holds access, and no
      pending collaborator request is visible through the provider. So there is
      nobody to share out TO under this task unless Brett names them.
    * **LEGACY books — still readable by `brettheap@gmail.com (owner)`.** The
      legacy owner IS a current reader of the retired content. That is EXPECTED
      rather than a leak: step 8 retired those notebooks BY RENAME and
      deliberately did not delete them, so their owner necessarily still reaches
      them.
  **A QUESTION FOR THE SITTING, not decided here:** does Brett want the legacy
  account's continued access recorded as an ACCEPTED FACT (the personal account
  keeps read access to archived copies) or eventually WOUND DOWN? Either answer
  is legitimate and the record should say which was chosen, because "the old
  owner can still read the old books" is exactly the kind of standing access that
  goes unexamined until someone asks.
  **The one known outstanding decision is task 2.5's 2026-08-15 request**, and
  step 9 says plainly it "is not visible through the provider's sharing API and
  must be resolved from whatever record originated it" — Brett's personal mail.
  Its requester is recorded nowhere here.
  **THE MINIMAL ACT, for Brett:** decide the 2026-08-15 request (grant or deny),
  and name anyone else who should hold access. Granting is
  `nlm share invite <alias> <email> --role viewer --profile company` or the same
  act in the account UI; the decision then writes a `share_out` entry, or a
  `denied` entry, per §12's lane. An agent can reconcile the roster from his
  recorded output afterwards — that is not backfilling, because the act came
  first.
  Original text: Share out to the current human readers from the new account
  through the §2.4 lane, so the first roster entries are written by the governed
  act rather than backfilled.

## 5. Close the operational item and validate green

- [ ] 5.1 **DISPOSITIONED 2026-08-31 — CARRIED FORWARD OUTSIDE THIS PACKET, AND
  DELIBERATELY STILL NOT TICKED.** Ruled by Brett Heap in session
  `openxfactory-f5`, by explicit multi-choice: the condition is **unmeetable
  today**, so this box archives **standing as a disposition** rather than closed,
  and the work moves to a **named successor** outside the packet. That is the
  #537 route, and it is what makes the archive lawful — an archive may carry a
  ruled-open box through provided the record says so in terms, which this does.
  Ticking it would assert a capability nobody has, which is the exact defect
  class this change exists to remove.
  **THE THREE GROUNDS, re-read at this act and all still true:**
    1. **Google's sign-in for `xFactor001@opensoft.one` is an interactive browser
       flow.** There is no unattended path today.
    2. **`nlm login` is additionally broken UPSTREAM** by the notebook.google.com
       rebrand: the CLI's `_is_notebooklm_url()` allow-list accepts only
       `notebooklm.google.com` / `notebooklm.cloud.google.com`, so
       `is_logged_in()` returns false for a browser that IS signed in and
       `nlm login --cdp-url` dies on "Login timeout" after its 300 s wait;
       `NOTEBOOKLM_BASE_URL` cannot be repointed at the new host because it is
       validated against the same allow-list. The CLI's API calls still work —
       only the login path is affected (evidence document § Findings, F1).
    3. **Custody's ratified text forbids the claim.**
       `add-notebook-hosting-credential-custody` states that custody governs who
       may OBTAIN the credential and **does not deliver automation**. No amount
       of custody work discharges this box.
  **THE NAMED SUCCESSOR: opensoft/openxFactory#537** — the deferred
  automated-Google-login item, carrying both halves kept distinct: the upstream
  CLI allow-list defect (F1, tractable now, and it only restores the ATTENDED
  route) and the machine-account "log in whenever it wants" property (the half
  this box is actually about, and the only one that closes it). It cites this box
  at its archived path
  `openspec/changes/archive/2026-08-31-add-notebook-projection-identity/tasks.md`.
  **`docs/notebooklm-sync-open-item.md` STAYS OPEN** and gains a pointer to #537
  in this same landing, so the blocker is not written down only inside an
  archived packet.
  **The 2026-08-26 evaluation this disposition rests on, kept unchanged:**
  **EVALUATED 2026-08-26 AND DELIBERATELY NOT TICKED — the condition is
  not met.** Step 8 executing does not close this item, and the difference is
  the point of the item.
  This open item records the **AUTHENTICATION BLOCKER**, and its "Strategic
  direction (retires the blocker)" is a machine account *"so xFactory can
  re-authenticate **unattended** from a persistent profile — the 'log in whenever
  it wants' property"*. The account moved; **the property does not exist**:
  Google's sign-in for `xFactor001@opensoft.one` is an interactive browser flow,
  `nlm login` is additionally broken by the notebook.google.com rebrand, and
  `add-notebook-hosting-credential-custody` states in ratified text that custody
  governs who may obtain the credential and **does not deliver automation**.
  Ticking this because the migration and retirement landed would assert a
  capability nobody has — the exact defect class this change exists to remove.
  It closes when unattended re-authentication actually works, and that is a named
  successor (the deferred automated-Google-login item), not this task.
  Original text: `docs/notebooklm-sync-open-item.md`: close it on the realization. It
  was deliberately left OPEN by the disposition round (PR #272 added only a
  dated pointer), because it closes on this change's realization and not on the
  rulings. Its "Strategic direction" section is what §4 executes.
- [x] 5.2 Gates: `pytest tests/ideation-dashboard`, `pytest
  tests/ideation_dashboard`, `pytest tests/doc-health`, `OPENSPEC_TELEMETRY=0
  openspec validate --all --strict`, doc-health zero-new against a fresh
  `origin/main` baseline, and `scripts/validate-ideation-dashboard-contracts.py`
  at its 0-error / 4-warning baseline.
  - GREEN AT THE LANDING SQUASH 2026-08-23 (`40b33845`, PR #277): 3983
    passed / 15 skipped (ideation-dashboard); 902 passed / 13 subtests
    (notebooklm + doc-health + ideation_dashboard) pre-merge and 839 + 13 at
    the squash; `openspec --all --strict` 72/72 fresh-counted at the squash (69
    before three other sessions' changes landed alongside); dashboard validator
    0 error / 4 warning; hosting validator 0 error. doc-health ZERO NEW
    attributable to this squash, measured against a baseline taken at
    `7431f033` — the commit immediately before it — because main had advanced
    by fourteen commits from other sessions and a plain pre-merge comparison
    would have charged this change with two `proposal-origin` errors belonging
    to the MedxChart/MedxPractice boundary changes.
- [x] 5.3 If §2.1 lands a contract-family artifact, register it in
  `contracts/manifest.yaml` + `contracts/CHANGELOG.md` at the next additive
  bundle cut and follow `docs/contract-versioning-policy.md`. If it lands a
  lighter governed record, say so explicitly and cut no bundle.
  - RESOLVED 2026-08-23, SAID EXPLICITLY: §2.1 landed a LIGHTER GOVERNED
    RECORD (`examples/notebook-projection-hosting.yaml` plus
    `scripts/validate-notebook-projection-hosting.py`), NOT a contract-family
    artifact. **No bundle was cut and no contract-release ritual fired**: no
    CHANGELOG allocation, no `contracts/manifest.yaml` row or digest, no
    `contract_bundle_version` bump, no inventory rebuild, no verify-commit, no
    tag. `contracts/` is byte-untouched across the whole realization, asserted
    at every gate run and again at the squash. The published bundle remains
    `contract-v1.40`.

## 6. Bookkeeping

- [x] 6.1 Retire the staged topic from `ideation/staging/INDEX.md` once its
  material has moved, per the index's own maintenance rule.
  - **DONE 2026-08-31, in this archive's own commit.** Two edits, in the index's
    own retirement style (precedents: `substantive-review-lane-questions`,
    "CLOSED AND RETIRED FROM STAGING 2026-08-22", and
    `staged-topic-outline-template`, "CHANGE ARCHIVED 2026-08-21"):
    * the `notebook-projection-identity` ROW and its DETAIL SECTION now record
      the archive, both boxes that did not close, and the two successor issues;
    * the sibling row `notebook-access-wallet-governance` said both
      `add-notebook-projection-identity` and
      `add-notebook-hosting-credential-custody` "are ACTIVE with
      ratified-but-unpromoted deltas this topic would amend" — a sentence this
      act makes half false. **Only the projection-identity half is corrected**:
      its deltas are now PROMOTED and the change archived. **The custody half is
      left exactly as it stands**, because it is still true and it changes at
      CUSTODY's archive, not at this one. Touching it here would be this step
      asserting a state it did not produce.
    * **AMENDED 2026-08-31, BEFORE THIS PACKET MERGED — CUSTODY'S ARCHIVE
      HAPPENED IN A PEER LANE WHILE THIS BRANCH WAS IN REVIEW, so the paragraph
      above is spent as a description of today.** **PR #541** archived
      `add-notebook-hosting-credential-custody` and, second, its dependent
      `add-binding-consumer-identity` on Brett Heap's ROUTE-1 ruling of the same
      date. "It changes at CUSTODY's archive, not at this one" names an event
      that has now occurred, so the sibling row's custody half is corrected in
      the SAME landing as this note rather than left to mislead a reader taking
      their sequencing base from it; the correction cites #541 as its author.
      **The reasoning above stands unchanged and is still sound** — this step
      did not produce that state, and it still does not; another lane did, and
      the correction says so. Recorded here rather than in the peer packets
      because THIS packet is not yet merged and its text is still this pull
      request's to correct, while the two archived peer packets are RECORDS and
      are not — this branch's earlier correction notes inside them were DROPPED
      at the catch-up merge of `2f1cd139` for exactly that reason.
    The topic FOLDER `ideation/staging/notebook-projection-identity/` is
    **retained as provenance and deliberately not deleted** — this act promotes
    the deltas and archives the change; deleting staged source is a separate
    disposition nobody has ruled.
- [x] 6.2 README OpenSpec Records: move this change from active to archived when
  it archives, on merged code with green realization evidence.
  - **DONE 2026-08-31, in this archive's own commit.** The row moved from
    "Active changes:" to "Archived changes:" in the house row style, pointing at
    `openspec/changes/archive/2026-08-31-add-notebook-projection-identity/proposal.md`.
    Both preconditions were read rather than assumed: the code surface merged at
    the realization squash `40b33845` (PR #277), and § 5.2's green realization
    evidence is recorded at that squash (3983 passed / 15 skipped
    ideation-dashboard; 839 + 13 subtests at the squash; `openspec --all
    --strict` 72/72; dashboard validator 0 error / 4 warning; hosting validator
    0 error; doc-health zero-new against `7431f033`). The row states the two
    boxes that did not close, so the README does not read as a clean finish.

- [x] 6.3 Adversarial review round (2026-08-23, PR #277): 1 blocking + 5
  should-fix, all reproduced before fixing, all fixed on the branch.
  - **B1** the runbook's re-derivation repointed the aliases its retirement
    step was required to DELETE — the alias store is one flat,
    profile-independent file and `resolve_or_create_book()` registers on the
    FOUND path too. The runbook now records the legacy notebook ids and
    deletes the aliases in step 1, before any `--apply`, per the 2026-08-10
    order; steps renumbered accordingly.
  - **S1** `--parity` issued three `alias set` calls while claiming never to
    mutate. Alias binding is now switchable and off for the read-only caller,
    and the test's blocklist covers `alias set`/`alias delete`.
  - **S2** a hosting file the narrow reader could not parse (flow style,
    four-space, tabs) took the UNDECLARED branch and ran the whole job
    unbound, while the validator passed the same file. An existing file now
    always yields a dict, and an empty one REFUSES.
  - **S3** `migration.state: in_progress` failed the validator and passed the
    sync, which bound the declared profile while the books were elsewhere.
    `_refuse_unusable_declaration()` now owns the state vocabulary and the
    pending-requires-`from_nlm_profile` rule — one rule, one owner.
  - **S4** "the CLI stores no email for a profile" was FALSE:
    `profiles/<name>/metadata.json` carries `email` (`farheap` populated,
    `personal` null). The sync now compares it to the declared account when
    present, reports null as unknown, and the claim is corrected in the
    docstring, §12 and the runbook.
  - **S5** runbook step references were off by one at the stranding point;
    corrected, and the deliberate refuse-window between binding the host and
    flipping the state is now stated.
  - All five new guards revert-tested individually.
- [x] 6.4 Notes recorded rather than fixed (review N2-N5):
  - **N2** a microsecond TOCTOU remains between `assert_still_bound()` and the
    `subprocess.run` after it. It cannot be closed without a per-invocation
    profile flag the CLI does not offer for these verbs; STATED in §12 rather
    than left implicit.
  - **N3** the hosting validator is not wired into CI. The pytest gate
    exercises it against the committed record
    (`test_the_committed_record_conforms`), which mitigates but does not
    replace a CI wiring; a follow-up may add it beside the other validators.
  - **N4** `self_hosted` declarations ignore `account_type` and `domain`, and
    the `denied:` list has no field discipline. Both are realization
    follow-ups: the self-hosted case deliberately carries no organizational
    obligation, and no denial has been recorded yet.
  - **N5** the runbook's `nlm share invite` and §12's "in the account's own UI"
    now describe ONE act with two interfaces, with the decision human either
    way, rather than reading as two different lanes.

## 7. NOT part of this change

- The `xf-wb-*` cross-checkout deletion bug (a routine `--apply` in one checkout
  can delete another engineer's scratch notebooks). Already recorded in
  `docs/notebooklm-sync-open-item.md` as wanting its own change.
- Any automated share-request detection or approval. Revisit only if the
  platform ever exposes a surface; the approval stays a human act regardless.
- Renaming the `credential-contracts` requirement whose body this change
  generalizes. Flagged for the ratification read in design.md, Ruling 2.

## 8. WHAT THIS ARCHIVE DID NOT CLOSE — the honest record (2026-08-31)

Written in the same landing as the archive, so nothing here depends on a reader
finding it in a commit message.

**ONE BOX STANDS OPEN BY RULING, not by neglect.** § 5.1 archives as a
DISPOSITION. `proposal_support.archive_change` refuses any change whose
`tasks.md` still carries a `^- [ ]` line — a blanket gate that cannot tell a
ruled-open item from unfinished work — so this took the same route
`add-signed-execution-chain` took on 2026-08-31 (PR #535), with earlier
precedents at `2026-08-28-declare-sentinel-pin-vocabulary` § 4 and the three
sibling archives of 2026-08-27. **The two things that wrapper adds were run
anyway, on both sides of the move**: `proposal-support.py verify` per-change and
whole-corpus (ok before, ok after), and packaging — a lawful no-op here, because
this change has no `supporting-docs/` at all.

**TWO SUCCESSORS ARE FILED IN THE OPEN, so neither lives only inside an archived
packet:**

| successor | what it carries | from |
| --- | --- | --- |
| **opensoft/openxFactory#536** | `ensure_workspace_record()` returns without registering a replacement when the key-derived `record_id` is found bound to a different `provider_notebook_id` | § 4.3's code half — its procedure half ran and is ticked |
| **opensoft/openxFactory#537** | automated Google login: the upstream `_is_notebooklm_url()` allow-list defect AND the machine-account unattended-re-auth property, kept as two distinct halves because only the second closes anything | § 5.1, in full |

`docs/notebooklm-sync-open-item.md` **stays OPEN** and gained a dated pointer to
#537 in this same landing. It closes when unattended re-authentication actually
works.

**ONE CITATION IS DELIBERATELY LEFT STALE, and the reason is recorded rather
than hoped.** The move makes `openspec/changes/add-notebook-projection-identity`
a stale spelling in exactly three places. Two were fixed here — the `Backed by:`
header of `docs/notebook-projection-retirement-runbook-step8.md` and the comment
citation in `examples/lifecycle-notebook-workspaces.yaml`. The third,
`docs/notebook-projection-migration-evidence-2026-08-24.md` § "Step 8 —
EXECUTED 2026-08-26", is **NOT** fixed: that document carries `Status: record`,
and doc-health's `record-immutability` family raises a **CRITICAL** on any
substantive line change to a captured record, excepting only markdown-link
pairs — which this backticked path is not. **Repointing it would trade a stale
path for a broken immutability guarantee**, and the record's own value is that
it says what was true when it was captured. The path is a citation a reader can
follow to the archive in one step; nothing resolves it mechanically.

**ADDENDUM 2026-08-31, AFTER THE CATCH-UP MERGE OF `origin/main` AT
`2f1cd139` — A THIRD THING THIS ARCHIVE DOES NOT CLOSE, ARRIVING FROM ANOTHER
LANE.** PR **#541** archived `add-notebook-hosting-credential-custody` and its
dependent `add-binding-consumer-identity` on Brett Heap's ROUTE-1 ruling of this
same day, while this branch was in review. Both archived copies leave exactly
one box unticked, and **both point HERE**: custody § 6.2 and the dependent
§ 7.3 — one reconciliation seen from two sides — each restated 2026-08-31 as
*"the obligation attaches to THAT change's archive … whoever archives
`add-notebook-projection-identity` discharges both."*

**THIS ACT DOES NOT DISCHARGE THEM, AND SAYS SO RATHER THAN LETTING SILENCE READ
AS DONE.** What is owed is the FULL read-together of the three packets'
`credential-contracts` text now that all three are promoted — a reading act with
findings of its own, not a side effect of moving a directory. What this act DOES
supply is the precondition it was always the holder of: the operated-identity
generalization is CANON as of this landing (`lifecycle-notebook-projection` +3
added / ~2 modified, `credential-contracts` ~1 modified, all six bodies
byte-identical), so the reconciliation is now performable by anyone and blocked
on nothing. It needs a successor act of its own, and it is written down here so
it does not live only in a commit message.

**THEIR BOXES ARE NOT TICKED FROM HERE EITHER, AND COULD NOT BE.** They sit
inside archived records, which this estate's doctrine forbids amending — the
same doctrine that made this branch DROP its own earlier correction notes inside
those two packets at the catch-up merge. And their *"is STILL ACTIVE and still
`Status: ratified`"* clauses, true when #541 landed and spent the moment this
packet merges, are **dated restatements inside a record** and are left exactly
as that lane wrote them: the very sentence that goes stale is the one directing
a reader to this act, so it points at the truth rather than away from it.

**WHAT IS NOT CLAIMED ANYWHERE IN THIS PACKET:** that `brett.heap@gmail.com` can
reach the company books (§ 4.7 — it cannot, and by ruling it is no longer meant
to); that a live `--session-sweep` under the personal profile has been run
(§ 4.2 — it needs the auth § 5.1 lacks, and rides #537); that a bulk
session-migration mode exists (§ 4.2 deferred it and nothing since added it);
and that unattended re-authentication is possible (§ 5.1, the whole point).

