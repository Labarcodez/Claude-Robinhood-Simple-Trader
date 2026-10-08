import argparse
from state import kill_active, mode, set_kill
from risk import load_config
from journal import connect, recent, log_event
from execution_guard import unresolved

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
    print("risk_mode:", c.get("mode", "account_aware"))
    print("portfolio_limits: NONE")
    print("position_limits: NONE")
    print("daily_loss_limit: NONE")
    print("order_size_limit: NONE")
    print("new_positions_per_day_limit: NONE")
    print("\nUnresolved local order records:")
    for row in unresolved():
        print(row)
    print("\nRecent decisions:")
    for row in recent(10):
        print(row)


def start():
    """Start the always-on autonomous supervisor."""
    from supervisor import main as supervisor_main
    supervisor_main()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kill", action="store_true")
    p.add_argument("--unkill", action="store_true")
    p.add_argument("--status", action="store_true")
    p.add_argument("--start", action="store_true",
                   help="Start the always-on autonomous trader (also the default).")
    args = p.parse_args()

    if args.kill:
        set_kill(True)
        print("Kill switch ACTIVATED.")
        return
    if args.unkill:
        set_kill(False)
        print("Kill switch CLEARED.")
        return
    if args.status:
        status()
        return

    # Default behavior is fully autonomous operation; --start is retained as
    # an explicit alias for scripts and users who prefer a visible flag.
    start()


if __name__ == "__main__":
    main()
