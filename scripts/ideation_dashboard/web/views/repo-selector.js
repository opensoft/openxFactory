// Repository selector + refresh affordance (add-dashboard-repo-selector tasks
// 3.2/3.6, and Brett's 2026-07-26 open-question rulings). The header control
// that switches the ACTIVE (repository, ref) snapshot and asks the serving side
// for fresher data.
//
// TWO same-origin backend routes, both answered by serve.py and both absent from
// a static image (which is exactly how the whole control degrades away):
//   GET  /snapshot-index.json  — the roster + per-entry freshness
//   POST /actions/refresh      — ONE affordance, the BINDING chosen by the plane
//                                (served: re-fetch; local: regenerate)
// The bundle NEVER addresses the external data source: the serving side performs
// that fetch (design D5), so the grep-proven no-external-URL boundary in
// tests/ideation-dashboard/test_renderer.py survives this change unedited.
//
// PASSIVE FRESHNESS HINT (ruling on open question 2): a background poll of the
// THIN index every POLL_INTERVAL_MS shows a "newer data available" badge when
// the source advertises a newer snapshot than the one loaded. It NEVER reloads
// by itself — the viewer clicks refresh. The poll re-uses the same index fetch,
// so no new data path appears.
//
// DOM-SAFETY: every dynamic value binds through textContent; innerHTML is never
// assigned here.

import {
  addableRepositories, buildPendingEdits, buildPendingProjects, buildProjects,
  buildRoster, defaultProjectScope, freshnessLabel, hintLabel, keyId,
  KIND_REPOSITORY, netPendingEdit, newerAvailable, projectFilterRows,
  repositoryVisible, sameKey, staleNotice, toggleVisibility,
  visibleRepositories,
} from "./repo-selector-model.js";
import { VIEW_SHARED, VIEW_UNION } from "./composed-model.js";

export const SNAPSHOT_INDEX_ROUTE = "/snapshot-index.json";
export const ACTIONS_REFRESH_ROUTE = "/actions/refresh";
// add-project-scoped-selection: the register projection the project picker
// reads, and the create-project commission route. Both degrade away exactly
// like the index: a static image 404s them and the selector renders unscoped.
export const PROJECT_REGISTER_PROJECTION_ROUTE = "/project-register.json";
export const ACTIONS_CREATE_PROJECT_ROUTE = "/actions/gate/create-project";
// add-opendox-project-header (D15/D16): the membership-edit commission route
// the filter popover's add line and trash controls POST to. Same degrade
// contract as its siblings.
export const ACTIONS_EDIT_PROJECT_ROUTE = "/actions/gate/edit-project";
// add-register-edit-lane: the apply button's route — the serve runs the
// fulfilment lane once (loopback + gate only).
export const ACTIONS_APPLY_REGISTER_EDITS_ROUTE = "/actions/apply-register-edits";
// The viewer's project scope survives the reload a selection triggers. It is
// THIRD-PARTY DATA on the way back in: it only ever filters client-side
// (membership-checked against the loaded projection) and never reaches a URL.
export const PROJECT_SCOPE_STORAGE_KEY = "xfDashProjectScope";
// D19: the per-project visible set + view mode (see `storedViewState`).
export const VIEW_STATE_STORAGE_KEY = "xfDashProjectView";
// ~5 minutes: the ruled cadence. Slow enough that the serving side's own peek
// cache absorbs N viewers, fast enough that "did my doc land?" answers itself
// while the tab is open.
export const POLL_INTERVAL_MS = 300000;

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

// Fetch the snapshot index. ANY failure (a static image 404s this route, an old
// server does not know it, file:// throws) resolves to null — the caller then
// renders exactly today's single-snapshot dashboard. Never throws.
export async function fetchIndex(injectedFetch) {
  try {
    const response = injectedFetch
      ? await injectedFetch(SNAPSHOT_INDEX_ROUTE, { cache: "no-store" })
      : await fetch(SNAPSHOT_INDEX_ROUTE, { cache: "no-store" });
    if (!response?.ok) return null;
    return await response.json();
  } catch {
    return null;
  }
}

// POST the refresh. Resolves to the backend's freshness result, or throws an
// Error carrying the backend's fixed message — the caller reports it INLINE and
// keeps the currently rendered snapshot (spec scenario "A refresh fails").
export async function postRefresh(body, injectedFetch) {
  const opts = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  };
  const response = injectedFetch
    ? await injectedFetch(ACTIONS_REFRESH_ROUTE, opts)
    : await fetch(ACTIONS_REFRESH_ROUTE, opts);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data?.message || data?.error || ("HTTP " + response.status));
  return data;
}

// Fetch the register projection. Same degrade contract as `fetchIndex`: any
// failure resolves to null and the picker simply does not render.
export async function fetchProjects(injectedFetch) {
  try {
    const response = injectedFetch
      ? await injectedFetch(PROJECT_REGISTER_PROJECTION_ROUTE, { cache: "no-store" })
      : await fetch(PROJECT_REGISTER_PROJECTION_ROUTE, { cache: "no-store" });
    if (!response?.ok) return null;
    return await response.json();
  } catch {
    return null;
  }
}

export function storedProjectScope(storage) {
  try {
    return (storage || window.sessionStorage).getItem(PROJECT_SCOPE_STORAGE_KEY) || null;
  } catch {
    return null;
  }
}

export function storeProjectScope(id, storage) {
  try {
    const store = storage || window.sessionStorage;
    if (id) store.setItem(PROJECT_SCOPE_STORAGE_KEY, id);
    else store.removeItem(PROJECT_SCOPE_STORAGE_KEY);
  } catch { /* storage denied: the scope is simply session-transient */ }
}

// D19 — the per-project VISIBLE set and view mode, one stored document:
// `{ "<project>": { "visible": [...], "mode": "union" } }`. Read defensively:
// any malformed value degrades to "nothing stored", which means every member
// under union — the composition's own default.
export function storedViewState(storage) {
  try {
    const raw = (storage || window.sessionStorage)
      .getItem(VIEW_STATE_STORAGE_KEY);
    const doc = raw ? JSON.parse(raw) : null;
    return doc && typeof doc === "object" && !Array.isArray(doc) ? doc : {};
  } catch {
    return {};
  }
}

export function storeViewState(projectId, state, storage) {
  if (!projectId) return;
  try {
    const store = storage || window.sessionStorage;
    const doc = storedViewState(store);
    doc[String(projectId)] = state;
    store.setItem(VIEW_STATE_STORAGE_KEY, JSON.stringify(doc));
  } catch { /* storage denied: the view is simply session-transient */ }
}

// The stored set/mode for one project, resolved against its CURRENT members.
//
// `active` reconciles the set with what is ACTUALLY SERVED: whenever the
// served snapshot is a single member repository — a project switch, an
// "open in <repo>" jump, a first-ever load — the visible set IS that
// repository, whatever was stored. The ticks describe the view rather than
// contradicting it, and no reload is needed to make them agree. When the
// aggregate is served, the stored set governs.
export function projectViewState(project, storage, active) {
  const doc = storedViewState(storage);
  const visibility = {};
  for (const [id, entry] of Object.entries(doc)) {
    if (entry && Array.isArray(entry.visible)) visibility[id] = entry.visible;
  }
  const stored = doc[String(project?.id)] || {};
  const members = (project?.repositories || []).map(String);
  const served = active && String(active.repository);
  const single = served && served !== String(project?.id)
    && members.includes(served);
  return {
    visible: single ? [served] : visibleRepositories(project, visibility),
    mode: stored.mode === VIEW_SHARED ? VIEW_SHARED : VIEW_UNION,
  };
}

export function refreshCapable(caps) {
  return caps?.actions?.refresh === true;
}

export function gateCapable(caps) {
  return caps?.actions?.gate === true;
}

export function refreshBinding(caps) {
  return caps?.refresh?.binding || null;
}

// The create-project affordance (add-project-scoped-selection): a COMMISSION,
// never a write — the POST records a project-register-edit descriptor + gate
// record and the aggregation-owned register is edited only by the fulfilment.
// Mounted only under the gate capability WITH a served register projection.
// Member candidates are ALL roster repositories: membership is multi-parent
// (Brett's 2026-08-06 ruling), so a repository already in a project is a
// legal member of a new one — projects are named views, not owners.
// Refusals render textContent-only; a successful commission retires the
// form for the session (the engine's duplicate guard is the backstop).
//
// REHOMED by add-opendox-project-header (D13): no standalone button — the
// project dropdown's "New Project" line opens the form through the returned
// opener.
function mountCreateProject(wrap, status, roster, projects, o, addPendingOption) {
  const seen = new Set();
  const candidates = [];
  for (const option of roster) {
    if (option.kind !== "repository") continue;
    if (seen.has(option.repository)) continue;
    seen.add(option.repository);
    candidates.push(option.repository);
  }

  // A LABELED PANEL, not a bare strip (Brett's 2026-08-06 annotation: "which
  // is this? i do not know how to use this widget") — a heading names the
  // act, the field and the member list carry captions, and the buttons say
  // what happens (a recorded commission, not a direct write).
  const form = el("span", "projectform projectpanel");
  form.hidden = true;
  form.appendChild(el("span", "panelhead", "New Project"));
  form.appendChild(el("span", "panelnote",
    "records a project-register commission — the project appears as pending "
    + "until a session fulfils it"));

  const nameField = el("label", "panelfield");
  nameField.appendChild(el("span", "panellabel", "project name"));
  const name = el("input", "projectname");
  name.type = "text";
  name.placeholder = "e.g. Field Pilots";
  name.setAttribute("aria-label", "new project name");
  nameField.appendChild(name);
  form.appendChild(nameField);

  form.appendChild(el("span", "panellabel", "member repositories"));
  const memberList = el("span", "panelmembers");
  const boxes = [];
  for (const repo of candidates) {
    const label = el("label", "projectmember");
    const box = el("input");
    box.type = "checkbox";
    box.value = repo;
    label.appendChild(box);
    label.appendChild(el("span", null, repo));
    boxes.push(box);
    memberList.appendChild(label);
  }
  if (!candidates.length) {
    memberList.appendChild(el("span", "projectform-note",
      "no published repositories to choose from"));
  }
  memberList.appendChild(el("span", "projectform-note",
    "optional — an empty project is fine; add repositories later from the "
    + "filter"));
  form.appendChild(memberList);

  const buttonRow = el("span", "panelbuttons");
  const submit = el("button", "repobtn", "commission project");
  submit.type = "button";
  buttonRow.appendChild(submit);
  const cancel = el("button", "repobtn projectcancel", "cancel");
  cancel.type = "button";
  cancel.addEventListener("click", () => { form.hidden = true; });
  buttonRow.appendChild(cancel);
  form.appendChild(buttonRow);

  submit.addEventListener("click", async () => {
    const members = boxes.filter((b) => b.checked).map((b) => b.value);
    status.textContent = "";
    submit.disabled = true;
    try {
      const opts = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name.value, repositories: members }),
      };
      const response = o.fetcher
        ? await o.fetcher(ACTIONS_CREATE_PROJECT_ROUTE, opts)
        : await fetch(ACTIONS_CREATE_PROJECT_ROUTE, opts);
      const data = await response.json().catch(() => ({}));
      if (!response.ok || data?.ok !== true) {
        submit.disabled = false;
        status.textContent = "create-project refused: "
          + (data?.message || data?.error || ("HTTP " + response.status));
        return;
      }
      form.hidden = true;                   // retired for the session
      status.textContent = "project-register edit recorded (" + data.job + ")";
      // the commission appears in the dropdown immediately as a pending entry
      // (D-e) — the register itself changes only when the fulfilment lands
      if (addPendingOption) addPendingOption(name.value || data.project_id);
    } catch (err) {
      submit.disabled = false;
      status.textContent = "create-project failed: " + (err?.message || "error");
    }
  });

  wrap.appendChild(form);
  return () => {                             // the "New Project…" opener (D13)
    form.hidden = false;
    name.focus();
  };
}

// The repo FILTER (add-opendox-project-header D14/D16): one icon, one
// popover scoped to the CURRENT project, working like the project dropdown
// (Brett's 2026-08-06 header annotation): the FIRST line adds a repository
// to the project, then the all-repos line, then one row per member — an
// EYEBALL on the left saying whether that repository is visible in the
// current view, the repository name (click = serve it), and a TRASH control
// on the right that commissions its removal (two-click, so a stray click
// arms rather than acts). Add and remove are edit-project COMMISSIONS —
// recorded, register untouched until fulfilment — and pending membership
// edits badge their rows (the D-e two-plane posture). Gate off, the add
// line and the trash controls are absent and the rows stay selectable.
// DOM-safety: textContent only, throughout.
function mountProjectFilter(project, roster, pendingEdits, opts) {
  const holder = el("span", "repofilter");
  if (!project) return holder;
  const o = opts || {};
  const gated = gateCapable(o.caps);
  // reread per render: a same-page commission appends to `pendingEdits`,
  // and edits QUEUE (topic D18) — the overlay is the NET of every queued row
  const currentPendingEdit = () => netPendingEdit(pendingEdits, project);

  // D19 — the visible set drives the view: `applyView` is the ONE writer, and
  // it persists then reloads, exactly the ratified reload-per-switch posture
  // every other selector gesture already uses.
  const visible = (o.visible || []).map(String);
  const applyView = (nextVisible, nextMode) =>
    o.onView?.({ visible: nextVisible.map(String), mode: nextMode });
  // The project's DERIVED aggregate, when the plane can compose one: its
  // presence is what makes a multi-repository view possible at all, so it
  // decides whether the rows below are visibility toggles or the pre-D19
  // single-select list.
  const aggregateOption = (projectFilterRows(roster, project)
    .find((r) => r.kind === "all") || {}).option || null;

  // The box names its content (Brett's 2026-08-06 annotation): a
  // single-member project shows THAT repository's name; several show the
  // count — now the VISIBLE count against the total (D19), so the header
  // states the view without opening the popover.
  const members = project.repositories || [];
  const boxLabel = members.length === 1 ? members[0]
    : (visible.length === members.length
        ? members.length + " Repos"
        : visible.length + " of " + members.length + " Repos");
  const button = el("button", "repobtn filterbtn", "\u29e9 " + boxLabel);
  button.type = "button";
  button.title = "repositories in " + project.name;
  button.setAttribute("aria-label", "repository filter for " + project.name);
  button.setAttribute("aria-expanded", "false");
  const pop = el("span", "filterpop");
  pop.hidden = true;
  button.addEventListener("click", () => {
    pop.hidden = !pop.hidden;
    button.setAttribute("aria-expanded", pop.hidden ? "false" : "true");
  });

  async function commissionEdit(body, control, restore) {
    o.status.textContent = "";
    try {
      const fetchOpts = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project_id: project.id, ...body }),
      };
      const response = o.fetcher
        ? await o.fetcher(ACTIONS_EDIT_PROJECT_ROUTE, fetchOpts)
        : await fetch(ACTIONS_EDIT_PROJECT_ROUTE, fetchOpts);
      const data = await response.json().catch(() => ({}));
      if (!response.ok || data?.ok !== true) {
        if (restore) restore();
        o.status.textContent = "edit-project refused: "
          + (data?.message || data?.error || ("HTTP " + response.status));
        return;
      }
      o.status.textContent = "membership edit recorded (" + data.job + ")";
      // badge immediately (D-e): re-render with this edit pending
      pendingEdits = (pendingEdits || []).concat([{
        projectId: project.id, add: data.add, remove: data.remove }]);
      renderRows();
    } catch (err) {
      if (restore) restore();
      o.status.textContent = "edit-project failed: " + (err?.message || "error");
    }
  }

  // D16's first line, refined by Brett's 2026-08-06 annotation: ONE dropdown
  // that closes like the project selector. The placeholder line IS the
  // affordance; choosing a candidate commissions the single addition and the
  // native select closes itself, the placeholder restoring immediately.
  function mountAddRow(pendingEdit) {
    const candidates = addableRepositories(roster, o.projects, project)
      .filter((r) => !(pendingEdit && pendingEdit.add.includes(r)));
    const select = el("select", "repopick filteraddselect");
    select.setAttribute("aria-label", "add a repository to " + project.name);
    const placeholder = el("option", null,
      candidates.length ? "\uff0b add repository\u2026"
                        : "\uff0b add repository\u2026 (none available)");
    placeholder.value = "";
    select.appendChild(placeholder);
    for (const repository of candidates) {
      const opt = el("option", null, repository);
      opt.value = repository;
      select.appendChild(opt);
    }
    select.disabled = !candidates.length;
    select.addEventListener("change", () => {
      const chosen = select.value;
      select.value = "";                  // the placeholder line returns
      if (chosen) commissionEdit({ add: [chosen] }, select, null);
    });
    pop.appendChild(select);
  }

  // D19 \u2014 the VIEW ROW: what the wheels currently span. Union/shared is one
  // toggle, "all"/"none" are the two bulk moves, and the count states the
  // set \u2014 which together cover every selection the old all-repos line and the
  // single-select click used to cover separately.
  // A LIVE BRANCH SESSION, addressable (Brett, 2026-08-10: "how do I get to the
  // rest of the workbench on this doc?"). The serving index advertises a live
  // session as an ordinary `(repository, ref)` row (FR-014) and the roster has
  // carried it all along — nothing here asks the server anything new. What was
  // missing was a way to NAME it: the repository row picked an arbitrary ref, so
  // the only way onto a session branch was to land on it unknowingly.
  //
  // Selecting one keys the whole dashboard to that branch, which is what the
  // runbook's §4 has always described, and the freshness header then names the
  // ref. It is deliberately a plain select, not a filter tick: a session is a
  // different VIEW of one repository, never a member of the merged view.
  function mountSessionRow(row) {
    const line = el("span", "filterline filtersessionline");
    const entry = el("button", "filterrow filtersession", "⎇ " + row.ref);
    entry.type = "button";
    entry.title = "read " + row.repository + " on its live session branch "
      + row.ref + " — the documents this session has created or rewritten, "
      + "which main does not carry";
    entry.addEventListener("click", () => o.onSelect?.({
      repository: row.option.repository, ref: row.option.ref }));
    line.appendChild(entry);
    line.appendChild(el("span", "filtersessionnote", "live session"));
    pop.appendChild(line);
  }

  function mountViewRow(aggregate) {
    const members = (project.repositories || []).map(String);
    const line = el("span", "filterline filterviewline");
    if (!aggregate) {
      // No derived aggregate (no member publishes a snapshot): nothing can be
      // composed, so the view row states that and the rows below stay
      // single-select exactly as they were.
      const note = el("span", "filterrow filterall",
        "\u229e all repositories in " + project.name
        + " (merged view unavailable \u2014 no member snapshot is published)");
      note.setAttribute("aria-disabled", "true");
      line.appendChild(note);
      pop.appendChild(line);
      return;
    }
    const sharing = o.viewMode === VIEW_SHARED;
    // NOT a `filterrow`: rows are member repositories, and conflating the
    // mode control with them makes both the styling and the DOM ambiguous.
    const mode = el("button", "filtermode", sharing ? "\u2229 shared" : "\u222a union");
    mode.type = "button";
    mode.title = sharing
      ? "showing only what TWO OR MORE visible repositories carry "
        + "\u2014 click for the union"
      : "showing everything from every visible repository "
        + "\u2014 click for what two or more of them share";
    mode.disabled = visible.length < 2;      // one repository: same either way
    mode.addEventListener("click", () => applyView(
      visible, sharing ? VIEW_UNION : VIEW_SHARED));
    line.appendChild(mode);

    const count = el("span", "filtercount",
      visible.length + " of " + members.length);
    line.appendChild(count);

    const all = el("button", "filterbulk", "all");
    all.type = "button";
    all.title = "show every repository in " + project.name;
    all.disabled = visible.length === members.length;
    all.addEventListener("click", () => applyView(members, o.viewMode));
    line.appendChild(all);

    const none = el("button", "filterbulk", "none");
    none.type = "button";
    none.title = "hide every repository (the view empties until you tick one)";
    none.disabled = visible.length === 0;
    none.addEventListener("click", () => applyView([], o.viewMode));
    line.appendChild(none);
    pop.appendChild(line);
  }

  function renderRows() {
    const pendingEdit = currentPendingEdit();
    pop.textContent = "";
    if (gated) mountAddRow(pendingEdit);
    for (const row of projectFilterRows(roster, project)) {
      if (row.kind === "all") {
        mountViewRow(row.option);
        continue;
      }
      if (row.kind === "session") {
        mountSessionRow(row);
        continue;
      }
      // one member row: [eye -> show/hide] [name -> only this one] [trash]
      const line = el("span", "filterline");
      // D19: with a composable project the eyeball IS the control \u2014 it ticks
      // this repository into or out of the view. Without one (no member
      // publishes) it stays the D16 indicator over the single served view.
      const composable = !!aggregateOption;
      const shown = composable
        ? visible.includes(String(row.repository))
        : repositoryVisible(row.repository, project, o.active);
      const eye = el(composable ? "button" : "span",
        "filtereye" + (shown ? " filtervisible" : ""),
        shown ? "\ud83d\udc41" : "\u25cc");
      if (composable) {
        eye.type = "button";
        eye.title = (shown ? "hide " : "show ") + row.repository
          + " in the view";
        eye.setAttribute("aria-pressed", shown ? "true" : "false");
        eye.disabled = !row.option;        // nothing published: nothing to show
        eye.addEventListener("click", () => applyView(
          toggleVisibility(visible, row.repository,
                           project.repositories || []), o.viewMode));
      } else {
        eye.title = shown
          ? "visible in the current view"
          : "not in the current view \u2014 click the name to serve it";
      }
      line.appendChild(eye);

      const entry = el("button", "filterrow", row.repository);
      entry.type = "button";
      if (pendingEdit && pendingEdit.remove.includes(row.repository)) {
        entry.textContent += " (removal pending)";
      }
      if (row.option) {
        if (sameKey(row.option, o.active)) entry.classList.add("filteractive");
        if (!row.option.available) {
          entry.textContent += " (" + (row.option.unavailableReason
            || "snapshot unavailable") + ")";
        }
        // D19: the NAME solos \u2014 the one-click "just show me this repository"
        // gesture the single-select filter had, expressed in the visible set
        // (one visible repository serves its own snapshot, fully interactive).
        entry.title = composable
          ? "show only " + row.repository
          : "serve " + row.repository;
        entry.addEventListener("click", () => (composable
          ? applyView([row.repository], o.viewMode)
          : o.onSelect?.({ repository: row.option.repository,
                           ref: row.option.ref })));
      } else {
        entry.disabled = true;
        entry.textContent += " (no published snapshot)";
      }
      line.appendChild(entry);

      if (gated && !(pendingEdit && pendingEdit.remove.includes(row.repository))) {
        // two-click removal: the first click ARMS, the second commissions —
        // a register edit should never ride a stray click.
        const trash = el("button", "filtertrash", "\ud83d\uddd1");
        trash.type = "button";
        trash.title = "remove " + row.repository + " from " + project.name
          + " (recorded commission; the register changes at fulfilment)";
        let armed = false;
        trash.addEventListener("click", () => {
          if (!armed) {
            armed = true;
            trash.textContent = "remove?";
            trash.classList.add("filterarmed");
            return;
          }
          trash.disabled = true;
          commissionEdit({ remove: [row.repository] }, trash, () => {
            trash.disabled = false;
            armed = false;
            trash.textContent = "\ud83d\uddd1";
            trash.classList.remove("filterarmed");
          });
        });
        line.appendChild(trash);
      }
      pop.appendChild(line);
    }
    for (const adding of ((currentPendingEdit() || {}).add || [])) {
      const row = el("button", "filterrow filterpending",
        adding + " (addition pending)");
      row.type = "button";
      row.disabled = true;
      pop.appendChild(row);
    }
  }

  renderRows();
  holder.appendChild(button);
  holder.appendChild(pop);
  return holder;
}

// The controller. `host` is the header slot; nothing is rendered when the index
// is absent (the static-image path) beyond whatever the caller already shows.
//
// `onSelect(key)` is the caller's "load that snapshot" hook; `onRefreshed(result)`
// runs after a successful refresh. Both `fetchIndex`/`postRefresh` are injectable
// for tests, and `schedule` replaces setInterval so the poll is testable.
export function mountRepoSelector(host, opts) {
  const o = opts || {};
  const post = o.post || postRefresh;
  const load = o.loadIndex || fetchIndex;
  let index = o.index || null;
  let active = o.active || null;
  let snapshot = o.snapshot || null;
  const caps = o.caps || {};
  const binding = refreshBinding(caps);

  const wrap = el("span", "repopicker");
  const status = el("span", "repopick-msg");
  const hint = el("button", "repohint", "");
  hint.type = "button";
  hint.hidden = true;
  hint.title = "the publication lane has newer data — click to load it";
  // Operator AT nit (2026-08-02): `title` is not a reliable accessible name,
  // and this badge ships EMPTY until `renderHint` fills it — so an assistive
  // technology meeting it mid-render would find an unnamed button. The
  // aria-label states the action independently of the visible glyph text.
  hint.setAttribute("aria-label", "load the newer published data");
  let button = null;

  function renderHint() {
    const show = newerAvailable(active, snapshot);
    hint.hidden = !show;
    if (show) hint.textContent = "◆ " + hintLabel(active);
  }

  async function runRefresh() {
    if (!button) return;
    const label = button.textContent;
    button.disabled = true;
    button.textContent = "refreshing…";
    status.textContent = "";
    try {
      const result = await post({
        repository: active?.repository, ref: active?.ref,
      });
      status.textContent = "";
      if (typeof o.onRefreshed === "function") o.onRefreshed(result);
    } catch (err) {
      // The previously rendered snapshot stays exactly as it is.
      status.textContent = "refresh failed: " + (err?.message || "error");
    } finally {
      button.disabled = false;
      button.textContent = label;
    }
  }

  // Assigned by the filter block below when there IS a roster to re-derive; a
  // no-entries plane leaves it null and the poll simply has no views to refresh.
  let rosterChanged = null;
  if (Array.isArray(index?.entries) && index.entries.length) {
    let roster = buildRoster(index);
    const projects = buildProjects(o.projects);
    const pendingProjects = buildPendingProjects(o.projects);
    const pendingEdits = buildPendingEdits(o.projects);
    // D13: the viewer is always IN a project — the stored scope when the
    // projection still names it, else the first register project.
    let scope = defaultProjectScope(projects, storedProjectScope(o.storage));
    const currentProject = () => projects.find((p) => p.id === scope) || null;

    // ---- the repo FILTER (D14): one icon, one popover, the current
    // project's members; re-rendered whenever the project changes ----
    let filterWrap = null;
    function renderFilter() {
      const project = currentProject();
      // D19: the visible set and view mode this project renders under —
      // resolved against its CURRENT members, so a departed repository drops.
      const view = projectViewState(project, o.storage, active);
      const next = mountProjectFilter(project, roster, pendingEdits, {
        active, caps, status, projects, fetcher: o.fetcher,
        visible: view.visible, viewMode: view.mode,
        onSelect: (key) => o.onSelect?.(key),
        onView: (state) => {
          storeViewState(project?.id, state, o.storage);
          // The view row and the wheels move together: one visible
          // repository serves ITS OWN snapshot (interactive), any other
          // count serves the project's composed aggregate, which app.js
          // narrows to the visible members under the stored mode.
          const aggregate = (projectFilterRows(roster, project)
            .find((r) => r.kind === "all") || {}).option || null;
          const solo = state.visible.length === 1
            ? roster.find((entry) => entry.kind === KIND_REPOSITORY
                && entry.repository === state.visible[0])
            : null;
          const target = solo || aggregate;
          if (target) {
            o.onSelect?.({ repository: target.repository, ref: target.ref });
          } else {
            renderFilter();          // nothing to serve: just restate the set
          }
        },
      });
      if (filterWrap) filterWrap.replaceWith(next);
      else wrap.appendChild(next);
      filterWrap = next;
    }

    // ---- the PROJECT DROPDOWN (D13): "New Project" first, then the
    // register's projects, pending commissions after them ----
    let addPendingOption = null;
    let openCreateForm = null;
    if (projects.length || pendingProjects.length) {
      const picker = el("select", "repopick projectpick");
      picker.id = "projectpick";
      picker.setAttribute("aria-label", "current project");
      const newRow = el("option", "projectnew", "New Project…");
      newRow.value = "__new__";
      if (!gateCapable(caps)) newRow.disabled = true;   // creating is a gate act
      picker.appendChild(newRow);
      for (const project of projects) {
        const opt = el("option", null, project.name);
        opt.value = project.id;
        if (project.id === scope) opt.selected = true;
        picker.appendChild(opt);
      }
      // INTENT entries (design D-e): recorded, undelivered create-project
      // commissions — visible so the act registered, non-selectable so a
      // pending project can never scope the roster.
      addPendingOption = (name) => {
        const opt = el("option", "projectpending",
          name + " (commissioned — pending fulfilment)");
        opt.value = "";
        opt.disabled = true;
        picker.appendChild(opt);
      };
      for (const pendingProject of pendingProjects) {
        addPendingOption(pendingProject.name);
      }
      picker.addEventListener("change", () => {
        if (picker.value === "__new__") {
          // D13: the first line ACTS — open the create form and restore the
          // previous selection. "New Project" is never a scope.
          picker.value = scope || "";
          if (openCreateForm) openCreateForm();
          return;
        }
        scope = picker.value || scope;
        storeProjectScope(scope, o.storage);
        renderFilter();
        // Switching to a project the active repository is not in serves that
        // project's DEFAULT VIEW (D19): its merged view when it has one — the
        // default visible set is every member — else the first published
        // member, which is what the pre-composition plane always did.
        const project = currentProject();
        if (project && active
            && active.repository !== project.id
            && !(project.repositories || []).includes(active.repository)) {
          const rows = projectFilterRows(roster, project);
          const aggregate = (rows.find((r) => r.kind === "all") || {}).option;
          const first = rows.find((r) => r.kind === "repo" && r.option?.available);
          const target = aggregate || first?.option;
          if (target) {
            o.onSelect?.({ repository: target.repository, ref: target.ref });
          }
        }
      });
      wrap.appendChild(picker);
    }
    renderFilter();
    // THE ROSTER CAN GROW WHILE THE PAGE IS OPEN (2026-08-10): a create opens a
    // branch session, and the serving index advertises it as a new row. The
    // filter is built from the roster, so without this the session the human
    // just created is missing from the one control that can address it — for
    // the page's whole life, since `poll` used to update only the newer-data
    // hint. Re-derived and re-rendered, so it appears on the next poll and on
    // the shell's own nudge after a session opens.
    rosterChanged = () => { roster = buildRoster(index); renderFilter(); };
    if (gateCapable(caps) && o.projects) {
      openCreateForm = mountCreateProject(wrap, status, roster, projects, o,
                                          addPendingOption);
      // add-register-edit-lane: the UPDATE button — visible whenever
      // recorded commissions await fulfilment; the serve runs the lane once
      // and the shell reloads onto the new register truth.
      const pendingCount = pendingProjects.length + pendingEdits.length;
      if (pendingCount) {
        const apply = el("button", "repobtn applybtn",
          "⟳ apply " + pendingCount + " pending");
        apply.type = "button";
        apply.title = "fulfil the recorded project-register commissions now "
          + "(validate, deliver, commit, push)";
        apply.addEventListener("click", async () => {
          apply.disabled = true;
          status.textContent = "applying…";
          try {
            const response = o.fetcher
              ? await o.fetcher(ACTIONS_APPLY_REGISTER_EDITS_ROUTE, { method: "POST" })
              : await fetch(ACTIONS_APPLY_REGISTER_EDITS_ROUTE, { method: "POST" });
            const data = await response.json().catch(() => ({}));
            if (!response.ok || data?.ok !== true) {
              apply.disabled = false;
              status.textContent = "apply failed: "
                + (data?.error || ("HTTP " + response.status))
                + (data?.skipped?.length
                    ? " — skipped: " + data.skipped.map((s) => s[1] + " (" + s[2] + ")").join("; ")
                    : "");
              return;
            }
            status.textContent = "applied " + (data.applied?.length || 0)
              + (data.skipped?.length ? (", skipped " + data.skipped.length) : "");
            if (typeof o.onRefreshed === "function") o.onRefreshed(data);
          } catch (err) {
            apply.disabled = false;
            status.textContent = "apply failed: " + (err?.message || "error");
          }
        });
        wrap.appendChild(apply);
      }
    }
  }
  if (refreshCapable(caps)) {
    button = el("button", "repobtn", binding === "regenerate" ? "↻ regenerate" : "↻ refresh");
    button.type = "button";
    button.title = binding === "regenerate"
      ? "re-run the generator against this checkout (derived snapshot only)"
      : "re-fetch the published index and snapshot (read-only)";
    button.addEventListener("click", runRefresh);
    wrap.appendChild(button);
  }
  wrap.appendChild(hint);
  wrap.appendChild(status);
  hint.addEventListener("click", runRefresh);
  renderHint();
  if (host) {
    host.textContent = "";
    host.appendChild(wrap);
  }

  // The background index poll: index only, never a snapshot, never a reload.
  let timer = null;
  const schedule = o.schedule || ((fn, ms) => setInterval(fn, ms));
  async function poll() {
    const fresh = await load();
    if (!fresh) return;
    index = fresh;
    active = buildRoster(index).find((r) => sameKey(r, active)) || active;
    renderHint();
    // …and the filter, so a session that opened since boot becomes addressable
    if (rosterChanged) rosterChanged();
  }
  if (o.poll !== false && refreshCapable(caps)) {
    timer = schedule(poll, o.intervalMs || POLL_INTERVAL_MS);
  }

  return {
    element: wrap,
    binding,
    poll,
    // Idempotent by design: clearing the handle is conditional, forgetting it is
    // NOT (a second stop() must stay a no-op). Braced so that reads the way it
    // runs — the one-line form said "conditional" and meant otherwise (S2681).
    stop() {
      if (timer) { clearInterval(timer); }
      timer = null;
    },
    setSnapshot(next) { snapshot = next; renderHint(); },
    setActive(next) { active = next; renderHint(); },
    refresh: runRefresh,
  };
}

// The stale banner (design D6) and the sparse-station note (D10). Rendered by
// the app shell above the views: a fallback that renders silently is the failure
// this change exists to end, so the banner is part of the contract, not chrome.
export function renderStaleBanner(host, active, sparseText) {
  if (!host) return null;
  host.textContent = "";
  const stale = staleNotice(active);
  if (!stale && !sparseText) {
    host.hidden = true;
    return null;
  }
  host.hidden = false;
  if (stale) host.appendChild(el("div", "stalebanner-line", "⚠ " + stale));
  if (sparseText) host.appendChild(el("div", "stalebanner-line sparse", "· " + sparseText));
  return host;
}

export { freshnessLabel, keyId };
