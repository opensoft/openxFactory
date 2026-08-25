# Realization evidence — add-doxbench-distilled-abstract §10.3

**PENDING — operator run not yet performed.** This file is the recipe plus an
empty record. §10.3 is an operator act: ONE run on the real corpus through a
REAL adapter. A green suite does not close it — `FakeWorkbenchModelPort` returns
a constant (`doxbench_model.py:1101`) the verifier refuses by design, so nobody
may fill the record below from a test run.

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
6. Capture the response body verbatim. Success carries exactly `ok,
   subject_path, subject_digest, model_id, prose, caption_state, generation,
   wait_bound_seconds`.

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

## The record (fill on the run)

> On <date> <operator> generated a distilled abstract for `<subject path>` in
> the `<repository>` corpus through the `omp` bridge lane, model `<model_id as
> echoed>`. The returned abstract was: "<prose verbatim>". The verifier ACCEPTED
> it — `caption_state: model-derived`, `generation: <n>`, `subject_digest:
> <digest>`, `wait_bound_seconds: <n>` — and the region rendered it under the
> ruled model-derived caption, named `<title> — Distilled by a model …`.
