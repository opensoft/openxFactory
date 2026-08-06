# Design: The openDox Project-First Header

## Context

Brett's 2026-08-06 header round (topic decisions D12–D15) reorganizes the
header around the CURRENT PROJECT. Exit 1's scoping machinery (picker,
register projection route, pending plane, create-project commission) is
the substrate; this change re-skins its surface and adds one verb.

## Decisions

### D12 (topic) — "Opensoft openDox"
Brand line and `<title>`. The repo chip retires: the freshness header
already answers "which repo, which revision" (`repo @ ref · sha · date`),
and the chip duplicated the select beside it — half of the reported
confusion.

### D13 (topic) — Always in a project
The dropdown's rows: "New Project", then the register's projects (pending
commissions keep their disabled entries). Selection default: the stored
scope when the projection still names it, else the FIRST register project.
The stored-scope discipline is unchanged (membership-checked third-party
data). "New Project" is a row, not a selection: choosing it opens the
create form and restores the previous selection — a dropdown line that
ACTS is acceptable here because it is the first line, Brett's explicit
placement.

### D14 (topic) — The filter replaces the select
One icon, one popover: the current project's members, single-select; the
active repository highlights; choosing another stores the key and reloads
(the ratified selector posture). "All repositories" renders first,
disabled with "(merged view: pending exit 2)" until the merged-projection
change realizes, at which point it selects the project's derived
aggregate. Repositories the index cannot serve render with their
unavailable reason exactly as the old select did.

### D15 (topic) — edit-project is a commission
The same mechanic as create-project, one verb over: target `project_id`
(existing project), payload `add`/`remove` member lists (either may be
empty, not both), workflow `project-register-edit`. Guards in ruled
order: human gate → project existence in the register projection →
additions in the roster-or-register universe → removals currently members
→ the at-least-one-member floor (the schema's `minItems: 1`, enforced at
commission so the fulfilment never authors an invalid register) →
duplicate via the shared (verb, target) index. Manage mode renders a
checkbox per register repository seeded from current membership; applying
diffs into add/remove. Pending edits badge the affected rows until the
fulfilment lands (the D-e two-plane posture, reused).

### D-g — One duplicate key for both project verbs
`create-project` and `edit-project` share the `project_id` target key, so
the shared undelivered-commission index scopes duplicates PER VERB
(FR-027's rule): an undelivered create does not block an edit of a
different project, and an undelivered edit blocks only a second edit of
the same project.

### D-h — The filter works like the dropdown (Brett's 2026-08-06 annotation)
Ruled through the vibe-annotate channel after the first realization pass:
"repo filter can work the same as the project dropdown. first line can be
add new repo. on the left we can have eyeball that shows if the repo is
visible in the view. on the right have trash can delete icon to remove the
repo from the project." Manage mode retires; in its place: the popover's
FIRST line is "＋ add repository…" (an inline candidate select over the
known-repository universe minus current members, commissioning a
single-addition edit), each member row carries an EYEBALL on the left
(visible = the active single-repo view, or any member under the project's
own merged view) and a TRASH control on the right whose first click ARMS
and second click commissions the single-removal edit — a register edit
never rides a stray click. Same engine verb, same pending badges; gate off,
the add line and trash controls are absent and rows stay selectable.
Recorded as topic decision D16.

## Risks / Trade-offs

- **A dropdown row that acts (New Project)** can surprise keyboard users;
  mitigated by restoring the previous selection on close and labelling the
  row unambiguously.
- **Manage mode's checkbox diff can race the register** (a fulfilment
  landing mid-edit); the engine revalidates against the live projection at
  commission time and refuses cleanly, the same posture as every other
  guard.

## Open Questions

None — D12–D15 ruled 2026-08-06; D-g is derivational.
