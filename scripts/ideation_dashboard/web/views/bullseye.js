// THE ONE match-count bullseye renderer (openxFactory
// `add-workbench-bullseye-and-create`, design D1/D6). Lifted VERBATIM out of
// views/lens.js so the keyword-lens tab and the staging workbench's lens panel
// draw the SAME rings, sectors, and dots from the SAME geometry — two
// hand-written SVG layouts over one `bullseyeLayout()` would drift silently
// (a ring label, a dot radius, the centre shading) and only a screenshot
// comparison would catch it.
//
// PURE of view state: the only inputs are a `buildLensModel()` result and
// `GEOM` (lens-model.js). No snapshot read, no derivation, no transport — the
// module issues no network call of any kind and holds no module-level state, so
// both callers can mount it as often as they redraw.
//
// THE CREATE GESTURE (design D6, EXTENDED by Brett's 2026-07-25 ruling on
// `add-workbench-bullseye-and-create` open question 2): `opts.onActivate`, when
// supplied, makes EVERY region of the bullseye an activatable, keyboard-reachable
// hit region — the matches-ALL centre zone AND each ring SECTOR. The centre is
// Brett's gesture from `ideation/brainstorm/lens-brainstorm-session-launch.md`
// ("clicking the bullseye's center ring starts a brainstorm session focused on
// the checked keyword set"); the ruling widened it because the rings are ALREADY
// sectored by which checked keywords matched, so a sector names a specific
// combination the human can act on directly instead of unchecking their way down
// to it. Every region is one `role="button" tabindex="0"` node in tab order.
//
// The callback is `onActivate(region)` with
// `{ kind: "centre"|"sector", keywords: [...], subsetKey }` — the region reports
// its own matched-keyword combination so no caller re-derives it from geometry
// or re-splits the joined label. `keywords` is the WHOLE checked set for the
// centre and the sector's own subset for a sector.
//
// With NO callback supplied NO region is rendered at all, so the keyword-lens
// tab's SVG is byte-identical to what it drew before the lift. A caller that
// wires the gesture MUST also carry a labelled button: an unlabelled hit region
// is undiscoverable, which is why the gesture is never the only affordance.
//
// DOM-SAFETY: every dynamic value binds through textContent (the svg() helper's
// text argument); innerHTML is never touched here.

import {
  GEOM, ringLabelIndices, sectorLabelText, clampLabel, labelBox, labelFits,
  nonOverlappingIndices,
} from "./lens-model.js";

// The three label faces, from styles.css (`.bullseye .ringlab|.seclab|.doclab`).
// Restated here because the geometry has to know the box the text occupies —
// that is the whole of defect 9 — and an SVG cannot ask CSS before it lays out.
const FONT = { ring: 10, sector: 14, doc: 10 };

// How far outside the outermost ring the SECTOR labels ride. Wide enough to
// clear the dot-label band that now sits just outside the outermost dots.
const SECTOR_LANE = 22;

const SVG_NS = "http://www.w3.org/2000/svg";  // w3.org XML namespace (not a fetch)

function svg(tag, attrs, text) {
  const node = document.createElementNS(SVG_NS, tag);
  for (const [k, v] of Object.entries(attrs || {})) node.setAttribute(k, String(v));
  if (text != null) node.textContent = text;
  return node;
}

function round(n) { return Math.round(n * 100) / 100; }

// One arc of `radius` from `a0` to `a1` degrees, as an SVG path. Kept here
// with the other pure geometry; no state, no DOM read.
function arcPath(cx, cy, radius, a0, a1) {
  const p0 = [cx + radius * Math.cos((a0 * Math.PI) / 180),
              cy + radius * Math.sin((a0 * Math.PI) / 180)];
  const p1 = [cx + radius * Math.cos((a1 * Math.PI) / 180),
              cy + radius * Math.sin((a1 * Math.PI) / 180)];
  const large = Math.abs(a1 - a0) > 180 ? 1 : 0;
  return "M " + round(p0[0]) + " " + round(p0[1])
    + " A " + round(radius) + " " + round(radius) + " 0 " + large + " 1 "
    + round(p1[0]) + " " + round(p1[1]);
}

// Wire ONE hit node: click and Enter/Space both call `onActivate(region)`. The
// single seam for every activatable region, so the centre and a sector can never
// diverge in what they do or in how a keyboard reaches them.
function activate(hit, opts, region) {
  hit.setAttribute("role", "button");
  hit.setAttribute("tabindex", "0");
  hit.setAttribute("aria-label", region.label);
  hit.appendChild(svg("title", {}, region.label));
  hit.addEventListener("click", (ev) => { ev.preventDefault(); opts.onActivate(region); });
  hit.addEventListener("keydown", (ev) => {
    if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); opts.onActivate(region); }
  });
}

// The activatable centre zone (matches-ALL). Rendered UNDER the dots so a dot's
// own hover/title still wins, and only when a caller supplies `onActivate`.
function centreGesture(node, ring, model, opts) {
  const g = GEOM;
  const hit = svg("circle", {
    class: "bullseye-centre", cx: g.cx, cy: g.cy, r: round(ring.outerRadius),
  });
  activate(hit, opts, {
    kind: "centre", keywords: [...model.checked],
    subsetKey: model.checked.join(" ∧ "),
    label: opts.centreLabel || "create a document from the matches-all centre ring",
  });
  node.appendChild(hit);
}

// The annulus-segment path for one sector: a `spanDeg`-wide slice of the ring
// band its subset size puts it on. Built from the sector's own geometry fields
// (lens-model.js) so the hit shape and the dots inside it come from ONE
// derivation. A sector reaching the centre (innerRadius 0) closes through the
// middle rather than drawing a zero-radius inner arc.
function sectorPath(sec) {
  const g = GEOM;
  const half = sec.spanDeg / 2;
  const a0 = ((sec.angleDeg - half) * Math.PI) / 180;
  const a1 = ((sec.angleDeg + half) * Math.PI) / 180;
  const big = sec.spanDeg > 180 ? 1 : 0;
  const pt = (r, a) => round(g.cx + r * Math.cos(a)) + " " + round(g.cy + r * Math.sin(a));
  const outer = round(sec.outerRadius);
  if (!sec.innerRadius) {
    return "M " + round(g.cx) + " " + round(g.cy) + " L " + pt(sec.outerRadius, a0) +
      " A " + outer + " " + outer + " 0 " + big + " 1 " + pt(sec.outerRadius, a1) + " Z";
  }
  const inner = round(sec.innerRadius);
  return "M " + pt(sec.innerRadius, a0) + " L " + pt(sec.outerRadius, a0) +
    " A " + outer + " " + outer + " 0 " + big + " 1 " + pt(sec.outerRadius, a1) +
    " L " + pt(sec.innerRadius, a1) +
    " A " + inner + " " + inner + " 0 " + big + " 0 " + pt(sec.innerRadius, a0) + " Z";
}

// The activatable ring sectors (open question 2's ruling). The matches-ALL
// sector is SKIPPED: the centre region already covers that exact combination,
// and two stacked hit nodes over one zone would put the same gesture into tab
// order twice.
function sectorGestures(node, model, opts) {
  for (const sec of model.sectors) {
    if (sec.isCenter || !sec.keywords.length) continue;
    const hit = svg("path", { class: "bullseye-sector", d: sectorPath(sec) });
    activate(hit, opts, {
      kind: "sector", keywords: [...sec.keywords], subsetKey: sec.subsetKey,
      label: "create a document from the " + sec.keywords.join(" ∧ ") +
        " combination (" + sec.matchCount + " of " + model.checked.length +
        " checked)",
    });
    node.appendChild(hit);
  }
}

// Render the bullseye for one lens model. `opts.onActivate(region)` wires the
// create gesture on EVERY region — the centre zone and each ring sector (design
// D6 as ruled); `opts.centreLabel` overrides the centre region's label.
export function renderBullseye(model, opts) {
  const o = opts || {};
  // `opts.onDocument(document)` makes a DOT a control for its own document —
  // the lens uses it to toggle that document's selection, so clicking a dot
  // and ticking its matrix row write the same state (Brett, 2026-08-09).
  // Absent, every dot is exactly as inert as it was.
  const onDocument = typeof o.onDocument === "function" ? o.onDocument : null;
  const g = GEOM;
  const node = svg("svg", {
    class: "bullseye", viewBox: "0 0 " + g.size + " " + g.size, role: "img",
    "aria-label": "Bullseye: rings by number of checked keywords matched " +
      "(innermost matches all); the matrix below carries the same membership.",
  });

  if (!model.checked.length) {
    node.appendChild(svg("text", { class: "ringlab", x: g.cx, y: g.cy, "text-anchor": "middle" },
      "check a keyword to stratify the corpus"));
    return node;
  }

  // rings (outer → inner), with the centre zone shaded. Every ring is DRAWN;
  // the labels are THINNED to the ones that fit (defect 9a — the stride is
  // rMax/n, so past ~16 rings every adjacent pair collides and the whole column
  // becomes unreadable). The matches-ALL centre and the outermost ring always
  // read; a ring whose label is dropped is still named by its dots' titles.
  const labelled = new Set(ringLabelIndices(model.rings.map((r) => r.outerRadius)));
  // Ring labels are the orienting frame and are drawn FIRST, so their boxes
  // are already occupied when the sector labels — which now sit at their own
  // ring rather than out at the rim — are placed.
  const ringBoxes = [];
  model.rings.forEach((ring, i) => {
    node.appendChild(svg("circle", {
      class: "ring" + (ring.isCenter ? " zone0" : ""),
      cx: g.cx, cy: g.cy, r: round(ring.outerRadius),
    }));
    if (!labelled.has(i)) return;
    // The label rides its own ring, in the widest arc that ring leaves empty
    // (the model picks the angle) — so it is clear of the dot band whatever
    // the band's depth, which radial nudging could not achieve once the dots
    // grew. A ring with nothing on it keeps the familiar top position.
    const angle = ((ring.labelAngle == null ? -90 : ring.labelAngle) * Math.PI) / 180;
    const lr = ring.outerRadius - 8;
    const at = clampLabel(g.cx + lr * Math.cos(angle), g.cy + lr * Math.sin(angle),
      ring.label.length, FONT.ring, g.size);
    node.appendChild(svg("text", {
      class: "ringlab", x: round(at.x), y: round(at.y), "text-anchor": "middle",
    }, ring.label));
    ringBoxes.push(labelBox(at.x, at.y, ring.label.length, FONT.ring));
  });

  // the create gesture (design D6, ruled to cover every region) — only when a
  // caller wires it. Both region families are appended HERE, under the sector
  // dividers, labels, and dots below, so a dot's own title still wins on hover
  // and the labels stay readable over the hit shapes.
  if (typeof o.onActivate === "function") {
    const centre = model.rings.find((r) => r.isCenter);
    if (centre) centreGesture(node, centre, model, o);
    sectorGestures(node, model, o);
  }

  // sector dividers, one per distinct matched subset. The DIVIDERS are always
  // drawn; the labels below are truncated, clamped into the viewBox and dropped
  // on collision (defect 9b — the full conjunction ran up to 464px wide in a
  // 520px box, so 10 of 20 were clipped at 18 keywords and the reader saw
  // "keyw" / "ideat" fragments naming the wrong sector).
  const seclabs = [];
  for (const sec of model.sectors) {
    const a = (sec.angleDeg * Math.PI) / 180;
    // A sector's documents only ever occupy ITS OWN ring band, so the divider
    // reaches only that far (Brett's 2026-08-07 finding: a full-radius spoke
    // and a rim label made a three-keyword sector look like it lived on the
    // outer ring, 60px from the dot it names).
    const from = sec.innerRadius != null ? sec.innerRadius : 0;
    const to = sec.outerRadius != null ? sec.outerRadius : g.rMax;
    node.appendChild(svg("line", {
      class: "sector",
      x1: round(g.cx + from * Math.cos(a)), y1: round(g.cy + from * Math.sin(a)),
      x2: round(g.cx + to * Math.cos(a)), y2: round(g.cy + to * Math.sin(a)),
    }));
    // The sector's OWN ARC, painted in its keywords' hues — one equal segment
    // each, so a combination sector shows every term it belongs to and the
    // reader can find "A" by colour instead of reading every label. Drawn on
    // the band's outer edge, under everything, and kept subtle by the
    // stylesheet (the hue is the only thing decided here).
    if (Array.isArray(sec.hues) && sec.hues.length) {
      const half = (sec.spanDeg * 0.9) / 2;
      const segments = sec.hues.length;
      for (let s = 0; s < segments; s += 1) {
        const a0 = sec.angleDeg - half + (2 * half * s) / segments;
        const a1 = sec.angleDeg - half + (2 * half * (s + 1)) / segments;
        node.appendChild(svg("path", {
          class: "secarc",
          style: "--h: " + sec.hues[s],
          d: arcPath(g.cx, g.cy, to - 1.5, a0, a1),
        }));
      }
    }
    // the matches-ALL sector is the shaded centre, already named by its ring
    // label ("all N ✓") — a second label on top of it would be noise
    if (sec.isCenter) continue;
    // The radar labels a sector by its keywords' RAIL LETTERS — "A ∧ G"
    // instead of a 464px conjunction, and letters rather than numbers so a
    // sector label can never be mistaken for a document's. The full
    // combination stays in the <title> below and in the rail, the legend.
    const text = sec.labels && sec.labels.length
      ? sec.labels.join(" ∧ ")
      : sectorLabelText(sec.subsetKey, sec.keywords);
    // …placed just outside the sector's OWN ring, beside the dots it names.
    // The outermost ring keeps a wider offset so its labels clear the dot
    // labels, which sit just outside their dots on that same band.
    // ONE lane per ring. A second radial lane was tried for the 14px
    // letters and does not pay: further out runs into the viewBox edge,
    // where clampLabel piles labels up (32 drawn versus 34), and further in
    // is where the dots are.
    const lane = (sec.outerRadius >= g.rMax - 0.001) ? SECTOR_LANE : 8;
    const lr = (sec.outerRadius != null ? sec.outerRadius : g.rMax) + lane;
    const at = clampLabel(g.cx + lr * Math.cos(a), g.cy + lr * Math.sin(a),
      text.length, FONT.sector, g.size);
    seclabs.push({ sec, text, at,
      box: labelBox(at.x, at.y, text.length, FONT.sector) });
  }
  const drawnSectorLabels = nonOverlappingIndices(
    ringBoxes.concat(seclabs.map((s) => s.box)))
    .filter((i) => i >= ringBoxes.length)
    .map((i) => i - ringBoxes.length);
  for (const i of drawnSectorLabels) {
    const { sec, text, at } = seclabs[i];
    const attrs = {
      class: "seclab", x: round(at.x), y: round(at.y), "text-anchor": "middle",
    };
    // a single-term sector carries that term's hue on its letter too, which
    // is the most direct "A is over there" the widget can offer
    if (Array.isArray(sec.hues) && sec.hues.length === 1) {
      // inline, because the stylesheet's own `fill` outranks a presentation
      // attribute — the first pass set the attribute and nothing changed
      // the HUE only, plus a flag the stylesheet keys on, so the theme
      // composes the colour and a tint never lands dark-on-dark
      attrs.style = "--h: " + sec.hues[0];
      attrs["data-tinted"] = "";
    }
    const label = svg("text", attrs, text);
    // the untruncated combination stays reachable on hover, where it was
    // already the authority for the hit region
    label.appendChild(svg("title", {}, sec.subsetKey));
    node.appendChild(label);
  }

  // dots — solid declared dots; the <title> carries the per-keyword match line.
  // Every dot is drawn. Its LABEL is drawn only when the box clears every label
  // already placed (defect 9c — a ring holds every document with the same match
  // count, so 66 label pairs overlapped at TWO checked keywords on the real
  // corpus; on a two-document fixture nothing overlaps and nothing is dropped).
  const dots = model.dots.map((d) => {
    const base = String(d.document).split("/").pop() || d.document;
    // the dot's LABEL is its matrix number; the basename stays in the title
    const text = d.number ? String(d.number) : base;
    // WHICH dots carry a label is the model's call (`packCell`): the outer
    // lane of a cell, and in a CROWDED cell only every other column of it.
    // Two inferences carry the rest, both small arithmetic:
    //   * down a column — the dots inboard of a labelled one are +1, +2, +3,
    //     because a column is numbered outer lane inward;
    //   * across to the next column — one column deeper than the label, so
    //     the unlabelled neighbour starts where the labelled column ended.
    // A dot big enough carries its number INSIDE (drawn with the dot below,
    // not in this outside-label pass), so it never enters the collision set.
    const inside = d.inside === true && d.number;
    const labelled = !inside && (d.labelled != null
      ? d.labelled : (d.row == null || d.row === 0));
    // The label sits RADIALLY OUTWARD of its dot — away from the centre, so
    // it never lands on the rows packed inside it — in two lanes, alternating
    // by slot, which is what lets neighbours on one arc both read.
    const outward = (d.size || 6) + 6 + (d.slot === 1 ? 11 : 0);
    const a = ((d.angleDeg == null ? 0 : d.angleDeg) * Math.PI) / 180;
    const lr = (d.radius || 0) + outward;
    const at = clampLabel(g.cx + lr * Math.cos(a), g.cy + lr * Math.sin(a) + 3.5,
      text.length, FONT.doc, g.size);
    return { d, base, text, at,
      fits: labelled && labelFits(text.length, FONT.doc, g.size),
      box: labelBox(at.x, at.y, text.length, FONT.doc) };
  });
  // a basename wider than the canvas cannot be labelled legibly at any anchor;
  // it is dropped rather than centred as an overflow, and its <title> still
  // carries the name. `nonOverlappingIndices` is fed a box that cannot collide
  // for those, so the indices stay aligned with `dots`.
  // The collision pass sees the SECTOR labels too: they are already drawn, so
  // a dot label that would sit on one is dropped rather than overprinting it
  // (its number stays on the dot's title and in the matrix). Their boxes go
  // in first and are then discarded, so the surviving indices still line up
  // with `dots`.
  const placedBoxes = ringBoxes.concat(
    drawnSectorLabels.map((i) => seclabs[i].box));
  const shown = new Set(nonOverlappingIndices(
    placedBoxes.concat(dots.map(
      (x) => (x.fits ? x.box : { left: 0, right: 0, top: 0, bottom: 0 }))))
    .filter((i) => i >= placedBoxes.length)
    .map((i) => i - placedBoxes.length));
  dots.forEach(({ d, base, text, at }, i) => {
    // The dot NAMES ITS DOCUMENT. A number on a dot and a number in a table
    // are two coordinates for one thing, and the reader was doing the join by
    // eye (Brett, 2026-08-08: "when I hover on one of these documents, the
    // corresponding dot should light up"). The renderer publishes the key; the
    // lens does the lighting, so the widget keeps no cross-view state.
    const gdot = svg("g", { class: "lensdot", "data-doc": String(d.document) });
    const circle = svg("circle", {
      class: "dot" + (d.declared ? " declared" : " inferred"),
      // the packed size: a crowded cell draws smaller dots rather than
      // overlapping ones (lens-model `packCell`). The matches-ALL centre
      // keeps its slightly larger dot where the packing leaves room for it.
      cx: round(d.x), cy: round(d.y),
      r: round(d.size != null
        ? d.size + (d.matchCount === model.checked.length && d.size >= 6 ? 1 : 0)
        : (d.matchCount === model.checked.length ? 7 : 6)),
    });
    circle.appendChild(svg("title", {},
      (d.number ? "#" + d.number + " " : "") + base + " — "
      + d.matchedSubset.join(" ✓ ") + " ✓"));
    // A DOT IS ITS DOCUMENT'S CHECKBOX (Brett, 2026-08-09: "when I click a
    // dot. make it work like checking the box on the doc"). The radar is where
    // the convergence is READ, so it is where the selection should be MADE —
    // writing the same state the matrix row's box writes, so the two can never
    // disagree. `stopPropagation` keeps the click off the hit region beneath
    // it, which activates a whole drill-in. The BOX remains the keyboard path:
    // 95 focusable dots would flood the tab order to no benefit.
    if (onDocument) {
      circle.style.cursor = "pointer";
      gdot.addEventListener("click", (ev) => {
        ev.stopPropagation();
        onDocument(String(d.document));
      });
    }
    gdot.appendChild(circle);
    // the inside number: centred on the dot, so it moves with it and can
    // never be dropped for want of room beside it
    if (d.inside === true && d.number) {
      gdot.appendChild(svg("text", {
        class: "dotnum", x: round(d.x), y: round(d.y),
        "text-anchor": "middle", "dominant-baseline": "central",
      }, String(d.number)));
    }
    if (shown.has(i) && dots[i].fits) {
      gdot.appendChild(svg("text", {
        class: "doclab", x: round(at.x), y: round(at.y), "text-anchor": "middle",
      }, text));
    }
    node.appendChild(gdot);
  });
  return node;
}
