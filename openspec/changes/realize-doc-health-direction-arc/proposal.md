---
code_surface: opensoft/openXdox-code, opensoft/openDox-code and openxFactory — named as RULED by ARC-Q3 (a) (`#656` `6003918488`, verbatim *"Own change, beside phase 5 (Recommended)"*: "a `code_surface:` naming openXdox-code, openDox-code and openxFactory host wiring"). In `opensoft/openXdox-code` the realization declares four governed seams, retargets the eight modules of `DOC_HEALTH_SURFACE` (`tests/test_dependency_direction.py:353-363` at `56e1c238`) away from openxFactory's `doc_health`, respells the 7 test files that import `doc_health` directly, and makes F9.2's two code removals. In `opensoft/openDox-code` it re-authors the generic `lines` slice (`split_keepends`, `join_rows`) and the one `RealGit` read the generator makes (`head_sha`) as a small standard-library module; nothing is relocated out of openxFactory (R2Q14 (a), #1144 11.1). In `openxFactory` it touches HOST WIRING only: `scripts/opendox_host.py` registers the governed implementations at openXdox-code's seams at startup, in the pattern of `scripts/opendox_host.py:518-533`, with a host-wiring test under `tests/domain_profile/`. THIS PACKET AUTHORS NO CODE BYTE: landing it is corpus text only (its four files, one README *Active changes* bullet and the machine-seeded row in `tests/sequenced_after/corpus-ledger.yaml`). The pins that carry the realization (the openDox and openXdox roots' code pins, openXdox-code's `opendox @` pin and openxFactory's two pin pairs) move by each owner's ordinary pin-sync act in the landing that needs it (plan 038 § "Pins and landing order", ARC-6) and are not runtime artifacts this change authors.
target_release: implemented — the affected repositories' main lines (openXdox-code, openDox-code, openxFactory), RULED by ARC-1 (a) (`#656` `6013547504`, verbatim *"implemented (Recommended)"*). No contract bundle is cut, no bundle number is reserved and no release tag is owed. The code surface is NON-EMPTY, so under `release-realization`'s archive gate this change, once ratified, stays ACTIVE as approved-but-unrealized intent until its realization is merged and green (tasks 7.1–7.4).
sequenced_after: []
---

# Proposal: realize-doc-health-direction-arc

Status: draft
Authored: 2026-10-06, lane `openxfactory-4` (display `openXfactory-4-openDox_extraction`), as plan 038's T070 (`specs/038-opendox-document-tool-self-maintenance/`, draft PR #1245).
Directed by: Brett Heap's ruling of the `doc_health` direction arc, ARC-Q1–ARC-Q4 all (a) (`#656` comment `6003918488`, 2026-10-05T21:59:43Z), and his ruling of plan 038 (`#656` comment `6013547504`, 2026-10-06T09:39:55Z: ARC-1 `implemented`, ARC-5 (a), and the tier-3 defaults ARC-2, ARC-3, ARC-4 and ARC-6 "as recommended").
Origin: the staged topic `ideation/staging/doc-health-direction-arc/` (`Staging ID: openxFactory:staging:doc-health-direction-arc`), through its own exit path (`doc-health-direction-arc.md:472-553`).
Kind: architecture

**DRAFT. FILING IS NOT RATIFYING.** The three lifecycle documents carry
`Status: draft`, and `.openspec.yaml` declares drafting provenance and no
approval pair. Brett Heap's ratify word is plan 038's T071. No realization
slice starts before it (plan 038 `tasks.md` T071, "No realization slice
starts before it").

## Why

openXdox-code is the neutral, standalone-installable layer that #1144
(`add-neutral-product-standalone-operability`) exists to make stand on its
own. Eight of its modules import openxFactory's own governance tooling,
`scripts/doc_health/`, by name: 13 statements, 7 at import time and 6
deferred, declared and guarded as `DOC_HEALTH_SURFACE`
(openXdox-code `tests/test_dependency_direction.py:353-363` at `56e1c238`).
That is the shape `corpus-adapter-seam` Requirement 1 refuses: *"no neutral
product `openxFactory` pins SHALL import `openxFactory`'s own tooling"*
(`openspec/specs/corpus-adapter-seam/spec.md:21-27`). Nothing in the ruled
record accepts the violation (the staged topic, `:489-493`).

Release 1 did not fix it. R1Q6 (d) (`#656` `5817152735`) ruled a counted,
reasoned exclusion for requirement 9's standalone-suite problem and deferred
the DIRECTION to this arc. Brett ruled the direction on 2026-10-05:

- **ARC-Q1 (a), *"Retarget all eight (Recommended)"*.** The generic `lines`
  slice is re-authored in openDox-code. The governed names are reached
  through seams that openXdox-code declares and openxFactory's host wiring
  registers. The 7 test files that import `doc_health` directly are
  respelled. Requirement 1 is met for all eight modules, with NO
  `corpus-adapter-seam` change.
- **ARC-Q2 (a), *"Composed CI in openXdox-code (Recommended)"*.** Whatever
  stays composed runs in openXdox-code's CI against a pinned openxFactory,
  permanently. That is #1144's requirement-9 work (plan 038 T073, lane
  openXfactory-3), not this change's.
- **ARC-Q3 (a), *"Own change, beside phase 5 (Recommended)"*.** The
  realization gets its OWN OpenSpec change, owned by lane openxfactory-4
  under plan 038. It gates neither release 2's close nor #1144's archive.
- **ARC-Q4 (a), *"Confirm (Recommended)"*.** The decision was owed before
  F12.1 runs, and the ruling discharged it. The realization is not on 12.5's
  path.

This packet is the change ARC-Q3 (a) names.

## What Changes

The realization runs in three repositories, as the code surface above names
them. `design.md` carries the measurements; `tasks.md` carries the steps.

- **openDox-code: the generic slice, re-authored (plan 038 T072).** A small
  standard-library module carrying `split_keepends`, `join_rows` and the one
  git read the generator takes from `RealGit` (`head_sha`,
  `src/openxdox/generator.py:128`). openxFactory's `scripts/doc_health/lines.py`
  stays where it is: this is a second implementation in the neutral product,
  not a move.
- **openXdox-code: the seams, the retargets and the respellings (T074).**
  - Four seams, each registered once at process start by a host: S1 corpus
    loading and status reading, S2 the possibles index and its disposition,
    S3 the readiness renderer, S4 the pin sentinel.
  - The eight modules stop importing `doc_health`: `completeness.py`,
    `round_trip.py` and `generator.py`'s generic half import T072's module,
    and every governed name is read through its seam AT USE.
  - The 7 test files that import `doc_health` directly are respelled. None is
    among 12.5's 16 protected suites or F5.2's 7 generator suites.
  - `DOC_HEALTH_SURFACE` falls to empty, and the `doc_health` reason leaves
    `tests/declared_exclusion.yaml`.
  - F9.2's two code removals: the help-tree test's `--deselect` in the
    required check, and the guard test beside it.
- **openxFactory: host wiring only (T075).** `scripts/opendox_host.py`
  registers openxFactory's governed implementations at the four seams at
  startup, in the pattern of `:518-533`, with a host-wiring test under
  `tests/domain_profile/`. It lands in the openxFactory PR that moves the
  openXdox pin pair to the openXdox root commit pinning T074's code (that root
  commit lands first, in its own PR), so openxFactory's `main` never runs an
  openXdox that declares seams it does not fill.
- **F9.2 (T076).** F9.2 is re-run and quoted in this change's own evidence.
  If #1144 is still active, F9.1's `--deselect` (batch J's) leaves #1144's
  `tasks.md` and F9.2 is ticked there; if #1144 has archived, the closure
  lives in this change's evidence alone (ARC-5 (a), `6013547504`).
- **The arc's own trailer and surfaces check (ARC-4; ADV-37).** Realization
  landings carry `Arc: realize-doc-health-direction-arc`, not #1144's value.
  Because that takes T075's openxFactory edit out of #1144's F11.1, this
  change runs an equivalent surfaces check over its own landings
  (`design.md` § 8), quoted in T075's PR and at the archive.
- **Archive and the staged topic's exit (T077).** On merged, green
  realization evidence; landed by merge commit, never squash.

## What this change does NOT do

- **It changes no specification.** `skip_specs: true`. Requirement 1 is MET,
  not changed, so there is no `corpus-adapter-seam` delta (ARC-Q1 (a); ARC-3).
  No openXdox-spec delta is needed either: the seams are in-process
  registration points inside openXdox-code, and release 1's six seams of the
  same kind landed with no spec-leg contract text (`design.md` § 5, D1).
- **It moves nothing out of openxFactory.** No `scripts/doc_health/` module
  moves, splits or gains a packaging file (R2Q14 (a); #1144 11.1). The
  governed implementations stay openxFactory's and reach openXdox only
  through the host's registration.
- **It does not do #1144's requirement-9 work.** The composed declarations
  (T073: the governed-behaviour files, R1Q24's 3 rail files and 5 contracts
  files, declared as composed integration tests in U-9's permanent workflow)
  are #1144's, carry #1144's `Arc:` value, and are not gated on this
  change's ratification.
- **It gates nothing.** Not release 2's close, not T061's 0.2.0 bump (ARC-6),
  not #1144's archive (ARC-Q3 (a); ARC-5 (a)). F12.1 stays composed, and the
  composition is its permanent home (CF-5).
- **It does not grow #1144's F11.1 guard.** F11.1 never sees this change's
  landings; the equivalent check here is this change's own.

## Class by class: which treatment reaches which declared-exclusion entry

The staged topic's exit path requires this, class by class
(`doc-health-direction-arc.md:532-536`). At openXdox-code `56e1c238`
`tests/declared_exclusion.yaml` holds 66 files: `doc_health` 60,
`status-exemption-rail` 3, `openxfactory-contracts` 5, with 58 files carrying
`doc_health` alone (`design.md` § 2).

| class | files | what reaches it | whose work |
|---|---|---|---|
| `doc_health` | 60 | This change removes the CAUSE: no module imports `doc_health` after T074, so the reason empties. Each of the 60 then goes one of two ways, measured file by file at T074's base: it collects and passes alone, and its entry leaves; or it tests governed BEHAVIOUR, which needs the host's implementations, and it runs composed as a declared integration test. How many go each way is NOT measured at filing. | this change (T074), with T073's declarations as the composed home |
| `status-exemption-rail` | 3 | Not this change. The rail is registered in the composed conftest, as U-1 registers the host, and the files run composed. | #1144 (T073, ARC-Q2 (a)) |
| `openxfactory-contracts` | 5 | Not this change. The files read 3 schemas that 7.1 and 7.1b keep in openxFactory, and run composed against the pinned openxFactory. | #1144 (T073, ARC-Q2 (a)) |

So this change closes the `doc_health` CAUSE and does not, by itself, empty
the declaration: requirement 9 closes for openXdox-code by DECLARATION, class
by class, through T073 (ARC-Q2 (a)).

## Module by module: Requirement 1 after the realization

All eight are retargeted under ARC-Q1 (a), so `corpus-adapter-seam`
Requirement 1 is met for every module. None is left on composition alone.

| module | today (`56e1c238`) | after T074 |
|---|---|---|
| `completeness.py` | `doc_health.lines.split_keepends` | T072's openDox-code module |
| `round_trip.py` | `doc_health.lines.join_rows`, `split_keepends` | T072's openDox-code module |
| `generator.py` | `corpus` (`Doc`, `load_docs`, `parse_status`, `STATUS_SCAN_LINES`), `RealGit` (`head_sha`), `lines.split_keepends` | generic half: T072's module; governed half: seam S1 |
| `corpus_root.py` | `corpus` (`GOVERNED_ROOTS`, `iter_doc_paths`) | seam S1 |
| `gate_console.py` | `corpus.STATUS_SCAN_LINES`; `derive_possibles` (seven names); `ideation_readiness._render_markdown` | seams S1, S2, S3 |
| `cli_gate.py` | `derive_possibles` (`INDEX_REL`, `INDEX_MD_REL`) | seam S2 |
| `gate_routes.py` | `derive_possibles` (`INDEX_REL`, `INDEX_MD_REL`) | seam S2 |
| `snapshot_registry.py` | `pin_sentinels.UNKNOWN` | seam S4 |

## Impact

- **Affected specs:** none (`skip_specs: true`).
- **Affected code:** openXdox-code `src/openxdox/` (the eight modules, the seam
  declarations, and the contribution modules `design.md` § 10 names), its
  tests, `tests/declared_exclusion.yaml` and its workflows; openDox-code (one
  new module and its tests); openxFactory `scripts/opendox_host.py` and
  `tests/domain_profile/`.
- **Trailer:** `Arc: realize-doc-health-direction-arc` on every realization
  landing (ARC-4). Bookkeeping, evidence and this filing carry none.
- **Ordering:** after T071 (the ratify word). T072 rides T061's pin only if it
  has already landed; otherwise the arc brings its own pin chain (ARC-6).
  T074 follows T021 and T073 on the files they share (plan 038's
  single-writer table).

## Decisions put for the ratify read

`design.md` § 11 states each with its alternative and what a veto costs:

- **D1.** No openXdox-spec delta (`skip_specs: true`), on a measured precedent.
- **D2.** Every seam is read at USE, never at import; three module-level
  constants change form.
- **D3.** An unregistered seam refuses BY NAME at use; it never degrades.
- **D4.** In a lone checkout, openXdox's governed columns are keyed on the
  governed seams being registered (recommended), not registered
  unconditionally.
- **D5.** The surfaces check: F11.1's guard over this change's own landings,
  plus the protected-suite oracle over its openXdox-code landings.
- **D6.** The staged topic stays staged until T077, declared as this change's
  `staged` origin.
- **D7.** The host fills openXdox's four seams as their own all-or-none
  group.

## Measured at filing, for the holder

`design.md` § 10 lists the files the realization must also edit that plan
038's T074 `Files` line does not name. The largest is that, at
openXdox-code `56e1c238`, the help-tree test's `--deselect` lives in
`.github/workflows/validate.yml` (`LEFT_OUT`, `:161-164`), and
`composed.yml` does not exist yet. This packet records them; amending plan
038 is the holder's act.
