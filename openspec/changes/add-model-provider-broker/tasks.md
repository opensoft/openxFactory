# Tasks: add-model-provider-broker

## 0. Ratification

- [x] 0.1 DECIDED (Brett, 2026-08-08): the broker MINTS a short-lived token
      and doxBench calls the provider directly — brokered dispatch "would be
      too slow".
- [x] 0.2 openProfiler declares its CLI surface AND what a minted token
      carries (lifetime, scope, provider-native or broker-issued). Nothing
      below hardcodes the command; the binding carries the argv template
      precisely so this can land first.
      DECLARED 2026-08-26 — openProfiler PR #18 merged: `openprofiler-broker`
      CLI (`intake`/`mint`/`revoke`/`list` implemented for api_key;
      `authorize`/oauth DECLARED-DESIGN; `--retry-of <audit_ref>` for the
      re-mint rule; secrets on stdin only; one JSON object on stdout, exit
      code authoritative) per `docs/broker-cli.md` at openProfiler main
      `d0538c31`. This tick records that the DECLARATION now exists and is
      landed — which is the whole of what this task asked. It does NOT record
      that this repository's adapter matches it: the cross-check below found
      six incompatibilities, and they are OWED WORK rather than discharged
      work. Read the tick as "there is now a surface to consume", not as "the
      seam consumes it".

      CROSS-CHECKED 2026-08-26 against the merged declaration
      (`opensoft/openProfiler`, `docs/broker-cli.md`, main `d0538c31`,
      PR #18). The declaration
      answers question 1 in full: a minted token is PROVIDER-NATIVE in both
      kinds; on the `api_key` path the minted token IS the stored key verbatim
      and `expires_at` is broker bookkeeping the consumer honours
      (`enforcement.expiry: "broker_bookkeeping"`), while the `oauth` path is
      DECLARED-DESIGN throughout and refuses with exit 5. Six seam findings
      follow. They are 0.2's to close, and recording them is not ticking it.

      ALREADY COMPATIBLE: the exit-code discipline (any non-zero maps onto one
      fixed redacted refusal), one JSON object on stdout with the error object
      on a stderr this adapter captures and drops unread, argv-never-a-shell-
      string, the closed placeholder vocabulary — which cannot name a secret,
      matching the declaration's own `secret_in_argv` refusal — the declared
      timeout, the bounded answer, the scrubbed child environment, and
      `_parse_expires_at` accepting the declaration's ISO-8601 `Z` spelling.
      The adapter also treats `expires_at` as binding and discards rather than
      reuses past it, which is exactly what the declaration asks of a consumer
      on the bookkeeping path.

      FINDING 1 — OPERATION FRAMING. This adapter names the operation in a
      JSON request line on the child's standard input
      (`model-provider-broker-request`, `operation: enroll|mint`). The
      declaration names it as an argv SUBCOMMAND (`intake`, `mint`, `revoke`,
      `list`) and reads no request document at all. A binding here carries ONE
      `broker_argv`; the declaration's own consumer template carries four
      (`intake_argv`, `mint_argv`, `revoke_argv`, `list_argv`). The binding
      needs a per-operation argv map before it can name this broker.

      FINDING 2 — THE ENROLMENT STANDARD INPUT IS CORRUPTED BY THE REQUEST
      LINE. `intake` reads standard input to EOF and treats ALL of it as the
      secret. This adapter writes the request line first and then streams the
      credential, so the broker would take the JSON line plus the value as the
      credential. The hand-off cannot work against the declared surface until
      the request line is dropped for an enrolment.

      FINDING 3 — THE MINT ANSWER SHAPE. `MINT_FIELDS` requires
      `kind: model-provider-broker-mint` plus `endpoint` and `dialect`. The
      declaration emits `kind: openprofiler_broker_mint` and carries NEITHER
      `endpoint` NOR `dialect`, deliberately: the broker is provider-agnostic
      about the request grammar and refuses to name an endpoint it would then
      be accountable for. Every real mint would therefore be refused as
      `DIAG_BROKER_MALFORMED`. Task 2.1 flagged `endpoint`/`dialect` FOR VETO
      pending exactly this declaration, and the declaration has answered: both
      facts must come from the BINDING rather than from the mint answer. (What
      the mint does carry beside `token`, `expires_at` and `audit_ref`:
      `reference`, `binding`, `provider`, `auth_kind`, `token_type`,
      `issued_at`, `expires_in_seconds`, `scope`, `issued_by`, `approved_by`,
      `retry_of`, `enforcement`.)

      FINDING 4 — THE ENROLMENT ANSWER KEY. `ENROLLMENT_FIELDS` requires
      `credential_ref`; the declaration's `intake` returns the same fact as
      `reference`, under `kind: openprofiler_broker_intake`.

      FINDING 5 — `--retry-of` IS NOT PASSED. The declaration carries
      `mint --retry-of <opaud-…>` for precisely the 0.3 ruling, so a re-mint
      is correlated in the broker's audit trail instead of reading as an
      unrelated second issuance. This adapter never reads `audit_ref` — it is
      not in `MINT_FIELDS` — and has no placeholder able to carry one, since
      `ARGV_PLACEHOLDERS` is closed to the binding's own fields. The DASHBOARD
      half of the ruling is discharged and asserted (see 2.4); the BROKER half
      of the correlation is not, and cannot be until the binding can express a
      retry argv.

      FINDING 6 — A BROKEN PIPE READS AS "COULD NOT BE STARTED". The
      declaration obliges a consumer to treat `EPIPE` on the stdin write as
      "read the refusal", because some invocations are refused before standard
      input is read at all. `subprocess_broker_runner` catches `OSError`
      around that write and raises `DIAG_BROKER_UNREACHABLE`, so an honest
      refusal reads as an unstartable broker. Nothing leaks either way — both
      are fixed redacted sentences — but the distinction the declaration asks
      for is lost.

      NONE OF THE SIX IS FIXED HERE, and with the declaration now merged that
      needs a better reason than the one that held while it was in flight.
      The reason is scope: closing them is a code change to the binding's
      SHAPE (a per-operation argv map, an endpoint and a dialect the binding
      declares rather than the mint answer, a placeholder able to carry a
      previous `audit_ref`) and to the adapter's PARSING of a document it does
      not own. That is a second slice, not a correction to this one — and it
      would land unreviewed on top of a build already carrying a boundary
      change that deserves its own read. So it is stated rather than done, and
      A RECONCILIATION SLICE IS OWED before any operator can declare a binding
      that names `openprofiler-broker`. Until it lands, this seam mints
      against the contract it declares in `doxbench_provider` and against no
      broker that exists — which is why every one of its tests drives a broker
      child this repository writes.
- [x] 0.3 RULED 2026-08-26 (Brett, in-session): at mid-turn expiry the
      dashboard RE-MINTS AND RETRIES ONCE, with the re-mint and the paid
      retry VISIBLY RECORDED in the turn record; a SECOND expiry within the
      same turn surfaces the standard refusal. Silently retrying a paid call
      was the decision this question named, and the ruling answers it by
      making the retry visible rather than by forbidding it.

## 1. The binding (implementable now)

- [x] 1.1 A `model-provider-binding` record: id, label, credential
      reference, auth kind (`api_key` | `oauth`), broker invocation. No
      secret field exists in the shape — not optional, ABSENT, so no code
      path can populate one.
      BUILT 2026-08-26 as `scripts/ideation_dashboard/doxbench_binding.py`:
      a frozen, SLOTTED `ModelProviderBinding` whose five fields are exactly
      `BINDING_FIELDS`. The absence is enforced by the type rather than by a
      validator — an extra keyword is a `TypeError` at construction and an
      extra attribute is refused at assignment, both asserted. Stored as YAML
      carrying `schema_version: 1` + `kind: model-provider-bindings`, each
      entry stamped `kind: model-provider-binding`, at
      `ideation/dashboard/model-provider-bindings.yaml` under the checkout —
      beside the gate records, because the proposal says in as many words
      that a binding is safe to commit.
      NO FILE UNDER `contracts/` WAS ADDED, and that is a decision: a schema
      there is a RELEASE act with a manifest digest and a `contract-v*` tag,
      this change declares `target_release: none`, and the record has exactly
      one producer and one consumer inside this repository. Flagged for veto.
- [x] 1.2 Settings surface: list, add, edit, remove bindings. Read-back
      discloses the binding and states plainly that the credential lives in
      the broker.
      BUILT 2026-08-26 as `BindingStore` (list/get/add/edit/remove/read_back)
      plus the `ideation-dashboard model-binding` CLI verb group. Read-back is
      the binding's own fields plus the fixed `CUSTODY_NOTICE`, which names
      the broker as custodian in words rather than leaving the absence to be
      inferred from a missing key; `REMOVAL_NOTICE` states that retiring a
      binding revokes nothing.
      THE OPERATOR DOOR IS A CLI VERB AND NOT A BROWSER PANE, and that is a
      stated limitation rather than the whole of the task. Two reasons: every
      other install-time declaration this console makes (notebook adapter,
      retrieval backend, model session root) is made at the entrypoint in
      exactly this idiom, and a credential typed at a terminal crosses no HTTP
      wire at all, so "no credential reaches the browser" is structural rather
      than something a form has to be careful about. A BROWSER settings pane
      for bindings IS NOT BUILT in this slice and is owed; the dashboard's
      only settings surface today is `web/views/settings.js`, a localStorage
      viewer-preference popover that holds no governance state and would have
      had to grow a server round trip to carry one.
      TICK AUDIT 2026-08-26: the verbs were covered only at the STORE, which
      would have passed just as well had `model-binding` been wired to
      nothing. `test_the_cli_verbs_list_add_edit_and_remove_a_binding` now
      drives all four through the real parser, so registration, the custody
      sentence and the removal notice are asserted on the surface an operator
      actually touches.
- [x] 1.3 A credential hand-off that retains nothing: value to the broker's
      stdin, reference back, and a test that greps the whole checkout and
      every response for the value afterwards.
      BUILT 2026-08-26 as `doxbench_provider.hand_off_credential(binding,
      source)`. `source` is an OPEN HANDLE and never a string — the signature
      is the enforcement, since a caller cannot pass a value it must
      therefore be holding — and the credential is STREAMED handle-to-pipe
      with `shutil.copyfileobj`, so it never becomes a whole string in this
      process. The sweep is
      `test_the_credential_survives_nowhere_in_the_checkout_or_the_surface`:
      it drives the real CLI verb against a real broker child, then greps
      every file under the checkout and every string the read-back produces.

## 2. Minting and the narrowed boundary

- [x] 2.1 A minting seam that shells out to the declared invocation and
      returns `(token, expires_at)` — memory only, never written, never
      logged, never in a response.
      BUILT 2026-08-26 as `doxbench_provider.mint`. The argv is the BINDING's
      substituted template and no command line appears in code. The stdin
      contract is one JSON request line (`model-provider-broker-request`,
      naming the operation, the binding and the REFERENCE — never a secret);
      the stdout contract is one JSON document whose required keys are
      `MINT_FIELDS`. `MintedToken` carries a REDACTING `__repr__`, so a
      traceback, a debugger and a formatted log line all disclose the same
      nothing.
      THE MINT ANSWER CARRIES `endpoint` AND `dialect` BESIDE `token` AND
      `expires_at`, and that is this session's decision pending task 0.2,
      FLAGGED FOR VETO. Reasoning: a token that did not say where it is good
      is unusable, and the broker is the only party that knows which provider
      the credential it holds belongs to. `dialect` is a CLOSED vocabulary of
      one member (this repository's own already-declared prompt-in /
      `assistant_prose`-out shape) so an UNKNOWN dialect REFUSES rather than
      being guessed at — sending an assembled prompt to an endpoint whose
      grammar this client does not know is a paid call that cannot succeed.
      When openProfiler declares a provider-native dialect, a second member
      joins the vocabulary and an arm joins beside the first; the check is
      never loosened.
      ANSWERED, AND NOT AS THIS SESSION GUESSED: openProfiler's landed
      declaration carries neither field — see 0.2 FINDING 3. The veto flag
      stands, and the reconciliation is 0.2's rather than this task's.
- [x] 2.2 ONE provider-client module behind it. Every other module stays
      free of provider endpoints, SDKs and tokens.
      BUILT 2026-08-26 as `scripts/ideation_dashboard/doxbench_provider.py`,
      which declares its own name in `PROVIDER_CLIENT_MODULE` so the module
      and the boundary test cannot drift into naming two different files.
- [x] 2.3 REWRITE the structural provider check to enforce the narrower
      boundary rather than deleting it: today it asserts no provider is
      contacted from anywhere; it becomes "from nowhere except this one
      module", and the views clause stays absolute.
      DONE 2026-08-26 — and the honest form of "rewrite" here is CONSOLIDATE
      AND NARROW, which is worth stating precisely. There was no single test
      carrying the old claim: it was carried by ELEVEN per-module source
      scans (`test_doxbench_model.py`, `test_doxbench_turns.py`,
      `test_doxbench_packet.py`, `test_doxbench_knowledge.py`,
      `test_doxbench_threads.py`, `test_doxbench_memory_gateway.py`,
      `test_doxbench_bridge.py`, and the three browser-side scans), each
      naming ONE file — so a new module under `scripts/ideation_dashboard/`
      inherited no check at all, which is exactly the gap a change
      introducing a provider client must close. Every one of those scans is
      UNTOUCHED and still passes, and the new
      `tests/ideation-dashboard/test_provider_boundary.py` pins their
      continued existence by name so the narrowing cannot be achieved by
      deleting the guard it narrows. The new file sweeps the WHOLE package in
      two tiers: the PROVIDER tier (SDKs, provider hosts and paths, this
      repository's own minted-token type) is exempt for one module only; the
      generic HTTP-client tier (`urllib.request`, `Authorization`, `Bearer `)
      has a second NAMED holder, `snapshot_registry.py`, whose bearer is the
      SNAPSHOT DATA SOURCE's and comes from an operator-named environment
      variable — and that exemption is fenced by a positive assertion that
      `snapshot_registry.py` holds nothing from the provider tier. The views
      clause is ABSOLUTE: no browser module is exempt from anything.
- [x] 2.4 Expiry handling per 0.3, and discard-on-expiry regardless.
      BUILT 2026-08-26 in `BrokeredProviderPort.dispatch`. Discard-on-expiry
      is unconditional and separate from the retry: a token past the broker's
      declared `expires_at` is dropped and re-minted before it is ever
      presented. The RULING's case is the race — a provider answering 401 to
      a token that was live when the turn began — and it re-mints, retries
      ONCE, appends `remint_after_expiry` and `paid_retry` to the port's
      content-free `ledger`, and prints the fixed `REMINT_NOTICE`. A second
      expiry inside one turn raises `DIAG_TOKEN_EXPIRED_TWICE`; no third
      paid call is bought. The retry budget is per TURN, asserted.
      WHERE "VISIBLY RECORDED" LANDS, stated rather than implied: in the
      port's `ledger` and on the console's stderr, NOT in the browser's turn
      record. The released `workbench-chat-turn-success` envelope has no field
      for it and inventing one would be a contract release this change does
      not carry. Surfacing the re-mint in the BROWSER is owed and is not done
      here.
      THE BROKER-SIDE CORRELATION IS NOT DONE EITHER. openProfiler's
      declaration carries `mint --retry-of <audit_ref>` for exactly this
      ruling, and this seam passes nothing — see 0.2 FINDING 5. What is
      asserted here is the dashboard half of the ruling, in full.
- [x] 2.5 Wire `serve.py`'s `model_port_factory`; unconfigured stays exactly
      the posture it is now.
      DONE 2026-08-26. Both entrypoints — `serve.serve()` and
      `cli.cmd_generate_and_open` — now declare
      `doxbench_install.declared_model_port_factory`, which reads the
      checkout's bindings and resolves the brokered port when one is declared
      and the SAME harness factory they have always resolved when none is. A
      bindings document that will not read falls back to the harness
      declaration and says so on stderr, because one bad line in a settings
      file must not take the console down and must not silently serve a
      different provider than the one declared.
      THE FIRST DECLARED BINDING IS THE ONE SERVED. The seam takes ONE port,
      so an install talks to one provider at a time; choosing among several
      declared bindings needs a selection rule this change does not have and
      must not invent. Stated, not hidden.

## 3. Verification

- [x] 3.1 No minted token reaches the browser, appears in a log, or lands in
      the checkout — asserted, not assumed.
      DONE 2026-08-26: `test_the_token_never_reaches_a_response_a_log_or_the_disk`
      sweeps the response, the port's repr, every notice line and every file
      in the tree for a token sentinel; the browser half is the ABSOLUTE views
      clause in `test_provider_boundary.py`; and the credential sweep is 1.3's.
- [x] 3.2 Every broker and provider failure maps onto the fixed redacted
      refusal, and a missing capability is distinguishable from a failed
      call.
      DONE 2026-08-26. `BrokerRefused` REFUSES to be constructed with anything
      outside `FIXED_DIAGNOSTICS`, so a sentence cannot be composed from what
      a broker or a provider said; the broker's stderr and the provider's
      error body are dropped unread. Six broker/provider failure modes are
      exercised, and `dispatch_turn` maps the raised refusal onto its own
      `model_failed` — a different code from `model_capability_unavailable`,
      which is what keeps "it broke" distinguishable from "nothing is
      configured". A failure is never an empty result: a broker that has
      refused marks the catalog entry unavailable rather than dropping it.
- [x] 3.3 The unconfigured posture is byte-for-byte what it is today.
      DONE 2026-08-26, asserted three ways: a checkout with no bindings
      resolves the SAME `OmpHarnessBridge` construction the entrypoints always
      made; a plane with no factory at all still refuses with the same code,
      the same 403 and the same fixed sentence, pinned at the JSON bytes; and
      the pre-existing route-level tests
      (`test_absent_model_port_refuses_model_capability_unavailable` and the
      catalog route's plane-gate refusals) are untouched and still pass.
