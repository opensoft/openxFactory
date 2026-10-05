# Data model: openDox, the document tool and self-maintenance (release 2)

Status: draft

**Feature**: [`spec.md`](./spec.md) (§ Key Entities) · **Plan**: [`plan.md`](./plan.md)
· **Contracts**: [`contracts/`](./contracts/)

Every entity below is a PROPOSAL until Brett rules the plan (T004). Field names
are the plan's; the three shapes that become openDox-spec schemas (R2Q22 (a))
are fixed in `contracts/`, and this file points there rather than repeating
them. "Owner" names the task that lands the entity.

## Phase 4: submission and landing

### Submission (12.1a; owner T011)

The report requirement 11's third scenario needs, returned by
`SubmissionPort.submit(branch)`.

| field | type | rule |
|---|---|---|
| `branch` | string | the local branch submitted; never `main` (R2Q5 (a)) |
| `remote` | string | always `origin` (OQ-12-12) |
| `destination` | string | the push URL with any userinfo REDACTED; a URL that carries a credential never gets here, because it is refused first (OQ-12-11) |
| `commit` | 40-hex | the branch tip that was pushed |
| `outcome` | `pushed` \| `refused` \| `failed` | |
| `message` | string | redacted, even for a refused or failed push (12.1a) |

`NoSubmissionTarget` (12.3) is the outcome when no `origin` is attached: an
error naming what is missing ("no remote named `origin` is attached; attach
one with …"), never an opaque failure. Several push URLs on `origin` are
refused by name (OQ-12-12).

### Governance (12.6a; R2Q4 (a), R2Q7 (a); owner T012)

`repository_governance()` returns exactly one of three values, fail closed.

| value | when |
|---|---|
| `governed` | a registered host profile declares an instrument (its contributed `SubmissionPort`); this outranks any declaration. Or the declaration at `main`'s tip says `governed` |
| `standalone` | no instrument, and the declaration at `main`'s tip says `standalone` |
| `unknown` | anything else: no `main`; no declaration; an unreadable file; another `kind`; an unknown key or value |

**The declaration** (decision N-1), `.opendox/governance.yaml`, read from the
blob at `main`'s tip (never the working tree):

```yaml
schema_version: 1
kind: opendox-governance
governance: standalone        # or: governed
```

With no declaration, `land` refuses, naming the exact file and content, which
the owner commits with git (R2Q7 (a)); the openDox root's README documents it
(T018).

### Confirmation capability (12.6a; owner T012)

| field | rule |
|---|---|
| `branch` | the branch it confirms |
| `head` | the branch tip at issue time; a moved branch invalidates it |
| `issuer` | `tty` (the `land` prompt over `/dev/tty`) or `view` (a nonce minted by the loopback server for that branch, consumed by the confirm control) |
| `nonce` | for `view`: a server-minted single-use value; for `tty`: none |
| `used` | single-use: a second `land` with the same capability is refused |

No other issuer exists, and a static check proves it (one of F12.2's thirteen
guardrail tests). With no `/dev/tty` and no view, `land` refuses (decision N-11).

### Landed and MergeConflict (12.6a; owner T012)

`LandingPort.land(branch, *, confirmation) -> Landed`.

| `Landed` field | rule |
|---|---|
| `branch` | the landed branch |
| `merge_commit` | the `--no-ff` merge commit made in the lander's own landing worktree |
| `previous_main` | `main` before the merge; `git revert -m 1 <merge_commit>` restores its tree |
| `served_checkout` | `fast-forwarded` (the served checkout held `main` and was clean: `git merge --ff-only <merge_commit>`) or `left` (it did not; the user's `main` ref still moved) |
| `pushed` | always `false`: `land` pushes nothing (R2Q6 (a)) |

`MergeConflict` lists the conflicting paths and names the remedy: bring `main`
into the branch and resolve there (OQ-038-1). Nothing is merged.

### The landing's states

```text
requested
  ├─ refused: governance unknown | governed-without-an-instrument | branch is main
  │           | no or used or stale confirmation | local main lacks the remote's tip (ls-remote)
  ├─ governed with an instrument → submitted through the instrument (Submission), no merge (R2Q4 (a))
  └─ standalone → merged in the landing worktree
        ├─ conflict → MergeConflict, nothing merged, the landing worktree discarded
        └─ merged → served checkout fast-forwarded if clean on main → Landed
              └─ a live session on that branch ends by the existing merge observation (R2Q5 (a))
```

## Phase 5: health

### Health run (14.4; owner T042, T046)

Table `health_runs` in `0003_` (OQ-H-22; DOMAIN, R2Q13 (a)):

| column | type | rule |
|---|---|---|
| `run_id` | uuid | primary key |
| `corpus_root` | text | the corpus's resolved root; no foreign key to `projects` |
| `commit` | 40-hex | the commit read (decision N-10: the committed tree of `HEAD`) |
| `default_tip` | bool | `commit` equals `main`'s tip at run time; only such runs form the baseline (R2Q12 (a)) |
| `dirty_tree` | bool | the working tree had changes, which were not scanned |
| `started_at`, `finished_at` | timestamptz | |
| `outcome` | `complete` \| `partial` \| `refused` | `partial` when a pack failed (its failure is a finding) |

### Finding (14.6, 15.2, 15.7, R2Q10 (a), R2Q25 (a); owner T041, T042)

The neutral shape is [`contracts/health-finding.md`](./contracts/health-finding.md)
(openDox-spec schema 1). Table `health_findings`:

| column | rule |
|---|---|
| `run_id` | references `health_runs` |
| `id` | `<pack_id>.<family>.<h16>`: `<h16>` is the first 16 hex digits of SHA-256 over the pack id, family, document path and family-supplied locator. Stable across a reset, unique per run, a valid ref-name component (decision N-13) |
| `kind` | the family (`broken-link`, `orphan`, …); `health list --json` carries it (R2Q10 (a)) |
| `pack_id` | NOT NULL; `opendox` for the product's own families (15.7, OQ-H15-19) |
| `pack_version` | NOT NULL; the installed version for `opendox` (OQ-H15-18) |
| `path` | corpus-relative; empty for an install-level or pre-run finding |
| `locator` | a family-supplied position (line span, link target); never document text |
| `severity` | the neutral severities U-0 spells |
| `resolution_class` | `auto-fix` \| `assisted` \| `human-only` (14.6) |
| `baseline_class` | `new` \| `pack-upgrade` \| `persistent` \| `unclassed` (R2Q12 (a); `unclassed` only with no `main`, interplay I-2) |
| `evidence` | locators only, never an excerpt (R2Q25 (a)); a family's own version rides here (OQ-H15-18) |
| `patch` | nullable; a pack's patch stored at `run`, validated at `run` and again at `fix` (OQ-H15-20) |

The store refuses a finding with no `pack_id` or `pack_version`
(`test_the_store_refuses_a_finding_without_provenance`) and holds no document
(14.3).

### Baseline classes (R2Q12 (a); owner T046)

```text
for a run R on main's tip, against B = the previous default-tip run in the store:
  id in R, not in B, pack_version unchanged        → new
  id in R, not in B, its pack's version changed     → pack-upgrade (D12)
  id in R and in B                                  → persistent
  id in B, not in R:
     cited (a landed health-fix draft, or a commit with a "Finding: <id>" trailer) → gone
     uncited → re-raised ONCE as human-only
for a run on any other commit: classes against B; no disappearance is measured
no main: every finding unclassed, plus one install-level no-default-branch finding (I-2)
after runtime reset: B is gone; the next default-tip run is the new baseline
```

### Exception (14.8, OQ-H-13; owner T054)

An entry of `health/dispositions.yaml` in git, never in the store:
[`contracts/health-exceptions.md`](./contracts/health-exceptions.md) (openDox-spec
schema 3). An accepted finding is suppressed; a run never stores it. Who and
when are git's (author, commit). A reset loses none (SC-006).

### Fix draft (14.7, OQ-12-17; owner T053)

A fix writes a DRAFT ON A BRANCH, `health-fix-<id>` (one finding) or
`health-fix-batch-<h16>` (several, `<h16>` over the sorted ids), never `main`;
it lands only through `land` (12.6a). `human-only` findings get no branch.

## Phase 5: check packs

### Manifest entry (15.1a, R2Q21 (a); owner T047)

[`contracts/health-packs-manifest.md`](./contracts/health-packs-manifest.md)
(openDox-spec schema 2). `health/packs.yaml` is authoritative for what runs.

### Pack declaration (15.2, OQ-H15-10; owner T045)

A static `opendox-pack.yaml` inside the pack, read before any pack code runs:
pack id, version (must equal the manifest entry's), the families it emits,
label keys, and the protocol version. Forbidden keys (baseline, landing,
classes) are refused by name.

### Patch (15.2a; owner T049)

| field | rule |
|---|---|
| `finding_id` | the finding it repairs |
| `path` | must equal the finding's `path`: a patch touches only its finding's own document |
| `base_blob` | the blob the patch was computed against; a mismatch at `fix` is refused |
| `content` | the replacement document text, or a unified diff over `base_blob` |

The engine validates every patch BEFORE any branch exists (15.2a); a pack's
`auto-fix` class is honoured only for a patch that validates.

### Sandbox probe and canary (15.1b, OQ-H15-9, OQ-H15-21; owner T048)

| field | rule |
|---|---|
| `bwrap` | the fixed system path, its version, and the three flags present |
| `userns` | whether unprivileged user namespaces are permitted |
| `canary` | per run: a self-check that a write, a network connect and a read outside the export all FAIL inside the sandbox |
| `verdict` | `live` → packs run; otherwise packs do not run, and ONE install-level finding (`pack_id` `opendox`, empty `path`, `human-only`) says why (R2Q16 (a)) |

## Relationships

```text
health_runs 1 ── * health_findings          (run_id)
health_findings * ── 0..1 exception          (by id, in git; suppresses)
health_findings 1 ── 0..1 patch              (stored at run)
health_findings * ── 0..1 fix draft branch   (health-fix-<id> / -batch-<h16>) ── land ──> Landed
manifest entry 1 ── 1 pack declaration       (version equal)
manifest entry 1 ── * health_findings        (pack_id, pack_version)
```
