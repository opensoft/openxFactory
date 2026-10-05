# Contract: `health`, CLI and HTTP

Status: draft

**Feature**: 038 · **Authority**: boxes 6.2, 14.4–14.8, 15.1a, 15.4–15.6;
answers R2Q9 (a) items 2 and 7, R2Q10 (a), R2Q12 (a), R2Q15 (a), R2Q16 (a).
**A PROPOSAL until Brett rules the plan** (OQ-H-2, -3, -14, -18; OQ-H15-14;
decisions N-2, N-10).

`health` is a contribution of openDox's DEFAULT profile (decision N-2). Every
action the view offers has a CLI verb and every CLI verb is offered by the view
(14.5; the three named tests of `tests/test_health_parity.py`).

## CLI

```text
opendox health run    [--repo-root PATH] [--local] [--pack ID]... [--timeout SECONDS]
opendox health list   [--repo-root PATH] [--local] [--json] [--class new|pack-upgrade|persistent|unclassed]
opendox health fix    [--repo-root PATH] [--local] --finding ID [--finding ID]...
opendox health accept [--repo-root PATH] [--local] --finding ID --reason TEXT
```

- **`run`** reads the committed tree of `HEAD` (decision N-10), runs the built-in
  families in process (attributed `opendox`) and every manifest-listed pack in
  the sandbox (R2Q16 (a)), stores the run and its findings, and classes them
  against the baseline (R2Q12 (a)). `--pack` restricts to listed packs;
  `--timeout` overrides the manifest default (15.6). On demand only; the root
  README documents an optional hook line, `opendox health run --repo-root .`, and
  the product writes nothing under `.git/` (OQ-H-18).
- **`list`** prints the last run's findings, new first; `--json` emits an array
  in `contracts/health-finding.md`'s shape, `kind` included (R2Q10 (a)).
- **`fix`** writes a DRAFT ON A BRANCH (`health-fix-<id>`, or one batch branch
  for several ids) and never `main`; `auto-fix` applies the family's or the
  pack's validated patch, `assisted` writes the deterministic proposal, and a
  `human-only` finding is refused with no branch made (14.6, 14.7; F14.1). The
  draft lands only through `land`.
- **`accept`** writes one entry to `health/dispositions.yaml`
  (`contracts/health-exceptions.md`).
- `--local` on every verb (R2Q9 (a) item 7). F14.1 and F15.1 first start the
  document server, as F13.1 does (R2Q9 (a) item 2).
- **The hosted plane** refuses all four verbs by name and records nothing; the
  schema still migrates (R2Q15 (a)).

## HTTP routes (loopback server; 12.4a's gate and the console token on every action)

| method and path | answer |
|---|---|
| `GET /health/findings` | the last run's findings, new first (`?class=` filters) |
| `POST /actions/health/run` | starts a run; answers the run's id and outcome |
| `POST /actions/health/fix` | `{"findings": ["<id>", …]}` → the draft branch's name |
| `POST /actions/health/accept` | `{"finding": "<id>", "reason": "…"}` → the entry written |
| landing a draft | the land routes of `contracts/cli-http-submit-land.md` |

## `/capabilities`: the `health` block

```json
{"health": {"available": true, "plane": "local", "packs": "live"}}
```

`available` is `false` on the hosted plane. `packs` is `live` where the sandbox
probe passed, else `none` (and one install-level finding says why).

## The scoped seam (Group 6)

openDox registers the engine's built-in families at the existing scoped seam
(`run_scoped_doc_health`); with no families named, the action asks for the
registered check's default scoped families (OQ-H-2, OQ-H-3). A scoped run is
not stored. A host's check registered through `register_health_check` runs in
process at that seam only, never stored (R2Q16 (a)).
