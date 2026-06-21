import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.environ.get('DB_PATH', os.path.join(os.path.dirname(__file__), 'bierbook.db'))


@contextmanager
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS breweries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                country TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS bottles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brewery_id INTEGER NOT NULL REFERENCES breweries(id),
                bezeichnung TEXT NOT NULL,
                style TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS bottle_photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bottle_id INTEGER NOT NULL REFERENCES bottles(id) ON DELETE CASCADE,
                filename TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)


def _get_or_create_brewery(conn, name, country=None):
    row = conn.execute("SELECT id, country FROM breweries WHERE name = ?", (name,)).fetchone()
    if row:
        if country and not row['country']:
            conn.execute("UPDATE breweries SET country=? WHERE id=?", (country, row['id']))
        return row['id']
    conn.execute("INSERT INTO breweries (name, country) VALUES (?, ?)", (name, country))
    return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def brewery_autocomplete(q):
    with db() as conn:
        rows = conn.execute(
            "SELECT id, name, country FROM breweries WHERE name LIKE ? ORDER BY name LIMIT 10",
            (f"%{q}%",)
        ).fetchall()
    return [dict(r) for r in rows]


def style_autocomplete(q):
    with db() as conn:
        rows = conn.execute(
            "SELECT DISTINCT style FROM bottles WHERE style LIKE ? AND style IS NOT NULL ORDER BY style LIMIT 10",
            (f"%{q}%",)
        ).fetchall()
    return [r['style'] for r in rows]


def list_bottles(search=None, brewery=None, style=None, country=None):
    query = """
        SELECT bo.id, bo.bezeichnung, bo.style, bo.notes, bo.created_at,
               br.id as brewery_id, br.name as brewery_name, br.country,
               (SELECT filename FROM bottle_photos WHERE bottle_id=bo.id ORDER BY id LIMIT 1) as thumb
        FROM bottles bo
        JOIN breweries br ON bo.brewery_id = br.id
        WHERE 1=1
    """
    params = []
    if search:
        query += " AND (br.name LIKE ? OR bo.bezeichnung LIKE ? OR bo.style LIKE ? OR bo.notes LIKE ?)"
        params.extend([f"%{search}%"] * 4)
    if brewery:
        query += " AND br.id = ?"
        params.append(brewery)
    if style:
        query += " AND bo.style LIKE ?"
        params.append(f"%{style}%")
    if country:
        query += " AND br.country LIKE ?"
        params.append(f"%{country}%")
    query += " ORDER BY bo.created_at DESC"
    with db() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(r) for r in rows]


def get_bottle(bottle_id):
    with db() as conn:
        row = conn.execute("""
            SELECT bo.id, bo.bezeichnung, bo.style, bo.notes, bo.created_at,
                   br.id as brewery_id, br.name as brewery_name, br.country
            FROM bottles bo JOIN breweries br ON bo.brewery_id = br.id
            WHERE bo.id = ?
        """, (bottle_id,)).fetchone()
        if not row:
            return None
        bottle = dict(row)
        photos = conn.execute(
            "SELECT id, filename FROM bottle_photos WHERE bottle_id = ? ORDER BY id",
            (bottle_id,)
        ).fetchall()
        bottle['photos'] = [dict(p) for p in photos]
    return bottle


def create_bottle(brewery_name, brewery_country, bezeichnung, style, notes):
    with db() as conn:
        brewery_id = _get_or_create_brewery(conn, brewery_name, brewery_country or None)
        conn.execute(
            "INSERT INTO bottles (brewery_id, bezeichnung, style, notes) VALUES (?, ?, ?, ?)",
            (brewery_id, bezeichnung, style or None, notes or None)
        )
        return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def update_bottle(bottle_id, brewery_name, brewery_country, bezeichnung, style, notes):
    with db() as conn:
        brewery_id = _get_or_create_brewery(conn, brewery_name, brewery_country or None)
        conn.execute(
            "UPDATE bottles SET brewery_id=?, bezeichnung=?, style=?, notes=? WHERE id=?",
            (brewery_id, bezeichnung, style or None, notes or None, bottle_id)
        )


def delete_bottle(bottle_id):
    with db() as conn:
        conn.execute("DELETE FROM bottles WHERE id=?", (bottle_id,))


def add_photo(bottle_id, filename):
    with db() as conn:
        conn.execute(
            "INSERT INTO bottle_photos (bottle_id, filename) VALUES (?, ?)",
            (bottle_id, filename)
        )


def delete_photo(photo_id):
    with db() as conn:
        row = conn.execute("SELECT filename FROM bottle_photos WHERE id=?", (photo_id,)).fetchone()
        if not row:
            return None
        conn.execute("DELETE FROM bottle_photos WHERE id=?", (photo_id,))
        return row['filename']


def list_breweries():
    with db() as conn:
        rows = conn.execute("""
            SELECT br.id, br.name, br.country, COUNT(bo.id) as bottle_count,
                   (SELECT bp.filename FROM bottle_photos bp
                    JOIN bottles bo2 ON bp.bottle_id = bo2.id
                    WHERE bo2.brewery_id = br.id ORDER BY bp.id LIMIT 1) as thumb
            FROM breweries br
            LEFT JOIN bottles bo ON bo.brewery_id = br.id
            GROUP BY br.id
            ORDER BY br.name
        """).fetchall()
    return [dict(r) for r in rows]


def get_brewery_with_bottles(brewery_id):
    with db() as conn:
        brewery = conn.execute("SELECT * FROM breweries WHERE id=?", (brewery_id,)).fetchone()
        if not brewery:
            return None, None
        rows = conn.execute("""
            SELECT bo.id, bo.bezeichnung, bo.style, bo.notes, bo.created_at,
                   (SELECT filename FROM bottle_photos WHERE bottle_id=bo.id ORDER BY id LIMIT 1) as thumb
            FROM bottles bo WHERE bo.brewery_id=? ORDER BY bo.created_at DESC
        """, (brewery_id,)).fetchall()
    return dict(brewery), [dict(r) for r in rows]


def update_brewery(brewery_id, name, country):
    try:
        with db() as conn:
            conn.execute(
                "UPDATE breweries SET name=?, country=? WHERE id=?",
                (name, country or None, brewery_id)
            )
        return True, None
    except sqlite3.IntegrityError:
        return False, "Eine Brauerei mit diesem Namen existiert bereits"


def delete_brewery(brewery_id):
    with db() as conn:
        count = conn.execute("SELECT COUNT(*) FROM bottles WHERE brewery_id=?", (brewery_id,)).fetchone()[0]
        if count:
            plural = 'n' if count != 1 else ''
            return False, f"Brauerei hat noch {count} Flasche{plural} — erst die Einträge ändern oder löschen"
        conn.execute("DELETE FROM breweries WHERE id=?", (brewery_id,))
        return True, None
