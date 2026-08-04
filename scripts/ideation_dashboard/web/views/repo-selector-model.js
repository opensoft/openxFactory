// Repository-selector VIEW MODEL (openxFactory change add-dashboard-repo-selector,
// tasks 3.2/3.5 and Brett's 2026-07-26 rulings). PURE derivation over the
// snapshot INDEX — no DOM, no fetch, no imports — so it is copied ALONE into a
// node harness (test_repo_selector.py) exactly like model.js/grouping.js.
//
// The index (openxFactory `ideation-dashboard-snapshot-index`) is the ONLY
// roster: the dashboard keeps no second repository list, so adding a repository
// is a project-register edit plus a publication run — no application change and
// no image rebuild (design D9). Entries the index carries but the register does
// not are still offered; they simply render ungrouped, which the snapshot's own
// absent `project` field already expresses.
//
// Three derivations live here:
//   * ROSTER — one option per (repository, ref) entry plus one per declared
//     aggregate, each carrying its availability so an unfetchable entry can say
//     so instead of vanishing (spec: "An indexed snapshot cannot be fetched");
//   * FRESHNESS — the `repo @ ref · short SHA · generated-at` header contract
//     (design D11), plus the stale-fallback notice (D6). A baked entry NEVER
//     renders silently; that silence is the bug this change exists to end;
//   * THE PASSIVE HINT — whether the data source advertises a NEWER snapshot
//     than the one loaded (Brett's 2026-07-26 ruling on open question 2: a
//     passive badge on a background index poll, never an auto-reload).

export const DEFAULT_REF = "main";
// The repository the dev plane opens on when the roster offers a choice and the
// viewer has not made one — today's single-repository behaviour, preserved.
export const PREFERRED_REPOSITORY = "openxFactory";
export const KIND_REPOSITORY = "repository";
export const KIND_AGGREGATE = "aggregate";

export function normalizeRef(ref) {
  const text = ref == null ? "" : String(ref).trim();
  return text || DEFAULT_REF;
}

// The wire/DOM form of a key — `repository@ref`, matching the server's key_id.
export function keyId(repository, ref) {
  return String(repository) + "@" + normalizeRef(ref);
}

export function parseKeyId(text) {
  const raw = text == null ? "" : String(text);
  const at = raw.lastIndexOf("@");
  if (at <= 0) return null;
  return { repository: raw.slice(0, at), ref: normalizeRef(raw.slice(at + 1)) };
}

export function sameKey(a, b) {
  if (!a || !b) return false;
  return String(a.repository) === String(b.repository)
    && normalizeRef(a.ref) === normalizeRef(b.ref);
}

// ---- request safety: what may address a request ----
//
// The snapshot INDEX arrives over the network and the viewer's stored preference
// arrives from sessionStorage, so both are THIRD-PARTY DATA — and two of their
// values (repository, ref) address the shell's one state fetch. Neither may be
// allowed to steer that request (Sonar jssecurity:S8476, CWE-20), so a key earns
// its way into a URL twice over:
//
//   * MEMBERSHIP — it must be a pair the loaded index actually advertises
//     (`resolveStoredKey` for the stored preference, `resolveActive` for
//     everything else). A repository that has left the roster stops being
//     requested, which is also the plain bug: a stale stored key kept fetching a
//     snapshot the index no longer offers;
//   * SHAPE — both segments must survive this ALLOW-LIST, which returns a string
//     rebuilt from KEY_SEGMENT_CHARS itself rather than a slice of the input, so
//     not one character of an index- or storage-supplied value reaches a request
//     URL. `..` is refused outright: no repository name and no git ref contains
//     it, and it is the one sequence that would mean something to a path-shaped
//     route.
//
// A BRANCH-SESSION ref (`draft/<topic>`, `cluster/<id>`) is a first-class citizen
// of this same path and introduces no second one (add-workbench-branch-sessions
// FR-014, G11): the serving index advertises the live session as an ordinary
// (repository, ref) row, so a session key earns a URL by the same membership +
// shape test, and a session that has ENDED stops being requested exactly as a
// repository that has left the roster does. Note what that rests on: `/` is in
// KEY_SEGMENT_CHARS because a git ref legitimately contains one. Removing it would
// silently make every session key unrequestable while leaving `main` working.
const KEY_SEGMENT_CHARS =
  "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-/";
const KEY_SEGMENT_TABLE = new Map([...KEY_SEGMENT_CHARS].map((c) => [c, c]));
export const KEY_SEGMENT_MAX = 200;

export function safeKeySegment(value) {
  const raw = value == null ? "" : String(value);
  if (!raw || raw.length > KEY_SEGMENT_MAX || raw.includes("..")) return null;
  let safe = "";
  for (const ch of raw) {
    const allowed = KEY_SEGMENT_TABLE.get(ch);
    if (allowed === undefined) return null;   // one stray character rejects the pair
    safe += allowed;                          // from the table, never from `raw`
  }
  return safe;
}

// The request-safe form of a key — `{ repository, ref }` rebuilt through the
// allow-list — or null when either segment cannot survive it.
export function safeKey(key) {
  if (!key) return null;
  const repository = safeKeySegment(key.repository);
  const ref = safeKeySegment(normalizeRef(key.ref));
  if (!repository || !ref) return null;
  return { repository, ref };
}

// ---- roster ----

function entryOption(entry) {
  const key = { repository: String(entry.repository), ref: normalizeRef(entry.ref) };
  const available = entry.available !== false;
  return {
    kind: KIND_REPOSITORY,
    id: keyId(key.repository, key.ref),
    repository: key.repository,
    ref: key.ref,
    label: entry.display_name || key.repository,
    available,
    unavailableReason: available ? null : (entry.unavailable_reason || "snapshot unavailable"),
    origin: entry.origin || null,
    stale: entry.stale === true,
    staleReason: entry.stale_reason || null,
    sourceRevision: entry.source_revision || null,
    generatedAt: entry.generated_at || null,
    latestSourceRevision: entry.latest_source_revision || null,
    latestGeneratedAt: entry.latest_generated_at || null,
    newerAvailable: entry.newer_available === true,
  };
}

function aggregateOption(aggregate) {
  const members = (aggregate.members || [])
    .filter((m) => m && m.repository)
    .map((m) => ({ repository: String(m.repository), ref: normalizeRef(m.ref) }));
  return {
    kind: KIND_AGGREGATE,
    id: keyId(aggregate.id, DEFAULT_REF),
    repository: String(aggregate.id),
    ref: DEFAULT_REF,
    label: aggregate.display_name || String(aggregate.id),
    available: members.length > 0,
    unavailableReason: members.length ? null : "no members declared",
    members,
    origin: "composed",
    stale: false,
    staleReason: null,
    sourceRevision: null,
    generatedAt: null,
    newerAvailable: false,
  };
}

// The selector's options, in index order for entries and declared order for
// aggregates (composed views sort last — they are a roll-up OF the repositories
// above them). Returns [] for a missing/empty index, which is what makes the
// no-index plane degrade to today's single-snapshot dashboard.
export function buildRoster(index) {
  if (!index || typeof index !== "object") return [];
  const entries = Array.isArray(index.entries) ? index.entries : [];
  const aggregates = Array.isArray(index.aggregates) ? index.aggregates : [];
  const options = entries
    .filter((e) => e && e.repository)
    .map(entryOption);
  const composed = aggregates
    .filter((a) => a && a.id)
    .map(aggregateOption);
  return options.concat(composed);
}

export function findOption(roster, key) {
  if (!key) return null;
  return roster.find((o) => sameKey(o, key)) || null;
}

// Does the loaded index actually advertise this (repository, ref) pair? The one
// membership question the shell asks before a stored value is allowed to matter.
export function hasKey(index, key) {
  const wanted = typeof key === "string" ? parseKeyId(key) : key;
  if (!wanted) return false;
  return findOption(buildRoster(index), wanted) !== null;
}

// The viewer's STORED key, validated against the roster: null when this index no
// longer advertises the pair (or when the stored text is not request-safe), and
// `resolveActive(index, null)` then picks the default exactly as if nothing had
// been stored. The value handed back is the ROSTER'S own pair rebuilt through the
// allow-list — deliberately not the storage's string — so what travels on to a
// request URL is an index-advertised, character-checked pair and nothing else.
export function resolveStoredKey(index, stored) {
  const wanted = typeof stored === "string" ? parseKeyId(stored) : stored;
  const safe = safeKey(wanted);
  if (!safe) return null;
  const option = findOption(buildRoster(index), safe);
  return option ? safeKey({ repository: option.repository, ref: option.ref }) : null;
}

// Which option is ACTIVE: an explicit request (a viewer's stored choice) wins
// when the roster still offers it; then whatever the server marked active; then
// the preferred repository at the default ref; then the first available option.
// A roster with nothing available still returns its first option rather than
// null — a selector that offers an unavailable repository and SAYS it is
// unavailable is more honest than an empty one.
export function resolveActive(index, requested) {
  const roster = buildRoster(index);
  if (!roster.length) return null;
  const wanted = typeof requested === "string" ? parseKeyId(requested) : requested;
  const explicit = findOption(roster, wanted);
  if (explicit) return explicit;
  const served = index && index.active ? findOption(roster, index.active) : null;
  if (served) return served;
  const preferred = findOption(roster, { repository: PREFERRED_REPOSITORY, ref: DEFAULT_REF });
  if (preferred) return preferred;
  return roster.find((o) => o.available) || roster[0];
}

// ---- freshness (design D11) ----

export function shortRevision(revision) {
  const text = revision == null ? "" : String(revision);
  return text ? text.slice(0, 12) : "unknown";
}

function stampDay(stamp) {
  const text = stamp == null ? "" : String(stamp);
  return text ? text.slice(0, 10) : "unknown";
}

// `repo @ ref · <short sha> · generated <date>` — the question behind the whole
// refresh ask ("did my doc make it in?") answered at a glance, against a stated
// revision rather than a deployment time.
export function freshnessLabel(option, snapshot) {
  const gen = (snapshot && snapshot.generation) || {};
  const repository = (option && option.repository) || snapshot?.repository || "unknown";
  const ref = normalizeRef(option && option.ref);
  const revision = (option && option.sourceRevision) || gen.source_revision;
  const stamp = (option && option.generatedAt) || gen.generated_at;
  return repository + " @ " + ref + " · " + shortRevision(revision)
    + " · generated " + stampDay(stamp);
}

// The stale-fallback notice (D6). Non-null ONLY when the rendered snapshot is
// the baked fallback: it names the fallback's generated-at, because the failure
// mode this change exists to end is not old data — it is old data that looked
// current.
export function staleNotice(option) {
  if (!option || option.stale !== true) return null;
  const detail = option.staleReason
    || "the declared data source is unreachable — showing the snapshot baked into this image";
  return "stale snapshot: " + detail + " (generated " + stampDay(option.generatedAt) + ")";
}

// ---- the passive newer-data hint (Brett 2026-07-26, open question 2) ----

// True when the index advertises a snapshot NEWER than the one loaded for this
// option. Revision inequality is the signal (the index restates the snapshot's
// own `source_revision`, so a difference means the source moved); a newer
// generated-at is accepted as a signal too. NEVER triggers a reload on its own —
// the viewer clicks refresh.
export function newerAvailable(option, snapshot) {
  if (!option) return false;
  const loadedRevision = (snapshot && snapshot.generation && snapshot.generation.source_revision)
    || option.sourceRevision || null;
  const latest = option.latestSourceRevision;
  if (latest && loadedRevision && String(latest) !== String(loadedRevision)) return true;
  if (option.newerAvailable === true && latest && !loadedRevision) return true;
  const loadedStamp = (snapshot && snapshot.generation && snapshot.generation.generated_at)
    || option.generatedAt || null;
  if (option.latestGeneratedAt && loadedStamp
      && String(option.latestGeneratedAt) > String(loadedStamp)) return true;
  return false;
}

export function hintLabel(option) {
  const stamp = option && option.latestGeneratedAt ? stampDay(option.latestGeneratedAt) : null;
  return "newer data available" + (stamp ? " (" + stamp + ")" : "") + " — click refresh";
}

// ---- sparse stations (design D10) ----

// Which funnel stations this snapshot has NO data for. Sparse is rendered, never
// refused: an install repository carrying only OpenSpec changes shows active and
// archived and says, explicitly, that the middle is empty in THIS repository.
export const STATIONS = [
  ["documents", "ideation documents"],
  ["clusters", "topic clusters"],
  ["possibles", "possibles"],
  ["staged_topics", "staged topics"],
  ["changes", "OpenSpec changes"],
];

export function emptyStations(snapshot) {
  const snap = snapshot || {};
  return STATIONS.filter(([key]) => !(Array.isArray(snap[key]) && snap[key].length))
    .map(([key, label]) => ({ key, label }));
}

export function sparseNotice(option, snapshot) {
  const empty = emptyStations(snapshot);
  if (!empty.length) return null;
  const repository = (option && option.repository) || snapshot?.repository || "this repository";
  return "no " + empty.map((s) => s.label).join(", no ") + " in " + repository
    + " — a sparse funnel is an honest funnel, not a broken one";
}
