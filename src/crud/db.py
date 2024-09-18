import sqlite3
import os

conn = sqlite3.connect('jow.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Recipes(
    id TEXT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    description TEXT,
    preparation_time INT ,
    cooking_time INT ,
    preparation_extra_time_per_cover INT ,
    covers_count INT 
);               
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Ingredient(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    quantity FLOAT8,
    unit TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS List_ingredients(
    id SERIAL PRIMARY KEY,
    id_ingredients INT NOT NULL,
    id_recipe TEXT NOT NULL,
    FOREIGN KEY (id_ingredients) REFERENCES Ingredient(id),
    FOREIGN KEY (id_recipe) REFERENCES Recipe(id)
);
''')




# Insérer des données factices
# cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 25)")
# cursor.execute("INSERT INTO users (name, age) VALUES ('Bob', 30)")
# conn.commit()
conn.close()
