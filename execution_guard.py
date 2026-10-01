"""Persistent operational guardrails for live order orchestration.

These are not strategy limits. They prevent duplicate submissions and unsafe
blind retries when broker state is unknown.
"""
import os
from pathlib import Path
import sqlite3
from datetime import datetime, timezone

DB_PATH = Path(__file__).parent / "data" / "trader.db"


def _db_path():
    return Path(os.getenv("TRADER_DB", str(DB_PATH)))


def _connect():
    path = _db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.execute("""CREATE TABLE IF NOT EXISTS order_guard (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        symbol TEXT NOT NULL,
        side TEXT NOT NULL,
        quantity REAL NOT NULL,
        client_key TEXT NOT NULL UNIQUE,
        broker_order_id TEXT,
        status TEXT NOT NULL,
        attempts INTEGER NOT NULL DEFAULT 1,
        last_checked_at TEXT
    )""")
    con.commit()
    return con


def client_key(symbol, side, quantity, intent_id):
    return f"{symbol.upper()}:{side.upper()}:{quantity}:{intent_id}"


def reserve(symbol, side, quantity, intent_id):
    key = client_key(symbol, side, quantity, intent_id)
    con = _connect()
    try:
        con.execute(
            """INSERT INTO order_guard
            (created_at,symbol,side,quantity,client_key,status,last_checked_at)
            VALUES (?,?,?,?,?,?,?)""",
            (datetime.now(timezone.utc).isoformat(), symbol.upper(),
             side.upper(), quantity, key, "reserved",
             datetime.now(timezone.utc).isoformat()))
        con.commit()
        return True, key
    except sqlite3.IntegrityError:
        return False, key
    finally:
        con.close()


def mark_submitted(client_key_value, broker_order_id):
    con = _connect()
    con.execute(
        """UPDATE order_guard SET broker_order_id=?, status='submitted',
           last_checked_at=? WHERE client_key=?""",
        (str(broker_order_id), datetime.now(timezone.utc).isoformat(),
         client_key_value))
    con.commit()
    con.close()


def mark_status(client_key_value, status):
    con = _connect()
    con.execute(
        """UPDATE order_guard SET status=?, last_checked_at=?
           WHERE client_key=?""",
        (status, datetime.now(timezone.utc).isoformat(),
         client_key_value))
    con.commit()
    con.close()


def unresolved():
    con = _connect()
    rows = con.execute(
        """SELECT symbol,side,quantity,client_key,broker_order_id,status,
                  created_at,last_checked_at
           FROM order_guard
           WHERE status IN ('reserved','submitted','unknown')
           ORDER BY id DESC""").fetchall()
    con.close()
    return rows
