from pathlib import Path
import sqlite3, json
from datetime import datetime, timezone

DB_PATH = Path(__file__).parent / "data" / "trader.db"

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute("""CREATE TABLE IF NOT EXISTS decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL, mode TEXT NOT NULL, symbol TEXT,
        action TEXT NOT NULL, notional REAL, confidence REAL,
        thesis TEXT, risk_reason TEXT, broker_order_id TEXT,
        broker_status TEXT, metadata_json TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL, event TEXT NOT NULL, detail TEXT)""")
    con.commit()
    return con

def log_decision(**kwargs):
    con = connect()
    con.execute("""INSERT INTO decisions
    (ts,mode,symbol,action,notional,confidence,thesis,risk_reason,
     broker_order_id,broker_status,metadata_json)
    VALUES (?,?,?,?,?,?,?,?,?,?,?)""", (
        datetime.now(timezone.utc).isoformat(),
        kwargs.get("mode","paper"), kwargs.get("symbol"),
        kwargs.get("action","NO_ACTION"), kwargs.get("notional"),
        kwargs.get("confidence"), kwargs.get("thesis"),
        kwargs.get("risk_reason"), kwargs.get("broker_order_id"),
        kwargs.get("broker_status"),
        json.dumps(kwargs.get("metadata",{}), default=str)))
    con.commit()
    con.close()

def log_event(event, detail=""):
    con = connect()
    con.execute("INSERT INTO events (ts,event,detail) VALUES (?,?,?)",
                (datetime.now(timezone.utc).isoformat(), event, detail))
    con.commit()
    con.close()

def recent(limit=20):
    con = connect()
    rows = con.execute(
        "SELECT ts,mode,symbol,action,notional,confidence,thesis,risk_reason,broker_order_id,broker_status "
        "FROM decisions ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    con.close()
    return rows
