"""A FAKE `omp --mode rpc` child, speaking the RECORDED frames and nothing else.

Used by `test_doxbench_bridge.py` so the bridge is exercised over a REAL pipe,
a real process boundary and real JSONL framing without the harness being
installed — it is not installed on this host, and no gate may require it
(add-doxbench-editing-phase-b §11's testing rule).

Every frame this script emits is one `verification-findings.md` recorded
hands-on:

  §3.6   `{"id":..,"type":"response","command":"prompt","success":true,
           "data":{"agentInvoked":false}}` + `{"type":"command_output","text":..}`
  §3.2   a full agent turn: response, `message_update` deltas, `agent_end`
  RPC note  `switch_session` -> `{"success":true,"data":{"cancelled":false}}`
            `set_model`      -> `{"success":true,"data":{"id":<modelId>}}`
  §3.5   `get_state`         -> `{"success":true,"data":{"sessionFile":<path>}}`

Behaviour is scripted from argv so one script covers every case a test needs:

  --session-file PATH   what `get_state` reports
  --reply TEXT          the assistant text a prompt answers with
  --die-after N         exit(9) once N commands have been handled
  --refuse-model        answer `set_model` with success:false
  --stderr TEXT         write TEXT to stderr at startup (the log-not-the-wire pin)
  --banner TEXT         write a NON-JSON line to stdout at startup

It is deliberately NOT importable from the package under test: a fake that
shared code with the thing it fakes would prove less.
"""

import argparse
import json
import sys


def emit(frame):
    sys.stdout.write(json.dumps(frame) + "\n")
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--session-file", default="")
    parser.add_argument("--reply", default="a grounded answer")
    parser.add_argument("--die-after", type=int, default=0)
    parser.add_argument("--refuse-model", action="store_true")
    parser.add_argument("--stderr", default="")
    parser.add_argument("--banner", default="")
    # The bridge's own launch flags. Accepted and IGNORED, so a spelling change
    # in the real launch config surfaces as an argparse failure here rather than
    # as a silently different child.
    parser.add_argument("--mode", default="rpc")
    parser.add_argument("--profile", default="")
    parser.add_argument("--session-dir", default="")
    parser.add_argument("--setting", action="append", default=[])
    args = parser.parse_args()

    if args.stderr:
        sys.stderr.write(args.stderr + "\n")
        sys.stderr.flush()
    if args.banner:
        sys.stdout.write(args.banner + "\n")
        sys.stdout.flush()

    handled = 0
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        frame = json.loads(line)
        handled += 1
        if args.die_after and handled >= args.die_after:
            sys.exit(9)
        kind = frame.get("type")
        request_id = frame.get("id")
        if kind == "get_state":
            emit({"id": request_id, "type": "response", "command": "get_state",
                  "success": True, "data": {"sessionFile": args.session_file}})
            continue
        if kind == "switch_session":
            emit({"id": request_id, "type": "response",
                  "command": "switch_session", "success": True,
                  "data": {"cancelled": False}})
            continue
        if kind == "set_model":
            emit({"id": request_id, "type": "response", "command": "set_model",
                  "success": not args.refuse_model,
                  "data": {"id": frame.get("modelId")}})
            continue
        if kind == "prompt":
            message = frame.get("message", "")
            if message.startswith("/shake"):
                # §3.6, verbatim: zero model calls, then a free-text summary.
                emit({"id": request_id, "type": "response",
                      "command": "prompt", "success": True,
                      "data": {"agentInvoked": False}})
                emit({"type": "command_output", "text": "Nothing to shake."})
                continue
            emit({"id": request_id, "type": "response", "command": "prompt",
                  "success": True, "data": {"agentInvoked": True}})
            emit({"type": "message_update", "text": args.reply})
            emit({"type": "agent_end", "data": {}})
            continue
        emit({"id": request_id, "type": "response", "command": str(kind),
              "success": False, "data": {}})


if __name__ == "__main__":
    main()
