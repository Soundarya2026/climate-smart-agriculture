import sqlite3

DB_NAME = "agriculture.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            farmer TEXT NOT NULL,
            area REAL NOT NULL,
            production REAL NOT NULL,
            status TEXT DEFAULT 'sowing the crops'
        )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM crops"
    ).fetchone()[0]

    if count == 0:
        conn.executemany("""
            INSERT INTO crops
            (name, farmer, area, production, status)
            VALUES (?, ?, ?, ?, ?)
        """, [
            ("Rice", "Arun", 5.5, 120, "Growing"),
            ("Wheat", "Kumar", 3.0, 80, "Harvested"),
            ("Tomato", "Ravi", 2.5, 60, "Growing"),
            ("Maize", "shalin", 4.0, 95, "Growing")
        ])

    conn.commit()
    conn.close()
