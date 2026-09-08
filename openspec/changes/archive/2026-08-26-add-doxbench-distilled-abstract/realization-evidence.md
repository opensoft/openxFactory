# Realization evidence — add-doxbench-distilled-abstract §10.3

**RECORDED — Attempt 2 CLOSED §10.3 on 2026-08-26.** This file is the recipe,
the account of both attempts, and the record they were run to fill. §10.3 is an
operator act: ONE run on the real corpus through a REAL adapter whose abstract
the verifier ACCEPTS. A green suite does not close it — `FakeWorkbenchModelPort`
returns a constant (`doxbench_model.py:1101`) the verifier refuses by design, so
nothing below was filled from a test run. Attempt 1 (below) did not close it and
is kept, because the two defects it found are why Attempt 2 could pass.

## Reachability — the `omp` harness

The bridge lane spawns `HARNESS_COMMAND = "omp"` (`doxbench_bridge.py:109`)
under profile `doxbench-bridge` (`:121`). Needed before starting:

1. `omp` on `PATH`, or `DOXBENCH_OMP_BINARY` pointing at it, or
   `DOXBENCH_OMP_HOME` holding `bin/omp` — the discovery order at
   `test_doxbench_bridge_live.py:98-110`. `omp` is a GUARDED BINARY in
   `tests/hermeticity.py`, so this run happens OUTSIDE pytest.
2. A provider in `~/.omp/profiles/doxbench-bridge/agent/models.yml` under
   provider id `local-proxy` (`doxbench_install.py:70`) serving model id
   `omp-local` (`:76`) — keyless local OpenAI-shaped endpoint (`auth: none`),
   matching the declared `data_handling` ("stays on this host").

## Steps

3. Start via the ENTRYPOINT — the only path declaring `model_port_factory`
   (`cli.py:330-331`); `serve()` has no callers:
   `python3 scripts/ideation_dashboard/cli.py generate-and-open --repo-root
   <checkout> --repository <repo-id> --model-session-root <scratch>/model-sessions`
   (omit the flag and sessions land beside the written snapshot; never inside
   the served checkout).
4. Open a STAGED tile; centre a document that IS in `projection.editable_paths`
   (readable-but-not-editable is refused before any provider, ruling 7(a)) and
   that declares `Topics:` and/or a staging destination (neither = no coverage
   base = refused before dispatch).
5. Switch the region to the model state, press **Generate** — one POST to
   `/actions/workbench/document-abstract`, body
   `{"scope": {...}, "subject_path": "...", "model_id": "omp-local"}`.
   The request shape is CLOSED and carries ONE optional extra field,
   `"refresh": true` — the EXPLICIT REFRESH INTENT the **re-generate** control
   issues, and nothing else does. **Generate** omits it; so do the mount, a
   selection change and a tile re-entry. Absent means "replay a completed
   answer for this key with no second dispatch"; `true` means "invalidate that
   answer, dispatch again, replace it". Anything other than a JSON boolean —
   `1`, `"true"` — is a MALFORMED request, and an unknown key still is.
6. Capture the response body verbatim. Success carries exactly `ok,
   subject_path, subject_digest, model_id, prose, caption_state, generation,
   wait_bound_seconds`.
7. **Press re-generate on the same document, unchanged.** The body is identical
   plus `"refresh": true`, and a SECOND dispatch must occur — the harness opens
   a second turn in the same `doxbench-abstract` conversation, and the returned
   `generation` moves. Without the intent this press would replay step 6's body
   byte for byte, which is the inert control packet review found (Codex on
   PR #352, landed as `85e05ebe`).

### One note on the model id, and on switching it

The cache key is `(repository, ref, subject_path, content_digest, RESOLVED
model id)`, and `model_id` in the body is the id the human SELECTED. Where the
catalog entry is a routing rule (an `auto` entry) the key and the recorded
`model_id` both carry the id it RESOLVES to, not the rule's — so a run through
`auto` and a run naming the resolved model directly are ONE question and the
second replays. Switching the rail's model and pressing Generate again on an
unchanged document is therefore a SECOND dispatch, not a replay, and the region
shows the not-yet-generated caption in between; that is worth doing once in the
same run, because it is the half of the key a single-model install never
exercises.

### One note on what the session root will hold

The abstract dispatches through a conversation of its OWN — key kind
`doxbench-abstract`, never the chat's `doxbench-conversation`
(`serve.py:doxbench_abstract_conversation_key`, added 2026-08-25 for the
adversarial review's B1). So generating an abstract for a document you have also
been chatting about opens a SECOND harness session under
`--model-session-root`: two session files for one document is the expected
shape, and ONE file serving both would be the defect
(`doxbench_bridge.select_thread`: "one session never serves two threads").
Before that fix the shipped adapter refused the first generation of every
session outright (`BridgeSessionConflict` on an unbound dispatch), so a run
performed against an earlier build recorded nothing about this route.

## Pass criterion

`caption_state == "model-derived"` (the verifier ACCEPTED it); the visible
caption reads `Distilled by a model — not authoritative; regenerable from the
document.` and the region's accessible name is `<title> — <that caption>`. Any
refusal class (`subject-mention-coverage`, `foreign-path`, `subject-not-named`,
`empty`, `no-declared-base`) is a run that did NOT close §10.3 — record it and
run again; never relax the verifier to pass.

## Attempt 1 — 2026-08-26 (did NOT close §10.3)

The first real run of this surface. Operator **Brett**, on the **T100
subscription adapter** (an operator-supplied rig fronting `sonnet` and `haiku`,
not the `omp` bridge lane), subject
`ideation/staging/client-credential-escrow-registry/client-credential-escrow-registry.md`.
Four presses of **Generate**. EVERY answer failed inside the adapter, on
`observed_hashes` — an adapter-side defect, fixed outside this repo — so each
press routed to `model_failed` and no abstract ever reached the verifier.

The run closed nothing, and it found two defects in THIS surface, both fixed by
`change/abstract-length-cap-and-visible-refusal`:

1. **The pane showed no reason.** `model_failed` is an ERROR-shaped body
   (`{ok, error, message}`) and NAMES NO SUBJECT, so the subject recheck at the
   paint boundary returned before recording anything: all four presses left the
   region on the not-yet-generated caption, and the control read as one that did
   nothing. The whole of `ABSTRACT_ERROR_SENTENCES` was unreachable. A refusal
   is now recorded against the path the request was DISPATCHED for, ahead of
   that recheck.
2. **The ask was one no model could obey.** A diagnostic dispatch made during
   the same session — the model answering directly, outside the failing adapter
   path — returned a 2_018-byte abstract against `MAX_ABSTRACT_PROSE_BYTES =
   1_500`. So the answer would have been refused `abstract-too-long`, in full,
   after a model call had been spent — while the VERIFIER ACCEPTED it: every
   claim in it held against the document's own declared fields. Only the length
   bound refused it, and it refused a good abstract. The prompt now asks for
   ~150 WORDS (`MAX_ABSTRACT_PROSE_WORDS`), a number a model can count while it
   writes, and the byte bound stays where the 280px region put it.

§10.3 still wants a run whose abstract reaches the verifier and is ACCEPTED.
Attempt 2 fills the record below.

## Attempt 2 — 2026-08-26 (CLOSED §10.3)

The pass run, on the corpus checkout at main `d4740415` — the #386 fix landed
FIRST, so this run exercised the ~150-WORD ask and the visible-refusal path
Attempt 1 bought, not the build that produced them.

**On the adapter, honestly.** This run did NOT go through the `omp` bridge lane
the "Reachability" section above describes: **`omp` is not installed on this
host**, so the bridge lane was never reachable here. It went through the
operator-supplied **T100 subscription adapter** at
`~/doxbench-operator/t100_serve.py` — a local console that serves the dashboard
with a `model_port_factory` bound to an adapter fronting the `claude` CLI on the
operator's own subscription. §10.3 asks for a REAL adapter, not specifically the
bridge lane ("the bridge lane (§2.2), or the T100 rig's operator-supplied
adapter"), and this is the second of those two. What the run therefore does NOT
evidence is the bridge lane itself — `OmpHarnessBridge` at an entrypoint, its
`doxbench-abstract` conversation key, and the second-session shape the section
above predicts remain covered by the suite and by §2's tasks, not by an operator
run. Anyone re-running this on a host with `omp` should follow the recipe above
unchanged.

**What was captured, and what was not.** The operator read the RENDERED PANE and
the adapter's own dispatch record; they did not open the network tab, so the
response body's `generation` and `wait_bound_seconds` were not captured and are
recorded as such below rather than invented. Both are nonetheless bounded by
declaration: the adapter's `timeout_seconds` is 115, and this was the first
generation for this cache key on a freshly started process.

## The record

> On **2026-08-26** **Brett** generated a distilled abstract for
> `ideation/staging/avatar-pilot-hardening/avatar-pilot-hardening.md` in the
> **openxFactory** corpus — checkout at main `d4740415`, content digest
> `20b36eb37ac3bf7b2bf97682c0979b4528501a61a178f1847bd62fd330be505a` as
> computed by `document_content_digest` over the saved bytes — at the local
> console served by `~/doxbench-operator/t100_serve.py`, whose declared model
> port is the **T100 subscription adapter over the `claude` CLI** (the `omp`
> bridge lane is not installed on this host). The model, as evidenced by the
> adapter's own dispatch record, was **`claude-haiku-subscription.low`** — that
> label in `turn-timings.jsonl`, and `adapter.log` carrying `dispatch ok
> model=haiku dur=27s prompt_bytes=15314 proposals=0`. The returned abstract was
> **1119 bytes**, inside `MAX_ABSTRACT_PROSE_BYTES = 1_500`, and read:
> "avatar-pilot-hardening.md is a staged architecture specification for
> replacing the avatar-pilot's static fixture authority implementation with real
> Hermes control and delegation behind frozen protocol ports, while adding
> per-domain overlays and personas atop the neutral kernel. It details
> commissioning a formal WCAG 2.2 AA accessibility audit, standing up production
> operations and telemetry infrastructure, and executing a staged pilot rollout
> with operational rollback. Seven core claims cover protocol stability,
> delegation layering, domain isolation, accessibility, operations, and
> fail-closed rollback. Six blocking open questions remain on Hermes call-site
> architecture, overlay scope, accessibility targeting, cohort selection,
> kill-switch granularity, and provider contractual ownership. Pilot entry
> requires qualified live voice profiles, SBOM, license review, formal audit,
> client-integrity evidence, privacy review, and penetration test. The
> capability cannot propose until predecessor capabilities complete and all
> blocking questions are resolved." The **verifier ACCEPTED it**: the pane
> rendered the abstract under the ruled caption *"Distilled by a model — not
> authoritative; regenerable from the document."* beside the controls *"show the
> document's own headers"* and *"re-generate from the current version"* — which
> is `caption_state: model-derived` and no refusal class. `generation` and
> `wait_bound_seconds` were **not captured** (the operator read the pane, not the
> network tab); the adapter's declared `timeout_seconds` is 115, and this was the
> first generation for this key on a fresh process.

The pass criterion above is met and §10.3 is closed. No verifier bound was
relaxed to reach it.
