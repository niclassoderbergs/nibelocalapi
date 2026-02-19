import sqlite3
from datetime import datetime, timedelta

DB_FILE = 'history.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS history 
                        (point_id INTEGER, value REAL, timestamp DATETIME)''')

def save_value(pid, value):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO history (point_id, value, timestamp) VALUES (?, ?, ?)",
                     (pid, value, datetime.now()))

def get_history(pid, hours=24):
    since = datetime.now() - timedelta(hours=hours)
    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute("SELECT timestamp, value FROM history WHERE point_id = ? AND timestamp > ? ORDER BY timestamp ASC",
                            (pid, since)).fetchall()
    return {"labels": [r[0][11:16] for r in rows], "values": [r[1] for r in rows]}