// Human select-to-edit transport. The dashboard never writes document content:
// this action asks the guarded loopback console to launch the selected source
// file in the human's editor.

export const ACTIONS_EDIT_ROUTE = "/actions/edit";
const CONSOLE_TOKEN_HEADER = "X-XF-Console-Token";

export function editCapable(caps) {
  return Boolean(caps?.actions?.edit === true
    && typeof caps?.console_token === "string"
    && caps.console_token.length > 0);
}

async function postEdit(path, caps, key, fetcher) {
  const selected = typeof key === "function" ? key() : key;
  if (!selected?.repository || !selected?.ref) {
    throw new Error("the selected document has no editable source key");
  }
  const body = { path };
  if (selected?.repository) body.repository = selected.repository;
  if (selected?.ref) body.ref = selected.ref;
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      [CONSOLE_TOKEN_HEADER]: caps.console_token,
    },
    body: JSON.stringify(body),
  };
  const doFetch = fetcher || fetch;
  const response = await doFetch(ACTIONS_EDIT_ROUTE, options);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload?.message || payload?.error || ("HTTP " + response.status));
  }
  return payload;
}

export function createEditAction({ caps, key, fetcher } = {}) {
  const enabled = editCapable(caps);
  return {
    enabled,
    async open(path) {
      if (!enabled) throw new Error("select-to-edit is unavailable");
      return postEdit(path, caps, key, fetcher);
    },
  };
}
