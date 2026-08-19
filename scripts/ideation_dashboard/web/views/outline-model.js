// The staged-topic outline model (add-staged-topic-outline-template, tasks
// 3.1-3.2).
//
// PURE. No DOM, no fetch, no markdown rendering — it turns a primary fragment's
// TEXT into the sections the outline tab renders, so the tab can show a topic's
// structure instead of undifferentiated prose, and (below) into the whole next
// text with ONE section added, which is what the tab's add-section affordance
// hands to the canvas buffer.
//
// Section identity comes from the fragment's own `## ` headings and its `xspec:`
// marker fences — the addressing grammar the template already uses. It is NEVER
// content-sniffed and NEVER fabricated: a heading the fragment does not carry
// does not appear, because a reader must be able to trust that what the tab
// shows is what the file says.
//
// FENCE-AWARE, and this is not incidental. The canonical template ships as a
// copy-pasteable ```markdown skeleton whose body contains every required
// heading. A fragment that merely QUOTES the skeleton has not adopted it, and a
// naive scanner would report the quoter as fully conforming — the same defect
// class that made `proposal-support.py verify` fail a correct bundle and that
// `doc_health.families._scan_lines` has tracked for longer than either.
//
// The classification here MIRRORS doc-health's `staged-topic-template` family
// (`_TEMPLATE_SECTIONS`, `_QUESTION_SUBFIELDS`). The checker and the surface
// must agree about what conformance means; change both together or neither.

export const REQUIRED_SECTIONS = [
  { needle: "idea notes", label: "pre-document idea notes" },
  { needle: "conflicts", label: "conflicts" },
  { needle: "open questions", label: "open questions" },
];

export const QUESTION_SUBFIELDS = [
  "Context", "Recommended answer", "Explanation", "Disposition status",
];

// `<!-- xspec:candidate ... -->` / `<!-- xspec:supersedes ... -->`
const XSPEC_RE = /<!--\s*xspec:(candidate|supersedes)\b/;

function isFence(line) {
  return String(line).trimStart().startsWith("```");
}

/** Split `text` into `## ` sections, ignoring everything inside code fences. */
export function outlineSections(text) {
  const lines = String(text == null ? "" : text).split("\n");
  const sections = [];
  let current = null;
  let fenced = false;

  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];
    if (isFence(line)) {
      fenced = !fenced;
      if (current) current.body.push(line);
      continue;
    }
    if (!fenced && line.startsWith("## ")) {
      current = {
        title: line.slice(3).trim(),
        line: i + 1,
        body: [],
        questions: [],
        addedBy: null,
        marked: false,
      };
      sections.push(current);
      continue;
    }
    if (!current) continue;
    current.body.push(line);
    if (!fenced) {
      if (XSPEC_RE.test(line)) current.marked = true;
      const provenance = /^Added-by:\s*(.+?)\s*$/.exec(line);
      if (provenance && !current.addedBy) current.addedBy = provenance[1];
      if (line.startsWith("### ")) {
        current.questions.push({ title: line.slice(4).trim(), fields: [] });
      } else if (current.questions.length) {
        const question = current.questions[current.questions.length - 1];
        for (const field of QUESTION_SUBFIELDS) {
          if (line.startsWith(field + ":") && !question.fields.includes(field)) {
            question.fields.push(field);
          }
        }
      }
    }
  }

  for (const section of sections) {
    const lower = section.title.toLowerCase();
    const required = REQUIRED_SECTIONS.find((s) => lower.includes(s.needle));
    section.role = required ? "required" : (section.marked ? "proposal-element" : "added");
    section.requiredLabel = required ? required.label : null;
    if (!lower.includes("open questions")) section.questions = [];
  }
  return sections;
}

/** What this fragment does not meet — empty means conforming. */
export function outlineGaps(sections) {
  const gaps = [];
  for (const { needle, label } of REQUIRED_SECTIONS) {
    const present = sections.some(
      (s) => s.title.toLowerCase().includes(needle));
    if (!present) gaps.push({ kind: "missing-section", label });
  }
  for (const section of sections) {
    for (const question of section.questions) {
      const missing = QUESTION_SUBFIELDS.filter(
        (f) => !question.fields.includes(f));
      if (missing.length) {
        gaps.push({ kind: "incomplete-question", label: question.title, missing });
      }
    }
  }
  return gaps;
}

/**
 * The tab's whole verdict for one fragment.
 *
 * DEGRADES, NEVER REFUSES. Topics staged before the template ratified are
 * conformant only opt-in, so a fragment carrying none of the required sections
 * is rendered as what it is — sections and all — and reported as `pre-template`
 * rather than as broken. Nothing here rewrites a fragment; conformance is
 * earned when a human next works the topic, never by the act of opening it.
 */
export function outlineModel(text) {
  const sections = outlineSections(text);
  const gaps = outlineGaps(sections);
  const anyRequired = sections.some((s) => s.role === "required");
  let state = "conforming";
  if (gaps.length) state = anyRequired ? "partial" : "pre-template";
  return { sections, gaps, state, conforming: gaps.length === 0 };
}

// ---- the add-section half (task 3.2) ----------------------------------------
//
// STILL PURE, and deliberately so: the affordance in staging-workbench.js
// computes the WHOLE next text here and hands it to the canvas's own
// `applyProposal`, which owns the settled-identity gate, the line-ending
// discipline and the dirty state. Nothing in this file writes, fetches, or knows
// what a buffer is — which is also what keeps every rule below testable without
// a DOM.

// The canonical heading order from the ratified skeleton
// (`docs/document-lifecycle.md`, "The Staged-Topic Outline Template"), as the
// lowercase needles a heading is matched by. It has exactly ONE job: deciding
// which existing section a new one goes next to, so an add never reorders
// material a human already wrote. A heading matching no needle has no canonical
// place — it is anchored explicitly or appended.
export const TEMPLATE_ORDER = [
  "last proposal attempt", "claims", "why", "what changes", "impact",
  "idea notes", "conflicts", "open questions", "exit",
];

/** This heading's place in the canonical order, or null when it has none. */
export function sectionRank(title) {
  const lower = String(title == null ? "" : title).toLowerCase();
  const at = TEMPLATE_ORDER.findIndex((needle) => lower.includes(needle));
  return at < 0 ? null : at;
}

// The heading each required section is added AS, and the body it is seeded with
// — both CARRIED from the ratified skeleton rather than reinvented, so a section
// added here is one doc-health's `staged-topic-template` family already accepts.
// The open-questions seed carries all four sub-fields for that reason: a bare
// question is non-conforming by the contract's own rule, so seeding one would
// be adding a defect.
//
// `Added-by:` PLACEMENT follows the contract, which is not uniform and should
// not be made so here: the skeleton stamps the required trio's provenance on the
// note or question itself (the line the human is about to write), and reserves a
// section-level `Added-by:` line for a section BEYOND the required set — the one
// the contract says "must stay attributable as it accumulates content nobody
// commissioned".
const REQUIRED_TEMPLATES = {
  "idea notes": {
    heading: "Idea notes (pre-document, non-documented)",
    body: (stamp) => ["- <idea note text> — Added-by: " + stamp],
  },
  conflicts: {
    heading: "Conflicts",
    body: (stamp) => ["- <conflict text> — Added-by: " + stamp],
  },
  "open questions": {
    heading: "Open questions",
    body: (stamp) => [
      "### Q1. <question, as a single sentence>",
      "",
      "Context: <what makes this undecided; what facts bear on it>",
      "Recommended answer: <a position, stated plainly — not a survey of options>",
      "Explanation: <why this is the recommended answer — the reasoning, not a "
        + "restatement of the recommendation>",
      "Disposition status: open",
      "Added-by: " + stamp,
    ],
  },
};

// TWO WAYS TO REACH A TEMPLATE, and keeping them apart is the whole of PR
// review finding F2.
//
// `requiredTemplateFor` is the REQUIRED-GAP route: the caller is the gap row's
// own button, which asks by the contract's LABEL ("pre-document idea notes"), so
// a loose `includes` match against the label's needle is doing necessary work.
// It is reached only when the caller declares `required: true`.
//
// `templateForExactHeading` is the FREE-FORM route, and it is exact on purpose.
// A human typing "Notes on conflicts" or "Conflicts with promoted specs" means
// that heading and not the required Conflicts section; the loose match used to
// silently rewrite the first to `## Conflicts` and refuse the second as a
// duplicate. The contract grants that a human or an AI "may add a section beyond
// the required set", and this is the only route to it, so anything but an exact
// canonical heading is written verbatim with the generic skeleton.
function requiredTemplateFor(title) {
  const lower = String(title == null ? "" : title).toLowerCase();
  const match = REQUIRED_SECTIONS.find((s) => lower.includes(s.needle));
  return match ? REQUIRED_TEMPLATES[match.needle] : null;
}

function templateForExactHeading(title) {
  const key = String(title == null ? "" : title).trim().toLowerCase();
  for (const needle of Object.keys(REQUIRED_TEMPLATES)) {
    const template = REQUIRED_TEMPLATES[needle];
    if (template.heading.toLowerCase() === key) return template;
  }
  return null;
}

// WHICH ROUTE A TITLE TOOK, answered in ONE place. `insertSection` needs it for
// the rank and `sectionSkeleton` for the heading and seed, and two resolutions of
// the same fact are two things to keep in step.
function resolveTemplate(title, required) {
  return required === true
    ? requiredTemplateFor(title)
    : templateForExactHeading(title);
}

/**
 * The text ONE added section is written as — heading, blank line, seeded body.
 *
 * Every slot stays a `<…>` fill-in, exactly as the skeleton ships them: the
 * affordance adds a section's SHAPE and its provenance, never content it made
 * up on the human's behalf.
 *
 * `required` names the gap-row route and is what licenses the canonical heading
 * and seed. Without it the title is written VERBATIM unless it already IS a
 * canonical heading, letter for letter.
 */
export function sectionSkeleton(title, { addedBy, date, required } = {}) {
  const stamp = String(addedBy || "unattributed") + " · " + String(date || "undated");
  const template = resolveTemplate(title, required);
  const heading = template ? template.heading : String(title == null ? "" : title).trim();
  const body = template
    ? template.body(stamp)
    : ["Added-by: " + stamp, "", "- <fill this in>"];
  return ["## " + heading, "", ...body].join("\n");
}

/**
 * True when the fragment's last code fence is never closed.
 *
 * The SAME `isFence` rule `outlineSections` toggles on, so the two cannot
 * disagree about where a fence is — this is not a second scanner, it is the one
 * fact that scanner's loop knows and does not report. `insertSection` refuses on
 * it, because inside an unclosed fence every heading is invisible to the model:
 * the append lands inside the fence, the duplicate guard then sees no sections at
 * all, and repeated presses pile up copies each reporting success.
 */
export function endsInsideFence(text) {
  let fenced = false;
  for (const line of String(text == null ? "" : text).split(/\r\n|\r|\n/)) {
    if (isFence(line)) fenced = !fenced;
  }
  return fenced;
}

// Where a section's own text stops: the next `## ` heading, or the end.
function sectionEnd(sections, target, total) {
  const next = sections[sections.indexOf(target) + 1];
  return next ? next.line - 1 : total;
}

/**
 * The whole next text of a fragment with ONE section added, or a stated refusal.
 *
 * `required: true` is the GAP-ROW route: the caller is asking for one of the
 * three required sections by the contract's own label, so the section lands under
 * its canonical heading with its canonical seed, in its canonical place, and a
 * section of the same RANK already present is a refusal. Everything else is
 * free-form: the title is written verbatim, the duplicate rule is exact-title
 * equality, and canonical placement applies only to a title that already IS a
 * canonical heading. That split is PR review finding F2 — a rank-wide refusal on
 * the free-form path made "Exit criteria", "Impact analysis" and
 * "Conflicts with promoted specs" all unaddable on a conforming fragment, which
 * is the only route the contract gives a human for adding one.
 *
 * `after` names the section the new one is inserted behind — the patch's
 * addressing key, and the "scoped by the target section" half of the contract.
 * Omitted, a canonical heading takes its canonical place (behind the last
 * earlier template section present, else ahead of the first later one) and
 * anything else is appended. Either way nothing already written moves.
 *
 * A section this outline ALREADY carries is a stated refusal, never a second
 * copy: the affordance is offered from what the STORED fragment lacks while the
 * insert is computed against what the BUFFER currently holds, and those two
 * differ by exactly the human's unsaved work.
 *
 * EOL-BLIND. Input is read on any of the three line breaks and returned in LF;
 * the canvas re-applies the document's own flavor at the swap. That is the same
 * rule the buffer contract's proposal path had to learn — applying LF text
 * verbatim to a CRLF document turns one reviewed insertion into a whole-file
 * line-ending rewrite.
 */
export function insertSection(text, options = {}) {
  const title = String(options.title == null ? "" : options.title).trim();
  if (!title) return { ok: false, reason: "a section needs a heading" };
  const lines = String(text == null ? "" : text).split(/\r\n|\r|\n/);
  const source = lines.join("\n");
  // REFUSED, NEVER REPAIRED (review finding F4). Closing the fence for the human
  // would be rewriting a fragment nobody asked us to change, which is the one
  // thing task 3.3 forbids outright.
  if (endsInsideFence(source)) {
    return { ok: false,
             reason: "this fragment ends inside an unclosed code fence — close "
               + "it before adding sections, or every heading below it is "
               + "invisible to the outline" };
  }
  const sections = outlineSections(source);
  const required = options.required === true;
  const template = resolveTemplate(title, required);
  if (required && !template) {
    return { ok: false,
             reason: '"' + title + '" is not one of the three required sections' };
  }
  // The rank drives BOTH the canonical placement and (on the required route) the
  // duplicate rule — and it is read off the TEMPLATE's heading, never off the
  // caller's free text, so no coincidental substring can reach it.
  const rank = template ? sectionRank(template.heading) : null;
  const clash = sections.find((section) =>
    section.title.trim().toLowerCase() === title.toLowerCase()
    || (required && rank !== null && sectionRank(section.title) === rank));
  if (clash) {
    return { ok: false,
             reason: 'this outline already carries the section "' + clash.title + '"' };
  }

  let target = null;
  let mode = "end";
  const after = options.after ? String(options.after) : null;
  if (after) {
    target = sections.find((section) => section.title === after) || null;
    if (!target) {
      return { ok: false,
               reason: 'this outline carries no "' + after + '" section to add after' };
    }
    mode = "after";
  } else if (rank !== null) {
    for (const section of sections) {
      const at = sectionRank(section.title);
      if (at !== null && at < rank) { target = section; mode = "after"; }
    }
    if (!target) {
      target = sections.find((section) => {
        const at = sectionRank(section.title);
        return at !== null && at > rank;
      }) || null;
      if (target) mode = "before";
    }
  }

  let at = lines.length;
  if (mode === "after") at = sectionEnd(sections, target, lines.length);
  else if (mode === "before") at = target.line - 1;

  // Exactly one blank line on each side of the inserted block, whatever the
  // surrounding whitespace was: a heading pressed against the previous
  // paragraph is not markdown the fragment's other sections are written in.
  const head = lines.slice(0, at);
  const tail = lines.slice(at);
  while (head.length && head[head.length - 1].trim() === "") head.pop();
  while (tail.length && tail[0].trim() === "") tail.shift();
  const section = sectionSkeleton(title, options);
  const out = [...head];
  if (out.length) out.push("");
  out.push(...section.split("\n"));
  if (tail.length) out.push("", ...tail);
  else out.push("");

  return {
    ok: true,
    text: out.join("\n"),
    section,
    // The heading actually written, which is NOT always the label the caller
    // asked by: a required section is added under its canonical skeleton
    // heading, and a surface reporting the request instead of the result would
    // name a heading the file does not contain.
    heading: section.split("\n")[0].slice(3),
    // The addressing key the patch was scoped by, so the surface can SAY it.
    target: target ? target.title : null,
    mode,
  };
}
