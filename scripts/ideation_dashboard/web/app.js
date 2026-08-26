// Ideation-dashboard app shell (T009). The SNAPSHOT-ONLY data path: this module
// performs the ONE state fetch — the snapshot JSON — and every view renders
// from that in-memory object. The snapshot source is the adjacent
// ./snapshot.json (serve.py's route), addressed by the ACTIVE (repository, ref)
// pair when the serving side offers a snapshot INDEX
// (add-dashboard-repo-selector task 2.1): the key comes from that index's
// roster — never from the URL bar — which is why the former `?snapshot=` URL
// override stays removed (it fed query-string data into the fetch URL).
//
// REPOSITORY SWITCHING is deliberately a re-load of the shell rather than an
// in-place re-mount: every view caches its own derived model and its own
// listeners, so re-rendering the whole page against the newly chosen snapshot is
// both the honest and the cheap way to guarantee no view keeps another
// repository's state. The chosen key survives in sessionStorage — it is a
// viewer preference, not shared state — and it is RE-VALIDATED against the
// index roster on every boot, so a repository that has left the roster stops
// being requested instead of being fetched forever.
//
// The only other READ calls anywhere in the bundle go to the same read-only
// `/source/<path>` pass-through (D15, T018): dashboard STATE stays
// snapshot-only, but a document's CONTENT is always the source file, fetched
// read-only from the pinned checkout via serve.py — never duplicated into the
// snapshot. viewer.js reads a selected document that way; wheel.js's archived
// `landed` verb reads a realized change's spec deltas the same way. (The local
// action-center POSTs in dispose.js and notebook.js are the separate loopback
// action seam, gated on the capability probe below.)
//
// CROSS-VIEW NAVIGATION is app.js's job, exactly as the explorer -> viewer
// wiring is: the wheel's read-only verbs get `nav` callbacks (open a document in
// the viewer, jump to the lens/canvas with a preselection) rather than importing
// those views themselves.

import { renderFunnel } from "./views/funnel.js";
import { renderWheel } from "./views/wheel.js";
import { renderBoard } from "./views/board.js";
import { renderDocs } from "./views/docs.js";
import { renderLineage, renderStats } from "./views/lineage.js";
import { mountExplorer } from "./views/explorer.js";
import { renderViewer } from "./views/viewer.js";
import { createEditAction } from "./views/edit.js";
import { renderCanvas } from "./views/canvas.js";
import { renderLens } from "./views/lens.js";
import { isGateBearing, mountGateBar } from "./views/gate.js";
import { mountStagingWorkbench } from "./views/staging-workbench.js";
import { firstEditTransport } from "./views/swb-session.js";
import { CONSOLE_TOKEN_FIELD } from "./views/staging-workbench-model.js";
import { runSave, savePlanState } from "./views/doxbench-save.js";
import { contentIdentity } from "./views/doxbench-state.js";
import { initSettings } from "./views/settings.js";
import { initAccountMenu } from "./views/account-menu.js";
import { createNotebookAction, notebookCapable, postNotebookAction, probeCapabilities } from "./views/notebook.js";
import { fetchIndex, fetchProjects, mountRepoSelector, projectViewState, renderStaleBanner, storeViewState } from "./views/repo-selector.js";
import { composedView, isComposed, memberRef, readOnlyCaps, scopedSnapshot, visibleSnapshot } from "./views/composed-model.js";
import {
  freshnessLabel, keyId, resolveActive, resolveStoredKey, safeKey,
} from "./views/repo-selector-model.js";

const SNAPSHOT_SOURCE = "./snapshot.json";
// Where the viewer's chosen (repository, ref) lives across a shell reload. A
// per-tab preference, never shared state — `main` remains the shared truth.
const ACTIVE_KEY_STORAGE = "xf-ideation-active-key";

// D21 — the repository lens's DRILL-IN scope: a set of document identities
// the human activated from the bullseye, stored so the whole shell re-renders
// over it (the ratified reload-per-switch posture every other selector
// gesture uses) and cleared from one banner control.
const DRILL_SCOPE_STORAGE = "xfDashDrillScope";

// Both go through `guardedSessionStorage()` — the seam that survives blocked
// site data, where the storage GETTER itself throws (T104 F7-2).
function storedDrillScope() {
  const store = guardedSessionStorage();
  if (!store) return null;
  try {
    const raw = store.getItem(DRILL_SCOPE_STORAGE);
    const doc = raw ? JSON.parse(raw) : null;
    return doc && Array.isArray(doc.identities) && doc.identities.length
      ? doc : null;
  } catch {
    return null;
  }
}

function storeDrillScope(scope) {
  const store = guardedSessionStorage();
  if (!store) return;
  try {
    if (scope) store.setItem(DRILL_SCOPE_STORAGE, JSON.stringify(scope));
    else store.removeItem(DRILL_SCOPE_STORAGE);
  } catch { /* storage denied: the drill-in is simply not sticky */ }
}

// D21 — the drill-in banner: what the shell is scoped to, and the way out.
// Rendered into the stale-banner's neighbourhood so the two read as one strip
// of "what you are looking at" facts.
function renderDrillBanner(drill, snapshot) {
  const host = document.getElementById("drillbanner");
  if (!host) return;
  host.textContent = "";
  host.hidden = !drill;
  if (!drill) return;
  const shown = (snapshot?.documents || []).length;
  const line = document.createElement("span");
  line.className = "drillnote";
  // The two numbers differ by design and both matter: a drill-in selects
  // IDENTITIES, and each identity shows one document per carrying repository.
  const n = drill.identities.length;
  line.textContent = "drilled in: " + shown + " document"
    + (shown === 1 ? "" : "s") + " — " + n + " identit" + (n === 1 ? "y" : "ies")
    + " carried by " + (drill.label || "a region");
  host.appendChild(line);
  const clear = document.createElement("button");
  clear.type = "button";
  clear.className = "cbtn drillclear";
  clear.textContent = "clear";
  clear.title = "leave the drill-in and render the whole visible set again";
  clear.addEventListener("click", () => {
    storeDrillScope(null);
    render();
  });
  host.appendChild(clear);
}

function storedKey() {
  try {
    return window.sessionStorage.getItem(ACTIVE_KEY_STORAGE);
  } catch {
    return null;  // private-mode / file:// — the default key applies
  }
}

function storeKey(key) {
  try {
    window.sessionStorage.setItem(ACTIVE_KEY_STORAGE, keyId(key.repository, key.ref));
  } catch {
    /* a viewer preference that cannot be stored is not an error */
  }
}

// The doxBench storage seam's ONE read of the storage global (T104 F7-2).
// Under blocked site data the GETTER ITSELF throws SecurityError — the same
// fact the stored-key helper above documents and guards — yet the seam
// bundle read `window.sessionStorage` bare, inside main()'s single try, so a
// browser blocking cookies replaced the ENTIRE dashboard with a false "Could not
// load the snapshot" error. Guarded to null, blocked storage degrades to the
// documented no-persistence posture: the views treat an absent storage seam
// as "no persistence", and everything else still renders. Exported so the
// Node suite can drive the guard with a throwing getter.
export function guardedSessionStorage() {
  try {
    return window.sessionStorage;
  } catch {
    return null;  // blocked site data / no window: no persistence, no error
  }
}

// The snapshot URL for an active key: the same same-origin route, with the key
// as query parameters the serving-side registry resolves. No key (no index) is
// exactly today's request.
//
// `safeKey` is the gate, not decoration: the (repository, ref) pair is lifted out
// of a FETCHED index (and possibly out of sessionStorage before that), so it
// reaches this URL only as the model's allow-list rebuilt it — encoding alone
// would keep third-party characters in the request (jssecurity:S8476). A pair
// that cannot survive the allow-list is REFUSED, never quietly swapped for the
// default: main's snapshot rendered under another repository's header is the
// silent-wrong-data failure this whole change exists to end.
function snapshotUrl(active) {
  if (!active) return SNAPSHOT_SOURCE;
  const key = safeKey(active);
  if (!key) throw new Error("the snapshot index offers an unusable (repository, ref) pair");
  return SNAPSHOT_SOURCE + "?repository=" + encodeURIComponent(key.repository)
    + "&ref=" + encodeURIComponent(key.ref);
}

// The read-only /source base for an active key: the keyed form when a key is
// active (per-entry confinement server-side), the plain route otherwise. Same
// allow-list gate — an unusable pair falls back to the unkeyed route, which the
// snapshot fetch above has already refused to load in the first place.
function sourceBaseFor(active) {
  const key = safeKey(active);
  if (!key) return "/source/";
  return "/source/" + encodeURIComponent(keyId(key.repository, key.ref)) + "/";
}

// The doxBench SOURCE-LOADING seam (010-doxbench-editor-chat T023, PARTIAL
// SLICE). app.js's SECOND fetch site, and the only new one this slice adds:
// the SAME read-only /source pass-through the viewer already reads (D15),
// never a new route and never a duplicated Markdown/hash/sanitizer
// implementation of its own. `sourceBaseOf` is called AT LOAD TIME, never
// memoized, so a workbench re-key (routeWorkbenchScope, rekeyToSession,
// resetEndedSession) is honoured by the very next load with no seam of its
// own to keep in sync -- mirrors viewer.js's own fetchSource() shape exactly,
// which is the pinned, reviewed precedent for an injectable-but-visible
// fetch. Returns null on a non-ok response (the caller's own honest
// "unavailable" state), and never a `revision` -- this route does not
// evidence a per-file revision, and doxbench-editor.js already falls back to
// projection.source_revision. A thrown fetch error is NOT swallowed here;
// the caller already degrades honestly on a throw.
//
// T023 names the source/hash foundations plus catalog, chat, and Save
// transports. All of them are now realized: source loading and the shared hash
// authority here, the two model transports immediately below, and Save through
// swb-session.js's single request site. Their CONSUMER -- the chat UI itself --
// LANDED with T052-T054 (doxbench-chat-model.js / doxbench-chat.js and the
// shell's rail wiring), so the bundle below is fully consumed; this file
// still builds the transports and renders nothing with them.
export function createDoxBenchSourceLoader(sourceBaseOf, injectedFetch) {
  return async function loadDoxBenchSource(path) {
    const sourceBase = sourceBaseOf();
    const response = injectedFetch
      ? await injectedFetch(sourceBase + path, { cache: "no-store" })
      : await fetch(sourceBase + path, { cache: "no-store" });
    if (!response.ok) return null;
    return {
      content: await response.text(),
      ref: response.headers.get("X-Snapshot-Ref") || null,
    };
  };
}

// The doxBench MODEL-CATALOG and CHAT-TURN transport seams (T023 wire clause).
// app.js's third and fourth fetch sites, and the last two this slice adds.
//
// Both routes are RELEASED, enveloped, and validated server-side against the
// pinned contract-v1.27 schemas, which is what made these buildable: a browser
// transport for an unreleased shape would have been inventing the contract.
// They are composed exactly like createDoxBenchSourceLoader -- a module-scope
// factory closing over an injected fetch plus a CALL-TIME reader, returning one
// async function -- so a capability re-probe or a session re-key is honoured by
// the very next call with no seam of its own to keep in sync.
//
// These are TRANSPORTS and deliberately nothing more. They move bytes: they
// build no request envelope, read no field of either payload, render nothing,
// and persist nothing. Interpreting a catalog or a turn result belongs to the
// chat model and view (T052-T054, landed 2026-07-31), and the transport-pin
// suite enforces that boundary by banning envelope/field spellings here.
//
// The ONE header they carry is the console-presence token the edit transport
// already carries (FR-019's third clause) -- never a provider credential, of
// which the browser holds none and can hold none (FR-020/FR-022).
const CATALOG_ROUTE = "/workbench/model-catalog";
const CHAT_TURN_ROUTE = "/actions/workbench/chat-turn";
// add-doxbench-editing-phase-b task 9.5: the THREAD READ route. A GET, and only
// a GET — a thread is written by a TURN, through the Save gate, and this seam
// has no write to offer.
const THREAD_ROUTE = "/workbench/thread";
// add-doxbench-distilled-abstract §5 / ruling 1(c)(i): the DOCUMENT-ABSTRACT
// route. A NEW same-origin serve.py route rather than a scoped chat turn --
// the chat-turn assembler is chat-shaped (it requires an outline buffer, a
// non-blank human message and a transcript) and an abstract request carries
// none of them, so smuggling one through that envelope would have meant
// widening a released contract to carry a request it was not written for.
// The request is a CLOSED shape: a scope, a subject path and a model id. It
// carries NO buffer, because the server reads the subject's SAVED bytes --
// which is also why unsaved text can never leave this browser through it.
const DOCUMENT_ABSTRACT_ROUTE = "/actions/workbench/document-abstract";
const CONSOLE_TOKEN_HEADER = "X-XF-Console-Token";

export function createDoxBenchCatalogLoader(consoleTokenOf, injectedFetch) {
  return async function loadDoxBenchCatalog() {
    // PR #63 review (Copilot): a MISSING token omits the header entirely --
    // never a literal "undefined"/"null" value; the server's console gate
    // then refuses honestly.
    const consoleToken = consoleTokenOf();
    const options = {
      cache: "no-store",
      headers: consoleToken ? { [CONSOLE_TOKEN_HEADER]: consoleToken } : {},
    };
    // The literal call site names its route: the transport-pin suite budgets
    // call sites individually, so an anonymous pass-through would make the
    // cap meaningless.
    const response = injectedFetch
      ? await injectedFetch(CATALOG_ROUTE, options)
      : await fetch(CATALOG_ROUTE, options);
    // A refusal is a DISTINGUISHED fixed failure, never a bare null (T104
    // F10-1): null collapsed a 403 stale console token (recoverable — reload)
    // and a 500 broken catalog (could not be read) into one misdiagnosis,
    // "no approved model is configured". The body's released error code picks
    // between exactly TWO fixed markers — the pre-identity console refusals
    // (`console_required` on the doxBench routes, `agent_invocation` on the
    // gate-action route: the R-3 pair) map to the stale-token posture,
    // everything else to unreadable — and NOTHING else from the body is
    // carried (FR-020/FR-022: no message, no echo). This is still a
    // transport-shaped answer: one error-code read to pick a marker, no
    // envelope field interpreted, nothing rendered or persisted. An EMPTY
    // approved list is NOT a refusal -- the released schema calls it a
    // success (FR-025/SC-008) -- so it comes back as the envelope it is.
    if (!response.ok) {
      const body = await response.json().catch(() => null);
      const code = body && body.error;
      return Object.freeze({
        failed: code === "console_required" || code === "agent_invocation"
          ? "console_required" : "unreadable",
      });
    }
    // A 200 with an unparseable body returns null -- the transport invents
    // no envelope, matching the turn submitter's own catch below (PR #63
    // triage item 14). What the CONSUMER does with that null (P3-11 fixed
    // this comment's drift): the rail's one-shot catalog path records it as
    // the catalog-UNREADABLE failure -- "the model catalog could not be
    // read" -- NOT the editor-only configured-none posture this line used to
    // claim. An answer that cannot be read is a failure fact with its own
    // remedy, never evidence that nothing is configured (T104 F10-1).
    return response.json().catch(() => null);
  };
}

export function createDoxBenchThreadLoader(consoleTokenOf, injectedFetch) {
  // A TRANSPORT MOVES BYTES. It names no field of the query it carries: the
  // caller hands over an already-built parameter object, exactly as the turn
  // submitter is handed an already-built request envelope, so this function
  // cannot grow into the thing that decides what a thread request says.
  return async function loadDoxBenchThread(query) {
    // Same missing-token rule as the two transports above.
    const consoleToken = consoleTokenOf();
    const options = {
      cache: "no-store",
      headers: consoleToken ? { [CONSOLE_TOKEN_HEADER]: consoleToken } : {},
    };
    const threadUrl =
      THREAD_ROUTE + "?" + new URLSearchParams(query || {}).toString();
    const response = injectedFetch
      ? await injectedFetch(threadUrl, options)
      : await fetch(threadUrl, options);
    // EVERY refusal is the SAME answer here, and deliberately: the four
    // absences task 9.5 enumerates — the hosted plane, no gate capability, an
    // unresolved actor, no live session — are one posture on this surface,
    // "this document has no readable thread", and the rail renders it as the
    // honest empty transcript. Nothing from the body is carried (FR-020/
    // FR-022): the rail states an absence, it never quotes a server.
    if (!response.ok) return null;
    return response.json().catch(() => null);
  };
}

export function createDoxBenchTurnSubmitter(consoleTokenOf, injectedFetch) {
  return async function submitDoxBenchTurn(request) {
    // Same missing-token rule as the catalog loader (PR #63 review).
    const consoleToken = consoleTokenOf();
    const options = {
      method: "POST",
      headers: consoleToken
        ? { "Content-Type": "application/json",
            [CONSOLE_TOKEN_HEADER]: consoleToken }
        : { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    };
    const response = injectedFetch
      ? await injectedFetch(CHAT_TURN_ROUTE, options)
      : await fetch(CHAT_TURN_ROUTE, options);
    // Status AND payload, both surfaced: a turn refusal carries meaning the
    // caller must act on, so unlike the catalog this never collapses to null.
    // An unparseable body becomes `payload: null` rather than a throw or an
    // invented shape -- the caller decides what an unreadable answer means.
    const payload = await response.json().catch(() => null);
    return { ok: response.ok, status: response.status, payload };
  };
}

export function createDoxBenchAbstractRequester(consoleTokenOf, injectedFetch) {
  return async function requestDoxBenchAbstract(request) {
    // Same missing-token rule as the three transports above (PR #63 review): a
    // MISSING token omits the header entirely rather than sending a literal
    // "undefined", so the server's console gate refuses honestly.
    const consoleToken = consoleTokenOf();
    const options = {
      method: "POST",
      headers: consoleToken
        ? { "Content-Type": "application/json",
            [CONSOLE_TOKEN_HEADER]: consoleToken }
        : { "Content-Type": "application/json" },
      // The caller hands over an already-built request. A TRANSPORT MOVES
      // BYTES: this function names no field of what it carries, so it cannot
      // grow into the thing that decides what an abstract request says.
      body: JSON.stringify(request),
    };
    const response = injectedFetch
      ? await injectedFetch(DOCUMENT_ABSTRACT_ROUTE, options)
      : await fetch(DOCUMENT_ABSTRACT_ROUTE, options);
    // Status AND payload, both surfaced, exactly like the turn submitter: an
    // abstract refusal is STATED and the region renders which class it was, so
    // this never collapses to null. An unparseable body becomes `payload:
    // null` rather than a throw or an invented shape -- the caller decides what
    // an unreadable answer means.
    const payload = await response.json().catch(() => null);
    return { ok: response.ok, status: response.status, payload };
  };
}

// ---- the console-token REPAIR (Brett, 2026-08-09) --------------------------
//
// A serve restart mints a new console token. The page read `/capabilities` once,
// at load, so from that moment every guarded write is refused — and because the
// shell now re-renders IN PLACE rather than navigating, nothing ever re-reads it.
// This is the one thing that does.
//
// It re-probes through `probeCapabilities` — the SAME same-origin GET the boot
// already performs, so no new route and no new fetch call site — and MUTATES the
// capability objects the views hold. Mutation is the point: `swb-create.js`,
// `swb-session.js` and `edit.js` were handed these objects by reference and read
// `console_token` at call time, so writing into them repairs every guarded
// surface at once. Handing back a fresh object would repair nothing they can see.
//
// Returns whether the re-read produced a USABLE token — the one question the
// retry decision turns on. It is deliberately NOT "did the token change": two
// writes refused at the same instant would both re-probe, and the second would
// be told "unchanged" by its own sibling's repair and stranded for no reason. A
// false here means the plane answered with no console at all (its session
// capability is gone, or the probe failed and degraded), and retrying THAT would
// refuse identically. The policy acting on this answer — and the two-attempt cap
// that stops it becoming a loop — is `withConsoleRepair` in
// staging-workbench-model.js.
export function createConsoleRepair(capsObjects, probe) {
  const readCapabilities = probe || probeCapabilities;
  return async function repairConsoleToken() {
    const fresh = await readCapabilities();
    const token = fresh && fresh[CONSOLE_TOKEN_FIELD];
    if (typeof token !== "string" || !token) return false;
    for (const caps of capsObjects || []) {
      if (caps) caps[CONSOLE_TOKEN_FIELD] = token;
    }
    return true;
  };
}

async function loadSnapshot(active) {
  // The one and only STATE fetch in the whole renderer — a same-origin path
  // whose only variable part is an index-supplied (repository, ref) key.
  const response = await fetch(snapshotUrl(active), { cache: "no-store" });
  if (!response.ok) throw new Error("snapshot fetch failed: HTTP " + response.status);
  return response.json();
}

// ---- theme toggle (light/dark, mockup theming) ----
function themeLabel(mode) {
  if (mode === "dark") return "☾ dark";
  if (mode === "light") return "☀ light";
  return "◐ auto";
}

// auto -> light -> dark -> auto
function nextThemeMode(mode) {
  if (mode === null) return "light";
  if (mode === "light") return "dark";
  return null;
}

function initTheme() {
  const btn = document.getElementById("themebtn");
  if (!btn) return;
  const apply = (mode) => {
    if (mode) document.documentElement.dataset.theme = mode;
    else delete document.documentElement.dataset.theme;
    btn.textContent = themeLabel(mode);
  };
  let mode = null; // auto (follow prefers-color-scheme)
  btn.addEventListener("click", () => {
    mode = nextThemeMode(mode);
    apply(mode);
  });
  apply(mode);
}

// ---- tab router ----
// `onOpenTile` is the funnel/board tiles' drill-down entrypoint (T017):
// staged/proposal/realized cards call it with (kind, id); the explorer
// resolves the snapshot-only folder listing and renders the overlay.
const TABS = [
  { tab: "tab-funnel", view: "view-funnel",
    render: (root, snap, ctx) => renderFunnel(root, snap, {
      onOpenTile: ctx.explorer.openTile, notebook: ctx.notebook,
      signal: ctx.signal }) },
  { tab: "tab-wheel", view: "view-wheel",
    render: (root, snap, ctx) => renderWheel(root, snap,
      { caps: ctx.caps, nav: ctx.nav, notebook: ctx.notebook,
        sourceBase: ctx.sourceBase, composed: ctx.composed,
        signal: ctx.signal }) },
  { tab: "tab-board", view: "view-board",
    render: (root, snap, ctx) => renderBoard(root, snap, { onOpenTile: ctx.explorer.openTile, notebook: ctx.notebook }) },
  { tab: "tab-canvas", view: "view-canvas",
    render: (root, snap, ctx) => renderCanvas(root, snap, { notebook: ctx.notebook }) },
  { tab: "tab-lens", view: "view-lens",
    // D21: the lens receives the UNNARROWED composed snapshot as well as the
    // rendered one. Its repository rail is the control surface for the
    // visible set, so it must see every member — the narrowed view could only
    // ever shrink further, never restore a repository the human unticked.
    render: (root, snap, ctx) => renderLens(root, snap, {
      caps: ctx.caps,
      composedSnapshot: ctx.rawSnapshot,
      visible: ctx.visible,
      onVisible: ctx.onVisible,
      onDrillIn: ctx.onDrillIn,
      // lens -> doxBench (Brett, 2026-08-08: "we need to have button to move
      // this to doxBench. and open the doxBench UI if the user moves
      // forward"). The same cross-view ownership every other jump has: the
      // view declares the verb, app.js performs it.
      onOpenDoxbench: ctx.nav.openDraft,
      // when the serve itself cannot create, and a drafted seed belongs to
      // exactly ONE member, the lens offers the jump to it rather than
      // telling the human to perform the switch themselves
      onOpenRepository: ctx.nav.openRepository,
      // AUTHORING FROM A COMPOSED VIEW (Brett, 2026-08-08: "yes, we need to
      // draft from a project view"). D10 strips every acting capability on a
      // composed snapshot because "a gate verb binds to one served checkout,
      // and a composed view has none" — true of a verb bound to a TILE, whose
      // repository this serve has no writable checkout for. A NEW staging
      // document binds to no tile: it lands in the serve's OWN checkout,
      // which exists and is writable. So this ONE affordance reads the
      // unstripped capability and the serve's own repository, and nothing
      // else on the composed view changes.
      createCaps: ctx.probedCaps,
      writableRepository: ctx.writableRepository,
    }) },
  // The doc list's rows open the SAME read-only explorer/viewer overlay the
  // wheel's `read` verb and the workbench's docs rows open (T092 acceptance
  // sweep, defect 7 — the rows advertised themselves as clickable and were
  // inert). app.js owns every cross-view jump, so the view declares the row and
  // calls back here; `ctx.nav.openDoc` is the one entry point.
  { tab: "tab-docs", view: "view-docs",
    render: (root, snap, ctx) => renderDocs(root, snap, { onOpenDoc: ctx.nav.openDoc }) },
  { tab: "tab-lineage", view: "view-lineage", render: (root, snap) => renderLineage(root, snap) },
];

// Tab router with the WAI-ARIA roving-tabindex pattern (a11y #19): only the
// selected tab is in the tab order (tabindex 0); arrows/Home/End move focus and
// activate. Also owns the global-search fan-out (#13): the active view's
// controller may expose `search(term)`, re-applied whenever the tab changes so
// a filter persists across tab switches.
// The "what is this?" popup (Brett, 2026-08-08). A native <dialog>: one
// listener to open it, and the platform's own Escape/backdrop handling to
// close. Guarded because the static image may serve an older index.
function initAbout(signal) {
  const link = document.getElementById("aboutlink");
  const dialog = document.getElementById("aboutdialog");
  if (!link || !dialog || typeof dialog.showModal !== "function") return;
  link.addEventListener("click", () => dialog.showModal(), { signal });
}

// WHERE THE HUMAN WAS (Brett, 2026-08-09: "currently we take the user back to
// home page and the user must drill back to where they were"). Five different
// controls store a key and reload — the repository jump, the repository/project
// selector, a refresh, and clearing a drill-in — and every one of them landed
// on the first tab, so a jump taken FROM the wheel arrived on the funnel.
//
// The tab is the right thing to keep, and the only thing: after a repository
// jump the tile you were on does not exist in the repository you jumped to,
// which is the point of jumping. Restoring the VIEW puts you where you were
// looking; restoring a tile would be restoring something that is gone.
const ACTIVE_TAB_STORAGE = "opendox.active-view";

function storedTab() {
  const store = guardedSessionStorage();
  try {
    return store ? store.getItem(ACTIVE_TAB_STORAGE) : null;
  } catch {
    return null;   // blocked site data: the default tab applies, as before
  }
}

function storeTab(view) {
  const store = guardedSessionStorage();
  try {
    if (store) store.setItem(ACTIVE_TAB_STORAGE, String(view));
  } catch {
    /* a viewer preference that cannot be stored is not an error */
  }
}

function initTabs(snapshot, ctx, signal) {
  const controllers = {};
  const rendered = new Set();
  const tabEls = TABS.map((t) => document.getElementById(t.tab));
  let current = TABS[0];
  let searchTerm = "";

  function applySearch() {
    const c = controllers[current.view];
    if (typeof c?.search === "function") c.search(searchTerm);
  }

  function show(target, focusTab) {
    current = target;
    storeTab(target.view);
    TABS.forEach((t, i) => {
      const isTarget = t.tab === target.tab;
      tabEls[i].setAttribute("aria-selected", String(isTarget));
      tabEls[i].tabIndex = isTarget ? 0 : -1;
      document.getElementById(t.view).hidden = !isTarget;
    });
    // The LENS takes the whole page (Brett, 2026-08-08: "when we are on the
    // lens screen we want to remove anything not lens related… give as much
    // screen as possible to the radar widget and the list of documents
    // below"). The stage tiles head the stage views — funnel, wheel, board —
    // and say nothing about a keyword or repository set, so the lens hides
    // them and takes the height back.
    document.querySelector(".wrap")
      ?.classList.toggle("lensfull", target.view === "view-lens");
    if (focusTab) document.getElementById(target.tab).focus();
    // lazy render on first activation; funnel edge geometry needs a visible layout
    if (!rendered.has(target.view)) {
      controllers[target.view] = target.render(document.getElementById(target.view), snapshot, ctx);
      rendered.add(target.view);
    } else if (controllers[target.view]?.redraw) {
      controllers[target.view].redraw();
    }
    applySearch();
  }

  function onTabKey(ev, i) {
    let next = -1;
    if (ev.key === "ArrowRight" || ev.key === "ArrowDown") next = (i + 1) % TABS.length;
    else if (ev.key === "ArrowLeft" || ev.key === "ArrowUp") next = (i - 1 + TABS.length) % TABS.length;
    else if (ev.key === "Home") next = 0;
    else if (ev.key === "End") next = TABS.length - 1;
    else return;
    ev.preventDefault();
    show(TABS[next], true);
  }

  TABS.forEach((t, i) => {
    // scoped to the RENDER: the tab strip is persistent DOM, so an unscoped
    // binding here would stack one router on top of another
    tabEls[i].addEventListener("click", () => show(t, false), { signal });
    tabEls[i].addEventListener("keydown", (ev) => onTabKey(ev, i), { signal });
  });
  // Open where the human was, if that view still exists on this plane — a tab
  // list can differ between planes, and a remembered view that is gone falls
  // back to the first exactly as before.
  const remembered = TABS.find((t) => t.view === storedTab());
  show(remembered || TABS[0], false);

  return {
    search(term) { searchTerm = String(term || ""); applySearch(); },
    // Programmatic tab activation for the wheel's nav verbs: activates the tab
    // (rendering it on first activation, exactly like a click) and returns that
    // view's controller so the caller can hand it a preselection.
    goto(view) {
      const target = TABS.find((t) => t.view === view);
      if (!target) return null;
      show(target, false);
      return controllers[view] || null;
    },
  };
}

// Always-visible staleness stamp (#8): "snapshot: <rev12> · generated <date>
// (<N days ago>)" with the age computed CLIENT-SIDE from generation.generated_at
// — amber past 24h, red past 72h. Reads only fields the snapshot already
// carries (source_revision + generated_at); no new data path.
function ageLabel(days) {
  if (days <= 0) return " (today)";
  if (days === 1) return " (1 day ago)";
  return " (" + days + " days ago)";
}

function staleClass(hours) {
  if (hours > 72) return "stale-red";
  if (hours > 24) return "stale-amber";
  return null;
}

function renderHeader(snapshot, active) {
  const asof = document.getElementById("asof");
  const gen = snapshot.generation || {};
  const rev = gen.source_revision ? gen.source_revision.slice(0, 12) : "unknown";
  const genAt = gen.generated_at || "";
  const when = genAt ? genAt.slice(0, 10) : "unknown";

  asof.classList.remove("stale-amber", "stale-red");
  let ageText = "";
  const genMs = genAt ? Date.parse(genAt) : Number.NaN;
  if (!Number.isNaN(genMs)) {
    const hours = (Date.now() - genMs) / 3600000;
    ageText = ageLabel(Math.floor(hours / 24));
    const cls = staleClass(hours);
    if (cls) asof.classList.add(cls);
  }
  // the dot then the stamp line, both composed as nodes (no markup strings)
  asof.textContent = "";
  const dot = document.createElement("span");
  dot.className = "stampdot";
  asof.appendChild(dot);
  asof.appendChild(document.createTextNode("snapshot: " + rev + " · generated " + when + ageText));

  // The repo chip retired with add-opendox-project-header (D12): the
  // freshness header below already names `repo @ ref`, and the project
  // dropdown carries the grouping context.

  // The FRESHNESS HEADER (design D11): `repo @ ref · short SHA · generated-at`,
  // on every plane, so "is the document I just landed in this view" is answered
  // without reasoning about deployment times.
  const fresh = document.getElementById("freshness");
  if (fresh) {
    fresh.textContent = freshnessLabel(active, snapshot);
    if (active?.origin) fresh.dataset.origin = active.origin;
    fresh.classList.toggle("fallback", active?.stale === true);
  }
}

// THE RENDER SCOPE (Brett, 2026-08-09: "yes, get rid of the flash too").
//
// Switching repository, project, drill scope or refreshing used to reload the
// page. Re-rendering in place instead means every listener and observer a
// render installs must come OFF before the next one goes on — otherwise the
// second Escape press runs two handlers, the third runs three, and the leak
// grows with every switch.
//
// One AbortController per render is the whole mechanism: everything a render
// binds passes `{ signal }`, and starting the next render aborts the last,
// which unbinds all of it at once. A view needs no `destroy()` and no
// bookkeeping — it just honours the signal it is handed, which is a rule that
// cannot be half-applied without the leak test noticing.
let renderScope = null;

// The account menu (views/account-menu.js) is a corner control like the
// settings gear: bound ONCE for the life of the page (it owns no snapshot
// state, so a re-render must not rebind it and leak listeners/asides). It reads
// the signed-in identity + derived access level from the SAME `/capabilities`
// object the render already probes, handed to it via `update()` after each
// probe — so the menu needs no fetch of its own.
let accountMenu = null;

function nextRenderScope() {
  if (renderScope) renderScope.abort();
  renderScope = new AbortController();
  return renderScope.signal;
}

async function main() {
  initTheme();
  // The settings gear (views/settings.js): pure viewer preferences in
  // localStorage, applied LIVE by event — deliberately wired before the
  // snapshot load, since it has no data dependency and must work even if the
  // snapshot fetch fails. Bound ONCE for the life of the page: it owns no
  // snapshot state, so a re-render must not rebind it.
  initSettings();
  // The account menu, wired beside the settings gear and bound once. It has no
  // capabilities yet (the render below probes `/capabilities`); it renders a
  // graceful "local session" default until `render()` hands it the probed
  // verdict via `accountMenu.update(...)`.
  accountMenu = initAccountMenu({ buttonId: "accountbtn" });
  await render();
}

async function render() {
  const signal = nextRenderScope();
  const status = document.getElementById("loadstatus");
  try {
    // The snapshot INDEX (add-dashboard-repo-selector): the roster the selector
    // renders and the freshness the header shows. Absent (a static image, an
    // older server) means one repository and today's behaviour — the whole
    // control simply does not render.
    const index = await fetchIndex();
    // The register PROJECTION (add-project-scoped-selection): the project
    // picker's roster. The snapshot index is a locator and carries no
    // grouping, so the projects come from the served register projection —
    // absent (static image, no reachable register), the picker hides.
    const projects = await fetchProjects();
    // The stored key is a viewer PREFERENCE, not an instruction: it becomes the
    // active pair only when THIS index still advertises it (resolveStoredKey).
    // A repository that has left the roster — or a stored value that is not
    // request-safe — resolves to null, and the default applies exactly as if
    // nothing had been stored.
    const active = resolveActive(index, resolveStoredKey(index, storedKey()));
    const rawSnapshot = await loadSnapshot(active);
    // add-project-merged-projection (D9/D10): a COMPOSED snapshot renders
    // through ONE derived view — same-topic clusters unioned — and every
    // acting capability stripped. The RAW snapshot keeps the freshness
    // header honest (`composed_from` is what the label reads).
    const composed = isComposed(rawSnapshot);
    // D19 (Brett, 2026-08-07): the composed snapshot renders the VISIBLE
    // member set under the stored view mode — union (everything from the
    // ticked repositories) or shared (only what two or more of them carry,
    // the D20 threshold). Narrow FIRST, union after: the cluster union then
    // sums tallies over the visible set instead of the whole project. The
    // narrowed snapshot also carries the trimmed `composed_from`, so the
    // freshness header names the repositories actually on screen.
    // A DERIVED aggregate is keyed by its project id and `composed_from`
    // names the members, so the view state resolves from the snapshot alone.
    // A hand-declared aggregate simply has no stored entry: every member,
    // union — exactly the pre-D19 render.
    const view = composed ? projectViewState({
      id: rawSnapshot.repository,
      repositories: rawSnapshot.generation.composed_from
        .map((m) => m && m.repository).filter(Boolean),
    }) : null;
    const narrowed = composed
      ? visibleSnapshot(rawSnapshot, view.visible, view.mode)
      : rawSnapshot;
    // D21 — the repository lens's DRILL-IN: a stored region scopes the whole
    // shell to that document set. Applied AFTER the visible-set narrowing and
    // BEFORE the cluster union, so the wheels, the explorer and the stats all
    // count the same documents; a scope whose identities no longer resolve
    // simply drops (nothing to show is reported by the banner, not by an
    // empty page with no explanation).
    const drill = composed ? storedDrillScope() : null;
    const shown = drill ? scopedSnapshot(narrowed, drill.identities) : narrowed;
    const snapshot = composed ? composedView(shown) : rawSnapshot;
    renderHeader(shown, active);
    renderDrillBanner(drill, shown);
    // The banner carries the STALE-FALLBACK warning only (Brett, 2026-08-08:
    // "we do not need this bar, it takes too much screen"). The sparse note
    // it used to add — "no possibles in X, a sparse funnel is an honest
    // funnel" — spent a full row restating what the empty STATIONS already
    // say in place, which is where the requirement actually puts it
    // ("a station with no data MUST render an explicit empty state naming
    // what is absent"). A genuinely stale fallback still never renders
    // silently.
    renderStaleBanner(document.getElementById("stalebanner"), active);
    // The grouping roll-up strip retired with the project-first header
    // (Brett's 2026-08-06 annotation: "with our new project and filter
    // boxes, we do not need this row anymore") — the project dropdown and
    // repo filter are where grouping now surfaces; the pure grouping
    // view-model module remains available to any view that wants a roll-up,
    // and the retired-everywhere guard in test_grouping.py pins that no
    // mount returns.
    renderStats(document.getElementById("stats"), snapshot);
    const explorerRoot = document.getElementById("explorer-root");
    // The explorer (T017) has no compile-time dependency on the viewer
    // (T018); app.js is what wires a selected file to renderViewer (D15
    // read-only Markdown pass-through).
    // A composed snapshot carries each projected item's member key. Resolve
    // content/edit routing from that item, never from the aggregate id (which is
    // a view, not a SnapshotEntry). A non-composed snapshot falls back to its
    // active key exactly as before.
    const sourceKeyFor = (entry) => {
      const explicit = safeKey(entry?.sourceKey);
      if (explicit) return explicit;
      const repository = entry?.repository || entry?.doc?.repository;
      let ref = entry?.ref || entry?.doc?.ref;
      const members = snapshot.generation?.composed_from;
      if (repository && !ref && Array.isArray(members)) {
        ref = members.find((member) => member?.repository === repository)?.ref;
      }
      if (repository) return safeKey({ repository, ref });
      if (Array.isArray(members)) return null;
      return safeKey(active) || safeKey({
        repository: snapshot.repository, ref: "main",
      });
    };
    const gateContext = (tile, entry, key) =>
      tile?.kind === "proposal" && isGateBearing(entry.path) && key
        ? { changeId: tile.id, repository: key.repository }
        : null;
    // The ONE capability probe (#1): a same-origin GET the local backend answers
    // and the static served image 404s. It also carries the per-serve console
    // token used by guarded human actions.
    const probedCaps = await probeCapabilities();
    // Hand the corner account menu the freshly probed verdict — it reads the
    // signed-in identity (`hosted_actor`) and derives the access level from this
    // SAME object, so it needs no fetch of its own. The RAW probe (before the
    // composed read-only strip below): the account menu states the serve's own
    // posture and identity, not the composed view's stripped affordances.
    if (accountMenu) accountMenu.update(probedCaps);
    // D10: a composed render strips every acting capability in ONE place, so
    // every view's existing capability check is the whole gating.
    const caps = composed ? readOnlyCaps(probedCaps) : probedCaps;
    // BOTH objects, because `readOnlyCaps` copies: `probedCaps` is what the
    // workbench's `openDraft` creates through (the serve's own posture), `caps`
    // is what every tile-bound surface reads. On a single-repository view they
    // are the same object, so the list is one object named twice — harmless,
    // and cheaper than deciding which of the two this render produced.
    const consoleRepair = createConsoleRepair([probedCaps, caps]);
    const explorer = mountExplorer(explorerRoot, snapshot, {
      signal,
      onOpenFile: (entry, pane, tile) => {
        const sourceKey = sourceKeyFor(entry);
        return renderViewer(pane, {
          path: entry.path,
          doc: entry.doc,
          sourceBase: sourceBaseFor(sourceKey),
          edit: createEditAction({ caps, key: sourceKey }),
          gate: gateContext(tile, entry, sourceKey),
          mountGate: (host, gctx) => mountGateBar(host, gctx, { caps }),
        });
      },
    });
    // When the capability probe reports the notebook action
    // available, tiles grow an "Open in NotebookLM" affordance; otherwise the
    // controller's button() returns null and nothing renders — the served/local
    // seam made visible with zero per-view branching.
    const notebook = createNotebookAction({ enabled: notebookCapable(caps), post: postNotebookAction });
    // The STAGING WORKBENCH overlay (add-staging-workbench): the scoped view the
    // wheel's `open workbench` verb opens. Mounted once, like the explorer; a
    // docs row jumps into the SAME explorer/viewer overlay the rest of the
    // dashboard reads documents through. NOT the workbench reference-set family
    // (workbench.py) — see the module's own naming note.
    // `caps` (add-workbench-bullseye-and-create task 5.1) is what makes the
    // workbench's posture pill honest and its writes — the human-only
    // create-document and branch-session gate verbs — live affordances on a
    // loopback bind and copyable CLI descriptors everywhere else. The overlay
    // itself carries no transport; its siblings swb-create.js and swb-session.js
    // take this same seam.
    // `active` + `index` (007-workbench-branch-sessions T082) are what make the
    // BRANCH-SESSION posture honest: the key this page's snapshot was fetched with
    // (so the workbench knows whether it is a DRAFT view) and the roster a live
    // session appears in as an ordinary (repository, ref) row (FR-014/FR-045).
    // Both are already loaded here; the workbench derives, and asks nothing new.
    //
    // Workbench routing is deliberately separate from the shell/explorer. A
    // draft re-key therefore cannot leak into a main document after the overlay
    // closes, while the created-document jump can still name the session key.
    let workbenchSourceKey = sourceKeyFor(null);
    let workbenchSourceBase = sourceBaseFor(workbenchSourceKey);
    const workbenchEdit = createEditAction({
      caps, key: () => workbenchSourceKey,
    });
    const routeWorkbenchScope = (item) => {
      const next = sourceKeyFor({ doc: item });
      if (!next) return null;
      workbenchSourceKey = next;
      workbenchSourceBase = sourceBaseFor(next);
      return { active: next, sourceBase: workbenchSourceBase };
    };
    // The header's own mount, held so a session that opens mid-page can nudge it
    // (below). Assigned further down, after the selector is built; only ever
    // read from a callback that runs on a human action, so the order is safe.
    let repoSelector = null;
    const rekeyToSession = async (ref) => {
      // THE SERVE'S OWN REPOSITORY FIRST (Brett, 2026-08-10 — measured: the
      // create landed and the page then asked for
      // `snapshot.json?repository=xfactory&ref=draft/…` and got
      // `404 no such snapshot`, so the session opened and its document view
      // never did). A session ref can only exist in the repository this serve
      // WRITES to — a create naming any other is refused by the route
      // (`refuse_foreign_repository`) — and `/capabilities` declares it. The
      // view's own key is not that answer: under a composed project view
      // `sourceKeyFor(null)` is null and the fallbacks below resolve to the
      // PROJECT id, which names no repository. This is the same ruling the
      // create itself already follows (lens.js `writableRepository`), applied
      // to the re-key that follows it — the browser never INFERS the
      // repository a session lives in.
      const repository = probedCaps?.repository
        || workbenchSourceKey?.repository
        || active?.repository || snapshot.repository;
      const key = safeKey({ repository, ref });
      if (!key) return null;
      const next = {
        ...workbenchSourceKey, repository: key.repository, ref: key.ref,
      };
      const nextSourceBase = sourceBaseFor(next);
      const nextIndex = await fetchIndex();
      const nextSnapshot = await loadSnapshot(next);
      workbenchSourceBase = nextSourceBase;
      workbenchSourceKey = next;
      // TELL THE HEADER (2026-08-10). The session is now an ordinary row in the
      // serving index, and the header's repo filter is the one control that can
      // address it — but the selector holds the roster it booted with and only
      // re-derived it on a five-minute poll. So the branch the human just
      // created was missing from the only way back to it until the page
      // reloaded. Nudging the selector's own poll re-reads the index once and
      // re-renders its rows; nothing else about the shell moves.
      repoSelector?.poll?.();
      return { active: next, index: nextIndex || index, snapshot: nextSnapshot,
               sourceBase: nextSourceBase };
    };
    // An abandon or already-merged save retires the session registry entry.
    // Fetch main first, then let the workbench atomically adopt its snapshot,
    // index, source routing, and edit key before the ending re-renders.
    const resetEndedSession = async () => {
      const repository = workbenchSourceKey?.repository
        || active?.repository || snapshot.repository;
      const next = safeKey({ repository, ref: "main" });
      if (!next) return null;
      const nextSourceBase = sourceBaseFor(next);
      // Do not change either route unless main is readable. If refresh fails,
      // the retained branch view keeps its branch edit key; a retired entry then
      // fails closed instead of opening the same path from the wrong checkout.
      const nextIndex = await fetchIndex();
      const nextSnapshot = await loadSnapshot(next);
      workbenchSourceBase = nextSourceBase;
      workbenchSourceKey = next;
      return { active: next, index: nextIndex || index, snapshot: nextSnapshot,
               sourceBase: nextSourceBase };
    };
    // The doxBench seam bundle (T023): the source loader closed over the
    // workbench's OWN live routing variable (never a snapshotted base, so a
    // re-key is honoured by the next load), the shared hash authority, the
    // governed Save seam, and -- once the contract was released and pinned --
    // the two model transports, each closed over the CAPS-derived console token
    // read at call time. `mountStagingWorkbench` forwards loadSource/hash/save
    // into `mountDoxBenchCanvas` and `catalog`/`chatTurn` into the T055 chat
    // rail -- every bundled seam now has its consumer (T052-T055 landed). This file only builds the seam -- it never renders or
    // persists anything with it.
    const doxbenchSeams = {
      // R-1 (2026-08-02): the per-key working-state store. Injected here, at
      // the composition root, exactly like every other seam — the views never
      // reach for a storage global (the privacy needles ban that), and a
      // caller that supplies none simply gets no persistence. The VALUE is
      // guarded (T104 F7-2): the sessionStorage getter throws under blocked
      // site data, and unguarded it took the whole dashboard down as a false
      // snapshot error; null here is the honest no-persistence posture.
      storage: guardedSessionStorage(),
      loadSource: createDoxBenchSourceLoader(() => workbenchSourceBase),
      hash: contentIdentity,
      // THE SAVE SCOPE RIDES THE REQUEST (add-doxbench-editing-phase-b, design
      // D4), as DEFENCE IN DEPTH — and this note says so plainly because an
      // earlier version of it claimed a guard it did not have (PR #207 review,
      // F7).
      //
      // What actually narrows a `docs` tile's Save is the CANVAS: `save({only})`
      // filters the buffer set to the named documents plus the outline BEFORE it
      // builds the request, so the request already carries only those rows and
      // `runSave` would persist only those rows whether or not the scope came with
      // it. Forwarding it makes `runSave`'s own scope AGREE with the request's
      // instead of being merely consistent with it, which is what keeps the
      // guarantee true for a future caller that hands over a wider buffer set.
      // The mechanism itself is pinned where it lives, on `runSave` over a
      // four-buffer state (`test_doxbench_save.py`). The canvas Save sends no
      // `only`, so its behaviour is byte-for-byte what it was.
      save: (request) => runSave(
        savePlanState(request),
        { transport: firstEditTransport({ caps, repair: consoleRepair }),
          ...(request && request.only !== undefined
            ? { only: request.only } : {}) }),
      catalog: createDoxBenchCatalogLoader(() => caps?.console_token),
      chatTurn: createDoxBenchTurnSubmitter(() => caps?.console_token),
      // add-doxbench-editing-phase-b task 7.2: the rail's loaded-document
      // selector switches the transcript to that document's thread, and this
      // is where it reads one. A READ seam only — there is no thread write on
      // this bundle, because a thread is written by a turn.
      thread: createDoxBenchThreadLoader(() => caps?.console_token),
      // add-doxbench-distilled-abstract §7: the docs subpane's model-derived
      // abstract. One seam, one route, one call site -- and no second provider
      // path: the route sits behind the SAME three-part verdict the catalog and
      // chat-turn routes do, and the browser holds no credential for either.
      documentAbstract: createDoxBenchAbstractRequester(
        () => caps?.console_token),
    };
    const stagingWorkbench = mountStagingWorkbench(
      document.getElementById("staging-workbench-root"), snapshot,
      { onOpenDoc: (path, doc) =>
          explorer.openDoc(path, doc, workbenchSourceKey),
        caps, active, index, signal,
        // the unstripped probe, read by the workbench's `openDraft` alone
        createCaps: probedCaps,
        // the console-token re-read, forwarded to the two write transports so a
        // page that outlived a serve restart repairs itself instead of
        // discarding what the human typed
        consoleRepair,
        doxbench: doxbenchSeams,
        sourceBase: workbenchSourceBase, edit: workbenchEdit,
        onScopeOpened: routeWorkbenchScope, onSessionRekey: rekeyToSession,
        onSessionEnded: resetEndedSession });
    // The wheel's read-only verbs (documents read · clusters lens/canvas): app.js
    // owns every cross-view jump, so the wheel declares the verb and calls back
    // here. `tabs` is assigned just below; the callbacks only run on a click.
    let tabs = null;
    const nav = {
      // documents -> the read-only source viewer (the explorer overlay's viewer
      // pane, the one place renderViewer is mounted).
      // Wheel staged/change entries pass their owning snapshot item separately
      // from the optional document. That owner is essential in an aggregate:
      // identical paths in two members must never fall through to the active
      // member or the first matching document.
      openDoc: (path, doc, owner) =>
        explorer.openDoc(path, doc, sourceKeyFor(owner || doc)),
      // clusters -> the keyword lens, pre-checked on this cluster's declared
      // topics (lens.js's own preselection entry point; the topics ARE the
      // declared keyword vocabulary the rail is built from).
      openLens: (keywords) => {
        const view = tabs?.goto("view-lens");
        if (view?.focusKeywords) view.focusKeywords(keywords);
      },
      // clusters -> the cluster canvas, pre-selected on this cluster.
      openCanvas: (clusterId) => {
        const view = tabs?.goto("view-canvas");
        if (view?.select) view.select(clusterId);
      },
      // clusters / possibles / staged -> the staging workbench, scoped to the
      // tile the verb was activated from (read-only; closes back to the wheel).
      openWorkbench: (kind, id) => stagingWorkbench.open(kind, id),
      // the lens's drafted staging seed, carried into doxBench as a prefilled
      // CREATE — the governed one, which opens a branch session, so a draft
      // never lands on main
      openDraft: (seed) => stagingWorkbench.openDraft(seed),
      // composed tiles -> the tile's member repository (D10's one verb): store
      // the key at the member's own ref and reload — the ratified selector
      // posture, after which every verb works as on any single-repo view.
      openRepository: (repository) => {
        storeKey({ repository, ref: memberRef(rawSnapshot, repository) });
        render();
      },
    };
    tabs = initTabs(snapshot, {
      explorer, notebook, caps, nav, composed, sourceBase: sourceBaseFor(active),
      // the UNSTRIPPED probe and the serve's own writable repository — read by
      // exactly one affordance (see `createCaps` at the lens's mount)
      probedCaps,
      // DECLARED by the serve, never inferred here: a plane reaching several
      // repositories writes into exactly one, and under a composed view the
      // rendered snapshot's `repository` is the PROJECT id — not a repository
      // at all, and refused by the create route.
      writableRepository: probedCaps?.repository || null,
      // D21 — the repository lens's seams: the whole aggregate to lens over,
      // the current visible set, the write-through, and the drill-in.
      rawSnapshot, visible: view ? view.visible : null,
      // handed to every view that binds outside its own root
      signal,
      onVisible: (repositories) => {
        if (!composed) return;
        storeViewState(rawSnapshot.repository,
          { visible: repositories, mode: view.mode });
      },
      onDrillIn: ({ region, identities }) => {
        if (!identities.length) return;
        storeDrillScope({
          identities,
          label: region.kind === "centre"
            ? "all " + (region.keywords || []).length + " visible repositories"
            : (region.keywords || []).join(" ∧ "),
        });
        render();
      },
    }, signal);
    // The REPOSITORY SELECTOR + the ONE refresh affordance (design D7/D9):
    // switching repositories stores the key and reloads the shell; a successful
    // refresh reloads it too (the data changed, so every view must re-derive); a
    // FAILED refresh reports inline and leaves this view exactly as it is.
    repoSelector = mountRepoSelector(document.getElementById("repopicker"), {
      index, active, snapshot, caps, projects,
      onSelect: (key) => { storeKey(key); render(); },
      onRefreshed: () => render(),
    });
    initAbout(signal);
    // global header search (#13): fan out to the active view's search hook.
    const searchInput = document.getElementById("globalsearch");
    if (searchInput) {
      searchInput.addEventListener("input", () => tabs.search(searchInput.value),
                                   { signal });
    }
    if (status) status.remove();
  } catch (err) {
    if (status) status.textContent = "Could not load the snapshot (" + err.message +
      "). The renderer reads a single generated snapshot; regenerate it and reload.";
  }
}

await main();
