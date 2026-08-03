# D10 Session Findings — 2026-07-31 (not clause evidence; follow-up register)

Findings surfaced during the acceptance pass that are real work items but do
not decide the clause cells by themselves.

## F1 — Header search does not cover staged-topic tiles

- Observed: searching for `workbench-branch-sessions` found nothing although
  the topic tile is on the staged wheel.
- Classification (code-checked): the global header search is wired as the
  funnel source-docs column filter (`funnel.js` `search(term)` hook, #13) —
  staged topics were never in the haystack, so this is a designed scope gap,
  not a regression. Brett's expectation (search finds staged topics) is the
  reasonable behavior; candidate follow-up for the doxBench/dashboard
  backlog.

## F2 — Completeness scorer undervalues mature staged packets

- Observed: `workbench-branch-sessions` (ratified predecessor, zero parked
  decisions in its change) scores 0.5 — the 0.60 gate would refuse it;
  Brett judges ~0.6 appropriate ("open questions are not blockers and only
  mid level").
- Brett's improvement direction, verbatim intent: (a) better analysis in the
  scorer; (b) a RUNBOOK for each staged packet; (c) each packet overview
  should carry every issue RANKED with what-to-do-to-overcome-it, so
  readiness is derived from ranked, actionable issues rather than raw
  open-question counts.
- Disposition: candidate staging topic / brainstorm entry (scorer analysis
  quality + per-packet runbook convention). Does not block D10; the 0.60
  threshold itself is affirmed, the scoring input needs depth.
- Extension (Brett, during the sitting): consider whether STAGED packets
  should adopt a structured multi-doc convention analogous to the
  brainstorm packet pattern (atomic topics + combined/synthesis + summary),
  giving every packet a predictable analysis surface (ranked issues,
  overcome-plans, runbook). Ruled NOT retrofitted onto
  consent-instrument-contract mid-acceptance (topic is one step from exit;
  Step D stays minimal; per-doc scoring). Belongs in the same V2 design as
  the scorer-depth work.
- Design input for that V2 (Brett question during the sitting: "do we want
  to only work on single-doc staging topics?" — answer: no, multi-doc is
  designed-in via fragments/partial promotion): if packets adopt structured
  roles (atomic/combined/summary), the scorer needs PER-ROLE signal
  expectations and the gate must define whether topic readiness means
  all-docs-clear (current min-score behavior) or exit-bearing-doc-clears.

## F3 — Scorer cannot distinguish ready-to-propose from already-complete,
## and misses unlisted open questions

- Observed: the only 0-blocker `ready` topics in the roster
  (`github-administration-plane`, `proposal-origin-contract`) are COMPLETED
  topics retained as provenance — vacuous propose candidates — while every
  genuinely live topic (including `consent-instrument-contract` at 0.458,
  rated ACCURATE by Brett) sits below the bar, partly because core open
  questions dominate and partly because some open questions are not listed
  in the docs at all.
- Brett's direction: strengthen doc analysis (V2): per-packet runbooks,
  ranked issues with overcome-plans, detection of unlisted open questions,
  and a readiness notion that separates "ready to propose" from "nothing
  left because it already promoted".

## F5 — Workbench lens/bullseye cannot form for staging-only-keyword topics

- Observed (Brett, live, Step B): the `consent-instrument-contract`
  workbench lens tab shows "forming: nothing yet — check a keyword to
  stratify this scope" with NO keyword controls at all.
- Root cause (code-traced): `keyword_index` carries declared counts from
  catalogued CORPUS documents only — staging packet docs do not feed it
  (generator.py ~700: "DECLARED counts only; inferred deferred until
  document-cataloging lands"). The workbench lens filters that index to the
  tile's scope; for a single-doc staged topic whose `Topics:` vocabulary
  (`consent-instrument`, `engagement-letter`, `authority-chain`,
  `revocation`) appears in no corpus doc, the intersection is EMPTY and the
  rail renders zero checkboxes. The workbench bullseye is thus structurally
  unusable for exactly the staging-native topics the workbench serves.
- UPGRADED during the same pass: the GLOBAL keyword-lens tab deliberately
  supplies no `onActivate` (lens.js:33), so its bullseye renders NO
  activatable region — display-only by design. The create gesture lives
  ONLY in the workbench lens panel, which is the panel that cannot form
  for staging-only-keyword topics. The two halves interlock: for such
  topics the bullseye-create gesture is unreachable ANYWHERE. Brett hit
  both halves live (empty workbench rail; inert global centre).
- The global lens DID still serve the scope-READING half of the clause:
  checked {consent, party-ladder, credential-contracts, delegation} formed
  a 7-doc all-outer-ring bullseye whose empty centre was read as the
  motivating gap (no corpus doc spans the consent neighborhood).
- Creation fell back to the workbench's standalone per-tab create buttons
  (outline: "＋ new fragment in this topic" / docs: "＋ new document in
  this scope") — the labelled affordance the bullseye comment itself
  mandates ("the gesture is never the only affordance").
- Candidate fixes for the backlog: staged-topic `Topics:` lines feed the
  keyword index (declared-count semantics unchanged), or the tile lens
  seeds its rail from the topic's own declared keywords rather than the
  corpus-filtered index.

## F6 — Lens should offer AI-proposed document directions

- Observed (Brett, live, Step B at the global lens): checked set
  {consent, party-ladder, credential-contracts, delegation} produced 7
  documents ALL in the outer ring — no overlap, empty centre. Brett: "at
  this point the AI should skim the docs and propose a document direction —
  a title and short description of what could be generated."
- Reading: the empty centre IS the motivating gap — no corpus doc spans
  the neighborhood. An AI skim-and-propose affordance at the lens is
  precisely the doxBench grounded-chat use case (010's chat rail grounded
  on scope), extended to the lens surface: scope in, typed document-
  direction proposals out (title + short description + create seed).
- Disposition: doxBench v2 candidate use case; ties to the existing typed-
  proposal machinery (a "document direction" is a create-seed-shaped
  proposal).

## F7 — Cluster list needs drill-in

- Observed (Brett, live): the lens view's right-side clusters list cannot
  be drilled into; the human wants to open a cluster and use its members
  as creation ideas.
- Disposition: dashboard backlog — cluster rows become activatable
  (expand to member docs, each openable in the viewer; optionally a
  create-from-cluster gesture mirroring the bullseye sector gesture).

## F8 — Session NotebookLM notebook creation broken by nlm CLI drift

- Observed (Step B create): the workbench ran `nlm notebook create … --json`
  and the installed nlm CLI rejected it ("No such option: --json"). The
  session opened fully usable without a notebook; the UI printed the
  FR-042/FR-040/D19 remedy (retire a finished tile's notebook, then
  `sync-notebooklm-books.py --session-ref <ref> --apply`).
- Disposition: codexFactory fix — the notebook-creation invocation must
  track the current nlm CLI surface (or feature-detect); also note the
  shared-account quota pressure the notice describes.

## F9 — Session base resolves from local `main`, not the served revision

- Observed (Step B create): the auto-opened session branch
  `draft/consent-instrument-contract` based on `c782d6d` — the repository's
  LOCAL `main` ref, 14 commits behind origin at open time — while the
  created doc's Source line truthfully named the SERVED revision
  `d09d582…`. Harmless in this session (ancestor of origin/main; the topic
  folder is byte-identical across the gap) but a real integrity gap in any
  multi-session tree where local main lags: a session can silently author
  against a stale corpus while its provenance line claims the served one.
- Disposition: codexFactory fix candidate — session base should resolve
  from the served checkout's HEAD (the revision the scope derived at), or
  refuse/warn when local main and the served revision diverge.

## F10 — Serve-plane gate records land untracked in the served checkout

- Observed: `open-pr`, `abandon-session`, and `propose` write their
  gate-action records (and the propose commission descriptor) UNTRACKED
  into the served checkout's `ideation/dashboard/gate-records/` — designed
  ("the record is written LAST and lands in the SERVED checkout, so it
  outlives the branch it names"), but it (a) dirties the served porcelain
  the 9.2 fingerprint clause reads, and (b) leaves audit artifacts with no
  commit sha until a separate governance commit lands them on main.
- Disposition: product design question for the backlog — either the
  records deserve their own commit-per-action on a records lane, or the
  fingerprint clause should name tracked-state-only.

## F11 — Session save vs create affordances are confusable

- Observed (Brett, live, verbatim): pressing what he took for save
  "started a new document… it is terrible UI if that is how we are
  supposed to save."
- Reading: the workbench's per-tab create buttons and the session verb row
  are visually adjacent and insufficiently differentiated; save's ⇪ label
  and placement did not survive contact with a real operator under real
  conditions. This is PRIMARY evidence for the doxBench evolution — 010's
  integrated shell with an explicit, unmistakable Save is the designed fix;
  CHK015's reviewer flag and this finding should be read together.

## F12 — Session-end reconciliation assumes the canonical single-checkout layout

- Observed: `open-pr`'s merge-ending check resolves the checkout's shared
  `refs/heads/main`; in a multi-session tree where another session holds
  the primary checkout dirty and behind, the ref cannot advance and the
  merge can never be observed from a dedicated serve worktree —
  fail-closed refusal (correct posture, preserved verbatim in the
  transcript), resolved via the sanctioned `abandon-session` path.
- Sibling of F9 (session base from local `main`). Disposition: session
  base/end resolution should follow the SERVED checkout's branch, or the
  serve should accept an explicit `--session-base`.

## F4 — Bare decision references make docs unreadable standalone

- Observed (Brett, live, while reviewing docs in the workbench): prose like
  "read-only-ness is D16 working" where `D16` is defined nowhere in the
  doc — the reader must already hold the defining change's context. Bare
  `Dnn` is also AMBIGUOUS: every change numbers its own D1..Dn.
- Brett's proposed fix, affirmed doable: reference sites carry the
  decision's TITLE and a HYPERLINK to the defining doc.
- Disposition, three tiers: (1) authoring convention — decision references
  outside the defining doc are written `[Dnn — title](path-to-defining-doc)`;
  (2) doc-health finding class "unresolved decision reference", with a
  harvested change→id→title registry making many findings auto-fixable;
  (3) later doxBench viewer sugar — hover previews from the same registry.
  Tier 1 is a documentation-lifecycle convention candidate; tier 2 lands in
  the codexFactory doc-health checker.
