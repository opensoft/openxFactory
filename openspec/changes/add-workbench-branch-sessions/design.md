# Design: Branch Sessions — The Branch Is The Unit Of Working State

## Context

Two days of dogfooding produced this change. On 2026-07-25 the workbench
learned to CREATE a document (`add-workbench-bullseye-and-create`), which
immediately raised the next question: how does the human EDIT it? On
2026-07-26 Brett decided the answer, and the whole design is one move —
**the working state moves onto a git branch, and the PULL REQUEST is the
formal re-entry into the governed doc system.**

Everything else follows from that move plus three constraints already on the
table:

1. **The ratified gates-happen-on-main rule.** "A lifecycle transition SHALL
   be performed against, and merged promptly to, the default branch to be
   considered real; an unmerged transition on any branch is exploration, not
   status, and MUST NOT be represented as the document's lifecycle state on
   shared surfaces." Read forwards, that rule does not merely PERMIT branch
   editing — it identifies an unmerged branch as the one place ordinary
   editing is legal, and it also dictates the visibility rule (drafts stay
   out of shared surfaces) and the authority rule (the merge is when
   anything becomes status).
2. **The (repository, ref) seam.** `add-dashboard-repo-selector` keyed the
   snapshot source on the pair and gave the serve ONE registry behind it,
   explicitly naming this change as the consumer the key exists for. So a
   session's panels are not an overlay problem; they are a second registry
   entry.
3. **The family's shared-checkout scar tissue.** Multiple sessions share one
   checkout, and this repository family has already paid for cross-session
   clobbering and mid-review tree mutation. A design that switched branches
   in the served checkout would re-open exactly that wound. A worktree
   closes it by construction.

## Goals / Non-Goals

**Goals**: give the human a legitimate place to stand between an idea and a
review; make editing possible without weakening a single gate; make the audit
trail free rather than re-invented; keep `main` the shared truth on every
shared surface; consume the (repository, ref) seam rather than build a second
projection path; keep the served checkout immovable.

**Non-Goals**: per-actor branches; a session-descriptor contract; delete
authority; an in-panel outline editor; hosted sessions; publishing a session
snapshot; relocating gate verbs other than `create-document` onto the branch;
changing the Merge-Master ritual; Track C's chat rail (its grounding set is
C1's change, and this change is what C1 will ground ON).

## Decisions

### D1 — The branch is the unit of working state; the PR is the re-entry
**Decision**: a workbench session's working state lives on a git branch, and
the formal re-entry of that work into the governed doc system is the pull
request.

**Rationale**: the alternatives are both worse in a way that is easy to state.
Writing edits to `main` from the workbench publishes unreviewed work to every
shared surface instantly — the exact failure gates-happen-on-main forbids. A
redline round per edit-batch is the ceremony main-resident documents already
carry, and it is unusable for AUTHORING: nobody drafts a document as a
sequence of proposed-then-applied diffs. The branch is the third option, and
it is the one where NOTHING relaxes: main is still where gates happen, review
is still where authority is exercised, the Merge Master still merges.

**Consequence**: "unmerged" becomes a first-class, legible state of the
workbench rather than an accident, and the human gets somewhere to stand.

### D2 — The branch is named for the TILE, not the actor
**Decision**: `draft/<staging-id>` for a staged topic, and the scope's kind
and id for a cluster or a possible. Two humans working the same tile join the
SAME session.

**Rationale**: Brett's 2026-07-26 decision. The unit of work in this system is
a topic, not a person: the workbench is already scoped to exactly one
topic-bearing tile, the staged topic is already the queue item, and the
readiness gate is already folder-scoped. A per-actor branch would fragment one
topic's drafts across N branches and N pull requests, which is the same
problem the staging packet exists to prevent.

**Consequence**: same-tile concurrent writing is possible, and is a named risk
below rather than a surprise. Per-ACTOR variants remain a future option if
collisions hurt in practice; the branch-naming rule is the only thing that
would change.

### D3 — A WORKTREE, never a checkout switch
**Decision**: the session branch is materialized as a git worktree. The served
checkout is never switched, reset, or stashed by any session operation.

**Rationale**: this is the load-bearing safety decision. The served checkout is
shared — by the serve, by the snapshot generator, by whatever other session is
working in it — and a surface that switched its branch would break all of them
at once, silently, in a way that looks like data loss. A worktree makes the
hazard structurally impossible rather than merely forbidden, which matters more
than usual here because this family has already been bitten by shared-checkout
mutation and has the incident records to prove it.

**Consequence**: worktrees are real directories that must be created, placed
somewhere gitignored, and torn down. Teardown is therefore part of the
lifecycle requirement and not an afterthought, and the notebook projection's
existing worktree exclusion already anticipates the placement.

### D4 — One commit per gate action, and the record names its commit
**Decision**: every gate action inside a session is exactly one commit carrying
both the documents it wrote and the gate-action record attesting to it, and the
record references that commit as a `commit`-kind artifact.

**Rationale**: the gate-action-record family has always wanted a record and its
artifact to be inseparable, and it can only approximate that when records and
documents land through different paths at different times. Riding one commit
makes it structural. The bonus is larger than the mechanism: the audit trail
FALLS OUT of version control. A reviewer reading the PR's commit series is
reading the action log, and there is nothing to reconcile because there is only
one artifact.

**Consequence**: a long session produces many small commits, and they are KEPT —
see D18. That is not a tolerance for noise: per Brett's 2026-07-26 ruling the
commit series is traceability evidence for medical FDA clearance, so the
granularity this decision creates is regulatory record and not merely a
convenience for reviewers.

### D5 — `edit-document` is session-only; the redline path is untouched
**Decision**: a new human-only gate verb `edit-document` rewrites an existing
document, valid ONLY inside an active branch session. The gate console's
`edit-apply` AI-redline path remains exactly as it is for MAIN-RESIDENT
documents outside a session.

**Rationale**: the two acts differ in risk, so they differ in ceremony. Editing
a document on `main` changes shared truth the moment it lands, and its
protection is the redline a human must apply. Editing a document on an unmerged
branch changes nothing anyone else sees, and its protection is the pull request
review — which is a STRONGER control than a redline, applied once to the whole
session rather than piecemeal. Keeping both is not redundancy; removing either
would be a loss.

**Consequence**: the verb must refuse outside a session, and that refusal is a
requirement scenario rather than an implementation detail — it is the boundary
that keeps the redline path meaningful.

### D6 — The session snapshot is a registry entry, not an overlay
**Decision**: the session's panels read a snapshot addressed `(repository,
session-branch)` through the registry `add-dashboard-repo-selector` lands,
generated from the worktree, regenerated after every gate action.

**Rationale**: the tempting alternative — render `main` and overlay the
branch's diff — invents a second projection path, a merge semantics, and a new
class of bug where the overlay and the snapshot disagree. The seam already
exists precisely to avoid that, and it was keyed for this consumer before this
consumer existed. Generating a whole snapshot from a worktree is the same
deterministic generator run against a different root, which is a configuration
difference rather than a code path.

**Consequence**: regeneration per gate action, which collides with the promoted
"still no per-commit regeneration" clause of `Delivery and regeneration` — a
clause that is true of the PUBLICATION lane and false of a session. The
MODIFIED requirement scopes it rather than deleting it.

### D7 — Draft visibility is confined to the session
**Decision**: branch drafts appear ONLY inside their session. The wheel, the
funnel, the pipeline board, the hosted dashboard, and every published
projection render `main`.

**Rationale**: this is gates-happen-on-main applied to the workbench. A shared
surface that showed unmerged drafts would silently redefine what the team's
pipeline picture MEANS — the wheel would stop answering "what is governed" and
start answering "what has anyone typed", and no viewer would be told which
question they were looking at.

**Consequence**: a real usability edge, recorded as a risk: a human who "saved"
in a session and then cannot see their work on the wheel needs the surface to
say why. The freshness header naming the session ref (D6) is half the answer;
the other half is that `open-pr` is called SAVE for exactly this reason.

### D8 — `open-pr` is "save", and it hands off rather than deciding
**Decision**: the save gesture is a gated `open-pr` verb that pushes the branch
and opens the pull request into the EXISTING Merge-Master ritual, recording the
dispatch. It cannot merge, approve, or bypass anything.

**Rationale**: the recorded-dispatch discipline the whole gate console already
follows — surfaces dispatch and never execute final actions. There is no new
approval path to design because the right one already exists and is enforced
outside the dashboard by branch protection. Calling it "save" is deliberate:
the human's mental model is saving, and the honest implementation of saving in
a governed system is offering work for review.

**Consequence**: "save" is a slightly heavier gesture than a save button, and
the readiness-gate question (the one remaining open question) is a direct consequence — the
recommendation is NO, because a draft PR is exploration and the readiness gate
guards PROPOSE, not SAVE.

### D9 — A session ends by merge or by abandon; abandon ends the SESSION only
**Decision**: two endings. On merge, teardown plus a main-view refresh, AND the
session branch is DELETED. On abandon, teardown plus a recorded reason — but
abandon MUST NOT delete pushed history or close a pull request on the human's
behalf.

**Rationale**: the two endings are asymmetric because their evidence is. A
merge has already preserved everything the branch held, on `main`, under the
Merge-Master ritual — so the branch is pure residue, and leaving it behind only
contends for its own deterministic name the next time the tile is worked (the
collision that decision D17 now handles). An abandon has preserved
nothing: an abandon that deleted a pushed branch would destroy potentially
auditable, potentially collaborative work with one click on a COLLABORATIVE
branch — the worst possible pairing with D2. Ending the session (worktree,
registry entry, notebook) reclaims all the local state that costs anything,
while the pushed branch and its PR remain reviewable evidence.

**Consequence**: abandon is recorded with a reason, like a demotion, because
"why did this topic's session end without merging" is durable signal. Branch
deletion is in-surface for the merge path only; on the abandon path it stays a
deliberate git action outside this surface. Because a surviving abandoned
branch is evidence rather than working state, it does NOT hold the tile: D15's
propose gate keys on the live session, not on branch existence.

### D15 — An unresolved session blocks `propose`
**Decision**: `propose` REFUSES while the tile carries a live branch session,
naming the session and both resolutions (merge the PR, or abandon to discard).
A session is unresolved while its snapshot registry entry is live; merged and
abandoned sessions are both resolved.

**Rationale**: proposal is the END of the staging pipeline — it commissions
authoring against the topic as it stands. Commissioning that while a session's
drafts sit unmerged on a branch proposes from a state the authoring workflow
cannot see and no reviewer can review, and it silently strands the session's
work: the proposal lands, the tile moves on, and the branch becomes orphaned
working state nobody owns. Forcing the choice at the boundary is the cheapest
place to catch it, and it needs no new verb — `open-pr`→merge and
`abandon-session` are exactly the two resolutions and both already exist.

**Consequence**: this change MODIFIES `add-propose-verb`'s "Staged-topic
proposal commissioning" requirement, so `add-propose-verb` joins the
archive-sequencing list. No other forward transition is gated: mid-pipeline
verbs leave the tile in staging where a session is legitimate working state,
and only proposal ends the pipeline.

### D18 — A session PR lands as a MERGE COMMIT; the series is never squashed
**Decision** (Brett, 2026-07-26, closing the staged topic's SQUASH-VERSUS-MERGE
question): session pull
requests merge with a MERGE COMMIT, preserving every gate-action commit on
`main`. A noisier `main` is accepted deliberately.

**Rationale**: Brett's reason is external, not aesthetic — "these are docs and we
are trying to have full traceability for medical FDA clearance, so keeping every
commit is better." That converts the merge method from a history-hygiene
preference into a constraint derived from a REGULATOR. Squashing would collapse
the per-action granularity D4 exists to create and leave it only inside the pull
request, which is a GitHub artifact rather than governed content — evidence
custody delegated to a forge. Under a clearance regime that is the wrong place
for it: the record must survive independently of the vendor hosting it.

**Consequence**: this reason MUST travel with the decision, or a later change
switches to squash for tidiness and silently deletes regulatory evidence. Note
that NOTHING mechanically enforces it today — squash and rebase are both still
enabled on `opensoft/openxFactory` and `opensoft/codexFactory`, and no org
ruleset forbids them, so the protection is currently review-only. Closing that
(disabling squash on the Tier-1 repositories) is a follow-up this change does
not own, because the Merge-Master ritual is explicitly out of its scope.

### D19 — A full notebook quota degrades the session; it never blocks it
**Decision** (Brett, 2026-07-26, closing the staged topic's NOTEBOOK-QUOTA
question): when the
NotebookLM quota is exhausted, the session STARTS anyway, without a notebook,
and the human is notified.

**Rationale**: a session's governed value is its branch, its commits, and its
pull request; the notebook is an L1 analysis convenience. Refusing to open a
session because an external SaaS quota is full would let a third party block
governed work — and under D18's clearance framing, block the creation of
regulatory record. The requirement already makes the notebook optional (`MAY
carry ONE`), so this changes tooling behaviour and no contract. The third
original option, evicting the oldest RETIRED notebook, was removed by D16: a
retired notebook is deleted, so there is no pool of retired notebooks to evict.

**Consequence**: the notification must be honest about WHOSE limit was hit.
Notebooks are per-TILE, not per-engineer (D2 — two humans on one tile share one
session and therefore one notebook), and the quota is consumed from ONE shared
NotebookLM account by three competing populations: the three lifecycle books,
every live `xf-wb-*` reference-set notebook, and every live `xf-session-*`. So
the count scales with CONCURRENT TILES ACROSS EVERYONE, not with the engineer
who happens to trip it, and the message must say so rather than implying the
human opened too many sessions. Note the shared-account model is an inference
from the tooling (`nlm` takes no account parameter; credentials are one cookie
jar under `~/.notebooklm-mcp-cli/`), not a documented decision — the account
model is unspecified anywhere in the corpus, and worth deciding separately.

### D17 — Reworking a tile with an abandoned branch: RESUME or NEW, and the branch dies at the proposal
**Decision** (Brett, 2026-07-26, closing the staged topic's BRANCH-NAME-REUSE
question): when the
first gate write lands on a tile whose previous session was abandoned and whose
branch survives, notify the human and offer two continuations — RESUME the
abandoned branch under its existing name, or start NEW under the next ordinal
(`draft/<staging-id>-2`). Separately: once the topic's PROPOSAL exists, a
surviving abandoned branch MAY be deleted.

**Rationale**: the collision this resolves is much narrower than when the
question was written, because D9 now deletes the branch at merge — so the only
way a tile's name is still occupied is an abandon, the one ending that
deliberately keeps pushed history. At that point the interesting question is
not what to NAME the new branch but whether the human wants the abandoned work
back. Silently allocating an ordinal answers the naming question and throws away
the more useful one; silently reusing the name would attach a new session to old
commits without the human saying so. Asking costs one prompt at exactly the
moment the human has the context to answer, and it is the only moment the
question is cheap. Letting the human name the continuation freely was rejected:
that would break D2, since two humans could pick different names for one tile
and fork it into two sessions.

The second half gives abandoned branches an END OF LIFE they previously lacked.
"Abandon never deletes pushed history" was absolute, which meant every abandoned
exploration accumulated forever. A proposal closes its topic off — once one
exists, the abandoned branch is no longer evidence anyone needs, so it becomes
deletable. That is a retention rule, not a weakening of the abandon rule: abandon
still never deletes anything at abandon time, and nothing is destroyed on the
strength of a `propose` DISPATCH, whose commissioned authoring may not have
produced a proposal yet.

**Reconciliation with D18's traceability requirement**: deleting anything can
look like it contradicts "keep every commit for FDA clearance", so the line is
stated rather than left implicit, because an auditor will ask. It follows from
the already-ratified gates-happen-on-main rule: an unmerged transition is
EXPLORATION, NOT STATUS. So merged history is the regulatory record and is
preserved commit-by-commit under D18; an abandoned branch never became status at
all, none of its gate actions were ever real, and the abandon ITSELF is a
recorded gate action on `main` carrying a reason — which is the durable trace
that the exploration happened and why it stopped. Deleting the branch therefore
removes no evidence the record depends on. What would be a violation is deleting
a MERGED session's commits, which D18 forbids.

**Consequence**: the ordinal mechanism survives but now carries meaning — a
`draft/<staging-id>-2` exists only where a previous attempt was abandoned AND
the human chose not to resume it, which is real signal rather than a counter of
how often a topic was worked. Two realization constraints follow: the highest
existing ordinal MUST be computed against the REMOTE, or two machines allocate
the same ordinal; and the prompt MUST be suppressed once any session is live, or
concurrent writers could answer it differently and fork the tile.

### D16 — A session notebook is RETIRED at session end; it never survives
**Decision** (Brett, 2026-07-26): retire the NotebookLM notebook when the
session ends, by either route. There is no re-pointing at `main` and no
surviving post-session notebook. This resolves the contradiction the adversarial
review found between the staged claim 7 wording ("retired, or re-pointed at
`main`") and the dashboard delta's unconditional teardown.

**Rationale**: after D9 the notebook has no source to survive on — merge deletes
the branch and tears down the worktree the notebook synced FROM. Re-pointing at
`main` would also invent a notebook class the promoted spec does not govern: a
re-pointed notebook is neither one of the three lifecycle books nor a §7 hybrid,
which requires a Canon release line, an enumerated origin folder, and a
`00 [hybrid charter]` seed. And it would duplicate a projection that already
exists — once merged, the topic's documents project into the lifecycle books by
the ordinary sync, which is what those books are for.

**Consequence**: the notebook's life is exactly the session's life, as the
requirement states. If a session's ANALYSIS (as distinct from its documents)
ever needs to outlive the branch, the route is an explicit conversion to a §7
hybrid under that section's existing charter and seeding rules — a future
change, not a silent re-point. Nothing in this change creates that route.

### D10 — NO session-descriptor artifact; the session is derived state
**Decision**: no new schema and no persisted session manifest. A session IS its
branch, its worktree, its registry entry, and a notebook alias derived from the
tile.

**Rationale**: every fact about a session is already derivable from git plus
the registry — the branch name derives from the tile, the worktree from `git
worktree list`, the notebook alias from the tile, the action history from the
commit series. A descriptor would be a second copy of all of that, capable of
disagreeing with the first, and disagreement is precisely what the
commit-per-action decision (D4) was designed to eliminate. Topic claim 10 says
the snapshot registry is the whole server-side addition, and holding to that is
worth more than a convenience.

**Consequence**: recorded honestly — a descriptor becomes necessary if sessions
ever need to carry facts git cannot answer (a session spanning repositories, a
session with an owner distinct from its committers, a scheduled expiry). Until
then, derived state cannot rot.

### D11 — Session notebooks are the one surface allowed to read a worktree
**Decision**: `xf-session-<topic>` session notebooks sync FROM the worktree. The
three lifecycle books (`xf-ideation`, `xf-drafts`, `xf-canon`) stay MAIN-ONLY
without exception. The `xf-session-` prefix is deliberately DISJOINT from the
workbench's `xf-wb-*` reference-set namespace: `add-ideation-dashboard` requires
the notebook sync to sweep every orphaned `xf-wb-*` notebook, liveness is proven
only by a workbench manifest, and D10 gives a session no manifest — so a session
notebook titled `xf-wb-*` would be an orphan from birth and the next routine
`sync-notebooklm-books.py --apply` would delete it mid-session. Renaming keeps
the two lifecycles independent without re-cutting the sweep's contract.

**Rationale**: a lifecycle book IS the lifecycle projection, so a book
containing unmerged sources is not a stale book — it is a WRONG book, asserting
lifecycle states that do not exist. Session notebooks are not books; they are
the same derived analysis workspace the promoted hybrid requirements already
describe, pointed at a worktree instead of a checkout. And that pointing is
possible only because NotebookLM knows uploaded SOURCES rather than git, which
is why this is projection TOOLING and not a contract change to the notebook
family beyond declaring the rule.

**Consequence**: the promoted `Corpus scan scope` requirement must be modified,
because its worktree exclusion currently reads as absolute across the whole
projection. The modification narrows the exclusion's SCOPE to the lifecycle
books while strengthening it there (naming branch-session worktrees explicitly)
and states that session notebooks may never contribute to a book.

### D12 — Local plane only, with `ref` as the future binding point
**Decision**: branch sessions are local-plane only. The hosted dashboard
exposes none of it until the intent plane's apply lane (§4 of
`add-ideation-intent-plane`) exists.

**Rationale**: a hosted session would need to apply writes the hosted surface
holds no authority to make — the same constitutional boundary
(`execute_final_action: false`) that keeps the pod from commissioning a rebake.
The intent plane's apply lane is the mechanism that will eventually produce a
ref legitimately, via its rolling PR.

**Consequence**: the requirement states the hosted surface exposes NONE of
this, rather than leaving it implicit, and the arrival path is named: bind the
apply lane's ref through the existing (repository, ref) seam. No redesign, one
binding.

### D13 — Additive gate-action-record growth, and what CANNOT be schema-required
**Decision**: `action` gains `edit-document`, `open-pr`, `abandon-session`;
artifact `kind` gains `commit` and `pull-request`; `target` gains an optional
`ref`; three per-action conditionals constrain only the new actions
(`edit-document` → `document` + `ref` + a `commit` artifact; `open-pr` → `ref`
+ a `pull-request` artifact; `abandon-session` → `ref` + `reason`).

**Rationale**: the shape `add-lens-gate-verbs` and
`add-workbench-bullseye-and-create` both used, for the same reason — no
`contract_schema_version` bump, no existing record invalidated, and a
per-action conditional is safe precisely because no record has ever carried the
new action. `commit` and `pull-request` are first-class kinds rather than
`other` on the precedent Brett set on 2026-07-25 for `document`: an audit
consumer should be able to filter for them from the enum.

**Consequence**, stated because it is a real limit: the commit-per-gate-action
rule CANNOT be made a schema conditional for `create-document`, because that
action already exists and can legitimately be performed outside a session where
no commit is produced. Requiring a `commit` artifact for it would invalidate
the non-session case and narrow a pre-existing action — the one thing this
schema's additive posture forbids. So the rule lives in the requirement and is
enforced at the route, and `target.ref` stays OPTIONAL for the same reason even
though the route must populate it for every in-session action.

### D14 — "Branch session" and "workbench session" are different things, named apart
**Decision**: the contract says BRANCH SESSION for the branch-and-worktree
lifetime, and reserves "workbench session" for the UI-lifetime state
`add-workbench-bullseye-and-create` defined (the checked-keyword selection's
scope lifetime).

**Rationale**: the same repository already had to keep two senses of
"workbench" apart (`add-staging-workbench` D5), and this is the same hazard one
level down. The two lifetimes genuinely differ: a workbench session dies when
the human closes the view or opens another scope; a branch session survives
page loads, machines, and actors, and dies only at a merge or an abandon.
Conflating them would make "does closing the tab lose my work?" ambiguous — and
the answer must be unambiguously no.

## Risks / Trade-offs

- **A collaborative branch invites concurrent worktree writes.** D2 puts two
  humans on one branch, and this family has already had two live concurrency
  incidents in a shared tree. Mitigation: each session gate action is a single
  commit against the branch tip, so a losing race fails loudly at commit time
  rather than silently clobbering; the worktree is per-machine, so the collision
  surface is the branch rather than the filesystem; and per-ACTOR branches
  remain one naming rule away (D2). Residual risk: two humans editing the SAME
  document in one session still need to talk to each other, and no mechanism
  here replaces that.
- **Long-lived session branches drift from `main`.** A session open for weeks
  produces a pull request against a moved target. Mitigation: `open-pr` is
  positioned as SAVE precisely to make sessions short, and the ordinary PR
  conflict path is the same one every engineering change already uses.
  Deliberately NOT in scope: automatic rebase or merge of `main` into a session
  branch, which would rewrite a human's working state under them.
- **Commit-per-action inflates history (settled by D18).** A long session
  opens a PR with many small commits. Mitigation: that granularity IS the audit
  trail (D4), the PR view collapses it for reading, and the recommendation is a
  merge commit rather than a squash for exactly this reason.
- **Regeneration cost per gate action.** Every gate action triggers a full
  session-snapshot regeneration. Mitigation: the generator is deterministic and
  already runs in the local loop; a session snapshot covers one repository; and
  the cost is bounded by human action rate, not by commit rate on `main`.
  Residual risk: on a very large corpus this becomes noticeable, and the fix
  (incremental regeneration) is a generator optimization behind an unchanged
  seam.
- **"I saved it — why can't anyone see it?"** D7's invisibility is correct and
  counter-intuitive. Mitigation: the freshness header names the session branch
  (D6), the affordance is called SAVE and its effect is a pull request (D8), and
  the merge is what makes work shared. This is a UX-honesty obligation, and it
  is why the freshness header is a requirement rather than decoration.
- **Worktrees accumulate.** An abandoned-but-not-abandoned session leaves a
  directory and a registry entry behind. Mitigation: teardown is part of the
  lifecycle requirement for both endings, and the container location is
  gitignored and already excluded from the notebook projection's scan.
- **An abandon can orphan an open pull request.** D9 deliberately leaves pushed
  history alone, so abandoning after `open-pr` leaves a PR nobody is driving.
  Mitigation: the abandon record carries a reason and names the branch, so the
  orphan is attributable; closing the PR stays a deliberate human act in the
  ordinary review surface.
- **A gate record on an unmerged branch is not yet an audit fact on `main`.**
  Anything recorded in a session becomes governed status only at the merge.
  Mitigation: that is not a defect but the gates-happen-on-main rule holding,
  and it is why verbs with effects OUTSIDE the branch are refused inside a
  session — a dispatch cannot be un-dispatched if the session is abandoned.

## Open Questions

One, with a recommendation, parked for Brett. It was raised while authoring
this change; the staged topic's own three were all ruled on 2026-07-26
(D17 branch-name reuse, D18 merge-not-squash, D19 notebook quota).

1. **Does `open-pr` require the topic's readiness gate to pass?** A session PR
   could be made conditional on the topic's readiness recommendation having
   fired.
   *Recommendation: NO, and the requirement states it.* A draft pull request is
   exploration offered for review — the readiness gate guards PROPOSE (the
   staging-to-proposal boundary), not SAVE. Gating save on readiness would make
   the readiness gate a precondition of WRITING anything down, which inverts
   what it measures: readiness is derived FROM the documents a session
   produces. It would also strand a session's work unmergeable on a branch,
   which is the one state this whole change exists to eliminate.
(A fifth question — whether a session notebook ever survives its session — was
raised by the 2026-07-26 adversarial review and RULED the same day. It is now
D16, not an open question.)
