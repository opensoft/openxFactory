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
# THE FLAG SPELLING IS THIS MODULE'S ONE UNVERIFIED LAUNCH DETAIL, and it is
# isolated here on purpose: the findings record the SETTING (its name, its enum,
# its default, its resolution function) but not the CLI spelling of a per-setting
# override. A companion test pins the produced argv, so correcting the spelling
# is a one-line change to this constant that a test will confirm — not a hunt
# through a launcher.
SETTING_FLAG = "--setting"
MEMORY_BACKEND_SETTING = "memory.backend"
MEMORY_BACKEND_OFF = "off"

BRIDGE_SETTINGS: tuple[tuple[str, str], ...] = (
    (MEMORY_BACKEND_SETTING, MEMORY_BACKEND_OFF),
)

# The ONLY environment variables a bridge child inherits. An ALLOWLIST rather
# than a denylist, because a denylist of credential-shaped names is a list
# somebody has to keep up with, and the one it misses is the one that leaks. A
# harness that genuinely needs another variable gains it HERE, visibly, in a
# diff a reviewer reads.
INHERITED_ENVIRONMENT: tuple[str, ...] = ("PATH", "HOME", "LANG", "LC_ALL", "TMPDIR")


@dataclasses.dataclass(frozen=True, slots=True)
class LaunchConfig:
    """Everything the bridge needs to start ONE harness child, as data.

    Data rather than code so a test can assert on the argv and the environment
    without starting anything, and so an operator reading a launch line sees the
    same tuple this module builds."""

    session_dir: Path
    command: str = HARNESS_COMMAND
    profile: str = BRIDGE_PROFILE
    settings: tuple[tuple[str, str], ...] = BRIDGE_SETTINGS
    extra_args: tuple[str, ...] = ()

    def argv(self) -> tuple[str, ...]:
        args = [self.command, MODE_FLAG, MODE_RPC,
                PROFILE_FLAG, self.profile,
                SESSION_DIR_FLAG, str(self.session_dir)]
        for name, value in self.settings:
            args.extend([SETTING_FLAG, f"{name}={value}"])
        args.extend(self.extra_args)
        return tuple(args)

    def environment(self, base: Mapping[str, str] | None = None) -> dict:
        return child_environment(os.environ if base is None else base)

    def declares_memory_off(self) -> bool:
        """The property task 11.5's sentence turns on, answerable without
        parsing an argv string."""
        return (MEMORY_BACKEND_SETTING, MEMORY_BACKEND_OFF) in self.settings


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

# The RECORDED shape of a slash command: there is no distinct RPC command type
# for `/shake`; it rides the same generic slash-command-over-`prompt` channel as
# every other builtin (verification §3.6, verbatim).
SHAKE_MODE_ELIDE = "elide"
SHAKE_MODE_IMAGES = "images"
SHAKE_MODES: tuple[str, ...] = (SHAKE_MODE_ELIDE, SHAKE_MODE_IMAGES)

# WHERE THE ASSISTANT'S TEXT ARRIVES. Verification §3.2 records that the reply
# text appears "in the subsequent `message_update` deltas" and that the turn ends
# at a terminal `agent_end`; it does not record the delta frame's own field
# spelling. The candidate spellings are declared HERE, in one closed tuple read
# in one place, rather than guessed at three call sites — so a correction is one
# line and a companion test pins the reader against each spelling.
ASSISTANT_TEXT_FIELDS: tuple[str, ...] = ("text", "delta", "content", "message")

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

    @property
    def agent_invoked(self) -> bool:
        return bool(self.data.get("agentInvoked", False))


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

# What a single frame may be. A harness that answered with an unbounded line
# would otherwise let a child spend the serve's memory.
MAX_FRAME_BYTES = 4 * 1024 * 1024

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
                for raw in stream:
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
                clock: Callable[[], float]) -> HarnessResponse:
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
        return self._await_response(request_id, deadline=deadline, clock=clock)

    def _await_response(self, request_id: str, *, deadline: float,
                        clock: Callable[[], float]) -> HarnessResponse:
        outputs: list[str] = []
        assistant: list[str] = []
        ended = False
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
                assistant.append(_assistant_text_of(frame))
                continue
            if kind == FRAME_AGENT_END:
                ended = True
                final = _assistant_text_of(frame)
                if final:
                    assistant.append(final)
                if settled is not None:
                    break
                continue
            if kind != FRAME_RESPONSE:
                continue
            if frame.get("id") != request_id:
                continue
            data = frame.get("data")
            settled = HarnessResponse(
                command=str(frame.get("command", "")),
                success=bool(frame.get("success", False)),
                data=data if isinstance(data, Mapping) else {},
                command_output=tuple(outputs),
                assistant_text="".join(assistant),
                agent_ended=ended)
            # A command that did NOT invoke the agent settles at its response
            # (verification §3.6's `/shake` round trip is exactly this); one
            # that DID keeps reading until the terminal `agent_end`.
            if not settled.agent_invoked or ended:
                if not settled.agent_invoked:
                    self._drain_trailing(outputs, assistant, deadline=deadline,
                                         clock=clock)
                break
        return dataclasses.replace(
            settled, command_output=tuple(outputs),
            assistant_text="".join(assistant), agent_ended=ended)

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
                assistant.append(_assistant_text_of(frame))


def _assistant_text_of(frame: Mapping[str, object]) -> str:
    """The assistant text carried by a delta or terminal frame, read through the
    ONE declared spelling set."""

    for container in (frame, frame.get("data") if isinstance(
            frame.get("data"), Mapping) else {}):
        if not isinstance(container, Mapping):
            continue
        for field in ASSISTANT_TEXT_FIELDS:
            value = container.get(field)
            if isinstance(value, str):
                return value
    return ""


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

        if not self._unavailable:
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

        with self._lock:
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

        with self._lock:
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
        with self._lock:
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
        would change that, and this line is already written for it."""

        entry = self._declared_catalog.entry_for(model_id)
        resolved = getattr(entry, "resolved_model_id", None) if entry else None
        frame = {"id": child.next_id("sm"), "type": CMD_SET_MODEL,
                 "modelId": str(resolved) if resolved else model_id}
        provider = getattr(entry, "provider_class", None) if entry else None
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
