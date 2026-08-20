"""A FAKE `omp --mode rpc` child, TRANSCRIBED FROM REAL CAPTURED FRAMES.

REBUILT after the adversarial review's P1-7. The previous version claimed
"every frame this script emits is one `verification-findings.md` recorded
hands-on" and three of them were INVENTED — a top-level `text` on
`message_update`, a `data.agentInvoked` on an agent prompt's response, and an
`agent_end` carrying `data`. All 36 bridge tests passed against a child that
does not exist, which is how P1-1/3/4/5 survived to review.

Every frame below is now transcribed from the ORIGINAL verification session's
raw captured stdout (`rpc-stdout-{2,3,5,6,7,8}.log`, real `omp` v17.3.7 against
a keyless local mock provider) and re-confirmed by a live run on 2026-08-19.
The shapes, in the order a real session emits them:

  startup   {"type":"ready","protocolVersion":1,"supportedProtocolVersions":[1,2],
             "maxFrameBytes":1048576,"maxReassembledFrameBytes":67108864}
            {"type":"extension_ui_request","id":…,"method":"setWidget",…}
            {"type":"available_commands_update","commands":[…]}
  get_state {"id":…,"type":"response","command":"get_state","success":true,
             "data":{…,"sessionFile":"…/<ts>_<uuid>.jsonl",…}}
  switch    {"id":…,"type":"response","command":"switch_session","success":true,
             "data":{"cancelled":false}}
  set_model {"id":…,"type":"response","command":"set_model","success":true,
             "data":{"id":"local-model","provider":"local-proxy",…}}
            …or, for a provider the harness does not know:
            {"id":…,…,"success":false,"error":"Model not found: <prov>/<model>"}
  /shake    {"type":"command_output","text":"Nothing to shake."}   <-- FIRST
            {"id":…,"type":"response","command":"prompt","success":true,
             "data":{"agentInvoked":false}}
  prompt    {"id":…,"type":"response","command":"prompt","success":true}
            ^^ NO `data` AT ALL. `rpc.md:104`: an omitted `agentInvoked` means
            the host must rely on SESSION EVENTS for completion.
            {"type":"agent_start"} {"type":"turn_start"}
            {"type":"message_start","message":{"role":"user",…}}
            {"type":"message_end","message":{"role":"user",…}}
            {"type":"message_start","message":{"role":"assistant",…}}
            {"type":"message_update","assistantMessageEvent":
               {"type":"text_start","contentIndex":0,"partial":{…}}}
            {"type":"message_update","assistantMessageEvent":
               {"type":"text_delta","contentIndex":0,"delta":"…","partial":{…}}}
            {"type":"message_update","assistantMessageEvent":
               {"type":"text_end","contentIndex":0,"content":"…","partial":{…}}}
            {"type":"message_end","message":{"role":"assistant",…}}
            {"type":"turn_end","message":{"role":"assistant",…},"toolResults":[]}
            {"type":"agent_end","messages":[…],"isTerminal":true}

THE ARGUMENT PARSER IS PART OF THE FIXTURE. The old one declared `--setting`
"so a spelling change surfaces as an argparse failure here" — and that is
exactly what hid P1-1, because the real binary has no such flag. This one
accepts ONLY flags `omp --help` (v17.3.7) really declares, so a launch line the
real binary would reject is rejected here too.

Scripted from argv so one script covers every case a test needs:

  --session-file PATH   what `get_state` reports (repeatable: one per start)
  --reply TEXT          the assistant text the agent turn streams
  --delta-chunks N      split the reply across N text_delta frames
  --die-after N         exit(9) once N commands have been handled
  --known-provider ID   the only provider `set_model` accepts (default local-proxy)
  --stderr TEXT         write TEXT to stderr at startup
  --banner TEXT         write a NON-JSON line to stdout at startup
  --no-ready            suppress the `ready` frame
"""

import argparse
import json
import sys
import uuid

# Verbatim from every captured transcript's first line.
READY_FRAME = {
    "type": "ready",
    "protocolVersion": 1,
    "supportedProtocolVersions": [1, 2],
    "maxFrameBytes": 1048576,
    "maxReassembledFrameBytes": 67108864,
}

# The unsolicited noise a real session emits around every command. A host that
# cannot ignore these cannot talk to omp at all.
NOISE_FRAMES = [
    {"type": "extension_ui_request", "id": "155ce02bb31ae9a4",
     "method": "setWidget", "widgetKey": "autoresearch"},
    {"type": "available_commands_update",
     "commands": [{"name": "security",
                   "description": "Plan, run, inspect, import, and compare "
                                  "OMP-native security scans"}]},
]

MODEL_DESCRIPTOR = {
    "id": "local-model",
    "name": "Local Mock Model",
    "api": "openai-completions",
    "provider": "local-proxy",
    "baseUrl": "http://127.0.0.1:8931/v1",
    "reasoning": False,
    "input": ["text"],
    "contextWindow": 32768,
    "maxTokens": 4096,
}


def emit(frame):
    sys.stdout.write(json.dumps(frame) + "\n")
    sys.stdout.flush()


def user_message(text):
    return {"role": "user", "content": [{"type": "text", "text": text}],
            "attribution": "user", "timestamp": 1787080386218}


def assistant_message(text):
    return {"role": "assistant", "content": [{"type": "text", "text": text}],
            "api": "openai-completions", "provider": "local-proxy",
            "model": "local-model",
            "usage": {"input": 0, "output": 0, "cacheRead": 0,
                      "cacheWrite": 0, "totalTokens": 0},
            "stopReason": "stop", "timestamp": 1787080386219}


def run_agent_turn(prompt_text, reply, chunks):
    """The real streaming shape, in the real order."""
    emit({"type": "agent_start"})
    emit({"type": "turn_start"})
    emit({"type": "message_start", "message": user_message(prompt_text)})
    emit({"type": "message_end", "message": user_message(prompt_text)})
    final = assistant_message(reply)
    emit({"type": "message_start", "message": final})
    emit({"type": "message_update",
          "assistantMessageEvent": {"type": "text_start", "contentIndex": 0,
                                    "partial": final}})
    size = max(1, -(-len(reply) // max(1, chunks))) if reply else 0
    pieces = [reply[i:i + size] for i in range(0, len(reply), size)] or [""]
    for piece in pieces:
        emit({"type": "message_update",
              "assistantMessageEvent": {"type": "text_delta", "contentIndex": 0,
                                        "delta": piece, "partial": final}})
    emit({"type": "message_update",
          "assistantMessageEvent": {"type": "text_end", "contentIndex": 0,
                                    "content": reply, "partial": final}})
    emit({"type": "message_end", "message": final})
    emit({"type": "turn_end", "message": final, "toolResults": []})
    emit({"type": "agent_end",
          "messages": [user_message(prompt_text), final],
          "isTerminal": True})


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--session-file", action="append", default=[])
    parser.add_argument("--reply", default="a grounded answer")
    parser.add_argument("--delta-chunks", type=int, default=1)
    parser.add_argument("--die-after", type=int, default=0)
    parser.add_argument("--known-provider", default="local-proxy")
    parser.add_argument("--current-model", default="local-model")
    parser.add_argument("--stderr", default="")
    parser.add_argument("--banner", default="")
    parser.add_argument("--no-ready", action="store_true")
    # THE REAL LAUNCH FLAGS, and ONLY the real ones (`omp --help`, v17.3.7).
    # `--config` is repeatable, exactly as the real binary declares it. There is
    # deliberately NO `--setting`: the real binary answers "unknown flag:
    # --setting" and so must this fixture.
    parser.add_argument("--mode", default="rpc")
    parser.add_argument("--profile", default="")
    parser.add_argument("--session-dir", default="")
    parser.add_argument("--config", action="append", default=[])
    args = parser.parse_args()

    if args.stderr:
        sys.stderr.write(args.stderr + "\n")
        sys.stderr.flush()
    if not args.no_ready:
        emit(READY_FRAME)
    if args.banner:
        sys.stdout.write(args.banner + "\n")
        sys.stdout.flush()
    for frame in NOISE_FRAMES:
        emit(frame)

    session_files = list(args.session_file)
    session_file = (session_files.pop(0) if session_files
                    else f"{args.session_dir or '.'}/2026-08-19T00-00-00-000Z_"
                         f"{uuid.uuid4()}.jsonl")

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
                  "success": True,
                  "data": {"model": dict(MODEL_DESCRIPTOR,
                                            id=args.current_model),
                           "sessionFile": session_file,
                           "sessionId": "01a01bf6-01ae-7000-a64c-83cb75fbdcdf",
                           "messageCount": 0, "isStreaming": False}})
            continue
        if kind == "switch_session":
            emit({"id": request_id, "type": "response",
                  "command": "switch_session", "success": True,
                  "data": {"cancelled": False}})
            continue
        if kind == "set_model":
            provider = frame.get("provider")
            # THE REAL REFUSAL SHAPE (P1-5, captured live): a provider the
            # harness does not know is "Model not found: <provider>/<modelId>",
            # NOT a generic failure. A governance data-handling label sent as a
            # provider id lands here every time.
            #
            # AND A MISSING PROVIDER IS REFUSED THE SAME WAY (re-verify N-1,
            # captured live): the harness stringifies the absent key, so a frame
            # with no `provider` answers
            # `Model not found: undefined/<modelId>`. This fixture used to
            # ACCEPT it — the P1-7 pattern recurring, and the reason the shipped
            # `provider_id=None` default looked fine in every hermetic test
            # while refusing every real turn.
            if provider is None:
                emit({"id": request_id, "type": "response",
                      "command": "set_model", "success": False,
                      "error": "Model not found: undefined/"
                               f"{frame.get('modelId')}"})
                continue
            if provider != args.known_provider:
                emit({"id": request_id, "type": "response",
                      "command": "set_model", "success": False,
                      "error": f"Model not found: {provider}/"
                               f"{frame.get('modelId')}"})
                continue
            emit({"id": request_id, "type": "response", "command": "set_model",
                  "success": True,
                  "data": dict(MODEL_DESCRIPTOR, id=frame.get("modelId"))})
            continue
        if kind == "prompt":
            message = frame.get("message", "")
            head = message.split()[0] if message.split() else ""
            if head in ("/shake", "/memory", "/mcp"):
                # A KNOWN builtin: the summary arrives BEFORE the response, and
                # the response DOES carry agentInvoked: false.
                emit({"type": "command_output", "text": "Nothing to shake."})
                emit({"id": request_id, "type": "response",
                      "command": "prompt", "success": True,
                      "data": {"agentInvoked": False}})
                continue
            # AN UNKNOWN SLASH COMMAND IS NOT AN ERROR IN THE HARNESS — it falls
            # straight through to a real model turn (re-verify N-2, captured
            # live: `/definitelynotacommand` -> agent_start -> 'MOCK_DONE'). The
            # fixture reproduces that, so a bridge that let one through would
            # fail a test rather than only production.
            # A REAL MODEL PROMPT: the response carries NO data at all, and the
            # turn is reported through session events (rpc.md:104).
            emit({"id": request_id, "type": "response", "command": "prompt",
                  "success": True})
            run_agent_turn(message, args.reply, args.delta_chunks)
            continue
        emit({"id": request_id, "type": "response", "command": str(kind),
              "success": False, "error": f"unknown command: {kind}"})


if __name__ == "__main__":
    main()
