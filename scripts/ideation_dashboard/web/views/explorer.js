// Drill-down explorer (T017): pipeline/funnel STAGED, PROPOSAL, and REALIZED
// tiles open as their underlying artifact folders (FR-008). Snapshot-only —
// folder listings come from `staged_topics[].files` and `changes[].files`
// (the generator's recursive, repo-relative listing of each change's own
// folder: proposal/design/tasks/spec-deltas/supporting-docs all live inside
// it by the OpenSpec change-folder convention), cross-referenced against
// `documents[]` for header metadata (status/kind/summary) where a listed file
// is itself a governed doc. The explorer NEVER scans the repository — it is a
// pure projection of these snapshot fields, laid out for a single overlay
// panel that also hosts the read-only viewer (viewer.js).
//
// Only staged/proposal/realized tiles are folder-openable (FR-008); doc,
// cluster, and possible tiles are not backed by a folder in the snapshot's
// current shape, so callers (funnel.js, board.js) only wire the open
// affordance onto those three column kinds.
//
// Decoupled from the viewer (T018) by design: this module never imports
// viewer.js. `mountExplorer` takes an `onOpenFile(entry, viewerPane)`
// callback (app.js supplies `viewer.js`'s `renderViewer`) so the folder
// listing and the Markdown renderer stay independently testable and
// independently landable.

function el(tag, cls, html) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (html != null) node.innerHTML = html;
  return node;
}
// Local copy (this module is copied ALONE into a node harness and is asserted
// to have zero imports, so it cannot import ./helpers.js). Kept in step with
// helpers.esc — apostrophe included.
function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function basename(path) {
  return String(path).split("/").at(-1) || path;
}

// A change-folder file's explorer group label, purely from its path — the
// OpenSpec change-folder convention (proposal.md/design.md/tasks.md at the
// folder root; specs/<capability>/spec.md for spec deltas; supporting-docs/
// for supporting material). Exported for the node-harness test.
export function classifyChangeFile(path) {
  const base = basename(path);
  if (base === "proposal.md") return "proposal";
  if (base === "design.md") return "design";
  if (base === "tasks.md") return "tasks";
  if (/(^|\/)specs\//.test(path)) return "spec deltas";
  if (/(^|\/)supporting-docs\//.test(path)) return "supporting docs";
  return "other";
}

const CHANGE_GROUP_ORDER = ["proposal", "design", "tasks", "spec deltas", "supporting docs", "other"];

function docByPath(snapshot, path, repository, ref) {
  return (snapshot.documents || []).find((d) =>
    d.path === path &&
    (!repository || d.repository === repository) &&
    (!ref || d.ref === ref)) || null;
}

function fileEntry(snapshot, path, owner) {
  const repository = owner?.repository || null;
  const ref = owner?.ref || null;
  const doc = docByPath(snapshot, path, repository, ref);
  return {
    path,
    doc,
    repository: doc?.repository || repository,
    ref: doc?.ref || owner?.ref || null,
  };
}

// The pure snapshot -> explorer-target derivation for one tile. `kind` is
// 'staged' | 'proposal' | 'realized'; `id` is the staging_id or change id.
// Returns null when the tile does not resolve against the snapshot (a stale
// click after regeneration, or a caller passing an unrecognized kind).
// DOM-free and pure — unit-tested via node exactly like model.js.
export function resolveExplorerTarget(kind, id, snapshot) {
  const s = snapshot || {};
  if (kind === "staged") {
    const t = (s.staged_topics || []).find((x) => x.staging_id === id);
    if (!t) return null;
    const files = (t.files || []).map((path) => fileEntry(s, path, t));
    const n = (t.files || []).length;
    return {
      kind, id, title: id,
      subtitle: "ideation/staging/" + id + " · " + n + " file" + (n === 1 ? "" : "s") +
        (t.target_change ? " · → " + t.target_change : " · no pick yet"),
      groups: [{ label: "topic folder (incl. any openspec/ drafts)", files }],
    };
  }
  if (kind === "proposal" || kind === "realized") {
    const c = (s.changes || []).find((x) => x.id === id);
    if (!c) return null;
    const byLabel = new Map();
    for (const path of c.files || []) {
      const label = classifyChangeFile(path);
      if (!byLabel.has(label)) byLabel.set(label, []);
      byLabel.get(label).push(fileEntry(s, path, c));
    }
    const groups = CHANGE_GROUP_ORDER
      .filter((label) => byLabel.has(label))
      .map((label) => ({ label, files: byLabel.get(label) }));
    return {
      kind, id, title: id,
      subtitle: c.folder || ("openspec/changes/" + id),
      groups,
    };
  }
  return null;
}

// ---- DOM: one row per listed file, with header chips when the file is
// itself a governed document in `documents[]` (status/kind/summary/topics);
// files outside that projection (e.g. a change's proposal.md) list by name
// only — the spec requires headers only for the staged-topic scenario.
function fileRow(entry, onOpen) {
  const row = el("div", "docrow explorer-row");
  const info = el("span");
  info.appendChild(el("span", "name", esc(basename(entry.path))));
  const bits = [entry.path];
  if (entry.doc) bits.push(entry.doc.stage, entry.doc.kind, entry.doc.summary);
  info.appendChild(el("div", "where", esc(bits.filter(Boolean).join(" · "))));
  row.appendChild(info);
  if (entry.doc && (entry.doc.topics || []).length) {
    const chips = el("span", "chips");
    for (const t of entry.doc.topics) chips.appendChild(el("span", "tchip", esc(t)));
    row.appendChild(chips);
  }
  row.tabIndex = 0;
  row.setAttribute("role", "button");
  row.addEventListener("click", () => onOpen(entry));
  row.addEventListener("keydown", (ev) => {
    if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); onOpen(entry); }
  });
  return row;
}

// Mounts the one explorer+viewer overlay panel into `container` (called once,
// from app.js). `onOpenFile(entry, viewerPaneElement)` renders the selected
// file's content into the viewer pane — app.js supplies `viewer.js`'s
// `renderViewer` here; this module has no compile-time dependency on it.
// Returns `{ openTile(kind, id), close() }` — the entrypoint funnel.js/
// board.js call when a staged/proposal/realized tile's "open folder"
// affordance is activated.
export function mountExplorer(container, snapshot, { onOpenFile, signal } = {}) {
  container.innerHTML = "";
  const overlay = el("div", "explorer-overlay");
  overlay.hidden = true;
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-modal", "true");

  const panel = el("div", "explorer-panel");
  const head = el("div", "explorer-head");
  const titles = el("div", "explorer-titles");
  const title = el("span", "explorer-title");
  // a11y (#19): the dialog is labelled by its own title element.
  title.id = "explorer-title";
  overlay.setAttribute("aria-labelledby", title.id);
  const subtitle = el("div", "explorer-subtitle");
  titles.appendChild(title);
  titles.appendChild(subtitle);
  const closeBtn = el("button", "explorer-close", "✕ close");
  closeBtn.type = "button";
  head.appendChild(titles);
  head.appendChild(closeBtn);

  const body = el("div", "explorer-body");
  const list = el("div", "doclist explorer-list");
  const viewer = el("div", "explorer-viewer");
  body.appendChild(list);
  body.appendChild(viewer);

  panel.appendChild(head);
  panel.appendChild(body);
  overlay.appendChild(panel);
  container.appendChild(overlay);

  // a11y (#19): the element that had focus when the dialog opened, restored on
  // close so keyboard focus never falls back to the top of the document.
  let lastFocused = null;

  // Focusable descendants of the panel, in DOM order, for the focus trap.
  function focusable() {
    const sel = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
    return [...panel.querySelectorAll(sel)].filter((node) => !node.disabled && node.offsetParent !== null);
  }

  function close() {
    overlay.hidden = true;
    viewer.innerHTML = "";
    if (typeof lastFocused?.focus === "function") lastFocused.focus();
    lastFocused = null;
  }
  closeBtn.addEventListener("click", close);
  overlay.addEventListener("click", (ev) => { if (ev.target === overlay) close(); });
  // scoped to the caller's RENDER: this overlay is re-mounted whenever the
  // shell re-renders, and an unscoped document listener would stack
  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape" && !overlay.hidden) close();
  }, { signal });
  // focus trap: Tab / Shift+Tab cycle WITHIN the open dialog.
  panel.addEventListener("keydown", (ev) => {
    if (ev.key !== "Tab") return;
    const items = focusable();
    if (!items.length) return;
    const first = items[0];
    const last = items.at(-1);
    if (ev.shiftKey && document.activeElement === first) { ev.preventDefault(); last.focus(); }
    else if (!ev.shiftKey && document.activeElement === last) { ev.preventDefault(); first.focus(); }
  });

  let currentTile = null; // the open tile ({ kind, id }) — threaded to onOpenFile
                          // so app.js can grow the gate bar on a proposal's docs.

  function openTile(kind, id) {
    lastFocused = document.activeElement; // the tile's "open folder" button
    currentTile = { kind, id };
    const target = resolveExplorerTarget(kind, id, snapshot);
    list.innerHTML = "";
    viewer.innerHTML = "";
    if (!target) {
      title.textContent = kind + " · " + id;
      subtitle.textContent = "";
      list.appendChild(el("div", "empty", "nothing to show for this tile in the snapshot"));
    } else {
      title.textContent = target.title;
      subtitle.textContent = target.subtitle || "";
      const anyFiles = target.groups.some((g) => g.files.length);
      if (!anyFiles) list.appendChild(el("div", "empty", "no files recorded for this folder"));
      for (const group of target.groups) {
        if (!group.files.length) continue;
        list.appendChild(el("div", "docgroup", esc(group.label)));
        for (const entry of group.files) {
          list.appendChild(fileRow(entry, (e) => {
            if (onOpenFile) onOpenFile(e, viewer, currentTile);
          }));
        }
      }
    }
    overlay.hidden = false;
    closeBtn.focus(); // initial focus lands inside the dialog (a11y #19)
  }

  // Open ONE document straight into the viewer pane (the wheel's documents
  // `read` verb, 2026-07-25). Same overlay, same read-only viewer, same
  // `onOpenFile` seam — the listing is just this one file, and it is rendered
  // immediately instead of waiting for a row click. No tile context is threaded
  // (a document opened outside a change never grows the gate bar).
  function openDoc(path, doc, sourceKey) {
    if (!path) return;
    lastFocused = document.activeElement;
    currentTile = null;
    const resolved = doc ||
      docByPath(snapshot, path, sourceKey?.repository, sourceKey?.ref);
    const entry = {
      path,
      doc: resolved,
      repository: resolved?.repository || sourceKey?.repository || null,
      ref: resolved?.ref || sourceKey?.ref || null,
      sourceKey: sourceKey || null,
    };
    list.innerHTML = "";
    viewer.innerHTML = "";
    title.textContent = basename(path);
    subtitle.textContent = path;
    list.appendChild(el("div", "docgroup", "source file (read-only)"));
    list.appendChild(fileRow(entry, (e) => {
      if (onOpenFile) onOpenFile(e, viewer, currentTile);
    }));
    overlay.hidden = false;
    closeBtn.focus(); // initial focus lands inside the dialog (a11y #19)
    if (onOpenFile) onOpenFile(entry, viewer, currentTile);
  }

  return { openTile, openDoc, close };
}
