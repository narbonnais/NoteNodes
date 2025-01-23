import sqlite3
import os

# Assurer que le dossier data existe
data_dir = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(data_dir, exist_ok=True)
DB_PATH = os.path.join(data_dir, "notes.db")

def get_connection():
    """Retourne une connexion SQLite."""
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    """Crée la table si elle n'existe pas encore."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_id INTEGER,
            title TEXT NOT NULL,
            content TEXT,
            collapsed INTEGER DEFAULT 0,
            FOREIGN KEY(parent_id) REFERENCES nodes(id)
        );
    """)
    
    # Add settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        );
    """)
    conn.commit()
    conn.close()

def create_node(title, parent_id=None, content="", collapsed=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO nodes (title, parent_id, content, collapsed)
        VALUES (?, ?, ?, ?)
    """, (title, parent_id, content, collapsed))
    conn.commit()
    node_id = cursor.lastrowid
    conn.close()
    return node_id

def get_node(node_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nodes WHERE id = ?", (node_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_children(parent_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if parent_id is None:
        cursor.execute("SELECT * FROM nodes WHERE parent_id IS NULL")
    else:
        cursor.execute("SELECT * FROM nodes WHERE parent_id = ?", (parent_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_node(node_id, title=None, content=None, collapsed=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    fields = []
    values = []
    
    if title is not None:
        fields.append("title = ?")
        values.append(title)
    if content is not None:
        fields.append("content = ?")
        values.append(content)
    if collapsed is not None:
        fields.append("collapsed = ?")
        values.append(collapsed)
        
    if not fields:
        return
        
    values.append(node_id)
    
    sql = f"UPDATE nodes SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(sql, tuple(values))
    conn.commit()
    conn.close()

def delete_node(node_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Récupérer les enfants
    cursor.execute("SELECT id FROM nodes WHERE parent_id = ?", (node_id,))
    child_ids = cursor.fetchall()
    for (child_id,) in child_ids:
        delete_node(child_id)  # récursion
    
    cursor.execute("DELETE FROM nodes WHERE id = ?", (node_id,))
    conn.commit()
    conn.close()

def update_node_parent(node_id, new_parent_id):
    """Met à jour le parent d'un nœud."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE nodes 
        SET parent_id = ? 
        WHERE id = ?
    """, (new_parent_id, node_id))
    conn.commit()
    conn.close()

def get_setting(key, default=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else default

def set_setting(key, value):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO settings (key, value)
        VALUES (?, ?)
    """, (key, value))
    conn.commit()
    conn.close() 