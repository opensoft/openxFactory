# Data model: openDox, the document tool and self-maintenance (release 2)

Status: draft

**Feature**: [`spec.md`](./spec.md) (§ Key Entities) · **Plan**: [`plan.md`](./plan.md)
· **Contracts**: [`contracts/`](./contracts/)

Every entity below was RULED with the plan (`#656` `6013547504`, every decision as
recommended; T004). Field names
are the plan's, except where #1144's ratified text or its falsifiers fix them
(then the box is cited). The three shapes that become openDox-spec schemas
(R2Q22 (a)) are fixed in `contracts/`, and this file points there rather than
repeating them. "Owner" names the task that lands the entity. Review round 1
(`evidence/analyze-round-1.md`, `evidence/plancheck-lane3-round-1.md`) corrected
this file; each correction cites its finding.

## Phase 4: submission and landing

### Submission (12.1a; owner T011)

The report requirement 11's third scenario needs, returned by
`SubmissionPort.submit(branch)` ONLY on success. F12.2 asserts
`r.ref.endswith("sess-1")` and that the remote's path is in `r.url`
(#1144 `tasks.md:2848`; ADV-02).

| field | type | rule |
|---|---|---|
| `remote` | string | the remote pushed to: the one named `origin`, else the repository's sole remote (ADV-26) |
| `ref` | string | the ref that received the work, `refs/heads/<branch>` |
| `url` | string | the remote's URL as git resolves it, with ANY credential it carries REDACTED: userinfo and query-string tokens (12.1a). The host and path stay, so the report says where the work went |
| `branch` | string | the local branch submitted; never `main` (R2Q5 (a)) |
| `commit` | 40-hex | the branch tip that was pushed |

**Failures raise; they never return.** A failure is told apart from a success
by what `submit` does, not by its logs (12.1a):
- `NoSubmissionTarget` (12.3; FR-002) is raised when no remote is attached, or
  when several remotes are attached and none is named `origin`. Its message
  names what is missing ("no remote is attached…", "several remotes and none
  named `origin`…").
- `SubmissionRefused` is raised when the remote rejects the push, when the
  chosen remote has several push URLs, or when the transport fails.
- Every message, of a success report and of each failure, is REDACTED by the
  same rule as `url`. A credential-bearing remote is PUSHED, not refused
  (12.1a designs exactly that case; ADV-09). The test that pins this is F12.2's
  `test_a_credential_in_the_remote_url_never_reaches_the_report`.

### Governance (12.6a; R2Q4 (a), R2Q7 (a); owner T012)

`repository_governance(checkout_root)` is declared in `session_pr` (FR-007) and
returns exactly one of three values, fail closed.

| value | when |
|---|---|
| `governed` | a registered host profile declares an instrument (its contributed `SubmissionPort`); this outranks any declaration. Or the declaration at `main`'s tip says `governed` |
| `standalone` | the explicit local install (`OPENDOX_INSTALL_MODE=local` or `--local`, 13.4), no instrument, and the declaration at `main`'s tip says `standalone` |
| `unknown` | anything else: no `main`; no declaration; an unreadable file; another `kind`; an unknown key or value |

**The declaration** (decision N-1), `.opendox/governance.yaml`, read from the
blob at `main`'s tip (never the working tree, never the branch being landed):

```yaml
schema_version: 1
kind: opendox-governance
governance: standalone        # or: governed
```

With no declaration, `land` refuses, naming the exact file and content, which
the owner commits with git (R2Q7 (a)). A repository with no `main` is `unknown`,
refused naming the absent branch (R2Q7 (a); both are T012 test nodes beside
F12.2's thirteen, lane 3's R2Q7 FIX). The openDox root's README documents it
(T018).

### Confirmation capability (12.6a; owner T012)

| field | rule |
|---|---|
| `branch` | the branch it confirms |
| `head` | the branch tip at issue time; a moved branch invalidates it |
| `issuer` | `tty` (the `land` prompt over `/dev/tty`) or `view` (a nonce minted by the loopback server for that branch, consumed by the confirm control) |
| `nonce` | for `view`: a server-minted single-use value; for `tty`: none |
| `used` | single-use: a second `land` with the same capability is refused |

No other issuer exists, and a static check proves it (F12.2's
`test_only_the_interactive_layers_call_an_issuer`). With no `/dev/tty` and no
view, `land` refuses (12.6a, "refuses when there is none").

### Landed and MergeConflict (12.6a; owner T012)

`LandingPort.land(branch, *, confirmation) -> Landed`, declared in `session_pr`.
The `land` ACT answers `Landed` when standalone, and the instrument's
`Submission` when governed, with no merge (R2Q4 (a)); the two are told apart by
their fields (`merge_commit` is `Landed`'s alone; contracts/cli-http-submit-land.md).

| `Landed` field | rule |
|---|---|
| `branch` | the landed branch |
| `merge_commit` | the `--no-ff` merge commit, made in the lander's own landing worktree under `<repo>-worktrees/` (`session_git.py:250-263`) |
| `previous_main` | `main` before the merge; `git revert -m 1 <merge_commit>` restores its tree |
| `served_checkout` | `fast-forwarded` (the served checkout held `main` and was clean: `git merge --ff-only <merge_commit>` there), or `left` (the served checkout holds ANOTHER branch, so only the `main` ref moved; ADV-08) |
| `pushed` | always `false`: `land` pushes nothing (R2Q6 (a)) |

`MergeConflict` lists the conflicting paths and names the remedy: bring `main`
into the branch and resolve there (OQ-038-1). Nothing is merged.

**The remote check** (R2Q6 (a); C6). Before merging, `land` reads the `main`
tip at the PUSH URL of the remote `submit` would choose: the one URL `git
remote get-url --push <remote>` returns (the fetch URL when no `pushurl` is
set), since the owner's later `git push` of `main` goes there. `git ls-remote
<remote>` would read the FETCH URL, another repository when a `pushurl` differs
(Copilot's review of `cbe2adfb`). A remote with several push URLs is refused by
name, as `submit` refuses it. **The push URL never reaches git's argv**, which
any local user can read through `/proc/<pid>/cmdline`, and a push URL may carry
a credential (12.1a). git probes it through a TRANSIENT remote passed in the
environment of that one child: `GIT_CONFIG_COUNT=1`,
`GIT_CONFIG_KEY_0=remote.<transient>.url`, `GIT_CONFIG_VALUE_0=<push URL>`, then
`git ls-remote <transient> refs/heads/main`, where `<transient>` is a name no
configured remote uses. This needs git 2.31 or later (CI's ubuntu-24.04 has
2.43); an older git is refused by name (Copilot's review of `74dfe79c`). If the push URL has a `main`,
local `main` must contain that tip (`git merge-base --is-ancestor`); otherwise
`land` refuses, naming `git pull`'s absence and the remedy. A remote with no
`main`, or no remote at all, passes the check. Every message is redacted by the
`Submission`'s `url` rule (12.1a).

### The landing's states

```text
requested
  ├─ refused: governance unknown (no main | no declaration | unreadable) | governed-without-an-instrument
  │           | branch is main | no, used or stale confirmation | local main lacks the push URL's main tip
  │           | the chosen remote has several push URLs
  │           | the served checkout holds main and is NOT clean (ADV-08: named remedy, commit or stash first)
  ├─ governed with an instrument → submitted through the instrument (Submission), no merge (R2Q4 (a))
  └─ standalone → merged in the lander's landing worktree
        ├─ conflict → MergeConflict, nothing merged, the landing worktree discarded
        └─ merged → served checkout on main and clean: ff-only → Landed(fast-forwarded)
                    served checkout on another branch: main ref moved only → Landed(left)
              └─ a live session on that branch ends by the existing merge observation (R2Q5 (a))
```

## Phase 5: health

### Health run (14.4; R2Q12 (a); owner T042, T046)

Table `health_runs` in `0003_` (OQ-H-22; DOMAIN, R2Q13 (a)):

| column | type | rule |
|---|---|---|
| `run_id` | uuid | primary key |
| `corpus_root` | text | the corpus's resolved root; no foreign key to `projects` |
| `kind` | text | `default-tip`, `branch` or `working-state` (below) |
| `commit` | 40-hex, nullable | the commit read; null for a working-state run |
| `baseline_branch` | text, nullable | the branch whose tip runs form the baseline (tier 1 decision I-2) |
| `started_at`, `finished_at` | timestamptz | |
| `outcome` | `complete` \| `partial` \| `refused` | `partial` when ANY selected pack was not evaluated: it failed, its manifest entry was refused or could not be fetched or digest-checked, or no live sandbox let it run (each such case is a finding). `complete` only when every selected pack ran to a result (Copilot's review of `97e28b6c`) |
| `pack_pins` | jsonb, NOT NULL | the run's PACK INVENTORY, with each pack's EXACT pin as the run used it: `{pack_id: {"version", "digest", "commit"}}` for every pack it ran, zero-finding packs and `opendox` itself included (`commit` null for a corpus-relative source; `opendox`'s entry the installed version alone). The baseline compares a pack's pins here, never findings (Copilot's reviews of `6d6911e1` and `6f073ed2`), and `fix` re-runs a pack only at its pin (§ Finding, the patch; Copilot's review of `3f807204`) |
| `export_commit` | 40-hex, NOT NULL | the commit whose committed export the packs read: `commit` for a default-tip or branch run, HEAD at run time for a working-state run (15.1b) |
| `full` | boolean, NOT NULL | true when no `--pack` restricted the run. Only a `complete`, `full` default-tip run forms a baseline or measures disappearances (Copilot review of `2076f24b`) |
| `sandbox` | jsonb, NOT NULL | what the per-run probe found: `{"live": bool, "pids_max": int or null}`; `pids_max` is null where no cgroup is delegated (an accepted limit, contracts/health-packs-manifest.md § Rules) |

The SQL column of the `full` field is `full_run`, because PostgreSQL 16 reserves `full` (the holder, `#656` `6064169640`).

**What a run reads** (R2Q12 (a), which names runs "at the tip, on a branch or
over the working state"; ADV-16 replaced the narrower reading):
- **default-tip**: HEAD is the baseline branch's tip and the working tree is
  clean. Reads that commit. Only these runs form the baseline and measure
  disappearances, and only when `complete` and `full`: a run restricted by
  `--pack`, or `partial` because a selected pack failed or never ran (no live
  sandbox, a refused or unfetchable entry), omits findings it did not look
  for, so it is classed against the baseline but never becomes one and never
  raises a disappearance.
- **branch**: HEAD is another commit and the working tree is clean. Reads that
  commit. Classed against the baseline; never raises a disappearance.
- **working-state**: the working tree differs from HEAD. The product's
  BUILT-IN checks read the working copy (tracked files, and untracked files
  that are not ignored), in process, where they stand; nothing is copied for
  them. Classed against the baseline; never raises a disappearance. Nothing is
  written under `.git/`.

**Packs ALWAYS see the committed export** (15.1b: the engine "exports the
corpus commit into a directory it owns (`git archive <commit> | tar -x`)"):
the commit a default-tip or branch run reads, and HEAD's commit in a
working-state run. No working-copy edit and no untracked file is ever copied to
a pack. The export is built so that `export-subst` and `export-ignore` cannot
steer it (R2Q9 (a) item 5). (Re-check of review round 1: an earlier wording
copied the working copy for every reader.)

### Finding (14.6, 15.2, 15.7, R2Q10 (a), R2Q25 (a); owner T041, T042)

The neutral shape is [`contracts/health-finding.md`](./contracts/health-finding.md)
(openDox-spec schema 1). Table `health_findings`:

| column | rule |
|---|---|
| `run_id` | references `health_runs` |
| `id` | `<pack_id>.<kind>.<h16>` (decision N-13, refined by ADV-07): `<h16>` is the first 16 hex digits of SHA-256 over the canonical JSON (sorted keys, no whitespace) of `{"pack_id", "kind", "path", "identity"}`. `identity` is a POSITION-INDEPENDENT key the family supplies (a link target as written, a pair of paths, a heading key), never a line number. Stable across edits elsewhere in the document and across a reset; unique per run; a valid ref-name component |
| `kind` | the family (`broken-link`, `orphan`, `empty-stub`, …); `health list --json` carries it (R2Q10 (a)) |
| `pack_id` | NOT NULL; `opendox` for the product's own families (15.7, OQ-H15-19) |
| `pack_version` | NOT NULL; the installed version for `opendox` (OQ-H15-18) |
| `path` | corpus-relative; empty for an install-level or pre-run finding |
| `identity` | NOT NULL, as T040's finding schema requires it: the position-independent key the family supplies, or the engine's own for an engine-authored finding (`{category, entry}` for a pathless one, `{collided_id}` for a collision); STORED as canonical sorted-key JSON and emitted by `health list --json` and the HTTP response (the holder, `6018624750`); bounded as openDox-spec's finding schema bounds it, with an engine cap on its serialized size, stricter than the schema's, as for `pack_id` and `kind` (the cap is T041's, the contract module's; T042 stores what T041 bounds) |
| `locator` | DISPLAY ONLY, outside the hash: a line span, a link target as written; never document text |
| `severity` | the neutral severities U-0 spells |
| `resolution_class` | `auto-fix` \| `assisted` \| `human-only` (14.6) |
| `baseline_class` | `new` \| `pack-upgrade` \| `persistent` (R2Q12 (a)); no fourth value (I-2 (a), ruled) |
| `message` | one line, bounded like `evidence` (ADV-27): at most 200 characters, written by the family from its own words; never document text |
| `evidence` | NOT NULL, `{}` when there is nothing to locate (14.5 lists it in every `list --json` finding); locators only, never an excerpt (R2Q25 (a)); a family's own version rides here (OQ-H15-18); a refused patch's `refused_patch` and `reason` (15.2a) |

The finding's `identity` (contracts/health-finding.md) is STORED and EMITTED (the
holder, `6018624750`, reversing the engine-internal refinement of Copilot's
review of `2076f24b`): the engine hashes it into `id` at run time, stores it in
the `identity` column above, and `list --json` and the HTTP response emit it. A
key such as a heading can be document text, so it is bounded as T040's finding
schema bounds it: no key named `excerpt`, `text`, `content` or `quote`, no
number, every string at most 200 characters (R2Q25 (a)). `list`, `fix` and
`accept` still address a finding by `id`, and `fix` re-runs the one pack that
produced it.

There is NO patch column (lane 3's MISLABEL row 31): a patch is document text,
and the store holds no document (14.3; R2Q25 (a)). A pack's patch is validated
at `run` (a refusal is stored as a finding naming `refused_patch` and `reason`,
no text) and RE-OBTAINED at `fix` by re-running that one pack in the sandbox,
then validated again before any branch exists (OQ-H15-20, refined). **The re-run
reproduces the run that found it, or `fix` refuses**: the pack's current
manifest pin must equal the run's `pack_pins` entry, and HEAD the run's
`export_commit`; and the re-run must report the same finding id. Otherwise
`fix` refuses by name, with no branch made, naming the remedy (run `health run`
again and fix the fresh finding), so a changed manifest source, commit or digest
under an unchanged `version`, or a moved HEAD, never runs other code or reads
another tree for an old finding (Copilot's review of `3f807204`). A built-in
family's repair follows the same rule: the installed version equal to the run's
`opendox` entry, and the finding reproduced at HEAD. **`fix` acts only on a
finding of a run over a commit** (default-tip or branch). A working-state run's
finding is refused by name, with no branch made, naming the remedy: commit the
change, run `health run` again, and fix the fresh finding; a draft is never
built from uncommitted content (Copilot's review of `97e28b6c`).

The store refuses a finding with no `pack_id` or `pack_version`
(`test_the_store_refuses_a_finding_without_provenance`) and holds no document
(14.3).

### Baseline classes (R2Q12 (a); owner T046)

```text
for a run R, against B = the latest earlier default-tip run in the store for the
SAME resolved corpus_root and baseline_branch (never another corpus's run) whose
outcome is complete and which is full (no --pack restriction),
with P(B) = B's pack inventory (health_runs.pack_pins):
  id in R, not in B, its pack in P(B) at the same pin       → new
  id in R, not in B, its pack in P(B) at another pin        → pack-upgrade (D12): another version, or
                                                              the same version from another digest or commit
  id in R, not in B, its pack NOT in P(B) (newly added)     → pack-upgrade (it came with a pack change)
  id in R and in B                                          → persistent
only when R is itself a complete, full default-tip run, for id in B, not in R,
and not accepted in the exceptions file R reads (an accepted id is suppressed,
not gone):
     cited → gone: a commit in git rev-list <B.commit>..<R.commit> (every ancestor of R's
            commit not reachable from B's, merges' second parents included) carries a
            "Finding: <id>" trailer naming it. A landed health-fix draft cites this way,
            since the fix loop writes that trailer on every repair commit (§ Fix draft)
     uncited → re-raised ONCE: R carries one engine-authored finding, kind
               uncited-disappearance, identity {"disappeared_id": <id>}, human-only,
               naming the original (contracts/health-finding.md); its id is its own
the re-raise is never itself measured as a disappearance: a later run without it
  raises nothing for it, and the original id is in neither R nor the next run's
  baseline (R), so a third run raises nothing for either
the baseline branch: main, else the branch HEAD names (tier 1 I-2 (a), ruled);
  with none (a detached HEAD and no main) no run is default-tip, so there is no B
no B at all (a first run, or after runtime reset): every finding is new, once
```

### Families: the stub criteria (14.4, 14.6; ADV-17, ADV-40; owner T044)

| kind | criterion (declared in `families.py` and here) | class |
|---|---|---|
| `empty-stub` | after front matter, the body holds no line that is neither blank nor a heading | `assisted` (14.6): the deterministic proposal is a front-matter note `health-note: empty stub; write it or remove it in this draft`, which the human edits |
| `stale-stub` | after front matter, the body holds 1 to 3 such lines, and the last commit that touched the file is older than 180 days at the run's commit | `human-only` (OQ-H-8) |

The 14.9 fixture plants one empty stub (T043) and T044 and T053 test it.

### Exception (14.8, OQ-H-13; owner T054)

An entry of `health/dispositions.yaml` in git, never in the store:
[`contracts/health-exceptions.md`](./contracts/health-exceptions.md) (openDox-spec
schema 3). An accepted finding is suppressed; a run never stores it.

**Which file a run reads** (C4, the spec's edge case at `spec.md:534-536`): the
one in what the run reads. A default-tip or branch run reads the committed file;
a working-state run reads the working tree's, so an uncommitted `accept`
suppresses in a working-state run and in no commit run until it is committed.
F14.1 commits before each run, so it reads the committed file. A reset loses no
exception (SC-006).

### Fix draft (14.7, OQ-12-17; owner T053)

The shape is exactly 14.5's, `health fix --repo-root <corpus> --finding ID
[--batch]` (ADV-11). Without `--batch`, the repair is its own draft,
`health-fix-<id>`, branched at HEAD. With `--batch`, it is added as one more
commit to the open batch draft, `health-fix-batch`, which is created at HEAD
when none is open (or when the last one is already contained in `main`);
several invocations put several repairs in ONE draft for ONE review (14.7).
**An open batch grows only at its base.** An addition needs HEAD to be the
batch's base: HEAD an ancestor of `health-fix-batch`, and every commit in
`HEAD..health-fix-batch` one of the fix loop's repair commits (each carries its
`Finding:` trailer). When HEAD has moved past the base, `fix --batch` refuses
by name, with no commit made, naming the remedies: land the open batch, delete
it, or fix without `--batch`. Git holds the base, so the store records nothing
for it (Copilot's review of `97e28b6c`).
The applier writes each draft in a worktree of its own, so HEAD and the working
tree never move (F14.1 asserts HEAD unmoved after every `fix`). **Every repair
commit carries a `Finding: <id>` trailer** for the finding it repairs, a batch
draft's one per commit, so the citation is durable in git: the baseline reads
the trailers in the commits a landing brought in (§ Baseline classes), never a
branch name, and a deleted draft branch loses nothing (Copilot's review of
`cbe2adfb`). Never `main`; a draft
lands only through `land` (12.6a). A `human-only` finding gets no branch.

## Phase 5: check packs

### Manifest entry (15.1a, R2Q21 (a); owner T047)

[`contracts/health-packs-manifest.md`](./contracts/health-packs-manifest.md)
(openDox-spec schema 2). `health/packs.yaml` is authoritative for what runs.
An entry carries exactly 15.1a's fields: `id`, `version`, `source`, `digest`, and
`commit` for a git-URL source only. A corpus-relative entry that carries a
`commit` is refused (15.1a). Time budgets and bounds are the ENGINE's, never the
corpus's (15.6; lane 3's bwrap-facts FIX).

### Pack declaration (15.2, OQ-H15-10; owner T045)

A static `opendox-pack.yaml` inside the pack, read before any pack code runs:
pack id, version (must equal the manifest entry's; none at all is refused, as
`fixture-anonymous-pack` tests), the families it emits, label keys, and the
protocol version. Forbidden keys (baseline, landing, classes) are refused by
name. **Each family declares 15.2's three parts** (FR-018; Copilot's review of
`55cc1334`):

```yaml
families:
  - kind: heading-case         # the family's id, ^[a-z0-9-]{1,40}$, unique in the pack
    version: "3"               # the family's OWN version, a non-empty string
    applies_to: ["notes/**/*.md", "*.md"]   # corpus-relative globs, at least one
```

A family without all three is refused, and so is the declaration. A finding of
a kind the declaration does not list, or whose `path` matches none of its
family's `applies_to` globs, is refused as a finding against that pack (15.5),
and the engine stamps the declared family version into the finding's
`evidence.family_version`.

### Patch (15.2, 15.2a; owner T049)

A patch is a UNIFIED DIFF, and nothing else (15.2; FR-018; ADV-12).

| field | rule |
|---|---|
| `finding` | the finding it repairs (by the pack's own finding reference, before the engine stamps the id) |
| `diff` | a unified diff against the export the pack saw |

REFUSED, each as a finding against the pack naming `refused_patch` and `reason`,
before any branch exists (15.2a, `tasks.md:3461-3479`):
- it edits a path other than its own finding's `path` (a finding that names no
  document carries no patch);
- it names an absolute path, a path with a `..` component, or a path with a
  `.git` component in any letter case;
- its target is a symbolic link in the corpus, or lies below one;
- it creates, deletes, renames, copies or re-modes a file, or is binary: the
  headers `new file mode`, `deleted file mode`, `rename from`, `copy from`,
  `old mode` and `GIT binary patch`;
- it is larger than 65,536 bytes, the engine's bound, declared by 15.2a and
  never read from the pack.

Only a patch that passes reaches `git apply --check` against the draft branch's
base.

### Sandbox probe and canary (15.1b, 15.6a, OQ-H15-9, OQ-H15-21; owner T048)

| field | rule |
|---|---|
| `bwrap` | the fixed system path, its version, and the flags present (`--json-status-fd`, `--disable-userns`, `--size`) |
| `userns` | whether unprivileged user namespaces are permitted |
| `canary` | per run (product behaviour, so F15.1 stands): the engine sets a CANARY environment variable in its own environment and holds a CANARY descriptor open before spawning (15.6a), then proves inside the sandbox that a write (including after a permission restore), a planted symlink out of the copy, a network connect, a read of `$HOME`, the CANARY variable and the CANARY descriptor through `/proc/self/fd` are ALL unreachable |
| `verdict` | `live` → packs run; otherwise packs do not run, and ONE install-level finding (`pack_id` `opendox`, empty `path`, `human-only`) says why (R2Q16 (a)) |

**What the sandbox binds** (R2Q18 (a); lane 3's T048 FIX): read-only, the
install's interpreter and its standard library, and `opendox.health_contract`
alone; never `site-packages`, `$HOME` or the checkout. `--clearenv` with the
allowlist `PATH`, `LANG`, `PYTHONNOUSERSITE=1` (15.1b). The invocation is
15.1b's in full: `--unshare-all`, `--die-with-parent`, `--new-session`, the
export at `/corpus` and the pack at `/pack`, both `--ro-bind`, a private
`--tmpfs /tmp`, its own `--proc /proc`, a minimal `--dev /dev`; spawned with
`close_fds=True`, stdin from `/dev/null` and two output pipes (T048).

## Relationships

```text
health_runs 1 ── * health_findings          (run_id)
health_findings * ── 0..1 exception          (by id, in git; suppresses)
health_findings * ── 0..1 fix draft branch   (health-fix-<id>, or the open health-fix-batch) ── land ──> Landed
manifest entry 1 ── 1 pack declaration       (version equal)
manifest entry 1 ── * health_findings        (pack_id, pack_version)
a pack's patch: never stored; re-obtained at fix from the run's pack_pins entry at its export_commit
```
