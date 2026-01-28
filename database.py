"""Database operations for Jow Gourmet app."""
import sqlite3
import json
import streamlit as st

DB_PATH = 'jow_favorites.db'


def get_db_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@st.cache_resource
def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            ingredients TEXT,
            url TEXT,
            image_url TEXT,
            prepa_time INTEGER,
            cooking_time INTEGER,
            covers INTEGER,
            adaptedFor INTEGER,
            adaptationFactor FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Add columns if they don't exist (migration)
    try:
        c.execute('ALTER TABLE favorites ADD COLUMN image_url TEXT')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE favorites ADD COLUMN prepa_time INTEGER')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE favorites ADD COLUMN cooking_time INTEGER')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE favorites ADD COLUMN covers INTEGER')
    except sqlite3.OperationalError:
        pass
    
    conn.commit()
    conn.close()


def add_favorite(recipe, adapted_for, adaptation_factor):
    """Add a recipe to favorites."""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Serialize ingredients
    ings = []
    for ing in getattr(recipe, 'ingredients', []):
        ings.append({
            'name': getattr(ing, 'name', 'Inconnu'),
            'quantity': str(getattr(ing, 'quantity', '')),
            'unit': getattr(ing, 'unit', '')
        })
    
    c.execute(
        """INSERT INTO favorites 
           (name, description, ingredients, url, image_url, prepa_time, cooking_time, covers, adaptedFor, adaptationFactor) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            getattr(recipe, 'name', 'N/A'),
            getattr(recipe, 'description', ''),
            json.dumps(ings),
            getattr(recipe, 'url', ''),
            getattr(recipe, 'imageUrl', ''),
            getattr(recipe, 'preparationTime', 0),
            getattr(recipe, 'cookingTime', 0),
            getattr(recipe, 'coversCount', 0),
            adapted_for,
            adaptation_factor
        )
    )
    conn.commit()
    conn.close()


def remove_favorite(fav_id):
    """Remove a favorite by ID."""
    conn = get_db_connection()
    conn.execute("DELETE FROM favorites WHERE id = ?", (fav_id,))
    conn.commit()
    conn.close()


def get_all_favorites():
    """Get all favorites from the database."""
    import pandas as pd
    conn = get_db_connection()
    favs = pd.read_sql_query("SELECT * FROM favorites ORDER BY created_at DESC", conn)
    conn.close()
    return favs


def clear_all_favorites():
    """Clear all favorites from the database."""
    conn = get_db_connection()
    conn.execute("DELETE FROM favorites")
    conn.commit()
    conn.close()
