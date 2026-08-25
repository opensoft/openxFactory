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
// source file in the user's own editor — which is why it is labelled "open in
// editor" and not "edit" (add-doxbench-editing-phase-a: on a doxBench surface
// the bare word "edit" is reserved for editing that happens INSIDE the app).
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
    // `data-label` STORES the derived label (T104 F7-6): it used to be
    // rendered into the visible text and thrown away, so the click-time
    // replacement <img> had nothing to carry as alt.
    return '<span class="ext-img" data-src="' + escForMarkup(src)
      + '" data-label="' + escForMarkup(label) + '">'
      + "\u{1F5BC} external image not loaded — " + escForMarkup(label)
      + ' <button type="button" class="ext-img-load">load image</button></span>';
  };
  sharedMarkdownRenderer = md;
  return sharedMarkdownRenderer;
}

// LOAD CONSENT, per container per src (T104 F6-5). mountSafeMarkdown rebuilds
// via innerHTML on every doxBench preview re-render (per debounced
// keystroke), which reverted an image the human explicitly loaded to a
// placeholder. The human's click is remembered HERE — a WeakMap so a
// discarded container takes its consent with it — and the rebuild re-loads
// exactly the srcs already consented to in THAT container; a NEW src still
// requires its own click, and a FAILED load revokes the consent (never an
// endless auto-retry of a dead URL).
const loadedExternalSrcs = new WeakMap();

function consentSetFor(container) {
  let set = loadedExternalSrcs.get(container);
  if (!set) {
    set = new Set();
    loadedExternalSrcs.set(container, set);
  }
  return set;
}

function placeholderLabel(holder) {
  return holder.dataset.label || holder.dataset.src || "";
}

// The RETRY placeholder a failed load restores (T104 F7-6): same classes and
// same data attributes as the rendered one, built as nodes (textContent
// binding — no markup string outside the render rule), so a failed external
// image is a labeled, retriable state instead of an empty broken-image box.
function retryPlaceholder(container, src, label) {
  const holder = document.createElement("span");
  holder.className = "ext-img";
  holder.dataset.src = src;
  holder.dataset.label = label;
  holder.textContent = "\u{1F5BC} external image failed to load — " + label + " ";
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "ext-img-load";
  btn.textContent = "retry load";
  holder.appendChild(btn);
  wireLoadButton(container, btn);
  return holder;
}

// The loaded replacement: the derived label rides along as alt (T104 F7-6 —
// it used to be dropped, leaving an unlabeled image), and a load failure
// swaps back to the labeled retry placeholder above.
function loadedExternalImage(container, src, label) {
  const img = document.createElement("img");
  img.src = src;
  img.className = "ext-img-loaded";
  img.alt = label;
  img.addEventListener("error", () => {
    // P3-9 (wave re-review P3 tail): act only while THIS img is still in the
    // container. The consent record is keyed by CONTAINER and survives every
    // rebuild — but an in-flight load detached by a per-keystroke preview
    // rebuild can still fire its error afterwards, and revoking here then
    // punished the LIVE container: its re-wired, visibly-loaded image
    // reverted to a placeholder on the next rebuild. A detached corpse's
    // late error says nothing about the live consent, so it is ignored; a
    // failure on the ATTACHED image still revokes exactly as before. The
    // walk is over parentNode (not Node.isConnected) so the same rule holds
    // in the DOM-shim harnesses.
    let node = img.parentNode;
    while (node && node !== container) node = node.parentNode;
    if (node !== container) return;
    consentSetFor(container).delete(src);
    img.replaceWith(retryPlaceholder(container, src, label));
  });
  return img;
}

function wireLoadButton(container, btn) {
  btn.addEventListener("click", () => {
    const holder = btn.closest(".ext-img");
    if (!holder) return;
    const src = holder.dataset.src;
    consentSetFor(container).add(src);
    holder.replaceWith(
      loadedExternalImage(container, src, placeholderLabel(holder)));
  });
}

// Wire the click-to-load affordance on every stripped external image. Loading
// is USER-INITIATED — the default render made no off-origin request; a click
// (and only a click) sets the src and lets the image load in place. After a
// REBUILD of a container the human already loaded images in, the consented
// srcs are re-loaded without a second click (F6-5): the consent was given per
// src in this container, and a re-render must not revoke it.
//
// AS DESIGNED (P3-9 review, recorded not fixed): re-loading a consented src on
// every debounced preview rebuild creates a fresh <img src> per keystroke.
// That is the browser cache's problem, and the browser owns it — an ordinary
// cacheable image is served from cache after the first load (these <img>
// loads carry no no-cache directive; only the viewer's DOCUMENT fetches use
// no-store), and a server that marks its images uncacheable has asked for
// exactly this traffic. Debouncing or memoizing loads here would duplicate
// the cache with a worse one.
function wireExternalImages(container) {
  for (const btn of container.querySelectorAll(".ext-img-load")) {
    wireLoadButton(container, btn);
  }
  const consented = loadedExternalSrcs.get(container);
  if (!consented || consented.size === 0) return;
  for (const holder of [...container.querySelectorAll(".ext-img")]) {
    if (consented.has(holder.dataset.src)) {
      holder.replaceWith(loadedExternalImage(
        container, holder.dataset.src, placeholderLabel(holder)));
    }
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
  // add-doxbench-editing-phase-a task 7.2: this button NAMES THE EXTERNAL
  // EDITOR. It used to read "✎ edit" and edit nothing in the app — while
  // `edit-document` / `edit-apply` are gate verbs and the doxBench canvas
  // beside it does in-app editing for real, so one bare word named three
  // structurally different acts. Behaviour is unchanged; only the claim is.
  const editBtn = el("button", "editbtn", "✎ open in editor");
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
  // READ-BACK SEAM (add-staged-topic-outline-template task 3.1's wiring), and
  // the reason it exists rather than a second fetch: this viewer OWNS the one
  // /source read for these bytes (D15), so a caller that needs the loaded text
  // for its own derivation — the outline tab, deriving the templated section
  // index — is handed the text the viewer already has. Called ONLY on a
  // successful load: a degraded or failed load leaves it silent, because the
  // viewer has already said so in its own body and a caller must not derive a
  // model from bytes that never arrived.
  const onText = typeof o.onText === "function" ? o.onText : null;

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
  if (onText) {
    // CONTAINED, IN BOTH SHAPES A CALLER CAN FAIL IN. Callers do not await this
    // function (the outline pane mounts it and moves on), so a failure while a
    // caller builds its own derivation would become a silent unhandled
    // rejection — and it would be the LAST statement that failed, after the
    // document itself had already rendered.
    //
    // A SYNCHRONOUS throw is caught below. An ASYNC `onText` never throws at
    // all: it hands back a rejected promise, which sails past a bare try/catch
    // untouched. Our one caller is synchronous today, so that half was latent —
    // but a containment claim true of only one of the two shapes is worse than
    // no claim, because this comment is what the next caller reads before
    // writing an async one (PR #208 review).
    //
    // Nothing is said on the page either way, beyond the derivation simply being
    // absent: the body above is already correct, and a message about a caller's
    // bug would libel the document.
    try {
      const derived = onText(text);
      // `.then(undefined, handler)` rather than `.catch`: only `then` is
      // required of a thenable, and this settles the rejection WITHOUT awaiting
      // it — the read is finished, and the viewer does not wait on anybody's
      // derivation to call itself done.
      if (derived && typeof derived.then === "function") {
        derived.then(undefined, () => {});
      }
    } catch (unused) { /* the caller's derivation, not the viewer's read */ }
  }
}
