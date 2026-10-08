#!/usr/bin/env python3
"""Always-on Claude trading supervisor.

Claude remains responsible for market research and Robinhood MCP actions.
This process owns scheduling, single-cycle locking, local state and recovery.
"""

import os
import shlex
import shutil
import signal
import subprocess
import time
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from journal import log_event
from state import kill_active

ROOT = Path(__file__).parent
INTERVAL = max(5, int(os.getenv("TRADING_INTERVAL_SECONDS", "60")))
TIMEOUT = max(30, int(os.getenv("CLAUDE_CYCLE_TIMEOUT_SECONDS", "600")))
CLAUDE_COMMAND = os.getenv("CLAUDE_COMMAND", "claude -p")
PROMPT_FILE = ROOT / "PROMPT.md"
LOCK_FILE = ROOT / "data" / "SUPERVISOR.lock"


def _command_available(command):
    executable = command[0]
    return bool(shutil.which(executable) or Path(executable).expanduser().exists())


def _pid_alive(pid):
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def acquire_lock():
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = LOCK_FILE.open("x")
        fd.write(str(os.getpid()))
        fd.close()
        return True
    except FileExistsError:
        try:
            old_pid = int(LOCK_FILE.read_text().strip())
        except (ValueError, OSError):
            old_pid = 0
        if old_pid and _pid_alive(old_pid):
            return False
        try:
            LOCK_FILE.unlink()
        except FileNotFoundError:
            pass
        try:
            fd = LOCK_FILE.open("x")
            fd.write(str(os.getpid()))
            fd.close()
            log_event("supervisor_recovered_lock", f"stale_pid={old_pid}")
            return True
        except FileExistsError:
            return False


def release_lock():
    try:
        if LOCK_FILE.read_text().strip() == str(os.getpid()):
            LOCK_FILE.unlink()
    except FileNotFoundError:
        pass


def build_prompt():
    return PROMPT_FILE.read_text() + """
<SUPERVISOR_CYCLE>
This is an automated live cycle. Read current Robinhood account, positions,
orders and buying power first. Reconcile unresolved local order-guard records
before considering any new order. Execute the full workflow using the connected
Robinhood MCP. Never invent data or claim a fill without broker confirmation.
If the local kill switch is active, take no trading action.
Treat this cycle as a complete research-to-execution pass: manage existing
positions first, then perform broad multi-pass discovery and deeply validate
only the strongest candidates before considering a new order.
</SUPERVISOR_CYCLE>
"""


def run_once():
    if kill_active():
        log_event("supervisor_skip", "kill switch active")
        return 0
    if not PROMPT_FILE.exists():
        log_event("supervisor_error", "PROMPT.md is missing")
        return 1

    try:
        command = shlex.split(CLAUDE_COMMAND)
    except ValueError as exc:
        log_event("supervisor_error", f"invalid CLAUDE_COMMAND: {exc!r}")
        return 1

    if not command:
        log_event("supervisor_error", "CLAUDE_COMMAND is empty")
        return 1
    if not _command_available(command):
        log_event("supervisor_error",
                  f"Claude executable unavailable: {command[0]}")
        return 127

    if not acquire_lock():
        log_event("supervisor_skip", "another supervisor cycle is running")
        return 0

    process = None
    try:
        log_event("supervisor_start", f"command={CLAUDE_COMMAND}")
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            text=True,
            cwd=ROOT,
            start_new_session=True,
        )
        process.communicate(input=build_prompt(), timeout=TIMEOUT)
        log_event("supervisor_finish", f"returncode={process.returncode}")
        return process.returncode or 0
    except subprocess.TimeoutExpired:
        log_event("supervisor_timeout", f"timeout_seconds={TIMEOUT}")
        if process is not None and process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=10)
            except (OSError, subprocess.TimeoutExpired):
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except OSError:
                    pass
        return 124
    except BrokenPipeError:
        log_event("supervisor_error", "Claude process closed stdin early")
        return 1
    except Exception as exc:
        log_event("supervisor_error", repr(exc))
        return 1
    finally:
        release_lock()


def main():
    print(f"Claude supervisor started: interval={INTERVAL}s "
          f"timeout={TIMEOUT}s command={CLAUDE_COMMAND!r}")
    while True:
        started = time.monotonic()
        run_once()
        elapsed = time.monotonic() - started
        time.sleep(max(1, INTERVAL - elapsed))


if __name__ == "__main__":
    main()
