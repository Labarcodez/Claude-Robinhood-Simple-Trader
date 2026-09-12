import argparse
from state import kill_active, mode, set_kill
from risk import load_config
from journal import connect, recent, log_event

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

def status():
    c = load_config()
    connect().close()
    print("=== SIMPLE CLAUDE ROBINHOOD TRADER ===")
    print("mode:", mode())
    print("kill_switch:", kill_active())
    print("max_position_pct:", c["max_position_pct"])
    print("max_total_exposure_pct:", c["max_total_exposure_pct"])
    print("max_daily_loss_pct:", c["max_daily_loss_pct"])
    print("max_open_positions:", c["max_open_positions"])
    print("\nRecent decisions:")
    for row in recent(10):
        print(row)

def cycle():
    if kill_active():
        print("KILL SWITCH ACTIVE — no new trading activity.")
        return
    print("Trading cycle ready.")
    print("Claude should execute CLAUDE.md / PROMPT.md using the connected Robinhood MCP.")
    log_event("cycle_ready", f"mode={mode()}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kill", action="store_true")
    p.add_argument("--unkill", action="store_true")
    p.add_argument("--status", action="store_true")
    args = p.parse_args()
    if args.kill:
        set_kill(True); print("Kill switch ACTIVATED."); return
    if args.unkill:
        set_kill(False); print("Kill switch CLEARED."); return
    if args.status:
        status(); return
    cycle()

if __name__ == "__main__":
    main()
