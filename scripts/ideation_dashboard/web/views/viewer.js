// Read-only Markdown viewer (T018). Renders any explorer-selected document as
// rendered Markdown served READ-ONLY, pass-through from the pinned checkout
// via `serve.py`'s `/source/<path>` route (D15) — the viewer never re-fetches
// or duplicates document content into the snapshot; the snapshot-only rule
// governs dashboard STATE, never document CONTENT. Vendored MIT `markdown-it`
// (`../vendor/markdown-it.min.js`) with the `html` option DISABLED: markdown-it
// escapes raw HTML (and always escapes fenced/indented code content
// regardless of the `html` option), so a document can never inject a live
// `<script>`/`<style>`/event-handler into the dashboard's own page.
//
// Surfaces the snapshot/checkout divergence from `X-Snapshot-Divergence`
// (serve.py's header) as a banner exactly when it reads `diverged` — the
// resolution is always "regenerate", never a hand-edit. The ✎ escape hatch
// does not edit anything itself (per the interactivity boundary): on a capable
// local human console it asks the guarded action route to launch the selected
// source file in the user's own editor.
//
// Degrades gracefully with NO_SHIM_MESSAGE when there is no serve.py to talk
// to (`file://` mode, or any fetch failure) — never a raw browser error.

import "../vendor/markdown-it.min.js";

export const NO_SHIM_MESSAGE = "viewer requires the serve shim — run generate-and-open";

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

// html DISABLED — never render raw HTML from a doc. linkify/typographer are
// also off: verbatim source semantics, no surprise auto-linking or smart
// punctuation substitution over governance prose.
//
// EXTERNAL IMAGES ARE STRIPPED BY DEFAULT. `html:false` already neutralises raw
// `<img>` tags, but a Markdown image whose source carries an external scheme or
// is protocol-relative would otherwise render a live `<img src>` — inserting it
// may fire a request the instant the node lands in the page (tracking pixel /
// egress). The image render rule below rewrites those sources into an inert
// placeholder: the alt text plus a click-to-load button. Relative and
// `data:image/` sources render normally; every other explicit scheme requires a
// human click.
function isExternalImageSrc(src) {
  const value = String(src || "").trim();
  if (/^data:image\//i.test(value)) return false;
  return /^(?:[a-z][a-z0-9+.-]*:|\/\/)/i.test(value);
}

// Local escape for the placeholder markup string (mirrors helpers-style
// completeness — apostrophe included). Both the attribute value and the
// visible label are escaped through it.
function escForMarkup(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

let sharedMarkdownRenderer = null;

function mdRenderer() {
  if (sharedMarkdownRenderer) return sharedMarkdownRenderer;
  const md = globalThis.markdownit({ html: false, linkify: false, typographer: false });
  const renderImage = md.renderer.rules.image
    || ((tokens, idx, options, env, self) => self.renderToken(tokens, idx, options));
  md.renderer.rules.image = (tokens, idx, options, env, self) => {
    const token = tokens[idx];
    const src = token.attrGet("src") || "";
    if (!isExternalImageSrc(src)) return renderImage(tokens, idx, options, env, self);
    const label = token.content || src;
    return '<span class="ext-img" data-src="' + escForMarkup(src) + '">'
      + "\u{1F5BC} external image not loaded — " + escForMarkup(label)
      + ' <button type="button" class="ext-img-load">load image</button></span>';
  };
  sharedMarkdownRenderer = md;
  return sharedMarkdownRenderer;
}

// Wire the click-to-load affordance on every stripped external image. Loading
// is USER-INITIATED — the default render made no off-origin request; a click
// (and only a click) sets the src and lets the image load in place.
function wireExternalImages(container) {
  for (const btn of container.querySelectorAll(".ext-img-load")) {
    btn.addEventListener("click", () => {
      const holder = btn.closest(".ext-img");
      if (!holder) return;
      const img = document.createElement("img");
      img.src = holder.dataset.src;
      img.className = "ext-img-loaded";
      img.alt = "";
      holder.replaceWith(img);
    });
  }
}

// The ONE reusable Markdown-to-HTML seam for the viewer and the doxBench
// preview. (Chat prose deliberately renders as PLAIN TEXT via textContent and
// never passes through this seam -- triage item 17 retired the stale claim.) Raw HTML stays disabled, URL linkification stays disabled, governance
// punctuation stays verbatim, and external image egress stays click-to-load.
// Callers that mount into the DOM should use mountSafeMarkdown so the reviewed
// HTML sink and external-image wiring remain centralized here.
export function renderSafeMarkdownHtml(markdown) {
  if (typeof markdown !== "string") {
    throw new TypeError("Markdown source must be a string");
  }
  return mdRenderer().render(markdown);
}

export function mountSafeMarkdown(container, markdown) {
  container.innerHTML = renderSafeMarkdownHtml(markdown);
  wireExternalImages(container);
  return container;
}

// pure — unit-tested via node without any DOM/fetch.
export function isFileProtocol(loc) {
  return loc?.protocol === "file:";
}

// pure — unit-tested via node. Only `diverged` produces a banner; `aligned`
// and `unknown` render nothing (spec: the banner is for the case the
// checkout has moved PAST the snapshot's revision).
export function divergenceBannerText(state) {
  return state === "diverged" ? "snapshot behind checkout — regenerate" : null;
}

// window.location unless the caller injects a `loc` override (tests).
function resolveLocation(o) {
  if ("loc" in o) return o.loc;
  if (typeof window !== "undefined") return window.location;
  return null;
}

// The one source fetch (D15 read-only pass-through), injectable for testing.
function fetchSource(injectedFetch, sourceBase, path) {
  if (injectedFetch) return injectedFetch(sourceBase + path, { cache: "no-store" });
  return fetch(sourceBase + path, { cache: "no-store" });
}

// One select-to-edit click cycle, extracted for a DOM-free Node test.
export async function runEditAction(btn, status, path, edit) {
  const label = btn.textContent;
  btn.disabled = true;
  btn.textContent = "opening editor…";
  status.hidden = false;
  status.textContent = "opening in your editor…";
  try {
    const result = await edit.open(path);
    status.textContent = "opened in your editor — " + (result?.path || path);
  } catch (err) {
    status.textContent = "could not open editor: " + (err?.message || "error");
  } finally {
    btn.disabled = false;
    btn.textContent = label;
  }
}

// Header strip + summary + banner/body/editline chrome. `mountGateHost` is the
// caller's chance to grow the gate bar between the summary and the banner.
// Returns the { banner, body } panes the fetch path writes into.
function buildViewerChrome(root, path, doc, edit, mountGateHost) {
  const head = el("div", "viewer-head");
  head.appendChild(el("span", "viewer-path", path));
  if (doc?.stage) head.appendChild(el("span", "pill stage", doc.stage));
  if (doc?.kind) head.appendChild(el("span", "pill neutral", doc.kind));
  const editBtn = el("button", "editbtn", "✎ edit");
  editBtn.type = "button";
  editBtn.disabled = !edit?.enabled;
  editBtn.title = edit?.enabled
    ? "open this document in your local editor"
    : "select-to-edit is available from the local human console";
  head.appendChild(editBtn);
  root.appendChild(head);
  const editline = el("div", "docstatus viewer-editline");
  editline.setAttribute("aria-live", "polite");
  editline.hidden = true;
  root.appendChild(editline);
  if (doc?.summary) root.appendChild(el("div", "viewer-summary", doc.summary));

  mountGateHost(root);

  const banner = el("div", "viewer-banner");
  banner.hidden = true;
  root.appendChild(banner);

  const body = el("div", "viewer-body markdown-body");
  root.appendChild(body);

  editBtn.addEventListener("click", () => runEditAction(editBtn, editline, path, edit));

  return { banner, body };
}

// Renders `opts.path` (repo-relative) into `root`. `opts.doc`, when supplied
// (the explorer's matched `documents[]` entry), seeds the header strip's
// status/kind chips and summary line — optional, since change-folder files
// (proposal.md etc.) are not themselves catalogued in `documents[]`.
export async function renderViewer(root, opts) {
  const o = opts || {};
  const path = o.path;
  const doc = o.doc || null;
  // Gate context ({ changeId, repository, actor }) + a `mountGate(host, ctx)`
  // callback, both supplied by app.js when a gate-bearing artifact is opened
  // from a proposal (active change) tile. The viewer grows the human gate bar
  // (D16/D17) but stays DECOUPLED from gate.js — app.js owns the wiring, exactly
  // as it wires the explorer to the viewer. Absent for docs opened outside a
  // change, which stay view-only. The bar produces CLI action descriptors only
  // (serve.py is read-only; no server-side gate).
  const gate = o.gate || null;
  const mountGate = o.mountGate || null;
  const sourceBase = o.sourceBase || "/source/";
  const edit = o.edit || { enabled: false };
  const loc = resolveLocation(o);
  // Injectable for testing; the real path (no override) calls the global
  // `fetch` directly — the ONE other legitimate network call in the whole
  // bundle besides app.js's snapshot fetch (D15 source pass-through).
  const injectedFetch = o.fetch;

  root.innerHTML = "";
  if (!path) {
    root.appendChild(el("div", "empty", "no document selected"));
    return;
  }

  const { banner, body } = buildViewerChrome(root, path, doc, edit, (host) => {
    // Human gate bar on a gate-bearing artifact opened from a proposal tile.
    // app.js decides gate-bearing and supplies mountGate (gate.js); the
    // read-only web v1 bar emits CLI action descriptors only.
    if (gate?.changeId && mountGate) {
      const gateHost = el("div", "viewer-gate");
      host.appendChild(gateHost);
      mountGate(gateHost, { changeId: gate.changeId, path, repository: gate.repository, actor: gate.actor });
    }
  });

  if (isFileProtocol(loc)) {
    body.textContent = NO_SHIM_MESSAGE;
    return;
  }

  let response;
  try {
    response = await fetchSource(injectedFetch, sourceBase, path);
  } catch {
    // no serve shim to talk to (file:// mode or network failure) — degrade
    body.textContent = NO_SHIM_MESSAGE;
    return;
  }

  const bannerText = divergenceBannerText(response.headers?.get("X-Snapshot-Divergence"));
  if (bannerText) {
    banner.hidden = false;
    banner.textContent = bannerText;
  }

  if (!response.ok) {
    body.textContent = "could not load " + path + " (HTTP " + response.status + ")";
    return;
  }

  const text = await response.text();
  mountSafeMarkdown(body, text);
}
