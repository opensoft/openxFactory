// Keyword-lens view-model + bullseye geometry (D13, T023/T024). PURE: no DOM,
// no I/O, no external imports — imported by lens.js in the browser AND unit-
// tested from Python via node (tests/ideation-dashboard/test_lens.py), exactly
// like model.js / canvas-model.js. Every value is derived from the snapshot's
// `keyword_index` + `documents[].topics` (DECLARED vocabulary only); where the
// hand-drawn sketch placed dots by hand, this module computes them.
//
// SEMANTICS (locked to lens.py — the Python half owns persistence/re-run):
//   check = stratify   a checked keyword adds to a doc's MATCH COUNT; the
//                      bullseye shows docs matching >= 1 checked keyword,
//                      stratified into rings by match count (innermost = ALL).
//   pin = require      a pinned keyword HARD-FILTERS: a doc lacking it is off
//                      the bullseye entirely. W1: pinned MUST be a subset of
//                      checked (the UI prevents it upstream; the engine on save).
//   matched            docs matching ALL checked keywords (innermost ring) —
//                      the recipe's intensional definition, auto-included.
//   overrides          manual + on an OUTER-ring/off-bullseye doc; manual − on a
//                      CENTER doc. Each REQUIRES a reason (collected by lens.js;
//                      the engine refuses without) — evidence, never a silent edit.
//
// declared (solid) vs inferred (hollow): v1 is DECLARED-ONLY — every dot is a
// solid declared dot. Inferred tags (hollow dots, radial strength) arrive with
// document-cataloging; the dot carries `declared: true` so the renderer's
// distinction is already wired for that follow-on.

// Shared HTML-escape (funnel.js / canvas-model.js discipline). Exported and
// node-tested; lens.js also binds every dynamic value via textContent.
export function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"]/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

// Bullseye SVG frame — the sketch's idiom (520×520, centred, outermost r=210).
export const GEOM = { size: 520, cx: 260, cy: 260, rMax: 210 };

// ---- label legibility at CORPUS scale (T092 acceptance sweep, defect 9) ------
//
// The bullseye's geometry is fine; its LABELS are not, and all three failures
// are the same mistake — text drawn at a computed point with no regard for the
// box the text occupies. On the real 151-keyword corpus, measured twice in
// independent driver runs with identical numbers:
//
//   ring labels    radii are rMax/n, so the stride is 210/n px against a
//                  12.52px label. At 12 checked keywords 0 pairs overlap; at 18
//                  the stride is 11.67px and ALL 17 adjacent pairs do, stacking
//                  "MATCHES 1" … "ALL 18 ✓" into one illegible column over the
//                  dots. The threshold is exact.
//   sector labels  the FULL conjunction ("doc-management ∧ doc-workflow ∧
//                  ideation-dashboard ∧ doc-health ∧ ideation-cross-reference"),
//                  middle-anchored at rMax+8, unwrapped and untruncated: up to
//                  464px wide in a 520px viewBox, so 1 is clipped at 4 keywords,
//                  4 at 8 and 10 of 20 at 18 — the reader sees "keyw", "ideat".
//   document dots  a ring holds every document with the same match count, so
//                  labels collide from the FIRST TWO keywords: 66 overlapping
//                  pairs at 2 checked. On a two-document fixture this is
//                  invisible; with 12 documents on one ring it is the normal
//                  case, which is precisely why the smoke never saw it.
//
// These helpers are PURE and live here beside the geometry they answer to, so
// the node harness can measure them at 151-keyword scale without a browser and
// the SHARED widget (bullseye.js) has exactly one definition to draw from.

// One glyph's advance in the SVG's monospace face, as a fraction of font-size.
// A conservative 0.62 (measured 0.6 for the stack in use) so a bound derived
// here is never narrower than what the browser paints.
export const CHAR_ADVANCE = 0.62;

// ...and one line of text occupies MORE vertical space than its font-size: the
// sweep measured the 10px `.ringlab` box at 12.52px, which is precisely why the
// 210/n ring stride collides at 18 checked keywords and not at 12. Modelling
// the box as the font-size would under-report every collision by a fifth.
export const LABEL_BOX_HEIGHT = 1.252;

// Ring labels are 10px uppercase with 0.06em tracking; the browser measured the
// box at 12.52px tall. The minimum stride is that box plus a hair.
export const RING_LABEL_MIN_GAP = 14;

// Which ring labels to draw, innermost first, so no two are closer than
// `minGap`. The matches-ALL centre and the outermost "matches 1" ring always
// read — they are the two the human orients by — and an intermediate label is
// dropped rather than allowed to collide with the outermost one.
export function ringLabelIndices(radii, minGap = RING_LABEL_MIN_GAP) {
  const n = radii.length;
  if (n <= 1) return n ? [0] : [];
  const keep = [0];
  for (let i = 1; i < n - 1; i++) {
    if (Math.abs(radii[i] - radii[keep[keep.length - 1]]) >= minGap) keep.push(i);
  }
  while (keep.length > 1
    && Math.abs(radii[n - 1] - radii[keep[keep.length - 1]]) < minGap) keep.pop();
  keep.push(n - 1);
  return keep;
}

// A sector label's DISPLAYED text. The full combination already lives in the
// region's <title>/aria-label (and now in the label's own <title>), so the drawn
// string is bounded: a long conjunction collapses to its first keyword plus a
// "+N" count rather than being clipped mid-word into a different keyword's name.
export const SECTOR_LABEL_MAX = 20;

export function sectorLabelText(subsetKey, keywords = [], max = SECTOR_LABEL_MAX) {
  const full = String(subsetKey || "");
  if (full.length <= max) return full;
  if (keywords.length > 1) {
    const more = " +" + (keywords.length - 1);
    const room = max - more.length;
    const head = keywords[0].length <= room
      ? keywords[0] : keywords[0].slice(0, Math.max(1, room - 1)) + "…";
    return head + more;
  }
  return full.slice(0, Math.max(1, max - 1)) + "…";
}

// Can a middle-anchored label of this length fit the drawing area at all? A
// document whose basename is longer than the canvas is wide cannot be labelled
// legibly at any anchor, so the caller drops the label rather than centring an
// overflow (the dot's <title> still carries the name).
export function labelFits(textLen, fontSize, size = GEOM.size) {
  return textLen * fontSize * CHAR_ADVANCE + 4 <= size;
}

// Keep a middle-anchored label inside the drawing area. A label whose box leaves
// the viewBox is not merely unreadable — it mislabels the sector next to it.
// Callers guard with `labelFits` first; a label that cannot fit is clamped to
// the centre here only so the return type stays total.
export function clampLabel(x, y, textLen, fontSize, size = GEOM.size) {
  const halfW = (textLen * fontSize * CHAR_ADVANCE) / 2;
  const pad = 2;
  return {
    x: labelFits(textLen, fontSize, size)
      ? Math.min(size - halfW - pad, Math.max(halfW + pad, x))
      : size / 2,
    y: Math.min(size - pad, Math.max(fontSize * LABEL_BOX_HEIGHT + pad, y)),
  };
}

// The label box a middle-anchored, baseline-positioned string occupies.
export function labelBox(x, y, textLen, fontSize) {
  const halfW = (textLen * fontSize * CHAR_ADVANCE) / 2;
  return { left: x - halfW, right: x + halfW,
           top: y - fontSize * LABEL_BOX_HEIGHT, bottom: y };
}

// Greedy non-overlap: keep a label only when its box clears every label already
// kept. Deterministic (the caller's order is the snapshot's), and it makes
// "zero overlapping pairs" true BY CONSTRUCTION at any density rather than by a
// threshold somebody has to re-tune when the corpus grows. The dropped dot keeps
// its <title>, which is where the name was always authoritative.
export function nonOverlappingIndices(boxes) {
  const kept = [];
  const taken = [];
  boxes.forEach((box, i) => {
    if (taken.some((b) => b.right > box.left && b.left < box.right
      && b.bottom > box.top && b.top < box.bottom)) return;
    taken.push(box);
    kept.push(i);
  });
  return kept;
}

// Deterministic string comparator — used where the default Array.sort() lexical
// coercion is a smell (S2871) and where a nested-ternary inline comparator would
// be (S3358). Matches the UTF-16 code-unit order the default sort applies.
function cmpStr(a, b) {
  if (a < b) return -1;
  return a > b ? 1 : 0;
}

// ---- snapshot readers (declared topics only) ----

function docTopics(snapshot) {
  // [id, Set(topics)] in snapshot document order (generator sorts by path).
  const out = [];
  for (const d of snapshot?.documents || []) {
    if (d?.id) out.push([d.id, new Set(d.topics || [])]);
  }
  return out;
}

// The keyword rail seed: `keyword_index` verbatim (declared counts), else
// derived from documents when the index is absent (degrade, never throw).
function keywordCounts(snapshot) {
  const s = snapshot || {};
  if ((s.keyword_index || []).length) {
    return (s.keyword_index || []).map((k) => ({
      keyword: k.keyword,
      declaredCount: k.declared_doc_count || 0,
    }));
  }
  const counts = new Map();
  for (const [, topics] of docTopics(s)) for (const t of topics) counts.set(t, (counts.get(t) || 0) + 1);
  return [...counts.keys()].sort(cmpStr).map((k) => ({ keyword: k, declaredCount: counts.get(k) }));
}

// ---- pure recipe evaluation (mirror of lens.evaluate_recipe) ----

// A document passes the pin filter (`pin = require`) when it carries EVERY
// pinned keyword. Shared by evaluateRecipe and coOccurrenceCounts.
function pinsSatisfied(topics, pinSet) {
  for (const p of pinSet) if (!topics.has(p)) return false;
  return true;
}

export function evaluateRecipe(snapshot, checked, pinned) {
  const chk = (checked || []).slice();
  const pin = (pinned || []).slice();
  const chkSet = new Set(chk);
  const stray = pin.filter((k) => !chkSet.has(k));
  if (stray.length) {
    throw new Error("recipe pinned keyword(s) [" + stray.sort().join(", ") +
      "] are not in checked (W1: pinned MUST be a subset of checked)");
  }
  const pinSet = new Set(pin);
  const nChecked = chk.length;
  const matched = [];
  const universe = [];
  const rows = [];
  for (const [docId, topics] of docTopics(snapshot)) {
    if (!pinsSatisfied(topics, pinSet)) continue; // pin = require: hard filter
    const subset = chk.filter((k) => topics.has(k)); // preserve checked order
    if (subset.length === 0) continue;           // off the bullseye
    universe.push(docId);
    rows.push({ document: docId, matchedSubset: subset, matchCount: subset.length });
    if (nChecked && subset.length === nChecked) matched.push(docId); // innermost = membership
  }
  return { checked: chk, pinned: pin, matched, universe, rows };
}

// ---- co-occurrence hints ("adding K pulls N docs inward / brings M new") ----
//
// For each UNCHECKED keyword K, deterministic counts describing what checking it
// would do: `pulledInward` current-universe docs also carry K (gain a match →
// move one ring in); `newDocs` docs off the bullseye (pass the pin filter, match
// no current checked kw) that carry K would ENTER at ring 1. Pure, snapshot-only.

// Counts for a single candidate keyword K: current-universe docs that also carry
// K (pulled inward) and off-bullseye-but-pin-passing docs that carry K (brought
// new). Extracted from coOccurrenceHints to keep it under the cognitive-
// complexity budget (S3776).
function coOccurrenceCounts(snapshot, keyword, pinSet, inUniverse) {
  let pulledInward = 0;
  let newDocs = 0;
  for (const [docId, topics] of docTopics(snapshot)) {
    if (!topics.has(keyword)) continue;
    if (!pinsSatisfied(topics, pinSet)) continue;
    if (inUniverse.has(docId)) pulledInward += 1;
    else newDocs += 1;
  }
  return { pulledInward, newDocs };
}

function coOccurrenceHintText(keyword, pulledInward, newDocs) {
  let hint = "+" + keyword + " → pulls " + pulledInward + " inward";
  if (newDocs) hint += ", brings " + newDocs + " new";
  return hint;
}

export function coOccurrenceHints(snapshot, checked, pinned) {
  const ev = evaluateRecipe(snapshot, checked, pinned);
  const inUniverse = new Set(ev.universe);
  const chkSet = new Set(ev.checked);
  const pinSet = new Set(ev.pinned);
  const hints = [];
  for (const { keyword, declaredCount } of keywordCounts(snapshot)) {
    if (chkSet.has(keyword)) continue;
    const { pulledInward, newDocs } = coOccurrenceCounts(snapshot, keyword, pinSet, inUniverse);
    const hint = coOccurrenceHintText(keyword, pulledInward, newDocs);
    hints.push({ keyword, declaredCount, pulledInward, newDocs, hint });
  }
  return hints;
}

// ---- bullseye geometry (rings / sectors / dot placements) ----

function toRad(deg) { return (deg * Math.PI) / 180; }

// Outer radius of the band for `matchCount` of `nChecked` checked keywords:
// match-all is the smallest (innermost), match-1 the largest (rMax).
function ringOuterRadius(matchCount, nChecked, rMax) {
  return (rMax * (nChecked - matchCount + 1)) / nChecked;
}

// Dot placement radius: the midpoint of the band [inner, outer] for its ring.
function dotRadius(matchCount, nChecked, rMax) {
  const outer = ringOuterRadius(matchCount, nChecked, rMax);
  const inner = matchCount >= nChecked ? 0 : ringOuterRadius(matchCount + 1, nChecked, rMax);
  return (outer + inner) / 2;
}

// Stable ordering of the distinct matched subsets present: larger subsets first
// (nearer the centre), then lexicographically — so a subset's sector angle is
// deterministic across renders and the JS/Python cross-check can assert it.
function subsetKey(subset) { return subset.join(" ∧ "); }

// ---- dot packing (Brett's 2026-08-07 ruling: dots must not touch) ---------

//: The drawn dot's radius at full size, and the floor below which a dot stops
//: reading as a dot. `DOT_GAP` is the clear space between two dots' EDGES —
//: what "not directly touching" means, measured.
export const DOT_R = 6;
export const DOT_MIN_R = 2.5;
export const DOT_GAP = 2.5;
//: A cell keeps a hair of its own span free at each end so two neighbouring
//: sectors' outermost dots do not read as one run.
const SPAN_MARGIN = 0.9;

//: Candidate sizes, largest first — a short deterministic ladder rather than a
//: solve, so the chosen size is reproducible and easy to reason about.
function sizeLadder() {
  const sizes = [];
  for (let s = DOT_R; s >= DOT_MIN_R; s -= 0.5) sizes.push(s);
  return sizes;
}

//: How many dots of pitch `pitch` fit on the arc this row spans.
function rowCapacity(radius, spanDeg, pitch) {
  const arc = Math.abs(radius) * ((spanDeg * SPAN_MARGIN * Math.PI) / 180);
  return Math.max(1, Math.floor(arc / pitch) + 1);
}

//: The row radii available in a band at a given pitch, outermost first. A dot
//: sits a half-pitch inside the band edge so it never straddles a ring line.
function rowRadii(inner, outer, pitch) {
  const radii = [];
  for (let r = outer - pitch / 2; r >= inner + pitch / 2 - 0.001; r -= pitch) {
    radii.push(r);
  }
  if (!radii.length) radii.push((inner + outer) / 2);   // band thinner than one dot
  return radii;
}

// Place `n` documents inside one cell — the band [inner, outer] × the
// `spanDeg` slice centred on `baseDeg` — as `{radius, angleDeg, size}`.
// Rows fill outermost-first and each row is centred on the sector's angle, so
// a cell reads as a compact block on its own ring rather than a smear.
export function packCell(n, inner, outer, spanDeg, baseDeg) {
  const count = Math.max(0, n | 0);
  if (!count) return [];
  let chosen = { size: DOT_MIN_R, radii: [], pitch: 2 * DOT_MIN_R + DOT_GAP };
  for (const size of sizeLadder()) {
    const pitch = 2 * size + DOT_GAP;
    const radii = rowRadii(inner, outer, pitch);
    const capacity = radii.reduce(
      (sum, r) => sum + rowCapacity(r, spanDeg, pitch), 0);
    chosen = { size, radii, pitch };
    if (capacity >= count) break;      // largest size that holds the cell
  }
  const { size, radii, pitch } = chosen;
  // distribute across the rows we have, filling each to its own capacity
  const perRow = [];
  let left = count;
  for (const radius of radii) {
    if (left <= 0) break;
    const take = Math.min(left, rowCapacity(radius, spanDeg, pitch));
    perRow.push({ radius, take });
    left -= take;
  }
  // A cell too crowded for its own area even at the minimum size cannot be
  // drawn without SOMETHING giving. Separation is the property Brett asked
  // for, so the overflow spreads evenly across every row — each row's dots
  // stay `pitch` apart and the cell reaches a little past its span — rather
  // than piling into one row or collapsing back into a touching bar.
  for (let i = 0; left > 0 && perRow.length; i = (i + 1) % perRow.length) {
    perRow[i].take += 1;
    left -= 1;
  }
  const out = [];
  for (const { radius, take } of perRow) {
    // the angular step that puts `pitch` between two dot CENTRES at this
    // radius — the geometric definition of "not touching", not a constant
    const step = radius > 0 ? (pitch / radius) * (180 / Math.PI) : 0;
    const start = baseDeg - (step * (take - 1)) / 2;
    for (let i = 0; i < take; i += 1) {
      // `slot` lets the renderer STAGGER labels along a row: consecutive dots
      // alternate their label above and below the arc, which doubles the
      // label room without moving a single dot (packing tightly to keep dots
      // apart otherwise costs exactly the space the numbers need).
      out.push({ radius, angleDeg: start + i * step, size, slot: i % 2 });
    }
  }
  return out;
}



function bullseyeLayout(rows, nChecked, geom) {
  const g = geom || GEOM;
  const rings = [];                    // one per match count present, innermost first
  const byCount = new Map();
  const subsetKeys = new Set();
  // key -> the matched keyword ARRAY behind it. The joined `subsetKey` is a
  // label; the array is what a caller acting on a sector needs (the create
  // gesture seeds `Topics:` from it — add-workbench-bullseye-and-create open
  // question 2's ruling), and splitting the label back apart would be a second,
  // fragile definition of the same list.
  const subsetOf = new Map();
  for (const r of rows) {
    const key = subsetKey(r.matchedSubset);
    subsetKeys.add(key);
    if (!subsetOf.has(key)) subsetOf.set(key, [...r.matchedSubset]);
    if (!byCount.has(r.matchCount)) byCount.set(r.matchCount, []);
    byCount.get(r.matchCount).push(r);
  }
  // sector angle per distinct subset (top-start, clockwise), deterministic order
  const orderedSubsets = [...subsetKeys].sort((a, b) => {
    const sa = a.split(" ∧ ").length, sb = b.split(" ∧ ").length;
    return sb - sa || cmpStr(a, b);
  });
  const sectorAngle = new Map();
  const total = orderedSubsets.length || 1;
  orderedSubsets.forEach((k, i) => sectorAngle.set(k, -90 + ((i + 0.5) * 360) / total));
  // one sector's angular slice — the bound a cell's dots must stay inside
  const span = 360 / total;

  // dots: ring radius by match count; sector angle by subset. Within a CELL
  // (one ring band × one sector) the documents are PACKED so no two dots
  // touch (Brett's 2026-08-07 ruling: "spread out the dots so they are not
  // directly touching each other — this should fix the numbers crowding too").
  //
  // The old rule fanned every dot along ONE arc at the band's midpoint with a
  // `min(18, 40/n)` step, which has two failures: the step collapses as n
  // grows (20 documents at ~6px apart is a solid bar of overlapping circles,
  // and their labels then lose the collision pass), while the band's RADIAL
  // depth — the whole area between this ring and the next — goes unused. And
  // for small n the fan could exceed the sector's own span and spill into a
  // neighbour it does not belong to.
  //
  // `packCell` uses the cell's real area instead: as many radial rows as the
  // band admits, each row holding as many dots as its own arc length admits,
  // bounded by the sector span, at the largest dot size that still leaves
  // `DOT_GAP` between edges. A cell too crowded even at the minimum size
  // degrades to that minimum rather than pretending to fit.
  const dots = [];
  const cellRows = new Map();
  for (const r of rows) {
    const key = r.matchCount + "|" + subsetKey(r.matchedSubset);
    if (!cellRows.has(key)) cellRows.set(key, []);
    cellRows.get(key).push(r);
  }
  for (const [cell, members] of cellRows) {
    const matchCount = members[0].matchCount;
    const key = subsetKey(members[0].matchedSubset);
    const base = sectorAngle.get(key);
    const outer = ringOuterRadius(matchCount, nChecked, g.rMax);
    const inner = matchCount >= nChecked
      ? 0 : ringOuterRadius(matchCount + 1, nChecked, g.rMax);
    const placed = packCell(members.length, inner, outer, span, base);
    members.forEach((r, i) => {
      const at = placed[i];
      dots.push({
        document: r.document,
        matchCount: r.matchCount,
        matchedSubset: r.matchedSubset,
        subsetKey: key,
        declared: true,                  // v1: declared-only, solid dots
        ringRadius: outer,
        radius: at.radius,
        size: at.size,
        slot: at.slot,
        angleBase: base,
        angleDeg: at.angleDeg,
        x: g.cx + at.radius * Math.cos(toRad(at.angleDeg)),
        y: g.cy + at.radius * Math.sin(toRad(at.angleDeg)),
      });
    });
    void cell;
  }
  // ring metadata (outer radius + label), innermost (match-all) first
  for (let mc = nChecked; mc >= 1; mc--) {
    rings.push({
      matchCount: mc,
      outerRadius: ringOuterRadius(mc, nChecked, g.rMax),
      isCenter: mc === nChecked,
      label: mc === nChecked ? "all " + nChecked + " ✓" : "matches " + mc,
      docCount: (byCount.get(mc) || []).length,
    });
  }
  // Sectors. Each is ONE distinct matched subset, so it lives on exactly one
  // ring — the ring for its own size — and occupies a `spanDeg`-wide slice
  // centred on `angleDeg`. `keywords`, `matchCount`, `spanDeg`, `outerRadius`,
  // and `innerRadius` are ADDITIVE fields the create gesture needs to make a
  // sector an activatable region (add-workbench-bullseye-and-create open
  // question 2's ruling); nothing existing reads them, and the two pre-existing
  // fields are unchanged. `isCenter` marks the matches-ALL subset, which the
  // widget already covers with the centre region rather than a wedge.
  const sectors = orderedSubsets.map((k) => {
    const keywords = subsetOf.get(k) || [];
    const mc = keywords.length;
    return {
      subsetKey: k,
      angleDeg: sectorAngle.get(k),
      keywords,
      matchCount: mc,
      spanDeg: span,
      isCenter: mc === nChecked,
      outerRadius: ringOuterRadius(mc, nChecked, g.rMax),
      innerRadius: mc >= nChecked ? 0 : ringOuterRadius(mc + 1, nChecked, g.rMax),
    };
  });
  return { rings, sectors, dots };
}

// ---- matrix rows (flat view of the SAME membership as the bullseye) ----

function matrixRows(rows, checked, docNumber) {
  return rows.map((r, i) => {
    const present = new Set(r.matchedSubset);
    return {
      document: r.document,
      // the radar's legend key for this row (see buildLensModel's NUMBERING)
      number: docNumber ? (docNumber.get(r.document) || i + 1) : i + 1,
      cells: checked.map((k) => ({ keyword: k, present: present.has(k) })),
      matchCount: r.matchCount,
      ring: r.matchCount === checked.length ? "all " + checked.length : String(r.matchCount),
    };
  });
}

// ---- forming set (default membership + override preview) ----

function formingSet(ev, includes, excludes) {
  const inc = includes || {};
  const exc = excludes || {};
  const excSet = new Set(Object.keys(exc));
  const matchedSet = new Set(ev.matched);
  const members = [];
  for (const doc of ev.matched) {
    if (excSet.has(doc)) continue;              // a center doc the human removed
    members.push({ document: doc, via: "recipe-match", matchCount: ev.checked.length });
  }
  for (const doc of Object.keys(inc)) {
    members.push({ document: doc, via: "manual-include", reason: inc[doc] });
  }
  const memberSet = new Set(members.map((m) => m.document));
  // near-miss candidates: on the bullseye, not matching ALL, not already a
  // member and not excluded — the outer-ring dots a `+` (with reason) pulls in.
  const candidates = [];
  for (const r of ev.rows) {
    if (matchedSet.has(r.document)) continue;
    if (memberSet.has(r.document) || excSet.has(r.document)) continue;
    candidates.push({ document: r.document, matchCount: r.matchCount, ring: r.matchCount });
  }
  const excluded = Object.keys(exc).map((doc) => ({ document: doc, reason: exc[doc] }));
  return { members, candidates, excluded };
}

// ---- recipe line (deterministic, mirrors the sketch's `recipe · …`) ----

export function recipeLine(checked, pinned, includes, excludes) {
  const chk = checked || [];
  const pin = new Set(pinned || []);
  const req = chk.filter((k) => pin.has(k));
  const strat = chk.filter((k) => !pin.has(k));
  let kw = "";
  if (req.length) kw += req.join(" ∧ ");
  if (strat.length) kw += (req.length ? " ∧ " : "") + "{" + strat.join(", ") + "}";
  if (!kw) kw = "(no keywords checked)";
  const nInc = Object.keys(includes || {}).length;
  const nExc = Object.keys(excludes || {}).length;
  const ov = (nInc || nExc)
    ? " · overrides: +" + nInc + " −" + nExc + " (reasons recorded)"
    : " · no overrides";
  return "recipe · kw: " + kw + ov + " · re-runs as the corpus grows";
}

// ---- the full lens model ----

export function buildLensModel(snapshot, query, geom) {
  const q = query || {};
  const checked = q.checked || [];
  const pinned = q.pinned || [];
  const includes = q.includes || {};
  const excludes = q.excludes || {};

  const counts = keywordCounts(snapshot);
  const chkSet = new Set(checked);
  const pinSet = new Set(pinned);
  // NUMBERING (Brett's 2026-08-07 ruling: "the keywords and doc names are too
  // large to be putting on the radar screen — number the keywords and docs,
  // then just put the number on the radar"). Two independent series, each
  // numbered over the list that ALSO acts as its legend:
  //   * keywords by RAIL position — the whole declared vocabulary, so a
  //     number does not move when the human ticks something;
  //   * documents by UNIVERSE position — exactly the rows the matrix lists
  //     beside the bullseye, so #7 on the radar is row 7 in the table.
  // Names never leave the widget: every dot and sector keeps its full name in
  // the SVG <title>, and the rail and matrix print number AND name.
  const rail = counts.map((c, i) => ({
    keyword: c.keyword,
    number: i + 1,
    declaredCount: c.declaredCount,
    checked: chkSet.has(c.keyword),
    pinned: pinSet.has(c.keyword),
  }));
  const keywordNumber = new Map(rail.map((k) => [k.keyword, k.number]));

  const ev = evaluateRecipe(snapshot, checked, pinned);
  const docNumber = new Map(ev.rows.map((r, i) => [r.document, i + 1]));
  const layout = bullseyeLayout(ev.rows, checked.length, geom);
  for (const dot of layout.dots) dot.number = docNumber.get(dot.document) || 0;
  for (const sector of layout.sectors) {
    sector.numbers = sector.keywords.map((k) => keywordNumber.get(k) || 0);
  }

  return {
    checked,
    pinned,
    rail,
    keywordNumbers: Object.fromEntries(keywordNumber),
    docNumbers: Object.fromEntries(docNumber),
    universe: ev.universe,
    matched: ev.matched,          // recipe membership (innermost ring)
    rings: layout.rings,
    sectors: layout.sectors,
    dots: layout.dots,
    matrix: matrixRows(ev.rows, checked, docNumber),
    formingSet: formingSet(ev, includes, excludes),
    coOccurrence: coOccurrenceHints(snapshot, checked, pinned),
    recipeLine: recipeLine(checked, pinned, includes, excludes),
  };
}

// Doc summary/basename lookup for the renderer (kept out of the plain-data
// model so the model stays JSON-serialisable for the node cross-checks).
export function docSummaries(snapshot) {
  const map = {};
  for (const d of snapshot?.documents || []) {
    map[d.id] = { base: String(d.id).split("/").pop() || d.id, summary: d.summary || null };
  }
  return map;
}

// ---- persistence plans (T024) — mirror lens.py; the browser confirms a PLAN,
// the tested Python engine materialises the manifest through the boundary.

// Gitignored workbench prefix + manifest path — MUST match workbench.WORKBENCH_DIR
// / manifest_relpath (locked by a JS/Python cross-check in test_lens.py).
export const WORKBENCH_DIR = "ideation/workbench/";

// The pending-proposal note — MUST be byte-identical to lens.PENDING_PROPOSAL_NOTE.
export const PENDING_PROPOSAL_NOTE =
  "Workbench reference set created (recipe-seeded, through the engine + " +
  "boundary) and the human-seen cluster proposal submitted to the " +
  "cross-reference queue with a pending_review disposition — a disposing " +
  "authority reviews it; it never bypasses review, and on acceptance it " +
  "becomes a topic cluster.";

// The slug's BOUND and its key half — MUST match workbench.MAX_SLUG_CHARS /
// _SLUG_KEY_SEPARATOR / _SLUG_KEY_DIGEST_CHARS. A slug is a filename component,
// and the lens's default set name is derived from every checked keyword, so past
// roughly 13-14 keywords an unbounded slug named a path the filesystem refuses —
// which the confirm dialog rendered as its "lands at:" line while the route died
// on it with an unhandled OSError (T092 acceptance sweep, defect 2).
export const MAX_SLUG_CHARS = 200;
const SLUG_KEY_SEPARATOR = "-k";
const SLUG_KEY_DIGEST_CHARS = 16;

// 64-bit FNV-1a over the full slug, hex — mirrors workbench._slug_key_digest.
// FNV rather than sha256 because THIS side has to compute it synchronously to
// render the plan, and the browser's only built-in sha256 is async; the digest
// disambiguates two long derived names and defends against nothing (see the
// Python docstring for the whole reasoning). The slug alphabet is ASCII by
// construction here, so char codes are bytes.
function slugKeyDigest(value) {
  let digest = 0xcbf29ce484222325n;
  for (let i = 0; i < value.length; i += 1) {
    digest = ((digest ^ BigInt(value.charCodeAt(i))) * 0x100000001b3n)
      & 0xffffffffffffffffn;
  }
  return digest.toString(16).padStart(SLUG_KEY_DIGEST_CHARS, "0");
}

// Single safe path segment from a set name — mirrors workbench.slug, BOUND
// included: at or under the bound the slug is unchanged, above it the stem is
// truncated and keyed with the digest of the whole slug.
export function slug(value) {
  let v = String(value == null ? "" : value).trim().toLowerCase();
  // The two prior replaces leave at most ONE leading/trailing dash (runs are
  // already collapsed), so a single-char trim is equivalent to `^-+|-+$` without
  // the quantifier that triggers the super-linear-backtracking smell (S8786).
  v = v.replace(/[^a-z0-9-]+/g, "-").replace(/-{2,}/g, "-").replace(/^-|-$/g, "");
  if (!v) return "untitled";
  if (v.length <= MAX_SLUG_CHARS) return v;
  const keep = MAX_SLUG_CHARS - SLUG_KEY_SEPARATOR.length - SLUG_KEY_DIGEST_CHARS;
  return v.slice(0, keep).replace(/-$/, "") + SLUG_KEY_SEPARATOR + slugKeyDigest(v);
}

export function manifestRelpath(name) {
  return WORKBENCH_DIR + slug(name) + ".workbench.yaml";
}

// The on-screen PLAN of a "save recipe" persistence: checked/pinned + the
// forming-set members (recipe-match auto + manual-include overrides) + the
// excluded overrides + where the manifest lands. Pure preview; the actual
// boundary-written manifest is lens.build_workbench_from_recipe + save.
export function savePlan(model, repository, name) {
  return {
    kind: "save-recipe",
    repository,
    name,
    checked: model.checked,
    pinned: model.pinned,
    members: model.formingSet.members,
    excluded: model.formingSet.excluded,
    recipeLine: model.recipeLine,
    landsAt: manifestRelpath(name),
  };
}

// The on-screen PLAN of "add as cluster": the same recipe-seeded manifest PLUS
// the note that the human-seen cross-reference-queue proposal enters with a
// pending_review disposition (T028 realized 2026-07-14; the tested engine
// lens.add_as_cluster submits it via human_seen.py — this surface previews the
// plan, the browser writes nothing).
export function clusterPlan(model, repository, name) {
  const plan = savePlan(model, repository, name);
  plan.kind = "add-as-cluster";
  plan.pendingNote = PENDING_PROPOSAL_NOTE;
  return plan;
}

// The two gate routes the lens verbs post to (add-lens-gate-verbs). Mirrors the
// dispose/propose route constants — the deployed static image never serves
// these; the plan panel probes the gate capability before revealing execute.
export const LENS_SAVE_ROUTE = "/actions/gate/lens-save-recipe";
export const LENS_CLUSTER_ROUTE = "/actions/gate/lens-add-as-cluster";

// The request body a save-recipe / add-as-cluster plan posts to its verb route.
// PURE: derives the recipe (checked/pinned) + the reasoned overrides from the
// SAME plan the panel confirmed — the server re-evaluates membership from these
// keywords against the pinned snapshot (it never trusts this member list), so
// the body carries only the human's inputs (recipe + reasons), not a derived set.
export function recipeRequest(plan) {
  const includes = {};
  for (const m of plan.members || []) {
    if (m.via === "manual-include" && m.reason) includes[m.document] = m.reason;
  }
  const excludes = {};
  for (const e of plan.excluded || []) excludes[e.document] = e.reason;
  return {
    repository: plan.repository,
    name: plan.name,
    checked: [...(plan.checked || [])],
    pinned: [...(plan.pinned || [])],
    includes,
    excludes,
  };
}

// The add-as-cluster body: the recipe request PLUS the human-seen organizer
// evidence block (proposer + committed revision + passage hash + section +
// rationale + confidence + alternatives). The engine enforces completeness
// BEFORE persistence, so an incomplete `evidence` still posts and the refusal
// renders verbatim — this builder never pre-validates.
export function clusterRequest(plan, evidence) {
  const body = recipeRequest(plan);
  body.evidence = evidence || {};
  return body;
}
