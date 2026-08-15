// The staged-topic outline model (add-staged-topic-outline-template, task 3.1).
//
// PURE. No DOM, no fetch, no markdown rendering — it turns a primary fragment's
// TEXT into the sections the outline tab renders, so the tab can show a topic's
// structure instead of undifferentiated prose.
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
