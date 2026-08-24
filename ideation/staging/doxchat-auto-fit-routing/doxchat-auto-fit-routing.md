# Staged: `auto` routes by FIT — per-turn size, capability, and a consented compress-or-refuse path

Status: staged
Kind: capability-proposal
Summary: `contract-v1.38` gives the doxBench catalog a ROUTING RULE whose
resolution is STATIC — an `auto` entry declares `resolved_model_id` and every
turn that selects it reaches that one model. Brett's direction, given at that
release's rule-5 ruling on 2026-08-21, is that the destination should instead be
chosen PER TURN by whether the model can accommodate the assembled context:
never route to a model too small for this turn's packet; when nothing fits, warn
the human and ask, with a session-sticky "continue for all following size
issues" consent; on continue, compress the context to fit the best-fitting
model; and treat size as one dimension among several, because a turn needing
multi-modal input constrains the routable set independently of bytes.
Topics: doxbench, model-catalog, auto-routing, context-fit, context-compression,
consent, multi-modal, ideation-dashboard, capability-routing
Repository context: openxFactory owns every piece this would touch —
`ideation-dashboard` (the doxBench capability and the chat-turn contracts),
`contracts/schemas/xfactory-workbench-model-catalog.schema.yaml` (the routing
declaration `contract-v1.38` released), and the runtime under
`scripts/ideation_dashboard/` (`doxbench_model.py`'s catalog types and
`effective_limit_bytes`, `doxbench_packet.py`'s assembled packet,
`doxbench_bridge.py`'s adapter). No domain repo is implicated; codexFactory is
a downstream CONSUMER of the catalog contract and would re-pin, not co-author.
Staging ID: openxFactory:staging:doxchat-auto-fit-routing
Captured: 2026-08-21
Source: Brett Heap, in-session 2026-08-21, immediately after ruling on rule 5'
of the `contract-v1.38` model-catalog release. The ruling itself ("Swap to rule
5'": bound a routing rule's declared limits against its RESOLVED model rather
than against the minimum over `routes_to`) was made BECAUSE the min-cap would
have baked in semantics contradicting this direction. Brett then said "Stage the
topic", which is this fragment.
Target capabilities: MODIFIED `ideation-dashboard` (per-turn fit-aware `auto`
resolution; the no-fit warn/ask surface and its session-sticky consent;
compress-to-fit as a turn outcome) plus a likely ADDITIVE model-catalog release
(per-model capability declarations beyond byte limits — at minimum a
modality dimension) and a likely additive chat-turn release (a routed turn's
recorded fit decision). Which of those is one change or three is Q5.

## Last proposal attempt (round-trip provenance)

Change ID: none yet
Raised: n/a
Status at demote: n/a
Demoted: n/a
Demote reason: n/a

## Origin quote (verbatim)

Brett Heap, in-session, 2026-08-21 — quoted exactly, because the decomposition
below is an interpretation of it and a reader must be able to check the
interpretation against the source:

> "wouldnt auto have to route to a model that can accomadate the ctx size? so
> just not route to models that are too small? and then if no model large enough,
> warn user and ask to continue and allow use same answer for following model
> size issues this session. if users continues or sets continue all, then we have
> to compress the ctx to fit the largest model best model fit. if we need multi
> modal then we have to select from that. so there are other items besides raw
> size that will determine the 'best' route."

## Claims

The following are what the quote settles. They are the fixed baseline the open
questions iterate against, and they are NOT reopened by them:

1. **`auto` resolution becomes PER-TURN and FIT-AWARE.** The destination is
   chosen when the turn is assembled, against that turn's actual packet, rather
   than declared once in the catalog. This is the direct successor to
   `contract-v1.38`'s static `resolved_model_id`.
2. **A model too small for this turn is not a candidate.** "just not route to
   models that are too small" — the routable set is FILTERED by fit before any
   "best" question is asked, rather than a large packet being sent to a small
   model and refused downstream.
3. **No fit is a HUMAN DECISION, not a silent failure.** "if no model large
   enough, warn user and ask to continue". The turn stops and asks; it neither
   fails opaquely nor proceeds on the system's own judgement.
4. **The answer is session-sticky, at the human's option.** "allow use same
   answer for following model size issues this session" — a human may answer
   once for this session rather than being asked per turn. That is a standing
   consent with a scope (this session) and a subject (model-size issues), which
   makes it a recordable decision and not merely a UI preference.
5. **On continue, the context is COMPRESSED TO FIT.** "then we have to compress
   the ctx to fit the largest model best model fit" — continuing does not mean
   truncating silently or sending an over-budget packet; it means producing a
   packet that fits the best-fitting available model.
6. **Fit is MULTI-DIMENSIONAL; raw size is one dimension.** "if we need multi
   modal then we have to select from that. so there are other items besides raw
   size that will determine the 'best' route." A turn that needs multi-modal
   input constrains the routable set independently of bytes, and the catalog has
   no field for that today.

## Why

`contract-v1.38` released the routing DECLARATION and deliberately stopped
there: an `auto` entry names the models it may route to and the one it currently
resolves to, and the resolution is static. That was the right floor — it made
the ratified "The menu offers a routing rule" scenario claimable and it changed
no runtime — but it leaves the actual routing DECISION unmade. Under static
resolution `auto` is a label for one model, and the interesting behaviour a
human expects from a thing called "Automatic" is exactly the behaviour that is
absent.

The gap is not hypothetical. `effective_limit_bytes` already computes a turn's
budget as the stricter of the server constant and the SELECTED entry's declared
limit, and for a routed turn the selected entry is the RULE. So the current
contract has to require that the rule's declared limits are honoured by the
model that answers — which is rule 5' — precisely because nothing chooses a
destination by fit. Make the router fit-aware and that constraint changes
character: a rule's declared ceiling becomes the widest thing it can serve, and
the per-turn choice guarantees the fit. Rule 5' was chosen over a min-cap for
this reason, and this topic is the other half of that ruling.

## What changes

- **The resolution point moves.** From a catalog field read at menu time to a
  decision taken at turn-assembly time, against the assembled packet.
- **The catalog grows capability dimensions.** At minimum a modality
  declaration; possibly more (Q3). Byte limits already exist and are already
  per-entry, so the size dimension needs no new field — only a reader.
- **A new turn outcome appears: no fit.** Today a turn either dispatches or
  takes one of `dispatch_turn`'s four fixed refusals. "Warn and ask" is neither;
  it is a turn suspended pending a human answer.
- **A session-scoped consent record appears.** Whatever carries "continue for
  all following size issues this session" has a subject, a scope and an
  expiry, which is the shape of a governed decision rather than a UI toggle.
- **Compression becomes a turn-level act with a recorded posture.** The
  assembled packet has a `full | reduced` posture whose release has SHIPPED —
  `contract-v1.40` carries `posture` and `reduced_reason` on the chat-turn
  record, the latter free prose to a 500-code-point ceiling. "Compressed to fit
  model X" is a third thing that reason field can say, and saying it needs no
  contract change at all. (Corrected 2026-08-24: this bullet, Q5's context and
  the Related-work entry all described 10.7's release as still owed. It landed
  as `contract-v1.40`.)

## Impact

- **Consumers of the catalog contract re-pin.** codexFactory pins the model
  catalog by digest; a capability-dimension growth is additive but consumers
  read it or ignore it.
- **The chat-turn record probably grows again.** A routed turn whose
  destination was chosen by fit, possibly after compression, records facts the
  v2 record has no field for — which is the same obligation pattern §13 and
  §11.7 both discharged, and it should be recorded against whichever release
  carries it rather than assumed.
- **The `auto` badge story gets harder, and must not regress.**
  `contract-v1.38`'s covering rule requires a routing entry's own badge to carry
  every routable model's badge as a segment, precisely so a human choosing
  `auto` reads the posture of everything it might reach. Per-turn routing does
  not relax that: the human still chooses before the destination is known, so
  the union badge remains the honest disclosure. Any design that narrows the
  badge to the chosen destination would be disclosing after the fact.
- **A no-fit prompt is a new interruption in the chat rail**, and doxBench's
  ratified posture is that write-implying controls are absent where authority is
  absent. Asking a human to consent to degraded context is a first for this
  surface.

## Idea notes (pre-document, non-documented)

- The fit question already has most of its arithmetic built.
  `doxbench_packet.py` assembles the packet and knows its byte size, and
  `effective_limit_bytes` already computes the stricter of two bounds. A
  fit-aware router is closer to a SELECTION over existing measurements than to
  new measurement machinery. — Added-by: Claude Opus 5 (session, Brett's
  direction) · 2026-08-21
- "Best fit" is stated as an optimisation in the quote ("the largest model best
  model fit") and the two halves of that phrase are not obviously the same
  objective — largest-capacity and best-fitting can diverge, e.g. a
  huge-but-expensive model versus a smaller one that just fits. The topic should
  not assume they are one criterion. — Added-by: Claude Opus 5 (session,
  Brett's direction) · 2026-08-21
- There is an existing staged topic on compression —
  `ideation/staging/context-compression-runtime/` — whose scope is the WORKER
  lane (RAM-only compression stage, three-tier audit, per-domain egress knob).
  Claim 5's compress-to-fit is a doxBench CHAT-lane act, so the two are probably
  siblings rather than one topic, but whichever lands second should reuse the
  first's compression vocabulary rather than invent a second one. — Added-by:
  Claude Opus 5 (session, Brett's direction) · 2026-08-21
- The session-sticky consent has an obvious governance home and an obvious
  cheap home, and they are not the same. Cheap: browser state beside the
  existing chat-state persistence. Governed: a gate-action-style record, which
  is what "the human consented to degraded context for this session" arguably
  is. The cheap one is invisible to any later reader of the transcript, which is
  the same class of defect `add-doxbench-editing-phase-b` §11.7's review found
  in the sidecar. — Added-by: Claude Opus 5 (session, Brett's direction) ·
  2026-08-21
- Multi-modal is named in the quote as an EXAMPLE of a non-size dimension, not
  as the only one. Plausible siblings: tool/function-calling support, structured
  output support, latency class, cost class. Enumerating a closed capability
  vocabulary is the sort of thing this family does well (the roster's
  `admission_surface`, the wallet's custody set) and badly if guessed at
  without consumers. — Added-by: Claude Opus 5 (session, Brett's direction) ·
  2026-08-21

## Conflicts

- **Against `contract-v1.38`'s own shape.** The released entry declares
  `resolved_model_id` as "the model this rule CURRENTLY resolves to", singular
  and static, and the turn record carries it as the model that answered. A
  per-turn router makes the catalog's declared resolution a DEFAULT at best and
  a fiction at worst. The released field is not wrong — it is the static floor —
  but this topic must decide whether it stays, becomes advisory, or is
  superseded, and an additive path is not obviously available for removing it.
- **Against rule 5' itself, in the other direction.** Rule 5' bounds an
  available rule's declared limits by its RESOLVED model's. If resolution
  becomes per-turn, "its resolved model" is no longer a static fact and the rule
  as written has no referent. The natural successor is that a rule's declared
  limits must be honoured by whatever it routes to for a GIVEN turn, which is a
  runtime guarantee rather than a catalog-validation one — a different KIND of
  rule, not a tightening of this one.
- **Against `dispatch_turn`'s closed refusal set.** Its four failure codes are
  documented as CLOSED, and "no model fits, awaiting a human answer" is not one
  of them and is not a failure. Either the set grows (a contract act) or the
  no-fit path is resolved before dispatch is reached. RESOLVED 2026-08-24 the
  second way, though not where this item guessed: the home is the assembly point
  INSIDE step 9, not precondition 7, because the packet does not exist at step 7
  (see Q1's disposition). The route's own `error` string is free-form rather
  than an enum, so the no-fit code costs no contract act and `dispatch_turn`'s
  four closed codes stay untouched.
- **Trim-to-fit ALREADY HAPPENS, silently, and nothing on the wire says so.**
  Found 2026-08-24 while adjudicating Q5. Under today's `posture: full` path the
  server already fits the packet to the selected model's budget rather than
  refusing over-budget context: `serve.py:2935-2956` computes
  `max_packet_bytes` from what the request left and comments that "the packet is
  FITTED to what the request left, rather than refused afterwards";
  `doxbench_packet.bounds_rail` (`:845`, applied `:1013`) performs the trim and
  returns what it dropped as `dropped_evidence` (`:607`, `:1025`). That field is
  a Python dataclass member and appears in NO released schema — it reaches no
  wire field, so a transcript reader cannot tell a trimmed turn from an untrimmed
  one. This does not contradict any claim; it REFRAMES exit (c). Compression is
  not a behaviour this topic introduces — it is a behaviour already running
  undisclosed, and (c)'s real content is making it honest. — Added-by: Claude
  Opus 5 (session, architect adjudication) · 2026-08-24
- **Against the `add-doxchat-model-intake` lane.** That ratified-but-unbuilt
  change owns the selector's operator path (a proposed-versus-approved
  distinction, the empty-catalog default selection, an approval gate action).
  Both changes touch the same selector and the same catalog type. They are not
  contradictory, but they must be sequenced deliberately rather than both
  discovering the same file.

## Open questions

### Q1. Where does the fit decision live — the adapter, the route, or a new selector?

Context: `contract-v1.38` put the RESOLVED id on the catalog and had the adapter
read it (`OmpHarnessBridge._apply_model` sends the resolved id to the harness).
A per-turn decision needs the assembled packet, which the ROUTE has and the
adapter does not — the adapter receives an opaque prompt envelope by design, and
the three-member `WorkbenchModelPort` is ratified as exactly three members, with
"a fourth member is a second provider verb by another name" an explicit
scenario. So the fit decision cannot become a port verb.
Recommended answer: the ROUTE decides, before dispatch. (Corrected 2026-08-24 —
this originally said "at the point where precondition 7 already revalidates the
selected model against the catalog", and that home is WRONG on a verified
ordering fact: the packet does not exist at step 7. The route's steps are 5
scope (`serve.py:2505`), 6 identity, 7 model and effective limits (`:2654`), 8
idempotency (`:2739`), 9 dispatch (`:2866`) — and assembly happens INSIDE step 9
at `:2926`, using step 7's limits. A fit decision at step 7 would be deciding
against a packet that has not been built.) It has the catalog and, at the
assembly point, the packet; the adapter continues to receive one already-chosen
model id and stays unchanged.
Explanation: this keeps the port at three members, keeps the adapter opaque, and
puts the decision where both of its inputs already are. The cost is that the
route grows a genuine policy step rather than a validation step, which is a
change in what that code is FOR and should be argued rather than slipped in.
Disposition status: resolved 2026-08-24 — architect adjudication, recommendation corrected
Disposition (2026-08-24, architect, on verified evidence): the ROUTE decides —
upheld — but at the ASSEMBLY POINT INSIDE STEP 9, pre-dispatch, not at
precondition 7. The sequence is: assemble (or size) the packet, filter the
rule's `routes_to` by fit, choose, then dispatch to the chosen id. The adapter
stays opaque with one already-chosen id and the `WorkbenchModelPort` stays at
exactly three members, so the ratified "a fourth member is a second provider
verb by another name" scenario is untouched.
Two enabling facts make this cheap. The route's refusal vocabulary is NOT
closed — the released failure envelope's `error` is a free-form
`^[a-z][a-z0-9_]{2,63}$` string rather than an enum, which `serve.py:306-312`
states as the basis for its own prior additions — so a no-fit route-level
refusal or suspend code needs NO contract act. And `dispatch_turn`'s four closed
codes stay untouched, because the no-fit path resolves before dispatch is
reached. That is also how conflict item 3 resolves: exactly as it guessed, if
not where it guessed.
Dispositioned-by: Claude Opus 5 (session, architect adjudication) · 2026-08-24
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-21

### Q2. What happens to the released `resolved_model_id` field?

Context: it is released, digest-pinned, consumed by the record derivation and
the adapter, and it means "the model this rule currently resolves to". Under
per-turn routing that is no longer a catalog fact.
Recommended answer: it stays and becomes the DECLARED DEFAULT — the destination
used when the fit computation is unavailable or when exactly one candidate
survives filtering — with the per-turn decision able to override it. Removing it
is a breaking change to a field released weeks earlier and would need a major
bump for no gain.
Explanation: keeping it preserves every consumer pinned to `contract-v1.38`,
preserves rule 6 (`resolved_model_id ∈ routes_to`) and rule 5' as static
guarantees about the default, and makes the new behaviour additive. The honest
cost is a field whose name says "currently resolves to" while the real
resolution is per-turn — a naming debt this topic should either accept
explicitly or pay with a deprecation.
Disposition status: resolved 2026-08-24 — architect adjudication, naming debt accepted
Disposition (2026-08-24, architect): per the recommendation. `resolved_model_id`
STAYS as the DECLARED DEFAULT — the destination used when fit computation is
unavailable, when exactly one candidate survives filtering, and as the static
answer consumers pinned at `contract-v1.38` already read. Rules 5' and 6 keep
their static referent: they remain guarantees about the default.
The naming debt is ACCEPTED EXPLICITLY rather than paid: a field whose name says
"currently resolves to" while real resolution is per-turn is a wart, and it is
recorded in prose here rather than deprecated. No deprecation now; a future
major may rename it. Removing it was REJECTED — a breaking change to a released,
digest-pinned field for no behavioural gain.
Dispositioned-by: Claude Opus 5 (session, architect adjudication) · 2026-08-24
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-21

### Q3. What is the capability vocabulary beyond byte size, and is it closed?

Context: the quote names multi-modal as one non-size dimension and says
explicitly "there are other items besides raw size". The catalog entry today has
`provider_class` (a free-form governance classification, NOT a capability) and
two byte limits. There is no field a router could read to learn that a model
accepts images.
Recommended answer: add ONE closed, additive capability declaration — a
`modalities` set — and resist enumerating latency, cost or tool-calling until a
consumer names itself. The family's own precedent is that closed vocabularies
earn their members from real consumers (the roster's `admission_surface` grew
`device` only when the Opsx node-inventory reader appeared).
Explanation: multi-modal is the only dimension the quote actually names, and the
only one with a concrete near-term consumer (a turn carrying an image). Guessing
the rest produces a vocabulary nobody validates against. The risk of being too
narrow is real but recoverable — an additive vocabulary extension is exactly
what `contract-v1.35` did for the roster.
Disposition status: resolved 2026-08-24 — architect adjudication, with a batching addition
Disposition (2026-08-24, architect): per the recommendation — ONE closed
additive capability declaration, `modalities`, and nothing else until a consumer
names itself. The family precedent holds: the roster's `admission_surface` earned
`device` only when a real consumer appeared, and a vocabulary guessed without
consumers is one nobody validates against.
ADDITION, and it is an obligation rather than a suggestion: the capability
release SHOULD BATCH the two recorded catalog follow-ups that touch the same
`$defs/model_entry` and the same construction gate — the type-side
`models.maxItems` enforcement question, and the `model_id` bounds gap recorded
as review finding N7. Each is to be DECIDED at drafting, taken or re-recorded
with reasons; the release MUST NOT silently pass them by. Batching them is
cheaper than a second cut against the same definitions.
Dispositioned-by: Claude Opus 5 (session, architect adjudication) · 2026-08-24
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-21

### Q4. Is the session-sticky "continue for all" a governed record or browser state?

Context: Claim 4 gives it a subject (model-size issues), a scope (this session)
and an implied expiry (session end). doxBench already distinguishes a human GATE
ACTION — loopback-only, resolved actor, demonstrated console presence, written
as a durable record — from ordinary browser state. A human consenting to
degraded context for a whole session is closer in kind to the former.
Recommended answer: a durable record, but NOT necessarily a `gate-action-record`
enum member. The lighter honest option is that the turn's own record states the
posture it ran under ("compressed to fit `<model>`, under a standing session
consent given at `<turn>`"), which makes every affected turn self-describing
without adding an action to a closed enum. Browser state alone is rejected.
Explanation: the failure mode that matters is a later reader of the transcript
not knowing the answer was produced from compressed context. That is fixed by
the TURN record, not by the consent record — and §11.7's review found exactly
this class of defect (the record was right, the transcript was not). If the
consent additionally needs its own record, that is a smaller question once every
turn already says what it ran under.
Disposition status: resolved 2026-08-24 — architect adjudication under Brett's OQ-3 test
Disposition (2026-08-24, architect): turn-record self-description PLUS a
recorded arm. Browser state alone is REJECTED, as recommended — but the
discriminator the question lacked comes from BRETT'S OWN RULING rather than from
judgement. His intake-lane OQ-3 ruling (2026-08-21) holds that a recorded gate
action suffices on the single-operator loopback console, and that a consent
INSTRUMENT is required only on tenant or shared installs, or where another
party's material is processed. Applying that test:
(a) every affected TURN self-describes — the turn record states the posture it
ran under and its reason names the standing consent ("compressed to fit
`<model>` under session consent given at `<turn>`"), exactly what a later
transcript reader needs, honoring the §11.7 lesson the question already cited;
(b) the consent act itself IS recorded, server-side in the session state, with
subject "model-size issues" and scope THIS SESSION — bounded by session
identity, rekey and generation, NEVER by a wall-clock window, honoring the
no-clock constraint from Brett's arm-and-reconfirm Send ruling of 2026-08-24
(`doxbench-chat.js:242-267`);
(c) on a future tenant or shared install the same act ESCALATES to a consent
instrument per OQ-3 — recorded here as the install-posture fork, not built now.
The shipped arm-and-reconfirm Send is the GESTURE precedent (warn, then a second
press), but it is deliberately per-press and unrecorded. The no-fit ask is the
same gesture family carrying a bigger consequence, which is why it gains the
record the Send gesture does without.
Dispositioned-by: Claude Opus 5 (session, architect adjudication) · 2026-08-24
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-21

### Q5. One change or a sequence, and where does compression's home sit?

Context: the claims span a catalog growth (Q3), a routing behaviour (Q1/Q2), a
human-consent surface (Q4) and a compression act (Claim 5). Task 10.7's
additive chat-turn-success release — the assembled context's `full | reduced`
posture AND ITS REASON — has SHIPPED as `contract-v1.40` (corrected 2026-08-24;
this context said it was still owed), and is the natural field for "compressed
to fit". `ideation/staging/context-compression-runtime/` owns compression in the
WORKER lane.
Recommended answer: three sequenced exits — (a) the capability-dimension catalog
growth, (b) fit-aware routing plus the no-fit warn/ask surface, (c)
compress-to-fit — with (c) explicitly consuming 10.7's posture-and-reason field
rather than inventing a second way to say the same thing, and reusing
`context-compression-runtime`'s vocabulary where the two overlap.
Explanation: (a) is additive and independently useful; (b) is the behaviour
change and the largest; (c) depends on both and on a release this sprint already
owes. Sequencing them lets (a) land while (b)'s design questions are still open,
which is the same shape `add-doxbench-editing-phase-b` used for its own release
obligations. The risk is three changes' worth of overhead for one idea, which is
why this is a question and not a claim.
Disposition status: resolved 2026-08-24 — architect adjudication, (c) redefined by verified facts
Disposition (2026-08-24, architect): THREE SEQUENCED EXITS, as recommended, with
(c) redefined by what the recon found.
(a) **The catalog capability release** — Q3's `modalities`, plus the two batched
catalog follow-ups.
(b) **Fit-aware routing** — the route-level decision (Q1), the no-fit warn/ask
surface with its session consent (Q4), and the turn-record facts (chosen-by-fit,
and BOTH badges per Q6). If the v2 record lacks fields for those, that is an
additive chat-turn growth following the §13 and §11.7 obligation pattern.
(c) **Compress-to-fit DISCLOSURE** — no longer what the recommendation thought
it was. Trim-to-fit ALREADY HAPPENS SILENTLY under `posture: full` (see the
Conflicts entry added the same day: `serve.py:2935-2956` fits the packet to the
selected model's budget, `bounds_rail` performs the trim, and `dropped_evidence`
reaches no wire field). So (c) does not INVENT compression — it makes an
existing act honest. Its content is a third REASON constant under
`posture: reduced`, riding the RELEASED `contract-v1.40` field with ZERO
contract change (free prose, 500 code points; the serve ceiling anticipated
later constants), plus the ruled fit-compression behaviour.
A third posture VALUE is REJECTED: it would need an enum release and four gates,
and the browser adopter silently drops unknown postures — which would mean no
disclosure at all, the opposite of the point. (c) also takes issue #263's
non-blank hardening (the whitespace-only `reduced_reason` hole), because this
change is what makes that field load-bearing, and reuses
`context-compression-runtime`'s vocabulary where the two overlap — noting that
its "tiers" are AUDIT tiers and must NOT be borrowed as compression tiers.
OPEN DESIGN FACT for (b)/(c) drafting, recorded rather than decided: whether
today's silent trim under `full` should itself become a disclosed
posture-and-reason once the field exists. Leaning yes; decided in the change.
Dispositioned-by: Claude Opus 5 (session, architect adjudication) · 2026-08-24
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-21

### Q6. Does the union badge survive per-turn routing unchanged?

Context: `contract-v1.38`'s covering rule requires a routing entry's own
`data_handling` to carry, as a segment, the badge of every model in `routes_to`
— because the human chooses `auto` before knowing the destination. Per-turn
routing does not change that ordering.
Recommended answer: yes, unchanged, and the topic should say so early so no
design drifts into narrowing the badge. The turn RECORD should additionally
carry the chosen destination's own badge, which the v2 record's
`selected_model.data_handling` already carries for the requested entry — so the
after-the-fact disclosure exists and the before-the-fact one is the union.
Explanation: narrowing the menu badge to a predicted destination would disclose
a posture the human cannot rely on, which is exactly what the ratified
requirement's "because" clause forbids. The only real question is whether the
record should carry BOTH badges (the union the human accepted and the specific
one that applied), and it probably should.
Disposition status: resolved 2026-08-24 — architect adjudication
Disposition (2026-08-24, architect): per the recommendation, and stated early so
no design drifts into it. The UNION BADGE ON THE MENU IS UNCHANGED and is a
non-negotiable: the human still chooses `auto` before the destination is known,
so narrowing the menu badge to a predicted destination would be disclosing after
the fact — forbidden by the ratified requirement's own "because" clause.
The turn record carries BOTH badges: the union the human accepted, and the
chosen destination's own. `selected_model.data_handling` already carries the
REQUESTED entry's badge, so the routed growth in exit (b) is what carries the
DESTINATION's.
Dispositioned-by: Claude Opus 5 (session, architect adjudication) · 2026-08-24
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-21

## Related work

- **`contract-v1.38` (this topic's floor)** — the static routing declaration
  released by `add-doxbench-editing-phase-b` task 11.7:
  `routing_rule` / `routes_to` / `resolved_model_id`, seven delegated rules
  including the badge covering and rule 5'. This topic is the successor that
  makes resolution dynamic; the release is what it builds on rather than
  replaces.
- **Task 10.7 of `add-doxbench-editing-phase-b`** — SHIPPED as
  `contract-v1.40` (corrected 2026-08-24; this entry said "still-owed"). The
  chat-turn record carries the assembled context's `full | reduced` posture and
  a free-prose `reduced_reason` to 500 code points. That is the home for a
  "compressed to fit" reason, and why Claim 5 invents no field of its own —
  exit (c) rides the released field with zero contract change.
- **`add-doxchat-model-intake`** (ratified, unbuilt) — owns the selector's
  operator path and the proposed-versus-approved catalog distinction. Same
  selector, same catalog type; sequence deliberately.
- **`add-model-provider-broker`** (ratified) — provisions the `doxbench-bridge`
  profile's credentials. A fit-aware router that widens the routable set widens
  which providers must be provisioned, so the two lanes meet at the point where
  a new destination becomes reachable.
- **`ideation/staging/context-compression-runtime/`** — compression in the
  worker lane; sibling vocabulary for Claim 5.

## Exit

All six questions carry dispositions as of 2026-08-24 — architect adjudications
on verified evidence, anchored in Brett's rulings where they turn on one (Q4 on
his intake-lane OQ-3 test and his arm-and-reconfirm Send ruling; the topic as a
whole on his 2026-08-21 rule-5' direction quoted above).

The topic exits as THREE SEQUENCED CHANGES, per Q5:

- **(a) the catalog capability release** — the closed additive `modalities`
  declaration on `$defs/model_entry`, plus the two batched catalog follow-ups
  (type-side `models.maxItems` enforcement; the `model_id` bounds gap, review
  N7), each decided rather than passed by. Schema, type and validator only.
- **(b) fit-aware routing** — the route-level decision at the step-9 assembly
  point, the no-fit warn/ask surface and its recorded session consent, and the
  turn-record facts including both badges.
- **(c) compress-to-fit disclosure** — a third `reduced_reason` constant riding
  the released `contract-v1.40` field, making an act that already happens
  silently honest, plus the #263 non-blank hardening.

Raise (a) first, at `Status: draft` for a ratification read. This topic exits via
its OWN changes, never via the doxBench editing sprint it builds on.

SEQUENCING — the gate this fragment waited on is CLEARED (recorded 2026-08-24).
The doxBench editing sprint's Phase B change ARCHIVED 2026-08-22 and its owed
chat-turn-success release shipped as `contract-v1.40`, so the static resolution
this topic builds on has shipped and been consumed. What remains is a DIFFERENT
sequencing fact: the model-intake lane listed under Related work (ratified,
unbuilt) collides with exit (b) on `doxbench-chat.js`, `serve.py` and
`doxbench_model.py`. Exit (a) touches none of them and is safe to raise now; (b)
must be sequenced deliberately against that build, which (a)'s own proposal
records. Both lanes are named by id under Related work rather than here, because
this section must not read as claiming another change's exit as its own.
