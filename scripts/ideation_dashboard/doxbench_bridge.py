"""The LOCAL HARNESS BRIDGE: an adapter for the UNCHANGED three-member
`WorkbenchModelPort`, speaking the harness's stdio RPC to a child process
(add-doxbench-editing-phase-b tasks §11.1-§11.6; design §5, decision D14;
`verification-findings.md` §§3.1, 3.2, 3.3, 3.5, 3.6).

WHAT THIS IS, IN ONE SENTENCE: the only component in the tree that knows the
harness protocol, translating one already-assembled prompt envelope into
`set_model` + `prompt` frames on a local child's stdin and reading its answer
back off stdout.

**D14, LITERALLY.** `WorkbenchModelPort` still declares exactly three members
(`timeout_seconds`, `catalog()`, `dispatch(prompt_envelope)`), and everything
this slice needs that a fourth member would have carried lives INSIDE this
adapter instead:

* per-turn model choice — `set_model` before `prompt`, read off the envelope's
  own `model_id` (task 11.6);
* harness session switching — `switch_session`, one session per document
  thread (task 11.4);
* `/shake`-style offload — an ordinary `prompt` frame carrying slash text
  (compression layer three, `verification-findings.md` §3.6);
* `artifact://` dereferencing — the seam `doxbench_threads.dereference_bodies`
  asks for, which only this component can serve because only it can read the
  harness's own store (`verification-findings.md` §3.5).

**WHAT IT HOLDS: NO CREDENTIAL.** The child is started with an ALLOWLISTED
environment (`child_environment`), so nothing credential-shaped in the serve's
own environment can reach it, and this module reads no key, no token and no
config file of its own. An API-backed catalog entry's credential comes from the
ratified broker lane (`add-model-provider-broker`); the bridge is the wrong
place for one and is built so it cannot become the right one.

**LOOPBACK-LOCAL BY CONSTRUCTION.** There is no socket here at all: the
transport is the child's own stdin/stdout pipe, which no browser and no
non-loopback surface can address. Upstream has no HTTP mode
(`verification-findings.md`'s install notes), and this module adds none.

**THE SPLIT-BRAIN PROHIBITION IS AN INSTALL FACT, NOT A POLICY.** The launch
config pins `memory.backend: off` explicitly AND runs under a dedicated profile,
so a developer's personal interactive harness memory settings cannot bleed into
a bridge session (`verification-findings.md` §3.1's implementation consequence).
The sidecar is the record; `HarnessThreadMirror` below is told what the record
says and can neither answer with a turn nor amend one.

**FRESH SESSION PER THREAD** is what keeps the source-ranking hierarchy fixed
and correct: `SYSTEM.md` is read once at session start and every later rebuild
replays that same startup-captured string (`verification-findings.md` §3.3), so
a hierarchy that must not change mid-conversation is guaranteed by never reusing
a session across threads.

Pure standard library. Nothing here reaches a network, and every seam a test
needs — the spawn, the clock, the log sink — is injected.
"""

from __future__ import annotations

import contextlib
import dataclasses
import json
import os
import queue
import subprocess  # noqa: S404 - a local child process IS this module's subject
import sys
import threading
import time
from collections.abc import Callable, Iterable, Mapping, Sequence
from pathlib import Path

from ideation_dashboard import doxbench_mcp, doxbench_threads
from ideation_dashboard.doxbench_hash import utf8_size
from ideation_dashboard.doxbench_model import (
    EMPTY_CATALOG, ModelCatalog, validated_timeout_seconds,
)

# ---------------------------------------------------------------------------
# refusals
# ---------------------------------------------------------------------------


class BridgeError(ValueError):
    """Base class for every bridge-shaped refusal. Carries this module's own
    vocabulary only — never a child's stderr, never a provider's text."""


class BridgeUnavailable(BridgeError):
    """The harness child cannot be started, or died and could not be restarted
    inside the bounded retry. The ROUTE's honest model-unavailable posture is
    what a caller sees; see `OmpHarnessBridge.catalog` for the two legs."""


class BridgeProtocolError(BridgeError):
    """A frame the harness sent is not one this module can read. Deliberately
    NOT a crash and never a partial answer."""


class BridgeSessionConflict(BridgeError):
    """One harness session was about to serve two document threads. Refused:
    two threads sharing a session is one document's context leaking into
    another's (design §5.2)."""


# ---------------------------------------------------------------------------
# the launch configuration (tasks 11.1, 11.5; verification §3.1)
# ---------------------------------------------------------------------------

# The harness's package id. `oh-my-pi` is NOT the npm package of that name —
# the correct artifact is `can1357/oh-my-pi`, whose binary is `omp`
# (verification-findings.md's opening correction). Declared once.
HARNESS_COMMAND = "omp"

# `--mode rpc` is the transport this module speaks; there is no HTTP mode
# upstream. Verified hands-on end to end (verification §§3.2, 3.5, 3.6 and the
# closing RPC-mechanics note).
MODE_FLAG = "--mode"
MODE_RPC = "rpc"

# A DEDICATED profile, so the invoking engineer's own interactive harness
# settings — memory backend included — can never bleed into a bridge session
# (verification §3.1's implementation consequence, in as many words).
PROFILE_FLAG = "--profile"
BRIDGE_PROFILE = "doxbench-bridge"

# `--session-dir` is a verified CLI override ("Directory for session storage and
# lookup", verification §3.5). The bridge names its own so every session file
# and its sibling artifact directory land somewhere this process can find them.
SESSION_DIR_FLAG = "--session-dir"

# A session is a `<timestamp>_<sessionId>.jsonl` file and its artifact directory
# is that same path WITHOUT the suffix — a sibling directory, derived from the
# session file and from nothing else (verification §3.5).
SESSION_FILE_SUFFIX = ".jsonl"

# BELT AND BRACES over the shipped default. `memory.backend` is a real enum
# setting whose default is already `off` and whose `off` backend is a true no-op
# (verification §3.1), but "the operator never opted in" is not a guarantee, so
# the bridge states it.
#
# HOW IT IS STATED — CORRECTED 2026-08-19 after the adversarial review's P1-1.
# This module used to emit `--setting memory.backend=off`. There is no such flag:
# real `omp` v17.3.7 answers `Error: unknown flag: --setting` and exits, so the
# bridge could never start a harness at all. The REAL per-run mechanism, from
# `omp --help` and `docs/config-usage.md` §4, is a config OVERLAY:
#
#   --config=<value>   Load an extra config.yml-style overlay for this run
#                      (repeatable)
#
# and its precedence is
# `defaults <- global <- project <- PI_CONFIG_FILES <- --config <- runtime`,
# so an overlay overrides both the operator's global settings and the project's.
# That is a STRONGER pin than the profile's own settings file — which an
# operator can edit — and it writes nothing into anybody's home directory: the
# overlay lives in the bridge's own session root beside its other files.
#
# LIVE-VERIFIED 2026-08-19 against the surviving v17.3.7 install: with this
# overlay `/memory diagnose` answers "Memory backend is off — there is nothing
# to show.", and with `backend: local` in the same slot it answers something
# else. The pin is observable in the running harness, not merely declared.
CONFIG_FLAG = "--config"
OVERLAY_FILENAME = "doxbench-bridge-overlay.yml"
MEMORY_SECTION = "memory"
MEMORY_BACKEND_KEY = "backend"
MEMORY_BACKEND_SETTING = f"{MEMORY_SECTION}.{MEMORY_BACKEND_KEY}"
MEMORY_BACKEND_OFF = "off"

# The overlay document itself. A nested mapping, exactly as `docs/memory.md`
# spells it, and the value is QUOTED when rendered because bare `off` is a YAML
# 1.1 boolean and the setting is a string enum.
BRIDGE_OVERLAY: Mapping[str, Mapping[str, str]] = {
    MEMORY_SECTION: {MEMORY_BACKEND_KEY: MEMORY_BACKEND_OFF},
}


def render_overlay(document: Mapping[str, Mapping[str, str]]) -> str:
    """The overlay file's bytes: a two-level mapping of quoted scalars.

    Hand-rendered rather than dumped, because this module is stdlib-only and a
    YAML library is not stdlib. The shape is deliberately tiny — section, key,
    quoted string — so the renderer cannot drift into being a serializer."""

    lines = []
    for section, entries in document.items():
        lines.append(f"{section}:")
        for key, value in entries.items():
            escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'  {key}: "{escaped}"')
    return "\n".join(lines) + "\n"

# The ONLY environment variables a bridge child inherits. An ALLOWLIST rather
# than a denylist, because a denylist of credential-shaped names is a list
# somebody has to keep up with, and the one it misses is the one that leaks. A
# harness that genuinely needs another variable gains it HERE, visibly, in a
# diff a reviewer reads.
INHERITED_ENVIRONMENT: tuple[str, ...] = ("PATH", "HOME", "LANG", "LC_ALL", "TMPDIR")


@dataclasses.dataclass(frozen=True, slots=True)
class LaunchConfig:
    """Everything the bridge needs to start ONE harness child, as data.

    Data rather than code so a test can assert on the argv, the overlay and the
    environment without starting anything, and so an operator reading a launch
    line sees the same tuple this module builds.

    `provider_id` is the INSTALL-SIDE declaration of the harness provider the
    approved models are registered under (`local-proxy`, `anthropic`, …). It
    lives HERE and not on the catalog entry, and that placement is a recorded
    judgement call — see `OmpHarnessBridge._apply_model`."""

    session_dir: Path
    command: str = HARNESS_COMMAND
    profile: str = BRIDGE_PROFILE
    overlay: Mapping[str, Mapping[str, str]] = dataclasses.field(
        default_factory=lambda: BRIDGE_OVERLAY)
    provider_id: str | None = None
    extra_args: tuple[str, ...] = ()

    @property
    def overlay_path(self) -> Path:
        """Where the overlay this launch pins is written. Inside the bridge's
        own session directory, which is also the child's cwd — so pinning the
        harness's memory backend writes into no operator's home and no corpus."""
        return Path(self.session_dir) / OVERLAY_FILENAME

    def argv(self) -> tuple[str, ...]:
        args = [self.command, MODE_FLAG, MODE_RPC,
                PROFILE_FLAG, self.profile,
                SESSION_DIR_FLAG, str(self.session_dir)]
        if self.overlay:
            # `--config=<path>` rather than `--config <path>`: the flag's own
            # declared spelling in `omp --help`, and the form verified live.
            args.append(f"{CONFIG_FLAG}={self.overlay_path}")
        args.extend(self.extra_args)
        return tuple(args)

    def overlay_text(self) -> str:
        return render_overlay(self.overlay)

    def write_overlay(self) -> Path:
        """Materialise the overlay. Called before every child start, because a
        `--config` overlay is STRICT: a missing file is a hard startup error, so
        the file has to exist whenever the argv names it."""
        target = self.overlay_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.overlay_text(), encoding="utf-8")
        return target

    def environment(self, base: Mapping[str, str] | None = None) -> dict:
        return child_environment(os.environ if base is None else base)

    def declares_memory_off(self) -> bool:
        """The property task 11.5's sentence turns on, read from the thing that
        ACTUALLY carries the pin — the overlay document this launch writes and
        names on the command line — rather than from a flag list that never
        reached the harness."""
        section = self.overlay.get(MEMORY_SECTION) if self.overlay else None
        if not isinstance(section, Mapping):
            return False
        return section.get(MEMORY_BACKEND_KEY) == MEMORY_BACKEND_OFF


def child_environment(base: Mapping[str, str]) -> dict:
    """The harness child's whole environment: the allowlist, and nothing else.

    A credential-shaped variable in the serve's own environment therefore cannot
    reach the child even by accident, which is what "the bridge holds no secret"
    has to mean once the bridge is the thing that starts a process."""

    return {name: str(base[name]) for name in INHERITED_ENVIRONMENT
            if name in base and base[name] is not None}


# ---------------------------------------------------------------------------
# the RPC frames (verification §§3.2, 3.5, 3.6 and the RPC-mechanics note)
# ---------------------------------------------------------------------------

CMD_PROMPT = "prompt"
CMD_SWITCH_SESSION = "switch_session"
CMD_SET_MODEL = "set_model"
CMD_GET_STATE = "get_state"

FRAME_RESPONSE = "response"
FRAME_COMMAND_OUTPUT = "command_output"
FRAME_AGENT_END = "agent_end"
FRAME_MESSAGE_UPDATE = "message_update"
FRAME_TURN_END = "turn_end"
FRAME_MESSAGE_END = "message_end"

# The RECORDED shape of a slash command: there is no distinct RPC command type
# for `/shake`; it rides the same generic slash-command-over-`prompt` channel as
# every other builtin (verification §3.6, verbatim).
SHAKE_MODE_ELIDE = "elide"
SHAKE_MODE_IMAGES = "images"
SHAKE_MODES: tuple[str, ...] = (SHAKE_MODE_ELIDE, SHAKE_MODE_IMAGES)

# WHERE THE ASSISTANT'S TEXT ACTUALLY ARRIVES — CORRECTED 2026-08-19 after the
# adversarial review's P1-3, against the ORIGINAL verification session's raw
# captured stdout (`rpc-stdout-{5,6,7}.log`) and a live re-run.
#
# The previous reading looked for a flat `text`/`delta`/`content`/`message` at
# the frame's top level or under `data`. A real `message_update` has exactly
# three top-level keys — `type`, `assistantMessageEvent`, `message` — and the
# text is ONE LEVEL DOWN:
#
#   {"type":"message_update",
#    "assistantMessageEvent":{"type":"text_delta","contentIndex":0,
#                             "delta":"MOCK_DONE","partial":{…}},
#    "message":{"role":"assistant","content":[{"type":"text","text":"MOCK_DONE"}],…}}
#
# so no addition to a flat tuple of top-level names could ever have found it.
# The event carries the streaming piece under a type-dependent key; the sibling
# `message` (and `agent_end.messages`) carries the WHOLE assistant message in
# the content-part shape. Both readers live below, each in one place.
ASSISTANT_EVENT_KEY = "assistantMessageEvent"
EVENT_TYPE_TEXT_DELTA = "text_delta"
EVENT_TYPE_TEXT_END = "text_end"
# The key each event type carries its text under. A CLOSED table rather than a
# guess-list: an event type absent from it contributes nothing.
EVENT_TEXT_KEYS: Mapping[str, str] = {
    EVENT_TYPE_TEXT_DELTA: "delta",
    EVENT_TYPE_TEXT_END: "content",
}
MESSAGE_KEY = "message"
MESSAGES_KEY = "messages"
CONTENT_KEY = "content"
ROLE_ASSISTANT = "assistant"
CONTENT_TYPE_TEXT = "text"

# How the envelope's sections become one prompt message. The sections already
# carry their own headings (`CONTEXT PACKET —`, `EVIDENCE —`, `Human message:`),
# so the keys are NOT rendered: rendering them would spend bytes the packet's
# budget arithmetic does not charge for, and `doxbench_packet`'s scaffold reserve
# charges exactly this separator per section.
SECTION_SEPARATOR = "\n\n"


def render_prompt_message(prompt_envelope: object) -> str:
    """The one place a `PromptEnvelope` becomes harness prompt text.

    Duck-typed on `sections`, exactly as every other seam in this family is:
    the envelope type lives in `doxbench_turns`, importing it here would make
    the adapter depend on prompt assembly, and D14 puts prompt assembly on the
    other side of the port."""

    # ONE SPELLING WHERE THERE IS ONE TO USE (adversarial review P3-20).
    # `doxbench_turns.PromptEnvelope.rendered()` already joins the sections in
    # the declared order, and it is the authority on how a prompt renders — so
    # an envelope that HAS it answers with it, and this function's own join is
    # the fallback for a duck-typed envelope that does not. A companion test
    # asserts the two agree byte for byte, so the fallback cannot drift.
    rendered = getattr(prompt_envelope, "rendered", None)
    if callable(rendered):
        text = rendered()
        if isinstance(text, str) and text:
            return text
    sections = getattr(prompt_envelope, "sections", None)
    if not isinstance(sections, (tuple, list)) or not sections:
        raise BridgeProtocolError(
            "a prompt envelope carries its assembled sections; this one carries "
            "none, and a bridge does not compose a prompt of its own")
    texts = []
    for section in sections:
        text = getattr(section, "text", None)
        if not isinstance(text, str):
            raise BridgeProtocolError(
                "every prompt section carries its exact text")
        texts.append(text)
    return SECTION_SEPARATOR.join(texts)


@dataclasses.dataclass(frozen=True, slots=True)
class HarnessResponse:
    """One command's answer, plus the free-text and terminal frames that
    arrived before it settled."""

    command: str
    success: bool
    data: Mapping[str, object]
    command_output: tuple[str, ...] = ()
    assistant_text: str = ""
    agent_ended: bool = False
    error: str = ""

    @property
    def agent_invoked(self) -> bool | None:
        """TRI-STATE, and the third state is the whole point (P1-4).

        `rpc.md:104`: a `prompt` success response *may* include
        `data.agentInvoked`, and **omitted means the host must rely on session
        events for completion**. This used to read `bool(data.get(...,False))`,
        collapsing "omitted" into "the agent was not invoked" — the exact
        opposite of the documented meaning — so `dispatch` returned at the
        response frame, 1.97 s in, with an empty answer, while the model's real
        reply arrived ~20 s later and was never read.

        `None` means OMITTED: keep reading until the terminal `agent_end`."""

        if "agentInvoked" not in self.data:
            return None
        return bool(self.data.get("agentInvoked"))


@dataclasses.dataclass(frozen=True, slots=True)
class ShakeReport:
    """What layer-three compression can honestly report.

    `command_output` is FREE TEXT, not a structured payload: verification §3.6
    is explicit that no structured bytes-reclaimed field exists, so this type
    carries the summary for bookkeeping and claims no number of its own."""

    agent_invoked: bool
    summary: str


# ---------------------------------------------------------------------------
# the supervised child (task 11.3)
# ---------------------------------------------------------------------------

# The bounded retry. Two, not "until it works": an unstartable harness is a
# posture the route already renders honestly, and an unbounded restart loop
# turns one bad turn into a serve that spends its life respawning.
MAX_RESTARTS = 2

# What a single frame may be. THE REAL v1 CAP, read off the `ready` frame every
# captured transcript opens with (`"maxFrameBytes": 1048576`) — the 4 MiB this
# module used to declare was both invented and dead, since a v1 harness never
# sends a physical frame past 1 MiB.
#
# It is enforced by a BOUNDED READ rather than a post-hoc length check
# (adversarial review P3-16): `readline(limit)` returns at most `limit` bytes,
# so an unbounded line with no newline can no longer be materialised in full
# before the guard runs.
MAX_FRAME_BYTES = 1024 * 1024

# How long a settled command waits for the free-text frame that follows it.
# `/shake` answers with its response FIRST and its `command_output` summary
# after (verification §3.6's captured stdout, in that order), so a reader that
# stopped at the response would drop the only thing the command reports. Small
# and bounded: the summary is bookkeeping, and a harness that never sends one
# must not hold a turn open for it.
TRAILING_FRAME_GRACE_SECONDS = 0.25

# The largest `artifact://` payload the bridge inlines into a sidecar. Past it
# the sidecar records the FACT of the elision, which is verification §3.5's own
# second remedy and is a record a reader can act on.
MAX_INLINE_ARTIFACT_BYTES = 256 * 1024


def _default_log(line: str) -> None:
    """The serve's own log, by default its stderr. NEVER the wire: this module
    hands child stderr to this sink and to nothing else."""
    print(f"[doxbench-bridge] {line}", file=sys.stderr)


class HarnessChild:
    """One live `omp --mode rpc` process, its reader threads, and its frame
    queue. Supervision (restart, bounded retry) belongs to the bridge above."""

    def __init__(self, launch: LaunchConfig, *, spawn=None, log=None,
                 environment: Mapping[str, str] | None = None) -> None:
        self.launch = launch
        self._spawn = spawn if spawn is not None else _spawn_child
        self._log = log if log is not None else _default_log
        self._environment = (dict(environment) if environment is not None
                             else launch.environment())
        self._process = None
        self._frames: "queue.Queue" = queue.Queue()
        self._readers: list[threading.Thread] = []
        self._next_id = 0

    # -- lifecycle ---------------------------------------------------------

    def start(self) -> None:
        if self._process is not None:
            return
        try:
            process = self._spawn(self.launch.argv(), self._environment,
                                  self.launch.session_dir)
        except BaseException as error:  # noqa: BLE001 - every start failure is one posture
            raise BridgeUnavailable(
                "the harness child could not be started; its details stay in "
                "this process") from error
        if process is None or getattr(process, "stdin", None) is None \
                or getattr(process, "stdout", None) is None:
            raise BridgeUnavailable(
                "the harness child was started without the stdio pipes this "
                "transport is")
        self._process = process
        self._readers = [
            self._reader(process.stdout, self._on_stdout, "stdout"),
        ]
        if getattr(process, "stderr", None) is not None:
            self._readers.append(
                self._reader(process.stderr, self._on_stderr, "stderr"))

    def _reader(self, stream, handler, name: str) -> threading.Thread:
        def _run():
            try:
                for raw in _bounded_lines(stream):
                    handler(raw)
            except (OSError, ValueError):
                # A closed pipe ends a reader, and that is the ordinary way a
                # reader ends. NARROW deliberately: a `BaseException` clause
                # here would swallow the suite's own hermeticity guard, which
                # is a `BaseException` precisely so no handler can disable it.
                return
        thread = threading.Thread(
            target=_run, daemon=True,
            name=f"doxbench-bridge-{name}")
        thread.start()
        return thread

    def _on_stdout(self, raw) -> None:
        line = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else str(raw)
        line = line.strip()
        if not line:
            return
        if utf8_size(line) > MAX_FRAME_BYTES:
            # A terminated line that is still over the cap. The unterminated
            # case never reaches here — `_bounded_lines` drops it while reading.
            self._log("dropping an oversize frame from the harness child")
            return
        try:
            frame = json.loads(line)
        except ValueError:
            # Not every stdout line is a frame; a harness banner is not a
            # protocol error and must not kill the turn.
            self._log("ignoring a non-JSON line on the harness child's stdout")
            return
        if isinstance(frame, dict):
            self._frames.put(frame)

    def _on_stderr(self, raw) -> None:
        """STDERR GOES TO THE SERVE'S LOG AND NOWHERE ELSE (task 11.3). It is
        never queued, never returned, and never reachable from a response."""
        line = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else str(raw)
        line = line.rstrip("\n")
        if line:
            self._log(line)

    @property
    def alive(self) -> bool:
        process = self._process
        if process is None:
            return False
        poll = getattr(process, "poll", None)
        return callable(poll) and poll() is None

    def stop(self) -> None:
        process, self._process = self._process, None
        self._readers = []
        if process is None:
            return
        for closer in ("stdin", "stdout", "stderr"):
            stream = getattr(process, closer, None)
            if stream is not None:
                try:
                    stream.close()
                except (OSError, ValueError):    # an already-closed pipe
                    pass
        for verb in ("terminate", "kill"):
            action = getattr(process, verb, None)
            if callable(action):
                try:
                    action()
                except OSError:                  # a dead child is already stopped
                    pass
                break

    # -- the wire ----------------------------------------------------------

    def next_id(self, prefix: str) -> str:
        self._next_id += 1
        return f"{prefix}{self._next_id}"

    def request(self, frame: dict, *, deadline: float,
                clock: Callable[[], float]) -> HarnessResponse:  # noqa: D401
        """Write one command frame and read until ITS response settles.

        Frames for other ids are DROPPED rather than buffered: this transport
        carries one in-flight command at a time by construction (the adapter
        holds the child while a turn runs), so a foreign id is a harness that
        is not answering the question asked."""

        process = self._process
        if process is None or not self.alive:
            raise BridgeUnavailable("the harness child is not running")
        request_id = frame["id"]
        payload = (json.dumps(frame, ensure_ascii=False) + "\n").encode("utf-8")
        try:
            process.stdin.write(payload)
            process.stdin.flush()
        except BaseException as error:  # noqa: BLE001 - a broken pipe is a dead child
            raise BridgeUnavailable(
                "the harness child's stdin closed mid-command") from error
        # ONLY A PROMPT HAS A TURN. `agentInvoked`'s omitted-means-await-events
        # rule is a property of `prompt` success responses and of nothing else:
        # `set_model`, `switch_session` and `get_state` never emit `agent_end`,
        # so awaiting one after them hangs until the deadline. Caught by the
        # LIVE run — the `set_model` response arrived at 1.03 s and the reader
        # sat on it for the full 45 s deadline. Read off the REQUEST's own type
        # rather than the response's `command`, so a harness that mislabels a
        # response cannot make this hang either.
        return self._await_response(
            request_id, deadline=deadline, clock=clock,
            awaits_turn=frame.get("type") == CMD_PROMPT)

    def _await_response(self, request_id: str, *, deadline: float,
                        clock: Callable[[], float],
                        awaits_turn: bool = False) -> HarnessResponse:
        outputs: list[str] = []
        assistant: list[str] = []
        ended = False
        final_messages: object = None
        last_message: object = None
        settled: HarnessResponse | None = None
        while True:
            remaining = deadline - clock()
            if remaining <= 0:
                raise BridgeUnavailable(
                    "the harness child did not answer inside the declared "
                    "deadline")
            try:
                frame = self._frames.get(timeout=min(remaining, 0.5))
            except queue.Empty:
                if not self.alive:
                    raise BridgeUnavailable(
                        "the harness child exited before answering")
                continue
            kind = frame.get("type")
            if kind == FRAME_COMMAND_OUTPUT:
                text = frame.get("text")
                if isinstance(text, str):
                    outputs.append(text)
                continue
            if kind == FRAME_MESSAGE_UPDATE:
                # ONLY the streaming deltas accumulate. `text_end` repeats the
                # whole run it closes, so accumulating it too would double every
                # answer a harness streams.
                event = frame.get(ASSISTANT_EVENT_KEY)
                if isinstance(event, Mapping) \
                        and event.get("type") == EVENT_TYPE_TEXT_DELTA:
                    assistant.append(_assistant_text_of(frame))
                continue
            if kind == FRAME_AGENT_END:
                ended = True
                # The terminal frame carries the WHOLE message list
                # (`agent_end.messages`), which is the harness's own final
                # state rather than a reassembly of deltas.
                final_messages = frame.get(MESSAGES_KEY)
                if settled is not None:
                    break
                continue
            if kind in (FRAME_TURN_END, FRAME_MESSAGE_END):
                # A single-turn fallback for the same fact: these carry the one
                # finished `message`. Read but never preferred over `agent_end`.
                carried = frame.get(MESSAGE_KEY)
                if isinstance(carried, Mapping) \
                        and carried.get("role") == ROLE_ASSISTANT:
                    last_message = carried
                continue
            if kind != FRAME_RESPONSE:
                continue
            if frame.get("id") != request_id:
                continue
            data = frame.get("data")
            error = frame.get("error")
            settled = HarnessResponse(
                command=str(frame.get("command", "")),
                success=bool(frame.get("success", False)),
                data=data if isinstance(data, Mapping) else {},
                command_output=tuple(outputs),
                assistant_text="".join(assistant),
                agent_ended=ended,
                error=error if isinstance(error, str) else "")
            # WHEN A COMMAND IS DONE (P1-4, corrected against the real
            # protocol):
            #
            #  * a FAILED command is done at its response — there is no turn;
            #  * `agentInvoked: false` (a builtin slash command like `/shake`)
            #    is done at its response, plus a bounded drain for the
            #    free-text summary that may trail it;
            #  * `agentInvoked` OMITTED — which is what a real model prompt's
            #    response looks like — means the turn is RUNNING and completion
            #    is reported through session events, so keep reading to the
            #    terminal `agent_end`;
            #  * `agentInvoked: true` is the same: keep reading.
            invoked = settled.agent_invoked
            if not awaits_turn or not settled.success or invoked is False:
                if awaits_turn and invoked is False:
                    self._drain_trailing(outputs, assistant, deadline=deadline,
                                         clock=clock)
                break
            if ended:
                break
        return dataclasses.replace(
            settled, command_output=tuple(outputs),
            assistant_text=self._answer(assistant, final_messages,
                                        last_message),
            agent_ended=ended)

    @staticmethod
    def _answer(deltas: list, final_messages: object,
                last_message: object) -> str:
        """The turn's answer, from the most authoritative source available.

        Order, and why: the terminal frame's own message list first (the
        harness's final state, complete even when the turn took several steps),
        then the single finished assistant message a `turn_end`/`message_end`
        carried, then the accumulated `text_delta` pieces. The deltas are last
        rather than first because a reassembly can lose a piece the harness
        never re-sent; they are kept because a harness that streams without a
        terminal message list is still legible."""

        return (final_assistant_text(final_messages)
                or _text_of_message(last_message)
                or "".join(deltas))

    def _drain_trailing(self, outputs: list, assistant: list, *,
                        deadline: float, clock: Callable[[], float]) -> None:
        """Collect the free-text frames a settled, agent-free command emits
        AFTER its response (verification §3.6). Bounded by the grace and by the
        turn's own deadline, and it stops at the first summary."""

        end = min(deadline, clock() + TRAILING_FRAME_GRACE_SECONDS)
        while clock() < end:
            try:
                frame = self._frames.get(timeout=max(0.0, min(0.05, end - clock())))
            except queue.Empty:
                continue
            kind = frame.get("type")
            if kind == FRAME_COMMAND_OUTPUT:
                text = frame.get("text")
                if isinstance(text, str):
                    outputs.append(text)
                return
            if kind == FRAME_MESSAGE_UPDATE:
                event = frame.get(ASSISTANT_EVENT_KEY)
                if isinstance(event, Mapping) \
                        and event.get("type") == EVENT_TYPE_TEXT_DELTA:
                    assistant.append(_assistant_text_of(frame))


def _assistant_text_of(frame: Mapping[str, object]) -> str:
    """The STREAMING piece one `message_update` carries, or "".

    Reads `assistantMessageEvent` and the closed `EVENT_TEXT_KEYS` table, so a
    `text_start` (no text), a `toolcall_start` (a tool call, not prose) and any
    event type this table does not name contribute nothing rather than
    contributing a guess. `text_end` is deliberately NOT accumulated by the
    caller — it repeats the whole run — but it is readable here so a harness that
    emits only `text_end` is still legible."""

    event = frame.get(ASSISTANT_EVENT_KEY)
    if not isinstance(event, Mapping):
        return ""
    key = EVENT_TEXT_KEYS.get(str(event.get("type")))
    if key is None:
        return ""
    value = event.get(key)
    return value if isinstance(value, str) else ""


def _text_of_message(message: object) -> str:
    """Every text part of ONE assistant message, joined. The content is a LIST
    of typed parts; a tool-call part carries no prose and is skipped."""

    if not isinstance(message, Mapping):
        return ""
    parts = message.get(CONTENT_KEY)
    if not isinstance(parts, (list, tuple)):
        return ""
    texts = []
    for part in parts:
        if not isinstance(part, Mapping) or part.get("type") != CONTENT_TYPE_TEXT:
            continue
        value = part.get(CONTENT_TYPE_TEXT)
        if isinstance(value, str):
            texts.append(value)
    return "".join(texts)


def final_assistant_text(messages: object) -> str:
    """The answer, read from a terminal frame's whole message list.

    THE LAST assistant message that carries any prose — not simply the last
    message, because a turn can end on a tool result, and not the first, because
    a multi-step turn's earlier assistant messages are working, not the answer.
    This is preferred over the accumulated deltas when a terminal frame provides
    it: it is the harness's own final state rather than a reassembly."""

    if not isinstance(messages, (list, tuple)):
        return ""
    for message in reversed(list(messages)):
        if not isinstance(message, Mapping):
            continue
        if message.get("role") != ROLE_ASSISTANT:
            continue
        text = _text_of_message(message)
        if text:
            return text
    return ""


def _bounded_lines(stream):
    """Yield complete lines, never reading more than `MAX_FRAME_BYTES` at once.

    A line longer than the cap is DROPPED — its head and every continuation —
    rather than assembled, so a harness that emits an unbounded run of bytes
    with no newline cannot spend the serve's memory. `readline(size)` is the
    stdlib primitive that makes this cheap: it returns at most `size` bytes and
    a short read without a trailing newline is exactly the over-long case."""

    limit = MAX_FRAME_BYTES + 1
    dropping = False
    while True:
        chunk = stream.readline(limit)
        if not chunk:
            return
        terminated = chunk.endswith(b"\n") if isinstance(chunk, bytes) \
            else chunk.endswith("\n")
        if dropping:
            dropping = not terminated
            continue
        if not terminated and len(chunk) >= MAX_FRAME_BYTES:
            dropping = True
            continue
        yield chunk


def _spawn_child(argv: Sequence[str], environment: Mapping[str, str],
                 cwd: Path):
    """The real spawn. Injected everywhere else so no test needs the harness
    installed — and no gate may require it, because it is not.

    THE CHILD'S CWD IS THE BRIDGE'S OWN SESSION DIRECTORY, never a git worktree
    or the served checkout. Two things follow, both deliberate: the harness's
    project-scoped `.omp/mcp.json` discovery (verification §3.2) finds the
    registration the bridge wrote there and nothing else, and a harness tool
    that reaches for the filesystem lands in a scratch directory rather than in
    the corpus. Grounding comes from the packet, which is assembled and bounded
    before this process exists."""

    return subprocess.Popen(  # noqa: S603 - argv is built from declared constants
        list(argv), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, env=dict(environment), cwd=str(cwd),
        close_fds=True)


# ---------------------------------------------------------------------------
# the adapter (tasks 11.1-11.6)
# ---------------------------------------------------------------------------


class OmpHarnessBridge:
    """The `WorkbenchModelPort` adapter over a supervised harness child.

    Three PORT members, and every other public name here is adapter surface the
    route reaches directly rather than through the seam: `select_thread`,
    `shake`, `dereference`, `mirror`. None of them is a second provider verb,
    which is what `FORBIDDEN_PORT_MEMBERS` protects and what a companion test
    asserts against this class's own public surface as well as the protocol's.
    """

    def __init__(self, catalog: ModelCatalog = EMPTY_CATALOG, *,
                 session_root: Path | str,
                 timeout_seconds: float = 60.0,
                 launch: LaunchConfig | None = None,
                 spawn=None, log=None,
                 clock: Callable[[], float] = time.monotonic,
                 environment: Mapping[str, str] | None = None,
                 max_restarts: int = MAX_RESTARTS) -> None:
        if not isinstance(catalog, ModelCatalog):
            raise TypeError(
                f"catalog must be a ModelCatalog, got {type(catalog).__name__}")
        self._declared_catalog = catalog
        self._timeout_seconds = validated_timeout_seconds(timeout_seconds)
        self._session_root = Path(session_root)
        self._launch = launch or LaunchConfig(session_dir=self._session_root)
        self._spawn = spawn
        self._log = log if log is not None else _default_log
        self._clock = clock
        self._environment = environment
        self._max_restarts = max(0, int(max_restarts))
        self._child: HarnessChild | None = None
        self._sessions: dict[str, str] = {}
        self._selected: str | None = None
        self._unavailable = False
        self._lock = threading.RLock()

    # -- PORT MEMBER 1 -----------------------------------------------------

    @property
    def timeout_seconds(self) -> float:
        return self._timeout_seconds

    # -- PORT MEMBER 2 -----------------------------------------------------

    @property
    def _known_dead(self) -> bool:
        """A child that WAS started and is no longer alive.

        THE OTHER HALF OF LEG 1 (adversarial review P2-8). `_unavailable` used
        to be set only where `Popen` itself raised or the bounded retry was
        spent — so the commonest real failure, a child that spawns and then
        exits (which is exactly what the `--setting` defect produced), left the
        catalog advertising the model as available forever and pushed every
        later turn onto leg 2. Liveness is consulted here so leg 1 engages for
        the failure class it was written for."""

        child = self._child
        return child is not None and not child.alive

    def catalog(self) -> ModelCatalog:
        """The DECLARED catalog, with every entry marked unavailable once the
        bridge is known dead or unstartable (task 11.3).

        THIS IS THE FIRST OF THE TWO LEGS the route's honest model-unavailable
        posture stands on, and it is the one that keeps the gate ORDER
        unchanged: an unavailable entry fails `selectable_entry_for` at the
        route's existing step 7, which refuses with the existing fixed code
        BEFORE any packet is assembled and before any dispatch. The second leg
        is a child that dies mid-turn, which `dispatch` reports by raising —
        mapped by `doxbench_model.dispatch_turn` to its fixed, redacted
        `model_failed`, the route's existing shape for an adapter that failed.

        It never STARTS the child: the bridge starts on demand at the first turn
        that needs it (task 11.3), and an editor-only session must not spawn a
        model process it never uses. So before the first turn the declaration
        stands as written; after a failure it does not."""

        if not (self._unavailable or self._known_dead):
            return self._declared_catalog
        return ModelCatalog.from_entries(
            dataclasses.replace(entry, available=False)
            for entry in self._declared_catalog.entries)

    # -- PORT MEMBER 3 -----------------------------------------------------

    def dispatch(self, prompt_envelope: object) -> object:
        """One turn: ensure the child, `set_model`, then `prompt`.

        Task 11.6, in three lines and no fourth port member: the model this turn
        wants is the `model_id` the envelope already carries, and it is applied
        INSIDE this method, immediately before the prompt frame, which is the
        recorded ordering (`switch_session` → `set_model` → `prompt`, verified
        hands-on in the RPC-mechanics note).

        Returns the shape `doxbench_model.dispatch_turn` validates — prose plus
        an empty proposal list. Typed proposals are the route's injected
        validator's business, not this adapter's: an adapter that parsed
        proposals would be doing response validation behind the seam."""

        with self._lock, self._marking_unavailable_on_death():
            child = self._ensure_child()
            deadline = self._clock() + self._timeout_seconds
            model_id = getattr(prompt_envelope, "model_id", None)
            if isinstance(model_id, str) and model_id:
                self._apply_model(child, model_id, deadline=deadline)
            message = render_prompt_message(prompt_envelope)
            answer = child.request(
                {"id": child.next_id("p"), "type": CMD_PROMPT,
                 "message": message},
                deadline=deadline, clock=self._clock)
            if not answer.success:
                raise BridgeProtocolError(
                    "the harness refused this prompt; its own text stays in "
                    "this process")
            return {"assistant_prose": answer.assistant_text, "proposals": []}

    # -- adapter surface (NOT port members) --------------------------------

    def select_thread(self, thread_key: str) -> str | None:
        """Bind the harness to ONE document thread's session (task 11.4).

        Rules, all from design §5.2:

        * one harness session per document thread, and one session NEVER serves
          two threads — a second thread claiming a bound session is refused
          rather than resolved;
        * switching the selected document switches the harness session, through
          the recorded `switch_session` frame carrying the session path
          `get_state` reported when that thread's session was created;
        * a thread with no session yet gets a FRESH one.

        THE ONE HONEST CONSEQUENCE, stated where it bites: the recorded RPC
        surface has no in-session "start another session" command. It has
        `switch_session` (verified) and it has process start with
        `--session-dir` (verified). So a thread that has never been seen gets
        its fresh session by RESTARTING the child under this bridge's own
        session directory and recording the `get_state.sessionFile` the new
        process reports. That is a real cost — one process start per new thread
        in a serve — and it is the option that keeps every frame inside the
        verified set instead of inventing one.

        Returns the session path now bound to this thread, or `None` where the
        harness reported no session file."""

        with self._lock, self._marking_unavailable_on_death():
            if self._selected == thread_key:
                return self._sessions.get(thread_key)
            child = self._ensure_child()
            deadline = self._clock() + self._timeout_seconds
            recorded = self._sessions.get(thread_key)
            if recorded is not None:
                answer = child.request(
                    {"id": child.next_id("sw"), "type": CMD_SWITCH_SESSION,
                     "sessionPath": recorded},
                    deadline=deadline, clock=self._clock)
                if not answer.success:
                    raise BridgeProtocolError(
                        "the harness refused to switch to this thread's own "
                        "session")
                self._selected = thread_key
                return recorded
            # A FRESH session for a thread nothing has opened one for.
            if self._selected is not None:
                self._restart_child()
                child = self._ensure_child()
                deadline = self._clock() + self._timeout_seconds
            path = self._session_path(child, deadline=deadline)
            if path is not None:
                owner = next((key for key, value in self._sessions.items()
                              if value == path), None)
                if owner is not None and owner != thread_key:
                    raise BridgeSessionConflict(
                        "this harness session already serves another document "
                        "thread; one session never serves two threads, because "
                        "that is one document's context leaking into another's")
                self._sessions[thread_key] = path
            self._selected = thread_key
            return path

    def register_knowledge_mount(self, manifest) -> tuple[Path, Path]:
        """Register the knowledge service's stdio MCP server for this tile,
        BEFORE the first turn of a thread that needs it (verification §3.2's
        realization note).

        Written into this bridge's own session root, which is the child's cwd —
        so the harness's project-scoped `.omp/mcp.json` discovery finds it and
        nothing in the corpus is touched.

        WHAT REGISTRATION-BEFORE-FIRST-TURN BUYS, AND WHAT IT DOES NOT. MCP
        discovery is documented as asynchronous, and a turn issued before it
        completes simply does not see the tool that turn — degrading to design
        §3.4's "no knowledge service" reduced-packet posture, which is the
        correct fallback already specified. A registration written while a child
        is already running therefore applies FROM THE NEXT CHILD, and this
        method says so by returning the paths rather than pretending to have
        waited for a discovery event nobody specified."""

        with self._lock:
            self._session_root.mkdir(parents=True, exist_ok=True)
            return doxbench_mcp.write_registration(self._session_root, manifest)

    def shake(self, mode: str = SHAKE_MODE_ELIDE) -> ShakeReport:
        """Compression LAYER THREE: mechanical, reversible offload at the model
        boundary, invoked exactly as verification §3.6 recorded it.

        `/shake` has no RPC command type of its own — it rides the generic
        slash-command-over-`prompt` channel — and it answers with
        `agentInvoked: false` plus a FREE-TEXT `command_output` frame. There is
        no structured bytes-reclaimed field, so this returns the summary for
        bookkeeping and asserts no number."""

        if mode not in SHAKE_MODES:
            raise BridgeError(
                f"{mode!r} is not a shake mode this bridge invokes; the "
                f"recorded modes are {SHAKE_MODES}")
        with self._lock, self._marking_unavailable_on_death():
            child = self._ensure_child()
            deadline = self._clock() + self._timeout_seconds
            answer = child.request(
                {"id": child.next_id("sh"), "type": CMD_PROMPT,
                 "message": f"/shake {mode}"},
                deadline=deadline, clock=self._clock)
            return ShakeReport(agent_invoked=answer.agent_invoked,
                               summary="\n".join(answer.command_output))

    def dereference(self, value: str) -> str:
        """The seam `doxbench_threads.dereference_bodies` asks for (§3.5).

        A harness `artifact://` reference resolves only inside the originating
        session's own home-relative store, which rides no branch — so a
        colleague who fetches the shared branch could never resolve one. This
        resolves the content THROUGH the harness's own store, which only this
        component can read, and where inlining is infeasible returns
        `elided_note(...)` instead: the FACT of the elision is a record a reader
        can act on, and a pointer they cannot follow is not.

        A half-resolving implementation cannot slip a survivor through, because
        the answer goes straight back into `ThreadTurn`'s absolute refusal."""

        if not isinstance(value, str):
            raise BridgeError("a dereference seam resolves text")
        if doxbench_threads.HARNESS_ARTIFACT_SCHEME not in value:
            return value
        resolved: list[str] = []
        for token in _split_artifact_tokens(value):
            if not token.startswith(doxbench_threads.HARNESS_ARTIFACT_SCHEME):
                resolved.append(token)
                continue
            resolved.append(self._resolve_artifact(token))
        return "".join(resolved)

    @property
    def launch(self) -> LaunchConfig:
        """The launch configuration this bridge starts children with. Public
        so the mirror can re-assert the memory pin without reaching inside."""
        return self._launch

    def mirror(self) -> "HarnessThreadMirror":
        """The `ThreadMirror` this bridge supplies to `mirror_turn`."""
        return HarnessThreadMirror(self)

    def stop(self) -> None:
        with self._lock:
            if self._child is not None:
                self._child.stop()
            self._child = None
            self._selected = None

    # -- supervision -------------------------------------------------------

    @property
    def started(self) -> bool:
        """Whether a child has been started at all. The task-11.3 negative — an
        editor-only session must not spawn a model process it never uses — is
        asserted against this."""
        return self._child is not None

    @property
    def available(self) -> bool:
        return not self._unavailable

    @contextlib.contextmanager
    def _marking_unavailable_on_death(self):
        """Every public entry point runs inside this, so leg 1 of the
        model-unavailable posture engages the moment a child dies — not only
        when a spawn raises (adversarial review P2-8)."""

        try:
            yield
        except BridgeUnavailable:
            self._unavailable = True
            raise

    def _ensure_child(self) -> HarnessChild:
        attempts = 0
        while True:
            child = self._child
            if child is not None and child.alive:
                self._unavailable = False
                return child
            if attempts > self._max_restarts:
                self._unavailable = True
                raise BridgeUnavailable(
                    "the harness bridge could not be started inside its bounded "
                    "retry; the model is unavailable for this turn")
            attempts += 1
            try:
                self._restart_child()
            except BridgeUnavailable:
                # BOUNDED, not unbounded: a start that fails is retried until
                # the bound is spent and then reported as the honest
                # model-unavailable posture. The alternative — reporting the
                # first failure — makes `max_restarts` a number nothing reads.
                if attempts > self._max_restarts:
                    raise
                continue

    def _restart_child(self) -> None:
        if self._child is not None:
            self._child.stop()
            self._child = None
            # THE RECORDED SESSION PATHS SURVIVE, and deliberately: a session
            # FILE lives under this bridge's own `--session-dir` and outlives
            # the process that opened it, and re-attaching a second process to
            # one by path is exactly what `switch_session` was verified doing
            # (the RPC-mechanics note). What does NOT survive is the SELECTION:
            # a new child holds a new session until a thread claims it, so the
            # next `select_thread` re-binds explicitly rather than assuming.
            self._selected = None
        self._session_root.mkdir(parents=True, exist_ok=True)
        # THE OVERLAY MUST EXIST WHENEVER THE ARGV NAMES IT: a `--config` file
        # that is missing is a hard startup error, not a skipped option.
        self._launch.write_overlay()
        child = HarnessChild(self._launch, spawn=self._spawn, log=self._log,
                             environment=self._environment)
        try:
            child.start()
        except BridgeUnavailable:
            self._unavailable = True
            raise
        self._child = child

    def _apply_model(self, child: HarnessChild, model_id: str, *,
                     deadline: float) -> None:
        """`set_model` BEFORE `prompt`, inside the adapter (task 11.6).

        The id sent is the RESOLVED one where the catalog can say so, and the
        requested one otherwise. Today no conformant catalog entry can declare a
        routing rule — the released catalog schema is a CLOSED seven-field entry
        — so the two are always equal and `routing_rule` is truthfully false
        everywhere; task 11.7 records the additive model-catalog release that
        would change that, and this line is already written for it.

        THE PROVIDER ID IS THE INSTALL'S, NOT THE CATALOG ENTRY'S — corrected
        2026-08-19 after the adversarial review's P1-5. This used to send
        `entry.provider_class`, which is a GOVERNANCE data-handling
        classification (`on-tenant`, `self_hosted`, …), not a harness provider
        id. Live, every such `set_model` was refused:

            >>> {"type":"set_model","provider":"self_hosted","modelId":"local-model"}
                {"success":false,"error":"Model not found: self_hosted/local-model"}
            >>> {"type":"set_model","provider":"local-proxy","modelId":"local-model"}
                {"success":true,"data":{"id":"local-model",…}}

        so no turn could ever have been dispatched.

        JUDGEMENT CALL, FLAGGED: the harness provider id now lives on
        `LaunchConfig.provider_id`, the bridge's INSTALL-SIDE declaration —
        the same placement §10 chose for the retrieval backend, and for the same
        reason: which provider an install talks to is an operator fact, and an
        operator must be able to read it where the install is declared. It is
        deliberately NOT on the catalog entry: that schema is a CLOSED
        seven-field shape whose widening is task 11.7's future release, and
        smuggling a harness-routing field into a governance record would be
        exactly the conflation that caused this defect.

        Undeclared, the `provider` key is OMITTED entirely, which lets the
        harness resolve the model id by its own matching — the documented
        `--model` behaviour — rather than being handed a label it must refuse."""

        entry = self._declared_catalog.entry_for(model_id)
        resolved = getattr(entry, "resolved_model_id", None) if entry else None
        frame = {"id": child.next_id("sm"), "type": CMD_SET_MODEL,
                 "modelId": str(resolved) if resolved else model_id}
        provider = self._launch.provider_id
        if isinstance(provider, str) and provider:
            frame["provider"] = provider
        answer = child.request(frame, deadline=deadline, clock=self._clock)
        if not answer.success:
            raise BridgeProtocolError(
                "the harness refused the model this turn selected")

    def _session_path(self, child: HarnessChild, *, deadline: float) -> str | None:
        answer = child.request({"id": child.next_id("gs"), "type": CMD_GET_STATE},
                               deadline=deadline, clock=self._clock)
        path = answer.data.get("sessionFile")
        return path if isinstance(path, str) and path else None

    def _artifact_dir(self) -> Path | None:
        """The artifact directory for the CURRENTLY selected thread's session.

        `ArtifactManager` derives it from the session file path — the sibling
        directory of `<timestamp>_<sessionId>.jsonl` — with no independent
        configuration of its own (verification §3.5)."""

        path = self._sessions.get(self._selected) if self._selected else None
        if not path:
            return None
        session_file = Path(path)
        if session_file.suffix == SESSION_FILE_SUFFIX:
            return session_file.with_suffix("")
        # A session path that does not end in the recorded suffix is taken as
        # given rather than re-derived: guessing at a second layout is how a
        # dereference reads somebody else's directory.
        return session_file

    def _resolve_artifact(self, token: str) -> str:
        identifier = token[len(doxbench_threads.HARNESS_ARTIFACT_SCHEME):]
        directory = self._artifact_dir()
        target = None
        if directory is not None and identifier and "/" not in identifier \
                and identifier not in ("", ".", ".."):
            candidate = directory / identifier
            if candidate.is_file():
                target = candidate
        if target is None:
            return doxbench_threads.elided_note(
                0, "the harness artifact store holds no readable content for "
                   "this reference")
        try:
            size = target.stat().st_size
        except OSError:
            return doxbench_threads.elided_note(
                0, "the harness artifact store could not be read")
        if size > MAX_INLINE_ARTIFACT_BYTES:
            return doxbench_threads.elided_note(
                size, "the spilled content is larger than a sidecar inlines")
        try:
            return target.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return doxbench_threads.elided_note(
                size, "the spilled content is not decodable text")


def _split_artifact_tokens(value: str) -> Iterable[str]:
    """Split a body into artifact references and the prose between them.

    A reference runs from the scheme to the first character that cannot be part
    of one. Deliberately conservative: over-splitting leaves prose intact, while
    under-splitting would swallow a sentence into an elision note."""

    scheme = doxbench_threads.HARNESS_ARTIFACT_SCHEME
    stop = set(" \t\n\r\"'<>)]},;")
    out: list[str] = []
    index = 0
    while True:
        found = value.find(scheme, index)
        if found < 0:
            out.append(value[index:])
            return out
        out.append(value[index:found])
        end = found + len(scheme)
        while end < len(value) and value[end] not in stop:
            end += 1
        out.append(value[found:end])
        index = end


class HarnessThreadMirror:
    """The `ThreadMirror` the bridge supplies (`doxbench_threads.MIRROR_OPERATIONS`).

    ONE method, and it returns nothing — the record is the sidecar, and a mirror
    is TOLD what the record says. What this implementation does with a turn is
    deliberately narrow, and the narrowness is the point:

    * it does NOT write the turn into any harness memory. The launch config pins
      `memory.backend: off` under a dedicated profile, so there is no native
      memory surface to write into, and the mirror re-asserts that rather than
      relying on it — a bridge whose launch config lost the pin refuses to
      mirror rather than quietly starting a second store;
    * it records the thread the turn belongs to against the harness session
      bound to it, which is what makes "one session never serves two threads"
      observable rather than merely intended.

    Two stores claiming to be the same thread is a split brain, and the sidecar
    wins by contract rather than by convention."""

    def __init__(self, bridge: OmpHarnessBridge) -> None:
        self._bridge = bridge
        self.mirrored: list[tuple[str, str]] = []

    def mirror_turn(self, thread, turn) -> None:
        if not self._bridge.launch.declares_memory_off():
            raise BridgeError(
                "refusing to mirror: this bridge's launch config does not pin "
                f"{MEMORY_BACKEND_SETTING}={MEMORY_BACKEND_OFF}, and a harness "
                "with a live memory backend is a second store claiming to be "
                "the thread the sidecar already is")
        self._bridge.select_thread(thread.document)
        self.mirrored.append((thread.document, turn.turn_id))
