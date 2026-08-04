// Human gate console bar (US9; D16/D17). The READ-ONLY web v1 surfaces the four
// gate affordances (demote / edit / ratify / kickoff) on a gate-bearing artifact
// and produces the ACTION DESCRIPTOR — the exact `cli.py gate ...` command a
// human runs against their pinned checkout. It NEVER executes a gate
// server-side: serve.py stays GET/HEAD read-only, and gate authority is
// human-only (a human running the CLI, whose `--actor` identity the record
// carries). This module is a pure descriptor builder plus a DOM-safe mount;
// every dynamic value is bound via textContent (never innerHTML), matching
// canvas.js's war-room DOM-safety posture.

export const GATE_ACTIONS = ["demote", "edit", "ratify", "kickoff"];

const LABELS = {
  demote: "⤺ reject → staging",
  edit: "✎ edit (redline)",
  ratify: "✓ approve / ratify",
  kickoff: "▶ kickoff next step",
};

const NOTES = {
  demote: "mechanized reverse transition — drafts return to the staging topic's openspec/ workspace",
  edit: "apply a HUMAN-approved redline; the AI drafting of redlines is a follow-on delta",
  ratify: "write the ratification record (ratifier, date) + register update",
  kickoff: "dispatch the ratified change's next step — refused without a recorded ratification",
};

const CLI = "python3 scripts/ideation_dashboard/cli.py";

// A change document is gate-bearing when it is one of the OpenSpec change
// documents (proposal / design / tasks / spec deltas) — purely from its path.
// Pure — unit-tested via node.
export function isGateBearing(path) {
  const p = String(path || "");
  const base = p.split("/").pop();
  return base === "proposal.md" || base === "design.md" || base === "tasks.md"
    || /(^|\/)specs\/.*\bspec\.md$/.test(p);
}

// Shell-quote one descriptor value so the emitted command is copy-pasteable
// VERBATIM — the promise these descriptors make, and the one they broke.
//
// POSIX SINGLE quotes, and EVERY interpolated value goes through here (PR #49
// review findings 15; the same discipline `q()` in staging-workbench-model.js
// carries, spelled locally because this module stays import-free so its pure
// helpers keep running standalone under node). Inside single quotes a POSIX
// shell expands NOTHING, so the only character needing care is `'` itself,
// closed and re-opened around an escaped literal (`'\''`).
//
// Wave 1 quoted the workbench's descriptors and left THIS emitter unquoted:
// `--change-id`, `--repository`, `--actor` and `--document` were interpolated
// bare, so a `$(…)` or backtick in a change id / repository / actor mutated the
// pasted command and a bare `;` split it into a second command the descriptor
// never showed. The values are snapshot- and corpus-derived (the change id and
// document path come from the served artifact, the repository from the snapshot
// identity), so the trust boundary crossed is "merged corpus content -> the
// human's shell in the served checkout".
//
// The `<...>` placeholders are quoted too. They are not decoration a shell can
// be trusted with: `<old>` unquoted is a REDIRECT, and `<why>` in double quotes
// is a redirect the moment the quotes are the outer ones. Quoting everything —
// placeholders, the literal `.` repo root, values already validated upstream —
// removes the standing question of which slots were safe.
//
// Quoting is not validation and does not pretend to be: the value reaches the
// CLI as ONE argument, and the CLI's own allowlist is what refuses it, inside
// the process, which is the layer that can refuse.
function q(value) {
  return "'" + String(value).split("'").join("'\\''") + "'";
}

// The exact CLI command for one action — copy-pasteable, with `<...>`
// placeholders a human fills. Pure — unit-tested via node.
export function gateCommand(action, ctx) {
  const c = ctx || {};
  const change = q(c.changeId || "<change-id>");
  const actor = q(c.actor || "<you>");
  const repo = q(c.repository || "<repo>");
  const id = `--repo-root ${q(".")} --actor ${actor} --change-id ${change}`;
  const snap = `--repository ${repo}`;
  switch (action) {
    case "demote":
      return `${CLI} gate demote ${id} ${snap} --reason ${q("<why>")} --execute`;
    case "ratify":
      return `${CLI} gate ratify ${id} --ratifier ${actor}`;
    case "edit":
      return `${CLI} gate edit-apply ${id} --document ${q(c.path || "<doc>")}`
        + ` --old-file ${q("<old>")} --new-file ${q("<new>")}`;
    case "kickoff":
      return `${CLI} gate kickoff ${id} ${snap}`;
    default:
      return null;
  }
}

// The full descriptor list for a gate-bearing artifact. Pure — unit-tested.
export function gateActionDescriptors(ctx) {
  return GATE_ACTIONS.map((action) => ({
    action,
    label: LABELS[action],
    note: NOTES[action],
    command: gateCommand(action, ctx),
  }));
}

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text; // textContent only — never innerHTML
  return node;
}

// Executing upgrade (add-ideation-intent-plane §3, local action center):
// when the caller supplies a capability verdict reporting `actions.gate`
// (loopback bind + real checkout + resolved actor), the RATIFY affordance
// executes through `POST /actions/gate/ratify` instead of only revealing
// the CLI command. demote / edit / kickoff stay descriptor-only this slice
// (multi-step plan/redline flows). Capabilities arrive via `opts.caps`
// (app.js owns the probe) — this module stays import-free so its pure
// helpers keep running standalone under node (the house test pattern).
export const GATE_RATIFY_ROUTE = "/actions/gate/ratify";

async function executeRatify(ctx, fetcher) {
  const doFetch = fetcher || fetch;
  const response = await doFetch(GATE_RATIFY_ROUTE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ change_id: ctx.changeId }),
  });
  try {
    return await response.json();
  } catch {
    return { ok: false, message: "malformed response (HTTP " + response.status + ")" };
  }
}

// Mounts the gate bar into `container` for the gate-bearing artifact described
// by `ctx` ({ changeId, path, repository, actor }). Each affordance reveals the
// exact CLI command (the action descriptor); ratify additionally EXECUTES when
// the local gate capability is live (`opts.caps` or a self-probe).
export function mountGateBar(container, ctx, opts) {
  // clear only — every dynamic value below is bound via textContent
  container.innerHTML = "";
  const bar = el("div", "gatebar");
  bar.appendChild(el("div", "gatebar-title", "human gate console — run the command in your pinned checkout"));
  const descriptors = gateActionDescriptors(ctx);
  const cmdLine = el("div", "gatebar-cmd docstatus");
  cmdLine.hidden = true;
  const actions = el("div", "gatebar-actions");
  const ratifyButtons = [];
  for (const d of descriptors) {
    const btn = el("button", "gatebtn", d.label);
    btn.type = "button";
    btn.title = d.note;
    btn.addEventListener("click", () => {
      cmdLine.hidden = false;
      cmdLine.textContent = d.note + "  —  " + d.command;
    });
    if (d.action === "ratify") ratifyButtons.push(btn);
    actions.appendChild(btn);
  }
  bar.appendChild(actions);
  bar.appendChild(cmdLine);
  container.appendChild(bar);

  // async executing upgrade — never blocks the descriptor render.
  const o = opts || {};
  const upgrade = (caps) => {
    if (!caps?.actions?.gate) return;
    for (const btn of ratifyButtons) {
      btn.classList.add("gatebtn-live");
      btn.title = "EXECUTES via the local gate route (actor: " + (caps.actor || "local") + ")";
      btn.addEventListener("click", async () => {
        cmdLine.hidden = false;
        cmdLine.textContent = "ratifying " + (ctx.changeId || "?") + "…";
        const result = await executeRatify(ctx, o.fetcher);
        cmdLine.textContent = result.ok
          ? "ratified " + result.change_id + " by " + result.ratifier + " (" + result.date + ") — record: " + result.record
          : "refused — " + (result.message || "gate action failed");
      });
    }
  };
  upgrade(o.caps || null);
  return { descriptors };
}
