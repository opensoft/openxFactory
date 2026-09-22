# Tasks: add-neutral-product-standalone-operability

Status: draft

Dependency-ordered. **Group 1 is the authoring THIS change performs and it
touches no code.** Groups 2-15 are the post-ratification realization, each in the
repository named in its heading and each carrying the FALSIFICATION COMMAND that
closes it — an exact invocation with its checkout preconditions and its expected
result, so the archive gate's evidence under `release-realization` is a command
re-run and quoted rather than a description believed.

**Groups 2-12 and 15 take one requirement each; TWO groups take more than one,**
because their requirements are satisfied by one act and splitting them would
produce boxes that cannot be closed independently: **Group 13** takes
requirements 12 and 13 (the install brings its datastore AND its identity mode —
one install story), and **Group 14** takes requirements 6, 14 and 15 (the store
that holds a finding, the loop that fixes it, and the exception that suppresses
it — one schema and one loop). Requirement 6 is therefore reached TWICE, by
Group 6 for the check itself and by Group 14 for where its results live, which is
the amendment the ruling of 2026-09-22 made to it. The requirement-to-group map is
the group headings, read as written; nothing below claims a bijection.

**Two classes of verb appear in the commands, and the difference matters.** Groups
2-13 name only verbs `src/opendox/cli.py` ALREADY DECLARES — the arc packages and
unblocks that surface, it does not invent one — and task 10.1 carries the verb
table those commands are written against. Groups 14 and 15 name the `health`
verbs this arc CREATES (task 14.6 declares them); their falsifications are
therefore acceptance tests for surface the realization must add, not re-runs of
surface that exists, and no box in 14 or 15 may be closed by a command whose verb
its own group did not first declare.

**Fixture corpora are DIRECTORIES in the code leg's checkout, never
repositories**, and none exists today — `git ls-tree` over openDox-code's
`tests/fixtures/` at `3c3a9e31` lists four files, none of them a corpus. Each is
shipped by the first group that needs it (5.0, 7.0, 14.9, 15.6a). **Every
falsification that needs a repository COPIES its fixture into a fresh `git init`
first**, so no command below can create a branch or a commit inside the checkout
it is testing, and a git adapter pointed at a fixture reads that fixture rather
than the enclosing repository. Each block carries its own three setup lines and
its own commit identity, so every group runs from a fresh shell on its own.

House rule: OpenSpec ratifies, Speckit builds. No group below is started before
ratification, no group is started without its own claim on
`opensoft/openxFactory#656` per lane-collision-protocol Rule 1, and this change
merges nothing anywhere.

Baselines, measured on `openxFactory` `main` `4f92d651` before this packet:
`OPENSPEC_TELEMETRY=0 openspec validate --all --strict` -> `Totals: 109 passed,
1 failed (110 items)`; `python3 scripts/validate-openspec-cli-pin.py --all
--no-cache` -> exit 0, `0 UNDISPOSITIONED failures`, 1 accepted exception
(`add-chain-attestation`, ratified disposition). This packet must add +1 item,
+1 passed and ZERO new failures.

## Group 1 — Authoring (THIS change; no code byte)

- [x] 1.1 Author `.openspec.yaml` — ad-hoc origin, the drafting-provenance shape
  with NO approval pair (`add-drafted-proposal-origin`), naming the archived
  packet's unclosed residue as the origin.
- [x] 1.2 Author `proposal.md`: the owner's goal in his own words from `#656`;
  the two-products measurement; the repository-choice FINDING; the G-to-
  requirement table; the explicit "what openxFactory keeps" section; honest
  `code_surface:` / `target_release:` front-matter.
- [x] 1.3 Author the `## ADDED Requirements` delta creating
  `neutral-product-standalone-operability` — 16 requirements, 67 scenarios,
  domain-neutral, openDox as the measured instance.
- [x] 1.4 Author `design.md`: D1-D8 and **R-G3** — filed as Q-G3, the one question
  put to Brett with three options and a recommendation; RULED the same day and
  rewritten as the record of the decision, the options as they were put, and the
  CORRECTION to this packet's own pricing of the rejected option.
- [x] 1.5 `OPENSPEC_TELEMETRY=0 openspec validate add-neutral-product-standalone-operability --strict`
  and `--all --strict` pass with no NEW failure against the baseline above.
- [x] 1.6 `python3 scripts/proposal-support.py . verify add-neutral-product-standalone-operability`
  passes; the `tests/sequenced_after/corpus-ledger.yaml` row is machine-seeded
  (`scripts/validate-sequenced-after.py --seed-ledger --moved-by … --moved-on …`),
  and the README "OpenSpec Records" *Active changes* bullet is added.
- [x] 1.7 **RULING G3 — GIVEN.** Brett Heap, `#656` comment `5783335210`,
  2026-09-22T20:08:59Z: *"yes, openDox gets its own neutral generator."* Group 5
  is no longer blocked and requirement 4 is written to the ruling. `design.md`
  § R-G3 records the options as they were put, what was ruled, and the CORRECTION
  to this packet's own pricing of option (a) — `generator.py:66-68` imports
  `doc_health`, which this packet had not measured when it recommended (c).
- [ ] 1.8 On ratification: `Status: ratified` + `Ratified by:` on all three
  lifecycle documents; `## Ratification record` in `proposal.md`; the approval
  pair ADDED beside the fixed origin in `.openspec.yaml`, never substituted.

## Group 2 — Requirement 2 / G1: imports with no consumer, publisher or host (openDox-code)

The highest-leverage box: TWO import statements, 1,232 of 1,298 measured errors
at `f8a1ece`, zero passed. An AST census of `src/` finds exactly two import-time
reaches (`serve.py:199`, `serve.py:206`) and two deferred ones; every other
mention in the package is prose.

- [ ] 2.1 Remove the module-level `from ideation_dashboard import
  serve_openxfactory_lanes` (`src/opendox/serve.py:199`) and the
  `from ideation_dashboard.serve_openxfactory_lanes import (…)` re-export block
  (`:206`). The five names (`ACTIONS_APPLY_REGISTER_EDITS_ROUTE`,
  `ACTIONS_DTN_SEED_ROUTE`, `ACTIONS_REFRESH_ROUTE`,
  `ACTIONS_STAGING_SEED_ROUTE`, `COMMITTED_INTENTS_ROUTE`) belong to
  openxFactory's lanes surface, filed `stays_openxfactory_adapter`. All five are
  plain route strings (`"/committed-intents.json"`, `"/actions/refresh"`,
  `"/actions/apply-register-edits"`, `"/actions/dtn-seed"`,
  `"/actions/staging-seed"`).
- [ ] 2.1a **DO NOT VENDOR the module.**
  `scripts/ideation_dashboard/serve_openxfactory_lanes.py` itself imports
  `from openxdox import snapshot_registry` (`:70`) and
  `from openxdox.serve_projection import hosted_ref_refused` (`:77`), so copying
  it into openDox re-creates the consumer dependency BUILD slice 2b removed.
- [ ] 2.2 Contribute those routes through the EXISTING seam —
  `serve.build_server(route_extensions=)` / `route_extension.RouteBinding` — from
  openxFactory's side, per the carve `design.md`'s own specification. No new
  mechanism is designed here.
- [ ] 2.3 Sweep every remaining module-level reach: grep `src/` for
  `ideation_dashboard`, `corpus_adapter_openxfactory`, `doc_health` and
  `openxdox` at import position, and close or defer each with a recorded reason.
- [ ] 2.4 Add a test in openDox-code's own suite that imports EVERY module of the
  package in a checkout with no sibling installed, failing with the name of the
  first module that still needs one.
- [ ] 2.5 Remove `validate.yml`'s three `--noconftest` steps and their enumerated
  file lists; the suite collects whole. Measured at `f8a1eced` by extracting the
  `run:` blocks that invoke pytest: **four blocks name 37 distinct test modules of
  the 63 in the tree** (`tests/` 53 + `tests_runtime/` 10), three of them under
  `--noconftest`; **26 modules are named by no pytest step at all**. This is the
  figure the whole packet uses — an earlier reading of "31 of 53" counted only the
  `--noconftest` blocks over `tests/`. The autouse fixture that produces
  the 1,298 setup errors is `tests/session_fixtures.py:413`, whose body is
  `from opendox import cli as cli_mod`.
- [ ] 2.6 Correct openDox-code's `README.md:39-42`, which still gives the
  narrowing's reason as *"Until the BUILD arc … inverts the openDox → openXdox
  dependency"*. That dependency IS inverted at import time; the live cause is
  `ideation_dashboard`.
- [ ] **FALSIFIED BY:** in a checkout of openDox-code alone,
  `python -c "import opendox.serve"`, `python -c "import opendox.cli"` and
  `python -c "import opendox.notebook_action"` each exit 0. Today all three raise
  `ModuleNotFoundError: No module named 'ideation_dashboard'`.

## Group 3 — Requirement 3 / G2: a default domain profile (openDox-code)

- [ ] 3.0 **RATIFICATION READ FIRST.** Requirement 3 revisits the PREMISE of RULED
  ASK-2 option (2) (`#656` comment `5628886636`) — not its reasoning. An EMPTY
  default stays refused; what changes is the refusal text's premise that *"openDox
  … ships no profile of its own"*. If the ratification read takes ASK-2 to
  foreclose this, requirement 3 is struck and the other **fifteen** stand. See
  `design.md` § D5.
- [ ] 3.1 Ship a default profile for openDox's OWN domain — documents and ideas —
  carrying none of openxFactory's status taxonomy or change/spec/delta nouns
  (RULING C2, DIRECTION Q5). Note the standalone problem this closes: the only
  host that exists, openxFactory's `scripts/opendox_host.py`, builds a composite
  whose base class is `openxdox.domain_profile.DomainProfile`, so today's only
  real profile needs BOTH siblings present.
- [ ] 3.2 `build_parser()` and `build_server()` fall back to it when no host has
  called `domain_profile.register()`, and a registered profile still replaces it.
  `profile_proxy.py`'s refusal is kept for the case it was written for — an
  ambiguous registration — and is NOT weakened into an empty tuple.
- [ ] 3.3 Record in the carve manifest that the `deleted_at_carve` row for
  `profile_openxfactory.py` is UNCHANGED by this: openxFactory's profile stays
  deleted from the core and `scripts/opendox_host.py` remains openxFactory's host.
- [ ] **FALSIFIED BY** (openDox-code checkout, `pip install -e .`, no sibling):

      python -c "from opendox.cli import build_parser; build_parser(); print('OK')"
      python -c "from opendox.serve import build_server; build_server(); print('OK')"

  Both print `OK`. Today both raise `domain_profile.ProfileNotRegistered`. Then
  `pytest tests/test_profile_registration.py` proves a registered profile still
  replaces the default.

## Group 4 — Requirement 5 / G4: the deferred reach resolves through the seam (openDox-code)

- [ ] 4.1 Replace `src/opendox/authoring.py:318`'s
  `from corpus_adapter_openxfactory import home_corpus` with a resolution of the
  REGISTERED corpus adapter through openDox's own `corpus_adapter` seam.
- [ ] 4.2 Where no adapter is registered, refuse naming the seam and the remedy —
  never a `ModuleNotFoundError` raised from inside a function.
- [ ] 4.3 Sweep the nineteen deferred reaches the ratchet declares today
  (`branch_session.py` 7, `serve_workbench.py` 7, `serve.py` 2,
  `serve_project.py` 2, `cli.py` 1) and classify each: resolvable through a
  declared seam, or genuinely owed to the consumer and therefore staying
  late-bound with its reason. The import-time column is already `0` — do not
  re-do it.
- [ ] **FALSIFIED BY** (openDox-code checkout, no sibling, no
  `corpus_adapter_openxfactory` importable):

      python -c "import opendox.authoring as a; a.required_header_fields()"

  Returns the fields through the registered adapter, or raises openDox's own named
  refusal. It MUST NOT raise `ModuleNotFoundError`. Today it raises
  `ModuleNotFoundError: No module named 'corpus_adapter_openxfactory'` while
  `python -c "import opendox.authoring"` exits 0.

## Group 5 — Requirement 4 / G3: openDox's own neutral projection (RULED, openDox-code)

**RULED: openDox gets its OWN neutral generator. `generator.py` does not move.**
The audit this box used to open with is spent — it would have priced a relocation
nobody is doing — and its decisive finding is recorded instead: `generator.py`
imports `doc_health` at `:66-68`, so relocating it was never lawful under
`corpus-adapter-seam` whatever its literals said.

- [ ] 5.0 **Ship `tests/fixtures/plain-documents`** — first needed here, and
  Groups 7 and 13 read it too: a handful of `.md` documents spread across the six
  neutral stages, carrying NONE of openxFactory's governance vocabulary (no
  `openspec`, no `proposal.md`, no `ratified`), which is what lets the assertion
  below mean something.
- [ ] 5.1 Write openDox's SMALL NEUTRAL PROJECTION over the `CorpusAdapter`
  protocol already declared at `src/opendox/corpus_adapter.py` (a
  `@runtime_checkable` `Protocol`, six closed members: `resolve`,
  `list_documents`, `read`, `classify`, `check`, `write_back`). New neutral code
  written to openDox's needs — NOT 3,164 lines re-expressed, and NOT a copy of
  openXdox's.
- [ ] 5.2 Bind `src/opendox/runtime/local_git_adapter.py` (2,796 lines, RULING
  C3's plain local git repository) as the conformant implementation, so the
  projection has a real corpus to read with nothing else installed.
- [ ] 5.3 Render `NEUTRAL_DISPLAY`'s SIX WORDS and no others — `sources`,
  `groups`, `candidates`, `selections`, `submissions`, `completed` (RULED
  *"keep those six words"*, same comment; the sixth is **`completed`** by RULING
  `5784654370`, *"2, keep completed"*, which corrected this packet's earlier
  `completions` — the DECLARED value in `display_profile.py`, not the docstring
  that narrated it). **No word is re-authored and no workflow is designed.**
  `src/opendox/display_profile.py` is unchanged by this group.
- [ ] 5.3a **openXdox declares the estate's FIRST `DISPLAY` facet — partial, one
  stage** (openXdox-code; RULED `5784683830`, *"1, keep completed and overlay
  implemented"*). On the profile openXdox contributes —
  `src/openxdox/domain_profile.py:317`'s `DomainProfile`, which openxFactory's
  `scripts/opendox_host.py` composite inherits — declare `DISPLAY` labelling the
  `completion` stage **"implemented"**, the governed lifecycle's own word, in its
  `short` AND its `label` field (measured: a facet giving `short` alone leaves
  `label` at `completed`), and NOTHING ELSE — openDox fills every other role and
  field from `NEUTRAL_DISPLAY`. The neutral word does not move. Claim it on
  `#656` before starting, like every group here.
- [ ] **FALSIFIED BY** (openXdox-code checkout with openDox installed):

      set -euo pipefail
      python3 - <<'PY'
      from opendox.display_profile import STAGE_ROLES, host_display, normalize_display
      from openxdox.domain_profile import DomainProfile
      facet = host_display(DomainProfile)                   # None today: no profile declares one
      assert facet is not None, "openXdox declares no DISPLAY facet"
      merged, neutral = normalize_display(facet), normalize_display(None)
      done = merged["stages"]["completion"]
      assert done["short"] == "implemented" and done["label"] == "implemented", done
      assert neutral["stages"]["completion"]["short"] == "completed"   # the neutral word stands
      for role in (r for r in STAGE_ROLES if r != "completion"):
          assert merged["stages"][role] == neutral["stages"][role], f"{role} was overlaid too"
      PY

  Three things, each an assertion: the governed host sees "implemented" wherever
  the stage is named; a host with no facet — and a standalone install — sees
  "completed"; and the facet is PARTIAL, the other five stages byte-identical to
  the neutral ones, so an overlay cannot quietly grow into a second vocabulary.
  The same calls were run against openDox-code `3c3a9e31` with a stand-in profile
  before this box was written, and behave as asserted.
- [ ] 5.4 **DECLARE THE GENERATOR SEAM — it does not exist and `CorpusAdapter` is
  not it.** `src/opendox/corpus_adapter.py`'s Protocol is CLOSED at six members
  (`resolve`, `list_documents`, `read`, `classify`, `check`, `write_back`) and its
  own docstring says *"Six methods. Nothing else, ever"* — none of them is a
  generator handoff, so "contribute it through the same seam" would name nothing
  and let two incompatible implementations both claim conformance. This box
  declares the seam: the operation handed over, the registration point (beside
  `domain_profile.register()`, which is the shape the product already uses), and
  the conformance a contributed generator must satisfy. `consumer_reach.py` says
  the corresponding injection *"does not exist yet and is BUILD-arc work"* — this
  is that work.
- [ ] 5.4a openXdox KEEPS `generator.py`, `snapshot.py`, `snapshot_registry.py`,
  `completeness.py` and `corpus_root.py`, and contributes its governed generator
  through the seam 5.4 declares. The publisher's corpus is projected exactly as
  today and the consumer loses no capability — requirement 4's third scenario is
  the check.
- [ ] 5.5 Lower `consumer_reach.py`'s generator-facing deferred reaches as the
  projection replaces them; the import-time column stays at zero.
- [x] 5.6 **Do NOT author the view-wiring slice here** — and it can no longer be
  duplicated: it was CLAIMED on openDox-code under actor `viewwire` (RULED *"wire
  the views and land it"*, same comment) and LANDED as **openDox-code#35 →
  `3c3a9e31`** (2026-09-22T21:39:18Z), converting the hardcoded
  `stage-brainstorm` / `stage-staged` / `stage-realized` spellings in
  `src/opendox/web/views/` to role lookups and joining `lens.js` to the display
  facet. Ticked on that landing, which is the evidence; nothing in this arc
  re-does it. The ruling is explicit that the generator is not in that claim.
- [ ] **FALSIFIED BY** (openDox-code checkout, `pip uninstall -y openxdox` so that
  `python -c "import openxdox"` raises, AND `python -c "import doc_health"` raises
  too — the neutral projection must reach neither the consumer nor the publisher
  — over a fixture directory of plain `.md` documents carrying none of
  openxFactory's governance vocabulary):

      set -euo pipefail
      # NOT the console script: 10.1 packages that later, and this list is
      # dependency-ordered. At group 5's boundary the module is importable
      # (group 2) and that is what this falsifier uses.
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      R=$(mktemp -d)/plain-documents && cp -r tests/fixtures/plain-documents "$R"   # 5.0's fixture, as a FRESH repository
      git -C "$R" init -q && git -C "$R" add -A && git -C "$R" commit -qm fixture
      python -m opendox.cli --repo-root "$R" generate --output /tmp/snap.json
      python -c "
      import json,sys
      d=json.load(open('/tmp/snap.json'))
      assert d['documents'], 'snapshot is empty'
      blob=json.dumps(d).lower()
      assert not any(w in blob for w in ('openspec','proposal.md','ratified')), 'publisher noun leaked'
      print('documents:', len(d['documents']))"

  Under `set -euo pipefail` the sequence exits non-zero on any step; the
  assertions are IN the command rather than in prose, so the check is
  machine-detectable. (`python -m opendox.cli` requires `cli.py` to expose a
  `__main__` entry or the box uses `python -c "from opendox.cli import main; main([...])"` —
  10.1 later packages the same callable as the console script.)

## Group 6 — Requirement 6 / G5: a health check over openDox's own documents (openDox-code)

- [ ] 6.1 **Expect to find almost nothing generic, and plan for that.** A strict
  measurement — comments and docstrings stripped, so only executable code counts
  — finds exactly ONE of `scripts/doc_health/`'s 37 Python modules free of
  openxFactory/OpenSpec identifiers: `lines.py`, 133 lines of 31,437 (0.4%).
  About 13 modules mix a reusable mechanism with hard-coded corpus identifiers
  (`corpus.py:39,59,92-93`; `inventory.py:37,52`; `preflight.py:20-25,180-185`),
  and about 23 are corpus operations by subject. **There is no extractable
  generic doc-health core**, so requirement 6 is satisfied by openDox growing its
  own check over its own declaration — not by relocating families.
- [ ] 6.1a Where a module genuinely mixes both, relocate the generic part into a
  module both sides depend on BEFORE either side moves — `corpus-adapter-seam`'s
  relocation rule applied inside a module.
- [ ] 6.2 openDox carries a health check over its own documents, reading its own
  declaration. **No openxFactory check family moves** (requirement 1). The seam
  already exists and is DEAD: `src/opendox/workbench.py:1389`'s
  `run_scoped_doc_health` (families `status-validity`, `tag-hygiene`) catches the
  `ImportError` and records `status = not-available`,
  `detail = doc-health machinery unavailable: No module named 'doc_health'`. Give
  it something to call.
- [ ] **FALSIFIED BY** (openDox-code checkout, no sibling):

      set -euo pipefail
      python3 - <<'PY'
      from opendox import workbench
      r = workbench.run_scoped_doc_health(".", ["README.md"])
      assert isinstance(r, workbench.ActionResult), type(r)
      assert r.status == "completed", f"the check did not run: status={r.status!r} detail={r.detail!r}"
      assert isinstance(r.findings, list) and r.reference, f"no result shape: {r!r}"
      PY

  The call returns an `ActionResult` DATACLASS (`workbench.py:1339`) whose
  `status` is one of `completed | not-available | skipped`, so the assertion is on
  the one value that means the check RAN — not merely on the call returning. The
  earlier form of this command printed the status and exited 0 whatever it was,
  and it subscripted the result (`['status']`), which a dataclass refuses with a
  `TypeError`: it could neither fail for the right reason nor pass. Today the
  assertion fails on `status='not-available'`, with
  `detail = doc-health machinery unavailable: No module named 'doc_health'`.

## Group 7 — Requirement 7 / G6: a validator openDox can run (openDox-code)

- [ ] 7.0 **Ship `tests/fixtures/malformed`**: 5.0's `plain-documents` with
  EXACTLY ONE rule violation the validator must name — so the falsification below
  can tell "refused for that rule" from "refused for anything".
- [ ] 7.1 **NARROW THE INPUT SET FIRST, then acquire what remains.** The existing
  validator's `SCHEMA_FILENAMES` names **ten** schemas and they have three
  different owners, so "give openDox the whole set" is the wrong shape:

  | owner | count | schemas |
  |---|---|---|
  | `opensoft/openDox-spec` | 3 | `ideation-workbench`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` |
  | `opensoft/openXdox-spec` | 3 | `ideation-dashboard-snapshot`, `ideation-dashboard-snapshot-index`, `gate-action-record` |
  | `openxFactory` | 4 | `ideation-possibles-register`, `project-register`, `demotion-execution-receipt`, `gate-intent` |

  Ownership is settled, not inferred: `docs/contract-versioning-policy.md`
  § 1047-1053 records openxFactory DIVESTING the first six to the two spec legs
  by canonical home, leg commit and unchanged `sha256`. Both code legs and both
  assembly roots carry **zero** schema files.

  **The default direction, and the one this task recommends:** openDox's
  validator validates openDox's OWN document kinds — its spec leg's **three** —
  which are openDox's own spec leg's. **How they reach the code leg is the part
  requirement 7 constrains and this box must settle, because the two obvious
  answers contradict each other.** `AGENTS-shape.md` puts a contract the code
  READS but does not OWN in the SPEC leg, reached from the assembly root with
  `CONTRACTS_DIR` — but `docs/project-repo-schema.md:54-58` puts the assembly and
  the code leg in DIFFERENT repositories, so an assembly-root read cannot satisfy
  requirement 7's one-checkout rule in a code-leg-only checkout. **The resolution
  this box takes: the INSTALLED product is the checkout requirement 7 means.** The
  three schemas ship as PACKAGE DATA of the openDox distribution, so
  `pip install openDox-code` puts them on disk beside the validator and the
  assembly root remains their source of truth for editing. The falsifications
  below therefore run against an INSTALLED product, not a bare clone. If that
  packaging is refused, the alternative is to run the validator from the assembly
  root and amend requirement 7's scenario to say so — recorded here so the choice
  is visible rather than discovered at implementation. The
  openXdox-spec three belong to the CONSUMER's validator and openDox never needs
  them. Only if a measured openDox verb genuinely needs one of openxFactory's
  four does it arrive as the DIGEST-PINNED VENDORED COPY `neutral-product-pin`
  admits — a CONSUMED manifest member, and note that capability admits **ONE**,
  so needing more than one is itself a finding to raise rather than a thing to do.
- [ ] 7.1b **AND TWO OF THOSE FOUR ARE NOT AVAILABLE BY THAT ROUTE AT ALL.**
  `gate-intent.schema.yaml` is an INTENT-PLANE schema — the carve manifest lists
  it among the validator's contract files (`docs/opendox-carve-manifest.yaml:459`)
  and requirement 1 keeps the intent-plane schemas with openxFactory. Vendoring
  it would satisfy requirement 7 by breaching requirement 1, which requirement 7's
  fifth scenario now refuses in terms. The same reasoning covers
  `ideation-possibles-register.schema.yaml`, filed
  `stays_openxfactory_adapter` as openxFactory's own candidate register. **If the
  narrowing in 7.1 is done properly, openDox needs neither**; if an openDox verb
  appears to need one, raise it as a finding about the boundary rather than
  copying the schema.
- [ ] 7.1a Record why the existing script cannot simply be reused: it derives
  `SCHEMAS_DIR` from `__file__` (`validate-ideation-dashboard-contracts.py:114-115`)
  and so looks for a `contracts/schemas/` its own leg does not have — run from
  openXdox-code it exits 2 with `ERROR .../contracts/schemas not found`. That is
  the G6 defect in one line, and it is the consumer's to fix for its own set.
- [ ] 7.2 openDox-code has **no `scripts/` directory at all** and one console
  script. Whatever validator it gains is new surface at the code leg, not a
  relocated one.
- [ ] 7.3 **Three carve-broken defects in `openxdox/snapshot.py` are unclaimed
  and belong to this box**, registered by the archived packet's § 5.5 residue and
  owed to *"a follow-up act with its own claim"* that nobody holds: `SCHEMAS_DIR`
  resolves to an absent directory; `VALIDATOR_RELPATH` names a path openxFactory
  shed; and **`find_validator`'s parent walk ADOPTS AN ENCLOSING PRE-SHED
  CHECKOUT** — which is exactly the "reaching into a host tree instead of an
  injected adapter" class this arc exists to close, appearing a second time.
  Claim them here or hand them on by name; do not leave them unowned again.
- [ ] **FALSIFIED BY** (openDox-code checkout, no sibling, **INSTALLED into a
  fresh venv**, because 7.1 settles that the three schemas travel as PACKAGE
  DATA and a bare clone therefore cannot exercise the packaged set this box is
  about). Validation is the
  POST-RENDER step inside the generate verbs — there is no `validate` verb and
  this packet adds none — so it is exercised through `--strict`, which also makes
  a validator that could not RUN fatal instead of a warning:

      set -euo pipefail
      python -m venv /tmp/v7 && . /tmp/v7/bin/activate && pip install .   # PACKAGE DATA on disk (7.1)
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      OK=$(mktemp -d)/plain-documents && cp -r tests/fixtures/plain-documents "$OK"
      git -C "$OK" init -q && git -C "$OK" add -A && git -C "$OK" commit -qm fixture
      BAD=$(mktemp -d)/malformed && cp -r tests/fixtures/malformed "$BAD"
      git -C "$BAD" init -q && git -C "$BAD" add -A && git -C "$BAD" commit -qm fixture
      python -m opendox.cli --repo-root "$OK" --strict generate --output /tmp/ok.json
      if python -m opendox.cli --repo-root "$BAD" --strict generate --output /tmp/bad.json 2>/tmp/err; then
        echo "FAIL: a malformed corpus validated"; exit 1
      fi
      ! grep -q "No such file or directory" /tmp/err  # the refusal must name a RULE, not a missing path

  The first exits 0; the second exits NON-ZERO and the sequence asserts that
  rather than printing it, so a validator returning zero on a malformed corpus
  fails the check. The last line is a NEGATIVE `grep` — `! grep -q` — not
  `grep -qv`, which would have succeeded on any single non-matching line and so
  passed a mixed "missing schema AND rule error" stderr. **Neither may fail on an unresolvable schema path** — today
  that is exactly how it fails, because `--strict` makes "the validator is
  unreachable" fatal and the validator is unreachable.

## Group 8 — Requirement 8 / G7: openDox-spec governs openDox (openDox-spec) — BLOCKED

**These boxes carry the reserved `[~]` marker, not `[ ]`, and that is deliberate.**
They are NOT this packet's act — they are openDox-spec's, in a repository this
packet cannot write — so a literal unchecked box would make this packet
unarchivable for work it was never entitled to do. The marker is the corpus's own
(`split-opendox-two-layer-product` closed at 67 [x] / 0 [ ] / 5 [~]).
**Owner: whoever holds openDox-spec's instance.**
**Exit condition: requirement 8's third scenario — when openDox-spec has promoted
the requirements the carve's map assigns it, these boxes close there and this
packet's interim arrangement ends.**

- [~] 8.1 openDox-spec promotes the requirements the carve's ratified
  per-requirement map assigns to openDox (the map's split: **71 openDox / 16
  openXdox / 15 openxFactory**; the 16 were carried into openXdox by the carve's
  § 6.1 and § 6.5 closures, and the 15 were re-promoted here by
  `repromote-engineering-vocabulary` under RULING DQ-1 — only openDox's 71 have
  no home). Measured by normalized-title scan of every `spec.md` in openDox-spec:
  **68 of the 71 appear nowhere in the repository**, and the three that do appear
  only inside `## MODIFIED` blocks of draft changes.
- [~] 8.1a **Unblocks openDox-spec's own backlog, which is why this is not
  housekeeping.** Three of its four active changes carry `## MODIFIED` blocks
  against `ideation-dashboard`, a spec that does not exist there, so **they can
  never be archived** — the loop is open at both ends: nothing can be promoted
  because nothing has been archived, and nothing can be archived because nothing
  has been promoted. Promoting the 71 is what breaks it.
- [~] 8.1b **Raise openDox-spec's CLI pin while doing it.** Both spec legs pin
  `@fission-ai/openspec@1.2.0`; openxFactory pins 1.12.0 by content address. Run
  against the same tree, **1.2.0 emits none of the three "Archive would refuse
  this delta" notices** that 1.12.0/1.13.x report. openDox-spec's gate cannot see
  the defect in 8.1a.
- [~] 8.2 On that landing, requirement 8's third scenario fires and work scoped to
  openDox is authored in openDox-spec. This packet's interim arrangement ends.
- [~] **FALSIFIED BY** (openDox-spec checkout):

      OPENSPEC_TELEMETRY=0 openspec list --specs
      OPENSPEC_TELEMETRY=0 openspec validate --all --strict

  The first lists the promoted capabilities; the second passes with no "Archive
  would refuse this delta" notice under a CLI at or above the openxFactory pin.
  Today the first answers `No specs found.`, and three of four changes carry the
  notice under 1.12.0 while their own gate at 1.2.0 cannot see it.

## Group 9 — Requirement 9 / G8: each leg's suite green alone (both legs)

- [ ] 9.1 openDox-code's required check runs the whole suite, no `--noconftest`,
  no file list (follows group 2).
- [ ] 9.2 openXdox-code the same, with `OPENDOX_BACK_IMPORTS` lowered as each
  deferred reach closes. The import-time column is ALREADY zero and stays there.
- [ ] 9.2a **Add the missing instrument.** No gate watches the openDox →
  openxFactory direction — the ratchet measures openDox → openXdox only, which is
  how two import-time reaches into the publisher survived a completed inversion
  under a green check. Requirement 2's third scenario is that instrument.
- [ ] 9.3 Behaviours needing both legs become declared INTEGRATION tests naming
  the pin they compose at, rather than being dropped from both suites — including
  the 31-entry assembled `--help` tree the carve manifest records as one
  *"which after the carve neither leg produces alone"*
  (`docs/opendox-carve-manifest.yaml:3088`). Nothing anywhere reproduces it today.
- [ ] 9.4 **Restore the margin, and stop the skips carrying the gap.** Both legs
  pass their floors with ZERO margin (openDox `1114/1111/3`, openXdox
  `539/533/6`), and every one of openXdox's six skips carries the same reason —
  *"doc_health reachability is BUILD-arc work (§ 3.5/3.6) … this test will assert
  for real once that lands"*. Two of openDox's three are the mirror image. **The
  whole-product assertions are precisely the ones that skip**, which is why both
  legs report green while neither product runs.
- [ ] 9.5 Note for whoever takes this box: openXdox pins openDox at `5c137a90`,
  nine commits behind openDox-code `main`, and the openDox root's gitlink and
  `contracts/code-pin.yaml` name `d816cf06`, two behind. Both are ancestors —
  nothing is forked — but the pins move before the integration run means
  anything.
- [ ] **FALSIFIED BY** (each leg's own checkout, no sibling installed):

      set -euo pipefail
      python -m pytest -q                                   # NOT --noconftest, NOT a file list
      test "$(grep -c -- --noconftest .github/workflows/validate.yml)" -eq 0
      # AND no pytest step enumerates a subset: a named file list with no
      # --noconftest would otherwise pass the assertion above.
      python - <<'EOF'
      import re, sys, pathlib
      w = pathlib.Path(".github/workflows/validate.yml").read_text()
      body = "\n".join(l.split("#")[0] for l in w.split("\n"))
      named = set(re.findall(r'tests(?:_runtime)?/test_[A-Za-z0-9_]+\.py', body))
      sys.exit(0 if not named else (print("FAIL: workflow still enumerates", len(named), "test files"), 1)[1])
      EOF

  All three statements must succeed: `set -e` propagates a failing suite (a passing
  `grep` after a failing `pytest` must not make the sequence exit zero), and the
  `test` asserts the exclusion count is ZERO rather than leaving it to a reader.
  Today openDox-code gives 1,298 errors / 0 passed and openXdox-code 1,089 / 0.

## Group 10 — Requirement 10 / G9, G10: one entry point (openDox-code + openDox root)

- [ ] 10.1 A `[project.scripts]` entry point for the DOCUMENT surface. **The verbs
  are NOT invented here — `src/opendox/cli.py` already declares them** and group 2
  is what makes them reachable; the entry point is the missing packaging line:

      opendox = "opendox.cli:main"

  and the surface it exposes is the one already in the tree, named here so every
  falsification below is executable rather than a placeholder:

  | verb | shape, as `cli.py` declares it today |
  |---|---|
  | `generate` | `--repo-root <corpus> generate --output <path>` (`:880-881`) |
  | `generate-and-open` | `--repo-root <corpus> generate-and-open [--run-dir P] [--host H] [--port N] [--no-open] [--no-serve]` (`:885-`) |
  | `create`, `edit` | scaffold a header-compliant doc; select-to-edit (`:911`, `:927`) |
  | shared | `--repo-root`, `--strict`, `--no-validate`, `--project`, `--possibles` (`:840-849`) |

  **There is no `serve` verb and no `validate` verb**, and this packet does not
  add either: serving is `generate-and-open`, and validation is a POST-RENDER
  step inside the generate verbs, hardened by `--strict` and skipped by
  `--no-validate`. Today the only console script is
  `opendox-runtime = "opendox.runtime.cli:main"` — a subsystem, not the product —
  and there is no `__main__.py` anywhere under `src/`. **RULED Q-R4 already places this work in THIS act** (`#656` comment
  `5701772032`, Brett Heap, 2026-09-16, recorded at `runtime/cli.py:40-46`): *"the
  verbs are wired into `opendox.cli` in the BUILD-arc act that repairs
  `opendox.serve`, and `opendox-runtime` is the spelling until then."* So 10.1
  follows group 2 and discharges Q-R4's condition.
- [ ] 10.2 The web bundle is served by that entry point and is reachable in a
  browser from an openDox-only install. openDox-code carries **42** web files,
  self-contained by declaration (`src/opendox/web/index.html`: *"All assets are
  local/vendored: no CDN, no external fonts, no remote scripts"*), and **nothing
  serves them**: `serve.py` will not import, and `runtime/app.py` mounts no
  `StaticFiles` — its routes are `/livez`, `/readyz` and `/api/v1`. The bundle is
  not the gap; the door is.
- [ ] 10.2a `intent-feed.js` stays at openxFactory under RULED OQ-F and is NOT
  owed to openDox; openDox's replacement is `views/intent-binding.js`. Do not
  count it as a missing file.
- [ ] 10.3 **The assembly root DOCUMENTS the entry point; it does not host it.**
  `openDox/Makefile` carries a row in `contracts/shape-pin.yaml` (`:49-50`), and
  `AGENTS-shape.md` § "Never edit a file that has a row" is explicit: *"An edit
  in place is reported as DRIFT and refused."* A `run`/`serve` target added there
  would red `make pins`, and the lawful route would be an upstream change in
  `opensoft/openRepoShape` binding EVERY project that carries the shape. So the
  entry point is a `[project.scripts]` console script at the CODE leg (10.1),
  which is where the shape's own "What goes where" puts *"the implementation and
  its tests"*; the root's `README.md` has no shape-pin row and is the project's
  own to edit, so it documents and points at the command.
- [ ] **FALSIFIED BY** (clean checkout of openDox-code ONLY, fresh venv, no
  sibling installed — the server is started in the BACKGROUND with a readiness
  wait so the sequence runs to completion unattended):

      set -euo pipefail
      python -m venv .venv && . .venv/bin/activate && pip install .
      if python -c "import openxdox" 2>/dev/null; then echo "FAIL: sibling present"; exit 1; fi
      opendox --help >/dev/null                       # the console script MUST exist
      opendox --repo-root tests/fixtures/plain-documents generate-and-open --no-open --port 8080 &
      SERVER=$!
      trap 'kill "$SERVER" 2>/dev/null || true' EXIT   # cleanup cannot mask the verdict
      ready=0
      for _ in $(seq 1 30); do
        if curl -sf http://127.0.0.1:8080/ >/dev/null; then ready=1; break; fi
        sleep 1
      done
      test "$ready" -eq 1                              # a server that never started FAILS here
      body=$(curl -sf http://127.0.0.1:8080/)          # no pipeline: curl's status is the status
      printf '%s' "$body" | grep -qi '<html'           # and it is really the bundle

  `opendox --help` exits 0, the readiness loop must SUCCEED within 30s or `test`
  fails the sequence, and the fetched body must really be HTML — the earlier form
  of this box could pass with a server that never started, because `kill` masked
  the preceding status and `curl | head` hid a failed fetch. Today `opendox` does not exist as a
  console script, there is no `__main__.py`, and nothing serves `web/` — the
  runtime's `app.py` mounts no `StaticFiles` and declares only `/livez`,
  `/readyz` and `/api/v1`.

## Group 11 — Requirement 1: the guard holds (openxFactory)

- [ ] 11.1 At the close of the arc, a diff of openxFactory across every group
  shows: no `scripts/doc_health/` family moved, no `openspec/specs/` capability
  removed, no corpus document moved, no intent-plane schema moved, and no
  integration test moved. The only openxFactory edits are carve-manifest row
  annotations recording each closed reach.
- [ ] **FALSIFIED BY** (openxFactory checkout, at the close of the arc).
  **`<arc-base>` is THIS PACKET'S OWN MERGE COMMIT, not a pre-authoring commit** —
  the guard measures what the ARC does to openxFactory, and the packet's own
  filing artifacts (the `openspec/changes/` directory, the README bullet and the
  machine-seeded `tests/sequenced_after/corpus-ledger.yaml` row) are the FILING,
  not the arc. Defining the base any earlier makes the command self-failing,
  because this packet necessarily edits the ledger it would then flag:

      set -euo pipefail
      git diff --name-only <this-packet's-merge-commit>..<arc-tip> \
        -- scripts/ contracts/ tests/ ideation/ docs/ openspec/specs/ \
        ':(exclude)tests/sequenced_after/corpus-ledger.yaml' > /tmp/arc-paths.txt
      python3 - /tmp/arc-paths.txt <<'PY'
      import sys
      ALLOWED = {"docs/opendox-carve-manifest.yaml",
                 "openspec/specs/neutral-product-standalone-operability/spec.md"}
      touched = [l.strip() for l in open(sys.argv[1]) if l.strip()]
      breach = [p for p in touched if p not in ALLOWED]
      if breach:
          sys.exit("FAIL: the arc touched paths requirement 1 keeps:\n  " + "\n  ".join(breach))
      print(f"requirement 1 holds: {len(touched)} path(s) changed, all on the allow-list")
      PY

  **The allow-list is ENFORCED, not described.** Every path the diff prints must
  be `docs/opendox-carve-manifest.yaml` or
  `openspec/specs/neutral-product-standalone-operability/spec.md`; any other path
  exits non-zero and names itself, and is a breach of requirement 1 to be reverted
  or declared. The diff is captured to a file first, so a failing `git diff` fails
  under `set -e` instead of handing the check an empty list that would read as
  a pass. The ledger is
  excluded by name because it is machine-seeded bookkeeping every filing owes and
  carries no behaviour; if it ever moves for another reason, that shows up in the
  seeder's own `--ledger-diff` gate instead.

## Group 12 — Requirement 11: the neutral submission step (RULED, openDox-code)

**RULED** by Brett Heap, `#656` comment `5783934499`, 2026-09-22T20:49:40Z:
*"add a neutral publish step to the build arc"*. Named **submission** in the
delta, after the fifth of the six ruled words, for the reasons in `design.md`
§ D9 — "publisher" is already taken in this capability for the repository that
publishes the corpus and the contract bundle.

The seam is NOT invented here: `src/opendox/session_pr.py:98-99` already declares
`@runtime_checkable class PullRequestPort(Protocol)` with `push`, `open_or_update`
and `find_open`, and `FakePullRequests` (`:116`) is already a second
implementation. What is missing is a NEUTRAL implementation and a default binding
that does not name a platform.

- [ ] 12.1 Reshape the protocol around the neutral ACT rather than the platform's
  artifact. `push(branch)` is already git-neutral in its ARGUMENT and stays;
  `open_or_update` and `find_open` return a `PullRequest` carrying `url` /
  `number` / `state`, and `number` is a hosting platform's concept. Whatever the
  neutral return becomes, it must be expressible by a plain push.
- [ ] 12.1a **WIDEN `push`'s RETURN, because requirement 11's second scenario is
  not otherwise observable.** Today `push(self, branch: str) -> None`
  (`session_pr.py:103`), and a `None` cannot *"report where the work went"*. It
  returns a `Submission` record naming the DESTINATION THE WORK REACHED —
  `remote`, `ref`, and the remote's `url` as git resolves it — so scenario 2 is
  asserted rather than inferred from a side effect, and so scenario 3's refusal is
  distinguishable from a silent success by its RETURN and not only by its logs.
  **This adds no operation**, so `FR-030`'s *"three operations, and the absence of
  every other one"* (`session_pr.py:99-101`) is untouched: the count is the
  invariant, not the return type. `FakePullRequests` and `GhPullRequests` widen
  with it, and the existing tests that ignore the return keep passing.
- [ ] 12.2 Ship the NEUTRAL DEFAULT **as a named class in `opendox.session_pr`,
  `LocalGitSubmissions`, constructed exactly as `GhPullRequests` is —
  `LocalGitSubmissions(Path(checkout_root))`, one positional argument
  (`serve.py:933`) — so the binding in 12.4 is a name swap and not a signature
  change.** On a plain git repository with a remote attached, it pushes the
  session branch to it and returns the 12.1a `Submission` reporting where the work
  went. The
  runtime already models the remote — `runtime/repository_act.py:1131`'s
  `attach_remote(..., executable="git")` takes ANY git remote and writes no
  object, *"which is what makes the eventual move a push, not a migration"*.
- [ ] 12.3 With NO remote attached, say so plainly. Not an opaque failure, not a
  reported success. This is the same refusal discipline `corpus-adapter-seam`
  requires of an unresolvable corpus, applied to an unresolvable destination.
  **The refusal is a named exception, `session_pr.NoSubmissionTarget`, whose
  message names what is missing** — named here so the falsification can catch that
  type and nothing else, which is what separates "refused for the right reason"
  from "raised something".
- [ ] 12.4 Stop the DEFAULT BINDING naming a platform. `cli.py:812` and
  `serve.py:933` construct `GhPullRequests` by name and `serve.py:1507` records
  that an unset injection *"builds the real `GhPullRequests`"*. The unset default
  becomes the neutral implementation; `GhPullRequests` becomes ONE contributed
  implementation. **NAME THE SUBMISSION REGISTRATION POINT, and keep it SEPARATE
  from the generator's.** The submission seam ALREADY EXISTS and is
  `pull_request_factory` — `serve.py:766` declares it, `:931-932` calls it, and
  `:1505` describes it as *"the same kind of seam"* — so this box repoints its
  UNSET DEFAULT to the neutral implementation rather than inventing a seam. The
  generator seam that task 5.4 declares is a DIFFERENT interface that does not
  exist yet; the two are contributed through the same PATTERN, not through the
  same registration point, and conflating them would make neither implementable.
- [ ] 12.5 **THE GOVERNED FLOW IS UNCHANGED.** With the host's implementation
  registered, openxFactory's GitHub pull-request flow behaves exactly as today.
  This is a generalization, not a replacement, and 12.5 is the box that proves it.
- [ ] 12.6 **MERGE AUTHORITY — RULED, HOLD RELEASED.** Brett Heap, `#656` comment
  `5784155201`, 2026-09-22T21:06:01Z: *"merge yes"* — landing authority follows
  whoever governs the repository. A GOVERNED host reserves landing and routes it
  to the governance's own instrument (openxFactory's flow unchanged); a STANDALONE
  owner IS the governance and openDox may land. **Three guardrails in EVERY mode,
  none configurable:** explicit human act, conflicts SHOWN, and a merge that is a
  COMMIT and therefore revertible. Implement all three as tests, not as prose.
  *(Superseded instruction, kept so the change of direction is legible:)* An earlier draft made the absence of `merge`, `approve`,
  `review`, `self_review`, `bypass_protection` and `enable_auto_merge` binding and
  refused a merging implementation in a scenario; **both were withdrawn from the
  delta** on Brett Heap's question of 2026-09-22 — *"if we are going to have
  openDox be standalone, then it will need to merge documents."* The two readings
  were set out for the operator and the packet recommended neither; the ruling
  above answers them. The GOVERNED host's implementation still declares no merge
  and openxFactory's flow is still unchanged (12.5) — that half was never in
  question.
- [ ] **FALSIFIED BY** (openDox-code checkout, no sibling, **INSTALLED** —
  `python -m venv /tmp/v12 && . /tmp/v12/bin/activate && pip install .` — and
  `gh` NOT installed: `command -v gh` must be empty, which is the student's
  machine):

      set -euo pipefail
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      rm -rf /tmp/plain /tmp/remote
      git init -q /tmp/plain && git -C /tmp/plain commit -q --allow-empty -m seed
      git -C /tmp/plain branch sess-1                       # the SESSION BRANCH must exist to be pushed
      git init -q --bare /tmp/remote && git -C /tmp/plain remote add origin /tmp/remote
      # the NEUTRAL DEFAULT 12.2 names, constructed as GhPullRequests is (serve.py:933):
      python - <<'PY'
      from pathlib import Path
      from opendox import session_pr
      port = session_pr.LocalGitSubmissions(Path("/tmp/plain"))
      assert isinstance(port, session_pr.PullRequestPort), "the neutral default is not a PullRequestPort"
      r = port.push("sess-1")                               # 12.1a: returns a Submission, never None
      assert r is not None and r.ref.endswith("sess-1"), f"push reported no destination: {r!r}"
      assert "/tmp/remote" in r.url, f"the report does not name WHERE the work went: {r!r}"
      PY
      git -C /tmp/remote rev-parse --verify sess-1          # and the branch ARRIVED

  and then the NO-REMOTE case, which is scenario 3 and is executed, not described:

      git -C /tmp/plain remote remove origin
      python - <<'PY'
      from pathlib import Path
      from opendox import session_pr
      port = session_pr.LocalGitSubmissions(Path("/tmp/plain"))
      try:
          r = port.push("sess-1")
      except session_pr.NoSubmissionTarget as e:          # 12.3 names this refusal
          assert "remote" in str(e).lower(), f"the refusal does not name what is missing: {e}"
      else:
          raise AssertionError(f"a repository with no remote reported a submission: {r!r}")
      PY

  Two things are asserted on the remote path, not one: the branch arrived
  (`rev-parse --verify` exits non-zero if it did not, and `set -e` fails the
  sequence) **and the call REPORTED where it went**, which is requirement 11's
  second scenario and which a `None`-returning `push` could not have satisfied
  however well the push worked. And the no-remote path fails the sequence in BOTH
  wrong directions — a silent success reaches the `else` and raises; an opaque
  error is not `NoSubmissionTarget` and propagates — which is exactly the pair
  scenario 3 forbids.

  **And the three guardrails are asserted, now that 12.6 is RULED — by NAME**, so
  a missing test FAILS the command rather than being quietly absent from it. 12.6
  owes these four tests, and pytest exits non-zero (`ERROR: not found`) for any
  node that does not exist, so today the command fails:

      python -m pytest -q \
        "tests/test_landing_guardrails.py::test_land_requires_an_explicit_human_act" \
        "tests/test_landing_guardrails.py::test_land_shows_a_conflict_and_does_not_resolve_it" \
        "tests/test_landing_guardrails.py::test_a_landed_merge_is_a_commit_that_git_revert_undoes" \
        "tests/test_landing_guardrails.py::test_no_configuration_enables_automatic_landing"

  The fourth is the "none configurable" clause made testable: it walks the
  product's configuration surface and fails if any key can switch a guardrail
  off. Naming test nodes in an ACCEPTANCE command is not the defect Group 9
  removes from `validate.yml` — CI must run the whole suite, and this command runs
  four named proofs in addition to it.

  Today none of this is reachable: the only implementation is `GhPullRequests`,
  which shells `["gh", "pr", ...]` (`:367`) against `_GITHUB_HOST = "github.com"`
  (`:233`), so a machine without `gh` and a repository without a GitHub remote
  have no submission path at all.


## Group 13 — Requirements 12, 13: the standalone install's shape (RULED, openDox-code)

**RULED** `#656` `5784155201`, 2026-09-22T21:06:01Z: *"bundled postgres, local
identity yes"*. `design.md` § D10 carries the measurements and the two
amendments.

- [ ] 13.1 **Bundle Postgres with the standalone install** so a user installs the
  product and not a database. The pieces exist: `pyproject.toml:134` pins
  `psycopg[binary,pool]>=3.2` and `deploy/compose/docker-compose.yaml:25` is
  already `image: postgres:16`. This box makes the LOCAL install bring it.
- [ ] 13.2 **Add no SQLite dialect**, and record the refusal where a future reader
  will look for it: a second dialect doubles every migration and every schema test
  forever, for a database that under RULING Q1 holds no document.
- [ ] 13.3 **Keep both DSNs.** `OPENDOX_MIGRATION_DATABASE_URL` for migrating and
  `OPENDOX_DATABASE_URL` for serving, with neither defaulted from the other —
  `config.py` already names the silent fallback as the thing not to do, and a
  single-user install is not a reason to serve from the migrating credential.
- [ ] 13.4 **A NAMED local single-user mode (AMENDS RULING Q2).** `config.py:89-92`
  makes `OPENDOX_OIDC_ISSUER` required — *"the Keycloak broker's issuer, pinned
  … (RULING Q2)"*. Add an explicit local mode that needs no broker. **The selector
  is `OPENDOX_IDENTITY_MODE`, values `local` and `hosted`, read in
  `runtime/config.py` beside `OPENDOX_OIDC_ISSUER` and defaulting to `hosted`** —
  named here so the falsification below is executable and so the default is the
  SAFE one: an install that sets nothing is hosted, and a hosted install with no
  issuer refuses (13.5). It is UNSET, not `local`, that must be safe.
- [ ] 13.5 **A hosted install SHALL NOT fall into local mode by omission.** An
  unset issuer in a hosted install stays a REFUSAL naming the setting. This box
  is the safety of 13.4 and must land with it, not after it.
- [ ] 13.6 The hosted multi-user mode is UNCHANGED: same broker, same pinned
  issuer, a token from any other issuer still refused.
- [ ] **FALSIFIED BY** (a machine with no database and no identity broker):

      set -euo pipefail
      # the install is group 10's, unchanged — one entry point, one command:
      python -m venv /tmp/v13 && . /tmp/v13/bin/activate && pip install .
      unset OPENDOX_DATABASE_URL OPENDOX_OIDC_ISSUER      # a machine with NEITHER
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      R=$(mktemp -d)/plain-documents && cp -r tests/fixtures/plain-documents "$R"   # this group's OWN corpus, not Group 12's
      git -C "$R" init -q && git -C "$R" add -A && git -C "$R" commit -qm fixture
      opendox --help >/dev/null
      # LOCAL mode starts, with no broker and no operator-supplied database:
      OPENDOX_IDENTITY_MODE=local opendox --repo-root "$R" generate-and-open --no-open --port 8080 &
      SERVER=$!; trap 'kill "$SERVER" 2>/dev/null || true' EXIT
      ready=0; for _ in $(seq 1 30); do curl -sf http://127.0.0.1:8080/ >/dev/null && { ready=1; break; }; sleep 1; done
      test "$ready" -eq 1
      kill "$SERVER"; wait "$SERVER" 2>/dev/null || true
      # and a HOSTED install with no issuer REFUSES — by the SAME server path, and
      # the refusal must NAME THE SETTING, or an unrelated error would pass here:
      if OPENDOX_IDENTITY_MODE=hosted opendox --repo-root "$R" generate-and-open --no-open --port 8081 2>/tmp/hosted.err; then
        echo "FAIL: hosted install started with no issuer"; exit 1
      fi
      grep -q "OPENDOX_OIDC_ISSUER" /tmp/hosted.err       # the reason, not merely a non-zero exit
      # and the DEFAULT is hosted, so an install that configures nothing refuses too:
      if opendox --repo-root "$R" generate-and-open --no-open --port 8082 >/dev/null 2>&1; then
        echo "FAIL: an unconfigured install fell into local mode"; exit 1
      fi

  **Three assertions, and the second and third are the safety.** The hosted probe
  takes the SAME `generate-and-open` server path the local probe takes — not
  `--no-serve`, which can return before configuration is read — and it is not
  satisfied by a non-zero exit: `grep -q OPENDOX_OIDC_ISSUER` requires the refusal
  to name the missing setting, so an unrelated generation failure cannot pass it.
  The third proves the DEFAULT: with `OPENDOX_IDENTITY_MODE` unset the install
  must refuse exactly as the hosted one does, because 13.5's whole point is that a
  mode is entered deliberately and never by omission.

  Today none of it is reachable: the runtime refuses without
  `OPENDOX_DATABASE_URL` and `OPENDOX_OIDC_ISSUER`, and there is no local mode.

## Group 14 — Requirements 6, 14, 15: health in the store, and the fix loop (RULED, openDox-code)

**RULED** `#656` `5784155201` (*"health in db"*) and `5784247356` (*"1, add the
fix loop to #1144"*). `design.md` §§ D10.4, D10.5 and D11.

- [ ] 14.1 **The health table arrives as `0003_`, NOT `0002_`.**
  `migrations/0002_migration_state.sql` already exists (the
  `opendox_schema_migrations` ledger). `0001` is applied verbatim behind
  `CANONICAL_MIGRATION_SHA256` and its own text says *"Changing the schema is
  therefore an ADDITIVE `0002_…`/`0003_…` file, never an edit here"*.
- [ ] 14.2 **DECLARE whether the health table is a DOMAIN table or install-owned,
  and say why.** This is the boundary claim, and the closure test is scoped to
  the CANONICAL migration only — which is why `0002`'s ledger table did not trip
  it. If DOMAIN: `identity.TABLES` and
  `tests_runtime/test_schema_shape.py`'s closure text move in the SAME change. If
  install-owned: the `0002` precedent already covers it and no closure text moves.
  **Either way the choice is stated in the open**, which is what
  `test_..._exactly_rulings_six_tables`'s message demands.
- [ ] 14.3 The store holds NO DOCUMENT and stays DISPOSABLE (Q1's principle,
  untouched): results are recomputable from git, so losing the store costs a
  recomputation.
- [ ] 14.4 **The neutral families**, as ruled: broken internal links, orphans,
  near-duplicates, missing neutral front matter from the adapter's fields, a
  declared stage that disagrees with the document's location among the six ruled
  words, and stale or empty stubs. On demand from dashboard and CLI, optionally on
  commit. Baseline-relative. Model-assisted checks only where a model is
  configured. **openxFactory's 23 governance families stay put** (requirement 1).
- [ ] 14.5 **The Health view, with CLI PARITY.** Every resolution action available
  in the view is available from the command line — requirement 14's last scenario
  exists because a standalone install may have no browser. **The verbs this arc
  adds to `opendox.cli`, named here so groups 14 and 15 close on an exact
  surface** (the preamble's rule: no box closes on a verb its own group did not
  declare):

  | verb | shape |
  |---|---|
  | `health run` | `--repo-root <corpus> health run [--pack ID] [--timeout SECONDS]` |
  | `health list` | `--repo-root <corpus> health list [--json]` |
  | `health fix` | `--repo-root <corpus> health fix --finding ID [--batch]` |
  | `health accept` | `--repo-root <corpus> health accept --finding ID --reason TEXT` |

  They are NEW surface — `cli.py` declares none of them today (10.1's table is the
  surface that exists) — and 14.6's applier is what `health fix` invokes.
- [ ] 14.6 **The three resolution classes, spelled `auto-fix`, `assisted` and
  `human-only` — exactly as RULED (`5784247356`) and exactly as requirement 14
  declares them, in the store, the CLI, the view and the pack contract (15.2)
  alike**, because a pack must return an ENGINE-declared class and two spellings
  of one class are two classes. `auto-fix` for the mechanical findings (moved link
  target, derivable front matter, stage/location mismatch), written by the
  product; `assisted` (near-duplicates, empty stubs), proposed for the human to
  edit, model-written only where a model is configured; `human-only`, evidence
  shown.
  **THE APPLIER IS NEW WORK** — openxFactory CLASSIFIES
  (`scripts/doc_health/__init__.py:17-18`, `AUTO_FIXABLE`/`CONTESTED`) and
  `grep -rln 'def apply_fix|def autofix|def fix('` over `scripts/doc_health/`
  returns nothing. Nothing in this estate applies a fix today.
- [ ] 14.7 **Every repair is a DRAFT ON A BRANCH and lands only through the
  landing rule** (requirement 11, group 12): standalone owner lands in openDox, a
  governed repository gets the governance's instrument, and in every mode the
  landing is an explicit human act with conflicts shown and a revertible commit.
  **NOTHING auto-merges, not even a one-line fix.** Batching many repairs into ONE
  draft for ONE review is the pressure valve, and is allowed.
- [ ] 14.8 **EXCEPTIONS LIVE IN GIT, NOT THE STORE**, on the pattern of
  openxFactory's `health/dispositions.yaml` — whose semantics already match:
  `scripts/doc_health/families.py:370` reads *"removing its
  health/dispositions.yaml entry re-opens"* the finding. An exception is a
  judgement that exists nowhere else; the store is disposable, so an exception
  stored there is a judgement scheduled for deletion.
- [ ] 14.9 **Ship `tests/fixtures/health-corpus`**: a small corpus with ONE
  known broken internal link (finding `broken-link`, class `auto-fix`) and ONE
  finding the fixture will accept (`accepted-finding`), and nothing else a
  neutral family would flag — so every assertion below is about a finding the
  fixture put there on purpose.
- [ ] **FALSIFIED BY** (openDox-code, installed, over 14.9's fixture corpus with a
  known broken link and a known accepted finding):

      set -euo pipefail
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      C=$(mktemp -d)/health-corpus && cp -r tests/fixtures/health-corpus "$C"   # a FRESH repository: fix branches and commits land HERE
      git -C "$C" init -q && git -C "$C" add -A && git -C "$C" commit -qm fixture
      opendox --repo-root $C health run
      opendox --repo-root $C health list > /tmp/h1.txt
      grep -q 'broken-link' /tmp/h1.txt
      # a mechanical repair writes a DRAFT ON A BRANCH and never the default branch:
      before=$(git -C $C rev-parse HEAD)
      opendox --repo-root $C health fix --finding broken-link
      test "$(git -C $C rev-parse HEAD)" = "$before"        # default branch UNMOVED
      git -C $C rev-parse --verify --quiet refs/heads/health-fix-broken-link
      # THE EXCEPTION IS PROVED TO EXIST BEFORE THE RESET, not merely absent after:
      opendox --repo-root $C health accept --finding accepted-finding --reason "fixture"
      git -C $C diff --quiet -- health/dispositions.yaml && { echo "FAIL: accept wrote nothing to git"; exit 1; }
      git -C $C add health/dispositions.yaml && git -C $C commit -qm "accept fixture finding"
      opendox --repo-root $C health run
      opendox --repo-root $C health list > /tmp/h2.txt
      ! grep -q 'accepted-finding' /tmp/h2.txt              # suppressed BEFORE the reset
      # ...and it survives the store being dropped and rebuilt:
      opendox-runtime runtime reset --confirm yes-drop-the-coordination-database
      opendox-runtime runtime migrate
      opendox --repo-root $C health run
      opendox --repo-root $C health list > /tmp/h3.txt      # a FAILING list now fails the sequence
      grep -q 'broken-link' /tmp/h3.txt                     # the run really did produce findings
      ! grep -q 'accepted-finding' /tmp/h3.txt              # and the exception still holds

  Four things are proved in order, and the order is the point: the exception is
  written TO GIT (a `git diff --quiet` that finds no change fails the sequence),
  it suppresses the finding BEFORE the reset, the post-reset run really produced
  findings (`broken-link` is present, so an empty listing cannot masquerade as
  suppression), and only then is `accepted-finding` asserted absent. **Every
  listing is captured to a file first and grepped second**, so a `health list`
  that exits non-zero fails under `set -e` instead of being read as the desired
  absence — which is exactly what the earlier `if … | grep -q` form would have
  done. The default branch must not move and the draft branch must exist.

  Today none of it exists: there is no health table, no health verb, and no
  applier anywhere in the estate.


## Group 15 — Requirement 16: the check-pack interface (RULED, openDox-code)

**RULED** `#656` `5784295745`, 2026-09-22T21:16:17Z: *"1, add the pack interface
to #1144"*. `design.md` § D12.

- [ ] 15.1 Declare the NEUTRAL CHECK-PACK CONTRACT in openDox, on the
  `src/opendox/corpus_adapter.py` Protocol pattern (a `@runtime_checkable`
  Protocol with a CLOSED member set, for the reasons that file's own docstring
  gives: structural conformance lets an implementation authored elsewhere satisfy
  it without importing this product's tooling).
- [ ] 15.2 A pack DECLARES check families: id, version, and which documents each
  applies to. It RETURNS findings in the neutral shape — severity, resolution
  class (`auto-fix` / `assisted` / `human-only`, 14.6's spellings and no
  other), evidence — and MAY return proposed
  fixes AS PATCHES ONLY.
- [ ] 15.3 A pack's labels resolve through the DISPLAY FACET
  (`src/opendox/display_profile.py`), never spelled into the neutral surface —
  the same rule slice S7 applied to the front end, and the reason
  `NEUTRAL_DISPLAY`'s six words stay openDox's own.
- [ ] 15.4 **THE ENGINE KEEPS**, identically for every pack: the Health view and
  its CLI parity, scheduling, the baseline, storage (results in the store,
  exceptions in git), and the fix loop with its landing rule.
- [ ] 15.5 **THE REFUSALS**, each as a test and not as prose: a pack that writes,
  commits or merges; a pack consumed without a commit-and-digest pin; a pack that
  returns a class the engine does not declare, or declares its own baseline or
  landing rule.
- [ ] 15.6 **A PACK THAT CRASHES OR TIMES OUT IS A FINDING AGAINST THAT PACK**,
  and the other packs still run. Give it a time budget: `health run --timeout
  SECONDS` (14.5), default declared by this box, applied PER PACK and enforced by
  the engine rather than by the caller — a pack cannot opt out of it. A health
  check whose failure mode is silence is worse than one that reports itself
  broken — the doc-health nightly failed silently every night from 2026-08-30 and
  nobody saw it.
- [ ] 15.6a **SHIP THE TWO FIXTURE PACKS the falsification needs**, under
  `tests/fixtures/packs/`, registered the way 15.1's contract says packs are
  registered (declare that registration here if 15.1 leaves it open):
  `fixture-crashing-pack`, which raises on its first family, and
  `fixture-slow-pack`, which sleeps past any timeout. They are test fixtures of
  the engine, not shipped packs, and they exist so 15.6 is falsifiable rather
  than asserted.
- [ ] 15.7 **PACK ID AND PACK VERSION ON EVERY FINDING, in the SAME additive
  migration as the results table** (group 14.1 — `0003_`, since `0002_` is the
  ledger), so the table is not migrated twice.
- [ ] **FALSIFIED BY** (openDox-code, installed, with a deliberately broken pack
  and a deliberately slow one registered beside the neutral checks):

      set -euo pipefail
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      C=$(mktemp -d)/health-corpus && cp -r tests/fixtures/health-corpus "$C"
      git -C "$C" init -q && git -C "$C" add -A && git -C "$C" commit -qm fixture
      # the two fixture packs of 15.6a are registered; the run is itself bounded,
      # so a hang is a FAILED FALSIFICATION and never a hung falsifier:
      timeout 120 opendox --repo-root $C health run --timeout 5
      # the neutral checks still produced findings despite a crashing pack:
      opendox --repo-root $C health list > /tmp/p1.txt
      grep -q 'broken-link' /tmp/p1.txt
      # and BOTH broken packs are themselves findings, attributed:
      opendox --repo-root $C health list --json > /tmp/p1.json
      python3 - /tmp/p1.json <<'PY'
      import json, sys
      f = json.load(open(sys.argv[1]))
      ids = {x['pack_id'] for x in f}
      assert 'fixture-crashing-pack' in ids, 'crashing pack not reported'
      assert 'fixture-slow-pack' in ids, 'timed-out pack not reported'
      assert all(x.get('pack_id') and x.get('pack_version') for x in f), 'a finding has no provenance'
      print('packs attributed:', sorted(ids))
      PY
      # and 15.5's REFUSALS, each a NAMED test — a missing node fails the command:
      python -m pytest -q \
        "tests/test_check_packs.py::test_a_pack_that_writes_commits_or_merges_is_refused" \
        "tests/test_check_packs.py::test_an_unpinned_pack_is_refused" \
        "tests/test_check_packs.py::test_a_pack_returning_an_undeclared_class_is_refused" \
        "tests/test_check_packs.py::test_a_pack_declaring_its_own_baseline_or_landing_rule_is_refused"

  Every finding carries a pack id and version, **BOTH** broken packs appear as
  findings rather than as a stack trace and a hang, and the run completes. The
  outer `timeout 120` is the difference between a falsifier that FAILS on a
  runaway pack and one that HANGS on it: without it, the very defect 15.6 exists
  to prevent would take the acceptance command down with it, and the box would
  look unfinished rather than failed. The JSON is captured to a file and read by
  `sys.argv[1]`, because a heredoc and a stdin redirect cannot both feed the same
  interpreter and the heredoc wins.

  Today none of this exists: there is no pack contract, no health run, and no
  findings store.

## Follow-ons named here and NOT authored here

- [~] F1 **Port openxFactory's 23 governance families into the openXdox pack.**
  An openXdox FOLLOW-ON with its own claim. Until it lands, requirement 1 keeps
  those families with openxFactory. **Owner: whoever claims it on `#656`.**
- [~] F2 **Each DomainxFactory's own pack**, pinned in that domain's `stack.yaml`.
  That domain's own work. **Owner: each domain.**
