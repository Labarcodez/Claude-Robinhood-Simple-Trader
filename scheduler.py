import os, time, subprocess
from pathlib import Path

ROOT = Path(__file__).parent
interval = int(os.getenv("TRADING_INTERVAL_SECONDS", "900"))
print(f"Scheduler started. Interval: {interval}s. Ctrl+C to stop.")
while True:
    subprocess.run(["python", str(ROOT / "run.py")], cwd=ROOT)
    time.sleep(interval)
