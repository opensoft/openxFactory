# Contract: `health`, CLI and HTTP

Status: draft

**Feature**: 038 · **Authority**: boxes 6.2, 14.4–14.8, 15.1a, 15.4–15.6;
answers R2Q9 (a) items 2 and 7, R2Q10 (a), R2Q12 (a), R2Q15 (a), R2Q16 (a).
**A PROPOSAL until Brett rules the plan** (OQ-H-2, -3, -14, -18; OQ-H15-14;
decisions N-2, N-10; tier 2's OQ-H-18 reading). Review round 1 restored 14.5's
exact shapes (ADV-11).

`health`, its routes and its capability block are contributions of openDox's
DEFAULT profile (decision N-2; ADV-14). Every action the view offers has a CLI
verb and every CLI verb is offered by the view (14.5; the three named tests of
`tests/test_health_parity.py`).

## CLI: 14.5's table, exactly, plus `--local` and one additive option

```text
opendox health run    --repo-root <corpus> [--pack ID] [--timeout SECONDS] [--local]
opendox health list   --repo-root <corpus> [--json] [--class new|pack-upgrade|persistent] [--local]
opendox health fix    --repo-root <corpus> --finding ID [--batch] [--local]
opendox health accept --repo-root <corpus> --finding ID --reason TEXT [--local]
```

Options follow the verb (10.1). `--class` is additive (a filter on `list`);
`--local` is R2Q9 (a) item 7's, refused only where it disagrees with
`OPENDOX_INSTALL_MODE`, naming both.

- **`run`** reads what the run's kind reads (data-model.md § Health run:
  default-tip, branch or working-state; R2Q12 (a)), runs the built-in families
  in process (attributed `opendox`) and every manifest-listed pack in the
  sandbox (R2Q16 (a)), stores the run and its findings, and classes them
  against the baseline. `--pack` restricts to listed packs. `--timeout` sets the
  per-pack budget: default 60 seconds, applied per pack and enforced by the
  engine, never by the pack, and capped at the engine's ceiling of 600 seconds
  (15.6; ADV-40; the manifest carries no budget of its own). `run` writes nothing
  to the working tree or under `.git/` (F15.1 asserts the checkout clean after
  it).
- **`list`** prints the last run's findings, new first; `--json` emits one object
  per finding with at least 14.5's fields (`id`, `resolution_class`, `path`,
  `severity`, `evidence`, `pack_id`, `pack_version`), plus `kind` (R2Q10 (a)) and
  `baseline_class`, in `contracts/health-finding.md`'s shape.
- **`fix`** writes a DRAFT ON A BRANCH and never `main`: `health-fix-<id>`, or,
  with `--batch`, one more commit on the open batch draft `health-fix-batch`
  (data-model.md § Fix draft). `auto-fix` applies the family's repair or the
  pack's re-obtained and re-validated patch; `assisted` writes the deterministic
  proposal; a `human-only` finding is refused with no branch made (14.6, 14.7;
  F14.1). The draft lands only through `land`.
- **`accept`** writes one entry to `health/dispositions.yaml`
  (`contracts/health-exceptions.md`).
- F14.1 and F15.1 first start the document server, as F13.1 does, and the
  `health` verbs reach the running bundle (R2Q9 (a) item 2).
- **The hosted plane** refuses all four verbs by name and records nothing; the
  schema still migrates (R2Q15 (a)).
- **On commit** (tier 2's OQ-H-18 reading): "optionally on commit" means a hook
  line the user may add, `opendox health run --repo-root .`, which the root
  README documents; the product writes nothing under `.git/`.

## HTTP routes (loopback server; 12.4a's gate and the console token on every action)

| method and path | answer |
|---|---|
| `GET /health/findings` | the last run's findings, new first (`?class=` filters) |
| `POST /actions/health/run` | starts a run; answers the run's id and outcome |
| `POST /actions/health/fix` | `{"finding": "<id>", "batch": false}` → the draft branch's name |
| `POST /actions/health/accept` | `{"finding": "<id>", "reason": "…"}` → the entry written |
| landing a draft | the land routes of `contracts/cli-http-submit-land.md` |

## `/capabilities`: the `health` block

Present only where openDox's default profile contributes the health routes
(derived from the route bindings, as `gate` is; ADV-14). It lists every
resolution action the view offers, as data, so parity is a comparison (14.5):

```json
{"health": {"available": true, "plane": "local", "packs": "live",
            "actions": ["run", "list", "fix", "fix-batch", "accept", "land"]}}
```

`available` is `false` on the hosted plane. `packs` is `live` where the sandbox
probe passed, else `none` (and one install-level finding says why).

## The scoped seam (Group 6)

openDox's own check, the engine's built-in families, is registered at the
existing scoped seam (`workbench.register_health_check`, `workbench.py:1622`;
`run_scoped_doc_health`, `:1666`) ONLY when the seam is empty, and a host's
check, registered through the same call, REPLACES it: the host's check wins,
in process and unstored (R2Q16 (a); ADV-18). Both registration orders are
tested (T052). With no families named, the scoped action asks for the
registered check's own default scoped families (OQ-H-2). A scoped run is not
stored (OQ-H-3).
