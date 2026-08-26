// Project grouping roll-up (US3, T014-T016, change 3.8). The generator
// already resolves each snapshot's `repository` -> `project` ->
// `project_group` (T006/T014, `register.py`'s ProjectRegisterAdapter); this
// module is PURELY a renderer-side roll-up over those already-resolved
// snapshot fields — it never reads the project register itself, so editing
// the register changes grouping only after the next `generate` run (spec
// "Project grouping hierarchy", acceptance scenario 4).
//
// Multi-repo readiness: `buildGroupingModel` takes an ARRAY of snapshots (a
// roll-up is several repositories' snapshots aggregated), even though v1
// loads exactly one (app.js's single `fetch`, unchanged). A repository
// absent from the register carries no `project`/`project_group` fields and
// renders as its OWN implicit project (never a failure) — the absence case
// every call site below must degrade into, not error on.
//
// Descriptive navigation only: no lifecycle or authority semantics attach to
// a roll-up scope (spec "Non-Negotiable Constraints"); the control never
// re-derives tallies, it only sums each member snapshot's OWN counts
// verbatim (aggregate, never re-score).
//
// This module is copied ALONE into a node harness (test_grouping.py), so it
// cannot import ./helpers.js; its local el() binds text via textContent (the
// same DOM-safety discipline), never innerHTML.

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

// ---- tallies: the same counts the stats strip shows, summed verbatim ----

const TALLY_FIELDS = [
  ["documents", "docs"],
  ["clusters", "clusters"],
  ["possibles", "possibles"],
  ["staged_topics", "staged"],
  ["changes_active", "proposals"],
  ["changes_archived", "realized"],
];

function snapshotTallies(snapshot) {
  const s = snapshot || {};
  const changes = s.changes || [];
  return {
    documents: (s.documents || []).length,
    clusters: (s.clusters || []).length,
    possibles: (s.possibles || []).length,
    staged_topics: (s.staged_topics || []).length,
    changes_active: changes.filter((c) => c.status === "active").length,
    changes_archived: changes.filter((c) => c.status === "archived").length,
  };
}

function zeroTallies() {
  const out = {};
  for (const [key] of TALLY_FIELDS) out[key] = 0;
  return out;
}

function sumTallies(list) {
  const out = zeroTallies();
  for (const t of list) for (const [key] of TALLY_FIELDS) out[key] += t[key] || 0;
  return out;
}

function tallyLine(tallies) {
  return TALLY_FIELDS.map(([key, label]) => tallies[key] + " " + label).join(" · ");
}

// ---- pure derivation: snapshots -> repo/project/group hierarchy ----
//
// Node-tested directly (tests/ideation-dashboard/test_grouping.py), exactly
// like model.js's buildFunnelModel: no DOM, no I/O, safe to run standalone.

function repositoryView(snap) {
  return {
    repository: snap.repository,
    project: snap.project || null,
    projectGroup: snap.project_group || null,
    tallies: snapshotTallies(snap),
  };
}

// Group by resolved project id; a repository with no `project` field gets an
// implicit project keyed by its OWN repository id (D10 fallback), so two
// different unregistered repositories never collide into one heading.
function deriveProjects(repositories) {
  const projectsByKey = new Map();
  for (const r of repositories) {
    const implicit = !r.project;
    const key = implicit ? "repo:" + r.repository : "project:" + r.project;
    if (!projectsByKey.has(key)) {
      projectsByKey.set(key, {
        id: implicit ? null : r.project,
        label: implicit ? r.repository : r.project,
        implicit,
        projectGroup: implicit ? null : r.projectGroup,
        repositories: [],
      });
    }
    projectsByKey.get(key).repositories.push(r);
  }
  const projects = [...projectsByKey.values()].sort((a, b) => a.label.localeCompare(b.label));
  for (const p of projects) p.tallies = sumTallies(p.repositories.map((r) => r.tallies));
  return projects;
}

function deriveGroups(projects) {
  const groupsByKey = new Map();
  const ungroupedProjects = [];
  for (const p of projects) {
    if (!p.projectGroup) { ungroupedProjects.push(p); continue; }
    if (!groupsByKey.has(p.projectGroup)) {
      groupsByKey.set(p.projectGroup, { id: p.projectGroup, label: p.projectGroup, projects: [] });
    }
    groupsByKey.get(p.projectGroup).projects.push(p);
  }
  const groups = [...groupsByKey.values()].sort((a, b) => a.label.localeCompare(b.label));
  for (const g of groups) g.tallies = sumTallies(g.projects.map((p) => p.tallies));
  return { groups, ungroupedProjects };
}

export function buildGroupingModel(snapshots) {
  const repositories = (snapshots || []).filter(Boolean).map(repositoryView);
  const projects = deriveProjects(repositories);
  const { groups, ungroupedProjects } = deriveGroups(projects);
  return { repositories, projects, groups, ungroupedProjects };
}

// ---- DOM: the roll-up control (header mount). The model itself is recomputed
// per render (cheap — it only sums fields already in memory, no re-scan).

function repoRow(r) {
  const row = el("div", "rollup-repo");
  row.appendChild(el("span", "rollup-repo-name", r.repository));
  row.appendChild(el("span", "rollup-repo-tallies", tallyLine(r.tallies)));
  return row;
}

function projectBlock(p) {
  const block = el("div", "rollup-project" + (p.implicit ? " implicit" : ""));
  const head = el("div", "rollup-project-head");
  head.appendChild(el("span", "rollup-project-name",
    p.label + (p.implicit ? " (ungrouped — its own implicit project)" : "")));
  head.appendChild(el("span", "rollup-project-tallies", tallyLine(p.tallies)));
  block.appendChild(head);
  // Per-repository detail reachable beneath a registered project's heading
  // (spec US3 independent test); an implicit project already IS the
  // repository, so nesting would just repeat the same row.
  if (!p.implicit) {
    const nested = el("div", "rollup-repos");
    for (const r of p.repositories) nested.appendChild(repoRow(r));
    block.appendChild(nested);
  }
  return block;
}

function groupBlock(g) {
  const block = el("div", "rollup-group");
  const head = el("div", "rollup-group-head");
  head.appendChild(el("span", "rollup-group-name", g.label));
  head.appendChild(el("span", "rollup-group-tallies", tallyLine(g.tallies)));
  block.appendChild(head);
  const nested = el("div", "rollup-projects");
  for (const p of g.projects) nested.appendChild(projectBlock(p));
  block.appendChild(nested);
  return block;
}

// ---- per-mode body renderers (extracted so the draw loop stays simple) ----

function renderRepositoryMode(body, model) {
  if (!model.repositories.length) {
    body.appendChild(el("div", "empty", "no repositories in the loaded snapshot(s)"));
    return;
  }
  for (const r of model.repositories) body.appendChild(repoRow(r));
}

function renderGroupMode(body, model) {
  if (!model.groups.length && !model.ungroupedProjects.length) {
    body.appendChild(el("div", "empty", "no project groups registered"));
    return;
  }
  for (const g of model.groups) body.appendChild(groupBlock(g));
  for (const p of model.ungroupedProjects) body.appendChild(projectBlock(p));
}

function renderProjectMode(body, model) {
  if (!model.projects.length) {
    body.appendChild(el("div", "empty", "no projects registered"));
    return;
  }
  for (const p of model.projects) body.appendChild(projectBlock(p));
}

const MODE_RENDERERS = {
  repository: renderRepositoryMode,
  group: renderGroupMode,
  project: renderProjectMode,
};

// `renderGroupingBar(root, snapshots, opts)`: mounts a repository/project/
// project-group scope toggle (mirroring funnel.js's six/five-column
// `.variant`/`.vbtn` control) plus the aggregated roll-up beneath it. Reads
// ONLY the `snapshots` array passed in — no fetch, no repository scan.
export function renderGroupingBar(root, snapshots, opts) {
  root.innerHTML = "";
  root.classList.add("rollup");

  const variant = el("div", "variant rollup-variant");
  variant.setAttribute("role", "group");
  variant.setAttribute("aria-label", "Grouping roll-up");
  const modes = [
    ["repository", "by repository"],
    ["project", "by project (default)"],
    ["group", "by project group"],
  ];
  let mode = opts?.defaultMode || "project";
  const buttons = {};
  for (const [key, label] of modes) {
    const btn = el("button", "vbtn", label);
    btn.type = "button";
    buttons[key] = btn;
    variant.appendChild(btn);
  }
  root.appendChild(variant);

  const body = el("div", "rollup-body");
  root.appendChild(body);

  function draw() {
    const model = buildGroupingModel(snapshots);
    for (const [key, btn] of Object.entries(buttons)) btn.setAttribute("aria-pressed", String(key === mode));
    body.innerHTML = "";
    (MODE_RENDERERS[mode] || renderProjectMode)(body, model);
  }
  for (const [key, btn] of Object.entries(buttons)) {
    btn.addEventListener("click", () => { mode = key; draw(); });
  }
  draw();

  return { redraw: draw };
}
