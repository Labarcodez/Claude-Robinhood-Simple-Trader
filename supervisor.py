#!/usr/bin/env python3
"""Always-on Claude trading supervisor.

Claude remains responsible for market research and Robinhood MCP actions.
This process owns scheduling, single-cycle locking, local state and recovery.
Set CLAUDE_COMMAND to the exact Claude Code headless command for your machine.
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

from journal import log_event
from state import kill_active

ROOT = Path(__file__).parent
INTERVAL = max(5, int(os.getenv("TRADING_INTERVAL_SECONDS", "60")))
TIMEOUT = max(30, int(os.getenv("CLAUDE_CYCLE_TIMEOUT_SECONDS", "600")))
CLAUDE_COMMAND = os.getenv("CLAUDE_COMMAND", "claude -p")
PROMPT_FILE = ROOT / "PROMPT.md"
LOCK_FILE = ROOT / "data" / "SUPERVISOR.lock"

def acquire_lock():
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = LOCK_FILE.open("x")
        fd.write(str(os.getpid()))
        fd.close()
        return True
    except FileExistsError:
        return False

def release_lock():
    try:
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
</SUPERVISOR_CYCLE>
"""

def run_once():
    if kill_active():
        log_event("supervisor_skip", "kill switch active")
        return 0
    if not acquire_lock():
        log_event("supervisor_skip", "another supervisor cycle is running")
        return 0
    try:
        command = shlex.split(CLAUDE_COMMAND)
        if not command:
            raise RuntimeError("CLAUDE_COMMAND is empty")
        log_event("supervisor_start", f"command={CLAUDE_COMMAND}")
        result = subprocess.run(
            command, input=build_prompt(), text=True, cwd=ROOT, timeout=TIMEOUT
        )
        log_event("supervisor_finish", f"returncode={result.returncode}")
        return result.returncode
    except FileNotFoundError:
        log_event("supervisor_error",
                  "Claude command not found; set CLAUDE_COMMAND")
        return 127
    except subprocess.TimeoutExpired:
        log_event("supervisor_timeout", f"timeout_seconds={TIMEOUT}")
        return 124
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
        time.sleep(max(1, INTERVAL - (time.monotonic() - started)))

if __name__ == "__main__":
    main()
