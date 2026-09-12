from pathlib import Path
import os

KILL_FILE = Path(__file__).parent / "data" / "KILL_SWITCH"

def mode():
    return os.getenv("TRADING_MODE", "paper").lower()

def kill_active():
    return KILL_FILE.exists()

def set_kill(active: bool):
    KILL_FILE.parent.mkdir(parents=True, exist_ok=True)
    if active:
        KILL_FILE.write_text("KILL SWITCH ACTIVE\n")
    elif KILL_FILE.exists():
        KILL_FILE.unlink()
